#!/usr/bin/env python3
"""Fail-closed release reconciliation for S56-M-0072-RELEASE."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile


if not __debug__:
    raise SystemExit("check_release.py requires Python assertions")


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0072"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM = "S56-M-0072-RELEASE"
THEOREM = "THM-M-0072"
BASE_REVISION = "d44ed2b11fb201a761afad9b133caa8bc97fd710"
BASE_TREE = "9602084a1c32fa6685f1c60eff540528226decff"
TOOLCHAIN = "leanprover/lean4:v4.29.0"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MATHLIB_REMOTE = "https://github.com/leanprover-community/mathlib4.git"
LEAN_SHA256 = "3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf"
LAKE_SHA256 = "a608ff084d7e2af228b92a29d7c2fd083ba0580e46889175ec74a81678c98359"
PYTHON_SHA256 = "b8d8288faefdd300201f43fcf00f6f539a27218eeed3a3dff5ab10b9c4c99700"
BWRAP_SHA256 = "0abea81db798ebf6b4742ac0664802d97521547a353c2a0dbdc21d76cbbfd2c0"
GIT_SHA256 = "5516c9f362c29376ab9a499a33082f9f611941d8c75930c880e30ad109e39c9a"
MATHLIB_LICENSE_SHA256 = "b40930bbcf80744c86c46a12bc9da056641d722716c378f5659b9e555ef833e1"
EXPRESSION_SHA256 = "c8a89538bd8b492ba31ce5d516a0f8fefef70a550e1d2fe74e39a4cba7849051"
DENOMINATOR_SHA256 = "7f5030b02a13572f021c17ac32f2472098e2a5de881bc5a4999716dd411f717b"
VALIDATION_RECEIPT_SHA256 = "7c958e00a91a405ea0fcc27dba243ed73b4249459cdda35f0a10ac7a0d7c3b7c"
ALLOWED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
VECTOR = {"H": "H1", "M": "M3", "R": "R4"}
INVENTORY_IDS = [
    "M0072-ROOT", "M0072-S-TARGET", "M0072-S-DOMAIN", "M0072-S-BOUNDARY",
    "M0072-S-TRANSPORT", "M0072-S-FOUNDATION", "M0072-N-OUTSIDE",
    "M0072-B-MEMBERSHIP", "M0072-T-INSIDE", "M0072-C-NORMAL",
    "M0072-L-INDEX-TWO", "M0072-C-QUOTIENT", "M0072-C-TRANSFER",
    "M0072-L-SYLOW-ODD", "M0072-C-COSET-ACTION", "M0072-L-FIXED-PARITY",
    "M0072-L-TRANSFER-FORMULA", "M0072-L-FACTOR-DICHOTOMY",
    "M0072-L-ODD-PRODUCT", "M0072-L-NOINDEX-TRANSFER",
    "M0072-B-CONTRADICTION", "M0072-T-OUTSIDE", "M0072-T-ASSEMBLE",
    "M0072-X-SOURCE", "M0072-X-PROVENANCE", "M0072-X-TRUST",
    "M0072-X-READABLE", "M0072-X-WORKFLOW",
]
PROVISIONAL_PROOF_IDS = [
    "M0072-ROOT", "M0072-N-OUTSIDE", "M0072-B-MEMBERSHIP",
    "M0072-T-INSIDE", "M0072-C-NORMAL", "M0072-L-INDEX-TWO",
    "M0072-C-QUOTIENT", "M0072-C-TRANSFER", "M0072-L-SYLOW-ODD",
    "M0072-C-COSET-ACTION", "M0072-L-FIXED-PARITY",
    "M0072-L-TRANSFER-FORMULA", "M0072-L-FACTOR-DICHOTOMY",
    "M0072-L-ODD-PRODUCT", "M0072-L-NOINDEX-TRANSFER",
    "M0072-B-CONTRADICTION", "M0072-T-OUTSIDE", "M0072-T-ASSEMBLE",
]
EXPECTED_INPUTS = {
    "README.md": "4cff214ddf30e5afbfca3430553a3d56252ac11e33d6295c6e5a861914f8109a",
    "Statement.lean": "0e9a35c7d2a9eaafb2aa6f8357277e9bf1e79e9a5e88500bda6cd8300a6757aa",
    "ObligationTree.lean": "e30e9833e607eea7a9dd025e86cd6f34a912ed375c0563186c0727424dcb838c",
    "AnchorAudit.lean": "5ef2cdf8984a7f728a9995e6c1afa7872a4cf579f9cf80f71486e08c56129731",
    "Proof.lean": "549f8b496b79d82071a93eb95a8e6809dd3afefcb7ee60392a8642fd6749ebc2",
    "Validation.lean": "1bf98acd7715b9efb10d97fb48bc36dd2cd4180ed9d86ea0b6ff896c274a987b",
    "instance.json": "d54c99adc532922ee41821cb3a1a97fbb55980f0087e04bc715d56b86e36a5ba",
    "task-dag.json": "0d838c49048bfb919104e544e147e419ba6fdf5047d61afb0da94cc51c531735",
    "statement.json": "ab2ab89125e95ced56ed588c965b03a283596dd6fb815f967bf9bb91114d1034",
    "source-statement-crosswalk.md": "fdb7992feb445b6000a591680aa20ae4a80d934305e5e569fb625e4c2747b2fd",
    "anchor-audit.json": "9124610a2becf3f4a5ff4972f9280235ad8217d10a79971ccddd5dbdf23bc6fd",
    "obligation-registry.json": "6e60eb6599e9fded2c5ce5100b469faedd20eaa83840917c6e979b5af12f2498",
    "typed-graphs.json": "d307d8c606150999add6b0e068510dcc70c2ddaa8945c944e1ed9f9980e67b8a",
    "intake-receipt.json": "b755c25bb0321dc719f3a79838332b034390a2ce11f52376bcf7aff97761edb4",
    "statement-receipt.json": "282753a07869637e1aca1e90f101994a4c8e55f964f382ed4ebc39a6a4133182",
    "anchor-audit-receipt.json": "ba1fdeba6311213ae895c016e713b81558951f8d78a59fa0575e6dede9665bcb",
    "obligation-tree-receipt.json": "9db92ae6a4d4a8862adb966b67eb1389ab2a3d431f66ee682a9f032db5b2c1ea",
    "proof-receipt.json": "b7c3c02e977540f8f5279ec5a75b5f9a082ab8bfd970bcb88520eab7d8b8b399",
    "validation-spec.json": "a45eb72a368c55b36666b75f2f2f75e09970e2316bca866f908114b9a642c356",
    "validation-receipt.json": VALIDATION_RECEIPT_SHA256,
    "check_validation.py": "fc96a32a4642ff997f000a763ddcdb372a3083ceff07e9ca83fa8a311c447ec9",
}
AUTHORITY_INPUTS = {
    "Docs/Stage1_Blueprint_rev-5.6.md": "7fee7ec2a7ca4aec249399c64feacf6803b1c2bc70b15409984ce09b74afece2",
    "Docs/Stage1_Targets_rev-5.6.json": "02eec284de534dd78e1cf75f82a477ff477567dd682b7445cb7587abd137ab2c",
    "Docs/Stage1_Execution_DAG_rev-5.6.json": "b5080b958f0d4a6d044d77ee55f1e28b2299729f531e64c1e46a25610e9b8f15",
    "skills/execute-stage1-rev56/SKILL.md": "26d47a66c6535feabb8bbf1051fd55d76a53fe761f4b3d953f86b97ec86152b8",
}
TOOL_INPUTS = {
    "lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/check_release.py",
    f"Stage1_Instances/{THEOREM}/release-decision.json",
    f"Stage1_Instances/{THEOREM}/release-receipt.json",
    f"Stage1_Instances/{THEOREM}/release-spec.json",
    f"Stage1_Instances/{THEOREM}/release-validation.md",
}
SUMMARY_LINES = [
    "PASS S56-M-0072-RELEASE reconciliation",
    "verdict=blocked lifecycle=planned accepted_root_vector=H1/M3/R4",
    "provisional_kernel_root=M0-L audit_complete=false theorem_complete=false",
    "accepted_receipts=0 accepted_obligations=0",
    "first_failed_gate=dependency.S56-M-0072-VALIDATION.master_acceptance",
    "first_failed_release_gate=S56-10.6-IMMUTABLE-CLEAN-INPUT",
    "next_failed_release_gate=S56-10.6-HERMETIC-COLD-EMPTY-CACHE-REPLAY",
]


def load(path: Path) -> dict:
    def reject_duplicates(pairs: list[tuple[str, object]]) -> dict:
        result: dict[str, object] = {}
        for key, value in pairs:
            assert key not in result, f"duplicate key {key!r} in {path}"
            result[key] = value
        return result

    value = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicates)
    assert isinstance(value, dict), path
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(argv: list[str], *, cwd: Path = ROOT, env: dict[str, str] | None = None) -> str:
    result = subprocess.run(
        argv, cwd=cwd, env=env, text=True, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, timeout=300, check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(f"command failed ({result.returncode}): {argv!r}\n{result.stdout}")
    return result.stdout


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["git", *args], cwd=cwd).strip()


def source_without_comments_and_strings(source: str) -> str:
    output: list[str] = []
    index = 0
    depth = 0
    in_string = False
    while index < len(source):
        if depth:
            if source.startswith("/-", index):
                depth += 1
                output.extend("  ")
                index += 2
            elif source.startswith("-/", index):
                depth -= 1
                output.extend("  ")
                index += 2
            else:
                output.append("\n" if source[index] == "\n" else " ")
                index += 1
        elif in_string:
            if source[index] == "\\" and index + 1 < len(source):
                output.extend("  ")
                index += 2
            elif source[index] == '"':
                in_string = False
                output.append(" ")
                index += 1
            else:
                output.append("\n" if source[index] == "\n" else " ")
                index += 1
        elif source.startswith("/-", index):
            depth = 1
            output.extend("  ")
            index += 2
        elif source.startswith("--", index):
            while index < len(source) and source[index] != "\n":
                output.append(" ")
                index += 1
        elif source[index] == '"':
            in_string = True
            output.append(" ")
            index += 1
        else:
            output.append(source[index])
            index += 1
    assert depth == 0 and not in_string
    return "".join(output)


def reported_axioms(output: str, declaration: str) -> set[str]:
    match = re.search(
        re.escape(f"'{declaration}' depends on axioms: [") + r"(.*?)]",
        output, re.DOTALL,
    )
    assert match is not None, f"missing axiom report for {declaration}"
    return {part.strip() for part in match.group(1).split(",") if part.strip()}


def assert_text_hygiene(path: Path) -> None:
    data = path.read_bytes()
    assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())


def narrow_replay() -> dict[str, str]:
    home = Path.home()
    env = {
        "HOME": str(home),
        "PATH": f"{home}/.elan/bin:/usr/bin:/bin",
        "ELAN_TOOLCHAIN": TOOLCHAIN,
        "LANG": "C.UTF-8",
        "LC_ALL": "C.UTF-8",
        "TZ": "UTC",
        "LEAN_NUM_THREADS": "1",
    }
    launcher = home / ".elan" / "bin" / "lake"
    lean = Path(run([str(launcher), "env", "which", "lean"], cwd=LEAN_ROOT, env=env).strip())
    lake = Path(run([str(launcher), "env", "which", "lake"], cwd=LEAN_ROOT, env=env).strip())
    assert sha256(lean) == LEAN_SHA256 and sha256(lake) == LAKE_SHA256
    assert sha256(Path("/usr/bin/python3").resolve()) == PYTHON_SHA256
    assert sha256(Path("/usr/bin/bwrap")) == BWRAP_SHA256
    assert sha256(Path("/usr/bin/git")) == GIT_SHA256
    assert LEAN_COMMIT in run([str(lean), "--version"], env=env)
    lean_path = run(
        [str(launcher), "env", "printenv", "LEAN_PATH"], cwd=LEAN_ROOT, env=env
    ).strip()

    with tempfile.TemporaryDirectory(prefix="stage1-m0072-release-", dir="/tmp") as raw:
        temp = Path(raw).resolve()
        (temp / "home").mkdir()
        for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
            (temp / name).write_bytes((HERE / name).read_bytes())
        base = [
            "/usr/bin/bwrap", "--ro-bind", "/", "/", "--bind", str(temp), str(temp),
            "--dev", "/dev", "--proc", "/proc", "--unshare-net", "--die-with-parent",
            "--clearenv", "--setenv", "HOME", str(temp / "home"), "--setenv", "TMPDIR",
            str(temp), "--setenv", "LANG", "C.UTF-8", "--setenv", "LC_ALL", "C.UTF-8",
            "--setenv", "TZ", "UTC", "--setenv", "LEAN_NUM_THREADS", "1",
            "--chdir", str(temp),
        ]

        def lean_run(name: str, module_path: str) -> str:
            return run(base + [
                "--setenv", "LEAN_PATH", module_path, str(lean), "--trust=0", "-t0",
                "-o", name.replace(".lean", ".olean"), name,
            ])

        outputs = {"statement": lean_run("Statement.lean", lean_path)}
        local_path = f"{temp}:{lean_path}"
        outputs["obligation_tree"] = lean_run("ObligationTree.lean", local_path)
        outputs["proof"] = lean_run("Proof.lean", local_path)
        outputs["validation"] = lean_run("Validation.lean", local_path)
        return outputs


def main() -> None:
    decision = load(HERE / "release-decision.json")
    receipt = load(HERE / "release-receipt.json")
    spec = load(HERE / "release-spec.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")
    instance = load(HERE / "instance.json")
    tasks = load(HERE / "task-dag.json")
    statement = load(HERE / "statement.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    proof = load(HERE / "proof-receipt.json")
    validation = load(HERE / "validation-receipt.json")
    targets = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    for name, expected in EXPECTED_INPUTS.items():
        assert sha256(HERE / name) == expected, f"reconciled input drifted: {name}"
    for relative, expected in AUTHORITY_INPUTS.items():
        assert sha256(ROOT / relative) == expected, f"authority input drifted: {relative}"
    for name, expected in TOOL_INPUTS.items():
        assert sha256(LEAN_ROOT / name) == expected, f"tool input drifted: {name}"

    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 1102
    assert target["lifecycle_mode"] == "planned" and target["baseline"] == "L0"
    assert target["rework_required"] is True and target["theorem_complete"] is False
    release_item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert release_item == {
        "id": ITEM, "theorem_id": THEOREM, "execution_rank": 1102,
        "phase": "release", "layer": 6, "state": "[ ]",
        "depends_on": ["S56-M-0072-VALIDATION"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Reconcile evidence and decide the exact theorem-completion verdict.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0, "children": [],
    }
    validation_item = next(
        row for row in execution["items"] if row["id"] == "S56-M-0072-VALIDATION"
    )
    assert validation_item["state"] == "[_]" and validation_item["attempts"] == 1
    local_release = next(row for row in tasks["tasks"] if row["id"] == ITEM)
    assert local_release["state"] == "open"
    assert local_release["depends_on"] == ["S56-M-0072-VALIDATION"]
    assert tasks["accepted_states"] == []

    assert instance["lifecycle"] == instance["lifecycle_mode"] == "planned"
    assert instance["root_vector"] == VECTOR
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == []
    assert instance["audit_complete"] is instance["theorem_complete"] is False
    formal = statement["canonical_formal_target"]
    assert formal["declaration_or_expression"] == (
        "Stage1Instances.THM_M_0072.ThompsonTransferLemmaTarget"
    )
    assert formal["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert registry["root_obligation_id"] == "M0072-ROOT"
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert registry["frozen_denominators"]["inventory"] == INVENTORY_IDS
    assert graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    closure = graphs["closure_boundary"]
    assert closure["root_closed"] is False
    assert closure["root_machine_classification"] == "M3"
    assert closure["accepted_closed_obligations"] == []
    assert closure["remaining_root_cut_set"] == ["M0072-T-OUTSIDE"]
    assert closure["audit_complete"] is closure["theorem_complete"] is False
    assert all(row["accepted"] is False for row in graphs["composition_certificates"])

    assert sha256(HERE / "validation-receipt.json") == VALIDATION_RECEIPT_SHA256
    assert proof["provisionally_closed_proof_obligation_ids"] == PROVISIONAL_PROOF_IDS
    assert proof["accepted_closed_obligation_ids"] == []
    assert proof["result"]["root_kernel_closed"] is True
    assert proof["result"]["accepted_root_closed"] is False
    assert validation["item_id"] == "S56-M-0072-VALIDATION"
    assert validation["receipt_id"] == "S56-M-0072-VALIDATION-WORKER-20260715"
    assert validation["support_state"] == "provisional_worker_selftest"
    assert validation["proposed_state"] == "[_]"
    assert validation["accepted"] is validation["release_grade"] is False
    assert validation["verdict"] == "blocked"
    assert validation["result"]["exact_root_kernel_replay"] == "provisional_pass"
    assert validation["result"]["accepted_root_machine_debt"] == "M3"
    assert validation["result"]["accepted_root_closed"] is False
    assert validation["result"]["hermetic_release_gate"] == "fail_closed"
    assert validation["result"]["independent_distinct_runner_gate"] == "fail_closed"
    assert validation["result"]["audit_complete"] is False
    assert validation["result"]["theorem_complete"] is False

    assert decision["schema_version"] == "stage1-release-decision/1.0"
    assert decision["item_id"] == ITEM and decision["theorem_id"] == THEOREM
    assert decision["base_revision"] == BASE_REVISION and decision["base_tree"] == BASE_TREE
    assert decision["support_state"] == "provisional_worker_selftest"
    assert decision["proposed_state"] == "[_]" and decision["accepted"] is False
    assert decision["release_grade"] is decision["content_addressed_release_evidence"] is False
    assert decision["verdict"] == "blocked"
    assert decision["lifecycle_before"] == decision["lifecycle_after"] == "planned"
    assert decision["root_vector"]["before"] == decision["root_vector"]["after"] == VECTOR
    assert decision["accepted_receipt_ids"] == []
    assert decision["terminal_decisions"] == {
        "audit_complete": False, "theorem_complete": False,
        "audit_z": "blocked", "theorem_z": "blocked",
        "release_accepted": False, "master_acceptance": False,
    }
    dependency = decision["dependency"]
    assert dependency["item_id"] == validation["item_id"]
    assert dependency["receipt_id"] == validation["receipt_id"]
    assert dependency["receipt_sha256"] == VALIDATION_RECEIPT_SHA256
    assert dependency["worker_projection"] == "[_]"
    assert dependency["master_accepted"] is dependency["receipt_accepted"] is False
    assert dependency["receipt_release_grade"] is False
    assert decision["first_failed_gate"]["gate_id"] == (
        "dependency.S56-M-0072-VALIDATION.master_acceptance"
    )
    assert decision["first_failed_release_gate"]["gate_id"] == (
        "S56-10.6-IMMUTABLE-CLEAN-INPUT"
    )
    assert decision["next_failed_release_gate"]["gate_id"] == (
        "S56-10.6-HERMETIC-COLD-EMPTY-CACHE-REPLAY"
    )
    assert decision["canonical_obligation_ids"] == INVENTORY_IDS
    assert decision["remaining_root_cut_set"] == ["M0072-T-OUTSIDE"]
    for key in (
        "dependency_master_acceptance", "authoritative_graph_reconciled",
        "accepted_root_m0", "accepted_composition_closure", "audit_z_accepted",
        "pinpoint_h0_review", "independent_r0_review",
        "complete_provenance_foundation_tcb_closure", "immutable_clean_release_input",
        "hermetic_cold_offline_replay", "sbom_license_archive_closure",
        "independent_clean_runner_attestations",
        "independently_implemented_minimal_verifier", "protected_ci_and_mutation_gates",
        "deterministic_release_bundle", "master_acceptance",
    ):
        assert decision["evidence_reconciliation"][key] is False, key
    remaining = "\n".join(decision["remaining_release_gate_set"])
    for fragment in (
        "S56-M-0072-VALIDATION", "M0072-T-OUTSIDE", "AUDIT-Z", "H0 primary-source",
        "R0 node-anchored", "empty-cache network-denied cold build", "SBOM and license",
        "two signed attestations", "minimal release verifier",
        "deterministic build-twice content-addressed release bundle",
    ):
        assert fragment in remaining, fragment

    assert spec["schema_version"] == "stage1-release-recipe/1.0"
    assert spec["item_id"] == ITEM and spec["theorem_id"] == THEOREM
    assert spec["argv"] == [
        "/usr/bin/python3", "-I", "-B", f"Stage1_Instances/{THEOREM}/check_release.py"
    ]
    assert spec["network_policy"] == "denied" and spec["expected_exit"] == 0
    assert spec["covered_obligation_ids"] == INVENTORY_IDS
    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["depends_on"] == ["S56-M-0072-VALIDATION"]
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["release_grade"] is receipt["content_addressed_release_evidence"] is False
    assert receipt["verdict"] == "blocked" and receipt["accepted_receipt_ids"] == []
    assert receipt["decision_id"] == decision["decision_id"]
    assert receipt["recipe"] == {
        key: spec[key] for key in (
            "recipe_id", "cwd", "argv", "env_allowlist", "timeout_seconds",
            "network_policy", "network_enforcement", "expected_exit", "expected_outputs",
            "covered_obligation_ids", "covered_declarations",
        )
    }
    assert receipt["result"]["root_vector_before"] == VECTOR
    assert receipt["result"]["root_vector_after"] == VECTOR
    assert receipt["result"]["audit_complete"] is receipt["result"]["theorem_complete"] is False
    assert receipt["result"]["accepted_receipt_ids"] == []
    assert receipt["output_summary"] == SUMMARY_LINES
    assert receipt["known_failures"] == decision["known_failures"]

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by|run_tac|oracle)\b|"
        r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
        r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
        r"(?:axiom|constant|opaque|unsafe|extern)\b",
        re.MULTILINE,
    )
    for name in ("Statement.lean", "ObligationTree.lean", "AnchorAudit.lean", "Proof.lean", "Validation.lean"):
        source = source_without_comments_and_strings((HERE / name).read_text(encoding="utf-8"))
        assert prohibited.search(source) is None, f"prohibited Lean device in {name}"

    manifest = load(LEAN_ROOT / "lake-manifest.json")
    mathlib_entry = next(row for row in manifest["packages"] if row["name"] == "mathlib")
    assert mathlib_entry["rev"] == mathlib_entry["inputRev"] == MATHLIB_REVISION
    assert mathlib_entry["url"] == MATHLIB_REMOTE
    assert (LEAN_ROOT / ".lake").is_symlink() and MATHLIB.resolve().is_dir()
    assert git("rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert git("status", "--porcelain=v1", "--untracked-files=all", cwd=MATHLIB) == ""
    assert git("remote", "get-url", "origin", cwd=MATHLIB) == MATHLIB_REMOTE
    assert sha256(MATHLIB / "LICENSE") == MATHLIB_LICENSE_SHA256

    outputs = narrow_replay()
    proof_output = outputs["proof"]
    validation_output = outputs["validation"]
    declarations = (
        "Stage1Instances.THM_M_0072.Proof.maximal_normal_of_pgroup",
        "Stage1Instances.THM_M_0072.Proof.quotient_isSimpleGroup_of_isCoatom",
        "Stage1Instances.THM_M_0072.Proof.maximal_index_prime_of_pgroup",
        "Stage1Instances.THM_M_0072.Proof.maximal_index_two_of_2group",
        "Stage1Instances.THM_M_0072.Proof.period_eq_one_or_two",
        "Stage1Instances.THM_M_0072.Proof.quotient_eq_of_both_not_mem",
        "Stage1Instances.THM_M_0072.Proof.outsideTransferConclusion",
        "Stage1Instances.THM_M_0072.Proof.thompsonTransferLemma_proof",
    )
    for declaration in declarations:
        assert reported_axioms(proof_output + validation_output, declaration) == ALLOWED_AXIOMS
    for declaration in (
        "Stage1Instances.THM_M_0072.Validation.exactOutsideReplay",
        "Stage1Instances.THM_M_0072.Validation.exactRootReplay",
    ):
        assert reported_axioms(validation_output, declaration) == ALLOWED_AXIOMS
    assert validation_output.count("Declarations are sorry-free!") == 14
    assert "VALIDATION_CLOSURE axioms=[propext, Classical.choice, Quot.sound]" in validation_output
    assert "VALIDATION_CLOSURE bodyless_nonaxioms=[]" in validation_output
    assert "VALIDATION_CLOSURE unsafe=[]" in validation_output
    assert "sorryAx" not in "\n".join(outputs.values())

    assert set(packet) == {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert packet["item_id"] == ITEM and packet["base_revision"] == BASE_REVISION
    assert packet["state"] == "[_]"
    assert set(packet["changed_paths"]) == set(receipt["changed_paths"]) == CHANGED_PATHS
    assert packet["known_failures"] == decision["known_failures"]
    actual = {
        line[3:] for line in git("status", "--short", "--untracked-files=all").splitlines()
        if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual == CHANGED_PATHS, (actual, CHANGED_PATHS)
    for relative in CHANGED_PATHS:
        assert_text_hygiene(ROOT / relative)

    print("\n".join(SUMMARY_LINES))


if __name__ == "__main__":
    main()
