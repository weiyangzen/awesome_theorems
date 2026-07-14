#!/usr/bin/env python3
"""Fail-closed narrow validator for S56-M-1026-VALIDATION."""

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
HERE = ROOT / "Stage1_Instances" / "THM-M-1026"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM = "S56-M-1026-VALIDATION"
THEOREM = "THM-M-1026"
BASE_REVISION = "a1a7e939e58f103f5ff5d23af51437fa8658aa04"
BASE_TREE = "d881fd9641fa3e5f3ebe5082b35672981e90adcf"
TARGET_EXPRESSION = "e39476697d12d054b84ab39c07251418d449ba5ea094c2bb37df9850c7caff93"
REGISTRY_DENOMINATOR = "e74cb65a6278468b7696e4ce10a93ccbe318c57ff57bf51b541680529880f3b2"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MATHLIB_REMOTE = "https://github.com/leanprover-community/mathlib4.git"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
EXPECTED_AXIOMS = ["propext", "Classical.choice", "Quot.sound"]
EXPECTED_INPUTS = {
    "Statement.lean": "f70d267d426daf28a4fbf912fa4215c5f27095a347fe714d83a4cd31eb605e8b",
    "ObligationTree.lean": "3429c56a3a6acaae51ca5858970e5337acbe5e312a32c4fe4cb42a4ea4bd19ed",
    "Proof.lean": "fb6670299962b85b1fd46f56b2511c8e872ff906bee9e032eb707bde0fbd2830",
    "Validation.lean": "e731491f6697d5d1946afa3ffe92c9f98e21a4e95317152eefed8a40c6e81830",
    "statement.json": "7501509afc67633c57b3eb26c937efa4f885d092d1f4c7df63a54dec1b4f7157",
    "anchor-audit.json": "c410a4e19149d6919ea6ef539c52585c26dfc3d5cc825d712f35fc57d36d42b8",
    "obligation-registry.json": "35ab2cdaf9fe3175eef9871a78cee8f7c27d98f94087c80a868e132d9c83f415",
    "typed-graphs.json": "f5cf4765e0825cb911fcb46f449ee0abd1264881c058ba9815567cadf82667d6",
    "validation-specs.json": "180646d0ed9036a227eaaacd0b03203996189a36bd575d16821fdbfdf75004bd",
    "proof-phase.json": "3c2681c2fb8c75159dfc303ec27a6713fa5df01a8a06376b004306eab1c6f72b",
    "proof-receipt.json": "23a90245dc4abf2385ff612746bfc58ae3fce18a34aa9f47f2862efec28a04db",
    "proof-blocker.json": "dfbcbe46ca62d94eed5ff584cefda474f38a2467344d59d8243fed0230e1d1c8",
}
EXPECTED_TOOL_INPUTS = {
    "lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
SELECTED_MATHLIB_INPUTS = {
    "Mathlib/MeasureTheory/Integral/BoundedContinuousFunction.lean": {
        "blob": "a771b55a86d70d2b8a1c36d9ac4063c6384eb294",
        "source": "89618242d6107158d2282a5d61c0a6880e964ed97619e355ab0f4f7afaa1be99",
        "olean": "e0c66c363273167eeb198c215989bc5444424c89cc5890147b2251b3fec70525",
    },
    "Mathlib/MeasureTheory/Group/Convolution.lean": {
        "blob": "9821a43e51b6efcc03fbea1af37b6e92b6dccf5a",
        "source": "296279281139b48031f72af924ba80c5c18170d1ac41d6fe4db934e604da0c72",
        "olean": "03255672f206a14c99d47073aa4a9ec581bdcdc451c3c6821ee34baca4219f65",
    },
    "Mathlib/MeasureTheory/Measure/CharacteristicFunction/Basic.lean": {
        "blob": "7f6995e17108894439cef647132609762bb805b6",
        "source": "c25fa7bec393a7ff980b5ab783a71e777916e0de76334b21907e1c79a199546b",
        "olean": "ac4c91ea6557bc04e225d37cc0206499c0822f15af19989d2ab513dc5cad53ad",
    },
    "Mathlib/MeasureTheory/Measure/LevyConvergence.lean": {
        "blob": "fc0bf2a7054634763040aa9bbcaae5f2c93b8d5f",
        "source": "54fa4a3baec8a8ab916524dd63c52a6da70bc919031e20318b198fa20755fff8",
        "olean": "9f5a27181b909026ed757f7fd257f83407fdcbf3315cb0560c1a65e22e994865",
    },
    "Mathlib/Probability/CentralLimitTheorem.lean": {
        "blob": "e0cfc897a4679025f71712abbf8834c1f318b2c1",
        "source": "4b42bad9589ec3772fe0e884ad70789c89fd0c11566d980f3df1c862bbc7f03d",
        "olean": "d3b747f6dd0a15d12d10d29a4cc86980a72b54d0af741dc31cf5b70a0b70b988",
    },
}
PROVISIONAL_CLOSED_IDS = [
    "M1026-B-CONVERSE",
    "M1026-C-STABLE-WITNESS",
    "M1026-L-CONSTANT-WEAK-LIMIT",
    "M1026-T-CONVERSE",
]
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/Validation.lean",
    f"Stage1_Instances/{THEOREM}/check_validation.py",
    f"Stage1_Instances/{THEOREM}/validation-phase.md",
    f"Stage1_Instances/{THEOREM}/validation-receipt.json",
    f"Stage1_Instances/{THEOREM}/validation-spec.json",
}
SUMMARY_LINES = (
    "PASS THM-M-1026 narrow validation",
    "PASS network-isolated trust-zero replay: exact statement, conditional merge, converse proof, and differential converse elaborated",
    "PASS trust observation: eight reports list exactly propext, Classical.choice, and Quot.sound",
    "PASS selected provenance: frozen hashes, clean mathlib pin, selected source blobs/oleans, license, and tools agree",
    "OPEN root: M1026-T-NECESSITY has no proof body; audit_complete=false; theorem_complete=false",
    "FAIL CLOSED authority: proof is worker-provisional and not master-accepted",
    "FAIL CLOSED release: incomplete trust/provenance, warm shared cache, and no distinct signed independent verifier",
)
RECIPE_STARTED = time.monotonic()
RECIPE_TIMEOUT_SECONDS = 600.0


