#!/usr/bin/env python3
"""Fail-closed release reconciliation for S56-M-1171-RELEASE."""

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
HERE = ROOT / "Stage1_Instances" / "THM-M-1171"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
ITEM = "S56-M-1171-RELEASE"
THEOREM = "THM-M-1171"
BASE_REVISION = "3d3099d0d4002093cf89da97132bdf954605810b"
BASE_TREE = "17ea0daeddceb9742a5df33c247d624d2842c520"
VALIDATION_BASE = "a1a7e939e58f103f5ff5d23af51437fa8658aa04"
TOOLCHAIN = "leanprover/lean4:v4.29.0"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MATHLIB_ORIGIN = "https://github.com/leanprover-community/mathlib4.git"
MATHLIB_LICENSE_SHA256 = "b40930bbcf80744c86c46a12bc9da056641d722716c378f5659b9e555ef833e1"
EXPRESSION_SHA256 = "94cb9c63c1ee16182bd550388d2f29156c59a6a5cbda91509fead48fcfcc2fd8"
DENOMINATOR_SHA256 = "b3c709ee6627b5d79f2dfe5d79cc0a7b828cd418b85f1dd9312cc6350fe1fc10"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
OPEN_ROOT_CUT = [
    "M1171-L-MIHLIN",
    "M1171-L-FOURIER-DERIV",
    "M1171-L-LP-ASSEMBLY",
]
PARTIAL_IDS = ["M1171-L-OPNORM", "M1171-L-LP-ASSEMBLY"]
INVENTORY_IDS = [
    "M1171-ROOT",
    "M1171-S-DEFINITIONS",
    "M1171-S-BOUNDARIES",
    "M1171-S-FOUNDATION",
    "M1171-N-SCHWARTZ",
    "M1171-N-COMPLEX",
    "M1171-L-FOURIER-DERIV",
    "M1171-C-MULTIPLIER",
    "M1171-L-MIHLIN",
    "M1171-L-ZERO-FREQ",
    "M1171-T-COMPONENT",
    "M1171-L-FDERIV-PARTIAL",
    "M1171-L-TRACE",
    "M1171-L-OPNORM",
    "M1171-L-LP-ASSEMBLY",
    "M1171-T-ASSEMBLE",
    "M1171-X-SOURCE",
    "M1171-X-PROVENANCE",
]
EXPECTED_INPUTS = {
    "Statement.lean": "8fbc30483425ab2e78c919b0f62c88e0161a0a290836cd532bd3ca837c225ae3",
    "Proof.lean": "c63fa9acc7ec26e3b5c80a7f71100fcda50d5b2858becad0ecb06e97023f7db2",
    "Validation.lean": "613227e5476da3c0c8f5e2593c8eb9e38f240a1ab5756ce0715c50880ce13dcf",
    "README.md": "6be8f78e3ed8f8d29790c8e5e8208fa31b4c3d418349d2241da77d739331b440",
    "source_statement_crosswalk.md": "8552fee1110c41b2753b7557ba9831fe6384cc88311f3148a874574ec50cf689",
    "intake.json": "f346e25861eb1b13e10fa4ac9165cc0e90df62e17d0ffa8b98b0f9bcc4f48834",
    "statement.json": "2dc7e41c0058d98ada82476b4e188d75728cd4292396cd8bbb646428d29c6010",
    "anchor-audit.json": "51986018a863065be0cd9c8068c757beb086d77705a345c6c17a7a68d064ed0c",
    "obligation-registry.json": "f242b01b394a8204269f8bb11a146040b2c4ce12b35dd719c2e5e934637556b0",
    "typed-graphs.json": "ced3a88d0ae8aefefa4c12e43ad68475de9c6c16a04ed7ac0dc851433ccab24b",
    "proof-receipt.json": "d074fe57bc5903533e91f68040594962b2110616471faa3b2d2087da45874042",
    "proof-blocker.json": "b5dad27839ed431ab0a0c0403575488a128f61a69fe165e3fd9de159f15a1404",
    "proof-validation.md": "debf3ad5b2d45a7894ed9b298b8a946dc8a37d1c0a55c1167e922221d46704d4",
    "validation-spec.json": "b9ef572c7fc4531822a89829bfc8f6083ce8de4e4be079fb68e1831c3090e72c",
    "validation-receipt.json": "a8f9ecf8f0f47278cf9b7e99af1e0ab38ddb615eed8c95fcf297ef109f9e3c45",
    "validation-phase.md": "2ebdbc21a118c3d268d03460ff8a5d3d8106aa342e4d7129b7e9fda5e8932466",
    "check_validation.py": "4490112bfe53ffae8a5bfccd664c4220ae97954908cd95e1a728ed591e7562c0",
}
EXPECTED_AUTHORITY_INPUTS = {
    "Docs/Stage1_Blueprint_rev-5.6.md": "5ab57c000ac93b3b6c442487585c79011dcbd6df3cc5069c630acc4e96681ce1",
    "Docs/Stage1_Targets_rev-5.6.json": "02eec284de534dd78e1cf75f82a477ff477567dd682b7445cb7587abd137ab2c",
    "Docs/Stage1_Execution_DAG_rev-5.6.json": "e2d3cc08c43b928591d6ffc711be8dc82640ab4fcdeb5497be686e52147e603b",
    "Docs/Blueprint_Guidelines.md": "a06c07b5ca1b270b4935ad3dab893e9a0e078c29c8da2ef9dca1e71193310535",
    "skills/execute-stage1-rev56/SKILL.md": "26d47a66c6535feabb8bbf1051fd55d76a53fe761f4b3d953f86b97ec86152b8",
    "Formalizations/Lean/lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "Formalizations/Lean/lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
RELEASE_INPUT_NAMES = (
    "release-spec.json",
    "release-decision.json",
    "release-receipt.json",
    "release-validation.md",
)
EXPECTED_RELEASE_OUTPUTS = {
    "release-spec.json": "061f54620e8db1a3fd77464b96e29818be9dd57242801de599a01a925cbfd98b",
    "release-decision.json": "2e567130c441e51b7e2b92fc2df775e8b816b2e0810a42165e7bcfed66cca7d2",
    "release-validation.md": "18530ed268d42e585dcb672c97b893f39239bee0cc21953f4d9b05cc96e4c09f",
}
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/check_release.py",
    *(f"Stage1_Instances/{THEOREM}/{name}" for name in RELEASE_INPUT_NAMES),
}
SUMMARY_LINES = [
    "PASS release reconciliation: target, DAG, receipts, registry, graphs, and hashes agree",
    "PASS narrow Lean replay: exact statement plus four partial bodies checked at trust zero",
    "BLOCKED S56-10.2-DEPENDENCY-ACCEPTANCE: validation is provisional and not master accepted",
    "BLOCKED exact root: H2/M4/R4 unchanged; zero frozen obligations closed",
    "BLOCKED AUDIT-Z and THEOREM-Z: source/readability, trust, hermetic, and independent gates are open",
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
        output,
        re.DOTALL,
    )
    assert match is not None, f"missing axiom report for {declaration}"
    return {
        part.strip() for part in match.group("axioms").split(",") if part.strip()
    }


