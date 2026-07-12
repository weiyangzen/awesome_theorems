# THM-M-0353 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository claim that the
Hermite functions form a complete orthonormal basis of `L^2`. The claim identifies a classical
theorem family, but the repository source does not specify the scalar field, underlying measure,
normalization of the Hermite polynomials/functions, or a primary theorem citation. Those choices
change the literal functions and constants even though standard versions are equivalent.

The intake therefore freezes the intended theorem family and its exclusion boundary, while leaving
the exact source statement and canonical Lean expression to the statement phase. The root remains
`[H1, M4, R4]`. A pinned Lean probe confirms that mathlib provides probabilists' Hermite
polynomials, their Gaussian derivative identity, `L^p` spaces, and the abstract `HilbertBasis`
interface. It does not define the required normalized Hermite functions or prove their
orthonormality/completeness. Exact commands and results are recorded in `validation.md`.

