#!/usr/bin/env python3
"""Extract a frozen, review-oriented theorem candidate set from ``set.mm``.

This tool is deliberately narrower than a Metamath-to-catalog importer.  It
authenticates one pinned ``set.mm`` snapshot, asks an external Metamath verifier
to check every proof, parses the database itself, and emits 1,500 deterministic
``$p`` candidates for Stage5 review (1,000 in S5.0 and 500 in S5.1).

The emitted rows preserve exact formal payloads and source locators.  Selection
signals such as a Metamath-100 marker, a bibliographic reference, a named-result
word, and proof-graph usage are discovery evidence only.  They do *not* prove
that every selected row is a distinct landmark theorem, establish an MSC code,
or establish that a result is mathematically recent/frontier work.  Downstream
identity and importance review remains mandatory.

Only the Python standard library is used.  The source parser implements the
small Metamath token language directly; it does not scrape generated HTML.
"""

from __future__ import annotations

import argparse
from bisect import bisect_right
from collections import Counter, defaultdict
from dataclasses import dataclass, field
import hashlib
import json
import math
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
from typing import Any, Iterator, Mapping, Sequence


PINNED_COMMIT = "a3f307fe846353a39d3e0fcbd7af70e437825539"
PINNED_SOURCE_SHA256 = "817f3c639d806d76a981b2b8c5e3339466ddf610cbf2bff114c05ef2d1ed8c83"
PINNED_LICENSE_SHA256 = "8a5f6a2b110cdecd3543c2b18c4d17fa2f08d16ca61c1fe0a1e41b1343464b5c"
PINNED_SOURCE_SIZE = 51_128_223
PINNED_SOURCE_URL = (
    "https://raw.githubusercontent.com/metamath/set.mm/"
    f"{PINNED_COMMIT}/set.mm"
)
PINNED_REPOSITORY_URL = "https://github.com/metamath/set.mm"
PINNED_LICENSE_URL = (
    "https://github.com/metamath/set.mm/blob/"
    f"{PINNED_COMMIT}/LICENSE"
)

EXPECTED_DATABASE_STATEMENTS = 250_568
EXPECTED_A_STATEMENTS = 3_008
EXPECTED_P_STATEMENTS = 47_673
EXPECTED_MAIN_P_STATEMENTS = 30_952
EXPECTED_MATHBOX_P_STATEMENTS = 16_721

SELECTION_TOTAL = 1_500
S50_TOTAL = 1_000
S51_TOTAL = 500

SCHEMA_VERSION = "awesome-theorems/metamath-theorem-candidates/5.0"
TRANSFORM_VERSION = "metamath-setmm-extractor/1.0"

WHITESPACE = b" \t\r\n\f"
LABEL_RE = re.compile(r"^[A-Za-z0-9._-]+$")
BIBLIOGRAPHY_RE = re.compile(r"\[([A-Za-z][A-Za-z0-9_-]*)\]")
CONTRIBUTED_RE = re.compile(
    r"\(Contributed by (.+?), ([0-9]{1,2}-[A-Z][a-z]{2}-[0-9]{4})\.\)"
)
REVISED_RE = re.compile(
    r"\((?:Revised|Proof shortened) by (.+?), "
    r"([0-9]{1,2}-[A-Z][a-z]{2}-[0-9]{4})\.\)"
)
RESULT_TERM_RE = re.compile(
    r"\b(theorem|inequality|identity|formula|law|principle|criterion|"
    r"corollary|proposition|lemma)\b",
    re.IGNORECASE,
)
METAMATH_100_RE = re.compile(r"\bMetamath 100(?: proof)?\b", re.IGNORECASE)
NEW_USAGE_DISCOURAGED_RE = re.compile(
    r"\(New usage is discouraged\.\)", re.IGNORECASE
)
OBSOLETE_RE = re.compile(r"\b(obsolete|deprecated)\b", re.IGNORECASE)
INTERNAL_LEMMA_RE = re.compile(
    r"(?:^|[.!?]\s+)(?:technical\s+|auxiliary\s+|preliminary\s+)?"
    r"lemma(?:\s+[0-9]+)?\s+for\b|\bproof-internal lemma\b|"
    r"\binternal lemma\b",
    re.IGNORECASE,
)
FORM_VARIANT_RE = re.compile(
    r"\b(?:deduction|inference|closed|alternate) form\b|"
    r"\balternate (?:proof|version)\b|\bversion of\s+~\s+|"
    r"\bspecial case of\s+~\s+",
    re.IGNORECASE,
)
LIBRARY_SURFACE_RE = re.compile(
    r"^(?:Value|Closure|Domain|Range|Membership|Equality) of\b",
    re.IGNORECASE,
)
SUFFIX_VARIANT_RE = re.compile(r"(?:ALT|ALTV|OLD)$")

TIER_ORDER: Mapping[str, int] = {
    "A_metamath_100_marker": 0,
    "B_cited_named_result": 1,
    "C_named_result": 2,
    "D_cited_result": 3,
}


class ExtractionError(RuntimeError):
    """A fail-closed source, parser, verification, or selection error."""


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def canonical_json_bytes(value: Any) -> bytes:
    try:
        return json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        ).encode("utf-8")
    except (TypeError, ValueError) as exc:
        raise ExtractionError(f"value is not canonical-JSON serializable: {exc}") from exc


def pretty_json_bytes(value: Any) -> bytes:
    try:
        return (
            json.dumps(
                value,
                ensure_ascii=False,
                sort_keys=True,
                indent=2,
                allow_nan=False,
            )
            + "\n"
        ).encode("utf-8")
    except (TypeError, ValueError) as exc:
        raise ExtractionError(f"value is not JSON serializable: {exc}") from exc


def stable_digest(namespace: str, value: Any) -> str:
    return sha256_bytes(namespace.encode("utf-8") + b"\0" + canonical_json_bytes(value))


def normalized_comment(text: str) -> str:
    return " ".join(text.split())


def token_digest(tokens: Sequence[str]) -> str:
    return stable_digest("metamath-token-sequence-v1", list(tokens))


@dataclass(frozen=True)
class Lexeme:
    kind: str
    value: str
    start: int
    end: int
    inner_start: int | None = None
    inner_end: int | None = None


