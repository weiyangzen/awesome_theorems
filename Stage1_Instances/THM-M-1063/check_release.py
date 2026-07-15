#!/usr/bin/env python3
"""Fail-closed release reconciliation for S56-M-1063-RELEASE."""

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
HERE = ROOT / "Stage1_Instances" / "THM-M-1063"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM = "S56-M-1063-RELEASE"
THEOREM = "THM-M-1063"
BASE_REVISION = "b4a28ca0ddecda7bf1bcfb2e0309f6596caf75bf"
BASE_TREE = "2fd84e6cf7daf8b6696416d97e3fbb9576042ba1"
EXPRESSION_SHA256 = "a5bb2e2443661e20f8342ed0dba6b7f7ef5f5ce445bc2d5bbdf19ef5ce842c81"
DENOMINATOR_SHA256 = "a55c3e289a005535836506a2ce233e3dbb5fa0a7b84717b38c221583d26a7703"
VALIDATION_RECEIPT_ID = "S56-M-1063-VALIDATION-network-isolated-20260715-slot22-v1"
VALIDATION_RECEIPT_SHA256 = (
    "b38b181d82d5528d194a1c2be889e64e54d8b6af9226836898994b84b5d6de44"
)
PROOF_RECEIPT_ID = "S56-M-1063-PROOF-worker-20260715T122830+0800"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MATHLIB_REMOTE = "https://github.com/leanprover-community/mathlib4.git"
MATHLIB_LICENSE_SHA256 = (
    "b40930bbcf80744c86c46a12bc9da056641d722716c378f5659b9e555ef833e1"
)
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
LEAN_SHA256 = "3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf"
LAKE_SHA256 = "a608ff084d7e2af228b92a29d7c2fd083ba0580e46889175ec74a81678c98359"
PYTHON_SHA256 = "b8d8288faefdd300201f43fcf00f6f539a27218eeed3a3dff5ab10b9c4c99700"
BASH_SHA256 = "3efccc187bafa75ff1e37d246270ab3e7aa559f242c7a52bf3ec2a1b5450bdbd"
BWRAP_SHA256 = "0abea81db798ebf6b4742ac0664802d97521547a353c2a0dbdc21d76cbbfd2c0"
ALLOWED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
VECTOR = {"H": "H2", "M": "M4", "R": "R4"}
ROOT_CUT = [
    "M1063-L-CLT",
    "M1063-L-MODULUS",
    "M1063-L-ASCOLI",
    "M1063-L-PROKHOROV",
    "M1063-L-LAW-UNIQUE",
    "M1063-T-API",
]
INVENTORY_IDS = [
    "M1063-ROOT", "M1063-S-DEFS", "M1063-S-DOMAINS", "M1063-S-BOUNDARY",
    "M1063-S-FOUNDATION", "M1063-N-STANDARDIZE", "M1063-N-FIDI",
    "M1063-B-FIDI", "M1063-B-TIGHT", "M1063-B-RECOMPOSE", "M1063-C-PATH",
    "M1063-C-MEAS", "M1063-C-TRUNC", "M1063-L-TAIL", "M1063-L-MAX",
    "M1063-L-MODULUS", "M1063-L-ORIGIN", "M1063-L-ASCOLI", "M1063-L-TIGHT",
    "M1063-L-CLT", "M1063-L-COV", "M1063-L-CRAMER", "M1063-L-BROWNIAN-FIDI",
    "M1063-L-PROKHOROV", "M1063-L-EVAL", "M1063-L-LAW-UNIQUE",
    "M1063-T-SEQUENCE", "M1063-T-API", "M1063-X-SCALAR-CLT",
    "M1063-X-SOURCE", "M1063-X-PROVENANCE",
]
MACHINE_IDS = INVENTORY_IDS[:-2]
RECONCILED_INPUTS = {
    "README.md": "de3d16fcc873df28fae98a2930de36af418a737ea7df80f790b79f3cc69118af",
    "instance.json": "5159c0ebfd8ed84904dc76f2afe6e5a7b93b4c05d4f9350d54d155469ae03cdd",
    "task-dag.json": "31c21e8af2a01d6089538037951f37812a2b7e21e49d4378e7a1fd0f12e085cb",
    "statement.json": "a9392798454f8d3a887bd6497b066133b4169fb1a9e1dd07d028f03f461e9ea5",
    "DonskerTarget.lean": "de889c475bd663395eb9385627686109c645ba3446ee513c4019cf82f00a1847",
    "source-statement-crosswalk.md": "0c12a2d4acb7a06e4cb460db8edf6f15f7828c446f35d4083b25bb924dfc3fac",
    "anchor-audit.md": "804833f95f8d9c6c4dbff761189f932405410706a750c3b9faa315be2b12605d",
    "AnchorAudit.lean": "dabce3ddee0e44881a0c36e7c9a5ad2153f2a61773c425fe75f9acbee7cf4e43",
    "obligation-registry.json": "7886d9ce4b1552493476e336bfb5cc1b7537debe8249e61989cdeec86a85d5e8",
    "typed-graphs.json": "e63f2ce6eab9bc6fa942b6e1a412ab0b07063fcc978676daf125779c6a0875b5",
    "ObligationTree.lean": "047c49fd7cefcec9845244077afe72a5cd11d2cbf55022c7b6d307c036991425",
    "Proof.lean": "c854d084d0d3b7d3533f9a8995b3fb81883ccfbe06014cead9871680f128174c",
    "proof-receipt.json": "daa917db3198c92f240f3b1ea53668ae732d252314a5b3d8eea684e6cf2be8a0",
    "proof-blocker.json": "4a47d2ee19bb4fa0a7fa89e22e887f9ff3db6ceffea0bc4477720eb76ef18638",
    "Validation.lean": "3ea9e1da4381d75d1518e22b5ee873908f9ef30d6503e31fda93bd75226241ec",
    "validation-spec.json": "6ddf56007ca92c7832779b4017a26112c3d9efe47743fffaf5366f6fb9345a34",
    "validation-receipt.json": VALIDATION_RECEIPT_SHA256,
    "validation-blocker.json": "6fd49f906187e039dc4fbbd03fa81f7f3ee6662c97d1f44a3628cf4b41fc85ab",
    "check_obligation_tree.py": "7b9c5f8eecd83f065f706130694d7a49d566a9f1214b5fac54f4792fd55b8c42",
    "check_proof.sh": "66ceaa959161e55fe2da1cb530ee88dfb3988fe4904b83b8d1c9b9210ea94263",
    "check_validation.py": "9aa4aa6c67b57c3174a3c3d682dc80e811caf2916622d310da8094eb53434ec7",
}
AUTHORITY_INPUTS = {
    "Docs/Stage1_Targets_rev-5.6.json":
        "02eec284de534dd78e1cf75f82a477ff477567dd682b7445cb7587abd137ab2c",
    "Docs/Stage1_Execution_DAG_rev-5.6.json":
        "f8002b1b20d8a3948a23a78036d3314e6eecf1fcf37e68591eb6e25cc1f6db0b",
    "Docs/Stage1_Blueprint_rev-5.6.md":
        "0564860501fa1b0c440419c788402e7a63bcfec3f1e55658d69656110e512784",
    "Docs/Blueprint_Guidelines.md":
        "a06c07b5ca1b270b4935ad3dab893e9a0e078c29c8da2ef9dca1e71193310535",
    "skills/execute-stage1-rev56/SKILL.md":
        "26d47a66c6535feabb8bbf1051fd55d76a53fe761f4b3d953f86b97ec86152b8",
    "Formalizations/Lean/lean-toolchain":
        "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "Formalizations/Lean/lake-manifest.json":
        "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
PROOF_DECLARATIONS = (
    "AwesomeTheorems.Stage1.THM_M_1063.Proof.standardizedIncrement_package",
    "AwesomeTheorems.Stage1.THM_M_1063.Proof.scalarPartialSums_tendstoInDistribution",
)
SUMMARY_LINES = [
    "PASS S56-M-1063-RELEASE negative reconciliation",
    "PASS current-base network-isolated trust-zero replay: exact target, identity-only root interface, and two partial scalar bodies",
    "BLOCKED dependency: S56-M-1063-VALIDATION is provisional, nonrelease, and not master-accepted",
    "BLOCKED exact root: zero frozen obligations are accepted closed and all 29 required terminal proof-body IDs are null",
    "BLOCKED assurance: H0/R0/trust/clean-cold-offline/SBOM/independent-verifier/bundle gates remain open",
    "verdict=blocked lifecycle=planned root_vector=H2/M4/R4 audit_complete=false theorem_complete=false",
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
            assert key not in result, f"duplicate JSON key in {path}: {key}"
            result[key] = value
        return result

    value = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicates)
    assert isinstance(value, dict), path
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(
    argv: list[str], *, cwd: Path = ROOT, env: dict[str, str] | None = None,
    timeout: int = 900,
) -> str:
    result = subprocess.run(
        argv, cwd=cwd, env=env, text=True, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, timeout=timeout, check=False,
    )
    if result.returncode != 0:
        raise AssertionError(f"command failed ({result.returncode}): {argv!r}\n{result.stdout}")
    return result.stdout


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["/usr/bin/git", *args], cwd=cwd).strip()


