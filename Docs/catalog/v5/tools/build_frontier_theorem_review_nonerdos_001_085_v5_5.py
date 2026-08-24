#!/usr/bin/env python3
"""Build the human evidence ledger for non-Erdos frontier ranks 1--85.

This builder is deliberately self-contained and deterministic. It reads the
frozen 5.4 release, 5.5 candidate queue, pinned source archive, and repo-owned
evidence. It never allocates an ID and never edits a release or queue artifact.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import tarfile
from collections import Counter
from pathlib import Path
from typing import Any


SCHEMA = "awesome-theorems/frontier-existing-credit-review/5.5"
RECEIPT_SCHEMA = "awesome-theorems/frontier-existing-credit-review-receipt/5.5"
REVIEW_AS_OF = "2026-08-10"
BATCH = "nonerdos-001-085"

QUEUE_REL = Path("Docs/catalog/v5/curation/Frontier_Theorem_Candidate_Queue_v5_5.json")
PARENT_REL = Path("Docs/catalog/v5/releases/5.4/Claim_Catalog.json")
MANIFEST_REL = Path("Docs/catalog/v5/releases/5.4/Release_Manifest.json")

EXPECTED_QUEUE_FILE_SHA256 = "b3b28b81cfcd9fe4dbf002d2bb8d9bedaa8094656396e224abb5c6221530b2fc"
EXPECTED_QUEUE_AUTHORITY_SHA256 = "375ca73546293f74fdc966209d4be0d184ad5e28273c70aecc7a12a601548133"
EXPECTED_PARENT_SHA256 = "384c1e34a57443dafe2e2ce70e36d6a6e23c6d03e006171b94aa2defa92e9709"
EXPECTED_MANIFEST_SHA256 = "8cc6a2b5d4f94861eedbf31c76026e08191595c2927ba253cdae3b26d9a8edc9"
EXPECTED_RELEASE_ROOT_SHA256 = "c6f559861849d839ceda2f10bc7878687e35d6c897ea1c316ea4523bc7673813"
SOURCE_COMMIT = "2270d31e8dd611521f979de6d86da364930b7669"
EXPECTED_SOURCE_ARCHIVE_SHA256 = "51535f4755574d97672515a75b8b076065aba2c0d79631e99fa57719f484dcc8"
EXPECTED_LICENSE_SHA256 = "cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30"

ELIGIBLE = {
    1, 2, 3, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,
    21, 22, 23, 24, 26, 27, 28, 29, 31, 33, 39, 40,
    48, 53, 54, 57, 58, 61, 65, 67, 68, 70, 71, 75,
    78, 80, 81, 84,
}
REJECT = {19, 34, 55, 59, 62, 64, 69, 73, 74, 77, 79, 82}
PENDING = set(range(1, 86)) - ELIGIBLE - REJECT

CONCEPTUAL_DUPLICATES = {59: 57, 74: 75, 79: 80}
NONFRONTIER_REJECTS = {19, 34, 55, 62, 64, 73, 77, 82}

# These are review conclusions, not source claims.  They explain why a row passed,
# remains pending, or was rejected.  No prose from a proof is reproduced.
FINDINGS: dict[int, str] = {
    1: "Read's 1985 BLMS counterexample matches the stated complex l1 invariant-subspace theorem.",
    2: "The pinned Khandhawit--Pagonakis--Sriswasdi paper proves the 0.232239 convex universal-cover lower bound.",
    3: "The Norwood--Poole DOI fixes the 0.260437 upper-bound construction; monotonicity of covering plus nonatomic measure-padding upgrades area <= a to the catalog's existence statement with area exactly a.",
    4: "The paper proves a subword-complexity formula, while the source itself says the bridge from the actual fixed word to the generating-function definition remains to be formalized.",
    5: "Park--Pham resolves the related Kahn--Kalai conjecture, not this missing lemma; the reported Perles counterexample lacks a fixed primary proof.",
    6: "arXiv:2606.22997v1 states and proves the exact gcd/prime-power equivalence; the pinned Lean target is closed.",
    7: "arXiv:2007.11017 proves convergence of the stated Borwein sine series.",
    8: "arXiv:2605.22763v2 supplies the theorem and proof, and the pinned Lean proof closes WOWII Conjecture 2.",
    9: "The pinned Casas--Alvero paper proves the positive-characteristic degree p+1 counterexample, with a matching closed Lean target.",
    10: "The pinned Casas--Alvero paper proves the degree 2 p^k case with the same scope as the candidate.",
    11: "Theorem B.1 of arXiv:2602.05192v2 proves the finite-free Stam inequality exactly as stated.",
    12: "Theorem 1.1 of arXiv:2205.15191 proves the large-n alternating-group product-free result.",
    13: "Pardon's pinned paper proves the Hilbert--Smith conjecture for three-dimensional manifolds.",
    14: "The theorem and arXiv:2510.11768 prove irreducibility; the docstring phrase 'formal disproof' is a polarity typo and is not propagated.",
    15: "The a=0 instance of Theorem 1.1 in arXiv:1207.4841 gives complexity(3^n)=3n.",
    16: "Only a mutable Busy Beaver wiki sketch and Discord discussion were identified; no stable complete primary proof was fixed.",
    17: "The WOWII page records a solution status but no complete fixed primary proof for this exact inequality was captured.",
    18: "The WOWII page records Waller's counterexample but no complete fixed primary counterexample proof was captured.",
    19: "The rational three-cubes parametrization is a historical classical theorem, not a frontier/open-problem resolution credit under this review policy.",
    20: "The WOWII page records a proof attribution but no complete fixed primary proof for this exact formal scope was captured.",
    21: "The pinned, closed Lean proof establishes the exact WOWII Conjecture 144 inequality.",
    22: "The pinned, closed Lean counterexample establishes falsity of WOWII Conjecture 327.",
    23: "The pinned, closed Lean proof establishes the exact denominator-free WOWII Conjecture 143 formulation.",
    24: "The pinned, closed Lean counterexample establishes falsity of WOWII Conjecture 109.",
    25: "The WOWII page gives a numerical counterexample description, but a complete fixed proof of all graph invariants was not captured.",
    26: "The pinned, closed Lean proof establishes the exact strengthened Slud-bound statement.",
    27: "The pinned, closed Lean proof establishes WOWII Conjecture 316 with the stated complement-average-degree scope.",
    28: "The pinned, closed Lean proof establishes WOWII Conjecture 1.",
    29: "The pinned, closed Lean counterexample establishes falsity of WOWII Conjecture 58.",
    30: "The source describes a counterexample, but no fixed complete proof of its induced-forest bound was captured.",
    31: "The pinned, closed Lean counterexample establishes falsity of WOWII Conjecture 194.",
    32: "The source describes a counterexample, but no fixed complete proof of all reported graph invariants was captured.",
    33: "The pinned, closed Lean proof establishes WOWII Conjecture 315.",
    34: "The finite-dimensional invariant-subspace statement is a standard Jordan-form consequence, not a frontier theorem.",
    35: "Only a mutable Busy Beaver wiki/Discord proof report was identified; no stable complete primary proof was fixed.",
    36: "The WOWII page supplies attribution/status but no complete fixed primary proof for this exact path/radius inequality.",
    37: "A counterexample is described, but no fixed complete primary proof of the asserted graph invariants was captured.",
    38: "The inclusion--exclusion attribution is not accompanied by a fixed complete primary proof for the exact formal statement.",
    39: "The pinned, closed Lean proof establishes WOWII Conjecture 322.",
    40: "The pinned, closed Lean proof establishes the audited WOWII Conjecture 217 formulation.",
    41: "The WOWII page does not provide a fixed complete proof for this exact induced-bipartite-subgraph bound.",
    42: "The WOWII page does not provide a fixed complete proof for this exact diameter/neighbourhood bound.",
    43: "The WOWII page does not provide a fixed complete proof for this exact spanning-tree bound.",
    44: "The WOWII page does not provide a fixed complete proof for this exact average-distance bound.",
    45: "The WOWII page does not provide a fixed complete proof for this exact average-degree bound.",
    46: "The WOWII page does not provide a fixed complete proof for this exact diameter bound.",
    47: "The WOWII page does not provide a fixed complete proof for this exact non-edge-neighbourhood bound.",
    48: "The fixed Gro-Tsen MathOverflow answer gives a complete transfinite construction and proves the exact R-to-R^2 connected-bijection variant.",
    49: "The WOWII page does not provide a fixed complete proof for this exact sphere/leaf bound.",
    50: "The WOWII page does not provide a fixed complete proof for this exact n-m-a leaf bound.",
    51: "The cited packing paper was not fixed as full text and checked against the exact 501/500 rectangle family and quantifiers.",
    52: "The cited packing paper was not fixed as full text and checked against the exact 133/132 rectangle family and quantifiers.",
    53: "The pinned Wang--Zahl paper proves the three-dimensional Kakeya conjecture.",
    54: "Theorem 1.3 of Tao's pinned paper proves the stated quantitative lonely-runner improvement.",
    55: "The K_2,2 Sidorenko case is a classical Cauchy--Schwarz textbook special case, not a distinct frontier credit.",
    56: "The source explicitly leaves the main tree induction as sorry; only the subsingleton base case is closed.",
    57: "Keevash's pinned general design-existence theorem implies infinitely many t=5 Steiner systems and receives the single credit for this resolution.",
    58: "The pinned Bukh--Chao paper proves the stated sharp finite-field Kakeya density bound.",
    59: "This t=4 corollary is the same Keevash general design-existence resolution already credited at rank 57.",
    60: "The Kisielewicz formula was not accompanied by a fixed, theorem-level primary proof that was checked against the exact indexing and bit conventions.",
    61: "Together the pinned Murray prime-characteristic paper and Gardam complex-group-ring paper cover the candidate's prime and zero characteristic claim.",
    62: "Gauss's O(r) circle-error estimate is a classical elementary result, not a frontier credit.",
    63: "The Zhang and Knorr--Lempken--Thielcke primary proofs were not fixed and checked against the exact solvable ah-group equivalence.",
    64: "Selfridge's finite covering proof for 78557 is a classical computation, not a frontier credit in this queue.",
    65: "Perelman's three pinned papers provide the accepted proof program for the Poincare conjecture.",
    66: "The source gives a proof narrative but no independently fixed complete proof of the global nonnegativity and identification step.",
    67: "The fixed MathOverflow answer gives the idealization construction, and the pinned Lean target proves existence of the proper invertible ideal in a total ring of fractions.",
    68: "The pinned, closed Lean proof gives the stated strict support-function separator for Green problem 57 over Z/3Z.",
    69: "The natural-language claim invokes the characteristic-zero field Jacobian conjecture, while the formal counterexample quantifies far more general rings; the classical conjecture remains open.",
    70: "The pinned Fox--Sah--Sawhney--Stoner--Zhao Triforce and Corners paper proves that the exponent is exactly 4.",
    71: "The main theorem of arXiv:2602.20143v2 proves the stated suffix-prefix avoidance product bound.",
    72: "The classical Brown--Schreiber--Taylor direction was not fixed as a complete primary source and checked against the candidate's exact Bessel witness.",
    73: "Euler's necessary form for an odd perfect number is a classical theorem, not a frontier resolution credit.",
    74: "The boundedness variant is witnessed by the same counterexample as rank 75 and is rejected as duplicate resolution credit.",
    75: "The fixed MathOverflow answer and pinned Lean target give a C1 counterexample in R^2 to the original supremum question (and boundedness equivalence).",
    76: "Danilov's sharpness result was not accompanied by a fixed complete primary proof checked against every quantifier in the formal statement.",
    77: "This is a conditional implication from a stronger prime-gap hypothesis; it neither proves Legendre's conjecture nor constitutes a frontier main result.",
    78: "The pinned Manners paper proves that finitely many rotations of every positive-width pyjama set cover the plane.",
    79: "The N=4,D=4 statement is a direct special case of the even N>=4,D=N theorem credited at rank 80.",
    80: "The pinned, closed Lean proof establishes nonexistence for every even N>=4 with D=N.",
    81: "The pinned Gowers--Green--Manners--Tao paper proves the polynomial Freiman--Ruzsa/Marton covering statement.",
    82: "The n^2 estimate is the paper's elementary pigeonhole upper bound, not a significant frontier resolution.",
    83: "The claimed 1000-digit Giuga lower bound lacks a fixed theorem-level primary source and exact scope check.",
    84: "Theorem 6 of Ford's pinned paper proves the stated 10^(10^10) lower bound for a Carmichael counterexample.",
    85: "The Ahlfors--Grunsky 1937 source was not fixed and checked against the exact gamma-function normalization of Bloch's constant.",
}

PENDING_REASON: dict[int, str] = {
    3: "exact_numeric_scope_not_verified",
    4: "definition_to_source_object_bridge_missing",
    5: "cited_resolution_scope_mismatch_and_counterexample_unfixed",
    16: "unstable_nonprimary_proof_only",
    17: "complete_primary_proof_not_fixed", 18: "complete_primary_proof_not_fixed",
    20: "complete_primary_proof_not_fixed", 25: "complete_primary_proof_not_fixed",
    30: "complete_primary_proof_not_fixed", 32: "complete_primary_proof_not_fixed",
    35: "unstable_nonprimary_proof_only", 36: "complete_primary_proof_not_fixed",
    37: "complete_primary_proof_not_fixed", 38: "complete_primary_proof_not_fixed",
    41: "complete_primary_proof_not_fixed", 42: "complete_primary_proof_not_fixed",
    43: "complete_primary_proof_not_fixed", 44: "complete_primary_proof_not_fixed",
    45: "complete_primary_proof_not_fixed", 46: "complete_primary_proof_not_fixed",
    47: "complete_primary_proof_not_fixed", 49: "complete_primary_proof_not_fixed",
    50: "complete_primary_proof_not_fixed", 51: "paywalled_primary_scope_not_verified",
    52: "paywalled_primary_scope_not_verified", 56: "main_formal_proof_incomplete",
    60: "primary_proof_not_fixed", 63: "primary_proof_not_fixed",
    66: "primary_proof_not_fixed", 72: "primary_proof_not_fixed",
    76: "primary_proof_not_fixed", 83: "primary_proof_not_fixed",
    85: "primary_proof_not_fixed",
}

REJECT_REASON: dict[int, str] = {
    19: "historical_nonfrontier_result", 34: "textbook_nonfrontier_result",
    55: "textbook_special_case_nonfrontier", 59: "conceptual_duplicate_resolution",
    62: "classical_elementary_nonfrontier", 64: "classical_finite_cover_nonfrontier",
    69: "formal_scope_mismatch_open_classical_conjecture",
    73: "classical_nonfrontier_result", 74: "conceptual_duplicate_resolution",
    77: "conditional_implication_not_resolution", 79: "conceptual_duplicate_resolution",
    82: "elementary_bound_nonfrontier",
}

# Assets are relative to --evidence-root.  The hashes make the references fixed;
# URLs alone are never used as the fixity mechanism except the DOI at rank 1.
ASSETS: dict[str, dict[str, str]] = {
    "rendering_worm_upper": {"asset_path": "reference-snapshots/web/springer-10.1007-s00454-002-0774-3-rendering.txt", "sha256": "6ec96221cd6bc357aa445a0a4666ce1752f57b28d98f887dd2068ec149e9fc90", "kind": "fixed_fulltext_rendering", "locator": "https://link.springer.com/content/pdf/10.1007/s00454-002-0774-3.pdf"},
    "pdf_1101": {"asset_path": "downloads/arxiv-1101.5638.pdf", "sha256": "9fa6e50aaba59459efd7e62f578573c5be3f866732ad2903319d2f8ab4e0a261", "kind": "fixed_arxiv_pdf", "locator": "https://arxiv.org/pdf/1101.5638"},
    "pdf_2606": {"asset_path": "downloads/arxiv-2606.22997.pdf", "sha256": "1c57be5823d785c05584b0b7481cc1a0ca43dd07549e4b2e100ab621f0d9f6b7", "kind": "fixed_arxiv_pdf", "locator": "https://arxiv.org/pdf/2606.22997v1"},
    "pdf_2007": {"asset_path": "downloads/arxiv-2007.11017.pdf", "sha256": "6bf1e83b14decacfcc6e85de9f48c2f66b04bc5a7d706b23ea6851dfef7ab08b", "kind": "fixed_arxiv_pdf", "locator": "https://arxiv.org/pdf/2007.11017"},
    "pdf_2605": {"asset_path": "downloads/arxiv-2605.22763.pdf", "sha256": "d71b78f1ea764ea0489b7fdec3c53d394cf99cd2ac2a22c1d61e744618e9573d", "kind": "fixed_arxiv_pdf", "locator": "https://arxiv.org/pdf/2605.22763v2"},
    "pdf_ca": {"asset_path": "downloads/arxiv-math_0605090.pdf", "sha256": "086fbe59afdcd46c9f729ee38f14d0c44310612cb0c3506189a2119606beecdc", "kind": "fixed_arxiv_pdf", "locator": "https://arxiv.org/pdf/math/0605090"},
    "pdf_stam": {"asset_path": "downloads/arxiv-2602.05192.pdf", "sha256": "d026aa8d9c07307dd889108f99b2dc7b277189314723bc46e9de0489ccac901e", "kind": "fixed_arxiv_pdf", "locator": "https://arxiv.org/pdf/2602.05192v2"},
    "pdf_green4": {"asset_path": "downloads/arxiv-2205.15191.pdf", "sha256": "132e552c49541bc7a3d23f8517ad96ecb52a903f8b7fc8177d4cc3a273252f5b", "kind": "fixed_arxiv_pdf", "locator": "https://arxiv.org/pdf/2205.15191"},
    "pdf_hs3": {"asset_path": "downloads/arxiv-1112.2324.pdf", "sha256": "828c1e930929c38673f732d0d3b1254dcd66a0f6c1822124c48c7fa73806e157", "kind": "fixed_arxiv_pdf", "locator": "https://arxiv.org/pdf/1112.2324"},
    "pdf_cuboid": {"asset_path": "downloads/arxiv-2510.11768.pdf", "sha256": "ceb69c07fee129a0f8c695102dca67705c8681bd92e288c31440b7a88266eec2", "kind": "fixed_arxiv_pdf", "locator": "https://arxiv.org/pdf/2510.11768"},
    "pdf_complexity": {"asset_path": "downloads/arxiv-1207.4841.pdf", "sha256": "5ee225ff737b4f308c0502534074f45ddc6c1d324658494f65e413b8122d4137", "kind": "fixed_arxiv_pdf", "locator": "https://arxiv.org/pdf/1207.4841"},
    "web_mo260589": {"asset_path": "reference-snapshots/web/mathoverflow.net_questions_260589.html", "sha256": "9f698e753d49bd9da0d35740d044bd93d1017c4bdc6a24f594eeebc94a160cdb", "kind": "fixed_web_snapshot", "locator": "https://mathoverflow.net/a/260589"},
    "pdf_kakeya3": {"asset_path": "downloads/arxiv-2502.17655.pdf", "sha256": "631e8b2118e3d03ded2d5fe79f9acdf74353877d143e9887a3c31278cd13ed01", "kind": "fixed_arxiv_pdf", "locator": "https://arxiv.org/pdf/2502.17655"},
    "pdf_lonely": {"asset_path": "downloads/arxiv-1701.02048.pdf", "sha256": "a65c771fb04c416b1c81a5b07560700b75dd897488f5a17d894a4acc3a93eccc", "kind": "fixed_arxiv_pdf", "locator": "https://arxiv.org/pdf/1701.02048"},
    "pdf_keevash": {"asset_path": "downloads/arxiv-1401.3665.pdf", "sha256": "892d8b968c3e56e588297fdc72ef67e36efe9a32173228412b310de63d00eccf", "kind": "fixed_arxiv_pdf", "locator": "https://arxiv.org/pdf/1401.3665"},
    "pdf_bukh_chao": {"asset_path": "downloads/arxiv-2108.00074.pdf", "sha256": "b0b2a3c979d8ce5a8a9662a30383780a75984c71730c68e5cadb1f9ba9a0b48a", "kind": "fixed_arxiv_pdf", "locator": "https://arxiv.org/pdf/2108.00074"},
    "pdf_murray": {"asset_path": "downloads/arxiv-2106.02147v1.pdf", "sha256": "4c7a83a9d71108c570f4cad3057c7fa51116b04eb1f0985e48a4c4e7a021ffed", "kind": "fixed_arxiv_pdf", "locator": "https://arxiv.org/pdf/2106.02147v1"},
    "pdf_gardam": {"asset_path": "downloads/arxiv-2312.05240v2.pdf", "sha256": "f9f7263a0b8d224b73861048297f40561cae1cbbde81d0afcc9b8648b45a649b", "kind": "fixed_arxiv_pdf", "locator": "https://arxiv.org/pdf/2312.05240v2"},
    "pdf_perelman1": {"asset_path": "downloads/arxiv-math_0211159.pdf", "sha256": "945e278613c45ea1ab617b28c3095783d0e68958dc0546dfcfa9b42b9674fbe1", "kind": "fixed_arxiv_pdf", "locator": "https://arxiv.org/pdf/math/0211159"},
    "pdf_perelman2": {"asset_path": "downloads/arxiv-math_0303109.pdf", "sha256": "6290421ec45e459a16a5ecad86d1162eecfed9f2c2646c7b2728f0503de8f706", "kind": "fixed_arxiv_pdf", "locator": "https://arxiv.org/pdf/math/0303109"},
    "pdf_perelman3": {"asset_path": "downloads/arxiv-math_0307245.pdf", "sha256": "460606386f35a6b719970471a94452ecea7769e8c2caeff8820b8a483aebe0c6", "kind": "fixed_arxiv_pdf", "locator": "https://arxiv.org/pdf/math/0307245"},
    "web_mo507128": {"asset_path": "reference-snapshots/web/mathoverflow.net_questions_507128_embeddability-order-on-picard-groups.html", "sha256": "921619094996d56eee7a89d4580663413deb0d8f644e6d7b5df9dfb4334817a6", "kind": "fixed_web_snapshot", "locator": "https://mathoverflow.net/questions/507128"},
    "pdf_triforce": {"asset_path": "downloads/arxiv-1903.04863.pdf", "sha256": "7f5c319425c7d351b94c5679f3de4e8834d97b54e06f92062d8b266a76671927", "kind": "fixed_arxiv_pdf", "locator": "https://arxiv.org/pdf/1903.04863"},
    "pdf_suffix": {"asset_path": "downloads/arxiv-2602.20143.pdf", "sha256": "15f6fbc4db84f0bd6b9c56942b51798e011f8e7cfe6f9777eb920e8d5bd274e3", "kind": "fixed_arxiv_pdf", "locator": "https://arxiv.org/pdf/2602.20143v2"},
    "web_mo347178": {"asset_path": "reference-snapshots/web/mathoverflow.net_questions_347178.html", "sha256": "6e8d1516673e589549634facb0957b80fe2f3f78149257fbb4c174433e4e73e6", "kind": "fixed_web_snapshot", "locator": "https://mathoverflow.net/questions/347178"},
    "pdf_pyjama": {"asset_path": "downloads/arxiv-1305.1514.pdf", "sha256": "11f7b6f0157ee39460d7d798028170ba70917b6f0ccaa3252e26d64ad69a0f8d", "kind": "fixed_arxiv_pdf", "locator": "https://arxiv.org/pdf/1305.1514"},
    "pdf_pfr": {"asset_path": "downloads/arxiv-2311.05762.pdf", "sha256": "1e3e7bfbc440f95b60202024c0d1e995e8a98dc2f5370bead60b47861d90e1b3", "kind": "fixed_arxiv_pdf", "locator": "https://arxiv.org/pdf/2311.05762"},
    "pdf_ford": {"asset_path": "downloads/arxiv-1104.3264.pdf", "sha256": "ba5678af612affd5d54f07e370df7a6c398804b55acf641379d68d10be324d50", "kind": "fixed_arxiv_pdf", "locator": "https://arxiv.org/pdf/1104.3264"},
}

FORMAL_ASSETS: dict[int, tuple[str, str, str]] = {
    6: ("006-80170.lean", "e098cb4975d59083c2e8586bf7dfa9f26c0758cd81ab8d82c7346e2209168347", "gcdCondition_iff_primePowerCondition"),
    8: ("008-GraphConjecture2.lean", "0ba2f8d543453911f18efd52ec3f6662d78e7a5502331708a00e1f0d9cc95d4c", "conjecture2"),
    9: ("009-CasasAlvero.lean", "6489ed6459ed1d5d64b5f3f77bfbfa268399d3041b033620fe08cc10f2679d96", "positive_char_counterexample"),
    14: ("014-EulerBrick.lean", "58fd6e4ce572ee09aa1825f3a91287e2cd9f4fa81027f28b7c80ab7a5c80aea6", "cuboidOne"),
    21: ("021-Main.lean", "79eff3cb6200e98ef971b8f2ef92c5b66f07ada919bf14852b14926e7d91a20d", "conjecture144"),
    22: ("022-GraphConjecture327.lean", "d888f321a3a85c41b7c1c413aed8603cb824a03a6d3078afb193ccf15396f191", "conjecture327"),
    23: ("023-GraphConjecture143.lean", "b64fbafa035c76da3ef57eb230d57e704b4ed9ab14ae67cc7848a5d2f6c174de", "conjecture143"),
    24: ("024-GraphConjecture109.lean", "96983d23efd3ad23020f79d51e8fe9037ad482b734760ff091e114629bc9f4d9", "conjecture109"),
    26: ("026-Conj63.lean", "54e9a8369d3321cd99f35b2bb95cc2e6d203ccc963d7970921b6b9043811395a", "conjecture6_3"),
    27: ("027-GraphConjecture316.lean", "d41bd5eca4bca48e5a0d6627d7a1f1ef30cb5b0ce35310550ba6e77bee0fd6e6", "conjecture316"),
    28: ("028-GraphConjecture1.lean", "e50973e15dd3d94de3d9071ad6224e2c579999f337fffc73f0f7a9c581c5e0d9", "conjecture1"),
    29: ("029-GraphConjecture58.lean", "a57d43f301e95aad244dc8e190ef7c3967fbeb528f71297e83fb227a5e3f0beb", "conjecture58"),
    31: ("031-GraphConjecture194.lean", "294aca601f0c4a1f1c207420b71b0e934c9d291874842ee7797395adb2c5ec9c", "conjecture194"),
    33: ("033-GraphConjecture315.lean", "304a24ffb13bbf2a5bf3e38a56a310443319fa871e1239be9b86b651d058a759", "conjecture315"),
    39: ("039-GraphConjecture322.lean", "f7da4cb014b0cd262c54653ed3c3ba8435c7d35f6149599de96e8b33d007d636", "conjecture322"),
    40: ("040-GraphConjecture217Audit.lean", "e13d71adc85c0cc244787b299868b07369f31ee9d854a6d4405720951af1477a", "conjecture217"),
    67: ("067-MO507128.lean", "90ef691c94610e8208496bb73c0e87c3830907939dacaa5b14373c5d35c6392d", "exists_isFractionRing_self_ideal_ne_top_invertible"),
    68: ("068-57.lean", "039debd7a522c215655a3d27265dcf95334cabcf04d22157a417db0382f38ca3", "z3_functional"),
    75: ("075-Mathoverflow347178.lean", "44fa7a97ea8bc2b42d13c42fc34fcfcded4fcd9d094b181a902550628a065840", "mathoverflow_347178"),
    79: ("079-MonochromaticQuantumGraph.lean", "d1d266c71dd9575e37ae3cb57b3a7cffcd0ad721f054d18c0a83b3f8a548af34", "eqSystem4_no_solution_d4"),
    80: ("080-MonochromaticQuantumGraph.lean", "d1d266c71dd9575e37ae3cb57b3a7cffcd0ad721f054d18c0a83b3f8a548af34", "eqSystem_no_solution_even_ge4_d_eq_n_explicit"),
}

FORMAL_LOCATORS: dict[int, str] = {
    6: "https://raw.githubusercontent.com/guodk/formal-conjectures/0720658844d76a50d48e4baa152eef14d4462907/FormalConjectures/OEIS/80170.lean",
    8: "https://raw.githubusercontent.com/google-deepmind/alphaproof-nexus-results/0647711a71183c1ea492ad60860776617ce1ea88/APNOutputs/AICollaborator/Graphs/GraphConjecture2.lean",
    9: "https://raw.githubusercontent.com/mzhorvath1/formal-conjectures/4f2343508f2c157f35abb7be4814bd550280ce81/FormalConjectures/Paper/CasasAlvero.lean",
    14: "https://raw.githubusercontent.com/google-deepmind/formal-conjectures/34c93bbad127a9a5354b9d53478d338eb65edb88/FormalConjectures/Wikipedia/EulerBrick.lean",
    21: "https://raw.githubusercontent.com/beowulf127/wowii144-lean/046429d509b28c90ee2ec38ae27c1ad377c6a5fc/WOWII144/Main.lean",
    22: "https://raw.githubusercontent.com/mo271/formal-conjectures/6e85aabe821e6ddf718d050a5bd8f19a48e4f2d9/FormalConjectures/WrittenOnTheWallII/GraphConjecture327.lean",
    23: "https://raw.githubusercontent.com/DomTheDeveloper/formal-conjectures/693e9aa206a5c6c98598aa4e6e5f3db0994a79b7/FormalConjectures/WrittenOnTheWallII/Proofs/GraphConjecture143.lean",
    24: "https://raw.githubusercontent.com/DomTheDeveloper/formal-conjectures/cf59008ef1cd432bf9803275dcf5d62ab1f094a3/FormalConjectures/WrittenOnTheWallII/GraphConjecture109.lean",
    26: "https://raw.githubusercontent.com/logical-intelligence/proofs/0dbb9215f472c532ca8af1376ed58a7ebca6dec2/LI/Conj63.lean",
    27: "https://raw.githubusercontent.com/KitaKen1/wowii-graph-conjecture-316-lean/3335e07151bc43e86d5c104dd30fee3596f06410/GraphConjecture316.lean",
    28: "https://raw.githubusercontent.com/MiskinAleksandr23/WOWII-1/eda16f6e96b313bd112351ae9859133b77d537c9/WOWII1/GraphConjecture1.lean",
    29: "https://raw.githubusercontent.com/mo271/formal-conjectures/4bd72a06842a10e1b8d7bb0fd6b1ef5e6bd20210/FormalConjectures/WrittenOnTheWallII/GraphConjecture58.lean",
    31: "https://raw.githubusercontent.com/anagnorisis2peripeteia/formal-conjectures/4bff865a14c2cd61fefbffbe9c49cbfc5a89ac45/FormalConjectures/WrittenOnTheWallII/GraphConjecture194.lean",
    33: "https://raw.githubusercontent.com/mo271/formal-conjectures/9ef80e1a3709ed3eda43d9ed6ff1087681621041/FormalConjectures/WrittenOnTheWallII/GraphConjecture315.lean",
    39: "https://raw.githubusercontent.com/SamuelSchlesinger/formal-conjectures/78f39db3ea9f5a8b2e6841e7769f538ff263dbf2/FormalConjectures/WrittenOnTheWallII/GraphConjecture322.lean",
    40: "https://raw.githubusercontent.com/KitaKen1/wowii-graph-conjecture-217-lean/6a2fb82fcd17aa15ec734736740794bb8bd194c0/lean/GraphConjecture217Audit.lean",
    67: "https://raw.githubusercontent.com/KitaKen1/mo507128-lean/e9507429c01c4288089e4af1c92a03b7d1e17f74/MO507128.lean",
    68: "https://raw.githubusercontent.com/mo271/formal-conjectures/f5afe85e1e02611f63c32ae041b33c67b7938cba/FormalConjectures/GreensOpenProblems/57.lean",
    75: "https://raw.githubusercontent.com/google-deepmind/formal-conjectures/fc20c0b55eab6fc26e2bb5b24fb3005303a0910b/FormalConjectures/Mathoverflow/347178.lean",
    79: "https://raw.githubusercontent.com/google-deepmind/formal-conjectures/af88acbf9da0f26e3e934743a819e986e02f6875/FormalConjectures/Paper/MonochromaticQuantumGraph.lean",
    80: "https://raw.githubusercontent.com/google-deepmind/formal-conjectures/af88acbf9da0f26e3e934743a819e986e02f6875/FormalConjectures/Paper/MonochromaticQuantumGraph.lean",
}

RANK_ASSETS: dict[int, list[str]] = {
    2: ["pdf_1101"], 3: ["rendering_worm_upper"], 6: ["pdf_2606"], 7: ["pdf_2007"], 8: ["pdf_2605"],
    9: ["pdf_ca"], 10: ["pdf_ca"], 11: ["pdf_stam"], 12: ["pdf_green4"],
    13: ["pdf_hs3"], 14: ["pdf_cuboid"], 15: ["pdf_complexity"],
    48: ["web_mo260589"], 53: ["pdf_kakeya3"], 54: ["pdf_lonely"],
    57: ["pdf_keevash"], 58: ["pdf_bukh_chao"], 59: ["pdf_keevash"],
    61: ["pdf_murray", "pdf_gardam"],
    65: ["pdf_perelman1", "pdf_perelman2", "pdf_perelman3"],
    67: ["web_mo507128"], 70: ["pdf_triforce"], 71: ["pdf_suffix"],
    74: ["web_mo347178"], 75: ["web_mo347178"], 78: ["pdf_pyjama"],
    81: ["pdf_pfr"], 84: ["pdf_ford"],
}


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def authority_ok(document: dict[str, Any], field: str) -> bool:
    work = dict(document)
    expected = work.pop(field)
    return expected == sha256_bytes(canonical_bytes(work))


def set_digest(values: list[Any] | set[Any]) -> str:
    return sha256_bytes(canonical_bytes(sorted(set(values))))


def fixed_references(rank: int, queue_row_sha256: str) -> list[dict[str, Any]]:
    refs: list[dict[str, Any]] = []
    doi_by_rank = {
        1: "10.1112/blms/17.4.305",
        3: "10.1007/s00454-002-0774-3",
    }
    if rank in doi_by_rank:
        doi = doi_by_rank[rank]
        refs.append({
            "role": "primary_resolution",
            "kind": "immutable_bibliographic_locator",
            "identifier_scheme": "doi",
            "identifier": doi,
            "locator": f"https://doi.org/{doi}",
            "fixed_in_source_row_sha256": queue_row_sha256,
        })
    for key in RANK_ASSETS.get(rank, []):
        asset = ASSETS[key]
        refs.append({
            "role": "primary_resolution",
            "asset_key": key,
            "kind": asset["kind"],
            "locator": asset["locator"],
            "external_snapshot_sha256": asset["sha256"],
            "artifact_path": None,
            "redistribution_status": "evidence_bytes_not_redistributed",
        })
    if rank in FORMAL_ASSETS:
        filename, digest, marker = FORMAL_ASSETS[rank]
        refs.append({
            "role": "primary_resolution_formal_check",
            "kind": "fixed_formal_proof",
            "asset_key": f"formal-{rank:03d}-{filename}",
            "locator": FORMAL_LOCATORS[rank],
            "external_snapshot_sha256": digest,
            "artifact_path": None,
            "redistribution_status": "evidence_bytes_not_redistributed",
            "target_marker": marker,
            "target_proof_sorry_free": True,
        })
    return refs


def decision_for(rank: int) -> str:
    if rank in ELIGIBLE:
        return "eligible_existing_frontier_credit"
    if rank in REJECT:
        return "reject"
    return "pending"


def reason_codes(rank: int) -> list[str]:
    if rank in ELIGIBLE:
        codes = ["all_eligibility_gates_passed", "existing_parent_identity_only"]
        if rank == 3:
            codes.append("published_strict_upper_bound_plus_exact_measure_padding")
        if rank == 14:
            codes.append("source_docstring_polarity_typo_corrected")
        if rank == 61:
            codes.append("combined_prime_and_zero_characteristic_references")
        return codes
    if rank in REJECT:
        return [REJECT_REASON[rank], "no_frontier_credit"]
    return [PENDING_REASON[rank], "manual_review_remains_open"]


def build(args: argparse.Namespace) -> tuple[Path, Path]:
    repo_root = args.repo_root.resolve()
    source_archive = (args.source_archive or (repo_root / "Docs/catalog/v5/sources/formal-conjectures-2270d31e8dd611521f979de6d86da364930b7669.tar.gz")).resolve()
    output_dir = (args.output_dir or (repo_root / "Docs/catalog/v5/curation/frontier_theorem_reviews_v5_5")).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    queue_path = repo_root / QUEUE_REL
    parent_path = repo_root / PARENT_REL
    manifest_path = repo_root / MANIFEST_REL
    assert sha256_file(queue_path) == EXPECTED_QUEUE_FILE_SHA256
    assert sha256_file(parent_path) == EXPECTED_PARENT_SHA256
    assert sha256_file(manifest_path) == EXPECTED_MANIFEST_SHA256
    assert sha256_file(source_archive) == EXPECTED_SOURCE_ARCHIVE_SHA256

    queue = json.loads(queue_path.read_text(encoding="utf-8"))
    parent = json.loads(parent_path.read_text(encoding="utf-8"))
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert queue["authority_sha256"] == EXPECTED_QUEUE_AUTHORITY_SHA256
    assert authority_ok(queue, "authority_sha256")
    assert manifest["release_root_sha256"] == EXPECTED_RELEASE_ROOT_SHA256
    assert queue["inputs"]["parent_catalog_sha256"] == EXPECTED_PARENT_SHA256
    assert queue["inputs"]["parent_manifest_sha256"] == EXPECTED_MANIFEST_SHA256
    assert queue["inputs"]["formal_conjectures_commit"] == SOURCE_COMMIT
    with tarfile.open(source_archive, "r:gz") as archive:
        regular = [m for m in archive.getmembers() if m.isfile()]
        source_members = {}
        license_bytes = None
        for member_info in regular:
            member_file = archive.extractfile(member_info)
            assert member_file is not None
            data = member_file.read()
            parts = Path(member_info.name).parts
            relative = Path(*parts[1:]).as_posix() if len(parts) > 1 else parts[0]
            source_members[relative] = data
            if relative == "LICENSE":
                license_bytes = data
        assert license_bytes is not None
        assert sha256_bytes(license_bytes) == EXPECTED_LICENSE_SHA256

    selected = queue["records"][:85]
    assert [row["candidate_rank"] for row in selected] == list(range(1, 86))
    assert len(FINDINGS) == 85 and set(FINDINGS) == set(range(1, 86))
    assert len(ELIGIBLE) == 41 and len(PENDING) == 32 and len(REJECT) == 12

    batch_semantic_counts = Counter(row["semantic_key"] for row in selected)
    parent_by_normalized: dict[str, list[dict[str, Any]]] = {}
    for parent_row in parent["records"]:
        normalized = parent_row.get("dedupe", {}).get("normalized_statement_sha256")
        if normalized:
            parent_by_normalized.setdefault(normalized, []).append(parent_row)

    # The human review used byte-pinned external snapshots.  Their hashes and
    # immutable locators are retained, but third-party full text is not copied.
    used_assets_by_key: dict[str, dict[str, Any]] = {}
    for rank in sorted(set(RANK_ASSETS) | set(FORMAL_ASSETS)):
        for ref in fixed_references(rank, "placeholder"):
            if "asset_key" not in ref:
                continue
            assert len(ref["external_snapshot_sha256"]) == 64
            assert ref["locator"].startswith("https://")
            inventory_entry = {
                "asset_key": ref["asset_key"],
                "kind": ref["kind"],
                "locator": ref["locator"],
                "external_snapshot_sha256": ref["external_snapshot_sha256"],
                "artifact_path": None,
                "redistribution_status": "evidence_bytes_not_redistributed",
            }
            previous = used_assets_by_key.setdefault(ref["asset_key"], inventory_entry)
            assert previous == inventory_entry

    rows: list[dict[str, Any]] = []
    for queue_row in selected:
        rank = queue_row["candidate_rank"]
        queue_core = dict(queue_row)
        source_row_sha256 = queue_core.pop("row_sha256")
        assert sha256_bytes(canonical_bytes(queue_core)) == source_row_sha256

        loc = queue_row["source_locator"]
        member_bytes = source_members[loc["member_path"]]
        assert sha256_bytes(member_bytes) == loc["file_sha256"]
        source_slice = member_bytes[loc["byte_start"]:loc["byte_end_exclusive"]]
        assert sha256_bytes(source_slice) == loc["raw_block_sha256"]
        assert loc["revision"] == SOURCE_COMMIT

        normalized = queue_row["semantic_key"].split("/", 1)[1]
        parent_matches = parent_by_normalized.get(normalized, [])
        assert len(parent_matches) == 1
        assert batch_semantic_counts[queue_row["semantic_key"]] == 1
        parent_row = parent_matches[0]
        assert parent_row["variant_id"] == queue_row["variant_id"]
        assert parent_row["stage_claim_id"] == queue_row["stage_claim_id"]

        decision = decision_for(rank)
        refs = fixed_references(rank, source_row_sha256)
        scope_verified = rank in ELIGIBLE or rank in REJECT - {69}
        proved_verified = rank in ELIGIBLE or rank in REJECT - {69}
        frontier_documented = rank not in NONFRONTIER_REJECTS and rank not in {77, 82}
        gates = {
            "complete_proved_theorem_statement": True,
            "primary_resolution_reference_fixed": bool(refs),
            "scope_matches_reference": scope_verified,
            "documented_open_problem_or_frontier_main_result": frontier_documented,
            "proved_status_verified_as_of_2026_08_10": proved_verified,
            "rights_review_complete_for_existing_credit": True,
            "semantic_dedupe_complete": True,
            "semantic_dedupe_passed": rank not in CONCEPTUAL_DUPLICATES,
        }
        if decision == "eligible_existing_frontier_credit":
            assert all(gates.values()) and refs

        if rank in ELIGIBLE:
            scope_finding = "Verified against the fixed primary resolution: " + FINDINGS[rank]
            frontier_finding = "A documented research problem resolution or significant frontier main result; existing-parent credit is warranted."
            status_finding = "Proved status independently verified as of 2026-08-10."
        elif rank in PENDING:
            scope_finding = "Not yet fully verified: " + FINDINGS[rank]
            frontier_finding = "Potential frontier/open-problem item, but no credit is granted while a required gate remains open."
            status_finding = "Proved status is not independently closed for this exact statement and fixed evidence set."
        else:
            scope_finding = FINDINGS[rank]
            frontier_finding = ("The mathematical resolution is already represented by the selected broader/same resolution."
                                if rank in CONCEPTUAL_DUPLICATES else
                                "The row fails the importance/frontier or scope policy and receives no frontier credit.")
            status_finding = ("Truth/resolution status is verified, but that does not overcome the rejection gate."
                              if rank != 69 else
                              "The claimed disproof does not verify the classical characteristic-zero Jacobian conjecture.")

        row: dict[str, Any] = {
            "schema_version": SCHEMA,
            "review_as_of": REVIEW_AS_OF,
            "review_batch": BATCH,
            "review_index": rank - 1,
            "candidate_rank": rank,
            "stage_claim_id": queue_row["stage_claim_id"],
            "variant_id": queue_row["variant_id"],
            "family_id": queue_row["family_id"],
            "semantic_key": queue_row["semantic_key"],
            "display_name": queue_row["display_name"],
            "source_row_sha256": source_row_sha256,
            "source_slice_binding": {
                "source_commit": SOURCE_COMMIT,
                "source_archive_sha256": EXPECTED_SOURCE_ARCHIVE_SHA256,
                "member_path": loc["member_path"],
                "file_sha256": loc["file_sha256"],
                "byte_start": loc["byte_start"],
                "byte_end_exclusive": loc["byte_end_exclusive"],
                "raw_block_sha256": loc["raw_block_sha256"],
            },
            "parent_binding": {
                "parent_release": "5.4",
                "parent_catalog_sha256": EXPECTED_PARENT_SHA256,
                "parent_variant_id": parent_row["variant_id"],
                "parent_stage_claim_id": parent_row["stage_claim_id"],
                "parent_record_canonical_sha256": sha256_bytes(canonical_bytes(parent_row)),
                "exact_parent_occurrences": len(parent_matches),
            },
            "decision": decision,
            "grants_frontier_credit": rank in ELIGIBLE,
            "grants_new_theorem_credit": False,
            "gates": gates,
            "primary_resolution_references": refs,
            "scope_finding": scope_finding,
            "frontier_finding": frontier_finding,
            "status_finding": status_finding,
            "rights_finding": (
                "Existing-parent identity audit only. Apache-2.0 covers the pinned Formal Conjectures code; "
                "source-specific docstring terms remain preserved and not independently cleared. No permission "
                "to republish external proof text is inferred."
            ),
            "dedupe_finding": {
                "exact_parent_occurrences": len(parent_matches),
                "exact_batch_occurrences": batch_semantic_counts[queue_row["semantic_key"]],
                "conceptual_duplicate_of_candidate_rank": CONCEPTUAL_DUPLICATES.get(rank),
                "distinct_for_frontier_credit": rank not in CONCEPTUAL_DUPLICATES,
            },
            "reason_codes": reason_codes(rank),
        }
        row["review_row_sha256"] = sha256_bytes(canonical_bytes(row))
        rows.append(row)

    jsonl_path = output_dir / "nonerdos_001_085.jsonl"
    jsonl_bytes = b"".join(canonical_bytes(row) + b"\n" for row in rows)
    jsonl_path.write_bytes(jsonl_bytes)

    decisions = Counter(row["decision"] for row in rows)
    used_assets = [used_assets_by_key[key] for key in sorted(used_assets_by_key)]
    receipt: dict[str, Any] = {
        "schema_version": RECEIPT_SCHEMA,
        "review_as_of": REVIEW_AS_OF,
        "review_batch": BATCH,
        "scope": "candidate_rank 1-85; non-Erdos existing-parent frontier-credit review only",
        "credit_policy": {
            "automatic_credit": False,
            "eligible_decision": "eligible_existing_frontier_credit",
            "all_grants_new_theorem_credit": False,
            "release_or_queue_modified": False,
            "external_proof_republication_authorized": False,
        },
        "inputs": {
            "queue_path": QUEUE_REL.as_posix(),
            "queue_file_sha256": EXPECTED_QUEUE_FILE_SHA256,
            "queue_authority_sha256": EXPECTED_QUEUE_AUTHORITY_SHA256,
            "parent_catalog_path": PARENT_REL.as_posix(),
            "parent_catalog_sha256": EXPECTED_PARENT_SHA256,
            "parent_manifest_path": MANIFEST_REL.as_posix(),
            "parent_manifest_sha256": EXPECTED_MANIFEST_SHA256,
            "parent_release_root_sha256": EXPECTED_RELEASE_ROOT_SHA256,
            "formal_conjectures_commit": SOURCE_COMMIT,
            "source_archive_path": source_archive.relative_to(repo_root).as_posix(),
            "source_archive_sha256": EXPECTED_SOURCE_ARCHIVE_SHA256,
            "source_license_sha256": EXPECTED_LICENSE_SHA256,
            "source_docstring_terms": "source-specific terms preserved; not independently cleared",
            "fixed_evidence_assets": used_assets,
            "fixed_evidence_asset_set_sha256": set_digest([
                f"{x['asset_key']}:{x['external_snapshot_sha256']}:{x['locator']}"
                for x in used_assets
            ]),
            "external_evidence_bytes_redistributed": False,
        },
        "candidate_range": {
            "candidate_rank_first": 1,
            "candidate_rank_last": 85,
            "review_index_first": 0,
            "review_index_last": 84,
        },
        "counts": {
            "review_rows": len(rows),
            "eligible_existing_frontier_credit": decisions["eligible_existing_frontier_credit"],
            "pending": decisions["pending"],
            "reject": decisions["reject"],
            "grants_frontier_credit": sum(row["grants_frontier_credit"] for row in rows),
            "grants_new_theorem_credit": sum(row["grants_new_theorem_credit"] for row in rows),
        },
        "output": {
            "jsonl_file": jsonl_path.name,
            "jsonl_sha256": sha256_bytes(jsonl_bytes),
            "review_row_sha256_set_sha256": set_digest([row["review_row_sha256"] for row in rows]),
            "candidate_rank_set_sha256": set_digest([row["candidate_rank"] for row in rows]),
            "stage_claim_id_set_sha256": set_digest([row["stage_claim_id"] for row in rows]),
            "variant_id_set_sha256": set_digest([row["variant_id"] for row in rows]),
            "semantic_key_set_sha256": set_digest([row["semantic_key"] for row in rows]),
            "eligible_variant_id_set_sha256": set_digest([row["variant_id"] for row in rows if row["grants_frontier_credit"]]),
            "eligible_semantic_key_set_sha256": set_digest([row["semantic_key"] for row in rows if row["grants_frontier_credit"]]),
            "decision_vector_sha256": sha256_bytes(canonical_bytes([[row["candidate_rank"], row["decision"]] for row in rows])),
        },
    }
    receipt["receipt_authority_sha256"] = sha256_bytes(canonical_bytes(receipt))
    receipt_path = output_dir / "nonerdos_001_085_summary.json"
    receipt_path.write_bytes(json.dumps(receipt, sort_keys=True, indent=2, ensure_ascii=False).encode("utf-8") + b"\n")
    return jsonl_path, receipt_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[4])
    parser.add_argument("--source-archive", type=Path, default=None)
    parser.add_argument("--output-dir", type=Path, default=None)
    return parser.parse_args()


if __name__ == "__main__":
    jsonl, receipt = build(parse_args())
    print(json.dumps({"jsonl": str(jsonl), "receipt": str(receipt)}, sort_keys=True))