@dataclass(frozen=True)
class Locator:
    byte_start: int
    byte_end_exclusive: int
    line_start: int
    line_end: int

    def as_dict(self) -> dict[str, int]:
        return {
            "byte_end_exclusive": self.byte_end_exclusive,
            "byte_start": self.byte_start,
            "line_end": self.line_end,
            "line_start": self.line_start,
        }


class LineIndex:
    def __init__(self, payload: bytes) -> None:
        self._newlines = [index for index, byte in enumerate(payload) if byte == 10]

    def line_at(self, byte_offset: int) -> int:
        return bisect_right(self._newlines, byte_offset) + 1

    def locator(self, start: int, end: int) -> Locator:
        if not (0 <= start < end):
            raise ExtractionError(f"invalid source span [{start}, {end})")
        return Locator(
            byte_start=start,
            byte_end_exclusive=end,
            line_start=self.line_at(start),
            line_end=self.line_at(end - 1),
        )


def scan_metamath(payload: bytes) -> Iterator[Lexeme]:
    """Yield Metamath tokens and comments with exact byte offsets."""

    size = len(payload)
    offset = 0
    while offset < size:
        if payload[offset] in WHITESPACE:
            offset += 1
            continue
        if payload.startswith(b"$(", offset):
            close = payload.find(b"$)", offset + 2)
            if close < 0:
                raise ExtractionError(f"unterminated comment at byte {offset}")
            inner = payload[offset + 2 : close]
            try:
                text = inner.decode("utf-8")
            except UnicodeDecodeError as exc:
                raise ExtractionError(f"non-UTF-8 comment at byte {offset}: {exc}") from exc
            yield Lexeme(
                kind="comment",
                value=text,
                start=offset,
                end=close + 2,
                inner_start=offset + 2,
                inner_end=close,
            )
            offset = close + 2
            continue

        end = offset + 1
        while end < size and payload[end] not in WHITESPACE:
            end += 1
        raw = payload[offset:end]
        try:
            token = raw.decode("ascii")
        except UnicodeDecodeError as exc:
            raise ExtractionError(f"non-ASCII Metamath token at byte {offset}: {exc}") from exc
        yield Lexeme(kind="token", value=token, start=offset, end=end)
        offset = end


@dataclass(frozen=True)
class Hypothesis:
    label: str
    kind: str
    tokens: tuple[str, ...]
    source_ordinal: int
    locator: Locator

    def as_dict(self) -> dict[str, Any]:
        return {
            "formula_normalized": " ".join(self.tokens),
            "formula_tokens": list(self.tokens),
            "formula_tokens_sha256": token_digest(self.tokens),
            "kind": self.kind,
            "label": self.label,
            "source_locator": self.locator.as_dict(),
            "source_statement_ordinal": self.source_ordinal,
        }


@dataclass
class ScopeFrame:
    hypothesis_length: int
    dv_length: int
    variables: list[str] = field(default_factory=list)


@dataclass
class Candidate:
    label: str
    part: str
    source_p_ordinal: int
    source_html_ordinal: int
    source_statement_ordinal: int
    formalization_contributor: str
    formalization_date: str
    revision_events: list[dict[str, str]]
    bibliography_keys: list[str]
    result_terms: list[str]
    metamath_100_marker: bool
    comment_exact: str
    comment_normalized: str
    comment_raw_sha256: str
    comment_locator: Locator
    formula_tokens: tuple[str, ...]
    formula_source_text: str
    formula_raw_sha256: str
    formula_locator: Locator
    mandatory_hypotheses: list[Hypothesis]
    mandatory_dv_pairs: list[tuple[str, str]]
    claim_payload_sha256: str
    proof_encoding: str
    proof_token_count: int
    proof_reference_labels: list[str]
    proof_tokens_sha256: str
    proof_raw_sha256: str
    proof_locator: Locator
    statement_locator: Locator
    raw_block_locator: Locator
    raw_statement_sha256: str
    raw_block_sha256: str
    section: dict[str, Any]
    source_permalink: str
    tier: str
    tier_evidence: list[str]
    exclusion_checks: dict[str, bool]
    direct_usage_all: int = 0
    direct_usage_main: int = 0
    exact_payload_duplicate_labels: list[str] = field(default_factory=list)

    def score(self) -> int:
        term_weights = {
            "theorem": 12,
            "law": 10,
            "principle": 9,
            "criterion": 8,
            "inequality": 7,
            "identity": 6,
            "formula": 5,
            "corollary": 3,
            "proposition": 2,
            "lemma": 1,
        }
        result_score = max((term_weights.get(term, 0) for term in self.result_terms), default=0)
        usage_score = int(math.log2(self.direct_usage_main + 1) * 8)
        citation_score = min(len(self.bibliography_keys), 4) * 3
        return result_score + usage_score + citation_score

    def selection_stub(self) -> dict[str, Any]:
        return {
            "bibliography_reference_count": len(self.bibliography_keys),
            "direct_usage_all_database": self.direct_usage_all,
            "direct_usage_main_database": self.direct_usage_main,
            "result_terms": self.result_terms,
            "score": self.score(),
            "tier": self.tier,
            "tier_evidence": self.tier_evidence,
        }

    def as_selected_row(self, rank: int) -> dict[str, Any]:
        batch = "S5.0" if rank <= S50_TOTAL else "S5.1"
        candidate_key = stable_digest(
            "metamath-stage5-candidate-key-v1",
            {
                "commit": PINNED_COMMIT,
                "label": self.label,
                "payload_sha256": self.claim_payload_sha256,
            },
        )
        row: dict[str, Any] = {
            "bibliography_keys": self.bibliography_keys,
            "candidate_key": f"MM-{candidate_key[:32].upper()}",
            "claim_payload_sha256": self.claim_payload_sha256,
            "description": {
                "exact_inner_text": self.comment_exact,
                "normalized_text": self.comment_normalized,
                "raw_sha256": self.comment_raw_sha256,
                "source_locator": self.comment_locator.as_dict(),
            },
            "exact_payload_duplicate_labels": self.exact_payload_duplicate_labels,
            "formalization_metadata": {
                "contributed_by": self.formalization_contributor,
                "contribution_date": self.formalization_date,
                "date_semantics": "formalization_contribution_not_mathematical_discovery",
                "revision_events": self.revision_events,
            },
            "formal_statement": {
                "formula_normalized": " ".join(self.formula_tokens),
                "formula_raw_sha256": self.formula_raw_sha256,
                "formula_source_text": self.formula_source_text,
                "formula_tokens": list(self.formula_tokens),
                "formula_tokens_sha256": token_digest(self.formula_tokens),
                "mandatory_disjoint_variable_pairs": [
                    list(pair) for pair in self.mandatory_dv_pairs
                ],
                "mandatory_hypotheses": [
                    hypothesis.as_dict() for hypothesis in self.mandatory_hypotheses
                ],
                "source_locator": self.formula_locator.as_dict(),
            },
            "metamath_label": self.label,
            "proof": {
                "encoding": self.proof_encoding,
                "raw_sha256": self.proof_raw_sha256,
                "reference_labels": self.proof_reference_labels,
                "source_locator": self.proof_locator.as_dict(),
                "token_count": self.proof_token_count,
                "tokens_sha256": self.proof_tokens_sha256,
                "verification_scope": "verified_relative_to_active_set.mm_$a_statements",
            },
            "section": self.section,
            "selection": {
                "batch": batch,
                "evidence": self.selection_stub(),
                "frontier_status": "not_established_by_set.mm",
                "importance_status": "candidate_requires_downstream_review",
                "rank": rank,
                "semantic_uniqueness_status": "exact_payload_only_not_semantic_equivalence",
            },
            "source": {
                "commit": PINNED_COMMIT,
                "html_statement_ordinal": self.source_html_ordinal,
                "p_statement_ordinal": self.source_p_ordinal,
                "permalink": self.source_permalink,
                "raw_block_locator": self.raw_block_locator.as_dict(),
                "raw_block_sha256": self.raw_block_sha256,
                "raw_statement_sha256": self.raw_statement_sha256,
                "statement_locator": self.statement_locator.as_dict(),
                "statement_ordinal": self.source_statement_ordinal,
            },
        }
        row["row_sha256"] = sha256_bytes(canonical_json_bytes(row))
        return row


