#!/usr/bin/env python3
"""Build human review rows for supplemental ranks 60--117 (global 314--371)."""

from __future__ import annotations

import hashlib
import json
import tarfile
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
QUEUE = ROOT / "Docs/catalog/v5/curation/Frontier_Theorem_Supplemental_Candidate_Queue_v5_5.json"
PRIMARY = ROOT / "Docs/catalog/v5/curation/Frontier_Theorem_Candidate_Queue_v5_5.json"
RELEASE = ROOT / "Docs/catalog/v5/releases/5.4/Claim_Catalog.json"
SOURCE = ROOT / "Docs/catalog/v5/sources/formal-conjectures-2270d31e8dd611521f979de6d86da364930b7669.tar.gz"
OUT = ROOT / "Docs/catalog/v5/curation/frontier_theorem_reviews_v5_5"
LEDGER = OUT / "nonerdos_supplemental_060_117.jsonl"
SUMMARY = OUT / "nonerdos_supplemental_060_117_summary.json"
CHECKER = ROOT / "Docs/catalog/v5/tools/check_frontier_theorem_review_nonerdos_supplemental_060_117_v5_5.py"
FIRST_SUPP = 60
LAST_SUPP = 117
FIRST_GLOBAL = 314
LAST_GLOBAL = 371
AS_OF = "2026-08-10"

QUEUE_SHA = "78c2d8e1e4068d59bf0471ecca9071fc139bb3300525df0aab8348718cbdc135"
QUEUE_AUTHORITY = "d382e4c9b6851150257fea50ab597051b6258085a24b04d43e517a81094c547c"
PRIMARY_SHA = "b3b28b81cfcd9fe4dbf002d2bb8d9bedaa8094656396e224abb5c6221530b2fc"
RELEASE_SHA = "384c1e34a57443dafe2e2ce70e36d6a6e23c6d03e006171b94aa2defa92e9709"
SOURCE_SHA = "51535f4755574d97672515a75b8b076065aba2c0d79631e99fa57719f484dcc8"
LICENSE_SHA = "cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30"


def cb(value: object) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def file_sha(path: Path) -> str:
    return sha(path.read_bytes())


def spec(kind: str, identifier: str, title: str, year: str, url: str | None = None,
         version: str | None = None, artifact_sha256: str | None = None) -> tuple:
    return kind, identifier, title, year, url, version, artifact_sha256


def make_ref(value: tuple, note: str) -> dict:
    kind, identifier, title, year, url, version, artifact_sha256 = value
    if url is None:
        if kind == "doi":
            url = "https://doi.org/" + identifier
        elif kind == "arxiv":
            url = "https://arxiv.org/abs/" + identifier.removeprefix("arXiv:")
        else:
            raise AssertionError((kind, identifier))
    return {
        "kind": kind, "identifier": identifier, "url": url, "title": title,
        "version": version, "published_at": year, "updated_at": None,
        "artifact_path": None, "artifact_sha256": artifact_sha256,
        "verification": note,
    }


