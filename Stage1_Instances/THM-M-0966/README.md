# THM-M-0966 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the Kruskal-Katona theorem. The
repository supplies the eponym, the attribution Kruskal/Katona, the year 1963, and only the gloss
`阴影的最小大小` ("minimum size of the shadow"). Its `已验证` label is untrusted metadata and
provides no statement, source, or proof credit.

The gloss identifies a classical theorem family but does not select one exact proposition. In
particular, it does not say whether the root is the one-step colex-minimizer comparison, the
numerical binomial/cascade formulation, an iterated-shadow theorem, the Lovasz binomial-threshold
form, or an equality characterization. It also leaves the ambient finite set, uniformity,
cardinality convention, lower-shadow definition, parameter ranges, and boundary cases unstated.

Kruskal's 1963 chapter *The Number of Simplices in a Complex* and Katona's *A Theorem of Finite
Sets* are recorded as bibliographic leads. Crossref metadata was inspected, but neither complete
original text, exact theorem passage, assumption list, proof boundary, correction record, nor an
independent source review was admitted. The source crosswalk therefore remains `H1`, not `H0`.

Pinned mathlib directly contains `Finset.kruskal_katona` in
`Mathlib.Combinatorics.SetFamily.KruskalKatona`. `IntakeProbe.lean` checks its exact displayed type,
nearby formulations, vocabulary, and reported axioms. The basic declaration compares the lower
shadow of an `r`-uniform family with that of a supplied colex initial segment of no greater
cardinality. It does not itself state existence of that segment, the full numerical cascade bound,
or equality classification. It is a credible formal candidate, not accepted proof credit for the
still-unselected catalog root.

The provisional vector is `[H1, M3, R4]`. Every downstream task remains open. No canonical
statement, expression fingerprint, H0, M0, R0, accepted state, audit completion, theorem
completion, or master acceptance is claimed.
