# THM-M-1247 proof recheck at `b366bdd9` (slot42)

Item: `S56-M-1247-PROOF`

Base revision: `b366bdd9f72217b5465ccd19133760b911ed0b58`

Base tree: `987b635fe76400c0818b485a6e5fc7a7067311e4`

Run date: `2026-07-15T20:03:07+08:00`

## Verdict

`blocked`. The assigned proof phase is not complete, so no
`.stage1-worker-selftest.json` was emitted.

The existing placeholder-free `Proof.lean` re-elaborates at trust level zero
and proves the exact frozen Lean proposition. It cannot receive proof credit
for the canonical human Rellich inequality because that proposition still has
two exact-statement mapping defects:

1. `ContDiff Real top` infers `top : WithTop ENat`, mathlib's analytic order
   `omega`; smooth infinity is `((top : ENat) : WithTop ENat)`.
2. `Euclidean n := Fin n -> Real` carries the finite Pi supremum norm;
   `EuclideanSpace Real (Fin n)` is `PiLp 2` with the Euclidean `L2` norm.

Support avoidance makes every function admitted by the malformed analytic
statement vanish near the origin. Analytic uniqueness makes it identically
zero, after which the encoded inequality simplifies to `0 <= 0`. This is a
real kernel proof of the frozen backend encoding, not a proof of the
source-mapped smooth Euclidean Rellich theorem. Rev-5.6 section 5 explicitly
forbids closing an unmapped canonical claim through a backend-specific proof.

The first failed gate remains exact backend-to-canonical statement mapping,
proposed at `M1247-S-DOMAIN`, before canonical proof credit may be inspected.
The predecessor `S56-M-1247-OBLIGATION_TREE` is only provisional `[_]`, not
master-accepted. Its registry is structurally valid but semantically stale,
and `root_of_coreRellichEstimate` consumes an explicit open
`CoreRellichEstimate` premise. The direct analytic-vacuity proof bypasses that
weighted route; it does not close `M1247-L-IBP`, `M1247-L-HARDY`, or
`M1247-L-CORE`.

Three stale projection details reinforce the failed mapping gate:

- `intake.json` names `EuclideanSpace Real (Fin n)`, while `Statement.lean`
  uses `Fin n -> Real`.
- `README.md` reverses the displayed left/right descriptions relative to the
  encoded `weighted <= Laplacian` inequality.
- `proof-blocker.json` lists `proof-validation.md` in `changed_paths`, but the
  file is absent from this tree.

## Current-Base Delta

The preceding integrated target packet was based at
`f7b3c872ab727ab689486d74020c11dc5d99869f`. Between that base and this base,
only that packet pair changed under `Stage1_Instances/THM-M-1247`. The target
statement, proof, obligation tree, registry, typed graphs, validation specs,
anchor audit, target-manifest entry, execution skill, and target task states
are unchanged. Authority-file changes promote ten unrelated items only.

There are now 35 integrated `proof-recheck-*.json` reports. The master-owned
proof item still records attempts zero and no children. Packet count is not
itself the authoritative execution-tick count, but rev-5.6 section 10.2
requires a split after five unresolved ticks. The master must reconcile these
packets rather than dispatch the same unsplit proof item again.

## Validation

