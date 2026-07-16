#!/usr/bin/env python3
"""Validate the exact THM-M-0105 statement and emit one semantic result."""

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
THEOREM_ID = "THM-M-0105"
ITEM_ID = "S56-M-0105-STATEMENT"
NAMESPACE = "Stage1Instances.THM_M_0105"
CANONICAL = "RiemannRochTarget"
MUTATIONS = (
    "MutationRemovedGeometricIntegrality",
    "MutationChangedDomainToRational",
    "MutationChangedDivisorBinderScope",
    "MutationOnlyCanonicalDivisor",
)
TRANSPORTS = ("riemannRochTarget_iff_expanded",)
DIRECT_IMPORTS = (
    "Mathlib.AlgebraicGeometry.Geometrically.Integral",
    "Mathlib.AlgebraicGeometry.Morphisms.Proper",
    "Mathlib.AlgebraicGeometry.Morphisms.Smooth",
)
IMPORT_REQUIRED_NAMES = {
    DIRECT_IMPORTS[0]: "GeometricallyIntegral",
    DIRECT_IMPORTS[1]: "IsProper",
    DIRECT_IMPORTS[2]: "SmoothOfRelativeDimension",
}
GRAPH_SHA256 = "e8472863a24609e37868f215bbf0e0654b11a62f912a403ebca5feb8de5a3b9b"
CONTEXT_SHA256 = "068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c"
CONTRACT_SHA256 = "1e7adf0f4fae0541b3595d4b0bfbb53f7eb17e28a4a889fec14f6df969e0cec4"
BASE_REVISION = "1cc6aa61bb055a5c032297ee457905c849af7608"
BASE_TREE = "dc3053b55c5724ccb2e6a247e7deffebca9dbb99"
EXPECTED_EXPRESSION_SHA256 = "e69f2d70cecb6da37ea45e75b35aa3e57b175eb35b8cdf5eb4056ac141815cb2"
EXPECTED_STATEMENT_SHA256 = "2c5bb3a3e12910b1d9317fa60be408c94037388a4133759615cea0bc9454b33d"
EXPECTED_LEAN_OUTPUT_SHA256 = "529a043c7b61e5b3956aed4ab1e53ddcf4f7f87955211c62e4db6dcb25117308"
EXPECTED_ROLE_HASHES = {
    "statement_record": "4c448cd3f9178fbbb51cf7abdd582dd7a2fafa0526f8ece24447849630cefb1f",
    "statement_source": EXPECTED_STATEMENT_SHA256,
    "source_crosswalk": "a7f134d2ec20ca9f9f0cc38f730a026b23968d76a08966440fb1504336a669c5",
}
EXPECTED_ROLE_BLOBS = {
    "statement_record": "0e92ff54521b5de28a8aca9967a60d5c5e75660e",
    "statement_source": "45095fc58262b753af4a0f25f1299fc9573396b4",
    "source_crosswalk": "f59552781b653814015661b0375ebc1cb59d0cea",
}
ROLE_PATHS = {
    "statement_record": "Stage1_Instances/THM-M-0105/statement.json",
    "statement_source": "Stage1_Instances/THM-M-0105/Statement.lean",
    "source_crosswalk": "Stage1_Instances/THM-M-0105/source-statement-crosswalk.md",
}
EXPECTED_INPUT_HASHES = {
    "Docs/Stage1_Blueprint_v2.md": "fb6cd286dc5c47e22d754ab73e5162986e98a18b5bc6d8e7213ae5d39b4256d1",
    "Docs/Stage1_Blueprint_rev-5.6.md": "3779901013ac5e0b1f1b2bb4ea7a2ee08429f85bb1ee26c4b96905d6796c65c8",
    "Docs/Stage1_Phase_Acceptance_Contracts.json": CONTRACT_SHA256,
    "Docs/Stage1_Targets_rev-5.6.json": "02eec284de534dd78e1cf75f82a477ff477567dd682b7445cb7587abd137ab2c",
    "Docs/Stage1_Theorem_DAG_v2.json": GRAPH_SHA256,
    "skills/execute-stage1-rev56/SKILL.md": "5da11caafdb40b121c2fd19e13cd232a1b13a615f7a64eb314aa82cc19fea454",
    "Stage1_Instances/THM-M-0105/intake.json": "f59bb3a8fcc007f0416e28fbd24f527f80de7dd4ffa090f500119ea634d16e96",
    "Stage1_Instances/THM-M-0105/dependency-reuse-ledger.json": "6babc2bc7c6038b4a99b3ca1eae2b1ec2448229a91cbc1f4e482eef2ce39e0c7",
    "Formalizations/Lean/lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "Formalizations/Lean/lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
IMPORT_SOURCE_SHA256 = {
    DIRECT_IMPORTS[0]: "5e4eaa58838f5e1cda8ec4b2e205eb3f597c295f28cd7f4d5174fce026fcfd2b",
    DIRECT_IMPORTS[1]: "eeb5b7352df6c6af10bcce6140b41be5a15efc3c2656640d2d316409e59a96a4",
    DIRECT_IMPORTS[2]: "3918ed842c3aad02c69746032e5e202f138028c44f48089e1b408f140c9d9e20",
}
EXPECTED_CHANGED = {
    ".stage1-worker-selftest.json",
    "Stage1_Instances/THM-M-0105/Statement.lean",
    "Stage1_Instances/THM-M-0105/check_statement.py",
    "Stage1_Instances/THM-M-0105/dependency-reuse-ledger.json",
    "Stage1_Instances/THM-M-0105/source-statement-crosswalk.md",
    "Stage1_Instances/THM-M-0105/statement-receipt.json",
    "Stage1_Instances/THM-M-0105/statement-validation.md",
    "Stage1_Instances/THM-M-0105/statement.json",
}
PROHIBITED = re.compile(
    r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by|extern|run_tac)\b|"
    r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
    r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
    r"(?:axiom|constant|opaque|unsafe)\b",
    re.MULTILINE,
)


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


