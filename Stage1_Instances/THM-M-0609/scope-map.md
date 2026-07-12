# Scope map

## Literal source boundary

The repository supplies the title "Floer homology", the attribution Andreas Floer, the year 1988,
and the gloss "an invariant in symplectic geometry and low-dimensional topology". This identifies
a subject and construction family, not a theorem with fixed domains, binders, hypotheses, and
conclusion. The source metadata label `已验证` is untrusted under rev-5.6 and gives no human-proof
or machine-proof credit.

## Family shape retained for selection

A later exact target may include the following nodes only after one primary theorem fixes them:

- a geometric configuration space and action/Morse functional;
- generators such as Hamiltonian periodic orbits or Lagrangian intersection points;
- a coefficient ring, relative or absolute grading, and orientation/sign convention;
- a differential defined by counts of isolated solutions to a Floer equation;
- compactification and gluing sufficient to prove `d^2 = 0`;
- independence under specified auxiliary choices via continuation maps; and
- an invariance or comparison conclusion for the selected geometric objects.

These bullets are a scope inventory, not a canonical statement or proof architecture.

## Proposition-changing decisions

| Decision | Alternatives that must remain separate | Effect on the target |
|---|---|---|
| Floer theory | Hamiltonian, Lagrangian intersection, instanton, monopole, Heegaard, symplectic | changes generators, trajectories, hypotheses, and invariant |
| Geometric regime | closed/convex/exact/monotone symplectic manifolds; admissible Lagrangians | changes compactness and bubbling arguments |
| Claim kind | existence of the complex, `d^2 = 0`, auxiliary-choice invariance, Hamiltonian-isotopy invariance, or comparison theorem | these are distinct propositions, not aliases |
| Coefficients and signs | `Z/2`, integers, Novikov rings, local systems | changes orientation and convergence obligations |
| Grading | relative, absolute, integer, or cyclic | changes the resulting homology object |
| Degeneracy | nondegenerate/transverse input versus perturbation-independent extension | changes binders and continuation obligations |

## Explicit exclusions

- `THM-M-0610` instanton Floer homology and `THM-M-0611` Lagrangian-intersection Floer homology as
  silent substitutes for this generic target.
- Morse homology on a finite-dimensional manifold as if it established a Floer analytic theory.
- A chain complex or homology group postulated as structure fields, including invariance supplied
  as an assumption.
- A dimension inequality, Euler-characteristic identity, or Arnold-conjecture consequence in place
  of construction and invariance of the selected Floer homology.
- Numerical trajectory counts or informal transversality/compactness arguments as kernel evidence.

The statement phase must first select one source theorem. If the generic umbrella title is to be
retained, it must be redirected to a precisely stated theory-construction theorem rather than
broadened across incompatible variants.
