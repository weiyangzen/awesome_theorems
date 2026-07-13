#!/usr/bin/env python3
"""Validate the exact THM-M-0958 statement and structural mutations."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
LEAN_DIR = ROOT / "Formalizations" / "Lean"
SOURCE = Path(__file__).with_name("Statement.lean")
STATEMENT = SOURCE.with_name("statement.json")
RECEIPT = SOURCE.with_name("statement-receipt.json")
THEOREM_ID = "THM-M-0958"
ITEM_ID = "S56-M-0958-STATEMENT"
RANK = 1492
NAMESPACE = "Stage1Instances.THM_M_0958"
CANONICAL = "ElkinConstructionTarget"
PRINT_MARKER = f"#print {NAMESPACE}.{CANONICAL}"
SUPPORT_DECLARATIONS = (
    "elkinScale",
    "SourceProgressionFree",
    "WitnessConstructionTarget",
    "RothNumberTarget",
    CANONICAL,
)
MUTATIONS = (
    "mutationRemovedPositiveConstant",
    "mutationIntegerIndexDomain",
    "mutationPerIndexConstant",
    "mutationShiftsIntervalEndpoint",
)
TRANSPORTS = (
    "sourceProgressionFree_iff_threeAPFree",
    "oneBasedRothNumber_eq_rothNumberNat",
    "elkinConstructionTarget_iff_witnessConstructionTarget",
    "oneBasedExtremalTarget_iff_rothNumberTarget",
    "elkinConstructionTarget_iff_rothNumberTarget",
)
BOUNDARIES = (
    "elkinScale_zero",
    "elkinScale_one",
    "oneBasedInterval_zero",
    "oneBasedInterval_one",
)
DIRECT_IMPORTS = (
    "Mathlib.Combinatorics.Additive.AP.Three.Defs",
    "Mathlib.Analysis.SpecialFunctions.Log.Base",
)
BASE_REVISION = "c79ae75db8880483f10bba17c9bc9dd91a9febcf"
BASE_TREE = "375fa18a4f8afa63bb51d8b05fb4c804f3bb1240"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    "Stage1_Instances/THM-M-0958/README.md",
    "Stage1_Instances/THM-M-0958/Statement.lean",
    "Stage1_Instances/THM-M-0958/check_intake.py",
    "Stage1_Instances/THM-M-0958/check_statement.py",
    "Stage1_Instances/THM-M-0958/instance.json",
    "Stage1_Instances/THM-M-0958/scope-map.md",
    "Stage1_Instances/THM-M-0958/source-statement-crosswalk.md",
    "Stage1_Instances/THM-M-0958/statement-receipt.json",
    "Stage1_Instances/THM-M-0958/statement-validation.md",
    "Stage1_Instances/THM-M-0958/statement.json",
    "Stage1_Instances/THM-M-0958/task-dag.json",
    "Stage1_Instances/THM-M-0958/validation.md",
}
SOURCE_INPUTS = {
    "Docs/Stage1_Targets_rev-5.6.json": "Docs/Stage1_Targets_rev-5.6.json",
    "Docs/Stage1_Blueprint_rev-5.6.md": "Docs/Stage1_Blueprint_rev-5.6.md",
    "Docs/Stage1_Execution_DAG_rev-5.6.json": "Docs/Stage1_Execution_DAG_rev-5.6.json",
    "skills/execute-stage1-rev56/SKILL.md": "skills/execute-stage1-rev56/SKILL.md",
    "Docs/Blueprint_Guidelines.md": "Docs/Blueprint_Guidelines.md",
    "Docs/researches/math_theorems.md": "Docs/researches/math_theorems.md",
    "Docs/Stage0_Blueprint.md": "Docs/Stage0_Blueprint.md",
    "Formalizations/Lean/lean-toolchain": "Formalizations/Lean/lean-toolchain",
    "Formalizations/Lean/lake-manifest.json": "Formalizations/Lean/lake-manifest.json",
    "Stage1_Instances/THM-M-0958/instance.json":
        "Stage1_Instances/THM-M-0958/instance.json",
    "Stage1_Instances/THM-M-0958/source-statement-crosswalk.md":
        "Stage1_Instances/THM-M-0958/source-statement-crosswalk.md",
    "Stage1_Instances/THM-M-0958/scope-map.md":
        "Stage1_Instances/THM-M-0958/scope-map.md",
    "Stage1_Instances/THM-M-0958/task-dag.json":
        "Stage1_Instances/THM-M-0958/task-dag.json",
    "Stage1_Instances/THM-M-0958/intake-receipt.json":
        "Stage1_Instances/THM-M-0958/intake-receipt.json",
}


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise SystemExit(f"{path} must contain a JSON object")
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(["git", *args], cwd=cwd, text=True).strip()


def run_lean(path: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["lake", "env", "lean", str(path)],
        cwd=LEAN_DIR,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=180,
        check=False,
    )


def elaborate(path: Path) -> str:
    result = run_lean(path)
    if result.returncode:
        sys.stdout.write(result.stdout)
        raise SystemExit(result.returncode)
    return result.stdout


def run_text(text: str) -> subprocess.CompletedProcess[str]:
    with tempfile.NamedTemporaryFile(
        "w", suffix=".lean", dir=SOURCE.parent, delete=False, encoding="utf-8"
    ) as handle:
        handle.write(text)
        temporary = Path(handle.name)
    try:
        return run_lean(temporary)
    finally:
        temporary.unlink()


def serialized_expression(declaration: str) -> tuple[str, str]:
    text = SOURCE.read_text(encoding="utf-8")
    if text.count(PRINT_MARKER) != 1:
        raise SystemExit("canonical #print marker is missing or ambiguous")
    result = run_text(text.replace(PRINT_MARKER, f"#print {NAMESPACE}.{declaration}"))
    if result.returncode:
        sys.stdout.write(result.stdout)
        raise SystemExit(result.returncode)
    qualified = re.escape(f"{NAMESPACE}.{declaration}")
    match = re.search(
        rf"def {qualified} : Prop :=\n(?P<expression>.*)\Z",
        result.stdout,
        re.DOTALL,
    )
    if not match:
        raise SystemExit(f"could not serialize {declaration}")
    expression = match.group("expression").strip()
    if "?m." in expression or "sorryAx" in expression:
        raise SystemExit(f"invalid elaborated expression for {declaration}")
    return expression, result.stdout


def statement_bundle() -> str:
    text = SOURCE.read_text(encoding="utf-8")
    replacement = "\n".join(
        f"#print {NAMESPACE}.{name}" for name in SUPPORT_DECLARATIONS
    )
    result = run_text(text.replace(PRINT_MARKER, replacement))
    if result.returncode:
        sys.stdout.write(result.stdout)
        raise SystemExit(result.returncode)
    marker = f"def {NAMESPACE}.{SUPPORT_DECLARATIONS[0]}"
    if marker not in result.stdout:
        raise SystemExit("statement bundle serialization is missing")
    bundle = result.stdout[result.stdout.index(marker):].strip()
    if "?m." in bundle or "sorryAx" in bundle:
        raise SystemExit("invalid statement bundle")
    return bundle


def check_minimal_imports(source_text: str) -> list[dict]:
    imports = tuple(re.findall(r"^import ([^\s]+)$", source_text, re.MULTILINE))
    if imports != DIRECT_IMPORTS:
        raise SystemExit(f"unexpected direct imports: {imports!r}")
    target = """noncomputable section
