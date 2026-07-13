#!/usr/bin/env python3
"""Fail-closed narrow validator for S56-M-0079-VALIDATION."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import platform
import re
import shutil
import subprocess
import tempfile
import time
from datetime import datetime


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0079"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM = "S56-M-0079-VALIDATION"
THEOREM = "THM-M-0079"
BASE_REVISION = "db6914155f1f63e835364b89ba0a3b25f1d7f936"
BASE_TREE = "a5488edccb2687c4ff0bbdccf4650e06b2e45337"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MATHLIB_REMOTE = "https://github.com/leanprover-community/mathlib4.git"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
EXPRESSION_SHA256 = "bb109f77dcbd6884a4ac90b32230cc213c08f19df6bc797ad04afac1a10da553"
DENOMINATOR_SHA256 = "88cf0ea4157fed371957616088fbbbbc9c0662d6d49d2ee1c502007b88956b92"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
EXPECTED_AXIOM_LIST = ["propext", "Classical.choice", "Quot.sound"]
EXPECTED_STDOUT_SHA256 = "81e0cb536a74a89c826f176e774c76f39b8f08cc0162b5edbdb46cf89cf69b7e"
EXPECTED_INPUTS = {
    "Statement.lean": "fdacf7f7c9a39400ce02e8d82e3ed2a3a66e33dcd57b553d9e01a1dd991878c5",
    "ObligationTree.lean": "67cf6edf67bf78970ad93629e53a05a6dcdf7423673c8392e213dcfddcbb81ca",
    "Proof.lean": "5ec32afd473175bf75df5a7b3813404ebee4fe92a783a0bbc39f58f9139ce839",
    "Validation.lean": "6fa8f8e91b7f6385b0f90179cf5079758e761ac465307e3432dc37caf0cc98a1",
    "proof-receipt.json": "6dc3b9e75c9532c375aab56361cb810b42b5688f7a615dae92090727fa7fff0e",
    "statement.json": "dc566c3a0da138501affdb072806ae4883a8f4f2abe351d1e0c950cd6b2984b8",
    "obligation-registry.json": "e15531a3ad569a83ee1ca6001903f1db5ccbc4f22d9fb71258965199e520824f",
    "typed-graphs.json": "25b9ebdbd4a909564857697caf4e683df2513936943d04bbfb475aa721bdc6f7",
    "validation-specs.json": "c34e49bc915733d7b33801effb558d8e9ea6de6a618a69c1458a09bc908708a5",
    "anchor-audit.json": "cf6d7f49db34f016ae61cac943c97e8581387b0e48f641c9774ec5af2c94f4ca",
}
EXPECTED_TOOL_INPUTS = {
    "lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
EXPECTED_VALIDATION_SPEC_SHA256 = "7a9693b0efa946981947aeef5e73559c5602ea7d909ece4e7e76cc02ffe53038"
SOURCE_BOUNDARY = {
    "Mathlib/GroupTheory/FreeGroup/NielsenSchreier.lean": (
        "08cc647c220b852784860c281f06a6ede45bb06f",
        "e777c40c3902fd54747eac57d2952b985aff464e5d6bf803c5c78037e4c0c847",
        "90500598b632ccdc30297fd2224a8c815e88abd1bf7ddb38041a4b3e32215582",
    ),
    "Mathlib/CategoryTheory/Action.lean": (
        "8d5284a82d52a4a24ac08671335274e2ce4d3858",
        "9a3ccec0f4a02143b425d7563061b7b066c71f4418c84ccad22f54bd4eda8cdd",
        "84aed037e49ad8cd840061fd52aa46c195379698ddd9574694755d5f4ef7f17c",
    ),
    "Mathlib/GroupTheory/FreeGroup/IsFreeGroup.lean": (
        "5ab9713d88aa95d139aa50936f447352006c95fa",
        "b5d6c1ae4fbeb1c2a5256d16d652a43f1615e4c945e03dcbf99f0cbb12558905",
        "80f4fd8299ab73e4d966537926061285f1b0b25c712ceb964a4a578ebbd50d96",
    ),
    "Mathlib/GroupTheory/GroupAction/Quotient.lean": (
        "ebdc6fb14b39ed8a8422eb6354ad636314bd7ed1",
        "50fc92cfeb4c8df97539ecbe4e6153518bea82afe6da61d531f92a9c0170ebb0",
        "75199007c28fbf6e2840d782274c70f635fbeebae53ec6d8c6bbe1546ea4efe6",
    ),
    "Mathlib/Combinatorics/Quiver/Arborescence.lean": (
        "233ee59ef5cca222270e3f722a09e85eb0960d32",
        "4653df221c528c1ab125af7d56407d7186ca6fff6fefdff7c81cf7d9e1d68a25",
        "9ae91f587565daed60aab756a574cfa395d1175b9e2a2c4a0b64d586047fe24e",
    ),
    "Mathlib/Combinatorics/Quiver/ConnectedComponent.lean": (
        "487b77e3ca3e42ba4469e12dd21280a7eecaa0e7",
        "f659393134bb9370a0692d899585ff28241ec1decf90c4de13c4f84dc5b5a675",
        "e8f3d7ea672898f5b2bb290e0a25088c9ecfcc5ed2b4ca53090528abce7da5e2",
    ),
    "Mathlib/CategoryTheory/IsConnected.lean": (
        "202947653f27408a5e7c0c74ae25ca354dcb2d31",
        "9cd7e32c52bb853f8cf7eb7e917fb7c7d01428b49662631f6726dd976ca51d27",
        "f4a7c8c7be35e4729b459c4714e91648b0c203685f5df8ab65e0cf05ef36bf07",
    ),
}
COVERED_IDS = [
    "M0079-ROOT",
    "M0079-L-QUOTIENT-PRETRANSITIVE",
    "M0079-C-QUOTIENT-NONEMPTY",
    "M0079-C-ACTION-CONNECTED",
    "M0079-C-ACTION-GROUPOID-FREE",
    "M0079-L-CONNECTED-END-FREE",
    "M0079-N-QUOTIENT-END-FREE",
    "M0079-C-STABILIZER-END",
    "M0079-L-QUOTIENT-STABILIZER",
    "M0079-C-END-SUBGROUP-EQUIV",
    "M0079-T-MULEQUIV-FREENESS",
    "M0079-T-ASSEMBLE",
]
PROOF_DECLARATIONS = (
    "quotientActionPretransitive",
    "quotientNonempty",
    "actionGroupoidFreeConstructor",
    "connectedFreeEndConstructor",
    "stabilizerEndConstructor",
    "quotientStabilizerIdentification",
    "mulEquivFreenessTransport",
    "quotientActionConnected",
    "endSubgroupEquivConstructor",
    "quotientVertexEndFree",
    "exactAssembly",
    "nielsenSchreier_via_frozen_composition",
    "nielsenSchreier_direct",
)
COMPOSITION_DECLARATIONS = (
    "quotientActionConnected_of_components",
    "endSubgroupEquiv_of_components",
    "quotientVertexEndFree_of_components",
    "exactAssembly_of_end_packages",
    "root_of_exactAssembly",
)
UNVERIFIED_CERTIFICATES = [
    "M0079-CERT-C-ACTION-GROUPOID-FREE",
    "M0079-CERT-C-ROOTED-CONNECTED",
    "M0079-CERT-C-GEODESIC-TREE",
    "M0079-CERT-L-GEODESIC-ARBORESCENCE",
    "M0079-CERT-C-TREE-LOOPS",
    "M0079-CERT-L-TREE-EDGE-IDENTITY",
    "M0079-CERT-C-FUNCTOR-END-HOM",
    "M0079-CERT-L-SPANNING-END-FREE",
    "M0079-CERT-L-CONNECTED-END-FREE",
]
TERMINAL_BODY_SHA256 = "1ab685e13340e3ee539c977dcd78b5f83b2cf8614feb23e5efef6b918cf6557d"
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/Validation.lean",
    f"Stage1_Instances/{THEOREM}/check_validation.py",
    f"Stage1_Instances/{THEOREM}/validation-phase.md",
    f"Stage1_Instances/{THEOREM}/validation-receipt.json",
    f"Stage1_Instances/{THEOREM}/validation-spec.json",
}
SUMMARY_LINES = (
    "PASS THM-M-0079 narrow validation",
    "PASS kernel replay: exact statement, five frozen compositions, thirteen proof declarations, two proof roots, pinned terminal, and differential adapter elaborated",
    "PASS trust observation: checked declarations depend only on propext, Classical.choice, and Quot.sound",
    "PASS selected provenance: frozen hashes, seven source/blob/olean boundaries, clean mathlib pin, remote, license, and tool identities agree",
    "PASS hygiene: Lean assert_no_sorry plus a supplemental prohibited-construct scan passed",
    "FAIL CLOSED authority: proof master acceptance and structured state reconciliation are pending; accepted root remains H1/M3/R4",
    "FAIL CLOSED trust: M0079-S-FOUNDATION, nine internal composition harnesses, and complete transitive provenance/TCB/SBOM closure remain open",
    "FAIL CLOSED hermetic/independent: shared warm .lake and same-worker adapter are neither cold offline replay nor distinct signed verification",
    "audit_complete=false; theorem_complete=false",
)
VALIDATION_STARTED = time.monotonic()
RECIPE_TIMEOUT_SECONDS = 180.0


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict), path
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(argv: list[str], *, cwd: Path = ROOT, env: dict[str, str] | None = None) -> str:
    remaining = RECIPE_TIMEOUT_SECONDS - (time.monotonic() - VALIDATION_STARTED)
    if remaining <= 0:
        raise TimeoutError("validation recipe exceeded its 180-second wall-clock bound")
    result = subprocess.run(
        argv,
        cwd=cwd,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=remaining,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(f"command failed ({result.returncode}): {argv!r}\n{result.stdout}")
    return result.stdout


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["git", *args], cwd=cwd).strip()


def code_without_comments(source: str) -> str:
    source = re.sub(r"/-.*?-/", "", source, flags=re.DOTALL)
    return re.sub(r"--.*$", "", source, flags=re.MULTILINE)


def printed_axioms(output: str, declaration: str) -> set[str]:
    pattern = re.compile(
        rf"'[^'\n]*{re.escape(declaration)}' depends on axioms:\s*\[([^]]+)]",
        re.DOTALL,
    )
    match = pattern.search(output)
    if match is None:
        no_axioms = re.search(
            rf"'[^'\n]*{re.escape(declaration)}' does not depend on any axioms",
            output,
        )
        assert no_axioms is not None, declaration
        return set()
    return {part.strip() for part in match.group(1).split(",") if part.strip()}


def assert_text_hygiene(path: Path) -> None:
    data = path.read_bytes()
    assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())


def main() -> None:
    spec = load(HERE / "validation-spec.json")
    receipt = load(HERE / "validation-receipt.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    manifest = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    instance = load(HERE / "instance.json")
    local_dag = load(HERE / "task-dag.json")
    statement = load(HERE / "statement.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    proof_receipt = load(HERE / "proof-receipt.json")
    frozen_specs = load(HERE / "validation-specs.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    target = next(row for row in manifest["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 1105 and target["baseline"] == "L0"
    assert target["lifecycle_mode"] == "planned"
    assert target["rework_required"] is True and target["theorem_complete"] is False
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item == {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 1105,
        "phase": "validation",
        "layer": 5,
        "state": "[ ]",
        "depends_on": ["S56-M-0079-PROOF"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Run hermetic kernel, trust, provenance, and independent validation gates.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }
    predecessor = next(row for row in execution["items"] if row["id"] == "S56-M-0079-PROOF")
    assert predecessor["state"] == "[_]"
    local_task = next(row for row in local_dag["tasks"] if row["id"] == ITEM)
    assert local_task["state"] == "open"
    assert local_task["depends_on"] == ["S56-M-0079-PROOF"]

    assert instance["root_vector"] == {"H": "H1", "M": "M3", "R": "R4"}
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == []
    assert instance["audit_complete"] is instance["theorem_complete"] is False
    closure = graphs["closure_boundary"]
    assert closure["accepted_closed_obligations"] == []
    assert closure["root_closed"] is False and closure["root_machine_classification"] == "M3"
    assert closure["audit_complete"] is closure["theorem_complete"] is False

    for name, expected in EXPECTED_INPUTS.items():
        assert sha256(HERE / name) == expected, f"stale validation input: {name}"
    for name, expected in EXPECTED_TOOL_INPUTS.items():
        assert sha256(LEAN_ROOT / name) == expected, f"changed tool input: {name}"
    assert sha256(HERE / "validation-spec.json") == EXPECTED_VALIDATION_SPEC_SHA256
    formal = statement["canonical_formal_target"]
    assert formal["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert formal["statement_file_sha256"] == EXPECTED_INPUTS["Statement.lean"]
    assert registry["frozen_against_statement_sha256"] == EXPECTED_INPUTS["Statement.lean"]
    assert registry["frozen_against_anchor_audit_sha256"] == EXPECTED_INPUTS["anchor-audit.json"]
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert proof_receipt["canonical_target_expression_sha256"] == EXPRESSION_SHA256
    assert proof_receipt["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert proof_receipt["proof_body"]["source_sha256"] == EXPECTED_INPUTS["Proof.lean"]
    assert proof_receipt["root_evidence"]["root_kernel_declaration_closed"] is True
    assert proof_receipt["root_evidence"]["accepted_root_closed"] is False
    assert proof_receipt["root_evidence"]["exact_declaration_evidence_ids"] == COVERED_IDS
    assert proof_receipt["root_evidence"]["unverified_internal_composition_certificate_ids"] == (
        UNVERIFIED_CERTIFICATES
    )
    assert proof_receipt["accepted_closed_obligation_ids"] == []
    assert proof_receipt["result"]["axioms"] == EXPECTED_AXIOM_LIST
    assert proof_receipt["accepted"] is False

    assert frozen_specs["item_id"] == "S56-M-0079-OBLIGATION_TREE"
    assert all(row["closure_credit"] is False for row in frozen_specs["recipes"])
    assert any(
        any(arg.endswith("check_obligation_tree.py") for arg in row["argv"])
        for row in frozen_specs["recipes"]
    )
    assert any(
        any(arg.endswith("build_obligation_artifacts.py") for arg in row["argv"])
        for row in frozen_specs["recipes"]
    )

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by|extern)\b|"
        r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
        r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
        r"(?:axiom|constant|opaque|unsafe)\b",
        re.MULTILINE,
    )
    for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
        source = code_without_comments((HERE / name).read_text(encoding="utf-8"))
        assert prohibited.search(source) is None, f"prohibited source token in {name}"
    differential = code_without_comments((HERE / "Validation.lean").read_text(encoding="utf-8"))
    for forbidden in (
        "import Proof",
        "import ObligationTree",
        "Proof.",
        "nielsenSchreier_direct",
        "nielsenSchreier_via_frozen_composition",
    ):
        assert forbidden not in differential, forbidden
    assert "MulAction.isPretransitive_quotient G H" in differential
    assert "IsFreeGroupoid.endIsFreeOfConnectedFree" in differential
    assert "endMulEquivSubgroup H" in differential
    assert "assert_no_sorry independentlyReconstructedTarget" in differential

    manifest_record = load(LEAN_ROOT / "lake-manifest.json")
    mathlib_entry = next(row for row in manifest_record["packages"] if row["name"] == "mathlib")
    assert mathlib_entry["rev"] == mathlib_entry["inputRev"] == MATHLIB_REVISION
    assert MATHLIB.is_dir(), "pinned mathlib artifacts are unavailable"
    assert git("rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert git("status", "--porcelain=v1", cwd=MATHLIB) == ""
    assert git("remote", "get-url", "origin", cwd=MATHLIB) == MATHLIB_REMOTE
    assert sha256(MATHLIB / "LICENSE") == (
        "b40930bbcf80744c86c46a12bc9da056641d722716c378f5659b9e555ef833e1"
    )
    for source_name, (blob_hash, source_hash, olean_hash) in SOURCE_BOUNDARY.items():
        assert git("rev-parse", f"HEAD:{source_name}", cwd=MATHLIB) == blob_hash
        assert sha256(MATHLIB / source_name) == source_hash, source_name
        olean_name = source_name.removesuffix(".lean") + ".olean"
        olean = MATHLIB / ".lake" / "build" / "lib" / "lean" / olean_name
        assert sha256(olean) == olean_hash

    lean = run(["lake", "env", "which", "lean"], cwd=LEAN_ROOT).strip()
    lake = run(["lake", "env", "which", "lake"], cwd=LEAN_ROOT).strip()
    lean_path = run(["lake", "env", "printenv", "LEAN_PATH"], cwd=LEAN_ROOT).strip()
    python = Path(os.path.realpath(os.sys.executable))
    git_path = shutil.which("git")
    assert git_path is not None
    git_executable = Path(os.path.realpath(git_path))
    assert LEAN_COMMIT in run([lean, "--version"])
    assert "5.0.0-src+98dc76e" in run([lake, "--version"])
    assert sha256(Path(lean)) == (
        "3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf"
    )
    assert sha256(Path(lake)) == (
        "a608ff084d7e2af228b92a29d7c2fd083ba0580e46889175ec74a81678c98359"
    )
    assert sha256(python) == (
        "b8d8288faefdd300201f43fcf00f6f539a27218eeed3a3dff5ab10b9c4c99700"
    )
    assert sha256(git_executable) == (
        "8a48eefa306b9a2a9c3e576784a74ad7485779279e5a46ec43361a1864760e45"
    )

    with tempfile.TemporaryDirectory(prefix="m0079-validation-") as tmp_name:
        tmp = Path(tmp_name)
        for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
            (tmp / name).write_bytes((HERE / name).read_bytes())
        base_env = {
            "HOME": os.environ.get("HOME", ""),
            "PATH": os.environ.get("PATH", ""),
            "LANG": "C.UTF-8",
            "LC_ALL": "C.UTF-8",
            "TZ": "UTC",
            "LEAN_PATH": lean_path,
        }
        run([lean, "-t", "0", "-o", "Statement.olean", "Statement.lean"], cwd=tmp, env=base_env)
        module_env = dict(base_env)
        module_env["LEAN_PATH"] = f"{tmp}:{lean_path}"
        obligation_output = run(
            [lean, "-t", "0", "-o", "ObligationTree.olean", "ObligationTree.lean"],
            cwd=tmp,
            env=module_env,
        )
        proof_output = run([lean, "-t", "0", "Proof.lean"], cwd=tmp, env=module_env)
        validation_output = run([lean, "-t", "0", "Validation.lean"], cwd=tmp, env=module_env)

    for declaration in COMPOSITION_DECLARATIONS:
        assert printed_axioms(obligation_output, declaration) <= EXPECTED_AXIOMS
    assert printed_axioms(proof_output, "subgroupIsFreeOfIsFree") == EXPECTED_AXIOMS
    for declaration in PROOF_DECLARATIONS:
        assert printed_axioms(proof_output, declaration) == EXPECTED_AXIOMS
    assert printed_axioms(validation_output, "subgroupIsFreeOfIsFree") == EXPECTED_AXIOMS
    assert printed_axioms(validation_output, "independentlyReconstructedTarget") == EXPECTED_AXIOMS
    assert proof_output.count("Declarations are sorry-free!") == len(PROOF_DECLARATIONS) + 1
    assert validation_output.count("Declarations are sorry-free!") == 2
    assert "sorryAx" not in obligation_output + proof_output + validation_output

    assert spec["schema_version"] == "stage1-validation-recipe/1.0"
    assert spec["item_id"] == ITEM and spec["theorem_id"] == THEOREM
    assert spec["cwd"] == "."
    assert spec["argv"] == ["python3", "-B", f"Stage1_Instances/{THEOREM}/check_validation.py"]
    assert spec["env_allowlist"] == {} and spec["timeout_seconds"] == 180
    assert spec["network_policy"] == "denied" and spec["expected_exit"] == 0
    assert "cannot provision a kernel network namespace" in spec["network_enforcement"]
    assert spec["covered_obligation_ids"] == COVERED_IDS
    assert spec["expected_outputs"] == [{
        "path_or_stream": "stdout",
        "semantic_hash_policy": "exact nine-line PASS/FAIL-CLOSED status summary",
    }]
    assert spec["covered_declarations"] == [
        "Stage1Instances.THM_M_0079.NielsenSchreierTarget",
        *(f"Stage1Instances.THM_M_0079.ObligationTree.{name}" for name in COMPOSITION_DECLARATIONS),
        *(f"Stage1Instances.THM_M_0079.Proof.{name}" for name in PROOF_DECLARATIONS),
        "subgroupIsFreeOfIsFree",
        "Stage1Instances.THM_M_0079.Validation.independentlyReconstructedTarget",
    ]

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["phase"] == "validation" and receipt["intent"] == "validate"
    assert receipt["depends_on"] == ["S56-M-0079-PROOF"]
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    started_at = datetime.fromisoformat(receipt["started_at"])
    ended_at = datetime.fromisoformat(receipt["ended_at"])
    validated_at = datetime.fromisoformat(receipt["validated_at"])
    assert started_at.tzinfo is not None and ended_at.tzinfo is not None
    assert started_at <= ended_at == validated_at
    attested_inputs = [
        HERE / name
        for name in (*EXPECTED_INPUTS, "validation-spec.json", "check_validation.py")
    ]
    assert all(
        datetime.fromtimestamp(path.stat().st_mtime, started_at.tzinfo) <= started_at
        for path in attested_inputs
    )
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["release_grade"] is receipt["content_addressed_release_evidence"] is False
    assert receipt["covered_obligation_ids"] == spec["covered_obligation_ids"] == COVERED_IDS
    for name, expected in EXPECTED_INPUTS.items():
        assert receipt["inputs"][name] == expected, name
    assert receipt["inputs"]["validation-spec.json"] == EXPECTED_VALIDATION_SPEC_SHA256
    assert receipt["inputs"]["check_validation.py"] == sha256(HERE / "check_validation.py")
    assert receipt["target"]["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert receipt["target"]["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert receipt["environment"]["platform"] == (
        f"{platform.system()} {platform.release()} {platform.machine()}"
    )
    assert receipt["environment"]["lean_executable_sha256"] == sha256(Path(lean))
    assert receipt["environment"]["lake_executable_sha256"] == sha256(Path(lake))
    assert receipt["environment"]["python_executable_sha256"] == sha256(python)
    assert receipt["environment"]["git_executable_sha256"] == sha256(git_executable)
    assert receipt["environment"]["mathlib_revision"] == MATHLIB_REVISION
    assert receipt["environment"]["mathlib_tree"] == MATHLIB_TREE
    provenance = receipt["provenance"]
    origin = provenance["origin"]
    owning_source = "Mathlib/GroupTheory/FreeGroup/NielsenSchreier.lean"
    assert provenance["terminal_declaration"] == "subgroupIsFreeOfIsFree"
    assert provenance["terminal_proof_body_id"] == f"sha256:{TERMINAL_BODY_SHA256}"
    assert origin["remote"] == MATHLIB_REMOTE
    assert origin["revision"] == MATHLIB_REVISION and origin["tree_hash"] == MATHLIB_TREE
    assert origin["file"] == owning_source
    assert [origin["source_blob"], origin["source_sha256"], origin["olean_sha256"]] == list(
        SOURCE_BOUNDARY[owning_source]
    )
    source_lines = (MATHLIB / owning_source).read_bytes().splitlines(keepends=True)
    assert hashlib.sha256(b"".join(source_lines[312:316])).hexdigest() == TERMINAL_BODY_SHA256
    assert provenance["selected_source_blob_olean_triples"] == {
        name: list(values) for name, values in SOURCE_BOUNDARY.items() if name != owning_source
    }
    assert provenance["license_sha256"] == sha256(MATHLIB / "LICENSE")
    assert receipt["recipe"] == {
        key: spec[key]
        for key in (
            "recipe_id",
            "cwd",
            "argv",
            "env_allowlist",
            "timeout_seconds",
            "network_policy",
            "expected_exit",
            "expected_outputs",
            "covered_obligation_ids",
            "covered_declarations",
        )
    }
    result = receipt["result"]
    assert result["axioms"] == EXPECTED_AXIOM_LIST
    assert result["kernel_replay"] == "provisional_pass"
    assert result["placeholder_and_unsafe_scan"] == "pass"
    assert result["selected_provenance"] == "pass"
    assert result["foundation_and_complete_trust_closure"] == "fail_closed"
    assert result["proof_master_acceptance"] == "fail_closed"
    assert result["internal_source_composition_harnesses"] == "fail_closed_nine_open"
    assert result["accepted_root_closed"] is False
    assert result["hermetic_cold_offline_replay"] == "fail_closed"
    assert result["independent_distinct_runner"] == "fail_closed"
    assert result["audit_complete"] is result["theorem_complete"] is False
    expected_stdout = "\n".join(SUMMARY_LINES) + "\n"
    assert hashlib.sha256(expected_stdout.encode("utf-8")).hexdigest() == EXPECTED_STDOUT_SHA256
    assert receipt["output_evidence"] == {
        "stdout_semantic_sha256": EXPECTED_STDOUT_SHA256,
        "stdout_bytes": len(expected_stdout.encode("utf-8")),
        "stdout_line_count": len(SUMMARY_LINES),
        "exit_code": 0,
        "log_boundary": "Canonical nine-line semantic summary; complete temporary Lean output is parsed in memory and is not retained as release evidence.",
    }
    assert receipt["first_failed_gate"] == "dependency.S56-M-0079-PROOF.master_acceptance"
    assert receipt["first_failed_release_gate"] == "S56-10.6-HERMETIC-COLD-BUILD"
    assert set(receipt["changed_paths"]) == CHANGED_PATHS
    assert packet["item_id"] == ITEM and packet["state"] == "[_]"
    assert packet["base_revision"] == BASE_REVISION
    assert set(packet["changed_paths"]) == CHANGED_PATHS
    assert packet["known_failures"] == receipt["known_failures"]

    status = git("status", "--short", "--untracked-files=all")
    actual_changes = {
        line[3:] for line in status.splitlines() if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual_changes == CHANGED_PATHS
    phase_notes = (HERE / "validation-phase.md").read_text(encoding="utf-8")
    assert "audit and theorem completion are false" in phase_notes
    assert "same-worker" in phase_notes and "cold empty-cache" in phase_notes
    for relative in CHANGED_PATHS:
        assert_text_hygiene(ROOT / relative)

    print("\n".join(SUMMARY_LINES))


if __name__ == "__main__":
    main()
