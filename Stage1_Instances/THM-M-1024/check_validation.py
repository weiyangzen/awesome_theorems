#!/usr/bin/env python3
"""Fail-closed narrow validator for S56-M-1024-VALIDATION."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import platform
import re
import shutil
import subprocess
import sys
import tempfile
import time


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-1024"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM = "S56-M-1024-VALIDATION"
THEOREM = "THM-M-1024"
BASE_REVISION = "400502797d73f88ee509ece5b25ced4e9b673e60"
BASE_TREE = "cd02fcbdbec1453085a80874225b6532d7dca222"
STATEMENT_SHA256 = "197a7197043d6645b3a2e0a190c57571f93521686da2a84a264faef959481a87"
DENOMINATOR_SHA256 = "09ae507f5852e0e927272c16a31701c7b4e7a9f69359716285d2a915bdb44921"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MATHLIB_REMOTE = "https://github.com/leanprover-community/mathlib4.git"
MATHLIB_LICENSE_SHA256 = "b40930bbcf80744c86c46a12bc9da056641d722716c378f5659b9e555ef833e1"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
LEAN_EXECUTABLE_SHA256 = "3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf"
LAKE_EXECUTABLE_SHA256 = "840179e70803ef373c2ec53342d6a45ea7d022533e4145489fc1278b4f716385"
BWRAP_SHA256 = "0abea81db798ebf6b4742ac0664802d97521547a353c2a0dbdc21d76cbbfd2c0"
LEAN_TOOLCHAIN_SHA256 = "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2"
LAKE_MANIFEST_SHA256 = "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81"
ALLOWED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
EXPECTED_INPUTS = {
    "Statement.lean": STATEMENT_SHA256,
    "ObligationTree.lean": "a731c59b39859c7e13677bf69e2e37cd4a719e5bab5905dfa03206abba087977",
    "Proof.lean": "86057da583c3dbcd6c5b1d9b67e538e6c02bcf46124222bc57b8f143f49bcaaa",
    "AnchorAudit.lean": "3f08c7bf2d3058b5cb035cb7f5b7a13d8a2b94ef97c8ec44b10b38a8bfe83326",
    "Validation.lean": "72791eff66e79e8d5ae960ff4b46b1186f64e51c1b06a87e1c8741e20a230bbc",
    "statement.json": "9179bc579f5dbbb9d8a9744ecc5114d0a4a2a93db08b100e684672370acef084",
    "anchor-audit.json": "26013142d8d916de7a8f6662e23e8833efdcd5032d11cf039f4e0e733a396199",
    "obligation-registry.json": "805d027545115d1078b522f0499a6bf69e11825657af01e9723165e961c78ee5",
    "typed-graphs.json": "8180ffacb09d1dddabf82cc56dc8c7d573186595b7072e9207a611d13f1dc8f0",
    "validation-specs.json": "e68b817e47edc917c8cdd11d676954c6499d10c173f12314bd165d42b96f600d",
    "proof-receipt.json": "f70c580ffd4e83a308193fa790af022a2c93779ee1c2927633e8a5f79ecfe599",
    "proof-blocker.json": "7ebddf83eeea4085f14a2ed7b220a17d13b3ccc47d214d1076f94631dd679c64",
    "source_statement_crosswalk.md": "4a02885ac05a8d5738b2286243e68d2c82493d629cc3403a9c30a436bffdc9bc",
    "check_obligation_tree.py": "dbb7196f7971728398512ab6f2256a327685b5b1efaec3845bdc7d62d890abed",
}
PINNED_TERMINALS = {
    "Mathlib/MeasureTheory/Measure/CharacteristicFunction/Basic.lean": {
        "source_sha256": "c25fa7bec393a7ff980b5ab783a71e777916e0de76334b21907e1c79a199546b",
        "git_blob": "7f6995e17108894439cef647132609762bb805b6",
        "olean_sha256": "ac4c91ea6557bc04e225d37cc0206499c0822f15af19989d2ab513dc5cad53ad",
    },
    "Mathlib/Analysis/Complex/Exponential.lean": {
        "source_sha256": "7be4020bce627174404a5e22d46e85e5cc42e012ba558548f6423356fbe17949",
        "git_blob": "152c3ac77bdbf7036125453b6240dbc616c9d535",
        "olean_sha256": "16d790de38ed55ac16419d380bb21c69c09d5d1466619c8c8a9acd44e9e97f02",
    },
    "Mathlib/MeasureTheory/Integral/DominatedConvergence.lean": {
        "source_sha256": "967aff89500aeff8a1a94358c79bb3200c4e77bdfabe1e6481d2beeda67f6191",
        "git_blob": "3aeb4ace15863cef3af283800c10f7d670c3727c",
        "olean_sha256": "32b03944f8d8944801e31f10f0e8687975f5d39f0c0b4f8adab077cdd3bc8cfd",
    },
    "Mathlib/Analysis/InnerProductSpace/Basic.lean": {
        "source_sha256": "5b95dccc6230b9251744b12292942814523bf36b7cb41bd50c31d00a99296f3e",
        "git_blob": "ce79b97ec898dbf4f472a05168a30295d3c6e194",
        "olean_sha256": "6090cc49caa93bad814bcd6db2ce2cd379c21666a8949c9fd8d4b62e55b0f2e4",
    },
    "Mathlib/MeasureTheory/Group/Convolution.lean": {
        "source_sha256": "296279281139b48031f72af924ba80c5c18170d1ac41d6fe4db934e604da0c72",
        "git_blob": "9821a43e51b6efcc03fbea1af37b6e92b6dccf5a",
        "olean_sha256": "03255672f206a14c99d47073aa4a9ec581bdcdc451c3c6821ee34baca4219f65",
    },
}
LEAN_MODULES = ("Statement.lean", "ObligationTree.lean", "Proof.lean", "AnchorAudit.lean", "Validation.lean")
AXIOM_DECLARATIONS = {
    "ObligationTree.lean": ("root_of_packages",),
    "Proof.lean": (
        "integrable_compensatedIntegrand",
        "integrable_levyExponent_jump",
        "levyExponent_zero",
        "continuous_integral_compensatedIntegrand",
        "continuous_levyExponent",
    ),
    "Validation.lean": (
        "directCompensatedIntegrand_zero_left",
        "directLevyExponent_zero",
        "directMeasurableCompensatedIntegrand",
        "directConditionalRoot",
    ),
}
EXPECTED_COVERED_OBLIGATIONS = {
    "M1024-S-DEFINITIONS",
    "M1024-S-CONVENTIONS",
    "M1024-S-BOUNDARY",
    "M1024-N-EXPONENT",
    "M1024-T-ASSEMBLE",
}
EXPECTED_COVERED_DECLARATIONS = {
    "Stage1Instances.THM_M_1024.root_of_packages",
    *{
        f"Stage1Instances.THM_M_1024.{name}"
        for name in (
            "compensatedIntegrand_zero_right",
            "compensatedIntegrand_zero_left",
            "levyExponent_zero",
            "measurable_compensatedIntegrand",
            "norm_compensatedIntegrand_le_two",
            "norm_compensatedIntegrand_le",
            "integrable_compensatedIntegrand",
            "integrable_levyExponent_jump",
            "continuous_integral_compensatedIntegrand",
            "continuous_levyExponent",
        )
    },
    *{
        f"Stage1Instances.THM_M_1024.Validation.{name}"
        for name in (
            "directCompensatedIntegrand_zero_left",
            "directLevyExponent_zero",
            "directMeasurableCompensatedIntegrand",
            "directConditionalRoot",
        )
    },
}
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/Validation.lean",
    f"Stage1_Instances/{THEOREM}/check_validation.py",
    f"Stage1_Instances/{THEOREM}/validation-phase.md",
    f"Stage1_Instances/{THEOREM}/validation-receipt.json",
    f"Stage1_Instances/{THEOREM}/validation-spec.json",
}
SUMMARY_LINES = (
    "PASS THM-M-1024 narrow validation",
    "PASS network-isolated trust-zero replay: exact statement, conditional composition, ten partial proof bodies, anchor probe, and four differential probes elaborated",
    "PASS trust observation: ten reports list exactly propext, Classical.choice, and Quot.sound",
    "PASS selected provenance: frozen hashes, clean mathlib pin, five source/blob/olean identities, license, and tool identities agree",
    "OPEN root: no forward, converse, or uniqueness package body; audit_complete=false; theorem_complete=false",
    "FAIL CLOSED authority: proof is worker-provisional and not master-accepted",
    "FAIL CLOSED release: incomplete trust/provenance, warm shared cache, and no distinct signed independent verifier",
)
STARTED = time.monotonic()
RECIPE_TIMEOUT_SECONDS = 600.0


if sys.flags.optimize:
    raise SystemExit("validation failed: Python optimization disables fail-closed assertions")


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
    timeout: float | None = None,
) -> str:
    remaining = RECIPE_TIMEOUT_SECONDS - (time.monotonic() - STARTED)
    if remaining <= 0:
        raise TimeoutError("validation recipe exceeded its 600-second wall-clock bound")
    limit = remaining if timeout is None else min(remaining, timeout)
    result = subprocess.run(
        argv,
        cwd=cwd,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=limit,
        check=False,
    )
    if result.returncode:
        raise RuntimeError(
            f"validation failed ({result.returncode}): {argv!r}\n{result.stdout}"
        )
    return result.stdout


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["git", *args], cwd=cwd, timeout=30).strip()


def source_without_comments(source: str) -> str:
    output: list[str] = []
    index = 0
    depth = 0
    while index < len(source):
        if depth == 0 and source.startswith("--", index):
            newline = source.find("\n", index)
            if newline < 0:
                break
            output.append("\n")
            index = newline + 1
        elif source.startswith("/-", index):
            depth += 1
            index += 2
        elif depth and source.startswith("-/", index):
            depth -= 1
            index += 2
        elif depth:
            if source[index] == "\n":
                output.append("\n")
            index += 1
        else:
            output.append(source[index])
            index += 1
    assert depth == 0, "unterminated Lean block comment"
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
    assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())


def main() -> None:
    os.umask(0o022)
    os.environ["LANG"] = "C.UTF-8"
    os.environ["LC_ALL"] = "C.UTF-8"
    os.environ["TZ"] = "UTC"

    spec = load(HERE / "validation-spec.json")
    receipt = load(HERE / "validation-receipt.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")
    statement = load(HERE / "statement.json")
    anchor = load(HERE / "anchor-audit.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    frozen_specs = load(HERE / "validation-specs.json")
    proof_receipt = load(HERE / "proof-receipt.json")
    proof_blocker = load(HERE / "proof-blocker.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE

    targets = load(ROOT / "Docs" / "Stage1_Targets_rev-5.6.json")
    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 500
    assert target["target_lane"] == "hard_mathlib_anchor_and_wrapper"
    assert target["baseline"] == "L0" and target["lifecycle_mode"] == "planned"
    assert target["rework_required"] is True and target["theorem_complete"] is False

    execution = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item == {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 500,
        "phase": "validation",
        "layer": 5,
        "state": "[ ]",
        "depends_on": ["S56-M-1024-PROOF"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Run hermetic kernel, trust, provenance, and independent validation gates.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }
    predecessor = next(row for row in execution["items"] if row["id"] == "S56-M-1024-PROOF")
    assert predecessor["state"] == "[_]" and predecessor["attempts"] == 1

    for name, expected in EXPECTED_INPUTS.items():
        assert sha256(HERE / name) == expected, f"stale validation input: {name}"
    assert sha256(LEAN_ROOT / "lean-toolchain") == LEAN_TOOLCHAIN_SHA256
    assert sha256(LEAN_ROOT / "lake-manifest.json") == LAKE_MANIFEST_SHA256
    formal = statement["canonical_formal_target"]
    assert formal["declaration_or_expression"] == (
        "Stage1Instances.THM_M_1024.LevyKhintchineTarget"
    )
    assert formal["statement_file_sha256"] == STATEMENT_SHA256
    assert registry["root_obligation_id"] == graphs["root_node_id"] == "M1024-ROOT"
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    closure = graphs["closure_boundary"]
    assert closure["closed_obligations"] == [
        "M1024-S-BOUNDARY",
        "M1024-S-CONVENTIONS",
        "M1024-S-DEFINITIONS",
        "M1024-T-ASSEMBLE",
    ]
    assert closure["root_closed"] is False
    assert closure["audit_complete"] is closure["theorem_complete"] is False
    assert closure["remaining_root_cut_set"] == [
        "M1024-T-FORWARD",
        "M1024-T-CONVERSE",
        "M1024-T-UNIQUENESS",
    ]
    root = next(node for node in graphs["nodes"] if node["obligation_id"] == "M1024-ROOT")
    assert (root["human_debt"], root["machine_debt"], root["readability_debt"]) == (
        "H1", "M3", "R3"
    )
    assert graphs["graphs"]["evidence"]["edges"] == []

    assert proof_receipt["accepted"] is False
    assert proof_receipt["proposed_state"] == "[_]"
    assert proof_receipt["supported_obligation_ids"] == []
    assert proof_receipt["partial_progress_toward_obligation_ids"] == ["M1024-N-EXPONENT"]
    assert proof_receipt["provisionally_closed_obligation_ids"] == []
    assert proof_receipt["accepted_closed_obligation_ids"] == []
    assert proof_receipt["proof_body"]["source_sha256"] == sha256(HERE / "Proof.lean")
    assert proof_receipt["result"]["root_kernel_closed"] is False
    assert proof_receipt["result"]["theorem_complete"] is False
    assert proof_receipt["remaining_root_cut_set"] == closure["remaining_root_cut_set"]
    assert proof_blocker["root_closed"] is proof_blocker["audit_complete"] is False
    assert proof_blocker["theorem_complete"] is False
    assert anchor["root_machine_classification"] == "M3"
    assert anchor["mathlib"]["exact_candidate_found"] is False

    # These old recipes establish architecture only, not any named mathematical closure.
    assert frozen_specs["item_id"] == "S56-M-1024-OBLIGATION_TREE"
    assert len(frozen_specs["recipes"]) == 24
    assert {tuple(recipe["argv"]) for recipe in frozen_specs["recipes"]} == {
        ("python3", f"Stage1_Instances/{THEOREM}/check_obligation_tree.py")
    }

    manifest = load(LEAN_ROOT / "lake-manifest.json")
    mathlib_pin = next(row for row in manifest["packages"] if row["name"] == "mathlib")
    assert mathlib_pin["rev"] == mathlib_pin["inputRev"] == MATHLIB_REVISION
    assert MATHLIB.resolve().is_dir()
    assert git("rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert git("status", "--porcelain=v1", "--untracked-files=all", cwd=MATHLIB) == ""
    assert git("remote", "get-url", "origin", cwd=MATHLIB) == MATHLIB_REMOTE
    assert sha256(MATHLIB / "LICENSE") == MATHLIB_LICENSE_SHA256
    olean_root = MATHLIB / ".lake" / "build" / "lib" / "lean"
    for relative, expected in PINNED_TERMINALS.items():
        source = MATHLIB / relative
        olean = olean_root / relative.replace(".lean", ".olean")
        assert sha256(source) == expected["source_sha256"]
        assert git("rev-parse", f"HEAD:{relative}", cwd=MATHLIB) == expected["git_blob"]
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
        assert prohibited.search(source) is None, f"prohibited proof construct in {name}"
    validation = source_without_comments((HERE / "Validation.lean").read_text(encoding="utf-8"))
    for forbidden in ("import Proof", "import ObligationTree", "root_of_packages", "compensatedIntegrand"):
        assert forbidden not in validation, forbidden
    for marker in (
        "theorem directCompensatedIntegrand_zero_left",
        "theorem directLevyExponent_zero",
        "theorem directMeasurableCompensatedIntegrand",
        "theorem directConditionalRoot",
    ):
        assert marker in validation
    assert not list(HERE.glob("*.olean")) and not list(HERE.glob("tmp*.lean"))

    lake_name = shutil.which("lake")
    bwrap_name = shutil.which("bwrap")
    assert lake_name is not None and bwrap_name is not None
    lake = Path(lake_name).resolve()
    bwrap = Path(bwrap_name).resolve()
    assert sha256(lake) == LAKE_EXECUTABLE_SHA256
    assert sha256(bwrap) == BWRAP_SHA256
    lean = Path(run([str(lake), "env", "which", "lean"], cwd=LEAN_ROOT, timeout=60).strip())
    lean_path = run(
        ["env", "-u", "LEAN_PATH", str(lake), "env", "printenv", "LEAN_PATH"],
        cwd=LEAN_ROOT,
        timeout=60,
    ).strip()
    assert lean.is_file() and sha256(lean) == LEAN_EXECUTABLE_SHA256
    assert "Lean (version 4.29.0" in run([str(lean), "--version"], timeout=30)
    assert LEAN_COMMIT in run([str(lean), "--version"], timeout=30)
    assert "Lake version 5.0.0" in run([str(lake), "--version"], cwd=LEAN_ROOT, timeout=30)

    outputs: dict[str, str] = {}
    with tempfile.TemporaryDirectory(prefix="m1024-validation-", dir="/tmp") as tmp_name:
        tmp = Path(tmp_name).resolve()
        for name in LEAN_MODULES:
            shutil.copy2(HERE / name, tmp / name)
        base = [
            str(bwrap),
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
            str(lean), "--trust=0", "-t0", "--root", str(tmp),
        ]
        local = base.copy()
        local[local.index(lean_path)] = f"{tmp}:{lean_path}"
        outputs["Statement.lean"] = run(
            base + ["-o", "Statement.olean", "Statement.lean"], timeout=300
        )
        outputs["ObligationTree.lean"] = run(
            local + ["-o", "ObligationTree.olean", "ObligationTree.lean"], timeout=300
        )
        outputs["Proof.lean"] = run(
            local + ["-o", "Proof.olean", "Proof.lean"], timeout=300
        )
        outputs["Validation.lean"] = run(
            local + ["-o", "Validation.olean", "Validation.lean"], timeout=300
        )
        outputs["AnchorAudit.lean"] = run(
            base + ["AnchorAudit.lean"], timeout=300
        )

    report_count = 0
    for name, declarations in AXIOM_DECLARATIONS.items():
        for declaration in declarations:
            assert printed_axioms(outputs[name], declaration) == ALLOWED_AXIOMS
            report_count += 1
    assert report_count == 10
    all_output = "\n".join(outputs.values())
    assert "sorryAx" not in all_output and "error:" not in all_output
    module_hashes = {name: hashlib.sha256(output.encode()).hexdigest() for name, output in outputs.items()}
    kernel_output_sha256 = hashlib.sha256(
        "\n".join(outputs[name] for name in LEAN_MODULES).encode()
    ).hexdigest()

    assert spec["schema_version"] == "stage1-validation-recipe/1.0"
    assert spec["item_id"] == ITEM and spec["theorem_id"] == THEOREM
    assert spec["cwd"] == "." and spec["argv"] == [
        "python3", "-I", "-B", f"Stage1_Instances/{THEOREM}/check_validation.py"
    ]
    assert spec["timeout_seconds"] == 600
    assert spec["network_policy"] == "denied" and spec["expected_exit"] == 0
    assert set(spec["covered_obligation_ids"]) == EXPECTED_COVERED_OBLIGATIONS
    assert set(spec["covered_declarations"]) == EXPECTED_COVERED_DECLARATIONS
    proof_source = source_without_comments((HERE / "Proof.lean").read_text(encoding="utf-8"))
    proof_declarations = set(re.findall(r"^theorem\s+([A-Za-z0-9_]+)", proof_source, re.MULTILINE))
    expected_proof_names = {
        name.rsplit(".", 1)[-1]
        for name in EXPECTED_COVERED_DECLARATIONS
        if ".Validation." not in name and name != "Stage1Instances.THM_M_1024.root_of_packages"
    }
    assert proof_declarations == expected_proof_names

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["phase"] == "validation" and receipt["intent"] == "validate"
    assert receipt["verdict"] == "blocked"
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["release_grade"] is receipt["content_addressed_release_evidence"] is False
    assert receipt["canonical_target"]["statement_file_sha256"] == STATEMENT_SHA256
    assert receipt["canonical_target"]["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert "elaborated_expression_sha256" not in receipt["canonical_target"]
    assert receipt["validation_spec"] == {
        "path": f"Stage1_Instances/{THEOREM}/validation-spec.json",
        "sha256": sha256(HERE / "validation-spec.json"),
    }
    for key in (
        "recipe_id", "cwd", "argv", "env_allowlist", "timeout_seconds",
        "network_policy", "network_enforcement", "expected_exit", "expected_outputs",
        "covered_obligation_ids", "covered_declarations",
    ):
        assert receipt["recipe"][key] == spec[key], key
    assert receipt["worktree"]["tracked_changes"] == []
    assert receipt["worktree"]["pre_existing_untracked"] == ["Formalizations/Lean/.lake"]
    assert receipt["worktree"]["validation_untracked_sha256"] == {
        relative: sha256(ROOT / relative)
        for relative in sorted(CHANGED_PATHS - {"Stage1_Instances/THM-M-1024/validation-receipt.json"})
    }
    assert receipt["worktree"]["self_referential_receipt_hash"] == "not_applicable"
    for name, expected in EXPECTED_INPUTS.items():
        assert receipt["inputs"][name] == expected
    assert receipt["inputs"]["validation-spec.json"] == sha256(HERE / "validation-spec.json")
    assert receipt["inputs"]["validation_verifier_sha256"] == sha256(Path(__file__).resolve())
    assert receipt["inputs"]["lean-toolchain"] == LEAN_TOOLCHAIN_SHA256
    assert receipt["inputs"]["lake-manifest.json"] == LAKE_MANIFEST_SHA256
    assert receipt["environment"]["platform"] == (
        f"{platform.system()} {platform.release()} {platform.machine()}"
    )
    assert receipt["environment"]["lean_executable_sha256"] == LEAN_EXECUTABLE_SHA256
    assert receipt["environment"]["lake_launcher_sha256"] == LAKE_EXECUTABLE_SHA256
    assert receipt["environment"]["bubblewrap_sha256"] == BWRAP_SHA256
    assert receipt["environment"]["mathlib_revision"] == MATHLIB_REVISION
    assert receipt["environment"]["mathlib_tree"] == MATHLIB_TREE
    receipt_terminals = receipt["provenance"]["selected_mathlib_sources"]
    for relative, expected in PINNED_TERMINALS.items():
        assert receipt_terminals[relative] == {
            "source_sha256": expected["source_sha256"],
            "git_blob": expected["git_blob"],
            "olean_sha256": expected["olean_sha256"],
        }
    assert receipt["execution"]["kernel_output_sha256"] == kernel_output_sha256
    assert receipt["execution"]["per_module_output_sha256"] == module_hashes
    assert receipt["execution"]["started_at"] < receipt["execution"]["ended_at"]
    assert isinstance(receipt["execution"]["duration_seconds"], int)
    assert receipt["execution"]["duration_seconds"] > 0
    result = receipt["result"]
    assert result["network_isolated_trust_zero_replay"] == "pass"
    assert result["axiom_report_count"] == 10
    assert set(result["observed_axioms"]) == ALLOWED_AXIOMS
    assert result["placeholder_and_unsafe_scan"] == "pass"
    assert result["selected_provenance"] == "pass"
    assert result["root_kernel_closed"] is False
    assert result["root_machine_debt"] == "M3"
    assert result["proof_master_acceptance"] == "fail_closed"
    assert result["accepted_closed_obligation_ids"] == []
    assert result["partially_observed_obligation_ids"] == ["M1024-N-EXPONENT"]
    assert result["conditional_composition_ids"] == ["M1024-T-ASSEMBLE"]
    assert result["complete_foundation_tcb_gate"] == "fail_closed"
    assert result["complete_provenance_gate"] == "fail_closed"
    assert result["hermetic_cold_offline_replay"] == "fail_closed"
    assert result["independent_distinct_runner"] == "fail_closed"
    assert result["audit_complete"] is result["theorem_complete"] is False
    assert receipt["remaining_root_cut_set"] == closure["remaining_root_cut_set"]
    assert receipt["first_failed_gate"] == "dependency.S56-M-1024-PROOF.master_acceptance"
    assert receipt["first_failed_statement_gate"] == "S56-5.1-CANONICAL-EXPRESSION-FINGERPRINT"
    assert receipt["first_failed_theorem_gate"] == "proof.M1024-N-EXPONENT.kernel_closure"
    assert receipt["first_failed_release_gate"] == "S56-7.3-TRANSITIVE-PROVENANCE-CLOSURE"
    assert receipt["accepted_receipt_ids"] == []
    assert receipt["root_vector_before"] == receipt["root_vector_after_worker_selftest"] == {
        "H": "H1", "M": "M3", "R": "R3"
    }
    assert receipt["debt_vector_delta"] == "none"

    assert set(packet) == {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert packet["item_id"] == ITEM and packet["state"] == "[_]"
    assert packet["base_revision"] == BASE_REVISION
    assert set(packet["changed_paths"]) == set(receipt["changed_paths"]) == CHANGED_PATHS
    assert packet["known_failures"] == receipt["known_failures"]
    assert packet["commands"] == [row["command"] for row in receipt["commands"]]
    assert {row["exit_code"] for row in receipt["commands"]} == {0}
    status = git("status", "--short", "--untracked-files=all")
    actual_changes = {
        line[3:] for line in status.splitlines()
        if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual_changes == CHANGED_PATHS, (actual_changes, CHANGED_PATHS)
    for relative in CHANGED_PATHS:
        assert_text_hygiene(ROOT / relative)

    stdout = "\n".join(SUMMARY_LINES) + "\n"
    assert receipt["execution"]["stdout_sha256"] == hashlib.sha256(stdout.encode()).hexdigest()
    print("\n".join(SUMMARY_LINES))


if __name__ == "__main__":
    main()
