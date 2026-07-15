#!/usr/bin/env python3
"""Fail-closed narrow validator for S56-M-0320-VALIDATION."""

from __future__ import annotations

import argparse
from datetime import datetime
import hashlib
import json
import os
from pathlib import Path
import platform
import re
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0320"
SOURCE = ROOT / "Stage1_Instances" / "THM-M-0318"
VENDOR = SOURCE / "Vendor"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
ITEM = "S56-M-0320-VALIDATION"
THEOREM = "THM-M-0320"
BASE_REVISION = "63a9ed9c4aae594da31423142b0658129d5452a7"
BASE_TREE = "7bee4fac4489bad36fd615a023df13bb294d1781"
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
BLUEPRINT_SHA256 = "11c69fc6ec7ddbb98a174bc14e2c471757e3838ee4f8171181763102ce5619ce"
EXECUTION_DAG_SHA256 = "8e271d0a1e6ea51950c87d16be55303172f6b1f237718facaeb23c1109d11d02"
TARGET_MANIFEST_SHA256 = "02eec284de534dd78e1cf75f82a477ff477567dd682b7445cb7587abd137ab2c"
SKILL_SHA256 = "26d47a66c6535feabb8bbf1051fd55d76a53fe761f4b3d953f86b97ec86152b8"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MATHLIB_REMOTE = "https://github.com/leanprover-community/mathlib4.git"
MATHLIB_LICENSE_SHA256 = "b40930bbcf80744c86c46a12bc9da056641d722716c378f5659b9e555ef833e1"
REGISTRY_DENOMINATOR_SHA256 = (
    "b513af2baba56c289271260eadeeaea0c1df46090f3728123c0395b955b0b974"
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
ACCEPTED_ROOT_VECTOR = {"H": "H1", "M": "M4", "R": "R4"}
FROZEN_CLOSED = ["M0320-S-STATEMENT", "M0320-T-ASSEMBLE", "M0320-T-COMPACT"]
FROZEN_OPEN_CUT = ["M0320-T-GRAPH", "M0320-C-CORE"]
EXPECTED_INPUTS = {
    "Statement.lean": "3faa541aa99857bcbebb808f0d49a077377d20ab5b73144bbb5eedd5e93f04df",
    "ObligationTree.lean": "88050f777a447ba3dd2f78dd9069bce14667567647197b6c5b24febbfddb84e2",
    "GraphBridgeProof.lean": "efbabf2c2418c4f068970871a5837071c742da274256d85e2081d5613c49e033",
    "BrouwerSource.lean": "164011f052a69a85b961cfaafccffe87f94ad99de916429850d5da320dbe65e9",
    "Proof.lean": "5c5545ee48cb84f046a112569b156f88637963e67965a244337db1ecb5c83c22",
    "Validation.lean": "e666cd52d7f2a20c23ee3eec47d7423126a23012555f622acb0a26e4658a92ba",
    "TrustAudit.lean": "6d3e0dfae9f31520416938e955cc87ee3c4820f1d45039204fb07eeb21247e6f",
    "instance.json": "8bc23a5d11b991f57015090215d049ad3d8dff5b55173777a6c09e1ccd7af789",
    "task-dag.json": "839f9714363fda9a8153c32efe0824008e9732d891b71897c52cf4bb45470746",
    "anchor-audit.json": "d53cbbccadba992b4e292ca3b759d9cc9d28a1e044aea3dea5a29843adb1c736",
    "obligation-registry.json": "1d83900afadc0effc677f1f4ad40ad0da96b6a8fba25911ee7c5488759622c13",
    "typed-graphs.json": "5bda34edf918402375545fd36aff0d03843f5cb62b16fa6692993f7544ddedc1",
    "validation-specs.json": "18fca0b3b6522967aad6e78bf188bacfa0846d3a8c4b5f7e1f297a3bc679a4fa",
    "proof-receipt.json": "e9b7f89884744a08f12b8bcdf3d7a05ac2d1f0bf6e05f5a66f4fced8dd06968e",
    "brouwer-source.json": "0f078d8b53c1dda2105b532f9159d053f0ce4a909c6a547326ce581c0b493d14",
    "check_obligation_tree.py": "01d75eb8613877a2347372ede62084f17170dccdc81d4543085e379232d29a14",
}
VENDOR_INPUTS = {
    "Vendor/Gametheory/Scarf.lean": "210dc01a3b823527ce3c4c079879ee897ef6f7aefb9e9a15406a20eeedcb92a6",
    "Vendor/Gametheory/ScarfPath.lean": "d9e661c3e46e9d0ffcdbed7ca62696d6baed5aa77f5e834002d307b30c86b2bd",
    "Vendor/Gametheory/Brouwer.lean": "8cb62d7ae0820c620e9665a9124e2f07b7b5c20da8455a44a633b1e6e8948110",
    "Vendor/LICENSE": "956bddafa77f8b8ad428bb35cf59424b0ddd0933ebab506037b97a20fab1a5d0",
    "vendor-manifest.json": "8735e7a3a1a17e47dff4b0e2ded4c358d7d8f28ba959cab48677c3dfe473283a",
    "VENDOR_PROVENANCE.md": "0e802682cd69bbca3e2e7c281e0d95836e065757836a096694ab77cef2e74995",
    "build_vendor_manifest.py": "b782c11a88d648482d45233186b6ea6b5b293d780bb60a4626925f8281c540f3",
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
    "Stage1Instances.THM_M_0320.closedGraphKakutaniCore",
    "Stage1Instances.THM_M_0320.kakutaniFixedPoint",
)
TREE_DECLARATIONS = (
    "Stage1Instances.THM_M_0320.compact_of_closed_bounded",
    "Stage1Instances.THM_M_0320.root_of_closedGraph_packages",
)
GRAPH_DECLARATIONS = (
    "Stage1Instances.THM_M_0320.upperHemicontinuityClosedGraphBridge",
)
VALIDATION_DECLARATIONS = (
    "Stage1Instances.THM_M_0320.Validation.compact_of_closed_bounded",
    "Stage1Instances.THM_M_0320.Validation.upperHemicontinuity_closedGraph",
    "Stage1Instances.THM_M_0320.Validation.kakutaniFixedPoint_conditional",
)
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/Validation.lean",
    f"Stage1_Instances/{THEOREM}/TrustAudit.lean",
    f"Stage1_Instances/{THEOREM}/check_validation.py",
    f"Stage1_Instances/{THEOREM}/validation-phase.md",
    f"Stage1_Instances/{THEOREM}/validation-receipt.json",
    f"Stage1_Instances/{THEOREM}/validation-spec.json",
}
SUMMARY_LINES = [
    "PASS kernel: exact statement, frozen composition, graph bridge, vendored Brouwer closure, proof core/root, and conditional differential replayed at trust zero",
    "PASS trust observation: fourteen reports are sorry-free and every checked proof-bearing declaration uses only propext, Classical.choice, and Quot.sound",
    "PASS selected provenance: local hashes, reversible MIT vendor port, immutable upstream identities, tools, license, and clean pinned mathlib agree",
    "FAIL CLOSED authority: all predecessors are provisional; local task/graph records predate proof; accepted root remains H1/M4/R4",
    "FAIL CLOSED identity/trust/provenance: no accepted expression fingerprint, foundation policy, full transitive declaration/artifact/TCB closure, or SBOM exists",
    "FAIL CLOSED hermeticity: canonical lake env is blocked by the incomplete flt-regular artifact and the successful replay reused shared warm dependencies",
    "FAIL CLOSED independence: the conditional no-import probe shares this worker, checkout, kernel, cache, and proof architecture; no distinct signed verifier exists",
    "audit_complete=false; theorem_complete=false",
]
EXPECTED_SUMMARY = ("PASS S56-M-0320-VALIDATION narrow validation\n" + "\n".join(SUMMARY_LINES) + "\n").encode()


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
    "PATH": "/usr/bin:/bin",
    "ELAN_TOOLCHAIN": TOOLCHAIN,
    "LANG": "C.UTF-8",
    "LC_ALL": "C.UTF-8",
    "TZ": "UTC",
    "LEAN_NUM_THREADS": "1",
}


