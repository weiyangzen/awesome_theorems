#!/usr/bin/env bash
set -euo pipefail

script_path="$(cd "$(dirname "$0")" && pwd)/$(basename "$0")"
if [[ "${1:-}" != "--bounded-inner" ]]; then
  if (( $# != 0 )); then
    printf 'usage: %s\n' "$0" >&2
    exit 2
  fi
  exec timeout --foreground --kill-after=10s 600s bash "$script_path" --bounded-inner
fi
if (( $# != 1 )); then
  printf 'invalid internal invocation\n' >&2
  exit 2
fi
if [[ -n "${http_proxy:-}${https_proxy:-}${HTTP_PROXY:-}${HTTPS_PROXY:-}${ALL_PROXY:-}" ]]; then
  printf 'network proxy variables must be unset for this replay\n' >&2
  exit 2
fi

repo_root="$(cd "$(dirname "$0")/../.." && pwd)"
target="$repo_root/Stage1_Instances/THM-M-1143"
lean_root="$repo_root/Formalizations/Lean"
tmp="$(mktemp -d /tmp/stage1-m1143-proof.XXXXXX)"
trap 'rm -rf "$tmp"' EXIT

cp "$target"/{Statement,ObligationTree,Proof}.lean "$tmp/"

lean_bin="$(cd "$lean_root" && lake env which lean)"
lean_path="$(cd "$lean_root" && env -u LEAN_PATH lake env printenv LEAN_PATH)"
cd "$tmp"
LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" timeout 180 "$lean_bin" --trust=0 \
  -o Statement.olean Statement.lean >/dev/null
LEAN_NUM_THREADS=1 LEAN_PATH=".:$lean_path" timeout 180 "$lean_bin" --trust=0 \
  -o ObligationTree.olean ObligationTree.lean >/dev/null
LEAN_NUM_THREADS=1 LEAN_PATH=".:$lean_path" timeout 180 "$lean_bin" --trust=0 Proof.lean \
  | tee proof.out

python3 - proof.out <<'PY'
import re
import sys
from pathlib import Path

output = Path(sys.argv[1]).read_text(encoding="utf-8")
declarations = (
    "Stage1Instances.THM_M_1143.exists_uniform_abs_bound",
    "Stage1Instances.THM_M_1143.exists_nonnegative_uniform_abs_bound",
    "Stage1Instances.THM_M_1143.continuousLinearMap_eq_zero_of_norm_le_div",
    "Stage1Instances.THM_M_1143.vanishingDerivativePackage_of_interiorGradientEstimate",
    "Stage1Instances.THM_M_1143.zeroDerivativeConstantPackage",
    "Stage1Instances.THM_M_1143.root_of_vanishingDerivativePackage",
    "Stage1Instances.THM_M_1143.root_of_interiorGradientEstimate",
)
allowed = {"propext", "Classical.choice", "Quot.sound"}
for declaration in declarations:
    match = re.search(
        re.escape(f"'{declaration}' depends on axioms: [") + r"(.*?)]",
        output,
        re.DOTALL,
    )
    assert match, f"missing axiom report for {declaration}"
    actual = {name.strip() for name in match.group(1).split(",") if name.strip()}
    assert actual <= allowed, f"unexpected axiom closure for {declaration}: {actual}"
assert "sorryAx" not in output
assert "declaration uses 'sorry'" not in output
assert "error:" not in output
print("PASS THM-M-1143 isolated Lean replay: seven local proof declarations checked")
PY
