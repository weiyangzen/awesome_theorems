#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ITEM = "S56-M-0119-OBLIGATION_TREE"
TID = "THM-M-0119"
PREFIX = "M0119"

# (short id, kind, parent, human statement, formal target, output, risk)
SPECS = [
    ("ROOT", "root", None, "Prove the exact frozen projective klt-pair Kawamata--Viehweg vanishing target.", "Stage1Instances.THMM0119.KawamataViehwegVanishingTarget", "the exact target", "critical"),
    ("T", "composition", "ROOT", "Assemble every typed mathematical premise into the universally quantified positive-degree vanishing implication.", "planned exact composition into KawamataViehwegVanishingTarget", "the canonical root", "critical"),
    ("S", "definition", "T", "Preserve the frozen field, scheme, divisor, positivity, singularity, sheaf, and cohomological interfaces.", "KawamataViehwegData.Hypotheses and VanishingConclusion", "an exact statement boundary", "critical"),
    ("S-DATA", "definition", "S", "Realize the abstract scheme, Q-divisor, Cartier-divisor, canonical-boundary, and cohomology fields without assuming vanishing.", "planned native refinement of KawamataViehwegData", "typed geometric data", "critical"),
    ("S-HYP", "definition", "S", "Realize normal projectivity, effective boundary, Q-Cartier compatibility, klt, and nef-and-big hypotheses with their standard meanings.", "KawamataViehwegData.Hypotheses", "the full hypothesis package", "critical"),
    ("S-DEGREE", "branch", "S", "Cover every natural cohomological degree i with 0 < i while excluding degree zero and adding no dimension restriction.", "KawamataViehwegData.VanishingConclusion", "the exact degree boundary", "high"),
    ("S-TRANSPORT", "transport", "S", "Check the compact target against its fully expanded ordered-binder form.", "kawamataViehwegVanishingTarget_iff_expanded", "checked statement transport", "normal"),
    ("S-FOUNDATION", "certificate", "S", "Audit classical choice, quotients, extensionality, sheaf foundations, and all admitted axioms used by later bodies.", "planned foundation certificate", "an explicit logical boundary", "high"),
    ("N", "normalization", "T", "Normalize the Q-boundary and positivity data to the birational form consumed by the vanishing engine.", "planned birational normalization theorem", "normalized vanishing input", "critical"),
    ("N-INDEX", "normalization", "N", "Choose and control a common Cartier index for the rational boundary and canonical divisor data.", "planned Q-Cartier index package", "integral multiple data", "high"),
    ("N-RESOLUTION", "normalization", "N", "Pass to a log resolution while recording every exceptional divisor and simple-normal-crossings condition.", "planned characteristic-zero log resolution bridge", "resolved pair data", "critical"),
    ("N-PULLBACK", "transport", "N", "Pull back D-(K_X+Delta), preserve the required positivity, and state the exact rounding correction.", "planned divisor pullback and rounding identity", "normalized divisor identity", "critical"),
    ("B", "branch", "T", "Separate the harmless zero-dimensional boundary from the positive-dimensional birational argument and prove exhaustiveness.", "planned dimension branch theorem", "exhaustive dimensional coverage", "high"),
    ("B-DIM0", "terminal", "B", "Prove positive-degree coherent cohomology vanishing in the zero-dimensional case.", "planned dimension-zero cohomology theorem", "the zero-dimensional branch", "normal"),
    ("B-POSDIM", "branch", "B", "Carry the normalized log-resolution argument for positive-dimensional X in every positive degree.", "planned positive-dimensional branch", "the main branch conclusion", "critical"),
    ("B-RECOMPOSE", "composition", "B", "Recombine the dimension branches without restricting the canonical root.", "planned exhaustive branch composition", "all dimensions", "high"),
    ("C", "construction", "T", "Construct the birational and sheaf-theoretic objects needed to compare the resolved vanishing statement with O_X(D).", "planned resolution/sheaf comparison package", "typed comparison data", "critical"),
    ("C-LOGRES", "construction", "C", "Construct a projective log resolution with the required SNC boundary over the characteristic-zero base.", "planned log resolution object", "a resolved projective pair", "critical"),
    ("C-DISCREP", "construction", "C", "Use the klt discrepancy inequalities to form the exceptional correction divisor with controlled coefficients.", "planned discrepancy divisor package", "controlled exceptional divisor", "critical"),
    ("C-ROUND", "core_lemma", "C", "Prove the floor/ceiling identities that turn the pulled-back rational divisor expression into an integral line bundle.", "planned rounding identity", "an integral resolved divisor", "critical"),
    ("C-PUSH", "bridge", "C", "Identify the pushforward with O_X(D) and prove the higher-direct-image vanishings required for descent.", "planned pushforward and relative-vanishing package", "derived pushforward comparison", "critical"),
    ("L", "core_lemma", "T", "Prove the normalized logarithmic vanishing theorem and descend it to the singular klt pair.", "planned Kawamata--Viehweg proof engine", "positive-degree vanishing", "critical"),
    ("L-SMOOTH", "core_lemma", "L", "Prove the smooth SNC logarithmic vanishing result under the normalized nef-and-big hypothesis.", "planned smooth logarithmic vanishing theorem", "resolved-space vanishing", "critical"),
    ("L-INJECT", "core_lemma", "L", "Establish the injectivity or covering argument used by the smooth logarithmic vanishing theorem.", "planned logarithmic injectivity/cyclic-cover theorem", "the central smooth-case implication", "critical"),
    ("L-COHOM", "bridge", "L", "Connect divisorial sheaves and derived sheaf cohomology to the concrete groups in the frozen target.", "planned coherent-cohomology comparison", "target cohomology identification", "critical"),
    ("L-DESCENT", "core_lemma", "L", "Apply Leray and the pushforward comparison to transport resolved vanishing back to X.", "planned Leray descent theorem", "vanishing of H^i(X,O_X(D))", "critical"),
    ("X", "bridge", "T", "Freeze every missing imported interface and external theorem boundary used by the mathematical route.", "planned pinned dependency boundary", "auditable formal dependencies", "critical"),
    ("X-APIS", "bridge", "X", "Implement or immutably pin the absent Q-divisor, klt, positivity, log-resolution, divisorial-sheaf, and coherent-cohomology APIs.", "planned Lean API integration", "usable formal interfaces", "critical"),
    ("X-ANCHORS", "provenance", None, "Bind supporting mathlib declarations and any future external proof bodies to immutable revisions without awarding root proof credit.", "anchor-audit.json plus future provenance records", "terminal provenance inventory", "high"),
    ("X-TCB", "certificate", None, "Audit the kernel, imports, axioms, placeholders, computation, and reproducibility boundary.", "planned transitive trust certificate", "release trust closure", "critical"),
    ("P", "provenance", None, "Deduplicate wrappers and transports and identify the terminal body behind every root-critical declaration.", "planned provenance certificate", "body-origin closure", "high"),
    ("V", "certificate", None, "Attach node-specific exact-type, axiom, placeholder, composition, and freshness evidence.", "planned evidence bundle", "accepted validation evidence", "high"),
    ("R", "documentation", None, "Map primary proof sources to every mathematical node and provide one reviewed readable reconstruction.", "planned H0/R0 package", "source and readable closure", "high"),
]


