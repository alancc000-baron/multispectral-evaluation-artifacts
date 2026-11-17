# TICRE-Net multispectral evaluation artifacts

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

`initial-generation.json` and `revision-generation.json` record generation settings. `appearance_transforms.py` contains the initial tone mapping and rain overlay for uint8 RGB arrays and uses NumPy and OpenCV. Consult the manuscript for the generator, screening, and training protocol. This release provides the recorded results and the prediction sets documented below. Original images and annotations are available through the respective providers. The complete expanded image archive, model checkpoints, and full training code are held separately.

Run `python verify_release.py` to check the published index and result counts using the Python standard library.

## Per-image detections on the expanded test splits

The six files in the predictions directory provide detections for TICRE-Net and the original UMPDP on the same 5,881 KAIST, 8,681 LLVIP, and 9,754 SWVID test samples per model. They correspond to the full expanded test-pool results reported for those two models. The repository also includes the eight-model aggregate comparison and the aggregate SWVID module ablation.

Each gzip-compressed JSON Lines file has one row per test sample. The image_id field joins to the corresponding test index, and width and height give the original image dimensions. The detections array contains [x_min, y_min, x_max, y_max, confidence] in original-image pixel coordinates, with the archived prediction order and numerical values. An empty array means that the archive recorded no post-processing detections for the sample. The detectors are evaluated for a single pedestrian class.

The files contain model predictions and sample identifiers. Evaluation annotations must be obtained under the relevant dataset terms and prepared according to the manuscript's evaluation protocol. The prediction manifest records sample and detection counts, compressed file sizes, and SHA-256 checksums.
