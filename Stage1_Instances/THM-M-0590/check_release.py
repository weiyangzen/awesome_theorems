#!/usr/bin/env python3
"""Fail-closed release reconciliation for S56-M-0590-RELEASE."""

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
HERE = ROOT / "Stage1_Instances" / "THM-M-0590"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
ITEM = "S56-M-0590-RELEASE"
THEOREM = "THM-M-0590"
BASE_REVISION = "fd50bb07f6632a2ad0bdc17737c200432ee242c8"
BASE_TREE = "ed66432029954bfa5b17e0afda5f3817eeb32d48"
VALIDATION_BASE = "e73a459aa33f8b656019c9c36e3d5dfc84dffc30"
TOOLCHAIN = "leanprover/lean4:v4.29.0"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
LEAN_SHA256 = "3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf"
LAKE_SHA256 = "a608ff084d7e2af228b92a29d7c2fd083ba0580e46889175ec74a81678c98359"
BWRAP_SHA256 = "0abea81db798ebf6b4742ac0664802d97521547a353c2a0dbdc21d76cbbfd2c0"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MATHLIB_ORIGIN = "https://github.com/leanprover-community/mathlib4.git"
MATHLIB_LICENSE_SHA256 = "b40930bbcf80744c86c46a12bc9da056641d722716c378f5659b9e555ef833e1"
STATEMENT_SHA256 = "eae40763685730f42ae296f54c7c41b982efc532836c7db8ce9de31de16b5b67"
DENOMINATOR_SHA256 = "2d5b17d162ed0ef7a445673a25243da41d3aeb4a2be8f39eab68511e1809a9e8"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
ROOT_VECTOR = ["H1", "M4", "R3"]
OPEN_ROOT_CUT = ["M0590-B-FORWARD", "M0590-T-BACKWARD"]
INVENTORY_IDS = [
    "M0590-ROOT",
    "M0590-S-DEFINITIONS",
    "M0590-S-DOMAINS",
    "M0590-S-BOUNDARY",
    "M0590-S-FOUNDATION",
    "M0590-N-CALKIN",
    "M0590-N-FREDHOLM",
    "M0590-L-FWD-SPECTRUM",
    "M0590-L-FWD-INDEX",
    "M0590-B-FORWARD",
    "M0590-C-BUSBY",
    "M0590-L-EXT-CLASS",
    "M0590-L-INDEX-COMPLETE",
    "M0590-T-BACKWARD",
    "M0590-T-ASSEMBLE",
    "M0590-X-SOURCE",
    "M0590-X-PROVENANCE",
]
EXPECTED_INPUTS = {
    "Statement.lean": "eae40763685730f42ae296f54c7c41b982efc532836c7db8ce9de31de16b5b67",
    "ObligationTree.lean": "cf0aa98535f1ec4a4218378d2950c3d25ca0a6047450bdeb5bbe5c390f38fe96",
    "Proof.lean": "3c3a31613315a3493e2e9786caa41cb33db79aec7df314e08a33ac2ec2912d43",
    "Validation.lean": "3b0e3567b9e271d6fd4d903d7005490cc00626d2e88ca40c8b448672e8d2129b",
    "README.md": "75e3cb17ba330cb8458e81ad46d748006316ddf90733a7773a2a63a030d5f11f",
    "source_statement_crosswalk.md": "a69611ac39f5cdc35e2b3b92f253fcb99d0f16aff45f1b6b444006a6743d6f9b",
    "intake.json": "dd49e193fac6fe658ab371322ce91fa8c652298c3075f85948b7ac36c436348a",
    "statement.json": "d20d505e795fbf0c7626d22e508a3cc8ef25f240353ba661f3d9402c1e8b05a0",
    "anchor-audit.json": "6a506ed464abfde062f0d0a8593a1f9eeda50737ab5e6b4feacc6fa31c6470cb",
    "obligation-registry.json": "de449de711d50b330e19da9e251a9a75beb3746a3b45f0ca8cb20298e90d3b0c",
    "typed-graphs.json": "62a92f3bf843dda0dcb90ce7c4016fc4ca91af9611bf69592ae53037ed9371bd",
    "proof-receipt.json": "a3f9fd5d680a560066132385145e71f57720037e6550be9bb1274dacb4e54e84",
    "proof-blocker.json": "7f92f24784ce430766118a182df78a8853e4618c7cee750a5f186e25bc825ac2",
    "proof-validation.md": "15e4203668a150941c081dcd8653e040bd16203a5d73d21f80e77578a620ba0c",
    "validation-spec.json": "c8aa4dd8771f387c29021ca73874cf91898a88339f158b3c1a6c6bc76ff21a16",
    "validation-receipt.json": "36882615a85e70c2115bc9a8e4659ec17b9cd90dacba1eb51269b53bef832464",
    "validation-blocker.json": "9bab6363dfb6c37dedb6061fe2d6c74ff67cb8131602f3ec39636daec44fd730",
    "validation-phase.md": "35710600c178271f7bb89bfb687f995de2bad18224e44ac5b0f4dc017e2df634",
    "check_obligation_tree.py": "c363510152258276fae777bf74ab69a1cbec8cc1648f2046531b0e9b5c2e04b2",
    "check_proof.sh": "05c114a4e38e2d7e447a81cc43715827b8bc0204ea3aa7eb0c4bcf4496c00587",
    "check_validation.py": "88a5694077df125a6d86b83bf81a61a649bd1632e8686ec007c4e175735f3f3e",
}
EXPECTED_AUTHORITY_INPUTS = {
    "Docs/Stage1_Blueprint_rev-5.6.md": "e999167643cde6dbccbde134545710ae92cc16a42b615c8be6160211723ce2a4",
    "Docs/Stage1_Targets_rev-5.6.json": "02eec284de534dd78e1cf75f82a477ff477567dd682b7445cb7587abd137ab2c",
    "Docs/Stage1_Execution_DAG_rev-5.6.json": "faef3cb448c94bc4a3b9ec9bf2ccc14bb637e69af3e33ee2b2e30c6f3ade45e5",
    "Docs/Blueprint_Guidelines.md": "a06c07b5ca1b270b4935ad3dab893e9a0e078c29c8da2ef9dca1e71193310535",
    "skills/execute-stage1-rev56/SKILL.md": "26d47a66c6535feabb8bbf1051fd55d76a53fe761f4b3d953f86b97ec86152b8",
    "Formalizations/Lean/lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "Formalizations/Lean/lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
RELEASE_OUTPUT_NAMES = (
    "release-spec.json",
    "release-decision.json",
    "release-receipt.json",
    "release-validation.md",
)
EXPECTED_RELEASE_OUTPUTS = {
    "release-spec.json": "532bfec4e1301f967cf49d5577be8659d3386a5c06c5b29e30f4b6f54d8fc30a",
    "release-decision.json": "d5de2c6937ea14d77d77033986e99fd905629aa52d2cd10d78b66ce5c1902780",
    "release-validation.md": "88cb181a7252b1421e78a2a37b7acc4e8d2a3ec1bc122fa77c9cb227588cea75",
}
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/check_release.py",
    *(f"Stage1_Instances/{THEOREM}/{name}" for name in RELEASE_OUTPUT_NAMES),
}
SUMMARY_LINES = [
    "PASS release reconciliation: target, DAG, receipts, registry, graphs, and hashes agree",
    "PASS narrow Lean replay: exact statement, conditional composition, five partial bodies, and three probes checked at trust zero",
    "BLOCKED S56-10.2-DEPENDENCY-ACCEPTANCE: validation is provisional and not master accepted",
    "BLOCKED exact root: H1/M4/R3 unchanged; open cut M0590-B-FORWARD, M0590-T-BACKWARD",
    "BLOCKED AUDIT-Z and THEOREM-Z: source/readability, trust, hermetic, and independent gates are open",
    "verdict=blocked audit_complete=false theorem_complete=false accepted_receipts=0",
]
PROOF_DECLARATIONS = [
    "THMM0590.isEssentiallyNormal_of_adjoint_comp_eq_comp_adjoint",
    "THMM0590.unitaryEquivalentModuloCompacts_refl",
    "THMM0590.isCompactOperator_unitary_conjugate",
    "THMM0590.isEssentiallyNormal_unitary_conjugate",
    "THMM0590.bdfInvariantEquivalence_refl",
]
VALIDATION_DECLARATIONS = [
    "THMM0590.Validation.essentiallyNormalOfNormalDirect",
    "THMM0590.Validation.diagonalInvariantEquivalenceDirect",
    "THMM0590.Validation.conditionalRootDirect",
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
    argv: list[str], *, cwd: Path = ROOT, timeout: int = 600,
    env: dict[str, str] | None = None, check: bool = True,
) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        argv, cwd=cwd, env=env, text=True, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, timeout=timeout, check=False,
    )
    if check and result.returncode != 0:
        raise RuntimeError(f"command failed ({result.returncode}): {argv!r}\n{result.stdout}")
    return result


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["git", *args], cwd=cwd, timeout=60).stdout.strip()


