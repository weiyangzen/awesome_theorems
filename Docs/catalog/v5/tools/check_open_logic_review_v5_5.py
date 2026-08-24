#!/usr/bin/env python3
"""Build and validate the fixed-commit Open Logic Problems source review.

This audit is deliberately release-external.  It binds 17 source records to the
pinned Open Logic Problems commit, the published awesome-theorems 5.4 parent,
and the reviewed cross-source occurrences.  The --write mode emits only files
under the selected audit directory; the default mode is read-only validation.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path
import tarfile
import tempfile
from typing import Any


SCHEMA_VERSION = "awesome-theorems/open-logic-strict-source-review/1.0"
REVIEW_AS_OF = "2026-08-10"
SOURCE_REPOSITORY = "https://github.com/pglutz/open-logic-problems"
SOURCE_COMMIT = "479fe770f974c6345559cabe278192133f037022"
REPO_ROOT = Path(__file__).resolve().parents[4]
SOURCE_ARCHIVE_DEFAULT = REPO_ROOT / "Docs/catalog/v5/sources/open-logic-problems-479fe770-source.tar.gz"
CB_ARCHIVE_DEFAULT = REPO_ROOT / "Docs/catalog/v5/sources/open-logic-crosscheck-conjecturebench-357bcb1a.tar.gz"
EVAND_ARCHIVE_DEFAULT = REPO_ROOT / "Docs/catalog/v5/sources/open-logic-crosscheck-open-math-problems-70e3fc18.tar.gz"
WORKSPACE_DEFAULT = REPO_ROOT
AUDIT_DIR_DEFAULT = REPO_ROOT / "Docs/catalog/v5/curation/open_logic_v5_5"

SOURCE_ARCHIVE_SHA256 = "012289b116f0ae7914d6a5ef6260635eac9ec9f3ac512ce61246094ca4a9eed5"
CB_ARCHIVE_SHA256 = "915fbf28a48465a1e7e83ab812b46ff301c1809000aa34bc1ae1dcf31f76c080"
EVAND_ARCHIVE_SHA256 = "bed4bbe0c6b00213d101cb4f2c9a0f518ba3da0bdabd9a6b562f5cfcfaafde57"

JSONL_NAME = "open-logic-review.jsonl"
SHA_NAME = "open-logic-review.sha256"
COUNT_NAME = "open-logic-review.count.json"

LICENSE_SHA256 = "6b2d3400b33b3edb412a475e32d1903823ffcd30e9ee84404b7c3d98e2c8f9b2"
STATUS_SNAPSHOT_SHA256 = "4c334cec63fa2dd7de24e9b96a285df4758d19191ac1aaf594b360062a39dbd1"
FAQ_SHA256 = "6f6963d787219fd380543e0b263a98f16766a8e058eb121debb9a44c53f3cdeb"
PARENT_CATALOG_REL = Path("Docs/catalog/v5/releases/5.4/Claim_Catalog.json")
PARENT_CATALOG_SHA256 = "384c1e34a57443dafe2e2ce70e36d6a6e23c6d03e006171b94aa2defa92e9709"

SOURCE_FILE_SHA256 = {
    1: "eacd3e0fc422434b843e6921e62ebf21821a054ce3c64a4b6934bbbe2b8b5f07",
    2: "f2eaf4b54da443f7a29437a6636176640bd4e907d99fd31c889f0d61f17c7224",
    3: "4e6197be294da25cac695873db092583a8fc5536b8d66149ec386f9cf0204e81",
    4: "54f2e1f72eef424163039332b6885dc1c77647d6dfba1f484f464dafe5a477cc",
    5: "bc323f5c1cfa43ae55d8884e2569a975ec3940e744460e2df8ad1829d9d3484b",
    6: "df42a91b012c7809569aaad5c080fb2ad14057d40df9d9309025d2df8b73dde2",
    7: "88ae9d51cae5e087ca932d62d3ac044029d6ff9cc5bd4d86c5b773c204197df6",
    8: "ec093a2b386ca6d4459e790d109043979da21dafc1b6a4e2a618ed950f619b2c",
    9: "5ad7529c8f77cbf77bd2575177f1382afaaf9027d33000f075004483ab9512d0",
    10: "1a1cc387c4e201bfbd57126fa9f56fa328ac822800b763b5e2757c56b97235f3",
    11: "6d9f042ec3087b7bd8c1097b8d3f15e08cad6ba1013a2a9d8883b977755e7254",
    12: "1184a74b2f6cac5b6710801c66a794c5601fe88e56ca0c6298a1982eced43489",
    13: "75150c093ecc3568d5467690d80444fa146529024025bbd8db23f36ee2dfe91c",
    14: "990e8f96050b72ff46bee999d48b443f6303344aa92be29e89aea9e80df30aaa",
    15: "72f677e41dd780a830b3bcd09c5b52c648cbb070deeb4ab8dfdf4ce38f2793ef",
    16: "bbb7fecfae394b86e15d9a49175826d36d09b6704d0d255a9eec7430dfd2111a",
    17: "7b2a9f39863331f0d717c754ece075ec53754bfca933f10b5b51cdeeebb65c80",
}

EXPECTED_NAMES = {
    1: "Vaught's Conjecture",
    2: "Martin's Conjecture",
    3: "Is Fraïssé's Conjecture Provable in ATR₀?",
    4: "Stable Forking Conjecture",
    5: "Does the Partition Principle imply the Axiom of Choice?",
    6: "Is the universal triangle free graph pseudofinite?",
    7: "Kolmogorov-Loveland randomness vs Martin-Löf randomness",
    8: "Conservativity of Ramsey's Theorem for pairs",
    9: "Borel boundedness of CBERs",
    10: "Is every Polish group graphic?",
    11: "Kreisel's Conjecture",
    12: "Weiss's Question",
    13: "Stable fields conjecture",
    14: "Cherlin-Zilber Algebraicity Conjecture",
    15: "Axiomatizability of generic automorphisms",
    16: "Axiom of Choice and bases for vector spaces over a specific field",
    17: "Non-trivial automorphisms of the Turing degrees",
}

EXACT_CLAIMS = {
    1: r"Vaught's Conjecture states that if $T$ is a first-order theory in a countable language then either $I(T, \aleph_0) \leq \aleph_0$ or $I(T, \aleph_0) = 2^{\aleph_0}$.",
    2: r"""Work in $\mathsf{ZF} + \mathsf{AD} + \mathsf{DC}$. Martin's Conjecture consists of the following two statements.

