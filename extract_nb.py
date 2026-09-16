import json

with open('training.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

for i, cell in enumerate(nb['cells']):
    if cell['cell_type'] == 'code' and i < 37:
        source = ''.join(cell['source'])
        print(f"=== Cell {i} (code) ===")
        print(source)
        print("---")
    elif cell['cell_type'] == 'markdown' and i < 37:
        source = ''.join(cell['source'])
        print(f"=== Cell {i} (markdown) ===")
        print(source)
        print("---")
