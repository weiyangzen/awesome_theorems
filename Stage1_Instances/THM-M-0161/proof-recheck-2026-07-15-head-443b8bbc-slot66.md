# THM-M-0161 current-base proof recheck

Item: `S56-M-0161-PROOF`

Intent: `prove`

Base revision: `443b8bbc23bf35a1e7a4bb7b3183073f76bbee2b`

Base tree: `c5771c47c12b80aba613e6d844570f83b39ded6d`

Rechecked: `2026-07-15T11:44:32+08:00`

## Verdict

`blocked`. The exact frozen positive target is false, so this proof item cannot truthfully be
completed. `Counterexample.lean`, which is already tracked in the worker base, kernel-checks

```text
Stage1Instances.THM_M_0161.frozen_target_false :
  Not FundamentalTheoremOfSpaceCurvesTarget
```

The item remains `[ ]`. No positive proof body, proof receipt, provisional completion, audit
completion, validation, release, theorem completion, or master acceptance is claimed.

The frozen target assumes only `DifferentiableOn Real kappa (Ioo a b)` but requires a `C^3`
realizing curve. For every such curve with positive realized curvature,
`curvature_is_contDiffOn_one` proves that its curvature is `C^1` on the interval. The checked
counterexample takes

```text
kappa161(x) = 2 + x^2 * sin(1/x),    tau(x) = 0,    interval = (-1, 1).
```

This curvature is differentiable everywhere and positive on `(-1,1)`, but its derivative is zero
at zero and `-1` along `1 / ((n + 1) * 2*pi)`, a sequence tending to zero. It is therefore not
`C^1`, contradicting the regularity forced by the target's existence conclusion. Uniqueness is
irrelevant: refuting the existence conjunct refutes the exact target.

The negative theorem is an `M0-L` body for `Not FundamentalTheoremOfSpaceCurvesTarget`; it supplies
no positive-root proof credit. Under rev-5.6 section 3, this proposes `H5/M5` for the frozen
under-regularized proposition and requires redirection to statement repair, a barrier theorem, or a
counterexample target. It does not refute the classical theorem with source-faithful coefficient
regularity.

The authoritative instance and typed graph still record historical `H1/M4/R4` and `H3/M3/R4`
vectors respectively. This proof worker does not rewrite predecessor statement, registry, graph,
or state authority. The current recheck supersedes only the proof diagnosis in `proof-blocker.json`
and `proof-validation.md`, and the stale-base/transient-copy details in the earlier slot72 reports.

## Validation

The successful kernel check used Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, mathlib commit
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, `--trust=0`, one thread, and temporary copies and
oleans removed on exit. It printed the exact negation, and `#print axioms` reported exactly
`propext`, `Classical.choice`, and `Quot.sound` for both key declarations. A source and output scan
found no `sorry`, `admit`, bodyless declaration, unsafe/oracle construct, or related prohibited
device. The only Lean diagnostic was a non-failing `unnecessarySeqFocus` linter warning at line 70.

The automation-provided `.lake` path is an untracked symlink to the shared canonical cache. An
initial required `lake env lean` invocation triggered or participated in Lake's attempt to clone the
unrelated manifest dependency `flt-regular`; the clone failed and left an incomplete checkout with
no resolvable `HEAD`. This crossed the intended read-only dependency boundary, so the failed Lake
attempt is recorded as an environment/policy incident and not as evidence. No repair, explicit
fetch, update, build, or removal was attempted. The successful replay invoked the pinned Lean
binary directly and used only the eight already-built package library directories needed by
Mathlib. This remains nonrelease blocker evidence.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check && python3 scripts/stage1_target.py show THM-M-0161` | 0 | 1546 unique targets; rank 660; planned; theorem incomplete |
| assigned-item `jq` query | 0 | proof item `[ ]`, obligation-tree prerequisite `[_]`, attempts `0` |
| `python3 Stage1_Instances/THM-M-0161/check_obligation_tree.py` | 0 | 21 obligations, 44 edges, denominator `48173f90...dadbe`; predecessor positive root open |
| `python3 Stage1_Instances/THM-M-0161/check_statement.py` | 1 | Lake could not resolve the incomplete unrelated `flt-regular`; no target artifact remained |
| initial `lake env lean .../Statement.lean` | not captured | automatic `flt-regular` clone attempt failed with Git exit 128; not accepted as evidence |
| `lake env lean --version` and independent `timeout 30 lake env which lean` | 1 each | `flt-regular` could not resolve `HEAD`; no repair attempted |
| direct pinned trust-zero recipe below | 0 | statement and counterexample elaborated; exact type, axiom, and prohibited-device checks passed |
| mathlib revision and status checks | 0 | pinned revision matched; tracked dependency worktree was clean |
| JSON and scoped whitespace checks | 0 | new blocker reports valid and free of whitespace errors |
| `test ! -e .stage1-worker-selftest.json` | 0 | completion manifest deliberately absent |

Exact successful replay, run from the repository root:

```bash
set -euo pipefail
ROOT=$PWD
TARGET=$ROOT/Stage1_Instances/THM-M-0161
LEAN_ROOT=$ROOT/Formalizations/Lean
LEAN=$HOME/.elan/toolchains/leanprover--lean4---v4.29.0/bin/lean
TMP=$(mktemp -d /tmp/thm-m-0161-recheck-443b8bbc.XXXXXX)
trap 'rm -rf "$TMP"' EXIT
cp "$TARGET/Statement.lean" "$TARGET/Counterexample.lean" "$TMP"/
LIBS=$(find -L "$LEAN_ROOT/.lake/packages" \
  -path '*/.lake/build/lib/lean' -type d ! -path '*/flt-regular/*' \
  -print | sort | paste -sd: -)
