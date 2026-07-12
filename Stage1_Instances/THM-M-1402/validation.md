# Intake validation

Base revision: `028e2535b68678b8296e63e2cacb05ed9775a2d8`.

This validation covers target membership, dossier structure, JSON integrity, and a narrow pinned
Lean API probe. Because the repository record supplies no proposition, no canonical target,
expression hash, mutation result, source acceptance, or proof is claimed. The automation-provided
canonical `.lake` symlink and artifacts were used read-only; no dependency update, build, clone,
fetch, or `.lake` mutation was performed. The symlink is a scheduler-provided, out-of-scope
untracked automation input, so this is nonrelease worker evidence.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1402` | exit 0; rank 901, planned, legacy artifacts unaccepted, theorem_complete false |
| `(cd Formalizations/Lean && lake env lean --version)` | exit 0; Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, x86_64 Linux |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | exit 0; mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | exit 0; hashes `651c8acc...b1d2` and `321626c8...2d81`, respectively |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1402/IntakeProbe.lean)` | exit 0; eight pinned stream, product-topology, Pi-reindexing, and periodic-point API checks elaborated |
| `rg -n -i 'symbolic dynamics\|symbolic dynamical\|subshift\|shift space\|full shift\|one-sided shift\|two-sided shift' Formalizations/Lean/.lake/packages/mathlib/Mathlib/Dynamics -g '*.lean'` | exit 1 (expected no-match); no obvious symbolic/full-shift framework found in pinned `Mathlib/Dynamics` |

The final JSON checks, `python3 Stage1_Instances/THM-M-1402/check_intake.py`, prohibited-construct
scan, and scoped whitespace check all exited as recorded in `intake-receipt.json`. The Git diff
check sees no tracked diff error; because this new dossier is untracked, `check_intake.py`
independently checks its final newlines, line endings, trailing whitespace, artifact inventory, and
recorded SHA-256 values. Known downstream failures remain intentionally open:
source selection and independent review; selection of a truth-valued proposition and all domain,
structure, convention, hypothesis, and boundary decisions; canonical elaboration and mutation
tests; discovery and obligation freezes; anchor audit; proof; hermetic replay; independent
verification; and master acceptance. They prevent theorem completion but do not invalidate a
truthful `planned` intake.
