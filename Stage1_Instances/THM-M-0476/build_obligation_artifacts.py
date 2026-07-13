#!/usr/bin/env python3
"""Build or check the frozen THM-M-0476 obligation registry and typed graphs."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ITEM = "S56-M-0476-OBLIGATION_TREE"
THEOREM = "THM-M-0476"
PREFIX = "M0476"
ROOT_EXPRESSION = "ee76edb160426d3e8d95b11bfedca7febcfe915f50007e042875c922ebc8a4ac"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
WILSON_BLOB = "9401f7b96b43c2c0afa1f823857bd31a20ae0ac2"
FINITE_BASIC_BLOB = "fb3668d594f865e52f20c8af45e91e7e3b1eebd8"
TASK_SUFFIXES = (
    "INTAKE", "STATEMENT", "ANCHOR_AUDIT", "OBLIGATION_TREE", "PROOF",
    "VALIDATION", "RELEASE",
)


def digest(value: object) -> str:
    encoded = json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=True
    ).encode()
    return hashlib.sha256(encoded).hexdigest()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def oid(short: str) -> str:
    return f"{PREFIX}-{short}"


REGISTRY_KIND = {
    "root": "root", "definition": "definition", "normalization": "reduction",
    "reduction": "reduction", "branch": "branch", "construction": "construction",
    "bridge": "lemma", "core_lemma": "lemma", "computation": "computation",
    "certificate": "terminal", "transport": "transport", "terminal": "terminal",
}


# Status is intentionally absent from this pre-status architecture table. The rows follow the
# exact target and every material step visible in the two pinned terminal source bodies.
ROWS = (
    (
        "ROOT", "root", "critical",
        "Prove the exact forward Wilson factorial congruence frozen in Statement.lean.",
        "Stage1Instances.THM_M_0476.WilsonTheoremTarget",
        "For every natural prime p, ((p - 1)! : ZMod p) = -1.",
        "required", "required", None, 20,
        ["Statement.lean; expression sha256 " + ROOT_EXPRESSION],
    ),
    (
        "S-INTERFACE", "definition", "high",
        "Preserve the natural modulus, explicit primality premise, factorial cast, ZMod equality, and forward direction.",
        "Stage1Instances.THM_M_0476.WilsonTheoremTarget",
        "The exact canonical interface without a strengthened, weakened, or substituted theorem.",
        "required", "not_applicable", None, 18,
        ["Statement.lean: WilsonTheoremTarget"],
    ),
    (
        "S-BOUNDARY", "branch", "high",
        "Retain p = 2 and exclude zero, one, and composite moduli only through p.Prime.",
        "the boundary policy of Stage1Instances.THM_M_0476.WilsonTheoremTarget",
        "An exhaustive degenerate-case policy for the canonical quantifier.",
        "required", "required", None, 18,
        ["statement.json: boundary_and_degenerate_cases"],
    ),
    (
        "S-FACT-TRANSPORT", "transport", "high",
        "Convert the explicit hp : p.Prime premise to the exact Fact-premise interface.",
        "Stage1Instances.THM_M_0476.ObligationTree.root_of_factWilsonAnchor",
        "The exact canonical root from FactWilsonAnchor without an added premise.",
        "required", "not_applicable",
        "local:Stage1_Instances/THM-M-0476/ObligationTree.lean#root_of_factWilsonAnchor", 12,
        ["ObligationTree.lean: root_of_factWilsonAnchor"],
    ),
    (
        "S-FOUNDATION", "certificate", "critical",
        "Audit propext, classical choice, quotient soundness, the kernel, imports, and the no-oracle policy.",
        "planned transitive foundation, TCB, and computation report",
        "An accepted foundation and trust boundary.",
        "required", "not_applicable", None, 28,
        ["ObligationTree.lean: #print axioms", "anchor-audit.json: immutable_environment"],
    ),
    (
        "T-COMPOSE", "terminal", "high",
        "Compose the factorial, residue-unit, and unit-product bridges into the exact Fact-premise anchor.",
        "Stage1Instances.THM_M_0476.ObligationTree.factWilsonAnchor_of_bridges",
        "FactWilsonAnchor, conditional on all three material bridges.",
        "required", "required",
        "local:Stage1_Instances/THM-M-0476/ObligationTree.lean#factWilsonAnchor_of_bridges", 20,
        ["ObligationTree.lean: factWilsonAnchor_of_bridges"],
    ),
    (
        "L-WILSON", "bridge", "critical",
        "Expose the exact pinned Wilson body rather than treating its short invocation as a primitive.",
        "ZMod.wilsons_lemma",
        "FactWilsonAnchor and the exact three-stage factorial-to-units proof route.",
        "required", "required", f"git-blob:{WILSON_BLOB}:ZMod.wilsons_lemma", 28,
        ["Mathlib/NumberTheory/Wilson.lean:43-68"],
    ),
    (
        "N-FACTORIAL-PRODUCT", "normalization", "high",
        "Rewrite the factorial as the cast of the natural interval product.",
        "Stage1Instances.THM_M_0476.ObligationTree.factorialProduct_of_identities",
        "FactorialProductBridge.",
        "required", "required",
        "local:Stage1_Instances/THM-M-0476/ObligationTree.lean#factorialProduct_of_identities", 18,
        ["Wilson.lean:46-47"],
    ),
    (
        "L-FACTORIAL-INTERVAL", "core_lemma", "high",
        "Prove the primitive product of natural numbers from one through n is n factorial.",
        "Finset.prod_Ico_id_eq_factorial",
        "FactorialIntervalIdentity.",
        "required", "required",
        f"pinned-mathlib:{MATHLIB_REVISION}#Finset.prod_Ico_id_eq_factorial", 24,
        ["Mathlib/Algebra/BigOperators/Intervals.lean:168-172"],
    ),
    (
        "T-NAT-CAST-PRODUCT", "transport", "normal",
        "Commute the natural cast into ZMod p with the finite product.",
        "Finset.prod_natCast",
        "NatIntervalCastIdentity.",
        "required", "required",
        f"pinned-mathlib:{MATHLIB_REVISION}#Finset.prod_natCast", 12,
        ["Mathlib/Algebra/BigOperators/Ring/Finset.lean:247-248"],
    ),
    (
        "N-PRIME-ENDPOINT", "normalization", "high",
        "Use primality to prove p > 0 and identify succ (p - 1) with the intended interval endpoint.",
        "Stage1Instances.THM_M_0476.ObligationTree.primeEndpointIdentity_from_prime",
        "PrimeEndpointIdentity: (p - 1) + 1 = p for every prime p.",
        "required", "required", None, 20,
        ["Wilson.lean:52-57,63", "ObligationTree.lean: primeEndpointIdentity_from_prime"],
    ),
    (
        "C-RESIDUE-UNITS-BIJECTION", "construction", "critical",
        "Bijection the canonical nonzero representatives with every unit and preserve the product value.",
        "Stage1Instances.THM_M_0476.ObligationTree.residueUnitsProduct_of_components",
        "ResidueUnitsProductBridge.",
        "required", "required",
        "local:Stage1_Instances/THM-M-0476/ObligationTree.lean#residueUnitsProduct_of_components", 26,
        ["Wilson.lean:53-68", "Finset.prod_bij"],
    ),
    (
        "B-UNIT-VAL-RANGE", "branch", "high",
        "Show each unit value is positive and below p, hence lies in the exact interval.",
        "Stage1Instances.THM_M_0476.ObligationTree.unitRepresentativeInPrimeRange_from_unit",
        "Every unit value satisfies 1 <= val and val < p.",
        "required", "required", None, 22,
        ["Wilson.lean:55-60"],
    ),
    (
        "L-UNIT-VAL-INJECTIVE", "core_lemma", "high",
        "Recover equality of units from equality of their ZMod values.",
        "Stage1Instances.THM_M_0476.ObligationTree.unitRepresentativeInjective_from_val",
        "Injectivity of the representative map.",
        "required", "required", None, 14,
        ["Wilson.lean:61"],
    ),
    (
        "C-RESIDUE-TO-UNIT", "construction", "critical",
        "Turn each interval representative into a nonzero ZMod element and construct Units.mk0.",
        "Stage1Instances.THM_M_0476.ObligationTree.residueRepresentativeSurjectiveAtEndpoint_from_mk0",
        "Every b with 1 <= b and b < p is the value of a unit.",
        "required", "required", None, 26,
        ["Wilson.lean:62-67"],
    ),
    (
        "T-REPRESENTATIVE-COE", "transport", "high",
        "Identify the cast of a unit's canonical value with the unit's underlying ZMod element.",
        "Stage1Instances.THM_M_0476.ObligationTree.representativeCastAgreement_from_natCast_val",
        "Product-value preservation for the representative bijection.",
        "required", "required", None, 12,
        ["Wilson.lean:68"],
    ),
    (
        "L-UNITS-PRODUCT", "bridge", "critical",
        "Prove that the product of all units of the finite domain ZMod p is negative one.",
        "FiniteField.prod_univ_units_id_eq_neg_one",
        "UnitProductIdentity.",
        "required", "required",
        f"git-blob:{FINITE_BASIC_BLOB}:FiniteField.prod_univ_units_id_eq_neg_one", 22,
        ["Mathlib/FieldTheory/Finite/Basic.lean:110-117"],
    ),
    (
        "C-INVERSE-PAIRING", "construction", "critical",
        "Pair every unit except negative one with its inverse and cancel every nonfixed pair.",
        "Stage1Instances.THM_M_0476.ObligationTree.unitEraseProduct_of_inversion; Finset.prod_involution",
        "UnitEraseNegOneProduct.",
        "required", "required",
        "local:Stage1_Instances/THM-M-0476/ObligationTree.lean#unitEraseProduct_of_inversion", 30,
        ["Finite.Basic.lean:112-116", "Finset/Basic.lean:665-682"],
    ),
    (
        "L-INVERSE-FIXED-POINTS", "core_lemma", "critical",
        "Classify inverse-fixed units as one or negative one, then use erasure and the non-one premise.",
        "Stage1Instances.THM_M_0476.ObligationTree.inverseFixedPointClassification_from_units",
        "Every remaining inverse fixed point is one and is excluded by prod_involution's premise.",
        "required", "required",
        f"pinned-mathlib:{MATHLIB_REVISION}#Units.inv_eq_self_iff", 22,
        ["Finite.Basic.lean:115", "Mathlib/Algebra/Ring/Commute.lean:239-245"],
    ),
    (
        "T-INSERT-NEGONE", "transport", "high",
        "Insert negative one back into the erased product and simplify the paired remainder to one.",
        "Stage1Instances.THM_M_0476.ObligationTree.unitProductIdentity_of_erase",
        "UnitProductIdentity.",
        "required", "required",
        "local:Stage1_Instances/THM-M-0476/ObligationTree.lean#unitProductIdentity_of_erase", 12,
        ["Finite.Basic.lean:113,117"],
    ),
    (
        "T-UNITS-COE-NEGONE", "transport", "high",
        "Map the unit-valued product identity into ZMod p and preserve negative one.",
        "Stage1Instances.THM_M_0476.ObligationTree.unitsProductBridge_of_components",
        "UnitsProductBridge.",
        "required", "required",
        "local:Stage1_Instances/THM-M-0476/ObligationTree.lean#unitsProductBridge_of_components", 18,
        ["Wilson.lean:49-51", "Units.coeHom", "Finset.map_prod"],
    ),
    (
        "X-SOURCE", "terminal", "critical",
        "Map every material premise and transition to a reviewed primary source with assumptions and errata.",
        "node-specific primary-source crosswalk pending",
        "Human-source evidence without machine proof credit.",
        "not_applicable", "required", None, 60,
        ["source-statement-crosswalk.md; pinpoint primary source remains open"],
    ),
    (
        "X-PROVENANCE", "certificate", "critical",
        "Bind wrappers, terminal bodies, transitive declarations, source hashes, pins, licenses, and replay evidence.",
        "planned machine-derived provenance closure",
        "Release provenance without mathematical proof credit.",
        "informational", "not_applicable", None, 50,
        ["anchor-audit.json: M0476-C01 and M0476-C03"],
    ),
    (
        "X-TRUST", "certificate", "critical",
        "Audit the transitive Lean/mathlib closure, executable TCB, axioms, unsafe boundaries, and replay.",
        "planned trust and TCB closure",
        "Release trust evidence without mathematical proof credit.",
        "informational", "not_applicable", None, 50,
        ["anchor-audit.json: machine_axioms", "ObligationTree.lean: #print axioms"],
    ),
    (
        "X-READABLE", "terminal", "high",
        "Produce and independently review a complete node-specific reconstruction of the frozen route.",
        "planned readable proof outline and process",
        "Readable coverage without machine proof credit.",
        "not_applicable", "required", None, 60,
        ["obligation-tree.md: architecture only; independent review pending"],
    ),
    (
        "X-WORKFLOW", "certificate", "high",
        "Bind proof, validation, release, freshness, revocation, and independent-verification acceptance.",
        "planned Stage1 workflow receipts",
        "Workflow acceptance without mathematical proof credit.",
        "informational", "not_applicable", None, 30,
        ["Docs/Stage1_Execution_DAG_rev-5.6.json"],
    ),
)


REQUIRES = {
    oid("ROOT"): [oid("S-FACT-TRANSPORT")],
    oid("S-FACT-TRANSPORT"): [oid("T-COMPOSE")],
    oid("T-COMPOSE"): [
        oid("N-FACTORIAL-PRODUCT"),
        oid("C-RESIDUE-UNITS-BIJECTION"), oid("T-UNITS-COE-NEGONE"),
    ],
    oid("N-FACTORIAL-PRODUCT"): [
        oid("L-FACTORIAL-INTERVAL"), oid("T-NAT-CAST-PRODUCT"),
    ],
    oid("C-RESIDUE-UNITS-BIJECTION"): [
        oid("N-PRIME-ENDPOINT"), oid("B-UNIT-VAL-RANGE"), oid("L-UNIT-VAL-INJECTIVE"),
        oid("C-RESIDUE-TO-UNIT"), oid("T-REPRESENTATIVE-COE"),
    ],
    oid("C-INVERSE-PAIRING"): [oid("L-INVERSE-FIXED-POINTS")],
    oid("T-INSERT-NEGONE"): [oid("C-INVERSE-PAIRING")],
    oid("T-UNITS-COE-NEGONE"): [oid("T-INSERT-NEGONE")],
}

PROOF_LEAVES = [
    oid("L-FACTORIAL-INTERVAL"), oid("T-NAT-CAST-PRODUCT"),
    oid("N-PRIME-ENDPOINT"), oid("B-UNIT-VAL-RANGE"),
    oid("L-UNIT-VAL-INJECTIVE"), oid("C-RESIDUE-TO-UNIT"),
    oid("T-REPRESENTATIVE-COE"), oid("L-INVERSE-FIXED-POINTS"),
]

TASK_OBLIGATION_LINKS = {
    "INTAKE": [oid("S-INTERFACE"), oid("S-BOUNDARY")],
    "STATEMENT": [oid("ROOT"), oid("S-INTERFACE"), oid("S-FACT-TRANSPORT")],
    "ANCHOR_AUDIT": [oid("L-WILSON"), oid("L-UNITS-PRODUCT"), oid("X-PROVENANCE")],
    "VALIDATION": [oid("S-FOUNDATION"), oid("X-PROVENANCE"), oid("X-TRUST")],
    "RELEASE": [oid("ROOT"), oid("X-SOURCE"), oid("X-PROVENANCE"), oid("X-TRUST"), oid("X-READABLE"), oid("X-WORKFLOW")],
}

# These non-crediting links expose source-body structure in the provenance graph as well as the
# exact proof graph. Proof credit remains empty until proof-phase evidence is accepted.
PROVENANCE_EXPANSIONS = {
    oid("L-WILSON"): [
        oid("N-FACTORIAL-PRODUCT"), oid("N-PRIME-ENDPOINT"),
        oid("C-RESIDUE-UNITS-BIJECTION"), oid("L-UNITS-PRODUCT"),
        oid("T-UNITS-COE-NEGONE"),
    ],
    oid("L-UNITS-PRODUCT"): [oid("C-INVERSE-PAIRING"), oid("T-INSERT-NEGONE")],
}


CHECKED_INTERFACES = {
    oid("ROOT"), oid("S-FACT-TRANSPORT"), oid("T-COMPOSE"),
    oid("N-PRIME-ENDPOINT"),
    oid("N-FACTORIAL-PRODUCT"), oid("C-RESIDUE-UNITS-BIJECTION"),
    oid("C-INVERSE-PAIRING"), oid("T-INSERT-NEGONE"),
    oid("T-UNITS-COE-NEGONE"),
}

LOCAL_DECLARATIONS = {
    oid("ROOT"): "Stage1Instances.THM_M_0476.ObligationTree.root_of_composedTarget",
    oid("S-FACT-TRANSPORT"): "Stage1Instances.THM_M_0476.ObligationTree.root_of_factWilsonAnchor",
    oid("T-COMPOSE"): "Stage1Instances.THM_M_0476.ObligationTree.factWilsonAnchor_of_bridges",
    oid("N-FACTORIAL-PRODUCT"): "Stage1Instances.THM_M_0476.ObligationTree.factorialProduct_of_identities",
    oid("C-RESIDUE-UNITS-BIJECTION"): "Stage1Instances.THM_M_0476.ObligationTree.residueUnitsProduct_of_components",
    oid("N-PRIME-ENDPOINT"): "Stage1Instances.THM_M_0476.ObligationTree.primeEndpointIdentity_from_prime",
    oid("C-INVERSE-PAIRING"): "Stage1Instances.THM_M_0476.ObligationTree.unitEraseProduct_of_inversion",
    oid("T-INSERT-NEGONE"): "Stage1Instances.THM_M_0476.ObligationTree.unitProductIdentity_of_erase",
    oid("T-UNITS-COE-NEGONE"): "Stage1Instances.THM_M_0476.ObligationTree.unitsProductBridge_of_components",
}

LEAF_DECLARATIONS = {
    oid("B-UNIT-VAL-RANGE"): "Stage1Instances.THM_M_0476.ObligationTree.unitRepresentativeInPrimeRange_from_unit",
    oid("L-UNIT-VAL-INJECTIVE"): "Stage1Instances.THM_M_0476.ObligationTree.unitRepresentativeInjective_from_val",
    oid("C-RESIDUE-TO-UNIT"): "Stage1Instances.THM_M_0476.ObligationTree.residueRepresentativeSurjectiveAtEndpoint_from_mk0",
    oid("T-REPRESENTATIVE-COE"): "Stage1Instances.THM_M_0476.ObligationTree.representativeCastAgreement_from_natCast_val",
    oid("L-INVERSE-FIXED-POINTS"): "Stage1Instances.THM_M_0476.ObligationTree.inverseFixedPointClassification_from_units",
}

SOURCE_NA = {
    oid("S-INTERFACE"), oid("S-FACT-TRANSPORT"), oid("S-FOUNDATION"),
    oid("X-PROVENANCE"), oid("X-TRUST"), oid("X-WORKFLOW"),
}

EXCLUSIONS = {
    oid("S-INTERFACE"): "formal_interface_source_coverage_inherited_from_root_pending_reviewer_acceptance",
    oid("S-FACT-TRANSPORT"): "formal_encoding_transport_source_coverage_inherited_from_root_pending_reviewer_acceptance",
    oid("S-FOUNDATION"): "formal_trust_boundary_not_a_human_mathematical_claim_pending_reviewer_acceptance",
    oid("X-SOURCE"): "human_source_boundary_only_pending_independent_source_review",
    oid("X-PROVENANCE"): "release_provenance_overlay_no_proof_credit_pending_integration_review",
    oid("X-TRUST"): "release_trust_overlay_no_proof_credit_pending_integration_review",
    oid("X-READABLE"): "readability_boundary_only_pending_independent_review",
    oid("X-WORKFLOW"): "workflow_overlay_no_proof_credit_pending_integration_review",
}


def task_contract_projection() -> list[dict]:
    """Freeze the seven immutable THM-M-0476 task contracts, never mutable cursor fields."""
    execution = json.loads(
        (ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json").read_text(encoding="utf-8")
    )
    fields = (
        "id", "theorem_id", "execution_rank", "phase", "layer", "depends_on",
        "owned_paths", "deliverable", "completion_gate", "children",
    )
    rows = [row for row in execution["items"] if row["theorem_id"] == THEOREM]
    assert [row["id"].rsplit("-", 1)[-1] for row in rows] == list(TASK_SUFFIXES)
    return [{field: row[field] for field in fields} for row in rows]


def semantic_steps(identifier: str, children: list[str], parents: list[str],
                   formal: str, output: str) -> list[dict]:
    use = parents or [f"{identifier}-PUBLIC-BOUNDARY"]
    step = lambda number, premises, inference, claim, outgoing: {
        "step_id": f"{identifier}-STEP-{number:02d}",
        "premise_ids": premises,
        "inference_or_source": inference,
        "output_claim": claim,
        "outgoing_use_ids": outgoing,
    }
    recipes: dict[str, list[tuple[list[str], str, str]]] = {
        oid("ROOT"): [
            ([oid("S-FACT-TRANSPORT")], "root_of_composedTarget after the exact explicit-prime transport", output),
        ],
        oid("S-INTERFACE"): [
            ([oid("ROOT")], "Statement.lean expression fingerprint: preserve p : Nat followed by hp : p.Prime", "the exact ordered binder and natural-modulus context"),
            ([], "preserve factorial (p - 1), its cast to ZMod p, equality, and the forward direction", output),
        ],
        oid("S-BOUNDARY"): [
            ([oid("ROOT")], "Nat.Prime excludes 0, 1, and composites while retaining the prime 2", output),
        ],
        oid("S-FACT-TRANSPORT"): [
            ([oid("T-COMPOSE")], "root_of_factWilsonAnchor installs Fact p.Prime from hp : p.Prime", output),
        ],
        oid("S-FOUNDATION"): [
            ([oid("ROOT")], "#print axioms over every conditional composition declaration", "the observed declaration axiom sets"),
            ([], "compare the observed sets with the pending foundation and TCB profiles", output),
        ],
        oid("L-WILSON"): [
            ([oid("T-COMPOSE")], "anchor-audit pins ZMod.wilsons_lemma while provenance maps its visible source route; no local composition certificate or proof credit", output),
        ],
        oid("T-COMPOSE"): [
            ([oid("N-FACTORIAL-PRODUCT"), oid("C-RESIDUE-UNITS-BIJECTION"), oid("T-UNITS-COE-NEGONE")], "factWilsonAnchor_of_bridges chains the three equalities", output),
        ],
        oid("N-FACTORIAL-PRODUCT"): [
            ([oid("L-FACTORIAL-INTERVAL"), oid("T-NAT-CAST-PRODUCT")], "factorialProduct_of_identities rewrites the natural factorial then commutes the cast with the product", output),
        ],
    oid("L-FACTORIAL-INTERVAL"): [
            ([oid("S-INTERFACE")], "Finset.prod_Ico_id_eq_factorial at pinned mathlib revision " + MATHLIB_REVISION, output),
        ],
        oid("T-NAT-CAST-PRODUCT"): [
            ([oid("S-INTERFACE")], "Finset.prod_natCast maps the natural interval product into ZMod p", output),
        ],
        oid("N-PRIME-ENDPOINT"): [
            ([oid("S-INTERFACE")], "primeEndpointIdentity_from_prime derives 1 <= p from Fact.out.ne_zero and applies Nat.sub_add_cancel", output),
        ],
        oid("C-RESIDUE-UNITS-BIJECTION"): [
            ([oid("N-PRIME-ENDPOINT"), oid("B-UNIT-VAL-RANGE"), oid("L-UNIT-VAL-INJECTIVE"), oid("C-RESIDUE-TO-UNIT"), oid("T-REPRESENTATIVE-COE")], "residueUnitsProduct_of_components rewrites the endpoint and applies Finset.prod_bij", output),
        ],
        oid("B-UNIT-VAL-RANGE"): [
            ([oid("S-INTERFACE")], "Units.ne_zero and ZMod.val_zero give positivity; ZMod.val_lt gives the strict upper bound", output),
        ],
        oid("L-UNIT-VAL-INJECTIVE"): [
            ([oid("S-INTERFACE")], "Units.ext_iff followed by ZMod.val_injective", output),
        ],
        oid("C-RESIDUE-TO-UNIT"): [
            ([oid("S-INTERFACE")], "the lower bound proves nonzero, Units.mk0 constructs the unit, and ZMod.val_cast_of_lt fixes its value", output),
        ],
        oid("T-REPRESENTATIVE-COE"): [
            ([oid("S-INTERFACE")], "ZMod.natCast_val identifies the cast representative with the underlying residue", output),
        ],
        oid("L-UNITS-PRODUCT"): [
            ([oid("T-INSERT-NEGONE")], "anchor-audit pins FiniteField.prod_univ_units_id_eq_neg_one while provenance maps its visible source route; no local composition certificate or proof credit", output),
        ],
        oid("C-INVERSE-PAIRING"): [
            ([oid("L-INVERSE-FIXED-POINTS")], "unitEraseProduct_of_inversion supplies group inverse laws locally and uses Finset.prod_involution", output),
        ],
        oid("L-INVERSE-FIXED-POINTS"): [
            ([oid("S-INTERFACE")], "Units.inv_eq_self_iff in the pinned integral-domain unit group", output),
        ],
        oid("T-INSERT-NEGONE"): [
            ([oid("C-INVERSE-PAIRING")], "unitProductIdentity_of_erase inserts -1 into univ.erase (-1), rewrites the erased product to one, and simplifies", output),
        ],
        oid("T-UNITS-COE-NEGONE"): [
            ([oid("T-INSERT-NEGONE")], "unitsProductBridge_of_components maps the locally reconstructed unit product through Units.coeHom and simplifies the value of -1", output),
        ],
        oid("X-SOURCE"): [
            ([oid("ROOT")], "source-statement-crosswalk.md identifies the catalog claim; pinpoint primary-source premise and transition maps remain open", output),
        ],
        oid("X-PROVENANCE"): [
            ([oid("L-WILSON"), oid("L-UNITS-PRODUCT")], "anchor-audit.json binds the two terminal candidates to immutable revisions and body blobs", output),
        ],
        oid("X-TRUST"): [
            ([oid("S-FOUNDATION")], "bind source hashes, observed axioms, dependency pins, and no-oracle policy without granting proof credit", output),
        ],
        oid("X-READABLE"): [
            ([oid("ROOT")], "obligation-tree.md publishes every stable node boundary and the complete planned route", output),
        ],
        oid("X-WORKFLOW"): [
            ([oid("ROOT")], "the static seven-task contract projection orders intake through release and links each task to obligations", output),
        ],
    }
    entries = recipes[identifier]
    built = []
    for index, (premises, inference, claim) in enumerate(entries, 1):
        if not premises:
            premises = [built[-1]["step_id"]]
        outgoing = [f"{identifier}-STEP-{index + 1:02d}"] if index < len(entries) else use
        built.append(step(index, premises, inference or formal, claim, outgoing))
    return built


def compute_registry_hash(registry: dict) -> str:
    return digest({field: registry[field] for field in registry["registry_hash_fields"]})


def build() -> tuple[dict, dict, dict]:
    obligations: list[dict] = []
    nodes: list[dict] = []
    parent_map: dict[str, list[str]] = {}
    for parent, children in REQUIRES.items():
        for child in children:
            parent_map.setdefault(child, []).append(parent)
    for short, kind, risk, claim, formal, output, machine, human, body, budget, anchors in ROWS:
        identifier = oid(short)
        if identifier == oid("N-PRIME-ENDPOINT"):
            body = "local:Stage1_Instances/THM-M-0476/ObligationTree.lean#primeEndpointIdentity_from_prime"
        elif identifier in LEAF_DECLARATIONS:
            body = (
                "local:Stage1_Instances/THM-M-0476/ObligationTree.lean#"
                + LEAF_DECLARATIONS[identifier].rsplit(".", 1)[-1]
            )
        fingerprint = (
            f"lean-expression-sha256:{ROOT_EXPRESSION}"
            if identifier in {oid("ROOT"), oid("S-INTERFACE")} else
            "planned:v1:sha256:" + digest([identifier, kind, claim, formal, output])
        )
        obligations.append({
            "obligation_id": identifier,
            "statement_fingerprint": fingerprint,
            "kind": REGISTRY_KIND[kind],
            "root_relevant": True,
            "machine_eligibility": machine,
            "human_source_eligibility": human,
            "readable_eligibility": "required",
            "risk_class": risk,
            "exclusion_reason": EXCLUSIONS.get(identifier),
            "terminal_proof_body_id": body,
        })
        if machine == "required":
            machine_debt = "M3"
        else:
            machine_debt = "M4"
        if identifier == oid("L-WILSON"):
            provenance = "anchor-audit:M0476-C01-MATHLIB-DIRECT"
        elif identifier == oid("L-UNITS-PRODUCT"):
            provenance = "anchor-audit:M0476-C03-MATHLIB-SUPPORT"
        elif body and body.startswith("pinned-mathlib"):
            provenance = "pinned-visible-terminal-chain"
        elif identifier in LOCAL_DECLARATIONS:
            provenance = "local-conditional-composition"
        else:
            provenance = "none"
        owned_sources = []
        if identifier in LOCAL_DECLARATIONS | LEAF_DECLARATIONS:
            owned_sources = ["Stage1_Instances/THM-M-0476/ObligationTree.lean"]
        elif identifier == oid("S-INTERFACE"):
            owned_sources = ["Stage1_Instances/THM-M-0476/Statement.lean"]
        nodes.append({
            "node_id": f"{THEOREM}-{short}",
            "obligation_id": identifier,
            "kind": kind,
            "human_statement": claim,
            "formal_target": formal,
            "output": output,
            "human_debt": "H1",
            "machine_debt": machine_debt,
            "readability_debt": "R4",
            "evidence_ids": [],
            "source_crosswalk_id": (
                "not-applicable-pending-review" if identifier in SOURCE_NA
                else "primary-source-node-map-pending"
            ),
            "provenance_id": provenance,
            "foundation_profile": "lean4-dependent-type-theory; accepted axiom policy and transitive review pending",
            "tcb_profile": "lean-4.29.0+mathlib-8a178386; transitive closure and independent replay pending",
            "computation_record": "none; no native computation, solver, oracle, experiment, or unchecked certificate is credited",
            "step_budget": budget,
            "step_budget_semantics": "split_threshold_only_not_readability_or_leaf_adequacy",
            "semantic_step_ledger": {
                "premises": [
                    premise
                    for step_record in semantic_steps(
                        identifier, REQUIRES.get(identifier, []),
                        parent_map.get(identifier, []), formal, output,
                    )
                    for premise in step_record["premise_ids"]
                ],
                "inference": claim,
                "source_anchors": anchors,
                "output": output,
                "outgoing_use": parent_map.get(identifier, [f"{identifier}-PUBLIC-BOUNDARY"]),
                "steps": semantic_steps(
                    identifier, REQUIRES.get(identifier, []),
                    parent_map.get(identifier, []), formal, output,
                ),
            },
            "public_readable_target": f"Stage1_Instances/THM-M-0476/obligation-tree.md#{identifier.lower()}",
            "validation_spec_id": (
                "S56-M-0476-OBLIGATION-TREE-LEAN"
                if identifier in CHECKED_INTERFACES | set(LEAF_DECLARATIONS)
                else "S56-M-0476-OBLIGATION-TREE-STRUCTURE"
            ),
            "status_boundary": "Frozen architecture, audited candidate, or conditional interface only; no accepted root proof or theorem completion.",
            "task_ids": [ITEM, "S56-M-0476-PROOF"],
            "owned_sources": owned_sources,
            "owner": "THM-M-0476 proof lane",
            "reviewer": "independent Stage1 integration lane",
            "validity": {
                "validated_at": "2026-07-13" if identifier in CHECKED_INTERFACES | set(LEAF_DECLARATIONS) else None,
                "review_due": "before proof acceptance",
                "invalidation_inputs": [
                    "Statement.lean", "anchor-audit.json", "obligation-registry.json",
                    "typed-graphs.json", "toolchain and dependency pins",
                ],
                "revocation_state": "provisional" if identifier in CHECKED_INTERFACES | set(LEAF_DECLARATIONS) else "open",
            },
        })

    fields = (
        "obligation_id", "statement_fingerprint", "kind", "root_relevant",
        "machine_eligibility", "human_source_eligibility", "readable_eligibility",
        "risk_class", "exclusion_reason", "terminal_proof_body_id",
    )
    denominator = digest([{field: row[field] for field in fields} for row in obligations])
    ids = [row["obligation_id"] for row in obligations]
    task_links = {
        f"S56-M-0476-{suffix}": targets
        for suffix, targets in {
            **TASK_OBLIGATION_LINKS,
            "OBLIGATION_TREE": ids,
            "PROOF": [
                identifier for identifier in ids
                if identifier not in {oid("X-SOURCE"), oid("X-READABLE"), oid("X-WORKFLOW")}
            ],
        }.items()
    }
    for node in nodes:
        node["task_ids"] = [
            task_id for task_id, linked_ids in task_links.items()
            if node["obligation_id"] in linked_ids
        ]

    registry = {
        "schema_version": "stage1-obligation-registry/1.0",
        "item_id": ITEM,
        "theorem_id": THEOREM,
        "registry_id": "THM-M-0476-OBLIGATIONS-v1",
        "registry_version": 1,
        "frozen_at": "2026-07-13T00:00:00+08:00",
        "freeze_basis": "The exact elaborated statement and every visible semantic step in the pinned Wilson and units-product bodies. Eligibility and denominators are assigned without proof-closure credit.",
        "frozen_against_statement_sha256": sha256(HERE / "Statement.lean"),
        "frozen_against_anchor_audit_sha256": sha256(HERE / "anchor-audit.json"),
        "frozen_task_contract_projection": task_contract_projection(),
        "frozen_task_contract_sha256": digest(task_contract_projection()),
        "root_obligation_id": oid("ROOT"),
        "denominator_sha256": denominator,
        "frozen_denominators": {
            "inventory": ids,
            "required_machine": [row["obligation_id"] for row in obligations if row["machine_eligibility"] == "required"],
            "required_human_source": [row["obligation_id"] for row in obligations if row["human_source_eligibility"] == "required"],
            "required_readable": ids,
            "informational_overlays": [row["obligation_id"] for row in obligations if row["machine_eligibility"] == "informational"],
        },
        "layer_assessment": {
            "S_statement_foundation": {"state": "required", "obligation_ids": [identifier for identifier in ids if "-S-" in identifier]},
            "N_normalization": {"state": "required", "obligation_ids": [identifier for identifier in ids if "-N-" in identifier]},
            "B_branch": {"state": "required", "obligation_ids": [oid("S-BOUNDARY"), oid("B-UNIT-VAL-RANGE")]},
            "C_construction": {"state": "required", "obligation_ids": [identifier for identifier in ids if "-C-" in identifier]},
            "L_core_lemma": {"state": "required", "obligation_ids": [identifier for identifier in ids if "-L-" in identifier]},
            "X_external_computation": {
                "state": "external_boundaries_required_computation_not_applicable_pending_independent_approval",
                "reason": "Pinned imported bodies and trust are material; no finite computation, automation, oracle, experiment, or certificate closes any mathematical node.",
                "obligation_ids": [identifier for identifier in ids if "-X-" in identifier],
                "reviewer": "unassigned independent Lean/TCB reviewer",
            },
            "T_terminal": {"state": "required", "obligation_ids": [identifier for identifier in ids if "-T-" in identifier] + [oid("ROOT")]},
        },
        "layer_exclusions": {
            "computation": {
                "status": "not_applicable_pending_independent_approval",
                "reason": "No reflection, solver, native code, oracle, experiment, enumeration, or unchecked certificate participates in the visible proof route.",
            }
        },
        "proof_body_aliases": {
            "ZMod.prod_Ico_one_prime": "presentation normalization in the same Wilson source; no second root-body credit",
            "Nat.prime_iff_fac_equiv_neg_one": "stronger iff whose forward branch invokes ZMod.wilsons_lemma; no duplicate body credit",
            "Nat.prime_of_fac_equiv_neg_one": "converse-only body outside the selected forward root",
            "external_Int.ModEq_Wilson": "different encoding and dependency pins; no checked transport or root credit",
        },
        "deduplication_policy": "The exact wrapper, Fact transport, related Wilson declarations, and readable presentation nodes cannot multiply semantic or terminal-body credit.",
        "delta_policy": "Any statement correction, split, merge, exclusion, eligibility/risk change, or proof-body identity change requires registry version 2 and an append-only old/new semantic-ID delta.",
        "append_only_delta": [],
        "obligations": obligations,
        "status_observed_after_freeze": {
            "conditional_interface_obligations": sorted(CHECKED_INTERFACES),
            "audited_candidate_obligation": oid("L-WILSON"),
            "audited_candidate_classification": "exact_pinned_candidate_only; accepted node remains M3 pending proof-phase admission and master acceptance",
            "accepted_closed_obligations": [],
            "root_machine_debt": "M3",
        },
        "status_boundary": "Registry scope and denominators only. No candidate or conditional interface has accepted proof credit; H0, M0, R0, audit completion, validation, release, and theorem completion remain open.",
    }
    registry_hash_fields = (
        "schema_version", "item_id", "theorem_id", "registry_id", "registry_version",
        "frozen_at", "freeze_basis", "frozen_against_statement_sha256",
        "frozen_against_anchor_audit_sha256", "frozen_task_contract_projection",
        "frozen_task_contract_sha256", "root_obligation_id", "denominator_sha256",
        "frozen_denominators", "layer_assessment", "layer_exclusions",
        "proof_body_aliases", "deduplication_policy", "delta_policy",
        "append_only_delta", "obligations", "status_boundary",
        "status_observed_after_freeze",
    )
    registry["registry_hash_fields"] = list(registry_hash_fields)
    registry["registry_content_sha256"] = digest(
        {field: registry[field] for field in registry_hash_fields}
    )

    def edge(edge_id: str, source: str, kind: str, target: str, reciprocal: str | None = None) -> dict:
        result = {"edge_id": edge_id, "type": kind, "from": source, "to": target}
        if reciprocal is not None:
            result["reciprocal_edge_id"] = reciprocal
        return result

    graph_names = (
        "proof", "refinement", "provenance", "evidence", "trust",
        "documentation", "workflow",
    )
    graph_edges: dict[str, list[dict]] = {name: [] for name in graph_names}
    for index, (parent, children) in enumerate(REQUIRES.items(), 1):
        for child_index, child in enumerate(children, 1):
            req = f"P{index:02d}-{child_index:02d}-REQ"
            comp = f"P{index:02d}-{child_index:02d}-COMP"
            graph_edges["proof"].extend([
                edge(req, parent, "proof_requires", child, comp),
                edge(comp, child, "composes", parent, req),
            ])
    graph_edges["refinement"] = [
        edge("R01", oid("ROOT"), "equivalent_to", oid("S-INTERFACE")),
        edge("R02", oid("ROOT"), "expository_decomposition", oid("S-BOUNDARY")),
        edge("R03", oid("S-FACT-TRANSPORT"), "transports", oid("ROOT")),
    ]
    provenance_targets = [
        identifier for identifier in ids
        if identifier not in {oid("X-SOURCE"), oid("X-PROVENANCE"), oid("X-TRUST"), oid("X-READABLE"), oid("X-WORKFLOW")}
    ]
    graph_edges["provenance"] = [
        *[
            edge(f"V{index:02d}", oid("X-PROVENANCE"), "provenance_of", target)
            for index, target in enumerate(provenance_targets, 1)
        ],
        *[
            edge(f"S{index:02d}", oid("X-SOURCE"), "source_map", target)
            for index, target in enumerate(
                [row["obligation_id"] for row in obligations if row["human_source_eligibility"] == "required"], 1
            )
            if target != oid("X-SOURCE")
        ],
        *[
            edge(
                f"E{parent_index:02d}-{child_index:02d}",
                child,
                "provenance_of",
                parent,
            )
            for parent_index, (parent, children) in enumerate(PROVENANCE_EXPANSIONS.items(), 1)
            for child_index, child in enumerate(children, 1)
        ],
    ]
    graph_edges["evidence"] = []
    graph_edges["trust"] = [
        edge("TR01", oid("ROOT"), "trusts", oid("S-FOUNDATION")),
        edge("TR02", oid("ROOT"), "trusts", oid("X-TRUST")),
        edge("TR03", oid("L-WILSON"), "trusts", oid("X-TRUST")),
        edge("TR04", oid("L-UNITS-PRODUCT"), "trusts", oid("X-TRUST")),
    ]
    graph_edges["documentation"] = [
        edge(f"D{index:02d}", oid("X-READABLE"), "documents", target)
        for index, target in enumerate(ids, 1) if target != oid("X-READABLE")
    ]
    task_projection = task_contract_projection()
    graph_edges["workflow"] = [
        edge("W01", oid("X-WORKFLOW"), "workflow_depends_on", oid("ROOT")),
        edge("W02", oid("X-WORKFLOW"), "workflow_depends_on", oid("X-SOURCE")),
        edge("W03", oid("X-WORKFLOW"), "workflow_depends_on", oid("X-PROVENANCE")),
        edge("W04", oid("X-WORKFLOW"), "workflow_depends_on", oid("X-TRUST")),
        edge("W05", oid("X-WORKFLOW"), "workflow_depends_on", oid("X-READABLE")),
    ]

    graphs = {}
    for name in graph_names:
        outgoing = {identifier: [] for identifier in ids}
        incoming = {identifier: [] for identifier in ids}
        for row in graph_edges[name]:
            outgoing[row["from"]].append(row["edge_id"])
            incoming[row["to"]].append(row["edge_id"])
        graphs[name] = {"edges": graph_edges[name], "out": outgoing, "in": incoming}

    fingerprints = {row["obligation_id"]: row["statement_fingerprint"] for row in obligations}
    certificates = []
    for parent, children in REQUIRES.items():
        certificates.append({
            "certificate_id": f"M0476-CERT-{parent.removeprefix(PREFIX + '-')}",
            "declaration": LOCAL_DECLARATIONS.get(parent, next(row[4] for row in ROWS if oid(row[0]) == parent)),
            "parent_id": parent,
            "parent_statement_fingerprint": fingerprints[parent],
            "required_child_ids": children,
            "required_child_statement_fingerprints": {child: fingerprints[child] for child in children},
            "conditional": True,
            "kernel_checked_interface": parent in LOCAL_DECLARATIONS,
            "accepted": False,
            "status": (
                "conditional_kernel_checked"
                if parent in LOCAL_DECLARATIONS
                else "planned_source_composition_pending_exact_child_harness"
            ),
            "statement_fingerprint_binding": "Root identity uses the elaborated expression hash; non-root planned:v1 hashes bind obligation ID, kind, claim, formal target, and output. Checked local declarations additionally carry exact Lean type ascriptions; proof-phase dependency inspection remains open.",
            "credit_boundary": (
                "tautological local expansion interface only; it does not invoke, identify, or admit the pinned terminal body"
                if parent in {oid("L-WILSON"), oid("L-UNITS-PRODUCT")} else
                "conditional exact-child composition only; accepted proof closure remains empty"
            ),
        })

    required_machine = registry["frozen_denominators"]["required_machine"]
    unique_frontier = list(PROOF_LEAVES)
    bundle = {
        "schema_version": "stage1-typed-graphs/1.0",
        "item_id": ITEM,
        "theorem_id": THEOREM,
        "registry_id": registry["registry_id"],
        "registry_denominator_sha256": denominator,
        "frozen_task_contract_sha256": registry["frozen_task_contract_sha256"],
        "root_node_id": oid("ROOT"),
        "edge_endpoint_namespace": "canonical obligation_id",
        "edge_direction": "proof_requires is parent-to-child; reciprocal composes is child-to-parent; non-proof graphs grant no proof closure",
        "graph_endpoint_policy": {
            "proof": {"allowed_types": ["proof_requires", "composes"], "excluded_endpoint_ids": [oid("S-FOUNDATION"), oid("S-BOUNDARY"), oid("X-SOURCE"), oid("X-PROVENANCE"), oid("X-TRUST"), oid("X-READABLE"), oid("X-WORKFLOW")], "endpoint_kind_policy": "mathematical obligations only; reciprocal exact-child pairs required"},
            "refinement": {"allowed_types": ["equivalent_to", "transports", "logical_decomposition", "expository_decomposition"], "excluded_endpoint_ids": [oid("X-SOURCE"), oid("X-PROVENANCE"), oid("X-TRUST"), oid("X-READABLE"), oid("X-WORKFLOW")], "endpoint_kind_policy": "mathematical obligations only; expository edges never affect machine closure"},
            "provenance": {"allowed_types": ["source_map", "provenance_of"], "required_source_ids": [oid("X-SOURCE"), oid("X-PROVENANCE")], "endpoint_kind_policy": "source/provenance overlays to mathematical obligations, plus pinned-body expansion links"},
            "evidence": {"allowed_types": ["evidence_for"], "must_be_empty": True, "endpoint_kind_policy": "empty until external content-addressed receipts exist"},
            "trust": {"allowed_types": ["trusts"], "allowed_target_ids": [oid("S-FOUNDATION"), oid("X-TRUST")], "endpoint_kind_policy": "mathematical obligations to foundation or trust certificate obligations"},
            "documentation": {"allowed_types": ["documents"], "allowed_source_ids": [oid("X-READABLE")], "endpoint_kind_policy": "readable overlay documents mathematical obligations"},
            "workflow": {"allowed_types": ["workflow_depends_on"], "allowed_source_ids": [oid("X-WORKFLOW")], "endpoint_kind_policy": "obligation overlay only; authoritative tasks live in workflow_task_graph"},
        },
        "workflow_task_graph": {
            "endpoint_namespace": "authoritative Stage1 task id",
            "task_contract_sha256": registry["frozen_task_contract_sha256"],
            "nodes": task_projection,
            "edges": [
                {"edge_id": f"TASK-{index:02d}", "type": "workflow_depends_on", "from": row["id"], "to": dependency}
                for index, row in enumerate(task_projection, 1)
                for dependency in row["depends_on"]
            ],
            "task_obligation_links": task_links,
        },
        "nodes": nodes,
        "graphs": graphs,
        "evidence_endpoint_policy": "Receipts are external typed objects. The evidence graph stays empty until content-addressed accepted evidence exists; node evidence_ids will bind it later.",
        "composition_certificates": certificates,
        "metrics": {
            "inventory_classification": {"numerator_ids": ids, "denominator_ids": ids, "status": "architecture_classified_unaccepted"},
            "unique_logical_leaf_closure": {"numerator_ids": [], "denominator_ids": unique_frontier},
            "distinct_proof_body_closure": {
                "numerator_ids": [],
                "denominator_ids": sorted({row["terminal_proof_body_id"] for row in obligations if row["terminal_proof_body_id"]}),
            },
            "interface_transport_closure": {
                "numerator_ids": [],
                "denominator_ids": [identifier for identifier in required_machine if any(token in identifier for token in ("S-INTERFACE", "S-FACT-TRANSPORT", "T-NAT-CAST", "T-REPRESENTATIVE", "T-INSERT", "T-UNITS-COE"))],
            },
            "readable_closure": {"numerator_ids": [], "denominator_ids": ids},
            "human_source_closure": {"numerator_ids": [], "denominator_ids": registry["frozen_denominators"]["required_human_source"]},
            "source_boundary_coverage": {"numerator_ids": [], "denominator_ids": required_machine},
            "root_closure": {"accepted": False, "root_id": oid("ROOT")},
            "critical_path_closure": {"numerator_ids": [], "denominator_ids": [oid("S-FACT-TRANSPORT"), oid("L-WILSON"), oid("T-COMPOSE")]},
            "risk_bucket_accepted_coverage": {
                risk: {"numerator_ids": [], "denominator_ids": [row["obligation_id"] for row in obligations if row["risk_class"] == risk]}
                for risk in ("critical", "high", "normal", "low")
            },
            "bounds": {"optimistic_closed_ids": [], "pessimistic_closed_ids": [], "disputed_eligibility_ids": []},
            "metamorphic_boundary": "aliases, wrappers, evidence-row cloning, and presentation splitting grant no accepted IDs and therefore leave all accepted numerators and root closure unchanged",
        },
        "closure_boundary": {
            "conditional_interface_obligations": sorted(CHECKED_INTERFACES),
            "candidate_only_obligations": [oid("L-WILSON"), oid("L-UNITS-PRODUCT")],
            "accepted_closed_obligations": [],
            "root_closed": False,
            "root_machine_debt": "M3",
            "audit_complete": False,
            "theorem_complete": False,
            "remaining_root_cut_set": [oid("S-FACT-TRANSPORT")],
            "remaining_proof_leaf_frontier": unique_frontier,
            "remaining_required_machine_assurance_frontier": [
                oid("S-INTERFACE"), oid("S-BOUNDARY"), oid("S-FACT-TRANSPORT"),
                oid("S-FOUNDATION"),
            ],
            "remaining_root_critical_nonproof_gates": [
                oid("S-FOUNDATION"), oid("X-SOURCE"), oid("X-PROVENANCE"),
                oid("X-TRUST"), oid("X-READABLE"), oid("X-WORKFLOW"),
            ],
            "reason": "Conditional interfaces elaborate, but the pinned body is not installed or accepted. H0/R0, transitive provenance/trust, validation, release, and master acceptance remain later gates.",
        },
    }

    recipes = {
        "schema_version": "stage1-validation-specs/1.0",
        "item_id": ITEM,
        "theorem_id": THEOREM,
        "recipes": [
            {
                "recipe_id": "S56-M-0476-OBLIGATION-TREE-STRUCTURE",
                "cwd": ".",
                "argv": ["python3", "-B", "Stage1_Instances/THM-M-0476/check_obligation_tree.py"],
                "env_allowlist": {},
                "timeout_seconds": 180,
                "network_policy": "denied",
                "expected_exit": 0,
                "expected_outputs": [{"path_or_stream": "stdout", "semantic_hash_policy": "contains PASS THM-M-0476 obligation tree"}],
                "covered_obligation_ids": [],
                "covered_declarations": [],
                "coverage_boundary": "registry, graphs, source pins, hygiene, and receipt structure only; no M0 or proof-closure credit",
            },
            {
                "recipe_id": "S56-M-0476-OBLIGATION-TREE-LEAN",
                "cwd": ".",
                "argv": ["python3", "-B", "Stage1_Instances/THM-M-0476/check_obligation_tree.py"],
                "env_allowlist": {},
                "timeout_seconds": 180,
                "network_policy": "denied",
                "expected_exit": 0,
                "expected_outputs": [{"path_or_stream": "stdout", "semantic_hash_policy": "reports conditional Lean output sha256"}],
                "covered_obligation_ids": sorted(CHECKED_INTERFACES | set(LEAF_DECLARATIONS)),
                "covered_declarations": sorted(set(LOCAL_DECLARATIONS.values()) | set(LEAF_DECLARATIONS.values())),
                "coverage_boundary": "conditional child-to-parent interface elaboration only; accepted proof closure remains empty",
            },
        ],
    }
    return registry, bundle, recipes


def serialized(value: dict) -> str:
    return json.dumps(value, ensure_ascii=True, indent=2) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()
    values = build()
    paths = ("obligation-registry.json", "typed-graphs.json", "validation-specs.json")
    if args.write:
        for name, value in zip(paths, values):
            (HERE / name).write_text(serialized(value), encoding="utf-8")
    else:
        for name, value in zip(paths, values):
            assert (HERE / name).read_text(encoding="utf-8") == serialized(value), (
                f"generated artifact drift: {name}"
            )
    edge_count = sum(len(graph["edges"]) for graph in values[1]["graphs"].values())
    print(f"PASS deterministic artifacts: {len(ROWS)} obligations, {edge_count} typed edges")
    print(f"registry denominator sha256: {values[0]['denominator_sha256']}")


if __name__ == "__main__":
    main()
