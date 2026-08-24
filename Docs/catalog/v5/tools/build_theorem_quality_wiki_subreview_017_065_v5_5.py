#!/usr/bin/env python3
import gzip
import hashlib
import json
from pathlib import Path


REPO = Path(__file__).resolve().parents[4]
CURATION = REPO / "Docs/catalog/v5/curation/theorem_quality_v5_5"
ASSET = REPO / "Docs/catalog/v5/sources/wikipedia-en-1000-plus-revisions-20260810.json.gz"
REFERENCE_ASSET = (
    REPO / "Docs/catalog/v5/curation/Thousand_Plus_Reference_Candidates_v5_5.json"
)
REVIEW = CURATION / "reviews/review-000-199.jsonl"
OUTPUT = CURATION / "reviews/wiki-reference-subreview-017-065.json"
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
    assert text.find(start_marker, char_start + 1) < 0, (
        page["resolved_title"],
        "non-unique start marker",
        start_marker,
    )
    if end_marker is None:
        char_end = len(text)
    else:
        char_end = text.find(end_marker, char_start)
        assert char_end >= 0, (page["resolved_title"], end_marker)
        char_end += len(end_marker)
    passage = text[char_start:char_end]
    assert passage.startswith(start_marker)
    if end_marker is not None:
        assert passage.endswith(end_marker)
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
        "offset_basis": (
            f"zero-based offsets into the exact {source_field} string; end is exclusive"
        ),
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
pages = {row["page_id"]: row for row in asset["pages"]}
identity_resolution = {row["external_id"]: row for row in asset["identity_resolution"]}
review_rows = [json.loads(line) for line in REVIEW.read_text(encoding="utf-8").splitlines()]
review_by_index = {row["index"]: row for row in review_rows}
pending = [
    row["index"]
    for row in review_rows
    if 17 <= row["index"] <= 65 and row["decision"] == "pending"
]
assert pending == [
    17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 28, 30, 33, 35, 36, 37, 38,
    39, 42, 43, 44, 45, 46, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58,
    59, 60, 61, 63, 64, 65,
]


