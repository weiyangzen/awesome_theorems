# THM-M-0962 rev-5.6 dossier

This directory is the fail-closed `planned` intake dossier for the catalog entry named the
Frankl-Wilson theorem and glossed only as "an upper bound for an intersecting family." The catalog
does not state any parameters, hypotheses, formula, or source citation.

The authors and year strongly identify P. Frankl and R. M. Wilson's 1981 paper *Intersection
theorems with geometric consequences*. The publisher abstract describes a modular intersection
bound for a uniform finite-set family over a prime modulus. The article body is closed-access in
the source discovery performed here, so its exact theorem, definitions, qualifications, proof,
corrections, and errata were not inspected. In particular, intake does not choose a prime-power
generalization, an allowed-residue occurrence convention, or an ordinary pairwise-nonempty
intersection theorem.

Pinned mathlib contains useful statement vocabulary, including `Set.IsIntersectingOf`, `Set.Sized`,
`Nat.ModEq`, finite uniform slices, and binomial coefficients. A bounded name/content search found
no Frankl-Wilson theorem declaration. The Lean probe checks only those interfaces; it introduces no
target declaration or proof.

Accordingly, the canonical mathematical statement and Lean target remain null. The proposed intake
vector is `[H1, M3, R4]`, and all six downstream tasks remain open. No exact statement, accepted
proof state, audit completion, theorem completion, or master acceptance is claimed.
