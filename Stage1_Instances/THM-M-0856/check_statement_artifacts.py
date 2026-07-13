#!/usr/bin/env python3
"""Cross-check the THM-M-0856 statement packet against fresh elaboration."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
LEAN_DIR = ROOT / "Formalizations" / "Lean"
THEOREM_ID = "THM-M-0856"
ITEM_ID = "S56-M-0856-STATEMENT"
BASE_REVISION = "748243faadc15828fb087059337fd05b7be9fdeb"
BASE_TREE = "e46d642646f80980838b6f016f5d69b817bd464d"
EXPRESSION_SHA256 = "5364250d1d4e132aaf1d5ce8ad5425369546963189991202f49b2fcf65095bae"
SOURCE_SHA256 = "cd7ec3e97a02ccc24578de4431a1a8ebf0e9572f9616b271b67f145d72fbedce"
LEAN_OUTPUT_SHA256 = "7f4494f834dd6a0f7edd67a666bdcf84d644d6b5ae3b878f6a398baa7b6f1c3b"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
DIRECT_IMPORT = "Mathlib.Combinatorics.SimpleGraph.Matching"
TOOLCHAIN = "leanprover/lean4:v4.29.0"
MUTATION_HASHES = {
    "mutationRemovedFiniteness": "976cab38432cdf447df48f35bbf0b5e5fde105d925e7bfb347549d852ec0b0a8",
    "mutationChangedDomainToCompleteGraphs": "a0a2e0f19d614356bad365e46c5062672a826ff1d5a638842e1b4fee769aa406",
    "mutationChangedGraphBinderScope": "4d2497193db3a1fff65a6366e0f0a8bb399b6c50ba46a9b7fa0cfbfc7cae8327",
    "mutationExcludedEmptyCarrier": "e705851921b23616ced405887d87f12ab2c5c58393a34a1379a1fd4cb76e47fa",
}
TRANSPORTS = [
    "tutteOneFactorTarget_iff_expanded",
    "tutteOneFactorTarget_iff_noTutteViolatorTarget",
]
CHANGED_PATHS = [
    ".stage1-worker-selftest.json",
    "Stage1_Instances/THM-M-0856/README.md",
    "Stage1_Instances/THM-M-0856/Statement.lean",
    "Stage1_Instances/THM-M-0856/check_statement.py",
    "Stage1_Instances/THM-M-0856/check_statement_artifacts.py",
    "Stage1_Instances/THM-M-0856/instance.json",
    "Stage1_Instances/THM-M-0856/scope-map.md",
    "Stage1_Instances/THM-M-0856/source-statement-crosswalk.md",
    "Stage1_Instances/THM-M-0856/statement-receipt.json",
    "Stage1_Instances/THM-M-0856/statement-validation.md",
    "Stage1_Instances/THM-M-0856/statement.json",
    "Stage1_Instances/THM-M-0856/task-dag.json",
]
STATEMENT_FILES = {
    "Statement.lean",
    "check_statement.py",
    "check_statement_artifacts.py",
    "statement-receipt.json",
    "statement-validation.md",
    "statement.json",
}
SOURCE_INPUTS = (
    "Docs/Stage1_Targets_rev-5.6.json",
    "Docs/Stage1_Blueprint_rev-5.6.md",
    "Docs/Stage1_Execution_DAG_rev-5.6.json",
    "skills/execute-stage1-rev56/SKILL.md",
    "Docs/Blueprint_Guidelines.md",
    "Docs/researches/math_theorems.md",
    "Docs/Stage0_Blueprint.md",
    "Formalizations/Lean/lean-toolchain",
    "Formalizations/Lean/lake-manifest.json",
    "Formalizations/Lean/.lake/packages/mathlib/Mathlib/Combinatorics/SimpleGraph/Matching.lean",
    "Stage1_Instances/THM-M-0856/instance.json",
    "Stage1_Instances/THM-M-0856/intake-receipt.json",
    "Stage1_Instances/THM-M-0856/task-dag.json",
    "Stage1_Instances/THM-M-0856/README.md",
    "Stage1_Instances/THM-M-0856/scope-map.md",
    "Stage1_Instances/THM-M-0856/source-statement-crosswalk.md",
)


def load(path: Path) -> dict:
    def reject_duplicates(pairs: list[tuple[str, object]]) -> dict:
        result: dict[str, object] = {}
        for key, value in pairs:
            if key in result:
                raise SystemExit(f"duplicate JSON key in {path}: {key}")
            result[key] = value
        return result

    value = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicates)
    if not isinstance(value, dict):
        raise SystemExit(f"{path} must contain a JSON object")
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(
        ["git", *args], cwd=cwd, text=True, stderr=subprocess.DEVNULL
    ).strip()


def changed_paths() -> list[str]:
    """Return destination paths from Git's NUL-delimited porcelain output."""
    status = subprocess.run(
        ["git", "status", "--porcelain=v1", "-z", "--untracked-files=all"],
        cwd=ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
    ).stdout
    entries = status.split(b"\0")
    paths: list[str] = []
    index = 0
    while index < len(entries):
        entry = entries[index]
        index += 1
        if not entry:
            continue
        if len(entry) < 4 or entry[2:3] != b" ":
            raise SystemExit("could not parse root worktree status")
        code = entry[:2]
        raw_path = entry[3:]
        if b"R" in code or b"C" in code:
            if index >= len(entries) or not entries[index]:
                raise SystemExit("could not parse rename/copy source path")
            # With `-z`, the destination is in this entry and the source follows it.
            index += 1
        paths.append(raw_path.decode("utf-8", errors="surrogateescape"))
    return sorted(paths)


