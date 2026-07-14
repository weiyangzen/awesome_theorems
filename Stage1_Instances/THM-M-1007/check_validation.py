#!/usr/bin/env python3
"""Fail-closed narrow validator for S56-M-1007-VALIDATION."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import platform
import re
import shutil
import subprocess
import tempfile
import time


if not __debug__:
    raise RuntimeError("validation requires Python assertions")

ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-1007"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"

ITEM = "S56-M-1007-VALIDATION"
THEOREM = "THM-M-1007"
BASE_REVISION = "a1a7e939e58f103f5ff5d23af51437fa8658aa04"
BASE_TREE = "d881fd9641fa3e5f3ebe5082b35672981e90adcf"
EXPRESSION_SHA256 = "3b1a82b3fc0ce70be489e8a49279e3f29cfe244f7a50c28f5c4e5de26894cf38"
DENOMINATOR_SHA256 = "0a29c34a938eeb9ddb91009316aabe1be97f16a7606fbc6da3c3aea7429e87cf"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MATHLIB_REMOTE = "https://github.com/leanprover-community/mathlib4.git"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
EXPECTED_INPUTS = {
    "Statement.lean": "596d935026c6276c8a0e57a0e95915d18c568971094a02762bd1f88cdfc5daa9",
    "ObligationTree.lean": "3f1b170706aaf5ed7c76e6f916e8398d25844fcb6471d8680ca6e194b564ed5f",
    "Proof.lean": "6a8f198527b1f8f915e979991a0e89a06b1728a1bf9e191910a6c63660ecb6c5",
    "Validation.lean": "3f6780b21eedcf7c2d83571808e455a8defc1369e01372c251d18602245548f0",
    "statement.json": "3590a105cf26828b45e7e70d966ea1764abde523338028e933aa47694085f137",
    "anchor_audit.json": "dddcefe41fae077838cf4b47f861be7731a7060bc7723ee7f1d069030b343b03",
    "obligation-registry.json": "49f4ca7878fea2342d4915a465c92dde637b1a288a7f3dd35429030e7d7e0cf4",
    "typed-graphs.json": "a054c4ef2b9e7b11e4966a549f17994cd57b2ad79c29502340fc29b0567d63b2",
    "validation-specs.json": "2915955f2ece1cd02befebf4ebd669800c768c57eceddf90ca2990fe7b1a2967",
    "proof-receipt.json": "35914be02b3722cfa95d8935f92122909e378974975aba2e2e532ecce0b8f525",
    "proof-blocker-2026-07-14.json": "990453f8c79e4873bcd6b0c4c4fec85300dcc800ed92ed9ed5d9a59256eaa9a3",
    "run_validation.sh": "73406cc856fcc46500b9f6a395ca1894fd9ce6474e5901fbbed5ac68db357589",
    "validation-spec.json": "94c65c48a761caec5098b7f41fc4d90e5dcfc666a73669750a2a5af422645f8f",
}
TOOL_INPUTS = {
    "lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
SELECTED_MATHLIB_INPUTS = {
    "LICENSE": "b40930bbcf80744c86c46a12bc9da056641d722716c378f5659b9e555ef833e1",
    "Mathlib/Probability/BorelCantelli.lean":
        "e0d1d942afe23e5168486650beb83255274103f1cc4b74bc74b4d3b5a72d500e",
    ".lake/build/lib/lean/Mathlib/Probability/BorelCantelli.olean":
        "e21fee914acea119483ca07170e6fb18f050e27f51ae8f6be65d77481defc39a",
    "Mathlib/Probability/Moments/Variance.lean":
        "920c022075149257307335beccbc8a62c7360fb3d9d73571b8240093dc2d72f0",
    ".lake/build/lib/lean/Mathlib/Probability/Moments/Variance.olean":
        "f852d980c81e4090e836efd8384cac224bbe6debf8d22178dd7bb5d417bc3262",
    "Mathlib/Util/AssertNoSorry.lean":
        "aa9f7bebacafc688c894ef2171930e51ed19e0dfe722581848a2414d28900d4d",
    ".lake/build/lib/lean/Mathlib/Util/AssertNoSorry.olean":
        "c8bf37753d9bad47b9fe67e32436da8b9af516a4abbbe14e74726f01ba2fb30b",
    "Mathlib/Util/PrintSorries.lean":
        "03670b0b0007740e5390dadd49c3d10a02b7d0919092d2b3214ef8a6a8cf798f",
    ".lake/build/lib/lean/Mathlib/Util/PrintSorries.olean":
        "9bcc4076e0aee5febb2eea5cf9dc959f38526e9f974afdfdd8658bfd318d5bb7",
}
PROOF_DECLARATIONS = (
    "measurable_truncationFunction", "measurable_truncate", "norm_truncate_le",
    "memLp_truncate", "integrable_truncate", "measurableSet_largeJump",
    "iIndepSet_largeJump", "iIndepFun_truncate", "largeJump_tsum_ne_top",
    "ae_eventually_no_largeJump",
    "summable_largeJump_of_ae_eventually_no_largeJump",
    "ae_eventually_no_largeJump_of_seriesConverges",
    "summable_largeJump_of_seriesConverges", "eventuallyEq_truncate",
    "seriesConverges_iff_of_eventuallyEq",
    "ae_seriesConverges_truncate_iff_of_summable_largeJump",
    "truncate_eq_centeredTruncate_add_mean",
    "measurable_centeredTruncationFunction", "measurable_centeredTruncate",
    "iIndepFun_centeredTruncate", "integral_centeredTruncate",
    "norm_centeredTruncate_le", "memLp_centeredTruncate",
    "variance_centeredTruncate", "seriesConverges_add_iff",
    "seriesConverges_centered_iff", "eLpNorm_one_le_two",
    "eLpNorm_one_le_sqrt_integral_sq",
    "ae_tendsto_sum_of_indep_centered_L1bdd",
    "ae_seriesConverges_centered_of_variance_summable",
    "ae_seriesConverges_truncate_of_mean_variance", "threeSeries_sufficiency",
    "obligationTree_sufficiency",
)
VALIDATION_DECLARATIONS = (
    "exactSufficiencyTypeProbe", "sufficiencyFromExplicitBridges",
)
PROVISIONAL_IDS = ["M1007-T-SUFFICIENCY"]
SUPPORT_ONLY_IDS = [
    "M1007-C-TRUNC-PROPS", "M1007-C-EVENT-INDEP",
    "M1007-B-LARGE-JUMP-NEC", "M1007-B-LARGE-JUMP-SUFF",
    "M1007-T-EVENTUAL", "M1007-N-CENTER",
]
FAIL_CLOSED_EVALUATION_IDS = [
    "M1007-ROOT", "M1007-S-INTERFACE", "M1007-T-ASSEMBLE",
    "M1007-X-PROVENANCE", "M1007-X-TCB",
]
MATHEMATICAL_CUT = ["M1007-L-BOUNDED-NEC"]
FROZEN_CUT = [
    "M1007-C-TRUNC-PROPS", "M1007-C-EVENT-INDEP",
    "M1007-B-LARGE-JUMP-NEC", "M1007-B-LARGE-JUMP-SUFF",
    "M1007-T-EVENTUAL", "M1007-L-BOUNDED-NEC", "M1007-L-BOUNDED-SUFF",
]
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/Validation.lean",
    f"Stage1_Instances/{THEOREM}/check_validation.py",
    f"Stage1_Instances/{THEOREM}/run_validation.sh",
    f"Stage1_Instances/{THEOREM}/validation-phase.md",
    f"Stage1_Instances/{THEOREM}/validation-receipt.json",
    f"Stage1_Instances/{THEOREM}/validation-spec.json",
}
SUMMARY_LINES = [
    "PASS THM-M-1007 narrow validation",
    "PASS network-isolated trust-zero replay: frozen statement, conditional composition, 33 proof declarations, exact sufficiency type probe, and differential bridge elaborated",
    "PASS trust observation: 36 distinct declarations list exactly propext, Classical.choice, and Quot.sound; transitive sorry probes and local hygiene passed",
    "PASS selected provenance: frozen hashes, proof linkage, clean pinned mathlib revision/tree/remote/license, selected source/olean hashes, and tool identities agree",
    "OPEN exact root: bounded-series necessity M1007-L-BOUNDED-NEC is absent; root remains H1/M3/R3 and theorem_complete=false",
    "FAIL CLOSED authority/trust/hermetic gates: proof master acceptance, accepted foundation profile, complete transitive TCB/SBOM, cold offline replay, H0, and R0 remain open",
    "FAIL CLOSED independent gate: the differential probe shares this worker, checkout, toolchain, kernel, and warm cache; no distinct signed verifier exists",
]
VALIDATION_STARTED = time.monotonic()
TIMEOUT_SECONDS = 900.0


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


def run(
    argv: list[str], *, cwd: Path = ROOT, env: dict[str, str] | None = None,
    timeout: int = 900,
) -> str:
    remaining = TIMEOUT_SECONDS - (time.monotonic() - VALIDATION_STARTED)
    if remaining <= 0:
        raise TimeoutError("validation recipe exceeded its 900-second wall-clock bound")
    result = subprocess.run(
        argv, cwd=cwd, env=env, text=True, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, timeout=min(timeout, remaining), check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(f"command failed ({result.returncode}): {argv!r}\n{result.stdout}")
    return result.stdout


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["git", *args], cwd=cwd).rstrip()


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


def axiom_reports(output: str) -> dict[str, set[str]]:
    reports: dict[str, set[str]] = {}
    for name, body in re.findall(
        r"'([^']+)' depends on axioms: \[(.*?)]", output, flags=re.DOTALL,
    ):
        assert name not in reports, name
        reports[name] = {part.strip() for part in body.split(",") if part.strip()}
    for name in re.findall(r"'([^']+)' does not depend on any axioms", output):
        assert name not in reports, name
        reports[name] = set()
    return reports


def assert_text_hygiene(path: Path) -> None:
    data = path.read_bytes()
    assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())


def main() -> None:
    spec = load(HERE / "validation-spec.json")
    receipt = load(HERE / "validation-receipt.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")
    targets = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    statement = load(HERE / "statement.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    frozen_specs = load(HERE / "validation-specs.json")
    proof_receipt = load(HERE / "proof-receipt.json")
    proof_blocker = load(HERE / "proof-blocker-2026-07-14.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 287 and target["baseline"] == "L0"
    assert target["lifecycle_mode"] == "planned"
    assert target["rework_required"] is True and target["theorem_complete"] is False
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item == {
        "id": ITEM, "theorem_id": THEOREM, "execution_rank": 287,
        "phase": "validation", "layer": 5, "state": "[ ]",
        "depends_on": ["S56-M-1007-PROOF"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Run hermetic kernel, trust, provenance, and independent validation gates.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0, "children": [],
    }
    predecessor = next(
        row for row in execution["items"] if row["id"] == "S56-M-1007-PROOF"
    )
    assert predecessor["state"] == "[_]" and predecessor["attempts"] == 1

    for name, expected in EXPECTED_INPUTS.items():
        assert sha256(HERE / name) == expected, f"stale validation input: {name}"
    for name, expected in TOOL_INPUTS.items():
        assert sha256(LEAN_ROOT / name) == expected, f"changed tool input: {name}"
    formal = statement["canonical_formal_target"]
    assert formal["declaration_or_expression"] == (
        "Stage1Instances.THM_M_1007.KolmogorovThreeSeriesTarget"
    )
    assert formal["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert formal["statement_file_sha256"] == EXPECTED_INPUTS["Statement.lean"]
    assert registry["root_obligation_id"] == "M1007-ROOT"
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    closure = graphs["closure_boundary"]
    assert closure["closed_obligations"] == [] and closure["root_closed"] is False
    assert closure["root_machine_debt"] == "M3"
    assert closure["remaining_root_cut_set"] == FROZEN_CUT
    assert closure["audit_complete"] is closure["theorem_complete"] is False
    root_node = next(row for row in graphs["nodes"] if row["obligation_id"] == "M1007-ROOT")
    assert (root_node["human_debt"], root_node["machine_debt"], root_node["readability_debt"]) == (
        "H1", "M3", "R3",
    )
    assert frozen_specs["item_id"] == "S56-M-1007-OBLIGATION_TREE"
    assert all(row["argv"][-1].endswith("ObligationTree.lean") for row in frozen_specs["recipes"])

    assert proof_receipt["item_id"] == "S56-M-1007-PROOF"
    assert proof_receipt["support_state"] == "provisional_worker_selftest"
    assert proof_receipt["accepted"] is False
    assert proof_receipt["canonical_target_expression_sha256"] == EXPRESSION_SHA256
    assert proof_receipt["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert proof_receipt["proof_body"]["source_sha256"] == EXPECTED_INPUTS["Proof.lean"]
    assert proof_receipt["exact_declarations"] == [
        f"Stage1Instances.THM_M_1007.Proof.{name}" for name in PROOF_DECLARATIONS
    ]
    assert proof_receipt["provisionally_closed_proof_obligation_ids"] == PROVISIONAL_IDS
    assert proof_receipt["accepted_closed_obligation_ids"] == []
    assert proof_receipt["result"]["root_closed"] is False
    assert proof_receipt["result"]["theorem_complete"] is False
    assert proof_receipt["provisional_mathematical_remaining_cut"] == MATHEMATICAL_CUT
    assert proof_receipt["authoritative_graph_open_cut_set_unchanged"] == FROZEN_CUT
    assert proof_blocker["root_closed"] is False
    assert proof_blocker["provisional_mathematical_remaining_cut"] == MATHEMATICAL_CUT

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by|run_tac)\b|"
        r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
        r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
        r"(?:axiom|constant|opaque|unsafe|extern)\b",
        flags=re.MULTILINE,
    )
    for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
        source = source_without_comments((HERE / name).read_text(encoding="utf-8"))
        source = re.sub(r"^#print sorries .*?$", "", source, flags=re.MULTILINE)
        assert prohibited.search(source) is None, f"prohibited source construct in {name}"
    validation_source = source_without_comments((HERE / "Validation.lean").read_text())
    proof_source = source_without_comments((HERE / "Proof.lean").read_text())
    assert "import Proof" in validation_source
    assert "import Statement" in validation_source
    assert "theorem exactSufficiencyTypeProbe" in validation_source
    assert "theorem sufficiencyFromExplicitBridges" in validation_source
    assert "KolmogorovThreeSeriesTarget := by" not in validation_source
    assert "Necessity" not in validation_source
    assert "KolmogorovThreeSeriesTarget := by" not in proof_source
    assert "theorem obligationTree_necessity" not in proof_source
    assert "ObligationTree.Necessity" not in proof_source

    manifest = load(LEAN_ROOT / "lake-manifest.json")
    mathlib_entry = next(row for row in manifest["packages"] if row["name"] == "mathlib")
    assert mathlib_entry["rev"] == mathlib_entry["inputRev"] == MATHLIB_REVISION
    assert MATHLIB.resolve().is_dir(), "canonical pinned mathlib artifact missing"
    assert git("rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert git("remote", "get-url", "origin", cwd=MATHLIB) == MATHLIB_REMOTE
    assert git("status", "--porcelain=v1", cwd=MATHLIB) == ""
    for name, expected in SELECTED_MATHLIB_INPUTS.items():
        assert sha256(MATHLIB / name) == expected, name

    fixed_env = os.environ.copy()
    fixed_env.update({
        "ELAN_TOOLCHAIN": "leanprover/lean4:v4.29.0", "LANG": "C.UTF-8",
        "LC_ALL": "C.UTF-8", "TZ": "UTC", "LEAN_NUM_THREADS": "1",
    })
    lean = Path(run(["lake", "env", "which", "lean"], cwd=LEAN_ROOT, env=fixed_env).strip())
    lake = Path(run(["lake", "env", "which", "lake"], cwd=LEAN_ROOT, env=fixed_env).strip())
    lean_path = run(["lake", "env", "printenv", "LEAN_PATH"], cwd=LEAN_ROOT, env=fixed_env).strip()
    bwrap = Path(shutil.which("bwrap") or "")
    assert lean.is_file() and lake.is_file() and bwrap.is_file()
    assert sha256(lean) == "3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf"
    assert sha256(lake) == "a608ff084d7e2af228b92a29d7c2fd083ba0580e46889175ec74a81678c98359"
    assert sha256(bwrap.resolve()) == "0abea81db798ebf6b4742ac0664802d97521547a353c2a0dbdc21d76cbbfd2c0"
    assert LEAN_COMMIT in run([str(lean), "--version"], env=fixed_env)

    tmp = Path(tempfile.mkdtemp(prefix="stage1-m1007-validation-", dir="/tmp"))
    try:
        for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
            shutil.copy2(HERE / name, tmp / name)
        (tmp / "home").mkdir()
        assert os.environ.get("STAGE1_OUTER_SANDBOX") == "1"

        def isolated_lean(args: list[str], *, local_modules: bool = False) -> str:
            module_path = f"{tmp}:{lean_path}" if local_modules else lean_path
            lean_env = fixed_env.copy()
            lean_env.update({"HOME": str(tmp / "home"), "LEAN_PATH": module_path})
            return run(
                [str(lean), "--trust=0", "-t0", *args], cwd=tmp, env=lean_env,
            )

        statement_output = isolated_lean(["-o", "Statement.olean", "Statement.lean"])
        obligation_output = isolated_lean(
            ["-o", "ObligationTree.olean", "ObligationTree.lean"], local_modules=True,
        )
        proof_output = isolated_lean(
            ["-o", "Proof.olean", "Proof.lean"], local_modules=True,
        )
        validation_output = isolated_lean(["Validation.lean"], local_modules=True)
    finally:
        shutil.rmtree(tmp)

    obligation_reports = axiom_reports(obligation_output)
    assert obligation_reports == {
        "Stage1Instances.THM_M_1007.ObligationTree.root_of_directions": EXPECTED_AXIOMS
    }
    proof_reports = axiom_reports(proof_output)
    assert proof_reports == {
        f"Stage1Instances.THM_M_1007.Proof.{name}": EXPECTED_AXIOMS
        for name in PROOF_DECLARATIONS
    }
    validation_reports = axiom_reports(validation_output)
    assert validation_reports == {
        "Stage1Instances.THM_M_1007.Proof.obligationTree_sufficiency": EXPECTED_AXIOMS,
        "Stage1Instances.THM_M_1007.Validation.exactSufficiencyTypeProbe": EXPECTED_AXIOMS,
        "Stage1Instances.THM_M_1007.Validation.sufficiencyFromExplicitBridges": EXPECTED_AXIOMS,
    }
    assert validation_output.count("Declarations are sorry-free!") == 3
    combined_output = statement_output + obligation_output + proof_output + validation_output
    assert "sorryAx" not in combined_output and "declaration uses 'sorry'" not in combined_output
    assert "error:" not in combined_output

    assert spec["schema_version"] == "stage1-validation-recipe/1.0"
    assert spec["item_id"] == ITEM and spec["theorem_id"] == THEOREM
    assert spec["argv"] == ["bash", f"Stage1_Instances/{THEOREM}/run_validation.sh"]
    assert spec["cwd"] == "." and spec["timeout_seconds"] == 900
    assert spec["network_policy"] == "denied"
    assert spec["expected_exit"] == 0
    assert "entire Python recipe" in spec["network_enforcement"]
    assert "bubblewrap --unshare-net" in spec["network_enforcement"]
    assert spec["provisional_kernel_evidence_obligation_ids"] == PROVISIONAL_IDS
    assert spec["support_only_obligation_ids"] == SUPPORT_ONLY_IDS
    assert spec["fail_closed_evaluation_obligation_ids"] == FAIL_CLOSED_EVALUATION_IDS
    assert set(spec["covered_obligation_ids"]) == (
        set(PROVISIONAL_IDS) | set(SUPPORT_ONLY_IDS) | set(FAIL_CLOSED_EVALUATION_IDS)
    )
    assert set(spec["covered_declarations"]) == (
        {
            "Stage1Instances.THM_M_1007.KolmogorovThreeSeriesTarget",
            "Stage1Instances.THM_M_1007.ObligationTree.root_of_directions",
        }
        | set(proof_receipt["exact_declarations"])
        | {f"Stage1Instances.THM_M_1007.Validation.{name}" for name in VALIDATION_DECLARATIONS}
    )

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["receipt_id"] == "S56-M-1007-VALIDATION-local-20260715T064753+0800"
    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["phase"] == "validation" and receipt["intent"] == "validate"
    assert receipt["depends_on"] == ["S56-M-1007-PROOF"]
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["release_grade"] is receipt["content_addressed_release_evidence"] is False
    assert receipt["started_at"] == "2026-07-15T06:45:18+08:00"
    assert receipt["finished_at"] == receipt["validated_at"] == (
        "2026-07-15T06:47:53+08:00"
    )
    assert receipt["duration_seconds"] == 155.458
    for name, expected in EXPECTED_INPUTS.items():
        assert receipt["inputs"][name] == expected, name
    assert receipt["inputs"]["check_validation.py"] == sha256(Path(__file__).resolve())
    assert receipt["inputs"]["validation-phase.md"] == sha256(HERE / "validation-phase.md")
    assert receipt["inputs"]["worker_packet_binding"] == (
        "validated structurally below; omitted from receipt hash inputs to avoid a receipt-packet hash cycle"
    )
    recipe_keys = (
        "recipe_id", "cwd", "argv", "env_allowlist", "timeout_seconds",
        "network_policy", "network_enforcement", "expected_exit", "expected_outputs",
        "covered_obligation_ids", "covered_declarations",
        "provisional_kernel_evidence_obligation_ids",
        "fail_closed_evaluation_obligation_ids", "support_only_obligation_ids",
        "scope_boundary",
    )
    assert receipt["recipe"] == {key: spec[key] for key in recipe_keys}
    assert receipt["verdict"] == "blocked"
    assert receipt["lifecycle_before"] == receipt["lifecycle_after"] == "planned"
    environment = receipt["environment"]
    assert environment["platform"] == f"{platform.system()} {platform.release()} {platform.machine()}"
    assert environment["lean_executable_sha256"] == sha256(lean)
    assert environment["lake_executable_sha256"] == sha256(lake)
    assert environment["bubblewrap_executable_sha256"] == sha256(bwrap.resolve())
    python = Path(os.path.realpath(shutil.which("python3") or ""))
    git_executable = Path(os.path.realpath(shutil.which("git") or ""))
    bash = Path(os.path.realpath(shutil.which("bash") or ""))
    assert environment["python_executable_sha256"] == sha256(python)
    assert environment["git_executable_sha256"] == sha256(git_executable)
    assert environment["bash_executable_sha256"] == sha256(bash)
    assert environment["lean_toolchain_sha256"] == TOOL_INPUTS["lean-toolchain"]
    assert environment["lake_manifest_sha256"] == TOOL_INPUTS["lake-manifest.json"]
    assert environment["mathlib_revision"] == MATHLIB_REVISION
    assert environment["mathlib_tree"] == MATHLIB_TREE
    assert environment["mathlib_remote"] == MATHLIB_REMOTE
    assert environment["mathlib_license_sha256"] == SELECTED_MATHLIB_INPUTS["LICENSE"]
    assert environment["mathlib_worktree"] == (
        "tracked source worktree clean; ignored warm build cache not globally audited"
    )
    provenance = receipt["selected_provenance"]
    selected_receipt_keys = {
        "Mathlib/Probability/BorelCantelli.lean": "BorelCantelli.lean_sha256",
        ".lake/build/lib/lean/Mathlib/Probability/BorelCantelli.olean":
            "BorelCantelli.olean_sha256",
        "Mathlib/Probability/Moments/Variance.lean": "Variance.lean_sha256",
        ".lake/build/lib/lean/Mathlib/Probability/Moments/Variance.olean":
            "Variance.olean_sha256",
        "Mathlib/Util/AssertNoSorry.lean": "AssertNoSorry.lean_sha256",
        ".lake/build/lib/lean/Mathlib/Util/AssertNoSorry.olean":
            "AssertNoSorry.olean_sha256",
        "Mathlib/Util/PrintSorries.lean": "PrintSorries.lean_sha256",
        ".lake/build/lib/lean/Mathlib/Util/PrintSorries.olean":
            "PrintSorries.olean_sha256",
    }
    for source_name, receipt_key in selected_receipt_keys.items():
        assert provenance[receipt_key] == SELECTED_MATHLIB_INPUTS[source_name]
    assert receipt["trust"]["accepted_foundation_profile"] is False
    assert receipt["trust"]["complete_transitive_trust_closure"] is False
    assert receipt["provenance"]["proof_dependency_master_accepted"] is False
    assert receipt["provenance"]["complete_terminal_body_import_artifact_source_boundary_and_tcb_closure"] is False
    assert receipt["hermeticity"]["decision"] == "fail_closed_nonrelease_warm_cache_replay"
    assert receipt["independent_validation"]["decision"] == "fail_closed"
    result = receipt["result"]
    assert result["network_isolated_trust_zero_replay"] == "pass"
    assert result["axiom_report_count"] == 36
    assert result["observed_axioms"] == sorted(EXPECTED_AXIOMS)
    assert result["transitive_sorry_check"] == "pass"
    assert result["provisionally_validated_obligation_ids"] == PROVISIONAL_IDS
    assert result["accepted_closed_obligation_ids"] == []
    assert result["root_kernel_closed"] is False and result["root_machine_debt"] == "M3"
    assert result["mathematical_remaining_cut"] == MATHEMATICAL_CUT
    assert result["authoritative_frozen_cut_set"] == FROZEN_CUT
    assert result["audit_complete"] is result["theorem_complete"] is False
    assert result["foundation_complete_tcb_gate"] == "fail_closed"
    assert result["hermetic_cold_offline_replay"] == "fail_closed"
    assert result["independent_distinct_runner"] == "fail_closed"
    assert receipt["first_failed_gate"] == "dependency.S56-M-1007-PROOF.master_acceptance"
    assert receipt["first_failed_mathematical_gate"] == "proof.root_kernel_closure.M1007-L-BOUNDED-NEC"
    assert receipt["first_failed_release_gate"] == "S56-10.6-HERMETIC-COLD-BUILD"
    assert receipt["remaining_root_cut_set"] == MATHEMATICAL_CUT
    assert set(receipt["changed_paths"]) == CHANGED_PATHS
    summary_sha256 = hashlib.sha256(("\n".join(SUMMARY_LINES) + "\n").encode()).hexdigest()
    assert receipt["output_evidence"] == {
        "captured_stdout_sha256": summary_sha256,
        "stdout_semantic_sha256": summary_sha256,
        "stderr_policy": "merged into captured stdout",
        "expected_line_count": len(SUMMARY_LINES),
        "exit_code": 0,
    }

    assert packet == {
        "item_id": ITEM,
        "changed_paths": receipt["changed_paths"],
        "commands": receipt["commands"],
        "output_summary": "\n".join(SUMMARY_LINES),
        "base_revision": BASE_REVISION,
        "known_failures": receipt["known_failures"],
        "state": "[_]",
    }
    status = run(["git", "status", "--short", "--untracked-files=all"])
    actual_changes = {
        line[3:] for line in status.splitlines()
        if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual_changes == CHANGED_PATHS, (actual_changes, CHANGED_PATHS)
    manifest_entries = [
        {
            "path": "Formalizations/Lean/.lake",
            "kind": "symlink",
            "target_sha256": hashlib.sha256(
                os.readlink(LEAN_ROOT / ".lake").encode()
            ).hexdigest(),
        }
    ]
    for relative in sorted(CHANGED_PATHS - {
        ".stage1-worker-selftest.json",
        f"Stage1_Instances/{THEOREM}/validation-receipt.json",
    }):
        path = ROOT / relative
        manifest_entries.append({
            "path": relative,
            "kind": "file",
            "sha256": sha256(path),
            "size": path.stat().st_size,
        })
    manifest_sha256 = hashlib.sha256(json.dumps(
        manifest_entries, sort_keys=True, separators=(",", ":"),
    ).encode()).hexdigest()
    tracked_patch = run([
        "git", "diff", "--binary", "--", str(HERE),
        str(ROOT / ".stage1-worker-selftest.json"),
    ])
    repository_state = receipt["repository_state"]
    assert repository_state["tracked_patch_sha256"] == hashlib.sha256(
        tracked_patch.encode()
    ).hexdigest()
    assert repository_state["git_status_porcelain_sha256"] == hashlib.sha256(
        status.encode()
    ).hexdigest()
    assert repository_state["untracked_validation_input_manifest"] == manifest_entries
    assert repository_state["untracked_validation_input_manifest_sha256"] == manifest_sha256
    assert repository_state["untracked_outputs"] == [
        ".stage1-worker-selftest.json",
        f"Stage1_Instances/{THEOREM}/validation-receipt.json",
    ]
    for relative in CHANGED_PATHS:
        assert_text_hygiene(ROOT / relative)
    print("\n".join(SUMMARY_LINES))


if __name__ == "__main__":
    main()
