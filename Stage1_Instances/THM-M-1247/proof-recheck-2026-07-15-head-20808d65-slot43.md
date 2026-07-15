# THM-M-1247 proof recheck at `20808d65` (slot43)

Item: `S56-M-1247-PROOF`

Base revision: `20808d65f53d8801e78f061504b93bb7efd49489`

Base tree: `a5bf33a278a7a285878c89177838ae1a0dcc9990`

Run date: `2026-07-15T17:19:42+08:00`

## Verdict

`blocked`. The proof phase is not complete, so no
`.stage1-worker-selftest.json` was emitted.

The tracked `Proof.lean` is placeholder-free and kernel-checks an inhabitant of
the frozen Lean proposition at trust level zero. It cannot receive proof credit
for the canonical human Rellich inequality because the frozen proposition has
two exact-statement mapping defects:

1. `ContDiff Real top` infers `top : WithTop ENat`, mathlib's analytic order
   `omega`; smooth infinity is `((top : ENat) : WithTop ENat)`.
2. `Euclidean n := Fin n -> Real` carries the finite Pi supremum norm;
   `EuclideanSpace Real (Fin n)` is `PiLp 2` with the Euclidean `L2` norm.

Support avoidance makes each function admitted by the malformed analytic
statement vanish near the origin. Analytic uniqueness makes it identically
zero, after which both integrals simplify to zero. That is a real proof of the
frozen backend encoding, but rev-5.6 section 5 says closing an unmapped backend
encoding does not close the canonical mathematical claim.

The first failed gate is therefore section 5's exact backend-to-canonical
statement mapping gate, proposed at `M1247-S-DOMAIN`, before proof credit may be
inspected.
The predecessor `S56-M-1247-OBLIGATION_TREE` is only provisional `[_]`, not
master-accepted. Its 13-obligation registry is structurally valid but stale
after this diagnosis; `root_of_coreRellichEstimate` also remains only a
conditional transport from an open `CoreRellichEstimate` premise.

## Current-Base Delta

The immediately preceding integrated target packet was based at
`4d389eb47e043f6f44925a418baee0d034f764ba`. Its JSON and Markdown companions
are the only THM-M-1247 files added between that base and this base. The target
statement, proof, obligation tree, registry, typed graphs, validation specs,
anchor audit, target-manifest row, execution skill, predecessor state, proof
item state, attempts, and children did not change. Intervening authority-file
changes concern six unrelated targets.

There were 29 integrated `proof-recheck-*.json` reports before this packet. The
master-owned proof item still records attempts zero and no children. These
repeated unresolved dispatch reports warrant the mandatory split rather than
another unchanged proof assignment. A worker cannot edit the authoritative
DAG; the scheduler must stop redispatching this unchanged proof item, reopen
the statement phase, and create dependency-legal repair and proof children.

## Validation

