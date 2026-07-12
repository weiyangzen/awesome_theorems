# Scope map

## Repository claim

The repository wording is only `KPZ普适类` ("KPZ universality class"), attributed to many
mathematicians and dated to the twenty-first century. It supplies no model, random variables,
parameters, quantifiers, hypotheses, convergence mode, or conclusion. The `已验证` label is
untrusted metadata under rev-5.6 and cannot resolve those omissions.

## Provisional included claim families

- A named stochastic growth, directed-polymer, last-passage-percolation, or interacting-particle
  model with its probability space, dynamics, and initial data explicitly fixed.
- Source-specific centering and KPZ `1:2:3` scaling: time, space, and height-fluctuation scales.
- A source-specific limit conclusion, such as one-point convergence to a Tracy-Widom law,
  process-level convergence to the Airy process, or height-function convergence to the KPZ fixed
  point, in an explicitly stated topology.
- Every parameter restriction, moment/tail hypothesis, boundary condition, and exceptional case in
  the selected proved theorem.

These are candidate theorem families, not interchangeable encodings and not a frozen theorem.

## Decisions required at statement freeze

The statement phase must choose a single pinpointed proved theorem and freeze: the microscopic
model and parameter range; probability spaces and random inputs; initial-data class; height/current
normalization and sign conventions; law and coupling conventions; deterministic centering;
non-universal scale constants; time, space, and fluctuation exponents; whether convergence is
one-point, finite-dimensional, or process-level; the state space and topology; the limiting object
and its normalization; and all degenerate or boundary cases. Ordered binders, universes, minimal
imports, foundation profile, and computation policy must follow that selection.

## Explicit exclusions

- The unrestricted assertion that every physical model believed to be in the KPZ class has the
  same scaling limit; no such blanket theorem is frozen or claimed proved here.
- The KPZ stochastic PDE, its well-posedness, or regularity structures alone as a substitute for a
  universality/convergence result.
- A Tracy-Widom distribution theorem with no proved scaling-limit map from the selected model.
- Numerical simulations, experimental exponent fits, physics renormalization predictions, or the
  repository's `已验证` label as theorem evidence.
- A structure or hypothesis that assumes the desired convergence, and a toy finite probability
  model substituted merely because it is easier to encode in Lean.

The later formal target must expose the actual random model, rescaling, and convergence predicate.
If the required stochastic-process topology or limiting object is absent from pinned dependencies,
that is an API blocker rather than permission to weaken the claim.