REFS = {
    314: [spec("arxiv", "arXiv:2312.05240", "Counterexamples to the Kaplansky unit conjecture", "2023")],
    315: [spec("git_commit", "mo271/formal-conjectures@4854c7233c58a7dce45fdd58b1826abf2c9c1a0f", "Formal proof of no complex solution for N=4 and every D>=4", "2026", "https://github.com/mo271/formal-conjectures/blob/4854c7233c58a7dce45fdd58b1826abf2c9c1a0f/FormalConjectures/Paper/MonochromaticQuantumGraph.lean#L549-L557", "4854c7233c58a7dce45fdd58b1826abf2c9c1a0f", "10e3a21cdf22112f6d37c3687e73ebcd4631a975b2337da3888d8b777c5e5dec")],
    316: [spec("course_notes", "Green-RKP-Theorem-20", "Restriction and Kakeya Phenomena", "2013", "https://people.maths.ox.ac.uk/greenbj/papers/rkp.pdf")],
    317: [spec("doi", "10.1016/0012-365X(91)90269-8", "Degree sequences in triangle-free graphs", "1991")],
    318: [spec("doi", "10.1007/S10474-024-01499-8", "On the diameter of finite Sidon sets", "2025")],
    319: [spec("course_notes", "Green-RKP-Example-3", "Restriction and Kakeya Phenomena", "2013", "https://people.maths.ox.ac.uk/greenbj/papers/rkp.pdf")],
    320: [spec("doi", "10.1142/S0219498815400071", "The Zariski cancellation problem and related problems in affine algebraic geometry", "2015")],
    321: [spec("arxiv", "arXiv:2605.12342", "Conjecture 1 and its stated boundary exclusions", "2026")],
    322: [spec("arxiv", "arXiv:2605.12342", "Conjecture 1 and its stated boundary exclusions", "2026")],
    323: [spec("doi", "10.1307/MMJ/1339011525", "At least one of the Euler--Mascheroni and Gompertz constants is irrational", "2012")],
    324: [spec("doi", "10.1016/J.JMAA.2010.07.030", "Improved bounds on the supremum of autoconvolutions", "2010")],
    325: [spec("doi", "10.1007/BF01457099", "Noether's problem for metacyclic groups", "1987")],
    326: [spec("doi", "10.1007/BF01457099", "Noether's problem for metacyclic groups", "1987")],
    327: [spec("doi", "10.1112/S0025579300013061", "Inscribed squares and square-like quadrilaterals in closed curves", "1989")],
    328: [spec("doi", "10.1007/BF01457099", "Noether's problem for metacyclic groups", "1987")],
    329: [spec("doi", "10.1137/20M1335030", "A large gap in a dilate of a set", "2020")],
    330: [spec("doi", "10.1017/S0963548320000371", "The length of an s-increasing sequence of r-tuples", "2021")],
    331: [spec("doi", "10.4064/AA-27-1-199-245", "On sets of integers containing no k elements in arithmetic progression", "1975")],
    332: [spec("doi", "10.1112/BLMS.12253", "Sums of dilates", "2019")],
    333: [spec("doi", "10.1090/PSPUM/008/0174539", "Extremal problems in number theory", "1965")],
    334: [spec("doi", "10.1016/0022-314X(76)90019-6", "Differences of residues (mod p)", "1976")],
    335: [spec("doi", "10.1112/PLMS/S3-23.4.629", "On a combinatorial problem in number theory", "1971")],
    337: [spec("arxiv", "arXiv:2511.09365v2", "A quantitative Green--Sawhney bound", "2025")],
    339: [spec("doi", "10.1007/S00493-023-00069-W", "On unique sums in Abelian groups", "2024")],
    341: [spec("doi", "10.1007/BF02570490", "A congruence of Giuga and Bernoulli numbers", "1990")],
    342: [spec("doi", "10.1090/S0894-0347-00-00345-3", "Entire solutions of semilinear elliptic equations with global minimization properties", "2000")],
    343: [spec("doi", "10.1007/S002080050196", "On a conjecture of De Giorgi and some related problems", "1998")],
    346: [spec("doi", "10.1090/MCOM/3348", "Elliptic curves of high rank and the Riemann zeta function", "2020")],
    348: [spec("primary_scan", "Hilbert-1892", "Ueber die Irreducibilitaet ganzer rationaler Functionen mit ganzzahligen Coefficienten", "1892", "https://eudml.org/doc/157573")],
    349: [spec("doi", "10.1017/S0963548320000371", "The length of an s-increasing sequence of r-tuples", "2021")],
    351: [spec("doi", "10.1070/IM1954V018N03ABEH000799", "Construction of fields of algebraic numbers with given solvable Galois group", "1954")],
    354: [spec("doi", "10.4007/ANNALS.2017.185.3.7", "The sphere packing problem in dimension 8", "2017")],
}

