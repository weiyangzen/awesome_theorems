# THM-M-0751 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for `图灵度的上确界`, literally
"supremum of Turing degrees." The repository supplies only the gloss `图灵度的格结构` (the
lattice structure of Turing degrees), an attribution to many mathematicians, a twentieth-century
date, and an untrusted `已验证` label. It gives no formula, source, domains, binders, or proof.

The strongest historical lead is Kleene and Post's 1954 paper *The Upper Semi-Lattice of Degrees
of Recursive Unsolvability*. An immutable Encyclopedia of Mathematics revision likewise says that
the degrees form an upper semilattice. These leads make binary join the likely family: a disjoint
sum of two representatives should induce a least upper bound. They do not turn the catalog wording
into an exact proposition. In particular, a binary join, an arbitrary-family supremum, a complete
lattice, and a lattice with binary meets are materially different claims.

Pinned mathlib defines Turing reducibility, equivalence, the quotient `TuringDegree`, and its
partial order in `Mathlib.Computability.TuringDegree`. It provides no join, supremum, semilattice,
or lattice declaration. `IntakeProbe.lean` authenticates that adjacent interface only; it declares
no target theorem and earns no proof credit.

The provisional vector is `[H1, M4, R4]`: a published theorem family and primary bibliographic lead
are identified, but the exact primary statement, assumptions, definitions, errata, and independent
crosswalk remain open; no usable exact Lean artifact is located; and no readable reconstruction can
attach to an unfrozen root. All six downstream phases remain open. This self-tested worker proposal
claims neither accepted state, audit completion, theorem completion, nor master acceptance.
