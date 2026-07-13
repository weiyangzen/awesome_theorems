#!/usr/bin/env python3
"""Fail-closed release reconciliation for S56-M-0405-RELEASE."""

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
HERE = ROOT / "Stage1_Instances" / "THM-M-0405"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM = "S56-M-0405-RELEASE"
THEOREM = "THM-M-0405"
BASE_REVISION = "18ff7447208231633bf2e01e8aad3111af56531a"
BASE_TREE = "9ea9aab30253e72b62ef25c80e17b575356fb7b6"
TOOLCHAIN = "leanprover/lean4:v4.29.0"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
LEAN_SHA256 = "3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf"
LAKE_SHA256 = "a608ff084d7e2af228b92a29d7c2fd083ba0580e46889175ec74a81678c98359"
BWRAP_SHA256 = "0abea81db798ebf6b4742ac0664802d97521547a353c2a0dbdc21d76cbbfd2c0"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MATHLIB_LICENSE_SHA256 = "b40930bbcf80744c86c46a12bc9da056641d722716c378f5659b9e555ef833e1"
STATEMENT_SHA256 = "db2edf61040b73d00d4d3ab2b7dc227b6ec418793400bf79ac86edc79aa18da1"
DENOMINATOR_SHA256 = "cd9daee4b82734d1e98e216a6371bd83f3fcff1a181e79381773133a6b9da793"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
INVENTORY_IDS = [
    "M0405-ROOT",
    "M0405-S-DEFINITIONS",
    "M0405-S-FOUNDATION",
    "M0405-B-LUCAS",
    "M0405-B-LEHMER",
    "M0405-N-PAIR-NORMALIZATION",
    "M0405-C-CYCLOTOMIC-FACTOR",
    "M0405-L-NONPRIMITIVE-BOUND",
    "M0405-L-LARGE-INDEX-EXCLUSION",
    "M0405-B-DEFECTIVE-CLASSIFICATION",
    "M0405-X-BHV-BRIDGE",
    "M0405-T-LUCAS-ADAPTER",
    "M0405-T-LEHMER-ADAPTER",
    "M0405-C-ROOT-COMPOSITION",
    "M0405-X-PROVENANCE",
]
EXPECTED_INPUTS = {
    "Statement.lean": "db2edf61040b73d00d4d3ab2b7dc227b6ec418793400bf79ac86edc79aa18da1",
    "ObligationTree.lean": "d43df06faea8c463eb51898e02d8db6fa3c92f7b23cdb4c331d70d9be69c9c9b",
    "Proof.lean": "93aaa87a8dde5817b8c8b6eb7396cf8ff4e432683e53448692def34d1a601255",
    "Validation.lean": "4698386f7272b8a9849da0a44cac3280d3e5bf269e656c55f70b7f84bc56e406",
    "instance.json": "a5e94c801a24623681b7ad2ad5c2bf0627c7448cfcb2dfb6cd87a4c757c1c642",
    "statement.json": "ae2b9c50c362176dac75d8788a1e8d0cb673266d9a9b4bc678f2a71edd13b2cb",
    "anchor-audit.json": "d23923ab22ce6bc50e4bdd534a1dadd332e8cd147f73306673e8d147318fbcd3",
    "obligation-registry.json": "85019c33ea774fc20b6011a242f3853dc1a442c3a4cda5495d8df7a628cbd12d",
    "typed-graphs.json": "a69a1ee0d5af3657b4807c6d737bc00dbcde74ea7b120bcad08a0c4a5251889b",
    "obligation-tree.md": "7f434a70c9d0696d94d3f249f09dfd1bfea654d40fdcb112cb22c7e7d29e7bcb",
    "proof-blocker.json": "aad47d62a17dd33dc0ecf7b94bd8c3b296f5ff6dd942d5c97fbf20b3abab9c03",
    "proof-receipt.json": "da86384b29c903ae4ecb9290e8ddfca63a5353a15163fed3fd3bfb85904054ce",
    "validation-spec.json": "42a0fbc3e4cb39bded0c9a67638101dfc7b55bebdd992d0de65c1f827d9efc02",
    "validation-receipt.json": "3f8f995d25ed5d41db78d37c637c1c46cd554be8e76a95c999ea5d278eefaa1f",
    "check_validation.py": "cdffe80fd54df99ca9423ee7748227e28df30534985eff6e616f54abc782d3a5",
}
EXPECTED_AUTHORITY_INPUTS = {
    "Docs/Stage1_Targets_rev-5.6.json": "02eec284de534dd78e1cf75f82a477ff477567dd682b7445cb7587abd137ab2c",
    "Docs/Stage1_Execution_DAG_rev-5.6.json": "4d7245295475f88329057b711b3ad5b7bdb99e1430db744a3787657cb97c44bc",
    "Docs/Stage1_Blueprint_rev-5.6.md": "33c1d952280a36a4efd00641bb613ef3eba59d2a406e70517b6418de938f3875",
    "Docs/Blueprint_Guidelines.md": "a06c07b5ca1b270b4935ad3dab893e9a0e078c29c8da2ef9dca1e71193310535",
    "skills/execute-stage1-rev56/SKILL.md": "26d47a66c6535feabb8bbf1051fd55d76a53fe761f4b3d953f86b97ec86152b8",
}
EXPECTED_TOOL_INPUTS = {
    "lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
OBLIGATION_DECLARATIONS = (
    "statement_of_branches",
    "lucasBranch_of_statement",
    "lehmerBranch_of_statement",
)
PROOF_DECLARATIONS = (
    "ne_of_ratioNotRootOfUnity",
    "LucasPair.alpha_ne_zero",
    "LucasPair.beta_ne_zero",
    "LucasPair.alpha_ne_beta",
    "LucasPair.denominator_ne_zero",
    "LucasPair.coe_discriminant",
    "LucasPair.term_zero",
    "LucasPair.term_one",
    "LehmerPair.alpha_ne_zero",
    "LehmerPair.beta_ne_zero",
    "LehmerPair.alpha_ne_beta",
    "LehmerPair.oddDenominator_ne_zero",
    "LehmerPair.add_ne_zero",
    "LehmerPair.sq_sub_sq_ne_zero",
    "LehmerPair.coe_discriminant",
    "LehmerPair.coe_squaredEvenDenominator",
    "LehmerPair.term_one",
    "LehmerPair.term_two",
)
VALIDATION_DECLARATIONS = (
    "lucas_beta_ne_zero",
    "lucas_alpha_ne_beta",
    "lucas_term_zero",
    "lucas_term_one",
)
SUMMARY_LINES = [
    "PASS release inputs: target, DAG dependency, receipts, registry, graphs, and hashes agree",
    "PASS current Lean replay: 25 theorem declarations, including 4 differential checks, are trust-zero and sorry-free",
    "PASS fail-closed state: lifecycle planned; root H1/M4/R3; accepted receipts 0; closed obligations 0",
    "BLOCKED S56-10.2-DEPENDENCY-ACCEPTANCE: validation is provisional and unaccepted",
    "BLOCKED M0405-X-BHV-BRIDGE and S56-10.6-HERMETIC-COLD-EMPTY-CACHE",
    "verdict=blocked audit_complete=false theorem_complete=false",
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
    argv: list[str],
    *,
    cwd: Path = ROOT,
    env: dict[str, str] | None = None,
    timeout: int = 600,
) -> str:
    result = subprocess.run(
        argv,
        cwd=cwd,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=timeout,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(f"command failed ({result.returncode}): {argv!r}\n{result.stdout}")
    return result.stdout


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["git", *args], cwd=cwd, timeout=60).strip()


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
    no_axioms = f"'{declaration}' does not depend on any axioms"
    pattern = re.compile(
        re.escape(f"'{declaration}' depends on axioms: [") + r"(.*?)]",
        re.DOTALL,
    )
    matches = pattern.findall(output)
    assert output.count(no_axioms) + len(matches) == 1, declaration
    if not matches:
        return set()
    return {part.strip() for part in matches[0].split(",") if part.strip()}


def assert_text_hygiene(path: Path) -> None:
    data = path.read_bytes()
    assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())


