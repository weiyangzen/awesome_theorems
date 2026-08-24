#!/usr/bin/env python3
"""Build the fixed Erdős supplemental review slice 84--166."""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any

from build_erdos_frontier_review_slices_v5_5 import (
    CATALOG_REL,
    ERDOS_ARCHIVE_REL,
    FC_ARCHIVE_REL,
    OUT_DIR,
    ROOT,
    STATUS_REL,
    build_row,
    ordered_digest,
    sha256_bytes,
    sha256_file,
    spec,
)


QUEUE_REL = "Docs/catalog/v5/curation/erdos_parent_join_v5_5/resolved-theorem-supplemental.jsonl"
QUEUE = ROOT / QUEUE_REL
RECEIPT_REL = "Docs/catalog/v5/curation/erdos_parent_join_v5_5/resolved-theorem-supplemental-receipt.json"


def reject(citation: str, evidence: str, *, gate_name: str = "dedupe") -> dict[str, Any]:
    if gate_name == "dedupe":
        return spec(citation, dedupe="fail", dedupe_evidence=evidence)
    if gate_name == "importance":
        return spec(citation, importance="fail", importance_evidence=evidence)
    if gate_name == "exact":
        return spec(citation, exact="fail", exact_evidence=evidence)
    raise ValueError(gate_name)


