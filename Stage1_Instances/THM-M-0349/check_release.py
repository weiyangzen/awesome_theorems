#!/usr/bin/env python3
"""Fail-closed release reconciliation for S56-M-0349-RELEASE."""

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
HERE = ROOT / "Stage1_Instances" / "THM-M-0349"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
ITEM = "S56-M-0349-RELEASE"
THEOREM = "THM-M-0349"
BASE_REVISION = "350285c48208616b6e3ad74154d9183d16523cfa"
BASE_TREE = "c4edebc115ec954e4940ed5faaa3ffacd4e56091"
VALIDATION_BASE = "d5ab961cb3cd92c7febcf21fb9ab746fde231c24"
VALIDATION_TREE = "5f3d5abbfee8a0f11198a295ecf024aca301867f"
TOOLCHAIN = "leanprover/lean4:v4.29.0"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MATHLIB_ORIGIN = "https://github.com/leanprover-community/mathlib4.git"
MATHLIB_LICENSE_SHA256 = "b40930bbcf80744c86c46a12bc9da056641d722716c378f5659b9e555ef833e1"
EXPRESSION_SHA256 = "5f80bebbbf59938add2cb517d6b6219f7a7a22ad8f09586d01e508db2e2ac908"
DENOMINATOR_SHA256 = "559befd6c5ac888249539d74acc96e0a274afa52e3b2e0683c05dc010cd3185d"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
FROZEN_ROOT_CUT = ["M0349-P-EXISTENCE", "M0349-P-BOUND"]
EXPANDED_OPEN_DEBT = [
    "M0349-L-WEAK11",
    "M0349-L-INTERPOLATE",
    "M0349-C-EXTEND",
    "M0349-L-FOURIER-ID",
    "M0349-P-EXISTENCE",
    "M0349-P-BOUND",
]
PARTIAL_IDS = ["M0349-C-POLYNOMIAL", "M0349-L-L2"]
INVENTORY_IDS = [
    "M0349-ROOT",
    "M0349-T-ASSEMBLE",
    "M0349-P-EXISTENCE",
    "M0349-P-BOUND",
    "M0349-D-DENSE",
    "M0349-C-POLYNOMIAL",
    "M0349-L-WEAK11",
    "M0349-L-L2",
    "M0349-L-INTERPOLATE",
    "M0349-C-EXTEND",
    "M0349-L-FOURIER-ID",
    "M0349-S-ENDPOINTS",
    "M0349-X-SOURCE",
    "M0349-X-TRUST",
    "M0349-X-PROVENANCE",
]
EXPECTED_INPUTS = {
    "Statement.lean": "c548991ce6ec39da14646f359edea6ad3b53e31dc71e27c4b90345b034afcf62",
    "ObligationTree.lean": "2c08dcdbe1871a1c3c3613aacb31b9fea6a05e59b6c0eb03da9781875be28ff7",
    "Proof.lean": "a7bbea29d7ebeaadcee60e352d1294617f3a8f46e4b4adc3142041ef15517942",
    "Validation.lean": "802f05d6665c8d6d044520da844382169aa610368e568b991f55040226c18808",
    "instance.json": "2593850ad0812654e4afbf28beb9252814d54c9fd355ce066e9a34ef09ed73ff",
    "task-dag.json": "fd94e3999832a9c9c3029af559c11326203c1da043501949987f12b907d9c42f",
    "source-statement-crosswalk.md": "2e4c2d79dd7c0ddfa9337df26368545a1fb267a3a51b64223086de78e8754d52",
    "anchor-audit.json": "f08d1cf12c010c556b2dd03c5d689493b403edfb7b81ccfc413bdac4fa27d820",
    "obligation-registry.json": "ae975d9ff9ea0432de87cf6b5794463ba81ac4057eaba42dbcf456506328bfe7",
    "typed-graphs.json": "1cd55ee81552085c965ffa43cea205b1e7f0e21c38c296eca043bf6b906cbad8",
    "proof-receipt.json": "6bd1042271f4a19fa3e2f0717b88f1c61ca5305d490ed8095d5e0ccd95c66cb1",
    "proof-blocker.json": "1a2d8ff322dc7eb1f709edae9699ea03bf61803ea4af2acca7f5147662e5391d",
    "validation-spec.json": "42503fd8f0af44c6dd7d40aa2023a4e6803ec4304bd69985f36afabc97ce1aba",
    "validation-receipt.json": "667c93b1f471aae2e68856161c5a27534f249071e138aba53894342df955ef07",
    "validation-blocker.json": "a4f0796d18f1b827062c816de8fceb42f260c43e6dfbab3f505d5a63b2fc18ae",
    "check_validation.py": "0c60927e8d02766359622c65dd09f6857b5575ff4d49404b11af27833d909695",
}
EXPECTED_AUTHORITY_INPUTS = {
    "Docs/Stage1_Blueprint_rev-5.6.md": "6640881cb112fdd384daa1a016588ca4b4c254d8237e92fcc34b40f3d0557942",
    "Docs/Stage1_Targets_rev-5.6.json": "02eec284de534dd78e1cf75f82a477ff477567dd682b7445cb7587abd137ab2c",
    "Docs/Stage1_Execution_DAG_rev-5.6.json": "27996ce44b0352923f10f0150728d7db409b5f928d4aaf36ff1f69ce29ee4320",
    "Docs/Blueprint_Guidelines.md": "a06c07b5ca1b270b4935ad3dab893e9a0e078c29c8da2ef9dca1e71193310535",
    "skills/execute-stage1-rev56/SKILL.md": "26d47a66c6535feabb8bbf1051fd55d76a53fe761f4b3d953f86b97ec86152b8",
    "Formalizations/Lean/lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "Formalizations/Lean/lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
RELEASE_OUTPUT_NAMES = (
    "release-spec.json",
    "release-decision.json",
    "release-receipt.json",
    "release-validation.md",
)
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/check_release.py",
    *(f"Stage1_Instances/{THEOREM}/{name}" for name in RELEASE_OUTPUT_NAMES),
}
SUMMARY_LINES = [
    "PASS release reconciliation: current target, DAG, receipts, registry, graphs, and hashes agree",
    "PASS narrow Lean replay: exact statement, L2 candidate, and conditional root checked at trust zero",
    "BLOCKED S56-10.2-DEPENDENCY-ACCEPTANCE: validation is provisional and not master accepted",
    "BLOCKED exact root: H3/M4/R4 unchanged; zero frozen obligations accepted closed",
    "BLOCKED AUDIT-Z and THEOREM-Z: source/readability, trust, cold hermetic, and independent gates are open",
    "verdict=blocked audit_complete=false theorem_complete=false accepted_receipts=0",
]


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
    argv: list[str], *, cwd: Path = ROOT, timeout: int = 600,
    env: dict[str, str] | None = None, check: bool = True,
) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        argv, cwd=cwd, env=env, text=True, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, timeout=timeout, check=False,
    )
    if check and result.returncode != 0:
        raise RuntimeError(f"command failed ({result.returncode}): {argv!r}\n{result.stdout}")
    return result


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["git", *args], cwd=cwd, timeout=60).stdout.strip()