def run(
    argv: list[str], *, cwd: Path = ROOT, env: dict[str, str] | None = None,
    timeout: int = 900,
) -> str:
    result = subprocess.run(
        argv, cwd=cwd, env=env, text=True, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, timeout=timeout, check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(f"command failed ({result.returncode}): {argv!r}\n{result.stdout}")
    return result.stdout


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["/usr/bin/git", *args], cwd=cwd, env=BASE_ENV).strip()


def strip_lean(source: str) -> str:
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


def normalized_axioms(output: str, declaration: str) -> set[str]:
    pattern = re.compile(
        re.escape(f"'{declaration}' depends on axioms: [") + r"(.*?)]", re.DOTALL
    )
    matches = pattern.findall(output)
    no_axioms = f"'{declaration}' does not depend on any axioms"
    assert len(matches) + output.count(no_axioms) == 1, declaration
    if not matches:
        return set()
    values = {part.strip() for part in matches[0].split(",") if part.strip()}
    return {"Classical.choice" if value == "choice" else value for value in values}


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


def replay(lean: Path, lean_path: str) -> dict[str, str]:
    with tempfile.TemporaryDirectory(prefix="stage1-m0320-validation-", dir="/tmp") as name:
        tmp = Path(name).resolve()
        target = tmp / "Stage1_Instances" / THEOREM
        vendor = target / "Vendor"
        target.mkdir(parents=True)
        for filename in (
            "Statement.lean", "ObligationTree.lean", "GraphBridgeProof.lean",
            "BrouwerSource.lean", "Proof.lean", "Validation.lean", "TrustAudit.lean",
        ):
            (target / filename).write_bytes((HERE / filename).read_bytes())
        for source in VENDOR.rglob("*"):
            if source.is_file():
                destination = vendor / source.relative_to(VENDOR)
                destination.parent.mkdir(parents=True, exist_ok=True)
                destination.write_bytes(source.read_bytes())
        (tmp / "home").mkdir()

        def lean_run(source: Path, module_path: str, root: Path, emit_olean: bool) -> str:
            argv = [str(lean), "--trust=0", "-t0", "-R", str(root)]
            if emit_olean:
                argv += ["-o", str(source.with_suffix(".olean"))]
            argv.append(str(source))
            env = {
                **BASE_ENV,
                "HOME": str(tmp / "home"),
                "TMPDIR": str(tmp),
                "LEAN_PATH": module_path,
            }
            return run(argv, cwd=tmp, env=env)

        statement = lean_run(target / "Statement.lean", lean_path, target, True)
        tree = lean_run(
            target / "ObligationTree.lean", f"{target}:{lean_path}", target, True
        )
        graph = lean_run(
            target / "GraphBridgeProof.lean", f"{target}:{lean_path}", target, True
        )
        vendor_outputs: list[str] = []
        for module in ("Gametheory.Scarf", "Gametheory.ScarfPath", "Gametheory.Brouwer"):
            source = vendor / Path(*module.split(".")).with_suffix(".lean")
            vendor_outputs.append(lean_run(source, f"{vendor}:{lean_path}", vendor, True))
        brouwer_source = lean_run(
            target / "BrouwerSource.lean", f"{target}:{vendor}:{lean_path}", target, True
        )
        proof = lean_run(
            target / "Proof.lean", f"{target}:{vendor}:{lean_path}", target, True
        )
        validation = lean_run(
            target / "Validation.lean", f"{target}:{lean_path}", target, False
        )
        trust = lean_run(
            target / "TrustAudit.lean", f"{target}:{vendor}:{lean_path}", target, False
        )
        for path in (
            target / "Statement.olean", target / "ObligationTree.olean",
            target / "GraphBridgeProof.olean", target / "BrouwerSource.olean",
            target / "Proof.olean", vendor / "Gametheory/Scarf.olean",
            vendor / "Gametheory/ScarfPath.olean", vendor / "Gametheory/Brouwer.olean",
        ):
            assert path.is_file() and path.stat().st_size > 0, path
        return {
            "statement": statement,
            "tree": tree,
            "graph": graph,
            "vendor": "".join(vendor_outputs),
            "brouwer_source": brouwer_source,
            "proof": proof,
            "validation": validation,
            "trust": trust,
        }


