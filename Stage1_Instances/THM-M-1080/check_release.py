#!/usr/bin/env python3
"""Fail-closed release reconciliation for S56-M-1080-RELEASE."""

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
HERE = ROOT / "Stage1_Instances" / "THM-M-1080"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM = "S56-M-1080-RELEASE"
THEOREM = "THM-M-1080"
BASE_REVISION = "79899c925fb9bacf9126eb11f7f24954b0516a3d"
BASE_TREE = "f5f0295fc2ae6f3f30ed37dc8afbb6bb14495c10"
VALIDATION_BASE = "3f555cfc0879cb7c42e83d6bcf7b9e3e09997e58"
TOOLCHAIN = "leanprover/lean4:v4.29.0"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MATHLIB_REMOTE = "https://github.com/leanprover-community/mathlib4.git"
LEAN_EXECUTABLE = Path.home() / ".elan/toolchains/leanprover--lean4---v4.29.0/bin/lean"
LEAN_LIBRARY = Path.home() / ".elan/toolchains/leanprover--lean4---v4.29.0/lib/lean"
EXPRESSION_SHA256 = "af69d1d82ed31033201ff05a06f14f6fe200307a16bd3538f34ab56d4fd0d350"
DENOMINATOR_SHA256 = "869c1a9abe79908244280909afaadc8e84b294df0d6b1e290b81e5363243df14"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
INVENTORY_IDS = [
    "M1080-ROOT", "M1080-S-DEFINITIONS", "M1080-S-SCOPE",
    "M1080-S-BOUNDARY", "M1080-S-FOUNDATION", "M1080-N-INCREMENTS",
    "M1080-N-TELESCOPE", "M1080-C-EXPONENTIAL", "M1080-L-COND-HOEFFDING",
    "M1080-L-MGF-ITERATE", "M1080-L-MARKOV", "M1080-L-OPTIMIZE",
    "M1080-T-POSITIVE", "M1080-T-ZERO", "M1080-T-ASSEMBLE",
    "M1080-X-MATHLIB", "M1080-X-SOURCE", "M1080-X-PROVENANCE",
]
PROOF_IDS = INVENTORY_IDS[:15]
FROZEN_PREPROOF_MACHINE_CUT = ["M1080-T-POSITIVE", "M1080-T-ZERO"]
PROVISIONAL_RELEASE_CUT = ["M1080-X-SOURCE", "M1080-X-PROVENANCE", "M1080-S-FOUNDATION"]
COVERED_DECLARATIONS = [
    "Stage1Instances.THM_M_1080.Statement",
    "Stage1Instances.THM_M_1080.ObligationTree.azumaUpperTail_of_threshold_packages",
    *(f"Stage1Instances.THM_M_1080.Proof.{name}" for name in (
        "sum_increment_eq_sub", "exp_secant_bound", "condExp_exp_increment_le",
        "exp_endpoint_integrable", "exp_increment_sum_integral_le", "positiveThreshold",
        "zeroThreshold", "azumaUpperTail",
    )),
    "Stage1Instances.THM_M_1080.ExactRoot.positiveThresholdPackage",
    "Stage1Instances.THM_M_1080.ExactRoot.zeroThresholdPackage",
    "Stage1Instances.THM_M_1080.ExactRoot.azumaUpperTail_exact",
    "Stage1Instances.THM_M_1080.Validation.directExactRoot",
]
EXPECTED_INPUTS = {
    "README.md": "68031a54e0a1d2b2b5a7f7cef34c8a00524247947649b03d614df8db8a1c5cef",
    "instance.json": "471ef09851f351fd8ff6d7be61916b0de2c2cdacbf3517302de4b269263d0f8b",
    "task-dag.json": "b07c403453d9972f17e69ee695beca9ce2ee53e4a3f2e93024f71523845cd555",
    "Statement.lean": "7c70293edee7d3bfc79ea241f932241483285342ab400e10e8290782666ebda4",
    "statement.json": "362e192f9d4d6a66e4654fb716090fadf1a5f1afe36301d49c8a88b23430a4ed",
    "source-statement-crosswalk.md": "6a91efd7368dcb472ddbd90d317f27db323ef088cc781acec2e002e1bea953d9",
    "AnchorAudit.lean": "895c71ad0a59764dcd797b898cd0da612f0431164066d7a2e8d21f58f7b96694",
    "anchor-audit.json": "6ca6e3bee4db7e77be06a0c1f775c43845b458e81d1ab68d8b1046a857b6a18a",
    "obligation-registry.json": "2238aecce213657fc484e2cb462d9bdb83d397e98bd753f1631ae6325d51f406",
    "typed-graphs.json": "7663e59aceb59ec263ce79dda260d2ce6be89dab7012cb204ffb015e52df6522",
    "validation-specs.json": "62c6c61b3b8f976b86211e08f6713512148452a1323b6be731d44812d2c0514a",
    "ObligationTree.lean": "ab7794789e88eb86ecf41a7a4356d0126dfde0298af4bf065a2bb0c4466c1d6d",
    "Proof.lean": "8332d6aaa5fc2fd24850bf24864ef2c600abfbb74e5468838df83c9f342d5e9e",
    "ExactRoot.lean": "c87fd2ffbfb88150e1c241ace9e45faaa9f9d25b84831b983b1616c41d5661f8",
    "proof-receipt.json": "5e1334dc3cc7545a3ec20637f7fbbdd724bfbe9c974a612331e26c519366ccfb",
    "Validation.lean": "637eaeedb32d5b27622cdb0598fc618cbe81959565dcf03ecca823746845eca1",
    "validation-spec.json": "984a7bb3a048b58deb52d06fb363a19cfdd192ce12f026e48e93cd3730ed2be3",
    "validation-receipt.json": "4e591b09b104e38e1b8302ec8cabe81f66fa5e5de9a145c5c8de397dc5d9c68c",
    "validation-phase.md": "9a97ccedd44366fa35ecd0b63b8697ee09cb8a3a18d7b2a6075856aacf948863",
    "check_validation.py": "7852edcf1c03e958ffe805fc885b1fe9895d053f6dfe1714d8b12a57f80da3dc",
}
EXPECTED_AUTHORITY_INPUTS = {
    "Docs/Stage1_Targets_rev-5.6.json": "02eec284de534dd78e1cf75f82a477ff477567dd682b7445cb7587abd137ab2c",
    "Docs/Stage1_Execution_DAG_rev-5.6.json": "7cdca293e6a93ce26cfce504b80ac9ec4d4ba2071201815ef4e12de05424d407",
    "Docs/Stage1_Blueprint_rev-5.6.md": "d79ce3bd87fe1a7cbdbcb1853d1d903691b10131afe2ca109b17d4969ded51af",
    "Docs/Blueprint_Guidelines.md": "a06c07b5ca1b270b4935ad3dab893e9a0e078c29c8da2ef9dca1e71193310535",
    "skills/execute-stage1-rev56/SKILL.md": "26d47a66c6535feabb8bbf1051fd55d76a53fe761f4b3d953f86b97ec86152b8",
    "Formalizations/Lean/lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "Formalizations/Lean/lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
RELEASE_OUTPUTS = (
    "release-spec.json", "release-decision.json", "release-receipt.json",
    "release-validation.md",
)
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/check_release.py",
    *(f"Stage1_Instances/{THEOREM}/{name}" for name in RELEASE_OUTPUTS),
}
SUMMARY_LINES = [
    "PASS negative reconciliation: target, DAG, receipts, registry, graph conflicts, and hashes authenticated",
    "PASS narrow Lean replay: exact root and differential bridge checked at trust zero",
    "BLOCKED S56-10.2-DEPENDENCY-ACCEPTANCE: validation is provisional and not master accepted",
    "BLOCKED AUDIT-Z: authority, source, readability, provenance, and trust remain unreconciled",
    "BLOCKED THEOREM-Z: cold/offline, independent-verifier, and deterministic-bundle gates are open",
    "verdict=blocked audit_complete=false theorem_complete=false accepted_receipts=0",
]
SUMMARY_STDOUT = "\n".join(SUMMARY_LINES) + "\n"
SUMMARY_STDOUT_SHA256 = "05a8475169064a007c206fe470e8973bf1adb03784bcc4e6c4f508cea73ebe44"


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
    argv: list[str], *, cwd: Path = ROOT, timeout: int = 1800,
    env: dict[str, str] | None = None,
) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        argv, cwd=cwd, env=env, text=True, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, timeout=timeout, check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(f"command failed ({result.returncode}): {argv!r}\n{result.stdout}")
    return result


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["git", *args], cwd=cwd, timeout=60).stdout.strip()


