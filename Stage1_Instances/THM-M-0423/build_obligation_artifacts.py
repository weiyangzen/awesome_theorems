#!/usr/bin/env python3
"""Build the THM-M-0423 rev-5.6 obligation architecture.

The registry is deliberately closure-blind.  It records a source-informed
implementation route, including every currently known hard boundary, without
promoting the small Lean harness in ObligationTree.lean to accepted evidence.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ITEM = "S56-M-0423-OBLIGATION_TREE"
THEOREM = "THM-M-0423"
PREFIX = "M0423-"
BASE_REVISION = "80f0191c83a1bb4026c2d490be957cf109464de1"
BASE_TREE = "b89a01cfc623bf97d1896fb3534a1ac24381fa71"
ROOT_EXPRESSION = "4b5061f2c6f01173d7cb6c9b7005ca489aaa1da1f5740e980ea477d37ae04738"
V1_DENOMINATOR = "1476e01a2281846a9ba95f86c32ccbb018134eed8dad8bbd69104b112b3a13ca"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"


def digest(value: object) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def stage(inference: str, output: str) -> tuple[str, str]:
    return inference, output


SPECS: list[dict] = []


def add(
    oid: str,
    kind: str,
    risk: str,
    claim: str,
    formal: str,
    output: str,
    locator: str,
    budget: int,
    stages: tuple[tuple[str, str], ...],
    *,
    machine: str = "required",
    human: str = "required",
    readable: str = "required",
    candidate: str = "M4_no_implemented_exact_body",
    body: str | None = None,
) -> None:
    SPECS.append({
        "id": oid,
        "kind": kind,
        "risk": risk,
        "claim": claim,
        "formal": formal,
        "output": output,
        "locator": locator,
        "budget": budget,
        "stages": stages,
        "machine": machine,
        "human": human,
        "readable": readable,
        "candidate": candidate,
        "body": body,
    })


# Statement and assurance overlays.  These are root-relevant registry entries,
# but they are never proof premises and cannot create machine-proof credit.
add(
    "M0423-S-INTERFACE", "definition", "high",
    "Fix the arbitrary number field, finite-dimensional module, nondegenerate quadratic form, nonzero isotropy predicate, and the two concrete completion families.",
    "Stage1.THM_M_0423.HasseMinkowskiStatement",
    "The exact ordered binders and conclusion interface serialized by statement.json.",
    "Statement.lean:20-63; statement.json", 20,
    (stage("Read the elaborated declaration rather than the historical prose label and retain every universe, typeclass, hypothesis, and completion binder.", "The canonical Lean interface with all binders and local predicates fixed."),
     stage("Compare the printed expression with the statement-phase SHA-256 and reject any coercion, universe, or binder drift.", "The exact ordered binders and conclusion interface serialized by statement.json.")),
    machine="informational", candidate="M3_exact_statement_interface",
)
add(
    "M0423-S-BOUNDARY", "definition", "high",
    "Keep the nonzero witness and nondegeneracy hypothesis, include finite and infinite completions, and exclude unrestricted Hasse principles and rational-only substitutes.",
    "Stage1.THM_M_0423.IsIsotropic plus the four statement mutations",
    "The exact degenerate-case, domain, binder-scope, and place-family boundary.",
    "Statement.lean:20-63; StatementMutations.lean", 18,
    (stage("Use the mutation probes to distinguish removal of nondegeneracy, specialization to Q, changed binder scope, and admission of the zero vector.", "Four independently failing non-equivalent boundary mutations."),
     stage("Retain every finite and infinite place in the positive target while excluding general varieties, integral solubility, and Q-only claims.", "The exact degenerate-case, domain, binder-scope, and place-family boundary.")),
    machine="informational", candidate="M3_checked_statement_boundary",
)
add(
    "M0423-S-COORDINATES", "transport", "high",
    "Relate the coordinate-free form to diagonal and homogeneous-polynomial presentations in both directions, including scalar extension and nonzero-witness transport.",
    "planned exact signature: coordinate, diagonal, and polynomial presentations are pairwise isometric and preserve global and completion-wise IsIsotropic",
    "A bidirectional presentation transport with no theorem strengthening.",
    "source_statement_crosswalk.md; no checked alternate encoding", 42,
    (stage("Choose a finite basis and record the coordinate quadratic polynomial together with the induced linear equivalence.", "A coordinate presentation of the same quadratic form."),
     stage("Prove that the equivalence and every scalar extension preserve nonzero isotropic witnesses in both directions.", "A bidirectional presentation transport with no theorem strengthening.")),
    machine="informational",
)
add(
    "M0423-S-FOUNDATION", "certificate", "critical",
    "Account for propext, Classical.choice, Quot.sound, the pinned Lean/mathlib artifacts, and the prohibition on placeholders, unsafe declarations, oracles, and unreviewed native computation.",
    "planned accepted foundation and TCB inclusion predicate for every root-relevant declaration",
    "The release foundation, computation, and TCB boundary.",
    "ObligationTree.lean axiom probes; anchor-audit.json", 36,
    (stage("Inventory the axioms reported for each checked local declaration and distinguish a warm worker probe from an accepted transitive trust closure.", "A candidate axiom inventory limited to propext, Classical.choice, and Quot.sound."),
     stage("Bind executables, compiled artifacts, source hashes, unsafe/oracle scans, and independent replay before accepting the profile.", "The release foundation, computation, and TCB boundary.")),
    machine="informational", human="not_applicable",
)
add(
    "M0423-X-MATHLIB", "bridge", "critical",
    "Bind every used tensor-product, quadratic-form, place/completion, real-classification, approximation, and algebraic declaration to the pinned mathlib body and dependency closure.",
    f"pinned mathlib support boundary at {MATHLIB_REVISION}",
    "Immutable support-declaration provenance without proof credit.",
    "anchor-audit.json mathlib_candidates; future proof receipts", 45,
    (stage("Resolve each candidate declaration to its source file, exact type, body identity, and direct dependencies at the pinned revision.", "A declaration-level pinned support inventory."),
     stage("Deduplicate wrappers and close the transitive body, license, and trust graph before any E1 claim.", "Immutable support-declaration provenance without proof credit.")),
    machine="informational", human="not_applicable",
)
add(
    "M0423-X-EXTERNAL", "bridge", "high",
    "Preserve the two immutable rational-only, placeholder-contaminated external candidates as rejected audit evidence and never use them as proof premises.",
    "anchor-audit candidates S56-M-0423-E01 and S56-M-0423-E02",
    "The exact scope, placeholder, toolchain, and license blockers for both external candidates.",
    "anchor-audit.json external_candidates", 24,
    (stage("Compare each candidate root with the arbitrary-number-field target and record the strict Q-only specialization.", "Two statement-mismatched external candidates."),
     stage("Follow the terminal bodies to their direct placeholders and retain the toolchain/license blockers.", "The exact scope, placeholder, toolchain, and license blockers for both external candidates.")),
    machine="informational", human="not_applicable", candidate="M5_rejected_external_candidates",
)
add(
    "M0423-X-SOURCE", "terminal", "critical",
    "Map every mathematical proof node to a pinpoint primary source, its assumptions, dependencies, correction status, and an independent reviewer.",
    "planned section-8.1 source-coverage predicate over required_human_source",
    "Node-level primary-source coverage without machine-proof credit.",
    "source_statement_crosswalk.md; Hasse 1924 pp. 113-130", 60,
    (stage("Replace the broad bibliographic anchor with theorem/page/premise locators for every material transition in the selected route.", "A complete candidate source-to-node crosswalk."),
     stage("Check edition identity, assumptions, errata, translations, and mathematical fidelity through an independent source review.", "Node-level primary-source coverage without machine-proof credit.")),
    machine="informational", readable="not_applicable",
)
add(
    "M0423-X-PROVENANCE", "certificate", "critical",
    "Resolve local wrappers, terminal bodies, immutable revisions, licenses, direct dependencies, and transitive declaration provenance without duplicate credit.",
    "planned content-addressed provenance-closure predicate",
    "Formal-body provenance without mathematical proof credit.",
    "anchor-audit.json; future proof receipts", 54,
    (stage("Associate every implemented or imported proof candidate with one terminal body identity and immutable source hash.", "A deduplicated direct provenance graph."),
     stage("Close transitive declarations, licenses, dependency pins, and invalidation inputs in a content-addressed receipt.", "Formal-body provenance without mathematical proof credit.")),
    machine="informational", human="not_applicable",
)
add(
    "M0423-X-TRUST", "certificate", "critical",
    "Audit the transitive Lean TCB, compiled artifacts, executables, axioms, unsafe/oracle boundaries, and replay environment for all credited bodies.",
    "planned accepted trust-closure predicate",
    "Release-grade trust inventory without proof credit.",
    "ObligationTree.lean probes; future validation and release receipts", 54,
    (stage("Recompute axiom and constant dependencies from terminal declarations rather than trusting wrapper labels.", "A transitive declaration and axiom inventory."),
     stage("Bind the inventory to toolchain binaries, compiled artifacts, source inputs, oracle policy, and an independent replay.", "Release-grade trust inventory without proof credit.")),
    machine="informational", human="not_applicable",
)
add(
    "M0423-X-READABLE", "terminal", "high",
    "Produce an independently reviewed readable reconstruction with assumptions, branch logic, boundaries, and formal/source anchors for every readable-required node.",
    "planned section-8 readable-coverage predicate",
    "Reader-facing proof reconstruction without machine-proof credit.",
    "obligation-tree.md is architecture only", 70,
    (stage("Expand each frozen ledger into a reader-first argument that explicitly marks every still-planned transition.", "A complete draft reconstruction with stable node anchors."),
     stage("Obtain independent review of mathematical fidelity, source mapping, formal correspondence, and all boundary sentences.", "Reader-facing proof reconstruction without machine-proof credit.")),
    machine="informational", human="not_applicable",
)
add(
    "M0423-X-WORKFLOW", "certificate", "high",
    "Require dependency-legal proof, validation, release, freshness, revocation, and independent-verification receipts before any promotion.",
    "planned task and receipt acceptance predicate",
    "Workflow acceptance without mathematical proof credit.",
    "Docs/Stage1_Execution_DAG_rev-5.6.json", 24,
    (stage("Check the anchor-audit, tree, proof, validation, and release task edges against the authoritative DAG.", "A topologically valid task projection."),
     stage("Require master acceptance, freshness, revocation, hermetic replay, and independent verification for every promoted node.", "Workflow acceptance without mathematical proof credit.")),
    machine="informational", human="not_applicable",
)


# Proof architecture.  Planned formal signatures are canonical targets for the
# next phase, not declarations asserted to exist in the current environment.
add(
    "M0423-ROOT", "root", "critical",
    "Every nondegenerate finite-dimensional quadratic form over an arbitrary number field is isotropic exactly when it is isotropic at every finite and infinite completion.",
    "Stage1.THM_M_0423.HasseMinkowskiStatement",
    "Stage1.THM_M_0423.HasseMinkowskiStatement.",
    "Statement.lean:57-63; statement.json expression hash", 12,
    (stage("Recompose the exact two directional conclusions under the frozen nondegeneracy hypothesis, preserving the conjunction of both completion families.", "Stage1.THM_M_0423.HasseMinkowskiStatement."),),
    candidate="M3_conditional_composition_harness_only",
)
add(
    "M0423-B-DIRECTIONS", "branch", "critical",
    "Split the exact equivalence into global-to-local and local-to-global implications and require both conclusions under the same frozen binders.",
    "planned exact package: GlobalToLocalObligation and LocalToGlobalObligation, jointly yielding HasseMinkowskiStatement",
    "Both exact directional implications with an exhaustive recomposition map.",
    "ObligationTree.lean:23-95; conditional harness only", 14,
    (stage("Pair the functorial implication with the hard Hasse-Minkowski implication, then feed both to the exact iff constructor without dropping nondegeneracy or either place family.", "Both exact directional implications with an exhaustive recomposition map."),),
    candidate="M3_conditional_composition_harness_only",
)
add(
    "M0423-T-GLOBAL-LOCAL", "terminal", "high",
    "Carry a nonzero global isotropic witness to every finite and infinite completion by scalar extension.",
    "Stage1.THM_M_0423.ObligationTree.GlobalToLocalObligation",
    "Global isotropy implies both exact completion-wise isotropy predicates.",
    "ObligationTree.lean:23-29,60-71", 18,
    (stage("Instantiate the scalar-extension witness package at each finite adic completion and discharge its CharZero instance.", "Isotropy at every finite completion."),
     stage("Instantiate the same package at each infinite completion and retain the nonzero witness.", "Global isotropy implies both exact completion-wise isotropy predicates.")),
    candidate="M0-L_requires_E0", body="local:ObligationTree.lean#global_to_local",
)
add(
    "M0423-C-PURE-TENSOR", "construction", "high",
    "For every field extension, construct 1 tensor x from a nonzero isotropic x and prove both its nonzeroness and its zero quadratic value.",
    "Stage1.THM_M_0423.ObligationTree.isotropic_after_baseChange",
    "A nonzero isotropic witness for the base-changed form.",
    "ObligationTree.lean:45-58", 20,
    (stage("Use faithful flatness to show that x maps injectively to 1 tensor x and hence remains nonzero.", "A nonzero pure tensor in the scalar extension."),
     stage("Evaluate the base-changed quadratic form on the pure tensor and map Q(x)=0 through the algebra homomorphism.", "A nonzero isotropic witness for the base-changed form.")),
    candidate="M0-L_requires_E0", body="local:ObligationTree.lean#isotropic_after_baseChange",
)
add(
    "M0423-X-FLAT-INJECTION", "bridge", "high",
    "The map x to 1 tensor x is injective for a field extension, so a nonzero global vector remains nonzero after scalar extension.",
    "Module.FaithfullyFlat.tensorProduct_mk_injective",
    "Injectivity of the pure-tensor unit map used by the witness construction.",
    "Mathlib/RingTheory/Flat/FaithfullyFlat/Algebra.lean", 18,
    (stage("Instantiate faithful flatness of the field extension and the tensor-product map on the frozen module.", "An injective linear map x |-> 1 tensor x."),
     stage("Apply injectivity to the inequality x != 0 rather than relying on an unproved tensor normal-form fact.", "Injectivity of the pure-tensor unit map used by the witness construction.")),
    candidate="M0-W_requires_E1", body=f"mathlib-{MATHLIB_REVISION}:Module.FaithfullyFlat.tensorProduct_mk_injective",
)
add(
    "M0423-L-BASECHANGE-EVAL", "core_lemma", "normal",
    "Evaluate the base-changed quadratic form at 1 tensor x as the algebra-map image of Q(x).",
    "QuadraticForm.baseChange_tmul",
    "The base-changed quadratic value of the pure tensor is zero whenever Q(x)=0.",
    "Mathlib/LinearAlgebra/QuadraticForm/TensorProduct.lean", 12,
    (stage("Specialize baseChange_tmul to scalar 1 and rewrite the quadratic scaling factor.", "baseChange(Q)(1 tensor x) = algebraMap(Q(x))."),
     stage("Rewrite Q(x)=0 and preserve the target field's zero through the algebra map.", "The base-changed quadratic value of the pure tensor is zero whenever Q(x)=0.")),
    candidate="M0-W_requires_E1", body=f"mathlib-{MATHLIB_REVISION}:QuadraticForm.baseChange_tmul",
)
add(
    "M0423-T-LOCAL-GLOBAL", "terminal", "critical",
    "From isotropy at every finite and infinite completion, derive a nonzero global isotropic vector for the original nondegenerate form.",
    "Stage1.THM_M_0423.ObligationTree.LocalToGlobalObligation",
    "Stage1.THM_M_0423.IsIsotropic Q.",
    "ObligationTree.lean:30-39; selected classification-and-comparison route", 24,
    (stage("Apply the fully expanded extraction package to the frozen nondegeneracy and the two exact completion-wise isotropy hypotheses.", "Stage1.THM_M_0423.IsIsotropic Q."),),
)
add(
    "M0423-N-DIAGONALIZE", "normalization", "critical",
    "Choose a finite basis, diagonalize the nondegenerate form with nonzero coefficients, and preserve global and completion-wise isotropy in both directions.",
    "planned exact package: a diagonal weighted-squares form, an isometry Q ~= diag(a), all a_i != 0, and global/local isotropy iff transports",
    "A diagonal nondegenerate representative with checked global and local transports.",
    "QuadraticForm diagonalization candidates; exact wrapper not implemented", 72,
    (stage("Assemble the basis diagonalization, coefficient nonvanishing, global witness transport, and scalar-extension transport without identifying any of them with the final theorem.", "A diagonal nondegenerate representative with checked global and local transports."),),
)
add(
    "M0423-T-DIAGONAL-MERGE", "terminal", "high",
    "Recombine the diagonal representative, coefficient invariant, and both transport directions into one normalization package.",
    "planned exact diagonal-normalization recomposition",
    "The complete diagonalization package consumed by the hard direction.",
    "future abstract-child composition harness", 24,
    (stage("Pair the diagonal isometry with nonzero coefficients and prove that its global and every completion base change preserve IsIsotropic both ways.", "The complete diagonalization package consumed by the hard direction."),),
)
add(
    "M0423-C-BASIS-DIAGONAL", "construction", "critical",
    "Construct a basis in which Q is a weighted sum of squares and record the explicit isometry equivalence.",
    "planned exact wrapper around QuadraticForm.equivalent_weightedSumSquares_units_of_nondegenerate'",
    "A finite coefficient family and isometry Q ~= weightedSumSquares(a).",
    "pinned quadratic-form diagonalization declarations; wrapper audit open", 48,
    (stage("Choose a finite basis for V and express the quadratic form through its diagonal coefficient function.", "A coordinate weighted-squares presentation."),
     stage("Package the change of basis as a quadratic-form isometry rather than mere equality of polynomial values.", "A finite coefficient family and isometry Q ~= weightedSumSquares(a).")),
)
add(
    "M0423-L-NONDEGENERATE-COEFFICIENTS", "core_lemma", "high",
    "For a diagonal representative of a nondegenerate form, every diagonal coefficient is nonzero.",
    "planned exact signature: Nondegenerate(diag a) -> forall i, a i != 0",
    "A unit/nonzero coefficient family suitable for discriminants and Hilbert symbols.",
    "quadratic radical of a diagonal form; exact lemma audit open", 30,
    (stage("Assume a diagonal coefficient vanishes and place the corresponding basis vector in the bilinear radical.", "A radical witness from any zero diagonal coefficient."),
     stage("Use nondegeneracy and basis-vector nonzeroness to rule out that witness.", "A unit/nonzero coefficient family suitable for discriminants and Hilbert symbols.")),
)
add(
    "M0423-T-GLOBAL-ISOTROPY-TRANSPORT", "transport", "high",
    "A quadratic-form isometry transports nonzero isotropic witnesses globally in both directions.",
    "planned exact signature: Q.IsometryEquiv Q' -> (IsIsotropic Q <-> IsIsotropic Q')",
    "Bidirectional global isotropy transport along the diagonalizing isometry.",
    "QuadraticForm.IsometryEquiv map and inverse", 24,
    (stage("Map a witness through the linear equivalence and preserve nonzeroness by injectivity.", "Forward transport of a nonzero vector."),
     stage("Rewrite the quadratic value with the isometry law and repeat with the inverse equivalence.", "Bidirectional global isotropy transport along the diagonalizing isometry.")),
)
add(
    "M0423-T-LOCAL-BASECHANGE-TRANSPORT", "transport", "critical",
    "Base changing a quadratic-form isometry to every completion preserves completion-wise nonzero isotropy in both directions.",
    "planned exact signature: baseChange of an isometry equivalence induces IsIsotropicAfterBaseChange iff at each finite/infinite completion",
    "Bidirectional completion-wise isotropy transport for the diagonalizing isometry.",
    "QuadraticForm baseChange functoriality; exact isometry wrapper missing", 44,
    (stage("Base change the linear equivalence and prove its inverse remains inverse over the completion field.", "A completion-wise linear equivalence."),
     stage("Transport nonzero witnesses and quadratic values along the base-changed isometry uniformly for both completion families.", "Bidirectional completion-wise isotropy transport for the diagonalizing isometry.")),
)
add(
    "M0423-N-PLACE-FAMILY", "normalization", "high",
    "Normalize the disjoint finite and infinite completion predicates to the complete place family used by the invariant route.",
    "planned exact package equating the frozen conjunction with universal local data over finite plus infinite places",
    "One exhaustive local-data family with no omitted archimedean or nonarchimedean place.",
    "Statement.lean:29-49; number-field place APIs", 36,
    (stage("Combine the finite-place carrier, infinite-place carrier, and their exhaustiveness result into one indexed family while preserving both original quantifiers.", "One exhaustive local-data family with no omitted archimedean or nonarchimedean place."),),
)
add(
    "M0423-T-PLACE-MERGE", "terminal", "high",
    "Recompose finite-place coverage, infinite-place coverage, and their disjoint exhaustiveness into the exact local family.",
    "planned exact finite/infinite place recomposition",
    "The normalized all-place package consumed by reciprocity and realization.",
    "future abstract-child composition harness", 22,
    (stage("Map each original local hypothesis into its tagged place branch and use exhaustiveness to recover every tagged local datum, with no converse strengthening.", "The normalized all-place package consumed by reciprocity and realization."),),
)
add(
    "M0423-C-FINITE-PLACE-COVERAGE", "construction", "normal",
    "Index every nonarchimedean completion used in the proof by the exact NumberField.FinitePlace binder in the statement.",
    "planned exact identity/transport for NumberField.FinitePlace completion fields",
    "Complete finite-place coverage with the statement's completion types.",
    "Statement.lean:29-38", 18,
    (stage("Unfold the finite local predicate and retain its maximal-ideal adic completion without replacing it by an abstract local field.", "Complete finite-place coverage with the statement's completion types."),),
)
add(
    "M0423-C-INFINITE-PLACE-COVERAGE", "construction", "normal",
    "Index every archimedean completion used in the proof by the exact NumberField.InfinitePlace binder in the statement.",
    "planned exact identity/transport for NumberField.InfinitePlace.Completion",
    "Complete infinite-place coverage with the statement's completion types.",
    "Statement.lean:40-49", 18,
    (stage("Unfold the infinite local predicate and retain w.Completion together with its algebra and CharZero structure.", "Complete infinite-place coverage with the statement's completion types."),),
)
add(
    "M0423-L-PLACE-EXHAUSTIVENESS", "core_lemma", "high",
    "Every place used by the selected global invariant theorem belongs to exactly the finite or infinite branch represented in the frozen statement.",
    "planned exact place-partition theorem and completion identification",
    "A disjoint exhaustive finite/infinite place partition.",
    "number-field place/completion API; selected source route audit open", 32,
    (stage("Relate valuations/nonarchimedean places to FinitePlace and embeddings/archimedean places to InfinitePlace.", "Surjectivity onto both concrete place carriers."),
     stage("Prove disjointness and that the completion fields agree with those used by the invariant theorems.", "A disjoint exhaustive finite/infinite place partition.")),
)
add(
    "M0423-B-LOCAL-PLACES", "branch", "critical",
    "Split local classification into the archimedean and nonarchimedean branches and recompose their exact outputs for the normalized all-place family.",
    "planned exact local-classification branch package",
    "Classification and isotropy data at every frozen completion.",
    "selected invariant route; primary-source node map open", 26,
    (stage("Apply the local-place merge to the finite and infinite classification packages under the normalized place partition.", "Classification and isotropy data at every frozen completion."),),
)
add(
    "M0423-T-LOCAL-PLACES-MERGE", "terminal", "critical",
    "Use the exhaustive place partition to merge the finite and infinite local classification packages.",
    "planned exact local-place recomposition",
    "A uniform local classification and isotropy interface over all places.",
    "future abstract-child composition harness", 24,
    (stage("Dispatch a normalized place to its unique branch, transport its completion type, and return that branch's full classification and isotropy criterion.", "A uniform local classification and isotropy interface over all places."),),
)
add(
    "M0423-L-INFINITE", "core_lemma", "critical",
    "Classify nondegenerate forms at every infinite completion and give the exact local isotropy and hyperbolic-splitting interface.",
    "planned exact archimedean local-classification package",
    "The complete infinite-place classification branch.",
    "real/complex completion APIs and quadratic classification", 52,
    (stage("Use the real/complex dichotomy merge to transport, classify, and derive isotropy criteria in both branches.", "The complete infinite-place classification branch."),),
)
add(
    "M0423-T-INFINITE-MERGE", "terminal", "high",
    "Split each infinite place into real or complex, consume both branch packages, and recompose the result for its actual completion.",
    "planned exact real/complex completion recomposition",
    "Classification and isotropy data for every infinite completion.",
    "future abstract-child composition harness", 24,
    (stage("Use the dichotomy proof to select the real or complex transport, apply its classification and isotropy criterion, and transport the result back to w.Completion.", "Classification and isotropy data for every infinite completion."),),
)
add(
    "M0423-C-INFINITE-DICHOTOMY", "construction", "high",
    "For every infinite place, produce the exclusive real/complex case and the corresponding completion equivalence.",
    "planned exact wrapper around InfinitePlace isReal/isComplex dichotomy and completion equivalences",
    "An exhaustive tagged real-or-complex completion equivalence.",
    "Mathlib NumberField Completion InfinitePlace", 28,
    (stage("Decide the real versus complex embedding class and rule out overlap at the place level.", "An exclusive real/complex tag."),
     stage("Attach the pinned completion ring/field equivalence for the selected tag.", "An exhaustive tagged real-or-complex completion equivalence.")),
)
add(
    "M0423-B-INFINITE-REAL", "branch", "high",
    "At a real infinite place, transport to R, classify by signature, and derive the exact nonzero-isotropy criterion.",
    "planned exact real-place classification package",
    "The real-completion classification and isotropy conclusion.",
    "InfinitePlace real equivalence; QuadraticForm.Real", 44,
    (stage("Compose the completion transport, Sylvester classification, and signature isotropy criterion while retaining nondegeneracy.", "The real-completion classification and isotropy conclusion."),),
)
add(
    "M0423-N-REAL-COMPLETION-TRANSPORT", "transport", "high",
    "Transport a form, nondegeneracy, and nonzero isotropy between a real completion and R along the pinned field equivalence.",
    "planned exact wrapper around InfinitePlace.ringEquivRealOfIsReal and quadratic-form scalar transport",
    "Bidirectional real-completion transport for classification and witnesses.",
    "Mathlib NumberField Completion InfinitePlace", 32,
    (stage("Turn the completion ring equivalence into the scalar and module transport required by quadratic forms.", "A quadratic form over R corresponding to the completion form."),
     stage("Transport nondegeneracy, signature data, and nonzero isotropic witnesses in both directions.", "Bidirectional real-completion transport for classification and witnesses.")),
)
add(
    "M0423-L-REAL-CLASSIFICATION", "bridge", "critical",
    "Every finite-dimensional real quadratic form is isometric to a diagonal form with entries 1, 0, and -1, with nondegeneracy excluding the zero block.",
    "planned exact wrapper around QuadraticForm.equivalent_one_zero_neg_one_weighted_sum_squared",
    "A nondegenerate real signature normal form.",
    "anchor-audit candidate S56-M-0423-C03", 46,
    (stage("Instantiate the pinned real diagonalization theorem and extract positive, zero, and negative multiplicities.", "A 1/0/-1 weighted-squares normal form."),
     stage("Use nondegeneracy to eliminate the zero summand and record the isometry and dimensions.", "A nondegenerate real signature normal form.")),
    candidate="M3_exact_mathlib_child_requires_wrapper_and_E1",
)
add(
    "M0423-L-REAL-ISOTROPY", "core_lemma", "high",
    "A nondegenerate real form is isotropic exactly when its signature has both a positive and a negative direction, subject to the low-dimensional boundary.",
    "planned exact signature criterion for the real normal form",
    "The exact real nonzero-isotropy criterion and witness.",
    "real signature algebra; primary-source mapping open", 36,
    (stage("Show a positive and negative coordinate give a scaled two-coordinate zero with a nonzero vector.", "An explicit isotropic witness for an indefinite form."),
     stage("Use positivity or negativity of every nonzero term to rule out a zero for definite forms, including dimensions zero and one.", "The exact real nonzero-isotropy criterion and witness.")),
)
add(
    "M0423-B-INFINITE-COMPLEX", "branch", "high",
    "At a complex infinite place, transport to C, classify the nondegenerate form, and derive its exact nonzero-isotropy boundary.",
    "planned exact complex-place classification package",
    "The complex-completion classification and isotropy conclusion.",
    "InfinitePlace complex equivalence; algebraically closed quadratic forms", 44,
    (stage("Compose the completion transport, complex diagonal classification, and the dimension-sensitive isotropy construction.", "The complex-completion classification and isotropy conclusion."),),
)
add(
    "M0423-N-COMPLEX-COMPLETION-TRANSPORT", "transport", "high",
    "Transport a form, nondegeneracy, and nonzero isotropy between a complex completion and C along the pinned field equivalence.",
    "planned exact wrapper around InfinitePlace.ringEquivComplexOfIsComplex and quadratic-form scalar transport",
    "Bidirectional complex-completion transport for classification and witnesses.",
    "Mathlib NumberField Completion InfinitePlace", 32,
    (stage("Lift the completion equivalence to the module and quadratic-form data over C.", "A corresponding finite-dimensional complex quadratic form."),
     stage("Transport nondegeneracy, diagonal data, and nonzero witnesses through the equivalence and its inverse.", "Bidirectional complex-completion transport for classification and witnesses.")),
)
add(
    "M0423-L-COMPLEX-CLASSIFICATION", "core_lemma", "critical",
    "A nondegenerate finite-dimensional quadratic form over C is isometric to a sum of nonzero squares.",
    "planned exact algebraically-closed-field diagonal classification specialized to C",
    "A complex diagonal normal form with every coefficient scaled to one.",
    "algebraically closed square roots plus diagonalization; exact Lean anchor missing", 44,
    (stage("Diagonalize the form and use nondegeneracy to make every coefficient nonzero.", "A diagonal complex form with nonzero coefficients."),
     stage("Choose square roots of the coefficients and rescale the basis to obtain unit coefficients.", "A complex diagonal normal form with every coefficient scaled to one.")),
)
add(
    "M0423-L-COMPLEX-ISOTROPY", "core_lemma", "high",
    "A nondegenerate complex quadratic form has a nonzero isotropic vector exactly in dimension at least two.",
    "planned exact dimension criterion for nondegenerate complex forms",
    "The exact complex nonzero-isotropy criterion and explicit witness.",
    "complex square root of -1 and one-dimensional boundary", 28,
    (stage("For dimension at least two, use coordinates (1,i,0,...) in the unit diagonal normal form.", "An explicit nonzero complex isotropic vector."),
     stage("For dimensions zero or one, use nondegeneracy to rule out a nonzero zero of the form.", "The exact complex nonzero-isotropy criterion and explicit witness.")),
)
add(
    "M0423-L-FINITE", "core_lemma", "critical",
    "Classify nondegenerate quadratic forms over every finite completion by dimension, determinant square class, and Hasse invariant, including Witt decomposition and isotropy.",
    "planned exact nonarchimedean local-classification package for the statement's adic completion fields",
    "The complete finite-place classification branch.",
    "missing from pinned mathlib; primary-source node map open", 64,
    (stage("Assemble the local symbol and Hasse invariant packages with existence, uniqueness, Witt decomposition, and the dimension-sensitive isotropy criterion.", "The complete finite-place classification branch."),),
)
add(
    "M0423-T-FINITE-MERGE", "terminal", "critical",
    "Consume the invariant definitions and every existence, uniqueness, Witt, and isotropy result needed for nonarchimedean classification.",
    "planned exact finite-place classification recomposition",
    "A uniform invariant classification and isotropy interface at every finite place.",
    "future abstract-child composition harness", 28,
    (stage("Package dimension, determinant, and the presentation-independent Hasse invariant; then use local existence/uniqueness and Witt splitting to derive the exact isotropy criterion.", "A uniform invariant classification and isotropy interface at every finite place."),),
)
add(
    "M0423-C-HILBERT-SYMBOL", "construction", "critical",
    "Define the local Hilbert symbol on nonzero square classes at every completion and establish its algebraic and completion-compatibility laws.",
    "planned exact HilbertSymbol package over the normalized place family",
    "A coherent, well-defined local binary symbol family.",
    "Hilbert-symbol API absent from pinned mathlib", 62,
    (stage("Merge the norm/conic definition, square-class descent, bilinearity, symmetry/normalization, and completion compatibility into one symbol interface.", "A coherent, well-defined local binary symbol family."),),
)
add(
    "M0423-T-SYMBOL-MERGE", "terminal", "critical",
    "Recombine the Hilbert-symbol definition with all laws used by local invariants and global reciprocity.",
    "planned exact Hilbert-symbol law-package recomposition",
    "The full local Hilbert-symbol interface with no hidden law premise.",
    "future abstract-child composition harness", 24,
    (stage("Descend the norm/conic predicate to square classes and attach bilinearity, symmetry, normalization, and compatibility at each concrete completion.", "The full local Hilbert-symbol interface with no hidden law premise."),),
)
add(
    "M0423-C-SYMBOL-DEFINITION", "construction", "critical",
    "For nonzero a and b over a local field, define (a,b) through solvability of the norm/conic equation and return a two-element sign.",
    "planned exact local Hilbert-symbol definition with nonzero-domain proof",
    "A raw local symbol together with its norm/conic criterion.",
    "classical local-field definition; source pinpoint open", 50,
    (stage("Form the quadratic extension generated by a square root of a and define the positive symbol case by b lying in its norm image.", "A Boolean/sign-valued predicate for nonzero a,b."),
     stage("Prove agreement with the equivalent ternary conic criterion used by quadratic-form calculations.", "A raw local symbol together with its norm/conic criterion.")),
)
add(
    "M0423-L-SYMBOL-WELLDEFINED", "core_lemma", "critical",
    "The raw Hilbert symbol is unchanged when either argument is multiplied by a nonzero square, so it descends to square classes.",
    "planned exact square-class well-definedness theorem",
    "A well-defined binary function on local square classes.",
    "local norm invariance; source pinpoint open", 46,
    (stage("Construct explicit isomorphisms between the quadratic extensions obtained after square rescaling the first argument.", "First-argument square invariance."),
     stage("Use multiplicativity of norms to absorb a square factor in the second argument and descend both arguments.", "A well-defined binary function on local square classes.")),
)
add(
    "M0423-L-SYMBOL-BILINEAR", "core_lemma", "critical",
    "The Hilbert symbol is multiplicative in each square-class argument.",
    "planned exact bilinearity theorem for the local Hilbert symbol",
    "Bilinearity on the two local square-class groups.",
    "local norm-residue algebra; source pinpoint open", 58,
    (stage("Prove (aa',b)=(a,b)(a',b) using the norm-residue description and local square-class relations.", "Multiplicativity in the first argument."),
     stage("Transfer the result through symmetry or prove the corresponding norm identity for the second argument.", "Bilinearity on the two local square-class groups.")),
)
add(
    "M0423-L-NORM-RESIDUE-BILINEARITY", "bridge", "critical",
    "The quadratic norm-residue character over a local field is additive in each Kummer class, and its sign realization is the Hilbert symbol.",
    "planned exact degree-two local norm-residue pairing bilinearity theorem",
    "Bilinearity of the local Kummer/norm-residue pairing before translation to Hilbert signs.",
    "local Kummer theory and cup-product bilinearity; source and Lean implementation open", 96,
    (stage("Identify nonzero square classes with degree-one Kummer cohomology and the quadratic norm-residue symbol with their cup product.", "A cohomological local pairing on square classes."),
     stage("Use additivity of cup product in both factors and evaluate the invariant in the two-element sign group.", "Bilinearity of the local Kummer/norm-residue pairing before translation to Hilbert signs.")),
)
add(
    "M0423-L-SYMBOL-SYMMETRY-NORMALIZATION", "core_lemma", "high",
    "The Hilbert symbol is symmetric and satisfies the unit, square, and (a,-a) normalization identities used in diagonal transformations.",
    "planned exact symmetry and normalization law bundle",
    "Symmetry and every named normalization identity used downstream.",
    "local Hilbert-symbol identities; source pinpoint open", 42,
    (stage("Exchange the two variables in the conic equation to prove symmetry.", "Symmetry of the local symbol."),
     stage("Construct elementary norm witnesses for 1, squares, and -a and combine them with bilinearity.", "Symmetry and every named normalization identity used downstream.")),
)
add(
    "M0423-L-SYMBOL-COMPLETION-COMPATIBILITY", "transport", "high",
    "The symbol transported along each completion equivalence agrees with the normalized finite or infinite place symbol.",
    "planned exact compatibility under finite/infinite completion field equivalences",
    "One coherent symbol value independent of the chosen completion presentation.",
    "completion transport and norm compatibility; wrapper missing", 38,
    (stage("Transport the quadratic extension and norm equation along the field equivalence attached to the place.", "Equality of raw symbol predicates after transport."),
     stage("Descend the equality to square classes and both concrete completion branches.", "One coherent symbol value independent of the chosen completion presentation.")),
)
add(
    "M0423-C-HASSE-INVARIANT", "construction", "critical",
    "Define the Hasse invariant from pairwise Hilbert symbols of diagonal coefficients and prove independence of the diagonal presentation without invoking local classification.",
    "planned exact localHasseInvariant package",
    "A presentation-independent local invariant of a nondegenerate quadratic form.",
    "Hasse-invariant API absent from pinned mathlib", 68,
    (stage("Merge the diagonal coefficient product with invariance under generating presentation moves and connectivity of diagonal presentations.", "A presentation-independent local invariant of a nondegenerate quadratic form."),),
)
add(
    "M0423-T-HASSE-MERGE", "terminal", "critical",
    "Consume the diagonal definition, presentation-move invariance, and presentation connectivity to obtain a form-level invariant.",
    "planned exact Hasse-invariant well-definedness recomposition",
    "The Hasse invariant of the form, independent of all basis and diagonalization choices.",
    "future abstract-child composition harness", 26,
    (stage("Apply move invariance along the finite chain connecting any two diagonal presentations and identify the endpoint pair-products.", "The Hasse invariant of the form, independent of all basis and diagonalization choices."),),
)
add(
    "M0423-C-HASSE-DIAGONAL", "construction", "high",
    "For a diagonal form with nonzero coefficients a_i, form the product of (a_i,a_j) over all i<j.",
    "planned exact finite pair-product definition on diagonal coefficient square classes",
    "A local Hasse value for one chosen diagonal presentation.",
    "finite pair product over the Hilbert-symbol package", 30,
    (stage("Map every nonzero coefficient to its local square class and enumerate unordered index pairs without duplication.", "A finite family of pairwise Hilbert symbols."),
     stage("Multiply the signs in the two-element target group and prove independence of pair enumeration.", "A local Hasse value for one chosen diagonal presentation.")),
)
add(
    "M0423-L-HASSE-PRESENTATION-MOVES", "core_lemma", "critical",
    "The diagonal Hasse value, together with dimension and determinant, transforms correctly under permutation, square rescaling, and elementary binary diagonal changes.",
    "planned exact invariance bundle for generators of diagonal-form isometry",
    "Hasse-value invariance under every generating presentation move.",
    "Hilbert-symbol identities and elementary 2x2 isometries", 72,
    (stage("Use commutativity of the pair index set to prove invariance under coefficient permutation.", "Permutation invariance."),
     stage("Use square-class well-definedness to prove invariance under basis-vector rescaling.", "Square-rescaling invariance."),
     stage("Compute the determinant and pair-symbol change for an elementary nondegenerate binary replacement using bilinearity and normalization.", "Hasse-value invariance under every generating presentation move.")),
)
add(
    "M0423-L-DIAGONAL-PRESENTATION-CONNECTIVITY", "core_lemma", "critical",
    "Any two diagonal presentations of isometric nondegenerate forms are connected by a finite sequence of the audited generating moves.",
    "planned exact diagonal-presentation connectivity theorem",
    "A finite move chain between any two diagonalizations of the same form.",
    "quadratic-form congruence generators; source pinpoint open", 74,
    (stage("Factor the change-of-basis congruence into elementary invertible transformations while maintaining a nondegenerate diagonal presentation at each checkpoint.", "A finite chain of elementary congruences."),
     stage("Refine each congruence into permutations, nonzero square rescalings, and audited binary diagonal replacements.", "A finite move chain between any two diagonalizations of the same form.")),
)
add(
    "M0423-L-CONGRUENCE-GENERATORS", "bridge", "critical",
    "Every congruence between nondegenerate diagonal quadratic matrices over a field of characteristic not two is generated, through nondegenerate checkpoints, by permutations, nonzero square rescalings, and elementary binary diagonal replacements.",
    "planned exact generator theorem for diagonal quadratic-form presentations",
    "A finite audited generating-move factorization for any diagonal congruence.",
    "quadratic congruence generator theorem; primary source and Lean implementation open", 100,
    (stage("Factor the change-of-basis matrix into elementary invertible operations while tracking congruence rather than row equivalence.", "A finite sequence of elementary congruence operations."),
     stage("Refine each operation to the three diagonal-preserving move classes and prove every intermediate diagonal block remains nondegenerate.", "A finite audited generating-move factorization for any diagonal congruence.")),
)
add(
    "M0423-L-FINITE-CLASSIFICATION-EXISTENCE", "core_lemma", "critical",
    "Every admissible dimension, determinant square class, and Hasse value over a finite completion is realized by a nondegenerate quadratic form.",
    "planned exact nonarchimedean local invariant-existence theorem",
    "A local form realizing each admissible invariant tuple.",
    "local quadratic-form classification; source pinpoint open", 78,
    (stage("Reduce the tuple to an explicit diagonal coefficient problem in the local square-class group.", "A finite coefficient constraint system."),
     stage("Choose coefficients realizing the determinant and final Hilbert-symbol product, checking dimensions zero and one separately.", "A local form realizing each admissible invariant tuple.")),
)
add(
    "M0423-L-FINITE-CLASSIFICATION-UNIQUENESS", "core_lemma", "critical",
    "Two nondegenerate forms over a finite completion with equal dimension, determinant square class, and Hasse invariant are isometric.",
    "planned exact nonarchimedean local invariant-uniqueness theorem",
    "Completeness of the local invariant tuple for isometry.",
    "local quadratic-form classification; source pinpoint open", 88,
    (stage("Diagonalize both forms and cancel common one-dimensional components using the local representation and Hilbert-symbol criteria.", "Reduced diagonal forms with aligned coefficients."),
     stage("Use equality of determinant and Hasse value to identify the final binary block and recompose the isometry.", "Completeness of the local invariant tuple for isometry.")),
)
add(
    "M0423-L-FINITE-REPRESENTATION", "bridge", "critical",
    "Over a nonarchimedean local field of odd or dyadic residue characteristic, characterize the nonzero values represented by each nondegenerate diagonal form in terms of its dimension, determinant, and Hilbert-symbol data.",
    "planned exact local value-representation theorem for the finite completion fields",
    "The representation criterion used to align and cancel diagonal coefficients in local uniqueness.",
    "local norm groups and binary/ternary representation theory; source pinpoint open", 94,
    (stage("Reduce representation of a nonzero scalar to isotropy of the form orthogonally summed with its negative one-dimensional form.", "A representation-to-isotropy equivalence."),
     stage("Compute the enlarged form's determinant and Hasse invariant and apply the dimension-sensitive local invariant criterion, with dyadic cases explicit.", "The representation criterion used to align and cancel diagonal coefficients in local uniqueness.")),
)
add(
    "M0423-L-FINITE-WITT-DECOMPOSITION", "core_lemma", "critical",
    "Every isotropic nondegenerate local form splits an explicit hyperbolic plane and a nondegenerate orthogonal residual form.",
    "planned exact local Witt-splitting theorem",
    "A hyperbolic plane plus nondegenerate residual decomposition preserving invariants.",
    "Witt decomposition over fields of characteristic not two", 58,
    (stage("Choose a nonzero isotropic vector and, by nondegeneracy, a partner with nonzero polar pairing.", "A nondegenerate two-dimensional subspace containing the isotropic vector."),
     stage("Normalize the partner to obtain a hyperbolic basis and take the orthogonal complement.", "A hyperbolic plane plus nondegenerate residual decomposition preserving invariants.")),
)
add(
    "M0423-L-FINITE-ISOTROPY-CRITERION", "core_lemma", "critical",
    "Give the exact dimension-sensitive criterion for a finite-completion invariant tuple to contain a hyperbolic plane.",
    "planned exact nonarchimedean local isotropy criterion",
    "An iff between local IsIsotropic and the classified invariant condition.",
    "local classification corollary; source pinpoint open", 82,
    (stage("Classify the possible anisotropic residual forms by dimension and invariant tuple without merging distinct boundary cases.", "A bounded list of anisotropic invariant tuples."),
     stage("Show every remaining tuple is represented by a hyperbolic-plane sum and transport the explicit witness through local uniqueness.", "An iff between local IsIsotropic and the classified invariant condition.")),
)


# Global invariant, realization, comparison, and uniqueness route.
add(
    "M0423-L-GLOBAL-CLASSIFICATION", "core_lemma", "critical",
    "From the normalized local isotropy data, construct a global hyperbolic comparison form and identify it with the diagonal input using explicit global invariant existence and uniqueness engines.",
    "planned exact global classification-and-comparison package yielding an isometry diag(Q) ~= H orthogonalSum R",
    "A global isometry from an explicitly isotropic comparison form to the diagonalized input.",
    "selected invariant route; node/page source audit open", 76,
    (stage("Use the diagonalization, normalized all-place family, and complete local-classification interfaces to form the local residual and invariant inputs.", "Normalized local residual data for the diagonal input."),
     stage("Consume the residual realization, comparison, reciprocity, and global uniqueness outputs without invoking this parent as a premise.", "A global isometry from an explicitly isotropic comparison form to the diagonalized input.")),
)
add(
    "M0423-T-GLOBAL-CLASSIFICATION-MERGE", "terminal", "critical",
    "Recompose local hyperbolic residuals, compatible global invariants, their realization, the isotropic comparison form, and global uniqueness.",
    "planned exact global-classification recomposition",
    "The complete algebraic local-to-global comparison package.",
    "future abstract-child composition harness", 32,
    (stage("Use reciprocity-compatible residual data to realize a global residual form, adjoin an explicit hyperbolic plane, verify every local invariant match, and apply the separately proved global uniqueness engine.", "The complete algebraic local-to-global comparison package."),),
)
add(
    "M0423-C-LOCAL-RESIDUALS", "construction", "critical",
    "At every completion, split the locally isotropic form as a hyperbolic plane plus a nondegenerate residual form and record its coherent invariants.",
    "planned exact all-place residual-family package",
    "A completion-indexed family of dimension n-2 residual forms and invariant data.",
    "Witt splitting plus normalized place family", 64,
    (stage("Merge the dimension boundary, hyperbolic splitting, and residual invariant computations uniformly over the finite/infinite place family.", "A completion-indexed family of dimension n-2 residual forms and invariant data."),),
)
add(
    "M0423-T-RESIDUAL-MERGE", "terminal", "critical",
    "Consume the dimension lower bound, local hyperbolic split, and residual invariant computation at every place.",
    "planned exact local-residual recomposition",
    "A coherent nondegenerate residual family suitable for global realization.",
    "future abstract-child composition harness", 26,
    (stage("For each local witness, split a hyperbolic plane, identify the residual dimension n-2, and calculate its determinant and Hasse data with the same normalization conventions.", "A coherent nondegenerate residual family suitable for global realization."),),
)
add(
    "M0423-L-DIMENSION-AT-LEAST-TWO", "core_lemma", "high",
    "A nondegenerate form with a nonzero isotropic vector has dimension at least two.",
    "planned exact signature: Nondegenerate Q -> IsIsotropic Q -> 2 <= finrank K V",
    "The legal n-2 dimension boundary for every local residual.",
    "elementary polar-form argument", 24,
    (stage("Use nondegeneracy to find a vector pairing nontrivially with the nonzero isotropic witness.", "Two linearly independent vectors."),
     stage("Convert linear independence to the finite-dimensional rank inequality.", "The legal n-2 dimension boundary for every local residual.")),
)
add(
    "M0423-L-HYPERBOLIC-SPLIT", "core_lemma", "critical",
    "A nonzero isotropic vector in a nondegenerate form over characteristic not two generates, with a suitable partner, an isometric hyperbolic plane summand.",
    "planned exact field-generic hyperbolic-splitting theorem",
    "An isometry Q ~= H orthogonalSum Qres with Qres nondegenerate.",
    "Witt splitting; exact Lean wrapper missing", 58,
    (stage("Choose a partner with nonzero polar pairing and modify it to become isotropic while preserving the pairing.", "A hyperbolic pair."),
     stage("Prove the pair spans a nondegenerate plane and split its orthogonal complement.", "An isometry Q ~= H orthogonalSum Qres with Qres nondegenerate.")),
)
add(
    "M0423-C-RESIDUAL-INVARIANTS", "construction", "critical",
    "Compute dimension, determinant, and Hasse invariant of the residual after removing a hyperbolic plane, consistently at every completion.",
    "planned exact hyperbolic-residual invariant formulas",
    "Coherent invariant data for every local residual form.",
    "orthogonal-sum determinant and Hasse formulas", 54,
    (stage("Apply the dimension and determinant formulas for orthogonal sums with the fixed hyperbolic plane convention.", "Residual dimension and determinant data."),
     stage("Expand pairwise Hilbert symbols across the orthogonal sum and isolate the residual Hasse factor.", "Coherent invariant data for every local residual form.")),
)
add(
    "M0423-C-GLOBAL-INVARIANTS", "construction", "critical",
    "Extract the global dimension and determinant together with the finite-support family of local Hasse data for the diagonalized form and its residual target.",
    "planned exact global invariant-data record",
    "A normalized global/local invariant tuple with explicit finite support.",
    "diagonal coefficients, local Hasse invariant, all-place normalization", 60,
    (stage("Compute global dimension and determinant square class from the nonzero diagonal coefficient family.", "The global algebraic invariant pair."),
     stage("Map coefficients to every completion, compute local Hasse values, and attach the finite-support certificate used by reciprocity.", "A normalized global/local invariant tuple with explicit finite support.")),
)
add(
    "M0423-L-HILBERT-RECIPROCITY", "bridge", "critical",
    "For global nonzero a and b, all but finitely many local Hilbert symbols are one and the product over every finite and infinite place is one.",
    "planned exact arbitrary-number-field Hilbert reciprocity package",
    "The finite-support global product constraint for local symbols.",
    "ordinary absolute-value product formula is insufficient; theorem missing", 84,
    (stage("Merge the finite-support theorem, local/global symbol comparison, and global reciprocity-product evaluation over the normalized place family.", "The finite-support global product constraint for local symbols."),),
)
add(
    "M0423-T-RECIPROCITY-MERGE", "terminal", "critical",
    "Consume finite support, the local/global norm-residue bridge, and the reciprocity law to derive the Hilbert-symbol product formula.",
    "planned exact Hilbert-reciprocity recomposition",
    "A well-defined finite product of local factors equal to one.",
    "future abstract-child composition harness", 28,
    (stage("Restrict to the finitely many nontrivial places, identify each factor with the global reciprocity invariant, and evaluate their product as the identity sign.", "A well-defined finite product of local factors equal to one."),),
)
add(
    "M0423-C-RECIPROCITY-FINITE-SUPPORT", "construction", "critical",
    "For fixed global nonzero a and b, prove that the local Hilbert symbol is trivial outside an explicit finite set containing dyadic, ramified, and coefficient-supported places.",
    "planned exact finite-support certificate for v |-> (a,b)_v",
    "A finite set containing every nontrivial local factor.",
    "integrality/unramified local norm criterion; source pinpoint open", 66,
    (stage("Choose a finite set containing archimedean, dyadic, ramified, and nonunit coefficient places.", "An explicit finite exceptional set."),
     stage("At every other place, apply the unramified unit norm criterion to prove the local symbol is one.", "A finite set containing every nontrivial local factor.")),
)
add(
    "M0423-L-RECIPROCITY-LOCAL-BRIDGE", "bridge", "critical",
    "Identify each completion Hilbert symbol with the local norm-residue invariant occurring in global reciprocity.",
    "planned exact compatibility theorem between HilbertSymbol and the global reciprocity map",
    "Equality of the local quadratic norm-residue factors.",
    "class-field/norm-residue bridge; no Lean anchor", 82,
    (stage("Map the quadratic extension and its local norm quotient into the local reciprocity group.", "A local norm-residue character."),
     stage("Evaluate that character on the second square class and compare both sign conventions.", "Equality of the local quadratic norm-residue factors.")),
)
add(
    "M0423-L-RECIPROCITY-PRODUCT", "bridge", "critical",
    "The product of all quadratic local norm-residue factors of two global elements is one.",
    "planned exact quadratic global reciprocity/product theorem",
    "The global identity for the finite product of local norm-residue signs.",
    "global reciprocity theorem; primary source and Lean implementation open", 90,
    (stage("Embed the global element diagonally into the ideles and apply global reciprocity triviality on principal ideles.", "Trivial global Artin image for the principal idele."),
     stage("Project to the quadratic character and express the result as the finite product of local signs.", "The global identity for the finite product of local norm-residue signs.")),
)
add(
    "M0423-L-PRINCIPAL-IDELE-RECIPROCITY", "bridge", "critical",
    "The global Artin reciprocity map is trivial on principal ideles, and its quadratic character decomposes as the product of the local norm-residue characters.",
    "planned exact principal-idele global reciprocity theorem with local factorization",
    "Triviality and local-product factorization of the quadratic global reciprocity character.",
    "global class field theory reciprocity; primary source and Lean implementation open", 100,
    (stage("Construct the global reciprocity map on the idele class group and prove the diagonal image of K* lies in its kernel.", "Triviality of global reciprocity on principal ideles."),
     stage("Restrict to the quadratic extension and identify each local component with its local norm-residue character.", "Triviality and local-product factorization of the quadratic global reciprocity character.")),
)
add(
    "M0423-L-INVARIANT-COMPATIBILITY", "core_lemma", "critical",
    "The residual local invariant family extracted from the input satisfies every determinant, signature, finite-support, and product constraint required for global realization.",
    "planned exact admissibility theorem for the residual invariant family",
    "An admissible global-realization input family.",
    "global invariant formulas plus Hilbert reciprocity", 58,
    (stage("Compute the product of residual Hasse factors using the hyperbolic-removal formulas and Hilbert reciprocity.", "The unique product compatibility equation."),
     stage("Combine that equation with common dimension, determinant, real signatures, and finite support.", "An admissible global-realization input family.")),
)
add(
    "M0423-C-GLOBAL-REALIZATION", "construction", "critical",
    "Construct a global nondegenerate residual form realizing the compatible dimension, determinant, signatures, and local Hasse data.",
    "planned exact arbitrary-number-field global invariant-realization theorem",
    "A global residual form matching the prescribed local residual at every place.",
    "Hasse existence/classification route; source mapping open", 94,
    (stage("Merge finite-support reduction, simultaneous approximation, the final reciprocity correction, and local match verification into one global diagonal residual.", "A global residual form matching the prescribed local residual at every place."),),
)
add(
    "M0423-T-REALIZATION-MERGE", "terminal", "critical",
    "Consume every construction and verification needed to realize the compatible local residual invariants globally.",
    "planned exact global-realization recomposition",
    "A nondegenerate global residual and certified local isometries at all places.",
    "future abstract-child composition harness", 30,
    (stage("Choose finitely constrained coefficients by weak approximation, correct the last invariant using reciprocity, and use local classification to verify every finite and infinite completion.", "A nondegenerate global residual and certified local isometries at all places."),),
)
add(
    "M0423-C-FINITE-SUPPORT-REDUCTION", "construction", "critical",
    "Reduce the infinite local realization request to a finite set of nontrivial square-class, sign, determinant, and Hasse constraints.",
    "planned exact finite realization-support set and outside-triviality certificate",
    "A finite family of local neighborhoods whose satisfaction forces all required local invariants.",
    "finite support from residual data and reciprocity", 64,
    (stage("Union the coefficient, dyadic, ramified, archimedean, and nontrivial invariant supports.", "A finite controlling place set."),
     stage("Prove that integral-unit choices outside the set force the default determinant and Hasse behavior.", "A finite family of local neighborhoods whose satisfaction forces all required local invariants.")),
)
add(
    "M0423-L-WEAK-APPROXIMATION", "bridge", "critical",
    "For finitely many finite and infinite places, choose one global element in prescribed open neighborhoods simultaneously.",
    "planned exact number-field weak-approximation theorem for the statement's completion family",
    "A global coefficient meeting every selected local neighborhood.",
    "number-field weak approximation; exact pinned anchor absent", 78,
    (stage("Embed K diagonally into the finite product of selected completions and use density of the diagonal image.", "A global element inside the product neighborhood."),
     stage("Project the product membership to each finite adic and infinite completion constraint.", "A global coefficient meeting every selected local neighborhood.")),
)
add(
    "M0423-C-APPROXIMATE-COEFFICIENTS", "construction", "critical",
    "Choose all but the final diagonal coefficient so their local square classes and real signs meet the finite realization constraints.",
    "planned exact iterative coefficient-approximation construction",
    "A partial global diagonal form satisfying every prescribed constraint except the final Hasse correction.",
    "finite-support reduction plus weak approximation", 76,
    (stage("Choose square-class-stable open neighborhoods for each required coefficient at the finite controlling set.", "A finite simultaneous approximation problem."),
     stage("Apply weak approximation coefficient by coefficient while avoiding zero and preserving the target determinant budget.", "A partial global diagonal form satisfying every prescribed constraint except the final Hasse correction.")),
)
add(
    "M0423-C-FINAL-INVARIANT-CORRECTION", "construction", "critical",
    "Choose the final coefficient so the determinant is exact and every local Hasse value agrees, using the single reciprocity compatibility relation.",
    "planned exact last-coefficient correction theorem",
    "A complete global diagonal form with the prescribed invariant family.",
    "Hilbert reciprocity and admissibility equation", 82,
    (stage("Determine the final coefficient square class from the required global determinant and the earlier coefficients.", "A unique determinant-correcting square class."),
     stage("Use the admissibility product equation to show its Hilbert-symbol effects match at the last uncontrolled place as well.", "A complete global diagonal form with the prescribed invariant family.")),
)
add(
    "M0423-L-LOCAL-MATCH-VERIFICATION", "core_lemma", "critical",
    "At every finite and infinite completion, the realized global residual has the same complete local invariants as the prescribed residual and hence is locally isometric to it.",
    "planned exact all-place local-match theorem",
    "A completion-wise isometry between realized and prescribed residual forms.",
    "finite and infinite local classification packages", 68,
    (stage("Verify dimension, determinant, Hasse value, and real signature equality from the coefficient construction.", "Equality of the complete local invariant tuple."),
     stage("Apply the correct finite, real, or complex uniqueness theorem and transport through the completion equivalence.", "A completion-wise isometry between realized and prescribed residual forms.")),
)
add(
    "M0423-C-ISOTROPIC-COMPARISON", "construction", "critical",
    "Adjoin a fixed global hyperbolic plane to the realized residual and certify that the resulting global form is explicitly isotropic and locally isometric to the input.",
    "planned exact comparison-form package H orthogonalSum R",
    "A globally isotropic comparison form locally isometric to the diagonalized input everywhere.",
    "realization plus hyperbolic-sum invariant formulas", 70,
    (stage("Merge the realized residual, fixed hyperbolic plane, explicit witness, and local invariant-match calculation without reconstructing the residual a second time.", "A globally isotropic comparison form locally isometric to the diagonalized input everywhere."),),
)
add(
    "M0423-T-COMPARISON-MERGE", "terminal", "critical",
    "Consume the one realized residual, hyperbolic plane, explicit witness, and local matching result to build the comparison form.",
    "planned exact isotropic-comparison recomposition",
    "A single comparison object with global witness and all local isometries.",
    "future abstract-child composition harness", 28,
    (stage("Form H orthogonalSum R, insert the named nonzero hyperbolic vector, and combine residual local isometries with the original local hyperbolic decompositions.", "A single comparison object with global witness and all local isometries."),),
)
add(
    "M0423-C-HYPERBOLIC-PLANE", "construction", "high",
    "Define one fixed nondegenerate two-dimensional hyperbolic plane over K with an explicit basis and quadratic convention.",
    "planned exact HyperbolicPlane K package compatible with the residual invariant formulas",
    "A nondegenerate global hyperbolic-plane quadratic form.",
    "standard hyperbolic plane; convention must be fixed", 26,
    (stage("Define the form on K x K by the selected xy or equivalent convention and calculate its polar form matrix.", "A two-dimensional quadratic form with fixed basis."),
     stage("Prove the polar matrix is invertible and record determinant and Hasse conventions.", "A nondegenerate global hyperbolic-plane quadratic form.")),
)
add(
    "M0423-C-EXPLICIT-HYPERBOLIC-WITNESS", "construction", "normal",
    "Exhibit a named nonzero vector in the fixed hyperbolic plane whose quadratic value is zero, and preserve it in an orthogonal sum.",
    "planned exact witness theorem for HyperbolicPlane K and H orthogonalSum R",
    "A nonzero global isotropic witness for the comparison form.",
    "hyperbolic basis vector calculation", 16,
    (stage("Choose the first hyperbolic basis vector and calculate both its nonzeroness and zero quadratic value.", "A nonzero isotropic vector in H."),
     stage("Include the vector with zero residual component in the orthogonal sum.", "A nonzero global isotropic witness for the comparison form.")),
)
add(
    "M0423-L-COMPARISON-INVARIANT-MATCH", "core_lemma", "critical",
    "At every completion, H plus the realized residual has exactly the input form's dimension, determinant, Hasse invariant, and archimedean signature.",
    "planned exact comparison invariant-match theorem",
    "Complete local invariant equality between comparison and input forms.",
    "hyperbolic-removal formulas and realized residual local matches", 64,
    (stage("Use the prescribed residual invariant formulas to reverse the removal of one hyperbolic plane.", "Dimension, determinant, and Hasse equality."),
     stage("At real places also restore one positive and one negative direction, and retain the complex dimension boundary.", "Complete local invariant equality between comparison and input forms.")),
)
add(
    "M0423-L-GLOBAL-UNIQUENESS", "core_lemma", "critical",
    "Two nondegenerate global forms that are isometric at every finite and infinite completion are globally isometric, proved through an explicit Witt-group injectivity and cancellation engine.",
    "planned exact arbitrary-number-field global uniqueness theorem",
    "A global isometry from completion-wise isometries of equal-dimensional forms.",
    "Hasse global classification/uniqueness; source pinpoint open", 92,
    (stage("Merge local data equality, the independently exposed Witt localization injectivity theorem, and Witt cancellation without invoking global classification recursively.", "A global isometry from completion-wise isometries of equal-dimensional forms."),),
)
add(
    "M0423-T-GLOBAL-UNIQUENESS-MERGE", "terminal", "critical",
    "Consume local Witt-class equality, injectivity of localization, and cancellation to obtain a global isometry.",
    "planned exact global-uniqueness recomposition",
    "Global isometry of the two original nondegenerate forms.",
    "future abstract-child composition harness", 28,
    (stage("Map all local isometries to equality of localized Witt classes, use injectivity to get global Witt equivalence, and cancel equal-dimensional hyperbolic summands.", "Global isometry of the two original nondegenerate forms."),),
)
add(
    "M0423-L-LOCAL-DATA-EQUALITY", "core_lemma", "high",
    "A completion-wise isometry gives equality of localized Witt classes, dimension, determinant, Hasse data, and real signatures.",
    "planned exact invariant preservation theorem for every local isometry",
    "Equality of the complete localized data used by global uniqueness.",
    "local isometry invariance and all-place normalization", 38,
    (stage("Apply isometry invariance of each local invariant and the functorial map to the local Witt group.", "Equality at each indexed completion."),
     stage("Reindex through the finite/infinite place normalization without losing real signature data.", "Equality of the complete localized data used by global uniqueness.")),
)
add(
    "M0423-L-WITT-INJECTIVITY", "bridge", "critical",
    "The diagonal localization map from the Witt group of K to the product of the Witt groups of all finite and infinite completions is injective.",
    "planned exact signature: Function.Injective (WittGroup.localizeAll K)",
    "Equality of global Witt classes from equality at every completion.",
    "global Witt exact sequence; no Lean implementation", 96,
    (stage("Merge the generator presentation, local-global square-class detection, reciprocity-kernel exactness, and generator-relation reduction into an injectivity proof.", "Equality of global Witt classes from equality at every completion."),),
)
add(
    "M0423-T-WITT-INJECTIVITY-MERGE", "terminal", "critical",
    "Consume the Witt generators and every arithmetic relation needed to prove that the localization kernel is zero.",
    "planned exact Witt-localization injectivity recomposition",
    "The zero-kernel theorem for the all-place Witt localization map.",
    "future abstract-child composition harness", 30,
    (stage("Reduce a kernel element to diagonal one-dimensional generators, detect square-class relations locally, use reciprocity exactness to lift them globally, and discharge the resulting Witt relations.", "The zero-kernel theorem for the all-place Witt localization map."),),
)
add(
    "M0423-C-WITT-GENERATORS", "construction", "critical",
    "Every Witt class of a nondegenerate form over K is represented by a finite orthogonal sum of one-dimensional nonzero forms, modulo hyperbolic relations.",
    "planned exact diagonal generator presentation of WittGroup K",
    "A finite generator-and-relation representation for every global Witt class.",
    "diagonalization and Witt quotient algebra", 62,
    (stage("Diagonalize a representative form and map each nonzero coefficient to its one-dimensional Witt class.", "A finite sum of one-dimensional generators."),
     stage("Identify basis changes and hyperbolic planes with the defining Witt relations.", "A finite generator-and-relation representation for every global Witt class.")),
)
add(
    "M0423-L-SQUARECLASS-LOCAL-GLOBAL", "bridge", "critical",
    "A nonzero global element that is a square in every finite and infinite completion is already a square in K.",
    "planned exact injectivity theorem K*/K*^2 -> product_v Kv*/Kv*^2",
    "Global equality of square classes from all local equalities.",
    "quadratic extension detected by a nontrivial place; source pinpoint open", 76,
    (stage("Associate a nonsquare with its nontrivial quadratic extension and use existence of a place with nontrivial local Frobenius or nonsplit completion.", "A completion where a nonsquare remains nonsquare."),
     stage("Contradict the all-place square hypothesis and descend equality to the global square-class quotient.", "Global equality of square classes from all local equalities.")),
)
add(
    "M0423-L-QUADRATIC-NONSPLIT-PLACE", "bridge", "critical",
    "Every nontrivial quadratic extension of a number field has a finite or infinite place at which the completed extension is nontrivial.",
    "planned exact nonsplit-place existence theorem for nontrivial quadratic extensions",
    "A completion detecting every nontrivial global quadratic extension.",
    "Chebotarev/Frobenius or norm argument; primary source and Lean implementation open", 100,
    (stage("Choose the nontrivial automorphism of the quadratic extension and apply the Frobenius-density/existence theorem to obtain an unramified prime with that Frobenius class.", "A finite prime that does not split in the extension."),
     stage("Identify nonsplitting with nontriviality of the completed quadratic extension.", "A completion detecting every nontrivial global quadratic extension.")),
)
add(
    "M0423-L-RECIPROCITY-KERNEL-EXACTNESS", "bridge", "critical",
    "The only finite-support local Hilbert-symbol relations invisible at every global square class are those generated by global square classes subject to the single reciprocity product relation.",
    "planned exact quadratic norm-residue localization-sequence exactness theorem",
    "Exactness at the local symbol-family term used by Witt localization.",
    "quadratic reciprocity exact sequence; source and Lean implementation open", 98,
    (stage("Use weak approximation to prescribe independent local square classes at a finite controlling set.", "Surjectivity onto finite local square-class constraints modulo one relation."),
     stage("Use Hilbert reciprocity to identify the unique product obstruction and prove that its kernel comes from a global class.", "Exactness at the local symbol-family term used by Witt localization.")),
)
add(
    "M0423-L-QUADRATIC-DUALITY-EXACTNESS", "bridge", "critical",
    "The global-to-local quadratic norm-residue sequence is exact: finite-support local square-class characters satisfying the reciprocity product constraint arise from global data.",
    "planned exact quadratic Albert-Brauer-Hasse-Noether/Poitou-Tate degree-two exactness theorem",
    "The arithmetic duality engine identifying the kernel and cokernel in the quadratic localization sequence.",
    "global quadratic reciprocity duality; primary source and Lean implementation open", 100,
    (stage("Identify quadratic square classes and local Hilbert pairings with degree-one and degree-two Galois cohomology and local invariant maps.", "The cohomological localization sequence with local pairings."),
     stage("Apply global duality/Albert-Brauer-Hasse-Noether exactness and translate the unique sum-of-local-invariants obstruction back to Hilbert signs.", "The arithmetic duality engine identifying the kernel and cokernel in the quadratic localization sequence.")),
)
add(
    "M0423-L-WITT-REDUCTION", "core_lemma", "critical",
    "If a diagonal Witt class localizes to zero everywhere, the generator presentation and reciprocity exactness reduce it by global hyperbolic relations to zero.",
    "planned exact zero-kernel reduction for diagonal Witt classes",
    "Global triviality of every locally trivial Witt class.",
    "Witt relations plus quadratic reciprocity exactness", 94,
    (stage("Translate local Witt triviality into square-class and Hilbert-symbol relations among the diagonal coefficients.", "A locally trivial finite relation vector."),
     stage("Lift the relation globally through reciprocity-kernel exactness and apply the corresponding binary hyperbolic reductions.", "Global triviality of every locally trivial Witt class.")),
)
add(
    "M0423-L-WITT-CANCELLATION", "bridge", "critical",
    "Equal-dimensional nondegenerate forms with equal Witt classes are isometric.",
    "planned exact Witt cancellation theorem over fields of characteristic not two",
    "An isometry after cancelling equal hyperbolic summands.",
    "Witt cancellation; exact pinned Lean anchor not audited", 68,
    (stage("Choose stable isometries after adjoining hyperbolic planes from equality in the Witt group.", "A stable quadratic-form isometry."),
     stage("Apply Witt cancellation repeatedly and use equal dimensions to eliminate every added hyperbolic summand.", "An isometry after cancelling equal hyperbolic summands.")),
)
add(
    "M0423-T-ISOTROPIC-EXTRACTION", "terminal", "critical",
    "Transport the explicit hyperbolic witness through the global comparison isometry and then through the inverse diagonalizing isometry to the original form.",
    "planned exact witness extraction yielding Stage1.THM_M_0423.IsIsotropic Q",
    "Stage1.THM_M_0423.IsIsotropic Q.",
    "comparison package and diagonal transport", 40,
    (stage("Use the global comparison isometry to move the named nonzero hyperbolic witness into the diagonalized input.", "A nonzero isotropic vector for the diagonalized form."),
     stage("Apply the inverse diagonalization transport, preserving nonzeroness and quadratic value exactly.", "Stage1.THM_M_0423.IsIsotropic Q.")),
)
add(
    "M0423-T-WITNESS-ISOMETRY-TRANSPORT", "transport", "high",
    "An isometry from an explicitly isotropic comparison form to the diagonal input transports the named witness without collapsing it to zero.",
    "planned exact nonzero-isotropic witness transport along QuadraticForm.IsometryEquiv",
    "A nonzero isotropic vector for the diagonalized input.",
    "linear-equivalence injectivity and isometry law", 24,
    (stage("Map the witness through the underlying linear equivalence and use injectivity for nonzeroness.", "A nonzero image vector."),
     stage("Rewrite its quadratic value with the isometry equation.", "A nonzero isotropic vector for the diagonalized input.")),
)
add(
    "M0423-T-DIAGONAL-TRANSPORT-BACK", "transport", "high",
    "Transport a nonzero isotropic vector from the diagonal representative back to Q through the inverse basis isometry.",
    "planned exact inverse of the global isotropy transport in M0423-N-DIAGONALIZE",
    "A nonzero isotropic vector for Q.",
    "diagonalization isometry inverse", 22,
    (stage("Apply the inverse linear equivalence and preserve nonzeroness.", "A nonzero vector in the original module."),
     stage("Use the inverse isometry equation to rewrite the original quadratic value as zero.", "A nonzero isotropic vector for Q.")),
)


# Parent-to-child proof requirements.  Overlay nodes never appear here.
REQUIRES: dict[str, list[str]] = {
    "M0423-ROOT": ["M0423-B-DIRECTIONS"],
    "M0423-B-DIRECTIONS": ["M0423-T-GLOBAL-LOCAL", "M0423-T-LOCAL-GLOBAL"],
    "M0423-T-GLOBAL-LOCAL": ["M0423-C-PURE-TENSOR"],
    "M0423-C-PURE-TENSOR": ["M0423-X-FLAT-INJECTION", "M0423-L-BASECHANGE-EVAL"],
    "M0423-T-LOCAL-GLOBAL": ["M0423-T-ISOTROPIC-EXTRACTION"],
    "M0423-N-DIAGONALIZE": ["M0423-T-DIAGONAL-MERGE"],
    "M0423-T-DIAGONAL-MERGE": ["M0423-C-BASIS-DIAGONAL", "M0423-L-NONDEGENERATE-COEFFICIENTS", "M0423-T-GLOBAL-ISOTROPY-TRANSPORT", "M0423-T-LOCAL-BASECHANGE-TRANSPORT"],
    "M0423-N-PLACE-FAMILY": ["M0423-T-PLACE-MERGE"],
    "M0423-T-PLACE-MERGE": ["M0423-C-FINITE-PLACE-COVERAGE", "M0423-C-INFINITE-PLACE-COVERAGE", "M0423-L-PLACE-EXHAUSTIVENESS"],
    "M0423-B-LOCAL-PLACES": ["M0423-T-LOCAL-PLACES-MERGE"],
    "M0423-T-LOCAL-PLACES-MERGE": ["M0423-L-INFINITE", "M0423-L-FINITE"],
    "M0423-L-INFINITE": ["M0423-T-INFINITE-MERGE"],
    "M0423-T-INFINITE-MERGE": ["M0423-C-INFINITE-DICHOTOMY", "M0423-B-INFINITE-REAL", "M0423-B-INFINITE-COMPLEX"],
    "M0423-B-INFINITE-REAL": ["M0423-N-REAL-COMPLETION-TRANSPORT", "M0423-L-REAL-CLASSIFICATION", "M0423-L-REAL-ISOTROPY"],
    "M0423-L-REAL-ISOTROPY": ["M0423-L-REAL-CLASSIFICATION"],
    "M0423-B-INFINITE-COMPLEX": ["M0423-N-COMPLEX-COMPLETION-TRANSPORT", "M0423-L-COMPLEX-CLASSIFICATION", "M0423-L-COMPLEX-ISOTROPY"],
    "M0423-L-COMPLEX-ISOTROPY": ["M0423-L-COMPLEX-CLASSIFICATION"],
    "M0423-L-FINITE": ["M0423-T-FINITE-MERGE"],
    "M0423-T-FINITE-MERGE": ["M0423-C-HILBERT-SYMBOL", "M0423-C-HASSE-INVARIANT", "M0423-L-FINITE-CLASSIFICATION-EXISTENCE", "M0423-L-FINITE-CLASSIFICATION-UNIQUENESS", "M0423-L-FINITE-WITT-DECOMPOSITION", "M0423-L-FINITE-ISOTROPY-CRITERION"],
    "M0423-L-FINITE-CLASSIFICATION-UNIQUENESS": ["M0423-C-HILBERT-SYMBOL", "M0423-C-HASSE-INVARIANT", "M0423-L-FINITE-REPRESENTATION"],
    "M0423-L-FINITE-REPRESENTATION": ["M0423-C-HILBERT-SYMBOL"],
    "M0423-L-FINITE-ISOTROPY-CRITERION": ["M0423-L-FINITE-CLASSIFICATION-EXISTENCE", "M0423-L-FINITE-CLASSIFICATION-UNIQUENESS", "M0423-L-FINITE-WITT-DECOMPOSITION"],
    "M0423-C-HILBERT-SYMBOL": ["M0423-T-SYMBOL-MERGE"],
    "M0423-T-SYMBOL-MERGE": ["M0423-C-SYMBOL-DEFINITION", "M0423-L-SYMBOL-WELLDEFINED", "M0423-L-SYMBOL-BILINEAR", "M0423-L-SYMBOL-SYMMETRY-NORMALIZATION", "M0423-L-SYMBOL-COMPLETION-COMPATIBILITY"],
    "M0423-L-SYMBOL-BILINEAR": ["M0423-L-NORM-RESIDUE-BILINEARITY"],
    "M0423-C-HASSE-INVARIANT": ["M0423-T-HASSE-MERGE"],
    "M0423-T-HASSE-MERGE": ["M0423-C-HASSE-DIAGONAL", "M0423-L-HASSE-PRESENTATION-MOVES", "M0423-L-DIAGONAL-PRESENTATION-CONNECTIVITY"],
    "M0423-L-DIAGONAL-PRESENTATION-CONNECTIVITY": ["M0423-L-CONGRUENCE-GENERATORS"],
    "M0423-C-HASSE-DIAGONAL": ["M0423-C-HILBERT-SYMBOL"],
    "M0423-L-HASSE-PRESENTATION-MOVES": ["M0423-C-HILBERT-SYMBOL"],
    "M0423-L-GLOBAL-CLASSIFICATION": ["M0423-N-DIAGONALIZE", "M0423-N-PLACE-FAMILY", "M0423-B-LOCAL-PLACES", "M0423-T-GLOBAL-CLASSIFICATION-MERGE"],
    "M0423-T-GLOBAL-CLASSIFICATION-MERGE": ["M0423-C-LOCAL-RESIDUALS", "M0423-C-GLOBAL-INVARIANTS", "M0423-L-HILBERT-RECIPROCITY", "M0423-L-INVARIANT-COMPATIBILITY", "M0423-C-GLOBAL-REALIZATION", "M0423-C-ISOTROPIC-COMPARISON", "M0423-L-GLOBAL-UNIQUENESS"],
    "M0423-C-LOCAL-RESIDUALS": ["M0423-T-RESIDUAL-MERGE"],
    "M0423-T-RESIDUAL-MERGE": ["M0423-L-DIMENSION-AT-LEAST-TWO", "M0423-L-HYPERBOLIC-SPLIT", "M0423-C-RESIDUAL-INVARIANTS"],
    "M0423-C-RESIDUAL-INVARIANTS": ["M0423-C-HILBERT-SYMBOL", "M0423-C-HASSE-INVARIANT"],
    "M0423-C-GLOBAL-INVARIANTS": ["M0423-N-DIAGONALIZE", "M0423-C-HASSE-INVARIANT", "M0423-C-RECIPROCITY-FINITE-SUPPORT"],
    "M0423-L-HILBERT-RECIPROCITY": ["M0423-T-RECIPROCITY-MERGE"],
    "M0423-T-RECIPROCITY-MERGE": ["M0423-C-RECIPROCITY-FINITE-SUPPORT", "M0423-L-RECIPROCITY-LOCAL-BRIDGE", "M0423-L-RECIPROCITY-PRODUCT"],
    "M0423-L-RECIPROCITY-PRODUCT": ["M0423-L-PRINCIPAL-IDELE-RECIPROCITY"],
    "M0423-L-RECIPROCITY-LOCAL-BRIDGE": ["M0423-C-HILBERT-SYMBOL"],
    "M0423-L-INVARIANT-COMPATIBILITY": ["M0423-C-GLOBAL-INVARIANTS", "M0423-L-HILBERT-RECIPROCITY"],
    "M0423-C-GLOBAL-REALIZATION": ["M0423-T-REALIZATION-MERGE"],
    "M0423-T-REALIZATION-MERGE": ["M0423-C-FINITE-SUPPORT-REDUCTION", "M0423-C-APPROXIMATE-COEFFICIENTS", "M0423-C-FINAL-INVARIANT-CORRECTION", "M0423-L-LOCAL-MATCH-VERIFICATION"],
    "M0423-C-FINITE-SUPPORT-REDUCTION": ["M0423-C-LOCAL-RESIDUALS", "M0423-L-HILBERT-RECIPROCITY"],
    "M0423-C-APPROXIMATE-COEFFICIENTS": ["M0423-C-FINITE-SUPPORT-REDUCTION", "M0423-L-WEAK-APPROXIMATION"],
    "M0423-C-FINAL-INVARIANT-CORRECTION": ["M0423-L-INVARIANT-COMPATIBILITY", "M0423-L-HILBERT-RECIPROCITY"],
    "M0423-L-LOCAL-MATCH-VERIFICATION": ["M0423-B-LOCAL-PLACES", "M0423-C-HASSE-INVARIANT"],
    "M0423-C-ISOTROPIC-COMPARISON": ["M0423-T-COMPARISON-MERGE"],
    "M0423-T-COMPARISON-MERGE": ["M0423-C-GLOBAL-REALIZATION", "M0423-C-HYPERBOLIC-PLANE", "M0423-C-EXPLICIT-HYPERBOLIC-WITNESS", "M0423-L-COMPARISON-INVARIANT-MATCH"],
    "M0423-C-EXPLICIT-HYPERBOLIC-WITNESS": ["M0423-C-HYPERBOLIC-PLANE"],
    "M0423-L-COMPARISON-INVARIANT-MATCH": ["M0423-C-LOCAL-RESIDUALS", "M0423-L-LOCAL-MATCH-VERIFICATION", "M0423-C-HYPERBOLIC-PLANE"],
    "M0423-L-GLOBAL-UNIQUENESS": ["M0423-T-GLOBAL-UNIQUENESS-MERGE"],
    "M0423-T-GLOBAL-UNIQUENESS-MERGE": ["M0423-L-LOCAL-DATA-EQUALITY", "M0423-L-WITT-INJECTIVITY", "M0423-L-WITT-CANCELLATION"],
    "M0423-L-LOCAL-DATA-EQUALITY": ["M0423-B-LOCAL-PLACES"],
    "M0423-L-WITT-INJECTIVITY": ["M0423-T-WITT-INJECTIVITY-MERGE"],
    "M0423-T-WITT-INJECTIVITY-MERGE": ["M0423-C-WITT-GENERATORS", "M0423-L-SQUARECLASS-LOCAL-GLOBAL", "M0423-L-RECIPROCITY-KERNEL-EXACTNESS", "M0423-L-WITT-REDUCTION"],
    "M0423-L-SQUARECLASS-LOCAL-GLOBAL": ["M0423-L-QUADRATIC-NONSPLIT-PLACE"],
    "M0423-L-RECIPROCITY-KERNEL-EXACTNESS": ["M0423-L-QUADRATIC-DUALITY-EXACTNESS", "M0423-L-HILBERT-RECIPROCITY", "M0423-L-WEAK-APPROXIMATION", "M0423-C-HILBERT-SYMBOL"],
    "M0423-L-WITT-REDUCTION": ["M0423-C-WITT-GENERATORS", "M0423-L-RECIPROCITY-KERNEL-EXACTNESS"],
    "M0423-T-ISOTROPIC-EXTRACTION": ["M0423-T-WITNESS-ISOMETRY-TRANSPORT", "M0423-T-DIAGONAL-TRANSPORT-BACK"],
    "M0423-T-WITNESS-ISOMETRY-TRANSPORT": ["M0423-L-GLOBAL-CLASSIFICATION", "M0423-C-EXPLICIT-HYPERBOLIC-WITNESS"],
    "M0423-T-DIAGONAL-TRANSPORT-BACK": ["M0423-N-DIAGONALIZE"],
}


def edge(
    edge_id: str,
    source: str,
    edge_type: str,
    target: str,
    reciprocal: str | None = None,
) -> dict:
    result = {"edge_id": edge_id, "from": source, "type": edge_type, "to": target}
    if reciprocal is not None:
        result["reciprocal_edge_id"] = reciprocal
    return result


def indexed(edges: list[dict]) -> dict:
    outgoing: dict[str, list[str]] = {}
    incoming: dict[str, list[str]] = {}
    for item in edges:
        outgoing.setdefault(item["from"], []).append(item["edge_id"])
        incoming.setdefault(item["to"], []).append(item["edge_id"])
    return {"edges": edges, "out": outgoing, "in": incoming}


def registry_projection(rows: list[dict]) -> list[dict]:
    fields = (
        "obligation_id", "statement_fingerprint", "kind", "root_relevant",
        "machine_eligibility", "human_source_eligibility", "readable_eligibility",
        "risk_class", "exclusion_reason", "terminal_proof_body_id",
    )
    return [{name: row[name] for name in fields} for row in rows]


def make_ledger(row: dict, parents: dict[str, list[str]]) -> list[dict]:
    oid = row["id"]
    children = REQUIRES.get(oid, [])
    result = []
    for index, (inference, output) in enumerate(row["stages"], 1):
        if index == 1:
            premises = children or ["frozen-formal-context"]
        else:
            premises = [f"{oid}-STEP-{index - 1:02d}"]
        final = index == len(row["stages"])
        outgoing = (
            [f"{oid}-STEP-{index + 1:02d}"]
            if not final else (parents.get(oid, []) or ["terminal-root-output"])
        )
        result.append({
            "step_id": f"{oid}-STEP-{index:02d}",
            "premise_ids": premises,
            "inference": inference,
            "source_locator": row["locator"],
            "output": output,
            "outgoing_use": outgoing,
        })
    assert result and result[-1]["output"] == row["output"], oid
    assert set(children) <= {premise for item in result for premise in item["premise_ids"]}, oid
    return result


def render_markdown(registry: dict, bundle: dict) -> str:
    count = len(registry["obligations"])
    edges = sum(len(graph["edges"]) for graph in bundle["graphs"].values())
    ledgers = sum(len(node["semantic_step_ledger"]) for node in bundle["nodes"])
    leaves = bundle["closure_boundary"]["executable_open_leaf_cut_set"]
    lines = [
        "# THM-M-0423 frozen obligation architecture", "",
        f"Item: `{ITEM}`.", "",
        f"Registry version 2 freezes {count} canonical obligations at denominator",
        f"`{registry['denominator_sha256']}`. The bundle contains {edges} typed edges and",
        f"{ledgers} substantive ledger steps. All accepted closure sets are empty.", "",
        "This is a source-informed implementation architecture, not a completed historical proof",
        "reconstruction. Hasse 1924 is still only an H1 anchor: pinpoint node/page mapping, errata",
        "review, and independent source review remain open. Planned signatures below are canonical",
        "targets for later implementation, not declarations asserted to exist.", "",
        "## Proof route", "", "```text",
        "ROOT -> directional split",
        "  global-to-local -> nonzero pure tensor + base-change evaluation",
        "  local-to-global -> diagonal and place normalization",
        "    local classification -> real/complex + nonarchimedean invariant packages",
        "    local hyperbolic residuals -> compatible global residual realization",
        "    comparison H + residual -> global Witt uniqueness/cancellation",
        "    explicit hyperbolic witness -> isometry transport -> original form",
        "```", "",
        "The proof graph contains no checked composition certificate. Every reverse proof edge is",
        "`logical_decomposition`; the Lean declarations in `ObligationTree.lean` are conditional",
        "or candidate harnesses only. In particular, `direction_package` consumes the open hard",
        "direction and is not an inhabitant of that package without a premise.", "",
        "## Node ledger", "",
    ]
    nodes = {node["obligation_id"]: node for node in bundle["nodes"]}
    for row in registry["obligations"]:
        node = nodes[row["obligation_id"]]
        lines.extend([
            f"### {row['obligation_id'].lower()}", "",
            node["human_statement"], "",
            f"Formal target: `{node['formal_target']}`.", "",
            f"Output: {node['output']}", "",
            f"Projected status: `[{node['human_debt']}, {node['machine_debt']}, {node['readability_debt']}]`; candidate classification: `{node['candidate_machine_classification']}`.", "",
            f"Source boundary: {node['semantic_step_ledger'][0]['source_locator']}.", "",
            f"Budget: {node['step_budget']} substantive steps maximum; ledger: {len(node['semantic_step_ledger'])} step(s).", "",
            f"Boundary: {node['status_boundary']}", "",
        ])
    lines.extend([
        "## Cut reporting", "",
        "The singleton `M0423-T-LOCAL-GLOBAL` is only the immediate mathematical cut if the",
        "top conditional harnesses and every planned internal composition are assumed valid. It is",
        "not the unqualified executable or release cut.", "",
        f"The executable open-leaf cut contains {len(leaves)} leaves, all listed in",
        "`typed-graphs.json`. Every proof parent also lacks a machine-derived composition",
        "certificate. Foundation, source, provenance, trust, readability, workflow, downstream",
        "proof/validation/release receipts, and master acceptance are separate release cuts.", "",
        "## Freeze boundary", "",
        "Registry v2 supersedes the unaccepted v1 draft and preserves its denominator in the",
        "append-only delta. V2 removes the speculative low/high-dimension shortcut, makes every",
        "finite/infinite merge consume its branches, proves Hasse-invariant independence through",
        "presentation moves rather than local classification, exposes reciprocity inputs, and",
        "separates global realization, comparison, Witt injectivity, cancellation, uniqueness, and",
        "witness extraction.", "",
        "The root remains `[H1, M3, R3]`. There is no E0/E1 evidence, accepted M0 node, checked",
        "composition certificate, H0/R0 review, audit completion, theorem completion, release",
        "receipt, or master acceptance.", "",
    ])
    return "\n".join(lines)


def render_intake(denominator: str) -> dict:
    statement = json.loads((HERE / "statement.json").read_text())
    environment = statement["environment"]
    return {
        "schema_version": "stage1-instance/5.6.0",
        "item_id": "S56-M-0423-INTAKE",
        "lifecycle_mode": "planned",
        "theorem_id": THEOREM,
        "canonical_name": "Hasse-Minkowski theorem for quadratic forms over number fields",
        "canonical_statement": "Let K be a number field, V a finite-dimensional K-vector space, and Q a nondegenerate quadratic form on V. Then Q has a nonzero isotropic vector over K if and only if its scalar extension has a nonzero isotropic vector at every finite and infinite completion of K.",
        "canonical_formal_target": {
            "backend": "lean4",
            "module": "Stage1_Instances/THM-M-0423/Statement.lean",
            "declaration_or_expression": "Stage1.THM_M_0423.HasseMinkowskiStatement",
            "elaborated_expression_hash": "sha256:" + ROOT_EXPRESSION,
            "environment_fingerprint": f"lean-4.29.0-{environment['lean'].split('/')[-1]}_mathlib-{environment['mathlib']}_imports-sha256:{sha256(HERE / 'Statement.lean')}",
            "gate_state": "provisional_self_tested_pending_master_acceptance",
        },
        "domain_and_universes": statement["domain_and_universes"],
        "quantifiers": [
            "for every K : Type u with Field K and NumberField K",
            "for every V : Type v with AddCommGroup V, Module K V, and FiniteDimensional K V",
            "for every Q : QuadraticForm K V",
            "for every NumberField.FinitePlace K and NumberField.InfinitePlace K in the local predicates",
        ],
        "hypotheses": ["Q.Nondegenerate"],
        "conclusion": statement["conclusion"],
        "alternate_encodings": [
            {"target": "homogeneous quadratic polynomial after choosing a basis", "relationship": "iff", "checked_witness": None, "credit": "none; bidirectional coordinate and completion transports remain open"},
            {"target": "diagonal dimension/determinant/local-Hasse-invariant classification", "relationship": "implies", "checked_witness": None, "credit": "none; selected proof architecture only"},
        ],
        "excluded_degenerate_cases": "The zero vector never witnesses isotropy. Degenerate forms, finite-place-only tests, Q-only specializations, integral variants, and unrestricted Hasse principles are excluded.",
        "foundation_profile": "Lean 4 classical candidate profile {propext, Classical.choice, Quot.sound}; acceptance and transitive closure remain open",
        "tcb_profile": f"Lean 4.29.0 kernel plus pinned mathlib {MATHLIB_REVISION}; compiled-artifact, executable, and transitive trust closure remain open",
        "computation_profile": "No solver, native evaluator, external computation, certificate, oracle, or experiment supplies proof credit",
        "formal_system": "Lean 4 + pinned mathlib",
        "source_revisions": {"lean": environment["lean"], "mathlib": environment["mathlib"], "statement_sha256": sha256(HERE / "Statement.lean"), "anchor_audit_sha256": sha256(HERE / "anchor-audit.json")},
        "obligation_registry_hash": "sha256:" + denominator,
        "obligation_registry_id": "THM-M-0423-OBLIGATIONS-v2",
        "discovery_protocol_hash": None,
        "authoritative_blueprint": "Docs/Stage1_Blueprint_rev-5.6.md",
        "public_merge_targets": ["Stage1_Instances/THM-M-0423/README.md", "Stage1_Instances/THM-M-0423/source_statement_crosswalk.md", "Stage1_Instances/THM-M-0423/obligation-tree.md"],
        "owners_and_reviewers": {"owner": "THM-M-0423 execution lane", "reviewer": "independent Stage1 integration lane"},
        "freshness_and_revocation_policy": "Invalidate on any canonical expression, import, toolchain, dependency, registry, source, foundation/TCB, checker, or workflow-state change.",
        "root_vector": {"human": "H1", "machine": "M3", "readability": "R3"},
        "audit_complete": False,
        "theorem_complete": False,
        "status_boundary": "The exact Lean statement and v2 obligation architecture are provisionally self-tested, but all accepted proof closures, source H0, readable R0, release gates, and master acceptance remain open.",
    }


def render_readme(count: int, denominator: str) -> str:
    return f"""# THM-M-0423 rev-5.6 dossier