AKS14 = spec("doi", "10.1016/J.DAM.2014.05.007", "On the van der Waerden numbers w(2;3,t)", "2014")
VDW_PRIMARY = {
    "chvatal": spec("primary_citation", "CiNii:1571698599268861952", "Some unknown van der Waerden numbers", "1970", "https://cir.nii.ac.jp/crid/1571698599268861952?lang=en"),
    "beeler_oneil": spec("doi", "10.1016/0012-365X(79)90090-6", "Some new van der Waerden numbers", "1979"),
    "landman_robertson_culver": spec("journal_article", "MR2192088", "Some new exact van der Waerden numbers", "2005", "https://mathscinet.ams.org/mathscinet-getitem?mr=2192088"),
    "kouril": spec("doctoral_thesis", "Kouril-2006", "Van der Waerden numbers", "2006", "https://www.proquest.com/docview/305274255"),
    "ahmed": spec("doi", "10.1515/INTEG.2010.032", "Some new van der Waerden numbers and some van der Waerden-type numbers", "2010"),
    "aks": AKS14,
}
VDW_GROUP_BY_R = {
    3: "chvatal", 4: "chvatal", 5: "chvatal", 6: "chvatal", 7: "chvatal",
    8: "beeler_oneil", 9: "beeler_oneil", 10: "beeler_oneil",
    11: "landman_robertson_culver", 12: "landman_robertson_culver", 13: "landman_robertson_culver",
    14: "kouril", 15: "kouril", 16: "kouril", 17: "ahmed", 18: "ahmed", 19: "aks",
}
VDW_R_BY_RANK = {355: 11, 356: 12, 357: 13, 358: 14, 359: 15, 360: 16,
                 361: 17, 362: 18, 363: 19, 364: 10, 365: 4, 366: 5,
                 367: 6, 368: 7, 369: 8, 370: 9, 371: 3}
for review_rank, parameter_r in VDW_R_BY_RANK.items():
    primary = VDW_PRIMARY[VDW_GROUP_BY_R[parameter_r]]
    REFS[review_rank] = [primary] if primary == AKS14 else [primary, AKS14]


ELIGIBLE = {
    316: "Green's fixed course notes, Theorem 20, prove the stated asymptotic upper obstruction for cosets in A+A.",
    318: "Carter--Hunter--O'Bryant prove the displayed 0.98183 Sidon-set upper coefficient with an additive constant.",
    319: "Green's fixed course notes, Example 3, establish the positive-density linear lower guarantee for a coset in A+A.",
    320: "The dimension-two Zariski cancellation theorem holds over arbitrary fields, matching the two-variable formal statement.",
    324: "Matolcsi--Vinuesa prove the 0.7505 upper bound for the normalized supremum of an autoconvolution.",
    327: "Stromquist proves the square-peg conclusion for C2 Jordan curves under the matching regularity assumptions.",
    329: "Shakan's Theorem 1 gives the exact floor(2p/|A|-2) gap after dilation for every prime modulus.",
    330: "Gowers--Long Proposition 1.4 supplies the perfect-square n^(3/2) construction represented by the row.",
    331: "Szemeredi's theorem proves the fixed-positive-density regime encoded by HasLargeGapDilate.",
    333: "Erdos's 1965 paper proves the displayed square-root upper bound for the sum-avoiding subset parameter.",
    334: "Straus proves the historical logarithmic lower bound for the unique-sum parameter along primes.",
    335: "Choi proves the displayed stronger upper bound for the Erdos--Moser sum-free subset parameter.",
    337: "Green--Sawhney Theorem 1.1 supplies the quantitative permissible bound encoded by N0.",
    339: "Bedert Theorem 5 proves the O((log p)^2) upper bound for the unique-sum parameter.",
    341: "Agoh's theorem proves the congruence/sum equivalence with the formal prime/composite quantifiers.",
    342: "Ambrosio--Cabre prove the De Giorgi conclusion in dimension three for the encoded bounded monotone solutions.",
    343: "Ghoussoub--Gui prove the corresponding De Giorgi conclusion in dimension two.",
    346: "Elkies supplies the explicit rational elliptic curve together with a proof that its Mordell--Weil rank is at least 28.",
    348: "Hilbert irreducibility yields realizations of every finite symmetric group over the rationals.",
    349: "Gowers--Long prove the stated n^2/exp(Omega(log-star n)) upper regime for s-increasing triples.",
    351: "Shafarevich's solvable inverse-Galois theorem in particular realizes every finite abelian group over the rationals.",
    354: "Viazovska constructs the sharp Cohn--Elkies auxiliary function in dimension eight.",
}
ELIGIBLE.update({
    rank: f"The cited primary computation proves the exact off-diagonal van der Waerden value W(3,{r}); AKS14 Table 1 independently fixes the same value and normalization."
    for rank, r in VDW_R_BY_RANK.items()
})


