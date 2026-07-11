# Source-statement crosswalk

| Claim component | Human source anchor | Intended Lean surface | Intake assessment |
|---|---|---|---|
| Product homology and the tensor/Tor short exact sequence | Allen Hatcher, *Algebraic Topology* (Cambridge University Press, 2002), Section 3.B, "The Kunneth Formula," Theorem 3B.6 | singular homology of `X × Y`, graded tensor sums, `Tor₁`, short exactness | Primary textbook theorem located, but edition hash, exact page verification, hypotheses, and errata review are not accepted: `H1` |
| Algebraic chain-complex theorem | Hatcher, Section 3.B, algebraic Kunneth theorem preceding the topological application | homological complexes, tensor product, homology, exact sequence | Candidate source boundary; exact theorem numbering and premise-to-node mapping remain open |
| Passage from chains on a product to tensor chains | Eilenberg-Zilber comparison used in the topological Kunneth proof | chain maps/homotopy equivalence between singular chains of the product and a tensor construction | Root-critical bridge; no Lean candidate or checked transport is credited |
| Field-coefficient formula | Corollary obtained by vanishing of `Tor` over a field | direct-sum isomorphism of graded homology | Strict special case only; explicitly not the canonical PID target |
| Naturality and splitting | Naturality is part of the theorem; the short exact sequence splits under the standard hypotheses, but not naturally in general | natural transformations/commuting squares; optional noncanonical splitting data | Exact source wording and Lean representation remain open |

The repository's legacy description, "computation of the homology groups of product spaces," does
not uniquely determine coefficients, finiteness/freeness assumptions, reduced versus unreduced
homology, grading conventions, or whether the conclusion is an isomorphism or a short exact
sequence. This intake resolves that ambiguity provisionally in favor of the standard PID short
exact sequence, because it retains both tensor and Tor information. Master acceptance of the intake
does not make this a checked Lean statement.

Discovery link (not an immutable evidence receipt):

- Hatcher's official book page: <https://pi.math.cornell.edu/~hatcher/AT/ATpage.html>

Required follow-up: archive and hash the cited edition, verify theorem/page and errata, map every
hypothesis and conclusion component, independently review the crosswalk, inspect pinned mathlib and
external Lean 4 candidates, and elaborate the exact target before assigning any machine credit.
