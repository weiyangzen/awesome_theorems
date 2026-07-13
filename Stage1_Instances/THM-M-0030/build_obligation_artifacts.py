#!/usr/bin/env python3
"""Build the frozen THM-M-0030 obligation registry and typed graph bundle."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ITEM = "S56-M-0030-OBLIGATION_TREE"
THEOREM = "THM-M-0030"
PREFIX = "M0030"
ROOT_EXPRESSION = "53389852e2c0875086c2c28cb4a60448670ee29145e13d86b4b1ad3e9df8861e"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
FILTRATION_BLOB = "c4fc3737f1859f1e22d387b199b46fe32d5f5093"
JACOBSON_BLOB = "3d8cf7766394242fb36c5998b52b6c6600f96451"
NAKAYAMA_BLOB = "2ec71ea73c3b8e45cb27c597ae51fb94d5d82b07"
LOCAL_RING_BLOB = "9d336345775f1676fb0685c8a1fb8e4e2bdf27ff"
GRAPH_NAMES = (
    "proof",
    "refinement",
    "provenance",
    "evidence",
    "trust",
    "documentation",
    "workflow",
)


def digest(value: object) -> str:
    data = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode()
    return hashlib.sha256(data).hexdigest()


def oid(short: str) -> str:
    return f"{PREFIX}-{short}"


# Eligibility, risk, and architecture are fixed here without consulting candidate closure. Machine
# candidate and accepted statuses are assigned only after the denominator projection is hashed.
ROWS = (
    (
        "ROOT", "root", "critical",
        "Prove the exact proper-ideal Krull intersection target frozen in Statement.lean.",
        "Stage1Instances.THM_M_0030.KrullIntersectionTarget",
        "The intersection of all natural powers of every proper ideal in a commutative Noetherian local ring is bottom.",
        "required", "required", None, 18,
    ),
    (
        "S-INTERFACE", "definition", "critical",
        "Preserve the universe, CommRing, IsNoetherianRing, IsLocalRing, ideal, properness, and natural-power binder order.",
        "Stage1Instances.THM_M_0030.KrullIntersectionTarget",
        "The canonical root interface with no domain, completeness, reducedness, dimension, characteristic, or principal-ideal premise.",
        "required", "required", None, 24,
    ),
    (
        "S-MEMBERSHIP-TRANSPORT", "transport", "high",
        "Relate ideal equality to elementwise membership in every power in both checked directions.",
        "Stage1Instances.THM_M_0030.krullIntersectionTarget_iff_membershipTarget",
        "A checked iff between the canonical ideal equality and its elementwise membership form.",
        "required", "not_applicable", None, 24,
    ),
    (
        "S-PROPER-BOUNDARY", "branch", "high",
        "Exclude I = top as a counter-boundary while retaining I = bottom and the n = 0 power.",
        "Stage1Instances.THM_M_0030.topIdeal_is_counterboundary and bottomIdeal_is_in_scope",
        "The exact properness boundary required by the root, with both sides checked in Lean.",
        "required", "required", None, 28,
    ),
    (
        "S-FOUNDATION", "certificate", "critical",
        "Audit propext, Classical.choice, Quot.sound, kernel, imports, computation policy, and the complete TCB.",
        "planned transitive foundation, axiom, computation, and TCB report",
        "An accepted foundation boundary for every terminal declaration and composition.",
        "required", "not_applicable", None, 55,
    ),
    (
        "X-MATHLIB-BODY", "bridge", "critical",
        "Install or otherwise validate the exact pinned Ideal.iInf_pow_eq_bot_of_isLocalRing body without duplicating its audit wrapper.",
        "Ideal.iInf_pow_eq_bot_of_isLocalRing",
        "The exact mathlib-order anchor consumed by the checked binder-order adapter to the root.",
        "required", "required", f"git-blob:{FILTRATION_BLOB}:Ideal.iInf_pow_eq_bot_of_isLocalRing", 32,
    ),
    (
        "N-FINITE-MODULE", "reduction", "critical",
        "For every finite module M, the intersection of I^n acting on top is bottom for a proper ideal of a Noetherian local ring.",
        "Stage1Instances.THM_M_0030.ObligationTree.FiniteModuleIntersectionTarget",
        "The exact finite-module intersection proposition consumed by the M = R specialization.",
        "required", "required", f"git-blob:{FILTRATION_BLOB}:Ideal.iInf_pow_smul_eq_bot_of_isLocalRing", 30,
    ),
    (
        "N-JACOBSON", "reduction", "critical",
        "For every finite module M, I below the Jacobson radical of bottom forces the intersection of I^n acting on top to be bottom.",
        "Stage1Instances.THM_M_0030.ObligationTree.JacobsonIntersectionTarget",
        "The exact general Jacobson-intersection proposition consumed by local specialization.",
        "required", "required", f"git-blob:{FILTRATION_BLOB}:Ideal.iInf_pow_smul_eq_bot_of_le_jacobson", 28,
    ),
    (
        "N-LOCAL-CONTAINMENT", "reduction", "critical",
        "Every proper ideal in a commutative local ring lies below the Jacobson radical of bottom.",
        "Stage1Instances.THM_M_0030.ObligationTree.LocalProperIdealJacobsonTarget",
        "The exact local containment consumed together with the general Jacobson theorem.",
        "required", "required", None, 20,
    ),
    (
        "L-PROPER-MAXIMAL", "core_lemma", "high",
        "Every proper ideal in a local ring lies below its unique maximal ideal.",
        "Stage1Instances.THM_M_0030.ObligationTree.ProperToMaximalTarget",
        "I <= IsLocalRing.maximalIdeal R.",
        "required", "required", f"git-blob:{LOCAL_RING_BLOB}:IsLocalRing.le_maximalIdeal", 20,
    ),
    (
        "L-MAXIMAL-JACOBSON", "core_lemma", "high",
        "The unique maximal ideal of a local ring lies below the Jacobson radical of bottom.",
        "Stage1Instances.THM_M_0030.ObligationTree.MaximalToJacobsonTarget",
        "IsLocalRing.maximalIdeal R <= Ideal.jacobson bottom.",
        "required", "required", f"git-blob:{LOCAL_RING_BLOB}:IsLocalRing.maximalIdeal_le_jacobson", 20,
    ),
    (
        "L-JACOBSON-UNIT", "bridge", "critical",
        "Turn r in the Jacobson radical into invertibility of 1-r and cancel its scalar action.",
        "Stage1Instances.THM_M_0030.ObligationTree.JacobsonUnitTarget",
        "An invertible scalar 1-r for the terminal fixed-point cancellation.",
        "required", "required", None, 45,
    ),
    (
        "X-JACOBSON-UNIT-SOURCE", "lemma", "critical",
        "If s-1 lies in the Jacobson radical of bottom, then s is a unit.",
        "Stage1Instances.THM_M_0030.ObligationTree.JacobsonUnitSourceTarget",
        "The source-shaped unit proposition consumed by the checked sign adapter.",
        "required", "required", f"git-blob:{JACOBSON_BLOB}:Ideal.isUnit_of_sub_one_mem_jacobson_bot", 30,
    ),
    (
        "N-FIXEDPOINT-IFF", "core_lemma", "critical",
        "Characterize membership in the intersection of I^n times top by a coefficient r in I fixing the element.",
        "Ideal.mem_iInf_smul_pow_eq_bot_iff",
        "For each x, intersection membership iff there exists r in I with r smul x = x.",
        "required", "required", f"git-blob:{FILTRATION_BLOB}:Ideal.mem_iInf_smul_pow_eq_bot_iff", 70,
    ),
    (
        "T-FIXEDPOINT-COMPOSE", "terminal", "critical",
        "Compose the forward and backward fixed-point directions into the exact iff used by the Jacobson proof.",
        "visible body of Ideal.mem_iInf_smul_pow_eq_bot_iff",
        "The complete fixed-point characterization, with both directions consumed.",
        "required", "required", None, 30,
    ),
    (
        "C-INFIMUM-SUBMODULE", "construction", "high",
        "Define N as the infimum of I^n times top and prove N is contained in every power term.",
        "let N := iInf fun i : Nat => I ^ i smul top; iInf_le",
        "A well-defined submodule N with all power-containment interfaces needed downstream.",
        "required", "required", None, 40,
    ),
    (
        "C-STABLE-INTERSECTION", "construction", "critical",
        "Intersect the stable I-power filtration with the trivial filtration at N and retain the resulting Stable witness.",
        "Ideal.stableFiltration_stable, Ideal.Filtration.Stable.inter_right, and Ideal.trivialFiltration",
        "Stability of the intersection filtration, without prematurely asserting N = I smul N.",
        "required", "required", f"git-blob:{FILTRATION_BLOB}:Ideal.Filtration.Stable.inter_right", 55,
    ),
    (
        "L-STABILIZATION-INDEX", "lemma", "critical",
        "Choose an index k at which the stable intersection filtration satisfies I smul F.N k = F.N (k+1).",
        "Ideal.Filtration.Stable",
        "An explicit k and the stabilization equality at k.",
        "required", "required", None, 30,
    ),
    (
        "T-STABILITY-EVALUATE", "terminal", "critical",
        "Evaluate both stabilized filtration terms as N and derive N <= I smul N.",
        "the hN evaluation and hk k step in Ideal.mem_iInf_smul_pow_eq_bot_iff",
        "The exact self-similarity premise N <= I smul N used by finite generation.",
        "required", "required", None, 35,
    ),
    (
        "L-FG-NAKAYAMA", "bridge", "critical",
        "Use Noetherian finite generation and N <= I smul N to obtain one r in I fixing every element of N.",
        "Submodule.exists_mem_and_smul_eq_self_of_fg_of_le_smul",
        "A uniform coefficient r in I with r smul n = n for all n in N.",
        "required", "required", f"git-blob:{NAKAYAMA_BLOB}:Submodule.exists_mem_and_smul_eq_self_of_fg_of_le_smul", 70,
    ),
    (
        "B-FIXEDPOINT-FORWARD", "branch", "critical",
        "From x in every I-power, construct r in I with r smul x = x using the stable finitely generated intersection N.",
        "forward branch of Ideal.mem_iInf_smul_pow_eq_bot_iff",
        "The forward implication from intersection membership to a fixed-point witness.",
        "required", "required", None, 60,
    ),
    (
        "B-FIXEDPOINT-BACKWARD", "branch", "high",
        "From r in I fixing x, prove by induction that x lies in every I-power acting on top.",
        "backward branch of Ideal.mem_iInf_smul_pow_eq_bot_iff",
        "The backward implication from a fixed-point witness to intersection membership.",
        "required", "required", None, 50,
    ),
    (
        "L-POWER-INDUCTION", "core_lemma", "high",
        "Establish the zero power base and successor step by rewriting powers and using r in I.",
        "Nat induction with Submodule.smul_mem_smul",
        "Membership of x in I^n times top for every natural n.",
        "required", "required", None, 45,
    ),
    (
        "X-SOURCE", "terminal", "critical",
        "Pinpoint and independently review the historical and modern source assumptions, proof steps, definitions, and errata for every material node.",
        "non-machine primary-source crosswalk",
        "Human-source evidence without machine proof credit.",
        "not_applicable", "required", None, 85,
    ),
    (
        "X-PROVENANCE", "certificate", "critical",
        "Resolve wrapper, terminal body, source blob, imports, licenses, direct declarations, and transitive declaration origins.",
        "planned machine-derived provenance closure",
        "Release provenance without mathematical proof credit.",
        "informational", "not_applicable", None, 65,
    ),
    (
        "X-TRUST", "certificate", "critical",
        "Resolve kernel, compiled artifacts, executables, axiom closure, supply chain, and offline replay boundaries.",
        "planned release trust and TCB closure",
        "Release trust evidence without mathematical proof credit.",
        "informational", "not_applicable", None, 65,
    ),
    (
        "X-READABLE", "terminal", "high",
        "Produce and independently review a complete readable reconstruction of the fixed-point and Jacobson route.",
        "planned node-specific readable reconstruction",
        "Readable coverage and review without machine proof credit.",
        "not_applicable", "required", None, 95,
    ),
    (
        "X-WORKFLOW", "certificate", "high",
        "Bind proof, validation, release, freshness, revocation, and independent-verification task acceptance.",
        "planned Stage1 workflow receipts",
        "Workflow acceptance without mathematical proof credit.",
        "informational", "not_applicable", None, 50,
    ),
)


# These edges have local conditional Lean composition certificates. The audited proof bodies remain
# explicit premises, so checking them does not install or accept the terminal theorem.
REQUIRES = {
    oid("ROOT"): [oid("X-MATHLIB-BODY")],
    oid("X-MATHLIB-BODY"): [oid("N-FINITE-MODULE")],
    oid("N-FINITE-MODULE"): [oid("N-JACOBSON"), oid("N-LOCAL-CONTAINMENT")],
    oid("N-LOCAL-CONTAINMENT"): [oid("L-PROPER-MAXIMAL"), oid("L-MAXIMAL-JACOBSON")],
    oid("N-JACOBSON"): [oid("N-FIXEDPOINT-IFF"), oid("L-JACOBSON-UNIT")],
    oid("L-JACOBSON-UNIT"): [oid("X-JACOBSON-UNIT-SOURCE")],
}

# The visible internals of the pinned fixed-point theorem are semantic decompositions. The exact
# two-branch iff interface is checked locally; the deeper source-body decomposition stays open for
# later proof work and therefore cannot close via `composes` in this phase.
BODY_DECOMPOSITION = {
    oid("N-FIXEDPOINT-IFF"): [oid("T-FIXEDPOINT-COMPOSE")],
    oid("T-FIXEDPOINT-COMPOSE"): [
        oid("B-FIXEDPOINT-FORWARD"), oid("B-FIXEDPOINT-BACKWARD")
    ],
    oid("B-FIXEDPOINT-FORWARD"): [
        oid("C-INFIMUM-SUBMODULE"), oid("C-STABLE-INTERSECTION"), oid("L-FG-NAKAYAMA")
    ],
    oid("C-STABLE-INTERSECTION"): [oid("C-INFIMUM-SUBMODULE")],
    oid("L-STABILIZATION-INDEX"): [oid("C-STABLE-INTERSECTION")],
    oid("T-STABILITY-EVALUATE"): [
        oid("C-INFIMUM-SUBMODULE"), oid("C-STABLE-INTERSECTION"), oid("L-STABILIZATION-INDEX")
    ],
    oid("L-FG-NAKAYAMA"): [oid("T-STABILITY-EVALUATE")],
    oid("B-FIXEDPOINT-BACKWARD"): [oid("L-POWER-INDUCTION")],
}

CHECKED_INTERFACES = {
    oid("S-INTERFACE"),
    oid("S-MEMBERSHIP-TRANSPORT"),
    oid("S-PROPER-BOUNDARY"),
}
CONDITIONAL_COMPOSITIONS = {
    oid("ROOT"),
    oid("X-MATHLIB-BODY"),
    oid("N-FINITE-MODULE"),
    oid("N-JACOBSON"),
    oid("N-LOCAL-CONTAINMENT"),
    oid("L-JACOBSON-UNIT"),
    oid("T-FIXEDPOINT-COMPOSE"),
}
SOURCE_NA = {
    oid("S-MEMBERSHIP-TRANSPORT"), oid("S-FOUNDATION"), oid("X-PROVENANCE"),
    oid("X-TRUST"), oid("X-WORKFLOW"),
}
REGISTRY_KIND = {
    "root": "root", "definition": "definition", "reduction": "reduction",
    "branch": "branch", "construction": "construction", "transport": "transport",
    "terminal": "terminal", "bridge": "lemma", "core_lemma": "lemma",
    "lemma": "lemma", "certificate": "terminal",
}
NODE_KIND = {
    "lemma": "core_lemma",
    "certificate": "certificate",
}
PINNED_SOURCE_BY_ID = {
    oid("X-MATHLIB-BODY"): "Mathlib/RingTheory/Filtration.lean#Ideal.iInf_pow_eq_bot_of_isLocalRing",
    oid("N-FINITE-MODULE"): "Mathlib/RingTheory/Filtration.lean#Ideal.iInf_pow_smul_eq_bot_of_isLocalRing",
    oid("N-JACOBSON"): "Mathlib/RingTheory/Filtration.lean#Ideal.iInf_pow_smul_eq_bot_of_le_jacobson",
    oid("L-PROPER-MAXIMAL"): "Mathlib/RingTheory/LocalRing/MaximalIdeal/Basic.lean#IsLocalRing.le_maximalIdeal",
    oid("L-MAXIMAL-JACOBSON"): "Mathlib/RingTheory/LocalRing/MaximalIdeal/Basic.lean#IsLocalRing.maximalIdeal_le_jacobson",
    oid("X-JACOBSON-UNIT-SOURCE"): "Mathlib/RingTheory/Jacobson/Ideal.lean#Ideal.isUnit_of_sub_one_mem_jacobson_bot",
    oid("N-FIXEDPOINT-IFF"): "Mathlib/RingTheory/Filtration.lean#Ideal.mem_iInf_smul_pow_eq_bot_iff",
    oid("C-STABLE-INTERSECTION"): "Mathlib/RingTheory/Filtration.lean#Ideal.Filtration.Stable.inter_right",
    oid("L-STABILIZATION-INDEX"): "Mathlib/RingTheory/Filtration.lean#Ideal.Filtration.Stable (definition dependency; no proof-body credit)",
    oid("L-FG-NAKAYAMA"): "Mathlib/RingTheory/Finiteness/Nakayama.lean#Submodule.exists_mem_and_smul_eq_self_of_fg_of_le_smul",
}


def substantive_steps(identifier: str, children: list[str], parents: list[str], target: str,
                      output: str) -> list[dict]:
    """Return a stable, node-specific semantic ledger rather than an asserted budget count."""
    routes: dict[str, list[tuple[list[str], str, str]]] = {
        oid("ROOT"): [
            ([oid("X-MATHLIB-BODY")], "root_of_exactMathlibAnchor: introduce the canonical binders and reorder only the source interface", output),
        ],
        oid("S-INTERFACE"): [
            ([oid("ROOT")], "freeze R : Type u with CommRing, IsNoetherianRing, and IsLocalRing", "the exact ring and typeclass context"),
            ([f"{identifier}-STEP-01"], "freeze I : Ideal R and I != top after the ring context", "the exact proper-ideal binder context"),
            ([f"{identifier}-STEP-02"], "freeze iInf over every n : Nat with conclusion bottom", output),
        ],
        oid("S-MEMBERSHIP-TRANSPORT"): [
            ([oid("ROOT")], "Ideal.mem_iInf.mpr and rewrite by the root equality", "root implies MembershipTarget"),
            ([f"{identifier}-STEP-01"], "Ideal.mem_iInf.mp, ideal extensionality, and bot_le", output),
        ],
        oid("S-PROPER-BOUNDARY"): [
            ([oid("S-INTERFACE")], "evaluate every power of top and use top_ne_bot", "I = top falsifies the conclusion"),
            ([oid("S-INTERFACE")], "evaluate the n = 1 bound for bottom and use bot_ne_top", "I = bottom is proper and satisfies the conclusion"),
            ([f"{identifier}-STEP-01", f"{identifier}-STEP-02"], "combine the excluded and included boundary witnesses", output),
        ],
        oid("X-MATHLIB-BODY"): [
            ([oid("N-FINITE-MODULE")], "specialize the finite-module theorem at M = R", "iInf (I^n smul top : Submodule R R) = bottom"),
            ([f"{identifier}-STEP-01"], "convert submodules to ideals using smul_eq_mul, one_eq_top, and mul_one", output),
        ],
        oid("N-FINITE-MODULE"): [
            ([oid("N-LOCAL-CONTAINMENT")], "obtain I <= Ideal.jacobson bottom from properness and locality", "the exact Jacobson containment premise"),
            ([oid("N-JACOBSON"), f"{identifier}-STEP-01"], "apply the general Jacobson-intersection child", output),
        ],
        oid("N-LOCAL-CONTAINMENT"): [
            ([oid("L-PROPER-MAXIMAL")], "map a proper ideal into the unique maximal ideal", "I <= IsLocalRing.maximalIdeal R"),
            ([oid("L-MAXIMAL-JACOBSON")], "map the unique maximal ideal into Ideal.jacobson bottom", "IsLocalRing.maximalIdeal R <= Ideal.jacobson bottom"),
            ([f"{identifier}-STEP-01", f"{identifier}-STEP-02"], "transitivity of ideal inclusion", output),
        ],
        oid("L-PROPER-MAXIMAL"): [
            ([oid("S-INTERFACE")], "pinned IsLocalRing.le_maximalIdeal applied to I != top", output),
        ],
        oid("L-MAXIMAL-JACOBSON"): [
            ([oid("S-INTERFACE")], "pinned IsLocalRing.maximalIdeal_le_jacobson at bottom", output),
        ],
        oid("L-JACOBSON-UNIT"): [
            ([oid("X-JACOBSON-UNIT-SOURCE")], "instantiate the source theorem at s = 1-r", "(1-r)-1 in the Jacobson radical implies IsUnit (1-r)"),
            ([f"{identifier}-STEP-01"], "use additive closure under negation and simplify (1-r)-1 = -r", output),
        ],
        oid("X-JACOBSON-UNIT-SOURCE"): [
            ([f"{identifier}-COMM-RING-CONTEXT", f"{identifier}-JACOBSON-MEMBERSHIP"], "pinned Ideal.isUnit_of_sub_one_mem_jacobson_bot", output),
        ],
        oid("N-JACOBSON"): [
            ([oid("N-FIXEDPOINT-IFF")], "for x in the intersection obtain r in I with r smul x = x", "a fixed-point witness r for x"),
            ([oid("L-JACOBSON-UNIT"), f"{identifier}-STEP-01"], "use I <= jacobson bottom to prove IsUnit (1-r)", "an invertible scalar 1-r"),
            ([f"{identifier}-STEP-01", f"{identifier}-STEP-02"], "cancel the unit action and simplify sub_smul using r smul x = x", "x = 0"),
            ([f"{identifier}-STEP-03"], "eq_bot_iff", output),
        ],
        oid("N-FIXEDPOINT-IFF"): [
            ([oid("T-FIXEDPOINT-COMPOSE")], "identify the composed forward/backward interface with the pinned fixed-point declaration", output),
        ],
        oid("T-FIXEDPOINT-COMPOSE"): [
            ([oid("B-FIXEDPOINT-FORWARD")], "export the forward branch", "the forward implication"),
            ([oid("B-FIXEDPOINT-BACKWARD")], "export the backward branch", "the backward implication"),
            ([f"{identifier}-STEP-01", f"{identifier}-STEP-02"], "construct the exact iff with no omitted branch", output),
        ],
        oid("C-INFIMUM-SUBMODULE"): [
            ([oid("S-INTERFACE")], "define N := iInf fun i : Nat => I^i smul top", "a submodule N"),
            ([f"{identifier}-STEP-01"], "iInf_le at each k", output),
        ],
        oid("C-STABLE-INTERSECTION"): [
            ([oid("C-INFIMUM-SUBMODULE")], "construct the stable power filtration and trivial filtration at N", "two I-filtrations"),
            ([f"{identifier}-STEP-01"], "Ideal.stableFiltration_stable followed by Stable.inter_right", output),
        ],
        oid("L-STABILIZATION-INDEX"): [
            ([oid("C-STABLE-INTERSECTION")], "unpack Stable as an eventual equality witness", "an index k and forall n >= k, I smul F.N n = F.N (n+1)"),
            ([f"{identifier}-STEP-01"], "specialize the witness at n = k and le_refl k", output),
        ],
        oid("T-STABILITY-EVALUATE"): [
            ([oid("C-INFIMUM-SUBMODULE"), oid("C-STABLE-INTERSECTION")], "prove hN j: the stable intersection filtration term at every j equals N", "F.N k = N and F.N (k+1) = N"),
            ([oid("L-STABILIZATION-INDEX"), f"{identifier}-STEP-01"], "rewrite both sides of the specialized stability equality by hN", "I smul N = N"),
            ([f"{identifier}-STEP-02"], "reverse the equality and take its le direction", output),
        ],
        oid("L-FG-NAKAYAMA"): [
            ([oid("C-INFIMUM-SUBMODULE")], "IsNoetherian.noetherian N supplies N.FG", "finite generation of N"),
            ([oid("T-STABILITY-EVALUATE"), f"{identifier}-STEP-01"], "apply Submodule.exists_mem_and_smul_eq_self_of_fg_of_le_smul", output),
        ],
        oid("B-FIXEDPOINT-FORWARD"): [
            ([oid("C-INFIMUM-SUBMODULE"), oid("C-STABLE-INTERSECTION")], "interpret hx as x in the stable intersection N", "x belongs to the finitely generated stable intersection N"),
            ([oid("L-FG-NAKAYAMA"), f"{identifier}-STEP-01"], "specialize the uniform Nakayama witness at x", output),
        ],
        oid("B-FIXEDPOINT-BACKWARD"): [
            ([oid("L-POWER-INDUCTION")], "obtain x in I^n smul top for every n", "pointwise membership in every power term"),
            ([f"{identifier}-STEP-01"], "Submodule.mem_iInf", output),
        ],
        oid("L-POWER-INDUCTION"): [
            ([f"{identifier}-FIXED-POINT-CONTEXT"], "base n = 0: simplify I^0 smul top to top", "x belongs to the zero power term"),
            ([f"{identifier}-FIXED-POINT-CONTEXT", f"{identifier}-INDUCTION-HYPOTHESIS"], "successor: rewrite pow_succ and smul_smul, replace x by r smul x", "x belongs to I^(n+1) smul top"),
            ([f"{identifier}-STEP-01", f"{identifier}-STEP-02"], "Nat induction", output),
        ],
    }
    actions = routes.get(identifier)
    if actions is None:
        premise_ids = children if children else [oid("ROOT")]
        actions = [(premise_ids, target, output)]
    steps = []
    for index, (premises, inference, claim) in enumerate(actions, start=1):
        step_id = f"{identifier}-STEP-{index:02d}"
        next_id = (
            f"{identifier}-STEP-{index + 1:02d}" if index < len(actions)
            else (parents if parents else [f"{identifier}-PUBLIC-BOUNDARY"])
        )
        steps.append({
            "step_id": step_id,
            "premise_ids": premises,
            "inference_or_source": inference,
            "output_claim": claim,
            "outgoing_use_ids": [next_id] if isinstance(next_id, str) else next_id,
        })
    return steps


def build() -> tuple[dict, dict, dict]:
    statement_hash = hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest()
    anchor_hash = hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest()
    parent_map: dict[str, list[str]] = {}
    all_architecture_edges = {**REQUIRES, **BODY_DECOMPOSITION}
    for parent, children in all_architecture_edges.items():
        for child in children:
            parent_map.setdefault(child, []).append(parent)

    obligations: list[dict] = []
    row_by_id: dict[str, tuple] = {}
    for row in ROWS:
        short, kind, risk, claim, target, output, machine, human_source, body, budget = row
        identifier = oid(short)
        row_by_id[identifier] = row
        fingerprint = (
            f"lean-expression-sha256:{ROOT_EXPRESSION}"
            if identifier in {oid("ROOT"), oid("S-INTERFACE")} else
            "planned:v1:sha256:" + digest([identifier, kind, claim, target, output])
        )
        exclusion = None
        if machine != "required" or human_source != "required":
            exclusion = {
                oid("S-MEMBERSHIP-TRANSPORT"): "formal_transport_source_coverage_inherited_from_root_pending_reviewer_acceptance",
                oid("S-FOUNDATION"): "formal_trust_boundary_not_a_human_claim_pending_reviewer_acceptance",
                oid("X-SOURCE"): "human_source_boundary_only_pending_independent_source_review",
                oid("X-PROVENANCE"): "provenance_overlay_no_proof_credit_pending_integration_review",
                oid("X-TRUST"): "trust_overlay_no_proof_credit_pending_integration_review",
                oid("X-READABLE"): "readability_boundary_only_pending_independent_review",
                oid("X-WORKFLOW"): "workflow_overlay_no_proof_credit_pending_integration_review",
            }[identifier]
        obligations.append({
            "obligation_id": identifier,
            "statement_fingerprint": fingerprint,
            "kind": REGISTRY_KIND[kind],
            "root_relevant": True,
            "machine_eligibility": machine,
            "human_source_eligibility": human_source,
            "readable_eligibility": "required",
            "risk_class": risk,
            "exclusion_reason": exclusion,
            "terminal_proof_body_id": body,
        })

    fields = (
        "obligation_id", "statement_fingerprint", "kind", "root_relevant",
        "machine_eligibility", "human_source_eligibility", "readable_eligibility",
        "risk_class", "exclusion_reason", "terminal_proof_body_id",
    )
    denominator = digest([{field: record[field] for field in fields} for record in obligations])
    ids = [record["obligation_id"] for record in obligations]

    nodes: list[dict] = []
    for obligation in obligations:
        identifier = obligation["obligation_id"]
        short, kind, _risk, claim, target, output, _machine, _human, _body, budget = row_by_id[identifier]
        if identifier in CHECKED_INTERFACES:
            candidate_status = "kernel-checked local interface; no proof-closure credit"
        elif identifier == oid("X-MATHLIB-BODY"):
            candidate_status = "exact pinned E2 candidate; accepted classification remains M3 until E1 proof-phase admission"
        elif identifier in CONDITIONAL_COMPOSITIONS:
            candidate_status = "kernel-checked conditional composition; required child premises remain open"
        elif identifier in PINNED_SOURCE_BY_ID:
            candidate_status = "located pinned supporting declaration/body; node evidence is unaccepted"
        else:
            candidate_status = "planned architecture only"
        accepted_machine_debt = "M3" if (
            identifier in CHECKED_INTERFACES | CONDITIONAL_COMPOSITIONS
            or identifier in PINNED_SOURCE_BY_ID
        ) else "M4"
        if identifier == oid("X-MATHLIB-BODY"):
            provenance = "anchor-audit:M0030-C01-MATHLIB-EXACT"
        elif identifier in CONDITIONAL_COMPOSITIONS:
            provenance = "local-conditional-composition"
        elif identifier in {item for values in BODY_DECOMPOSITION.values() for item in values}:
            provenance = "pinned-visible-terminal-body"
        else:
            provenance = "none"
        owned_sources: list[str] = []
        if identifier in CONDITIONAL_COMPOSITIONS:
            owned_sources = [f"Stage1_Instances/{THEOREM}/ObligationTree.lean"]
        elif identifier in CHECKED_INTERFACES:
            owned_sources = [f"Stage1_Instances/{THEOREM}/Statement.lean"]
        elif identifier in PINNED_SOURCE_BY_ID:
            owned_sources = [
                f"pinned-mathlib:{MATHLIB_REVISION}:{PINNED_SOURCE_BY_ID[identifier]}"
            ]
        children = all_architecture_edges.get(identifier, [])
        parents = parent_map.get(identifier, [])
        nodes.append({
            "node_id": f"{THEOREM}-{short}",
            "obligation_id": identifier,
            "kind": NODE_KIND.get(kind, kind),
            "human_statement": claim,
            "formal_target": target,
            "output": output,
            "human_debt": "H1",
            "machine_debt": accepted_machine_debt,
            "machine_candidate_status": candidate_status,
            "readability_debt": "R3",
            "evidence_ids": [],
            "source_crosswalk_id": (
                "not-applicable-pending-review" if identifier in SOURCE_NA
                else "primary-source-node-map-pending-independent-review"
            ),
            "provenance_id": provenance,
            "foundation_profile": "lean4-dependent-type-theory; accepted axiom policy and transitive review pending",
            "tcb_profile": "lean-4.29.0+mathlib-8a178386; transitive closure and independent replay pending",
            "computation_record": "none; no native computation, solver, oracle, experiment, or unchecked certificate is credited",
            "step_budget": budget,
            "semantic_step_ledger": {
                "premises": children if children else ["exact formal context and no undeclared mathematical premise"],
                "inference": claim,
                "output": output,
                "outgoing_use": parents if parents else ["typed support edge only or canonical terminal output"],
                "steps": substantive_steps(identifier, children, parents, target, output),
            },
            "public_readable_target": f"Stage1_Instances/{THEOREM}/obligation-tree.md#{identifier.lower()}",
            "validation_spec_id": f"VAL-{identifier}",
            "status_boundary": "Frozen architecture, audited candidate, or conditional interface only; no accepted proof state, H0, R0, or theorem completion.",
            "task_ids": [ITEM, "S56-M-0030-PROOF"],
            "owned_sources": owned_sources,
            "owner": "THM-M-0030 proof lane",
            "reviewer": "independent Stage1 integration lane",
            "validity": {
                "validated_at": "2026-07-13" if identifier in CHECKED_INTERFACES | CONDITIONAL_COMPOSITIONS else None,
                "review_due": "before proof acceptance",
                "invalidation_inputs": [
                    "Statement.lean", "anchor-audit.json", "obligation-registry.json",
                    "typed-graphs.json", "toolchain and dependency pins",
                ],
                "revocation_state": "provisional" if identifier in CHECKED_INTERFACES | CONDITIONAL_COMPOSITIONS else "open",
            },
        })

    registry = {
        "schema_version": "stage1-obligation-registry/1.0",
        "item_id": ITEM,
        "theorem_id": THEOREM,
        "registry_id": "THM-M-0030-OBLIGATIONS-v1",
        "registry_version": 1,
        "frozen_at": "2026-07-13T00:00:00+08:00",
        "freeze_basis": "The exact statement and visible semantic architecture of the pinned terminal body. Eligibility, risks, and denominators are architecture-derived without using candidate closure status.",
        "frozen_against_statement_sha256": statement_hash,
        "frozen_against_anchor_audit_sha256": anchor_hash,
        "root_obligation_id": oid("ROOT"),
        "denominator_sha256": denominator,
        "frozen_denominators": {
            "inventory": ids,
            "required_machine": [r["obligation_id"] for r in obligations if r["machine_eligibility"] == "required"],
            "required_human_source": [r["obligation_id"] for r in obligations if r["human_source_eligibility"] == "required"],
            "required_readable": ids,
            "informational_overlays": [r["obligation_id"] for r in obligations if r["machine_eligibility"] == "informational"],
        },
        "layer_exclusions": {
            "representative_symmetry_sign_order_normalization": {
                "status": "not_applicable_pending_independent_approval",
                "reason": "The pinned route has no representative quotient, sign, symmetry, or order normalization; its ideal-to-module conversion is an explicit reduction node.",
            },
            "additional_finite_infinite_or_local_global_normalization": {
                "status": "not_applicable_pending_independent_approval",
                "reason": "The only local transition is the explicit proper-local-ideal to Jacobson reduction; no finite/infinite or further local/global split occurs in the visible body.",
            },
            "computation": {
                "status": "not_applicable_pending_independent_approval",
                "reason": "No reflection, solver, native code, oracle, experiment, finite computation, or certificate occurs in the visible terminal body.",
            },
        },
        "proof_body_aliases": {
            "Stage1Instances.THM_M_0030_AnchorAudit.exactTarget_mathlib_candidate": "deduplicated_to:Ideal.iInf_pow_eq_bot_of_isLocalRing",
            "Stage1Instances.THM_M_0030.ObligationTree.root_of_exactMathlibAnchor": "conditional_adapter_no_distinct_terminal_body",
            "future proof-phase canonical wrapper": "deduplicated_to:Ideal.iInf_pow_eq_bot_of_isLocalRing",
        },
        "supporting_same_path_declarations": [
            "Ideal.iInf_pow_smul_eq_bot_of_isLocalRing",
            "Ideal.iInf_pow_smul_eq_bot_of_le_jacobson",
            "Ideal.mem_iInf_smul_pow_eq_bot_iff",
            "Submodule.exists_mem_and_smul_eq_self_of_fg_of_le_smul",
        ],
        "delta_policy": "Any target change, correction, split, merge, exclusion, eligibility/risk change, or proof-body identity change requires registry version 2 and an append-only old/new ID delta.",
        "append_only_delta": [],
        "obligations": obligations,
        "status_observed_after_freeze": {
            "checked_interface_obligations": sorted(CHECKED_INTERFACES),
            "conditional_composition_obligations": sorted(CONDITIONAL_COMPOSITIONS),
            "audited_candidate_obligation": oid("X-MATHLIB-BODY"),
            "audited_candidate_classification": "exact_pinned_E2_candidate_accepted_root_remains_M3_pending_E1_proof_phase_and_master_acceptance",
            "accepted_closed_obligations": [],
            "root_machine_debt": "M3",
        },
        "status_boundary": "Registry and typed architecture only. The exact candidate is not installed or accepted; H0, R0, audit completion, validation, release, and theorem completion remain open.",
    }
    hash_fields = (
        "schema_version", "item_id", "theorem_id", "registry_id", "registry_version",
        "frozen_at", "freeze_basis", "frozen_against_statement_sha256",
        "frozen_against_anchor_audit_sha256", "root_obligation_id", "denominator_sha256",
        "frozen_denominators", "layer_exclusions", "proof_body_aliases",
        "supporting_same_path_declarations", "delta_policy", "append_only_delta", "obligations",
        "status_boundary",
    )
    registry["registry_hash_fields"] = list(hash_fields)
    registry["registry_content_sha256"] = digest({field: registry[field] for field in hash_fields})

    def edge(edge_id: str, source: str, edge_type: str, target: str, reciprocal: str | None = None) -> dict:
        value = {"edge_id": edge_id, "from": source, "type": edge_type, "to": target}
        if reciprocal is not None:
            value["reciprocal_edge_id"] = reciprocal
        return value

    proof: list[dict] = []
    for parent, children in REQUIRES.items():
        for child in children:
            req = f"REQ-{parent}-{child}"
            comp = f"CMP-{child}-{parent}"
            proof.extend([
                edge(req, parent, "proof_requires", child, comp),
                edge(comp, child, "composes", parent, req),
            ])
    graph_edges = {
        "proof": proof,
        "refinement": [
            edge("REF-ROOT-INTERFACE", oid("ROOT"), "logical_decomposition", oid("S-INTERFACE")),
            edge("REF-ROOT-BOUNDARY", oid("ROOT"), "logical_decomposition", oid("S-PROPER-BOUNDARY")),
            edge("EQ-ROOT-MEMBERSHIP", oid("ROOT"), "equivalent_to", oid("S-MEMBERSHIP-TRANSPORT")),
            edge("EQ-MEMBERSHIP-ROOT", oid("S-MEMBERSHIP-TRANSPORT"), "equivalent_to", oid("ROOT")),
        ] + [
            edge(f"REF-{parent}-{child}", parent, "logical_decomposition", child)
            for parent, children in BODY_DECOMPOSITION.items() for child in children
        ],
        "provenance": [
            edge("SRC-ROOT", oid("X-SOURCE"), "source_map", oid("ROOT")),
            edge("SRC-FIXEDPOINT", oid("X-SOURCE"), "source_map", oid("N-FIXEDPOINT-IFF")),
            edge("SRC-NAKAYAMA", oid("X-SOURCE"), "source_map", oid("L-FG-NAKAYAMA")),
            edge("PROV-BODY", oid("X-PROVENANCE"), "provenance_of", oid("X-MATHLIB-BODY")),
            edge("PROV-FINITE-MODULE", oid("X-PROVENANCE"), "provenance_of", oid("N-FINITE-MODULE")),
            edge("PROV-JACOBSON", oid("X-PROVENANCE"), "provenance_of", oid("N-JACOBSON")),
            edge("PROV-PROPER-MAXIMAL", oid("X-PROVENANCE"), "provenance_of", oid("L-PROPER-MAXIMAL")),
            edge("PROV-MAXIMAL-JACOBSON", oid("X-PROVENANCE"), "provenance_of", oid("L-MAXIMAL-JACOBSON")),
            edge("PROV-FIXEDPOINT", oid("X-PROVENANCE"), "provenance_of", oid("N-FIXEDPOINT-IFF")),
            edge("PROV-UNIT", oid("X-PROVENANCE"), "provenance_of", oid("X-JACOBSON-UNIT-SOURCE")),
            edge("PROV-STABLE", oid("X-PROVENANCE"), "provenance_of", oid("C-STABLE-INTERSECTION")),
            edge("PROV-NAKAYAMA", oid("X-PROVENANCE"), "provenance_of", oid("L-FG-NAKAYAMA")),
        ],
        "evidence": [
            edge("EVID-BODY", oid("X-PROVENANCE"), "evidence_for", oid("X-MATHLIB-BODY")),
            edge("EVID-WORKFLOW", oid("X-WORKFLOW"), "evidence_for", oid("ROOT")),
        ],
        "trust": [
            edge("TRUST-ROOT-FOUNDATION", oid("ROOT"), "trusts", oid("S-FOUNDATION")),
            edge("TRUST-ROOT-TCB", oid("ROOT"), "trusts", oid("X-TRUST")),
            edge("TRUST-BODY-TCB", oid("X-MATHLIB-BODY"), "trusts", oid("X-TRUST")),
        ] + [
            edge(f"TRUST-{identifier}-TCB", identifier, "trusts", oid("X-TRUST"))
            for identifier in (
                oid("N-FINITE-MODULE"), oid("N-JACOBSON"), oid("L-PROPER-MAXIMAL"),
                oid("L-MAXIMAL-JACOBSON"), oid("X-JACOBSON-UNIT-SOURCE"),
                oid("N-FIXEDPOINT-IFF"), oid("C-STABLE-INTERSECTION"), oid("L-FG-NAKAYAMA"),
            )
        ],
        "documentation": [
            edge("DOC-READABLE-ROOT", oid("X-READABLE"), "documents", oid("ROOT")),
            edge("DOC-READABLE-FIXEDPOINT", oid("X-READABLE"), "documents", oid("N-FIXEDPOINT-IFF")),
            edge("DOC-READABLE-NAKAYAMA", oid("X-READABLE"), "documents", oid("L-FG-NAKAYAMA")),
            edge("DOC-SOURCE-ROOT", oid("X-SOURCE"), "documents", oid("ROOT")),
        ],
        "workflow": [
            edge("FLOW-TREE-ANCHOR", oid("ROOT"), "workflow_depends_on", oid("X-MATHLIB-BODY")),
            edge("FLOW-PROOF-TREE", oid("X-PROVENANCE"), "workflow_depends_on", oid("ROOT")),
            edge("FLOW-VALIDATION-PROOF", oid("X-TRUST"), "workflow_depends_on", oid("X-PROVENANCE")),
            edge("FLOW-RELEASE-VALIDATION", oid("X-WORKFLOW"), "workflow_depends_on", oid("X-TRUST")),
            edge("FLOW-RELEASE-READABLE", oid("X-WORKFLOW"), "workflow_depends_on", oid("X-READABLE")),
            edge("FLOW-RELEASE-SOURCE", oid("X-WORKFLOW"), "workflow_depends_on", oid("X-SOURCE")),
        ],
    }
    graphs = {}
    for name in GRAPH_NAMES:
        outgoing = {identifier: [] for identifier in ids}
        incoming = {identifier: [] for identifier in ids}
        for record in graph_edges[name]:
            outgoing[record["from"]].append(record["edge_id"])
            incoming[record["to"]].append(record["edge_id"])
        graphs[name] = {"edges": graph_edges[name], "out": outgoing, "in": incoming}

    bundle = {
        "schema_version": "stage1-typed-graphs/1.0",
        "item_id": ITEM,
        "theorem_id": THEOREM,
        "registry_id": registry["registry_id"],
        "registry_denominator_sha256": denominator,
        "root_node_id": oid("ROOT"),
        "edge_endpoint_namespace": "canonical obligation_id",
        "edge_direction": "proof_requires is parent-to-child; reciprocal composes is child-to-parent",
        "workflow_task_projection": {
            "S56-M-0030-ANCHOR_AUDIT": {"projects_to": oid("X-MATHLIB-BODY"), "depends_on": ["S56-M-0030-STATEMENT"]},
            "S56-M-0030-OBLIGATION_TREE": {"projects_to": oid("ROOT"), "depends_on": ["S56-M-0030-ANCHOR_AUDIT"]},
            "S56-M-0030-PROOF": {"projects_to": oid("X-PROVENANCE"), "depends_on": [ITEM]},
            "S56-M-0030-VALIDATION": {"projects_to": oid("X-TRUST"), "depends_on": ["S56-M-0030-PROOF"]},
            "S56-M-0030-RELEASE": {"projects_to": oid("X-WORKFLOW"), "depends_on": ["S56-M-0030-VALIDATION"]},
        },
        "nodes": nodes,
        "graphs": graphs,
        "closure_boundary": {
            "checked_interface_obligations": sorted(CHECKED_INTERFACES),
            "conditional_composition_obligations": sorted(CONDITIONAL_COMPOSITIONS),
            "accepted_closed_obligations": [],
            "root_closed": False,
            "root_machine_debt": "M3",
            "audit_complete": False,
            "theorem_complete": False,
            "remaining_root_cut_set": [
                oid("X-MATHLIB-BODY"), oid("X-SOURCE"), oid("S-FOUNDATION"),
                oid("X-PROVENANCE"), oid("X-TRUST"), oid("X-READABLE"), oid("X-WORKFLOW"),
            ],
            "composition_certificates": [
                {
                    "declaration": "Stage1Instances.THM_M_0030.ObligationTree.root_of_exactMathlibAnchor",
                    "parent": oid("ROOT"), "required_children": [oid("X-MATHLIB-BODY")],
                    "status": "conditional_kernel_checked",
                },
                {
                    "declaration": "Stage1Instances.THM_M_0030.ObligationTree.exactMathlibAnchor_of_finiteModuleIntersection",
                    "parent": oid("X-MATHLIB-BODY"), "required_children": [oid("N-FINITE-MODULE")],
                    "status": "conditional_kernel_checked",
                },
                {
                    "declaration": "Stage1Instances.THM_M_0030.ObligationTree.finiteModuleIntersection_of_jacobson",
                    "parent": oid("N-FINITE-MODULE"),
                    "required_children": [oid("N-JACOBSON"), oid("N-LOCAL-CONTAINMENT")],
                    "status": "conditional_kernel_checked",
                },
                {
                    "declaration": "Stage1Instances.THM_M_0030.ObligationTree.localProperIdealJacobson_of_bounds",
                    "parent": oid("N-LOCAL-CONTAINMENT"),
                    "required_children": [oid("L-PROPER-MAXIMAL"), oid("L-MAXIMAL-JACOBSON")],
                    "status": "conditional_kernel_checked",
                },
                {
                    "declaration": "Stage1Instances.THM_M_0030.ObligationTree.jacobsonIntersection_of_fixedPoint",
                    "parent": oid("N-JACOBSON"),
                    "required_children": [oid("N-FIXEDPOINT-IFF"), oid("L-JACOBSON-UNIT")],
                    "status": "conditional_kernel_checked",
                },
                {
                    "declaration": "Stage1Instances.THM_M_0030.ObligationTree.jacobsonUnit_of_source",
                    "parent": oid("L-JACOBSON-UNIT"),
                    "required_children": [oid("X-JACOBSON-UNIT-SOURCE")],
                    "status": "conditional_kernel_checked",
                },
                {
                    "declaration": "Stage1Instances.THM_M_0030.ObligationTree.fixedPointCharacterization_of_branches",
                    "parent": oid("T-FIXEDPOINT-COMPOSE"),
                    "required_children": [oid("B-FIXEDPOINT-FORWARD"), oid("B-FIXEDPOINT-BACKWARD")],
                    "status": "conditional_kernel_checked",
                },
            ],
            "reason": "All compositions are conditional and accepted state is empty. The pinned terminal theorem remains uninstalled until proof-phase validation and master acceptance.",
        },
    }

    declaration_by_id = {
        oid("ROOT"): ["Stage1Instances.THM_M_0030.ObligationTree.root_of_exactMathlibAnchor"],
        oid("X-MATHLIB-BODY"): [
            "Ideal.iInf_pow_eq_bot_of_isLocalRing",
            "Stage1Instances.THM_M_0030.ObligationTree.exactMathlibAnchor_of_finiteModuleIntersection",
        ],
        oid("N-FINITE-MODULE"): [
            "Ideal.iInf_pow_smul_eq_bot_of_isLocalRing",
            "Stage1Instances.THM_M_0030.ObligationTree.finiteModuleIntersection_of_jacobson",
        ],
        oid("N-JACOBSON"): [
            "Ideal.iInf_pow_smul_eq_bot_of_le_jacobson",
            "Stage1Instances.THM_M_0030.ObligationTree.jacobsonIntersection_of_fixedPoint",
        ],
        oid("N-LOCAL-CONTAINMENT"): [
            "Stage1Instances.THM_M_0030.ObligationTree.localProperIdealJacobson_of_bounds"
        ],
        oid("L-JACOBSON-UNIT"): [
            "Stage1Instances.THM_M_0030.ObligationTree.jacobsonUnit_of_source"
        ],
        oid("N-FIXEDPOINT-IFF"): ["Ideal.mem_iInf_smul_pow_eq_bot_iff"],
        oid("T-FIXEDPOINT-COMPOSE"): [
            "Stage1Instances.THM_M_0030.ObligationTree.fixedPointCharacterization_of_branches"
        ],
        oid("L-FG-NAKAYAMA"): ["Submodule.exists_mem_and_smul_eq_self_of_fg_of_le_smul"],
    }
    recipes = {
        "schema_version": "stage1-validation-specs/1.0",
        "item_id": ITEM,
        "theorem_id": THEOREM,
        "recipes": [
            {
                "recipe_id": f"VAL-{identifier}",
                "cwd": ".",
                "argv": ["python3", "-B", f"Stage1_Instances/{THEOREM}/check_obligation_tree.py"],
                "env_allowlist": {},
                "timeout_seconds": 180,
                "network_policy": "denied",
                "expected_exit": 0,
                "expected_outputs": [{
                    "path_or_stream": "stdout",
                    "semantic_hash_policy": "contains PASS THM-M-0030 obligation tree",
                }],
                "covered_obligation_ids": [identifier],
                "covered_declarations": declaration_by_id.get(identifier, []),
                "coverage_semantics": "architecture_validation_only",
                "closure_credit": False,
            }
            for identifier in ids
        ],
    }
    return registry, bundle, recipes


def main() -> None:
    outputs = build()
    for name, value in zip(
        ("obligation-registry.json", "typed-graphs.json", "validation-specs.json"), outputs
    ):
        (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    registry, bundle, _ = outputs
    edge_count = sum(len(graph["edges"]) for graph in bundle["graphs"].values())
    print(f"generated {len(registry['obligations'])} obligations and {edge_count} typed edges")
    print(f"registry denominator sha256: {registry['denominator_sha256']}")


if __name__ == "__main__":
    main()
