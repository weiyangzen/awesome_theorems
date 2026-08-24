#!/usr/bin/env python3
"""Build human review rows for supplemental ranks 1--59 (global 255--313)."""

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
LEDGER = OUT / "nonerdos_supplemental_001_059.jsonl"
SUMMARY = OUT / "nonerdos_supplemental_001_059_summary.json"
CHECKER = ROOT / "Docs/catalog/v5/tools/check_frontier_theorem_review_nonerdos_supplemental_001_059_v5_5.py"
FIRST_SUPP = 1
LAST_SUPP = 59
FIRST_GLOBAL = 255
LAST_GLOBAL = 313
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
    255: [spec("doi", "10.1016/J.JALGEBRA.2007.06.017", "The Casas-Alvero conjecture for infinitely many degrees", "2007")],
    256: [spec("doi", "10.1017/S0305004100046867", "Some remarks on the Kakeya problem", "1971")],
    258: [spec("git_commit", "mo271/formal-conjectures@4854c7233c58a7dce45fdd58b1826abf2c9c1a0f", "Formal proof of no complex solution for N=4 and every D>=4", "2026", "https://github.com/mo271/formal-conjectures/blob/4854c7233c58a7dce45fdd58b1826abf2c9c1a0f/FormalConjectures/Paper/MonochromaticQuantumGraph.lean#L549-L557", "4854c7233c58a7dce45fdd58b1826abf2c9c1a0f", "10e3a21cdf22112f6d37c3687e73ebcd4631a975b2337da3888d8b777c5e5dec")],
    259: [spec("git_commit", "mo271/formal-conjectures@2cc6df2e95835d759caedb15e36b70025b2eae2c", "Formal proof of no complex solution for N=8,D=10", "2026", "https://github.com/mo271/formal-conjectures/blob/2cc6df2e95835d759caedb15e36b70025b2eae2c/FormalConjectures/Paper/MonochromaticQuantumGraph.lean#L853-L856", "2cc6df2e95835d759caedb15e36b70025b2eae2c", "39182b119e0f66a275937b1f7a478273e09474df8f771b5782429e55db7a7ec2")],
    260: [spec("doi", "10.1007/BF02787110", "On Bloch's constant", "1996")],
    261: [spec("doi", "10.1080/17476930903197199", "The univalent Bloch constant problem", "2009")],
    262: [spec("doi", "10.1007/BF02788763", "On the locally univalent Bloch constant", "1995")],
    263: [spec("doi", "10.1007/BF02948948", "Uber Steinersche Systeme", "1937")],
    264: [spec("doi", "10.1007/BF02948948", "Uber Steinersche Systeme", "1937")],
    265: [spec("doi", "10.3390/E25050767", "Dimension-Free Bounds for the Union-Closed Sets Conjecture", "2023")],
    266: [spec("journal_article", "MR2264090", "An improved upper bound for the worm problem", "2006", "https://mathscinet.ams.org/mathscinet-getitem?mr=2264090")],
    267: [spec("arxiv", "arXiv:math/0104012", "Perfect numbers and groups", "2001")],
    268: [spec("doi", "10.1103/PHYSREVA.86.052335", "Absolutely maximally entangled states: Existence and applications", "2012")],
    269: [spec("doi", "10.1103/PHYSREVLETT.118.200502", "Absolutely Maximally Entangled States of Seven Qubits Do Not Exist", "2017")],
    272: [spec("doi", "10.1016/S0375-9601(00)00480-0", "How entangled can two couples get?", "2000")],
    273: [spec("primary_scan", "NUMDAM:AST_1979__61__11_0", "Irrationalite de zeta(2) et zeta(3)", "1979", "http://www.numdam.org/item/AST_1979__61__11_0/")],
    274: [spec("doi", "10.1103/PHYSREVLETT.128.080507", "Thirty-six entangled officers of Euler", "2022")],
    275: [spec("doi", "10.1112/MTK.70027", "Mills' constant is irrational", "2025")],
    276: [spec("source_page", "OpenQuantumProblem:35-AME(11,4)", "Absolutely maximally entangled states benchmark", "2026", "https://oqp.iqoqi.oeaw.ac.at/open-quantum-problems/35")],
    284: [spec("doi", "10.4153/CMB-2007-016-8", "A Note on Giuga's Conjecture", "2007")],
    286: [spec("doi", "10.1080/00029890.1996.12004697", "Giuga's Conjecture on Primality", "1996")],
    289: [spec("doi", "10.1007/BF01692494", "Disjointness in ergodic theory, minimal sets, and a problem in Diophantine approximation", "1967")],
    293: [spec("primary_citation", "Giuga-1950", "Su una presumibile proprieta caratteristica dei numeri primi", "1950", "https://eudml.org/doc/194305")],
    299: [spec("doi", "10.1112/PLMS/S2-15.1.192", "On the expression of a number as the sum of two squares", "1916")],
    306: [spec("doi", "10.1016/0097-3165(91)90045-I", "Additive bases of vector spaces over prime fields", "1991")],
    308: [spec("arxiv", "arXiv:1312.7859", "The average size of the 5-Selmer group of elliptic curves is 6, and the average rank is less than 1", "2013")],
    309: [spec("doi", "10.1006/JCTA.2000.3127", "Binary B2-Sequences: A New Upper Bound", "2001")],
}