1. Every Turing invariant function $f\colon 2^\mathbb{N} \to 2^\mathbb{N}$ is either Martin equivalent to a constant function or Martin above the identity function.
2. The Martin order restricted to the Turing invariant functions which are Martin above the identity function is a prewellorder and the successor operation is given by the Turing jump—i.e. the successor of $f$ in the prewellorder is the function $x \mapsto f(x)'$.""",
    4: r"The Stable Forking Conjecture states that if $T$ is a simple theory then forking is always witnessed by stable formulas. In particular, if $\operatorname{tp}(a/Cb)$ forks over $C$ then there is a stable formula $\varphi(x, y)$ such that $\varphi(x, b) \in \operatorname{tp}(a/Cb)$ and $\varphi(x, b)$ forks over $C$.",
    13: "The stable fields conjecture asserts that every infinite stable field is separably closed.",
    14: "Every infinite simple group of finite Morley rank is an algebraic group over an algebraically closed field.",
}

FORMS = {
    1: "declarative_conjecture_with_meta_question",
    2: "declarative_compound_conjecture",
    3: "background_plus_interrogative",
    4: "declarative_conjecture",
    5: "definition_plus_interrogative",
    6: "definition_plus_compound_interrogative",
    7: "interrogative",
    8: "interrogative",
    9: "interrogative",
    10: "definition_plus_interrogative",
    11: "setup_plus_interrogative",
    12: "interrogative",
    13: "declarative_conjecture",
    14: "declarative_conjecture",
    15: "setup_plus_interrogative",
    16: "background_plus_compound_interrogative",
    17: "interrogative",
}

TARGET_COMPONENTS = {2: 2, 3: 2, 6: 2, 16: 2}

DECISIONS = {
    1: ("reject", "semantic_duplicate_parent_5_4", "The explicit Vaught proposition is already represented by the parent 5.4 strict claim; an occurrence cannot earn new quota credit."),
    2: ("accept", "explicit_compound_open_conjecture", "The source explicitly calls both numbered propositions Martin's Conjecture, supplies the ZF+AD+DC scope and definitions, marks it open, and assigns impact 3."),
    3: ("reject", "interrogative_not_asserted_conjecture", "The open target is asked as two questions; the surrounding proved implications do not assert either answer."),
    4: ("accept", "explicit_open_conjecture", "The source explicitly asserts the stable-forking proposition, gives its witness formulation, marks it open, and assigns impact 2."),
    5: ("reject", "interrogative_not_asserted_conjecture", "The source defines the Partition Principle but only asks whether it implies Choice; the implication is not asserted."),
    6: ("reject", "interrogative_not_asserted_conjecture", "Both the Henson-graph instance and the general K_n-free version are questions, not source assertions."),
    7: ("reject", "interrogative_not_asserted_conjecture", "The KL-randomness implication is written only as a question."),
    8: ("reject", "interrogative_not_asserted_conjecture", "The Pi^1_1-conservativity target is written only as a question."),
    9: ("reject", "interrogative_not_asserted_conjecture", "Borel boundedness of all countable Borel equivalence relations is written only as a question."),
    10: ("reject", "interrogative_and_below_importance_threshold", "The target is a question and source impact 1 maps below the high/medium admission threshold."),
    11: ("reject", "interrogative_and_below_importance_threshold", "Kreisel's target is a question, source impact is 1, and the canonical-reference metadata also needs correction."),
    12: ("reject", "interrogative_not_asserted_conjecture", "Weiss's target is written only as a question; its high impact does not authorize conversion to an assertion."),
    13: ("accept", "explicit_open_conjecture", "The source explicitly asserts the stable-fields proposition, marks it open, assigns impact 2, and supplies a usable reference after trimming DOI whitespace."),
    14: ("accept", "explicit_open_conjecture", "The source gives a declarative contemporary Cherlin-Zilber formulation, marks it open, assigns impact 2, and supplies historical plus modern supporting references; the 1979 citation must not be described as the exact contemporary wording."),
    15: ("reject", "interrogative_and_below_importance_threshold", "The generic-automorphism target is a question, source impact is 1, and the canonical year is incorrect."),
    16: ("reject", "interrogative_not_asserted_conjecture", "The source explicitly presents two versions as questions and does not assert either implication."),
    17: ("reject", "interrogative_not_asserted_conjecture", "Existence of a nontrivial Turing-degree automorphism is written only as a question."),
}