def check_packet(path: Path, receipt: dict) -> None:
    packet = load(path.resolve())
    if set(packet) != {
        "item_id",
        "changed_paths",
        "commands",
        "output_summary",
        "base_revision",
        "known_failures",
        "state",
    }:
        raise SystemExit("worker packet must contain exactly the seven authorized keys")
    if packet["item_id"] != ITEM_ID or packet["state"] != "[_]":
        raise SystemExit("worker packet identity/state mismatch")
    if packet["base_revision"] != BASE_REVISION:
        raise SystemExit("worker packet base mismatch")
    if packet["changed_paths"] != CHANGED_PATHS:
        raise SystemExit("worker packet changed_paths mismatch")
    if packet["commands"] != receipt["commands_and_results"]:
        raise SystemExit("worker packet commands mismatch")
    if packet["known_failures"] != receipt["known_failures"]:
        raise SystemExit("worker packet known_failures mismatch")
    if not isinstance(packet["output_summary"], str) or not packet["output_summary"]:
        raise SystemExit("worker packet output_summary is missing")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker-packet", type=Path)
    args = parser.parse_args()

    statement = load(HERE / "statement.json")
    receipt = load(HERE / "statement-receipt.json")
    instance = load(HERE / "instance.json")
    local_dag = load(HERE / "task-dag.json")
    expected_statement_keys = {
        "schema_version": "stage1-statement/1.0",
        "normative_profile": "machine-theorem-assurance/1.0",
        "item_id": ITEM_ID,
        "theorem_id": THEOREM_ID,
        "execution_rank": 1410,
        "lifecycle_mode": "planned",
        "lifecycle": "planned",
        "formal_system": "Lean 4 + pinned mathlib under the rev-5.6 adapter",
        "statement_elaborated": True,
        "theorem_proved": False,
        "audit_complete": False,
        "theorem_complete": False,
    }
    for key, expected in expected_statement_keys.items():
        if statement.get(key) != expected:
            raise SystemExit(f"statement metadata mismatch: {key}")
    if sha256(HERE / "Statement.lean") != SOURCE_SHA256:
        raise SystemExit("Statement.lean hash is stale")

    formal = statement["canonical_formal_target"]
    if instance["item_id"] != ITEM_ID or instance["intent"] != "statement":
        raise SystemExit("instance manifest is not reconciled to the statement node")
    instance_formal = instance["canonical_formal_target"]
    if instance_formal["module"] != formal["module"]:
        raise SystemExit("instance statement module is stale")
    if instance_formal["declaration_or_expression"] != formal["declaration_or_expression"]:
        raise SystemExit("instance canonical declaration is stale")
    if instance_formal["elaborated_expression_hash"] != f"sha256:{EXPRESSION_SHA256}":
        raise SystemExit("instance expression fingerprint is stale")
    if instance["statement_blocker"] is not None:
        raise SystemExit("instance retains a resolved statement blocker")
    instance_revisions = instance["source_revisions"]
    for relative, key in (
        ("Docs/Stage1_Blueprint_rev-5.6.md", "authoritative_blueprint_sha256"),
        ("Docs/Stage1_Execution_DAG_rev-5.6.json", "execution_dag_sha256"),
    ):
        if instance_revisions[key] != sha256(ROOT / relative):
            raise SystemExit(f"instance source revision is stale: {relative}")
    if instance["support_window"] != (
        "provisional statement proposal only; expires on any invalidation input "
        "and cannot support release"
    ):
        raise SystemExit("instance support window is stale")
    if instance["review_due"] != (
        "at dependency-ordered master integration and on every invalidation input change"
    ):
        raise SystemExit("instance review boundary is stale")
    if instance["root_vector"] != {"H": "H1", "M": "M3", "R": "R4"}:
        raise SystemExit("instance debt vector changed")
    local_statement_task = next(row for row in local_dag["tasks"] if row["id"] == ITEM_ID)
    if local_statement_task["state"] != "open":
        raise SystemExit("worker cannot accept the local statement task")
    if local_statement_task["worker_receipt"] != (
        "Stage1_Instances/THM-M-0856/statement-receipt.json"
    ):
        raise SystemExit("local statement task is not linked to its worker receipt")
    if formal["elaborated_expression_sha256"] != EXPRESSION_SHA256:
        raise SystemExit("statement expression hash is stale")
    if formal["statement_file_sha256"] != SOURCE_SHA256:
        raise SystemExit("statement source hash is stale")
    if hashlib.sha256(formal["fully_explicit_expression"].encode()).hexdigest() != EXPRESSION_SHA256:
        raise SystemExit("preserved explicit expression disagrees with its fingerprint")
    if receipt["statement_fingerprints"] != [f"sha256:{EXPRESSION_SHA256}"]:
        raise SystemExit("receipt expression hash is stale")
    if receipt["statement_file_sha256"] != SOURCE_SHA256:
        raise SystemExit("receipt source hash is stale")
    if receipt["lean_output_sha256"] != LEAN_OUTPUT_SHA256:
        raise SystemExit("receipt Lean output hash is stale")
    if formal["declaration_or_expression"] != "Stage1Instances.THM_M_0856.TutteOneFactorTarget":
        raise SystemExit("canonical declaration changed")
    if statement["direct_imports"] != [DIRECT_IMPORT]:
        raise SystemExit("statement direct-import metadata changed")
    if [row["checked_witness"].removeprefix("Stage1Instances.THM_M_0856.")
            for row in statement["alternate_encodings"]] != TRANSPORTS:
        raise SystemExit("statement transport metadata changed")

    if receipt["item_id"] != ITEM_ID or receipt["theorem_id"] != THEOREM_ID:
        raise SystemExit("receipt identity mismatch")
    if receipt["phase"] != receipt["intent"] or receipt["phase"] != "statement":
        raise SystemExit("receipt phase mismatch")
    if receipt["environment"]["platform"] != "Linux 7.0.0-27-generic x86_64":
        raise SystemExit("receipt platform changed")
    if receipt["base_revision"] != BASE_REVISION or receipt["base_tree"] != BASE_TREE:
        raise SystemExit("receipt base mismatch")
    if receipt["changed_paths"] != CHANGED_PATHS:
        raise SystemExit("receipt changed_paths mismatch")
    actual_changed_paths = changed_paths()
    preexisting_untracked = receipt["preexisting_untracked_paths"]
    if preexisting_untracked != ["Formalizations/Lean/.lake"]:
        raise SystemExit("pre-existing untracked-path classification changed")
    if actual_changed_paths != sorted([*CHANGED_PATHS, *preexisting_untracked]):
        raise SystemExit(f"root worktree delta mismatch: {actual_changed_paths}")
    if receipt["proposed_state"] != "[_]" or receipt["accepted"]:
        raise SystemExit("receipt must remain provisional")
    if statement["theorem_proved"] or statement["theorem_complete"]:
        raise SystemExit("statement metadata claims proof completion")
    if receipt["audit_complete"] or receipt["theorem_complete"]:
        raise SystemExit("receipt claims a terminal decision")
    if statement["root_vector_after"] != {"H": "H1", "M": "M3", "R": "R4"}:
        raise SystemExit("statement debt vector changed")
    if receipt["accepted_receipt_ids"] or receipt["proof_body_locations"]:
        raise SystemExit("statement receipt claims accepted or proof-body evidence")
    if receipt["remaining_root_cut_set"] != [
        "S56-M-0856-ANCHOR_AUDIT",
        "S56-M-0856-OBLIGATION_TREE",
        "S56-M-0856-PROOF",
        "S56-M-0856-VALIDATION",
        "S56-M-0856-RELEASE",
    ]:
        raise SystemExit("statement receipt remaining cut set is stale")
    expected_validators = {
        "Stage1_Instances/THM-M-0856/check_statement.py": sha256(HERE / "check_statement.py"),
        "Stage1_Instances/THM-M-0856/check_statement_artifacts.py": sha256(
            HERE / "check_statement_artifacts.py"
        ),
    }
    if receipt["validator_sha256"] != expected_validators:
        raise SystemExit("receipt validator hash is stale")
    if receipt["mutation_expression_sha256"] != MUTATION_HASHES:
        raise SystemExit("receipt mutation fingerprints changed")
    if not receipt["prior_intake_receipt_status"].startswith(
        "historical provisional receipt invalidated for current replay"
    ):
        raise SystemExit("prior intake receipt invalidation is not classified")
    if not receipt["prior_intake_projection_status"].startswith(
        "validation.md and check_intake.py remain immutable historical"
    ):
        raise SystemExit("historical intake projections are not classified")
    if receipt["attestor"] != "Stage1 rev-5.6 isolated worker self-test; unsigned and not independent":
        raise SystemExit("receipt attestor changed")
    if receipt["owner"] != "Stage1 integration lane":
        raise SystemExit("receipt owner changed")
    if not receipt["supersession_state"].startswith("current provisional statement worker receipt"):
        raise SystemExit("receipt supersession state is missing")
    if not receipt["revocation_state"].startswith("not revoked"):
        raise SystemExit("receipt revocation state is missing")
    if set(receipt["validation_window"]) != {"start", "end"}:
        raise SystemExit("receipt validation window is malformed")
    actual_statement_files = {
        path.name for path in HERE.iterdir()
        if path.is_file() and (
            path.name == "Statement.lean"
            or path.name.startswith("check_statement")
            or path.name.startswith("statement-")
            or path.name == "statement.json"
        )
    }
    if actual_statement_files != STATEMENT_FILES:
        raise SystemExit(
            f"unexpected statement artifact inventory: {sorted(actual_statement_files)}"
        )

    authority = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    item = next(row for row in authority["items"] if row["id"] == ITEM_ID)
    if item["theorem_id"] != THEOREM_ID or item["phase"] != "statement":
        raise SystemExit("authoritative statement identity changed")
    if item["layer"] != 1 or item["depends_on"] != ["S56-M-0856-INTAKE"]:
        raise SystemExit("authoritative statement dependency changed")
    if item["owned_paths"] != ["Stage1_Instances/THM-M-0856"]:
        raise SystemExit("authoritative statement ownership changed")

    for relative in SOURCE_INPUTS:
        expected = f"sha256:{sha256(ROOT / relative)}"
        if receipt["source_inputs"][relative] != expected:
            raise SystemExit(f"receipt source hash is stale: {relative}")
    if git("rev-parse", "HEAD") != BASE_REVISION or git("rev-parse", "HEAD^{tree}") != BASE_TREE:
        raise SystemExit("worker base revision changed")
    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    if git("rev-parse", "HEAD", cwd=mathlib) != MATHLIB_REVISION:
        raise SystemExit("mathlib revision changed")
    if git("rev-parse", "HEAD^{tree}", cwd=mathlib) != MATHLIB_TREE:
        raise SystemExit("mathlib tree changed")
    if git("status", "--short", cwd=mathlib):
        raise SystemExit("pinned mathlib worktree is dirty")

    result = subprocess.run(
        ["python3", "-B", str(HERE / "check_statement.py")],
        cwd=LEAN_DIR,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=180,
        check=False,
    )
    if result.returncode:
        sys.stdout.write(result.stdout)
        raise SystemExit(result.returncode)
    payload = json.loads(result.stdout)
    if payload["elaborated_expression_sha256"] != EXPRESSION_SHA256:
        raise SystemExit("fresh elaborated expression disagrees with metadata")
    if payload["statement_file_sha256"] != SOURCE_SHA256:
        raise SystemExit("fresh statement source disagrees with metadata")
    if payload["lean_output_sha256"] != LEAN_OUTPUT_SHA256:
        raise SystemExit("fresh Lean output disagrees with receipt")
    if payload["minimal_import_deletion_exit"] == 0:
        raise SystemExit("minimal import deletion unexpectedly passed")
    if payload["direct_import"] != DIRECT_IMPORT or payload["toolchain"] != TOOLCHAIN:
        raise SystemExit("fresh import/toolchain payload disagrees with metadata")
    if payload["killed_mutations"] != list(MUTATION_HASHES):
        raise SystemExit("fresh mutation inventory disagrees with metadata")
    if payload["mutation_expression_sha256"] != MUTATION_HASHES:
        raise SystemExit("fresh mutation fingerprints disagree with receipt")
    if payload["transports"] != TRANSPORTS:
        raise SystemExit("fresh transport inventory disagrees with metadata")

    for path in HERE.iterdir():
        if not path.is_file():
            continue
        data = path.read_bytes()
        if not data.endswith(b"\n") or b"\r" in data or b"\x00" in data:
            raise SystemExit(f"invalid file encoding/ending: {path.name}")
        if any(line.endswith((b" ", b"\t")) for line in data.splitlines()):
            raise SystemExit(f"trailing whitespace: {path.name}")
    for name in (
        "README.md",
        "scope-map.md",
        "source-statement-crosswalk.md",
        "statement.json",
        "statement-receipt.json",
        "statement-validation.md",
    ):
        text = (HERE / name).read_text(encoding="utf-8")
        if "/home/" in text or ".cron/" in text:
            raise SystemExit(f"private absolute/runtime path leaked into {name}")

    if args.worker_packet is not None:
        check_packet(args.worker_packet, receipt)
    print("statement artifact check: ok (THM-M-0856; provisional; theorem_complete false)")


if __name__ == "__main__":
    main()
