#!/usr/bin/env python3
"""Independent verifier for the Stage5 mathematics catalog release 5.3.

No production extractor, curation writer, or release generator is imported.
The checker authenticates the fixed mathlib source JSON, independently derives
the literal-theorem pool and exact-formal-type winners, replays the two-phase
500-row selection, and then reconstructs the append-only release package.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import copy
import hashlib
import json
from pathlib import Path
import re
import sys
from typing import Any, Iterable, Mapping, Sequence
import unicodedata

try:
    import jsonschema
except ImportError:  # pragma: no cover
    jsonschema = None


RELEASE = "5.3"
PARENT_RELEASE = "5.2"
REVIEW_DATE = "2026-08-10"
SOURCE_ID = "SRC-MATH-V5-MATHLIB-8A178386"
CATALOG_ROOT = Path("Docs/catalog/v5")
CONTRACT_PATH = CATALOG_ROOT / "Stage5_Math_Expansion_Contract_v5_3.json"
SCHEMA_PATH = CATALOG_ROOT / "Math_Claim_Record_Schema_v5_3.json"
SOURCE_REGISTRY_PATH = CATALOG_ROOT / "Math_Source_Registry_v5_3.json"
PARENT_RECEIPT_PATH = CATALOG_ROOT / "V5_2_Parent_Receipt_v5_3.json"
CURATION_PATH = CATALOG_ROOT / "curation/Mathlib_Theorem_Curation_v5_3.json"
SOURCE_PATH = CATALOG_ROOT / "sources/mathlib-theorems-8a178386.json"
PARENT_DIR = CATALOG_ROOT / "releases/5.2"
RELEASE_DIR = CATALOG_ROOT / "releases/5.3"
CURRENT_PATH = CATALOG_ROOT / "Current_Release.json"

RELEASE_FILES = (
    "Claim_Catalog.json",
    "Claim_ID_Registry.json",
    "Stage5_Claim_ID_Registry.json",
    "Migration_v4_to_v5.json",
    "Theorem_List.json",
    "Open_Claim_List.json",
    "Coverage_Ledger.json",
    "Strict_Conjecture_Ledger.json",
)
MANIFEST_NAME = "Release_Manifest.json"

SOURCE_FILE_SHA256 = "236b9f6ac192eaf87215663bfd7fadb80c439b452049cef1747ea804c458637a"
SOURCE_FILE_SIZE = 6_316_287
SOURCE_CONTENT_DIGEST = "dd49c8322d8eded995c84a235fd458fc093a187230323f87bea78049ae90e53b"
MATHLIB_COMMIT = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_LICENSE_SHA256 = "b40930bbcf80744c86c46a12bc9da056641d722716c378f5659b9e555ef833e1"
SOURCE_ROWS = 1_500
LITERAL_THEOREMS = 1_235
LITERAL_LEMMAS = 265
UNIQUE_FORMAL_TYPES = 1_231
DUPLICATE_GROUPS = 3
DUPLICATE_LOSERS = 4
PHASE_ONE_ROWS = 180
PHASE_TWO_ROWS = 320
NEW_ROWS = 500
PARENT_CATALOG_ROWS = 3_100
PARENT_ATV_HIGH_WATERMARK = 6_584
PARENT_ATF_HIGH_WATERMARK = 6_354
LAST_ATV_ORDINAL = 7_084
LAST_ATF_ORDINAL = 6_854
PARENT_ROOT = "edee3a3e5f29a345a16fb526654aecfeaeaaf62da0e0101ed5e9bd2cbb374e2e"
SOURCE_REGISTRY_FILE_SHA256 = "30f92aff96c104450a113a1ce56c3e0c0866d9a9e6dea3730e980dcf96c8baca"
SOURCE_REGISTRY_AUTHORITY = "4a374b3c6bb509802c1e0b13e8dd340b646b2f88706c09fa95ebb0f0eac5f310"
PARENT_RECEIPT_FILE_SHA256 = "95de05869d43a267ac7174c5f377e5e4ed003e36b95b71b213bcc72fbf2ad374"
PARENT_RECEIPT_AUTHORITY = "c52dec430bcf120e5b25b5f8d35f0a2206e83fe6815f7891f8946147ce8ad98a"
CURATION_FILE_SHA256 = "379e165ae52ffd911e383fdb351fc602d36ec585e40bade54612c1512a7a1905"
CURATION_AUTHORITY = "9661eebbd25bbb8aee3a0c7ae1c9cbe671ec77324f889d25e967811ffd9f7d5d"
CONTRACT_FILE_SHA256 = "a600128e9036eec4a8af44741cc79ef52ad465402813401544ca405c6d9b76a6"
CONTRACT_AUTHORITY = "2de7e9b81f3299670f6b9e77afc7df0b5dc4c544fa32d342c6211e0520172da8"
SCHEMA_FILE_SHA256 = "58054bfdad90b7fa6391cf495285b8281e8346e4f80d9b3a53ade6ee36dc81a3"
SCHEMA_AUTHORITY = "160de5babf18c2b299f2a04a097f6d4c78de6ff39211dd54d471598922dd6d0a"

DOCS_SIGNAL = "mathlib_1000_theorems"
MODULE_SIGNAL = "mathlib_module_main_result"
ALLOWED_SIGNALS = {DOCS_SIGNAL, MODULE_SIGNAL}
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
SOURCE_RECORD_ID_RE = re.compile(r"^ML4-[0-9A-F]{20}$")
ATV_RE = re.compile(r"^ATV-([0-9]{8})$")

SOURCE_TOP_FIELDS = {
    "schema_version",
    "generator",
    "source_snapshot",
    "optional_thousand_plus_snapshot",
    "selection_policy",
    "counts",
    "runtime_rejections",
    "records",
    "content_digest_before_self_field",
}
SOURCE_ROW_FIELDS = {
    "source_record_id",
    "selection_rank",
    "selection_cohort",
    "declaration",
    "display_label",
    "exact_curated_summary",
    "declaration_kind",
    "source_syntax_kind",
    "formal_type",
    "formal_type_sha256",
    "declaration_docstring",
    "formal_docstring",
    "formal_docstring_origin",
    "formal_docstring_sha256",
    "formal_proof_state",
    "raw_category",
    "raw_status",
    "material_status",
    "msc2020",
    "proof_evidence",
    "source",
    "importance_signals",
    "rights",
}
CURATION_ROW_FIELDS = {
    "candidate_key",
    "source_index",
    "source_record_id",
    "source_record_sha256",
    "declaration",
    "declaration_kind",
    "source_syntax_kind",
    "selection_rank",
    "selection_cohort",
    "formal_proof_state",
    "formal_type_sha256",
    "formal_docstring_sha256",
    "proof_evidence_payload_sha256",
    "importance_payload_sha256",
    "rights_payload_sha256",
    "semantic_key",
    "semantic_key_method",
    "semantic_key_payload_sha256",
    "disposition",
    "reason_code",
    "accepted_rank",
    "target_variant_id",
    "target_s5_id",
    "canonical_source_record_id",
    "duplicate_of_semantic_key",
    "duplicate_of_variant_id",
    "dedupe_rationale",
    "dedupe_confidence",
    "dedupe_reviewer",
    "grants_catalog_entry",
    "grants_theorem_credit",
    "row_sha256",
}


class CheckFailure(RuntimeError):
    """An input or release invariant failed closed."""


class Checker:
    def __init__(self, root: Path) -> None:
        self.root = root.resolve()
        self.errors: list[str] = []
        self.notes: list[str] = []

    def path(self, relative: str | Path) -> Path:
        value = Path(relative)
        if value.is_absolute() or ".." in value.parts:
            raise CheckFailure(f"unsafe repository path: {relative!r}")
        return self.root / value

    def load_json(self, relative: str | Path) -> tuple[dict[str, Any], bytes]:
        path = self.path(relative)
        try:
            payload = path.read_bytes()
        except OSError as error:
            raise CheckFailure(f"cannot read {relative}: {error}") from error
        return strict_json_object(payload, str(relative)), payload

    def fail(self, message: str) -> None:
        self.errors.append(message)

    def note(self, message: str) -> None:
        self.notes.append(message)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise CheckFailure(message)


def reject_constant(value: str) -> None:
    raise CheckFailure(f"non-finite JSON number is forbidden: {value}")


def object_without_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        require(key not in result, f"duplicate JSON object key: {key!r}")
        result[key] = value
    return result


def strict_json_object(payload: bytes, label: str) -> dict[str, Any]:
    try:
        value = json.loads(
            payload.decode("utf-8"),
            object_pairs_hook=object_without_duplicate_keys,
            parse_constant=reject_constant,
        )
    except (UnicodeError, json.JSONDecodeError) as error:
        raise CheckFailure(f"invalid JSON in {label}: {error}") from error
    require(isinstance(value, dict), f"{label} must contain one JSON object")
    return value


def canonical_json_bytes(value: Any) -> bytes:
    try:
        return json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        ).encode("utf-8")
    except (TypeError, ValueError) as error:
        raise CheckFailure(f"value is not canonical JSON: {error}") from error


def pretty_source_json_bytes(value: Any) -> bytes:
    return (
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True, allow_nan=False)
        + "\n"
    ).encode("utf-8")


def encoded_document(value: Mapping[str, Any]) -> bytes:
    return canonical_json_bytes(value) + b"\n"


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    try:
        with path.open("rb") as stream:
            for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                digest.update(chunk)
    except OSError as error:
        raise CheckFailure(f"cannot hash {path}: {error}") from error
    return digest.hexdigest()


def hash_without(value: Mapping[str, Any], *fields: str) -> str:
    omitted = set(fields)
    return sha256_bytes(
        canonical_json_bytes({key: item for key, item in value.items() if key not in omitted})
    )


def seal(value: Mapping[str, Any]) -> dict[str, Any]:
    result = dict(value)
    result.pop("authority_sha256", None)
    result["authority_sha256"] = hash_without(result, "authority_sha256")
    return result


def seal_field(value: Mapping[str, Any], field: str, *also_omit: str) -> dict[str, Any]:
    result = dict(value)
    result.pop(field, None)
    result[field] = hash_without(result, field, *also_omit)
    return result


def verify_seal(value: Mapping[str, Any], label: str) -> str:
    observed = value.get("authority_sha256")
    require(isinstance(observed, str) and SHA256_RE.fullmatch(observed) is not None, f"{label} has no valid authority_sha256")
    require(observed == hash_without(value, "authority_sha256"), f"{label} authority seal drifted")
    return observed


def set_digest(values: Iterable[str]) -> str:
    return sha256_bytes(canonical_json_bytes(sorted(values)))


def ordinal(identifier: str) -> int:
    match = ATV_RE.fullmatch(identifier)
    require(match is not None, f"invalid ATV identifier: {identifier!r}")
    return int(match.group(1))


def normalize_declaration_name(value: str) -> str:
    return unicodedata.normalize("NFKC", value).casefold().strip()


def declaration_name_key_sha256(value: str) -> str:
    return sha256_bytes(normalize_declaration_name(value).encode("utf-8"))


def normalized_formal_type(value: str) -> str:
    return " ".join(value.split())


def normalized_formal_type_sha256(value: str) -> str:
    return sha256_bytes(normalized_formal_type(value).encode("utf-8"))


def source_record_sha256(row: Mapping[str, Any]) -> str:
    return sha256_bytes(canonical_json_bytes(row))


def importance_signal_kinds(row: Mapping[str, Any]) -> tuple[str, ...]:
    signals = row.get("importance_signals")
    require(isinstance(signals, list) and bool(signals), f"{row.get('source_record_id')} lacks importance signals")
    kinds: set[str] = set()
    for index, signal in enumerate(signals):
        require(isinstance(signal, dict), f"importance signal {index} is not an object")
        kind = signal.get("kind")
        require(isinstance(kind, str) and kind in ALLOWED_SIGNALS, f"unsupported importance signal: {kind!r}")
        if kind == DOCS_SIGNAL:
            require(signal.get("source_path") == "docs/1000.yaml", "docs/1000 signal locator drifted")
            require(signal.get("formalization_status") == "formalized", "docs/1000 signal is not formalized")
        else:
            signal_module = signal.get("module")
            require(isinstance(signal_module, str) and signal_module.startswith("Mathlib."), "module-main signal module drifted")
            expected_signal_path = "/".join(signal_module.split(".")) + ".lean"
            require(signal.get("source_path") == expected_signal_path, "module-main signal path drifted")
        kinds.add(kind)
    return tuple(sorted(kinds))


def has_importance_signal(row: Mapping[str, Any], kind: str) -> bool:
    return kind in importance_signal_kinds(row)


def module_root(row: Mapping[str, Any]) -> str:
    module = str(row["source"]["module"])
    pieces = module.split(".")
    require(len(pieces) >= 2 and pieces[0] == "Mathlib" and bool(pieces[1]), f"invalid Mathlib module: {module!r}")
    return pieces[1]


def verify_source_record(row: Mapping[str, Any], index: int) -> None:
    label = f"mathlib source record {index}"
    require(set(row) == SOURCE_ROW_FIELDS, f"{label} field closure drifted")
    source_id = row.get("source_record_id")
    require(isinstance(source_id, str) and SOURCE_RECORD_ID_RE.fullmatch(source_id) is not None, f"{label} source_record_id is invalid")
    declaration = row.get("declaration")
    require(isinstance(declaration, str) and bool(declaration.strip()), f"{label} declaration is invalid")
    expected_id = "ML4-" + sha256_bytes(f"{MATHLIB_COMMIT}\0{declaration}".encode("utf-8"))[:20].upper()
    require(source_id == expected_id, f"{label} source_record_id does not bind commit/declaration")
    require(row.get("selection_rank") == index, f"{label} selection rank drifted")
    require(row.get("selection_cohort") == ("baseline" if index <= 1_000 else "dynamic_expansion"), f"{label} cohort/rank drifted")
    kind = row.get("declaration_kind")
    require(kind in {"theorem", "lemma"}, f"{label} is not a literal theorem/lemma")
    require(row.get("source_syntax_kind") == kind and row.get("raw_category") == kind, f"{label} literal-kind fields disagree")
    formal_type = row.get("formal_type")
    formal_docstring = row.get("formal_docstring")
    require(isinstance(formal_type, str) and bool(formal_type.strip()), f"{label} formal type is empty")
    require(isinstance(formal_docstring, str) and bool(formal_docstring.strip()), f"{label} formal docstring is empty")
    require(row.get("formal_type_sha256") == sha256_bytes(formal_type.encode("utf-8")), f"{label} formal-type hash drifted")
    require(row.get("formal_docstring_sha256") == sha256_bytes(formal_docstring.encode("utf-8")), f"{label} formal-docstring hash drifted")
    declaration_docstring = row.get("declaration_docstring")
    require(declaration_docstring is None or isinstance(declaration_docstring, str), f"{label} declaration docstring type drifted")
    if declaration_docstring:
        require(row.get("formal_docstring_origin") == "declaration_docstring" and formal_docstring == declaration_docstring, f"{label} declaration docstring binding drifted")
    else:
        require(row.get("formal_docstring_origin") == "module_main_result_docstring", f"{label} module-doc origin drifted")
        require(has_importance_signal(row, MODULE_SIGNAL), f"{label} module-doc fallback lacks module-main signal")
    require(row.get("formal_proof_state") == "kernel_checked_sorry_free", f"{label} is not kernel checked/sorry free")
    require(row.get("raw_status") == "lean_checked_thmInfo_sorry_free", f"{label} raw proof status drifted")
    status = row.get("material_status")
    require(isinstance(status, dict) and status.get("status") == "proved_formal" and status.get("as_of_commit") == MATHLIB_COMMIT, f"{label} material status drifted")
    proof = row.get("proof_evidence")
    require(isinstance(proof, dict), f"{label} proof evidence is not an object")
    require(proof.get("uses_sorry") is False, f"{label} permits sorryAx")
    require(proof.get("verification") == "lean_checked_environment_thmInfo_and_collectAxioms_without_sorryAx", f"{label} proof verification mode drifted")
    axioms = proof.get("batch_axiom_dependency_union")
    require(isinstance(axioms, list) and all(isinstance(item, str) for item in axioms) and "sorryAx" not in axioms, f"{label} axiom evidence includes sorryAx or is malformed")
    source = row.get("source")
    require(isinstance(source, dict), f"{label} source locator is not an object")
    module = source.get("module")
    path = source.get("path")
    require(isinstance(module, str) and isinstance(path, str), f"{label} module/path is invalid")
    require(module == proof.get("compiled_module"), f"{label} compiled module drifted")
    expected_path = "/".join(module.split(".")) + ".lean"
    require(path == expected_path, f"{label} module/source path drifted")
    source_range = source.get("range")
    require(isinstance(source_range, dict), f"{label} source range is malformed")
    start = source_range.get("line_start")
    end = source_range.get("line_end")
    require(isinstance(start, int) and not isinstance(start, bool) and isinstance(end, int) and not isinstance(end, bool) and 1 <= start <= end, f"{label} source line range is invalid")
    expected_url = f"https://github.com/leanprover-community/mathlib4/blob/{MATHLIB_COMMIT}/{path}#L{start}-L{end}"
    require(source.get("url") == expected_url, f"{label} commit-pinned source URL drifted")
    require(isinstance(source.get("source_sha256"), str) and SHA256_RE.fullmatch(source["source_sha256"]) is not None, f"{label} source-file SHA is invalid")
    for suffix in ("ilean", "olean"):
        expected_cache_path = f".lake/build/lib/lean/{'/'.join(module.split('.'))}.{suffix}"
        require(proof.get(f"{suffix}_path") == expected_cache_path, f"{label} {suffix} locator drifted")
        digest = proof.get(f"{suffix}_sha256")
        require(isinstance(digest, str) and SHA256_RE.fullmatch(digest) is not None, f"{label} {suffix} SHA drifted")
    require(row.get("rights") == {
        "source_license": "Apache-2.0",
        "use": "formal_statement_docstring_and_bibliographic_metadata",
        "attribution": "The mathlib Community",
    }, f"{label} rights/attribution drifted")
    importance_signal_kinds(row)
    module_root(row)


def load_mathlib_source(
    checker: Checker,
) -> tuple[dict[str, Any], list[dict[str, Any]], dict[str, int], dict[str, str]]:
    source, payload = checker.load_json(SOURCE_PATH)
    require(len(payload) == SOURCE_FILE_SIZE, "mathlib source byte size drifted")
    require(sha256_bytes(payload) == SOURCE_FILE_SHA256, "mathlib source file SHA-256 drifted")
    require(set(source) == SOURCE_TOP_FIELDS, "mathlib source top-level closure drifted")
    require(source.get("schema_version") == "awesome-theorems/mathlib-theorem-source/1.0", "mathlib source schema drifted")
    body = dict(source)
    declared_digest = body.pop("content_digest_before_self_field", None)
    rebuilt_digest = sha256_bytes(pretty_source_json_bytes(body))
    require(declared_digest == rebuilt_digest == SOURCE_CONTENT_DIGEST, "mathlib source self/content digest drifted")
    snapshot = source.get("source_snapshot")
    require(isinstance(snapshot, dict), "mathlib source snapshot is malformed")
    require(snapshot.get("commit") == MATHLIB_COMMIT, "mathlib commit pin drifted")
    require(snapshot.get("license") == "Apache-2.0" and snapshot.get("license_sha256") == MATHLIB_LICENSE_SHA256, "mathlib license pin drifted")
    require(snapshot.get("module_cache_complete") is True, "mathlib compiled module cache was incomplete")
    require(snapshot.get("available_source_modules") == snapshot.get("available_ilean_modules") == snapshot.get("available_olean_modules") == 7_871, "mathlib module-cache inventory drifted")
    rows = source.get("records")
    require(isinstance(rows, list) and len(rows) == SOURCE_ROWS and all(isinstance(row, dict) for row in rows), "mathlib source must contain 1,500 object rows")
    ids: dict[str, int] = {}
    hashes: dict[str, str] = {}
    normalized_names: set[str] = set()
    kinds: Counter[str] = Counter()
    for index, row in enumerate(rows, start=1):
        verify_source_record(row, index)
        source_id = str(row["source_record_id"])
        require(source_id not in ids, f"mathlib source repeats ID {source_id}")
        ids[source_id] = index
        hashes[source_id] = source_record_sha256(row)
        normalized_name = normalize_declaration_name(str(row["declaration"]))
        require(normalized_name not in normalized_names, f"mathlib source repeats declaration {row['declaration']!r}")
        normalized_names.add(normalized_name)
        kinds[str(row["declaration_kind"])] += 1
    require(kinds == Counter({"theorem": LITERAL_THEOREMS, "lemma": LITERAL_LEMMAS}), "literal theorem/lemma partition is not 1235/265")
    require(set(ids.values()) == set(range(1, SOURCE_ROWS + 1)), "source ranks are not exactly 1..1500")
    counts = source.get("counts")
    require(isinstance(counts, dict), "mathlib source counts is malformed")
    require(counts.get("selected_total") == SOURCE_ROWS and counts.get("selected_baseline") == 1_000 and counts.get("selected_dynamic_expansion") == 500, "mathlib source selection counts drifted")
    require(counts.get("selected_with_docs_1000_signal") == sum(has_importance_signal(row, DOCS_SIGNAL) for row in rows), "mathlib source docs/1000 count drifted")
    require(counts.get("selected_with_module_main_signal") == sum(has_importance_signal(row, MODULE_SIGNAL) for row in rows), "mathlib source module-main count drifted")
    require(counts.get("selected_with_declaration_docstring") == sum(bool(row["declaration_docstring"]) for row in rows), "mathlib source declaration-docstring count drifted")
    roots = Counter(module_root(row) for row in rows)
    require(counts.get("selected_by_module_root") == dict(sorted(roots.items())), "mathlib source module-root counts drifted")
    return source, rows, ids, hashes


def duplicate_winner_rank(row: Mapping[str, Any]) -> tuple[int, int, str]:
    return (
        -int(has_importance_signal(row, DOCS_SIGNAL)),
        int(row["selection_rank"]),
        str(row["source_record_id"]),
    )


def select_mathlib_rows(
    records: Sequence[dict[str, Any]],
) -> tuple[list[dict[str, Any]], dict[str, dict[str, Any]], dict[str, str]]:
    literal = [
        row
        for row in records
        if row["declaration_kind"] == "theorem" and row["source_syntax_kind"] == "theorem"
    ]
    require(len(literal) == LITERAL_THEOREMS, "literal theorem pool is not 1,235")
    by_id = {str(row["source_record_id"]): row for row in literal}
    parents = {source_id: source_id for source_id in by_id}

    def find(source_id: str) -> str:
        while parents[source_id] != source_id:
            parents[source_id] = parents[parents[source_id]]
            source_id = parents[source_id]
        return source_id

    def union(left: str, right: str) -> None:
        left_root = find(left)
        right_root = find(right)
        if left_root != right_root:
            parents[max(left_root, right_root)] = min(left_root, right_root)

    axes: list[dict[str, list[dict[str, Any]]]] = []
    for key in (
        lambda row: str(row["formal_type_sha256"]),
        lambda row: normalized_formal_type_sha256(str(row["formal_type"])),
        lambda row: normalize_declaration_name(str(row["declaration"])),
    ):
        groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for row in literal:
            groups[key(row)].append(row)
        axes.append(groups)
        for group in groups.values():
            first = str(group[0]["source_record_id"])
            for row in group[1:]:
                union(first, str(row["source_record_id"]))

    exact_groups, normalized_groups, name_groups = axes
    require(
        len(exact_groups) == UNIQUE_FORMAL_TYPES,
        "literal theorem formal types are not 1,231-way unique",
    )
    require(
        sum(len(group) > 1 for group in exact_groups.values()) == DUPLICATE_GROUPS
        and sum(len(group) - 1 for group in exact_groups.values())
        == DUPLICATE_LOSERS,
        "exact formal-type duplicate boundary is not three groups/four losers",
    )

    def gate_losers(
        groups: Mapping[str, Sequence[dict[str, Any]]]
    ) -> set[str]:
        result: set[str] = set()
        for group in groups.values():
            ordered = sorted(group, key=duplicate_winner_rank)
            result.update(str(row["source_record_id"]) for row in ordered[1:])
        return result

    exact_losers = gate_losers(exact_groups)
    normalized_losers = gate_losers(normalized_groups)
    name_losers = gate_losers(name_groups)
    require(
        normalized_losers - exact_losers == set()
        and name_losers - exact_losers - normalized_losers == set(),
        "source has an unexpected whitespace-normalized or full-name-only duplicate",
    )

    components: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for source_id, row in by_id.items():
        components[find(source_id)].append(row)
    winner_for_id: dict[str, dict[str, Any]] = {}
    losers: dict[str, str] = {}
    winners: list[dict[str, Any]] = []
    for component in components.values():
        ordered = sorted(component, key=duplicate_winner_rank)
        winner = ordered[0]
        winners.append(winner)
        for row in ordered:
            winner_for_id[str(row["source_record_id"])] = winner
        for row in ordered[1:]:
            losers[str(row["source_record_id"])] = str(winner["source_record_id"])
    require(
        len(winners) == UNIQUE_FORMAL_TYPES and len(losers) == DUPLICATE_LOSERS,
        "three-gate source winner replay drifted",
    )
    phase_one = sorted(
        (row for row in winners if has_importance_signal(row, DOCS_SIGNAL)),
        key=lambda row: (int(row["selection_rank"]), str(row["source_record_id"])),
    )
    require(len(phase_one) == PHASE_ONE_ROWS, "deduplicated docs/1000 phase is not 180")
    phase_one_ids = {str(row["source_record_id"]) for row in phase_one}
    buckets: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in winners:
        if str(row["source_record_id"]) in phase_one_ids:
            continue
        if has_importance_signal(row, MODULE_SIGNAL):
            buckets[module_root(row)].append(row)
    for bucket in buckets.values():
        bucket.sort(key=lambda row: (int(row["selection_rank"]), str(row["source_record_id"])))
    roots = sorted(buckets)
    require(len(roots) == 21, "module-main phase does not have 21 roots")
    offsets = {root: 0 for root in roots}
    phase_two: list[dict[str, Any]] = []
    while len(phase_two) < PHASE_TWO_ROWS:
        advanced = False
        for root in roots:
            offset = offsets[root]
            if offset >= len(buckets[root]):
                continue
            phase_two.append(buckets[root][offset])
            offsets[root] += 1
            advanced = True
            if len(phase_two) == PHASE_TWO_ROWS:
                break
        require(advanced, "module-root balanced phase exhausted before 320")
    selected = phase_one + phase_two
    require(len(selected) == NEW_ROWS, "two-phase selection is not 500")
    require(len({row["source_record_id"] for row in selected}) == NEW_ROWS, "two-phase selection repeats source IDs")
    require(len({row["declaration"] for row in selected}) == NEW_ROWS, "two-phase selection repeats declarations")
    require(len({row["formal_type_sha256"] for row in selected}) == NEW_ROWS, "two-phase selection repeats formal types")
    return selected, winner_for_id, losers


def importance_tier(row: Mapping[str, Any]) -> str:
    kinds = set(importance_signal_kinds(row))
    if kinds == {DOCS_SIGNAL, MODULE_SIGNAL}:
        return "docs_1000_and_module_main"
    if kinds == {DOCS_SIGNAL}:
        return "docs_1000"
    require(kinds == {MODULE_SIGNAL}, "source row has no recognized importance tier")
    return "module_main_result"


def primary_row_count(document: Mapping[str, Any]) -> int:
    candidates = document.get("candidate_dispositions")
    coverage = document.get("msc_coverage")
    if isinstance(candidates, list) and isinstance(coverage, list):
        return len(candidates) + len(coverage)
    strict = document.get("strict_credits")
    corrections = document.get("credit_corrections")
    if isinstance(strict, list) and isinstance(corrections, list):
        return len(strict) + len(corrections)
    for key in ("records", "variants", "mappings", "migrations", "rows"):
        rows = document.get(key)
        if isinstance(rows, list):
            return len(rows)
    return 0


def release_root(inventory: Sequence[Mapping[str, Any]]) -> str:
    payload = [
        {"path": row["path"], "sha256": row["sha256"], "size_bytes": row["size_bytes"]}
        for row in sorted(inventory, key=lambda row: str(row["path"]))
    ]
    return sha256_bytes(canonical_json_bytes(payload))


def load_release_documents(
    checker: Checker, directory: Path
) -> tuple[dict[str, dict[str, Any]], dict[str, bytes]]:
    root = checker.path(directory)
    require(root.is_dir(), f"release directory is missing: {directory}")
    expected_names = set(RELEASE_FILES) | {MANIFEST_NAME}
    actual_names = {item.name for item in root.iterdir() if item.is_file()}
    require(actual_names == expected_names and all(item.is_file() for item in root.iterdir()), f"{directory} is not the exact immutable artifact set")
    documents: dict[str, dict[str, Any]] = {}
    payloads: dict[str, bytes] = {}
    for name in sorted(expected_names):
        path = root / name
        payload = path.read_bytes()
        value = strict_json_object(payload, str(path))
        require(payload == encoded_document(value), f"{path} is not canonical JSON plus LF")
        verify_seal(value, str(path))
        documents[name] = value
        payloads[name] = payload
    return documents, payloads


def verify_manifest_inventory(
    manifest: Mapping[str, Any],
    documents: Mapping[str, Mapping[str, Any]],
    payloads: Mapping[str, bytes],
    label: str,
) -> str:
    inventory = manifest.get("artifacts")
    require(isinstance(inventory, list), f"{label} manifest inventory is malformed")
    require([row.get("path") for row in inventory] == sorted(RELEASE_FILES), f"{label} manifest artifact set/order drifted")
    for row in inventory:
        require(isinstance(row, dict) and set(row) == {"path", "sha256", "size_bytes", "row_count"}, f"{label} inventory row closure drifted")
        name = row["path"]
        require(row["sha256"] == sha256_bytes(payloads[name]), f"{label} artifact hash drifted: {name}")
        require(row["size_bytes"] == len(payloads[name]), f"{label} artifact size drifted: {name}")
        require(row["row_count"] == primary_row_count(documents[name]), f"{label} row count drifted: {name}")
    root = release_root(inventory)
    require(manifest.get("release_root_sha256") == root, f"{label} release root drifted")
    return root


def load_parent_release(
    checker: Checker,
) -> tuple[dict[str, dict[str, Any]], dict[str, bytes]]:
    documents, payloads = load_release_documents(checker, PARENT_DIR)
    manifest = documents[MANIFEST_NAME]
    require(manifest.get("release") == PARENT_RELEASE, "parent manifest release drifted")
    require(verify_manifest_inventory(manifest, documents, payloads, "parent 5.2") == PARENT_ROOT, "parent release root is not the frozen 5.2 root")
    catalog = documents["Claim_Catalog.json"]
    registry = documents["Claim_ID_Registry.json"]
    require(len(catalog.get("records", [])) == PARENT_CATALOG_ROWS, "parent catalog is not 3,100 rows")
    require(catalog.get("counts", {}).get("cumulative_theorems") == 1_500, "parent theorem count drifted")
    require(catalog.get("counts", {}).get("cumulative_open_claims") == 1_600, "parent open count drifted")
    require(registry.get("namespace_high_watermarks", {}).get("ATV") == PARENT_ATV_HIGH_WATERMARK, "parent ATV high-watermark drifted")
    require(registry.get("namespace_high_watermarks", {}).get("ATF") == PARENT_ATF_HIGH_WATERMARK, "parent ATF high-watermark drifted")
    return documents, payloads


def parent_identity_indexes(
    rows: Sequence[Mapping[str, Any]],
) -> tuple[dict[str, str], dict[str, str], dict[str, str]]:
    exact_sets: dict[str, set[str]] = defaultdict(set)
    normalized_sets: dict[str, set[str]] = defaultdict(set)
    name_sets: dict[str, set[str]] = defaultdict(set)
    for row in rows:
        variant_id = str(row["variant_id"])
        formal_statement = row.get("formal_statement")
        formal_sha = row.get("formal_type_sha256")
        formal_type = row.get("formal_type")
        name = row.get("qualified_name")
        if isinstance(formal_statement, dict):
            if not isinstance(formal_sha, str):
                candidate_sha = formal_statement.get("formal_type_sha256")
                if not isinstance(candidate_sha, str):
                    candidate_sha = formal_statement.get("declaration_type_sha256")
                formal_sha = candidate_sha
            if not isinstance(formal_type, str):
                candidate_type = formal_statement.get("formal_type")
                if not isinstance(candidate_type, str):
                    candidate_type = formal_statement.get("declaration_type")
                formal_type = candidate_type
            if not isinstance(name, str):
                candidate_name = formal_statement.get("declaration")
                if not isinstance(candidate_name, str):
                    candidate_name = formal_statement.get("qualified_declaration")
                name = candidate_name
        if isinstance(formal_sha, str) and SHA256_RE.fullmatch(formal_sha):
            exact_sets[formal_sha].add(variant_id)
        if isinstance(formal_type, str) and formal_type:
            normalized_sets[normalized_formal_type_sha256(formal_type)].add(variant_id)
        if isinstance(name, str) and name:
            name_sets[normalize_declaration_name(name)].add(variant_id)
    return (
        {key: min(values) for key, values in exact_sets.items()},
        {key: min(values) for key, values in normalized_sets.items()},
        {key: min(values) for key, values in name_sets.items()},
    )


def verify_parent_receipt(
    checker: Checker,
    receipt: Mapping[str, Any],
    parent: Mapping[str, Mapping[str, Any]],
    payloads: Mapping[str, bytes],
) -> None:
    binding = receipt.get("parent_release")
    require(isinstance(binding, dict), "5.3 parent receipt binding is malformed")
    manifest = parent[MANIFEST_NAME]
    require(binding.get("release") == PARENT_RELEASE and binding.get("release_root_sha256") == PARENT_ROOT, "5.3 parent receipt release/root drifted")
    require(binding.get("manifest_file_sha256") == sha256_bytes(payloads[MANIFEST_NAME]), "5.3 parent receipt manifest bytes drifted")
    require(binding.get("manifest_authority_sha256") == manifest["authority_sha256"], "5.3 parent receipt manifest authority drifted")
    inventory = receipt.get("artifact_inventory")
    require(isinstance(inventory, list) and {row.get("path") for row in inventory} == set(RELEASE_FILES), "5.3 parent receipt artifact set drifted")
    for row in inventory:
        name = row["path"]
        require(row.get("file_sha256") == sha256_bytes(payloads[name]), f"parent receipt artifact hash drifted: {name}")
        require(row.get("size_bytes") == len(payloads[name]), f"parent receipt artifact size drifted: {name}")
        require(row.get("row_count") == primary_row_count(parent[name]), f"parent receipt row count drifted: {name}")
        require(row.get("authority_sha256") == parent[name]["authority_sha256"], f"parent receipt authority drifted: {name}")
    identity = receipt.get("identity_boundary")
    require(isinstance(identity, dict), "parent receipt identity boundary is malformed")
    require(identity.get("variant_high_watermark") == PARENT_ATV_HIGH_WATERMARK and identity.get("family_high_watermark") == PARENT_ATF_HIGH_WATERMARK and identity.get("first_child_variant_ordinal") == 6_585, "parent receipt identity boundary drifted")
    counts = receipt.get("claim_count_boundary")
    require(isinstance(counts, dict), "parent receipt claim-count boundary is malformed")
    require(counts.get("catalog_records") == 3_100 and counts.get("theorem_records") == 1_500 and counts.get("open_claim_records") == 1_600, "parent receipt catalog counts drifted")
    require(counts.get("effective_strict_conjecture_credits") == 1_000 and counts.get("open_problem_records") == 599, "parent receipt strict/open-problem boundary drifted")
    strict = parent["Strict_Conjecture_Ledger.json"]
    strict_boundary = receipt.get("strict_credit_boundary")
    require(isinstance(strict_boundary, dict), "parent receipt strict boundary is malformed")
    require(strict_boundary.get("ledger_file_sha256") == sha256_bytes(payloads["Strict_Conjecture_Ledger.json"]), "parent strict-ledger file binding drifted")
    require(strict_boundary.get("ledger_authority_sha256") == strict["authority_sha256"], "parent strict-ledger authority drifted")
    require(strict_boundary.get("effective_credit_count") == len(strict["strict_credits"]) == 1_000, "parent strict-credit count drifted")
    require(strict_boundary.get("credit_correction_count") == len(strict["credit_corrections"]) == 1, "parent strict correction count drifted")


def verify_authorities(
    checker: Checker,
    parent: Mapping[str, Mapping[str, Any]],
    parent_payloads: Mapping[str, bytes],
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    contract, contract_payload = checker.load_json(CONTRACT_PATH)
    schema, schema_payload = checker.load_json(SCHEMA_PATH)
    registry, registry_payload = checker.load_json(SOURCE_REGISTRY_PATH)
    receipt, receipt_payload = checker.load_json(PARENT_RECEIPT_PATH)
    curation, curation_payload = checker.load_json(CURATION_PATH)
    for path, document in (
        (CONTRACT_PATH, contract),
        (SCHEMA_PATH, schema),
        (SOURCE_REGISTRY_PATH, registry),
        (PARENT_RECEIPT_PATH, receipt),
        (CURATION_PATH, curation),
    ):
        verify_seal(document, str(path))
    require(
        sha256_bytes(contract_payload) == CONTRACT_FILE_SHA256
        and contract.get("authority_sha256") == CONTRACT_AUTHORITY,
        "the independently frozen 5.3 contract anchor drifted",
    )
    require(
        sha256_bytes(schema_payload) == SCHEMA_FILE_SHA256
        and schema.get("authority_sha256") == SCHEMA_AUTHORITY,
        "the independently frozen 5.3 record-schema anchor drifted",
    )
    require(
        sha256_bytes(registry_payload) == SOURCE_REGISTRY_FILE_SHA256
        and registry.get("authority_sha256") == SOURCE_REGISTRY_AUTHORITY,
        "the independently frozen 5.3 source-registry anchor drifted",
    )
    require(
        sha256_bytes(receipt_payload) == PARENT_RECEIPT_FILE_SHA256
        and receipt.get("authority_sha256") == PARENT_RECEIPT_AUTHORITY,
        "the independently frozen 5.2 parent-receipt anchor drifted",
    )
    require(
        sha256_bytes(curation_payload) == CURATION_FILE_SHA256
        and curation.get("authority_sha256") == CURATION_AUTHORITY,
        "the independently frozen mathlib-curation anchor drifted",
    )
    require(contract.get("release") == RELEASE, "5.3 contract release drifted")
    require(contract.get("review_date") == REVIEW_DATE, "5.3 contract review date drifted")
    require(
        schema.get("$id")
        == "urn:awesome-theorems:schema:stage5-math-claim-record:5.3",
        "5.3 record-schema identity drifted",
    )
    bindings = contract.get("versioned_authorities")
    require(isinstance(bindings, dict), "5.3 authority bindings are malformed")
    for key, path, document in (
        ("record_schema", SCHEMA_PATH, schema),
        ("source_registry", SOURCE_REGISTRY_PATH, registry),
        ("parent_receipt", PARENT_RECEIPT_PATH, receipt),
    ):
        binding = bindings.get(key)
        require(isinstance(binding, dict), f"missing 5.3 authority binding: {key}")
        require(binding.get("path") == path.as_posix(), f"5.3 {key} path drifted")
        require(binding.get("file_sha256") == sha256_file(checker.path(path)), f"5.3 {key} file hash drifted")
        require(binding.get("authority_sha256") == document["authority_sha256"], f"5.3 {key} authority drifted")
    curation_binding = bindings.get("mathlib_curation_ledger")
    require(isinstance(curation_binding, dict), "missing curation authority binding")
    require(curation_binding.get("path") == CURATION_PATH.as_posix(), "curation authority path drifted")
    if curation_binding.get("file_sha256") is not None:
        require(curation_binding["file_sha256"] == sha256_file(checker.path(CURATION_PATH)), "contract curation file hash drifted")
    if curation_binding.get("authority_sha256") is not None:
        require(curation_binding["authority_sha256"] == curation["authority_sha256"], "contract curation authority drifted")
    curation_contract = contract.get("curation_ledger_contract")
    require(isinstance(curation_contract, dict), "contract curation-ledger policy is malformed")
    require(curation_contract.get("schema_version") == "awesome-theorems/mathlib-theorem-curation/5.3", "contract/curation schema interface drifted")
    require(set(curation_contract.get("top_level_required_fields", [])) == set(curation), "contract/curation top-level closure differs")
    require(set(curation_contract.get("candidate_disposition_required_fields", [])) == CURATION_ROW_FIELDS, "contract/curation row interface differs")
    require(set(curation_contract.get("disposition_enum", [])) == {"accepted_new_kernel_checked_theorem", "eligible_not_selected", "rejected_nonliteral_lemma", "rejected_source_semantic_duplicate"}, "contract/curation disposition interface differs")
    require(registry.get("schema_version") == "awesome-theorems/stage5-math-source-registry/5.3", "5.3 source registry schema drifted")
    sources = registry.get("sources")
    require(isinstance(sources, list), "5.3 source registry sources is malformed")
    matches = [row for row in sources if isinstance(row, dict) and row.get("source_id") == SOURCE_ID]
    require(len(matches) == 1, "5.3 source registry lacks one unique mathlib source")
    asset = matches[0].get("asset")
    require(isinstance(asset, dict), "mathlib source-registry asset is malformed")
    require(asset.get("path") == SOURCE_PATH.as_posix() and asset.get("sha256") == SOURCE_FILE_SHA256 and asset.get("size_bytes") == SOURCE_FILE_SIZE and asset.get("record_count") == SOURCE_ROWS and asset.get("content_digest_before_self_field") == SOURCE_CONTENT_DIGEST, "mathlib source-registry asset binding drifted")
    facts = matches[0].get("content_facts")
    require(isinstance(facts, dict), "mathlib source-registry content facts are malformed")
    require(facts.get("literal_theorem_records") == LITERAL_THEOREMS and facts.get("literal_lemma_records") == LITERAL_LEMMAS and facts.get("unique_literal_theorem_formal_type_sha256") == UNIQUE_FORMAL_TYPES and facts.get("duplicate_formal_type_excess_rows") == DUPLICATE_LOSERS, "mathlib source-registry theorem/dedupe facts drifted")
    verify_parent_receipt(checker, receipt, parent, parent_payloads)
    return contract, schema, registry, receipt, curation


def semantic_key(row: Mapping[str, Any]) -> str:
    return "mathlib-theorem-semantic/" + str(row["formal_type_sha256"])


def expected_curation_rows(
    source_rows: Sequence[dict[str, Any]],
    parent_rows: Sequence[Mapping[str, Any]],
) -> tuple[list[dict[str, Any]], list[tuple[dict[str, Any], dict[str, Any]]]]:
    selected, winner_for_id, duplicate_losers = select_mathlib_rows(source_rows)
    selected_ranks = {
        str(row["source_record_id"]): rank
        for rank, row in enumerate(selected, start=1)
    }
    parent_exact, parent_normalized, parent_names = parent_identity_indexes(parent_rows)
    parent_links: dict[str, str] = {}
    for row in source_rows:
        if row["declaration_kind"] != "theorem":
            continue
        candidates = {
            value
            for value in (
                parent_exact.get(str(row["formal_type_sha256"])),
                parent_normalized.get(normalized_formal_type_sha256(str(row["formal_type"]))),
                parent_names.get(normalize_declaration_name(str(row["declaration"]))),
            )
            if value is not None
        }
        if candidates:
            parent_links[str(row["source_record_id"])] = min(candidates)
    require(not parent_links, "mathlib literal theorem pool unexpectedly intersects parent identities")

    expected: list[dict[str, Any]] = []
    accepted: list[tuple[dict[str, Any], dict[str, Any]]] = []
    for source_index, source in enumerate(source_rows):
        source_id = str(source["source_record_id"])
        canonical_id = duplicate_losers.get(source_id)
        parent_variant = parent_links.get(source_id)
        if source["declaration_kind"] == "lemma":
            disposition = "rejected_nonliteral_lemma"
            reason = "literal_declaration_kind_is_lemma"
        elif source["formal_proof_state"] != "kernel_checked_sorry_free":
            disposition = "rejected_proof_boundary"
            reason = "not_kernel_checked_sorry_free"
        elif parent_variant is not None:
            disposition = "rejected_parent_duplicate"
            reason = "exact_name_or_formal_type_already_in_parent_5_2"
        elif canonical_id is not None:
            canonical = winner_for_id[source_id]
            if normalize_declaration_name(str(source["declaration"])) == normalize_declaration_name(str(canonical["declaration"])):
                disposition = "rejected_source_name_duplicate"
                reason = "normalized_declaration_name_duplicate"
            else:
                disposition = "rejected_source_semantic_duplicate"
                reason = "normalized_formal_type_duplicate"
        elif source_id in selected_ranks:
            disposition = "accepted_new_kernel_checked_theorem"
            reason = "selected_docs_1000_priority_seed" if selected_ranks[source_id] <= PHASE_ONE_ROWS else "selected_module_main_round_robin_fill"
        else:
            disposition = "eligible_not_selected"
            reason = "viable_theorem_outside_exact_500_selection"
        grants = disposition == "accepted_new_kernel_checked_theorem"
        accepted_rank = selected_ranks.get(source_id) if grants else None
        item_ordinal = PARENT_ATV_HIGH_WATERMARK + accepted_rank if accepted_rank is not None else None
        if canonical_id is not None:
            rationale = "Exact equality of the pinned pretty-printed formal_type SHA-256; the higher-ranked source row is the sole canonical candidate."
            confidence = "exact"
            reviewer = "deterministic_exact_identity_v1"
        elif parent_variant is not None:
            rationale = "Exact full qualified-name or exact/whitespace-normalized formal-type identity with the sealed parent Claim_Catalog."
            confidence = "exact"
            reviewer = "deterministic_parent_identity_v1"
        else:
            rationale = None
            confidence = None
            reviewer = None
        semantic = semantic_key(source)
        row: dict[str, Any] = {
            "candidate_key": f"mathlib:{source_id}",
            "source_index": source_index,
            "source_record_id": source_id,
            "source_record_sha256": source_record_sha256(source),
            "declaration": source["declaration"],
            "declaration_kind": source["declaration_kind"],
            "source_syntax_kind": source["source_syntax_kind"],
            "selection_rank": source["selection_rank"],
            "selection_cohort": source["selection_cohort"],
            "formal_proof_state": source["formal_proof_state"],
            "formal_type_sha256": source["formal_type_sha256"],
            "formal_docstring_sha256": source["formal_docstring_sha256"],
            "proof_evidence_payload_sha256": sha256_bytes(canonical_json_bytes(source["proof_evidence"])),
            "importance_payload_sha256": sha256_bytes(canonical_json_bytes(source["importance_signals"])),
            "rights_payload_sha256": sha256_bytes(canonical_json_bytes(source["rights"])),
            "semantic_key": semantic,
            "semantic_key_method": "exact_formal_type_sha256_v1",
            "semantic_key_payload_sha256": sha256_bytes(
                canonical_json_bytes(
                    {
                        "method": "exact_formal_type_sha256_v1",
                        "formal_type_sha256": source["formal_type_sha256"],
                    }
                )
            ),
            "disposition": disposition,
            "reason_code": reason,
            "accepted_rank": accepted_rank,
            "target_variant_id": f"ATV-{item_ordinal:08d}" if item_ordinal is not None else None,
            "target_s5_id": f"S5-CLM-{item_ordinal:08d}" if item_ordinal is not None else None,
            "canonical_source_record_id": canonical_id,
            "duplicate_of_semantic_key": semantic if canonical_id is not None else None,
            "duplicate_of_variant_id": parent_variant,
            "dedupe_rationale": rationale,
            "dedupe_confidence": confidence,
            "dedupe_reviewer": reviewer,
            "grants_catalog_entry": grants,
            "grants_theorem_credit": grants,
        }
        row["row_sha256"] = hash_without(row, "row_sha256")
        require(set(row) == CURATION_ROW_FIELDS, "independent curation row field closure drifted")
        expected.append(row)
        if grants:
            accepted.append((row, source))
    accepted.sort(key=lambda pair: int(pair[0]["accepted_rank"]))
    require(len(accepted) == NEW_ROWS, "independent curation replay did not accept 500 rows")
    return expected, accepted


def verify_curation(
    curation: Mapping[str, Any],
    registry: Mapping[str, Any],
    receipt: Mapping[str, Any],
    source_rows: Sequence[dict[str, Any]],
    parent_rows: Sequence[Mapping[str, Any]],
) -> list[tuple[dict[str, Any], dict[str, Any]]]:
    required_top = {
        "schema_version",
        "source_id",
        "source_registry_authority_sha256",
        "source_asset_sha256",
        "parent_receipt_authority_sha256",
        "candidate_dispositions",
        "counts",
        "set_digests",
        "authority_sha256",
    }
    require(set(curation) == required_top, "mathlib curation top-level closure drifted")
    require(curation.get("schema_version") == "awesome-theorems/mathlib-theorem-curation/5.3", "mathlib curation schema drifted")
    require(curation.get("source_id") == SOURCE_ID, "mathlib curation source ID drifted")
    require(curation.get("source_registry_authority_sha256") == registry["authority_sha256"], "mathlib curation registry binding drifted")
    require(curation.get("parent_receipt_authority_sha256") == receipt["authority_sha256"], "mathlib curation parent-receipt binding drifted")
    require(curation.get("source_asset_sha256") == SOURCE_FILE_SHA256, "mathlib curation source asset binding drifted")
    expected_rows, accepted = expected_curation_rows(source_rows, parent_rows)
    require(curation.get("candidate_dispositions") == expected_rows, "mathlib curation does not exactly replay the 1,500-row selection")
    dispositions = Counter(str(row["disposition"]) for row in expected_rows)
    selected_sources = [source for _, source in accepted]
    selected_by_root = Counter(module_root(row) for row in selected_sources)
    selected_by_tier = Counter(importance_tier(row) for row in selected_sources)
    expected_counts = {
        "source_rows": SOURCE_ROWS,
        "candidate_disposition_rows": SOURCE_ROWS,
        "eligible_literal_theorems": LITERAL_THEOREMS,
        "pre_eligibility_excluded_lemmas": LITERAL_LEMMAS,
        "literal_theorems": LITERAL_THEOREMS,
        "literal_lemmas": LITERAL_LEMMAS,
        "kernel_checked_sorry_free": SOURCE_ROWS,
        "accepted": NEW_ROWS,
        "nonaccepted_eligible": LITERAL_THEOREMS - NEW_ROWS,
        "nonaccepted_total": SOURCE_ROWS - NEW_ROWS,
        "docs_1000_priority_seed": PHASE_ONE_ROWS,
        "module_main_balanced_fill": PHASE_TWO_ROWS,
        "source_semantic_duplicate_rows": DUPLICATE_LOSERS,
        "parent_duplicate_rows": 0,
        "selected_branches": len(selected_by_root),
        "selected_with_docs_1000_signal": sum(has_importance_signal(row, DOCS_SIGNAL) for row in selected_sources),
        "selected_with_module_main_signal": sum(has_importance_signal(row, MODULE_SIGNAL) for row in selected_sources),
        "by_disposition": dict(sorted(dispositions.items())),
        "selected_by_module_root": dict(sorted(selected_by_root.items())),
        "selected_by_importance_tier": dict(sorted(selected_by_tier.items())),
    }
    require(curation.get("counts") == expected_counts, "mathlib curation counts drifted")
    accepted_rows = [row for row, _ in accepted]
    expected_digests = {
        "candidate_source_record_id_set_sha256": set_digest(str(row["source_record_id"]) for row in expected_rows),
        "eligible_theorem_source_record_id_set_sha256": set_digest(str(row["source_record_id"]) for row in expected_rows if row["declaration_kind"] == "theorem"),
        "excluded_lemma_source_record_id_set_sha256": set_digest(str(row["source_record_id"]) for row in expected_rows if row["disposition"] == "rejected_nonliteral_lemma"),
        "nonaccepted_eligible_source_record_id_set_sha256": set_digest(str(row["source_record_id"]) for row in expected_rows if row["declaration_kind"] == "theorem" and row["disposition"] != "accepted_new_kernel_checked_theorem"),
        "selected_source_record_id_set_sha256": set_digest(str(row["source_record_id"]) for row in accepted_rows),
        "selected_declaration_set_sha256": set_digest(str(row["declaration"]) for row in accepted_rows),
        "selected_formal_type_sha256_set_sha256": set_digest(str(row["formal_type_sha256"]) for row in accepted_rows),
        "selected_semantic_key_set_sha256": set_digest(str(row["semantic_key"]) for row in accepted_rows),
        "selected_variant_id_set_sha256": set_digest(str(row["target_variant_id"]) for row in accepted_rows),
        "selected_s5_id_set_sha256": set_digest(str(row["target_s5_id"]) for row in accepted_rows),
        "candidate_row_sha256_set_sha256": set_digest(str(row["row_sha256"]) for row in expected_rows),
    }
    require(curation.get("set_digests") == expected_digests, "mathlib curation set digests drifted")
    lemma_rows = [row for row in expected_rows if row["declaration_kind"] == "lemma"]
    require(len(lemma_rows) == LITERAL_LEMMAS and all(not row["grants_theorem_credit"] and row["accepted_rank"] is None for row in lemma_rows), "a literal lemma receives theorem credit or identity")
    duplicate_rows = [row for row in expected_rows if row["canonical_source_record_id"] is not None]
    require(len(duplicate_rows) == DUPLICATE_LOSERS and all(not row["grants_theorem_credit"] and row["accepted_rank"] is None for row in duplicate_rows), "a formal-type duplicate receives theorem credit or identity")
    return accepted


def theorem_predicate(row: Mapping[str, Any]) -> bool:
    base = bool(
        row.get("lifecycle") == "active"
        and row.get("record_role") == "claim"
        and row.get("atomicity") == "atomic"
        and row.get("truth_apt") is True
        and row.get("category") == "theorem"
        and row.get("current_claim_kind") == "theorem"
        and row.get("material_status") == "proved"
    )
    if not base:
        return False
    if row.get("origin_release") == RELEASE:
        formal = row.get("formal_statement")
        proof = row.get("proof_evidence")
        return bool(
            isinstance(formal, dict)
            and formal.get("declaration_kind") == "theorem"
            and formal.get("source_syntax_kind") == "theorem"
            and isinstance(proof, dict)
            and proof.get("formal_proof_state") == "kernel_checked_sorry_free"
            and proof.get("uses_sorry") is False
        )
    return row.get("declaration_kind") == "theorem"


def open_predicate(row: Mapping[str, Any]) -> bool:
    base = bool(
        row.get("lifecycle") == "active"
        and row.get("record_role") == "claim"
        and row.get("atomicity") == "atomic"
        and row.get("truth_apt") is True
        and row.get("category") == "open_claim"
        and row.get("current_claim_kind") in {"conjecture", "hypothesis", "open_problem"}
        and row.get("material_status") in {"open", "partial", "independent", "disputed"}
    )
    if not base:
        return False
    if row.get("origin_release") == "5.2":
        source_block = row.get("source_block")
        return isinstance(source_block, dict) and source_block.get("language") == "LaTeX"
    return row.get("declaration_kind") == "theorem"


def validate_new_record_schema(
    row: Mapping[str, Any], schema: Mapping[str, Any], index: int
) -> None:
    """Validate an origin-5.3 row with the separately loaded closed schema."""

    require(jsonschema is not None, "the independent checker requires jsonschema")
    try:
        validator_type = jsonschema.validators.validator_for(schema)
        validator_type.check_schema(schema)
        errors = sorted(
            validator_type(schema).iter_errors(row),
            key=lambda error: tuple(str(part) for part in error.absolute_path),
        )
    except Exception as error:  # pragma: no cover - defensive dependency boundary
        raise CheckFailure(f"cannot evaluate the 5.3 record schema: {error}") from error
    if errors:
        first = errors[0]
        location = ".".join(str(part) for part in first.absolute_path) or "$"
        raise CheckFailure(
            f"origin-5.3 catalog row {index} fails schema at {location}: {first.message}"
        )


def expected_claim_row(
    checker: Checker,
    ledger_row: Mapping[str, Any],
    source: Mapping[str, Any],
    schema: Mapping[str, Any],
    parent_registry_authority: str,
    curation_authority: str,
    curation_file_sha256: str,
    parent_catalog_file_sha256: str,
) -> dict[str, Any]:
    """Independently materialize one accepted mathlib theorem record."""

    rank = int(ledger_row["accepted_rank"])
    atv_ordinal = PARENT_ATV_HIGH_WATERMARK + rank
    atf_ordinal = PARENT_ATF_HIGH_WATERMARK + rank
    source_id = str(source["source_record_id"])
    source_hash = source_record_sha256(source)
    source_data = source["source"]
    semantic = semantic_key(source)
    formal_type = str(source["formal_type"])
    formal_sha = str(source["formal_type_sha256"])
    root = module_root(source)

    source_locator = {
        "source_id": SOURCE_ID,
        "artifact_path": SOURCE_PATH.as_posix(),
        "artifact_sha256": SOURCE_FILE_SHA256,
        "artifact_size_bytes": SOURCE_FILE_SIZE,
        "record_index": ledger_row["source_index"],
        "source_record_id": source_id,
        "source_record_sha256": source_hash,
        "mathlib_commit": MATHLIB_COMMIT,
        "module": source_data["module"],
        "source_path": source_data["path"],
        "source_sha256": source_data["source_sha256"],
        "url": source_data["url"],
        "source_range": copy.deepcopy(source_data["range"]),
        "selection_range": copy.deepcopy(source_data["selection_range"]),
    }
    formal_statement = {
        "language": "Lean4",
        "completeness": "exact_runtime_formal_type_and_source_locator",
        "declaration": source["declaration"],
        "declaration_kind": source["declaration_kind"],
        "source_syntax_kind": source["source_syntax_kind"],
        "module": source_data["module"],
        "formal_type": formal_type,
        "formal_type_sha256": formal_sha,
        "formal_docstring": source["formal_docstring"],
        "formal_docstring_origin": source["formal_docstring_origin"],
        "formal_docstring_sha256": source["formal_docstring_sha256"],
    }
    mathematical_statement = seal_field(
        {
            "completeness": "exact_formal",
            "language": "Lean4",
            "natural_language": source["exact_curated_summary"],
            "formal_type": formal_type,
            "formal_type_sha256": formal_sha,
        },
        "statement_sha256",
    )
    theorem_selection = {
        "source_record_id": source_id,
        "selection_cohort": source["selection_cohort"],
        "selection_rank": source["selection_rank"],
        "display_label": source["display_label"],
        "exact_curated_summary": source["exact_curated_summary"],
        "importance_signals": copy.deepcopy(source["importance_signals"]),
        "selection_phase": ledger_row["reason_code"],
        "phase_rank": rank if rank <= PHASE_ONE_ROWS else rank - PHASE_ONE_ROWS,
        "module_root": root,
    }
    curator_disposition = {
        "curation_ledger_path": CURATION_PATH.as_posix(),
        "curation_ledger_file_sha256": curation_file_sha256,
        "curation_ledger_authority_sha256": curation_authority,
        "source_index": ledger_row["source_index"],
        "source_record_id": source_id,
        "curation_row_sha256": ledger_row["row_sha256"],
        "disposition": ledger_row["disposition"],
        "reason_code": ledger_row["reason_code"],
        "accepted_rank": rank,
        "target_variant_id": ledger_row["target_variant_id"],
        "target_s5_id": ledger_row["target_s5_id"],
        "grants_catalog_entry": ledger_row["grants_catalog_entry"],
        "grants_theorem_credit": ledger_row["grants_theorem_credit"],
        "semantic_key": semantic,
    }
    status_detail = {
        "source_material_status": source["material_status"]["status"],
        "status_as_of_commit": source["material_status"]["as_of_commit"],
        "basis": source["material_status"]["basis"],
        "source_refs": [SOURCE_ID],
        "evidence_level": "kernel_checked_sorry_free_at_pinned_commit",
        "later_commit_status_not_inferred": True,
    }
    classification = {
        "msc2020_code": source["msc2020"]["code"],
        "basis": source["msc2020"]["basis"],
        "status": (
            "source_curated_exact"
            if source["msc2020"]["basis"] == "1000_plus_curated"
            else "machine_root_crosswalk"
        ),
        "module_root": root,
    }
    provenance = {
        "formal_source_ref": SOURCE_ID,
        "source_refs": [SOURCE_ID],
        "extraction_mode": "pinned_mathlib_runtime_extraction",
        "extractor_path": "Docs/tools/extract_mathlib_theorems_v5.py",
        "extractor_version": "1.1.0",
        "extractor_file_sha256": "0e26af2b6740abf4626f3cf43d84fb8f7e1f1a6104096e71f1f9b1f2c33189af",
        "source_asset_sha256": SOURCE_FILE_SHA256,
        "source_record_id": source_id,
        "source_record_sha256": source_hash,
        "mathlib_commit": MATHLIB_COMMIT,
        "exact_source_replay_required": True,
    }
    docs_signal = has_importance_signal(source, DOCS_SIGNAL)
    rights = seal_field(
        {
            "formal_code_terms": "Apache-2.0",
            "docstring_terms": "Apache-2.0",
            "optional_metadata_terms": "Unlicense" if docs_signal else "not_applicable",
            "status": "cleared_with_attribution",
            "redistribution_mode": "apache_2_0_with_attribution",
            "attribution": ["The mathlib Community"],
            "source_refs": [SOURCE_ID],
            "mathlib_license_sha256": MATHLIB_LICENSE_SHA256,
            "catalog_relicenses_source": False,
        },
        "rights_payload_sha256",
    )
    source_proof = source["proof_evidence"]
    proof_evidence = seal_field(
        {
            "formal_proof_state": source["formal_proof_state"],
            "verification": source_proof["verification"],
            "uses_sorry": source_proof["uses_sorry"],
            "compiled_module": source_proof["compiled_module"],
            "ilean_path": source_proof["ilean_path"],
            "ilean_sha256": source_proof["ilean_sha256"],
            "olean_path": source_proof["olean_path"],
            "olean_sha256": source_proof["olean_sha256"],
            "batch_axiom_dependency_union": copy.deepcopy(
                source_proof["batch_axiom_dependency_union"]
            ),
            "axiom_evidence_scope": "batch_union_not_per_declaration_exact_dependencies",
            "mathlib_commit": MATHLIB_COMMIT,
        },
        "proof_payload_sha256",
    )
    importance = {
        "tier": "source_signaled_mathlib_theorem",
        "basis": (
            "mathlib_1000_formalized_signal"
            if docs_signal
            else "mathlib_module_main_result_signal"
        ),
        "rationale": (
            "Selected from the pinned formalized mathlib 1000-theorems signal."
            if docs_signal
            else "Selected from a pinned mathlib module Main-result signal."
        ),
        "evidence_level": "source_documentation_signal",
        "independent_universal_ranking_claimed": False,
    }
    dedupe = {
        "normalized_declaration_key": normalize_declaration_name(
            str(source["declaration"])
        ),
        "formal_type_sha256": formal_sha,
        "source_record_sha256": source_hash,
        "semantic_key": semantic,
        "candidate_atv_ids": [],
        "parent_catalog_file_sha256": parent_catalog_file_sha256,
        "verdict": "unique_after_source_and_parent_curation",
        "validation_status": "machine_replayed_and_manifest_bound_curation",
        "duplicate_grants_quota": False,
        "no_evidence_or_status_inheritance": True,
    }
    allocation_request = {
        "origin_release": RELEASE,
        "source_id": SOURCE_ID,
        "source_record_id": source_id,
        "source_record_sha256": source_hash,
        "semantic_key": semantic,
        "statement_sha256": mathematical_statement["statement_sha256"],
        "family_action": "new_family",
    }
    allocation = {
        "parent_registry_authority_sha256": parent_registry_authority,
        "parent_release_root_sha256": PARENT_ROOT,
        "allocation_request_sha256": sha256_bytes(
            canonical_json_bytes(allocation_request)
        ),
        "transaction_id": f"S5-ALLOC-{atv_ordinal:08d}",
        "family_action": "new_family",
        "append_only": True,
    }
    aliases = list(
        dict.fromkeys(
            value
            for value in (
                str(source["declaration"]),
                str(source["exact_curated_summary"]),
            )
            if value != str(source["display_label"])
        )
    )
    row: dict[str, Any] = {
        "schema_version": "awesome-theorems/stage5-math-claim-record/5.3",
        "release_id": RELEASE,
        "origin_stage": "Stage5",
        "origin_release": RELEASE,
        "curation_key": f"mathlib/{source_id}",
        "allocation": allocation,
        "occurrence_id": f"ATO-{atv_ordinal:08d}",
        "family_id": f"ATF-{atf_ordinal:08d}",
        "sense_id": f"ATS-{atv_ordinal:08d}",
        "variant_id": f"ATV-{atv_ordinal:08d}",
        "stage_claim_id": f"S5-CLM-{atv_ordinal:08d}",
        "display_name": source["display_label"],
        "aliases": aliases,
        "owner_domain": "mathematics",
        "membership_domains": ["mathematics"],
        "record_role": "claim",
        "claim_kind": "theorem",
        "current_claim_kind": "theorem",
        "historical_kind": "theorem",
        "atomicity": "atomic",
        "truth_apt": True,
        "category": "theorem",
        "material_status": "proved",
        "source_id": SOURCE_ID,
        "source_locator": source_locator,
        "formal_statement": formal_statement,
        "theorem_selection": theorem_selection,
        "curator_disposition": curator_disposition,
        "mathematical_statement": mathematical_statement,
        "status_detail": status_detail,
        "classification": classification,
        "provenance": provenance,
        "rights": rights,
        "dedupe": dedupe,
        "proof_evidence": proof_evidence,
        "importance": importance,
        "lifecycle": "active",
        "lineage": [],
        "semantic_key": semantic,
    }
    row["content_payload_sha256"] = sha256_bytes(
        canonical_json_bytes(
            {
                "formal_statement": formal_statement,
                "mathematical_statement": mathematical_statement,
            }
        )
    )
    row["source_payload_sha256"] = sha256_bytes(
        canonical_json_bytes(
            {
                "source_locator": source_locator,
                "theorem_selection": theorem_selection,
                "provenance": provenance,
            }
        )
    )
    row["proof_payload_sha256"] = proof_evidence["proof_payload_sha256"]
    row["semantic_payload_sha256"] = sha256_bytes(
        canonical_json_bytes(
            {
                "record_role": row["record_role"],
                "atomicity": row["atomicity"],
                "truth_apt": row["truth_apt"],
                "category": row["category"],
                "current_claim_kind": row["current_claim_kind"],
                "semantic_key": semantic,
                "statement_sha256": mathematical_statement["statement_sha256"],
            }
        )
    )
    require(
        set(row) == set(schema.get("required", [])) == set(schema.get("properties", {})),
        "independent 5.3 claim-record field closure drifted",
    )
    require(
        row["variant_id"] == ledger_row["target_variant_id"]
        and row["stage_claim_id"] == ledger_row["target_s5_id"],
        "independent allocation differs from curation targets",
    )
    return row


def expected_authoritative_inputs(
    checker: Checker,
    contract: Mapping[str, Any],
    schema: Mapping[str, Any],
    registry: Mapping[str, Any],
    receipt: Mapping[str, Any],
    curation: Mapping[str, Any],
    parent: Mapping[str, Mapping[str, Any]],
    parent_payloads: Mapping[str, bytes],
) -> dict[str, Any]:
    def authority(path: Path, document: Mapping[str, Any]) -> dict[str, Any]:
        resolved = checker.path(path)
        return {
            "path": path.as_posix(),
            "file_sha256": sha256_file(resolved),
            "size_bytes": resolved.stat().st_size,
            "authority_sha256": document["authority_sha256"],
        }

    return {
        "contract": authority(CONTRACT_PATH, contract),
        "record_schema": authority(SCHEMA_PATH, schema),
        "source_registry": authority(SOURCE_REGISTRY_PATH, registry),
        "parent_receipt": authority(PARENT_RECEIPT_PATH, receipt),
        "curation_ledger": authority(CURATION_PATH, curation),
        "mathlib_asset": {
            "path": SOURCE_PATH.as_posix(),
            "file_sha256": SOURCE_FILE_SHA256,
            "size_bytes": SOURCE_FILE_SIZE,
            "content_digest_before_self_field": SOURCE_CONTENT_DIGEST,
            "mathlib_commit": MATHLIB_COMMIT,
        },
        "parent_release": {
            "release": PARENT_RELEASE,
            "release_root_sha256": PARENT_ROOT,
            "manifest_file_sha256": sha256_bytes(parent_payloads[MANIFEST_NAME]),
            "manifest_authority_sha256": parent[MANIFEST_NAME]["authority_sha256"],
            "registry_authority_sha256": parent["Claim_ID_Registry.json"][
                "authority_sha256"
            ],
        },
    }


def expected_registry_rows(
    rows: Sequence[Mapping[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    families: list[dict[str, Any]] = []
    senses: list[dict[str, Any]] = []
    variants: list[dict[str, Any]] = []
    for row in rows:
        request = row["allocation"]["allocation_request_sha256"]
        families.append(
            {
                "family_id": row["family_id"],
                "curation_key": row["curation_key"],
                "display_titles": list(
                    dict.fromkeys([row["display_name"]] + list(row["aliases"]))
                ),
                "member_occurrence_ids": [row["occurrence_id"]],
                "historical_member_occurrence_ids": [row["occurrence_id"]],
                "idempotency_request_sha256": request,
                "identity_state": "stage5_mathlib_exact_formal_type_family",
                "lifecycle": "current",
                "semantic_equivalence_asserted": True,
            }
        )
        senses.append(
            {
                "sense_id": row["sense_id"],
                "family_id": row["family_id"],
                "bootstrap_occurrence_id": row["occurrence_id"],
                "curation_key": row["curation_key"],
                "idempotency_request_sha256": request,
                "identity_state": "stage5_mathlib_exact_formal_type_sense",
                "lifecycle": "current",
            }
        )
        variants.append(
            {
                "variant_id": row["variant_id"],
                "sense_id": row["sense_id"],
                "bootstrap_occurrence_id": row["occurrence_id"],
                "curation_key": row["curation_key"],
                "idempotency_request_sha256": request,
                "semantic_payload_sha256": row["semantic_payload_sha256"],
                "identity_state": "stage5_mathlib_exact_formal_type_variant",
                "lifecycle": "current",
            }
        )
    return families, senses, variants


def expected_coverage(
    parent: Mapping[str, Any],
    curation: Mapping[str, Any],
    new_rows: Sequence[Mapping[str, Any]],
    inputs: Mapping[str, Any],
) -> dict[str, Any]:
    additions = [
        {
            "candidate_key": row["candidate_key"],
            "source_id": SOURCE_ID,
            "source_index": row["source_index"],
            "source_record_id": row["source_record_id"],
            "source_record_sha256": row["source_record_sha256"],
            "declaration": row["declaration"],
            "declaration_kind": row["declaration_kind"],
            "source_syntax_kind": row["source_syntax_kind"],
            "formal_type_sha256": row["formal_type_sha256"],
            "semantic_key": row["semantic_key"],
            "disposition": row["disposition"],
            "reason_code": row["reason_code"],
            "accepted_rank": row["accepted_rank"],
            "target_variant_id": row["target_variant_id"],
            "target_s5_id": row["target_s5_id"],
            "canonical_source_record_id": row["canonical_source_record_id"],
            "duplicate_of_semantic_key": row["duplicate_of_semantic_key"],
            "duplicate_of_variant_id": row["duplicate_of_variant_id"],
            "grants_catalog_entry": row["grants_catalog_entry"],
            "grants_theorem_credit": row["grants_theorem_credit"],
            "origin_release": RELEASE,
            "curation_row_sha256": row["row_sha256"],
        }
        for row in curation["candidate_dispositions"]
    ]
    by_code: dict[str, list[Mapping[str, Any]]] = defaultdict(list)
    for row in new_rows:
        by_code[str(row["classification"]["msc2020_code"])].append(row)
    coverage_rows: list[dict[str, Any]] = []
    for parent_row in parent["msc_coverage"]:
        row = copy.deepcopy(parent_row)
        code = str(row["msc_top_class"])
        selected = by_code.pop(code, [])
        new_ids = sorted(str(item["stage_claim_id"]) for item in selected)
        row["current_theorem_s5_ids"] = sorted(
            list(row["current_theorem_s5_ids"]) + new_ids
        )
        row["origin_theorem_s5_ids"] = new_ids
        row["origin_open_s5_ids"] = []
        if selected:
            row["source_ids"] = sorted(set(row["source_ids"]) | {SOURCE_ID})
        exact = sum(
            item["classification"]["basis"] == "1000_plus_curated"
            for item in selected
        )
        row["classification_basis_counts"]["source_annotation"] += exact
        row["classification_basis_counts"]["machine_crosswalk"] += len(selected) - exact
        counts = row["counts"]
        counts.update(
            {
                "current_theorems": len(row["current_theorem_s5_ids"]),
                "current_open": len(row["current_open_s5_ids"]),
                "origin_theorems": len(new_ids),
                "origin_open": 0,
                "open_reserve": len(row["open_reserve_candidate_keys"]),
            }
        )
        classified = (
            counts["current_theorems"] + counts["current_open"] + counts["open_reserve"]
        )
        if classified == 0:
            row["scarcity"] = "zero"
            row["scarcity_reason"] = (
                "No current or open-reserve member has this primary source annotation."
            )
        elif classified < 10:
            row["scarcity"] = "thin"
            row["scarcity_reason"] = (
                "Fewer than ten current-plus-reserve members have this primary class."
            )
        else:
            row["scarcity"] = "adequate_in_source_inventory"
            row["scarcity_reason"] = (
                "At least ten current-plus-reserve members have this primary class."
            )
        coverage_rows.append(row)
    require(not by_code, f"new records use unknown MSC classes: {sorted(by_code)}")
    dispositions = Counter(str(row["disposition"]) for row in additions)
    candidates = copy.deepcopy(parent["candidate_dispositions"]) + additions
    return seal(
        {
            "schema_version": "awesome-theorems/stage5-coverage-ledger/5.3",
            "release": RELEASE,
            "authoritative_inputs": copy.deepcopy(inputs),
            "candidate_dispositions": candidates,
            "msc_coverage": coverage_rows,
            "counts": {
                "candidate_dispositions": len(candidates),
                "msc_coverage": len(coverage_rows),
                "origin_5_3_candidates": len(additions),
                "origin_5_3_accepted_new_theorems": dispositions[
                    "accepted_new_kernel_checked_theorem"
                ],
                "origin_5_3_literal_lemma_noncredit": dispositions[
                    "rejected_nonliteral_lemma"
                ],
                "origin_5_3_source_duplicate_noncredit": dispositions[
                    "rejected_source_semantic_duplicate"
                ],
                "origin_5_3_eligible_not_selected": dispositions[
                    "eligible_not_selected"
                ],
            },
        }
    )


def expected_release_artifacts(
    inputs: Mapping[str, Any],
    parent: Mapping[str, Mapping[str, Any]],
    curation: Mapping[str, Any],
    new_rows: Sequence[dict[str, Any]],
) -> dict[str, dict[str, Any]]:
    parent_catalog = parent["Claim_Catalog.json"]
    all_rows = copy.deepcopy(parent_catalog["records"]) + list(new_rows)
    catalog = seal(
        {
            "schema_version": "awesome-theorems/stage5-claim-catalog/5.3",
            "artifact": "Claim_Catalog.json",
            "release": RELEASE,
            "catalog_scope": parent_catalog["catalog_scope"],
            "authoritative_inputs": copy.deepcopy(inputs),
            "counts": {
                "records": len(all_rows),
                "origin_theorems": sum(theorem_predicate(row) for row in new_rows),
                "origin_open_claims": sum(open_predicate(row) for row in new_rows),
                "cumulative_theorems": sum(theorem_predicate(row) for row in all_rows),
                "cumulative_open_claims": sum(open_predicate(row) for row in all_rows),
            },
            "records": all_rows,
        }
    )
    require(
        catalog["counts"]
        == {
            "records": 3_600,
            "origin_theorems": 500,
            "origin_open_claims": 0,
            "cumulative_theorems": 2_000,
            "cumulative_open_claims": 1_600,
        },
        "independent theorem/open predicates do not reproduce the 5.3 counts",
    )

    parent_registry = parent["Claim_ID_Registry.json"]
    families, senses, variants = expected_registry_rows(new_rows)
    allocation_policy = copy.deepcopy(parent_registry["allocation_policy"])
    allocation_policy.update(
        {
            "release_5_3_first_new_atv_ordinal": PARENT_ATV_HIGH_WATERMARK + 1,
            "release_5_3_new_family_first_atf_ordinal": PARENT_ATF_HIGH_WATERMARK
            + 1,
        }
    )
    registry = seal(
        {
            "schema_version": "awesome-theorems/claim-id-registry/5.3",
            "artifact": "Claim_ID_Registry.json",
            "release": RELEASE,
            "parent_registry_authority_sha256": parent_registry["authority_sha256"],
            "baseline_registry_authority_sha256": parent_registry[
                "baseline_registry_authority_sha256"
            ],
            "authoritative_inputs": copy.deepcopy(inputs),
            "allocation_policy": allocation_policy,
            "namespace_high_watermarks": {
                "ATF": LAST_ATF_ORDINAL,
                "ATO": LAST_ATV_ORDINAL,
                "ATS": LAST_ATV_ORDINAL,
                "ATV": LAST_ATV_ORDINAL,
            },
            "families": copy.deepcopy(parent_registry["families"]) + families,
            "senses": copy.deepcopy(parent_registry["senses"]) + senses,
            "variants": copy.deepcopy(parent_registry["variants"]) + variants,
            "legacy_aliases": copy.deepcopy(parent_registry.get("legacy_aliases", [])),
            "redirects": copy.deepcopy(parent_registry.get("redirects", [])),
            "splits": copy.deepcopy(parent_registry.get("splits", [])),
            "family_membership_extensions": copy.deepcopy(
                parent_registry.get("family_membership_extensions", [])
            ),
            "counts": {
                "families": len(parent_registry["families"]) + NEW_ROWS,
                "senses": len(parent_registry["senses"]) + NEW_ROWS,
                "variants": len(parent_registry["variants"]) + NEW_ROWS,
                "stage4_variants": parent_registry["counts"]["stage4_variants"],
                "stage5_additions": parent_registry["counts"]["stage5_additions"]
                + NEW_ROWS,
                "legacy_aliases": len(parent_registry.get("legacy_aliases", [])),
                "redirects": len(parent_registry.get("redirects", [])),
                "splits": len(parent_registry.get("splits", [])),
            },
        }
    )

    parent_stage = parent["Stage5_Claim_ID_Registry.json"]
    stage_additions = [
        {
            "ordinal": ordinal(str(row["variant_id"])),
            "variant_id": row["variant_id"],
            "predecessor_stage_claim_id": None,
            "stage_claim_id": row["stage_claim_id"],
            "lifecycle": "current",
        }
        for row in new_rows
    ]
    stage = seal(
        {
            "schema_version": "awesome-theorems/stage5-claim-id-registry/5.3",
            "artifact": "Stage5_Claim_ID_Registry.json",
            "release": RELEASE,
            "authoritative_inputs": copy.deepcopy(inputs),
            "numbering_policy": copy.deepcopy(parent_stage["numbering_policy"]),
            "counts": {
                "mappings": len(parent_stage["mappings"]) + len(stage_additions)
            },
            "mappings": copy.deepcopy(parent_stage["mappings"]) + stage_additions,
        }
    )

    parent_migration = parent["Migration_v4_to_v5.json"]
    migration_additions = []
    for row in new_rows:
        item_ordinal = ordinal(str(row["variant_id"]))
        migration_additions.append(
            {
                "ordinal": item_ordinal,
                "variant_id": row["variant_id"],
                "v4_variant_id": None,
                "s4_claim_id": None,
                "stage_claim_id": row["stage_claim_id"],
                "migration_action": "new_stage5_allocation",
                "predecessor_record_sha256": None,
                "current_resolution": {
                    "kind": "current",
                    "terminal_atv_ids": [row["variant_id"]],
                    "terminal_s5_ids": [row["stage_claim_id"]],
                    "default_child": None,
                    "evidence_inherited": False,
                },
            }
        )
    migration = seal(
        {
            "schema_version": "awesome-theorems/migration-v4-to-v5/5.3",
            "artifact": "Migration_v4_to_v5.json",
            "release": RELEASE,
            "authoritative_inputs": copy.deepcopy(inputs),
            "v4_import_receipt": copy.deepcopy(parent_migration["v4_import_receipt"]),
            "counts": {
                "historical_bindings": parent_migration["counts"][
                    "historical_bindings"
                ],
                "new_allocations": parent_migration["counts"]["new_allocations"]
                + NEW_ROWS,
                "migrations": len(parent_migration["migrations"])
                + len(migration_additions),
            },
            "migrations": copy.deepcopy(parent_migration["migrations"])
            + migration_additions,
        }
    )

    def projection(name: str, predicate: Any) -> dict[str, Any]:
        records = [row for row in all_rows if predicate(row)]
        return seal(
            {
                "schema_version": "awesome-theorems/stage5-query-projection/5.3",
                "artifact": name,
                "release": RELEASE,
                "authoritative_inputs": copy.deepcopy(inputs),
                "query": "pure predicate over Claim_Catalog.json; records copied byte-semantically",
                "stage_claim_ids": [row["stage_claim_id"] for row in records],
                "counts": {"records": len(records)},
                "records": records,
            }
        )

    parent_strict = parent["Strict_Conjecture_Ledger.json"]
    strict = seal(
        {
            "schema_version": "awesome-theorems/stage5-strict-conjecture-ledger/5.3",
            "release": RELEASE,
            "parent_release_root_sha256": PARENT_ROOT,
            "parent_strict_ledger_file_sha256": sha256_bytes(
                encoded_document(parent_strict)
            ),
            "parent_strict_ledger_authority_sha256": parent_strict[
                "authority_sha256"
            ],
            "strict_credits": copy.deepcopy(parent_strict["strict_credits"]),
            "credit_corrections": copy.deepcopy(parent_strict["credit_corrections"]),
            "counts": copy.deepcopy(parent_strict["counts"]),
            "set_digests": copy.deepcopy(parent_strict["set_digests"]),
        }
    )
    require(
        len(strict["strict_credits"]) == 1_000
        and len(strict["credit_corrections"]) == 1
        and strict["set_digests"]["effective_s5_id_set_sha256"]
        == set_digest(str(row["stage_claim_id"]) for row in strict["strict_credits"])
        and strict["set_digests"]["effective_variant_id_set_sha256"]
        == set_digest(str(row["variant_id"]) for row in strict["strict_credits"]),
        "inherited strict-credit set is not exactly 1,000 plus one correction",
    )

    artifacts = {
        "Claim_Catalog.json": catalog,
        "Claim_ID_Registry.json": registry,
        "Stage5_Claim_ID_Registry.json": stage,
        "Migration_v4_to_v5.json": migration,
        "Theorem_List.json": projection("Theorem_List.json", theorem_predicate),
        "Open_Claim_List.json": projection("Open_Claim_List.json", open_predicate),
        "Coverage_Ledger.json": expected_coverage(
            parent["Coverage_Ledger.json"], curation, new_rows, inputs
        ),
        "Strict_Conjecture_Ledger.json": strict,
    }
    require(
        len(artifacts["Theorem_List.json"]["records"]) == 2_000
        and len(artifacts["Open_Claim_List.json"]["records"]) == 1_600,
        "independent query projections have wrong theorem/open counts",
    )
    return artifacts


def expected_manifest(
    artifacts: Mapping[str, Mapping[str, Any]],
    inputs: Mapping[str, Any],
    curation: Mapping[str, Any],
) -> tuple[dict[str, Any], dict[str, bytes], str]:
    payloads = {name: encoded_document(artifacts[name]) for name in RELEASE_FILES}
    inventory = [
        {
            "path": name,
            "sha256": sha256_bytes(payloads[name]),
            "size_bytes": len(payloads[name]),
            "row_count": primary_row_count(artifacts[name]),
        }
        for name in sorted(RELEASE_FILES)
    ]
    root = release_root(inventory)
    strict = artifacts["Strict_Conjecture_Ledger.json"]
    selected = curation["set_digests"]
    manifest = seal(
        {
            "schema_version": "awesome-theorems/stage5-release-manifest/5.3",
            "release": RELEASE,
            "parent_release": PARENT_RELEASE,
            "parent_release_root_sha256": PARENT_ROOT,
            "release_root_sha256": root,
            "authoritative_inputs": copy.deepcopy(inputs),
            "accepted_set_digests": {
                "source_record_id_set_sha256": selected[
                    "selected_source_record_id_set_sha256"
                ],
                "declaration_set_sha256": selected[
                    "selected_declaration_set_sha256"
                ],
                "formal_type_sha256_set_sha256": selected[
                    "selected_formal_type_sha256_set_sha256"
                ],
                "semantic_key_set_sha256": selected[
                    "selected_semantic_key_set_sha256"
                ],
                "variant_id_set_sha256": selected[
                    "selected_variant_id_set_sha256"
                ],
                "s5_id_set_sha256": selected["selected_s5_id_set_sha256"],
            },
            "strict_credit_binding": {
                "path": "Strict_Conjecture_Ledger.json",
                "file_sha256": sha256_bytes(payloads["Strict_Conjecture_Ledger.json"]),
                "authority_sha256": strict["authority_sha256"],
                "effective_s5_id_set_sha256": strict["set_digests"][
                    "effective_s5_id_set_sha256"
                ],
                "effective_variant_id_set_sha256": strict["set_digests"][
                    "effective_variant_id_set_sha256"
                ],
            },
            "artifacts": inventory,
            "counts": {
                "non_manifest_artifacts": 8,
                "catalog_records": 3_600,
                "origin_theorems": 500,
                "origin_open_claims": 0,
                "cumulative_theorems": 2_000,
                "cumulative_open_claims": 1_600,
                "effective_strict_conjecture_credits": 1_000,
            },
        }
    )
    payloads[MANIFEST_NAME] = encoded_document(manifest)
    return manifest, payloads, root


def validate_new_rows_schema(
    rows: Sequence[Mapping[str, Any]], schema: Mapping[str, Any]
) -> None:
    require(jsonschema is not None, "the independent checker requires jsonschema")
    try:
        validator_type = jsonschema.validators.validator_for(schema)
        validator_type.check_schema(schema)
        validator = validator_type(schema)
    except Exception as error:  # pragma: no cover - dependency boundary
        raise CheckFailure(f"cannot initialize the 5.3 record schema: {error}") from error
    for index, row in enumerate(rows, start=1):
        errors = sorted(
            validator.iter_errors(row),
            key=lambda error: tuple(str(part) for part in error.absolute_path),
        )
        if errors:
            first = errors[0]
            location = ".".join(str(part) for part in first.absolute_path) or "$"
            raise CheckFailure(
                f"origin-5.3 row {index} fails schema at {location}: {first.message}"
            )


def verify_release(checker: Checker) -> str:
    parent, parent_payloads = load_parent_release(checker)
    contract, schema, registry, receipt, curation = verify_authorities(
        checker, parent, parent_payloads
    )
    require(
        tuple(contract.get("release_layout", {}).get("non_manifest_artifacts", []))
        == RELEASE_FILES,
        "contract release artifact set/order drifted",
    )
    release_counts = contract.get("release_counts")
    require(
        isinstance(release_counts, dict)
        and release_counts.get("origin_5_3_records") == NEW_ROWS
        and release_counts.get("origin_5_3_theorems") == NEW_ROWS
        and release_counts.get("origin_5_3_open_claims") == 0
        and release_counts.get("cumulative_catalog_records") == 3_600
        and release_counts.get("cumulative_theorem_records") == 2_000
        and release_counts.get("cumulative_open_claim_records") == 1_600
        and release_counts.get("effective_cumulative_strict_conjecture_credits")
        == 1_000
        and release_counts.get("cumulative_open_problem_records") == 599,
        "contract exact release counts drifted",
    )

    _source, source_rows, _source_ids, _source_hashes = load_mathlib_source(checker)
    accepted = verify_curation(
        curation,
        registry,
        receipt,
        source_rows,
        parent["Claim_Catalog.json"]["records"],
    )
    inputs = expected_authoritative_inputs(
        checker,
        contract,
        schema,
        registry,
        receipt,
        curation,
        parent,
        parent_payloads,
    )
    new_rows = [
        expected_claim_row(
            checker,
            ledger_row,
            source_row,
            schema,
            parent["Claim_ID_Registry.json"]["authority_sha256"],
            str(curation["authority_sha256"]),
            CURATION_FILE_SHA256,
            sha256_bytes(parent_payloads["Claim_Catalog.json"]),
        )
        for ledger_row, source_row in accepted
    ]
    require(len(new_rows) == NEW_ROWS, "independent catalog rebuild is not 500 rows")
    validate_new_rows_schema(new_rows, schema)

    expected_artifacts = expected_release_artifacts(inputs, parent, curation, new_rows)
    expected_release_manifest, expected_payloads, expected_root = expected_manifest(
        expected_artifacts, inputs, curation
    )
    release, release_payloads = load_release_documents(checker, RELEASE_DIR)
    observed_root = verify_manifest_inventory(
        release[MANIFEST_NAME], release, release_payloads, "release 5.3"
    )
    require(observed_root == expected_root, "5.3 manifest root differs from independent rebuild")
    for name in RELEASE_FILES:
        require(
            release[name] == expected_artifacts[name],
            f"5.3 artifact differs from independent rebuild: {name}",
        )
        require(
            release_payloads[name] == expected_payloads[name],
            f"5.3 artifact bytes differ from independent rebuild: {name}",
        )
    require(
        release[MANIFEST_NAME] == expected_release_manifest
        and release_payloads[MANIFEST_NAME] == expected_payloads[MANIFEST_NAME],
        "5.3 release manifest differs from independent rebuild",
    )

    catalog_rows = release["Claim_Catalog.json"]["records"]
    require(
        catalog_rows[:PARENT_CATALOG_ROWS] == parent["Claim_Catalog.json"]["records"]
        and catalog_rows[PARENT_CATALOG_ROWS:] == new_rows,
        "5.3 catalog is not the exact immutable parent prefix plus 500 rows",
    )
    validate_new_rows_schema(catalog_rows[PARENT_CATALOG_ROWS:], schema)
    require(
        [row["variant_id"] for row in new_rows]
        == [f"ATV-{value:08d}" for value in range(6_585, 7_085)]
        and [row["stage_claim_id"] for row in new_rows]
        == [f"S5-CLM-{value:08d}" for value in range(6_585, 7_085)],
        "5.3 new ATV/S5 identities are not exactly 6585..7084",
    )
    require(
        sum(row.get("current_claim_kind") == "open_problem" for row in catalog_rows)
        == 599,
        "5.3 catalog open-problem count is not 599",
    )

    current, current_payload = checker.load_json(CURRENT_PATH)
    require(
        current_payload == encoded_document(current),
        "Current_Release.json is not canonical JSON plus LF",
    )
    verify_seal(current, str(CURRENT_PATH))
    expected_current = seal(
        {
            "schema_version": "awesome-theorems/stage5-current-release/5.3",
            "release": RELEASE,
            "release_root_sha256": expected_root,
            "manifest_sha256": sha256_bytes(expected_payloads[MANIFEST_NAME]),
            "manifest_path": f"releases/{RELEASE}/{MANIFEST_NAME}",
        }
    )
    require(current == expected_current, "Current_Release.json differs from sealed 5.3")

    checker.note(
        "source=1500; literal-theorem=1235; literal-lemma=265; "
        "unique-theorem=1231; selected=180+320=500"
    )
    checker.note(
        "catalog=3600; theorem=2000; open=1600; open-problem=599; strict=1000+1"
    )
    checker.note(
        "all statement/rights/proof/allocation/content/source/semantic redundant "
        "hash payloads were independently reconstructed; the sealed authorities "
        "require recomputation but do not enumerate every exact payload formula"
    )
    return expected_root


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="repository root containing Docs/catalog/v5",
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    checker = Checker(args.root)
    try:
        root = verify_release(checker)
    except (
        CheckFailure,
        OSError,
        ValueError,
        TypeError,
        KeyError,
        IndexError,
    ) as error:
        print(f"FAIL check_math_catalog_v5_3: {error}", file=sys.stderr)
        return 1
    print("PASS check_math_catalog_v5_3")
    for note in checker.notes:
        print(f"NOTE {note}")
    print(f"NOTE release_root={root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
