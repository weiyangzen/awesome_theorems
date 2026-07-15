#!/usr/bin/env python3
"""Fail-closed narrow validation for S56-M-0347-VALIDATION."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import platform
import re
import subprocess
import sys
import time


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0347"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM = "S56-M-0347-VALIDATION"
THEOREM = "THM-M-0347"
BASE_REVISION = "57d8d01796f84ffc9de9adf1f5d0723555e7babb"
BASE_TREE = "cdea5b3fad713816ee6c9ed6aae7a10f9009a18e"
EXPRESSION_SHA256 = "ae3d7a520ec1089f6b6a798ee280d598bb18738b4eecf0042a8d9e7fbd3fa564"
DENOMINATOR_SHA256 = "01ec6fc2f46c410770093c63f64aacff21537af51959956e4c041faa20c80bde"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MATHLIB_REMOTE = "https://github.com/leanprover-community/mathlib4.git"
MATHLIB_LICENSE_SHA256 = "b40930bbcf80744c86c46a12bc9da056641d722716c378f5659b9e555ef833e1"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
UPSTREAM_REVISION = "34ffed396f376454c1a9b297f3fd74c5c801fb50"
UPSTREAM_TREE = "c12fe2315fe475d70a4fcee81d6b731f853373ab"
UPSTREAM_BLOB = "5d399cda446f9bd901902b281bb796123c5ec856"
UPSTREAM_SOURCE_SHA256 = "f205a16c5146232c7c23e66a018ebd2dd954d70c5c481de5491d3b0cc8752f4f"
ATLAS_LICENSE_SHA256 = "289dc0e96c537ecc7883cd94c3f65e2b691ac0fd6f4372fc01604531cbbf1abc"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
EXPECTED_AXIOM_LIST = ["propext", "Classical.choice", "Quot.sound"]
MACHINE_IDS = [
    "M0347-ROOT", "M0347-S-INTERFACE", "M0347-N-CONVOLUTION",
    "M0347-C-KERNEL", "M0347-L-POSITIVITY", "M0347-L-MASS",
    "M0347-L-CONCENTRATION", "M0347-L-UNIFORM-CONTINUITY",
    "M0347-L-ESTIMATE", "M0347-T-ASSEMBLE", "M0347-X-FOUNDATION",
]
EXPECTED_INPUTS = {
    "Statement.lean": "040feef72b83e3b2e90a3db8b1a8b018c20c2625724a5f8c8b70e4e6590ec889",
    "statement.json": "088e56fc1e76ff397429dfbab474578ed4cc90fd38817e51548e5b001e9fdd7a",
    "AtlasFourierSeries.lean": UPSTREAM_SOURCE_SHA256,
    "AtlasAxiomProbe.lean": "72a7f095ce5f2f771b0bf4853d0dba5c2453e112035efc34103c894bc0b709e5",
    "ObligationTree.lean": "e399cfd5da238f8a66f5dcb7cf8928fd56fb4df13735d9b31c2126141371b7aa",
    "Proof.lean": "2a0b7cdf0c80389ad4c3121ee190f0856ffd5c728f4090c46f753cbdf631653a",
    "anchor-audit.json": "7a85a9107e14399eb204d64c0d9ba3349b780aabab9efdca964da3b30c478147",
    "obligation-registry.json": "5701fb89e11b97aa16cff48abc7f2b89c74d2b9d78d2ed21b3656faf565368cd",
    "typed-graphs.json": "624555a233e198b667d384c4b08672c36394a4bacec423fd873a019360f3b88a",
    "task-dag.json": "9ea774aaf68d62c263b6602e475ef5baf76bf8d136dc7ac374a92064f2a4b80c",
    "instance.json": "83aa3ed8347f8595e59f38bbe429459db0746de569e37579cc9b110f954d914f",
    "proof-receipt.json": "a8ae49d966a2baee0ed29e66906f6c4ad7c6f3c8f3b9cb25fb2d649e15c6509e",
    "proof-validation.md": "957e1883b3184cfaa2ae89c4dd275560591d5a5c2bdd5716638bec6db6b2138f",
    "check_proof.py": "d7939832f56faf5ae66fdf9a8abf774b1d427e47b51ff8661fbeacdef87d815d",
    "check_proof.sh": "4a4c3d9d4e5a39de9688868ee0f793046fbaf622fbc89b33a00a0562321a5133",
    "ATLAS-LICENSE": ATLAS_LICENSE_SHA256,
    "Validation.lean": "bd6f157f3a199e3c25ccc9e9ad5ae18eb6e36fadde64d23eaa6961e29178ff9e",
    "check_validation.sh": "217b461b7881f6939157b8bf48b0d633c816adde42a98d6f281de6fa76551fe9",
    "validation-spec.json": "69b728190901b989875c947a7265aff4a0ebc689ab847265845c0b5d94a8d7ef",
}
EXPECTED_REPO_INPUTS = {
    "Formalizations/Lean/lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "Formalizations/Lean/lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
    "Docs/Stage1_Blueprint_rev-5.6.md": "fd843a8f8afb7e945795712e03d899f2e2d67d841c168edc4879856ae441beb7",
    "Docs/Stage1_Execution_DAG_rev-5.6.json": "ad358f5aeacccc908a64046bfc4686df2c493452703f74c7a77578212aaa1d0b",
    "Docs/Stage1_Targets_rev-5.6.json": "02eec284de534dd78e1cf75f82a477ff477567dd682b7445cb7587abd137ab2c",
    "skills/execute-stage1-rev56/SKILL.md": "26d47a66c6535feabb8bbf1051fd55d76a53fe761f4b3d953f86b97ec86152b8",
}
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/Validation.lean",
    f"Stage1_Instances/{THEOREM}/check_validation.py",
    f"Stage1_Instances/{THEOREM}/check_validation.sh",
    f"Stage1_Instances/{THEOREM}/validation-phase.md",
    f"Stage1_Instances/{THEOREM}/validation-receipt.json",
    f"Stage1_Instances/{THEOREM}/validation-spec.json",
}
SUMMARY_LINES = (
    "PASS THM-M-0347 narrow validation",
    "PASS network-isolated kernel replay: exact statement, vendored Fejer source, frozen conditional composition, proof root, and differential root elaborated",
    "PASS trust observation: selected source and differential declarations are sorry-free and report exactly propext, Classical.choice, and Quot.sound",
    "PASS selected provenance: frozen hashes, exact upstream blob, retained license, clean mathlib pin, and tool identities agree",
    "FAIL CLOSED authority/license: proof is only worker-self-tested and ATLAS license/rider compatibility is unreviewed",
    "FAIL CLOSED composition/trust: frozen per-node composition and complete transitive foundation, compiled-artifact, and TCB closure remain open",
    "FAIL CLOSED hermetic release: shared warm .lake is not clean-checkout empty-cache bootstrap, offline restoration, or a deterministic TCB/SBOM bundle",
    "FAIL CLOSED independent release: the differential proof used this worker and shared cache, not a distinct signed verifier",
    "audit_complete=false; theorem_complete=false",
)
LEAN_OUTPUT_SHA256 = "33f453f8a8cc5fabced357c190ac517a5e8233babc7ead9225fba9c56d1550b1"
SUMMARY_OUTPUT_SHA256 = "458b0ea609d063d2c28546d4d757a7cc5c15ae59a55944aea5037a695f1275a3"
RECIPE_STARTED = time.monotonic()
RECIPE_TIMEOUT_SECONDS = 600.0


if sys.flags.optimize:
    raise SystemExit("validation failed: Python optimization disables fail-closed assertions")


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


def run(argv: list[str], *, cwd: Path = ROOT) -> str:
    remaining = RECIPE_TIMEOUT_SECONDS - (time.monotonic() - RECIPE_STARTED)
    if remaining <= 0:
        raise TimeoutError("validation recipe exceeded its 600-second wall-clock bound")
    result = subprocess.run(
        argv, cwd=cwd, text=True, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, timeout=remaining, check=False,
    )
    if result.returncode:
        raise RuntimeError(
            f"validation failed ({result.returncode}): {argv!r}\n{result.stdout}"
        )
    return result.stdout


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["/home/sansha-2/.local/bin/git", *args], cwd=cwd).strip()


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


def printed_axioms(output: str, declaration: str) -> set[str]:
    match = re.search(
        re.escape(f"'{declaration}' depends on axioms: [") + r"(.*?)]",
        output,
        re.DOTALL,
    )
    assert match is not None, declaration
    return {part.strip() for part in match.group(1).split(",") if part.strip()}


def assert_text_hygiene(path: Path) -> None:
    data = path.read_bytes()
    assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())


def main() -> None:
    spec = load(HERE / "validation-spec.json")
    receipt = load(HERE / "validation-receipt.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")
    targets = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    statement = load(HERE / "statement.json")
    anchor = load(HERE / "anchor-audit.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    local_dag = load(HERE / "task-dag.json")
    instance = load(HERE / "instance.json")
    proof_receipt = load(HERE / "proof-receipt.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 840 and target["baseline"] == "L0"
    assert target["lifecycle_mode"] == "planned"
    assert target["rework_required"] is True and target["theorem_complete"] is False
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item == {
        "id": ITEM, "theorem_id": THEOREM, "execution_rank": 840,
        "phase": "validation", "layer": 5, "state": "[ ]",
        "depends_on": ["S56-M-0347-PROOF"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Run hermetic kernel, trust, provenance, and independent validation gates.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0, "children": [],
    }
    predecessor = next(row for row in execution["items"] if row["id"] == "S56-M-0347-PROOF")
    assert predecessor["state"] == "[_]" and predecessor["attempts"] == 1
    assert next(row for row in local_dag["tasks"] if row["id"] == ITEM)["state"] == "open"
    assert local_dag["accepted_states"] == []
    assert instance["lifecycle"] == "planned"
    assert instance["root_vector"] == {"H": "H1", "M": "M3", "R": "R4"}
    assert instance["accepted_proof_state"] == []
    assert instance["audit_complete"] is instance["theorem_complete"] is False

    for name, expected in EXPECTED_INPUTS.items():
        if name == "check_validation.py":
            continue
        assert sha256(HERE / name) == expected, f"stale validation input: {name}"
    for relative, expected in EXPECTED_REPO_INPUTS.items():
        assert sha256(ROOT / relative) == expected, f"stale repository input: {relative}"
    formal = statement["canonical_formal_target"]
    assert formal["declaration_or_expression"] == "Stage1Instances.THM_M_0347.FejerTheoremTarget"
    assert formal["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert formal["statement_file_sha256"] == EXPECTED_INPUTS["Statement.lean"]
    assert anchor["canonical_target"] == formal["declaration_or_expression"]
    assert anchor["decision"]["machine_debt"] == "M3"
    assert anchor["decision"]["exact_external_closure_found"] is False
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert registry["frozen_denominators"]["required_machine"] == MACHINE_IDS
    assert graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    closure = graphs["closure_boundary"]
    assert closure["root_closed"] is False
    assert closure["root_machine_classification"] == "M3"
    assert closure["theorem_complete"] is False

    assert proof_receipt["item_id"] == "S56-M-0347-PROOF"
    assert proof_receipt["canonical_target_expression_sha256"] == EXPRESSION_SHA256
    assert proof_receipt["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert proof_receipt["accepted"] is False
    assert proof_receipt["accepted_closed_obligation_ids"] == []
    assert proof_receipt["root_evidence"]["root_kernel_declaration_closed"] is True
    assert proof_receipt["root_evidence"]["accepted_root_closed"] is False
    assert proof_receipt["root_evidence"]["internal_per_node_composition_credit"] is False
    assert proof_receipt["result"]["axioms"] == EXPECTED_AXIOM_LIST
    assert proof_receipt["result"]["theorem_complete"] is False
    proof_body = proof_receipt["proof_bodies"][0]
    assert proof_body["upstream_revision"] == UPSTREAM_REVISION
    assert proof_body["upstream_tree"] == UPSTREAM_TREE
    assert proof_body["upstream_blob"] == UPSTREAM_BLOB
    assert proof_body["source_sha256"] == UPSTREAM_SOURCE_SHA256
    assert proof_body["upstream_license_sha256"] == ATLAS_LICENSE_SHA256
    assert proof_body["license_compatibility"] == "unreviewed_blocker"
    assert git("hash-object", str(HERE / "AtlasFourierSeries.lean")) == UPSTREAM_BLOB

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
    differential = code_without_comments_and_strings(
        (HERE / "Validation.lean").read_text(encoding="utf-8")
    )
    for forbidden in (
        "import Proof", "import ObligationTree", "symmetricFourierPartialSum_apply",
        "fejerMean_apply", "fejerTheorem :",
    ):
        assert forbidden not in differential, forbidden
    assert "using fejer_uniform_convergence f" in differential
    assert "assert_no_sorry reconstructedFejerTheorem" in differential

    manifest = load(LEAN_ROOT / "lake-manifest.json")
    mathlib_entry = next(row for row in manifest["packages"] if row["name"] == "mathlib")
    assert mathlib_entry["rev"] == mathlib_entry["inputRev"] == MATHLIB_REVISION
    assert MATHLIB.resolve().is_dir(), "pinned mathlib artifact is unavailable"
    assert git("rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert git("remote", "get-url", "origin", cwd=MATHLIB) == MATHLIB_REMOTE
    assert git("status", "--porcelain=v1", cwd=MATHLIB) == ""
    assert sha256(MATHLIB / "LICENSE") == MATHLIB_LICENSE_SHA256

    toolchain = Path.home() / ".elan/toolchains/leanprover--lean4---v4.29.0"
    lean = toolchain / "bin/lean"
    lake = toolchain / "bin/lake"
    assert lean.is_file() and lake.is_file()
    lean_version = run([str(lean), "--version"])
    assert "4.29.0" in lean_version and LEAN_COMMIT in lean_version
    python = Path(os.path.realpath(sys.executable))
    git_path = Path("/home/sansha-2/.local/bin/git")
    bash = Path("/usr/bin/bash")
    bwrap = Path("/usr/bin/bwrap")
    expected_tools = {
        lean: "3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf",
        lake: "a608ff084d7e2af228b92a29d7c2fd083ba0580e46889175ec74a81678c98359",
        python: "b8d8288faefdd300201f43fcf00f6f539a27218eeed3a3dff5ab10b9c4c99700",
        git_path: "8a48eefa306b9a2a9c3e576784a74ad7485779279e5a46ec43361a1864760e45",
        bash: "3efccc187bafa75ff1e37d246270ab3e7aa559f242c7a52bf3ec2a1b5450bdbd",
        bwrap: "0abea81db798ebf6b4742ac0664802d97521547a353c2a0dbdc21d76cbbfd2c0",
    }
    for path, expected in expected_tools.items():
        assert sha256(path) == expected, path

    runner_output = run([str(bash), str(HERE / "check_validation.sh")])
    assert hashlib.sha256(runner_output.encode()).hexdigest() == LEAN_OUTPUT_SHA256
    assert len(runner_output.encode()) == 2522 and len(runner_output.splitlines()) == 38
    declarations = (
        "Stage1Instances.THM_M_0347.ObligationTree.root_of_uniformFejerEstimate",
        "FourierSeries.fejer_kernel_properties",
        "FourierSeries.cesaroMean_eq_fejer_convolution",
        "fejerKernel_eq_ofReal", "integral_norm_fejerKernel",
        "cesaroMean_uniform_bound", "fejer_uniform_convergence",
        "Stage1Instances.THM_M_0347.symmetricFourierPartialSum_apply",
        "Stage1Instances.THM_M_0347.fejerMean_apply",
        "Stage1Instances.THM_M_0347.fejerTheorem",
        "Stage1Instances.THM_M_0347.Validation.reconstructedPartialSum",
        "Stage1Instances.THM_M_0347.Validation.reconstructedMean",
        "Stage1Instances.THM_M_0347.Validation.reconstructedFejerTheorem",
    )
    for declaration in declarations:
        assert printed_axioms(runner_output, declaration) == EXPECTED_AXIOMS
    assert runner_output.count("Declarations are sorry-free!") == 9
    assert "PASS THM-M-0347 network-isolated trust-zero Lean validation" in runner_output
    assert "sorryAx" not in runner_output and "declaration uses 'sorry'" not in runner_output

    assert spec["schema_version"] == "stage1-validation-spec/1.0"
    assert spec["item_id"] == ITEM and spec["theorem_id"] == THEOREM
    assert spec["phase"] == "validation" and spec["intent"] == "validate"
    assert spec["cwd"] == "."
    assert spec["argv"] == [
        "python3", "-B", f"Stage1_Instances/{THEOREM}/check_validation.py"
    ]
    assert spec["env_allowlist"] == {} and spec["timeout_seconds"] == 600
    assert spec["network_policy"] == "denied" and spec["expected_exit"] == 0
    assert "--unshare-net" in spec["network_enforcement"]
    assert spec["covered_obligation_ids"] == MACHINE_IDS
    assert spec["expected_outputs"] == [{
        "path_or_stream": "stdout",
        "semantic_hash_policy": "exact ordered nine-line PASS/FAIL-CLOSED summary bound by validation-receipt.json",
    }]

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["phase"] == "validation" and receipt["intent"] == "validate"
    assert receipt["depends_on"] == ["S56-M-0347-PROOF"]
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]" and receipt["verdict"] == "blocked"
    assert receipt["accepted"] is receipt["release_grade"] is receipt["content_addressed"] is False
    assert receipt["validated_at"] == "2026-07-15T06:11:22Z"
    assert receipt["review_due"] and receipt["attestor"] and receipt["owner"]
    assert receipt["target"]["canonical_target_expression_sha256"] == EXPRESSION_SHA256
    assert receipt["target"]["registry_denominator_sha256"] == DENOMINATOR_SHA256
    for name, expected in EXPECTED_INPUTS.items():
        if name == "check_validation.py":
            assert receipt["inputs"][name] == sha256(HERE / name)
        else:
            assert receipt["inputs"][name] == expected, name
    for relative, expected in EXPECTED_REPO_INPUTS.items():
        assert receipt["inputs"][relative] == expected, relative
    environment = receipt["environment"]
    assert environment["platform"] == f"{platform.system()} {platform.machine()}"
    assert environment["mathlib_revision"] == MATHLIB_REVISION
    assert environment["mathlib_tree"] == MATHLIB_TREE
    assert environment["lean_executable_sha256"] == sha256(lean)
    assert environment["lake_executable_sha256"] == sha256(lake)
    assert environment["python_executable_sha256"] == sha256(python)
    assert environment["git_executable_sha256"] == sha256(git_path)
    assert environment["bash_executable_sha256"] == sha256(bash)
    assert environment["bubblewrap_executable_sha256"] == sha256(bwrap)
    for key in (
        "recipe_id", "cwd", "argv", "env_allowlist", "timeout_seconds",
        "network_policy", "expected_exit", "covered_obligation_ids",
    ):
        assert receipt["recipe"][key] == spec[key], key
    result = receipt["results"]
    assert result["network_isolated_trust_zero_kernel_replay"] == "pass"
    assert result["exact_root_kernel_replay"] == "provisional_pass"
    assert result["differential_exact_root_replay"] == "provisional_pass_same_worker"
    assert result["observed_axioms"] == EXPECTED_AXIOM_LIST
    assert result["placeholder_unsafe_oracle_scan"] == "pass"
    assert result["selected_vendored_provenance"] == "pass"
    assert result["proof_master_acceptance"] == "fail_closed"
    assert result["accepted_root_machine_debt"] == "M3"
    assert result["accepted_root_closed"] is False
    assert result["accepted_closed_obligation_ids"] == []
    for key in (
        "frozen_internal_composition_gate", "license_compatibility_gate",
        "accepted_foundation_and_complete_trust_closure",
        "complete_provenance_and_sbom_gate", "hermetic_cold_offline_replay",
        "independent_distinct_runner",
    ):
        assert result[key] == "fail_closed", key
    assert result["accepted_state_changed"] is False
    assert result["audit_complete"] is result["theorem_complete"] is False
    assert receipt["first_failed_gate"] == "dependency.S56-M-0347-PROOF.master_acceptance"
    assert receipt["first_failed_proof_acceptance_gate"] == "provenance.ATLAS-license-rider-compatibility"
    assert receipt["first_failed_release_gate"] == "S56-10.6-HERMETIC-COLD-BUILD"
    outputs = receipt["outputs"]
    assert outputs["lean_replay_started_at"] == "2026-07-15T06:09:51Z"
    assert outputs["lean_replay_finished_at"] == "2026-07-15T06:11:22Z"
    assert outputs["lean_replay_duration_ms"] == 91026
    assert outputs["lean_replay_exit_code"] == 0
    assert outputs["lean_replay_stdout_sha256"] == LEAN_OUTPUT_SHA256
    assert outputs["lean_replay_stdout_bytes"] == 2522
    assert outputs["lean_replay_stdout_lines"] == 38
    summary_output = "\n".join(SUMMARY_LINES) + "\n"
    assert hashlib.sha256(summary_output.encode()).hexdigest() == SUMMARY_OUTPUT_SHA256
    assert outputs["checker_summary_sha256"] == SUMMARY_OUTPUT_SHA256
    assert outputs["checker_summary_bytes"] == len(summary_output.encode()) == 1033
    assert outputs["checker_summary_lines"] == len(SUMMARY_LINES) == 9

    assert packet["item_id"] == ITEM and packet["state"] == "[_]"
    assert packet["base_revision"] == BASE_REVISION
    assert set(packet["changed_paths"]) == CHANGED_PATHS
    assert set(receipt["changed_paths"]) == CHANGED_PATHS
    status = git("status", "--short", "--untracked-files=all")
    actual_changed = {
        line[3:] for line in status.splitlines()
        if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual_changed == CHANGED_PATHS, (actual_changed, CHANGED_PATHS)
    phase_notes = (HERE / "validation-phase.md").read_text(encoding="utf-8")
    assert "This is self-tested `blocked` worker evidence" in phase_notes
    assert "empty-cache cold bootstrap" in phase_notes
    assert "theorem_complete=false" in phase_notes
    for relative in CHANGED_PATHS - {".stage1-worker-selftest.json"}:
        assert_text_hygiene(ROOT / relative)

    print("\n".join(SUMMARY_LINES))


if __name__ == "__main__":
    main()
