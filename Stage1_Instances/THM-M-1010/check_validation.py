#!/usr/bin/env python3
"""Fail-closed narrow validator for S56-M-1010-VALIDATION."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-1010"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
ITEM = "S56-M-1010-VALIDATION"
THEOREM = "THM-M-1010"
BASE_REVISION = "fd995645725ec3633e4da7e6d759deb14f530861"
BASE_TREE = "5846121ab94ff0502b98217f643539881bc9c045"
TOOLCHAIN = "leanprover/lean4:v4.29.0"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
LEAN_SHA256 = "3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf"
LAKE_SHA256 = "a608ff084d7e2af228b92a29d7c2fd083ba0580e46889175ec74a81678c98359"
BWRAP_SHA256 = "0abea81db798ebf6b4742ac0664802d97521547a353c2a0dbdc21d76cbbfd2c0"
PYTHON_SHA256 = "b8d8288faefdd300201f43fcf00f6f539a27218eeed3a3dff5ab10b9c4c99700"
GIT_SHA256 = "5516c9f362c29376ab9a499a33082f9f611941d8c75930c880e30ad109e39c9a"
TOOLCHAIN_SHA256 = "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2"
MANIFEST_SHA256 = "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MATHLIB_REMOTE = "https://github.com/leanprover-community/mathlib4.git"
MATHLIB_LICENSE_SHA256 = "b40930bbcf80744c86c46a12bc9da056641d722716c378f5659b9e555ef833e1"
EXPRESSION_SHA256 = "f5f12340fa49d0be0eed038c99c47c921017284447b4a73f4b096e085e800d18"
DENOMINATOR_SHA256 = "8cf08f666cc9a074319f3cd4a905f2f94deedbe62f344fb3554399f3f5d16016"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
ROOT_VECTOR = {"H": "H1", "M": "M3", "R": "R3"}
OPEN_ROOT_CUT = [
    "M1010-N-PARTITIONS",
    "M1010-C-INTERVAL",
    "M1010-L-MEASURABLE",
    "M1010-L-LAWS",
    "M1010-L-AE-STABILIZE",
]
EXPECTED_INPUTS = {
    "Statement.lean": "79eada2911ea773a8fffd02d59d67f49c1e43cb091c7510d563afeed57994f94",
    "ObligationTree.lean": "a52bc1afbf854c891abacb7da1acc8f074351b3f8f88e1676a7e0b54b6f5d6d6",
    "Proof.lean": "e652a54085931d125e1fa5ea7c73329fc46728c5e673a29e264af65914f79ca5",
    "statement.json": "6c9cc2af8cc6c80be42d5a4d3acc7c4995f1664f428be6daf4dcd317424b5cc8",
    "anchor_audit.json": "fa466dc83c1678d016a346dc095b22cfaab3921a65ea33dbaa386cab3ffc0cea",
    "obligation-registry.json": "4b40bc6a126f1e76f43a83c5c77610fd1d0bf7c6ab4d83ed5a4cf61eb5dae7e4",
    "typed-graphs.json": "142369c75e6b0eae8d7ad7248210866727b6c9b33d800cb86e3b8776cd9b6afd",
    "validation-specs.json": "6b1e55b6499c41e3fd5ad4af593d90be58dd56d94680ebcc87fc7c2218ce17b0",
    "proof-receipt.json": "3f4ccf395ddf5a73b5e4787dcdd41cf1cd1a388eb9893e08e02bd3fb286f63b1",
    "check_proof.sh": "0792f4c273a910ef5fe562bd00f62cfd016745f662bc882d86ebbf4769c0ba80",
    "check_proof.py": "8d47e0c9bd2a7b625f5785546d220cc626613785a13f5169d0be56e9a0bb50c4",
    "proof-validation.md": "8d202034070dd0c8785687467d662adf523b2c6018bb0bea68db07a4081fb150",
}
SOURCE_BOUNDARIES = {
    "Mathlib/Probability/HasLaw.lean": {
        "blob": "fe1155e2c2d5f4876171e888c06b48bd9110a449",
        "source_sha256": "8c8185583405be950464928a4690181da39d7b10462315bbc9d9c44ad0044d41",
        "olean_sha256": "77e6a772ca63cf0c6b117513e73d2e4ddb9b8ede12272ead42d3c941d343449d",
        "olean_bytes": 94168,
    },
    "Mathlib/Probability/HasLawExists.lean": {
        "blob": "a0bb5807d52562981ecfdb0cd36abc92a02ea29b",
        "source_sha256": "de026870cd46baaebc3562fa0bc8df9dcc364323b8f5aaa1842f55df3f4d312b",
        "olean_sha256": "6532760ef828805bc51b6d9dda0f209567c977405869849b706c41db90ca36e9",
        "olean_bytes": 12896,
    },
    "Mathlib/MeasureTheory/Measure/LevyProkhorovMetric.lean": {
        "blob": "9fb875215400ee5d7b52b616257e1d27df3a14ee",
        "source_sha256": "8ef2c7a731801d3f411c08ae76f28e0cda22d80e98db1031bddc9f447e46de47",
        "olean_sha256": "9c7c18f54988078254dfcc8f88218a1f709a24e9dc3931c1e49283955a5e399c",
        "olean_bytes": 188176,
    },
}
PROOF_DECLARATIONS = (
    "Stage1Instances.THM_M_1010.exists_common_space_exact_marginals",
    "Stage1Instances.THM_M_1010.representation_of_constant_laws",
    "Stage1Instances.THM_M_1010.target_for_constant_sequence",
)
COMPOSITION_DECLARATION = (
    "Stage1Instances.THM_M_1010.ObligationTree.target_of_couplingPackage"
)
CHANGED_PATHS = [
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/Validation.lean",
    f"Stage1_Instances/{THEOREM}/check_validation.py",
    f"Stage1_Instances/{THEOREM}/validation-blocker.json",
    f"Stage1_Instances/{THEOREM}/validation-phase.md",
    f"Stage1_Instances/{THEOREM}/validation-receipt.json",
    f"Stage1_Instances/{THEOREM}/validation-spec.json",
]
SUMMARY_LINES = [
    "PASS network-isolated trust-zero replay: exact statement, conditional composer, three partial proof declarations, and validation audit elaborated",
    "PASS trust observation: four audited declarations are sorry-free and use only propext, Classical.choice, and Quot.sound",
    "PASS selected provenance: frozen hashes, tool identities, clean mathlib pin, license, and three source/olean boundaries agree",
    "OPEN exact Skorokhod root: proof phase closes zero frozen obligations and the five-node root cut remains",
    "FAIL CLOSED complete trust/provenance: accepted foundation policy, serialized transitive provenance, and complete TCB/SBOM are absent",
    "FAIL CLOSED release gates: shared warm cache is not cold hermetic evidence and this worker is not a distinct independent verifier",
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
    if result.returncode < 0:
        raise RuntimeError(
            f"command terminated by signal {-result.returncode}: {argv!r}\n{result.stdout}"
        )
    if result.returncode != 0:
        raise RuntimeError(f"command failed ({result.returncode}): {argv!r}\n{result.stdout}")
    return result.stdout


BASE_ENV = {
    "HOME": os.environ["HOME"],
    "PATH": f"{os.environ['HOME']}/.elan/bin:/usr/bin:/bin",
    "ELAN_TOOLCHAIN": TOOLCHAIN,
    "LANG": "C.UTF-8",
    "LC_ALL": "C.UTF-8",
    "TZ": "UTC",
    "LEAN_NUM_THREADS": "1",
}


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["/usr/bin/git", *args], cwd=cwd, env=BASE_ENV).strip()


def source_without_comments_and_strings(source: str) -> str:
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


def reported_axioms(output: str, declaration: str) -> set[str]:
    pattern = re.compile(
        re.escape(f"'{declaration}' depends on axioms: [") + r"(.*?)]", re.DOTALL
    )
    matches = pattern.findall(output)
    assert len(matches) == 1, f"missing or duplicate axiom report for {declaration}"
    return {part.strip() for part in matches[0].split(",") if part.strip()}


def pinned_lean_path(lean: Path) -> str:
    package_names = (
        "batteries", "Qq", "aesop", "proofwidgets", "importGraph",
        "LeanSearchClient", "plausible", "mathlib",
    )
    roots = [
        (LEAN_ROOT / ".lake" / "packages" / name / ".lake/build/lib/lean").resolve()
        for name in package_names
    ]
    assert all(path.is_dir() for path in roots)
    local = (LEAN_ROOT / ".lake/build/lib/lean").resolve()
    assert local.is_dir()
    return ":".join([*(str(path) for path in roots), str(local), str(lean.parent.parent / "lib/lean")])


def isolated_replay(lean: Path, bwrap: Path, lean_path: str) -> dict[str, str]:
    with tempfile.TemporaryDirectory(prefix="stage1-m1010-validation-", dir="/tmp") as tmp_name:
        tmp = Path(tmp_name).resolve()
        module_dir = tmp / "Stage1_Instances" / THEOREM
        module_dir.mkdir(parents=True)
        for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
            shutil.copy2(HERE / name, module_dir / name)
        (tmp / "home").mkdir()
        base = [
            str(bwrap), "--ro-bind", "/", "/", "--bind", str(tmp), str(tmp),
            "--dev", "/dev", "--proc", "/proc", "--unshare-net", "--die-with-parent",
            "--clearenv", "--setenv", "HOME", str(tmp / "home"), "--setenv", "TMPDIR",
            str(tmp), "--setenv", "LANG", "C.UTF-8", "--setenv", "LC_ALL", "C.UTF-8",
            "--setenv", "TZ", "UTC", "--setenv", "LEAN_NUM_THREADS", "1", "--chdir",
            str(tmp),
        ]

        def lean_run(name: str, module_path: str, emit_olean: bool) -> str:
            argv = base + ["--setenv", "LEAN_PATH", module_path, str(lean), "--trust=0", "-t0"]
            if emit_olean:
                argv += ["-o", str(module_dir / name.replace(".lean", ".olean"))]
            argv.append(str(module_dir / name))
            return run(argv)

        statement = lean_run("Statement.lean", lean_path, True)
        tree = lean_run("ObligationTree.lean", f"{tmp}:{lean_path}", True)
        proof = lean_run("Proof.lean", f"{tmp}:{lean_path}", True)
        validation = lean_run("Validation.lean", f"{tmp}:{lean_path}", False)
        return {
            "statement": statement,
            "obligation_tree": tree,
            "proof": proof,
            "validation": validation,
        }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--probe", action="store_true")
    parser.add_argument("--worker-packet", type=Path)
    args = parser.parse_args()

    execution = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")
    targets = load(ROOT / "Docs" / "Stage1_Targets_rev-5.6.json")
    statement = load(HERE / "statement.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    proof_receipt = load(HERE / "proof-receipt.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target == {
        "execution_rank": 290,
        "legacy_priority_slot": "S1-M-290",
        "theorem_id": THEOREM,
        "name": "Skorokhod表示定理",
        "category": "概率论与随机过程 / 概率论基础",
        "source_status_untrusted": "已验证",
        "baseline": "L0",
        "rework_required": True,
        "legacy_artifacts_accepted": False,
        "target_lane": "hard_mathlib_anchor_and_wrapper",
        "intake_score": 138,
        "lifecycle_mode": "planned",
        "theorem_complete": False,
    }
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item == {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 290,
        "phase": "validation",
        "layer": 5,
        "state": "[ ]",
        "depends_on": ["S56-M-1010-PROOF"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Run hermetic kernel, trust, provenance, and independent validation gates.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }
    predecessor = next(row for row in execution["items"] if row["id"] == "S56-M-1010-PROOF")
    assert predecessor["state"] == "[_]" and predecessor["attempts"] == 1

    for name, expected in EXPECTED_INPUTS.items():
        assert sha256(HERE / name) == expected, f"stale validation input: {name}"
    assert sha256(LEAN_ROOT / "lean-toolchain") == TOOLCHAIN_SHA256
    assert sha256(LEAN_ROOT / "lake-manifest.json") == MANIFEST_SHA256
    assert statement["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert registry["root_obligation_id"] == graphs["root_node_id"] == "M1010-ROOT"
    assert registry["denominator_sha256"] == graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert len(registry["obligations"]) == 15
    root = next(node for node in graphs["nodes"] if node["obligation_id"] == "M1010-ROOT")
    assert {
        "H": root["human_debt"], "M": root["machine_debt"], "R": root["readability_debt"]
    } == ROOT_VECTOR
    closure = graphs["closure_boundary"]
    assert closure["root_closed"] is False and closure["audit_complete"] is False
    assert closure["theorem_complete"] is False and closure["remaining_root_cut_set"] == OPEN_ROOT_CUT
    assert closure["composition_certificates"] == [COMPOSITION_DECLARATION]

    assert proof_receipt["item_id"] == "S56-M-1010-PROOF" and proof_receipt["accepted"] is False
    assert proof_receipt["supported_obligation_ids"] == []
    assert proof_receipt["provisionally_closed_obligation_ids"] == []
    assert proof_receipt["accepted_closed_obligation_ids"] == []
    assert proof_receipt["result"]["proof_phase_complete"] is False
    assert proof_receipt["result"]["root_kernel_closed"] is False
    assert proof_receipt["result"]["theorem_complete"] is False
    assert proof_receipt["remaining_root_cut_set"] == OPEN_ROOT_CUT

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by|run_tac|oracle)\b|"
        r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
        r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
        r"(?:axiom|constant|opaque|unsafe|extern)\b",
        flags=re.MULTILINE,
    )
    for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
        source = source_without_comments_and_strings((HERE / name).read_text(encoding="utf-8"))
        assert prohibited.search(source) is None, name
    proof_source = source_without_comments_and_strings((HERE / "Proof.lean").read_text())
    assert not re.search(r"^theorem\s+(?:Target|CouplingPackage)\b", proof_source, re.MULTILINE)

    manifest = load(LEAN_ROOT / "lake-manifest.json")
    mathlib_entry = next(row for row in manifest["packages"] if row["name"] == "mathlib")
    assert mathlib_entry["rev"] == mathlib_entry["inputRev"] == MATHLIB_REVISION
    assert mathlib_entry["url"] == MATHLIB_REMOTE
    assert (LEAN_ROOT / ".lake").is_symlink()
    mathlib = (LEAN_ROOT / ".lake/packages/mathlib").resolve()
    assert git("rev-parse", "HEAD", cwd=mathlib) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == MATHLIB_TREE
    assert git("status", "--porcelain=v1", "--untracked-files=all", cwd=mathlib) == ""
    assert git("remote", "get-url", "origin", cwd=mathlib) == MATHLIB_REMOTE
    assert sha256(mathlib / "LICENSE") == MATHLIB_LICENSE_SHA256
    for relative, expected in SOURCE_BOUNDARIES.items():
        source = mathlib / relative
        olean = mathlib / ".lake/build/lib/lean" / Path(relative).with_suffix(".olean")
        assert git("rev-parse", f"HEAD:{relative}", cwd=mathlib) == expected["blob"]
        assert sha256(source) == expected["source_sha256"]
        assert sha256(olean) == expected["olean_sha256"]
        assert olean.stat().st_size == expected["olean_bytes"]

    toolchain_dir = TOOLCHAIN.replace("/", "--").replace(":", "---")
    lean = Path(os.environ["HOME"]) / ".elan" / "toolchains" / toolchain_dir / "bin" / "lean"
    lake = lean.with_name("lake")
    bwrap = Path("/usr/bin/bwrap")
    python = Path("/usr/bin/python3").resolve()
    assert sha256(lean) == LEAN_SHA256 and sha256(lake) == LAKE_SHA256
    assert sha256(bwrap) == BWRAP_SHA256 and sha256(python) == PYTHON_SHA256
    assert sha256(Path("/usr/bin/git")) == GIT_SHA256
    assert LEAN_COMMIT in run([str(lean), "--version"], env=BASE_ENV)
    assert "5.0.0-src+98dc76e" in run([str(lake), "--version"], env=BASE_ENV)

    outputs = isolated_replay(lean, bwrap, pinned_lean_path(lean))
    combined = "\n".join(outputs.values())
    assert "sorryAx" not in combined and all("error:" not in output for output in outputs.values())
    for declaration in PROOF_DECLARATIONS:
        assert reported_axioms(outputs["proof"], declaration) == EXPECTED_AXIOMS
    for declaration in (*PROOF_DECLARATIONS, COMPOSITION_DECLARATION):
        assert reported_axioms(outputs["validation"], declaration) == EXPECTED_AXIOMS
    assert outputs["validation"].count("Declarations are sorry-free!") == 4
    closure_match = re.search(
        r"VALIDATION_CLOSURE roots=(\d+) declarations=(\d+) modules=(\d+)",
        outputs["validation"],
    )
    assert closure_match is not None and int(closure_match.group(1)) == 4
    assert "VALIDATION_CLOSURE axioms=[propext, Classical.choice, Quot.sound]" in outputs["validation"]
    assert "VALIDATION_CLOSURE bodyless_nonaxioms=[]" in outputs["validation"]
    assert "VALIDATION_CLOSURE unsafe=[]" in outputs["validation"]
    observation = {
        "lean_output_sha256": {
            name: hashlib.sha256(output.encode()).hexdigest() for name, output in outputs.items()
        },
        "observed_axioms": sorted(EXPECTED_AXIOMS),
        "validation_closure": {
            "roots": 4,
            "declarations": int(closure_match.group(2)),
            "modules": int(closure_match.group(3)),
            "bodyless_nonaxioms": [],
            "unsafe": [],
        },
    }
    expected_observation = {
        "lean_output_sha256": {
            "statement": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
            "obligation_tree": "cbee87b9fcb01d1f01f3df744768b1af976aa032d917174e3500f2a6a9329abb",
            "proof": "c838da65db3b5a285200610e3094263883081320d51304baa0efd577ed661832",
            "validation": "03d968f484dae96e5406bd4d9cc7bbe5761694a1a4ccb555bd0ec9a2c2744f41",
        },
        "observed_axioms": ["Classical.choice", "Quot.sound", "propext"],
        "validation_closure": {
            "roots": 4,
            "declarations": 27818,
            "modules": 1019,
            "bodyless_nonaxioms": [],
            "unsafe": [],
        },
    }
    assert observation == expected_observation
    if args.probe:
        print(json.dumps(observation, sort_keys=True))
        return

    spec = load(HERE / "validation-spec.json")
    receipt = load(HERE / "validation-receipt.json")
    blocker = load(HERE / "validation-blocker.json")
    packet_path = args.worker_packet or (ROOT / ".stage1-worker-selftest.json")
    packet = load(packet_path.resolve())
    assert receipt["inputs"]["check_validation.py"] == sha256(HERE / "check_validation.py")
    assert receipt["inputs"]["validation-spec.json"] == sha256(HERE / "validation-spec.json")
    assert receipt["inputs"]["Validation.lean"] == sha256(HERE / "Validation.lean")
    assert spec["schema_version"] == "stage1-validation-spec/1.0"
    assert spec["item_id"] == receipt["item_id"] == blocker["item_id"] == packet["item_id"] == ITEM
    assert spec["theorem_id"] == receipt["theorem_id"] == blocker["theorem_id"] == THEOREM
    assert spec["depends_on"] == receipt["depends_on"] == ["S56-M-1010-PROOF"]
    assert len(spec["recipes"]) == 1 and spec["recipes"][0] == receipt["recipe"]
    recipe = spec["recipes"][0]
    assert recipe["argv"] == [
        "python3", "-I", "-B", f"Stage1_Instances/{THEOREM}/check_validation.py",
        "--worker-packet", ".stage1-worker-selftest.json",
    ]
    assert recipe["cwd"] == "." and recipe["timeout_seconds"] == 600
    assert recipe["network_policy"] == "denied" and recipe["expected_exit"] == 0
    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["phase"] == "validation" and receipt["intent"] == "validate"
    assert receipt["base_revision"] == blocker["base_revision"] == packet["base_revision"] == BASE_REVISION
    assert receipt["base_tree"] == blocker["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["verdict"] == "blocked" and receipt["release_grade"] is False
    assert receipt["canonical_target_expression_sha256"] == EXPRESSION_SHA256
    assert receipt["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert receipt["result"]["root_kernel_closed"] is False
    assert receipt["result"]["validation_complete"] is False
    assert receipt["result"]["hermetic_cold_offline_replay"] == "fail_closed"
    assert receipt["result"]["independent_distinct_runner"] == "fail_closed"
    assert receipt["result"]["lean_output_sha256"] == observation["lean_output_sha256"]
    assert receipt["result"]["observed_axioms"] == observation["observed_axioms"]
    assert receipt["result"]["validation_closure"] == {
        "roots": observation["validation_closure"]["roots"],
        "declarations": observation["validation_closure"]["declarations"],
        "modules": observation["validation_closure"]["modules"],
        "bodyless_nonaxioms": [],
        "unsafe_declarations": [],
    }
    assert receipt["result"]["audit_complete"] is receipt["result"]["theorem_complete"] is False
    assert receipt["remaining_root_cut_set"] == OPEN_ROOT_CUT
    assert blocker["outcome"] == "validation_packet_self_tested_gates_blocked"
    assert blocker["validation_phase_complete"] is False
    assert blocker["root_closed"] is blocker["audit_complete"] is blocker["theorem_complete"] is False
    assert set(packet) == {
        "item_id", "changed_paths", "commands", "output_summary", "base_revision",
        "known_failures", "state",
    }
    assert packet["state"] == "[_]"
    assert packet["changed_paths"] == receipt["changed_paths"] == CHANGED_PATHS
    assert packet["known_failures"] == receipt["known_failures"]
    status = git("status", "--short", "--untracked-files=all")
    actual = [line[3:] for line in status.splitlines() if line[3:] != "Formalizations/Lean/.lake"]
    assert sorted(actual) == sorted(CHANGED_PATHS), (actual, CHANGED_PATHS)
    for relative in CHANGED_PATHS:
        data = (ROOT / relative).read_bytes()
        assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())

    for line in SUMMARY_LINES:
        print(line)


if __name__ == "__main__":
    main()
