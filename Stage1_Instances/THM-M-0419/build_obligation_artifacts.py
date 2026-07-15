#!/usr/bin/env python3
"""Build THM-M-0419's frozen obligation registry and typed graph bundle."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ITEM = "S56-M-0419-OBLIGATION_TREE"
THEOREM = "THM-M-0419"
PREFIX = "M0419-"
ROOT_EXPRESSION = "d30ce90a242e9fe3900ec73e893184ad8878c5b90f5362a4f70ca3846342faeb"
ATLAS_REVISION = "34ffed396f376454c1a9b297f3fd74c5c801fb50"
ATLAS_SOURCE = "0b0d4795e29bdbcbaa1b255c06632b3275956b3f999909400858f4c2779e3617"
RECEIPT_ID = "S56-M-0419-OBLIGATION-TREE-WORKER-20260715"
GRAPH_NAMES = (
    "proof", "refinement", "provenance", "evidence", "trust",
    "documentation", "workflow",
)
REGISTRY_FIELDS = (
    "obligation_id", "statement_fingerprint", "kind", "root_relevant",
    "machine_eligibility", "human_source_eligibility", "readable_eligibility",
    "risk_class", "exclusion_reason", "terminal_proof_body_id",
)


def sha(name: str) -> str:
    return hashlib.sha256((HERE / name).read_bytes()).hexdigest()


def digest(value: object) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(payload).hexdigest()


def oid(short: str) -> str:
    return PREFIX + short


def planned(short: str, formal_target: str) -> str:
    return "planned-v1-sha256:" + digest(
        {"obligation_id": oid(short), "formal_target": formal_target}
    )


# short id, registry kind, node kind, risk, human claim, formal target, output,
# M eligibility, H eligibility, R eligibility, terminal body, budget, M debt.
ROWS = (
    (
        "ROOT", "root", "root", "critical",
        "Every finite abelian extension of the rational numbers embeds over Q into a cyclotomic field of nonzero index.",
        "Stage1.THM_M_0419.Statement",
        "The exact frozen Kronecker-Weber proposition.",
        "required", "required", "required", None, 8, "M3",
    ),
    (
        "S-TARGET", "definition", "definition", "critical",
        "Freeze the carrier universe, Field, Algebra Q, NumberField, IsAbelianGalois, nonzero conductor, algebraBase instance, and AlgHom conclusion.",
        "Stage1.THM_M_0419.Statement and StatementShape",
        "The exact ordered target interface.",
        "required", "not_applicable", "required", None, 7, "M0-L",
    ),
    (
        "S-BOUNDARY", "branch", "branch", "high",
        "Retain the trivial extension and every universe presentation while excluding only conductor zero.",
        "Statement.lean plus statement-gate mutation receipts",
        "A boundary policy that neither strengthens nor weakens the target.",
        "required", "required", "required", None, 6, "M0-L",
    ),
    (
        "S-POSITIVE", "transport", "transport", "high",
        "Transport the source-shaped positive-index containment conclusion to the exact nonzero-index target.",
        "Stage1.THM_M_0419.ObligationTree.checkedPositiveTransport",
        "PositiveContainmentTarget implies the exact canonical Statement.",
        "required", "required", "required",
        "local:ObligationTree.lean#checkedPositiveTransport", 4, "M0-L",
    ),
    (
        "S-FOUNDATION", "certificate", "certificate", "critical",
        "Account for Lean's kernel, classical choice, quotient soundness, propositional extensionality, imports, compiled artifacts, and the no-oracle boundary.",
        "foundation/TCB validation of every eventual terminal declaration",
        "An accepted theorem-specific foundation and trust policy.",
        "required", "not_applicable", "required", None, 7, "M3",
    ),
    (
        "N-COMPLETION", "normalization", "normalization", "critical",
        "For each rational prime, pass from K/Q to a finite abelian extension of Q_p while preserving a checked route back to the global automorphism data.",
        "planned: rational-prime completion and abelian-extension transport",
        "The p-adic extension consumed by local Kronecker-Weber.",
        "required", "required", "required", None, 8, "M4",
    ),
    (
        "N-LOCAL-PRESENTATION", "normalization", "normalization", "critical",
        "Normalize local containment, positivity, cyclotomic algebra structures, and field presentations without changing the extension claim.",
        "planned: local containment representation transports",
        "A common LocalContainment interface over Q_p.",
        "required", "required", "required", None, 7, "M4",
    ),
    (
        "B-INDUCTION", "reduction", "reduction", "critical",
        "Use strong induction on local degree and split a non-cyclic abelian group into complementary proper subextensions whose cyclotomic containments recombine.",
        "Stage1.THM_M_0419.ObligationTree.LocalInductionPackage",
        "CyclicPrimePowerPackage implies LocalContainmentPackage.",
        "required", "required", "required", None, 10, "M4",
    ),
    (
        "B-CYCLIC", "branch", "branch", "critical",
        "Exhaust cyclic prime-power local extensions by the tame degree-prime-not-p case, odd wild case, and 2-adic wild case.",
        "Stage1.THM_M_0419.ObligationTree.cyclicPrimePower_of_branches",
        "The complete CyclicPrimePowerPackage.",
        "required", "required", "required",
        "local:ObligationTree.lean#cyclicPrimePower_of_branches", 7, "M0-L",
    ),
    (
        "L-TAME", "lemma", "core_lemma", "critical",
        "Embed every cyclic local extension of prime-power degree l^r with l distinct from the residue prime p into a cyclotomic extension.",
        "Stage1.THM_M_0419.ObligationTree.TameBranchPackage",
        "The tame branch of CyclicPrimePowerPackage.",
        "required", "required", "required", None, 9, "M4",
    ),
    (
        "L-WILD-ODD", "lemma", "core_lemma", "critical",
        "Embed every cyclic p-power extension of Q_p for odd p into a cyclotomic extension.",
        "Stage1.THM_M_0419.ObligationTree.WildOddBranchPackage",
        "The odd wildly ramified branch.",
        "required", "required", "required", None, 10, "M4",
    ),
    (
        "L-WILD-TWO", "lemma", "core_lemma", "critical",
        "Embed every cyclic 2-power extension of Q_2 into a cyclotomic extension, including the exceptional 2-adic group structure.",
        "Stage1.THM_M_0419.ObligationTree.WildTwoBranchPackage",
        "The 2-adic wildly ramified branch.",
        "required", "required", "required", None, 10, "M4",
    ),
    (
        "C-LOCAL-COMPOSITUM", "construction", "construction", "critical",
        "Combine the two proper subextension embeddings and all selected local cyclotomic fields into one local cyclotomic field.",
        "planned: complementary-subfield and local cyclotomic compositum construction",
        "The recombination invariant required by local strong induction.",
        "required", "required", "required", None, 9, "M4",
    ),
    (
        "T-LOCAL", "terminal", "terminal", "critical",
        "Compose cyclic branches with the induction engine to prove local Kronecker-Weber for every finite abelian extension of Q_p.",
        "Stage1.THM_M_0419.ObligationTree.localContainment_of_induction",
        "LocalContainmentPackage.",
        "required", "required", "required",
        "local:ObligationTree.lean#localContainment_of_induction", 4, "M3",
    ),
    (
        "C-GLOBAL-CONDUCTOR", "construction", "construction", "critical",
        "Extract finitely supported local conductor data and construct one positive global cyclotomic modulus and a compatible cyclotomic extension.",
        "planned: conductor_from_local_cyclotomic_data",
        "A positive modulus m and a global cyclotomic extension carrying the local data.",
        "required", "required", "required", None, 10, "M4",
    ),
    (
        "L-INERTIA-EMBED", "lemma", "core_lemma", "critical",
        "Use inertia data and the Minkowski argument to embed K into the global cyclotomic extension produced by the conductor step.",
        "planned: inertia_minkowski_gives_embedding",
        "A Q-algebra embedding from K into the constructed cyclotomic extension.",
        "required", "required", "required", None, 10, "M4",
    ),
    (
        "C-CYCLOTOMIC-IDENTIFY", "transport", "transport", "critical",
        "Identify an abstract singleton cyclotomic extension with CyclotomicField m Q under algebraBase and compose the embedding.",
        "planned: IsCyclotomicExtension.algEquiv adapter to CyclotomicField",
        "The exact PositiveContainmentTarget embedding.",
        "required", "required", "required", None, 7, "M4",
    ),
    (
        "T-GLOBAL", "terminal", "terminal", "critical",
        "Compose completion, local containment, conductor construction, inertia embedding, and cyclotomic identification into the positive global target.",
        "Stage1.THM_M_0419.ObligationTree.GlobalizationPackage",
        "PositiveContainmentTarget.",
        "required", "required", "required", None, 8, "M4",
    ),
    (
        "T-ASSEMBLE", "terminal", "terminal", "critical",
        "Consume the exact transport, local package, and globalization package to yield the frozen root with no undeclared premise.",
        "Stage1.THM_M_0419.ObligationTree.root_of_packages",
        "Stage1.THM_M_0419.Statement.",
        "required", "required", "required",
        "local:ObligationTree.lean#root_of_packages", 5, "M0-L",
    ),
    (
        "X-SOURCE", "terminal", "terminal", "high",
        "Pinpoint and independently review a primary human proof, its hypotheses, pages, errata, and the mapping to every mathematical obligation.",
        "Washington Chapter 14 pinpoint source ledger pending",
        "Human-source coverage without machine-proof credit.",
        "not_applicable", "required", "required", None, 8, "M4",
    ),
    (
        "X-ATLAS", "terminal", "terminal", "critical",
        "Record the immutable Atlas theorem_20_1 architecture, every placeholder-bearing terminal dependency, representation delta, and license boundary without proof credit.",
        f"atlas-lean@{ATLAS_REVISION}:KroneckerWeber.theorem_20_1",
        "A classified external provenance boundary, never a proof premise.",
        "informational", "not_applicable", "required",
        f"external-placeholder:{ATLAS_REVISION}:{ATLAS_SOURCE}#KroneckerWeber.theorem_20_1", 9, "M3",
    ),
    (
        "X-PROVENANCE", "certificate", "certificate", "critical",
        "Resolve every wrapper, terminal body, source blob, revision, import, license, and shared body identity before any machine closure is credited.",
        "transitive declaration and proof-body provenance inventory pending",
        "Body-level provenance and deduplication without proof credit.",
        "informational", "not_applicable", "required", None, 8, "M3",
    ),
    (
        "X-TRUST", "certificate", "certificate", "critical",
        "Audit terminal axioms, unsafe/oracle boundaries, executable and compiled-artifact identities, supply chain, hermetic replay, and independent verification.",
        "Lean 4.29.0 plus mathlib 8a178386 transitive trust closure pending",
        "Release trust coverage without mathematical proof credit.",
        "informational", "not_applicable", "required", None, 9, "M3",
    ),
    (
        "X-READABLE", "terminal", "terminal", "high",
        "Produce and independently review a node-specific readable reconstruction with substantive ledgers for the entire local-to-global proof.",
        "independent readable reconstruction pending",
        "Readable coverage without machine-proof credit.",
        "not_applicable", "required", "required", None, 8, "M4",
    ),
    (
        "X-WORKFLOW", "certificate", "certificate", "high",
        "Bind proof, validation, source/readable review, freshness, revocation, release, and independent-verification acceptance.",
        "Stage1 task and receipt workflow",
        "Workflow acceptance without mathematical proof credit.",
        "informational", "not_applicable", "required", None, 7, "M3",
    ),
)


LEDGER_DETAILS = {
    oid("ROOT"): (
        [oid("T-ASSEMBLE")],
        "Apply the checked exact-root assembly and retain the frozen binder context.",
        ["theorem root and release decision"],
    ),
    oid("S-TARGET"): (
        ["Statement.lean", "statement.json expression fingerprint"],
        "Elaborate StatementShape, Statement, and statement_iff with fixed imports and universes.",
        [oid("ROOT"), oid("S-POSITIVE")],
    ),
    oid("S-BOUNDARY"): (
        ["statement mutations: removed hypothesis, changed domain, changed scope, conductor zero"],
        "Preserve the exact source domain and prove the nonzero-index boundary is intentional.",
        [oid("ROOT"), oid("S-POSITIVE")],
    ),
    oid("S-POSITIVE"): (
        ["PositiveContainmentTarget", "Nat.ne_of_gt"],
        "Convert 1 <= n to n != 0 without changing the algebra embedding.",
        [oid("T-ASSEMBLE")],
    ),
    oid("S-FOUNDATION"): (
        ["actual eventual terminal declarations", "pinned Lean and dependency closure"],
        "Compare machine-derived axioms and TCB elements to the theorem-specific accepted profiles.",
        [oid("ROOT"), oid("X-TRUST")],
    ),
    oid("N-COMPLETION"): (
        ["finite abelian K/Q", "one rational prime p"],
        "Construct a bounded finite Galois p-adic completion and inject its automorphism group into Gal(K/Q).",
        [oid("T-GLOBAL")],
    ),
    oid("N-LOCAL-PRESENTATION"): (
        [oid("N-COMPLETION"), "cyclotomic algebraBase convention"],
        "Transport completion and cyclotomic presentations into LocalContainment without losing positivity or scalar compatibility.",
        [oid("T-LOCAL"), oid("T-GLOBAL")],
    ),
    oid("B-INDUCTION"): (
        [oid("B-CYCLIC"), oid("C-LOCAL-COMPOSITUM")],
        "Strong-induct on finrank; use the cyclic prime-power case or two proper fixed fields and recombine them.",
        [oid("T-LOCAL")],
    ),
    oid("B-CYCLIC"): (
        [oid("L-TAME"), oid("L-WILD-ODD"), oid("L-WILD-TWO")],
        "Split on l = p and p = 2; dispatch exactly one exhaustive branch.",
        [oid("B-INDUCTION"), oid("T-LOCAL")],
    ),
    oid("L-TAME"): (
        ["cyclic local degree l^r", "l prime", "l != p"],
        "Use tame decomposition, unramified and ramified cyclotomic factors, and their compositum embedding.",
        [oid("B-CYCLIC")],
    ),
    oid("L-WILD-ODD"): (
        ["cyclic local degree p^r", "p odd"],
        "Use the odd-prime ramified/unramified cyclotomic structure and exclude the forbidden Galois-group configuration.",
        [oid("B-CYCLIC")],
    ),
    oid("L-WILD-TWO"): (
        ["cyclic local degree 2^r"],
        "Handle the exceptional 2-adic unit-group cases and exclude the Z2xZ4 and Z4xZ4xZ4 obstructions.",
        [oid("B-CYCLIC")],
    ),
    oid("C-LOCAL-COMPOSITUM"): (
        ["two complementary proper subextensions", "their local cyclotomic embeddings"],
        "Construct one common cyclotomic overfield and embed the compositum generated by both fixed fields.",
        [oid("B-INDUCTION")],
    ),
    oid("T-LOCAL"): (
        [oid("B-INDUCTION"), oid("B-CYCLIC")],
        "Apply the checked LocalInductionPackage interface to CyclicPrimePowerPackage.",
        [oid("T-GLOBAL")],
    ),
    oid("C-GLOBAL-CONDUCTOR"): (
        [oid("N-COMPLETION"), oid("T-LOCAL")],
        "Bound local conductors, discard trivial primes, and combine the finite data into one positive modulus m.",
        [oid("L-INERTIA-EMBED"), oid("T-GLOBAL")],
    ),
    oid("L-INERTIA-EMBED"): (
        [oid("C-GLOBAL-CONDUCTOR"), "global inertia groups", "Minkowski bound"],
        "Show the constructed cyclotomic extension has enough inertia data to admit a Q-algebra embedding of K.",
        [oid("C-CYCLOTOMIC-IDENTIFY")],
    ),
    oid("C-CYCLOTOMIC-IDENTIFY"): (
        [oid("L-INERTIA-EMBED"), "singleton IsCyclotomicExtension"],
        "Choose the canonical equivalence to CyclotomicField m Q and compose its AlgHom with the K embedding.",
        [oid("T-GLOBAL")],
    ),
    oid("T-GLOBAL"): (
        [oid("N-COMPLETION"), oid("T-LOCAL"), oid("C-GLOBAL-CONDUCTOR"), oid("L-INERTIA-EMBED"), oid("C-CYCLOTOMIC-IDENTIFY")],
        "Compose every local-to-global stage into PositiveContainmentTarget.",
        [oid("T-ASSEMBLE")],
    ),
    oid("T-ASSEMBLE"): (
        [oid("S-POSITIVE"), oid("T-LOCAL"), oid("T-GLOBAL")],
        "Use root_of_packages to consume transport, local containment, globalization, and the root assembly interface.",
        [oid("ROOT")],
    ),
    oid("X-SOURCE"): (
        ["immutable primary edition", "pinpoint theorem and proof", "errata", "independent reviewer"],
        "Map every mathematical node to exact source passages and classify fidelity independently of Lean status.",
        [oid("ROOT"), oid("X-READABLE")],
    ),
    oid("X-ATLAS"): (
        [f"atlas-lean@{ATLAS_REVISION}", f"source sha256 {ATLAS_SOURCE}", "22 placeholder occurrences"],
        "Trace theorem_20_1 through theorem_20_2 and proposition_20_3, record placeholder-bearing leaves and grant zero credit.",
        [oid("X-PROVENANCE")],
    ),
    oid("X-PROVENANCE"): (
        ["repo-local declarations", "pinned mathlib", oid("X-ATLAS")],
        "Resolve conclusion, wrapper, terminal body, transitive dependencies, revisions, source hashes, and licenses.",
        [oid("ROOT"), oid("X-TRUST")],
    ),
    oid("X-TRUST"): (
        [oid("S-FOUNDATION"), oid("X-PROVENANCE"), "actual proof bodies"],
        "Recompute axioms, unsafe/oracle boundaries, executable hashes, dependency closure, and replay evidence.",
        [oid("ROOT"), oid("X-WORKFLOW")],
    ),
    oid("X-READABLE"): (
        [oid("X-SOURCE"), "every required readable obligation", "independent reviewer"],
        "Publish exact claim, role, inputs, route, branches, formal map, trust, ledger, boundary, and status per node.",
        [oid("ROOT"), oid("X-WORKFLOW")],
    ),
    oid("X-WORKFLOW"): (
        ["accepted proof/source/readable/trust receipts", "freshness and revocation state"],
        "Enforce dependency order through proof, validation, release, and independent verification.",
        ["AUDIT-Z and THEOREM-Z decisions"],
    ),
}


def substantive_steps(identifier: str, count: int, formal_target: str, output: str) -> list[dict]:
    premises, inference, outgoing = LEDGER_DETAILS[identifier]
    stages = (
        (premises, "Fix the exact inputs and context for this obligation.", "The obligation context is fixed."),
        ([identifier], inference, output),
        ([identifier], "Check that no stronger premise, hidden branch, or support edge is introduced.", "The stated output has exactly the recorded boundary."),
        ([identifier], "Bind the output to its declared proof, support, or workflow consumers.", "Only the recorded outgoing uses may consume the result."),
        ([identifier], "Retain the stated H/M/R debt and invalidation inputs until accepted evidence exists.", "The node remains truthfully classified."),
        ([identifier], "Keep aliases, wrappers, and presentation variants on the same canonical identity.", "No duplicate coverage is created."),
        ([identifier], "Require the node-specific structured validation recipe before any state proposal.", "The validation boundary is explicit."),
        ([identifier], "Require independent master review for every acceptance-sensitive conclusion.", "No worker assertion becomes accepted state."),
        ([identifier], "Record the remaining proof or assurance debt for downstream execution.", "The next open dependency is explicit."),
        ([identifier], "Publish the precise node boundary in the readable architecture.", "The readable target cannot imply theorem completion."),
    )
    result = []
    for index, (step_premises, step_inference, exact_output) in enumerate(stages[:count], 1):
        result.append({
            "step_id": f"{identifier}-STEP-{index:02d}",
            "premise_ids": step_premises,
            "inference_or_source": step_inference,
            "exact_output": exact_output,
            "outgoing_use_ids": outgoing,
        })
    return result


def graph(ids: list[str], edges: list[dict]) -> dict:
    incoming = {identifier: [] for identifier in ids}
    outgoing = {identifier: [] for identifier in ids}
    for edge in edges:
        outgoing[edge["from"]].append(edge["edge_id"])
        incoming[edge["to"]].append(edge["edge_id"])
    return {"edges": edges, "out": outgoing, "in": incoming}


def support_edges(prefix: str, kind: str, pairs: list[tuple[str, str]]) -> list[dict]:
    return [
        {"edge_id": f"{prefix}{index:02d}", "type": kind, "from": source, "to": target}
        for index, (source, target) in enumerate(pairs, 1)
    ]


def build() -> tuple[dict, dict, dict]:
    obligations = []
    for row in ROWS:
        short, registry_kind, _node_kind, risk, _human, formal, _output, machine, human, readable, body, _budget, _debt = row
        identifier = oid(short)
        fingerprint = (
            "lean-expression-sha256:" + ROOT_EXPRESSION
            if short in {"ROOT", "S-TARGET"}
            else planned(short, formal)
        )
        exclusions = []
        if machine != "required":
            exclusions.append("machine_" + machine)
        if human != "required":
            exclusions.append("human_source_" + human)
        if readable != "required":
            exclusions.append("readable_" + readable)
        obligations.append({
            "obligation_id": identifier,
            "statement_fingerprint": fingerprint,
            "kind": registry_kind,
            "root_relevant": True,
            "machine_eligibility": machine,
            "human_source_eligibility": human,
            "readable_eligibility": readable,
            "risk_class": risk,
            "exclusion_reason": (
                "+".join(exclusions) + ":pending_independent_approval" if exclusions else None
            ),
            "terminal_proof_body_id": body,
        })

    ids = [row["obligation_id"] for row in obligations]
    projection = [{field: row[field] for field in REGISTRY_FIELDS} for row in obligations]
    denominator = digest(projection)
    registry = {
        "schema_version": "stage1-obligation-registry/1.0",
        "registry_id": "THM-M-0419-OBLIGATIONS-v1",
        "item_id": ITEM,
        "theorem_id": THEOREM,
        "registry_version": 1,
        "frozen_at": "2026-07-15T15:32:25+08:00",
        "freeze_basis": "The exact elaborated statement and bounded immutable anchor audit determine the local-to-global Kronecker-Weber architecture. Eligibility follows semantic root relevance rather than available proof status.",
        "freeze_timing_boundary": "The workflow orders anchor audit before this freeze. Candidate status was therefore observable, but every source, bridge, construction, branch, transport, trust, readable, and workflow obligation remains in the denominator independently of proof convenience.",
        "frozen_against_statement_sha256": sha("Statement.lean"),
        "frozen_against_statement_record_sha256": sha("statement.json"),
        "frozen_against_anchor_audit_sha256": sha("anchor-audit.json"),
        "root_obligation_id": oid("ROOT"),
        "denominator_sha256": denominator,
        "frozen_denominators": {
            "inventory": ids,
            "required_machine": [row["obligation_id"] for row in obligations if row["machine_eligibility"] == "required"],
            "required_human_source": [row["obligation_id"] for row in obligations if row["human_source_eligibility"] == "required"],
            "required_readable": [row["obligation_id"] for row in obligations if row["readable_eligibility"] == "required"],
            "informational_overlays": [row["obligation_id"] for row in obligations if row["machine_eligibility"] == "informational"],
        },
        "mandatory_layer_analysis": {
            "S": [oid("S-TARGET"), oid("S-BOUNDARY"), oid("S-POSITIVE"), oid("S-FOUNDATION")],
            "N": [oid("N-COMPLETION"), oid("N-LOCAL-PRESENTATION")],
            "B": [oid("B-INDUCTION"), oid("B-CYCLIC")],
            "C": [oid("C-LOCAL-COMPOSITUM"), oid("C-GLOBAL-CONDUCTOR"), oid("C-CYCLOTOMIC-IDENTIFY")],
            "L": [oid("L-TAME"), oid("L-WILD-ODD"), oid("L-WILD-TWO"), oid("L-INERTIA-EMBED")],
            "X": [oid("X-SOURCE"), oid("X-ATLAS"), oid("X-PROVENANCE"), oid("X-TRUST"), oid("X-READABLE"), oid("X-WORKFLOW")],
            "T": [oid("T-LOCAL"), oid("T-GLOBAL"), oid("T-ASSEMBLE")],
            "not_applicable_layers": [],
        },
        "delta_policy": "Any correction, split, merge, target change, eligibility change, exclusion, or weight change requires registry version 2 and an append-only old/new ID delta; v1 remains reportable.",
        "obligations": obligations,
        "append_only_delta": [],
        "deduplication": {
            "local_conditional_declarations": "Composition interfaces receive no substantive theorem-body credit and do not duplicate their premises.",
            "atlas_terminal": f"KroneckerWeber.theorem_20_1@{ATLAS_REVISION} is one zero-credit placeholder-bearing candidate body.",
            "atlas_aliases_without_independent_credit": [
                "Atlas.NumberTheoryI.KroneckerWeber.theorem_20_1",
                "KroneckerWeber.proposition_20_3",
                "KroneckerWeber.theorem_20_2",
            ],
        },
        "status_observed_after_freeze": {
            "accepted_closed_obligations": [],
            "provisionally_checked_interfaces": [
                oid("S-POSITIVE"), oid("B-CYCLIC"), oid("T-LOCAL"), oid("T-ASSEMBLE")
            ],
            "authoritative_root_vector": {"H": "H1", "M": "M3", "R": "R3"},
        },
        "status_boundary": "This freeze supplies architecture and conditional interfaces only. It accepts no proof, source, readable, trust, validation, audit, or theorem-completion state.",
    }

    nodes = []
    for row in ROWS:
        short, _registry_kind, node_kind, _risk, human, formal, output, _machine, human_eligibility, _readable, body, budget, machine_debt = row
        identifier = oid(short)
        owned = []
        if short in {"S-TARGET", "S-BOUNDARY"}:
            owned.append("Stage1_Instances/THM-M-0419/Statement.lean")
        if body and body.startswith("local:"):
            owned.append("Stage1_Instances/THM-M-0419/ObligationTree.lean")
        source_crosswalk = (
            "not-applicable"
            if human_eligibility == "not_applicable"
            else "source_statement_crosswalk.md:pinpoint-node-review-pending"
        )
        provenance = (
            "anchor-audit:S56-M-0419-C03-zero-credit" if short == "X-ATLAS"
            else "local:ObligationTree.lean" if body and body.startswith("local:")
            else "pending"
        )
        steps = substantive_steps(identifier, budget, formal, output)
        nodes.append({
            "node_id": identifier,
            "obligation_id": identifier,
            "kind": node_kind,
            "human_statement": human,
            "formal_target": formal,
            "output": output,
            "human_debt": "H1",
            "machine_debt": machine_debt,
            "readability_debt": "R3",
            "evidence_ids": [],
            "source_crosswalk_id": source_crosswalk,
            "provenance_id": provenance,
            "foundation_profile": "lean4-mathlib-classical/propext+Classical.choice+Quot.sound-observed-acceptance-pending",
            "tcb_profile": "lean-4.29.0+mathlib-8a178386/transitive-closure-and-independent-replay-pending",
            "computation_record": "none; no computation, oracle, native evaluator, or external solver receives proof credit",
            "step_budget": budget,
            "semantic_step_ledger": {
                "premises": LEDGER_DETAILS[identifier][0],
                "inference": LEDGER_DETAILS[identifier][1],
                "output": output,
                "outgoing_use": LEDGER_DETAILS[identifier][2],
                "steps": steps,
            },
            "public_readable_target": f"Stage1_Instances/THM-M-0419/obligation-tree.md#{identifier.lower()}",
            "validation_spec_id": "VAL-" + identifier,
            "status_boundary": "Provisional obligation architecture only; conditional interface checks supply no accepted substantive premise or theorem closure.",
            "task_ids": [ITEM, "S56-M-0419-PROOF", "S56-M-0419-VALIDATION"],
            "owned_sources": owned,
            "owner": "THM-M-0419 execution lane",
            "reviewer": "independent Stage1 integration lane",
            "validity": {
                "validated_at": "2026-07-15" if owned else None,
                "review_due": "before master acceptance and on every invalidation input change",
                "invalidation_inputs": [
                    "Statement.lean", "statement.json", "anchor-audit.json",
                    "obligation-registry.json", "ObligationTree.lean", "toolchain",
                ],
                "revocation_state": "provisional" if owned else "open",
            },
        })

    # Only interfaces with checked child-to-parent terms use proof_requires/composes.
    proof_pairs = [
        (oid("ROOT"), oid("T-ASSEMBLE")),
        (oid("T-ASSEMBLE"), oid("S-POSITIVE")),
        (oid("T-ASSEMBLE"), oid("T-LOCAL")),
        (oid("T-ASSEMBLE"), oid("T-GLOBAL")),
        (oid("T-LOCAL"), oid("B-INDUCTION")),
        (oid("T-LOCAL"), oid("B-CYCLIC")),
        (oid("B-CYCLIC"), oid("L-TAME")),
        (oid("B-CYCLIC"), oid("L-WILD-ODD")),
        (oid("B-CYCLIC"), oid("L-WILD-TWO")),
    ]
    proof_edges = []
    for index, pair in enumerate(proof_pairs, 1):
        parent, child = pair
        requirement = f"P{index:02d}-REQ"
        reciprocal = f"P{index:02d}-COMP"
        proof_edges.extend([
            {
                "edge_id": requirement,
                "type": "proof_requires",
                "from": parent,
                "to": child,
                "reciprocal_edge_id": reciprocal,
            },
            {
                "edge_id": reciprocal,
                "type": "composes",
                "from": child,
                "to": parent,
                "reciprocal_edge_id": requirement,
            },
        ])

    refinement_pairs = [
        (oid("ROOT"), oid("S-TARGET")),
        (oid("S-TARGET"), oid("S-BOUNDARY")),
        (oid("T-GLOBAL"), oid("N-COMPLETION")),
        (oid("T-GLOBAL"), oid("N-LOCAL-PRESENTATION")),
        (oid("B-INDUCTION"), oid("C-LOCAL-COMPOSITUM")),
        (oid("T-GLOBAL"), oid("C-GLOBAL-CONDUCTOR")),
        (oid("T-GLOBAL"), oid("L-INERTIA-EMBED")),
        (oid("T-GLOBAL"), oid("C-CYCLOTOMIC-IDENTIFY")),
    ]
    provenance_pairs = [
        (oid("X-ATLAS"), oid("B-INDUCTION")),
        (oid("X-ATLAS"), oid("L-TAME")),
        (oid("X-ATLAS"), oid("L-WILD-ODD")),
        (oid("X-ATLAS"), oid("L-WILD-TWO")),
        (oid("X-ATLAS"), oid("C-GLOBAL-CONDUCTOR")),
        (oid("X-ATLAS"), oid("L-INERTIA-EMBED")),
        (oid("X-PROVENANCE"), oid("ROOT")),
    ]
    trust_pairs = [
        (oid("ROOT"), oid("S-FOUNDATION")),
        (oid("ROOT"), oid("X-TRUST")),
        (oid("X-PROVENANCE"), oid("X-TRUST")),
    ]
    documentation_pairs = [
        (oid("X-READABLE"), identifier) for identifier in ids if identifier != oid("X-READABLE")
    ]
    workflow_pairs = [
        (oid("ROOT"), oid("X-SOURCE")),
        (oid("ROOT"), oid("X-PROVENANCE")),
        (oid("ROOT"), oid("X-TRUST")),
        (oid("ROOT"), oid("X-READABLE")),
        (oid("ROOT"), oid("X-WORKFLOW")),
    ]
    graphs = {
        "proof": graph(ids, proof_edges),
        "refinement": graph(ids, support_edges("R", "logical_decomposition", refinement_pairs)),
        "provenance": graph(ids, support_edges("V", "provenance_of", provenance_pairs)),
        "evidence": graph(ids, []),
        "trust": graph(ids, support_edges("TR", "trusts", trust_pairs)),
        "documentation": graph(ids, support_edges("D", "documents", documentation_pairs)),
        "workflow": graph(ids, support_edges("W", "workflow_depends_on", workflow_pairs)),
    }

    task_nodes = [
        ("INTAKE", "intake", 0), ("STATEMENT", "statement", 1),
        ("ANCHOR_AUDIT", "anchor_audit", 2), ("OBLIGATION_TREE", "obligation_tree", 3),
        ("PROOF", "proof", 4), ("VALIDATION", "validation", 5),
        ("RELEASE", "release", 6),
    ]
    task_ids = {name: f"S56-M-0419-{name}" for name, _phase, _layer in task_nodes}
    task_edges = []
    dependency_order = (
        ("STATEMENT", "INTAKE"), ("ANCHOR_AUDIT", "STATEMENT"),
        ("OBLIGATION_TREE", "ANCHOR_AUDIT"), ("PROOF", "OBLIGATION_TREE"),
        ("VALIDATION", "PROOF"), ("RELEASE", "VALIDATION"),
    )
    for index, (source, target) in enumerate(dependency_order, 1):
        task_edges.append({
            "edge_id": f"TASK-{index:02d}",
            "type": "workflow_depends_on",
            "from": task_ids[source],
            "to": task_ids[target],
        })
    task_links = []
    for identifier in ids:
        task_links.append({"task_id": ITEM, "obligation_id": identifier})
        if identifier not in {oid("X-SOURCE"), oid("S-FOUNDATION"), oid("X-PROVENANCE"), oid("X-TRUST"), oid("X-READABLE"), oid("X-WORKFLOW")}:
            task_links.append({"task_id": task_ids["PROOF"], "obligation_id": identifier})
        task_links.append({"task_id": task_ids["VALIDATION"], "obligation_id": identifier})

    bundle = {
        "schema_version": "stage1-typed-graphs/1.0",
        "item_id": ITEM,
        "theorem_id": THEOREM,
        "registry_id": registry["registry_id"],
        "registry_denominator_sha256": denominator,
        "root_node_id": oid("ROOT"),
        "edge_direction": "proof_requires runs parent to child; its reciprocal composes edge runs child to parent. Support graphs never confer machine closure.",
        "nodes": nodes,
        "graphs": graphs,
        "composition_certificates": [
            {
                "certificate_id": "COMP-M0419-CYCLIC",
                "declaration": "Stage1.THM_M_0419.ObligationTree.cyclicPrimePower_of_branches",
                "parent_obligation_id": oid("B-CYCLIC"),
                "consumes": [oid("L-TAME"), oid("L-WILD-ODD"), oid("L-WILD-TWO")],
                "state": "kernel_checked_conditional_provisional",
            },
            {
                "certificate_id": "COMP-M0419-LOCAL",
                "declaration": "Stage1.THM_M_0419.ObligationTree.localContainment_of_induction",
                "parent_obligation_id": oid("T-LOCAL"),
                "consumes": [oid("B-INDUCTION"), oid("B-CYCLIC")],
                "state": "kernel_checked_conditional_provisional",
            },
            {
                "certificate_id": "COMP-M0419-ROOT",
                "declaration": "Stage1.THM_M_0419.ObligationTree.checkedRootAssembly",
                "parent_obligation_id": oid("T-ASSEMBLE"),
                "consumes": [oid("S-POSITIVE"), oid("T-LOCAL"), oid("T-GLOBAL")],
                "state": "kernel_checked_conditional_provisional",
            },
            {
                "certificate_id": "COMP-M0419-ROOT-BIND",
                "declaration": "Stage1.THM_M_0419.ObligationTree.root_of_packages",
                "parent_obligation_id": oid("ROOT"),
                "consumes": [oid("T-ASSEMBLE")],
                "state": "kernel_checked_conditional_provisional",
            },
        ],
        "unverified_decomposition_plans": [
            {"parent": parent, "child": child, "state": "planned_no_composition_credit"}
            for parent, child in refinement_pairs
        ],
        "workflow_task_graph": {
            "nodes": [
                {"task_id": task_ids[name], "phase": phase, "layer": layer}
                for name, phase, layer in task_nodes
            ],
            "edges": task_edges,
            "task_obligation_links": task_links,
        },
        "evidence_endpoint_policy": "The evidence graph is empty because this phase creates only an unaccepted provisional worker receipt, not a canonical accepted evidence-object obligation.",
        "closure_boundary": {
            "accepted_closed_obligations": [],
            "provisionally_checked_interfaces": [
                oid("S-POSITIVE"), oid("B-CYCLIC"), oid("T-LOCAL"), oid("T-ASSEMBLE")
            ],
            "root_closed": False,
            "audit_complete": False,
            "theorem_complete": False,
            "authoritative_root_vector": {"H": "H1", "M": "M3", "R": "R3"},
            "minimal_open_proof_cut_set": [oid("B-INDUCTION"), oid("L-TAME"), oid("L-WILD-ODD"), oid("L-WILD-TWO"), oid("T-GLOBAL")],
            "remaining_root_assurance_cut_set": [oid("X-SOURCE"), oid("S-FOUNDATION"), oid("X-PROVENANCE"), oid("X-TRUST"), oid("X-READABLE"), oid("X-WORKFLOW")],
            "reason": "All Lean declarations are transports or conditional compositions. The local induction engine, all three cyclic branches, globalization, source, provenance, trust, readable review, and workflow acceptance remain open.",
        },
        "status_boundary": "No graph support edge, conditional theorem, source mapping, or worker receipt closes a mathematical obligation or the canonical root.",
    }

    covered_declarations = {
        oid("S-POSITIVE"): ["Stage1.THM_M_0419.ObligationTree.checkedPositiveTransport"],
        oid("B-CYCLIC"): ["Stage1.THM_M_0419.ObligationTree.cyclicPrimePower_of_branches"],
        oid("T-LOCAL"): ["Stage1.THM_M_0419.ObligationTree.localContainment_of_induction"],
        oid("T-ASSEMBLE"): ["Stage1.THM_M_0419.ObligationTree.checkedRootAssembly"],
        oid("ROOT"): ["Stage1.THM_M_0419.ObligationTree.root_of_packages"],
    }
    recipes = {
        "schema_version": "stage1-validation-specs/1.0",
        "item_id": ITEM,
        "theorem_id": THEOREM,
        "registry_denominator_sha256": denominator,
        "recipes": [
            {
                "recipe_id": "VAL-" + identifier,
                "cwd": ".",
                "argv": ["python3", "-B", "Stage1_Instances/THM-M-0419/check_obligation_tree.py"],
                "env_allowlist": {},
                "timeout_seconds": 180,
                "network_policy": "denied",
                "expected_exit": 0,
                "expected_outputs": [{
                    "path_or_stream": "stdout",
                    "semantic_hash_policy": "contains PASS THM-M-0419 obligation tree",
                }],
                "covered_obligation_ids": [identifier],
                "covered_declarations": covered_declarations.get(identifier, []),
                "coverage_semantics": (
                    "provisional_conditional_interface_validation"
                    if identifier in covered_declarations
                    else "open_state_architecture_classification_only"
                ),
                "closure_credit": False,
            }
            for identifier in ids
        ],
        "status_boundary": "Every recipe validates architecture or an explicitly conditional interface. No recipe supplies substantive proof or accepted closure credit.",
    }
    return registry, bundle, recipes


def render(value: dict) -> str:
    return json.dumps(value, indent=2, ensure_ascii=True) + "\n"


def main() -> None:
    registry, bundle, recipes = build()
    for name, value in (
        ("obligation-registry.json", registry),
        ("typed-graphs.json", bundle),
        ("validation-specs.json", recipes),
    ):
        (HERE / name).write_text(render(value), encoding="utf-8")
    edge_count = sum(len(value["edges"]) for value in bundle["graphs"].values())
    print(f"generated {len(registry['obligations'])} obligations and {edge_count} typed edges")
    print(f"registry denominator sha256: {registry['denominator_sha256']}")


if __name__ == "__main__":
    main()