PENDING = {
    336: "The length-190 dimension-nine snake is reported as a best construction, but no fixed primary construction or replayable certificate was bound.",
    338: "The 2024 Elkies--Klagsbrun rank-29 curve is reported publicly, but this review did not bind a fixed unconditional rank certificate for the exact coefficients.",
    347: "The f_tilde(2)=1 claim is attributed to Struik's 1994 thesis, but no fixed primary thesis text was bound to the exact formal normalization.",
    350: "The finite equational countermodel is plausible, but no immutable project certificate or independently replayable model was bound.",
    353: "The covering-code counting bound is standard, but no fixed primary theorem was matched to the exact liminf and ENNReal formulation.",
}


REJECT = {
    314: ("semantic_duplicate", "This complex-characteristic component is subsumed by primary rank 99's arbitrary-characteristic Kaplansky counterexample resolution."),
    315: ("semantic_duplicate", "The nnreal N=4,D>=4 statement is a coefficient restriction of the complex theorem already accepted at rank 258."),
    317: ("semantic_duplicate", "The cited theorem holds for every triangle-free graph; adding connectedness produces only a narrower corollary of the same resolution."),
    321: ("source_scope_excluded", "The Fernandes conjecture explicitly excludes the rank-(4,3) boundary case, so it is not a proved resolution of that conjecture."),
    322: ("source_scope_excluded", "The Fernandes conjecture explicitly excludes the rank-(4,4) boundary case, so it is not a proved resolution of that conjecture."),
    323: ("statement_constant_mismatch", "The primary result concerns the Euler--Mascheroni and Gompertz constants; the formal row substitutes Catalan's constant."),
    325: ("scope_metric_mismatch", "The low-dimensional Noether result concerns a specified permutation action, while the formal row quantifies arbitrary automorphism subgroups and does not use G."),
    326: ("scope_metric_mismatch", "The low-dimensional Noether result concerns a specified permutation action, while the formal row quantifies arbitrary automorphism subgroups and does not use G."),
    328: ("scope_metric_mismatch", "The low-dimensional Noether result concerns a specified permutation action, while the formal row quantifies arbitrary automorphism subgroups and does not use G."),
    332: ("not_frontier_result", "The n^2 bound is the immediate pigeonhole upper bound obtained by projecting A x A, not an independent frontier resolution."),
    340: ("semantic_duplicate", "Existence of a least Mills number is the standard well-ordering component of the Mills theorem already represented at rank 126."),
    344: ("not_frontier_result", "The inequality f_tilde<=f follows directly from the two definitions by restricting the admissible subset family."),
    345: ("not_frontier_result", "Strong Giuga implies Carmichael is a direct projection of the source's isStrongGiuga_iff characterization."),
    352: ("semantic_duplicate", "The cyclic inverse-Galois row is strictly contained in the finite-abelian theorem retained at rank 351."),
}


