#!/usr/bin/env python3
"""Fail-closed narrow validator for S56-M-0318-VALIDATION."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import re
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0318"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
ITEM = "S56-M-0318-VALIDATION"
THEOREM = "THM-M-0318"
BASE_REVISION = "443b8bbc23bf35a1e7a4bb7b3183073f76bbee2b"
BASE_TREE = "c5771c47c12b80aba613e6d844570f83b39ded6d"
TOOLCHAIN = "leanprover/lean4:v4.29.0"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
LEAN_SHA256 = "3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf"
LAKE_SHA256 = "a608ff084d7e2af228b92a29d7c2fd083ba0580e46889175ec74a81678c98359"
BWRAP_SHA256 = "0abea81db798ebf6b4742ac0664802d97521547a353c2a0dbdc21d76cbbfd2c0"
PYTHON_SHA256 = "b8d8288faefdd300201f43fcf00f6f539a27218eeed3a3dff5ab10b9c4c99700"
GIT_SHA256 = "5516c9f362c29376ab9a499a33082f9f611941d8c75930c880e30ad109e39c9a"
ELAN_LAUNCHER_SHA256 = "840179e70803ef373c2ec53342d6a45ea7d022533e4145489fc1278b4f716385"
TOOLCHAIN_SHA256 = "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2"
MANIFEST_SHA256 = "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81"
BLUEPRINT_SHA256 = "c09f9f713bdbc820559e41e1e1840423d60cc2af666aeaf5f3c88587de77f161"
EXECUTION_DAG_SHA256 = "0bb2f433832fe71156aa46c0828102ec3fb61a00dec81fae129c2826a59f63ca"
TARGET_MANIFEST_SHA256 = "02eec284de534dd78e1cf75f82a477ff477567dd682b7445cb7587abd137ab2c"
SKILL_SHA256 = "26d47a66c6535feabb8bbf1051fd55d76a53fe761f4b3d953f86b97ec86152b8"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MATHLIB_REMOTE = "https://github.com/leanprover-community/mathlib4.git"
MATHLIB_LICENSE_SHA256 = "b40930bbcf80744c86c46a12bc9da056641d722716c378f5659b9e555ef833e1"
TARGET_EXPRESSION_SHA256 = (
    "2605ac76f3d50dddcc135d3094639fbed3de58a10b26a8f9eeb504101e556b5f"
)
INVENTORY_SHA256 = (
    "57d77a8fccc8308a704f1185c92057a17791da515e45325179aa81d000376f87"
)
UPSTREAM_REVISION = "c02205edf347ad45f0d62db85497598ba2c4291e"
UPSTREAM_TREE = "5dda2d10fdd4a0db1aba85f1fa1a7acc509f80e4"
UPSTREAM_ARCHIVE_SHA256 = (
    "8591fadd6737d75b921eee27dc9d85d5d9f040a83ad7dcb2d81dc208754c04cd"
)
COMPATIBILITY_PATCH_SHA256 = (
    "39fff43f92e646d6365f6279fd565d0d2d7b873f0922a1df9165f880a36b8790"
)
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
ROOT_VECTOR = {"H": "H2", "M": "M3", "R": "R4"}
FROZEN_OPEN_CUT = [
    "THM-M-0318-C-NET",
    "THM-M-0318-C-MAP",
    "THM-M-0318-B-BROUWER",
    "THM-M-0318-L-LIMIT",
    "THM-M-0318-L-CONT",
]
PROOF_OBLIGATION_IDS = [
    "M0318-ROOT",
    "M0318-C",
    "M0318-C-NET",
    "M0318-C-MAP",
    "M0318-B-BROUWER",
    "M0318-L-APPROX",
    "M0318-L-LIMIT",
    "M0318-L-CONT",
    "M0318-T-COMPOSE",
]
EXPECTED_INPUTS = {
    "Statement.lean": "e428904e22f39e9dd3b2283c1155ade8c1df09b40d1a15052e3dd4ca71b2912d",
    "ObligationTree.lean": "623fa1763a74dc4c88bb72617d27a8173b3642cb450a019aeba88a8b41946fd7",
    "Proof.lean": "c8dfef2073737c4a71c0b3866de79fc2ff1276c82ae17c7f809e5fce0eca5602",
    "statement.json": "3747826c9a83a687ecbfaff3b8580124b4e8ee37e53b1647582eb08ff9b8a467",
    "instance.json": "2b568fdf6949c4ddf79c08c41df406e34fb2d48ebff4efd7668972b3f7bdc401",
    "task-dag.json": "c8039a55c6c1e3a5c9eac3d50672add2c7059e1591af3978d614a77903b054f1",
    "anchor-audit.json": "3725b4d6e29d267a8a4f9aac33f7fb368df023c297f6888b2113f7c68b1d4a7b",
    "obligation-registry.json": "d4c5634e3dbb15243dfe056f870d9901119785af7220cabc964c8ca4c783a4d6",
    "typed-graphs.json": "f7357052495d200f51c736329c66f153ed25e859ff511811fda808dd665ea9d1",
    "proof-receipt.json": "fbea33158e266f23b698be1664d0296db436310f9f7c4bdf5b0fb28b6b43c0d4",
    "vendor-manifest.json": "8735e7a3a1a17e47dff4b0e2ded4c358d7d8f28ba959cab48677c3dfe473283a",
    "VENDOR_PROVENANCE.md": "0e802682cd69bbca3e2e7c281e0d95836e065757836a096694ab77cef2e74995",
    "build_vendor_manifest.py": "b782c11a88d648482d45233186b6ea6b5b293d780bb60a4626925f8281c540f3",
    "Validation.lean": "f4f7dfebc40776d7114bf28ff2391bfd19721cadffb095b71549cc474d0bc621",
}
TRUST_SOURCE_BOUNDARIES = {
    "Mathlib/Util/AssertNoSorry.lean": {
        "blob": "060d8a764d2a6d1d2963d9c500b6084a05bed534",
        "source_sha256": "aa9f7bebacafc688c894ef2171930e51ed19e0dfe722581848a2414d28900d4d",
        "olean_sha256": "c8bf37753d9bad47b9fe67e32436da8b9af516a4abbbe14e74726f01ba2fb30b",
        "olean_bytes": 51336,
    },
    "Mathlib/Util/PrintSorries.lean": {
        "blob": "24d72cc680fa8b07f0d1062f670a5a824934a227",
        "source_sha256": "03670b0b0007740e5390dadd49c3d10a02b7d0919092d2b3214ef8a6a8cf798f",
        "olean_sha256": "9bcc4076e0aee5febb2eea5cf9dc959f38526e9f974afdfdd8658bfd318d5bb7",
        "olean_bytes": 314480,
    },
}
PROOF_DECLARATIONS = (
    "IndexedLOrder.Scarf",
    "IndexedLOrder.GiComponentStructure_holds",
    "Brouwer",
    "Stage1Instances.THM_M_0318.exists_simplex_approximation",
    "Stage1Instances.THM_M_0318.hasApproximateFixedPoints",
    "Stage1Instances.THM_M_0318.approximationEngine",
    "Stage1Instances.THM_M_0318.compactLimitEngine",
    "Stage1Instances.THM_M_0318.exactSchauderTarget",
    "Stage1Instances.THM_M_0318.schauderFixedPoint",
)
VALIDATION_DECLARATIONS = (
    "IndexedLOrder.Scarf",
    "IndexedLOrder.GiComponentStructure_holds",
    "Brouwer",
    "Stage1Instances.THM_M_0318.Validation.validationSimplexApproximation",
    "Stage1Instances.THM_M_0318.Validation.schauderFixedPoint_validation",
)
CHANGED_PATHS = [
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/Validation.lean",
    f"Stage1_Instances/{THEOREM}/check_validation.py",
    f"Stage1_Instances/{THEOREM}/validation-phase.md",
    f"Stage1_Instances/{THEOREM}/validation-receipt.json",
    f"Stage1_Instances/{THEOREM}/validation-spec.json",
]
SUMMARY_LINES = [
    "PASS kernel: exact statement, frozen composition, vendored closure, proof root, and no-import differential root replayed at trust zero",
    "PASS trust observation: fourteen reports are sorry-free and each axiom closure is exactly propext, Classical.choice, and Quot.sound",
    "PASS selected provenance: current source hashes, reversible vendor port, immutable upstream identities, tools, license, and clean mathlib pin agree",
    "FAIL CLOSED authority: proof is provisional and frozen graph/task records predate it; accepted root remains H2/M3/R4",
    "FAIL CLOSED complete trust/provenance: accepted foundation policy and full transitive declaration, compiled-artifact, TCB, and SBOM closure are absent",
    "FAIL CLOSED hermetic/independent: shared warm cache and same-worker parallel source replay are not a cold build or distinct signed verifier",
    "audit_complete=false; theorem_complete=false",
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

    value = json.loads(
        path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicates
    )
    assert isinstance(value, dict), path
    return value


def run(
    argv: list[str], *, cwd: Path = ROOT, env: dict[str, str] | None = None,
    timeout: int = 900,
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
    return run(["/usr/bin/git", *args], cwd=cwd, env=BASE_ENV).strip()


def strip_lean_comments_and_strings(source: str) -> str:
    output: list[str] = []
    index = 0
    block_depth = 0
    in_string = False
    escaped = False
    while index < len(source):
        pair = source[index:index + 2]
        char = source[index]
        if block_depth:
            if pair == "/-":
                block_depth += 1
                output.extend("  ")
                index += 2
            elif pair == "-/":
                block_depth -= 1
                output.extend("  ")
                index += 2
            else:
                output.append("\n" if char == "\n" else " ")
                index += 1
        elif in_string:
            output.append("\n" if char == "\n" else " ")
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
            index += 1
        elif pair == "/-":
            block_depth = 1
            output.extend("  ")
            index += 2
        elif pair == "--":
            newline = source.find("\n", index)
            if newline < 0:
                output.extend(" " * (len(source) - index))
                index = len(source)
            else:
                output.extend(" " * (newline - index))
                index = newline
        elif char == '"':
            in_string = True
            output.append(" ")
            index += 1
        else:
            output.append(char)
            index += 1
    assert block_depth == 0 and not in_string
    return "".join(output)


def reported_axioms(output: str, declaration: str) -> set[str]:
    match = re.search(
        re.escape(f"'{declaration}' depends on axioms: [") + r"(.*?)]",
        output,
        re.DOTALL,
    )
    if match:
        return {part.strip() for part in match.group(1).split(",") if part.strip()}
    assert f"'{declaration}' does not depend on any axioms" in output, declaration
    return set()


def assert_text_hygiene(path: Path) -> None:
    data = path.read_bytes()
    assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())


HOME = os.environ["HOME"]
BASE_ENV = {
    "HOME": HOME,
    "PATH": f"{HOME}/.elan/bin:/usr/bin:/bin",
    "ELAN_TOOLCHAIN": TOOLCHAIN,
    "LANG": "C.UTF-8",
    "LC_ALL": "C.UTF-8",
    "TZ": "UTC",
    "LEAN_NUM_THREADS": "1",
}


def pinned_lean_path(lean: Path) -> str:
    packages = (
        "batteries", "Qq", "aesop", "proofwidgets", "importGraph",
        "LeanSearchClient", "plausible", "mathlib",
    )
    roots = [
        (LEAN_ROOT / ".lake/packages" / package / ".lake/build/lib/lean").resolve()
        for package in packages
    ]
    assert all(path.is_dir() for path in roots)
    local = (LEAN_ROOT / ".lake/build/lib/lean").resolve()
    assert local.is_dir()
    return ":".join(
        [*(str(path) for path in roots), str(local), str(lean.parent.parent / "lib/lean")]
    )


def isolated_replay(lean: Path, bwrap: Path, lean_path: str) -> dict[str, str]:
    with tempfile.TemporaryDirectory(prefix="stage1-m0318-validation-", dir="/tmp") as name:
        tmp = Path(name).resolve()
        target = tmp / "Stage1_Instances" / THEOREM
        vendor = target / "Vendor"
        target.mkdir(parents=True)
        for filename in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
            (target / filename).write_bytes((HERE / filename).read_bytes())
        for source in (HERE / "Vendor").rglob("*"):
            if source.is_file():
                destination = vendor / source.relative_to(HERE / "Vendor")
                destination.parent.mkdir(parents=True, exist_ok=True)
                destination.write_bytes(source.read_bytes())
        (tmp / "home").mkdir()
        base = [
            str(bwrap), "--ro-bind", "/", "/", "--bind", str(tmp), str(tmp),
            "--dev", "/dev", "--proc", "/proc", "--unshare-net", "--die-with-parent",
            "--clearenv", "--setenv", "HOME", str(tmp / "home"),
            "--setenv", "TMPDIR", str(tmp), "--setenv", "LANG", "C.UTF-8",
            "--setenv", "LC_ALL", "C.UTF-8", "--setenv", "TZ", "UTC",
            "--setenv", "LEAN_NUM_THREADS", "1", "--chdir", str(tmp),
        ]

        def lean_run(
            source: Path, module_path: str, root: Path, emit_olean: bool
        ) -> str:
            argv = base + [
                "--setenv", "LEAN_PATH", module_path, str(lean), "--trust=0",
                "-t0", "-R", str(root),
            ]
            if emit_olean:
                argv += ["-o", str(source.with_suffix(".olean"))]
            argv.append(str(source))
            return run(argv, env=BASE_ENV)

        statement = lean_run(target / "Statement.lean", lean_path, target, True)
        tree = lean_run(
            target / "ObligationTree.lean", f"{target}:{lean_path}", target, True
        )
        vendor_outputs: list[str] = []
        for module in ("Gametheory.Scarf", "Gametheory.ScarfPath", "Gametheory.Brouwer"):
            source = vendor / Path(*module.split(".")).with_suffix(".lean")
            vendor_outputs.append(
                lean_run(source, f"{vendor}:{lean_path}", vendor, True)
            )
        proof = lean_run(
            target / "Proof.lean", f"{target}:{vendor}:{lean_path}", target, True
        )
        validation = lean_run(
            target / "Validation.lean", f"{target}:{vendor}:{lean_path}", target, False
        )
        return {
            "statement": statement,
            "tree": tree,
            "vendor": "".join(vendor_outputs),
            "proof": proof,
            "validation": validation,
        }


def assert_network_isolation(bwrap: Path) -> None:
    probe = subprocess.run(
        [
            str(bwrap), "--ro-bind", "/", "/", "--dev", "/dev", "--proc", "/proc",
            "--unshare-net", "--die-with-parent", "/usr/bin/python3", "-I", "-c",
            "import socket; s=socket.socket(); s.settimeout(0.2); "
            "s.connect(('1.1.1.1', 53))",
        ],
        env=BASE_ENV,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=10,
        check=False,
    )
    assert probe.returncode != 0, "network-denial mutation unexpectedly connected"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--probe", action="store_true")
    args = parser.parse_args()

    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    targets = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    statement = load(HERE / "statement.json")
    instance = load(HERE / "instance.json")
    task_dag = load(HERE / "task-dag.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    proof_receipt = load(HERE / "proof-receipt.json")
    vendor_manifest = load(HERE / "vendor-manifest.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    assert sha256(ROOT / "Docs/Stage1_Blueprint_rev-5.6.md") == BLUEPRINT_SHA256
    assert sha256(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json") == EXECUTION_DAG_SHA256
    assert sha256(ROOT / "Docs/Stage1_Targets_rev-5.6.json") == TARGET_MANIFEST_SHA256
    assert sha256(ROOT / "skills/execute-stage1-rev56/SKILL.md") == SKILL_SHA256
    target_row = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target_row["execution_rank"] == 684 and target_row["baseline"] == "L0"
    assert target_row["rework_required"] is True and target_row["theorem_complete"] is False
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item == {
        "id": ITEM, "theorem_id": THEOREM, "execution_rank": 684,
        "phase": "validation", "layer": 5, "state": "[ ]",
        "depends_on": ["S56-M-0318-PROOF"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Run hermetic kernel, trust, provenance, and independent validation gates.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0, "children": [],
    }
    predecessor = next(row for row in execution["items"] if row["id"] == "S56-M-0318-PROOF")
    assert predecessor["state"] == "[_]" and predecessor["attempts"] == 1
    assert instance["root_vector"] == ROOT_VECTOR
    assert instance["accepted_proof_state"] == []
    assert instance["audit_complete"] is instance["theorem_complete"] is False

    for filename, expected in EXPECTED_INPUTS.items():
        assert sha256(HERE / filename) == expected, f"stale validation input: {filename}"
    assert sha256(LEAN_ROOT / "lean-toolchain") == TOOLCHAIN_SHA256
    assert sha256(LEAN_ROOT / "lake-manifest.json") == MANIFEST_SHA256
    assert statement["canonical_formal_target"]["elaborated_expression_sha256"] == (
        TARGET_EXPRESSION_SHA256
    )
    assert registry["root_obligation_id"] == "M0318-ROOT"
    assert registry["frozen_denominators"]["inventory_sha256"] == INVENTORY_SHA256
    assert graphs["root_reachability"]["open_cut_set"] == FROZEN_OPEN_CUT
    assert graphs["theorem_complete"] is registry["theorem_complete"] is False
    assert task_dag["accepted_states"] == []
    assert next(row for row in task_dag["tasks"] if row["id"].endswith("-PROOF"))[
        "state"
    ] == "open"
    assert proof_receipt["canonical_target_expression_sha256"] == TARGET_EXPRESSION_SHA256
    assert proof_receipt["registry_inventory_sha256"] == INVENTORY_SHA256
    assert proof_receipt["proof_body"]["source_sha256"] == EXPECTED_INPUTS["Proof.lean"]
    assert proof_receipt["accepted"] is False
    assert proof_receipt["result"]["root_kernel_inhabitant_observed"] is True
    assert proof_receipt["result"]["accepted_root_closed"] is False
    assert proof_receipt["accepted_closed_obligation_ids"] == []
    assert proof_receipt["covered_obligation_ids"] == PROOF_OBLIGATION_IDS

    assert vendor_manifest["upstream"]["revision"] == UPSTREAM_REVISION
    assert vendor_manifest["upstream"]["source_tree"] == UPSTREAM_TREE
    assert vendor_manifest["upstream"]["source_archive_sha256"] == UPSTREAM_ARCHIVE_SHA256
    assert vendor_manifest["closure"]["normalized_compatibility_patch_sha256"] == (
        COMPATIBILITY_PATCH_SHA256
    )
    assert vendor_manifest["license"]["sha256"] == sha256(HERE / "Vendor/LICENSE")
    vendor_sources = {
        path.relative_to(HERE / "Vendor").as_posix()
        for path in (HERE / "Vendor").rglob("*.lean")
    }
    assert vendor_sources == {row["path"] for row in vendor_manifest["files"]}
    for row in vendor_manifest["files"]:
        source = HERE / "Vendor" / row["path"]
        assert sha256(source) == row["vendored_sha256"]
        assert source.stat().st_size == row["vendored_bytes"]
    vendor_check = run(
        ["/usr/bin/python3", "-I", "-B", str(HERE / "build_vendor_manifest.py")],
        env=BASE_ENV,
    )
    assert vendor_check.startswith("PASS THM-M-0318 vendor closure:")

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by)\b|"
        r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
        r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
        r"(?:axiom|constant|opaque|unsafe|extern)\b",
        re.MULTILINE,
    )
    scanned = [
        HERE / name
        for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean")
    ] + sorted((HERE / "Vendor").rglob("*.lean"))
    for path in scanned:
        source = strip_lean_comments_and_strings(path.read_text(encoding="utf-8"))
        match = prohibited.search(source)
        assert match is None, (path, match.group(0) if match else None)
    validation_source = (HERE / "Validation.lean").read_text(encoding="utf-8")
    assert "import Proof" not in validation_source
    assert "import ObligationTree" not in validation_source
    assert "theorem schauderFixedPoint_validation : SchauderFixedPointTarget.{u}" in (
        validation_source
    )

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
    for relative, expected in TRUST_SOURCE_BOUNDARIES.items():
        source = mathlib / relative
        olean = mathlib / ".lake/build/lib/lean" / Path(relative).with_suffix(".olean")
        assert git("rev-parse", f"HEAD:{relative}", cwd=mathlib) == expected["blob"]
        assert sha256(source) == expected["source_sha256"]
        assert sha256(olean) == expected["olean_sha256"]
        assert olean.stat().st_size == expected["olean_bytes"]

    launcher = Path(HOME) / ".elan/bin/lake"
    assert sha256(launcher) == ELAN_LAUNCHER_SHA256
    toolchain_root = (
        Path(HOME) / ".elan/toolchains/leanprover--lean4---v4.29.0"
    )
    lean = toolchain_root / "bin/lean"
    lake = toolchain_root / "bin/lake"
    bwrap = Path("/usr/bin/bwrap")
    python = Path("/usr/bin/python3").resolve()
    git_executable = Path("/usr/bin/git")
    assert sha256(lean) == LEAN_SHA256 and sha256(lake) == LAKE_SHA256
    assert sha256(bwrap) == BWRAP_SHA256 and sha256(python) == PYTHON_SHA256
    assert sha256(git_executable) == GIT_SHA256
    assert LEAN_COMMIT in run([str(lean), "--version"], env=BASE_ENV)
    assert_network_isolation(bwrap)

    outputs = isolated_replay(lean, bwrap, pinned_lean_path(lean))
    combined = "\n".join(outputs.values())
    assert "sorryAx" not in combined and "error:" not in combined.lower()
    assert outputs["proof"].count("Declarations are sorry-free!") == len(
        PROOF_DECLARATIONS
    )
    assert outputs["validation"].count("Declarations are sorry-free!") == len(
        VALIDATION_DECLARATIONS
    )
    for declaration in PROOF_DECLARATIONS:
        assert reported_axioms(outputs["proof"], declaration) == EXPECTED_AXIOMS
    for declaration in VALIDATION_DECLARATIONS:
        assert reported_axioms(outputs["validation"], declaration) == EXPECTED_AXIOMS
    observation = {
        "lean_output_sha256": {
            name: hashlib.sha256(output.encode()).hexdigest()
            for name, output in outputs.items()
        },
        "observed_axioms": sorted(EXPECTED_AXIOMS),
        "proof_sorry_free_reports": len(PROOF_DECLARATIONS),
        "validation_sorry_free_reports": len(VALIDATION_DECLARATIONS),
        "vendor_manifest_output_sha256": hashlib.sha256(
            vendor_check.encode()
        ).hexdigest(),
    }
    if args.probe:
        print(json.dumps(observation, sort_keys=True))
        return

    spec = load(HERE / "validation-spec.json")
    receipt = load(HERE / "validation-receipt.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")
    assert spec["schema_version"] == "stage1-validation-spec/1.0"
    assert spec["item_id"] == receipt["item_id"] == packet["item_id"] == ITEM
    assert spec["theorem_id"] == receipt["theorem_id"] == THEOREM
    assert spec["depends_on"] == receipt["depends_on"] == ["S56-M-0318-PROOF"]
    assert len(spec["recipes"]) == 1 and spec["recipes"][0] == receipt["recipe"]
    recipe = spec["recipes"][0]
    assert recipe["argv"] == [
        "python3", "-I", "-B", f"Stage1_Instances/{THEOREM}/check_validation.py"
    ]
    assert recipe["network_policy"] == "denied" and recipe["expected_exit"] == 0
    assert "bubblewrap" in recipe["network_enforcement"].lower()
    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["phase"] == "validation" and receipt["intent"] == "validate"
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == packet["state"] == "[_]"
    assert receipt["accepted"] is receipt["release_grade"] is False
    assert receipt["verdict"] == "blocked"
    assert receipt["root_vector_before"] == receipt["root_vector_after"] == ROOT_VECTOR
    assert receipt["accepted_receipt_ids"] == []
    assert receipt["accepted_closed_obligation_ids"] == []
    repository = receipt["repository_state"]
    assert repository["release_clean"] is False
    assert repository["tracked_patch_sha256"] == hashlib.sha256(b"").hexdigest()
    assert repository["tracked_patch_bytes"] == 0
    unhashed_inputs = [
        f"Stage1_Instances/{THEOREM}/Validation.lean",
        f"Stage1_Instances/{THEOREM}/check_validation.py",
        f"Stage1_Instances/{THEOREM}/validation-phase.md",
        f"Stage1_Instances/{THEOREM}/validation-spec.json",
    ]
    payload = [
        {"path": relative, "sha256": sha256(ROOT / relative)}
        for relative in unhashed_inputs
    ]
    assert repository["untracked_input_scope"] == unhashed_inputs
    assert repository["untracked_input_sha256"] == {
        row["path"]: row["sha256"] for row in payload
    }
    assert repository["untracked_input_bundle_sha256"] == hashlib.sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    assert repository["preexisting_lake_symlink_target_sha256"] == hashlib.sha256(
        os.readlink(LEAN_ROOT / ".lake").encode()
    ).hexdigest()
    assert receipt["target"] == {
        "declaration": "Stage1Instances.THM_M_0318.SchauderFixedPointTarget",
        "elaborated_expression_sha256": TARGET_EXPRESSION_SHA256,
        "statement_source_sha256": EXPECTED_INPUTS["Statement.lean"],
        "registry_inventory_sha256": INVENTORY_SHA256,
        "exact_statement_delta": "none",
    }
    for name, expected in EXPECTED_INPUTS.items():
        assert receipt["inputs"][name] == expected
    for name, expected in {
        "lean-toolchain": TOOLCHAIN_SHA256,
        "lake-manifest.json": MANIFEST_SHA256,
        "Stage1_Blueprint_rev-5.6.md": BLUEPRINT_SHA256,
        "Stage1_Execution_DAG_rev-5.6.json": EXECUTION_DAG_SHA256,
        "Stage1_Targets_rev-5.6.json": TARGET_MANIFEST_SHA256,
        "execute-stage1-rev56/SKILL.md": SKILL_SHA256,
    }.items():
        assert receipt["inputs"][name] == expected
    assert receipt["inputs"]["check_validation.py"] == sha256(HERE / "check_validation.py")
    assert receipt["inputs"]["validation-spec.json"] == sha256(HERE / "validation-spec.json")
    environment = receipt["environment"]
    assert environment["platform"] == (
        f"{platform.system()} {platform.release()} {platform.machine()}"
    )
    assert environment["lean_executable_sha256"] == sha256(lean)
    assert environment["lake_executable_sha256"] == sha256(lake)
    assert environment["python_executable_sha256"] == sha256(python)
    assert environment["git_executable_sha256"] == sha256(git_executable)
    assert environment["bubblewrap_executable_sha256"] == sha256(bwrap)
    assert environment["mathlib_revision"] == MATHLIB_REVISION
    assert environment["mathlib_tree"] == MATHLIB_TREE
    assert environment["mathlib_worktree_clean"] is True
    assert receipt["provenance"]["complete_provenance_gate"] == "fail_closed"
    assert receipt["trust"]["accepted_foundation_policy"] is False
    assert receipt["trust"]["complete_transitive_tcb_inventory"] is False
    assert receipt["hermeticity"]["decision"].startswith("fail_closed")
    assert receipt["independent_validation"]["decision"] == "fail_closed"
    assert receipt["result"]["lean_output_sha256"] == observation["lean_output_sha256"]
    assert receipt["result"]["observed_axioms"] == observation["observed_axioms"]
    assert receipt["result"]["proof_sorry_free_reports"] == len(PROOF_DECLARATIONS)
    assert receipt["result"]["validation_sorry_free_reports"] == len(
        VALIDATION_DECLARATIONS
    )
    assert receipt["result"]["vendor_manifest_output_sha256"] == (
        observation["vendor_manifest_output_sha256"]
    )
    assert receipt["result"]["exact_root_kernel_replay"] == "pass_provisional_nonrelease"
    assert receipt["result"]["accepted_closed_obligation_ids"] == []
    assert receipt["result"]["accepted_root_machine_debt"] == "M3"
    assert receipt["result"]["hermetic_release_gate"] == "fail_closed"
    assert receipt["result"]["independent_distinct_runner_gate"] == "fail_closed"
    assert receipt["result"]["audit_complete"] is receipt["result"]["theorem_complete"] is False
    assert receipt["first_failed_gate"] == "dependency.S56-M-0318-PROOF.master_acceptance"
    assert receipt["remaining_root_cut_set"] == FROZEN_OPEN_CUT
    assert receipt["output_summary"] == ["PASS THM-M-0318 narrow validation", *SUMMARY_LINES]
    assert set(receipt["changed_paths"]) == set(CHANGED_PATHS)
    assert set(packet["changed_paths"]) == set(CHANGED_PATHS)
    assert packet["base_revision"] == BASE_REVISION
    assert packet["known_failures"] == receipt["known_failures"]
    status = git("status", "--short", "--untracked-files=all").splitlines()
    actual = {line[3:] for line in status if line[3:] != "Formalizations/Lean/.lake"}
    assert actual == set(CHANGED_PATHS), (actual, CHANGED_PATHS)
    for relative in CHANGED_PATHS:
        assert_text_hygiene(ROOT / relative)

    print("PASS THM-M-0318 narrow validation")
    for line in SUMMARY_LINES:
        print(line)


if __name__ == "__main__":
    main()