def source_without_comments_and_strings(source: str) -> str:
    output: list[str] = []
    index = 0
    depth = 0
    in_string = False
    escaped = False
    while index < len(source):
        pair = source[index:index + 2]
        char = source[index]
        if depth:
            if pair == "/-":
                depth += 1
                output.extend("  ")
                index += 2
            elif pair == "-/":
                depth -= 1
                output.extend("  ")
                index += 2
            else:
                output.append("\n" if char == "\n" else " ")
                index += 1
        elif in_string:
            output.append("\n" if char == "\n" else " ")
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
            index += 1
        elif pair == "/-":
            depth = 1
            output.extend("  ")
            index += 2
        elif pair == "--":
            newline = source.find("\n", index)
            if newline < 0:
                output.extend(" " * (len(source) - index))
                index = len(source)
            else:
                output.extend(" " * (newline - index))
                index = newline
        elif char == '"':
            in_string = True
            output.append(" ")
            index += 1
        else:
            output.append(char)
            index += 1
    assert depth == 0 and not in_string
    return "".join(output)


def reported_axioms(output: str, declaration: str) -> set[str]:
    match = re.search(
        rf"'{re.escape(declaration)}' depends on axioms:\s*\[(?P<axioms>.*?)]",
        output,
        re.DOTALL,
    )
    assert match is not None, f"missing axiom report for {declaration}"
    return {part.strip() for part in match.group("axioms").split(",") if part.strip()}


