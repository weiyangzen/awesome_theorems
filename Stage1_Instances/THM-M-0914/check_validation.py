#!/usr/bin/env python3
"""Fail-closed narrow validator for S56-M-0914-VALIDATION."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import tempfile


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM = "S56-M-0914-VALIDATION"
THEOREM = "THM-M-0914"
BASE_REVISION = "c45f3c7090cb4adf616d45e5414985f956e807b2"
BASE_TREE = "da6f991c07f11e8608ddc090af9356558d64d360"
EXPRESSION_SHA256 = "faef4a7f73219dc5b6178b8788978e21377c593ad84b845b4d49547218e6ae3b"
DENOMINATOR_SHA256 = "5a421bbbcc8afad0a1a35bb461a33c7712f8e2abd081706a36b4ccb4ce59f3ce"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MATHLIB_REMOTE = "https://github.com/leanprover-community/mathlib4.git"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
LEAN_TOOLCHAIN_SHA256 = "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2"
LAKE_MANIFEST_SHA256 = "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81"
LEAN_EXECUTABLE_SHA256 = "3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf"
LAKE_EXECUTABLE_SHA256 = "a608ff084d7e2af228b92a29d7c2fd083ba0580e46889175ec74a81678c98359"
PYTHON_EXECUTABLE_SHA256 = "b8d8288faefdd300201f43fcf00f6f539a27218eeed3a3dff5ab10b9c4c99700"
GIT_EXECUTABLE_SHA256 = "8a48eefa306b9a2a9c3e576784a74ad7485779279e5a46ec43361a1864760e45"
BWRAP_EXECUTABLE_SHA256 = "0abea81db798ebf6b4742ac0664802d97521547a353c2a0dbdc21d76cbbfd2c0"

EXPECTED_TRACKED_INPUTS = {
    "Statement.lean": "953cf5ba54e27cf08cce5a91880fd79d36f4b5aa7b92228bd27474a1399233db",
    "ObligationTree.lean": "b345e54fc0ee31fe58f76b8d15394dba7c090492eed94fad8468b6a79cc47272",
    "Proof.lean": "12f28163c757670e301e45282b6b5d02d50779c85fc5ce70109a7b3a9774bc8a",
    "statement.json": "d7b6f9308f62afef5210ca8c01c17363cc0443ea5cb4a3261cdb9aa3c5ce646a",
    "instance.json": "f073d38465200586aa998fc551211369cd62ecaf83503c09a67bab427af0f217",
    "task-dag.json": "ea3a86f9b7eef9f649cf32c7cedf21d728f347bc9d86a721d33e8e0c6244b7fe",
    "anchor-audit.json": "3bad78f64fb4b2f28d4e1a032bb82c4c4fc4f528ee80781b1f5b227cf1bdca92",
    "obligation-registry.json": "3379290c9bb2aa12cb9f2bd50d16174a5dbfefb1833bef961c394f8459c33d00",
    "typed-graphs.json": "05bacf88ed9a87e4cc5b796d0dae4944d57319ae890d67569e3e7bffccfdd5cc",
    "validation-specs.json": "c08a12cf9afbf8dbcf5de27721b15229dc75bf124ac2bf676025bdf13b204f2b",
    "proof-receipt.json": "15bbda352f967c3c2cfa32da8845be241db1d1bbcf448e225bef5e1deac28b78",
}
VALIDATION_STATIC_INPUTS = {
    "Validation.lean": "0a3b58a8f8e8b0edfa6b9c2bf85886912df366b941a757b16e721732c151824f",
    "check_validation.sh": "60d36f42e7dafde712fe1ee0d4d434908f69e29719062527c8c7d503e516ce2b",
    "validation-spec.json": "36a73bb2fcfbb5dc100845a74d7eb3db14091181d924f5a249a6aa224c283966",
}
PROOF_IDS = [
    "M0914-ROOT", "M0914-T-ROOT-COMPOSE", "M0914-N-FIN-CARD-INEQUALITY",
    "M0914-A-FINTYPE-WRAPPER", "M0914-N-FIN-CARD-IDENTITY",
    "M0914-N-SUCCESSOR-LT", "M0914-L-FINSET-COLLISION",
    "M0914-N-UNIV-MAPS-TO", "M0914-L-CARD-INJON-BOUND",
    "M0914-L-NO-COLLISION-INJON",
]
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/Validation.lean",
    f"Stage1_Instances/{THEOREM}/check_validation.py",
    f"Stage1_Instances/{THEOREM}/check_validation.sh",
    f"Stage1_Instances/{THEOREM}/validation-phase.md",
    f"Stage1_Instances/{THEOREM}/validation-receipt.json",
    f"Stage1_Instances/{THEOREM}/validation-spec.json",
}

PROVENANCE_FILES = {
    "pigeonhole": {
        "source": Path("Mathlib/Data/Fintype/Pigeonhole.lean"),
        "blob": "19ebeb40518e099dc572d5b3b627ce2f62c0745a",
        "source_sha256": "fa4604d2b1ae480f910e6000ca8814a632299082b48a14f598314303b68cc582",
        "olean_sha256": "0d557d94dc54047f6c54aa3c94785d859a4f3738e6bf98d3b42257ee6bb36931",
    },
    "finset_card": {
        "source": Path("Mathlib/Data/Finset/Card.lean"),
        "blob": "d1c2c1e36ea9028aa27c4724c2c9d76afd9af35b",
        "source_sha256": "5566f2afb81cb80e2aa7349d8b04214f3667d84e4b81d965f85714ec5a8f0e27",
        "olean_sha256": "b8504bc80578476685d30420a182799a2e385bde6c35299494034e828767023d",
    },
    "fintype_card": {
        "source": Path("Mathlib/Data/Fintype/Card.lean"),
        "blob": "acca9b0f9856a75b506179095f17725748864732",
        "source_sha256": "fa741a491945b426f4a38cc838433c832b9a1e0f588f2075c63349eb200bb465",
        "olean_sha256": "0497d8bcacbeda685c736bf70f73c49214b190b548e67691e3a53bf571ff8f1f",
    },
    "function_basic": {
        "source": Path("Mathlib/Logic/Function/Basic.lean"),
        "blob": "44534ad0ffc9444b1758a0fdc099b216b0da6ac0",
        "source_sha256": "5dffbb69147f9bf2cfc8de6083b7eab88d0b297762052e5e81d19a77f346dc97",
        "olean_sha256": "0eaa970b546776cc0908bb720718e6b9d499e3e6b5c90836739f174d92352293",
    },
}


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict), path
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(
    argv: list[str], *, cwd: Path = ROOT, env: dict[str, str] | None = None,
    timeout: int = 300,
) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        argv, cwd=cwd, env=env, text=True, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, timeout=timeout, check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(f"command failed ({result.returncode}): {argv!r}\n{result.stdout}")
    return result


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["git", *args], cwd=cwd).stdout.strip()


def without_comments(source: str) -> str:
    source = re.sub(r"/-.*?-/", "", source, flags=re.DOTALL)
    return re.sub(r"--.*$", "", source, flags=re.MULTILINE)


def body_sha256(path: Path, first: int, last: int) -> str:
    lines = path.read_bytes().splitlines(keepends=True)
    return hashlib.sha256(b"".join(lines[first - 1:last])).hexdigest()


def no_index_patch_sha256(path: Path) -> str:
    result = subprocess.run(
        ["git", "diff", "--no-index", "--binary", "/dev/null", str(path)],
        cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False,
    )
    assert result.returncode == 1, path
    return hashlib.sha256(result.stdout).hexdigest()


def check_text(path: Path) -> None:
    data = path.read_bytes()
    assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data, path
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines()), path


def main() -> None:
    spec = load(HERE / "validation-spec.json")
    receipt = load(HERE / "validation-receipt.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")
    statement = load(HERE / "statement.json")
    instance = load(HERE / "instance.json")
    task_dag = load(HERE / "task-dag.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    anchor = load(HERE / "anchor-audit.json")
    proof_receipt = load(HERE / "proof-receipt.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item == {
        "id": ITEM, "theorem_id": THEOREM, "execution_rank": 1456,
        "phase": "validation", "layer": 5, "state": "[ ]",
        "depends_on": ["S56-M-0914-PROOF"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Run hermetic kernel, trust, provenance, and independent validation gates.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0, "children": [],
    }
    predecessor = next(row for row in execution["items"] if row["id"] == "S56-M-0914-PROOF")
    assert predecessor["state"] == "[_]" and predecessor["attempts"] == 1
    local_task = next(row for row in task_dag["tasks"] if row["id"] == ITEM)
    assert local_task["state"] == "open" and task_dag["accepted_states"] == []

    assert spec["schema_version"] == "stage1-validation-recipe/1.0"
    assert spec["item_id"] == receipt["item_id"] == ITEM
    assert spec["theorem_id"] == receipt["theorem_id"] == THEOREM
    assert spec["cwd"] == "." and spec["argv"] == [
        "bash", f"Stage1_Instances/{THEOREM}/check_validation.sh"
    ]
    assert spec["env_allowlist"] == {}
    assert spec["timeout_seconds"] == 300
    assert spec["network_policy"] == "denied" and spec["expected_exit"] == 0
    assert "bubblewrap" in spec["network_enforcement"] and "--unshare-net" in spec["network_enforcement"]
    assert set(PROOF_IDS + ["M0914-X-PROVENANCE", "M0914-X-TRUST"]) == set(spec["covered_obligation_ids"])

    for name, expected in EXPECTED_TRACKED_INPUTS.items():
        assert sha256(HERE / name) == expected, f"stale tracked input: {name}"
    for name, expected in VALIDATION_STATIC_INPUTS.items():
        assert sha256(HERE / name) == expected, f"changed validation input: {name}"
    assert receipt["inputs"] == {
        **EXPECTED_TRACKED_INPUTS, **VALIDATION_STATIC_INPUTS,
        "check_validation.py": sha256(HERE / "check_validation.py"),
    }

    formal = statement["canonical_formal_target"]
    assert formal["declaration_or_expression"] == "Stage1Instances.THM_M_0914.PigeonholeTarget"
    assert formal["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert formal["statement_file_sha256"] == EXPECTED_TRACKED_INPUTS["Statement.lean"]
    assert anchor["canonical_target"] == "Stage1Instances.THM_M_0914.PigeonholeTarget"
    assert anchor["canonical_target_expression_sha256"] == EXPRESSION_SHA256
    assert registry["denominator_sha256"] == graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert registry["root_obligation_id"] == graphs["root_node_id"] == "M0914-ROOT"
    assert proof_receipt["canonical_target_expression_sha256"] == EXPRESSION_SHA256
    assert proof_receipt["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert proof_receipt["provisionally_closed_proof_obligation_ids"] == PROOF_IDS
    assert receipt["statement_fingerprints"] == proof_receipt["statement_fingerprints"]
    assert proof_receipt["proof_body"]["source_sha256"] == EXPECTED_TRACKED_INPUTS["Proof.lean"]
    assert proof_receipt["result"]["root_kernel_closed"] is True
    assert set(proof_receipt["result"]["axioms"]) == EXPECTED_AXIOMS
    assert proof_receipt["accepted"] is False
    assert instance["root_vector"] == {"H": "H1", "M": "M3", "R": "R4"}
    assert instance["audit_complete"] is instance["theorem_complete"] is False
    closure = graphs["closure_boundary"]
    assert closure["accepted_closed_obligations"] == []
    assert closure["root_closed"] is False and closure["root_machine_debt"] == "M3"

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|implemented_by|native_decide|extern|opaque)\b|"
        r"^[ \t]*(?:axiom|constant|unsafe)[ \t]+", re.MULTILINE,
    )
    for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
        assert prohibited.search(without_comments((HERE / name).read_text(encoding="utf-8"))) is None, name
    validation = (HERE / "Validation.lean").read_text(encoding="utf-8")
    assert "import Proof" not in validation and "import ObligationTree" not in validation
    assert "Fintype.not_injective_of_card_lt f hCard" in validation
    assert "Function.not_injective_iff.mp hNotInjective" in validation
    assert "theorem pigeonholeTarget_differential : PigeonholeTarget := by" in validation

    recipe_run = run(spec["argv"], cwd=ROOT, timeout=spec["timeout_seconds"])
    expected_recipe_output = (
        "PASS THM-M-0914 network-isolated validation: exact proof and differential "
        "roots replayed; 15 declarations sorry-free; axioms within "
        "propext, Classical.choice, Quot.sound; closure has no unsafe or bodyless nonaxioms\n"
    )
    assert recipe_run.stdout == expected_recipe_output
    assert receipt["result"]["recipe_stdout_sha256"] == hashlib.sha256(
        recipe_run.stdout.encode()
    ).hexdigest()
    assert receipt["result"]["recipe_stdout_bytes"] == len(recipe_run.stdout.encode())

    assert sha256(LEAN_ROOT / "lean-toolchain") == LEAN_TOOLCHAIN_SHA256
    assert sha256(LEAN_ROOT / "lake-manifest.json") == LAKE_MANIFEST_SHA256
    manifest = load(LEAN_ROOT / "lake-manifest.json")
    mathlib_entry = next(row for row in manifest["packages"] if row["name"] == "mathlib")
    assert mathlib_entry["rev"] == mathlib_entry["inputRev"] == MATHLIB_REVISION
    assert MATHLIB.resolve().is_dir(), "canonical pinned mathlib artifacts are missing"
    assert git("rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert git("remote", "get-url", "origin", cwd=MATHLIB) == MATHLIB_REMOTE
    assert git("status", "--porcelain=v1", cwd=MATHLIB) == ""
    for record in PROVENANCE_FILES.values():
        source = MATHLIB / record["source"]
        olean = MATHLIB / ".lake/build/lib/lean" / record["source"].with_suffix(".olean")
        assert git("rev-parse", f"HEAD:{record['source']}", cwd=MATHLIB) == record["blob"]
        assert sha256(source) == record["source_sha256"]
        assert sha256(olean) == record["olean_sha256"]
    assert body_sha256(MATHLIB / PROVENANCE_FILES["pigeonhole"]["source"], 46, 49) == "d84d5bc0b4c083cfdfb02001f2def9855531a4c250dbc855132fd9064669eb2f"
    assert body_sha256(MATHLIB / PROVENANCE_FILES["finset_card"]["source"], 413, 418) == "11c401a65812e6d18a01c623ba3ce05b5ac7a4e707a007cfee8a013613e84b1e"
    assert body_sha256(MATHLIB / PROVENANCE_FILES["finset_card"]["source"], 442, 449) == "c88e185f9515ef671655ee204e5526c49887f3a23a56b99a0d849074cdcb9707"
    assert body_sha256(MATHLIB / PROVENANCE_FILES["fintype_card"]["source"], 238, 245) == "b90a277e10566a82ef4e6d96e7fff4494a84e67b6f8cc2ccf638758871661ff7"
    assert body_sha256(MATHLIB / PROVENANCE_FILES["function_basic"]["source"], 81, 83) == "df6e5cff5375141b0c5ff21012718bdeda1bfe2a6e3876b9afd67ec90b0b7bf7"
    assert sha256(MATHLIB / "LICENSE") == "b40930bbcf80744c86c46a12bc9da056641d722716c378f5659b9e555ef833e1"

    assert shutil.which("bwrap") is not None
    lean = Path(run(["lake", "env", "which", "lean"], cwd=LEAN_ROOT).stdout.strip())
    assert sha256(lean) == LEAN_EXECUTABLE_SHA256
    version = run(["lake", "env", "lean", "--version"], cwd=LEAN_ROOT).stdout
    assert "4.29.0" in version and LEAN_COMMIT in version
    lean_path = run(["lake", "env", "printenv", "LEAN_PATH"], cwd=LEAN_ROOT).stdout.strip()
    with tempfile.TemporaryDirectory(prefix="stage1-m0914-python-validation-") as directory:
        temporary = Path(directory)
        for name in ("Statement.lean", "Validation.lean"):
            (temporary / name).write_bytes((HERE / name).read_bytes())
        base = [
            "bwrap", "--ro-bind", "/", "/", "--bind", str(temporary), str(temporary),
            "--dev", "/dev", "--proc", "/proc", "--unshare-net", "--die-with-parent",
            "--setenv", "LANG", "C", "--setenv", "LC_ALL", "C",
            "--setenv", "NO_COLOR", "1", "--setenv", "TZ", "UTC",
            "--chdir", str(temporary),
        ]
        run(base + ["--setenv", "LEAN_PATH", lean_path, str(lean), "--trust=0", "-o", "Statement.olean", "Statement.lean"], timeout=300)
        differential = run(base + ["--setenv", "LEAN_PATH", f"{temporary}:{lean_path}", str(lean), "--trust=0", "Validation.lean"], timeout=300).stdout
    assert differential.count("Declarations are sorry-free!") == 3
    assert "VALIDATION_CLOSURE bodyless_nonaxioms=[]" in differential
    assert "VALIDATION_CLOSURE unsafe=[]" in differential
    assert "sorryAx" not in differential and "error:" not in differential

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["depends_on"] == ["S56-M-0914-PROOF"] and receipt["intent"] == "validate"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["verdict"] == "blocked" and receipt["release_grade"] is False
    assert set(receipt["changed_paths"]) == CHANGED_PATHS
    assert receipt["canonical_target_expression_sha256"] == EXPRESSION_SHA256
    assert receipt["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert receipt["result"]["root_kernel_replayed"] is True
    assert receipt["result"]["differential_exact_root_replayed"] is True
    assert receipt["result"]["accepted_root_closed"] is False
    assert receipt["result"]["hermetic_release_gate"] == "fail_closed"
    assert receipt["result"]["independent_verification_gate"] == "fail_closed"
    assert receipt["result"]["audit_complete"] is receipt["result"]["theorem_complete"] is False
    assert receipt["first_failed_gate"] == "dependency.S56-M-0914-PROOF.master_acceptance"
    assert receipt["first_failed_release_gate"] == "hermetic.cold_empty_cache_offline_replay"
    repository_state = receipt["repository_state"]
    assert repository_state["dirty"] is True
    assert repository_state["tracked_patch_sha256"] is None
    assert repository_state["tracked_patch_bytes"] == 0
    assert repository_state["untracked_input_hashes"] == {
        f"Stage1_Instances/{THEOREM}/{name}": expected
        for name, expected in VALIDATION_STATIC_INPUTS.items()
    }
    assert repository_state["untracked_no_index_patch_hashes"] == {
        f"Stage1_Instances/{THEOREM}/{name}": no_index_patch_sha256(HERE / name)
        for name in VALIDATION_STATIC_INPUTS
    }
    recorded_recipe = dict(receipt["recipe"])
    assert recorded_recipe.pop("observed_exit") == 0
    assert recorded_recipe == {
        key: spec[key] for key in (
            "recipe_id", "cwd", "argv", "env_allowlist", "timeout_seconds",
            "network_policy", "network_enforcement", "expected_exit",
            "expected_outputs", "covered_obligation_ids", "covered_declarations",
            "scope_boundary",
        )
    }
    assert set(spec["covered_declarations"]) <= set(receipt["validated_declarations"])
    environment = receipt["environment"]
    assert environment["lean_executable_sha256"] == LEAN_EXECUTABLE_SHA256
    assert environment["lake_executable_sha256"] == LAKE_EXECUTABLE_SHA256
    assert environment["python_executable_sha256"] == PYTHON_EXECUTABLE_SHA256
    assert environment["git_executable_sha256"] == GIT_EXECUTABLE_SHA256
    assert environment["bubblewrap_executable_sha256"] == BWRAP_EXECUTABLE_SHA256
    assert sha256(Path(run(["lake", "env", "which", "lake"], cwd=LEAN_ROOT).stdout.strip())) == LAKE_EXECUTABLE_SHA256
    assert sha256(Path(shutil.which("python3") or "")) == PYTHON_EXECUTABLE_SHA256
    assert sha256(Path(shutil.which("git") or "")) == GIT_EXECUTABLE_SHA256
    assert sha256(Path(shutil.which("bwrap") or "")) == BWRAP_EXECUTABLE_SHA256
    provenance = receipt["provenance"]
    assert provenance["origin_remote"] == MATHLIB_REMOTE
    assert provenance["dependency_revision"] == MATHLIB_REVISION
    assert provenance["dependency_tree"] == MATHLIB_TREE
    assert provenance["dependency_worktree_clean"] is True
    assert provenance["license_sha256"] == sha256(MATHLIB / "LICENSE")

    assert set(packet) == {"item_id", "changed_paths", "commands", "output_summary", "base_revision", "known_failures", "state"}
    assert packet["item_id"] == ITEM and packet["state"] == "[_]"
    assert packet["base_revision"] == BASE_REVISION
    assert set(packet["changed_paths"]) == CHANGED_PATHS
    assert packet["known_failures"] == receipt["known_failures"]
    assert packet["commands"] == receipt["commands_and_results"]
    assert packet["output_summary"] == receipt["output_summary"]
    assert packet["commands"] and all(isinstance(row["argv"], list) and row["exit_code"] == 0 and row["result"] for row in packet["commands"])
    assert "theorem_complete=false" in packet["output_summary"]

    status = git("status", "--porcelain=v1", "--untracked-files=all", "--", HERE.relative_to(ROOT), ".stage1-worker-selftest.json")
    actual = {line[3:] for line in status.splitlines() if line}
    assert actual == CHANGED_PATHS, (actual, CHANGED_PATHS)
    phase = (HERE / "validation-phase.md").read_text(encoding="utf-8")
    assert "same-worker differential" in phase
    assert "not section 10.6 release-grade hermetic evidence" in phase
    assert "not section 10.7 independent verification" in phase
    for path in [ROOT / name for name in CHANGED_PATHS]:
        check_text(path)

    print("PASS THM-M-0914 validation phase: exact network-isolated differential replay, pins, provenance, trust observations, receipt, and fail-closed boundaries agree")


if __name__ == "__main__":
    main()