ELIGIBLE = {
    255: "The primary paper proves Casas-Alvero in every prime-power degree over characteristic zero, exactly the formal specialization.",
    256: "Davies proves the planar Kakeya set conjecture, matching the catalog's dimension-two definition.",
    258: "The immutable cited commit contains a complete proof of the exact N=4, all D>=4 complex equation-system statement; the target theorem body has no sorry or added axiom.",
    259: "The immutable cited commit contains a complete proof of the exact N=8,D=10 complex statement; this parameter pair is not implied by the D=N result at primary rank 80.",
    260: "Chen and Gauthier's primary improvement gives the exact sqrt(3)/4+2*10^-4 lower bound under the source normalization.",
    261: "Skinner's primary paper gives the displayed 0.5708858 lower bound for the univalent Bloch constant.",
    262: "Yanagihara's primary paper gives the displayed 0.5+10^-335 lower bound for Landau's constant.",
    263: "Witt's primary construction establishes existence of the small Witt Steiner system S(5,6,12).",
    264: "Witt's primary construction establishes existence of the large Witt Steiner system S(5,8,24).",
    265: "Yu proves the dimension-free 0.38234 frequency bound for nontrivial union-closed families, matching the rational constant in the row.",
    267: "Leinster gives explicit nonabelian Leinster groups, proving the row's existential noncommutative statement.",
    268: "The primary AME construction supplies an AME(4,3) state with the same subsystem-maximal-mixing definition.",
    269: "Huber-Guhne-Siewert prove nonexistence of an AME(7,2) state, exactly the negative benchmark statement.",
    272: "Higuchi and Sudbery prove that no four-qubit pure state is absolutely maximally entangled.",
    273: "Apery's primary proof establishes irrationality of zeta(3), exactly the existential irrational representation in the row.",
    274: "The primary quantum-design construction proves existence of AME(4,6), resolving the corresponding finite benchmark.",
    275: "Saito proves irrationality of the minimal Mills constant, matching IsMinMills rather than an arbitrary Mills number.",
    284: "Tipu proves the O(sqrt(X) log X) counting bound for Giuga counterexamples represented by strong Giuga numbers.",
    286: "Borwein-Borwein-Borwein-Girgensohn establish the stronger 13000-digit lower bound; this is the canonical row and subsumes ranks 83 and 297.",
    289: "Furstenberg's primary times-two/times-three theorem proves density for every irrational starting point.",
    299: "The Hardy-Landau omega result is exactly the failure of little-o at r^(1/2)(log r)^(1/4).",
    306: "Alon-Linial-Meshulam prove the O(log n) number of cubes sufficient over each fixed prime field.",
    308: "Bhargava-Shankar Theorem 3 proves the height-ordered average-rank upper bound below 0.885.",
    309: "Cohen-Litsyn-Zemor prove the N^0.5753 upper bound for binary Sidon sets represented here.",
}


PENDING = {
    266: "The primary article locator is known, but the exact area equality, convex cover normalization, and orientation-preserving-isometry formulation were not matched to fixed primary text.",
    276: "The claimed AME(11,4) circulant witness is reported by an experimental pipeline, but no fixed proof/certificate artifact was bound and the alternate code remark has a local-dimension ambiguity.",
    293: "The historical Giuga citation is plausible, but the exact strong-Giuga definition and at-least-nine-distinct-prime-factors statement were not verified against a fixed primary scan.",
    295: "Attainment via Blaschke selection is plausible, but no primary theorem was bound to the exact WormCovers topology, convexity, and volume formulation.",
    296: "The source says only that a prover agent showed AME(11,5); no immutable witness or independently replayable proof is supplied.",
    311: "The source attributes the nonnegative-weight nonexistence theorem only to Bogdanov and gives no stable primary paper or proof artifact for all even N>=6,D>=3.",
}


