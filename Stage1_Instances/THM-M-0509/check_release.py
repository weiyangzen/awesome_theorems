#!/usr/bin/env python3
"""Fail-closed release reconciliation for S56-M-0509-RELEASE."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import platform
import re
import shutil
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0509"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
ITEM = "S56-M-0509-RELEASE"
THEOREM = "THM-M-0509"
BASE_REVISION = "350285c48208616b6e3ad74154d9183d16523cfa"
BASE_TREE = "c4edebc115ec954e4940ed5faaa3ffacd4e56091"
VALIDATION_BASE_REVISION = "229ca98e7478d389ccf8de8173c94e0e7c8fe670"
VALIDATION_BASE_TREE = "d3cc9562940b923aebbe7e01ce66232079760b3b"
VALIDATION_RECEIPT_SHA256 = (
    "e7724b9dc147cdabceab1c76e9b27e379843bf8e44de2e9459ec1a8f7d447613"
)
TOOLCHAIN = "leanprover/lean4:v4.29.0"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MATHLIB_REMOTE = "https://github.com/leanprover-community/mathlib4.git"
MATHLIB_LICENSE_SHA256 = (
    "b40930bbcf80744c86c46a12bc9da056641d722716c378f5659b9e555ef833e1"
)
EXPRESSION_SHA256 = "e2c8d3782d80648aa229dab05f90a84506ed5b6f213fa3083e312674aa6c64f7"
DENOMINATOR_SHA256 = "74b4c30d82e3aa7c44f356d24eb5cd21c2d48ce06e53898a12333504350703bd"
VECTOR = {"H": "H1", "M": "M4", "R": "R4"}
INVENTORY_IDS = [
    "M0509-ROOT", "M0509-S-DEFINITIONS", "M0509-S-BOUNDARY",
    "M0509-S-FOUNDATION", "M0509-C-REPRESENTATION",
    "M0509-S-SIEVE-SETUP", "M0509-N-DISTRIBUTION",
    "M0509-L-WEIGHTED-SIEVE", "M0509-L-SWITCHING",
    "M0509-L-REMAINDER", "M0509-T-POSITIVITY",
    "M0509-T-P2-EXTRACTION", "M0509-T-ASSEMBLE",
    "M0509-X-SOURCE", "M0509-X-PROVENANCE",
]
MATHEMATICAL_CUT = ["M0509-T-P2-EXTRACTION"]
GRAPH_CLOSED_IDS = [
    "M0509-S-BOUNDARY", "M0509-S-DEFINITIONS", "M0509-T-ASSEMBLE",
]
DECISION_GRAPH_CLOSED_IDS = [
    "M0509-S-DEFINITIONS", "M0509-S-BOUNDARY", "M0509-T-ASSEMBLE",
]
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
EXPECTED_OUTPUT_SHA256 = {
    "statement": "ea1d26e07a15f888e20c8f1215bc9cf1215e510fd54f8ada36971790d6b11a8c",
    "obligation": "3f0adca66e9e4cf80cadd3b1328514c601c0ac93696def89df292fede9bd8b74",
    "proof": "c4f2930fec852cfa7fb582b0bdcbdd0026b32a3aa1dd5f320adb7cc4144742b4",
    "validation": "6e31fdcd6a37ee04b8c2c6100df1e62a46b1082c856dea3baaf35ba62b9e64d3",
}
EXPECTED_INPUTS = {
    "README.md": "8627c7381963a8418c3ee5cd566d18c55edf0fbd34cd2b14b89457a5d582f220",
    "scope-map.md": "f355a0a8e3fe78ef930a79422e9419e588a56cb3d16fad4815747834f6fe8e8a",
    "source-statement-crosswalk.md": "d5b526645cf8da7af710819aa0cdaf0a7fdd53d2c90bf8048b37e6fc8f91b402",
    "instance.json": "31297cb5449dfd1773fcadce2cded5ca22cec345bcee6dc1cbc074510c1115e4",
    "task-dag.json": "6f720a26fff6b245da7a7f645be23cd55c9006fadd6ee05bac7a5434b3cf9905",
    "Statement.lean": "fe4685daeb9747b01adb0d896c293c167c2e763a0c1f5b9130e80eb1afa776a9",
    "AnchorAudit.lean": "97508a37bc81c8ebf97d09a407f88f1be7e219ac96efd66717e4b5f8bc9a93e4",
    "ObligationTree.lean": "6af99da9bbe9840cb3e3d51c6544c4452deab4b7f4bf13ad3dd0fe9079215dd4",
    "Proof.lean": "20f0ca7f8822a590fdbb3c3b9ad2b4e375aebe3e8357244e00f7dc655f896428",
    "Validation.lean": "7860acf5382248aa1173c917d56f1dc611332339e886695c2cd340feff14ac13",
    "statement.json": "4873c32b63234d892a49fe4724a1eaee96cdb18097ca933af544c2dd9a74636b",
    "anchor-audit.json": "36afc1d91251bfae073fff8f29eee977844b4e957c93065dab6ff7d86a4c5dd7",
    "obligation-registry.json": "e8430fa07323ff530331012a6cc75b96df84302ce3c215e3832aca6aabb6eb13",
    "obligation-tree-receipt.json": "5a140ba40bbdb4987518af0a90d87ccf771db63e05337f274bebd8148c8c54fd",
    "typed-graphs.json": "549160e15c5ef40e3644142a7745e9e011f3bb3fe0f3a4f2598dd3b5836d1bff",
    "proof-receipt.json": "8264c431575417e4e69b543b06b373a3fa75960fff139c283dd93ade9881ba0e",
    "proof-blocker.json": "db05852bd2ea8c2240d55c44866906d7613329b0603221c9c3f0b4a5c8658266",
    "validation-spec.json": "de34e1d5be6ec5a20b78adf2545bcc13c33e6f711175678b5e8fa099631e6c51",
    "validation-receipt.json": VALIDATION_RECEIPT_SHA256,
    "validation-blocker.json": "538a5b5260aba46daccc1861586c33be620df49514efc1bf21f9a81720da3e69",
    "check_validation.py": "b091a2f52699d40aeb62d1ec963aaa8e46ac9cf640af00dce78352a71562e322",
}
AUTHORITY_INPUTS = {
    "Docs/Stage1_Targets_rev-5.6.json": "02eec284de534dd78e1cf75f82a477ff477567dd682b7445cb7587abd137ab2c",
    "Docs/Stage1_Execution_DAG_rev-5.6.json": "27996ce44b0352923f10f0150728d7db409b5f928d4aaf36ff1f69ce29ee4320",
    "Docs/Stage1_Blueprint_rev-5.6.md": "6640881cb112fdd384daa1a016588ca4b4c254d8237e92fcc34b40f3d0557942",
    "Docs/Blueprint_Guidelines.md": "a06c07b5ca1b270b4935ad3dab893e9a0e078c29c8da2ef9dca1e71193310535",
    "skills/execute-stage1-rev56/SKILL.md": "26d47a66c6535feabb8bbf1051fd55d76a53fe761f4b3d953f86b97ec86152b8",
    "Formalizations/Lean/lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "Formalizations/Lean/lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
RELEASE_NAMES = (
    "check_release.py", "release-decision.json", "release-receipt.json",
    "release-spec.json", "release-validation.md",
)
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    *(f"Stage1_Instances/{THEOREM}/{name}" for name in RELEASE_NAMES),
}
SUMMARY_LINES = [
    "PASS S56-M-0509-RELEASE negative reconciliation",
    "PASS current trust-zero replay: exact interfaces and conditional compositions only",
    "BLOCKED dependency.S56-M-0509-VALIDATION.master_acceptance",
    "BLOCKED exact root: H1/M4/R4 unchanged; M0509-T-P2-EXTRACTION remains open",
    "BLOCKED AUDIT-Z and THEOREM-Z: source, state, trust, hermetic, and independent gates open",
    "verdict=blocked audit_complete=false theorem_complete=false accepted_receipts=0",
]


def load(path: Path) -> dict:
    def reject_duplicates(pairs: list[tuple[str, object]]) -> dict:
        value: dict[str, object] = {}
        for key, item in pairs:
            assert key not in value, f"duplicate JSON key in {path}: {key}"
            value[key] = item
        return value

    result = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicates)
    assert isinstance(result, dict), path
    return result


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(
    argv: list[str], *, cwd: Path = ROOT, env: dict[str, str] | None = None,
    timeout: int = 600,
) -> str:
    result = subprocess.run(
        argv, cwd=cwd, env=env, text=True, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, timeout=timeout, check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(f"command failed ({result.returncode}): {argv!r}\n{result.stdout}")
    return result.stdout


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["git", *args], cwd=cwd, timeout=60).strip()


def code_without_comments(source: str) -> str:
    output: list[str] = []
    index = 0
    depth = 0
    in_string = False
    while index < len(source):
        if depth:
            if source.startswith("/-", index):
                depth += 1
                index += 2
            elif source.startswith("-/", index):
                depth -= 1
                index += 2
            else:
                index += 1
        elif in_string:
            if source[index] == "\\" and index + 1 < len(source):
                index += 2
            elif source[index] == '"':
                in_string = False
                output.append('"')
                index += 1
            else:
                index += 1
        elif source.startswith("/-", index):
            depth = 1
            index += 2
        elif source.startswith("--", index):
            newline = source.find("\n", index)
            index = len(source) if newline < 0 else newline
        elif source[index] == '"':
            in_string = True
            output.append('"')
            index += 1
        else:
            output.append(source[index])
            index += 1
    assert depth == 0 and not in_string, "unterminated Lean comment or string"
    return "".join(output)


def reported_axioms(output: str, declaration: str) -> set[str]:
    match = re.search(
        rf"'[^']*{re.escape(declaration)}' depends on axioms:\s*\[(.*?)\]",
        output,
        flags=re.DOTALL,
    )
    if match is None:
        assert f"'{declaration}' does not depend on any axioms" in output
        return set()
    return {
        part.strip()
        for part in match.group(1).replace("\n", "").split(",")
        if part.strip()
    }


def assert_text_hygiene(path: Path) -> None:
    data = path.read_bytes()
    assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data, path
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines()), path


def compiled_roots() -> list[Path]:
    packages = LEAN_ROOT / ".lake" / "packages"
    roots = sorted(
        (path / ".lake" / "build" / "lib" / "lean").resolve()
        for path in packages.iterdir()
        if path.is_dir() and (path / ".lake" / "build" / "lib" / "lean").is_dir()
    )
    assert roots, "no pre-existing pinned compiled artifacts"
    return roots


def current_lean_replay() -> dict[str, object]:
    fixed_env = {
        "ELAN_TOOLCHAIN": TOOLCHAIN,
        "LANG": "C.UTF-8",
        "LC_ALL": "C.UTF-8",
        "TZ": "UTC",
        "LEAN_NUM_THREADS": "1",
    }
    bwrap_name = shutil.which("bwrap")
    assert bwrap_name is not None
    bwrap = Path(bwrap_name).resolve()
    tool_root = Path.home() / ".elan" / "toolchains" / "leanprover--lean4---v4.29.0" / "bin"
    lean = tool_root / "lean"
    lake = tool_root / "lake"
    assert LEAN_COMMIT in run([str(lean), "--version"], env=fixed_env)
    assert "5.0.0-src+98dc76e" in run([str(lake), "--version"], env=fixed_env)
    mathlib = (LEAN_ROOT / ".lake" / "packages" / "mathlib").resolve()
    dependency_path = ":".join(str(path) for path in compiled_roots())

    with tempfile.TemporaryDirectory(prefix="m0509-release-", dir="/tmp") as name:
        tmp = Path(name).resolve()
        for source in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
            (tmp / source).write_bytes((HERE / source).read_bytes())
        base = [
            str(bwrap), "--ro-bind", "/", "/", "--bind", str(tmp), str(tmp),
            "--dev", "/dev", "--proc", "/proc", "--unshare-net",
            "--die-with-parent", "--clearenv", "--setenv", "HOME", str(tmp),
            "--setenv", "TMPDIR", str(tmp), "--setenv", "LANG", "C.UTF-8",
            "--setenv", "LC_ALL", "C.UTF-8", "--setenv", "TZ", "UTC",
            "--setenv", "LEAN_NUM_THREADS", "1", "--chdir", str(mathlib),
        ]

        def lean_run(source: str, local_imports: bool, emit_olean: bool) -> str:
            lean_path = f"{tmp}:{dependency_path}" if local_imports else dependency_path
            argv = base + [
                "--setenv", "LEAN_PATH", lean_path, str(lake), "env", "lean",
                "--trust=0", f"--root={tmp}",
            ]
            if emit_olean:
                argv += ["-o", str(tmp / Path(source).with_suffix(".olean"))]
            argv.append(str(tmp / source))
            return run(argv, env=fixed_env)

        outputs = {
            "statement": lean_run("Statement.lean", False, True),
            "obligation": lean_run("ObligationTree.lean", True, True),
            "proof": lean_run("Proof.lean", True, True),
            "validation": lean_run("Validation.lean", True, False),
        }

    assert {
        key: hashlib.sha256(value.encode()).hexdigest() for key, value in outputs.items()
    } == EXPECTED_OUTPUT_SHA256
    proof_declarations = (
        "Stage1Instances.THM_M_0509.Proof.isP2_iff_cardFactors_pos_le_two",
        "Stage1Instances.THM_M_0509.Proof.representationCount_pos_iff",
        "Stage1Instances.THM_M_0509.Proof.chenTheoremTarget_iff_eventualPositiveRepresentationCount",
    )
    for declaration in proof_declarations:
        assert reported_axioms(outputs["proof"], declaration) == EXPECTED_AXIOMS
        assert reported_axioms(outputs["validation"], declaration) == EXPECTED_AXIOMS
    assert reported_axioms(
        outputs["obligation"], "Stage1Instances.THM_M_0509.root_of_sieve_package",
    ) == {"propext"}
    assert reported_axioms(
        outputs["validation"],
        "Stage1Instances.THM_M_0509.Validation.rootFromEventualPositiveCount",
    ) == EXPECTED_AXIOMS
    combined = "\n".join(outputs.values())
    assert "sorryAx" not in combined and "declaration uses 'sorry'" not in combined
    assert all("error:" not in output for output in outputs.values())
    closure = re.search(
        r"VALIDATION_CLOSURE roots=(\d+) declarations=(\d+) modules=(\d+)",
        outputs["validation"],
    )
    assert closure is not None and int(closure.group(1)) == 5
    assert "VALIDATION_CLOSURE axioms=[propext, Classical.choice, Quot.sound]" in outputs["validation"]
    assert "VALIDATION_CLOSURE bodyless_nonaxioms=[]" in outputs["validation"]
    assert "VALIDATION_CLOSURE unsafe=[]" in outputs["validation"]
    return {
        "output_sha256": EXPECTED_OUTPUT_SHA256,
        "closure": {
            "roots": 5,
            "declarations": int(closure.group(2)),
            "modules": int(closure.group(3)),
            "axioms": sorted(EXPECTED_AXIOMS),
            "bodyless_nonaxioms": [],
            "unsafe_declarations": [],
        },
    }


def main() -> None:
    if not __debug__ or sys.flags.optimize != 0:
        raise RuntimeError("release checker requires Python assertions")

    decision = load(HERE / "release-decision.json")
    receipt = load(HERE / "release-receipt.json")
    spec = load(HERE / "release-spec.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")
    instance = load(HERE / "instance.json")
    local_dag = load(HERE / "task-dag.json")
    statement = load(HERE / "statement.json")
    registry = load(HERE / "obligation-registry.json")
    tree_receipt = load(HERE / "obligation-tree-receipt.json")
    graphs = load(HERE / "typed-graphs.json")
    proof = load(HERE / "proof-receipt.json")
    validation = load(HERE / "validation-receipt.json")
    targets = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    manifest = load(LEAN_ROOT / "lake-manifest.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    assert run([
        "git", "merge-base", "--is-ancestor", VALIDATION_BASE_REVISION, BASE_REVISION,
    ]) == ""
    assert git("rev-parse", f"{VALIDATION_BASE_REVISION}^{{tree}}") == VALIDATION_BASE_TREE
    for name, expected in EXPECTED_INPUTS.items():
        assert sha256(HERE / name) == expected, f"reconciled input drifted: {name}"
    assert decision["reconciled_inputs"] == EXPECTED_INPUTS
    for name, expected in AUTHORITY_INPUTS.items():
        assert sha256(ROOT / name) == expected, f"authority input drifted: {name}"
    assert decision["authority_inputs"] == AUTHORITY_INPUTS

    target_rows = [row for row in targets["targets"] if row["theorem_id"] == THEOREM]
    assert len(target_rows) == 1
    target = target_rows[0]
    assert target["execution_rank"] == 883
    assert target["baseline"] == "L0" and target["rework_required"] is True
    assert target["legacy_artifacts_accepted"] is False
    assert target["lifecycle_mode"] == "planned" and target["theorem_complete"] is False
    items = {row["id"]: row for row in execution["items"]}
    assert items[ITEM] == {
        "id": ITEM, "theorem_id": THEOREM, "execution_rank": 883,
        "phase": "release", "layer": 6, "state": "[ ]",
        "depends_on": ["S56-M-0509-VALIDATION"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Reconcile evidence and decide the exact theorem-completion verdict.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0, "children": [],
    }
    assert items["S56-M-0509-VALIDATION"]["state"] == "[_]"
    assert items["S56-M-0509-VALIDATION"]["attempts"] == 1

    assert instance["lifecycle"] == local_dag["lifecycle"] == "planned"
    assert instance["root_vector"] == VECTOR
    assert instance["accepted_proof_state"] == []
    assert instance["audit_complete"] is instance["theorem_complete"] is False
    assert local_dag["accepted_states"] == []
    local_tasks = {row["id"]: row for row in local_dag["tasks"]}
    assert local_tasks[ITEM] == {
        "id": ITEM, "depends_on": ["S56-M-0509-VALIDATION"], "state": "open",
    }
    assert local_tasks["S56-M-0509-VALIDATION"]["state"] == "open"

    formal = statement["canonical_formal_target"]
    assert formal["declaration_or_expression"] == (
        "Stage1Instances.THM_M_0509.ChenTheoremTarget"
    )
    assert formal["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert formal["statement_file_sha256"] == EXPECTED_INPUTS["Statement.lean"]
    assert registry["root_obligation_id"] == "M0509-ROOT"
    assert registry["frozen_denominators"]["inventory"] == INVENTORY_IDS
    assert [row["obligation_id"] for row in registry["obligations"]] == INVENTORY_IDS
    assert graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert [row["obligation_id"] for row in graphs["nodes"]] == INVENTORY_IDS
    root = next(row for row in graphs["nodes"] if row["obligation_id"] == "M0509-ROOT")
    assert {
        "H": root["human_debt"], "M": root["machine_debt"], "R": root["readability_debt"],
    } == VECTOR
    assert root["evidence_ids"] == []
    closure = graphs["closure_boundary"]
    assert closure["closed_obligations"] == GRAPH_CLOSED_IDS
    assert closure["root_closed"] is False
    assert closure["audit_complete"] is closure["theorem_complete"] is False
    assert closure["remaining_root_cut_set"] == MATHEMATICAL_CUT
    assert all(row["evidence_ids"] == [] for row in graphs["nodes"])
    assert tree_receipt["closed_obligations"] == []
    assert tree_receipt["audit_complete"] is tree_receipt["theorem_complete"] is False

    assert proof["support_state"] == "provisional_worker_selftest"
    assert proof["accepted"] is False
    assert proof["provisionally_closed_obligation_ids"] == []
    assert proof["accepted_closed_obligation_ids"] == []
    assert proof["result"]["root_kernel_closed"] is False
    assert proof["remaining_root_cut_set"] == MATHEMATICAL_CUT
    assert sha256(HERE / "validation-receipt.json") == VALIDATION_RECEIPT_SHA256
    assert validation["base_revision"] == VALIDATION_BASE_REVISION
    assert validation["base_tree"] == VALIDATION_BASE_TREE
    assert validation["support_state"] == "provisional_worker_selftest"
    assert validation["accepted"] is validation["release_grade"] is False
    assert validation["accepted_receipt_ids"] == []
    assert validation["result"]["accepted_closed_obligation_ids"] == []
    assert validation["result"]["root_kernel_closed"] is False
    assert validation["result"]["open_root_cut_set"] == MATHEMATICAL_CUT
    assert validation["result"]["audit_complete"] is validation["result"]["theorem_complete"] is False
    assert validation["first_failed_gate"] == "dependency.S56-M-0509-PROOF.master_acceptance"
    predecessor = (HERE / "check_validation.py").read_text(encoding="utf-8")
    assert f'BASE_REVISION = "{VALIDATION_BASE_REVISION}"' in predecessor
    assert '"state": "[ ]"' in predecessor and '"attempts": 0' in predecessor
    assert '"--worker-packet", ".stage1-worker-selftest.json"' in predecessor

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by|extern)\b|"
        r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
        r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
        r"(?:axiom|constant|opaque|unsafe)\b",
        re.MULTILINE,
    )
    for name in ("Statement.lean", "AnchorAudit.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
        source = code_without_comments((HERE / name).read_text(encoding="utf-8"))
        source = re.sub(r"^#print sorries .*?$", "", source, flags=re.MULTILINE)
        assert prohibited.search(source) is None, f"prohibited source construct in {name}"
    proof_source = code_without_comments((HERE / "Proof.lean").read_text(encoding="utf-8"))
    assert "def EventualPositiveRepresentationCount : Prop" in proof_source
    assert re.search(r"(?:theorem|def)\s+eventualPositiveRepresentationCount\b", proof_source) is None
    validation_source = code_without_comments((HERE / "Validation.lean").read_text(encoding="utf-8"))
    assert "(positive : EventualPositiveRepresentationCount)" in validation_source

    mathlib_rows = [row for row in manifest["packages"] if row["name"] == "mathlib"]
    assert len(mathlib_rows) == 1
    mathlib_entry = mathlib_rows[0]
    assert mathlib_entry["rev"] == mathlib_entry["inputRev"] == MATHLIB_REVISION
    assert (LEAN_ROOT / ".lake").is_symlink()
    mathlib = (LEAN_ROOT / ".lake" / "packages" / "mathlib").resolve()
    assert git("rev-parse", "HEAD", cwd=mathlib) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == MATHLIB_TREE
    assert git("status", "--porcelain=v1", "--untracked-files=all", cwd=mathlib) == ""
    assert git("remote", "get-url", "origin", cwd=mathlib) == MATHLIB_REMOTE
    assert sha256(mathlib / "LICENSE") == MATHLIB_LICENSE_SHA256
    observation = current_lean_replay()
    assert observation["closure"] == {
        "roots": 5, "declarations": 5203, "modules": 200,
        "axioms": ["Classical.choice", "Quot.sound", "propext"],
        "bodyless_nonaxioms": [], "unsafe_declarations": [],
    }

    assert decision["schema_version"] == "stage1-release-decision/1.0"
    assert decision["item_id"] == ITEM and decision["theorem_id"] == THEOREM
    assert decision["phase"] == decision["intent"] == "release"
    assert decision["base_revision"] == BASE_REVISION and decision["base_tree"] == BASE_TREE
    assert decision["verdict"] == "blocked"
    assert decision["release_grade"] is decision["release_accepted"] is False
    assert decision["lifecycle_before"] == decision["lifecycle_after"] == "planned"
    assert decision["accepted_receipt_ids"] == decision["accepted_closed_obligation_ids"] == []
    assert decision["root_vector"] == {"before": VECTOR, "after": VECTOR}
    assert decision["terminal_decisions"] == {
        "audit_complete": False, "theorem_complete": False,
        "audit_z": "blocked", "theorem_z": "blocked", "release_accepted": False,
    }
    assert decision["first_failed_gate"]["gate_id"] == "S56-10.2-DEPENDENCY-ACCEPTANCE"
    assert decision["first_failed_gate"]["dependency_gate"] == (
        "dependency.S56-M-0509-VALIDATION.master_acceptance"
    )
    assert decision["nested_predecessor_failure"]["gate_id"] == (
        "dependency.S56-M-0509-PROOF.master_acceptance"
    )
    assert decision["first_failed_theorem_gate"]["gate_id"] == "M0509-T-P2-EXTRACTION"
    assert decision["first_failed_reproduction_gate"]["gate_id"] == (
        "S56-10.6-HERMETIC-COLD-EMPTY-CACHE"
    )
    assert decision["mathematical_root_cut_set"] == MATHEMATICAL_CUT
    dependency = decision["dependency"]
    assert dependency["receipt_id"] == validation["receipt_id"]
    assert dependency["receipt_sha256"] == VALIDATION_RECEIPT_SHA256
    assert dependency["accepted"] is dependency["master_accepted"] is False
    reconciliation = decision["evidence_reconciliation"]
    assert reconciliation["accepted_closed_obligation_ids"] == []
    assert reconciliation["typed_graph_claimed_closed_obligation_ids"] == (
        DECISION_GRAPH_CLOSED_IDS
    )
    assert set(DECISION_GRAPH_CLOSED_IDS) == set(GRAPH_CLOSED_IDS)
    assert reconciliation["obligation_receipt_closed_obligation_ids"] == []
    assert reconciliation["proof_and_validation_accepted_closed_obligation_ids"] == []
    for key in (
        "validation_dependency_master_accepted", "exact_root_kernel_closed",
        "structured_public_state_reconciled", "pinpoint_h0_and_independent_source_review",
        "independent_r0_review", "audit_z_accepted", "accepted_foundation_profile",
        "complete_transitive_provenance_and_tcb", "immutable_clean_release_input",
        "hermetic_empty_cache_cold_offline_replay", "complete_sbom_license_archive_closure",
        "two_independent_signed_runner_attestations", "independently_implemented_minimal_verifier",
        "protected_ci_and_adversarial_gates", "deterministic_content_addressed_release_bundle",
        "master_acceptance",
    ):
        assert reconciliation[key] is False, key

    assert spec["schema_version"] == "stage1-release-recipe/1.0"
    assert spec["item_id"] == receipt["item_id"] == ITEM
    assert spec["theorem_id"] == receipt["theorem_id"] == THEOREM
    assert spec["argv"] == [
        "/usr/bin/python3", "-I", "-B", f"Stage1_Instances/{THEOREM}/check_release.py",
    ]
    assert spec["cwd"] == "." and spec["timeout_seconds"] == 600
    assert spec["network_policy"] == "denied" and spec["expected_exit"] == 0
    assert spec["covered_obligation_ids"] == []
    assert spec["observed_open_state_obligation_ids"] == INVENTORY_IDS
    assert "proof or acceptance evidence for none" in spec["coverage_semantics"]

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["depends_on"] == ["S56-M-0509-VALIDATION"]
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]"
    assert receipt["accepted"] is receipt["release_grade"] is receipt["master_accepted"] is False
    assert receipt["content_addressed_release_evidence"] is False
    assert receipt["decision_id"] == decision["decision_id"]
    assert receipt["decision_sha256"] == sha256(HERE / "release-decision.json")
    assert receipt["release_spec_sha256"] == sha256(HERE / "release-spec.json")
    assert receipt["release_validation_sha256"] == sha256(HERE / "release-validation.md")
    assert receipt["checker_sha256"] == sha256(HERE / "check_release.py")
    assert receipt["verdict"] == "blocked"
    assert receipt["recipe"] == {
        key: spec[key] for key in (
            "recipe_id", "cwd", "argv", "env_allowlist", "timeout_seconds",
            "network_policy", "network_enforcement", "expected_exit", "expected_outputs",
            "covered_obligation_ids", "observed_open_state_obligation_ids",
            "coverage_semantics", "covered_declarations", "declaration_coverage_semantics",
        )
    }
    result = receipt["result"]
    assert result["verdict"] == "blocked"
    assert result["lifecycle_before"] == result["lifecycle_after"] == "planned"
    assert result["root_vector_before"] == result["root_vector_after"] == VECTOR
    assert result["accepted_receipt_ids"] == result["accepted_closed_obligation_ids"] == []
    assert result["mathematical_root_cut_set"] == MATHEMATICAL_CUT
    assert result["current_lean_replay"] == "pass_nonrelease_warm_cache"
    assert result["current_lean_output_sha256"] == EXPECTED_OUTPUT_SHA256
    assert result["current_trust_closure_observation"] == observation["closure"]
    assert result["audit_complete"] is result["theorem_complete"] is False
    assert result["audit_z"] == result["theorem_z"] == "blocked"
    assert result["release_accepted"] is False
    assert receipt["accepted_receipt_ids"] == []
    assert receipt["known_failures"] == decision["known_failures"]
    assert receipt["changed_paths"] == sorted(CHANGED_PATHS)
    assert receipt["output_summary"] == SUMMARY_LINES
    assert receipt["environment"]["platform"] == (
        f"{platform.system()} {platform.release()} {platform.machine()}"
    )

    assert set(packet) == {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert packet["item_id"] == ITEM and packet["state"] == "[_]"
    assert packet["base_revision"] == BASE_REVISION
    assert packet["changed_paths"] == sorted(CHANGED_PATHS)
    assert packet["known_failures"] == decision["known_failures"]
    assert packet["commands"] == receipt["commands_and_results"]
    assert packet["output_summary"] == receipt["output_summary"]
    assert any(
        command.get("argv") == spec["argv"] and command.get("exit_code") == 0
        for command in packet["commands"]
    )
    actual_changed = {
        line[3:] for line in git(
            "status", "--short", "--untracked-files=all", "--",
            str(HERE.relative_to(ROOT)), ".stage1-worker-selftest.json",
        ).splitlines()
    }
    assert actual_changed == CHANGED_PATHS, (actual_changed, CHANGED_PATHS)

    handoff = (HERE / "release-validation.md").read_text(encoding="utf-8")
    for fragment in (
        "`blocked`", "`[H1, M4, R4]`", "`AUDIT-Z`", "`THEOREM-Z`",
        "This worker accepts no receipt", "release_grade=false",
    ):
        assert fragment in handoff, fragment
    assert str(ROOT) not in handoff
    for relative in CHANGED_PATHS:
        assert_text_hygiene(ROOT / relative)

    print("\n".join(SUMMARY_LINES))


if __name__ == "__main__":
    main()
