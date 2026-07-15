#!/usr/bin/env python3
"""Fail-closed narrow validation for S56-M-1065-VALIDATION."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import platform
import re
import shutil
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-1065"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
TOOLCHAIN_BIN = Path.home() / ".elan/toolchains/leanprover--lean4---v4.29.0/bin"

ITEM = "S56-M-1065-VALIDATION"
THEOREM = "THM-M-1065"
BASE_REVISION = "3c3068d5f6ad9d773ce52d46d68a43c2a9272683"
BASE_TREE = "f9413d0895f280a855bb16104daf0403d51a24fb"
EXPRESSION_SHA256 = "b257ceb188a0b84aab11fd389b5df322129c283dbc38f5c226900a4fec5cebd0"
DENOMINATOR_SHA256 = "d5e21a3abc7d96576d5aeba4b8377a8ef8d92136b5ed448f9f28723f00d91ac2"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MATHLIB_REMOTE = "https://github.com/leanprover-community/mathlib4.git"
MATHLIB_LICENSE_SHA256 = "b40930bbcf80744c86c46a12bc9da056641d722716c378f5659b9e555ef833e1"
TOOLCHAIN_SHA256 = "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2"
MANIFEST_SHA256 = "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81"
LEAN_SHA256 = "3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf"
LAKE_SHA256 = "a608ff084d7e2af228b92a29d7c2fd083ba0580e46889175ec74a81678c98359"
PYTHON_SHA256 = "b8d8288faefdd300201f43fcf00f6f539a27218eeed3a3dff5ab10b9c4c99700"
GIT_SHA256 = "8a48eefa306b9a2a9c3e576784a74ad7485779279e5a46ec43361a1864760e45"
BWRAP_SHA256 = "0abea81db798ebf6b4742ac0664802d97521547a353c2a0dbdc21d76cbbfd2c0"
ALLOWED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
FROZEN_CUT = [
    "M1065-C-SPACE",
    "M1065-L-BLOCK-COUPLING",
    "M1065-L-MAXIMAL-TAIL",
]
EXPECTED_INPUTS = {
    "Statement.lean": "7f3b249e058dcdc4410c966622b1d707daff6cd486a0666bf3c0c8cf1e2edaf1",
    "ObligationTree.lean": "9aa9a38f406f2d8f38deaeb919d41af053547b4e8322d6ec99b3496e03ab5873",
    "Proof.lean": "e445a607d6291e1a8991551c4cc6d3140146df2213637d468a9753b586fae5fb",
    "AnchorAudit.lean": "64d04f6cdbf62fc7aea44798f914010dc12d66abbfd5c9ea1a7e8445135930c9",
    "Validation.lean": "edb1c9a3b2d54adeb5b2d27e3aa457409b12d4727f29c960265a111fb8d8775e",
    "instance.json": "85818edf62136acee862596b776b9f09e75f39ee8113e10ffff76de7f3146af1",
    "task-dag.json": "7e35f3ac1f43d0d85b65129924390270dc1efba4c8a5bb7e329b657d4f240f77",
    "statement.json": "940f961fc3d0970df44a354edccea84ecfcaf76fec6321348387792fda748995",
    "anchor-audit.json": "ecb5d943f920d43832fe007283321c777a72a96fb8d9f81f6e8dbe3134973d27",
    "obligation-registry.json": "79eb5a4cc430f81c41baf2b70160f82037a600b795cf1d7dd4c23bdee27a7b44",
    "typed-graphs.json": "dcb4876d08a30eb8dc5bf604e18ac7e83c0fa864c04ef808bf720ceeb41c325c",
    "proof-receipt-2026-07-15-head-72a35d5f-slot53.json": (
        "b7b86cdf1f471181478650e294524ca7aeeee844da575a8ef84a455388803e47"
    ),
    "proof-blocker-2026-07-15-head-72a35d5f-slot53.json": (
        "bdd292d4c86e54538d290788fa00b5c9b51b15e3cd8c5410cd593ef7e48fdd3d"
    ),
    "check_proof.sh": "95d2ad0b4b4910176b1ebffdea8e03aa6ed72e479f0f5f0b2b80ce18d4567022",
    "check_validation.sh": "a912f589d69ef3b7a889a95b8f7de2deeeaad441d090f49c94e43bf4f0bf7be1",
    "validation-spec.json": "2b11c9fa03483f4207a50b992edc1e796947d8a9a65aaabad0cdcd012aa592ce",
    "validation-phase.md": "bcd67abc4f9db20729ae470a0eac0f80c778367d3c4b65c4e81110f0796a9a47",
    "validation-blocker.json": "9c23446b22b63b77854ba84a1a2f2c8a730fd3eff384b5d3771f89c1a50dcaf5",
}
SELECTED_MATHLIB = {
    "Mathlib/Probability/HasLawExists.lean": {
        "blob": "a0bb5807d52562981ecfdb0cd36abc92a02ea29b",
        "source_sha256": "de026870cd46baaebc3562fa0bc8df9dcc364323b8f5aaa1842f55df3f4d312b",
        "olean_sha256": "6532760ef828805bc51b6d9dda0f209567c977405869849b706c41db90ca36e9",
    },
    "Mathlib/Probability/Distributions/Gaussian/Real.lean": {
        "blob": "f5795fbfb92475879b67b0ee8577687575a82258",
        "source_sha256": "f5321db08f0156c5a12e15986d2ced9108183c907e3082d2566da8ef8da931a8",
        "olean_sha256": "b5894530bc315c897142ff650c774ed5ee3180b1df45690021fdd830e6e82ea4",
    },
    "Mathlib/Probability/Independence/Basic.lean": {
        "blob": "cd1d3a773dce98f7e146f2099055e552c6ba0118",
        "source_sha256": "67f71d5c3d32371ad4822fc29f0db84bb0cffbbab24f82ae2f88702152ffe33b",
        "olean_sha256": "b01ba1680e1314dd542516e46eda73efb2d5b4c1d7c911a31117aa1391e1a4c4",
    },
    "Mathlib/MeasureTheory/Constructions/Pi.lean": {
        "blob": "5f0f7f9209e3a2608c555cacb2ad994ee0c734cf",
        "source_sha256": "fc458dc8dcc870458fbd4f6146cc3b4494cf08fdb9db78b657584c3eba894a9e",
        "olean_sha256": "3edb94ce8ead5ecb56620ba5a735372d52e024949a96879dfaea662a76637647",
    },
}
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/Validation.lean",
    f"Stage1_Instances/{THEOREM}/check_validation.py",
    f"Stage1_Instances/{THEOREM}/check_validation.sh",
    f"Stage1_Instances/{THEOREM}/validation-blocker.json",
    f"Stage1_Instances/{THEOREM}/validation-phase.md",
    f"Stage1_Instances/{THEOREM}/validation-receipt.json",
    f"Stage1_Instances/{THEOREM}/validation-spec.json",
}
SUMMARY = (
    "PASS THM-M-1065 narrow validation",
    "PASS network-isolated trust-zero replay: exact statement, conditional composition, two partial proof bodies, two anchor decisions, and two differential statement probes elaborated",
    "PASS trust observation: all checked declarations are sorry-free and use no axioms beyond propext, Classical.choice, and Quot.sound",
    "PASS selected provenance: frozen local hashes, tracked-clean pinned mathlib revision/tree/remote/license, and four source/blob/olean boundaries agree",
    "FAIL CLOSED root: dependent KMT coupling, finite-block construction, and uniform maximal-tail packages remain open at M4",
    "FAIL CLOSED authority/trust: proof master acceptance and complete transitive foundation, provenance, and TCB closure remain open",
    "FAIL CLOSED hermetic release: shared warm .lake is not a clean empty-cache cold offline replay",
    "FAIL CLOSED independent release: same-worker differential checks are not a distinct signed verifier",
    "audit_complete=false; theorem_complete=false",
)


def fail(message: str) -> None:
    raise SystemExit(f"FAIL THM-M-1065 validation: {message}")


def load(path: Path) -> dict:
    def reject_duplicates(pairs: list[tuple[str, object]]) -> dict:
        result: dict[str, object] = {}
        for key, value in pairs:
            if key in result:
                fail(f"duplicate JSON key {key!r} in {path.relative_to(ROOT)}")
            result[key] = value
        return result

    try:
        value = json.loads(
            path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicates
        )
    except (OSError, json.JSONDecodeError) as error:
        fail(f"cannot load {path.relative_to(ROOT)}: {error}")
    if not isinstance(value, dict):
        fail(f"expected a JSON object in {path.relative_to(ROOT)}")
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(argv: list[str], *, cwd: Path = ROOT, timeout: int = 900) -> str:
    result = subprocess.run(
        argv,
        cwd=cwd,
        env={
            **os.environ,
            "LANG": "C.UTF-8",
            "LC_ALL": "C.UTF-8",
            "TZ": "UTC",
            "LEAN_NUM_THREADS": "1",
        },
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=timeout,
        check=False,
    )
    if result.returncode:
        fail(f"command exited {result.returncode}: {argv!r}\n{result.stdout}")
    return result.stdout


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["git", *args], cwd=cwd, timeout=60).rstrip()


def lean_without_comments(source: str) -> str:
    output: list[str] = []
    index = 0
    depth = 0
    in_string = False
    escaped = False
    while index < len(source):
        char = source[index]
        pair = source[index:index + 2]
        if depth:
            if pair == "/-":
                depth += 1
                output.extend("  ")
                index += 2
            elif pair == "-/":
                depth -= 1
                output.extend("  ")
                index += 2
            else:
                output.append("\n" if char == "\n" else " ")
                index += 1
        elif in_string:
            output.append(char)
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
            index += 1
        elif pair == "/-":
            depth = 1
            output.extend("  ")
            index += 2
        elif pair == "--":
            while index < len(source) and source[index] != "\n":
                output.append(" ")
                index += 1
        else:
            output.append(char)
            if char == '"':
                in_string = True
            index += 1
    if depth or in_string:
        fail("unterminated Lean comment or string during hygiene scan")
    return "".join(output)


def assert_text_hygiene(path: Path) -> None:
    data = path.read_bytes()
    assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())


def main() -> None:
    if not __debug__:
        fail("Python assertions must be enabled")

    spec = load(HERE / "validation-spec.json")
    receipt = load(HERE / "validation-receipt.json")
    blocker = load(HERE / "validation-blocker.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")
    targets = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    instance = load(HERE / "instance.json")
    task_dag = load(HERE / "task-dag.json")
    statement = load(HERE / "statement.json")
    anchor = load(HERE / "anchor-audit.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    proof_receipt = load(
        HERE / "proof-receipt-2026-07-15-head-72a35d5f-slot53.json"
    )
    proof_blocker = load(
        HERE / "proof-blocker-2026-07-15-head-72a35d5f-slot53.json"
    )

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 507 and target["baseline"] == "L0"
    assert target["lifecycle_mode"] == "planned"
    assert target["rework_required"] is True and target["theorem_complete"] is False
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item == {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 507,
        "phase": "validation",
        "layer": 5,
        "state": "[ ]",
        "depends_on": ["S56-M-1065-PROOF"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Run hermetic kernel, trust, provenance, and independent validation gates.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }
    predecessor = next(
        row for row in execution["items"] if row["id"] == "S56-M-1065-PROOF"
    )
    assert predecessor["state"] == "[_]" and predecessor["attempts"] == 1
    local_task = next(row for row in task_dag["tasks"] if row["id"] == ITEM)
    assert local_task["state"] == "open"
    assert local_task["depends_on"] == ["S56-M-1065-PROOF"]
    assert task_dag["accepted_states"] == []

    assert instance["root_vector"] == {"H": "H2", "M": "M4", "R": "R4"}
    assert instance["accepted_proof_state"] == []
    assert instance["audit_complete"] is instance["theorem_complete"] is False
    formal = statement["canonical_formal_target"]
    assert formal["declaration_or_expression"] == (
        "Stage1Instances.THM_M_1065.KMTStrongApproximationTarget"
    )
    assert formal["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert formal["statement_file_sha256"] == EXPECTED_INPUTS["Statement.lean"]
    assert anchor["canonical_target_expression_sha256"] == EXPRESSION_SHA256
    assert anchor["root_decision"]["kernel_closed"] is False
    assert anchor["theorem_complete"] is False

    assert registry["root_obligation_id"] == graphs["root_node_id"] == "M1065-ROOT"
    denominator = registry["frozen_denominators"]
    denominator_digest = hashlib.sha256(
        json.dumps(denominator, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    assert denominator_digest == graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    rows = registry["obligations"]
    assert len(rows) == 18
    assert all(row["terminal_proof_body_id"] is None for row in rows)
    nodes = graphs["nodes"]
    assert len(nodes) == 18
    assert all(node["evidence_ids"] == [] for node in nodes)
    assert all(node["validation_spec_id"].endswith("-PENDING") for node in nodes)
    closure = graphs["closure_boundary"]
    assert closure["closed_obligations"] == []
    assert closure["root_closed"] is False and closure["root_machine_debt"] == "M4"
    assert closure["remaining_root_cut_set"] == FROZEN_CUT
    assert closure["audit_complete"] is closure["theorem_complete"] is False

    assert proof_receipt["support_state"] == "provisional_worker_selftest"
    assert proof_receipt["accepted"] is False
    assert proof_receipt["supported_obligation_ids"] == []
    assert proof_receipt["provisionally_closed_obligation_ids"] == []
    assert proof_receipt["accepted_closed_obligation_ids"] == []
    assert proof_receipt["result"]["root_kernel_closed"] is False
    assert proof_receipt["remaining_root_cut_set"] == FROZEN_CUT
    assert proof_blocker["root_closed"] is proof_blocker["theorem_complete"] is False
    assert proof_blocker["remaining_root_cut_set"] == FROZEN_CUT

    for name, expected in EXPECTED_INPUTS.items():
        actual = sha256(HERE / name)
        if actual != expected:
            fail(f"stale validation input {name}: expected {expected}, got {actual}")
        assert receipt["inputs"][name] == expected
    assert sha256(LEAN_ROOT / "lean-toolchain") == TOOLCHAIN_SHA256
    assert sha256(LEAN_ROOT / "lake-manifest.json") == MANIFEST_SHA256

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by|run_tac|extern)\b|"
        r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
        r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
        r"(?:axiom|constant|opaque|unsafe)\b",
        re.MULTILINE,
    )
    for name in (
        "Statement.lean", "ObligationTree.lean", "Proof.lean",
        "AnchorAudit.lean", "Validation.lean",
    ):
        source = lean_without_comments((HERE / name).read_text(encoding="utf-8"))
        assert prohibited.search(source) is None, f"prohibited source construct in {name}"
    validation_source = lean_without_comments(
        (HERE / "Validation.lean").read_text(encoding="utf-8")
    )
    assert "import Proof" not in validation_source
    assert "import ObligationTree" not in validation_source
    assert "KMTStrongApproximationTarget := by" not in validation_source
    for forbidden in (
        "exists_commonIIDSequences",
        "measurableSet_discrepancyEvent",
        "kmtTarget_iff_couplingData",
    ):
        assert forbidden not in validation_source

    manifest = load(LEAN_ROOT / "lake-manifest.json")
    mathlib_entry = next(row for row in manifest["packages"] if row["name"] == "mathlib")
    assert mathlib_entry["rev"] == mathlib_entry["inputRev"] == MATHLIB_REVISION
    assert MATHLIB.resolve().is_dir(), "pinned mathlib artifact is unavailable"
    assert git("rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert git("remote", "get-url", "origin", cwd=MATHLIB) == MATHLIB_REMOTE
    # Concurrent workers can create untracked scratch directories below the shared canonical
    # checkout. Tracked cleanliness plus selected source/blob/olean hashes is the stable bounded
    # observation; untracked shared-cache material keeps this receipt nonrelease.
    assert git("status", "--porcelain=v1", "--untracked-files=no", cwd=MATHLIB) == ""
    assert sha256(MATHLIB / "LICENSE") == MATHLIB_LICENSE_SHA256
    assert anchor["immutable_environment"]["mathlib_revision"] == MATHLIB_REVISION

    for relative, expected in SELECTED_MATHLIB.items():
        source = MATHLIB / relative
        olean = MATHLIB / ".lake/build/lib/lean" / relative.replace(".lean", ".olean")
        assert git("rev-parse", f"HEAD:{relative}", cwd=MATHLIB) == expected["blob"]
        assert sha256(source) == expected["source_sha256"]
        assert sha256(olean) == expected["olean_sha256"]
        assert receipt["provenance"]["selected_mathlib_sources"][relative] == expected

    lean = TOOLCHAIN_BIN / "lean"
    lake = TOOLCHAIN_BIN / "lake"
    python = Path(os.path.realpath(sys.executable))
    git_executable = shutil.which("git")
    bwrap = shutil.which("bwrap")
    assert git_executable is not None and bwrap is not None
    assert sha256(lean) == LEAN_SHA256 and sha256(lake) == LAKE_SHA256
    assert sha256(python) == PYTHON_SHA256
    assert sha256(Path(os.path.realpath(git_executable))) == GIT_SHA256
    assert sha256(Path(os.path.realpath(bwrap))) == BWRAP_SHA256
    lean_version = run([str(lean), "--version"], timeout=60)
    lake_version = run([str(lake), "--version"], timeout=60)
    assert "4.29.0" in lean_version
    assert "98dc76e3c0a9b856c9b98726b713fb04fab16740" in lean_version
    assert "5.0.0-src+98dc76e" in lake_version

    replay = run(["bash", str(HERE / "check_validation.sh")], timeout=650)
    assert replay.count("Declarations are sorry-free!") == 9
    assert "sorryAx" not in replay and "declaration uses 'sorry'" not in replay
    assert "no unexpected axioms" in replay

    assert spec["schema_version"] == "stage1-validation-spec/1.0"
    assert spec["item_id"] == ITEM and spec["theorem_id"] == THEOREM
    assert spec["cwd"] == "."
    assert spec["argv"] == [
        "python3", "-I", "-B", f"Stage1_Instances/{THEOREM}/check_validation.py"
    ]
    assert spec["env_allowlist"] == {} and spec["timeout_seconds"] == 900
    assert spec["network_policy"] == "denied"
    assert "bubblewrap --unshare-net" in spec["network_enforcement"]
    assert spec["expected_exit"] == 0
    assert len(spec["covered_obligation_ids"]) == len(set(spec["covered_obligation_ids"]))
    assert set(spec["covered_obligation_ids"]) <= {row["obligation_id"] for row in rows}

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == blocker["item_id"] == ITEM
    assert receipt["theorem_id"] == blocker["theorem_id"] == THEOREM
    assert receipt["phase"] == "validation" and receipt["intent"] == "validate"
    assert receipt["depends_on"] == ["S56-M-1065-PROOF"]
    assert receipt["base_revision"] == blocker["base_revision"] == BASE_REVISION
    assert receipt["base_tree"] == blocker["base_tree"] == BASE_TREE
    assert receipt["support_state"] == blocker["support_state"] == (
        "provisional_worker_selftest"
    )
    assert receipt["proposed_state"] == blocker["proposed_state"] == "[_]"
    assert receipt["accepted"] is blocker["accepted"] is False
    assert receipt["verdict"] == blocker["verdict"] == "blocked"
    assert receipt["release_grade"] is False and receipt["signature"] is None
    assert receipt["canonical_target"] == {
        "declaration": "Stage1Instances.THM_M_1065.KMTStrongApproximationTarget",
        "elaborated_expression_sha256": EXPRESSION_SHA256,
        "statement_source_sha256": EXPECTED_INPUTS["Statement.lean"],
        "registry_denominator_sha256": DENOMINATOR_SHA256,
    }
    for key in (
        "recipe_id", "cwd", "argv", "env_allowlist", "timeout_seconds",
        "network_policy", "network_enforcement", "expected_exit", "expected_outputs",
        "covered_obligation_ids", "covered_declarations", "scope_boundary",
    ):
        assert receipt["recipe"][key] == spec[key], key
    assert receipt["inputs"]["check_validation.py"] == "self_hash_structurally_bound"
    assert receipt["inputs"]["validation-receipt.json"] == "self_excluded"

    environment = receipt["environment"]
    assert environment["platform"] == (
        f"{platform.system()} {platform.release()} {platform.machine()}"
    )
    assert environment["lean_executable_sha256"] == LEAN_SHA256
    assert environment["lake_executable_sha256"] == LAKE_SHA256
    assert environment["python_executable_sha256"] == PYTHON_SHA256
    assert environment["git_executable_sha256"] == GIT_SHA256
    assert environment["bubblewrap_executable_sha256"] == BWRAP_SHA256
    assert environment["mathlib_revision"] == MATHLIB_REVISION
    assert environment["mathlib_tree"] == MATHLIB_TREE
    assert environment["mathlib_remote"] == MATHLIB_REMOTE
    assert environment["mathlib_license_sha256"] == MATHLIB_LICENSE_SHA256

    result = receipt["result"]
    assert result["exact_statement_replay"] == "pass"
    assert result["partial_proof_replay"] == "pass_no_frozen_obligation_credit"
    assert result["same_worker_differential_statement_replay"] == "pass"
    assert result["placeholder_and_unsafe_scan"] == "pass"
    assert set(result["observed_axioms"]) == ALLOWED_AXIOMS
    assert result["network_isolated_lean_replay"] == "pass"
    assert result["raw_replay_output_sha256"] == (
        "aa65e369656f328f9972b1621532c1cc16084243008480e1e2662b137af0097b"
    )
    assert result["raw_replay_output_bytes"] == 1780
    assert result["proof_master_acceptance"] == "fail_closed"
    assert result["root_kernel_closed"] is result["accepted_root_closed"] is False
    assert result["root_machine_debt"] == "M4"
    assert result["frozen_closed_obligation_ids"] == []
    assert result["accepted_closed_obligation_ids"] == []
    assert result["remaining_root_cut_set"] == FROZEN_CUT
    assert result["complete_trust_and_provenance_closure"] == "fail_closed"
    assert result["hermetic_cold_offline_replay"] == "fail_closed"
    assert result["independent_distinct_runner"] == "fail_closed"
    assert result["audit_complete"] is result["theorem_complete"] is False
    assert receipt["root_vector_before"] == receipt["root_vector_after_worker_selftest"] == {
        "H": "H2", "M": "M4", "R": "R4"
    }
    assert receipt["first_failed_gate"] == "dependency.S56-M-1065-PROOF.master_acceptance"
    assert receipt["first_failed_mathematical_gate"] == "M1065-C-SPACE"
    assert receipt["first_failed_release_gate"] == "S56-10.6-HERMETIC-COLD-BUILD"
    assert receipt["accepted_receipt_ids"] == []
    assert blocker["frozen_architecture"]["remaining_root_cut_set"] == FROZEN_CUT
    assert blocker["frozen_architecture"]["root_closed"] is False
    assert blocker["frozen_architecture"]["theorem_complete"] is False
    assert blocker["validation_observations"]["independent_distinct_runner"] == "fail_closed"

    assert set(packet) == {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert packet["item_id"] == ITEM and packet["state"] == "[_]"
    assert packet["base_revision"] == BASE_REVISION
    assert packet["known_failures"] == receipt["known_failures"] == blocker["known_failures"]
    assert set(packet["changed_paths"]) == set(receipt["changed_paths"]) == CHANGED_PATHS
    assert packet["commands"] == [
        "python3 Docs/tools/check_stage1_standard.py",
        "python3 scripts/stage1_target.py check",
        "python3 scripts/stage1_target.py show THM-M-1065",
        "python3 Stage1_Instances/THM-M-1065/check_anchor_audit.py",
        "python3 Stage1_Instances/THM-M-1065/check_obligation_tree.py",
        "bash Stage1_Instances/THM-M-1065/check_validation.sh",
        "python3 -I -B Stage1_Instances/THM-M-1065/check_validation.py",
        "python3 -m json.tool Stage1_Instances/THM-M-1065/validation-spec.json",
        "python3 -m json.tool Stage1_Instances/THM-M-1065/validation-receipt.json",
        "python3 -m json.tool Stage1_Instances/THM-M-1065/validation-blocker.json",
        "python3 -m json.tool .stage1-worker-selftest.json",
        "PYTHONPYCACHEPREFIX=/tmp/stage1-m1065-validation-pycache python3 -m py_compile Stage1_Instances/THM-M-1065/check_validation.py",
        "git diff --check -- Stage1_Instances/THM-M-1065 .stage1-worker-selftest.json",
    ]
    assert "root remains H2/M4/R4" in packet["output_summary"]

    status = git("status", "--short", "--untracked-files=all")
    actual_changed = {
        line[3:]
        for line in status.splitlines()
        if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual_changed == CHANGED_PATHS, (actual_changed, CHANGED_PATHS)
    for relative in CHANGED_PATHS:
        assert_text_hygiene(ROOT / relative)

    for line in SUMMARY:
        print(line)


if __name__ == "__main__":
    try:
        main()
    except (AssertionError, KeyError, StopIteration) as error:
        _, _, traceback = sys.exc_info()
        line = traceback.tb_next.tb_lineno if traceback and traceback.tb_next else "unknown"
        fail(f"invariant failed at line {line}: {error}")
    except subprocess.TimeoutExpired as error:
        fail(f"command timed out after {error.timeout} seconds: {error.cmd!r}")
