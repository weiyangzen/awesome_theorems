# Scope map

## Metadata boundary

The repository supplies the name "Lagrangian intersection Floer homology" and the gloss
"intersection theory of Lagrangian submanifolds". These denote a subject, not a proposition with a
truth value. Intake can identify Floer's Lagrangian-intersection theory, but it cannot choose among
its construction, invariance, rank-bound, cup-length, or generalized forms without a pinpoint
source statement.

## Candidate mathematical boundary

A source-faithful formulation may require the following data, with every convention fixed by the
selected theorem:

- a symplectic manifold `(P, omega)` and compact Lagrangian submanifolds `L` and `L'`;
- a Hamiltonian isotopy relating the Lagrangians and a transversality condition on `L ∩ L'`;
- hypotheses excluding or controlling holomorphic-disc and sphere bubbling, expressed in the
  original paper by conditions involving relative homotopy and later by exactness, monotonicity,
  minimal Maslov number, bounding data, or Novikov coefficients;
- a compatible almost-complex structure, Hamiltonian perturbation, moduli spaces of strips,
  compactness, gluing, and a proof that the differential squares to zero;
- a coefficient ring, grading and orientation convention, including whether only `Z/2`
  coefficients are available; and
- continuation maps and independence of auxiliary choices if the root is a well-definedness or
  invariance theorem.

For an intersection estimate, the conclusion must distinguish cardinality from algebraic count,
transverse from nontransverse intersection, the sum of Betti numbers from cup-length, and the
precise coefficient field. For a homology construction, it must specify the chain generators,
differential, grading, invariance relation, and comparison target.

## Variant decision required

The metadata could reasonably denote several inequivalent roots:

1. existence and well-definedness of Lagrangian intersection Floer homology under Floer's original
   no-bubbling assumptions;
2. invariance under Hamiltonian isotopy and identification with the ordinary homology of a
   Lagrangian in the self/isotopic case;
3. the resulting lower bound on the number of transverse intersections by the total mod-2 Betti
   number;
4. a cup-length lower bound; or
5. a later monotone, exact, unobstructed, or Fukaya-categorical generalization.

The statement phase must select one source-labelled theorem and preserve its exact assumptions.
Floer's original transverse-intersection lower bound is a plausible discovery candidate, but this
intake does not freeze it as the canonical claim.

## Explicit exclusions

- Defining an arbitrary chain complex whose homology is invariant by construction and calling it
  Lagrangian Floer homology.
- Assuming the desired rank or intersection inequality as a hypothesis.
- Restricting to identical Lagrangians, a finite toy model, or an empty intersection merely to
  obtain an easy Lean proposition.
- Dropping compactness, transversality, bubbling, orientation, coefficient, or Maslov-class
  hypotheses from a cited theorem.
- Substituting Hamiltonian Floer homology, Morse homology, or a finite-dimensional intersection
  number without a checked equivalence theorem.
- Treating `已验证`, mathematical consensus, or a citation as Lean or H0 evidence.

Before proof-tree work, the statement phase must freeze the exact ordered binders, hypotheses,
conclusion, degenerate cases, conventions, profiles, Lean imports and expression, environment
fingerprint, checked transports, and mutation fixtures.
