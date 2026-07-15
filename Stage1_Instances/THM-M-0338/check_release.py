#!/usr/bin/env python3
"""Fail-closed release reconciliation for S56-M-0338-RELEASE."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0338"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
ITEM = "S56-M-0338-RELEASE"
THEOREM = "THM-M-0338"
BASE_REVISION = "90a1d52c43113012c8aa0e2b110da02e58ce1724"
BASE_TREE = "bc399f3ba59411f2a72d4f29d98eb85e7689b28c"
VALIDATION_BASE = "38502dd8cfdb1c7b89d62d802952ab596838ec7e"
VALIDATION_RECEIPT_SHA256 = (
    "cf7d8c8eab38759194d32a93bb48fc2c9968de2a31844585ea42c63efee2ab7e"
)
EXPRESSION_SHA256 = "c0c479c898a7b418bd4d82ad05d7514edfcc885cfd9a5487fb1a4ac5ffc37868"
DENOMINATOR_SHA256 = "e53a0b15267ae38e68bb1b727edd51b52d0b60c8f244fd912fc2153c2a0cca6e"
INSTANCE_VECTOR = {"H": "H1", "M": "M4", "R": "R4"}
GRAPH_VECTOR = {"H": "H1", "M": "M3", "R": "R4"}
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
AUTHORITATIVE_OPEN_CUT = [
    "M0338-E-EXTENSION",
    "M0338-KS-PAVING",
    "M0338-W-MSS",
    "M0338-X-SOURCE",
    "M0338-X-FOUNDATION",
]
PROVISIONAL_POST_EXISTENCE_CUT = [
    "M0338-KS-PAVING",
    "M0338-W-MSS",
    "M0338-X-SOURCE",
    "M0338-X-FOUNDATION",
]
INVENTORY_IDS = [
    "M0338-ROOT",
    "M0338-S-ENCODING",
    "M0338-C-COMPONENTS",
    "M0338-E-EXTENSION",
    "M0338-U-UNIQUE",
    "M0338-KS-PAVING",
    "M0338-P-WEAVER",
    "M0338-W-MSS",
    "M0338-M-MIXED",
    "M0338-M-INTERLACE",
    "M0338-M-REALROOT",
    "M0338-F-FINITE",
    "M0338-T-ASSEMBLE",
    "M0338-X-SOURCE",
    "M0338-X-FOUNDATION",
    "M0338-X-PROVENANCE",
]
EXPECTED_INPUTS = {
    "README.md": "92b9dfb31c80979f8d840a1bebe2f77fe81991123a5101e17ce17ffdb228e797",
    "instance.json": "2bd5e0507fae9dc0e7d4ae0414e48760ded5c56022707055acf53e1c5374b07b",
    "task-dag.json": "2f900821c1603775bf5e97d747c1410ef0b7b8a1f81b4642e66b3885183eb522",
    "Statement.lean": "6619fde250e55f083e861d4de954745713a3448e12a10d0e140f1d7a4064ad12",
    "ObligationTree.lean": "fdce8a20bf3dd3c352231fd96191dfb586be762dc16d70ef65275c1d161feecc",
    "Proof.lean": "e01e94a10cd5ce14e8ed6a9db278613dc36db450bd6321b6b7b024d5b745ce63",
    "Validation.lean": "8055c5c3b52893f32d66b1103eb9f6070a1c310111fa91b85c0891c037e423ee",
    "statement.json": "4958303246f52b32343c85eb0e84632baf3431f8a33c49e1aa683b247105dc7a",
    "anchor-audit.json": "f5f569f97f8191ec2bb496d0ad6d16c1fd7d926d11529c913685a15a01e95e69",
    "obligation-registry.json": "cf68ffc3d5de606e9160b88caea41d416987fb4819b29d0675297e0c3f770c0e",
    "typed-graphs.json": "5377a8337b27397d9429db358c731574236f17cfaa8fba733e2cdc25193df237",
    "source-statement-crosswalk.md": "a81f9c569f0ec8e63053b180bfb6cbeb404581402757d784344924ad5974a13a",
    "proof-receipt.json": "9d77bf742ddeb4d71b802bead98c64607d7d08e3e897774a2b28c4c3980781c7",
    "proof-blocker.json": "2b029cf5a081d4beb6c0766619b8e1fec90fe9b565bae04af46dedf266f56ca1",
    "validation-spec.json": "13093ea3a40c3dbca134d6e32b5e990fb9a1f9e281c7ad9770549faf432ec59e",
    "validation-receipt.json": VALIDATION_RECEIPT_SHA256,
    "validation-blocker.json": "508213b0722e0b9a4ec1d561edde8798ec7874a3dd6b97a2509664a059f4ca3d",
    "validation-phase.md": "b5d21e2b472a1fb807f61dd4c41c7837b26f2e06f97bec05603190ec13c6a720",
    "check_validation.py": "be8037522b1778d562144b3e8900857f35b3f812ed14046c74c54110d209caec",
    "check_proof.sh": "2e505d195731d34d4fc5bf70cf70cf42e403771d2f415dc655f92ae154c46013",
}
EXPECTED_AUTHORITY_INPUTS = {
    "Docs/Stage1_Blueprint_rev-5.6.md": "b7eda91ee4c892cad95da8607ee88781bc7526b77e84a5d830fb3c1fc0b0815d",
    "Docs/Stage1_Targets_rev-5.6.json": "02eec284de534dd78e1cf75f82a477ff477567dd682b7445cb7587abd137ab2c",
    "Docs/Stage1_Execution_DAG_rev-5.6.json": "c5c937788f05379c1ea5584d53e3c81a2dc4f9402c0c8a159478880093f5f2cf",
    "Docs/Blueprint_Guidelines.md": "a06c07b5ca1b270b4935ad3dab893e9a0e078c29c8da2ef9dca1e71193310535",
    "skills/execute-stage1-rev56/SKILL.md": "26d47a66c6535feabb8bbf1051fd55d76a53fe761f4b3d953f86b97ec86152b8",
    "Formalizations/Lean/lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "Formalizations/Lean/lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
RELEASE_OUTPUT_NAMES = (
    "check_release.py",
    "release-spec.json",
    "release-decision.json",
    "release-validation.md",
)
CHANGED_PATHS = [
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/check_release.py",
    f"Stage1_Instances/{THEOREM}/release-decision.json",
    f"Stage1_Instances/{THEOREM}/release-receipt.json",
    f"Stage1_Instances/{THEOREM}/release-spec.json",
    f"Stage1_Instances/{THEOREM}/release-validation.md",
]
SUMMARY_LINES = [
    "PASS release reconciliation: target, DAG, receipts, registry, graphs, and immutable input hashes agree",
    "PASS current narrow replay: exact statement, conditional composition, and extension existence checked at trust zero",
    "BLOCKED S56-10.2-DEPENDENCY-ACCEPTANCE: validation is provisional, blocked, and not master accepted",
    "BLOCKED exact root: ExtensionAtMostOne and the Kadison-Singer/MSS route have no proof body",
    "BLOCKED structured state: instance M4 conflicts with graph/validation M3; weaker M4 projection retained",
    "BLOCKED AUDIT-Z and THEOREM-Z: source/readability, trust, hermetic, independent, and bundle gates are open",
    "verdict=blocked audit_complete=false theorem_complete=false accepted_receipts=0",
]


if not __debug__:
    raise RuntimeError("release validation requires Python assertions")


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
    argv: list[str], *, cwd: Path = ROOT, timeout: int = 600, expected_exit: int = 0,
) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        argv,
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=timeout,
        check=False,
    )
    if result.returncode != expected_exit:
        raise RuntimeError(
            f"command exit {result.returncode}, expected {expected_exit}: {argv!r}\n"
            f"{result.stdout}"
        )
    return result


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["/usr/bin/git", *args], cwd=cwd, timeout=60).stdout.strip()


def assert_text_hygiene(path: Path) -> None:
    data = path.read_bytes()
    assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines()), path


def source_without_comments(source: str) -> str:
    output: list[str] = []
    index = 0
    depth = 0
    while index < len(source):
        if depth == 0 and source.startswith("--", index):
            newline = source.find("\n", index)
            if newline < 0:
                break
            output.append("\n")
            index = newline + 1
        elif source.startswith("/-", index):
            depth += 1
            index += 2
        elif depth and source.startswith("-/", index):
            depth -= 1
            index += 2
        elif depth:
            if source[index] == "\n":
                output.append("\n")
            index += 1
        else:
            output.append(source[index])
            index += 1
    assert depth == 0, "unterminated Lean block comment"
    return "".join(output)


def current_narrow_replay() -> dict[str, object]:
    result = run(["/bin/bash", str(HERE / "check_proof.sh")], timeout=420)
    output = result.stdout
    for declaration in (
        "Stage1.THM_M_0338.extension_exists_for_state",
        "Stage1.THM_M_0338.extension_exists_for_kadison_singer_input",
    ):
        matches = re.findall(
            re.escape(f"'{declaration}' depends on axioms: [") + r"(.*?)]",
            output,
            flags=re.DOTALL,
        )
        assert len(matches) == 1, declaration
        actual = {part.strip() for part in matches[0].split(",") if part.strip()}
        assert actual == EXPECTED_AXIOMS, (declaration, actual)
    assert output.count("Declarations are sorry-free!") == 2
    assert "PASS THM-M-0338 isolated Lean replay" in output
    assert "sorryAx" not in output and "error:" not in output.lower()
    return {
        "stdout_sha256": hashlib.sha256(output.encode()).hexdigest(),
        "sorry_free_reports": 2,
        "observed_axioms": sorted(EXPECTED_AXIOMS),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker-packet", type=Path)
    args = parser.parse_args()

    decision = load(HERE / "release-decision.json")
    receipt = load(HERE / "release-receipt.json")
    spec = load(HERE / "release-spec.json")
    validation = load(HERE / "validation-receipt.json")
    validation_blocker = load(HERE / "validation-blocker.json")
    proof = load(HERE / "proof-receipt.json")
    proof_blocker = load(HERE / "proof-blocker.json")
    instance = load(HERE / "instance.json")
    local_dag = load(HERE / "task-dag.json")
    statement = load(HERE / "statement.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    targets = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target == {
        "execution_rank": 831,
        "legacy_priority_slot": None,
        "theorem_id": THEOREM,
        "name": "卡迪生-辛格问题",
        "category": "分析学 / 泛函分析",
        "source_status_untrusted": "已验证",
        "baseline": "L0",
        "rework_required": True,
        "legacy_artifacts_accepted": False,
        "target_lane": "hard_statement_first_partial_verification",
        "intake_score": 120,
        "lifecycle_mode": "planned",
        "theorem_complete": False,
    }
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item == {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 831,
        "phase": "release",
        "layer": 6,
        "state": "[ ]",
        "depends_on": ["S56-M-0338-VALIDATION"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Reconcile evidence and decide the exact theorem-completion verdict.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }
    predecessor = next(
        row for row in execution["items"] if row["id"] == "S56-M-0338-VALIDATION"
    )
    assert predecessor["state"] == "[_]" and predecessor["attempts"] == 1
    local_release = next(row for row in local_dag["tasks"] if row["id"] == ITEM)
    assert local_release["state"] == "open"

    for filename, expected in EXPECTED_INPUTS.items():
        assert sha256(HERE / filename) == expected, f"release input drifted: {filename}"
    for relative, expected in EXPECTED_AUTHORITY_INPUTS.items():
        assert sha256(ROOT / relative) == expected, f"authority input drifted: {relative}"

    assert instance["lifecycle"] == "planned"
    assert instance["root_vector"] == INSTANCE_VECTOR
    assert instance["accepted_proof_state"] == []
    assert instance["audit_complete"] is instance["theorem_complete"] is False
    assert instance["canonical_formal_target"]["elaborated_expression_hash"] == (
        f"sha256:{EXPRESSION_SHA256}"
    )
    assert statement["canonical_formal_target"]["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert registry["frozen_denominators"]["inventory"] == INVENTORY_IDS
    assert graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert graphs["closure_boundary"] == {
        "root_closed": False,
        "root_machine_classification": "M3",
        "theorem_complete": False,
        "open_cut_set": AUTHORITATIVE_OPEN_CUT,
    }
    graph_root = next(
        node for node in graphs["nodes"] if node["obligation_id"] == "M0338-ROOT"
    )
    assert {
        "H": graph_root["human_debt"],
        "M": graph_root["machine_debt"],
        "R": graph_root["readability_debt"],
    } == GRAPH_VECTOR
    assert INSTANCE_VECTOR != GRAPH_VECTOR

    assert proof["accepted"] is False
    assert proof["accepted_closed_obligation_ids"] == []
    assert proof["provisionally_closed_obligation_ids"] == ["M0338-E-EXTENSION"]
    assert proof["result"]["root_kernel_closed"] is False
    assert proof["provisional_remaining_machine_cut"] == PROVISIONAL_POST_EXISTENCE_CUT
    assert proof_blocker["remaining_machine_root_cut_set"] == PROVISIONAL_POST_EXISTENCE_CUT
    assert validation["receipt_id"] == decision["dependency"]["receipt_id"]
    assert sha256(HERE / "validation-receipt.json") == VALIDATION_RECEIPT_SHA256
    assert validation["base_revision"] == VALIDATION_BASE
    assert validation["verdict"] == validation_blocker["verdict"] == "blocked"
    assert validation["accepted"] is False and validation["release_grade"] is False
    assert validation["accepted_receipt_ids"] == []
    assert validation["result"]["accepted_closed_obligation_ids"] == []
    assert validation["result"]["root_kernel_closed"] is False
    assert validation["result"]["audit_complete"] is False
    assert validation["result"]["theorem_complete"] is False
    assert validation["result"]["authoritative_open_root_cut"] == AUTHORITATIVE_OPEN_CUT
    assert validation["result"]["provisional_remaining_root_cut"] == PROVISIONAL_POST_EXISTENCE_CUT

    obligation_source = (HERE / "ObligationTree.lean").read_text(encoding="utf-8")
    proof_source = (HERE / "Proof.lean").read_text(encoding="utf-8")
    assert "theorem root_of_components (components : KadisonSingerComponents" in obligation_source
    assert "theorem extension_exists_for_state" in proof_source
    assert "theorem extension_exists_for_kadison_singer_input" in proof_source
    assert "theorem KadisonSingerStatement" not in proof_source
    assert "ExtensionAtMostOne" not in proof_source
    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by|run_tac)\b|"
        r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
        r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
        r"(?:axiom|constant|opaque|unsafe|extern)\b",
        flags=re.MULTILINE,
    )
    executable_lean = "\n".join(
        source_without_comments((HERE / name).read_text(encoding="utf-8"))
        for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean")
    )
    assert prohibited.search(executable_lean) is None

    assert spec["schema_version"] == "stage1-validation-recipe/1.0"
    assert spec["recipe_id"] == "S56-M-0338-RELEASE-negative-reconciliation-v1"
    assert spec["item_id"] == ITEM and spec["theorem_id"] == THEOREM
    assert spec["intent"] == "release"
    assert spec["cwd"] == "." and spec["timeout_seconds"] == 600
    assert spec["network_policy"] == "denied" and spec["expected_exit"] == 0
    assert spec["covered_obligation_ids"] == INVENTORY_IDS
    assert spec["covered_decisions"] == ["AUDIT-Z", "THEOREM-Z"]
    assert spec["argv"] == [
        "/usr/bin/python3",
        "-I",
        "-B",
        f"Stage1_Instances/{THEOREM}/check_release.py",
        "--worker-packet",
        ".stage1-worker-selftest.json",
    ]

    assert decision["schema_version"] == "stage1-release-decision/1.0"
    assert decision["decision_id"] == receipt["decision_id"]
    assert decision["item_id"] == receipt["item_id"] == ITEM
    assert decision["theorem_id"] == receipt["theorem_id"] == THEOREM
    assert decision["base_revision"] == receipt["base_revision"] == BASE_REVISION
    assert decision["base_tree"] == receipt["base_tree"] == BASE_TREE
    assert decision["verdict"] == receipt["verdict"] == "blocked"
    assert decision["proposed_state"] == receipt["proposed_state"] == "[_]"
    assert decision["release_grade"] is receipt["release_grade"] is False
    assert decision["release_accepted"] is receipt["release_accepted"] is False
    assert decision["accepted_receipt_ids"] == receipt["accepted_receipt_ids"] == []
    assert decision["accepted_closed_obligation_ids"] == []
    assert decision["dependency"] == receipt["dependency"]
    assert decision["canonical_obligation_ids"] == receipt["canonical_obligation_ids"] == INVENTORY_IDS
    assert decision["canonical_target"] == receipt["canonical_target"]
    assert decision["proof_body_locations"] == receipt["proof_body_locations"]
    assert decision["root_vector"]["instance_projection"] == INSTANCE_VECTOR
    assert decision["root_vector"]["frozen_graph_and_validation_projection"] == GRAPH_VECTOR
    assert decision["root_vector"]["accepted_after"] == INSTANCE_VECTOR
    assert decision["root_vector"]["reconciliation"].startswith("blocked_")
    assert decision["terminal_decisions"] == {
        "audit_complete": False,
        "theorem_complete": False,
        "audit_z": "blocked",
        "theorem_z": "blocked",
        "release_accepted": False,
    }
    reconciliation = decision["evidence_reconciliation"]
    assert reconciliation["exact_statement_current_kernel_replay"] is True
    assert reconciliation["extension_existence_current_kernel_replay"] is True
    assert reconciliation["conditional_composition_current_kernel_replay"] is True
    assert reconciliation["premise_free_exact_root_kernel_closure"] is False
    assert reconciliation["extension_at_most_one_kernel_closure"] is False
    assert reconciliation["accepted_frozen_obligation_count"] == 0
    for gate in (
        "dependency_master_acceptance",
        "structured_root_vector_reconciled",
        "audit_inventory_reconciliation",
        "pinpoint_h0_review",
        "independent_r0_review",
        "accepted_foundation_profile",
        "complete_provenance_trust_tcb_and_sbom",
        "immutable_clean_release_input",
        "hermetic_cold_offline_replay",
        "independent_signed_runner_attestations",
        "independent_minimal_verifier",
        "protected_ci_mutation_gates",
        "deterministic_release_bundle",
        "master_acceptance",
    ):
        assert reconciliation[gate] is False, gate
    assert decision["first_failed_gate"]["gate_id"] == "S56-10.2-DEPENDENCY-ACCEPTANCE"
    assert decision["first_failed_gate"]["node_gate"] == (
        "dependency.S56-M-0338-VALIDATION.master_acceptance"
    )
    assert decision["first_failed_theorem_gate"]["node_gate"] == "M0338-U-UNIQUE"
    assert decision["first_failed_release_gate"]["gate_id"] == (
        "S56-RELEASE-IMMUTABLE-CLEAN-INPUT"
    )
    assert decision["first_failed_reproduction_gate"]["gate_id"] == (
        "S56-10.6-HERMETIC-COLD-EMPTY-CACHE"
    )
    assert decision["authoritative_remaining_root_cut_set"] == AUTHORITATIVE_OPEN_CUT
    assert decision["provisional_post_existence_root_cut_set"] == PROVISIONAL_POST_EXISTENCE_CUT

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["phase"] == receipt["intent"] == "release"
    assert receipt["accepted"] is receipt["master_accepted"] is False
    assert receipt["content_addressed_release_evidence"] is False
    assert receipt["result"]["instance_root_vector_before"] == INSTANCE_VECTOR
    assert receipt["result"]["graph_validation_root_vector_before"] == GRAPH_VECTOR
    assert receipt["result"]["accepted_root_vector_after"] == INSTANCE_VECTOR
    assert receipt["result"]["structured_root_vector_reconciled"] is False
    assert receipt["result"]["accepted_root_closed"] is False
    assert receipt["result"]["accepted_receipt_ids"] == []
    assert receipt["result"]["accepted_closed_obligation_ids"] == []
    assert receipt["result"]["authoritative_remaining_root_cut_set"] == AUTHORITATIVE_OPEN_CUT
    assert receipt["result"]["audit_complete"] is False
    assert receipt["result"]["theorem_complete"] is False
    assert receipt["result"]["release_accepted"] is False
    assert receipt["current_narrow_replay"]["exit_code"] == 0
    assert receipt["current_narrow_replay"]["observed_axioms"] == sorted(EXPECTED_AXIOMS)
    assert receipt["current_narrow_replay"]["root_credit"] is False
    assert receipt["recipe"]["recipe_id"] == spec["recipe_id"]
    assert receipt["recipe"]["argv"] == spec["argv"]
    assert receipt["recipe"]["expected_exit"] == 0
    for relative, expected in receipt["input_bindings"].items():
        assert sha256(ROOT / relative) == expected, relative

    replay = current_narrow_replay()
    assert replay["sorry_free_reports"] == 2
    assert replay["observed_axioms"] == sorted(EXPECTED_AXIOMS)

    release_hashes = {
        f"Stage1_Instances/{THEOREM}/{name}": sha256(HERE / name)
        for name in RELEASE_OUTPUT_NAMES
    }
    assert receipt["release_artifact_bindings"] == release_hashes
    expected_stdout = ("\n".join(SUMMARY_LINES) + "\n").encode()
    assert receipt["output_evidence"]["stdout_semantic_sha256"] == hashlib.sha256(
        expected_stdout
    ).hexdigest()
    assert receipt["output_evidence"]["expected_line_count"] == len(SUMMARY_LINES)
    assert receipt["changed_paths"] == CHANGED_PATHS

    if args.worker_packet is not None:
        packet = load(args.worker_packet.resolve())
        assert set(packet) == {
            "item_id",
            "changed_paths",
            "commands",
            "output_summary",
            "base_revision",
            "known_failures",
            "state",
        }
        assert packet["item_id"] == ITEM and packet["state"] == "[_]"
        assert packet["base_revision"] == BASE_REVISION
        assert packet["changed_paths"] == receipt["changed_paths"] == CHANGED_PATHS
        assert packet["commands"] == receipt["commands"]
        assert packet["output_summary"] == receipt["output_summary"]
        assert packet["known_failures"] == receipt["known_failures"]
        status = git("status", "--short", "--untracked-files=all")
        actual = {
            line[3:]
            for line in status.splitlines()
            if line[3:] != "Formalizations/Lean/.lake"
        }
        assert actual == set(CHANGED_PATHS), (actual, set(CHANGED_PATHS))

    for relative in CHANGED_PATHS:
        assert_text_hygiene(ROOT / relative)
    for line in SUMMARY_LINES:
        print(line)


if __name__ == "__main__":
    main()