TOOLCHAIN=$HOME/.elan/toolchains/leanprover--lean4---v4.29.0/lib/lean

LEAN_NUM_THREADS=1 LEAN_PATH="$LIBS:$TOOLCHAIN" timeout 300 \
  "$LEAN" --trust=0 -t0 --root="$TMP" -o "$TMP/Statement.olean" \
  "$TMP/Statement.lean" >"$TMP/statement.out" 2>&1
LEAN_NUM_THREADS=1 LEAN_PATH="$TMP:$LIBS:$TOOLCHAIN" timeout 300 \
  "$LEAN" --trust=0 -t0 --root="$TMP" -o "$TMP/Counterexample.olean" \
  "$TMP/Counterexample.lean" >"$TMP/counterexample.out" 2>&1

python3 - "$TARGET/Counterexample.lean" "$TMP/counterexample.out" <<'PY'
import re
import sys
from pathlib import Path

source = Path(sys.argv[1]).read_text(encoding="utf-8")
output = Path(sys.argv[2]).read_text(encoding="utf-8")
source = re.sub(r"/-.*?-/", "", source, flags=re.DOTALL)
source = re.sub(r"--.*", "", source)
prohibited = re.compile(
    r"\b(?:sorry|admit|sorryAx|implemented_by|native_decide)\b|"
    r"^[ \t]*(?:axiom|constant|opaque|unsafe|extern)\b",
    re.MULTILINE,
)
matches = prohibited.findall(source)
if matches:
    raise SystemExit(f"prohibited constructs: {matches}")
allowed = {"propext", "Classical.choice", "Quot.sound"}
for name in ("curvature_is_contDiffOn_one", "frozen_target_false"):
    declaration = f"Stage1Instances.THM_M_0161.{name}"
    pattern = re.escape(f"'{declaration}' depends on axioms: [") + r"(.*?)]"
    found = re.findall(pattern, output, re.DOTALL)
    if len(found) != 1:
        raise SystemExit(f"missing or duplicate axiom report: {declaration}")
    actual = {x.strip() for x in found[0].split(",") if x.strip()}
    if actual != allowed:
        raise SystemExit(f"unexpected axiom closure for {declaration}: {actual}")
if not re.search(
    r"frozen_target_false : (?:Not |¬\s*)FundamentalTheoremOfSpaceCurvesTarget",
    output,
):
    raise SystemExit("exact negation type was not printed")
for bad in ("sorryAx", "declaration uses 'sorry'", "error:"):
    if bad in output:
        raise SystemExit(f"prohibited Lean output: {bad}")
print("PROHIBITED_MATCH_COUNT=0")
print("AXIOM_AND_EXACT_TYPE_CHECK=PASS")
PY

cat "$TMP/counterexample.out"
printf 'LEAN_PATH_COMPONENTS=%s\n' "$(printf '%s' "$LIBS" | awk -F: '{print NF}')"
"$LEAN" --version
git -C "$LEAN_ROOT/.lake/packages/mathlib" rev-parse HEAD
printf '%s\n' 'DIRECT_PINNED_TRUST_ZERO_REPLAY=PASS'
```

The eight `LIBS` entries were the existing build-library directories for `LeanSearchClient`, `Qq`,
`aesop`, `batteries`, `importGraph`, `mathlib`, `plausible`, and `proofwidgets`. The actual replay
also ran a Python check over the counterexample source and Lean output. After stripping comments,
it rejected

```text
\b(sorry|admit|sorryAx|implemented_by|native_decide)\b
^[ \t]*(axiom|constant|opaque|unsafe|extern)\b
```

and required the exact negation plus the exact allowed axiom set. It printed
`PROHIBITED_MATCH_COUNT=0`, `AXIOM_AND_EXACT_TYPE_CHECK=PASS`, and
`DIRECT_PINNED_TRUST_ZERO_REPLAY=PASS`.

## Retry condition

Do not retry the unchanged positive root. Authorized source and statement review must first repair
the coefficient regularity to `C^1` or stronger, or replace the task with an accepted
counterexample/barrier target. A corrected target then needs a new canonical fingerprint, an
append-only obligation-registry and typed-graph version delta, and fresh statement mutation, source,
anchor, obligation-tree, and proof execution in dependency order.

Because the positive proof phase is blocked rather than genuinely complete,
`.stage1-worker-selftest.json` is deliberately absent.