Credited checks read the automation-provided pinned Lake artifacts. No update,
build, clone, fetch, network request, or `.lake` mutation was performed. Fresh
Lean outputs existed only in temporary directories under `/tmp` and were
removed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `15` assurance groups; `1546` uniform-L0 targets; execution skill present. |
| `python3 scripts/stage1_target.py check` | 0 | `1546` unique targets, ranks 1 through 1546, all `L0/rework_required`. |
| `python3 scripts/stage1_target.py show THM-M-1247` | 0 | Rank 427; lifecycle `planned`; legacy artifacts unaccepted; theorem incomplete. |
| `timeout --foreground --kill-after=5s 300s python3 Stage1_Instances/THM-M-1247/check_anchor_audit.py` | 0 | Three pinned mathlib candidate families checked; exact external candidates `0`; terminal result open. |
| `timeout --foreground --kill-after=5s 300s python3 Stage1_Instances/THM-M-1247/check_obligation_tree.py` | 0 | 13 obligations, 34 typed edges, denominator `9df3b5e9...79a590`; root open at `M3`, with six analytic obligations at `M4`. |
| Isolated pinned `lake env lean --trust=0` statement/proof recipe below | 0 | Fresh `Statement.olean` and `Proof.olean` elaborated; exact frozen type checked; axioms exactly `propext`, `Classical.choice`, and `Quot.sound`. |
| Isolated pinned `lake env lean --trust=0` statement/obligation-tree recipe below | 0 | Fresh `Statement.olean` and `ObligationTree.olean` elaborated; conditional transport and its open premise checked. |
| `rg -n -i 'Rellich\|Hardy[-_ ]?Rellich\|HardyRellich' Formalizations/Lean/.lake/packages --glob '*.lean'` | 1, expected | No matching theorem in readable pinned package sources. |
| `rg -n '\b(sorry\|admit\|sorryAx)\b\|^[[:space:]]*(axiom\|unsafe\|opaque)[[:space:]]' Stage1_Instances/THM-M-1247/{Statement,Proof,ObligationTree}.lean` | 1, expected | No prohibited lexical match; this does not replace a transitive provenance audit. |
| `git diff --name-status f7b3c872..HEAD -- Stage1_Instances/THM-M-1247 Docs/Stage1_Targets_rev-5.6.json Docs/Stage1_Blueprint_rev-5.6.md Docs/Stage1_Execution_DAG_rev-5.6.json skills/execute-stage1-rev56/SKILL.md` | 0 | Only the prior target blocker pair and ten unrelated authority promotions changed; target semantics and governing skill are unchanged. |
| `jq -c '.items[] \| select(.id \| startswith("S56-M-1247-")) \| {id,phase,state,attempts,depends_on,children}' Docs/Stage1_Execution_DAG_rev-5.6.json` | 0 | Intake through obligation tree remain `[_]`; proof remains `[ ]`, attempts zero, children empty; validation and release remain `[ ]`. |
| `git ls-tree -r --name-only HEAD Stage1_Instances/THM-M-1247 \| rg 'proof-recheck-.*\.json$' \| wc -l` | 0 | `35`; master reconciliation must decide how many are unresolved execution ticks. |
| `python3 -m json.tool Stage1_Instances/THM-M-1247/proof-recheck-2026-07-15-head-b366bdd9-slot42.json` | 0 | Current-base blocker JSON parsed. |
| Packet invariant recipe below | 0 | Item/base/tree identities, hashes, changed paths, blocker state, and deliberate self-test absence agree. |
| `git diff --check -- Stage1_Instances/THM-M-1247 .stage1-worker-selftest.json` | 0 | No whitespace diagnostics. |
| `git diff --no-index --check /dev/null FILE` separately for each new packet file | 1, expected | Each command reports an addition-only diff and emits zero whitespace diagnostics. |
| `test ! -e .stage1-worker-selftest.json` | 0 | The incomplete proof phase emitted no false worker-completion packet. |

The proof replay used the pinned `lake env lean` executable with a clean
temporary module directory:

```bash
set -euo pipefail
ROOT="$PWD"
TARGET="$ROOT/Stage1_Instances/THM-M-1247"
LEAN_ROOT="$ROOT/Formalizations/Lean"
MATHLIB="$LEAN_ROOT/.lake/packages/mathlib"
TMP=$(mktemp -d /tmp/thm1247-lake-proof.XXXXXX)
trap 'rm -rf "$TMP"' EXIT
cp "$TARGET"/{Statement,Proof}.lean "$TMP"/
BASE_LEAN_PATH="$(find -L "$LEAN_ROOT/.lake/packages" -type d \
  -path '*/.lake/build/lib/lean' -print | LC_ALL=C sort | paste -sd:):\
$(readlink -f "$LEAN_ROOT/.lake")/build/lib/lean:\
$HOME/.elan/toolchains/leanprover--lean4---v4.29.0/lib/lean"
cd "$MATHLIB"
LEAN_NUM_THREADS=1 LEAN_PATH="$BASE_LEAN_PATH" \
  timeout --foreground --kill-after=5s 300s \
  lake env lean --trust=0 -t0 --root="$TMP" \
  -o "$TMP/Statement.olean" "$TMP/Statement.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$TMP:$BASE_LEAN_PATH" \
  timeout --foreground --kill-after=5s 300s \
  lake env lean --trust=0 -t0 --root="$TMP" \
  -o "$TMP/Proof.olean" "$TMP/Proof.lean"
```

