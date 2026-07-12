# Scope map

## Received scope

The catalog fixes only the Chinese title `Axiom A系统`, Stephen Smale, the year 1967, and the gloss
`双曲系统的公理` ("axioms for hyperbolic systems"). Source audit identifies the historical
definition as Smale 1967, section 1.6, item (6.1), printed page 777. The item defines a conceptual
class rather than asserting a truth-valued theorem.

## Candidate definition boundary

A later definition formalization or redirected theorem statement must retain the following
source-frozen boundary, but no bullet is credited as a theorem statement at intake:

- a connected compact `C^r` manifold and `C^r` diffeomorphism `f : M -> M`, with
  `1 <= r <= infinity` under Smale's standing conventions and the unresolved boundary convention
  made explicit;
- an exact nonwandering-set predicate, including the quantifier order over neighborhoods and
  positive return times;
- an invariant hyperbolic splitting of the tangent bundle over that set, with continuous stable and
  unstable subbundles and exact uniform contraction/expansion constants;
- the exact clause from item (6.1): periodic points of `f` are dense in the nonwandering set.

If the repository owner redirects this definition label to a theorem, the replacement must be
explicitly approved and source-frozen. Candidate theorem directions include equivalence between
reviewed definitions, openness/structural stability properties under additional hypotheses, or a
consequence such as spectral decomposition. None is silently selected here.

## Ambiguities to resolve

1. Whether the repository owner accepts a definition formalization as the deliverable or redirects
   the item to a truth-valued proposition about the source-frozen class.
2. How Smale's standing manifold conventions are made explicit in a modern exact statement,
   including boundary, dimension, Riemannian metric, and differentiability-class details.
3. How the source's nonwandering-set neighborhood quantifiers and positive-time convention are
   encoded without changing their scope.
4. How the source's Whitney splitting and contracting/expanding terminology are translated into
   Lean vector-bundle data and uniform estimates, and which metric-independence result is needed.
5. Whether an approved redirected theorem uses item (6.1) purely as a hypothesis/definition and what
   additional assumptions and exact conclusion it has.
6. Whether empty invariant sets, zero-dimensional manifolds, manifolds with boundary, finite
   discrete systems, and period-zero conventions are admitted; disconnected manifolds are outside
   Smale's stated standing convention.

## Explicit exclusions

- Presenting a newly defined predicate `IsAxiomA f` as if its definition were a theorem proof.
- Assuming hyperbolicity or periodic-point density as fields of a structure and projecting those
  fields as closure of the catalog target.
- Replacing differentiable hyperbolicity by expansivity, topological transitivity, mixing, positive
  entropy, or dense periodic points alone.
- Substituting the Anosov whole-manifold condition from `THM-M-1412`, the spectral decomposition
  theorem from `THM-M-1414`, or the Markov-partition result from `THM-M-1415`.
- Treating generic tangent maps, omega-limit sets, periodic-point predicates, or `Dense` as an
  Axiom A framework or an exact statement match.
- Crediting the catalog label `已验证` as primary human-source or Lean kernel evidence.

No canonical Lean expression is frozen at intake. The dependent statement phase is blocked until
an accountable source decision supplies a truth-valued proposition or an approved redirection.