def assert_text_hygiene(path: Path) -> None:
    data = path.read_bytes()
    assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines()), path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--probe", action="store_true")
    args = parser.parse_args()
    verify_receipt = os.environ.get("STAGE1_SKIP_RECEIPT_CHECK") != "1"
    assert os.environ.get("STAGE1_OUTER_NETWORK_ISOLATED") == "1", (
        "the complete recorded recipe must run inside the network-denied Bubblewrap namespace"
    )

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    assert sha256(ROOT / "Docs/Stage1_Blueprint_rev-5.6.md") == BLUEPRINT_SHA256
    assert sha256(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json") == EXECUTION_DAG_SHA256
    assert sha256(ROOT / "Docs/Stage1_Targets_rev-5.6.json") == TARGET_MANIFEST_SHA256
    assert sha256(ROOT / "skills/execute-stage1-rev56/SKILL.md") == SKILL_SHA256

    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    targets = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item == {
        "id": ITEM, "theorem_id": THEOREM, "execution_rank": 686,
        "phase": "validation", "layer": 5, "state": "[ ]",
        "depends_on": ["S56-M-0320-PROOF"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Run hermetic kernel, trust, provenance, and independent validation gates.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0, "children": [],
    }
    predecessor = next(row for row in execution["items"] if row["id"] == "S56-M-0320-PROOF")
    assert predecessor["state"] == "[_]" and predecessor["attempts"] == 1
    for phase in ("INTAKE", "STATEMENT", "ANCHOR_AUDIT", "OBLIGATION_TREE", "PROOF"):
        row = next(r for r in execution["items"] if r["id"] == f"S56-M-0320-{phase}")
        assert row["state"] == "[_]"
    target_row = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target_row["execution_rank"] == 686 and target_row["baseline"] == "L0"
    assert target_row["rework_required"] is True and target_row["theorem_complete"] is False

    for name, expected in EXPECTED_INPUTS.items():
        assert sha256(HERE / name) == expected, f"stale validation input: {name}"
    for name, expected in VENDOR_INPUTS.items():
        assert sha256(SOURCE / name) == expected, f"stale vendor input: {name}"
    assert sha256(LEAN_ROOT / "lean-toolchain") == TOOLCHAIN_SHA256
    assert sha256(LEAN_ROOT / "lake-manifest.json") == MANIFEST_SHA256

    instance = load(HERE / "instance.json")
    tasks = load(HERE / "task-dag.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    frozen_specs = load(HERE / "validation-specs.json")
    proof_receipt = load(HERE / "proof-receipt.json")
    source_record = load(HERE / "brouwer-source.json")
    vendor_manifest = load(SOURCE / "vendor-manifest.json")
    assert instance["lifecycle"] == tasks["lifecycle"] == "planned"
    assert instance["root_vector"] == ACCEPTED_ROOT_VECTOR
    assert instance["accepted_proof_state"] == tasks["accepted_states"] == []
    assert instance["audit_complete"] is instance["theorem_complete"] is False
    assert next(row for row in tasks["tasks"] if row["id"].endswith("-PROOF"))["state"] == "open"
    assert registry["denominator_sha256"] == graphs["registry_denominator_sha256"] == REGISTRY_DENOMINATOR_SHA256
    assert registry["root_obligation_id"] == graphs["root_node_id"] == "M0320-ROOT"
    assert graphs["closure_boundary"]["closed_obligations"] == FROZEN_CLOSED
    assert graphs["closure_boundary"]["remaining_root_cut_set"] == FROZEN_OPEN_CUT
    assert graphs["closure_boundary"]["root_closed"] is False
    assert graphs["closure_boundary"]["audit_complete"] is False
    assert graphs["closure_boundary"]["theorem_complete"] is False
    assert frozen_specs["item_id"] == "S56-M-0320-OBLIGATION_TREE"
    assert len(frozen_specs["recipes"]) == 10
    assert all("command" in row and "argv" not in row for row in frozen_specs["recipes"])
    assert proof_receipt["item_id"] == "S56-M-0320-PROOF"
    assert proof_receipt["accepted"] is False and proof_receipt["proposed_state"] == "[_]"
    assert proof_receipt["proof_source_sha256"] == EXPECTED_INPUTS["Proof.lean"]
    assert proof_receipt["accepted_closed_obligation_ids"] == []
    assert proof_receipt["theorem_complete"] is False
    assert source_record["upstream"]["revision"] == UPSTREAM_REVISION
    assert source_record["upstream"]["tree"] == UPSTREAM_TREE
    assert source_record["upstream"]["archive_sha256"] == UPSTREAM_ARCHIVE_SHA256
    assert vendor_manifest["upstream"]["revision"] == UPSTREAM_REVISION
    assert vendor_manifest["upstream"]["source_tree"] == UPSTREAM_TREE
    assert vendor_manifest["upstream"]["source_archive_sha256"] == UPSTREAM_ARCHIVE_SHA256
    assert vendor_manifest["closure"]["normalized_compatibility_patch_sha256"] == COMPATIBILITY_PATCH_SHA256

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by|run_tac)\b|"
        r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
        r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
        r"(?:axiom|constant|opaque|unsafe|extern)\b",
        re.MULTILINE,
    )
    scanned = [
        HERE / name for name in (
            "Statement.lean", "ObligationTree.lean", "GraphBridgeProof.lean",
            "BrouwerSource.lean", "Proof.lean", "Validation.lean", "TrustAudit.lean",
        )
    ] + sorted(VENDOR.rglob("*.lean"))
    for path in scanned:
        clean = strip_lean(path.read_text(encoding="utf-8"))
        match = prohibited.search(clean)
        assert match is None, (path, match.group(0) if match else None)
    imports = (HERE / "Validation.lean").read_text(encoding="utf-8").split("/-!", 1)[0]
    assert "import Proof" not in imports and "import ObligationTree" not in imports
    assert "core : ClosedGraphKakutaniCore" in (HERE / "Validation.lean").read_text()

    manifest = load(LEAN_ROOT / "lake-manifest.json")
    mathlib_entry = next(row for row in manifest["packages"] if row["name"] == "mathlib")
    assert mathlib_entry["rev"] == mathlib_entry["inputRev"] == MATHLIB_REVISION
    assert mathlib_entry["url"] == MATHLIB_REMOTE
    mathlib = (LEAN_ROOT / ".lake/packages/mathlib").resolve()
    assert git("rev-parse", "HEAD", cwd=mathlib) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == MATHLIB_TREE
    assert git("remote", "get-url", "origin", cwd=mathlib) == MATHLIB_REMOTE
    assert git("status", "--porcelain=v1", "--untracked-files=all", cwd=mathlib) == ""
    assert sha256(mathlib / "LICENSE") == MATHLIB_LICENSE_SHA256
    for relative, expected in TRUST_SOURCE_BOUNDARIES.items():
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
    git_binary = Path("/usr/bin/git")
    elan_lake = Path(HOME) / ".elan/bin/lake"
    assert sha256(lean) == LEAN_SHA256 and sha256(lake) == LAKE_SHA256
    assert sha256(bwrap) == BWRAP_SHA256 and sha256(python) == PYTHON_SHA256
    assert sha256(git_binary) == GIT_SHA256 and sha256(elan_lake) == ELAN_LAUNCHER_SHA256
    assert LEAN_COMMIT in run([str(lean), "--version"], cwd=LEAN_ROOT, env=BASE_ENV)
    assert "5.0.0" in run([str(lake), "--version"], cwd=LEAN_ROOT, env=BASE_ENV)
    outputs = replay(lean, pinned_lean_path(lean))
    combined = "\n".join(outputs.values())
    assert "error:" not in combined.lower()
    assert "sorryAx" not in combined and "declaration uses 'sorry'" not in combined
    assert outputs["proof"].count("Declarations are sorry-free!") == 3
    assert outputs["validation"].count("Declarations are sorry-free!") == 3
    assert outputs["trust"].count("Declarations are sorry-free!") == 8
    for declaration in (*TREE_DECLARATIONS, *GRAPH_DECLARATIONS, *PROOF_DECLARATIONS):
        assert normalized_axioms(outputs["trust"], declaration) <= EXPECTED_AXIOMS
    assert normalized_axioms(
        outputs["trust"], "Stage1Instances.THM_M_0320.kakutaniFixedPoint"
    ) == EXPECTED_AXIOMS
    for declaration in VALIDATION_DECLARATIONS:
        assert normalized_axioms(outputs["validation"], declaration) <= EXPECTED_AXIOMS
    statement_sha = hashlib.sha256(outputs["statement"].encode()).hexdigest()
    observations = {
        "lean_output_sha256": {
            name: hashlib.sha256(output.encode()).hexdigest()
            for name, output in outputs.items()
        },
        "statement_print_stdout_sha256": statement_sha,
        "observed_axioms": sorted(EXPECTED_AXIOMS),
        "proof_sorry_free_reports": 3,
        "validation_sorry_free_reports": 3,
        "trust_audit_sorry_free_reports": 8,
    }
    if args.probe:
        print(json.dumps(observations, sort_keys=True))
        return

    if verify_receipt:
        spec = load(HERE / "validation-spec.json")
        receipt = load(HERE / "validation-receipt.json")
        packet = load(ROOT / ".stage1-worker-selftest.json")
        assert spec["schema_version"] == "stage1-validation-spec/1.0"
        assert spec["item_id"] == receipt["item_id"] == packet["item_id"] == ITEM
        assert spec["theorem_id"] == receipt["theorem_id"] == THEOREM
        assert spec["cwd"] == "." and spec["network_policy"] == "denied"
        assert spec["expected_exit"] == 0 and spec["timeout_seconds"] == 900
        assert spec["covered_obligation_ids"] == receipt["covered_obligation_ids"]
        assert spec["covered_declarations"] == receipt["covered_declarations"]
        assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
        assert receipt["support_state"] == "provisional_worker_selftest"
        assert receipt["proposed_state"] == packet["state"] == "[_]"
        assert receipt["accepted"] is receipt["release_grade"] is False
        assert receipt["verdict"] == "blocked"
        assert receipt["specification_sha256"] == sha256(HERE / "validation-spec.json")
        assert receipt["registry_sha256"] == EXPECTED_INPUTS["obligation-registry.json"]
        assert receipt["registry_denominator_sha256"] == REGISTRY_DENOMINATOR_SHA256
        assert receipt["canonical_target_source_fingerprint"] == (
            "lean-source:v1:sha256:" + EXPECTED_INPUTS["Statement.lean"]
        )
        assert receipt["canonical_target_expression_fingerprint"] is None
        assert receipt["observed_statement_print_stdout_sha256"] == statement_sha
        for key, name in (
            ("statement_source_sha256", "Statement.lean"),
            ("obligation_tree_source_sha256", "ObligationTree.lean"),
            ("graph_bridge_source_sha256", "GraphBridgeProof.lean"),
            ("brouwer_wrapper_source_sha256", "BrouwerSource.lean"),
            ("proof_source_sha256", "Proof.lean"),
            ("validation_probe_sha256", "Validation.lean"),
            ("instance_sha256", "instance.json"),
            ("task_dag_sha256", "task-dag.json"),
            ("anchor_audit_sha256", "anchor-audit.json"),
            ("obligation_registry_sha256", "obligation-registry.json"),
            ("typed_graphs_sha256", "typed-graphs.json"),
            ("frozen_validation_specs_sha256", "validation-specs.json"),
            ("proof_receipt_sha256", "proof-receipt.json"),
            ("brouwer_source_record_sha256", "brouwer-source.json"),
        ):
            assert receipt["inputs"][key] == sha256(HERE / name), key
        assert receipt["inputs"]["validator_sha256"] == sha256(HERE / "check_validation.py")
        assert receipt["inputs"]["validation_spec_sha256"] == sha256(HERE / "validation-spec.json")
        assert receipt["result"]["lean_output_sha256"] == observations["lean_output_sha256"]
        assert receipt["result"]["observed_axioms"] == observations["observed_axioms"]
        assert receipt["result"]["newly_accepted_closed_obligation_ids"] == []
        assert receipt["result"]["accepted_root_vector_before"] == ACCEPTED_ROOT_VECTOR
        assert receipt["result"]["accepted_root_vector_after"] == ACCEPTED_ROOT_VECTOR
        assert receipt["result"]["audit_complete"] is False
        assert receipt["result"]["theorem_complete"] is False
        assert receipt["first_failed_gate"] == "dependency.S56-M-0320-PROOF.master_acceptance"
        assert receipt["remaining_root_cut_set"] == FROZEN_OPEN_CUT
        assert set(receipt["changed_paths"]) == CHANGED_PATHS
        assert receipt["known_failures"] == packet["known_failures"]
        assert set(packet) == {
            "item_id", "changed_paths", "commands", "output_summary",
            "base_revision", "known_failures", "state",
        }
        assert packet["base_revision"] == BASE_REVISION
        assert set(packet["changed_paths"]) == CHANGED_PATHS
        actual = {
            line[3:] for line in git("status", "--short", "--untracked-files=all").splitlines()
        }
        actual.discard("Formalizations/Lean/.lake")
        assert actual == CHANGED_PATHS, (actual, CHANGED_PATHS)
        started = datetime.fromisoformat(receipt["validation_started_at"])
        ended = datetime.fromisoformat(receipt["validation_ended_at"])
        assert started <= ended and receipt["validated_at"] == receipt["validation_ended_at"]
        assert receipt["evidence_log"] == {
            "stream": "stdout",
            "bytes": len(EXPECTED_SUMMARY),
            "sha256": hashlib.sha256(EXPECTED_SUMMARY).hexdigest(),
            "exit_code": 0,
            "archive_classification": "deterministic nonrelease semantic log digest; transient raw log is not a release archive",
        }

    for relative in CHANGED_PATHS - {".stage1-worker-selftest.json"}:
        path = ROOT / relative
        if path.exists():
            assert_text_hygiene(path)
    print(EXPECTED_SUMMARY.decode(), end="", flush=True)


if __name__ == "__main__":
    main()
