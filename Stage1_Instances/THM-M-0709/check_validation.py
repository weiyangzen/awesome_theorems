#!/usr/bin/env python3
"""Fail-closed narrow validator for S56-M-0709-VALIDATION."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import platform
import re
import shutil
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0709"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
ITEM = "S56-M-0709-VALIDATION"
THEOREM = "THM-M-0709"
BASE_REVISION = "443b8bbc23bf35a1e7a4bb7b3183073f76bbee2b"
BASE_TREE = "c5771c47c12b80aba613e6d844570f83b39ded6d"
TOOLCHAIN = "leanprover/lean4:v4.29.0"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
LEAN_EXECUTABLE_SHA256 = "3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf"
LAKE_EXECUTABLE_SHA256 = "a608ff084d7e2af228b92a29d7c2fd083ba0580e46889175ec74a81678c98359"
ELAN_LAUNCHER_SHA256 = "840179e70803ef373c2ec53342d6a45ea7d022533e4145489fc1278b4f716385"
PYTHON_EXECUTABLE_SHA256 = "b8d8288faefdd300201f43fcf00f6f539a27218eeed3a3dff5ab10b9c4c99700"
GIT_EXECUTABLE_SHA256 = "8a48eefa306b9a2a9c3e576784a74ad7485779279e5a46ec43361a1864760e45"
BWRAP_EXECUTABLE_SHA256 = "0abea81db798ebf6b4742ac0664802d97521547a353c2a0dbdc21d76cbbfd2c0"
TOOLCHAIN_SHA256 = "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2"
MANIFEST_SHA256 = "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MATHLIB_REMOTE = "https://github.com/leanprover-community/mathlib4.git"
MATHLIB_LICENSE_SHA256 = "b40930bbcf80744c86c46a12bc9da056641d722716c378f5659b9e555ef833e1"
EXPRESSION_SHA256 = "5d375802e054a1c87b9fe6c8c24b728e9bcf8bfa20025ebe987d461545926d03"
DENOMINATOR_SHA256 = "f3731049c66ed6cf5e4687115b723249d54dae577f83859e130b76911f519b38"
ROOT_VECTOR = {"H": "H1", "M": "M3", "R": "R3"}
ACCEPTED_ROOT_VECTOR = {"H": "H1", "M": "M4", "R": "R3"}
OPEN_ROOT_CUT = [
    "M0709-C-MACHINE",
    "M0709-C-MPCP",
    "M0709-T-MPCP-PCP",
    "M0709-N-BINARY",
    "M0709-T-REDUCTION",
]
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
EXPECTED_INPUTS = {
    "Statement.lean": "354a0a291b2c304451ad1e22157ba233ce18730c792a09d9d339b7df3ab29121",
    "ObligationTree.lean": "0b6806c0a66432d88c3c0ca0ed918304e4bdee8033bd3efa242b71ba5d7ddce2",
    "Proof.lean": "0dc9bc3950f59ba31380934472b8a464124dfca8c89aeb56376b0bd1a9335744",
    "Validation.lean": "f36a8265fab01a346a8645f6f8b8ce9562a1665760f0faa5a5f49bc5d0b7f668",
    "statement.json": "0552d73a85d26e55d9db6d2493bb34954f56b6c51475928f5aa13db3fe0dfe7d",
    "anchor-audit.json": "ea7cbf9af3afb94ef90f55b75ce4307ebbcc64288d9c5d7e5b8ca762db4f2b05",
    "obligation-registry.json": "c1416c5954697319b053d0e5b416ce3caad3cb3650b537a4bfe7005e143d56db",
    "typed-graphs.json": "178ef0452526de4e9f078a3b3a6aa88e5e7b88b36f33ad74a58b97d08eebea93",
    "validation-specs.json": "e6d3e4117447e56ec84fc5fd9ae6de343fc32aca647649b85f9e6430d092bad8",
    "proof-receipt.json": "bca9c6b2399530404223006ff727f5f729bec3e39ca0ecc447e1a54d921a9b35",
    "proof-blocker.json": "8121066819e46b9f5659df2e6117de1e828c6710d4ed7024f8131a489a65e6f1",
    "instance.json": "7e132cf93df7f73f6b3ae2ad3e72bda8e7365a2b94b9cf8b0a20629ca6daf300",
}
PROVENANCE = {
    "Mathlib/Computability/Halting.lean": {
        "git_blob": "0834371356762db805d37208b9cf8a1fc0efd217",
        "source_sha256": "c2a073a05c631e7fc957577a66025e9ac36dac741f9aa865e0f053b17f0c85de",
        "olean_sha256": "a4d0f485725fd93028f52418d4c5b6251cbd59cececed2b4ff1f4ac5578a61ba",
        "olean_bytes": 107608,
    },
    "Mathlib/Computability/Reduce.lean": {
        "git_blob": "aa5487c021cfdb4c7644efdd30ec5eb9dc0775bb",
        "source_sha256": "30513e477c461fdce1518542f4dc16085f1d98ab47ba2bfbc28d5b741b18e556",
        "olean_sha256": "ed05cc633a618b11db47fafc0daa6333c804d18e5114d7013c0cda9259c33dfe",
        "olean_bytes": 197560,
    },
}
CHANGED_PATHS = [
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/Validation.lean",
    f"Stage1_Instances/{THEOREM}/check_validation.py",
    f"Stage1_Instances/{THEOREM}/validation-phase.md",
    f"Stage1_Instances/{THEOREM}/validation-receipt.json",
    f"Stage1_Instances/{THEOREM}/validation-spec.json",
]
SUMMARY_LINES = [
    "PASS narrow kernel replay: statement, root interface, partial proof, and differential probes elaborated at trust zero",
    "PASS trust observation: checked terminal and local declarations are sorry-free and report only propext, Classical.choice, and Quot.sound",
    "PASS selected provenance: frozen hashes, clean pinned mathlib, two source/blob/olean identities, license, and tool digests agree",
    "OPEN exact root: the reduction remains unimplemented; accepted instance stays M4, frozen graph/proof evidence is M3, and no obligation is accepted",
    "FAIL CLOSED complete trust/provenance: accepted foundation policy, serialized transitive closure, and full TCB/SBOM inventory are absent",
    "FAIL CLOSED release gates: the shared cache is contaminated and warm, and this worker is not a distinct independent verifier",
]


if not __debug__:
    raise RuntimeError("validation requires Python assertions; optimized mode is forbidden")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path: Path) -> dict:
    def reject_duplicates(pairs: list[tuple[str, object]]) -> dict:
        value: dict[str, object] = {}
        for key, item in pairs:
            assert key not in value, f"duplicate JSON key in {path}: {key}"
            value[key] = item
        return value

    value = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicates)
    assert isinstance(value, dict), path
    return value


def run(
    argv: list[str], *, cwd: Path = ROOT, env: dict[str, str] | None = None,
    timeout: int = 600,
) -> str:
    result = subprocess.run(
        argv, cwd=cwd, env=env, text=True, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, timeout=timeout, check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"command failed ({result.returncode}): {argv!r}\n{result.stdout}"
        )
    return result.stdout


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["git", *args], cwd=cwd).strip()


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


def printed_axioms(output: str, declaration: str) -> set[str]:
    match = re.search(
        re.escape(f"'{declaration}' depends on axioms: [") + r"(.*?)]",
        output,
        flags=re.DOTALL,
    )
    assert match is not None, f"missing axiom report for {declaration}"
    return {part.strip() for part in match.group(1).split(",") if part.strip()}


def assert_text_hygiene(path: Path) -> None:
    data = path.read_bytes()
    assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())


def sandboxed_replay(lean: Path, lean_path: str, bwrap: Path) -> dict[str, str]:
    with tempfile.TemporaryDirectory(prefix="m0709-validation-", dir="/tmp") as tmp_name:
        tmp = Path(tmp_name).resolve()
        for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
            (tmp / name).write_bytes((HERE / name).read_bytes())

        base = [
            str(bwrap), "--ro-bind", "/", "/", "--bind", str(tmp), str(tmp),
            "--dev", "/dev", "--proc", "/proc", "--unshare-net",
            "--die-with-parent", "--clearenv", "--setenv", "HOME", str(tmp),
            "--setenv", "TMPDIR", str(tmp), "--setenv", "LANG", "C.UTF-8",
            "--setenv", "LC_ALL", "C.UTF-8", "--setenv", "TZ", "UTC",
            "--setenv", "LEAN_NUM_THREADS", "1", "--chdir", str(tmp),
        ]

        def lean_run(name: str, module_path: str, emit_olean: bool) -> str:
            argv = base + ["--setenv", "LEAN_PATH", module_path, str(lean), "--trust=0"]
            if emit_olean:
                argv += ["-o", name.replace(".lean", ".olean")]
            argv.append(name)
            return run(argv, timeout=600)

        return {
            "statement": lean_run("Statement.lean", lean_path, True),
            "obligation_tree": lean_run("ObligationTree.lean", f"{tmp}:{lean_path}", True),
            "proof": lean_run("Proof.lean", f"{tmp}:{lean_path}", False),
            "validation": lean_run("Validation.lean", f"{tmp}:{lean_path}", False),
        }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--probe", action="store_true")
    parser.add_argument("--worker-packet", type=Path)
    args = parser.parse_args()

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    targets = load(ROOT / "Docs" / "Stage1_Targets_rev-5.6.json")
    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target == {
        "execution_rank": 750,
        "legacy_priority_slot": None,
        "theorem_id": THEOREM,
        "name": "Post对应问题",
        "category": "数理逻辑 / 证明论",
        "source_status_untrusted": "已验证",
        "baseline": "L0",
        "rework_required": True,
        "legacy_artifacts_accepted": False,
        "target_lane": "hard_statement_first_partial_verification",
        "intake_score": 124,
        "lifecycle_mode": "planned",
        "theorem_complete": False,
    }
    execution = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item == {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 750,
        "phase": "validation",
        "layer": 5,
        "state": "[ ]",
        "depends_on": ["S56-M-0709-PROOF"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Run hermetic kernel, trust, provenance, and independent validation gates.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }
    predecessor = next(row for row in execution["items"] if row["id"] == "S56-M-0709-PROOF")
    assert predecessor["state"] == "[_]" and predecessor["attempts"] == 1

    statement = load(HERE / "statement.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    proof_receipt = load(HERE / "proof-receipt.json")
    proof_blocker = load(HERE / "proof-blocker.json")
    instance = load(HERE / "instance.json")
    for name, expected in EXPECTED_INPUTS.items():
        assert sha256(HERE / name) == expected, f"stale validation input: {name}"
    assert statement["canonical_formal_target"]["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert statement["canonical_formal_target"]["statement_file_sha256"] == EXPECTED_INPUTS["Statement.lean"]
    assert registry["frozen_against_statement_sha256"] == EXPECTED_INPUTS["Statement.lean"]
    assert registry["frozen_against_anchor_audit_sha256"] == EXPECTED_INPUTS["anchor-audit.json"]
    assert registry["denominator_sha256"] == graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert graphs["root_node_id"] == registry["root_obligation_id"] == "M0709-ROOT"
    closure = graphs["closure_boundary"]
    assert closure["root_closed"] is closure["theorem_complete"] is False
    assert closure["root_machine_classification"] == "M3"
    root = next(node for node in graphs["nodes"] if node["obligation_id"] == "M0709-ROOT")
    assert {"H": root["human_debt"], "M": root["machine_debt"], "R": root["readability_debt"]} == ROOT_VECTOR
    assert instance["lifecycle"] == "planned"
    assert instance["root_vector"] == ACCEPTED_ROOT_VECTOR
    assert instance["audit_complete"] is instance["theorem_complete"] is False
    assert proof_receipt["item_id"] == "S56-M-0709-PROOF"
    assert proof_receipt["proof_body"]["source_sha256"] == EXPECTED_INPUTS["Proof.lean"]
    assert proof_receipt["result"]["root_kernel_closed"] is False
    assert proof_receipt["result"]["theorem_complete"] is False
    assert proof_receipt["remaining_root_cut_set"] == OPEN_ROOT_CUT
    assert proof_blocker["root_closed"] is proof_blocker["theorem_complete"] is False
    assert proof_blocker["remaining_root_cut_set"] == OPEN_ROOT_CUT

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by)\b|"
        r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
        r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
        r"(?:axiom|constant|opaque|unsafe|extern)\b",
        flags=re.MULTILINE,
    )
    for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
        source = source_without_comments((HERE / name).read_text(encoding="utf-8"))
        assert prohibited.search(source) is None, f"prohibited proof construct in {name}"
    validation_source = source_without_comments((HERE / "Validation.lean").read_text(encoding="utf-8"))
    assert not re.search(r"^[ \t]*import[ \t]+(?:Proof|ObligationTree)\b", validation_source, re.MULTILINE)
    for fragment in (
        "theorem manyOnePullback_validation",
        "ComputablePred.computable_of_manyOneReducible hred htarget",
        "theorem haltingLeaf_validation",
        "ComputablePred.halting_problem input",
        "theorem conditionalRoot_validation",
        "hred : ValidationHaltingPredicate input ≤₀ HasSolution",
        "assert_no_sorry conditionalRoot_validation",
        "#print axioms conditionalRoot_validation",
    ):
        assert fragment in validation_source, fragment

    assert sha256(LEAN_ROOT / "lean-toolchain") == TOOLCHAIN_SHA256
    assert sha256(LEAN_ROOT / "lake-manifest.json") == MANIFEST_SHA256
    manifest = load(LEAN_ROOT / "lake-manifest.json")
    mathlib_entry = next(row for row in manifest["packages"] if row["name"] == "mathlib")
    flt_entry = next(row for row in manifest["packages"] if row["name"] == "«flt-regular»")
    assert mathlib_entry["rev"] == mathlib_entry["inputRev"] == MATHLIB_REVISION
    assert flt_entry["rev"] == flt_entry["inputRev"] == "56161b6eb5281fbfe9c38f2bcec0f429ebc11a27"
    assert (LEAN_ROOT / ".lake").is_symlink(), "canonical worker .lake symlink is missing"
    mathlib = (LEAN_ROOT / ".lake/packages/mathlib").resolve()
    assert mathlib.is_dir(), "pinned mathlib artifact is missing"
    assert git("rev-parse", "HEAD", cwd=mathlib) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == MATHLIB_TREE
    assert git("status", "--porcelain=v1", cwd=mathlib) == ""
    assert git("remote", "get-url", "origin", cwd=mathlib) == MATHLIB_REMOTE
    for relative, expected in PROVENANCE.items():
        relative_path = Path(relative)
        source = mathlib / relative_path
        olean = mathlib / ".lake/build/lib/lean" / relative_path.with_suffix(".olean")
        assert git("rev-parse", f"HEAD:{relative}", cwd=mathlib) == expected["git_blob"]
        assert sha256(source) == expected["source_sha256"]
        assert sha256(olean) == expected["olean_sha256"]
        assert olean.stat().st_size == expected["olean_bytes"]
    assert sha256(mathlib / "LICENSE") == MATHLIB_LICENSE_SHA256

    # The unrelated flt-regular package is deliberately not repaired or used.
    # Its shared Git metadata is concurrently mutable, so only exclusion from
    # the positive replay is asserted; global cache stability fails closed.
    fixed_env = {
        "ELAN_TOOLCHAIN": TOOLCHAIN,
        "LANG": "C.UTF-8",
        "LC_ALL": "C.UTF-8",
        "TZ": "UTC",
        "LEAN_NUM_THREADS": "1",
    }
    elan_name = shutil.which("elan")
    assert elan_name is not None
    elan = Path(elan_name).resolve()
    lean = Path(run([str(elan), "which", "lean"], cwd=LEAN_ROOT, env=fixed_env).strip())
    lake = Path(run([str(elan), "which", "lake"], cwd=LEAN_ROOT, env=fixed_env).strip())
    python = Path(shutil.which("python3") or "").resolve()
    git_executable = Path(shutil.which("git") or "").resolve()
    bwrap = Path(shutil.which("bwrap") or "").resolve()
    assert sha256(lean) == LEAN_EXECUTABLE_SHA256
    assert sha256(lake) == LAKE_EXECUTABLE_SHA256
    assert sha256(elan) == ELAN_LAUNCHER_SHA256
    assert sha256(python) == PYTHON_EXECUTABLE_SHA256
    assert sha256(git_executable) == GIT_EXECUTABLE_SHA256
    assert sha256(bwrap) == BWRAP_EXECUTABLE_SHA256
    assert LEAN_COMMIT in run([str(lean), "--version"], env=fixed_env)
    assert "5.0.0-src+98dc76e" in run([str(lake), "--version"], env=fixed_env)

    package_names = (
        "Cli", "batteries", "Qq", "aesop", "proofwidgets", "importGraph",
        "LeanSearchClient", "plausible", "checkdecls", "mathlib",
    )
    compiled_roots = []
    for name in package_names:
        path = (LEAN_ROOT / ".lake/packages" / name).resolve() / ".lake/build/lib/lean"
        if path.is_dir():
            compiled_roots.append(path)
    assert mathlib / ".lake/build/lib/lean" in compiled_roots
    assert all("flt-regular" not in str(path) for path in compiled_roots)
    lean_path = ":".join([
        *(str(path) for path in compiled_roots),
        str((LEAN_ROOT / ".lake/build/lib/lean").resolve()),
        str((lean.parent.parent / "lib/lean").resolve()),
    ])
    outputs = sandboxed_replay(lean, lean_path, bwrap)
    proof_declarations = (
        "Stage1Instances.THM_M_0709.not_computablePred_of_manyOneReducible",
        "Stage1Instances.THM_M_0709.haltingPredicate_not_computable",
        "Stage1Instances.THM_M_0709.postCorrespondenceUndecidable_of_haltingReduction",
        "ComputablePred.computable_of_manyOneReducible",
        "ComputablePred.halting_problem",
    )
    validation_declarations = (
        "ComputablePred.computable_of_manyOneReducible",
        "ComputablePred.halting_problem",
        "Stage1Instances.THM_M_0709.Validation.manyOnePullback_validation",
        "Stage1Instances.THM_M_0709.Validation.haltingLeaf_validation",
        "Stage1Instances.THM_M_0709.Validation.conditionalRoot_validation",
    )
    assert printed_axioms(outputs["obligation_tree"], "Stage1Instances.THM_M_0709.root_interface") == EXPECTED_AXIOMS
    for declaration in proof_declarations:
        assert printed_axioms(outputs["proof"], declaration) == EXPECTED_AXIOMS
    for declaration in validation_declarations:
        assert printed_axioms(outputs["validation"], declaration) == EXPECTED_AXIOMS
    proof_sorry_free = outputs["proof"].count("Declarations are sorry-free!")
    validation_sorry_free = outputs["validation"].count("Declarations are sorry-free!")
    assert proof_sorry_free == 5
    assert validation_sorry_free >= 1
    closure_match = re.search(r"VALIDATION_CLOSURE declarations=(\d+) modules=(\d+)", outputs["validation"])
    assert closure_match is not None
    assert "VALIDATION_CLOSURE axioms=[propext, Classical.choice, Quot.sound]" in outputs["validation"]
    assert "VALIDATION_CLOSURE bodyless_nonaxioms=[]" in outputs["validation"]
    assert "VALIDATION_CLOSURE unsafe=[]" in outputs["validation"]
    assert "sorryAx" not in "\n".join(outputs.values())
    assert all("error:" not in output for output in outputs.values())

    observation = {
        "output_sha256": {
            name: hashlib.sha256(output.encode()).hexdigest()
            for name, output in outputs.items()
        },
        "observed_axioms": sorted(EXPECTED_AXIOMS),
        "proof_sorry_free_reports": proof_sorry_free,
        "validation_sorry_free_reports": validation_sorry_free,
        "validation_closure": {
            "declarations": int(closure_match.group(1)),
            "modules": int(closure_match.group(2)),
            "bodyless_nonaxioms": [],
            "unsafe_declarations": [],
        },
    }
    if args.probe:
        print(json.dumps(observation, sort_keys=True))
        return

    spec = load(HERE / "validation-spec.json")
    receipt = load(HERE / "validation-receipt.json")
    assert spec["schema_version"] == "stage1-validation-spec/1.0"
    assert spec["item_id"] == receipt["item_id"] == ITEM
    assert spec["theorem_id"] == receipt["theorem_id"] == THEOREM
    assert spec["depends_on"] == receipt["depends_on"] == ["S56-M-0709-PROOF"]
    assert len(spec["recipes"]) == 1
    recipe = spec["recipes"][0]
    assert recipe["recipe_id"] == "S56-M-0709-VALIDATION-network-isolated-v1"
    assert recipe["argv"] == [
        "python3", "-B", f"Stage1_Instances/{THEOREM}/check_validation.py",
        "--worker-packet", ".stage1-worker-selftest.json",
    ]
    assert recipe["cwd"] == "." and recipe["timeout_seconds"] == 600
    assert recipe["network_policy"] == "denied" and recipe["expected_exit"] == 0
    assert "bubblewrap" in recipe["network_enforcement"]
    assert receipt["recipe"] == recipe

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["phase"] == "validation" and receipt["intent"] == "validate"
    assert receipt["verdict"] == "blocked"
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["release_grade"] is receipt["content_addressed_release_evidence"] is False
    assert receipt["lifecycle_before"] == receipt["lifecycle_after"] == "planned"
    assert receipt["accepted_root_vector_before"] == \
        receipt["accepted_root_vector_after"] == ACCEPTED_ROOT_VECTOR
    assert receipt["frozen_graph_root_vector"] == ROOT_VECTOR
    assert receipt["debt_vector_change_proposed"] is False
    timing = receipt["timing"]
    assert timing["validation_action_started_at"] < timing["validation_action_finished_at"]
    assert timing["validation_action_finished_at"] <= receipt["validated_at"]
    assert receipt["accepted_receipt_ids"] == []
    for name, expected in EXPECTED_INPUTS.items():
        assert receipt["inputs"][name] == expected, name
    assert receipt["inputs"]["validation-spec.json"] == sha256(HERE / "validation-spec.json")
    assert receipt["inputs"]["check_validation.py"] == sha256(HERE / "check_validation.py")
    assert receipt["target"]["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert receipt["target"]["registry_denominator_sha256"] == DENOMINATOR_SHA256
    environment = receipt["environment"]
    assert environment["platform"] == f"{platform.system()} {platform.release()} {platform.machine()}"
    assert environment["lean_executable_sha256"] == sha256(lean)
    assert environment["lake_executable_sha256"] == sha256(lake)
    assert environment["elan_launcher_sha256"] == sha256(elan)
    assert environment["python_executable_sha256"] == sha256(python)
    assert environment["git_executable_sha256"] == sha256(git_executable)
    assert environment["bubblewrap_executable_sha256"] == sha256(bwrap)
    assert environment["mathlib_revision"] == MATHLIB_REVISION
    assert environment["mathlib_tree"] == MATHLIB_TREE
    assert receipt["result"]["lean_output_sha256"] == observation["output_sha256"]
    assert receipt["result"]["observed_axioms"] == observation["observed_axioms"]
    assert receipt["result"]["validation_closure"] == observation["validation_closure"]
    assert receipt["result"]["proof_dependency_master_acceptance"] == "fail_closed"
    assert receipt["result"]["accepted_closed_obligation_ids"] == []
    assert receipt["result"]["root_kernel_closed"] is False
    assert receipt["result"]["frozen_graph_root_machine_debt"] == "M3"
    assert receipt["result"]["proof_phase_open_root_cut_set"] == OPEN_ROOT_CUT
    assert receipt["proof_phase_remaining_root_cut_set"] == OPEN_ROOT_CUT
    assert receipt["accepted_state_first_open_cut"] == closure["first_open_cut"]
    assert receipt["result"]["complete_trust_provenance_gate"] == "fail_closed"
    assert receipt["result"]["hermetic_release_gate"] == "fail_closed"
    assert receipt["result"]["independent_distinct_runner_gate"] == "fail_closed"
    assert receipt["result"]["audit_complete"] is receipt["result"]["theorem_complete"] is False
    assert receipt["first_failed_gate"] == "dependency.S56-M-0709-PROOF.master_acceptance"
    assert receipt["first_failed_root_gate"] == "M0709-C-MACHINE.root_kernel_closure"
    assert receipt["first_failed_release_gate"] == "S56-10.6-HERMETIC-COLD-BUILD"
    expected_stdout = ("\n".join(SUMMARY_LINES) + "\n").encode()
    assert receipt["output_evidence"] == {
        "stdout_semantic_sha256": hashlib.sha256(expected_stdout).hexdigest(),
        "expected_line_count": len(SUMMARY_LINES),
        "exit_code": 0,
    }

    if args.worker_packet is not None:
        packet = load(args.worker_packet.resolve())
        assert set(packet) == {
            "item_id", "changed_paths", "commands", "output_summary",
            "base_revision", "known_failures", "state",
        }
        assert packet["item_id"] == ITEM and packet["state"] == "[_]"
        assert packet["base_revision"] == BASE_REVISION
        assert packet["changed_paths"] == receipt["changed_paths"] == CHANGED_PATHS
        assert packet["commands"] == receipt["commands"]
        assert packet["output_summary"] == receipt["output_summary"]
        assert packet["known_failures"] == receipt["known_failures"]
        status = git("status", "--short", "--untracked-files=all")
        actual = {
            line[3:] for line in status.splitlines()
            if line[3:] != "Formalizations/Lean/.lake"
        }
        assert actual == set(CHANGED_PATHS), (actual, set(CHANGED_PATHS))

    for relative in CHANGED_PATHS:
        assert_text_hygiene(ROOT / relative)
    for line in SUMMARY_LINES:
        print(line)


if __name__ == "__main__":
    main()
