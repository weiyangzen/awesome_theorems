#!/usr/bin/env python3
"""Build the manually researched Erdős frontier-review slices owned by this worker.

The source queue is immutable.  This builder only projects explicit row decisions and
fixed citation/proof locators into the common review schema; it grants no release credit.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[4]
QUEUE_REL = "Docs/catalog/v5/curation/erdos_parent_join_v5_5/resolved-theorem-max2-selected.jsonl"
QUEUE = ROOT / QUEUE_REL
OUT_DIR = ROOT / "Docs/catalog/v5/curation/frontier_theorem_reviews_v5_5"

STATUS_REL = "Docs/catalog/v5/sources/erdosproblems-status-af90db96.json"
ERDOS_ARCHIVE_REL = "Docs/catalog/v5/sources/erdosproblems-af90db96-source.tar.gz"
FC_ARCHIVE_REL = (
    "Docs/catalog/v5/sources/"
    "formal-conjectures-2270d31e8dd611521f979de6d86da364930b7669.tar.gz"
)
CATALOG_REL = "Docs/catalog/v5/releases/5.4/Claim_Catalog.json"


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def ordered_digest(values: list[str]) -> str:
    return sha256_bytes(("\n".join(values) + "\n").encode("utf-8"))


def spec(
    citation: str,
    *,
    exact: str = "pass",
    primary: str = "pass",
    importance: str = "pass",
    dedupe: str = "pass",
    exact_evidence: str | None = None,
    primary_evidence: str | None = None,
    importance_evidence: str | None = None,
    dedupe_evidence: str | None = None,
    duplicate_rows: list[int] | None = None,
) -> dict[str, Any]:
    return {
        "citation": citation,
        "exact": exact,
        "primary": primary,
        "importance": importance,
        "dedupe": dedupe,
        "exact_evidence": exact_evidence,
        "primary_evidence": primary_evidence,
        "importance_evidence": importance_evidence,
        "dedupe_evidence": dedupe_evidence,
        "duplicate_rows": duplicate_rows or [],
    }


SLICES: dict[str, dict[str, Any]] = {
    "285_320": {
        "first": 285,
        "last": 320,
        "rows": {
            285: spec(
                "Shashi456/erdos-formalizations@286f856aa3fc08957b80950fd18a45aab8d045ea, "
                "Erdos/P694/proof.pdf sha256=7286f5e49795df1d3760fa05a09a2cf52f9dee781753b0cae74d2a3c319eecea; "
                "Erdos/P694/Proof.lean sha256=b3f1f29947e8de0afad25794e961e8346a3aff6feddaf1aca4ea5563d7597a53",
                primary_evidence=(
                    "The fixed mathematical proof and exact asymptotic wrapper were inspected. "
                    "The Lean reduction has no sorry, while its Mertens-product and Linnik inputs "
                    "are explicitly declared axioms rather than concealed kernel proofs."
                ),
            ),
            286: spec("Er79e, MR 556666"),
            287: spec(
                "Ha92, MR 1189509",
                exact="fail",
                exact_evidence=(
                    "The pinned prose says alpha < 1/log 2, but the selected formal theorem assumes "
                    "1/log 2 < alpha.  The threshold inequality is reversed, so this row cannot bind "
                    "the cited part of Hall's theorem."
                ),
            ),
            288: spec(
                "Ha92, MR 1189509",
                importance="fail",
                importance_evidence=(
                    "This is the routine density-existence support lemma for a finite union of "
                    "divisibility progressions, not the nontrivial threshold theorem resolving the problem."
                ),
            ),
            289: spec("ErSz78, MR 519358"),
            290: spec(
                "ErSz78, MR 519358",
                importance="fail",
                importance_evidence=(
                    "The i=1, j=p, n=2p equality check is an elementary sharpness example, not a "
                    "separately creditable frontier theorem."
                ),
            ),
            291: spec(
                "OD99, P. O'Donnell, High girth unit-distance graphs, Rutgers PhD dissertation (1999)",
                primary="pending",
                primary_evidence=(
                    "The live bibliography identifies the dissertation, but no fixed repository copy, "
                    "stable scholarly identifier, or independently pinned exact theorem text was located."
                ),
            ),
            292: spec(
                "AlMi25, arXiv:2510.19804; Ha47, MR 23536; "
                "plby/lean-proofs@68da20b96673899166e94638f5a7fffeb7231d35, "
                "src/v4.24.0/ErdosProblems/Erdos707.lean sha256=98f2eff5714406a90bf5d45010285a8c685f66d63ad41dcc2f01d5442d05405f",
                dedupe="fail",
                dedupe_evidence=(
                    "The universal base negation receives no second credit: retained row 293 supplies "
                    "the explicit Sidon-set counterexample from the same disproof event."
                ),
                duplicate_rows=[293],
            ),
            293: spec(
                "AlMi25, arXiv:2510.19804; Ha47, MR 23536; "
                "plby/lean-proofs@68da20b96673899166e94638f5a7fffeb7231d35, "
                "src/v4.24.0/ErdosProblems/Erdos707.lean sha256=98f2eff5714406a90bf5d45010285a8c685f66d63ad41dcc2f01d5442d05405f"
            ),
            294: spec(
                "Bo77, MR 441786; Jayyhk/erdos-lean@110d489ed5c07e5b216453e092e9113127c98c9a, "
                "problems/71/Erdos71.lean"
            ),
            295: spec(
                "plby/lean-proofs@68da20b96673899166e94638f5a7fffeb7231d35, "
                "src/v4.24.0/ErdosProblems/Erdos728p.lean "
                "sha256=59c034e18f9721e462e0da12017ce1038d5c662ff69eeb47262964b3a64ce296",
                primary_evidence=(
                    "The fixed proof develops the density-one factorial-divisibility result from which "
                    "the displayed C<C' existence statement follows; executable declarations were checked "
                    "and the only literal 'sorry' occurrence is explanatory text inside a comment."
                ),
            ),
            296: spec(
                "plby/lean-proofs@68da20b96673899166e94638f5a7fffeb7231d35, "
                "src/v4.29.1/ErdosProblems/Erdos729.lean "
                "sha256=7d1190c34d37fe0f2e0548a615bc6b13973a3464ff7516be49533bea9d2fd1a5"
            ),
            297: spec(
                "google-deepmind/formal-conjectures@9d492049e42167b0d2fd58a9e91da3bf160172b5, "
                "FormalConjectures/ErdosProblems/741.lean lines 228-238, "
                "file sha256=b330a0789b379fc6a2aa8e6f548f83aee85a0dc405bb0300d2a8084775e60c4f"
            ),
            298: spec(
                "mo271/formal-conjectures@486bc8afae062b6711cd16d3466d651ee2880a52, "
                "FormalConjectures/ErdosProblems/741.lean lines 1449-1462, "
                "file sha256=e5c9beacb4bf765bdf1d10210d370771382ff6ca0a46773f78c057c970807ebe"
            ),
            299: spec(
                "Ulam Erdős 750 proof PDF sha256=adad62e08d6e8191743cf59ecc3730cf7c8ff5b06288cd426a63dee82c6b082a; "
                "Shashi456/erdos-formalizations@286f856aa3fc08957b80950fd18a45aab8d045ea, "
                "Erdos/P750/Proof.lean sha256=83ff0b5922db99276e9bcb2198613a6ff617edd4ae54fbeb185c6d7d8862c3e8",
                primary_evidence=(
                    "The fixed paper states the arbitrary f(m)->infinity theorem. The exact FC wrapper "
                    "was inspected; its Lean derivation explicitly assumes the Stiebitz lower-bound theorem."
                ),
            ),
            300: spec(
                "EHS82, MR 806975, DOI 10.1016/S0304-0208(08)73497-2",
                primary="pending",
                primary_evidence=(
                    "Stable bibliographic metadata was fixed, but the unavailable primary text was not "
                    "independently checked for the exact every-epsilon quantifier and m/2-epsilon*m scope."
                ),
            ),
            301: spec(
                "BoVi98, MR 1487781",
                dedupe="fail",
                dedupe_evidence=(
                    "This negative answer is only the chromatic-number corollary of the Bondy-Vince "
                    "minimum-degree theorem retained at row 302."
                ),
                duplicate_rows=[302],
            ),
            302: spec("BoVi98, MR 1487781"),
            303: spec(
                "Al92, MR 1179241",
                dedupe="fail",
                dedupe_evidence=(
                    "The rejected universal lower-bound question is a direct consequence of the stronger "
                    "Alon construction retained at row 304."
                ),
                duplicate_rows=[304],
            ),
            304: spec(
                "Al92, MR 1179241; plby/lean-proofs@68da20b96673899166e94638f5a7fffeb7231d35, "
                "src/v4.29.1/ErdosProblems/Erdos753.lean "
                "sha256=c5186d29a7e4e8f7720e5ffb91a8648bcf4fd897ae764c7a0266c3caff59729a"
            ),
            305: spec(
                "CDL25b, arXiv:2507.19841",
                dedupe="fail",
                dedupe_evidence=(
                    "The unit-side upper bound is the immediate subset corollary of the exact any-side "
                    "asymptotic retained at row 306."
                ),
                duplicate_rows=[306],
            ),
            306: spec("CDL25b, arXiv:2507.19841"),
            307: spec(
                "Bh24, arXiv:2407.01174",
                dedupe="fail",
                dedupe_evidence=(
                    "The asymptotic yes-answer is the direct corollary of Bhowmick's explicit construction "
                    "retained at row 308."
                ),
                duplicate_rows=[308],
            ),
            308: spec(
                "Bh24, arXiv:2407.01174; plby/lean-proofs@68da20b96673899166e94638f5a7fffeb7231d35, "
                "src/v4.29.1/ErdosProblems/Erdos756.lean "
                "sha256=5aa5c5eb289bc6b85ed20b775c5afa8363f85b206fe47bdeb3cdd6f3f30c3aa5"
            ),
            309: spec(
                "AKS97, MR 1459895; plby/lean-proofs@68da20b96673899166e94638f5a7fffeb7231d35, "
                "src/v4.29.1/ErdosProblems/Erdos760.lean "
                "sha256=a6e8b2138354e03066fff722517dd8b0ae9266d9567410bc95a705c8bfafa071"
            ),
            310: spec("ErGi93, MR 1217997"),
            311: spec(
                "St24b, arXiv:2408.02400; plby/lean-proofs@68da20b96673899166e94638f5a7fffeb7231d35, "
                "src/v4.29.1/ErdosProblems/Erdos762.lean "
                "sha256=052131c0fb2702b779adf818096fb4b405315c47a3d769e6ee1d42aa06988ea2"
            ),
            312: spec("EGS90, MR 1059554"),
            313: spec(
                "Ga25, arXiv:2510.14804; plby/lean-proofs@68da20b96673899166e94638f5a7fffeb7231d35, "
                "src/v4.29.1/ErdosProblems/Erdos775.lean "
                "sha256=a6373d1394cadc827f44357ce9c6c3a864cc05da11fdd4fcaf9e608f1c84891b",
                dedupe="fail",
                dedupe_evidence=(
                    "The no-answer wrapper is a direct corollary of Gao's quantified deficit theorem "
                    "retained at supplemental_index 140."
                ),
            ),
            314: spec("Sp71, MR 282873"),
            315: spec("ChFa11, MR 2745640"),
            316: spec("Da64, MR 161830"),
            317: spec(
                "fixed counterexample proof: plby/lean-proofs@68da20b96673899166e94638f5a7fffeb7231d35, "
                "src/v4.29.1/ErdosProblems/Erdos794.lean "
                "sha256=1daa41ae0b6b7893d5df01ddff8046364a0c60504f7be17561d8fa17738e85a5"
            ),
            318: spec(
                "problem-page observation attributed to Balogh",
                importance="fail",
                importance_evidence=(
                    "The five-vertex/seven-edge implication is an elementary cleanup observation about a "
                    "misstated condition, not a separately published or frontier theorem."
                ),
            ),
            319: spec(
                "Al91, MR 1118729; plby/lean-proofs@68da20b96673899166e94638f5a7fffeb7231d35, "
                "src/v4.29.1/ErdosProblems/Erdos798.lean "
                "sha256=b3092877b7a869f229e8a750eec8b5f6091aa5a167e16cd75c2da75523b923ac",
                dedupe="fail",
                dedupe_evidence=(
                    "The t(n)=o(n) wrapper is a direct corollary of Alon's sharper "
                    "O(n^(2/3) log n) theorem retained at supplemental_index 57."
                ),
            ),
            320: spec("ErPu75, MR 392837"),
        },
        "scope_boundaries": {
            "row_287": "Rejected because the selected formal threshold inequality reverses the pinned prose/citation.",
            "row_291": "Pending until O'Donnell's dissertation is pinned and its exact construction scope is checked.",
            "row_300": "Pending exact EHS82 scope; DOI/MR metadata alone is not treated as theorem-text evidence.",
            "same_event_dedupe": "Rows 292, 301, 303, 305, 307, and 319 are denied a second credit in favor of their explicit or stronger companion rows; row 319 points across queues to supplemental_index 57.",
            "independent_lean_replay_performed": False,
            "formal_proof_source_inspection_performed": True,
            "paper_full_text_reproduced": False,
        },
    },
    "351_378": {
        "first": 351,
        "last": 378,
        "rows": {
            351: spec(
                "BoNi05, MR 2180806; plby/lean-proofs@68da20b96673899166e94638f5a7fffeb7231d35, "
                "src/v4.29.1/ErdosProblems/Erdos904.lean "
                "sha256=dc0e121c81bd2adcca2d7f9a482b252fb1573d887c6c8d27d7fdae1162e68b47"
            ),
            352: spec(
                "KhNi79, MR 562936; plby/lean-proofs@68da20b96673899166e94638f5a7fffeb7231d35, "
                "src/v4.29.1/ErdosProblems/Erdos905.lean "
                "sha256=4e999fa26534dc431e5007a86d60f1443125b55e99fb1b21fc8afe43616b66c6"
            ),
            353: spec(
                "dB51, MR 43870; plby/lean-proofs@68da20b96673899166e94638f5a7fffeb7231d35, "
                "src/v4.29.1/ErdosProblems/Erdos907.lean "
                "sha256=63df7ce57eb24207c40866ddeda1f2a05710cf3fad3de1f755e03124704723aa"
            ),
            354: spec(
                "CoHa63, MR 200185; HaSz70, MR 297607; KiKo08, MR 2396352; "
                "plby/lean-proofs@68da20b96673899166e94638f5a7fffeb7231d35, "
                "src/v4.29.1/ErdosProblems/Erdos914.lean "
                "sha256=9cab5a63801592a18ae7f33e2e81171b1fe24cc1a92a241c8659b623493a2900"
            ),
            355: spec(
                "HaSz70, MR 297607; KiKo08, MR 2396352",
                dedupe="fail",
                dedupe_evidence=(
                    "The equitable-colouring formulation is the complement-graph equivalent of the "
                    "Hajnal-Szemerédi clique-packing theorem retained at row 354."
                ),
                duplicate_rows=[354],
            ),
            356: spec(
                "Ki95, DOI 10.1002/rsa.3240070302; DaIl22, MR 4413062",
                primary_evidence=(
                    "The standard triangle-free Ramsey-number asymptotic and its chi-Ramsey translation "
                    "support the displayed f_3 theta estimate."
                ),
            ),
            357: spec("MaVe23, arXiv:2306.04007"),
            358: spec(
                "Ro77, MR 469806; plby/lean-proofs@68da20b96673899166e94638f5a7fffeb7231d35, "
                "src/v4.29.1/ErdosProblems/Erdos923.lean "
                "sha256=c60c5954ecf2e475fb2b926dff21ec8dac6572be0b6b4e4f34f3e926223d30c2"
            ),
            359: spec(
                "Al63, MR 154192; plby/lean-proofs@1d7b3f00780b85ed0462e79a1cd5650ee9055655, "
                "src/v4.29.1/ErdosProblems/Erdos93.lean"
            ),
            360: spec("BBC24, MR 4688726"),
            361: spec(
                "Er97c, MR 1425174; LeTh95, MR 1357284",
                dedupe="fail",
                dedupe_evidence=(
                    "The convex-position estimate is an immediate corollary of the no-three-collinear "
                    "theorem retained at row 362; the Fishburn attribution supplies no independent source."
                ),
                duplicate_rows=[362],
            ),
            362: spec(
                "LeTh95, MR 1357284; plby/lean-proofs@68da20b96673899166e94638f5a7fffeb7231d35, "
                "src/v4.29.1/ErdosProblems/Erdos94.lean "
                "sha256=53002f831d5b3510b2da461230ccf48d3bc7aec30beccf566b41b14bcd8dfe4e"
            ),
            363: spec("He84, MR 762186, DOI 10.1112/S0025579300010743"),
            364: spec("Hi85/87, DOI 10.2140/pjm.1987.129.307"),
            365: spec(
                "CDL25, arXiv:2505.04283; plby/lean-proofs@68da20b96673899166e94638f5a7fffeb7231d35, "
                "src/v4.29.1/ErdosProblems/Erdos958.lean "
                "sha256=2c389ecc5172a0b0f91bab6b87ba99c423675a0cf22bcb6f0838e57c7495d8dd"
            ),
            366: spec(
                "Ko16, MR 3511943; Sokoup-Weiss, https://danieltsoukup.github.io/academic/finset_colouring.pdf",
                dedupe="fail",
                dedupe_evidence=(
                    "The two-sum counterexample is the k=2 instance of the same-paper k-sum construction "
                    "retained at row 367."
                ),
                duplicate_rows=[367],
            ),
            367: spec(
                "Ko16, MR 3511943; Sokoup-Weiss, https://danieltsoukup.github.io/academic/finset_colouring.pdf"
            ),
            368: spec(
                "fixed exact proof: plby/lean-proofs@68da20b96673899166e94638f5a7fffeb7231d35, "
                "src/v4.29.1/ErdosProblems/Erdos966.lean "
                "sha256=56db2afcb88dccf5d6d48b5089238317f82034c79e0794db81dc72b0380ed09a; "
                "historical report Er75b, MR 0374075",
                primary_evidence=(
                    "The historical report lacks Spencer's original reference, so the fixed sorry-free "
                    "exact Lean proof is the primary resolution artifact used by this review."
                ),
            ),
            369: spec(
                "Yi25, arXiv:2512.16528; fixed gist sha256=6b379e4f9622c7b477a52f80ca8247327c68a965d7d7dddc1212738d3bf1919c",
                dedupe="fail",
                dedupe_evidence=(
                    "The negative answer is the direct consequence of Yip's parameterized counterexample "
                    "retained at row 370."
                ),
                duplicate_rows=[370],
            ),
            370: spec(
                "Yi25, arXiv:2512.16528; llllvvuu gist d25f037d1f1000bdabd6ca928c74c9bb, "
                "sha256=6b379e4f9622c7b477a52f80ca8247327c68a965d7d7dddc1212738d3bf1919c"
            ),
            371: spec(
                "Ti66, MR 205942",
                dedupe="fail",
                dedupe_evidence=(
                    "The infinitely-many-tuples hypothesis is a direct special case of Tijdeman's "
                    "two-tuples theorem retained at row 372."
                ),
                duplicate_rows=[372],
            ),
            372: spec(
                "Ti66, MR 205942; plby/lean-proofs@68da20b96673899166e94638f5a7fffeb7231d35, "
                "src/v4.29.1/ErdosProblems/Erdos974.lean "
                "sha256=44de9cf2801f0c84e667ff61151efcbccc154b4c47ae77ad67732c9746342d64"
            ),
            373: spec(
                "Cl67, MR 213317; Marti2203/formal-conjectures@19c63d48acce3099c242b059518c49bf8dc0eab8, "
                "FormalConjectures/ErdosProblems/987.lean "
                "sha256=2201303ab97881d35c1d9a791fdb0fe6e8fa99589498420487a9934c85386dc4",
                dedupe="fail",
                dedupe_evidence=(
                    "The limsup-infinity answer is a direct corollary of Clunie's sqrt(k) lower bound "
                    "retained at supplemental_index 165."
                ),
            ),
            374: spec(
                "APSSV26b, arXiv:2604.06609; Marti2203/formal-conjectures@19c63d48acce3099c242b059518c49bf8dc0eab8, "
                "FormalConjectures/ErdosProblems/987.lean "
                "sha256=2201303ab97881d35c1d9a791fdb0fe6e8fa99589498420487a9934c85386dc4",
                dedupe="fail",
                dedupe_evidence=(
                    "The o(k) answer is the immediate asymptotic corollary of the explicit sqrt(k log k) "
                    "upper bound retained at supplemental_index 164."
                ),
            ),
            375: spec(
                "APSSV26b, arXiv:2604.06609",
                dedupe="fail",
                dedupe_evidence=(
                    "The no-answer is the direct consequence of the explicit bounded-M high-multiplicity "
                    "counterexample retained at row 376."
                ),
                duplicate_rows=[376],
            ),
            376: spec(
                "APSSV26b, arXiv:2604.06609; plby/lean-proofs@68da20b96673899166e94638f5a7fffeb7231d35, "
                "src/v4.29.1/ErdosProblems/Erdos990.lean "
                "sha256=986d6e36f24064509f6e0b7370bea169701c5093ffd8564311784f1bb61e9ae2"
            ),
            377: spec(
                "APSSV26, arXiv:2603.29961; pitmonticone gist revision "
                "b7dfc05c525ae385b5835f89f1ada721443e4305, "
                "sha256=8e25731d664e2a4e0bb6e36960f9dc6a67380c29196196ac89e1d767092a5f11",
                primary_evidence=(
                    "The publication supplies the theorem. The fixed Lean formalization was inspected and "
                    "explicitly declares the Maynard-Tao bounded-gaps input as an axiom."
                ),
            ),
            378: spec("CLLW24, arXiv:2406.19491"),
        },
        "scope_boundaries": {
            "row_356": "Credits the displayed f_3 theta estimate through the standard R(3,t) asymptotic translation.",
            "row_368": "The fixed exact formal proof, rather than an unavailable Spencer reference, is the primary artifact.",
            "row_377": "The formal proof's Maynard-Tao bounded-gaps axiom boundary is explicit; the mathematical publication remains primary.",
            "same_event_dedupe": "Rows 355, 361, 366, 369, 371, and 375 are equivalent or direct-corollary companions of retained stronger rows.",
            "independent_lean_replay_performed": False,
            "formal_proof_source_inspection_performed": True,
            "paper_full_text_reproduced": False,
        },
    },
    "321_350": {
        "first": 321,
        "last": 350,
        "rows": {
            321: spec("So09d, MR 2538014", dedupe="fail", dedupe_evidence="The original C-exists wrapper is the direct weak form of Solymosi's C=1 theorem retained at row 322.", duplicate_rows=[322]),
            322: spec("So09d, MR 2538014; plby/lean-proofs@68da20b96673899166e94638f5a7fffeb7231d35, Erdos818.lean sha256=0a0ae74e"),
            323: spec("GIL, arXiv:2306.16035; DOI 10.1016/j.jnt.2024.03.010; MR 4739371", exact="fail", primary="fail", exact_evidence="The formal HasPosDensity requires an existing positive natural density, while GIL proves only a positive lower-density/counting lower bound.", primary_evidence="The cited primary theorem does not establish existence of the natural-density limit required by the selected formal type."),
            324: spec("Larsen-Daniel/Erdos-825@18411fce, 825.pdf sha256=cf656022d032285ca9703c132753d650873dbeca1adf8e1c3597b730365ca533"),
            325: spec("elementary n=70 witness", importance="fail", importance_evidence="The necessary-condition row is only an elementary n=70 witness and has no independent research-theorem source."),
            326: spec("AMS25, arXiv:2507.01928v2; Ch74, MR 369170; fixed gist@7d811e, sha256=ac2b3a9"),
            327: spec("van Doorn-Everts, arXiv:2511.04585v1; plby/lean-proofs@68da20b, Erdos845.lean sha256=716ecb1b"),
            328: spec("PSV, arXiv:2602.21275v1; google-deepmind/formal-conjectures@2404258, 846.lean sha256=3b909a34"),
            329: spec("RRS24, arXiv:2311.08556v2; MR 4810571; DOI 10.1112/jlms.12987"),
            330: spec("Price/GPT proof, fixed Overleaf main.tex sha256=4cd4c83c7f4d242bc3d42a07914007cf5dee645b7722d225baee50b3e38e540e", exact="fail", primary="fail", exact_evidence="The formal HasDensity d requires an existing natural density, while the selected prose claims only density informally.", primary_evidence="The fixed main theorem proves lower natural density at least 1-epsilon, not existence of the natural-density limit."),
            331: spec("Ro34, MR 1512916", exact="fail", exact_evidence="TwoPowAddSet 1 contains all prime powers (and boundary cases), not only the prose's primes/1, so the stated Romanoff set and formal set are unequal."),
            332: spec("SaTh15, MR 3385638", dedupe="fail", dedupe_evidence="The not-little-o answer is directly implied by the explicit 0.16 sqrt(N) exponent bound retained at row 333.", duplicate_rows=[333]),
            333: spec("Saxton-Thomason, MR 3385638; plby/lean-proofs@68da20b, Erdos862.lean sha256=906d86e9"),
            334: spec("classical folklore", importance="fail", importance_evidence="The source itself labels this the classical elementary k=2 folklore fact; it is not a separately sourced frontier theorem."),
            335: spec("CES75, MR 369305"),
            336: spec("Fr93 background", dedupe="fail", dedupe_evidence="The broad negative wrapper is replaced by the stricter Freud 19/36 construction retained at supplemental_index 58."),
            337: spec("Adenwalla observation; CoPh96, MR 1386875", dedupe="fail", importance="fail", dedupe_evidence="The 2/3+o(1) upper bound is strictly weakened by the Coppersmith-Phillips bound retained at supplemental_index 152.", importance_evidence="The source is an elementary webpage observation rather than an independently sourced theorem."),
            338: spec("Larsen-Larsen", dedupe="fail", dedupe_evidence="The tends-to-infinity counterexample is strictly weakened by the c log n counterexample from the same solution retained at row 339.", duplicate_rows=[339]),
            339: spec("Larsen-Larsen, Robust additive bases without minimal subbases, github@3e4c4db/868.pdf sha256=d7c2ec8e1c5681e1b93dc1470f1c9a5c45b6b3c9f71d964a3ee3d6b3a90f9a3c"),
            340: spec("plby/lean-proofs@68da20b, v4.29.1 Erdos871.lean sha256=cf8eb5ef; ErNa88 MR 938865; ErNa89 MR 1030090"),
            341: spec("Larsen github@c4c27cdf/884.pdf sha256=763d0dc89b48eb9c51f7bad3056294127db61c26d19cac87093d4d2527baf39a; Jayyhk/erdos-lean@f8a5197, sha256=4ac63126"),
            342: spec("Tao conditional PDF sha256=39e4848e", exact="fail", primary="fail", dedupe="fail", exact_evidence="The formal Hardy-Littlewood predicate is a Big-O asymptotic condition, not Tao's qualitative prime-tuples existence hypothesis.", primary_evidence="The selected formal implication therefore does not match the fixed conditional proof's exact assumption.", dedupe_evidence="In any case, the conditional negative conclusion is subsumed by the unconditional disproof retained at row 341.", duplicate_rows=[341]),
            343: spec("Ulam erdos888.pdf sha256=cd90dd7f6ba8d7f3f0073067c9ba9a80276c58f106d1d39961b0a7b33c8a785e"),
            344: spec("prime-set observation", importance="fail", dedupe="fail", importance_evidence="The primes example is an elementary lower bound, not a separately sourced frontier theorem.", dedupe_evidence="It is also strictly subsumed by the theta asymptotic retained at row 343.", duplicate_rows=[343]),
            345: spec("Wi70", exact="fail", primary="fail", exact_evidence="The prose/source theorem states f(n)=c log n+O(1), while the formal type records only a one-sided upper inequality.", primary_evidence="Wi70 does not bind the weaker one-sided formal surface as an exact statement of its theorem."),
            346: spec("Wi81, MR 637365; plby/lean-proofs@68da20b, v4.24 Erdos897.lean sha256=aaf11992"),
            347: spec("Erdős-Mordell inequality; Er82e, MR 690096; plby/lean-proofs@68da20b, Erdos898.lean sha256=d66867f0"),
            348: spec("Ru78, MR 519317"),
            349: spec("unit-distance disproof", dedupe="fail", dedupe_evidence="The broad no-answer wrapper is directly implied by the explicit construction retained at supplemental_index 60."),
            350: spec("arXiv:2605.20695; arXiv:2605.20579", dedupe="fail", dedupe_evidence="The qualitative polynomial lower bound is strictly strengthened by Sawin's explicit c=0.014114 theorem retained at supplemental_index 60."),
        },
        "scope_boundaries": {
            "formal_scope_rejects": "Rows 323, 330, 331, 342, and 345 fail exact primary/formal scope; solved-page status is not enough.",
            "cross_queue_dedupe": "Rows 336, 337, 349, and 350 are replaced by stronger supplemental indices 58, 152, and 60.",
            "independent_lean_replay_performed": False,
            "formal_proof_source_inspection_performed": True,
            "paper_full_text_reproduced": False,
        },
    },
}


def gate(verdict: str, evidence: str, **extra: Any) -> dict[str, Any]:
    result: dict[str, Any] = {"verdict": verdict, "evidence": evidence}
    result.update(extra)
    return result


def build_row(index: int, source: dict[str, Any], raw_line: bytes, row_spec: dict[str, Any], queue_sha: str) -> dict[str, Any]:
    exact = row_spec["exact"]
    primary = row_spec["primary"]
    importance = row_spec["importance"]
    dedupe = row_spec["dedupe"]
    verdicts = [exact, "pass", primary, importance, dedupe, "pass"]
    decision = "reject" if "fail" in verdicts else "pending" if "pending" in verdicts else "accept"
    all_pass = all(value == "pass" for value in verdicts)
    if (decision == "accept") != all_pass:
        raise ValueError(f"row {index}: accept/all-gates invariant failed")

    parent = source["parent"]
    identity = source["identity"]
    locator = parent["locator"]
    statement = parent["mathematical_statement"]
    status = source["source_problem"]["derived_status"]
    problem = source["source_problem"]["problem_number"]

    exact_default = (
        "Pinned natural-language block and exact formal type were compared for polarity, quantifiers, "
        "domain, constants, and scope."
    )
    primary_default = (
        "A fixed publication, primary proof, or fixed proof artifact supports the exact statement, "
        "an equivalent form, or an explicitly stronger theorem."
    )
    importance_default = (
        "This is a nontrivial numbered-problem resolution or a separately sourced research theorem "
        "materially used in the problem record."
    )
    dedupe_default = (
        "The exact parent identity is unique and manual cohort comparison found no retained "
        "semantic-equivalent credit in rows 285-320."
    )

    return {
        "schema_version": "awesome-theorems/frontier-theorem-row-review/5.5",
        "source_binding": {
            "path": QUEUE_REL,
            "full_file_sha256": queue_sha,
            "zero_based_row": index,
            "row_sha256": sha256_bytes(raw_line),
        },
        "identity": {
            "problem_number": problem,
            "stage_claim_id": parent["stage_claim_id"],
            "variant_id": parent["variant_id"],
            "qualified_name": parent["qualified_name"],
            "role": identity["role_within_problem"],
            "semantic_identity_key": identity["semantic_identity_key"],
            "identity_payload_sha256": identity["identity_payload_sha256"],
        },
        "statement_binding": {
            "member_path": locator["member_path"],
            "source_revision": locator["revision"],
            "line_start": locator["line_start"],
            "line_end": locator["line_end"],
            "raw_block_sha256": locator["raw_block_sha256"],
            "formal_type_sha256": parent["formal_type_sha256"],
            "statement_sha256": statement["statement_sha256"],
        },
        "decision": decision,
        "all_gates_pass": all_pass,
        "gates": {
            "exact_statement_scope": gate(exact, row_spec["exact_evidence"] or exact_default),
            "current_upstream_status": gate(
                "pass",
                f"Pinned teorth status is {status['state']} as of {status.get('last_update', source['source_problem'].get('last_update', 'pinned snapshot'))}; numbered problem page was checked resolved during review.",
                problem_page=f"https://www.erdosproblems.com/{problem}",
            ),
            "primary_resolution": gate(
                primary,
                row_spec["primary_evidence"] or primary_default,
                citation_evidence=row_spec["citation"],
                problem_page=f"https://www.erdosproblems.com/{problem}",
            ),
            "importance_frontier": gate(
                importance,
                row_spec["importance_evidence"] or importance_default,
            ),
            "semantic_dedupe": gate(
                dedupe,
                row_spec["dedupe_evidence"] or dedupe_default,
                duplicate_review_rows=row_spec["duplicate_rows"],
            ),
            "rights": gate(
                "pass",
                "Only hashes, identifiers, locators, and original assessment are emitted. The pinned "
                "Lean member header is Apache-2.0; third-party paper text and source docstrings are not reproduced.",
            ),
        },
        "rights_boundary": {
            "formal_member_terms": "Apache-2.0",
            "formal_policy_locator": "pinned Formal Conjectures README.md:120-148",
            "erdos_status_snapshot_terms": "Apache-2.0",
            "third_party_text_reused": False,
            "metadata_and_locator_only": True,
        },
        "credit": {
            "frontier_theorem_credit_granted": False,
            "new_theorem_credit_granted": False,
            "release_modified": False,
        },
        "reviewer_notes": (
            "All six review gates pass; review evidence only, no release credit."
            if decision == "accept"
            else "Evidence remains pending at one or more gates; no release credit."
            if decision == "pending"
            else "Rejected by at least one review gate; no release credit."
        ),
    }


def build_slice(name: str) -> tuple[Path, Path]:
    config = SLICES[name]
    first = config["first"]
    last = config["last"]
    expected = set(range(first, last + 1))
    if set(config["rows"]) != expected:
        raise ValueError(f"{name}: decision rows do not exactly cover {first}..{last}")

    raw_lines = QUEUE.read_bytes().splitlines()
    queue_sha = sha256_file(QUEUE)
    if len(raw_lines) != 379:
        raise ValueError(f"queue row count drifted: {len(raw_lines)}")

    rows = [
        build_row(index, json.loads(raw_lines[index]), raw_lines[index], config["rows"][index], queue_sha)
        for index in range(first, last + 1)
    ]
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    review_path = OUT_DIR / f"erdos_{name}.jsonl"
    review_payload = b"".join(
        (json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n").encode("utf-8")
        for row in rows
    )
    review_path.write_bytes(review_payload)

    decisions = Counter(row["decision"] for row in rows)
    gate_counts: dict[str, dict[str, int]] = {}
    for gate_name in rows[0]["gates"]:
        gate_counts[gate_name] = dict(Counter(row["gates"][gate_name]["verdict"] for row in rows))
    pending_rows = [row["source_binding"]["zero_based_row"] for row in rows if row["decision"] == "pending"]
    reject_rows = [row["source_binding"]["zero_based_row"] for row in rows if row["decision"] == "reject"]
    semantic_rejects = [
        row["source_binding"]["zero_based_row"]
        for row in rows
        if row["gates"]["semantic_dedupe"]["verdict"] == "fail"
    ]
    exact_nonpass = [
        row["source_binding"]["zero_based_row"]
        for row in rows
        if row["gates"]["exact_statement_scope"]["verdict"] != "pass"
    ]
    primary_nonpass = [
        row["source_binding"]["zero_based_row"]
        for row in rows
        if row["gates"]["primary_resolution"]["verdict"] != "pass"
    ]
    importance_rejects = [
        row["source_binding"]["zero_based_row"]
        for row in rows
        if row["gates"]["importance_frontier"]["verdict"] == "fail"
    ]
    stage_digest = ordered_digest([row["identity"]["stage_claim_id"] for row in rows])
    identity_digest = ordered_digest([row["identity"]["identity_payload_sha256"] for row in rows])
    row_digest = ordered_digest([row["source_binding"]["row_sha256"] for row in rows])
    review_sha = sha256_bytes(review_payload)
    authority_preimage = f"{queue_sha} {review_sha} {stage_digest} {identity_digest}\n".encode("ascii")

    summary = {
        "schema_version": "awesome-theorems/frontier-theorem-review-summary/5.5",
        "review_name": f"erdos_{name}",
        "scope": f"Human gate review of zero-based rows {first} through {last} inclusive of the capped Erdős resolved-theorem candidate queue.",
        "review_date_utc": "2026-08-10",
        "source_binding": {
            "path": QUEUE_REL,
            "sha256": queue_sha,
            "source_rows": len(raw_lines),
            "reviewed_zero_based_first": first,
            "reviewed_zero_based_last": last,
            "reviewed_rows": len(rows),
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
            "bytes": len(review_payload),
            "rows": len(rows),
            "ordered_source_row_sha256_values_sha256": row_digest,
            "ordered_stage_claim_ids_sha256": stage_digest,
            "ordered_identity_payload_sha256_values_sha256": identity_digest,
        },
        "counts": {
            "accept": decisions.get("accept", 0),
            "pending": decisions.get("pending", 0),
            "reject": decisions.get("reject", 0),
            "all_gates_pass": sum(row["all_gates_pass"] for row in rows),
            "unique_stage_claim_ids": len({row["identity"]["stage_claim_id"] for row in rows}),
            "unique_semantic_identity_keys": len({row["identity"]["semantic_identity_key"] for row in rows}),
            "unique_problem_numbers": len({row["identity"]["problem_number"] for row in rows}),
            "accepted_unique_problem_numbers": len(
                {row["identity"]["problem_number"] for row in rows if row["decision"] == "accept"}
            ),
        },
        "gate_verdict_counts": gate_counts,
        "nonacceptance": {
            "pending_rows": pending_rows,
            "reject_rows": reject_rows,
            "semantic_dedupe_reject_rows": semantic_rejects,
            "exact_scope_nonpass_rows": exact_nonpass,
            "primary_resolution_nonpass_rows": primary_nonpass,
            "importance_reject_rows": importance_rejects,
        },
        "method": {
            "statement_review": "Compared every pinned natural-language block and exact formal type for polarity, quantifiers, domain, constants, and scope.",
            "status_review": "Checked every pinned teorth status record and the numbered Erdős page during review.",
            "resolution_review": "Matched live bibliography/remarks to fixed MR, arXiv, PDF, or git-commit evidence and inspected material formal-proof boundaries.",
            "importance_review": "Required a nontrivial numbered-problem resolution or separately sourced research theorem; routine support and elementary cleanup rows were rejected.",
            "dedupe_review": "Denied double credit to direct corollaries, special cases, and same-solution restatements inside the cohort.",
            "rights_review": "Emitted metadata, hashes, locators, and original assessments only; no third-party paper text or source docstring is copied into the review.",
        },
        "scope_boundaries": config["scope_boundaries"],
        "credit_boundary": {
            "frontier_theorem_credit_granted": 0,
            "new_theorem_credit_granted": 0,
            "release_modified": False,
            "accepted_rows_are_release_credit": False,
        },
        "validation": {
            f"contiguous_order_{first}_through_{last}": True,
            "source_row_sha256_recomputed_for_every_row": True,
            "decision_partition_sums_to_reviewed_rows": True,
            "accept_iff_all_gates_pass": True,
            "all_credit_fields_false": True,
            "authority_preimage_format": "ASCII source_sha256, review_sha256, ordered_stage_claim_ids_sha256, and ordered_identity_payload_sha256_values_sha256 separated by one space and terminated by LF",
            "authority_sha256": sha256_bytes(authority_preimage),
        },
    }
    summary_path = OUT_DIR / f"erdos_{name}_summary.json"
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return review_path, summary_path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("slice", choices=sorted(SLICES))
    args = parser.parse_args()
    review, summary = build_slice(args.slice)
    print(review.relative_to(ROOT))
    print(summary.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