This planned instance freezes the classical Hasse-Minkowski theorem for nondegenerate quadratic
forms over arbitrary number fields. The exact Lean target is
`Stage1.THM_M_0423.HasseMinkowskiStatement`; it quantifies both finite and infinite completions and
uses a nonzero isotropic witness. The historical label "Hasse principle" is not broadened to
general varieties or restricted to the rational field.

## Current surfaces

| Surface | Current boundary |
|---|---|
| Exact statement | Elaborated expression SHA-256 `{ROOT_EXPRESSION}`; statement evidence is provisional pending master acceptance |
| Anchor audit | Pinned mathlib supplies support only; both external candidates are Q-only and placeholder-contaminated |
| Obligation architecture | Registry v2 contains {count} canonical obligations at `{denominator}` |
| Lean work | Scalar-extension witness preservation and global-to-local elaborate; no accepted E0/E1 packet exists |
| Hard direction | Classification, reciprocity, realization, global Witt uniqueness, cancellation, and extraction are explicit open obligations |
| Source/readability | Hasse 1924 is H1 only; pinpoint node mapping, errata review, readable R0, and independent reviews remain open |

The typed proof graph is separate from source, provenance, evidence, trust, documentation, and
workflow overlays. All reverse proof edges are unverified `logical_decomposition` edges. The Lean
directional combinators are conditional harnesses and do not inhabit the open local-to-global
premise.

