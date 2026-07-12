# Scope map

## Included theorem family

- Brown's existence result for a representing object, not the definition or universal-element
  characterization of a functor that is already known to be representable.
- The repository's stated application to generalized cohomology theories.
- A contravariant homotopy functor on the precise pointed CW domain chosen from the primary source.
- The source's wedge axiom and its excision, weak-pushout, or Mayer-Vietoris condition.
- A natural representation by pointed homotopy classes into a representing space.
- Degreewise representation for a graded theory; spectrum compatibility only if the selected
  source statement and formal target explicitly include it.

## Decisions reserved for the statement phase

The local source phrase is not an exact proposition. Primary-source inspection must fix the domain
(including connectedness and CW hypotheses), variance, codomain, wedge cardinality, exactness
condition, binder order, and whether Brown's general functor theorem or its cohomology-theory
corollary is canonical. It must also determine how the 1963 correction affects the proof or
assumptions. Lean universes, quotient/homotopy encodings, classical principles, minimal imports,
and boundary cases then follow those mathematical choices rather than convenience.

## Boundary and non-substitution rules

- A Yoneda or `RepresentableBy` equivalence does not establish existence of a representing object.
- Freyd's representability or adjoint functor theorem is not substituted unless a checked bridge
  verifies all Brown hypotheses and the exact conclusion.
- Representability of ordinary singular cohomology alone is only a special case.
- A finite-CW, finite-wedge, stable-category, or spectrum-level theorem is not silently exchanged
  for the source theorem.
- `THM-M-0561` (Omega-spectrum representation) remains a distinct repository target. An
  Omega-spectrum package is not folded into this root without an explicit source and scope ruling.
- The metadata label `已验证` is untrusted and supplies no proof or formalization credit.

## Planned architecture, not frozen obligations

The likely proof architecture has separate nodes for the homotopy category, wedge and excision
axioms, construction of increasingly universal elements/representing approximations, a limiting
object, surjectivity and injectivity of the induced natural map, and naturality. These are intake
scope markers only. The obligation-tree phase must derive the exact branches from the inspected
source before freezing its denominator.
