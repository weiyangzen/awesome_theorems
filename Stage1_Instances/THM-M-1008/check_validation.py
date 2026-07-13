#!/usr/bin/env python3
"""Fail-closed narrow validator for S56-M-1008-VALIDATION."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-1008"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM = "S56-M-1008-VALIDATION"
THEOREM = "THM-M-1008"
BASE_REVISION = "4e632139f5060edf088cd107551caac63981263b"
BASE_TREE = "7a87a6b3f6b71cfb0b2d98872327edc8fe8620e6"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MATHLIB_REMOTE = "https://github.com/leanprover-community/mathlib4.git"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
EXPRESSION_SHA256 = "2d9e3cd06b290ffddd906b177c7400dc999028ef45dc0134d845621a4aa7b76c"
DENOMINATOR_SHA256 = "d41339ef9ffeddf215d8f5f37732901fbfecdb1b1f662e794344c7a2f4665b3d"
EXPECTED_AXIOMS = ["propext", "Classical.choice", "Quot.sound"]
EXPECTED_RUNNER_STDOUT_SHA256 = "7e0a0dedb3373ed464bca81d9296985e252f9c9ade8ba22e0ddd572dc0284bbe"
EXPECTED_INPUTS = {
    "Statement.lean": "95e22d470855eae44d723c6c58101abf1211d5405bc36d5c838f623a879febf6",
    "ObligationTree.lean": "6c9731ae18bc398ce660645f8ba073af562d3e6eb93b0c3765530a478b3a306c",
    "Proof.lean": "1eba05c2aa6aca47991e95119de172cb83f0f7f9d2196129ae2ac5cba416e6a2",
    "Validation.lean": "4d9f370fcf85fde3257d7ad2732803f3ce21d4974180a083876e613ba944b33b",
    "intake.json": "3ffa07e728c3550950c5f1882ab0edabb6698c2e6de456f9b89b3d0bbaed0c3e",
    "statement.json": "62a01eeea532a214c6e8f0ebae79c8b831e84c622c7c4d310445c246d48534b4",
    "anchor-audit.json": "dd1a35659d5f1ee69aa8c1fdb4fbf1ea523535df0ed99a1613948ad49dfccf3d",
    "obligation-registry.json": "e7a31a8b5aead50a20b1bfa0ea3d76fa5a90fc1780eefa0f53ce35c99fd3d14f",
    "typed-graphs.json": "50bc3f03b26f4b23212080e4489bf90de1348ab0ef3eea30bb370eab26b34162",
    "validation-specs.json": "34a966cf777563131cded8d12d01d67bf36c76b60707a93c83b7730de5e006a5",
    "source_statement_crosswalk.md": "5df09f728e30c0fd3cbeab03615f6ef9a378941a3acfa2c4cc6340f87035a497",
    "proof-validation.md": "4f5020d521d496c5246695289c3bfafe247b3669ae8ad39b283cb668e8c62387",
    "check_obligation_tree.py": "2070b2a260c7615be9e9f71ab868ffe881cb246daab29e01bf2c17955ed7b45c",
    "check_validation.sh": "aed324a311049f876b88aaf24461cfba41be96faf33a5ae059b90a9e12b16f1d",
    "validation-spec.json": "9570d04c1fb0be1b6c9fa3b80ff02dd0ef46317c9a1a3cfa76cd0fd14b16c8a5",
}
EXPECTED_TOOL_INPUTS = {
    "lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
DIRECT_IMPORTS = {
    "Mathlib/Probability/IdentDistribIndep": (
        "f8f96ae62d11dfa68b55b49eeadcf0ed8d43b2422c08c71d8c960e409cebd93c",
        "b3de0ef146c92812e2861a2bc9f013664b3cf1513e17d6875a10044975b8b3ee",
    ),
    "Mathlib/Probability/Independence/ZeroOne": (
        "91add87eb03878efc30ae07701488bf712f85d82788de6a9da5af6a715de20fe",
        "d33fd1ca0f08ec71f1e6b8a795b1a93bfa8847295ba5aafeb794566a531b899b",
    ),
    "Mathlib/Probability/ProductMeasure": (
        "5f90deb8a7679e5a5631f6dca5615ddefa80ae0776978b9ab1107f256a42d485",
        "4876d74b787c2a5b2bef1d0f4b0f6f42a4608b963aca9cdf77f0ea00a4226475",
    ),
    "Mathlib/MeasureTheory/Measure/SeparableMeasure": (
        "634256c968e2f35a5a950ddc5e1bcfb1c747e5ebaa66a51160093e805d2fd5a4",
        "0276883ae8757038fd7847313b40e9f2bdb4844d6671f46a74cae9996b4036ba",
    ),
    "Mathlib/MeasureTheory/Measure/MeasuredSets": (
        "bea003d248da5c7af44103575f86739c130a90c5ea298e9e6bc2a2b7037932cd",
        "5d2f7bd5201d00c49dcadc961caa897212280d92a9360a520d922d620ccbc6d1",
    ),
    "Mathlib/GroupTheory/Perm/Fin": (
        "3cf255a32be19160c0f8b94047271f3a57137ebdb81b346aeea610f94e56950f",
        "841eed8894f63bc4061c77652dbb07b6463b6025216fc314b30da3194818c489",
    ),
    "Mathlib/Logic/Equiv/Fin/Basic": (
        "7d0c67b09cf410ce56f3b7cc564709b6775f0cab12c68f6e3719c81f6bcca0e2",
        "4ce3d855f48e727488c25c7eb29d54b51741cda93d59b1823e7398f0a8c2fa34",
    ),
}
LICENSE_SHA256 = "b40930bbcf80744c86c46a12bc9da056641d722716c378f5659b9e555ef833e1"
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/Validation.lean",
    f"Stage1_Instances/{THEOREM}/check_validation.py",
    f"Stage1_Instances/{THEOREM}/check_validation.sh",
    f"Stage1_Instances/{THEOREM}/validation-phase.md",
    f"Stage1_Instances/{THEOREM}/validation-receipt.json",
    f"Stage1_Instances/{THEOREM}/validation-spec.json",
}
SUMMARY_LINES = (
    "PASS THM-M-1008 narrow validation",
    "PASS kernel replay: exact statement, conditional composition, proof root, and exact-type probe elaborated under network isolation",
    "PASS trust observation: checked declarations report exactly propext, Classical.choice, and Quot.sound and the root is transitively sorry-free",
    "PASS selected provenance: frozen hashes, direct imports, compiled objects, clean mathlib pin, license, and tool identities agree",
    "PASS hygiene: comment-stripped prohibited-construct scan and kernel sorry checks passed",
    "FAIL CLOSED authority: proof master acceptance, a proof receipt, and frozen-graph/direct-idempotence-route reconciliation are absent",
    "FAIL CLOSED trust/provenance: foundation policy, complete transitive declaration/TCB closure, SBOM, and source-boundary acceptance remain open",
    "FAIL CLOSED hermetic/independent: shared warm .lake and same-worker type probe are neither cold offline replay nor distinct signed verification",
    "audit_complete=false; theorem_complete=false",
)
TIMEOUT_SECONDS = 600.0


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict), path
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(argv: list[str], *, cwd: Path = ROOT, check: bool = True) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        argv,
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=TIMEOUT_SECONDS,
        check=False,
    )
    if check and result.returncode != 0:
        raise RuntimeError(f"command failed ({result.returncode}): {argv!r}\n{result.stdout}")
    return result


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["git", *args], cwd=cwd).stdout.strip()


def code_without_comments(source: str) -> str:
    source = re.sub(r"/-.*?-/", "", source, flags=re.DOTALL)
    return re.sub(r"--.*$", "", source, flags=re.MULTILINE)


def assert_text_hygiene(path: Path) -> None:
    data = path.read_bytes()
    assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())


def main() -> None:
    spec = load(HERE / "validation-spec.json")
    receipt = load(HERE / "validation-receipt.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")
    targets = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    intake = load(HERE / "intake.json")
    statement = load(HERE / "statement.json")
    anchor = load(HERE / "anchor-audit.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    frozen_specs = load(HERE / "validation-specs.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 288 and target["baseline"] == "L0"
    assert target["lifecycle_mode"] == "planned"
    assert target["rework_required"] is True and target["theorem_complete"] is False
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item == {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 288,
        "phase": "validation",
        "layer": 5,
        "state": "[ ]",
        "depends_on": ["S56-M-1008-PROOF"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Run hermetic kernel, trust, provenance, and independent validation gates.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }
    predecessor = next(row for row in execution["items"] if row["id"] == "S56-M-1008-PROOF")
    assert predecessor["state"] == "[_]" and predecessor["attempts"] == 1
    assert not (HERE / "proof-receipt.json").exists()

    for name, expected in EXPECTED_INPUTS.items():
        assert sha256(HERE / name) == expected, f"stale validation input: {name}"
    for name, expected in EXPECTED_TOOL_INPUTS.items():
        assert sha256(LEAN_ROOT / name) == expected, f"changed tool input: {name}"
    formal = statement["canonical_formal_target"]
    assert formal["declaration_or_expression"] == (
        "Stage1Instances.THM_M_1008.HewittSavageZeroOneTarget"
    )
    assert formal["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert formal["statement_file_sha256"] == EXPECTED_INPUTS["Statement.lean"]
    assert anchor["canonical_target_expression_sha256"] == EXPRESSION_SHA256
    assert registry["frozen_against_statement_sha256"] == EXPECTED_INPUTS["Statement.lean"]
    assert registry["frozen_against_anchor_audit_sha256"] == EXPECTED_INPUTS["anchor-audit.json"]
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert intake["obligation_registry_hash"] == "sha256:" + DENOMINATOR_SHA256

    closure = graphs["closure_boundary"]
    assert closure["root_closed"] is False
    assert closure["remaining_root_cut_set"] == ["M1008-T-SELF-INDEPENDENCE"]
    assert closure["theorem_complete"] is False
    root_node = next(node for node in graphs["nodes"] if node["obligation_id"] == "M1008-ROOT")
    assert root_node["machine_debt"] == "M2"
    assert next(node for node in graphs["nodes"] if node["obligation_id"] == "M1008-S-FOUNDATION")[
        "machine_debt"
    ] == "M4"
    assert next(node for node in graphs["nodes"] if node["obligation_id"] == "M1008-X-PROVENANCE")[
        "machine_debt"
    ] == "M4"
    proof_graph = graphs["graphs"]["proof"]["edges"]
    assert any(
        edge["from"] == "M1008-ROOT" and edge["to"] == "M1008-T-ASSEMBLE"
        for edge in proof_graph
    )
    proof_source = (HERE / "Proof.lean").read_text(encoding="utf-8")
    assert "theorem hewittSavageZeroOneTarget : HewittSavageZeroOneTarget" in proof_source
    for unused_frozen_route in (
        "root_of_selfIndependencePackage",
        "zeroOne_of_selfIndependence",
        "SelfIndependencePackage",
    ):
        assert unused_frozen_route not in code_without_comments(proof_source)
    assert "symmetric_path_measureReal_factorization" in proof_source
    assert "eq_zero_or_one_of_sq_eq_self" in proof_source
    assert frozen_specs["item_id"] == "S56-M-1008-OBLIGATION_TREE"

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
    probe = code_without_comments((HERE / "Validation.lean").read_text(encoding="utf-8"))
    assert "import Proof" in probe
    assert "exactRootTypeProbe" in probe and "assert_no_sorry" in probe

    manifest = load(LEAN_ROOT / "lake-manifest.json")
    mathlib_entry = next(row for row in manifest["packages"] if row["name"] == "mathlib")
    assert mathlib_entry["rev"] == mathlib_entry["inputRev"] == MATHLIB_REVISION
    assert MATHLIB.resolve().is_dir(), "pinned mathlib artifact is unavailable"
    assert git("rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert git("remote", "get-url", "origin", cwd=MATHLIB) == MATHLIB_REMOTE
    assert git("status", "--porcelain=v1", cwd=MATHLIB) == ""
    for module, (source_hash, olean_hash) in DIRECT_IMPORTS.items():
        assert sha256(MATHLIB / f"{module}.lean") == source_hash
        assert sha256(MATHLIB / ".lake" / "build" / "lib" / "lean" / f"{module}.olean") == olean_hash
    assert sha256(MATHLIB / "LICENSE") == LICENSE_SHA256

    lean = Path.home() / ".elan" / "toolchains" / "leanprover--lean4---v4.29.0" / "bin" / "lean"
    lake = lean.with_name("lake")
    python = Path(os.path.realpath(os.sys.executable))
    git_path = shutil.which("git")
    bwrap_path = shutil.which("bwrap")
    assert git_path is not None and bwrap_path is not None
    assert LEAN_COMMIT in run([str(lean), "--version"]).stdout
    assert "5.0.0-src+98dc76e" in run([str(lake), "--version"]).stdout
    assert sha256(lean) == "3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf"
    assert sha256(lake) == "a608ff084d7e2af228b92a29d7c2fd083ba0580e46889175ec74a81678c98359"
    assert sha256(python) == "b8d8288faefdd300201f43fcf00f6f539a27218eeed3a3dff5ab10b9c4c99700"
    assert sha256(Path(os.path.realpath(git_path))) == (
        "8a48eefa306b9a2a9c3e576784a74ad7485779279e5a46ec43361a1864760e45"
    )
    assert sha256(Path(os.path.realpath(bwrap_path))) == (
        "0abea81db798ebf6b4742ac0664802d97521547a353c2a0dbdc21d76cbbfd2c0"
    )

    runner = run(["bash", str(HERE / "check_validation.sh")]).stdout
    assert hashlib.sha256(runner.encode()).hexdigest() == EXPECTED_RUNNER_STDOUT_SHA256
    assert runner.splitlines() == [
        "PASS THM-M-1008 network-isolated narrow kernel replay",
        "PASS exact root/type probe: propext, Classical.choice, Quot.sound",
        "PASS transitive sorry check: proof root and type probe are sorry-free",
    ]

    assert spec["schema_version"] == "stage1-validation-spec/1.0"
    assert spec["item_id"] == ITEM and spec["theorem_id"] == THEOREM
    assert spec["cwd"] == "."
    assert spec["argv"] == ["python3", "-B", f"Stage1_Instances/{THEOREM}/check_validation.py"]
    assert spec["timeout_seconds"] == 600 and spec["network_policy"] == "denied"
    assert spec["expected_exit"] == 0 and spec["release_grade"] is False
    assert "unshared network namespace" in spec["network_enforcement"]
    assert spec["allowed_observed_axioms"] == EXPECTED_AXIOMS

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["phase"] == "validation" and receipt["intent"] == "validate"
    assert receipt["depends_on"] == ["S56-M-1008-PROOF"]
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["release_grade"] is False and receipt["content_addressed_release_evidence"] is False
    assert receipt["covered_obligation_ids"] == spec["covered_obligation_ids"]
    assert receipt["validated_declarations"] == spec["covered_declarations"]
    assert receipt["accepted_closed_obligation_ids"] == []
    for name, expected in EXPECTED_INPUTS.items():
        assert receipt["inputs"][name] == expected, name
    assert receipt["inputs"]["check_validation.py"] == sha256(HERE / "check_validation.py")
    assert receipt["inputs"]["validation-phase.md"] == sha256(HERE / "validation-phase.md")
    assert receipt["inputs"]["worker_packet"] == sha256(ROOT / ".stage1-worker-selftest.json")
    assert receipt["canonical_target"] == {
        "declaration": "Stage1Instances.THM_M_1008.HewittSavageZeroOneTarget",
        "proof_declaration": "Stage1Instances.THM_M_1008.hewittSavageZeroOneTarget",
        "elaborated_expression_sha256": EXPRESSION_SHA256,
        "registry_denominator_sha256": DENOMINATOR_SHA256,
    }
    result = receipt["result"]
    assert result["root_kernel_replay"] == "provisional_pass"
    assert result["observed_axioms"] == EXPECTED_AXIOMS
    assert result["transitive_sorry_check"] == "pass"
    assert result["proof_master_acceptance"] == "fail_closed"
    assert result["structured_state_reconciliation"].startswith("fail_closed_")
    assert result["hermetic_cold_offline_replay"] == "fail_closed"
    assert result["independent_distinct_runner"] == "fail_closed"
    assert result["accepted_root_closed"] is False
    assert result["audit_complete"] is result["theorem_complete"] is False
    assert receipt["root_vector_before"] == {"H": "H1", "M": "M2", "R": "R3"}
    assert receipt["root_vector_after_worker_selftest"] == receipt["root_vector_before"]
    assert receipt["first_failed_gate"] == "dependency.S56-M-1008-PROOF.master_acceptance"
    assert receipt["first_failed_release_gate"] == "S56-10.6-HERMETIC-COLD-BUILD"
    assert set(receipt["changed_paths"]) == CHANGED_PATHS

    assert packet == {
        "item_id": ITEM,
        "changed_paths": receipt["changed_paths"],
        "commands": receipt["worker_commands"],
        "output_summary": "\n".join(SUMMARY_LINES),
        "base_revision": BASE_REVISION,
        "known_failures": receipt["known_failures"],
        "state": "[_]",
    }
    actual_changes = {
        line[3:] for line in git("status", "--short", "--untracked-files=all").splitlines()
        if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual_changes == CHANGED_PATHS, (actual_changes, CHANGED_PATHS)
    for path in CHANGED_PATHS:
        assert_text_hygiene(ROOT / path)

    assert receipt["output_evidence"]["stdout_semantic_sha256"] == hashlib.sha256(
        ("\n".join(SUMMARY_LINES) + "\n").encode()
    ).hexdigest()
    print("\n".join(SUMMARY_LINES))


if __name__ == "__main__":
    main()
