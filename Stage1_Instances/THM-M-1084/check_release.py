#!/usr/bin/env python3
"""Fail-closed release reconciliation for S56-M-1084-RELEASE."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-1084"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM = "S56-M-1084-RELEASE"
THEOREM = "THM-M-1084"
BASE_REVISION = "111bbeb1a210ae4e8525a4342012921ab60e466f"
BASE_TREE = "8f705aa79622bf1e9be0665ae1254313df21b4f6"
EXPRESSION_SHA256 = "25bdfe85eaaa67694f865e6af60c240b013b2fbcd9acfb2949e5abdb0b34ca99"
DENOMINATOR_SHA256 = "a2bf7a0e46b0ca64f3ce1259043f8e1f7c85975bb4762a9e2a5256709555111a"
VALIDATION_RECEIPT_ID = "S56-M-1084-VALIDATION-local-20260715T063000+0800"
VALIDATION_RECEIPT_SHA256 = "cbd1f7054a9b06896c99542229ab0a426dff3e15a65cab981071df974436ff4a"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
ALLOWED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
VECTOR = {"H": "H1", "M": "M3", "R": "R3"}
MATHEMATICAL_CUT = ["M1084-T-INTEGRABLE", "M1084-T-ENTROPY"]
INVENTORY_IDS = [
    "M1084-ROOT", "M1084-S-DEFINITIONS", "M1084-S-BOUNDARY",
    "M1084-S-FOUNDATION", "M1084-N-GAUSSIAN-MGF", "M1084-C-NETS",
    "M1084-C-CHAIN", "M1084-L-MAX-INCREMENT", "M1084-L-DYADIC-SUM",
    "M1084-L-LIMIT", "M1084-T-INTEGRABLE", "M1084-T-ENTROPY",
    "M1084-T-ASSEMBLE", "M1084-X-SOURCE", "M1084-X-EXTERNAL",
    "M1084-X-PROVENANCE",
]
RECONCILED_INPUTS = {
    "instance.json": "6610ef0b1862fafd446b143754fb3e32d835d95a581a17ad1938ed8a04503103",
    "task-dag.json": "d5bf4d607b7bb9283438bbe1b47a79ab6857a4f77f3fe828eac1f4ca3b0754cb",
    "statement.json": "ea2e93a4d5e878331376aec2724eba0d57a8727e9674e55fb941a110f4cbbe42",
    "Statement.lean": "75ce1fe27d00a5b5f42d0fe6bfc961e9e836145cb2f608faab5ddb122ba98222",
    "anchor-audit.json": "7e0e035b4a1a97db174b53d939eec6e946d29339f6c425c03c236bfdbe609976",
    "AnchorAudit.lean": "d8d2993319211686db17d8e06c5997b8e1899060eb7669dbd85ab843ce446ac5",
    "obligation-registry.json": "1c447a6f1691e586160ba324c732072ad9604643e2edd7ee3d8fd7a3b4396117",
    "typed-graphs.json": "38c06677202fa48a54df6b892b4d0790dbf5867b20fec188fe69ff864a0e46ef",
    "ObligationTree.lean": "8868690697aeac26a40f48b5abb88a5859c632b3eadbc7e63666e427f35aabc6",
    "GaussianMGFBridge.lean": "721c0fcae4dbcaf106382d7ac01b5239d29aec941502bc9c59ccdf24d4576142",
    "CoveringNets.lean": "aab49b3768a09f6db7f4925495e6d3113c3c25d3a2bce274bb393079e027a32f",
    "Validation.lean": "236262c9f0fe969a1e0bc0e928335574f97e5b6c401379318a25682fb098f53e",
    "proof-attempt.json": "e2120e7140102367186e2e252dd4609d818c4c7194d60b687efcd20725dc26f1",
    "proof-receipt.json": "8f3217aee237783ed970490ee03c91a355590c6f7236e6e1b0ccb4bc4779c677",
    "validation-spec.json": "ae891862cc92af0907928cab7f7940631cb6c684bbe536eb599c791c05bce2b1",
    "validation-receipt.json": VALIDATION_RECEIPT_SHA256,
    "check_validation.py": "fdfab82263289490842f7754c092aeaccccbd85cacbea7e29d1df7e02cf76f6c",
    "source-statement-crosswalk.md": "829cd5942374bdc40b246c99ed2e6502eb919de26ce3117ec815a0f42e670352",
}
PARTIAL_DECLARATIONS = (
    "Stage1Instances.THM_M_1084.Proof.hasSubgaussianMGF_of_hasGaussianLaw_of_integral_eq_zero",
    "Stage1Instances.THM_M_1084.Proof.increment_mgf_eq_dist_sq",
    "Stage1Instances.THM_M_1084.Proof.increment_hasSubgaussianMGF",
    "Stage1Instances.THM_M_1084.Proof.gaussianIncrementMGFPackage",
    "Stage1Instances.THM_M_1084.Proof.exists_openBallCover",
    "Stage1Instances.THM_M_1084.Proof.exists_minimal_openBallCover",
    "Stage1Instances.THM_M_1084.Proof.coveringNumber_pos",
)
DIFFERENTIAL_DECLARATIONS = (
    "Stage1Instances.THM_M_1084.Validation.independentlyReconstructedGaussianIncrementMGFPackage",
    "Stage1Instances.THM_M_1084.Validation.independentlyReconstructedCoveringNumberPos",
)
COMPOSITION = "Stage1Instances.THM_M_1084.root_of_integrability_and_entropy_packages"
SUMMARY_LINES = [
    "PASS S56-M-1084-RELEASE negative reconciliation",
    "PASS fresh trust-zero network-isolated replay: exact statement, conditional composition, and partial bodies",
    "BLOCKED dependency: S56-M-1084-VALIDATION is provisional and not master-accepted",
    "BLOCKED exact root: M1084-T-INTEGRABLE and M1084-T-ENTROPY have no proof bodies",
    "BLOCKED assurance: H0/R0/trust/cold-offline/SBOM/independent-verifier/bundle gates remain open",
    "verdict=blocked lifecycle=planned root_vector=H1/M3/R3 audit_complete=false theorem_complete=false",
]
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/check_release.py",
    f"Stage1_Instances/{THEOREM}/release-decision.json",
    f"Stage1_Instances/{THEOREM}/release-receipt.json",
    f"Stage1_Instances/{THEOREM}/release-spec.json",
    f"Stage1_Instances/{THEOREM}/release-validation.md",
}


def load(path: Path) -> dict:
    def reject_duplicates(pairs: list[tuple[str, object]]) -> dict:
        result: dict[str, object] = {}
        for key, value in pairs:
            if key in result:
                raise AssertionError(f"duplicate JSON key in {path}: {key}")
            result[key] = value
        return result

    value = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicates)
    assert isinstance(value, dict), path
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(
    argv: list[str],
    *,
    cwd: Path = ROOT,
    env: dict[str, str] | None = None,
    timeout: int = 900,
) -> str:
    result = subprocess.run(
        argv, cwd=cwd, env=env, text=True, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, timeout=timeout, check=False,
    )
    if result.returncode != 0:
        raise AssertionError(
            f"command failed ({result.returncode}): {argv!r}\n{result.stdout}"
        )
    return result.stdout


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["git", *args], cwd=cwd).strip()


def code_without_comments(source: str) -> str:
    source = re.sub(r"/-.*?-/", "", source, flags=re.DOTALL)
    return re.sub(r"--.*$", "", source, flags=re.MULTILINE)


def printed_axioms(output: str, declaration: str) -> set[str]:
    no_axioms = f"'{declaration}' does not depend on any axioms"
    match = re.search(
        re.escape(f"'{declaration}' depends on axioms: [") + r"(.*?)]",
        output,
        re.DOTALL,
    )
    assert output.count(no_axioms) + (match is not None) == 1, declaration
    if match is None:
        return set()
    return {part.strip() for part in match.group(1).split(",") if part.strip()}


def network_isolated(
    bwrap: str,
    argv: list[str],
    *,
    cwd: Path,
    env: dict[str, str],
) -> str:
    fixed_env = dict(env)
    fixed_env["PWD"] = str(cwd)
    command = [
        bwrap, "--unshare-net", "--dev-bind", "/", "/", "--proc", "/proc",
        "--chdir", str(cwd), "--", "env", "-i",
        *[f"{key}={value}" for key, value in sorted(fixed_env.items())],
        *argv,
    ]
    return run(command, cwd=cwd)


def assert_text_hygiene(path: Path) -> None:
    data = path.read_bytes()
    assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())


def main() -> None:
    if sys.flags.optimize != 0:
        raise RuntimeError("release checker requires Python assertions")

    decision = load(HERE / "release-decision.json")
    receipt = load(HERE / "release-receipt.json")
    spec = load(HERE / "release-spec.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")
    instance = load(HERE / "instance.json")
    tasks = load(HERE / "task-dag.json")
    statement = load(HERE / "statement.json")
    anchor = load(HERE / "anchor-audit.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    proof = load(HERE / "proof-receipt.json")
    validation = load(HERE / "validation-receipt.json")
    targets = load(ROOT / "Docs" / "Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 526 and target["baseline"] == "L0"
    assert target["rework_required"] is True and target["legacy_artifacts_accepted"] is False
    assert target["lifecycle_mode"] == "planned" and target["theorem_complete"] is False
    release_item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert release_item == {
        "id": ITEM, "theorem_id": THEOREM, "execution_rank": 526,
        "phase": "release", "layer": 6, "state": "[ ]",
        "depends_on": ["S56-M-1084-VALIDATION"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Reconcile evidence and decide the exact theorem-completion verdict.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0, "children": [],
    }
    validation_item = next(
        row for row in execution["items"] if row["id"] == "S56-M-1084-VALIDATION"
    )
    assert validation_item["state"] == "[_]" and validation_item["attempts"] == 1
    local_release = next(row for row in tasks["tasks"] if row["id"] == ITEM)
    local_validation = next(
        row for row in tasks["tasks"] if row["id"] == "S56-M-1084-VALIDATION"
    )
    assert local_release == {
        "id": ITEM, "depends_on": ["S56-M-1084-VALIDATION"], "state": "open"
    }
    assert local_validation["state"] == "open" and tasks["accepted_states"] == []

    assert decision["reconciled_inputs"] == RECONCILED_INPUTS
    for name, expected in RECONCILED_INPUTS.items():
        assert sha256(HERE / name) == expected, f"reconciled input drifted: {name}"

    assert instance["lifecycle"] == tasks["lifecycle"] == "planned"
    assert instance["root_vector"] == VECTOR
    assert instance["accepted_proof_state"] == []
    assert instance["audit_complete"] is instance["theorem_complete"] is False
    formal = statement["canonical_formal_target"]
    assert formal["declaration_or_expression"] == (
        "Stage1Instances.THM_M_1084.DudleyEntropyBoundTarget"
    )
    assert formal["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert formal["statement_file_sha256"] == RECONCILED_INPUTS["Statement.lean"]
    assert registry["root_obligation_id"] == "M1084-ROOT"
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert [row["obligation_id"] for row in registry["obligations"]] == INVENTORY_IDS
    assert registry["status_observed_after_freeze"]["root_machine_debt"] == "M3"
    assert graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    closure = graphs["closure_boundary"]
    assert closure["root_closed"] is closure["audit_complete"] is False
    assert closure["theorem_complete"] is False
    assert closure["remaining_root_cut_set"] == MATHEMATICAL_CUT
    root_node = next(row for row in graphs["nodes"] if row["obligation_id"] == "M1084-ROOT")
    assert root_node["machine_debt"] == "M3" and root_node["evidence_ids"] == []
    for obligation_id in MATHEMATICAL_CUT:
        node = next(row for row in graphs["nodes"] if row["obligation_id"] == obligation_id)
        assert node["machine_debt"] == "M4" and node["evidence_ids"] == []

    assert anchor["root_machine_classification"] == "M1"
    assert "type is not the frozen target" in anchor["root_classification_reason"]
    external = next(row for row in anchor["candidates"] if row["candidate_id"] == "S56-M-1084-C03")
    assert external["kind"] == "near_external_proof_candidate"
    assert external["classification"] == "M1_external_upstream_anchor_only"
    assert external["normalized_match"].startswith("not exact:")
    assert "not locally checked" in external["integration_status"]

    assert proof["accepted"] is False
    assert proof["result"]["root_kernel_closed"] is False
    assert proof["remaining_root_cut_set"] == MATHEMATICAL_CUT
    assert validation["receipt_id"] == VALIDATION_RECEIPT_ID
    assert validation["support_state"] == "provisional_worker_selftest"
    assert validation["accepted"] is validation["release_grade"] is False
    assert validation["accepted_closed_obligation_ids"] == []
    validation_result = validation["result"]
    assert validation_result["root_kernel_closed"] is False
    assert validation_result["remaining_root_cut_set"] == MATHEMATICAL_CUT
    assert validation_result["complete_trust_and_provenance_closure"] == "fail_closed"
    assert validation_result["hermetic_cold_offline_replay"] == "fail_closed"
    assert validation_result["independent_distinct_runner"] == "fail_closed"
    assert validation_result["audit_complete"] is validation_result["theorem_complete"] is False

    assert decision["item_id"] == ITEM and decision["theorem_id"] == THEOREM
    assert decision["base_revision"] == BASE_REVISION and decision["base_tree"] == BASE_TREE
    assert decision["support_state"] == "provisional_worker_selftest"
    assert decision["proposed_state"] == "[_]" and decision["release_grade"] is False
    assert decision["verdict"] == "blocked"
    assert decision["lifecycle_before"] == decision["lifecycle_after"] == "planned"
    assert decision["accepted_receipt_ids"] == []
    dependency = decision["dependency"]
    assert dependency["item_id"] == validation["item_id"]
    assert dependency["receipt_id"] == validation["receipt_id"]
    assert dependency["receipt_sha256"] == VALIDATION_RECEIPT_SHA256
    assert dependency["worker_projection"] == "[_]"
    assert dependency["master_accepted"] is dependency["receipt_accepted"] is False
    assert dependency["receipt_release_grade"] is False
    assert decision["root_vector"]["accepted_before"] == VECTOR
    assert decision["root_vector"]["accepted_after"] == VECTOR
    assert decision["terminal_decisions"] == {
        "audit_complete": False, "theorem_complete": False,
        "audit_z": "blocked", "theorem_z": "blocked", "release_accepted": False,
    }
    assert decision["first_failed_gate"]["gate_id"] == "S56-10.2-DEPENDENCY-ACCEPTANCE"
    assert decision["first_failed_gate"]["dependency_gate"] == (
        "dependency.S56-M-1084-VALIDATION.master_acceptance"
    )
    assert decision["first_failed_theorem_gate"]["gate_id"] == "proof.root_kernel_closure"
    assert decision["first_failed_release_gate"]["gate_id"] == (
        "S56-10.6-HERMETIC-COLD-BUILD"
    )
    assert decision["canonical_obligation_ids"] == INVENTORY_IDS
    assert decision["registry_denominator_sha256"] == DENOMINATOR_SHA256
    for key in (
        "audit_inventory_reconciliation", "human_source_acceptance",
        "readability_acceptance", "foundation_and_trust_closure",
        "hermetic_release_reproduction", "supply_chain_closure",
        "independent_release_verification", "protected_ci_and_adversarial_gates",
        "deterministic_release_bundle", "master_acceptance",
    ):
        assert decision["evidence_reconciliation"][key].startswith("missing"), key
    assert decision["evidence_reconciliation"]["root_kernel_closure"].startswith("failed")
    assert "rejected as a root promotion" in decision["evidence_reconciliation"][
        "anchor_machine_projection"
    ]
    cut_text = "\n".join(decision["remaining_root_cut_set"])
    for fragment in (
        "master acceptance", "M1084-T-INTEGRABLE", "M1084-T-ENTROPY",
        "AUDIT-Z", "accepted H0", "accepted R0", "accepted foundation profile",
        "empty-cache network-denied cold build", "SBOM and license",
        "two signed attestations", "minimal release verifier",
        "deterministic build-twice content-addressed release bundle",
    ):
        assert fragment in cut_text, fragment

    assert spec["recipe_id"] == "S56-M-1084-RELEASE-negative-reconciliation-v1"
    assert spec["schema_version"] == "stage1-release-recipe/1.0"
    assert spec["item_id"] == ITEM and spec["theorem_id"] == THEOREM
    assert spec["argv"] == [
        "python3", "-I", "-B", f"Stage1_Instances/{THEOREM}/check_release.py"
    ]
    assert spec["network_policy"] == "denied" and spec["expected_exit"] == 0
    assert receipt["recipe"] == {
        key: spec[key] for key in (
            "recipe_id", "cwd", "argv", "env_allowlist", "timeout_seconds",
            "network_policy", "network_enforcement", "expected_exit",
            "expected_outputs", "covered_obligation_ids", "covered_declarations",
        )
    }

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by|extern)\b|"
        r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
        r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
        r"(?:axiom|constant|opaque|unsafe)\b",
        re.MULTILINE,
    )
    lean_files = (
        "Statement.lean", "AnchorAudit.lean", "ObligationTree.lean",
        "GaussianMGFBridge.lean", "CoveringNets.lean", "Validation.lean",
    )
    for name in lean_files:
        source = code_without_comments((HERE / name).read_text(encoding="utf-8"))
        assert prohibited.search(source) is None, f"prohibited source token in {name}"
    validation_source = code_without_comments((HERE / "Validation.lean").read_text())
    for forbidden in (
        "DudleyEntropyBoundTarget", "SupremumIntegrabilityPackage",
        "EntropyInequalityPackage", "root_of_integrability_and_entropy_packages",
    ):
        assert forbidden not in validation_source, forbidden

    manifest = load(LEAN_ROOT / "lake-manifest.json")
    mathlib_entry = next(row for row in manifest["packages"] if row["name"] == "mathlib")
    assert mathlib_entry["rev"] == mathlib_entry["inputRev"] == MATHLIB_REVISION
    assert MATHLIB.resolve().is_dir(), "pinned mathlib artifact is unavailable"
    assert git("rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert git("status", "--porcelain=v1", cwd=MATHLIB) == ""
    lean = run(["lake", "env", "which", "lean"], cwd=LEAN_ROOT).strip()
    lake = run(["lake", "env", "which", "lake"], cwd=LEAN_ROOT).strip()
    lean_version = run(["lake", "env", "lean", "--version"], cwd=LEAN_ROOT)
    lake_version = run(["lake", "--version"], cwd=LEAN_ROOT)
    assert "4.29.0" in lean_version and LEAN_COMMIT in lean_version
    assert "5.0.0-src+98dc76e" in lake_version
    lean_path = run(["lake", "env", "printenv", "LEAN_PATH"], cwd=LEAN_ROOT).strip()
    bwrap = shutil.which("bwrap")
    assert bwrap is not None, "bubblewrap unavailable for denied-network replay"
    python = Path(os.path.realpath(sys.executable))
    git_path = shutil.which("git")
    assert git_path is not None
    environment = receipt["environment"]
    assert environment["lean_executable_sha256"] == sha256(Path(lean))
    assert environment["lake_executable_sha256"] == sha256(Path(lake))
    assert environment["python_executable_sha256"] == sha256(python)
    assert environment["git_executable_sha256"] == sha256(
        Path(os.path.realpath(git_path))
    )
    assert environment["bubblewrap_executable_sha256"] == sha256(
        Path(os.path.realpath(bwrap))
    )
    assert environment["mathlib_revision"] == MATHLIB_REVISION
    assert environment["mathlib_tree"] == MATHLIB_TREE
    assert environment["mathlib_license_sha256"] == sha256(MATHLIB / "LICENSE")

    with tempfile.TemporaryDirectory(prefix="stage1-m1084-release-") as tmp_name:
        tmp = Path(tmp_name)
        for name in lean_files:
            (tmp / name).write_bytes((HERE / name).read_bytes())
        common_env = {
            "HOME": os.environ.get("HOME", "/nonexistent"),
            "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8", "LEAN_NUM_THREADS": "1",
            "PATH": os.environ.get("PATH", ""), "TZ": "UTC",
        }
        os.chmod(tmp, 0o700)
        old_umask = os.umask(0o022)
        try:
            statement_out = network_isolated(
                bwrap,
                [lean, "--trust=0", "-o", str(tmp / "Statement.olean"), "Statement.lean"],
                cwd=tmp, env={**common_env, "LEAN_PATH": lean_path},
            )
            local_path = f"{tmp}:{lean_path}"
            anchor_out = network_isolated(
                bwrap, [lean, "--trust=0", "AnchorAudit.lean"],
                cwd=tmp, env={**common_env, "LEAN_PATH": local_path},
            )
            obligation_out = network_isolated(
                bwrap, [lean, "--trust=0", "ObligationTree.lean"],
                cwd=tmp, env={**common_env, "LEAN_PATH": local_path},
            )
            mgf_out = network_isolated(
                bwrap,
                [lean, "--trust=0", "-o", str(tmp / "GaussianMGFBridge.olean"),
                 "GaussianMGFBridge.lean"],
                cwd=tmp, env={**common_env, "LEAN_PATH": local_path},
            )
            nets_out = network_isolated(
                bwrap,
                [lean, "--trust=0", "-o", str(tmp / "CoveringNets.olean"),
                 "CoveringNets.lean"],
                cwd=tmp, env={**common_env, "LEAN_PATH": local_path},
            )
            validation_out = network_isolated(
                bwrap, [lean, "--trust=0", "Validation.lean"],
                cwd=tmp, env={**common_env, "LEAN_PATH": local_path},
            )
        finally:
            os.umask(old_umask)

    assert "DudleyEntropyBoundTarget" in statement_out
    assert "noRetainedCandidateClaimsTerminalProof" in anchor_out
    assert "anchorAuditPermitsTheoremCompletion_eq_false" in anchor_out
    assert printed_axioms(obligation_out, COMPOSITION) <= ALLOWED_AXIOMS
    combined_partial = mgf_out + nets_out
    for declaration in PARTIAL_DECLARATIONS:
        assert printed_axioms(combined_partial, declaration) <= ALLOWED_AXIOMS
    assert combined_partial.count("Declarations are sorry-free!") == len(
        PARTIAL_DECLARATIONS
    )
    for declaration in DIFFERENTIAL_DECLARATIONS:
        assert printed_axioms(validation_out, declaration) <= ALLOWED_AXIOMS
    assert validation_out.count("Declarations are sorry-free!") == len(
        DIFFERENTIAL_DECLARATIONS
    )
    for output in (obligation_out, combined_partial, validation_out):
        assert "sorryAx" not in output and "declaration uses 'sorry'" not in output
        assert "error:" not in output

    assert receipt["receipt_id"] == "S56-M-1084-RELEASE-local-20260715T065457+0800"
    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["phase"] == receipt["intent"] == "release"
    assert receipt["depends_on"] == ["S56-M-1084-VALIDATION"]
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["release_grade"] is receipt["content_addressed_release_evidence"] is False
    assert receipt["result"]["verdict"] == "blocked"
    assert receipt["result"]["audit_complete"] is False
    assert receipt["result"]["theorem_complete"] is False
    assert receipt["root_vector_before"] == receipt["root_vector_after_worker_selftest"] == VECTOR
    assert receipt["accepted_receipt_ids"] == []
    assert receipt["first_failed_gate"] == "S56-10.2-DEPENDENCY-ACCEPTANCE"
    assert receipt["first_failed_dependency_gate"] == (
        "dependency.S56-M-1084-VALIDATION.master_acceptance"
    )
    assert receipt["first_failed_theorem_gate"] == "proof.root_kernel_closure"
    assert receipt["first_failed_release_gate"] == "S56-10.6-HERMETIC-COLD-BUILD"
    assert receipt["remaining_root_cut_set"] == decision["remaining_root_cut_set"]
    assert receipt["inputs"]["release_spec_sha256"] == sha256(HERE / "release-spec.json")
    assert receipt["inputs"]["release_decision_sha256"] == sha256(
        HERE / "release-decision.json"
    )
    assert receipt["inputs"]["release_validation_sha256"] == sha256(
        HERE / "release-validation.md"
    )
    assert receipt["inputs"]["check_release_sha256"] == sha256(HERE / "check_release.py")
    for name, expected in RECONCILED_INPUTS.items():
        assert receipt["inputs"][name] == expected, name

    assert set(packet) == {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert packet["item_id"] == ITEM and packet["base_revision"] == BASE_REVISION
    assert packet["state"] == "[_]"
    assert set(packet["changed_paths"]) == set(receipt["changed_paths"]) == CHANGED_PATHS
    assert packet["known_failures"] == receipt["known_failures"]
    assert packet["output_summary"] == receipt["output_summary"] == SUMMARY_LINES

    status = git("status", "--short", "--untracked-files=all")
    actual_changed = {
        line[3:] for line in status.splitlines()
        if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual_changed == CHANGED_PATHS, (actual_changed, CHANGED_PATHS)
    for relative in CHANGED_PATHS:
        assert_text_hygiene(ROOT / relative)

    obligation_output = run([
        "python3", f"Stage1_Instances/{THEOREM}/check_obligation_tree.py"
    ])
    assert "root closure: open (M3)" in obligation_output
    public = "\n".join(
        (HERE / name).read_text(encoding="utf-8")
        for name in ("release-decision.json", "release-validation.md")
    )
    assert "/home/" not in public and ".cron/" not in public
    for line in SUMMARY_LINES:
        print(line)


if __name__ == "__main__":
    main()
