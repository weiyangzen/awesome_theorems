#!/usr/bin/env python3
"""Fail-closed release reconciliation for S56-M-1070-RELEASE."""

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
HERE = ROOT / "Stage1_Instances" / "THM-M-1070"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM = "S56-M-1070-RELEASE"
THEOREM = "THM-M-1070"
BASE_REVISION = "8b9311952b6b4186c774d25758d16597a7c10a8b"
BASE_TREE = "69a7cea0132f4b76e7324c2d5cc320dec94d2f10"
EXPRESSION_SHA256 = "8e1440de837395201d12a0f2085afe0c03d2504e99240b68154595fc2f8cffc1"
DENOMINATOR_SHA256 = "c5866f4be491aa8209171938c78c36bde996941a27c87686d2a109d6679c5aa9"
VALIDATION_RECEIPT_ID = (
    "S56-M-1070-VALIDATION-network-isolated-20260715T082315+0800-v1"
)
VALIDATION_RECEIPT_SHA256 = (
    "0fef98609b008a7ffdf29b61e1df1c9eda3d914f3ed5092de3a08847822a2b84"
)
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
ALLOWED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
VECTOR = {"H": "H1", "M": "M3", "R": "R4"}
MATHEMATICAL_CUT = [
    "M1070-L-INDEPENDENT",
    "M1070-L-STATIONARY",
    "M1070-L-STOCH-CONT",
]
INVENTORY_IDS = [
    "M1070-ROOT", "M1070-S-DEFINITIONS", "M1070-S-BOUNDARY",
    "M1070-S-FOUNDATION", "M1070-L-PROBABILITY", "M1070-L-MEASURABLE",
    "M1070-L-ZERO", "M1070-L-INDEPENDENT", "M1070-L-STATIONARY",
    "M1070-L-STOCH-CONT", "M1070-T-COMPOSE", "M1070-X-SOURCE",
    "M1070-X-PROVENANCE",
]
SEMANTIC_LEAVES = [
    "M1070-L-PROBABILITY", "M1070-L-MEASURABLE", "M1070-L-ZERO",
    "M1070-L-INDEPENDENT", "M1070-L-STATIONARY", "M1070-L-STOCH-CONT",
]
RECONCILED_INPUTS = {
    "instance.json": "561559bade7af46e6ffc9b1f0806a93f1a19ed73e04b15cc054faf9d7f76de73",
    "task-dag.json": "afbbf04d3c8d80add5b46fa72ccfaa96f2cfc1e6e9d63a3c086bdf9ac341f6f8",
    "statement.json": "eb1dd62ab3d16e9421809d29384bec55485ea35e5e66b30a779c2fa0a4c2316e",
    "Statement.lean": "6968f5fbf916f36d31518be99b631a560afe8a5fbc2ca30108ff1d57bd692268",
    "anchor-audit.json": "74ec2b694f12b059f23d4816379f32a2cadb481da3ac12bed89fd4bc5fbd7679",
    "AnchorAudit.lean": "fcb2f2502a5e3488164d1bb3c3812c246a528a3fa717e4fede61a54cff7dfde9",
    "obligation-registry.json": "4e0fa630b1284cc79e8c02cb73b6f1e4c2ce69dedf9674e6a9b32a4797775a51",
    "typed-graphs.json": "ced9c0f2a6516be3d1fea8e7421d3b3a00c5d96ed81751461c465dd072025206",
    "ObligationTree.lean": "fb81286bcc0f1cdb673f370dd40264ec940995a175099d418d650fa95d242142",
    "Proof.lean": "fccf2d4b3cafa1cfefc2cd8e6166285e7c7fd89fd78f2cae46908b0fa0e8f339",
    "Validation.lean": "60daacec951fa81161d20a9d028137af1aae1a1c47989d9ca4e3d25ee7fde9a9",
    "proof-receipt.json": "bb42b68276a80de61d7f162ab1cc2e34fcff0fa264c3f209eedcfc353f3bb0e4",
    "proof-blocker.json": "f28427a13439fb96e3e15be061a63dc6ec65c77dbca13c88612207a4571b83fb",
    "validation-spec.json": "e181b7150cc3c2c08e16dec840f00743804cd99351d4d8d13fa2078019291c55",
    "validation-receipt.json": VALIDATION_RECEIPT_SHA256,
    "check_validation.py": "3a9784f5c727a6f1916decf57f717f6d6e12d75196e56477d2e2bcf802b02a41",
    "source-statement-crosswalk.md": "5024d6c477ec2457c9d7dc8ad89f655b339c6ae243bc1d6b982e50c6549f9483",
}
AUTHORITY_INPUTS = {
    "Docs/Stage1_Targets_rev-5.6.json":
        "02eec284de534dd78e1cf75f82a477ff477567dd682b7445cb7587abd137ab2c",
    "Docs/Stage1_Execution_DAG_rev-5.6.json":
        "1f06f20eec06afd4b6f16b2a9f3fc028980a12976cddfafbd44582508e933db4",
    "Docs/Stage1_Blueprint_rev-5.6.md":
        "d9edb70e225b3f79d445026072a2a5cb6a55f69403ba6b9cf990f68cc82f9777",
    "skills/execute-stage1-rev56/SKILL.md":
        "26d47a66c6535feabb8bbf1051fd55d76a53fe761f4b3d953f86b97ec86152b8",
    "Formalizations/Lean/lean-toolchain":
        "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "Formalizations/Lean/lake-manifest.json":
        "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
PROOF_DECLARATIONS = (
    "Stage1Instances.THM_M_1070.isLevyProcess_of_clauses",
    "Stage1Instances.THM_M_1070.clauses_of_isLevyProcess",
    "Stage1Instances.THM_M_1070.isLevyProcess_zero",
    "Stage1Instances.THM_M_1070.zeroMeasure_not_isLevyProcess",
)
STATEMENT_DECLARATION = (
    "Stage1Instances.THM_M_1070.isLevyProcess_iff_expandedSourceShape"
)
ANCHOR_DECLARATIONS = (
    "Stage1Instances.THM_M_1070.AnchorAudit.hasIndepIncrements_iff_finiteFamily",
    "Stage1Instances.THM_M_1070.AnchorAudit.pairwiseConsequence",
)
COMPOSITION_DECLARATIONS = (
    "Stage1Instances.THM_M_1070.isLevyProcess_of_components",
    "Stage1Instances.THM_M_1070.isLevyProcess_iff_components",
)
SUMMARY_LINES = [
    "PASS S56-M-1070-RELEASE negative reconciliation",
    "PASS fresh trust-zero network-isolated replay: exact statement, conditional composition, specialized witness, and countermodel",
    "BLOCKED dependency: S56-M-1070-VALIDATION is provisional and not master-accepted",
    "BLOCKED exact root: the arbitrary-P/arbitrary-X target is unproved and its unconditional reading has a checked zero-measure countermodel",
    "BLOCKED assurance: H0/R0/trust/cold-offline/SBOM/independent-verifier/bundle gates remain open",
    "verdict=blocked lifecycle=planned root_vector=H1/M3/R4 audit_complete=false theorem_complete=false",
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
    output: list[str] = []
    index = 0
    depth = 0
    while index < len(source):
        if depth == 0 and source.startswith("--", index):
            newline = source.find("\n", index)
            if newline < 0:
                break
            output.append("\n")
            index = newline + 1
        elif source.startswith("/-", index):
            depth += 1
            index += 2
        elif depth and source.startswith("-/", index):
            depth -= 1
            index += 2
        elif depth:
            if source[index] == "\n":
                output.append("\n")
            index += 1
        else:
            output.append(source[index])
            index += 1
    assert depth == 0, "unterminated Lean block comment"
    return "".join(output)


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
    blocker = load(HERE / "proof-blocker.json")
    validation = load(HERE / "validation-receipt.json")
    targets = load(ROOT / "Docs" / "Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    for relative, expected in AUTHORITY_INPUTS.items():
        assert sha256(ROOT / relative) == expected, f"authority input drifted: {relative}"

    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target == {
        "execution_rank": 512,
        "legacy_priority_slot": None,
        "theorem_id": THEOREM,
        "name": "Lévy过程",
        "category": "概率论与随机过程 / 随机过程",
        "source_status_untrusted": "已验证",
        "baseline": "L0",
        "rework_required": True,
        "legacy_artifacts_accepted": False,
        "target_lane": "hard_mathlib_anchor_and_wrapper",
        "intake_score": 138,
        "lifecycle_mode": "planned",
        "theorem_complete": False,
    }
    release_item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert release_item == {
        "id": ITEM, "theorem_id": THEOREM, "execution_rank": 512,
        "phase": "release", "layer": 6, "state": "[ ]",
        "depends_on": ["S56-M-1070-VALIDATION"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Reconcile evidence and decide the exact theorem-completion verdict.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0, "children": [],
    }
    validation_item = next(
        row for row in execution["items"] if row["id"] == "S56-M-1070-VALIDATION"
    )
    assert validation_item["state"] == "[_]" and validation_item["attempts"] == 1
    local_release = next(row for row in tasks["tasks"] if row["id"] == ITEM)
    local_validation = next(
        row for row in tasks["tasks"] if row["id"] == "S56-M-1070-VALIDATION"
    )
    assert local_release == {
        "id": ITEM, "depends_on": ["S56-M-1070-VALIDATION"], "state": "open"
    }
    assert local_validation["state"] == "open" and tasks["accepted_states"] == []

    assert decision["reconciled_inputs"] == RECONCILED_INPUTS
    assert decision["authority_inputs"] == AUTHORITY_INPUTS
    for name, expected in RECONCILED_INPUTS.items():
        assert sha256(HERE / name) == expected, f"reconciled input drifted: {name}"

    assert instance["lifecycle"] == tasks["lifecycle"] == "planned"
    assert instance["root_vector"] == VECTOR
    assert instance["accepted_proof_state"] == []
    assert instance["audit_complete"] is instance["theorem_complete"] is False
    formal = statement["canonical_formal_target"]
    assert formal["declaration_or_expression"] == (
        "Stage1Instances.THM_M_1070.IsLevyProcess"
    )
    assert formal["source_sha256"] == RECONCILED_INPUTS["Statement.lean"]
    assert registry["root_obligation_id"] == "M1070-ROOT"
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert [row["obligation_id"] for row in registry["obligations"]] == INVENTORY_IDS
    root_registry = registry["obligations"][0]
    assert root_registry["statement_fingerprint"] == (
        f"lean-expression-sha256:{EXPRESSION_SHA256}"
    )
    assert graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    closure = graphs["closure_boundary"]
    assert closure["root_closed"] is closure["audit_complete"] is False
    assert closure["theorem_complete"] is False
    assert closure["root_machine_debt"] == "M3"
    assert closure["remaining_root_cut_set"] == MATHEMATICAL_CUT
    assert closure["composition_certificates"] == [
        "Stage1Instances.THM_M_1070.isLevyProcess_of_components"
    ]
    root_node = next(row for row in graphs["nodes"] if row["obligation_id"] == "M1070-ROOT")
    assert (root_node["human_debt"], root_node["machine_debt"], root_node["readability_debt"]) == (
        "H1", "M3", "R4",
    )
    assert root_node["evidence_ids"] == []
    for obligation_id in SEMANTIC_LEAVES:
        node = next(row for row in graphs["nodes"] if row["obligation_id"] == obligation_id)
        assert node["machine_debt"] == "M4" and node["evidence_ids"] == []

    assert anchor["root_vector_after"] == VECTOR
    assert anchor["audit_complete"] is anchor["theorem_complete"] is False
    assert anchor["negative_result"].startswith("No full Levy-process declaration")
    external = next(row for row in anchor["candidates"] if row["id"] == "LEANLEVY-IS-LEVY-PROCESS")
    assert external["machine_classification"] == "M3_nonidentical_external_anchor"
    assert external["integration_status"].startswith("not a repository dependency")

    assert proof["support_state"] == "provisional_worker_selftest"
    assert proof["accepted"] is False and proof["verdict"] == "no_state_change"
    assert proof["supported_obligation_ids"] == []
    assert proof["provisionally_closed_obligation_ids"] == []
    assert proof["accepted_closed_obligation_ids"] == []
    assert proof["result"]["root_kernel_closed"] is False
    assert proof["remaining_root_cut_set"] == MATHEMATICAL_CUT
    assert blocker["proof_phase_complete"] is False
    assert blocker["root_closed"] is blocker["theorem_complete"] is False
    assert "zero-measure countermodel" in blocker["blocker"].lower()

    assert validation["receipt_id"] == VALIDATION_RECEIPT_ID
    assert sha256(HERE / "validation-receipt.json") == VALIDATION_RECEIPT_SHA256
    assert validation["support_state"] == "provisional_worker_selftest"
    assert validation["proposed_state"] == "[_]"
    assert validation["accepted"] is validation["release_grade"] is False
    assert validation["verdict"] == "blocked"
    validation_result = validation["result"]
    assert validation_result["root_closed"] is validation_result["root_kernel_closed"] is False
    assert validation_result["accepted_closed_obligation_ids"] == []
    assert validation_result["audit_complete"] is validation_result["theorem_complete"] is False
    assert validation["remaining_root_cut_set"] == MATHEMATICAL_CUT
    assert validation["first_failed_gate"] == (
        "dependency.S56-M-1070-PROOF.master_acceptance_and_exact_root_closure"
    )
    assert validation["first_failed_mathematical_gate"] == "proof.root_kernel_closure"
    assert validation["first_failed_release_gate"] == (
        "S56-10.6-HERMETIC-COLD-EMPTY-CACHE"
    )

    assert decision["schema_version"] == "stage1-release-decision/1.0"
    assert decision["item_id"] == ITEM and decision["theorem_id"] == THEOREM
    assert decision["phase"] == decision["intent"] == "release"
    assert decision["base_revision"] == BASE_REVISION and decision["base_tree"] == BASE_TREE
    assert decision["support_state"] == "provisional_worker_selftest"
    assert decision["proposed_state"] == "[_]" and decision["accepted"] is False
    assert decision["release_grade"] is decision["content_addressed_release_evidence"] is False
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
    assert decision["root_vector"]["before"] == decision["root_vector"]["after"] == VECTOR
    assert decision["terminal_decisions"] == {
        "audit_complete": False, "theorem_complete": False,
        "audit_z": "blocked", "theorem_z": "blocked",
        "release_accepted": False, "master_acceptance": False,
    }
    assert decision["first_failed_gate"]["gate_id"] == "S56-10.2-DEPENDENCY-ACCEPTANCE"
    assert decision["first_failed_gate"]["dependency_gate"] == (
        "dependency.S56-M-1070-VALIDATION.master_acceptance"
    )
    assert decision["first_failed_theorem_gate"]["gate_id"] == "proof.root_kernel_closure"
    assert decision["first_failed_release_gate"]["gate_id"] == (
        "S56-10.6-HERMETIC-COLD-EMPTY-CACHE"
    )
    assert decision["canonical_obligation_ids"] == INVENTORY_IDS
    assert decision["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert decision["statement_fingerprint"] == (
        f"lean-expression-sha256:{EXPRESSION_SHA256}"
    )
    for key in (
        "audit_inventory_reconciliation", "human_source_acceptance",
        "readability_acceptance", "foundation_and_trust_closure",
        "hermetic_release_reproduction", "supply_chain_closure",
        "independent_release_verification", "protected_ci_and_adversarial_gates",
        "deterministic_release_bundle", "master_acceptance",
    ):
        assert decision["evidence_reconciliation"][key].startswith("missing"), key
    assert decision["evidence_reconciliation"]["root_kernel_closure"].startswith("failed")
    cut_text = "\n".join(decision["remaining_root_cut_set"])
    for fragment in (
        "master acceptance", "repair and refreeze", "AUDIT-Z", "accepted H0",
        "accepted R0", "accepted foundation profile", "empty-cache network-denied cold build",
        "SBOM and license", "two signed attestations", "minimal release verifier",
        "deterministic build-twice content-addressed release bundle",
    ):
        assert fragment in cut_text, fragment

    assert spec["schema_version"] == "stage1-release-recipe/1.0"
    assert spec["recipe_id"] == "S56-M-1070-RELEASE-negative-reconciliation-v1"
    assert spec["item_id"] == ITEM and spec["theorem_id"] == THEOREM
    assert spec["argv"] == [
        "python3", "-I", "-B", f"Stage1_Instances/{THEOREM}/check_release.py"
    ]
    assert spec["network_policy"] == "denied" and spec["expected_exit"] == 0
    assert spec["covered_obligation_ids"] == INVENTORY_IDS
    assert receipt["recipe"] == {
        key: spec[key] for key in (
            "recipe_id", "cwd", "argv", "env_allowlist", "timeout_seconds",
            "network_policy", "network_enforcement", "expected_exit",
            "expected_outputs", "covered_obligation_ids", "covered_declarations",
        )
    }

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by|oracle)\b|"
        r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
        r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
        r"(?:axiom|constant|opaque|unsafe|extern)\b",
        re.MULTILINE,
    )
    lean_files = (
        "Statement.lean", "AnchorAudit.lean", "ObligationTree.lean", "Proof.lean",
        "Validation.lean",
    )
    for name in lean_files:
        source = code_without_comments((HERE / name).read_text(encoding="utf-8"))
        assert prohibited.search(source) is None, f"prohibited source token in {name}"
    validation_source = code_without_comments((HERE / "Validation.lean").read_text())
    assert re.search(r"^(?:theorem|lemma|def)\s", validation_source, re.MULTILINE) is None

    manifest = load(LEAN_ROOT / "lake-manifest.json")
    mathlib_entry = next(row for row in manifest["packages"] if row["name"] == "mathlib")
    assert mathlib_entry["rev"] == mathlib_entry["inputRev"] == MATHLIB_REVISION
    assert MATHLIB.resolve().is_dir(), "pinned mathlib artifact is unavailable"
    assert git("rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert git("status", "--porcelain=v1", "--untracked-files=all", cwd=MATHLIB) == ""
    assert git("remote", "get-url", "origin", cwd=MATHLIB) == (
        "https://github.com/leanprover-community/mathlib4.git"
    )
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

    with tempfile.TemporaryDirectory(prefix="stage1-m1070-release-") as tmp_name:
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
                bwrap,
                [lean, "--trust=0", "-o", str(tmp / "ObligationTree.olean"),
                 "ObligationTree.lean"],
                cwd=tmp, env={**common_env, "LEAN_PATH": local_path},
            )
            proof_out = network_isolated(
                bwrap,
                [lean, "--trust=0", "-o", str(tmp / "Proof.olean"), "Proof.lean"],
                cwd=tmp, env={**common_env, "LEAN_PATH": local_path},
            )
            validation_out = network_isolated(
                bwrap, [lean, "--trust=0", "Validation.lean"],
                cwd=tmp, env={**common_env, "LEAN_PATH": local_path},
            )
        finally:
            os.umask(old_umask)

    assert "IsLevyProcess" in statement_out
    for declaration in (*ANCHOR_DECLARATIONS, *COMPOSITION_DECLARATIONS,
                        *PROOF_DECLARATIONS):
        output = anchor_out
        if declaration in COMPOSITION_DECLARATIONS:
            output = obligation_out
        elif declaration in PROOF_DECLARATIONS:
            output = proof_out
        assert printed_axioms(output, declaration) <= ALLOWED_AXIOMS
    for declaration in (STATEMENT_DECLARATION, *PROOF_DECLARATIONS):
        assert declaration in validation_out
    for output in (statement_out, anchor_out, obligation_out, proof_out, validation_out):
        assert "sorryAx" not in output and "declaration uses 'sorry'" not in output
        assert "error:" not in output

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["phase"] == receipt["intent"] == "release"
    assert receipt["depends_on"] == ["S56-M-1070-VALIDATION"]
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
        "dependency.S56-M-1070-VALIDATION.master_acceptance"
    )
    assert receipt["first_failed_theorem_gate"] == "proof.root_kernel_closure"
    assert receipt["first_failed_release_gate"] == "S56-10.6-HERMETIC-COLD-EMPTY-CACHE"
    assert receipt["remaining_root_cut_set"] == decision["remaining_root_cut_set"]
    assert receipt["inputs"]["release_spec_sha256"] == sha256(HERE / "release-spec.json")
    assert receipt["inputs"]["release_decision_sha256"] == sha256(
        HERE / "release-decision.json"
    )
    assert receipt["inputs"]["release_validation_sha256"] == sha256(
        HERE / "release-validation.md"
    )
    assert receipt["inputs"]["check_release_sha256"] == sha256(
        HERE / "check_release.py"
    )
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
    command_rows = packet["commands"]
    assert command_rows[-1] == {
        "argv": ["python3", "-I", "-B", f"Stage1_Instances/{THEOREM}/check_release.py"],
        "exit_code": 0,
        "result": "hash-bound negative release reconciliation and fresh network-isolated trust-zero Lean replay passed",
    }

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
