#!/usr/bin/env python3
"""Validate the exact THM-M-0822 statement and structural mutations."""

from pathlib import Path
import argparse
import hashlib
import json
import re
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[2]
LEAN_DIR = ROOT / "Formalizations" / "Lean"
SOURCE = Path(__file__).with_name("Statement.lean")
NAMESPACE = "Stage1Instances.THM_M_0822"
CANONICAL = "ErdosKoRadoMaximumTarget"
MUTATIONS = [
    "mutationRemovedIntersectingHypothesis",
    "mutationChangedSubsetDomain",
    "mutationChangedFamilyBinderScope",
    "mutationExcludesEqualityBoundary",
]
DIRECT_IMPORTS = [
    "Mathlib.Combinatorics.SetFamily.Intersecting",
    "Mathlib.Data.Finset.Slice",
]
STATEMENT_RECORD = SOURCE.with_name("statement.json")
RECEIPT = SOURCE.with_name("statement-receipt.json")
ITEM_ID = "S56-M-0822-STATEMENT"
THEOREM_ID = "THM-M-0822"
BASE_REVISION = "46a0f2a3ea74765a0467c489264b838ffbb70675"
BASE_TREE = "7b1b5269d7da840fd086da731d6f92903c209c35"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    "Stage1_Instances/THM-M-0822/README.md",
    "Stage1_Instances/THM-M-0822/Statement.lean",
    "Stage1_Instances/THM-M-0822/check_statement.py",
    "Stage1_Instances/THM-M-0822/instance.json",
    "Stage1_Instances/THM-M-0822/scope-map.md",
    "Stage1_Instances/THM-M-0822/source-statement-crosswalk.md",
    "Stage1_Instances/THM-M-0822/statement-receipt.json",
    "Stage1_Instances/THM-M-0822/statement-validation.md",
    "Stage1_Instances/THM-M-0822/statement.json",
    "Stage1_Instances/THM-M-0822/task-dag.json",
}
SOURCE_INPUTS = {
    "Docs/Stage1_Targets_rev-5.6.json": "Docs/Stage1_Targets_rev-5.6.json",
    "Docs/Stage1_Blueprint_rev-5.6.md": "Docs/Stage1_Blueprint_rev-5.6.md",
    "Docs/Stage1_Execution_DAG_rev-5.6.json":
        "Docs/Stage1_Execution_DAG_rev-5.6.json",
    "skills/execute-stage1-rev56/SKILL.md":
        "skills/execute-stage1-rev56/SKILL.md",
    "Docs/Blueprint_Guidelines.md": "Docs/Blueprint_Guidelines.md",
    "Docs/researches/math_theorems.md": "Docs/researches/math_theorems.md",
    "Docs/Stage0_Blueprint.md": "Docs/Stage0_Blueprint.md",
    "Formalizations/Lean/lean-toolchain": "Formalizations/Lean/lean-toolchain",
    "Formalizations/Lean/lakefile.lean": "Formalizations/Lean/lakefile.lean",
    "Formalizations/Lean/lake-manifest.json": "Formalizations/Lean/lake-manifest.json",
}
OWNED_INPUTS = {
    "Stage1_Instances/THM-M-0822/instance.json":
        "Stage1_Instances/THM-M-0822/instance.json",
    "Stage1_Instances/THM-M-0822/intake-receipt.json":
        "Stage1_Instances/THM-M-0822/intake-receipt.json",
    "Stage1_Instances/THM-M-0822/source-statement-crosswalk.md":
        "Stage1_Instances/THM-M-0822/source-statement-crosswalk.md",
    "Stage1_Instances/THM-M-0822/scope-map.md":
        "Stage1_Instances/THM-M-0822/scope-map.md",
    "Stage1_Instances/THM-M-0822/task-dag.json":
        "Stage1_Instances/THM-M-0822/task-dag.json",
}
IMPORT_SOURCES = {
    "Mathlib.Combinatorics.SetFamily.Intersecting":
        "Mathlib/Combinatorics/SetFamily/Intersecting.lean",
    "Mathlib.Data.Finset.Slice": "Mathlib/Data/Finset/Slice.lean",
}
RUN_ENV = {
    "HOME": "/home/sansha-2",
    "LANG": "C.UTF-8",
    "PATH": "/home/sansha-2/.elan/bin:/usr/bin:/bin",
}
SANDBOX_PREFIX = [
    "bwrap", "--unshare-net", "--bind", "/", "/", "--dev-bind", "/dev", "/dev",
    "--proc", "/proc", "--", "env", "-i",
    "HOME=/home/sansha-2", "LANG=C.UTF-8",
    "PATH=/home/sansha-2/.elan/bin:/usr/bin:/bin",
]


