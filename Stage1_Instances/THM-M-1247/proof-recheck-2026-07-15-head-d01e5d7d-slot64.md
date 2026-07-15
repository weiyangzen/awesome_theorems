# THM-M-1247 proof-phase recheck at `d01e5d7d` (slot64)

Item: `S56-M-1247-PROOF`

Date: `2026-07-15T08:33:43+08:00` (`Asia/Shanghai`)

Base revision: `d01e5d7daab630d25a32f781a754be9af1b82761`

Base tree: `32894fb5c2ce690dc4959f6964ed4c745d26a1ec`

## Verdict

`blocked`. The tracked placeholder-free declaration

```text
Stage1Instances.THM_M_1247.rellichInequalityTarget :
  Stage1Instances.THM_M_1247.RellichInequalityTarget
```

re-elaborates at trust level zero, but it closes only a malformed frozen Lean
encoding. It cannot receive proof credit for the canonical Rellich inequality.

The source claim requires arbitrary smooth compactly supported functions on
Euclidean space. In `Statement.lean`, however, `ContDiff Real top` infers
`top : WithTop ENat`, mathlib's analytic order `omega`, rather than smooth
order `infinity`. Support avoidance gives a neighborhood of the origin where
the analytic function is zero. Analytic uniqueness then makes it zero
everywhere, and both sides of the frozen inequality simplify to zero.

Independently, `Euclidean n := Fin n -> Real` uses mathlib's finite Pi
supremum norm. It is not `EuclideanSpace Real (Fin n)`, which is `PiLp 2` with
the Euclidean L2 norm required by the radial Rellich weight. The checked body
therefore provides diagnostic evidence for the statement mismatch, not a
proof of a broadened, repaired, or substituted theorem. A fresh search found
no exact Rellich or Hardy-Rellich declaration in the pinned Lake package
source closure.

The recorded dossier vector remains `[H1, M3, R3]`; `M5` is only the proposed
machine diagnosis. The registry and graphs remain structurally valid but
stale relative to this diagnosis. The required
`S56-M-1247-OBLIGATION_TREE` predecessor is also still provisional at `[_]`,
not master-accepted. No proof receipt, state transition, audit completion,
validation completion, release, or theorem completion is claimed.
`.stage1-worker-selftest.json` is deliberately absent because the assigned
positive proof phase is not genuinely complete.

## Failed Gate

The first failed gate is the Stage1 rev-5.6 section 5.1 Lean statement gate;
`M1247-S-DOMAIN` is the proposed first invalidated obligation mapping. The
first repair task is `S56-M-1247-STATEMENT`. A repaired statement would also
require refreshing `S56-M-1247-ANCHOR_AUDIT` and
`S56-M-1247-OBLIGATION_TREE`. The frozen proof graph still reports the stale
cut `M1247-L-IBP`, `M1247-L-HARDY`, `M1247-N-WEIGHTS`,
`M1247-S-BOUNDARY`, `M1247-S-DOMAIN`, and `M1247-S-LAPLACIAN`; it cannot
supersede the earlier statement mismatch. Correcting the statement in this
proof-only item would be an unauthorized substitution and would invalidate
the frozen downstream artifacts.

Retry only after an authorized statement-phase repair uses
`EuclideanSpace Real (Fin n)` and
`ContDiff Real ((top : ENat) : WithTop ENat)`, reruns the statement and
mutation gates, and publishes a versioned registry/graph delta with downstream
invalidations before a new proof attempt.

## Validation

