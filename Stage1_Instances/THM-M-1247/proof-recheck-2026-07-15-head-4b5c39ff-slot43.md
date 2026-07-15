# THM-M-1247 proof recheck at `4b5c39ff` (slot43)

Item: `S56-M-1247-PROOF`

Base revision: `4b5c39ffcc0e35a8509d4216af53c7cdeb190c7b`

Base tree: `e569e54769b7b5aab913ec248c533231658657f0`

Run date: `2026-07-15T19:16:35+08:00`

## Verdict

`blocked`. The proof phase is not complete, so no
`.stage1-worker-selftest.json` was emitted.

The existing placeholder-free `Proof.lean` re-elaborates an inhabitant of the
frozen Lean proposition at trust level zero. It cannot receive proof credit for
the canonical human Rellich inequality because the frozen proposition has two
exact-statement mapping defects:

1. `ContDiff Real top` infers `top : WithTop ENat`, mathlib's analytic order
   `omega`; smooth infinity is `((top : ENat) : WithTop ENat)`.
2. `Euclidean n := Fin n -> Real` carries the finite Pi supremum norm;
   `EuclideanSpace Real (Fin n)` is `PiLp 2` with the Euclidean `L2` norm.

Support avoidance makes every function admitted by the malformed analytic
statement vanish near the origin. Analytic uniqueness then makes it
identically zero, after which the encoded inequality simplifies to `0 <= 0`.
This is a kernel proof of the frozen backend encoding, not a proof of the
source-mapped smooth Euclidean Rellich theorem. Rev-5.6 section 5 forbids
crediting an unmapped backend encoding as the canonical claim.

The first failed gate remains exact backend-to-canonical statement mapping,
proposed at `M1247-S-DOMAIN`, before proof credit may be inspected. The
predecessor `S56-M-1247-OBLIGATION_TREE` is only provisional `[_]`, not
master-accepted. Its registry is structurally valid but semantically stale
after this mapping diagnosis, and its checked root theorem consumes an
explicit open `CoreRellichEstimate` premise.

## Current-Base Delta

The immediately preceding integrated THM-M-1247 packet was based at
`69662621a19907de342801b09124e8dfe3495e40`. Between that base and this base,
only that packet pair changed under the target path. The statement, proof,
obligation tree, registry, typed graphs, validation specs, anchor audit,
target-manifest row, execution skill, and THM-M-1247 item states are unchanged.
Authority-file changes promote three unrelated items only.

There are now 33 integrated `proof-recheck-*.json` reports. The master-owned
proof item still records attempts zero and no children. Rev-5.6 requires a
split after five unresolved execution ticks, but packet count is not itself an
authoritative tick count. The statement phase must be repaired before this
proof item can proceed. Separately, the master must reconcile these packets
with actual ticks and create dependency-legal repair and proof children if at
least five packets qualify. This worker may not edit the authoritative DAG.

## Validation