REFERENCE_REVIEW: dict[int, dict[str, Any]] = {
    1: {"identifier": "arXiv:2508.06854", "issues": [], "support": "direct_recent_reference"},
    2: {"identifier": "arXiv:1109.1875", "issues": [], "support": "direct_book_chapter_reference"},
    3: {"identifier": "doi:10.1142/S0219061317500064", "issues": [], "support": "direct_reference"},
    4: {"identifier": "arXiv:2607.09069", "issues": [], "support": "direct_recent_reference"},
    5: {"identifier": "doi:10.1305/ndjfl/1093635502", "issues": [], "support": "direct_reference"},
    6: {
        "identifier": "doi:10.1090/conm/558/11055",
        "issues": ["canonical_venue_should_be_Contemporary_Mathematics_not_Pacific_Journal_of_Mathematics"],
        "verified": {"venue": "Contemporary Mathematics", "year": 2011},
        "support": "direct_reference_with_venue_correction",
    },
    7: {"identifier": "doi:10.2178/bsl/1154698740", "issues": [], "support": "direct_reference"},
    8: {"identifier": "doi:10.1016/j.aim.2016.11.036", "issues": [], "support": "direct_reference"},
    9: {"identifier": "doi:10.1090/conm/425/08121", "issues": [], "support": "direct_reference"},
    10: {"identifier": "doi:10.1016/j.aim.2025.110765", "issues": [], "support": "direct_reference"},
    11: {
        "identifier": "doi:10.1098/rsta.2022.0020",
        "issues": [
            "canonical_year_2024_should_be_2023",
            "canonical_author_list_omits_Andreas_Weiermann",
            "doi_stored_as_https_url_instead_of_bare_identifier",
        ],
        "verified": {"year": 2023, "authors": ["J. P. Aguilera", "F. Pakhomov", "A. Weiermann"]},
        "support": "direct_reference_with_metadata_corrections",
    },
    12: {
        "identifier": "doi:10.2307/2275102",
        "issues": ["canonical_doi_has_trailing_period_and_literal_value_does_not_resolve"],
        "verified": {"year": 1993},
        "support": "direct_reference_after_doi_normalization",
    },
    13: {
        "identifier": "doi:10.1017/bsl.2019.13",
        "issues": ["canonical_doi_has_trailing_whitespace"],
        "verified": {"year": 2019},
        "support": "direct_reference_after_whitespace_normalization",
    },
    14: {
        "identifier": "doi:10.1016/0003-4843(79)90019-6",
        "issues": [
            "doi_stored_as_https_url_instead_of_bare_identifier",
            "canonical_1979_reference_is_historical_and_not_exact_source_for_the_contemporary_finite_Morley_rank_wording",
            "canonical_venue_has_trailing_whitespace",
        ],
        "verified": {"year": 1979},
        "support": "historical_reference_plus_modern_additional_references",
        "release_citation_rule": "Describe the 1979 item as historical; cite a modern additional reference for the contemporary formulation.",
    },
    15: {
        "identifier": "doi:10.2307/2586697",
        "issues": ["canonical_year_2014_should_be_2000"],
        "verified": {"year": 2000},
        "support": "direct_reference_with_year_correction",
    },
    16: {
        "identifier": "doi:10.1002/malq.201200049",
        "issues": ["doi_stored_as_https_url_instead_of_bare_identifier"],
        "verified": {"year": 2013},
        "support": "direct_reference_after_identifier_normalization",
    },
    17: {
        "identifier": "doi:10.1017/bsl.2018.15",
        "issues": ["canonical_title_has_leading_whitespace"],
        "verified": {"year": 2018},
        "support": "direct_reference_after_title_normalization",
    },
}

