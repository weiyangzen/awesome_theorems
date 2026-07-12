# Scope map

## Received claim

The repository supplies only:

- title: Artin-Wedderburn theorem;
- attribution: Emil Artin / Joseph Wedderburn;
- year: 1927;
- gloss: classification of central simple algebras;
- untrusted status: verified.

This identifies a theorem family, not a proposition. In particular, `central simple algebra` may
encode finite-dimensionality as part of the object, as mathlib's `CSA K` does, while other sources
state an Artinian or finite-dimensional hypothesis separately.

## Candidate classical boundary

A source-authorized root could assert that a finite-dimensional central simple algebra over a
field is isomorphic as an algebra to a full matrix algebra over a finite-dimensional division
algebra. Before that can become canonical, the statement phase must decide whether the division
algebra is required to be central over the base field and whether uniqueness of its isomorphism
class and the matrix degree belongs to the theorem. This candidate is recorded only to make the
ambiguity executable; it is not the frozen root.

## Pinned formal candidates

| Candidate | What it supplies | Intake boundary |
|---|---|---|
| `CSA K` in `Mathlib.Algebra.BrauerGroup.Defs` | A finite-dimensional central simple `K`-algebra carrier | Domain candidate only; choosing this bundled encoding requires a source decision |
| `IsSimpleRing.exists_algEquiv_matrix_divisionRing` | Matrix-algebra normal form for a simple Artinian algebra | Does not by itself select the finite central-simple source formulation |
| `IsSimpleRing.exists_algEquiv_matrix_divisionRing_finite` | Also makes the resulting division algebra finite over the base | The conclusion has `DivisionRing D`, `Algebra K D`, and `Module.Finite K D`; explicit centrality and uniqueness are not in its visible type |
| foreign `csa_wedderburn_artin_finite` | Applies the finite theorem to `A : CSA K` after deriving Artinianity | Discovery input owned by the legacy THM-M-0424 surface; no status or proof credit is transferred |

## Decisions required at the statement gate

1. Pin an exact primary or accepted modern source assertion, edition, theorem/page, definitions,
   assumptions, and correction/errata status.
2. Fix the base as a field and decide characteristic assumptions, if any.
3. Fix whether the input is a bundled `CSA K`, an algebra with explicit central/simple/finite
   hypotheses, or a simple Artinian algebra.
4. Fix universe levels, typeclass order, algebra versus ring equivalence, positive matrix size, and
   the precise division-algebra output.
5. Decide existence only versus uniqueness up to isomorphism, and forward theorem versus an iff.
6. Resolve whether output centrality over the base is explicit or obtained by a checked consequence.
7. Freeze zero-ring, nontriviality, dimension-zero, `n = 1`, split-algebra, and algebraically closed
   field behavior.
8. Elaborate the selected expression, hash it and its environment, check every alternate transport,
   and mutation-test removed hypotheses, domain, binder scope, and boundary cases.

## Explicit exclusions

- The finite-product decomposition for an arbitrary semisimple ring owned by `THM-M-0027`.
- Brauer equivalence, the Brauer group law, or arithmetic/cohomological classification owned by
  `THM-M-0037` or `THM-M-0424`.
- Wedderburn's little theorem for finite division rings.
- An algebraically closed-field split specialization used as the unrestricted root.
- A simple-Artinian theorem used as the central-simple root without a checked source transport.
- Existence silently strengthened by uniqueness or weakened by dropping centrality, finiteness, or
  the source's other premises.
- A structure or hypothesis that assumes the desired matrix decomposition.
- The catalogue `已验证` label, theorem-name match, foreign wrapper, or intake probe used as proof
  credit.

No canonical Lean expression, ordered binders, hypotheses, conclusion, alternate encoding, or
degenerate-case exclusion is frozen by this intake.