def git_blob_bytes(value: bytes) -> str:
    return hashlib.sha1(f"blob {len(value)}\0".encode("ascii") + value).hexdigest()


def load(path: Path) -> dict:
    def reject_duplicates(pairs: list[tuple[str, object]]) -> dict:
        result: dict[str, object] = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f"duplicate JSON key {key!r} in {path.name}")
            result[key] = value
        return result

    value = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicates)
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
        "w", suffix=".lean", encoding="utf-8",
        dir=Path(os.environ.get("TMPDIR", "/tmp")), delete=False
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
    namespace_end = f"end {NAMESPACE}"
    if source.count(marker) != 1 or source.count(namespace_end) != 1:
        raise ValueError("canonical print marker or namespace terminator is not unique")
    source = source.replace(marker, "")
    declarations = (CANONICAL,) + MUTATIONS
    dispatcher = "".join(
        "set_option pp.universes true in\n"
        "set_option pp.explicit true in\n"
        f"#print {name}\n\n" for name in declarations
    )
    result = run_text(source.replace(namespace_end, dispatcher + namespace_end))
    if result.returncode:
        raise ValueError(f"Lean expression serialization failed: {result.stdout[:500]}")
    expressions: dict[str, str] = {}
    for index, name in enumerate(declarations):
        qualified = re.escape(f"{NAMESPACE}.{name}")
        next_prefix = (
            rf"\ndef {re.escape(f'{NAMESPACE}.{declarations[index + 1]}')}"
            if index + 1 < len(declarations) else r"\Z"
        )
        match = re.search(
            rf"def {qualified}(?:\.\{{[^\n]*\}})? : Prop :=\n(?P<body>.*?){next_prefix}",
            result.stdout,
            re.DOTALL,
        )
        if match is None:
            raise ValueError(f"explicit expression unavailable for {name}")
        expressions[name] = match.group("body").strip()
    canonical_output = result.stdout.split(
        f"def {NAMESPACE}.{MUTATIONS[0]}", 1
    )[0].rstrip() + "\n"
    return expressions, canonical_output


