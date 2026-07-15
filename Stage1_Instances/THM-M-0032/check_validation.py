#!/usr/bin/env python3
"""Fail-closed narrow validator for S56-M-0032-VALIDATION."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0032"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
ITEM = "S56-M-0032-VALIDATION"
THEOREM = "THM-M-0032"
BASE_REVISION = "289e3709a4204b41baa98cb95e0548b9811b26bb"
BASE_TREE = "6adc6103dba02e89467851fce1b2f6e301490938"
TOOLCHAIN = "leanprover/lean4:v4.29.0"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MATHLIB_REMOTE = "https://github.com/leanprover-community/mathlib4.git"
MATHLIB_LICENSE_SHA256 = "b40930bbcf80744c86c46a12bc9da056641d722716c378f5659b9e555ef833e1"
LEAN_SHA256 = "3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf"
LAKE_SHA256 = "a608ff084d7e2af228b92a29d7c2fd083ba0580e46889175ec74a81678c98359"
ELAN_SHA256 = "840179e70803ef373c2ec53342d6a45ea7d022533e4145489fc1278b4f716385"
BWRAP_SHA256 = "0abea81db798ebf6b4742ac0664802d97521547a353c2a0dbdc21d76cbbfd2c0"
PYTHON_SHA256 = "b8d8288faefdd300201f43fcf00f6f539a27218eeed3a3dff5ab10b9c4c99700"
GIT_SHA256 = "5516c9f362c29376ab9a499a33082f9f611941d8c75930c880e30ad109e39c9a"
TOOLCHAIN_SHA256 = "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2"
MANIFEST_SHA256 = "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81"
EXPRESSION_SHA256 = "199d16d669438ea6e1cd556adbc4a9475805acf048379e01ae1a1f75f453a8d8"
DENOMINATOR_SHA256 = "7ddbec795ccfc7f42c1efc171aee6f2e8d1a82af6f5bb5d2382c926d64d451c7"
ROOT_VECTOR = {"H": "H1", "M": "M3", "R": "R4"}
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
OPEN_MACHINE_CUT = ["M0032-A-PRIME-ELEMENT"]
OPEN_ROOT_CUT = [
    "M0032-A-PRIME-ELEMENT",
    "M0032-X-PRIMARY-SOURCE",
    "M0032-S-FOUNDATION",
    "M0032-X-PROVENANCE",
    "M0032-X-TRUST",
    "M0032-X-READABLE",
    "M0032-X-WORKFLOW",
]
PROVISIONALLY_VALIDATED = ["M0032-N-DOMAIN"]
LEAN_NAMES = (
    "Statement.lean",
    "AnchorAudit.lean",
    "ObligationTree.lean",
    "DomainProof.lean",
    "Validation.lean",
)
EXPECTED_INPUTS = {
    "Statement.lean": "5391ab5cef4895413e28fcabe5a3e23e7b93aeea643c1fbae991223c34c07f3a",
    "AnchorAudit.lean": "54671e8ba0bd947b08a9fead77160812fe1be69fa0f5b7ba059556bd600cba76",
    "ObligationTree.lean": "9c54c27a3eb16d8c5c9e1e582c3b8decd6fd601baa5d6e6b58c3d6bddd1617e8",
    "DomainProof.lean": "d238dcaca7887307661b22a6169286187cc3d780253ffbab26207f8c9a0dae35",
    "Validation.lean": "3d13b20adc4077ca1701926f8436f3793eddfc1b1a63d45fbfb285c77ae0feee",
    "statement.json": "c3a183b2e1632a888fd50a719ce4271784d0482cabc281e17b6de11dded2785f",
    "anchor-audit.json": "76df6db906b70a95b31c7803e7dc29d8ea57fb3b0fc0852531fe1ca05884ade1",
    "obligation-registry.json": "29620e59139767a5cd261a5cf493400d7be1c01eeb315174fe03007054b16e18",
    "typed-graphs.json": "694914102c38ed74d6ef00b29cb7795430f58f8f950399e356125f333dab53ef",
    "validation-specs.json": "7264d42f4aa9fcedf2ecf0981f51494a23aca4c7df429659ae85378298c29197",
    "proof-receipt-partial-domain.json": "76f53f0f61e3dfe61fb3f6575b01ce04eebe726f27e4ed41a26e6e969f8ab027",
    "instance.json": "63f0252c106a794e4f3ad1f5451299cb0cbd6b4101ddc4233a13a0d8fc54fc99",
    "task-dag.json": "4b1b2df37a2842748442d1f0f7e484370cb9a7f25eda0f4daed45502e6796a7e",
    "validation-spec.json": "e106db22d27e43a9c68a96270c7f7207025c88cc2c9ac2540646c5e79d23bb7c",
    "validation-blocker.json": "b5555b6ca4e0390210998f9e700da055db8e00e863c5281ec6db4f803774058a",
    "validation-phase.md": "444a425d6a94f0f58c5421225147e4b715fe99088fa4c23f362e84ed1c7f3dfe",
}
SOURCE_PROVENANCE = {
    "Mathlib/RingTheory/Ideal/MinimalPrime/Noetherian.lean": {
        "blob": "095b86bfd5f04212cbeedadbe98bbc0bf145d222",
        "source_sha256": "3cd749379a133d461f389db748343a0011a72939a2ed6221d6ff6e6fe7aa6546",
        "olean_sha256": "a9e609d93908c4639de3c581c1ba1e102a46502c35f79f763ea071e4a6699db9",
    },
    "Mathlib/RingTheory/UniqueFactorizationDomain/Kaplansky.lean": {
        "blob": "800605f6d9dfa41a3817e420dfef18aaa8a3d425",
        "source_sha256": "1ce495be94eba57eeac5e8d114b0ad548cd6266c8351abbd54138b426e9e40a6",
        "olean_sha256": "32f0df60173cd44fe80094de97f80705e1496bf28e2df5a27c52e63ce38a9bec",
    },
    "Mathlib/RingTheory/RegularLocalRing/Defs.lean": {
        "blob": "fc526882c0c464a9132d0cc8a4386ec35b76b65a",
        "source_sha256": "3031d9946232a1d726a4556d0674632345b0877f049a23c104c495f5b2128c6f",
        "olean_sha256": "c478e113748adf9a905700cb97e9b3d96ba632331fb72c96f123e920385add03",
    },
    "Mathlib/Util/AssertNoSorry.lean": {
        "blob": "060d8a764d2a6d1d2963d9c500b6084a05bed534",
        "source_sha256": "aa9f7bebacafc688c894ef2171930e51ed19e0dfe722581848a2414d28900d4d",
        "olean_sha256": "c8bf37753d9bad47b9fe67e32436da8b9af516a4abbbe14e74726f01ba2fb30b",
    },
    "Mathlib/Util/PrintSorries.lean": {
        "blob": "24d72cc680fa8b07f0d1062f670a5a824934a227",
        "source_sha256": "03670b0b0007740e5390dadd49c3d10a02b7d0919092d2b3214ef8a6a8cf798f",
        "olean_sha256": "9bcc4076e0aee5febb2eea5cf9dc959f38526e9f974afdfdd8658bfd318d5bb7",
    },
}
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
    "PASS narrow kernel replay: exact statement, anchor probe, conditional composition, domain package, and validation closure elaborated at trust zero",
    "PASS trust observation: four checked roots are sorry-free and use only propext, Classical.choice, and Quot.sound",
    "PASS selected provenance: frozen inputs, clean mathlib pin/tree/remote, five selected sources and oleans, toolchain, and license agree",
    "OPEN exact root: RegularLocalPrimeElementPackage has no inhabitant; accepted root remains M3 with machine cut M0032-A-PRIME-ELEMENT",
    "FAIL CLOSED proof dependency: S56-M-0032-PROOF is worker-provisional rather than master-accepted",
    "FAIL CLOSED release gates: complete TCB/provenance, cold hermetic replay, and distinct signed independent verification are unavailable",
]

if not __debug__:
    raise RuntimeError("validation requires Python assertions; optimized mode is forbidden")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


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


def run(
    argv: list[str], *, cwd: Path = ROOT, env: dict[str, str] | None = None,
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
    return run(["/usr/bin/git", *args], cwd=cwd).strip()


def code_without_comments(source: str) -> str:
    """Remove nested Lean comments and strings for defense-in-depth scans."""
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
            end = source.find("\n", index)
            index = len(source) if end < 0 else end
        elif source[index] == '"':
            in_string = True
            output.append('"')
            index += 1
        else:
            output.append(source[index])
            index += 1
    assert depth == 0 and not in_string, "unterminated Lean comment or string"
    return "".join(output)


def printed_axioms(output: str, declaration: str) -> set[str]:
    match = re.search(
        rf"'[^']*{re.escape(declaration)}' depends on axioms:\s*\[(.*?)\]",
        output,
        flags=re.DOTALL,
    )
    assert match is not None, (declaration, output)
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
    roots = sorted(
        (path / ".lake" / "build" / "lib" / "lean").resolve()
        for path in (LEAN_ROOT / ".lake" / "packages").iterdir()
        if path.is_dir() and (path / ".lake" / "build" / "lib" / "lean").is_dir()
    )
    assert roots, "no pre-existing pinned compiled artifacts"
    return roots


def sandboxed_replay(lean: Path, bwrap: Path) -> dict[str, str]:
    with tempfile.TemporaryDirectory(prefix="m0032-validation-", dir="/tmp") as tmp_name:
        tmp = Path(tmp_name).resolve()
        for name in LEAN_NAMES:
            (tmp / name).write_bytes((HERE / name).read_bytes())
        dependency_path = ":".join(str(path) for path in compiled_roots())
        base = [
            str(bwrap), "--ro-bind", "/", "/", "--bind", str(tmp), str(tmp),
            "--dev", "/dev", "--proc", "/proc", "--unshare-net",
            "--die-with-parent", "--clearenv", "--setenv", "HOME", str(tmp),
            "--setenv", "TMPDIR", str(tmp), "--setenv", "LANG", "C.UTF-8",
            "--setenv", "LC_ALL", "C.UTF-8", "--setenv", "TZ", "UTC",
            "--setenv", "LEAN_NUM_THREADS", "1", "--chdir", str(tmp),
        ]

        def lean_run(name: str, local_imports: bool, emit_olean: bool) -> str:
            lean_path = f"{tmp}:{dependency_path}" if local_imports else dependency_path
            argv = base + ["--setenv", "LEAN_PATH", lean_path, str(lean), "--trust=0", "-t0"]
            if emit_olean:
                argv += ["-o", Path(name).with_suffix(".olean").name]
            argv.append(name)
            return run(argv, timeout=600)

        return {
            "statement": lean_run("Statement.lean", False, True),
            "anchor_audit": lean_run("AnchorAudit.lean", True, False),
            "obligation_tree": lean_run("ObligationTree.lean", True, True),
            "domain_proof": lean_run("DomainProof.lean", True, True),
            "validation": lean_run("Validation.lean", True, False),
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
    old_specs = load(HERE / "validation-specs.json")
    proof_receipt = load(HERE / "proof-receipt-partial-domain.json")
    instance = load(HERE / "instance.json")
    local_tasks = load(HERE / "task-dag.json")
    spec = load(HERE / "validation-spec.json")
    blocker = load(HERE / "validation-blocker.json")
    receipt = load(HERE / "validation-receipt.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 1076 and target["baseline"] == "L0"
    assert target["lifecycle_mode"] == "planned"
    assert target["rework_required"] is True and target["theorem_complete"] is False
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item == {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 1076,
        "phase": "validation",
        "layer": 5,
        "state": "[ ]",
        "depends_on": ["S56-M-0032-PROOF"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Run hermetic kernel, trust, provenance, and independent validation gates.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }
    predecessor = next(row for row in execution["items"] if row["id"] == "S56-M-0032-PROOF")
    assert predecessor["state"] == "[_]" and predecessor["attempts"] == 1
    dependency_accepted = (
        predecessor["state"] == "[x]"
        and proof_receipt.get("support_state") == "master_accepted"
    )
    assert dependency_accepted is False
    assert local_tasks["accepted_states"] == []
    assert all(task["state"] == "open" for task in local_tasks["tasks"])

    for name, expected in EXPECTED_INPUTS.items():
        assert sha256(HERE / name) == expected, f"stale validation input: {name}"
    assert sha256(LEAN_ROOT / "lean-toolchain") == TOOLCHAIN_SHA256
    assert sha256(LEAN_ROOT / "lake-manifest.json") == MANIFEST_SHA256
    canonical = statement["canonical_formal_target"]
    assert canonical["declaration_or_expression"] == (
        "Stage1Instances.THM_M_0032.AuslanderBuchsbaumUFDTarget"
    )
    assert canonical["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert canonical["statement_file_sha256"] == EXPECTED_INPUTS["Statement.lean"]
    assert registry["frozen_against_statement_sha256"] == EXPECTED_INPUTS["Statement.lean"]
    assert registry["frozen_against_anchor_audit_sha256"] == EXPECTED_INPUTS["anchor-audit.json"]
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    inventory = registry["frozen_denominators"]["inventory"]
    assert len(inventory) == 38 and len(set(inventory)) == 38
    assert [row["obligation_id"] for row in registry["obligations"]] == inventory
    assert len(old_specs["recipes"]) == len(inventory)
    assert {
        recipe["covered_obligation_ids"][0] for recipe in old_specs["recipes"]
    } == set(inventory)
    assert spec["schema_version"] == "stage1-validation-spec/1.0"
    assert spec["item_id"] == ITEM and spec["theorem_id"] == THEOREM
    assert spec["depends_on"] == ["S56-M-0032-PROOF"] and len(spec["recipes"]) == 1
    recipe = spec["recipes"][0]
    assert recipe["argv"] == [
        "/usr/bin/python3", "-I", "-B",
        f"Stage1_Instances/{THEOREM}/check_validation.py",
        "--worker-packet", ".stage1-worker-selftest.json",
    ]
    assert recipe["cwd"] == "." and recipe["env_allowlist"] == {}
    assert recipe["timeout_seconds"] == 600 and recipe["network_policy"] == "denied"
    assert recipe["expected_exit"] == 0
    assert recipe["covered_obligation_ids"] == inventory
    assert receipt["base_revision"] == blocker["base_revision"] == BASE_REVISION
    assert receipt["base_tree"] == blocker["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["release_grade"] is receipt["content_addressed_release_evidence"] is False
    expected_worktree_hashes = {
        relative: sha256(ROOT / relative)
        for relative in CHANGED_PATHS
        if relative not in {
            ".stage1-worker-selftest.json",
            f"Stage1_Instances/{THEOREM}/validation-receipt.json",
        }
    }
    expected_worktree_hashes[f"Stage1_Instances/{THEOREM}/validation-receipt.json"] = (
        "self_referential_excluded_from_owned_changed_path_sha256"
    )
    assert receipt["worktree_evidence"]["owned_changed_path_sha256"] == expected_worktree_hashes
    assert receipt["worktree_evidence"]["preexisting_untracked_paths"] == [
        "Formalizations/Lean/.lake"
    ]

    root = next(node for node in graphs["nodes"] if node["obligation_id"] == "M0032-ROOT")
    assert {
        "H": root["human_debt"], "M": root["machine_debt"], "R": root["readability_debt"]
    } == ROOT_VECTOR
    closure = graphs["closure_boundary"]
    assert closure["accepted_closed_obligations"] == []
    assert closure["root_closed"] is False and closure["root_machine_debt"] == "M3"
    assert closure["audit_complete"] is closure["theorem_complete"] is False
    assert instance["lifecycle_mode"] == "planned" and instance["root_vector"] == ROOT_VECTOR
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == []
    assert instance["audit_complete"] is instance["theorem_complete"] is False
    assert proof_receipt["item_id"] == "S56-M-0032-PROOF"
    assert proof_receipt["accepted"] is False
    assert proof_receipt["provisionally_closed_obligation_ids"] == PROVISIONALLY_VALIDATED
    assert proof_receipt["accepted_closed_obligation_ids"] == []
    assert proof_receipt["result"]["domain_package_kernel_closed"] is True
    assert proof_receipt["result"]["root_kernel_closed"] is False
    assert proof_receipt["remaining_machine_proof_cut_set"] == OPEN_MACHINE_CUT
    assert proof_receipt["remaining_root_cut_set"] == OPEN_ROOT_CUT

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by|extern|run_tac)\b|"
        r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
        r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
        r"(?:axiom|constant|opaque|unsafe)\b",
        flags=re.MULTILINE,
    )
    for name in LEAN_NAMES:
        assert prohibited.search(code_without_comments((HERE / name).read_text())) is None, name
    validation_source = code_without_comments((HERE / "Validation.lean").read_text())
    assert "assert_no_sorry regularLocalDomainPackage" in validation_source
    assert "assert_no_sorry root_of_domain_primeElement_and_kaplansky" in validation_source
    assert "theorem rootFromPrimeElement" not in validation_source
    assert "RegularLocalPrimeElementPackage" not in validation_source

    manifest = load(LEAN_ROOT / "lake-manifest.json")
    mathlib_entry = next(row for row in manifest["packages"] if row["name"] == "mathlib")
    assert mathlib_entry["rev"] == mathlib_entry["inputRev"] == MATHLIB_REVISION
    assert (LEAN_ROOT / ".lake").is_symlink()
    mathlib = (LEAN_ROOT / ".lake" / "packages" / "mathlib").resolve()
    assert git("rev-parse", "HEAD", cwd=mathlib) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == MATHLIB_TREE
    assert git("remote", "get-url", "origin", cwd=mathlib) == MATHLIB_REMOTE
    assert git("status", "--porcelain=v1", cwd=mathlib) == ""
    assert sha256(mathlib / "LICENSE") == MATHLIB_LICENSE_SHA256
    for relative, expected in SOURCE_PROVENANCE.items():
        source = mathlib / relative
        olean = mathlib / ".lake" / "build" / "lib" / "lean" / Path(relative).with_suffix(".olean")
        assert git("rev-parse", f"HEAD:{relative}", cwd=mathlib) == expected["blob"]
        assert sha256(source) == expected["source_sha256"]
        assert sha256(olean) == expected["olean_sha256"]

    fixed_env = {
        "ELAN_TOOLCHAIN": TOOLCHAIN,
        "LANG": "C.UTF-8",
        "LC_ALL": "C.UTF-8",
        "TZ": "UTC",
        "LEAN_NUM_THREADS": "1",
    }
    elan = Path("/home/sansha-2/.elan/bin/elan")
    bwrap = Path("/usr/bin/bwrap")
    python = Path("/usr/bin/python3").resolve()
    git_executable = Path("/usr/bin/git")
    tool_root = Path.home() / ".elan" / "toolchains" / "leanprover--lean4---v4.29.0" / "bin"
    lean = tool_root / "lean"
    lake = tool_root / "lake"
    assert sha256(lean) == LEAN_SHA256
    assert sha256(lake) == LAKE_SHA256
    assert sha256(elan) == ELAN_SHA256
    assert sha256(bwrap) == BWRAP_SHA256
    assert sha256(python) == PYTHON_SHA256
    assert sha256(git_executable) == GIT_SHA256
    assert LEAN_COMMIT in run([str(lean), "--version"], env=fixed_env)
    assert "5.0.0-src+98dc76e" in run([str(lake), "--version"], env=fixed_env)

    outputs = sandboxed_replay(lean, bwrap)
    declaration_outputs = {
        "regularLocalRing_isDomain": outputs["domain_proof"] + outputs["validation"],
        "regularLocalDomainPackage": outputs["domain_proof"] + outputs["validation"],
        "pinnedKaplanskyCriterionPackage": outputs["obligation_tree"] + outputs["validation"],
        "root_of_domain_primeElement_and_kaplansky": (
            outputs["obligation_tree"] + outputs["validation"]
        ),
    }
    for declaration, output in declaration_outputs.items():
        assert printed_axioms(output, declaration) == EXPECTED_AXIOMS, declaration
    validation_output = outputs["validation"]
    assert validation_output.count("Declarations are sorry-free!") == 4
    assert "VALIDATION_CLOSURE roots=4 declarations=22572 modules=841" in validation_output
    assert "VALIDATION_CLOSURE axioms=[propext, Classical.choice, Quot.sound]" in validation_output
    assert "VALIDATION_CLOSURE bodyless_nonaxioms=[]" in validation_output
    assert "VALIDATION_CLOSURE unsafe=[]" in validation_output
    assert "error:" not in "\n".join(outputs.values()).lower()

    assert blocker["item_id"] == receipt["item_id"] == ITEM
    assert blocker["verdict"] == receipt["verdict"] == "blocked"
    assert blocker["proposed_state"] == receipt["proposed_state"] == "[_]"
    assert blocker["accepted"] is receipt["accepted"] is False
    assert blocker["root_kernel_closed"] is receipt["result"]["root_kernel_closed"] is False
    assert blocker["validation_phase_complete"] is receipt["result"]["validation_complete"] is False
    assert blocker["audit_complete"] is blocker["theorem_complete"] is False
    assert receipt["result"]["audit_complete"] is receipt["result"]["theorem_complete"] is False
    assert blocker["root_vector_before"] == blocker["root_vector_after"] == ROOT_VECTOR
    assert receipt["root_vector_before"] == receipt["root_vector_after_worker_selftest"] == ROOT_VECTOR
    assert blocker["provisionally_validated_obligation_ids"] == PROVISIONALLY_VALIDATED
    assert receipt["provisionally_validated_obligation_ids"] == PROVISIONALLY_VALIDATED
    assert blocker["accepted_closed_obligation_ids"] == receipt["accepted_closed_obligation_ids"] == []
    assert blocker["remaining_machine_proof_cut_set"] == OPEN_MACHINE_CUT
    assert receipt["remaining_machine_proof_cut_set"] == OPEN_MACHINE_CUT
    assert blocker["remaining_root_cut_set"] == receipt["remaining_root_cut_set"] == OPEN_ROOT_CUT
    assert blocker["first_failed_gate"] == receipt["first_failed_gate"] == (
        "dependency.S56-M-0032-PROOF.master_acceptance"
    )
    assert blocker["changed_paths"] == receipt["changed_paths"] == CHANGED_PATHS
    for key, expected in EXPECTED_INPUTS.items():
        assert receipt["inputs"][key] == expected
    assert receipt["inputs"]["check_validation.py"] == sha256(HERE / "check_validation.py")
    for key in (
        "recipe_id", "cwd", "argv", "env_allowlist", "timeout_seconds",
        "network_policy", "expected_exit", "expected_outputs", "covered_obligation_ids",
        "covered_declarations", "coverage_boundary",
    ):
        assert receipt["recipe"][key] == recipe[key], key
    expected_output_hashes = {
        "statement": "2a26d392cff0eab1fc3a25aed89898827f02c059f9dc7c4f21748ab0c86637d1",
        "anchor_audit": "8d3b1018d6ad7a7fc5dd1cdcfdb53ad9a83146347c8d7a9a82e128f937c9968f",
        "obligation_tree": "fc1829fe5092c0134ba770a658cf8c3f9bfc92247b1d1054fb2fc679b6fc5e12",
        "domain_proof": "3365f3ee3c477ccae203b7f5ca7a853b8dc523163d47ad9a01a2dd446f634b94",
        "validation": "7e123a7b506c494058f6256222924e94849f665bdef7260c2cea7e569b5ad803",
    }
    assert receipt["result"]["lean_output_sha256"] == expected_output_hashes
    assert {
        name: hashlib.sha256(output.encode()).hexdigest()
        for name, output in outputs.items()
    } == expected_output_hashes
    assert receipt["result"]["validation_closure"] == {
        "roots": 4,
        "declarations": 22572,
        "modules": 841,
        "axioms": ["propext", "Classical.choice", "Quot.sound"],
        "bodyless_nonaxioms": [],
        "unsafe_declarations": [],
    }

    if args.worker_packet is not None:
        packet_path = args.worker_packet
        if not packet_path.is_absolute():
            packet_path = ROOT / packet_path
        packet = load(packet_path)
        assert set(packet) == {
            "item_id", "changed_paths", "commands", "output_summary",
            "base_revision", "known_failures", "state",
        }
        assert packet["item_id"] == ITEM and packet["state"] == "[_]"
        assert packet["base_revision"] == BASE_REVISION
        assert packet["changed_paths"] == CHANGED_PATHS
        assert packet["known_failures"] == receipt["known_failures"]
        assert packet["output_summary"] == "\n".join(SUMMARY_LINES)
        assert receipt["worktree_evidence"]["worker_packet_sha256"] == sha256(packet_path)
        assert packet["commands"][-1] == {
            "argv": recipe["argv"],
            "cwd": ".",
            "exit_code": 0,
            "output_summary": "exact six-line PASS/OPEN/FAIL CLOSED summary",
        }
        status = git("status", "--short", "--untracked-files=all")
        actual_changed = sorted(
            line[3:] for line in status.splitlines()
            if line[3:] != "Formalizations/Lean/.lake"
        )
        assert actual_changed == sorted(CHANGED_PATHS), (actual_changed, CHANGED_PATHS)
        for relative in CHANGED_PATHS:
            assert_text_hygiene(ROOT / relative)

    for line in SUMMARY_LINES:
        print(line)


if __name__ == "__main__":
    main()
