#!/usr/bin/env python3
"""Fail-closed semantic validator for S56-M-0108-STATEMENT."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0108"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
WORKER_PACKET = ROOT / ".stage1-worker-selftest.json"
ITEM_ID = "S56-M-0108-STATEMENT"
THEOREM_ID = "THM-M-0108"
PHASE = "statement"
BASE_REVISION = "2dc5a410b68eff806858fd6ed0cb33d57f6209f7"
BASE_TREE = "841bdd6114e7436cff4a3a1ff248fc1e884a9ddc"
GRAPH_SHA256 = "3d32f808e2914b338c459d52651b69731f0979a90a720f98bc0f31a577e2bafa"
CONTEXT_SHA256 = "068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c"
CONTRACT_SHA256 = "1e7adf0f4fae0541b3595d4b0bfbb53f7eb17e28a4a889fec14f6df969e0cec4"
SOURCE_SHA256 = "cbe8852abcc4d3fe4ed87be2fcdcec848b72c9041df017fbc7d9b4cd09b39c59"
EXPECTED_EXPRESSION_SHA256 = "32fabc4d6654c80d342bc7705594dddae1d3e4836404d62075eb56e859978789"
MUTATIONS = {
    "mutationRemovedClosedness": "removed_hypothesis",
    "mutationChangedDomain": "changed_domain",
    "mutationChangedBinderScope": "changed_binder_scope",
    "mutationExcludedDimensionZero": "boundary_case",
}
EXPECTED_PINS = {
    "lean_toolchain": "leanprover/lean4:v4.29.0",
    "mathlib_revision": "8a178386ffc0f5fef0b77738bb5449d50efeea95",
    "mathlib_tree": "bdc39a3123201dae413a9d9be56ec242c19e5c2b",
    "lean_toolchain_sha256":
        "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "lake_manifest_sha256":
        "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
    "lean_sha256":
        "3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf",
    "lake_sha256":
        "a608ff084d7e2af228b92a29d7c2fd083ba0580e46889175ec74a81678c98359",
}
DIRECT_IMPORTS = [
    "Mathlib.Analysis.Complex.Basic",
    "Mathlib.Analysis.Analytic.Basic",
    "Mathlib.LinearAlgebra.Projectivization.Basic",
    "Mathlib.RingTheory.MvPolynomial.Homogeneous",
]
DIRECT_IMPORT_SHA256 = {
    "Mathlib.Analysis.Complex.Basic":
        "2233a892e4a9cbdc9250806652511d921b081773edf6f33e94e5652bb49f1b93",
    "Mathlib.Analysis.Analytic.Basic":
        "2ff8b93f0a0d8978f813534dfc2a8ba94cc4dc59b3b12180921cebfccc712f30",
    "Mathlib.LinearAlgebra.Projectivization.Basic":
        "9fe7a41a1a504d078c18d0104ba13af39234376bf5c9b5a6c51e776287db4f04",
    "Mathlib.RingTheory.MvPolynomial.Homogeneous":
        "3369737ba24d5916f243a07296bb31dfe03fbc26d5564ed8abc0ce11140a193c",
}
ROLE_PATHS = {
    "statement_record": "Stage1_Instances/THM-M-0108/statement.json",
    "statement_source": "Stage1_Instances/THM-M-0108/Statement.lean",
    "source_crosswalk": "Stage1_Instances/THM-M-0108/source_statement_crosswalk.md",
    "phase_receipt": "Stage1_Instances/THM-M-0108/statement-receipt.json",
}
RECEIPT_INPUT_PATHS = {
    **{role: path for role, path in ROLE_PATHS.items() if role != "phase_receipt"},
    "dependency_reuse_ledger":
        "Stage1_Instances/THM-M-0108/dependency-reuse-ledger.json",
    "validator": "Stage1_Instances/THM-M-0108/check_statement.py",
}
SUPPORTING_PATHS = [
    "Stage1_Instances/THM-M-0108/README.md",
    "Stage1_Instances/THM-M-0108/scope.md",
    "Stage1_Instances/THM-M-0108/validation.md",
]
AUTHORITY_PATHS = [
    "Docs/Stage1_Blueprint_v2.md",
    "Docs/Stage1_Blueprint_rev-5.6.md",
    "Docs/Stage1_Phase_Acceptance_Contracts.json",
    "Docs/Stage1_Theorem_DAG_v2.json",
    "skills/execute-stage1-rev56/SKILL.md",
]
CHANGED_PATHS = [
    ".stage1-worker-selftest.json",
    "Stage1_Instances/THM-M-0108/README.md",
    "Stage1_Instances/THM-M-0108/Statement.lean",
    "Stage1_Instances/THM-M-0108/check_statement.py",
    "Stage1_Instances/THM-M-0108/dependency-reuse-ledger.json",
    "Stage1_Instances/THM-M-0108/scope.md",
    "Stage1_Instances/THM-M-0108/source_statement_crosswalk.md",
    "Stage1_Instances/THM-M-0108/statement-receipt.json",
    "Stage1_Instances/THM-M-0108/statement.json",
    "Stage1_Instances/THM-M-0108/validation.md",
]
EXACT_SEMANTIC_FIELDS = {
    "schema_version", "item_id", "theorem_id", "phase", "status", "verdict",
    "phase_accepted", "audit_complete", "theorem_complete",
    "phase_predicate_proven", "first_failed_gate", "open_obligations",
    "stale_inputs", "blocked", "message",
}
PROHIBITED = re.compile(
    r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by|extern|run_tac)\b|"
    r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
    r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
    r"(?:axiom|constant|opaque|unsafe)\b",
    flags=re.MULTILINE,
)


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def git_blob(path: Path) -> str:
    value = path.read_bytes()
    return hashlib.sha1(f"blob {len(value)}\0".encode("ascii") + value).hexdigest()


def load_json(path: Path) -> dict:
    def reject_duplicates(pairs: list[tuple[str, object]]) -> dict:
        value: dict[str, object] = {}
        for key, child in pairs:
            if key in value:
                raise AssertionError(f"duplicate JSON key {key!r} in {path.name}")
            value[key] = child
        return value

    value = json.loads(
        path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicates
    )
    if not isinstance(value, dict):
        raise AssertionError(f"{path.name} is not a JSON object")
    return value


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def git(*argv: str) -> str:
    result = subprocess.run(
        ["git", *argv], cwd=ROOT, text=True, capture_output=True, timeout=30
    )
    require(result.returncode == 0, f"git {' '.join(argv)} failed")
    return result.stdout.strip()


def pinned_lake() -> Path:
    elan = shutil.which("elan")
    require(elan is not None, "elan is unavailable for pinned toolchain discovery")
    elan_root = Path(elan).resolve().parent.parent
    lake = elan_root / "toolchains" / "leanprover--lean4---v4.29.0" / "bin" / "lake"
    require(lake.is_file() and not lake.is_symlink(), "pinned Lake executable missing")
    return lake


def lean_environment(lake: Path) -> dict[str, str]:
    return {
        "ELAN_TOOLCHAIN": EXPECTED_PINS["lean_toolchain"],
        "LC_ALL": "C",
        "PATH": f"{lake.parent}:/usr/bin:/bin",
        "TZ": "UTC",
    }


def elaborate(source: Path, lake: Path) -> str:
    environment = {"LC_ALL": "C", "TZ": "UTC"}
    environment.update(lean_environment(lake))
    result = subprocess.run(
        [str(lake), "env", "lean", str(source)],
        cwd=LEAN_ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=180,
        env=environment,
    )
    require(result.returncode == 0, f"Lean elaboration failed: {result.stdout}{result.stderr}")
    require("sorryAx" not in result.stdout, "Lean output reports sorryAx")
    return result.stdout


def printed_declarations(output: str) -> dict[str, str]:
    markers = ["ChowTheoremTarget", *MUTATIONS]
    starts: list[tuple[int, str]] = []
    for name in markers:
        marker = f"def Stage1Instances.THMM0108.{name} : Prop :=\n"
        offset = output.find(marker)
        require(offset >= 0, f"Lean output omits {name}")
        starts.append((offset, name))
    starts.sort()
    result: dict[str, str] = {}
    for index, (offset, name) in enumerate(starts):
        end = starts[index + 1][0] if index + 1 < len(starts) else output.find(
            "'Stage1Instances.THMM0108.ChowTheoremTarget' depends", offset
        )
        require(end > offset, f"could not delimit {name}")
        result[name] = output[offset:end].rstrip() + "\n"
    return result


def validate() -> dict[str, str]:
    source = HERE / "Statement.lean"
    record = load_json(HERE / "statement.json")
    receipt = load_json(HERE / "statement-receipt.json")
    contract = load_json(ROOT / "Docs/Stage1_Phase_Acceptance_Contracts.json")
    dag = load_json(ROOT / "Docs/Stage1_Theorem_DAG_v2.json")
    ledger = load_json(HERE / "dependency-reuse-ledger.json")
    packet = load_json(WORKER_PACKET)
    lake = pinned_lake()

    require(git("rev-parse", "HEAD") == BASE_REVISION, "repository revision drift")
    require(git("rev-parse", "HEAD^{tree}") == BASE_TREE, "repository tree drift")
    require(sha256(ROOT / "Docs/Stage1_Phase_Acceptance_Contracts.json") == CONTRACT_SHA256,
            "phase contract drift")
    require(sha256(ROOT / "Docs/Stage1_Theorem_DAG_v2.json") == GRAPH_SHA256,
            "theorem DAG drift")
    require(sha256(source) == SOURCE_SHA256, "statement source drift")

    node = next(row for row in dag["theorems"] if row["theorem_id"] == THEOREM_ID)
    require(node["v2_execution_rank"] == 267, "v2 execution rank drift")
    require(node["phase_states"]["intake"] == "[_]", "intake state drift")
    require(node["phase_states"][PHASE] == "[ ]", "statement state drift")
    require(node["dependency_context_sha256"] == CONTEXT_SHA256, "context drift")
    for field in (
        "direct_hard_parents", "transitive_hard_ancestors",
        "direct_reuse_hint_ids", "shared_lemma_group_ids",
    ):
        require(node[field] == [], f"nonempty dependency context at {field}")

    require(ledger["schema_version"] == "stage1-dependency-reuse-ledger/1.1",
            "dependency ledger schema drift")
    require(ledger["observed_theorem_dag_sha256"] == GRAPH_SHA256,
            "dependency ledger graph drift")
    require(ledger["dependency_context_sha256"] == CONTEXT_SHA256,
            "dependency ledger context drift")
    require(ledger["repository_revision"] == BASE_REVISION,
            "dependency ledger revision drift")
    for field in (
        "direct_parent_ids", "transitive_ancestor_ids", "hard_edge_ids",
        "reuse_hint_ids", "shared_group_ids", "inspections", "reuse_decisions",
        "unresolved_compatibility_obligations",
    ):
        require(ledger[field] == [], f"dependency ledger field {field} is not empty")

    phase_row = next(row for row in contract["phases"] if row["phase"] == PHASE)
    selected_roles: dict[str, str] = {}
    for role in phase_row["required_artifact_roles"]:
        candidates = [
            path.format(theorem_id=THEOREM_ID)
            for path in role["path_candidates"]
            if (ROOT / path.format(theorem_id=THEOREM_ID)).is_file()
        ]
        require(len(candidates) == 1,
                f"role {role['role']} has {len(candidates)} candidates")
        selected_roles[role["role"]] = candidates[0]
    require(selected_roles == ROLE_PATHS, "statement artifact role resolution drift")
    validator_candidates = [
        row["path_pattern"].format(theorem_id=THEOREM_ID)
        for row in phase_row["validator_candidates"]
        if (ROOT / row["path_pattern"].format(theorem_id=THEOREM_ID)).is_file()
    ]
    require(validator_candidates == [RECEIPT_INPUT_PATHS["validator"]],
            "validator candidate selection is missing or ambiguous")

    required_fields = phase_row["phase_receipt_required_fields"]
    for pointer in required_fields:
        value: object = receipt
        for component in pointer.removeprefix("/").split("/"):
            require(isinstance(value, dict) and component in value,
                    f"receipt omits {pointer}")
            value = value[component]
    require(receipt["schema_version"] == "stage1-node-receipt/1.0",
            "receipt schema drift")
    require(receipt["item_id"] == ITEM_ID and receipt["theorem_id"] == THEOREM_ID,
            "receipt identity drift")
    require(receipt["phase"] == PHASE and receipt["intent"] == "audit",
            "receipt phase or intent drift")
    require(receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE,
            "receipt base drift")
    require(receipt["proposed_state"] == "[_]" and receipt["accepted"] is False,
            "worker receipt transfers acceptance")
    require(receipt["verdict"] == "no_state_change", "worker verdict drift")
    require(receipt["selftest_status"] == "passed", "receipt self-test not passed")
    require(receipt["selftest_result"]["exit_code"] == 0
            and receipt["selftest_result"]["commands"], "receipt commands missing")
    require(receipt["audit_complete"] is False and receipt["theorem_complete"] is False,
            "receipt overclaims terminal completion")
    require(packet["item_id"] == ITEM_ID and packet["state"] == "[_]",
            "worker packet identity or state drift")
    require(packet["base_revision"] == BASE_REVISION, "worker packet base drift")
    require(packet["changed_paths"] == CHANGED_PATHS,
            "worker packet changed-path coverage drift")
    require(packet["commands"] == receipt["selftest_result"]["commands"],
            "worker packet command record drift")
    require(packet["known_failures"] == receipt["known_failures"],
            "worker packet known-failure record drift")
    tracked_delta = set(git("diff", "--name-only", "HEAD", "--", ".").splitlines())
    untracked_delta = set(git("ls-files", "--others", "--exclude-standard").splitlines())
    status_paths = tracked_delta | untracked_delta
    require(status_paths == set(CHANGED_PATHS) | {"Formalizations/Lean/.lake"},
            "worker packet does not cover the scoped worktree delta")
    bindings = receipt["artifact_bindings"]
    require(set(bindings) == set(ROLE_PATHS), "receipt artifact binding roles drift")
    for role, relative in ROLE_PATHS.items():
        binding = bindings[role]
        require(binding["role"] == role and binding["path"] == relative,
                f"receipt artifact identity drift for {role}")
        if role == "phase_receipt":
            require(binding["sha256"] == "self_referential_excluded"
                    and binding["git_blob"] == "self_referential_excluded",
                    "phase receipt does not declare its self-binding boundary")
        else:
            path = ROOT / relative
            require(binding["sha256"] == sha256(path),
                    f"receipt artifact SHA drift for {role}")
            require(binding["git_blob"] == git_blob(path),
                    f"receipt artifact Git blob drift for {role}")
    for role, relative in RECEIPT_INPUT_PATHS.items():
        binding = receipt["inputs"][role]
        require(binding["path"] == relative, f"receipt input path drift for {role}")
        require(binding["sha256"] == sha256(ROOT / relative),
                f"receipt input SHA drift for {role}")
        require(binding["git_blob"] == git_blob(ROOT / relative),
                f"receipt input Git blob drift for {role}")
    supporting = receipt["inputs"]["supporting_surfaces"]
    require([row["path"] for row in supporting] == SUPPORTING_PATHS,
            "receipt supporting surface set or order drift")
    for binding in supporting:
        path = ROOT / binding["path"]
        require(binding["sha256"] == sha256(path),
                f"receipt supporting SHA drift for {binding['path']}")
        require(binding["git_blob"] == git_blob(path),
                f"receipt supporting Git blob drift for {binding['path']}")
    authorities = receipt["inputs"]["authorities"]
    require([row["path"] for row in authorities] == AUTHORITY_PATHS,
            "receipt authority set or order drift")
    for binding in authorities:
        path = ROOT / binding["path"]
        require(binding["sha256"] == sha256(path),
                f"receipt authority SHA drift for {binding['path']}")
        require(binding["git_blob"] == git("rev-parse", f"HEAD:{binding['path']}"),
                f"receipt authority Git blob drift for {binding['path']}")

    require(record["schema_version"] == "stage1-statement/1.0",
            "statement record schema drift")
    require(record["item_id"] == ITEM_ID and record["theorem_id"] == THEOREM_ID,
            "statement record identity drift")
    require(record["canonical_formal_target"]["declaration_or_expression"]
            == "Stage1Instances.THMM0108.ChowTheoremTarget", "target declaration drift")
    require(record["direct_imports"] == DIRECT_IMPORTS, "direct import record drift")
    require(record["statement_elaborated"] is True
            and record["theorem_proved"] is False
            and record["theorem_complete"] is False, "statement boundary drift")

    source_text = source.read_text(encoding="utf-8")
    require(PROHIBITED.search(source_text) is None, "prohibited Lean construct found")
    actual_imports = [
        line.removeprefix("import ").strip()
        for line in source_text.splitlines() if line.startswith("import ")
    ]
    require(actual_imports == DIRECT_IMPORTS, "direct imports are not exact")

    output = elaborate(source, lake)
    expressions = printed_declarations(output)
    fingerprints = {name: sha256_bytes(value.encode()) for name, value in expressions.items()}
    require(fingerprints["ChowTheoremTarget"] == EXPECTED_EXPRESSION_SHA256,
            "canonical expression fingerprint drift")
    require(len(set(fingerprints.values())) == len(fingerprints),
            "a non-equivalent mutation survived expression identity")
    require(record["canonical_formal_target"]["elaborated_expression_sha256"]
            == fingerprints["ChowTheoremTarget"], "record expression hash drift")
    require(receipt["statement_fingerprints"]
            == [f"sha256:{fingerprints['ChowTheoremTarget']}"],
            "receipt statement fingerprint drift")
    receipt_mutations = {row["declaration"]: row for row in receipt["mutation_tests"]}
    require(set(receipt_mutations) == set(MUTATIONS), "receipt mutation set drift")
    for declaration, kind in MUTATIONS.items():
        row = receipt_mutations[declaration]
        require(row["kind"] == kind, f"mutation class drift for {declaration}")
        require(row["expression_sha256"] == fingerprints[declaration],
                f"mutation fingerprint drift for {declaration}")

    manifest = load_json(LEAN_ROOT / "lake-manifest.json")
    mathlib_revision = next(
        row["rev"] for row in manifest["packages"] if row["name"] == "mathlib"
    )
    require((LEAN_ROOT / "lean-toolchain").read_text().strip()
            == EXPECTED_PINS["lean_toolchain"], "Lean toolchain drift")
    require(sha256(LEAN_ROOT / "lean-toolchain")
            == EXPECTED_PINS["lean_toolchain_sha256"], "Lean toolchain file drift")
    require(sha256(LEAN_ROOT / "lake-manifest.json")
            == EXPECTED_PINS["lake_manifest_sha256"], "Lake manifest drift")
    require(mathlib_revision == EXPECTED_PINS["mathlib_revision"], "mathlib pin drift")
    require(lake.is_file() and not lake.is_symlink(), "pinned Lake executable missing")
    require(sha256(lake) == EXPECTED_PINS["lake_sha256"], "pinned Lake bytes drift")
    lean = lake.with_name("lean")
    require(lean.is_file() and sha256(lean) == EXPECTED_PINS["lean_sha256"],
            "pinned Lean bytes drift")
    mathlib = (LEAN_ROOT / ".lake" / "packages" / "mathlib").resolve()
    require(mathlib.is_dir(), "canonical pinned mathlib artifacts missing")
    require(git("-C", str(mathlib), "rev-parse", "HEAD")
            == EXPECTED_PINS["mathlib_revision"], "materialized mathlib revision drift")
    require(git("-C", str(mathlib), "rev-parse", "HEAD^{tree}")
            == EXPECTED_PINS["mathlib_tree"], "materialized mathlib tree drift")
    require(git("-C", str(mathlib), "status", "--porcelain=v1", "--untracked-files=no")
            == "", "materialized mathlib source is dirty")
    for name, expected in DIRECT_IMPORT_SHA256.items():
        path = mathlib / (name.replace(".", "/") + ".lean")
        require(sha256(path) == expected, f"direct import source drift: {name}")

    for index in range(len(DIRECT_IMPORTS)):
        reduced = [name for i, name in enumerate(DIRECT_IMPORTS) if i != index]
        candidate = re.sub(
            r"(?:^import .*\n){4}",
            "".join(f"import {name}\n" for name in reduced),
            source_text,
            count=1,
            flags=re.MULTILINE,
        )
        with tempfile.NamedTemporaryFile(
            "w", suffix=".lean", dir="/tmp", encoding="utf-8", delete=False
        ) as handle:
            handle.write(candidate)
            temporary = Path(handle.name)
        try:
            environment = lean_environment(lake)
            result = subprocess.run(
                [str(lake), "env", "lean", str(temporary)], cwd=LEAN_ROOT,
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=180,
                env=environment,
            )
        finally:
            temporary.unlink()
        require(result.returncode != 0,
                f"direct import is redundant: {DIRECT_IMPORTS[index]}")
    return fingerprints


def semantic_result(*, passed: bool, message: str) -> dict:
    result = {
        "schema_version": "stage1-validator-semantic-result/1.0",
        "item_id": ITEM_ID,
        "theorem_id": THEOREM_ID,
        "phase": PHASE,
        "status": "passed" if passed else "failed",
        "verdict": "phase_accepted" if passed else "repair_required",
        "phase_accepted": passed,
        "audit_complete": False,
        "theorem_complete": False,
        "phase_predicate_proven": passed,
        "first_failed_gate": None if passed else "STATEMENT-SEMANTIC-CHECK",
        "open_obligations": 0 if passed else 1,
        "stale_inputs": [],
        "blocked": False,
        "message": message,
    }
    require(set(result) == EXACT_SEMANTIC_FIELDS,
            "validator semantic result field set drift")
    return result


def main() -> int:
    try:
        fingerprints = validate()
    except Exception as exc:
        print(json.dumps(semantic_result(passed=False, message=str(exc)), sort_keys=True))
        return 1
    print(json.dumps(semantic_result(
        passed=True,
        message=(
            "S01-S03 proven: exact reduced-carrier Chow target elaborated at "
            f"{fingerprints['ChowTheoremTarget']}; all four structural mutations "
            "are distinct and each direct import is necessary."
        ),
    ), sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
