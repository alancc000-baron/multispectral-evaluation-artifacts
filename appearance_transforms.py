"""Tone mapping and rain overlay used during initial candidate generation."""
import hashlib
import json
from pathlib import Path

import cv2
import numpy as np

CONFIG = json.loads(Path(__file__).with_name("initial-generation.json").read_text(encoding="utf-8"))
SEED = CONFIG["seed"]

def tone(image, condition):
    prefix = 'twilight' if condition == 'twilight' else 'rainy_night'
    target, exposure = CONFIG[prefix + '_mean_target'], CONFIG[prefix + '_exposure']
    gains = np.array(CONFIG[prefix + '_gains'], np.float32)
    small = cv2.resize(image, (96, 96), interpolation=cv2.INTER_AREA).astype(np.float32) / 255
    histogram = np.stack([np.bincount(np.rint(small[..., channel] * 255).astype(np.uint8).ravel(), minlength=256) for channel in range(3)], axis=1)
    histogram = histogram.astype(np.float32) / (96 * 96)
    levels = np.arange(256, dtype=np.float32)[:, None] / 255
    low, high = CONFIG[prefix + '_gamma_min'], CONFIG[prefix + '_gamma_max']
    for _ in range(14):
        gamma = (low + high) / 2
        transformed = np.clip(levels ** gamma * exposure * gains, 0, 1)
        mean = float((histogram * transformed).sum(axis=0) @ np.array([.299, .587, .114], np.float32) * 255)
        if mean > target:
            low = gamma
        else:
            high = gamma
    gamma = (low + high) / 2
    mapped_mean = float((histogram * np.clip(levels ** gamma * exposure * gains, 0, 1)).sum(axis=0) @ np.array([.299, .587, .114], np.float32) * 255)
    if mapped_mean > target:
        exposure *= target / mapped_mean
    lut = np.rint(np.clip((np.arange(256, dtype=np.float32)[:, None] / 255) ** gamma * exposure * gains * 255, 0, 255)).astype(np.uint8)
    result = np.empty_like(image)
    for channel in range(3):
        result[..., channel] = cv2.LUT(image[..., channel], lut[:, channel])
    return result, gamma, exposure


def rain_layer(image, source_key):
    height, width = image.shape[:2]
    seed = int.from_bytes(hashlib.sha256((str(SEED) + source_key).encode()).digest()[:8], 'little')
    rng = np.random.default_rng(seed)
    mask = np.zeros((height, width), np.uint8)
    scale = width / 640
    length = max(4, round(CONFIG['rain_length_at640'] * scale))
    slant = round(CONFIG['rain_slant_at640'] * scale)
    count = round(width * height / 1e6 * CONFIG['rain_density_per_megapixel'])
    for x, y, value in zip(rng.integers(0, width, count), rng.integers(-length, height, count), rng.integers(100, 256, count)):
        cv2.line(mask, (int(x), int(y)), (int(x + slant), int(y + length)), int(value), max(1, round(scale)), cv2.LINE_AA)
    mask = cv2.GaussianBlur(mask, (3, 3), .65).astype(np.float32) / 255 * CONFIG['rain_opacity']
    result = image.astype(np.float32) * (1 - mask[..., None]) + np.array([175, 185, 200], np.float32) * mask[..., None]
    return np.rint(result).astype(np.uint8)
