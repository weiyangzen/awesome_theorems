# THM-M-0400 intake dossier

This is the rev-5.6 `planned` intake for Schmidt's Subspace Theorem. The
authoritative structured record is `intake.json`. It freezes the intended
archimedean product-of-linear-forms variant, its quantifier order, exclusions,
and the boundary between source metadata and an exact theorem statement.

The historical declaration `Stage1.THMM0400.StatementShape` is discovery input
only. It abstracts the decisive inequality and mathematical hypotheses as
arbitrary propositions, so it is not the exact source theorem and receives no
rev-5.6 proof credit. The next phase must verify the primary-source theorem and
page, choose exact height and coefficient models, and elaborate those choices.

## Validation record

- Base revision: `a8d6489fd935cd71fa4499f2f3f5b051998203f4`.
- `python3 -m json.tool Stage1_Instances/THM-M-0400/intake.json`: passed.
- `python3 Docs/tools/check_stage1_standard.py`: passed (`1546` targets).
- `python3 scripts/stage1_target.py check`: passed (`1546` unique targets).
- `python3 scripts/stage1_target.py show THM-M-0400`: passed; rank 13,
  `L0`, `rework_required`, `planned`, theorem incomplete.
- `git diff --check -- Stage1_Instances/THM-M-0400`: passed.

No Lean proof or theorem-completion claim is made in this intake phase.