def assert_text_hygiene(path: Path) -> None:
    data = path.read_bytes()
    assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())


def historical_validation_integrity(receipt: dict) -> None:
    for name, expected in EXPECTED_INPUTS.items():
        if name in receipt["inputs"]:
            assert receipt["inputs"][name] == expected, name
    assert receipt["base_revision"] == VALIDATION_BASE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]"
    assert receipt["accepted"] is receipt["release_grade"] is False
    assert receipt["verdict"] == "blocked"
    assert receipt["accepted_receipt_ids"] == []
    assert receipt["root_vector_before"] == receipt["root_vector_after"] == {
        "H": "H2", "M": "M4", "R": "R4"
    }
    result = receipt["result"]
    assert result["supported_obligation_ids"] == []
    assert result["accepted_closed_obligation_ids"] == []
    assert result["root_closed"] is result["root_kernel_closed"] is False
    assert result["root_machine_debt"] == "M4"
    assert result["open_root_cut_set"] == OPEN_ROOT_CUT
    assert result["audit_complete"] is result["theorem_complete"] is False
    assert receipt["hermeticity"]["decision"] == "fail_closed_nonrelease_warm_cache_replay"
    assert receipt["independent_validation"]["decision"] == "fail_closed"


def narrow_lean_replay() -> dict[str, str]:
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

    with tempfile.TemporaryDirectory(prefix="stage1-m1171-release-", dir="/tmp") as name:
        tmp = Path(name).resolve()
        (tmp / "home").mkdir()
        for source in ("Statement.lean", "Proof.lean", "Validation.lean"):
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
            argv = base + ["--setenv", "LEAN_PATH", module_path, str(lean), "--trust=0"]
            if emit_olean:
                argv += ["-o", source.replace(".lean", ".olean")]
            argv.append(source)
            return run(argv, env=fixed_env).stdout

        outputs = {
            "statement": lean_run("Statement.lean", lean_path, True),
            "proof": lean_run("Proof.lean", lean_path, False),
            "validation": lean_run("Validation.lean", f"{tmp}:{lean_path}", False),
        }

    combined = "\n".join(outputs.values())
    assert "sorryAx" not in combined and "error:" not in combined
    for declaration in (
        "Stage1Instances.THM_M_1171.opNorm_le_componentSum",
        "Stage1Instances.THM_M_1171.eLpNorm_finset_sum_le",
    ):
        assert reported_axioms(outputs["proof"], declaration) == EXPECTED_AXIOMS
    for declaration in (
        "Stage1Instances.THM_M_1171.Validation.differentialOpNormLeComponentSum",
        "Stage1Instances.THM_M_1171.Validation.differentialELpNormFinsetSumLe",
    ):
        assert reported_axioms(outputs["validation"], declaration) == EXPECTED_AXIOMS
    assert outputs["validation"].count("Declarations are sorry-free!") == 2
    assert "VALIDATION_CLOSURE bodyless_nonaxioms=[]" in outputs["validation"]
    assert "VALIDATION_CLOSURE unsafe=[]" in outputs["validation"]
    return {
        key: hashlib.sha256(value.encode()).hexdigest() for key, value in outputs.items()
    }