def source_without_comments(source: str) -> str:
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


def reported_axioms(output: str, declaration: str) -> set[str]:
    match = re.search(
        rf"'{re.escape(declaration)}' depends on axioms:\s*\[(?P<axioms>.*?)\]",
        output, re.DOTALL,
    )
    assert match is not None, f"missing axiom report for {declaration}"
    return {part.strip() for part in match.group("axioms").split(",") if part.strip()}


def assert_text_hygiene(path: Path) -> None:
    data = path.read_bytes()
    assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())


def assert_no_prohibited_lean() -> None:
    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by|extern)\b|"
        r"^[ \t]*(?:axiom|constant|opaque|unsafe)\b",
        re.MULTILINE,
    )
    for name in (
        "Statement.lean", "AnchorAudit.lean", "ObligationTree.lean", "Proof.lean",
        "ExactRoot.lean", "Validation.lean",
    ):
        source = source_without_comments((HERE / name).read_text(encoding="utf-8"))
        assert prohibited.search(source) is None, f"prohibited Lean construct in {name}"


def narrow_lean_replay() -> None:
    bwrap = Path(os.path.realpath(shutil.which("bwrap") or ""))
    assert bwrap.is_file(), "bubblewrap is required for network-denied replay"
    fixed_env = os.environ.copy()
    fixed_env.pop("LEAN_PATH", None)
    fixed_env.update({
        "ELAN_TOOLCHAIN": TOOLCHAIN,
        "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8", "TZ": "UTC",
        "LEAN_NUM_THREADS": "1",
    })
    lean = LEAN_EXECUTABLE
    package_roots = [
        "Cli", "batteries", "Qq", "aesop", "proofwidgets", "importGraph",
        "LeanSearchClient", "plausible", "checkdecls", "mathlib", "flt-regular",
    ]
    lean_paths = [
        LEAN_ROOT / ".lake/packages" / package / ".lake/build/lib/lean"
        for package in package_roots
    ]
    lean_paths += [LEAN_ROOT / ".lake/build/lib/lean", LEAN_LIBRARY]
    lean_paths = [path for path in lean_paths if path.is_dir()]
    assert (MATHLIB / ".lake/build/lib/lean").resolve() in {
        path.resolve() for path in lean_paths
    }, "pinned mathlib object path missing"
    lean_path = ":".join(str(path.resolve()) for path in lean_paths)
    assert lean.is_file()
    assert LEAN_COMMIT in run([str(lean), "--version"], env=fixed_env, timeout=60).stdout

    with tempfile.TemporaryDirectory(prefix="stage1-m1080-release-", dir="/tmp") as name:
        tmp = Path(name).resolve()
        (tmp / "home").mkdir()
        for source in (
            "Statement.lean", "ObligationTree.lean", "Proof.lean", "ExactRoot.lean",
            "Validation.lean",
        ):
            shutil.copy2(HERE / source, tmp / source)
        base = [
            str(bwrap), "--ro-bind", "/", "/", "--bind", str(tmp), str(tmp),
            "--dev", "/dev", "--proc", "/proc", "--unshare-net", "--die-with-parent",
            "--clearenv", "--setenv", "HOME", str(tmp / "home"),
            "--setenv", "LANG", "C.UTF-8", "--setenv", "LC_ALL", "C.UTF-8",
            "--setenv", "TZ", "UTC", "--setenv", "LEAN_NUM_THREADS", "1",
            "--chdir", str(tmp),
        ]

        def lean_run(source: str, *, sibling_path: bool, emit_olean: bool) -> str:
            module_path = f"{tmp}:{lean_path}" if sibling_path else lean_path
            argv = base + [
                "--setenv", "LEAN_PATH", module_path, str(lean), "--trust=0", "-t0",
            ]
            if emit_olean:
                argv += ["-o", source.replace(".lean", ".olean")]
            argv.append(source)
            return run(argv, env=fixed_env).stdout

        statement_output = lean_run("Statement.lean", sibling_path=False, emit_olean=True)
        obligation_output = lean_run("ObligationTree.lean", sibling_path=False, emit_olean=True)
        proof_output = lean_run("Proof.lean", sibling_path=False, emit_olean=True)
        exact_output = lean_run("ExactRoot.lean", sibling_path=True, emit_olean=True)
        validation_output = lean_run("Validation.lean", sibling_path=True, emit_olean=False)

    assert "AzumaUpperTail" in statement_output
    declarations = {
        obligation_output: [
            "Stage1Instances.THM_M_1080.ObligationTree.azumaUpperTail_of_threshold_packages",
        ],
        proof_output: [
            f"Stage1Instances.THM_M_1080.Proof.{name}" for name in (
                "sum_increment_eq_sub", "exp_secant_bound", "condExp_exp_increment_le",
                "exp_endpoint_integrable", "exp_increment_sum_integral_le",
                "positiveThreshold", "zeroThreshold", "azumaUpperTail",
            )
        ],
        exact_output: [
            f"Stage1Instances.THM_M_1080.ExactRoot.{name}" for name in (
                "positiveThresholdPackage", "zeroThresholdPackage", "azumaUpperTail_exact",
            )
        ],
        validation_output: [
            "Stage1Instances.THM_M_1080.Proof.azumaUpperTail",
            "Stage1Instances.THM_M_1080.Validation.directExactRoot",
        ],
    }
    for output, names in declarations.items():
        for declaration in names:
            assert reported_axioms(output, declaration) == EXPECTED_AXIOMS
    all_output = obligation_output + proof_output + exact_output + validation_output
    assert "sorryAx" not in all_output and "declaration uses 'sorry'" not in all_output
    assert "VALIDATION_CLOSURE axioms=[propext, Classical.choice, Quot.sound]" in validation_output
    assert "VALIDATION_CLOSURE bodyless_nonaxioms=[]" in validation_output
    assert "VALIDATION_CLOSURE unsafe=[]" in validation_output