## Verdict

Lifecycle remains `planned`; root vector is `[H1, M3, R3]`. Accepted closure is empty,
`audit_complete=false`, and `theorem_complete=false`. Dependency-ordered master acceptance of the
prior phases and this worker proposal remains required.
"""


def render_crosswalk() -> str:
    return """# Source-statement crosswalk

| Claim component | Human source boundary | Exact Lean surface | Current classification |
|---|---|---|---|
| Arbitrary-number-field local-global isotropy | H. Hasse, *Darstellbarkeit von Zahlen durch quadratische Formen in einem beliebigen algebraischen Zahlkorper*, Crelle 153 (1924), pp. 113-130 | `Stage1.THM_M_0423.HasseMinkowskiStatement` | H1: paper identified; theorem/page premise map, edition hash, errata audit, and independent review open |
| Nonzero witness and nondegeneracy | Same source statement must be checked against modern conventions | `IsIsotropic`; `Q.Nondegenerate` | Exact Lean boundary elaborated; human-source convention mapping open |
| Every finite and infinite completion | Hasse's place-by-place theorem; exact sections still to be mapped | `IsIsotropicAtEveryFinitePlace` and `IsIsotropicAtEveryInfinitePlace` | Exact Lean carriers elaborated; source-place normalization open |
| Global-to-local direction | Functorial scalar extension | `ObligationTree.global_to_local` | Local candidate body elaborates; M0-L would require accepted E0 and is not projected |
| Local-to-global direction | Hasse 1924 hard theorem | `ObligationTree.LocalToGlobalObligation` | H1/M4 hard route; no body or accepted proof evidence |
| Diagonal/invariant route | Candidate reconstruction using local classification, Hilbert reciprocity, realization, and global uniqueness | Planned v2 proof nodes | Source-informed architecture only; no claim this is yet a complete page-faithful reconstruction |
| Polynomial/coordinate form | Basis-dependent alternate statement | `M0423-S-COORDINATES` | No credit until bidirectional global/local transports elaborate |

