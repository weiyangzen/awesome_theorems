# THM-M-1288 frozen obligation tree

Registry version 1 contains 19 canonical obligations. The denominator digest is `89405ccd8affe61b940c2af5b00d295725716503f9aa7b81947e70fb3da55eb4`.

Proof edges point from a parent to required children and have reciprocal `composes` edges. Source, provenance, trust, documentation, and workflow graphs carry no proof credit. The exact root remains open.

## M1288-ROOT

Kind: `root`. Step budget: `20`.

The exact frozen Talenti inequality and least-admissible-constant proposition.

Formal surface: `Stage1Instances.THM_M_1288.TalentiSharpSobolevTarget`. Output: The canonical proposition.

Boundary: this frozen node supplies no proof unless its machine evidence and incoming composition edges are accepted.

## M1288-S-DEFINITIONS

Kind: `definition`. Step budget: `30`.

Fix Euclidean space, real integral powers, Sobolev conjugate, gradient, admissibility, and the displayed Gamma-function constant exactly as in Statement.lean.

Formal surface: `Stage1Instances.THM_M_1288.{Space,lpNorm,vectorLpNorm,sobolevConjugate,talentiConstant,IsAdmissibleConstant}`. Output: The exact formal vocabulary used by every proof child.

Boundary: this frozen node supplies no proof unless its machine evidence and incoming composition edges are accepted.

## M1288-S-DOMAIN

Kind: `terminal`. Step budget: `45`.

Derive n at least two, positivity of p and n-p, finiteness of the displayed expressions, and handle the zero test function without adding endpoint assumptions.

Formal surface: `planned Lean domain-and-boundary package for 1 < p < (n : Real)`. Output: All domain side conditions required by later transports and computations.

Boundary: this frozen node supplies no proof unless its machine evidence and incoming composition edges are accepted.

## M1288-S-FOUNDATION

Kind: `certificate`. Step budget: `20`.

Freeze the classical logic, choice, quotient, extensionality, TCB, and no-oracle policy for all terminal proof bodies.

Formal surface: `planned transitive axiom and trust report`. Output: Accepted foundation boundary.

Boundary: this frozen node supplies no proof unless its machine evidence and incoming composition edges are accepted.

## M1288-N-ELPNORM

Kind: `transport`. Step budget: `70`.

Transport the frozen real integral-power scalar and vector norms to and from mathlib eLpNorm statements under the exact positivity and integrability hypotheses.

Formal surface: `planned checked lpNorm/vectorLpNorm versus eLpNorm equivalences`. Output: Exact norm equalities or directed inequalities usable in the frozen target.

Boundary: this frozen node supplies no proof unless its machine evidence and incoming composition edges are accepted.

## M1288-N-GRADIENT

Kind: `transport`. Step budget: `65`.

Identify the norm of the total gradient of a smooth scalar map with the operator norm of its Frechet derivative in Euclidean space.

Formal surface: `planned checked gradient/fderiv operator-norm bridge`. Output: The derivative expression required by Sobolev infrastructure.

Boundary: this frozen node supplies no proof unless its machine evidence and incoming composition edges are accepted.

## M1288-N-REARRANGEMENT

Kind: `reduction`. Step budget: `90`.

Replace a compactly supported smooth function by its symmetric decreasing rearrangement, preserving its L^q mass and not increasing its gradient L^p mass.

Formal surface: `planned equimeasurability and Polya-Szego reduction`. Output: A radial nonincreasing representative sufficient for the sharp estimate.

Boundary: this frozen node supplies no proof unless its machine evidence and incoming composition edges are accepted.

## M1288-N-RADIAL

Kind: `reduction`. Step budget: `80`.

Convert the radial Euclidean norm integrals to weighted one-dimensional integrals with the correct sphere-area normalization.

Formal surface: `planned polar-coordinate radial integral reduction`. Output: The exact weighted one-dimensional variational inequality.

Boundary: this frozen node supplies no proof unless its machine evidence and incoming composition edges are accepted.

## M1288-B-BOUNDARY

Kind: `branch`. Step budget: `35`.

Separate zero and nonzero test functions and prove the split exhaustive; the zero branch closes directly and the nonzero branch supports normalization.

Formal surface: `planned zero/nonzero function split and recomposition`. Output: Exhaustive branches without division by a zero norm.

