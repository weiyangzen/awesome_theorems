#!/usr/bin/env python3
"""Independent, stdlib-only verifier for the Stage4 claim-catalog supplement.

This checker deliberately does not import the Stage4 generator.  It derives the
frozen baseline, candidate, proposal, numbering, migration, and projection sets
from their primary inputs and compares them with the generated Stage4 surfaces.

``--require-complete`` means that the *frozen Stage4 supplement* (154 review
keys and 623 v2 repair proposals) is closed.  It does not claim that the 3,338
inherited machine-triage variants have received full semantic review.
"""

from __future__ import annotations

import argparse
from copy import deepcopy
import fcntl
import hashlib
import json
import os
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Iterable, Iterator, Mapping, Sequence
from urllib.parse import urlparse


ATO_RE = re.compile(r"^ATO-([0-9]{8})$")
ATV_RE = re.compile(r"^ATV-([0-9]{8})$")
S4_RE = re.compile(r"^S4-CLM-([0-9]{8})$")
THM_RE = re.compile(r"^THM-[MPC]-[0-9]{4}$")
CANDIDATE_RE = re.compile(r"^(?:missing\.(?:math|physics|cs)|collision\.)[a-z0-9_.-]+$")
SHA256_RE = re.compile(r"^(?:sha256:)?([0-9a-f]{64})$")
REDIRECT_RE = re.compile(r"^REDIRECT-[0-9A-F]{24}$")
SPLIT_RE = re.compile(r"^SPLIT-[0-9A-F]{24}$")

# These lifecycle rows were already sealed in the accepted Stage4 allocator
# state before the final append-only review.  Their row digests are an
# independent historical anchor: later releases may append lifecycle rows,
# but cannot silently delete or rewrite any row listed here merely by editing
# the current curation manifest.  The digest covers every field in the row.
SEALED_LIFECYCLE_ROW_SHA256: Mapping[str, str] = {
    "REDIRECT-B30E3CD21DD7E2602BD3E0E5": "334d801f193c331eedabbc374878aec66af319d9e8f93a344df7a39d9226ba9e",
    "REDIRECT-4504297B39A7A25BB4C020E5": "a0e67884e808a3573c39928660ede2cad9b4454f4f225bab162ff992b6171724",
    "REDIRECT-FB27B04079086231E4E4C53F": "7a1cd1e6c1566d77d4a5855133c09b8da485b6993b676e04e5e6d19a84cc71a8",
    "REDIRECT-D438734A52F72EFBF4FB42A2": "bf9769eececdd183492ed9b33b332a320b35d2c0d2e0a477f2c3bbd65e10ddf5",
    "REDIRECT-6032E22033E288237E493FF6": "346dce6252246ec29ab90d9df72377fe493527a094d7a8609e1c6eb2710c3a7d",
    "REDIRECT-BC3F80E148AD88B187EEDD2A": "32ed4be34aeaea2011cb3fe30f4a4e13e4a7496f1e8f1ddde8928dbfec23d19e",
    "REDIRECT-167829F9FD68CED39348DC5D": "f83f58cae5a9cbc9feeb7e9df1f1466f20c05555f24ed7b9520a8c582cefc1fa",
    "REDIRECT-DCA5F275CC316F8A763348F5": "28cb48dd74106a448ab4c453f321945a00d62e14e51864af48b4a8dcf4467fd4",
    "SPLIT-B40A7EFEDCFD4C6306D5D857": "01bfcb18ffcf85814538c1a87ed0027d6e8d866c7a93704b1d2a28753b24f1a0",
    "SPLIT-825096F3118A866AA336504F": "026b21f328eea65630c81ce007afb57b79257230464174a4f71d44883365688a",
    "SPLIT-C8D4B0B44F90920D7DA33479": "bb4909fc092216c97d1213ba942173e00c75f20d129c3ef6f042250e58f2fe96",
    "SPLIT-EEC5BA3081476410928A5D99": "495aaca0cb5bdda18a5cac95261cefe9cef9ca087b795d0f75b6a1bf4bbdaf3f",
}

REGRESSION_KEYS = {
    "regression.math.thm_m_0323",
    "regression.math.thm_m_0324",
    "regression.math.lln_assumption_family",
    "regression.math.clt_assumption_family",
    "regression.math.euler_conjecture_counterexample",
    "regression.math.dinitz_galvin",
    "regression.math.theorem_proof_event_formal_artifact",
    "regression.math.optional_stopping_aliasing",
    "regression.math.marcus_spielman_srivastava_distinct_claims",
    "regression.physics.euler_equation_homonyms",
    "regression.physics.feynman_rules_homonyms",
    "regression.physics.dispersion_homonyms",
    "regression.physics.area_law_homonyms",
    "regression.physics.convention_homonyms",
    "regression.physics.zeno_anti_zeno",
    "regression.physics.cosmic_censorship",
    "regression.physics.cmb",
    "regression.physics.nanograv",
    "regression.physics.hubble_inference",
    "regression.physics.quark_mass_scheme",
    "regression.cs.rice",
    "regression.cs.ntime_hierarchy",
    "regression.cs.lfkn",
    "regression.cs.max_3sat",
    "regression.cs.owf_converse",
    "regression.cs.fiat_shamir",
    "regression.cs.compiler_correctness",
    "regression.cs.flp",
    "regression.cs.paxos",
    "regression.cs.hhl",
    "regression.cs.channel_coding",
    "regression.cs.hamming",
    "regression.cs.huffman",
    "regression.cs.bwt",
    "regression.cs.folded_cs_atos",
    "regression.cross_domain.wedderburn_artin_scope_variants",
    "regression.cross_domain.hausdorff_young",
    "regression.cross_domain.caffarelli_kohn_nirenberg_distinct_claims",
    "regression.cross_domain.heat_maximum_principles",
    "regression.cross_domain.nekhoroshev",
    "regression.cross_domain.maxwell_differential_integral_forms",
    "regression.cross_domain.model_specific_adequacy",
    "regression.hard_negative.konig_homonyms",
    "regression.hard_negative.liouville_homonyms",
    "regression.hard_negative.uniqueness_homonyms",
    "regression.hard_negative.pcp_homonyms",
}

THEOREM_KINDS = {
    "theorem",
    "lemma",
    "result",
    "complexity_result",
    "undecidability_result",
    "no_go_theorem",
    "reconstruction_theorem",
    "representation_theorem",
    "structure_theorem",
    "sum_rule",
    "model_consequence",
    "identity",
    "inequality",
    "law",
}
THEOREM_SUBTYPES = {
    "no_go_theorem",
    "representation_theorem",
    "structure_theorem",
    "sum_rule",
    "reconstruction_theorem",
    "model_consequence",
}
OPEN_KINDS = {"conjecture", "hypothesis", "open_problem", "assumption"}
OPEN_STATUS_WORDS = {
    "open",
    "unresolved",
    "independent",
    "partial",
    "partially_resolved",
    "disputed",
    "conditional_open",
}

STATUS_BUCKETS = {
    "proved": "proved",
    "proven": "proved",
    "established": "proved",
    "true": "proved",
    "resolved_proved": "proved",
    "confirmed": "proved",
    "open": "open",
    "unresolved": "open",
    "open_problem": "open",
    "refuted": "refuted",
    "disproved": "refuted",
    "false": "refuted",
    "counterexample": "refuted",
    "independent": "independent",
    "independence": "independent",
    "partial": "partial",
    "partially_resolved": "partial",
    "disputed": "disputed",
    "contested": "disputed",
    "conditional": "conditional",
    "conditional_open": "conditional",
    "conditional_assumption": "conditional",
    "assumption": "conditional",
    "unknown": "unknown",
    "unreviewed": "unknown",
    "missing": "unknown",
    "none": "unknown",
    "": "unknown",
}

V2_SOURCE = Path("Docs/catalog/Source_Records_v2.json")
V2_REGISTRY = Path("Docs/catalog/Claim_ID_Registry_v2.json")
V2_CATALOG = Path("Docs/catalog/Claim_Catalog_v2.json")
V2_CANDIDATES = Path("Docs/catalog/Coverage_Candidates_v2.json")
V3_AUDIT = Path("Docs/reviews/Stage3_v3_18_Agent_Critical_Audit_2026-08-10.md")
V4_MANIFEST = Path("Docs/catalog/v4/Stage4_Curation_Manifest_v4.json")
REPAIR_INPUTS = (
    Path("Docs/catalog/repairs/Mathematics_v2.json"),
    Path("Docs/catalog/repairs/Physics_v2.json"),
    Path("Docs/catalog/repairs/Computer_Science_v2.json"),
)
LEGACY_SOURCE_INPUTS = (
    Path("Docs/researches/math_theorems.md"),
    Path("Docs/researches/physics_theorems.md"),
    Path("Docs/researches/cs_theorems.md"),
)

OUTPUT_CANDIDATES: Mapping[str, tuple[Path, ...]] = {
    "source_records": (Path("Docs/catalog/v4/Source_Records_v4.json"),),
    "id_registry": (Path("Docs/catalog/v4/Claim_ID_Registry_v4.json"),),
    "numbering": (Path("Docs/catalog/v4/Stage4_Claim_ID_Registry_v4.json"),),
    "catalog": (
        Path("Docs/catalog/v4/Claim_Catalog_v4.json"),
        Path("Docs/catalog/v4/Stage4_Claim_Catalog_v4.json"),
    ),
    "migration": (
        Path("Docs/catalog/v4/Claim_ID_Migration_v2_to_v4.json"),
        Path("Docs/catalog/v4/Claim_ID_Migration_v4.json"),
        Path("Docs/catalog/v4/Stage4_Claim_ID_Migration_v4.json"),
    ),
    "candidate_dispositions": (Path("Docs/catalog/v4/Candidate_Dispositions_v4.json"),),
    "proposal_dispositions": (
        Path("Docs/catalog/v4/Repair_Proposal_Dispositions_v4.json"),
    ),
    "theorem_json": (
        Path("Docs/catalog/v4/Theorem_List_v4.json"),
        Path("Docs/catalog/v4/Stage4_Theorem_List_v4.json"),
    ),
    "theorem_md": (
        Path("Docs/catalog/v4/Theorem_List_v4.md"),
        Path("Docs/catalog/v4/Stage4_Theorem_List_v4.md"),
    ),
    "open_json": (
        Path("Docs/catalog/v4/Conjecture_Hypothesis_Open_List_v4.json"),
        Path("Docs/catalog/v4/Stage4_Conjecture_Hypothesis_Open_List_v4.json"),
    ),
    "open_md": (
        Path("Docs/catalog/v4/Conjecture_Hypothesis_Open_List_v4.md"),
        Path("Docs/catalog/v4/Stage4_Conjecture_Hypothesis_Open_List_v4.md"),
    ),
    "status_json": (Path("Docs/catalog/v4/Status_Index_v4.json"),),
    "status_md": (Path("Docs/catalog/v4/Status_Index_v4.md"),),
}

_CANONICAL_COMMON_KEYS = frozenset(
    {
        "schema_version",
        "artifact",
        "generated_by",
        "authoritative_inputs",
        "authoritative_inputs_sha256",
        "counts",
        "authority_sha256",
    }
)
CANONICAL_ARTIFACT_KEYS: Mapping[str, frozenset[str]] = {
    "Source_Records_v4.json": _CANONICAL_COMMON_KEYS
    | {
        "baseline_authority_sha256",
        "baseline_occurrence_ids",
        "folded_occurrence_ids",
        "identity_policy",
        "namespace_high_watermark",
        "records",
    },
    "Claim_ID_Registry_v4.json": _CANONICAL_COMMON_KEYS
    | {
        "allocation_policy",
        "baseline_registry_authority_sha256",
        "families",
        "family_membership_extensions",
        "legacy_aliases",
        "namespace_high_watermarks",
        "redirects",
        "senses",
        "source_records_authority_sha256",
        "splits",
        "variants",
    },
    "Stage4_Claim_ID_Registry_v4.json": _CANONICAL_COMMON_KEYS
    | {"mappings", "numbering_policy"},
    "Claim_ID_Migration_v2_to_v4.json": _CANONICAL_COMMON_KEYS
    | {
        "folded_occurrence_ids",
        "folded_variant_ids",
        "legacy_alias_migrations",
        "migrations",
        "policy",
    },
    "Candidate_Dispositions_v4.json": _CANONICAL_COMMON_KEYS
    | {"completion_boundary", "dispositions"},
    "Repair_Proposal_Dispositions_v4.json": _CANONICAL_COMMON_KEYS
    | {"dispositions", "policy"},
    "Claim_Catalog_v4.json": _CANONICAL_COMMON_KEYS
    | {"records", "sources", "trust_boundary"},
    "Theorem_List_v4.json": _CANONICAL_COMMON_KEYS
    | {"projection_policy", "records", "stage_claim_ids"},
    "Conjecture_Hypothesis_Open_List_v4.json": _CANONICAL_COMMON_KEYS
    | {"projection_policy", "records", "stage_claim_ids"},
    "Status_Index_v4.json": _CANONICAL_COMMON_KEYS
    | {"projection_policy", "records", "stage_claim_ids"},
}


class CheckFailure(RuntimeError):
    """Raised only for input errors that make further checking impossible."""


class Checker:
    def __init__(self, root: Path, require_complete: bool) -> None:
        self.root = root.resolve()
        self.require_complete = require_complete
        self.errors: list[str] = []
        self.notes: list[str] = []

    def fail(self, message: str) -> None:
        self.errors.append(message)

    def note(self, message: str) -> None:
        self.notes.append(message)

    def path(self, relative: Path | str) -> Path:
        return self.root / relative

    def load_json(self, relative: Path | str, *, required: bool = True) -> Any:
        path = self.path(relative)
        if not path.is_file():
            if required:
                self.fail(f"missing JSON artifact: {path.relative_to(self.root)}")
            return None
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError) as exc:
            self.fail(f"invalid JSON {path.relative_to(self.root)}: {exc}")
            return None

    def load_text(self, relative: Path | str, *, required: bool = True) -> str:
        path = self.path(relative)
        if not path.is_file():
            if required:
                self.fail(f"missing text artifact: {path.relative_to(self.root)}")
            return ""
        try:
            return path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            self.fail(f"unreadable text {path.relative_to(self.root)}: {exc}")
            return ""


def canonical_json_bytes(value: Any) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def authority_digest(namespace: str, document: Mapping[str, Any]) -> str:
    body = {key: value for key, value in document.items() if key != "authority_sha256"}
    return sha256_bytes(namespace.encode("utf-8") + b"\0" + canonical_json_bytes(body))


def plain_authority_digest(document: Mapping[str, Any]) -> str:
    body = {key: value for key, value in document.items() if key != "authority_sha256"}
    return sha256_bytes(canonical_json_bytes(body))


def as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def as_dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def payload_dict(document: Mapping[str, Any]) -> dict[str, Any]:
    """Return a legacy fixture envelope, never a canonical artifact envelope.

    Canonical Stage4 artifacts are specified as top-level objects.  Treating
    an injected ``payload`` object as higher priority would let a resealed
    artifact present one body to authority/envelope checks and another body to
    semantic checks.
    """

    if document.get("artifact") in CANONICAL_ARTIFACT_KEYS:
        return dict(document)
    payload = document.get("payload")
    return payload if isinstance(payload, dict) else dict(document)


def check_canonical_artifact_shape(
    checker: Checker, label: str, document: Mapping[str, Any]
) -> None:
    artifact = document.get("artifact")
    if not isinstance(artifact, str) or artifact not in CANONICAL_ARTIFACT_KEYS:
        checker.fail(f"{label} does not identify a supported canonical Stage4 artifact")
        return
    expected = CANONICAL_ARTIFACT_KEYS[artifact]
    observed = set(document)
    missing = sorted(expected - observed)
    extra = sorted(observed - expected)
    if missing or extra:
        checker.fail(
            f"{label} canonical top-level shape differs: "
            f"missing={missing!r}, extra={extra!r}"
        )


