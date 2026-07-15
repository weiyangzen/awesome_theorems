# THM-M-1247 proof recheck at `475865d2` (slot30)

Item: `S56-M-1247-PROOF`

Base revision: `475865d2b8e950de525943da03cfc25ae9b14214`

Base tree: `e57db7a6052a6a249d701144f0ca4a21bec5c613`

Run date: `2026-07-15T23:13:46+08:00`

## Verdict

`blocked`. The proof phase is not complete, so no
`.stage1-worker-selftest.json` was emitted.

The tracked `Proof.lean` is placeholder-free and kernel-checks an inhabitant of
the frozen Lean proposition. It cannot receive proof credit for the canonical
human Rellich inequality because the frozen proposition has two exact-statement
mapping defects:

1. `ContDiff Real top` infers `top : WithTop ENat`, mathlib's analytic order
   `omega`; smooth infinity is `((top : ENat) : WithTop ENat)`.
2. `Euclidean n := Fin n -> Real` carries the finite Pi supremum norm;
   `EuclideanSpace Real (Fin n)` is `PiLp 2` with the Euclidean `L2` norm.

Support avoidance makes every admitted analytic function vanish near the
origin. Analytic uniqueness then makes it identically zero, and simplification
closes only this malformed backend encoding. The first failed gate remains the
rev-5.6 section 5 exact backend-to-canonical statement-mapping gate, proposed
at `M1247-S-DOMAIN`.

The predecessor `S56-M-1247-OBLIGATION_TREE` is provisional `[_]`, not
master-accepted. Its 13-obligation registry remains structurally valid but is
semantically stale after the mismatch diagnosis. The conditional declaration
`root_of_coreRellichEstimate` still consumes an open `CoreRellichEstimate`
premise and supplies no missing analytic proof.

## Current-Base Delta

The preceding target recheck was based at
`cf0d919f2dfc00f3f777e9319188dec0f644d159`. Between that base and the current
base, the only target-owned additions are that prior recheck's JSON and
Markdown companions. The statement, proof body, obligation tree, registry,
graphs, validation specifications, anchor audit, target manifest entry,
proof-item state, and execution skill did not change. The only authority change
is an unrelated provisional promotion for `S56-M-0594-RELEASE`.

There were 42 integrated `proof-recheck-*.json` files before this packet, while
the authoritative proof item still records zero attempts and no children. The
master must reconcile these reports with execution ticks and apply the section
10.2 five-tick split rule if at least five qualify. This worker may not edit the
master DAG and cannot repair the statement under a proof-only assignment.

## Validation

All Lean checks read the automation-provided canonical pinned artifacts. No
update, build, clone, fetch, network request, or `.lake` mutation was performed.
Fresh outputs lived only in a temporary directory under `/tmp` and were
removed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups; 1546 uniform-L0 targets; execution skill present. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required`. |
| `python3 scripts/stage1_target.py show THM-M-1247` | 0 | Rank 427; lifecycle `planned`; legacy artifacts unaccepted; theorem incomplete. |
| `timeout --foreground --kill-after=5s 300s python3 Stage1_Instances/THM-M-1247/check_statement.py` | 0 | Expression SHA-256 `4697dbba...5c90e`; all four recorded structural mutations killed. This validates only the frozen encoding. |
| `timeout --foreground --kill-after=5s 300s python3 Stage1_Instances/THM-M-1247/check_anchor_audit.py` | 0 | Three pinned mathlib candidate families checked; exact external candidates `0`; terminal result open. |
| `timeout --foreground --kill-after=5s 300s python3 Stage1_Instances/THM-M-1247/check_obligation_tree.py` | 0 | 13 obligations, 34 typed edges, denominator `9df3b5e9...79a590`; root open at `M3`, with six analytic obligations at `M4`. |
| Isolated pinned `lake env lean --trust=0` recipe below | 0 | Fresh `Statement.olean`, `Proof.lean`, and `ObligationTree.lean` elaborated; exact frozen type checked; axioms exactly `propext`, `Classical.choice`, `Quot.sound`. |
| Independent read-only agent replay | 0 | Independently checked the same proof route and axiom output; corroboration only, not release-independence credit. |
| `rg -n -i 'Rellich|Hardy[-_ ]?Rellich|HardyRellich' Formalizations/Lean/.lake/packages --glob '*.lean'` | 1, expected | No exact theorem candidate in readable pinned package Lean sources. |
| Prohibited proof-token scan over `Statement.lean`, `Proof.lean`, and `ObligationTree.lean` | 1, expected | No `sorry`, `admit`, `sorryAx`, declared `axiom`, `unsafe`, or `opaque`; this is not a transitive provenance audit. |
| `git diff --name-status cf0d919f2dfc00f3f777e9319188dec0f644d159..HEAD -- Stage1_Instances/THM-M-1247 Docs/Stage1_Blueprint_rev-5.6.md Docs/Stage1_Execution_DAG_rev-5.6.json Docs/Stage1_Targets_rev-5.6.json skills/execute-stage1-rev56/SKILL.md` | 0 | Only the prior target blocker pair and one unrelated authority promotion; no target semantic input, target task state, manifest entry, or governing-skill change. |
| Packet JSON parse and assertion recipe below | 0 | Current base, hashes, open-state boundary, and deliberate self-test absence agree. |
| `git diff --check -- Stage1_Instances/THM-M-1247 .stage1-worker-selftest.json` | 0 | No whitespace diagnostics. |
| `test ! -e .stage1-worker-selftest.json` | 0 | No false worker-completion packet exists. |

The successful narrow Lean replay was:

```bash
set -euo pipefail
ROOT="$PWD"
TARGET="$ROOT/Stage1_Instances/THM-M-1247"
LEAN_ROOT="$ROOT/Formalizations/Lean"
TMP=$(mktemp -d /tmp/thm-m-1247-proof-head-475865d2-slot30.XXXXXX)
trap 'rm -rf "$TMP"' EXIT
cp "$TARGET"/{Statement,Proof,ObligationTree}.lean "$TMP/"
cd "$LEAN_ROOT"
BASE_LEAN_PATH=$(timeout --foreground --kill-after=5s 300s lake env printenv LEAN_PATH)
LEAN_NUM_THREADS=1 LEAN_PATH="$BASE_LEAN_PATH" \
  timeout --foreground --kill-after=5s 300s \
  lake env lean --trust=0 -t0 --root="$TMP" \
  -o "$TMP/Statement.olean" "$TMP/Statement.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$TMP:$BASE_LEAN_PATH" \
  timeout --foreground --kill-after=5s 300s \
  lake env lean --trust=0 -t0 --root="$TMP" "$TMP/Proof.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$TMP:$BASE_LEAN_PATH" \
  timeout --foreground --kill-after=5s 300s \
  lake env lean --trust=0 -t0 --root="$TMP" "$TMP/ObligationTree.lean"