def code_without_comments_and_strings(source: str) -> str:
    output: list[str] = []
    depth = 0
    index = 0
    in_string = False
    while index < len(source):
        if not in_string and source.startswith("/-", index):
            depth += 1
            output.extend("  ")
            index += 2
        elif depth and source.startswith("-/", index):
            depth -= 1
            output.extend("  ")
            index += 2
        elif depth:
            output.append("\n" if source[index] == "\n" else " ")
            index += 1
        elif not in_string and source.startswith("--", index):
            end = source.find("\n", index)
            end = len(source) if end < 0 else end
            output.extend(" " * (end - index))
            index = end
        elif source[index] == '"':
            in_string = not in_string
            output.append(" ")
            index += 1
        elif in_string:
            if source[index] == "\\" and index + 1 < len(source):
                output.extend("  ")
                index += 2
            else:
                output.append("\n" if source[index] == "\n" else " ")
                index += 1
        else:
            output.append(source[index])
            index += 1
    assert depth == 0 and not in_string, "unterminated Lean comment or string"
    return "".join(output)


def printed_axioms(output: str, declaration: str) -> set[str]:
    no_axioms = f"'{declaration}' does not depend on any axioms"
    match = re.search(
        re.escape(f"'{declaration}' depends on axioms: [") + r"(.*?)]",
        output, re.DOTALL,
    )
    assert output.count(no_axioms) + (match is not None) == 1, declaration
    if match is None:
        return set()
    return {part.strip() for part in match.group(1).split(",") if part.strip()}


