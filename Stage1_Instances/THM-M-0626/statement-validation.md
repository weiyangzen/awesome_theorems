# Statement validation

Item: `S56-M-0626-STATEMENT`

Base revision: `0f70149d61a952d44f907f4662a143372bcb4c44` (tree
`35328e4f56f47446a4e1dfdbe361a1b70a4b18a7`). Validation date: 2026-07-13
(`Asia/Shanghai`).

## Selected target

The catalog says that the continuous image of a connected set is connected. The exact target now
uses the inspected Stacks Project formulation: arbitrary topological spaces, a subset `s`,
mathlib's nonempty `IsConnected s`, global `Continuous f`, direct set image `f '' s`, and
`IsConnected (f '' s)`. Global continuity is not an added convenience here; it is the premise in
the selected source statement and in the intake's human canonical scope.

Pinned mathlib exposes the sharper `ContinuousOn f s` formulation. `Statement.lean` records that
as a credited alternate and checks the correct direction: assuming the local theorem yields the
global root through `Continuous.continuousOn`. It claims no converse. A separate iff expands both
connectedness predicates into nonemptiness plus `IsPreconnected`, fixing the empty-set convention.

The exact declaration is `Stage1Instances.THM_M_0626.ConnectedImageTarget`. Its explicit serialized
expression SHA-256 is `5c32b45abf131975cd4673ca095ca1a8e0122e4104bf616a4afab09a03289231`;
the environment fingerprint SHA-256 is
`aee8c1e19573413be5fb0ad0c854de55a1cfc41e45f473e37b2a886c9b587eac`.

## Statement boundary

The module has one direct import, `Mathlib.Topology.Connected.Basic`. Removing that import from a
temporary exact copy makes elaboration fail. This establishes deletion-minimality of the declared
import list, not an exhaustive claim about every possible alternative public module.

Five separately elaborated mutations are rejected by `#check_failure` identity probes and have
explicit expressions distinct from the root: removed connectedness, removed continuity, changed
domain, changed universal function scope to existential, and changed ordinary connectedness to the
empty-allowing `IsPreconnected` boundary. Kernel-checked fixtures also show that the empty set is
not `IsConnected`, while singleton sources and constant maps remain in scope.

The definitional expansion depends on no axioms. The local-to-global wrapper reports `propext`,
`Classical.choice`, and `Quot.sound`, inherited from the pinned topology API. The scoped source
scan finds no `sorry`, `admit`, custom axiom, opaque or unsafe declaration, or `sorryAx`.

## Commands and results

Commands ran from the worker-clone root unless a working directory is shown.

| Command | Exit | Exact result summary |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0626` | 0 | rank 1320, planned, legacy artifacts unaccepted, theorem incomplete |
| `git rev-parse HEAD` and `git rev-parse 'HEAD^{tree}'` | 0 | base identifiers above |
| pre-edit `git status --short --untracked-files=all` | 0 | only the automation-provided `Formalizations/Lean/.lake` was untracked |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | Lean 4.29.0 commit `98dc76e3...`; Lake `5.0.0-src+98dc76e` |
| pinned mathlib revision, tree, and status checks | 0 | revision `8a178386...`, tree `bdc39a31...`; package worktree clean |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0626/Statement.lean)` | 0 | target, two checked transports, five expected mutation rejections, three boundary fixtures, axiom results, and explicit expression elaborated; output SHA-256 `a376c599...bb7c` |
| `(cd Formalizations/Lean && python3 ../../Stage1_Instances/THM-M-0626/check_statement.py)` | 0 | expression and environment hashes agreed; five mutations killed; one-import deletion rejected; pinned dependencies agreed; output SHA-256 `5b7e9a9d...1133` |
| `python3 Stage1_Instances/THM-M-0626/check_statement_artifacts.py` | 0 | assignment, provisional state, declaration, fingerprints, hashes, mutation classes, dependency pin, false theorem completion, and worker packet agreed |
| `python3 -m json.tool` on the statement record, receipt, and worker packet | 0 | all finalized structured artifacts parsed |
| scoped invariant and prohibited-construct checks | 0 | item, target, hashes, imports, mutation set, dependency boundary, and false theorem completion agreed; no prohibited construct found |
| `git diff --check -- Stage1_Instances/THM-M-0626 .stage1-worker-selftest.json` plus checks of new files | 0 | no whitespace diagnostics |

The automation-provided `.lake` link to canonical pinned artifacts was used read-only. No update,
build, clone, fetch, or other dependency mutation was run.

## Status boundary

This is a worker-local exact statement proposal. It adds no root proof and does not change the
conservative `[H1, M3, R4]` vector. The intake predecessor remains provisional, and the independent
review of its source/convention map has not occurred. Source acceptance, anchor audit, obligation
tree, proof, trust closure, hermetic replay, independent verification, release, master acceptance,
and theorem completion all remain open.
