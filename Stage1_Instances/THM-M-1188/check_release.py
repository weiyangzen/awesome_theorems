#!/usr/bin/env python3
"""Fail-closed release reconciliation for S56-M-1188-RELEASE."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-1188"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
FLT_REGULAR = LEAN_ROOT / ".lake" / "packages" / "flt-regular"
ITEM = "S56-M-1188-RELEASE"
THEOREM = "THM-M-1188"
BASE_REVISION = "a86029b30f12acc3537f70ab1c167cc25702c09b"
BASE_TREE = "ab12055e811b574338987391b59b010338c120d2"
PROOF_BASE = "309f58b7a54d36653b3483a543c6378eea53882c"
VALIDATION_BASE = "4d2c77230343716176b4192dc38e26f4c20c7547"
EXPRESSION_SHA256 = "0564abe47c982ec2eea57b707d8e761b8f00999b3d35fc307f18e406c163ffd8"
DENOMINATOR_SHA256 = "2c191411ea8f03dd1a2dcd2e206e72315fb39f01c51f6e6c146efbbe93b55ffd"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
LEAN_TOOLCHAIN = "leanprover/lean4:v4.29.0"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
FLT_REGULAR_REVISION = "56161b6eb5281fbfe9c38f2bcec0f429ebc11a27"
FLT_REGULAR_TREE = "32c9eace926573a9981787ae97643e520353c893"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
EXPECTED_TOOL_HASHES = {
    "lean": "3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf",
    "lake": "840179e70803ef373c2ec53342d6a45ea7d022533e4145489fc1278b4f716385",
    "python3": "b8d8288faefdd300201f43fcf00f6f539a27218eeed3a3dff5ab10b9c4c99700",
    "git": "8a48eefa306b9a2a9c3e576784a74ad7485779279e5a46ec43361a1864760e45",
    "bash": "3efccc187bafa75ff1e37d246270ab3e7aa559f242c7a52bf3ec2a1b5450bdbd",
    "bwrap": "0abea81db798ebf6b4742ac0664802d97521547a353c2a0dbdc21d76cbbfd2c0",
}
INVENTORY_IDS = [
    "M1188-ROOT",
    "M1188-S-DOMAIN",
    "M1188-S-BOUNDARY",
    "M1188-S-REGULARITY",
    "M1188-S-FOUNDATION",
    "M1188-C-COMPACT",
    "M1188-L-ATTAIN",
    "M1188-C-PERTURB",
    "M1188-L-SPATIAL",
    "M1188-L-TEMPORAL",
    "M1188-B-INTERIOR",
    "M1188-N-BOUNDARY",
    "M1188-L-EPSILON",
    "M1188-T-ENGINE",
    "M1188-T-ASSEMBLE",
    "M1188-X-SOURCE",
    "M1188-X-PROVENANCE",
]
PROVISIONAL_PROOF_IDS = [
    "M1188-ROOT",
    "M1188-S-DOMAIN",
    "M1188-S-BOUNDARY",
    "M1188-S-REGULARITY",
    "M1188-C-COMPACT",
    "M1188-L-ATTAIN",
    "M1188-C-PERTURB",
    "M1188-L-SPATIAL",
    "M1188-L-TEMPORAL",
    "M1188-B-INTERIOR",
    "M1188-N-BOUNDARY",
    "M1188-L-EPSILON",
    "M1188-T-ENGINE",
    "M1188-T-ASSEMBLE",
]
EXPECTED_INPUTS = {
    "Statement.lean": "1e84c9edaec0f86f93e7f8ad8e0eca243fa5ba0efa3c3cb8bfc329bff9d0a4b0",
    "ObligationTree.lean": "ae204448fee6a75acf367b43874ae3d5bb6b026d759ccabae4f04594b074b959",
    "Proof.lean": "0043ed68df3928c41f7ed189b48c970581c2aaf9c6ab4108374848ff7bde1a97",
    "Validation.lean": "cb784237e3b7e47598cadec4614a028b64ad1bf63da2c58671064690a1790e8e",
    "README.md": "41f3c2aad441878fbf2617b17bf098aabc7e027d8ece72e61f6a49ccd3d82365",
    "source_statement_crosswalk.md": "d2b9fad59f3e94c8d6d737550babf367c1b8efbc0907e937b0aa09a0c154c586",
    "intake.json": "bdd4fbea5dd89223eff75ddd9f26d21c7b1534b3dd9919f21e6e5021e64aeaf7",
    "statement.json": "5b47a6e4c1e86be177945dd151a0b903bf46dd9d467bf7340cfa6683ee7f7d6a",
    "anchor-audit.json": "84fe65f23a0c34421b25e04aaab8c85bbb71d56543b15f0fb355a9ebfdbaab86",
    "obligation-registry.json": "2edda82e85a548d5a756aaf757b9de7c9a813e4aabeea84d84e5933d7c6fa608",
    "typed-graphs.json": "02fc0a5882f0415aa8f9847fff723b556a56bddfb52b1d4c9b9921581925dda6",
    "validation-specs.json": "67871c7863cd3b43606095ecaa2c3bdd1994f86e56352119b4baa64a903058e7",
    "proof-receipt.json": "97269855a03efccc85cf372d3e2a330a1eafcda9f1eb301969dfd4ec53679388",
    "validation-spec.json": "300dc2327845d8eb8cd9f7264a1da6a8b8b831d714059544fb01e84448d1f4ae",
    "validation-receipt.json": "9ebbc4fcf30afbd03a9e15fd89a57c2b10d09d673e0aad644e29392c6712081c",
    "check_validation.py": "d674335b4183fddb3dcecb159dffb933382d6cd9467b969a181a2fe6982b1173",
    "check_validation.sh": "50eafa1e2d35630885dd6521cc1e71a8f9040874b59d4fcea9b11d53e94535a4",
}
EXPECTED_AUTHORITY_INPUTS = {
    "Docs/Stage1_Targets_rev-5.6.json": "02eec284de534dd78e1cf75f82a477ff477567dd682b7445cb7587abd137ab2c",
    "Docs/Stage1_Blueprint_rev-5.6.md": "5ffe2f390fc81a83e5258ec6d56e9c7ebc749cbe06dfe6ad309ecac9e822b276",
    "Docs/Stage1_Execution_DAG_rev-5.6.json": "61407315b2ddef583c7b13e73935eecd4e1aa86112cea3484827588af6e2250b",
    "Docs/Blueprint_Guidelines.md": "a06c07b5ca1b270b4935ad3dab893e9a0e078c29c8da2ef9dca1e71193310535",
    "skills/execute-stage1-rev56/SKILL.md": "26d47a66c6535feabb8bbf1051fd55d76a53fe761f4b3d953f86b97ec86152b8",
}
EXPECTED_TOOL_INPUTS = {
    "lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
EXPECTED_RELEASE_INPUTS = {
    "ReleaseCheck.lean": "cfe694f0087971949b6c1a59a95ba358558ee86837140cc8834b05a662f10fad",
    "release-spec.json": "9b7256a0ae9e75562d4a76988d15144632096911410490dfd955d5cefd7460bb",
    "release-decision.json": "1011ad82f5151ebe09fca9e85ed1d747eae3293d84c5d79939ff7f7da5bb523c",
    "release-validation.md": "a61263d5f855be686a9be8edb2aa1afc14f6a1b31054ccc0fc55ea0771202c1d",
}
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/ReleaseCheck.lean",
    f"Stage1_Instances/{THEOREM}/check_release.py",
    f"Stage1_Instances/{THEOREM}/release-decision.json",
    f"Stage1_Instances/{THEOREM}/release-receipt.json",
    f"Stage1_Instances/{THEOREM}/release-spec.json",
    f"Stage1_Instances/{THEOREM}/release-validation.md",
}
SUMMARY_LINES = (
    "PASS release inputs: target, DAG, predecessor receipts, frozen registry, typed graphs, and hashes agree",
    "PASS fail-closed state: lifecycle planned; accepted root H2/M3/R3; accepted receipts 0",
    "PASS current narrow replay: trust-zero, network-isolated exact root, frozen composition, validation adapters, and release adapters",
    "BLOCKED S56-10.2-DEPENDENCY-ACCEPTANCE: validation and predecessors are provisional and not master accepted",
    "BLOCKED release assurance: stale authority, H0/R0, provenance/TCB, cold offline replay, independent verification, and bundle remain open",
    "verdict=blocked audit_complete=false theorem_complete=false",
)


def load(path: Path) -> dict:
    def reject_duplicates(pairs: list[tuple[str, object]]) -> dict:
        result: dict[str, object] = {}
        for key, value in pairs:
            assert key not in result, f"duplicate key {key!r} in {path}"
            result[key] = value
        return result

    value = json.loads(
        path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicates
    )
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
    check: bool = True,
) -> subprocess.CompletedProcess[str]:
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
    if check and result.returncode != 0:
        raise RuntimeError(
            f"command failed ({result.returncode}): {argv!r}\n{result.stdout}"
        )
    return result


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["git", *args], cwd=cwd, timeout=30).stdout.strip()


def git_path_exists(revision: str, path: str) -> bool:
    result = run(
        ["git", "cat-file", "-e", f"{revision}:{path}"],
        timeout=30,
        check=False,
    )
    return result.returncode == 0


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


def pinned_artifacts_usable(manifest: dict) -> None:
    assert MATHLIB.is_dir(), "missing pinned mathlib artifact; do not fetch it"
    assert FLT_REGULAR.is_dir(), "missing pinned flt-regular artifact; do not fetch it"
    assert git("rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert git("status", "--porcelain=v1", "--untracked-files=all", cwd=MATHLIB) == ""
    assert git("rev-parse", "HEAD", cwd=FLT_REGULAR) == FLT_REGULAR_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=FLT_REGULAR) == FLT_REGULAR_TREE
    assert git("status", "--porcelain=v1", "--untracked-files=all", cwd=FLT_REGULAR) == ""
    packages = {row["name"].strip("«»"): row for row in manifest["packages"]}
    assert packages["mathlib"]["rev"] == MATHLIB_REVISION
    assert packages["flt-regular"]["rev"] == FLT_REGULAR_REVISION


def narrow_lean_replay() -> None:
    fixed_env = os.environ.copy()
    fixed_env.update(
        {
            "ELAN_TOOLCHAIN": LEAN_TOOLCHAIN,
            "LANG": "C.UTF-8",
            "LC_ALL": "C.UTF-8",
            "TZ": "UTC",
            "LEAN_NUM_THREADS": "1",
        }
    )
    lean_result = run(
        ["lake", "env", "which", "lean"], cwd=LEAN_ROOT, env=fixed_env
    )
    path_result = run(
        ["lake", "env", "printenv", "LEAN_PATH"], cwd=LEAN_ROOT, env=fixed_env
    )
    lean = Path(lean_result.stdout.strip())
    lake = Path.home() / ".elan" / "bin" / "lake"
    bwrap = Path(shutil.which("bwrap") or "")
    assert sha256(lean) == EXPECTED_TOOL_HASHES["lean"]
    assert sha256(lake) == EXPECTED_TOOL_HASHES["lake"]
    assert bwrap.is_file() and sha256(bwrap) == EXPECTED_TOOL_HASHES["bwrap"]
    assert LEAN_COMMIT in run([str(lean), "--version"], env=fixed_env).stdout
    lean_path = path_result.stdout.strip()

    with tempfile.TemporaryDirectory(
        prefix="stage1-m1188-release-", dir="/tmp"
    ) as name:
        tmp = Path(name)
        (tmp / "home").mkdir()
        for source in (
            "Statement.lean",
            "ObligationTree.lean",
            "Proof.lean",
            "Validation.lean",
            "ReleaseCheck.lean",
        ):
            shutil.copy2(HERE / source, tmp / source)

        def isolated_lean(args: list[str], *, modules: bool = False) -> str:
            module_path = f"{tmp}:{lean_path}" if modules else lean_path
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
                    "--setenv", "LEAN_NUM_THREADS", "1",
                    "--setenv", "ELAN_HOME", str(Path.home() / ".elan"),
                    "--setenv", "ELAN_TOOLCHAIN", LEAN_TOOLCHAIN,
                    "--setenv", "LEAN_PATH", module_path,
                    "--chdir", str(tmp),
                    str(lake),
                    "env",
                    "lean",
                    "--trust=0",
                    *args,
                ],
                env=fixed_env,
            ).stdout

        isolated_lean(["-o", "Statement.olean", "Statement.lean"])
        obligation_output = isolated_lean(
            ["-o", "ObligationTree.olean", "ObligationTree.lean"], modules=True
        )
        proof_output = isolated_lean(
            ["-o", "Proof.olean", "Proof.lean"], modules=True
        )
        validation_output = isolated_lean(
            ["-o", "Validation.olean", "Validation.lean"], modules=True
        )
        release_output = isolated_lean(["ReleaseCheck.lean"], modules=True)

    expected = {
        "Stage1Instances.THM_M_1188.ObligationTree.root_compose": obligation_output,
        "Stage1Instances.THM_M_1188.Proof.heatEquationWeakMaximumPrinciple": proof_output,
        "Stage1Instances.THM_M_1188.Proof.analyticMaximumEngine": proof_output,
        "Stage1Instances.THM_M_1188.Proof.assembledObligationRoot": proof_output,
        "Stage1Instances.THM_M_1188.Validation.exactCanonicalRoot": validation_output,
        "Stage1Instances.THM_M_1188.Validation.exactComposedRoot": validation_output,
        "Stage1Instances.THM_M_1188.ReleaseCheck.exactCanonicalRoot": release_output,
        "Stage1Instances.THM_M_1188.ReleaseCheck.exactComposedRoot": release_output,
    }
    for declaration, output in expected.items():
        assert reported_axioms(output, declaration) == EXPECTED_AXIOMS
    combined = obligation_output + proof_output + validation_output + release_output
    assert combined.count("Declarations are sorry-free!") == 2
    assert "sorryAx" not in combined and "declaration uses 'sorry'" not in combined
    assert "error:" not in combined


def main() -> None:
    if not __debug__:
        raise RuntimeError("release checker requires Python assertions")

    decision = load(HERE / "release-decision.json")
    receipt = load(HERE / "release-receipt.json")
    spec = load(HERE / "release-spec.json")
    validation = load(HERE / "validation-receipt.json")
    proof = load(HERE / "proof-receipt.json")
    intake = load(HERE / "intake.json")
    statement = load(HERE / "statement.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    targets = load(ROOT / "Docs" / "Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")
    manifest = load(LEAN_ROOT / "lake-manifest.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 383
    assert target["baseline"] == "L0" and target["rework_required"] is True
    assert target["legacy_artifacts_accepted"] is False
    assert target["lifecycle_mode"] == "planned" and target["theorem_complete"] is False

    release_item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert release_item == {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 383,
        "phase": "release",
        "layer": 6,
        "state": "[ ]",
        "depends_on": ["S56-M-1188-VALIDATION"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Reconcile evidence and decide the exact theorem-completion verdict.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }
    predecessor = next(
        row for row in execution["items"] if row["id"] == "S56-M-1188-VALIDATION"
    )
    assert predecessor["state"] == "[_]" and predecessor["attempts"] == 1

    for name, expected in EXPECTED_INPUTS.items():
        assert sha256(HERE / name) == expected, f"reconciled input drifted: {name}"
    for name, expected in EXPECTED_RELEASE_INPUTS.items():
        assert sha256(HERE / name) == expected, f"release input drifted: {name}"
    for name, expected in EXPECTED_AUTHORITY_INPUTS.items():
        assert sha256(ROOT / name) == expected, f"authority input drifted: {name}"
    for name, expected in EXPECTED_TOOL_INPUTS.items():
        assert sha256(LEAN_ROOT / name) == expected, f"tool input drifted: {name}"
    assert decision["reconciled_inputs"] == EXPECTED_INPUTS
    assert decision["authority_inputs"] == EXPECTED_AUTHORITY_INPUTS
    assert decision["base_revision"] == BASE_REVISION
    assert decision["base_tree"] == BASE_TREE
    assert decision["item_id"] == ITEM and decision["theorem_id"] == THEOREM
    assert decision["execution_rank"] == 383
    assert decision["phase"] == decision["intent"] == "release"
    assert decision["decision_support"] == "provisional_worker_selftest"
    assert decision["proposed_state"] == "[_]" and decision["release_grade"] is False
    assert decision["content_addressed_release_evidence"] is False
    assert "content-binds the checker and worker packet" in decision["mutable_handoff_binding_boundary"]

    dependency = decision["dependency"]
    assert dependency["item_id"] == validation["item_id"] == predecessor["id"]
    assert dependency["receipt_id"] == validation["receipt_id"]
    assert dependency["receipt_sha256"] == sha256(HERE / "validation-receipt.json")
    assert dependency["receipt_base_revision"] == validation["base_revision"] == VALIDATION_BASE
    assert dependency["support_state"] == validation["support_state"]
    assert dependency["accepted"] is validation["accepted"] is False
    assert dependency["release_grade"] is validation["release_grade"] is False
    assert dependency["master_accepted"] is False

    assert spec["schema_version"] == "stage1-validation-recipe/1.0"
    assert spec["item_id"] == ITEM and spec["theorem_id"] == THEOREM
    assert spec["argv"] == [
        "python3", "-I", "-B", f"Stage1_Instances/{THEOREM}/check_release.py"
    ]
    assert spec["cwd"] == "." and spec["env_allowlist"] == {}
    assert spec["timeout_seconds"] == 600 and spec["network_policy"] == "denied"
    assert spec["expected_exit"] == 0
    assert spec["covered_obligation_ids"] == INVENTORY_IDS
    assert spec["covered_decisions"] == ["AUDIT-Z", "THEOREM-Z"]

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["phase"] == receipt["intent"] == "release"
    assert receipt["depends_on"] == [predecessor["id"]]
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]"
    assert receipt["accepted"] is receipt["release_grade"] is False
    assert receipt["master_accepted"] is receipt["content_addressed_release_evidence"] is False
    assert "validator, and root worker packet are content-bound" in receipt["mutable_handoff_binding_boundary"]
    assert "integration lane" in receipt["mutable_handoff_binding_boundary"]
    assert receipt["decision_id"] == decision["decision_id"]
    assert decision["node_receipt_id"] == receipt["receipt_id"]
    assert receipt["verdict"] == "blocked"
    assert receipt["canonical_obligation_ids"] == INVENTORY_IDS
    assert receipt["accepted_receipt_ids"] == []
    for relative, expected in receipt["input_bindings"].items():
        assert sha256(ROOT / relative) == expected, f"receipt input drifted: {relative}"
    expected_bindings = {
        **{f"Stage1_Instances/{THEOREM}/{name}": digest for name, digest in EXPECTED_INPUTS.items()},
        **{f"Stage1_Instances/{THEOREM}/{name}": digest for name, digest in EXPECTED_RELEASE_INPUTS.items()},
        **EXPECTED_AUTHORITY_INPUTS,
        **{f"Formalizations/Lean/{name}": digest for name, digest in EXPECTED_TOOL_INPUTS.items()},
    }
    assert receipt["input_bindings"] == expected_bindings
    for key in (
        "recipe_id", "cwd", "argv", "env_allowlist", "timeout_seconds",
        "network_policy", "network_enforcement", "expected_exit",
    ):
        assert receipt["recipe"][key] == spec[key], key

    assert intake["lifecycle_mode"] == "planned" and intake["theorem_complete"] is False
    assert statement["canonical_formal_target"]["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert registry["root_obligation_id"] == graphs["root_node_id"] == "M1188-ROOT"
    assert registry["denominator_sha256"] == graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert registry["frozen_denominators"]["inventory"] == INVENTORY_IDS
    closure = graphs["closure_boundary"]
    assert closure["root_closed"] is closure["audit_complete"] is closure["theorem_complete"] is False
    assert closure["closed_obligations"] == []
    root = next(node for node in graphs["nodes"] if node["obligation_id"] == "M1188-ROOT")
    assert root["machine_debt"] == "M3" and root["human_debt"] == "H2"
    assert root["readability_debt"] == "R3" and root["evidence_ids"] == []
    assert root["provenance_id"] == "none" and root["owned_sources"] == []

    assert proof["base_revision"] == PROOF_BASE and proof["accepted"] is False
    assert proof["provisionally_closed_obligation_ids"] == PROVISIONAL_PROOF_IDS
    assert proof["accepted_closed_obligation_ids"] == []
    assert proof["result"]["root_kernel_closed"] is True
    assert proof["result"]["accepted_root_closed"] is False
    assert proof["result"]["theorem_complete"] is False
    assert not git_path_exists(PROOF_BASE, f"Stage1_Instances/{THEOREM}/Proof.lean")
    assert validation["accepted_closed_obligation_ids"] == []
    assert validation["result"]["exact_root_kernel_replay"] == "provisional_pass"
    assert validation["result"]["audit_complete"] is validation["result"]["theorem_complete"] is False
    assert not git_path_exists(VALIDATION_BASE, f"Stage1_Instances/{THEOREM}/Validation.lean")

    result = decision["decision"]
    assert result["verdict"] == "blocked"
    assert result["lifecycle_before"] == result["lifecycle_after"] == "planned"
    assert result["root_vector_before"] == result["root_vector_after"] == ["H2", "M3", "R3"]
    assert result["audit_complete"] is result["theorem_complete"] is False
    assert result["audit_z"] == result["theorem_z"] == "blocked"
    assert result["release_accepted"] is False
    assert decision["accepted_receipt_ids"] == []
    assert result["first_failed_gate"]["gate_id"] == "S56-10.2-DEPENDENCY-ACCEPTANCE"
    assert result["first_failed_theorem_gate"]["gate_id"] == "S56-THEOREM-AUTHORITATIVE-M0-RECONCILIATION"
    assert result["first_failed_release_specific_gate"]["gate_id"] == "S56-RELEASE-IMMUTABLE-CLEAN-INPUT"
    assert result["next_failed_release_gate"]["gate_id"] == "S56-10.6-HERMETIC-COLD-BUILD"

    reconciliation = decision["evidence_reconciliation"]
    assert reconciliation["provisional_exact_root_kernel_closure"] is True
    for key in (
        "accepted_exact_root_kernel_closure",
        "typed_authority_reconciled",
        "node_specific_receipts_complete",
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
    assert reconciliation["accepted_closed_obligations"] == []

    all_source = "\n".join(
        source_without_comments((HERE / name).read_text(encoding="utf-8"))
        for name in (
            "Statement.lean", "ObligationTree.lean", "Proof.lean",
            "Validation.lean", "ReleaseCheck.lean",
        )
    )
    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by)\b|"
        r"^[ \t]*(?:axiom|constant|opaque|unsafe|extern)\b",
        re.MULTILINE,
    )
    assert prohibited.search(all_source) is None
    for name in (*EXPECTED_RELEASE_INPUTS, "release-receipt.json"):
        assert_text_hygiene(HERE / name)
    assert_text_hygiene(Path(__file__).resolve())

    executables = {
        "python3": Path(os.path.realpath(shutil.which("python3") or "")),
        "git": Path(os.path.realpath(shutil.which("git") or "")),
        "bash": Path(os.path.realpath(shutil.which("bash") or "")),
        "bwrap": Path(os.path.realpath(shutil.which("bwrap") or "")),
    }
    for name, path in executables.items():
        assert path.is_file() and sha256(path) == EXPECTED_TOOL_HASHES[name], (name, path)
    pinned_artifacts_usable(manifest)
    narrow_lean_replay()
    replay_result = (
        "provisional_pass_trust_zero_network_isolated_fresh_output_for_exact_root_"
        "frozen_composition_validation_adapters_and_release_adapters"
    )
    assert reconciliation["current_release_narrow_lean_replay"] == replay_result
    assert receipt["result"]["current_release_narrow_lean_replay"] == replay_result

    packet_path = ROOT / ".stage1-worker-selftest.json"
    if packet_path.exists():
        packet = load(packet_path)
        assert set(packet) == {
            "item_id", "changed_paths", "commands", "output_summary",
            "base_revision", "known_failures", "state",
        }
        assert packet["item_id"] == ITEM and packet["state"] == "[_]"
        assert packet["base_revision"] == BASE_REVISION
        assert set(packet["changed_paths"]) == CHANGED_PATHS
        assert packet["known_failures"] == receipt["known_failures"]
        assert packet["output_summary"] == receipt["output_summary"]
        assert_text_hygiene(packet_path)
        handoff_hashes = receipt["nonrelease_handoff_hashes"]
        assert handoff_hashes["validator_sha256"] == sha256(Path(__file__).resolve())
        assert handoff_hashes["worker_packet_sha256"] == sha256(packet_path)
        status = git("status", "--short", "--untracked-files=all")
        actual_changes = {
            line[3:] for line in status.splitlines()
            if line[3:] != "Formalizations/Lean/.lake"
        }
        assert actual_changes == CHANGED_PATHS, (actual_changes, CHANGED_PATHS)

        with tempfile.TemporaryDirectory(
            prefix="stage1-m1188-index-", dir="/tmp"
        ) as index_dir:
            index_file = Path(index_dir) / "index"
            index_env = os.environ.copy()
            index_env["GIT_INDEX_FILE"] = str(index_file)
            run(["git", "read-tree", "HEAD"], env=index_env, timeout=30)
            run(
                ["git", "add", "--intent-to-add", "--", *sorted(CHANGED_PATHS)],
                env=index_env,
                timeout=30,
            )
            diff_check = run(
                ["git", "diff", "--check", "--", *sorted(CHANGED_PATHS)],
                env=index_env,
                timeout=30,
            )
            assert diff_check.stdout == ""

    print("\n".join(SUMMARY_LINES))


if __name__ == "__main__":
    main()
