# Statement validation record

Item: `S56-M-0786-STATEMENT`  
Base revision: `5314165df54baa70993fddf08cc142a9739a74e0`

## Frozen target

`Stage1Instances.THM_M_0786.BorelDeterminacyTarget` formalizes the intake-selected claim: arbitrary
Borel payoff sets in Baire space, natural-number moves, alternating perfect information, and the
disjunction of a strategy forcing payoff membership for Player I or nonmembership for Player II.
Strategies are total functions on finite chronological histories; compatibility consults Player I
at even lengths and Player II at odd lengths. This neither restricts the payoff to an easier Borel
subclass nor assumes determinacy.

The only direct import is `Mathlib.MeasureTheory.Constructions.Pi`; its removal was tested and made
elaboration fail. `target_iff_expanded` kernel-checks the definitions against a direct binder-level
expression. This is statement identity, not proof credit. Fidelity to an independently inspected
edition of Martin's paper remains H1 debt for the source/anchor phase.

## Commands and results

Commands ran on 2026-07-12 in this worker clone. Lean reused the existing pinned `.lake` artifacts;
no update, build, clone, or fetch was performed.

| Command | Exit | Result |
|---|---:|---|
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0786/Statement.lean)` | 0 | target, expansion transport, four mutations, two Borel boundary lemmas, and explicit expression elaborated |
| `(cd Formalizations/Lean && python3 ../../Stage1_Instances/THM-M-0786/check_statement.py)` | 0 | expression SHA-256 `4cca4f76...ef97a`; four mutations distinguished; file SHA-256 `fc3d76c6...16738` |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `sha256sum Statement.lean lean-toolchain lake-manifest.json` (respective paths) | 0 | `fc3d76c6...16738`, `651c8acc...5b1d2`, `321626c8...2d81` |
| sole-import removal trial using a temporary `/tmp` file | 0 as test harness | removal caused Lean elaboration failure |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets valid |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0786` | 0 | rank 791, planned, theorem completion false |
| `git diff --check -- Stage1_Instances/THM-M-0786 .stage1-worker-selftest.json` | 0 | no whitespace errors |

## Status boundary

The validator distinguishes removal of Borelness, a changed move domain, reversal of move parity,
and corruption of Player II's complement payoff. Empty and universal payoff sets remain included.
This statement phase is self-tested pending master acceptance. No Borel-determinacy proof, source
acceptance, anchor audit, audit completion, or theorem completion is claimed.