def unique_strings(
    checker: Checker, values: Iterable[Any], label: str, pattern: re.Pattern[str] | None = None
) -> set[str]:
    strings: list[str] = []
    for value in values:
        if not isinstance(value, str):
            checker.fail(f"{label} contains a non-string value: {value!r}")
            continue
        if pattern is not None and pattern.fullmatch(value) is None:
            checker.fail(f"{label} contains malformed ID: {value!r}")
            continue
        strings.append(value)
    duplicates = sorted(key for key, count in Counter(strings).items() if count != 1)
    if duplicates:
        checker.fail(f"{label} contains duplicate IDs: {duplicates[:8]!r}")
    return set(strings)


def exact_set(checker: Checker, observed: set[str], expected: set[str], label: str) -> None:
    missing = sorted(expected - observed)
    extra = sorted(observed - expected)
    if missing or extra:
        checker.fail(
            f"{label} exact-set mismatch: missing={missing[:8]!r} ({len(missing)}), "
            f"extra={extra[:8]!r} ({len(extra)})"
        )


def select_output(checker: Checker, name: str) -> Path | None:
    matches = [candidate for candidate in OUTPUT_CANDIDATES[name] if checker.path(candidate).is_file()]
    if len(matches) != 1:
        if not matches:
            checker.fail(
                f"missing generated {name}; expected one of "
                + ", ".join(str(path) for path in OUTPUT_CANDIDATES[name])
            )
        else:
            checker.fail(f"multiple generated {name} authorities: {[str(path) for path in matches]!r}")
        return None
    return matches[0]


def check_v2_authorities(checker: Checker, source: dict[str, Any], registry: dict[str, Any]) -> None:
    contracts = (
        (source, "awesome-theorems/source-records-authority/v2", str(V2_SOURCE)),
        (registry, "awesome-theorems/claim-id-registry-authority/v2", str(V2_REGISTRY)),
    )
    for document, namespace, label in contracts:
        observed = document.get("authority_sha256")
        expected = authority_digest(namespace, document)
        if observed != expected:
            checker.fail(f"stale v2 authority_sha256 in {label}")


def derive_v2_sets(
    checker: Checker, source: dict[str, Any], registry: dict[str, Any], catalog: dict[str, Any]
) -> tuple[set[str], set[str], dict[str, str], set[str]]:
    ato_ids = unique_strings(
        checker,
        (row.get("occurrence_id") for row in as_list(source.get("records")) if isinstance(row, dict)),
        "v2 ATO records",
        ATO_RE,
    )
    atv_ids = unique_strings(
        checker,
        (row.get("variant_id") for row in as_list(registry.get("variants")) if isinstance(row, dict)),
        "v2 ATV registry",
        ATV_RE,
    )
    aliases: dict[str, str] = {}
    alias_rows = as_list(registry.get("legacy_aliases"))
    for row in alias_rows:
        if not isinstance(row, dict):
            checker.fail("v2 legacy_aliases contains a non-object")
            continue
        alias = row.get("alias_id")
        target = row.get("target_variant_id")
        if not isinstance(alias, str) or THM_RE.fullmatch(alias) is None:
            checker.fail(f"malformed v2 legacy alias: {alias!r}")
            continue
        if not isinstance(target, str) or ATV_RE.fullmatch(target) is None:
            checker.fail(f"malformed v2 legacy alias target for {alias}: {target!r}")
            continue
        if alias in aliases:
            checker.fail(f"duplicate v2 legacy alias: {alias}")
        aliases[alias] = target
    target_occurrences = {
        row.get("target_occurrence_id")
        for row in alias_rows
        if isinstance(row, dict) and isinstance(row.get("target_occurrence_id"), str)
    }
    folded = ato_ids - target_occurrences

    if len(ato_ids) != 3338:
        checker.fail(f"v2 ATO denominator is {len(ato_ids)}, expected 3338")
    if len(atv_ids) != 3338:
        checker.fail(f"v2 ATV denominator is {len(atv_ids)}, expected 3338")
    if len(aliases) != 3262:
        checker.fail(f"v2 alias denominator is {len(aliases)}, expected 3262")
    if len(folded) != 76:
        checker.fail(f"v2 folded occurrence denominator is {len(folded)}, expected 76")
    expected_catalog_atv = {
        row.get("record_id")
        for row in as_list(catalog.get("records"))
        if isinstance(row, dict) and row.get("record_type") == "ATV"
    }
    if expected_catalog_atv != atv_ids:
        checker.fail("v2 catalog ATV set differs from the v2 registry ATV set")
    return ato_ids, atv_ids, aliases, folded


def derive_candidate_keys(
    checker: Checker, coverage: dict[str, Any], audit_text: str
) -> tuple[set[str], set[str], set[str]]:
    legacy_rows = as_list(coverage.get("missing_candidates")) + as_list(
        coverage.get("present_collisions")
    )
    legacy = unique_strings(
        checker,
        (row.get("candidate_key") for row in legacy_rows if isinstance(row, dict)),
        "v2 candidate inventory",
        CANDIDATE_RE,
    )
    delta_list = re.findall(
        r"(?<![A-Za-z0-9_.-])missing\.(?:math|physics|cs)\.[a-z0-9_]+", audit_text
    )
    delta = set(delta_list)
    if len(legacy) != 98:
        checker.fail(f"v2 candidate denominator is {len(legacy)}, expected 98")
    if len(delta) != 56:
        checker.fail(f"Stage3 audit candidate delta is {len(delta)}, expected 56")
    overlap = legacy & delta
    if overlap:
        checker.fail(f"v2 and Stage3 delta candidate sets overlap: {sorted(overlap)!r}")
    return legacy, delta, legacy | delta


def proposal_rows() -> tuple[tuple[str, Path, str], ...]:
    return (
        ("mathematics", Path("Docs/catalog/repairs/Mathematics_v2.json"), "repairs"),
        ("physics", Path("Docs/catalog/repairs/Physics_v2.json"), "repairs"),
        ("computer_science", Path("Docs/catalog/repairs/Computer_Science_v2.json"), "records"),
    )


def derive_proposals(
    checker: Checker,
) -> tuple[set[tuple[str, str]], list[dict[str, Any]]]:
    result: set[tuple[str, str]] = set()
    source_rows: list[dict[str, Any]] = []
    expected_counts = {"mathematics": 120, "physics": 105, "computer_science": 398}
    for domain, path, field in proposal_rows():
        document = checker.load_json(path)
        rows = as_list(as_dict(document).get(field))
        if len(rows) != expected_counts[domain]:
            checker.fail(
                f"{path} proposal denominator is {len(rows)}, expected {expected_counts[domain]}"
            )
        for index, row in enumerate(rows, start=1):
            legacy_id = row.get("legacy_id") if isinstance(row, dict) else None
            key = (domain, legacy_id)
            if not isinstance(legacy_id, str) or THM_RE.fullmatch(legacy_id) is None:
                checker.fail(f"malformed {domain} proposal legacy_id: {legacy_id!r}")
                continue
            if key in result:
                checker.fail(f"duplicate v2 proposal key: {key!r}")
            result.add(key)
            if isinstance(row, dict):
                source_rows.append(
                    {
                        "domain": domain,
                        "source_path": str(path),
                        "source_index": index,
                        "legacy_id": legacy_id,
                        "proposal": deepcopy(row),
                    }
                )
    if len(result) != 623:
        checker.fail(f"v2 proposal union is {len(result)}, expected 623")
    return result, source_rows


def load_v4_fragments(checker: Checker, manifest: dict[str, Any]) -> list[tuple[Path, dict[str, Any]]]:
    declared = as_list(manifest.get("fragments"))
    declared_strings = [value for value in declared if isinstance(value, str)]
    required = {
        "Docs/catalog/v4/fragments/Mathematics_v4.json",
        "Docs/catalog/v4/fragments/Physics_v4.json",
        "Docs/catalog/v4/fragments/Computer_Science_v4.json",
        "Docs/catalog/v4/fragments/Cross_Domain_v4.json",
    }
    if len(declared_strings) != len(declared) or len(set(declared_strings)) != len(declared):
        checker.fail("Stage4 manifest fragment paths must be unique strings")
    missing_required = sorted(required - set(declared_strings))
    if missing_required:
        checker.fail(f"Stage4 manifest omits required curation fragments: {missing_required!r}")
    result: list[tuple[Path, dict[str, Any]]] = []
    for value in declared:
        if not isinstance(value, str):
            checker.fail(f"non-string fragment path: {value!r}")
            continue
        literal = Path(value)
        if literal.is_absolute() or ".." in literal.parts:
            checker.fail(f"Stage4 manifest fragment has unsafe path: {value!r}")
            continue
        resolved = safe_repo_path(checker, value, "Stage4 manifest fragment")
        if resolved is None:
            continue
        relative = resolved.relative_to(checker.root)
        document = checker.load_json(relative)
        if isinstance(document, dict):
            result.append((relative, document))
    return result


def merged_rows(
    manifest: dict[str, Any], fragments: Sequence[tuple[Path, dict[str, Any]]], field: str
) -> list[tuple[str, dict[str, Any]]]:
    result: list[tuple[str, dict[str, Any]]] = []
    for index, row in enumerate(as_list(manifest.get(field))):
        if isinstance(row, dict):
            result.append((f"{V4_MANIFEST}:{field}[{index}]", row))
    for path, fragment in fragments:
        for index, row in enumerate(as_list(fragment.get(field))):
            if isinstance(row, dict):
                result.append((f"{path}:{field}[{index}]", row))
    return result


def check_candidate_dispositions(
    checker: Checker,
    manifest: dict[str, Any],
    fragments: Sequence[tuple[Path, dict[str, Any]]],
    expected: set[str],
) -> None:
    rows = merged_rows(manifest, fragments, "dispositions")
    keys: list[str] = []
    unresolved_words = {"pending", "unreviewed", "unknown", "deferred", "blocked", "quarantine"}
    for label, row in rows:
        key = row.get("candidate_key")
        if not isinstance(key, str):
            checker.fail(f"{label} has no candidate_key")
            continue
        keys.append(key)
        if not isinstance(row.get("disposition"), str) or not row.get("disposition"):
            checker.fail(f"{label} has no disposition")
        if not as_list(row.get("source_refs")):
            checker.fail(f"{label} has no source_refs")
        if checker.require_complete and str(row.get("disposition", "")).casefold() in unresolved_words:
            checker.fail(f"{label} remains unresolved under --require-complete")
    duplicates = sorted(key for key, count in Counter(keys).items() if count != 1)
    if duplicates:
        checker.fail(f"Stage4 candidate dispositions contain duplicates: {duplicates[:8]!r}")
    inventory_keys = [key for key in keys if key in expected or CANDIDATE_RE.fullmatch(key)]
    observed = unique_strings(checker, inventory_keys, "Stage4 candidate dispositions")
    exact_set(checker, observed, expected, "Stage4 candidate dispositions")


def check_regression_fixtures(
    checker: Checker, fragments: Sequence[tuple[Path, dict[str, Any]]]
) -> None:
    rows: dict[str, dict[str, Any]] = {}
    for path, fragment in fragments:
        if path.name != "Regression_Fixtures_v4.json":
            continue
        for _pointer, row in iter_dicts(fragment):
            key = row.get("regression_key") or row.get("candidate_key") or row.get("fixture_key")
            if not isinstance(key, str) or not key.startswith("regression."):
                continue
            if key in rows and rows[key] != row:
                checker.fail(f"regression fixture {key!r} has conflicting definitions")
            rows[key] = row
    exact_set(checker, set(rows), REGRESSION_KEYS, "Stage4 regression fixture inventory")
    optional = rows.get("regression.math.optional_stopping_aliasing")
    if optional is not None:
        referenced = {
            value
            for _pointer, nested in iter_dicts(optional)
            for value in nested.values()
            if isinstance(value, str) and ATV_RE.fullmatch(value)
        }
        for _pointer, nested in iter_dicts(optional):
            for value in nested.values():
                if isinstance(value, list):
                    referenced.update(
                        item for item in value if isinstance(item, str) and ATV_RE.fullmatch(item)
                    )
        if "ATV-00001037" not in referenced:
            checker.fail(
                "optional-stopping regression fixture does not bind existing ATV-00001037"
            )


def domain_from_fragment(fragment: dict[str, Any]) -> str | None:
    value = fragment.get("domain")
    aliases = {
        "math": "mathematics",
        "mathematics": "mathematics",
        "physics": "physics",
        "cs": "computer_science",
        "computer_science": "computer_science",
    }
    return aliases.get(value) if isinstance(value, str) else None


def proposal_id(domain: str, legacy_id: str, index: int) -> str:
    prefix = {
        "mathematics": "M",
        "physics": "P",
        "computer_science": "C",
    }[domain]
    return f"RPR-{prefix}-{index:04d}-{legacy_id}"


def applied_repair_proposal_keys(
    checker: Checker,
    manifest: dict[str, Any],
    fragments: Sequence[tuple[Path, dict[str, Any]]],
) -> dict[str, list[str]]:
    applied: dict[str, list[str]] = {}
    for field in ("additions", "overlays"):
        for label, row in merged_rows(manifest, fragments, field):
            key = row.get("curation_key")
            if not isinstance(key, str):
                # Compact split overlay instructions are normalized to a
                # stable generated key, but cannot cite repair proposals in
                # their compact form.
                if as_list(row.get("repair_proposal_refs")):
                    checker.fail(f"{label} cites repairs without a curation_key")
                continue
            refs = row.get("repair_proposal_refs", [])
            if not isinstance(refs, list):
                checker.fail(f"{label}.repair_proposal_refs is not a list")
                continue
            if len(refs) != len(set(refs)) or not all(
                isinstance(ref, str) and ref for ref in refs
            ):
                checker.fail(f"{label}.repair_proposal_refs is malformed/duplicated")
                continue
            for ref in refs:
                applied.setdefault(ref, []).append(key)
    return {proposal: sorted(keys) for proposal, keys in applied.items()}


def expected_repair_disposition_rows(
    checker: Checker,
    proposal_sources: Sequence[dict[str, Any]],
    applied: Mapping[str, Sequence[str]],
) -> list[dict[str, Any]]:
    expected: list[dict[str, Any]] = []
    known_ids: set[str] = set()
    for source in proposal_sources:
        domain = source["domain"]
        legacy_id = source["legacy_id"]
        index = source["source_index"]
        identifier = proposal_id(domain, legacy_id, index)
        if identifier in known_ids:
            checker.fail(f"deterministic repair proposal ID is duplicated: {identifier}")
        known_ids.add(identifier)
        applied_keys = list(applied.get(identifier, ()))
        proposal = deepcopy(source["proposal"])
        expected.append(
            {
                "proposal_id": identifier,
                "domain": domain,
                "source_path": source["source_path"],
                "source_index": index,
                "legacy_id": legacy_id,
                "proposal_sha256": independent_stable_digest(
                    "awesome-theorems/stage4-repair-proposal/v4", proposal
                ),
                "proposal": proposal,
                "disposition": (
                    "applied_by_explicit_curation"
                    if applied_keys
                    else "proposal_only_preserved"
                ),
                "applied_by_curation_keys": applied_keys,
                "grants_truth_credit": False,
            }
        )
    unknown = sorted(set(applied) - known_ids)
    if unknown:
        checker.fail(f"curation cites unknown repair proposal IDs: {unknown[:8]!r}")
    return expected