All credited checks ran in this worker clone against the existing pinned Lean
and Lake artifacts. No `lake update`, `lake build`, dependency clone/fetch,
network action, or other `.lake` mutation was performed. Generated Lean output
was confined to fresh `/tmp` directories; checker-created transient source
files were removed by the checkers. The automation-provided untracked `.lake`
symlink makes this nonrelease evidence.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-1247` | 0 | Rank 427; lifecycle `planned`; baseline `L0/rework_required`; legacy artifacts unaccepted; theorem incomplete. |
| `git status --short --untracked-files=all` before this report | 0 | Only the automation-provided `?? Formalizations/Lean/.lake` symlink was present; the owned target path was clean. |
| `python3 Stage1_Instances/THM-M-1247/check_statement.py` | 0 | Expression SHA-256 `4697dbba...5c90e`; all four recorded structural mutations killed. This confirms elaboration of the frozen encoding, not source-statement fidelity. |
| `python3 Stage1_Instances/THM-M-1247/check_anchor_audit.py` | 0 | Three pinned mathlib candidate families checked; zero exact external candidates; terminal result remains open. |
| `python3 Stage1_Instances/THM-M-1247/check_obligation_tree.py` | 0 | `PASS`: 13 obligations and 34 typed edges; denominator `9df3b5e...79a590`; root open at M3 with six obligations at M4. |
| Isolated pinned `lake env lean --trust=0` recipe below | 0 | Fresh `Statement.olean` plus `Proof.lean` elaborated. The root has the exact frozen type; all three proof declarations report exactly `[propext, Classical.choice, Quot.sound]`. |
| Independent isolated execution of the same two-step pinned recipe | 0 | A second agent independently derived and rechecked the same proof in a separate fresh `/tmp` directory, with the same exact type and axiom output. This is corroboration, not rev-5.6 independent release validation. |
| `sed -n '88,125p' Formalizations/Lean/.lake/packages/mathlib/Mathlib/Analysis/Calculus/ContDiff/FTaylorSeries.lean` | 0 | Pinned mathlib defines analytic `omega` as `top : WithTop ENat` and smooth `infinity` as `((top : ENat) : WithTop ENat)`. |
| `sed -n '32,40p;96,120p' Formalizations/Lean/.lake/packages/mathlib/Mathlib/Analysis/InnerProductSpace/PiL2.lean` | 0 | Pinned mathlib defines `EuclideanSpace` as `PiLp 2`, with the L2 norm. |
| `rg -n -i 'Rellich\|Hardy[-_ ]?Rellich\|HardyRellich' Formalizations/Lean/.lake/packages --glob '*.lean'` | 1 | Expected no-match from this fresh narrow corroborating search; the preceding anchor audit owns the broader candidate inventory. |
| `rg -n '\b(sorry\|admit\|sorryAx)\b\|^[[:space:]]*(axiom\|unsafe\|opaque)[[:space:]]' Stage1_Instances/THM-M-1247/{Statement,Proof}.lean` | 1 | Expected no-match in this local lexical scan. This does not substitute for a transitive provenance scan. |
| `python3 -m json.tool Stage1_Instances/THM-M-1247/proof-recheck-2026-07-15-head-d01e5d7d-slot64.json >/dev/null` plus the invariant recipe below | 0 | Current-base blocker fields, source hashes, open-state boundary, and deliberate self-test absence agree. |
| `git diff --check -- Stage1_Instances/THM-M-1247` | 0 | No whitespace errors in tracked owned changes. |
| `git diff --no-index --check /dev/null Stage1_Instances/THM-M-1247/proof-recheck-2026-07-15-head-d01e5d7d-slot64.json` | 1, expected added-file diff | No whitespace errors in the new JSON packet. |
| `git diff --no-index --check /dev/null Stage1_Instances/THM-M-1247/proof-recheck-2026-07-15-head-d01e5d7d-slot64.md` | 1, expected added-file diff | No whitespace errors in the new Markdown report. |
| `test ! -e .stage1-worker-selftest.json` | 0 | The incomplete proof phase emitted no worker-completion packet. |

The isolated Lean recipe was:

```bash
set -euo pipefail
ROOT="$PWD"
TARGET="$ROOT/Stage1_Instances/THM-M-1247"
LEAN_ROOT="$ROOT/Formalizations/Lean"
TMP=$(mktemp -d /tmp/thm-m-1247-proof-head-d01e5d7d.XXXXXX)
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

The exact proof-specific output was:

```text
Stage1Instances.THM_M_1247.rellichInequalityTarget : RellichInequalityTarget
'Stage1Instances.THM_M_1247.frozen_top_is_analytic_order' depends on axioms: [propext, Classical.choice, Quot.sound]
'Stage1Instances.THM_M_1247.analytic_avoidance_eq_zero' depends on axioms: [propext, Classical.choice, Quot.sound]
'Stage1Instances.THM_M_1247.rellichInequalityTarget' depends on axioms: [propext, Classical.choice, Quot.sound]
```

The expanded statement output also contains `@Top.top (WithTop ENat)` and the
finite-Pi `@Pi.normedAddCommGroup`/`@Pi.normedSpace` instances, confirming the
two encoding mismatches described above.

The packet invariant recipe was:

```bash
python3 - \
  Stage1_Instances/THM-M-1247/proof-recheck-2026-07-15-head-d01e5d7d-slot64.json <<'PY'
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