CB_COMMIT = "357bcb1a1daf93917d42e8206ceaa55645729a09"
CB_FILES = {
    "unsolvedmath-1220": ("problems/extended-catalog/unsolvedmath/unsolvedmath-1220.json", "a7200aafaca17a1d4f94c531a4e10ed519d100dba76fe2d84dd75e4f16709672"),
    "unsolvedmath-1343": ("problems/extended-catalog/unsolvedmath/unsolvedmath-1343.json", "bbf7f4d78c006cebf4625e713ea59d7484e4d0c791c57156cbce51bd277710a9"),
    "unsolvedmath-1344": ("problems/extended-catalog/unsolvedmath/unsolvedmath-1344.json", "f56b3750c15da5454a423ac7cef23f995e1160e544a993b15db783029e6c805f"),
    "unsolvedmath-1347": ("problems/extended-catalog/unsolvedmath/unsolvedmath-1347.json", "1c80a0b02f733c91091f4e9933966603fdc64926b03e818ef8f9c67436f505a3"),
    "unsolvedmath-1458": ("problems/extended-catalog/unsolvedmath/unsolvedmath-1458.json", "f6e3a903c786649e75bf87cdd4c4d8f0fb5e228f57deb3985f9ae0f6c2f5c31f"),
    "unsolvedmath-1461": ("problems/extended-catalog/unsolvedmath/unsolvedmath-1461.json", "ed4dfc88970ee46a9007a3ea57a03013fd639e89f2cd08fc440ea51c063ae297"),
    "unsolvedmath-1463": ("problems/extended-catalog/unsolvedmath/unsolvedmath-1463.json", "71f282baef47deb9d1df154a3e252b9977c2a3dec21ee7d35d9e939b52b9c77e"),
    "unsolvedmath-1464": ("problems/extended-catalog/unsolvedmath/unsolvedmath-1464.json", "82b7e1d099d190ee18d5ab8c4bf61bda933e130b23a172eac5490cfaaa5736e2"),
    "fc-bench-v1-1012": ("problems/extended-catalog/formal-conjectures/fc-bench-v1-1012.json", "4a108ad6ced4efe9db4473d7d5a0878c156c5ec2d70493e64286d28edf8a2c40"),
}

CB_OVERLAPS = {
    1: [
        ("unsolvedmath-1343", "semantically_equivalent_interrogative_occurrence", False),
        ("unsolvedmath-1461", "semantically_equivalent_interrogative_occurrence", False),
        ("fc-bench-v1-1012", "exact_formal_occurrence_same_lineage_as_parent_duplicate", True),
    ],
    5: [("unsolvedmath-1347", "semantically_equivalent_interrogative_occurrence", False)],
    6: [("unsolvedmath-1464", "semantically_equivalent_interrogative_occurrence", False)],
    13: [("unsolvedmath-1463", "semantically_equivalent_interrogative_occurrence", False)],
    14: [
        ("unsolvedmath-1220", "related_broader_stable_group_interrogative_variant", False),
        ("unsolvedmath-1344", "related_historical_omega_stable_interrogative_variant", False),
        ("unsolvedmath-1458", "related_broader_stable_group_interrogative_variant", False),
    ],
}

EVAND_COMMIT = "70e3fc1867180fe22e49062309ea2ddc06c48746"
EVAND_README_SHA256 = "ff76f0fa939ec53de67b0efc5a5e8f73186456120f766414a7d7f8dc8839e918"
EVAND_MENTIONS = {
    1: (192, "72. **Vaught's Conjecture** — model theory's white whale.", "name_only_related_mention"),
    2: (241, "109. **Martin's conjecture & rigidity of the Turing degrees** — computability theory's organizing conjecture: the only reasonable Turing-invariant functions are the transfinite jumps. Plus the companion question of whether the degree structure has any nontrivial automorphisms. The July logic section was CH and Vaught — half of logic was missing.", "informal_bundled_summary_not_complete_claim"),
    17: (241, "109. **Martin's conjecture & rigidity of the Turing degrees** — computability theory's organizing conjecture: the only reasonable Turing-invariant functions are the transfinite jumps. Plus the companion question of whether the degree structure has any nontrivial automorphisms. The July logic section was CH and Vaught — half of logic was missing.", "informal_bundled_summary_not_complete_claim"),
}