def assert_text_hygiene(path: Path) -> None:
    data = path.read_bytes()
    assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())


def historical_validation_integrity(receipt: dict) -> None:
    assert receipt["base_revision"] == VALIDATION_BASE
    assert receipt["base_tree"] == VALIDATION_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]"
    assert receipt["accepted"] is receipt["release_grade"] is False
    assert receipt["verdict"] == "blocked"
    assert receipt["accepted_receipt_ids"] == []
    assert receipt["root_vector_before"] == receipt["root_vector_after"] == {
        "H": "H3", "M": "M4", "R": "R4"
    }
    result = receipt["result"]
    assert result["supported_obligation_ids"] == []
    assert result["accepted_closed_obligation_ids"] == []
    assert result["root_closed"] is result["root_kernel_closed"] is False
    assert result["root_machine_debt"] == "M4"
    assert result["frozen_graph_minimal_open_root_cut"] == FROZEN_ROOT_CUT
    assert result["expanded_open_root_debt"] == EXPANDED_OPEN_DEBT
    assert result["audit_complete"] is result["theorem_complete"] is False
    assert receipt["hermeticity"]["decision"].startswith("fail_closed")
    assert receipt["independent_validation"]["decision"] == "fail_closed"


def historical_validation_stale_probe() -> None:
    result = run(
        [
            "/usr/bin/python3", "-I", "-B",
            f"Stage1_Instances/{THEOREM}/check_validation.py", "--probe",
        ],
        timeout=60,
        check=False,
    )
    assert result.returncode == 1
    assert "AssertionError" in result.stdout
    assert f'BASE_REVISION = "{VALIDATION_BASE}"' in (HERE / "check_validation.py").read_text()