def source_without_comments_and_strings(source: str) -> str:
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
    match = re.search(
        rf"'{re.escape(declaration)}' depends on axioms:\s*\[(?P<axioms>.*?)\]",
        output,
        re.DOTALL,
    )
    assert match is not None, f"missing axiom report for {declaration}"
    return {part.strip() for part in match.group("axioms").split(",") if part.strip()}


def assert_text_hygiene(path: Path) -> None:
    data = path.read_bytes()
    assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())


def historical_validation_integrity(receipt: dict) -> None:
    for name, expected in EXPECTED_INPUTS.items():
        if name in receipt["inputs"]:
            assert receipt["inputs"][name] == expected, name
    assert receipt["base_revision"] == VALIDATION_BASE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]"
    assert receipt["accepted"] is receipt["release_grade"] is False
    assert receipt["verdict"] == "blocked"
    assert receipt["accepted_receipt_ids"] == []
    assert receipt["root_vector_before"] == receipt["root_vector_after"] == {
        "H": "H1", "M": "M4", "R": "R3"
    }
    result = receipt["result"]
    assert result["proof_dependency_master_accepted"] is False
    assert result["accepted_closed_obligation_ids"] == []
    assert result["root_kernel_closed"] is False
    assert result["root_machine_debt"] == "M4"
    assert result["audit_complete"] is result["theorem_complete"] is False
    assert receipt["remaining_root_cut_set"] == OPEN_ROOT_CUT


