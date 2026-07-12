# Exact-statement gate: blocked

Item: `S56-M-0535-STATEMENT`  
Theorem: `THM-M-0535`  
Verdict: blocked; no canonical Lean target is claimed.

## First failed gate

The repository source record says only "the excision property of relative homology groups." It
does not identify a source theorem or freeze the proposition-changing choices required by section
5.1 of the rev-5.6 standard: singular versus another homology theory, coefficients, reduced versus
unreduced conventions, grading, the representation of a pair, the induced map, or the precise
excision hypothesis. The intake's Hatcher Proposition 2.21 and Eilenberg-Steenrod references are
explicitly discovery candidates whose exact editions, pages, definitions, assumptions, and errata
have not been inspected or independently approved. Choosing one of their inequivalent formulations
here would invent the missing source decision.

There is also no pinned formal substrate that removes this ambiguity. A scoped search of pinned
mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` found absolute singular chain and
homology functors in `Mathlib.AlgebraicTopology.SingularHomology.Basic`, but no relative singular
homology construction or excision declaration. Consequently the required map
`H_n(X \ Z, A \ Z) -> H_n(X, A)` cannot be named without first designing and validating a relative
chain-complex API. Replacing it by absolute homology, an abstract assumed functor on pairs, or an
assumed isomorphism would broaden or substitute the theorem and is forbidden.

Therefore ordered binders, the exact conclusion, credited alternate transports, an elaborated
expression fingerprint, and the required removed-hypothesis/domain/binder/boundary mutation tests
cannot truthfully be frozen. Machine debt remains `M4`; statement acceptance and theorem
completion are false.

## Lean boundary checked

`StatementInfrastructure.lean` uses the sole direct import
`Mathlib.AlgebraicTopology.SingularHomology.Basic`. It elaborates the pinned absolute
`singularChainComplexFunctor`, `singularHomologyFunctor`, and the conventional ambient-set condition
`closure Z subset interior A`. The last definition is only a topology substrate check, not a
canonical excision statement and not proof evidence.

All commands ran in this worker clone. Lean ran from `Formalizations/Lean` against the existing
canonical `.lake` artifacts. No update, build, clone, or fetch command was used.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0535` | 0 | rank 592, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `lake env lean ../../Stage1_Instances/THM-M-0535/StatementInfrastructure.lean` | 0 | absolute singular-chain/homology functors, conventional closure/interior condition, and their types elaborated |
| `lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C .lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `rg -n -i 'excision|relative.*homology|homology.*relative|RelativeHomology' .lake/packages/mathlib/Mathlib` | 0 | only unrelated prose plus absolute singular-homology files; no relative-homology/excision declaration located (scoped search, not an exhaustive absence proof) |
| `sha256sum lean-toolchain lake-manifest.json` | 0 | `651c8acc...b1d2` and `321626c8...2d81` |
| `git diff --check -- Stage1_Instances/THM-M-0535` | 0 | no whitespace errors |

Base revision: `7ebc835c8cb3bb8d31a59476f3e8815026f161d0`. Validation date: 2026-07-12.

## Retry condition

The authoritative lane must approve an immutable primary or standard-source proposition with all
coefficients, conventions, hypotheses, map, grading, and boundary cases fixed. The statement phase
must then either construct the missing relative singular-homology definitions and induced pair map
with minimal pinned imports, or pin an exact compatible Lean 4 implementation, before elaborating
and mutation-testing the canonical target.

Because the assigned statement phase did not pass its completion gate, no
`.stage1-worker-selftest.json` is emitted.