def narrow_lean_replay() -> dict[str, object]:
    bwrap = Path(shutil.which("bwrap") or "")
    assert bwrap.is_file(), "bubblewrap is required for network-denied replay"
    fixed_env = os.environ.copy()
    fixed_env.pop("LEAN_PATH", None)
    fixed_env.update({
        "ELAN_TOOLCHAIN": TOOLCHAIN,
        "LANG": "C.UTF-8",
        "LC_ALL": "C.UTF-8",
        "TZ": "UTC",
        "LEAN_NUM_THREADS": "1",
    })
    lean = Path(run(
        ["lake", "env", "which", "lean"], cwd=LEAN_ROOT, env=fixed_env, timeout=120
    ).stdout.strip())
    lean_path = run(
        ["lake", "env", "printenv", "LEAN_PATH"], cwd=LEAN_ROOT,
        env=fixed_env, timeout=120,
    ).stdout.strip()
    assert lean.is_file() and LEAN_COMMIT in run([str(lean), "--version"]).stdout

    with tempfile.TemporaryDirectory(prefix="stage1-m0349-release-", dir="/tmp") as name:
        tmp = Path(name).resolve()
        (tmp / "home").mkdir()
        for source in ("Statement.lean", "Proof.lean", "ObligationTree.lean", "Validation.lean"):
            shutil.copy2(HERE / source, tmp / source)
        base = [
            str(bwrap), "--ro-bind", "/", "/", "--bind", str(tmp), str(tmp),
            "--dev", "/dev", "--proc", "/proc", "--unshare-net",
            "--die-with-parent", "--clearenv", "--setenv", "HOME", str(tmp / "home"),
            "--setenv", "LANG", "C.UTF-8", "--setenv", "LC_ALL", "C.UTF-8",
            "--setenv", "TZ", "UTC", "--setenv", "LEAN_NUM_THREADS", "1",
            "--chdir", str(tmp),
        ]

        def lean_run(source: str, module_path: str, emit_olean: bool) -> str:
            argv = base + [
                "--setenv", "LEAN_PATH", module_path, str(lean), "--trust=0", "-t0",
            ]
            if emit_olean:
                argv += ["-o", source.replace(".lean", ".olean")]
            argv.append(source)
            return run(argv, env=fixed_env).stdout

        outputs = {
            "statement": lean_run("Statement.lean", lean_path, True),
            "proof": lean_run("Proof.lean", f"{tmp}:{lean_path}", True),
            "obligation_tree": lean_run("ObligationTree.lean", f"{tmp}:{lean_path}", True),
            "validation": lean_run("Validation.lean", f"{tmp}:{lean_path}", False),
        }

    combined = "\n".join(outputs.values())
    assert "sorryAx" not in combined and "error:" not in combined
    for declaration in (
        "Stage1Instances.THM_M_0349.conjugate_l2_bound",
        "Stage1Instances.THM_M_0349.root_of_conjugate_packages",
    ):
        assert reported_axioms(outputs["validation"], declaration) == EXPECTED_AXIOMS
    closure = re.search(
        r"VALIDATION_CLOSURE declarations=(\d+) modules=(\d+)", outputs["validation"]
    )
    assert closure is not None
    assert "VALIDATION_CLOSURE unexpected_bodyless=[]" in outputs["validation"]
    assert "VALIDATION_CLOSURE unsafe=[]" in outputs["validation"]
    return {
        "output_sha256": {
            key: hashlib.sha256(value.encode()).hexdigest()
            for key, value in outputs.items()
        },
        "closure_declarations": int(closure.group(1)),
        "closure_modules": int(closure.group(2)),
    }


