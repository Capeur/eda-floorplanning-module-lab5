#!/usr/bin/env bash
# Redraw every Stage 3 picture of floorplanning Lab 05 (B*-tree), exactly as it was made.
#   bash run_all.sh [teacher clone]        (default: ../../eda-learning-lab5-fp)
# Writes into <clone>/courses/learn_floorplanning/module02-03-bstar-tree/assets/ only.
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO="$(cd "${1:-$HERE/../../eda-learning-lab5-fp}" && pwd)"
M=courses/learn_floorplanning/module02-03-bstar-tree
S=.cursor/skills/module-slides/scripts
export PYTHONDONTWRITEBYTECODE=1

# 1. numbers from the checker, then the scratch walkthrough viewer (a copy of the clone's platform)
python3 "$HERE/facts.py" "$REPO/$M"
python3 "$HERE/patch_walkthrough.py" --source "$REPO/platform"

# 2. serve the scratch viewer on 8081
python3 -m http.server 8081 --bind 127.0.0.1 --directory "$HERE/wt-platform" >/dev/null 2>&1 &
P1=$!
trap 'kill $P1 2>/dev/null' EXIT
for _ in $(seq 20); do
  curl -sf -o /dev/null http://127.0.0.1:8081/ && break
  python3 -c "import time; time.sleep(0.5)"
done

cd "$REPO"
# 3. walkthrough frames + STEPS.md (teacher's script), then put STEPS.md back to CRLF
python3 $S/capture_algorithm_walkthrough.py $M --algo bstar-tree \
  --base http://127.0.0.1:8081/tools/algorithm-walkthrough
python3 - "$M/assets/STEPS.md" <<'EOF'
import sys
from pathlib import Path
p = Path(sys.argv[1])
t = p.read_text(encoding="utf-8").replace("\r\n", "\n")
p.write_bytes(t.replace("\n", "\r\n").encode("utf-8"))
EOF

# 4. the explanation figures and their step figures (tree on top, outline below)
python3 "$HERE/make_figures.py" --module "$M"

# 5. a shell running the checker: the reference, then a wrong packer caught (teacher's script)
python3 $S/capture_real_shell.py $M --example-subdir . \
  --commands "python3 bstar_check.py --show | grep PASS | head -6,python3 bstar_check.py --impl wrong/right_first.py | grep FAIL"
