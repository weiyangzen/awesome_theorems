#!/usr/bin/env python3
"""Elaborate, fingerprint, and mutation-test the THM-M-0914 statement."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
from datetime import datetime, timezone


ROOT = Path(__file__).resolve().parents[2]
LEAN_DIR = ROOT / "Formalizations" / "Lean"
SOURCE = Path(__file__).with_name("Statement.lean")
NAMESPACE = "Stage1Instances.THM_M_0914"
THEOREM_ID = "THM-M-0914"
ITEM_ID = "S56-M-0914-STATEMENT"
CANONICAL = "PigeonholeTarget"
DECLARATIONS = (
    CANONICAL,
    "mutationRemovedDistinctness",
    "mutationChangedDomain",
    "mutationChangedBinderScope",
    "mutationExcludesZeroBoxes",
)
TRANSPORTS = ("pigeonholeTarget_iff_boxWitnessTarget",)
BOUNDARIES = ("no_placement_into_zero_boxes", "one_box_boundary")
MUTATION_GUARDS = (
    "#check_failure (show PigeonholeTarget from hRemoved)",
    "#check_failure (show PigeonholeTarget from hDomain)",
    "#check_failure (show PigeonholeTarget from hScope)",
    "#check_failure (show PigeonholeTarget from hBoundary)",
)
DIRECT_IMPORTS: tuple[str, ...] = ()
PRINT_MARKER = "#print PigeonholeTarget"
EXPECTED_EXPRESSION_SHA256 = "faef4a7f73219dc5b6178b8788978e21377c593ad84b845b4d49547218e6ae3b"
EXPECTED_STATEMENT_FILE_SHA256 = "953cf5ba54e27cf08cce5a91880fd79d36f4b5aa7b92228bd27474a1399233db"
EXPECTED_LEAN_OUTPUT_SHA256 = "718818aba6701c758379a3dfc2e1bcbb07b233527aa103636b67328266418b64"


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def load(path: Path) -> dict:
    def reject_duplicate_keys(pairs: list[tuple[str, object]]) -> dict:
        result: dict[str, object] = {}
        for key, value in pairs:
            if key in result:
                raise SystemExit(f"duplicate JSON key in {path}: {key}")
            result[key] = value
        return result

    value = json.loads(
        path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicate_keys
    )
    if not isinstance(value, dict):
        raise SystemExit(f"{path} must contain a JSON object")
    return value


def run_lean(path: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["lake", "env", "lean", str(path)],
        cwd=LEAN_DIR,
        env={**os.environ, "LC_ALL": "C", "TZ": "UTC"},
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )


def run_text(text: str) -> subprocess.CompletedProcess[str]:
    with tempfile.NamedTemporaryFile(
        "w", suffix=".lean", encoding="utf-8", delete=False
    ) as handle:
        handle.write(text)
        temporary = Path(handle.name)
    try:
        return run_lean(temporary)
    finally:
        temporary.unlink()


def elaborate_expression(declaration: str) -> tuple[str, str]:
    text = SOURCE.read_text(encoding="utf-8")
    if text.count(PRINT_MARKER) != 1:
        raise SystemExit("canonical #print marker must occur exactly once")
    text = text.replace(PRINT_MARKER, f"#print {declaration}")
    result = run_text(text)
    if result.returncode:
        print(result.stdout, end="")
        raise SystemExit(result.returncode)
    qualified = re.escape(f"{NAMESPACE}.{declaration}")
    match = re.search(
        rf"def {qualified} : Prop :=\n(?P<expression>.*)\Z", result.stdout, re.DOTALL
    )
    if not match:
        raise SystemExit(f"could not extract explicit expression for {declaration}")
    return match.group("expression").strip(), result.stdout


def main() -> None:
    source_text = SOURCE.read_text(encoding="utf-8")
    actual_imports = tuple(re.findall(r"^import ([^\s]+)$", source_text, re.MULTILINE))
    if actual_imports != DIRECT_IMPORTS:
        raise SystemExit(f"direct imports changed: {actual_imports!r}")

    execution = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")
    item = next(row for row in execution["items"] if row["id"] == ITEM_ID)
    if item["theorem_id"] != THEOREM_ID or item["phase"] != "statement":
        raise SystemExit("authoritative statement item identity changed")
    if item["layer"] != 1 or item["depends_on"] != ["S56-M-0914-INTAKE"]:
        raise SystemExit("authoritative statement dependency changed")
    if item["owned_paths"] != [f"Stage1_Instances/{THEOREM_ID}"]:
        raise SystemExit("authoritative statement ownership changed")

    expressions: dict[str, str] = {}
    canonical_output = ""
    for declaration in DECLARATIONS:
        expression, output = elaborate_expression(declaration)
        expressions[declaration] = expression
        if declaration == CANONICAL:
            canonical_output = output
    canonical = expressions[CANONICAL]
    survivors = [name for name in DECLARATIONS[1:] if expressions[name] == canonical]
    if survivors:
        raise SystemExit(f"statement mutation survived: {', '.join(survivors)}")

    for name in TRANSPORTS + BOUNDARIES:
        if not re.search(rf"^theorem {re.escape(name)}\b", source_text, re.MULTILINE):
            raise SystemExit(f"missing transport or boundary declaration: {name}")
    for guard in MUTATION_GUARDS:
        if source_text.count(guard) != 1:
            raise SystemExit(f"missing or duplicated mutation failure guard: {guard}")
    if source_text.count("#check_failure") != len(MUTATION_GUARDS):
        raise SystemExit("unexpected additional mutation failure guard")

    expression_hash = sha256_bytes(canonical.encode("utf-8"))
    statement_file_hash = sha256_bytes(SOURCE.read_bytes())
    lean_output_hash = sha256_bytes(canonical_output.encode("utf-8"))
    expected = (
        ("expression", expression_hash, EXPECTED_EXPRESSION_SHA256),
        ("statement source", statement_file_hash, EXPECTED_STATEMENT_FILE_SHA256),
        ("Lean output", lean_output_hash, EXPECTED_LEAN_OUTPUT_SHA256),
    )
    for label, actual, wanted in expected:
        if wanted != "TO_BE_RECONCILED" and actual != wanted:
            raise SystemExit(f"{label} changed without reconciliation")

    statement_path = SOURCE.with_name("statement.json")
    receipt_path = SOURCE.with_name("statement-receipt.json")
    if statement_path.exists() and receipt_path.exists():
        statement = load(statement_path)
        receipt = load(receipt_path)
        formal = statement["canonical_formal_target"]
        if formal["elaborated_expression_sha256"] != expression_hash:
            raise SystemExit("structured statement expression fingerprint is stale")
        if formal["statement_file_sha256"] != statement_file_hash:
            raise SystemExit("structured statement source fingerprint is stale")
        if formal["fully_explicit_expression"] != " ".join(canonical.split()):
            raise SystemExit("serialized fully explicit expression is stale")
        if receipt["statement_fingerprints"] != [f"sha256:{expression_hash}"]:
            raise SystemExit("receipt expression fingerprint is stale")
        if receipt["statement_file_sha256"] != statement_file_hash:
            raise SystemExit("receipt statement source fingerprint is stale")
        if receipt["lean_output_sha256"] != lean_output_hash:
            raise SystemExit("receipt Lean-output fingerprint is stale")
        if tuple(receipt["direct_imports"]) != DIRECT_IMPORTS:
            raise SystemExit("receipt direct-import record is stale")
        instance = load(SOURCE.with_name("instance.json"))
        instance_formal = instance["canonical_formal_target"]
        if instance["canonical_statement"] != statement["canonical_statement"]:
            raise SystemExit("instance canonical statement is stale")
        if instance_formal["elaborated_expression_hash"] != f"sha256:{expression_hash}":
            raise SystemExit("instance expression fingerprint is stale")
        if instance_formal["module"] != f"Stage1_Instances/{THEOREM_ID}/Statement.lean":
            raise SystemExit("instance statement module is stale")

        expected_files = {
            "README.md",
            "instance.json",
            "scope-map.md",
            "source-statement-crosswalk.md",
            "task-dag.json",
            "IntakeProbe.lean",
            "check_intake.py",
            "validation.md",
            "intake-receipt.json",
            "Statement.lean",
            "check_statement.py",
            "statement.json",
            "statement-receipt.json",
            "statement-validation.md",
        }
        actual_files = {path.name for path in SOURCE.parent.iterdir() if path.is_file()}
        if actual_files != expected_files or set(instance["owned_artifacts"]) != expected_files:
            raise SystemExit("owned statement artifact inventory changed")
        public = {f"Stage1_Instances/{THEOREM_ID}/{name}" for name in expected_files}
        if set(instance["public_merge_targets"]) != public:
            raise SystemExit("public statement artifact inventory changed")

        dag = load(SOURCE.with_name("task-dag.json"))
        expected_dependency = "S56-M-0914-INTAKE"
        for task in dag["tasks"]:
            authoritative = next(
                row for row in execution["items"] if row["id"] == task["id"]
            )
            for field in (
                "phase",
                "layer",
                "depends_on",
                "owned_paths",
                "deliverable",
                "completion_gate",
            ):
                if task[field] != authoritative[field]:
                    raise SystemExit(f"task DAG disagrees on {task['id']} {field}")
            if task["depends_on"] != [expected_dependency] or task["state"] != "open":
                raise SystemExit(f"task DAG dependency or state changed: {task['id']}")
            expected_dependency = task["id"]
        if dag["accepted_states"] or dag["audit_complete"] or dag["theorem_complete"]:
            raise SystemExit("planned statement DAG cannot contain accepted or terminal state")

        source_inputs = receipt["source_inputs"]
        for relative, tagged_digest in source_inputs.items():
            actual = sha256_bytes((ROOT / relative).read_bytes())
            if tagged_digest != f"sha256:{actual}":
                raise SystemExit(f"stale receipt source input: {relative}")
        if receipt["base_revision"] != "a3b18eec39bf04be025b1641cae02f4d44fdf11a":
            raise SystemExit("statement base revision changed")
        if receipt["base_tree"] != "fdfff18dea4c6798c5b322b6088dfe556109c134":
            raise SystemExit("statement base tree changed")
        if receipt["root_vector_before"] != receipt["root_vector_after"]:
            raise SystemExit("statement phase unexpectedly changes the H1/M3/R4 vector")
        if receipt["root_vector_after"] != instance["root_vector"]:
            raise SystemExit("receipt and instance debt vectors disagree")
        if receipt["accepted"] or receipt["accepted_receipt_ids"]:
            raise SystemExit("worker statement receipt cannot claim accepted state")
        if receipt["audit_complete"] or receipt["theorem_complete"]:
            raise SystemExit("statement receipt cannot claim audit or theorem completion")
        expected_cut = [
            "S56-M-0914-ANCHOR_AUDIT",
            "S56-M-0914-OBLIGATION_TREE",
            "S56-M-0914-PROOF",
            "S56-M-0914-VALIDATION",
            "S56-M-0914-RELEASE",
        ]
        if receipt["remaining_root_cut_set"] != expected_cut:
            raise SystemExit("statement remaining root cut set changed")

        artifacts = receipt["nonrelease_artifact_inputs"]
        excluded = set(artifacts["self_referential_exclusions"])
        expected_hashed = expected_files - excluded
        if set(artifacts["artifact_sha256"]) != expected_hashed:
            raise SystemExit("nonrelease artifact hash inventory changed")
        for name, digest in artifacts["artifact_sha256"].items():
            if digest != sha256_bytes((SOURCE.parent / name).read_bytes()):
                raise SystemExit(f"stale nonrelease artifact hash: {name}")
        packet_hash = sha256_bytes((ROOT / ".stage1-worker-selftest.json").read_bytes())
        if artifacts["worker_packet_sha256"] != packet_hash:
            raise SystemExit("worker packet fingerprint changed")
        patch = subprocess.check_output(
            ["git", "diff", "--binary", "--", f"Stage1_Instances/{THEOREM_ID}"],
            cwd=ROOT,
        )
        if artifacts["tracked_patch_sha256"] != sha256_bytes(patch):
            raise SystemExit("tracked owned-path patch fingerprint changed")
        lake_target = (ROOT / "Formalizations/Lean/.lake").readlink().as_posix().encode()
        if artifacts["lake_symlink_target_sha256"] != sha256_bytes(lake_target):
            raise SystemExit("automation .lake symlink target fingerprint changed")
        for key in ("owner", "attestor", "platform", "validation_started_at",
                    "validation_ended_at", "validated_at", "review_due",
                    "invalidation_inputs", "support_state", "supersession_state",
                    "revocation_state", "incident_path"):
            if not receipt.get(key):
                raise SystemExit(f"receipt evidence field missing: {key}")
        started = datetime.fromisoformat(receipt["validation_started_at"])
        ended = datetime.fromisoformat(receipt["validation_ended_at"])
        if not started <= ended <= datetime.now(timezone.utc).astimezone():
            raise SystemExit("receipt validation interval is invalid")
        if receipt["validated_at"] != receipt["validation_ended_at"]:
            raise SystemExit("receipt validated_at disagrees with validation end")
        for recipe in receipt["structured_validation_recipes"]:
            required_recipe_fields = {
                "recipe_id",
                "cwd",
                "argv",
                "env_allowlist",
                "timeout_seconds",
                "network_policy",
                "expected_exit",
                "exit_code",
                "expected_outputs",
                "covered_obligation_ids",
                "covered_declarations",
            }
            if set(recipe) != required_recipe_fields:
                raise SystemExit(f"structured recipe fields changed: {recipe.get('recipe_id')}")
            if recipe["expected_exit"] != recipe["exit_code"] or recipe["exit_code"] != 0:
                raise SystemExit(f"structured recipe did not pass: {recipe['recipe_id']}")
            if recipe["network_policy"] != "denied" or not recipe["expected_outputs"]:
                raise SystemExit(f"structured recipe boundary changed: {recipe['recipe_id']}")

        init_prefix = subprocess.check_output(
            ["lake", "env", "lean", "--print-prefix"], cwd=LEAN_DIR, text=True
        ).strip()
        init_source = Path(init_prefix) / "src/lean/Init.lean"
        init_olean = Path(init_prefix) / "lib/lean/Init.olean"
        inputs = receipt["worker_input_hashes"]
        if inputs["lean_init_source"] != f"sha256:{sha256_bytes(init_source.read_bytes())}":
            raise SystemExit("pinned Lean Init source fingerprint changed")
        if inputs["lean_init_olean"] != f"sha256:{sha256_bytes(init_olean.read_bytes())}":
            raise SystemExit("pinned Lean Init object fingerprint changed")

        prohibited = re.compile(
            r"\b(?:sorry|admit|sorryAx)\b|^\s*(?:axiom|constant|opaque)\s+|"
            r"^\s*unsafe\b|\b(?:TODO|FIXME)\b",
            re.MULTILINE,
        )
        if prohibited.search(source_text):
            raise SystemExit("prohibited declaration or placeholder marker in statement source")

    manifest = load(LEAN_DIR / "lake-manifest.json")
    mathlib_revision = next(
        package["rev"]
        for package in manifest["packages"]
        if package["name"] == "mathlib"
    )
    payload = {
        "direct_imports": list(DIRECT_IMPORTS),
        "expression_sha256": expression_hash,
        "killed_mutations": list(DECLARATIONS[1:]),
        "lean_output_sha256": lean_output_hash,
        "mathlib_revision": mathlib_revision,
        "statement_file_sha256": statement_file_hash,
        "toolchain": (LEAN_DIR / "lean-toolchain").read_text(encoding="utf-8").strip(),
        "transports": list(TRANSPORTS),
        "validated_boundaries": list(BOUNDARIES),
    }

    packet_args = sys.argv[1:]
    if packet_args:
        if packet_args[:1] != ["--worker-packet"] or len(packet_args) != 2:
            raise SystemExit("usage: check_statement.py [--worker-packet PATH]")
        packet_path = Path(packet_args[1])
        if not packet_path.is_absolute():
            packet_path = Path.cwd() / packet_path
        packet = load(packet_path.resolve())
        expected_packet_fields = {
            "item_id",
            "changed_paths",
            "commands",
            "output_summary",
            "base_revision",
            "known_failures",
            "state",
        }
        if set(packet) != expected_packet_fields:
            raise SystemExit("worker packet fields changed")
        if packet["item_id"] != ITEM_ID or packet["state"] != "[_]":
            raise SystemExit("worker packet item or proposed state changed")
        if packet["base_revision"] != receipt["base_revision"]:
            raise SystemExit("worker packet base revision changed")
        if set(packet["changed_paths"]) != set(receipt["changed_paths"]):
            raise SystemExit("worker packet changed-path inventory disagrees with receipt")
        if packet["known_failures"] != receipt["known_failures"]:
            raise SystemExit("worker packet known failures disagree with receipt")
        if not packet["commands"] or not packet["output_summary"]:
            raise SystemExit("worker packet command or output summary is empty")
        checker_argv = [
            "python3",
            "-B",
            "../../Stage1_Instances/THM-M-0914/check_statement.py",
            "--worker-packet",
            "../../.stage1-worker-selftest.json",
        ]
        if not any(
            command.get("cwd") == "Formalizations/Lean"
            and command.get("argv") == checker_argv
            and command.get("exit_code") == 0
            for command in packet["commands"]
        ):
            raise SystemExit("worker packet lacks the exact successful packet-aware checker command")
    print(json.dumps(payload, sort_keys=True))


if __name__ == "__main__":
    main()
