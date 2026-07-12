# Scope map

## Included theorem family

- A pointed topological space `(X, x)` and a positive sphere/loop dimension `n`.
- Based continuous maps from the pointed `n`-sphere to `(X, x)`, modulo based homotopy relative to
  the basepoint, or a checked equivalent iterated-loop encoding.
- The group operation induced by the standard sphere pinch/concatenation construction, with
  identity and inverse, if group formation is selected as the exact root.
- The higher-dimensional commutativity result for the source's range, ordinarily `n >= 2`, if it
  is selected as part of the root.
- Functoriality under pointed continuous maps and invariance under pointed homotopy equivalence only
  when included by the selected source theorem.

## Decisions required at statement freeze

The statement phase must select one proposition from this family and freeze the source edition and
pinpoint theorem; the natural-number convention for `pi_0`, `pi_1`, and "higher"; pointed versus
unpointed spaces; the sphere or iterated-loop model; based homotopy and quotient/setoid encoding;
the exact group operation and proof of well-definedness; the abelian range; universes and topology
typeclasses; functoriality variance; and whether the result is a construction, an isomorphism, or a
property of an already defined object. It must explicitly handle `n = 0`, `n = 1`, empty types,
basepoint changes, disconnected spaces, and non-Hausdorff spaces according to the chosen source.

These choices change the Lean binders and conclusion. In particular, a definition of
`HomotopyGroup.Pi` is not interchangeable with the theorem that it has a group or commutative-group
structure.

## Explicit exclusions

- The fundamental group alone, a computation of the homotopy groups of one particular space, or
  stable homotopy groups as a substitute for the general unstable construction.
- The Hurewicz theorem relating homotopy and homology, which is the separate target `THM-M-0558`.
- Weak homotopy equivalence/Whitehead results, long exact sequences, or fibration calculations
  unless they are dependencies of the selected exact root.
- Free homotopy classes in place of based homotopy classes without a checked transport and the
  necessary connectedness/basepoint hypotheses.
- An abstract structure that takes the desired group laws, commutativity, or invariance as fields.
- The repository metadata value `已验证` or an adjacent mathlib API as theorem-completion evidence.

No canonical Lean expression is frozen by intake. A later statement must expose the concrete
pointed maps, homotopy relation, quotient/loop model, operation, and selected conclusion.