All Lean checks read the automation-provided pinned Lake artifacts. No update,
build, clone, fetch, network request, or `.lake` mutation was performed. Fresh
outputs existed only in a temporary directory under `/tmp` and were removed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `15` assurance groups; `1546` uniform-L0 targets; execution skill present. |
| `python3 scripts/stage1_target.py check` | 0 | `1546` unique targets, ranks 1 through 1546, all `L0/rework_required`. |
| `python3 scripts/stage1_target.py show THM-M-1247` | 0 | Rank 427; lifecycle `planned`; legacy artifacts unaccepted; theorem incomplete. |
| `timeout --foreground --kill-after=5s 300s python3 Stage1_Instances/THM-M-1247/check_statement.py` | 0 | Frozen expression SHA-256 `4697dbba...5c90e`; all four recorded mutations killed. This does not validate the human-claim mapping. |
| `timeout --foreground --kill-after=5s 300s python3 Stage1_Instances/THM-M-1247/check_anchor_audit.py` | 0 | Three pinned mathlib candidate families checked; exact external candidates `0`; terminal result open. |
| `timeout --foreground --kill-after=5s 300s python3 Stage1_Instances/THM-M-1247/check_obligation_tree.py` | 0 | 13 obligations, 34 typed edges, denominator `9df3b5e9...79a590`; root open at `M3`, with six analytic obligations at `M4`. |
| Isolated pinned `lake env lean --trust=0` recipe below | 0 | Fresh `Statement.olean`, `Proof.lean`, and `ObligationTree.lean` elaborated; exact frozen type checked; axioms exactly `propext`, `Classical.choice`, and `Quot.sound`. |
| `rg -n -i 'Rellich\|Hardy[-_ ]?Rellich\|HardyRellich' Formalizations/Lean/.lake/packages --glob '*.lean'` | 1, expected | No matching theorem in readable pinned package sources. |
| `rg -n '\b(sorry\|admit\|sorryAx)\b\|^[[:space:]]*(axiom\|unsafe\|opaque)[[:space:]]' Stage1_Instances/THM-M-1247/{Statement,Proof,ObligationTree}.lean` | 1, expected | No prohibited lexical match; this is defense in depth, not a transitive provenance audit. |
| `git diff --name-status 69662621..HEAD -- Stage1_Instances/THM-M-1247 Docs/Stage1_Targets_rev-5.6.json Docs/Stage1_Blueprint_rev-5.6.md Docs/Stage1_Execution_DAG_rev-5.6.json skills/execute-stage1-rev56/SKILL.md` | 0 | Only the prior target blocker pair and three unrelated authority-state promotions changed; target semantics and governing skill are unchanged. |
| `jq -c '.items[] \| select(.id == "S56-M-1247-STATEMENT" or .id == "S56-M-1247-ANCHOR_AUDIT" or .id == "S56-M-1247-OBLIGATION_TREE" or .id == "S56-M-1247-PROOF") \| {id,state,attempts,children,depends_on}' Docs/Stage1_Execution_DAG_rev-5.6.json` | 0 | The first three phases remain `[_]`, attempts 1; proof remains `[ ]`, attempts 0, children empty. |
| `git ls-tree -r --name-only HEAD Stage1_Instances/THM-M-1247 \| rg 'proof-recheck-.*\.json$' \| wc -l` | 0 | `33`; master reconciliation must determine how many qualify as unresolved execution ticks. |
| `python3 -m json.tool Stage1_Instances/THM-M-1247/proof-recheck-2026-07-15-head-4b5c39ff-slot43.json` | 0 | Blocker JSON parsed. |
| Packet invariant recipe below | 0 | Item/base/tree identities, hashes, changed-path count, blocker state, and deliberate self-test absence agree. |
| `git diff --check -- Stage1_Instances/THM-M-1247 .stage1-worker-selftest.json` | 0 | No whitespace diagnostics. |
| `git diff --no-index --check /dev/null FILE` separately for each new packet file | 1, expected | Each command reports an addition-only diff and emits zero whitespace diagnostics. |
| `test ! -e .stage1-worker-selftest.json` | 0 | The incomplete proof phase emitted no false worker-completion packet. |

The narrow Lean replay was:

```bash
set -euo pipefail
ROOT="$PWD"
TARGET="$ROOT/Stage1_Instances/THM-M-1247"
LEAN_ROOT="$ROOT/Formalizations/Lean"
MATHLIB="$LEAN_ROOT/.lake/packages/mathlib"
TMP=$(mktemp -d /tmp/thm-m-1247-proof-head-4b5c39ff-slot43.XXXXXX)
trap 'rm -rf "$TMP"' EXIT
cp "$TARGET"/{Statement,Proof,ObligationTree}.lean "$TMP"/
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

The expanded root output contains `@Top.top (WithTop ENat)` and finite-Pi
`@Pi.normedAddCommGroup` / `@Pi.normedSpace` instances, independently
confirming both mapping defects.

The packet invariant recipe was:

```bash
python3 - \
  Stage1_Instances/THM-M-1247/proof-recheck-2026-07-15-head-4b5c39ff-slot43.json <<'PY'
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
assert not data["theorem_complete"]
assert not data["selftest_manifest_written"]
assert data["authority_snapshot"]["integrated_prior_recheck_pairs"] == 33
assert data["first_repair_task"] == "S56-M-1247-STATEMENT"
for rel, expected in data["source_hashes"].items():
    if rel in {"lake-manifest.json", "lean-toolchain"}:
        file = root / "Formalizations" / "Lean" / rel
    else:
        file = root / "Stage1_Instances" / "THM-M-1247" / rel
    assert hashlib.sha256(file.read_bytes()).hexdigest() == expected
assert all((root / rel).exists() for rel in data["changed_paths"])
assert not (root / ".stage1-worker-selftest.json").exists()
print("PASS blocker packet invariants and source hashes")
PY
```

## Retry Condition

Do not silently dispatch `S56-M-1247-PROOF` unchanged again. Under an
authorized statement-phase assignment, use `EuclideanSpace Real (Fin n)` and
`ContDiff Real ((top : ENat) : WithTop ENat)`, rerun exact-expression and
mutation gates, publish a versioned obligation-registry/typed-graph delta with
downstream invalidations, and only then resume proof execution. Separately,
reconcile the prior packets with the authoritative tick counter and split
weighted integration by parts, derivative Hardy, normalization, core estimate,
and transport into dependency-legal child tasks if the five-tick threshold is
confirmed.

## Status Boundary

This is current-base blocker and scheduler-escalation evidence under the owned
target path. It does not satisfy `S56-M-1247-PROOF`. The item remains `[ ]`;
there is no worker self-test, accepted receipt, audit completion, validation,
release, or theorem-completion claim.