eligible_specs = {
    18: {
        "page_id": 1982872,
        "field": "extract",
        "start": "The five color theorem is a result from graph theory",
        "end": "(i.e., not merely a corner where three or more regions meet).",
        "reason_code": "complete_exact_five_color_map_statement",
        "completeness": (
            "Complete map-coloring form: the passage fixes a plane partition into regions, "
            "defines adjacency as a shared nonzero-length boundary, and concludes that at most "
            "five colors suffice with adjacent regions differently colored."
        ),
    },
    19: {
        "page_id": 55227,
        "field": "wikitext",
        "start": "A [[Baire space]] is a topological space",
        "end": "every [[locally compact regular]] space is a Baire space.",
        "reason_code": "complete_exact_baire_category_two_standard_forms",
        "completeness": (
            "Complete named-theorem coverage: the passage defines a Baire space and states both "
            "standard BCT forms, including the complete-pseudometric and locally-compact-regular "
            "generalisations, rather than only the previously mapped special case."
        ),
    },
    20: {
        "page_id": 2874706,
        "field": "wikitext",
        "start": "== Statement of the theorem for the {{math|*/∞}} case ==",
        "end": "</ref>",
        "reason_code": "complete_exact_stolz_cesaro_two_cases",
        "completeness": (
            "Complete source-presented theorem coverage: the contiguous passage gives the real-"
            "sequence hypotheses, monotonicity and limiting assumptions, and ratio conclusion "
            "for both the */infinity and 0/0 cases."
        ),
    },
    22: {
        "page_id": 719575,
        "field": "extract",
        "start": "In social choice theory, May's theorem",
        "end": "every person's dominant strategy is to honestly disclose their preferences.",
        "reason_code": "complete_exact_may_majority_characterization",
        "completeness": (
            "Complete characterization as presented: the passage fixes ranked social choice "
            "between two candidates, identifies majority vote as unique, and enumerates all five "
            "criteria together with the stated strategyproofness replacement."
        ),
    },
    24: {
        "page_id": 1543358,
        "field": "wikitext",
        "start": "==Statement==\nSuppose that <math>\\theta </math>",
        "end": "+ \\mathrm{d}x_{p+1}.</math>",
        "reason_code": "complete_exact_darboux_one_form_normal_forms",
        "completeness": (
            "Complete general one-form statement: it fixes an n-manifold, a one-form whose "
            "exterior derivative has constant rank p, splits on the wedge condition, and gives "
            "the exact local normal coordinates in both cases."
        ),
    },
    25: {
        "page_id": 2473208,
        "field": "wikitext",
        "start": "==Definition and interpretation==\nThe Frisch–Waugh–Lovell theorem states",
        "end": "does not depend on statistical properties of the data.",
        "reason_code": "complete_exact_fwl_residual_regression_statement",
        "completeness": (
            "Complete coefficient form: the passage supplies the full least-squares regression, "
            "quantifies the non-intercept coefficients, states both residual-regression steps and "
            "the resulting coefficient formula, and identifies the result as purely numerical."
        ),
    },
    26: {
        "page_id": 485472,
        "field": "extract",
        "start": "Earnshaw's theorem states",
        "end": "solely by the electrostatic interaction of the charges.",
        "reason_code": "complete_exact_earnshaw_electrostatic_statement",
        "completeness": (
            "Complete classical electrostatic form: the objects, allowed interaction, stability "
            "condition, and impossibility conclusion are all explicit in one sentence."
        ),
    },
    30: {
        "page_id": 351853,
        "field": "wikitext",
        "start": "==Bounded convergence theorem==",
        "end": ":<math>\\lim_{n\\to\\infty} \\int_S{f_n\\,d\\mu} = \\int_S{f\\,d\\mu}.</math>",
        "reason_code": "complete_exact_bounded_convergence_corollary",
        "completeness": (
            "Complete bounded-convergence form: the passage fixes complex measurable functions, "
            "uniform boundedness, pointwise convergence and finite measure, then concludes "
            "integrability of the limit and convergence of the integrals."
        ),
    },
    33: {
        "page_id": 1527098,
        "field": "wikitext",
        "start": "==Formula==\nClairaut's theorem says",
        "end": "<ref name=\"Stokes\" />",
        "reason_code": "complete_exact_clairaut_gravity_formula",
        "completeness": (
            "Complete formula form: the passage states the hydrostatic-spheroid setting, gives "
            "surface gravity as a function of latitude, defines equatorial gravity, centrifugal "
            "ratio and flattening, and records the formula's surface/density scope."
        ),
    },
    35: {
        "page_id": 68090028,
        "field": "extract",
        "start": "Theorem Let ",
        "end": None,
        "reason_code": "complete_exact_bochner_tube_extension_statement",
        "completeness": (
            "Complete theorem statement from the revision intro: omega is connected and open, "
            "the tube domain and holomorphic input are explicit, and the conclusion is holomorphic "
            "extension to its convex hull."
        ),
    },
    36: {
        "page_id": 7503941,
        "field": "wikitext",
        "start": "== Statement ==\nConsider a [[compact set]]",
        "end": "The boundary case of equality is attained by the regular ''n''-[[simplex]].",
        "reason_code": "complete_exact_jung_euclidean_radius_bound",
        "completeness": (
            "Complete Euclidean n-dimensional form: the compact set and its diameter are defined, "
            "the enclosing-ball radius bound is explicit, and the equality case is identified."
        ),
    },
    37: {
        "page_id": 68102162,
        "field": "extract",
        "start": "Theorem Let",
        "end": None,
        "reason_code": "complete_exact_malgrange_zerner_extension_statement",
        "completeness": (
            "Complete theorem statement from the intro: X, P and its convex hull W are defined; "
            "local boundedness, smoothness and separate holomorphicity are quantified; and the "
            "unique joint holomorphic extension conclusion is explicit."
        ),
    },
    38: {
        "page_id": 3655598,
        "field": "wikitext",
        "start": "'''Choquet's theorem''' states",
        "end": (
            "gives a similar representation with a probability measure that vanishes on the "
            "[[Baire set|Baire subsets]] of ''C'' which contain no extreme points."
        ),
        "reason_code": "complete_contextualized_choquet_bishop_de_leeuw_statement",
        "completeness": (
            "Complete contextualized statement: the contiguous passage spells out the compact "
            "convex representation and affine integral identity, then replaces metrizability by "
            "the Bishop–de Leeuw Baire-set vanishing condition for nonmetrizable C."
        ),
    },
    39: {
        "page_id": 68241562,
        "field": "extract",
        "start": "In formal language theory",
        "end": "we can find an MSO formula defining the same language.",
        "reason_code": "complete_exact_buchi_elgot_trakhtenbrot_equivalence",
        "completeness": (
            "Complete bidirectional characterization: the passage equates regular languages and "
            "MSO definability and explicitly gives both effective translations between MSO "
            "formulas and finite-state automata."
        ),
    },
    42: {
        "page_id": 485168,
        "field": "extract",
        "start": "The hairy ball theorem",
        "end": "(a p such that f(p) = 0).",
        "reason_code": "complete_exact_hairy_ball_even_sphere_statement",
        "completeness": (
            "Complete general and concrete forms: it states nonexistence of a nonvanishing "
            "continuous tangent field on every even-dimensional sphere and expands the ordinary "
            "2-sphere case with the tangent-field and zero conclusion."
        ),
    },
    43: {
        "page_id": 104790,
        "field": "wikitext",
        "start": "This is a general property.  For each positive number",
        "end": "later was generalized as [[Glaisher's theorem]].",
        "reason_code": "complete_exact_euler_partition_odd_distinct_equinumerosity",
        "completeness": (
            "Complete Euler partition statement: for every positive integer it identifies the "
            "two restricted partition classes and asserts equality of their counts."
        ),
    },
    45: {
        "page_id": 9914115,
        "field": "extract",
        "start": "In algebraic geometry",
        "end": "it is an open problem.",
        "reason_code": "complete_exact_hironaka_characteristic_zero_resolution",
        "completeness": (
            "Complete characteristic-zero form: resolution is defined as a nonsingular variety "
            "with a proper birational map to V, and existence for every variety over a "
            "characteristic-zero field is explicitly asserted."
        ),
    },
    46: {
        "page_id": 1711336,
        "field": "extract",
        "start": "In mathematics, Apéry's theorem",
        "end": "where p and q are integers.",
        "reason_code": "complete_exact_apery_zeta_three_irrationality",
        "completeness": (
            "Complete irrationality statement: zeta(3) is identified by its convergent series and "
            "the conclusion is spelled out as non-representability by an integer fraction p/q."
        ),
    },
    48: {
        "page_id": 19357539,
        "field": "wikitext",
        "start": "==Statement of the theorem==\nLet ''H'' be a [[Hilbert space]]",
        "end": ":<math>B(h, v) = \\langle f, v \\rangle \\mbox{ for all } v \\in V.</math>",
        "reason_code": "complete_exact_lions_lax_milgram_equivalence",
        "completeness": (
            "Complete source-presented equivalence: H, V and continuous bilinear B are fixed; the "
            "coercivity bound is explicit; and it is equated to existence of a weak inverse for "
            "every continuous functional on V."
        ),
    },
    49: {
        "page_id": 69955049,
        "field": "wikitext",
        "start": "== Statement of the theorem for direct products ==",
        "end": "in the first-order theory of [[field of sets|fields of sets]].",
        "reason_code": "complete_exact_feferman_vaught_direct_product_reduction",
        "completeness": (
            "Complete direct-product reduction form: the passage fixes a first-order formula and "
            "component truth-index sets, then states the algorithm constructing phi-star and its "
            "finite field-of-sets interpretation."
        ),
    },
    51: {
        "page_id": 61969687,
        "field": "extract",
        "start": "In mathematical logic, the Friedberg–Muchnik theorem",
        "end": None,
        "reason_code": "complete_exact_friedberg_muchnik_incomparable_ce_sets",
        "completeness": (
            "Complete computability statement: it asserts existence of two computably enumerable "
            "languages and defines their incomparability as absence of Turing reductions in both "
            "directions."
        ),
    },
    53: {
        "page_id": 40429150,
        "field": "wikitext",
        "start": "===Dinostratus's theorem===",
        "end": "{{r|Hischer}}",
        "reason_code": "complete_exact_dinostratus_quadratrix_ratio",
        "completeness": (
            "Complete geometric ratio form: the defining square, endpoint J and side AB are fixed, "
            "and the exact AJ/AB = 2/pi conclusion is displayed."
        ),
    },
    54: {
        "page_id": 70302266,
        "field": "wikitext",
        "start": "==Statement of the theorem==",
        "end": "the lengths of the columns of the partition <math>\\lambda</math>.",
        "reason_code": "complete_exact_gamas_nonvanishing_characterization",
        "completeness": (
            "Complete necessary-and-sufficient statement: V, lambda, the irreducible character and "
            "the symmetrized decomposable tensor are defined, followed by the exact nonzero iff "
            "partition-into-independent-sets criterion."
        ),
    },
    55: {
        "page_id": 70997704,
        "field": "extract",
        "start": "In mathematical analysis, Netto's theorem",
        "end": "between two smooth manifolds of different dimension.",
        "reason_code": "complete_exact_netto_dimension_invariance",
        "completeness": (
            "Complete manifold form: the morphism class is continuous bijections, the objects are "
            "smooth manifolds, and preservation/equality of dimension is stated equivalently as a "
            "nonexistence result."
        ),
    },
    56: {
        "page_id": 342602,
        "field": "extract",
        "start": "In statistics, the Lehmann–Scheffé theorem",
        "end": None,
        "reason_code": "complete_exact_lehmann_scheffe_umvue_statement",
        "completeness": (
            "Complete estimator characterization: unbiasedness, dependence only through a "
            "complete sufficient statistic, and the unique uniformly minimum-variance unbiased "
            "conclusion are all explicit."
        ),
    },
    57: {
        "page_id": 4637081,
        "field": "extract",
        "start": "In computational complexity",
        "end": "P = NP if and only if NPI is empty.",
        "reason_code": "complete_exact_ladner_np_intermediate_existence",
        "completeness": (
            "Complete conditional existence form: NPI is defined, P != NP is the hypothesis, and "
            "existence of an NP problem that is neither in P nor NP-complete is the conclusion."
        ),
    },
    58: {
        "page_id": 1793003,
        "field": "wikitext",
        "start": "Sklar's theorem states that every",
        "end": "with marginal distributions <math>F_i(x)</math>.",
        "reason_code": "complete_exact_sklar_existence_uniqueness_converse",
        "completeness": (
            "Complete Sklar coverage: it gives the multivariate CDF factorization through its "
            "marginals and a copula, uniqueness on the product of marginal ranges (hence for "
            "continuous marginals), and the converse construction."
        ),
    },
    59: {
        "page_id": 622844,
        "field": "wikitext",
        "start": "{{Math theorem\n| name = Euler's homogeneous function theorem",
        "end": (
            "Conversely, every maximal continuously differentiable solution of this partial "
            "differentiable equation is a positively homogeneous function of degree {{mvar|k}}, "
            "defined on a positive cone (here, ''maximal'' means that the solution cannot be "
            "prolongated to a function with a larger domain).\n}}"
        ),
        "reason_code": "complete_exact_euler_homogeneous_function_characterization",
        "completeness": (
            "Complete differentiable characterization: positive homogeneity and C1 regularity on "
            "an open set imply the displayed Euler PDE, and maximal C1 solutions of that PDE are "
            "conversely positively homogeneous on a positive cone."
        ),
    },
    60: {
        "page_id": 4165181,
        "field": "wikitext",
        "start": "This [[theorem]] states that if <math>S</math> is a [[convex set]]",
        "end": "defines a supporting hyperplane.",
        "reason_code": "complete_exact_supporting_hyperplane_boundary_statement",
        "completeness": (
            "Complete finite-dimensional existence form: S is convex in R^n, x0 is a boundary "
            "point, a supporting hyperplane through x0 is asserted, and its nonzero-functional "
            "representation is supplied."
        ),
    },
    61: {
        "page_id": 749033,
        "field": "extract",
        "start": "In mathematics, in the areas of order theory and combinatorics",
        "end": "This number is called the width of the partial order.",
        "reason_code": "complete_exact_dilworth_finite_poset_statement",
        "completeness": (
            "Complete finite-poset equality: the universe is a finite partially ordered set and "
            "the maximum antichain size is equated to the minimum number of covering chains."
        ),
    },
    63: {
        "page_id": 1433747,
        "field": "extract",
        "start": "In the mathematical field of partial differential equations",
        "end": "the limit is a harmonic function on G.",
        "reason_code": "complete_exact_harnack_monotone_harmonic_sequence_principle",
        "completeness": (
            "Complete Harnack principle: the passage fixes a monotone increasing sequence of "
            "harmonic functions on an open connected Euclidean domain and gives the infinite-"
            "everywhere versus compact-uniform finite harmonic-limit dichotomy."
        ),
    },
    64: {
        "page_id": 23190553,
        "field": "wikitext",
        "start": "==Statement==\n\nLet {''f<sub>k</sub>''}",
        "end": "as&nbsp;''k''&nbsp;→&nbsp;∞.",
        "reason_code": "complete_exact_hurwitz_zero_multiplicity_statement",
        "completeness": (
            "Complete zero-convergence theorem: the connected domain, compact-uniform holomorphic "
            "convergence and nonzero limit are fixed; a zero of order m yields exactly m nearby "
            "zeros with multiplicity, converging to that zero."
        ),
    },
    65: {
        "page_id": 2539254,
        "field": "extract",
        "start": "In physics, the optical theorem",
        "end": "k is the wave vector in the incident direction.",
        "reason_code": "complete_exact_optical_forward_amplitude_cross_section_relation",
        "completeness": (
            "Complete conventional normalization: the passage states the total-cross-section/"
            "forward-amplitude relation, displays sigma = 4pi Im f(0)/k, and defines f(0) and k."
        ),
    },
}


