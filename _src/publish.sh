#!/bin/bash
# Rebuild the site from _src and copy the output to the repo root.
# Usage (from the repo root): bash _src/publish.sh
set -e
cd "$(dirname "$0")/.."
python3 _src/gen/build.py
python3 - <<'PY'
import os, shutil
keep = {".git", "CNAME", ".nojekyll", "_src"}
for n in os.listdir("."):
    if n in keep: continue
    p = os.path.join(".", n)
    shutil.rmtree(p) if os.path.isdir(p) and not os.path.islink(p) else os.remove(p)
for n in os.listdir("_src/dist"):
    if n in keep: continue
    s = os.path.join("_src/dist", n)
    shutil.copytree(s, n) if os.path.isdir(s) else shutil.copy2(s, n)
shutil.rmtree("_src/dist")
PY
rm -rf _src/gen/__pycache__
echo "built; now: git add -A && git commit && git push"
