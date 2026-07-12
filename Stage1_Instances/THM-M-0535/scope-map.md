# Scope map

## Included theorem family

- Relative singular homology of a pair of subspaces `A subset X`.
- A subspace `Z subset A` satisfying the exact neighborhood condition selected from the source,
  conventionally `closure Z subset interior A` (closures and interiors taken in `X`).
- The inclusion of pairs `(X \ Z, A \ Z) -> (X, A)` and its induced map on relative homology.
- An isomorphism in every homological degree, over the selected coefficient ring.

## Decisions required at statement freeze

The statement phase must select and inspect one exact source theorem and freeze: the ambient
topological hypotheses; whether `A` and `Z` are literal subsets or subspaces; where closure and
interior are computed; whether the premise is `closure Z subset interior A` or an equivalent
cover-interior condition; singular versus another homology theory; reduced or unreduced homology;
the coefficient ring/module; degree indexing; and the exact induced inclusion map. It must also
settle empty `Z`, `Z = A`, empty complements, degree zero, disconnected spaces, and universe/size
assumptions.

The pair map must be well-defined: the selected assumptions must imply `A \ Z subset X \ Z`, and
its two inclusion components must commute. Any equivalence between a source's cover formulation
and the closure/interior formulation requires an explicit checked transport rather than prose.

## Explicit exclusions

- Excision for measures, ideals, sheaves, triangulated categories, or generalized homology theories
  as a substitute for the selected singular-homology theorem.
- Mayer-Vietoris, homotopy invariance, or a long exact sequence alone without the excision
  isomorphism.
- Only a chain-level small-simplex lemma without the induced relative-homology isomorphism.
- Assuming the desired isomorphism or chain equivalence as structure data.
- Omitting the excision hypothesis, changing the ambient topology used by closure/interior, or
  silently strengthening it to an easier open/closed special case.
- The repository metadata value `已验证` as human-source or kernel evidence.

No Lean expression is frozen at intake. The later target must expose concrete pairs, relative
singular homology, the induced inclusion map, and the isomorphism claim.