All Lean checks read the automation-provided pinned Lake artifacts. No update,
build, clone, fetch, network request, or `.lake` mutation was performed. Fresh
outputs existed only in temporary directories under `/tmp` and were removed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `15` assurance groups; `1546` uniform-L0 targets; execution skill present. |
| `python3 scripts/stage1_target.py check` | 0 | `1546` unique targets, ranks 1 through 1546, all `L0/rework_required`. |
| `python3 scripts/stage1_target.py show THM-M-1247` | 0 | Rank 427; lifecycle `planned`; legacy artifacts unaccepted; theorem incomplete. |
| `timeout --foreground --kill-after=5s 300s python3 Stage1_Instances/THM-M-1247/check_statement.py` | 0 | Frozen expression SHA-256 `4697dbba...5c90e`; all four recorded mutations killed. This does not validate human-claim mapping. |
| `timeout --foreground --kill-after=5s 300s python3 Stage1_Instances/THM-M-1247/check_anchor_audit.py` | 0 | Three pinned mathlib candidate families checked; exact external candidates `0`; terminal result open. |
| `python3 Stage1_Instances/THM-M-1247/check_obligation_tree.py` | 0 | 13 obligations, 34 typed edges, denominator `9df3b5e9...79a590`; root open at `M3`, with six analytic obligations at `M4`. |
| Literal isolated pinned `lake env lean --trust=0` shell recipe below | 0 | Fresh `Statement.olean`, `Proof.lean`, and `ObligationTree.lean` elaborated; exact frozen type checked; axioms exactly `propext`, `Classical.choice`, and `Quot.sound`. |
| `rg -n -i 'Rellich\|Hardy[-_ ]?Rellich\|HardyRellich' Formalizations/Lean/.lake/packages --glob '*.lean'` | 1, expected | No matching theorem in readable pinned package sources. |
| `rg -n '\b(sorry\|admit\|sorryAx)\b\|^[[:space:]]*(axiom\|unsafe\|opaque)[[:space:]]' Stage1_Instances/THM-M-1247/{Statement,Proof,ObligationTree}.lean` | 1, expected | No prohibited lexical match; this is defense in depth, not a transitive provenance audit. |
| `git diff --name-status 4d389eb4..HEAD -- Stage1_Instances/THM-M-1247 Docs/Stage1_Targets_rev-5.6.json skills/execute-stage1-rev56/SKILL.md` | 0 | Only the prior target blocker pair changed; semantic inputs, target manifest, and execution skill are unchanged. |
| `jq -c '.items[] | select(.id == "S56-M-1247-OBLIGATION_TREE" or .id == "S56-M-1247-PROOF") | {id,state,attempts,children}' Docs/Stage1_Execution_DAG_rev-5.6.json` | 0 | Predecessor remains `[_]`, attempts 1; proof remains `[ ]`, attempts 0, children empty. |
| `git ls-tree -r --name-only HEAD Stage1_Instances/THM-M-1247 | rg 'proof-recheck-.*\.json$' | wc -l` | 0 | `29`; repeated unresolved dispatch reports warrant the section 10.2 split. |
| `python3 -m json.tool Stage1_Instances/THM-M-1247/proof-recheck-2026-07-15-head-20808d65-slot43.json` plus the literal `jq -e` assertions recorded in the JSON companion | 0 | JSON parsed; identities, hashes, open state, changed paths, escalation, and deliberate self-test absence agree. |
| `git diff --check -- Stage1_Instances/THM-M-1247 .stage1-worker-selftest.json` | 0 | No tracked-diff whitespace diagnostics. |
| `git diff --no-index --check /dev/null FILE` for each new packet file | 1, expected | Each returns 1 only because the file is an addition; diagnostic output is empty. |
| `test ! -e .stage1-worker-selftest.json` | 0 | No false worker-completion packet exists. |

The narrow Lean replay was:

```bash
set -euo pipefail
ROOT="$PWD"
TARGET="$ROOT/Stage1_Instances/THM-M-1247"
LEAN_ROOT="$ROOT/Formalizations/Lean"
MATHLIB="$LEAN_ROOT/.lake/packages/mathlib"
TMP=$(mktemp -d /tmp/thm-m-1247-proof-head-20808d65-slot43.XXXXXX)
trap 'rm -rf "$TMP"' EXIT
cp "$TARGET"/{Statement,Proof,ObligationTree}.lean "$TMP/"
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
`@Pi.normedAddCommGroup` / `@Pi.normedSpace` instances, confirming both mapping
defects.

## Retry Condition

Do not dispatch `S56-M-1247-PROOF` unchanged again. Reopen
`S56-M-1247-STATEMENT` under an authorized assignment, use
`EuclideanSpace Real (Fin n)` and
`ContDiff Real ((top : ENat) : WithTop ENat)`, rerun the exact-expression and
mutation gates, publish a versioned obligation-registry/typed-graph delta with
downstream invalidations, and split weighted integration by parts, derivative
Hardy, normalization, core estimate, and transport into dependency-legal child
tasks before proof execution resumes.

## Status Boundary

This is current-base blocker and scheduler-escalation evidence under the owned
target path. It does not satisfy `S56-M-1247-PROOF`. The item remains `[ ]`;
there is no worker self-test, accepted receipt, audit completion, validation,
release, or theorem-completion claim.
