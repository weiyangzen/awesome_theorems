#!/usr/bin/env python3
"""Fail-closed narrow validator for S56-M-0498-VALIDATION."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import platform
import re
import shutil
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0498"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
ITEM = "S56-M-0498-VALIDATION"
THEOREM = "THM-M-0498"
BASE_REVISION = "823dfcd5e231e84436ac3d88948d8e669c168fdb"
BASE_TREE = "a87f5f99350f49ddeb9d7df23dc6e0fe6fe3011f"
TOOLCHAIN = "leanprover/lean4:v4.29.0"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
LEAN_EXECUTABLE_SHA256 = "3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf"
LAKE_EXECUTABLE_SHA256 = "a608ff084d7e2af228b92a29d7c2fd083ba0580e46889175ec74a81678c98359"
TOOLCHAIN_SHA256 = "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2"
MANIFEST_SHA256 = "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MATHLIB_REMOTE = "https://github.com/leanprover-community/mathlib4.git"
MATHLIB_LICENSE_SHA256 = "b40930bbcf80744c86c46a12bc9da056641d722716c378f5659b9e555ef833e1"
TERMINAL_SOURCE = Path("Mathlib/NumberTheory/LSeries/Dirichlet.lean")
TERMINAL_SOURCE_BLOB = "adc4d5b6a96f5f12332bbc5fe723c09e23b6c34f"
TERMINAL_SOURCE_SHA256 = "99118a9578c0891aead06bdf0546fb137b68b12cd44bc311fcb242fc40e23f17"
TERMINAL_BODY_SHA256 = "50a896671d4c2c4a0e072c1363b836ae6b6529227cbed34075aa9b0fc04ec22a"
TERMINAL_OLEAN_SHA256 = "722ba67755d61af55e3c463a962a399a20c760ecd99af75d15a62b5814cca18d"
TERMINAL_OLEAN_BYTES = 106704
EXPRESSION_SHA256 = "4de2508b7d4cc86d13c5d51e1b5d6b8c61e43dec6655035224c21e25745af526"
DENOMINATOR_SHA256 = "8a964cd4c13dc98d9bfa75e22cf5bab2af31d96d83bde13600049c669d88f144"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
EXPECTED_INPUTS = {
    "Statement.lean": "ffdaf423ec563b3f6a33e7611e1627b01a8d1299c9afb62cbef2342dd54c623a",
    "ObligationTree.lean": "f6f710870505be57520ebd92305033876744d8c058a2a8837421200ea008efd6",
    "Proof.lean": "ccd61a7ac076de1226504ba53e95d1da6cb6485db1b52eac255a0678b5efc6df",
    "Validation.lean": "c32210a93ec0ca0ec5fa1056299a54a2a1003ea70f048d710abc91ad9a8d49d9",
    "statement.json": "895b79efd4b5bbd99e2b146c694ba40cd9756366222098cff34e2adb800d8201",
    "anchor-audit.json": "98722578675a0d2c4259792c5564bbb8072314111c75c9e43cdd8af2256c3312",
    "obligation-registry.json": "8707ec15002e01d30c5fbaf9b413f5e19aa5a91fd62949c3fd63152cd5d7e12b",
    "typed-graphs.json": "3f56008f4190bf3e50bb3117e2d57e6860c37080c68f5603a178759ce2f11210",
    "validation-specs.json": "5cb84e4fe80a2d40f388d23e6c4acf77bf9fa05d9a241f1976c27877710040bb",
    "proof-receipt.json": "90e3ac70da5b338e19c94cf1fb91a17693fb57fe03985f6526ff283b8248bba9",
    "proof-blocker.json": "8fba334340a27581d7057f3b3a39c95725006f39e7b02961e01cfe8219e27754",
}
ROOT_VECTOR = {"H": "H3", "M": "M4", "R": "R4"}
OPEN_ROOT_CUT = ["M0498-T-ANALYTIC"]
CHANGED_PATHS = [
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/Validation.lean",
    f"Stage1_Instances/{THEOREM}/check_validation.py",
    f"Stage1_Instances/{THEOREM}/validation-phase.md",
    f"Stage1_Instances/{THEOREM}/validation-receipt.json",
    f"Stage1_Instances/{THEOREM}/validation-spec.json",
]
SUMMARY_LINES = [
    "PASS narrow kernel replay: statement, conditional composition, proof bridge, and differential probes elaborated at trust zero",
    "PASS trust observation: terminal, local bridge, conditional composition, and probes report only propext, Classical.choice, and Quot.sound",
    "PASS selected provenance: frozen hashes, terminal body/source/olean/license, toolchain pins, and clean pinned mathlib revision agree",
    "OPEN exact root: the analytic explicit-formula package remains unproved at M4; no frozen proof obligation is newly closed",
    "FAIL CLOSED complete trust/provenance: accepted foundation policy, serialized transitive closure, and full TCB/SBOM inventory are absent",
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
        raise RuntimeError(
            f"command failed ({result.returncode}): {argv!r}\n{result.stdout}"
        )
    return result.stdout


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["git", *args], cwd=cwd).strip()


def code_without_comments(source: str) -> str:
    source = re.sub(r"/-.*?-/", "", source, flags=re.DOTALL)
    return re.sub(r"--.*$", "", source, flags=re.MULTILINE)


def printed_axioms(output: str, declaration: str) -> set[str]:
    match = re.search(
        rf"'[^']*{re.escape(declaration)}' depends on axioms:\s*\[(.*?)\]",
        output,
        flags=re.DOTALL,
    )
    assert match is not None, f"missing axiom report for {declaration}"
    return {
        part.strip()
        for part in match.group(1).replace("\n", "").split(",")
        if part.strip()
    }


def assert_text_hygiene(path: Path) -> None:
    data = path.read_bytes()
    assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())


def sandboxed_replay(lean: Path, lean_path: str, bwrap: Path) -> dict[str, str]:
    with tempfile.TemporaryDirectory(prefix="m0498-validation-", dir="/tmp") as tmp_name:
        tmp = Path(tmp_name).resolve()
        for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
            (tmp / name).write_bytes((HERE / name).read_bytes())

        base = [
            str(bwrap), "--ro-bind", "/", "/", "--bind", str(tmp), str(tmp),
            "--dev", "/dev", "--proc", "/proc", "--unshare-net",
            "--die-with-parent", "--clearenv", "--setenv", "HOME", str(tmp),
            "--setenv", "TMPDIR", str(tmp), "--setenv", "LANG", "C.UTF-8",
            "--setenv", "LC_ALL", "C.UTF-8", "--setenv", "TZ", "UTC",
            "--setenv", "LEAN_NUM_THREADS", "1", "--chdir", str(tmp),
        ]

        def lean_run(name: str, module_path: str, emit_olean: bool) -> str:
            argv = base + ["--setenv", "LEAN_PATH", module_path, str(lean), "--trust=0"]
            if emit_olean:
                argv += ["-o", name.replace(".lean", ".olean")]
            argv.append(name)
            return run(argv, timeout=600)

        outputs = {
            "statement": lean_run("Statement.lean", lean_path, True),
            "obligation_tree": lean_run(
                "ObligationTree.lean", f"{tmp}:{lean_path}", True
            ),
            "proof": lean_run("Proof.lean", f"{tmp}:{lean_path}", False),
            "validation": lean_run("Validation.lean", f"{tmp}:{lean_path}", False),
        }
    return outputs


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
    assert target["execution_rank"] == 258 and target["baseline"] == "L0"
    assert target["lifecycle_mode"] == "planned"
    assert target["rework_required"] is True and target["theorem_complete"] is False
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item == {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 258,
        "phase": "validation",
        "layer": 5,
        "state": "[ ]",
        "depends_on": ["S56-M-0498-PROOF"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Run hermetic kernel, trust, provenance, and independent validation gates.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }
    predecessor = next(
        row for row in execution["items"] if row["id"] == "S56-M-0498-PROOF"
    )
    assert predecessor["state"] == "[_]" and predecessor["attempts"] == 1
    dependency_support = load(HERE / "proof-receipt.json")
    dependency_accepted = (
        predecessor["state"] == "[x]"
        and dependency_support.get("support_state") == "master_accepted"
    )
    assert dependency_accepted is False

    for name, expected in EXPECTED_INPUTS.items():
        assert sha256(HERE / name) == expected, f"stale validation input: {name}"
    assert sha256(LEAN_ROOT / "lean-toolchain") == TOOLCHAIN_SHA256
    assert sha256(LEAN_ROOT / "lake-manifest.json") == MANIFEST_SHA256
    assert statement["canonical_formal_target"]["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert statement["canonical_formal_target"]["statement_file_sha256"] == EXPECTED_INPUTS["Statement.lean"]
    assert registry["frozen_against_statement_sha256"] == EXPECTED_INPUTS["Statement.lean"]
    assert registry["frozen_against_anchor_audit_sha256"] == EXPECTED_INPUTS["anchor-audit.json"]
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    closure = graphs["closure_boundary"]
    assert closure["root_closed"] is False
    assert closure["audit_complete"] is closure["theorem_complete"] is False
    assert closure["remaining_root_cut_set"] == OPEN_ROOT_CUT
    root = next(node for node in graphs["nodes"] if node["obligation_id"] == "M0498-ROOT")
    assert {
        "H": root["human_debt"], "M": root["machine_debt"], "R": root["readability_debt"]
    } == ROOT_VECTOR
    dirichlet = next(
        node for node in graphs["nodes"] if node["obligation_id"] == "M0498-A-DIRICHLET"
    )
    assert dirichlet["machine_debt"] == "M4"
    assert dirichlet["formal_target"].startswith("planned wrapper around")
    assert proof_receipt["item_id"] == "S56-M-0498-PROOF"
    assert proof_receipt["proof_body"]["source_sha256"] == EXPECTED_INPUTS["Proof.lean"]
    assert proof_receipt["closed_obligation_ids"] == []
    assert proof_receipt["result"]["root_closed"] is False
    assert proof_receipt["result"]["theorem_complete"] is False
    assert proof_receipt["remaining_root_cut_set"] == OPEN_ROOT_CUT

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by|extern)\b|"
        r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
        r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
        r"(?:axiom|constant|opaque|unsafe)\b",
        flags=re.MULTILINE,
    )
    for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
        source = code_without_comments((HERE / name).read_text(encoding="utf-8"))
        assert prohibited.search(source) is None, f"prohibited proof construct in {name}"
    validation_source = code_without_comments((HERE / "Validation.lean").read_text())
    assert not re.search(
        r"^[ \t]*import[ \t]+(?:Proof|ObligationTree)\b",
        validation_source,
        flags=re.MULTILINE,
    )
    for fragment in (
        "theorem logDerivativeDirect",
        "ArithmeticFunction.LSeries_vonMangoldt_eq_deriv_riemannZeta_div hs",
        "theorem rootConditionalProbe (analytic : AnalyticPackageProbe)",
        "exact analytic E x hx hpp",
        "assert_no_sorry rootConditionalProbe",
        "#print axioms rootConditionalProbe",
    ):
        assert fragment in validation_source, fragment

    manifest = load(LEAN_ROOT / "lake-manifest.json")
    mathlib_entry = next(row for row in manifest["packages"] if row["name"] == "mathlib")
    flt_entry = next(row for row in manifest["packages"] if row["name"] == "«flt-regular»")
    assert mathlib_entry["rev"] == mathlib_entry["inputRev"] == MATHLIB_REVISION
    assert flt_entry["rev"] == flt_entry["inputRev"] == "56161b6eb5281fbfe9c38f2bcec0f429ebc11a27"
    assert (LEAN_ROOT / ".lake").is_symlink(), "canonical worker .lake symlink is missing"
    mathlib = (LEAN_ROOT / ".lake" / "packages" / "mathlib").resolve()
    assert mathlib.is_dir(), "canonical pinned mathlib artifact is missing"
    assert git("rev-parse", "HEAD", cwd=mathlib) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == MATHLIB_TREE
    assert git("status", "--porcelain=v1", cwd=mathlib) == ""
    assert git("remote", "get-url", "origin", cwd=mathlib) == MATHLIB_REMOTE
    assert git("rev-parse", f"HEAD:{TERMINAL_SOURCE}", cwd=mathlib) == TERMINAL_SOURCE_BLOB
    assert sha256(mathlib / TERMINAL_SOURCE) == TERMINAL_SOURCE_SHA256
    terminal_olean = mathlib / ".lake/build/lib/lean/Mathlib/NumberTheory/LSeries/Dirichlet.olean"
    assert sha256(terminal_olean) == TERMINAL_OLEAN_SHA256
    assert terminal_olean.stat().st_size == TERMINAL_OLEAN_BYTES
    assert sha256(mathlib / "LICENSE") == MATHLIB_LICENSE_SHA256
    declared_flt = LEAN_ROOT / ".lake/packages/«flt-regular»/.lake/build/lib/lean"
    fallback_flt = LEAN_ROOT / ".lake/packages/flt-regular"
    assert not declared_flt.exists()
    assert fallback_flt.is_dir()
    assert git("rev-parse", "HEAD", cwd=fallback_flt) == flt_entry["rev"]
    assert git("status", "--porcelain=v1", cwd=fallback_flt) == ""
    assert not (fallback_flt / ".lake/build/lib/lean").exists()
    terminal_lines = (mathlib / TERMINAL_SOURCE).read_bytes().splitlines(keepends=True)
    assert hashlib.sha256(b"".join(terminal_lines[433:440])).hexdigest() == TERMINAL_BODY_SHA256
    terminal_code = code_without_comments((mathlib / TERMINAL_SOURCE).read_text(encoding="utf-8"))
    assert prohibited.search(terminal_code) is None

    fixed_env = {
        "ELAN_TOOLCHAIN": TOOLCHAIN,
        "LANG": "C.UTF-8",
        "LC_ALL": "C.UTF-8",
        "TZ": "UTC",
        "LEAN_NUM_THREADS": "1",
    }
    elan_launcher_name = shutil.which("elan")
    assert elan_launcher_name is not None, "Elan launcher is unavailable"
    elan_launcher = Path(elan_launcher_name).resolve()
    assert sha256(elan_launcher) == "840179e70803ef373c2ec53342d6a45ea7d022533e4145489fc1278b4f716385"
    lean = Path(run(
        [str(elan_launcher), "which", "lean"], cwd=LEAN_ROOT, env=fixed_env
    ).strip())
    lake = Path(run(
        [str(elan_launcher), "which", "lake"], cwd=LEAN_ROOT, env=fixed_env
    ).strip())
    package_names = (
        "Cli", "batteries", "Qq", "aesop", "proofwidgets", "importGraph",
        "LeanSearchClient", "plausible", "checkdecls", "mathlib",
    )
    package_roots = [
        (LEAN_ROOT / ".lake/packages" / name).resolve() for name in package_names
    ]
    compiled_roots = [
        path / ".lake/build/lib/lean"
        for path in package_roots
        if (path / ".lake/build/lib/lean").is_dir()
    ]
    assert (mathlib / ".lake/build/lib/lean") in compiled_roots
    lean_path = ":".join([
        *(str(path) for path in compiled_roots),
        str((LEAN_ROOT / ".lake/build/lib/lean").resolve()),
        str((lean.parent.parent / "lib/lean").resolve()),
    ])
    bwrap_name = shutil.which("bwrap")
    assert bwrap_name is not None, "bubblewrap is required for network-denied replay"
    bwrap = Path(bwrap_name).resolve()
    assert sha256(lean) == LEAN_EXECUTABLE_SHA256
    assert sha256(lake) == LAKE_EXECUTABLE_SHA256
    assert LEAN_COMMIT in run([str(lean), "--version"], env=fixed_env)
    assert "5.0.0-src+98dc76e" in run([str(lake), "--version"], env=fixed_env)

    outputs = sandboxed_replay(lean, lean_path, bwrap)
    proof_declarations = (
        "ArithmeticFunction.LSeries_vonMangoldt_eq_deriv_riemannZeta_div",
        "Stage1Instances.THM_M_0498.LSeries_vonMangoldt_logDerivative",
    )
    validation_declarations = (
        "ArithmeticFunction.LSeries_vonMangoldt_eq_deriv_riemannZeta_div",
        "Stage1Instances.THM_M_0498.Validation.logDerivativeDirect",
        "Stage1Instances.THM_M_0498.Validation.rootConditionalProbe",
    )
    for declaration in proof_declarations:
        assert printed_axioms(outputs["proof"], declaration) == EXPECTED_AXIOMS
    for declaration in validation_declarations:
        assert printed_axioms(outputs["validation"], declaration) == EXPECTED_AXIOMS
    assert printed_axioms(
        outputs["obligation_tree"],
        "Stage1Instances.THM_M_0498.root_of_analytic_package",
    ) == EXPECTED_AXIOMS
    proof_sorry_free = outputs["proof"].count("Declarations are sorry-free!")
    validation_sorry_free = outputs["validation"].count("Declarations are sorry-free!")
    assert proof_sorry_free >= 1
    assert validation_sorry_free >= 1
    closure_match = re.search(
        r"VALIDATION_CLOSURE declarations=(\d+) modules=(\d+)",
        outputs["validation"],
    )
    assert closure_match is not None
    assert "VALIDATION_CLOSURE axioms=[propext, Classical.choice, Quot.sound]" in outputs["validation"]
    assert "VALIDATION_CLOSURE bodyless_nonaxioms=[]" in outputs["validation"]
    assert "VALIDATION_CLOSURE unsafe=[]" in outputs["validation"]
    assert "sorryAx" not in "\n".join(outputs.values())
    assert all("error:" not in output for output in outputs.values())

    observation = {
        "output_sha256": {
            name: hashlib.sha256(output.encode()).hexdigest()
            for name, output in outputs.items()
        },
        "observed_axioms": sorted(EXPECTED_AXIOMS),
        "conditional_composition_axioms": sorted(EXPECTED_AXIOMS),
        "proof_sorry_free_reports": proof_sorry_free,
        "validation_sorry_free_reports": validation_sorry_free,
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
    assert spec["schema_version"] == "stage1-validation-spec/1.0"
    assert spec["item_id"] == receipt["item_id"] == ITEM
    assert spec["theorem_id"] == receipt["theorem_id"] == THEOREM
    assert spec["depends_on"] == receipt["depends_on"] == ["S56-M-0498-PROOF"]
    assert len(spec["recipes"]) == 1
    recipe = spec["recipes"][0]
    assert recipe["argv"] == [
        "python3", "-B", f"Stage1_Instances/{THEOREM}/check_validation.py",
        "--worker-packet", ".stage1-worker-selftest.json",
    ]
    assert recipe["cwd"] == "." and recipe["timeout_seconds"] == 600
    assert recipe["network_policy"] == "denied"
    assert recipe["expected_exit"] == 0
    assert "bubblewrap" in recipe["network_enforcement"]
    assert receipt["recipe"] == recipe

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["phase"] == "validation" and receipt["intent"] == "validate"
    assert receipt["verdict"] == "blocked"
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["release_grade"] is False
    assert receipt["content_addressed_release_evidence"] is False
    assert receipt["lifecycle_before"] == receipt["lifecycle_after"] == "planned"
    assert receipt["root_vector_before"] == receipt["root_vector_after"] == ROOT_VECTOR
    assert receipt["debt_vector_change_proposed"] is False
    assert receipt["accepted_receipt_ids"] == []
    for name, expected in EXPECTED_INPUTS.items():
        assert receipt["inputs"][name] == expected, name
    assert receipt["inputs"]["validation-spec.json"] == sha256(HERE / "validation-spec.json")
    assert receipt["inputs"]["check_validation.py"] == sha256(HERE / "check_validation.py")
    assert receipt["target"]["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert receipt["target"]["registry_denominator_sha256"] == DENOMINATOR_SHA256
    environment = receipt["environment"]
    assert environment["platform"] == f"{platform.system()} {platform.release()} {platform.machine()}"
    assert environment["lean_executable_sha256"] == sha256(lean)
    assert environment["lake_executable_sha256"] == sha256(lake)
    assert environment["elan_launcher_sha256"] == sha256(elan_launcher)
    assert environment["bubblewrap_executable_sha256"] == sha256(bwrap)
    python = Path(shutil.which("python3") or "").resolve()
    git_executable = Path(shutil.which("git") or "").resolve()
    assert environment["python_executable_sha256"] == sha256(python)
    assert environment["git_executable_sha256"] == sha256(git_executable)
    assert environment["bubblewrap_version"] in run([str(bwrap), "--version"])
    assert environment["python_version"] in run([str(python), "--version"])
    assert environment["git_version"] in run([str(git_executable), "--version"])
    assert environment["mathlib_revision"] == MATHLIB_REVISION
    assert environment["mathlib_tree"] == MATHLIB_TREE
    assert receipt["result"]["lean_output_sha256"] == observation["output_sha256"]
    assert receipt["result"]["observed_axioms"] == observation["observed_axioms"]
    assert receipt["result"]["validation_closure"] == observation["validation_closure"]
    assert receipt["result"]["proof_dependency_master_acceptance"] == "fail_closed"
    assert receipt["result"]["accepted_closed_obligation_ids"] == []
    assert receipt["result"]["root_kernel_closed"] is False
    assert receipt["result"]["root_machine_debt"] == "M4"
    assert receipt["result"]["open_root_cut_set"] == OPEN_ROOT_CUT
    assert receipt["remaining_root_cut_set"] == OPEN_ROOT_CUT
    assert receipt["result"]["complete_trust_provenance_gate"] == "fail_closed"
    assert receipt["result"]["hermetic_release_gate"] == "fail_closed"
    assert receipt["result"]["independent_distinct_runner_gate"] == "fail_closed"
    assert receipt["result"]["audit_complete"] is receipt["result"]["theorem_complete"] is False
    assert receipt["first_failed_gate"] == "dependency.S56-M-0498-PROOF.master_acceptance"
    assert receipt["first_failed_release_gate"] == "S56-10.6-HERMETIC-COLD-BUILD"
    expected_stdout = ("\n".join(SUMMARY_LINES) + "\n").encode()
    assert receipt["output_evidence"] == {
        "stdout_semantic_sha256": hashlib.sha256(expected_stdout).hexdigest(),
        "expected_line_count": len(SUMMARY_LINES),
        "exit_code": 0,
    }

    if args.worker_packet is not None:
        packet = load(args.worker_packet.resolve())
        assert set(packet) == {
            "item_id", "changed_paths", "commands", "output_summary",
            "base_revision", "known_failures", "state",
        }
        assert packet["item_id"] == ITEM and packet["state"] == "[_]"
        assert packet["base_revision"] == BASE_REVISION
        assert packet["changed_paths"] == receipt["changed_paths"] == CHANGED_PATHS
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
