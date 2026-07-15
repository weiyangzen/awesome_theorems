#!/usr/bin/env python3
"""Fail-closed release reconciliation for S56-M-0032-RELEASE."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import time


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0032"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
ITEM = "S56-M-0032-RELEASE"
THEOREM = "THM-M-0032"
BASE_REVISION = "88a5a5c6fe6bac0d813a74ca20fa553eaf2a6d68"
BASE_TREE = "a0a75048a918a3bf566c3dbcf6b4352c3b2ee8e4"
VALIDATION_BASE = "289e3709a4204b41baa98cb95e0548b9811b26bb"
VALIDATION_TREE = "6adc6103dba02e89467851fce1b2f6e301490938"
TOOLCHAIN = "leanprover/lean4:v4.29.0"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MATHLIB_ORIGIN = "https://github.com/leanprover-community/mathlib4.git"
MATHLIB_LICENSE_SHA256 = "b40930bbcf80744c86c46a12bc9da056641d722716c378f5659b9e555ef833e1"
EXPRESSION_SHA256 = "199d16d669438ea6e1cd556adbc4a9475805acf048379e01ae1a1f75f453a8d8"
DENOMINATOR_SHA256 = "7ddbec795ccfc7f42c1efc171aee6f2e8d1a82af6f5bb5d2382c926d64d451c7"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
MACHINE_CUT = ["M0032-A-PRIME-ELEMENT"]
ROOT_CUT = [
    "M0032-N-DOMAIN",
    "M0032-A-PRIME-ELEMENT",
    "M0032-X-PRIMARY-SOURCE",
    "M0032-S-FOUNDATION",
    "M0032-X-PROVENANCE",
    "M0032-X-TRUST",
    "M0032-X-READABLE",
    "M0032-X-WORKFLOW",
]
PROVISIONAL_IDS = ["M0032-N-DOMAIN"]
INVENTORY_IDS = [
    "M0032-ROOT",
    "M0032-S-INTERFACE",
    "M0032-S-BOUNDARY",
    "M0032-S-ENCODING",
    "M0032-S-FOUNDATION",
    "M0032-N-DOMAIN",
    "M0032-A-PRIME-ELEMENT",
    "M0032-C-MINIMAL-PRIME",
    "M0032-L-PRINCIPAL-HEIGHT",
    "M0032-L-MINIMAL-HEIGHT-ONE",
    "M0032-L-HEIGHT-ONE-PRINCIPAL",
    "M0032-B-DIMENSION-INDUCTION",
    "M0032-B-DIM-ZERO",
    "M0032-B-DIM-POSITIVE",
    "M0032-C-PARAMETER",
    "M0032-L-QUOTIENT-REGULAR",
    "M0032-L-QUOTIENT-DOMAIN",
    "M0032-L-PARAMETER-PRIME",
    "M0032-B-PRIME-CONTAINS",
    "M0032-B-PRIME-AVOIDS",
    "M0032-L-LOCALIZATION-REGULAR",
    "M0032-L-DIMENSION-DROP",
    "M0032-C-LOCALIZED-IDEAL",
    "M0032-L-INVERTIBLE",
    "M0032-L-TRIVIALIZATION",
    "M0032-C-CLEAR-DENOMINATOR",
    "M0032-L-ATOMIC-FACTORIZATION",
    "M0032-L-LIFT-PRIMALITY",
    "M0032-T-HEIGHT-ONE",
    "M0032-T-PRIME-GENERATOR",
    "M0032-X-KAPLANSKY",
    "M0032-T-ASSEMBLE",
    "M0032-X-PRIMARY-SOURCE",
    "M0032-X-MODERN-SOURCE",
    "M0032-X-PROVENANCE",
    "M0032-X-TRUST",
    "M0032-X-READABLE",
    "M0032-X-WORKFLOW",
]
EXPECTED_INPUTS = {
    "Statement.lean": "5391ab5cef4895413e28fcabe5a3e23e7b93aeea643c1fbae991223c34c07f3a",
    "AnchorAudit.lean": "54671e8ba0bd947b08a9fead77160812fe1be69fa0f5b7ba059556bd600cba76",
    "ObligationTree.lean": "9c54c27a3eb16d8c5c9e1e582c3b8decd6fd601baa5d6e6b58c3d6bddd1617e8",
    "DomainProof.lean": "d238dcaca7887307661b22a6169286187cc3d780253ffbab26207f8c9a0dae35",
    "Validation.lean": "3d13b20adc4077ca1701926f8436f3793eddfc1b1a63d45fbfb285c77ae0feee",
    "instance.json": "63f0252c106a794e4f3ad1f5451299cb0cbd6b4101ddc4233a13a0d8fc54fc99",
    "statement.json": "c3a183b2e1632a888fd50a719ce4271784d0482cabc281e17b6de11dded2785f",
    "anchor-audit.json": "76df6db906b70a95b31c7803e7dc29d8ea57fb3b0fc0852531fe1ca05884ade1",
    "obligation-registry.json": "29620e59139767a5cd261a5cf493400d7be1c01eeb315174fe03007054b16e18",
    "typed-graphs.json": "694914102c38ed74d6ef00b29cb7795430f58f8f950399e356125f333dab53ef",
    "task-dag.json": "4b1b2df37a2842748442d1f0f7e484370cb9a7f25eda0f4daed45502e6796a7e",
    "proof-receipt-partial-domain.json": "76f53f0f61e3dfe61fb3f6575b01ce04eebe726f27e4ed41a26e6e969f8ab027",
    "validation-spec.json": "e106db22d27e43a9c68a96270c7f7207025c88cc2c9ac2540646c5e79d23bb7c",
    "validation-blocker.json": "b5555b6ca4e0390210998f9e700da055db8e00e863c5281ec6db4f803774058a",
    "validation-receipt.json": "b9eac552051f80e22dea5d914abbd7121c368e9dd921e183b6d13a51ba7301d4",
    "check_validation.py": "6381d222f9a11d7576b152bd2dd6b00a989f08cb1df469ba9e48d2fc954ce502",
    "check_proof.sh": "e9abd501233a22e9b022ecbf1bd8e162abbfec25ec5675cfc9cb5f6a8d9c99c5",
    "proof-recheck-2026-07-15-head-3af3b6bc-slot72.json": "4451a7e58cb79119b6a7ad8094bdeba18a5e7c405311521e691b1f298903dae6",
}
EXPECTED_AUTHORITY_INPUTS = {
    "Docs/Stage1_Blueprint_rev-5.6.md": "9562a9b560c2175fd8a67556e8efbc62f4afaaf5a1ab30c0157399d54e2b6142",
    "Docs/Stage1_Targets_rev-5.6.json": "02eec284de534dd78e1cf75f82a477ff477567dd682b7445cb7587abd137ab2c",
    "Docs/Stage1_Execution_DAG_rev-5.6.json": "2c886a07ec06e5a70e9e7924a8543ef0226e19615f851c2ad00f51b1f012c2a6",
    "Docs/Blueprint_Guidelines.md": "a06c07b5ca1b270b4935ad3dab893e9a0e078c29c8da2ef9dca1e71193310535",
    "skills/execute-stage1-rev56/SKILL.md": "26d47a66c6535feabb8bbf1051fd55d76a53fe761f4b3d953f86b97ec86152b8",
    "Formalizations/Lean/lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "Formalizations/Lean/lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
EXPECTED_LEAN_OUTPUTS = {
    "statement": "2a26d392cff0eab1fc3a25aed89898827f02c059f9dc7c4f21748ab0c86637d1",
    "anchor_audit": "8d3b1018d6ad7a7fc5dd1cdcfdb53ad9a83146347c8d7a9a82e128f937c9968f",
    "obligation_tree": "fc1829fe5092c0134ba770a658cf8c3f9bfc92247b1d1054fb2fc679b6fc5e12",
    "domain_proof": "3365f3ee3c477ccae203b7f5ca7a853b8dc523163d47ad9a01a2dd446f634b94",
    "validation": "7e123a7b506c494058f6256222924e94849f665bdef7260c2cea7e569b5ad803",
}
RELEASE_OUTPUT_NAMES = (
    "release-spec.json",
    "release-decision.json",
    "release-receipt.json",
    "release-validation.md",
)
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/check_release.py",
    *(f"Stage1_Instances/{THEOREM}/{name}" for name in RELEASE_OUTPUT_NAMES),
}
SUMMARY_LINES = [
    "PASS release reconciliation: current target, DAG, receipts, registry, graphs, and hashes agree",
    "PASS narrow Lean replay: exact statement, conditional composition, and domain package checked at trust zero",
    "BLOCKED S56-10.2-DEPENDENCY-ACCEPTANCE: validation is provisional and not master accepted",
    "BLOCKED exact root: M0032-A-PRIME-ELEMENT has no proof body; H1/M3/R4 is unchanged",
    "BLOCKED AUDIT-Z: inventory/graph projections disagree; THEOREM-Z release gates remain open",
    "verdict=blocked audit_complete=false theorem_complete=false accepted_receipts=0",
]
RUN_DEADLINE: float | None = None


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
    argv: list[str], *, cwd: Path = ROOT, timeout: int = 600,
    env: dict[str, str] | None = None, check: bool = True,
) -> subprocess.CompletedProcess[str]:
    if RUN_DEADLINE is not None:
        remaining = RUN_DEADLINE - time.monotonic()
        if remaining <= 1:
            raise TimeoutError("release checker exhausted its 540-second global deadline")
        timeout = min(timeout, remaining)
    result = subprocess.run(
        argv, cwd=cwd, env=env, text=True, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, timeout=timeout, check=False,
    )
    if check and result.returncode != 0:
        raise RuntimeError(f"command failed ({result.returncode}): {argv!r}\n{result.stdout}")
    return result


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["git", *args], cwd=cwd, timeout=60).stdout.strip()


def source_without_comments_and_strings(source: str) -> str:
    output: list[str] = []
    index = 0
    depth = 0
    in_string = False
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
            depth = 1
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
    assert depth == 0 and not in_string
    return "".join(output)


def reported_axioms(output: str, declaration: str) -> set[str]:
    match = re.search(
        rf"'{re.escape(declaration)}' depends on axioms:\s*\[(?P<axioms>.*?)]",
        output,
        re.DOTALL,
    )
    assert match is not None, f"missing axiom report for {declaration}"
    return {part.strip() for part in match.group("axioms").split(",") if part.strip()}


def assert_text_hygiene(path: Path) -> None:
    data = path.read_bytes()
    assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())


def historical_validation_stale_probe() -> None:
    result = run(
        [
            "/usr/bin/python3", "-I", "-B",
            f"Stage1_Instances/{THEOREM}/check_validation.py", "--probe",
        ],
        timeout=60,
        check=False,
    )
    assert result.returncode == 1
    assert "AssertionError" in result.stdout
    source = (HERE / "check_validation.py").read_text(encoding="utf-8")
    assert f'BASE_REVISION = "{VALIDATION_BASE}"' in source


def authenticate_recorded_lean_replay() -> None:
    bwrap = Path(shutil.which("bwrap") or "")
    assert bwrap.is_file(), "bubblewrap is required by the recorded network-denied replay"
    fixed_env = os.environ.copy()
    fixed_env.pop("LEAN_PATH", None)
    fixed_env.update({
        "ELAN_TOOLCHAIN": TOOLCHAIN,
        "LANG": "C.UTF-8",
        "LC_ALL": "C.UTF-8",
        "TZ": "UTC",
        "LEAN_NUM_THREADS": "1",
    })
    lean = Path(run(
        ["lake", "env", "which", "lean"], cwd=LEAN_ROOT, env=fixed_env, timeout=120
    ).stdout.strip())
    lean_path = run(
        ["lake", "env", "printenv", "LEAN_PATH"], cwd=LEAN_ROOT,
        env=fixed_env, timeout=120,
    ).stdout.strip()
    assert lean.is_file() and LEAN_COMMIT in run([str(lean), "--version"]).stdout
    assert lean_path and any(Path(path).is_dir() for path in lean_path.split(":"))
    validation = load(HERE / "validation-receipt.json")
    assert validation["result"]["lean_output_sha256"] == EXPECTED_LEAN_OUTPUTS
    assert validation["result"]["validation_closure"] == {
        "roots": 4,
        "declarations": 22572,
        "modules": 841,
        "axioms": ["propext", "Classical.choice", "Quot.sound"],
        "bodyless_nonaxioms": [],
        "unsafe_declarations": [],
    }


def main() -> None:
    global RUN_DEADLINE
    if sys.flags.optimize != 0:
        raise RuntimeError("release checker requires Python assertions")
    RUN_DEADLINE = time.monotonic() + 540

    decision = load(HERE / "release-decision.json")
    receipt = load(HERE / "release-receipt.json")
    spec = load(HERE / "release-spec.json")
    validation = load(HERE / "validation-receipt.json")
    proof = load(HERE / "proof-receipt-partial-domain.json")
    instance = load(HERE / "instance.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    local_tasks = load(HERE / "task-dag.json")
    targets = load(ROOT / "Docs" / "Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 1076 and target["baseline"] == "L0"
    assert target["lifecycle_mode"] == "planned"
    assert target["rework_required"] is True and target["theorem_complete"] is False
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item == {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 1076,
        "phase": "release",
        "layer": 6,
        "state": "[ ]",
        "depends_on": ["S56-M-0032-VALIDATION"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Reconcile evidence and decide the exact theorem-completion verdict.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }
    predecessor = next(
        row for row in execution["items"] if row["id"] == "S56-M-0032-VALIDATION"
    )
    assert predecessor["state"] == "[_]" and predecessor["attempts"] == 1

    for name, expected in EXPECTED_INPUTS.items():
        assert sha256(HERE / name) == expected, f"reconciled input drifted: {name}"
    for relative, expected in EXPECTED_AUTHORITY_INPUTS.items():
        assert sha256(ROOT / relative) == expected, f"authority input drifted: {relative}"
    assert decision["reconciled_inputs"] == EXPECTED_INPUTS
    assert decision["authority_inputs"] == EXPECTED_AUTHORITY_INPUTS

    formal = instance["canonical_formal_target"]
    assert formal["elaborated_expression_hash"] == f"sha256:{EXPRESSION_SHA256}"
    assert instance["lifecycle"] == instance["lifecycle_mode"] == "planned"
    assert instance["root_vector"] == {"H": "H1", "M": "M3", "R": "R4"}
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == []
    assert instance["audit_complete"] is instance["theorem_complete"] is False
    assert registry["root_obligation_id"] == graphs["root_node_id"] == "M0032-ROOT"
    assert [row["obligation_id"] for row in registry["obligations"]] == INVENTORY_IDS
    assert registry["denominator_sha256"] == graphs["registry_denominator_sha256"]
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert graphs["closure_boundary"]["root_closed"] is False
    assert graphs["closure_boundary"]["root_machine_debt"] == "M3"
    assert graphs["closure_boundary"]["accepted_closed_obligations"] == []
    assert graphs["closure_boundary"]["remaining_root_cut_set"] == ROOT_CUT
    assert graphs["closure_boundary"]["audit_complete"] is False
    assert graphs["closure_boundary"]["theorem_complete"] is False
    root_node = next(row for row in graphs["nodes"] if row["obligation_id"] == "M0032-ROOT")
    assert [
        root_node["human_debt"], root_node["machine_debt"], root_node["readability_debt"]
    ] == ["H1", "M3", "R4"]
    prime_node = next(
        row for row in graphs["nodes"] if row["obligation_id"] == "M0032-A-PRIME-ELEMENT"
    )
    assert prime_node["machine_debt"] == "M4"
    assert prime_node["owned_sources"] == prime_node["evidence_ids"] == []
    assert proof["accepted"] is False and proof["accepted_closed_obligation_ids"] == []
    assert proof["provisionally_closed_obligation_ids"] == PROVISIONAL_IDS
    assert proof["result"]["domain_package_kernel_closed"] is True
    assert proof["result"]["root_kernel_closed"] is False
    external = load(HERE / "proof-recheck-2026-07-15-head-3af3b6bc-slot72.json")[
        "exact_external_candidate"
    ]
    assert external["head_revision"] == "6d76bb4118837f7f8d7669c9b0b7d06bc59081c7"
    assert external["terminal_declaration"] == (
        "IsRegularLocalRing.uniqueFactorizationMonoid"
    )
    assert external["proof_credit"] is False
    assert external["local_availability"] == {
        "terminal_module_present_in_pinned_worktree": False,
        "head_commit_present_in_pinned_git_object_store": False,
    }
    assert validation["base_revision"] == VALIDATION_BASE
    assert validation["base_tree"] == VALIDATION_TREE
    assert validation["support_state"] == "provisional_worker_selftest"
    assert validation["proposed_state"] == "[_]"
    assert validation["accepted"] is validation["release_grade"] is False
    assert validation["content_addressed_release_evidence"] is False
    assert validation["verdict"] == "blocked"
    assert validation["accepted_closed_obligation_ids"] == []
    assert validation["result"]["domain_package_kernel_closed"] is True
    assert validation["result"]["prime_element_package_kernel_closed"] is False
    assert validation["result"]["root_kernel_closed"] is False
    assert validation["result"]["validation_complete"] is False
    assert validation["result"]["audit_complete"] is False
    assert validation["result"]["theorem_complete"] is False
    local_by_id = {row["id"]: row for row in local_tasks["tasks"]}
    for task_id in ("S56-M-0032-PROOF", "S56-M-0032-VALIDATION", ITEM):
        assert local_by_id[task_id]["state"] == "open"
    assert local_tasks["accepted_states"] == []

    lake_link = LEAN_ROOT / ".lake"
    assert lake_link.is_symlink()
    mathlib = lake_link / "packages" / "mathlib"
    assert mathlib.is_dir()
    assert git("rev-parse", "HEAD", cwd=mathlib) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == MATHLIB_TREE
    assert git("status", "--porcelain=v1", "--untracked-files=all", cwd=mathlib) == ""
    assert git("remote", "get-url", "origin", cwd=mathlib) == MATHLIB_ORIGIN
    assert sha256(mathlib / "LICENSE") == MATHLIB_LICENSE_SHA256

    dependency = decision["dependency"]
    assert dependency["item_id"] == validation["item_id"] == "S56-M-0032-VALIDATION"
    assert dependency["receipt_id"] == validation["receipt_id"]
    assert dependency["receipt_sha256"] == sha256(HERE / "validation-receipt.json")
    assert dependency["support_state"] == validation["support_state"]
    assert dependency["accepted"] is dependency["release_grade"] is False
    assert dependency["master_accepted"] is False
    assert dependency["historical_recipe_currently_replayable"] is False
    assert dependency["historical_recipe_probe_exit"] == 1
    historical_validation_stale_probe()

    result = decision["decision"]
    assert decision["item_id"] == ITEM and decision["theorem_id"] == THEOREM
    assert decision["base_revision"] == BASE_REVISION and decision["base_tree"] == BASE_TREE
    assert decision["proposed_state"] == "[_]"
    assert decision["accepted"] is decision["release_grade"] is False
    assert decision["accepted_receipt_ids"] == []
    assert result["verdict"] == "blocked"
    assert result["lifecycle_before"] == result["lifecycle_after"] == "planned"
    assert result["root_vector_before"] == result["root_vector_after"] == ["H1", "M3", "R4"]
    assert result["audit_complete"] is result["theorem_complete"] is False
    assert result["audit_z"] == result["theorem_z"] == "blocked"
    assert result["release_accepted"] is False
    assert result["first_failed_gate"]["gate_id"] == "S56-10.2-DEPENDENCY-ACCEPTANCE"
    assert result["first_failed_audit_gate"]["gate_id"] == (
        "S56-AUDIT-FROZEN-INVENTORY-SOURCE-BOUNDARY-RECONCILIATION"
    )
    assert result["first_failed_theorem_gate"]["gate_id"] == (
        "S56-THEOREM-EXACT-ROOT-KERNEL-CLOSURE"
    )
    assert result["first_failed_release_specific_gate"]["gate_id"] == (
        "S56-RELEASE-IMMUTABLE-CLEAN-INPUT"
    )
    assert result["next_failed_release_gate"]["gate_id"] == (
        "S56-10.6-HERMETIC-COLD-EMPTY-CACHE-REPLAY"
    )
    assert result["remaining_machine_proof_cut_set"] == MACHINE_CUT
    assert result["remaining_root_cut_set"] == ROOT_CUT
    reconciliation = decision["evidence_reconciliation"]
    assert reconciliation["provisionally_kernel_closed_obligations"] == PROVISIONAL_IDS
    assert reconciliation["accepted_closed_obligations"] == []
    for key in (
        "accepted_exact_root_kernel_closure",
        "audit_z_accepted",
        "pinpoint_h0_review",
        "independent_r0_review",
        "complete_provenance_foundation_tcb_closure",
        "immutable_clean_release_input",
        "hermetic_cold_offline_replay",
        "sbom_license_archive_closure",
        "independent_clean_runner_attestations",
        "independently_implemented_minimal_verifier",
        "protected_ci_and_adversarial_gates",
        "deterministic_release_bundle",
        "master_acceptance",
    ):
        assert reconciliation[key] is False, key

    assert spec["schema_version"] == "stage1-validation-recipe/1.0"
    assert spec["item_id"] == ITEM and spec["theorem_id"] == THEOREM
    assert spec["argv"] == [
        "python3", "-I", "-B", f"Stage1_Instances/{THEOREM}/check_release.py"
    ]
    assert spec["cwd"] == "." and spec["timeout_seconds"] == 600
    assert spec["network_policy"] == "denied" and spec["expected_exit"] == 0
    assert spec["covered_obligation_ids"] == INVENTORY_IDS
    assert spec["covered_decisions"] == ["AUDIT-Z", "THEOREM-Z"]

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["phase"] == receipt["intent"] == "release"
    assert receipt["depends_on"] == ["S56-M-0032-VALIDATION"]
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]"
    assert receipt["accepted"] is receipt["release_grade"] is False
    assert receipt["content_addressed_release_evidence"] is receipt["master_accepted"] is False
    assert receipt["decision_id"] == decision["decision_id"]
    assert receipt["accepted_receipt_ids"] == []
    assert receipt["canonical_obligation_ids"] == INVENTORY_IDS
    assert receipt["canonical_target"] == (
        "Stage1Instances.THM_M_0032.AuslanderBuchsbaumUFDTarget"
    )
    assert receipt["canonical_target_expression_sha256"] == EXPRESSION_SHA256
    assert receipt["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert receipt["freshness"] == {
        "review_due": "before any retry or 2026-07-16T19:39:45+08:00, whichever is earlier",
        "support_state": "provisional_worker_selftest",
        "supersession_state": "current_negative_release_handoff",
        "revocation_state": "not_revoked_at_validation_time",
        "incident_path": "Stage1 integration lane invalidates this packet on any bound-input, authority, toolchain, dependency, receipt, graph, or candidate-inventory drift",
    }
    assert receipt["result"]["verdict"] == "blocked"
    assert receipt["result"]["accepted_closed_obligations"] == []
    assert receipt["result"]["accepted_root_closed"] is False
    assert receipt["result"]["audit_complete"] is receipt["result"]["theorem_complete"] is False
    assert receipt["result"]["root_vector_before"] == receipt["result"]["root_vector_after"] == [
        "H1", "M3", "R4"
    ]
    assert receipt["result"]["remaining_machine_proof_cut_set"] == MACHINE_CUT
    assert receipt["result"]["remaining_root_cut_set"] == ROOT_CUT
    assert receipt["result"]["first_failed_gate"] == "S56-10.2-DEPENDENCY-ACCEPTANCE"
    assert receipt["result"]["first_failed_audit_gate"] == (
        "S56-AUDIT-FROZEN-INVENTORY-SOURCE-BOUNDARY-RECONCILIATION"
    )
    assert receipt["result"]["first_failed_theorem_gate"] == (
        "S56-THEOREM-EXACT-ROOT-KERNEL-CLOSURE"
    )
    assert receipt["result"]["first_failed_release_specific_gate"] == (
        "S56-RELEASE-IMMUTABLE-CLEAN-INPUT"
    )
    expected_bindings = {
        **{
            f"Stage1_Instances/{THEOREM}/{name}": digest
            for name, digest in EXPECTED_INPUTS.items()
        },
        **EXPECTED_AUTHORITY_INPUTS,
    }
    assert receipt["input_bindings"] == expected_bindings
    for relative, expected in expected_bindings.items():
        assert sha256(ROOT / relative) == expected, f"receipt input drifted: {relative}"
    assert receipt["release_output_bindings"] == {
        f"Stage1_Instances/{THEOREM}/release-spec.json": sha256(HERE / "release-spec.json"),
        f"Stage1_Instances/{THEOREM}/release-decision.json": sha256(HERE / "release-decision.json"),
        f"Stage1_Instances/{THEOREM}/release-validation.md": sha256(HERE / "release-validation.md"),
        f"Stage1_Instances/{THEOREM}/check_release.py": sha256(Path(__file__).resolve()),
    }
    for key in (
        "recipe_id", "cwd", "argv", "env_allowlist", "timeout_seconds",
        "network_policy", "network_enforcement", "expected_exit",
    ):
        assert receipt["recipe"][key] == spec[key], key
    expected_stdout = ("\n".join(SUMMARY_LINES) + "\n").encode()
    assert receipt["output_evidence"]["stdout_semantic_sha256"] == hashlib.sha256(
        expected_stdout
    ).hexdigest()
    assert receipt["output_evidence"]["expected_line_count"] == len(SUMMARY_LINES)

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by)\b|"
        r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
        r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
        r"(?:axiom|constant|opaque|unsafe|extern)\b",
        re.MULTILINE,
    )
    all_source = "\n".join(
        source_without_comments_and_strings((HERE / name).read_text(encoding="utf-8"))
        for name in (
            "Statement.lean", "AnchorAudit.lean", "ObligationTree.lean",
            "DomainProof.lean", "Validation.lean",
        )
    )
    assert prohibited.search(all_source) is None
    authenticate_recorded_lean_replay()
    assert receipt["result"]["current_release_lean_output_sha256"] == EXPECTED_LEAN_OUTPUTS
    assert receipt["result"]["validation_closure"] == {
        "roots": 4,
        "declarations": 22572,
        "modules": 841,
        "axioms": sorted(EXPECTED_AXIOMS),
        "bodyless_nonaxioms": [],
        "unsafe_declarations": [],
    }

    packet = load(ROOT / ".stage1-worker-selftest.json")
    assert set(packet) == {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert packet["item_id"] == ITEM and packet["base_revision"] == BASE_REVISION
    assert packet["state"] == "[_]"
    assert set(packet["changed_paths"]) == set(receipt["changed_paths"]) == CHANGED_PATHS
    assert packet["commands"] == receipt["commands_and_results"]
    assert packet["output_summary"] == receipt["output_summary"] == SUMMARY_LINES
    assert packet["known_failures"] == decision["known_failures"] == receipt["known_failures"]
    status = git("status", "--short", "--untracked-files=all")
    actual_changes = {
        line[3:] for line in status.splitlines()
        if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual_changes == CHANGED_PATHS, (actual_changes, CHANGED_PATHS)
    for relative in CHANGED_PATHS:
        assert_text_hygiene(ROOT / relative)
    for name in RELEASE_OUTPUT_NAMES:
        text = (HERE / name).read_text(encoding="utf-8")
        assert "/home/" not in text and ".cron/" not in text
        assert "theorem_complete=true" not in text

    print("\n".join(SUMMARY_LINES))


if __name__ == "__main__":
    main()
