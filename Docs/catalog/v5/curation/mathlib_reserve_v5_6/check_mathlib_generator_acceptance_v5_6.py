#!/usr/bin/env python3
"""Independent checker and receipt writer for the mathlib v5.6 accepted set.

This checker intentionally does not import either local builder.  It derives
the canonical formal identities, parent exclusions, semantic-review screen,
and 1,092-row accepted set again from the sealed mathlib source and complete
5.5 parent catalog.  ``--write-receipt`` requires a live Lean extraction
replay; ordinary invocation rechecks all deterministic evidence and compares
the existing receipt byte-for-byte.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
from typing import Any, Iterable, Mapping, Sequence
import unicodedata


SCHEMA = "awesome-theorems/mathlib-generator-acceptance-receipt/5.6"
SOURCE_COMMIT = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
THOUSAND_PLUS_COMMIT = "8e04b97dd24adc6e931be78a884da7e935bc8780"

FULL_SHA = "7075e0bb151182ae4ba01cd34945657969be4bc60f7ee4ae6a62fc518f5386c3"
THEOREM_SHA = "f57b885995f4edf8204e96b57b7489c3dfa9d6ac96785031d0498b9ed80f46ab"
CATALOG_SHA = "9d6dc79b1cbdee401f2f022ee027557a04331fa9605dc7f443fdc09a62b029b4"
MANIFEST_SHA = "773253c2afad3a91c1b14cc9b5f60b51ec9b7e258d1619f0168dd23c9c4b0a43"
QUALIFIED_SHA = "b03a2a3df17165b7f1e4bff7e2de80a8ecea6060a115b0fed66975827fb0f039"
QUALIFIED_INVENTORY_SHA = "669ad0d5b3f7d4b26000ffc36c153f5d415fdce4f7824f85177d999a80d34ab9"
ACCEPTED_SHA = "7943e8f473aaac523d617a8debd1dda5d589187bf62844933af684172570ab86"
EXTRACTOR_SHA = "0e26af2b6740abf4626f3cf43d84fb8f7e1f1a6104096e71f1f9b1f2c33189af"
PARENT_CHECKER_SHA = "44ea7bd61f8e15f2ac48ff185ae7c9110e85a0180de00e8d4c09392fe1a2dd12"

EXPECTED_LOSER_RANKS = [38, 378, 618, 619, 2_517]
EXPECTED_COUNTS = {
    "source_screened_runtime_thmInfo_sorry_free": 2_575,
    "materialized_documented_runtime_thmInfo": 2_566,
    "canonical_formal_proposition_identities": 2_561,
    "precanonical_rejected_exact_duplicates": 5,
    "parent_theorem_records": 2_500,
    "parent_claim_records": 4_525,
    "parent_mathlib_formal_identities": 1_000,
    "unadmitted_canonical_candidates": 1_561,
    "candidate_source_syntax_theorem": 1_072,
    "candidate_source_syntax_lemma": 489,
    "machine_qualified_accepted_set": 1_092,
    "semantic_variant_review_quarantine": 469,
    "canonical_candidate_rejected": 0,
    "accepted_source_syntax_theorem": 707,
    "accepted_source_syntax_lemma": 385,
    "quarantine_source_syntax_theorem": 365,
    "quarantine_source_syntax_lemma": 104,
    "catalog_entries_granted_by_receipt": 0,
    "theorem_credits_granted_by_receipt": 0,
}


class CheckError(RuntimeError):
    pass


def find_repo(start: Path) -> Path:
    for candidate in (start, *start.parents):
        if (candidate / ".git").exists():
            return candidate
    raise CheckError("cannot find repository root")


HERE = Path(__file__).resolve().parent
REPO = find_repo(HERE)
FULL = HERE / "mathlib-verified-theorems-8a178386-full.json"
THEOREM = REPO / "Docs/catalog/v5/releases/5.5/Theorem_List.json"
CATALOG = REPO / "Docs/catalog/v5/releases/5.5/Claim_Catalog.json"
MANIFEST = REPO / "Docs/catalog/v5/releases/5.5/Release_Manifest.json"
QUALIFIED = HERE / "Mathlib_Qualified_Theorem_Candidates_v5_6.jsonl"
QUALIFIED_INVENTORY = HERE / "Mathlib_Qualified_Batch_Inventory_v5_6.json"
ACCEPTED = HERE / "Mathlib_Generator_Accepted_Set_v5_6.jsonl"
RECEIPT = HERE / "Mathlib_Generator_Acceptance_Receipt_v5_6.json"
EXTRACTOR = REPO / "Docs/tools/extract_mathlib_theorems_v5.py"
PARENT_CHECKER = REPO / "Docs/catalog/v5/tools/check_math_catalog_v5_5.py"
QUALIFIED_BUILDER = HERE / "build_mathlib_qualified_batch_v5_6.py"
ACCEPTED_BUILDER = HERE / "build_mathlib_generator_accepted_set_v5_6.py"

SHA_RE = re.compile(r"[0-9a-f]{64}")
BOLD_RE = re.compile(r"\*\*([^*\n]+?)\*\*")
NAMED_RE = re.compile(
    r"(?:theorem|inequalit(?:y|ies)|equation|principle|lemma|law|formula|"
    r"criterion|identity|duality|decomposition|classification|reciprocity|h[öo]hensatz)",
    re.IGNORECASE,
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise CheckError(message)


def canonical(value: Any) -> bytes:
    try:
        return json.dumps(
            value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False
        ).encode("utf-8")
    except (TypeError, ValueError) as error:
        raise CheckError(f"non-canonical JSON value: {error}") from error


def pretty(value: Any) -> bytes:
    return (
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True, allow_nan=False) + "\n"
    ).encode("utf-8")


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def hash_without(value: Mapping[str, Any], *fields: str) -> str:
    omitted = set(fields)
    return sha(canonical({key: item for key, item in value.items() if key not in omitted}))


def set_digest(values: Iterable[str]) -> str:
    return sha(canonical(sorted(set(values))))


def reject_constant(value: str) -> None:
    raise CheckError(f"non-finite JSON number: {value}")


def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        require(key not in result, f"duplicate JSON key {key!r}")
        result[key] = value
    return result


def parse_json(payload: bytes, label: str) -> dict[str, Any]:
    try:
        value = json.loads(
            payload.decode("utf-8"),
            object_pairs_hook=unique_object,
            parse_constant=reject_constant,
        )
    except (UnicodeError, json.JSONDecodeError) as error:
        raise CheckError(f"invalid JSON in {label}: {error}") from error
    require(isinstance(value, dict), f"{label} must contain one object")
    return value


def load_json(path: Path, expected_sha: str) -> tuple[dict[str, Any], bytes]:
    payload = path.read_bytes()
    require(sha(payload) == expected_sha, f"{path} SHA-256 drifted")
    return parse_json(payload, str(path)), payload


def load_jsonl(path: Path, expected_sha: str) -> tuple[list[dict[str, Any]], bytes]:
    payload = path.read_bytes()
    require(sha(payload) == expected_sha, f"{path} SHA-256 drifted")
    rows: list[dict[str, Any]] = []
    for line_number, raw in enumerate(payload.splitlines(), 1):
        require(bool(raw), f"{path} line {line_number} is empty")
        row = parse_json(raw, f"{path}:{line_number}")
        require(raw == canonical(row), f"{path} line {line_number} is not canonical JSON")
        require(row.get("row_sha256") == hash_without(row, "row_sha256"), f"{path} line {line_number} seal is stale")
        rows.append(row)
    return rows, payload


def normalize_type(value: str) -> str:
    return " ".join(value.split())


def normalize_name(value: str) -> str:
    return unicodedata.normalize("NFKC", value).casefold().strip()


def normalize_text(value: str) -> str:
    return " ".join(normalize_name(value).split())


def type_sha(value: str) -> str:
    return sha(normalize_type(value).encode("utf-8"))


def name_sha(value: str) -> str:
    return sha(normalize_name(value).encode("utf-8"))


def embedded_labels(values: Iterable[Any]) -> set[str]:
    result: set[str] = set()
    for value in values:
        if not isinstance(value, str):
            continue
        for raw in BOLD_RE.findall(value):
            if NAMED_RE.search(raw):
                label = normalize_text(raw).strip(" .,:;")
                if label:
                    result.add(label)
    return result


def signal_kinds(row: Mapping[str, Any]) -> set[str]:
    signals = row.get("importance_signals")
    require(isinstance(signals, list) and bool(signals), "source importance signals missing")
    kinds: set[str] = set()
    for signal in signals:
        require(isinstance(signal, dict), "source importance signal is not an object")
        kind = signal.get("kind")
        require(kind in {"mathlib_1000_theorems", "mathlib_module_main_result"}, "unknown importance signal")
        kinds.add(str(kind))
    return kinds


def module_root(row: Mapping[str, Any]) -> str:
    source = row.get("source")
    require(isinstance(source, dict), "source object missing")
    module = source.get("module")
    require(isinstance(module, str), "source module missing")
    pieces = module.split(".")
    require(len(pieces) > 1 and pieces[0] == "Mathlib", "invalid mathlib module")
    return pieces[1]


def source_features(row: Mapping[str, Any]) -> dict[str, set[str]]:
    declaration = str(row["declaration"])
    output: dict[str, set[str]] = {
        "leaf": {normalize_text(declaration.rsplit(".", 1)[-1])},
        "display": {normalize_text(str(row["display_label"]))},
        "decldoc": set(),
        "main": set(),
        "wikidata": set(),
        "named": set(),
    }
    docstring = row.get("declaration_docstring")
    if isinstance(docstring, str) and docstring.strip():
        output["decldoc"].add(normalize_text(docstring))
    named_values: list[Any] = [
        row.get("declaration_docstring"),
        row.get("formal_docstring"),
        row.get("exact_curated_summary"),
    ]
    for signal in row["importance_signals"]:
        if signal["kind"] == "mathlib_module_main_result":
            description = signal.get("description")
            require(isinstance(description, str) and bool(description.strip()), "empty module-main description")
            output["main"].add(normalize_text(description))
            named_values.append(description)
        else:
            external = signal.get("external_id")
            require(isinstance(external, str) and bool(external.strip()), "empty Wikidata ID")
            output["wikidata"].add(normalize_text(external))
            named_values.extend((signal.get("title"), signal.get("upstream_title")))
    output["named"] = embedded_labels(named_values)
    return output


def validate_source_rows(document: Mapping[str, Any]) -> list[dict[str, Any]]:
    require(document.get("schema_version") == "awesome-theorems/mathlib-theorem-source/1.0", "source schema drifted")
    body = dict(document)
    declared_digest = body.pop("content_digest_before_self_field", None)
    require(declared_digest == sha(pretty(body)), "source self digest is stale")
    snapshot = document.get("source_snapshot")
    require(isinstance(snapshot, dict), "source snapshot missing")
    require(
        snapshot.get("commit") == SOURCE_COMMIT
        and snapshot.get("module_cache_complete") is True
        and snapshot.get("available_source_modules")
        == snapshot.get("available_ilean_modules")
        == snapshot.get("available_olean_modules")
        == 7_871,
        "source environment boundary drifted",
    )
    thousand = document.get("optional_thousand_plus_snapshot")
    require(
        isinstance(thousand, dict)
        and thousand.get("commit") == THOUSAND_PLUS_COMMIT
        and thousand.get("records_loaded") == 1_200,
        "1000+ source snapshot drifted",
    )
    counts = document.get("counts")
    require(
        isinstance(counts, dict)
        and counts.get("source_screened_candidates") == 2_575
        and counts.get("lean_verified_theorem_candidates") == 2_566
        and counts.get("runtime_rejected") == 9
        and counts.get("selected_total") == 2_566,
        "source counts drifted",
    )
    exclusions = document.get("runtime_rejections")
    require(
        isinstance(exclusions, list)
        and len(exclusions) == 9
        and all(
            isinstance(row, dict)
            and row.get("runtime_kind") == "theorem"
            and row.get("uses_sorry") == "False"
            and row.get("reason") == "no_declaration_or_module_main_docstring"
            for row in exclusions
        ),
        "metadata-quality exclusion boundary drifted",
    )
    rows = document.get("records")
    require(
        isinstance(rows, list) and len(rows) == 2_566 and all(isinstance(row, dict) for row in rows),
        "source rows drifted",
    )
    seen_ids: set[str] = set()
    seen_names: set[str] = set()
    file_hashes: dict[Path, str] = {}
    mathlib_root = REPO / "Formalizations/Lean/.lake/packages/mathlib"
    for rank, row in enumerate(rows, 1):
        source_id = row.get("source_record_id")
        declaration = row.get("declaration")
        formal_type = row.get("formal_type")
        require(isinstance(source_id, str) and source_id not in seen_ids, f"source id invalid at rank {rank}")
        seen_ids.add(source_id)
        require(row.get("selection_rank") == rank, "source ranks are not dense")
        require(isinstance(declaration, str) and bool(declaration), "source declaration missing")
        expected_id = "ML4-" + sha(f"{SOURCE_COMMIT}\0{declaration}".encode("utf-8"))[:20].upper()
        require(source_id == expected_id, f"source ID formula drifted at rank {rank}")
        normalized_declaration = normalize_name(declaration)
        require(normalized_declaration not in seen_names, "source declaration name duplicated")
        seen_names.add(normalized_declaration)
        syntax = row.get("source_syntax_kind")
        require(
            syntax in {"theorem", "lemma"}
            and row.get("declaration_kind") == syntax
            and row.get("raw_category") == syntax,
            "source syntax boundary drifted",
        )
        require(isinstance(formal_type, str) and row.get("formal_type_sha256") == sha(formal_type.encode("utf-8")), "formal type hash drifted")
        require(
            row.get("formal_proof_state") == "kernel_checked_sorry_free"
            and row.get("raw_status") == "lean_checked_thmInfo_sorry_free",
            "formal truth status drifted",
        )
        proof = row.get("proof_evidence")
        require(isinstance(proof, dict), "proof evidence missing")
        require(
            proof.get("uses_sorry") is False
            and proof.get("verification") == "lean_checked_environment_thmInfo_and_collectAxioms_without_sorryAx"
            and isinstance(proof.get("batch_axiom_dependency_union"), list)
            and "sorryAx" not in proof["batch_axiom_dependency_union"],
            "source proof gate failed",
        )
        status = row.get("material_status")
        require(
            isinstance(status, dict)
            and status.get("status") == "proved_formal"
            and status.get("as_of_commit") == SOURCE_COMMIT,
            "source material status drifted",
        )
        rights = row.get("rights")
        require(isinstance(rights, dict) and rights.get("source_license") == "Apache-2.0", "source rights drifted")
        signal_kinds(row)
        module_root(row)
        source = row["source"]
        for relative, expected in (
            (source.get("path"), source.get("source_sha256")),
            (proof.get("olean_path"), proof.get("olean_sha256")),
            (proof.get("ilean_path"), proof.get("ilean_sha256")),
        ):
            require(isinstance(relative, str) and isinstance(expected, str), "source/object binding missing")
            path = mathlib_root / relative
            if path not in file_hashes:
                require(path.is_file(), f"bound mathlib file missing: {path}")
                file_hashes[path] = sha_file(path)
            require(file_hashes[path] == expected, f"bound mathlib file hash drifted: {path}")
    return rows


def exact_identity(row: Mapping[str, Any]) -> tuple[str | None, str | None, str | None]:
    formal = row.get("formal_statement")
    formal = formal if isinstance(formal, dict) else {}
    digest = formal.get("formal_type_sha256") or formal.get("declaration_type_sha256") or row.get("formal_type_sha256")
    text = formal.get("formal_type") or formal.get("declaration_type") or row.get("formal_type")
    name = formal.get("declaration") or formal.get("qualified_declaration") or formal.get("declaration_name") or row.get("qualified_name")
    return (
        digest if isinstance(digest, str) and SHA_RE.fullmatch(digest) else None,
        type_sha(text) if isinstance(text, str) and text else None,
        name_sha(name) if isinstance(name, str) and name else None,
    )


def identity_sets(rows: Sequence[Mapping[str, Any]]) -> tuple[set[str], set[str], set[str]]:
    exact: set[str] = set()
    types: set[str] = set()
    names: set[str] = set()
    for row in rows:
        e, t, n = exact_identity(row)
        if e:
            exact.add(e)
        if t:
            types.add(t)
        if n:
            names.add(n)
    return exact, types, names


def winner_key(row: Mapping[str, Any]) -> tuple[int, int, str]:
    return (
        0 if "mathlib_1000_theorems" in signal_kinds(row) else 1,
        int(row["selection_rank"]),
        str(row["source_record_id"]),
    )


def canonicalize(rows: Sequence[Mapping[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    groups: dict[str, list[Mapping[str, Any]]] = defaultdict(list)
    for row in rows:
        groups[type_sha(str(row["formal_type"]))].append(row)
    winners: list[dict[str, Any]] = []
    losers: list[dict[str, Any]] = []
    for component in groups.values():
        ordered = sorted(component, key=winner_key)
        winners.append(dict(ordered[0]))
        losers.extend(dict(row) for row in ordered[1:])
    winners.sort(key=lambda row: int(row["selection_rank"]))
    losers.sort(key=lambda row: int(row["selection_rank"]))
    return winners, losers


def parent_alias_indexes(rows: Sequence[Mapping[str, Any]]) -> tuple[set[str], set[str], set[str]]:
    labels: set[str] = set()
    docstrings: set[str] = set()
    named: set[str] = set()
    for row in rows:
        formal = row.get("formal_statement")
        formal = formal if isinstance(formal, dict) else {}
        label_values: list[Any] = [
            row.get("display_name"), row.get("qualified_name"), formal.get("declaration"),
            formal.get("qualified_declaration"), formal.get("declaration_name"),
        ]
        if isinstance(row.get("aliases"), list):
            label_values.extend(row["aliases"])
        statement = row.get("statement")
        statement = statement if isinstance(statement, dict) else {}
        doc_values = [
            row.get("formal_docstring"), formal.get("formal_docstring"), formal.get("docstring"),
            statement.get("natural_language"),
        ]
        labels.update(normalize_text(value) for value in label_values if isinstance(value, str) and value.strip())
        docstrings.update(normalize_text(value) for value in doc_values if isinstance(value, str) and value.strip())
        named.update(embedded_labels([*label_values, *doc_values]))
    return labels, docstrings, named


def semantic_ready_ids(
    candidates: Sequence[Mapping[str, Any]],
    current: Sequence[Mapping[str, Any]],
    parent_rows: Sequence[Mapping[str, Any]],
) -> tuple[set[str], set[str], dict[str, int]]:
    candidate_ids = {str(row["source_record_id"]) for row in candidates}
    universe = [*current, *candidates]
    indexes: dict[str, dict[str, set[str]]] = {
        feature: defaultdict(set)
        for feature in ("leaf", "display", "decldoc", "main", "wikidata", "named")
    }
    for row in universe:
        source_id = str(row["source_record_id"])
        for feature, values in source_features(row).items():
            for value in values:
                indexes[feature][value].add(source_id)
    parent_labels, parent_docs, parent_named = parent_alias_indexes(parent_rows)
    blocked: set[str] = set()
    feature_rows: Counter[str] = Counter()
    for row in candidates:
        source_id = str(row["source_record_id"])
        observed: set[str] = set()
        features = source_features(row)
        for feature, values in features.items():
            if any(indexes[feature][value] - {source_id} for value in values):
                observed.add(feature)
        direct_labels = {normalize_text(str(row["declaration"])), normalize_text(str(row["display_label"]))}
        if direct_labels & parent_labels:
            observed.add("explicit_parent_label")
        docstring = row.get("declaration_docstring")
        if isinstance(docstring, str) and docstring.strip() and normalize_text(docstring) in parent_docs:
            observed.add("explicit_parent_docstring")
        if features["named"] & parent_named:
            observed.add("embedded_named_label_with_parent")
        if observed:
            blocked.add(source_id)
            feature_rows.update(observed)
    return candidate_ids - blocked, blocked, dict(sorted(feature_rows.items()))


def validate_parent() -> tuple[
    list[dict[str, Any]], list[dict[str, Any]], bytes, bytes, bytes, str
]:
    theorem, theorem_payload = load_json(THEOREM, THEOREM_SHA)
    catalog, catalog_payload = load_json(CATALOG, CATALOG_SHA)
    manifest, manifest_payload = load_json(MANIFEST, MANIFEST_SHA)
    for document, label in ((theorem, "theorem list"), (catalog, "claim catalog"), (manifest, "manifest")):
        require(document.get("authority_sha256") == hash_without(document, "authority_sha256"), f"{label} authority seal stale")
    theorem_rows = theorem.get("records")
    catalog_rows = catalog.get("records")
    require(isinstance(theorem_rows, list) and len(theorem_rows) == 2_500, "parent theorem count drifted")
    require(isinstance(catalog_rows, list) and len(catalog_rows) == 4_525, "parent catalog count drifted")
    require(manifest.get("release") == "5.5" and manifest.get("release_root_sha256") == "fea893e7b5d0b3b958c64ac672f9164efd06996e086c08385462527dcb75dbb0", "parent manifest boundary drifted")
    artifact = next((row for row in manifest.get("artifacts", []) if row.get("path") == "Theorem_List.json"), None)
    require(
        isinstance(artifact, dict)
        and artifact.get("sha256") == THEOREM_SHA
        and artifact.get("size_bytes") == len(theorem_payload)
        and artifact.get("row_count") == 2_500,
        "manifest theorem binding drifted",
    )
    require(sha_file(PARENT_CHECKER) == PARENT_CHECKER_SHA, "parent independent checker drifted")
    completed = subprocess.run(
        [sys.executable, str(PARENT_CHECKER)], cwd=REPO, text=True,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
    )
    require(completed.returncode == 0, "parent 5.5 independent checker failed:\n" + completed.stdout + completed.stderr)
    return theorem_rows, catalog_rows, theorem_payload, catalog_payload, manifest_payload, completed.stdout.strip()


def git_text(root: Path, *args: str) -> str:
    completed = subprocess.run(
        ["git", "-C", str(root), *args], text=True,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
    )
    require(completed.returncode == 0, f"git {' '.join(args)} failed at {root}")
    return completed.stdout.strip()


def verify_live_replay(thousand_plus_root: Path) -> str:
    root = thousand_plus_root.resolve()
    require(root.is_dir(), "1000+ live-replay checkout missing")
    require(git_text(root, "rev-parse", "HEAD") == THOUSAND_PLUS_COMMIT, "1000+ checkout commit drifted")
    require(not git_text(root, "status", "--porcelain"), "1000+ checkout is dirty")
    require(sha_file(EXTRACTOR) == EXTRACTOR_SHA, "mathlib extractor drifted")
    completed = subprocess.run(
        [
            sys.executable, str(EXTRACTOR), "--output", str(FULL),
            "--thousand-plus-root", str(root), "--baseline-count", "1000",
            "--dynamic-count", "1566", "--jobs", "4", "--check",
        ],
        cwd=REPO, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
    )
    require(completed.returncode == 0, "live Lean source replay failed:\n" + completed.stdout + completed.stderr)
    return completed.stdout.strip()


def binding(path: Path, payload: bytes | None = None) -> dict[str, Any]:
    data = path.read_bytes() if payload is None else payload
    return {
        "path": path.relative_to(REPO).as_posix(),
        "sha256": sha(data),
        "size_bytes": len(data),
    }


def expected_accepted_row(
    source: Mapping[str, Any], qualified: Mapping[str, Any], acceptance_rank: int
) -> dict[str, Any]:
    row: dict[str, Any] = {
        "schema_version": "awesome-theorems/mathlib-generator-accepted-candidate/5.6",
        "acceptance_rank": acceptance_rank,
        "qualified_candidate_index": qualified["candidate_index"],
        "candidate_key": qualified["candidate_key"],
        "qualified_candidate_row_sha256": qualified["row_sha256"],
        "source_binding": qualified["source_binding"],
        "declaration": source["declaration"],
        "source_syntax_kind": source["source_syntax_kind"],
        "theorem_record_kind": "theorem",
        "formal_proof_state": source["formal_proof_state"],
        "formal_type_sha256": source["formal_type_sha256"],
        "normalized_formal_type_sha256": type_sha(str(source["formal_type"])),
        "normalized_declaration_name_sha256": name_sha(str(source["declaration"])),
        "module": source["source"]["module"],
        "module_root": module_root(source),
        "runtime_truth_status": "kernel_checked_thmInfo_sorry_free_at_pinned_commit",
        "documentation_status": (
            "individual_declaration_docstring"
            if source.get("declaration_docstring") is not None
            else "module_main_result_description"
        ),
        "credit_policy_status": "v5.6_theorem_record_regardless_of_theorem_or_lemma_source_keyword",
        "formal_identity_status": "unique_against_existing_2500_and_qualified_batch",
        "semantic_canonical_status": "no_exact_alias_or_family_signal_found",
        "semantic_alias_evidence_sha256": sha(canonical([])),
        "qualification_status": "independently_checkable_for_future_release_transaction",
        "generator_disposition": "accepted_set_pending_release_transaction",
        "qualification_receipt_path": RECEIPT.relative_to(REPO).as_posix(),
        "target_variant_id": None,
        "target_stage_claim_id": None,
        "candidate_only": True,
        "release_credit_pending_transaction": True,
        "grants_catalog_entry": False,
        "grants_theorem_credit": False,
        "row_sha256": None,
    }
    row["row_sha256"] = hash_without(row, "row_sha256")
    return row


def build_receipt(
    *,
    counts: Mapping[str, Any],
    feature_rows: Mapping[str, int],
    inputs: Mapping[str, tuple[Path, bytes]],
    accepted_rows: Sequence[Mapping[str, Any]],
    accepted_payload: bytes,
    qualified_payload: bytes,
    parent_checker_stdout: str,
) -> dict[str, Any]:
    receipt: dict[str, Any] = {
        "schema_version": SCHEMA,
        "artifact": RECEIPT.name,
        "as_of": "2026-08-10",
        "decision": "qualified_candidate_set_accepted_for_future_release_transaction",
        "candidate_only": True,
        "release_mutation_authorized_or_performed": False,
        "counts": dict(counts),
        "semantic_screen_rows_by_signal": dict(feature_rows),
        "inputs": {
            key: binding(path, payload) for key, (path, payload) in sorted(inputs.items())
        },
        "tools": {
            "independent_acceptance_checker": binding(Path(__file__).resolve()),
            "parent_release_checker": binding(PARENT_CHECKER),
            "mathlib_live_extractor": binding(EXTRACTOR),
            "qualified_batch_builder": binding(QUALIFIED_BUILDER),
            "accepted_set_builder": binding(ACCEPTED_BUILDER),
        },
        "parent_validation": {
            "checker_status": "pass",
            "checker_stdout_sha256": sha(parent_checker_stdout.encode("utf-8")),
            "release": "5.5",
            "release_root_sha256": "fea893e7b5d0b3b958c64ac672f9164efd06996e086c08385462527dcb75dbb0",
        },
        "live_truth_replay": {
            "status": "pass",
            "mathlib_commit": SOURCE_COMMIT,
            "thousand_plus_commit": THOUSAND_PLUS_COMMIT,
            "full_source_sha256": FULL_SHA,
            "mode": "pinned extractor --check; thmInfo and batch collectAxioms union excludes sorryAx",
            "batch_union_not_direct_dependency_graph": True,
        },
        "output": {
            "path": ACCEPTED.relative_to(REPO).as_posix(),
            "sha256": sha(accepted_payload),
            "size_bytes": len(accepted_payload),
            "rows": len(accepted_rows),
            "row_sha256_set_sha256": set_digest(str(row["row_sha256"]) for row in accepted_rows),
            "source_record_id_set_sha256": set_digest(str(row["source_binding"]["source_record_id"]) for row in accepted_rows),
            "formal_type_sha256_set_sha256": set_digest(str(row["formal_type_sha256"]) for row in accepted_rows),
        },
        "qualification_boundary": {
            "all_1561_rows_mechanically_adjudicated": True,
            "independently_machine_qualified_rows": 1_092,
            "semantic_review_pending_rows": 469,
            "canonical_candidate_rejections": 0,
            "precanonical_exact_duplicate_rejections": 5,
            "human_semantic_review_claimed": False,
            "formal_identity_not_named_theorem_concept": (
                "Counts are unique pinned formal proposition identities. They are not a claim that every row "
                "is a distinct human-level named theorem; the parent itself contains multiple formal variants "
                "of some named theorems."
            ),
        },
        "credit_boundary": {
            "catalog_entries_granted": 0,
            "theorem_credits_granted": 0,
            "ids_allocated": 0,
            "release_credit_authority": (
                "Only a later append-only release transaction with parent-prefix conservation, ID allocation, "
                "release generation, independent release checking, and acceptance can grant credit."
            ),
        },
        "putnam_boundary": {
            "closure_nodes_admitted_by_this_receipt": 0,
            "direct_constant_ledger_available": False,
            "named_label_relation_can_only_release_one_quarantined_row_after_row_specific_review": True,
            "topic_tag_import_or_direction_inference_forbidden": True,
            "isabelle_or_coq_constant_names_not_joinable_to_mathlib": True,
        },
        "qualified_candidate_ledger_sha256": sha(qualified_payload),
        "authority_sha256": None,
    }
    receipt["authority_sha256"] = hash_without(receipt, "authority_sha256")
    return receipt


def atomic_write(path: Path, payload: bytes) -> None:
    with tempfile.NamedTemporaryFile(
        mode="wb", prefix=path.name + ".", suffix=".tmp", dir=path.parent, delete=False
    ) as stream:
        temporary = Path(stream.name)
        stream.write(payload)
        stream.flush()
        os.fsync(stream.fileno())
    os.replace(temporary, path)


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-receipt", action="store_true", help="write the qualification receipt")
    parser.add_argument("--live-replay", action="store_true", help="rerun the Lean extractor")
    parser.add_argument("--thousand-plus-root", type=Path, help="clean pinned 1000+ checkout")
    args = parser.parse_args(argv)
    if args.write_receipt and not args.live_replay:
        parser.error("--write-receipt requires --live-replay")
    if args.live_replay and args.thousand_plus_root is None:
        parser.error("--live-replay requires --thousand-plus-root")
    if args.thousand_plus_root is not None and not args.live_replay:
        parser.error("--thousand-plus-root is only valid with --live-replay")
    return args


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    try:
        full, full_payload = load_json(FULL, FULL_SHA)
        source_rows = validate_source_rows(full)
        theorem_rows, catalog_rows, theorem_payload, catalog_payload, manifest_payload, parent_stdout = validate_parent()
        qualified_inventory, qualified_inventory_payload = load_json(QUALIFIED_INVENTORY, QUALIFIED_INVENTORY_SHA)
        require(
            qualified_inventory.get("authority_sha256") == hash_without(qualified_inventory, "authority_sha256"),
            "qualified inventory authority seal stale",
        )
        qualified_rows, qualified_payload = load_jsonl(QUALIFIED, QUALIFIED_SHA)
        accepted_rows, accepted_payload = load_jsonl(ACCEPTED, ACCEPTED_SHA)
        require(len(qualified_rows) == 1_561 and len(accepted_rows) == 1_092, "candidate/accepted row counts drifted")

        canonical_rows, losers = canonicalize(source_rows)
        require(len(canonical_rows) == 2_561, "canonical formal identity count drifted")
        require([row["selection_rank"] for row in losers] == EXPECTED_LOSER_RANKS, "exact duplicate loser set drifted")
        require(all(type_sha(str(row["formal_type"])) in {type_sha(str(other["formal_type"])) for other in canonical_rows} for row in losers), "duplicate loser lacks canonical winner")

        source_by_id = {str(row["source_record_id"]): row for row in canonical_rows}
        current_ids: set[str] = set()
        current_variants: dict[str, str] = {}
        for row in theorem_rows:
            if row.get("source_id") != "SRC-MATH-V5-MATHLIB-8A178386":
                continue
            provenance = row.get("provenance")
            require(isinstance(provenance, dict), "parent mathlib provenance missing")
            source_id = provenance.get("source_record_id")
            require(isinstance(source_id, str) and source_id not in current_ids, "parent mathlib source id invalid")
            current_ids.add(source_id)
            current_variants[source_id] = str(row["variant_id"])
        require(len(current_ids) == 1_000 and current_ids <= set(source_by_id), "parent mathlib identity set drifted")
        candidates = [row for row in canonical_rows if row["source_record_id"] not in current_ids]
        current = [source_by_id[source_id] for source_id in sorted(current_ids)]
        require(len(candidates) == 1_561, "unadmitted canonical candidate count drifted")

        theorem_exact, theorem_types, theorem_names = identity_sets(theorem_rows)
        catalog_exact, catalog_types, catalog_names = identity_sets(catalog_rows)
        for row in candidates:
            exact = str(row["formal_type_sha256"])
            normalized = type_sha(str(row["formal_type"]))
            name = name_sha(str(row["declaration"]))
            require(
                exact not in theorem_exact and normalized not in theorem_types and name not in theorem_names,
                f"candidate conflicts with parent theorem surface: {row['declaration']}",
            )
            require(
                exact not in catalog_exact and normalized not in catalog_types and name not in catalog_names,
                f"candidate conflicts with complete parent claim surface: {row['declaration']}",
            )

        ready_ids, quarantine_ids, feature_rows = semantic_ready_ids(candidates, current, theorem_rows)
        require(len(ready_ids) == 1_092 and len(quarantine_ids) == 469, "semantic screen partition drifted")
        require(ready_ids.isdisjoint(quarantine_ids), "semantic screen overlaps lanes")

        qualified_by_id: dict[str, dict[str, Any]] = {}
        for index, row in enumerate(qualified_rows, 1):
            require(row.get("candidate_index") == index, "qualified candidate indexes are not dense")
            binding_value = row.get("source_binding")
            require(isinstance(binding_value, dict), "qualified source binding missing")
            source_id = binding_value.get("source_record_id")
            require(isinstance(source_id, str) and source_id not in qualified_by_id, "qualified source id invalid")
            source = source_by_id.get(source_id)
            require(source is not None and source_id not in current_ids, "qualified row is not an unadmitted canonical source")
            require(binding_value.get("source_record_sha256") == sha(canonical(source)), "qualified source binding stale")
            require(row.get("theorem_record_kind") == "theorem", "qualified lemma was not promoted to theorem record")
            expected_ready = source_id in ready_ids
            require(row.get("generator_admission_qualified") is expected_ready, "qualified semantic disposition disagrees with independent screen")
            require(
                row.get("generator_lane")
                == ("provisional_generator_admission" if expected_ready else "semantic_variant_review_quarantine"),
                "qualified generator lane disagrees with independent screen",
            )
            require(row.get("candidate_only") is True and row.get("grants_theorem_credit") is False, "qualified row grants premature credit")
            qualified_by_id[source_id] = row
        require(set(qualified_by_id) == {str(row["source_record_id"]) for row in candidates}, "qualified ledger coverage drifted")

        expected_ready_order = [str(row["source_record_id"]) for row in candidates if row["source_record_id"] in ready_ids]
        require(len(expected_ready_order) == 1_092, "accepted order denominator drifted")
        for acceptance_rank, (source_id, observed) in enumerate(zip(expected_ready_order, accepted_rows, strict=True), 1):
            source = source_by_id[source_id]
            qualified = qualified_by_id[source_id]
            expected = expected_accepted_row(source, qualified, acceptance_rank)
            require(observed == expected, f"accepted row {acceptance_rank} differs from independent reconstruction")
        accepted_ids = {str(row["source_binding"]["source_record_id"]) for row in accepted_rows}
        require(accepted_ids == ready_ids, "accepted set differs from independent ready set")
        require(not accepted_ids & {str(row["source_record_id"]) for row in losers}, "exact duplicate loser entered accepted set")

        counts = {
            **EXPECTED_COUNTS,
        }
        require(sum(row["source_syntax_kind"] == "theorem" for row in candidates) == 1_072, "candidate theorem syntax count drifted")
        require(sum(row["source_syntax_kind"] == "lemma" for row in candidates) == 489, "candidate lemma syntax count drifted")
        require(sum(source_by_id[source_id]["source_syntax_kind"] == "theorem" for source_id in ready_ids) == 707, "accepted theorem syntax count drifted")
        require(sum(source_by_id[source_id]["source_syntax_kind"] == "lemma" for source_id in ready_ids) == 385, "accepted lemma syntax count drifted")
        require(sum(source_by_id[source_id]["source_syntax_kind"] == "theorem" for source_id in quarantine_ids) == 365, "quarantine theorem syntax count drifted")
        require(sum(source_by_id[source_id]["source_syntax_kind"] == "lemma" for source_id in quarantine_ids) == 104, "quarantine lemma syntax count drifted")

        live_stdout = verify_live_replay(args.thousand_plus_root) if args.live_replay else None
        receipt_inputs = {
            "full_mathlib_source": (FULL, full_payload),
            "parent_5_5_theorem_list": (THEOREM, theorem_payload),
            "parent_5_5_claim_catalog": (CATALOG, catalog_payload),
            "parent_5_5_manifest": (MANIFEST, manifest_payload),
            "qualified_candidate_ledger": (QUALIFIED, qualified_payload),
            "qualified_batch_inventory": (QUALIFIED_INVENTORY, qualified_inventory_payload),
            "generator_accepted_set": (ACCEPTED, accepted_payload),
        }
        receipt = build_receipt(
            counts=counts,
            feature_rows=feature_rows,
            inputs=receipt_inputs,
            accepted_rows=accepted_rows,
            accepted_payload=accepted_payload,
            qualified_payload=qualified_payload,
            parent_checker_stdout=parent_stdout,
        )
        receipt_payload = pretty(receipt)
        if args.write_receipt:
            require(live_stdout is not None, "receipt write lacks live replay")
            atomic_write(RECEIPT, receipt_payload)
            action = "wrote"
        else:
            observed_receipt = RECEIPT.read_bytes()
            require(observed_receipt == receipt_payload, f"acceptance receipt drifted: {sha(observed_receipt)} != {sha(receipt_payload)}")
            action = "checked"
        print(
            f"PASS {action} independent mathlib generator acceptance v5.6 "
            f"accepted=1092 quarantine=469 rejected=0 duplicate_losers=5 "
            f"receipt_authority={receipt['authority_sha256']}"
        )
        if live_stdout is not None:
            print("PASS live Lean replay: " + live_stdout)
        return 0
    except (CheckError, OSError) as error:
        print(f"FAIL independent mathlib generator acceptance v5.6: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