def check_repair_proposal_dispositions(
    checker: Checker,
    document: dict[str, Any],
    manifest: dict[str, Any],
    fragments: Sequence[tuple[Path, dict[str, Any]]],
    proposal_sources: Sequence[dict[str, Any]],
) -> None:
    """Rebuild and compare every one of the 623 repair disposition rows."""

    applied = applied_repair_proposal_keys(checker, manifest, fragments)
    expected = expected_repair_disposition_rows(checker, proposal_sources, applied)
    body = payload_dict(document)
    observed = body.get("dispositions")
    if not isinstance(observed, list):
        checker.fail("Repair_Proposal_Dispositions_v4.dispositions is not a list")
        return
    if observed != expected:
        if len(observed) != len(expected):
            checker.fail(
                "repair disposition row count differs: "
                f"observed={len(observed)}, expected={len(expected)}"
            )
        for index, (actual, wanted) in enumerate(zip(observed, expected)):
            if actual != wanted:
                if isinstance(actual, dict):
                    report_exact_row_difference(
                        checker, f"repair disposition row[{index}]", actual, wanted
                    )
                else:
                    checker.fail(f"repair disposition row[{index}] is not an object")
                break

    dispositions = Counter(row["disposition"] for row in expected)
    domains = Counter(row["domain"] for row in expected)
    expected_counts = {
        "total": len(expected),
        "mathematics": domains["mathematics"],
        "physics": domains["physics"],
        "computer_science": domains["computer_science"],
        "applied_by_explicit_curation": dispositions["applied_by_explicit_curation"],
        "proposal_only_preserved": dispositions["proposal_only_preserved"],
    }
    if body.get("counts") != expected_counts:
        checker.fail(
            "repair proposal counts differ from the exact row oracle: "
            f"observed={body.get('counts')!r}, expected={expected_counts!r}"
        )
    expected_policy = {
        "proposal_presence_is_review_credit": False,
        "proposal_presence_is_truth_credit": False,
        "all_v2_proposals_conserved": True,
    }
    if body.get("policy") != expected_policy:
        checker.fail("repair proposal disposition policy differs from the closed contract")


def terminal_variant_ids(
    checker: Checker,
    roots: Iterable[str],
    redirects: Mapping[str, str],
    splits: Mapping[str, Sequence[str]],
) -> set[str]:
    terminals: set[str] = set()
    visiting: set[str] = set()

    def visit(identifier: str) -> None:
        if identifier in visiting:
            checker.fail(f"variant resolution graph contains a cycle at {identifier}")
            return
        if identifier in redirects:
            visiting.add(identifier)
            visit(redirects[identifier])
            visiting.remove(identifier)
            return
        if identifier in splits:
            visiting.add(identifier)
            for child in splits[identifier]:
                visit(child)
            visiting.remove(identifier)
            return
        terminals.add(identifier)

    for root in roots:
        visit(root)
    return terminals


def check_terminal_candidate_dispositions(
    checker: Checker,
    document: dict[str, Any],
    registry: dict[str, Any],
    numbering: Mapping[str, str],
) -> None:
    """Require candidate truth credit to use terminal, not superseded, children."""

    registry_body = payload_dict(registry)
    variant_by_id = {
        row.get("variant_id"): row
        for row in as_list(registry_body.get("variants"))
        if isinstance(row, dict) and isinstance(row.get("variant_id"), str)
    }
    redirects: dict[str, str] = {}
    for row in as_list(registry_body.get("redirects")):
        if not isinstance(row, dict):
            continue
        source = first_string(row, ("source_variant_id", "from_variant_id"))
        target = first_string(row, ("target_variant_id", "to_variant_id"))
        if isinstance(source, str) and isinstance(target, str):
            redirects[source] = target
    splits: dict[str, list[str]] = {}
    for row in as_list(registry_body.get("splits")):
        if not isinstance(row, dict):
            continue
        source = first_string(row, ("source_variant_id", "from_variant_id"))
        children = first_string_list(
            row, ("child_variant_ids", "target_variant_ids", "to_variant_ids")
        )
        if isinstance(source, str) and children is not None:
            splits[source] = children

    body = payload_dict(document)
    rows = as_list(body.get("dispositions")) or as_list(body.get("rows"))
    for index, row in enumerate(rows):
        if not isinstance(row, dict):
            checker.fail(f"candidate disposition output row[{index}] is not an object")
            continue
        key = row.get("candidate_key", f"row[{index}]")
        roots = [
            value
            for value in as_list(row.get("target_atv_ids"))
            if isinstance(value, str) and ATV_RE.fullmatch(value)
        ]
        expected = terminal_variant_ids(checker, roots, redirects, splits)
        terminal_values = row.get("terminal_atv_ids")
        if not isinstance(terminal_values, list):
            checker.fail(f"candidate {key!r} omits explicit terminal_atv_ids")
            continue
        observed = unique_strings(
            checker, terminal_values, f"candidate {key!r} terminal_atv_ids", ATV_RE
        )
        exact_set(
            checker,
            observed,
            expected,
            f"candidate {key!r} terminal resolution",
        )
        stage_values = row.get("terminal_stage_ids")
        if not isinstance(stage_values, list):
            checker.fail(f"candidate {key!r} omits explicit terminal_stage_ids")
        else:
            observed_stage = unique_strings(
                checker,
                stage_values,
                f"candidate {key!r} terminal_stage_ids",
                S4_RE,
            )
            expected_stage = {numbering[value] for value in expected if value in numbering}
            exact_set(
                checker,
                observed_stage,
                expected_stage,
                f"candidate {key!r} terminal Stage4 resolution",
            )
        terminal_children = row.get("terminal_children")
        if not isinstance(terminal_children, list):
            checker.fail(f"candidate {key!r} omits explicit terminal_children")
        else:
            child_atv = [
                child.get("variant_id")
                for child in terminal_children
                if isinstance(child, dict)
            ]
            child_set = unique_strings(
                checker,
                child_atv,
                f"candidate {key!r} terminal_children",
                ATV_RE,
            )
            exact_set(
                checker,
                child_set,
                expected,
                f"candidate {key!r} terminal child content",
            )
            for child in terminal_children:
                if not isinstance(child, dict):
                    checker.fail(f"candidate {key!r} terminal_children has a non-object")
                    continue
                atv = child.get("variant_id")
                variant = variant_by_id.get(atv)
                expected_child = {
                    "curation_key": variant.get("curation_key") if variant else None,
                    "variant_id": atv,
                    "stage_claim_id": numbering.get(atv),
                    "lifecycle": "active",
                }
                if child != expected_child:
                    checker.fail(
                        f"candidate {key!r} terminal child {atv!r} differs from "
                        "the registry-derived terminal record"
                    )

        for child_index, child in enumerate(as_list(row.get("children"))):
            if not isinstance(child, dict):
                checker.fail(f"candidate {key!r} children[{child_index}] is not an object")
                continue
            root = child.get("variant_id")
            if not isinstance(root, str) or ATV_RE.fullmatch(root) is None:
                checker.fail(f"candidate {key!r} child has malformed variant_id {root!r}")
                continue
            resolved = terminal_variant_ids(checker, [root], redirects, splits)
            expected_kind = (
                "redirect" if root in redirects else "split" if root in splits else "current"
            )
            expected_lifecycle = {
                "redirect": "redirected",
                "split": "split",
                "current": "active",
            }[expected_kind]
            if child.get("lifecycle") != expected_lifecycle:
                checker.fail(
                    f"candidate {key!r} child {root} has stale lifecycle "
                    f"{child.get('lifecycle')!r}"
                )
            resolution = child.get("current_resolution")
            if not isinstance(resolution, dict):
                checker.fail(
                    f"candidate {key!r} child {root} omits current_resolution"
                )
                continue
            if resolution.get("kind") != expected_kind:
                checker.fail(f"candidate {key!r} child {root} has wrong resolution kind")
            resolved_atv = resolution.get("terminal_atv_ids")
            if not isinstance(resolved_atv, list) or set(resolved_atv) != resolved or len(resolved_atv) != len(resolved):
                checker.fail(f"candidate {key!r} child {root} has stale terminal ATV resolution")
            resolved_stage = resolution.get("terminal_stage_ids")
            expected_resolved_stage = {numbering[value] for value in resolved}
            if (
                not isinstance(resolved_stage, list)
                or set(resolved_stage) != expected_resolved_stage
                or len(resolved_stage) != len(expected_resolved_stage)
            ):
                checker.fail(f"candidate {key!r} child {root} has stale terminal Stage4 resolution")
            if resolution.get("default_child") is not None:
                checker.fail(f"candidate {key!r} child {root} declares a default terminal")
            if resolution.get("evidence_inherited") is not False:
                checker.fail(f"candidate {key!r} child {root} inherits evidence")


def records_from_catalog(catalog: dict[str, Any]) -> list[dict[str, Any]]:
    body = payload_dict(catalog)
    rows = body.get("claims")
    if isinstance(rows, list):
        return [row for row in rows if isinstance(row, dict)]
    rows = body.get("records")
    if isinstance(rows, list):
        return [row for row in rows if isinstance(row, dict)]
    rows = body.get("claims")
    return [row for row in as_list(rows) if isinstance(row, dict)]


def record_atv_id(row: Mapping[str, Any]) -> str | None:
    for key in ("variant_id", "atv_id", "canonical_variant_id"):
        if isinstance(row.get(key), str):
            return row[key]
    if row.get("record_type") == "ATV" and isinstance(row.get("record_id"), str):
        return row["record_id"]
    return None


def record_s4_id(row: Mapping[str, Any]) -> str | None:
    for key in ("stage_claim_id", "stage_id", "s4_id"):
        if isinstance(row.get(key), str):
            return row[key]
    return None


def catalog_ato_ids(catalog: dict[str, Any]) -> set[str]:
    body = payload_dict(catalog)
    explicit = as_dict(body.get("universe")).get("baseline_ato_ids")
    if isinstance(explicit, list):
        return {value for value in explicit if isinstance(value, str)}
    result: set[str] = set()
    for row in records_from_catalog(catalog):
        if row.get("record_type") == "ATO" and isinstance(row.get("record_id"), str):
            result.add(row["record_id"])
        for value in as_list(row.get("source_occurrence_ids")):
            if isinstance(value, str) and ATO_RE.fullmatch(value):
                result.add(value)
    return result


def numbering_rows(numbering: dict[str, Any], catalog: dict[str, Any]) -> list[dict[str, Any]]:
    numbering_body = payload_dict(numbering)
    for key in ("rows", "mappings", "numbering", "claims", "records"):
        value = numbering_body.get(key)
        if isinstance(value, list):
            return [row for row in value if isinstance(row, dict)]
    result: list[dict[str, Any]] = []
    for row in records_from_catalog(catalog):
        atv = record_atv_id(row)
        stage = record_s4_id(row)
        if atv and stage:
            result.append({"atv_id": atv, "stage_claim_id": stage})
    return result


def check_catalog_and_numbering(
    checker: Checker,
    catalog: dict[str, Any],
    numbering: dict[str, Any],
    source_records_v4: dict[str, Any],
    baseline_ato: set[str],
    baseline_atv: set[str],
) -> tuple[set[str], dict[str, str], dict[str, dict[str, Any]]]:
    source_body = payload_dict(source_records_v4)
    source_rows = as_list(source_body.get("records"))
    observed_ato = unique_strings(
        checker,
        (
            row.get("occurrence_id")
            for row in source_rows
            if isinstance(row, dict)
        ),
        "Stage4 source records",
        ATO_RE,
    )
    declared_baseline_ato = unique_strings(
        checker,
        source_body.get("baseline_occurrence_ids", []),
        "Stage4 declared baseline occurrences",
        ATO_RE,
    )
    exact_set(
        checker,
        declared_baseline_ato,
        baseline_ato,
        "Stage4 declared baseline ATO",
    )
    if not baseline_ato <= observed_ato:
        exact_set(checker, observed_ato & baseline_ato, baseline_ato, "Stage4 baseline ATO")

    catalog_rows = records_from_catalog(catalog)
    catalog_by_atv: dict[str, dict[str, Any]] = {}
    for row in catalog_rows:
        atv = record_atv_id(row)
        if atv is None:
            continue
        if ATV_RE.fullmatch(atv) is None:
            checker.fail(f"catalog record has malformed ATV ID: {atv!r}")
            continue
        if atv in catalog_by_atv:
            checker.fail(f"catalog has duplicate ATV record: {atv}")
        catalog_by_atv[atv] = row
    catalog_atv = set(catalog_by_atv)
    missing_baseline = baseline_atv - catalog_atv
    if missing_baseline:
        checker.fail(f"Stage4 catalog drops baseline ATV IDs: {sorted(missing_baseline)[:8]!r}")

    pairs: list[tuple[str, str]] = []
    for row in numbering_rows(numbering, catalog):
        atv = row.get("atv_id") or row.get("variant_id") or row.get("canonical_variant_id")
        stage = row.get("stage_claim_id") or row.get("stage_id") or row.get("s4_id")
        if not isinstance(atv, str) or not isinstance(stage, str):
            checker.fail(f"numbering row lacks ATV/S4 IDs: {row!r}")
            continue
        atv_match = ATV_RE.fullmatch(atv)
        s4_match = S4_RE.fullmatch(stage)
        if atv_match is None or s4_match is None:
            checker.fail(f"malformed numbering pair: {atv!r} <-> {stage!r}")
            continue
        if atv_match.group(1) != s4_match.group(1):
            checker.fail(f"ordinal mismatch in numbering: {atv} <-> {stage}")
        pairs.append((atv, stage))
    by_atv = Counter(atv for atv, _stage in pairs)
    by_stage = Counter(stage for _atv, stage in pairs)
    duplicate_atv = sorted(key for key, count in by_atv.items() if count != 1)
    duplicate_stage = sorted(key for key, count in by_stage.items() if count != 1)
    if duplicate_atv:
        checker.fail(f"numbering is not functional by ATV: {duplicate_atv[:8]!r}")
    if duplicate_stage:
        checker.fail(f"numbering is not injective by S4 ID: {duplicate_stage[:8]!r}")
    mapping = dict(pairs)
    if set(mapping) != catalog_atv:
        exact_set(checker, set(mapping), catalog_atv, "ATV/S4 numbering domain")

    new_ordinals = sorted(int(ATV_RE.fullmatch(value).group(1)) for value in catalog_atv - baseline_atv)
    if new_ordinals:
        expected_new = list(range(3339, max(new_ordinals) + 1))
        if new_ordinals != expected_new:
            checker.fail(
                f"new ATV allocation is not an append-only contiguous suffix: {new_ordinals[:8]!r}"
            )
    declared_highwaters: list[int] = []
    for container in (
        numbering,
        catalog,
        payload_dict(numbering),
        payload_dict(catalog),
        as_dict(numbering.get("counts")),
        as_dict(catalog.get("counts")),
    ):
        for key in ("atv_high_watermark", "variant_high_watermark", "ATV"):
            value = container.get(key) if isinstance(container, dict) else None
            if isinstance(value, int):
                declared_highwaters.append(value)
    expected_highwater = max(int(ATV_RE.fullmatch(value).group(1)) for value in catalog_atv)
    if declared_highwaters and any(value != expected_highwater for value in declared_highwaters):
        checker.fail(
            f"declared ATV high-watermark differs from exact catalog max {expected_highwater}: "
            f"{declared_highwaters!r}"
        )
    return catalog_atv, mapping, catalog_by_atv