def oid(short):
    return f"{PREFIX}-{short}"


def digest(value):
    raw = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


children = {short: [] for short, *_ in SPECS}
for short, _kind, parent, *_rest in SPECS:
    if parent:
        children[parent].append(short)

statement_sha = hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest()
overlays = {"X-ANCHORS", "X-TCB", "P", "V", "R"}
obligations = []
nodes = []
for short, kind, parent, statement, formal, output, risk in SPECS:
    overlay = short in overlays
    fingerprint = (
        f"lean-source-sha256:{statement_sha}"
        if short == "ROOT"
        else "planned:v1:sha256:" + digest({"id": oid(short), "kind": kind, "statement": statement, "formal_target": formal, "parent": oid(parent) if parent else None, "output": output})
    )
    obligations.append({
        "obligation_id": oid(short), "statement_fingerprint": fingerprint, "kind": kind,
        "root_relevant": not overlay, "machine_eligibility": "informational" if overlay else "required",
        "human_source_eligibility": "not_applicable" if short in {"X-TCB", "V"} else "required",
        "readable_eligibility": "required", "risk_class": risk,
        "exclusion_reason": "typed_provenance_evidence_trust_or_documentation_overlay" if overlay else None,
        "terminal_proof_body_id": None,
    })
    leaf = not children[short]
    nodes.append({
        "node_id": f"{TID}-{short}", "obligation_id": oid(short), "kind": kind,
        "human_statement": statement, "formal_target": formal, "output": output,
        "human_debt": "H4", "machine_debt": "M3" if short == "ROOT" else "M4",
        "readability_debt": "R4", "evidence_ids": [],
        "source_crosswalk_id": "anchor-audit-bounded-boundary" if short in {"ROOT", "X-ANCHORS"} else "pending-primary-source-node-crosswalk",
        "provenance_id": "M0119-A-MATHLIB" if short == "X-ANCHORS" else "none",
        "foundation_profile": "lean4-dependent-type-theory/policy-audit-pending",
        "tcb_profile": "lean-4.29.0/transitive-closure-pending", "computation_record": "none",
        "step_budget": 2 if leaf else "split-required",
        "semantic_step_ledger": [
            {"premises": f"exact inputs and hypotheses of {oid(short)}", "inference": statement, "output": output, "outgoing_use": oid(parent) if parent else "typed assurance graph"},
            {"premises": f"output of {oid(short)} plus its declared typed edge", "inference": "check the exact child-to-parent handoff without strengthening or hidden premises", "output": f"validated handoff of {oid(short)}", "outgoing_use": oid(parent) if parent else "audit or release gate"},
        ],
        "public_readable_target": f"Stage1_Instances/THM-M-0119/obligation-tree.md#{oid(short).lower()}",
        "validation_spec_id": f"VAL-{oid(short)}-PENDING",
        "status_boundary": "Frozen architecture only; no proof closure or source/readability acceptance is credited.",
        "task_ids": [ITEM, "S56-M-0119-PROOF"], "owned_sources": [],
        "owner": "THM-M-0119 proof implementer", "reviewer": "independent Stage1 integration reviewer",
        "validity": "frozen-2026-07-12; review_due=before-proof-acceptance; invalidate_on=statement,registry,edge,source,toolchain change; revocation=none",
    })

fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
projection = [{key: row[key] for key in fields} for row in obligations]
ids = [row["obligation_id"] for row in obligations]
registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM, "theorem_id": TID,
    "registry_version": 1,
    "freeze_basis": "The elaborated exact statement and bounded immutable anchor audit precede the mandatory S/N/B/C/L/X/T expansion. Eligibility was frozen while every proof body remained open.",
    "root_obligation_id": oid("ROOT"),
    "frozen_denominators": {
        "inventory": ids,
        "required_machine": [r["obligation_id"] for r in obligations if r["machine_eligibility"] == "required"],
        "required_human_source": [r["obligation_id"] for r in obligations if r["human_source_eligibility"] == "required"],
        "required_readable": ids,
        "informational_overlays": [r["obligation_id"] for r in obligations if r["machine_eligibility"] == "informational"],
    },
    "denominator_sha256": digest(projection),
    "delta_policy": "Any split, merge, eligibility change, exclusion, or target change requires registry version 2 and an append-only old/new ID delta.",
    "obligations": obligations,
}

edge_rows = {name: [] for name in ("proof", "refinement", "provenance", "evidence", "trust", "documentation", "workflow")}
for short, _kind, parent, *_rest in SPECS:
    if not parent:
        continue
    edge_rows["proof"].append({
        "edge_id": f"PROOF-{parent}-{short}",
        "type": "composes" if parent == "ROOT" else "proof_requires",
        "from": oid(parent), "to": oid(short),
    })
