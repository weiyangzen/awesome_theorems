#!/usr/bin/env python3
"""Build the fixed-source existing-entry theorem review for indices 67..133.

The output is a quality-only review of already allocated landmark identities.  It
cannot append a catalog row or grant a new theorem/conjecture inventory credit.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
from pathlib import Path


REPO = Path(__file__).resolve().parents[4]
AUDIT = REPO / "Docs/catalog/v5/curation/theorem_quality_v5_5"
LEDGER = AUDIT / "landmark-ledger-0-1199.json"
WIKIPEDIA = REPO / "Docs/catalog/v5/sources/wikipedia-en-1000-plus-revisions-20260810.json.gz"
REFERENCES = REPO / "Docs/catalog/v5/curation/Thousand_Plus_Reference_Candidates_v5_5.json"
OPENALEX = REPO / "Docs/catalog/v5/sources/openalex-thousand-plus-doi-metadata-20260810.json.gz"
OUTPUT = AUDIT / "reviews/wiki-reference-review-067-133.json"

RELEASE_SENTINELS = {
    REPO / "Docs/catalog/v5/Current_Release.json":
        "261f27d39f379a879ea0fcacbab9e3c43dc5be8d83ea56473b2e8b4e6c384795",
    REPO / "Docs/catalog/v5/releases/5.4/Release_Manifest.json":
        "8cc6a2b5d4f94861eedbf31c76026e08191595c2927ba253cdae3b26d9a8edc9",
    REPO / "Docs/catalog/v5/releases/5.4/Claim_Catalog.json":
        "384c1e34a57443dafe2e2ce70e36d6a6e23c6d03e006171b94aa2defa92e9709",
    REPO / "Docs/catalog/v5/releases/5.4/Strict_Conjecture_Ledger.json":
        "52ba1ccf06462741bcc48028fb121e5e30d1e7b56128cfeb910dc56a2e1a83a3",
}

FIXED_INPUT_SHA256 = {
    LEDGER: "51c5607cd4289f8340745879b8b134673bbd44e873cebc82e2da59f0ba6c1471",
    WIKIPEDIA: "73341aebcc1d9d1c577881d2c6d59734ce102d7cc07b1f8ec6d21c9875076d33",
    REFERENCES: "f86b87afcffbf120d2f3cf0ff8860e7c925e8f9fa514db3714936e3cfa100435",
    OPENALEX: "e3d490619eac4e16bdf24478c74de2024d32d3ec0d603f3ac4a102ad4c206486",
}
LEDGER_AUTHORITY_SHA256 = "2cc91efdcbd604f46fd7a4f59ca9f19b25a74fdabd5e829fc7a6c50e5c7bf844"
REFERENCE_AUTHORITY_SHA256 = "d428f5659c242fa66c3e78f5497013ea1b6eaf13a4558c4f15e6c0af005acc42"
OPENALEX_AUTHORITY_SHA256 = "4a6abb7d9f22dbca688eed164116b429beacb15a643465bf424f41d0e0e3f565"

EXPECTED_PENDING = [
    69, 70, 71, 72, 73, 74, 75, 76, 79, 80, 82, 84, 85, 87, 88, 89,
    90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 104, 105, 106,
    107, 108, 109, 110, 112, 115, 117, 118, 119, 120, 121, 122, 123,
    124, 125, 126, 127, 128, 129, 132, 133,
]


def eligible_extract(
    *, reference_kind: str, reference_id: str, completeness: str,
    reference_rationale: str,
) -> dict:
    return {
        "source_field": "extract",
        "full_field": True,
        "start": None,
        "end": None,
        "end_before": None,
        "reference_kind": reference_kind,
        "reference_id": reference_id,
        "completeness": completeness,
        "reference_rationale": reference_rationale,
    }


def eligible_passage(
    start: str, *, end: str | None = None, end_before: str | None = None,
    reference_kind: str, reference_id: str, completeness: str,
    reference_rationale: str,
) -> dict:
    return {
        "source_field": "wikitext",
        "full_field": False,
        "start": start,
        "end": end,
        "end_before": end_before,
        "reference_kind": reference_kind,
        "reference_id": reference_id,
        "completeness": completeness,
        "reference_rationale": reference_rationale,
    }


ELIGIBLE_SPECS = {
    69: eligible_extract(
        reference_kind="doi", reference_id="10.1007/bf01448439",
        completeness="The pinned introduction fixes finite-dimensional unital real algebras, the positive-definite multiplicative quadratic-form hypothesis, and the four possible isomorphism classes.",
        reference_rationale="Hurwitz's posthumous paper on composition of quadratic forms is the fixed original source named by the page and directly matches the composition-algebra classification.",
    ),
    75: eligible_extract(
        reference_kind="doi", reference_id="10.1007/bf01456931",
        completeness="The pinned introduction states continuity, nonempty compact convex domain, self-map, and existence of a fixed point.",
        reference_rationale="Brouwer's 1911 paper is the fixed original source cited for the general continuous-mapping result.",
    ),
    76: eligible_extract(
        reference_kind="isbn", reference_id="9780387946566",
        completeness="The pinned introduction states the universal polygonal-number representation with the exact number of allowed summands and defines the polygonal numbers in scope.",
        reference_rationale="The fixed Nathanson volume is explicitly annotated as containing proofs of the polygonal number theorem.",
    ),
    79: eligible_extract(
        reference_kind="doi", reference_id="10.2307/2268019",
        completeness="The pinned introduction states that every Goodstein sequence terminates at zero and identifies the arithmetic independence context.",
        reference_rationale="Goodstein's fixed 1944 paper 'On the restricted ordinal theorem' is the original theorem source listed on the page.",
    ),
    80: eligible_extract(
        reference_kind="doi", reference_id="10.1112/blms/14.4.285",
        completeness="The pinned introduction states the Kirby--Paris result that Goodstein termination is unprovable in Peano arithmetic while provable in stronger systems.",
        reference_rationale="Kirby and Paris's fixed paper 'Accessible Independence Results for Peano Arithmetic' directly matches the selected independence result.",
    ),
    82: eligible_extract(
        reference_kind="isbn", reference_id="9780071072595",
        completeness="The pinned introduction fixes three coplanar concurrent non-collinear equilibrium forces and states the complete sine-ratio identity with the opposite angles.",
        reference_rationale="The fixed Engineering Mechanics citation is attached inline to the variables and angles in the exact theorem statement.",
    ),
    84: eligible_extract(
        reference_kind="doi", reference_id="10.1080/00029890.1994.11997027",
        completeness="The pinned introduction states that every compass-and-straightedge point/circle construction can be performed with a compass alone and explains the line convention.",
        reference_rationale="Hungerbuehler's fixed article is explicitly titled 'A Short Elementary Proof of the Mohr--Mascheroni Theorem'.",
    ),
    85: eligible_extract(
        reference_kind="doi", reference_id="10.1103/physrev.127.965",
        completeness="The pinned introduction and theorem passage state continuous spontaneous symmetry breaking and the necessary massless scalar excitation conclusion.",
        reference_rationale="Goldstone, Salam and Weinberg's fixed 'Broken Symmetries' paper is the theorem's systematic quantum-field-theory source.",
    ),
    88: eligible_extract(
        reference_kind="doi", reference_id="10.2307/1989664",
        completeness="The pinned introduction states that every Boolean algebra is isomorphic to a field of sets and identifies the representing Stone space.",
        reference_rationale="Stone's fixed 1936 paper 'The Theory of Representations of Boolean Algebras' is the original exact source.",
    ),
    89: eligible_extract(
        reference_kind="doi", reference_id="10.2307/1969302",
        completeness="The pinned introduction gives the closed even-dimensional Riemannian-manifold hypothesis and equates the Euler characteristic with the curvature integral.",
        reference_rationale="Chern's fixed paper is explicitly titled 'A Simple Intrinsic Proof of the Gauss-Bonnet Formula for Closed Riemannian Manifolds'.",
    ),
    91: eligible_extract(
        reference_kind="doi", reference_id="10.2307/3666323",
        completeness="The pinned introduction states the no-tax/no-friction efficient-market hypotheses and the invariance of enterprise value under financing choice.",
        reference_rationale="Titman's fixed theorem-specific article directly reviews the Modigliani--Miller result and its financial-market scope.",
    ),
    93: eligible_extract(
        reference_kind="doi", reference_id="10.1007/bf02564296",
        completeness="The pinned introduction states that integration induces an isomorphism from de Rham cohomology to singular cohomology.",
        reference_rationale="Weil's fixed article 'Sur les théorèmes de de Rham' is theorem-specific and directly matches the selected cohomological comparison.",
    ),
    96: eligible_passage(
        "== Statement ==\nFor non-negative", end_before="\n\n== Proofs ==",
        reference_kind="doi", reference_id="10.2307/2369308",
        completeness="The statement section fixes base-p expansions of m and n and gives the exact digitwise binomial congruence modulo p.",
        reference_rationale="Lucas's fixed 1878 first paper in the cited series is the original source for the digitwise binomial congruence.",
    ),
    97: eligible_passage(
        "== Group-theoretic version ==", end_before="\n\n== Proof ==",
        reference_kind="isbn", reference_id="9780486142135",
        completeness="The section fixes groups G and H, a homomorphism, a normal subgroup contained in its kernel, the unique quotient factorization, and the first-isomorphism consequence.",
        reference_rationale="Grove's fixed Algebra citation identifies Theorem 1.11 by the exact name 'The Fundamental Homomorphism Theorem' and is a group-algebra source.",
    ),
    98: eligible_extract(
        reference_kind="isbn", reference_id="9780486458038",
        completeness="The pinned introduction states that every planar curve of constant width has perimeter pi times that width.",
        reference_rationale="The fixed Lay citation binds this result to Theorem 11.11 on pages 81--82.",
    ),
    99: eligible_extract(
        reference_kind="doi", reference_id="10.1215/kjm/1250524859",
        completeness="The pinned introduction states the separated finite-type morphism to a Noetherian scheme and its factorization as an open immersion followed by a proper morphism.",
        reference_rationale="Nagata's fixed 1963 paper is explicitly a generalization of the abstract-variety compactification problem and matches the selected morphism-level form.",
    ),
    106: eligible_extract(
        reference_kind="isbn", reference_id="0387965327",
        completeness="The pinned introduction states that the three diagonals joining opposite vertices of a hexagon circumscribed about a conic are concurrent.",
        reference_rationale="The fixed Coxeter Projective Geometry citation binds Brianchon's theorem to Theorem 9.15, page 83.",
    ),
    107: eligible_passage(
        "==Statement==", end_before="\n==Locating the circle centers==",
        reference_kind="doi", reference_id="10.1007/s00283-022-10234-6",
        completeness="The section defines signed curvature, fixes four pairwise tangent circles with distinct tangencies, and gives the exact Descartes quadratic identity and its solved form.",
        reference_rationale="Bradford's fixed article is explicitly titled 'An even more straightforward proof of Descartes's circle theorem'.",
    ),
    109: eligible_extract(
        reference_kind="doi", reference_id="10.1007/s00283-023-10288-0",
        completeness="The pinned introduction fixes a tetrahedron with a tri-rectangular corner and states the exact sum-of-squared-face-areas identity.",
        reference_rationale="Tran's fixed article explicitly names and proves a generalization of de Gua's theorem, directly covering the selected base identity.",
    ),
    117: eligible_extract(
        reference_kind="doi", reference_id="10.2307/2271358",
        completeness="The pinned introduction specifies the expression generators and states undecidability of equality/zero questions for that class.",
        reference_rationale="Richardson's fixed original paper is explicitly titled 'Some Undecidable Problems Involving Elementary Functions of a Real Variable'.",
    ),
    118: eligible_passage(
        "Schwenk<ref>", end_before="\n\nCull ''et al.''",
        reference_kind="doi", reference_id="10.1080/0025570x.1991.11977627",
        completeness="The passage quantifies rectangular m-by-n boards and gives the complete three-case exception list for existence of a closed knight's tour.",
        reference_rationale="Schwenk's fixed article is explicitly titled 'Which Rectangular Chessboards Have a Knight's Tour?' and contains the selected classification.",
    ),
    125: eligible_extract(
        reference_kind="doi", reference_id="10.2307/1989762",
        completeness="The pinned introduction states confluence for lambda-calculus reduction and gives the common-descendant formulation.",
        reference_rationale="Church and Rosser's fixed original paper 'Some properties of conversion' is the direct source of the theorem.",
    ),
    126: eligible_passage(
        "==Theorem==", end_before="\n===Proof sketch===",
        reference_kind="doi", reference_id="10.1007/bf02418410",
        completeness="The section fixes a discrete pole set without finite accumulation, prescribed principal parts, and existence of a meromorphic function with exactly those principal parts.",
        reference_rationale="Mittag-Leffler's fixed 1884 paper is the original analytic representation source cited for the theorem.",
    ),
    127: eligible_extract(
        reference_kind="doi", reference_id="10.1112/jlms/s2-10.4.500",
        completeness="The pinned introduction states both that every sufficiently large even integer is prime plus a semiprime and that infinitely many primes p have p+2 semiprime.",
        reference_rationale="Ross's fixed article states Chen's exact large-even-number representation in its title.",
    ),
    128: eligible_extract(
        reference_kind="isbn", reference_id="0919611214",
        completeness="The pinned introduction states triangulation-invariance of the sum of triangle inradii for a cyclic polygon and the converse.",
        reference_rationale="The fixed Japanese Temple Geometry citation gives the theorem-specific source pages 125--128.",
    ),
    132: eligible_extract(
        reference_kind="isbn", reference_id="0070542341",
        completeness="The pinned introduction states factorization of an entire function from its zeros and the companion prescribed-zero existence result.",
        reference_rationale="The fixed Rudin Real and Complex Analysis citation binds the material to pages 299--304.",
    ),
    133: eligible_passage(
        "==Statement of the classification theorem==", end_before="\n==Overview of the proof of the classification theorem==",
        reference_kind="doi", reference_id="10.1090/s0273-0979-1979-14551-8",
        completeness="The section states the exhaustive finite-simple-group alternatives: prime cyclic, alternating, sixteen Lie-type families, or twenty-six sporadic groups.",
        reference_rationale="Gorenstein's fixed theorem-specific survey 'The classification of finite simple groups. I' directly binds the classification program and listed families.",
    ),
}


OTHER_SPECS = {
    70: ("pending", "fixed_wikipedia_identity_unresolved", "The fixed source has no resolved revision for the plaintext target, so no exact statement passage can be bound."),
    71: ("pending", "reference_scope_not_fixed", "The page states Morera's theorem, but all fixed candidates are bare book identifiers without theorem number, page, or statement linkage."),
    72: ("pending", "reference_candidates_do_not_support_selected_pcp_statement", "The fixed candidates support importance, applications, or a weaker PCP result; the direct PCP theorem papers occur outside the sealed candidate set."),
    73: ("pending", "reference_candidate_missing", "The fixed page states an atomic Carnot identity, but the sealed reference row has no candidate."),
    74: ("pending", "reference_scope_not_fixed", "The sole trade-theory chapter is broad and the sealed context does not bind the exact factor-abundance/export conclusion."),
    87: ("pending", "statement_variant_and_reference_scope_not_fixed", "The long semisimple spherical Plancherel page contains several expansions and cases; no single reviewed statement/reference pair fixes the selected variant."),
    90: ("pending", "reference_candidates_are_extensions_or_applications", "The candidates are attractor-reconstruction surveys, extensions, or applications rather than a direct fixed source for Takens's selected embedding theorem."),
    92: ("pending", "redei_variant_reference_scope_not_fixed", "The resolved Hajós page mentions Rédei's prime-cardinality strengthening, but the bare candidate contexts do not bind that exact variant."),
    94: ("pending", "logic_system_variant_not_bound", "The deduction theorem depends on the proof system and connective conventions; no atomic system-specific variant is selected."),
    95: ("pending", "reference_candidates_do_not_bind_main_theorem", "The fixed citations chiefly support center nonconstructibility, related straightedge constructions, or broad history rather than the selected universality statement."),
    100: ("pending", "reference_candidate_is_application_not_theorem_source", "The only fixed candidate is Knuth's Fibonacci multiplication article and does not directly bind Zeckendorf's unique-representation theorem."),
    101: ("pending", "statement_omits_required_regularity_hypotheses", "The fixed passage does not select the regular-family/support hypotheses needed for a precise Pitman--Koopman--Darmois theorem."),
    104: ("pending", "reference_linkage_is_expository_analogy_or_unpaged_general_text", "The inline Needham page supports the dog-leash analogy, while the remaining books are not fixed to a theorem number or verified statement page."),
    110: ("pending", "reference_candidate_missing", "The page contains a formal Kaplansky density statement, but the sealed reference row has no candidate."),
    112: ("pending", "reference_candidates_do_not_bind_khinchin_statement", "The fixed candidates cover later metric-Diophantine results or broad textbooks without a theorem/page binding to the selected Khinchin form."),
    115: ("pending", "reference_scope_not_fixed", "The fixed books have no theorem number or page binding for the exact discrete-time Doob decomposition statement."),
    119: ("pending", "reference_candidates_do_not_bind_main_statement", "The fixed papers concern choice principles and the books are broad or bare identifiers; none is sealed to the exact subgroup-of-a-free-group statement."),
    120: ("pending", "reference_scope_not_fixed", "The fixed functional-analysis books have no page or theorem locator that binds the selected Schwartz kernel formulation."),
    121: ("pending", "reference_is_generalization_not_selected_manifold_theorem", "The only fixed source concerns vector fields on singular varieties and is not bound to the selected smooth compact-manifold theorem."),
    105: ("reject", "non_atomic_plural_metrization_family", "The catalog identity names a family of metrization theorems rather than one theorem with one hypothesis/conclusion boundary."),
    108: ("reject", "non_atomic_plural_mertens_family", "The catalog identity names several inequivalent Mertens theorems and does not select one atomic variant."),
    122: ("reject", "non_atomic_nash_embedding_family", "The page explicitly separates the C1 and smooth/analytic Nash embedding theorems, which have materially different claims."),
    123: ("reject", "non_atomic_whitney_embedding_family", "The page presents distinct weak and strong Whitney embedding theorems under the same identity."),
    124: ("reject", "non_atomic_kunneth_variant_family", "Coefficient rings, Tor terms, and homology/cohomology variants are not resolved to one atomic Künneth statement."),
    129: ("reject", "non_atomic_plural_dirac_family", "The source identity is explicitly plural and resolves into multiple graph-theoretic Dirac theorems."),
}


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_sha256(value: object) -> str:
    return sha256(json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8"))


def canonical_row_sha256(row: dict) -> str:
    return canonical_sha256({key: value for key, value in row.items() if key != "row_sha256"})


def rel(path: Path) -> str:
    return path.relative_to(REPO).as_posix()


def exact_passage(page: dict, spec: dict) -> dict:
    field = spec["source_field"]
    text = page[field]
    if spec["full_field"]:
        start, end = 0, len(text)
        selection = "full_revision_pinned_extract"
    else:
        start = text.find(spec["start"])
        assert start >= 0, (page["resolved_title"], spec["start"])
        assert text.find(spec["start"], start + 1) < 0, (page["resolved_title"], "nonunique start")
        if spec["end_before"] is not None:
            end = text.find(spec["end_before"], start + len(spec["start"]))
            assert end >= 0, (page["resolved_title"], spec["end_before"])
        else:
            marker = spec["end"]
            assert marker is not None
            end = text.find(marker, start + len(spec["start"]))
            assert end >= 0, (page["resolved_title"], marker)
            end += len(marker)
        selection = "reviewed_contiguous_theorem_passage"
    passage = text[start:end]
    byte_start = len(text[:start].encode("utf-8"))
    byte_end = len(text[:end].encode("utf-8"))
    assert text.encode("utf-8")[byte_start:byte_end].decode("utf-8") == passage
    return {
        "asset": rel(WIKIPEDIA),
        "asset_sha256": FIXED_INPUT_SHA256[WIKIPEDIA],
        "source_field": field,
        "source_field_sha256": page[f"{field}_sha256"],
        "selection": selection,
        "page": page["resolved_title"],
        "page_id": page["page_id"],
        "revision_id": page["revision_id"],
        "revision_timestamp": page["revision_timestamp"],
        "mediawiki_revision_sha1": page["mediawiki_revision_sha1"],
        "attribution_url": page["attribution_url"],
        "passage": passage,
        "char_start": start,
        "char_end_exclusive": end,
        "utf8_byte_start": byte_start,
        "utf8_byte_end_exclusive": byte_end,
        "passage_sha256": sha256(passage.encode("utf-8")),
        "offset_basis": "zero-based offsets into the exact pinned source field; end is exclusive",
        "completeness": spec["completeness"],
    }


def page_bindings(resolution: dict, pages: dict[int, dict]) -> list[dict]:
    return [{
        "page": pages[page_id]["resolved_title"],
        "page_id": page_id,
        "revision_id": pages[page_id]["revision_id"],
        "revision_timestamp": pages[page_id]["revision_timestamp"],
        "mediawiki_revision_sha1": pages[page_id]["mediawiki_revision_sha1"],
        "wikitext_sha256": pages[page_id]["wikitext_sha256"],
        "extract_sha256": pages[page_id]["extract_sha256"],
        "attribution_url": pages[page_id]["attribution_url"],
    } for page_id in resolution["resolved_page_ids"]]


def exact_reference(
    parent: dict, page: dict, spec: dict, reference_parent: dict,
    wikipedia_rights: dict, openalex_by_doi: dict[str, dict],
) -> dict:
    matches = [
        candidate for candidate in reference_parent["reference_candidates"]
        if candidate["kind"] == spec["reference_kind"]
        and candidate["normalized_identifier"] == spec["reference_id"]
    ]
    assert len(matches) == 1, (parent["source_index"], spec["reference_id"], len(matches))
    candidate = matches[0]
    assert candidate["automatic_credit"] is False
    assert canonical_row_sha256(candidate) == candidate["row_sha256"]
    assert candidate["page_id"] == page["page_id"]
    assert candidate["revision_id"] == page["revision_id"]
    assert candidate["wikitext_sha256"] == page["wikitext_sha256"]
    text = page["wikitext"]
    cs, ce = candidate["context_char_start"], candidate["context_char_end_exclusive"]
    context = text[cs:ce]
    assert context == candidate["context_text"]
    assert sha256(context.encode("utf-8")) == candidate["context_sha256"]
    cbs, cbe = len(text[:cs].encode("utf-8")), len(text[:ce].encode("utf-8"))
    ids, ide = candidate["identifier_char_start"], candidate["identifier_char_end_exclusive"]
    identifier_text = text[ids:ide]
    assert candidate["raw_identifier"] in identifier_text
    ibs, ibe = len(text[:ids].encode("utf-8")), len(text[:ide].encode("utf-8"))
    openalex_binding = None
    if candidate["kind"] == "doi":
        oa = openalex_by_doi[candidate["normalized_identifier"]]
        assert canonical_row_sha256(oa) == oa["row_sha256"]
        assert oa["evidence_boundary"] == {
            "bibliographic_metadata_only": True,
            "quality_credit_granted": False,
            "supports_exact_theorem_statement_verified": False,
        }
        openalex_binding = {
            "asset": rel(OPENALEX),
            "asset_sha256": FIXED_INPUT_SHA256[OPENALEX],
            "authority_sha256": OPENALEX_AUTHORITY_SHA256,
            "join_key": candidate["normalized_identifier"],
            "record": oa,
            "bibliographic_metadata_only": True,
            "quality_credit_granted": False,
            "supports_exact_theorem_statement_verified": False,
        }
    return {
        "asset": rel(REFERENCES),
        "asset_sha256": FIXED_INPUT_SHA256[REFERENCES],
        "authority_sha256": REFERENCE_AUTHORITY_SHA256,
        "automatic_credit": False,
        "human_match_performed": True,
        "bibliographic_identity_human_verified": True,
        "human_match_rationale": spec["reference_rationale"],
        "external_fulltext_checked": False,
        "external_proof_checked": False,
        "rights_for_reproduced_material_verified": True,
        "reproduced_material_rights": wikipedia_rights,
        "record": {
            "external_id": reference_parent["external_id"],
            "source_record_id": reference_parent["source_record_id"],
            "title": reference_parent["title"],
            "row_sha256": reference_parent["row_sha256"],
        },
        "candidate": {
            "kind": candidate["kind"],
            "normalized_identifier": candidate["normalized_identifier"],
            "raw_identifier": candidate["raw_identifier"],
            "row_sha256": candidate["row_sha256"],
            "page": candidate["resolved_title"],
            "page_id": candidate["page_id"],
            "revision_id": candidate["revision_id"],
            "revision_timestamp": candidate["revision_timestamp"],
            "mediawiki_revision_sha1": candidate["mediawiki_revision_sha1"],
            "wikitext_sha256": candidate["wikitext_sha256"],
            "source_locator": candidate["source_locator"],
            "context_text": context,
            "context_char_start": cs,
            "context_char_end_exclusive": ce,
            "context_utf8_byte_start": cbs,
            "context_utf8_byte_end_exclusive": cbe,
            "context_sha256": candidate["context_sha256"],
            "identifier_char_start": ids,
            "identifier_char_end_exclusive": ide,
            "identifier_text": identifier_text,
            "identifier_utf8_byte_start": ibs,
            "identifier_utf8_byte_end_exclusive": ibe,
            "identifier_text_sha256": sha256(identifier_text.encode("utf-8")),
        },
        "openalex_metadata": openalex_binding,
    }


def build() -> dict:
    for path, expected in {**FIXED_INPUT_SHA256, **RELEASE_SENTINELS}.items():
        actual = sha256(path.read_bytes())
        assert actual == expected, (path, actual, expected)

    ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    assert ledger["authority_sha256"] == LEDGER_AUTHORITY_SHA256
    with gzip.open(WIKIPEDIA, "rt", encoding="utf-8") as stream:
        wikipedia = json.load(stream)
    references = json.loads(REFERENCES.read_text(encoding="utf-8"))
    assert references["authority_sha256"] == REFERENCE_AUTHORITY_SHA256
    assert references["policy"]["page_or_identifier_presence_grants_credit"] is False
    with gzip.open(OPENALEX, "rt", encoding="utf-8") as stream:
        openalex = json.load(stream)
    assert openalex["authority_sha256"] == OPENALEX_AUTHORITY_SHA256
    assert openalex["policy"]["openalex_metadata_grants_theorem_support_credit"] is False

    manifest = json.loads((REPO / "Docs/catalog/v5/releases/5.4/Release_Manifest.json").read_text(encoding="utf-8"))
    assert manifest["counts"]["cumulative_theorems"] == 2500
    assert manifest["counts"]["effective_strict_conjecture_credits"] == 1000

    parent_by_index = {row["source_index"]: row for row in ledger["records"]}
    pending = [
        row["source_index"] for row in ledger["records"]
        if 67 <= row["source_index"] <= 133 and row["review_disposition"] == "pending"
    ]
    assert pending == EXPECTED_PENDING
    assert set(ELIGIBLE_SPECS) | set(OTHER_SPECS) == set(EXPECTED_PENDING)
    assert set(ELIGIBLE_SPECS).isdisjoint(OTHER_SPECS)

    pages = {row["page_id"]: row for row in wikipedia["pages"]}
    resolution_by_source = {row["source_record_id"]: row for row in wikipedia["identity_resolution"]}
    reference_by_source = {row["source_record_id"]: row for row in references["records"]}
    openalex_by_doi = {row["normalized_doi"]: row for row in openalex["records"]}

    records = []
    for index in EXPECTED_PENDING:
        parent = parent_by_index[index]
        assert parent["review_disposition"] == "pending"
        assert parent["grants_existing_quality_credit"] is False
        assert parent["grants_new_release_theorem_credit"] is False
        resolution = resolution_by_source[parent["source_record_id"]]
        assert canonical_row_sha256(resolution) == resolution["row_sha256"]
        assert resolution["source_row_sha256"] == parent["source_row_sha256"]
        page_rows = [pages[page_id] for page_id in resolution["resolved_page_ids"]]
        assert len(page_rows) in {0, 1}, (index, resolution["resolved_page_ids"])
        reference_parent = reference_by_source[parent["source_record_id"]]
        assert canonical_row_sha256(reference_parent) == reference_parent["row_sha256"]
        assert reference_parent["row_sha256"] == parent["reference_candidate_entry"]["asset_row_sha256"]

        spec = ELIGIBLE_SPECS.get(index)
        if spec is not None:
            assert len(page_rows) == 1, index
            page = page_rows[0]
            decision = "eligible"
            reason_code = "complete_exact_statement_and_human_matched_reference"
            rationale = "The fixed revision contains a complete truth-apt statement and the selected fixed reference has been manually matched to this theorem identity and scope."
            evidence = exact_passage(page, spec)
            reference_evidence = exact_reference(
                parent, page, spec, reference_parent, wikipedia["rights"], openalex_by_doi
            )
            blockers = []
        else:
            decision, reason_code, rationale = OTHER_SPECS[index]
            evidence = None
            reference_evidence = None
            blockers = [reason_code]

        row = {
            "source_index": index,
            "source_record_id": parent["source_record_id"],
            "external_id": parent["external_id"],
            "title": parent["title"],
            "msc2020": parent["msc2020"],
            "original_review_disposition": "pending",
            "decision": decision,
            "reason_code": reason_code,
            "rationale": rationale,
            "blockers": blockers,
            "grants_existing_quality_credit": decision == "eligible",
            "grants_new_catalog_entry": False,
            "grants_new_release_theorem_credit": False,
            "grants_strict_conjecture_credit": False,
            "formal_proof_claimed": False,
            "external_proof_checked": False,
            "existing_parent_boundary": {
                "base_ledger_path": rel(LEDGER),
                "base_ledger_sha256": FIXED_INPUT_SHA256[LEDGER],
                "base_ledger_authority_sha256": LEDGER_AUTHORITY_SHA256,
                "base_record_canonical_sha256": canonical_sha256(parent),
                "base_source_row_sha256": parent["source_row_sha256"],
                "base_source_review_record_canonical_sha256": parent["source_review_record_canonical_sha256"],
                "base_reference_row_sha256": reference_parent["row_sha256"],
                "base_existing_quality_credit": False,
                "base_new_release_theorem_credit": False,
                "overlay_only": True,
                "creates_identity": False,
                "creates_family": False,
                "reopens_parent_dedupe": False,
                "semantic_key": parent["source_review_record"]["dedupe"]["semantic_key"],
            },
            "wikipedia_revision_bindings": page_bindings(resolution, pages),
            "reference_parent_boundary": {
                "asset": rel(REFERENCES),
                "asset_sha256": FIXED_INPUT_SHA256[REFERENCES],
                "authority_sha256": REFERENCE_AUTHORITY_SHA256,
                "row_sha256": reference_parent["row_sha256"],
                "candidate_count": len(reference_parent["reference_candidates"]),
                "automatic_credit": False,
            },
            "statement_evidence": evidence,
            "reference_evidence": reference_evidence,
        }
        row["row_sha256"] = canonical_row_sha256(row)
        records.append(row)

    counts = {
        "rows": len(records),
        "eligible_existing_quality_credit": sum(row["decision"] == "eligible" for row in records),
        "pending": sum(row["decision"] == "pending" for row in records),
        "reject": sum(row["decision"] == "reject" for row in records),
        "new_catalog_entries": 0,
        "new_release_theorem_credits": 0,
        "strict_conjecture_credits": 0,
        "formal_proofs_claimed": 0,
    }
    assert counts == {
        "rows": 52,
        "eligible_existing_quality_credit": 27,
        "pending": 19,
        "reject": 6,
        "new_catalog_entries": 0,
        "new_release_theorem_credits": 0,
        "strict_conjecture_credits": 0,
        "formal_proofs_claimed": 0,
    }

    payload = {
        "schema_version": "awesome-theorems/wikipedia-reference-range-review/1.0",
        "artifact_path": rel(OUTPUT),
        "review_as_of": "2026-08-10",
        "scope": {
            "source_index_range": [67, 133],
            "reviewed_parent_pending_indices": EXPECTED_PENDING,
            "credit_scope": "existing_catalog_quality_only",
            "base_ledger_is_frozen": True,
            "existing_parent_overlay_only": True,
            "not_a_release_append": True,
            "release_modified": False,
            "new_catalog_entries_granted": False,
            "new_release_theorem_credits_granted": False,
            "strict_conjecture_credits_granted": False,
        },
        "inputs": {
            rel(path): {"file_sha256": digest}
            for path, digest in FIXED_INPUT_SHA256.items()
        },
        "input_authorities": {
            rel(LEDGER): LEDGER_AUTHORITY_SHA256,
            rel(REFERENCES): REFERENCE_AUTHORITY_SHA256,
            rel(OPENALEX): OPENALEX_AUTHORITY_SHA256,
        },
        "release_boundary": {
            "release": "5.4",
            "protected_file_sha256": {rel(path): digest for path, digest in RELEASE_SENTINELS.items()},
            "theorem_status_records": 2500,
            "effective_strict_conjecture_credits": 1000,
            "open_problem_records": 599,
            "review_changes_inventory_counts": False,
        },
        "reference_policy": references["policy"],
        "openalex_policy": openalex["policy"],
        "rights": wikipedia["rights"],
        "decision_sets": {
            "eligible": sorted(ELIGIBLE_SPECS),
            "pending": sorted(index for index, value in OTHER_SPECS.items() if value[0] == "pending"),
            "reject": sorted(index for index, value in OTHER_SPECS.items() if value[0] == "reject"),
        },
        "counts": counts,
        "records_canonical_sha256": canonical_sha256(records),
        "records": records,
    }
    payload["authority_sha256"] = canonical_sha256(payload)
    encoded = json.dumps(payload, ensure_ascii=False, sort_keys=True).encode("utf-8")
    assert b"/tmp/" not in encoded and b"/home/" not in encoded
    return payload


def serialized(payload: dict) -> bytes:
    return (json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    payload = build()
    expected = serialized(payload)
    if args.check:
        if not OUTPUT.exists() or OUTPUT.read_bytes() != expected:
            raise SystemExit(f"stale or missing artifact: {OUTPUT}")
    else:
        OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT.write_bytes(expected)
    print(json.dumps({
        "output": rel(OUTPUT),
        "sha256": sha256(expected),
        "check": args.check,
        **payload["counts"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
