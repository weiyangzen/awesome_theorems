#!/usr/bin/env python3
"""Validate the exact THM-M-0812 statement and structural mutations."""

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
STATEMENT_RECORD = SOURCE.with_name("statement.json")
RECEIPT = SOURCE.with_name("statement-receipt.json")
NAMESPACE = "Stage1Instances.THM_M_0812"
CANONICAL = "KonigMatchingCoverTarget"
SUPPORT_DECLARATIONS = [
    "IsEdgeMatching",
    "IsBipartiteVertexCover",
    "HasMatchingNumber",
    "HasVertexCoverNumber",
    "SimpleRelationKonigTarget",
]
MUTATIONS = [
    "mutationRemovedFiniteEdges",
    "mutationCountsMatchingVertices",
    "mutationChangedEndpointBinderScope",
    "mutationExcludesEdgelessGraph",
]
DIRECT_IMPORTS = ["Mathlib.Data.Finite.Card", "Mathlib.Data.Set.Card"]
ITEM_ID = "S56-M-0812-STATEMENT"
THEOREM_ID = "THM-M-0812"
BASE_REVISION = "39704171d88ffcdc33a47365ae9791f855fa3a44"
BASE_TREE = "050ab5c6392560337051d2eadd1b82277dbe1c4f"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    "Stage1_Instances/THM-M-0812/README.md",
    "Stage1_Instances/THM-M-0812/Statement.lean",
    "Stage1_Instances/THM-M-0812/check_statement.py",
    "Stage1_Instances/THM-M-0812/instance.json",
    "Stage1_Instances/THM-M-0812/scope-map.md",
    "Stage1_Instances/THM-M-0812/source-statement-crosswalk.md",
    "Stage1_Instances/THM-M-0812/statement-receipt.json",
    "Stage1_Instances/THM-M-0812/statement-validation.md",
    "Stage1_Instances/THM-M-0812/statement.json",
    "Stage1_Instances/THM-M-0812/task-dag.json",
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
    "Stage1_Instances/THM-M-0812/instance.json": "Stage1_Instances/THM-M-0812/instance.json",
    "Stage1_Instances/THM-M-0812/source-statement-crosswalk.md":
        "Stage1_Instances/THM-M-0812/source-statement-crosswalk.md",
    "Stage1_Instances/THM-M-0812/intake-receipt.json":
        "Stage1_Instances/THM-M-0812/intake-receipt.json",
    "Stage1_Instances/THM-M-0812/task-dag.json":
        "Stage1_Instances/THM-M-0812/task-dag.json",
    "Stage1_Instances/THM-M-0812/scope-map.md":
        "Stage1_Instances/THM-M-0812/scope-map.md",
}


