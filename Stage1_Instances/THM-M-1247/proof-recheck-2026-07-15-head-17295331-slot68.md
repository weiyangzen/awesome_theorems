# THM-M-1247 proof-phase recheck at `17295331` (slot68)

Item: `S56-M-1247-PROOF`

Date: `2026-07-15T09:01:05+08:00` (`Asia/Shanghai`)

Base revision: `1729533156a59958dac4908793303a66434eb925`

Base tree: `604b6669e6ab2f485c9dcb71de3a150c6deaf755`

## Verdict

`blocked`. The existing placeholder-free declaration

```text
Stage1Instances.THM_M_1247.rellichInequalityTarget :
  Stage1Instances.THM_M_1247.RellichInequalityTarget
```

re-elaborates at trust level zero, but it closes only a malformed frozen Lean
encoding. It cannot receive proof credit for the canonical Rellich inequality.

The source claim quantifies over arbitrary smooth compactly supported functions
on Euclidean space. In `Statement.lean`, `ContDiff Real top` instead infers
`top : WithTop ENat`, mathlib's analytic order `omega`, not smooth order
`infinity`. Support avoidance gives a neighborhood of the origin on which the
analytic function is zero. Analytic uniqueness then makes it zero everywhere,
so both sides of the encoded inequality simplify to zero.

Independently, `Euclidean n := Fin n -> Real` has the finite Pi supremum norm.
It is not `EuclideanSpace Real (Fin n)`, the `PiLp 2` space carrying the
Euclidean L2 norm required by the radial weight. The checked body is therefore
diagnostic evidence for an exact-statement mismatch, not a proof of the
classical theorem. A fresh narrow search found no exact Rellich or
Hardy-Rellich declaration in the pinned package sources.

The root vector remains `[H1, M3, R3]`; `M5` is only a proposed diagnosis. The
frozen registry and graphs are structurally valid but stale relative to that
diagnosis. The required `S56-M-1247-OBLIGATION_TREE` predecessor is also only
worker-provisional at `[_]`, not master-accepted. No proof receipt, state
transition, audit completion, validation, release, or theorem completion is
claimed. `.stage1-worker-selftest.json` is deliberately absent because the
assigned positive proof phase is not genuinely complete.

## Failed Gate

The first failed gate is Stage1 rev-5.6 section 5.1, the exact Lean statement
gate; `M1247-S-DOMAIN` is the proposed first invalidated obligation. The first
repair task is `S56-M-1247-STATEMENT`. Correcting the statement in this
proof-only assignment would be an unauthorized substitution and would also
invalidate the frozen inputs to the anchor audit and obligation tree.

Retry only after an authorized statement-phase repair uses
`EuclideanSpace Real (Fin n)` and
`ContDiff Real ((top : ENat) : WithTop ENat)`, reruns the statement and mutation
gates, and publishes a versioned registry/graph delta with downstream
invalidations before a new proof attempt.

## Validation