def replay_lean() -> None:
    fixed_env = os.environ.copy()
    fixed_env.pop("LEAN_PATH", None)
    fixed_env.update({
        "ELAN_TOOLCHAIN": TOOLCHAIN,
        "LANG": "C.UTF-8",
        "LC_ALL": "C.UTF-8",
        "TZ": "UTC",
        "LEAN_NUM_THREADS": "1",
    })
    lean = Path(run(["lake", "env", "which", "lean"], cwd=LEAN_ROOT, env=fixed_env).strip())
    lake = Path(run(["lake", "env", "which", "lake"], cwd=LEAN_ROOT, env=fixed_env).strip())
    lean_path = run(
        ["lake", "env", "printenv", "LEAN_PATH"], cwd=LEAN_ROOT, env=fixed_env
    ).strip()
    bwrap = Path(shutil.which("bwrap") or "")
    assert lean.is_file() and lake.is_file() and bwrap.is_file()
    assert sha256(lean) == LEAN_SHA256
    assert sha256(lake) == LAKE_SHA256
    assert sha256(bwrap) == BWRAP_SHA256
    assert LEAN_COMMIT in run([str(lean), "--version"], env=fixed_env, timeout=60)

    tmp = Path(tempfile.mkdtemp(prefix="stage1-m0405-release-", dir="/tmp")).resolve()
    try:
        for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
            shutil.copy2(HERE / name, tmp / name)
        (tmp / "home").mkdir()

        def isolated_lean(args: list[str], *, module_path: bool = False) -> str:
            path = f"{tmp}:{lean_path}" if module_path else lean_path
            return run(
                [
                    str(bwrap),
                    "--ro-bind", "/", "/",
                    "--bind", str(tmp), str(tmp),
                    "--dev", "/dev",
                    "--proc", "/proc",
                    "--unshare-net",
                    "--die-with-parent",
                    "--clearenv",
                    "--setenv", "HOME", str(tmp / "home"),
                    "--setenv", "LANG", "C.UTF-8",
                    "--setenv", "LC_ALL", "C.UTF-8",
                    "--setenv", "TZ", "UTC",
                    "--setenv", "ELAN_TOOLCHAIN", TOOLCHAIN,
                    "--setenv", "LEAN_NUM_THREADS", "1",
                    "--setenv", "LEAN_PATH", path,
                    "--chdir", str(tmp),
                    str(lean),
                    "--trust=0",
                    *args,
                ],
                env=fixed_env,
                timeout=300,
            )

        isolated_lean(["-o", "Statement.olean", "Statement.lean"])
        obligation_output = isolated_lean(
            ["-o", "ObligationTree.olean", "ObligationTree.lean"], module_path=True
        )
        proof_output = isolated_lean(
            ["-o", "Proof.olean", "Proof.lean"], module_path=True
        )
        validation_output = isolated_lean(["Validation.lean"], module_path=True)
    finally:
        shutil.rmtree(tmp)

    for short_name in OBLIGATION_DECLARATIONS:
        declaration = "Stage1.THM_M_0405." + short_name
        assert reported_axioms(obligation_output, declaration) <= EXPECTED_AXIOMS
    for short_name in PROOF_DECLARATIONS:
        declaration = "Stage1.THM_M_0405." + short_name
        assert reported_axioms(proof_output, declaration) <= EXPECTED_AXIOMS
    for short_name in VALIDATION_DECLARATIONS:
        declaration = "Stage1.THM_M_0405.Validation." + short_name
        assert reported_axioms(validation_output, declaration) <= EXPECTED_AXIOMS
    assert validation_output.count("Declarations are sorry-free!") == len(VALIDATION_DECLARATIONS)
    combined = "\n".join((obligation_output, proof_output, validation_output))
    assert "sorryAx" not in combined and "declaration uses 'sorry'" not in combined
    assert "error:" not in combined


