# Multispectral evaluation artifacts

This package accompanies the TICRE-Net study on visible–thermal pedestrian detection. It provides the final expanded dataset indices, recorded evaluation results, generation settings, and the initial tone-mapping and rain-overlay functions.

## Dataset indices

The nine gzip-compressed CSV files contain the samples admitted to the final train, validation, and test lists. They contain 115,398 pairs across KAIST, LLVIP, and SWVID. `source_id` identifies the source sample shared by its appearance variants, and `image_id` identifies the individual version. `condition` distinguishes original images, synthetic twilight, and synthetic rainy-night versions. Illumination labels are 0 for night, 1 for day, and 2 for twilight. Synthetic variants inherit the source split. `split-counts.json` records the counts.

Access original imagery and annotations through the dataset providers under their terms:

- [KAIST benchmark](https://soonminhwang.github.io/rgbt-ped-detection/)
- [LLVIP](https://bupt-ai-cz.github.io/LLVIP/)
- [SWVID / CFMW](https://github.com/lhy-zju/CFMW). The study used a locally documented v3 archive.

The CSV files contain sample identifiers and condition labels. Redistribution of source and derived imagery is subject to the underlying dataset terms.

## Recorded evaluation results

- `main-results.json`: eight model families on three datasets, with full, original, and synthetic condition groups.
- `swvid-ablation.json`: SWVID module and mechanism comparisons, including the fixed-epoch endpoint.
- `checkpoint-comparisons.json`: evaluation results obtained from existing checkpoints.

Metric proportions retain their source precision. Multiply proportions by 100 to compare them with percentages in the manuscript. The main comparison evaluates existing systems on common test lists with shared scoring rules. TICRE-Net uses the stagewise adaptation described in the manuscript.

## Generation components

`initial-generation.json` and `revision-generation.json` record generation settings. `appearance_transforms.py` contains the initial tone mapping and rain overlay for uint8 RGB arrays and uses NumPy and OpenCV. Consult the manuscript for the generator, screening, and training protocol. Full image collections, per-image predictions, model checkpoints, and an end-to-end training pipeline are outside this release.

Run `python verify_release.py` to check the published index and result counts using the Python standard library.
