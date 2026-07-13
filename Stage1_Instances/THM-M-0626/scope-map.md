# Scope map

## Received claim

The repository supplies a truth-valued sentence, `连通集的连续像连通`: the continuous image of a
connected set is connected. Unlike a generic "properties of connected spaces" label, this fixes
the operation (continuous image), the source property (connected), and the conclusion (connected).
It does not supply a bibliography, formal definitions, binder order, or boundary conventions.

## Candidate mathematical scope

The intake candidate has arbitrary topological spaces `X` and `Y`, a subset `E` of `X`, and a
continuous map `f : X -> Y`. If `E` is nonempty and connected, then the direct image `f(E)` is
nonempty and connected. No separation, countability, compactness, metrizability,
injectivity, or surjectivity assumption is added.

The Stacks Project's immutable modern formulation assumes `f` is globally continuous. Pinned
mathlib's `IsConnected.image` assumes only `ContinuousOn f s`. The latter is the sharper natural
set theorem and global continuity implies it, but intake does not credit that relationship until a
Lean transport is compiled during the statement phase.

## Definitions and boundary cases

- Ordinary connectedness is provisionally the nonempty convention. Pinned mathlib defines
  `IsConnected s` as `s.Nonempty` together with `IsPreconnected s`; the inspected Stacks definition
  likewise says a connected space is nonempty.
- The empty set is therefore outside the canonical candidate. `IsPreconnected.image` is a valid
  empty-allowing generalization, not the literal nonempty-connected root.
- Singleton sets and constant maps are included. Their image is a singleton and remains connected.
- The function may be noninjective or nonsurjective, and the ambient spaces may be non-Hausdorff.
- Continuity is required only on the source subset in the direct candidate. A globally continuous
  formulation is an alternate stronger-premise encoding, not an unrecorded replacement.
- The conclusion concerns the set image `f '' s`, not necessarily the whole codomain or a range
  from the entire source space.

## Decisions required at statement freeze

1. Obtain independent approval of the modern source lead, its definitions, assumptions, proof
   boundary, history/correction disposition, and exact relation to the uncited catalog sentence.
2. Fix the canonical nonempty `IsConnected` convention and state explicitly why the empty-allowing
   `IsPreconnected` variant is not the root.
3. Fix arbitrary topological types, universes, topology instances, set, function, binder order,
   implicit-versus-explicit parameters, hypotheses, and conclusion.
4. Decide whether `ContinuousOn f s` is canonical and global `Continuous f` an alternate, or the
   reverse; compile every credited implication or equivalence.
5. Fix the direct image versus subtype/range representation and compile any credited transport.
6. Elaborate with the minimal pinned import, serialize the expression/environment fingerprints,
   and mutation-test removed connectedness or continuity, changed domain and binder scope, and
   empty/singleton/constant-map boundary cases.
7. Audit the candidate's terminal proof body, transitive dependencies, axioms, trust boundaries,
   placeholders, and exact source provenance before assigning machine proof credit.

## Explicit exclusions

- Do not replace ordinary connectedness with `IsPreconnected` while dropping nonemptiness.
- Do not replace the subset theorem with `isConnected_range`, which assumes a connected whole
  source space and global continuity.
- Do not replace it with `Function.Surjective.connectedSpace`, which additionally changes the
  conclusion to connectedness of the whole codomain and assumes surjectivity.
- Do not add global continuity, injectivity, surjectivity, Hausdorffness, compactness, metrizability,
  or other simplifying premises without recording a checked relationship to the canonical claim.
- Do not substitute path-connected image preservation; that belongs to `THM-M-0627`.
- Do not use a predicate, axiom, structure field, hypothesis, oracle, or certificate that already
  contains the desired result.
- Do not treat the catalog's `已验证` label, a source citation, a theorem-name match, the probe, or
  an unrelated build as source or proof evidence.

## Retry condition

The statement phase may proceed after master acceptance of this intake and an independent reviewer
approves the source and convention map. It must then elaborate and fingerprint one exact Lean
target and compile the required alternate-form transports and mutations before inspecting proof
closure.