@dataclass
class ParseResult:
    candidates: list[Candidate]
    counts: dict[str, Any]
    exclusion_counts: Counter[str]
    tier_counts: Counter[str]
    part_p_counts: Counter[str]
    part_eligible_counts: Counter[str]


class MetamathParser:
    def __init__(self, payload: bytes) -> None:
        self.payload = payload
        self.lines = LineIndex(payload)
        self.events = iter(scan_metamath(payload))
        self.pending_comment: Lexeme | None = None
        self.section_levels: list[str | None] = [None, None, None, None]
        self.frames: list[ScopeFrame] = [ScopeFrame(0, 0)]
        self.active_hypotheses: list[Hypothesis] = []
        self.active_dv_pairs: list[tuple[str, str]] = []
        self.active_variable_counts: Counter[str] = Counter()
        self.labels: set[str] = set()
        self.database_statement_ordinal = 0
        self.p_ordinal = 0
        self.html_ordinal = 0
        self.a_count = 0
        self.p_count = 0
        self.main_p_count = 0
        self.mathbox_p_count = 0
        self.part_p_counts: Counter[str] = Counter()
        self.part_eligible_counts: Counter[str] = Counter()
        self.exclusion_counts: Counter[str] = Counter()
        self.tier_counts: Counter[str] = Counter()
        self.direct_usage_all: Counter[str] = Counter()
        self.direct_usage_main: Counter[str] = Counter()
        self.candidates: list[Candidate] = []
        self.comment_with_contribution_count = 0

    def _next_event(self) -> Lexeme:
        try:
            return next(self.events)
        except StopIteration as exc:
            raise ExtractionError("unexpected end of Metamath source") from exc

    def _next_token_inside_statement(self) -> Lexeme:
        while True:
            event = self._next_event()
            if event.kind == "token":
                return event

    def _tokens_until(self, terminal: str) -> tuple[list[Lexeme], Lexeme]:
        tokens: list[Lexeme] = []
        while True:
            token = self._next_token_inside_statement()
            if token.value == terminal:
                return tokens, token
            tokens.append(token)

    def _update_section(self, comment: Lexeme) -> None:
        lines = comment.value.splitlines()
        for index, raw_line in enumerate(lines):
            marker = raw_line.strip()
            level: int | None = None
            if len(marker) >= 20 and set(marker) == {"#"}:
                level = 0
            elif (
                len(marker) >= 20
                and set(marker).issubset({"#", "*"})
                and "#" in marker
                and "*" in marker
            ):
                level = 1
            elif (
                len(marker) >= 20
                and set(marker).issubset({"=", "-"})
                and "=" in marker
                and "-" in marker
            ):
                level = 2
            elif (
                len(marker) >= 20
                and set(marker).issubset({"-", "."})
                and "-" in marker
                and "." in marker
            ):
                level = 3
            if level is None:
                continue
            title: str | None = None
            for following in lines[index + 1 :]:
                stripped = following.strip()
                if stripped:
                    title = stripped
                    break
            if title is None:
                continue
            self.section_levels[level] = title
            for lower in range(level + 1, len(self.section_levels)):
                self.section_levels[lower] = None
            return

    def _section(self) -> dict[str, Any]:
        names = ("part", "section", "subsection", "subsubsection")
        result = {name: self.section_levels[index] for index, name in enumerate(names)}
        result["path"] = [value for value in self.section_levels if value is not None]
        return result

    def _part(self) -> str:
        return self.section_levels[0] or "(before first major part)"

    def _is_mathbox(self) -> bool:
        return self._part() == "SUPPLEMENTARY MATERIAL (USERS' MATHBOXES)"

    def _is_deprecated_section(self) -> bool:
        return any(
            value is not None and "(DEPRECATED)" in value
            for value in self.section_levels
        )

    def _declare_label(self, label: str) -> None:
        if LABEL_RE.fullmatch(label) is None:
            raise ExtractionError(f"invalid Metamath label {label!r}")
        if label in self.labels:
            raise ExtractionError(f"duplicate Metamath label {label!r}")
        self.labels.add(label)

    def _pop_scope(self) -> None:
        if len(self.frames) == 1:
            raise ExtractionError("unmatched $} at root scope")
        frame = self.frames.pop()
        del self.active_hypotheses[frame.hypothesis_length :]
        del self.active_dv_pairs[frame.dv_length :]
        for variable in frame.variables:
            self.active_variable_counts[variable] -= 1
            if self.active_variable_counts[variable] == 0:
                del self.active_variable_counts[variable]

    def _add_variables(self, tokens: Sequence[Lexeme]) -> None:
        if not tokens:
            raise ExtractionError("$v statement declares no variables")
        for token in tokens:
            if self.active_variable_counts[token.value]:
                raise ExtractionError(f"active variable redeclared: {token.value!r}")
            self.active_variable_counts[token.value] += 1
            self.frames[-1].variables.append(token.value)

    def _add_dv(self, tokens: Sequence[Lexeme]) -> None:
        variables = [token.value for token in tokens]
        if len(variables) < 2:
            raise ExtractionError("$d statement needs at least two variables")
        for variable in variables:
            if not self.active_variable_counts[variable]:
                raise ExtractionError(f"$d uses inactive variable {variable!r}")
        for left_index, left in enumerate(variables):
            for right in variables[left_index + 1 :]:
                pair = tuple(sorted((left, right)))
                self.active_dv_pairs.append(pair)

    def _add_hypothesis(
        self,
        label: str,
        kind: str,
        formula: Sequence[Lexeme],
        label_token: Lexeme,
        terminator: Lexeme,
    ) -> None:
        values = tuple(token.value for token in formula)
        if kind == "floating":
            if len(values) != 2:
                raise ExtractionError(f"floating hypothesis {label!r} is not two tokens")
            if not self.active_variable_counts[values[1]]:
                raise ExtractionError(
                    f"floating hypothesis {label!r} uses inactive variable {values[1]!r}"
                )
        hypothesis = Hypothesis(
            label=label,
            kind=kind,
            tokens=values,
            source_ordinal=self.database_statement_ordinal,
            locator=self.lines.locator(label_token.start, terminator.end),
        )
        self.active_hypotheses.append(hypothesis)

    def _mandatory_frame(
        self, formula_tokens: Sequence[str]
    ) -> tuple[list[Hypothesis], list[tuple[str, str]]]:
        mandatory_variables = {
            token for token in formula_tokens if self.active_variable_counts[token]
        }
        essential_hypotheses = [
            hypothesis for hypothesis in self.active_hypotheses if hypothesis.kind == "essential"
        ]
        for hypothesis in essential_hypotheses:
            mandatory_variables.update(
                token
                for token in hypothesis.tokens
                if self.active_variable_counts[token]
            )
        floating_hypotheses = [
            hypothesis
            for hypothesis in self.active_hypotheses
            if hypothesis.kind == "floating"
            and len(hypothesis.tokens) == 2
            and hypothesis.tokens[1] in mandatory_variables
        ]
        mandatory_hypotheses = sorted(
            [*floating_hypotheses, *essential_hypotheses],
            key=lambda hypothesis: hypothesis.source_ordinal,
        )
        mandatory_dv_pairs = sorted(
            {
                pair
                for pair in self.active_dv_pairs
                if pair[0] in mandatory_variables and pair[1] in mandatory_variables
            }
        )
        return mandatory_hypotheses, mandatory_dv_pairs

    @staticmethod
    def _proof_references(proof_tokens: Sequence[str]) -> tuple[str, list[str]]:
        if not proof_tokens:
            raise ExtractionError("empty proof payload")
        if "?" in proof_tokens:
            raise ExtractionError("incomplete proof marker '?' found in pinned verified source")
        if proof_tokens[0] == "(":
            try:
                closing = proof_tokens.index(")")
            except ValueError as exc:
                raise ExtractionError("compressed proof lacks closing ')' token") from exc
            references = list(proof_tokens[1:closing])
            encoding = "compressed"
        else:
            references = list(proof_tokens)
            encoding = "uncompressed"
        unique_references = list(dict.fromkeys(references))
        return encoding, unique_references

    def _candidate_tier(
        self,
        label: str,
        comment: str,
        bibliography_keys: Sequence[str],
        result_terms: Sequence[str],
        metamath_100_marker: bool,
    ) -> tuple[str | None, list[str], list[str], dict[str, bool]]:
        exclusions: list[str] = []
        checks = {
            "main_database": not self._is_mathbox(),
            "nondeprecated_section": not self._is_deprecated_section(),
            "not_discouraged": NEW_USAGE_DISCOURAGED_RE.search(comment) is None,
            "not_obsolete": OBSOLETE_RE.search(comment) is None,
            "not_internal_lemma": INTERNAL_LEMMA_RE.search(comment) is None,
            "not_form_variant": FORM_VARIANT_RE.search(comment) is None,
            "not_library_surface": LIBRARY_SURFACE_RE.search(comment) is None,
            "not_suffix_variant": SUFFIX_VARIANT_RE.search(label) is None,
        }
        reason_by_check = {
            "main_database": "mathbox",
            "nondeprecated_section": "deprecated_section",
            "not_discouraged": "new_usage_discouraged",
            "not_obsolete": "obsolete_or_deprecated_comment",
            "not_internal_lemma": "internal_lemma",
            "not_form_variant": "logical_or_alternate_form_variant",
            "not_library_surface": "library_surface_statement",
            "not_suffix_variant": "suffix_variant",
        }
        for check, passed in checks.items():
            if not passed:
                exclusions.append(reason_by_check[check])
        if exclusions:
            return None, [], exclusions, checks

        evidence = ["main_database", "nondeprecated_section"]
        if metamath_100_marker:
            evidence.append("description_marks_metamath_100")
            return "A_metamath_100_marker", evidence, [], checks
        if bibliography_keys and result_terms:
            evidence.extend(["bibliographic_reference", "named_result_term"])
            return "B_cited_named_result", evidence, [], checks
        if result_terms:
            evidence.append("named_result_term")
            return "C_named_result", evidence, [], checks
        if bibliography_keys:
            evidence.append("bibliographic_reference")
            return "D_cited_result", evidence, [], checks
        return None, [], ["no_positive_selection_signal"], checks

    def _build_candidate(
        self,
        label: str,
        label_token: Lexeme,
        keyword_token: Lexeme,
        formula_lexemes: Sequence[Lexeme],
        equals_token: Lexeme,
        proof_lexemes: Sequence[Lexeme],
        terminator: Lexeme,
        description: Lexeme,
        mandatory_hypotheses: list[Hypothesis],
        mandatory_dv_pairs: list[tuple[str, str]],
        proof_encoding: str,
        proof_references: list[str],
        tier: str,
        tier_evidence: list[str],
        exclusion_checks: dict[str, bool],
    ) -> Candidate:
        if description.inner_start is None or description.inner_end is None:
            raise ExtractionError(f"description offsets missing for {label}")
        comment_raw = self.payload[description.inner_start : description.inner_end]
        comment_exact = comment_raw.decode("utf-8")
        comment_normalized = normalized_comment(comment_exact)
        contribution = CONTRIBUTED_RE.search(comment_normalized)
        if contribution is None:
            raise ExtractionError(f"selected theorem {label!r} lacks contribution metadata")
        revisions = [
            {"contributor": match.group(1), "date": match.group(2)}
            for match in REVISED_RE.finditer(comment_normalized)
        ]
        bibliography_keys = sorted(set(BIBLIOGRAPHY_RE.findall(comment_normalized)))
        result_terms = sorted(
            {match.group(1).lower() for match in RESULT_TERM_RE.finditer(comment_normalized)}
        )
        formula_tokens = tuple(token.value for token in formula_lexemes)
        proof_tokens = tuple(token.value for token in proof_lexemes)
        formula_start = keyword_token.end
        formula_end = equals_token.start
        proof_start = equals_token.end
        proof_end = terminator.start
        formula_raw = self.payload[formula_start:formula_end]
        proof_raw = self.payload[proof_start:proof_end]
        statement_raw = self.payload[label_token.start : terminator.end]
        raw_block = self.payload[description.start : terminator.end]
        payload_body = {
            "assertion_tokens": list(formula_tokens),
            "mandatory_disjoint_variable_pairs": [list(pair) for pair in mandatory_dv_pairs],
            "mandatory_hypotheses": [
                {"kind": hypothesis.kind, "tokens": list(hypothesis.tokens)}
                for hypothesis in mandatory_hypotheses
            ],
        }
        statement_locator = self.lines.locator(label_token.start, terminator.end)
        line_start = statement_locator.line_start
        line_end = statement_locator.line_end
        source_permalink = (
            "https://github.com/metamath/set.mm/blob/"
            f"{PINNED_COMMIT}/set.mm#L{line_start}-L{line_end}"
        )
        return Candidate(
            label=label,
            part=self._part(),
            source_p_ordinal=self.p_ordinal,
            source_html_ordinal=self.html_ordinal,
            source_statement_ordinal=self.database_statement_ordinal,
            formalization_contributor=contribution.group(1),
            formalization_date=contribution.group(2),
            revision_events=revisions,
            bibliography_keys=bibliography_keys,
            result_terms=result_terms,
            metamath_100_marker=METAMATH_100_RE.search(comment_normalized) is not None,
            comment_exact=comment_exact,
            comment_normalized=comment_normalized,
            comment_raw_sha256=sha256_bytes(comment_raw),
            comment_locator=self.lines.locator(description.start, description.end),
            formula_tokens=formula_tokens,
            formula_source_text=formula_raw.decode("ascii"),
            formula_raw_sha256=sha256_bytes(formula_raw),
            formula_locator=self.lines.locator(formula_start, formula_end),
            mandatory_hypotheses=mandatory_hypotheses,
            mandatory_dv_pairs=mandatory_dv_pairs,
            claim_payload_sha256=stable_digest(
                "metamath-exact-claim-payload-v1", payload_body
            ),
            proof_encoding=proof_encoding,
            proof_token_count=len(proof_tokens),
            proof_reference_labels=proof_references,
            proof_tokens_sha256=token_digest(proof_tokens),
            proof_raw_sha256=sha256_bytes(proof_raw),
            proof_locator=self.lines.locator(proof_start, proof_end),
            statement_locator=statement_locator,
            raw_block_locator=self.lines.locator(description.start, terminator.end),
            raw_statement_sha256=sha256_bytes(statement_raw),
            raw_block_sha256=sha256_bytes(raw_block),
            section=self._section(),
            source_permalink=source_permalink,
            tier=tier,
            tier_evidence=tier_evidence,
            exclusion_checks=exclusion_checks,
        )

    def _parse_labelled_statement(
        self, label_token: Lexeme, description: Lexeme | None
    ) -> None:
        label = label_token.value
        keyword = self._next_token_inside_statement()
        if keyword.value not in {"$f", "$e", "$a", "$p"}:
            raise ExtractionError(
                f"label {label!r} at byte {label_token.start} is followed by {keyword.value!r}"
            )
        self._declare_label(label)
        self.database_statement_ordinal += 1

        if keyword.value in {"$f", "$e", "$a"}:
            formula, terminator = self._tokens_until("$.")
            if not formula:
                raise ExtractionError(f"empty {keyword.value} statement {label!r}")
            if keyword.value == "$f":
                self._add_hypothesis(label, "floating", formula, label_token, terminator)
            elif keyword.value == "$e":
                self._add_hypothesis(label, "essential", formula, label_token, terminator)
            else:
                self.a_count += 1
                self.html_ordinal += 1
            return

        formula, equals = self._tokens_until("$=")
        proof, terminator = self._tokens_until("$.")
        if not formula:
            raise ExtractionError(f"empty $p formula for {label!r}")
        self.p_count += 1
        self.p_ordinal += 1
        self.html_ordinal += 1
        part = self._part()
        self.part_p_counts[part] += 1
        if self._is_mathbox():
            self.mathbox_p_count += 1
        else:
            self.main_p_count += 1

        formula_values = tuple(token.value for token in formula)
        mandatory_hypotheses, mandatory_dv_pairs = self._mandatory_frame(formula_values)
        proof_values = tuple(token.value for token in proof)
        proof_encoding, proof_references = self._proof_references(proof_values)
        for reference in proof_references:
            self.direct_usage_all[reference] += 1
            if not self._is_mathbox():
                self.direct_usage_main[reference] += 1

        if description is None:
            raise ExtractionError(f"$p statement {label!r} lacks an immediate description comment")
        comment = normalized_comment(description.value)
        if CONTRIBUTED_RE.search(comment):
            self.comment_with_contribution_count += 1
        bibliography_keys = sorted(set(BIBLIOGRAPHY_RE.findall(comment)))
        result_terms = sorted(
            {match.group(1).lower() for match in RESULT_TERM_RE.finditer(comment)}
        )
        marker = METAMATH_100_RE.search(comment) is not None
        tier, evidence, exclusions, checks = self._candidate_tier(
            label,
            comment,
            bibliography_keys,
            result_terms,
            marker,
        )
        if tier is None:
            for reason in exclusions:
                self.exclusion_counts[reason] += 1
            return
        self.tier_counts[tier] += 1
        self.part_eligible_counts[part] += 1
        candidate = self._build_candidate(
            label=label,
            label_token=label_token,
            keyword_token=keyword,
            formula_lexemes=formula,
            equals_token=equals,
            proof_lexemes=proof,
            terminator=terminator,
            description=description,
            mandatory_hypotheses=mandatory_hypotheses,
            mandatory_dv_pairs=mandatory_dv_pairs,
            proof_encoding=proof_encoding,
            proof_references=proof_references,
            tier=tier,
            tier_evidence=evidence,
            exclusion_checks=checks,
        )
        self.candidates.append(candidate)

    def parse(self) -> ParseResult:
        for event in self.events:
            if event.kind == "comment":
                self._update_section(event)
                self.pending_comment = event
                continue

            token = event.value
            description = self.pending_comment
            self.pending_comment = None
            if token == "${":
                # Metamath's displayed statement ordinal counts both scope
                # delimiters as statements.  Keeping the same ordinal makes a
                # row directly comparable with SHOW STATEMENT ... / FULL.
                self.database_statement_ordinal += 1
                self.frames.append(
                    ScopeFrame(len(self.active_hypotheses), len(self.active_dv_pairs))
                )
                continue
            if token == "$}":
                self.database_statement_ordinal += 1
                self._pop_scope()
                continue
            if token in {"$c", "$v", "$d"}:
                values, _terminator = self._tokens_until("$.")
                self.database_statement_ordinal += 1
                if token == "$v":
                    self._add_variables(values)
                elif token == "$d":
                    self._add_dv(values)
                elif not values:
                    raise ExtractionError("$c statement declares no constants")
                continue
            if token == "$[":
                raise ExtractionError(
                    "real $[ include directives are unsupported; use the canonical merged set.mm"
                )
            if token.startswith("$"):
                raise ExtractionError(
                    f"unexpected top-level token {token!r} at byte {event.start}"
                )
            self._parse_labelled_statement(event, description)

        if len(self.frames) != 1:
            raise ExtractionError(f"unclosed Metamath scopes: {len(self.frames) - 1}")
        if self.a_count != EXPECTED_A_STATEMENTS:
            raise ExtractionError(
                f"$a count drift: expected {EXPECTED_A_STATEMENTS}, parsed {self.a_count}"
            )
        if self.p_count != EXPECTED_P_STATEMENTS:
            raise ExtractionError(
                f"$p count drift: expected {EXPECTED_P_STATEMENTS}, parsed {self.p_count}"
            )
        if self.main_p_count != EXPECTED_MAIN_P_STATEMENTS:
            raise ExtractionError(
                "main $p count drift: expected "
                f"{EXPECTED_MAIN_P_STATEMENTS}, parsed {self.main_p_count}"
            )
        if self.mathbox_p_count != EXPECTED_MATHBOX_P_STATEMENTS:
            raise ExtractionError(
                "mathbox $p count drift: expected "
                f"{EXPECTED_MATHBOX_P_STATEMENTS}, parsed {self.mathbox_p_count}"
            )
        if self.comment_with_contribution_count != EXPECTED_P_STATEMENTS:
            raise ExtractionError(
                "not every $p has recognized contribution metadata: "
                f"{self.comment_with_contribution_count}/{EXPECTED_P_STATEMENTS}"
            )
        if self.database_statement_ordinal != EXPECTED_DATABASE_STATEMENTS:
            raise ExtractionError(
                "database statement count drift: expected "
                f"{EXPECTED_DATABASE_STATEMENTS}, parsed {self.database_statement_ordinal}"
            )
        for candidate in self.candidates:
            candidate.direct_usage_all = self.direct_usage_all[candidate.label]
            candidate.direct_usage_main = self.direct_usage_main[candidate.label]

        counts = {
            "a_statements": self.a_count,
            "a_plus_p_statements": self.a_count + self.p_count,
            "comments_with_recognized_contribution_metadata": (
                self.comment_with_contribution_count
            ),
            "database_statement_ordinal_count": self.database_statement_ordinal,
            "main_p_statements": self.main_p_count,
            "mathbox_p_statements_including_boundary_dummy": self.mathbox_p_count,
            "p_statements": self.p_count,
        }
        return ParseResult(
            candidates=self.candidates,
            counts=counts,
            exclusion_counts=self.exclusion_counts,
            tier_counts=self.tier_counts,
            part_p_counts=self.part_p_counts,
            part_eligible_counts=self.part_eligible_counts,
        )