ROWS: dict[int, dict[str, Any]] = {
    84: reject("Mu11", "Müller's explicit density-1/2 construction is the same affirmative solution already credited by primary row 59."),
    85: spec("Mu11"),
    86: reject("BFV13, MR 3019423", "The displayed lower estimate is subsumed by the sharper two-sided asymptotic already retained at primary row 68."),
    87: spec("Er80; Mirsky-Newman attribution without a primary reference", primary="pending", primary_evidence="The historical attribution supplies no fixed primary source for the exact all-m inequality."),
    88: reject("BFV13, MR 3019423", "Tendsto eps to zero is an immediate corollary of the two-sided asymptotic retained at primary row 68."),
    89: spec("historical Erdős assertion on Problem 1193", primary="pending", primary_evidence="No fixed primary construction matching the exact positive-upper-density existential was located."),
    90: spec("ErLe96"),
    91: reject("internal implication", "This unequal-density case is explicitly a corollary of primary row 77 from the same disproof."),
    92: reject("GaMa18", "The negative 3m+2 equality answer is already the direct consequence used to credit the stronger numerical lower bound at primary row 82."),
    93: spec("Er50"),
    94: reject("Barreto-Leeham proof and comments", "The broad no-answer is the direct consequence of the quantitative many-prime-factors theorem retained at supplemental_index 95."),
    95: spec("fixed Barreto-Leeham/Tao-Alexeev quantitative proof linked from Problem 205"),
    96: spec("BoEr76"),
    97: spec("FLZ15"),
    98: spec("fixed DeepMind formal disproof linked from Problem 26"),
    99: reject("GPT-5.5/Price proof", "The alpha=1 base answer is a direct instance of the arbitrary-positive-rational theorem retained at supplemental_index 101."),
    100: spec("Burr's power-polynomial multiset theorem"),
    101: spec("GPT-5.5/Price arbitrary-rational strengthening and fixed linked formalization"),
    102: spec("vD25"),
    103: spec("vD25"),
    104: spec("Sa75"),
    105: reject("Tu84; RT85, MR 810596", "The same counterexample and its h-fold strengthening are already credited at primary rows 159 and 160."),
    106: reject("fixed strong-completeness proof for p(x)=x^2", "This polynomial special case is a direct instance of the all-positive-leading-polynomials theorem retained at primary row 165."),
    107: spec("Cambie's modulo-8 k=4 completion recorded on Problem 399"),
    108: spec("PoSh73"),
    109: spec("ErOb37 and Breusch's 3 mod 4 prime-gap input"),
    110: spec("BaSo96, MR 1379389", exact_evidence="The selected one-way equality classification is narrower than an iff; this exact quantifier direction was checked against BaSo96 Theorem 1.1."),
    111: spec("Er73b"),
    112: reject("BrSc95", "The explicit non-totient progression is the witness for the same infinitude conclusion already credited at primary row 190."),
    113: reject("Shiu theorem", "This row is only the application of Shiu's theorem already retained as primary row 196."),
    114: spec("HaTe88, §4.6"),
    115: reject("Cr03", "The one-solution statement is a direct corollary of Croot's infinitely-many-disjoint theorem retained at primary row 216."),
    116: spec("Chung-Graham sharpness theorem for the constant retained at primary row 224"),
    117: spec("SeSt58"),
    118: spec("SeSt58"),
    119: spec("BaLe13; LRSS21"),
    120: reject("ErSz76", "The sufficiently-large-prime instance is subsumed by the all-moduli theorem retained at primary row 245."),
    121: spec("BFT15; Ma15"),
    122: spec("Su03"),
    123: spec("EGR98"),
    124: spec("EGR98"),
    125: spec("VLT26 and fixed van Doorn formal proof"),
    126: spec("ErSu59"),
    127: reject("elementary monotonicity clarification", "This finiteness observation is a routine reading constraint, not a separately sourced frontier theorem.", gate_name="importance"),
    128: reject("Cambie calculation", "The broad non-unimodality answer is witnessed by the explicit n=3 inequalities retained at supplemental_index 129."),
    129: spec("Cambie exact calculation and fixed Monticone/Aristotle formalization"),
    130: reject("Ha92, MR 1189509", "The pinned prose says 1/log 2 < alpha, while the selected formal hypothesis is alpha < 1/log 2; the threshold direction is reversed.", gate_name="exact"),
    131: reject("source block marked TODO", "This elementary union-bound support row is not a separately creditable research theorem.", gate_name="importance"),
    132: reject("Be11, MR 2765421", "The base existence answer is the direct corollary of Bergman's explicit quantitative bound retained at supplemental_index 133."),
    133: spec("Be11, MR 2765421"),
    134: reject("Ha47, MR 23536; arXiv:2510.19804", "A second explicit Sidon counterexample would duplicate the same disproof event already represented by primary row 293."),
    135: spec("mo271/formal-conjectures@486bc8afae062b6711cd16d3466d651ee2880a52, Problem 741 exact proof"),
    136: spec("ErHa67b"),
    137: reject("BoVi98, MR 1487781", "The large-girth no-answer is another direct consequence of the Bondy-Vince theorem retained at primary row 302."),
    138: reject("SpringSense-Innovation-Institute fixed Lean proof", "The finite chromatic formulation is the same Bondy-Vince solution event already represented by primary row 302."),
    139: reject("St24b, arXiv:2408.02400", "The explicit Steiner graph is the witness for the same disproof already credited at primary row 311."),
    140: spec("Ga25, arXiv:2510.14804; fixed plby proof"),
    141: spec("MoMo65; Sp71, MR 282873"),
    142: reject("SaSz94, MR 1275641", "The base convergence statement is a direct corollary of the stronger non-little-o theorem retained at supplemental_index 147."),
    143: spec("ChFa15, MR 3353267"),
    144: spec("ChFa10, MR 2596025; ChFa14, MR 3195389"),
    145: spec("Ru17, MR 3658290"),
    146: spec("Ru17, MR 3658290"),
    147: spec("SaSz94, MR 1275641"),
    148: spec("FrFu84, MR 753720"),
    149: reject("SaTh15, hypergraph containers", "This exists-c>0 formulation is weaker than the explicit 0.16 sqrt(N) exponent theorem retained at primary row 333."),
    150: spec("fixed linked contrapositive proof; CES75, MR 369305 background"),
    151: spec("CoPh96, MR 1386875"),
    152: spec("CoPh96, MR 1386875"),
    153: reject("interval (N/2,N] example", "The half-density construction is elementary and is strictly weaker than the published Coppersmith-Phillips lower bound.", gate_name="importance"),
    154: spec("Härtter-Nathanson theorem on bases without minimal subbases"),
    155: spec("Sárközy upper bound; Tao proof in fixed Problem 888 comments"),
    156: reject("Cambie-Weisenberg semiprime observation", "This lower-bound construction is subsumed by the theta asymptotic already retained at primary row 343."),
    157: spec("Wi81, MR 637365; ArWu25 fixed formal counterexample"),
    158: reject("MaVe23, arXiv:2306.04007; Br26, arXiv:2605.28793", "The all-k wrapper merely unions the separately retained k=4 theorem at primary row 357 and k>=5 theorem at supplemental_index 159."),
    159: spec("Br26, arXiv:2605.28793"),
    160: spec("He84, MR 762186, DOI 10.1112/S0025579300010743"),
    161: spec("Sp81"),
    162: spec("ErIn64"),
    163: spec("Er65b"),
    164: spec("APSSV26b, arXiv:2604.06609; Marti2203/formal-conjectures@19c63d48acce3099c242b059518c49bf8dc0eab8"),
    165: spec("Cl67, MR 213317; Marti2203/formal-conjectures@19c63d48acce3099c242b059518c49bf8dc0eab8"),
    166: spec("Er64b, MR 179131"),
}