reference_specs = {
    18: {
        "kind": "doi",
        "normalized_identifier": "10.2307/2039977",
        "human_match_rationale": (
            "The fixed citation title is 'A Generalization of the 5-Color Theorem', and the "
            "adjacent page prose identifies Kainen's simplified proof of the same planar "
            "five-color result selected here."
        ),
    },
    20: {
        "kind": "isbn",
        "normalized_identifier": "9788132221470",
        "human_match_rationale": (
            "The Real Analysis on Intervals citation gives pages 59–60 and is attached to the "
            "complete Stolz–Cesàro 0/0 conclusion in the same fixed statement section."
        ),
    },
    22: {
        "kind": "doi",
        "normalized_identifier": "10.2307/1907651",
        "human_match_rationale": (
            "May's original paper is cited directly at the theorem introduction and its title "
            "states necessary and sufficient conditions for simple majority decision, exactly "
            "the characterization selected here."
        ),
    },
    24: {
        "kind": "isbn",
        "normalized_identifier": "9780828403160",
        "human_match_rationale": (
            "The selected one-form normal-form statement is followed by discussion of Darboux's "
            "original proof, with Sternberg pages 140–141 as the fixed source citation."
        ),
    },
    25: {
        "kind": "doi",
        "normalized_identifier": "10.3200/jece.39.1.88-91",
        "human_match_rationale": (
            "The citation title is exactly 'A Simple Proof of the FWL Theorem', which directly "
            "binds it to the selected residual-regression coefficient identity."
        ),
    },
    26: {
        "kind": "doi",
        "normalized_identifier": "10.1119/1.10449",
        "human_match_rationale": (
            "The fixed article title explicitly names Earnshaw's theorem and is cited in the "
            "page's proof discussion for the same electrostatic impossibility statement."
        ),
    },
    35: {
        "kind": "doi",
        "normalized_identifier": "10.1090/s0002-9939-09-10057-6",
        "human_match_rationale": (
            "The cited paper is explicitly titled 'A Proof of Bochner's Tube Theorem' and is "
            "listed after the exact tube-domain extension statement."
        ),
    },
    37: {
        "kind": "doi",
        "normalized_identifier": "10.4064/ap-38-2-181-186",
        "human_match_rationale": (
            "The citation is attached at the theorem heading and is explicitly titled 'A "
            "generalization of the Malgrange–Zerner theorem'."
        ),
    },
    38: {
        "kind": "isbn",
        "normalized_identifier": "9783540418344",
        "human_match_rationale": (
            "Phelps's 'Lectures on Choquet's theorem' citation is used by the fixed page for both "
            "the compact-metrizable statement and the Bishop–de Leeuw nonmetrizable extension "
            "selected in the contiguous passage."
        ),
    },
    39: {
        "kind": "doi",
        "normalized_identifier": "10.1002/malq.19600060105",
        "human_match_rationale": (
            "Büchi's original 'Weak second order arithmetic and finite automata' paper is cited "
            "directly in the attribution sentence and matches the selected MSO/finite-automata "
            "equivalence."
        ),
    },
    42: {
        "kind": "doi",
        "normalized_identifier": "10.1080/09205071.2016.1169226",
        "human_match_rationale": (
            "The fixed article title explicitly names the Poincaré–Brouwer ('hairy ball') theorem, "
            "providing an unambiguous named-reference match to the selected even-sphere statement."
        ),
    },
    46: {
        "kind": "doi",
        "normalized_identifier": "10.1112/blms/11.3.268",
        "human_match_rationale": (
            "Beukers's cited paper is explicitly about the irrationality of zeta(2) and zeta(3), "
            "directly supporting the selected zeta(3) irrationality statement."
        ),
    },
    49: {
        "kind": "doi",
        "normalized_identifier": "10.4064/fm-47-1-57-103",
        "human_match_rationale": (
            "The Feferman–Vaught original paper title, 'The first order properties of products of "
            "algebraic systems', directly matches the selected first-order direct-product "
            "reduction."
        ),
    },
    51: {
        "kind": "doi",
        "normalized_identifier": "10.1007/978-3-031-26904-2_7",
        "human_match_rationale": (
            "The cited chapter is exactly titled 'Finite Injury (Friedberg-Muchnik Theorem)', so "
            "the named theorem and its incomparable c.e.-set construction are explicit."
        ),
    },
    54: {
        "kind": "doi",
        "normalized_identifier": "10.1016/j.laa.2008.09.027",
        "human_match_rationale": (
            "The fixed reference is explicitly titled 'A short proof of Gamas's theorem' and "
            "therefore directly names the selected tensor nonvanishing characterization."
        ),
    },
    55: {
        "kind": "doi",
        "normalized_identifier": "10.1007/978-1-4612-0871-6",
        "human_match_rationale": (
            "The captured Sagan citation explicitly says Theorem 1.3, page 6 contains the theorem "
            "statement and pages 97–98 contain 'Proof of Netto's Theorem'."
        ),
    },
    56: {
        "kind": "doi",
        "normalized_identifier": "10.1007/978-1-4614-1412-4_23",
        "human_match_rationale": (
            "The first Lehmann–Scheffé paper on completeness and unbiased estimation is the "
            "primary citation for the complete-sufficient-statistic UMVUE result selected here."
        ),
    },
    57: {
        "kind": "doi",
        "normalized_identifier": "10.1145/321864.321877",
        "human_match_rationale": (
            "Ladner's original 'On the Structure of Polynomial Time Reducibility' paper is the "
            "fixed primary reference for the selected conditional NP-intermediate existence "
            "statement."
        ),
    },
    58: {
        "kind": "doi",
        "normalized_identifier": "10.1016/j.aml.2013.04.005",
        "human_match_rationale": (
            "The citation title is exactly 'A topological proof of Sklar's theorem', directly "
            "binding it to the selected existence, uniqueness and converse statement."
        ),
    },
    60: {
        "kind": "isbn",
        "normalized_identifier": "9780521833783",
        "human_match_rationale": (
            "The Boyd–Vandenberghe citation, with pages 50–51, begins immediately after the exact "
            "selected supporting-hyperplane conclusion in the fixed wikitext."
        ),
    },
    61: {
        "kind": "doi",
        "normalized_identifier": "10.2307/1969503",
        "human_match_rationale": (
            "The candidate DOI occurs in the full fixed citation to Dilworth's original paper "
            "'A Decomposition Theorem for Partially Ordered Sets', an exact subject match for the "
            "selected finite-poset chain decomposition equality."
        ),
    },
    63: {
        "kind": "doi",
        "normalized_identifier": "10.1007/978-3-642-61798-0",
        "human_match_rationale": (
            "Gilbarg–Trudinger's 'Elliptic partial differential equations of second order' is "
            "listed under the fixed page's labeled Sources section for the Harnack principle and "
            "matches the selected harmonic-sequence statement's PDE scope."
        ),
    },
    64: {
        "kind": "isbn",
        "normalized_identifier": "0070006571",
        "human_match_rationale": (
            "The exact theorem sentence carries the fixed Ahlfors 1978 page-178 citation, and the "
            "candidate is the matching third-edition Ahlfors Complex Analysis bibliography entry "
            "with ISBN 0-07-000657-1."
        ),
    },
    65: {
        "kind": "doi",
        "normalized_identifier": "10.1119/1.10324",
        "human_match_rationale": (
            "The fixed paper title is 'Optical Theorem and Beyond', directly naming and matching "
            "the selected forward-amplitude/total-cross-section relation."
        ),
    },
}


