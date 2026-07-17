#!/usr/bin/env python3
"""Generate the theorem-level Stage1 v2 dependency and reuse DAG.

The 10822-row checklist embedded in ``Docs/Stage1_Blueprint_v2.md`` is the
state authority.  The execution and theorem JSON DAGs are derived projections.
Only audited, machine-readable dependencies are hard edges; useful but
unintegrated common results are nonblocking reuse hints.
"""

from __future__ import annotations

from collections import Counter, defaultdict
import hashlib
import heapq
import json
from pathlib import Path
import re
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
TARGETS = ROOT / "Docs" / "Stage1_Targets_rev-5.6.json"
BLUEPRINT = ROOT / "Docs" / "Stage1_Blueprint_v2.md"
LEGACY_DAG = ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json"
OUTPUT = ROOT / "Docs" / "Stage1_Theorem_DAG_v2.json"
PHASES = ("intake", "statement", "anchor_audit", "obligation_tree", "proof", "validation", "release")
PHASE_DELIVERABLES = {
    "intake": "Create the theorem dossier, scope map, and source-statement crosswalk.",
    "statement": "Elaborate the exact Lean 4 target with the minimal pinned imports.",
    "anchor_audit": "Audit mathlib and external Lean 4 candidates at immutable revisions.",
    "obligation_tree": "Freeze the obligation registry and typed proof/provenance/workflow graphs.",
    "proof": "Implement or pin/import the required proof bodies without placeholders.",
    "validation": "Run hermetic kernel, trust, provenance, and independent validation gates.",
    "release": "Reconcile evidence and decide the exact theorem-completion verdict.",
}
VALID_STATES = {"[ ]", "[_]", "[x]"}
CHECKLIST_BEGIN = "<!-- STAGE1-EXECUTION-CHECKLIST:BEGIN -->"
CHECKLIST_END = "<!-- STAGE1-EXECUTION-CHECKLIST:END -->"
CHECKLIST_ROW_RE = re.compile(
    r"^- (?P<state>\[[_x ]\]) `(?P<id>S56-M-\d{4}-(?:INTAKE|STATEMENT|ANCHOR_AUDIT|OBLIGATION_TREE|PROOF|VALIDATION|RELEASE))`"
    r" / `(?P<theorem>THM-M-\d{4})` / `(?P<phase>intake|statement|anchor_audit|obligation_tree|proof|validation|release)`"
    r": (?P<deliverable>.+?) \{attempts=(?P<attempts>\d+)\}$"
    r"\n(?P<detail>  Depends: .+)$",
    re.MULTILINE,
)
BUCKET_ORDER = {
    "master_complete": 0,
    "fully_self_tested": 1,
    "partial": 2,
    "unstarted": 3,
}
EXECUTION_CONTRACT = {
    "claim_order": ["v2_execution_rank", "phase_layer", "phase_item_id"],
    "proof_parent_inspection": {
        "scope": ["direct_hard_parents", "transitive_hard_ancestors"],
        "order": "ascending_v2_execution_rank_parent_before_child",
        "complete_closure_required": True,
    },
    "accepted_reuse_relationships": ["exact", "checked_transport"],
    "checked_transport_requires": [
        "content_bound_provider_source",
        "provider_and_consumer_statement_fingerprints",
        "consumer_owned_import_or_wrapper",
        "consumer_validation_receipt",
    ],
    "provider_checkbox_state_is_observation_only": True,
    "provider_acceptance_inherited": False,
    "consumer_acceptance_required": True,
}
IMPORT_RE = re.compile(r"^\s*import\s+.*?[«.]?(THM-M-\d{4})[».]?(?:\.|»)", re.MULTILINE)
MODULE_IDENTITY_KEYS = {
    "module",
    "source_module",
    "lean_module",
    "import_module",
    "module_name",
    "minimal_import_module",
    "terminal_module",
}
TERMINAL_IDENTITY_KEYS = {
    "terminal_proof_body_id",
    "terminal_root_declaration",
    "source_declaration",
    "terminal_declaration",
    "composition_declaration",
}
LEAN_MODULE_ID = re.compile(r"[A-Za-z_][A-Za-z0-9_']*(?:\.[A-Za-z_][A-Za-z0-9_']*)*")
LEAN_DECLARATION_ID = re.compile(r"[A-Za-z_][A-Za-z0-9_']*(?:\.[A-Za-z_][A-Za-z0-9_']*)+")
PINNED_GLOBAL_DECLARATION_ID = re.compile(
    r"mathlib:[0-9a-f]{7,64}:[A-Za-z_][A-Za-z0-9_']*(?:\.[A-Za-z_][A-Za-z0-9_']*)+"
)
LEAN_RESERVED_SEGMENTS = {
    "and", "as", "axiom", "by", "class", "constant", "def", "deriving",
    "do", "else", "end", "example", "export", "extends", "for", "from",
    "fun", "if", "import", "in", "include", "inductive", "infix", "instance",
    "let", "macro", "match", "namespace", "opaque", "open", "private", "protected",
    "section", "structure", "syntax", "theorem", "then", "universe", "variable", "where",
    "with",
}


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise RuntimeError(f"{path.relative_to(ROOT)} must contain an object")
    return value


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def canonical_sha256(value: Any) -> str:
    payload = json.dumps(value, ensure_ascii=True, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def evidence(path: str, locator: str, evidence_kind: str) -> dict[str, str]:
    source = ROOT / path
    if not source.is_file():
        raise RuntimeError(f"missing dependency evidence: {path}")
    return {
        "path": path,
        "locator": locator,
        "evidence_kind": evidence_kind,
        "sha256": file_sha256(source),
    }


def material_source(path: str, declarations: list[str]) -> dict[str, Any]:
    """Content-bind one admitted Lean source and the declarations it may supply."""
    source = ROOT / path
    if not source.is_file() or source.suffix != ".lean":
        raise RuntimeError(f"missing hard-edge Lean material: {path}")
    if not declarations or any(not isinstance(name, str) or not name for name in declarations):
        raise RuntimeError(f"hard-edge material lacks declarations: {path}")
    return {
        "path": path,
        "sha256": file_sha256(source),
        "declarations": sorted(set(declarations)),
    }


def phase_bucket(states: list[str]) -> str:
    if all(state == "[x]" for state in states):
        return "master_complete"
    if all(state == "[_]" for state in states):
        return "fully_self_tested"
    if all(state == "[ ]" for state in states):
        return "unstarted"
    return "partial"


def blueprint_state_items() -> list[dict[str, Any]]:
    """Read the state cursor only from the v2 blueprint checklist."""
    text = BLUEPRINT.read_text(encoding="utf-8")
    if text.count(CHECKLIST_BEGIN) != 1 or text.count(CHECKLIST_END) != 1:
        raise RuntimeError("v2 blueprint must contain exactly one execution checklist")
    body = text.split(CHECKLIST_BEGIN, 1)[1].split(CHECKLIST_END, 1)[0]
    matches = list(CHECKLIST_ROW_RE.finditer(body))
    items = [
        {
            "id": match["id"],
            "theorem_id": match["theorem"],
            "phase": match["phase"],
            "state": match["state"],
            "attempts": int(match["attempts"]),
        }
        for match in matches
    ]
    if len(items) != 1546 * len(PHASES) or len({item["id"] for item in items}) != len(items):
        raise RuntimeError("v2 blueprint checklist state coverage is incomplete or duplicated")
    targets = load_json(TARGETS).get("targets")
    if not isinstance(targets, list) or len(targets) != 1546:
        raise RuntimeError("target manifest must contain exactly 1546 targets")
    expected_order = [
        (target.get("theorem_id"), phase)
        for target in targets
        for phase in PHASES
    ]
    if [(item["theorem_id"], item["phase"]) for item in items] != expected_order:
        raise RuntimeError("v2 blueprint checklist is not in canonical target/phase order")
    for match, item in zip(matches, items):
        theorem_id, phase = item["theorem_id"], item["phase"]
        phase_index = PHASES.index(phase)
        expected_id = f"S56-{theorem_id.removeprefix('THM-')}-{phase.upper()}"
        dependency = "none" if phase_index == 0 else f"`S56-{theorem_id.removeprefix('THM-')}-{PHASES[phase_index - 1].upper()}`"
        expected_detail = (
            f"  Depends: {dependency}. Owned paths: `Stage1_Instances/{theorem_id}`. "
            "Gate: rev-5.6 node-specific receipt and master acceptance."
        )
        if (
            item["id"] != expected_id
            or match["deliverable"] != PHASE_DELIVERABLES[phase]
            or match["detail"] != expected_detail
        ):
            raise RuntimeError(f"v2 blueprint checklist row is noncanonical: {item['id']}")
    counts = Counter(item["state"] for item in items)
    summary = (
        "Authoritative progress summary (derived and validated from the rows below):\n"
        f"- `[_]` {counts['[_]']} ({100 * counts['[_]'] / len(items):.2f}% worker self-tested)\n"
        f"- `[ ]` {counts['[ ]']}\n"
        f"- `[x]` {counts['[x]']}"
    )
    if body.count(summary) != 1:
        raise RuntimeError("v2 blueprint progress summary is missing, duplicated, or stale")
    return items


def discover_cross_target_imports(target_ids: set[str]) -> list[tuple[str, str, list[dict[str, str]]]]:
    """Return parent, child, evidence for every exact cross-target Lean import."""
    found: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    instances = ROOT / "Stage1_Instances"
    for source in sorted(instances.glob("THM-M-*")):
        if not source.is_dir() or source.name not in target_ids:
            continue
        child = source.name
        for lean_path in sorted(source.rglob("*.lean")):
            text = lean_path.read_text(encoding="utf-8", errors="replace")
            for match in IMPORT_RE.finditer(text):
                parent = match.group(1)
                if parent in target_ids and parent != child:
                    line = text.count("\n", 0, match.start()) + 1
                    found[(parent, child)].append(
                        evidence(rel(lean_path), f"line:{line}", "exact_cross_target_lean_import")
                    )
    return [(parent, child, rows) for (parent, child), rows in sorted(found.items())]


def hard_edges(target_ids: set[str]) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    exact_imports = discover_cross_target_imports(target_ids)
    for parent, child, rows in exact_imports:
        # A cross-target import is hard only when a receipt binds the imported
        # provider content.  At present THM-M-0990 supplies that complete audit.
        receipt_path = ROOT / "Stage1_Instances" / child / "proof-receipt.json"
        receipt = load_json(receipt_path) if receipt_path.is_file() else {}
        dependency_key = parent.lower().replace("-", "_") + "_dependency"
        bound = receipt.get("inputs", {}).get(dependency_key) if isinstance(receipt.get("inputs"), dict) else None
        if not isinstance(bound, dict):
            raise RuntimeError(f"cross-target import {parent} -> {child} lacks a content-binding proof receipt")
        provider_dir = ROOT / "Stage1_Instances" / parent
        imported_sources: list[Path] = []
        for row in rows:
            line = (ROOT / row["path"]).read_text(encoding="utf-8").splitlines()[int(row["locator"].split(":")[1]) - 1]
            module = line.rsplit(".", 1)[-1].replace("»", "").strip()
            candidate = provider_dir / f"{module}.lean"
            if candidate.is_file():
                imported_sources.append(candidate)
        for imported in imported_sources:
            if file_sha256(imported) not in set(bound.values()):
                raise RuntimeError(f"receipt hash does not bind imported source {rel(imported)}")
        # The edge contract is deliberately narrower than the provider owner.
        # It records only source bytes and declarations actually consumed by
        # the admitted import/replay route; an unrelated theorem in the same
        # directory therefore cannot satisfy an accepted hard-edge decision.
        if (parent, child) != ("THM-M-0989", "THM-M-0990"):
            raise RuntimeError(f"unreviewed cross-target proof material: {parent} -> {child}")
        provider_sources = [
            material_source(
                "Stage1_Instances/THM-M-0989/Statement.lean",
                ["Stage1Instances.THM_M_0989.truncatedSecondMoment"],
            ),
            material_source(
                "Stage1_Instances/THM-M-0989/Proof.lean",
                [
                    "Stage1Instances.THM_M_0989.integrable_truncatedSecondMoment_integrand",
                    "Stage1Instances.THM_M_0989.truncatedSecondMoment_nonneg",
                ],
            ),
            material_source(
                "Stage1_Instances/THM-M-0989/CharFunBound.lean",
                [
                    "Stage1Instances.THM_M_0989.CharFunBound.norm_cexp_mul_I_sub_one_sub_le_half_sq",
                    "Stage1Instances.THM_M_0989.CharFunBound.norm_cexp_mul_I_sub_taylor_two_le",
                    "Stage1Instances.THM_M_0989.CharFunBound.norm_cexp_mul_I_sub_taylor_two_le_crude",
                ],
            ),
        ]
        receipt_hashes = {value for key, value in bound.items() if key.endswith("_sha256")}
        if any(row["sha256"] not in receipt_hashes for row in provider_sources):
            raise RuntimeError(f"proof receipt does not bind every admitted provider source: {parent} -> {child}")
        consumer_sources = [
            material_source(
                "Stage1_Instances/THM-M-0990/GeneralizedLindeberg.lean",
                [
                    "Stage1Instances.THM_M_0990.eventualLindebergFeller_exact",
                    "Stage1Instances.THM_M_0990.secondMoment_le_sq_add_truncated",
                ],
            )
        ]
        rows.append(evidence(rel(receipt_path), f"/inputs/{dependency_key}", "content_binding_receipt"))
        result.append(
            {
                "edge_id": f"HARD-{parent}-{child}-PROOF",
                "edge_type": "proof_dependency",
                "parent_theorem_id": parent,
                "child_theorem_id": child,
                "blocking": True,
                "evidence_strength": "A_exact_import_and_content_bound_receipt",
                "evidence": rows,
                "material_contract": {
                    "contract_kind": "cross_target_import_and_proof_receipt_input",
                    "provider_sources": provider_sources,
                    "consumer_sources": consumer_sources,
                    "receipt_input_binding": {
                        "path": rel(receipt_path),
                        "sha256": file_sha256(receipt_path),
                        "json_pointer": f"/inputs/{dependency_key}",
                    },
                },
                "state_semantics": "orders proof preparation; never transfers checkbox state or theorem-completion credit",
            }
        )

    # THM-M-0320's checker consumes content-addressed THM-M-0318 vendor files.
    # This is an artifact-availability/hash hard edge, not inherited theorem state.
    source_record_path = ROOT / "Stage1_Instances/THM-M-0320/brouwer-source.json"
    if source_record_path.is_file():
        record = load_json(source_record_path)
        parent = record.get("source_theorem_id")
        child = record.get("theorem_id")
        hashes = record.get("source_path_sha256")
        if parent in target_ids and child in target_ids and isinstance(hashes, dict) and hashes:
            for path, expected in hashes.items():
                source = ROOT / path
                if not source.is_file() or file_sha256(source) != expected:
                    raise RuntimeError(f"cross-target source binding is stale: {path}")
            if (parent, child) != ("THM-M-0318", "THM-M-0320"):
                raise RuntimeError(f"unreviewed cross-target artifact material: {parent} -> {child}")
            provider_sources = [
                material_source(
                    "Stage1_Instances/THM-M-0318/Vendor/Gametheory/Brouwer.lean",
                    ["Brouwer"],
                )
            ]
            if any(row["path"] not in hashes or hashes[row["path"]] != row["sha256"] for row in provider_sources):
                raise RuntimeError("artifact provider allowlist is not derived from source_path_sha256")
            consumer_sources = [
                material_source(
                    "Stage1_Instances/THM-M-0320/Proof.lean",
                    [
                        "Stage1Instances.THM_M_0320.closedGraphKakutaniCore",
                        "Stage1Instances.THM_M_0320.schauderFixedPoint",
                    ],
                )
            ]
            result.append(
                {
                    "edge_id": f"HARD-{parent}-{child}-ARTIFACT",
                    "edge_type": "artifact_dependency",
                    "parent_theorem_id": parent,
                    "child_theorem_id": child,
                    "blocking": True,
                    "evidence_strength": "B_structured_source_id_path_hash_and_replay_input",
                    "evidence": [
                        evidence(rel(source_record_path), "/source_theorem_id,/source_path_sha256", "structured_content_binding"),
                        evidence("Stage1_Instances/THM-M-0320/BrouwerSource.lean", "line:1", "consumer_adapter_import"),
                        evidence("Stage1_Instances/THM-M-0320/check_proof.sh", "cross-target source replay", "validator_consumes_provider_artifact"),
                        evidence("Stage1_Instances/THM-M-0320/proof-receipt.json", "/proof_route/source_boundary", "proof_receipt_boundary"),
                    ],
                    "material_contract": {
                        "contract_kind": "source_manifest_and_consumer_adapter",
                        "provider_sources": provider_sources,
                        "consumer_sources": consumer_sources,
                        "source_manifest_binding": {
                            "path": rel(source_record_path),
                            "sha256": file_sha256(source_record_path),
                            "source_theorem_id_pointer": "/source_theorem_id",
                            "source_path_sha256_pointer": "/source_path_sha256",
                            "source_declaration_pointer": "/source_declaration",
                            "consumer_adapter_path": "Stage1_Instances/THM-M-0320/BrouwerSource.lean",
                            "consumer_adapter_sha256": file_sha256(ROOT / "Stage1_Instances/THM-M-0320/BrouwerSource.lean"),
                            "consumer_replay_path": "Stage1_Instances/THM-M-0320/check_proof.sh",
                            "consumer_replay_sha256": file_sha256(ROOT / "Stage1_Instances/THM-M-0320/check_proof.sh"),
                        },
                    },
                    "state_semantics": "blocks only on provider artifact availability/hash; never requires or inherits provider checkbox state",
                }
            )
    return sorted(result, key=lambda edge: edge["edge_id"])


def reuse_hints(target_ids: set[str]) -> list[dict[str, Any]]:
    specs = [
        (
            "REUSE-THM-M-0318-THM-M-0319-ADAPTATION",
            "adaptation_provenance",
            "THM-M-0318",
            "THM-M-0319",
            "medium",
            [("Stage1_Instances/THM-M-0319/proof-receipt.json", "/proof_body/local_reuse_provenance", "named_local_adaptation")],
            "inspect the provider proof before rebuilding the compact-minimization bridge; an exact checked transport is still absent",
        ),
        (
            "REUSE-THM-M-1057-THM-M-1056-KINGMAN",
            "shared_lemma_candidate",
            "THM-M-1057",
            "THM-M-1056",
            "checked_candidate",
            [("Stage1_Instances/THM-M-1056/proof-recheck-2026-07-15-head-31db90ba.json", "/repo_local_kingman", "named_checked_declarations")],
            "Kingman declarations can discharge an analytic input only after a target-local adapter and composition check",
        ),
        (
            "REUSE-THM-M-1057-THM-M-1419-KINGMAN",
            "shared_lemma_candidate",
            "THM-M-1057",
            "THM-M-1419",
            "checked_candidate",
            [("Stage1_Instances/THM-M-1419/proof-recheck-2026-07-15-head-f26cfacf-slot49.json", "/available_checked_inputs", "named_checked_declarations")],
            "Kingman is one analytic input and does not construct the Oseledets splitting",
        ),
        (
            "REUSE-THM-M-0990-THM-M-1063-CLT",
            "shared_lemma_candidate",
            "THM-M-0990",
            "THM-M-1063",
            "checked_candidate",
            [("Stage1_Instances/THM-M-1063/proof-recheck-2026-07-15-head-557b928b-slot59.json", "/newly_available_unintegrated_support/0", "named_checked_declaration_with_source_hash")],
            "generic CLT is reusable, but weighted-row construction, limit transport, and target composition remain open",
        ),
        (
            "REUSE-THM-M-1013-THM-M-1063-CRAMER-WOLD",
            "shared_lemma_candidate",
            "THM-M-1013",
            "THM-M-1063",
            "checked_candidate",
            [("Stage1_Instances/THM-M-1063/proof-recheck-2026-07-15-head-557b928b-slot59.json", "/newly_available_unintegrated_support/1", "named_checked_declaration_with_source_hash")],
            "Cramer-Wold is reusable, but evaluation-vector laws and scalar projection limits remain open",
        ),
    ]
    result = []
    for hint_id, kind, provider, consumer, confidence, evidence_specs, boundary in specs:
        if provider not in target_ids or consumer not in target_ids:
            raise RuntimeError(f"reuse hint endpoint outside target set: {hint_id}")
        result.append(
            {
                "hint_id": hint_id,
                "hint_type": kind,
                "provider_theorem_id": provider,
                "consumer_theorem_id": consumer,
                "blocking": False,
                "confidence": confidence,
                "evidence": [evidence(path, locator, evidence_kind) for path, locator, evidence_kind in evidence_specs],
                "reuse_boundary": boundary,
            }
        )
    return result


def structured_identity_values(value: Any, key: str | None = None) -> list[tuple[str, str]]:
    """Extract only allowlisted structured module/proof-body identities."""
    result: list[tuple[str, str]] = []
    if isinstance(value, dict):
        for child_key, child in value.items():
            result.extend(structured_identity_values(child, child_key))
    elif isinstance(value, list):
        for child in value:
            result.extend(structured_identity_values(child, key))
    elif isinstance(value, str) and key in MODULE_IDENTITY_KEYS | TERMINAL_IDENTITY_KEYS:
        identity = value.strip()
        if identity and identity.lower() not in {"none", "null", "unknown", "not_applicable", "not applicable"}:
            kind = "lean_module" if key in MODULE_IDENTITY_KEYS else "terminal_proof_body"
            result.append((kind, identity))
    return result


def valid_lean_module_identity(identity: str) -> bool:
    """Accept one syntactically unambiguous module name, never prose/path lists."""
    return (
        LEAN_MODULE_ID.fullmatch(identity) is not None
        and all(segment not in LEAN_RESERVED_SEGMENTS for segment in identity.split("."))
    )


def local_terminal_identity(identity: str) -> bool:
    """Identify target-local/path identities which must never merge globally."""
    lowered = identity.lower()
    return (
        lowered.startswith(("local:", "repo-local:", "repo_local:", "path:", "file:"))
        or identity.startswith(("Stage1_Instances.", "Stage1Instances.THM_", "AwesomeTheorems.Stage1.S1_M_"))
        or "/" in identity
        or "\\" in identity
        or lowered.endswith((".lean", ".json", ".yaml", ".yml", ".md"))
    )


def valid_global_terminal_identity(identity: str) -> bool:
    """Keep only globally named declarations or revision-qualified global bodies."""
    if local_terminal_identity(identity):
        return False
    return (
        LEAN_DECLARATION_ID.fullmatch(identity) is not None
        or PINNED_GLOBAL_DECLARATION_ID.fullmatch(identity) is not None
    )


def shared_lemma_groups(target_ids: set[str]) -> list[dict[str, Any]]:
    """Aggregate strict module clusters and truly global terminal bodies only."""
    occurrences: dict[tuple[str, str], dict[str, set[str]]] = defaultdict(lambda: defaultdict(set))
    for theorem_id in sorted(target_ids):
        directory = ROOT / "Stage1_Instances" / theorem_id
        if not directory.is_dir():
            continue
        for path in sorted(directory.rglob("*.json")):
            # Reuse ledgers are derived consumers of this graph. Including
            # them as discovery inputs would make a proof handoff mutate its
            # own dependency context and create a self-invalidating cycle.
            if path.name == "dependency-reuse-ledger.json":
                continue
            try:
                value = json.loads(path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                continue
            for identity_kind, identity in set(structured_identity_values(value)):
                if identity_kind == "lean_module" and not valid_lean_module_identity(identity):
                    continue
                if identity_kind == "terminal_proof_body":
                    if local_terminal_identity(identity):
                        # Namespace local identities before aggregation.  The
                        # theorem-qualified key cannot become a cross-target
                        # shared group, which is the intended fail-closed result.
                        identity = f"{theorem_id}::{identity}"
                    elif not valid_global_terminal_identity(identity):
                        continue
                occurrences[(identity_kind, identity)][theorem_id].add(rel(path))
    result = []
    for (identity_kind, identity), by_theorem in sorted(occurrences.items()):
        if len(by_theorem) < 2:
            continue
        group_type = "shared_module_cluster" if identity_kind == "lean_module" else "shared_terminal_body"
        digest = hashlib.sha256(f"{group_type}\0{identity}".encode("utf-8")).hexdigest()[:16]
        evidence_paths = sorted({path for paths in by_theorem.values() for path in paths})
        result.append(
            {
                "group_id": f"SHARED-{'MODULE' if identity_kind == 'lean_module' else 'TERMINAL'}-{digest}",
                "group_type": group_type,
                "identity_kind": identity_kind,
                "canonical_identity": identity,
                "member_theorem_ids": sorted(by_theorem),
                "evidence_paths": evidence_paths,
                "confidence": "hint",
                "blocking": False,
                "reuse_boundary": (
                    "weak shared-module co-mention only, not a common lemma or proof body; inspect exact imports and declarations before reuse"
                    if group_type == "shared_module_cluster"
                    else "shared global terminal-body identity only; inspect exact types, imports, adapters, provenance, and receipts before credit"
                ),
            }
        )
    return result


def inventory(theorem_id: str) -> tuple[dict[str, Any], list[dict[str, str]]]:
    directory = ROOT / "Stage1_Instances" / theorem_id
    if not directory.is_dir():
        return (
            {
                "instance_directory": f"Stage1_Instances/{theorem_id}",
                "instance_directory_exists": False,
                "lean_sources": [],
                "receipt_files": [],
                "structured_json_files": [],
            },
            [],
        )
    lean = sorted(rel(path) for path in directory.rglob("*.lean") if path.is_file())
    receipts = sorted(rel(path) for path in directory.rglob("*receipt*.json") if path.is_file())
    structured = sorted(rel(path) for path in directory.rglob("*.json") if path.is_file())
    reusable_paths = sorted(set(lean + receipts + [path for path in structured if "source" in Path(path).name.lower()]))
    reusable = []
    for path in reusable_paths:
        name = Path(path).name.lower()
        kind = "lean_source" if path.endswith(".lean") else "evidence_receipt" if "receipt" in name else "dependency_source_manifest"
        reusable.append({"path": path, "artifact_kind": kind, "sha256": file_sha256(ROOT / path)})
    return (
        {
            "instance_directory": rel(directory),
            "instance_directory_exists": True,
            "lean_sources": lean,
            "receipt_files": receipts,
            "structured_json_files": structured,
        },
        reusable,
    )


def topological_metadata(
    theorem_ids: set[str], edges: list[dict[str, Any]], buckets: dict[str, str], original_ranks: dict[str, int]
) -> tuple[list[str], dict[str, int], dict[str, list[str]], dict[str, list[str]], dict[str, list[str]]]:
    parents: dict[str, list[str]] = {theorem_id: [] for theorem_id in theorem_ids}
    children: dict[str, list[str]] = {theorem_id: [] for theorem_id in theorem_ids}
    for edge in edges:
        parent, child = edge["parent_theorem_id"], edge["child_theorem_id"]
        parents[child].append(parent)
        children[parent].append(child)
    parents = {key: sorted(value) for key, value in parents.items()}
    children = {key: sorted(value) for key, value in children.items()}
    indegree = {theorem_id: len(parents[theorem_id]) for theorem_id in theorem_ids}
    layer = {theorem_id: 0 for theorem_id in theorem_ids}
    ready: list[tuple[int, int, int, str]] = []
    for theorem_id, degree in indegree.items():
        if degree == 0:
            heapq.heappush(ready, (BUCKET_ORDER[buckets[theorem_id]], 0, original_ranks[theorem_id], theorem_id))
    ordered: list[str] = []
    while ready:
        _, _, _, theorem_id = heapq.heappop(ready)
        ordered.append(theorem_id)
        for child in children[theorem_id]:
            layer[child] = max(layer[child], layer[theorem_id] + 1)
            indegree[child] -= 1
            if indegree[child] == 0:
                heapq.heappush(
                    ready,
                    (BUCKET_ORDER[buckets[child]], layer[child], original_ranks[child], child),
                )
    if len(ordered) != len(theorem_ids):
        raise RuntimeError("hard theorem dependency graph contains a cycle")
    order_index = {theorem_id: index for index, theorem_id in enumerate(ordered)}
    ancestors: dict[str, list[str]] = {}
    for theorem_id in ordered:
        closure = set(parents[theorem_id])
        for parent in parents[theorem_id]:
            closure.update(ancestors[parent])
        ancestors[theorem_id] = sorted(closure, key=order_index.__getitem__)
        if any(order_index[ancestor] >= order_index[theorem_id] for ancestor in ancestors[theorem_id]):
            raise RuntimeError(f"hard ancestor is not ordered before its consumer: {theorem_id}")
    return ordered, layer, parents, children, ancestors


def build() -> dict[str, Any]:
    target_manifest = load_json(TARGETS)
    targets = target_manifest.get("targets")
    items = blueprint_state_items()
    if not isinstance(targets, list) or len(targets) != 1546:
        raise RuntimeError("target manifest must contain exactly 1546 targets")
    if not isinstance(items, list) or len(items) != 1546 * len(PHASES):
        raise RuntimeError("v2 blueprint must contain exactly 10822 phase items")
    target_ids = {target["theorem_id"] for target in targets}
    if len(target_ids) != 1546:
        raise RuntimeError("target IDs are not unique")
    by_target: dict[str, dict[str, dict[str, Any]]] = defaultdict(dict)
    for item in items:
        if item.get("theorem_id") not in target_ids or item.get("phase") not in PHASES:
            raise RuntimeError(f"invalid legacy item: {item.get('id')}")
        if item.get("state") not in VALID_STATES or item["phase"] in by_target[item["theorem_id"]]:
            raise RuntimeError(f"invalid or duplicate blueprint phase: {item.get('id')}")
        by_target[item["theorem_id"]][item["phase"]] = item
    if any(set(by_target[theorem_id]) != set(PHASES) for theorem_id in target_ids):
        raise RuntimeError("blueprint phase coverage is incomplete")

    target_by_id = {target["theorem_id"]: target for target in targets}
    original_ranks = {theorem_id: target_by_id[theorem_id]["execution_rank"] for theorem_id in target_ids}
    buckets = {
        theorem_id: phase_bucket([by_target[theorem_id][phase]["state"] for phase in PHASES])
        for theorem_id in target_ids
    }
    hard = hard_edges(target_ids)
    hints = reuse_hints(target_ids)
    shared_groups = shared_lemma_groups(target_ids)
    order, layers, parents, children, ancestors = topological_metadata(target_ids, hard, buckets, original_ranks)
    v2_ranks = {theorem_id: rank for rank, theorem_id in enumerate(order, 1)}
    hints_by_consumer: dict[str, list[str]] = defaultdict(list)
    for hint in hints:
        hints_by_consumer[hint["consumer_theorem_id"]].append(hint["hint_id"])
    groups_by_theorem: dict[str, list[str]] = defaultdict(list)
    for group in shared_groups:
        for theorem_id in group["member_theorem_ids"]:
            groups_by_theorem[theorem_id].append(group["group_id"])
    hard_by_child: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for edge in hard:
        hard_by_child[edge["child_theorem_id"]].append(edge)
    hint_by_id = {hint["hint_id"]: hint for hint in hints}
    group_by_id = {group["group_id"]: group for group in shared_groups}

    theorem_rows = []
    for theorem_id in order:
        target = target_by_id[theorem_id]
        phase_states = {phase: by_target[theorem_id][phase]["state"] for phase in PHASES}
        phase_attempts = {phase: by_target[theorem_id][phase].get("attempts", 0) for phase in PHASES}
        evidence_inventory, reusable_artifacts = inventory(theorem_id)
        if parents[theorem_id]:
            audit_status = "audited_hard_dependency_found"
        elif hints_by_consumer[theorem_id] or groups_by_theorem[theorem_id]:
            audit_status = "audited_reuse_only"
        else:
            audit_status = "unknown_not_independent_proof_claim"
        context_nodes = set(ancestors[theorem_id]) | {theorem_id}
        dependency_context = {
            "direct_hard_parents": parents[theorem_id],
            "transitive_hard_ancestors": ancestors[theorem_id],
            "hard_edges": sorted(
                (
                    edge
                    for child in context_nodes
                    for edge in hard_by_child[child]
                    if edge["parent_theorem_id"] in context_nodes
                ),
                key=lambda edge: edge["edge_id"],
            ),
            "direct_reuse_hints": [
                hint_by_id[hint_id] for hint_id in sorted(hints_by_consumer[theorem_id])
            ],
            "shared_groups": [
                group_by_id[group_id] for group_id in sorted(groups_by_theorem[theorem_id])
            ],
        }
        theorem_rows.append(
            {
                "theorem_id": theorem_id,
                "name": target["name"],
                "category": target["category"],
                "original_execution_rank": original_ranks[theorem_id],
                "v2_execution_rank": v2_ranks[theorem_id],
                "completion_bucket": buckets[theorem_id],
                "phase_states": phase_states,
                "phase_attempts": phase_attempts,
                "state_counts": dict(sorted(Counter(phase_states.values()).items())),
                "topological_layer": layers[theorem_id],
                "direct_hard_parents": parents[theorem_id],
                "direct_hard_children": children[theorem_id],
                "transitive_hard_ancestors": ancestors[theorem_id],
                "direct_reuse_hint_ids": sorted(hints_by_consumer[theorem_id]),
                "shared_lemma_group_ids": sorted(groups_by_theorem[theorem_id]),
                "dependency_context_sha256": canonical_sha256(dependency_context),
                "dependency_audit_status": audit_status,
                "evidence_inventory": evidence_inventory,
                "reusable_artifacts": reusable_artifacts,
            }
        )

    state_records = [
        {"id": item["id"], "state": item["state"], "attempts": item.get("attempts", 0)}
        for item in sorted(items, key=lambda row: row["id"])
    ]
    bucket_counts = Counter(buckets.values())
    return {
        "schema_version": "stage1-theorem-dag/2.0",
        "generated_by": "Docs/tools/generate_stage1_theorem_dag_v2.py",
        "requirements_source": "Docs/Stage1_Blueprint_v2.md",
        "target_manifest": "Docs/Stage1_Targets_rev-5.6.json",
        # Read-only projection path. It contains no independently writable
        # state; all marks and attempts originate in the v2 blueprint.
        "execution_dag_projection": "Docs/Stage1_Execution_DAG_rev-5.6.json",
        "target_id_set_sha256": target_manifest["scope"]["canonical_sorted_target_id_set_sha256"],
        "state_protocol": {"not_done": "[ ]", "worker_self_tested": "[_]", "master_accepted": "[x]"},
        "completion_bucket_order": list(BUCKET_ORDER),
        "execution_contract": EXECUTION_CONTRACT,
        "edge_policy": {
            "hard_edge_admission": "exact cross-target Lean import plus content-bound receipt, or structured source theorem/path hashes consumed by a replay validator",
            "reuse_hint_admission": "named provider theorem/declaration/module with reviewable evidence but no checked target-local import/transport",
            "unknown_policy": "absence of an admitted edge is unknown_not_independent_proof_claim, never proof of independence",
            "hard_dependency_worker_policy": "before proof work, inspect every direct and transitive hard parent plus its reusable artifacts",
            "reuse_hint_worker_policy": "inspect hints opportunistically; hints never block claims, acceptance, or transfer checkbox state",
        },
        "blueprint_state_snapshot": {
            "authoritative_blueprint": "Docs/Stage1_Blueprint_v2.md",
            "authoritative_blueprint_sha256": file_sha256(BLUEPRINT),
            "item_count": len(items),
            "item_state_counts": dict(sorted(Counter(item["state"] for item in items).items())),
            "item_state_attempts_sha256": canonical_sha256(state_records),
        },
        "graph_summary": {
            "theorem_count": len(theorem_rows),
            "hard_edge_count": len(hard),
            "reuse_hint_count": len(hints),
            "shared_lemma_group_count": len(shared_groups),
            "shared_group_type_counts": dict(sorted(Counter(group["group_type"] for group in shared_groups).items())),
            "root_count": sum(not parents[theorem_id] for theorem_id in target_ids),
            "max_topological_layer": max(layers.values(), default=0),
            "completion_bucket_counts": {bucket: bucket_counts[bucket] for bucket in BUCKET_ORDER},
            "dependency_audit_status_counts": dict(sorted(Counter(row["dependency_audit_status"] for row in theorem_rows).items())),
        },
        "hard_edges": hard,
        "reuse_hints": hints,
        "shared_lemma_groups": shared_groups,
        "theorems": theorem_rows,
    }


def main() -> None:
    output = build()
    OUTPUT.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(
        "generate_stage1_theorem_dag_v2: ok "
        f"({len(output['theorems'])} theorems, {len(output['hard_edges'])} hard edges, "
        f"{len(output['reuse_hints'])} nonblocking reuse hints, "
        f"{len(output['shared_lemma_groups'])} shared-identity groups)"
    )


if __name__ == "__main__":
    main()
