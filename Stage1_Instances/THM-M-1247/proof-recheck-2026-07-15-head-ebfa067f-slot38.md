# THM-M-1247 proof-phase recheck at `ebfa067f` (slot38)

## Verdict

`blocked`; `S56-M-1247-PROOF` remains `[ ]` and the lifecycle remains
`planned`. The exact frozen Lean proposition still has a placeholder-free
kernel proof, but it is not the canonical classical Rellich inequality. No
proof body, authority surface, task state, or root self-test manifest was
changed.

The first failed gate is the Stage1 rev-5.6 section 5
backend-to-canonical-statement mapping gate. In the frozen target,
`ContDiff Real top` elaborates at order `top : WithTop ENat`, which is
mathlib's analytic order `omega`, not smooth infinity. In addition,
`Fin n -> Real` uses the finite Pi supremum norm, not the Euclidean `L2`
norm. The current obligation registry predates this diagnosis and cannot
support canonical proof credit.

The existing `Proof.lean` proves only the malformed encoding. Support
avoidance makes the admitted analytic function zero near the origin;
analytic uniqueness makes it identically zero; simplification then closes
both integrals. The trust-0 replay reports only `propext`,
`Classical.choice`, and `Quot.sound`. This diagnostic is not a broadened or
substituted proof of Rellich's inequality.

The source crosswalk also records DOI `10.1007/PL00004387`; the cited
Davies-Hinz article in volume 227, pages 511-523 is DOI
`10.1007/PL00004389`. That correction belongs to an authorized source or
statement task and leaves the human-source status at `H1` here.

## Authority And Delta

- Base commit: `ebfa067f2385ca03cc0a0eeecf151993a994962c`
- Base tree: `4d482bdb45ec4ff17c128d712608f7c7eea1ffc8`
- Target rank/lane: `427` / `hard_mathlib_anchor_and_wrapper`
- Dependency: `S56-M-1247-OBLIGATION_TREE` is provisional `[_]`, not
  master-accepted
- Proof authority: `[ ]`, attempts `0`, children `[]`
- Integrated prior proof recheck JSON packets: `39`; this count is not
  asserted to equal normative execution ticks
- Prior packet: `proof-recheck-2026-07-15-head-4516c2b9-slot40.{json,md}`

Since that packet, only its two target-owned blocker files and four
unrelated authority promotions were integrated. `Statement.lean`,
`Proof.lean`, `ObligationTree.lean`, the target registry/graphs, the target
manifest entry, the THM-M-1247 task states, and the execution skill did not
change.

The master must reconcile the repeated blocker packets with execution ticks.
If at least five qualify, section 10.2 requires dependency-legal child tasks
instead of another unsplit dispatch. This worker cannot edit the master-owned
DAG.

## Validation

All checks used the existing pinned worker cache. No network, `lake update`,
`lake build`, clone, or fetch was used.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Standard structure passes for 1546 uniform-L0 targets. |
| `python3 scripts/stage1_target.py check` | 0 | Ordered target manifest passes. |
| `python3 scripts/stage1_target.py show THM-M-1247` | 0 | Rank 427; planned; L0/rework required; theorem incomplete. |
| `timeout --foreground --kill-after=5s 300s python3 Stage1_Instances/THM-M-1247/check_statement.py` | 0 | Frozen expression hash `4697dbba...a5c90e`; all four recorded mutations killed. This does not validate canonical mapping. |
| `timeout --foreground --kill-after=5s 300s python3 Stage1_Instances/THM-M-1247/check_anchor_audit.py` | 0 | Three pinned mathlib candidate families checked; zero exact candidates; terminal result open. |
| `timeout --foreground --kill-after=5s 300s python3 Stage1_Instances/THM-M-1247/check_obligation_tree.py` | 0 | 13 obligations and 34 typed edges pass structurally; root remains M3 and six analytic obligations M4. |
| Isolated pinned `lake env lean --trust=0 -t0` replay below | 0 | Fresh statement, proof, and composition modules elaborate; frozen-target defects remain visible. |
| `rg -n -i 'Rellich|Hardy[-_ ]?Rellich|HardyRellich' Formalizations/Lean/.lake/packages --glob '*.lean'` | 1, expected | No match in readable pinned package Lean sources. |
| Placeholder/bodyless lexical scan over the three Lean modules | 1, expected | No `sorry`, `admit`, `sorryAx`, `axiom`, `unsafe`, or `opaque` match. |
| `git diff --name-status 4516c2b9..HEAD` over target/governing inputs | 0 | Prior blocker pair plus unrelated promotions only; no target semantic or task-state change. |
| Count integrated `proof-recheck-*.json` files before this packet | 0 | `39`; no claim that packet count equals execution ticks. |
| `python3 -m json.tool <current blocker JSON> >/dev/null` | 0 | Current-base packet parses. |
| Target-scoped packet invariant recipe below | 0 | Identities, hashes, open state, changed paths, and deliberate self-test absence agree. |
| `git diff --check -- Stage1_Instances/THM-M-1247 .stage1-worker-selftest.json` | 0 | No whitespace diagnostics. |
| `git diff --no-index --check /dev/null <new-packet-file>` for each companion | 1, expected | Addition-only exit with no whitespace diagnostics. |
| `test ! -e .stage1-worker-selftest.json` | 0 | No false proof-completion handoff exists. |

