# THM-M-0332 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository label "spectral
mapping theorem" and gloss "the spectrum of the holomorphic functional calculus".

The intended classical shape is plausibly `spectrum (f(a)) = f '' spectrum(a)`, but the repository
source does not specify the ambient complex unital Banach algebra, the element, the open
neighborhood on which `f` is holomorphic, the construction denoted by `f(a)`, or the treatment of
nonunital algebras and empty spectra. Those choices are mathematically material, so intake does not
invent a canonical proposition.

A pinned Lean probe confirms the available spectrum API and two nearby, genuinely checked spectral
mapping families: continuous functional calculus and polynomial evaluation. Neither is credited as
the requested holomorphic-functional-calculus theorem. The root remains `[H1, M4, R4]`, and no proof
or theorem-completion state is accepted. Exact commands and results are recorded in `validation.md`.