The rational-field specialization associated with Minkowski is historical context, not a substitute
for this target. The two audited external Lean candidates prove only Q-shaped statements and contain
placeholders at their pinned revisions; they are rejected M5 audit records and never proof premises.

No node is H0. Source review must map every material v2 proof obligation to versioned primary-source
locators, assumptions, dependencies, corrections, and an independent reviewer before H0 can be
considered.
"""


def render_validation(registry: dict, bundle: dict) -> str:
    count = len(registry["obligations"])
    edges = sum(len(graph["edges"]) for graph in bundle["graphs"].values())
    ledgers = sum(len(node["semantic_step_ledger"]) for node in bundle["nodes"])
    plans = len(bundle["unverified_decomposition_plans"])
    leaves = len(bundle["closure_boundary"]["executable_open_leaf_cut_set"])
    return f"""# THM-M-0423 obligation-tree validation

Item: `{ITEM}`

Base revision: `{BASE_REVISION}`

Base tree: `{BASE_TREE}`

Validation date: 2026-07-15 (`Asia/Shanghai`)

## Result

Registry v2 freezes {count} obligations at denominator SHA-256
`{registry['denominator_sha256']}`. The typed bundle has {edges} edges, {ledgers} substantive ledger
steps, {plans} unverified parent decomposition plans, zero checked composition certificates, and
{leaves} executable open proof leaves. V2 preserves the unaccepted v1 denominator in an append-only
delta and accepts no proof closure.