def check_import_minimality(source: str) -> None:
    for imported, required_name in IMPORT_REQUIRED_NAMES.items():
        result = run_text(source.replace(f"import {imported}\n", "", 1))
        if result.returncode == 0 or required_name not in result.stdout:
            raise ValueError(f"direct import deletion did not fail on {required_name}")


def require_pointer(record: dict, pointer: str) -> None:
    current: object = record
    for part in pointer.lstrip("/").split("/"):
        if not isinstance(current, dict) or part not in current:
            raise ValueError(f"receipt lacks contract field {pointer}")
        current = current[part]


def check() -> tuple[str, str, str]:
    source_text = SOURCE.read_text(encoding="utf-8")
    if PROHIBITED.search(source_text):
        raise ValueError("statement source contains a prohibited construct")
    imports = tuple(re.findall(r"^import ([^\s]+)$", source_text, re.MULTILINE))
    if imports != DIRECT_IMPORTS:
        raise ValueError("direct imports changed")

    head = subprocess.run(
        ["git", "rev-parse", "HEAD", "HEAD^{tree}"], cwd=ROOT,
        text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True
    ).stdout.splitlines()
    if head != [BASE_REVISION, BASE_TREE]:
        raise ValueError("worker base revision or tree changed")
    for relative, expected in EXPECTED_INPUT_HASHES.items():
        if sha256_bytes((ROOT / relative).read_bytes()) != expected:
            raise ValueError(f"authority or support input changed: {relative}")

    targets = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM_ID)
    if target["execution_rank"] != 27 or target["lifecycle_mode"] != "planned":
        raise ValueError("target manifest identity changed")
    blueprint = (ROOT / "Docs/Stage1_Blueprint_v2.md").read_text(encoding="utf-8")
    if re.search(
        r"^- \[ \] `S56-M-0105-STATEMENT` / `THM-M-0105` / `statement`:.*\n"
        r"  Depends: `S56-M-0105-INTAKE`\. Owned paths: `Stage1_Instances/THM-M-0105`\.",
        blueprint, re.MULTILINE
    ) is None:
        raise ValueError("authoritative v2 statement row changed")

    dag = load(ROOT / "Docs/Stage1_Theorem_DAG_v2.json")
    node = next(row for row in dag["theorems"] if row["theorem_id"] == THEOREM_ID)
    if node["v2_execution_rank"] != 264 or node["topological_layer"] != 0:
        raise ValueError("v2 claim order changed")
    if node["phase_states"]["statement"] != "[ ]" or node["dependency_context_sha256"] != CONTEXT_SHA256:
        raise ValueError("v2 phase state or dependency context changed")
    for field in (
        "direct_hard_parents", "transitive_hard_ancestors",
        "direct_reuse_hint_ids", "shared_lemma_group_ids"
    ):
        if node[field] != []:
            raise ValueError(f"declared empty dependency field changed: {field}")

    contract = load(ROOT / "Docs/Stage1_Phase_Acceptance_Contracts.json")
    phase = next(row for row in contract["phases"] if row["phase"] == "statement")
    selected = {}
    for role in phase["required_artifact_roles"]:
        candidates = [
            path.format(theorem_id=THEOREM_ID) for path in role["path_candidates"]
            if (ROOT / path.format(theorem_id=THEOREM_ID)).is_file()
        ]
        if len(candidates) != 1:
            raise ValueError(f"role {role['role']} is missing or ambiguous")
        selected[role["role"]] = candidates[0]
    if selected != {**ROLE_PATHS, "phase_receipt": "Stage1_Instances/THM-M-0105/statement-receipt.json"}:
        raise ValueError("statement artifact-role selection changed")
    validators = [
        row["path_pattern"].format(theorem_id=THEOREM_ID)
        for row in phase["validator_candidates"]
        if (ROOT / row["path_pattern"].format(theorem_id=THEOREM_ID)).is_file()
    ]
    if validators != ["Stage1_Instances/THM-M-0105/check_statement.py"]:
        raise ValueError("validator selection is not exactly one declared candidate")

    ledger = load(LEDGER)
    if ledger["schema_version"] != "stage1-dependency-reuse-ledger/1.1":
        raise ValueError("dependency ledger schema changed")
    if ledger["consumer_theorem_id"] != THEOREM_ID or ledger["observed_theorem_dag_sha256"] != GRAPH_SHA256:
        raise ValueError("dependency ledger identity or graph binding changed")
    if ledger["dependency_context_sha256"] != CONTEXT_SHA256 or ledger["repository_revision"] != BASE_REVISION:
        raise ValueError("dependency ledger context or revision changed")
    for field in (
        "direct_parent_ids", "transitive_ancestor_ids", "hard_edge_ids",
        "reuse_hint_ids", "shared_group_ids", "inspections", "reuse_decisions",
        "unresolved_compatibility_obligations"
    ):
        if ledger[field] != []:
            raise ValueError(f"empty dependency ledger field changed: {field}")
    if ledger["closure_audit"]["parent_inspection_order"] != []:
        raise ValueError("empty parent inspection order changed")
    if ledger["claim_order"] != {
        "v2_execution_rank": 264,
        "phase_layer": 1,
        "phase_item_id": ITEM_ID,
    }:
        raise ValueError("ledger claim order changed")

    expressions, canonical_output = elaborate_expressions()
    if len(set(expressions.values())) != len(expressions):
        raise ValueError("a required mutation has the canonical expression")
    check_import_minimality(source_text)
    for name in TRANSPORTS:
        if re.search(rf"^theorem {name}\b", source_text, re.MULTILINE) is None:
            raise ValueError(f"checked transport missing: {name}")
    axiom_line = (
        "'Stage1Instances.THM_M_0105.riemannRochTarget_iff_expanded' depends on axioms: "
        "[propext, Classical.choice, Quot.sound]"
    )
    if axiom_line not in canonical_output.splitlines() or "sorryAx" in canonical_output:
        raise ValueError("checked transport axiom boundary changed")

    expression_hash = sha256_bytes(expressions[CANONICAL].encode("utf-8"))
    source_hash = sha256_bytes(SOURCE.read_bytes())
    output_hash = sha256_bytes(canonical_output.encode("utf-8"))
    for label, expected, actual in (
        ("expression", EXPECTED_EXPRESSION_SHA256, expression_hash),
        ("statement source", EXPECTED_STATEMENT_SHA256, source_hash),
        ("Lean output", EXPECTED_LEAN_OUTPUT_SHA256, output_hash),
    ):
        if expected != "TO_BE_RECONCILED" and expected != actual:
            raise ValueError(f"{label} fingerprint changed")

    statement = load(STATEMENT)
    receipt = load(RECEIPT)
    formal = statement["canonical_formal_target"]
    if formal["elaborated_expression_sha256"] != expression_hash or formal["statement_file_sha256"] != source_hash:
        raise ValueError("statement fingerprints are stale")
    if statement["direct_imports"] != list(DIRECT_IMPORTS):
        raise ValueError("statement import inventory is stale")
    if receipt["statement_fingerprints"] != [f"sha256:{expression_hash}"]:
        raise ValueError("receipt expression fingerprint is stale")
    if receipt["statement_file_sha256"] != source_hash or receipt["lean_output_sha256"] != output_hash:
        raise ValueError("receipt source or Lean-output fingerprint is stale")
    if receipt["base_revision"] != BASE_REVISION or receipt["base_tree"] != BASE_TREE:
        raise ValueError("receipt base binding changed")
    if receipt["schema_version"] != "stage1-node-receipt/1.0" or receipt["intent"] != "audit":
        raise ValueError("receipt schema or intent changed")
    if receipt["accepted"] is not False or receipt["proposed_state"] != "[_]" or receipt["verdict"] != "accepted":
        raise ValueError("receipt worker/master boundary changed")
    if receipt["selftest_status"] != "passed" or receipt["selftest_result"]["exit_code"] != 0:
        raise ValueError("receipt self-test status changed")
    if receipt["audit_complete"] is not False or receipt["theorem_complete"] is not False:
        raise ValueError("receipt overclaims a terminal state")
    for pointer in set(contract["artifact_resolution"]["worker_phase_receipt_required_fields"]) | set(phase["phase_receipt_required_fields"]):
        require_pointer(receipt, pointer)
    for relative, tagged in receipt["inputs"].items():
        algorithm, expected = tagged.split(":", 1)
        if algorithm != "sha256" or sha256_bytes((ROOT / relative).read_bytes()) != expected:
            raise ValueError(f"receipt input binding is stale: {relative}")
    if receipt["import_source_sha256"] != IMPORT_SOURCE_SHA256:
        raise ValueError("import source inventory changed")
    mathlib = LEAN_DIR / ".lake/packages/mathlib"
    for module, expected in IMPORT_SOURCE_SHA256.items():
        path = mathlib / (module.replace(".", "/") + ".lean")
        if sha256_bytes(path.read_bytes()) != expected:
            raise ValueError(f"import source changed: {module}")

    bindings = receipt["artifact_bindings"]
    if {row["role"] for row in bindings} != set(ROLE_PATHS) or len(bindings) != 3:
        raise ValueError("receipt selected-role bindings are incomplete")
    for row in bindings:
        data = (ROOT / row["path"]).read_bytes()
        if row["path"] != ROLE_PATHS[row["role"]]:
            raise ValueError(f"receipt role path changed: {row['role']}")
        if row["sha256"] != sha256_bytes(data) or row["git_blob"] != git_blob_bytes(data):
            raise ValueError(f"receipt role binding is stale: {row['role']}")
    if receipt["phase_receipt_self_binding"] != {
        "role": "phase_receipt",
        "path": "Stage1_Instances/THM-M-0105/statement-receipt.json",
        "binding_kind": "git_object_at_integration",
        "expected_sha256": None,
        "expected_git_blob": None,
        "status": "deferred_to_scheduler_master_lane_after_HEAD_tracking",
    }:
        raise ValueError("phase receipt self-binding changed")

    packet = load(PACKET)
    if set(packet) != {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state"
    }:
        raise ValueError("worker packet fields changed")
    if packet["item_id"] != ITEM_ID or packet["state"] != "[_]" or packet["base_revision"] != BASE_REVISION:
        raise ValueError("worker packet identity changed")
    if set(packet["changed_paths"]) != EXPECTED_CHANGED or set(receipt["changed_paths"]) != EXPECTED_CHANGED:
        raise ValueError("changed-path inventory is stale")
    if packet["commands"] != receipt["selftest_result"]["commands"]:
        raise ValueError("worker packet commands differ from receipt commands")
    if packet["known_failures"] != receipt["known_failures"]:
        raise ValueError("worker packet failures differ from receipt failures")
    for path in (PACKET, SOURCE, Path(__file__), STATEMENT, RECEIPT, LEDGER, VALIDATION, HERE / "source-statement-crosswalk.md"):
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
            gate="S56-M-0105-STATEMENT.validator",
            message=f"Statement evidence failed closed: {error}",
        )
    else:
        result = semantic(
            passed=True,
            gate=None,
            message=(
                "Exact algebraic-curve Riemann-Roch target, minimal imports, transport, "
                f"and four mutations passed; expression={expression_hash}; "
                f"source={source_hash}; lean_output={output_hash}."
            ),
        )
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))


def fingerprints() -> None:
    expressions, canonical_output = elaborate_expressions()
    print(json.dumps({
        "expression_sha256": sha256_bytes(expressions[CANONICAL].encode("utf-8")),
        "lean_output_sha256": sha256_bytes(canonical_output.encode("utf-8")),
        "mutation_expression_sha256": {
            name: sha256_bytes(expressions[name].encode("utf-8")) for name in MUTATIONS
        },
        "statement_file_sha256": sha256_bytes(SOURCE.read_bytes()),
    }, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    if os.environ.get("STAGE1_FINGERPRINT_ONLY") == "1":
        fingerprints()
    else:
        main()