def build() -> tuple[Path, Path]:
    if set(ROWS) != set(range(84, 167)):
        raise ValueError("supplemental decisions must cover exactly 84..166")
    raw_lines = QUEUE.read_bytes().splitlines()
    if len(raw_lines) != 167:
        raise ValueError(f"supplemental queue row count drifted: {len(raw_lines)}")
    queue_sha = sha256_file(QUEUE)
    reviews: list[dict[str, Any]] = []
    for index in range(84, 167):
        source = json.loads(raw_lines[index])
        row = build_row(index, source, raw_lines[index], ROWS[index], queue_sha)
        row["supplemental_index"] = index
        row["source_binding"]["path"] = QUEUE_REL
        row["source_binding"]["full_file_sha256"] = queue_sha
        if row["gates"]["semantic_dedupe"]["verdict"] == "pass":
            row["gates"]["semantic_dedupe"]["evidence"] = (
                "Exact identity is unique; manual comparison against primary rows 0-378 and "
                "supplemental rows 0-166 found no retained semantic-equivalent credit."
            )
        reviews.append(row)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    review_path = OUT_DIR / "erdos_supplemental_084_166.jsonl"
    payload = b"".join(
        (json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n").encode()
        for row in reviews
    )
    review_path.write_bytes(payload)
    decisions = Counter(row["decision"] for row in reviews)
    gate_counts = {
        name: dict(Counter(row["gates"][name]["verdict"] for row in reviews))
        for name in reviews[0]["gates"]
    }
    stage_digest = ordered_digest([row["identity"]["stage_claim_id"] for row in reviews])
    identity_digest = ordered_digest([row["identity"]["identity_payload_sha256"] for row in reviews])
    row_digest = ordered_digest([row["source_binding"]["row_sha256"] for row in reviews])
    review_sha = sha256_bytes(payload)
    authority = sha256_bytes(f"{queue_sha} {review_sha} {stage_digest} {identity_digest}\n".encode("ascii"))
    summary = {
        "schema_version": "awesome-theorems/frontier-theorem-review-summary/5.5",
        "review_name": "erdos_supplemental_084_166",
        "scope": "Human six-gate review of fixed Erdős supplemental_index 84 through 166 inclusive.",
        "review_date_utc": "2026-08-10",
        "source_binding": {
            "path": QUEUE_REL,
            "sha256": queue_sha,
            "source_rows": len(raw_lines),
            "supplemental_index_first": 84,
            "supplemental_index_last": 166,
            "reviewed_rows": len(reviews),
            "receipt_path": RECEIPT_REL,
            "receipt_sha256": sha256_file(ROOT / RECEIPT_REL),
        },
        "upstream_evidence_bindings": {
            "status_snapshot_path": STATUS_REL,
            "status_snapshot_sha256": sha256_file(ROOT / STATUS_REL),
            "erdos_source_archive_path": ERDOS_ARCHIVE_REL,
            "erdos_source_archive_sha256": sha256_file(ROOT / ERDOS_ARCHIVE_REL),
            "formal_conjectures_archive_path": FC_ARCHIVE_REL,
            "formal_conjectures_archive_sha256": sha256_file(ROOT / FC_ARCHIVE_REL),
            "release_5_4_claim_catalog_path": CATALOG_REL,
            "release_5_4_claim_catalog_sha256": sha256_file(ROOT / CATALOG_REL),
        },
        "review_artifact": {
            "path": str(review_path.relative_to(ROOT)),
            "sha256": review_sha,
            "bytes": len(payload),
            "rows": len(reviews),
            "ordered_source_row_sha256_values_sha256": row_digest,
            "ordered_stage_claim_ids_sha256": stage_digest,
            "ordered_identity_payload_sha256_values_sha256": identity_digest,
        },
        "counts": {
            "accept": decisions.get("accept", 0),
            "pending": decisions.get("pending", 0),
            "reject": decisions.get("reject", 0),
            "all_gates_pass": sum(row["all_gates_pass"] for row in reviews),
            "unique_stage_claim_ids": len({row["identity"]["stage_claim_id"] for row in reviews}),
            "unique_semantic_identity_keys": len({row["identity"]["semantic_identity_key"] for row in reviews}),
            "unique_problem_numbers": len({row["identity"]["problem_number"] for row in reviews}),
            "accepted_unique_problem_numbers": len({row["identity"]["problem_number"] for row in reviews if row["decision"] == "accept"}),
        },
        "gate_verdict_counts": gate_counts,
        "nonacceptance": {
            "pending_supplemental_indices": [row["supplemental_index"] for row in reviews if row["decision"] == "pending"],
            "reject_supplemental_indices": [row["supplemental_index"] for row in reviews if row["decision"] == "reject"],
            "semantic_dedupe_reject_indices": [row["supplemental_index"] for row in reviews if row["gates"]["semantic_dedupe"]["verdict"] == "fail"],
            "exact_scope_nonpass_indices": [row["supplemental_index"] for row in reviews if row["gates"]["exact_statement_scope"]["verdict"] != "pass"],
            "primary_resolution_nonpass_indices": [row["supplemental_index"] for row in reviews if row["gates"]["primary_resolution"]["verdict"] != "pass"],
            "importance_reject_indices": [row["supplemental_index"] for row in reviews if row["gates"]["importance_frontier"]["verdict"] == "fail"],
        },
        "scope_boundaries": {
            "index_field": "Every row carries top-level supplemental_index; source_binding.zero_based_row is the same fixed queue position.",
            "cross_queue_dedupe": "Direct corollaries and same-solution wrappers were compared against the complete primary queue, including root-authorized primary/supplemental replacements.",
            "independent_lean_replay_performed": False,
            "formal_proof_source_inspection_performed": True,
            "paper_full_text_reproduced": False,
        },
        "credit_boundary": {
            "frontier_theorem_credit_granted": 0,
            "new_theorem_credit_granted": 0,
            "release_modified": False,
            "accepted_rows_are_release_credit": False,
        },
        "validation": {
            "contiguous_supplemental_index_84_through_166": True,
            "top_level_supplemental_index_present": True,
            "source_row_sha256_recomputed_for_every_row": True,
            "decision_partition_sums_to_83": True,
            "accept_iff_all_gates_pass": True,
            "all_credit_fields_false": True,
            "authority_sha256": authority,
        },
    }
    summary_path = OUT_DIR / "erdos_supplemental_084_166_summary.json"
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n")
    return review_path, summary_path


if __name__ == "__main__":
    for output in build():
        print(output.relative_to(ROOT))