if sys.flags.optimize:
    raise SystemExit("validation failed: Python optimization disables fail-closed assertions")


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict), path
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(argv: list[str], *, cwd: Path = ROOT, timeout: float | None = None) -> str:
    remaining = RECIPE_TIMEOUT_SECONDS - (time.monotonic() - RECIPE_STARTED)
    if remaining <= 0:
        raise TimeoutError("validation recipe exceeded its 600-second wall-clock bound")
    result = subprocess.run(
        argv,
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=min(remaining, timeout) if timeout is not None else remaining,
        check=False,
    )
    if result.returncode:
        raise RuntimeError(
            f"validation failed ({result.returncode}): {argv!r}\n{result.stdout}"
        )
    return result.stdout


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["git", *args], cwd=cwd, timeout=30).strip()


def code_without_comments(source: str) -> str:
    source = re.sub(r"/-.*?-/", "", source, flags=re.DOTALL)
    return re.sub(r"--.*$", "", source, flags=re.MULTILINE)


def axiom_reports(output: str) -> dict[str, list[str]]:
    matches = re.findall(r"'([^']+)' depends on axioms:\s*\[([^]]*)\]", output, re.DOTALL)
    return {
        name: [part.strip() for part in raw.split(",") if part.strip()]
        for name, raw in matches
    }


