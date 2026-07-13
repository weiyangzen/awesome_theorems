#!/usr/bin/env python3
"""Build the frozen THM-M-0471 obligation registry and typed graph bundle."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ITEM = "S56-M-0471-OBLIGATION_TREE"
THEOREM = "THM-M-0471"
PREFIX = "M0471"
ROOT_EXPRESSION = "07ae92b7b398b89a1bbe8413563f1c30da5b8bbd0522f6d070fd62dcea0ac4e4"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
FACTORS_BLOB = "292355d305be37499c8415d15b430aa241132c9b"
LIST_PRIME_BLOB = "17337ba91fd2f4b2b947301cca165a253662e377"
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
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return hashlib.sha256(payload.encode()).hexdigest()


def oid(short: str) -> str:
    return f"{PREFIX}-{short}"


# Eligibility and risk are frozen here before any observed closure status is attached.
ROWS = (
    (
        "ROOT", "root", "critical",
        "Prove the exact natural-number prime-list target frozen in Statement.lean.",
        "Stage1Instances.THM_M_0471.FundamentalTheoremOfArithmeticTarget",
        "Every n > 1 has a nonempty prime list with product n, unique up to permutation.",
        "required", "required", None, 30,
    ),
    (
        "S-INTERFACE", "definition", "critical",
        "Preserve the Nat domain, n > 1 premise, list witness, primality, product, and List.Perm binder scope.",
        "Stage1Instances.THM_M_0471.FundamentalTheoremOfArithmeticTarget",
        "The exact canonical proposition with no strengthened or weakened clause.",
        "required", "required", None, 45,
    ),
    (
        "S-BOUNDARY", "branch", "high",
        "Exclude zero and one through 1 < n while retaining n = 2, prime powers, repeated factors, and reorderings.",
        "the boundary policy of FundamentalTheoremOfArithmeticTarget",
        "An exhaustive boundary account for the selected positive-natural root.",
        "required", "required", None, 40,
    ),
    (
        "S-TRANSPORT", "transport", "high",
        "Relate the named target to its checked direct expansion without adding an integer or exponent-map encoding.",
        "Stage1Instances.THM_M_0471.fundamentalTheoremOfArithmeticTarget_iff_expanded",
        "A checked iff to the expanded prime-list clauses.",
        "required", "not_applicable",
        "formal_encoding_transport_not_a_separate_human_claim_pending_reviewer_acceptance", 25,
    ),
    (
        "S-FOUNDATION", "certificate", "critical",
        "Audit propext, Classical.choice, Quot.sound, the Lean kernel, imports, and the no-oracle policy.",
        "planned transitive foundation, TCB, and computation report",
        "An accepted trust boundary for every root-critical declaration.",
        "required", "not_applicable",
        "formal_trust_boundary_not_a_human_mathematical_claim_pending_reviewer_acceptance", 60,
    ),
    (
        "T-ROOT-COMPOSE", "terminal", "high",
        "Consume the exact prime-list child proposition and return the canonical target without adding a premise.",
        "Stage1Instances.THM_M_0471.ObligationTree.root_of_exactPrimeListAnchor",
        "Stage1Instances.THM_M_0471.FundamentalTheoremOfArithmeticTarget.",
        "required", "required",
        "local:Stage1_Instances/THM-M-0471/ObligationTree.lean#root_of_exactPrimeListAnchor", 12,
    ),
    (
        "T-ASSEMBLE", "terminal", "critical",
        "Assemble the factor witness and pairwise uniqueness packages into the exact prime-list anchor.",
        "Stage1Instances.THM_M_0471.ObligationTree.exactPrimeListAnchor_of_packages",
        "Stage1Instances.THM_M_0471.ObligationTree.ExactPrimeListAnchor.",
        "required", "required",
        "local:Stage1_Instances/THM-M-0471/ObligationTree.lean#exactPrimeListAnchor_of_packages", 30,
    ),
    (
        "C-WITNESS", "construction", "critical",
        "Choose n.primeFactorsList as the canonical finite witness for each n > 1.",
        "Nat.primeFactorsList",
        "The list used by the nonempty, primality, product, and uniqueness children.",
        "required", "required",
        f"git-blob:{FACTORS_BLOB}:Nat.primeFactorsList", 35,
    ),
    (
        "L-NONEMPTY", "core_lemma", "high",
        "Derive nonemptiness of the canonical factor list exactly from 1 < n.",
        "Nat.primeFactorsList_ne_nil",
        "n.primeFactorsList != [].",
        "required", "required",
        f"git-blob:{FACTORS_BLOB}:Nat.primeFactorsList_ne_nil", 30,
    ),
    (
        "N-NONZERO", "normalization", "high",
        "Convert 1 < n to n != 0 for product reconstruction and rule out product zero in uniqueness.",
        "Nat.ne_zero_of_lt together with Prime.ne_zero and List.prod_eq_zero_iff",
        "The nonzero side conditions used by reconstruction and uniqueness.",
        "required", "required", None, 40,
    ),
    (
        "L-PRIMALITY", "core_lemma", "critical",
        "Prove every member of primeFactorsList n prime by recursive minFac extraction.",
        "Nat.prime_of_mem_primeFactorsList",
        "forall p in n.primeFactorsList, p.Prime.",
        "required", "required",
        f"git-blob:{FACTORS_BLOB}:Nat.prime_of_mem_primeFactorsList", 60,
    ),
    (
        "L-PRODUCT", "core_lemma", "critical",
        "Reconstruct n as the product of its recursive minFac factor list.",
        "Nat.prod_primeFactorsList",
        "n.primeFactorsList.prod = n for n != 0.",
        "required", "required",
        f"git-blob:{FACTORS_BLOB}:Nat.prod_primeFactorsList", 60,
    ),
    (
        "L-UNIQUENESS", "bridge", "critical",
        "Show every prime list with product n permutes to n.primeFactorsList.",
        "Nat.primeFactorsList_unique",
        "k.Perm n.primeFactorsList for every prime list k with product n.",
        "required", "required",
        f"git-blob:{FACTORS_BLOB}:Nat.primeFactorsList_unique", 55,
    ),
    (
        "L-PERM-PRODUCT", "core_lemma", "critical",
        "Turn equal products of prime lists into a permutation by recursive head matching and cancellation.",
        "perm_of_prod_eq_prod",
        "List.Perm l1 l2 from equal products and primality of both lists.",
        "required", "required",
        f"git-blob:{LIST_PRIME_BLOB}:perm_of_prod_eq_prod", 65,
    ),
    (
        "L-PRIME-DVD-PRODUCT", "core_lemma", "high",
        "Expose the prime-divides-product equivalence used to locate a matching list member.",
        "Prime.dvd_prod_iff",
        "A prime divisor of a list product divides one member.",
        "required", "required",
        f"git-blob:{LIST_PRIME_BLOB}:Prime.dvd_prod_iff", 50,
    ),
    (
        "L-MEM-PRIME-DIVISOR", "core_lemma", "high",
        "Use primality of every list member to strengthen divisibility of the product to membership.",
        "mem_list_primes_of_dvd_prod",
        "A prime divisor of a product of primes occurs in that list.",
        "required", "required",
        f"git-blob:{LIST_PRIME_BLOB}:mem_list_primes_of_dvd_prod", 35,
    ),
    (
        "C-ERASE-PERM", "construction", "high",
        "Move the matching prime to the head and erase its selected occurrence from the second list.",
        "List.perm_cons_erase",
        "A permutation from the second list to the common head plus its erasure.",
        "required", "required", None, 35,
    ),
    (
        "N-CANCEL-HEAD", "normalization", "high",
        "Cancel the common nonzero prime factor and recurse on the remaining equal products.",
        "mul_right_inj' together with List.Perm.prod_eq",
        "Equality of tail products after matching and cancelling one prime.",
        "required", "required", None, 45,
    ),
    (
        "X-SOURCE", "terminal", "critical",
        "Map existence, uniqueness, boundaries, and assumptions to pinpoint primary human sources and errata.",
        "non-machine primary-source crosswalk",
        "Reviewed H evidence for every mathematical node.",
        "not_applicable", "required",
        "non_machine_source_boundary_pending_independent_approval", 60,
    ),
    (
        "X-PROVENANCE", "certificate", "critical",
        "Resolve wrapper, terminal bodies, source blobs, imports, aliases, licenses, and transitive declaration origins.",
        "planned machine-derived provenance closure",
        "A deduplicated terminal-body and dependency graph.",
        "not_applicable", "not_applicable",
        "informational_provenance_overlay_pending_independent_approval", 60,
    ),
    (
        "X-READABLE", "terminal", "high",
        "Produce and independently review a node-specific readable reconstruction of both existence and uniqueness.",
        "planned readable proof reconstruction",
        "Reviewed R evidence linked to every root-critical node.",
        "not_applicable", "required",
        "non_machine_readability_boundary_pending_independent_approval", 60,
    ),
    (
        "X-WORKFLOW", "certificate", "critical",
        "Bind proof, validation, hermetic replay, freshness, revocation, independent verification, and release receipts.",
        "planned Stage1 workflow receipts",
        "Dependency-legal accepted state without becoming a proof premise.",
        "not_applicable", "not_applicable",
        "workflow_overlay_pending_independent_approval", 60,
    ),
)


def make_edge(edge_id: str, source: str, kind: str, target: str, reciprocal: str | None = None) -> dict:
    edge = {"edge_id": edge_id, "from": oid(source), "type": kind, "to": oid(target)}
    if reciprocal is not None:
        edge["reciprocal_edge_id"] = reciprocal
    return edge


PROOF_REQUIREMENTS = (
    ("ROOT", "T-ROOT-COMPOSE"),
    ("T-ROOT-COMPOSE", "T-ASSEMBLE"),
    ("T-ASSEMBLE", "C-WITNESS"),
    ("T-ASSEMBLE", "L-NONEMPTY"),
    ("T-ASSEMBLE", "L-PRIMALITY"),
    ("T-ASSEMBLE", "L-PRODUCT"),
    ("T-ASSEMBLE", "L-UNIQUENESS"),
    ("L-NONEMPTY", "S-BOUNDARY"),
    ("L-PRODUCT", "N-NONZERO"),
    ("L-UNIQUENESS", "N-NONZERO"),
    ("L-UNIQUENESS", "L-PERM-PRODUCT"),
    ("L-PERM-PRODUCT", "L-PRIME-DVD-PRODUCT"),
    ("L-PERM-PRODUCT", "L-MEM-PRIME-DIVISOR"),
    ("L-PERM-PRODUCT", "C-ERASE-PERM"),
    ("L-PERM-PRODUCT", "N-CANCEL-HEAD"),
)

OTHER_EDGES = {
    "refinement": (
        ("REF-ROOT-INTERFACE", "ROOT", "equivalent_to", "S-INTERFACE"),
        ("REF-ROOT-BOUNDARY", "ROOT", "logical_decomposition", "S-BOUNDARY"),
        ("REF-ROOT-TRANSPORT", "ROOT", "transports", "S-TRANSPORT"),
        ("REF-WITNESS-PRIMALITY", "C-WITNESS", "logical_decomposition", "L-PRIMALITY"),
        ("REF-WITNESS-PRODUCT", "C-WITNESS", "logical_decomposition", "L-PRODUCT"),
    ),
    "provenance": (
        ("PROV-FACTORS-BODY", "X-PROVENANCE", "provenance_of", "L-UNIQUENESS"),
        ("PROV-LIST-BODY", "X-PROVENANCE", "provenance_of", "L-PERM-PRODUCT"),
        ("SRC-ROOT", "X-SOURCE", "source_map", "ROOT"),
        ("SRC-EXISTENCE", "X-SOURCE", "source_map", "L-PRODUCT"),
        ("SRC-UNIQUENESS", "X-SOURCE", "source_map", "L-UNIQUENESS"),
    ),
    "evidence": (
        ("EVID-PROVENANCE-UNIQUE", "X-PROVENANCE", "evidence_for", "L-UNIQUENESS"),
        ("EVID-WORKFLOW-ROOT", "X-WORKFLOW", "evidence_for", "ROOT"),
    ),
    "trust": (
        ("TRUST-ROOT-FOUNDATION", "ROOT", "trusts", "S-FOUNDATION"),
        ("TRUST-ROOT-PROVENANCE", "ROOT", "trusts", "X-PROVENANCE"),
        ("TRUST-UNIQUE-PROVENANCE", "L-UNIQUENESS", "trusts", "X-PROVENANCE"),
    ),
    "documentation": (
        ("DOC-READABLE-ROOT", "X-READABLE", "documents", "ROOT"),
        ("DOC-READABLE-EXISTENCE", "X-READABLE", "documents", "L-PRODUCT"),
        ("DOC-READABLE-UNIQUE", "X-READABLE", "documents", "L-PERM-PRODUCT"),
        ("DOC-SOURCE-ROOT", "X-SOURCE", "documents", "ROOT"),
    ),
    "workflow": (
        ("FLOW-ROOT-PROOF", "X-WORKFLOW", "workflow_depends_on", "T-ASSEMBLE"),
        ("FLOW-ROOT-PROVENANCE", "X-WORKFLOW", "workflow_depends_on", "X-PROVENANCE"),
        ("FLOW-ROOT-SOURCE", "X-WORKFLOW", "workflow_depends_on", "X-SOURCE"),
        ("FLOW-ROOT-READABLE", "X-WORKFLOW", "workflow_depends_on", "X-READABLE"),
        ("FLOW-ROOT-FOUNDATION", "X-WORKFLOW", "workflow_depends_on", "S-FOUNDATION"),
    ),
}


def planned_fingerprint(short: str, human: str, formal: str, output: str) -> str:
    if short in {"ROOT", "S-INTERFACE"}:
        return f"lean-expression-sha256:{ROOT_EXPRESSION}"
    return f"planned:v1:sha256:{digest({'id': oid(short), 'human': human, 'formal': formal, 'output': output})}"


def build() -> tuple[dict, dict, dict]:
    obligations = []
    for short, kind, risk, human, formal, output, machine, source, body, _budget in ROWS:
        exclusion = None
        if machine != "required" or source != "required":
            # The reason is stored in the body-position companion for non-required overlays only.
            exclusion = body if body and "pending" in body else None
        terminal_body = body if body and "pending" not in body else None
        obligations.append({
            "obligation_id": oid(short),
            "statement_fingerprint": planned_fingerprint(short, human, formal, output),
            "kind": kind,
            "root_relevant": short not in {"X-PROVENANCE", "X-WORKFLOW"},
            "machine_eligibility": machine,
            "human_source_eligibility": source,
            "readable_eligibility": "required",
            "risk_class": risk,
            "exclusion_reason": exclusion,
            "terminal_proof_body_id": terminal_body,
        })

    field_order = (
        "obligation_id", "statement_fingerprint", "kind", "root_relevant",
        "machine_eligibility", "human_source_eligibility", "readable_eligibility",
        "risk_class", "exclusion_reason", "terminal_proof_body_id",
    )
    projection = [{key: row[key] for key in field_order} for row in obligations]
    denominator = digest(projection)
    ids = [row["obligation_id"] for row in obligations]
    registry = {
        "schema_version": "stage1-obligation-registry/1.0",
        "item_id": ITEM,
        "theorem_id": THEOREM,
        "registry_version": 1,
        "frozen_at": "2026-07-13T00:00:00+08:00",
        "freeze_basis": "Exact Nat/list/permutation statement and immutable anchor inventory, expanded through the visible pinned Factors.lean and List/Prime.lean terminal bodies before current closure status was attached.",
        "frozen_against_statement_sha256": hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest(),
        "frozen_against_anchor_audit_sha256": hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest(),
        "root_obligation_id": oid("ROOT"),
        "denominator_sha256": denominator,
        "frozen_denominators": {
            "inventory": ids,
            "required_machine": [row["obligation_id"] for row in obligations if row["machine_eligibility"] == "required"],
            "required_human_source": [row["obligation_id"] for row in obligations if row["human_source_eligibility"] == "required"],
            "required_readable": ids,
            "informational_overlays": [oid("X-PROVENANCE"), oid("X-WORKFLOW")],
        },
        "layer_exclusions": {
            "independent_branch_split": {
                "status": "not_applicable_pending_independent_approval",
                "reason": "The candidate proof is uniform for n > 1; zero, one, n = 2, primes, prime powers, and reorderings remain explicit in M0471-S-BOUNDARY rather than becoming proof-credit branches.",
            },
            "external_computation": {
                "status": "not_applicable_pending_independent_approval",
                "reason": "The visible route uses kernel-checked recursive definitions and theorems; no solver, native evaluator, oracle, experiment, or certificate participates.",
            },
        },
        "delta_policy": "Any target correction, split, merge, exclusion, eligibility change, or proof-body identity change requires registry version 2 and an append-only old/new semantic ID delta.",
        "append_only_delta": [],
        "obligations": obligations,
        "status_observed_after_freeze": {
            "accepted_closed_obligations": [],
            "root_vector": {"H": "H1", "M": "M3", "R": "R4"},
            "root_machine_debt": "M3",
            "candidate_observation": "Exact M0-W candidate exists in pinned mathlib but remains uninstalled and unaccepted until the proof phase and master validation.",
            "audit_complete": False,
            "theorem_complete": False,
        },
        "status_boundary": "Registry and eligibility freeze only; no node is accepted closed and no proof, source, readability, trust, audit-completion, release, or theorem-completion credit is created.",
    }

    nodes = []
    for short, kind, _risk, human, formal, output, _machine, source, body, budget in ROWS:
        machine_debt = "M3" if short in {"ROOT", "T-ROOT-COMPOSE", "T-ASSEMBLE"} else "M4"
        if short in {"S-INTERFACE", "S-TRANSPORT"}:
            machine_debt = "M0-L"
        source_id = "source-statement-crosswalk.md; node pinpoint and independent review pending"
        if source == "not_applicable":
            source_id = "not-applicable; exclusion pending independent approval"
        provenance = "anchor-audit.json; full transitive provenance pending"
        if body and "pending" not in body:
            provenance = body
        nodes.append({
            "node_id": f"{THEOREM}-{short}",
            "obligation_id": oid(short),
            "kind": kind,
            "human_statement": human,
            "formal_target": formal,
            "output": output,
            "human_debt": "H1",
            "machine_debt": machine_debt,
            "readability_debt": "R4",
            "evidence_ids": [],
            "source_crosswalk_id": source_id,
            "provenance_id": provenance,
            "foundation_profile": "lean4-foundation-statement/1.0; transitive acceptance pending",
            "tcb_profile": "lean-4.29.0+mathlib-8a178386; transitive closure pending",
            "computation_record": "none; no computation, oracle, or unchecked certificate may close this node",
            "step_budget": budget,
            "semantic_step_ledger": {
                "premises": "Only the typed proof_requires children and the stated formal context.",
                "inference": human,
                "output": output,
                "outgoing_use": "Only declared typed edges may consume this output; source, documentation, trust, and workflow edges confer no proof credit.",
            },
            "public_readable_target": f"Stage1_Instances/{THEOREM}/obligation-tree.md#{oid(short).lower()}",
            "validation_spec_id": f"VAL-{oid(short)}",
            "status_boundary": "Frozen architecture or checked conditional interface only; this record does not install a proof body or close an open child.",
            "task_ids": [ITEM, "S56-M-0471-PROOF", "S56-M-0471-VALIDATION"],
            "owned_sources": [formal] if formal.startswith("Stage1Instances.") else [],
            "owner": "THM-M-0471 proof lane",
            "reviewer": "independent Stage1 integration lane",
            "validity": {
                "validated_at": None,
                "review_due": "before proof acceptance",
                "invalidation_inputs": ["statement", "registry", "anchor inventory", "source map", "toolchain"],
                "revocation_state": "open",
            },
        })

    graph_edges: dict[str, list[dict]] = {name: [] for name in GRAPH_NAMES}
    for parent, child in PROOF_REQUIREMENTS:
        req = f"REQ-{oid(parent)}-{oid(child)}"
        comp = f"CMP-{oid(child)}-{oid(parent)}"
        graph_edges["proof"].append(make_edge(req, parent, "proof_requires", child, comp))
        graph_edges["proof"].append(make_edge(comp, child, "composes", parent, req))
    for graph_name, edges in OTHER_EDGES.items():
        for edge_id, source, kind, target in edges:
            graph_edges[graph_name].append(make_edge(edge_id, source, kind, target))

    graphs = {}
    for name, edges in graph_edges.items():
        outgoing = {obligation_id: [] for obligation_id in ids}
        incoming = {obligation_id: [] for obligation_id in ids}
        for edge in edges:
            outgoing[edge["from"]].append(edge["edge_id"])
            incoming[edge["to"]].append(edge["edge_id"])
        graphs[name] = {"edges": edges, "out": outgoing, "in": incoming}

    bundle = {
        "schema_version": "stage1-typed-graphs/1.0",
        "item_id": ITEM,
        "theorem_id": THEOREM,
        "registry_id": f"{THEOREM}-OBLIGATIONS-v1",
        "registry_denominator_sha256": denominator,
        "root_node_id": oid("ROOT"),
        "edge_endpoint_namespace": "canonical obligation_id",
        "edge_direction": "proof_requires is parent-to-child; reciprocal composes is child-to-parent",
        "nodes": nodes,
        "graphs": graphs,
        "closure_boundary": {
            "interface_checked_obligations": [oid("S-INTERFACE"), oid("S-TRANSPORT"), oid("T-ROOT-COMPOSE"), oid("T-ASSEMBLE")],
            "accepted_closed_obligations": [],
            "root_closed": False,
            "root_machine_debt": "M3",
            "audit_complete": False,
            "theorem_complete": False,
            "remaining_root_cut_set": [oid("T-ASSEMBLE"), oid("S-FOUNDATION"), oid("X-SOURCE"), oid("X-PROVENANCE"), oid("X-READABLE"), oid("X-WORKFLOW")],
            "composition_certificates": [
                "Stage1Instances.THM_M_0471.ObligationTree.exactPrimeListAnchor_of_packages",
                "Stage1Instances.THM_M_0471.ObligationTree.root_of_exactPrimeListAnchor",
            ],
            "reason": "Both compositions are conditional. The exact pinned mathlib family remains uninstalled and unaccepted until proof-phase adoption and master validation.",
        },
    }

    recipes = []
    for row, node in zip(obligations, nodes):
        declarations = []
        formal = node["formal_target"]
        if formal.startswith(("Stage1Instances.", "Nat.", "Prime.", "List.", "perm_", "mem_")):
            declarations = [formal]
        recipes.append({
            "recipe_id": node["validation_spec_id"],
            "cwd": ".",
            "argv": ["python3", "-B", f"Stage1_Instances/{THEOREM}/check_obligation_tree.py"],
            "env_allowlist": {},
            "timeout_seconds": 180,
            "network_policy": "denied",
            "expected_exit": 0,
            "expected_outputs": [{"path_or_stream": "stdout", "semantic_hash_policy": f"contains PASS {THEOREM} obligation tree"}],
            "covered_obligation_ids": [row["obligation_id"]],
            "covered_declarations": declarations,
        })
    specs = {
        "schema_version": "stage1-validation-specs/1.0",
        "item_id": ITEM,
        "theorem_id": THEOREM,
        "recipes": recipes,
    }
    return registry, bundle, specs


def canonical(value: object) -> str:
    return json.dumps(value, indent=2, ensure_ascii=True) + "\n"


def main() -> None:
    registry, bundle, specs = build()
    for name, value in (
        ("obligation-registry.json", registry),
        ("typed-graphs.json", bundle),
        ("validation-specs.json", specs),
    ):
        (HERE / name).write_text(canonical(value), encoding="utf-8")
    edge_count = sum(len(graph["edges"]) for graph in bundle["graphs"].values())
    print(f"wrote {len(registry['obligations'])} obligations and {edge_count} typed edges")
    print(f"registry denominator sha256: {registry['denominator_sha256']}")


if __name__ == "__main__":
    main()