noneligible_specs = {
    17: {
        "decision": "pending",
        "page_id": 2056790,
        "reason_code": "first_order_intro_only_rough_exact_passage_is_propositional_special_case",
        "rationale": (
            "The intro explicitly labels its first-order-oriented description 'Roughly stated'. "
            "The only exact Math theorem block is expressly a propositional-logic theorem, while "
            "the exact first-order section states Lyndon's stronger variant. The fixed revision "
            "therefore does not isolate an exact full Craig first-order statement without changing "
            "variant identity."
        ),
    },
    19: {
        "decision": "pending",
        "page_id": 55227,
        "reason_code": "complete_statement_but_reference_candidates_lack_exact_variant_binding",
        "rationale": (
            "The fixed page states both standard Baire category forms, but the candidate contexts "
            "are general topology/set-theory bibliography entries without a page, theorem number, "
            "or inline linkage to this exact two-form statement."
        ),
    },
    21: {
        "decision": "pending",
        "page_id": 49089,
        "reason_code": "cox_postulates_acknowledged_nonrigorous_missing_augmenting_assumptions",
        "rationale": (
            "Although the page lists postulates and probability-law implications, it explicitly "
            "says Cox's stated postulates are not mathematically rigorous and require various "
            "additional implicit or explicit assumptions for a valid theorem. The fixed revision "
            "does not pin one scope-complete hypothesis set."
        ),
    },
    23: {
        "decision": "reject",
        "page_id": 53993,
        "reason_code": "non_atomic_plural_sylow_theorem_collection",
        "rationale": (
            "The title and fixed page explicitly identify a collection: existence of Sylow "
            "p-subgroups, conjugacy/containment, and congruence/divisibility of their number are "
            "distinct assertions. A single atomic theorem credit cannot be assigned to this plural "
            "family row."
        ),
    },
    28: {
        "decision": "reject",
        "page_id": 45241,
        "reason_code": "non_atomic_isomorphism_theorem_family_across_structures",
        "rationale": (
            "The fixed page is a family inventory with multiple numbered theorems for groups and "
            "separate versions for rings, modules and universal algebra. The singular catalog label "
            "does not resolve one atomic claim."
        ),
    },
    30: {
        "decision": "pending",
        "page_id": 351853,
        "reason_code": "complete_statement_but_reference_candidates_lack_bounded_form_binding",
        "rationale": (
            "The bounded-convergence corollary is complete in the fixed page, but its candidates "
            "are bare identifiers or generic convergence-theorem texts without a captured binding "
            "to this exact bounded finite-measure form."
        ),
    },
    33: {
        "decision": "pending",
        "page_id": 1527098,
        "reason_code": "complete_formula_but_reference_candidates_do_not_bind_exact_formula",
        "rationale": (
            "The fixed gravity formula is complete, but the available candidate contexts concern "
            "history, Earth shape or applications and do not explicitly bind every term and scope "
            "of the selected Clairaut formula."
        ),
    },
    36: {
        "decision": "pending",
        "page_id": 7503941,
        "reason_code": "complete_statement_but_candidate_contexts_are_unreviewable_identifier_fragments",
        "rationale": (
            "The fixed Euclidean Jung radius bound is complete, but the reference candidates "
            "retain only bare DOI/ISBN fragments and no title, page, theorem number or inline "
            "linkage sufficient to audit the exact n-dimensional form."
        ),
    },
    43: {
        "decision": "pending",
        "page_id": 104790,
        "reason_code": "complete_statement_but_reference_candidates_lack_exact_euler_identity_binding",
        "rationale": (
            "The odd-parts/distinct-parts equinumerosity is complete in the fixed page, but the "
            "candidate bibliography contexts do not explicitly bind a page or theorem number to "
            "that exact Euler partition identity."
        ),
    },
    44: {
        "decision": "pending",
        "page_id": 3036126,
        "reason_code": "vafa_witten_intro_omits_full_hypotheses_page_flags_missing_statement",
        "rationale": (
            "The revision has only a qualitative intro and itself carries an expert-needed notice "
            "asking where the theorem statement is. It omits the technical hypotheses needed to "
            "turn its symmetry-breaking summary into a scope-complete theorem statement."
        ),
    },
    45: {
        "decision": "pending",
        "page_id": 9914115,
        "reason_code": "complete_statement_but_reference_candidates_lack_exact_resolution_binding",
        "rationale": (
            "The fixed characteristic-zero resolution statement is complete, but the candidate "
            "contexts do not explicitly identify the precise selected formulation rather than "
            "related resolution literature."
        ),
    },
    48: {
        "decision": "pending",
        "page_id": 19357539,
        "reason_code": "complete_statement_but_reference_candidates_lack_exact_variant_binding",
        "rationale": (
            "The fixed Lions–Lax–Milgram equivalence is complete, but the captured reference "
            "contexts do not explicitly bind this exact Hilbert/subspace/coercivity variant."
        ),
    },
    50: {
        "decision": "reject",
        "page_id": 632992,
        "reason_code": "non_atomic_paley_wiener_variant_family",
        "rationale": (
            "The fixed intro explicitly says 'a Paley-Wiener theorem', describes various original "
            "versions, and the page separately states holomorphic Fourier-transform and Schwartz "
            "distribution forms. This is a theorem family rather than one atomic claim."
        ),
    },
    52: {
        "decision": "reject",
        "page_id": 7635266,
        "reason_code": "non_atomic_krylov_bogolyubov_two_theorem_family",
        "rationale": (
            "The revision explicitly says the name may refer to either of two related fundamental "
            "theorems and separately formulates a single-map result and a Markov-process result. "
            "One catalog row cannot receive atomic theorem credit without disambiguation."
        ),
    },
    53: {
        "decision": "pending",
        "page_id": 40429150,
        "reason_code": "complete_statement_but_reference_candidates_lack_exact_ratio_binding",
        "rationale": (
            "The fixed quadratrix ratio is complete, but the available general historical "
            "references do not provide a captured page or theorem linkage to the exact AJ/AB "
            "equals 2/pi formulation."
        ),
    },
    59: {
        "decision": "pending",
        "page_id": 622844,
        "reason_code": "complete_statement_but_reference_candidates_lack_exact_pde_characterization_binding",
        "rationale": (
            "The fixed theorem block contains the full differentiable equivalence and converse, "
            "but the reference candidates are general texts without a captured page/theorem "
            "binding to this exact PDE characterization."
        ),
    },
}