The proof-specific output was:

```text
Stage1Instances.THM_M_1247.rellichInequalityTarget : RellichInequalityTarget
'Stage1Instances.THM_M_1247.frozen_top_is_analytic_order' depends on axioms: [propext, Classical.choice, Quot.sound]
'Stage1Instances.THM_M_1247.analytic_avoidance_eq_zero' depends on axioms: [propext, Classical.choice, Quot.sound]
'Stage1Instances.THM_M_1247.rellichInequalityTarget' depends on axioms: [propext, Classical.choice, Quot.sound]
STATEMENT_EXIT=0
PROOF_EXIT=0
```

The obligation-tree replay used the same recipe with
`{Statement,ObligationTree}.lean`; it exited zero and reported:

```text
'Stage1Instances.THM_M_1247.root_of_coreRellichEstimate' depends on axioms: [propext, Classical.choice, Quot.sound]
STATEMENT_EXIT=0
OBLIGATION_TREE_EXIT=0
```

The packet invariant check was:

```bash
python3 - \
  Stage1_Instances/THM-M-1247/proof-recheck-2026-07-15-head-b366bdd9-slot42.json <<'PY'
import hashlib
import json
import pathlib
import subprocess
import sys

path = pathlib.Path(sys.argv[1])
data = json.loads(path.read_text())
root = pathlib.Path.cwd()
assert data["item_id"] == "S56-M-1247-PROOF"
assert data["theorem_id"] == "THM-M-1247"
assert data["base_revision"] == subprocess.check_output(
    ["git", "rev-parse", "HEAD"], text=True).strip()
assert data["base_tree"] == subprocess.check_output(
    ["git", "rev-parse", "HEAD^{tree}"], text=True).strip()
assert data["verdict"] == "blocked" and data["state"] == "[ ]"
assert not data["proof_phase_complete"]
assert not data["source_claim_proved"]
assert not data["root_closed"]
assert not data["theorem_complete"]
assert not data["selftest_manifest_written"]
assert data["authority_snapshot"]["integrated_prior_recheck_pairs"] == 35
assert data["first_repair_task"] == "S56-M-1247-STATEMENT"
for rel, expected in data["source_hashes"].items():
    if rel in {"lake-manifest.json", "lean-toolchain"}:
        file = root / "Formalizations" / "Lean" / rel
    else:
        file = root / "Stage1_Instances" / "THM-M-1247" / rel
    assert hashlib.sha256(file.read_bytes()).hexdigest() == expected, rel
assert all((root / rel).exists() for rel in data["changed_paths"])
assert not (root / ".stage1-worker-selftest.json").exists()
print("PASS blocker packet invariants and source hashes")
PY
```

## Retry Condition

Do not dispatch `S56-M-1247-PROOF` unchanged again. Under an authorized
statement-phase assignment, use `EuclideanSpace Real (Fin n)` and
`ContDiff Real ((top : ENat) : WithTop ENat)`, rerun exact-expression and
mutation gates, and publish a versioned obligation-registry/typed-graph delta
with downstream invalidations. Then split and implement weighted integration
by parts, derivative Hardy, normalization, the core estimate, and transport as
dependency-legal children if the master confirms the five-tick threshold.

## Status Boundary

This is current-base blocker and scheduler-escalation evidence under the owned
target path. It does not satisfy `S56-M-1247-PROOF`. The item remains `[ ]`;
there is no worker self-test, accepted receipt, canonical root closure, audit
completion, validation, release, or theorem-completion claim.