class AuditError(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AuditError(message)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def git_output(repo: Path, *args: str) -> str:
    proc = subprocess.run(
        ["git", "-C", str(repo), *args],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    return proc.stdout.strip()


def parse_scalar(raw: str) -> Any:
    value = raw.strip()
    if value.startswith('"') and value.endswith('"'):
        return json.loads(value)
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1].strip()
        return [] if not inner else [part.strip() for part in inner.split(",")]
    if value.isdigit():
        return int(value)
    return value


def parse_problem(path: Path) -> tuple[dict[str, Any], str, int, int]:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    require(lines and lines[0] == "---", f"{path}: missing opening frontmatter delimiter")
    try:
        fm_end = lines.index("---", 1)
    except ValueError as exc:
        raise AuditError(f"{path}: missing closing frontmatter delimiter") from exc

    meta: dict[str, Any] = {}
    canonical: dict[str, Any] = {}
    in_canonical = False
    for line in lines[1:fm_end]:
        if not line.strip():
            continue
        if line.startswith("  "):
            require(in_canonical, f"{path}: unexpected nested frontmatter line {line!r}")
            key, raw = line.strip().split(":", 1)
            canonical[key] = parse_scalar(raw)
            continue
        key, raw = line.split(":", 1)
        if key == "canonical_reference":
            require(not raw.strip(), f"{path}: canonical_reference must be a mapping")
            in_canonical = True
            continue
        in_canonical = False
        meta[key] = parse_scalar(raw)
    meta["canonical_reference"] = canonical

    try:
        heading_idx = lines.index("## Statement")
    except ValueError as exc:
        raise AuditError(f"{path}: missing Statement heading") from exc
    body_start = heading_idx + 1
    body_end = len(lines)
    for idx in range(body_start, len(lines)):
        if lines[idx].startswith("## "):
            body_end = idx
            break
    while body_start < body_end and not lines[body_start].strip():
        body_start += 1
    while body_end > body_start and not lines[body_end - 1].strip():
        body_end -= 1
    require(body_start < body_end, f"{path}: empty Statement section")
    statement = "\n".join(lines[body_start:body_end])
    return meta, statement, body_start + 1, body_end


def validate_source(source_repo: Path) -> dict[int, dict[str, Any]]:
    require(source_repo.is_dir(), f"missing source repository: {source_repo}")
    problem_paths = sorted((source_repo / "problems").glob("*.md"), key=lambda p: int(p.stem))
    require([path.name for path in problem_paths] == [f"{i}.md" for i in range(1, 18)], "problem files are not exactly 1.md through 17.md")

    license_path = source_repo / "CONTENT-LICENSE.md"
    snapshot_path = source_repo / "data/status-snapshot.json"
    faq_path = source_repo / "src/pages/faq.md"
    require(sha256_file(license_path) == LICENSE_SHA256, "CONTENT-LICENSE.md hash mismatch")
    require(sha256_file(snapshot_path) == STATUS_SNAPSHOT_SHA256, "status snapshot hash mismatch")
    require(sha256_file(faq_path) == FAQ_SHA256, "impact FAQ hash mismatch")
    license_text = license_path.read_text(encoding="utf-8")
    license_text_flat = " ".join(license_text.split())
    for phrase in (
        "`problems/` directory",
        "Creative Commons Attribution 4.0 International License (CC BY 4.0)",
        "give appropriate credit",
        "provide a link to the license",
        "indicate if changes were made",
        'credit "Open Problems in Mathematical Logic contributors"',
        "Canonical references cited within each problem file remain the copyright of their original authors/publishers",
    ):
        require(phrase in license_text_flat, f"license evidence phrase missing: {phrase}")
    faq_text = faq_path.read_text(encoding="utf-8")
    require("Three exclamation marks" in faq_text and "very high impact" in faq_text, "impact-3 definition missing")
    require("Two exclamation marks" in faq_text and "high impact" in faq_text, "impact-2 definition missing")
    snapshot = json.loads(snapshot_path.read_text(encoding="utf-8"))
    require(snapshot == {str(i): "open" for i in range(1, 18)}, "status snapshot is not exactly 17 open records")

    parsed: dict[int, dict[str, Any]] = {}
    seen_ids: set[int] = set()
    for path in problem_paths:
        problem_id = int(path.stem)
        require(sha256_file(path) == SOURCE_FILE_SHA256[problem_id], f"source hash mismatch for {path}")
        meta, statement, line_start, line_end = parse_problem(path)
        require(meta.get("id") == problem_id, f"frontmatter ID mismatch for {path}")
        require(problem_id not in seen_ids, f"duplicate frontmatter ID {problem_id}")
        seen_ids.add(problem_id)
        require(meta.get("name") == EXPECTED_NAMES[problem_id], f"name mismatch for problem {problem_id}")
        require(meta.get("status") == "open", f"problem {problem_id} is not source-marked open")
        require(snapshot[str(problem_id)] == "open", f"problem {problem_id} snapshot is not open")
        require(meta.get("impact") in {1, 2, 3}, f"problem {problem_id} has invalid impact")
        require(isinstance(meta.get("area"), list) and meta["area"], f"problem {problem_id} has no area")
        reference = meta.get("canonical_reference")
        require(isinstance(reference, dict), f"problem {problem_id} missing canonical reference")
        require(all(reference.get(k) not in (None, "") for k in ("title", "author", "year")), f"problem {problem_id} incomplete title/author/year")
        require(bool(reference.get("doi") or reference.get("link")), f"problem {problem_id} lacks DOI/link")
        parsed[problem_id] = {
            "meta": meta,
            "statement": statement,
            "statement_line_start": line_start,
            "statement_line_end": line_end,
        }
    require(seen_ids == set(range(1, 18)), "frontmatter IDs are not exactly 1..17")
    return parsed


def validate_parent(workspace: Path) -> dict[str, Any]:
    parent_path = workspace / PARENT_CATALOG_REL
    require(parent_path.is_file(), f"missing parent catalog: {parent_path}")
    require(sha256_file(parent_path) == PARENT_CATALOG_SHA256, "parent 5.4 catalog hash mismatch")
    catalog = json.loads(parent_path.read_text(encoding="utf-8"))
    matches = [r for r in catalog["records"] if r.get("stage_claim_id") == "S5-CLM-00005433"]
    require(len(matches) == 1, "parent Vaught target is not unique")
    row = matches[0]
    require(row.get("variant_id") == "ATV-00005433", "parent Vaught variant ID mismatch")
    require(row.get("display_name") == "VaughtConjecture.vaught_conjecture", "parent Vaught name mismatch")
    require(row.get("material_status") == "open" and row.get("current_claim_kind") == "conjecture", "parent Vaught status/kind mismatch")
    formal_type = row.get("mathematical_statement", {}).get("formal_type", "")
    natural = row.get("mathematical_statement", {}).get("natural_language", "")
    require("T.IsComplete" in formal_type and "numberOfCountableModels" in formal_type, "parent Vaught formal proposition mismatch")
    require("Vaught conjecture" in natural and "countable models" in natural, "parent Vaught natural proposition mismatch")
    return {
        "catalog_path": str(PARENT_CATALOG_REL),
        "catalog_sha256": PARENT_CATALOG_SHA256,
        "stage_claim_id": row["stage_claim_id"],
        "variant_id": row["variant_id"],
        "display_name": row["display_name"],
        "relation": "semantically_equivalent_same_Vaught_dichotomy",
        "grants_new_strict_credit": False,
    }


def validate_cross_sources(cb_repo: Path, evand_repo: Path) -> tuple[dict[str, dict[str, Any]], dict[int, dict[str, Any]]]:
    cb_rows: dict[str, dict[str, Any]] = {}
    for record_id, (relative, expected_sha) in CB_FILES.items():
        path = cb_repo / relative
        require(sha256_file(path) == expected_sha, f"ConjectureBench hash mismatch: {record_id}")
        data = json.loads(path.read_text(encoding="utf-8"))
        require(data.get("id") == record_id, f"ConjectureBench ID mismatch: {record_id}")
        statement_obj = data.get("statement", {})
        statement = statement_obj.get("text")
        require(isinstance(statement, str) and statement, f"ConjectureBench statement missing: {record_id}")
        cb_rows[record_id] = {
            "source": "ConjectureBench extended catalog",
            "source_commit": CB_COMMIT,
            "record_id": record_id,
            "path": relative,
            "file_sha256": expected_sha,
            "title": data.get("title"),
            "statement": statement,
            "statement_sha256": sha256_bytes(statement.encode("utf-8")),
            "source_form": "interrogative" if statement.rstrip().endswith("?") else "formal_declarative",
        }

    readme = evand_repo / "README.md"
    require(sha256_file(readme) == EVAND_README_SHA256, "open-math-problems README hash mismatch")
    readme_lines = readme.read_text(encoding="utf-8").splitlines()
    mentions: dict[int, dict[str, Any]] = {}
    for problem_id, (line_number, expected_text, relation) in EVAND_MENTIONS.items():
        require(readme_lines[line_number - 1] == expected_text, f"open-math-problems mention mismatch for problem {problem_id}")
        mentions[problem_id] = {
            "source": "evand/open-math-problems",
            "source_commit": EVAND_COMMIT,
            "path": "README.md",
            "file_sha256": EVAND_README_SHA256,
            "line": line_number,
            "text": expected_text,
            "relation": relation,
            "complete_truth_apt_claim": False,
            "preexisting_strict_credit": False,
        }
    return cb_rows, mentions


def importance_tier(impact: int) -> str:
    return {3: "high", 2: "medium", 1: "low"}[impact]


def build_rows(
    source_repo: Path,
    parsed: dict[int, dict[str, Any]],
    parent_target: dict[str, Any],
    cb_rows: dict[str, dict[str, Any]],
    evand_mentions: dict[int, dict[str, Any]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for problem_id in range(1, 18):
        source = parsed[problem_id]
        meta = source["meta"]
        statement = source["statement"]
        explicit = problem_id in EXACT_CLAIMS
        exact_claim = EXACT_CLAIMS.get(problem_id)
        if exact_claim is not None:
            require(exact_claim in statement, f"exact claim is not a verbatim substring for problem {problem_id}")
        else:
            require(
                "?" in statement or "This question asks whether" in statement,
                f"reviewed question-form problem {problem_id} lacks its expected interrogative cue",
            )

        decision, reason_code, review_basis = DECISIONS[problem_id]
        impact = meta["impact"]
        tier = importance_tier(impact)
        reference_review = dict(REFERENCE_REVIEW[problem_id])
        reference_review["minimum_fields_complete"] = True
        reference_review["raw_metadata_release_ready"] = not bool(reference_review["issues"])
        reference_review["verification_as_of"] = REVIEW_AS_OF
        reference_review["verification_basis"] = "source replay plus DOI/Crossref or arXiv metadata review"

        overlaps: list[dict[str, Any]] = []
        for record_id, relation, preexisting_credit in CB_OVERLAPS.get(problem_id, []):
            overlap = dict(cb_rows[record_id])
            overlap["relation"] = relation
            overlap["preexisting_strict_credit"] = preexisting_credit
            overlaps.append(overlap)
        if problem_id in evand_mentions:
            overlaps.append(dict(evand_mentions[problem_id]))

        line_start = source["statement_line_start"]
        line_end = source["statement_line_end"]
        path = f"problems/{problem_id}.md"
        row = {
            "schema_version": SCHEMA_VERSION,
            "review_as_of": REVIEW_AS_OF,
            "problem_id": problem_id,
            "name": meta["name"],
            "source": {
                "repository": SOURCE_REPOSITORY,
                "commit": SOURCE_COMMIT,
                "path": path,
                "url": f"{SOURCE_REPOSITORY}/blob/{SOURCE_COMMIT}/{path}#L{line_start}-L{line_end}",
                "file_sha256": SOURCE_FILE_SHA256[problem_id],
                "statement_line_start": line_start,
                "statement_line_end": line_end,
                "statement_sha256": sha256_bytes(statement.encode("utf-8")),
            },
            "source_statement": statement,
            "source_status": {
                "frontmatter": meta["status"],
                "snapshot": "open",
                "source_asserted_open_as_of_commit": True,
                "current_open_as_of_review": True,
                "evidence_level": "pinned_source_repository_and_status_snapshot",
            },
            "areas": meta["area"],
            "impact": impact,
            "importance_tier": tier,
            "importance_eligible": tier in {"high", "medium"},
            "importance_basis": f"Open Logic Problems impact {impact}; audit mapping 3→high, 2→medium, 1→low/below threshold.",
            "source_form": FORMS[problem_id],
            "target_component_count": TARGET_COMPONENTS.get(problem_id, 1),
            "exact_claim_text": exact_claim,
            "truth_apt": explicit,
            "context_complete": True,
            "underlying_question_well_formed": not explicit,
            "question_to_assertion_promotion_permitted": False,
            "canonical_reference": meta["canonical_reference"],
            "canonical_reference_review": reference_review,
            "rights": {
                "status": "cleared_cc_by_4_0_with_attribution",
                "license": "CC-BY-4.0",
                "license_url": "https://creativecommons.org/licenses/by/4.0/",
                "license_evidence_path": "CONTENT-LICENSE.md",
                "license_evidence_sha256": LICENSE_SHA256,
                "scope": "curated text in problems/*.md",
                "attribution": "Open Problems in Mathematical Logic contributors",
                "attribution_url": SOURCE_REPOSITORY,
                "license_link_required": True,
                "change_notice_required_if_adapted": True,
                "referenced_works_relicensed": False,
            },
            "dedupe": {
                "parent_5_4_catalog_sha256": PARENT_CATALOG_SHA256,
                "parent_semantic_review": "full_fixed_parent_reviewed",
                "parent_duplicate_targets": [parent_target] if problem_id == 1 else [],
                "within_batch": "unique",
                "other_source_overlaps": overlaps,
                "other_overlap_grants_duplicate_credit": False,
            },
            "decision": decision,
            "reason_code": reason_code,
            "review_basis": review_basis,
            "acceptance_evidence_complete": decision == "accept",
            "grants_strict_conjecture_credit": decision == "accept",
            "release_mutation_authorized_or_performed": False,
        }
        rows.append(row)

    require([r["problem_id"] for r in rows] == list(range(1, 18)), "row order/IDs mismatch")
    require({r["problem_id"] for r in rows if r["decision"] == "accept"} == {2, 4, 13, 14}, "accepted set mismatch")
    require({r["problem_id"] for r in rows if r["truth_apt"]} == {1, 2, 4, 13, 14}, "explicit-assertion set mismatch")
    for row in rows:
        if not row["truth_apt"]:
            require(row["exact_claim_text"] is None, f"question row {row['problem_id']} gained a claim")
            require(not row["grants_strict_conjecture_credit"], f"question row {row['problem_id']} gained strict credit")
        if row["grants_strict_conjecture_credit"]:
            require(row["importance_eligible"], f"accepted row {row['problem_id']} below importance threshold")
            require(row["source_status"]["current_open_as_of_review"], f"accepted row {row['problem_id']} not open")
            require(row["context_complete"], f"accepted row {row['problem_id']} incomplete")
            require(row["rights"]["status"] == "cleared_cc_by_4_0_with_attribution", f"accepted row {row['problem_id']} rights failure")
            require(row["canonical_reference_review"]["minimum_fields_complete"], f"accepted row {row['problem_id']} reference failure")
    require(rows[0]["dedupe"]["parent_duplicate_targets"][0]["stage_claim_id"] == "S5-CLM-00005433", "Vaught parent binding missing")
    require(all(not r["dedupe"]["parent_duplicate_targets"] for r in rows[1:]), "unexpected parent duplicate")
    return rows


def canonical_json_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def jsonl_bytes(rows: list[dict[str, Any]]) -> bytes:
    return b"".join(canonical_json_bytes(row) for row in rows)


def count_payload(rows: list[dict[str, Any]], artifact_sha256: str) -> dict[str, Any]:
    accepted = [r["problem_id"] for r in rows if r["decision"] == "accept"]
    rejected = [r["problem_id"] for r in rows if r["decision"] == "reject"]
    assertions = [r["problem_id"] for r in rows if r["truth_apt"]]
    questions = [r["problem_id"] for r in rows if not r["truth_apt"]]
    return {
        "schema_version": "awesome-theorems/open-logic-strict-source-review-count/1.0",
        "artifact": JSONL_NAME,
        "artifact_sha256": artifact_sha256,
        "source_commit": SOURCE_COMMIT,
        "parent_5_4_catalog_sha256": PARENT_CATALOG_SHA256,
        "counts": {
            "total": len(rows),
            "accepted": len(accepted),
            "rejected": len(rejected),
            "grants_strict_conjecture_credit": sum(bool(r["grants_strict_conjecture_credit"]) for r in rows),
            "explicit_declarative_conjecture_targets": len(assertions),
            "interrogative_open_targets": len(questions),
            "parent_semantic_duplicates": sum(bool(r["dedupe"]["parent_duplicate_targets"]) for r in rows),
            "high_importance": sum(r["importance_tier"] == "high" for r in rows),
            "medium_importance": sum(r["importance_tier"] == "medium" for r in rows),
            "low_importance": sum(r["importance_tier"] == "low" for r in rows),
            "canonical_reference_minimum_complete": sum(r["canonical_reference_review"]["minimum_fields_complete"] for r in rows),
            "canonical_reference_issue_rows": sum(bool(r["canonical_reference_review"]["issues"]) for r in rows),
            "cc_by_4_0_cleared_with_attribution": sum(r["rights"]["license"] == "CC-BY-4.0" for r in rows),
        },
        "accepted_problem_ids": accepted,
        "rejected_problem_ids": rejected,
        "explicit_assertion_problem_ids": assertions,
        "interrogative_problem_ids": questions,
        "parent_duplicate_problem_ids": [r["problem_id"] for r in rows if r["dedupe"]["parent_duplicate_targets"]],
        "release_modified": False,
    }


def write_or_validate(audit_dir: Path, rows: list[dict[str, Any]], write: bool) -> tuple[str, dict[str, Any]]:
    artifact = jsonl_bytes(rows)
    artifact_sha = sha256_bytes(artifact)
    sha_file = f"{artifact_sha}  {JSONL_NAME}\n".encode("utf-8")
    counts = count_payload(rows, artifact_sha)
    count_file = canonical_json_bytes(counts)
    expected = {
        audit_dir / JSONL_NAME: artifact,
        audit_dir / SHA_NAME: sha_file,
        audit_dir / COUNT_NAME: count_file,
    }
    if write:
        audit_dir.mkdir(parents=True, exist_ok=True)
        for path, data in expected.items():
            path.write_bytes(data)
    for path, data in expected.items():
        require(path.is_file(), f"missing audit artifact: {path}")
        actual = path.read_bytes()
        require(actual == data, f"noncanonical or stale audit artifact: {path}")
    require(sha256_file(audit_dir / JSONL_NAME) == artifact_sha, "JSONL SHA recheck failed")
    return artifact_sha, counts


def extract_fixed_archive(archive: Path, expected_sha256: str, destination: Path) -> None:
    require(archive.is_file(), f"missing fixed archive: {archive}")
    require(sha256_file(archive) == expected_sha256, f"fixed archive hash mismatch: {archive.name}")
    with tarfile.open(archive, "r:gz") as stream:
        for member in stream.getmembers():
            name = Path(member.name)
            require(not member.name.startswith("/") and ".." not in name.parts, f"unsafe archive member: {member.name}")
            target = destination / name
            if member.isdir():
                target.mkdir(parents=True, exist_ok=True)
                continue
            require(member.isfile(), f"non-regular archive member: {member.name}")
            handle = stream.extractfile(member)
            require(handle is not None, f"cannot extract archive member: {member.name}")
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(handle.read())


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-archive", type=Path, default=SOURCE_ARCHIVE_DEFAULT)
    parser.add_argument("--workspace", type=Path, default=WORKSPACE_DEFAULT)
    parser.add_argument("--conjecturebench-archive", type=Path, default=CB_ARCHIVE_DEFAULT)
    parser.add_argument("--open-math-problems-archive", type=Path, default=EVAND_ARCHIVE_DEFAULT)
    parser.add_argument("--audit-dir", type=Path, default=AUDIT_DIR_DEFAULT)
    parser.add_argument("--write", action="store_true", help="write canonical JSONL, SHA and count files before validating")
    args = parser.parse_args()

    with tempfile.TemporaryDirectory(prefix="open-logic-review-") as directory:
        temporary = Path(directory)
        source_repo = temporary / "source"
        cb_repo = temporary / "conjecturebench"
        evand_repo = temporary / "open-math-problems"
        extract_fixed_archive(args.source_archive.resolve(), SOURCE_ARCHIVE_SHA256, source_repo)
        extract_fixed_archive(args.conjecturebench_archive.resolve(), CB_ARCHIVE_SHA256, cb_repo)
        extract_fixed_archive(args.open_math_problems_archive.resolve(), EVAND_ARCHIVE_SHA256, evand_repo)
        parsed = validate_source(source_repo)
        parent_target = validate_parent(args.workspace.resolve())
        cb_rows, evand_mentions = validate_cross_sources(cb_repo, evand_repo)
        rows = build_rows(source_repo, parsed, parent_target, cb_rows, evand_mentions)
        artifact_sha, counts = write_or_validate(args.audit_dir.resolve(), rows, args.write)
    c = counts["counts"]
    print(
        "PASS open-logic-review "
        f"source={SOURCE_COMMIT} total={c['total']} accepted={c['accepted']} rejected={c['rejected']} "
        f"assertions={c['explicit_declarative_conjecture_targets']} questions={c['interrogative_open_targets']} "
        f"parent_duplicates={c['parent_semantic_duplicates']} sha256={artifact_sha}"
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (AuditError, OSError, subprocess.CalledProcessError, json.JSONDecodeError) as exc:
        print(f"FAIL open-logic-review: {exc}", file=sys.stderr)
        raise SystemExit(1)
