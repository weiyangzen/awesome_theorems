#!/usr/bin/env bash
set -euo pipefail

export LC_ALL=C.UTF-8
export TZ=UTC

root=$(git rev-parse --show-toplevel)
here="$root/Stage1_Instances/THM-M-0034"
lean_dir="$root/Formalizations/Lean"
tmp=$(mktemp -d "/tmp/m0034-proof.XXXXXX")
trap 'rm -rf "$tmp"' EXIT

lean=$(cd "$lean_dir" && lake env which lean)
lean_path=$(cd "$lean_dir" && lake env printenv LEAN_PATH)
options=(
  --trust=0
  -t0
  -DautoImplicit=false
  -DrelaxedAutoImplicit=false
  -Dweak.linter.mathlibStandardSet=false
  -DmaxSynthPendingDepth=3
)

test -x "$lean"
test "$(git -C "$lean_dir/.lake/packages/mathlib" rev-parse HEAD)" = \
  "8a178386ffc0f5fef0b77738bb5449d50efeea95"
test -z "$(git -C "$lean_dir/.lake/packages/mathlib" status --short)"

mkdir -p "$tmp/Stage1_Instances/THM-M-0034"
cp "$here"/{Statement,Proof,ProofAudit}.lean "$tmp/Stage1_Instances/THM-M-0034/"
cp -R "$here/Vendor" "$tmp/Stage1_Instances/THM-M-0034/Vendor"

modules=(
  "Stage1_Instances/THM-M-0034/Statement"
  "Stage1_Instances/THM-M-0034/Vendor/QuillenSuslin/UnimodularVector/BivariatePolynomial"
  "Stage1_Instances/THM-M-0034/Vendor/QuillenSuslin/UnimodularVector/SuslinMonicPolynomialThm"
  "Stage1_Instances/THM-M-0034/Vendor/QuillenSuslin/UnimodularVector/Basic"
  "Stage1_Instances/THM-M-0034/Vendor/QuillenSuslin/UnimodularVector/PID"
  "Stage1_Instances/THM-M-0034/Vendor/QuillenSuslin/FiniteFreeResolution/Basic"
  "Stage1_Instances/THM-M-0034/Vendor/QuillenSuslin/FiniteFreeResolution/Polynomial"
  "Stage1_Instances/THM-M-0034/Vendor/QuillenSuslin/FiniteFreeResolution/StablyFree"
  "Stage1_Instances/THM-M-0034/Vendor/QuillenSuslin/MainTheorem"
  "Stage1_Instances/THM-M-0034/Proof"
  "Stage1_Instances/THM-M-0034/ProofAudit"
)

for module in "${modules[@]}"; do
  source="$tmp/$module.lean"
  target="${source%.lean}.olean"
  log="$tmp/${module//\//-}.out"
  mkdir -p "$(dirname "$target")"
  env LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" \
    "$lean" "${options[@]}" -R "$tmp" -o "$target" "$source" > "$log" 2>&1
done

audit="$tmp/Stage1_Instances-THM-M-0034-ProofAudit.out"
python3 - "$audit" <<'PY'
import re
import sys
from pathlib import Path

output = Path(sys.argv[1]).read_text(encoding="utf-8")
declarations = (
    "quillenSuslin",
    "Stage1Instances.THM_M_0034.quillenSuslinTarget",
)
allowed = {"propext", "Classical.choice", "Quot.sound"}
assert output.count("Declarations are sorry-free!") == len(declarations), output
for declaration in declarations:
    match = re.search(
        re.escape(f"'{declaration}' depends on axioms: [") + r"(.*?)]",
        output,
        re.DOTALL,
    )
    assert match, f"missing axiom report for {declaration}"
    actual = {name.strip() for name in match.group(1).split(",") if name.strip()}
    assert actual == allowed, f"unexpected axiom closure for {declaration}: {actual}"
assert "sorryAx" not in output
assert "declaration uses 'sorry'" not in output
assert "error:" not in output.lower()
PY

test -s "$tmp/Stage1_Instances/THM-M-0034/Proof.olean"
test -s "$tmp/Stage1_Instances/THM-M-0034/ProofAudit.olean"
echo "PASS THM-M-0034 isolated proof elaboration (8 vendored modules, --trust=0 -t0)"