def main() -> None:
    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    for name, expected in EXPECTED_INPUTS.items():
        assert sha256(HERE / name) == expected, f"stale input: {name}"
    for name, expected in EXPECTED_AUTHORITY_INPUTS.items():
        assert sha256(ROOT / name) == expected, f"changed authority input: {name}"

    targets = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 522
    assert target["baseline"] == "L0" and target["rework_required"] is True
    assert target["lifecycle_mode"] == "planned" and target["theorem_complete"] is False

    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item == {
        "id": ITEM, "theorem_id": THEOREM, "execution_rank": 522,
        "phase": "release", "layer": 6, "state": "[ ]",
        "depends_on": ["S56-M-1080-VALIDATION"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Reconcile evidence and decide the exact theorem-completion verdict.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0, "children": [],
    }
    validation_item = next(
        row for row in execution["items"] if row["id"] == "S56-M-1080-VALIDATION"
    )
    assert validation_item["state"] == "[_]"

    instance = load(HERE / "instance.json")
    local_dag = load(HERE / "task-dag.json")
    statement = load(HERE / "statement.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    proof_receipt = load(HERE / "proof-receipt.json")
    validation_receipt = load(HERE / "validation-receipt.json")
    spec = load(HERE / "release-spec.json")
    decision = load(HERE / "release-decision.json")
    receipt = load(HERE / "release-receipt.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")

    assert instance["lifecycle"] == "planned"
    assert instance["root_vector"] == {"H": "H1", "M": "M4", "R": "R4"}
    assert instance["accepted_proof_state"] == []
    assert instance["audit_complete"] is instance["theorem_complete"] is False
    assert local_dag["lifecycle"] == "planned" and local_dag["accepted_states"] == []
    assert all(task["state"] == "open" for task in local_dag["tasks"])

    formal = statement["canonical_formal_target"]
    assert formal["declaration_or_expression"] == "Stage1Instances.THM_M_1080.Statement"
    assert formal["elaborated_expression_sha256"] == EXPRESSION_SHA256
    ids = [row["obligation_id"] for row in registry["obligations"]]
    assert ids == INVENTORY_IDS
    assert registry["denominator_sha256"] == graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    closure = graphs["closure_boundary"]
    assert closure["closed_obligations"] == ["M1080-T-ASSEMBLE"]
    assert closure["root_closed"] is closure["audit_complete"] is closure["theorem_complete"] is False
    assert closure["root_machine_debt"] == "M3"
    assert graphs["graphs"]["evidence"]["edges"] == []
    assert all(node["readability_debt"] == "R3" for node in graphs["nodes"])

    assert proof_receipt["accepted"] is False
    assert proof_receipt["accepted_closed_obligation_ids"] == []
    assert proof_receipt["result"]["root_kernel_closed"] is True
    assert proof_receipt["result"]["accepted_root_closed"] is False
    assert proof_receipt["result"]["theorem_complete"] is False
    assert proof_receipt["root_vector_proposed"] == {"H": "H2", "M": "M0-L", "R": "R3"}
    assert set(proof_receipt["provisionally_closed_proof_obligation_ids"]) == set(PROOF_IDS)
    assert decision["provisional_receipt_ids_inspected"] == [
        proof_receipt["receipt_id"], validation_receipt["receipt_id"],
    ]
    predecessor_receipts = {
        path.name for path in HERE.glob("*receipt*.json")
        if path.name != "release-receipt.json"
    }
    assert predecessor_receipts == {"proof-receipt.json", "validation-receipt.json"}

    assert validation_receipt["base_revision"] == VALIDATION_BASE
    assert validation_receipt["support_state"] == "provisional_worker_selftest"
    assert validation_receipt["proposed_state"] == "[_]"
    assert validation_receipt["accepted"] is validation_receipt["release_grade"] is False
    assert validation_receipt["result"]["exact_root_kernel_closed"] is True
    assert validation_receipt["result"]["accepted_closed_obligations"] == []
    assert validation_receipt["result"]["audit_complete"] is False
    assert validation_receipt["result"]["theorem_complete"] is False
    for gate in (
        "dependency_master_acceptance_gate", "complete_provenance_gate", "complete_tcb_gate",
        "hermetic_cold_reproduction_gate", "independent_distinct_runner_gate",
    ):
        assert validation_receipt["result"][gate] == "fail_closed"

    manifest = load(LEAN_ROOT / "lake-manifest.json")
    mathlib = next(row for row in manifest["packages"] if row["name"] == "mathlib")
    assert mathlib["rev"] == mathlib["inputRev"] == MATHLIB_REVISION
    assert MATHLIB.resolve().is_dir()
    assert git("rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert git("remote", "get-url", "origin", cwd=MATHLIB) == MATHLIB_REMOTE
    assert git("status", "--porcelain=v1", cwd=MATHLIB) == ""

    assert spec["schema_version"] == "stage1-validation-recipe/1.0"
    assert spec["recipe_id"] == "S56-M-1080-RELEASE-negative-reconciliation-v1"
    assert spec["item_id"] == ITEM and spec["theorem_id"] == THEOREM
    assert spec["cwd"] == "."
    assert spec["argv"] == ["python3", "-I", "-B", f"Stage1_Instances/{THEOREM}/check_release.py"]
    assert spec["network_policy"] == "denied" and spec["expected_exit"] == 0
    assert spec["env_allowlist"] == {
        "ELAN_TOOLCHAIN": TOOLCHAIN, "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8",
        "TZ": "UTC", "LEAN_NUM_THREADS": "1",
    }
    assert spec["timeout_seconds"] == 1800
    assert "Every Lean elaboration subprocess runs under bubblewrap" in spec["network_enforcement"]
    assert "outer process is not namespace-isolated" in spec["network_enforcement"]
    assert spec["expected_outputs"] == [{
        "path_or_stream": "stdout",
        "semantic_hash_policy": (
            "exact six-line negative release summary bound in release-receipt.json"
        ),
    }]
    assert spec["covered_obligation_ids"] == INVENTORY_IDS
    assert spec["covered_declarations"] == COVERED_DECLARATIONS
    assert spec["covered_decisions"] == ["AUDIT-Z", "THEOREM-Z"]

    assert decision["schema_version"] == "stage1-release-decision/1.0"
    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert decision["item_id"] == receipt["item_id"] == packet["item_id"] == ITEM
    assert decision["theorem_id"] == receipt["theorem_id"] == THEOREM
    assert decision["phase"] == receipt["phase"] == "release"
    assert decision["intent"] == receipt["intent"] == "release"
    assert decision["depends_on"] == receipt["depends_on"] == ["S56-M-1080-VALIDATION"]
    assert decision["decision_id"] == receipt["decision_id"] == "S56-M-1080-RELEASE-WORKER-20260715"
    assert decision["base_revision"] == receipt["base_revision"] == packet["base_revision"] == BASE_REVISION
    assert decision["verdict"] == receipt["verdict"] == "blocked"
    assert decision["lifecycle_before"] == decision["lifecycle_after"] == "planned"
    assert decision["accepted"] is decision["release_grade"] is False
    assert decision["content_addressed_release_evidence"] is False
    assert receipt["accepted"] is receipt["release_grade"] is receipt["master_accepted"] is False
    assert receipt["content_addressed_release_evidence"] is False
    assert decision["accepted_receipt_ids"] == receipt["accepted_receipt_ids"] == []
    assert decision["frozen_preproof_machine_root_cut_set"] == FROZEN_PREPROOF_MACHINE_CUT
    assert receipt["frozen_preproof_machine_root_cut_set"] == FROZEN_PREPROOF_MACHINE_CUT
    assert decision["provisional_kernel_release_assurance_cut_set"] == PROVISIONAL_RELEASE_CUT
    assert receipt["provisional_kernel_release_assurance_cut_set"] == PROVISIONAL_RELEASE_CUT
    assert closure["remaining_root_cut_set"] == FROZEN_PREPROOF_MACHINE_CUT
    assert decision["terminal_decisions"] == {
        "audit_complete": False, "theorem_complete": False,
        "audit_z": "blocked", "theorem_z": "blocked",
        "release_accepted": False, "master_acceptance": False,
    }
    assert receipt["result"] == {
        "exit_code": 0, "dependency_master_accepted": False,
        "accepted_closed_obligation_ids": [], "accepted_receipt_ids": [],
        "audit_complete": False, "theorem_complete": False,
        "audit_z": "blocked", "theorem_z": "blocked",
        "release_accepted": False, "master_acceptance": False,
    }
    assert receipt["output_evidence"] == {
        "stream": "stdout",
        "line_count": len(SUMMARY_LINES),
        "byte_count": len(SUMMARY_STDOUT.encode("utf-8")),
        "sha256": SUMMARY_STDOUT_SHA256,
        "canonicalization": (
            "UTF-8 exact SUMMARY_LINES in order, each terminated by LF, including the final line"
        ),
    }
    assert hashlib.sha256(SUMMARY_STDOUT.encode("utf-8")).hexdigest() == SUMMARY_STDOUT_SHA256
    assert decision["first_failed_gate"]["detail"] == "dependency.S56-M-1080-VALIDATION.master_acceptance"
    assert decision["first_failed_audit_gate"]["gate_id"] == "S56-9-AUTHORITY-RECONCILIATION"
    assert decision["first_failed_theorem_gate"]["gate_id"] == "S56-11-T-Z-AUDIT-DEPENDENCY"
    assert decision["first_failed_release_gate"]["gate_id"] == "S56-10.6-HERMETIC-COLD-EMPTY-CACHE"
    assert decision["root_vector"]["instance_authority_before"] == instance["root_vector"]
    assert decision["root_vector"]["instance_authority_after"] == instance["root_vector"]
    assert decision["root_vector"]["proposed_kernel_candidate"] == proof_receipt["root_vector_proposed"]
    assert decision["root_vector"]["unreconciled_no_promotion_boundary"] == instance["root_vector"]
    assert decision["reconciled_inputs"] == EXPECTED_INPUTS
    assert decision["authority_inputs"] == EXPECTED_AUTHORITY_INPUTS

    required_packet_fields = {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert set(packet) == required_packet_fields
    assert packet["state"] == decision["proposed_state"] == receipt["proposed_state"] == "[_]"
    assert set(packet["changed_paths"]) == set(decision["changed_paths"]) == CHANGED_PATHS
    assert packet["known_failures"] == decision["known_failures"] == receipt["known_failures"]
    assert receipt["receipt_contract_limitations"] == {
        "started_at": None,
        "ended_at": None,
        "raw_combined_log_sha256": None,
        "reason": (
            "The bounded worker self-test captured exact exit status and canonical six-line stdout "
            "but did not retain wall-clock timestamps or a raw combined log. This prevents "
            "release-grade receipt status and is recorded rather than reconstructed after the run."
        ),
    }
    impact = receipt["ownership_and_change_impact"]
    assert impact["owned_path"] == f"Stage1_Instances/{THEOREM}"
    assert impact["changed_sources"] == impact["changed_declarations"] == []
    assert impact["changed_graphs"] == impact["changed_composition_certificates"] == []
    assert packet["commands"] == receipt["commands"]
    assert packet["output_summary"] == receipt["output_summary"]
    expected_commands = [
        ("python3 Docs/tools/check_stage1_standard.py", 0),
        ("python3 scripts/stage1_target.py check", 0),
        ("python3 scripts/stage1_target.py show THM-M-1080", 0),
        (f"python3 -I -B Stage1_Instances/{THEOREM}/check_release.py", 0),
        (
            f"for path in Stage1_Instances/{THEOREM}/release-spec.json "
            f"Stage1_Instances/{THEOREM}/release-decision.json "
            f"Stage1_Instances/{THEOREM}/release-receipt.json .stage1-worker-selftest.json; "
            f"do python3 -m json.tool $path >/dev/null || exit; done",
            0,
        ),
        (
            f"PYTHONPYCACHEPREFIX=/tmp/stage1-m1080-release-pycache python3 -m "
            f"py_compile Stage1_Instances/{THEOREM}/check_release.py",
            0,
        ),
        (f"git diff --check -- Stage1_Instances/{THEOREM} .stage1-worker-selftest.json", 0),
    ]
    assert [(row["command"], row["exit_code"]) for row in packet["commands"]] == expected_commands
    assert receipt["dependency"] == decision["dependency"]
    assert receipt["target"] == decision["canonical_target"]
    assert receipt["recipe"] == spec
    assert receipt["decision_sha256"] == sha256(HERE / "release-decision.json")
    assert receipt["release_spec_sha256"] == sha256(HERE / "release-spec.json")
    assert receipt["checker_sha256"] == sha256(HERE / "check_release.py")
    assert receipt["public_projection_sha256"] == sha256(HERE / "release-validation.md")
    tool_paths = {
        "lean": LEAN_EXECUTABLE,
        "python": Path(sys.executable).resolve(),
        "git": Path(os.path.realpath(shutil.which("git") or "")),
        "bubblewrap": Path(os.path.realpath(shutil.which("bwrap") or "")),
    }
    for tool, path in tool_paths.items():
        assert path.is_file()
        assert receipt["environment"][f"{tool}_executable_sha256"] == sha256(path)
    lake_link = LEAN_ROOT / ".lake"
    assert lake_link.is_symlink()
    target_digest = hashlib.sha256(os.readlink(lake_link).encode("utf-8")).hexdigest()
    assert receipt["nonrelease_worktree_evidence"]["automation_lake_symlink_target_sha256"] == target_digest
    assert git("diff", "--", str(HERE), str(ROOT / ".stage1-worker-selftest.json")) == ""

    assert_no_prohibited_lean()
    narrow_lean_replay()

    status = git(
        "status", "--porcelain=v1", "--untracked-files=all", "--",
        str(HERE), str(ROOT / ".stage1-worker-selftest.json"),
    )
    actual_changed = {
        line[3:] if line[:2] == "??" else line[2:].lstrip()
        for line in status.splitlines()
    }
    assert actual_changed == CHANGED_PATHS, (actual_changed, CHANGED_PATHS)
    for relative in CHANGED_PATHS:
        assert_text_hygiene(ROOT / relative)
    for name in RELEASE_OUTPUTS:
        text = (HERE / name).read_text(encoding="utf-8")
        assert "/home/" not in text and ".cron/" not in text
        assert "theorem_complete=true" not in text

    for line in SUMMARY_LINES:
        print(line)


if __name__ == "__main__":
    main()
