#!/usr/bin/env python3
"""Fail-closed release reconciliation for S56-M-0318-RELEASE."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import pwd
import re
import subprocess
import tempfile


if not __debug__:
    raise SystemExit("release validation requires Python assertions")

ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0318"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
ITEM = "S56-M-0318-RELEASE"
THEOREM = "THM-M-0318"
BASE_REVISION = "63a9ed9c4aae594da31423142b0658129d5452a7"
BASE_TREE = "7bee4fac4489bad36fd615a023df13bb294d1781"
ROOT_VECTOR = {"H": "H2", "M": "M3", "R": "R4"}
TARGET_EXPRESSION_SHA256 = (
    "2605ac76f3d50dddcc135d3094639fbed3de58a10b26a8f9eeb504101e556b5f"
)
INVENTORY_SHA256 = (
    "57d77a8fccc8308a704f1185c92057a17791da515e45325179aa81d000376f87"
)
VALIDATION_RECEIPT_SHA256 = (
    "a2d34f849f47c9b0069d869faaed70cb5b4ccc5996f47fc3cbb657df41c11ef0"
)
PROOF_RECEIPT_SHA256 = (
    "fbea33158e266f23b698be1664d0296db436310f9f7c4bdf5b0fb28b6b43c0d4"
)
TOOLCHAIN = "leanprover/lean4:v4.29.0"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
LEAN_SHA256 = "3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
INVENTORY_IDS = [
    "M0318-ROOT", "M0318-S", "M0318-S-TRANSPORT", "M0318-C",
    "M0318-C-NET", "M0318-C-MAP", "M0318-B-BROUWER",
    "M0318-L-APPROX", "M0318-L-LIMIT", "M0318-L-CONT",
    "M0318-X-TRUST", "M0318-T-COMPOSE",
]
FROZEN_OPEN_CUT = [
    "THM-M-0318-C-NET", "THM-M-0318-C-MAP",
    "THM-M-0318-B-BROUWER", "THM-M-0318-L-LIMIT",
    "THM-M-0318-L-CONT",
]
PROOF_DECLARATIONS = (
    "IndexedLOrder.Scarf",
    "IndexedLOrder.GiComponentStructure_holds",
    "Brouwer",
    "Stage1Instances.THM_M_0318.exists_simplex_approximation",
    "Stage1Instances.THM_M_0318.hasApproximateFixedPoints",
    "Stage1Instances.THM_M_0318.approximationEngine",
    "Stage1Instances.THM_M_0318.compactLimitEngine",
    "Stage1Instances.THM_M_0318.exactSchauderTarget",
    "Stage1Instances.THM_M_0318.schauderFixedPoint",
)
VALIDATION_DECLARATIONS = (
    "IndexedLOrder.Scarf",
    "IndexedLOrder.GiComponentStructure_holds",
    "Brouwer",
    "Stage1Instances.THM_M_0318.Validation.validationSimplexApproximation",
    "Stage1Instances.THM_M_0318.Validation.schauderFixedPoint_validation",
)
EXPECTED_INPUTS = {
    "README.md": "0173cb1ff3297cc34cd8bc6883428ba8d7cb50b8d562d6d8e48db815f57d6243",
    "instance.json": "2b568fdf6949c4ddf79c08c41df406e34fb2d48ebff4efd7668972b3f7bdc401",
    "task-dag.json": "c8039a55c6c1e3a5c9eac3d50672add2c7059e1591af3978d614a77903b054f1",
    "Statement.lean": "e428904e22f39e9dd3b2283c1155ade8c1df09b40d1a15052e3dd4ca71b2912d",
    "ObligationTree.lean": "623fa1763a74dc4c88bb72617d27a8173b3642cb450a019aeba88a8b41946fd7",
    "Proof.lean": "c8dfef2073737c4a71c0b3866de79fc2ff1276c82ae17c7f809e5fce0eca5602",
    "Validation.lean": "f4f7dfebc40776d7114bf28ff2391bfd19721cadffb095b71549cc474d0bc621",
    "statement.json": "3747826c9a83a687ecbfaff3b8580124b4e8ee37e53b1647582eb08ff9b8a467",
    "obligation-registry.json": "d4c5634e3dbb15243dfe056f870d9901119785af7220cabc964c8ca4c783a4d6",
    "typed-graphs.json": "f7357052495d200f51c736329c66f153ed25e859ff511811fda808dd665ea9d1",
    "source-statement-crosswalk.md": "a461c01b6c6dfca5f33b82152eff3365a8945266f4c663d4e87ed3c9a36f2e2a",
    "proof-receipt.json": PROOF_RECEIPT_SHA256,
    "validation-receipt.json": VALIDATION_RECEIPT_SHA256,
    "validation-spec.json": "f99875e4078ef46e4b611592e89f0cbd0e72c0625e49ff73bbdf0e2f662ce9d9",
    "check_validation.py": "1c244b38d82f88fceda6f649a1e18b84a70ae81ae5800c7db10bbcf667080f1f",
    "vendor-manifest.json": "8735e7a3a1a17e47dff4b0e2ded4c358d7d8f28ba959cab48677c3dfe473283a",
    "VENDOR_PROVENANCE.md": "0e802682cd69bbca3e2e7c281e0d95836e065757836a096694ab77cef2e74995",
}
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/check_release.py",
    f"Stage1_Instances/{THEOREM}/release-decision.json",
    f"Stage1_Instances/{THEOREM}/release-receipt.json",
    f"Stage1_Instances/{THEOREM}/release-spec.json",
    f"Stage1_Instances/{THEOREM}/release-validation.md",
}
SUMMARY_LINES = (
    "PASS current-head direct Lean replay: exact root and differential root are sorry-free at trust zero",
    "PASS release reconciliation: provisional receipts and frozen authoritative cut agree",
    "BLOCKED dependency.S56-M-0318-VALIDATION.master_acceptance",
    "BLOCKED AUDIT-Z and THEOREM-Z; accepted root remains H2/M3/R4",
    "audit_complete=false theorem_complete=false accepted_receipts=0",
)


def load(path: Path) -> dict:
    def reject_duplicates(pairs: list[tuple[str, object]]) -> dict:
        result: dict[str, object] = {}
        for key, value in pairs:
            assert key not in result, f"duplicate JSON key in {path}: {key}"
            result[key] = value
        return result

    value = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicates)
    assert isinstance(value, dict), path
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(
    argv: list[str], *, cwd: Path = ROOT, env: dict[str, str] | None = None,
    timeout: int = 900, expected_exit: int = 0,
) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        argv, cwd=cwd, env=env, text=True, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, timeout=timeout, check=False,
    )
    assert result.returncode == expected_exit, (
        f"command exited {result.returncode}, expected {expected_exit}: {argv!r}\n"
        f"{result.stdout}"
    )
    return result


def git(*args: str, cwd: Path = ROOT, expected_exit: int = 0) -> str:
    return run(["/usr/bin/git", *args], cwd=cwd, expected_exit=expected_exit).stdout.strip()


def reported_axioms(output: str, declaration: str) -> set[str]:
    match = re.search(
        re.escape(f"'{declaration}' depends on axioms: [") + r"(.*?)]",
        output, re.DOTALL,
    )
    assert match, f"missing axiom report for {declaration}"
    return {part.strip() for part in match.group(1).split(",") if part.strip()}


def assert_text_hygiene(path: Path) -> None:
    data = path.read_bytes()
    assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines()), path


def current_direct_replay() -> dict[str, str]:
    account_home = Path(pwd.getpwuid(os.getuid()).pw_dir)
    toolchain_root = account_home / (
        ".elan/toolchains/leanprover--lean4---v4.29.0"
    )
    lean = toolchain_root / "bin/lean"
    assert sha256(lean) == LEAN_SHA256
    assert LEAN_COMMIT in run([str(lean), "--version"]).stdout
    lake_root = LEAN_ROOT / ".lake"
    assert lake_root.is_symlink()
    dependency_roots = [
        (lake_root / "packages" / name / ".lake/build/lib/lean").resolve()
        for name in (
            "batteries", "Qq", "aesop", "proofwidgets", "importGraph",
            "LeanSearchClient", "plausible", "mathlib",
        )
    ]
    local_root = (lake_root / "build/lib/lean").resolve()
    assert all(path.is_dir() for path in [*dependency_roots, local_root])
    lean_path = ":".join(
        [*(str(path) for path in dependency_roots), str(local_root),
         str(toolchain_root / "lib/lean")]
    )
    base_env = {
        "HOME": str(account_home),
        "PATH": f"{toolchain_root / 'bin'}:/usr/bin:/bin",
        "ELAN_TOOLCHAIN": TOOLCHAIN,
        "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8", "TZ": "UTC",
        "LEAN_NUM_THREADS": "1",
    }

    mathlib = (lake_root / "packages/mathlib").resolve()
    assert git("rev-parse", "HEAD", cwd=mathlib) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == MATHLIB_TREE
    assert git("status", "--porcelain=v1", "--untracked-files=all", cwd=mathlib) == ""

    with tempfile.TemporaryDirectory(prefix="stage1-m0318-release-", dir="/tmp") as name:
        tmp = Path(name)
        target = tmp / "Stage1_Instances" / THEOREM
        vendor = target / "Vendor"
        target.mkdir(parents=True)
        for filename in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
            (target / filename).write_bytes((HERE / filename).read_bytes())
        for source in (HERE / "Vendor").rglob("*"):
            if source.is_file():
                destination = vendor / source.relative_to(HERE / "Vendor")
                destination.parent.mkdir(parents=True, exist_ok=True)
                destination.write_bytes(source.read_bytes())

        def elaborate(source: Path, module_path: str, root: Path, emit: bool) -> str:
            argv = [str(lean), "--trust=0", "-t0", "-R", str(root)]
            if emit:
                argv += ["-o", str(source.with_suffix(".olean"))]
            argv.append(str(source))
            env = dict(base_env)
            env["LEAN_PATH"] = module_path
            return run(argv, cwd=tmp, env=env).stdout

        statement = elaborate(target / "Statement.lean", lean_path, target, True)
        tree = elaborate(target / "ObligationTree.lean", f"{target}:{lean_path}", target, True)
        vendor_outputs: list[str] = []
        for module in ("Gametheory.Scarf", "Gametheory.ScarfPath", "Gametheory.Brouwer"):
            source = vendor / Path(*module.split(".")).with_suffix(".lean")
            vendor_outputs.append(elaborate(source, f"{vendor}:{lean_path}", vendor, True))
        proof = elaborate(target / "Proof.lean", f"{target}:{vendor}:{lean_path}", target, True)
        validation = elaborate(
            target / "Validation.lean", f"{target}:{vendor}:{lean_path}", target, False
        )

    assert proof.count("Declarations are sorry-free!") == len(PROOF_DECLARATIONS)
    assert validation.count("Declarations are sorry-free!") == len(VALIDATION_DECLARATIONS)
    for declaration in PROOF_DECLARATIONS:
        assert reported_axioms(proof, declaration) == EXPECTED_AXIOMS
    for declaration in VALIDATION_DECLARATIONS:
        assert reported_axioms(validation, declaration) == EXPECTED_AXIOMS
    combined = "\n".join((statement, tree, *vendor_outputs, proof, validation))
    assert "error:" not in combined.lower() and "declaration uses 'sorry'" not in combined
    return {
        "statement": hashlib.sha256(statement.encode()).hexdigest(),
        "tree": hashlib.sha256(tree.encode()).hexdigest(),
        "vendor": hashlib.sha256("".join(vendor_outputs).encode()).hexdigest(),
        "proof": hashlib.sha256(proof.encode()).hexdigest(),
        "validation": hashlib.sha256(validation.encode()).hexdigest(),
    }


def main() -> None:
    decision = load(HERE / "release-decision.json")
    receipt = load(HERE / "release-receipt.json")
    spec = load(HERE / "release-spec.json")
    validation = load(HERE / "validation-receipt.json")
    proof = load(HERE / "proof-receipt.json")
    instance = load(HERE / "instance.json")
    local_dag = load(HERE / "task-dag.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    statement = load(HERE / "statement.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    targets = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 684 and target["baseline"] == "L0"
    assert target["rework_required"] is True and target["lifecycle_mode"] == "planned"
    assert target["theorem_complete"] is False
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item == {
        "id": ITEM, "theorem_id": THEOREM, "execution_rank": 684,
        "phase": "release", "layer": 6, "state": "[ ]",
        "depends_on": ["S56-M-0318-VALIDATION"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Reconcile evidence and decide the exact theorem-completion verdict.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0, "children": [],
    }
    predecessor = next(
        row for row in execution["items"] if row["id"] == "S56-M-0318-VALIDATION"
    )
    assert predecessor["state"] == "[_]" and predecessor["attempts"] == 1
    local_release = next(row for row in local_dag["tasks"] if row["id"] == ITEM)
    assert local_release["state"] == "open"

    for filename, expected in EXPECTED_INPUTS.items():
        assert sha256(HERE / filename) == expected, f"release input drifted: {filename}"
    assert statement["canonical_formal_target"]["elaborated_expression_sha256"] == (
        TARGET_EXPRESSION_SHA256
    )
    assert registry["frozen_denominators"]["inventory"] == INVENTORY_IDS
    assert registry["frozen_denominators"]["inventory_sha256"] == INVENTORY_SHA256
    assert graphs["root_reachability"]["open_cut_set"] == FROZEN_OPEN_CUT

    assert validation["item_id"] == "S56-M-0318-VALIDATION"
    assert sha256(HERE / "validation-receipt.json") == VALIDATION_RECEIPT_SHA256
    assert validation["support_state"] == "provisional_worker_selftest"
    assert validation["proposed_state"] == "[_]"
    assert validation["accepted"] is validation["release_grade"] is False
    assert validation["verdict"] == "blocked"
    assert validation["result"]["audit_complete"] is False
    assert validation["result"]["theorem_complete"] is False
    assert proof["accepted"] is False and proof["result"]["accepted_root_closed"] is False
    assert proof["root_vector_before"] == proof["root_vector_after"] == {
        "H": "H2", "M": "M4", "R": "R4",
    }
    assert sha256(HERE / "proof-receipt.json") == PROOF_RECEIPT_SHA256
    assert instance["root_vector"] == ROOT_VECTOR
    assert instance["accepted_proof_state"] == []
    assert instance["audit_complete"] is instance["theorem_complete"] is False

    assert decision["schema_version"] == "stage1-release-decision/1.0"
    assert decision["item_id"] == receipt["item_id"] == spec["item_id"] == ITEM
    assert decision["theorem_id"] == receipt["theorem_id"] == spec["theorem_id"] == THEOREM
    assert decision["base_revision"] == receipt["base_revision"] == BASE_REVISION
    assert decision["base_tree"] == receipt["base_tree"] == BASE_TREE
    assert decision["proposed_state"] == receipt["proposed_state"] == packet["state"] == "[_]"
    assert decision["verdict"] == receipt["verdict"] == "blocked"
    assert decision["accepted_receipt_ids"] == receipt["accepted_receipt_ids"] == []
    dependency = decision["dependency"]
    assert dependency["item_id"] == validation["item_id"]
    assert dependency["receipt_id"] == validation["receipt_id"]
    assert dependency["receipt_sha256"] == VALIDATION_RECEIPT_SHA256
    assert dependency["accepted"] is dependency["release_grade"] is False
    assert dependency["master_accepted"] is False

    terminal = decision["terminal_decisions"]
    assert terminal == {
        "audit_complete": False, "theorem_complete": False,
        "audit_z": "blocked", "theorem_z": "blocked", "release_accepted": False,
    }
    assert decision["root_vector"]["accepted_before"] == ROOT_VECTOR
    assert decision["root_vector"]["accepted_after"] == ROOT_VECTOR
    assert decision["first_failed_gate"]["node_gate"] == (
        "dependency.S56-M-0318-VALIDATION.master_acceptance"
    )
    assert decision["canonical_obligation_ids"] == INVENTORY_IDS
    assert decision["first_failed_release_gate"]["gate_id"] == (
        "S56-RELEASE-IMMUTABLE-CLEAN-INPUT"
    )
    assert decision["first_failed_reproduction_gate"]["gate_id"] == (
        "S56-10.6-HERMETIC-COLD-EMPTY-CACHE"
    )
    assert decision["authoritative_remaining_root_cut_set"] == FROZEN_OPEN_CUT
    for key in (
        "dependency_master_acceptance", "authoritative_graph_reconciliation",
        "audit_inventory_reconciliation", "proof_receipt_debt_vector_consistent",
        "pinpoint_h0_review", "independent_r0_review",
        "accepted_foundation_profile", "complete_provenance_trust_tcb_and_sbom",
        "immutable_clean_release_input", "hermetic_cold_offline_replay",
        "independent_signed_runner_attestations", "independent_minimal_verifier",
        "protected_ci_mutation_gates", "deterministic_release_bundle", "master_acceptance",
    ):
        assert decision["evidence_reconciliation"][key] is False, key

    assert spec["schema_version"] == "stage1-validation-recipe/1.0"
    assert spec["argv"] == ["python3", "-I", "-B", f"Stage1_Instances/{THEOREM}/check_release.py"]
    assert spec["cwd"] == "." and spec["network_policy"] == "denied"
    assert spec["expected_exit"] == 0 and spec["covered_obligation_ids"] == INVENTORY_IDS
    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["accepted"] is receipt["release_grade"] is False
    assert receipt["content_addressed_release_evidence"] is False
    assert receipt["result"]["audit_complete"] is False
    assert receipt["result"]["theorem_complete"] is False
    assert receipt["result"]["root_vector_before"] == ROOT_VECTOR
    assert receipt["result"]["root_vector_after"] == ROOT_VECTOR
    assert receipt["canonical_obligation_ids"] == INVENTORY_IDS
    assert receipt["known_failures"] == decision["known_failures"]
    for relative, expected in receipt["input_bindings"].items():
        assert sha256(ROOT / relative) == expected, f"receipt input drifted: {relative}"
    for relative, expected in receipt["release_artifact_bindings"].items():
        assert sha256(ROOT / relative) == expected, f"release artifact drifted: {relative}"
    assert receipt["recipe"] == {
        key: spec[key]
        for key in (
            "recipe_id", "cwd", "argv", "env_allowlist", "timeout_seconds",
            "network_policy", "network_enforcement", "expected_exit",
            "expected_outputs", "covered_obligation_ids", "covered_declarations",
        )
    }

    observed_hashes = current_direct_replay()
    assert receipt["current_direct_replay"]["output_sha256"] == observed_hashes
    assert receipt["current_direct_replay"]["observed_axioms"] == sorted(EXPECTED_AXIOMS)
    assert receipt["current_direct_replay"]["proof_sorry_free_reports"] == 9
    assert receipt["current_direct_replay"]["validation_sorry_free_reports"] == 5

    assert set(packet) == {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert packet["item_id"] == ITEM and packet["base_revision"] == BASE_REVISION
    assert set(packet["changed_paths"]) == CHANGED_PATHS
    assert packet["known_failures"] == decision["known_failures"]
    actual = {
        line[3:] for line in git("status", "--short", "--untracked-files=all").splitlines()
        if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual == CHANGED_PATHS, (actual, CHANGED_PATHS)
    for relative in CHANGED_PATHS:
        assert_text_hygiene(ROOT / relative)

    handoff = (HERE / "release-validation.md").read_text(encoding="utf-8")
    for fragment in (
        "`blocked`", "`[H2, M3, R4]`", "`AUDIT-Z`", "`THEOREM-Z`",
        "accepts no receipt", "current-head direct replay",
    ):
        assert fragment in handoff, fragment
    for line in SUMMARY_LINES:
        print(line)


if __name__ == "__main__":
    main()
