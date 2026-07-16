#!/usr/bin/env python3
"""Validate the exact THM-M-0123 statement and emit one semantic result."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
LEAN_DIR = ROOT / "Formalizations" / "Lean"
SOURCE = HERE / "Statement.lean"
STATEMENT = HERE / "statement.json"
RECEIPT = HERE / "statement-receipt.json"
LEDGER = HERE / "dependency-reuse-ledger.json"
VALIDATION = HERE / "statement-validation.md"
PACKET = ROOT / ".stage1-worker-selftest.json"
THEOREM_ID = "THM-M-0123"
ITEM_ID = "S56-M-0123-STATEMENT"
NAMESPACE = "Stage1Instances.THM_M_0123"
CANONICAL = "MordellTarget"
MUTATIONS = (
    "MutationRemovedGenusHypothesis",
    "MutationRemovedNumberField",
    "MutationChangedCurveBinderScope",
    "MutationIncludesGenusOne",
)
TRANSPORTS = (
    "mordellTarget_iff_expanded",
    "finite_rationalPoint_iff_finite_over",
    "mordellTarget_iff_over",
)
DIRECT_IMPORTS = (
    "Mathlib.AlgebraicGeometry.Geometrically.Basic",
    "Mathlib.AlgebraicGeometry.Modules.Sheaf",
    "Mathlib.AlgebraicGeometry.Morphisms.Proper",
    "Mathlib.AlgebraicGeometry.Morphisms.Smooth",
    "Mathlib.CategoryTheory.Abelian.GrothendieckCategory.HasExt",
    "Mathlib.CategoryTheory.Sites.SheafCohomology.Basic",
    "Mathlib.NumberTheory.NumberField.Basic",
    "Mathlib.Topology.Sheaves.Abelian",
)
GRAPH_SHA256 = "3d32f808e2914b338c459d52651b69731f0979a90a720f98bc0f31a577e2bafa"
CONTEXT_SHA256 = "068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c"
CONTRACT_SHA256 = "1e7adf0f4fae0541b3595d4b0bfbb53f7eb17e28a4a889fec14f6df969e0cec4"
BASE_REVISION = "2dc5a410b68eff806858fd6ed0cb33d57f6209f7"
BASE_TREE = "841bdd6114e7436cff4a3a1ff248fc1e884a9ddc"
EXPECTED_EXPRESSION_SHA256 = "9fa3c7a0bff55098e7cc234793cb06ec1628e84e003ddb273a6dc47094f58dbd"
EXPECTED_STATEMENT_SHA256 = "62c3d5936d64ed2225d239246ac8139663bc4f722f896625b94bb9a11e59ca8f"
EXPECTED_LEAN_OUTPUT_SHA256 = "f57215dfa63c8993cf43abfd1a3bbe60715bdda3e635f2c4a9a8cf35591748a6"


def semantic(*, passed: bool, gate: str | None, message: str) -> dict[str, object]:
    return {
        "schema_version": "stage1-validator-semantic-result/1.0",
        "item_id": ITEM_ID,
        "theorem_id": THEOREM_ID,
        "phase": "statement",
        "status": "passed" if passed else "failed",
        "verdict": "phase_accepted" if passed else "repair_required",
        "phase_accepted": passed,
        "audit_complete": False,
        "theorem_complete": False,
        "phase_predicate_proven": passed,
        "first_failed_gate": gate,
        "open_obligations": 0 if passed else 1,
        "stale_inputs": [],
        "blocked": False,
        "message": message,
    }


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path.relative_to(ROOT)} is not a JSON object")
    return value


def run_lean(path: Path) -> subprocess.CompletedProcess[str]:
    environment = os.environ.copy()
    environment.update({"LC_ALL": "C", "TZ": "UTC"})
    return subprocess.run(
        ["lake", "env", "lean", str(path)],
        cwd=LEAN_DIR,
        env=environment,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )


def run_text(value: str) -> subprocess.CompletedProcess[str]:
    with tempfile.NamedTemporaryFile(
        "w", suffix=".lean", encoding="utf-8", dir=Path(os.environ.get("TMPDIR", "/tmp")),
        delete=False
    ) as handle:
        handle.write(value)
        temporary = Path(handle.name)
    try:
        return run_lean(temporary)
    finally:
        temporary.unlink()


def elaborate_expressions() -> tuple[dict[str, str], str]:
    source = SOURCE.read_text(encoding="utf-8")
    marker = f"#print {CANONICAL}"
    if source.count(marker) != 1:
        raise ValueError("canonical print marker is not unique")
    namespace_end = f"end {NAMESPACE}"
    if source.count(namespace_end) != 1:
        raise ValueError("namespace terminator is not unique")
    source = source.replace(marker, "")
    declarations = (CANONICAL,) + MUTATIONS
    dispatcher = "".join(
        "set_option pp.universes true in\n"
        "set_option pp.explicit true in\n"
        f"#print {declaration}\n\n"
        for declaration in declarations
    )
    source = source.replace(namespace_end, dispatcher + namespace_end)
    result = run_text(source)
    if result.returncode:
        raise ValueError(f"Lean failed during expression serialization: {result.stdout[:600]}")
    expressions: dict[str, str] = {}
    for index, declaration in enumerate(declarations):
        qualified = re.escape(f"{NAMESPACE}.{declaration}")
        next_prefix = (
            rf"\ndef {re.escape(f'{NAMESPACE}.{declarations[index + 1]}')}"
            if index + 1 < len(declarations)
            else r"\Z"
        )
        match = re.search(
            rf"def {qualified}(?:\.\{{[^\n]*\}})? : Prop :=\n(?P<body>.*?){next_prefix}",
            result.stdout,
            re.DOTALL,
        )
        if match is None:
            raise ValueError(f"explicit expression unavailable for {declaration}")
        expressions[declaration] = match.group("body").strip()
    canonical_output = result.stdout.split(
        f"def {NAMESPACE}.{MUTATIONS[0]}", 1
    )[0].rstrip() + "\n"
    return expressions, canonical_output


def check() -> tuple[str, str, str]:
    source_text = SOURCE.read_text(encoding="utf-8")
    imports = tuple(re.findall(r"^import ([^\s]+)$", source_text, re.MULTILINE))
    if imports != DIRECT_IMPORTS:
        raise ValueError("direct imports changed")

    blueprint = (ROOT / "Docs" / "Stage1_Blueprint_v2.md").read_text(encoding="utf-8")
    row = re.search(
        r"^- \[ \] `S56-M-0123-STATEMENT` / `THM-M-0123` / `statement`:.*\n"
        r"  Depends: `S56-M-0123-INTAKE`\. Owned paths: `Stage1_Instances/THM-M-0123`\.",
        blueprint,
        re.MULTILINE,
    )
    if row is None:
        raise ValueError("authoritative v2 statement row changed")

    dag = load(ROOT / "Docs" / "Stage1_Theorem_DAG_v2.json")
    node = next(item for item in dag["theorems"] if item["theorem_id"] == THEOREM_ID)
    graph_hash = sha256_bytes((ROOT / "Docs" / "Stage1_Theorem_DAG_v2.json").read_bytes())
    if graph_hash != GRAPH_SHA256:
        raise ValueError("v2 graph digest changed")
    if node["v2_execution_rank"] != 276 or node["topological_layer"] != 0:
        raise ValueError("v2 claim order changed")
    if node["phase_states"]["statement"] != "[ ]":
        raise ValueError("authoritative statement state changed")
    if node["dependency_context_sha256"] != CONTEXT_SHA256:
        raise ValueError("dependency context changed")
    for field in (
        "direct_hard_parents",
        "transitive_hard_ancestors",
        "direct_reuse_hint_ids",
        "shared_lemma_group_ids",
    ):
        if node[field] != []:
            raise ValueError(f"unexpected nonempty dependency field {field}")

    contract = load(ROOT / "Docs" / "Stage1_Phase_Acceptance_Contracts.json")
    if sha256_bytes((ROOT / "Docs" / "Stage1_Phase_Acceptance_Contracts.json").read_bytes()) != CONTRACT_SHA256:
        raise ValueError("statement phase contract digest changed")
    phase_rows = [row for row in contract["phases"] if row["phase"] == "statement"]
    if len(phase_rows) != 1:
        raise ValueError("statement phase contract is ambiguous")
    phase_row = phase_rows[0]
    roles = {row["role"]: row for row in phase_row["required_artifact_roles"]}
    expected_role_paths = {
        "statement_record": "Stage1_Instances/{theorem_id}/statement.json",
        "statement_source": "Stage1_Instances/{theorem_id}/Statement.lean",
        "phase_receipt": "Stage1_Instances/{theorem_id}/statement-receipt.json",
    }
    for role, path in expected_role_paths.items():
        if roles.get(role, {}).get("path_candidates") != [path]:
            raise ValueError(f"statement contract candidate changed: {role}")
    if "Stage1_Instances/{theorem_id}/source-statement-crosswalk.md" not in roles.get(
        "source_crosswalk", {}
    ).get("path_candidates", []):
        raise ValueError("source crosswalk contract candidate changed")
    validator_paths = {row["path_pattern"] for row in phase_row["validator_candidates"]}
    if "Stage1_Instances/{theorem_id}/check_statement.py" not in validator_paths:
        raise ValueError("statement validator candidate changed")
    common_fields = set(contract["artifact_resolution"]["worker_phase_receipt_required_fields"])
    phase_fields = set(phase_row["phase_receipt_required_fields"])
    receipt_for_contract = load(RECEIPT)
    for pointer in common_fields | phase_fields:
        current: object = receipt_for_contract
        for part in pointer.lstrip("/").split("/"):
            if not isinstance(current, dict) or part not in current:
                raise ValueError(f"receipt lacks contract field {pointer}")
            current = current[part]

    ledger = load(LEDGER)
    if ledger != {
        "schema_version": "stage1-dependency-reuse-ledger/1.1",
        "theorem_id": THEOREM_ID,
        "graph_sha256": GRAPH_SHA256,
        "dependency_context_sha256": CONTEXT_SHA256,
        "repository_revision": BASE_REVISION,
        "direct_parent_ids": [],
        "transitive_ancestor_ids": [],
        "hard_edge_ids": [],
        "reuse_hint_ids": [],
        "shared_group_ids": [],
        "inspections": [],
        "reuse_decisions": [],
        "unresolved_compatibility_obligations": [],
    }:
        raise ValueError("empty audited dependency ledger changed")

    expressions, canonical_output = elaborate_expressions()
    if len(set(expressions.values())) != len(expressions):
        raise ValueError("a required mutation has the canonical expression")

    for name in TRANSPORTS:
        if re.search(rf"^theorem {name}\b", source_text, re.MULTILINE) is None:
            raise ValueError(f"checked transport missing: {name}")
    if "sorryAx" in canonical_output or "warning: declaration uses `sorry`" in canonical_output:
        raise ValueError("canonical elaboration contains sorry evidence")
    expected_axioms = {
        "'Stage1Instances.THM_M_0123.mordellTarget_iff_expanded' depends on axioms: "
        "[propext, Classical.choice, Quot.sound]",
        "'Stage1Instances.THM_M_0123.mordellTarget_iff_over' depends on axioms: "
        "[propext, Classical.choice, Quot.sound]",
    }
    if not expected_axioms.issubset(set(canonical_output.splitlines())):
        raise ValueError("statement transport axiom report changed")

    expression_hash = sha256_bytes(expressions[CANONICAL].encode("utf-8"))
    source_hash = sha256_bytes(SOURCE.read_bytes())
    output_hash = sha256_bytes(canonical_output.encode("utf-8"))
    pinned = (
        ("expression", EXPECTED_EXPRESSION_SHA256, expression_hash),
        ("source", EXPECTED_STATEMENT_SHA256, source_hash),
        ("Lean output", EXPECTED_LEAN_OUTPUT_SHA256, output_hash),
    )
    for label, expected, actual in pinned:
        if expected != "TO_BE_RECONCILED" and expected != actual:
            raise ValueError(f"{label} fingerprint changed")

    statement = load(STATEMENT)
    receipt = load(RECEIPT)
    formal = statement["canonical_formal_target"]
    if formal["elaborated_expression_sha256"] != expression_hash:
        raise ValueError("statement expression hash is stale")
    if formal["statement_file_sha256"] != source_hash:
        raise ValueError("statement source hash is stale")
    if statement["direct_imports"] != list(DIRECT_IMPORTS):
        raise ValueError("statement import record is stale")
    if receipt["statement_fingerprints"] != [f"sha256:{expression_hash}"]:
        raise ValueError("receipt expression hash is stale")
    if receipt["statement_file_sha256"] != source_hash:
        raise ValueError("receipt source hash is stale")
    if receipt["lean_output_sha256"] != output_hash:
        raise ValueError("receipt Lean-output hash is stale")
    if receipt["base_revision"] != BASE_REVISION or receipt["base_tree"] != BASE_TREE:
        raise ValueError("receipt base identity changed")
    if receipt["contract_sha256"] != CONTRACT_SHA256:
        raise ValueError("receipt contract binding changed")
    if receipt["receipt_id"] != f"{ITEM_ID}-WORKER-{expression_hash[:12].upper()}":
        raise ValueError("receipt id is stale")
    if receipt["selftest_status"] != "passed" or receipt["selftest_result"]["exit_code"] != 0:
        raise ValueError("receipt self-test status changed")
    if receipt["validator_sha256"] != sha256_bytes(Path(__file__).read_bytes()):
        raise ValueError("receipt validator hash is stale")
    if receipt["accepted"] is not False or receipt["proposed_state"] != "[_]":
        raise ValueError("receipt acceptance boundary changed")
    if receipt["audit_complete"] is not False or receipt["theorem_complete"] is not False:
        raise ValueError("receipt terminal boundary changed")
    for path_string, tagged_hash in receipt["inputs"].items():
        algorithm, expected_hash = tagged_hash.split(":", 1)
        if algorithm != "sha256" or sha256_bytes((ROOT / path_string).read_bytes()) != expected_hash:
            raise ValueError(f"receipt input binding is stale: {path_string}")
    import_sources = receipt["import_source_sha256"]
    if set(import_sources) != set(DIRECT_IMPORTS):
        raise ValueError("receipt import-source inventory changed")
    mathlib_root = LEAN_DIR / ".lake" / "packages" / "mathlib"
    for module, expected_hash in import_sources.items():
        module_path = mathlib_root / (module.replace(".", "/") + ".lean")
        if sha256_bytes(module_path.read_bytes()) != expected_hash:
            raise ValueError(f"import source changed: {module}")
    receipt_bindings = receipt["artifact_bindings"]
    if len(receipt_bindings) != 3 or {row["role"] for row in receipt_bindings} != {
        "statement_record", "statement_source", "source_crosswalk"
    }:
        raise ValueError("receipt artifact roles changed")
    for binding in receipt_bindings:
        path = ROOT / binding["path"]
        data = path.read_bytes()
        framed = f"blob {len(data)}\0".encode("ascii") + data
        if binding["sha256"] != sha256_bytes(data):
            raise ValueError(f"stale artifact sha256: {binding['role']}")
        if binding["git_blob"] != hashlib.sha1(framed).hexdigest():
            raise ValueError(f"stale artifact Git blob: {binding['role']}")
    if receipt["phase_receipt_self_binding"] != {
        "role": "phase_receipt",
        "path": "Stage1_Instances/THM-M-0123/statement-receipt.json",
        "binding_kind": "git_object_at_integration",
        "expected_sha256": None,
        "expected_git_blob": None,
        "status": "deferred_to_scheduler_master_lane_after_HEAD_tracking",
    }:
        raise ValueError("phase-receipt integration binding changed")
    changed = {
        ".stage1-worker-selftest.json",
        "Stage1_Instances/THM-M-0123/Statement.lean",
        "Stage1_Instances/THM-M-0123/check_statement.py",
        "Stage1_Instances/THM-M-0123/dependency-reuse-ledger.json",
        "Stage1_Instances/THM-M-0123/source-statement-crosswalk.md",
        "Stage1_Instances/THM-M-0123/statement-receipt.json",
        "Stage1_Instances/THM-M-0123/statement-validation.md",
        "Stage1_Instances/THM-M-0123/statement.json",
    }
    if set(receipt["changed_paths"]) != changed:
        raise ValueError("receipt changed-path inventory is stale")
    packet = load(PACKET)
    if set(packet) != {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state"
    }:
        raise ValueError("worker packet fields changed")
    if packet["item_id"] != ITEM_ID or packet["state"] != "[_]":
        raise ValueError("worker packet identity changed")
    if packet["base_revision"] != BASE_REVISION or set(packet["changed_paths"]) != changed:
        raise ValueError("worker packet base or changed paths changed")
    if packet["commands"] != receipt["selftest_result"]["commands"]:
        raise ValueError("worker packet commands differ from receipt commands")
    if not packet["known_failures"]:
        raise ValueError("worker packet omits known failures")
    for path in (
        PACKET, SOURCE, Path(__file__), STATEMENT, RECEIPT, LEDGER, VALIDATION,
        HERE / "source-statement-crosswalk.md"
    ):
        data = path.read_bytes()
        if not data.endswith(b"\n") or b"\r" in data or b"\0" in data:
            raise ValueError(f"artifact formatting changed: {path.name}")
    return expression_hash, source_hash, output_hash


def main() -> None:
    try:
        expression_hash, source_hash, output_hash = check()
    except Exception as error:
        result = semantic(
            passed=False,
            gate="S56-M-0123-STATEMENT.validator",
            message=f"Statement evidence failed closed: {error}",
        )
    else:
        result = semantic(
            passed=True,
            gate=None,
            message=(
                "Exact cohomological Mordell target, minimal imports, transports, "
                f"and four mutations passed; expression={expression_hash}; "
                f"source={source_hash}; lean_output={output_hash}."
            ),
        )
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))


def fingerprints() -> None:
    expressions, canonical_output = elaborate_expressions()
    print(
        json.dumps(
            {
                "expression_sha256": sha256_bytes(expressions[CANONICAL].encode("utf-8")),
                "lean_output_sha256": sha256_bytes(canonical_output.encode("utf-8")),
                "mutation_expression_sha256": {
                    name: sha256_bytes(expressions[name].encode("utf-8")) for name in MUTATIONS
                },
                "statement_file_sha256": sha256_bytes(SOURCE.read_bytes()),
            },
            sort_keys=True,
            separators=(",", ":"),
        )
    )


if __name__ == "__main__":
    if os.environ.get("STAGE1_FINGERPRINT_ONLY") == "1":
        fingerprints()
    else:
        main()
