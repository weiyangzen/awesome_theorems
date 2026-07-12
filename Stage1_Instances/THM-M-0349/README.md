# THM-M-0349 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the conjugate function theorem. The
repository gloss identifies the classical Marcel Riesz result that the periodic conjugate-function
operator is bounded on `L^p` for `1 < p < infinity`, but it does not fix the underlying circle
normalization, the definition of the operator, scalar field, or an exact source passage.

The statement phase now freezes the classical strong-type formulation on the period-one additive
circle: complex `L^p` equivalence classes, Haar measure, multiplier `-i sign(n)`, zero constant mode,
and a nonnegative bound depending on `p`. `Statement.lean` elaborates this exact proposition from
the single direct import `Mathlib.Analysis.Fourier.AddCircle`; four structural mutations are
separately elaborated and fingerprint-distinguished. The provisional root vector remains
`[H3, M4, R4]` because statement elaboration is not a proof.

The original repository gloss still lacks a pinpoint source passage and independent review, so the
Fourier-multiplier conventions remain a provisional statement proposal until master acceptance.
No proof, audit completion, or theorem completion is claimed.
