#!/usr/bin/env python3
import gzip
import hashlib
import json
from pathlib import Path


REPO = Path(__file__).resolve().parents[4]
CURATION = REPO / "Docs/catalog/v5/curation/theorem_quality_v5_5"
ASSET = REPO / "Docs/catalog/v5/sources/wikipedia-en-1000-plus-revisions-20260810.json.gz"
REFERENCE_ASSET = REPO / "Docs/catalog/v5/curation/Thousand_Plus_Reference_Candidates_v5_5.json"
REVIEW = CURATION / "reviews/review-000-199.jsonl"
OUTPUT = CURATION / "reviews/wiki-reference-subreview-000-016.json"
ASSET_SHA256 = "73341aebcc1d9d1c577881d2c6d59734ce102d7cc07b1f8ec6d21c9875076d33"
REFERENCE_ASSET_SHA256 = "f86b87afcffbf120d2f3cf0ff8860e7c925e8f9fa514db3714936e3cfa100435"
REFERENCE_AUTHORITY_SHA256 = "d428f5659c242fa66c3e78f5497013ea1b6eaf13a4558c4f15e6c0af005acc42"
REVIEW_SHA256 = "9bbaf8db012b5f7283bac1f2362717a27e50ef8178e379992e24a2693dd59052"


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def canonical_row_sha256(row):
    payload = {key: value for key, value in row.items() if key != "row_sha256"}
    encoded = json.dumps(
        payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return sha256_bytes(encoded)


def exact_passage(page, source_field, start_marker, end_marker, completeness):
    text = page[source_field]
    char_start = text.find(start_marker)
    assert char_start >= 0, (page["resolved_title"], start_marker)
    second_start = text.find(start_marker, char_start + 1)
    assert second_start < 0, (page["resolved_title"], "non-unique start marker")
    char_end = text.find(end_marker, char_start)
    assert char_end >= 0, (page["resolved_title"], end_marker)
    char_end += len(end_marker)
    passage = text[char_start:char_end]
    assert passage.startswith(start_marker) and passage.endswith(end_marker)
    byte_start = len(text[:char_start].encode("utf-8"))
    byte_end = len(text[:char_end].encode("utf-8"))
    encoded = text.encode("utf-8")
    assert encoded[byte_start:byte_end].decode("utf-8") == passage
    return {
        "asset": str(ASSET.relative_to(REPO)),
        "asset_sha256": ASSET_SHA256,
        "source_field": source_field,
        "source_field_sha256": page[f"{source_field}_sha256"],
        "page": page["resolved_title"],
        "page_id": page["page_id"],
        "revision_id": page["revision_id"],
        "revision_timestamp": page["revision_timestamp"],
        "attribution_url": page["attribution_url"],
        "passage": passage,
        "char_start": char_start,
        "char_end_exclusive": char_end,
        "utf8_byte_start": byte_start,
        "utf8_byte_end_exclusive": byte_end,
        "passage_sha256": sha256_bytes(passage.encode("utf-8")),
        "offset_basis": f"zero-based offsets into the exact {source_field} string; end is exclusive",
        "completeness": completeness,
    }


def exact_reference(external_id, page, spec):
    parent = reference_by_external_id[external_id]
    assert canonical_row_sha256(parent) == parent["row_sha256"]
    matches = [
        candidate
        for candidate in parent["reference_candidates"]
        if candidate["kind"] == spec["kind"]
        and candidate["normalized_identifier"] == spec["normalized_identifier"]
    ]
    assert len(matches) == 1, (external_id, spec, len(matches))
    candidate = matches[0]
    assert candidate["automatic_credit"] is False
    assert canonical_row_sha256(candidate) == candidate["row_sha256"]
    assert candidate["page_id"] == page["page_id"]
    assert candidate["revision_id"] == page["revision_id"]
    assert candidate["wikitext_sha256"] == page["wikitext_sha256"]
    text = page["wikitext"]
    context_start = candidate["context_char_start"]
    context_end = candidate["context_char_end_exclusive"]
    context = text[context_start:context_end]
    assert context == candidate["context_text"]
    assert sha256_bytes(context.encode("utf-8")) == candidate["context_sha256"]
    context_byte_start = len(text[:context_start].encode("utf-8"))
    context_byte_end = len(text[:context_end].encode("utf-8"))
    assert (
        text.encode("utf-8")[context_byte_start:context_byte_end].decode("utf-8")
        == context
    )
    identifier_start = candidate["identifier_char_start"]
    identifier_end = candidate["identifier_char_end_exclusive"]
    identifier_text = text[identifier_start:identifier_end]
    assert candidate["raw_identifier"] in identifier_text, (
        external_id,
        identifier_text,
        candidate["raw_identifier"],
    )
    identifier_byte_start = len(text[:identifier_start].encode("utf-8"))
    identifier_byte_end = len(text[:identifier_end].encode("utf-8"))
    return {
        "asset": str(REFERENCE_ASSET.relative_to(REPO)),
        "asset_sha256": REFERENCE_ASSET_SHA256,
        "authority_sha256": REFERENCE_AUTHORITY_SHA256,
        "automatic_credit": False,
        "external_proof_checked": False,
        "bibliographic_identity_human_verified": True,
        "rights_for_reproduced_material_verified": True,
        "reproduced_material_rights": asset["rights"],
        "external_fulltext_checked": False,
        "human_match_performed": True,
        "human_match_rationale": spec["human_match_rationale"],
        "record": {
            "external_id": parent["external_id"],
            "source_record_id": parent["source_record_id"],
            "title": parent["title"],
            "row_sha256": parent["row_sha256"],
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
            "context_char_start": context_start,
            "context_char_end_exclusive": context_end,
            "context_utf8_byte_start": context_byte_start,
            "context_utf8_byte_end_exclusive": context_byte_end,
            "context_sha256": candidate["context_sha256"],
            "identifier_char_start": identifier_start,
            "identifier_char_end_exclusive": identifier_end,
            "identifier_text": identifier_text,
            "identifier_utf8_byte_start": identifier_byte_start,
            "identifier_utf8_byte_end_exclusive": identifier_byte_end,
            "identifier_text_sha256": sha256_bytes(identifier_text.encode("utf-8")),
        },
    }


def reference_parent_binding(external_id):
    parent = reference_by_external_id[external_id]
    assert canonical_row_sha256(parent) == parent["row_sha256"]
    return {
        "asset": str(REFERENCE_ASSET.relative_to(REPO)),
        "asset_sha256": REFERENCE_ASSET_SHA256,
        "authority_sha256": REFERENCE_AUTHORITY_SHA256,
        "external_id": parent["external_id"],
        "source_record_id": parent["source_record_id"],
        "title": parent["title"],
        "row_sha256": parent["row_sha256"],
        "candidate_count": len(parent["reference_candidates"]),
        "automatic_credit": False,
    }


assert sha256_bytes(ASSET.read_bytes()) == ASSET_SHA256
assert sha256_bytes(REFERENCE_ASSET.read_bytes()) == REFERENCE_ASSET_SHA256
assert sha256_bytes(REVIEW.read_bytes()) == REVIEW_SHA256
with gzip.open(ASSET, "rt", encoding="utf-8") as handle:
    asset = json.load(handle)
reference_asset = json.loads(REFERENCE_ASSET.read_text(encoding="utf-8"))
assert reference_asset["authority_sha256"] == REFERENCE_AUTHORITY_SHA256
assert reference_asset["policy"]["page_or_identifier_presence_grants_credit"] is False
reference_by_external_id = {
    row["external_id"]: row for row in reference_asset["records"]
}
pages = {row["resolved_title"]: row for row in asset["pages"]}
review_rows = [json.loads(line) for line in REVIEW.read_text(encoding="utf-8").splitlines()]
review_by_index = {row["index"]: row for row in review_rows}
pending = [
    row["index"]
    for row in review_rows
    if 0 <= row["index"] <= 16 and row["decision"] == "pending"
]
assert pending == [3, 4, 5, 7, 9, 10, 11, 12, 13, 15, 16]


eligible_specs = {
    3: {
        "page": "Noether's second theorem",
        "field": "wikitext",
        "start": "For Noether's second theorem, we consider those variational symmetries",
        "end": (
            "then there exist <math>q</math> linear differential relations between the "
            "Euler-Lagrange equations of <math display=\"inline\">L</math>."
        ),
        "reason_code": "complete_exact_noether_second_theorem_statement",
        "completeness": (
            "Complete exact theorem form: the passage specifies the linearly and differentially "
            "parameterized gauge variations (including their generic formula and coefficient "
            "range), the exact-symmetry condition, the finite positive parameter count q, and "
            "the conclusion of q linear differential relations among the Euler–Lagrange equations."
        ),
    },
    4: {
        "page": "Pólya enumeration theorem",
        "field": "wikitext",
        "start": "Let ''X'' be a [[finite set]]",
        "end": "when considered as a permutation of ''X''.",
        "reason_code": "complete_exact_polya_unweighted_form",
        "completeness": (
            "Complete exact simplified/unweighted form explicitly presented by the source: the "
            "passage fixes finite X, the permutation group G, the finite color set Y and induced "
            "action, then gives the orbit-count formula and defines every symbol in it."
        ),
    },
    5: {
        "page": "Lamé's theorem",
        "field": "wikitext",
        "start": "== Statement ==\nThe number of division steps",
        "end": "Let <math>u>v</math> be two positive integers.",
        "reason_code": "complete_exact_lame_complexity_bound",
        "completeness": (
            "Complete exact theorem form with the immediately following domain setup: u and v are "
            "positive integers (ordered without loss of generality), and the conclusion bounds "
            "Euclidean-algorithm division steps by five times the decimal-digit count of min(u,v)."
        ),
    },
    7: {
        "page": "Szemerédi's theorem",
        "field": "wikitext",
        "start": "A subset ''A'' of the [[natural numbers]] is said to have positive upper density if",
        "end": (
            "Szemerédi's theorem asserts that a subset of the natural numbers with positive upper "
            "density contains an arithmetic progression of length ''k'' for all positive integers ''k''."
        ),
        "reason_code": "complete_exact_szemeredi_density_form",
        "completeness": (
            "Complete exact infinitary form: the passage defines positive upper density by its "
            "limsup formula, fixes the domain as subsets of the natural numbers, and states the "
            "arithmetic-progression conclusion for every positive integer k."
        ),
    },
    9: {
        "page": "Jacobson–Morozov theorem",
        "field": "wikitext",
        "start": (
            "The statement of Jacobson&ndash;Morozov relies on the following preliminary notions"
        ),
        "end": (
            "The Jacobson&ndash;Morozov theorem states that, conversely, any nilpotent non-zero "
            "element <math>e \\in \\mathfrak g</math> can be extended to an "
            "sl<sub>2</sub>-triple.<ref>{{harvtxt|Bourbaki|2007|loc=Ch. VIII, §11, "
            "Prop. 2}}</ref><ref>{{harvtxt|Jacobson|1979|loc=Ch. III, §11, Theorem "
            "17}}</ref>"
        ),
        "reason_code": "complete_exact_jacobson_morozov_statement",
        "completeness": (
            "Complete exact Lie-algebra form: the passage fixes a semisimple Lie algebra over a "
            "field of characteristic zero, defines an sl2-triple by its bracket identities, "
            "defines nilpotence via the adjoint endomorphism, and gives the nonzero-nilpotent "
            "extension conclusion."
        ),
    },
    11: {
        "page": "Joubert's theorem",
        "field": "wikitext",
        "start": (
            "In [[polynomial algebra]] and [[Field (mathematics)|field theory]], "
            "'''Joubert's theorem''' states that if"
        ),
        "end": "for some constants <math>c_4, c_2, c_1, c_0</math> in <math>K</math>.",
        "reason_code": "complete_exact_joubert_statement",
        "completeness": (
            "Complete exact field-theoretic statement: the passage gives the fields K and L, "
            "separability, degree six, characteristic not two, existence of a primitive generator, "
            "and the full required shape of its minimal polynomial with coefficients in K."
        ),
    },
    12: {
        "page": "Theorema Egregium",
        "field": "extract",
        "start": "In modern mathematical terminology, the theorem may be stated as follows:",
        "end": "The Gaussian curvature of a surface is invariant under local isometry.",
        "reason_code": "complete_exact_theorema_egregium_modern_form",
        "completeness": (
            "Complete exact modern formulation: for surfaces related by a local isometry, the "
            "passage states the invariant quantity (Gaussian curvature) and the conclusion "
            "(invariance at corresponding local points)."
        ),
    },
    15: {
        "page": "Hartogs's theorem on separate holomorphicity",
        "field": "wikitext",
        "start": "In [[mathematics]], '''Hartogs's theorem'''",
        "end": (
            "Therefore, 'separate analyticity' and 'analyticity' are coincident notions, in the "
            "theory of several complex variables."
        ),
        "reason_code": "complete_exact_hartogs_separate_holomorphicity_statement",
        "completeness": (
            "Complete exact stated form: the passage fixes F:C^n→C, assumes analyticity in each "
            "variable with the others fixed, concludes continuity, and records the resulting full "
            "n-variable analyticity/Taylor-expansion conclusion."
        ),
    },
}


reference_specs = {
    3: {
        "kind": "doi",
        "normalized_identifier": "10.1080/00411457108231446",
        "human_match_rationale": (
            "The fixed citation is Noether's original 1918 paper together with its 1971 "
            "English translation, and is the primary source explicitly attached to this named "
            "Noether theorem page and statement variant."
        ),
    },
    4: {
        "kind": "doi",
        "normalized_identifier": "10.1007/bf02546665",
        "human_match_rationale": (
            "The citation is Pólya's 1937 original enumeration paper and is a direct primary "
            "source for the named enumeration theorem and its orbit-counting formula."
        ),
    },
    5: {
        "kind": "doi",
        "normalized_identifier": "10.1006/hmat.1994.1031",
        "human_match_rationale": (
            "Shallit's cited paper is specifically about the origins and analysis of the "
            "Euclidean algorithm and is attached to the Lamé theorem page containing the exact "
            "division-step bound."
        ),
    },
    7: {
        "kind": "doi",
        "normalized_identifier": "10.4064/aa-27-1-199-245",
        "human_match_rationale": (
            "The candidate is Szemerédi's 1975 original paper 'On sets of integers containing "
            "no k elements in arithmetic progression', which directly matches the selected "
            "positive-density arithmetic-progression theorem."
        ),
    },
    9: {
        "kind": "isbn",
        "normalized_identifier": "0486638324",
        "human_match_rationale": (
            "The exact selected theorem sentence is immediately followed by the fixed inline "
            "citation 'Jacobson 1979, Ch. III, §11, Theorem 17'. The candidate is the matching "
            "Jacobson Lie algebras book entry (ISBN 0-486-63832-4), so the statement-to-reference "
            "link is explicit rather than inferred from bibliography presence."
        ),
    },
    11: {
        "kind": "doi",
        "normalized_identifier": "10.1016/j.crma.2014.08.004",
        "human_match_rationale": (
            "The cited article is explicitly titled 'Joubert's theorem fails in characteristic "
            "2'; that title binds the reference to the exact characteristic-not-two theorem "
            "statement selected from the fixed page."
        ),
    },
}


reference_pending_specs = {
    12: {
        "page": "Theorema Egregium",
        "reason_code": "complete_wikipedia_statement_but_no_explicit_candidate_reference_match",
        "rationale": (
            "The fixed Wikipedia revision contains a complete modern local-isometry statement, "
            "but the reference asset offers only general differential-geometry books or Gauss's "
            "collected surface text. Their captured contexts do not explicitly bind a page or "
            "theorem number to this exact selected formulation, so reference matching remains "
            "pending."
        ),
    },
    15: {
        "page": "Hartogs's theorem on separate holomorphicity",
        "reason_code": "complete_wikipedia_statement_but_no_explicit_candidate_reference_match",
        "rationale": (
            "The fixed Wikipedia revision contains a complete separate-holomorphicity statement, "
            "but the reference asset contains only broad several-complex-variables book citations "
            "without a theorem/page binding in the captured context. Identifier presence alone "
            "cannot grant the quality credit."
        ),
    },
}


records = []
for index in pending:
    base = review_by_index[index]
    record = {
        "index": index,
        "title": base["identity"]["title"],
        "original_decision": "pending",
        "grants_new_catalog_entry": False,
        "formal_proof_claimed": False,
    }
    if index in reference_specs:
        spec = eligible_specs[index]
        page = pages[spec["page"]]
        evidence = exact_passage(
            page,
            spec["field"],
            spec["start"],
            spec["end"],
            spec["completeness"],
        )
        record.update(
            {
                "decision": "eligible",
                "grants_existing_quality_credit": True,
                "reason_code": spec["reason_code"],
                "rationale": (
                    "The fixed revision contains a contiguous, exact, scope-complete statement "
                    "with explicit hypotheses/range and conclusion."
                ),
                "evidence": evidence,
                "reference_evidence": exact_reference(
                    base["identity"]["synthetic_source_id"],
                    page,
                    reference_specs[index],
                ),
            }
        )
    elif index == 10:
        page = pages["Density functional theory"]
        record.update(
            {
                "decision": "reject",
                "grants_existing_quality_credit": False,
                "reason_code": "non_atomic_plural_family_two_distinct_theorems",
                "rationale": (
                    "The catalog title is explicitly plural. The pinned broader DFT page calls "
                    "these the two Hohenberg–Kohn theorems and separately labels Theorem 1 "
                    "(external potential/energy as a unique density functional) and Theorem 2 "
                    "(the variational minimum at the true ground-state density). They are distinct "
                    "claims, so one atomic theorem credit cannot be assigned to this family row."
                ),
                "inspected_source": {
                    "page": page["resolved_title"],
                    "page_id": page["page_id"],
                    "revision_id": page["revision_id"],
                    "source_field": "wikitext",
                    "source_field_sha256": page["wikitext_sha256"],
                },
                "evidence": None,
                "reference_evidence": None,
            }
        )
    elif index == 13:
        page = pages["Coase theorem"]
        record.update(
            {
                "decision": "reject",
                "grants_existing_quality_credit": False,
                "reason_code": "unsettled_non_atomic_efficiency_and_invariance_formulations",
                "rationale": (
                    "The pinned page explicitly says the exact definition remains unsettled and "
                    "distinguishes two claims, an efficiency version and an invariance version. "
                    "Its intro also uses the non-quantified condition 'sufficiently low transaction "
                    "costs'. The title therefore does not identify one exact atomic mathematical "
                    "claim suitable for strict theorem credit."
                ),
                "inspected_source": {
                    "page": page["resolved_title"],
                    "page_id": page["page_id"],
                    "revision_id": page["revision_id"],
                    "source_field": "wikitext",
                    "source_field_sha256": page["wikitext_sha256"],
                },
                "evidence": None,
                "reference_evidence": None,
            }
        )
    elif index in reference_pending_specs:
        spec = reference_pending_specs[index]
        page = pages[spec["page"]]
        statement_spec = eligible_specs[index]
        statement_evidence = exact_passage(
            page,
            statement_spec["field"],
            statement_spec["start"],
            statement_spec["end"],
            statement_spec["completeness"],
        )
        record.update(
            {
                "decision": "pending",
                "grants_existing_quality_credit": False,
                "reason_code": spec["reason_code"],
                "rationale": spec["rationale"],
                "inspected_source": {
                    "asset": str(ASSET.relative_to(REPO)),
                    "asset_sha256": ASSET_SHA256,
                    "page": page["resolved_title"],
                    "page_id": page["page_id"],
                    "revision_id": page["revision_id"],
                    "revision_timestamp": page["revision_timestamp"],
                    "source_field": statement_spec["field"],
                    "source_field_sha256": page[f"{statement_spec['field']}_sha256"],
                    "reference_asset": str(REFERENCE_ASSET.relative_to(REPO)),
                    "reference_asset_sha256": REFERENCE_ASSET_SHA256,
                    "reference_authority_sha256": REFERENCE_AUTHORITY_SHA256,
                },
                "evidence": None,
                "statement_evidence": statement_evidence,
                "reference_evidence": None,
                "reference_parent": reference_parent_binding(
                    base["identity"]["synthetic_source_id"]
                ),
            }
        )
    elif index == 16:
        identity = next(
            row for row in asset["identity_resolution"] if row["external_id"] == "Q1051404"
        )
        title_resolution = next(
            row
            for row in asset["title_resolution"]
            if row["requested_title"] == "Cesàro's theorem"
        )
        assert identity["resolved_page_ids"] == []
        assert title_resolution["resolution_status"] == "missing"
        assert not any(page["revision_id"] == 1362701000 for page in asset["pages"])
        record.update(
            {
                "decision": "pending",
                "grants_existing_quality_credit": False,
                "reason_code": "fixed_asset_missing_page_and_source_identity_repair_required",
                "rationale": (
                    "The fixed asset records the supplied title Cesàro's theorem as missing and "
                    "Q1051404 with no resolved page IDs. It contains no page row for the later "
                    "Cauchy product fallback revision cited by the draft review, while the Wikidata "
                    "label/sitelink identify Cauchy product rather than the catalog title. An exact "
                    "fixed-asset passage and offsets therefore cannot be supplied until the source "
                    "identity and asset are repaired."
                ),
                "inspected_source": {
                    "requested_page": "Cesàro's theorem",
                    "revision_id": None,
                    "fixed_asset_resolution_status": title_resolution["resolution_status"],
                    "fixed_asset_resolved_page_ids": identity["resolved_page_ids"],
                    "draft_fallback_page": "Cauchy product",
                    "draft_fallback_revision_id": 1362701000,
                    "fallback_revision_present_in_fixed_asset_pages": False,
                },
                "evidence": None,
                "reference_evidence": None,
                "reference_parent": reference_parent_binding(
                    base["identity"]["synthetic_source_id"]
                ),
            }
        )
    else:
        raise AssertionError(index)
    records.append(record)


assert [row["index"] for row in records] == pending
assert sum(row["decision"] == "eligible" for row in records) == 6
assert sum(row["decision"] == "reject" for row in records) == 2
assert sum(row["decision"] == "pending" for row in records) == 3
assert all(row["grants_new_catalog_entry"] is False for row in records)
assert all(row["formal_proof_claimed"] is False for row in records)

OUTPUT.write_text(
    json.dumps(records, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
    encoding="utf-8",
)

# Parse and revalidate the exact slices from the serialized artifact.
loaded = json.loads(OUTPUT.read_text(encoding="utf-8"))
for row in loaded:
    if row["decision"] != "eligible":
        assert row["evidence"] is None
        assert row["reference_evidence"] is None
        if row.get("statement_evidence"):
            statement = row["statement_evidence"]
            page = pages[statement["page"]]
            text = page[statement["source_field"]]
            assert (
                text[statement["char_start"] : statement["char_end_exclusive"]]
                == statement["passage"]
            )
        continue
    ev = row["evidence"]
    text = pages[ev["page"]][ev["source_field"]]
    passage = ev["passage"]
    assert text[ev["char_start"] : ev["char_end_exclusive"]] == passage
    encoded = text.encode("utf-8")
    assert (
        encoded[ev["utf8_byte_start"] : ev["utf8_byte_end_exclusive"]].decode("utf-8")
        == passage
    )
    assert sha256_bytes(passage.encode("utf-8")) == ev["passage_sha256"]
    ref = row["reference_evidence"]
    assert ref["automatic_credit"] is False
    assert ref["external_proof_checked"] is False

print(
    json.dumps(
        {
            "output": str(OUTPUT),
            "sha256": sha256_bytes(OUTPUT.read_bytes()),
            "records": len(records),
            "eligible": 6,
            "reject": 2,
            "pending": 3,
        },
        sort_keys=True,
    )
)
