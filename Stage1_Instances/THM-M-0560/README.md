# THM-M-0560 rev-5.6 intake

This directory is the `planned` rev-5.6 dossier for Brown representability. The repository source
fixes the intended theorem family as representability of generalized cohomology theories, but it
does not specify reduced versus unreduced theories, the category of spaces, the precise Brown
axioms, or whether the root is degreewise representability or the stronger compatible spectrum
package. Intake preserves those distinctions rather than selecting a convenient categorical
representability tautology.

The provisional root vector is `[H1, M4, R3]`. The historical 1962 paper and its 1963 correction
are identified, but their exact theorem text, assumptions, page span, and correction impact have
not yet been inspected. No canonical Lean expression or terminal Lean proof is credited. In
particular, mathlib's general `RepresentableBy` API and the repository's representable-functor
wrapper characterize what representability means; they do not prove Brown's existence theorem.

The scope map, source-statement crosswalk, structured intake, and open task DAG define the work
that follows. Exact intake checks are recorded in `validation.md`. This node claims only a
self-tested planned intake pending master acceptance, not statement closure, audit completion, or
theorem completion.