def expression_chunks(output: str) -> dict[str, str]:
    names = (
        "GeneralizedCentralLimitTheorem",
        "MutationAllowsDegenerateLimit",
        "MutationAllowsZeroScale",
        "MutationGaussianOnly",
        "MutationNecessityOnly",
    )
    rendered: dict[str, str] = {}
    for index, name in enumerate(names):
        marker = f"def Stage1Instances.THM_M_1026.{name} : Prop :="
        start = output.find(marker)
        assert start >= 0, f"missing elaborated expression for {name}"
        later = [output.find(f"def Stage1Instances.THM_M_1026.{other} : Prop :=", start + 1)
                 for other in names[index + 1:]]
        ends = [position for position in later if position >= 0]
        rendered[name] = " ".join(output[start:min(ends) if ends else None].split())
    return rendered


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
    targets = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    statement = load(HERE / "statement.json")
    anchor = load(HERE / "anchor-audit.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    proof_phase = load(HERE / "proof-phase.json")
    proof_receipt = load(HERE / "proof-receipt.json")
    proof_blocker = load(HERE / "proof-blocker.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 502 and target["baseline"] == "L0"
    assert target["target_lane"] == "hard_mathlib_anchor_and_wrapper"
    assert target["lifecycle_mode"] == "planned"
    assert target["rework_required"] is True and target["theorem_complete"] is False
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item == {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 502,
        "phase": "validation",
        "layer": 5,
        "state": "[ ]",
        "depends_on": ["S56-M-1026-PROOF"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Run hermetic kernel, trust, provenance, and independent validation gates.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }
    predecessor = next(row for row in execution["items"] if row["id"] == "S56-M-1026-PROOF")
    assert predecessor["state"] == "[_]"

    formal = statement["canonical_formal_target"]
    assert formal["declaration_or_expression"] == "Stage1Instances.THM_M_1026.Statement"
    assert formal["elaborated_expression_sha256"] == TARGET_EXPRESSION
    assert formal["statement_file_sha256"] == EXPECTED_INPUTS["Statement.lean"]
    assert anchor["target"] == "Stage1Instances.THM_M_1026.Statement"
    assert anchor["theorem_complete"] is False
    assert registry["root_obligation_id"] == "M1026-ROOT"
    assert registry["denominator_sha256"] == REGISTRY_DENOMINATOR
    assert graphs["registry_denominator_sha256"] == REGISTRY_DENOMINATOR
    closure = graphs["closure_boundary"]
    assert closure["root_closed"] is closure["theorem_complete"] is False
    assert closure["root_machine_debt"] == "M3"
    assert closure["remaining_root_cut_set"] == ["M1026-T-NECESSITY", "M1026-T-CONVERSE"]

    assert proof_phase["canonical_expression_sha256"] == TARGET_EXPRESSION
    assert proof_phase["closed_obligation_ids"] == PROVISIONAL_CLOSED_IDS
    assert proof_phase["remaining_root_cut_set"] == ["M1026-T-NECESSITY"]
    assert proof_phase["root_closed"] is proof_phase["theorem_complete"] is False
    assert proof_receipt["item_id"] == "S56-M-1026-PROOF"
    assert proof_receipt["accepted"] is False and proof_receipt["proposed_state"] == "[_]"
    assert proof_receipt["closed_obligation_ids"] == PROVISIONAL_CLOSED_IDS
    assert proof_receipt["remaining_root_cut_set"] == ["M1026-T-NECESSITY"]
    assert proof_receipt["result"]["axioms"] == EXPECTED_AXIOMS
    assert proof_receipt["result"]["root_closed"] is False
    assert proof_blocker["first_failed_gate"] == "M1026-C-BLOCK-DECOMPOSITION"
    assert proof_blocker["remaining_root_cut_set"] == ["M1026-T-NECESSITY"]
    assert proof_blocker["root_closed"] is proof_blocker["theorem_complete"] is False

    for name, expected in EXPECTED_INPUTS.items():
        assert sha256(HERE / name) == expected, f"stale validation input: {name}"
        assert receipt["inputs"][name] == expected, name
    for name, expected in EXPECTED_TOOL_INPUTS.items():
        assert sha256(LEAN_ROOT / name) == expected, f"changed tool input: {name}"
        receipt_key = name if name == "lake-manifest.json" else "lean-toolchain"
        assert receipt["inputs"][receipt_key] == expected, name
    for name in ("validation-spec.json", "check_validation.py", "validation-phase.md"):
        assert receipt["inputs"][name] == sha256(HERE / name), name

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|implemented_by|native_decide)\b|"
        r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
        r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
        r"(?:axiom|constant|opaque|unsafe|extern)\b",
        re.MULTILINE,
    )
    for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
        code = code_without_comments((HERE / name).read_text(encoding="utf-8"))
        assert prohibited.search(code) is None, f"prohibited proof device in {name}"
    differential = code_without_comments((HERE / "Validation.lean").read_text(encoding="utf-8"))
    assert "import Proof" not in differential
    assert "Stage1Instances.THM_M_1026.Proof" not in differential
    assert "independentlyReconstructedConverse" in differential
    assert not list(HERE.glob("*.olean")) and not list(HERE.glob("tmp*.lean"))

    manifest = load(LEAN_ROOT / "lake-manifest.json")
    mathlib_entry = next(row for row in manifest["packages"] if row["name"] == "mathlib")
    assert mathlib_entry["rev"] == mathlib_entry["inputRev"] == MATHLIB_REVISION
    assert MATHLIB.resolve().is_dir(), "pinned mathlib artifact is unavailable"
    assert git("rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert git("remote", "get-url", "origin", cwd=MATHLIB) == MATHLIB_REMOTE
    assert git("status", "--porcelain=v1", cwd=MATHLIB) == ""
    for relative, expected in SELECTED_MATHLIB_INPUTS.items():
        assert git("rev-parse", f"HEAD:{relative}", cwd=MATHLIB) == expected["blob"]
        assert sha256(MATHLIB / relative) == expected["source"]
        olean = MATHLIB / ".lake" / "build" / "lib" / "lean" / Path(relative).with_suffix(".olean")
        assert sha256(olean) == expected["olean"]
        assert receipt["provenance"]["selected_mathlib_sources"][relative] == {
            "blob": expected["blob"],
            "source_sha256": expected["source"],
            "olean_sha256": expected["olean"],
        }
    assert sha256(MATHLIB / "LICENSE") == "b40930bbcf80744c86c46a12bc9da056641d722716c378f5659b9e555ef833e1"

    bwrap_name = shutil.which("bwrap")
    assert bwrap_name is not None, "bubblewrap is required for network-denied Lean replay"
    lean = Path(run(["lake", "env", "which", "lean"], cwd=LEAN_ROOT, timeout=60).strip())
    lake = Path(run(["lake", "env", "which", "lake"], cwd=LEAN_ROOT, timeout=60).strip())
    lean_path = run(["lake", "env", "printenv", "LEAN_PATH"], cwd=LEAN_ROOT, timeout=60).strip()
    lean_version = run(["lake", "env", "lean", "--version"], cwd=LEAN_ROOT, timeout=60)
    lake_version = run(["lake", "env", "lake", "--version"], cwd=LEAN_ROOT, timeout=60)
    assert "4.29.0" in lean_version and LEAN_COMMIT in lean_version
    assert "5.0.0-src+98dc76e" in lake_version
    python = Path(os.path.realpath(sys.executable))
    git_path = Path(os.path.realpath(shutil.which("git") or ""))
    bwrap = Path(bwrap_name).resolve()
    environment = receipt["environment"]
    assert environment["platform"] == f"{platform.system()} {platform.release()} {platform.machine()}"
    assert environment["lean_executable_sha256"] == sha256(lean)
    assert environment["lake_executable_sha256"] == sha256(lake)
    assert environment["python_executable_sha256"] == sha256(python)
    assert environment["git_executable_sha256"] == sha256(git_path)
    assert environment["bubblewrap_executable_sha256"] == sha256(bwrap)
    assert environment["mathlib_revision"] == MATHLIB_REVISION
    assert environment["mathlib_tree"] == MATHLIB_TREE

    outputs: dict[str, str] = {}
    with tempfile.TemporaryDirectory(prefix="m1026-validation-") as tmp_name:
        tmp = Path(tmp_name).resolve()
        for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
            (tmp / name).write_bytes((HERE / name).read_bytes())
        base = [
            str(bwrap), "--ro-bind", "/", "/", "--bind", str(tmp), str(tmp),
            "--dev", "/dev", "--proc", "/proc", "--unshare-net", "--die-with-parent",
            "--setenv", "HOME", str(tmp), "--setenv", "LANG", "C.UTF-8",
            "--setenv", "LC_ALL", "C.UTF-8", "--setenv", "TZ", "UTC",
            "--setenv", "LEAN_NUM_THREADS", "1", "--chdir", str(tmp),
        ]
        outputs["Statement.lean"] = run(base + [
            "--setenv", "LEAN_PATH", lean_path, str(lean), "--trust=0", "-t0",
            "-o", "Statement.olean", "Statement.lean",
        ])
        module_path = f"{tmp}:{lean_path}"
        outputs["ObligationTree.lean"] = run(base + [
            "--setenv", "LEAN_PATH", module_path, str(lean), "--trust=0", "-t0",
            "-o", "ObligationTree.olean", "ObligationTree.lean",
        ])
        outputs["Proof.lean"] = run(base + [
            "--setenv", "LEAN_PATH", module_path, str(lean), "--trust=0", "-t0", "Proof.lean",
        ])
        outputs["Validation.lean"] = run(base + [
            "--setenv", "LEAN_PATH", module_path, str(lean), "--trust=0", "-t0",
            "Validation.lean",
        ])

    rendered = expression_chunks(outputs["Statement.lean"])
    canonical = rendered["GeneralizedCentralLimitTheorem"]
    assert hashlib.sha256(canonical.encode()).hexdigest() == TARGET_EXPRESSION
    assert all(value != canonical for name, value in rendered.items()
               if name != "GeneralizedCentralLimitTheorem")
    tree_reports = axiom_reports(outputs["ObligationTree.lean"])
    assert tree_reports == {
        "Stage1Instances.THM_M_1026.ObligationTree.root_of_directions": EXPECTED_AXIOMS,
    }
    proof_reports = axiom_reports(outputs["Proof.lean"])
    assert proof_reports == {
        "Stage1Instances.THM_M_1026.Proof.stable_normalizers": EXPECTED_AXIOMS,
        "Stage1Instances.THM_M_1026.Proof.weaklyConverges_of_eventually_eq": EXPECTED_AXIOMS,
        "Stage1Instances.THM_M_1026.Proof.converseTerminal": EXPECTED_AXIOMS,
    }
    validation_reports = axiom_reports(outputs["Validation.lean"])
    assert validation_reports == {
        "Stage1Instances.THM_M_1026.Validation.independentlyReconstructedStableNormalizers": EXPECTED_AXIOMS,
        "Stage1Instances.THM_M_1026.Validation.independentlyReconstructedWeakLimit": EXPECTED_AXIOMS,
        "Stage1Instances.THM_M_1026.Validation.independentlyReconstructedConverse": EXPECTED_AXIOMS,
        "Stage1Instances.THM_M_1026.Validation.independentlyReconstructedConditionalRoot": EXPECTED_AXIOMS,
    }
    combined = "".join(outputs.values())
    assert "sorryAx" not in combined and "declaration uses 'sorry'" not in combined
    assert "error:" not in combined
    kernel_digest = hashlib.sha256("".join(
        f"{name}\0{outputs[name]}" for name in
        ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean")
    ).encode()).hexdigest()
    assert receipt["execution"]["kernel_output_sha256"] == kernel_digest, (
        kernel_digest, receipt["execution"]["kernel_output_sha256"]
    )
    module_output_hashes = {
        name: hashlib.sha256(output.encode()).hexdigest()
        for name, output in outputs.items()
    }
    if receipt["execution"]["per_module_output_sha256"] != module_output_hashes:
        print(json.dumps({"per_module_output_sha256": module_output_hashes}, sort_keys=True))
        raise AssertionError("per-module output hashes differ")
    assert receipt["execution"]["raw_logs"] == (
        "ephemeral temporary files removed after semantic hashes were computed"
    )

    assert spec["schema_version"] == "stage1-validation-recipe/1.0"
    assert spec["item_id"] == ITEM and spec["theorem_id"] == THEOREM
    assert spec["cwd"] == "."
    assert spec["argv"] == [
        "python3", "-I", "-B", f"Stage1_Instances/{THEOREM}/check_validation.py"
    ]
    assert spec["env_allowlist"] == {
        "PATH": "runner-provided command discovery; every resolved executable is content-hash checked",
        "HOME": "runner-provided only for Lake/Elan discovery; inner Lean sandbox overrides HOME with a fresh temporary directory",
        "LANG": "C.UTF-8",
        "LC_ALL": "C.UTF-8",
        "TZ": "UTC",
    }
    assert spec["timeout_seconds"] == 600
    assert spec["network_policy"] == "denied" and spec["expected_exit"] == 0
    assert "--unshare-net" in spec["network_enforcement"]
    assert spec["expected_outputs"] == [{
        "path_or_stream": "stdout",
        "semantic_hash_policy": "exact seven-line PASS/OPEN/FAIL-CLOSED status summary",
    }]
    for key in (
        "recipe_id", "cwd", "argv", "env_allowlist", "timeout_seconds",
        "network_policy", "network_enforcement", "expected_exit", "expected_outputs",
        "covered_obligation_ids", "covered_declarations",
    ):
        assert receipt["recipe"][key] == spec[key], key

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["phase"] == "validation" and receipt["intent"] == "validate"
    assert receipt["depends_on"] == ["S56-M-1026-PROOF"]
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["verdict"] == "blocked"
    assert receipt["release_grade"] is receipt["content_addressed_release_evidence"] is False
    assert receipt["accepted_closed_obligation_ids"] == []
    assert receipt["provisionally_validated_closed_obligation_ids"] == PROVISIONAL_CLOSED_IDS
    result = receipt["result"]
    assert result["network_isolated_trust_zero_replay"] == "pass"
    assert result["axiom_report_count"] == 8 and result["observed_axioms"] == EXPECTED_AXIOMS
    assert result["placeholder_and_unsafe_scan"] == "pass"
    assert result["selected_provenance"] == "pass"
    assert result["proof_master_acceptance"] == "fail_closed"
    assert result["root_kernel_closed"] is False
    assert result["frozen_preproof_graph_machine_debt"] == "M3"
    assert result["proposed_root_machine_debt_after_proof_acceptance"] == "M2"
    assert result["frozen_preproof_graph_remaining_root_cut_set"] == [
        "M1026-T-NECESSITY", "M1026-T-CONVERSE"
    ]
    assert result["proposed_remaining_root_cut_set_after_proof_acceptance"] == [
        "M1026-T-NECESSITY"
    ]
    assert result["complete_foundation_tcb_gate"] == "fail_closed"
    assert result["complete_provenance_gate"] == "fail_closed"
    assert result["hermetic_cold_offline_replay"] == "fail_closed"
    assert result["independent_distinct_runner"] == "fail_closed"
    assert result["audit_complete"] is result["theorem_complete"] is False
    assert receipt["first_failed_gate"] == "dependency.S56-M-1026-PROOF.master_acceptance"
    assert receipt["first_failed_theorem_gate"] == "proof.root_kernel_closure.M1026-T-NECESSITY"
    assert receipt["first_failed_release_gate"] == "S56-10.6-HERMETIC-COLD-BUILD"
    assert receipt["frozen_preproof_graph_remaining_root_cut_set"] == [
        "M1026-T-NECESSITY", "M1026-T-CONVERSE"
    ]
    assert receipt["proposed_remaining_root_cut_set_after_proof_acceptance"] == [
        "M1026-T-NECESSITY"
    ]
    assert receipt["lifecycle_before"] == receipt["lifecycle_after"] == "planned"
    assert receipt["frozen_preproof_graph_root_vector_before"] == (
        receipt["frozen_preproof_graph_root_vector_after"]
    ) == {
        "H": "H2", "M": "M3", "R": "R4"
    }
    assert receipt["proposed_root_vector_after_proof_acceptance"] == {
        "H": "H2", "M": "M2", "R": "R4"
    }
    assert receipt["accepted_receipt_ids"] == []

    packet = load(ROOT / ".stage1-worker-selftest.json")
    assert set(packet) == {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert packet["item_id"] == ITEM and packet["state"] == "[_]"
    assert packet["base_revision"] == BASE_REVISION
    assert set(packet["changed_paths"]) == set(receipt["changed_paths"]) == CHANGED_PATHS
    assert packet["commands"] == receipt["commands"]
    assert packet["output_summary"] == receipt["output_summary"]
    assert packet["known_failures"] == receipt["known_failures"] and packet["known_failures"]
    assert all(command["exit_code"] == 0 for command in packet["commands"])
    status = git(
        "status", "--porcelain=v1", "--untracked-files=all", "--",
        str(HERE), str(ROOT / ".stage1-worker-selftest.json"),
    )
    actual_changed = {
        line[3:] if line[:2] == "??" else line[2:].lstrip()
        for line in status.splitlines()
    }
    assert actual_changed == CHANGED_PATHS, (actual_changed, CHANGED_PATHS)
    owned_untracked = sorted(
        CHANGED_PATHS - {".stage1-worker-selftest.json", f"Stage1_Instances/{THEOREM}/validation-receipt.json"}
    )
    assert receipt["dirty_state"]["owned_untracked_paths"] == owned_untracked
    owned_manifest = "".join(
        f"{relative}\0{sha256(ROOT / relative)}\n" for relative in owned_untracked
    )
    assert receipt["dirty_state"]["owned_untracked_manifest_sha256"] == (
        hashlib.sha256(owned_manifest.encode()).hexdigest()
    )
    assert (LEAN_ROOT / ".lake").is_symlink()
    lake_target = os.readlink(LEAN_ROOT / ".lake")
    assert receipt["dirty_state"]["pre_existing_lake_symlink"] == {
        "path": "Formalizations/Lean/.lake",
        "target_sha256": hashlib.sha256(lake_target.encode()).hexdigest(),
        "classification": "pre-existing automation artifact; reused read-only and excluded from changed_paths",
    }
    assert receipt["dirty_state"]["tracked_patch_sha256"] == hashlib.sha256(b"").hexdigest()
    assert receipt["dirty_state"]["tracked_patch_classification"] == (
        "no tracked modifications; SHA-256 of empty byte string"
    )
    assert receipt["dirty_state"]["selftest_content_hash"] == (
        "excluded to avoid a receipt-packet finalization cycle; packet fields are bound structurally by this checker"
    )
    assert receipt["dirty_state"]["receipt_content_hash"] == (
        "self-referential and therefore excluded; receipt fields are bound structurally by this checker"
    )
    for relative in CHANGED_PATHS:
        assert_text_hygiene(ROOT / relative)

    stdout = "\n".join(SUMMARY_LINES) + "\n"
    assert receipt["execution"]["stdout_sha256"] == hashlib.sha256(stdout.encode()).hexdigest()
    print("\n".join(SUMMARY_LINES))


if __name__ == "__main__":
    main()
