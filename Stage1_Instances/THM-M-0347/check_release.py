#!/usr/bin/env python3
"""Fail-closed release reconciliation for S56-M-0347-RELEASE."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0347"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM = "S56-M-0347-RELEASE"
THEOREM = "THM-M-0347"
BASE_REVISION = "48fb6596b1844f4183c411142415d872ff21e842"
BASE_TREE = "eb8dfff0e90b5ce5b11ac2096777060d62874064"
EXPRESSION_SHA256 = "ae3d7a520ec1089f6b6a798ee280d598bb18738b4eecf0042a8d9e7fbd3fa564"
DENOMINATOR_SHA256 = "01ec6fc2f46c410770093c63f64aacff21537af51959956e4c041faa20c80bde"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
EXPECTED_AXIOMS = ["propext", "Classical.choice", "Quot.sound"]
INVENTORY_IDS = [
    "M0347-ROOT", "M0347-S-INTERFACE", "M0347-N-CONVOLUTION",
    "M0347-C-KERNEL", "M0347-L-POSITIVITY", "M0347-L-MASS",
    "M0347-L-CONCENTRATION", "M0347-L-UNIFORM-CONTINUITY",
    "M0347-L-ESTIMATE", "M0347-T-ASSEMBLE", "M0347-X-SOURCE",
    "M0347-X-FOUNDATION", "M0347-X-PROVENANCE", "M0347-X-READABLE",
    "M0347-X-WORKFLOW",
]
EXPECTED_INPUTS = {
    "Statement.lean": "040feef72b83e3b2e90a3db8b1a8b018c20c2625724a5f8c8b70e4e6590ec889",
    "AtlasFourierSeries.lean": "f205a16c5146232c7c23e66a018ebd2dd954d70c5c481de5491d3b0cc8752f4f",
    "AtlasAxiomProbe.lean": "72a7f095ce5f2f771b0bf4853d0dba5c2453e112035efc34103c894bc0b709e5",
    "ObligationTree.lean": "e399cfd5da238f8a66f5dcb7cf8928fd56fb4df13735d9b31c2126141371b7aa",
    "Proof.lean": "2a0b7cdf0c80389ad4c3121ee190f0856ffd5c728f4090c46f753cbdf631653a",
    "Validation.lean": "bd6f157f3a199e3c25ccc9e9ad5ae18eb6e36fadde64d23eaa6961e29178ff9e",
    "instance.json": "83aa3ed8347f8595e59f38bbe429459db0746de569e37579cc9b110f954d914f",
    "task-dag.json": "9ea774aaf68d62c263b6602e475ef5baf76bf8d136dc7ac374a92064f2a4b80c",
    "statement.json": "088e56fc1e76ff397429dfbab474578ed4cc90fd38817e51548e5b001e9fdd7a",
    "anchor-audit.json": "7a85a9107e14399eb204d64c0d9ba3349b780aabab9efdca964da3b30c478147",
    "obligation-registry.json": "5701fb89e11b97aa16cff48abc7f2b89c74d2b9d78d2ed21b3656faf565368cd",
    "typed-graphs.json": "624555a233e198b667d384c4b08672c36394a4bacec423fd873a019360f3b88a",
    "proof-receipt.json": "a8ae49d966a2baee0ed29e66906f6c4ad7c6f3c8f3b9cb25fb2d649e15c6509e",
    "proof-validation.md": "957e1883b3184cfaa2ae89c4dd275560591d5a5c2bdd5716638bec6db6b2138f",
    "validation-spec.json": "69b728190901b989875c947a7265aff4a0ebc689ab847265845c0b5d94a8d7ef",
    "validation-receipt.json": "e495e3d0fad8aa5efa44325bdc836b3f0732c81ef6796d887542480c8f377109",
    "validation-phase.md": "925f5b18f9977b43cffe58d7178dc090d1fc8d641a3950dd3fbd6a9cd158673a",
    "check_validation.py": "3f4f9ec68c84b76f4585e244bbb85164b027c4105425a5287ec1f85f18e166fa",
    "check_validation.sh": "217b461b7881f6939157b8bf48b0d633c816adde42a98d6f281de6fa76551fe9",
    "ATLAS-LICENSE": "289dc0e96c537ecc7883cd94c3f65e2b691ac0fd6f4372fc01604531cbbf1abc",
    "release-spec.json": "416d86fa1aa3dde56a138f94c651d1aac0fc536dbe3e9f83056b0cbcab32c711",
    "release-decision.json": "84de4567aa349d214f35d28fb0c8a57d23d6b67fa446783477fe69e6830d5f63",
    "release-validation.md": "33e1a0f10a8a469e10c04f688aacfc58808b9450a666cff14fa90611f31a8239",
}
EXPECTED_REPO_INPUTS = {
    "Formalizations/Lean/lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "Formalizations/Lean/lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
    "Docs/Stage1_Targets_rev-5.6.json": "02eec284de534dd78e1cf75f82a477ff477567dd682b7445cb7587abd137ab2c",
    "Docs/Stage1_Execution_DAG_rev-5.6.json": "9f4aad0f6f2d8d116835bd0d90d4049c235862b2c615e5240454719faee2e821",
    "Docs/Stage1_Blueprint_rev-5.6.md": "6d4f3cb243eff847eb1308456d142dd16e037ee7190906ac9d81a03514b838f1",
    "skills/execute-stage1-rev56/SKILL.md": "26d47a66c6535feabb8bbf1051fd55d76a53fe761f4b3d953f86b97ec86152b8",
}
SUMMARY_LINES = [
    "release-decision: ok (blocked at validation dependency acceptance)",
    "narrow Lean replay: ok (13 declarations, trust-zero, network-isolated, warm-cache)",
    "accepted boundary: H1/M3/R4 unchanged; accepted obligations and receipts remain empty",
    "provisional exact root: kernel-closed candidate without accepted per-node composition or E1 credit",
    "AUDIT-Z=false; THEOREM-Z=false; theorem_complete=false; release_accepted=false",
    "release assurance: license, H0/R0, TCB/SBOM, clean cold-offline, independent-verifier, CI, deterministic-bundle, and master gates open",
]
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/check_release.py",
    f"Stage1_Instances/{THEOREM}/release-decision.json",
    f"Stage1_Instances/{THEOREM}/release-receipt.json",
    f"Stage1_Instances/{THEOREM}/release-spec.json",
    f"Stage1_Instances/{THEOREM}/release-validation.md",
}


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


def run(argv: list[str], *, cwd: Path = ROOT, timeout: int = 600) -> str:
    result = subprocess.run(
        argv, cwd=cwd, text=True, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, timeout=timeout, check=False,
    )
    assert result.returncode == 0, (argv, result.returncode, result.stdout)
    return result.stdout


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["git", *args], cwd=cwd, timeout=60).strip()


def code_without_comments_and_strings(source: str) -> str:
    output: list[str] = []
    index = 0
    block_depth = 0
    in_string = False
    escaped = False
    while index < len(source):
        pair = source[index:index + 2]
        char = source[index]
        if block_depth:
            if pair == "/-":
                block_depth += 1
                output.extend("  ")
                index += 2
            elif pair == "-/":
                block_depth -= 1
                output.extend("  ")
                index += 2
            else:
                output.append("\n" if char == "\n" else " ")
                index += 1
        elif in_string:
            output.append("\n" if char == "\n" else " ")
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
            index += 1
        elif pair == "/-":
            block_depth = 1
            output.extend("  ")
            index += 2
        elif pair == "--":
            newline = source.find("\n", index)
            if newline < 0:
                output.extend(" " * (len(source) - index))
                index = len(source)
            else:
                output.extend(" " * (newline - index))
                index = newline
        elif char == '"':
            in_string = True
            output.append(" ")
            index += 1
        else:
            output.append(char)
            index += 1
    assert block_depth == 0 and not in_string
    return "".join(output)


def assert_text_hygiene(path: Path) -> None:
    data = path.read_bytes()
    assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())


def main() -> None:
    if not __debug__ or sys.flags.optimize:
        raise SystemExit("release-decision: FAIL: Python assertions are disabled")

    decision = load(HERE / "release-decision.json")
    receipt = load(HERE / "release-receipt.json")
    spec = load(HERE / "release-spec.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")
    validation = load(HERE / "validation-receipt.json")
    proof = load(HERE / "proof-receipt.json")
    instance = load(HERE / "instance.json")
    local_dag = load(HERE / "task-dag.json")
    statement = load(HERE / "statement.json")
    anchor = load(HERE / "anchor-audit.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    targets = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 840 and target["baseline"] == "L0"
    assert target["rework_required"] is True
    assert target["lifecycle_mode"] == "planned" and target["theorem_complete"] is False
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item == {
        "id": ITEM, "theorem_id": THEOREM, "execution_rank": 840,
        "phase": "release", "layer": 6, "state": "[ ]",
        "depends_on": ["S56-M-0347-VALIDATION"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Reconcile evidence and decide the exact theorem-completion verdict.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0, "children": [],
    }
    predecessor = next(
        row for row in execution["items"] if row["id"] == "S56-M-0347-VALIDATION"
    )
    assert predecessor["state"] == "[_]" and predecessor["attempts"] == 1
    assert next(row for row in local_dag["tasks"] if row["id"] == ITEM)["state"] == "open"
    assert local_dag["accepted_states"] == []

    for name, expected in EXPECTED_INPUTS.items():
        assert sha256(HERE / name) == expected, f"reconciled input drifted: {name}"
        assert receipt["input_bindings"][f"Stage1_Instances/{THEOREM}/{name}"] == expected
    for relative, expected in EXPECTED_REPO_INPUTS.items():
        assert sha256(ROOT / relative) == expected, f"repository input drifted: {relative}"
        assert receipt["input_bindings"][relative] == expected
    assert receipt["input_bindings"][f"Stage1_Instances/{THEOREM}/check_release.py"] == sha256(
        HERE / "check_release.py"
    )

    formal = statement["canonical_formal_target"]
    assert formal["declaration_or_expression"] == "Stage1Instances.THM_M_0347.FejerTheoremTarget"
    assert formal["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert registry["frozen_denominators"]["inventory"] == INVENTORY_IDS
    assert graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert graphs["closure_boundary"] == {
        "root_closed": False,
        "root_machine_classification": "M3",
        "theorem_complete": False,
        "first_open_cut": [
            "M0347-N-CONVOLUTION", "M0347-C-KERNEL", "M0347-L-POSITIVITY",
            "M0347-L-MASS", "M0347-L-CONCENTRATION",
            "M0347-L-UNIFORM-CONTINUITY", "M0347-X-SOURCE",
            "M0347-X-FOUNDATION", "M0347-X-PROVENANCE",
            "M0347-X-READABLE", "M0347-X-WORKFLOW",
        ],
    }
    root_node = next(node for node in graphs["nodes"] if node["obligation_id"] == "M0347-ROOT")
    assert [
        root_node["human_debt"], root_node["machine_debt"], root_node["readability_debt"]
    ] == ["H1", "M3", "R4"]
    assert instance["lifecycle"] == "planned"
    assert instance["root_vector"] == {"H": "H1", "M": "M3", "R": "R4"}
    assert instance["accepted_proof_state"] == []
    assert instance["audit_complete"] is instance["theorem_complete"] is False

    assert anchor["decision"]["machine_debt"] == "M3"
    assert anchor["decision"]["exact_external_closure_found"] is False
    assert proof["accepted"] is proof["content_addressed"] is False
    assert proof["root_evidence"]["root_kernel_declaration_closed"] is True
    assert proof["root_evidence"]["accepted_root_closed"] is False
    assert proof["root_evidence"]["internal_per_node_composition_credit"] is False
    assert proof["accepted_closed_obligation_ids"] == []
    assert proof["proof_bodies"][0]["license_compatibility"] == "unreviewed_blocker"
    assert validation["item_id"] == "S56-M-0347-VALIDATION"
    assert validation["verdict"] == "blocked"
    assert validation["support_state"] == "provisional_worker_selftest"
    assert validation["accepted"] is validation["release_grade"] is False
    assert validation["content_addressed"] is False
    assert validation["root_vector_before"] == validation["root_vector_after_worker_selftest"] == {
        "H": "H1", "M": "M3", "R": "R4"
    }
    assert validation["results"]["exact_root_kernel_replay"] == "provisional_pass"
    assert validation["results"]["accepted_root_closed"] is False
    assert validation["results"]["accepted_closed_obligation_ids"] == []
    assert validation["results"]["audit_complete"] is False
    assert validation["results"]["theorem_complete"] is False

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by|extern|proof_wanted)\b|"
        r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
        r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
        r"(?:axiom|constant|opaque|unsafe)\b",
        re.MULTILINE,
    )
    for name in (
        "Statement.lean", "AtlasFourierSeries.lean", "AtlasAxiomProbe.lean",
        "ObligationTree.lean", "Proof.lean", "Validation.lean",
    ):
        source = code_without_comments_and_strings((HERE / name).read_text(encoding="utf-8"))
        assert prohibited.search(source) is None, f"prohibited source token in {name}"

    assert decision["item_id"] == ITEM and decision["theorem_id"] == THEOREM
    assert decision["base_revision"] == BASE_REVISION and decision["base_tree"] == BASE_TREE
    assert decision["intent"] == "release" and decision["proposed_state"] == "[_]"
    assert decision["release_grade"] is decision["release_accepted"] is False
    assert decision["verdict"] == "blocked"
    assert decision["lifecycle_before"] == decision["lifecycle_after"] == "planned"
    assert decision["root_vector_before"] == decision["root_vector_after"] == {
        "H": "H1", "M": "M3", "R": "R4"
    }
    assert decision["audit_complete"] is decision["theorem_complete"] is False
    assert decision["accepted_receipt_ids"] == decision["accepted_closed_obligation_ids"] == []
    dependency = decision["dependency"]
    assert dependency["item_id"] == validation["item_id"]
    assert dependency["receipt_id"] == validation["receipt_id"]
    assert dependency["receipt_sha256"] == sha256(HERE / "validation-receipt.json")
    assert dependency["accepted"] is dependency["release_grade"] is False
    assert dependency["master_accepted"] is False
    terminal = decision["terminal_decisions"]
    assert terminal["verdict"] == "blocked"
    assert terminal["lifecycle_before"] == terminal["lifecycle_after"] == "planned"
    assert terminal["root_vector_before"] == terminal["root_vector_after"] == {
        "H": "H1", "M": "M3", "R": "R4"
    }
    assert terminal["audit_complete"] is terminal["theorem_complete"] is False
    assert terminal["audit_z"] == terminal["theorem_z"] == "blocked"
    assert decision["first_failed_gate"]["gate_id"] == "S56-10.2-DEPENDENCY-ACCEPTANCE"
    assert decision["first_failed_substantive_gate"]["gate_id"] == (
        "S56-M0347-ATLAS-LICENSE-AND-ANCHOR-RECONCILIATION"
    )
    assert decision["next_failed_release_gate"]["gate_id"] == "S56-10.6-HERMETIC-COLD-BUILD"
    cut = "\n".join(decision["remaining_root_cut_set"])
    for fragment in (
        "S56-M-0347-VALIDATION", "ATLAS", "per-node composition", "M0-P/E1",
        "primary-source", "R0", "AUDIT-Z", "empty-cache", "two signed",
        "minimal release verifier", "deterministic", "THEOREM-Z",
    ):
        assert fragment in cut, fragment

    assert spec["schema_version"] == "stage1-validation-recipe/1.0"
    assert spec["recipe_id"] == "S56-M-0347-RELEASE-negative-reconciliation-v1"
    assert spec["item_id"] == ITEM and spec["theorem_id"] == THEOREM
    assert spec["argv"] == [
        "python3", "-B", f"Stage1_Instances/{THEOREM}/check_release.py"
    ]
    assert spec["env_allowlist"] == {}
    assert spec["timeout_seconds"] == 1800
    assert spec["network_policy"] == "denied" and spec["expected_exit"] == 0
    assert spec["covered_obligation_ids"] == INVENTORY_IDS
    assert spec["covered_decisions"] == ["AUDIT-Z-blocked", "THEOREM-Z-blocked"]

    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["phase"] == receipt["intent"] == "release"
    assert receipt["depends_on"] == ["S56-M-0347-VALIDATION"]
    assert receipt["decision_id"] == decision["decision_id"]
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["release_grade"] is receipt["content_addressed_release_evidence"] is False
    assert receipt["master_accepted"] is False and receipt["verdict"] == "blocked"
    assert receipt["repository_state"]["tracked_patch_sha256_before_release_outputs"] == (
        "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    )
    result = receipt["result"]
    assert result["verdict"] == "blocked"
    assert result["root_vector_before"] == result["root_vector_after"] == ["H1", "M3", "R4"]
    assert result["observed_axioms"] == EXPECTED_AXIOMS
    assert result["accepted_root_closed"] is False
    assert result["accepted_receipt_ids"] == result["accepted_closed_obligations"] == []
    assert result["audit_complete"] is result["theorem_complete"] is False
    assert result["first_failed_gate"] == "S56-10.2-DEPENDENCY-ACCEPTANCE"
    assert receipt["canonical_obligation_ids"] == INVENTORY_IDS
    environment = receipt["environment"]
    expected_tool_hashes = {
        "lean_executable_sha256": "3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf",
        "lake_executable_sha256": "a608ff084d7e2af228b92a29d7c2fd083ba0580e46889175ec74a81678c98359",
        "python_executable_sha256": "b8d8288faefdd300201f43fcf00f6f539a27218eeed3a3dff5ab10b9c4c99700",
        "git_executable_sha256": "8a48eefa306b9a2a9c3e576784a74ad7485779279e5a46ec43361a1864760e45",
        "bash_executable_sha256": "3efccc187bafa75ff1e37d246270ab3e7aa559f242c7a52bf3ec2a1b5450bdbd",
        "bubblewrap_executable_sha256": "0abea81db798ebf6b4742ac0664802d97521547a353c2a0dbdc21d76cbbfd2c0",
    }
    for key, expected in expected_tool_hashes.items():
        assert environment[key] == expected
    assert environment["mathlib_revision"] == MATHLIB_REVISION
    assert environment["mathlib_tree"] == MATHLIB_TREE

    manifest = load(LEAN_ROOT / "lake-manifest.json")
    mathlib_pin = next(row for row in manifest["packages"] if row["name"] == "mathlib")
    assert mathlib_pin["rev"] == mathlib_pin["inputRev"] == MATHLIB_REVISION
    assert git("rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert git("status", "--porcelain=v1", cwd=MATHLIB) == ""

    lean_output = run(["bash", str(HERE / "check_validation.sh")])
    assert hashlib.sha256(lean_output.encode()).hexdigest() == (
        "33f453f8a8cc5fabced357c190ac517a5e8233babc7ead9225fba9c56d1550b1"
    )
    assert "PASS THM-M-0347 network-isolated trust-zero Lean validation" in lean_output

    assert set(packet) == {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert packet["item_id"] == ITEM and packet["base_revision"] == BASE_REVISION
    assert packet["state"] == "[_]"
    assert set(packet["changed_paths"]) == set(receipt["changed_paths"]) == CHANGED_PATHS
    assert packet["commands"] == receipt["commands_and_results"]
    assert packet["known_failures"] == decision["known_failures"] == receipt["known_failures"]
    assert packet["output_summary"] == SUMMARY_LINES == receipt["output_summary"]

    status = git("status", "--short", "--untracked-files=all")
    actual_changed = {
        line[3:] for line in status.splitlines()
        if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual_changed == CHANGED_PATHS, (actual_changed, CHANGED_PATHS)
    for relative in CHANGED_PATHS:
        assert_text_hygiene(ROOT / relative)
    for path in (
        HERE / "release-decision.json", HERE / "release-receipt.json",
        HERE / "release-validation.md",
    ):
        public_text = path.read_text(encoding="utf-8")
        assert "/home/" not in public_text and ".cron/" not in public_text
        assert "theorem_complete=true" not in public_text

    for line in SUMMARY_LINES:
        print(line)


if __name__ == "__main__":
    main()
