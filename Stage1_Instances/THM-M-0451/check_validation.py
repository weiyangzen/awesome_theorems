#!/usr/bin/env python3
"""Fail-closed narrow validator for S56-M-0451-VALIDATION."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import time


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0451"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
ITEM = "S56-M-0451-VALIDATION"
THEOREM = "THM-M-0451"
BASE_REVISION = "a1a7e939e58f103f5ff5d23af51437fa8658aa04"
BASE_TREE = "d881fd9641fa3e5f3ebe5082b35672981e90adcf"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
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
ALL_DECLARATIONS = PROOF_DECLARATIONS | {VALIDATION_DECLARATION}
CANONICAL_IDS = [
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
EXPECTED_FIXED_INPUTS = {
    "Stage1_Instances/THM-M-0451/Statement.lean":
        "f288b8eb0959aa199c316bc0727f84a85df9d3c3612c257da49b94dd8a6a6c52",
    "Stage1_Instances/THM-M-0451/ObligationTree.lean":
        "96a2a4b4955baad71cd23ca45e3a60070d84dc6793f4751036d5fabc70831f38",
    "Stage1_Instances/THM-M-0451/Proof.lean":
        "7cab7cf2608dd7dd236c9d97834695a04fccdc11f54c1dfc2dc5d795e77bf11b",
    "Stage1_Instances/THM-M-0451/ProofAudit.lean":
        "08049b966a40ed5121e581e5a2d8f25c51bec265802cd3d08f123d5a29e0032c",
    "Stage1_Instances/THM-M-0451/Validation.lean":
        "edcbc59586453ec8f96c7692ea02162e621a86ab475d043a83215d171d1c1f62",
    "Stage1_Instances/THM-M-0451/statement.json":
        "789930d7eddc88137f5491140f4c265790bb0c12d554aa71cf11c41d38d357e4",
    "Stage1_Instances/THM-M-0451/anchor-audit.json":
        "92f4a43ef98277af3165a809f7159428d66455447ada11af48b9ae8dacc8c1c2",
    "Stage1_Instances/THM-M-0451/obligation-registry.json":
        "b31f76ecf12e6936dcbfe0e536df7b0a353f0adf83af31d07a96341b130ae100",
    "Stage1_Instances/THM-M-0451/typed-graphs.json":
        "b957531c419f6648336d1abbd51c161f81b5cdbd90f3a092335c2dfdabbf57ce",
    "Stage1_Instances/THM-M-0451/proof-receipt.json":
        "5ed343b673c102441d5d889823508bec6c53faf17c056e2485af1728bcfad5a6",
    "Stage1_Instances/THM-M-0451/task-dag.json":
        "7e4a1fa021fc5db54ebe213f60d5f5b77e87f91aed73239af8f7210d647730c1",
    "Stage1_Instances/THM-M-0451/source_statement_crosswalk.md":
        "250a1999ee9eef2db43f21073f03cd05b111fe1d22136d49cc6e0a7a06dda124",
    "Formalizations/Lean/lean-toolchain":
        "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "Formalizations/Lean/lake-manifest.json":
        "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
EXPECTED_TOOLS = {
    "lean": "3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf",
    "lake": "a608ff084d7e2af228b92a29d7c2fd083ba0580e46889175ec74a81678c98359",
    "python": "b8d8288faefdd300201f43fcf00f6f539a27218eeed3a3dff5ab10b9c4c99700",
    "git": "8a48eefa306b9a2a9c3e576784a74ad7485779279e5a46ec43361a1864760e45",
    "bwrap": "0abea81db798ebf6b4742ac0664802d97521547a353c2a0dbdc21d76cbbfd2c0",
}
EXPECTED_PROVENANCE = {
    "Mathlib/AlgebraicGeometry/EllipticCurve/Affine/Point.lean": (
        "07376bf4e749af9bf07dd592a7553e8a28c6e210",
        "3506899af1d461a468526a5488f5250038f68f7a5b33856a8655af3d32de77ea",
        "00233b31e01d00a2b3affe5c746c174f6279dee266d35fbbd03634385f48c9e9",
    ),
    "Mathlib/NumberTheory/Height/Basic.lean": (
        "341d341af156303d8eaf1dab41e32dc51e5b90fa",
        "2c82aa843b0519ef3e2f8ed6540c720f639f032101cfe14d7dc654c1c3cde7ac",
        "35fdbb63f76ec0db1626fd5dfdded0e7c109daa0254b41e67dd95680e39aa2b1",
    ),
    "Mathlib/NumberTheory/Height/NumberField.lean": (
        "eea77e3f6f101501024b27804699e340150abac8",
        "1f65072acec3a8b21bcf66c8b0e2613d19c4df7bbbe154ecec6d42fcca884953",
        "2840173f33b4d956643c3fe1b34e014cbb518766da40cc998c180c40844b08cb",
    ),
    "Mathlib/Analysis/SpecificLimits/Basic.lean": (
        "bc8ec6bb99d6f20d35ebe38f6b6d736e0ffe4868",
        "610f7383f9487ad6a68c0e27eeedc98236f5cb5cffed8bfbbf78cf2c43b521ca",
        "aa4bf5024b7b011d370e7e6d895e381de2404ec501a14273abc0bf1eb6dcf68b",
    ),
}
SUMMARY_LINES = (
    "PASS THM-M-0451 narrow validation",
    "kernel: exact statement, conditional composition, 11 proof declarations, recursive sorry audit, and same-worker split-field adapter probe replayed at trust zero with network denied",
    "trust: all 13 complete axiom reports are exactly propext, Classical.choice, Quot.sound; local prohibited constructs absent",
    "provenance: target hashes and selected clean pinned mathlib source, olean, remote, and license identities agree",
    "root open: exact elliptic height estimates and zero-to-torsion remain unproved; no frozen obligation receives accepted closure",
    "authority open: proof is provisional and accepted graph/task state is pre-proof; no worker reconciliation or debt promotion",
    "release blocked: complete provenance/TCB/SBOM, cold empty-cache offline replay, independent source review, and distinct signed runners are absent",
)
STARTED = time.monotonic()


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path: Path) -> dict:
    def reject_duplicates(pairs: list[tuple[str, object]]) -> dict:
        result: dict[str, object] = {}
        for key, value in pairs:
            if key in result:
                raise AssertionError(f"duplicate JSON key in {path}: {key}")
            result[key] = value
        return result

    value = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicates)
    assert isinstance(value, dict), path
    return value


def run(argv: list[str], *, cwd: Path = ROOT, timeout: float = 1200.0) -> str:
    remaining = 1200.0 - (time.monotonic() - STARTED)
    assert remaining > 0, "validation exceeded its 1200-second aggregate timeout"
    result = subprocess.run(
        argv, cwd=cwd, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        timeout=min(timeout, remaining), check=False,
    )
    if result.returncode:
        raise RuntimeError(f"validation failed ({result.returncode}): {argv!r}\n{result.stdout}")
    return result.stdout


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["git", *args], cwd=cwd).strip()


def without_comments(source: str) -> str:
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
        reports[declaration] = {part.strip() for part in body.split(",") if part.strip()}
    return reports


def sandboxed_lean(lean: str, lean_path: str, tmp: Path, source: str) -> str:
    output = source.removesuffix(".lean") + ".olean"
    return run([
        "bwrap", "--unshare-net", "--die-with-parent", "--ro-bind", "/", "/",
        "--bind", str(tmp), str(tmp), "--dev", "/dev", "--proc", "/proc",
        "--dir", "/run", "--setenv", "HOME", "/tmp/home", "--setenv", "TMPDIR",
        "/tmp", "--setenv", "LANG", "C.UTF-8", "--setenv", "LC_ALL", "C.UTF-8",
        "--setenv", "TZ", "UTC", "--setenv", "LEAN_NUM_THREADS", "1",
        "--setenv", "LEAN_PATH", f"{tmp}:{lean_path}", "--chdir", str(tmp), "--",
        lean, "--trust=0", "-t0", "-o", output, source,
    ])


def main() -> None:
    spec = load(HERE / "validation-spec.json")
    receipt = load(HERE / "validation-receipt.json")
    statement = load(HERE / "statement.json")
    anchor = load(HERE / "anchor-audit.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    proof_receipt = load(HERE / "proof-receipt.json")
    local_tasks = load(HERE / "task-dag.json")
    targets = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    assert spec["item_id"] == receipt["item_id"] == ITEM
    assert spec["theorem_id"] == receipt["theorem_id"] == THEOREM
    assert len(spec["recipes"]) == 1
    recipe = spec["recipes"][0]
    assert receipt["recipe"] == recipe
    assert recipe["cwd"] == "." and recipe["argv"] == [
        "python3", "-I", "-B", "Stage1_Instances/THM-M-0451/check_validation.py"
    ]
    assert recipe["timeout_seconds"] == 1200 and recipe["expected_exit"] == 0
    assert recipe["network_policy"] == "denied"
    assert set(recipe["covered_declarations"]) == ALL_DECLARATIONS

    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 93 and target["baseline"] == "L0"
    assert target["lifecycle_mode"] == "planned"
    assert target["rework_required"] is True and target["theorem_complete"] is False
    validation_item = next(row for row in execution["items"] if row["id"] == ITEM)
    proof_item = next(row for row in execution["items"] if row["id"] == "S56-M-0451-PROOF")
    assert validation_item == {
        "id": ITEM, "theorem_id": THEOREM, "execution_rank": 93,
        "phase": "validation", "layer": 5, "state": "[ ]",
        "depends_on": ["S56-M-0451-PROOF"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Run hermetic kernel, trust, provenance, and independent validation gates.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0, "children": [],
    }
    assert proof_item["state"] == "[_]" and proof_item["attempts"] == 1

    assert registry["root_obligation_id"] == graphs["root_obligation_id"] == "M0451-ROOT"
    ids = [row["obligation_id"] for row in registry["obligations"]]
    assert ids == CANONICAL_IDS
    assert {row["obligation_id"] for row in graphs["nodes"]} == set(CANONICAL_IDS)
    assert registry["frozen_against_statement_sha256"] == digest(HERE / "Statement.lean")
    assert registry["frozen_against_anchor_audit_sha256"] == digest(HERE / "anchor-audit.json")
    assert statement["canonical_formal_target"] == {
        "backend": "lean4",
        "module": "Stage1_Instances/THM-M-0451/Statement.lean",
        "declaration_or_expression": "Stage1Instances.THM_M_0451.NeronTateCanonicalHeightTarget",
        "elaborated_expression_sha256":
            "76392071dc0670ad9c58f8eabc2195eecd990545084cfce9d6ecb13696803ed8",
        "statement_file_sha256": EXPECTED_FIXED_INPUTS[
            "Stage1_Instances/THM-M-0451/Statement.lean"
        ],
    }
    closure = graphs["closure_boundary"]
    assert closure["closed_obligations"] == []
    assert closure["root_closed"] is False
    assert closure["audit_complete"] is False and closure["theorem_complete"] is False
    assert closure["remaining_root_cut_set"] == ACCEPTED_CUT

    assert proof_receipt["item_id"] == "S56-M-0451-PROOF"
    assert proof_receipt["support_state"] == "provisional_worker_selftest"
    assert proof_receipt["accepted"] is False
    assert proof_receipt["newly_closed_obligation_ids"] == []
    assert proof_receipt["accepted_closed_obligation_ids"] == []
    assert proof_receipt["inputs"] == {
        "proof_sha256": digest(HERE / "Proof.lean"),
        "statement_sha256": digest(HERE / "Statement.lean"),
        "obligation_tree_sha256": digest(HERE / "ObligationTree.lean"),
        "obligation_registry_sha256": digest(HERE / "obligation-registry.json"),
    }
    assert proof_receipt["proof_body"]["source_sha256"] == digest(HERE / "Proof.lean")
    assert proof_receipt["result"]["root_closed"] is False
    assert proof_receipt["result"]["theorem_complete"] is False
    assert proof_receipt["remaining_root_cut_set"] == PROPOSED_CUT
    assert receipt["accepted_remaining_root_cut_set"] == ACCEPTED_CUT
    assert receipt["proposed_remaining_root_cut_set_after_proof_acceptance"] == PROPOSED_CUT
    assert all(row["accepted_receipt_ids"] == [] for row in local_tasks["nodes"])
    assert next(row for row in local_tasks["nodes"] if row["id"] == proof_item["id"])["state"] == "open"

    for relative, expected in EXPECTED_FIXED_INPUTS.items():
        assert digest(ROOT / relative) == expected, f"stale validation input: {relative}"
        assert receipt["inputs"][relative] == expected
    for relative in (
        "Stage1_Instances/THM-M-0451/validation-spec.json",
        "Stage1_Instances/THM-M-0451/check_validation.py",
    ):
        assert receipt["inputs"][relative] == digest(ROOT / relative)

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by|run_tac|oracle)\b|"
        r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
        r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
        r"(?:axiom|constant|opaque|unsafe|extern)\b",
        re.MULTILINE,
    )
    for name in (
        "Statement.lean", "AnchorAudit.lean", "ObligationTree.lean", "Proof.lean",
        "ProofAudit.lean", "Validation.lean",
    ):
        code = without_comments((HERE / name).read_text(encoding="utf-8"))
        assert prohibited.search(code) is None, f"prohibited proof device in {name}"
    validation_code = without_comments((HERE / "Validation.lean").read_text(encoding="utf-8"))
    assert not re.search(r"^import (?:Proof|ObligationTree)$", validation_code, re.MULTILINE)
    assert "Proof." not in validation_code and "ObligationTree." not in validation_code

    manifest = load(LEAN_ROOT / "lake-manifest.json")
    mathlib_record = next(row for row in manifest["packages"] if row["name"] == "mathlib")
    assert mathlib_record["rev"] == MATHLIB_REVISION
    mathlib = (LEAN_ROOT / ".lake/packages/mathlib").resolve()
    assert mathlib.is_dir(), "pinned mathlib artifact is missing"
    assert git("rev-parse", "HEAD", cwd=mathlib) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == MATHLIB_TREE
    assert git("status", "--porcelain=v1", cwd=mathlib) == ""
    provenance = receipt["selected_provenance"]
    assert provenance["revision"] == MATHLIB_REVISION and provenance["tree"] == MATHLIB_TREE
    assert git("remote", "get-url", "origin", cwd=mathlib) == provenance["remote"]
    records = {row["file"]: row for row in provenance["selected_import_sources"]}
    assert set(records) == set(EXPECTED_PROVENANCE)
    for relative, (blob, source_hash, olean_hash) in EXPECTED_PROVENANCE.items():
        record = records[relative]
        assert record["git_blob"] == git("rev-parse", f"HEAD:{relative}", cwd=mathlib) == blob
        assert record["source_sha256"] == digest(mathlib / relative) == source_hash
        assert record["olean_sha256"] == digest(mathlib / record["olean"]) == olean_hash
    assert provenance["license_sha256"] == digest(mathlib / "LICENSE") == (
        "b40930bbcf80744c86c46a12bc9da056641d722716c378f5659b9e555ef833e1"
    )
    substrate = next(
        row for row in anchor["candidates"] if row["candidate_id"] == "M0451-MATHLIB-SUBSTRATE"
    )
    assert substrate["revision"] == MATHLIB_REVISION and substrate["tree"] == MATHLIB_TREE

    lean = run(["lake", "env", "which", "lean"], cwd=LEAN_ROOT).strip()
    lake = run(["lake", "env", "which", "lake"], cwd=LEAN_ROOT).strip()
    lean_path = run(["lake", "env", "printenv", "LEAN_PATH"], cwd=LEAN_ROOT).strip()
    tools = {
        "lean": Path(lean), "lake": Path(lake), "python": Path(os.path.realpath(shutil.which("python3") or "")),
        "git": Path(os.path.realpath(shutil.which("git") or "")),
        "bwrap": Path(os.path.realpath(shutil.which("bwrap") or "")),
    }
    for name, path in tools.items():
        assert path.is_file() and digest(path) == EXPECTED_TOOLS[name]
    assert hashlib.sha256((lean_path + "\n").encode()).hexdigest() == (
        receipt["environment"]["lean_path_sha256"]
    )

    with tempfile.TemporaryDirectory(prefix="m0451-validation-") as tmp_name:
        tmp = Path(tmp_name)
        names = (
            "Statement.lean", "AnchorAudit.lean", "ObligationTree.lean", "Proof.lean",
            "ProofAudit.lean", "Validation.lean",
        )
        for name in names:
            shutil.copy2(HERE / name, tmp / name)
        outputs = {name: sandboxed_lean(lean, lean_path, tmp, name) for name in names}

    proof_reports = axiom_reports(outputs["ProofAudit.lean"])
    assert set(proof_reports) == PROOF_DECLARATIONS, sorted(proof_reports)
    assert all(axioms == EXPECTED_AXIOMS for axioms in proof_reports.values())
    validation_reports = axiom_reports(outputs["Validation.lean"])
    assert validation_reports == {VALIDATION_DECLARATION: EXPECTED_AXIOMS}
    combined = "\n".join(outputs.values())
    assert "contains sorry" not in combined and "sorryAx" not in combined
    assert outputs["ProofAudit.lean"].count("Declarations are sorry-free!") == 12
    assert outputs["Validation.lean"].count("Declarations are sorry-free!") == 1

    result = receipt["result"]
    assert result["accepted_closed_obligation_ids"] == []
    assert result["root_closed"] is False and result["audit_complete"] is False
    assert result["theorem_complete"] is False
    for gate in (
        "structured_authority_reconciliation_gate", "statement_source_fidelity_gate",
        "complete_transitive_provenance_gate",
        "complete_transitive_tcb_gate", "hermetic_release_gate",
        "independent_distinct_runner_gate",
    ):
        assert result[gate] == "fail closed"
    assert receipt["accepted"] is False and receipt["release_grade"] is False
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["corroborated_partial_obligation_ids"] == recipe["covered_obligation_ids"]
    expected_output = recipe["expected_outputs"]
    assert len(expected_output) == 1
    assert expected_output[0]["semantic_sha256"] == receipt["result"]["stdout_sha256"] == (
        "c3f63daa5353abb31a191b72b5a6fe928468cb2ba4d18cdafdce572eded79e91"
    )
    assert expected_output[0]["bytes"] == receipt["result"]["stdout_bytes"] == 847
    expected_summary = "\n".join(SUMMARY_LINES) + "\n"
    assert hashlib.sha256(expected_summary.encode()).hexdigest() == expected_output[0]["semantic_sha256"]
    assert len(expected_summary.encode()) == expected_output[0]["bytes"]
    assert re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\+08:00", receipt["validation_started_at"])
    assert re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\+08:00", receipt["validation_finished_at"])
    assert receipt["validated_at"] == receipt["validation_finished_at"]
    assert receipt["repository_state"]["commit"] == BASE_REVISION
    assert receipt["repository_state"]["tree"] == BASE_TREE
    assert receipt["repository_state"]["dirty"] is True
    assert receipt["repository_state"]["release_evidence"] is False
    assert receipt["repository_state"]["patch_sha256"] == (
        "934d6b5715e7250627987c8e5d40ae0af5675fbe1859749b9f931959b074ccb4"
    )
    assert receipt["repository_state"]["untracked_input_hashes"] == {
        "Stage1_Instances/THM-M-0451/ProofAudit.lean":
            "08049b966a40ed5121e581e5a2d8f25c51bec265802cd3d08f123d5a29e0032c",
        "Stage1_Instances/THM-M-0451/Validation.lean":
            "edcbc59586453ec8f96c7692ea02162e621a86ab475d043a83215d171d1c1f62",
        "Stage1_Instances/THM-M-0451/check_validation.py":
            "92247c34a1eafa8fa07a653d46c82b3e3408234593d1bf3bc05fd64eb646ffb1",
        "Stage1_Instances/THM-M-0451/validation-receipt.json":
            "25a35418e4ba7beaa4509de3a31c28be35a245c706f368fb4aa216936d73d5ea",
        "Stage1_Instances/THM-M-0451/validation-spec.json":
            "6dd3da5f23f5d2cb1c5af807b69be83d5b7e0b18d3ec1e7621442615c67bb2d4",
    }
    assert receipt["debt_vector"]["accepted_before"] == (
        receipt["debt_vector"]["accepted_after_worker_validation"]
    ) == {"H": "H1", "M": "M3", "R": "R3"}
    assert receipt["first_failed_gate"] == "dependency.S56-M-0451-PROOF.master_acceptance"

    selftest_path = ROOT / ".stage1-worker-selftest.json"
    if selftest_path.exists():
        selftest = load(selftest_path)
        if selftest.get("item_id") == ITEM:
            assert set(selftest) == {
                "item_id", "changed_paths", "commands", "output_summary",
                "base_revision", "known_failures", "state",
            }
            assert selftest["state"] == "[_]"
            assert selftest["base_revision"] == BASE_REVISION
            assert selftest["changed_paths"] == receipt["changed_paths"]
            assert selftest["known_failures"] == receipt["known_failures"]

    print("\n".join(SUMMARY_LINES))


if __name__ == "__main__":
    main()