The narrow kernel replay was:

```bash
set -euo pipefail
ROOT="$PWD"
TARGET="$ROOT/Stage1_Instances/THM-M-1247"
LEAN_ROOT="$ROOT/Formalizations/Lean"
MATHLIB="$LEAN_ROOT/.lake/packages/mathlib"
TMP=$(mktemp -d /tmp/thm-m-1247-proof-head-ebfa067f-slot38.XXXXXX)
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
  lake env lean --trust=0 -t0 --root="$TMP" \
  -o "$TMP/Proof.olean" "$TMP/Proof.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$TMP:$BASE_LEAN_PATH" \
  timeout --foreground --kill-after=5s 300s \
  lake env lean --trust=0 -t0 --root="$TMP" \
  -o "$TMP/ObligationTree.olean" "$TMP/ObligationTree.lean"
```

Proof-specific output:

```text
Stage1Instances.THM_M_1247.rellichInequalityTarget : RellichInequalityTarget
'Stage1Instances.THM_M_1247.frozen_top_is_analytic_order' depends on axioms: [propext, Classical.choice, Quot.sound]
'Stage1Instances.THM_M_1247.analytic_avoidance_eq_zero' depends on axioms: [propext, Classical.choice, Quot.sound]
'Stage1Instances.THM_M_1247.rellichInequalityTarget' depends on axioms: [propext, Classical.choice, Quot.sound]
'Stage1Instances.THM_M_1247.root_of_coreRellichEstimate' depends on axioms: [propext, Classical.choice, Quot.sound]
STATEMENT_EXIT=0
PROOF_EXIT=0
OBLIGATION_TREE_EXIT=0
```

The expanded target contains `@Top.top (WithTop ENat)` and finite-Pi
`@Pi.normedAddCommGroup` / `@Pi.normedSpace` instances, independently
confirming both mapping defects.

The packet invariant recipe is:

```bash
python3 - \
  Stage1_Instances/THM-M-1247/proof-recheck-2026-07-15-head-ebfa067f-slot38.json <<'PY'
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
assert not data["canonical_root_closed"]
assert not data["theorem_complete"]
assert not data["selftest_manifest_written"]
assert data["authority_snapshot"]["integrated_prior_recheck_pairs"] == 39
assert data["first_repair_task"] == "S56-M-1247-STATEMENT"
for rel, expected in data["source_hashes"].items():
    if rel in {"lake-manifest.json", "lean-toolchain"}:
        file = root / "Formalizations" / "Lean" / rel
    else:
        file = root / "Stage1_Instances" / "THM-M-1247" / rel
    assert hashlib.sha256(file.read_bytes()).hexdigest() == expected
for rel in data["changed_paths"]:
    assert (root / rel).exists()
assert not (root / ".stage1-worker-selftest.json").exists()
print("PASS blocker packet invariants and source hashes")
PY
```

## Retry Condition

Do not dispatch this proof item unchanged again. Under an authorized
statement-phase assignment, replace the domain with
`EuclideanSpace Real (Fin n)` and analytic `top` with smooth
`((top : ENat) : WithTop ENat)`. Then rerun exact-expression and mutation
gates and publish a versioned registry/graph delta with downstream
invalidations. Correct the Davies-Hinz DOI under the appropriate source or
statement task. After that, implement the weighted integration-by-parts,
sharp Hardy, normalization, core-estimate, and transport obligations as
dependency-legal children if the master confirms the five-tick threshold.

## Status Boundary

This is current-base blocker and scheduler-escalation evidence only. It does
not satisfy `S56-M-1247-PROOF`; the item remains `[ ]`. No proof receipt,
canonical root closure, audit completion, validation, release, or theorem
completion is claimed.