```

The proof-specific output was:

```text
Stage1Instances.THM_M_1247.rellichInequalityTarget : RellichInequalityTarget
'Stage1Instances.THM_M_1247.frozen_top_is_analytic_order' depends on axioms: [propext, Classical.choice, Quot.sound]
'Stage1Instances.THM_M_1247.analytic_avoidance_eq_zero' depends on axioms: [propext, Classical.choice, Quot.sound]
'Stage1Instances.THM_M_1247.rellichInequalityTarget' depends on axioms: [propext, Classical.choice, Quot.sound]
'Stage1Instances.THM_M_1247.root_of_coreRellichEstimate' depends on axioms: [propext, Classical.choice, Quot.sound]
```

The expanded root output contains `@Top.top (WithTop ENat)` together with
finite-Pi `@Pi.normedAddCommGroup` and `@Pi.normedSpace` instances, confirming
both mapping defects.

The packet check was:

```bash
python3 -m json.tool \
  Stage1_Instances/THM-M-1247/proof-recheck-2026-07-15-head-475865d2-slot30.json \
  >/dev/null
python3 - <<'PY'
import hashlib
import json
import pathlib
import subprocess

p = pathlib.Path(
    "Stage1_Instances/THM-M-1247/"
    "proof-recheck-2026-07-15-head-475865d2-slot30.json"
)
d = json.loads(p.read_text())
assert d["item_id"] == "S56-M-1247-PROOF"
assert d["theorem_id"] == "THM-M-1247"
assert d["base_revision"] == subprocess.check_output(
    ["git", "rev-parse", "HEAD"], text=True
).strip()
assert d["base_tree"] == subprocess.check_output(
    ["git", "rev-parse", "HEAD^{tree}"], text=True
).strip()
assert d["state"] == "[ ]" and d["verdict"] == "blocked"
assert not d["proof_phase_complete"] and not d["theorem_complete"]
assert not d["selftest_manifest_written"]
for changed in d["changed_paths"]:
    assert pathlib.Path(changed).is_file()
for name, expected in d["source_hashes"].items():
    path = {
        "lake-manifest.json": pathlib.Path("Formalizations/Lean/lake-manifest.json"),
        "lean-toolchain": pathlib.Path("Formalizations/Lean/lean-toolchain"),
    }.get(name, pathlib.Path("Stage1_Instances/THM-M-1247") / name)
    assert hashlib.sha256(path.read_bytes()).hexdigest() == expected
assert not pathlib.Path(".stage1-worker-selftest.json").exists()
print("PASS current-base blocker packet assertions")
PY
```

## Retry Condition

Do not dispatch `S56-M-1247-PROOF` unchanged again. Reopen
`S56-M-1247-STATEMENT` under an authorized assignment. Import
`Mathlib.MeasureTheory.Measure.Haar.InnerProductSpace` for the Euclidean-space
canonical-volume instance, use `EuclideanSpace Real (Fin n)` with
`EuclideanSpace.single` coordinate directions, and spell smooth infinity with
`open scoped ContDiff` and an explicitly typed order. Then rerun
exact-expression and mutation gates, publish a versioned
obligation-registry/typed-graph delta with downstream invalidations, and, if
the master confirms at least five unresolved execution ticks, split weighted
integration by parts, derivative Hardy, normalization, core estimate, and
transport into dependency-legal child tasks before resuming proof execution.
The source-audit repair should also
correct the Davies-Hinz article DOI from `10.1007/PL00004387` to
`10.1007/PL00004389`.

## Status Boundary

This is current-base blocker and scheduler-escalation evidence under the owned
target path. It does not satisfy `S56-M-1247-PROOF`. The item remains `[ ]`;
there is no worker self-test, accepted receipt, audit completion, validation,
release, or theorem-completion claim.
