#!/usr/bin/env python3
"""Build the frozen THM-M-0070 obligation registry and typed graph bundle."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ITEM = "S56-M-0070-OBLIGATION_TREE"
THEOREM = "THM-M-0070"
PREFIX = "M0070-"
ROOT_EXPRESSION = "51024e84c9b068a6de27ff2d3ba0f1e479c02dfd36d8072f3d243d46f3324c93"
COQ_REVISION = "6afa795b9018c64ab5c7cd2f9b3c9ab5dd45d93f"
COQ_TREE = "0ddbbe81c42419e179d75d4baaea800b601ccf73"
COQ_ARCHIVE_SHA256 = "c0287e97d56c5003745271b4aeaec0d4bd291d41c0f803f9c78a7c680b877dd3"
LEAN_PLACEHOLDER_REVISION = "0f4a5daeaf6f26efd5af808ecd05e4744d8a2924"
GRAPH_NAMES = (
    "proof", "refinement", "provenance", "evidence", "trust", "documentation", "workflow"
)


def oid(short: str) -> str:
    return PREFIX + short


def digest(value: object) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode()
    return hashlib.sha256(payload).hexdigest()


def architecture_rows() -> list[dict]:
    rows: list[dict] = []

    def add(short: str, kind: str, risk: str, claim: str, formal: str, output: str,
            budget: int, machine: str = "required", human: str = "required",
            terminal: str | None = None, package: bool = False) -> None:
        rows.append({
            "short": short,
            "kind": kind,
            "risk": risk,
            "claim": claim,
            "formal": formal,
            "output": output,
            "budget": budget,
            "machine": machine,
            "human": human,
            "terminal": terminal,
            "package": package,
        })

    add("ROOT", "root", "critical",
        "Every finite multiplicative group whose natural-number cardinality is odd is solvable.",
        "Stage1Instances.THM_M_0070.OddOrderSolvabilityTarget",
        "The exact frozen finite odd-order solvability proposition.", 8)
    add("S-INTERFACE", "definition", "critical",
        "Preserve the universe, Group and Finite binders, Nat.card oddness premise, and IsSolvable conclusion in their frozen order.",
        "Stage1Instances.THM_M_0070.OddOrderSolvabilityTarget",
        "The exact formal context and conclusion without a special-group restriction.", 16,
        human="not_applicable")
    add("S-BOUNDARY", "branch", "high",
        "Include the trivial group and all finite noncommutative odd-order groups while excluding no odd cardinality and adding no nontriviality premise.",
        "Statement.lean boundary witnesses and four mutation classes",
        "The complete source-faithful degenerate and domain boundary policy.", 20,
        human="not_applicable")
    add("S-ENCODINGS", "transport", "high",
        "Relate Finite/Nat.card to Fintype.card, Odd to congruence modulo two, and IsSolvable to eventual triviality of the derived series.",
        "oddOrderSolvabilityTarget_iff_fintypeCardTarget; oddOrderSolvabilityTarget_iff_modTwoTarget; oddOrderSolvabilityTarget_iff_derivedSeriesTarget",
        "Three checked bidirectional encoding transports.", 18, human="not_applicable",
        terminal="repo:Statement.lean#three-checked-transports")
    add("S-FOUNDATION", "certificate", "critical",
        "Fix the Lean kernel, classical choice, quotient, extensionality, import, computation, and accepted TCB policies for any terminal translation.",
        "planned transitive Lean foundation and TCB certificate",
        "A release-grade foundation decision without mathematical proof credit.", 40,
        machine="informational", human="not_applicable")
    add("N-MINIMAL-INDUCTION", "normalization", "critical",
        "Reduce a hypothetical nonsolvable odd-order finite group by well-founded induction on cardinality to a minimal simple odd-order counterexample.",
        "Coq:BGsection7.minSimpleOdd_ind (planned Lean translation)",
        "A minimal-simple-odd-group context or solvability of the original group.", 96,
        terminal="coq:BGsection7.minSimpleOdd_ind", package=True)
    add("B-MINIMAL-COUNTEREXAMPLE", "branch", "critical",
        "Separate the induction branch already closed by proper odd-order sections from the minimal nonsolvable simple counterexample branch.",
        "planned exhaustive branch theorem around minSimpleOdd_ind",
        "Exhaustive induction branches with the minimal branch isolated.", 82, package=True)
    add("C-MINIMAL-SIMPLE", "construction", "critical",
        "Package the carrier, odd order, nonsolvability, simplicity, and strict-cardinality induction hypotheses of a minimal counterexample.",
        "Coq:minSimpleOddGroupType and TheMinSimpleOddGroup (planned Lean structure)",
        "A well-formed minimal-simple odd group context used by local and character analysis.", 94,
        terminal="coq:minSimpleOddGroupType", package=True)
    add("L-NO-MINIMAL", "core_lemma", "critical",
        "Derive a contradiction from every minimal simple odd-order group by combining Bender-Glauberman local analysis with Peterfalvi character theory.",
        "Coq:PFsection14.no_minSimple_odd_group (planned Lean translation)",
        "False in the minimal-simple-odd-group context.", 98,
        terminal="coq:PFsection14.no_minSimple_odd_group", package=True)
    add("B-TYPE-PAIR", "branch", "critical",
        "Split the final minimal-group analysis between the all-type-I alternative and the existence of a paired type-P configuration S,T.",
        "Coq:PFsection14.no_minSimple_odd_group case split via FTtypeP_pair_cases",
        "An exhaustive final structural alternative.", 72, package=True)
    add("B-ALL-TYPE1", "branch", "critical",
        "Contradict the alternative that every maximal subgroup lies in the type-I configuration.",
        "Coq:PFsection14.not_all_FTtype1",
        "False for the all-type-I branch.", 86, terminal="coq:PFsection14.not_all_FTtype1",
        package=True)
    add("B-TYPE2-EXCLUSION", "branch", "critical",
        "For a paired S,T configuration, derive the type-II structure and exclude it through support coherence and the final character contradiction.",
        "Coq:PFsection14.FTtype2_exclusion",
        "False for the paired type-P branch.", 98,
        terminal="coq:PFsection14.FTtype2_exclusion", package=True)
    add("C-LOCAL-CONTEXT", "construction", "critical",
        "Construct the maximal-subgroup types, Fitting cores, complements, TI sets, and local configurations used by the final contradiction.",
        "Coq:BGsection10-16 local-analysis contexts (planned Lean structures)",
        "The complete local finite-group data consumed by Peterfalvi sections 8-14.", 96,
        package=True)
    add("C-CHARACTER-CONTEXT", "construction", "critical",
        "Construct class-function supports, Dade and cyclic-TI isometries, coherence data, and integral character expansions.",
        "Coq:PFsection1-7 character-theory contexts (planned Lean structures)",
        "The character-theoretic data and invariants consumed by the final sections.", 98,
        package=True)
    add("T-COQ-CAPSTONE", "terminal", "critical",
        "Compose minimal-counterexample induction with nonexistence of a minimal simple odd-order group to obtain the MathComp theorem.",
        "Coq:odd_order.PFsection14.Feit_Thompson",
        "The exact Coq/MathComp odd-order solvability conclusion.", 12,
        terminal="coq:PFsection14.Feit_Thompson")
    add("X-LEAN-BODY", "bridge", "critical",
        "Implement or approve a semantics-preserving placeholder-free Lean body for the exact frozen root; the Coq source alone cannot inhabit this obligation.",
        "Stage1Instances.THM_M_0070.ObligationTree.TranslatedOddOrderBody",
        "An authorized Lean kernel term of the exact translated-body type.", 30)
    add("X-COQ-SOURCE", "bridge", "critical",
        "Reproduce and audit the immutable MathComp odd-order source and use it only as an architecture/provenance input until an approved Lean bridge exists.",
        f"math-comp/odd-order@{COQ_REVISION}:PFsection14.Feit_Thompson",
        "A checked other-prover source record with no Lean proof credit.", 48,
        machine="informational", terminal="coq:PFsection14.Feit_Thompson", package=True)
    add("X-LEAN-PLACEHOLDER", "bridge", "critical",
        "Track the exact external Lean statement as rejected until its terminal body is not a placeholder and compatible pins are integrated.",
        f"ianklatzco/odd-order-lean@{LEAN_PLACEHOLDER_REVISION}:odd_order_solvable",
        "A rejection boundary; never a proof premise or numerator.", 18,
        machine="informational", human="not_applicable")
    add("T-ADAPTER", "terminal", "critical",
        "Consume the exact translated Lean body without weakening, strengthening, or changing an encoding.",
        "Stage1Instances.THM_M_0070.ObligationTree.target_of_translatedOddOrderBody",
        "The exact canonical target as a conditional conclusion.", 4, human="not_applicable",
        terminal="repo:ObligationTree.lean#target_of_translatedOddOrderBody")
    add("T-ROOT", "terminal", "critical",
        "Consume the exact adapter output and return the complete frozen root.",
        "Stage1Instances.THM_M_0070.ObligationTree.terminalTarget_of_target",
        "The complete root conclusion with no added premise beyond the open body child.", 4,
        human="not_applicable", terminal="repo:ObligationTree.lean#terminalTarget_of_target")

    infrastructure = [
        ("I-SOLVABLE-GROUP", "Solvable-group infrastructure: Hall subgroups, pi-cores, coprime action, Fitting theory, chief factors, and minimal-normal elementary-abelian structure.", "planned Lean Layer 0a; Coq/MathComp finite-group substrate", "The finite solvable-group and local-analysis substrate required by BG sections.", 96),
        ("I-CHARACTER", "Arithmetic character infrastructure: class functions, orthogonality, induction, integrality, virtual characters, isometries, inertia, and Galois action.", "planned Lean Layer 0b; Coq/MathComp character substrate", "The ordinary and virtual character-theory substrate required by PF sections.", 98),
        ("I-FROBENIUS-WIELANDT", "Frobenius-group structure, kernel results, semiregularity, and the Wielandt fixed-point order formula.", "Coq:wielandt_fixpoint plus Frobenius substrate (planned Lean translation)", "The Frobenius and fixed-point engines shared by BG and PF analysis.", 96),
    ]
    for short, claim, formal, output, budget in infrastructure:
        add(short, "bridge", "critical", claim, formal, output, budget, package=True)

    bg_descriptions = {
        "1": "p-length, p-stability, p-constraint, Puig series, and finite-group local-analysis definitions",
        "2": "odd-order linear groups and the GL(2,p) representation bounds",
        "3": "Frobenius, Wielandt, regular-action, and metacyclic local structure",
        "4": "rank-two p-group and elementary-abelian local structure",
        "5": "narrow p-groups and their characteristic subgroups",
        "6": "factorization and transitivity inputs for the uniqueness analysis",
        "7": "minimal-simple-odd framework and Thompson transitivity",
        "8": "first uniqueness theorem for maximal local configurations",
        "9": "the uniqueness theorem chapter and its conjugacy consequences",
        "10": "sigma, alpha, beta, uniqueness, and maximal-subgroup machinery",
        "11": "the kappa-family hypotheses and structural consequences",
        "12": "type-F complements and the main local classification engine",
        "13": "prime and regular actions used by later maximal-subgroup types",
        "14": "kappa-complement structure and the section-14 local analysis",
        "15": "corrected local structure theorems feeding the final type classification",
        "16": "type F/P/P1/P2 and type I-V interface consumed by Peterfalvi analysis",
    }
    for section, description in bg_descriptions.items():
        add(f"BG-{section}", "bridge", "critical",
            f"Translate and compose Bender-Glauberman section {section}: {description}.",
            f"Coq:BGsection{section}.v theorem package (planned Lean translation)",
            f"The reviewed section-{section} interface required by its downstream BG/PF consumers.",
            98, terminal=f"coq-package:BGsection{section}.v", package=True)
    add("BG-APPENDIX-AB", "bridge", "critical",
        "Translate p-stability and the Puig ZL-theorem from Bender-Glauberman appendices A and B.",
        "Coq:BGappendixAB.v theorem package", "The p-stability and Puig-factorization interface.",
        98, terminal="coq-package:BGappendixAB.v", package=True)
    add("BG-APPENDIX-C", "bridge", "critical",
        "Translate the finite-field norm and character estimate of Appendix C used only in Peterfalvi theorem 14.2.",
        "Coq:BGappendixC.prime_dim_normed_finField",
        "The arithmetic inequality excluding the final Galois configuration.", 98,
        terminal="coq:BGappendixC.prime_dim_normed_finField", package=True)

    pf_descriptions = {
        "1": "preliminary virtual-character, algebraic-integer, and automorphism results",
        "2": "the Dade isometry and reciprocity",
        "3": "cyclic-normalizer TI subsets and their isometry",
        "4": "the Dade isometry for the prime-TI subgroup configuration",
        "5": "the coherence framework for induced-character families",
        "6": "Sibley coherence and supporting estimates",
        "7": "inverse Dade and nonexistence of the preliminary odd-order configuration",
        "8": "FT-Dade instances and the bridge from BG type definitions",
        "9": "maximal subgroups of types II, III, and IV",
        "10": "noncoherence and exclusion of type V",
        "11": "precise structure of maximal subgroups of types III and IV",
        "12": "type-I Frobenius structure and coherence consequences",
        "13": "the paired subgroups S and T and their symmetric character data",
        "14": "nonexistence of the minimal simple odd group and the final contradiction",
    }
    for section, description in pf_descriptions.items():
        add(f"PF-{section}", "bridge", "critical",
            f"Translate and compose Peterfalvi section {section}: {description}.",
            f"Coq:PFsection{section}.v theorem package (planned Lean translation)",
            f"The reviewed section-{section} interface required by its downstream PF consumers.",
            98, terminal=f"coq-package:PFsection{section}.v", package=True)

    overlays = [
        ("X-SOURCE", "source_boundary", "Pinpoint every obligation to the complete Feit-Thompson, Bender-Glauberman, Peterfalvi, and formal-source proof boundaries, corrections, and errata.", "planned primary-source and formal-source crosswalk", "An independently accepted H0 node map.", "not_applicable", "required", 98),
        ("X-PROVENANCE", "certificate", "Freeze every wrapper, terminal declaration, proof body, source blob, revision, dependency, and alias without duplicate credit.", "planned body-level provenance closure", "Complete transitive declaration and proof-body provenance.", "informational", "not_applicable", 92),
        ("X-TRUST", "certificate", "Audit Lean and any supporting Coq kernels, axioms, artifacts, dependencies, unsafe/oracle boundaries, supply chain, and replay transitively.", "planned transitive trust closure", "An accepted cross-system trust and TCB decision.", "informational", "not_applicable", 94),
        ("X-LICENSE", "certificate", "Verify CeCILL-B, Apache-2.0, mathlib, and every transitive source license and redistribution boundary.", "planned license and SBOM packet", "An accepted supply-chain license decision.", "informational", "not_applicable", 30),
        ("X-READABLE", "certificate", "Produce a complete independently reviewed readable reconstruction aligned with every high-risk local and character-theory package.", "planned long readable proof and review", "R0 coverage of the exact obligation denominator.", "informational", "required", 98),
        ("X-WORKFLOW", "certificate", "Bind proof, validation, freshness, revocation, independent verification, deterministic evidence, and release receipts.", "planned rev-5.6 workflow evidence", "A dependency-legal release decision without mathematical proof credit.", "informational", "not_applicable", 56),
    ]
    for short, kind, claim, formal, output, machine, human, budget in overlays:
        add(short, kind, "critical", claim, formal, output, budget, machine=machine, human=human,
            package=short in {"X-SOURCE", "X-READABLE"})
    return rows


PROOF_REQUIRES = {
    oid("ROOT"): [oid("T-ROOT")],
    oid("T-ROOT"): [oid("T-ADAPTER")],
    oid("T-ADAPTER"): [oid("X-LEAN-BODY")],
}


def refinement_map() -> dict[str, list[str]]:
    mapping: dict[str, list[str]] = {
        oid("ROOT"): [oid("S-INTERFACE"), oid("S-BOUNDARY"), oid("S-ENCODINGS"),
                      oid("S-FOUNDATION"), oid("T-ROOT"), oid("X-COQ-SOURCE")],
        oid("X-COQ-SOURCE"): [oid("T-COQ-CAPSTONE")],
        oid("T-COQ-CAPSTONE"): [oid("N-MINIMAL-INDUCTION"), oid("L-NO-MINIMAL")],
        oid("N-MINIMAL-INDUCTION"): [oid("B-MINIMAL-COUNTEREXAMPLE"), oid("C-MINIMAL-SIMPLE"), oid("BG-7")],
        oid("L-NO-MINIMAL"): [oid("B-TYPE-PAIR"), oid("C-LOCAL-CONTEXT"),
                              oid("C-CHARACTER-CONTEXT"), oid("PF-14")],
        oid("B-TYPE-PAIR"): [oid("B-ALL-TYPE1"), oid("B-TYPE2-EXCLUSION")],
        oid("B-TYPE2-EXCLUSION"): [oid("PF-14")],
        oid("C-LOCAL-CONTEXT"): [oid("BG-16")],
        oid("C-CHARACTER-CONTEXT"): [oid("PF-7")],
        oid("PF-14"): [oid("PF-13"), oid("BG-APPENDIX-C")],
        oid("PF-8"): [oid("PF-7"), oid("BG-16")],
        oid("PF-1"): [oid("I-CHARACTER")],
        oid("BG-16"): [oid("BG-15")],
        oid("BG-7"): [oid("BG-6"), oid("I-SOLVABLE-GROUP")],
        oid("BG-6"): [oid("BG-5"), oid("BG-APPENDIX-AB")],
        oid("BG-3"): [oid("BG-2"), oid("I-FROBENIUS-WIELANDT")],
        oid("BG-2"): [oid("BG-1"), oid("I-CHARACTER")],
        oid("BG-1"): [oid("I-SOLVABLE-GROUP")],
        oid("I-FROBENIUS-WIELANDT"): [oid("I-SOLVABLE-GROUP"), oid("I-CHARACTER")],
    }
    for n in range(14, 8, -1):
        mapping.setdefault(oid(f"PF-{n}"), []).append(oid(f"PF-{n - 1}"))
    mapping.setdefault(oid("PF-9"), []).extend([oid("PF-8"), oid("I-FROBENIUS-WIELANDT")])
    for n in range(7, 1, -1):
        mapping.setdefault(oid(f"PF-{n}"), []).append(oid(f"PF-{n - 1}"))
    for n in range(15, 7, -1):
        mapping.setdefault(oid(f"BG-{n}"), []).append(oid(f"BG-{n - 1}"))
    mapping.setdefault(oid("BG-8"), []).append(oid("BG-7"))
    for n in range(6, 3, -1):
        mapping.setdefault(oid(f"BG-{n}"), []).append(oid(f"BG-{n - 1}"))
    mapping.setdefault(oid("BG-4"), []).append(oid("BG-3"))
    mapping = {parent: list(dict.fromkeys(children)) for parent, children in mapping.items()}
    return mapping


def build() -> tuple[dict, dict, dict, str]:
    rows = architecture_rows()
    source_index = json.loads((HERE / "source-obligation-index.json").read_text(encoding="utf-8"))
    source_entries = source_index["entries"]
    statement_hash = hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest()
    anchor_hash = hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest()
    refinement = refinement_map()
    outgoing_uses: dict[str, list[str]] = {oid(row["short"]): [] for row in rows}
    for parent, children in {**refinement, **PROOF_REQUIRES}.items():
        for child in children:
            outgoing_uses[child].append(parent)
    declared_children = {
        identifier: sorted(set(refinement.get(identifier, []) + PROOF_REQUIRES.get(identifier, [])))
        for identifier in outgoing_uses
    }

    checked = {oid("S-INTERFACE"), oid("S-BOUNDARY"), oid("S-ENCODINGS"),
               oid("T-ADAPTER"), oid("T-ROOT")}
    obligations: list[dict] = []
    nodes: list[dict] = []
    for row in rows:
        identifier = oid(row["short"])
        excluded = row["machine"] != "required" or row["human"] != "required"
        registry_kind = {
            "normalization": "reduction", "bridge": "lemma", "core_lemma": "lemma",
            "certificate": "lemma", "source_boundary": "lemma",
        }.get(row["kind"], row["kind"])
        fingerprint = (f"lean-expression-sha256:{ROOT_EXPRESSION}"
                       if row["short"] in {"ROOT", "S-INTERFACE"}
                       else f"planned:v1:sha256:{digest({'claim': row['claim'], 'formal': row['formal']})}")
        exclusion = None
        if excluded:
            exclusion = "architecture_support_or_nonmathematical_boundary_pending_independent_approval"
        obligations.append({
            "obligation_id": identifier,
            "statement_fingerprint": fingerprint,
            "kind": registry_kind,
            "root_relevant": True,
            "machine_eligibility": row["machine"],
            "human_source_eligibility": row["human"],
            "readable_eligibility": "required",
            "risk_class": row["risk"],
            "exclusion_reason": exclusion,
            "terminal_proof_body_id": row["terminal"],
        })
        if row["short"] == "X-LEAN-PLACEHOLDER":
            machine_debt = "M5"
        elif identifier in checked:
            machine_debt = "M0-L"
        elif row["short"] in {"ROOT", "X-LEAN-BODY", "X-COQ-SOURCE", "T-COQ-CAPSTONE"}:
            machine_debt = "M3"
        else:
            machine_debt = "M4"
        uses = outgoing_uses[identifier] or ["release or independent review gate"]
        step = {
            "step_id": f"{identifier}-STEP-01",
            "premise_ids": declared_children[identifier] or ["EXACT-FROZEN-CONTEXT"],
            "inference_or_boundary": row["formal"],
            "output_claim": row["output"],
            "outgoing_use_ids": uses,
        }
        provenance = "none"
        if row["short"] == "X-LEAN-PLACEHOLDER":
            provenance = "anchor-audit:M0070-C05-ODD-ORDER-LEAN-PLACEHOLDER"
        elif row["short"] == "X-COQ-SOURCE" or row["short"].startswith(("BG-", "PF-")):
            provenance = "anchor-audit:M0070-C06-MATHCOMP-ODD-ORDER-COQ"
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
            "source_crosswalk_id": ("primary-and-formal-source-node-map-pending"
                                    if row["human"] == "required" else "not-applicable-pending-review"),
            "provenance_id": provenance,
            "foundation_profile": "lean4-dependent-type-theory; accepted cross-system policy and transitive review pending",
            "tcb_profile": "lean-4.29.0+mathlib-8a178386; Coq source is outside the Lean TCB; full closure pending",
            "computation_record": "none; no reflection, native computation, solver, oracle, experiment, or unchecked certificate is credited",
            "step_budget": row["budget"],
            "semantic_step_ledger": {
                "premises": step["premise_ids"],
                "inference": row["formal"],
                "output": row["output"],
                "outgoing_use": uses,
                "steps": [step],
                "package_expansion_state": ("split_required_before_proof_acceptance"
                                            if row["package"] else "locally_bounded"),
            },
            "public_readable_target": f"Stage1_Instances/{THEOREM}/obligation-tree.md#{identifier.lower()}",
            "validation_spec_id": f"VAL-{identifier}",
            "status_boundary": "Frozen architecture or conditionally checked interface only; no external body, accepted root proof, H0, R0, or theorem completion.",
            "task_ids": [ITEM, "S56-M-0070-PROOF"],
            "owned_sources": ([f"Stage1_Instances/{THEOREM}/ObligationTree.lean"] if identifier in checked
                              else [f"Stage1_Instances/{THEOREM}/obligation-tree.md"]),
            "owner": "THM-M-0070 proof lane",
            "reviewer": "independent Stage1 integration lane",
            "validity": {
                "validated_at": "2026-07-13" if identifier in checked else None,
                "review_due": "before proof acceptance",
                "invalidation_inputs": ["Statement.lean", "anchor-audit.json", "obligation-registry.json",
                                        "typed-graphs.json", "external source revisions", "toolchain and dependency pins"],
                "revocation_state": "provisional_interface_check" if identifier in checked else "open",
            },
        })

    fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant",
              "machine_eligibility", "human_source_eligibility", "readable_eligibility",
              "risk_class", "exclusion_reason", "terminal_proof_body_id")
    denominator = digest([{field: row[field] for field in fields} for row in obligations])
    ids = [row["obligation_id"] for row in obligations]
    registry = {
        "schema_version": "stage1-obligation-registry/1.0",
        "item_id": ITEM,
        "theorem_id": THEOREM,
        "registry_id": "THM-M-0070-OBLIGATIONS-v1",
        "registry_version": 1,
        "frozen_at": "2026-07-13T00:00:00+08:00",
        "freeze_basis": "The exact frozen statement, completed immutable candidate inventory, official MathComp terminal body, transitive source package structure, and audited port roadmap. Eligibility and denominators are independent of closure status.",
        "frozen_against_statement_sha256": statement_hash,
        "frozen_against_anchor_audit_sha256": anchor_hash,
        "selected_architecture_source_revision": COQ_REVISION,
        "selected_architecture_source_tree": COQ_TREE,
        "selected_architecture_source_archive_sha256": COQ_ARCHIVE_SHA256,
        "root_obligation_id": oid("ROOT"),
        "denominator_sha256": denominator,
        "frozen_denominators": {
            "inventory": ids,
            "required_machine": [row["obligation_id"] for row in obligations if row["machine_eligibility"] == "required"],
            "required_human_source": [row["obligation_id"] for row in obligations if row["human_source_eligibility"] == "required"],
            "required_readable": ids,
            "informational_overlays": [row["obligation_id"] for row in obligations if row["machine_eligibility"] == "informational"],
            "unique_logical_package_ids": [row["obligation_id"] for row in obligations if row["machine_eligibility"] == "required" and row["kind"] not in {"definition", "transport"}],
            "interface_and_transport_ids": [row["obligation_id"] for row in obligations if row["kind"] in {"definition", "transport"}],
            "source_boundary_ids": [oid("X-COQ-SOURCE"), oid("X-LEAN-PLACEHOLDER"), oid("X-SOURCE")],
            "exact_root_ids": [oid("ROOT")],
            "source_declaration_obligation_ids": [entry[0] for entry in source_entries],
            "source_body_chunk_obligation_ids": [chunk[0] for entry in source_entries for chunk in entry[12]],
        },
        "source_obligation_subregistry": {
            "path": f"Stage1_Instances/{THEOREM}/source-obligation-index.json",
            "schema_version": source_index["schema_version"],
            "entry_count": source_index["entry_count"],
            "chunk_count": source_index["chunk_count"],
            "denominator_sha256": source_index["denominator_sha256"],
            "attachment_semantics": "Every entry is a required logical child of source_package_id; every chunk is a required body-expansion child of its entry obligation.",
        },
        "layer_exclusions": {
            "symmetry_sign_order_normalization": {"status": "not_applicable_pending_independent_approval", "reason": "The root has no chosen representative, sign, or ordering quotient; S/T symmetry is retained inside PF-13 and B-TYPE-PAIR."},
            "finite_infinite_split": {"status": "not_applicable_pending_independent_approval", "reason": "The exact target quantifies only over finite carriers; infinite groups are outside the frozen claim."},
            "computation": {"status": "not_applicable_pending_independent_approval", "reason": "No finite calculation, reflection engine, solver, native code, experiment, or unchecked certificate is credited by the selected route."},
            "cross_kernel_import": {"status": "excluded_pending_independent_approval", "reason": "Lean cannot import the Coq kernel object; X-LEAN-BODY stays required until an approved checked bridge or translation exists."},
        },
        "proof_body_aliases": {
            "PFsection14.Feit_Thompson": "other_prover_architecture_source_no_lean_credit",
            "stripped_Odd_Order": "deduplicated_to:PFsection14.Feit_Thompson",
            "ianklatzco.odd_order_solvable": "rejected_placeholder_no_proof_body_credit",
            "ObligationTree.TranslatedOddOrderBody": "conditional_interface_no_proof_body_credit",
        },
        "delta_policy": "Any target correction, split, merge, exclusion, eligibility/risk change, source revision, package decomposition, or terminal-body identity change requires registry version 2 and an append-only old/new-ID delta.",
        "append_only_delta": [],
        "obligations": obligations,
        "status_observed_after_freeze": {
            "provisionally_checked_interfaces": sorted(checked),
            "accepted_closed_obligations": [],
            "exact_lean_candidate": "M5_placeholder_rejected",
            "other_prover_source": "M3_E3_architecture_anchor_only",
            "root_machine_debt": "M3",
        },
        "status_boundary": "The registry freezes an open translation architecture. Coq packages and the rejected Lean placeholder receive no Lean closure; no obligation is accepted closed.",
    }

    def edge(eid: str, source: str, kind: str, target: str, reciprocal: str | None = None) -> dict:
        result = {"edge_id": eid, "from": source, "type": kind, "to": target}
        if reciprocal:
            result["reciprocal_edge_id"] = reciprocal
        return result

    proof: list[dict] = []
    for parent, children in PROOF_REQUIRES.items():
        for child in children:
            req = f"REQ-{parent}-{child}"
            comp = f"CMP-{child}-{parent}"
            proof.extend([edge(req, parent, "proof_requires", child, comp),
                          edge(comp, child, "composes", parent, req)])
    graph_edges = {
        "proof": proof,
        "refinement": [edge(f"REF-{parent}-{child}", parent, "logical_decomposition", child)
                       for parent, children in refinement.items() for child in children],
        "provenance": [
            edge("SRC-ROOT", oid("X-SOURCE"), "source_map", oid("ROOT")),
            edge("SRC-MINIMAL", oid("X-SOURCE"), "source_map", oid("N-MINIMAL-INDUCTION")),
            edge("SRC-FINAL", oid("X-SOURCE"), "source_map", oid("L-NO-MINIMAL")),
            edge("PROV-COQ", oid("X-PROVENANCE"), "provenance_of", oid("X-COQ-SOURCE")),
            edge("PROV-LEAN", oid("X-PROVENANCE"), "provenance_of", oid("X-LEAN-BODY")),
            edge("PROV-PLACEHOLDER", oid("X-PROVENANCE"), "provenance_of", oid("X-LEAN-PLACEHOLDER")),
        ],
        "evidence": [
            edge("EVID-COQ", oid("X-PROVENANCE"), "evidence_for", oid("X-COQ-SOURCE")),
            edge("EVID-PLACEHOLDER", oid("X-PROVENANCE"), "evidence_for", oid("X-LEAN-PLACEHOLDER")),
            edge("EVID-WORKFLOW", oid("X-WORKFLOW"), "evidence_for", oid("ROOT")),
        ],
        "trust": [
            edge("TRUST-ROOT-FOUNDATION", oid("ROOT"), "trusts", oid("S-FOUNDATION")),
            edge("TRUST-LEAN", oid("X-LEAN-BODY"), "trusts", oid("X-TRUST")),
            edge("TRUST-COQ", oid("X-COQ-SOURCE"), "trusts", oid("X-TRUST")),
            edge("TRUST-LICENSE", oid("X-COQ-SOURCE"), "trusts", oid("X-LICENSE")),
        ],
        "documentation": [
            edge("DOC-ROOT", oid("X-READABLE"), "documents", oid("ROOT")),
            edge("DOC-MINIMAL", oid("X-READABLE"), "documents", oid("N-MINIMAL-INDUCTION")),
            edge("DOC-BG", oid("X-READABLE"), "documents", oid("BG-16")),
            edge("DOC-PF", oid("X-READABLE"), "documents", oid("PF-14")),
        ],
        "workflow": [
            edge("FLOW-BODY", oid("X-WORKFLOW"), "workflow_depends_on", oid("X-LEAN-BODY")),
            edge("FLOW-SOURCE", oid("X-WORKFLOW"), "workflow_depends_on", oid("X-SOURCE")),
            edge("FLOW-PROVENANCE", oid("X-WORKFLOW"), "workflow_depends_on", oid("X-PROVENANCE")),
            edge("FLOW-TRUST", oid("X-WORKFLOW"), "workflow_depends_on", oid("X-TRUST")),
            edge("FLOW-LICENSE", oid("X-WORKFLOW"), "workflow_depends_on", oid("X-LICENSE")),
            edge("FLOW-READABLE", oid("X-WORKFLOW"), "workflow_depends_on", oid("X-READABLE")),
        ],
    }
    graphs = {}
    for name in GRAPH_NAMES:
        outgoing = {identifier: [] for identifier in ids}
        incoming = {identifier: [] for identifier in ids}
        for row in graph_edges[name]:
            outgoing[row["from"]].append(row["edge_id"])
            incoming[row["to"]].append(row["edge_id"])
        graphs[name] = {"edges": graph_edges[name], "out": outgoing, "in": incoming}

    architecture_reachable: set[str] = set()
    frontier = [oid("ROOT")]
    while frontier:
        current = frontier.pop()
        if current in architecture_reachable:
            continue
        architecture_reachable.add(current)
        frontier.extend(refinement.get(current, []))
        frontier.extend(PROOF_REQUIRES.get(current, []))
    edge_count = sum(len(graph["edges"]) for graph in graphs.values())
    bundle = {
        "schema_version": "stage1-typed-graphs/1.0",
        "item_id": ITEM,
        "theorem_id": THEOREM,
        "registry_id": registry["registry_id"],
        "registry_denominator_sha256": denominator,
        "root_node_id": oid("ROOT"),
        "edge_endpoint_namespace": "canonical obligation_id",
        "edge_direction": "proof_requires is parent-to-child; reciprocal composes is child-to-parent",
        "nodes": nodes,
        "graphs": graphs,
        "metrics_projection": {
            "denominator_ids": ids,
            "architecture_reachable_ids": sorted(architecture_reachable),
            "proof_requires_reachable_ids": [oid("ROOT"), oid("T-ROOT"), oid("T-ADAPTER"), oid("X-LEAN-BODY")],
            "machine_closure_reachable_ids": sorted(architecture_reachable),
            "accepted_numerator_ids": [],
            "alias_and_presentation_nodes_receive_credit": False,
            "source_declaration_index_count": len(source_entries),
            "source_body_chunk_count": source_index["chunk_count"],
            "source_declaration_index_sha256": hashlib.sha256(
                (HERE / "source-obligation-index.json").read_bytes()).hexdigest(),
        },
        "closure_boundary": {
            "provisionally_checked_interfaces": sorted(checked),
            "accepted_closed_obligations": [],
            "root_closed": False,
            "root_machine_debt": "M3",
            "open_logical_decomposition_ids": sorted(
                {child for children in refinement.values() for child in children}
            ),
            "open_source_declaration_obligation_ids": [entry[0] for entry in source_entries],
            "open_source_body_chunk_obligation_ids": [
                chunk[0] for entry in source_entries for chunk in entry[12]
            ],
            "audit_complete": False,
            "theorem_complete": False,
            "remaining_root_cut_set": [oid("X-LEAN-BODY"), oid("X-SOURCE"), oid("S-FOUNDATION"),
                                       oid("X-PROVENANCE"), oid("X-TRUST"), oid("X-LICENSE"),
                                       oid("X-READABLE"), oid("X-WORKFLOW")],
            "composition_certificates": [
                "Stage1Instances.THM_M_0070.ObligationTree.target_of_translatedOddOrderBody",
                "Stage1Instances.THM_M_0070.ObligationTree.terminalTarget_of_target",
                "Stage1Instances.THM_M_0070.ObligationTree.root_of_terminalTarget",
            ],
            "missing_composition_certificates": [
                "placeholder-free TranslatedOddOrderBody inhabitant",
                "all logical-decomposition child-to-parent Lean compositions below the external package architecture",
            ],
            "reason": "All local composition is conditional. The exact external Lean body is a placeholder and the MathComp source is a different formal system with no approved Lean bridge.",
        },
        "typed_edge_count": edge_count,
    }

    recipes = []
    for identifier in ids:
        recipes.append({
            "recipe_id": f"VAL-{identifier}",
            "cwd": ".",
            "argv": ["python3", "-B", f"Stage1_Instances/{THEOREM}/check_obligation_tree.py"],
            "env_allowlist": {},
            "timeout_seconds": 180,
            "network_policy": "denied",
            "expected_exit": 0,
            "expected_outputs": [{"path_or_stream": "stdout", "semantic_hash_policy": "contains PASS THM-M-0070 obligation tree"}],
            "covered_obligation_ids": [identifier],
            "covered_declarations": ([
                "Stage1Instances.THM_M_0070.ObligationTree.target_of_translatedOddOrderBody",
                "Stage1Instances.THM_M_0070.ObligationTree.terminalTarget_of_target",
                "Stage1Instances.THM_M_0070.ObligationTree.root_of_terminalTarget",
            ] if identifier in checked else []),
            "coverage_semantics": "conditional_interface_only" if identifier in checked else "architecture_validation_only",
            "closure_credit": False,
        })
    specs = {
        "schema_version": "stage1-validation-specs/1.0",
        "item_id": ITEM,
        "theorem_id": THEOREM,
        "recipes": recipes,
        "status_boundary": "These recipes validate the frozen architecture and conditional Lean interfaces only; they do not import Coq or inhabit the root.",
    }

    lines = [
        "# THM-M-0070 frozen obligation tree", "", f"Item: `{ITEM}`", "",
        "The denominator is frozen from the exact Lean target, immutable anchor inventory, official",
        "MathComp capstone, transitive BG/PF source packages, and the audited Lean-port roadmap. The",
        "available exact Lean declaration is a placeholder and the exact MathComp theorem is a different",
        "kernel object. Neither receives Lean proof credit.", "", "## Checked route and boundary", "",
        "The only locally checked proof path is `M0070-ROOT -> M0070-T-ROOT -> M0070-T-ADAPTER ->",
        "M0070-X-LEAN-BODY`. `ObligationTree.lean` verifies exact conditional composition; the last node",
        "is deliberately open. The MathComp route is a logical architecture rooted at",
        "`M0070-X-COQ-SOURCE`, not a `proof_requires` path. Its section packages must be recursively split",
        "and translated before proof acceptance. A 2,084-entry source declaration index records every",
        "named declaration beneath those packages. Their split ceilings are not proof-length or closure",
        "claims.", "", "## Obligation ledger", "",
    ]
    node_by_id = {node["obligation_id"]: node for node in nodes}
    for obligation in obligations:
        node = node_by_id[obligation["obligation_id"]]
        anchor = obligation["obligation_id"].lower()
        lines += [f'<a id="{anchor}"></a>', f'### `{obligation["obligation_id"]}` - {node["kind"]}', "",
                  node["human_statement"], "",
                  f'- Formal target: `{node["formal_target"]}`',
                  f'- Output: {node["output"]}',
                  f'- Eligibility: machine `{obligation["machine_eligibility"]}`, human source `{obligation["human_source_eligibility"]}`, readable `{obligation["readable_eligibility"]}`',
                  f'- Current debt: `{node["human_debt"]}/{node["machine_debt"]}/{node["readability_debt"]}`; risk `{obligation["risk_class"]}`; split ceiling `{node["step_budget"]}`',
                  f'- Premises: {json.dumps(node["semantic_step_ledger"]["premises"], ensure_ascii=True)}',
                  f'- Inference: `{node["semantic_step_ledger"]["inference"]}`',
                  f'- Outgoing use: {json.dumps(node["semantic_step_ledger"]["outgoing_use"], ensure_ascii=True)}',
                  f'- Package state: `{node["semantic_step_ledger"]["package_expansion_state"]}`',
                  f'- Structured ledger: {json.dumps(node["semantic_step_ledger"]["steps"], ensure_ascii=True)}',
                  f'- Boundary: {node["status_boundary"]}', ""]
    lines += ["## Root cut", "",
              "The root remains `H1/M3/R4`. The first machine cut is `M0070-X-LEAN-BODY`. Source,",
              "foundation, provenance, trust, license, readability, workflow, proof, validation, release,",
              "and master acceptance remain open. No obligation in this registry is accepted closed.", ""]
    return registry, bundle, specs, "\n".join(lines)


def main() -> None:
    registry, bundle, specs, readable = build()
    for name, value in (("obligation-registry.json", registry), ("typed-graphs.json", bundle),
                        ("validation-specs.json", specs)):
        (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    (HERE / "obligation-tree.md").write_text(readable, encoding="utf-8")
    print(f"wrote {len(registry['obligations'])} obligations and {bundle['typed_edge_count']} typed edges")
    print(f"registry denominator sha256: {registry['denominator_sha256']}")


if __name__ == "__main__":
    main()
