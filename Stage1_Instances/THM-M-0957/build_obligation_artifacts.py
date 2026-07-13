#!/usr/bin/env python3
"""Deterministically build the THM-M-0957 obligation freeze."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ITEM = "S56-M-0957-OBLIGATION_TREE"
THEOREM = "THM-M-0957"
PREFIX = "M0957-"
ROOT_EXPRESSION = "e611db43ce6f3419553e3ebe0fe85a3ce89e4d3930b3842f5a09be8a7683d2ed"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_BLOB = "7d3eb0e603040dcd72fe35e39c82f4d615b3e254"
MATHLIB_BODY = f"mathlib4@{MATHLIB_REVISION}:{MATHLIB_BLOB}"
GRAPH_NAMES = (
    "proof", "refinement", "provenance", "evidence", "trust",
    "documentation", "workflow",
)
TASK_IDS = (
    "S56-M-0957-INTAKE",
    "S56-M-0957-STATEMENT",
    "S56-M-0957-ANCHOR_AUDIT",
    ITEM,
    "S56-M-0957-PROOF",
    "S56-M-0957-VALIDATION",
    "S56-M-0957-RELEASE",
)


def oid(short: str) -> str:
    return PREFIX + short


def digest(value: object) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def row(
    short: str,
    kind: str,
    risk: str,
    claim: str,
    formal: str,
    result: str,
    inference: str,
    locator: str,
    budget: int,
    machine: str = "required",
    human: str = "required",
    body: str | None = None,
) -> tuple:
    return (
        short, kind, risk, claim, formal, result, inference, locator, budget,
        machine, human, body,
    )


ROWS = (
    row(
        "ROOT", "root", "critical",
        "For every positive real epsilon, eventually the historical sharp real-power lower bound is strictly below rothNumberNat (N + 1).",
        "Stage1Instances.THM_M_0957.BehrendConstructionTarget",
        "The exact frozen inclusive-interval historical proposition.",
        "Consume the exact three-package assembly through the checked root certificate.",
        "Statement.lean:32-38; ObligationTree.lean#root_of_exactAssembly", 4,
    ),
    row(
        "S-TARGET", "definition", "critical",
        "Freeze the epsilon-dependent threshold, strict Real.rpow inequality, natural-log convention, and inclusive N + 1 extremal index.",
        "Stage1Instances.THM_M_0957.BehrendConstructionTarget",
        "The elaborated root interface with expression fingerprint e611db43...d2ed.",
        "Preserve every binder, coercion, constant, denominator, strictness, and endpoint.",
        "Statement.lean:25-38; statement.json", 14,
        machine="informational", human="not_applicable",
    ),
    row(
        "S-PREDICATE", "transport", "high",
        "The source exclusion of pairwise-distinct natural triples is equivalent to mathlib's ThreeAPFree predicate.",
        "Stage1Instances.THM_M_0957.sourceThreeAPFree_iff_threeAPFree",
        "A checked predicate transport in both directions.",
        "Use cancellation to show any progression with two equal natural terms is constant.",
        "Statement.lean:54-75", 16, human="not_applicable",
        body="local:Stage1_Instances/THM-M-0957/Statement.lean#sourceThreeAPFree_iff_threeAPFree",
    ),
    row(
        "S-EXTREMAL", "transport", "critical",
        "The Roth-extremum root is equivalent to the direct source-predicate finite-set formulation on {0,...,N}.",
        "Stage1Instances.THM_M_0957.behrendConstructionTarget_iff_finiteSet",
        "The checked extremal-to-existential transport.",
        "Use rothNumberNat_spec in one direction and ThreeAPFree.le_rothNumberNat in the other.",
        "Statement.lean:77-100", 24, human="not_applicable",
        body="local:Stage1_Instances/THM-M-0957/Statement.lean#behrendConstructionTarget_iff_finiteSet",
    ),
    row(
        "S-FINITE-TARGET", "definition", "high",
        "The direct finite-set formulation preserves the inclusive interval, literal source predicate, and cardinality lower bound.",
        "Stage1Instances.THM_M_0957.BehrendFiniteSetTarget",
        "The exact alternate proposition with a checked iff witness for the historical root.",
        "Expose the alternate proposition; S-EXTREMAL supplies its checked iff witness.",
        "Statement.lean:40-54", 14, machine="informational",
        human="not_applicable",
    ),
    row(
        "S-BOUNDARY", "branch", "high",
        "Retain epsilon > 0, N = 0/1 as eventually excluded cases, strict inequality, pairwise-distinct progressions, Real.log, Real.sqrt, and inclusive range N + 1.",
        "statement mutation and boundary fixtures",
        "A frozen boundary policy without weakening the root, pending independent review.",
        "Kill removed-positivity, rational-domain, uniform-threshold, and exclusive-interval mutations.",
        "Statement.lean:102-142; statement-receipt.json", 18,
        machine="informational", human="not_applicable",
    ),
    row(
        "S-FOUNDATION", "certificate", "critical",
        "Audit classical choice, quotient soundness, propositional extensionality, Real.rpow/log/sqrt, the Lean kernel, and the no-oracle policy.",
        "Lean 4.29.0 and pinned mathlib transitive trust packet",
        "A planned foundation, computation, and TCB boundary pending acceptance.",
        "Recompute declarations, artifacts, executables, axioms, and oracle boundaries transitively.",
        "anchor-audit.json immutable_environment and trust_audit", 42,
        machine="informational", human="not_applicable",
    ),
    row(
        "T-ASSEMBLE", "terminal", "critical",
        "Pair the exact quantitative construction package, sharp parameter package, and inclusive-index monotonicity package.",
        "Stage1Instances.THM_M_0957_ObligationTree.ExactAssembly",
        "All and only the premises consumed by the canonical root composition.",
        "Form the conjunction and pass it to the exact root certificate.",
        "ObligationTree.lean#exactAssembly_of_children", 4,
    ),
    row(
        "T-CONSTRUCTION", "bridge", "critical",
        "For every admissible n and d, d^(n-2)/n is at most rothNumberNat ((2*d-1)^n).",
        "Stage1Instances.THM_M_0957_ObligationTree.QuantitativeConstructionPackage",
        "The exact quantitative construction premise used by the root.",
        "Invoke the pinned Behrend.bound_aux body without the later constant-four optimization.",
        "Behrend.lean:267-271; ObligationTree.lean#pinnedQuantitativeConstruction", 3,
        body=MATHLIB_BODY + "#Behrend.bound_aux",
    ),
    row(
        "C-BOX-SPHERE", "construction", "high",
        "Construct the digit box and its integer squared-radius fibers.",
        "Behrend.box; Behrend.sphere",
        "Finite candidate point sets indexed by n, d, and k.",
        "Filter the finite digit box by the sum-of-squares equation.",
        "Behrend.lean:96-118", 18, machine="informational",
        body=MATHLIB_BODY + "#Behrend.sphere",
    ),
    row(
        "L-SPHERE-FREE", "bridge", "critical",
        "An integer sphere contains only trivial three-term arithmetic progressions.",
        "Behrend.threeAPFree_sphere",
        "ThreeAPFree (Behrend.sphere n d k).",
        "Transport into a strictly convex Euclidean sphere and use its frontier geometry.",
        "Behrend.lean:56-79,174-183", 38, machine="informational",
        body=MATHLIB_BODY + "#Behrend.threeAPFree_sphere",
    ),
    row(
        "C-DIGIT-MAP", "construction", "critical",
        "Encode digit vectors as natural numbers in base 2*d-1, injectively on the box and with a controlled range.",
        "Behrend.map; Behrend.map_injOn; Behrend.map_le_of_mem_box",
        "An additive, box-injective encoding into an initial natural interval.",
        "Prove digit uniqueness recursively and bound the geometric digit sum.",
        "Behrend.lean:131-172", 48, machine="informational",
        body=MATHLIB_BODY + "#Behrend.map_injOn",
    ),
    row(
        "L-IMAGE-FREE", "bridge", "critical",
        "The digit-map image of the integer sphere is ThreeAPFree.",
        "Behrend.threeAPFree_image_sphere",
        "A finite progression-free set of natural numbers.",
        "Combine additive Freiman preservation, digit injectivity, and the sphere theorem.",
        "Behrend.lean:185-195", 26, machine="informational",
        body=MATHLIB_BODY + "#Behrend.threeAPFree_image_sphere",
    ),
    row(
        "L-EXTREMAL-CARD", "bridge", "critical",
        "The cardinality of every digit sphere is bounded by rothNumberNat ((2*d-1)^n).",
        "Behrend.card_sphere_le_rothNumberNat",
        "The construction-to-extremal cardinal inequality.",
        "Use the progression-free digit image, its range bound, and image-card injectivity.",
        "Behrend.lean:211-224", 26, machine="informational",
        body=MATHLIB_BODY + "#Behrend.card_sphere_le_rothNumberNat",
    ),
    row(
        "L-LARGE-SPHERE", "bridge", "critical",
        "Some squared-radius fiber contains at least d^n/(n*d^2) integer points.",
        "Behrend.exists_large_sphere_aux; Behrend.exists_large_sphere",
        "A large sphere selected by finite pigeonhole.",
        "Bound the squared-radius range and average the box points across its fibers.",
        "Behrend.lean:236-261", 38, machine="informational",
        body=MATHLIB_BODY + "#Behrend.exists_large_sphere",
    ),
    row(
        "L-IMPLICIT-BOUND", "bridge", "critical",
        "Combine a large sphere and its Roth-number cardinal bound, then cancel d^2 to obtain d^(n-2)/n.",
        "Behrend.bound_aux'; Behrend.bound_aux",
        "The exact QuantitativeConstructionPackage.",
        "Select the large fiber, compose inequalities, and normalize powers under d != 0 and 2 <= n.",
        "Behrend.lean:263-271", 18, machine="informational",
        body=MATHLIB_BODY + "#Behrend.bound_aux",
    ),
    row(
        "N-SHARP-DIMENSION", "normalization", "critical",
        "Select ceil(sqrt(2*log(N+1)/log 2)) and prove it is eventually at least two and within one of its real proxy.",
        "Stage1Instances.THM_M_0957_ObligationTree.DimensionControlPackage",
        "Eventual DimensionControlAt N.",
        "Use logarithmic growth, positivity of log 2, sqrt bounds, and ceil inequalities.",
        "ObligationTree.lean#sharpDimension; Behrend 1946 p.332", 44,
    ),
    row(
        "L-RADIX-NONZERO", "core_lemma", "critical",
        "Select floor((N+1)^(1/n)/2) for the sharp dimension and prove it is eventually nonzero.",
        "Stage1Instances.THM_M_0957_ObligationTree.RadixNonzeroPackage",
        "Eventual sharpRadix N not equal to zero.",
        "Establish the real proxy exceeds one and apply floor positivity.",
        "ObligationTree.lean#sharpRadix; Behrend 1946 p.332", 36,
    ),
    row(
        "T-PARAM-ADMISSIBLE", "terminal", "critical",
        "Combine rounded-dimension control and eventual radix nonzeroness under one threshold.",
        "Stage1Instances.THM_M_0957_ObligationTree.ParameterAdmissibilityPackage",
        "Eventual radix nonzeroness and dimension at least two.",
        "Take the maximum of the dimension and radix thresholds and project both conclusions.",
        "ObligationTree.lean#parameterAdmissibility_of_dimension_and_radix", 5,
        body="local:Stage1_Instances/THM-M-0957/ObligationTree.lean#parameterAdmissibility_of_dimension_and_radix",
    ),
    row(
        "L-RADIX-FLOOR", "core_lemma", "critical",
        "Control the loss from replacing the real radix proxy by the floored natural radix.",
        "Stage1Instances.THM_M_0957_ObligationTree.RadixFloorPackage",
        "Eventually 0 <= radixProxy N <= sharpRadix N as reals.",
        "Use floor inequalities after proving the unrounded radix is sufficiently large.",
        "ObligationTree.lean#radixProxy; Behrend 1946 p.332", 42,
    ),
    row(
        "L-AMBIENT-FIT", "core_lemma", "critical",
        "The selected digit image lies within an interval of size at most N + 1.",
        "Stage1Instances.THM_M_0957_ObligationTree.AmbientFitPackage",
        "Eventually (2*sharpRadix N-1)^sharpDimension N <= N+1.",
        "Bound the floor by the real radix, take powers, and cancel the reciprocal exponent.",
        "ObligationTree.lean#AmbientFitPackage", 42,
    ),
    row(
        "N-RPOW-EXP", "normalization", "critical",
        "Rewrite the historical real power into an exponential loss expression for sufficiently large N.",
        "Stage1Instances.THM_M_0957_ObligationTree.RpowNormalizationPackage",
        "The historical lower is at most exp(log N-(c+epsilon)*sqrt(log N)).",
        "Use Real.rpow_def_of_pos, log positivity, and sqrt(log N)^2 = log N.",
        "ObligationTree.lean#RpowNormalizationPackage", 34,
    ),
    row(
        "L-OPTIMAL-EXPONENT", "core_lemma", "critical",
        "For the rounded sharp dimension, absorb reciprocal-dimension, power, logarithmic, and fixed losses into delta*sqrt(log N) and obtain coefficient 2*sqrt(2*log 2)+delta.",
        "Stage1Instances.THM_M_0957_ObligationTree.OptimalExponentBridgePackage",
        "The central exponential lower bound at the real radix proxy.",
        "Expand log(radixProxy^(n-2)/n), balance 2*log N/n with n*log 2, and dominate all rounding and log n losses eventually.",
        "Behrend 1946 p.332; exact modern inequality proof pending", 100,
    ),
    row(
        "L-PROXY-LOG", "core_lemma", "high",
        "The floored-radix proxy is eventually positive and its logarithm retains the main log N / n - log 2 term up to one quarter of the positive slack.",
        "Stage1Instances.THM_M_0957_ObligationTree.ProxyLogLowerPackage",
        "Eventual proxy positivity and logarithmic lower bound under DimensionControlAt N.",
        "Control log(N+1), the real radix before flooring, and the subtraction by one.",
        "Behrend 1946 p.332; exact proxy logarithm proof pending", 64,
    ),
    row(
        "L-PROXY-RPOW-IDENTITY", "normalization", "normal",
        "Express radixProxy N + 1 as the exponential of log(N+1)/n - log 2 for the selected positive dimension.",
        "Stage1Instances.THM_M_0957_ObligationTree.ProxyRpowIdentityPackage",
        "The exact exponential identity immediately above the subtraction-by-one proxy.",
        "Use dimension positivity, Real.rpow_def_of_pos, logarithm rules, and division by two.",
        "ObligationTree.lean#ProxyRpowIdentityPackage; Behrend 1946 p.332", 34,
    ),
    row(
        "L-PROXY-SLACK", "core_lemma", "high",
        "Eventually the allocated quarter-slack dominates both the N-to-N+1 change and subtraction by one.",
        "Stage1Instances.THM_M_0957_ObligationTree.ProxySlackAbsorptionPackage",
        "An exponential comparison retaining enough additive room for the proxy subtraction.",
        "Compare log N with log(N+1) and use exponential growth to absorb the fixed additive one.",
        "ObligationTree.lean#ProxySlackAbsorptionPackage; Behrend 1946 p.332", 54,
    ),
    row(
        "L-RECIPROCAL-LOSS", "core_lemma", "high",
        "The reciprocal-dimension loss 2*log N/n is eventually bounded by its balanced square-root term plus one eighth of the slack.",
        "Stage1Instances.THM_M_0957_ObligationTree.ReciprocalDimensionLossPackage",
        "The reciprocal half of the balanced exponent estimate.",
        "Use the lower ceiling control for n and positivity of log 2 and log N.",
        "Behrend 1946 p.332; exact reciprocal loss proof pending", 56,
    ),
    row(
        "L-RECIPROCAL-CORE", "core_lemma", "high",
        "The ceiling-selected dimension gives the no-slack reciprocal half of the balanced exponent bound.",
        "Stage1Instances.THM_M_0957_ObligationTree.ReciprocalBalancedCorePackage",
        "The exact reciprocal balance before adding positive delta slack.",
        "Use the lower ceiling inequality, log N <= log(N+1), and positivity to divide and square safely.",
        "ObligationTree.lean#ReciprocalBalancedCorePackage; Behrend 1946 p.332", 48,
    ),
    row(
        "L-LINEAR-LOSS", "core_lemma", "high",
        "The linear dimension loss n*log 2 is eventually bounded by its balanced square-root term plus one eighth of the slack.",
        "Stage1Instances.THM_M_0957_ObligationTree.LinearDimensionLossPackage",
        "The linear half of the balanced exponent estimate.",
        "Use the upper ceiling control and eventual absorption of the rounding error.",
        "Behrend 1946 p.332; exact linear loss proof pending", 56,
    ),
    row(
        "L-LINEAR-CEILING", "normalization", "normal",
        "The ceiling-selected dimension is at most its real square-root proxy plus one, after multiplying by log 2.",
        "Stage1Instances.THM_M_0957_ObligationTree.LinearCeilingPackage",
        "The exact linear ceiling estimate before asymptotic increment absorption.",
        "Use the upper DimensionControlAt inequality and normalize the square-root coefficient.",
        "ObligationTree.lean#LinearCeilingPackage; Behrend 1946 p.332", 38,
    ),
    row(
        "L-LINEAR-INCREMENT", "core_lemma", "high",
        "Eventually the allocated eighth-slack absorbs the N+1 logarithmic increment and the additive ceiling loss.",
        "Stage1Instances.THM_M_0957_ObligationTree.LinearIncrementAbsorptionPackage",
        "The exact comparison from the ceiling estimate to the slackened linear balance.",
        "Control log(N+1)-log N and dominate the fixed log 2 term by sqrt(log N).",
        "ObligationTree.lean#LinearIncrementAbsorptionPackage; Behrend 1946 p.332", 52,
    ),
    row(
        "L-SUBLEADING-LOSS", "core_lemma", "high",
        "The floor slack, reciprocal-dimension denominator, fixed factors, and logarithmic terms are eventually absorbed by the remaining square-root slack.",
        "Stage1Instances.THM_M_0957_ObligationTree.SubleadingLossPackage",
        "The strict subleading-loss estimate needed to close the optimal exponent parent.",
        "Dominate log n and fixed losses by sqrt(log N), retaining strict positive slack.",
        "Behrend 1946 p.332; exact subleading loss proof pending", 72,
    ),
    row(
        "L-DIMENSION-SLACK", "core_lemma", "high",
        "Eventually the dimension multiple of one quarter of delta uses at most one half of delta times sqrt(log N).",
        "Stage1Instances.THM_M_0957_ObligationTree.DimensionSlackPackage",
        "The exact dimension-dependent portion of the subleading-loss estimate.",
        "Use the upper dimension control and the positive asymptotic scale to absorb its rounding term.",
        "ObligationTree.lean#DimensionSlackPackage; Behrend 1946 p.332", 44,
    ),
    row(
        "L-LOG-DIMENSION", "core_lemma", "high",
        "Eventually log of the selected dimension minus the fixed factor uses less than one quarter of delta times sqrt(log N).",
        "Stage1Instances.THM_M_0957_ObligationTree.LogDimensionLossPackage",
        "The exact logarithmic and fixed-factor portion of the subleading-loss estimate.",
        "Bound log(sharpDimension N) by a logarithm of the square-root scale and apply log N = o(sqrt(log N)).",
        "ObligationTree.lean#LogDimensionLossPackage; Behrend 1946 p.332", 56,
    ),
    row(
        "T-PROXY-ASYMPTOTIC", "terminal", "critical",
        "Apply the optimal-exponent bridge to the selected rounded dimension.",
        "Stage1Instances.THM_M_0957_ObligationTree.ProxyAsymptoticPackage",
        "The sharp exponential comparison at radixProxy.",
        "Merge the eventual thresholds and discharge DimensionControlAt.",
        "ObligationTree.lean#proxyAsymptotic_of_dimension_and_bridge", 5,
        body="local:Stage1_Instances/THM-M-0957/ObligationTree.lean#proxyAsymptotic_of_dimension_and_bridge",
    ),
    row(
        "T-RATIO-ASYMPTOTIC", "terminal", "critical",
        "Transfer the proxy asymptotic estimate through the floor comparison to the selected natural radix.",
        "Stage1Instances.THM_M_0957_ObligationTree.RatioAsymptoticPackage",
        "The sharp exponential comparison at sharpRadix.",
        "Use nonnegative natural-power monotonicity and divide by the positive dimension.",
        "ObligationTree.lean#ratioAsymptotic_of_proxy_floor_and_dimension", 8,
        body="local:Stage1_Instances/THM-M-0957/ObligationTree.lean#ratioAsymptotic_of_proxy_floor_and_dimension",
    ),
    row(
        "T-SHARP-ESTIMATE", "terminal", "critical",
        "Combine rpow normalization at epsilon with the ratio asymptotic estimate at epsilon/2, using the remaining half-epsilon as strict slack.",
        "Stage1Instances.THM_M_0957_ObligationTree.SharpEstimatePackage",
        "The historical lower is strictly below the selected d^(n-2)/n ratio.",
        "Merge thresholds, prove sqrt(log N)>0, compare exponential losses, and compose strict inequalities.",
        "ObligationTree.lean#sharpEstimate_of_normalization_and_ratio", 10,
        body="local:Stage1_Instances/THM-M-0957/ObligationTree.lean#sharpEstimate_of_normalization_and_ratio",
    ),
    row(
        "T-SHARP-PARAMETERS", "terminal", "critical",
        "Merge parameter admissibility, ambient fit, and the sharp estimate under one epsilon-dependent threshold.",
        "Stage1Instances.THM_M_0957_ObligationTree.SharpParameterPackage",
        "All sharp parameter facts consumed by root composition.",
        "Take the maximum of the three thresholds and project every child conclusion.",
        "ObligationTree.lean#sharpParameters_of_components", 7,
        body="local:Stage1_Instances/THM-M-0957/ObligationTree.lean#sharpParameters_of_components",
    ),
    row(
        "N-INCLUSIVE-INDEX", "transport", "high",
        "Monotonicity transports rothNumberNat from the constructed digit interval into the inclusive source interval N + 1.",
        "Stage1Instances.THM_M_0957_ObligationTree.IndexMonotonicityPackage",
        "The exact cast Roth-number inequality used by the root.",
        "Apply rothNumberNat.mono and cast the natural inequality to Real.",
        "ObligationTree.lean#pinnedIndexMonotonicity", 4,
        body="local:Stage1_Instances/THM-M-0957/ObligationTree.lean#pinnedIndexMonotonicity",
    ),
    row(
        "X-CONSTANT4-MISMATCH", "certificate", "high",
        "Pinned constant-four terminal bounds are weaker than the historical target at epsilon = 1 and cannot be root premises.",
        "Stage1Instances.THM_M_0957_AnchorAudit.historicalConstantAtOne_lt_mathlibConstant",
        "A checked exclusion of the tempting but invalid root substitution.",
        "Prove 2*sqrt(2*log 2)+1 < 4 and retain the constant-four route as non-proof evidence only.",
        "AnchorAudit.lean:49-89", 12, machine="informational",
        human="not_applicable",
        body="local:Stage1_Instances/THM-M-0957/AnchorAudit.lean#historicalConstantAtOne_lt_mathlibConstant",
    ),
    row(
        "X-SOURCE", "terminal", "critical",
        "Map every construction and sharp-optimization transition to an admitted immutable primary source, corrections, errata, and independent review.",
        "Behrend 1946 pages 331-332 node-specific source packet pending",
        "Human-source coverage without machine-proof credit.",
        "Preserve exact page locators and obtain independent source admission and review.",
        "source-statement-crosswalk.md; observed scans only", 80,
        machine="not_applicable",
    ),
    row(
        "X-PROVENANCE", "certificate", "critical",
        "Bind local compositions, pinned terminal bodies, transitive imports, aliases, licenses, and revocations without duplicate proof credit.",
        "anchor-audit.json plus future declaration-level closure",
        "Release-grade proof-body provenance without mathematical proof credit.",
        "Deduplicate bound_aux wrappers and trace every terminal body transitively.",
        "anchor-audit.json candidates and immutable_environment", 48,
        machine="informational", human="not_applicable",
    ),
    row(
        "X-TRUST", "certificate", "critical",
        "Audit toolchain, compiled artifacts, axioms, unsafe/oracle boundaries, replay, and supply-chain trust transitively.",
        "Lean 4.29.0 and mathlib 8a178386 transitive trust closure",
        "Release trust evidence without proof credit.",
        "Recompute the closure in a clean, cold, network-denied environment with independent verification.",
        "anchor-audit.json trust_audit", 48,
        machine="informational", human="not_applicable",
    ),
    row(
        "X-READABLE", "terminal", "high",
        "Produce and independently review a complete reconstruction of the sphere/digit construction and sharp asymptotic optimization.",
        "node-specific proof outline and long process surface pending",
        "Readable coverage without machine-proof credit.",
        "Expand every critical leaf into source-bound premise-to-output mathematical steps.",
        "obligation-tree.md is architecture only", 80,
        machine="not_applicable", human="not_applicable",
    ),
    row(
        "X-WORKFLOW", "certificate", "critical",
        "Bind dependency-legal proof implementation, validation, source/readability review, freshness, revocation, and independent release verification.",
        "Stage1 rev-5.6 task and receipt workflow",
        "Workflow acceptance without mathematical proof credit.",
        "Require accepted predecessor and node receipts before downstream state transitions.",
        "Docs/Stage1_Execution_DAG_rev-5.6.json", 32,
        machine="informational", human="not_applicable",
    ),
)


REQUIRES = {
    oid("ROOT"): [oid("T-ASSEMBLE")],
    oid("T-ASSEMBLE"): [
        oid("T-CONSTRUCTION"), oid("T-SHARP-PARAMETERS"), oid("N-INCLUSIVE-INDEX")
    ],
    oid("T-CONSTRUCTION"): [],
    oid("T-SHARP-PARAMETERS"): [
        oid("T-PARAM-ADMISSIBLE"), oid("L-AMBIENT-FIT"),
        oid("T-SHARP-ESTIMATE"),
    ],
    oid("T-PARAM-ADMISSIBLE"): [
        oid("N-SHARP-DIMENSION"), oid("L-RADIX-NONZERO")
    ],
    oid("N-SHARP-DIMENSION"): [],
    oid("L-RADIX-NONZERO"): [],
    oid("L-AMBIENT-FIT"): [],
    oid("T-SHARP-ESTIMATE"): [oid("N-RPOW-EXP"), oid("T-RATIO-ASYMPTOTIC")],
    oid("N-RPOW-EXP"): [],
    oid("T-RATIO-ASYMPTOTIC"): [
        oid("T-PROXY-ASYMPTOTIC"), oid("L-RADIX-FLOOR"),
        oid("N-SHARP-DIMENSION"),
    ],
    oid("L-RADIX-FLOOR"): [],
    oid("T-PROXY-ASYMPTOTIC"): [
        oid("N-SHARP-DIMENSION"), oid("L-OPTIMAL-EXPONENT")
    ],
    oid("L-OPTIMAL-EXPONENT"): [
        oid("L-PROXY-LOG"), oid("L-RECIPROCAL-LOSS"),
        oid("L-LINEAR-LOSS"), oid("L-SUBLEADING-LOSS"),
    ],
    oid("L-PROXY-LOG"): [
        oid("L-PROXY-RPOW-IDENTITY"), oid("L-PROXY-SLACK")
    ],
    oid("L-PROXY-RPOW-IDENTITY"): [],
    oid("L-PROXY-SLACK"): [],
    oid("L-RECIPROCAL-LOSS"): [oid("L-RECIPROCAL-CORE")],
    oid("L-RECIPROCAL-CORE"): [],
    oid("L-LINEAR-LOSS"): [
        oid("L-LINEAR-CEILING"), oid("L-LINEAR-INCREMENT")
    ],
    oid("L-LINEAR-CEILING"): [],
    oid("L-LINEAR-INCREMENT"): [],
    oid("L-SUBLEADING-LOSS"): [
        oid("L-DIMENSION-SLACK"), oid("L-LOG-DIMENSION")
    ],
    oid("L-DIMENSION-SLACK"): [],
    oid("L-LOG-DIMENSION"): [],
    oid("N-INCLUSIVE-INDEX"): [],
}

CERTIFICATES = {
    oid("ROOT"): "Stage1Instances.THM_M_0957_ObligationTree.root_of_exactAssembly",
    oid("T-ASSEMBLE"): "Stage1Instances.THM_M_0957_ObligationTree.exactAssembly_of_children",
    oid("T-PARAM-ADMISSIBLE"): "Stage1Instances.THM_M_0957_ObligationTree.parameterAdmissibility_of_dimension_and_radix",
    oid("L-PROXY-LOG"): "Stage1Instances.THM_M_0957_ObligationTree.proxyLogLower_of_identity_and_slack",
    oid("L-RECIPROCAL-LOSS"): "Stage1Instances.THM_M_0957_ObligationTree.reciprocalLoss_of_balanced_core",
    oid("L-LINEAR-LOSS"): "Stage1Instances.THM_M_0957_ObligationTree.linearLoss_of_ceiling_and_increment",
    oid("L-SUBLEADING-LOSS"): "Stage1Instances.THM_M_0957_ObligationTree.subleadingLoss_of_dimension_and_log",
    oid("T-SHARP-PARAMETERS"): "Stage1Instances.THM_M_0957_ObligationTree.sharpParameters_of_components",
    oid("T-SHARP-ESTIMATE"): "Stage1Instances.THM_M_0957_ObligationTree.sharpEstimate_of_normalization_and_ratio",
    oid("T-RATIO-ASYMPTOTIC"): "Stage1Instances.THM_M_0957_ObligationTree.ratioAsymptotic_of_proxy_floor_and_dimension",
    oid("T-PROXY-ASYMPTOTIC"): "Stage1Instances.THM_M_0957_ObligationTree.proxyAsymptotic_of_dimension_and_bridge",
    oid("L-OPTIMAL-EXPONENT"): "Stage1Instances.THM_M_0957_ObligationTree.optimalExponent_of_components",
}

PINNED_CONSTRUCTION = {
    oid("T-CONSTRUCTION"), oid("C-BOX-SPHERE"), oid("L-SPHERE-FREE"),
    oid("C-DIGIT-MAP"), oid("L-IMAGE-FREE"), oid("L-EXTREMAL-CARD"),
    oid("L-LARGE-SPHERE"), oid("L-IMPLICIT-BOUND"),
}

LOCAL_CHECKED = {
    oid("S-PREDICATE"), oid("S-EXTREMAL"), oid("T-ASSEMBLE"),
    oid("ROOT"), oid("T-PARAM-ADMISSIBLE"),
    oid("L-PROXY-LOG"), oid("L-RECIPROCAL-LOSS"),
    oid("L-LINEAR-LOSS"), oid("L-SUBLEADING-LOSS"),
    oid("T-PROXY-ASYMPTOTIC"),
    oid("T-RATIO-ASYMPTOTIC"), oid("T-SHARP-ESTIMATE"),
    oid("T-SHARP-PARAMETERS"), oid("N-INCLUSIVE-INDEX"),
    oid("L-OPTIMAL-EXPONENT"),
    oid("X-CONSTANT4-MISMATCH"),
}


# Ordered proof-plan ledgers for the final open mathematical leaves. References such as "$2"
# point to an earlier step in the same ledger; they are resolved to stable step IDs below.
LEAF_LEDGER_DETAILS = {
    "N-SHARP-DIMENSION": [
        (["frozen-formal-context"],
         "Establish 0 < log 2 and an eventual threshold where log (N + 1) is positive and exceeds every fixed bound used below.",
         "Mathlib.Analysis.SpecialFunctions.Log.Basic; Behrend 1946 p.332",
         "A common large-N domain with positive logarithm and denominator."),
        (["$1"],
         "Show the real proxy sqrt (2 * log (N + 1) / log 2) is eventually at least two.",
         "Real.sqrt_le_iff; Real.log_atTop",
         "The unrounded dimension proxy is at least two."),
        (["$2"],
         "Apply the natural-ceiling lower bound to obtain 2 <= sharpDimension N.",
         "Nat.le_ceil",
         "The selected natural dimension is admissible."),
        (["$1"],
         "Apply both natural-ceiling inequalities and cast them to Real.",
         "Nat.ceil_lt_add_one; Nat.le_ceil",
         "The selected dimension lies between the real proxy and that proxy plus one."),
        (["$3", "$4"],
         "Rewrite the two-sided ceiling bounds as the required absolute-value estimate and pair it with admissibility.",
         "abs_le",
         "Eventual DimensionControlAt N, hence DimensionControlPackage."),
    ],
    "L-RADIX-NONZERO": [
        (["M0957-N-SHARP-DIMENSION"],
         "Use dimension control to keep sharpDimension positive and bound its reciprocal on the large-N domain.",
         "ObligationTree.lean#DimensionControlAt",
         "A positive exponent denominator for the selected real radix."),
        (["$1", "frozen-formal-context"],
         "Use logarithmic growth and the dimension upper bound to show ((N+1):Real)^(1/n) / 2 is eventually at least one.",
         "Real.rpow_def_of_pos; Real.exp_le_exp",
         "The unrounded radix is eventually at least one."),
        (["$2"],
         "Apply the natural-floor positivity criterion and unfold sharpRadix.",
         "Nat.floor_pos",
         "Eventual 0 < sharpRadix N."),
        (["$3"],
         "Convert positivity to nonzeroness and package the common threshold.",
         "Nat.pos_iff_ne_zero",
         "RadixNonzeroPackage."),
    ],
    "L-RADIX-FLOOR": [
        (["M0957-N-SHARP-DIMENSION", "frozen-formal-context"],
         "Show the unrounded radix is eventually at least one, so radixProxy N is nonnegative.",
         "Real.rpow_def_of_pos; sub_nonneg",
         "Eventual 0 <= radixProxy N."),
        (["$1"],
         "Apply the strict upper floor inequality to the unrounded radix.",
         "Nat.lt_floor_add_one",
         "The unrounded radix is below sharpRadix N + 1 after casting."),
        (["$2"],
         "Subtract one and weaken the strict comparison to obtain radixProxy N <= (sharpRadix N : Real).",
         "sub_le_iff_le_add; le_of_lt",
         "The exact proxy-to-natural-radix upper comparison."),
        (["$1", "$3"],
         "Merge thresholds and pair the nonnegative and upper comparisons.",
         "Nat.max_def",
         "RadixFloorPackage."),
    ],
    "L-AMBIENT-FIT": [
        (["M0957-N-SHARP-DIMENSION", "frozen-formal-context"],
         "Use Nat.floor_le to bound twice the selected radix by the positive real rpow base.",
         "Nat.floor_le; mul_le_mul_of_nonneg_left",
         "A real upper bound for 2 * sharpRadix N."),
        (["$1"],
         "Bound 2 * sharpRadix N - 1 by the same nonnegative base and raise both sides to sharpDimension N.",
         "pow_le_pow_left₀; Nat.cast_sub",
         "A real-power upper bound for the digit interval size."),
        (["M0957-N-SHARP-DIMENSION", "frozen-formal-context"],
         "Normalize the selected reciprocal exponent multiplied by the positive natural dimension.",
         "Real.rpow_natCast; inv_mul_cancel₀",
         "The bounding real power is at most (N + 1 : Real)."),
        (["$2", "$3"],
         "Compose the real inequalities and cast the resulting natural comparison back to Nat.",
         "Nat.cast_le",
         "Eventual (2 * sharpRadix N - 1)^sharpDimension N <= N + 1."),
        (["$4"],
         "Package the large-N threshold.",
         "eventual threshold introduction",
         "AmbientFitPackage."),
    ],
    "N-RPOW-EXP": [
        (["frozen-formal-context"],
         "Choose a threshold N >= 2, giving 0 < (N : Real), 0 < log N, and 0 < sqrt (log N).",
         "Real.log_pos; Real.sqrt_pos.2",
         "A valid positive domain for rpow and square-root cancellation."),
        (["$1"],
         "Expand the historical real power with Real.rpow_def_of_pos.",
         "Real.rpow_def_of_pos",
         "The lower expression as exp of its exponent times log N."),
        (["$1"],
         "Use sqrt(log N)^2 = log N and divide by the positive square root.",
         "Real.sq_sqrt; div_mul_eq_mul_div",
         "The exponent product equals log N - (sharpConstant + epsilon) * sqrt(log N)."),
        (["$2", "$3"],
         "Rewrite by the exponent identity and close by reflexive inequality.",
         "Real.exp_le_exp",
         "The required pointwise normalization inequality."),
        (["$4"],
         "Quantify over positive epsilon and package the uniform large-N threshold.",
         "threshold introduction",
         "RpowNormalizationPackage."),
    ],
    "L-PROXY-RPOW-IDENTITY": [
        (["M0957-N-SHARP-DIMENSION"],
         "Extract positivity and nonzeroness of (sharpDimension N : Real).",
         "ObligationTree.lean#DimensionControlAt",
         "A nonzero real dimension denominator."),
        (["$1", "frozen-formal-context"],
         "Expand the positive-base real power in sharpRadix's unrounded expression.",
         "Real.rpow_def_of_pos",
         "The unrounded power as exp (log(N+1) * n^-1)."),
        (["$1", "$2"],
         "Rewrite multiplication by the inverse as division by the dimension.",
         "div_eq_mul_inv",
         "The exponent log(N+1) / n."),
        (["$3", "frozen-formal-context"],
         "Rewrite division by two as subtraction of log 2 inside the exponential.",
         "Real.exp_sub; Real.exp_log",
         "The exponential expression for the unrounded radix."),
        (["$4"],
         "Unfold radixProxy and cancel the added and subtracted one.",
         "ObligationTree.lean#radixProxy",
         "ProxyRpowIdentityPackage."),
    ],
    "L-PROXY-SLACK": [
        (["M0957-N-SHARP-DIMENSION", "frozen-formal-context"],
         "Work on a threshold where log N is positive and sharpDimension N is comparable to sqrt(log N).",
         "Real.log_atTop; ObligationTree.lean#DimensionControlAt",
         "Positive large-N logarithmic and dimension scales."),
        (["$1"],
         "Show the N-to-N+1 logarithmic increment divided by sharpDimension tends to zero.",
         "Real.tendsto_log_atTop; asymptotic comparison",
         "The exponent change from N to N+1 consumes less than one eighth of delta."),
        (["$1"],
         "Show the exponential at the retained main exponent tends to infinity.",
         "Real.tendsto_exp_atTop; dimension upper control",
         "The growing exponential eventually absorbs the fixed additive one."),
        (["$2", "$3"],
         "Allocate the quarter-delta slack between the logarithmic increment and fixed additive loss, then compose the exponential inequalities.",
         "Real.exp_le_exp; add_le_add",
         "The exact pointwise proxy-slack inequality."),
        (["$4"],
         "Merge thresholds and quantify over positive delta.",
         "threshold maximum",
         "ProxySlackAbsorptionPackage."),
    ],
    "L-RECIPROCAL-CORE": [
        (["M0957-N-SHARP-DIMENSION"],
         "Use the ceiling lower bound to place sharpDimension above sqrt(2 * log(N+1) / log 2).",
         "ObligationTree.lean#DimensionControlAt; Nat.le_ceil",
         "A positive lower bound for the dimension denominator."),
        (["frozen-formal-context"],
         "On N >= 1, compare log N <= log(N+1) and record positivity of log 2 and both square roots.",
         "Real.strictMonoOn_log; Real.sqrt_nonneg",
         "Monotone nonnegative logarithmic inputs."),
        (["$1", "$2"],
         "Divide by the positive dimension lower bound and normalize the balanced square-root product.",
         "div_le_iff₀; Real.sqrt_mul",
         "The no-slack reciprocal balance at N."),
        (["$3"],
         "Choose a common threshold and package DimensionControlAt as the local premise.",
         "threshold introduction",
         "ReciprocalBalancedCorePackage."),
    ],
    "L-LINEAR-CEILING": [
        (["M0957-N-SHARP-DIMENSION"],
         "Rewrite the absolute-value dimension control as the upper ceiling inequality n <= proxy + 1.",
         "abs_le.mp; ObligationTree.lean#DimensionControlAt",
         "An upper real bound for sharpDimension N."),
        (["frozen-formal-context"],
         "Record 0 < log 2 and nonnegativity of the real square-root proxy.",
         "Real.log_pos; Real.sqrt_nonneg",
         "Nonnegative factors for monotone multiplication."),
        (["$1", "$2"],
         "Multiply the ceiling inequality by log 2.",
         "mul_le_mul_of_nonneg_right",
         "n * log 2 is bounded by (proxy + 1) * log 2."),
        (["$2", "$3"],
         "Normalize proxy * log 2 to sqrt(2 * log(N+1) * log 2) and distribute the additive term.",
         "Real.sqrt_mul; ring normalization",
         "LinearCeilingPackage."),
    ],
    "L-LINEAR-INCREMENT": [
        (["frozen-formal-context"],
         "Work eventually with positive log N and compare log(N+1) - log N to zero.",
         "Real.log_atTop; Real.log_div",
         "The N-to-N+1 logarithmic increment is asymptotically negligible."),
        (["$1"],
         "Transfer the negligible logarithmic increment through the nonnegative square-root expression.",
         "Real.sqrt_le_sqrt; square-root asymptotics",
         "The square-root main term at N+1 differs from its N counterpart by o(sqrt(log N))."),
        (["$1"],
         "Use sqrt(log N) tending to infinity to absorb the fixed additive log 2.",
         "Filter.Tendsto.eventually_const_lt; Real.tendsto_sqrt_atTop",
         "The fixed ceiling loss uses less than the remaining allocated slack."),
        (["$2", "$3"],
         "Allocate delta/8 across the increment and fixed loss and normalize the main coefficient.",
         "add_le_add; ring normalization",
         "The required pointwise linear-increment comparison."),
        (["$4"],
         "Quantify over positive delta and package a common threshold.",
         "threshold maximum",
         "LinearIncrementAbsorptionPackage."),
    ],
    "L-DIMENSION-SLACK": [
        (["M0957-N-SHARP-DIMENSION"],
         "Extract the upper dimension bound n <= sqrt(2 * log(N+1) / log 2) + 1.",
         "abs_le.mp; ObligationTree.lean#DimensionControlAt",
         "A source-shaped upper bound for the selected dimension."),
        (["frozen-formal-context"],
         "Show the coefficient sqrt(2 / log 2) is strictly below two.",
         "Real.sqrt_lt_iff; numerical log bound",
         "Positive fixed room below 2 * sqrt(log N)."),
        (["$1", "$2"],
         "Absorb the N+1 increment and additive ceiling one into that fixed coefficient room.",
         "large-N logarithmic comparison",
         "Eventually (sharpDimension N - 2 : Nat) <= 2 * sqrt(log N) after casting."),
        (["$3", "frozen-formal-context"],
         "Multiply by delta/4 using delta positivity.",
         "mul_le_mul_of_nonneg_left",
         "The exact pointwise dimension-slack inequality."),
        (["$4"],
         "Quantify over positive delta and package the threshold.",
         "threshold introduction",
         "DimensionSlackPackage."),
    ],
    "L-LOG-DIMENSION": [
        (["M0957-N-SHARP-DIMENSION"],
         "Bound sharpDimension N by a fixed positive multiple of sqrt(log N) on a large-N domain.",
         "ObligationTree.lean#DimensionControlAt; N-to-N+1 comparison",
         "An eventual positive upper bound for the logarithmic dimension."),
        (["$1", "frozen-formal-context"],
         "Apply monotonicity of log and expand the logarithm of the fixed multiple.",
         "Real.strictMonoOn_log; Real.log_mul",
         "log(sharpDimension N) <= fixed constant + log(sqrt(log N))."),
        (["frozen-formal-context"],
         "Use log(log N) = o(sqrt(log N)) on the positive large-N domain.",
         "Real.isLittleO_log_id_atTop; asymptotic composition",
         "The logarithmic dimension term uses arbitrarily small positive square-root slack."),
        (["$2", "$3"],
         "Absorb the fixed constants, including -2 * log 2, within delta/4 of the square-root scale.",
         "eventual constant absorption; linarith",
         "The exact pointwise logarithmic-loss inequality."),
        (["$4"],
         "Quantify over positive delta and package the common threshold.",
         "threshold maximum",
         "LogDimensionLossPackage."),
    ],
}


def edge(
    edge_id: str, source: str, edge_type: str, target: str,
    reciprocal: str | None = None,
) -> dict:
    value = {"edge_id": edge_id, "from": source, "type": edge_type, "to": target}
    if reciprocal is not None:
        value["reciprocal_edge_id"] = reciprocal
    return value


def graph(edges: list[dict], endpoints: list[str]) -> dict:
    outgoing = {identifier: [] for identifier in endpoints}
    incoming = {identifier: [] for identifier in endpoints}
    for value in edges:
        outgoing[value["from"]].append(value["edge_id"])
        incoming[value["to"]].append(value["edge_id"])
    return {"edges": edges, "out": outgoing, "in": incoming}


def build() -> tuple[dict, dict, dict]:
    statement_hash = hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest()
    anchor_hash = hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest()

    exclusions = {
        oid("S-PREDICATE"): "formal_predicate_transport_human_source_not_applicable_pending_approval",
        oid("S-EXTREMAL"): "formal_extremal_transport_human_source_not_applicable_pending_approval",
        oid("S-TARGET"): "statement_overlay_no_independent_machine_credit_pending_approval",
        oid("S-FINITE-TARGET"): "alternate_proposition_overlay_no_independent_machine_credit_pending_approval",
        oid("S-BOUNDARY"): "boundary_overlay_no_independent_machine_credit_pending_approval",
        oid("S-FOUNDATION"): "foundation_overlay_no_proof_credit_pending_approval",
        oid("C-BOX-SPHERE"): "pinned_body_internal_overlay_no_independent_machine_credit_pending_signature_review",
        oid("L-SPHERE-FREE"): "pinned_body_internal_overlay_no_independent_machine_credit_pending_signature_review",
        oid("C-DIGIT-MAP"): "pinned_body_internal_overlay_no_independent_machine_credit_pending_signature_review",
        oid("L-IMAGE-FREE"): "pinned_body_internal_overlay_no_independent_machine_credit_pending_signature_review",
        oid("L-EXTREMAL-CARD"): "pinned_body_internal_overlay_no_independent_machine_credit_pending_signature_review",
        oid("L-LARGE-SPHERE"): "pinned_body_internal_overlay_no_independent_machine_credit_pending_signature_review",
        oid("L-IMPLICIT-BOUND"): "pinned_body_internal_overlay_no_independent_machine_credit_pending_signature_review",
        oid("X-CONSTANT4-MISMATCH"): "mismatch_exclusion_overlay_no_root_proof_credit",
        oid("X-SOURCE"): "human_source_boundary_only_pending_independent_source_review",
        oid("X-PROVENANCE"): "provenance_overlay_no_proof_credit_pending_integration_review",
        oid("X-TRUST"): "trust_overlay_no_proof_credit_pending_integration_review",
        oid("X-READABLE"): "readability_boundary_only_pending_independent_review",
        oid("X-WORKFLOW"): "workflow_overlay_no_proof_credit_pending_integration_review",
    }

    parent_of: dict[str, list[str]] = {}
    for parent, children in REQUIRES.items():
        for child in children:
            parent_of.setdefault(child, []).append(parent)

    obligations: list[dict] = []
    nodes: list[dict] = []
    for (
        short, kind, risk, claim, formal, result, inference, locator, budget,
        machine, human, body,
    ) in ROWS:
        identifier = oid(short)
        fingerprint = (
            f"lean-expression-sha256:{ROOT_EXPRESSION}"
            if identifier in {oid("ROOT"), oid("S-TARGET")}
            else "planned:v1:sha256:" + digest(
                [identifier, kind, claim, formal, result]
            )
        )
        obligations.append({
            "obligation_id": identifier,
            "statement_fingerprint": fingerprint,
            "kind": kind,
            "root_relevant": True,
            "machine_eligibility": machine,
            "human_source_eligibility": human,
        "readable_eligibility": "required",
            "risk_class": risk,
            "exclusion_reason": exclusions.get(identifier),
            "terminal_proof_body_id": body,
        })

        premises = REQUIRES.get(identifier, [])
        if not premises:
            premises = [
                "pinned-mathlib-source" if identifier in PINNED_CONSTRUCTION
                else "frozen-formal-context"
            ]
        outgoing_use = (
            "Consumed by " + ", ".join(parent_of[identifier]) + "."
            if identifier in parent_of
            else "Supports only a typed non-proof, documentation, trust, or workflow edge."
        )

        if identifier in PINNED_CONSTRUCTION:
            provenance = "anchor-audit:M0957-C02-MATHLIB-CONSTRUCTION-FAMILY"
        elif identifier in LOCAL_CHECKED:
            provenance = "target-local-checked-interface-or-composition"
        else:
            provenance = "none"

        owned_sources: list[str] = []
        if identifier in {
            oid("S-TARGET"), oid("S-PREDICATE"), oid("S-EXTREMAL"),
            oid("S-FINITE-TARGET"), oid("S-BOUNDARY"),
        }:
            owned_sources = [f"Stage1_Instances/{THEOREM}/Statement.lean"]
        elif identifier in {
            oid("ROOT"), oid("T-ASSEMBLE"),
            oid("T-CONSTRUCTION"), oid("N-SHARP-DIMENSION"), oid("L-RADIX-NONZERO"),
            oid("T-PARAM-ADMISSIBLE"),
            oid("L-RADIX-FLOOR"), oid("L-AMBIENT-FIT"), oid("N-RPOW-EXP"),
            oid("L-OPTIMAL-EXPONENT"), oid("L-PROXY-LOG"),
            oid("L-RECIPROCAL-LOSS"), oid("L-LINEAR-LOSS"),
            oid("L-SUBLEADING-LOSS"), oid("L-PROXY-RPOW-IDENTITY"),
            oid("L-PROXY-SLACK"), oid("L-RECIPROCAL-CORE"),
            oid("L-LINEAR-CEILING"), oid("L-LINEAR-INCREMENT"),
            oid("L-DIMENSION-SLACK"), oid("L-LOG-DIMENSION"),
            oid("T-PROXY-ASYMPTOTIC"),
            oid("T-RATIO-ASYMPTOTIC"), oid("T-SHARP-ESTIMATE"),
            oid("T-SHARP-PARAMETERS"), oid("N-INCLUSIVE-INDEX"),
        }:
            owned_sources = [f"Stage1_Instances/{THEOREM}/ObligationTree.lean"]
        elif identifier == oid("X-CONSTANT4-MISMATCH"):
            owned_sources = [f"Stage1_Instances/{THEOREM}/AnchorAudit.lean"]
        elif identifier == oid("X-SOURCE"):
            owned_sources = [f"Stage1_Instances/{THEOREM}/source-statement-crosswalk.md"]
        elif identifier == oid("X-READABLE"):
            owned_sources = [f"Stage1_Instances/{THEOREM}/obligation-tree.md"]

        task_ids = [ITEM]
        if machine == "required":
            task_ids.append("S56-M-0957-PROOF")
        if identifier in {oid("S-FOUNDATION"), oid("X-PROVENANCE"), oid("X-TRUST")}:
            task_ids.extend(["S56-M-0957-VALIDATION", "S56-M-0957-RELEASE"])
        if identifier in {oid("X-SOURCE"), oid("X-READABLE"), oid("X-WORKFLOW")}:
            task_ids.append("S56-M-0957-RELEASE")

        detailed = LEAF_LEDGER_DETAILS.get(short)
        if detailed is None:
            ledger = [{
                "step_id": f"{identifier}-STEP-01",
                "premise_ids": premises,
                "inference": inference,
                "source_locator": locator,
                "output": result,
                "outgoing_use": outgoing_use,
            }]
            proof_budget_status = (
                "composition_certificate_checked"
                if identifier in CERTIFICATES
                else "architecture_overlay_not_a_leaf_proof_budget"
            )
        else:
            ledger = []
            for index, (step_premises, step_inference, step_locator, step_output) in enumerate(
                detailed, start=1
            ):
                step_id = f"{identifier}-STEP-{index:02d}"
                resolved_premises = [
                    f"{identifier}-STEP-{int(value[1:]):02d}"
                    if value.startswith("$") else value
                    for value in step_premises
                ]
                ledger.append({
                    "step_id": step_id,
                    "premise_ids": resolved_premises,
                    "inference": step_inference,
                    "source_locator": step_locator,
                    "output": step_output,
                    "outgoing_use": (
                        f"Consumed by {identifier}-STEP-{index + 1:02d}."
                        if index < len(detailed) else outgoing_use
                    ),
                })
            proof_budget_status = (
                "unchecked_open_proof_plan_within_allocated_step_budget; "
                "no leaf-budget closure or proof acceptance"
            )

        nodes.append({
            "node_id": f"{THEOREM}-{short}",
            "obligation_id": identifier,
            "kind": kind,
            "human_statement": claim,
            "formal_target": formal,
            "output": result,
            "human_debt": "H1",
            "machine_debt": "M3" if machine != "not_applicable" else "M4",
            "readability_debt": "R3",
            "evidence_ids": [],
            "source_crosswalk_id": (
                "Behrend-1946-node-map-pending-independent-review"
                if human == "required" else "not-applicable-pending-review"
            ),
            "provenance_id": provenance,
            "foundation_profile": (
                "Lean 4 dependent type theory; observed axioms propext, "
                "Classical.choice, Quot.sound; accepted policy pending"
            ),
            "tcb_profile": (
                "Lean 4.29.0 plus mathlib 8a178386; compiled-artifact and "
                "independent release closure pending"
            ),
            "computation_record": (
                "none; no native computation, solver, oracle, experiment, or unchecked "
                "certificate is credited"
            ),
            "step_budget": budget,
            "semantic_step_ledger": ledger,
            "proof_budget_status": proof_budget_status,
            "public_readable_target": (
                f"Stage1_Instances/{THEOREM}/obligation-tree.md#{identifier.lower()}"
            ),
            "validation_spec_id": "VAL-M0957-OBLIGATION-BUNDLE",
            "status_boundary": (
                "Frozen architecture or provisionally checked interface only; no M0, "
                "accepted obligation, audit completion, or theorem completion."
            ),
            "task_ids": list(dict.fromkeys(task_ids)),
            "owned_sources": owned_sources,
            "owner": "THM-M-0957 proof lane",
            "reviewer": "independent Stage1 integration lane",
            "validity": {
                "validated_at": None,
                "review_due": "before master acceptance",
                "invalidation_inputs": [
                    "Statement.lean", "anchor-audit.json", "obligation-registry.json",
                    "typed-graphs.json", "toolchain and dependency pins",
                ],
                "revocation_state": "not-accepted",
            },
        })

    fields = (
        "obligation_id", "statement_fingerprint", "kind", "root_relevant",
        "machine_eligibility", "human_source_eligibility", "readable_eligibility",
        "risk_class", "exclusion_reason", "terminal_proof_body_id",
    )
    projection = [{field: value[field] for field in fields} for value in obligations]
    denominator = digest(projection)
    ids = [value["obligation_id"] for value in obligations]

    registry = {
        "schema_version": "stage1-obligation-registry/1.0",
        "normative_profile": "machine-theorem-assurance/1.0",
        "item_id": ITEM,
        "theorem_id": THEOREM,
        "registry_id": "THM-M-0957-OBLIGATIONS-v1",
        "registry_version": 1,
        "frozen_at": "2026-07-13T23:59:00+08:00",
        "freeze_basis": (
            "The exact frozen historical statement, inspected 1946 construction, and pinned "
            "mathlib bound_aux body determine the architecture. Eligibility, risk, and the "
            "denominator were selected without treating the weaker constant-four theorem as "
            "root proof evidence and before any proof-phase acceptance."
        ),
        "frozen_against_statement_sha256": statement_hash,
        "frozen_against_anchor_audit_sha256": anchor_hash,
        "root_obligation_id": oid("ROOT"),
        "denominator_sha256": denominator,
        "frozen_denominators": {
            "inventory": ids,
            "required_machine": [
                value["obligation_id"] for value in obligations
                if value["machine_eligibility"] == "required"
            ],
            "required_human_source": [
                value["obligation_id"] for value in obligations
                if value["human_source_eligibility"] == "required"
            ],
            "required_readable": ids,
            "informational_overlays": [
                value["obligation_id"] for value in obligations
                if value["machine_eligibility"] == "informational"
            ],
        },
        "layer_applicability": {
            "S_statement_foundation": {
                "status": "required",
                "obligation_ids": [oid(short) for short in (
                    "S-TARGET", "S-PREDICATE", "S-EXTREMAL", "S-FINITE-TARGET",
                    "S-BOUNDARY", "S-FOUNDATION"
                )],
            },
            "N_normalization": {
                "status": "required",
                "obligation_ids": [oid(short) for short in (
                    "N-SHARP-DIMENSION", "N-RPOW-EXP", "L-PROXY-RPOW-IDENTITY",
                    "L-LINEAR-CEILING"
                )],
            },
            "B_branch": {"status": "required", "obligation_ids": [oid("S-BOUNDARY")]},
            "C_construction": {
                "status": "required",
                "obligation_ids": [oid(short) for short in (
                    "C-BOX-SPHERE", "C-DIGIT-MAP"
                )],
            },
            "L_core_lemma": {
                "status": "required",
                "obligation_ids": [oid(short) for short in (
                    "L-SPHERE-FREE", "L-IMAGE-FREE", "L-EXTREMAL-CARD",
                    "L-LARGE-SPHERE", "L-IMPLICIT-BOUND", "L-RADIX-FLOOR",
                    "L-RADIX-NONZERO", "L-AMBIENT-FIT", "L-OPTIMAL-EXPONENT",
                    "L-PROXY-LOG",
                    "L-PROXY-SLACK",
                    "L-RECIPROCAL-LOSS", "L-RECIPROCAL-CORE",
                    "L-LINEAR-LOSS", "L-LINEAR-INCREMENT",
                    "L-SUBLEADING-LOSS", "L-DIMENSION-SLACK", "L-LOG-DIMENSION"
                )],
            },
            "X_external_and_computation": {
                "status": "required_external_boundary_and_not_applicable_computation_pending_independent_approval",
                "reason": (
                    "Pinned mathlib bodies and trust are material. No reflection, solver, "
                    "native computation, oracle, experiment, or unchecked certificate is credited."
                ),
                "obligation_ids": [oid(short) for short in (
                    "T-CONSTRUCTION", "X-CONSTANT4-MISMATCH", "X-SOURCE",
                    "X-PROVENANCE", "X-TRUST", "X-READABLE", "X-WORKFLOW"
                )],
            },
            "T_terminal_transport": {
                "status": "required",
                "obligation_ids": [oid(short) for short in (
                    "T-ASSEMBLE", "T-PARAM-ADMISSIBLE", "T-PROXY-ASYMPTOTIC",
                    "T-RATIO-ASYMPTOTIC", "T-SHARP-ESTIMATE", "T-SHARP-PARAMETERS",
                    "N-INCLUSIVE-INDEX"
                )],
            },
            "ROOT_exact_theorem": {"status": "required", "obligation_ids": [oid("ROOT")]},
        },
        "layer_exclusions": {
            "additional_case_splits": {
                "status": "not_applicable_pending_independent_approval",
                "reason": (
                    "Beyond eventual small-N exclusion, the selected one-branch sphere/digit "
                    "construction has no parity, prime, induction, or local/global case split."
                ),
            },
            "external_computation": {
                "status": "not_applicable_pending_independent_approval",
                "reason": (
                    "No reflection, solver, native computation, enumeration, oracle, "
                    "experiment, or unchecked certificate proves the universal target."
                ),
            },
            "constant_four_root_route": {
                "status": "excluded_checked_statement_mismatch",
                "reason": (
                    "At epsilon = 1 the historical coefficient is below four, so the fixed "
                    "constant-four mathlib theorem is too weak and is not a root proof child."
                ),
            },
        },
        "proof_body_aliases": {
            "Stage1Instances.THM_M_0957_ObligationTree.exactAssembly_of_children": "composition_harness_only:no_distinct_terminal_proof_body_credit",
            "Stage1Instances.THM_M_0957_ObligationTree.root_of_exactAssembly": "wrapper_only_terminal_composition_over:ExactAssembly;semantic_body:Stage1Instances.THM_M_0957_ObligationTree.root_of_quantitative_and_parameters",
            "Stage1Instances.THM_M_0957_ObligationTree.pinnedQuantitativeConstruction": "wrapper_only_deduplicated_to:Behrend.bound_aux",
            "Stage1Instances.THM_M_0957_AnchorAudit.mathlibExplicitCandidate": "wrapper_only_deduplicated_to:Behrend.roth_lower_bound_explicit",
            "Stage1Instances.THM_M_0957_AnchorAudit.mathlibAllNCandidate": "wrapper_only_deduplicated_to:Behrend.roth_lower_bound",
            "Stage1Instances.THM_M_0957_AnchorAudit.mathlibCandidate_restricted": "restricted_adapter_no_historical_root_credit",
        },
        "delta_policy": (
            "Any target correction, split, merge, exclusion, eligibility/risk change, or "
            "terminal-body identity change requires registry version 2 and an append-only delta."
        ),
        "append_only_delta": [],
        "obligations": obligations,
        "status_observed_after_freeze": {
            "provisionally_checked_interfaces": sorted(LOCAL_CHECKED | {oid("T-CONSTRUCTION")}),
            "audited_partial_construction_obligations": sorted(PINNED_CONSTRUCTION),
            "candidate_route": (
                "pinned implicit construction family plus open sharp optimization; "
                "no unconditional or accepted exact root proof body"
            ),
            "accepted_closed_obligations": [],
            "accepted_root_machine_debt": "M3",
        },
        "status_boundary": (
            "Registry scope and denominators only. The sharp dimension, radix, floor, ambient, "
            "rpow, and optimal-exponent obligations are open; the pinned construction and local "
            "compositions are not installed or accepted; H0, R0, validation, release, AUDIT-Z, "
            "and theorem completion remain open."
        ),
    }

    proof_edges: list[dict] = []
    for parent, children in REQUIRES.items():
        for child in children:
            requirement = f"REQ-{parent}-{child}"
            composition = f"CMP-{child}-{parent}"
            proof_edges.extend([
                edge(requirement, parent, "proof_requires", child, composition),
                edge(composition, child, "composes", parent, requirement),
            ])

    refinement_edges = [
        edge("REF-ROOT-TARGET", oid("ROOT"), "expository_decomposition", oid("S-TARGET")),
        edge("REF-ROOT-FINITE", oid("ROOT"), "equivalent_to", oid("S-FINITE-TARGET")),
        edge("REF-FINITE-PREDICATE", oid("S-FINITE-TARGET"), "expository_decomposition", oid("S-PREDICATE")),
        edge("REF-ROOT-BOUNDARY", oid("ROOT"), "expository_decomposition", oid("S-BOUNDARY")),
        edge("REF-BOUND-BOX", oid("T-CONSTRUCTION"), "expository_decomposition", oid("C-BOX-SPHERE")),
        edge("REF-BOUND-SPHERE", oid("T-CONSTRUCTION"), "expository_decomposition", oid("L-SPHERE-FREE")),
        edge("REF-BOUND-DIGIT", oid("T-CONSTRUCTION"), "expository_decomposition", oid("C-DIGIT-MAP")),
        edge("REF-BOUND-IMAGE", oid("T-CONSTRUCTION"), "expository_decomposition", oid("L-IMAGE-FREE")),
        edge("REF-BOUND-EXTREMAL", oid("T-CONSTRUCTION"), "expository_decomposition", oid("L-EXTREMAL-CARD")),
        edge("REF-BOUND-LARGE", oid("T-CONSTRUCTION"), "expository_decomposition", oid("L-LARGE-SPHERE")),
        edge("REF-BOUND-IMPLICIT", oid("T-CONSTRUCTION"), "expository_decomposition", oid("L-IMPLICIT-BOUND")),
    ]

    source_required_ids = [
        value["obligation_id"] for value in obligations
        if value["human_source_eligibility"] == "required"
        and value["obligation_id"] != oid("X-SOURCE")
    ]
    provenance_body_ids = [
        value["obligation_id"] for value in obligations
        if value["terminal_proof_body_id"] is not None
        and value["obligation_id"] != oid("X-PROVENANCE")
    ]
    provenance_composition_ids = [
        identifier for identifier in CERTIFICATES
        if identifier not in provenance_body_ids
    ]
    provenance_interface_ids = [
        oid("S-PREDICATE"), oid("S-EXTREMAL"), oid("N-INCLUSIVE-INDEX")
    ]

    graph_edges = {
        "proof": proof_edges,
        "refinement": refinement_edges,
        "provenance": [
            *[
                edge(f"SOURCE-{identifier}", oid("X-SOURCE"), "source_map", identifier)
                for identifier in source_required_ids
            ],
            *[
                edge(f"PROV-BODY-{identifier}", oid("X-PROVENANCE"), "provenance_of", identifier)
                for identifier in provenance_body_ids
            ],
            *[
                edge(f"PROV-COMPOSITION-{identifier}", oid("X-PROVENANCE"), "provenance_of", identifier)
                for identifier in provenance_composition_ids
            ],
            *[
                edge(f"PROV-INTERFACE-{identifier}", oid("X-PROVENANCE"), "provenance_of", identifier)
                for identifier in provenance_interface_ids
                if identifier not in provenance_body_ids
                and identifier not in provenance_composition_ids
            ],
        ],
        "evidence": [
            edge("EVID-PROVENANCE-CONSTRUCTION", oid("X-PROVENANCE"), "evidence_for", oid("T-CONSTRUCTION")),
            edge("EVID-CONSTANT-MISMATCH", oid("X-CONSTANT4-MISMATCH"), "evidence_for", oid("S-BOUNDARY")),
            edge("EVID-CONSTANT-MISMATCH-ROOT", oid("X-CONSTANT4-MISMATCH"), "evidence_for", oid("ROOT")),
            edge("EVID-FINITE-IFF", oid("S-EXTREMAL"), "evidence_for", oid("S-FINITE-TARGET")),
        ],
        "trust": [
            edge("TRUST-ROOT-FOUNDATION", oid("ROOT"), "trusts", oid("S-FOUNDATION")),
            edge("TRUST-ROOT-CLOSURE", oid("ROOT"), "trusts", oid("X-TRUST")),
            edge("TRUST-CONSTRUCTION", oid("T-CONSTRUCTION"), "trusts", oid("X-TRUST")),
        ],
        "documentation": [
            edge("DOC-READABLE-ROOT", oid("X-READABLE"), "documents", oid("ROOT")),
            edge("DOC-READABLE-CONSTRUCTION", oid("X-READABLE"), "documents", oid("T-CONSTRUCTION")),
            edge("DOC-READABLE-OPTIMAL", oid("X-READABLE"), "documents", oid("L-OPTIMAL-EXPONENT")),
            edge("DOC-SOURCE-ROOT", oid("X-SOURCE"), "documents", oid("ROOT")),
            edge("DOC-BOUNDARY", oid("S-BOUNDARY"), "documents", oid("ROOT")),
        ],
        "workflow": [
            edge(f"TASK-{index}", TASK_IDS[index], "workflow_depends_on", TASK_IDS[index - 1])
            for index in range(1, len(TASK_IDS))
        ],
    }

    graphs = {
        name: graph(graph_edges[name], list(TASK_IDS) if name == "workflow" else ids)
        for name in GRAPH_NAMES
    }
    fingerprints = {
        value["obligation_id"]: value["statement_fingerprint"] for value in obligations
    }
    certificates = []
    for parent, declaration in CERTIFICATES.items():
        children = REQUIRES[parent]
        certificates.append({
            "certificate_id": f"CERT-{parent}",
            "parent_obligation_id": parent,
            "required_child_ids": children,
            "parent_statement_fingerprint": fingerprints[parent],
            "required_child_statement_fingerprints": {
                child: fingerprints[child] for child in children
            },
            "declaration": declaration,
            "certificate_kind": (
                "pinned_transparent_body_review"
                if declaration.startswith("pinned-body composition")
                else "lean_abstract_child_harness"
            ),
            "introduces_undeclared_premises": False,
            "status": "provisionally_elaborated_not_accepted",
        })

    checked_parents = set(CERTIFICATES)
    unverified = []
    for parent, children in REQUIRES.items():
        if children and parent not in checked_parents:
            unverified.append({
                "parent_obligation_id": parent,
                "required_child_ids": children,
                "status": "open_composition_certificate_required_before_parent_closure",
            })

    bundle = {
        "schema_version": "stage1-typed-graphs/1.0",
        "normative_profile": "machine-theorem-assurance/1.0",
        "item_id": ITEM,
        "theorem_id": THEOREM,
        "registry_id": registry["registry_id"],
        "registry_denominator_sha256": denominator,
        "root_node_id": oid("ROOT"),
        "edge_endpoint_namespace": (
            "canonical obligation_id except workflow, which uses authoritative task IDs"
        ),
        "edge_direction": (
            "proof_requires is parent-to-child; reciprocal composes is child-to-parent; "
            "workflow_depends_on is task-to-prerequisite"
        ),
        "workflow_task_nodes": list(TASK_IDS),
        "nodes": nodes,
        "graphs": graphs,
        "composition_certificates": certificates,
        "statement_fingerprint_boundary": (
            "ROOT and S-TARGET use the statement-phase elaborated expression hash. Other "
            "records use deterministic planned:v1 architecture fingerprints over the stable "
            "obligation ID, kind, human claim, formal-target label, and exact output. For every "
            "local Lean composition certificate, ObligationTree.lean also ascribes the exact "
            "child and parent Prop packages and the checker elaborates that declaration at "
            "trust=0. The planned hashes are not claimed to be machine-extracted Lean expression "
            "hashes; proof-phase acceptance must replace or independently bind them before M0."
        ),
        "unverified_decomposition_plans": unverified,
        "closure_boundary": {
            "provisionally_checked_interfaces": sorted(LOCAL_CHECKED | {oid("T-CONSTRUCTION")}),
            "candidate_only_obligations": sorted(PINNED_CONSTRUCTION),
            "accepted_closed_obligations": [],
            "root_closed": False,
            "accepted_root_machine_debt": "M3",
            "audit_complete": False,
            "theorem_complete": False,
            "required_proof_leaf_ids": [
                oid("T-CONSTRUCTION"), oid("N-SHARP-DIMENSION"),
                oid("L-RADIX-NONZERO"), oid("L-RADIX-FLOOR"),
                oid("L-AMBIENT-FIT"), oid("N-RPOW-EXP"),
                oid("L-PROXY-RPOW-IDENTITY"), oid("L-PROXY-SLACK"),
                oid("L-RECIPROCAL-CORE"), oid("L-LINEAR-CEILING"),
                oid("L-LINEAR-INCREMENT"), oid("L-DIMENSION-SLACK"),
                oid("L-LOG-DIMENSION"), oid("N-INCLUSIVE-INDEX"),
            ],
            "unimplemented_proof_leaf_ids": [
                oid("N-SHARP-DIMENSION"), oid("L-RADIX-NONZERO"),
                oid("L-RADIX-FLOOR"), oid("L-AMBIENT-FIT"),
                oid("N-RPOW-EXP"), oid("L-PROXY-RPOW-IDENTITY"),
                oid("L-PROXY-SLACK"), oid("L-RECIPROCAL-CORE"),
                oid("L-LINEAR-CEILING"), oid("L-LINEAR-INCREMENT"),
                oid("L-DIMENSION-SLACK"), oid("L-LOG-DIMENSION"),
            ],
            "checked_candidate_leaf_ids": [
                oid("T-CONSTRUCTION"), oid("N-INCLUSIVE-INDEX"),
            ],
            "accepted_proof_leaf_ids": [],
            "proof_leaf_cut_set": [
                oid("T-CONSTRUCTION"), oid("N-SHARP-DIMENSION"),
                oid("L-RADIX-NONZERO"), oid("L-RADIX-FLOOR"),
                oid("L-AMBIENT-FIT"), oid("N-RPOW-EXP"),
                oid("L-PROXY-RPOW-IDENTITY"), oid("L-PROXY-SLACK"),
                oid("L-RECIPROCAL-CORE"), oid("L-LINEAR-CEILING"),
                oid("L-LINEAR-INCREMENT"), oid("L-DIMENSION-SLACK"),
                oid("L-LOG-DIMENSION"), oid("N-INCLUSIVE-INDEX"),
            ],
            "remaining_root_cut_set": [
                oid("T-CONSTRUCTION"), oid("N-SHARP-DIMENSION"), oid("L-RADIX-NONZERO"),
                oid("L-RADIX-FLOOR"), oid("L-AMBIENT-FIT"),
                oid("N-RPOW-EXP"), oid("L-PROXY-RPOW-IDENTITY"),
                oid("L-PROXY-SLACK"), oid("L-RECIPROCAL-CORE"),
                oid("L-LINEAR-CEILING"), oid("L-LINEAR-INCREMENT"),
                oid("L-DIMENSION-SLACK"), oid("L-LOG-DIMENSION"),
                oid("N-INCLUSIVE-INDEX"),
                oid("S-FOUNDATION"), oid("X-SOURCE"), oid("X-PROVENANCE"),
                oid("X-TRUST"), oid("X-READABLE"), oid("X-WORKFLOW"),
            ],
            "reason": (
                "The imported construction and local index adapter are checked candidates only, "
                "not accepted proof leaves. The twelve unimplemented sharp parameter/analytic "
                "leaves and six release overlays also remain open, so no root closure is recorded."
            ),
        },
    }

    specs = {
        "schema_version": "stage1-validation-specs/1.0",
        "normative_profile": "machine-theorem-assurance/1.0",
        "item_id": ITEM,
        "theorem_id": THEOREM,
        "recipe_scope_boundary": (
            "This aggregate architecture recipe covers the frozen inventory but is not a "
            "distinct accepted node receipt or M0 closure claim."
        ),
        "recipes": [{
            "recipe_id": "VAL-M0957-OBLIGATION-BUNDLE",
            "cwd": ".",
            "argv": ["python3", "-B", f"Stage1_Instances/{THEOREM}/check_obligation_tree.py"],
            "env_allowlist": {"LC_ALL": "C", "TZ": "UTC"},
            "timeout_seconds": 300,
            "network_policy": "denied",
            "expected_exit": 0,
            "expected_outputs": [{
                "path_or_stream": "stdout",
                "semantic_hash_policy": "contains PASS THM-M-0957 obligation tree",
            }],
            "covered_obligation_ids": ids,
            "covered_declarations": [
                "Stage1Instances.THM_M_0957.BehrendConstructionTarget",
                "Stage1Instances.THM_M_0957.sourceThreeAPFree_iff_threeAPFree",
                "Stage1Instances.THM_M_0957.behrendConstructionTarget_iff_finiteSet",
                "Behrend.bound_aux",
                "Stage1Instances.THM_M_0957_ObligationTree.pinnedQuantitativeConstruction",
                "Stage1Instances.THM_M_0957_ObligationTree.pinnedIndexMonotonicity",
                "Stage1Instances.THM_M_0957_ObligationTree.parameterAdmissibility_of_dimension_and_radix",
                "Stage1Instances.THM_M_0957_ObligationTree.proxyLogLower_of_identity_and_slack",
                "Stage1Instances.THM_M_0957_ObligationTree.reciprocalLoss_of_balanced_core",
                "Stage1Instances.THM_M_0957_ObligationTree.linearLoss_of_ceiling_and_increment",
                "Stage1Instances.THM_M_0957_ObligationTree.subleadingLoss_of_dimension_and_log",
                "Stage1Instances.THM_M_0957_ObligationTree.proxyAsymptotic_of_dimension_and_bridge",
                "Stage1Instances.THM_M_0957_ObligationTree.ratioAsymptotic_of_proxy_floor_and_dimension",
                "Stage1Instances.THM_M_0957_ObligationTree.sharpEstimate_of_normalization_and_ratio",
                "Stage1Instances.THM_M_0957_ObligationTree.sharpParameters_of_components",
                "Stage1Instances.THM_M_0957_ObligationTree.exactAssembly_of_children",
                "Stage1Instances.THM_M_0957_ObligationTree.root_of_exactAssembly",
                "validator-only Stage1Instances.THM_M_0957_ObligationTree.root_eq_actualCanonical",
            ],
            "evidence_boundary": (
                "Provisional architecture self-test only; proof and validation phases must emit "
                "declaration-specific accepted receipts before any machine closure."
            ),
        }],
    }
    return registry, bundle, specs


def main() -> None:
    values = build()
    for name, value in zip(
        ("obligation-registry.json", "typed-graphs.json", "validation-specs.json"),
        values,
    ):
        (HERE / name).write_text(
            json.dumps(value, indent=2, ensure_ascii=True) + "\n", encoding="utf-8"
        )
    edge_count = sum(len(value["edges"]) for value in values[1]["graphs"].values())
    print(f"wrote {len(ROWS)} obligations and {edge_count} typed edges")
    print(f"registry denominator sha256: {values[0]['denominator_sha256']}")


if __name__ == "__main__":
    main()
