# Statement gate blocker

Item: `S56-M-0007-STATEMENT`  
Theorem: `THM-M-0007`  
Verdict: blocked; no exact canonical Lean target is claimed.

## First failed gate

The intake identifies Weibel, *An Introduction to Homological Algebra*, Theorem 5.8.3 only as an
uninspected theorem-family anchor. The owned source crosswalk explicitly leaves the printed
definitions, exact hypotheses, page convention, naturality, and convergence conclusion open. The
repository contains no scan or transcription of the cited pages. Consequently there is not enough
source evidence in this clone to choose, without inventing mathematics, among an objectwise versus
functorial target, weak versus strong convergence, the associated filtration and its boundedness,
or the precise placement of enough-injectives and acyclicity assumptions.

There is also a concrete encoding gap in the pinned dependency. Mathlib provides the typed carrier
`E₂CohomologicalSpectralSequenceNat E`, its pages and differentials, and the required right-derived
functors, but a repository-wide search of pinned `Mathlib/Algebra/Homology` and
`Mathlib/CategoryTheory` finds no abutment, `ConvergesTo`, or `StronglyConvergesTo` interface. The
legacy `GrothendieckSpectralSequenceBoundary` cannot fill that gap: its `spectralSequence` is an
arbitrary `Type`, while naturality and convergence are bare `Prop` fields. Reusing it would violate
the intake's explicit exclusion of opaque proxy fields and would broaden the exact-statement claim.

Therefore ordered binders, exact conclusion, definition-level source crosswalk, expression
fingerprint, checked transports, and meaningful statement mutations cannot truthfully be frozen.
`StatementInfrastructure.lean` checks only the noncontroversial typed substrate and deliberately
declares no canonical theorem, axiom, placeholder, or proxy convergence predicate.

## Environment fingerprint

- Repository base revision: `526d1cb643888ebd37396204101ee24420b8bd95`.
- Validation date: 2026-07-12.
- Lean toolchain: `leanprover/lean4:v4.29.0`; Lean `4.29.0`, commit
  `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- mathlib Lake pin: `8a178386ffc0f5fef0b77738bb5449d50efeea95`.

## Validation evidence

Lean commands ran from `Formalizations/Lean` against the existing pinned `.lake` symlink. No
update, build, fetch, or clone command was used.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-0007/StatementInfrastructure.lean` | 0 | all four `#check` commands printed typed declarations |
| `lake env lean AwesomeTheorems/Stage1/S1_M_094.lean` | 0 | legacy discovery artifact elaborated; not exact-statement credit |
| `lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C .lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `sha256sum lean-toolchain lake-manifest.json lakefile.lean` | 0 | respectively `651c8a...81d2`, `321626...2d81`, and `43259b...4b4dcda` |
| `rg -l "StronglyConverges\|stronglyConverges\|ConvergesTo\|convergesTo\|abutment\|Abutment" Formalizations/Lean/.lake/packages/mathlib/Mathlib/Algebra/Homology Formalizations/Lean/.lake/packages/mathlib/Mathlib/CategoryTheory -g '*.lean' \| wc -l` | 0 | `0` matching files |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546 |
| `python3 scripts/stage1_target.py show THM-M-0007` | 0 | rank 94, planned, L0/rework-required, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-0007/{instance,task-dag}.json` (expanded to one command per file) | 0 | both inherited intake JSON files remain valid |
| `git diff --check -- Stage1_Instances/THM-M-0007` | 0 | no output |

## Retry condition

The authoritative lane must provide and approve a page-level transcription of the selected primary
source, including its definitions of acyclicity and convergence, and select or implement a typed
Lean convergence/abutment interface. The statement phase can then encode the exact claim, verify
its complete expansion, and run source-directed hypothesis, domain, binder-scope, and boundary
mutations.

Until then the statement gate remains at `M4`; statement acceptance and theorem completion are
false. Because the assigned phase cannot be self-tested to completion, no
`.stage1-worker-selftest.json` is emitted.