def narrow_lean_replay() -> dict[str, str]:
    fixed_env = {
        "HOME": os.environ["HOME"],
        "PATH": os.environ["PATH"],
        "ELAN_TOOLCHAIN": TOOLCHAIN,
        "LANG": "C.UTF-8",
        "LC_ALL": "C.UTF-8",
        "TZ": "UTC",
        "LEAN_NUM_THREADS": "1",
    }
    lean = Path(run(
        ["lake", "env", "which", "lean"], cwd=LEAN_ROOT, env=fixed_env, timeout=120
    ).stdout.strip())
    lake = lean.parent / "lake"
    bwrap = Path(shutil.which("bwrap") or "")
    assert lean.is_file() and lake.is_file() and bwrap.is_file()
    assert sha256(lean) == LEAN_SHA256
    assert sha256(lake) == LAKE_SHA256
    assert sha256(bwrap) == BWRAP_SHA256
    assert LEAN_COMMIT in run([str(lean), "--version"]).stdout
    lean_path = run(
        [str(lake), "env", "printenv", "LEAN_PATH"], cwd=LEAN_ROOT,
        env=fixed_env, timeout=120,
    ).stdout.strip()

    with tempfile.TemporaryDirectory(prefix="stage1-m0590-release-", dir="/tmp") as name:
        tmp = Path(name).resolve()
        (tmp / "home").mkdir()
        for source in (
            "Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean",
        ):
            shutil.copy2(HERE / source, tmp / source)
        base = [
            str(bwrap), "--ro-bind", "/", "/", "--bind", str(tmp), str(tmp),
            "--dev", "/dev", "--proc", "/proc", "--unshare-net",
            "--die-with-parent", "--clearenv", "--setenv", "HOME", str(tmp / "home"),
            "--setenv", "LANG", "C.UTF-8", "--setenv", "LC_ALL", "C.UTF-8",
            "--setenv", "TZ", "UTC", "--setenv", "LEAN_NUM_THREADS", "1",
            "--chdir", str(tmp),
        ]

        def lean_run(source: str, module_path: str, emit_olean: bool) -> str:
            argv = base + [
                "--setenv", "LEAN_PATH", module_path, str(lean), "--trust=0", "-t0",
            ]
            if emit_olean:
                argv += ["-o", source.replace(".lean", ".olean")]
            argv.append(source)
            return run(argv, env=fixed_env).stdout

        outputs = {
            "statement": lean_run("Statement.lean", lean_path, True),
            "obligation_tree": lean_run(
                "ObligationTree.lean", f"{tmp}:{lean_path}", True
            ),
            "proof": lean_run("Proof.lean", f"{tmp}:{lean_path}", True),
            "validation": lean_run("Validation.lean", f"{tmp}:{lean_path}", False),
        }

    combined = "\n".join(outputs.values())
    for bad in (
        "declaration uses 'sorry'", "declaration has metavariables", "unsolved goals",
        "unknown constant", "error:",
    ):
        assert bad not in combined
    assert "THMM0590.brownDouglasFillmoreTarget" in outputs["statement"]
    assert reported_axioms(
        outputs["obligation_tree"], "THMM0590.root_of_directional_packages"
    ) == EXPECTED_AXIOMS
    for declaration in PROOF_DECLARATIONS:
        assert reported_axioms(outputs["proof"], declaration) == EXPECTED_AXIOMS
    for declaration in VALIDATION_DECLARATIONS:
        assert reported_axioms(outputs["validation"], declaration) == EXPECTED_AXIOMS
    assert outputs["proof"].count("Declarations are sorry-free!") == 5
    assert outputs["validation"].count("Declarations are sorry-free!") == 3
    assert (
        "VALIDATION_CLOSURE roots=3 declarations=18827 modules=752 "
        "bodyless_nonaxioms=0 unsafe=0"
    ) in outputs["validation"]
    return {key: hashlib.sha256(value.encode()).hexdigest() for key, value in outputs.items()}