def main() -> None:
    if sys.flags.optimize != 0:
        raise RuntimeError("release checker requires Python assertions")

    decision = load(HERE / "release-decision.json")
    receipt = load(HERE / "release-receipt.json")
    spec = load(HERE / "release-spec.json")
    validation = load(HERE / "validation-receipt.json")
    proof = load(HERE / "proof-receipt.json")
    statement = load(HERE / "statement.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    targets = load(ROOT / "Docs" / "Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 372 and target["baseline"] == "L0"
    assert target["lifecycle_mode"] == "planned"
    assert target["rework_required"] is True and target["theorem_complete"] is False
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item == {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 372,
        "phase": "release",
        "layer": 6,
        "state": "[ ]",
        "depends_on": ["S56-M-1171-VALIDATION"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Reconcile evidence and decide the exact theorem-completion verdict.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }
    predecessor = next(
        row for row in execution["items"] if row["id"] == "S56-M-1171-VALIDATION"
    )
    assert predecessor["state"] == "[_]" and predecessor["attempts"] == 1

    for name, expected in EXPECTED_INPUTS.items():
        assert sha256(HERE / name) == expected, f"reconciled input drifted: {name}"
    for relative, expected in EXPECTED_AUTHORITY_INPUTS.items():
        assert sha256(ROOT / relative) == expected, f"authority input drifted: {relative}"
    assert decision["reconciled_inputs"] == EXPECTED_INPUTS
    assert decision["authority_inputs"] == EXPECTED_AUTHORITY_INPUTS

    assert statement["canonical_formal_target"]["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert registry["root_obligation_id"] == graphs["root_node_id"] == "M1171-ROOT"
    assert registry["frozen_denominators"]["inventory"] == INVENTORY_IDS
    assert graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert graphs["closure_boundary"] == {
        "closed_obligations": [],
        "root_closed": False,
        "audit_complete": False,
        "theorem_complete": False,
        "remaining_root_cut_set": OPEN_ROOT_CUT,
        "root_machine_debt": "M4",
    }
    root = next(node for node in graphs["nodes"] if node["obligation_id"] == "M1171-ROOT")
    assert [root["human_debt"], root["machine_debt"], root["readability_debt"]] == [
        "H2", "M4", "R4"
    ]
    assert proof["accepted"] is False
    assert proof["partial_progress_toward_obligation_ids"] == PARTIAL_IDS
    assert proof["supported_obligation_ids"] == proof["accepted_closed_obligation_ids"] == []
    assert proof["result"]["root_kernel_closed"] is False
    assert proof["result"]["theorem_complete"] is False
    historical_validation_integrity(validation)
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
    assert dependency["item_id"] == validation["item_id"] == "S56-M-1171-VALIDATION"
    assert dependency["receipt_id"] == validation["receipt_id"]
    assert dependency["receipt_sha256"] == sha256(HERE / "validation-receipt.json")
    assert dependency["support_state"] == validation["support_state"]
    assert dependency["accepted"] is dependency["release_grade"] is False
    assert dependency["master_accepted"] is False
    assert dependency["historical_recipe_currently_replayable"] is False
    assert VALIDATION_BASE != BASE_REVISION
    assert f'BASE_REVISION = "{VALIDATION_BASE}"' in (HERE / "check_validation.py").read_text()

    result = decision["decision"]
    assert decision["item_id"] == ITEM and decision["theorem_id"] == THEOREM
    assert decision["base_revision"] == BASE_REVISION and decision["base_tree"] == BASE_TREE
    assert decision["proposed_state"] == "[_]" and decision["release_grade"] is False
    assert decision["accepted_receipt_ids"] == []
    assert result["verdict"] == "blocked"
    assert result["lifecycle_before"] == result["lifecycle_after"] == "planned"
    assert result["root_vector_before"] == result["root_vector_after"] == ["H2", "M4", "R4"]
    assert result["audit_complete"] is result["theorem_complete"] is False
    assert result["audit_z"] == result["theorem_z"] == "blocked"
    assert result["release_accepted"] is False
    assert result["first_failed_gate"]["gate_id"] == "S56-10.2-DEPENDENCY-ACCEPTANCE"
    assert result["first_failed_theorem_gate"]["gate_id"] == (
        "S56-THEOREM-EXACT-ROOT-KERNEL-CLOSURE"
    )
    assert result["first_failed_release_specific_gate"]["gate_id"] == (
        "S56-RELEASE-IMMUTABLE-CLEAN-INPUT"
    )
    assert result["next_failed_release_gate"]["gate_id"] == "S56-10.6-HERMETIC-COLD-BUILD"
    assert result["remaining_root_cut_set"] == OPEN_ROOT_CUT
    assert result["first_failed_audit_gate"]["gate_id"] == (
        "S56-AUDIT-FROZEN-INVENTORY-SOURCE-BOUNDARY-RECONCILIATION"
    )
    disagreement = decision["authority_disagreement"]
    assert disagreement["intake_projection"] == ["H2", "M4", "R3"]
    assert disagreement["typed_graph_and_validation_projection"] == ["H2", "M4", "R4"]
    assert disagreement["conservative_release_vector"] == ["H2", "M4", "R4"]
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
    assert receipt["depends_on"] == ["S56-M-1171-VALIDATION"]
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
        "H2", "M4", "R4"
    ]
    assert receipt["result"]["remaining_root_cut_set"] == OPEN_ROOT_CUT
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
    expected_release_bindings = {
        f"Stage1_Instances/{THEOREM}/{name}": digest
        for name, digest in EXPECTED_RELEASE_OUTPUTS.items()
    }
    expected_release_bindings[f"Stage1_Instances/{THEOREM}/check_release.py"] = sha256(
        Path(__file__).resolve()
    )
    assert receipt["release_output_bindings"] == expected_release_bindings
    for relative, expected in expected_release_bindings.items():
        assert sha256(ROOT / relative) == expected, f"release output drifted: {relative}"
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
        source_without_comments((HERE / name).read_text(encoding="utf-8"))
        for name in ("Statement.lean", "Proof.lean", "Validation.lean")
    )
    assert prohibited.search(all_source) is None
    lean_hashes = narrow_lean_replay()
    assert receipt["result"]["current_release_lean_output_sha256"] == lean_hashes

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
    for name in RELEASE_INPUT_NAMES:
        text = (HERE / name).read_text(encoding="utf-8")
        assert "/home/" not in text and ".cron/" not in text
        assert "theorem_complete=true" not in text

    print("\n".join(SUMMARY_LINES))


if __name__ == "__main__":
    main()