open Finset
def ImportProbeScale (n : Nat) : Real :=
  ((n : Real) / (2 : Real) ^ (2 * Real.sqrt 2 * Real.sqrt
    (Real.logb 2 (n : Real)))) * (Real.logb 2 (n : Real)) ^ (1 / 4 : Real)
def ImportProbeTarget : Prop :=
  exists c : Real, 0 < c /\\ exists N : Nat, 0 < N /\\ forall n : Nat,
    N <= n -> c * ImportProbeScale n <=
      (addRothNumber (Ico 1 (n + 1)) : Real)
"""
    failures = []
    for omitted in DIRECT_IMPORTS:
        remaining = "".join(
            f"import {name}\n" for name in DIRECT_IMPORTS if name != omitted
        )
        result = run_text(remaining + target)
        if result.returncode == 0:
            raise SystemExit(f"direct import is redundant: {omitted}")
        normalized = re.sub(r"/[^:\n]+\.lean", "<fixture>.lean", result.stdout)
        first_error = next(
            (line for line in normalized.splitlines() if "error" in line),
            "Lean rejected the import-deletion fixture",
        )
        failures.append({
            "import": omitted,
            "exit_code": result.returncode,
            "first_error": first_error,
            "output_sha256": hashlib.sha256(normalized.encode()).hexdigest(),
        })
    return failures


def check_forbidden_constructs(text: str) -> None:
    no_comments = re.sub(r"/-.*?-/", "", text, flags=re.DOTALL)
    no_comments = re.sub(r"--.*", "", no_comments)
    forbidden = re.search(
        r"\b(?:sorry|admit|sorryAx|axiom|constant|opaque|unsafe)\b", no_comments
    )
    if forbidden:
        raise SystemExit(f"forbidden Lean construct: {forbidden.group(0)}")


def check_text_file(path: Path) -> None:
    data = path.read_bytes()
    if not data.endswith(b"\n"):
        raise SystemExit(f"missing final newline: {path}")
    if b"\r" in data or b"\x00" in data:
        raise SystemExit(f"invalid byte in {path}")
    if any(line.endswith((b" ", b"\t")) for line in data.splitlines()):
        raise SystemExit(f"trailing whitespace in {path}")


def check_artifacts(payload: dict, worker_packet: Path | None) -> None:
    statement = load(STATEMENT)
    receipt = load(RECEIPT)
    instance = load(SOURCE.with_name("instance.json"))
    task_dag = load(SOURCE.with_name("task-dag.json"))
    targets = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM_ID)
    item = next(row for row in execution["items"] if row["id"] == ITEM_ID)

    if target["execution_rank"] != statement["execution_rank"] or target["execution_rank"] != RANK:
        raise SystemExit("target rank mismatch")
    if target["baseline"] != "L0" or not target["rework_required"] or target["theorem_complete"]:
        raise SystemExit("target baseline or completion mismatch")
    if item["theorem_id"] != THEOREM_ID or item["phase"] != "statement" or item["layer"] != 1:
        raise SystemExit("authoritative item identity mismatch")
    if item["state"] != "[ ]" or item["depends_on"] != ["S56-M-0958-INTAKE"]:
        raise SystemExit("authoritative dependency/state mismatch")
    if item["owned_paths"] != [f"Stage1_Instances/{THEOREM_ID}"]:
        raise SystemExit("authoritative ownership mismatch")

    formal = statement["canonical_formal_target"]
    if statement["item_id"] != receipt["item_id"] or statement["item_id"] != ITEM_ID:
        raise SystemExit("statement item mismatch")
    if statement["theorem_id"] != receipt["theorem_id"] or statement["theorem_id"] != THEOREM_ID:
        raise SystemExit("statement theorem mismatch")
    if formal["declaration_or_expression"] != f"{NAMESPACE}.{CANONICAL}":
        raise SystemExit("canonical declaration mismatch")
    if formal["elaborated_expression_sha256"] != payload["elaborated_expression_sha256"]:
        raise SystemExit("expression fingerprint mismatch")
    if formal["statement_bundle_sha256"] != payload["statement_bundle_sha256"]:
        raise SystemExit("bundle fingerprint mismatch")
    if formal["statement_file_sha256"] != payload["statement_file_sha256"]:
        raise SystemExit("source fingerprint mismatch")
    if tuple(statement["direct_imports"]) != DIRECT_IMPORTS:
        raise SystemExit("statement import mismatch")
    if statement["root_vector_before"] != {"H": "H1", "M": "M4", "R": "R4"}:
        raise SystemExit("incorrect prior debt vector")
    if statement["root_vector_after"] != {"H": "H1", "M": "M3", "R": "R4"}:
        raise SystemExit("incorrect statement debt vector")
    if not statement["statement_elaborated"] or statement["theorem_proved"]:
        raise SystemExit("statement elaboration/proof flag mismatch")
    if statement["audit_complete"] or statement["theorem_complete"] or statement["accepted_receipt_ids"]:
        raise SystemExit("statement overclaims closure")

    instance_formal = instance["canonical_formal_target"]
    if instance["canonical_statement"] != statement["canonical_statement"]:
        raise SystemExit("instance statement is stale")
    if instance_formal["elaborated_expression_hash"] != f"sha256:{payload['elaborated_expression_sha256']}":
        raise SystemExit("instance expression fingerprint is stale")
    if instance["root_vector"] != statement["root_vector_after"]:
        raise SystemExit("instance debt vector is stale")
    local_item = next(row for row in task_dag["tasks"] if row["id"] == ITEM_ID)
    if receipt["receipt_id"] not in local_item["evidence_ids"]:
        raise SystemExit("local task DAG omits statement receipt")

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
    if receipt["statement_fingerprints"] != [f"sha256:{payload['statement_bundle_sha256']}"]:
        raise SystemExit("receipt statement fingerprint mismatch")
    if receipt["statement_file_sha256"] != payload["statement_file_sha256"]:
        raise SystemExit("receipt source hash mismatch")
    if receipt["checker_sha256"] != sha256(Path(__file__)):
        raise SystemExit("receipt checker hash mismatch")
    if receipt["lean_output_sha256"] != payload["lean_output_sha256"]:
        raise SystemExit("receipt Lean output hash mismatch")
    if receipt["root_vector_before"] != statement["root_vector_before"] or receipt["root_vector_after"] != statement["root_vector_after"]:
        raise SystemExit("receipt debt vector mismatch")
    if receipt["accepted_receipt_ids"] or receipt["proof_body_locations"]:
        raise SystemExit("receipt claims proof or acceptance")
    if receipt["audit_complete"] or receipt["theorem_complete"] or receipt["selftest_result"] != "pass":
        raise SystemExit("receipt completion/self-test mismatch")

    for key, relative in SOURCE_INPUTS.items():
        expected = f"sha256:{sha256(ROOT / relative)}"
        if receipt["source_inputs"].get(key) != expected:
            raise SystemExit(f"stale source hash: {key}")
    mathlib = LEAN_DIR / ".lake/packages/mathlib"
    if git("rev-parse", "HEAD", cwd=mathlib) != MATHLIB_REVISION:
        raise SystemExit("mathlib revision mismatch")
    if git("rev-parse", "HEAD^{tree}", cwd=mathlib) != MATHLIB_TREE:
        raise SystemExit("mathlib tree mismatch")
    if git("status", "--short", cwd=mathlib):
        raise SystemExit("mathlib worktree is dirty")
    for module in DIRECT_IMPORTS:
        source = mathlib / (module.replace(".", "/") + ".lean")
        if receipt["worker_input_hashes"].get(module) != f"sha256:{sha256(source)}":
            raise SystemExit(f"direct import hash mismatch: {module}")

    for relative in CHANGED_PATHS - {".stage1-worker-selftest.json"}:
        check_text_file(ROOT / relative)

    if worker_packet is not None:
        packet = load(worker_packet.resolve())
        required = {
            "item_id", "changed_paths", "commands", "output_summary",
            "base_revision", "known_failures", "state",
        }
        if set(packet) != required:
            raise SystemExit("worker packet key mismatch")
        if packet["item_id"] != ITEM_ID or packet["state"] != "[_]":
            raise SystemExit("worker packet identity/state mismatch")
        if packet["base_revision"] != BASE_REVISION:
            raise SystemExit("worker packet base mismatch")
        if set(packet["changed_paths"]) != CHANGED_PATHS:
            raise SystemExit("worker packet changed-path mismatch")
        if packet["known_failures"] != receipt["known_failures"]:
            raise SystemExit("worker packet failure list mismatch")
        if not packet["commands"] or not packet["output_summary"]:
            raise SystemExit("worker packet evidence is incomplete")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker-packet", type=Path)
    args = parser.parse_args()

    source_text = SOURCE.read_text(encoding="utf-8")
    check_forbidden_constructs(source_text)
    lean_output = elaborate(SOURCE)
    canonical, _ = serialized_expression(CANONICAL)
    mutation_expressions = {
        name: serialized_expression(name)[0] for name in MUTATIONS
    }
    survivors = [name for name, value in mutation_expressions.items() if value == canonical]
    if survivors:
        raise SystemExit(f"statement mutation survived: {', '.join(survivors)}")
    for name in TRANSPORTS + BOUNDARIES:
        if not re.search(rf"^theorem {re.escape(name)}\b", source_text, re.MULTILINE):
            raise SystemExit(f"missing checked statement witness: {name}")
    import_failures = check_minimal_imports(source_text)
    bundle = statement_bundle()
    payload = {
        "direct_imports": list(DIRECT_IMPORTS),
        "elaborated_expression_sha256": hashlib.sha256(canonical.encode()).hexdigest(),
        "killed_mutations": list(MUTATIONS),
        "lean_output_sha256": hashlib.sha256(lean_output.encode()).hexdigest(),
        "mathlib_revision": MATHLIB_REVISION,
        "minimal_import_deletion_failures": import_failures,
        "mutation_expression_sha256": {
            name: hashlib.sha256(value.encode()).hexdigest()
            for name, value in mutation_expressions.items()
        },
        "statement_bundle_sha256": hashlib.sha256(bundle.encode()).hexdigest(),
        "statement_file_sha256": sha256(SOURCE),
        "toolchain": (LEAN_DIR / "lean-toolchain").read_text(encoding="utf-8").strip(),
    }
    if STATEMENT.exists() and RECEIPT.exists():
        check_artifacts(payload, args.worker_packet)
    elif args.worker_packet is not None:
        raise SystemExit("worker-packet validation requires finalized records")
    print(json.dumps(payload, sort_keys=True))


if __name__ == "__main__":
    main()