edge_rows["refinement"] = [
    {"edge_id": "REFINE-N-C", "type": "logical_decomposition", "from": oid("N"), "to": oid("C")},
    {"edge_id": "REFINE-C-LDESC", "type": "logical_decomposition", "from": oid("C-PUSH"), "to": oid("L-DESCENT")},
]
edge_rows["provenance"] = [
    {"edge_id": "PROV-ROOT-P", "type": "provenance_of", "from": oid("ROOT"), "to": oid("P")},
    {"edge_id": "PROV-X-ANCHORS", "type": "provenance_of", "from": oid("X"), "to": oid("X-ANCHORS")},
]
edge_rows["evidence"] = [
    {"edge_id": "EVID-ROOT-V", "type": "evidence_for", "from": oid("ROOT"), "to": oid("V")},
    {"edge_id": "EVID-V-TRANSPORT", "type": "evidence_for", "from": oid("V"), "to": oid("S-TRANSPORT")},
]
edge_rows["trust"] = [
    {"edge_id": "TRUST-ROOT-TCB", "type": "trusts", "from": oid("ROOT"), "to": oid("X-TCB")},
    {"edge_id": "TRUST-V-TCB", "type": "trusts", "from": oid("V"), "to": oid("X-TCB")},
]
edge_rows["documentation"] = [
    {"edge_id": "DOC-ROOT-R", "type": "documents", "from": oid("ROOT"), "to": oid("R")},
    {"edge_id": "DOC-R-S", "type": "documents", "from": oid("R"), "to": oid("S")},
    {"edge_id": "DOC-R-N", "type": "documents", "from": oid("R"), "to": oid("N")},
    {"edge_id": "DOC-R-C", "type": "documents", "from": oid("R"), "to": oid("C")},
    {"edge_id": "DOC-R-L", "type": "documents", "from": oid("R"), "to": oid("L")},
]
edge_rows["workflow"] = [
    {"edge_id": "FLOW-ROOT-T", "type": "workflow_depends_on", "from": oid("ROOT"), "to": oid("T")},
    {"edge_id": "FLOW-T-V", "type": "workflow_depends_on", "from": oid("T"), "to": oid("V")},
]

graphs = {}
for name, edges in edge_rows.items():
    outgoing = {node: [] for node in ids}
    incoming = {node: [] for node in ids}
    for edge in edges:
        outgoing[edge["from"]].append(edge["edge_id"])
        incoming[edge["to"]].append(edge["edge_id"])
    graphs[name] = {"edges": edges, "out": outgoing, "in": incoming}

bundle = {
    "schema_version": "stage1-typed-graphs/1.0", "item_id": ITEM, "theorem_id": TID,
    "nodes": nodes, "graphs": graphs,
    "closure_boundary": {
        "closed_obligations": [], "root_machine_debt": "M3",
        "remaining_root_cut_set": [oid("X-APIS"), oid("N-RESOLUTION"), oid("L-SMOOTH"), oid("C-PUSH")],
        "composition_certificates_checked": [
            "Stage1Instances.THMM0119.ObligationTree.positive_degrees_compose",
            "Stage1Instances.THMM0119.ObligationTree.implication_compose",
        ],
        "theorem_complete": False,
        "reason": "The pinned environment has only an elaborated abstract statement interface and nearby sheaf infrastructure; all substantive birational, singularity, positivity, and vanishing bodies remain open.",
    },
}

(HERE / "obligation-registry.json").write_text(json.dumps(registry, indent=2) + "\n")
(HERE / "typed-graphs.json").write_text(json.dumps(bundle, indent=2) + "\n")
print(f"wrote {len(obligations)} obligations and {sum(len(v) for v in edge_rows.values())} typed edges")
print(f"registry denominator sha256: {registry['denominator_sha256']}")
