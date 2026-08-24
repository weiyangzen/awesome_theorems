#!/usr/bin/env python3
"""Build the fixed-source existing-entry theorem review for indices 134..200.

This is a quality-only overlay review.  It cannot allocate an identity, append a
catalog row, alter release 5.4, or grant a new theorem/conjecture credit.
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
OUTPUT = AUDIT / "range_reviews/wiki-reference-review-134-200.json"

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
    135, 136, 137, 138, 139, 140, 141, 142, 143, 145, 146, 147, 148,
    149, 150, 151, 152, 153, 155, 156, 157, 158, 159, 160, 161, 165,
    167, 168, 169, 171, 172, 173, 174, 176, 177, 179, 180, 182, 183,
    184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196,
    197, 199,
]


def eligible(
    start: str,
    *,
    end: str | None = None,
    end_before: str | None = None,
    reference_kind: str,
    reference_id: str,
    completeness: str,
    reference_rationale: str,
) -> dict:
    return {
        "start": start,
        "end": end,
        "end_before": end_before,
        "reference_kind": reference_kind,
        "reference_id": reference_id,
        "completeness": completeness,
        "reference_rationale": reference_rationale,
    }


ELIGIBLE_SPECS = {
    136: eligible(
        "The '''Rybczynski theorem''' was developed",
        end="and an absolute decline of the output of the other good.",
        reference_kind="doi", reference_id="10.2307/2551188",
        completeness="The passage fixes constant relative goods prices, changes one factor endowment, and states both sector-output conclusions.",
        reference_rationale="Rybczynski's 1955 paper is the original fixed citation for the factor-endowment/output result stated in the passage.",
    ),
    137: eligible(
        "==Statement of the theorem==",
        end="<math>H_*(C_*(X \\times Y)) \\cong H_*(C_*(X) \\otimes C_*(Y)).</math>",
        reference_kind="doi", reference_id="10.2307/2372629",
        completeness="The section specifies the spaces, chain complexes, tensor differential, natural chain maps, homotopies, and resulting homology isomorphism.",
        reference_rationale="Eilenberg and Zilber's original paper 'On Products of Complexes' directly matches the selected product-chain theorem.",
    ),
    138: eligible(
        "{{Math theorem\n|name = {{visible anchor|Riesz representation theorem}}",
        end_before="\n\n{{Math theorem\n| name = Corollary",
        reference_kind="isbn", reference_id="9780387728285",
        completeness="The theorem box fixes the Hilbert-space convention and gives existence, uniqueness, the representation formula, norm identity, and minimum-norm characterization.",
        reference_rationale="The selected theorem carries the inline Roman 2008, Theorem 13.32 citation; the captured ISBN is that exact Advanced Linear Algebra edition.",
    ),
    141: eligible(
        "==Statement of the theorem==",
        end_before="\n==Notes==",
        reference_kind="doi", reference_id="10.1090/s0002-9904-1956-10036-0",
        completeness="The section quantifies the finite exponent and infinite cardinal, defines the iterated exponential, states the partition relation and sharpness, and expands the arrow notation.",
        reference_rationale="Erdős and Rado's fixed 1956 paper 'A partition calculus in set theory' is the primary source for the selected partition theorem.",
    ),
    142: eligible(
        "The Kronecker–Weber theorem can be stated in terms of",
        end="a field obtained by adjoining a [[root of unity]] to the rational numbers.",
        reference_kind="doi", reference_id="10.2307/2319208",
        completeness="The passage gives both the finite-abelian-extension hypothesis and the cyclotomic-subfield conclusion in field-theoretic form.",
        reference_rationale="Greenberg's cited article is explicitly titled 'An Elementary Proof of the Kronecker-Weber Theorem'.",
    ),
    147: eligible(
        "In [[abstract algebra]], '''Hilbert's Theorem 90'''",
        end="<math>a=b/\\sigma(b).</math></blockquote>",
        reference_kind="doi", reference_id="10.1515/crll.1855.50.212",
        completeness="The passage fixes a cyclic Galois extension, generator, norm-one element, and the exact coboundary conclusion.",
        reference_rationale="The page identifies Kummer's 1855 paper as the original source of this basic cyclic form, and the selected DOI is that paper.",
    ),
    148: eligible(
        "In [[functional analysis]], a branch of mathematics, the '''Ryll-Nardzewski fixed-point theorem'''",
        end="fixed]] by each map in the set.)",
        reference_kind="doi", reference_id="10.1090/s0002-9904-1967-11779-8",
        completeness="The passage states the normed-space, nonempty convex weakly compact set, affine-isometry semigroup, and common-fixed-point conclusion.",
        reference_rationale="Namioka and Asplund's fixed article is explicitly titled 'A geometric proof of Ryll-Nardzewski's fixed point theorem'.",
    ),
    149: eligible(
        "In [[geometry]], '''Euler's theorem''' states",
        end="(the radii of the [[circumscribed circle]] and [[inscribed circle]] respectively).",
        reference_kind="isbn", reference_id="9780883855584",
        completeness="The passage states both equivalent distance identities and defines the circumcenter/incenter distance and both radii.",
        reference_rationale="The formula is tagged with the Dunham citation; the captured ISBN is the cited edition and page 300.",
    ),
    150: eligible(
        "'''Frucht's theorem''' is a result",
        end="is [[group isomorphism|isomorphic]] to <math> G </math>.",
        reference_kind="doi", reference_id="10.4153/cjm-1949-033-6",
        completeness="The passage quantifies every finite group and gives both finite-graph realization and the stronger infinite family of connected simple realizations.",
        reference_rationale="Frucht's cited 1949 paper constructs degree-three graphs with a prescribed abstract group, directly supporting the selected realization statement.",
    ),
    153: eligible(
        "==Statement==",
        end_before="\n===Effective version===",
        reference_kind="doi", reference_id="10.1007/bf01206606",
        completeness="The section fixes a finite Galois extension, conjugation-stable subset, unramified primes, Frobenius classes, and both natural/analytic density conclusion.",
        reference_rationale="Chebotarev's fixed original paper is explicitly about the density of primes belonging to a substitution class and is cited on the page.",
    ),
    156: eligible(
        "==General formulation==",
        end_before="\n==Derivation==",
        reference_kind="doi", reference_id="10.1103/physrev.83.34",
        completeness="The section defines the observable, equilibrium spectrum, perturbing field and susceptibility, then states the classical frequency-domain relation and its quantum replacement.",
        reference_rationale="The page identifies Callen and Welton's 1951 'Irreversibility and Generalized Noise' as the proof of the fluctuation–dissipation theorem and cites it again for the generalization.",
    ),
    158: eligible(
        "Parseval's theorem can also be expressed as follows:",
        end="<math display=\"block\">\\frac{1}{\\pi} \\int_{-\\pi}^{\\pi} f^2(x) \\,\\mathrm{d}x = \\tfrac12 a_0^2 + \\sum_{n=1}^{\\infty} \\left(a_n^2 + b_n^2 \\right).</math>",
        reference_kind="isbn", reference_id="0201578883",
        completeness="The passage fixes square integrability, the real Fourier-series convention, and the exact coefficient/integral identity.",
        reference_rationale="The equality is immediately preceded by the Kaplan Advanced Calculus page-519 citation captured under this ISBN.",
    ),
    160: eligible(
        "==Statement of the theorem==",
        end_before="\n===Proof===",
        reference_kind="doi", reference_id="10.2307/1969855",
        completeness="The section specifies an n-connected pointed CW/simplicial space, the suspension-loop map, and the exact isomorphism and epimorphism ranges.",
        reference_rationale="Whitehead's fixed paper is explicitly titled 'On the Freudenthal Theorems' and is listed as a source for this statement.",
    ),
    161: eligible(
        "In [[mathematics]], the '''well-ordering theorem'''",
        end="|isbn=1-4020-0198-3 }}</ref>",
        reference_kind="isbn", reference_id="1402001983",
        completeness="The passage says every set admits a strict total order in which every nonempty subset has a least element, and records equivalence to choice.",
        reference_rationale="The exact introductory statement is followed by the fixed Encyclopaedia of Mathematics page-458 citation captured under this ISBN.",
    ),
    165: eligible(
        "It states the following:\n\nDenoting by '''C'''",
        end="those poles lie in ''A''.",
        reference_kind="doi", reference_id="10.1007/bf02400416",
        completeness="The passage fixes the compact set, holomorphic neighborhood, one allowed pole per complement component, uniform approximation, and pole restriction.",
        reference_rationale="Runge's 1885 original paper is cited immediately before the selected statement and is the fixed primary reference.",
    ),
    167: eligible(
        "In the [[mathematics]] of [[Lie theory]], '''Lie's third theorem'''",
        end="The theorem is part of the [[Lie group–Lie algebra correspondence]].",
        reference_kind="doi", reference_id="10.1007/978-3-642-56936-4",
        completeness="The passage quantifies every finite-dimensional real Lie algebra and concludes the existence of an associated Lie group.",
        reference_rationale="Duistermaat and Kolk's cited Lie Groups volume is attached to a constructive proof that builds the integrating Lie group.",
    ),
    168: eligible(
        "Let ''G'' be a compact group. The theorem has three parts.",
        end="this last result is simply a standard result from [[Fourier series]].",
        reference_kind="doi", reference_id="10.1007/bf01447892",
        completeness="The passage states density of matrix coefficients, complete reducibility, regular-representation decomposition, and the orthonormal-basis conclusion for compact groups.",
        reference_rationale="Peter and Weyl's 1927 original paper is the fixed primary citation for the compact-group completeness theorem.",
    ),
    169: eligible(
        "<blockquote>'''[[Nelson Dunford|Dunford]]–[[Billy James Pettis|Pettis]] theorem'''",
        end="</blockquote>",
        reference_kind="doi", reference_id="10.1090/s0002-9947-1938-1501971-x",
        completeness="The block fixes a sigma-finite measure space and an L1 family, and states equivalence between weak compact closure and uniform integrability.",
        reference_rationale="Dunford's 1938 'Uniformity in linear spaces' paper is cited directly in the theorem label and statement.",
    ),
    173: eligible(
        "== Statement of the theorem ==",
        end_before="\n==Version for the real line==",
        reference_kind="isbn", reference_id="9783642971464",
        completeness="The section specifies the smooth Jordan curve, analytic density, Cauchy-type integral, interior/exterior limits, principal value, and both boundary formulas.",
        reference_rationale="Kress's Linear Integral Equations page 88 is cited in the theorem introduction and captured under this exact ISBN.",
    ),
    174: eligible(
        "In [[quantum field theory]] and [[statistical mechanics]], the '''Hohenberg–Mermin–Wagner theorem'''",
        end="in dimensions {{math|''d'' ≤ 2}}.",
        reference_kind="doi", reference_id="10.1007/s10955-018-2202-y",
        completeness="The passage states the continuous-symmetry, finite-temperature, sufficiently-short-range-interaction hypotheses and the no-spontaneous-breaking conclusion in d <= 2.",
        reference_rationale="Halperin's fixed review explicitly names the Hohenberg–Mermin–Wagner theorem and its limitations and is cited for the rigorous result.",
    ),
    179: eligible(
        "== Formal description ==",
        end_before="\n== Physical / heuristic point of view ==",
        reference_kind="doi", reference_id="10.1007/s10773-005-8977-z",
        completeness="The formal section states both modern parts, including invariance/vacuum assumptions and the Wightman-function and free-field conclusions.",
        reference_rationale="Lupher's cited article is explicitly titled 'Who proved Haag's theorem?' and discusses the multiple precise formulations selected here.",
    ),
    180: eligible(
        "==Statement==",
        end_before="\n== Proof ==",
        reference_kind="doi", reference_id="10.1080/00029890.2008.11920532",
        completeness="The section fixes three noncollinear cubic zeros, the unique midpoint-tangent Steiner inellipse, and identifies its foci with the derivative zeros.",
        reference_rationale="Kalman's fixed article is explicitly titled 'An Elementary Proof of Marden's Theorem'.",
    ),
    182: eligible(
        "==Lindemann–Weierstrass theorem ==",
        end_before="\n===Proof===",
        reference_kind="doi", reference_id="10.1017/cbo9781139093835",
        completeness="The theorem box quantifies nonzero algebraic coefficients and distinct algebraic exponents and states the nonvanishing exponential sum.",
        reference_rationale="Baker's Comprehensive Course in Number Theory, page 53, is cited inside the exact selected reformulation and has the captured DOI.",
    ),
    183: eligible(
        "The theorem states that for [[almost all]] real numbers",
        end="{{OEIS|id=A086819}}.",
        reference_kind="doi", reference_id="10.1007/bf02993063",
        completeness="The passage fixes almost every real in (0,1), defines decimal places and continued-fraction terms, and gives their exact asymptotic ratio.",
        reference_rationale="Lochs's 1964 original paper on comparing decimal and continued-fraction accuracy is cited immediately before the statement.",
    ),
    184: eligible(
        "==Statement==",
        end_before="\n==See also==",
        reference_kind="isbn", reference_id="1568811624",
        completeness="The section defines the weighted prime count and error variance and gives the uniform Q-range, big-O estimate, and historical parameter variants.",
        reference_rationale="Hooley's captured book chapter is explicitly titled 'On theorems of Barban-Davenport-Halberstam type'.",
    ),
    185: eligible(
        "In [[model theory]], the notion of a categorical theory",
        end="then it is categorical in all uncountable cardinalities.",
        reference_kind="doi", reference_id="10.2307/1994188",
        completeness="The passage defines kappa-categoricity and states the countable-language, one-uncountable-cardinal hypothesis and all-uncountable-cardinals conclusion.",
        reference_rationale="Morley's original 1965 paper 'Categoricity in Power' is the fixed primary source for this theorem.",
    ),
    187: eligible(
        "The theorem is stated as follows: Let {{mvar|ABCD}}",
        end="{{r|Alsina|Honsberger}}",
        reference_kind="isbn", reference_id="9781470454654",
        completeness="The passage fixes a non-parallelogram convex quadrilateral, diagonal midpoints and interior point, then gives the area equality and Newton-line conclusion.",
        reference_rationale="The theorem introduction and conclusion cite Alsina–Nelsen; the captured book gives exact pages 12–13 for this result.",
    ),
    188: eligible(
        "Let ''ABCD'' be a tangential quadrilateral",
        end="connecting the midpoints of the diagonals.{{r|alsina}}",
        reference_kind="isbn", reference_id="9780883853481",
        completeness="The passage specifies the non-rhombus tangential quadrilateral, both diagonal midpoints and incircle center, and the collinearity conclusion.",
        reference_rationale="The selected statement carries the Alsina citation; the captured Charming Proofs entry identifies pages 117–118.",
    ),
    189: eligible(
        "==Statement==",
        end_before="\n==Application==",
        reference_kind="doi", reference_id="10.1007/bf01214300",
        completeness="The section constructs two squares sharing a vertex, defines all four derived midpoints/centers, and concludes the resulting quadrilateral is a square.",
        reference_rationale="The page identifies Finsler and Hadwiger's 1937 original paper, specifically page 324, as the publication of this theorem.",
    ),
    190: eligible(
        "==Statement of the theorem==",
        end_before="\n==Variants of the theorem==",
        reference_kind="doi", reference_id="10.2140/pjm.1961.11.679",
        completeness="The section fixes a linear operator on a Banach-space subspace and gives all three necessary-and-sufficient generator conditions.",
        reference_rationale="Lumer and Phillips's original 'Dissipative operators in a Banach space' paper is the fixed primary reference.",
    ),
    191: eligible(
        "This theorem is about the existence of solutions to a system",
        end="has a unique analytic solution ''ƒ''&nbsp;:&nbsp;''W''&nbsp;→&nbsp;''V'' near&nbsp;0.",
        reference_kind="isbn", reference_id="0691043612",
        completeness="The passage fixes real/complex finite dimensions, analytic coefficient maps, the quasilinear PDE and zero initial hypersurface, and local analytic existence and uniqueness.",
        reference_rationale="Folland's fixed Introduction to Partial Differential Equations entry links directly to a Cauchy–Kowalevski search and is a theorem-specific source on this page.",
    ),
    192: eligible(
        "Let <math>X </math> be a Hausdorff [[locally convex topological vector space]]",
        end="then it is countably additive (in the original topology of the space <math>X </math>).",
        reference_kind="doi", reference_id="10.2140/pjm.1967.22.297",
        completeness="The passage defines subseries convergence and states the equivalent weak-to-strong series and vector-measure forms for a Hausdorff locally convex space.",
        reference_rationale="McArthur's fixed paper is explicitly titled 'On a theorem of Orlicz and Pettis' and is cited as a direct proof of the selected locally convex form.",
    ),
    193: eligible(
        "==Matiyasevich's theorem==",
        end_before="\nIt is easy to see that every Diophantine set is computably enumerable:",
        reference_kind="isbn", reference_id="0262132958",
        completeness="The section states the computably-enumerable iff Diophantine equivalence and expands both sides with the halting and integer-polynomial quantifiers.",
        reference_rationale="Matiyasevich's own fixed monograph 'Hilbert's 10th Problem' is the theorem-specific reference captured under this ISBN.",
    ),
    194: eligible(
        "In [[number theory]], '''Hurwitz's theorem'''",
        end="<math display=\"block\">\\left |\\xi-\\frac{m}{n}\\right | < \\frac{1}{\\sqrt{5}\\, n^2}.</math>",
        reference_kind="doi", reference_id="10.1007/bf01206656",
        completeness="The passage quantifies every irrational number and infinitely many coprime numerator/denominator pairs and states the sharp-form approximation bound.",
        reference_rationale="Hurwitz's 1891 original paper on rational approximation is the fixed primary citation.",
    ),
    195: eligible(
        "In [[Euclidean plane]] [[geometry]], '''Lester's theorem'''",
        end="lie on the same circle.",
        reference_kind="doi", reference_id="10.1017/s0025557200178581",
        completeness="The single sentence fixes a scalene triangle and all four named centers/points and states their concyclicity.",
        reference_rationale="Duff's captured paper is explicitly titled 'A short projective proof of Lester's theorem'.",
    ),
    196: eligible(
        "The '''Steiner–Lehmus theorem''', a [[theorem]] in [[elementary geometry]]",
        end=": ''Every [[triangle]] with two [[angle bisector]]s of equal lengths is [[isosceles]]''.",
        reference_kind="doi", reference_id="10.1215/00294527-2017-0019",
        completeness="The passage quantifies every triangle, states equality of two angle-bisector lengths, and concludes isoscelesness.",
        reference_rationale="Pambuccian's captured paper is explicitly titled 'Negation-free and contradiction-free proof of the Steiner-Lehmus theorem'.",
    ),
    197: eligible(
        "==The theorem==",
        end=".<ref name=\"bpr\" />",
        reference_kind="doi", reference_id="10.2307/3028551",
        completeness="The passage defines the Sturm chain and sign variation and states the exact root count on a half-open interval for square-free real polynomials.",
        reference_rationale="The fixed article 'Sturm's Theorem for Multiple Roots' explicitly names and treats the same root-count theorem and its non-square-free extension.",
    ),
    199: eligible(
        "== Definition ==",
        end_before="\n=== Integral form ===",
        reference_kind="doi", reference_id="10.1098/rstl.1884.0016",
        completeness="The section states the local energy-transfer balance, gives the differential equation, and defines energy density, Poynting flux and charge-work terms.",
        reference_rationale="Poynting's original 1884 'On the Transfer of Energy in the Electromagnetic Field' paper is cited immediately before the selected law.",
    ),
}

OTHER_SPECS = {
    135: ("pending", "reference_candidate_missing", "The page contains an exact alternate-angle implication, but the fixed reference-candidate row has zero candidates; no independently bound reference can be promoted."),
    139: ("pending", "reference_candidate_missing", "The page states the real finite-dimensional associative division-algebra classification, but its fixed reference-candidate row is empty."),
    140: ("pending", "reference_candidate_missing", "The page gives classical and Radon-space forms of Lusin's theorem, but no fixed reference candidate is available for the required independent match."),
    143: ("pending", "reference_candidate_missing", "The page gives Casey's exact tangent-length identity, but its fixed reference-candidate row has zero candidates."),
    145: ("reject", "non_atomic_proved_and_conjectural_no_hair_family", "The page's general mass/charge/angular-momentum identity is presented as a conjectural or heuristic slogan, while rigorous results require differing restrictions and the page also records counterexamples; this is not one proved atomic theorem."),
    146: ("pending", "exact_franel_landau_reference_not_captured", "The Farey-sequence page states both Franel and Landau equivalences, but their original citations have no captured identifier and the available candidates concern other Farey results."),
    151: ("reject", "non_atomic_spectral_theorem_variant_family", "The page explicitly treats many finite-dimensional, compact, bounded, unbounded and multiplication-operator spectral theorems; the unsuffixed row does not identify one atomic hypotheses/conclusion pair."),
    152: ("pending", "reference_candidate_missing", "The Brahmagupta geometry statement is present, but the fixed reference-candidate row is empty."),
    155: ("pending", "exact_busy_beaver_five_proof_reference_not_captured", "The pinned page gives exact S(5), space(5), and Sigma(5) values, but the 2025 proof citation falls outside the capped candidate asset and the captured older references do not prove the exact result."),
    157: ("reject", "resolved_page_lacks_max_noether_statement", "The identity resolves to the broad Algebraic surface page, which contains no complete statement of the named Max Noether theorem."),
    159: ("reject", "plural_singularity_theorem_family_not_atomic", "The page discusses a family of Penrose, Hawking and Hawking–Penrose singularity theorems with differing assumptions and conclusions rather than one atomic theorem statement."),
    171: ("reject", "cpctc_is_mnemonic_definition_not_theorem", "The selected passage expands CPCTC as a mnemonic restatement of the definition of congruent triangles, not a standalone truth-apt theorem with independent mathematical content."),
    172: ("pending", "exact_bezout_statement_reference_match_not_closed", "The page gives exact plane and projective forms, but captured candidates are historical/general references or variants; the fixed evidence does not close an exact statement-to-reference match."),
    176: ("pending", "reeh_schlieder_reference_match_not_closed", "The page gives a complete cyclic-vacuum statement, while captured candidates concern implications and later extensions rather than a directly bound source for that exact statement."),
    177: ("pending", "perron_frobenius_reference_match_not_closed", "The page gives several complete positive/nonnegative matrix forms, but captured candidates attach to applications or later properties and do not close a direct match to the selected main form."),
    186: ("pending", "reference_candidate_missing", "The page states Van Schooten's exact equilateral-triangle identity, but the fixed reference-candidate row is empty."),
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
    text = page["wikitext"]
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
    passage = text[start:end]
    byte_start = len(text[:start].encode("utf-8"))
    byte_end = len(text[:end].encode("utf-8"))
    assert text.encode("utf-8")[byte_start:byte_end].decode("utf-8") == passage
    return {
        "asset": rel(WIKIPEDIA),
        "asset_sha256": FIXED_INPUT_SHA256[WIKIPEDIA],
        "source_field": "wikitext",
        "source_field_sha256": page["wikitext_sha256"],
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
        "offset_basis": "zero-based offsets into exact pinned wikitext; end is exclusive",
        "completeness": spec["completeness"],
    }


def page_bindings(resolution: dict, pages: dict[int, dict]) -> list[dict]:
    result = []
    for page_id in resolution["resolved_page_ids"]:
        page = pages[page_id]
        result.append({
            "page": page["resolved_title"],
            "page_id": page_id,
            "revision_id": page["revision_id"],
            "revision_timestamp": page["revision_timestamp"],
            "mediawiki_revision_sha1": page["mediawiki_revision_sha1"],
            "wikitext_sha256": page["wikitext_sha256"],
            "attribution_url": page["attribution_url"],
        })
    return result


def exact_reference(
    parent: dict,
    page: dict,
    spec: dict,
    reference_parent: dict,
    wikipedia_rights: dict,
    openalex_by_doi: dict[str, dict],
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
        if 134 <= row["source_index"] <= 200 and row["review_disposition"] == "pending"
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
        assert len(page_rows) == 1, (index, resolution["resolved_page_ids"])
        page = page_rows[0]
        reference_parent = reference_by_source[parent["source_record_id"]]
        assert canonical_row_sha256(reference_parent) == reference_parent["row_sha256"]
        assert reference_parent["row_sha256"] == parent["reference_candidate_entry"]["asset_row_sha256"]

        spec = ELIGIBLE_SPECS.get(index)
        if spec is not None:
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
        "eligible_existing_quality_credit": sum(r["decision"] == "eligible" for r in records),
        "pending": sum(r["decision"] == "pending" for r in records),
        "reject": sum(r["decision"] == "reject" for r in records),
        "new_catalog_entries": 0,
        "new_release_theorem_credits": 0,
        "strict_conjecture_credits": 0,
        "formal_proofs_claimed": 0,
    }
    assert counts == {
        "rows": 54,
        "eligible_existing_quality_credit": 38,
        "pending": 11,
        "reject": 5,
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
            "source_index_range": [134, 200],
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
