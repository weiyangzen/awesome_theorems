# Statement validation record

Item: `S56-M-0329-STATEMENT`  
Base revision: `8014740e5a37eff82745f6fd2bc69f0ee45e67c9`

## Frozen target

`Stage1Instances.THM_M_0329.LaxMilgramTarget` states the standard variational form over an arbitrary
real Hilbert space: every continuous coercive bilinear form `B` and continuous functional `F` have
a unique solution `u` with `B u v = F v` for all `v`. The unknown is fixed in the first argument.
The exact pinned `IsCoercive` definition supplies `C > 0` and
`C * norm u * norm u <= B u u`; symmetry is not assumed.

The sole direct import is `Mathlib.Analysis.InnerProductSpace.Dual`, which provides the structures,
coercivity predicate, and Riesz equivalence but does not import the mathlib Lax-Milgram proof.
`target_iff_rieszRepresentativeShape` kernel-checks the transport between an arbitrary functional
and its Riesz representative without using Lax-Milgram.

## Commands and results

Commands ran in this worker clone against the existing pinned Lake environment. No dependency
update, build, fetch, or clone was run.

| Command | Exit | Result |
|---|---:|---|
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0329/Statement.lean` | 0 | canonical target, checked Riesz transport, and four structural mutations elaborated; explicit target printed |
| `cd Formalizations/Lean && python3 ../../Stage1_Instances/THM-M-0329/check_statement.py` | 0 | expression SHA-256 `1f7b5e8d8098022646a019e1953472658efcd08d8b1af081a6bc6295a1731b93`; all four mutations distinguished |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `sha256sum Stage1_Instances/THM-M-0329/Statement.lean Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | `1aa927...d5e6`, `651c8a...b1d2`, and `321626...2d81` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets valid |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0329` | 0 | rank 822, planned, legacy artifacts unaccepted, theorem incomplete |
| `rg -n '\\b(sorry\|admit)\\b\|^[[:space:]]*axiom\\b' Stage1_Instances/THM-M-0329 -g '*.lean'` | 1 (expected) | no prohibited placeholder or axiom found |
| `git diff --check -- Stage1_Instances/THM-M-0329 .stage1-worker-selftest.json` | 0 | no whitespace errors |

The mutations remove coercivity, specialize the domain to `Real`, move coercivity under the unique
witness, and exclude the zero functional. They elaborate to distinct explicit expressions and
cannot substitute for the canonical target. The zero space and zero datum remain in scope.

## Status boundary

This is self-tested statement evidence pending master acceptance. It proves no Lax-Milgram theorem
and claims no H0, M0, audit completion, theorem completion, or dependent-phase completion. The
primary-source pinpoint and formal candidate provenance remain open for the anchor-audit phase.