The checker validates exact target membership and DAG ownership, deterministic generated bytes,
registry eligibility and denominator fields, ledger premise/step/output references, proof
reachability and acyclicity, reciprocal edges, merge consumption, semantic anti-cycle assertions,
overlay separation, workflow projection, document reconciliation, receipt hashes, and worker packet
ownership. In-memory negative fixtures exercise corrupted denominators, reciprocity, ledgers,
unsupported M0, planned-fingerprint certificates, cycles, false closure, stale documents, and a
missing worker packet.

The isolated Lean check uses `lake env lean --trust=0 -t0` on temporary copies. It elaborates the
exact statement, scalar-extension witness preservation, the full global-to-local direction, and
the conditional recomposition harnesses. Five local declarations report exactly `propext`,
`Classical.choice`, and `Quot.sound`; none reports `sorryAx`. These are candidate interfaces only:
no E0/E1 packet or accepted M0 projection is created.

## Commands

The final worker packet records exact argv arrays and exit codes for:

1. `python3 Docs/tools/check_stage1_standard.py`
2. `python3 scripts/stage1_target.py check`
3. `python3 scripts/stage1_target.py show THM-M-0423`
4. `python3 -B Stage1_Instances/THM-M-0423/build_obligation_artifacts.py --check`
5. JSON parsing of every structured owned artifact
6. Python compilation with `PYTHONPYCACHEPREFIX` outside the repository
7. a scoped prohibited-token scan of `ObligationTree.lean`
8. scoped `git diff --check`
9. `python3 -B Stage1_Instances/THM-M-0423/check_obligation_tree.py --worker-packet .stage1-worker-selftest.json`