def lean_executable() -> Path:
    toolchain = (LEAN_ROOT / "lean-toolchain").read_text(encoding="utf-8").strip()
    directory = toolchain.replace("/", "--").replace(":", "---")
    return Path.home() / ".elan" / "toolchains" / directory / "bin" / "lean"


def lean_path(lean: Path) -> str:
    roots = sorted(
        path.resolve()
        for path in (LEAN_ROOT / ".lake" / "packages").glob("*/.lake/build/lib/lean")
        if path.is_dir()
    )
    roots.append((LEAN_ROOT / ".lake" / "build" / "lib" / "lean").resolve())
    roots.append((lean.parent.parent / "lib" / "lean").resolve())
    return ":".join(map(str, roots))


def network_isolated_replay(lean: Path) -> dict[str, str]:
    bwrap = Path("/usr/bin/bwrap")
    assert bwrap.is_file()
    path = lean_path(lean)
    names = ("DonskerTarget.lean", "ObligationTree.lean", "Proof.lean")
    with tempfile.TemporaryDirectory(prefix="stage1-m1063-release-") as raw_tmp:
        tmp = Path(raw_tmp)
        for name in names:
            shutil.copy2(HERE / name, tmp / name)
        common = [
            str(bwrap), "--ro-bind", "/", "/", "--bind", str(tmp), str(tmp),
            "--dev", "/dev", "--proc", "/proc", "--unshare-net", "--die-with-parent",
            "--clearenv", "--setenv", "HOME", str(tmp), "--setenv", "LANG", "C.UTF-8",
            "--setenv", "LC_ALL", "C.UTF-8", "--setenv", "TZ", "UTC",
            "--setenv", "LEAN_NUM_THREADS", "1", "--setenv", "LEAN_PATH", path,
            "--chdir", str(tmp), str(lean), "--trust=0", "-t0",
        ]
        old_umask = os.umask(0o022)
        try:
            outputs = {name: run(common + [name], cwd=tmp) for name in names}
        finally:
            os.umask(old_umask)
    return outputs


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
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    proof = load(HERE / "proof-receipt.json")
    blocker = load(HERE / "proof-blocker.json")
    validation = load(HERE / "validation-receipt.json")
    validation_blocker = load(HERE / "validation-blocker.json")
    targets = load(ROOT / "Docs" / "Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    for relative, expected in AUTHORITY_INPUTS.items():
        assert sha256(ROOT / relative) == expected, f"authority input drifted: {relative}"
    for relative, expected in RECONCILED_INPUTS.items():
        assert sha256(HERE / relative) == expected, f"reconciled input drifted: {relative}"
    assert decision["reconciled_inputs"] == RECONCILED_INPUTS
    assert decision["authority_inputs"] == AUTHORITY_INPUTS

    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target == {
        "execution_rank": 506,
        "legacy_priority_slot": None,
        "theorem_id": THEOREM,
        "name": "Donsker不变原理",
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
        "id": ITEM, "theorem_id": THEOREM, "execution_rank": 506,
        "phase": "release", "layer": 6, "state": "[ ]",
        "depends_on": ["S56-M-1063-VALIDATION"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Reconcile evidence and decide the exact theorem-completion verdict.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0, "children": [],
    }
    validation_item = next(
        row for row in execution["items"] if row["id"] == "S56-M-1063-VALIDATION"
    )
    assert validation_item["state"] == "[_]" and validation_item["attempts"] == 1
    local_release = next(row for row in tasks["tasks"] if row["id"] == ITEM)
    assert local_release == {
        "id": ITEM, "depends_on": ["S56-M-1063-VALIDATION"], "state": "open"
    }
    assert tasks["accepted_states"] == [] and tasks["lifecycle"] == "planned"

    assert instance["lifecycle"] == "planned"
    assert instance["root_vector"] == {"H": "H2", "M": "M3", "R": "R4"}
    assert instance["accepted_proof_state"] == []
    assert instance["audit_complete"] is instance["theorem_complete"] is False
    formal = statement["canonical_formal_target"]
    assert formal["declaration_or_expression"] == (
        "AwesomeTheorems.Stage1.THM_M_1063.DonskerInvariancePrinciple"
    )
    assert formal["statement_file_sha256"] == RECONCILED_INPUTS["DonskerTarget.lean"]
    assert statement["statement_elaborated"] is True
    assert statement["theorem_proved"] is statement["theorem_complete"] is False

    assert registry["root_obligation_id"] == "M1063-ROOT"
    assert [row["obligation_id"] for row in registry["obligations"]] == INVENTORY_IDS
    assert registry["frozen_denominators"]["inventory"] == INVENTORY_IDS
    assert registry["frozen_denominators"]["required_machine"] == MACHINE_IDS
    for row in registry["obligations"]:
        assert row["terminal_proof_body_id"] is None, row["obligation_id"]
    root_registry = registry["obligations"][0]
    assert root_registry["statement_fingerprint"] == (
        f"lean-expression-sha256:{EXPRESSION_SHA256}"
    )

    assert graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert len(graphs["nodes"]) == len(INVENTORY_IDS)
    assert sum(len(graph["edges"]) for graph in graphs["graphs"].values()) == 125
    assert len(graphs["graphs"]["evidence"]["edges"]) == 0
    closure = graphs["closure_boundary"]
    assert closure == {
        "closed_obligations": [], "root_closed": False, "root_machine_debt": "M4",
        "audit_complete": False, "theorem_complete": False,
        "remaining_root_cut_set": ROOT_CUT,
    }
    root_node = next(row for row in graphs["nodes"] if row["obligation_id"] == "M1063-ROOT")
    assert (root_node["human_debt"], root_node["machine_debt"], root_node["readability_debt"]) == (
        "H2", "M4", "R4",
    )
    assert root_node["evidence_ids"] == []
    composition = graphs["composition_certificates"]
    assert composition == [{
        "certificate_id": "COMP-M1063-ROOT-IDENTITY-V1",
        "parent": "M1063-ROOT", "required_children": ["M1063-B-RECOMPOSE"],
        "checked_declaration": (
            "AwesomeTheorems.Stage1.THM_M_1063.ObligationTree.exactRoot_of_exactRoot"
        ),
        "status": "exact-root identity interface kernel-checked; substantive child composition remains open",
    }]

    assert proof["receipt_id"] == PROOF_RECEIPT_ID
    assert proof["support_state"] == "provisional_worker_selftest"
    assert proof["accepted"] is False and proof["verdict"] == "no_state_change"
    assert proof["supported_obligation_ids"] == []
    assert proof["provisionally_closed_obligation_ids"] == []
    assert proof["accepted_closed_obligation_ids"] == []
    assert proof["result"]["root_kernel_closed"] is False
    assert proof["result"]["proof_phase_complete"] is False
    assert proof["remaining_root_cut_set"] == ROOT_CUT
    assert blocker["proof_phase_complete"] is False
    assert blocker["root_closed"] is blocker["theorem_complete"] is False

    assert validation["receipt_id"] == VALIDATION_RECEIPT_ID
    assert sha256(HERE / "validation-receipt.json") == VALIDATION_RECEIPT_SHA256
    assert validation["support_state"] == "provisional_worker_selftest"
    assert validation["proposed_state"] == "[_]"
    assert validation["accepted"] is validation["release_grade"] is False
    assert validation["verdict"] == "blocked"
    assert validation["accepted_closed_obligation_ids"] == []
    result = validation["result"]
    assert result["root_kernel_closed"] is result["validation_complete"] is False
    assert result["audit_complete"] is result["theorem_complete"] is False
    assert validation["root_vector_before"] == validation["root_vector_after"] == VECTOR
    assert validation["remaining_root_cut_set"] == ROOT_CUT
    assert validation["first_failed_gate"] == (
        "dependency.S56-M-1063-PROOF.master_acceptance_and_exact_root_closure"
    )
    assert validation_blocker["closed_obligation_ids"] == []
    assert validation_blocker["required_machine_obligation_count"] == len(MACHINE_IDS)
    assert validation_blocker["required_terminal_proof_body_ids_present"] == 0
    assert validation_blocker["root_closed"] is validation_blocker["theorem_complete"] is False

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
        "dependency.S56-M-1063-VALIDATION.master_acceptance"
    )
    assert decision["first_failed_theorem_gate"]["gate_id"] == "M1063-C-PATH"
    assert decision["first_failed_release_gate"]["gate_id"] == (
        "S56-10.6-IMMUTABLE-CLEAN-INPUT"
    )
    assert decision["canonical_obligation_ids"] == INVENTORY_IDS
    assert decision["machine_required_obligation_ids"] == MACHINE_IDS
    assert decision["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert decision["statement_fingerprint"] == f"lean-expression-sha256:{EXPRESSION_SHA256}"
    for key in (
        "audit_inventory_reconciliation", "human_source_acceptance",
        "readability_acceptance", "statement_mutation_evidence",
        "foundation_and_trust_closure", "hermetic_release_reproduction",
        "supply_chain_closure", "independent_release_verification",
        "protected_ci_and_adversarial_gates", "deterministic_release_bundle",
        "master_acceptance",
    ):
        assert decision["evidence_reconciliation"][key].startswith("missing"), key
    assert decision["evidence_reconciliation"]["root_kernel_closure"].startswith("failed")
    cut_text = "\n".join(decision["remaining_root_cut_set"])
    for fragment in (
        "master acceptance", "29 machine-required obligations", "six frozen root-cut",
        "AUDIT-Z", "accepted H0", "accepted R0", "accepted foundation profile",
        "empty-cache network-denied cold build", "SBOM and license", "two signed attestations",
        "minimal release verifier", "deterministic build-twice content-addressed release bundle",
    ):
        assert fragment in cut_text, fragment

    assert spec["schema_version"] == "stage1-release-recipe/1.0"
    assert spec["recipe_id"] == "S56-M-1063-RELEASE-negative-reconciliation-v1"
    assert spec["item_id"] == ITEM and spec["theorem_id"] == THEOREM
    assert spec["argv"] == [
        "/usr/bin/python3", "-I", "-B", f"Stage1_Instances/{THEOREM}/check_release.py"
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
        r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by|run_tac|oracle)\b|"
        r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
        r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
        r"(?:axiom|constant|opaque|unsafe|extern)\b",
        re.MULTILINE,
    )
    lean_files = (
        "DonskerTarget.lean", "AnchorAudit.lean", "ObligationTree.lean", "Proof.lean",
        "Validation.lean",
    )
    for name in lean_files:
        source = code_without_comments_and_strings((HERE / name).read_text(encoding="utf-8"))
        assert prohibited.search(source) is None, f"prohibited source token in {name}"

    manifest = load(LEAN_ROOT / "lake-manifest.json")
    mathlib_entry = next(row for row in manifest["packages"] if row["name"] == "mathlib")
    assert mathlib_entry["rev"] == mathlib_entry["inputRev"] == MATHLIB_REVISION
    assert MATHLIB.resolve().is_dir(), "pinned mathlib artifact is unavailable"
    assert git("rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert git("status", "--porcelain=v1", "--untracked-files=all", cwd=MATHLIB) == ""
    assert git("remote", "get-url", "origin", cwd=MATHLIB) == MATHLIB_REMOTE
    assert sha256(MATHLIB / "LICENSE") == MATHLIB_LICENSE_SHA256

    lean = lean_executable()
    lake = lean.parent / "lake"
    assert lean.is_file() and lake.is_file()
    assert sha256(lean) == LEAN_SHA256 and sha256(lake) == LAKE_SHA256
    assert sha256(Path("/usr/bin/python3")) == PYTHON_SHA256
    assert sha256(Path("/usr/bin/bash")) == BASH_SHA256
    assert sha256(Path("/usr/bin/bwrap")) == BWRAP_SHA256
    lean_version = run([str(lean), "--version"])
    lake_version = run([str(lake), "--version"])
    assert "4.29.0" in lean_version and LEAN_COMMIT in lean_version
    assert "5.0.0-src+98dc76e" in lake_version

    outputs = network_isolated_replay(lean)
    assert "DonskerInvariancePrinciple" in outputs["DonskerTarget.lean"]
    assert "exactRoot_of_exactRoot" in outputs["ObligationTree.lean"]
    for declaration in PROOF_DECLARATIONS:
        assert printed_axioms(outputs["Proof.lean"], declaration) == ALLOWED_AXIOMS
    combined = "\n".join(outputs.values())
    assert "sorryAx" not in combined and "declaration uses 'sorry'" not in combined
    assert not re.search(r"(^|\n).*error(?:\([^)]*\))?:", combined)

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["phase"] == receipt["intent"] == "release"
    assert receipt["depends_on"] == ["S56-M-1063-VALIDATION"]
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["release_grade"] is receipt["content_addressed_release_evidence"] is False
    assert receipt["result"]["verdict"] == "blocked"
    assert receipt["result"]["audit_complete"] is receipt["result"]["theorem_complete"] is False
    assert receipt["root_vector_before"] == receipt["root_vector_after_worker_selftest"] == VECTOR
    assert receipt["accepted_receipt_ids"] == []
    assert receipt["first_failed_gate"] == "S56-10.2-DEPENDENCY-ACCEPTANCE"
    assert receipt["first_failed_dependency_gate"] == (
        "dependency.S56-M-1063-VALIDATION.master_acceptance"
    )
    assert receipt["first_failed_theorem_gate"] == "M1063-C-PATH"
    assert receipt["first_failed_release_gate"] == "S56-10.6-IMMUTABLE-CLEAN-INPUT"
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
    assert packet["commands"][-1] == {
        "argv": [
            "/usr/bin/python3", "-I", "-B",
            f"Stage1_Instances/{THEOREM}/check_release.py",
        ],
        "exit_code": 0,
        "result": "hash-bound negative release reconciliation and fresh network-isolated trust-zero Lean replay passed",
    }

    status = git("status", "--short", "--untracked-files=all")
    actual_changed = {
        line[3:] for line in status.splitlines() if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual_changed == CHANGED_PATHS, (actual_changed, CHANGED_PATHS)
    for relative in CHANGED_PATHS:
        assert_text_hygiene(ROOT / relative)

    obligation_output = run([
        "/usr/bin/python3", "-B", f"Stage1_Instances/{THEOREM}/check_obligation_tree.py"
    ])
    assert "31 obligations, 125 typed edges" in obligation_output
    assert "root closure: open (M4)" in obligation_output
    public = "\n".join(
        (HERE / name).read_text(encoding="utf-8")
        for name in ("release-decision.json", "release-validation.md")
    )
    assert "/home/" not in public and ".cron/" not in public

    for line in SUMMARY_LINES:
        print(line)


if __name__ == "__main__":
    main()
