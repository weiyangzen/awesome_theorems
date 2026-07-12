# THM-M-0356 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository topic "Daubechies
wavelets". The supplied claim is only "compactly supported orthogonal wavelet". It does not say
whether the target is one example, a family indexed by filter length or vanishing moments, or the
stronger construction with prescribed regularity. It also leaves normalization, translation and
dilation conventions, scalar field, and the formal meanings of compact support and completeness
open.

The human scope is therefore provisional. A narrow pinned Lean probe confirms that mathlib exposes
compact support, `L^p`, and orthonormal-basis interfaces that a later exact statement may use. It
does not define a Daubechies filter or establish the construction. The provisional root vector is
`[H3, M4, R4]`.

All downstream tasks remain open. This intake claims neither an exact statement nor a proof, audit
completion, or theorem completion.