assert set(reference_specs) | set(noneligible_specs) == set(pending)
assert set(reference_specs).isdisjoint(noneligible_specs)
records = []
for index in pending:
    base = review_by_index[index]
    external_id = base["identity"]["synthetic_source_id"]
    resolved_ids = identity_resolution[external_id]["resolved_page_ids"]
    record = {
        "index": index,
        "title": base["identity"]["title"],
        "original_decision": "pending",
        "grants_new_catalog_entry": False,
        "formal_proof_claimed": False,
    }
    if index in reference_specs:
        spec = eligible_specs[index]
        assert spec["page_id"] in resolved_ids, (index, spec["page_id"], resolved_ids)
        page = pages[spec["page_id"]]
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
                    external_id,
                    page,
                    reference_specs[index],
                ),
            }
        )
    else:
        spec = noneligible_specs[index]
        assert spec["page_id"] in resolved_ids, (index, spec["page_id"], resolved_ids)
        page = pages[spec["page_id"]]
        record.update(
            {
                "decision": spec["decision"],
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
                    "source_field": "wikitext",
                    "source_field_sha256": page["wikitext_sha256"],
                    "reference_asset": str(REFERENCE_ASSET.relative_to(REPO)),
                    "reference_asset_sha256": REFERENCE_ASSET_SHA256,
                    "reference_authority_sha256": REFERENCE_AUTHORITY_SHA256,
                },
                "evidence": None,
                "reference_evidence": None,
            }
        )
    records.append(record)


assert [row["index"] for row in records] == pending
assert sum(row["decision"] == "eligible" for row in records) == 24
assert sum(row["decision"] == "reject" for row in records) == 4
assert sum(row["decision"] == "pending" for row in records) == 12
assert all(row["grants_new_catalog_entry"] is False for row in records)
assert all(row["formal_proof_claimed"] is False for row in records)

OUTPUT.write_text(
    json.dumps(records, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
    encoding="utf-8",
)

# Revalidate exact character and UTF-8 byte slices from the serialized artifact.
loaded = json.loads(OUTPUT.read_text(encoding="utf-8"))
for row in loaded:
    if row["decision"] != "eligible":
        assert row["evidence"] is None
        assert row["reference_evidence"] is None
        continue
    ev = row["evidence"]
    page = pages[ev["page_id"]]
    text = page[ev["source_field"]]
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
            "eligible": 24,
            "reject": 4,
            "pending": 12,
        },
        sort_keys=True,
    )
)