def run_lean(source: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["lake", "env", "lean", str(source)],
        cwd=LEAN_DIR,
        env=RUN_ENV,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=120,
    )


def elaborate(source: Path) -> str:
    result = run_lean(source)
    if result.returncode:
        sys.stdout.write(result.stdout)
        raise SystemExit(result.returncode)
    return result.stdout


def expression(declaration: str) -> tuple[str, str]:
    source_text = SOURCE.read_text(encoding="utf-8")
    marker = f"#print {NAMESPACE}.{CANONICAL}"
    if source_text.count(marker) != 1:
        raise SystemExit("canonical #print marker is missing or ambiguous")
    source_text = source_text.replace(marker, f"#print {NAMESPACE}.{declaration}")
    with tempfile.NamedTemporaryFile(
        "w", suffix=".lean", dir=SOURCE.parent, delete=False, encoding="utf-8"
    ) as handle:
        handle.write(source_text)
        temporary = Path(handle.name)
    try:
        output = elaborate(temporary)
    finally:
        temporary.unlink()
    match = re.search(r" : Prop :=\n(?P<expression>.*)\Z", output, re.DOTALL)
    if not match:
        raise SystemExit(f"could not serialize {declaration}")
    serialized = match.group("expression").strip()
    if "?m." in serialized:
        raise SystemExit(f"unresolved metavariable in {declaration}")
    return serialized, output


def target_fixture(source_text: str) -> str:
    start_marker = "/-- The exact maximum-value form selected from the repository gloss."
    end_marker = "/-- The star of all `r`-subsets of `Fin n` containing `x`. -/"
    if source_text.count(start_marker) != 1 or source_text.count(end_marker) != 1:
        raise SystemExit("canonical target fixture marker is missing or ambiguous")
    prefix_end = source_text.index(start_marker)
    body_end = source_text.index(end_marker)
    return (
        source_text[:prefix_end]
        + source_text[prefix_end:body_end]
        + "\nend Stage1Instances.THM_M_0822\n"
    )


def run_temporary(text: str) -> subprocess.CompletedProcess[str]:
    with tempfile.NamedTemporaryFile(
        "w", suffix=".lean", dir=SOURCE.parent, delete=False, encoding="utf-8"
    ) as handle:
        handle.write(text)
        temporary = Path(handle.name)
    try:
        return run_lean(temporary)
    finally:
        temporary.unlink()


def check_minimal_imports(source_text: str) -> dict[str, dict[str, str | int]]:
    actual_imports = [
        line.removeprefix("import ")
        for line in source_text.splitlines()
        if line.startswith("import ")
    ]
    if actual_imports != DIRECT_IMPORTS:
        raise SystemExit(f"unexpected direct imports: {actual_imports}")

    fixture = target_fixture(source_text)
    baseline = run_temporary(fixture)
    if baseline.returncode:
        sys.stdout.write(baseline.stdout)
        raise SystemExit("canonical target fixture does not elaborate")

    failures = {}
    for module in DIRECT_IMPORTS:
        candidate = fixture.replace(f"import {module}\n", "", 1)
        result = run_temporary(candidate)
        if result.returncode == 0:
            raise SystemExit(f"direct import is redundant in target fixture: {module}")
        failures[module] = {
            "exit_code": result.returncode,
            "failure_class": "canonical target fixture does not elaborate",
        }
    return failures


