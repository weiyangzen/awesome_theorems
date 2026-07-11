#!/usr/bin/env bash
set -euo pipefail

here="$(cd "$(dirname "$0")" && pwd)"
lean_root="$here/../../Formalizations/Lean"
statement_olean=../../Stage1_Instances/THM-M-0414/Statement.olean
trap 'rm -f "$statement_olean"' EXIT

cd "$lean_root"
lake env lean -R ../.. -o "$statement_olean" \
  ../../Stage1_Instances/THM-M-0414/Statement.lean
LEAN_PATH="../../Stage1_Instances/THM-M-0414:$(lake env printenv LEAN_PATH)" \
  lake env lean -R ../.. ../../Stage1_Instances/THM-M-0414/Proof.lean

python3 - "$here/Proof.lean" <<'PY'
from pathlib import Path
import re
import sys

source = Path(sys.argv[1]).read_text()
for pattern in (r"\bsorry\b", r"\badmit\b", r"\baxiom\b", r"\bunsafe\b", r"sorryAx"):
    if re.search(pattern, source):
        raise SystemExit(f"forbidden proof-source token matched: {pattern}")
print("PASS: exact root and both frozen components are present without forbidden proof tokens")
PY
