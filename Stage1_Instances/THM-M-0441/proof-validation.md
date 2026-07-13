# THM-M-0441 proof-phase attempt

Item: `S56-M-0441-PROOF`  
Date: `2026-07-14` (`Asia/Shanghai`)  
Base revision: `c45f3c7090cb4adf616d45e5414985f956e807b2`

## Verdict

`blocked`, with partial machine progress. `Proof.lean` adds eleven genuine,
placeholder-free proof bodies. They establish the elementary algebraic-part
laws, finite bounded-height rational slices, the statement's explicit
finiteness conjunct, and the empty-transcendental-part counting branch with
the required positive constant `c = 1`.

These results advance `M0441-S-HEIGHT`, `M0441-S-ALG`, `M0441-B-ZERO`,
`M0441-B-POS`, and `M0441-L-COUNT`, but do not close any frozen obligation in
full. In particular, they do not inhabit the four fields consumed by
`ObligationTree.engine_compose`. The exact general root remains `M3`,
`root_closed=false`, and `theorem_complete=false`.

The first missing deep package is `M0441-C-PARAM`. The pinned closure contains
no uniform o-minimal `C^r` parameterization theorem for the canonical
definability encoding. `M0441-L-DET`, `M0441-C-BLOCKS`, and
`M0441-B-INDUCT` also remain open. The prerequisite immutable audit found no
compatible external terminal body. Treating `CountingEngine.deriveCounting`
as proof provenance, assuming one of these packages, or substituting one of
the closed special cases would violate the exact-target and placeholder gates.

Because the assigned proof deliverable is incomplete,
`.stage1-worker-selftest.json` is deliberately absent.

## Narrow validation evidence

All commands ran in this worker clone using the existing canonical pinned Lake
artifacts. No `lake update`, `lake build`, dependency clone/fetch, or `.lake`
mutation was performed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | rev-5.6 standard, 15 assurance groups, and 1546 uniform-L0 Lean 4 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-0441` | 0 | Rank 87; planned; hard-mathlib-anchor lane; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0441/check_obligation_tree.py` | 0 | `PASS THM-M-0441 obligation freeze: 21 obligations, 18 proof edges; root open`. |
| Concatenate `Statement.lean`, `ObligationTree.lean`, and `Proof.lean` after removing the two local import lines, then pipe to `cd Formalizations/Lean && LEAN_NUM_THREADS=1 lake env lean /dev/stdin` | 0 | The exact target, conditional composition, and all eleven new declarations elaborated. Every `#print axioms` report was a subset of `propext`, `Classical.choice`, and `Quot.sound`; no `sorryAx` occurred. |
| `rg -n '\b(sorry\|admit\|sorryAx\|axiom\|unsafe)\b' Stage1_Instances/THM-M-0441 --glob '*.lean'` | 1 | Expected no-match exit; no prohibited token occurs in the owned Lean sources. |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95`. |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release. |
| `sha256sum Stage1_Instances/THM-M-0441/{Statement.lean,obligation-registry.json,typed-graphs.json,Proof.lean}` | 0 | `a0a7c75b...db563b`, `228f8e7c...ba50f`, `b6bf264e...aeee`, `466e3466...f4f62`. |
| `python3 -m json.tool Stage1_Instances/THM-M-0441/proof-blocker.json >/dev/null` | 0 | Structured blocker record parsed. |
| `git diff --check -- Stage1_Instances/THM-M-0441 .stage1-worker-selftest.json` | 0 | No whitespace errors. |
| `test ! -e .stage1-worker-selftest.json` | 0 | The incomplete proof phase emitted no worker completion manifest. |

The elaboration recipe uses only a pipeline and no repository build output:

```bash
set -o pipefail
{
  sed '/^import Statement$/d' Stage1_Instances/THM-M-0441/Statement.lean
  sed '/^import Statement$/d' Stage1_Instances/THM-M-0441/ObligationTree.lean
  sed '/^import ObligationTree$/d' Stage1_Instances/THM-M-0441/Proof.lean
} | (cd Formalizations/Lean && LEAN_NUM_THREADS=1 lake env lean /dev/stdin)
```

The automation-provided untracked `Formalizations/Lean/.lake` symlink points to
the canonical pinned artifacts and was not modified. This is scoped nonrelease
blocker evidence, not release validation.

## Reopen condition

Resume after implementing the frozen parameterization, determinant, block, and
dimension-induction packages without placeholders, or after locating an
immutable compatible Lean 4 Pila-Wilkie proof whose exact type, terminal body,
dependencies, axioms, license, and provenance can all be validated in the
pinned environment.
