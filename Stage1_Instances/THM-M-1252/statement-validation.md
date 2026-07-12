# Statement validation record

Item: `S56-M-1252-STATEMENT`  
Base revision: `a80ab2514294b0e85527fd5a7d419748401215b2`

## Frozen target

`Stage1Instances.THM_M_1252.DistributionSupportLocalizationTarget` freezes the localization
characterization identified by the intake: the complement of a distribution's support is its
largest open zero region, expressed as the union of every open set on which it vanishes. The
distribution is real-valued and defined on an arbitrary open subset of a finite-dimensional real
normed space. `ExpandedTarget` spells vanishing out as zero evaluation on every test function whose
topological support lies in that open set, and the checked iff validates this expansion.

This selection resolves the intake's formal encoding decisions but does not upgrade its incomplete
primary-source crosswalk to `H0`. The exact mathlib API independently matches the selected claim;
source-edition, theorem/page, and errata review remain downstream source debt.

## Commands and results

Lean commands ran from `Formalizations/Lean` against the existing pinned environment. No update,
fetch, build, or `.lake` mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-1252/Statement.lean` | 0 | canonical target, expanded iff, and three structural mutations elaborated; explicit target printed |
| `lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C .lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `sha256sum ../../Stage1_Instances/THM-M-1252/Statement.lean lean-toolchain lake-manifest.json` | 0 | `507071b9...b9da`, `651c8acc...b1d2`, `321626c8...2d81` |
| `rg -n '\\b(sorry|axiom|admit)\\b' ../../Stage1_Instances/THM-M-1252/Statement.lean` | 1 | no placeholders or new axioms found |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1252` | 0 | rank 431, planned, legacy artifacts unaccepted, theorem incomplete |

The mutations retain well-typed but rejected alternatives: closed rather than open zero regions,
support rather than its complement, and one existential zero region rather than the union of all
such regions. Degenerate inputs are deliberately not excluded. This is statement-only evidence
pending master acceptance; anchor audit, proof architecture, proof, validation, and release remain
open.
