import json

with open('training.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

for i, cell in enumerate(nb['cells']):
    if i >= 37:
        source = ''.join(cell['source'])
        print(f"=== Cell {i} ({cell['cell_type']}) ===")
        print(source)
        print("---")
