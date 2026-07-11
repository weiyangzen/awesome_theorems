# Scope map

## Provisionally included branch

- Closed, connected, oriented, simply connected topological four-manifolds.
- Integral second homology and its unimodular symmetric intersection form.
- Kirby-Siebenmann obstruction where required by the selected source statement.
- An orientation-preserving homeomorphism classification conclusion, with existence and uniqueness
  separated if the inspected source states them separately.

## Decisions reserved for the statement phase

Primary-source inspection must freeze whether manifolds are required to be compact, boundaryless,
and based; whether classification is of manifolds or oriented homotopy equivalences; whether the
form is supplied with an isometry; the odd/even and definite/indefinite branches; the precise role
and normalization of the Kirby-Siebenmann invariant; and any exceptional or stabilization clauses.
It must also freeze universes, binder order, orientation reversal, empty/disconnected degeneracies,
and whether existence and uniqueness are distinct canonical Lean targets.

## Explicit exclusions

- A classification of all topological four-manifolds with arbitrary fundamental group.
- Smooth or PL classification, Donaldson diagonalization, exotic smooth structures, or a claim
  that homeomorphic four-manifolds are diffeomorphic.
- Classification by intersection form alone when the selected theorem requires additional data.
- A structure that assumes the desired homeomorphism or classification equivalence as a field.
- The legacy module's algebraic constructors, blocker enums, or partial wrappers as terminal proof.

Downstream formalization must provide concrete manifold, orientation, homology, intersection-form,
Kirby-Siebenmann, and homeomorphism interfaces, or record exact API blockers without weakening the
source theorem.
