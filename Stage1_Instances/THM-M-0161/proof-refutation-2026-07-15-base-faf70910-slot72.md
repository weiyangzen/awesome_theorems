# THM-M-0161 proof-phase refutation blocker

Item: `S56-M-0161-PROOF`

Intent: `prove`

Base revision: `faf70910840a85c6b24375b5de7ab8ba046bcf67`

Base tree: `bcb52d1788ee99171b510659f66226f7db6b5619`

Validated: `2026-07-15` (`Asia/Shanghai`)

## Verdict

`blocked`. The exact frozen positive target is false, so this proof item cannot truthfully be
completed. `Counterexample.lean` kernel-checks

```text
Stage1Instances.THM_M_0161.frozen_target_false :
  Not FundamentalTheoremOfSpaceCurvesTarget
```

No positive proof body, proof receipt, provisional completion, audit completion, or theorem
completion is claimed. The item remains `[ ]`, with `root_closed=false` and
`theorem_complete=false`.

The checked `Counterexample.lean` body is content-addressed by SHA-256
`2f306383c91022b4767de275a59be8fbb987da4d765f2d72e632a83d34f710f9`. It already exists
byte-for-byte in the scheduler's descendant commit `d01e5d7daab630d25a32f781a754be9af1b82761`, whose
parent is exactly this worker base. The file was materialized from that immutable commit in this
clone for the recorded check, then removed from the Git delta so this blocked handoff does not
resubmit an existing scheduler destination.
The two fresh report files below supersede the older M4-only diagnosis without modifying
predecessor artifacts.

The frozen target assumes only `DifferentiableOn Real kappa (Ioo a b)` but requires a `C^3`
realizing curve. For every such curve with positive prescribed curvature,
`curvature_is_contDiffOn_one` proves that the curvature is `C^1` on the interval. The checked
counterexample uses

```text
kappa161(x) = 2 + x^2 * sin(1/x),    tau(x) = 0,    interval = (-1, 1).
```

Here `kappa161` is differentiable everywhere and strictly positive on `(-1, 1)`, but its derivative
is discontinuous at zero: it is zero at zero and equals `-1` along
`1 / ((n + 1) * 2*pi)`. Thus `kappa161` is not `C^1`, contradicting the regularity forced by the
existence conclusion. This refutes only the frozen Lean encoding, not the correctly regularized
classical theorem of space curves.

The exact-target truth/consistency gate therefore fails. Under rev-5.6 section 3, the new evidence
proposes `H5` (refuted or ill-posed target, pending source and statement review) and `M5` (exact
positive candidate invalid by statement mismatch). The frozen v1 typed graph still records
`[H3, M3, R4]`; this proof worker did not rewrite predecessor authority. Reconciliation of the
proposed `[H5, M5, R4]` vector belongs to authorized statement/source review and a versioned graph
update.

## Validation

All commands ran in this worker clone. The Lean recipe below reused the existing pinned Lake
closure, created oleans only in a disposable `/tmp` directory, used `--trust=0`, and removed the
directory on exit. No `lake update`, `lake build`, dependency clone/fetch, network access, or
`.lake` mutation was performed.

| Command | Exit | Exact result |
|---|---:|---|
| isolated pinned Lean recipe below | 0 | statement and counterexample elaborated under `--trust=0`; exact negation printed; both key declarations depend only on `propext`, `Classical.choice`, and `Quot.sound` |
| prohibited-construct/output scan in the recipe | 0 | no prohibited declaration or proof device, `sorryAx`, `sorry` warning, or Lean error found |
| `python3 Stage1_Instances/THM-M-0161/check_obligation_tree.py` | 0 | 21 obligations and 44 typed edges passed; denominator `48173f90...dadbe`; predecessor positive root remains open |
| `python3 Stage1_Instances/THM-M-0161/check_statement.py` | 0 | exact target expression `c140d1d1...f82` and all four structural mutation tests passed; this confirms statement identity, not truth |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0161` | 0 | rank 660; planned; L0/rework-required; theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-0161/proof-refutation-2026-07-15-base-faf70910-slot72.json >/dev/null` | 0 | fresh structured blocker is valid JSON |
| wrapped new-file `git diff --no-index --check` commands below plus scoped `git diff --check` | 0 | both fresh report artifacts and the complete scoped worker delta have no whitespace errors |
| `test ! -e .stage1-worker-selftest.json` | 0 | completion self-test deliberately absent |

Exact isolated Lean recipe, run from the repository root:

