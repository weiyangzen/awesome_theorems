# Statement validation record

The exact target is `Stage1.THM_M_1129.PoissonFormulaTarget` in `Statement.lean`. It uses the
fixed unit-disk form, so the scale factor is `t / (2*pi)` after the two-dimensional change of
variables. The statement distinguishes the singular display at positive time from the initial
conditions at zero.

From `Formalizations/Lean`, `lake env lean ../../Stage1_Instances/THM-M-1129/Statement.lean`
exited 0 under Lean 4.29.0 and mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95`.
The output printed the elaborated target and confirmed rejection of mutations removing positive
speed, changing dimension, changing binder scope, and including the zero-time boundary.

The source SHA-256 is `7f3427de436cf46a7162b2f1cded47f12dd348f6cea1c117788027a8d3bd70de`;
the complete elaboration-output SHA-256 is
`0cb797156a05d1c76475f474799fc7993b09556fa4254dbcf2f61bdb48298b69`.
The structured command record and dependency fingerprints are in `statement_receipt.json`.

This receipt is nonrelease worker evidence because the clone began with the automation-provided
untracked `.lake` symlink. It claims statement elaboration only, not proof closure, source `H0`, or
theorem completion.