def main() -> None:
    if sys.flags.optimize != 0:
        raise RuntimeError("release checker requires Python assertions")

    decision = load(HERE / "release-decision.json")
    receipt = load(HERE / "release-receipt.json")
    spec = load(HERE / "release-spec.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")
    instance = load(HERE / "instance.json")
    statement = load(HERE / "statement.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    proof = load(HERE / "proof-receipt.json")
    proof_blocker = load(HERE / "proof-blocker.json")
    validation = load(HERE / "validation-receipt.json")
    execution = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")
    targets = load(ROOT / "Docs" / "Stage1_Targets_rev-5.6.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target == {
        "execution_rank": 18,
        "legacy_priority_slot": "S1-M-018",
        "theorem_id": THEOREM,
        "name": "比拉斯基定理",
        "category": "数论 / 丢番图方程",
        "source_status_untrusted": "已验证",
        "baseline": "L0",
        "rework_required": True,
        "legacy_artifacts_accepted": False,
        "target_lane": "hard_mathlib_anchor_and_wrapper",
        "intake_score": 156,
        "lifecycle_mode": "planned",
        "theorem_complete": False,
    }
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item == {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 18,
        "phase": "release",
        "layer": 6,
        "state": "[ ]",
        "depends_on": ["S56-M-0405-VALIDATION"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Reconcile evidence and decide the exact theorem-completion verdict.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }
    predecessor = next(
        row for row in execution["items"] if row["id"] == "S56-M-0405-VALIDATION"
    )
    assert predecessor["state"] == "[_]" and predecessor["attempts"] == 1

    for name, expected in EXPECTED_INPUTS.items():
        assert sha256(HERE / name) == expected, f"reconciled input drifted: {name}"
    for name, expected in EXPECTED_AUTHORITY_INPUTS.items():
        assert sha256(ROOT / name) == expected, f"authority input drifted: {name}"
    for name, expected in EXPECTED_TOOL_INPUTS.items():
        assert sha256(LEAN_ROOT / name) == expected, f"tool input drifted: {name}"
    assert decision["reconciled_inputs"] == EXPECTED_INPUTS

    assert instance["lifecycle_mode"] == "planned"
    assert instance["audit_complete"] is instance["theorem_complete"] is False
    assert statement["statement_sha256"] == STATEMENT_SHA256
    assert statement["audit_complete"] is statement["theorem_complete"] is False
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert [row["obligation_id"] for row in registry["obligations"]] == INVENTORY_IDS
    assert registry["eligibility_counts"]["human_source_required"] == 11
    assert registry["status_observed_after_freeze"] == {
        "closed_obligations": [], "root_machine_debt": "M4"
    }
    closure = graphs["closure_boundary"]
    assert closure["root_machine_debt"] == "M4"
    assert closure["closed_obligations"] == []
    assert closure["minimal_open_root_cut_set"] == ["M0405-X-BHV-BRIDGE"]
    assert closure["audit_complete"] is closure["theorem_complete"] is False
    root = next(node for node in graphs["nodes"] if node["node_id"] == "M0405-ROOT")
    assert [root["human_debt"], root["machine_debt"], root["readability_debt"]] == [
        "H1", "M4", "R3"
    ]
    bad_graph_sources = [
        node for node in graphs["nodes"]
        if "Stage1_Instances/THM-M-0405/obligation-graphs.json" in node["owned_sources"]
    ]
    assert len(bad_graph_sources) == 12 and not (HERE / "obligation-graphs.json").exists()
    tree_text = (HERE / "obligation-tree.md").read_text(encoding="utf-8")
    assert "12 require\nhuman-source crosswalks" in tree_text

    assert proof["support_state"] == "provisional_worker_selftest"
    assert proof["accepted"] is False
    assert proof["supported_obligation_ids"] == []
    assert proof["provisionally_closed_obligation_ids"] == []
    assert proof["accepted_closed_obligation_ids"] == []
    assert proof["result"]["root_kernel_closed"] is False
    assert proof["result"]["theorem_complete"] is False
    assert proof["remaining_root_cut_set"] == ["M0405-X-BHV-BRIDGE"]
    assert proof_blocker["root_closed"] is proof_blocker["theorem_complete"] is False
    assert validation["support_state"] == "provisional_worker_selftest"
    assert validation["accepted"] is validation["release_grade"] is False
    assert validation["verdict"] == "blocked"
    assert validation["result"]["accepted_closed_obligation_ids"] == []
    assert validation["result"]["root_closed"] is False
    assert validation["result"]["root_machine_debt"] == "M4"
    assert validation["result"]["audit_complete"] is False
    assert validation["result"]["theorem_complete"] is False

    assert decision["item_id"] == receipt["item_id"] == ITEM
    assert decision["theorem_id"] == receipt["theorem_id"] == THEOREM
    assert decision["base_revision"] == receipt["base_revision"] == BASE_REVISION
    assert decision["base_tree"] == receipt["base_tree"] == BASE_TREE
    dependency = decision["dependency"]
    assert dependency["item_id"] == validation["item_id"]
    assert dependency["receipt_id"] == validation["receipt_id"]
    assert dependency["receipt_sha256"] == sha256(HERE / "validation-receipt.json")
    assert dependency["accepted"] is dependency["release_grade"] is False
    assert dependency["master_accepted"] is False
    result = decision["decision"]
    assert result["verdict"] == "blocked"
    assert result["lifecycle_before"] == result["lifecycle_after"] == "planned"
    assert result["root_vector_before"] == result["root_vector_after"] == {
        "H": "H1", "M": "M4", "R": "R3"
    }
    assert result["audit_complete"] is result["theorem_complete"] is False
    assert result["audit_z"] == result["theorem_z"] == "blocked"
    assert result["release_accepted"] is False
    assert result["first_failed_gate"]["gate_id"] == "S56-10.2-DEPENDENCY-ACCEPTANCE"
    assert result["first_failed_root_kernel_gate"]["obligation_id"] == "M0405-X-BHV-BRIDGE"
    assert result["first_failed_release_gate"]["gate_id"] == "S56-10.6-HERMETIC-COLD-EMPTY-CACHE"
    assert decision["accepted_receipt_ids"] == []

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by)\b|"
        r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
        r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
        r"(?:axiom|constant|opaque|unsafe|extern)\b",
        re.MULTILINE,
    )
    for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
        source = source_without_comments((HERE / name).read_text(encoding="utf-8"))
        source = source.replace("assert_no_sorry", "")
        assert prohibited.search(source) is None, f"prohibited proof construct in {name}"
    all_source = "\n".join(
        (HERE / name).read_text(encoding="utf-8")
        for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean")
    )
    assert "theorem proof : Statement" not in all_source

    manifest = load(LEAN_ROOT / "lake-manifest.json")
    mathlib_pin = next(row for row in manifest["packages"] if row["name"] == "mathlib")
    assert mathlib_pin["rev"] == mathlib_pin["inputRev"] == MATHLIB_REVISION
    assert MATHLIB.resolve().is_dir(), "pinned mathlib artifact is unavailable"
    assert git("rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert git("status", "--porcelain=v1", "--untracked-files=all", cwd=MATHLIB) == ""
    assert sha256(MATHLIB / "LICENSE") == MATHLIB_LICENSE_SHA256
    replay_lean()

    assert spec["recipe_id"] == "S56-M-0405-RELEASE-NARROW-v1"
    assert spec["item_id"] == ITEM and spec["theorem_id"] == THEOREM
    assert spec["argv"] == ["python3", "-I", "-B", f"Stage1_Instances/{THEOREM}/check_release.py"]
    assert spec["network_policy"] == "denied" and spec["expected_exit"] == 0
    assert spec["covered_obligation_ids"] == INVENTORY_IDS

    assert receipt["decision_id"] == decision["decision_id"]
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["release_grade"] is receipt["content_addressed_release_evidence"] is False
    assert receipt["result"]["verdict"] == "blocked"
    assert receipt["result"]["audit_complete"] is receipt["result"]["theorem_complete"] is False
    assert receipt["result"]["accepted_receipt_ids"] == []
    assert receipt["result"]["first_failed_gate"] == "S56-10.2-DEPENDENCY-ACCEPTANCE"
    assert receipt["result"]["first_failed_root_kernel_gate"] == "M0405-X-BHV-BRIDGE"
    assert receipt["result"]["first_failed_release_gate"] == "S56-10.6-HERMETIC-COLD-EMPTY-CACHE"
    assert receipt["inputs"]["release_spec_sha256"] == sha256(HERE / "release-spec.json")
    assert receipt["inputs"]["release_decision_sha256"] == sha256(HERE / "release-decision.json")
    assert receipt["inputs"]["release_validation_sha256"] == sha256(HERE / "release-validation.md")
    assert receipt["inputs"]["check_release_sha256"] == sha256(HERE / "check_release.py")
    for key in (
        "recipe_id", "cwd", "argv", "env_allowlist", "timeout_seconds",
        "network_policy", "expected_exit", "covered_obligation_ids", "covered_declarations",
    ):
        assert receipt["recipe"][key] == spec[key]

    assert set(packet) == {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert packet["item_id"] == ITEM and packet["base_revision"] == BASE_REVISION
    assert packet["state"] == "[_]"
    assert set(packet["changed_paths"]) == set(receipt["changed_paths"]) == CHANGED_PATHS
    assert packet["known_failures"] == decision["known_failures"] == receipt["known_failures"]
    assert packet["output_summary"] == SUMMARY_LINES == receipt["output_summary"]
    status = git("status", "--short", "--untracked-files=all")
    actual_changed = {
        line[3:] for line in status.splitlines()
        if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual_changed == CHANGED_PATHS, (actual_changed, CHANGED_PATHS)
    for relative in CHANGED_PATHS:
        assert_text_hygiene(ROOT / relative)

    for line in SUMMARY_LINES:
        print(line)


if __name__ == "__main__":
    main()
