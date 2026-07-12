# THM-M-0345 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for Hardy's uncertainty principle. The
repository source identifies the theorem and gives only the gloss "limits on the decay of a
function and its Fourier transform". It does not state the decay bounds, Fourier normalization,
critical constant, dimension, regularity assumptions, or equality conclusion.

Several standard formulations are close but not interchangeable: a one-dimensional pointwise
Gaussian-decay theorem, an `L2`-weighted version, higher-dimensional variants, and versions with
different Fourier kernels have different constants and hypotheses. Choosing one from the gloss
would substitute an unstated proposition. The intake therefore freezes that ambiguity and the
scope boundary rather than pretending to freeze an exact theorem.

The root remains `[H3, M4, R4]`. A pinned Lean probe confirms that the Fourier-transform and
Gaussian APIs needed for a future encoding are available, including mathlib's checked transform
formula for a Gaussian. That formula is infrastructure, not Hardy's uncertainty principle and
receives no proof credit. Exact commands and results are recorded in `validation.md`.