REJECT_OVERRIDES = {
    314: {"frontier_or_documented_resolution": True, "semantic_dedupe": False},
    315: {"frontier_or_documented_resolution": True, "semantic_dedupe": False},
    317: {"frontier_or_documented_resolution": True, "semantic_dedupe": False},
    321: {"scope_match": False, "current_proved_status": False},
    322: {"scope_match": False, "current_proved_status": False},
    323: {"scope_match": False, "current_proved_status": False},
    325: {"scope_match": False, "current_proved_status": False},
    326: {"scope_match": False, "current_proved_status": False},
    328: {"scope_match": False, "current_proved_status": False},
    340: {"frontier_or_documented_resolution": True, "semantic_dedupe": False},
    352: {"frontier_or_documented_resolution": True, "semantic_dedupe": False},
}



def decision(rank: int) -> tuple[str, list[str], str]:
    if rank in ELIGIBLE:
        return "eligible_existing_frontier_credit", ["all_review_gates_pass", "review_eligibility_only_no_formal_credit"], ELIGIBLE[rank]
    if rank in PENDING:
        return "pending", ["independent_primary_or_scope_verification_pending"], PENDING[rank]
    code, note = REJECT[rank]
    return "reject", [code], note


def gate(value: bool, *evidence: str) -> dict:
    return {"pass": value, "evidence": list(evidence)}


def gates(candidate: dict, result: str, refs: list[dict], note: str, uniqueness: str) -> dict:
    rank = candidate["candidate_rank"]
    if result == "eligible_existing_frontier_credit":
        values = {name: True for name in ("complete_proved_statement", "primary_reference", "scope_match", "current_proved_status", "frontier_or_documented_resolution", "rights", "semantic_dedupe")}
    elif result == "pending":
        values = {"complete_proved_statement": True, "primary_reference": False, "scope_match": False, "current_proved_status": False, "frontier_or_documented_resolution": False, "rights": True, "semantic_dedupe": True}
    else:
        values = {"complete_proved_statement": True, "primary_reference": bool(refs), "scope_match": True, "current_proved_status": True, "frontier_or_documented_resolution": False, "rights": True, "semantic_dedupe": True}
        values.update(REJECT_OVERRIDES.get(rank, {}))
    ref_evidence = [f"{item['identifier']}: {item['verification']}" for item in refs] or ["No exact independently verified primary resolution locator passed this review."]
    return {
        "complete_proved_statement": gate(values["complete_proved_statement"], f"Inspected frozen source block {candidate['source_member_path']}:{candidate['source_locator']['line_start']}-{candidate['source_locator']['line_end']} and formal_type_sha256={candidate['formal_type_sha256']}.", note),
        "primary_reference": gate(values["primary_reference"], *ref_evidence),
        "scope_match": gate(values["scope_match"], "Definitions, hypotheses, quantifiers, constants, and conclusion match the bound evidence." if values["scope_match"] else "Exact formal scope was not matched to the cited result.", note),
        "current_proved_status": gate(values["current_proved_status"], f"Exact proved status was independently supported as of {AS_OF}." if values["current_proved_status"] else f"Exact proved status was not independently established as of {AS_OF}."),
        "frontier_or_documented_resolution": gate(values["frontier_or_documented_resolution"], note, "The source category was treated only as discovery evidence."),
        "rights": gate(True, f"Pinned source archive sha256={SOURCE_SHA}; LICENSE sha256={LICENSE_SHA}; the source file carries its Apache-2.0 header.", "Metadata-only review preserves attribution and locators, copies no paper prose, and grants no release or new-theorem credit."),
        "semantic_dedupe": gate(values["semantic_dedupe"], uniqueness, note),
    }


