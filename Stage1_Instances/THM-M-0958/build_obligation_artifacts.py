#!/usr/bin/env python3
"""Build the frozen THM-M-0958 obligation registry and typed graph bundle."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ITEM = "S56-M-0958-OBLIGATION_TREE"
THEOREM = "THM-M-0958"
PREFIX = "M0958-"
REGISTRY_ID = "THM-M-0958-OBLIGATIONS-v1"
ROOT_EXPRESSION = "bc0d841038cdbcd4960581583c4ddfb7004d7ad38cf6432ab4803e9908f8f59c"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
BEHREND_BLOB = "7d3eb0e603040dcd72fe35e39c82f4d615b3e254"
GRAPH_NAMES = (
    "proof", "refinement", "provenance", "evidence", "trust",
    "documentation", "workflow",
)


def oid(short: str) -> str:
    return PREFIX + short


def digest(value: object) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(payload).hexdigest()


def file_digest(name: str) -> str:
    return hashlib.sha256((HERE / name).read_bytes()).hexdigest()


def spec(short: str, kind: str, risk: str, claim: str, formal: str,
         output: str, budget: int, inference: str, locator: str, *,
         machine: str = "required", human: str = "required",
         readable: str = "required", body: str | None = None,
         root_relevant: bool = True) -> dict:
    return {
        "short": short, "kind": kind, "risk": risk, "claim": claim,
        "formal": formal, "output": output, "budget": budget,
        "inference": inference, "locator": locator, "machine": machine,
        "human": human, "readable": readable, "body": body,
        "root_relevant": root_relevant,
    }


ROWS = [
    spec(
        "ROOT", "root", "critical",
        "Elkin's exact one-based asymptotic lower bound for three-term-progression-free subsets.",
        "Stage1Instances.THM_M_0958.ElkinConstructionTarget",
        "The complete frozen ElkinConstructionTarget.", 12,
        "Consume the exact root composition, witness package, and witness-to-root transport without changing any binder or quantitative factor.",
        "Stage1_Instances/THM-M-0958/Statement.lean:62-64",
    ),
    spec(
        "S-INTERFACE", "definition", "critical",
        "Preserve the ordered c, positivity, N, positivity, n, and N <= n binders and the Real-coerced one-based extremum.",
        "Stage1Instances.THM_M_0958.ElkinConstructionTarget",
        "The exact canonical formal interface.", 18,
        "Read the elaborated expression and preserve every domain, binder scope, coercion, endpoint, and inequality orientation.",
        "Stage1_Instances/THM-M-0958/statement.json",
        machine="informational", human="not_applicable",
    ),
    spec(
        "S-DEFINITIONS", "definition", "critical",
        "Freeze elkinScale, SourceProgressionFree, addRothNumber, and the one-based interval as the source vocabulary.",
        "Stage1Instances.THM_M_0958.{elkinScale,SourceProgressionFree}",
        "Exact definitions of the quantitative scale, progression predicate, and extremal set domain.", 30,
        "Unfold base-two logarithms, the fourth-root rpow, distinct-triple arithmetic, and Ico 1 (n+1) exactly once at their interfaces.",
        "Stage1_Instances/THM-M-0958/Statement.lean:22-38",
        machine="informational",
    ),
    spec(
        "S-BOUNDARY", "branch", "high",
        "Retain the positive asymptotic threshold, its included endpoint, totalized n=0/1 expressions, repeated-triple policy, and no hidden finite-case strengthening.",
        "Statement boundary lemmas and four structural mutations",
        "A complete boundary policy distinguishing the root from weakened or shifted variants.", 36,
        "Use the four killed mutations and the zero/one fixtures to reject removed positivity, changed domains or scope, and the off-by-one interval.",
        "Stage1_Instances/THM-M-0958/Statement.lean:120-167",
        machine="informational",
    ),
    spec(
        "S-WITNESS-TRANSPORT", "transport", "critical",
        "Transport an exact one-based progression-free witness package to the canonical extremal inequality.",
        "Stage1Instances.THM_M_0958.ObligationTree.WitnessToRootTransport",
        "WitnessConstructionTarget implies ElkinConstructionTarget.", 18,
        "Apply the checked witness/extremum equivalence only in its declared witness-to-root direction.",
        "Stage1_Instances/THM-M-0958/ObligationTree.lean#checkedWitnessToRootTransport",
        human="not_applicable",
    ),
    spec(
        "S-ROTH-TRANSPORT", "transport", "high",
        "Relate the one-based source extremum to mathlib's zero-based rothNumberNat without changing n or the scale.",
        "Stage1Instances.THM_M_0958.elkinConstructionTarget_iff_rothNumberTarget",
        "A checked bidirectional alternate encoding with no duplicate root credit.", 16,
        "Use addRothNumber_Ico at endpoints 1 and n+1 and retain the same quantitative expression.",
        "Stage1_Instances/THM-M-0958/Statement.lean:81-113",
        machine="informational", body="local-statement#elkinConstructionTarget_iff_rothNumberTarget",
        root_relevant=False,
    ),
    spec(
        "S-FOUNDATION", "certificate", "critical",
        "Audit classical choice, quotient and extensionality principles, compiled artifacts, and the no-oracle computation policy transitively.",
        "Lean 4.29.0 foundation and TCB report for all eventual terminal bodies",
        "An accepted foundation and computation boundary.", 55,
        "Compare machine-derived axioms, executables, compiled inputs, and computation mechanisms with the selected profiles.",
        "Stage1_Instances/THM-M-0958/anchor-audit.json",
        machine="informational", human="not_applicable",
    ),
    spec(
        "N-PARAMETERS", "normalization", "critical",
        "Choose and relate the dimension k, digit width y, annulus width g, radius window, and sufficiently-large-n threshold.",
        "planned exact Lean Elkin parameter package",
        "Parameters satisfying every construction, counting, embedding, and asymptotic side condition.", 38,
        "Assemble the separately frozen dimension, radix, annulus-width, rounding, and common-threshold packages.",
        "arXiv:0801.4310v1, Section 4, printed pages 5-6",
    ),
    spec(
        "N-DIMENSION", "normalization", "critical",
        "Set k near sqrt(2 log_2 n) with explicit natural rounding and prove the required lower bounds on k.",
        "planned exact Lean dimension parameter signature",
        "A positive natural k with quantified comparison to sqrt(2 log_2 n).", 55,
        "Convert ceil/floor inequalities into explicit bounds strong enough for every later exponent and dimension condition.",
        "arXiv:0801.4310v1, Sections 3-4, equations (8) and (12)",
    ),
    spec(
        "N-DIGIT-RADIX", "normalization", "critical",
        "Set y to floor(n^(1/k)/2), keep y positive, and bound the base-(2y) image below n.",
        "planned exact Lean digit/radix parameter signature",
        "A natural digit width y and radix 2y with exact range and power inequalities.", 70,
        "Replace the paper's integral idealization by floor inequalities and quantify the constant loss.",
        "arXiv:0801.4310v1, printed page 5, equation (8) and rounding paragraph",
    ),
    spec(
        "N-ANNULUS-WIDTH", "normalization", "critical",
        "Choose one universal positive epsilon and integer annulus width g corresponding to epsilon*k with exact endpoints.",
        "planned exact Lean annulus-width signature",
        "An integer g between the required positive lower bound and k, plus exact shell endpoints.", 62,
        "Specify the floor/ceiling convention for epsilon*k and prove every width and partition-count inequality.",
        "arXiv:0801.4310v1, printed pages 5-6, equations (9)-(10)",
    ),
    spec(
        "N-ROUNDING", "normalization", "critical",
        "Control every floor, ceiling, integer squared-norm endpoint, and constant-factor loss suppressed as a minor adjustment in the source.",
        "planned exact Lean rounding and coercion package",
        "Checked transfers from real parameter formulas to natural dimensions, digits, shell widths, and cardinalities.", 95,
        "Prove each rounding error is absorbed by a named universal constant after one explicit threshold.",
        "arXiv:0801.4310v1, printed page 5, first paragraph",
    ),
    spec(
        "N-THRESHOLDS", "normalization", "critical",
        "Synchronize all sufficiently-large qualifications from dimensions, moments, volume, discrepancy, epsilon, and embedding.",
        "planned exact Lean common-threshold signature",
        "One positive natural N supporting every downstream side condition for all n >= N.", 80,
        "Take a finite maximum of named thresholds and transport every local eventual statement to the canonical quantifier order.",
        "arXiv:0801.4310v1, Sections 3-5",
    ),
    spec(
        "B-Y-INTEGRAL", "branch", "high",
        "Handle the ideal branch where n^(1/k)/2 is represented by the selected integer y without floor loss.",
        "planned exact Lean ideal-digit branch",
        "The fixed-index estimates under the ideal radix identity.", 35,
        "Derive the source's clean cardinality and range estimates from the exact radix identity.",
        "arXiv:0801.4310v1, printed page 5",
    ),
    spec(
        "B-Y-FLOOR", "branch", "critical",
        "Handle the actual floor branch y=floor(n^(1/k)/2) and prove the promised constant-factor comparison.",
        "planned exact Lean floored-digit branch",
        "The same fixed-index estimates with explicit constant losses and no integrality assumption.", 88,
        "Use large-n lower bounds to compare the floored digit width to the ideal value and propagate the loss through y^(k-2).",
        "arXiv:0801.4310v1, printed page 5, rounding paragraph",
    ),
    spec(
        "B-PARAMETER-MERGE", "branch", "critical",
        "Recompose the ideal and floored parameter analyses into one exhaustive natural-n construction route.",
        "planned exact Lean parameter-branch recomposition",
        "A fixed-index parameter package without an unproved integrality assumption.", 28,
        "Split on the relevant floor equality and consume both parameter branches with the same final output type.",
        "arXiv:0801.4310v1, printed page 5",
    ),
    spec(
        "C-RANDOM-VARIABLES", "construction", "critical",
        "Construct independent uniform digit variables Y_i, their squares Z_i, and the squared-norm sum Z over the discrete cube.",
        "planned exact Lean finite probability-space construction",
        "A finite probability model whose outcomes enumerate the digit cube uniformly.", 75,
        "Build the product probability space and identify Z with the squared Euclidean norm of the sampled digit vector.",
        "arXiv:0801.4310v1, Sections 3-4, printed pages 3-5",
    ),
    spec(
        "L-DIGIT-MEAN", "core_lemma", "high",
        "Compute the exact digit-square expectation and its asymptotic comparison with y^2/3.",
        "planned exact Lean finite-sum expectation lemma",
        "An exact formula and explicit error bound for E[Z_i] and E[Z].", 70,
        "Evaluate finite sums of squares, divide by the uniform mass, and sum across k coordinates.",
        "arXiv:0801.4310v1, equation (6), printed page 3",
    ),
    spec(
        "L-DIGIT-VARIANCE", "core_lemma", "critical",
        "Compute the digit-square variance and bound the standard deviation by the explicit sqrt(k)*y^2 scale.",
        "planned exact Lean finite-sum variance lemma",
        "Exact variance identities and two-sided bounds for sigma_Z.", 90,
        "Evaluate fourth-power sums, use independence to add variances, and replace asymptotic notation by named constants.",
        "arXiv:0801.4310v1, equation (7), printed page 3",
    ),
    spec(
        "L-MOMENTS", "core_lemma", "critical",
        "Assemble the mean and variance calculations into the radius and shell-scale estimates used by the construction.",
        "planned exact Lean moment package",
        "Bounds for mu_Z and sigma_Z uniform over all indices above the parameter threshold.", 25,
        "Combine the exact mean and variance children without replacing their explicit constants by untracked O-notation.",
        "arXiv:0801.4310v1, equations (6)-(7)",
    ),
    spec(
        "L-CHEBYSHEV", "bridge", "critical",
        "At least three quarters of the digit cube lies in the squared-norm window mu_Z plus or minus 2 sigma_Z.",
        "planned exact Lean finite Chebyshev specialization",
        "A cardinality lower bound for integer cube points in the wide annulus.", 55,
        "Apply a pinned kernel-checked Chebyshev inequality and translate probability mass back to finite cardinality.",
        "arXiv:0801.4310v1, equation (9), printed page 5",
    ),
    spec(
        "C-ANNULUS-PARTITION", "construction", "critical",
        "Partition the wide norm window into disjoint integer squared-norm shells of width g, including the final endpoint convention.",
        "planned exact Lean finite shell partition",
        "A disjoint exhaustive indexed family of thin annuli and a bound on its cardinality.", 75,
        "Define integer shell indices using floor/ceiling operations and prove disjointness, coverage, and the 4 sigma_Z/g count.",
        "arXiv:0801.4310v1, printed page 5, before equation (10)",
    ),
    spec(
        "L-LARGE-ANNULUS", "core_lemma", "critical",
        "Some thin annulus contains at least a constant times epsilon*sqrt(k)*y^(k-2) cube points.",
        "planned exact Lean shell pigeonhole theorem",
        "A radius R and a large integer-point set in the thin annulus [R^2-g,R^2].", 65,
        "Apply finite pigeonhole to the shell partition and substitute the explicit variance and width bounds.",
        "arXiv:0801.4310v1, equations (10)-(11), printed pages 5-6",
    ),
    spec(
        "C-EXTERIOR-SUBSET", "construction", "critical",
        "Select the annulus points lying in Ext(B) and retain at least half of all selected cube points.",
        "planned exact Lean exterior-point subset construction",
        "A convexly independent integer-vector set with at least half the large-annulus cardinality.", 55,
        "Subtract the union-bounded nonextreme points and use the strict epsilon inequality to prove the half-cardinality bound.",
        "arXiv:0801.4310v1, equations (12)-(21), printed pages 6-11",
    ),
    spec(
        "L-NONEXTREME-WITNESS", "core_lemma", "critical",
        "Every nonextreme integer point in the outer shell yields a nonzero short integer direction delta with 0 <= <b,delta> <= g and norm-squared <= g.",
        "planned exact Lean Lemma 4.1 signature",
        "A short-direction witness for every bad annulus point.", 60,
        "Choose one endpoint of a nontrivial convex representation with inner product at least norm-squared and expand norm(b+delta)^2.",
        "arXiv:0801.4310v1, Lemma 4.1, printed pages 6-7",
    ),
    spec(
        "L-SHORT-DIRECTION-COUNT", "core_lemma", "critical",
        "The number of nonzero integer vectors with norm-squared at most g=epsilon*k is at most a constant times 2^(eta(epsilon)k), with eta tending to zero.",
        "planned exact Lean Lemma 4.2 signature",
        "An explicit entropy-style upper bound D_hat(g) for short directions.", 85,
        "Count square decompositions by stars and bars, account for signs, sum over h <= g, and verify the limit of eta.",
        "arXiv:0801.4310v1, Lemma 4.2, printed page 7",
    ),
    spec(
        "L-HYPERPLANE-SECTION", "core_lemma", "high",
        "Intersecting the radius-squared-T sphere with <alpha,delta>=h produces the stated centered (k-1)-sphere and annular section.",
        "planned exact Lean Lemma 4.3 signature",
        "The exact center, squared radius, and width of each hyperplane section.", 45,
        "Complete the square around (h/norm(delta)^2)delta and preserve the annulus inequalities.",
        "arXiv:0801.4310v1, Lemma 4.3, printed page 8",
    ),
    spec(
        "L-OCTANT-COORDINATES", "core_lemma", "critical",
        "A short integer direction has at most epsilon*k nonzero entries, giving at least (1-epsilon)k nonnegative coordinates after the adapted orthonormal change of basis.",
        "planned exact Lean Lemma 4.4 signature",
        "Containment of the cube section in a union of at most 2^(epsilon*k) positive-octant pieces.", 75,
        "Build the adapted hyperplane basis, identify standard basis vectors outside the support, and prove their coordinates are nonnegative on the cube.",
        "arXiv:0801.4310v1, Lemma 4.4, printed pages 8-10",
    ),
    spec(
        "L-ANNULUS-VOLUME", "core_lemma", "critical",
        "Bound the positive-octant (k-1)-annulus volume by g*(pi*e/6)^(k/2)*y^(k-3)*2^(O(sqrt(k))).",
        "planned exact Lean Lemma 4.5 signature with explicit constants",
        "An explicit volume upper bound suitable for the bad-point count.", 100,
        "Subtract ball volumes, apply the radius estimate, split Gamma parity cases, use explicit Stirling bounds, and replace every O-term by named constants.",
        "arXiv:0801.4310v1, Lemma 4.5 and equations (16)-(18), printed pages 10-11",
    ),
    spec(
        "C-ROTATED-LATTICE", "construction", "critical",
        "Define the rotated integer lattice and its intersections with balls and coordinate half-spaces after the hyperplane basis change.",
        "planned exact Lean rotated-lattice and halfspace package",
        "Covolume-preserving lattice-count and volume objects used in Section 5.", 85,
        "Extend the hyperplane basis orthogonally, transport the integer lattice, and prove rotation preserves norm, volume, and point bijections.",
        "arXiv:0801.4310v1, Section 5, printed pages 12-13",
    ),
    spec(
        "L-Q-COUNT", "core_lemma", "critical",
        "Bound the integer points in each octant-annulus section by the Section 5 discrepancy estimate and the annular volume difference.",
        "planned exact Lean Lemma 5.1 signature",
        "Equation (22), hence the point-count input required by equation (19).", 80,
        "Apply discrepancy to external and internal halfspace balls, subtract counts, bound both errors, and normalize beta_(k-3) against beta_(k-1).",
        "arXiv:0801.4310v1, Lemma 5.1, printed pages 12-13",
    ),
    spec(
        "L-DISCREPANCY-INDUCTION", "core_lemma", "critical",
        "Prove the rotated-lattice halfspace-ball discrepancy bound uniformly for growing dimension k by induction.",
        "planned exact Lean Lemma 5.2 signature",
        "An explicit version of |A_bar_k(t)-V_bar_k(t)| <= C*k^(3/2)*V_bar_(k-2)(t).", 35,
        "Recompose the base dimension, signed and halfspace slice branches, recurrence, Euler error, and volume normalization packages.",
        "arXiv:0801.4310v1, Lemma 5.2, printed pages 13-18",
    ),
    spec(
        "B-DISCREPANCY-BASE", "branch", "critical",
        "Establish the five-dimensional discrepancy base used by Lemma 5.2 for every rotated lattice and required halfspace intersection.",
        "planned exact Lean k=5 discrepancy theorem",
        "The induction invariant at dimension five with a uniform constant.", 95,
        "Import or prove the cited dimension-five lattice estimate and transport it to the rotated, halfspace-restricted setting without strengthening its hypotheses.",
        "arXiv:0801.4310v1, Lemma 5.2 proof base; Adhikari [1] boundary",
    ),
    spec(
        "B-DISCREPANCY-SIGNED", "branch", "critical",
        "Handle the slice recurrence when the new coordinate is unrestricted and integer slices range over both signs.",
        "planned exact Lean signed-slice induction branch",
        "The k+1 discrepancy step for k+1<m.", 70,
        "Sum the induction error over symmetric integer slices and compare the volume sum using the Euler package.",
        "arXiv:0801.4310v1, equations (30)-(36), printed pages 15-17",
    ),
    spec(
        "B-DISCREPANCY-HALFSPACE", "branch", "critical",
        "Handle the slice recurrence when the new coordinate is restricted to the nonnegative halfspace.",
        "planned exact Lean halfspace-slice induction branch",
        "The k+1 discrepancy step for k+1>=m.", 75,
        "Use nonnegative integer slices, the shifted Euler interval, and the one-sided integral-error bound.",
        "arXiv:0801.4310v1, equations (32), (34), and (37), printed pages 16-18",
    ),
    spec(
        "L-SLICE-RECURRENCE", "core_lemma", "critical",
        "Express rotated-lattice point counts and halfspace-ball volumes as lower-dimensional coordinate slices.",
        "planned exact Lean lattice/volume slicing identities",
        "Exact finite sums and integrals relating dimensions k+1 and k.", 85,
        "Disintegrate along the final orthonormal coordinate and prove the correct signed or nonnegative index domain in each branch.",
        "arXiv:0801.4310v1, Lemma 5.2 proof, printed pages 15-16",
    ),
    spec(
        "L-VOLUME-SUM-ERROR", "core_lemma", "critical",
        "Compare the lower-dimensional volume slice sum with the next-dimensional ball volume using explicit Euler remainder bounds.",
        "planned exact Lean equations (31)-(34) package",
        "The signed and one-sided volume-sum errors needed by both induction branches.", 90,
        "Differentiate the ball-volume function, apply Euler summation, and bound the sawtooth integral with Lemma 5.5.",
        "arXiv:0801.4310v1, equations (31)-(34), printed pages 16-17",
    ),
    spec(
        "T-DISCREPANCY-MERGE", "terminal", "high",
        "Recompose the exhaustive signed and halfspace slice branches and close the dimension induction constant.",
        "planned exact Lean Lemma 5.2 branch merge",
        "The full discrepancy theorem for every k>=5 and sufficiently large t.", 55,
        "Use the beta_k/beta_(k-1) comparison to absorb both branch errors into one universal induction constant.",
        "arXiv:0801.4310v1, equations (35)-(37), printed pages 17-18",
    ),
    spec(
        "L-EULER-SUM", "bridge", "critical",
        "Euler's summation formula relates a differentiable function's integer sum to its integral, endpoints, and sawtooth derivative integral.",
        "planned exact Lean Lemma 5.3 signature",
        "The exact finite summation identity used in the discrepancy induction.", 80,
        "Formalize the floor sawtooth function and prove the finite interval formula with all endpoint conventions.",
        "arXiv:0801.4310v1, Lemma 5.3, printed page 14; source [7]",
    ),
    spec(
        "L-SAWTOOTH", "core_lemma", "high",
        "Every interval integral of psi(u)=u-floor(u)-1/2 lies between -1/2 and 1.",
        "planned exact Lean Lemma 5.4 signature",
        "The uniform interval integral bound for the Euler remainder.", 55,
        "Split at integer endpoints, integrate the centered affine piece on each unit interval, and bound the two residual pieces.",
        "arXiv:0801.4310v1, Lemma 5.4, printed page 14",
    ),
    spec(
        "L-INTEGRAL-ERROR", "core_lemma", "critical",
        "Bound the weighted sawtooth integral by t^(p/2-1/2) in the ranges required by the discrepancy induction.",
        "planned exact Lean Lemma 5.5 and equation (28) signatures",
        "Signed and shifted interval error bounds for ball-volume derivatives.", 90,
        "Apply mean-value arguments to the monotone factors, invoke the sawtooth interval bound, and handle the [-1/2,0] residual explicitly.",
        "arXiv:0801.4310v1, Lemma 5.5 and equation (28), printed pages 14-15",
    ),
    spec(
        "L-BAD-POINT-UNION", "core_lemma", "critical",
        "Sum hyperplane-section point bounds over h and all short directions to bound nonextreme annulus points.",
        "planned exact Lean equations (13)-(21) union-bound package",
        "An upper bound N strictly below half the large-annulus cardinality.", 90,
        "Partition by the integer inner product h, sum through equations (13)-(20), insert D_hat(g), and compare exponential bases using the epsilon choice.",
        "arXiv:0801.4310v1, equations (13)-(21), printed pages 8-11",
    ),
    spec(
        "L-EPSILON", "core_lemma", "critical",
        "Choose one positive universal epsilon with epsilon+eta(epsilon)<1-log_2(pi*e/6) and make every asymptotic slack explicit.",
        "planned exact Lean universal-epsilon existence theorem",
        "A fixed epsilon and threshold making the bad-point bound at most half the annulus count.", 85,
        "Use eta(epsilon)->0, prove pi*e/6<2, choose positive slack, then absorb polynomial and 2^(O(sqrt(k))) factors after a named k threshold.",
        "arXiv:0801.4310v1, equation (21), printed page 11",
    ),
    spec(
        "C-DIGIT-EMBED", "construction", "critical",
        "Map the convexly independent digit vectors to naturals through base 2y and retain cardinality, range, and progression-freeness.",
        "planned exact Lean base-(2*y) embedding construction",
        "A large progression-free Finset Nat inside the required interval.", 35,
        "Assemble the separately checked injection, no-carry, progression, and range children into one finite-set image package.",
        "arXiv:0801.4310v1, Section 3 embedding reused in Section 4, printed pages 4-6",
    ),
    spec(
        "L-DIGIT-INJECTIVE", "core_lemma", "high",
        "Base-(2y) evaluation is injective on k-tuples with digits in [0,y-1].",
        "planned exact Lean digit-map injectivity theorem",
        "Cardinality preservation for the embedded finite set.", 55,
        "Recover digits recursively by residues modulo 2y and quotient identities under the digit bounds.",
        "arXiv:0801.4310v1, printed page 4; compare pinned Behrend.map_injOn",
    ),
    spec(
        "L-NO-CARRY", "core_lemma", "critical",
        "An arithmetic-progression equality between embedded numbers lifts coordinatewise because sums of two digits are below 2y.",
        "planned exact Lean no-carry transport theorem",
        "Coordinatewise midpoint equality for any embedded arithmetic triple.", 70,
        "Use uniqueness of base-(2y) expansions with digit sums at most 2y-2 to transport the doubled-middle equation coordinatewise.",
        "arXiv:0801.4310v1, printed page 4",
    ),
    spec(
        "L-PROGRESSION-FREE", "core_lemma", "critical",
        "Convex independence of the selected vectors and no-carry transport imply ThreeAPFree for their digit image.",
        "planned exact Lean image progression-free theorem",
        "SourceProgressionFree for the embedded finite set.", 65,
        "Turn an assumed nontrivial arithmetic triple into a nontrivial midpoint relation and contradict convex independence.",
        "arXiv:0801.4310v1, equation (12) conclusion, printed page 6",
    ),
    spec(
        "L-EMBED-RANGE", "core_lemma", "critical",
        "Every embedded digit vector lies in the required zero- or one-based interval after the floored radix choice.",
        "planned exact Lean embedding range theorem",
        "Image containment in range n, then checked translation to Ico 1 (n+1).", 70,
        "Bound the geometric digit sum by (2y)^k-1, compare this with n, and apply the existing one-based extremal transport.",
        "arXiv:0801.4310v1, printed pages 4-6",
    ),
    spec(
        "T-FIXED-INDEX", "terminal", "critical",
        "For every sufficiently large n, construct a one-based progression-free witness with the explicit pre-optimization cardinality lower bound.",
        "planned exact Lean fixed-index Elkin construction theorem",
        "A witness Finset with all structural properties and a lower bound in k, y, and epsilon.", 45,
        "Compose the parameter, annulus, exterior-subset, digit-embedding, and rounding packages for one n.",
        "arXiv:0801.4310v1, Section 4 through equation (12)",
    ),
    spec(
        "L-ASYMPTOTIC-OPTIMIZATION", "core_lemma", "critical",
        "Convert the fixed-index bound sqrt(k)*y^(k-2) into a universal positive multiple of the exact elkinScale n.",
        "planned exact Lean asymptotic optimization theorem",
        "The exact base-two factor 2*sqrt(2), fourth-root logarithm, and universal constants required by WitnessConstructionTarget.", 100,
        "Substitute rounded k and y, expand every O/Omega term into constants, control powers and logarithms, and synchronize all thresholds.",
        "arXiv:0801.4310v1, equations (8), (12), and result (5), printed pages 3, 5-6",
    ),
    spec(
        "T-WITNESS", "terminal", "critical",
        "Package the fixed-index construction and exact asymptotic estimate as WitnessConstructionTarget.",
        "Stage1Instances.THM_M_0958.ObligationTree.ConstructionWitnessPackage",
        "The exact source witness-form proposition consumed by the root transport.", 32,
        "Choose the universal c and common N, then return the constructed set with interval containment, progression-freeness, and exact Real cardinality inequality.",
        "Stage1_Instances/THM-M-0958/Statement.lean:66-73",
    ),
    spec(
        "T-ROOT-COMPOSE", "terminal", "critical",
        "Compose the exact witness package and checked witness-to-root transport into ElkinConstructionTarget.",
        "Stage1Instances.THM_M_0958.ObligationTree.RootComposition",
        "A checked abstract-child composition with the exact root conclusion.", 14,
        "Apply the transport to the witness and introduce no additional premise, axiom, or theorem substitution.",
        "Stage1_Instances/THM-M-0958/ObligationTree.lean#rootComposition_checked",
        human="not_applicable",
    ),
    spec(
        "X-DISCREPANCY-BASE", "bridge", "critical",
        "Resolve the externally cited dimension-five lattice discrepancy theorem and its applicability after rotation and halfspace restriction.",
        "planned exact imported-or-local k=5 discrepancy boundary",
        "A pinned, source-mapped, placeholder-free base theorem for B-DISCREPANCY-BASE.", 75,
        "Locate or formalize the exact base estimate, compare hypotheses, pin its terminal body, and check the required transports.",
        "arXiv:0801.4310v1, Lemma 5.2 proof; Adhikari [1]",
    ),
    spec(
        "X-BEHREND-SUPPORT", "bridge", "high",
        "Classify reusable pinned Behrend box, map, sphere, counting, and optimization declarations without treating the weaker bound as Elkin's theorem.",
        "pinned mathlib Behrend support interfaces",
        "Typed support candidates with zero exact-root credit until their precise child roles are installed.", 55,
        "Reuse only exact declarations whose types match a frozen child; keep the shared terminal body deduplicated and retain the quantitative mismatch guard.",
        "Stage1_Instances/THM-M-0958/anchor-audit.json:M0958-C02,C03",
        machine="informational", human="not_applicable",
        body=f"mathlib4@{MATHLIB_REVISION}:{BEHREND_BLOB}#Behrend.roth_lower_bound",
        root_relevant=False,
    ),
    spec(
        "X-PROBABILITY", "bridge", "high",
        "Pin exact finite-product probability, expectation, variance, Chebyshev, and pigeonhole interfaces used by the construction.",
        "planned pinned mathlib probability/counting boundary",
        "Audited imported primitives with exact hypotheses and transitive trust records.", 65,
        "Search pinned mathlib, choose minimal exact interfaces, and make every conversion between probability and finite cardinality explicit.",
        "arXiv:0801.4310v1, Sections 3-4",
        machine="informational", human="not_applicable",
    ),
    spec(
        "X-SOURCE-ELKIN", "terminal", "critical",
        "Pinpoint every material premise and transition in Elkin's Sections 2-5 and compare the arXiv, SODA, and journal editions.",
        "reviewed primary-source node crosswalk pending",
        "Human-source evidence for the main construction without machine-proof credit.", 95,
        "Admit a lawful immutable edition, map definitions and equations (5)-(37), audit corrections and errata, and obtain independent review.",
        "Michael Elkin, arXiv:0801.4310v1, printed pages 1-18",
        machine="not_applicable",
    ),
    spec(
        "X-SOURCE-COPPERSMITH", "terminal", "high",
        "Record the attribution and supplied proof boundary for Lemma 4.1, credited by Elkin to Don Coppersmith personal communication.",
        "reviewed source/provenance record for Lemma 4.1 pending",
        "A source-fidelity decision for the nonextreme-point witness lemma.", 45,
        "Distinguish Elkin's printed proof from the personal-communication attribution and review the exact assumptions used downstream.",
        "arXiv:0801.4310v1, Lemma 4.1, printed pages 6-7",
        machine="not_applicable",
    ),
    spec(
        "X-SOURCE-DISCREPANCY", "terminal", "critical",
        "Audit the lattice discrepancy references and distinguish their fixed-dimension results from Elkin's growing-dimension extension.",
        "reviewed source crosswalk for Section 5 pending",
        "Primary or authoritative source coverage for the discrepancy base and Euler formula.", 80,
        "Pin [1] and [7], map exact theorems/pages and hypotheses, and review all generalizations to rotations and halfspaces.",
        "arXiv:0801.4310v1, Section 5 references [1] and [7]",
        machine="not_applicable",
    ),
    spec(
        "X-SOURCE-SPECIAL", "terminal", "high",
        "Audit unit-ball volume, Gamma identities, parity bounds, and Stirling inequalities used in Lemma 4.5.",
        "reviewed special-function source/import crosswalk pending",
        "Exact source and formal boundaries for every volume and Gamma estimate.", 60,
        "Map equations (1)-(3), choose pinned formal lemmas or prove explicit variants, and record every normalization constant.",
        "arXiv:0801.4310v1, Section 2 and Lemma 4.5",
        machine="not_applicable",
    ),
    spec(
        "X-PROVENANCE", "certificate", "critical",
        "Bind every local wrapper, imported declaration, terminal body, source blob, revision, license, alias, and transitive dependency without duplicate credit.",
        "content-addressed terminal provenance closure pending",
        "Release-grade conclusion-to-body provenance without mathematical proof credit.", 75,
        "Trace every eventual terminal theorem through wrappers and compositions to unique body identities and classify every source boundary.",
        "Stage1_Instances/THM-M-0958/anchor-audit.json",
        machine="informational", human="not_applicable",
    ),
    spec(
        "X-EVIDENCE", "certificate", "critical",
        "Bind exact recipes, outputs, fingerprints, axiom reports, placeholder checks, freshness, and invalidation inputs for every obligation.",
        "content-addressed evidence bundle pending",
        "Replayable node evidence without independent mathematical proof credit.", 65,
        "Execute each structured recipe against its exact declaration and registry version and reject stale or scope-mismatched results.",
        "Docs/Stage1_Blueprint_rev-5.6.md, Sections 9-10",
        machine="informational", human="not_applicable",
    ),
    spec(
        "X-TRUST", "certificate", "critical",
        "Close the Lean executable, compiled artifact, axiom, unsafe, oracle, supply-chain, SBOM, and offline replay trust boundary.",
        "release TCB and foundation closure pending",
        "Accepted transitive trust evidence without mathematical proof credit.", 75,
        "Recompute all terminal declaration closures in a cold network-denied environment and compare them with the selected profiles.",
        "Docs/Stage1_Blueprint_rev-5.6.md, Sections 7.4 and 10.6",
        machine="informational", human="not_applicable",
    ),
    spec(
        "X-READABLE", "terminal", "high",
        "Write and independently review a complete readable reconstruction of the annulus, bad-point, discrepancy, embedding, and optimization routes.",
        "node-specific readable proof and signed review pending",
        "Readable coverage without machine-proof credit.", 100,
        "Expand each high-risk package into premise-to-inference-to-output steps and reconcile it with exact formal declarations.",
        "Stage1_Instances/THM-M-0958/obligation-tree.md",
        machine="not_applicable", human="not_applicable",
    ),
    spec(
        "X-WORKFLOW", "certificate", "high",
        "Enforce dependency-legal proof, validation, release, freshness, revocation, and independent-verification acceptance.",
        "Stage1 rev-5.6 workflow receipts pending",
        "Workflow acceptance without mathematical proof credit.", 35,
        "Require accepted predecessors before proof adoption and accepted proof, validation, and release receipts before terminal decisions.",
        "Docs/Stage1_Execution_DAG_rev-5.6.json",
        machine="informational", human="not_applicable",
    ),
]


# Only this exact abstract-child harness belongs in the proof graph. All
# source-shaped mathematical expansion remains a logical plan until exact Lean
# child signatures and consuming parent compositions exist.
REQUIRES = {
    oid("ROOT"): [oid("T-ROOT-COMPOSE"), oid("T-WITNESS"), oid("S-WITNESS-TRANSPORT")],
}

CERTIFICATES = {
    oid("ROOT"): "Stage1Instances.THM_M_0958.ObligationTree.root_of_terminal_packages",
}

LOGICAL_PLANS = {
    oid("T-WITNESS"): [oid("T-FIXED-INDEX"), oid("L-ASYMPTOTIC-OPTIMIZATION")],
    oid("T-FIXED-INDEX"): [
        oid("N-PARAMETERS"), oid("B-PARAMETER-MERGE"), oid("L-LARGE-ANNULUS"),
        oid("C-EXTERIOR-SUBSET"), oid("C-DIGIT-EMBED"),
    ],
    oid("N-PARAMETERS"): [
        oid("N-DIMENSION"), oid("N-DIGIT-RADIX"), oid("N-ANNULUS-WIDTH"),
        oid("N-ROUNDING"), oid("N-THRESHOLDS"),
    ],
    oid("B-PARAMETER-MERGE"): [oid("B-Y-INTEGRAL"), oid("B-Y-FLOOR"), oid("N-ROUNDING")],
    oid("L-LARGE-ANNULUS"): [
        oid("C-RANDOM-VARIABLES"), oid("L-MOMENTS"), oid("L-CHEBYSHEV"),
        oid("C-ANNULUS-PARTITION"),
    ],
    oid("L-MOMENTS"): [oid("L-DIGIT-MEAN"), oid("L-DIGIT-VARIANCE")],
    oid("C-EXTERIOR-SUBSET"): [
        oid("L-NONEXTREME-WITNESS"), oid("L-SHORT-DIRECTION-COUNT"),
        oid("L-BAD-POINT-UNION"),
    ],
    oid("L-BAD-POINT-UNION"): [
        oid("L-HYPERPLANE-SECTION"), oid("L-OCTANT-COORDINATES"),
        oid("L-ANNULUS-VOLUME"), oid("L-Q-COUNT"), oid("L-EPSILON"),
    ],
    oid("L-Q-COUNT"): [oid("C-ROTATED-LATTICE"), oid("L-DISCREPANCY-INDUCTION")],
    oid("L-DISCREPANCY-INDUCTION"): [
        oid("B-DISCREPANCY-BASE"), oid("B-DISCREPANCY-SIGNED"),
        oid("B-DISCREPANCY-HALFSPACE"), oid("L-SLICE-RECURRENCE"),
        oid("L-VOLUME-SUM-ERROR"), oid("T-DISCREPANCY-MERGE"),
        oid("L-EULER-SUM"), oid("L-SAWTOOTH"), oid("L-INTEGRAL-ERROR"),
    ],
    oid("B-DISCREPANCY-BASE"): [oid("X-DISCREPANCY-BASE")],
    oid("C-DIGIT-EMBED"): [
        oid("L-DIGIT-INJECTIVE"), oid("L-NO-CARRY"),
        oid("L-PROGRESSION-FREE"), oid("L-EMBED-RANGE"),
    ],
    oid("L-ASYMPTOTIC-OPTIMIZATION"): [
        oid("N-PARAMETERS"), oid("L-EPSILON"), oid("N-THRESHOLDS"),
    ],
}


def edge(edge_id: str, source: str, edge_type: str, target: str,
         reciprocal: str | None = None) -> dict:
    result = {"edge_id": edge_id, "from": source, "type": edge_type, "to": target}
    if reciprocal is not None:
        result["reciprocal_edge_id"] = reciprocal
    return result


def graph(edges: list[dict]) -> dict:
    incoming: dict[str, list[str]] = {}
    outgoing: dict[str, list[str]] = {}
    for item in edges:
        outgoing.setdefault(item["from"], []).append(item["edge_id"])
        incoming.setdefault(item["to"], []).append(item["edge_id"])
    return {"edges": edges, "out": outgoing, "in": incoming}


def build() -> tuple[dict, dict, dict, str]:
    statement_hash = file_digest("Statement.lean")
    anchor_hash = file_digest("anchor-audit.json")
    tree_hash = file_digest("ObligationTree.lean")
    checked_local = {oid("S-WITNESS-TRANSPORT"), oid("S-ROTH-TRANSPORT"), oid("T-ROOT-COMPOSE")}
    exclusions = {
        oid("S-INTERFACE"): "formal_interface_overlay_no_duplicate_machine_or_source_credit_pending_review",
        oid("S-DEFINITIONS"): "formal_definition_overlay_no_duplicate_machine_proof_credit_pending_review",
        oid("S-BOUNDARY"): "formal_boundary_overlay_no_duplicate_machine_proof_credit_pending_review",
        oid("S-WITNESS-TRANSPORT"): "formal_transport_has_no_separate_human_source_eligibility_pending_review",
        oid("S-ROTH-TRANSPORT"): "alternate_encoding_overlay_no_duplicate_root_credit_pending_review",
        oid("S-FOUNDATION"): "foundation_overlay_no_mathematical_proof_credit_pending_review",
        oid("X-BEHREND-SUPPORT"): "nonidentical_support_candidate_no_elkin_root_credit_pending_review",
        oid("X-PROBABILITY"): "import_inventory_overlay_no_mathematical_proof_credit_pending_review",
        oid("X-SOURCE-ELKIN"): "human_source_boundary_only_pending_independent_review",
        oid("X-SOURCE-COPPERSMITH"): "human_source_boundary_only_pending_independent_review",
        oid("X-SOURCE-DISCREPANCY"): "human_source_boundary_only_pending_independent_review",
        oid("X-SOURCE-SPECIAL"): "human_source_boundary_only_pending_independent_review",
        oid("X-PROVENANCE"): "provenance_overlay_no_mathematical_proof_credit_pending_review",
        oid("X-EVIDENCE"): "evidence_overlay_no_mathematical_proof_credit_pending_review",
        oid("X-TRUST"): "trust_overlay_no_mathematical_proof_credit_pending_review",
        oid("X-READABLE"): "readability_boundary_only_pending_independent_review",
        oid("X-WORKFLOW"): "workflow_overlay_no_mathematical_proof_credit_pending_review",
        oid("T-ROOT-COMPOSE"): "formal_composition_has_no_separate_human_source_eligibility_pending_review",
    }
    obligations: list[dict] = []
    nodes: list[dict] = []
    all_ids = [oid(row["short"]) for row in ROWS]
    source_only = {
        oid("X-SOURCE-ELKIN"), oid("X-SOURCE-COPPERSMITH"),
        oid("X-SOURCE-DISCREPANCY"), oid("X-SOURCE-SPECIAL"),
    }
    for row in ROWS:
        identifier = oid(row["short"])
        if identifier in {oid("ROOT"), oid("S-INTERFACE")}:
            fingerprint = f"lean-expression-sha256:{ROOT_EXPRESSION}"
        else:
            fingerprint = "planned:v1:sha256:" + digest([
                identifier, row["kind"], row["claim"], row["formal"], row["output"],
            ])
        body = row["body"]
        if identifier == oid("S-WITNESS-TRANSPORT"):
            body = f"local-source-sha256:{tree_hash}#checkedWitnessToRootTransport"
        elif identifier == oid("T-ROOT-COMPOSE"):
            body = f"local-source-sha256:{tree_hash}#rootComposition_checked"
        elif identifier == oid("S-ROTH-TRANSPORT"):
            body = f"local-source-sha256:{statement_hash}#elkinConstructionTarget_iff_rothNumberTarget"
        obligation = {
            "obligation_id": identifier,
            "statement_fingerprint": fingerprint,
            "kind": row["kind"],
            "root_relevant": row["root_relevant"],
            "machine_eligibility": row["machine"],
            "human_source_eligibility": row["human"],
            "readable_eligibility": row["readable"],
            "risk_class": row["risk"],
            "exclusion_reason": exclusions.get(identifier),
            "terminal_proof_body_id": body,
        }
        obligations.append(obligation)
        if identifier == oid("ROOT"):
            machine_debt = "M3"
            provenance = "none"
        elif identifier in checked_local:
            machine_debt = "M0-L"
            provenance = "local-conditional-interface"
        elif identifier == oid("X-BEHREND-SUPPORT"):
            machine_debt = "M0-W"
            provenance = "anchor-audit:M0958-C02/C03-nonidentical-support"
        elif identifier in {oid("S-INTERFACE"), oid("S-DEFINITIONS"), oid("S-BOUNDARY")}:
            machine_debt = "M3"
            provenance = "statement-phase-provisional"
        else:
            machine_debt = "M4"
            provenance = "pending"
        if identifier in REQUIRES:
            premise_ids = REQUIRES[identifier]
        elif identifier in LOGICAL_PLANS:
            premise_ids = LOGICAL_PLANS[identifier]
        elif identifier in source_only:
            premise_ids = ["frozen-source-context"]
        else:
            premise_ids = ["frozen-formal-context"]
        ledger = [{
            "step_id": f"STEP-{identifier}-01",
            "premise_ids": premise_ids,
            "inference": row["inference"],
            "source_locator": row["locator"],
            "output": row["output"],
            "outgoing_use": "Only a declared proof parent or typed non-proof edge may consume this exact output.",
        }]
        owned_sources: list[str] = []
        if identifier in {oid("S-WITNESS-TRANSPORT"), oid("T-ROOT-COMPOSE")}:
            owned_sources = ["Stage1_Instances/THM-M-0958/ObligationTree.lean"]
        elif identifier in {oid("S-INTERFACE"), oid("S-DEFINITIONS"), oid("S-BOUNDARY"), oid("S-ROTH-TRANSPORT")}:
            owned_sources = ["Stage1_Instances/THM-M-0958/Statement.lean"]
        nodes.append({
            "node_id": f"{THEOREM}-{row['short']}",
            "obligation_id": identifier,
            "kind": row["kind"],
            "human_statement": row["claim"],
            "formal_target": row["formal"],
            "output": row["output"],
            "human_debt": "H1",
            "machine_debt": machine_debt,
            "readability_debt": "R4",
            "evidence_ids": [],
            "source_crosswalk_id": (
                "not-applicable-pending-review" if row["human"] == "not_applicable"
                else "arxiv-0801.4310v1-node-map-pending-independent-review"
            ),
            "provenance_id": provenance,
            "foundation_profile": "lean4-dependent-type-theory; propext/Classical.choice/Quot.sound policy review pending",
            "tcb_profile": "lean-4.29.0+mathlib-8a178386; transitive closure and independent replay pending",
            "computation_record": "none; no native computation, solver, oracle, experiment, or unchecked certificate is credited",
            "step_budget": row["budget"],
            "semantic_step_ledger": ledger,
            "public_readable_target": f"Stage1_Instances/THM-M-0958/obligation-tree.md#{identifier.lower()}",
            "validation_spec_id": f"VAL-{identifier}",
            "status_boundary": "Frozen architecture or conditional interface only; no accepted M0 root, H0/R0 closure, audit completion, or theorem completion.",
            "task_ids": [ITEM, "S56-M-0958-PROOF"],
            "owned_sources": owned_sources,
            "owner": "THM-M-0958 proof lane",
            "reviewer": "independent Stage1 integration lane",
            "validity": {
                "validated_at": "2026-07-13" if identifier in checked_local else None,
                "review_due": "before proof acceptance",
                "invalidation_inputs": [
                    "Statement.lean", "anchor-audit.json", "obligation-registry.json",
                    "typed-graphs.json", "source-node map", "toolchain and dependency pins",
                ],
                "revocation_state": "provisional" if identifier in checked_local else "open",
            },
        })

    fields = (
        "obligation_id", "statement_fingerprint", "kind", "root_relevant",
        "machine_eligibility", "human_source_eligibility", "readable_eligibility",
        "risk_class", "exclusion_reason", "terminal_proof_body_id",
    )
    projection = [{key: row[key] for key in fields} for row in obligations]
    denominator = digest(projection)
    registry = {
        "schema_version": "stage1-obligation-registry/1.0",
        "item_id": ITEM,
        "theorem_id": THEOREM,
        "registry_id": REGISTRY_ID,
        "registry_version": 1,
        "frozen_at": "2026-07-13T23:50:00+08:00",
        "freeze_basis": "The exact elaborated Elkin statement, the bounded immutable anchor audit, and the source-shaped Sections 3-5 route. Eligibility and denominators are frozen without observing or accepting proof closure.",
        "frozen_against_statement_sha256": statement_hash,
        "frozen_against_anchor_audit_sha256": anchor_hash,
        "architecture_source_sha256": tree_hash,
        "root_obligation_id": oid("ROOT"),
        "denominator_sha256": denominator,
        "frozen_denominators": {
            "inventory": all_ids,
            "required_machine": [row["obligation_id"] for row in obligations if row["machine_eligibility"] == "required"],
            "required_human_source": [row["obligation_id"] for row in obligations if row["human_source_eligibility"] == "required"],
            "required_readable": [row["obligation_id"] for row in obligations if row["readable_eligibility"] == "required"],
            "informational_overlays": [row["obligation_id"] for row in obligations if row["machine_eligibility"] == "informational"],
        },
        "mandatory_layers": {
            "S": [oid(short) for short in ("S-INTERFACE", "S-DEFINITIONS", "S-BOUNDARY", "S-WITNESS-TRANSPORT", "S-ROTH-TRANSPORT", "S-FOUNDATION")],
            "N": [oid(short) for short in ("N-PARAMETERS", "N-DIMENSION", "N-DIGIT-RADIX", "N-ANNULUS-WIDTH", "N-ROUNDING", "N-THRESHOLDS")],
            "B": [oid(short) for short in ("B-Y-INTEGRAL", "B-Y-FLOOR", "B-PARAMETER-MERGE", "B-DISCREPANCY-BASE", "B-DISCREPANCY-SIGNED", "B-DISCREPANCY-HALFSPACE")],
            "C": [row["obligation_id"] for row in obligations if row["kind"] == "construction"],
            "L": [row["obligation_id"] for row in obligations if row["kind"] in {"core_lemma", "bridge"} and not row["obligation_id"].startswith("M0958-X-")],
            "X": [row["obligation_id"] for row in obligations if row["obligation_id"].startswith("M0958-X-")],
            "T": [oid(short) for short in ("T-FIXED-INDEX", "T-WITNESS", "T-ROOT-COMPOSE", "T-DISCREPANCY-MERGE")],
        },
        "layer_exclusions": {
            "additional_symmetry_sign_or_representative_normalization": {
                "status": "not_applicable_pending_independent_approval",
                "reason": "The proof uses explicit coordinate order, an adapted orthonormal basis, and signed/nonnegative discrepancy branches; no further quotient representative or symmetry normalization is used.",
            },
            "external_computation": {
                "status": "not_applicable_pending_independent_approval",
                "reason": "The selected source route is analytic and combinatorial. No finite search, native evaluator, solver, oracle, numerical experiment, or external certificate is credited.",
            },
        },
        "delta_policy": "Any target correction, split, merge, exclusion, eligibility change, or proof-route replacement requires registry version 2 and an append-only old/new ID delta.",
        "obligations": obligations,
        "append_only_delta": [],
        "status_observed_after_freeze": {
            "accepted_closed_obligations": [],
            "provisionally_checked_interfaces": [oid("S-WITNESS-TRANSPORT"), oid("T-ROOT-COMPOSE")],
            "accepted_root_machine_debt": "M3",
            "candidate_route": "No exact Elkin proof candidate exists in the frozen inventory; pinned Behrend is nonidentical support only.",
        },
        "status_boundary": "Architecture only; no obligation is accepted closed and both terminal decisions remain false.",
    }

    proof_edges: list[dict] = []
    for parent, children in REQUIRES.items():
        for child in children:
            request = f"REQ-{parent}-{child}"
            compose = f"CMP-{child}-{parent}"
            proof_edges.append(edge(request, parent, "proof_requires", child, compose))
            proof_edges.append(edge(compose, child, "composes", parent, request))
    refinement_edges = [
        edge("REF-ROOT-INTERFACE", oid("ROOT"), "expository_decomposition", oid("S-INTERFACE")),
        edge("REF-ROOT-DEFINITIONS", oid("ROOT"), "expository_decomposition", oid("S-DEFINITIONS")),
        edge("REF-ROOT-BOUNDARY", oid("ROOT"), "expository_decomposition", oid("S-BOUNDARY")),
        edge("REF-ROOT-ROTH", oid("ROOT"), "equivalent_to", oid("S-ROTH-TRANSPORT")),
    ]
    for parent, children in LOGICAL_PLANS.items():
        for child in children:
            refinement_edges.append(edge(f"LOG-{parent}-{child}", parent, "logical_decomposition", child))
    provenance_edges = [
        edge("PROV-ROOT", oid("X-PROVENANCE"), "provenance_of", oid("ROOT")),
        edge("PROV-WITNESS", oid("X-PROVENANCE"), "provenance_of", oid("T-WITNESS")),
        edge("PROV-TRANSPORT", oid("X-PROVENANCE"), "provenance_of", oid("S-WITNESS-TRANSPORT")),
        edge("PROV-BEHREND", oid("X-PROVENANCE"), "provenance_of", oid("X-BEHREND-SUPPORT")),
        edge("SRC-ELKIN-CONSTRUCTION", oid("T-FIXED-INDEX"), "source_map", oid("X-SOURCE-ELKIN")),
        edge("SRC-ELKIN-DISCREPANCY", oid("L-DISCREPANCY-INDUCTION"), "source_map", oid("X-SOURCE-ELKIN")),
        edge("SRC-COPPERSMITH", oid("L-NONEXTREME-WITNESS"), "source_map", oid("X-SOURCE-COPPERSMITH")),
        edge("SRC-DISCREPANCY", oid("X-DISCREPANCY-BASE"), "source_map", oid("X-SOURCE-DISCREPANCY")),
        edge("SRC-SPECIAL", oid("L-ANNULUS-VOLUME"), "source_map", oid("X-SOURCE-SPECIAL")),
    ]
    evidence_edges = [
        edge("EVIDENCE-STATEMENT", oid("X-EVIDENCE"), "evidence_for", oid("S-INTERFACE")),
        edge("EVIDENCE-TRANSPORT", oid("X-EVIDENCE"), "evidence_for", oid("S-WITNESS-TRANSPORT")),
        edge("EVIDENCE-COMPOSITION", oid("X-EVIDENCE"), "evidence_for", oid("T-ROOT-COMPOSE")),
        edge("EVIDENCE-ANCHOR", oid("X-EVIDENCE"), "evidence_for", oid("X-BEHREND-SUPPORT")),
    ]
    trust_edges = [
        edge("TRUST-FOUNDATION", oid("ROOT"), "trusts", oid("S-FOUNDATION")),
        edge("TRUST-RELEASE", oid("ROOT"), "trusts", oid("X-TRUST")),
        edge("TRUST-COMPOSITION", oid("T-ROOT-COMPOSE"), "trusts", oid("X-TRUST")),
        edge("TRUST-PROBABILITY", oid("L-CHEBYSHEV"), "trusts", oid("X-PROBABILITY")),
    ]
    documentation_edges = [
        edge("DOC-ROOT", oid("X-READABLE"), "documents", oid("ROOT")),
        edge("DOC-CONSTRUCTION", oid("X-READABLE"), "documents", oid("T-FIXED-INDEX")),
        edge("DOC-DISCREPANCY", oid("X-READABLE"), "documents", oid("L-DISCREPANCY-INDUCTION")),
        edge("DOC-OPTIMIZATION", oid("X-READABLE"), "documents", oid("L-ASYMPTOTIC-OPTIMIZATION")),
        edge("DOC-SOURCE", oid("X-SOURCE-ELKIN"), "documents", oid("ROOT")),
    ]
    workflow_nodes = [
        "S56-M-0958-STATEMENT", "S56-M-0958-ANCHOR_AUDIT", ITEM,
        "S56-M-0958-PROOF", "S56-M-0958-VALIDATION", "S56-M-0958-RELEASE",
    ]
    workflow_edges = [
        edge(f"FLOW-{index}", workflow_nodes[index], "workflow_depends_on", workflow_nodes[index - 1])
        for index in range(1, len(workflow_nodes))
    ]
    graphs = {
        "proof": graph(proof_edges),
        "refinement": graph(refinement_edges),
        "provenance": graph(provenance_edges),
        "evidence": graph(evidence_edges),
        "trust": graph(trust_edges),
        "documentation": graph(documentation_edges),
        "workflow": graph(workflow_edges),
    }
    fingerprints = {row["obligation_id"]: row["statement_fingerprint"] for row in obligations}
    certificates = [{
        "certificate_id": f"CERT-{parent}",
        "parent_obligation_id": parent,
        "parent_statement_fingerprint": fingerprints[parent],
        "required_child_ids": children,
        "required_child_statement_fingerprints": {child: fingerprints[child] for child in children},
        "declaration": CERTIFICATES[parent],
        "certificate_kind": "lean_abstract_child_harness",
        "introduces_undeclared_premises": False,
        "status": "provisionally_elaborated_not_accepted",
    } for parent, children in REQUIRES.items()]
    unverified = [{
        "plan_id": f"DECOMP-{parent}",
        "parent_obligation_id": parent,
        "planned_child_ids": children,
        "source_locator": next(row["locator"] for row in ROWS if oid(row["short"]) == parent),
        "status": "source_body_decomposition_unverified_as_child_to_parent_composition",
        "required_future_certificate": "An exact Lean abstract-child harness must bind these fingerprints and consume every child before parent closure.",
    } for parent, children in LOGICAL_PLANS.items()]
    bundle = {
        "schema_version": "stage1-typed-graphs/1.0",
        "item_id": ITEM,
        "theorem_id": THEOREM,
        "registry_id": REGISTRY_ID,
        "registry_denominator_sha256": denominator,
        "root_node_id": oid("ROOT"),
        "edge_direction": "proof_requires runs parent to child and reciprocal composes runs child to parent; logical plans run parent to child.",
        "nodes": nodes,
        "graphs": graphs,
        "workflow_task_nodes": workflow_nodes,
        "composition_certificates": certificates,
        "unverified_decomposition_plans": unverified,
        "closure_boundary": {
            "accepted_closed_obligations": [],
            "root_closed": False,
            "accepted_root_machine_debt": "M3",
            "audit_complete": False,
            "theorem_complete": False,
            "minimal_open_machine_proof_cut_sets": [[oid("T-WITNESS")]],
            "remaining_root_cut_set": [
                oid("T-WITNESS"), oid("X-SOURCE-ELKIN"), oid("S-FOUNDATION"),
                oid("X-PROVENANCE"), oid("X-EVIDENCE"), oid("X-TRUST"),
                oid("X-READABLE"), oid("X-WORKFLOW"),
            ],
            "reason": "The exact witness package and every substantive Elkin construction child remain open; checked transports and conditional composition do not prove them.",
        },
    }
    declaration_map = {
        oid("ROOT"): ["Stage1Instances.THM_M_0958.ElkinConstructionTarget"],
        oid("S-WITNESS-TRANSPORT"): ["Stage1Instances.THM_M_0958.ObligationTree.checkedWitnessToRootTransport"],
        oid("S-ROTH-TRANSPORT"): ["Stage1Instances.THM_M_0958.elkinConstructionTarget_iff_rothNumberTarget"],
        oid("T-ROOT-COMPOSE"): [
            "Stage1Instances.THM_M_0958.ObligationTree.rootComposition_checked",
            "Stage1Instances.THM_M_0958.ObligationTree.root_of_terminal_packages",
        ],
    }
    recipes = []
    for identifier in all_ids:
        recipes.append({
            "recipe_id": f"VAL-{identifier}",
            "cwd": ".",
            "argv": ["python3", "-B", "Stage1_Instances/THM-M-0958/check_obligation_tree.py"],
            "env_allowlist": {"LC_ALL": "C", "TZ": "UTC"},
            "timeout_seconds": 300,
            "network_policy": "denied",
            "expected_exit": 0,
            "expected_outputs": [{
                "path_or_stream": "stdout",
                "semantic_hash_policy": "contains PASS THM-M-0958 obligation tree and accepted obligations 0",
            }],
            "covered_obligation_ids": [identifier],
            "covered_declarations": declaration_map.get(identifier, []),
            "closure_credit": False,
        })
    validation = {
        "schema_version": "stage1-validation-specs/1.0",
        "item_id": ITEM,
        "theorem_id": THEOREM,
        "recipes": recipes,
    }
    lines = [
        "# THM-M-0958 frozen obligation architecture", "", "## Freeze boundary", "",
        f"Registry version 1 freezes {len(obligations)} canonical obligations before proof execution.",
        "The denominator binds the exact statement and anchor-audit inputs. The source-shaped route",
        "expands Elkin's thin annulus, exterior-point bound, growing-dimension lattice discrepancy,",
        "digit embedding, rounding, and asymptotic optimization. No obligation is accepted closed.",
        "", "## Proof route", "", "```text",
        "M0958-ROOT exact ElkinConstructionTarget",
        "`-- M0958-T-WITNESS exact WitnessConstructionTarget [open cut]",
        "    |-- parameter and floor/threshold normalization",
        "    |-- large thin-annulus construction",
        "    |-- exterior-point selection and bad-point union bound",
        "    |   `-- rotated-lattice discrepancy, Lemmas 5.1-5.5",
        "    |-- base-(2y) injective no-carry embedding",
        "    `-- exact base-two asymptotic optimization",
        "```", "",
        "The proof graph contains only the kernel-checked abstract-child root harness. All internal",
        "source relations are typed logical decompositions until proof work supplies exact child",
        "signatures and consuming composition declarations. Source, evidence, provenance, trust,",
        "documentation, and workflow edges cannot close a mathematical premise.", "", "## Node ledger", "",
    ]
    node_by_id = {node["obligation_id"]: node for node in nodes}
    for obligation in obligations:
        identifier = obligation["obligation_id"]
        node = node_by_id[identifier]
        lines += [
            f"### {identifier.lower()}", "",
            f"Kind: `{node['kind']}`. Risk: `{obligation['risk_class']}`. Step budget: `{node['step_budget']}`.", "",
            f"Claim: {node['human_statement']}", "",
            f"Formal target: `{node['formal_target']}`", "",
            f"Output: {node['output']}", "", "Semantic ledger:", "",
        ]
        for index, step in enumerate(node["semantic_step_ledger"], 1):
            lines.append(f"{index}. `{step['step_id']}`: {step['inference']} Output: {step['output']}")
        lines += ["", f"Boundary: {node['status_boundary']}", ""]
    lines += [
        "## Closure boundary", "",
        "The minimal open machine-proof cut is `M0958-T-WITNESS`. Primary-source H0, readable R0,",
        "full provenance/evidence/trust closure, hermetic replay, independent verification, master",
        "acceptance, AUDIT-Z, and THEOREM-Z remain open. The root stays `[H1, M3, R4]`.", "",
    ]
    return registry, bundle, validation, "\n".join(lines)


def serialized(value: dict) -> bytes:
    return (json.dumps(value, indent=2, ensure_ascii=True) + "\n").encode()


def main() -> None:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()
    registry, bundle, validation, readable = build()
    outputs = {
        "obligation-registry.json": serialized(registry),
        "typed-graphs.json": serialized(bundle),
        "validation-specs.json": serialized(validation),
        "obligation-tree.md": readable.encode(),
    }
    for name, data in outputs.items():
        path = HERE / name
        if args.check:
            if not path.is_file() or path.read_bytes() != data:
                raise SystemExit(f"stale generated artifact: {name}")
        else:
            path.write_bytes(data)
    action = "checked" if args.check else "wrote"
    edge_count = sum(len(value["edges"]) for value in bundle["graphs"].values())
    print(f"{action} {len(registry['obligations'])} obligations and {edge_count} typed edges")
    print(f"registry denominator sha256: {registry['denominator_sha256']}")


if __name__ == "__main__":
    main()