All credited checks ran in this worker clone using the existing pinned Lean and
Lake artifacts. No update, build, clone, fetch, network action, or `.lake`
mutation was performed. Lean outputs were confined to a fresh `/tmp` directory;
checker-created transient source files were removed. The automation-provided
untracked `.lake` symlink makes this nonrelease evidence.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-1247` | 0 | Rank 427; lifecycle `planned`; baseline `L0/rework_required`; legacy artifacts unaccepted; theorem incomplete. |
| `git status --short --untracked-files=all` before this report | 0 | Only `?? Formalizations/Lean/.lake`, the automation-provided symlink; the owned target path was clean. |
| `python3 Stage1_Instances/THM-M-1247/check_statement.py` | 0 | Expression SHA-256 `4697dbba...5c90e`; all four recorded structural mutations killed. This checks the frozen encoding, not its source fidelity. |
| `python3 Stage1_Instances/THM-M-1247/check_anchor_audit.py` | 0 | Three pinned mathlib candidate families checked; zero exact external candidates; terminal result open. |
| `python3 Stage1_Instances/THM-M-1247/check_obligation_tree.py` | 0 | `PASS`: 13 obligations and 34 typed edges; denominator `9df3b5e...79a590`; root open at M3 and six root-relevant obligations recorded at M4. |
| Isolated pinned `lake env lean --trust=0` recipe below | 0 | Fresh `Statement.olean` and `Proof.lean` elaborated. The root has the exact frozen type; all three local proof declarations report `[propext, Classical.choice, Quot.sound]`. |
| Two independent task-agent isolated elaborations | 0, 0 | Each independently reported the same frozen exact type and axiom output. They are corroboration only, not rev-5.6 release-independence evidence. |
| `sed -n '88,125p' pinned mathlib `FTaylorSeries.lean` | 0 | Pinned mathlib defines analytic `omega` as `top : WithTop ENat` and smooth `infinity` as `((top : ENat) : WithTop ENat)`. |
| `sed -n '32,40p;96,120p' pinned mathlib `PiL2.lean` | 0 | Pinned mathlib defines `EuclideanSpace` as `PiLp 2`, with the L2 norm. |
| `rg -n -i 'Rellich\|Hardy[-_ ]?Rellich\|HardyRellich' Formalizations/Lean/.lake/packages --glob '*.lean'` | 1 | Expected no-match from the narrow corroborating search; the anchor audit owns the broader inventory. |
| `rg -n '\b(sorry\|admit\|sorryAx)\b\|^[[:space:]]*(axiom\|unsafe\|opaque)[[:space:]]' Stage1_Instances/THM-M-1247/{Statement,Proof}.lean` | 1 | Expected no-match in this local lexical scan; it is not a transitive provenance check. |
| Packet invariant and source-hash recipe below | 0 | Current-base identity, hashes, open-state boundary, dependency status, and deliberate self-test absence agree. |
| `git diff --check -- Stage1_Instances/THM-M-1247` | 0 | No whitespace errors in owned changes. |
| `git diff --no-index --check /dev/null <new-file>` | 1, expected | Each report is an added-file diff and emits no whitespace diagnostic. |
| `test ! -e .stage1-worker-selftest.json` | 0 | The incomplete proof phase emitted no worker-completion packet. |

The isolated Lean recipe was:

```bash
set -euo pipefail
ROOT="$PWD"
TARGET="$ROOT/Stage1_Instances/THM-M-1247"
LEAN_ROOT="$ROOT/Formalizations/Lean"
TMP=$(mktemp -d /tmp/thm-m-1247-proof-head-17295331-slot68.XXXXXX)
trap 'rm -rf "$TMP"' EXIT
cp "$TARGET"/{Statement,Proof}.lean "$TMP/"
cd "$LEAN_ROOT"
BASE_LEAN_PATH=$(timeout 180 lake env printenv LEAN_PATH)
LEAN_NUM_THREADS=1 LEAN_PATH="$BASE_LEAN_PATH" timeout 600 \
  lake env lean --trust=0 -t0 --root="$TMP" \
  -o "$TMP/Statement.olean" "$TMP/Statement.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$TMP:$BASE_LEAN_PATH" timeout 600 \
  lake env lean --trust=0 -t0 --root="$TMP" "$TMP/Proof.lean"
```

The proof-specific output was:

```text
Stage1Instances.THM_M_1247.rellichInequalityTarget : RellichInequalityTarget
'Stage1Instances.THM_M_1247.frozen_top_is_analytic_order' depends on axioms: [propext, Classical.choice, Quot.sound]
'Stage1Instances.THM_M_1247.analytic_avoidance_eq_zero' depends on axioms: [propext, Classical.choice, Quot.sound]
'Stage1Instances.THM_M_1247.rellichInequalityTarget' depends on axioms: [propext, Classical.choice, Quot.sound]
```

The expanded statement output also contains `@Top.top (WithTop ENat)` and the
finite-Pi `@Pi.normedAddCommGroup`/`@Pi.normedSpace` instances, confirming the
two encoding mismatches described above.

The packet check was:

```bash
python3 - \
  Stage1_Instances/THM-M-1247/proof-recheck-2026-07-15-head-17295331-slot68.json <<'PY'
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
assert not data["root_closed"]
assert not data["audit_complete"]
assert not data["theorem_complete"]
assert data["accepted_receipt_ids"] == []
assert not data["selftest_manifest_written"]
assert not (root / ".stage1-worker-selftest.json").exists()
assert data["dependency_gate"]["observed_state"] == "[_]"
assert not data["dependency_gate"]["master_accepted"]
assert data["first_repair_task"] == "S56-M-1247-STATEMENT"
assert data["workflow_acceptance_cut_set"] == [
    "S56-M-1247-STATEMENT", "S56-M-1247-ANCHOR_AUDIT",
    "S56-M-1247-OBLIGATION_TREE",
]
assert data["remaining_root_cut_set"] == [
    "M1247-L-IBP", "M1247-L-HARDY", "M1247-N-WEIGHTS",
    "M1247-S-BOUNDARY", "M1247-S-DOMAIN", "M1247-S-LAPLACIAN",
]
for rel, expected in data["source_hashes"].items():
    if rel in {"lake-manifest.json", "lean-toolchain"}:
        file = root / "Formalizations" / "Lean" / rel
    else:
        file = root / "Stage1_Instances" / "THM-M-1247" / rel
    assert hashlib.sha256(file.read_bytes()).hexdigest() == expected
assert all((root / rel).exists() for rel in data["changed_paths"])
print("PASS blocker packet invariants and source hashes")
PY
```

## Status Boundary

This is current-base blocker evidence under the owned target path. It is not a
positive proof receipt and does not satisfy `S56-M-1247-PROOF`. The assigned
item remains `[ ]`; no accepted receipt ID or worker self-test manifest exists.
