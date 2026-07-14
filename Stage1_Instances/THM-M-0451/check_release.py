#!/usr/bin/env python3
"""Fail-closed release reconciliation for S56-M-0451-RELEASE."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0451"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
ITEM = "S56-M-0451-RELEASE"
THEOREM = "THM-M-0451"
BASE_REVISION = "bbe7a5bd1c72a12f3f43b79b6a4cac3f62d2085a"
BASE_TREE = "aa558ed6f23779c7d2d9a8427775f709d8b7e31b"
EXPRESSION_SHA256 = (
    "76392071dc0670ad9c58f8eabc2195eecd990545084cfce9d6ecb13696803ed8"
)
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
INVENTORY_IDS = [
    "M0451-ROOT", "M0451-ASSEMBLE", "M0451-HEIGHT", "M0451-LIMIT",
    "M0451-APPROX", "M0451-BOUNDED", "M0451-QUADRATIC",
    "M0451-PARALLELOGRAM", "M0451-NONNEGATIVE", "M0451-TORSION-KERNEL",
    "M0451-TORSION-ZERO", "M0451-ZERO-TORSION", "M0451-XHEIGHT",
    "M0451-FOUNDATION", "M0451-SOURCE", "M0451-PROVENANCE", "M0451-TRUST",
]
ACCEPTED_CUT = [
    "M0451-APPROX", "M0451-LIMIT", "M0451-BOUNDED", "M0451-QUADRATIC",
    "M0451-PARALLELOGRAM", "M0451-NONNEGATIVE", "M0451-TORSION-ZERO",
    "M0451-ZERO-TORSION", "M0451-SOURCE", "M0451-PROVENANCE", "M0451-TRUST",
]
PROPOSED_CUT = [
    "M0451-APPROX", "M0451-ZERO-TORSION", "M0451-SOURCE",
    "M0451-PROVENANCE", "M0451-TRUST",
]
PROOF_DECLARATIONS = {
    "Stage1Instances.THM_M_0451.ObligationTree.engine_compose",
    "Stage1Instances.THM_M_0451.Proof.tateSequence_tendsto",
    "Stage1Instances.THM_M_0451.Proof.tateLimit_sub_le",
    "Stage1Instances.THM_M_0451.Proof.tateLimit_map",
    "Stage1Instances.THM_M_0451.Proof.limit_formula_of_doubling_bound",
    "Stage1Instances.THM_M_0451.Proof.bounded_difference_of_doubling_bound",
    "Stage1Instances.THM_M_0451.Proof.constructedCanonicalHeight_double",
    "Stage1Instances.THM_M_0451.Proof.constructedCanonicalHeight_nonnegative",
    "Stage1Instances.THM_M_0451.Proof.constructedCanonicalHeight_parallelogram_of_bounds",
    "Stage1Instances.THM_M_0451.Proof.constructedCanonicalHeight_quadratic_of_bounds",
    "Stage1Instances.THM_M_0451.Proof.constructedCanonicalHeight_torsion_zero",
    "Stage1Instances.THM_M_0451.Proof.torsion_to_zero_of_quadratic",
}
VALIDATION_DECLARATION = (
    "Stage1Instances.THM_M_0451.Validation.exactTarget_conditional_probe"
)
RECONCILED_INPUTS = {
    "Statement.lean": "f288b8eb0959aa199c316bc0727f84a85df9d3c3612c257da49b94dd8a6a6c52",
    "AnchorAudit.lean": "25d7c3e12515b92653fa8696aabdb1016a4822a5dad12a3643fc841b18331282",
    "ObligationTree.lean": "96a2a4b4955baad71cd23ca45e3a60070d84dc6793f4751036d5fabc70831f38",
    "Proof.lean": "7cab7cf2608dd7dd236c9d97834695a04fccdc11f54c1dfc2dc5d795e77bf11b",
    "ProofAudit.lean": "08049b966a40ed5121e581e5a2d8f25c51bec265802cd3d08f123d5a29e0032c",
    "Validation.lean": "edcbc59586453ec8f96c7692ea02162e621a86ab475d043a83215d171d1c1f62",
    "statement.json": "789930d7eddc88137f5491140f4c265790bb0c12d554aa71cf11c41d38d357e4",
    "anchor-audit.json": "92f4a43ef98277af3165a809f7159428d66455447ada11af48b9ae8dacc8c1c2",
    "obligation-registry.json": "b31f76ecf12e6936dcbfe0e536df7b0a353f0adf83af31d07a96341b130ae100",
    "typed-graphs.json": "b957531c419f6648336d1abbd51c161f81b5cdbd90f3a092335c2dfdabbf57ce",
    "proof-receipt.json": "5ed343b673c102441d5d889823508bec6c53faf17c056e2485af1728bcfad5a6",
    "validation-spec.json": "c271f94b7619d6622181d154a1c845db04f9131051443ac74a6a49b169aa2885",
    "validation-receipt.json": "d9d96d1bcea7afd6ed43c5d3a6604123f08ab53544e5cecbcc79c219abd36162",
    "check_validation.py": "58827795b85571b3d319d7f9a44a897d84b6f1aa8b454db93e980e87d83ba2b2",
    "task-dag.json": "7e4a1fa021fc5db54ebe213f60d5f5b77e87f91aed73239af8f7210d647730c1",
    "source_statement_crosswalk.md": "250a1999ee9eef2db43f21073f03cd05b111fe1d22136d49cc6e0a7a06dda124",
}
AUTHORITY_INPUTS = {
    "Docs/Stage1_Targets_rev-5.6.json": (
        "02eec284de534dd78e1cf75f82a477ff477567dd682b7445cb7587abd137ab2c"
    ),
    "Docs/Stage1_Execution_DAG_rev-5.6.json": (
        "358d0c707eae8d12a55cb5a6fa9679292ae34bbb3e258433ec4d3980f5d9f42a"
    ),
    "Docs/Stage1_Blueprint_rev-5.6.md": (
        "cb508dfc71b4c2c55b5652b8338c75c3b992ca298f0749dd2e0f3c5e92396384"
    ),
    "skills/execute-stage1-rev56/SKILL.md": (
        "26d47a66c6535feabb8bbf1051fd55d76a53fe761f4b3d953f86b97ec86152b8"
    ),
}
TOOL_INPUTS = {
    "Formalizations/Lean/lean-toolchain": (
        "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2"
    ),
    "Formalizations/Lean/lake-manifest.json": (
        "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81"
    ),
}
EXPECTED_TOOLS = {
    "lean": "3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf",
    "lake": "a608ff084d7e2af228b92a29d7c2fd083ba0580e46889175ec74a81678c98359",
    "bwrap": "0abea81db798ebf6b4742ac0664802d97521547a353c2a0dbdc21d76cbbfd2c0",
    "python": "b8d8288faefdd300201f43fcf00f6f539a27218eeed3a3dff5ab10b9c4c99700",
    "git": "8a48eefa306b9a2a9c3e576784a74ad7485779279e5a46ec43361a1864760e45",
}
EXPECTED_LEAN_PATH_SHA256 = (
    "fb2ba7bbb2215a5213ba4e6d91fd79c8e9c0d5a70b2124b212feedc9312d1427"
)
EXPECTED_OLEANS = {
    "Mathlib/AlgebraicGeometry/EllipticCurve/Affine/Point.olean": (
        "00233b31e01d00a2b3affe5c746c174f6279dee266d35fbbd03634385f48c9e9"
    ),
    "Mathlib/NumberTheory/Height/Basic.olean": (
        "35fdbb63f76ec0db1626fd5dfdded0e7c109daa0254b41e67dd95680e39aa2b1"
    ),
    "Mathlib/NumberTheory/Height/NumberField.olean": (
        "2840173f33b4d956643c3fe1b34e014cbb518766da40cc998c180c40844b08cb"
    ),
    "Mathlib/Analysis/SpecificLimits/Basic.olean": (
        "aa4bf5024b7b011d370e7e6d895e381de2404ec501a14273abc0bf1eb6dcf68b"
    ),
}
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/check_release.py",
    f"Stage1_Instances/{THEOREM}/release-decision.json",
    f"Stage1_Instances/{THEOREM}/release-phase.md",
    f"Stage1_Instances/{THEOREM}/release-receipt.json",
    f"Stage1_Instances/{THEOREM}/release-spec.json",
}
SUMMARY_LINES = (
    "PASS release inputs: target, DAG, receipts, frozen registry, graphs, and hashes agree",
    "PASS current narrow replay: trust-zero network-isolated statement, conditional proof, sorry, and axiom probes",
    "PASS fail-closed state: lifecycle planned; accepted root H1/M3/R3; accepted receipts 0",
    "BLOCKED S56-10.2-DEPENDENCY-ACCEPTANCE: validation is provisional and not master accepted",
    "BLOCKED exact root and release: M0451-APPROX and M0451-ZERO-TORSION are open; replay is warm and same-worker",
    "verdict=blocked audit_complete=false theorem_complete=false",
)


def load(path: Path) -> dict:
    def reject_duplicates(pairs: list[tuple[str, object]]) -> dict:
        result: dict[str, object] = {}
        for key, value in pairs:
            assert key not in result, f"duplicate JSON key in {path}: {key}"
            result[key] = value
        return result

    value = json.loads(
        path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicates
    )
    assert isinstance(value, dict), path
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(
    argv: list[str], *, cwd: Path = ROOT, env: dict[str, str] | None = None,
    timeout: int = 360, check: bool = True,
) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        argv, cwd=cwd, env=env, text=True, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, timeout=timeout, check=False,
    )
    if check and result.returncode != 0:
        raise RuntimeError(
            f"command failed ({result.returncode}): {argv!r}\n{result.stdout}"
        )
    return result


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["git", *args], cwd=cwd).stdout.strip()


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
    for declaration, body in re.findall(
        r"'([^']+)' depends on axioms:\s*\[([^]]*)\]", output, re.DOTALL
    ):
        reports[declaration] = {
            part.strip() for part in body.split(",") if part.strip()
        }
    return reports


def assert_text_hygiene(path: Path) -> None:
    data = path.read_bytes()
    assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())


def sandboxed_lean(
    lean: Path, lean_path: str, tmp: Path, source: str,
) -> subprocess.CompletedProcess[str]:
    output = source.removesuffix(".lean") + ".olean"
    return run([
        str(shutil.which("bwrap")), "--unshare-net", "--die-with-parent",
        "--ro-bind", "/", "/", "--bind", str(tmp), str(tmp), "--dev", "/dev",
        "--proc", "/proc", "--dir", "/run", "--setenv", "HOME", "/tmp/home",
        "--setenv", "TMPDIR", "/tmp", "--setenv", "LANG", "C.UTF-8",
        "--setenv", "LC_ALL", "C.UTF-8", "--setenv", "TZ", "UTC",
        "--setenv", "LEAN_NUM_THREADS", "1", "--setenv", "LEAN_PATH",
        f"{tmp}:{lean_path}", "--chdir", str(tmp), "--", str(lean),
        "--trust=0", "-t0", "-o", output, source,
    ])


def current_narrow_replay() -> None:
    manifest = load(LEAN_ROOT / "lake-manifest.json")
    mathlib_record = next(row for row in manifest["packages"] if row["name"] == "mathlib")
    assert mathlib_record["rev"] == MATHLIB_REVISION
    mathlib = (LEAN_ROOT / ".lake/packages/mathlib").resolve()
    assert mathlib.is_dir(), "pinned mathlib artifact is missing"
    assert git("rev-parse", "HEAD", cwd=mathlib) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == MATHLIB_TREE
    assert git("status", "--porcelain=v1", cwd=mathlib) == ""
    for relative, expected in EXPECTED_OLEANS.items():
        assert sha256(mathlib / ".lake/build/lib/lean" / relative) == expected

    lean = Path(run(["lake", "env", "which", "lean"], cwd=LEAN_ROOT).stdout.strip())
    lake = Path(run(["lake", "env", "which", "lake"], cwd=LEAN_ROOT).stdout.strip())
    lean_path = run(["lake", "env", "printenv", "LEAN_PATH"], cwd=LEAN_ROOT).stdout.strip()
    bwrap = Path(os.path.realpath(shutil.which("bwrap") or ""))
    python = Path(os.path.realpath(shutil.which("python3") or ""))
    git_executable = Path(os.path.realpath(shutil.which("git") or ""))
    for name, path in {
        "lean": lean, "lake": lake, "bwrap": bwrap,
        "python": python, "git": git_executable,
    }.items():
        assert path.is_file() and sha256(path) == EXPECTED_TOOLS[name]
    assert hashlib.sha256((lean_path + "\n").encode()).hexdigest() == (
        EXPECTED_LEAN_PATH_SHA256
    )

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by|run_tac|oracle)\b|"
        r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
        r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
        r"(?:axiom|constant|opaque|unsafe|extern)\b",
        re.MULTILINE,
    )
    names = (
        "Statement.lean", "AnchorAudit.lean", "ObligationTree.lean", "Proof.lean",
        "ProofAudit.lean", "Validation.lean",
    )
    for name in names:
        source = source_without_comments((HERE / name).read_text(encoding="utf-8"))
        assert prohibited.search(source) is None, f"prohibited proof device in {name}"

    with tempfile.TemporaryDirectory(prefix="m0451-release-") as directory:
        tmp = Path(directory)
        for name in names:
            shutil.copy2(HERE / name, tmp / name)
        outputs = {
            name: sandboxed_lean(lean, lean_path, tmp, name).stdout for name in names
        }
    proof_reports = axiom_reports(outputs["ProofAudit.lean"])
    assert set(proof_reports) == PROOF_DECLARATIONS
    assert all(axioms == EXPECTED_AXIOMS for axioms in proof_reports.values())
    validation_reports = axiom_reports(outputs["Validation.lean"])
    assert validation_reports == {VALIDATION_DECLARATION: EXPECTED_AXIOMS}
    combined = "\n".join(outputs.values())
    assert "contains sorry" not in combined and "sorryAx" not in combined
    assert outputs["ProofAudit.lean"].count("Declarations are sorry-free!") == 12
    assert outputs["Validation.lean"].count("Declarations are sorry-free!") == 1
    assert "NeronTateCanonicalHeightTarget" in outputs["Statement.lean"]


def main() -> None:
    if not __debug__:
        raise RuntimeError("release validation requires Python assertions")

    decision = load(HERE / "release-decision.json")
    spec = load(HERE / "release-spec.json")
    receipt_path = HERE / "release-receipt.json"
    receipt = load(receipt_path) if receipt_path.exists() else None
    validation = load(HERE / "validation-receipt.json")
    proof = load(HERE / "proof-receipt.json")
    statement = load(HERE / "statement.json")
    anchor = load(HERE / "anchor-audit.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    local_tasks = load(HERE / "task-dag.json")
    targets = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    assert decision["item_id"] == spec["item_id"] == ITEM
    assert decision["theorem_id"] == spec["theorem_id"] == THEOREM
    assert decision["base_revision"] == BASE_REVISION
    assert decision["base_tree"] == BASE_TREE
    assert spec["argv"] == ["python3", "-I", "-B", str(HERE.relative_to(ROOT) / "check_release.py")]
    assert spec["network_policy"] == (
        "nested_lean_denied_release_orchestration_not_isolated"
    ) and spec["expected_exit"] == 0
    assert spec["covered_obligation_ids"] == INVENTORY_IDS
    expected_summary = "\n".join(SUMMARY_LINES) + "\n"
    assert spec["expected_outputs"] == [{
        "path_or_stream": "stdout",
        "semantic_hash_policy": "exact six-line PASS/BLOCKED negative release summary",
        "semantic_sha256": hashlib.sha256(expected_summary.encode()).hexdigest(),
        "bytes": len(expected_summary.encode()),
    }]

    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 93 and target["baseline"] == "L0"
    assert target["rework_required"] is True and target["legacy_artifacts_accepted"] is False
    assert target["lifecycle_mode"] == "planned" and target["theorem_complete"] is False
    release_item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert release_item == {
        "id": ITEM, "theorem_id": THEOREM, "execution_rank": 93,
        "phase": "release", "layer": 6, "state": "[ ]",
        "depends_on": ["S56-M-0451-VALIDATION"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Reconcile evidence and decide the exact theorem-completion verdict.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0, "children": [],
    }
    validation_item = next(
        row for row in execution["items"] if row["id"] == "S56-M-0451-VALIDATION"
    )
    assert validation_item["state"] == "[_]" and validation_item["attempts"] == 1
    assert all(row["accepted_receipt_ids"] == [] for row in local_tasks["nodes"])
    assert next(
        row for row in local_tasks["nodes"] if row["id"] == "S56-M-0451-VALIDATION"
    )["state"] == "open"

    assert decision["reconciled_inputs"] == RECONCILED_INPUTS
    for name, expected in RECONCILED_INPUTS.items():
        assert sha256(HERE / name) == expected, f"reconciled input drifted: {name}"
    assert decision["authority_inputs"] == AUTHORITY_INPUTS
    for name, expected in AUTHORITY_INPUTS.items():
        assert sha256(ROOT / name) == expected, f"authority input drifted: {name}"
    for name, expected in TOOL_INPUTS.items():
        assert sha256(ROOT / name) == expected, f"tool input drifted: {name}"

    canonical = statement["canonical_formal_target"]
    assert canonical["declaration_or_expression"] == (
        "Stage1Instances.THM_M_0451.NeronTateCanonicalHeightTarget"
    )
    assert canonical["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert anchor["decision"]["root_machine_classification"] == "M3"
    assert anchor["decision"]["exact_external_closure_found"] is False
    assert anchor["decision"]["theorem_complete"] is False
    assert registry["root_obligation_id"] == graphs["root_obligation_id"] == "M0451-ROOT"
    assert registry["frozen_denominators"]["inventory"] == INVENTORY_IDS
    assert [row["obligation_id"] for row in registry["obligations"]] == INVENTORY_IDS
    closure = graphs["closure_boundary"]
    assert closure["closed_obligations"] == []
    assert closure["root_closed"] is closure["audit_complete"] is False
    assert closure["theorem_complete"] is False
    assert closure["remaining_root_cut_set"] == ACCEPTED_CUT

    assert validation["support_state"] == "provisional_worker_selftest"
    assert validation["accepted"] is validation["release_grade"] is False
    assert validation["result"]["root_closed"] is False
    assert validation["result"]["audit_complete"] is False
    assert validation["result"]["theorem_complete"] is False
    assert validation["accepted_remaining_root_cut_set"] == ACCEPTED_CUT
    assert validation["proposed_remaining_root_cut_set_after_proof_acceptance"] == PROPOSED_CUT
    assert proof["accepted"] is False and proof["result"]["root_closed"] is False
    assert proof["result"]["theorem_complete"] is False
    dependency = decision["dependency"]
    assert dependency["receipt_id"] == validation["receipt_id"]
    assert dependency["receipt_sha256"] == sha256(HERE / "validation-receipt.json")
    assert dependency["receipt_accepted"] is dependency["master_accepted"] is False
    assert dependency["receipt_release_grade"] is False

    result = decision["decision"]
    assert result["verdict"] == "blocked"
    assert result["lifecycle_before"] == result["lifecycle_after"] == "planned"
    vector = {"H": "H1", "M": "M3", "R": "R3"}
    assert result["root_vector_before"] == result["root_vector_after"] == vector
    assert result["audit_complete"] is result["theorem_complete"] is False
    assert result["release_accepted"] is False and result["accepted_receipt_ids"] == []
    assert result["first_failed_gate"] == "S56-10.2-DEPENDENCY-ACCEPTANCE"
    assert result["first_failed_gate_detail"] == (
        "dependency.S56-M-0451-VALIDATION.master_acceptance"
    )
    assert result["first_failed_theorem_gate"] == "M0451-APPROX.kernel_closure"
    assert result["next_failed_theorem_gate"] == "M0451-ZERO-TORSION.kernel_closure"
    assert result["accepted_remaining_root_cut_set"] == ACCEPTED_CUT
    assert result["proposed_cut_after_proof_acceptance"] == PROPOSED_CUT
    for gate in (
        "validation_dependency_master_accepted", "authoritative_public_projection_reconciled",
        "statement_source_normalization_resolved", "human_source_h0_accepted",
        "readability_r0_accepted", "accepted_foundation_profile",
        "complete_transitive_provenance_and_tcb", "immutable_clean_release_input",
        "cold_empty_cache_build", "offline_archive_replay",
        "complete_sbom_and_license_closure", "deterministic_release_bundle",
        "distinct_runner_independent_verification",
        "independently_implemented_minimal_verifier", "second_signed_attestation",
        "protected_ci_and_adversarial_gates", "master_acceptance",
    ):
        assert decision["evidence_reconciliation"][gate] is False, gate

    current_narrow_replay()

    if receipt is not None:
        assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
        assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
        assert receipt["support_state"] == "provisional_worker_selftest"
        assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
        assert receipt["release_grade"] is False
        assert receipt["result"]["verdict"] == "blocked"
        assert receipt["result"]["stdout_sha256"] == (
            spec["expected_outputs"][0]["semantic_sha256"]
        )
        assert receipt["result"]["stdout_bytes"] == spec["expected_outputs"][0]["bytes"]
        assert receipt["result"]["audit_complete"] is False
        assert receipt["result"]["theorem_complete"] is False
        assert receipt["root_vector_before"] == receipt["root_vector_after_worker_selftest"] == vector
        assert receipt["accepted_receipt_ids"] == []
        assert receipt["first_failed_gate"] == result["first_failed_gate"]
        assert receipt["first_failed_dependency_gate"] == result["first_failed_gate_detail"]
        assert receipt["first_failed_theorem_gate"] == result["first_failed_theorem_gate"]
        assert receipt["accepted_remaining_root_cut_set"] == ACCEPTED_CUT
        assert receipt["proposed_cut_after_proof_acceptance"] == PROPOSED_CUT
        assert receipt["recipe"] == {
            key: spec[key] for key in (
                "recipe_id", "cwd", "argv", "env_allowlist", "timeout_seconds",
                "network_policy", "network_enforcement", "expected_exit",
                "expected_outputs", "covered_obligation_ids", "covered_declarations",
                "covered_decisions",
            )
        }
        assert receipt["inputs"]["release_spec_sha256"] == sha256(HERE / "release-spec.json")
        assert receipt["inputs"]["release_decision_sha256"] == sha256(HERE / "release-decision.json")
        assert receipt["inputs"]["release_phase_sha256"] == sha256(HERE / "release-phase.md")
        assert receipt["inputs"]["check_release_sha256"] == sha256(HERE / "check_release.py")
        patch_inputs = receipt["repository_state"]["untracked_input_hashes"]
        assert set(patch_inputs) == CHANGED_PATHS - {
            ".stage1-worker-selftest.json",
            f"Stage1_Instances/{THEOREM}/release-receipt.json",
        }
        for relative, expected in patch_inputs.items():
            assert sha256(ROOT / relative) == expected
        ledger = "".join(
            f"{digest}  {relative}\n" for relative, digest in sorted(patch_inputs.items())
        )
        assert hashlib.sha256(ledger.encode()).hexdigest() == (
            receipt["repository_state"]["patch_sha256"]
        )
        assert set(receipt["changed_paths"]) == CHANGED_PATHS
        assert receipt["known_failures"] == decision["known_failures"]
        assert receipt["output_summary"] == list(SUMMARY_LINES)

    selftest_path = ROOT / ".stage1-worker-selftest.json"
    if selftest_path.exists():
        packet = load(selftest_path)
        if packet.get("item_id") == ITEM:
            assert set(packet) == {
                "item_id", "changed_paths", "commands", "output_summary",
                "base_revision", "known_failures", "state",
            }
            assert packet["state"] == "[_]" and packet["base_revision"] == BASE_REVISION
            assert set(packet["changed_paths"]) == CHANGED_PATHS
            assert packet["known_failures"] == decision["known_failures"]
            assert packet["output_summary"] == list(SUMMARY_LINES)

    status = run(["git", "status", "--short", "--untracked-files=all"]).stdout
    actual_changed = {
        line[3:] for line in status.splitlines()
        if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual_changed <= CHANGED_PATHS, (actual_changed, CHANGED_PATHS)
    for relative in actual_changed:
        assert_text_hygiene(ROOT / relative)
    print("\n".join(SUMMARY_LINES))


if __name__ == "__main__":
    main()
