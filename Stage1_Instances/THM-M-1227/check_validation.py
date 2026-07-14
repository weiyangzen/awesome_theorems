#!/usr/bin/env python3
"""Fail-closed narrow validation for S56-M-1227-VALIDATION."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime
from pathlib import Path
import platform
import re
import shutil
import subprocess
import sys
import tempfile


if not __debug__:
    raise SystemExit("check_validation.py must run without Python optimization")


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-1227"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"

ITEM = "S56-M-1227-VALIDATION"
THEOREM = "THM-M-1227"
BASE_REVISION = "a1a7e939e58f103f5ff5d23af51437fa8658aa04"
BASE_TREE = "d881fd9641fa3e5f3ebe5082b35672981e90adcf"
STATEMENT_SHA256 = "ee8e2db1ef14b921333b55bb8e821d0c17fabdd0d295597205f932abecf4059b"
EXPRESSION_SHA256 = "9c937d18171ee1e302da926183a828ff4f60033685be1f71f5578c46bccd185b"
DENOMINATOR_SHA256 = "ace8d258d4f8205d28cccaf6f5a7d49b26ec069b08dbe407660bd46d7cc63dff"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MATHLIB_REMOTE = "https://github.com/leanprover-community/mathlib4.git"
LEAN_TOOLCHAIN_SHA256 = "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2"
LAKE_MANIFEST_SHA256 = "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81"
LEAN_EXECUTABLE_SHA256 = "3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf"
LAKE_EXECUTABLE_SHA256 = "840179e70803ef373c2ec53342d6a45ea7d022533e4145489fc1278b4f716385"
PYTHON_EXECUTABLE_SHA256 = "b8d8288faefdd300201f43fcf00f6f539a27218eeed3a3dff5ab10b9c4c99700"
GIT_EXECUTABLE_SHA256 = "8a48eefa306b9a2a9c3e576784a74ad7485779279e5a46ec43361a1864760e45"
BWRAP_EXECUTABLE_SHA256 = "0abea81db798ebf6b4742ac0664802d97521547a353c2a0dbdc21d76cbbfd2c0"
LICENSE_SHA256 = "b40930bbcf80744c86c46a12bc9da056641d722716c378f5659b9e555ef833e1"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
LEAN_MODULES = ("Statement.lean", "Proof.lean", "Validation.lean")

EXPECTED_INPUTS = {
    "Statement.lean": STATEMENT_SHA256,
    "Proof.lean": "f6f03cbf4cc61927cea5a175c7afa1fbc314a27d423598a75f1b228a7f16cabb",
    "Validation.lean": "8199394074782dfb56abc75ea8e6520555ffc4622b3452b1820aa532c742018b",
    "instance.json": "42701e3ea938ead3abfd0f8f4f65d30c4211bab1ca36a6295d8dfc199255a58c",
    "task-dag.json": "237b51f2770ac0475264e5fdc1d27a0c412cef54c15965a5c41d677cb61c0ee3",
    "anchor-audit.json": "069b66d6772ccc9ae3b3ef9001ac731255a40bb29b987d89759c08db69c664e6",
    "obligation-registry.json": "e34f878ce8d28069c162520557363410819832382c05f86879c9d629400dda31",
    "typed-graphs.json": "ed22b83ad7493b8505eb05cc9303cafc95db5a5d1ab7c11c44cf1d4d9837f232",
    "proof-receipt.json": "63910c5b76bde8135dabf8ed8090603ce7453be3b8766fcda6598b8d6d4b08e7",
    "proof-blocker.json": "e51e6902b594b1fd7aa90d78852b94bcd17fa27ebe32f49f46c27a7a5881f419",
    "validation-specs.json": "34544b2fba3b5b36c5ce965602f16c71a848b6c730cf8f5311a5757148ed2ad3",
    "scope-map.md": "a7b08c0072409dd00285e357e87b90194d3ec706191e419463e422ef92340f29",
    "source-statement-crosswalk.md": "220ef3f7050df62ff11b5b76d9fcdcbfafa486b486580d80bb8003720e56e11b",
    "statement.md": "8cb06eddabf40058da5f8f463c6599138108d8cdb564087c0eb50432c2ba9d13",
    "validation-spec.json": "f0031d7b77dce5b4f99a14cc49a044750bf6d0f86a22c186ad993f06fe00e4b6",
}

PINNED_IMPORTS = {
    "Mathlib/Analysis/Calculus/ContDiff/Basic.lean": {
        "source_blob": "e0ad3b97537a731639b45d1a0d47bacff40a5129",
        "source_sha256": "c3da4bad51dbed2870e5a92284953176992b5a04bc959a4c3284f63411ad52d4",
        "olean_sha256": "b2d73b6e964ed930bc8db763568dea3578ba0b60808a6f59b8b8055e6ec66b1e",
    },
    "Mathlib/MeasureTheory/Integral/Bochner/Basic.lean": {
        "source_blob": "587ad1e81dc387ba2835c29c4ef7aa05c5efd82e",
        "source_sha256": "b2e4b3eb233147e1dc8d2cb8fa4eae1773badbf1e37234dd7e8dfd54d9dd0a0a",
        "olean_sha256": "9d3ef22d441b3cf3b125673f3fe33411eb7d39f131548793f43d7041224082da",
    },
    "Mathlib/MeasureTheory/Measure/Lebesgue/EqHaar.lean": {
        "source_blob": "315139bd21407b2f5170bd789f287181d54e261b",
        "source_sha256": "b67b9e4928958783e9c57c3d61c37ab106adc9f3395f99221fde6f1e7b457f0c",
        "olean_sha256": "480eec6cdf4317e0f8f6b2a9b0255aadc416d80828862b8b273566cf46346d96",
    },
}

AXIOM_DECLARATIONS = {
    "Statement.lean": ("isLerayHopfSolution_compose",),
    "Proof.lean": (
        "zero_isLerayHopfSolution",
        "lerayHopfExistence_of_eq_zero",
    ),
    "Validation.lean": (
        "zero_isLerayHopfSolution_direct",
        "lerayHopfExistence_of_eq_zero_direct",
    ),
}

SUMMARY_LINES = (
    "PASS THM-M-1227 narrow validation",
    "PASS network-isolated trust-zero replay: frozen statement, conditional composer, proof zero branch, and differential zero branch elaborated",
    "PASS hygiene: kernel sorry checks and supplemental comment-stripped prohibited-construct scan passed for the hash-bound owned sources",
    "PASS trust observation: five checked declarations use exactly propext, Classical.choice, and Quot.sound",
    "PASS selected provenance: target hashes, denominator, clean mathlib pin/tree/remote, three direct import source/blob/olean identities, license, and Lean binary agree",
    "FAIL CLOSED authority/root: proof predecessor is only provisional, B-ZERO has a planned fingerprint, and the five-node general-data cut leaves the exact root at M4",
    "FAIL CLOSED source fidelity: primary theorem/page review is open and target-local scope prose disagrees with the frozen 3D unforced strong-trace Prop",
    "FAIL CLOSED complete trust/hermeticity: selected direct imports and a shared warm cache are not a transitive TCB/SBOM closure or cold offline-restored replay",
    "FAIL CLOSED independence: the differential source ran in this worker checkout and cache, not on a distinct signed independently provisioned runner",
    "audit_complete=false; theorem_complete=false",
)

KNOWN_FAILURES = (
    "S56-M-1227-PROOF is only provisionally self-tested [_], not master-accepted, and its receipt accepts no closed obligation.",
    "The exact canonical root has no proof body. M1227-N-DATA, M1227-N-GLOBAL, M1227-C-GALERKIN, M1227-C-BOUNDS, and M1227-C-COMPACT remain the frozen root cut.",
    "M1227-B-ZERO has only a planned registry fingerprint, so its checked declarations remain an implementation candidate pending master exact-statement mapping; no M0-L or closed-obligation status is accepted.",
    "The frozen pre-proof graph remains root M4 with no closed obligations. The older validation-specs.json checks only Statement.lean for every node and is not proof-validation evidence.",
    "Primary-source theorem/page, assumptions, errata, and independent source review remain open. scope-map.md still describes dimensions 2 or 3, optional forcing, and a source-prescribed weak trace, while Statement.lean freezes dimension 3, no force, and a strong squared-L2 trace.",
    "The frozen test class and energy formulation need source-level scrutiny: smooth tests vanishing for every negative time force phi 0 = 0, and the dissipation integral has no explicit time-integrability premise. Narrow validation establishes only the local Prop, not equivalence with the classical source theorem.",
    "The complete transitive declaration/import provenance, accepted foundation and TCB profile, dependency SBOM/license closure, and deterministic archive remain open.",
    "The replay used the automation-provided shared warm .lake cache. Network was denied and sources were copied to a fresh directory, but this is not a new clean checkout, empty-cache cold build, or offline-restored hermetic release replay.",
    "Validation.lean is separately implemented and imports only Statement, but it ran under this worker identity, checkout, kernel, and shared cache; it is not a second signed independently provisioned runner or independent release verifier.",
    "H0, R0, AUDIT-Z, THEOREM-Z, release, theorem completion, and master acceptance remain open.",
)


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


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(
    argv: list[str],
    *,
    cwd: Path = ROOT,
    env: dict[str, str] | None = None,
    timeout: int = 180,
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
    assert result.returncode == 0, (argv, result.returncode, result.stdout)
    return result.stdout.strip()


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["git", *args], cwd=cwd)


def source_without_comments(source: str) -> str:
    output: list[str] = []
    index = 0
    depth = 0
    in_string = False
    escaped = False
    while index < len(source):
        pair = source[index : index + 2]
        char = source[index]
        if depth:
            if pair == "/-":
                depth += 1
                index += 2
            elif pair == "-/":
                depth -= 1
                index += 2
            else:
                index += 1
            continue
        if in_string:
            output.append(char)
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
            index += 1
            continue
        if pair == "/-":
            depth = 1
            index += 2
        elif pair == "--":
            newline = source.find("\n", index + 2)
            if newline < 0:
                break
            output.append("\n")
            index = newline + 1
        else:
            output.append(char)
            if char == '"':
                in_string = True
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


def assert_sorry_free(output: str, declaration: str) -> None:
    marker = f"declaration uses 'sorry': '{declaration}'"
    assert marker not in output, (declaration, output)


def assert_text_hygiene(path: Path) -> None:
    data = path.read_bytes()
    assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())


def main() -> None:
    spec = load(HERE / "validation-spec.json")
    receipt = load(HERE / "validation-receipt.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    proof_receipt = load(HERE / "proof-receipt.json")
    proof_blocker = load(HERE / "proof-blocker.json")
    legacy_specs = load(HERE / "validation-specs.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE

    targets = load(ROOT / "Docs" / "Stage1_Targets_rev-5.6.json")
    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 416 and target["baseline"] == "L0"
    assert target["lifecycle_mode"] == "planned"
    assert target["rework_required"] is True and target["theorem_complete"] is False

    execution = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item == {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 416,
        "phase": "validation",
        "layer": 5,
        "state": "[ ]",
        "depends_on": ["S56-M-1227-PROOF"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Run hermetic kernel, trust, provenance, and independent validation gates.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }
    predecessor = next(row for row in execution["items"] if row["id"] == "S56-M-1227-PROOF")
    assert predecessor["state"] == "[_]" and predecessor["attempts"] == 1

    for name, expected in EXPECTED_INPUTS.items():
        assert sha256(HERE / name) == expected, f"stale validation input: {name}"
    assert receipt["inputs"]["validation-spec.json"] == EXPECTED_INPUTS["validation-spec.json"]
    assert sha256(HERE / "check_validation.py") == receipt["inputs"]["check_validation.py"]
    assert sha256(LEAN_ROOT / "lean-toolchain") == LEAN_TOOLCHAIN_SHA256
    assert sha256(LEAN_ROOT / "lake-manifest.json") == LAKE_MANIFEST_SHA256

    assert registry["root_obligation_id"] == "M1227-ROOT"
    assert registry["frozen_against_statement_sha256"] == STATEMENT_SHA256
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    closure = graphs["closure_boundary"]
    cut = [
        "M1227-N-DATA",
        "M1227-N-GLOBAL",
        "M1227-C-GALERKIN",
        "M1227-C-BOUNDS",
        "M1227-C-COMPACT",
    ]
    assert closure["closed_obligations"] == []
    assert closure["root_closed"] is False and closure["root_machine_debt"] == "M4"
    assert closure["remaining_root_cut_set"] == cut
    assert closure["audit_complete"] is closure["theorem_complete"] is False
    assert closure["composition_certificates_checked"] == [
        "Stage1.THM_M_1227.isLerayHopfSolution_compose"
    ]

    fingerprints = {
        row["obligation_id"]: row["statement_fingerprint"]
        for row in registry["obligations"]
    }
    assert fingerprints["M1227-B-ZERO"].startswith("planned:v1:sha256:")
    assert proof_receipt["accepted"] is False
    assert proof_receipt["accepted_closed_obligation_ids"] == []
    assert proof_receipt["provisionally_implemented_obligation_ids"] == ["M1227-B-ZERO"]
    assert proof_receipt["obligation_statement_fingerprints"]["M1227-B-ZERO"] == (
        fingerprints["M1227-B-ZERO"]
    )
    assert proof_receipt["result"]["root_closed"] is False
    assert proof_receipt["result"]["theorem_complete"] is False
    assert proof_receipt["proof_body"]["source_sha256"] == EXPECTED_INPUTS["Proof.lean"]
    assert proof_receipt["inputs"]["statement_source_sha256"] == STATEMENT_SHA256
    assert proof_receipt["inputs"]["obligation_registry_sha256"] == (
        EXPECTED_INPUTS["obligation-registry.json"]
    )
    assert set(proof_receipt["result"]["axioms"]) == EXPECTED_AXIOMS
    assert proof_blocker["remaining_root_cut_set"] == cut
    assert proof_blocker["accepted_receipt_ids"] == []

    assert legacy_specs["item_id"] == "S56-M-1227-OBLIGATION_TREE"
    assert len(legacy_specs["recipes"]) == 21
    assert all(row["argv"][-1].endswith("/Statement.lean") for row in legacy_specs["recipes"])

    manifest = load(LEAN_ROOT / "lake-manifest.json")
    mathlib_pin = next(row for row in manifest["packages"] if row["name"] == "mathlib")
    assert mathlib_pin["rev"] == mathlib_pin["inputRev"] == MATHLIB_REVISION
    assert MATHLIB.resolve().is_dir()
    assert git("rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert git("status", "--porcelain=v1", cwd=MATHLIB) == ""
    assert git("remote", "get-url", "origin", cwd=MATHLIB) == MATHLIB_REMOTE
    assert sha256(MATHLIB / "LICENSE") == LICENSE_SHA256

    olean_root = MATHLIB / ".lake" / "build" / "lib" / "lean"
    for relative, expected in PINNED_IMPORTS.items():
        source = MATHLIB / relative
        olean = olean_root / relative.replace(".lean", ".olean")
        assert git("rev-parse", f"HEAD:{relative}", cwd=MATHLIB) == expected["source_blob"]
        assert sha256(source) == expected["source_sha256"]
        assert sha256(olean) == expected["olean_sha256"]

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|implemented_by|native_decide|run_tac)\b|"
        r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
        r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
        r"(?:axiom|constant|opaque|unsafe)\b|\bextern[ \t]+",
        flags=re.MULTILINE,
    )
    for name in LEAN_MODULES:
        source = source_without_comments((HERE / name).read_text(encoding="utf-8"))
        source = source.replace("#print sorries", "")
        assert prohibited.search(source) is None, f"prohibited proof construct in {name}"

    validation = source_without_comments((HERE / "Validation.lean").read_text(encoding="utf-8"))
    assert validation.startswith('import Stage1_Instances.«THM-M-1227».Statement\n')
    assert "import Proof" not in validation and "zero_isLerayHopfSolution nu" not in validation
    assert "isLerayHopfSolution_compose" not in validation
    for marker in (
        "theorem zero_isLerayHopfSolution_direct",
        "theorem lerayHopfExistence_of_eq_zero_direct",
        "refine ⟨?_, ?_, ?_, ?_, ?_, ?_⟩",
    ):
        assert marker in validation

    scope_map = (HERE / "scope-map.md").read_text(encoding="utf-8")
    statement_record = (HERE / "statement.md").read_text(encoding="utf-8")
    assert "dimension `d = 2` or `d = 3`" in scope_map
    assert "External forcing only if" in scope_map
    assert "dimension two is not part of this canonical target" in statement_record
    assert "There is no external force" in statement_record

    lean = Path(run(["lake", "env", "which", "lean"], cwd=LEAN_ROOT))
    lean_path = run(["lake", "env", "printenv", "LEAN_PATH"], cwd=LEAN_ROOT)
    assert lean.is_file() and sha256(lean) == LEAN_EXECUTABLE_SHA256
    assert "Lean (version 4.29.0" in run([str(lean), "--version"])
    assert platform.system() == "Linux" and platform.machine() == "x86_64"
    python = Path(sys.executable).resolve()
    lake = Path(shutil.which("lake") or "").resolve()
    git_executable = Path(shutil.which("git") or "").resolve()
    bwrap_path = Path(shutil.which("bwrap") or "").resolve()
    assert python.is_file() and sha256(python) == PYTHON_EXECUTABLE_SHA256
    assert lake.is_file() and sha256(lake) == LAKE_EXECUTABLE_SHA256
    assert git_executable.is_file() and sha256(git_executable) == GIT_EXECUTABLE_SHA256
    assert bwrap_path.is_file() and sha256(bwrap_path) == BWRAP_EXECUTABLE_SHA256
    bwrap = str(bwrap_path)

    outputs: dict[str, str] = {}
    with tempfile.TemporaryDirectory(prefix="m1227-validation-", dir="/tmp") as tmp_name:
        tmp = Path(tmp_name).resolve()
        module_dir = tmp / "Stage1_Instances" / THEOREM
        module_dir.mkdir(parents=True)
        for name in LEAN_MODULES:
            (module_dir / name).write_bytes((HERE / name).read_bytes())
        base = [
            bwrap,
            "--ro-bind", "/", "/",
            "--bind", str(tmp), str(tmp),
            "--dev", "/dev",
            "--proc", "/proc",
            "--unshare-net",
            "--die-with-parent",
            "--clearenv",
            "--setenv", "HOME", str(tmp),
            "--setenv", "LANG", "C.UTF-8",
            "--setenv", "LC_ALL", "C.UTF-8",
            "--setenv", "TZ", "UTC",
            "--setenv", "LEAN_NUM_THREADS", "1",
            "--setenv", "LEAN_PATH", lean_path,
            "--chdir", str(tmp),
            str(lean), "--trust=0", "-t0", "-R", ".",
        ]
        local = base.copy()
        local[local.index(lean_path)] = f"{tmp}:{lean_path}"
        relative = f"Stage1_Instances/{THEOREM}"
        outputs["Statement.lean"] = run(
            base + [
                "-o", f"{relative}/Statement.olean", f"{relative}/Statement.lean"
            ],
            timeout=300,
        )
        expression_source = (HERE / "Statement.lean").read_text(encoding="utf-8").replace(
            "#check lerayHopfExistenceTarget\n",
            "#check lerayHopfExistenceTarget\n#print lerayHopfExistenceTarget\n",
            1,
        )
        (module_dir / "Expression.lean").write_text(expression_source, encoding="utf-8")
        outputs["Expression.lean"] = run(
            base + [f"{relative}/Expression.lean"], timeout=300
        )
        for name in ("Proof.lean", "Validation.lean"):
            outputs[name] = run(local + [f"{relative}/{name}"], timeout=300)

    expression_marker = "def Stage1.THM_M_1227.lerayHopfExistenceTarget : Prop :=\n"
    expression_end = "\n'Stage1.THM_M_1227.isLerayHopfSolution_compose'"
    expression_output = outputs.pop("Expression.lean")
    assert expression_marker in expression_output and expression_end in expression_output
    expression = (
        expression_marker
        + expression_output.split(expression_marker, 1)[1].split(expression_end, 1)[0].strip()
        + "\n"
    )
    assert hashlib.sha256(expression.encode("utf-8")).hexdigest() == EXPRESSION_SHA256

    for name, declarations in AXIOM_DECLARATIONS.items():
        for declaration in declarations:
            assert printed_axioms(outputs[name], declaration) == EXPECTED_AXIOMS
            assert_sorry_free(outputs[name], declaration)
    all_output = "\n".join(outputs.values())
    assert "sorryAx" not in all_output and "error:" not in all_output
    assert outputs["Proof.lean"].count("Declarations are sorry-free!") == 2
    assert outputs["Validation.lean"].count("Declarations are sorry-free!") == 2
    kernel_bytes = all_output.encode("utf-8")
    actual_kernel_result = (hashlib.sha256(kernel_bytes).hexdigest(), len(kernel_bytes))
    expected_kernel_result = (
        receipt["result"]["kernel_output_sha256"],
        receipt["result"]["kernel_output_bytes"],
    )
    assert actual_kernel_result == expected_kernel_result, actual_kernel_result

    assert spec["schema_version"] == "stage1-validation-spec/1.0"
    assert spec["item_id"] == ITEM and spec["theorem_id"] == THEOREM
    assert spec["cwd"] == "."
    assert spec["argv"] == [
        "python3", "-I", "-B", f"Stage1_Instances/{THEOREM}/check_validation.py"
    ]
    assert spec["env_allowlist"] == {
        "ELAN_TOOLCHAIN": "leanprover/lean4:v4.29.0",
        "LANG": "C.UTF-8",
        "LC_ALL": "C.UTF-8",
        "TZ": "UTC",
    }
    assert spec["timeout_seconds"] == 600
    assert spec["network_policy"] == "denied" and spec["expected_exit"] == 0
    assert set(spec["covered_declarations"]) == set(receipt["validated_declarations"])
    assert spec["covered_declarations"][:2] == [
        "Stage1.THM_M_1227.lerayHopfExistenceTarget",
        "Stage1.THM_M_1227.isLerayHopfSolution_compose",
    ]
    assert len(spec["covered_declarations"]) == 6 and sum(
        len(declarations) for declarations in AXIOM_DECLARATIONS.values()
    ) == 5
    recipe_fields = {
        key: value
        for key, value in spec.items()
        if key not in {"schema_version", "item_id", "theorem_id"}
    }
    assert receipt["recipe"] == recipe_fields

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["phase"] == "validation" and receipt["intent"] == "validate"
    assert receipt["verdict"] == "blocked"
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["release_grade"] is receipt["content_addressed_release_evidence"] is False
    assert receipt["canonical_target"]["statement_source_sha256"] == STATEMENT_SHA256
    assert receipt["canonical_target"]["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert receipt["canonical_target"]["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert receipt["result"]["root_kernel_closed"] is False
    assert receipt["result"]["complete_transitive_trust_and_provenance"] == "fail_closed"
    assert receipt["result"]["hermetic_release_gate"] == "fail_closed"
    assert receipt["result"]["independent_release_verification_gate"] == "fail_closed"
    assert receipt["result"]["audit_complete"] is receipt["result"]["theorem_complete"] is False
    assert receipt["remaining_root_cut_set"] == cut
    assert receipt["first_failed_gate"] == "dependency.S56-M-1227-PROOF.master_acceptance"
    assert receipt["accepted_receipt_ids"] == []
    assert receipt["lifecycle_before"] == receipt["lifecycle_after"] == "planned"
    assert receipt["debt_vector_delta"] == {
        "before": {"H": "H2", "M": "M4", "R": "R4"},
        "after_worker_selftest": {"H": "H2", "M": "M4", "R": "R4"},
        "changed": False,
    }
    assert receipt["known_failures"] == list(KNOWN_FAILURES)
    assert receipt["worker_handoff"]["receipt_id"] == receipt["receipt_id"]
    started_at = datetime.fromisoformat(receipt["started_at"])
    ended_at = datetime.fromisoformat(receipt["ended_at"])
    validated_at = datetime.fromisoformat(receipt["validated_at"])
    assert started_at.tzinfo is not None and ended_at.tzinfo is not None
    assert started_at <= ended_at == validated_at <= datetime.now().astimezone()
    assert (ended_at - started_at).total_seconds() <= spec["timeout_seconds"]
    assert receipt["environment"]["platform"] == "Linux 7.0.0-27-generic x86_64"
    assert receipt["environment"]["locale"] == "LANG=C.UTF-8; LC_ALL=C.UTF-8"
    assert receipt["environment"]["timezone"] == "UTC"
    assert receipt["environment"]["umask"] == "0002"
    assert receipt["nonrelease_worktree"]["tracked_patch_sha256"] == (
        "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    )
    assert receipt["nonrelease_worktree"]["pre_existing_untracked_path"] == (
        "Formalizations/Lean/.lake"
    )
    assert receipt["nonrelease_worktree"]["pre_existing_symlink_target"] == (
        "scheduler checkout Formalizations/Lean/.lake (absolute runtime path redacted)"
    )
    assert receipt["worker_handoff"]["recipe_id"] == spec["recipe_id"]
    assert receipt["worker_handoff"]["typed_graph_changes"] == []
    assert receipt["commands_and_exit_codes"] == [
        {"argv": row["argv"], "exit_code": row["exit_code"]}
        for row in packet["commands"]
    ]
    stdout_bytes = ("\n".join(SUMMARY_LINES) + "\n").encode("utf-8")
    assert receipt["result"]["stdout_sha256"] == hashlib.sha256(stdout_bytes).hexdigest()
    assert receipt["result"]["stdout_bytes"] == len(stdout_bytes)

    changed_paths = {
        ".stage1-worker-selftest.json",
        f"Stage1_Instances/{THEOREM}/Validation.lean",
        f"Stage1_Instances/{THEOREM}/check_validation.py",
        f"Stage1_Instances/{THEOREM}/validation-phase.md",
        f"Stage1_Instances/{THEOREM}/validation-receipt.json",
        f"Stage1_Instances/{THEOREM}/validation-spec.json",
    }
    assert set(packet) == {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert packet["item_id"] == ITEM and packet["state"] == "[_]"
    assert packet["base_revision"] == BASE_REVISION
    assert set(packet["changed_paths"]) == set(receipt["changed_paths"]) == changed_paths
    assert packet["known_failures"] == receipt["known_failures"] == list(KNOWN_FAILURES)
    status = git("status", "--short", "--untracked-files=all")
    actual_changes = {
        line[3:]
        for line in status.splitlines()
        if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual_changes == changed_paths, (actual_changes, changed_paths)

    for path in [ROOT / path for path in changed_paths]:
        assert_text_hygiene(path)
    for line in SUMMARY_LINES:
        print(line)


if __name__ == "__main__":
    main()
