#!/usr/bin/env python3
"""Build the frozen rev-5.6 obligation registry and typed graph bundle."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-0767-OBLIGATION_TREE"
TASKS = [ITEM, "S56-M-0767-PROOF"]


def row(oid, kind, human, formal, output, *, risk="normal", machine="required",
        human_source="required", readable="required", body=None, steps=4,
        provenance="none"):
    fingerprint = hashlib.sha256(
        f"THM-M-0767|{oid}|{formal}".encode()
    ).hexdigest()
    root_relevant = machine == "required"
    exclusion = None if root_relevant else "typed_trust_or_provenance_overlay"
    return {
        "registry": {
            "obligation_id": oid,
            "statement_fingerprint": fingerprint,
            "kind": kind,
            "root_relevant": root_relevant,
            "machine_eligibility": machine,
            "human_source_eligibility": human_source,
            "readable_eligibility": readable,
            "risk_class": risk,
            "exclusion_reason": exclusion,
            "terminal_proof_body_id": body,
        },
        "node": {
            "node_id": f"THM-M-0767-{oid.removeprefix('M0767-')}",
            "obligation_id": oid,
            "kind": kind,
            "human_statement": human,
            "formal_target": formal,
            "output": output,
            "human_debt": "H1",
            "machine_debt": "M3" if oid in {"M0767-ROOT", "M0767-X-X2", "M0767-T-T2"} else "M4",
            "readability_debt": "R4",
            "evidence_ids": [],
            "source_crosswalk_id": "source-statement-crosswalk:crosswalk",
            "provenance_id": provenance,
            "foundation_profile": "lean4-cardinal-classical/v1-review-pending",
            "tcb_profile": "lean-4.29.0-mathlib-8a178386/transitive-closure-pending",
            "computation_record": "none",
            "step_budget": steps,
            "semantic_step_ledger": (
                f"Premises are the incoming typed proof/refinement edges for {oid}; "
                f"establish the exact target `{formal}`; deliver `{output}` to every outgoing "
                "composition edge. No source, wrapper, or name supplies proof credit by itself."
            ),
            "public_readable_target": f"Stage1_Instances/THM-M-0767/obligation-tree.md#{oid.lower().replace('.', '')}",
            "validation_spec_id": f"VAL-{oid}-PENDING",
            "status_boundary": "Architecture only; no proof body or parent composition certificate is accepted by this freeze.",
            "task_ids": TASKS,
            "owned_sources": [],
            "owner": "THM-M-0767 proof implementer",
            "reviewer": "independent Stage1 integration reviewer",
            "validity": "frozen-2026-07-12; review_due=before-proof-acceptance; invalidate_on=statement,registry,source,toolchain,profile change; revocation=none",
        },
    }


specs = [
    row("M0767-ROOT", "root", "Every set has cardinality strictly below its full powerset.",
        "Stage1.THM_M_0767.CanonicalTarget", "The exact canonical target.", risk="critical", steps="split-required"),
    row("M0767-S", "definition", "Freeze the statement, universe, boundary, transports, and foundation policy.",
        "Statement/foundation package for CanonicalTarget", "An unambiguous exact target and policy.", risk="high", steps="split-required"),
    row("M0767-S-S1", "definition", "A set is represented by its subtype and its powerset by Set.powerset.",
        "alpha : Type u; s : Set alpha; Set.powerset s", "The two carrier subtypes compared by Cardinal.mk."),
    row("M0767-S-S2", "definition", "Both compared subtype cardinals inhabit the same universe.",
        "Cardinal.mk s < Cardinal.mk (Set.powerset s)", "No Cardinal.lift or hidden universe premise."),
    row("M0767-S-S3", "branch", "The target includes empty, finite, and infinite sets without extra hypotheses.",
        "CanonicalTarget with alpha=Empty and alpha=Fin 3 fixtures", "Boundary coverage without exclusions."),
    row("M0767-S-S4", "transport", "Set-level, type-level, and cardinal-exponential formulations are related in checked directions.",
        "canonical_iff_exponential / canonical_iff_type", "Checked encoding transports.", risk="high"),
    row("M0767-S-S5", "definition", "The allowed use of propext, Classical.choice, and Quot.sound is explicitly reviewed.",
        "axioms of all admitted terminal declarations subset accepted foundation profile", "Accepted foundation boundary.", risk="high"),
    row("M0767-N", "normalization", "Normalize powerset subtype cardinality to cardinal exponentiation.",
        "Cardinal.mk (Set.powerset s) = 2 ^ Cardinal.mk s", "Canonical exponential comparison.", risk="high", steps="split-required"),
    row("M0767-N-N1", "transport", "Apply the checked powerset-cardinality identity in the required direction.",
        "Cardinal.mk_powerset (s := s)", "Rewrite the root conclusion to Cardinal.mk s < 2 ^ Cardinal.mk s.", risk="high",
        provenance="mathlib:Cardinal.mk_powerset@8a178386"),
    row("M0767-N-N2", "normalization", "Preserve the direction and strictness of the cardinal comparison.",
        "Cardinal.mk s < 2 ^ Cardinal.mk s", "The normalized strict inequality, not a non-strict or reversed mutation."),
    row("M0767-B", "branch", "The contradiction route rules out every proposed reverse embedding.",
        "not (Cardinal.mk (Set s) <= Cardinal.mk s)", "Strictness after the forward singleton embedding.", risk="high", steps="split-required"),
    row("M0767-B-B1", "branch", "Assume a reverse injection from subsets to elements.",
        "f : Set beta -> beta; Function.Injective f", "The universally quantified counterexample input for diagonalization.", risk="high"),
    row("M0767-B-B2", "terminal", "Diagonalization contradicts injectivity of every map from Set beta to beta.",
        "Function.cantor_injective f : not Function.Injective f", "Contradiction closing the reverse-embedding branch.", risk="critical",
        provenance="mathlib:Function.cantor_injective@8a178386"),
    row("M0767-C", "construction", "Construct the forward embedding used by strict cardinal order.",
        "Function.Embedding singleton", "Cardinal.mk beta <= Cardinal.mk (Set beta).", risk="high", steps="split-required"),
    row("M0767-C-C1", "construction", "Send each element to its singleton subset.",
        "singleton : beta -> Set beta", "The forward powerset map."),
    row("M0767-C-C2", "core_lemma", "Singleton equality reflects equality of elements.",
        "singleton_eq_singleton_iff", "Injectivity of the singleton map."),
    row("M0767-L", "core_lemma", "Cantor diagonalization supplies the no-reverse-injection engine.",
        "Function.cantor_injective", "No injection Set beta -> beta.", risk="critical", steps="split-required"),
    row("M0767-L-L1", "construction", "Build the diagonal predicate associated with a proposed injection.",
        "fun a => {b | forall U, a = f U -> b in U}", "A right inverse candidate used to force surjectivity.", risk="high"),
    row("M0767-L-L2", "terminal", "Lawvere/Cantor self-reference forbids surjectivity onto Set beta.",
        "Function.cantor_surjective", "The terminal diagonal contradiction.", risk="critical",
        provenance="mathlib:Function.cantor_surjective@8a178386"),
    row("M0767-X", "bridge", "Audit every imported theorem and trust boundary used by the root.",
        "Pinned mathlib import/provenance package", "Eligible imported boundaries and trust records.", risk="critical", steps="split-required"),
    row("M0767-X-X1", "bridge", "The powerset normalization is pinned to its exact mathlib body and revision.",
        "Cardinal.mk_powerset", "Audited normalization boundary.", risk="high", provenance="mathlib:Cardinal.mk_powerset@8a178386"),
    row("M0767-X-X2", "bridge", "The central imported cardinal theorem is pinned and must receive node-scoped evidence.",
        "Cardinal.cantor : forall a, a < 2 ^ a", "Exact normalized Cantor conclusion.", risk="critical",
        body="mathlib:Cardinal.cantor:Order.lean:338-344:sha256-7a219ff0", provenance="mathlib:Cardinal.cantor@8a178386"),
    row("M0767-X-X3", "terminal", "Record the terminal diagonal declaration provenance.",
        "Function.cantor_surjective / Function.cantor_injective", "Provenance overlay only.", risk="high", machine="informational",
        human_source="not_applicable", readable="not_applicable", body="mathlib:Function.cantor-diagonal:Basic.lean:246-266:sha256-5dffbb69"),
    row("M0767-X-X4", "terminal", "Record transitive axioms and declaration closure.",
        "#print axioms plus transitive declaration graph", "Trust overlay only.", risk="critical", machine="informational",
        human_source="not_applicable", readable="not_applicable"),
    row("M0767-X-X5", "terminal", "Record pinned kernel, compiled imports, package lock, and reproducibility boundary.",
        "Lean 4.29.0 / mathlib 8a178386 TCB inventory", "Release-trust overlay only.", risk="critical", machine="informational",
        human_source="not_applicable", readable="not_applicable"),
    row("M0767-T", "terminal", "Compose normalization and the pinned Cantor theorem back to the canonical statement.",
        "CanonicalTarget", "Exact root theorem.", risk="critical", steps="split-required"),
    row("M0767-T-T1", "transport", "Rewrite the set powerset cardinal into the exponential form.",
        "rw [Cardinal.mk_powerset]", "Normalized goal for the imported cardinal theorem.", risk="high"),
    row("M0767-T-T2", "terminal", "Apply Cardinal.cantor at Cardinal.mk s and return the exact canonical conclusion.",
        "Stage1.THM_M_0767.AnchorAudit.mathlib_anchor", "The checked wrapper conclusion, pending proof-phase admission.", risk="critical",
        provenance="local-wrapper-to-mathlib:Cardinal.cantor"),
]

obligations = [x["registry"] for x in specs]
nodes = [x["node"] for x in specs]
ids = [x["obligation_id"] for x in obligations]
fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant",
          "machine_eligibility", "human_source_eligibility", "readable_eligibility",
          "risk_class", "exclusion_reason", "terminal_proof_body_id")
projection = [{k: x[k] for k in fields} for x in obligations]
denominator = hashlib.sha256(json.dumps(projection, sort_keys=True, separators=(",", ":")).encode()).hexdigest()

registry = {
    "schema_version": "stage1-obligation-registry/1.0",
    "item_id": ITEM,
    "theorem_id": "THM-M-0767",
    "registry_version": 1,
    "freeze_basis": "Exact statement and audited pinned anchors; eligibility assigned without admitting candidate proof closure.",
    "root_obligation_id": "M0767-ROOT",
    "frozen_denominators": {
        "inventory": ids,
        "required_machine": [x["obligation_id"] for x in obligations if x["machine_eligibility"] == "required"],
        "required_human_source": [x["obligation_id"] for x in obligations if x["human_source_eligibility"] == "required"],
        "required_readable": [x["obligation_id"] for x in obligations if x["readable_eligibility"] == "required"],
    },
    "denominator_sha256": denominator,
    "obligations": obligations,
    "status_boundary": "Frozen architecture only; all obligations remain open and no M0, AUDIT-Z, or THEOREM-Z is claimed.",
}

edges = {name: [] for name in ("proof", "refinement", "provenance", "evidence", "trust", "documentation", "workflow")}


def edge(graph, source, target, typ):
    eid = f"{graph.upper()}-{source}-{target}"
    edges[graph].append({"edge_id": eid, "from": source, "type": typ, "to": target})


edge("proof", "M0767-ROOT", "M0767-T", "proof_requires")
for child in ("M0767-T-T1", "M0767-T-T2"):
    edge("proof", "M0767-T", child, "proof_requires")
edge("proof", "M0767-T-T1", "M0767-N-N1", "proof_requires")
edge("proof", "M0767-T-T2", "M0767-X-X2", "proof_requires")
for parent, children in {
    "M0767-S": ["M0767-S-S1", "M0767-S-S2", "M0767-S-S3", "M0767-S-S4", "M0767-S-S5"],
    "M0767-N": ["M0767-N-N1", "M0767-N-N2"],
    "M0767-B": ["M0767-B-B1", "M0767-B-B2"],
    "M0767-C": ["M0767-C-C1", "M0767-C-C2"],
    "M0767-L": ["M0767-L-L1", "M0767-L-L2"],
    "M0767-X": ["M0767-X-X1", "M0767-X-X2", "M0767-X-X3", "M0767-X-X4", "M0767-X-X5"],
}.items():
    for child in children:
        edge("refinement", parent, child, "logical_decomposition")
for layer in ("M0767-S", "M0767-N", "M0767-B", "M0767-C", "M0767-L", "M0767-X"):
    edge("refinement", "M0767-ROOT", layer, "logical_decomposition")
for child in ("M0767-C", "M0767-B"):
    edge("refinement", "M0767-X-X2", child, "logical_decomposition")
edge("refinement", "M0767-B-B2", "M0767-L", "logical_decomposition")
edge("provenance", "M0767-X-X2", "M0767-X-X3", "provenance_of")
edge("provenance", "M0767-T-T2", "M0767-X-X2", "provenance_of")
edge("provenance", "M0767-N-N1", "M0767-X-X1", "provenance_of")
edge("trust", "M0767-X-X2", "M0767-X-X4", "trusts")
edge("trust", "M0767-X-X2", "M0767-X-X5", "trusts")
for layer in ("M0767-S", "M0767-N", "M0767-B", "M0767-C", "M0767-L", "M0767-X", "M0767-T"):
    edge("documentation", "M0767-ROOT", layer, "documents")
edge("workflow", "M0767-ROOT", "M0767-T", "workflow_depends_on")
edge("workflow", "M0767-T", "M0767-X", "workflow_depends_on")


def graph(rows):
    incoming, outgoing = {}, {}
    for x in rows:
        outgoing.setdefault(x["from"], []).append(x["edge_id"])
        incoming.setdefault(x["to"], []).append(x["edge_id"])
    return {"edges": rows, "out": outgoing, "in": incoming}


bundle = {
    "schema_version": "stage1-typed-graphs/1.0",
    "item_id": ITEM,
    "theorem_id": "THM-M-0767",
    "nodes": nodes,
    "graphs": {name: graph(rows) for name, rows in edges.items()},
    "closure_boundary": {
        "closed_obligations": [],
        "root_machine_debt": "M3",
        "theorem_complete": False,
        "remaining_root_cut_set": ["M0767-T-T1", "M0767-T-T2"],
        "reason": "Candidate wrapper exists, but proof-body admission, composition, trust, source, readability, and release evidence remain open.",
    },
}

(HERE / "obligation-registry.json").write_text(json.dumps(registry, indent=2) + "\n")
(HERE / "typed-graphs.json").write_text(json.dumps(bundle, indent=2) + "\n")
print(f"wrote {len(obligations)} obligations and {sum(map(len, edges.values()))} typed edges")
