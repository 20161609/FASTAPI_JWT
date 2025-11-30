import os

TARGET_EXT = {'.py'}        # allowed extensions
SKIP_DIRS = {'venv', '.venv', '__pycache__'}  # skip these dirs

def collecter(root=".", output_name="output.txt"):
    collected = []

    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]  # block descent

        for f in filenames:
            _, ext = os.path.splitext(f)
            if ext in TARGET_EXT and f != 'collecter.py':
                full_path = os.path.join(dirpath, f)
                rel_path = os.path.relpath(full_path, root)

                with open(full_path, "r", encoding="utf-8", errors="ignore") as fp:
                    content = fp.read()

                collected.append(f'"""\n{content}\n""" {rel_path}')

    with open(output_name, "w", encoding="utf-8") as out:
        out.write("\n\n".join(collected))

collecter(".")
