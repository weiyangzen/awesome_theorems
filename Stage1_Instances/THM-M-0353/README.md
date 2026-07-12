# THM-M-0353 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository claim that the
Hermite functions form a complete orthonormal basis of `L^2`. The claim identifies a classical
theorem family, but the repository source does not specify the scalar field, underlying measure,
normalization of the Hermite polynomials/functions, or a primary theorem citation. Those choices
change the literal functions and constants even though standard versions are equivalent.

The statement phase now freezes the standard complex Lebesgue `L^2` formulation using mathlib's
probabilists' Hermite polynomial and elaborates it in `Statement.lean`. This does not prove the
integrability, orthonormality, or completeness obligations. The root therefore remains open, and
no theorem-completion state is claimed. Intake commands are recorded in `validation.md`; exact
statement commands and the statement-only boundary are recorded in `statement-validation.md`.