def check_registry_append(
    checker: Checker,
    v2_source: dict[str, Any],
    v2_registry: dict[str, Any],
    v4_registry: dict[str, Any],
    source_records_v4: dict[str, Any],
    catalog_atv: set[str],
) -> None:
    v4_body = payload_dict(v4_registry)
    specs = (
        ("ATF", "families", "family_id", 3119),
        ("ATS", "senses", "sense_id", 3338),
        ("ATV", "variants", "variant_id", 3338),
    )
    for prefix, field, id_field, baseline_high in specs:
        old_by_id = {
            row[id_field]: row
            for row in as_list(v2_registry.get(field))
            if isinstance(row, dict) and isinstance(row.get(id_field), str)
        }
        old = set(old_by_id)
        rows = as_list(v4_body.get(field))
        ids_list = [row.get(id_field) for row in rows if isinstance(row, dict)]
        pattern = re.compile(rf"^{prefix}-([0-9]{{8}})$")
        current = unique_strings(checker, ids_list, f"Stage4 {prefix} registry", pattern)
        missing = old - current
        if missing:
            checker.fail(f"Stage4 {prefix} registry drops baseline IDs: {sorted(missing)[:8]!r}")
        current_by_id = {
            row[id_field]: row
            for row in rows
            if isinstance(row, dict) and isinstance(row.get(id_field), str)
        }
        # Every inherited identity row is immutable, including all ATF
        # fields.  Reused-family membership belongs in the separate
        # family_membership_extensions edge list; it must never be smuggled
        # into a rewritten baseline family row.
        mutated = sorted(
            identifier
            for identifier in old & current
            if current_by_id[identifier] != old_by_id[identifier]
        )
        if mutated:
            checker.fail(f"Stage4 {prefix} registry mutates baseline rows: {mutated[:8]!r}")
        new_ordinals = sorted(
            int(pattern.fullmatch(value).group(1)) for value in current - old
        )
        if new_ordinals and new_ordinals != list(range(baseline_high + 1, max(new_ordinals) + 1)):
            checker.fail(f"Stage4 {prefix} allocation is not an append-only contiguous suffix")
        declared = as_dict(v4_body.get("namespace_high_watermarks")).get(prefix)
        expected = max(int(pattern.fullmatch(value).group(1)) for value in current)
        if declared != expected:
            checker.fail(f"Stage4 {prefix} high-watermark is {declared!r}, expected {expected}")
    v4_variants = {
        row.get("variant_id")
        for row in as_list(v4_body.get("variants"))
        if isinstance(row, dict) and isinstance(row.get("variant_id"), str)
    }
    if v4_variants != catalog_atv:
        exact_set(checker, v4_variants, catalog_atv, "Stage4 registry/catalog ATV")
    if v4_body.get("legacy_aliases") != v2_registry.get("legacy_aliases"):
        checker.fail("Stage4 registry mutates, reorders, drops, or adds legacy aliases")

    source_body = payload_dict(source_records_v4)
    source_rows = as_list(source_body.get("records"))
    ato_ids = {
        row.get("occurrence_id")
        for row in source_rows
        if isinstance(row, dict)
        and isinstance(row.get("occurrence_id"), str)
        and ATO_RE.fullmatch(row.get("occurrence_id"))
    }
    old_source_by_id = {
        row["occurrence_id"]: row
        for row in as_list(v2_source.get("records"))
        if isinstance(row, dict) and isinstance(row.get("occurrence_id"), str)
    }
    current_source_by_id = {
        row["occurrence_id"]: row
        for row in source_rows
        if isinstance(row, dict) and isinstance(row.get("occurrence_id"), str)
    }
    mutated_sources = sorted(
        occurrence_id
        for occurrence_id in set(old_source_by_id) & set(current_source_by_id)
        if current_source_by_id[occurrence_id] != old_source_by_id[occurrence_id]
    )
    if mutated_sources:
        checker.fail(f"Stage4 ATO records mutate baseline rows: {mutated_sources[:8]!r}")
    new_ato = sorted(int(ATO_RE.fullmatch(value).group(1)) for value in ato_ids if int(value[-8:]) > 3338)
    if new_ato and new_ato != list(range(3339, max(new_ato) + 1)):
        checker.fail("Stage4 ATO allocation is not an append-only contiguous suffix")
    declared_ato = source_body.get("namespace_high_watermark")
    expected_ato_highwater = max(int(value[-8:]) for value in ato_ids)
    if declared_ato != expected_ato_highwater:
        checker.fail("Stage4 ATO high-watermark differs from the exact source-record maximum")
    registry_ato = as_dict(v4_body.get("namespace_high_watermarks")).get("ATO")
    if registry_ato != expected_ato_highwater:
        checker.fail("Stage4 registry ATO high-watermark differs from source records")


def check_authoritative_supersessions(
    checker: Checker,
    manifest: dict[str, Any],
    fragments: Sequence[tuple[Path, dict[str, Any]]],
    v4_registry: dict[str, Any],
    catalog_by_atv: Mapping[str, dict[str, Any]],
) -> None:
    """Verify append-only corrections point from old exact ATV to one new ATV."""

    additions = authoritative_row_map(
        checker, manifest, fragments, "additions", "curation_key"
    )
    registry_body = payload_dict(v4_registry)
    variant_by_key = {
        row.get("curation_key"): row
        for row in as_list(registry_body.get("variants"))
        if isinstance(row, dict) and isinstance(row.get("curation_key"), str)
    }
    expected_redirects: dict[str, str] = {}
    for key, addition in additions.items():
        child = variant_by_key.get(key)
        for relation in as_list(addition.get("lineage")):
            if not isinstance(relation, dict) or relation.get("relation_type") != "supersedes":
                continue
            target = relation.get("target_atv_id")
            if relation.get("evidence_inherited") is not False:
                checker.fail(f"superseding addition {key!r} inherits evidence")
            if not isinstance(target, str) or target not in catalog_by_atv:
                checker.fail(
                    f"superseding addition {key!r} targets unknown prior ATV {target!r}"
                )
                continue
            child_id = child.get("variant_id") if isinstance(child, dict) else None
            if not isinstance(child_id, str) or child_id == target:
                checker.fail(f"superseding addition {key!r} has no distinct new ATV")
                continue
            target_ordinal = int(ATV_RE.fullmatch(target).group(1))
            child_ordinal = int(ATV_RE.fullmatch(child_id).group(1))
            if child_ordinal <= target_ordinal:
                checker.fail(f"superseding addition {key!r} is not append-only")
            if target in expected_redirects:
                checker.fail(f"prior ATV {target} is superseded by multiple additions")
            expected_redirects[target] = child_id

    observed_redirects: dict[str, str] = {}
    for row in as_list(registry_body.get("redirects")):
        if not isinstance(row, dict):
            checker.fail("Stage4 registry redirects contains a non-object")
            continue
        source = first_string(row, ("source_variant_id", "from_variant_id"))
        target = first_string(row, ("target_variant_id", "to_variant_id"))
        if not isinstance(source, str) or not isinstance(target, str):
            checker.fail(f"malformed Stage4 redirect row: {row!r}")
            continue
        if row.get("evidence_inherited") not in (False, None):
            checker.fail(f"Stage4 redirect {source} inherits evidence")
        if source in observed_redirects:
            checker.fail(f"Stage4 registry duplicates redirect source {source}")
        observed_redirects[source] = target
    if observed_redirects != expected_redirects:
        exact_set(
            checker,
            set(observed_redirects),
            set(expected_redirects),
            "authoritative supersession redirect sources",
        )
        changed = sorted(
            source
            for source in set(observed_redirects) & set(expected_redirects)
            if observed_redirects[source] != expected_redirects[source]
        )
        if changed:
            checker.fail(f"supersession redirects have wrong targets: {changed[:8]!r}")


def check_sealed_lifecycle_history(
    checker: Checker, v4_registry: dict[str, Any]
) -> None:
    """Enforce immutable sealed lifecycle rows and validate append-only rows."""

    body = payload_dict(v4_registry)
    variants = {
        row.get("variant_id")
        for row in as_list(body.get("variants"))
        if isinstance(row, dict) and isinstance(row.get("variant_id"), str)
    }
    rows_by_id: dict[str, dict[str, Any]] = {}
    lifecycle_sources: dict[str, str] = {}

    for field, id_field, pattern in (
        ("redirects", "redirect_id", REDIRECT_RE),
        ("splits", "split_id", SPLIT_RE),
    ):
        rows = body.get(field)
        if not isinstance(rows, list):
            checker.fail(f"Stage4 registry {field} is not a list")
            continue
        for index, row in enumerate(rows):
            if not isinstance(row, dict):
                checker.fail(f"Stage4 registry {field}[{index}] is not an object")
                continue
            lifecycle_id = row.get(id_field)
            if not isinstance(lifecycle_id, str) or pattern.fullmatch(lifecycle_id) is None:
                checker.fail(
                    f"Stage4 registry {field}[{index}] has malformed {id_field}: "
                    f"{lifecycle_id!r}"
                )
                continue
            if lifecycle_id in rows_by_id:
                checker.fail(f"Stage4 lifecycle ID is duplicated: {lifecycle_id}")
                continue
            rows_by_id[lifecycle_id] = row

            source = row.get("source_variant_id")
            if not isinstance(source, str) or source not in variants:
                checker.fail(f"Stage4 lifecycle row {lifecycle_id} has unknown source {source!r}")
            elif source in lifecycle_sources:
                checker.fail(
                    f"Stage4 variant {source} has multiple lifecycle actions: "
                    f"{lifecycle_sources[source]}, {lifecycle_id}"
                )
            else:
                lifecycle_sources[source] = lifecycle_id

            if field == "redirects":
                target = row.get("target_variant_id")
                if not isinstance(target, str) or target not in variants:
                    checker.fail(
                        f"Stage4 redirect {lifecycle_id} has unknown target {target!r}"
                    )
                if target == source:
                    checker.fail(f"Stage4 redirect {lifecycle_id} is a self-loop")
                payload = {
                    "source_variant_id": source,
                    "target_variant_id": target,
                    "curation_key": row.get("curation_key"),
                }
                expected_id = "REDIRECT-" + independent_stable_digest(
                    "awesome-theorems/stage4-supersedes-redirect/v4", payload
                )[:24].upper()
            else:
                children = row.get("child_variant_ids")
                if not isinstance(children, list) or not all(
                    isinstance(child, str) and child in variants for child in children
                ):
                    checker.fail(
                        f"Stage4 split {lifecycle_id} has unknown/malformed child variants"
                    )
                    children = as_list(children)
                if len(children) < 2 or len(children) != len(set(children)):
                    checker.fail(
                        f"Stage4 split {lifecycle_id} lacks at least two unique children"
                    )
                if source in children:
                    checker.fail(f"Stage4 split {lifecycle_id} contains its own source")
                payload = {
                    "source_variant_id": source,
                    "child_variant_ids": children,
                }
                expected_id = "SPLIT-" + independent_stable_digest(
                    "awesome-theorems/stage4-split/v4", payload
                )[:24].upper()
            if lifecycle_id != expected_id:
                checker.fail(
                    f"Stage4 lifecycle row {lifecycle_id} has non-deterministic ID; "
                    f"expected {expected_id}"
                )

    missing = sorted(set(SEALED_LIFECYCLE_ROW_SHA256) - set(rows_by_id))
    if missing:
        checker.fail(
            f"Stage4 registry removes sealed lifecycle history: {missing[:8]!r}"
        )
    for lifecycle_id in sorted(set(SEALED_LIFECYCLE_ROW_SHA256) & set(rows_by_id)):
        observed = sha256_bytes(canonical_json_bytes(rows_by_id[lifecycle_id]))
        expected = SEALED_LIFECYCLE_ROW_SHA256[lifecycle_id]
        if observed != expected:
            checker.fail(
                f"Stage4 registry rebinds/mutates sealed lifecycle row {lifecycle_id}"
            )


def find_alias_rows(documents: Sequence[dict[str, Any]]) -> list[dict[str, Any]]:
    # The canonical migration is variant-centric.  Expand each variant's alias
    # list together with its separate current resolution before considering
    # any alias-centric compatibility shape.  In particular,
    # legacy_alias_migrations carries only historical facts and cannot stand
    # in for the current resolution.
    for document in documents:
        body = payload_dict(document)
        for key in ("migrations", "mappings"):
            value = body.get(key)
            if not isinstance(value, list):
                continue
            expanded: list[dict[str, Any]] = []
            for mapping in value:
                if not isinstance(mapping, dict):
                    continue
                historical = mapping.get("v2_variant_id")
                current = as_dict(mapping.get("current_resolution"))
                for alias in as_list(mapping.get("legacy_alias_ids")):
                    expanded.append(
                        {
                            "alias_id": alias,
                            "historical_atv_id": historical,
                            "resolution_kind": current.get("kind", "current"),
                            "current_terminal_stage_ids": current.get(
                                "target_stage_claim_ids", []
                            ),
                            "default_child": current.get("default_child"),
                            "evidence_inherited": current.get("evidence_inherited"),
                        }
                    )
            if expanded:
                return expanded
    for document in documents:
        body = payload_dict(document)
        for key in ("legacy_aliases", "aliases"):
            value = body.get(key)
            if isinstance(value, list) and value:
                rows = [row for row in value if isinstance(row, dict)]
                if rows:
                    return rows
    return []


def first_string(row: Mapping[str, Any], keys: Sequence[str]) -> str | None:
    for key in keys:
        value = row.get(key)
        if isinstance(value, str):
            return value
    return None


def first_string_list(row: Mapping[str, Any], keys: Sequence[str]) -> list[str] | None:
    for key in keys:
        value = row.get(key)
        if isinstance(value, list) and all(isinstance(item, str) for item in value):
            return list(value)
    return None


def check_legacy_aliases(
    checker: Checker,
    documents: Sequence[dict[str, Any]],
    expected_aliases: dict[str, str],
    numbering: dict[str, str],
) -> list[dict[str, Any]]:
    rows = find_alias_rows(documents)
    if not rows:
        checker.fail("generated Stage4 outputs contain no legacy alias resolution rows")
        return []
    observed: dict[str, str] = {}
    stage_to_atv = {stage: atv for atv, stage in numbering.items()}
    for row in rows:
        alias = first_string(row, ("alias_id", "legacy_alias_id", "source_alias_id"))
        historical = first_string(
            row,
            (
                "historical_atv_id",
                "historical_target_atv_id",
                "historical_target_variant_id",
            ),
        )
        current = first_string_list(
            row,
            (
                "current_terminal_atv_ids",
                "current_target_atv_ids",
                "terminal_atv_ids",
                "current_terminal_target_ids",
                "current_terminal_stage_ids",
            ),
        )
        if not isinstance(alias, str) or THM_RE.fullmatch(alias) is None:
            checker.fail(f"malformed generated legacy alias row: {row!r}")
            continue
        if not isinstance(historical, str):
            checker.fail(f"legacy alias {alias} lacks separate historical ATV resolution")
            continue
        if current is None:
            checker.fail(f"legacy alias {alias} lacks separate current terminal resolution")
            current = []
        if alias in observed:
            checker.fail(f"duplicate generated legacy alias: {alias}")
        observed[alias] = historical
        kind = str(row.get("resolution_kind") or row.get("lifecycle") or "active")
        if kind == "split" and len(current) < 2:
            checker.fail(f"split alias {alias} has fewer than two current terminal targets")
        if kind in {"active", "current", "redirect", "redirected", "preserved"} and len(current) != 1:
            checker.fail(f"single-target alias {alias} has {len(current)} current targets")
        for target in current:
            if target not in numbering and target not in stage_to_atv:
                checker.fail(f"legacy alias {alias} resolves to unknown current target {target}")
        historical_s4 = first_string(row, ("historical_s4_id", "historical_stage_claim_id"))
        if historical_s4 is not None and numbering.get(historical) != historical_s4:
            checker.fail(f"legacy alias {alias} has inconsistent historical S4 resolution")
    if observed != expected_aliases:
        exact_set(checker, set(observed), set(expected_aliases), "Stage4 legacy alias IDs")
        rebound = sorted(
            alias
            for alias in set(observed) & set(expected_aliases)
            if observed[alias] != expected_aliases[alias]
        )
        if rebound:
            checker.fail(f"Stage4 rebinds historical legacy aliases: {rebound[:8]!r}")

    # Check the alias-centric historical migration independently.  It is an
    # immutable historical binding, not a replacement for current_resolution.
    historical_rows: list[dict[str, Any]] = []
    for document in documents:
        value = payload_dict(document).get("legacy_alias_migrations")
        if isinstance(value, list):
            historical_rows.extend(row for row in value if isinstance(row, dict))
    if not historical_rows:
        checker.fail("migration contains no historical legacy alias migration rows")
    else:
        historical_observed: dict[str, str] = {}
        for row in historical_rows:
            alias = first_string(row, ("alias_id", "legacy_alias_id"))
            target = first_string(
                row,
                ("historical_target_variant_id", "historical_target_atv_id"),
            )
            if not isinstance(alias, str) or not isinstance(target, str):
                checker.fail(f"malformed historical legacy alias migration: {row!r}")
                continue
            if alias in historical_observed:
                checker.fail(f"duplicate historical legacy alias migration: {alias}")
            historical_observed[alias] = target
            if row.get("rebound") is not False:
                checker.fail(f"historical legacy alias {alias} is marked rebound")
            stage_id = first_string(row, ("historical_stage_claim_id", "historical_s4_id"))
            if stage_id is not None and numbering.get(target) != stage_id:
                checker.fail(f"historical legacy alias {alias} has inconsistent Stage4 ID")
        if historical_observed != expected_aliases:
            exact_set(
                checker,
                set(historical_observed),
                set(expected_aliases),
                "historical legacy alias migration IDs",
            )
            rebound = sorted(
                alias
                for alias in set(historical_observed) & set(expected_aliases)
                if historical_observed[alias] != expected_aliases[alias]
            )
            if rebound:
                checker.fail(f"historical legacy alias migrations rebind aliases: {rebound[:8]!r}")
    m0387 = "THM-M-0387"
    if expected_aliases.get(m0387) != "ATV-00000393":
        checker.fail("v2 authority no longer maps THM-M-0387 to ATV-00000393")
    if observed.get(m0387) != "ATV-00000393":
        checker.fail("Stage4 historical resolution for THM-M-0387 is not ATV-00000393")
    if numbering.get("ATV-00000393") != "S4-CLM-00000393":
        checker.fail("Stage4 numbering does not map M0387 ATV to S4-CLM-00000393")
    return rows