def main() -> None:
    if sys.flags.optimize != 0:
        raise RuntimeError("release checker requires Python assertions")

    decision = load(HERE / "release-decision.json")
    receipt = load(HERE / "release-receipt.json")
    spec = load(HERE / "release-spec.json")
    validation = load(HERE / "validation-receipt.json")
    proof = load(HERE / "proof-receipt.json")
    instance = load(HERE / "instance.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    local_tasks = load(HERE / "task-dag.json")
    targets = load(ROOT / "Docs" / "Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 842 and target["baseline"] == "L0"
    assert target["lifecycle_mode"] == "planned"
    assert target["rework_required"] is True and target["theorem_complete"] is False
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item == {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 842,
        "phase": "release",
        "layer": 6,
        "state": "[ ]",
        "depends_on": ["S56-M-0349-VALIDATION"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Reconcile evidence and decide the exact theorem-completion verdict.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }
    predecessor = next(
        row for row in execution["items"] if row["id"] == "S56-M-0349-VALIDATION"
    )
    assert predecessor["state"] == "[_]" and predecessor["attempts"] == 1

    for name, expected in EXPECTED_INPUTS.items():
        assert sha256(HERE / name) == expected, f"reconciled input drifted: {name}"
    for relative, expected in EXPECTED_AUTHORITY_INPUTS.items():
        assert sha256(ROOT / relative) == expected, f"authority input drifted: {relative}"
    assert decision["reconciled_inputs"] == EXPECTED_INPUTS
    assert decision["authority_inputs"] == EXPECTED_AUTHORITY_INPUTS

    formal = instance["canonical_formal_target"]
    assert formal["elaborated_expression_hash"] == f"sha256:{EXPRESSION_SHA256}"
    assert registry["root_obligation_id"] == graphs["root_node_id"] == "M0349-ROOT"
    assert [row["obligation_id"] for row in registry["obligations"]] == INVENTORY_IDS
    assert registry["denominator_sha256"] == graphs["registry_denominator_sha256"]
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert graphs["closure_boundary"] == {
        "root_closed": False,
        "theorem_complete": False,
        "minimal_open_root_cut": FROZEN_ROOT_CUT,
    }
    graph_root = next(row for row in graphs["nodes"] if row["obligation_id"] == "M0349-ROOT")
    assert [
        graph_root["human_debt"], graph_root["machine_debt"],
        graph_root["readability_debt"],
    ] == ["H3", "M3", "R4"]
    assert instance["root_vector"] == {"H": "H3", "M": "M4", "R": "R4"}
    l2_registry = next(row for row in registry["obligations"] if row["obligation_id"] == "M0349-L-L2")
    l2_graph = next(row for row in graphs["nodes"] if row["obligation_id"] == "M0349-L-L2")
    assert l2_registry["terminal_proof_body_id"] is None
    assert l2_graph["formal_target"] == "planned exact L2 estimate"
    assert l2_graph["owned_sources"] == l2_graph["evidence_ids"] == []
    assert proof["accepted"] is False
    assert proof["partial_progress_toward_obligation_ids"] == PARTIAL_IDS
    assert proof["supported_obligation_ids"] == proof["accepted_closed_obligation_ids"] == []
    assert proof["result"]["root_kernel_closed"] is False
    assert proof["result"]["theorem_complete"] is False
    historical_validation_integrity(validation)
    local_by_id = {row["id"]: row for row in local_tasks["tasks"]}
    for task_id in ("S56-M-0349-PROOF", "S56-M-0349-VALIDATION", ITEM):
        assert local_by_id[task_id]["state"] == "open"

    lake_link = LEAN_ROOT / ".lake"
    assert lake_link.is_symlink()
    mathlib = lake_link / "packages" / "mathlib"
    assert mathlib.is_dir()
    assert git("rev-parse", "HEAD", cwd=mathlib) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == MATHLIB_TREE
    assert git("status", "--porcelain=v1", "--untracked-files=all", cwd=mathlib) == ""
    assert git("remote", "get-url", "origin", cwd=mathlib) == MATHLIB_ORIGIN
    assert sha256(mathlib / "LICENSE") == MATHLIB_LICENSE_SHA256

    dependency = decision["dependency"]
    assert dependency["item_id"] == validation["item_id"] == "S56-M-0349-VALIDATION"
    assert dependency["receipt_id"] == validation["receipt_id"]
    assert dependency["receipt_sha256"] == sha256(HERE / "validation-receipt.json")
    assert dependency["support_state"] == validation["support_state"]
    assert dependency["accepted"] is dependency["release_grade"] is False
    assert dependency["master_accepted"] is False
    assert dependency["historical_recipe_currently_replayable"] is False
    assert dependency["historical_recipe_probe_exit"] == 1
    historical_validation_stale_probe()

    result = decision["decision"]
    assert decision["item_id"] == ITEM and decision["theorem_id"] == THEOREM
    assert decision["base_revision"] == BASE_REVISION and decision["base_tree"] == BASE_TREE
    assert decision["proposed_state"] == "[_]"
    assert decision["accepted"] is decision["release_grade"] is False
    assert decision["accepted_receipt_ids"] == []
    assert result["verdict"] == "blocked"
    assert result["lifecycle_before"] == result["lifecycle_after"] == "planned"
    assert result["root_vector_before"] == result["root_vector_after"] == ["H3", "M4", "R4"]
    assert result["audit_complete"] is result["theorem_complete"] is False
    assert result["audit_z"] == result["theorem_z"] == "blocked"
    assert result["release_accepted"] is False
    assert result["first_failed_gate"]["gate_id"] == "S56-10.2-DEPENDENCY-ACCEPTANCE"
    assert result["first_failed_audit_gate"]["gate_id"] == (
        "S56-AUDIT-FROZEN-INVENTORY-SOURCE-BOUNDARY-RECONCILIATION"
    )
    assert result["first_failed_theorem_gate"]["gate_id"] == (
        "S56-THEOREM-EXACT-ROOT-KERNEL-CLOSURE"
    )
    assert result["first_failed_release_specific_gate"]["gate_id"] == (
        "S56-RELEASE-IMMUTABLE-CLEAN-INPUT"
    )
    assert result["next_failed_release_gate"]["gate_id"] == "S56-10.6-HERMETIC-COLD-BUILD"
    assert result["remaining_root_cut_set"] == EXPANDED_OPEN_DEBT
    disagreement = decision["authority_disagreement"]
    assert disagreement["instance_manifest_root_vector"] == ["H3", "M4", "R4"]
    assert disagreement["typed_graph_root_vector"] == ["H3", "M3", "R4"]
    assert disagreement["conservative_release_vector"] == ["H3", "M4", "R4"]
    assert disagreement["reconciled"] is False
    reconciliation = decision["evidence_reconciliation"]
    assert reconciliation["validated_partial_progress_toward_obligations"] == PARTIAL_IDS
    assert reconciliation["accepted_closed_obligations"] == []
    for key in (
        "accepted_exact_root_kernel_closure",
        "audit_z_accepted",
        "pinpoint_h0_review",
        "independent_r0_review",
        "complete_provenance_foundation_tcb_closure",
        "immutable_clean_release_input",
        "hermetic_cold_offline_replay",
        "sbom_license_archive_closure",
        "independent_clean_runner_attestations",
        "independently_implemented_minimal_verifier",
        "protected_ci_and_adversarial_gates",
        "deterministic_release_bundle",
        "master_acceptance",
    ):
        assert reconciliation[key] is False, key

    assert spec["schema_version"] == "stage1-validation-recipe/1.0"
    assert spec["item_id"] == ITEM and spec["theorem_id"] == THEOREM
    assert spec["argv"] == [
        "python3", "-I", "-B", f"Stage1_Instances/{THEOREM}/check_release.py"
    ]
    assert spec["cwd"] == "." and spec["timeout_seconds"] == 600
    assert spec["network_policy"] == "denied" and spec["expected_exit"] == 0
    assert spec["covered_obligation_ids"] == INVENTORY_IDS
    assert spec["covered_decisions"] == ["AUDIT-Z", "THEOREM-Z"]

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["phase"] == receipt["intent"] == "release"
    assert receipt["depends_on"] == ["S56-M-0349-VALIDATION"]
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]"
    assert receipt["accepted"] is receipt["release_grade"] is False
    assert receipt["content_addressed_release_evidence"] is receipt["master_accepted"] is False
    assert receipt["decision_id"] == decision["decision_id"]
    assert receipt["accepted_receipt_ids"] == []
    assert receipt["canonical_obligation_ids"] == INVENTORY_IDS
    assert receipt["result"]["verdict"] == "blocked"
    assert receipt["result"]["accepted_closed_obligations"] == []
    assert receipt["result"]["accepted_root_closed"] is False
    assert receipt["result"]["audit_complete"] is receipt["result"]["theorem_complete"] is False
    assert receipt["result"]["root_vector_before"] == receipt["result"]["root_vector_after"] == [
        "H3", "M4", "R4"
    ]
    assert receipt["result"]["remaining_root_cut_set"] == EXPANDED_OPEN_DEBT
    assert receipt["result"]["first_failed_gate"] == "S56-10.2-DEPENDENCY-ACCEPTANCE"
    assert receipt["result"]["first_failed_audit_gate"] == (
        "S56-AUDIT-FROZEN-INVENTORY-SOURCE-BOUNDARY-RECONCILIATION"
    )
    assert receipt["result"]["first_failed_theorem_gate"] == (
        "S56-THEOREM-EXACT-ROOT-KERNEL-CLOSURE"
    )
    assert receipt["result"]["first_failed_release_specific_gate"] == (
        "S56-RELEASE-IMMUTABLE-CLEAN-INPUT"
    )
    expected_bindings = {
        **{
            f"Stage1_Instances/{THEOREM}/{name}": digest
            for name, digest in EXPECTED_INPUTS.items()
        },
        **EXPECTED_AUTHORITY_INPUTS,
    }
    assert receipt["input_bindings"] == expected_bindings
    for relative, expected in expected_bindings.items():
        assert sha256(ROOT / relative) == expected, f"receipt input drifted: {relative}"
    assert receipt["release_output_bindings"] == {
        f"Stage1_Instances/{THEOREM}/release-spec.json": sha256(HERE / "release-spec.json"),
        f"Stage1_Instances/{THEOREM}/release-decision.json": sha256(HERE / "release-decision.json"),
        f"Stage1_Instances/{THEOREM}/release-validation.md": sha256(HERE / "release-validation.md"),
        f"Stage1_Instances/{THEOREM}/check_release.py": sha256(Path(__file__).resolve()),
    }
    for key in (
        "recipe_id", "cwd", "argv", "env_allowlist", "timeout_seconds",
        "network_policy", "network_enforcement", "expected_exit",
    ):
        assert receipt["recipe"][key] == spec[key], key
    expected_stdout = ("\n".join(SUMMARY_LINES) + "\n").encode()
    assert receipt["output_evidence"]["stdout_semantic_sha256"] == hashlib.sha256(
        expected_stdout
    ).hexdigest()
    assert receipt["output_evidence"]["expected_line_count"] == len(SUMMARY_LINES)

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by)\b|"
        r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
        r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
        r"(?:axiom|constant|opaque|unsafe|extern)\b",
        re.MULTILINE,
    )
    all_source = "\n".join(
        source_without_comments_and_strings((HERE / name).read_text(encoding="utf-8"))
        for name in ("Statement.lean", "Proof.lean", "ObligationTree.lean", "Validation.lean")
    )
    assert prohibited.search(all_source) is None
    replay = narrow_lean_replay()
    assert receipt["result"]["current_release_lean_output_sha256"] == replay["output_sha256"]
    assert receipt["result"]["validation_closure"] == {
        "declarations": replay["closure_declarations"],
        "modules": replay["closure_modules"],
        "unexpected_bodyless": [],
        "unsafe_declarations": [],
    }

    packet = load(ROOT / ".stage1-worker-selftest.json")
    assert set(packet) == {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert packet["item_id"] == ITEM and packet["base_revision"] == BASE_REVISION
    assert packet["state"] == "[_]"
    assert set(packet["changed_paths"]) == set(receipt["changed_paths"]) == CHANGED_PATHS
    assert packet["commands"] == receipt["commands_and_results"]
    assert packet["output_summary"] == receipt["output_summary"] == SUMMARY_LINES
    assert packet["known_failures"] == decision["known_failures"] == receipt["known_failures"]
    status = git("status", "--short", "--untracked-files=all")
    actual_changes = {
        line[3:] for line in status.splitlines()
        if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual_changes == CHANGED_PATHS, (actual_changes, CHANGED_PATHS)
    for relative in CHANGED_PATHS:
        assert_text_hygiene(ROOT / relative)
    for name in RELEASE_OUTPUT_NAMES:
        text = (HERE / name).read_text(encoding="utf-8")
        assert "/home/" not in text and ".cron/" not in text
        assert "theorem_complete=true" not in text

    print("\n".join(SUMMARY_LINES))


if __name__ == "__main__":
    main()
