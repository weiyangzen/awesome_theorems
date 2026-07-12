# THM-M-0357 rev-5.6 intake

This directory is the fail-closed `planned` intake for the repository label "wavelet
multiresolution analysis". The repository supplies only the gloss "the multiresolution framework
of wavelets", an attribution to Mallat and Meyer, and the year 1986. It does not identify one
theorem, a source edition, or its hypotheses.

The provisional scope is the classical multiresolution-analysis (MRA) framework on
`L^2(Real)`: a nested integer-indexed family of closed subspaces, compatible with dyadic dilation,
whose union is dense and whose intersection is trivial, together with the scaling-function and
wavelet-basis conclusions when the source supplies their additional hypotheses. Those conclusions
are not interchangeable, so intake deliberately leaves the canonical claim open.

The root remains `[H3, M4, R4]`. A pinned Lean probe checks only nearby `Lp`, domain action,
closed-subspace, and orthonormal-basis APIs; it is encoding evidence, not an MRA statement or proof.
Exact commands and results are in `validation.md`.
