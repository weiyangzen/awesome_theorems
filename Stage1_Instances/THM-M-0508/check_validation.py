#!/usr/bin/env python3
"""Fail-closed narrow validator for S56-M-0508-VALIDATION."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import platform
import re
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0508"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
ITEM = "S56-M-0508-VALIDATION"
THEOREM = "THM-M-0508"
BASE_REVISION = "5b35bc151522d93c7f54966ef64f1fc630371537"
BASE_TREE = "fe77824631ab2573a4596bddc1a2534c06cd23f8"
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
EXPRESSION_SHA256 = "54ddaa6fe49c75368fd333adae9bc7ab50a9542516ef24d73fb5e43f0c1ac5fb"
DENOMINATOR_SHA256 = "79ff122b736335e90938cf7304db0b680dc23531e4d12d4b8c987d0ddc953bc2"
ROOT_VECTOR = {"H": "H1", "M": "M4", "R": "R3"}
OPEN_ROOT_CUT = [
    "M0508-N-FOURIER",
    "M0508-B-ARCS",
    "M0508-L-MAJOR",
    "M0508-L-SINGULAR",
    "M0508-L-MINOR",
]
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
SOURCE_PROVENANCE = {
    "Mathlib/Data/Nat/Prime/Basic.lean": {
        "blob": "e059d0ae408fdf5dcf90e34afbcc397a2f880a9b",
        "source_sha256": "b97e83d65681b68b3ad1f4bdfd36defd0a30aa173cf726b3d2807acf8bde5027",
        "olean_sha256": "40563ffd4a337bd07e5832a763aed1c5243602aba08aa0509844081b61b79d12",
    },
    "Mathlib/Order/Filter/AtTopBot/CountablyGenerated.lean": {
        "blob": "cdee995c5a8fe15511ae5505dcbb824663e00b56",
        "source_sha256": "6e5c6511f71d619068048f35cad01dc73a1e1a3d7c10f6373c37c34afebdfe25",
        "olean_sha256": "4cf22f4c12cace512db047a9105fb288bcd43981c28a093d097261103ebc585f",
    },
    "Mathlib/Data/Finset/Prod.lean": {
        "blob": "9161ff8ee434b8cb3305ad4a86ceb8dfc7d4dd7d",
        "source_sha256": "2cdc3c68d117332b7e947e3628a3903cd3a94cbed37764fe05f402966a979744",
        "olean_sha256": "17246154756657153ca03c888df021501b2befe866bc410c644e3084a20a69eb",
    },
    "Mathlib/NumberTheory/Chebyshev.lean": {
        "blob": "c35ccba69c47a62c6fdbc98569adf86c886ed663",
        "source_sha256": "6e69d416fc028b21782762876ee70af3f052295057b75baab1dac17d406abf98",
        "olean_sha256": "c3f1d510d800d12b1759dd39e881e182cf1614563f1b41e12ba03bda25357152",
    },
    "Mathlib/NumberTheory/SumPrimeReciprocals.lean": {
        "blob": "94e4d2573685272766a687bf557c0eee91d12780",
        "source_sha256": "7fe6a032b1a639a87b78dc67a444954fa3ec89a9b125d66de6047a0bdf042fe4",
        "olean_sha256": "275f7928c4524362426b26d18583f995f6067adcecf0bc152d4423182a67b36b",
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
EXPECTED_INPUTS = {
    "README.md": "d3059dc69f9957225dca13b444fed22498fd41d459cfd5cfa0ee62a41cee6676",
    "Statement.lean": "e27734b0b8a7c6ad8f858cba756fd1ac64abd3a7d3bbedde435c3d9a007080da",
    "ObligationTree.lean": "576a3fc66f3ed890202b5d02acdd4188b5edc1842bc8d06ae8906499e93aa172",
    "AnchorAudit.lean": "64a284fa92225bd52c38bcdb665e96a9073503a655fdb2abcdc5592442752ece",
    "Proof.lean": "b93b1556141f269c687cef3d4b738fa6f6dd8c3c49be01a9a4c8e5448bbe5e1f",
    "statement.json": "2ada9429a0cc593dddc826cb68156a9974116292fe9f42b433b109290b84a9b9",
    "anchor-audit.json": "dcb3df3d79927fa33a9ac3a28b128befb896b3c93e748f30e020963968a53d00",
    "obligation-registry.json": "1f5afb0285f5b3ed5b76f85ee0fc0dac5363b52a4d2f4c01fec35f1d6708d695",
    "typed-graphs.json": "86e4c89eba8b80aa5c8f4e0edbbd2e79d008ab7222a16e2fe811701568fb6539",
    "proof-receipt.json": "d212c0e5d69066fc0ad5be9588a2aace90555fa030c32012fd32033ee9dcd8b8",
    "proof-blocker.json": "dde0c80cd9f0cbafa25b4f244957f357a7be620b676622255335181c051e4ec0",
    "instance.json": "714166282856b99e8d0e1170a5187f7739e565cf38dc05cc57b4393869e24744",
    "task-dag.json": "0ed037db47be3f58c1428162b03c81e67222538d9e337789332ca4808ee77ac0",
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
    "PASS narrow kernel replay: statement, conditional handoff, proof interfaces, and differential composition elaborated at trust zero",
    "PASS trust observation: five checked declarations are sorry-free and use only propext, Classical.choice, and Quot.sound",
    "PASS selected provenance: frozen inputs, clean mathlib pin/tree/remote, seven selected sources and oleans, toolchain, and license agree",
    "OPEN exact root: no inhabitant of EventualPositiveRepresentationCount exists; root remains M4 on the frozen five-node cut",
    "FAIL CLOSED proof dependency: S56-M-0508-PROOF is worker-provisional rather than master-accepted",
    "FAIL CLOSED release gates: predecessor node specs, cold hermetic evidence, and a distinct signed verifier are absent",
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
    """Remove nested Lean comments while preserving strings for hygiene scans."""
    out: list[str] = []
    i = 0
    depth = 0
    in_string = False
    while i < len(source):
        if depth:
            if source.startswith("/-", i):
                depth += 1
                i += 2
            elif source.startswith("-/", i):
                depth -= 1
                i += 2
            else:
                i += 1
        elif in_string:
            if source[i] == "\\" and i + 1 < len(source):
                i += 2
            elif source[i] == '"':
                in_string = False
                out.append('"')
                i += 1
            else:
                i += 1
        elif source.startswith("/-", i):
            depth = 1
            i += 2
        elif source.startswith("--", i):
            end = source.find("\n", i)
            i = len(source) if end < 0 else end
        elif source[i] == '"':
            in_string = True
            out.append('"')
            i += 1
        else:
            out.append(source[i])
            i += 1
    assert depth == 0 and not in_string, "unterminated Lean comment or string"
    return "".join(out)


def printed_axioms(output: str, declaration: str) -> set[str]:
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


def sandboxed_replay(lean: Path, bwrap: Path) -> dict[str, str]:
    with tempfile.TemporaryDirectory(prefix="m0508-validation-", dir="/tmp") as tmp_name:
        tmp = Path(tmp_name).resolve()
        names = (
            "Statement.lean", "AnchorAudit.lean", "ObligationTree.lean",
            "Proof.lean", "Validation.lean",
        )
        for name in names:
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
            argv = base + ["--setenv", "LEAN_PATH", lean_path, str(lean), "--trust=0"]
            if emit_olean:
                argv += ["-o", Path(name).with_suffix(".olean").name]
            argv.append(name)
            return run(argv, timeout=600)

        return {
            "statement": lean_run("Statement.lean", False, True),
            "anchor_audit": lean_run("AnchorAudit.lean", True, False),
            "obligation_tree": lean_run("ObligationTree.lean", True, True),
            "proof": lean_run("Proof.lean", True, True),
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
    proof_receipt = load(HERE / "proof-receipt.json")
    proof_blocker = load(HERE / "proof-blocker.json")
    local_tasks = load(HERE / "task-dag.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 882 and target["baseline"] == "L0"
    assert target["lifecycle_mode"] == "planned"
    assert target["rework_required"] is True and target["theorem_complete"] is False
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item == {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 882,
        "phase": "validation",
        "layer": 5,
        "state": "[ ]",
        "depends_on": ["S56-M-0508-PROOF"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Run hermetic kernel, trust, provenance, and independent validation gates.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }
    predecessor = next(row for row in execution["items"] if row["id"] == "S56-M-0508-PROOF")
    assert predecessor["state"] == "[_]" and predecessor["attempts"] == 1
    dependency_accepted = (
        predecessor["state"] == "[x]"
        and proof_receipt.get("support_state") == "master_accepted"
    )
    assert dependency_accepted is False
    assert local_tasks["accepted_states"] == []
    assert all(task["state"] == "open" for task in local_tasks["tasks"])
    assert not (HERE / "validation-specs.json").exists()

    for name, expected in EXPECTED_INPUTS.items():
        assert sha256(HERE / name) == expected, f"stale validation input: {name}"
    assert sha256(LEAN_ROOT / "lean-toolchain") == TOOLCHAIN_SHA256
    assert sha256(LEAN_ROOT / "lake-manifest.json") == MANIFEST_SHA256
    assert statement["declaration"] == (
        "Stage1Instances.THM_M_0508.VinogradovThreePrimesTarget"
    )
    assert statement["environment_fingerprint"]["statement_source_sha256"] == (
        EXPECTED_INPUTS["Statement.lean"]
    )
    instance = load(HERE / "instance.json")
    assert instance["canonical_formal_target"]["elaborated_expression_hash"] == (
        f"sha256:{EXPRESSION_SHA256}"
    )
    assert registry["frozen_against_statement_sha256"] == EXPECTED_INPUTS["Statement.lean"]
    assert registry["frozen_against_anchor_audit_sha256"] == EXPECTED_INPUTS["anchor-audit.json"]
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    closure = graphs["closure_boundary"]
    assert closure["root_closed"] is False and closure["theorem_complete"] is False
    assert closure["first_open_cut_set"] == OPEN_ROOT_CUT
    root = next(node for node in graphs["nodes"] if node["obligation_id"] == "M0508-ROOT")
    assert {
        "H": root["human_debt"], "M": root["machine_debt"], "R": root["readability_debt"]
    } == ROOT_VECTOR
    local_checked = {
        node["obligation_id"]: node
        for node in graphs["nodes"]
        if node["obligation_id"] in {"M0508-L-COUNT-POS", "M0508-T-ASSEMBLE"}
    }
    assert all(node["evidence_ids"] == [] for node in local_checked.values())
    assert proof_receipt["item_id"] == "S56-M-0508-PROOF"
    assert proof_receipt["accepted"] is False
    assert proof_receipt["accepted_closed_obligation_ids"] == []
    assert proof_receipt["result"]["root_kernel_closed"] is False
    assert proof_receipt["remaining_root_cut_set"] == OPEN_ROOT_CUT
    assert proof_blocker["root_closed"] is False
    assert proof_blocker["theorem_complete"] is False

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by|extern)\b|"
        r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
        r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
        r"(?:axiom|constant|opaque|unsafe)\b",
        flags=re.MULTILINE,
    )
    for name in (
        "Statement.lean", "AnchorAudit.lean", "ObligationTree.lean",
        "Proof.lean", "Validation.lean",
    ):
        assert prohibited.search(code_without_comments((HERE / name).read_text())) is None, name
    validation_source = code_without_comments((HERE / "Validation.lean").read_text())
    assert "theorem rootFromEventualPositiveCount" in validation_source
    assert "(positive : ObligationTree.EventualPositiveRepresentationCount)" in validation_source
    assert "theorem vinogradovThreePrimesTarget_proof" not in validation_source

    manifest = load(LEAN_ROOT / "lake-manifest.json")
    mathlib_entry = next(row for row in manifest["packages"] if row["name"] == "mathlib")
    assert mathlib_entry["rev"] == mathlib_entry["inputRev"] == MATHLIB_REVISION
    assert (LEAN_ROOT / ".lake").is_symlink(), "automation-provided canonical .lake symlink missing"
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
        if not relative.startswith("Mathlib/Util/"):
            assert prohibited.search(code_without_comments(source.read_text())) is None

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
    proof_declarations = (
        "Stage1Instances.THM_M_0508.Proof.vinogradovThreePrimesTarget_iff_eventualPositiveRepresentationCount",
        "Stage1Instances.THM_M_0508.Proof.vinogradovThreePrimesTarget_of_eventualPositiveRepresentationCount",
    )
    for declaration in proof_declarations:
        assert printed_axioms(outputs["proof"], declaration) == EXPECTED_AXIOMS
        assert printed_axioms(outputs["validation"], declaration) == EXPECTED_AXIOMS
    obligation_declarations = (
        "Stage1Instances.THM_M_0508.ObligationTree.representationCount_pos_iff",
        "Stage1Instances.THM_M_0508.ObligationTree.root_of_eventualPositiveRepresentationCount",
    )
    for declaration in obligation_declarations:
        assert printed_axioms(outputs["obligation_tree"], declaration) == EXPECTED_AXIOMS
        assert printed_axioms(outputs["validation"], declaration) == EXPECTED_AXIOMS
    assert printed_axioms(
        outputs["validation"],
        "Stage1Instances.THM_M_0508.Validation.rootFromEventualPositiveCount",
    ) == EXPECTED_AXIOMS
    assert outputs["proof"].count("Declarations are sorry-free!") == 2
    assert outputs["validation"].count("Declarations are sorry-free!") == 1
    combined = "\n".join(outputs.values())
    assert "sorryAx" not in combined and "declaration uses 'sorry'" not in combined
    assert all("error:" not in output for output in outputs.values())
    closure_match = re.search(
        r"VALIDATION_CLOSURE roots=(\d+) declarations=(\d+) modules=(\d+)",
        outputs["validation"],
    )
    assert closure_match is not None and int(closure_match.group(1)) == 5
    assert "VALIDATION_CLOSURE axioms=[propext, Classical.choice, Quot.sound]" in outputs["validation"]
    assert "VALIDATION_CLOSURE bodyless_nonaxioms=[]" in outputs["validation"]
    assert "VALIDATION_CLOSURE unsafe=[]" in outputs["validation"]
    observation = {
        "lean_output_sha256": {
            name: hashlib.sha256(output.encode()).hexdigest()
            for name, output in outputs.items()
        },
        "closure": {
            "roots": 5,
            "declarations": int(closure_match.group(2)),
            "modules": int(closure_match.group(3)),
            "axioms": sorted(EXPECTED_AXIOMS),
            "bodyless_nonaxioms": [],
            "unsafe_declarations": [],
        },
    }
    if args.probe:
        print(json.dumps(observation, sort_keys=True))
        return

    spec = load(HERE / "validation-spec.json")
    receipt = load(HERE / "validation-receipt.json")
    blocker = load(HERE / "validation-blocker.json")
    assert spec["schema_version"] == "stage1-validation-spec/1.0"
    assert spec["item_id"] == receipt["item_id"] == blocker["item_id"] == ITEM
    assert spec["theorem_id"] == receipt["theorem_id"] == blocker["theorem_id"] == THEOREM
    assert spec["depends_on"] == receipt["depends_on"] == ["S56-M-0508-PROOF"]
    assert len(spec["recipes"]) == 1
    recipe = spec["recipes"][0]
    assert recipe["cwd"] == "."
    assert recipe["argv"] == [
        "/usr/bin/python3", "-I", "-B",
        f"Stage1_Instances/{THEOREM}/check_validation.py",
        "--worker-packet", ".stage1-worker-selftest.json",
    ]
    assert recipe["network_policy"] == "denied" and recipe["expected_exit"] == 0
    assert receipt["recipe"] == recipe
    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["phase"] == "validation" and receipt["intent"] == "validate"
    assert receipt["verdict"] == "blocked"
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["release_grade"] is False
    assert receipt["accepted_receipt_ids"] == []
    assert receipt["root_vector_before"] == receipt["root_vector_after"] == ROOT_VECTOR
    assert receipt["target"]["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert receipt["target"]["registry_denominator_sha256"] == DENOMINATOR_SHA256
    for name, expected in EXPECTED_INPUTS.items():
        assert receipt["inputs"][name] == expected, name
    for name in ("Validation.lean", "check_validation.py", "validation-spec.json"):
        assert receipt["inputs"][name] == sha256(HERE / name), name
    assert receipt["environment"]["platform"] == (
        f"{platform.system()} {platform.release()} {platform.machine()}"
    )
    assert receipt["environment"]["lean_executable_sha256"] == sha256(lean)
    assert receipt["environment"]["lake_executable_sha256"] == sha256(lake)
    assert receipt["environment"]["mathlib_revision"] == MATHLIB_REVISION
    assert receipt["environment"]["mathlib_tree"] == MATHLIB_TREE
    assert receipt["result"]["lean_output_sha256"] == observation["lean_output_sha256"]
    summary_stdout = "\n".join(SUMMARY_LINES) + "\n"
    assert receipt["result"]["stdout_semantic_sha256"] == hashlib.sha256(
        summary_stdout.encode()
    ).hexdigest()
    assert receipt["result"]["trust_closure_observation"] == observation["closure"]
    assert receipt["result"]["proof_dependency_master_acceptance"] == "fail_closed"
    assert receipt["result"]["root_kernel_closed"] is False
    assert receipt["result"]["accepted_closed_obligation_ids"] == []
    assert receipt["result"]["open_root_cut_set"] == OPEN_ROOT_CUT
    assert receipt["result"]["predecessor_validation_specs_gate"] == "fail_closed"
    assert receipt["result"]["complete_trust_provenance_gate"] == "fail_closed"
    assert receipt["result"]["hermetic_release_gate"] == "fail_closed"
    assert receipt["result"]["independent_distinct_runner_gate"] == "fail_closed"
    assert receipt["result"]["audit_complete"] is receipt["result"]["theorem_complete"] is False
    assert receipt["remaining_root_cut_set"] == OPEN_ROOT_CUT
    assert receipt["first_failed_gate"] == "dependency.S56-M-0508-PROOF.master_acceptance"
    assert blocker["first_failed_gate"] == receipt["first_failed_gate"]
    assert blocker["root_kernel_closed"] is blocker["theorem_complete"] is False
    assert receipt["changed_paths"] == blocker["changed_paths"] == CHANGED_PATHS

    if args.worker_packet is not None:
        packet = load(args.worker_packet.resolve())
        assert set(packet) == {
            "item_id", "changed_paths", "commands", "output_summary",
            "base_revision", "known_failures", "state",
        }
        assert packet["item_id"] == ITEM and packet["state"] == "[_]"
        assert packet["base_revision"] == BASE_REVISION
        assert packet["changed_paths"] == CHANGED_PATHS
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
