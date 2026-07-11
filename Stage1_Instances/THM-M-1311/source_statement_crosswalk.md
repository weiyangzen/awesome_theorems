# Source-statement crosswalk

| Claim component | Human source anchor | Lean target component | Intake assessment |
|---|---|---|---|
| Local Cauchy existence for Einstein's equations | Y. Fourès-Bruhat, *Théorème d'existence pour certains systèmes d'équations aux dérivées partielles non linéaires*, Acta Mathematica 88 (1952), 141-225, DOI `10.1007/BF02392131` | Future exact root declaration | Primary historical paper identified, but theorem/page-level premise mapping, edition hash, and errata review remain open: `H1` |
| Vacuum initial data and constraint equations | Same paper and its Einstein-equation application; exact section/theorem pinpoint pending | Initial-data structure and constraint predicate | Dimension, differentiability/Sobolev assumptions, conventions, and allowed topology are not frozen |
| Hyperbolic reduction | The paper's reduction of the field equations to a hyperbolic PDE system; exact pinpoint pending | Gauge-reduction bridge | Candidate architecture only; no checked formal bridge |
| Reduced-system local solution | General nonlinear PDE existence results developed in the 1952 paper | PDE local-existence obligation | Function spaces, estimates, and lifespan conclusion require source-level extraction |
| Return to the geometric Einstein equations | Einstein application in the same work | Constraint/gauge propagation and reconstruction obligations | Exact conclusion, uniqueness strength, and equivalence modulo coordinates remain unresolved |
| Maximal globally hyperbolic development | Y. Choquet-Bruhat and R. Geroch, *Global aspects of the Cauchy problem in general relativity*, Communications in Mathematical Physics 14 (1969), 329-335, DOI `10.1007/BF01645389` | None in this target | Explicitly excluded; this is the neighboring THM-M-1312 claim |

The repository discovery source says only "Einstein equations have local existence" and labels the
result verified. That wording omits the equation regime, initial-data constraints, regularity,
gauge, uniqueness, and equivalence relation, so it cannot serve as the canonical statement. The
1952 title also covers a broader nonlinear-PDE framework; this dossier does not silently substitute
that general PDE theorem for the Einstein application.

No Lean declaration or public Lean 4 proof is asserted at intake. The later statement phase must
obtain and hash the source text, pinpoint the exact Einstein theorem and assumptions, decide whether
uniqueness is part of this target, define every geometric/PDE object, elaborate one canonical Lean
expression, and mutation-test constraints, regularity, dimension, gauge scope, and local/global
boundaries. Anchor audit must separately search mathlib and external Lean projects.

Discovery links (not immutable evidence receipts):

- 1952 paper: <https://doi.org/10.1007/BF02392131>
- 1969 exclusion boundary: <https://doi.org/10.1007/BF01645389>

No `H0`, `M0`, or readable-proof closure is claimed. Independent source review remains required.
