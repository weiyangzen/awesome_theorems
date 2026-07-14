#!/usr/bin/env python3
"""Fail-closed release reconciliation for S56-M-1227-RELEASE."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys


if not __debug__:
    raise SystemExit("check_release.py must run without Python optimization")


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-1227"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"

ITEM = "S56-M-1227-RELEASE"
THEOREM = "THM-M-1227"
BASE_REVISION = "ed9193169ea1291e0e28619c37c2594f6452edc6"
BASE_TREE = "483c7046328bfa48de64682332a46c3c1aded582"
EXPRESSION_SHA256 = "9c937d18171ee1e302da926183a828ff4f60033685be1f71f5578c46bccd185b"
DENOMINATOR_SHA256 = "ace8d258d4f8205d28cccaf6f5a7d49b26ec069b08dbe407660bd46d7cc63dff"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
LEAN_TOOLCHAIN_SHA256 = "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2"
LAKE_MANIFEST_SHA256 = "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81"
LEAN_EXECUTABLE_SHA256 = "3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf"
LAKE_EXECUTABLE_SHA256 = "840179e70803ef373c2ec53342d6a45ea7d022533e4145489fc1278b4f716385"
PYTHON_EXECUTABLE_SHA256 = "b8d8288faefdd300201f43fcf00f6f539a27218eeed3a3dff5ab10b9c4c99700"
GIT_EXECUTABLE_SHA256 = "8a48eefa306b9a2a9c3e576784a74ad7485779279e5a46ec43361a1864760e45"
VECTOR = {"H": "H2", "M": "M4", "R": "R4"}
CUT = [
    "M1227-N-DATA",
    "M1227-N-GLOBAL",
    "M1227-C-GALERKIN",
    "M1227-C-BOUNDS",
    "M1227-C-COMPACT",
]
SUMMARY_LINES = (
    "PASS S56-M-1227-RELEASE negative reconciliation",
    "fresh Lean replay: B-ZERO candidate sorry-free; exact general root absent",
    "verdict=blocked lifecycle=planned root_vector=H2/M4/R4",
    "AUDIT-Z=false THEOREM-Z=false theorem_complete=false accepted_receipts=0",
    "first_failed_gate=dependency.S56-M-1227-VALIDATION.master_acceptance",
    "first_failed_theorem_gate=proof.M1227-N-DATA.kernel_closure",
    "first_failed_release_gate=S56-10.6-HERMETIC-COLD-BUILD",
)
EVIDENCE_INPUTS = {
    "Statement.lean": "ee8e2db1ef14b921333b55bb8e821d0c17fabdd0d295597205f932abecf4059b",
    "Proof.lean": "f6f03cbf4cc61927cea5a175c7afa1fbc314a27d423598a75f1b228a7f16cabb",
    "Validation.lean": "8199394074782dfb56abc75ea8e6520555ffc4622b3452b1820aa532c742018b",
    "instance.json": "42701e3ea938ead3abfd0f8f4f65d30c4211bab1ca36a6295d8dfc199255a58c",
    "task-dag.json": "237b51f2770ac0475264e5fdc1d27a0c412cef54c15965a5c41d677cb61c0ee3",
    "obligation-registry.json": "e34f878ce8d28069c162520557363410819832382c05f86879c9d629400dda31",
    "typed-graphs.json": "ed22b83ad7493b8505eb05cc9303cafc95db5a5d1ab7c11c44cf1d4d9837f232",
    "proof-receipt.json": "63910c5b76bde8135dabf8ed8090603ce7453be3b8766fcda6598b8d6d4b08e7",
    "proof-blocker.json": "e51e6902b594b1fd7aa90d78852b94bcd17fa27ebe32f49f46c27a7a5881f419",
    "validation-receipt.json": "6da841b690d67e67fc5a976dcfaf73c77b0a4b35fb4f3d24c5328b8c93a7c030",
    "validation-spec.json": "f0031d7b77dce5b4f99a14cc49a044750bf6d0f86a22c186ad993f06fe00e4b6",
    "check_validation.py": "089267c9e8e7b332729e8a3a3517814bc20ed7208117d045870416ba03a75071",
    "scope-map.md": "a7b08c0072409dd00285e357e87b90194d3ec706191e419463e422ef92340f29",
    "source-statement-crosswalk.md": "220ef3f7050df62ff11b5b76d9fcdcbfafa486b486580d80bb8003720e56e11b",
    "statement.md": "8cb06eddabf40058da5f8f463c6599138108d8cdb564087c0eb50432c2ba9d13",
}
AUTHORITY_INPUTS = {
    "Docs/Stage1_Targets_rev-5.6.json": "02eec284de534dd78e1cf75f82a477ff477567dd682b7445cb7587abd137ab2c",
    "Docs/Stage1_Execution_DAG_rev-5.6.json": "47593ddea3a3adf041cae11f40e184e58397e9f478e55ad564d8d4a4f8cf93c9",
}


def fail(message: str) -> None:
    raise SystemExit(f"release-decision: FAIL: {message}")


def load(path: Path) -> dict:
    def no_duplicates(pairs: list[tuple[str, object]]) -> dict:
        value: dict[str, object] = {}
        for key, item in pairs:
            if key in value:
                fail(f"duplicate JSON key in {path}: {key}")
            value[key] = item
        return value

    try:
        value = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=no_duplicates)
    except (OSError, json.JSONDecodeError) as error:
        fail(f"cannot load {path}: {error}")
    if not isinstance(value, dict):
        fail(f"{path} is not a JSON object")
    return value


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(argv: list[str], *, cwd: Path = ROOT, timeout: int = 600) -> str:
    try:
        completed = subprocess.run(
            argv,
            cwd=cwd,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired as error:
        fail(f"command timed out: {argv!r}\n{error.stdout or ''}")
    if completed.returncode:
        fail(f"command failed ({completed.returncode}): {argv!r}\n{completed.stdout}")
    return completed.stdout


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["git", *args], cwd=cwd, timeout=60).strip()


def assert_hygiene(path: Path) -> None:
    data = path.read_bytes()
    if not data.endswith(b"\n") or b"\r" in data or b"\x00" in data:
        fail(f"file hygiene failed: {path}")
    if any(line.endswith((b" ", b"\t")) for line in data.splitlines()):
        fail(f"trailing whitespace: {path}")


def main() -> None:
    spec = load(HERE / "release-spec.json")
    decision = load(HERE / "release-decision.json")
    receipt = load(HERE / "release-receipt.json")
    instance = load(HERE / "instance.json")
    local_dag = load(HERE / "task-dag.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    proof = load(HERE / "proof-receipt.json")
    blocker = load(HERE / "proof-blocker.json")
    validation = load(HERE / "validation-receipt.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")
    targets = load(ROOT / "Docs" / "Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")

    if git("rev-parse", "HEAD") != BASE_REVISION:
        fail("repository base revision drifted")
    if git("rev-parse", "HEAD^{tree}") != BASE_TREE:
        fail("repository base tree drifted")

    for name, expected in EVIDENCE_INPUTS.items():
        if digest(HERE / name) != expected:
            fail(f"stale evidence input: {name}")
    for name, expected in AUTHORITY_INPUTS.items():
        if digest(ROOT / name) != expected:
            fail(f"stale authority input: {name}")

    target = next((row for row in targets["targets"] if row["theorem_id"] == THEOREM), None)
    if target is None:
        fail("target is absent from manifest")
    target_boundary = {
        "execution_rank": 416,
        "legacy_priority_slot": None,
        "theorem_id": THEOREM,
        "baseline": "L0",
        "rework_required": True,
        "legacy_artifacts_accepted": False,
        "target_lane": "hard_mathlib_anchor_and_wrapper",
        "intake_score": 142,
        "lifecycle_mode": "planned",
        "theorem_complete": False,
    }
    if any(target.get(key) != expected for key, expected in target_boundary.items()):
        fail("target manifest entry drifted")

    release_item = next((row for row in execution["items"] if row["id"] == ITEM), None)
    validation_item = next(
        (row for row in execution["items"] if row["id"] == "S56-M-1227-VALIDATION"), None
    )
    expected_release = {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 416,
        "phase": "release",
        "layer": 6,
        "state": "[ ]",
        "depends_on": ["S56-M-1227-VALIDATION"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Reconcile evidence and decide the exact theorem-completion verdict.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }
    if release_item != expected_release:
        fail("release execution item drifted")
    if validation_item is None or validation_item["state"] != "[_]":
        fail("validation worker projection drifted")

    local_release = next((row for row in local_dag["tasks"] if row["id"] == ITEM), None)
    local_validation = next(
        (row for row in local_dag["tasks"] if row["id"] == "S56-M-1227-VALIDATION"), None
    )
    if local_release is None or local_release["state"] != "open":
        fail("local release authority no longer records an open item")
    if local_validation is None or local_validation["state"] != "open":
        fail("local validation authority no longer records an open item")
    if local_dag["accepted_states"]:
        fail("local task authority unexpectedly contains accepted state")

    if instance["lifecycle"] != "planned" or instance["root_vector"] != VECTOR:
        fail("instance lifecycle or root vector drifted")
    if instance["accepted_proof_state"]:
        fail("instance unexpectedly contains accepted proof state")
    if instance["audit_complete"] is not False or instance["theorem_complete"] is not False:
        fail("instance unexpectedly claims terminal completion")
    if registry["root_obligation_id"] != "M1227-ROOT":
        fail("registry root drifted")
    if registry["denominator_sha256"] != DENOMINATOR_SHA256:
        fail("registry denominator drifted")

    closure = graphs["closure_boundary"]
    if closure["closed_obligations"] or closure["root_closed"] is not False:
        fail("authoritative graph unexpectedly contains root closure")
    if closure["root_machine_debt"] != "M4" or closure["remaining_root_cut_set"] != CUT:
        fail("authoritative graph vector or cut set drifted")
    if closure["audit_complete"] is not False or closure["theorem_complete"] is not False:
        fail("authoritative graph unexpectedly claims terminal completion")

    if proof["support_state"] != "provisional_worker_selftest" or proof["accepted"] is not False:
        fail("proof support classification drifted")
    if proof["accepted_closed_obligation_ids"] != []:
        fail("proof receipt unexpectedly accepts an obligation")
    if proof["provisionally_implemented_obligation_ids"] != ["M1227-B-ZERO"]:
        fail("proof receipt scope drifted")
    if proof["result"]["root_closed"] is not False:
        fail("proof receipt unexpectedly closes the root")
    if blocker["remaining_root_cut_set"] != CUT or blocker["theorem_complete"] is not False:
        fail("proof blocker drifted")

    if validation["receipt_id"] != decision["dependency"]["receipt_id"]:
        fail("release decision references the wrong validation receipt")
    if digest(HERE / "validation-receipt.json") != decision["dependency"]["receipt_sha256"]:
        fail("validation dependency hash drifted")
    if validation["accepted"] is not False or validation["release_grade"] is not False:
        fail("validation was falsely represented as accepted or release grade")
    if validation["result"]["root_kernel_closed"] is not False:
        fail("validation unexpectedly reports root closure")
    if validation["result"]["audit_complete"] is not False:
        fail("validation unexpectedly reports audit completion")
    if validation["result"]["theorem_complete"] is not False:
        fail("validation unexpectedly reports theorem completion")
    if validation["base_revision"] == BASE_REVISION:
        fail("historical validation receipt unexpectedly claims current base")

    validation_checker = (HERE / "check_validation.py").read_text(encoding="utf-8")
    if f'BASE_REVISION = "{validation["base_revision"]}"' not in validation_checker:
        fail("historical validation base is not explicit in its checker")
    if 'packet = load(ROOT / ".stage1-worker-selftest.json")' not in validation_checker:
        fail("historical validation packet dependency is no longer explicit")

    if spec["schema_version"] != "stage1-validation-spec/1.0":
        fail("release specification schema drifted")
    if spec["item_id"] != ITEM or spec["theorem_id"] != THEOREM:
        fail("release specification identity drifted")
    if spec["argv"] != ["python3", "-I", "-B", f"Stage1_Instances/{THEOREM}/check_release.py"]:
        fail("release recipe argv drifted")
    if spec["network_policy"] != "denied" or spec["expected_exit"] != 0:
        fail("release recipe policy drifted")
    if spec["kernel_replayed_obligation_ids"] != ["M1227-B-ZERO"]:
        fail("kernel replay obligation scope drifted")
    if spec["kernel_replayed_declarations"] != [
        "Stage1.THM_M_1227.zero_isLerayHopfSolution",
        "Stage1.THM_M_1227.lerayHopfExistence_of_eq_zero",
    ]:
        fail("kernel replay declaration scope drifted")

    if decision["schema_version"] != "stage1-release-decision/1.0":
        fail("release decision schema drifted")
    if decision["item_id"] != ITEM or decision["theorem_id"] != THEOREM:
        fail("release decision identity drifted")
    if decision["base_revision"] != BASE_REVISION or decision["base_tree"] != BASE_TREE:
        fail("release decision base drifted")
    if decision["support_state"] != "provisional_worker_selftest":
        fail("release decision support classification drifted")
    if decision["release_grade"] is not False or decision["verdict"] != "blocked":
        fail("release decision overclaims release")
    if decision["lifecycle_before"] != "planned" or decision["lifecycle_after"] != "planned":
        fail("release decision lifecycle drifted")
    if decision["root_vector_before"] != VECTOR or decision["root_vector_after"] != VECTOR:
        fail("release decision vector drifted")
    if decision["accepted_receipt_ids"]:
        fail("release decision unexpectedly accepts a receipt")
    if decision["audit_complete"] is not False or decision["theorem_complete"] is not False:
        fail("release decision unexpectedly claims terminal completion")
    if decision["release_accepted"] is not False:
        fail("release decision unexpectedly accepts release")
    if decision["first_failed_gate"]["gate_id"] != (
        "dependency.S56-M-1227-VALIDATION.master_acceptance"
    ):
        fail("first release-node gate drifted")
    if decision["first_failed_theorem_gate"]["gate_id"] != (
        "proof.M1227-N-DATA.kernel_closure"
    ):
        fail("first theorem gate drifted")
    if decision["first_failed_release_gate"]["gate_id"] != (
        "S56-10.6-HERMETIC-COLD-BUILD"
    ):
        fail("first release-specific gate drifted")
    if decision["authoritative_graph_remaining_root_cut_set"] != CUT:
        fail("release decision cut set drifted")
    for name, expected in decision["reconciled_inputs"].items():
        if digest(HERE / name) != expected:
            fail(f"decision input drifted: {name}")
    for name, expected in decision["authority_inputs"].items():
        if digest(ROOT / name) != expected:
            fail(f"decision authority input drifted: {name}")

    if receipt["schema_version"] != "stage1-node-receipt/1.0":
        fail("release receipt schema drifted")
    if receipt["item_id"] != ITEM or receipt["theorem_id"] != THEOREM:
        fail("release receipt identity drifted")
    if receipt["base_revision"] != BASE_REVISION or receipt["base_tree"] != BASE_TREE:
        fail("release receipt base drifted")
    if receipt["decision_id"] != decision["decision_id"]:
        fail("release receipt identifies the wrong decision")
    if receipt["support_state"] != "provisional_worker_selftest":
        fail("release receipt support classification drifted")
    if receipt["proposed_state"] != "[_]" or receipt["accepted"] is not False:
        fail("release receipt accepted state drifted")
    if receipt["release_grade"] is not False:
        fail("release receipt falsely claims release grade")
    if receipt["content_addressed_release_evidence"] is not False:
        fail("release receipt falsely claims a release bundle")
    if receipt["master_acceptance"] != "pending_and_not_claimed":
        fail("release receipt falsely claims master acceptance")
    if receipt["canonical_target_expression_sha256"] != EXPRESSION_SHA256:
        fail("release receipt target fingerprint drifted")
    if receipt["registry_denominator_sha256"] != DENOMINATOR_SHA256:
        fail("release receipt denominator drifted")
    if receipt["authority_inputs"] != {
        **AUTHORITY_INPUTS,
        "task-dag.json": EVIDENCE_INPUTS["task-dag.json"],
    }:
        fail("release receipt authority hashes drifted")
    release_artifact_paths = {
        "release-spec.json": HERE / "release-spec.json",
        "release-decision.json": HERE / "release-decision.json",
        "release-validation.md": HERE / "release-validation.md",
        ".stage1-worker-selftest.json": ROOT / ".stage1-worker-selftest.json",
    }
    for name, path in release_artifact_paths.items():
        if receipt["release_artifact_inputs"].get(name) != digest(path):
            fail(f"release artifact hash drifted: {name}")
    if receipt["evidence_inputs"] != {
        name: expected for name, expected in EVIDENCE_INPUTS.items() if name != "task-dag.json"
    }:
        fail("release receipt evidence hashes drifted")
    receipt_recipe = receipt["recipe"]
    for key in (
        "recipe_id",
        "cwd",
        "argv",
        "env_allowlist",
        "timeout_seconds",
        "network_policy",
        "network_enforcement",
        "expected_exit",
        "expected_outputs",
        "covered_obligation_ids",
        "covered_declarations",
        "kernel_replayed_obligation_ids",
        "kernel_replayed_declarations",
        "scope_boundary",
    ):
        if receipt_recipe.get(key) != spec.get(key):
            fail(f"release receipt recipe drifted: {key}")
    result = receipt["result"]
    if result["verdict"] != "blocked" or result["exact_root_kernel_closed"] is not False:
        fail("release receipt result overclaims root closure")
    if result["audit_complete"] is not False or result["theorem_complete"] is not False:
        fail("release receipt result overclaims terminal completion")
    if result["release_accepted"] is not False or result["accepted_receipt_ids"]:
        fail("release receipt result overclaims acceptance")
    if result["root_vector_before"] != VECTOR or result["root_vector_after"] != VECTOR:
        fail("release receipt result vector drifted")
    semantic_output = ("\n".join(SUMMARY_LINES) + "\n").encode("utf-8")
    if result["semantic_output_sha256"] != hashlib.sha256(semantic_output).hexdigest():
        fail("release receipt semantic output hash drifted")
    if result["semantic_output_bytes"] != len(semantic_output):
        fail("release receipt semantic output size drifted")
    if result["fresh_zero_branch_kernel_replay"] != "pass":
        fail("release receipt does not record the scoped Lean replay pass")
    if set(result["observed_axioms"]) != {"propext", "Classical.choice", "Quot.sound"}:
        fail("release receipt axiom observation drifted")
    if receipt["remaining_root_cut_set"] != CUT:
        fail("release receipt cut set drifted")

    environment = receipt["environment"]
    if digest(LEAN_ROOT / "lean-toolchain") != LEAN_TOOLCHAIN_SHA256:
        fail("Lean toolchain file drifted")
    if digest(LEAN_ROOT / "lake-manifest.json") != LAKE_MANIFEST_SHA256:
        fail("Lake manifest drifted")
    lean = Path(run(["lake", "env", "which", "lean"], cwd=LEAN_ROOT, timeout=60).strip())
    lake = Path(shutil.which("lake") or "").resolve()
    python = Path(sys.executable).resolve()
    git_executable = Path(shutil.which("git") or "").resolve()
    executable_hashes = {
        "lean_executable_sha256": (lean, LEAN_EXECUTABLE_SHA256),
        "lake_executable_sha256": (lake, LAKE_EXECUTABLE_SHA256),
        "python_executable_sha256": (python, PYTHON_EXECUTABLE_SHA256),
        "git_executable_sha256": (git_executable, GIT_EXECUTABLE_SHA256),
    }
    for field, (path, expected) in executable_hashes.items():
        if not path.is_file() or digest(path) != expected or environment.get(field) != expected:
            fail(f"release environment executable drifted: {field}")
    if environment.get("lean_toolchain_sha256") != LEAN_TOOLCHAIN_SHA256:
        fail("release receipt Lean toolchain hash drifted")
    if environment.get("lake_manifest_sha256") != LAKE_MANIFEST_SHA256:
        fail("release receipt Lake manifest hash drifted")

    if git("rev-parse", "HEAD", cwd=MATHLIB) != MATHLIB_REVISION:
        fail("mathlib revision drifted")
    if git("rev-parse", "HEAD^{tree}", cwd=MATHLIB) != MATHLIB_TREE:
        fail("mathlib tree drifted")
    if git("status", "--porcelain=v1", cwd=MATHLIB):
        fail("mathlib worktree is dirty")

    replay = run(["bash", str(HERE / "check_proof.sh")], timeout=600)
    if "PASS THM-M-1227 isolated Lean replay: zero-data branch checked" not in replay:
        fail("fresh zero-data replay did not report its scoped pass")
    if replay.count("Declarations are sorry-free!") != 2:
        fail("fresh zero-data replay did not report both declarations sorry-free")
    for axiom in ("propext", "Classical.choice", "Quot.sound"):
        if axiom not in replay:
            fail(f"fresh zero-data replay omitted axiom report: {axiom}")

    changed_paths = {
        ".stage1-worker-selftest.json",
        f"Stage1_Instances/{THEOREM}/check_release.py",
        f"Stage1_Instances/{THEOREM}/release-decision.json",
        f"Stage1_Instances/{THEOREM}/release-receipt.json",
        f"Stage1_Instances/{THEOREM}/release-spec.json",
        f"Stage1_Instances/{THEOREM}/release-validation.md",
    }
    required_packet_keys = {
        "item_id",
        "changed_paths",
        "commands",
        "output_summary",
        "base_revision",
        "known_failures",
        "state",
    }
    if set(packet) != required_packet_keys:
        fail("worker self-test schema drifted")
    if packet["item_id"] != ITEM or packet["state"] != "[_]":
        fail("worker self-test identity or state drifted")
    if packet["base_revision"] != BASE_REVISION:
        fail("worker self-test base drifted")
    if set(packet["changed_paths"]) != changed_paths:
        fail("worker self-test changed paths drifted")
    if not packet["known_failures"]:
        fail("worker self-test omits known failures")
    release_commands = [
        row for row in packet["commands"]
        if row.get("argv") == [
            "python3", "-I", "-B", f"Stage1_Instances/{THEOREM}/check_release.py"
        ]
    ]
    if not release_commands or any(row.get("exit_code") != 0 for row in release_commands):
        fail("worker self-test omits a passing release recipe")
    if release_commands[0].get("env") != spec["env_allowlist"]:
        fail("worker self-test release environment drifted")
    checker_binding = f"check_release.py_sha256={digest(HERE / 'check_release.py')}"
    if checker_binding not in release_commands[0].get("output_summary", ""):
        fail("worker self-test does not bind the current release checker")

    status = git("status", "--short", "--untracked-files=all")
    actual_changes = {
        line[3:]
        for line in status.splitlines()
        if line[3:] != "Formalizations/Lean/.lake"
    }
    if actual_changes != changed_paths:
        fail(f"unexpected worker changes: {sorted(actual_changes ^ changed_paths)}")

    for path in [ROOT / name for name in changed_paths]:
        assert_hygiene(path)

    for line in SUMMARY_LINES:
        print(line)


if __name__ == "__main__":
    main()