REJECT = {
    257: ("not_frontier_result", "The K2 Sidorenko row reduces definitionally to x<=x and is explicitly a trivial base identity."),
    270: ("duplicate_resolution_family", "Gamma(1/3) is another special-value consequence of the same Chudnovsky transcendence theorem already represented by ranks 124 and 125; it receives no separate resolution credit."),
    271: ("not_frontier_result", "Gamma(1/2)=sqrt(pi), so this is a textbook corollary of the transcendence of pi rather than a separate Chudnovsky frontier result."),
    277: ("source_status_unproved", "The source offers numerical separation evidence for the Z/3 case, not a proof of the formal negative answer."),
    278: ("not_frontier_result", "The subsingleton-tree Sidorenko inequality is the definitional 1<=1 induction base case."),
    279: ("not_frontier_result", "The normal-operator case follows from the classical spectral theorem and is textbook context for the general invariant-subspace problem."),
    280: ("not_frontier_result", "The nonseparable case follows from the elementary separable cyclic-orbit closure argument and does not resolve the separable Hilbert-space problem."),
    281: ("semantic_duplicate", "The integer-coefficient statement is an immediate coefficient-restriction corollary of canonical complex theorem rank 258."),
    282: ("semantic_duplicate", "The trinary-integer statement is an immediate further restriction of canonical complex theorem rank 258."),
    283: ("semantic_duplicate", "The real-coefficient statement is an immediate subfield corollary of canonical complex theorem rank 258."),
    285: ("semantic_duplicate", "The N=10,D=10 row is a direct specialization of primary rank 80's all-even-N,D=N theorem."),
    287: ("semantic_duplicate", "The N=6,D=6 row is a direct specialization of primary rank 80's all-even-N,D=N theorem."),
    288: ("not_frontier_result", "The upper bound one is proved in the source by testing the identity function and is explicitly trivial."),
    290: ("scope_metric_mismatch", "Myers-Steenrod requires the isometries of a Riemannian metric; the formal row assumes only an arbitrary MetricSpace structure with no compatibility with the smooth manifold."),
    291: ("semantic_duplicate", "The degree-three FourProp statement is a direct specialization of the all-degrees theorem already accepted at primary rank 11."),
    292: ("missing_nonempty_hypothesis", "For an empty ground type the universal claim is vacuous, so its negation is false; the formal row omits the nonempty hypothesis needed by the sharpness example."),
    294: ("not_frontier_result", "The source explicitly describes this as the trivial large-k counterexample regime using singleton partition parts."),
    297: ("semantic_duplicate", "The 1700-digit lower bound is strictly superseded by the 13000-digit theorem retained at rank 286."),
    298: ("not_frontier_result", "The two-element-universe union-closed case is a brute-force toy case, not a frontier resolution."),
    300: ("not_frontier_result", "AME(3,2) is witnessed by the elementary GHZ state and is subsumed by the all-d GHZ benchmark at rank 305."),
    301: ("not_frontier_result", "The stated logarithmic regime is explicitly the basic Dirichlet/Bohr-set lower bound used only as context for Green problem 32."),
    302: ("not_frontier_result", "This divisibility equivalence is an elementary reformulation of the weak-Giuga definition."),
    303: ("not_frontier_result", "This reciprocal-sum equivalence is an elementary reformulation of the weak-Giuga definition."),
    304: ("not_frontier_result", "The singleton-member union-closed case is an elementary special case and does not resolve the conjecture."),
    305: ("not_frontier_result", "Existence of AME(3,d) is the standard generalized GHZ construction, not a frontier benchmark resolution."),
    307: ("not_frontier_result", "The two-qubit Bell state is a definitional benchmark example."),
    310: ("not_frontier_result", "Existence of AME(2,d) is the standard generalized Bell-state construction."),
    312: ("not_frontier_result", "The F(3)=7 base value is small finite boundary data, not the frontier extremal construction represented by the stronger F(4)<=19 row."),
    313: ("semantic_duplicate", "This positive-prime-characteristic Promislow-group component belongs to the arbitrary-characteristic Kaplansky counterexample resolution already retained at rank 99."),
}


REJECT_OVERRIDES = {
    270: {"frontier_or_documented_resolution": True, "semantic_dedupe": False},
    277: {"current_proved_status": False},
    281: {"frontier_or_documented_resolution": True, "semantic_dedupe": False},
    282: {"frontier_or_documented_resolution": True, "semantic_dedupe": False},
    283: {"frontier_or_documented_resolution": True, "semantic_dedupe": False},
    285: {"frontier_or_documented_resolution": True, "semantic_dedupe": False},
    287: {"frontier_or_documented_resolution": True, "semantic_dedupe": False},
    290: {"scope_match": False, "current_proved_status": False},
    291: {"frontier_or_documented_resolution": True, "semantic_dedupe": False},
    292: {"complete_proved_statement": False, "scope_match": False, "current_proved_status": False},
    297: {"frontier_or_documented_resolution": True, "semantic_dedupe": False},
    313: {"frontier_or_documented_resolution": True, "semantic_dedupe": False},
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
        if rank == 266:
            values["primary_reference"] = True
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
        "scope": "non-Erdos supplemental candidates, supplemental ranks 1--59 / global ranks 255--313; review eligibility only",
        "rank_range": {"supplemental_first": FIRST_SUPP, "supplemental_last": LAST_SUPP, "candidate_first": FIRST_GLOBAL, "candidate_last": LAST_GLOBAL, "inclusive": True, "expected_rows": 59},
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
            "rank_286_subsumes": [83, 297], "rank_258_subsumes": [281, 282, 283],
            "primary_rank_80_subsumes": [285, 287], "primary_rank_11_subsumes": [291],
            "primary_rank_99_represents_resolution_family_of": [313],
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
