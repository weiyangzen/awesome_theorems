#!/usr/bin/env python3
"""Fail-closed narrow validator for S56-M-0319-VALIDATION."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
from datetime import datetime, timezone


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0319"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
ITEM = "S56-M-0319-VALIDATION"
THEOREM = "THM-M-0319"
BASE_REVISION = "8d6ac2078d37dc107d80c38c020de01c6f9affce"
BASE_TREE = "a9332226f35fa562b7dbbe9feab5f5a2da80d013"
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
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MATHLIB_REMOTE = "https://github.com/leanprover-community/mathlib4.git"
MATHLIB_LICENSE_SHA256 = "b40930bbcf80744c86c46a12bc9da056641d722716c378f5659b9e555ef833e1"
EXPRESSION_SHA256 = "2e4dc02230de7a1c08fdf4a19ef0ec1da107297972dee0e85d893bdb33d6a514"
DENOMINATOR_SHA256 = "9d15b5eafa794b7f3cc1e83d4006447c90a75f8d8175bbaeb4b50fe8306ccee8"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
ROOT_VECTOR = {"H": "H1", "M": "M4", "R": "R4"}
FROZEN_OPEN_CUT = ["M0319-T-EXTERNAL"]
EXPECTED_INPUTS = {
    "Statement.lean": "1b2804bde5a77937dc470ccf1f6e54856d98b86e268b5dc30fe19f0a84bc440a",
    "ObligationTree.lean": "e80086143cdf2bf3b2e5ab42da94217dffddd062dd157609b6565c8a8de67cbd",
    "Proof.lean": "793e81e88075d53b3a1a11226808a12bf910bf89f4323ecee701ae125bdd2f38",
    "statement.json": "fecb49cb5ce1392bd29c3eef365c55a003dca217b9dab415bab2ad9cb8e3e1ca",
    "anchor-audit.json": "747de378a621b873e2eb5f96016c6d7429c350e7dbb619d20f1994b6af70f524",
    "obligation-registry.json": "6e0d9d0b3ff8044cd0162c47b3f8aee57ecf4070fcc517b38a1b58011e398d2f",
    "typed-graphs.json": "983c863161c535ecaee625f7b34b1f52dc5852beaa75189eaaf561175a644428",
    "proof-receipt.json": "3330f95b90aa4a2dd09187d4326bfeda1f2b671e6e6462c1e939b4d77982df90",
    "proof-blocker.json": "191816f73c04567fcdf4b67f6cbf51d876ee668855c881f4685526780562d0cd",
    "source-statement-crosswalk.md": "20694f6cc26c947b18af187bac350f89a57ba03ab97c0c42c980c2f4aaf26abb",
    "vendor-manifest.json": "d344d645fc61ac6a4cc3e8c22dc803bff84312c1ebe25a508469e6ab54f98bc7",
    "VENDOR_PROVENANCE.md": "c6736160e360ea36b3a1be90cd9036716069e56e4b52e9f413ed9d02fdaf8c2f",
    "Vendor/LICENSE": "956bddafa77f8b8ad428bb35cf59424b0ddd0933ebab506037b97a20fab1a5d0",
    "Vendor/Gametheory/Scarf.lean": "210dc01a3b823527ce3c4c079879ee897ef6f7aefb9e9a15406a20eeedcb92a6",
    "Vendor/Gametheory/ScarfPath.lean": "d9e661c3e46e9d0ffcdbed7ca62696d6baed5aa77f5e834002d307b30c86b2bd",
    "Vendor/Gametheory/Brouwer.lean": "8cb62d7ae0820c620e9665a9124e2f07b7b5c20da8455a44a633b1e6e8948110",
    "build_vendor_manifest.py": "0ba2b3b2cdc455542d5e374d53079ba87be68c708dde9f2ec8d0ae6b1e0bb4a4",
    "check_proof.sh": "3b1f4b0708e13445b5b45a07c1209195e16d2b610e29d83bf4d734b6f3a51b67",
    "Validation.lean": "d1323014a1c1d339683d3ac463a18071085163c68b103215504ec8cc222f7187",
}
VENDOR_FILES = {
    "Gametheory/Scarf.lean": ("d296baf07b372b6e734ab00588f0cc3330e64ad297e0e16a2cb05d21310802d2", 111310),
    "Gametheory/ScarfPath.lean": ("49fec577cfaf341ca5febe74cdaa23b767857320a8466b03a9aedb779a422ff1", 34297),
    "Gametheory/Brouwer.lean": ("d9358072002e47e362e46b5416779ed8cae9a635490530e1ae168ee152a3805b", 36756),
}
PROOF_DECLARATIONS = (
    "IndexedLOrder.Scarf",
    "IndexedLOrder.GiComponentStructure_holds",
    "Brouwer",
    "Stage1Instances.THM_M_0319.exists_simplex_approximation",
    "Stage1Instances.THM_M_0319.hasApproximateFixedPoints",
    "Stage1Instances.THM_M_0319.exactFixedPoint",
    "Stage1Instances.THM_M_0319.brouwerFixedPoint",
)
VALIDATION_DECLARATION = "Stage1Instances.THM_M_0319.Validation.recomposedBrouwerFixedPoint"
CHANGED_PATHS = [
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/Validation.lean",
    f"Stage1_Instances/{THEOREM}/check_validation.py",
    f"Stage1_Instances/{THEOREM}/validation-phase.md",
    f"Stage1_Instances/{THEOREM}/validation-receipt.json",
    f"Stage1_Instances/{THEOREM}/validation-spec.json",
]
SUMMARY_LINES = [
    "PASS narrow kernel replay: exact statement, frozen interfaces, three vendored modules, proof bodies, exact root, and differential recomposition elaborated at trust zero",
    "PASS trust observation: eight checked declarations use exactly propext, Classical.choice, and Quot.sound; root closure has no unexpected bodyless or unsafe declaration",
    "PASS selected provenance: frozen local/vendor hashes, reversible upstream reconstruction, MIT license, tool identities, and clean pinned mathlib agree",
    "FAIL CLOSED authority and graph: proof is not master accepted and the frozen Harfe/cube graph does not describe the simplex/partition-of-unity proof route",
    "FAIL CLOSED complete trust/provenance: accepted foundation policy and complete transitive TCB, compiled-artifact, origin, and SBOM closure are absent",
    "FAIL CLOSED hermetic/independent: network-isolated fresh outputs still reuse a warm shared cache and same-worker recomposition is not distinct signed verification",
    "accepted root remains H1/M4/R4; audit_complete=false; theorem_complete=false",
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


def run(argv: list[str], *, cwd: Path = ROOT, env: dict[str, str] | None = None) -> str:
    result = subprocess.run(
        argv, cwd=cwd, env=env, text=True, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, timeout=900, check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(f"command failed ({result.returncode}): {argv!r}\n{result.stdout}")
    return result.stdout


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["/usr/bin/git", *args], cwd=cwd, env=BASE_ENV).strip()


def source_without_comments_or_strings(source: str) -> str:
    output: list[str] = []
    index = depth = 0
    in_string = False
    while index < len(source):
        if depth == 0 and not in_string and source.startswith("--", index):
            newline = source.find("\n", index)
            if newline < 0:
                break
            output.append("\n")
            index = newline + 1
        elif not in_string and source.startswith("/-", index):
            depth += 1
            index += 2
        elif depth and source.startswith("-/", index):
            depth -= 1
            index += 2
        elif depth:
            if source[index] == "\n":
                output.append("\n")
            index += 1
        elif in_string:
            if source[index] == "\\":
                index += 2
            elif source[index] == '"':
                in_string = False
                index += 1
            else:
                if source[index] == "\n":
                    output.append("\n")
                index += 1
        elif source[index] == '"':
            in_string = True
            index += 1
        else:
            output.append(source[index])
            index += 1
    assert depth == 0 and not in_string, "unterminated Lean comment or string"
    return "".join(output)


def reported_axioms(output: str, declaration: str) -> set[str]:
    report = re.search(
        re.escape(f"'{declaration}' depends on axioms: [") + r"(.*?)]",
        output, re.DOTALL,
    )
    if report:
        return {part.strip() for part in report.group(1).split(",") if part.strip()}
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
    package_root = (LEAN_ROOT / ".lake" / "packages").resolve()
    roots = sorted(
        path.resolve() for path in package_root.glob("*/.lake/build/lib/lean")
        if path.is_dir()
    )
    local = (LEAN_ROOT / ".lake/build/lib/lean").resolve()
    assert roots and local.is_dir()
    return ":".join([*(str(path) for path in roots), str(local), str(lean.parent.parent / "lib/lean")])


def isolated_replay(lean: Path, bwrap: Path, lean_path: str, outer_isolated: bool) -> dict[str, str]:
    with tempfile.TemporaryDirectory(prefix="stage1-m0319-validation-", dir="/tmp") as tmp_name:
        tmp = Path(tmp_name).resolve()
        vendor = tmp / "Vendor" / "Gametheory"
        vendor.mkdir(parents=True)
        for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
            (tmp / name).write_bytes((HERE / name).read_bytes())
        for name in ("Scarf.lean", "ScarfPath.lean", "Brouwer.lean"):
            (vendor / name).write_bytes((HERE / "Vendor" / "Gametheory" / name).read_bytes())
        (tmp / "home").mkdir()
        base = [] if outer_isolated else [
            str(bwrap), "--ro-bind", "/", "/", "--bind", str(tmp), str(tmp),
            "--dev", "/dev", "--proc", "/proc", "--unshare-net", "--die-with-parent",
            "--clearenv", "--setenv", "HOME", str(tmp / "home"),
            "--setenv", "TMPDIR", str(tmp), "--setenv", "LANG", "C.UTF-8",
            "--setenv", "LC_ALL", "C.UTF-8", "--setenv", "TZ", "UTC",
            "--setenv", "LEAN_NUM_THREADS", "1", "--chdir", str(tmp),
        ]

        def lean_run(source: Path, module_path: str, output: Path | None) -> str:
            prefix = [] if outer_isolated else ["--setenv", "LEAN_PATH", module_path]
            argv = base + prefix + [str(lean), "--trust=0", "-t0", "-R", str(tmp)]
            if output is not None:
                argv += ["-o", str(output)]
            argv.append(str(source))
            child_env = {
                **BASE_ENV,
                "HOME": str(tmp / "home"),
                "TMPDIR": str(tmp),
                "LEAN_PATH": module_path,
            }
            return run(argv, cwd=tmp, env=child_env)

        outputs: dict[str, str] = {}
        outputs["statement"] = lean_run(tmp / "Statement.lean", lean_path, tmp / "Statement.olean")
        outputs["tree"] = lean_run(tmp / "ObligationTree.lean", lean_path, tmp / "ObligationTree.olean")
        vendor_path = f"{tmp / 'Vendor'}:{lean_path}"
        for stem in ("Scarf", "ScarfPath", "Brouwer"):
            outputs[f"vendor_{stem.lower()}"] = lean_run(
                vendor / f"{stem}.lean", vendor_path, vendor / f"{stem}.olean"
            )
        proof_path = f"{tmp}:{tmp / 'Vendor'}:{lean_path}"
        outputs["proof"] = lean_run(tmp / "Proof.lean", proof_path, tmp / "Proof.olean")
        outputs["validation"] = lean_run(tmp / "Validation.lean", proof_path, None)
        return outputs


def assert_network_isolation(bwrap: Path, outer_isolated: bool) -> None:
    if outer_isolated:
        interfaces = Path("/proc/net/dev").read_text(encoding="utf-8")
        assert all(line.strip().startswith("lo:") for line in interfaces.splitlines()[2:] if line.strip())
        probe = subprocess.run(
            [
                "/usr/bin/python3", "-I", "-c",
                "import socket; s=socket.socket(); s.settimeout(0.2); s.connect(('1.1.1.1', 53))",
            ],
            env=BASE_ENV, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            timeout=10, check=False,
        )
        assert probe.returncode != 0, "outer network-denial mutation unexpectedly connected"
        return
    probe = subprocess.run(
        [
            str(bwrap), "--ro-bind", "/", "/", "--dev", "/dev", "--proc", "/proc",
            "--unshare-net", "--die-with-parent", "/usr/bin/python3", "-I", "-c",
            "import socket; s=socket.socket(); s.settimeout(0.2); s.connect(('1.1.1.1', 53))",
        ],
        env=BASE_ENV, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        timeout=10, check=False,
    )
    assert probe.returncode != 0, "bubblewrap network-denial mutation unexpectedly connected"


def assert_vendor_manifest() -> None:
    manifest = load(HERE / "vendor-manifest.json")
    assert manifest["upstream"] == {
        "project": "math-xmum/Brouwer",
        "remote": "https://github.com/math-xmum/Brouwer",
        "revision": "c02205edf347ad45f0d62db85497598ba2c4291e",
        "source_tree": "5dda2d10fdd4a0db1aba85f1fa1a7acc509f80e4",
        "source_archive_url": "https://github.com/math-xmum/Brouwer/archive/c02205edf347ad45f0d62db85497598ba2c4291e.tar.gz",
        "source_archive_sha256": "8591fadd6737d75b921eee27dc9d85d5d9f040a83ad7dcb2d81dc208754c04cd",
        "toolchain": "leanprover/lean4:v4.31.0",
        "mathlib_revision": "fabf563a7c95a166b8d7b6efca11c8b4dc9d911f",
    }
    assert manifest["license"]["spdx"] == "MIT"
    assert manifest["license"]["sha256"] == EXPECTED_INPUTS["Vendor/LICENSE"]
    assert manifest["closure"] == {
        "module_count": 3,
        "vendored_bytes": 182363,
        "vendored_lines": 4239,
        "normalized_compatibility_patch_sha256": "39fff43f92e646d6365f6279fd565d0d2d7b873f0922a1df9165f880a36b8790",
    }
    rows = {row["path"]: row for row in manifest["files"]}
    assert set(rows) == set(VENDOR_FILES)
    for relative, (upstream_sha, byte_count) in VENDOR_FILES.items():
        row = rows[relative]
        path = HERE / "Vendor" / relative
        assert row["upstream_sha256"] == upstream_sha
        assert row["vendored_sha256"] == sha256(path)
        assert row["vendored_bytes"] == byte_count == path.stat().st_size


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--probe", action="store_true")
    args = parser.parse_args()
    outer_isolated = os.environ.get("STAGE1_OUTER_NETWORK_ISOLATED") == "1"

    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    targets = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    statement = load(HERE / "statement.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    proof_receipt = load(HERE / "proof-receipt.json")
    instance = load(HERE / "instance.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    target_row = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target_row["execution_rank"] == 685 and target_row["baseline"] == "L0"
    assert target_row["rework_required"] is True and target_row["theorem_complete"] is False
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item == {
        "id": ITEM, "theorem_id": THEOREM, "execution_rank": 685,
        "phase": "validation", "layer": 5, "state": "[ ]",
        "depends_on": ["S56-M-0319-PROOF"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Run hermetic kernel, trust, provenance, and independent validation gates.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0, "children": [],
    }
    predecessor = next(row for row in execution["items"] if row["id"] == "S56-M-0319-PROOF")
    assert predecessor["state"] == "[_]" and predecessor["attempts"] == 1
    assert instance["root_vector"] == ROOT_VECTOR
    assert instance["accepted_proof_state"] == []
    assert instance["audit_complete"] is instance["theorem_complete"] is False

    for name, expected in EXPECTED_INPUTS.items():
        assert sha256(HERE / name) == expected, f"stale validation input: {name}"
    assert sha256(LEAN_ROOT / "lean-toolchain") == TOOLCHAIN_SHA256
    assert sha256(LEAN_ROOT / "lake-manifest.json") == MANIFEST_SHA256
    assert statement["canonical_formal_target"]["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert registry["root_obligation_id"] == "M0319-ROOT"
    assert registry["denominator_sha256"] == graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert graphs["closure_boundary"] == {
        "root_closed": False,
        "minimal_open_root_cut": FROZEN_OPEN_CUT,
        "theorem_complete": False,
    }
    assert proof_receipt["canonical_target_expression_sha256"] == EXPRESSION_SHA256
    assert proof_receipt["proof_body"]["source_sha256"] == EXPECTED_INPUTS["Proof.lean"]
    assert proof_receipt["result"]["root_kernel_inhabitant_observed"] is True
    assert proof_receipt["accepted"] is proof_receipt["result"]["theorem_complete"] is False
    assert proof_receipt["graph_reconciliation_pending"]["required"] is True

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by)\b|"
        r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
        r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
        r"(?:axiom|constant|opaque|unsafe|extern)\b",
        re.MULTILINE,
    )
    all_source = "\n".join(
        source_without_comments_or_strings((HERE / name).read_text(encoding="utf-8"))
        for name in (
            "Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean",
            "Vendor/Gametheory/Scarf.lean", "Vendor/Gametheory/ScarfPath.lean",
            "Vendor/Gametheory/Brouwer.lean",
        )
    )
    assert prohibited.search(all_source) is None
    validation_source = (HERE / "Validation.lean").read_text(encoding="utf-8")
    for fragment in (
        "theorem recomposedBrouwerFixedPoint", "exactFixedPoint _ K f",
        "hasApproximateFixedPoints _ K f", "assert_no_sorry Brouwer",
        "#print_validation_closure",
    ):
        assert fragment in validation_source, fragment
    theorem_body = validation_source.split("theorem recomposedBrouwerFixedPoint", 1)[1].split("assert_no_sorry", 1)[0]
    assert "brouwerFixedPoint" not in theorem_body
    assert_vendor_manifest()
    vendor_rebuild = run(["/usr/bin/python3", "-I", "-B", str(HERE / "build_vendor_manifest.py")], env=BASE_ENV)
    assert "PASS" in vendor_rebuild

    lake_manifest = load(LEAN_ROOT / "lake-manifest.json")
    mathlib_entry = next(row for row in lake_manifest["packages"] if row["name"] == "mathlib")
    assert mathlib_entry["rev"] == mathlib_entry["inputRev"] == MATHLIB_REVISION
    assert mathlib_entry["url"] == MATHLIB_REMOTE
    assert (LEAN_ROOT / ".lake").is_symlink()
    mathlib = (LEAN_ROOT / ".lake/packages/mathlib").resolve()
    assert git("rev-parse", "HEAD", cwd=mathlib) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == MATHLIB_TREE
    assert git("status", "--porcelain=v1", "--untracked-files=all", cwd=mathlib) == ""
    assert git("remote", "get-url", "origin", cwd=mathlib) == MATHLIB_REMOTE
    assert sha256(mathlib / "LICENSE") == MATHLIB_LICENSE_SHA256

    launcher = Path(HOME) / ".elan/bin/lake"
    assert sha256(launcher) == ELAN_LAUNCHER_SHA256
    lean = Path(run([str(launcher), "env", "which", "lean"], cwd=mathlib, env=BASE_ENV).strip())
    lake = Path(run([str(launcher), "env", "which", "lake"], cwd=mathlib, env=BASE_ENV).strip())
    bwrap = Path("/usr/bin/bwrap")
    python = Path("/usr/bin/python3").resolve()
    git_executable = Path("/usr/bin/git")
    assert sha256(lean) == LEAN_SHA256 and sha256(lake) == LAKE_SHA256
    assert sha256(bwrap) == BWRAP_SHA256 and sha256(python) == PYTHON_SHA256
    assert sha256(git_executable) == GIT_SHA256
    assert LEAN_COMMIT in run([str(lean), "--version"], env=BASE_ENV)
    assert_network_isolation(bwrap, outer_isolated)

    outputs = isolated_replay(lean, bwrap, pinned_lean_path(lean), outer_isolated)
    combined = "\n".join(outputs.values())
    assert "sorryAx" not in combined and "error:" not in combined.lower()
    for declaration in PROOF_DECLARATIONS:
        assert reported_axioms(outputs["proof"], declaration) == EXPECTED_AXIOMS
    assert reported_axioms(outputs["validation"], "Stage1Instances.THM_M_0319.brouwerFixedPoint") == EXPECTED_AXIOMS
    assert reported_axioms(outputs["validation"], VALIDATION_DECLARATION) == EXPECTED_AXIOMS
    assert outputs["validation"].count("Declarations are sorry-free!") == 2
    closure_match = re.search(r"VALIDATION_CLOSURE declarations=(\d+) modules=(\d+)", outputs["validation"])
    assert closure_match is not None
    assert "VALIDATION_CLOSURE axioms=[propext, Classical.choice, Quot.sound]" in outputs["validation"]
    assert "VALIDATION_CLOSURE bodyless_nonaxioms=[]" in outputs["validation"]
    assert "VALIDATION_CLOSURE unsafe=[]" in outputs["validation"]
    observation = {
        "lean_output_sha256": {name: hashlib.sha256(output.encode()).hexdigest() for name, output in outputs.items()},
        "observed_axioms": sorted(EXPECTED_AXIOMS),
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
    packet = load(ROOT / ".stage1-worker-selftest.json")
    assert spec["schema_version"] == "stage1-validation-spec/1.0"
    assert spec["item_id"] == receipt["item_id"] == packet["item_id"] == ITEM
    assert spec["theorem_id"] == receipt["theorem_id"] == THEOREM
    assert spec["depends_on"] == receipt["depends_on"] == ["S56-M-0319-PROOF"]
    assert len(spec["recipes"]) == 1 and spec["recipes"][0] == receipt["recipe"]
    assert receipt["target"] == {
        "declaration": "Stage1Instances.THM_M_0319.BrouwerFixedPointTarget",
        "elaborated_expression_sha256": EXPRESSION_SHA256,
        "statement_source_sha256": EXPECTED_INPUTS["Statement.lean"],
        "registry_denominator_sha256": DENOMINATOR_SHA256,
        "exact_statement_delta": "none",
    }
    recipe = spec["recipes"][0]
    assert recipe["argv"] == [
        "/usr/bin/bwrap", "--ro-bind", "/", "/", "--dev", "/dev", "--proc", "/proc",
        "--tmpfs", "/tmp", "--unshare-net", "--die-with-parent",
        "--setenv", "LANG", "C.UTF-8", "--setenv", "LC_ALL", "C.UTF-8",
        "--setenv", "TZ", "UTC", "--setenv", "LEAN_NUM_THREADS", "1",
        "--setenv", "STAGE1_OUTER_NETWORK_ISOLATED", "1",
        "/usr/bin/python3", "-I", "-B", f"Stage1_Instances/{THEOREM}/check_validation.py",
    ]
    assert recipe["network_policy"] == "denied" and recipe["expected_exit"] == 0
    assert recipe["timeout_seconds"] == 1800
    assert "bubblewrap" in recipe["network_enforcement"].lower()
    assert outer_isolated, "recorded recipe must enclose the Python parent in Bubblewrap"
    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["phase"] == "validation" and receipt["intent"] == "validate"
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    started = datetime.fromisoformat(receipt["validation_started_at"])
    ended = datetime.fromisoformat(receipt["validation_ended_at"])
    validated = datetime.fromisoformat(receipt["validated_at"])
    assert started.tzinfo is not None and ended.tzinfo is not None and validated.tzinfo is not None
    now = datetime.now(timezone.utc)
    assert started <= ended == validated
    assert ended <= now or os.environ.get("STAGE1_BOOTSTRAP_RECEIPT") == "1"
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == packet["state"] == "[_]"
    assert receipt["accepted"] is receipt["release_grade"] is False
    assert receipt["verdict"] == "blocked"
    assert receipt["root_vector_before"] == receipt["root_vector_after"] == ROOT_VECTOR
    assert receipt["accepted_receipt_ids"] == []
    repository_state = receipt["repository_state"]
    assert repository_state["release_clean"] is False
    tracked_patch = run(
        ["/usr/bin/git", "diff", "--binary", "--", f"Stage1_Instances/{THEOREM}"],
        env=BASE_ENV,
    ).encode()
    assert repository_state["tracked_patch_sha256"] == hashlib.sha256(tracked_patch).hexdigest()
    assert repository_state["tracked_patch_bytes"] == len(tracked_patch) == 0
    input_payload = [
        {"path": relative, "sha256": sha256(ROOT / relative)}
        for relative in (
            f"Stage1_Instances/{THEOREM}/Validation.lean",
            f"Stage1_Instances/{THEOREM}/check_validation.py",
            f"Stage1_Instances/{THEOREM}/validation-phase.md",
            f"Stage1_Instances/{THEOREM}/validation-spec.json",
        )
    ]
    assert repository_state["untracked_input_scope"] == [row["path"] for row in input_payload]
    assert repository_state["untracked_input_sha256"] == {row["path"]: row["sha256"] for row in input_payload}
    assert repository_state["untracked_input_bundle_sha256"] == hashlib.sha256(
        json.dumps(input_payload, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    assert repository_state["preexisting_lake_symlink_target_sha256"] == hashlib.sha256(
        os.readlink(LEAN_ROOT / ".lake").encode()
    ).hexdigest()
    assert "non-circular input bundle" in repository_state["untracked_input_scope_boundary"]
    change_impact = receipt["change_impact"]
    assert change_impact["exact_statement_changes"] == []
    assert change_impact["typed_graph_changes"] == []
    assert change_impact["authoritative_state_changes"] == []
    assert change_impact["exact_declarations_added"] == [VALIDATION_DECLARATION]
    for name, expected in EXPECTED_INPUTS.items():
        assert receipt["inputs"][name] == expected
    assert receipt["inputs"]["lean-toolchain"] == TOOLCHAIN_SHA256
    assert receipt["inputs"]["lake-manifest.json"] == MANIFEST_SHA256
    assert receipt["inputs"]["validation-spec.json"] == sha256(HERE / "validation-spec.json")
    assert receipt["inputs"]["check_validation.py"] == sha256(Path(__file__).resolve())
    environment = receipt["environment"]
    assert environment["lean_executable_sha256"] == sha256(lean)
    assert environment["lake_executable_sha256"] == sha256(lake)
    assert environment["python_executable_sha256"] == sha256(python)
    assert environment["git_executable_sha256"] == sha256(git_executable)
    assert environment["bubblewrap_executable_sha256"] == sha256(bwrap)
    assert environment["mathlib_revision"] == MATHLIB_REVISION
    assert environment["mathlib_tree"] == MATHLIB_TREE
    assert environment["mathlib_worktree_clean"] is True
    assert receipt["trust"]["accepted_foundation_policy"] is False
    assert receipt["trust"]["complete_transitive_tcb_inventory"] is False
    assert receipt["provenance"]["complete_provenance_gate"] == "fail_closed"
    assert receipt["hermeticity"]["decision"].startswith("fail_closed")
    assert receipt["independent_validation"]["decision"] == "fail_closed"
    assert receipt["result"]["lean_output_sha256"] == observation["lean_output_sha256"]
    assert receipt["result"]["observed_axioms"] == observation["observed_axioms"]
    assert receipt["result"]["validation_closure"] == observation["validation_closure"]
    assert receipt["result"]["exact_root_kernel_replay"] == "pass_provisional_nonrelease"
    assert receipt["result"]["accepted_closed_obligation_ids"] == []
    assert receipt["result"]["frozen_composition_gate"] == "fail_closed"
    assert receipt["result"]["hermetic_release_gate"] == "fail_closed"
    assert receipt["result"]["independent_distinct_runner_gate"] == "fail_closed"
    assert receipt["result"]["audit_complete"] is receipt["result"]["theorem_complete"] is False
    summary_text = "PASS THM-M-0319 narrow validation\n" + "\n".join(SUMMARY_LINES) + "\n"
    assert receipt["evidence_log"] == {
        "stream": "stdout",
        "bytes": len(summary_text.encode()),
        "sha256": hashlib.sha256(summary_text.encode()).hexdigest(),
        "exit_code": 0,
        "archive_classification": "Deterministic nonrelease semantic summary digest; transient raw Lean subprocess streams are individually content-addressed in result.lean_output_sha256 but are not a release archive.",
    }
    assert receipt["first_failed_gate"] == "dependency.S56-M-0319-PROOF.master_acceptance"
    assert receipt["remaining_root_cut_set"] == FROZEN_OPEN_CUT
    assert receipt["output_summary"] == ["PASS THM-M-0319 narrow validation", *SUMMARY_LINES]
    assert len(receipt["commands"]) == len(packet["commands"])
    assert all(isinstance(row, dict) and "exit_code" in row for row in receipt["commands"])
    assert [" ".join(row["argv"]) for row in receipt["commands"] if "env" not in row] == [
        command for command in packet["commands"] if not command.startswith("PYTHONPYCACHEPREFIX=")
    ]
    assert set(receipt["changed_paths"]) == set(CHANGED_PATHS)
    assert set(packet["changed_paths"]) == set(CHANGED_PATHS)
    assert packet["base_revision"] == BASE_REVISION and packet["known_failures"]
    status = git("status", "--short", "--untracked-files=all").splitlines()
    assert all(line.startswith("?? ") for line in status), status
    actual = {line[3:] for line in status if line[3:] != "Formalizations/Lean/.lake"}
    assert actual == set(CHANGED_PATHS), (actual, CHANGED_PATHS)
    for relative in CHANGED_PATHS:
        assert_text_hygiene(ROOT / relative)

    print("PASS THM-M-0319 narrow validation")
    for line in SUMMARY_LINES:
        print(line)


if __name__ == "__main__":
    main()
