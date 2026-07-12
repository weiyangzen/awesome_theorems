# Statement validation

Base revision: `a8aba97a7ef2ff387e7814fe517e1b35524a04dc`.

This phase freezes the intake-selected natural, coprime-base target. The source catalog itself omits
the hypotheses and domain, so this is not a primary-source acceptance or `H0` claim. The Lean file
uses only the primitive natural congruence and prime-definition modules. In particular it does not
import the finite-field module containing the pinned proof candidate, and it claims no proof credit.

The automation-provided canonical `.lake` symlink is used read-only. It is a pre-existing untracked
worker input, making this nonrelease evidence; no update, build, clone, fetch, or dependency mutation
is performed.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0474` | exit 0; rank 938, planned, legacy artifacts unaccepted, theorem incomplete |
| `(cd Formalizations/Lean && lake env lean --version)` | exit 0; Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, x86_64 Linux |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | exit 0; mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0474/Statement.lean)` | exit 0; target and checked premise transport elaborate, four expected type rejections are emitted, explicit target and transport axioms are printed |
| `(cd Formalizations/Lean && python3 ../../Stage1_Instances/THM-M-0474/check_statement.py)` | exit 0; expression/file/output fingerprints emitted, all four mutations distinguished, both declared imports independently shown necessary |

The final JSON, dossier, Python, prohibited-construct, and scoped whitespace checks are recorded in
`statement-receipt.json`. The checked premise transport reports `propext`, `Classical.choice`, and
`Quot.sound`; this is a transparent foundation observation, not a completed trust audit.

Known downstream failures remain open: pinpoint primary-source and independent source review; formal
candidate and proof-body provenance/trust audit; discovery and obligation freezes; proof and checked
composition; readable reconstruction; hermetic replay; deterministic evidence bundle; independent
verification; and master acceptance. The integer, `ZMod`, and all-base forms remain uncredited.
