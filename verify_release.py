import csv
import gzip
import json
from collections import Counter
from pathlib import Path


root = Path(__file__).resolve().parent
expected = json.loads((root / 'split-counts.json').read_text(encoding='utf-8'))
observed = Counter()
source_splits = {}
for path in sorted(root.glob('*.csv.gz')):
    with gzip.open(path, 'rt', encoding='utf-8', newline='') as stream:
        ids = set()
        for row in csv.DictReader(stream):
            dataset, split = row['dataset'], row['split']
            assert path.name == f'{dataset.lower()}-{split}.csv.gz'
            assert row['image_id'] not in ids
            ids.add(row['image_id'])
            key = (dataset, row['source_id'])
            assert source_splits.setdefault(key, split) == split
            observed[f'{dataset}/{split}'] += 1
assert observed == expected and sum(observed.values()) == 115398
for name, expected_count in [('main-results', 96), ('swvid-ablation', 40), ('checkpoint-comparisons', 48)]:
    rows = json.loads((root / f'{name}.json').read_text(encoding='utf-8'))
    assert len(rows) == expected_count
    assert all(0 <= row['metrics']['map50'] <= 1 for row in rows)
print('Verified 115,398 released sample pairs and all three recorded result sets.')
