# THM-M-0347 rev-5.6 dossier

This directory is the fail-closed `planned` intake dossier for Fejer's theorem in periodic Fourier
analysis. The repository gloss says only that the Cesaro means for a continuous function converge.
The standard theorem concerns the first-order Cesaro means of the Fourier partial sums of a
continuous periodic function and gives uniform convergence back to that function.

The statement phase selects arbitrary positive real period, complex-valued continuous maps,
mathlib's normalized Haar Fourier coefficients, symmetric frequencies `-n, ..., n`, and the mean
of `S_0, ..., S_n`. The conclusion is convergence in the continuous-map topology, the uniform
conclusion on the compact circle. `Statement.lean` elaborates this exact target with the single
direct import `Mathlib.Analysis.Fourier.AddCircle`, checks a direct expansion, distinguishes four
structural mutations, and proves the two index-zero boundary identities.

The proof phase now vendors an exact immutable ATLAS Fejer development and
checks adapters from both frozen definitions to its symmetric Fourier sums and
`n + 1` Cesaro convention. The premise-free exact root declaration elaborates
at trust zero with only `propext`, `Classical.choice`, and `Quot.sound` in its
axiom closure. This is a provisional `M0-P` candidate, not accepted M0.

The accepted vector remains `H1/M3/R4`. ATLAS license/rider compatibility,
frozen internal composition review, E0 validation, independent verification,
release, and master acceptance remain open; no theorem-completion claim is
made. Exact proof provenance and commands are in `proof-validation.md` and
`proof-receipt.json`. The earlier negative proof attempt is retained as
superseded historical evidence.