def main() -> None:
    if sys.flags.optimize != 0:
        raise RuntimeError("release checker requires Python assertions")

    decision = load(HERE / "release-decision.json")
    receipt = load(HERE / "release-receipt.json")
    spec = load(HERE / "release-spec.json")
    validation = load(HERE / "validation-receipt.json")
    proof = load(HERE / "proof-receipt.json")
    statement = load(HERE / "statement.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    targets = load(ROOT / "Docs" / "Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target == {
        "execution_rank": 630,
        "legacy_priority_slot": None,
        "theorem_id": THEOREM,
        "name": "布朗-道格拉斯-菲尔莫尔理论",
        "category": "拓扑学 / 代数拓扑",
        "source_status_untrusted": "已验证",
        "baseline": "L0",
        "rework_required": True,
        "legacy_artifacts_accepted": False,
        "target_lane": "hard_statement_first_partial_verification",
        "intake_score": 132,
        "lifecycle_mode": "planned",
        "theorem_complete": False,
    }
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item == {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 630,
        "phase": "release",
        "layer": 6,
        "state": "[ ]",
        "depends_on": ["S56-M-0590-VALIDATION"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Reconcile evidence and decide the exact theorem-completion verdict.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }
    predecessor = next(
        row for row in execution["items"] if row["id"] == "S56-M-0590-VALIDATION"
    )
    assert predecessor["state"] == "[_]" and predecessor["attempts"] == 1

    for name, expected in EXPECTED_INPUTS.items():
        assert sha256(HERE / name) == expected, f"reconciled input drifted: {name}"
    for relative, expected in EXPECTED_AUTHORITY_INPUTS.items():
        assert sha256(ROOT / relative) == expected, f"authority input drifted: {relative}"

    assert statement["canonical_expression"] == "THMM0590.brownDouglasFillmoreTarget"
    assert statement["environment"]["statement_sha256"] == STATEMENT_SHA256
    assert registry["root_obligation_id"] == graphs["root_node_id"] == "M0590-ROOT"
    assert registry["frozen_denominators"]["inventory"] == INVENTORY_IDS
    assert graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    closure = graphs["closure_boundary"]
    assert closure["closed_obligations"] == [
        "M0590-S-DEFINITIONS", "M0590-S-DOMAINS", "M0590-T-ASSEMBLE",
    ]
    assert closure["root_closed"] is closure["audit_complete"] is False
    assert closure["theorem_complete"] is False
    assert closure["remaining_root_cut_set"] == OPEN_ROOT_CUT
    root = next(node for node in graphs["nodes"] if node["obligation_id"] == "M0590-ROOT")
    assert [root["human_debt"], root["machine_debt"], root["readability_debt"]] == ROOT_VECTOR
    assert graphs["graphs"]["evidence"]["edges"] == []
    for obligation_id in ["M0590-ROOT", *OPEN_ROOT_CUT]:
        row = next(
            entry for entry in registry["obligations"]
            if entry["obligation_id"] == obligation_id
        )
        assert row["terminal_proof_body_id"] is None

    assert proof["accepted"] is False
    assert proof["supported_obligation_ids"] == []
    assert proof["provisionally_closed_obligation_ids"] == []
    assert proof["accepted_closed_obligation_ids"] == []
    assert proof["result"]["root_kernel_closed"] is False
    assert proof["result"]["theorem_complete"] is False
    historical_validation_integrity(validation)

    lake_link = LEAN_ROOT / ".lake"
    assert lake_link.is_symlink()
    mathlib = lake_link / "packages" / "mathlib"
    assert mathlib.is_dir()
    assert git("rev-parse", "HEAD", cwd=mathlib) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == MATHLIB_TREE
    assert git("status", "--porcelain=v1", "--untracked-files=all", cwd=mathlib) == ""
    assert git("remote", "get-url", "origin", cwd=mathlib) == MATHLIB_ORIGIN
    assert sha256(mathlib / "LICENSE") == MATHLIB_LICENSE_SHA256

    dependency = decision["dependency"]
    assert dependency["item_id"] == validation["item_id"] == "S56-M-0590-VALIDATION"
    assert dependency["receipt_id"] == validation["receipt_id"]
    assert dependency["receipt_sha256"] == sha256(HERE / "validation-receipt.json")
    assert dependency["support_state"] == validation["support_state"]
    assert dependency["accepted"] is dependency["release_grade"] is False
    assert dependency["master_accepted"] is False
    assert dependency["historical_recipe_currently_replayable"] is False
    assert VALIDATION_BASE != BASE_REVISION
    assert f'BASE_REVISION = "{VALIDATION_BASE}"' in (
        HERE / "check_validation.py"
    ).read_text(encoding="utf-8")

    result = decision["decision"]
    assert decision["item_id"] == ITEM and decision["theorem_id"] == THEOREM
    assert decision["base_revision"] == BASE_REVISION and decision["base_tree"] == BASE_TREE
    assert decision["proposed_state"] == "[_]" and decision["release_grade"] is False
    assert decision["accepted_receipt_ids"] == []
    assert result["verdict"] == "blocked"
    assert result["lifecycle_before"] == result["lifecycle_after"] == "planned"
    assert result["root_vector_before"] == result["root_vector_after"] == ROOT_VECTOR
    assert result["debt_vector_delta"] == "none"
    assert result["audit_complete"] is result["theorem_complete"] is False
    assert result["audit_z"] == result["theorem_z"] == "blocked"
    assert result["release_accepted"] is False
    assert result["first_failed_gate"]["gate_id"] == "S56-10.2-DEPENDENCY-ACCEPTANCE"
    assert result["first_failed_audit_gate"]["gate_id"] == (
        "S56-AUDIT-FROZEN-INVENTORY-SOURCE-BOUNDARY-RECONCILIATION"
    )
    assert result["first_failed_theorem_gate"]["gate_id"] == (
        "S56-THEOREM-EXACT-ROOT-KERNEL-CLOSURE"
    )
    assert result["first_failed_release_specific_gate"]["gate_id"] == (
        "S56-RELEASE-IMMUTABLE-CLEAN-INPUT"
    )
    assert result["next_failed_release_gate"]["gate_id"] == "S56-10.6-HERMETIC-COLD-BUILD"
    assert result["remaining_root_cut_set"] == OPEN_ROOT_CUT
    disagreement = decision["authority_disagreement"]
    assert disagreement["intake_projection"] == ["H1", "M3", "R3"]
    assert disagreement["typed_graph_and_validation_projection"] == ROOT_VECTOR
    assert disagreement["conservative_release_vector"] == ROOT_VECTOR
    assert disagreement["reconciled"] is False
    reconciliation = decision["evidence_reconciliation"]
    assert reconciliation["observed_graph_closed_obligations_unaccepted"] == [
        "M0590-S-DEFINITIONS", "M0590-S-DOMAINS", "M0590-T-ASSEMBLE",
    ]
    assert reconciliation["accepted_closed_obligations"] == []
    for key in (
        "accepted_exact_root_kernel_closure",
        "audit_z_accepted",
        "pinpoint_h0_review",
        "independent_r0_review",
        "complete_provenance_foundation_tcb_closure",
        "immutable_clean_release_input",
        "hermetic_cold_offline_replay",
        "sbom_license_archive_closure",
        "independent_clean_runner_attestations",
        "independently_implemented_minimal_verifier",
        "protected_ci_and_adversarial_gates",
        "deterministic_release_bundle",
        "master_acceptance",
    ):
        assert reconciliation[key] is False, key

    assert spec["schema_version"] == "stage1-validation-recipe/1.0"
    assert spec["item_id"] == ITEM and spec["theorem_id"] == THEOREM
    assert spec["argv"] == [
        "python3", "-I", "-B", f"Stage1_Instances/{THEOREM}/check_release.py",
    ]
    assert spec["cwd"] == "." and spec["timeout_seconds"] == 600
    assert spec["network_policy"] == "denied" and spec["expected_exit"] == 0
    assert spec["covered_obligation_ids"] == INVENTORY_IDS
    assert spec["covered_decisions"] == ["AUDIT-Z", "THEOREM-Z"]

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["phase"] == receipt["intent"] == "release"
    assert receipt["depends_on"] == ["S56-M-0590-VALIDATION"]
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]"
    assert receipt["accepted"] is receipt["release_grade"] is False
    assert receipt["content_addressed_release_evidence"] is receipt["master_accepted"] is False
    assert receipt["decision_id"] == decision["decision_id"]
    assert receipt["accepted_receipt_ids"] == []
    assert receipt["canonical_obligation_ids"] == INVENTORY_IDS
    receipt_result = receipt["result"]
    assert receipt_result["verdict"] == "blocked"
    assert receipt_result["accepted_closed_obligations"] == []
    assert receipt_result["accepted_root_closed"] is False
    assert receipt_result["audit_complete"] is receipt_result["theorem_complete"] is False
    assert receipt_result["root_vector_before"] == receipt_result["root_vector_after"] == ROOT_VECTOR
    assert receipt_result["remaining_root_cut_set"] == OPEN_ROOT_CUT
    assert receipt_result["first_failed_gate"] == "S56-10.2-DEPENDENCY-ACCEPTANCE"
    assert receipt_result["first_failed_audit_gate"] == (
        "S56-AUDIT-FROZEN-INVENTORY-SOURCE-BOUNDARY-RECONCILIATION"
    )
    assert receipt_result["first_failed_theorem_gate"] == (
        "S56-THEOREM-EXACT-ROOT-KERNEL-CLOSURE"
    )
    assert receipt_result["first_failed_release_specific_gate"] == (
        "S56-RELEASE-IMMUTABLE-CLEAN-INPUT"
    )
    expected_bindings = {
        **{
            f"Stage1_Instances/{THEOREM}/{name}": digest
            for name, digest in EXPECTED_INPUTS.items()
        },
        **EXPECTED_AUTHORITY_INPUTS,
    }
    assert receipt["input_bindings"] == expected_bindings
    for relative, expected in expected_bindings.items():
        assert sha256(ROOT / relative) == expected, f"receipt input drifted: {relative}"
    expected_release_bindings = {
        f"Stage1_Instances/{THEOREM}/{name}": digest
        for name, digest in EXPECTED_RELEASE_OUTPUTS.items()
    }
    expected_release_bindings[f"Stage1_Instances/{THEOREM}/check_release.py"] = sha256(
        Path(__file__).resolve()
    )
    assert receipt["release_output_bindings"] == expected_release_bindings
    for relative, expected in expected_release_bindings.items():
        assert sha256(ROOT / relative) == expected, f"release output drifted: {relative}"
    for key in (
        "recipe_id", "cwd", "argv", "env_allowlist", "timeout_seconds",
        "network_policy", "network_enforcement", "expected_exit", "expected_outputs",
        "covered_obligation_ids", "covered_decisions", "covered_declarations",
        "scope_boundary",
    ):
        assert receipt["recipe"][key] == spec[key], key
    expected_stdout = ("\n".join(SUMMARY_LINES) + "\n").encode()
    assert receipt["output_evidence"]["stdout_semantic_sha256"] == hashlib.sha256(
        expected_stdout
    ).hexdigest()
    assert receipt["output_evidence"]["expected_line_count"] == len(SUMMARY_LINES)

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by|run_tac|oracle)\b|"
        r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
        r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
        r"(?:axiom|constant|opaque|unsafe|extern)\b",
        re.MULTILINE,
    )
    all_source = "\n".join(
        source_without_comments_and_strings((HERE / name).read_text(encoding="utf-8"))
        for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean")
    )
    assert prohibited.search(all_source) is None
    lean_hashes = narrow_lean_replay()
    assert receipt_result["current_release_lean_output_sha256"] == lean_hashes

    packet = load(ROOT / ".stage1-worker-selftest.json")
    assert set(packet) == {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state", "evidence_artifacts",
    }
    assert packet["item_id"] == ITEM and packet["base_revision"] == BASE_REVISION
    assert packet["state"] == "[_]"
    assert set(packet["changed_paths"]) == set(receipt["changed_paths"]) == CHANGED_PATHS
    assert packet["commands"] == receipt["commands_and_results"]
    assert packet["output_summary"] == receipt["output_summary"] == SUMMARY_LINES
    assert packet["known_failures"] == decision["known_failures"] == receipt["known_failures"]
    assert packet["evidence_artifacts"] == {
        "decision": f"Stage1_Instances/{THEOREM}/release-decision.json",
        "receipt": f"Stage1_Instances/{THEOREM}/release-receipt.json",
        "recipe": f"Stage1_Instances/{THEOREM}/release-spec.json",
        "readable_reconciliation": f"Stage1_Instances/{THEOREM}/release-validation.md",
    }
    status = git("status", "--short", "--untracked-files=all")
    actual_changes = {
        line[3:] for line in status.splitlines()
        if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual_changes == CHANGED_PATHS, (actual_changes, CHANGED_PATHS)
    for relative in CHANGED_PATHS:
        assert_text_hygiene(ROOT / relative)
    for name in RELEASE_OUTPUT_NAMES:
        text = (HERE / name).read_text(encoding="utf-8")
        assert "/home/" not in text and ".cron/" not in text
        assert "theorem_complete=true" not in text

    print("\n".join(SUMMARY_LINES))


if __name__ == "__main__":
    main()
