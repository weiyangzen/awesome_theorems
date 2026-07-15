#!/usr/bin/env python3
"""Fail-closed validation for S56-M-0034-VALIDATION."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0034"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM = "S56-M-0034-VALIDATION"
THEOREM = "THM-M-0034"
BASE_REVISION = "61f7b69093a1a921bba3b39c1c58955f9b3a4808"
BASE_TREE = "5849148c92f4a72549a18481b3eda847afb1e3da"
TOOLCHAIN = "leanprover/lean4:v4.29.0"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
LEAN_SHA256 = "3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf"
LAKE_SHA256 = "840179e70803ef373c2ec53342d6a45ea7d022533e4145489fc1278b4f716385"
BWRAP_SHA256 = "0abea81db798ebf6b4742ac0664802d97521547a353c2a0dbdc21d76cbbfd2c0"
PYTHON_SHA256 = "b8d8288faefdd300201f43fcf00f6f539a27218eeed3a3dff5ab10b9c4c99700"
GIT_SHA256 = "5516c9f362c29376ab9a499a33082f9f611941d8c75930c880e30ad109e39c9a"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MATHLIB_REMOTE = "https://github.com/leanprover-community/mathlib4.git"
TARGET_EXPRESSION_SHA256 = (
    "d80cc9860ed5a53c81a0851b4dc8e702aa5a23d448f373ae6d68ed0c9b5604b1"
)
REGISTRY_DENOMINATOR_SHA256 = (
    "0f1fd6b2f8450f934acd51372109d93d3b86bfc9ecaac8fe0f58bc566d7fb090"
)
SELECTED_EXTERNAL_REVISION = "e8d85a6f6fa210ba0be12bd02aa22009699f0c35"
VENDORED_EXTERNAL_REVISION = "51ed173b17b274e61f759556ab3e1c090267d1bd"
VENDORED_EXTERNAL_TREE = "264c487a24b2158bf8432459fd0b1e326acdf1eb"
VENDORED_ARCHIVE_SHA256 = (
    "ad8bd7662861ddf984f6c244f3b1d3eabbe4b0fd9b33f51dd85e2918d737babf"
)
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
EXPECTED_CLOSURE = {"declarations": 30764, "modules": 1094}
EXPECTED_INPUTS = {
    "Statement.lean": "cfdfeabe825f5b7936905cee310c2306dba8b18a4b25281fb09c7d10719b79e8",
    "ObligationTree.lean": "a7e6115c86e73a0ecf8d79acb5b84d1fe7d2f0f2a24b094e0dfa8b134e11b64c",
    "Proof.lean": "44fd994f47c80f6dc3d6578615cd97c832cfb02badb6c82902c2df11c9d83c83",
    "ProofAudit.lean": "8f38dca325cd5518cf27538fe7fb3573b3ff0db5c02a282720c2506dff5a279e",
    "Validation.lean": "db03ea574fadda2a4b1c3c9d686eebabcba857b1773bc2da7a66d5114fc1ec91",
    "statement.json": "35dc0d711e856ccc9a4e325b208e79106007f20e0bbf28f93f757ac2001d013c",
    "anchor-audit.json": "af9c964f520ecf5492d1a93c2fda96f4dee400d610641ae1dfbe4411f5c2ddcd",
    "obligation-registry.json": "de388aac08659553285062670f11ef3c68d0fa5539c6c575e6e8744fa1a1e133",
    "typed-graphs.json": "fa5cfa00873556291a783b7376d3cb0d949cfc36b4d6a9bcf34e8c96d90e3c0b",
    "proof-receipt.json": "466c2c3818cfb8b1b62ec1e8666f2218fe524d1095502a5b21f436507dbea9ef",
    "vendor-manifest.json": "f2806ec825b0dfe2495f5666a99c5dc906442cd610f33ec6c5743e861910371d",
    "PORT_PROVENANCE.md": "5c1316c7bf35956c7a6671b668b94588cacf163565a4d7e6d9929fed712c92f2",
    "build_vendor_manifest.py": "2e0eab89ea3e6af102a4d80bca2ee902c89e8186cf8278a79f7b933a1b85bbac",
    "check_proof.sh": "6d1cff2873daeaa79483eea5805676a0970ef4c665ee7770a9bd573fa08a2333",
    "validation-spec.json": "f3067eed95abedf4e995da13e3bb26a7ad3ea80a27bbad67d110963146b7665b",
    "validation-phase.md": "94b1b43767e47c8630748bcaea0a7a4be1570e04d394fd28eb2621d41a919985",
}
EXPECTED_TOOL_INPUTS = {
    "lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
VENDOR_BUILD_ORDER = [
    "Stage1_Instances/THM-M-0034/Vendor/QuillenSuslin/UnimodularVector/BivariatePolynomial",
    "Stage1_Instances/THM-M-0034/Vendor/QuillenSuslin/UnimodularVector/SuslinMonicPolynomialThm",
    "Stage1_Instances/THM-M-0034/Vendor/QuillenSuslin/UnimodularVector/Basic",
    "Stage1_Instances/THM-M-0034/Vendor/QuillenSuslin/UnimodularVector/PID",
    "Stage1_Instances/THM-M-0034/Vendor/QuillenSuslin/FiniteFreeResolution/Basic",
    "Stage1_Instances/THM-M-0034/Vendor/QuillenSuslin/FiniteFreeResolution/Polynomial",
    "Stage1_Instances/THM-M-0034/Vendor/QuillenSuslin/FiniteFreeResolution/StablyFree",
    "Stage1_Instances/THM-M-0034/Vendor/QuillenSuslin/MainTheorem",
]
SUMMARY_LINES = [
    "PASS narrow kernel replay: frozen target, vendored terminal body, exact proof adapter, and differential adapter elaborated at trust zero",
    "PASS trust observation: terminal, local, and differential roots are sorry-free with only propext, Classical.choice, and Quot.sound",
    "PASS direct provenance: local hashes, reversible vendor ledger, Apache-2.0 boundary, and clean pinned mathlib agree",
    "FAIL CLOSED dependency and architecture: proof is provisional and the frozen graph selects a different external body",
    "FAIL CLOSED hermetic release: network-isolated fresh outputs reused the shared warm cache and no cold offline restoration exists",
    "FAIL CLOSED independent verification: same-worker differential checking is not a distinct signed runner or minimal verifier",
]
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/Validation.lean",
    f"Stage1_Instances/{THEOREM}/check_validation.py",
    f"Stage1_Instances/{THEOREM}/validation-phase.md",
    f"Stage1_Instances/{THEOREM}/validation-receipt.json",
    f"Stage1_Instances/{THEOREM}/validation-spec.json",
}


def reject_duplicate_keys(pairs: list[tuple[str, object]]) -> dict:
    value: dict[str, object] = {}
    for key, item in pairs:
        assert key not in value, f"duplicate JSON key: {key}"
        value[key] = item
    return value


def load(path: Path) -> dict:
    value = json.loads(
        path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicate_keys
    )
    assert isinstance(value, dict), path
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


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


def run(
    argv: list[str], *, cwd: Path = ROOT, env: dict[str, str] | None = None,
    timeout: int = 900
) -> bytes:
    result = subprocess.run(
        argv,
        cwd=cwd,
        env=env if env is not None else BASE_ENV,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=timeout,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"command failed ({result.returncode}): {argv!r}\n"
            + result.stdout.decode("utf-8", errors="replace")
        )
    return result.stdout


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["/usr/bin/git", *args], cwd=cwd).decode().strip()


def source_without_comments_and_strings(source: str) -> str:
    output: list[str] = []
    index = 0
    block_depth = 0
    in_string = False
    in_char = False
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
        elif in_string or in_char:
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
        elif char == "'" and index + 2 < len(source) and source[index + 2] == "'":
            in_char = True
            output.append(" ")
            index += 1
        else:
            output.append(char)
            index += 1
    assert block_depth == 0 and not in_string and not in_char
    return "".join(output)


def assert_axioms(output: str, declaration: str) -> None:
    match = re.search(
        re.escape(f"'{declaration}' depends on axioms: [") + r"(.*?)]",
        output,
        re.DOTALL,
    )
    assert match is not None, f"missing axiom report for {declaration}"
    actual = {part.strip() for part in match.group(1).split(",") if part.strip()}
    assert actual == EXPECTED_AXIOMS, (declaration, actual)


def assert_text_hygiene(path: Path) -> None:
    data = path.read_bytes()
    assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data, path
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines()), path


def replay(lean: Path, lean_path: str, bwrap: Path) -> dict[str, bytes]:
    with tempfile.TemporaryDirectory(prefix="m0034-validation-", dir="/tmp") as name:
        tmp = Path(name).resolve()
        target_dir = tmp / "Stage1_Instances" / THEOREM
        target_dir.mkdir(parents=True)
        for source in ("Statement.lean", "Proof.lean", "ProofAudit.lean", "Validation.lean"):
            shutil.copy2(HERE / source, target_dir / source)
        shutil.copytree(HERE / "Vendor", target_dir / "Vendor")
        (tmp / "home").mkdir()
        options = [
            "--trust=0", "-t0", "-DautoImplicit=false",
            "-DrelaxedAutoImplicit=false", "-Dweak.linter.mathlibStandardSet=false",
            "-DmaxSynthPendingDepth=3", "-R", str(tmp),
        ]
        base = [
            str(bwrap), "--ro-bind", "/", "/", "--bind", str(tmp), str(tmp),
            "--dev", "/dev", "--proc", "/proc", "--unshare-net", "--die-with-parent",
            "--clearenv", "--setenv", "HOME", str(tmp / "home"),
            "--setenv", "TMPDIR", str(tmp), "--setenv", "LANG", "C.UTF-8",
            "--setenv", "LC_ALL", "C.UTF-8", "--setenv", "TZ", "UTC",
            "--setenv", "LEAN_NUM_THREADS", "1", "--chdir", str(tmp),
            "--setenv", "LEAN_PATH", f"{tmp}:{lean_path}", str(lean), *options,
        ]

        def compile_module(module: str, *, emit_olean: bool) -> bytes:
            argv = [*base]
            if emit_olean:
                argv += ["-o", f"{module}.olean"]
            argv.append(f"{module}.lean")
            return run(argv, timeout=900)

        outputs: dict[str, bytes] = {}
        outputs["statement"] = compile_module(
            f"Stage1_Instances/{THEOREM}/Statement", emit_olean=True
        )
        for module in VENDOR_BUILD_ORDER:
            compile_module(module, emit_olean=True)
        outputs["proof"] = compile_module(
            f"Stage1_Instances/{THEOREM}/Proof", emit_olean=True
        )
        outputs["proof_audit"] = compile_module(
            f"Stage1_Instances/{THEOREM}/ProofAudit", emit_olean=False
        )
        outputs["validation"] = compile_module(
            f"Stage1_Instances/{THEOREM}/Validation", emit_olean=False
        )
        return outputs


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker-packet", type=Path)
    args = parser.parse_args()

    targets = load(ROOT / "Docs" / "Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")
    statement = load(HERE / "statement.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    proof_receipt = load(HERE / "proof-receipt.json")
    vendor_manifest = load(HERE / "vendor-manifest.json")
    spec = load(HERE / "validation-spec.json")
    receipt = load(HERE / "validation-receipt.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 1078 and target["baseline"] == "L0"
    assert target["rework_required"] is True and target["lifecycle_mode"] == "planned"
    assert target["theorem_complete"] is False
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item == {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 1078,
        "phase": "validation",
        "layer": 5,
        "state": "[ ]",
        "depends_on": ["S56-M-0034-PROOF"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Run hermetic kernel, trust, provenance, and independent validation gates.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }
    predecessor = next(
        row for row in execution["items"] if row["id"] == "S56-M-0034-PROOF"
    )
    assert predecessor["state"] == "[_]" and predecessor["attempts"] == 1

    for name, expected in EXPECTED_INPUTS.items():
        assert sha256(HERE / name) == expected, f"stale validation input: {name}"
    for name, expected in EXPECTED_TOOL_INPUTS.items():
        assert sha256(LEAN_ROOT / name) == expected, f"changed tool input: {name}"

    formal = statement["canonical_formal_target"]
    assert formal["declaration_or_expression"] == (
        "Stage1Instances.THM_M_0034.QuillenSuslinTarget"
    )
    assert formal["elaborated_expression_sha256"] == TARGET_EXPRESSION_SHA256
    assert formal["statement_file_sha256"] == EXPECTED_INPUTS["Statement.lean"]
    assert registry["root_obligation_id"] == "M0034-ROOT"
    assert registry["denominator_sha256"] == REGISTRY_DENOMINATOR_SHA256
    assert graphs["registry_denominator_sha256"] == REGISTRY_DENOMINATOR_SHA256
    assert registry["selected_external_revision"] == SELECTED_EXTERNAL_REVISION
    assert registry["proof_body_aliases"]["mbkybky.QuillenSuslin.quillenSuslin"] == (
        "alternative_body_no_selected_credit"
    )
    alternative = next(
        row for row in registry["obligations"]
        if row["obligation_id"] == "M0034-X-ALT-PID"
    )
    assert alternative["machine_eligibility"] == "informational"
    assert alternative["terminal_proof_body_id"] is None
    closure = graphs["closure_boundary"]
    assert closure["accepted_closed_obligations"] == []
    assert closure["root_closed"] is False and closure["root_machine_debt"] == "M3"
    assert closure["audit_complete"] is False and closure["theorem_complete"] is False
    assert "M0034-X-EXTERNAL-BODY" in closure["remaining_root_cut_set"]

    assert proof_receipt["item_id"] == "S56-M-0034-PROOF"
    assert proof_receipt["accepted"] is False
    assert proof_receipt["proposed_state"] == "[_]"
    assert proof_receipt["closed_obligation_ids_proposed"] == []
    assert proof_receipt["accepted_closed_obligation_ids"] == []
    assert proof_receipt["graph_reconciliation_pending"]["required"] is True
    assert proof_receipt["graph_reconciliation_pending"]["frozen_selected_revision"] == (
        SELECTED_EXTERNAL_REVISION
    )
    assert proof_receipt["graph_reconciliation_pending"]["observed_alternate_revision"] == (
        VENDORED_EXTERNAL_REVISION
    )
    assert proof_receipt["proof_body"]["source_sha256"] == EXPECTED_INPUTS["Proof.lean"]
    assert proof_receipt["proof_body"]["vendor_manifest_sha256"] == (
        EXPECTED_INPUTS["vendor-manifest.json"]
    )

    assert vendor_manifest["upstream"]["revision"] == VENDORED_EXTERNAL_REVISION
    assert vendor_manifest["upstream"]["source_tree"] == VENDORED_EXTERNAL_TREE
    assert vendor_manifest["upstream"]["source_archive_sha256"] == VENDORED_ARCHIVE_SHA256
    assert vendor_manifest["target_environment"]["mathlib_revision"] == MATHLIB_REVISION
    assert vendor_manifest["target_environment"]["mathlib_tree"] == MATHLIB_TREE
    assert vendor_manifest["license"]["spdx"] == "Apache-2.0"
    assert vendor_manifest["license"]["standard_text_supplied_locally"] is True
    assert vendor_manifest["license"]["copied_from_upstream_archive"] is False
    assert vendor_manifest["closure"] == {
        "module_count": 8,
        "internal_import_edges": 7,
        "vendored_bytes": 260645,
        "vendored_lines": 5079,
        "semantic_diff_sha256": (
            "372acc2ec8f1f0921b9ffe63fda67f4ec40487840d8379af091a7297047d0d19"
        ),
        "normalized_compatibility_patch_sha256": (
            "c76174fb78f391ceb00fc57df79829ef3af99c0dc43b477f444c61085ed02fe3"
        ),
    }

    recipes = spec["recipes"]
    assert len(recipes) == 1 and spec["item_id"] == ITEM
    recipe = recipes[0]
    assert recipe["argv"] == [
        "python3", "-I", "-B", f"Stage1_Instances/{THEOREM}/check_validation.py",
        "--worker-packet", ".stage1-worker-selftest.json",
    ]
    assert recipe["network_policy"] == "denied" and recipe["expected_exit"] == 0
    assert recipe["covered_obligation_ids"] == []
    assert recipe["observed_without_graph_credit_obligation_ids"] == [
        "M0034-ROOT", "M0034-X-ALT-PID"
    ]

    prohibited = re.compile(
        r"#exit\b|\b(?:sorry|admit|sorryAx|native_decide|implemented_by)\b|"
        r"^[ \t]*(?:axiom|constant|opaque|unsafe|extern)[ \t]+",
        re.MULTILINE,
    )
    sources = [HERE / name for name in (
        "Statement.lean", "ObligationTree.lean", "Proof.lean", "ProofAudit.lean",
        "Validation.lean",
    )] + sorted((HERE / "Vendor").rglob("*.lean"))
    for path in sources:
        stripped = source_without_comments_and_strings(path.read_text(encoding="utf-8"))
        match = prohibited.search(stripped)
        assert match is None, (path, match.group(0) if match else None)
    validation_source = (HERE / "Validation.lean").read_text(encoding="utf-8")
    assert "import «Stage1_Instances».«THM-M-0034».Proof" not in validation_source
    assert "import «Stage1_Instances».«THM-M-0034».ObligationTree" not in validation_source
    assert "theorem differentialQuillenSuslinTarget" in validation_source

    manifest = load(LEAN_ROOT / "lake-manifest.json")
    mathlib_entry = next(row for row in manifest["packages"] if row["name"] == "mathlib")
    assert mathlib_entry["rev"] == mathlib_entry["inputRev"] == MATHLIB_REVISION
    assert MATHLIB.resolve().is_dir(), "pinned mathlib artifacts unavailable"
    assert git("rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert git("remote", "get-url", "origin", cwd=MATHLIB) == MATHLIB_REMOTE
    assert git("status", "--porcelain=v1", cwd=MATHLIB) == ""
    assert sha256(MATHLIB / "LICENSE") == (
        "b40930bbcf80744c86c46a12bc9da056641d722716c378f5659b9e555ef833e1"
    )
    assert sha256(HERE / "Vendor" / "LICENSE") == (
        "cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30"
    )

    bwrap_name = shutil.which("bwrap", path=BASE_ENV["PATH"])
    assert bwrap_name is not None, "bubblewrap required for network-denied replay"
    bwrap = Path(bwrap_name).resolve()
    lean = Path(
        run([f"{HOME}/.elan/bin/lake", "env", "which", "lean"], cwd=LEAN_ROOT)
        .decode().strip()
    ).resolve()
    lean_path = run(
        [f"{HOME}/.elan/bin/lake", "env", "printenv", "LEAN_PATH"], cwd=LEAN_ROOT
    ).decode().strip()
    version = run([str(lean), "--version"]).decode()
    assert "4.29.0" in version and LEAN_COMMIT in version
    assert sha256(lean) == LEAN_SHA256
    lake = Path(f"{HOME}/.elan/bin/lake").resolve()
    assert sha256(lake) == LAKE_SHA256
    assert sha256(bwrap) == BWRAP_SHA256
    assert sha256(Path(sys.executable).resolve()) == PYTHON_SHA256
    assert sha256(Path("/usr/bin/git").resolve()) == GIT_SHA256

    vendor_output = run(
        ["/usr/bin/python3", "-I", "-B", str(HERE / "build_vendor_manifest.py")],
        timeout=120,
    )
    assert vendor_output.startswith(b"PASS THM-M-0034 vendor closure:")
    outputs = replay(lean, lean_path, bwrap)
    proof_audit = outputs["proof_audit"].decode("utf-8")
    validation_output = outputs["validation"].decode("utf-8")
    for declaration in (
        "quillenSuslin",
        "Stage1Instances.THM_M_0034.quillenSuslinTarget",
    ):
        assert_axioms(proof_audit, declaration)
    for declaration in (
        "quillenSuslin",
        "Stage1Instances.THM_M_0034.Validation.differentialQuillenSuslinTarget",
    ):
        assert_axioms(validation_output, declaration)
    assert proof_audit.count("Declarations are sorry-free!") == 2
    assert validation_output.count("Declarations are sorry-free!") == 2
    assert "declaration uses 'sorry'" not in proof_audit + validation_output
    closure_match = re.search(
        r"VALIDATION_CLOSURE declarations=(\d+) modules=(\d+)", validation_output
    )
    assert closure_match is not None
    observed_closure = {
        "declarations": int(closure_match.group(1)),
        "modules": int(closure_match.group(2)),
    }
    assert observed_closure == EXPECTED_CLOSURE
    assert "VALIDATION_CLOSURE axioms=[propext, Classical.choice, Quot.sound]" in validation_output
    assert "VALIDATION_CLOSURE bodyless_nonaxioms=[]" in validation_output
    assert "VALIDATION_CLOSURE unsafe=[]" in validation_output
    assert not list(HERE.rglob("*.olean")) and not list(HERE.rglob("*.ilean"))

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest_blocked"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["release_grade"] is False and receipt["verdict"] == "blocked"
    assert receipt["target"]["elaborated_expression_sha256"] == TARGET_EXPRESSION_SHA256
    assert receipt["target"]["registry_denominator_sha256"] == REGISTRY_DENOMINATOR_SHA256
    assert receipt["result"]["root_kernel_inhabitant_observed"] is True
    assert receipt["result"]["covered_frozen_obligation_ids"] == []
    assert receipt["result"]["accepted_closed_obligation_ids"] == []
    assert receipt["result"]["frozen_graph_root_closed"] is False
    assert receipt["result"]["audit_complete"] is False
    assert receipt["result"]["theorem_complete"] is False
    assert receipt["trust"]["observed_axioms"] == sorted(EXPECTED_AXIOMS)
    assert receipt["trust"]["validation_closure"] == {
        **EXPECTED_CLOSURE,
        "bodyless_nonaxioms": [],
        "unsafe_declarations": [],
    }
    receipt_environment = receipt["environment"]
    assert receipt_environment["platform"] == "Linux 7.0.0-27-generic x86_64"
    assert receipt_environment["toolchain"] == TOOLCHAIN
    assert receipt_environment["lean_commit"] == LEAN_COMMIT
    assert receipt_environment["lean_executable_sha256"] == LEAN_SHA256
    assert receipt_environment["lake_executable_sha256"] == LAKE_SHA256
    assert receipt_environment["bubblewrap_executable_sha256"] == BWRAP_SHA256
    assert receipt_environment["python_executable_sha256"] == PYTHON_SHA256
    assert receipt_environment["git_executable_sha256"] == GIT_SHA256
    assert receipt_environment["mathlib_revision"] == MATHLIB_REVISION
    assert receipt_environment["mathlib_tree"] == MATHLIB_TREE
    assert receipt_environment["mathlib_origin"] == MATHLIB_REMOTE
    assert receipt_environment["mathlib_license_sha256"] == sha256(MATHLIB / "LICENSE")
    assert receipt_environment["mathlib_source_clean"] is True
    assert receipt_environment["cache_classification"] == "shared_warm_cache_nonrelease"
    assert receipt["recipe"] == recipe
    assert receipt["inputs"]["check_validation.py"] == sha256(Path(__file__))
    for name, expected in EXPECTED_INPUTS.items():
        assert receipt["inputs"][name] == expected
    for name, expected in EXPECTED_TOOL_INPUTS.items():
        assert receipt["inputs"][name] == expected
    assert receipt["output_evidence"]["stdout_semantic_sha256"] == digest(
        ("\n".join(SUMMARY_LINES) + "\n").encode("utf-8")
    )
    assert receipt["first_failed_gate"] == (
        "dependency.S56-M-0034-PROOF.master_acceptance_and_frozen_route_reconciliation"
    )

    packet_path = args.worker_packet
    if packet_path is not None:
        packet_path = (ROOT / packet_path).resolve() if not packet_path.is_absolute() else packet_path
        packet = load(packet_path)
        assert set(packet) == {
            "item_id", "changed_paths", "commands", "output_summary",
            "base_revision", "known_failures", "state",
        }
        assert packet["item_id"] == ITEM and packet["state"] == "[_]"
        assert packet["base_revision"] == BASE_REVISION
        assert set(packet["changed_paths"]) == CHANGED_PATHS
        assert packet["known_failures"] == receipt["known_failures"]
        assert len(packet["commands"]) == len(receipt["commands_and_results"])
        for packet_command, receipt_command in zip(
            packet["commands"], receipt["commands_and_results"], strict=True
        ):
            assert packet_command["cwd"] == receipt_command["cwd"]
            assert packet_command["argv"] == receipt_command["argv"]
            assert packet_command["exit_code"] == receipt_command["exit_code"]
            assert packet_command["output_summary"]
        assert "validation phase complete=false" in packet["output_summary"].lower()
        assert "accepted=false" in packet["output_summary"].lower()
        assert "theorem_complete=false" in packet["output_summary"].lower()

    status = git("status", "--short", "--untracked-files=all")
    actual_changes = {
        line[3:] for line in status.splitlines()
        if line[3:] != "Formalizations/Lean/.lake"
        and not line[3:].startswith("Formalizations/Lean/.lake/")
    }
    assert actual_changes == CHANGED_PATHS, (actual_changes, CHANGED_PATHS)
    assert all(
        path == ".stage1-worker-selftest.json"
        or path.startswith(f"Stage1_Instances/{THEOREM}/")
        for path in actual_changes
    )
    for path in (
        Path(__file__), HERE / "Validation.lean", HERE / "validation-spec.json",
        HERE / "validation-receipt.json", HERE / "validation-phase.md",
        ROOT / ".stage1-worker-selftest.json",
    ):
        assert_text_hygiene(path)

    print("\n".join(SUMMARY_LINES))


if __name__ == "__main__":
    main()