```bash
set -euo pipefail
root=$PWD
target=$root/Stage1_Instances/THM-M-0161
lean_root=$root/Formalizations/Lean
tmp=$(mktemp -d /tmp/thm-m-0161-refutation.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
lean_bin=$(cd "$lean_root" && env -u LEAN_PATH timeout 300 lake env which lean)
lean_path=$(cd "$lean_root" && env -u LEAN_PATH timeout 300 lake env printenv LEAN_PATH)
test "$(sha256sum "$target/Statement.lean" | cut -d' ' -f1)" = \
  82f74a6f99d1b81fe3dac43628a6d5d7dd0f88a323d42b0d21c300bb92a43060
test "$(sha256sum "$target/Counterexample.lean" | cut -d' ' -f1)" = \
  2f306383c91022b4767de275a59be8fbb987da4d765f2d72e632a83d34f710f9
LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" timeout 300 \
  "$lean_bin" --trust=0 -R "$target" -o "$tmp/Statement.olean" \
  "$target/Statement.lean" >"$tmp/statement.out" 2>&1
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" timeout 300 \
  "$lean_bin" --trust=0 -R "$target" -o "$tmp/Counterexample.olean" \
  "$target/Counterexample.lean" >"$tmp/counterexample.out" 2>&1
python3 - "$target/Counterexample.lean" "$tmp/counterexample.out" <<'PY'
import re
import sys
from pathlib import Path
source = Path(sys.argv[1]).read_text(encoding="utf-8")
output = Path(sys.argv[2]).read_text(encoding="utf-8")
source = re.sub(r"/-.*?-/", "", source, flags=re.DOTALL)
source = re.sub(r"--.*", "", source)
prohibited = re.compile(
    r"\b(?:sorry|admit|sorryAx|implemented_by|native_decide)\b|"
    r"^[ \t]*(?:axiom|constant|opaque|unsafe|extern)\b", re.MULTILINE)
if prohibited.search(source):
    raise SystemExit("prohibited construct in Counterexample.lean")
allowed = {"propext", "Classical.choice", "Quot.sound"}
for name in ("curvature_is_contDiffOn_one", "frozen_target_false"):
    declaration = f"Stage1Instances.THM_M_0161.{name}"
    pattern = re.escape(f"'{declaration}' depends on axioms: [") + r"(.*?)]"
    matches = re.findall(pattern, output, re.DOTALL)
    if len(matches) != 1:
        raise SystemExit(f"missing or duplicate axiom report: {declaration}")
    actual = {x.strip() for x in matches[0].split(",") if x.strip()}
    if actual != allowed:
        raise SystemExit(f"unexpected axiom closure for {declaration}: {actual}")
if not re.search(r"frozen_target_false : (?:Not |¬\s*)FundamentalTheoremOfSpaceCurvesTarget", output):
    raise SystemExit("exact negation type was not printed")
for bad in ("sorryAx", "declaration uses 'sorry'", "error:"):
    if bad in output:
        raise SystemExit(f"prohibited Lean output: {bad}")
PY
cat "$tmp/counterexample.out"
"$lean_bin" --version
git -C "$lean_root/.lake/packages/mathlib" rev-parse HEAD
printf '%s\n' 'ISOLATED_TRUST_ZERO_REPLAY=PASS'
```

The recipe exited zero. It printed Lean `4.29.0` commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, and mathlib was pinned at
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. `#print axioms` reported exactly
`[propext, Classical.choice, Quot.sound]` for both key declarations.

Exact whitespace-check wrapper (Git's expected new-file status is `1`; empty diagnostics are the
success condition):

```bash
set -euo pipefail
for file in \
  Stage1_Instances/THM-M-0161/proof-refutation-2026-07-15-base-faf70910-slot72.json \
  Stage1_Instances/THM-M-0161/proof-refutation-2026-07-15-base-faf70910-slot72.md
do
  log=$(mktemp)
  rc=0
  git diff --no-index --check /dev/null "$file" >"$log" 2>&1 || rc=$?
  test "$rc" -eq 1
  test ! -s "$log"
  rm -f "$log"
done
git diff --check -- Stage1_Instances/THM-M-0161 .stage1-worker-selftest.json
```

## Retry condition

Ordinary positive proof work may resume only after authorized statement repair supplies
source-faithful `C^1` or stronger coefficient regularity, or otherwise excludes this counterexample
without assuming the conclusion. The integration lane must then accept a new statement fingerprint,
publish an append-only obligation-registry version delta, and rerun mutation testing, source review,
anchor audit, typed-graph construction, and proof execution in dependency order.

Because the assigned positive proof phase is not genuinely complete, `.stage1-worker-selftest.json`
is deliberately absent. This is actionable blocker evidence, not proof completion.
