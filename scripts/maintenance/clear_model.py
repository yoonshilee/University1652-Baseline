from pathlib import Path

root = Path(__file__).resolve().parents[2] / 'model'
for folder in root.iterdir():
    if not folder.is_dir():
        continue
    for checkpoint in folder.iterdir():
        name = checkpoint.name
        if name[0:3] != 'net':
            continue
        if name[5] == 'a':
            continue
        if int(name[4]) < 1:
            print(checkpoint)
            checkpoint.unlink()
