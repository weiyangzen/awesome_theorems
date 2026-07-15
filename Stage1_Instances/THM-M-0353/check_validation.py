#!/usr/bin/env python3
"""Fail-closed narrow validator for S56-M-0353-VALIDATION."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import platform
import re
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0353"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
ITEM = "S56-M-0353-VALIDATION"
THEOREM = "THM-M-0353"
BASE_REVISION = "b8c0a0c119a82ef435e23f9ff85bfd783db95736"
BASE_TREE = "831576eb7d1273d01e99653d36b616e99e85dc0f"
TOOLCHAIN = "leanprover/lean4:v4.29.0"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
LEAN_SHA256 = "3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf"
LAKE_SHA256 = "a608ff084d7e2af228b92a29d7c2fd083ba0580e46889175ec74a81678c98359"
BWRAP_SHA256 = "0abea81db798ebf6b4742ac0664802d97521547a353c2a0dbdc21d76cbbfd2c0"
PYTHON_SHA256 = "b8d8288faefdd300201f43fcf00f6f539a27218eeed3a3dff5ab10b9c4c99700"
GIT_SHA256 = "5516c9f362c29376ab9a499a33082f9f611941d8c75930c880e30ad109e39c9a"
BASH_SHA256 = "3efccc187bafa75ff1e37d246270ab3e7aa559f242c7a52bf3ec2a1b5450bdbd"
TIMEOUT_SHA256 = "48893b0fb21436b54619db80486e83ef39dfccaf1aefe83dfa00c02d6146e8c0"
TOOLCHAIN_SHA256 = "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2"
MANIFEST_SHA256 = "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81"
BLUEPRINT_SHA256 = "972a2ca9fd6b8e283aeb923875c2e14960706f936605a48868b321a11f94e1c4"
EXECUTION_DAG_SHA256 = "89b38a84a11fb9beeb96794ac1affb8fa433c6d1b87ead215658f28f326791f6"
TARGET_MANIFEST_SHA256 = "02eec284de534dd78e1cf75f82a477ff477567dd682b7445cb7587abd137ab2c"
SKILL_SHA256 = "26d47a66c6535feabb8bbf1051fd55d76a53fe761f4b3d953f86b97ec86152b8"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MATHLIB_REMOTE = "https://github.com/leanprover-community/mathlib4.git"
MATHLIB_LICENSE_SHA256 = "b40930bbcf80744c86c46a12bc9da056641d722716c378f5659b9e555ef833e1"
EXPRESSION_SHA256 = "planned:v1:sha256:1367304ec51ed39ff267372c97e62f55f36bde2ed1901683c076f889917bbe6f"
DENOMINATOR_SHA256 = "4516c92f499b2c9dfc0c2097d27d1a7eb177a4965b00d4b1dcf38456d8efd0f0"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
ROOT_VECTOR = {"H": "H1", "M": "M4", "R": "R4"}
FROZEN_OPEN_CUT = ["M0353-P-MEMLP", "M0353-P-BASIS"]
EXPECTED_INPUTS = {
    "Statement.lean": "58416bc39074209c0d725fce0a9c0dbf09725d847e2be24a77ebaa73527e2d99",
    "ObligationTree.lean": "fdd4f947aea690c1cdbfaeb1dcbff9ded6476267163c31c28f85d0792ab0dfbc",
    "Proof.lean": "8e911384a90dab39dd135b73e5205fb05cb673146e27743b2d51ca045e7b6e23",
    "instance.json": "00478a787aaf2d703ed45d6fbf366258e7b79ebc913f515b3f19a5a86a484bc1",
    "task-dag.json": "f663ea0e3293ca14da37e4f1339f81df3ba582d3d9ed1573dae89d3eee608a8e",
    "anchor-audit.json": "468b16881b49a74d5b868a3b8600b5d5b8be2c923024056e9432a2497ec7ebfe",
    "obligation-registry.json": "e87ac0a8bd1d6e1816f8816ec85d08e94686230e6afd00d294eca8f732bd6376",
    "typed-graphs.json": "868cdcbd5d6c2e049b21c8138016a96a0fdd1ba7e9eceba8ce5685032c3fc329",
    "proof-receipt.json": "37046312afe3a15490decb23ac4688d4198d95ce3804f144a90897ae5d9ea167",
    "proof-validation.md": "308f01ce1d528494234585eba92398735b5c046d42a0ff1b2deff7aeead0c68c",
    "check_proof.py": "04094408b20d77adcec55a7c780b6e1f4fbc6aebd5b455250a18e0e251e6cf0b",
    "check_proof.sh": "1726c71d35d2dfd586e35acc95451eb4822df40dae392a9c8140c6b99b7fcabf",
    "vendor-manifest.json": "7fb077d8c7a26522e65b3c9237d8500be15be4ffc55cee8e0ba68f3b24a5ab7c",
    "VENDOR_PROVENANCE.md": "94d06437c58c3ff5a364001b50c53ae9ce1001525021c0dfef2eb7b22f5ea700",
    "build_vendor_manifest.py": "4af810edb20cc4e4916fe9c41a5bdcc87d6fde14215e041f7eaeb8833efc7c59",
    "Vendor/GaussianField/HermiteFunctions.lean": "e25548a1e042a61b340e24931dc05fd49bcaa6cf1daf68c335859df58d3b3d49",
    "Vendor/LICENSE": "2d3b806e6fd270f11819d0f797f721747adb0d497760e1b9053b6cd1fae4cf54",
    "Validation.lean": "8ec719b062588cc90970aaf9577bce7e540edbff14cde0225cf5217dbd96a0ed",
}
TRUST_BOUNDARIES = {
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
    "hermiteFunction_memLp",
    "hermiteFunction_orthonormal",
    "hermiteFunction_complete",
    "Stage1Instances.THM_M_0353.hermiteMemLpPackage_proof",
    "Stage1Instances.THM_M_0353.hermiteBasisPackage_proof",
    "Stage1Instances.THM_M_0353.hermiteCompletenessTarget_proof",
)
VALIDATION_DECLARATION = (
    "Stage1Instances.THM_M_0353.Validation.recomposedHermiteCompleteness"
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
    "PASS narrow kernel replay: exact statement, frozen composer, byte-identical vendor source, proof bodies, exact root, and differential recomposition elaborated at trust zero",
    "PASS trust observation: seven checked declarations use exactly propext, Classical.choice, and Quot.sound; root closure has no unexpected bodyless or unsafe declaration",
    "PASS selected provenance: frozen inputs, upstream source/blob/archive identities, Apache-2.0 license, tool identities, and clean pinned mathlib agree",
    "FAIL CLOSED authority and graph: proof is not master accepted and the frozen weighted-density route is not reconciled with the vendored moments/Fourier-uniqueness proof route",
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
        result: dict[str, object] = {}
        for key, value in pairs:
            assert key not in result, f"duplicate JSON key in {path}: {key}"
            result[key] = value
        return result

    value = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicates)
    assert isinstance(value, dict), path
    return value


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


def run(argv: list[str], *, cwd: Path = ROOT, env: dict[str, str] | None = None) -> str:
    result = subprocess.run(
        argv, cwd=cwd, env=env, text=True, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, timeout=1800, check=False,
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
    escaped = False
    while index < len(source):
        pair = source[index:index + 2]
        char = source[index]
        if depth:
            if pair == "/-":
                depth += 1
                index += 2
            elif pair == "-/":
                depth -= 1
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
            depth = 1
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
            index += 1
        else:
            output.append(char)
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


def pinned_lean_path(lean: Path) -> str:
    package_root = (LEAN_ROOT / ".lake/packages").resolve()
    roots = sorted(
        path.resolve() for path in package_root.glob("*/.lake/build/lib/lean")
        if path.is_dir()
    )
    local = (LEAN_ROOT / ".lake/build/lib/lean").resolve()
    assert roots and local.is_dir()
    return ":".join([*(str(path) for path in roots), str(local), str(lean.parent.parent / "lib/lean")])


def isolated_replay(lean: Path, lean_path: str, outer_isolated: bool) -> dict[str, str]:
    with tempfile.TemporaryDirectory(prefix="stage1-m0353-validation-", dir="/tmp") as tmp_name:
        tmp = Path(tmp_name).resolve()
        vendor = tmp / "Vendor" / "GaussianField"
        vendor.mkdir(parents=True)
        for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
            (tmp / name).write_bytes((HERE / name).read_bytes())
        (vendor / "HermiteFunctions.lean").write_bytes(
            (HERE / "Vendor/GaussianField/HermiteFunctions.lean").read_bytes()
        )
        (tmp / "home").mkdir()

        def lean_run(source: Path, module_path: str, output: Path | None) -> str:
            argv = [str(lean), "--trust=0", "-t0", "-R", str(tmp)]
            if output is not None:
                argv += ["-o", str(output)]
            argv.append(str(source))
            child_env = {
                **BASE_ENV,
                "HOME": str(tmp / "home"),
                "TMPDIR": str(tmp),
                "LEAN_PATH": module_path,
            }
            assert outer_isolated, "recorded recipe must enclose every Lean child"
            return run(argv, cwd=tmp, env=child_env)

        outputs: dict[str, str] = {}
        outputs["statement"] = lean_run(tmp / "Statement.lean", lean_path, tmp / "Statement.olean")
        outputs["tree"] = lean_run(
            tmp / "ObligationTree.lean", f"{tmp}:{lean_path}", tmp / "ObligationTree.olean"
        )
        outputs["vendor"] = lean_run(
            vendor / "HermiteFunctions.lean", lean_path, vendor / "HermiteFunctions.olean"
        )
        proof_path = f"{tmp}:{lean_path}"
        outputs["proof"] = lean_run(tmp / "Proof.lean", proof_path, tmp / "Proof.olean")
        outputs["validation"] = lean_run(tmp / "Validation.lean", proof_path, None)
        return outputs


def assert_network_isolation(outer_isolated: bool) -> None:
    assert outer_isolated, "recorded recipe must enclose the Python parent in Bubblewrap"
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
    assert probe.returncode != 0, "network-denial mutation unexpectedly connected"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--probe", action="store_true")
    args = parser.parse_args()
    outer_isolated = os.environ.get("STAGE1_OUTER_NETWORK_ISOLATED") == "1"

    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    targets = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    instance = load(HERE / "instance.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    proof_receipt = load(HERE / "proof-receipt.json")
    vendor_manifest = load(HERE / "vendor-manifest.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    target_row = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target_row["execution_rank"] == 846 and target_row["baseline"] == "L0"
    assert target_row["lifecycle_mode"] == "planned"
    assert target_row["rework_required"] is True and target_row["theorem_complete"] is False
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item == {
        "id": ITEM, "theorem_id": THEOREM, "execution_rank": 846,
        "phase": "validation", "layer": 5, "state": "[ ]",
        "depends_on": ["S56-M-0353-PROOF"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Run hermetic kernel, trust, provenance, and independent validation gates.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0, "children": [],
    }
    predecessor = next(row for row in execution["items"] if row["id"] == "S56-M-0353-PROOF")
    assert predecessor["state"] == "[_]" and predecessor["attempts"] == 1
    assert instance["root_vector"] == ROOT_VECTOR
    assert instance["accepted_proof_state"] == []
    assert instance["audit_complete"] is instance["theorem_complete"] is False

    for name, expected in EXPECTED_INPUTS.items():
        assert sha256(HERE / name) == expected, f"stale validation input: {name}"
    assert sha256(LEAN_ROOT / "lean-toolchain") == TOOLCHAIN_SHA256
    assert sha256(LEAN_ROOT / "lake-manifest.json") == MANIFEST_SHA256
    assert registry["root_obligation_id"] == "M0353-ROOT"
    assert registry["denominator_sha256"] == graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert graphs["closure_boundary"] == {
        "root_closed": False,
        "theorem_complete": False,
        "minimal_open_root_cut": FROZEN_OPEN_CUT,
    }
    assert proof_receipt["canonical_target"] == (
        "Stage1Instances.THM_M_0353.HermiteCompletenessTarget"
    )
    assert proof_receipt["canonical_target_expression_sha256"] == EXPRESSION_SHA256
    assert proof_receipt["proof_body"]["source_sha256"] == EXPECTED_INPUTS["Proof.lean"]
    assert proof_receipt["result"]["root_kernel_closed"] is True
    assert proof_receipt["accepted"] is proof_receipt["result"]["theorem_complete"] is False
    assert proof_receipt["accepted_closed_obligation_ids"] == []

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by)\b|"
        r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
        r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
        r"(?:axiom|constant|opaque|unsafe|extern)\b",
        re.MULTILINE,
    )
    for relative in (
        "Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean",
        "Vendor/GaussianField/HermiteFunctions.lean",
    ):
        source = source_without_comments_or_strings((HERE / relative).read_text(encoding="utf-8"))
        match = prohibited.search(source)
        assert match is None, (relative, match.group(0) if match else None)
    validation_source = (HERE / "Validation.lean").read_text(encoding="utf-8")
    assert "theorem recomposedHermiteCompleteness : HermiteCompletenessTarget" in validation_source
    assert "hermiteCompletenessTarget_proof" not in validation_source.split(
        "theorem recomposedHermiteCompleteness", 1
    )[1].split("assert_no_sorry", 1)[0]

    upstream = vendor_manifest["upstream"]
    assert upstream["project"] == "mrdouglasny/gaussian-field"
    assert upstream["revision"] == "d63a28568a75d99f6cb27af1f888a49a69855a66"
    assert upstream["source_tree"] == "7b2c1a97a992cacee49dcbd347a9d78d59fdc383"
    assert upstream["source_archive_sha256"] == (
        "3d0504de255e7684f9f7badebff98dcb05619dfe180dbfa56d55c94bcdc4961c"
    )
    assert vendor_manifest["license"]["spdx"] == "Apache-2.0"
    assert vendor_manifest["license"]["sha256"] == EXPECTED_INPUTS["Vendor/LICENSE"]
    assert vendor_manifest["files"][0]["git_blob_sha1"] == (
        "077d911f5e26a11199bc0756f50a803a58490807"
    )
    assert vendor_manifest["compatibility"]["source_transform_count"] == 0

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
    for relative, expected in TRUST_BOUNDARIES.items():
        source = mathlib / relative
        olean = mathlib / ".lake/build/lib/lean" / Path(relative).with_suffix(".olean")
        assert git("rev-parse", f"HEAD:{relative}", cwd=mathlib) == expected["blob"]
        assert sha256(source) == expected["source_sha256"]
        assert sha256(olean) == expected["olean_sha256"]
        assert olean.stat().st_size == expected["olean_bytes"]

    toolchain_root = Path(HOME) / ".elan/toolchains/leanprover--lean4---v4.29.0"
    lean = toolchain_root / "bin/lean"
    lake = toolchain_root / "bin/lake"
    bwrap = Path("/usr/bin/bwrap")
    python = Path("/usr/bin/python3").resolve()
    git_executable = Path("/usr/bin/git")
    bash = Path("/usr/bin/bash")
    timeout = Path("/usr/bin/timeout")
    assert sha256(lean) == LEAN_SHA256 and sha256(lake) == LAKE_SHA256
    assert sha256(bwrap) == BWRAP_SHA256 and sha256(python) == PYTHON_SHA256
    assert sha256(git_executable) == GIT_SHA256 and sha256(bash) == BASH_SHA256
    assert sha256(timeout) == TIMEOUT_SHA256
    assert LEAN_COMMIT in run([str(lean), "--version"], env=BASE_ENV)
    assert_network_isolation(outer_isolated)

    outputs = isolated_replay(lean, pinned_lean_path(lean), outer_isolated)
    combined = "\n".join(outputs.values())
    assert "sorryAx" not in combined and "error:" not in combined.lower()
    assert outputs["proof"].count("Declarations are sorry-free!") == len(PROOF_DECLARATIONS)
    validation_sorry_reports = outputs["validation"].count("Declarations are sorry-free!")
    if args.probe and validation_sorry_reports != 2:
        raise RuntimeError(
            f"validation sorry report count={validation_sorry_reports}\n"
            f"{outputs['validation']}"
        )
    assert validation_sorry_reports == 2
    for declaration in PROOF_DECLARATIONS:
        assert reported_axioms(outputs["proof"], declaration) == EXPECTED_AXIOMS
    assert reported_axioms(outputs["validation"], PROOF_DECLARATIONS[-1]) == EXPECTED_AXIOMS
    assert reported_axioms(outputs["validation"], VALIDATION_DECLARATION) == EXPECTED_AXIOMS
    closure = re.search(
        r"VALIDATION_CLOSURE declarations=(\d+) modules=(\d+).*?"
        r"VALIDATION_CLOSURE axioms=\[(.*?)\].*?"
        r"VALIDATION_CLOSURE bodyless_nonaxioms=\[(.*?)\].*?"
        r"VALIDATION_CLOSURE unsafe=\[(.*?)\]",
        outputs["validation"], re.DOTALL,
    )
    assert closure is not None, outputs["validation"]
    assert int(closure.group(1)) > 100 and int(closure.group(2)) > 10
    assert set(closure.group(3).split(", ")) == EXPECTED_AXIOMS
    assert closure.group(4) == closure.group(5) == ""

    observation = {
        "lean_output_sha256": {
            name: hashlib.sha256(output.encode()).hexdigest()
            for name, output in outputs.items()
        },
        "observed_axioms": sorted(EXPECTED_AXIOMS),
        "proof_sorry_free_reports": len(PROOF_DECLARATIONS),
        "validation_sorry_free_reports": validation_sorry_reports,
        "closure_declaration_count": int(closure.group(1)),
        "closure_module_count": int(closure.group(2)),
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
    assert spec["depends_on"] == receipt["depends_on"] == ["S56-M-0353-PROOF"]
    assert len(spec["recipes"]) == 1 and spec["recipes"][0] == receipt["recipe"]
    recipe = spec["recipes"][0]
    assert recipe["network_policy"] == "denied" and recipe["expected_exit"] == 0
    assert outer_isolated and "bubblewrap" in recipe["network_enforcement"].lower()
    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["phase"] == "validation" and receipt["intent"] == "validate"
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == packet["state"] == "[_]"
    assert receipt["accepted"] is receipt["release_grade"] is False
    assert receipt["verdict"] == "blocked"
    assert receipt["root_vector_before"] == receipt["root_vector_after"] == ROOT_VECTOR
    assert receipt["accepted_receipt_ids"] == receipt["accepted_closed_obligation_ids"] == []
    assert receipt["target"] == {
        "declaration": "Stage1Instances.THM_M_0353.HermiteCompletenessTarget",
        "expression_fingerprint": EXPRESSION_SHA256,
        "statement_source_sha256": EXPECTED_INPUTS["Statement.lean"],
        "registry_denominator_sha256": DENOMINATOR_SHA256,
        "exact_statement_delta": "none",
    }
    for name, expected in EXPECTED_INPUTS.items():
        assert receipt["inputs"][name] == expected
    fixed_inputs = {
        "Formalizations/Lean/lean-toolchain": TOOLCHAIN_SHA256,
        "Formalizations/Lean/lake-manifest.json": MANIFEST_SHA256,
        "Docs/Stage1_Blueprint_rev-5.6.md": BLUEPRINT_SHA256,
        "Docs/Stage1_Execution_DAG_rev-5.6.json": EXECUTION_DAG_SHA256,
        "Docs/Stage1_Targets_rev-5.6.json": TARGET_MANIFEST_SHA256,
        "skills/execute-stage1-rev56/SKILL.md": SKILL_SHA256,
    }
    for name, expected in fixed_inputs.items():
        assert receipt["inputs"][name] == expected
    assert receipt["inputs"]["check_validation.py"] == sha256(HERE / "check_validation.py")
    assert receipt["inputs"]["validation-spec.json"] == sha256(HERE / "validation-spec.json")
    environment = receipt["environment"]
    assert environment["platform"] == f"{platform.system()} {platform.release()} {platform.machine()}"
    assert environment["lean_executable_sha256"] == sha256(lean)
    assert environment["lake_executable_sha256"] == sha256(lake)
    assert environment["python_executable_sha256"] == sha256(python)
    assert environment["git_executable_sha256"] == sha256(git_executable)
    assert environment["bubblewrap_executable_sha256"] == sha256(bwrap)
    assert environment["mathlib_revision"] == MATHLIB_REVISION
    assert environment["mathlib_tree"] == MATHLIB_TREE
    assert environment["mathlib_worktree_clean"] is True
    assert receipt["result"]["lean_output_sha256"] == observation["lean_output_sha256"]
    assert receipt["result"]["observed_axioms"] == observation["observed_axioms"]
    assert receipt["result"]["closure_declaration_count"] == observation["closure_declaration_count"]
    assert receipt["result"]["closure_module_count"] == observation["closure_module_count"]
    assert receipt["result"]["exact_root_kernel_replay"] == "pass_provisional_nonrelease"
    assert receipt["result"]["accepted_closed_obligation_ids"] == []
    assert receipt["result"]["accepted_root_machine_debt"] == "M4"
    assert receipt["result"]["audit_complete"] is receipt["result"]["theorem_complete"] is False
    assert receipt["provenance"]["complete_provenance_gate"] == "fail_closed"
    assert receipt["trust"]["accepted_foundation_policy"] is False
    assert receipt["trust"]["complete_transitive_tcb_inventory"] is False
    assert receipt["hermeticity"]["decision"] == "fail_closed"
    assert receipt["independent_validation"]["decision"] == "fail_closed"
    assert receipt["first_failed_gate"] == "dependency.S56-M-0353-PROOF.master_acceptance"
    assert receipt["remaining_root_cut_set"] == FROZEN_OPEN_CUT
    assert receipt["output_summary"] == ["PASS THM-M-0353 narrow validation", *SUMMARY_LINES]
    assert set(receipt["changed_paths"]) == set(CHANGED_PATHS)
    assert set(packet["changed_paths"]) == set(CHANGED_PATHS)
    assert packet["base_revision"] == BASE_REVISION
    assert packet["known_failures"] == receipt["known_failures"]
    status = git("status", "--short", "--untracked-files=all").splitlines()
    actual = {line[3:] for line in status if line[3:] != "Formalizations/Lean/.lake"}
    assert actual == set(CHANGED_PATHS), (actual, CHANGED_PATHS)
    for relative in CHANGED_PATHS:
        assert_text_hygiene(ROOT / relative)

    print("PASS THM-M-0353 narrow validation")
    for line in SUMMARY_LINES:
        print(line)


if __name__ == "__main__":
    main()
