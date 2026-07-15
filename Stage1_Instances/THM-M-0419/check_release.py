#!/usr/bin/env python3
"""Fail-closed release reconciliation for S56-M-0419-RELEASE."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0419"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
ITEM = "S56-M-0419-RELEASE"
THEOREM = "THM-M-0419"
BASE_REVISION = "9faf2e13566ce7ad1047f54337157387eaed48bf"
BASE_TREE = "438505eefd23e6c86d2100b87e98212be6fd8675"
EXPRESSION_SHA256 = "d30ce90a242e9fe3900ec73e893184ad8878c5b90f5362a4f70ca3846342faeb"
DENOMINATOR_SHA256 = "84b22238b8c01210c72a112261776db3e96002fde700709d0336a2d07d799f71"
VALIDATION_RECEIPT_SHA256 = "6bdcf527c120971ef22e5fc29670f43a1de1f23cd5aa0254fa4173a729265b76"
ROOT_CUT = [
    "M0419-B-INDUCTION",
    "M0419-L-TAME",
    "M0419-L-WILD-ODD",
    "M0419-L-WILD-TWO",
    "M0419-T-GLOBAL",
]
ASSURANCE_CUT = [
    "M0419-X-SOURCE",
    "M0419-S-FOUNDATION",
    "M0419-X-PROVENANCE",
    "M0419-X-TRUST",
    "M0419-X-READABLE",
    "M0419-X-WORKFLOW",
]
EXPECTED_INPUTS = {
    "intake.json": "78e7d42738df7cfd74a442e98cc04901fbf3cde72d378a2c5844d8f0509f6ef4",
    "README.md": "57e19f08d16e9ef284c77fce95e978d4bfd47b8e6181337459c17488c30278ae",
    "source_statement_crosswalk.md": "723dfb771a2cef56c49441766c041291c87d2b809c716b4751f6fd2560b568f5",
    "statement.json": "ee0354ca1c5bc7ea046199e6c19e90b88beddfd51a0f3540d029f84dd0fee5de",
    "anchor-audit.json": "e2c1faabe061196d98145375329356da99ee7970be16728dec5f8e7e7f133f70",
    "obligation-registry.json": "860e52d35f41f870858a3d2d1b230b7a2418bcf17c374efa618d62f93bd1dd7b",
    "typed-graphs.json": "a4385d65ac70f1d772b4e8d1d3f06607a5ba893534c555d70488d1c7f78f85ae",
    "proof-phase.json": "1f61e2a0371665484a49a30dcdc9d7593da600f26f31018c05e58c9f6a122f85",
    "proof-receipt.json": "c28bfe7d41195ff701a50c0f5eede7f5720feb4f21869d32b651f7557004ff59",
    "proof-blocker.json": "92934ec809b1f2dad3364af9d69e791d4536b51822722527d821a4858b05939f",
    "validation-spec.json": "0bb12d18104e4727c74d8f02b1967b01e386ef2e2c46b637774ea05aea912dd8",
    "validation-receipt.json": VALIDATION_RECEIPT_SHA256,
    "validation-blocker.json": "823c6755603b1f756dad6aa03e5798a165a5d27d77d887abc80b6be88b981989",
    "Statement.lean": "db9efe3e6fbf82023500558480b83a88b583a51444272f2ee642a05fd38a0422",
    "ObligationTree.lean": "ac4ad27955b95ee77f2747cde2aea5f0552de2e7a009fb0b4aea39a8d8a38951",
    "Proof.lean": "1a42f62f56c5f62df0d9e5ee245f68a77fb44e7e42240dcbb9db7e5863220f7a",
    "Validation.lean": "7bea8975fad9200c37dd89405eeaef832a302fe4b1536755904a99961d86d21f",
    "check_proof.sh": "ac0d8a0b762e7675f8448f9870343fccc113e8fc4efbb100c3e0e1403f6a39df",
    "check_validation.py": "964f3ab3123bdb7dac32bdadc9270dd493a903303be12f89c654bf420cec5a4f",
}
EXPECTED_AUTHORITY_INPUTS = {
    "Docs/Stage1_Blueprint_rev-5.6.md": "15f10ace28b2c91b49ea51765374fde98bd11f9457fd491c23c6db369cae970a",
    "Docs/Stage1_Targets_rev-5.6.json": "02eec284de534dd78e1cf75f82a477ff477567dd682b7445cb7587abd137ab2c",
    "Docs/Stage1_Execution_DAG_rev-5.6.json": "2a1712d2fa5980d1251a181d2db7547dd710d8a4cc2647bafc34c18d9043de67",
    "Docs/Blueprint_Guidelines.md": "a06c07b5ca1b270b4935ad3dab893e9a0e078c29c8da2ef9dca1e71193310535",
    "skills/execute-stage1-rev56/SKILL.md": "26d47a66c6535feabb8bbf1051fd55d76a53fe761f4b3d953f86b97ec86152b8",
    "Formalizations/Lean/lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "Formalizations/Lean/lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
EXPECTED_RELEASE_OUTPUTS = {
    "release-spec.json": "9121d2fc4346e76b135187dd71394ab181d78a4c3c02cd72307202202133f5fe",
    "release-decision.json": "54e001bc4c805b8483e17c16492ce88fce844e2e7712bc650d4d0bf4f4c7fb70",
    "release-validation.md": "45541edf692b8f8f0302020569529d9b76e28f13d8afa7438996736206ee0dd8",
}
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/check_release.py",
    f"Stage1_Instances/{THEOREM}/release-decision.json",
    f"Stage1_Instances/{THEOREM}/release-receipt.json",
    f"Stage1_Instances/{THEOREM}/release-spec.json",
    f"Stage1_Instances/{THEOREM}/release-validation.md",
}
SUMMARY_LINES = [
    "PASS release reconciliation: target, DAG, receipts, registry, graphs, and hashes agree",
    "PASS narrow Lean replay: exact statement, conditional composition, and partial cyclotomic transport checked at trust zero",
    "BLOCKED S56-10.2-DEPENDENCY-ACCEPTANCE: validation is provisional and not master accepted",
    "BLOCKED exact root: H1/M3/R3 unchanged; five mathematical packages remain open",
    "BLOCKED AUDIT-Z and THEOREM-Z: source/readability, trust, hermetic, and independent gates are open",
    "verdict=blocked audit_complete=false theorem_complete=false accepted_receipts=0",
]


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


def run(argv: list[str], *, cwd: Path = ROOT, timeout: int = 600) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        argv,
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=timeout,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(f"command failed ({result.returncode}): {argv!r}\n{result.stdout}")
    return result


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["git", *args], cwd=cwd, timeout=60).stdout.strip()


def assert_text_hygiene(path: Path) -> None:
    data = path.read_bytes()
    assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())


def main() -> None:
    if sys.flags.optimize != 0:
        raise RuntimeError("release checker requires Python assertions")

    decision = load(HERE / "release-decision.json")
    receipt = load(HERE / "release-receipt.json")
    spec = load(HERE / "release-spec.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")
    validation = load(HERE / "validation-receipt.json")
    proof = load(HERE / "proof-receipt.json")
    proof_phase = load(HERE / "proof-phase.json")
    statement = load(HERE / "statement.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    targets = load(ROOT / "Docs" / "Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 74 and target["baseline"] == "L0"
    assert target["lifecycle_mode"] == "planned"
    assert target["rework_required"] is True and target["theorem_complete"] is False
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item == {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 74,
        "phase": "release",
        "layer": 6,
        "state": "[ ]",
        "depends_on": ["S56-M-0419-VALIDATION"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Reconcile evidence and decide the exact theorem-completion verdict.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }
    predecessor = next(
        row for row in execution["items"] if row["id"] == "S56-M-0419-VALIDATION"
    )
    assert predecessor["state"] == "[_]" and predecessor["attempts"] == 1

    for name, expected in EXPECTED_INPUTS.items():
        assert sha256(HERE / name) == expected, f"reconciled input drifted: {name}"
    for relative, expected in EXPECTED_AUTHORITY_INPUTS.items():
        assert sha256(ROOT / relative) == expected, f"authority input drifted: {relative}"
    for name, expected in EXPECTED_RELEASE_OUTPUTS.items():
        assert sha256(HERE / name) == expected, f"release output drifted: {name}"
    assert decision["reconciled_inputs"] == EXPECTED_INPUTS
    assert decision["authority_inputs"] == EXPECTED_AUTHORITY_INPUTS

    assert statement["elaborated_output_sha256"] == EXPRESSION_SHA256
    assert registry["root_obligation_id"] == graphs["root_node_id"] == "M0419-ROOT"
    assert len(registry["frozen_denominators"]["inventory"]) == 25
    assert graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    closure = graphs["closure_boundary"]
    assert closure["accepted_closed_obligations"] == []
    assert closure["root_closed"] is closure["audit_complete"] is closure["theorem_complete"] is False
    assert closure["authoritative_root_vector"] == {"H": "H1", "M": "M3", "R": "R3"}
    assert closure["minimal_open_proof_cut_set"] == ROOT_CUT
    assert closure["remaining_root_assurance_cut_set"] == ASSURANCE_CUT

    assert proof["accepted"] is False and proof["accepted_closed_obligation_ids"] == []
    assert proof["proposed_closed_obligation_ids"] == ["M0419-C-CYCLOTOMIC-IDENTIFY"]
    assert proof["root_closed"] is proof["audit_complete"] is proof["theorem_complete"] is False
    assert proof["remaining_root_cut_set"] == ROOT_CUT
    assert proof_phase["accepted_closed_obligation_ids"] == []
    assert proof_phase["remaining_root_cut_set"] == ROOT_CUT

    assert sha256(HERE / "validation-receipt.json") == VALIDATION_RECEIPT_SHA256
    assert validation["item_id"] == "S56-M-0419-VALIDATION"
    assert validation["support_state"] == "provisional_worker_selftest"
    assert validation["proposed_state"] == "[_]"
    assert validation["accepted"] is validation["release_grade"] is False
    assert validation["verdict"] == "blocked" and validation["accepted_receipt_ids"] == []
    result = validation["result"]
    assert result["accepted_closed_obligation_ids"] == []
    assert result["root_closed"] is result["root_kernel_closed"] is False
    assert result["root_machine_debt"] == "M3"
    assert result["remaining_root_cut_set"] == ROOT_CUT
    assert result["audit_complete"] is result["theorem_complete"] is False
    assert validation["hermeticity"]["decision"] == "fail_closed_nonrelease_warm_cache_replay"
    assert validation["independent_validation"]["decision"] == "fail_closed"

    assert spec["item_id"] == decision["item_id"] == receipt["item_id"] == ITEM
    assert spec["theorem_id"] == decision["theorem_id"] == receipt["theorem_id"] == THEOREM
    assert decision["verdict"] == receipt["verdict"] == "blocked"
    assert decision["lifecycle_before"] == decision["lifecycle_after"] == "planned"
    assert decision["accepted_receipt_ids"] == receipt["accepted_receipt_ids"] == []
    terminal = decision["terminal_decisions"]
    assert terminal == {
        "audit_complete": False,
        "theorem_complete": False,
        "audit_z": "blocked",
        "theorem_z": "blocked",
    }
    assert decision["first_failed_gate"]["gate_id"] == "S56-10.2-DEPENDENCY-ACCEPTANCE"
    assert decision["minimal_open_proof_cut_set"] == ROOT_CUT
    assert decision["remaining_root_assurance_cut_set"] == ASSURANCE_CUT
    dependency = decision["dependency"]
    assert dependency["item_id"] == validation["item_id"]
    assert dependency["receipt_id"] == validation["receipt_id"]
    assert dependency["receipt_sha256"] == VALIDATION_RECEIPT_SHA256
    assert dependency["master_accepted"] is dependency["receipt_accepted"] is False

    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]"
    assert receipt["accepted"] is receipt["release_grade"] is receipt["master_accepted"] is False
    assert receipt["result"]["root_vector_before"] == receipt["result"]["root_vector_after"] == [
        "H1", "M3", "R3"
    ]
    assert receipt["result"]["minimal_open_proof_cut_set"] == ROOT_CUT
    assert receipt["result"]["audit_complete"] is receipt["result"]["theorem_complete"] is False
    assert receipt["result"]["audit_z"] == receipt["result"]["theorem_z"] == "blocked"
    assert receipt["result"]["first_failed_gate"] == "S56-10.2-DEPENDENCY-ACCEPTANCE"
    assert receipt["changed_paths"] == sorted(CHANGED_PATHS)
    assert packet["item_id"] == ITEM
    assert packet["changed_paths"] == receipt["changed_paths"]
    assert packet["base_revision"] == BASE_REVISION
    assert packet["known_failures"] == receipt["known_failures"]
    assert packet["state"] == "[_]"
    assert isinstance(packet["commands"], list) and packet["commands"]
    assert isinstance(packet["output_summary"], str) and packet["output_summary"]

    status = git("status", "--short", "--untracked-files=all").splitlines()
    actual = {line[2:].lstrip() for line in status}
    actual.discard("Formalizations/Lean/.lake")
    assert actual == CHANGED_PATHS
    assert (LEAN_ROOT / ".lake").is_symlink()
    for path in [HERE / name for name in EXPECTED_INPUTS] + [HERE / name for name in EXPECTED_RELEASE_OUTPUTS]:
        assert_text_hygiene(path)

    replay = run(["bash", str(HERE / "check_proof.sh")])
    assert "PASS THM-M-0419 isolated Lean replay: M0419-C-CYCLOTOMIC-IDENTIFY checked" in replay.stdout
    assert "Stage1.THM_M_0419.Proof.cyclotomicIdentify" in replay.stdout
    assert "sorryAx" not in replay.stdout and "error:" not in replay.stdout

    summary = "\n".join(SUMMARY_LINES) + "\n"
    assert receipt["output_evidence"]["stdout_semantic_sha256"] == hashlib.sha256(
        summary.encode()
    ).hexdigest()
    print(summary, end="")


if __name__ == "__main__":
    main()