def check_forbidden_constructs(source_text: str) -> None:
    without_comments = re.sub(r"/-.*?-/", "", source_text, flags=re.DOTALL)
    without_comments = re.sub(r"--.*", "", without_comments)
    match = re.search(
        r"\b(?:sorry|admit|sorryAx|axiom|constant|opaque|unsafe)\b",
        without_comments,
    )
    if match:
        raise SystemExit(f"forbidden Lean construct: {match.group(0)}")


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise SystemExit(f"{path} must contain a JSON object")
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(["git", *args], cwd=cwd, text=True).strip()


def check_text_file(path: Path) -> None:
    data = path.read_bytes()
    if not data.endswith(b"\n"):
        raise SystemExit(f"missing final newline: {path}")
    if b"\r" in data or b"\x00" in data:
        raise SystemExit(f"invalid byte in {path}")
    if any(line.endswith((b" ", b"\t")) for line in data.splitlines()):
        raise SystemExit(f"trailing whitespace in {path}")


def changed_path_snapshot() -> tuple[dict[str, str], str]:
    """Hash the dirty packet without making the receipt hash itself recursive."""
    hashes = {
        relative: sha256(ROOT / relative)
        for relative in sorted(CHANGED_PATHS)
        if relative != "Stage1_Instances/THM-M-0822/statement-receipt.json"
    }
    records = "".join(f"{digest}  {relative}\n" for relative, digest in hashes.items())
    return hashes, hashlib.sha256(records.encode()).hexdigest()


