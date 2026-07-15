#!/usr/bin/env python3
"""Fail-closed release reconciliation for S56-M-0957-RELEASE."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0957"
ITEM = "S56-M-0957-RELEASE"
THEOREM = "THM-M-0957"
BASE_REVISION = "6bf9ee93a322e7d25cf9249226222095f95d1cff"
BASE_TREE = "24acf86e69ab2e6fca9480c6269b6429874ba295"
GRAPH_SHA256 = "73e99d2276c8ba9fec8f89ed41b712308d7f5667e95ba8185e49f1f5bfd40eca"
CONTEXT_SHA256 = "597fb262ed0080242a24b2d15146117dfdb7a64ac96a66fcb8715ec264935bd9"
EXPRESSION_SHA256 = "e611db43ce6f3419553e3ebe0fe85a3ce89e4d3930b3842f5a09be8a7683d2ed"
DENOMINATOR_SHA256 = "84f7eaea7de3659e4324dc64f7849fde4024dd057d4d320c879b0b59dd692a63"
VALIDATION_RECEIPT_SHA256 = "2b9324eba88875a93d8fde16c8a4594f7722419facca359e54ef0280891d4d09"
LEDGER_SHA256 = "63fbc3b8821d2a451e8af8ba2b6a4b03574f1f5b0ce41f003bbfd7a10409f777"
SPEC_SHA256 = "4c35592e9cab1057e65406188c2fd18e52ef16192442cc065b978acf82f69497"
DECISION_SHA256 = "21d7821fa847fcce6040fbecc287107f834221c66782d7fbe61f3ed5895ecdb3"
REPORT_SHA256 = "8a94495354f00f837af41b6731ef1bf8908e0eff5c493c63f1c392b13a9cbf21"
RECEIPT_SHA256 = "b509a7554ec9aa3529cae498775498d2aa8add70f9f0daf6a291ca2c2cdf0239"
STDOUT_SHA256 = "886fd5272ada92d5a58331d7550ec18439c105a4d83d3e77dd69b3e24b241c15"
SHARED_GROUP = "SHARED-MODULE-1d5edf843c0d2042"
SHARED_MEMBER = "THM-M-0958"
SUMMARY_LINES = (
    "PASS release inputs: target, v2 context, receipts, frozen state, and content hashes agree",
    "PASS dependency audit: hard parent closure is empty; weak shared group inspected with no reuse credit",
    "PASS provisional Lean evidence boundary: exact root replay exists, but accepted closure remains H1/M3/R3",
    "BLOCKED dependency.S56-M-0957-VALIDATION.master_acceptance: validation is [_], blocked, and unaccepted",
    "BLOCKED release protocol: no immutable clean cold/offline bundle or independent verifier evidence exists",
    "verdict=blocked audit_complete=false theorem_complete=false",
)

EXPECTED_TARGET_INPUTS = {
    "README.md": "29daad74d4a5eb38eca9dba16bcfefc83a462841ec9aef050bdc794cbbaebf7d",
    "source-statement-crosswalk.md": "a71cfdc4815783314661aa21b38753dbaca921fc4e18922029a9e122d2719113",
    "Statement.lean": "b4bda6c926b0568d8b244623c12b4784651d55a9eb7df9d9ba3f512ed2cd9e46",
    "ObligationTree.lean": "efbe7ff68dac5f55bd98fbc00339a3850dfc2c1935f1cde4cf5c7eefe1224223",
    "Proof.lean": "fd8e72e675c88d8dc17b9a64764d4c17a45b462b0689140453cf45463bc024e2",
    "Validation.lean": "091c0ed8d216e623c51a3f594711eb29e270f4cc3b63172ec931af39aeb59347",
    "instance.json": "1291982f7e8f15eca9d00cb6f77d28a1035a97b9851d0b105fd54a2fd4ef4b5f",
    "task-dag.json": "e5631d9c3c802b3d454a487862c4cbf593893061b75415c96551954a32ae1b86",
    "statement.json": "b70cb423c41c9d822b85696a57193ca0fc2dc26fe88b2a471bb68f6a9cb8dfab",
    "anchor-audit.json": "10eff04369551920531fcacb97521ba95f0e0ee45483e8d66ba4e58e49a24423",
    "obligation-registry.json": "75896bc70b85e96fca7bc0ae9e08da4c30cf6c0fb5cecf33cfda6d37eee0e39c",
    "typed-graphs.json": "7b951fc5715c3c4d5d88b210acc355cb98a0ace927a638951803efb95362dde0",
    "proof-receipt.json": "7ed071053e8b7237d95274e0c448366c916253b69a347c848c38f17802f60448",
    "validation-spec.json": "4ad216b2511871a109279f9c487a59ef39adb2ebc654cce0a3974597b952e03d",
    "validation-receipt.json": VALIDATION_RECEIPT_SHA256,
    "validation-phase.md": "9e998ed2d0458000fd54fc8fbec9a28e8c6755a6e7794a112f3a10dde07fed28",
    "check_validation.py": "787a8409182beca31e773b734d372b1f01359114322a7d51c2a4b719de12ba5f",
    "dependency-reuse-ledger.json": LEDGER_SHA256,
}
EXPECTED_SHARED_INPUTS = {
    "Stage1_Instances/THM-M-0958/anchor-audit.json": "eba38a4e3bb2530ffb45bc9560be6b667823a4b3ff9e19fdedc802fc6190224d",
    "Stage1_Instances/THM-M-0958/instance.json": "28dd5b490a3e83306ea10985feeba58904b5d1193fa605eb53f27990413b8990",
}
EXPECTED_AUTHORITY_INPUTS = {
    "Docs/Stage1_Targets_rev-5.6.json": "02eec284de534dd78e1cf75f82a477ff477567dd682b7445cb7587abd137ab2c",
    "Docs/Stage1_Execution_DAG_rev-5.6.json": "f0465351c62c18cf5ae60dedf94e280921346ec1632815c70a646b1f0ae27faa",
    "Docs/Stage1_Theorem_DAG_v2.json": GRAPH_SHA256,
    "Docs/Stage1_Blueprint_v2.md": "52bd099d295cb537212e272cfe5bc494f020ac1a82d4a4e07b600dd0bbc50f5b",
    "Docs/Stage1_Blueprint_rev-5.6.md": "ea65df5ca888dbfcc69cd2a729c9b94f3eae1b8ca5cfc2db6035ef9f8494e58b",
    "Docs/Blueprint_Guidelines.md": "a06c07b5ca1b270b4935ad3dab893e9a0e078c29c8da2ef9dca1e71193310535",
    "skills/execute-stage1-rev56/SKILL.md": "445d47263e9cd9f465ede7513eabbe1c8f7d058acd4130f75160417f3b68ccbd",
    "Formalizations/Lean/lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "Formalizations/Lean/lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
EXPECTED_RELEASE_INPUTS = {
    "release-spec.json": SPEC_SHA256,
    "release-decision.json": DECISION_SHA256,
    "release-validation.md": REPORT_SHA256,
    "release-receipt.json": RECEIPT_SHA256,
}


def load(path: Path) -> dict:
    def reject_duplicates(pairs: list[tuple[str, object]]) -> dict:
        result: dict[str, object] = {}
        for key, value in pairs:
            assert key not in result, f"duplicate JSON key {key!r} in {path}"
            result[key] = value
        return result

    value = json.loads(
        path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicates
    )
    assert isinstance(value, dict), path
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(["git", *args], cwd=cwd, text=True).strip()


def assert_text_hygiene(path: Path) -> None:
    data = path.read_bytes()
    assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())


def source_without_comments_and_strings(source: str) -> str:
    output: list[str] = []
    index = 0
    depth = 0
    in_string = False
    while index < len(source):
        if depth:
            if source.startswith("/-", index):
                depth += 1
                index += 2
            elif source.startswith("-/", index):
                depth -= 1
                index += 2
            else:
                if source[index] == "\n":
                    output.append("\n")
                index += 1
        elif in_string:
            if source[index] == "\\":
                index += 2
            elif source[index] == '"':
                in_string = False
                output.append('"')
                index += 1
            else:
                if source[index] == "\n":
                    output.append("\n")
                index += 1
        elif source.startswith("--", index):
            newline = source.find("\n", index)
            if newline < 0:
                break
            output.append("\n")
            index = newline + 1
        elif source.startswith("/-", index):
            depth = 1
            index += 2
        elif source[index] == '"':
            in_string = True
            output.append('"')
            index += 1
        else:
            output.append(source[index])
            index += 1
    assert depth == 0 and not in_string
    return "".join(output)


def assert_no_prohibited_constructs() -> None:
    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|implemented_by|native_decide)\b|"
        r"^[ \t]*(?:axiom|constant|opaque|unsafe|extern)\b",
        re.MULTILINE,
    )
    for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
        source = source_without_comments_and_strings(
            (HERE / name).read_text(encoding="utf-8")
        )
        assert prohibited.search(source) is None, name


def find_node(theorem_dag: dict, theorem_id: str) -> dict:
    nodes = theorem_dag.get("theorems", theorem_dag.get("nodes", []))
    matches = [row for row in nodes if row.get("theorem_id") == theorem_id]
    assert len(matches) == 1, theorem_id
    return matches[0]


def main() -> None:
    if sys.flags.optimize != 0:
        raise RuntimeError("release checker requires Python assertions")

    decision = load(HERE / "release-decision.json")
    receipt = load(HERE / "release-receipt.json")
    spec = load(HERE / "release-spec.json")
    ledger = load(HERE / "dependency-reuse-ledger.json")
    validation = load(HERE / "validation-receipt.json")
    proof = load(HERE / "proof-receipt.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")
    instance = load(HERE / "instance.json")
    statement = load(HERE / "statement.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    theorem_dag = load(ROOT / "Docs/Stage1_Theorem_DAG_v2.json")
    targets = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE

    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 1491
    assert target["lifecycle_mode"] == "planned"
    assert target["baseline"] == "L0" and target["rework_required"] is True
    assert target["theorem_complete"] is False

    release_item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert release_item == {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 1491,
        "phase": "release",
        "layer": 6,
        "state": "[ ]",
        "depends_on": ["S56-M-0957-VALIDATION"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Reconcile evidence and decide the exact theorem-completion verdict.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }
    predecessor = next(
        row for row in execution["items"] if row["id"] == "S56-M-0957-VALIDATION"
    )
    assert predecessor["state"] == "[_]" and predecessor["attempts"] == 1

    theorem_node = find_node(theorem_dag, THEOREM)
    assert theorem_node["phase_states"]["validation"] == "[_]"
    assert theorem_node["phase_states"]["release"] == "[ ]"
    assert theorem_node["direct_hard_parents"] == []
    assert theorem_node["transitive_hard_ancestors"] == []
    assert theorem_node["direct_reuse_hint_ids"] == []
    assert theorem_node["shared_lemma_group_ids"] == [SHARED_GROUP]
    assert theorem_node["dependency_context_sha256"] == CONTEXT_SHA256

    for name, expected in EXPECTED_TARGET_INPUTS.items():
        assert sha256(HERE / name) == expected, f"target input drifted: {name}"
    for name, expected in EXPECTED_SHARED_INPUTS.items():
        assert sha256(ROOT / name) == expected, f"shared input drifted: {name}"
    for name, expected in EXPECTED_AUTHORITY_INPUTS.items():
        assert sha256(ROOT / name) == expected, f"authority input drifted: {name}"
    for name, expected in EXPECTED_RELEASE_INPUTS.items():
        assert sha256(HERE / name) == expected, f"release input drifted: {name}"

    assert ledger == {
        "schema_version": "stage1-dependency-reuse-ledger/1.1",
        "consumer_theorem_id": THEOREM,
        "observed_theorem_dag_sha256": GRAPH_SHA256,
        "dependency_context_sha256": CONTEXT_SHA256,
        "repository_revision": BASE_REVISION,
        "direct_parent_ids": [],
        "transitive_ancestor_ids": [],
        "hard_edge_ids": [],
        "reuse_hint_ids": [],
        "shared_group_ids": [SHARED_GROUP],
        "inspections": [],
        "reuse_decisions": ledger["reuse_decisions"],
        "unresolved_compatibility_obligations": [],
    }
    assert len(ledger["reuse_decisions"]) == 1
    shared_decision = ledger["reuse_decisions"][0]
    assert shared_decision["source_id"] == SHARED_GROUP
    assert shared_decision["provider_theorem_id"] == SHARED_MEMBER
    assert shared_decision["relationship"] == "candidate_only"
    assert shared_decision["decision"] == "not_applicable"
    assert shared_decision["context_digest"] == CONTEXT_SHA256
    assert "shared theorem body" in shared_decision["non_reuse_reason"]
    forbidden_material_fields = {
        "consumer_obligation_id",
        "provider_obligation_id",
        "terminal_proof_body_id",
        "provider_statement_fingerprint",
        "consumer_required_fingerprint",
        "consumer_import_or_wrapper",
    }
    assert forbidden_material_fields.isdisjoint(shared_decision)

    assert validation["item_id"] == "S56-M-0957-VALIDATION"
    assert validation["receipt_id"] == receipt["dependency_receipt"]["receipt_id"]
    assert sha256(HERE / "validation-receipt.json") == VALIDATION_RECEIPT_SHA256
    assert validation["support_state"] == "provisional_worker_selftest"
    assert validation["verdict"] == "blocked"
    assert validation["accepted"] is False and validation["release_grade"] is False
    assert validation.get("selftest_status") is None
    assert validation.get("selftest_result") is None
    assert validation["result"]["exact_root_kernel_replay"] == "provisional_pass"
    assert validation["result"]["accepted_root_closed"] is False
    assert validation["result"]["audit_complete"] is False
    assert validation["result"]["theorem_complete"] is False

    assert proof["result"]["root_kernel_closed"] is True
    assert proof["result"]["accepted_root_closed"] is False
    assert proof["accepted_closed_obligation_ids"] == []
    assert instance["lifecycle"] == "planned"
    assert instance["root_vector"] == {"H": "H1", "M": "M3", "R": "R3"}
    assert instance["accepted_proof_state"] == []
    assert instance["accepted_receipt_ids"] == []
    assert instance["audit_complete"] is False and instance["theorem_complete"] is False
    assert statement["canonical_formal_target"]["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256

    assert spec["schema_version"] == "stage1-release-recipe/1.0"
    assert spec["item_id"] == ITEM and spec["theorem_id"] == THEOREM
    assert spec["argv"] == [
        "python3", "-I", "-B", f"Stage1_Instances/{THEOREM}/check_release.py"
    ]
    assert spec["cwd"] == "." and spec["network_policy"] == "denied"
    assert spec["expected_exit"] == 0

    assert decision["schema_version"] == "stage1-release-decision/1.0"
    assert decision["item_id"] == ITEM and decision["theorem_id"] == THEOREM
    assert decision["base_revision"] == BASE_REVISION
    assert decision["base_tree"] == BASE_TREE
    assert decision["decision_support"] == "provisional_worker_selftest"
    assert decision["proposed_state"] == "[_]"
    assert decision["verdict"] == "blocked" and decision["release_grade"] is False
    assert decision["lifecycle_before"] == decision["lifecycle_after"] == "planned"
    assert decision["dependency"]["master_accepted"] is False
    assert decision["dependency"]["receipt_accepted"] is False
    assert decision["dependency"]["receipt_release_grade"] is False
    assert decision["accepted_receipt_ids"] == []
    assert decision["root_vector"]["before"] == decision["root_vector"]["after"] == {
        "H": "H1", "M": "M3", "R": "R3"
    }
    assert decision["terminal_decisions"] == {
        "audit_complete": False,
        "theorem_complete": False,
        "audit_z": "blocked",
        "theorem_z": "blocked",
        "release_accepted": False,
    }
    assert decision["first_failed_gate"]["dependency_gate"] == (
        "dependency.S56-M-0957-VALIDATION.master_acceptance"
    )
    for name, digest in decision["reconciled_inputs"].items():
        assert sha256(HERE / name) == digest, f"decision target binding drifted: {name}"
    for relative, digest in decision["shared_group_inspection_inputs"].items():
        assert sha256(ROOT / relative) == digest, f"decision shared binding drifted: {relative}"
    for relative, digest in decision["authority_inputs"].items():
        assert sha256(ROOT / relative) == digest, f"decision authority binding drifted: {relative}"
    for relative, digest in decision["tool_inputs"].items():
        if "/" in relative:
            assert sha256(ROOT / relative) == digest, f"decision tool binding drifted: {relative}"

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["phase"] == "release" and receipt["intent"] == "release"
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]"
    assert receipt["accepted"] is receipt["release_grade"] is receipt["master_accepted"] is False
    assert receipt["verdict"] == "blocked"
    assert receipt["accepted_receipt_ids"] == []
    assert receipt["inspected_parent_ids"] == []
    assert receipt["reused_declaration_ids"] == []
    assert receipt["result"]["accepted_root_closed"] is False
    assert receipt["result"]["audit_complete"] is False
    assert receipt["result"]["theorem_complete"] is False
    assert receipt["result"]["first_failed_gate"] == (
        "dependency.S56-M-0957-VALIDATION.master_acceptance"
    )
    for relative, digest in receipt["input_bindings"].items():
        assert sha256(ROOT / relative) == digest, f"receipt input binding drifted: {relative}"
    assert receipt["commands"] and receipt["output_summary"]
    assert receipt["release_checker_stdout_sha256"] == STDOUT_SHA256
    release_command = next(
        row for row in receipt["commands"]
        if row["argv"][-1] == f"Stage1_Instances/{THEOREM}/check_release.py"
    )
    assert release_command["exit_code"] == 0
    assert decision["known_failures"] == receipt["known_failures"]

    expected_changed_paths = {
        ".stage1-worker-selftest.json",
        f"Stage1_Instances/{THEOREM}/check_release.py",
        f"Stage1_Instances/{THEOREM}/dependency-reuse-ledger.json",
        f"Stage1_Instances/{THEOREM}/release-decision.json",
        f"Stage1_Instances/{THEOREM}/release-receipt.json",
        f"Stage1_Instances/{THEOREM}/release-spec.json",
        f"Stage1_Instances/{THEOREM}/release-validation.md",
    }
    assert set(packet) == {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert packet["item_id"] == ITEM and packet["state"] == "[_]"
    assert packet["base_revision"] == BASE_REVISION
    assert set(packet["changed_paths"]) == set(receipt["changed_paths"]) == expected_changed_paths
    assert packet["known_failures"] == receipt["known_failures"]
    packet_release_command = next(
        row for row in packet["commands"]
        if row["argv"] == spec["argv"]
    )
    assert packet_release_command["exit_code"] == 0
    actual_changed = {
        line[3:] for line in git(
            "status", "--short", "--untracked-files=all", "--",
            str(HERE.relative_to(ROOT)), ".stage1-worker-selftest.json",
        ).splitlines()
    }
    assert actual_changed == expected_changed_paths, (actual_changed, expected_changed_paths)

    worker_log = ROOT.parents[1] / "logs" / f"{ITEM}.out"
    if worker_log.is_file():
        log_text = worker_log.read_text(encoding="utf-8", errors="replace")
        executed = re.findall(
            r"(?ms)^exec\n(.*?)(?=\n(?:succeeded|failed) in |\nexec\n|\Z)",
            log_text,
        )
        forbidden_dependency_operations = (
            r"(?:^|[;&|]\s*|(?:/bin/)?bash\s+-lc\s+['\"])lake\s+(?:update|build)\b",
            r"(?:^|[;&|]\s*|(?:/bin/)?bash\s+-lc\s+['\"])git\s+(?:clone|fetch|pull)\b.*?\.lake",
        )
        assert not any(
            re.search(pattern, command)
            for command in executed
            for pattern in forbidden_dependency_operations
        ), "worker log records a mutable Lean dependency operation"

    report = (HERE / "release-validation.md").read_text(encoding="utf-8")
    for marker in (
        "The release verdict is `blocked`",
        "`audit_complete` and `theorem_complete` are false",
        "`AUDIT-Z` nor `THEOREM-Z` is accepted",
        "no reused declaration or proof credit",
        "no accepted proof state",
    ):
        assert marker in report, marker

    assert_no_prohibited_constructs()
    for path in [
        *(HERE / name for name in EXPECTED_RELEASE_INPUTS),
        HERE / "dependency-reuse-ledger.json",
        HERE / "check_release.py",
    ]:
        assert_text_hygiene(path)

    for line in SUMMARY_LINES:
        print(line)


if __name__ == "__main__":
    main()