def main() -> None:
    assert file_sha(QUEUE) == QUEUE_SHA and file_sha(PRIMARY) == PRIMARY_SHA
    assert file_sha(RELEASE) == RELEASE_SHA and file_sha(SOURCE) == SOURCE_SHA
    queue = json.loads(QUEUE.read_text(encoding="utf-8"))
    release = json.loads(RELEASE.read_text(encoding="utf-8"))
    assert queue["authority_sha256"] == QUEUE_AUTHORITY
    selected = [row for row in queue["records"] if FIRST_SUPP <= row["supplemental_rank"] <= LAST_SUPP]
    assert [row["supplemental_rank"] for row in selected] == list(range(FIRST_SUPP, LAST_SUPP + 1))
    assert [row["candidate_rank"] for row in selected] == list(range(FIRST_GLOBAL, LAST_GLOBAL + 1))
    expected = set(range(FIRST_GLOBAL, LAST_GLOBAL + 1))
    assert set(ELIGIBLE) | set(PENDING) | set(REJECT) == expected
    assert not (set(ELIGIBLE) & set(PENDING) or set(ELIGIBLE) & set(REJECT) or set(PENDING) & set(REJECT))
    assert set(ELIGIBLE) <= set(REFS)
    parent_by_stage = {row["stage_claim_id"]: row for row in release["records"]}
    archive_prefix = "formal-conjectures-2270d31e8dd611521f979de6d86da364930b7669/"
    with tarfile.open(SOURCE, "r:gz") as tf:
        assert sha(tf.extractfile(archive_prefix + "LICENSE").read()) == LICENSE_SHA
        for candidate in selected:
            data = tf.extractfile(archive_prefix + candidate["source_member_path"]).read()
            assert sha(data) == candidate["source_locator"]["file_sha256"]
            assert b"Licensed under the Apache License, Version 2.0" in data[:800]

    rows = []
    for candidate in selected:
        assert sha(cb({key: value for key, value in candidate.items() if key != "row_sha256"})) == candidate["row_sha256"]
        parent = parent_by_stage[candidate["stage_claim_id"]]
        assert parent["formal_type_sha256"] == candidate["formal_type_sha256"]
        assert parent["dedupe"]["normalized_statement_sha256"] == candidate["semantic_key"].split("/", 1)[1]
        result, reasons, note = decision(candidate["candidate_rank"])
        references = [make_ref(value, note) for value in REFS.get(candidate["candidate_rank"], [])]
        uniqueness = (
            f"Supplemental queue exact-cross-primary flags are semantic=false and formal=false; release 5.4 identity is {candidate['stage_claim_id']}; manual logical-subsumption review against primary ranks 1--254 and supplemental ranks 255--371 was applied."
        )
        review_gates = gates(candidate, result, references, note, uniqueness)
        all_pass = all(value["pass"] for value in review_gates.values())
        assert all_pass == (result == "eligible_existing_frontier_credit")
        review_key = None
        if all_pass:
            payload = [sorted(ref["identifier"] for ref in references), candidate["formal_type_sha256"], candidate["semantic_key"]]
            review_key = "frontier-resolution-sha256/" + sha(cb(payload))
        row = {
            "schema_version": "awesome-theorems/frontier-theorem-human-review/5.5",
            "reviewed_as_of": AS_OF,
            "candidate_rank": candidate["candidate_rank"],
            "supplemental_rank": candidate["supplemental_rank"],
            "stage_claim_id": candidate["stage_claim_id"],
            "variant_id": candidate["variant_id"],
            "family_id": candidate["family_id"],
            "display_name": candidate["display_name"],
            "queue_row_sha256": candidate["row_sha256"],
            "semantic_key": candidate["semantic_key"],
            "decision": result,
            "gates": review_gates,
            "primary_references": references,
            "frontier_credit_key": review_key,
            "reason_codes": reasons,
            "reviewer_notes": note,
            "review_eligible_frontier_credit": all_pass,
            "grants_frontier_credit": False,
            "grants_new_theorem_credit": False,
        }
        row["row_sha256"] = sha(cb(row))
        rows.append(row)

    OUT.mkdir(parents=True, exist_ok=True)
    ledger_data = b"".join(cb(row) + b"\n" for row in rows)
    LEDGER.write_bytes(ledger_data)
    decisions = Counter(row["decision"] for row in rows)
    keys = [row["frontier_credit_key"] for row in rows if row["frontier_credit_key"]]
    assert len(keys) == len(set(keys))
    builder = Path(__file__).resolve()
    summary = {
        "schema_version": "awesome-theorems/frontier-theorem-human-review-summary/5.5",
        "reviewed_as_of": AS_OF,
        "scope": "non-Erdos supplemental candidates, supplemental ranks 60--117 / global ranks 314--371; review eligibility only",
        "rank_range": {"supplemental_first": FIRST_SUPP, "supplemental_last": LAST_SUPP, "candidate_first": FIRST_GLOBAL, "candidate_last": LAST_GLOBAL, "inclusive": True, "expected_rows": 58},
        "inputs": {
            "supplemental_queue_path": QUEUE.relative_to(ROOT).as_posix(),
            "supplemental_queue_sha256": QUEUE_SHA,
            "supplemental_queue_authority_sha256": QUEUE_AUTHORITY,
            "primary_queue_path": PRIMARY.relative_to(ROOT).as_posix(),
            "primary_queue_sha256": PRIMARY_SHA,
            "release_5_4_claim_catalog_path": RELEASE.relative_to(ROOT).as_posix(),
            "release_5_4_claim_catalog_sha256": RELEASE_SHA,
            "source_archive_path": SOURCE.relative_to(ROOT).as_posix(),
            "source_archive_sha256": SOURCE_SHA,
            "source_license_sha256": LICENSE_SHA,
        },
        "output": {"ledger_path": LEDGER.relative_to(ROOT).as_posix(), "ledger_sha256": sha(ledger_data), "ledger_bytes": len(ledger_data), "ledger_rows": len(rows)},
        "counts": {
            "eligible_existing_frontier_credit": decisions["eligible_existing_frontier_credit"],
            "pending": decisions["pending"], "reject": decisions["reject"], "review_rows": len(rows),
            "review_eligible_frontier_keys": len(keys), "formal_release_frontier_credits_granted": 0,
            "new_theorem_credits_granted": 0,
        },
        "set_digests": {
            "ordered_queue_row_sha256_chain": sha(cb([row["queue_row_sha256"] for row in rows])),
            "ordered_review_row_sha256_chain": sha(cb([row["row_sha256"] for row in rows])),
            "semantic_key_set_sha256": sha(cb(sorted({row["semantic_key"] for row in rows}))),
            "frontier_credit_key_set_sha256": sha(cb(sorted(keys))),
            "eligible_candidate_rank_set_sha256": sha(cb(sorted(row["candidate_rank"] for row in rows if row["decision"] == "eligible_existing_frontier_credit"))),
            "pending_candidate_rank_set_sha256": sha(cb(sorted(row["candidate_rank"] for row in rows if row["decision"] == "pending"))),
            "reject_candidate_rank_set_sha256": sha(cb(sorted(row["candidate_rank"] for row in rows if row["decision"] == "reject"))),
        },
        "cross_batch_dedupe": {
            "primary_rank_99_represents_resolution_family_of": [314],
            "rank_258_subsumes": [315],
            "rank_351_subsumes": [352],
            "rank_126_represents_mills_resolution_family_of": [340],
        },
        "invariants": {
            "all_seven_gates_required_for_review_eligibility": True,
            "manual_cross_batch_logical_subsumption_applied": True,
            "metadata_only_rights_review": True, "formal_release_modified": False,
            "review_alone_grants_release_credit": False, "all_rows_grant_frontier_credit_false": True,
            "all_rows_grant_new_theorem_credit_false": True,
        },
        "validation": {
            "builder_path": builder.relative_to(ROOT).as_posix(), "builder_sha256": file_sha(builder),
            "checker_path": CHECKER.relative_to(ROOT).as_posix(), "checker_sha256": file_sha(CHECKER),
            "status": "checker_bound; independent read-only checker required and run after generation",
        },
    }
    summary["authority_sha256"] = sha(cb(summary))
    SUMMARY.write_bytes(json.dumps(summary, ensure_ascii=False, sort_keys=True, indent=2).encode("utf-8") + b"\n")
    print(json.dumps({"rows": len(rows), "counts": summary["counts"], "ledger_sha256": summary["output"]["ledger_sha256"], "authority_sha256": summary["authority_sha256"]}, sort_keys=True))


if __name__ == "__main__":
    main()
