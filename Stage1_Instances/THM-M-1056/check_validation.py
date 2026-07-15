#!/usr/bin/env python3
"""Fail-closed narrow validator for S56-M-1056-VALIDATION."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import re
import shutil
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-1056"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
ITEM = "S56-M-1056-VALIDATION"
THEOREM = "THM-M-1056"
BASE_REVISION = "4c1d50aa6552eb6ec56338a663a5dff79a4ae2e3"
BASE_TREE = "e38ee217e0bb768c5c915905d1d0b04fc89e25f2"
TOOLCHAIN = "leanprover/lean4:v4.29.0"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
LEAN_SHA256 = "3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf"
LAKE_SHA256 = "a608ff084d7e2af228b92a29d7c2fd083ba0580e46889175ec74a81678c98359"
BWRAP_SHA256 = "0abea81db798ebf6b4742ac0664802d97521547a353c2a0dbdc21d76cbbfd2c0"
PYTHON_SHA256 = "b8d8288faefdd300201f43fcf00f6f539a27218eeed3a3dff5ab10b9c4c99700"
GIT_SHA256 = "5516c9f362c29376ab9a499a33082f9f611941d8c75930c880e30ad109e39c9a"
PATCH_SHA256 = "44ecd416d1958be9c2b60488fa893e76aae8d0f81d2fedb9e83eb661da0ee18c"
TOOLCHAIN_SHA256 = "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2"
LAKE_MANIFEST_SHA256 = "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MATHLIB_REMOTE = "https://github.com/leanprover-community/mathlib4.git"
MATHLIB_LICENSE_SHA256 = "b40930bbcf80744c86c46a12bc9da056641d722716c378f5659b9e555ef833e1"
EXPRESSION_SHA256 = "8e1a96a304ce3dd43838f934406d58ac3594b9d34c6e1617461abc17e65d403b"
DENOMINATOR_SHA256 = "5246a9d5966e76ff5cb379c8f39f48100fafd3c2ce99bf7c7e10f953f8b57828"
UPSTREAM_REVISION = "ed3fa6b8a30594eeb791160563942ba115581aa0"
UPSTREAM_ARCHIVE_SHA256 = "3c0ef177500430ab55950061cfd73991347f5336b5b3d5032ffe46ac56009a52"
LICENSE_SHA256 = "cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30"
PORT_PATCH_SHA256 = "7984d9e0199f8cbd1540d6fa8411bd931b79ea3431ae4acb0fbe534594d9c529"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
ROOT_VECTOR = {"H": "H1", "M": "M3", "R": "R3"}
OPEN_ROOT_CUT = ["M1056-T-CORE"]

WRAPPER_MODULES = (
    "Statement",
    "CoordinateBridge",
    "IntegrabilityBridge",
    "CocycleBridge",
    "GrowthBridge",
    "ExternalInvoke",
    "ConditionalWrapper",
    "M1056ProjectionBridge",
    "ConcreteProjectionPackage",
    "Proof",
)
AUDITED_DECLARATIONS = (
    "ErgodicTheory.oseledets_splitting",
    "Stage1Instances.THM_M_1056.external_oseledets_on_arbitrary_fiber_coordinates",
    "Stage1Instances.THM_M_1056.measurableObliqueProjectionPackage",
    "Stage1Instances.THM_M_1056.oseledets_multiplicative_ergodic_target",
    "Stage1Instances.THM_M_1056.oseledetsMultiplicativeErgodic",
    "Stage1Instances.THM_M_1056.oseledetsMultiplicativeErgodicTarget",
)
MACHINE_IDS = [
    "M1056-ROOT",
    "M1056-S-INTERFACE",
    "M1056-S-BOUNDARY",
    "M1056-S-FOUNDATION",
    "M1056-N-ITERATES",
    "M1056-N-COORDINATES",
    "M1056-L-SUBADDITIVE",
    "M1056-L-KINGMAN",
    "M1056-C-FORWARD-FLAG",
    "M1056-C-BACKWARD-FLAG",
    "M1056-L-TRANSVERSAL",
    "M1056-C-PROJECTIONS",
    "M1056-L-EQUIVARIANCE",
    "M1056-L-GROWTH",
    "M1056-T-CORE",
    "M1056-T-ASSEMBLE",
    "M1056-X-EXTERNAL",
]
EXPECTED_INPUTS = {
    "Statement.lean": "00c1ca022adb35d49369df14a420b64b4c7b77f1fe8858aba85d4df0793f3886",
    "AnchorAudit.lean": "23ec9b11a64f02426a34e7cd2a0c7ee0270f25a65215c838e66176de453ffd3a",
    "ObligationTree.lean": "4286d31290c2df8d1535cd9d58d6574ad0dad1b828fb58a78b5be3c3a5b3647c",
    "CoordinateBridge.lean": "e6f25b00d29866b941800c54ccca55f90062668db3ae6be0c47a8bd88cd2a54f",
    "IntegrabilityBridge.lean": "f5b60155ac6155675f02f99936f6f90eade49d1b914e8901d3e2c559722ee1a6",
    "CocycleBridge.lean": "1b6b625b6a7bf0c1743bfe9b81c98b8185f0eeeb8ce5101cf5679b6792da2e4c",
    "GrowthBridge.lean": "5e73b7bc91c53ec6be8e5dd72784a69f93673fb8ac2b7ecb4cbba68b924505be",
    "ExternalInvoke.lean": "10b44fd12426d6fababe600133ad12d1b5c64ad0ab5f50ee98f40ca88a64621d",
    "ConditionalWrapper.lean": "1c9440d1f7cd486e410b618b8ae00959653426b1f0c22e309de95e9f6d96136f",
    "M1056ProjectionBridge.lean": "8c8dae2a327fa0cb90857a71d3c2e06238a65cd550a338011a514acd03ba9bf8",
    "ConcreteProjectionPackage.lean": "fa73c27bf0040e648bc1802a4eaa31fecacad25d2db1711eb0567fc76eab31b2",
    "Proof.lean": "e93f37d77807b8e7f8ac027f45955186159cd4a1e2370d1609f1f6bad05a2a69",
    "statement.json": "7835415516fd94c870bda3b54ca9e3a14e83785e6dd6cb9ea34fc2b5acb08bf3",
    "anchor-audit.json": "9cc94971f4c40cdfff42ea61b07790868b4bc4f2f5f324862457b47aba37ae04",
    "obligation-registry.json": "281d9dcd7ede39aa609c30a42649f57b14b7886d46ca9d0c767a626577316476",
    "typed-graphs.json": "50903cbdbc7208ff4d6282421fabcb9661e4575fb1298210d631b84ca468b477",
    "validation-specs.json": "a121b4549a4f48a3b472b067e4c9db7a2f8148d1f04db38352fd91bb2d2c8509",
    "proof-receipt.json": "c9916f9c13eb16561b0e66d216ff22ce2b32324d5435f49ee6a9e9eef8d901a7",
    "check_proof.py": "84fef139e53de35c382ccb9d32cd21634e265678dcf571e012bb5a3aef061348",
    "check_proof.sh": "ccf9716aca3d70274729552ef7ab4a02b79415d6439d0792e81670dc7705d148",
    "check_vendor.py": "cbf0f23b6818d75a42586ed38813cb36ff444a04bd2065e5951ec63bbd6ea1e1",
    "vendor-manifest.json": "9a5a40b26cad81ee0430a326e112205b2e4a95bcb9d3911e65150025384c9679",
    "VENDOR_PROVENANCE.md": "86d1b09f42556f4deb5fe32cb87998e4782db34a6a0a100ee8c00a0e4115ca13",
    "source_statement_crosswalk.md": "8ef07ef7dce3a99e1218b6461a7375a455124c05a5cd145cb27f955553841bbe",
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
    "PASS kernel replay: 62 vendored modules and 11 target/probe modules rebuilt from copied source at Lean trust zero",
    "PASS exact target: both public root names inhabit the unchanged frozen Oseledets target",
    "PASS trust observation: six audited declarations are sorry-free and use exactly propext, Classical.choice, and Quot.sound",
    "PASS source hygiene: 73 active Lean inputs contain no prohibited placeholder, bodyless, unsafe, or oracle construct",
    "PASS selected provenance: vendor hashes, reversible port, upstream pin, licenses, tool identities, and clean mathlib pin agree",
    "OPEN authority reconciliation: the frozen graph remains H1/M3/R3 with cut M1056-T-CORE and no accepted closed obligation",
    "FAIL CLOSED predecessor gate: S56-M-1056-PROOF is worker-provisional and not master-accepted",
    "FAIL CLOSED complete trust/provenance: accepted foundation policy, node/body graph, transitive TCB/SBOM, H0, and R0 are absent",
    "FAIL CLOSED cold hermetic gate: shared warm pinned artifacts are not an empty-cache offline bootstrap",
    "FAIL CLOSED independent gate: this same-worker replay is not a distinct signed runner or independent minimal verifier",
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
    timeout: int = 2700,
) -> str:
    result = subprocess.run(
        argv, cwd=cwd, env=env, text=True, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, timeout=timeout, check=False,
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
    in_char = False
    escaped = False
    while index < len(source):
        pair = source[index:index + 2]
        char = source[index]
        if depth:
            if pair == "/-":
                depth += 1
                output.extend("  ")
                index += 2
            elif pair == "-/":
                depth -= 1
                output.extend("  ")
                index += 2
            else:
                output.append("\n" if char == "\n" else " ")
                index += 1
            continue
        if in_string or in_char:
            output.append("\n" if char == "\n" else " ")
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif in_string and char == '"':
                in_string = False
            elif in_char and char == "'":
                in_char = False
            index += 1
            continue
        if pair == "/-":
            depth = 1
            output.extend("  ")
            index += 2
        elif pair == "--":
            end = source.find("\n", index)
            end = len(source) if end < 0 else end
            output.extend(" " * (end - index))
            index = end
        elif char == '"':
            in_string = True
            output.append(" ")
            index += 1
        elif char == "'" and index + 2 < len(source) and source[index + 2] == "'":
            in_char = True
            output.append(" ")
            index += 1
        else:
            output.append(char)
            index += 1
    assert depth == 0 and not in_string and not in_char, "unterminated Lean comment/string"
    return "".join(output)


def reported_axioms(output: str, declaration: str) -> set[str]:
    pattern = re.compile(
        re.escape(f"'{declaration}' depends on axioms: [") + r"(.*?)]", re.DOTALL
    )
    matches = pattern.findall(output)
    assert len(matches) == 1, f"missing or duplicate axiom report for {declaration}"
    return {part.strip() for part in matches[0].split(",") if part.strip()}


def pinned_lake_and_path() -> tuple[Path, Path, str]:
    lean = Path(run(["lake", "env", "which", "lean"], cwd=LEAN_ROOT, env=BASE_ENV).strip())
    lake = lean.with_name("lake")
    lean_path = run(
        ["lake", "env", "printenv", "LEAN_PATH"], cwd=LEAN_ROOT, env=BASE_ENV
    ).strip()
    roots = [Path(part).resolve() for part in lean_path.split(":") if Path(part).is_dir()]
    assert roots and any("mathlib" in path.parts for path in roots), roots
    return lean, lake, ":".join(str(path) for path in roots)


def isolated_replay(lake: Path, lean_path: str, order: list[str]) -> dict:
    with tempfile.TemporaryDirectory(prefix="stage1-m1056-validation-", dir="/tmp") as tmp_name:
        tmp = Path(tmp_name).resolve()
        vendor_source = tmp / "vendor"
        wrapper_source = tmp / "wrapper"
        external_out = tmp / "build" / "external"
        wrapper_out = tmp / "build" / "wrapper"
        home = tmp / "home"
        shutil.copytree(HERE / "External" / "Oseledets", vendor_source)
        wrapper_source.mkdir()
        external_out.mkdir(parents=True)
        wrapper_out.mkdir(parents=True)
        home.mkdir()
        for module in WRAPPER_MODULES:
            shutil.copy2(HERE / f"{module}.lean", wrapper_source / f"{module}.lean")
        shutil.copy2(HERE / "Validation.lean", wrapper_source / "Validation.lean")
        assert not list(tmp.rglob("*.olean"))

        base = [
            "/usr/bin/bwrap", "--ro-bind", "/", "/", "--bind", str(tmp), str(tmp),
            "--dev", "/dev", "--proc", "/proc", "--unshare-net", "--die-with-parent",
            "--clearenv", "--setenv", "HOME", str(home), "--setenv", "TMPDIR", str(tmp),
            "--setenv", "LANG", "C.UTF-8", "--setenv", "LC_ALL", "C.UTF-8",
            "--setenv", "TZ", "UTC", "--setenv", "LEAN_NUM_THREADS", "1",
            "--setenv", "ELAN_TOOLCHAIN", TOOLCHAIN, "--chdir", str(LEAN_ROOT),
        ]
        combined_parts: list[str] = []
        outputs: dict[str, str] = {}

        def compile_module(
            label: str, module_root: Path, output: Path, source: Path, module_path: str
        ) -> str:
            output.parent.mkdir(parents=True, exist_ok=True)
            argv = base + [
                "--setenv", "LEAN_PATH", module_path, str(lake), "env", "lean",
                "--trust=0", "-t0", "-R", str(module_root), "-o", str(output), str(source),
            ]
            result = run(argv, env=BASE_ENV, timeout=900)
            assert output.is_file() and output.stat().st_size > 0
            combined_parts.append(f"[compile] {label}\n{result}")
            outputs[label] = result
            return result

        for index, module in enumerate(order, 1):
            relative = Path(*module.split("."))
            compile_module(
                f"external {index}/62 {module}", vendor_source,
                external_out / relative.with_suffix(".olean"),
                vendor_source / relative.with_suffix(".lean"),
                f"{external_out}:{lean_path}",
            )
        wrapper_outputs: dict[str, str] = {}
        for module in WRAPPER_MODULES:
            wrapper_outputs[module] = compile_module(
                f"target {module}", wrapper_source, wrapper_out / f"{module}.olean",
                wrapper_source / f"{module}.lean",
                f"{wrapper_out}:{external_out}:{lean_path}",
            )
        validation_output = compile_module(
            "target Validation", wrapper_source, wrapper_out / "Validation.olean",
            wrapper_source / "Validation.lean", f"{wrapper_out}:{external_out}:{lean_path}",
        )
        assert len(list(external_out.rglob("*.olean"))) == 62
        assert len(list(wrapper_out.glob("*.olean"))) == 11
        assert not list(HERE.rglob("*.olean"))

        terminal = external_out / "ErgodicTheory" / "TwoSided" / "SplittingAssembly.olean"
        proof = wrapper_out / "Proof.olean"
        combined = "".join(combined_parts)
        normalized_combined = combined.replace(str(tmp), "$REPLAY_ROOT")
        return {
            "combined_output_sha256": hashlib.sha256(normalized_combined.encode()).hexdigest(),
            "combined_output_bytes": len(normalized_combined.encode()),
            "validation_output_sha256": hashlib.sha256(validation_output.encode()).hexdigest(),
            "validation_output_bytes": len(validation_output.encode()),
            "terminal_olean_sha256": sha256(terminal),
            "proof_olean_sha256": sha256(proof),
            "external_olean_aggregate_sha256": hashlib.sha256(
                "".join(
                    f"{path.relative_to(external_out).as_posix()} {sha256(path)}\n"
                    for path in sorted(external_out.rglob("*.olean"))
                ).encode()
            ).hexdigest(),
            "wrapper_olean_aggregate_sha256": hashlib.sha256(
                "".join(
                    f"{path.relative_to(wrapper_out).as_posix()} {sha256(path)}\n"
                    for path in sorted(wrapper_out.glob("*.olean"))
                ).encode()
            ).hexdigest(),
            "external_module_count": 62,
            "target_module_count": 11,
            "module_outputs": outputs,
            "validation_output": validation_output,
        }


def assert_static_inputs() -> tuple[dict, dict, dict, dict, dict]:
    execution = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")
    targets = load(ROOT / "Docs" / "Stage1_Targets_rev-5.6.json")
    statement = load(HERE / "statement.json")
    anchor = load(HERE / "anchor-audit.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    proof_receipt = load(HERE / "proof-receipt.json")
    manifest = load(HERE / "vendor-manifest.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 248 and target["baseline"] == "L0"
    assert target["lifecycle_mode"] == "planned"
    assert target["rework_required"] is True and target["theorem_complete"] is False
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item == {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 248,
        "phase": "validation",
        "layer": 5,
        "state": "[ ]",
        "depends_on": ["S56-M-1056-PROOF"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Run hermetic kernel, trust, provenance, and independent validation gates.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }
    predecessor = next(row for row in execution["items"] if row["id"] == "S56-M-1056-PROOF")
    assert predecessor["state"] == "[_]" and predecessor["attempts"] == 1

    for name, expected in EXPECTED_INPUTS.items():
        assert sha256(HERE / name) == expected, f"stale validation input: {name}"
    assert sha256(LEAN_ROOT / "lean-toolchain") == TOOLCHAIN_SHA256
    assert sha256(LEAN_ROOT / "lake-manifest.json") == LAKE_MANIFEST_SHA256
    formal = statement["canonical_formal_target"]
    assert formal["declaration_or_expression"] == (
        "Stage1Instances.THM_M_1056.OseledetsMultiplicativeErgodicTarget"
    )
    assert formal["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert formal["statement_file_sha256"] == EXPECTED_INPUTS["Statement.lean"]
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert registry["frozen_denominators"]["required_machine"] == MACHINE_IDS
    assert len(registry["obligations"]) == 19
    assert graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    closure = graphs["closure_boundary"]
    assert closure["root_closed"] is False and closure["theorem_complete"] is False
    assert closure["remaining_root_cut_set"] == OPEN_ROOT_CUT
    graph_root = next(node for node in graphs["nodes"] if node["obligation_id"] == "M1056-ROOT")
    assert {
        "H": graph_root["human_debt"],
        "M": graph_root["machine_debt"],
        "R": graph_root["readability_debt"],
    } == ROOT_VECTOR

    assert proof_receipt["item_id"] == "S56-M-1056-PROOF"
    assert proof_receipt["accepted"] is False and proof_receipt["proposed_state"] == "[_]"
    assert proof_receipt["canonical_target_expression_sha256"] == EXPRESSION_SHA256
    assert proof_receipt["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert proof_receipt["kernel_inhabited_obligation_ids_observed"] == ["M1056-ROOT"]
    assert proof_receipt["closed_obligation_ids_proposed"] == []
    assert proof_receipt["accepted_closed_obligation_ids"] == []
    assert proof_receipt["root_vector_before"] == proof_receipt["root_vector_after"] == ROOT_VECTOR
    assert proof_receipt["graph_reconciliation_pending"]["required"] is True
    assert anchor["external_lean4"]["integration_status"] == "blocked_not_attempted"
    assert anchor["classification"] == {
        "human": "H1",
        "machine": "M3",
        "readability": "R3",
        "evidence_class": "E3",
        "reason": anchor["classification"]["reason"],
    }
    assert manifest["upstream"]["revision"] == UPSTREAM_REVISION
    assert manifest["upstream"]["source_archive_sha256"] == UPSTREAM_ARCHIVE_SHA256
    assert manifest["license"]["sha256"] == LICENSE_SHA256
    assert manifest["compatibility_port"]["patch_sha256"] == PORT_PATCH_SHA256
    assert manifest["closure"]["module_count"] == 62

    old_specs = load(HERE / "validation-specs.json")
    assert old_specs["item_id"] == "S56-M-1056-OBLIGATION_TREE"
    assert all(isinstance(row.get("command"), str) for row in old_specs["recipes"])
    assert all("argv" not in row for row in old_specs["recipes"])
    return registry, graphs, proof_receipt, manifest, anchor


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--probe", action="store_true")
    parser.add_argument("--worker-packet", type=Path)
    args = parser.parse_args()

    registry, graphs, proof_receipt, manifest, anchor = assert_static_inputs()
    vendor_output = run(["python3", "-I", "-B", str(HERE / "check_vendor.py")])
    assert "PASS THM-M-1056 vendor closure" in vendor_output

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by|run_tac|oracle)\b|"
        r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
        r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
        r"(?:axiom|constant|opaque|unsafe|extern)\b",
        flags=re.MULTILINE,
    )
    active_sources = [HERE / f"{module}.lean" for module in WRAPPER_MODULES]
    active_sources.append(HERE / "Validation.lean")
    active_sources.extend(
        HERE / "External" / "Oseledets" / row["path"] for row in manifest["files"]
    )
    assert len(active_sources) == 73
    for path in active_sources:
        source = source_without_comments_and_strings(path.read_text(encoding="utf-8"))
        assert prohibited.search(source) is None, path

    lake_manifest = load(LEAN_ROOT / "lake-manifest.json")
    mathlib_entry = next(row for row in lake_manifest["packages"] if row["name"] == "mathlib")
    assert mathlib_entry["rev"] == mathlib_entry["inputRev"] == MATHLIB_REVISION
    assert mathlib_entry["url"] == MATHLIB_REMOTE
    assert (LEAN_ROOT / ".lake").is_symlink()
    mathlib = (LEAN_ROOT / ".lake/packages/mathlib").resolve()
    assert git("rev-parse", "HEAD", cwd=mathlib) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == MATHLIB_TREE
    assert git("status", "--porcelain=v1", "--untracked-files=no", cwd=mathlib) == ""
    assert git("remote", "get-url", "origin", cwd=mathlib) == MATHLIB_REMOTE
    assert sha256(mathlib / "LICENSE") == MATHLIB_LICENSE_SHA256

    lean, lake, lean_path = pinned_lake_and_path()
    assert sha256(lean) == LEAN_SHA256 and sha256(lake) == LAKE_SHA256
    assert sha256(Path("/usr/bin/bwrap")) == BWRAP_SHA256
    assert sha256(Path("/usr/bin/python3").resolve()) == PYTHON_SHA256
    assert sha256(Path("/usr/bin/git")) == GIT_SHA256
    assert sha256(Path("/usr/bin/patch")) == PATCH_SHA256
    assert LEAN_COMMIT in run([str(lake), "env", "lean", "--version"], cwd=LEAN_ROOT, env=BASE_ENV)
    assert "5.0.0-src+98dc76e" in run([str(lake), "--version"], env=BASE_ENV)
    assert "bubblewrap 0.11.1" in run(["/usr/bin/bwrap", "--version"], env=BASE_ENV)

    order = (HERE / "External" / "Oseledets" / "order.txt").read_text().splitlines()
    assert order == manifest["build_order"] and len(order) == 62
    observation = isolated_replay(lake, lean_path, order)
    output = observation["validation_output"]
    assert output.count("Declarations are sorry-free!") == len(AUDITED_DECLARATIONS)
    assert "declaration uses 'sorry'" not in output and "error:" not in output.lower()
    proof_output = observation["module_outputs"]["target Proof"]
    assert proof_output.count("Declarations are sorry-free!") == 1
    assert reported_axioms(
        proof_output, "Stage1Instances.THM_M_1056.oseledetsMultiplicativeErgodic"
    ) == EXPECTED_AXIOMS
    for declaration in AUDITED_DECLARATIONS:
        assert reported_axioms(output, declaration) == EXPECTED_AXIOMS
    closure_match = re.search(
        r"VALIDATION_CLOSURE roots=(\d+) declarations=(\d+) modules=(\d+)", output
    )
    assert closure_match is not None and int(closure_match.group(1)) == 6
    assert "VALIDATION_CLOSURE axioms=[propext, Classical.choice, Quot.sound]" in output
    assert "VALIDATION_CLOSURE bodyless_nonaxioms=[]" in output
    assert "VALIDATION_CLOSURE unsafe=[]" in output
    observation["observed_axioms"] = sorted(EXPECTED_AXIOMS)
    observation["closure"] = {
        "roots": 6,
        "declarations": int(closure_match.group(2)),
        "modules": int(closure_match.group(3)),
        "bodyless_nonaxioms": [],
        "unsafe": [],
    }
    observation["platform"] = f"{platform.system()} {platform.release()} {platform.machine()}"
    observation["vendor_check_output_sha256"] = hashlib.sha256(vendor_output.encode()).hexdigest()
    observation["vendor_check_output_bytes"] = len(vendor_output.encode())
    del observation["module_outputs"]
    del observation["validation_output"]
    if args.probe:
        print(json.dumps(observation, sort_keys=True))
        return

    spec = load(HERE / "validation-spec.json")
    receipt = load(HERE / "validation-receipt.json")
    blocker = load(HERE / "validation-blocker.json")
    packet_path = (args.worker_packet or ROOT / ".stage1-worker-selftest.json").resolve()
    packet = load(packet_path)
    assert spec["schema_version"] == "stage1-validation-spec/1.0"
    assert spec["item_id"] == receipt["item_id"] == blocker["item_id"] == packet["item_id"] == ITEM
    assert spec["theorem_id"] == receipt["theorem_id"] == blocker["theorem_id"] == THEOREM
    assert spec["depends_on"] == receipt["depends_on"] == ["S56-M-1056-PROOF"]
    assert len(spec["recipes"]) == 1 and spec["recipes"][0] == receipt["recipe"]
    recipe = spec["recipes"][0]
    assert recipe["cwd"] == "." and recipe["argv"] == [
        "python3", "-I", "-B", f"Stage1_Instances/{THEOREM}/check_validation.py",
        "--worker-packet", ".stage1-worker-selftest.json",
    ]
    assert recipe["timeout_seconds"] == 2700 and recipe["network_policy"] == "denied"
    assert recipe["expected_exit"] == 0 and recipe["covered_obligation_ids"] == MACHINE_IDS
    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["phase"] == "validation" and receipt["intent"] == "validate"
    assert receipt["base_revision"] == blocker["base_revision"] == packet["base_revision"] == BASE_REVISION
    assert receipt["base_tree"] == blocker["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["verdict"] == "blocked" and receipt["release_grade"] is False
    assert receipt["canonical_target_expression_sha256"] == EXPRESSION_SHA256
    assert receipt["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert receipt["covered_obligation_ids"] == MACHINE_IDS
    assert receipt["accepted_closed_obligation_ids"] == []
    assert receipt["result"]["root_kernel_inhabitant_observed"] is True
    assert receipt["result"]["accepted_root_closed"] is False
    assert receipt["result"]["validation_complete"] is False
    assert receipt["result"]["hermetic_cold_offline_replay"] == "fail_closed"
    assert receipt["result"]["independent_distinct_runner"] == "fail_closed"
    assert receipt["result"]["audit_complete"] is receipt["result"]["theorem_complete"] is False
    assert receipt["remaining_root_cut_set"] == OPEN_ROOT_CUT
    for key in (
        "combined_output_sha256", "combined_output_bytes", "validation_output_sha256",
        "validation_output_bytes", "terminal_olean_sha256", "proof_olean_sha256",
        "external_olean_aggregate_sha256", "wrapper_olean_aggregate_sha256",
        "external_module_count", "target_module_count", "observed_axioms", "closure",
        "platform", "vendor_check_output_sha256", "vendor_check_output_bytes",
    ):
        assert receipt["result"][key] == observation[key], key
    assert receipt["inputs"]["check_validation.py"] == sha256(HERE / "check_validation.py")
    assert receipt["inputs"]["Validation.lean"] == sha256(HERE / "Validation.lean")
    assert receipt["inputs"]["validation-spec.json"] == sha256(HERE / "validation-spec.json")
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
    assert packet["commands"] == receipt["commands"]
    assert packet["output_summary"] == receipt["output_summary"]
    status = git("status", "--short", "--untracked-files=all")
    actual = [line[3:] for line in status.splitlines() if line[3:] != "Formalizations/Lean/.lake"]
    assert sorted(actual) == sorted(CHANGED_PATHS), (actual, CHANGED_PATHS)
    for relative in CHANGED_PATHS:
        data = (ROOT / relative).read_bytes()
        assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())
    for path in (HERE / "validation-receipt.json", HERE / "validation-phase.md"):
        text = path.read_text(encoding="utf-8")
        assert "/home/" not in text and ".cron/" not in text
        assert "theorem_complete=true" not in text

    for line in SUMMARY_LINES:
        print(line)


if __name__ == "__main__":
    main()