def verify_source_and_license(source: Path, license_path: Path) -> tuple[bytes, bytes]:
    try:
        source_payload = source.read_bytes()
    except OSError as exc:
        raise ExtractionError(f"cannot read pinned set.mm source {source}: {exc}") from exc
    try:
        license_payload = license_path.read_bytes()
    except OSError as exc:
        raise ExtractionError(f"cannot read pinned license {license_path}: {exc}") from exc
    if len(source_payload) != PINNED_SOURCE_SIZE:
        raise ExtractionError(
            f"set.mm size drift: expected {PINNED_SOURCE_SIZE}, got {len(source_payload)}"
        )
    source_sha = sha256_bytes(source_payload)
    if source_sha != PINNED_SOURCE_SHA256:
        raise ExtractionError(
            f"set.mm SHA-256 mismatch: expected {PINNED_SOURCE_SHA256}, got {source_sha}"
        )
    license_sha = sha256_bytes(license_payload)
    if license_sha != PINNED_LICENSE_SHA256:
        raise ExtractionError(
            f"LICENSE SHA-256 mismatch: expected {PINNED_LICENSE_SHA256}, got {license_sha}"
        )
    if b"CC0 1.0 Universal" not in license_payload:
        raise ExtractionError("pinned LICENSE no longer identifies CC0 1.0 Universal")
    source_head = source_payload[:4096]
    if b"PUBLIC DOMAIN" not in source_head or b"CC0" not in source_head:
        raise ExtractionError("set.mm header lacks the expected public-domain/CC0 notice")
    return source_payload, license_payload