def run_lean(source: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["lake", "env", "lean", str(source)],
        cwd=LEAN_DIR,
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


def serialized_expression(declaration: str) -> tuple[str, str]:
    text = SOURCE.read_text(encoding="utf-8")
    marker = f"#print {NAMESPACE}.{CANONICAL}"
    if text.count(marker) != 1:
        raise SystemExit("canonical #print marker is missing or ambiguous")
    text = text.replace(marker, f"#print {NAMESPACE}.{declaration}")
    with tempfile.NamedTemporaryFile(
        "w", suffix=".lean", dir=SOURCE.parent, delete=False, encoding="utf-8"
    ) as handle:
        handle.write(text)
        temporary = Path(handle.name)
    try:
        output = elaborate(temporary)
    finally:
        temporary.unlink()
    match = re.search(
        rf"(?:def|theorem) {re.escape(NAMESPACE)}\.{re.escape(declaration)}"
        r"(?:\.\{[^\n]*\})?[^:]*: Prop :=\n(?P<expression>.*)\Z",
        output,
        re.DOTALL,
    )
    if not match:
        raise SystemExit(f"could not serialize {declaration}")
    expression = match.group("expression").strip()
    if "?m." in expression:
        raise SystemExit(f"unresolved metavariable in {declaration}")
    return expression, output


def support_serialization() -> str:
    text = SOURCE.read_text(encoding="utf-8")
    marker = f"#print {NAMESPACE}.{CANONICAL}"
    replacement = "\n".join(
        f"#print {NAMESPACE}.{name}" for name in [*SUPPORT_DECLARATIONS, CANONICAL]
    )
    text = text.replace(marker, replacement)
    with tempfile.NamedTemporaryFile(
        "w", suffix=".lean", dir=SOURCE.parent, delete=False, encoding="utf-8"
    ) as handle:
        handle.write(text)
        temporary = Path(handle.name)
    try:
        output = elaborate(temporary)
    finally:
        temporary.unlink()
    tail = output[output.index(f"def {NAMESPACE}.{SUPPORT_DECLARATIONS[0]}") :].strip()
    if "?m." in tail:
        raise SystemExit("unresolved metavariable in canonical statement bundle")
    return tail


def check_minimal_import(source_text: str) -> dict[str, str | int]:
    imports = [
        line.removeprefix("import ")
        for line in source_text.splitlines()
        if line.startswith("import ")
    ]
    if imports != DIRECT_IMPORTS:
        raise SystemExit(f"unexpected direct imports: {imports}")

    canonical_start = "/-- A set of edges is a matching when neither endpoint map identifies two"
    mutation_start = "/-! Structural statement mutations. -/"
    if source_text.count(canonical_start) != 1 or source_text.count(mutation_start) != 1:
        raise SystemExit("canonical target fixture marker is missing or ambiguous")
    fixture = (
        source_text[: source_text.index(mutation_start)]
        + "\nend Stage1Instances.THM_M_0812\n"
    )
    with tempfile.NamedTemporaryFile(
        "w", suffix=".lean", dir=SOURCE.parent, delete=False, encoding="utf-8"
    ) as handle:
        handle.write(fixture)
        baseline = Path(handle.name)
    try:
        baseline_result = run_lean(baseline)
    finally:
        baseline.unlink()
    if baseline_result.returncode:
        sys.stdout.write(baseline_result.stdout)
        raise SystemExit("canonical fixture does not elaborate with the declared import")

    negative_results = []
    for direct_import in DIRECT_IMPORTS:
        candidate = fixture.replace(f"import {direct_import}\n", "", 1)
        with tempfile.NamedTemporaryFile(
            "w", suffix=".lean", dir=SOURCE.parent, delete=False, encoding="utf-8"
        ) as handle:
            handle.write(candidate)
            no_import = Path(handle.name)
        try:
            result = run_lean(no_import)
        finally:
            no_import.unlink()
        if result.returncode == 0:
            raise SystemExit(f"direct import is redundant: {direct_import}")
        negative_results.append({"import": direct_import, "exit_code": result.returncode})
    return {
        "fixture": "canonical definitions and checked statement transports",
        "deletions": negative_results,
        "result": "expected failure after deleting either direct import",
    }


def check_forbidden_constructs(text: str) -> None:
    no_comments = re.sub(r"/-.*?-/", "", text, flags=re.DOTALL)
    no_comments = re.sub(r"--.*", "", no_comments)
    match = re.search(
        r"\b(?:sorry|admit|sorryAx|axiom|constant|opaque|unsafe)\b", no_comments
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


def check_artifacts(payload: dict, worker_packet: Path | None) -> None:
    statement = load(STATEMENT_RECORD)
    receipt = load(RECEIPT)
    targets = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM_ID)
    item = next(row for row in execution["items"] if row["id"] == ITEM_ID)

    if target["execution_rank"] != 1371 or statement["execution_rank"] != 1371:
        raise SystemExit("target execution rank mismatch")
    if target["baseline"] != "L0" or not target["rework_required"]:
        raise SystemExit("target baseline mismatch")
    if target["theorem_complete"]:
        raise SystemExit("target manifest overclaims theorem completion")
    if item["theorem_id"] != THEOREM_ID or item["phase"] != "statement":
        raise SystemExit("statement DAG identity mismatch")
    if item["state"] != "[ ]" or item["depends_on"] != ["S56-M-0812-INTAKE"]:
        raise SystemExit("statement DAG dependency/state mismatch")
    if item["owned_paths"] != ["Stage1_Instances/THM-M-0812"]:
        raise SystemExit("statement ownership mismatch")

    formal = statement["canonical_formal_target"]
    if statement["item_id"] != receipt["item_id"] or statement["item_id"] != ITEM_ID:
        raise SystemExit("item id mismatch")
    if statement["theorem_id"] != receipt["theorem_id"] or statement["theorem_id"] != THEOREM_ID:
        raise SystemExit("theorem id mismatch")
    if formal["declaration_or_expression"] != f"{NAMESPACE}.{CANONICAL}":
        raise SystemExit("canonical declaration mismatch")
    if formal["elaborated_expression_sha256"] != payload["elaborated_expression_sha256"]:
        raise SystemExit("canonical expression hash mismatch")
    if formal["statement_bundle_sha256"] != payload["statement_bundle_sha256"]:
        raise SystemExit("statement bundle hash mismatch")
    if formal["statement_file_sha256"] != payload["statement_file_sha256"]:
        raise SystemExit("statement source hash mismatch")
    if statement["direct_imports"] != DIRECT_IMPORTS:
        raise SystemExit("statement import mismatch")
    if statement["root_vector_before"] != statement["root_vector_after"]:
        raise SystemExit("unexpected debt-vector transition")
    if statement["root_vector_after"] != {"H": "H1", "M": "M3", "R": "R2"}:
        raise SystemExit("incorrect statement debt vector")
    if not statement["statement_elaborated"]:
        raise SystemExit("statement is not marked elaborated")
    if statement["theorem_proved"] or statement["audit_complete"] or statement["theorem_complete"]:
        raise SystemExit("statement record overclaims closure")
    if statement["accepted_receipt_ids"]:
        raise SystemExit("statement record claims accepted receipt")

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
        f"sha256:{payload['statement_bundle_sha256']}"
    ]:
        raise SystemExit("receipt statement fingerprint mismatch")
    if receipt["statement_file_sha256"] != payload["statement_file_sha256"]:
        raise SystemExit("receipt source hash mismatch")
    if receipt["checker_sha256"] != sha256(Path(__file__)):
        raise SystemExit("receipt checker hash mismatch")
    if receipt["lean_output_sha256"] != payload["lean_output_sha256"]:
        raise SystemExit("receipt Lean output hash mismatch")
    if receipt["direct_imports"] != DIRECT_IMPORTS:
        raise SystemExit("receipt import mismatch")
    if receipt["root_vector_before"] != receipt["root_vector_after"]:
        raise SystemExit("receipt debt transition mismatch")
    if receipt["root_vector_after"] != {"H": "H1", "M": "M3", "R": "R2"}:
        raise SystemExit("receipt debt vector mismatch")
    if receipt["accepted_receipt_ids"] or receipt["proof_body_locations"]:
        raise SystemExit("receipt claims proof or acceptance")
    if receipt["audit_complete"] or receipt["theorem_complete"]:
        raise SystemExit("receipt overclaims closure")
    if receipt["selftest_result"] != "pass":
        raise SystemExit("receipt self-test is not final")

    expected_cut_set = [
        "S56-M-0812-INTAKE",
        "S56-M-0812-STATEMENT",
        "S56-M-0812-ANCHOR_AUDIT",
        "S56-M-0812-OBLIGATION_TREE",
        "S56-M-0812-PROOF",
        "S56-M-0812-VALIDATION",
        "S56-M-0812-RELEASE",
    ]
    if receipt["remaining_root_cut_set"] != expected_cut_set:
        raise SystemExit("receipt root cut set omits an unfinished dependency")

    for key, relative in SOURCE_INPUTS.items():
        if receipt["source_inputs"].get(key) != f"sha256:{sha256(ROOT / relative)}":
            raise SystemExit(f"stale source hash: {key}")
    mathlib = LEAN_DIR / ".lake/packages/mathlib"
    if git("rev-parse", "HEAD", cwd=mathlib) != MATHLIB_REVISION:
        raise SystemExit("mathlib revision mismatch")
    if git("rev-parse", "HEAD^{tree}", cwd=mathlib) != MATHLIB_TREE:
        raise SystemExit("mathlib tree mismatch")
    if git("status", "--short", cwd=mathlib):
        raise SystemExit("mathlib worktree is dirty")
    for direct_import in DIRECT_IMPORTS:
        direct_source = mathlib / (direct_import.replace(".", "/") + ".lean")
        if receipt["worker_input_hashes"][direct_import] != f"sha256:{sha256(direct_source)}":
            raise SystemExit(f"direct-import source hash mismatch: {direct_import}")

    for relative in CHANGED_PATHS - {".stage1-worker-selftest.json"}:
        check_text_file(ROOT / relative)

    if worker_packet is not None:
        packet = load(worker_packet)
        required_keys = {
            "item_id", "changed_paths", "commands", "output_summary",
            "base_revision", "known_failures", "state",
        }
        if set(packet) != required_keys:
            raise SystemExit("worker packet key mismatch")
        if packet["item_id"] != ITEM_ID or packet["state"] != "[_]":
            raise SystemExit("worker packet identity/state mismatch")
        if packet["base_revision"] != BASE_REVISION:
            raise SystemExit("worker packet base mismatch")
        if set(packet["changed_paths"]) != CHANGED_PATHS:
            raise SystemExit("worker packet changed-path mismatch")
        if not packet["commands"] or not packet["known_failures"]:
            raise SystemExit("worker packet evidence is incomplete")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker-packet", type=Path)
    args = parser.parse_args()

    source_text = SOURCE.read_text(encoding="utf-8")
    check_forbidden_constructs(source_text)
    lean_output = elaborate(SOURCE)
    canonical, _ = serialized_expression(CANONICAL)
    expressions = {name: serialized_expression(name)[0] for name in MUTATIONS}
    survivors = [name for name, value in expressions.items() if value == canonical]
    if survivors:
        raise SystemExit(f"statement mutation survived: {', '.join(survivors)}")
    minimal_import = check_minimal_import(source_text)
    bundle = support_serialization()

    payload = {
        "direct_imports": DIRECT_IMPORTS,
        "elaborated_expression_sha256": hashlib.sha256(canonical.encode()).hexdigest(),
        "killed_mutations": MUTATIONS,
        "lean_output_sha256": hashlib.sha256(lean_output.encode()).hexdigest(),
        "mathlib_revision": MATHLIB_REVISION,
        "minimal_import_negative": minimal_import,
        "statement_bundle_sha256": hashlib.sha256(bundle.encode()).hexdigest(),
        "statement_file_sha256": sha256(SOURCE),
        "toolchain": (LEAN_DIR / "lean-toolchain").read_text().strip(),
    }
    if STATEMENT_RECORD.exists() and RECEIPT.exists():
        check_artifacts(payload, args.worker_packet)
    elif args.worker_packet is not None:
        raise SystemExit("worker packet validation requires finalized records")
    print(json.dumps(payload, sort_keys=True))


if __name__ == "__main__":
    main()