def check_artifacts(payload: dict, worker_packet: Path | None) -> None:
    statement = load(STATEMENT_RECORD)
    receipt = load(RECEIPT)
    instance = load(SOURCE.with_name("instance.json"))
    local_dag = load(SOURCE.with_name("task-dag.json"))
    intake_receipt = load(SOURCE.with_name("intake-receipt.json"))
    target_manifest = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")

    target = next(
        row for row in target_manifest["targets"]
        if row["theorem_id"] == THEOREM_ID
    )
    item = next(row for row in execution["items"] if row["id"] == ITEM_ID)
    if target["execution_rank"] != statement["execution_rank"] or target["execution_rank"] != 1380:
        raise SystemExit("target execution rank mismatch")
    if target["name"] != "Erdős-Ko-Rado定理" or target["baseline"] != "L0":
        raise SystemExit("target manifest identity mismatch")
    if not target["rework_required"] or target["theorem_complete"]:
        raise SystemExit("target manifest lifecycle mismatch")
    if item["theorem_id"] != THEOREM_ID or item["phase"] != "statement":
        raise SystemExit("statement DAG identity mismatch")
    if item["state"] != "[ ]" or item["depends_on"] != ["S56-M-0822-INTAKE"]:
        raise SystemExit("statement DAG dependency/state mismatch")
    if item["owned_paths"] != ["Stage1_Instances/THM-M-0822"]:
        raise SystemExit("statement ownership mismatch")
    if item["deliverable"] != "Elaborate the exact Lean 4 target with the minimal pinned imports.":
        raise SystemExit("statement deliverable mismatch")

    formal = statement["canonical_formal_target"]
    if statement["item_id"] != receipt["item_id"] or statement["item_id"] != ITEM_ID:
        raise SystemExit("item id mismatch")
    if statement["theorem_id"] != receipt["theorem_id"] or statement["theorem_id"] != THEOREM_ID:
        raise SystemExit("theorem id mismatch")
    if formal["declaration_or_expression"] != f"{NAMESPACE}.{CANONICAL}":
        raise SystemExit("canonical declaration mismatch")
    if formal["elaborated_expression_sha256"] != payload["elaborated_expression_sha256"]:
        raise SystemExit("statement expression hash mismatch")
    if formal["statement_file_sha256"] != payload["statement_file_sha256"]:
        raise SystemExit("statement source hash mismatch")
    if formal["environment_fingerprint_sha256"] != payload["environment_fingerprint_sha256"]:
        raise SystemExit("statement environment fingerprint mismatch")
    if statement["direct_imports"] != payload["direct_imports"]:
        raise SystemExit("statement import mismatch")
    if statement["root_vector_before"] != statement["root_vector_after"]:
        raise SystemExit("unexpected statement debt transition")
    if statement["root_vector_after"] != {"H": "H1", "M": "M3", "R": "R4"}:
        raise SystemExit("incorrect statement debt vector")
    if not statement["statement_elaborated"]:
        raise SystemExit("statement not marked elaborated")
    if statement["theorem_proved"] or statement["audit_complete"] or statement["theorem_complete"]:
        raise SystemExit("statement record overclaims closure")
    if statement["accepted_receipt_ids"]:
        raise SystemExit("statement record claims accepted receipt")

    canonical_claim = statement["canonical_statement"]
    if instance["canonical_statement"] != canonical_claim:
        raise SystemExit("instance/statement human claim mismatch")
    instance_formal = instance["canonical_formal_target"]
    if instance_formal["declaration_or_expression"] != f"{NAMESPACE}.{CANONICAL}":
        raise SystemExit("instance canonical declaration mismatch")
    if instance_formal["elaborated_expression_hash"] != (
        f"sha256:{payload['elaborated_expression_sha256']}"
    ):
        raise SystemExit("instance expression hash mismatch")
    if instance_formal["environment_fingerprint"] != (
        f"sha256:{payload['environment_fingerprint_sha256']}"
    ):
        raise SystemExit("instance environment fingerprint mismatch")
    if instance["statement_blocker"] is not None:
        raise SystemExit("instance retains a resolved statement blocker")
    revisions = instance["source_revisions"]
    if revisions["authoritative_blueprint_sha256"] != sha256(
        ROOT / "Docs/Stage1_Blueprint_rev-5.6.md"
    ):
        raise SystemExit("instance blueprint hash mismatch")
    if revisions["execution_dag_sha256"] != sha256(
        ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json"
    ):
        raise SystemExit("instance execution DAG hash mismatch")
    if instance["root_vector"] != {"H": "H1", "M": "M3", "R": "R4"}:
        raise SystemExit("instance debt vector mismatch")
    if instance["audit_complete"] or instance["theorem_complete"]:
        raise SystemExit("instance overclaims closure")
    expected_owned = {path.name for path in SOURCE.parent.iterdir() if path.is_file()}
    if set(instance["owned_artifacts"]) != expected_owned:
        raise SystemExit("instance owned-artifact inventory mismatch")
    if set(instance["public_merge_targets"]) != {
        f"Stage1_Instances/THM-M-0822/{name}" for name in expected_owned
    }:
        raise SystemExit("instance public merge-target inventory mismatch")

    statement_task = next(
        task for task in local_dag["tasks"] if task["id"] == ITEM_ID
    )
    expected_blocker = (
        "dependency-ordered master acceptance of the provisional intake and this "
        "self-tested standard positive uniform maximum-value statement proposal; "
        "independent source H0 review remains open"
    )
    if statement_task["state"] != "open" or statement_task["first_blocker"] != expected_blocker:
        raise SystemExit("local statement task boundary mismatch")
    if local_dag["accepted_states"] or local_dag["audit_complete"] or local_dag["theorem_complete"]:
        raise SystemExit("local task DAG overclaims state")
    if intake_receipt["support_state"] != "provisional_worker_only":
        raise SystemExit("historical intake receipt was rewritten")
    if intake_receipt["supersession_state"] != "current_unsuperseded_worker_report":
        raise SystemExit("historical intake receipt supersession field was rewritten")

    if receipt["proposed_state"] != "[_]" or receipt["accepted"]:
        raise SystemExit("receipt authority/state mismatch")
    if receipt["verdict"] != "no_state_change" or receipt["content_addressed"]:
        raise SystemExit("receipt boundary mismatch")
    if receipt["base_revision"] != BASE_REVISION or receipt["base_tree"] != BASE_TREE:
        raise SystemExit("receipt base mismatch")
    if git("rev-parse", "HEAD") != BASE_REVISION or git("rev-parse", "HEAD^{tree}") != BASE_TREE:
        raise SystemExit("worker HEAD moved from recorded base")
    if set(receipt["changed_paths"]) != CHANGED_PATHS:
        raise SystemExit("receipt changed-path mismatch")
    if receipt["statement_fingerprints"] != [
        f"sha256:{payload['elaborated_expression_sha256']}"
    ]:
        raise SystemExit("receipt statement fingerprint mismatch")
    if receipt["statement_file_sha256"] != payload["statement_file_sha256"]:
        raise SystemExit("receipt statement file hash mismatch")
    if receipt["checker_sha256"] != sha256(Path(__file__)):
        raise SystemExit("receipt checker hash mismatch")
    snapshot_hashes, snapshot_digest = changed_path_snapshot()
    if receipt["changed_path_sha256_excluding_receipt"] != {
        path: f"sha256:{digest}" for path, digest in snapshot_hashes.items()
    }:
        raise SystemExit("receipt dirty-path hash mismatch")
    if receipt["changed_path_snapshot_sha256_excluding_receipt"] != (
        f"sha256:{snapshot_digest}"
    ):
        raise SystemExit("receipt dirty snapshot hash mismatch")
    if receipt["lean_output_sha256"] != payload["lean_output_sha256"]:
        raise SystemExit("receipt Lean output hash mismatch")
    if receipt["direct_imports"] != DIRECT_IMPORTS:
        raise SystemExit("receipt import mismatch")
    if receipt["root_vector_before"] != receipt["root_vector_after"]:
        raise SystemExit("receipt debt transition mismatch")
    if receipt["root_vector_after"] != {"H": "H1", "M": "M3", "R": "R4"}:
        raise SystemExit("receipt debt vector mismatch")
    if receipt["accepted_receipt_ids"] or receipt["proof_body_locations"]:
        raise SystemExit("receipt claims proof or acceptance")
    if receipt["audit_complete"] or receipt["theorem_complete"]:
        raise SystemExit("receipt overclaims closure")
    if receipt["selftest_result"] != "pass":
        raise SystemExit("receipt self-test is not final")
    if not receipt["commands_and_results"]:
        raise SystemExit("receipt has no command evidence")
    if receipt["validated_at"] != "2026-07-13T22:13:17+08:00":
        raise SystemExit("receipt validation timestamp mismatch")
    if receipt["worker_input_hashes"]["lean_toolchain"] != (
        f"sha256:{sha256(LEAN_DIR / 'lean-toolchain')}"
    ):
        raise SystemExit("receipt toolchain hash mismatch")
    if receipt["worker_input_hashes"]["lakefile"] != (
        f"sha256:{sha256(LEAN_DIR / 'lakefile.lean')}"
    ):
        raise SystemExit("receipt lakefile hash mismatch")
    if receipt["worker_input_hashes"]["lake_manifest"] != (
        f"sha256:{sha256(LEAN_DIR / 'lake-manifest.json')}"
    ):
        raise SystemExit("receipt dependency-lock hash mismatch")
    lake_target_hash = hashlib.sha256(
        (LEAN_DIR / ".lake").readlink().as_posix().encode()
    ).hexdigest()
    if receipt["worker_input_hashes"]["lake_symlink_target_string"] != (
        f"sha256:{lake_target_hash}"
    ):
        raise SystemExit("receipt lake symlink target mismatch")
    expected_cut_set = [
        "S56-M-0822-INTAKE",
        "S56-M-0822-STATEMENT",
        "S56-M-0822-ANCHOR_AUDIT",
        "S56-M-0822-OBLIGATION_TREE",
        "S56-M-0822-PROOF",
        "S56-M-0822-VALIDATION",
        "S56-M-0822-RELEASE",
    ]
    if receipt["remaining_root_cut_set"] != expected_cut_set:
        raise SystemExit("receipt root cut set omits an unfinished dependency")
    for unfinished_token in ("PEND" + "ING", "PLACE" + "HOLDER", "TO_" + "COMPUTE"):
        if (
            unfinished_token in json.dumps(receipt)
            or unfinished_token in json.dumps(statement)
            or unfinished_token in json.dumps(instance)
        ):
            raise SystemExit("unfinished marker in finalized statement artifacts")

    for key, relative in SOURCE_INPUTS.items():
        expected = f"sha256:{sha256(ROOT / relative)}"
        if receipt["source_inputs"].get(key) != expected:
            raise SystemExit(f"stale receipt source hash: {key}")
    for key, relative in OWNED_INPUTS.items():
        expected = f"sha256:{sha256(ROOT / relative)}"
        if receipt["source_inputs"].get(key) != expected:
            raise SystemExit(f"stale owned intake input hash: {key}")

    mathlib = LEAN_DIR / ".lake/packages/mathlib"
    if git("rev-parse", "HEAD", cwd=mathlib) != MATHLIB_REVISION:
        raise SystemExit("mathlib revision mismatch")
    if git("rev-parse", "HEAD^{tree}", cwd=mathlib) != MATHLIB_TREE:
        raise SystemExit("mathlib tree mismatch")
    if git("status", "--short", cwd=mathlib):
        raise SystemExit("mathlib worktree is dirty")
    for module, relative in IMPORT_SOURCES.items():
        expected = f"sha256:{sha256(mathlib / relative)}"
        if receipt["worker_input_hashes"].get(module) != expected:
            raise SystemExit(f"direct import source hash mismatch: {module}")

    recipes = receipt["structured_validation_recipes"]
    if len(recipes) != 2:
        raise SystemExit("unexpected statement recipe count")
    for recipe in recipes:
        if not isinstance(recipe["argv"], list) or not recipe["argv"]:
            raise SystemExit("invalid recipe argv")
        if recipe["env_allowlist"] != receipt["run_environment"] or recipe["network_policy"] != "denied":
            raise SystemExit("recipe environment/network policy mismatch")
        if recipe["expected_exit"] != 0 or not recipe["covered_declarations"]:
            raise SystemExit("recipe exit or declaration coverage mismatch")
    if recipes[0]["argv"] != SANDBOX_PREFIX + [
        "lake", "env", "lean", "../../Stage1_Instances/THM-M-0822/Statement.lean"
    ]:
        raise SystemExit("Lean recipe mismatch")
    if recipes[1]["argv"] != SANDBOX_PREFIX + [
        "python3", "-B", "../../Stage1_Instances/THM-M-0822/check_statement.py",
        "--worker-packet", "../../.stage1-worker-selftest.json",
    ]:
        raise SystemExit("checker recipe mismatch")

    for relative in CHANGED_PATHS - {".stage1-worker-selftest.json"}:
        check_text_file(ROOT / relative)

    actual_status = {
        line
        for line in subprocess.check_output(
            ["git", "status", "--porcelain=v1", "--untracked-files=all"],
            cwd=ROOT,
            text=True,
        ).splitlines()
        if not re.fullmatch(
            r"\?\? Stage1_Instances/THM-M-0822/tmp[a-zA-Z0-9_]+\.lean", line
        )
    }
    expected_status = {"?? Formalizations/Lean/.lake"} | {
        f"?? {relative}"
        for relative in CHANGED_PATHS
        if relative == ".stage1-worker-selftest.json"
        or not (ROOT / relative).exists()
    }
    expected_status |= {
        f" M {relative}"
        for relative in CHANGED_PATHS
        if relative != ".stage1-worker-selftest.json"
        and (ROOT / relative).exists()
        and relative in git("ls-files", "--", relative).splitlines()
    }
    expected_status |= {
        f"?? {relative}"
        for relative in CHANGED_PATHS
        if relative != ".stage1-worker-selftest.json"
        and (ROOT / relative).exists()
        and relative not in git("ls-files", "--", relative).splitlines()
    }
    if actual_status != expected_status:
        raise SystemExit(f"unexpected worker status: {sorted(actual_status)}")

    if worker_packet is not None:
        packet = load(worker_packet)
        if set(packet) != {
            "item_id", "changed_paths", "commands", "output_summary",
            "base_revision", "known_failures", "state",
        }:
            raise SystemExit("worker packet schema mismatch")
        if packet["item_id"] != ITEM_ID or packet["state"] != "[_]":
            raise SystemExit("worker packet state mismatch")
        if packet["base_revision"] != BASE_REVISION:
            raise SystemExit("worker packet base mismatch")
        if set(packet["changed_paths"]) != CHANGED_PATHS:
            raise SystemExit("worker packet changed-path mismatch")
        if packet["known_failures"] != receipt["known_failures"]:
            raise SystemExit("worker packet failure ledger mismatch")
        if not packet["commands"] or not packet["output_summary"]:
            raise SystemExit("worker packet evidence missing")
        check_text_file(worker_packet)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker-packet", type=Path)
    parser.add_argument("--compute-only", action="store_true")
    args = parser.parse_args()

    source_text = SOURCE.read_text(encoding="utf-8")
    check_forbidden_constructs(source_text)
    import_failures = check_minimal_imports(source_text)

    serialized = {}
    outputs = {}
    for declaration in [CANONICAL, *MUTATIONS]:
        serialized[declaration], outputs[declaration] = expression(declaration)
    canonical = serialized[CANONICAL]
    survivors = [name for name in MUTATIONS if serialized[name] == canonical]
    if survivors:
        raise SystemExit(f"statement mutation survived: {', '.join(survivors)}")

    manifest = json.loads((LEAN_DIR / "lake-manifest.json").read_text(encoding="utf-8"))
    mathlib_revision = next(
        package["rev"]
        for package in manifest["packages"]
        if package["name"] == "mathlib"
    )
    payload = {
        "direct_imports": DIRECT_IMPORTS,
        "elaborated_expression_sha256": hashlib.sha256(canonical.encode()).hexdigest(),
        "killed_mutations": MUTATIONS,
        "lean_output_sha256": hashlib.sha256(outputs[CANONICAL].encode()).hexdigest(),
        "mathlib_revision": mathlib_revision,
        "minimal_import_deletion_failures": import_failures,
        "mutation_expression_sha256": {
            name: hashlib.sha256(serialized[name].encode()).hexdigest()
            for name in MUTATIONS
        },
        "statement_file_sha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
        "toolchain": (LEAN_DIR / "lean-toolchain").read_text(encoding="utf-8").strip(),
    }
    environment_record = {
        "base_revision": BASE_REVISION,
        "base_tree": BASE_TREE,
        "direct_imports": DIRECT_IMPORTS,
        "foundation_profile": "foundation-profile/1.0",
        "lake_manifest_sha256": sha256(LEAN_DIR / "lake-manifest.json"),
        "lakefile_sha256": sha256(LEAN_DIR / "lakefile.lean"),
        "lean_commit": "98dc76e3c0a9b856c9b98726b713fb04fab16740",
        "lean_toolchain": payload["toolchain"],
        "mathlib_revision": MATHLIB_REVISION,
        "mathlib_tree": MATHLIB_TREE,
        "options": ["pp.explicit=true", "pp.universes=true"],
        "run_env": RUN_ENV,
        "target_declaration": f"{NAMESPACE}.{CANONICAL}",
    }
    canonical_environment = json.dumps(
        environment_record, sort_keys=True, separators=(",", ":")
    ).encode()
    payload["environment_fingerprint_sha256"] = hashlib.sha256(
        canonical_environment
    ).hexdigest()
    if not args.compute_only:
        check_artifacts(payload, args.worker_packet)
    print(json.dumps(payload, sort_keys=True))


if __name__ == "__main__":
    main()