def run_proof_verification(metamath_bin: Path, source: Path) -> dict[str, Any]:
    if not metamath_bin.is_file():
        raise ExtractionError(f"Metamath verifier is not a file: {metamath_bin}")
    resolved_source = source.resolve()
    source_text = str(resolved_source)
    if any(character in source_text for character in {'"', "\n", "\r"}):
        raise ExtractionError("source path contains characters unsafe for Metamath command input")
    try:
        completed = subprocess.run(
            [
                str(metamath_bin.resolve()),
                f'read "{source_text}"',
                "verify proof *",
                "quit",
            ],
            cwd=str(source.parent.resolve()),
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=300,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        raise ExtractionError(f"failed to execute Metamath verifier: {exc}") from exc
    output = completed.stdout.decode("utf-8", errors="replace")
    count_match = re.search(
        r"The source has ([0-9]+) statements; ([0-9]+) are \$a and "
        r"([0-9]+) are \$p\.",
        output,
    )
    if completed.returncode != 0:
        raise ExtractionError(
            f"Metamath verifier exited {completed.returncode}:\n{output[-4000:]}"
        )
    if count_match is None:
        raise ExtractionError(f"Metamath verifier did not report source counts:\n{output[-4000:]}")
    reported = tuple(int(count_match.group(index)) for index in range(1, 4))
    expected = (
        EXPECTED_DATABASE_STATEMENTS,
        EXPECTED_A_STATEMENTS,
        EXPECTED_P_STATEMENTS,
    )
    if reported != expected:
        raise ExtractionError(
            f"Metamath verifier count drift: expected {expected}, reported {reported}"
        )
    if "All proofs in the database were verified" not in output:
        raise ExtractionError(f"Metamath verifier did not verify every proof:\n{output[-4000:]}")
    return {
        "a_statements": reported[1],
        "command": "VERIFY PROOF *",
        "database_statements": reported[0],
        "p_statements": reported[2],
        "result": "pass",
        "verifier_family": "metamath-exe",
    }


def deduplicate_exact_payloads(
    candidates: Sequence[Candidate],
) -> tuple[list[Candidate], dict[str, list[str]]]:
    grouped: dict[str, list[Candidate]] = defaultdict(list)
    for candidate in candidates:
        grouped[candidate.claim_payload_sha256].append(candidate)
    representatives: list[Candidate] = []
    duplicates: dict[str, list[str]] = {}
    for payload_sha, rows in grouped.items():
        ordered = sorted(
            rows,
            key=lambda row: (
                TIER_ORDER[row.tier],
                -row.score(),
                row.source_p_ordinal,
                row.label,
            ),
        )
        representative = ordered[0]
        duplicate_labels = sorted(row.label for row in ordered[1:])
        representative.exact_payload_duplicate_labels = duplicate_labels
        representatives.append(representative)
        if duplicate_labels:
            duplicates[payload_sha] = [representative.label, *duplicate_labels]
    return representatives, duplicates


def round_robin_by_part(candidates: Sequence[Candidate]) -> list[Candidate]:
    by_part: dict[str, list[Candidate]] = defaultdict(list)
    part_first_ordinal: dict[str, int] = {}
    for candidate in candidates:
        by_part[candidate.part].append(candidate)
        part_first_ordinal[candidate.part] = min(
            part_first_ordinal.get(candidate.part, candidate.source_p_ordinal),
            candidate.source_p_ordinal,
        )
    for rows in by_part.values():
        rows.sort(key=lambda row: (-row.score(), row.source_p_ordinal, row.label))
    part_order = sorted(by_part, key=lambda part: (part_first_ordinal[part], part))
    positions = {part: 0 for part in part_order}
    result: list[Candidate] = []
    while True:
        emitted = False
        for part in part_order:
            position = positions[part]
            rows = by_part[part]
            if position >= len(rows):
                continue
            result.append(rows[position])
            positions[part] = position + 1
            emitted = True
        if not emitted:
            return result


def select_candidates(
    candidates: Sequence[Candidate],
) -> tuple[list[Candidate], dict[str, Any]]:
    representatives, duplicate_groups = deduplicate_exact_payloads(candidates)
    selected: list[Candidate] = []
    selected_keys: set[tuple[str, str]] = set()
    tier_available: Counter[str] = Counter(row.tier for row in representatives)
    tier_selected: Counter[str] = Counter()
    for tier in sorted(TIER_ORDER, key=TIER_ORDER.__getitem__):
        tier_rows = [row for row in representatives if row.tier == tier]
        for row in round_robin_by_part(tier_rows):
            key = (row.label, row.claim_payload_sha256)
            if key in selected_keys:
                raise ExtractionError(f"selection duplicated {row.label}")
            selected.append(row)
            selected_keys.add(key)
            tier_selected[tier] += 1
            if len(selected) == SELECTION_TOTAL:
                break
        if len(selected) == SELECTION_TOTAL:
            break
    if len(selected) != SELECTION_TOTAL:
        raise ExtractionError(
            f"only {len(selected)} eligible unique payloads; need {SELECTION_TOTAL}"
        )
    if S50_TOTAL + S51_TOTAL != SELECTION_TOTAL:
        raise ExtractionError("selection batch constants do not sum to total")
    part_selected = Counter(row.part for row in selected)
    policy_counts = {
        "eligible_before_exact_payload_deduplication": len(candidates),
        "eligible_exact_payload_duplicate_groups": len(duplicate_groups),
        "eligible_unique_exact_payloads": len(representatives),
        "selected_by_part": dict(sorted(part_selected.items())),
        "selected_by_tier": dict(sorted(tier_selected.items())),
        "tier_available_after_exact_payload_deduplication": dict(
            sorted(tier_available.items())
        ),
    }
    return selected, policy_counts


def build_document(
    source: Path,
    source_payload: bytes,
    license_payload: bytes,
    verification: Mapping[str, Any],
) -> dict[str, Any]:
    parsed = MetamathParser(source_payload).parse()
    selected, selection_counts = select_candidates(parsed.candidates)
    rows = [candidate.as_selected_row(rank) for rank, candidate in enumerate(selected, 1)]
    batch_counts = Counter(row["selection"]["batch"] for row in rows)
    if batch_counts != Counter({"S5.0": S50_TOTAL, "S5.1": S51_TOTAL}):
        raise ExtractionError(f"selection batch count drift: {dict(batch_counts)}")
    if len({row["candidate_key"] for row in rows}) != len(rows):
        raise ExtractionError("candidate keys are not unique")
    if len({row["metamath_label"] for row in rows}) != len(rows):
        raise ExtractionError("selected Metamath labels are not unique")

    body: dict[str, Any] = {
        "artifact": "Metamath_Theorem_Candidates_v5.json",
        "counts": {
            **parsed.counts,
            **selection_counts,
            "selected_rows": len(rows),
            "selection_batches": dict(sorted(batch_counts.items())),
        },
        "limitations": {
            "blanket_landmark_claim": False,
            "embedded_third_party_quote_rights_cleared": False,
            "frontier_status_established": False,
            "msc_mapping_established": False,
            "semantic_deduplication_established": False,
            "statement": (
                "Rows are deterministic, formally verified source candidates. "
                "Selection signals do not establish that every row is an independent "
                "landmark, a frontier result, or semantically unique."
            ),
        },
        "parser": {
            "language": "Metamath",
            "source_transform_version": TRANSFORM_VERSION,
            "statement_kind_included": "$p",
            "statement_kinds_excluded": ["$a", "$c", "$d", "$e", "$f", "$v"],
        },
        "proof_verification": dict(verification),
        "schema_version": SCHEMA_VERSION,
        "selection_policy": {
            "batch_policy": {
                "S5.0": S50_TOTAL,
                "S5.1": S51_TOTAL,
            },
            "discovery_only": True,
            "exact_payload_deduplication": True,
            "exclusion_counts": dict(sorted(parsed.exclusion_counts.items())),
            "exclusions": [
                "user mathboxes",
                "deprecated sections",
                "comments marked new-usage-discouraged, obsolete, or deprecated",
                "internal helper lemmas",
                "deduction/inference/closed/alternate-form variants",
                "value/closure/domain/range/membership/equality library surfaces",
                "ALT, ALTV, and OLD label suffix variants",
            ],
            "part_eligible_counts_before_exact_payload_deduplication": dict(
                sorted(parsed.part_eligible_counts.items())
            ),
            "part_p_statement_counts": dict(sorted(parsed.part_p_counts.items())),
            "ranking": (
                "tier order, then deterministic round-robin across major parts; "
                "within each part: named-result weight, log-scaled direct main-database "
                "usage, bibliography count, source ordinal, label"
            ),
            "tier_definitions": {
                "A_metamath_100_marker": (
                    "the pinned set.mm description explicitly mentions Metamath 100"
                ),
                "B_cited_named_result": (
                    "the description has a bracketed bibliography key and a named-result term"
                ),
                "C_named_result": "the description has a named-result term",
                "D_cited_result": "the description has a bracketed bibliography key",
            },
            "tier_eligible_counts_before_exact_payload_deduplication": dict(
                sorted(parsed.tier_counts.items())
            ),
        },
        "source": {
            "access_model": "commit-pinned_git_snapshot",
            "commit": PINNED_COMMIT,
            "database_path": "set.mm",
            "database_sha256": sha256_bytes(source_payload),
            "database_size_bytes": len(source_payload),
            "input_path_for_this_run": str(source.resolve()),
            "license": "CC0-1.0",
            "license_path": "LICENSE",
            "license_sha256": sha256_bytes(license_payload),
            "license_scope_note": (
                "The repository and set.mm declare CC0.  The CC0 disclaimer does not "
                "clear rights in third-party material quoted inside descriptions; "
                "field-level rights review remains required before republication."
            ),
            "license_url": PINNED_LICENSE_URL,
            "repository_url": PINNED_REPOSITORY_URL,
            "source_url": PINNED_SOURCE_URL,
        },
        "stage": "Stage5",
        "rows": rows,
    }
    # Local absolute input paths are operational metadata and would make the
    # artifact machine-dependent.  Keep them out of the sealed authority.
    body["source"].pop("input_path_for_this_run")
    body["authority_sha256"] = sha256_bytes(canonical_json_bytes(body))
    return body


def atomic_write(path: Path, payload: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.", suffix=".tmp", dir=str(path.parent)
    )
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary_name, path)
    except BaseException:
        try:
            os.unlink(temporary_name)
        except FileNotFoundError:
            pass
        raise


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", required=True, type=Path, help="pinned set.mm path")
    parser.add_argument("--license", required=True, type=Path, help="pinned LICENSE path")
    parser.add_argument(
        "--metamath-bin",
        required=True,
        type=Path,
        help="metamath-exe binary used for VERIFY PROOF *",
    )
    parser.add_argument("--output", required=True, type=Path, help="output JSON path")
    parser.add_argument(
        "--check",
        action="store_true",
        help="compare with --output and perform no writes",
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    try:
        source_payload, license_payload = verify_source_and_license(
            args.source, args.license
        )
        verification = run_proof_verification(args.metamath_bin, args.source)
        document = build_document(
            args.source,
            source_payload,
            license_payload,
            verification,
        )
        expected = pretty_json_bytes(document)
        if args.check:
            try:
                actual = args.output.read_bytes()
            except OSError as exc:
                raise ExtractionError(f"cannot read check target {args.output}: {exc}") from exc
            if actual != expected:
                raise ExtractionError(
                    f"check target differs from deterministic extraction: {args.output}"
                )
            print(
                f"PASS: {args.output} ({len(document['rows'])} rows, "
                f"authority {document['authority_sha256']})"
            )
            return 0
        atomic_write(args.output, expected)
        print(
            f"WROTE: {args.output} ({len(document['rows'])} rows, "
            f"authority {document['authority_sha256']})"
        )
        return 0
    except ExtractionError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
