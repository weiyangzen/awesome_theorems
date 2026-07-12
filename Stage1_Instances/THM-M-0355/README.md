# THM-M-0355 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the Meyer wavelet construction. The
repository source supplies only the gloss "construction of smooth wavelets", an attribution to
Yves Meyer, and the year 1985. It does not state which Meyer construction, Fourier convention,
regularity class, support bounds, scalar field, normalization, or basis conclusion is intended.

The likely mathematical family concerns a smooth frequency-window construction whose dyadic
dilates and integer translates form an orthonormal basis of `L^2(R)`. That description is recorded
only as a provisional scope locator, not as the canonical theorem. A narrow pinned Lean probe
confirms that mathlib exposes Schwartz maps, Fourier transforms on Schwartz maps and `L^2`, and
Hilbert/orthonormal basis interfaces. It neither defines a Meyer wavelet nor proves its existence.

The root remains `[H3, M4, R4]`. All statement, source-audit, obligation, proof, validation, and
release work remains open; no exact theorem or completion state is claimed.
