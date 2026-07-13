#!/usr/bin/env python3
"""Deterministically build THM-M-0995 registry-v2 proof artifacts."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
TREE_ITEM = "S56-M-0995-OBLIGATION_TREE"
PROOF_ITEM = "S56-M-0995-PROOF"
PREFIX = "M0995-"
V1_DENOMINATOR = "40ec266a8614befd347bb0f00848703182aac04f6446a113a6a2e6b1a0348794"
V1_REGISTRY_SHA256 = "1150adeecf0ca78639706ee32c082dfebbbd58d576db1d17ca039852d0bce100"

# short id, kind, risk, description, formal target, H/M/R, budget
SPECS = [
    ("ROOT", "root", "critical", "Prove the exact frozen bounded-summand upper-tail Bernstein inequality.", "Stage1Instances.THM_M_0995.ObligationTree.Root", "H2", "M0-L", "R4", 8),
    ("S-EXACT", "definition", "high", "Preserve all frozen binders, hypotheses, event convention, constants, and totalized division boundaries.", "Stage1Instances.THM_M_0995.StatementShape", "H2", "M0-L", "R3", 12),
    ("L-EXP-REMAINDER", "core_lemma", "critical", "Bound exp(x)-1-x by the Bernstein geometric-series remainder whenever abs(x) is below the tilt barrier.", "Stage1Instances.THM_M_0995.ObligationTree.ExpRemainderPackage", "H2", "M0-L", "R4", 65),
    ("L-IND-MGF", "core_lemma", "critical", "Integrate the scalar remainder bound and use centering and variance to obtain each summand MGF estimate.", "Stage1Instances.THM_M_0995.ObligationTree.IndividualMGFPackage", "H2", "M0-L", "R4", 70),
    ("T-IND-MGF", "terminal", "high", "Compose the scalar exponential remainder into the exact individual-MGF package.", "Stage1Instances.THM_M_0995.ObligationTree.IndividualMGFAssemblyPackage", "H2", "M0-L", "R3", 12),
    ("L-PREFIX-MGF", "bridge", "critical", "Factor the MGF of the finite independent prefix into the product of its summand MGFs.", "Stage1Instances.THM_M_0995.ObligationTree.PrefixMGFPackage", "H2", "M0-L", "R4", 45),
    ("L-SUM-MGF", "bridge", "critical", "Combine individual MGF bounds and apply the variance budget to the finite sum.", "Stage1Instances.THM_M_0995.ObligationTree.SumMGFPackage", "H2", "M0-L", "R4", 45),
    ("T-SUM-MGF", "terminal", "high", "Compose the individual and finite-prefix MGF packages into the sum-MGF package.", "Stage1Instances.THM_M_0995.ObligationTree.SumMGFAssemblyPackage", "H2", "M0-L", "R3", 12),
    ("L-CHERNOFF", "bridge", "high", "Apply exponential Markov to the exact non-strict upper-tail event.", "Stage1Instances.THM_M_0995.ObligationTree.ChernoffPackage", "H2", "M0-L", "R3", 30),
    ("L-OPTIMIZE-POS", "core_lemma", "critical", "Choose the Bernstein tilt and verify admissibility and exponent algebra when the variance budget is positive.", "Stage1Instances.THM_M_0995.ObligationTree.PositiveVarianceOptimizePackage", "H2", "M0-L", "R4", 55),
    ("L-VAR-ZERO-AE", "core_lemma", "critical", "Use nonnegative variances, zero total variance, and centering to show the finite partial sum is zero almost everywhere.", "Stage1Instances.THM_M_0995.ObligationTree.VarianceZeroAEPackage", "H2", "M0-L", "R4", 45),
    ("B-ZERO-DENOM", "branch", "high", "Prove the totalized zero-denominator boundary by the probability-measure bound.", "Stage1Instances.THM_M_0995.ObligationTree.ZeroDenominatorPackage", "H2", "M0-L", "R3", 20),
    ("B-VAR-ZERO", "branch", "critical", "Handle zero variance, splitting threshold zero from the strictly positive null-tail event.", "Stage1Instances.THM_M_0995.ObligationTree.ZeroVariancePackage", "H2", "M0-L", "R4", 35),
    ("T-VAR-ZERO", "terminal", "high", "Compose the denominator boundary and almost-everywhere zero result into the zero-variance branch.", "Stage1Instances.THM_M_0995.ObligationTree.ZeroVarianceAssemblyPackage", "H2", "M0-L", "R3", 12),
    ("B-EMPTY", "branch", "medium", "Retain the empty-family case and its zero partial sum inside the exact root.", "Stage1Instances.THM_M_0995.emptyPartialSum", "H2", "M0-L", "R3", 20),
    ("T-ASSEMBLE-V2", "terminal", "critical", "Split exhaustively on zero versus positive variance and compose the corrected proof packages into the exact root.", "Stage1Instances.THM_M_0995.ObligationTree.AssemblyPackageV2", "H2", "M0-L", "R4", 35),
    ("X-MATHLIB", "provenance", "high", "Pin and audit the imported exponential-series, MGF, independence, Chernoff, and variance bodies.", "mathlib 8a178386: Probability.Moments.SubGaussian and transitive imports", "H2", "M2", "R3", 20),
    ("X-EXTERNAL", "provenance", "high", "Keep the mismatched HighDimProb Bernstein result isolated from proof credit.", "HighDimProb 8d4eec8: Concentration.Bernstein", "H2", "M5", "R4", 20),
    ("X-SOURCE", "source", "high", "Pinpoint a primary human theorem, assumptions, constants, proof crosswalk, and errata.", "primary source theorem/page open", "H2", "M5", "R4", 30),
    ("X-TCB", "trust", "high", "Audit the transitive kernel, dependency, axiom, executable, and computation boundary.", "Lean 4.29.0; mathlib 8a178386", "H2", "M3", "R4", 25),
    ("X-V1-REFUTATION", "certificate", "critical", "Preserve the kernel-checked counterexample that invalidated registry-v1's optimizer interface.", "Stage1Instances.THM_M_0995.Proof.not_optimizeExponentPackage", "H2", "M0-L", "R3", 10),
]


def oid(short):
    return PREFIX + short


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def graph(edges):
    outgoing, incoming = {}, {}
    for edge in edges:
        outgoing.setdefault(edge["from"], []).append(edge["edge_id"])
        incoming.setdefault(edge["to"], []).append(edge["edge_id"])
    return {"edges": edges, "out": outgoing, "in": incoming}


statement = json.loads((HERE / "statement.json").read_text())
expr_hash = statement["canonical_formal_target"]["elaborated_expression_sha256"]
overlays = {"X-MATHLIB", "X-EXTERNAL", "X-SOURCE", "X-TCB", "X-V1-REFUTATION"}
no_human = {"S-EXACT", "B-EMPTY", "X-TCB", "X-V1-REFUTATION"}
body_ids = {
    "ROOT": "Stage1Instances.THM_M_0995.Proof.bernsteinInequality_via_registry_v2",
    "L-EXP-REMAINDER": "Stage1Instances.THM_M_0995.Proof.exp_sub_one_sub_le_quadratic",
    "L-IND-MGF": "Stage1Instances.THM_M_0995.Proof.individualMGFPackage",
    "T-IND-MGF": "Stage1Instances.THM_M_0995.Proof.individualMGFAssemblyPackage",
    "L-PREFIX-MGF": "Stage1Instances.THM_M_0995.Proof.partialSum_mgf_eq_prod",
    "L-SUM-MGF": "Stage1Instances.THM_M_0995.Proof.sumMGFPackage",
    "T-SUM-MGF": "Stage1Instances.THM_M_0995.Proof.sumMGFAssemblyPackage",
    "L-CHERNOFF": "Stage1Instances.THM_M_0995.Proof.chernoffPackage",
    "L-OPTIMIZE-POS": "Stage1Instances.THM_M_0995.Proof.optimizeExponentPackage_of_pos",
    "L-VAR-ZERO-AE": "Stage1Instances.THM_M_0995.Proof.partialSum_ae_zero_of_varianceBudget_eq_zero",
    "B-ZERO-DENOM": "Stage1Instances.THM_M_0995.Proof.zeroDenominatorPackage",
    "B-VAR-ZERO": "Stage1Instances.THM_M_0995.Proof.zeroVariancePackage",
    "T-VAR-ZERO": "Stage1Instances.THM_M_0995.Proof.zeroVarianceAssemblyPackage",
    "B-EMPTY": "Stage1Instances.THM_M_0995.emptyPartialSum",
    "T-ASSEMBLE-V2": "Stage1Instances.THM_M_0995.Proof.assemblyPackageV2",
    "X-V1-REFUTATION": "Stage1Instances.THM_M_0995.Proof.not_optimizeExponentPackage",
}
v1_identity = {
    "L-IND-MGF": ("planned:v1:sha256:8eb3bda5a6931360db2c8ff0bda5454c4c7edc92ca60c26592b0030820ca5fde", "critical", None),
    "L-SUM-MGF": ("planned:v1:sha256:c2e3c848020eba7b635e2523ea97b5f7df301d554e0d9fa7a3d229f0b525d16c", "critical", None),
    "L-CHERNOFF": ("planned:v1:sha256:db78bc6d09fd49b3959fefbfa46de07544db777f7d9f829c6f161a00aa066087", "high", "mathlib:8a178386:ProbabilityTheory.measure_ge_le_exp_mul_mgf"),
    "B-ZERO-DENOM": ("planned:v1:sha256:7c85b3f942a2109128feac36ad56958369be8adfa16b2b8beeb60f4069351c7b", "critical", None),
    "B-EMPTY": ("planned:v1:sha256:3431851d351b3db3c97dea9e9652c34b8fc56c43a4ecf8728b4fa81514d8ef34", "medium", "repo:Stage1Instances.THM_M_0995.emptyPartialSum"),
    "X-MATHLIB": ("planned:v1:sha256:a04747e779915b7bbc5d9e36ac45fccaddd242473e81a0e951739537a3670416", "high", None),
    "X-EXTERNAL": ("planned:v1:sha256:165b0362dd4ed431c7ed5c563640e1cc8a3fa6550f4fa4b94c44e20a3f6c2846", "high", None),
    "X-SOURCE": ("planned:v1:sha256:e369ce3af96c4dd7ccd733a47c0062ed8a860aeade2e990c896e91f656fc66c9", "high", None),
    "X-TCB": ("planned:v1:sha256:97d1568040132d335bfc2b33b12d78d733208bf75f4c5435dfadc7c68e6c270b", "high", None),
}

rows = []
for short, kind, risk, desc, formal, _hd, _md, _rd, _budget in SPECS:
    fingerprint = ("lean-expression-sha256:" + expr_hash) if short in {"ROOT", "S-EXACT"} else (
        "planned:v2:sha256:" + hashlib.sha256((desc + "\n" + formal).encode()).hexdigest())
    stored_risk = risk
    stored_body = body_ids.get(short)
    if short in v1_identity:
        fingerprint, stored_risk, stored_body = v1_identity[short]
    rows.append({
        "obligation_id": oid(short), "statement_fingerprint": fingerprint, "kind": kind,
        "root_relevant": short not in overlays,
        "machine_eligibility": "informational" if short in overlays else "required",
        "human_source_eligibility": "not_applicable" if short in no_human else "required",
        "readable_eligibility": "required", "risk_class": stored_risk, "exclusion_reason": None,
        "terminal_proof_body_id": stored_body,
    })

fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility",
          "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason",
          "terminal_proof_body_id")
projection = [{key: row[key] for key in fields} for row in rows]
denominator = hashlib.sha256(json.dumps(projection, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
ids = [row["obligation_id"] for row in rows]

registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": TREE_ITEM,
    "theorem_id": "THM-M-0995", "registry_version": 2,
    "frozen_at": "2026-07-12T00:00:00+08:00",
    "amended_at": "2026-07-13T00:00:00+08:00",
    "freeze_basis": "Version 2 preserves the exact frozen statement and corrects only the proof architecture after registry-v1's optimizer was kernel-refuted at v=0, b=1, t=1.",
    "frozen_against_statement_sha256": sha256(HERE / "statement.json"),
    "frozen_against_anchor_audit_sha256": sha256(HERE / "anchor-audit.json"),
    "root_obligation_id": oid("ROOT"), "denominator_sha256": denominator,
    "registry_history": [{
        "registry_version": 1,
        "registry_sha256": V1_REGISTRY_SHA256,
        "denominator_sha256": V1_DENOMINATOR,
        "inventory": [oid(x) for x in ("ROOT", "S-EXACT", "L-IND-MGF", "L-SUM-MGF", "L-CHERNOFF", "L-OPTIMIZE", "B-ZERO-DENOM", "B-EMPTY", "T-ASSEMBLE", "X-MATHLIB", "X-EXTERNAL", "X-SOURCE", "X-TCB")],
        "supersession_reason": "M0995-L-OPTIMIZE was false on an allowed positive-denominator, zero-variance input; the root requires an explicit zero/positive variance split.",
    }],
    "append_only_delta": {
        "from_version": 1, "to_version": 2,
        "preserved_ids": [oid(x) for x in ("ROOT", "S-EXACT", "L-IND-MGF", "L-SUM-MGF", "L-CHERNOFF", "B-ZERO-DENOM", "B-EMPTY", "X-MATHLIB", "X-EXTERNAL", "X-SOURCE", "X-TCB")],
        "retired_ids": [{"obligation_id": oid("L-OPTIMIZE"), "reason": "false_interface_refuted_by_local_kernel_proof", "replacement_ids": [oid("L-OPTIMIZE-POS"), oid("L-VAR-ZERO-AE"), oid("B-VAR-ZERO"), oid("T-VAR-ZERO")]}],
        "replaced_ids": [{"old_id": oid("T-ASSEMBLE"), "new_id": oid("T-ASSEMBLE-V2"), "reason": "composition now consumes the exhaustive zero/positive variance branches"}],
        "added_ids": [oid(x) for x in ("L-EXP-REMAINDER", "T-IND-MGF", "L-PREFIX-MGF", "T-SUM-MGF", "L-OPTIMIZE-POS", "L-VAR-ZERO-AE", "B-VAR-ZERO", "T-VAR-ZERO", "X-V1-REFUTATION")],
        "eligibility_changes": [],
        "status_only_updates": [
            {"obligation_id": oid("ROOT"), "field": "terminal_proof_body_id", "old": None, "new": body_ids["ROOT"]},
            {"obligation_id": oid("L-IND-MGF"), "field": "proof_evidence", "old": "open", "new": body_ids["L-IND-MGF"]},
            {"obligation_id": oid("L-SUM-MGF"), "field": "proof_evidence", "old": "open", "new": body_ids["L-SUM-MGF"]},
            {"obligation_id": oid("L-CHERNOFF"), "field": "proof_evidence", "old": "anchor_only", "new": body_ids["L-CHERNOFF"]},
            {"obligation_id": oid("B-ZERO-DENOM"), "field": "proof_evidence", "old": "open", "new": body_ids["B-ZERO-DENOM"]},
        ],
    },
    "frozen_denominators": {
        "inventory": ids,
        "required_machine": [r["obligation_id"] for r in rows if r["machine_eligibility"] == "required"],
        "required_human_source": [r["obligation_id"] for r in rows if r["human_source_eligibility"] == "required"],
        "required_readable": ids,
        "informational_overlays": [r["obligation_id"] for r in rows if r["machine_eligibility"] == "informational"],
    },
    "delta_policy": "Any further correction, split, merge, eligibility, exclusion, risk, or proof-body identity change requires registry version 3 and another append-only delta; v1 and v2 denominators remain reportable.",
    "obligations": rows,
}

nodes = []
for spec, row in zip(SPECS, rows):
    short, kind, _risk, desc, formal, hd, md, rd, budget = spec
    nodes.append({
        "node_id": "THM-M-0995-" + short, "obligation_id": oid(short), "kind": kind,
        "human_statement": desc, "formal_target": formal, "output": desc,
        "human_debt": hd, "machine_debt": md, "readability_debt": rd,
        "evidence_ids": ["S56-M-0995-PROOF-local-20260714"] if short not in overlays else [],
        "source_crosswalk_id": "SRC-M0995-PRIMARY-OPEN" if row["human_source_eligibility"] == "required" else "not-applicable",
        "provenance_id": "PROV-M0995-MATHLIB" if short in {"L-EXP-REMAINDER", "L-PREFIX-MGF", "L-CHERNOFF", "X-MATHLIB"} else ("PROV-M0995-HIGHDIMPROB-NONEXACT" if short == "X-EXTERNAL" else "local-proof-v2"),
        "foundation_profile": "Lean 4 kernel plus pinned mathlib; observed axioms: propext, Classical.choice, Quot.sound",
        "tcb_profile": "Lean 4.29.0 (98dc76e); mathlib 8a178386; release-grade transitive audit open",
        "computation_record": "none", "step_budget": budget,
        "semantic_step_ledger": {"premises": ["exact typed children in registry-v2 proof graph"], "inference": formal, "output": desc, "outgoing_use": "typed parent edge or exact root"},
        "public_readable_target": "Stage1_Instances/THM-M-0995/obligation-tree.md#" + short.lower(),
        "validation_spec_id": "VAL-M0995-" + short,
        "status_boundary": "Proof-phase kernel closure is provisional; source/readability/trust/validation/release gates remain open.",
        "task_ids": [TREE_ITEM, PROOF_ITEM],
        "owned_sources": ["Stage1_Instances/THM-M-0995/ObligationTree.lean", "Stage1_Instances/THM-M-0995/Proof.lean"],
        "owner": "Stage1 execution worker", "reviewer": "independent integration lane",
        "validity": {"validated_at": "2026-07-13", "review_due": "before master acceptance", "invalidation_inputs": ["statement", "registry", "proof source", "toolchain", "mathlib revision", "anchor provenance"], "revocation_state": "not-accepted"},
    })

proof_pairs = [
    ("ROOT", "L-SUM-MGF"), ("ROOT", "L-CHERNOFF"),
    ("ROOT", "L-OPTIMIZE-POS"), ("ROOT", "B-VAR-ZERO"),
    ("ROOT", "T-ASSEMBLE-V2"),
    ("L-IND-MGF", "L-EXP-REMAINDER"), ("L-IND-MGF", "T-IND-MGF"),
    ("L-SUM-MGF", "L-IND-MGF"), ("L-SUM-MGF", "L-PREFIX-MGF"),
    ("L-SUM-MGF", "T-SUM-MGF"),
    ("B-VAR-ZERO", "B-ZERO-DENOM"), ("B-VAR-ZERO", "L-VAR-ZERO-AE"),
    ("B-VAR-ZERO", "T-VAR-ZERO"),
]
proof_edges = []
for parent, child in proof_pairs:
    forward, reverse = f"PROOF-{parent}-{child}", f"COMPOSE-{child}-{parent}"
    proof_edges += [
        {"edge_id": forward, "from": oid(parent), "type": "proof_requires", "to": oid(child), "reciprocal_edge_id": reverse},
        {"edge_id": reverse, "from": oid(child), "type": "composes", "to": oid(parent), "reciprocal_edge_id": forward},
    ]

graphs = {
    "proof": graph(proof_edges),
    "refinement": graph([
        {"edge_id": "REFINE-ROOT-EXACT", "from": oid("ROOT"), "type": "logical_decomposition", "to": oid("S-EXACT")},
        {"edge_id": "REFINE-EXACT-EMPTY", "from": oid("S-EXACT"), "type": "logical_decomposition", "to": oid("B-EMPTY")},
    ]),
    "provenance": graph([
        {"edge_id": "PROV-EXP-MATHLIB", "from": oid("L-EXP-REMAINDER"), "type": "provenance_of", "to": oid("X-MATHLIB")},
        {"edge_id": "PROV-PREFIX-MATHLIB", "from": oid("L-PREFIX-MGF"), "type": "provenance_of", "to": oid("X-MATHLIB")},
        {"edge_id": "PROV-CHERNOFF-MATHLIB", "from": oid("L-CHERNOFF"), "type": "provenance_of", "to": oid("X-MATHLIB")},
        {"edge_id": "PROV-ROOT-EXTERNAL", "from": oid("ROOT"), "type": "provenance_of", "to": oid("X-EXTERNAL")},
        {"edge_id": "SOURCE-ROOT", "from": oid("ROOT"), "type": "source_map", "to": oid("X-SOURCE")},
    ]),
    "evidence": graph([
        {"edge_id": "EVID-ROOT-MATHLIB", "from": oid("ROOT"), "type": "evidence_for", "to": oid("X-MATHLIB")},
        {"edge_id": "EVID-V1-REFUTATION", "from": oid("X-V1-REFUTATION"), "type": "evidence_for", "to": oid("L-OPTIMIZE-POS")},
    ]),
    "trust": graph([{ "edge_id": "TRUST-ROOT-TCB", "from": oid("ROOT"), "type": "trusts", "to": oid("X-TCB")}]),
    "documentation": graph([{ "edge_id": "DOC-ROOT-SOURCE", "from": oid("ROOT"), "type": "documents", "to": oid("X-SOURCE")}]),
    "workflow": graph([
        {"edge_id": "FLOW-ROOT-ASSEMBLE", "from": oid("ROOT"), "type": "workflow_depends_on", "to": oid("T-ASSEMBLE-V2")},
        {"edge_id": "FLOW-ASSEMBLE-MATHLIB", "from": oid("T-ASSEMBLE-V2"), "type": "workflow_depends_on", "to": oid("X-MATHLIB")},
    ]),
}

closed = [r["obligation_id"] for r in rows if r["machine_eligibility"] == "required"]
bundle = {
    "schema_version": "stage1-typed-graphs/1.0", "item_id": TREE_ITEM, "theorem_id": "THM-M-0995",
    "registry_version": 2, "registry_denominator_sha256": denominator, "nodes": nodes, "graphs": graphs,
    "closure_boundary": {
        "closed_obligations": closed, "root_closed": True, "root_machine_debt": "M0-L",
        "remaining_root_cut_set": [],
        "composition_certificates_checked": [
            "Stage1Instances.THM_M_0995.ObligationTree.individualMGF_compose",
            "Stage1Instances.THM_M_0995.ObligationTree.sumMGF_compose",
            "Stage1Instances.THM_M_0995.ObligationTree.zeroVariance_compose",
            "Stage1Instances.THM_M_0995.ObligationTree.root_compose_v2",
        ],
        "refinement_certificates_checked": [
            "Stage1Instances.THM_M_0995.statementShape_iff_expandedSourceShape",
            "Stage1Instances.THM_M_0995.emptyPartialSum",
        ],
        "audit_complete": False, "theorem_complete": False,
        "status_boundary": "Exact root machine closure is provisional at proof phase; H0, R0, transitive trust, hermetic validation, independent replay, release, and master acceptance remain open.",
    },
}

recipes = []
declarations = dict(body_ids)
declarations["S-EXACT"] = "Stage1Instances.THM_M_0995.statementShape_iff_expandedSourceShape"
for spec in SPECS:
    short = spec[0]
    recipes.append({
        "recipe_id": "VAL-M0995-" + short,
        "cwd": "Stage1_Instances/THM-M-0995",
        "argv": ["bash", "check_proof.sh"],
        "env_allowlist": {"ELAN_TOOLCHAIN": "leanprover/lean4:v4.29.0"},
        "timeout_seconds": 300, "network_policy": "denied", "expected_exit": 0,
        "expected_outputs": [{"path_or_stream": "stdout", "semantic_hash_policy": "exact declarations and axiom reports are parsed by the proof-phase runner"}],
        "covered_obligation_ids": [oid(short)],
        "covered_declarations": [declarations[short]] if short in declarations else [],
        "support_boundary": "proof_elaboration" if short not in overlays else "informational_overlay_not_proof_closure",
    })
validation = {"schema_version": "stage1-validation-specs/1.0", "item_id": TREE_ITEM,
              "theorem_id": "THM-M-0995", "registry_version": 2,
              "registry_denominator_sha256": denominator, "recipes": recipes}

for name, value in (("obligation-registry.json", registry), ("typed-graphs.json", bundle),
                    ("validation-specs.json", validation)):
    (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n")

print(f"wrote registry v2: {len(rows)} obligations, {sum(len(g['edges']) for g in graphs.values())} typed edges")
print(f"registry v1 denominator retained: {V1_DENOMINATOR}")
print(f"registry v2 denominator sha256: {denominator}")