def iter_dicts(value: Any, path: str = "$") -> Iterator[tuple[str, dict[str, Any]]]:
    if isinstance(value, dict):
        yield path, value
        for key, child in value.items():
            yield from iter_dicts(child, f"{path}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from iter_dicts(child, f"{path}[{index}]")


def check_splits(checker: Checker, documents: Sequence[tuple[str, dict[str, Any]]]) -> None:
    forbidden_default_keys = {"default_child", "default_child_id", "default_target", "preferred_child"}
    inheritance_keys = {
        "evidence_inherited",
        "inherits_evidence",
        "proof_inherited",
        "status_inherited",
        "receipt_inherited",
    }
    child_keys = (
        "split_children",
        "child_variant_ids",
        "child_atv_ids",
        "to_atv_ids",
        "current_terminal_atv_ids",
        "current_terminal_stage_ids",
        "current_terminal_target_ids",
        "target_stage_claim_ids",
    )
    for label, document in documents:
        for pointer, row in iter_dicts(document):
            state_values = {
                str(row.get(key)).casefold()
                for key in (
                    "action",
                    "kind",
                    "lifecycle",
                    "resolution_kind",
                    "migration_action",
                )
                if row.get(key) is not None
            }
            is_split_registry_row = isinstance(row.get("split_id"), str)
            if "split" not in state_values and not is_split_registry_row:
                continue
            children = first_string_list(row, child_keys)
            if children is None or len(children) < 2 or len(children) != len(set(children)):
                checker.fail(f"{label}{pointer} split lacks at least two unique children")
            for key in forbidden_default_keys:
                if key in row and row[key] not in (None, "", False):
                    checker.fail(f"{label}{pointer} split declares forbidden {key}")
            found_inheritance_contract = False
            for key in inheritance_keys:
                if key in row:
                    found_inheritance_contract = True
                    if row[key] not in (False, None, [], {}):
                        checker.fail(f"{label}{pointer} split inherits evidence via {key}")
            if "evidence_inheritance" in row:
                found_inheritance_contract = True
                if row["evidence_inheritance"] not in (False, None, [], {}, "none"):
                    checker.fail(f"{label}{pointer} split inherits evidence")
            if not found_inheritance_contract:
                checker.fail(f"{label}{pointer} split omits the no-evidence-inheritance contract")


def nested_value(row: Mapping[str, Any], *paths: Sequence[str]) -> Any:
    for path in paths:
        value: Any = row
        for key in path:
            if not isinstance(value, dict) or key not in value:
                value = None
                break
            value = value[key]
        if value is not None:
            return value
    return None


def truth_apt(row: Mapping[str, Any]) -> bool:
    value = nested_value(row, ("truth_apt",), ("claim_kind", "truth_apt"))
    if value is None:
        return row.get("record_role") == "claim"
    return value is True or value == "truth_apt"


def atomic(row: Mapping[str, Any]) -> bool:
    value = nested_value(row, ("atomicity",), ("claim_kind", "atomicity"))
    return value == "atomic"


def material_status(row: Mapping[str, Any]) -> str | None:
    value = nested_value(
        row,
        ("material_status", "value"),
        ("material_status", "status"),
        ("material_status",),
        ("statuses", "human_truth", "status"),
    )
    return value if isinstance(value, str) else None


def active_terminal(row: Mapping[str, Any]) -> bool:
    lifecycle = row.get("lifecycle", "active")
    return lifecycle == "active" and not as_list(row.get("lifecycle_target_stage_ids"))


def independent_stable_digest(namespace: str, payload: Any) -> str:
    """Reproduce a specified namespaced digest without importing the generator."""

    return sha256_bytes(namespace.encode("utf-8") + b"\0" + canonical_json_bytes(payload))


def stage_id_for_variant(checker: Checker, variant_id: Any, label: str) -> str:
    match = ATV_RE.fullmatch(variant_id) if isinstance(variant_id, str) else None
    if match is None:
        checker.fail(f"{label} has malformed variant ID: {variant_id!r}")
        return "S4-CLM-INVALID"
    return f"S4-CLM-{match.group(1)}"


def preferred_label_text(checker: Checker, value: Any, label: str) -> str:
    if isinstance(value, str) and value.strip():
        return value
    if isinstance(value, dict):
        preferred = value.get("zh-Hans", value.get("en"))
        if isinstance(preferred, str) and preferred.strip():
            return preferred
    checker.fail(f"{label} is not a usable preferred label")
    return str(value)


def canonical_claim_kind(value: Any) -> str:
    kind = str(value)
    return "theorem" if kind in THEOREM_SUBTYPES else kind


def semantic_payload_sha256(addition: Mapping[str, Any]) -> str:
    payload = {
        "record_role": addition.get("record_role"),
        "claim_kind": addition.get("claim_kind"),
        "atomicity": addition.get("atomicity"),
        "statement": addition.get("statement"),
    }
    return independent_stable_digest(
        "awesome-theorems/stage4-semantic-payload/v4", payload
    )


def status_bucket(record: Mapping[str, Any]) -> str:
    status = str(as_dict(record.get("material_status")).get("status", "unknown"))
    normalized = status.strip().casefold()
    return STATUS_BUCKETS.get(normalized, normalized.replace(" ", "_") or "unknown")


def authoritative_row_map(
    checker: Checker,
    manifest: dict[str, Any],
    fragments: Sequence[tuple[Path, dict[str, Any]]],
    field: str,
    key_field: str,
) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for label, raw in merged_rows(manifest, fragments, field):
        row = deepcopy({key: value for key, value in raw.items() if not key.startswith("_")})
        key = row.get(key_field)
        if not isinstance(key, str) or not key:
            checker.fail(f"{label} has no {key_field}")
            continue
        if key in result:
            checker.fail(f"authoritative {field} duplicates {key_field} {key!r}")
            continue
        result[key] = row
    return result


def expected_catalog_sources(
    checker: Checker,
    manifest: dict[str, Any],
    fragments: Sequence[tuple[Path, dict[str, Any]]],
) -> list[dict[str, Any]]:
    by_id: dict[str, dict[str, Any]] = {}
    for label, raw in merged_rows(manifest, fragments, "sources"):
        row = deepcopy({key: value for key, value in raw.items() if not key.startswith("_")})
        source_id = row.get("source_id")
        if not isinstance(source_id, str) or not source_id:
            checker.fail(f"{label} has no source_id")
            continue
        if source_id in by_id and by_id[source_id] != row:
            checker.fail(f"authoritative source {source_id!r} has conflicting definitions")
            continue
        by_id[source_id] = row
    return [by_id[source_id] for source_id in sorted(by_id)]


def baseline_catalog_oracle(
    checker: Checker,
    v2_catalog: dict[str, Any],
    v2_registry: dict[str, Any],
) -> dict[str, dict[str, Any]]:
    """Synthesize inherited catalog rows directly from the two v2 authorities."""

    raw_by_atv: dict[str, dict[str, Any]] = {}
    for raw in as_list(v2_catalog.get("records")):
        if not isinstance(raw, dict) or raw.get("record_type") != "ATV":
            continue
        variant_id = raw.get("record_id")
        if not isinstance(variant_id, str):
            checker.fail("v2 catalog contains an ATV row without record_id")
            continue
        if variant_id in raw_by_atv:
            checker.fail(f"v2 catalog duplicates ATV row {variant_id}")
        raw_by_atv[variant_id] = raw

    senses = {
        row.get("sense_id"): row
        for row in as_list(v2_registry.get("senses"))
        if isinstance(row, dict) and isinstance(row.get("sense_id"), str)
    }
    aliases_by_variant: dict[str, list[str]] = {}
    for row in as_list(v2_registry.get("legacy_aliases")):
        if not isinstance(row, dict):
            continue
        target = row.get("target_variant_id")
        alias = row.get("alias_id")
        if isinstance(target, str) and isinstance(alias, str):
            aliases_by_variant.setdefault(target, []).append(alias)

    expected: dict[str, dict[str, Any]] = {}
    for variant in as_list(v2_registry.get("variants")):
        if not isinstance(variant, dict):
            continue
        variant_id = variant.get("variant_id")
        if not isinstance(variant_id, str):
            checker.fail("v2 registry contains a variant without variant_id")
            continue
        raw = raw_by_atv.get(variant_id)
        sense = senses.get(variant.get("sense_id"))
        if raw is None or sense is None:
            checker.fail(f"cannot synthesize inherited catalog row {variant_id}")
            continue
        kind = as_dict(raw.get("claim_kind"))
        identity = as_dict(raw.get("identity"))
        tags = deepcopy(as_list(identity.get("discipline_tags")))
        human = as_dict(as_dict(raw.get("statuses")).get("human_truth"))
        preferred = identity.get("preferred_label", variant_id)
        evidence_refs = deepcopy(as_list(as_dict(raw.get("provenance")).get("evidence_refs")))
        labels = as_list(identity.get("labels"))
        registry_lifecycle = variant.get("lifecycle", "current")
        expected[variant_id] = {
            "variant_id": variant_id,
            "stage_claim_id": stage_id_for_variant(checker, variant_id, "v2 variant"),
            "stage_id": stage_id_for_variant(checker, variant_id, "v2 variant"),
            "source_occurrence_id": variant.get("bootstrap_occurrence_id"),
            "family_id": sense.get("family_id"),
            "sense_id": variant.get("sense_id"),
            "preferred_label": preferred,
            "aliases": [
                label.get("text")
                for label in labels
                if isinstance(label, dict) and label.get("text") != preferred
            ],
            "legacy_alias_ids": sorted(aliases_by_variant.get(variant_id, [])),
            "owner_domain": tags[0] if tags else "unreviewed",
            "membership_domains": tags,
            "record_role": "unreviewed_source_variant",
            "claim_kind": "unknown",
            "current_claim_kind": "unknown",
            "machine_triage_claim_kind": deepcopy(kind),
            "historical_kind": kind.get("historical_kind", "unreviewed"),
            "atomicity": kind.get("atomicity", "unknown"),
            "truth_apt": kind.get("truth_apt", "unknown"),
            "statement": deepcopy(as_dict(raw.get("exact_statement"))),
            "material_status": {
                "status": human.get("status", "unknown"),
                "as_of": human.get("as_of"),
                "basis": human.get("scope_note", "Inherited v2 machine triage."),
                "source_refs": deepcopy(as_list(human.get("source_refs"))),
            },
            "status_events": [],
            "provenance_source_refs": deepcopy(evidence_refs),
            "source_refs": deepcopy(evidence_refs),
            "rights_status": as_dict(raw.get("license")).get("status", "unknown"),
            "lineage": deepcopy(as_list(raw.get("relations"))),
            "lifecycle": (
                "active" if registry_lifecycle == "current" else registry_lifecycle
            ),
            "registry_lifecycle": registry_lifecycle,
            "curation_state": "inherited_v2_machine_triage",
            "curation_key": None,
            "candidate_keys": [],
            "overlay_keys": [],
        }
    if set(expected) != set(raw_by_atv):
        exact_set(checker, set(expected), set(raw_by_atv), "v2 catalog semantic oracle")
    return expected


def normalized_authoritative_overlays(
    checker: Checker,
    manifest: dict[str, Any],
    fragments: Sequence[tuple[Path, dict[str, Any]]],
    dispositions: Mapping[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for label, raw in merged_rows(manifest, fragments, "overlays"):
        row = deepcopy({key: value for key, value in raw.items() if not key.startswith("_")})
        if "curation_key" not in row:
            children = as_list(row.get("child_keys"))
            target = row.get("target_atv_id")
            inferred = sorted(
                candidate_key
                for candidate_key, disposition in dispositions.items()
                if set(as_list(disposition.get("child_keys"))) & set(children)
                or target in as_list(disposition.get("existing_atv_ids"))
            )
            digest = independent_stable_digest(
                "awesome-theorems/stage4-overlay-instruction/v4",
                {
                    "target_atv_id": target,
                    "action": row.get("action"),
                    "child_keys": children,
                },
            )
            row.update(
                {
                    "curation_key": f"overlay.{digest[:24]}",
                    "candidate_keys": inferred,
                    "change_class": (
                        "split_instruction" if children else "lineage_instruction"
                    ),
                    "evidence_inherited": False,
                }
            )
        key = row.get("curation_key")
        if not isinstance(key, str) or not key:
            checker.fail(f"{label} has no normalized curation_key")
            continue
        if key in result:
            checker.fail(f"authoritative overlays duplicate curation_key {key!r}")
            continue
        result[key] = row
    return [result[key] for key in sorted(result)]


def synthesize_expected_catalog(
    checker: Checker,
    v2_catalog: dict[str, Any],
    v2_registry: dict[str, Any],
    source_records_v4: dict[str, Any],
    registry_v4: dict[str, Any],
    manifest: dict[str, Any],
    fragments: Sequence[tuple[Path, dict[str, Any]]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Build a generator-independent exact catalog oracle from sealed inputs."""

    expected = baseline_catalog_oracle(checker, v2_catalog, v2_registry)
    baseline_ids = set(expected)
    additions = authoritative_row_map(
        checker, manifest, fragments, "additions", "curation_key"
    )
    dispositions = authoritative_row_map(
        checker, manifest, fragments, "dispositions", "candidate_key"
    )

    # A disposition edge is authoritative in both directions.  Regression
    # fixtures may attach an additional key to a child owned by another
    # fragment, so synthesize the normalized reverse edge explicitly.
    for candidate_key, disposition in dispositions.items():
        for child_key in as_list(disposition.get("child_keys")):
            addition = additions.get(child_key)
            if addition is None:
                checker.fail(
                    f"authoritative disposition {candidate_key!r} names missing child {child_key!r}"
                )
                continue
            addition["candidate_keys"] = sorted(
                set(as_list(addition.get("candidate_keys"))) | {candidate_key}
            )

    registry_body = payload_dict(registry_v4)
    source_body = payload_dict(source_records_v4)
    variant_by_key: dict[str, dict[str, Any]] = {}
    for row in as_list(registry_body.get("variants")):
        if not isinstance(row, dict) or row.get("variant_id") in baseline_ids:
            continue
        key = row.get("curation_key")
        if not isinstance(key, str) or not key:
            checker.fail(f"new registry variant lacks curation_key: {row.get('variant_id')!r}")
            continue
        if key in variant_by_key:
            checker.fail(f"new registry variants duplicate curation_key {key!r}")
        variant_by_key[key] = row
    exact_set(
        checker,
        set(variant_by_key),
        set(additions),
        "authoritative additions/new registry variants",
    )

    source_by_key: dict[str, dict[str, Any]] = {}
    for row in as_list(source_body.get("records")):
        if not isinstance(row, dict) or not isinstance(row.get("curation_key"), str):
            continue
        key = row["curation_key"]
        if key in source_by_key:
            checker.fail(f"Stage4 source rows duplicate curation_key {key!r}")
        source_by_key[key] = row
    exact_set(
        checker,
        set(source_by_key),
        set(additions),
        "authoritative additions/new source occurrences",
    )
    sense_by_id = {
        row.get("sense_id"): row
        for row in as_list(registry_body.get("senses"))
        if isinstance(row, dict) and isinstance(row.get("sense_id"), str)
    }
    family_by_id = {
        row.get("family_id"): row
        for row in as_list(registry_body.get("families"))
        if isinstance(row, dict) and isinstance(row.get("family_id"), str)
    }

    for key, addition in additions.items():
        variant = variant_by_key.get(key)
        source = source_by_key.get(key)
        if variant is None or source is None:
            continue
        variant_id = variant.get("variant_id")
        sense = sense_by_id.get(variant.get("sense_id"))
        if sense is None:
            checker.fail(f"addition {key!r} has no allocated registry sense")
            continue
        family_id = sense.get("family_id")
        family = family_by_id.get(family_id)
        occurrence_id = source.get("occurrence_id")
        if family is None:
            checker.fail(f"addition {key!r} has no allocated registry family")
        if variant.get("bootstrap_occurrence_id") != occurrence_id:
            checker.fail(f"addition {key!r} variant/source occurrence binding differs")
        if sense.get("bootstrap_occurrence_id") != occurrence_id:
            checker.fail(f"addition {key!r} sense/source occurrence binding differs")
        if sense.get("curation_key") != key or source.get("curation_key") != key:
            checker.fail(f"addition {key!r} allocation curation keys differ")
        expected_semantic_sha = semantic_payload_sha256(addition)
        if variant.get("semantic_payload_sha256") != expected_semantic_sha:
            checker.fail(f"addition {key!r} registry semantic digest differs from authority")
        if source.get("semantic_payload_sha256") != expected_semantic_sha:
            checker.fail(f"addition {key!r} source semantic digest differs from authority")
        # Source_Records_v4 is the immutable birth occurrence authority.  A
        # later metadata/status/source refinement updates the current catalog
        # projection but must not rewrite the already allocated ATO birth
        # row.  Current candidate/source edges are checked below by exact
        # manifest-to-catalog synthesis; only identity and semantic-payload
        # bindings are required of the frozen occurrence here.
        if addition.get("family_action") == "reuse_family":
            if family_id != addition.get("reuse_atf_id"):
                checker.fail(f"addition {key!r} changed its authoritative reused family")
        elif isinstance(family, dict) and family.get("curation_key") != key:
            checker.fail(f"addition {key!r} new family is not bound to its curation key")

        preferred = preferred_label_text(
            checker, addition.get("preferred_label"), f"addition {key!r}"
        )
        canonical_kind = canonical_claim_kind(addition.get("claim_kind"))
        lineage: list[dict[str, Any]] = []
        for relation in as_list(addition.get("lineage")):
            if not isinstance(relation, dict):
                checker.fail(f"addition {key!r} contains a non-object lineage edge")
                continue
            copied = deepcopy(relation)
            copied["target_stage_claim_id"] = stage_id_for_variant(
                checker, relation.get("target_atv_id"), f"addition {key!r} lineage"
            )
            lineage.append(copied)
        if not isinstance(variant_id, str):
            checker.fail(f"addition {key!r} lacks an allocated variant ID")
            continue
        expected[variant_id] = {
            "variant_id": variant_id,
            "stage_claim_id": stage_id_for_variant(checker, variant_id, f"addition {key!r}"),
            "stage_id": stage_id_for_variant(checker, variant_id, f"addition {key!r}"),
            "source_occurrence_id": occurrence_id,
            "family_id": family_id,
            "sense_id": sense.get("sense_id"),
            "preferred_label": preferred,
            "labels": (
                deepcopy(addition.get("preferred_label"))
                if isinstance(addition.get("preferred_label"), dict)
                else {"und": str(addition.get("preferred_label"))}
            ),
            "aliases": deepcopy(as_list(addition.get("aliases"))),
            "legacy_alias_ids": [],
            "owner_domain": addition.get("owner_domain"),
            "membership_domains": deepcopy(as_list(addition.get("membership_domains"))),
            "record_role": addition.get("record_role"),
            "claim_kind": canonical_kind,
            "current_claim_kind": canonical_kind,
            "claim_subtype": (
                addition.get("claim_kind")
                if canonical_kind != addition.get("claim_kind")
                else None
            ),
            "historical_kind": addition.get("historical_kind"),
            "atomicity": addition.get("atomicity"),
            "truth_apt": addition.get("record_role") == "claim",
            "statement": deepcopy(as_dict(addition.get("statement"))),
            "material_status": deepcopy(as_dict(addition.get("material_status"))),
            "status_events": [deepcopy(as_dict(addition.get("material_status")))],
            "provenance_source_refs": deepcopy(
                as_list(addition.get("provenance_source_refs"))
            ),
            "source_refs": deepcopy(as_list(addition.get("provenance_source_refs"))),
            "rights_status": addition.get("rights_status"),
            "lineage": lineage,
            "lifecycle": "active",
            "curation_state": "stage4_curated_addition",
            "curation_key": key,
            "candidate_keys": deepcopy(as_list(addition.get("candidate_keys"))),
            "overlay_keys": [],
            "semantic_payload_sha256": expected_semantic_sha,
        }

    superseded_targets = {
        relation.get("target_atv_id"): key
        for key, addition in additions.items()
        for relation in as_list(addition.get("lineage"))
        if isinstance(relation, dict) and relation.get("relation_type") == "supersedes"
    }
    redirect_by_source = {
        first_string(row, ("source_variant_id", "from_variant_id")): first_string(
            row, ("target_variant_id", "to_variant_id")
        )
        for row in as_list(registry_body.get("redirects"))
        if isinstance(row, dict)
    }
    for target, superseding_key in superseded_targets.items():
        if not isinstance(target, str) or target not in expected:
            checker.fail(
                f"superseding addition {superseding_key!r} targets absent prior catalog ATV {target!r}"
            )
            continue
        record = expected[target]
        record["lifecycle"] = "redirected"
        redirect_target = redirect_by_source.get(target)
        if isinstance(redirect_target, str):
            record["lifecycle_target_stage_ids"] = [
                stage_id_for_variant(
                    checker, redirect_target, f"superseded catalog record {target}"
                )
            ]
        record["redirected_by_curation_key"] = superseding_key

    overlays = normalized_authoritative_overlays(
        checker, manifest, fragments, dispositions
    )
    for overlay in overlays:
        key = overlay["curation_key"]
        target_id = overlay.get("target_atv_id")
        target = expected.get(target_id) if isinstance(target_id, str) else None
        if target is None:
            checker.fail(f"overlay {key!r} targets unknown catalog record {target_id!r}")
            continue
        if overlay.get("statement") not in (None, {}):
            checker.fail(f"overlay {key!r} attempts to change an exact statement")
        if "rights_status" in overlay:
            checker.fail(f"overlay {key!r} attempts to change catalog rights")
        if "preferred_label" in overlay:
            target["preferred_label"] = preferred_label_text(
                checker, overlay["preferred_label"], f"overlay {key!r}"
            )
            target["labels"] = (
                deepcopy(overlay["preferred_label"])
                if isinstance(overlay["preferred_label"], dict)
                else {"und": str(overlay["preferred_label"])}
            )
        if "claim_kind" in overlay:
            canonical_kind = canonical_claim_kind(overlay["claim_kind"])
            target["claim_kind"] = canonical_kind
            target["current_claim_kind"] = canonical_kind
            target["claim_subtype"] = (
                overlay["claim_kind"]
                if canonical_kind != overlay["claim_kind"]
                else None
            )
        if "historical_kind" in overlay:
            target["historical_kind"] = overlay["historical_kind"]
        if "material_status" in overlay:
            material = deepcopy(as_dict(overlay["material_status"]))
            target["material_status"] = material
            target["status_events"].append(deepcopy(material))
        membership_add = as_list(overlay.get("membership_domains_add"))
        if membership_add:
            if not all(isinstance(domain, str) and domain for domain in membership_add):
                checker.fail(f"overlay {key!r} has invalid membership_domains_add")
            target["membership_domains"] = sorted(
                set(as_list(target.get("membership_domains"))) | set(membership_add)
            )
        target["source_refs"] = sorted(
            set(as_list(target.get("source_refs")))
            | set(as_list(overlay.get("source_refs")))
        )
        target["provenance_source_refs"] = sorted(
            set(as_list(target.get("provenance_source_refs")))
            | set(as_list(overlay.get("source_refs")))
        )
        target["candidate_keys"] = sorted(
            set(as_list(target.get("candidate_keys")))
            | set(as_list(overlay.get("candidate_keys")))
        )
        target["overlay_keys"].append(key)
        child_keys = as_list(overlay.get("child_keys"))
        if child_keys:
            children: list[dict[str, Any]] = []
            for child_key in child_keys:
                variant = variant_by_key.get(child_key)
                if variant is None:
                    checker.fail(f"overlay {key!r} names unallocated child {child_key!r}")
                    continue
                child_variant = variant.get("variant_id")
                children.append(
                    {
                        "curation_key": child_key,
                        "variant_id": child_variant,
                        "stage_claim_id": stage_id_for_variant(
                            checker, child_variant, f"overlay {key!r} child"
                        ),
                        "evidence_inherited": False,
                    }
                )
            target["split_children"] = children
        target["curation_state"] = "stage4_curated_overlay"

    expected_rows = [expected[variant_id] for variant_id in sorted(expected)]
    return expected_rows, expected_catalog_sources(checker, manifest, fragments)


def report_exact_row_difference(
    checker: Checker,
    label: str,
    observed: Mapping[str, Any],
    expected: Mapping[str, Any],
) -> None:
    differing = [
        key
        for key in sorted(set(observed) | set(expected))
        if key not in observed or key not in expected or observed.get(key) != expected.get(key)
    ]
    if differing:
        first = differing[0]
        checker.fail(
            f"{label} differs from authoritative synthesis at field {first!r}; "
            f"differing_fields={differing[:8]!r}"
        )


def check_exact_catalog_content(
    checker: Checker,
    catalog: dict[str, Any],
    expected_rows: Sequence[dict[str, Any]],
    expected_sources: Sequence[dict[str, Any]],
) -> dict[str, dict[str, Any]]:
    body = payload_dict(catalog)
    observed_rows = records_from_catalog(catalog)
    expected_by_atv = {row["variant_id"]: row for row in expected_rows}
    observed_by_atv: dict[str, dict[str, Any]] = {}
    observed_order: list[str] = []
    for row in observed_rows:
        variant_id = record_atv_id(row)
        if not isinstance(variant_id, str):
            checker.fail("catalog contains a record without an ATV identity")
            continue
        observed_order.append(variant_id)
        if variant_id in observed_by_atv:
            checker.fail(f"catalog duplicates exact record {variant_id}")
        observed_by_atv[variant_id] = row
    exact_set(
        checker,
        set(observed_by_atv),
        set(expected_by_atv),
        "catalog authoritative record inventory",
    )
    expected_order = [row["variant_id"] for row in expected_rows]
    if observed_order != expected_order:
        checker.fail("catalog record order differs from ascending authoritative ATV order")
    for variant_id in sorted(set(observed_by_atv) & set(expected_by_atv)):
        if observed_by_atv[variant_id] != expected_by_atv[variant_id]:
            report_exact_row_difference(
                checker,
                f"catalog record {variant_id}",
                observed_by_atv[variant_id],
                expected_by_atv[variant_id],
            )

    state_counts = Counter(row["curation_state"] for row in expected_rows)
    expected_counts = {
        "records": len(expected_rows),
        "baseline_machine_triage": state_counts["inherited_v2_machine_triage"],
        "curated_additions": state_counts["stage4_curated_addition"],
        "curated_overlays": state_counts["stage4_curated_overlay"],
    }
    if body.get("counts", catalog.get("counts")) != expected_counts:
        checker.fail(
            f"catalog counts differ from authoritative synthesis: "
            f"observed={catalog.get('counts')!r}, expected={expected_counts!r}"
        )
    if body.get("sources", catalog.get("sources")) != list(expected_sources):
        checker.fail("catalog source table differs from sealed manifest/fragments")
    return observed_by_atv


def check_catalog_semantic_cross_fields(
    checker: Checker, records: Sequence[Mapping[str, Any]]
) -> None:
    """Reject internally consistent but semantically impossible catalog states."""

    material_claim_buckets = {
        "proved",
        "open",
        "partial",
        "independent",
        "conditional",
        "disputed",
        "refuted",
        "empirically_supported",
    }
    nonclaim_roles = {"entity", "event", "aggregate", "nonclaim"}
    for row in records:
        identifier = str(row.get("variant_id", "<unknown ATV>"))
        bucket = status_bucket(row)
        role = row.get("record_role")
        if bucket in material_claim_buckets:
            if role != "claim" or row.get("truth_apt") is not True:
                checker.fail(
                    f"catalog record {identifier} assigns material status {bucket!r} "
                    "to a non-truth-apt claim"
                )
            if row.get("atomicity") != "atomic":
                checker.fail(
                    f"catalog record {identifier} assigns material status {bucket!r} "
                    "without atomicity=atomic"
                )
        if role == "claim" and bucket == "not_applicable":
            checker.fail(
                f"catalog truth-claim record {identifier} has nonclaim status 'not_applicable'"
            )
        if role in nonclaim_roles:
            if bucket != "not_applicable":
                checker.fail(
                    f"catalog nonclaim record {identifier} has status {bucket!r}, "
                    "expected 'not_applicable'"
                )
            if row.get("truth_apt") is not False:
                checker.fail(
                    f"catalog nonclaim record {identifier} does not set truth_apt=false"
                )


def expected_projection_row(record: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "stage_claim_id": record["stage_claim_id"],
        "stage_id": record["stage_claim_id"],
        "variant_id": record["variant_id"],
        "preferred_label": record["preferred_label"],
        "owner_domain": record["owner_domain"],
        "record_role": record["record_role"],
        "current_claim_kind": record["current_claim_kind"],
        "historical_kind": record["historical_kind"],
        "material_status": deepcopy(record["material_status"]),
        "status_bucket": status_bucket(record),
        "statement": deepcopy(record["statement"]),
        "source_refs": deepcopy(record["source_refs"]),
        "curation_state": record["curation_state"],
        "lifecycle": record.get("lifecycle", "active"),
        "lifecycle_target_stage_ids": deepcopy(
            as_list(record.get("lifecycle_target_stage_ids"))
        ),
        "redirected_by_curation_key": record.get("redirected_by_curation_key"),
    }


def expected_projection_surfaces(
    expected_catalog_rows: Sequence[dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    theorem: list[dict[str, Any]] = []
    open_rows: list[dict[str, Any]] = []
    status: list[dict[str, Any]] = []
    for record in expected_catalog_rows:
        projected = expected_projection_row(record)
        eligible = (
            record.get("lifecycle", "active") == "active"
            and not record.get("split_children")
            and record.get("record_role") == "claim"
            and record.get("atomicity") == "atomic"
            and record.get("truth_apt") is True
        )
        bucket = projected["status_bucket"]
        if eligible and bucket == "proved":
            theorem.append(deepcopy(projected))
        if eligible and bucket in {
            "open",
            "partial",
            "independent",
            "conditional",
            "disputed",
        }:
            open_rows.append(deepcopy(projected))
        projected["status_event_count"] = len(as_list(record.get("status_events")))
        status.append(projected)
    theorem.sort(key=lambda row: row["stage_claim_id"])
    open_rows.sort(key=lambda row: row["stage_claim_id"])
    status.sort(key=lambda row: row["stage_claim_id"])
    return theorem, open_rows, status


def check_exact_projection_document(
    checker: Checker,
    kind: str,
    document: dict[str, Any],
    expected_rows: Sequence[dict[str, Any]],
    expected_counts: Mapping[str, Any],
    expected_policy: Mapping[str, Any],
) -> None:
    body = payload_dict(document)
    observed_rows = as_list(body.get("records"))
    if observed_rows != list(expected_rows):
        if len(observed_rows) != len(expected_rows):
            checker.fail(
                f"{kind} projection row count differs: "
                f"observed={len(observed_rows)}, expected={len(expected_rows)}"
            )
        for index, (observed, expected) in enumerate(zip(observed_rows, expected_rows)):
            if observed != expected:
                if isinstance(observed, dict):
                    report_exact_row_difference(
                        checker, f"{kind} projection row[{index}]", observed, expected
                    )
                else:
                    checker.fail(f"{kind} projection row[{index}] is not an object")
                break
    expected_ids = [row["stage_claim_id"] for row in expected_rows]
    if body.get("stage_claim_ids") != expected_ids:
        checker.fail(f"{kind} stage_claim_ids differ from authoritative projection order")
    if body.get("counts") != dict(expected_counts):
        checker.fail(
            f"{kind} projection counts differ: observed={body.get('counts')!r}, "
            f"expected={dict(expected_counts)!r}"
        )
    if body.get("projection_policy") != dict(expected_policy):
        checker.fail(f"{kind} projection policy differs from the Stage4 contract")


def markdown_escape(value: Any) -> str:
    if value is None:
        return ""
    return str(value).replace("|", "\\|").replace("\n", " ")


def render_expected_list_markdown(
    document: Mapping[str, Any],
    rows: Sequence[Mapping[str, Any]],
    title: str,
    caveat: str,
) -> str:
    lines = [
        f"# {title}",
        "",
        "> Generated from `Claim_Catalog_v4.json`; do not edit by hand.",
        ">",
        f"> {caveat}",
        "",
        f"Authority: `{document.get('authority_sha256')}`",
        "",
        "| Stage4 ID | ATV | Label | Domain | Kind | Status | Curation |",
        "|---|---|---|---|---|---|---|",
    ]
    for row in rows:
        lines.append(
            "| "
            + " | ".join(
                markdown_escape(value)
                for value in (
                    row["stage_claim_id"],
                    row["variant_id"],
                    row["preferred_label"],
                    row["owner_domain"],
                    row["current_claim_kind"],
                    as_dict(row.get("material_status")).get("status"),
                    row["curation_state"],
                )
            )
            + " |"
        )
    lines.extend(["", f"Records: **{len(rows)}**", ""])
    return "\n".join(lines)


def render_expected_status_markdown(
    document: Mapping[str, Any], rows: Sequence[Mapping[str, Any]]
) -> str:
    lines = [
        "# Stage4 Status Index",
        "",
        "> Generated from `Claim_Catalog_v4.json`; do not edit by hand.",
        "> Inherited `unknown` values remain unknown; list membership is not proof credit.",
        "",
        f"Authority: `{document.get('authority_sha256')}`",
        "",
        "| Stage4 ID | ATV | Label | Kind | Bucket | As of | Curation |",
        "|---|---|---|---|---|---|---|",
    ]
    for row in rows:
        lines.append(
            "| "
            + " | ".join(
                markdown_escape(value)
                for value in (
                    row["stage_claim_id"],
                    row["variant_id"],
                    row["preferred_label"],
                    row["current_claim_kind"],
                    row["status_bucket"],
                    as_dict(row.get("material_status")).get("as_of"),
                    row["curation_state"],
                )
            )
            + " |"
        )
    lines.extend(["", f"Records: **{len(rows)}**", ""])
    return "\n".join(lines)


def check_exact_projection_surfaces(
    checker: Checker,
    expected_catalog_rows: Sequence[dict[str, Any]],
    theorem_document: dict[str, Any],
    theorem_markdown: str,
    open_document: dict[str, Any],
    open_markdown: str,
    status_document: dict[str, Any],
    status_markdown: str,
) -> None:
    theorem_rows, open_rows, status_rows = expected_projection_surfaces(
        expected_catalog_rows
    )
    theorem_counts = {
        "records": len(theorem_rows),
        "curated": sum(
            row["curation_state"] != "inherited_v2_machine_triage"
            for row in theorem_rows
        ),
        "inherited_machine_triage": sum(
            row["curation_state"] == "inherited_v2_machine_triage"
            for row in theorem_rows
        ),
    }
    open_counts = {
        "records": len(open_rows),
        "curated": sum(
            row["curation_state"] != "inherited_v2_machine_triage"
            for row in open_rows
        ),
        "inherited_machine_triage": sum(
            row["curation_state"] == "inherited_v2_machine_triage"
            for row in open_rows
        ),
    }
    status_counts = {
        "records": len(status_rows),
        "buckets": dict(sorted(Counter(row["status_bucket"] for row in status_rows).items())),
    }
    check_exact_projection_document(
        checker,
        "theorem",
        theorem_document,
        theorem_rows,
        theorem_counts,
        {
            "query": "current_claim_kind in theorem-kind set and not open-kind/status",
            "machine_triage_rows_are_labeled": True,
        },
    )
    check_exact_projection_document(
        checker,
        "open",
        open_document,
        open_rows,
        open_counts,
        {
            "query": "current conjecture/hypothesis/open/assumption kind or material open-status",
            "historical_kind_does_not_imply_current_open_status": True,
        },
    )
    check_exact_projection_document(
        checker,
        "status",
        status_document,
        status_rows,
        status_counts,
        {
            "exactly_one_current_bucket_per_variant": True,
            "historical_and_current_status_are_distinct": True,
            "baseline_unknown_is_not_upgraded": True,
        },
    )

    expected_theorem_md = render_expected_list_markdown(
        theorem_document,
        theorem_rows,
        "Stage4 Theorem List",
        "Inherited machine-triage classifications remain visibly labeled and are not human truth review.",
    )
    if theorem_markdown != expected_theorem_md:
        checker.fail("theorem Markdown differs from the authoritative content projection")
    expected_open_md = render_expected_list_markdown(
        open_document,
        open_rows,
        "Stage4 Conjecture, Hypothesis, and Open List",
        "Current status is exact-variant scoped; historical conjecture names do not imply current openness.",
    )
    if open_markdown != expected_open_md:
        checker.fail("open Markdown differs from the authoritative content projection")
    expected_status_md = render_expected_status_markdown(status_document, status_rows)
    if status_markdown != expected_status_md:
        checker.fail("status Markdown differs from the authoritative content projection")


def catalog_projection_sets(
    catalog_by_atv: Mapping[str, dict[str, Any]], numbering: Mapping[str, str]
) -> tuple[set[str], set[str]]:
    theorem: set[str] = set()
    open_claims: set[str] = set()
    for atv, row in catalog_by_atv.items():
        stage_id = numbering.get(atv)
        if stage_id is None:
            continue
        status = str(as_dict(row.get("material_status")).get("status", "")).casefold()
        eligible = (
            active_terminal(row)
            and not as_list(row.get("split_children"))
            and row.get("record_role") == "claim"
            and atomic(row)
            and truth_apt(row)
        )
        if eligible and status in {"open", "partial", "independent", "conditional", "disputed"}:
            open_claims.add(stage_id)
        if eligible and status == "proved":
            theorem.add(stage_id)
    return theorem, open_claims


def projection_ids(document: dict[str, Any]) -> list[str]:
    document = payload_dict(document)
    for key in (
        "stage_claim_ids",
        "theorem_stage_ids",
        "open_or_conditional_stage_ids",
        "ids",
    ):
        value = document.get(key)
        if isinstance(value, list) and all(isinstance(item, str) for item in value):
            return list(value)
    rows = (
        document.get("rows")
        or document.get("records")
        or document.get("entries")
        or document.get("claims")
    )
    result: list[str] = []
    for row in as_list(rows):
        if not isinstance(row, dict):
            continue
        value = record_s4_id(row)
        if value is not None:
            result.append(value)
    return result


def check_projection(
    checker: Checker,
    kind: str,
    document: dict[str, Any],
    markdown: str,
    expected: set[str],
) -> None:
    ids = projection_ids(document)
    observed = unique_strings(checker, ids, f"{kind} JSON projection", S4_RE)
    exact_set(checker, observed, expected, f"{kind} catalog predicate projection")
    md_ids = re.findall(r"(?<![A-Za-z0-9-])S4-CLM-[0-9]{8}(?![0-9])", markdown)
    md_observed = unique_strings(checker, md_ids, f"{kind} Markdown projection", S4_RE)
    exact_set(checker, md_observed, observed, f"{kind} JSON/Markdown projection")


def normalize_hash(value: Any) -> str | None:
    if not isinstance(value, str):
        return None
    match = SHA256_RE.fullmatch(value)
    return match.group(1) if match else None


def check_authority_hashes(
    checker: Checker, documents: Sequence[tuple[str, dict[str, Any]]]
) -> None:
    artifact_names = {
        "Source_Records_v4.json": "source-records",
        "Claim_ID_Registry_v4.json": "claim-id-registry",
        "Stage4_Claim_ID_Registry_v4.json": "stage4-claim-id-registry",
        "Claim_ID_Migration_v2_to_v4.json": "claim-id-migration-v2-to-v4",
        "Candidate_Dispositions_v4.json": "candidate-dispositions",
        "Repair_Proposal_Dispositions_v4.json": "repair-proposal-dispositions",
        "Claim_Catalog_v4.json": "claim-catalog",
        "Theorem_List_v4.json": "theorem-list",
        "Conjecture_Hypothesis_Open_List_v4.json": "conjecture-hypothesis-open-list",
        "Status_Index_v4.json": "status-index",
    }
    for label, document in documents:
        if "authority_sha256" not in document:
            if Path(label).name in artifact_names:
                checker.fail(f"{label} has no authority_sha256")
            continue
        observed = normalize_hash(document.get("authority_sha256"))
        if observed is None:
            checker.fail(f"{label} has malformed authority_sha256")
            continue
        artifact = artifact_names.get(Path(label).name)
        if artifact is not None:
            expected_name = Path(label).name
            if document.get("artifact") != expected_name:
                checker.fail(
                    f"{label} artifact field is {document.get('artifact')!r}, "
                    f"expected {expected_name!r}"
                )
            if document.get("generated_by") != "Docs/tools/generate_claim_catalog_v4.py":
                checker.fail(f"{label} has an unexpected generated_by value")
            # Stage4 seals the canonical JSON body directly.  Artifact name
            # and schema are already fields in that body, so the independent
            # verifier needs no shared namespace lookup table.
            expected = plain_authority_digest(document)
            if observed != expected:
                checker.fail(f"{label} has stale authority_sha256")
            continue
        namespace = document.get("authority_namespace")
        candidates = {plain_authority_digest(document)}
        if isinstance(namespace, str) and namespace:
            candidates.add(authority_digest(namespace, document))
        schema_version = document.get("schema_version")
        if isinstance(schema_version, str):
            candidates.add(authority_digest(schema_version, document))
        if observed not in candidates:
            checker.fail(f"{label} has stale authority_sha256")


def safe_repo_path(checker: Checker, value: str, label: str) -> Path | None:
    candidate = Path(value.split("#", 1)[0])
    if candidate.is_absolute() or ".." in candidate.parts:
        checker.fail(f"{label} has unsafe source path: {value!r}")
        return None
    resolved = (checker.root / candidate).resolve()
    try:
        resolved.relative_to(checker.root)
    except ValueError:
        checker.fail(f"{label} escapes repository: {value!r}")
        return None
    return resolved


def check_source_ref(
    checker: Checker, value: Any, label: str, declared_source_ids: set[str]
) -> None:
    if not isinstance(value, str) or not value.strip():
        checker.fail(f"{label} contains an empty/non-string source reference")
        return
    parsed = urlparse(value)
    if value in declared_source_ids:
        return
    if parsed.scheme in {"https", "http"}:
        if not parsed.netloc:
            checker.fail(f"{label} has malformed URL: {value!r}")
        return
    if parsed.scheme == "doi":
        if not parsed.path:
            checker.fail(f"{label} has malformed DOI: {value!r}")
        return
    if re.fullmatch(r"10\.[0-9]{4,9}/\S+", value):
        return
    path = safe_repo_path(checker, value, label)
    if path is not None and not path.is_file():
        checker.fail(f"{label} points to missing repository file: {value!r}")


def check_source_refs(
    checker: Checker, documents: Sequence[tuple[str, dict[str, Any]]]
) -> None:
    source_rows: dict[str, tuple[str, dict[str, Any]]] = {}
    for label, document in documents:
        body = payload_dict(document)
        for index, row in enumerate(as_list(body.get("sources"))):
            if not isinstance(row, dict):
                checker.fail(f"{label}.sources[{index}] is not an object")
                continue
            source_id = row.get("source_id")
            if not isinstance(source_id, str) or not source_id:
                checker.fail(f"{label}.sources[{index}] has no source_id")
                continue
            if source_id in source_rows and source_rows[source_id][1] != row:
                checker.fail(f"source ID {source_id!r} has conflicting definitions")
            source_rows[source_id] = (label, row)
    declared_source_ids = set(source_rows)
    for source_id, (label, row) in source_rows.items():
        locator = row.get("locator") or row.get("url") or row.get("doi")
        check_source_ref(
            checker,
            locator,
            f"{label}.sources[{source_id!r}].locator",
            declared_source_ids,
        )
    for label, document in documents:
        for pointer, row in iter_dicts(document):
            for key, value in row.items():
                if key == "source_refs" or key.endswith("_source_refs"):
                    if not isinstance(value, list):
                        checker.fail(f"{label}{pointer}.{key} is not a list")
                        continue
                    for index, ref in enumerate(value):
                        check_source_ref(
                            checker,
                            ref,
                            f"{label}{pointer}.{key}[{index}]",
                            declared_source_ids,
                        )


def check_generation_manifest(checker: Checker, document: dict[str, Any]) -> None:
    checked = 0
    for pointer, row in iter_dicts(document):
        path_value = row.get("path")
        digest_value = row.get("sha256")
        if not isinstance(path_value, str) or digest_value is None:
            continue
        expected = normalize_hash(digest_value)
        if expected is None:
            checker.fail(f"generation manifest {pointer} has malformed sha256")
            continue
        path = safe_repo_path(checker, path_value, f"generation manifest {pointer}")
        if path is None or not path.is_file():
            checker.fail(f"generation manifest references missing file: {path_value!r}")
            continue
        if sha256_file(path) != expected:
            checker.fail(f"generation manifest has stale hash for {path_value}")
        checked += 1
    if checked == 0:
        checker.fail("generation manifest contains no verifiable path/sha256 bindings")


def check_authoritative_inputs(checker: Checker, label: str, document: dict[str, Any]) -> None:
    inputs = document.get("authoritative_inputs")
    if not isinstance(inputs, list):
        checker.fail(f"{label}.authoritative_inputs is not a list")
    declared_inventory_hash = normalize_hash(document.get("authoritative_inputs_sha256"))
    expected_inventory_hash = sha256_bytes(
        b"awesome-theorems/stage4-authoritative-inputs/v4\0"
        + canonical_json_bytes(inputs)
    )
    if declared_inventory_hash != expected_inventory_hash:
        checker.fail(f"{label} authoritative_inputs_sha256 is stale or malformed")
    checked = 0
    if isinstance(inputs, dict):
        for path_value, digest_value in inputs.items():
            expected = normalize_hash(digest_value)
            if not isinstance(path_value, str) or expected is None:
                continue
            path = safe_repo_path(checker, path_value, f"{label}.authoritative_inputs")
            if path is None or not path.is_file():
                checker.fail(f"{label} authoritative input is missing: {path_value!r}")
                continue
            if sha256_file(path) != expected:
                checker.fail(f"{label} authoritative input hash is stale: {path_value}")
            checked += 1
    for pointer, row in iter_dicts(inputs, "$.authoritative_inputs"):
        path_value = row.get("path")
        expected = normalize_hash(row.get("sha256"))
        if not isinstance(path_value, str) or expected is None:
            continue
        path = safe_repo_path(checker, path_value, f"{label}{pointer}")
        if path is None or not path.is_file():
            checker.fail(f"{label} authoritative input is missing: {path_value!r}")
            continue
        if sha256_file(path) != expected:
            checker.fail(f"{label} authoritative input hash is stale: {path_value}")
        checked += 1
    if checked == 0:
        checker.fail(f"{label} contains no independently verifiable authoritative input hash")


def authoritative_input_snapshot(
    checker: Checker, fragments: Sequence[tuple[Path, dict[str, Any]]]
) -> list[dict[str, Any]]:
    """Snapshot the complete specified input set without trusting an output list."""

    paths = (
        V2_SOURCE,
        V2_REGISTRY,
        V2_CATALOG,
        V2_CANDIDATES,
        V3_AUDIT,
        V4_MANIFEST,
        *REPAIR_INPUTS,
        *LEGACY_SOURCE_INPUTS,
        *(path for path, _document in fragments),
    )
    unique = {str(path): path for path in paths}
    snapshot: list[dict[str, Any]] = []
    for relative, path in sorted(unique.items()):
        absolute = checker.path(path)
        if not absolute.is_file():
            checker.fail(f"generation snapshot input is missing: {relative}")
            continue
        try:
            payload = absolute.read_bytes()
            size_after = absolute.stat().st_size
        except OSError as exc:
            checker.fail(f"generation snapshot input is unreadable: {relative}: {exc}")
            continue
        if len(payload) != size_after:
            checker.fail(f"generation snapshot input changed while reading: {relative}")
            continue
        snapshot.append(
            {
                "path": relative,
                "sha256": sha256_bytes(payload),
                "size_bytes": len(payload),
            }
        )
    return snapshot


def generated_output_snapshot(
    checker: Checker, paths: Iterable[Path]
) -> list[dict[str, Any]]:
    """Capture all selected output bytes while the shared directory lock is held."""

    snapshot: list[dict[str, Any]] = []
    for path in sorted(set(paths), key=str):
        absolute = checker.path(path)
        if not absolute.is_file():
            snapshot.append({"path": str(path), "exists": False})
            continue
        try:
            payload = absolute.read_bytes()
            size_after = absolute.stat().st_size
        except OSError as exc:
            checker.fail(f"generated output snapshot is unreadable: {path}: {exc}")
            continue
        if len(payload) != size_after:
            checker.fail(f"generated output changed while snapshotting: {path}")
            continue
        snapshot.append(
            {
                "path": str(path),
                "exists": True,
                "size_bytes": len(payload),
                "sha256": sha256_bytes(payload),
            }
        )
    return snapshot


def check_generation_snapshot_contract(
    checker: Checker,
    documents: Sequence[tuple[str, dict[str, Any]]],
    expected_snapshot: Sequence[dict[str, Any]],
) -> None:
    """Bind every JSON artifact to one complete, independently derived input CAS."""

    expected = list(expected_snapshot)
    expected_digest = independent_stable_digest(
        "awesome-theorems/stage4-authoritative-inputs/v4", expected
    )
    for label, document in documents:
        if document.get("generated_by") != "Docs/tools/generate_claim_catalog_v4.py":
            continue
        if document.get("authoritative_inputs") != expected:
            checker.fail(
                f"{label} is not bound to the complete current generation input snapshot"
            )
        if document.get("authoritative_inputs_sha256") != expected_digest:
            checker.fail(f"{label} has a divergent generation input snapshot digest")


def validate_manifest_contract(
    checker: Checker, manifest: dict[str, Any], expected_candidates: set[str]
) -> None:
    if manifest.get("schema_version") != "awesome-theorems/stage4-curation-manifest/4.0":
        checker.fail("unexpected Stage4 curation manifest schema_version")
    scope = as_dict(manifest.get("scope"))
    boundary = scope.get("completion_boundary")
    if boundary != "frozen_candidate_supplement_and_full_number_migration":
        checker.fail("Stage4 completion boundary is not the frozen supplement/full migration boundary")
    if scope.get("baseline_catalog_semantics") != "preserved_machine_triage_not_claimed_complete":
        checker.fail("Stage4 manifest overstates inherited baseline semantic completion")
    policy = as_dict(manifest.get("policy"))
    if str(policy.get("release_state", "")).casefold() != "sealed":
        checker.fail("Stage4 curation authority is not sealed")
    counts = as_dict(scope.get("candidate_universe"))
    expected_counts = {
        "coverage_v2_missing": 62,
        "coverage_v2_collisions": 36,
        "stage3_v3_delta": 56,
        "total": 154,
    }
    for key, expected in expected_counts.items():
        if counts.get(key) != expected:
            checker.fail(f"Stage4 manifest candidate count {key} is not {expected}")
    baseline = as_dict(scope.get("baseline_universe"))
    for key, expected in {
        "source_occurrences": 3338,
        "canonical_variants": 3338,
        "legacy_aliases": 3262,
        "folded_occurrences": 76,
    }.items():
        if baseline.get(key) != expected:
            checker.fail(f"Stage4 manifest baseline count {key} is not {expected}")
    if len(expected_candidates) != 154:
        checker.fail("internal candidate derivation did not produce 154 keys")


def run(checker: Checker) -> None:
    checker.note("completion_profile=audited_gap_supplement_and_full_number_migration")
    checker.note("global_baseline_semantic_completion=false")
    source = as_dict(checker.load_json(V2_SOURCE))
    registry = as_dict(checker.load_json(V2_REGISTRY))
    v2_catalog = as_dict(checker.load_json(V2_CATALOG))
    coverage = as_dict(checker.load_json(V2_CANDIDATES))
    audit_text = checker.load_text(V3_AUDIT)
    manifest = as_dict(checker.load_json(V4_MANIFEST))
    if checker.errors:
        return

    check_v2_authorities(checker, source, registry)
    baseline_ato, baseline_atv, aliases, folded = derive_v2_sets(
        checker, source, registry, v2_catalog
    )
    legacy_candidates, delta_candidates, candidates = derive_candidate_keys(
        checker, coverage, audit_text
    )
    proposals, proposal_sources = derive_proposals(checker)
    validate_manifest_contract(checker, manifest, candidates)
    fragments = load_v4_fragments(checker, manifest)
    generation_input_snapshot = authoritative_input_snapshot(checker, fragments)
    check_candidate_dispositions(checker, manifest, fragments, candidates)
    check_regression_fixtures(checker, fragments)

    selected = {name: select_output(checker, name) for name in OUTPUT_CANDIDATES}
    if any(value is None for value in selected.values()):
        return
    output_snapshot = generated_output_snapshot(
        checker, (path for path in selected.values() if path is not None)
    )
    markdown_names = {"theorem_md", "open_md", "status_md"}
    loaded = {
        name: checker.load_json(path) if name not in markdown_names else None
        for name, path in selected.items()
    }
    theorem_md = checker.load_text(selected["theorem_md"])
    open_md = checker.load_text(selected["open_md"])
    status_md = checker.load_text(selected["status_md"])
    if checker.errors:
        return

    catalog = as_dict(loaded["catalog"])
    source_records_v4 = as_dict(loaded["source_records"])
    id_registry_v4 = as_dict(loaded["id_registry"])
    migration = as_dict(loaded["migration"])
    numbering_document = as_dict(loaded["numbering"])
    candidate_document = as_dict(loaded["candidate_dispositions"])
    proposal_document = as_dict(loaded["proposal_dispositions"])
    theorem_document = as_dict(loaded["theorem_json"])
    open_document = as_dict(loaded["open_json"])
    status_document = as_dict(loaded["status_json"])

    for output_name, document in (
        ("source_records", source_records_v4),
        ("id_registry", id_registry_v4),
        ("numbering", numbering_document),
        ("migration", migration),
        ("candidate_dispositions", candidate_document),
        ("proposal_dispositions", proposal_document),
        ("catalog", catalog),
        ("theorem_json", theorem_document),
        ("open_json", open_document),
        ("status_json", status_document),
    ):
        check_canonical_artifact_shape(
            checker, str(selected[output_name]), document
        )

    candidate_payload = payload_dict(candidate_document)
    candidate_output_rows = as_list(candidate_payload.get("dispositions")) or as_list(
        candidate_payload.get("rows")
    )
    check_candidate_dispositions(
        checker,
        {"dispositions": candidate_output_rows},
        (),
        candidates,
    )
    check_repair_proposal_dispositions(
        checker,
        proposal_document,
        manifest,
        fragments,
        proposal_sources,
    )

    catalog_atv, numbering, catalog_by_atv = check_catalog_and_numbering(
        checker, catalog, numbering_document, source_records_v4, baseline_ato, baseline_atv
    )
    check_terminal_candidate_dispositions(
        checker, candidate_document, id_registry_v4, numbering
    )
    check_registry_append(
        checker, source, registry, id_registry_v4, source_records_v4, catalog_atv
    )
    check_sealed_lifecycle_history(checker, id_registry_v4)
    check_authoritative_supersessions(
        checker, manifest, fragments, id_registry_v4, catalog_by_atv
    )
    expected_catalog_rows, expected_catalog_source_rows = synthesize_expected_catalog(
        checker,
        v2_catalog,
        registry,
        source_records_v4,
        id_registry_v4,
        manifest,
        fragments,
    )
    check_exact_catalog_content(
        checker,
        catalog,
        expected_catalog_rows,
        expected_catalog_source_rows,
    )
    check_catalog_semantic_cross_fields(checker, expected_catalog_rows)
    alias_rows = check_legacy_aliases(
        checker, (migration,), aliases, numbering
    )
    check_exact_projection_surfaces(
        checker,
        expected_catalog_rows,
        theorem_document,
        theorem_md,
        open_document,
        open_md,
        status_document,
        status_md,
    )

    all_documents: list[tuple[str, dict[str, Any]]] = [
        (str(V4_MANIFEST), manifest),
        *((str(path), fragment) for path, fragment in fragments),
        (str(selected["source_records"]), source_records_v4),
        (str(selected["id_registry"]), id_registry_v4),
        (str(selected["catalog"]), catalog),
        (str(selected["migration"]), migration),
        (str(selected["numbering"]), numbering_document),
        (str(selected["candidate_dispositions"]), candidate_document),
        (str(selected["proposal_dispositions"]), proposal_document),
        (str(selected["theorem_json"]), theorem_document),
        (str(selected["open_json"]), open_document),
        (str(selected["status_json"]), status_document),
    ]
    check_splits(checker, all_documents)
    check_authority_hashes(checker, all_documents)
    check_source_refs(checker, all_documents)
    check_generation_snapshot_contract(
        checker, all_documents, generation_input_snapshot
    )
    for label, document in all_documents:
        if Path(label).name in {
            "Source_Records_v4.json",
            "Claim_ID_Registry_v4.json",
            "Stage4_Claim_ID_Registry_v4.json",
            "Claim_ID_Migration_v2_to_v4.json",
            "Candidate_Dispositions_v4.json",
            "Repair_Proposal_Dispositions_v4.json",
            "Claim_Catalog_v4.json",
            "Theorem_List_v4.json",
            "Conjecture_Hypothesis_Open_List_v4.json",
            "Status_Index_v4.json",
        }:
            check_authoritative_inputs(checker, label, document)

    # The exact folded set must be explicitly conserved somewhere in generated
    # authority, not merely represented by a count.
    explicit_folded: set[str] = set()
    for document in (source_records_v4, id_registry_v4, catalog, migration, numbering_document):
        body = payload_dict(document)
        universe = as_dict(body.get("universe"))
        for key in ("folded_occurrence_ids", "baseline_folded_occurrence_ids"):
            values = universe.get(key, body.get(key))
            if isinstance(values, list):
                explicit_folded.update(value for value in values if isinstance(value, str))
    if not explicit_folded:
        registry_aliases = as_list(payload_dict(id_registry_v4).get("legacy_aliases"))
        target_occurrences = {
            row.get("target_occurrence_id")
            for row in registry_aliases
            if isinstance(row, dict) and isinstance(row.get("target_occurrence_id"), str)
        }
        explicit_folded = baseline_ato - target_occurrences
    if explicit_folded != folded:
        exact_set(checker, explicit_folded, folded, "Stage4 folded occurrence conservation")

    # A migration must cover every inherited ATV exactly once.  Accept common
    # row field names but never infer coverage from a total alone.
    migration_rows: list[dict[str, Any]] = []
    migration_body = payload_dict(migration)
    for key in ("mappings", "migrations", "rows", "variant_migrations"):
        value = migration_body.get(key)
        if isinstance(value, list):
            migration_rows = [row for row in value if isinstance(row, dict)]
            if migration_rows:
                break
    covered: list[str] = []
    for row in migration_rows:
        values = first_string_list(row, ("from_atv_ids", "historical_target_ids"))
        if values is None:
            single = first_string(
                row, ("v2_variant_id", "from_atv_id", "source_atv_id", "source_id")
            )
            values = [single] if isinstance(single, str) and ATV_RE.fullmatch(single) else []
        covered.extend(value for value in values if ATV_RE.fullmatch(value))
    counts = Counter(covered)
    duplicates = sorted(value for value, count in counts.items() if count != 1)
    if duplicates:
        checker.fail(f"baseline ATV migration has duplicate source coverage: {duplicates[:8]!r}")
    exact_set(checker, set(covered) & baseline_atv, baseline_atv, "baseline ATV migration coverage")

    if checker.require_complete:
        # Completeness here is intentionally bounded.  Baseline semantic
        # machine-triage values remain honest and are not a failure.
        if len(candidates) != 154 or len(proposals) != 623:
            checker.fail("frozen supplement denominators are not 154 candidates and 623 proposals")
        if not baseline_atv <= catalog_atv or len(alias_rows) != 3262:
            checker.fail("full numbering migration does not conserve the inherited baseline")
        checker.note(
            "require_complete_scope=frozen_154_candidates+623_proposals+3338_numbering+"
            "3262_alias_resolution; inherited baseline semantic review is not claimed"
        )
    checker.note(
        f"baseline ATO/ATV={len(baseline_ato)}/{len(baseline_atv)}, aliases={len(aliases)}, "
        f"folded={len(folded)}, candidates={len(legacy_candidates)}+{len(delta_candidates)}, "
        f"proposals={len(proposals)}, current ATV/S4={len(numbering)}"
    )
    if authoritative_input_snapshot(checker, fragments) != generation_input_snapshot:
        checker.fail("authoritative inputs changed during the shared-lock verification snapshot")
    if generated_output_snapshot(
        checker, (path for path in selected.values() if path is not None)
    ) != output_snapshot:
        checker.fail("generated output set changed during the shared-lock verification snapshot")


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="repository root (default: inferred from this script)",
    )
    parser.add_argument(
        "--require-complete",
        action="store_true",
        help="require closure of the frozen Stage4 supplement, not full baseline semantic review",
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    checker = Checker(args.root, args.require_complete)
    lock_fd: int | None = None
    try:
        # The Stage4 publisher holds an exclusive flock on this directory
        # from its first input/prior-state snapshot through all renames and
        # the directory fsync.  Holding the matching shared lock for the
        # complete independent check prevents observation of a partially
        # published generation without introducing a mutable lock file.
        lock_fd = os.open(checker.path(Path("Docs/catalog/v4")), os.O_RDONLY)
        fcntl.flock(lock_fd, fcntl.LOCK_SH)
        run(checker)
    except (OSError, ValueError, TypeError, CheckFailure) as exc:
        checker.fail(f"unhandled verification input error: {exc}")
    finally:
        if lock_fd is not None:
            try:
                fcntl.flock(lock_fd, fcntl.LOCK_UN)
            finally:
                os.close(lock_fd)
    if checker.errors:
        print(f"FAIL check_claim_catalog_v4 ({len(checker.errors)} errors)")
        for note in checker.notes:
            print(f"- {note}")
        for error in checker.errors:
            print(f"- {error}")
        return 1
    suffix = " --require-complete" if checker.require_complete else ""
    print(f"PASS check_claim_catalog_v4{suffix}")
    for note in checker.notes:
        print(f"- {note}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
