#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "$0")/../.." && pwd)"
target="$repo_root/Stage1_Instances/THM-M-1237"
lean_root="$repo_root/Formalizations/Lean"
tmp="$(mktemp -d /tmp/stage1-m1237-validation.XXXXXX)"
trap 'rm -rf "$tmp"' EXIT

cp "$target"/{Statement,ObligationTree,Proof,ProofAudit,Validation}.lean "$tmp/"

cd "$lean_root"
lean_bin="$(lake env which lean)"
lean_path="$(lake env printenv LEAN_PATH)"
tmp="$(realpath "$tmp")"

base=(
  bwrap --ro-bind / / --bind "$tmp" "$tmp" --dev /dev --proc /proc
  --unshare-net --die-with-parent
  --setenv LANG C.UTF-8 --setenv LC_ALL C.UTF-8 --setenv TZ UTC
  --chdir "$tmp"
)
"${base[@]}" --setenv LEAN_PATH "$lean_path" \
  "$lean_bin" --trust=0 -o Statement.olean Statement.lean > "$tmp/statement.out"
"${base[@]}" --setenv LEAN_PATH "$tmp:$lean_path" \
  "$lean_bin" --trust=0 -o ObligationTree.olean ObligationTree.lean > "$tmp/obligation.out"
"${base[@]}" --setenv LEAN_PATH "$tmp:$lean_path" \
  "$lean_bin" --trust=0 -o Proof.olean Proof.lean > "$tmp/proof.out"
"${base[@]}" --setenv LEAN_PATH "$tmp:$lean_path" \
  "$lean_bin" --trust=0 ProofAudit.lean > "$tmp/audit.out"
"${base[@]}" --setenv LEAN_PATH "$tmp:$lean_path" \
  "$lean_bin" --trust=0 Validation.lean > "$tmp/validation.out"
cat "$tmp/statement.out" "$tmp/obligation.out" "$tmp/proof.out" \
  "$tmp/audit.out" "$tmp/validation.out"

python3 - "$tmp/audit.out" "$tmp/validation.out" <<'PY'
import re
import sys
from pathlib import Path

audit = Path(sys.argv[1]).read_text(encoding="utf-8")
validation = Path(sys.argv[2]).read_text(encoding="utf-8")
allowed = {"propext", "Classical.choice", "Quot.sound"}
audit_declarations = (
    "Stage1Rev56.THMM1237.statement_iff_expanded",
    "Stage1Rev56.THMM1237.ObligationTree.root_compose",
    "Stage1Rev56.THMM1237.Proof.representativeFamily",
    "Stage1Rev56.THMM1237.Proof.not_valueEstimateFamily",
)
differential = (
    "Stage1Rev56.THMM1237.Validation.independentlyRefutedValueEstimateFamily"
)


def observed_axioms(output: str, declaration: str) -> set[str]:
    match = re.search(
        re.escape(f"'{declaration}' depends on axioms: [") + r"(.*?)]",
        output,
        re.DOTALL,
    )
    assert match, f"missing axiom report for {declaration}"
    return {name.strip() for name in match.group(1).split(",") if name.strip()}


expected_audit = {
    audit_declarations[0]: allowed,
    audit_declarations[1]: allowed,
    audit_declarations[2]: allowed,
    audit_declarations[3]: allowed,
}
for declaration, expected in expected_audit.items():
    assert observed_axioms(audit, declaration) == expected, declaration
assert observed_axioms(validation, differential) == allowed
assert audit.count("Declarations are sorry-free!") == len(audit_declarations)
assert validation.count("Declarations are sorry-free!") == 1
combined = audit + validation
assert "sorryAx" not in combined
assert "declaration uses 'sorry'" not in combined
assert "error:" not in combined
PY
