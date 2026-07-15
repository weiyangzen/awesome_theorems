#!/usr/bin/env python3
"""Fail-closed release reconciliation for S56-M-1060-RELEASE."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-1060"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM = "S56-M-1060-RELEASE"
THEOREM = "THM-M-1060"
BASE_REVISION = "23d1722530f7b3b136c8b91db99531a51b16fad8"
BASE_TREE = "a7e9dea5be1dcc0304a7385d19d35795a47e04dd"
VALIDATION_BASE = "5cca979173a36d739670a3b5ecad23d89dc96292"
VALIDATION_TREE = "97ccf7381b147bf0f25425a5a7678e51265c6eb3"
VALIDATION_RECEIPT_ID = (
    "S56-M-1060-VALIDATION-network-isolated-20260715T155509+0800-v1"
)
VALIDATION_RECEIPT_SHA256 = (
    "841570057a8ab9fd1fcaa420a280aa8b566778251bbd0d3308916e1b04e8147e"
)
PROOF_RECEIPT_ID = "S56-M-1060-PROOF-worker-20260715T151806+0800"
EXPRESSION_SHA256 = "a5d3c4e6d9c19f45a79240a26c72c098a43adf164171b3167ee8bee67c1ab7f8"
DENOMINATOR_SHA256 = "32d2df11f1dd7faa40b53ee0ae86fc93d52317f80c4d3e9c1f8bcbe00b2a3f74"
TOOLCHAIN = "leanprover/lean4:v4.29.0"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
LEAN_SHA256 = "3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf"
LAKE_SHA256 = "a608ff084d7e2af228b92a29d7c2fd083ba0580e46889175ec74a81678c98359"
PYTHON_SHA256 = "b8d8288faefdd300201f43fcf00f6f539a27218eeed3a3dff5ab10b9c4c99700"
BASH_SHA256 = "3efccc187bafa75ff1e37d246270ab3e7aa559f242c7a52bf3ec2a1b5450bdbd"
BWRAP_SHA256 = "0abea81db798ebf6b4742ac0664802d97521547a353c2a0dbdc21d76cbbfd2c0"
GIT_SHA256 = "5516c9f362c29376ab9a499a33082f9f611941d8c75930c880e30ad109e39c9a"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MATHLIB_REMOTE = "https://github.com/leanprover-community/mathlib4.git"
MATHLIB_LICENSE_SHA256 = (
    "b40930bbcf80744c86c46a12bc9da056641d722716c378f5659b9e555ef833e1"
)
ALLOWED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
VECTOR = {"H": "H2", "M": "M4", "R": "R4"}
INVENTORY_IDS = [
    "M1060-ROOT", "M1060-S-DEFINITIONS", "M1060-S-BOUNDARY",
    "M1060-S-FOUNDATION", "M1060-N-WIENER", "M1060-N-LDP",
    "M1060-C-PROJECTION", "M1060-L-GAUSSIAN", "M1060-L-PROJECTED",
    "M1060-L-MODULUS", "M1060-L-EXP-EQUIV", "M1060-L-RATE-ID",
    "M1060-T-LOWER", "M1060-T-UPPER", "M1060-C-CM-WITNESS",
    "M1060-L-RATE-LSC", "M1060-L-SUBLEVEL-BOUND", "M1060-T-GOOD",
    "M1060-T-COMPOSE", "M1060-X-SOURCE", "M1060-X-PROVENANCE",
]
MACHINE_IDS = INVENTORY_IDS[:-2]
ROOT_CUT = [
    "M1060-L-GAUSSIAN", "M1060-L-MODULUS", "M1060-L-EXP-EQUIV",
    "M1060-L-RATE-ID", "M1060-L-RATE-LSC", "M1060-L-SUBLEVEL-BOUND",
]
PROOF_DECLARATIONS = (
    "Stage1Instances.THM_M_1060.isProbabilityMeasure_of_isWienerMeasure",
    "Stage1Instances.THM_M_1060.measurableEvaluationLinear",
    "Stage1Instances.THM_M_1060.continuousScale",
    "Stage1Instances.THM_M_1060.zeroTimeVarianceAndLaw",
    "Stage1Instances.THM_M_1060.zeroTimeLaw",
    "Stage1Instances.THM_M_1060.oneTimeVarianceAndLaw",
    "Stage1Instances.THM_M_1060.oneTimeLaw",
    "Stage1Instances.THM_M_1060.isGaussianProcess_of_isWienerMeasure",
)
COMPOSITION_DECLARATIONS = (
    "Stage1Instances.THM_M_1060.ObligationTree.smallNoiseLDP_of_bounds_and_good",
    "Stage1Instances.THM_M_1060.ObligationTree.schilderTarget_of_components",
)
RECONCILED_INPUTS = {
    "README.md": "f9f0d45ed8799fe7652896878693c91c77780901898cdd417f807025bd03dcc1",
    "Statement.lean": "d2bfdc20fcb2cd7c3de27588917dad689056d73e05880814590ab1e3c604581a",
    "ObligationTree.lean": "36b33f8fc27041bda1f08bfdbea6a776848b974d1cf8f6825bb07bc7da3bf985",
    "AnchorAudit.lean": "073381c52bca1c31a618aaaf50e23b57f26003333bea987ace5c098a43b7f7fd",
    "Proof.lean": "9d5626f018862f239c79cdc49b2917abc23565d81fb8c8b8dc7aee6cbedf2069",
    "Validation.lean": "f80cc0d2c02d03d09f987990aa2253ac04e053105149c916736deef05f473036",
    "instance.json": "10525f4db03d4f453d9a0fc2b885f588f8b7707572b5135f987964f6efba8600",
    "task-dag.json": "427cda7b1247e01e60ff673414347a715a0fac908f547f7839a1f874d1d74582",
    "source-statement-crosswalk.md": "00d0a097a4d8546fa8f0303cb69f8f4ea641a768f0df0ea7ad081ff92d948d94",
    "anchor-audit.md": "56681a76eb1749c36dbaea086a8f6419da2d307f98b41ccd5d6ac92a26fc1445",
    "obligation-registry.json": "cb01f4a60e1dc76401a13d41c7fc14a38e391e6d15325827dff178788f2add05",
    "typed-graphs.json": "f707b692bd77c98f1aa435c51165a83f539fdb1bb96a2d765f47746c95814cb9",
    "proof-receipt.json": "28bd48441b97aa7f472f41d53ec0c2f3ab345f1d879c800e8882fa21f491ca38",
    "proof-blocker-2026-07-15-head-48fb6596.json": (
        "a2b6c24a9433e521a8138bcc62e9a82515bc07d4c80202964f4d98763feffbc1"
    ),
    "validation-spec.json": "e38a20dbc301121fd6f1ce3bb2ba0fcac6f6fdae96f0b0d7cff13ba7778739c0",
    "validation-receipt.json": VALIDATION_RECEIPT_SHA256,
    "validation-blocker.json": "9a1b61fc907cc862097c0d57e3ecc5dfcc220722f6693e6d18a4c48dc71108fa",
    "check_obligation_tree.py": "10fe4302b23c37de54207396428ce18115c639b961b6c96ab744bb082596c5f8",
    "check_proof.sh": "356f7b432ae01d6b35b130543ce83d826772fce007ca705d0df8b105ae804531",
    "check_validation.py": "b2f97f56ecd82b03100a93582f643fd5d360b82f228ad155807d236b0bd289d9",
}
AUTHORITY_INPUTS = {
    "Docs/Stage1_Blueprint_rev-5.6.md": (
        "b5f70d04c75d28f256a4b96e252364cc7ea9efa2df778ac262f5210e1bf0cba8"
    ),
    "Docs/Stage1_Targets_rev-5.6.json": (
        "02eec284de534dd78e1cf75f82a477ff477567dd682b7445cb7587abd137ab2c"
    ),
    "Docs/Stage1_Execution_DAG_rev-5.6.json": (
        "53b280d8b02c1fc68c9dd9d10a9763b0a0d1bcb8a95130d14e63955ade2d0dbb"
    ),
    "Docs/Blueprint_Guidelines.md": (
        "a06c07b5ca1b270b4935ad3dab893e9a0e078c29c8da2ef9dca1e71193310535"
    ),
    "skills/execute-stage1-rev56/SKILL.md": (
        "26d47a66c6535feabb8bbf1051fd55d76a53fe761f4b3d953f86b97ec86152b8"
    ),
    "Formalizations/Lean/lean-toolchain": (
        "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2"
    ),
    "Formalizations/Lean/lake-manifest.json": (
        "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81"
    ),
}
RELEASE_OUTPUTS = {
    "release-spec.json": "372a67a4ff91f24dac69121ad9fb9c23759bb06f7ebc221cc275ad5833239478",
    "release-decision.json": "8306d79a09b6e2d9e8adad262c042f1e31aee95856fe05fddb22e15f19263629",
    "release-validation.md": "96d191840821771b22026183fc37f4ca92313ca357df12993c2d1e4da1616d63",
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
    "PASS S56-M-1060-RELEASE negative reconciliation",
    "PASS current-base network-isolated trust-zero replay: exact target, two conditional composers, anchor audit, eight partial bodies, and validation audit",
    "BLOCKED dependency: S56-M-1060-VALIDATION is provisional, nonrelease, and not master-accepted",
    "BLOCKED exact root: zero frozen obligations are closed and all 19 required terminal proof-body IDs are null",
    "BLOCKED assurance: AUDIT-Z/H0/R0/trust/clean-cold-offline/SBOM/independent-verifier/bundle gates remain open",
    "verdict=blocked lifecycle=planned root_vector=H2/M4/R4 audit_complete=false theorem_complete=false",
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


def run(
    argv: list[str], *, cwd: Path = ROOT, env: dict[str, str] | None = None,
    timeout: int = 900,
) -> str:
    result = subprocess.run(
        argv, cwd=cwd, env=env, text=True, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, timeout=timeout, check=False,
    )
    if result.returncode != 0:
        raise AssertionError(f"command failed ({result.returncode}): {argv!r}\n{result.stdout}")
    return result.stdout


BASE_ENV = {
    "HOME": os.environ["HOME"],
    "PATH": f"{os.environ['HOME']}/.elan/bin:/usr/bin:/bin",
    "ELAN_TOOLCHAIN": TOOLCHAIN,
    "LANG": "C.UTF-8",
    "LC_ALL": "C.UTF-8",
    "TZ": "UTC",
    "LEAN_NUM_THREADS": "1",
}


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["/usr/bin/git", *args], cwd=cwd, env=BASE_ENV).strip()


def code_without_comments_and_strings(source: str) -> str:
    output: list[str] = []
    depth = 0
    index = 0
    in_string = False
    while index < len(source):
        if not in_string and source.startswith("/-", index):
            depth += 1
            output.extend("  ")
            index += 2
        elif depth and source.startswith("-/", index):
            depth -= 1
            output.extend("  ")
            index += 2
        elif depth:
            output.append("\n" if source[index] == "\n" else " ")
            index += 1
        elif not in_string and source.startswith("--", index):
            end = source.find("\n", index)
            end = len(source) if end < 0 else end
            output.extend(" " * (end - index))
            index = end
        elif source[index] == '"':
            in_string = not in_string
            output.append(" ")
            index += 1
        elif in_string:
            if source[index] == "\\" and index + 1 < len(source):
                output.extend("  ")
                index += 2
            else:
                output.append("\n" if source[index] == "\n" else " ")
                index += 1
        else:
            output.append(source[index])
            index += 1
    assert depth == 0 and not in_string, "unterminated Lean comment or string"
    return "".join(output)


def reported_axioms(output: str, declaration: str) -> set[str]:
    pattern = re.compile(
        re.escape(f"'{declaration}' depends on axioms: [") + r"(.*?)]", re.DOTALL
    )
    matches = pattern.findall(output)
    assert len(matches) == 1, f"missing or duplicate axiom report for {declaration}"
    return {part.strip() for part in matches[0].split(",") if part.strip()}


def lean_executable() -> Path:
    toolchain = (LEAN_ROOT / "lean-toolchain").read_text(encoding="utf-8").strip()
    directory = toolchain.replace("/", "--").replace(":", "---")
    return Path.home() / ".elan" / "toolchains" / directory / "bin" / "lean"


def lean_path(lean: Path) -> str:
    package_names = (
        "batteries", "Qq", "aesop", "proofwidgets", "importGraph",
        "LeanSearchClient", "plausible", "mathlib",
    )
    roots = [
        (LEAN_ROOT / ".lake" / "packages" / name / ".lake/build/lib/lean").resolve()
        for name in package_names
    ]
    assert all(path.is_dir() for path in roots)
    local = (LEAN_ROOT / ".lake/build/lib/lean").resolve()
    assert local.is_dir()
    return ":".join(
        [*(str(path) for path in roots), str(local), str(lean.parent.parent / "lib/lean")]
    )


def network_isolated_replay(lean: Path) -> dict[str, str]:
    bwrap = Path("/usr/bin/bwrap")
    assert bwrap.is_file()
    pinned_path = lean_path(lean)
    names = (
        "Statement.lean", "Proof.lean", "ObligationTree.lean", "AnchorAudit.lean",
        "Validation.lean",
    )
    with tempfile.TemporaryDirectory(prefix="stage1-m1060-release-", dir="/tmp") as raw:
        tmp = Path(raw).resolve()
        (tmp / "home").mkdir()
        for name in names:
            shutil.copy2(HERE / name, tmp / name)
        base = [
            str(bwrap), "--ro-bind", "/", "/", "--bind", str(tmp), str(tmp),
            "--dev", "/dev", "--proc", "/proc", "--unshare-net", "--die-with-parent",
            "--clearenv", "--setenv", "HOME", str(tmp / "home"), "--setenv", "TMPDIR",
            str(tmp), "--setenv", "LANG", "C.UTF-8", "--setenv", "LC_ALL", "C.UTF-8",
            "--setenv", "TZ", "UTC", "--setenv", "LEAN_NUM_THREADS", "1",
            "--chdir", str(tmp),
        ]

        def lean_run(name: str, module_path: str, emit_olean: bool) -> str:
            argv = base + ["--setenv", "LEAN_PATH", module_path, str(lean), "--trust=0", "-t0"]
            if emit_olean:
                argv += ["-o", name.replace(".lean", ".olean")]
            argv.append(name)
            return run(argv, cwd=tmp, env=BASE_ENV)

        old_umask = os.umask(0o022)
        try:
            outputs = {
                "statement": lean_run("Statement.lean", pinned_path, True),
                "proof": lean_run("Proof.lean", f"{tmp}:{pinned_path}", True),
                "obligation_tree": lean_run("ObligationTree.lean", pinned_path, True),
                "anchor_audit": lean_run("AnchorAudit.lean", pinned_path, False),
                "validation": lean_run("Validation.lean", f"{tmp}:{pinned_path}", False),
            }
        finally:
            os.umask(old_umask)
    return outputs


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
    instance = load(HERE / "instance.json")
    tasks = load(HERE / "task-dag.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    proof = load(HERE / "proof-receipt.json")
    proof_blocker = load(HERE / "proof-blocker-2026-07-15-head-48fb6596.json")
    validation = load(HERE / "validation-receipt.json")
    validation_blocker = load(HERE / "validation-blocker.json")
    targets = load(ROOT / "Docs" / "Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    for relative, expected in AUTHORITY_INPUTS.items():
        assert sha256(ROOT / relative) == expected, f"authority input drifted: {relative}"
    for relative, expected in RECONCILED_INPUTS.items():
        assert sha256(HERE / relative) == expected, f"reconciled input drifted: {relative}"
    for relative, expected in RELEASE_OUTPUTS.items():
        assert sha256(HERE / relative) == expected, f"release output drifted: {relative}"
    assert decision["reconciled_inputs"] == RECONCILED_INPUTS
    assert decision["authority_inputs"] == AUTHORITY_INPUTS
    expected_bound_outputs = {
        f"Stage1_Instances/{THEOREM}/{name}": expected
        for name, expected in RELEASE_OUTPUTS.items()
    }
    expected_bound_outputs[f"Stage1_Instances/{THEOREM}/check_release.py"] = sha256(
        HERE / "check_release.py"
    )
    assert receipt["release_output_bindings"] == expected_bound_outputs

    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target == {
        "execution_rank": 503, "legacy_priority_slot": None, "theorem_id": THEOREM,
        "name": "Schilder定理", "category": "概率论与随机过程 / 随机过程",
        "source_status_untrusted": "已验证", "baseline": "L0",
        "rework_required": True, "legacy_artifacts_accepted": False,
        "target_lane": "hard_mathlib_anchor_and_wrapper", "intake_score": 138,
        "lifecycle_mode": "planned", "theorem_complete": False,
    }
    release_item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert release_item == {
        "id": ITEM, "theorem_id": THEOREM, "execution_rank": 503,
        "phase": "release", "layer": 6, "state": "[ ]",
        "depends_on": ["S56-M-1060-VALIDATION"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Reconcile evidence and decide the exact theorem-completion verdict.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0, "children": [],
    }
    validation_item = next(
        row for row in execution["items"] if row["id"] == "S56-M-1060-VALIDATION"
    )
    assert validation_item["state"] == "[_]" and validation_item["attempts"] == 1
    assert tasks["lifecycle"] == "planned" and tasks["accepted_states"] == []
    assert all(row["state"] == "open" for row in tasks["tasks"])

    assert instance["lifecycle"] == "planned"
    assert instance["root_vector"] == {"H": "H2", "M": "M3", "R": "R4"}
    assert instance["accepted_proof_state"] == []
    assert instance["audit_complete"] is instance["theorem_complete"] is False

    assert registry["root_obligation_id"] == graphs["root_node_id"] == "M1060-ROOT"
    assert [row["obligation_id"] for row in registry["obligations"]] == INVENTORY_IDS
    assert registry["frozen_denominators"]["inventory"] == INVENTORY_IDS
    assert registry["frozen_denominators"]["required_machine"] == MACHINE_IDS
    assert all(row["terminal_proof_body_id"] is None for row in registry["obligations"])
    root_registry = registry["obligations"][0]
    assert root_registry["statement_fingerprint"] == (
        f"lean-expression-sha256:{EXPRESSION_SHA256}"
    )
    denominator = hashlib.sha256(
        json.dumps(
            registry["frozen_denominators"], sort_keys=True, separators=(",", ":")
        ).encode()
    ).hexdigest()
    assert denominator == graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert len(graphs["nodes"]) == 21
    assert sum(len(graph["edges"]) for graph in graphs["graphs"].values()) == 83
    assert graphs["graphs"]["evidence"]["edges"] == []
    assert all(node["evidence_ids"] == [] for node in graphs["nodes"])
    closure = graphs["closure_boundary"]
    assert closure == {
        "closed_obligations": [], "root_closed": False, "root_machine_debt": "M4",
        "audit_complete": False, "theorem_complete": False,
        "remaining_root_cut_set": ROOT_CUT,
    }
    root_node = graphs["nodes"][0]
    assert {
        "H": root_node["human_debt"], "M": root_node["machine_debt"],
        "R": root_node["readability_debt"],
    } == VECTOR
    assert [row["checked_declaration"] for row in graphs["composition_certificates"]] == [
        *COMPOSITION_DECLARATIONS,
    ]

    assert proof["receipt_id"] == PROOF_RECEIPT_ID
    assert proof["support_state"] == "provisional_worker_selftest"
    assert proof["accepted"] is False and proof["verdict"] == "no_state_change"
    assert proof["supported_obligation_ids"] == []
    assert proof["provisionally_closed_obligation_ids"] == []
    assert proof["accepted_closed_obligation_ids"] == []
    assert proof["result"]["proof_phase_complete"] is False
    assert proof["result"]["root_kernel_closed"] is False
    assert proof["remaining_root_cut_set"] == ROOT_CUT
    assert proof_blocker["proof_phase_complete"] is False
    assert proof_blocker["root_closed"] is proof_blocker["theorem_complete"] is False

    assert sha256(HERE / "validation-receipt.json") == VALIDATION_RECEIPT_SHA256
    assert validation["receipt_id"] == VALIDATION_RECEIPT_ID
    assert validation["base_revision"] == VALIDATION_BASE
    assert validation["base_tree"] == VALIDATION_TREE
    assert validation["support_state"] == "provisional_worker_selftest"
    assert validation["proposed_state"] == "[_]"
    assert validation["accepted"] is validation["release_grade"] is False
    assert validation["verdict"] == "blocked"
    assert validation["supported_obligation_ids"] == []
    assert validation["accepted_closed_obligation_ids"] == []
    assert validation["result"]["root_kernel_closed"] is False
    assert validation["result"]["validation_complete"] is False
    assert validation["result"]["audit_complete"] is False
    assert validation["result"]["theorem_complete"] is False
    assert validation["root_vector_before"] == validation["root_vector_after"] == VECTOR
    assert validation["remaining_root_cut_set"] == ROOT_CUT
    assert validation_blocker["closed_obligation_ids"] == []
    assert validation_blocker["required_machine_obligation_count"] == 19
    assert validation_blocker["required_terminal_proof_body_ids_present"] == 0
    assert validation_blocker["root_closed"] is validation_blocker["theorem_complete"] is False
    for name, expected in validation["inputs"].items():
        path = LEAN_ROOT / name if name in {"lean-toolchain", "lake-manifest.json"} else HERE / name
        assert sha256(path) == expected, f"historical validation input drifted: {name}"

    assert decision["schema_version"] == "stage1-release-decision/1.0"
    assert decision["item_id"] == ITEM and decision["theorem_id"] == THEOREM
    assert decision["phase"] == decision["intent"] == "release"
    assert decision["base_revision"] == BASE_REVISION and decision["base_tree"] == BASE_TREE
    assert decision["support_state"] == "provisional_worker_selftest"
    assert decision["proposed_state"] == "[_]" and decision["accepted"] is False
    assert decision["release_grade"] is decision["content_addressed_release_evidence"] is False
    assert decision["verdict"] == "blocked"
    assert decision["lifecycle_before"] == decision["lifecycle_after"] == "planned"
    assert decision["accepted_receipt_ids"] == []
    dependency = decision["dependency"]
    assert dependency["item_id"] == validation["item_id"]
    assert dependency["receipt_id"] == validation["receipt_id"]
    assert dependency["receipt_sha256"] == VALIDATION_RECEIPT_SHA256
    assert dependency["worker_projection"] == "[_]"
    assert dependency["master_accepted"] is dependency["receipt_accepted"] is False
    assert dependency["receipt_release_grade"] is False
    assert dependency["historical_input_hashes_current"] is True
    assert dependency["historical_recipe_currently_replayable"] is False
    assert decision["root_vector"]["before"] == decision["root_vector"]["after"] == VECTOR
    assert decision["terminal_decisions"] == {
        "audit_complete": False, "theorem_complete": False,
        "audit_z": "blocked", "theorem_z": "blocked",
        "release_accepted": False, "master_acceptance": False,
    }
    assert decision["first_failed_gate"]["gate_id"] == "S56-10.2-DEPENDENCY-ACCEPTANCE"
    assert decision["first_failed_gate"]["dependency_gate"] == (
        "dependency.S56-M-1060-VALIDATION.master_acceptance"
    )
    assert decision["first_failed_theorem_gate"]["gate_id"] == (
        "M1060-N-WIENER.complete_increment_covariance_path_law_interface"
    )
    assert decision["first_failed_release_gate"]["gate_id"] == (
        "S56-10.6-IMMUTABLE-CLEAN-INPUT"
    )
    assert decision["next_failed_release_gate"]["gate_id"] == (
        "S56-10.6-HERMETIC-COLD-EMPTY-CACHE-REPLAY"
    )
    assert decision["canonical_obligation_ids"] == INVENTORY_IDS
    assert decision["machine_required_obligation_ids"] == MACHINE_IDS
    assert decision["remaining_root_cut_set"] == ROOT_CUT
    release_gate_text = "\n".join(decision["remaining_release_gate_set"])
    for fragment in (
        "master acceptance", "M1060-N-WIENER", "M1060-L-GAUSSIAN", "AUDIT-Z",
        "accepted H0", "accepted R0", "accepted foundation profile",
        "empty-cache network-denied cold build", "SBOM and license",
        "two signed attestations", "minimal release verifier",
        "deterministic build-twice content-addressed release bundle",
    ):
        assert fragment in release_gate_text, fragment
    assert decision["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert decision["statement_fingerprint"] == f"lean-expression-sha256:{EXPRESSION_SHA256}"
    for key in (
        "audit_inventory_reconciliation", "human_source_acceptance",
        "readability_acceptance", "foundation_and_trust_closure",
        "hermetic_release_reproduction", "supply_chain_closure",
        "independent_release_verification", "protected_ci_and_adversarial_gates",
        "deterministic_release_bundle", "master_acceptance",
    ):
        assert decision["evidence_reconciliation"][key].startswith("missing"), key
    assert decision["evidence_reconciliation"]["root_kernel_closure"].startswith("failed")

    assert spec["schema_version"] == "stage1-release-recipe/1.0"
    assert spec["recipe_id"] == "S56-M-1060-RELEASE-negative-reconciliation-v1"
    assert spec["item_id"] == ITEM and spec["theorem_id"] == THEOREM
    assert spec["argv"] == [
        "/usr/bin/python3", "-I", "-B", f"Stage1_Instances/{THEOREM}/check_release.py"
    ]
    assert spec["network_policy"] == "denied" and spec["expected_exit"] == 0
    assert spec["covered_obligation_ids"] == INVENTORY_IDS
    assert receipt["recipe"] == {
        key: spec[key] for key in (
            "recipe_id", "cwd", "argv", "env_allowlist", "timeout_seconds",
            "network_policy", "network_enforcement", "expected_exit",
            "expected_outputs", "covered_obligation_ids", "covered_declarations",
        )
    }
    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["release_grade"] is receipt["content_addressed_release_evidence"] is False
    assert receipt["verdict"] == "blocked" and receipt["accepted_receipt_ids"] == []
    assert receipt["result"]["required_machine_terminal_body_ids_total"] == 19
    assert receipt["result"]["required_machine_terminal_body_ids_present"] == 0
    assert receipt["result"]["audit_complete"] is receipt["result"]["theorem_complete"] is False
    assert receipt["output_summary"] == SUMMARY_LINES
    assert receipt["remaining_root_cut_set"] == ROOT_CUT

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by|run_tac|oracle)\b|"
        r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
        r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
        r"(?:axiom|constant|opaque|unsafe|extern)\b",
        re.MULTILINE,
    )
    lean_files = (
        "Statement.lean", "ObligationTree.lean", "AnchorAudit.lean", "Proof.lean",
        "Validation.lean",
    )
    for name in lean_files:
        source = code_without_comments_and_strings((HERE / name).read_text(encoding="utf-8"))
        assert prohibited.search(source) is None, f"prohibited source token in {name}"
    proof_source = code_without_comments_and_strings((HERE / "Proof.lean").read_text())
    assert "SchilderTarget" not in proof_source

    manifest = load(LEAN_ROOT / "lake-manifest.json")
    mathlib_entry = next(row for row in manifest["packages"] if row["name"] == "mathlib")
    assert mathlib_entry["rev"] == mathlib_entry["inputRev"] == MATHLIB_REVISION
    assert mathlib_entry["url"] == MATHLIB_REMOTE
    assert (LEAN_ROOT / ".lake").is_symlink()
    assert MATHLIB.resolve().is_dir()
    assert git("rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert git("status", "--porcelain=v1", "--untracked-files=all", cwd=MATHLIB) == ""
    assert git("remote", "get-url", "origin", cwd=MATHLIB) == MATHLIB_REMOTE
    assert sha256(MATHLIB / "LICENSE") == MATHLIB_LICENSE_SHA256

    lean = lean_executable()
    lake = lean.with_name("lake")
    assert lean.is_file() and lake.is_file()
    assert sha256(lean) == LEAN_SHA256 and sha256(lake) == LAKE_SHA256
    assert sha256(Path("/usr/bin/python3").resolve()) == PYTHON_SHA256
    assert sha256(Path("/usr/bin/bash")) == BASH_SHA256
    assert sha256(Path("/usr/bin/bwrap")) == BWRAP_SHA256
    assert sha256(Path("/usr/bin/git")) == GIT_SHA256
    assert LEAN_COMMIT in run([str(lean), "--version"], env=BASE_ENV)
    assert "5.0.0-src+98dc76e" in run([str(lake), "--version"], env=BASE_ENV)

    outputs = network_isolated_replay(lean)
    combined = "\n".join(outputs.values())
    assert "SchilderTarget" in outputs["statement"]
    assert "smallNoiseLDP_of_bounds_and_good" in outputs["obligation_tree"]
    assert "schilderTarget_of_components" in outputs["obligation_tree"]
    assert "noRetainedCandidateClaimsTerminalProof" in outputs["anchor_audit"]
    assert "anchorAuditPermitsTheoremCompletion_eq_false" in outputs["anchor_audit"]
    for declaration in PROOF_DECLARATIONS:
        assert reported_axioms(outputs["proof"], declaration) == ALLOWED_AXIOMS
    for declaration in (*PROOF_DECLARATIONS, *COMPOSITION_DECLARATIONS):
        assert reported_axioms(outputs["validation"], declaration) == ALLOWED_AXIOMS
    assert outputs["validation"].count("Declarations are sorry-free!") == 10
    assert "VALIDATION_CLOSURE roots=10" in outputs["validation"]
    assert "VALIDATION_CLOSURE axioms=[propext, Classical.choice, Quot.sound]" in outputs["validation"]
    assert "VALIDATION_CLOSURE bodyless_nonaxioms=[]" in outputs["validation"]
    assert "VALIDATION_CLOSURE unsafe=[]" in outputs["validation"]
    assert "sorryAx" not in combined and "declaration uses 'sorry'" not in combined
    assert not re.search(r"(^|\n).*error(?:\([^)]*\))?:", combined)

    assert set(packet) == {
        "item_id", "changed_paths", "commands", "output_summary", "base_revision",
        "known_failures", "state",
    }
    assert packet["item_id"] == ITEM and packet["base_revision"] == BASE_REVISION
    assert packet["state"] == "[_]"
    assert set(packet["changed_paths"]) == set(receipt["changed_paths"]) == CHANGED_PATHS
    assert packet["known_failures"] == receipt["known_failures"]
    status = git("status", "--short", "--untracked-files=all")
    actual = {
        line[3:] for line in status.splitlines() if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual == CHANGED_PATHS, (actual, CHANGED_PATHS)
    for relative in CHANGED_PATHS:
        assert_text_hygiene(ROOT / relative)

    for line in SUMMARY_LINES:
        print(line)


if __name__ == "__main__":
    main()