The final checker recomputes every receipt artifact/source hash, executes the narrow Lean commands,
and verifies the pinned mathlib revision/tree and clean dependency state before and after
elaboration. The automation-provided `.lake` symlink is
read only. No update, build, dependency clone/fetch, or network operation is part of this evidence.

## Boundary

`M0423-T-LOCAL-GLOBAL` is only the immediate mathematical cut under assumed-valid top harnesses.
Every proof parent still lacks a machine-derived composition certificate; {leaves} executable proof
leaves remain open; and foundation, source, provenance, trust, readability, workflow, proof,
validation, release, independent verification, and master-acceptance cuts remain. The root stays
`[H1, M3, R3]`, `audit_complete=false`, and `theorem_complete=false`.
"""


def build() -> dict[str, object]:
    ids = [row["id"] for row in SPECS]
    assert len(ids) == len(set(ids))
    spec_by_id = {row["id"]: row for row in SPECS}
    assert set(REQUIRES) <= set(ids)
    assert {child for children in REQUIRES.values() for child in children} <= set(ids)
    parents: dict[str, list[str]] = {}
    for parent, children in REQUIRES.items():
        for child in children:
            parents.setdefault(child, []).append(parent)

    obligations = []
    for row in SPECS:
        oid = row["id"]
        fingerprint = (
            "lean-expression-sha256:" + ROOT_EXPRESSION
            if oid in {"M0423-ROOT", "M0423-S-INTERFACE"}
            else "planned:v2:sha256:" + digest({
                "obligation_id": oid,
                "formal_target": row["formal"],
                "output": row["output"],
                "human_statement": row["claim"],
            })
        )
        excluded = any(row[key] != "required" for key in ("machine", "human", "readable"))
        obligations.append({
            "obligation_id": oid,
            "statement_fingerprint": fingerprint,
            "kind": row["kind"],
            "root_relevant": True,
            "machine_eligibility": row["machine"],
            "human_source_eligibility": row["human"],
            "readable_eligibility": row["readable"],
            "risk_class": row["risk"],
            "exclusion_reason": ({
                "code": "NON_PROOF_ASSURANCE_OVERLAY",
                "justification": "This node records statement, source, provenance, trust, readability, workflow, or rejected-candidate assurance and is not an independent mathematical proof premise.",
                "independent_approval": "pending Stage1 integration-lane review",
            } if excluded else None),
            "terminal_proof_body_id": row["body"],
        })
    denominator = digest(registry_projection(obligations))
    proof_ids = [row["id"] for row in SPECS if row["machine"] == "required"]
    overlay_ids = [row["id"] for row in SPECS if row["machine"] != "required"]
    proof_leaves = sorted(set(proof_ids) - set(REQUIRES))
    changed_existing = [row["obligation_id"] for row in obligations if row["obligation_id"] in {
        "M0423-ROOT", "M0423-S-INTERFACE", "M0423-S-BOUNDARY", "M0423-S-COORDINATES", "M0423-S-FOUNDATION",
        "M0423-B-DIRECTIONS", "M0423-T-GLOBAL-LOCAL", "M0423-C-PURE-TENSOR", "M0423-X-FLAT-INJECTION",
        "M0423-L-BASECHANGE-EVAL", "M0423-T-LOCAL-GLOBAL", "M0423-N-DIAGONALIZE", "M0423-N-PLACE-FAMILY",
        "M0423-B-LOCAL-PLACES", "M0423-L-INFINITE", "M0423-L-FINITE", "M0423-C-HILBERT-SYMBOL",
        "M0423-C-HASSE-INVARIANT", "M0423-L-HILBERT-RECIPROCITY", "M0423-L-GLOBAL-CLASSIFICATION",
        "M0423-C-GLOBAL-INVARIANTS", "M0423-L-WEAK-APPROXIMATION", "M0423-L-INVARIANT-COMPATIBILITY",
        "M0423-C-GLOBAL-REALIZATION", "M0423-T-ISOTROPIC-EXTRACTION", "M0423-C-ISOTROPIC-COMPARISON",
        "M0423-B-INFINITE-REAL", "M0423-B-INFINITE-COMPLEX", "M0423-T-INFINITE-MERGE", "M0423-X-MATHLIB",
        "M0423-X-EXTERNAL", "M0423-X-SOURCE", "M0423-X-PROVENANCE", "M0423-X-TRUST", "M0423-X-READABLE", "M0423-X-WORKFLOW",
    }]
    v1_ids = set(changed_existing) | {"M0423-B-DIMENSION", "M0423-B-DIM-LOW", "M0423-B-DIM-HIGH", "M0423-T-DIMENSION-MERGE"}
    registry = {
        "schema_version": "stage1-obligation-registry/1.0",
        "registry_id": "THM-M-0423-OBLIGATIONS-v2",
        "item_id": ITEM,
        "theorem_id": THEOREM,
        "registry_version": 2,
        "frozen_at": "2026-07-15T00:00:00+08:00",
        "freeze_basis": "Closure-blind v2 freeze over the exact statement and bounded anchor inventory. The selected classification/comparison route is source-informed but retains H1 until node-level primary-source review.",
        "closure_status_excluded_from_freeze_decisions": True,
        "frozen_against_statement_sha256": sha256(HERE / "Statement.lean"),
        "frozen_against_statement_record_sha256": sha256(HERE / "statement.json"),
        "frozen_against_anchor_audit_sha256": sha256(HERE / "anchor-audit.json"),
        "canonical_expression_sha256": ROOT_EXPRESSION,
        "root_obligation_id": "M0423-ROOT",
        "denominator_sha256": denominator,
        "frozen_denominators": {
            "inventory": ids,
            "required_machine": proof_ids,
            "required_human_source": [row["obligation_id"] for row in obligations if row["human_source_eligibility"] == "required"],
            "required_readable": [row["obligation_id"] for row in obligations if row["readable_eligibility"] == "required"],
            "informational_overlays": overlay_ids,
        },
        "layer_analysis": {
            "statement_foundation": {"status": "represented", "obligation_ids": [oid for oid in ids if "-S-" in oid]},
            "normalization": {"status": "represented", "obligation_ids": [oid for oid in ids if "-N-" in oid]},
            "branch": {"status": "represented", "obligation_ids": [oid for oid in ids if "-B-" in oid]},
            "construction": {"status": "represented", "obligation_ids": [oid for oid in ids if "-C-" in oid]},
            "core_lemma": {"status": "represented", "obligation_ids": [oid for oid in ids if "-L-" in oid]},
            "external_trust": {"status": "represented", "obligation_ids": [oid for oid in ids if "-X-" in oid]},
            "terminal": {"status": "represented", "obligation_ids": [oid for oid in ids if "-T-" in oid] + ["M0423-ROOT"]},
            "computation": {"status": "not_applicable_pending_independent_approval", "reason": "The selected route uses no finite computation, reflection, solver, numerical experiment, or certificate as a proof premise."},
        },
        "alias_and_body_deduplication": {
            "coordinate_polynomial_form": "unchecked transport overlay; no separate proof closure credit",
            "finite_and_infinite_predicate_conjunction": "one canonical local-family requirement",
            "external_Q_specializations": "scope-mismatched M5 audit evidence only",
            "global_realization_vs_comparison": "realization constructs the single residual R; comparison constructs H orthogonalSum R and never realizes R again",
        },
        "append_only_delta": [{
            "from_registry_id": "THM-M-0423-OBLIGATIONS-v1",
            "from_denominator_sha256": V1_DENOMINATOR,
            "from_inventory_count": 40,
            "to_registry_id": "THM-M-0423-OBLIGATIONS-v2",
            "to_denominator_sha256": denominator,
            "to_inventory_count": len(ids),
            "added_obligation_ids": sorted(set(ids) - v1_ids),
            "removed_obligation_ids": ["M0423-B-DIMENSION", "M0423-B-DIM-LOW", "M0423-B-DIM-HIGH", "M0423-T-DIMENSION-MERGE"],
            "changed_existing_obligation_ids": changed_existing,
            "reason": "Supersede the unaccepted v1 draft: expand hidden critical leaves, remove the unaudited low/high-dimension shortcut, repair all merge dependencies and semantic cycles, separate realization/comparison/uniqueness, downgrade unsupported M0 projections, and re-fingerprint every changed planned signature.",
            "status_effect": "No obligation closes; accepted closure remains empty and root H1/M3/R3 is unchanged.",
        }],
        "status_observed_after_freeze": {
            "accepted_closed_obligations": [],
            "accepted_root_machine_debt": "M3",
            "root_human_debt": "H1",
            "root_readability_debt": "R3",
            "candidate_local_bodies": {
                "M0423-T-GLOBAL-LOCAL": "M0-L_requires_E0",
                "M0423-C-PURE-TENSOR": "M0-L_requires_E0",
                "M0423-X-FLAT-INJECTION": "M0-W_requires_E1",
                "M0423-L-BASECHANGE-EVAL": "M0-W_requires_E1",
            },
            "conditional_harness_boundary": "direction_package and root_from_direction_package consume abstract open premises; they are M3 harnesses, not closed package/root bodies",
        },
        "intake_reconciliation": {
            "path": "Stage1_Instances/THM-M-0423/intake.json",
            "formal_target_expression_sha256": ROOT_EXPRESSION,
            "registry_denominator_sha256": denominator,
            "status": "reconciled projection; prior task acceptance remains integration-lane authority",
        },
        "classification_metrics": {
            "inventory_obligation_ids": ids,
            "required_machine_obligation_ids": proof_ids,
            "executable_proof_leaf_ids": proof_leaves,
            "interface_and_transport_ids": [row["id"] for row in SPECS if row["kind"] in {"definition", "normalization", "transport"}],
            "critical_risk_ids": [row["id"] for row in SPECS if row["risk"] == "critical"],
            "high_risk_ids": [row["id"] for row in SPECS if row["risk"] == "high"],
            "source_boundary_ids": ["M0423-X-SOURCE"],
            "accepted_machine_numerator_ids": [],
            "accepted_h0_numerator_ids": [],
            "accepted_r0_numerator_ids": [],
            "accepted_root_or_critical_path_ids": [],
            "known_distinct_terminal_proof_body_ids": sorted({row["body"] for row in SPECS if row["body"]}),
            "alias_policy": "Wrappers, transports, rejected specializations, and conditional harnesses do not create duplicate proof-body credit.",
            "numerator_denominator_sets": {
                "inventory_classification": {"numerator": ids, "denominator": ids},
                "unique_logical_leaf_closure": {"numerator": [], "denominator": proof_leaves},
                "distinct_proof_body_closure": {"numerator": [], "denominator": sorted({row["body"] for row in SPECS if row["body"]})},
                "interface_transport_closure": {"numerator": [], "denominator": [row["id"] for row in SPECS if row["machine"] == "required" and row["kind"] in {"definition", "normalization", "transport"}]},
                "readable_closure": {"numerator": [], "denominator": [row["obligation_id"] for row in obligations if row["readable_eligibility"] == "required"]},
                "human_source_closure": {"numerator": [], "denominator": [row["obligation_id"] for row in obligations if row["human_source_eligibility"] == "required"]},
                "source_boundary_coverage": {"numerator": [], "denominator": proof_ids},
                "root_closure": {"numerator": [], "denominator": ["M0423-ROOT"]},
            },
            "disputed_eligibility_bounds": {"pessimistic_closed_ids": [], "optimistic_closed_ids": [], "reason": "No accepted proof evidence exists, so disputed eligibility cannot change the zero closure numerator."},
        },
        "obligations": obligations,
        "audit_complete": False,
        "theorem_complete": False,
    }

    nodes = []
    obligation_by_id = {row["obligation_id"]: row for row in obligations}
    for row in SPECS:
        oid = row["id"]
        machine_debt = "M3" if row["candidate"].startswith("M3") or row["candidate"].startswith("M0-") else "M4"
        if row["candidate"].startswith("M5"):
            machine_debt = "M5"
        proof_leaf = row["machine"] == "required" and oid not in REQUIRES
        nodes.append({
            "node_id": THEOREM + "-" + oid.removeprefix(PREFIX),
            "obligation_id": oid,
            "kind": row["kind"],
            "human_statement": row["claim"],
            "formal_target": row["formal"],
            "output": row["output"],
            "human_debt": "H1" if row["human"] == "required" else "H2",
            "machine_debt": machine_debt,
            "readability_debt": "R3",
            "candidate_machine_classification": row["candidate"],
            "evidence_ids": [],
            "source_crosswalk_id": "SRC-M0423-HASSE1924-PARTIAL" if row["human"] == "required" else "not-applicable",
            "provenance_id": "none; candidate provenance is not accepted evidence",
            "foundation_profile": "Lean4-mathlib classical candidate {propext, Classical.choice, Quot.sound}; acceptance open",
            "tcb_profile": f"Lean-4.29.0+mathlib-{MATHLIB_REVISION}; transitive and release closure open",
            "computation_record": "none; no solver, native evaluation, external computation, certificate, or oracle closes this node",
            "step_budget": row["budget"],
            "semantic_step_ledger": make_ledger(row, parents),
            "public_readable_target": f"Stage1_Instances/THM-M-0423/obligation-tree.md#{oid.lower()}",
            "validation_spec_id": "VAL-M0423-OBLIGATION-BUNDLE",
            "status_boundary": "Architecture, exact statement interface, or unaccepted candidate body only; no accepted E0/E1, M0, H0, R0, composition, audit completion, theorem completion, or master acceptance.",
            "task_ids": [ITEM] + (["S56-M-0423-PROOF", "S56-M-0423-VALIDATION"] if row["machine"] == "required" else ["S56-M-0423-VALIDATION"]),
            "owned_sources": [
                f"Stage1_Instances/THM-M-0423/obligation-tree.md#{oid.lower()}"
            ] + ([
                "Stage1_Instances/THM-M-0423/ObligationTree.lean#" + row["body"].rsplit("#", 1)[1]
            ] if row["body"] and row["body"].startswith("local:") else []),
            "owner": "THM-M-0423 execution lane",
            "reviewer": "independent Stage1 integration lane",
            "validity": {"validated_at": "2026-07-15", "review_due": "before proof-phase acceptance", "invalidation_inputs": ["statement hash", "anchor hash", "registry denominator", "typed proof edges", "source mapping", "toolchain and mathlib pin", "foundation and TCB profile"], "revocation_state": "not-accepted"},
            "leaf_stop_record": ({
                "is_proof_leaf": True,
                "canonical_signature_status": "exact named declaration" if not row["formal"].startswith("planned") else "planned canonical signature; elaboration remains a proof-phase task",
                "hidden_branch_or_package": False,
                "expansion_audit_status": "provisionally_split_to_one_canonical_engine; independent architecture review required before proof acceptance",
                "explicit_blocker": "No accepted exact proof body and E0/E1 receipt exists for this leaf at the frozen environment.",
                "retry_event": "Independently review the leaf for further hidden branches; then implement or locate the exact signature, elaborate it without placeholders, bind provenance/trust, and produce the required accepted evidence tier.",
            } if proof_leaf else {"is_proof_leaf": False, "reason": "expanded by proof_requires children or non-proof assurance overlay"}),
        })

    proof_edges = []
    plans = []
    for parent, children in REQUIRES.items():
        for child in children:
            forward = f"REQ-{parent}-{child}"
            reverse = f"DECOMP-{child}-{parent}"
            proof_edges.extend([
                edge(forward, parent, "proof_requires", child, reverse),
                edge(reverse, child, "logical_decomposition", parent, forward),
            ])
        plans.append({
            "plan_id": "PLAN-" + parent,
            "parent_obligation_id": parent,
            "planned_child_ids": children,
            "parent_statement_fingerprint": obligation_by_id[parent]["statement_fingerprint"],
            "child_statement_fingerprints": {child: obligation_by_id[child]["statement_fingerprint"] for child in children},
            "status": "unverified_child_to_parent_composition",
            "required_future_certificate": "Machine-derived exact endpoint fingerprints and an abstract-child harness that consumes every child and yields the complete parent without undeclared premises.",
        })
    workflow_tasks = ["S56-M-0423-ANCHOR_AUDIT", ITEM, "S56-M-0423-PROOF", "S56-M-0423-VALIDATION", "S56-M-0423-RELEASE"]
    graph_edges = {
        "proof": proof_edges,
        "refinement": [
            edge("REF-ROOT-INTERFACE", "M0423-ROOT", "expository_decomposition", "M0423-S-INTERFACE", "REF-INTERFACE-DOCS-ROOT"),
            edge("REF-INTERFACE-DOCS-ROOT", "M0423-S-INTERFACE", "documents", "M0423-ROOT", "REF-ROOT-INTERFACE"),
            edge("REF-ROOT-BOUNDARY", "M0423-ROOT", "expository_decomposition", "M0423-S-BOUNDARY", "REF-BOUNDARY-DOCS-ROOT"),
            edge("REF-BOUNDARY-DOCS-ROOT", "M0423-S-BOUNDARY", "documents", "M0423-ROOT", "REF-ROOT-BOUNDARY"),
            edge("REF-ROOT-COORDINATES", "M0423-ROOT", "expository_decomposition", "M0423-S-COORDINATES", "REF-COORDINATES-DOCS-ROOT"),
            edge("REF-COORDINATES-DOCS-ROOT", "M0423-S-COORDINATES", "documents", "M0423-ROOT", "REF-ROOT-COORDINATES"),
        ],
        "provenance": [],
        "evidence": [],
        "trust": [
            edge("TRUST-ROOT-FOUNDATION", "M0423-ROOT", "trusts", "M0423-S-FOUNDATION", "TRUST-FOUNDATION-ROOT"),
            edge("TRUST-FOUNDATION-ROOT", "M0423-S-FOUNDATION", "trusted_by", "M0423-ROOT", "TRUST-ROOT-FOUNDATION"),
            edge("TRUST-ROOT-RELEASE", "M0423-ROOT", "trusts", "M0423-X-TRUST", "TRUST-RELEASE-ROOT"),
            edge("TRUST-RELEASE-ROOT", "M0423-X-TRUST", "trusted_by", "M0423-ROOT", "TRUST-ROOT-RELEASE"),
        ],
        "documentation": [],
        "workflow": [
            edge("FLOW-TREE-ANCHOR", ITEM, "workflow_depends_on", "S56-M-0423-ANCHOR_AUDIT"),
            edge("FLOW-PROOF-TREE", "S56-M-0423-PROOF", "workflow_depends_on", ITEM),
            edge("FLOW-VALIDATION-PROOF", "S56-M-0423-VALIDATION", "workflow_depends_on", "S56-M-0423-PROOF"),
            edge("FLOW-RELEASE-VALIDATION", "S56-M-0423-RELEASE", "workflow_depends_on", "S56-M-0423-VALIDATION"),
        ],
    }
    for obligation in obligations:
        oid = obligation["obligation_id"]
        if obligation["human_source_eligibility"] == "required" and oid != "M0423-X-SOURCE":
            graph_edges["provenance"].append(edge("SOURCE-MAP-" + oid, oid, "source_map", "M0423-X-SOURCE"))
        if obligation["machine_eligibility"] == "required":
            graph_edges["provenance"].append(edge("PROVENANCE-" + oid, "M0423-X-PROVENANCE", "provenance_of", oid))
        if obligation["readable_eligibility"] == "required" and oid != "M0423-X-READABLE":
            graph_edges["documentation"].append(edge("READABLE-" + oid, "M0423-X-READABLE", "documents", oid))
    bundle = {
        "schema_version": "stage1-typed-graphs/1.0",
        "item_id": ITEM,
        "theorem_id": THEOREM,
        "registry_id": registry["registry_id"],
        "registry_denominator_sha256": denominator,
        "root_node_id": "THM-M-0423-ROOT",
        "edge_direction": "Proof requirements run parent to child; all reverse proof edges are unverified logical decompositions. Workflow dependencies run task to prerequisite.",
        "endpoint_domains": {"workflow": "task_id", "all_other_graphs": "obligation_id"},
        "workflow_task_nodes": workflow_tasks,
        "proof_obligation_ids": proof_ids,
        "assurance_overlay_ids": overlay_ids,
        "reciprocal_edge_type_contract": {
            "proof": {"proof_requires": ["logical_decomposition"], "logical_decomposition": ["proof_requires"]},
            "refinement": {"expository_decomposition": ["documents"], "documents": ["expository_decomposition"]},
            "trust": {"trusts": ["trusted_by"], "trusted_by": ["trusts"]},
        },
        "nodes": nodes,
        "graphs": {name: indexed(items) for name, items in graph_edges.items()},
        "composition_certificates": [],
        "conditional_lean_harnesses": [
            {"declaration": "Stage1.THM_M_0423.ObligationTree.root_composition", "status": "elaborated conditional function; exact endpoint composition certificate not emitted"},
            {"declaration": "Stage1.THM_M_0423.ObligationTree.direction_package", "status": "elaborated function consuming both directions; not an inhabitant of DirectionPackage"},
            {"declaration": "Stage1.THM_M_0423.ObligationTree.root_from_direction_package", "status": "elaborated conditional function; package premise remains open"},
        ],
        "unverified_decomposition_plans": plans,
        "closure_boundary": {
            "accepted_closed_obligations": [],
            "accepted_evidence_ids": [],
            "root_machine_debt": "M3",
            "root_closed": False,
            "audit_complete": False,
            "theorem_complete": False,
            "immediate_mathematical_cut_under_assumed_valid_top_harnesses": ["M0423-T-LOCAL-GLOBAL"],
            "missing_composition_certificate_cut_set": sorted(REQUIRES),
            "executable_open_leaf_cut_set": proof_leaves,
            "release_gate_cut_set": ["M0423-S-FOUNDATION", "M0423-X-SOURCE", "M0423-X-PROVENANCE", "M0423-X-TRUST", "M0423-X-READABLE", "M0423-X-WORKFLOW", "proof-phase node receipts", "validation and release receipts", "independent verification", "master acceptance"],
            "remaining_root_cut_set": ["all executable open proof leaves", "all missing child-to-parent composition certificates", "all assurance/release gates", "dependency-ordered master acceptance"],
            "reason": "The easy direction and conditional top combinators elaborate, but no E0/E1 evidence or composition certificate is accepted. The hard classification, reciprocity, realization, uniqueness, cancellation, and extraction route remains open.",
        },
    }
    recipe = {
        "schema_version": "stage1-validation-specs/1.0",
        "item_id": ITEM,
        "theorem_id": THEOREM,
        "recipes": [{
            "recipe_id": "VAL-M0423-OBLIGATION-BUNDLE",
            "cwd": ".",
            "argv": ["python3", "-B", "Stage1_Instances/THM-M-0423/check_obligation_tree.py", "--worker-packet", ".stage1-worker-selftest.json"],
            "env_allowlist": {"PATH": "runner-provided pinned tool path", "HOME": "runner-provided toolchain home", "TMPDIR": "runner-provided temporary directory", "PYTHONDONTWRITEBYTECODE": "1", "LEAN_NUM_THREADS": "1"},
            "timeout_seconds": 300,
            "network_policy": "denied",
            "expected_exit": 0,
            "expected_outputs": [
                {"path_or_stream": "stdout", "semantic_hash_policy": "contains PASS THM-M-0423 obligation tree with exact generated counts"},
                {"path_or_stream": "stdout", "semantic_hash_policy": "contains zero accepted closures, root H1/M3/R3, audit_complete=false, theorem_complete=false"},
            ],
            "covered_obligation_ids": ids,
            "covered_declarations": [
                "Stage1.THM_M_0423.HasseMinkowskiStatement",
                "Stage1.THM_M_0423.ObligationTree.isotropic_after_baseChange",
                "Stage1.THM_M_0423.ObligationTree.global_to_local",
                "Stage1.THM_M_0423.ObligationTree.root_composition",
                "Stage1.THM_M_0423.ObligationTree.direction_package",
                "Stage1.THM_M_0423.ObligationTree.root_from_direction_package",
            ],
            "coverage_boundary": "Structural checks cover every registry node. Kernel coverage is limited to the exact statement, two candidate local bodies, and three conditional combinators; it does not cover any planned hard-route signature or create proof credit.",
        }],
        "status_boundary": "Warm provisional worker validation of architecture and named Lean candidates only; no accepted evidence, hard local-to-global proof, audit completion, theorem completion, or release gate.",
    }
    markdown = render_markdown(registry, bundle)
    intake = render_intake(denominator)
    readme = render_readme(len(ids), denominator)
    crosswalk = render_crosswalk()
    validation_markdown = render_validation(registry, bundle)
    return {
        "obligation-registry.json": registry,
        "typed-graphs.json": bundle,
        "validation-specs.json": recipe,
        "obligation-tree.md": markdown,
        "intake.json": intake,
        "README.md": readme,
        "source_statement_crosswalk.md": crosswalk,
        "obligation-tree-validation.md": validation_markdown,
    }


def canonical_bytes(value: object) -> bytes:
    if isinstance(value, str):
        return value.encode()
    return (json.dumps(value, indent=2, ensure_ascii=True) + "\n").encode()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    artifacts = build()
    for name, value in artifacts.items():
        expected = canonical_bytes(value)
        path = HERE / name
        if args.check:
            assert path.read_bytes() == expected, f"generated artifact drift: {name}"
        else:
            path.write_bytes(expected)
    registry = artifacts["obligation-registry.json"]
    bundle = artifacts["typed-graphs.json"]
    assert isinstance(registry, dict) and isinstance(bundle, dict)
    edge_count = sum(len(graph["edges"]) for graph in bundle["graphs"].values())
    action = "checked" if args.check else "wrote"
    print(f"{action} {len(registry['obligations'])} obligations and {edge_count} typed edges")
    print(f"registry denominator sha256: {registry['denominator_sha256']}")


if __name__ == "__main__":
    main()