Boundary: this frozen node supplies no proof unless its machine evidence and incoming composition edges are accepted.

## M1288-L-WEIGHTED

Kind: `core_lemma`. Step budget: `100`.

Prove the sharp weighted one-dimensional Sobolev inequality produced by radial reduction, including all integration and limit boundary terms.

Formal surface: `planned sharp weighted one-dimensional inequality`. Output: The sharp radial inequality with its beta-integral coefficient.

Boundary: this frozen node supplies no proof unless its machine evidence and incoming composition edges are accepted.

## M1288-L-GAMMA

Kind: `computation`. Step budget: `85`.

Evaluate the beta and sphere-volume factors and prove algebraically that their coefficient equals talentiConstant n p in the frozen normalization.

Formal surface: `planned symbolic Beta/Gamma constant identity`. Output: Literal equality with Stage1Instances.THM_M_1288.talentiConstant.

Boundary: this frozen node supplies no proof unless its machine evidence and incoming composition edges are accepted.

## M1288-T-ADMISSIBILITY

Kind: `terminal`. Step budget: `55`.

Compose domain, encoding, rearrangement, radial, weighted-estimate, and constant computations to prove the displayed constant admissible.

Formal surface: `Stage1Instances.THM_M_1288.TalentiAdmissibilityPackage`. Output: Admissibility at exactly talentiConstant n p.

Boundary: this frozen node supplies no proof unless its machine evidence and incoming composition edges are accepted.

## M1288-C-EXTREMIZERS

Kind: `construction`. Step budget: `100`.

Construct smooth compactly supported approximations to the Aubin-Talenti profile and prove support, smoothness, scaling, and convergence invariants.

Formal surface: `planned compactly-supported extremizing sequence`. Output: Admissible test functions whose norm ratios converge to the displayed constant.

Boundary: this frozen node supplies no proof unless its machine evidence and incoming composition edges are accepted.

## M1288-L-LOWER-BOUND

Kind: `core_lemma`. Step budget: `75`.

Apply every admissible constant to the extremizing sequence and pass to the limit to bound it below by talentiConstant.

Formal surface: `planned least-constant lower-bound theorem`. Output: For every admissible C, talentiConstant n p <= C.

Boundary: this frozen node supplies no proof unless its machine evidence and incoming composition edges are accepted.

## M1288-T-OPTIMALITY

Kind: `terminal`. Step budget: `30`.

Package the extremizing-sequence lower bound with the exact ordered binders and admissibility predicate.

Formal surface: `Stage1Instances.THM_M_1288.TalentiOptimalityPackage`. Output: Least-admissible-constant sharpness.

Boundary: this frozen node supplies no proof unless its machine evidence and incoming composition edges are accepted.

## M1288-T-ASSEMBLE

Kind: `transport`. Step budget: `12`.

Compose exact admissibility and optimality packages into the conjunction of the frozen root.

Formal surface: `Stage1Instances.THM_M_1288.talentiSharpSobolevTarget_of_packages`. Output: The exact canonical root conditional on both packages.

Boundary: this frozen node supplies no proof unless its machine evidence and incoming composition edges are accepted.

## M1288-X-MATHLIB

Kind: `bridge`. Step budget: `40`.

Audit and, where exact, consume pinned mathlib's non-sharp eLpNorm/fderiv Sobolev family without crediting it for the Talenti constant or optimality.

Formal surface: `MeasureTheory.eLpNorm_le_eLpNorm_fderiv_of_eq`. Output: Supporting non-sharp infrastructure only.

Boundary: this frozen node supplies no proof unless its machine evidence and incoming composition edges are accepted.

## M1288-X-SOURCE

Kind: `terminal`. Step budget: `40`.

Map every material analytic and constant step to pinpoint reviewed primary-source passages, conventions, and errata results.

Formal surface: `non-machine primary-source node crosswalk`. Output: Human-source coverage without machine proof credit.

Boundary: this frozen node supplies no proof unless its machine evidence and incoming composition edges are accepted.

## M1288-X-PROVENANCE

Kind: `certificate`. Step budget: `35`.

Inventory terminal bodies, wrappers, imports, licenses, axioms, trust closure, and replay receipts.

Formal surface: `planned machine-derived provenance closure`. Output: Release provenance overlay without mathematical proof credit.

Boundary: this frozen node supplies no proof unless its machine evidence and incoming composition edges are accepted.
