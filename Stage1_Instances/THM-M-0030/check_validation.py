#!/usr/bin/env python3
"""Fail-closed narrow validation for S56-M-0030-VALIDATION."""

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
import tempfile


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0030"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM = "S56-M-0030-VALIDATION"
THEOREM = "THM-M-0030"
BASE_REVISION = "bb6fb28ac1c55ecb52f3f1c84e7fbb35c26b47ad"
BASE_TREE = "ca999baf360c6ce2440bbc2c01aeb8d519269a90"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MATHLIB_REMOTE = "https://github.com/leanprover-community/mathlib4.git"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
EXPRESSION_SHA256 = "53389852e2c0875086c2c28cb4a60448670ee29145e13d86b4b1ad3e9df8861e"
DENOMINATOR_SHA256 = "2c8a394f62ce23e20c104f25129c82e7966b24cc2ac991a50f9d7a68ce1c6a45"
EXPECTED_INPUTS = {
    "Statement.lean": "737a2cf8a656d39617aecf8aa7d8b2bb3d5739807ea34f6e75dbb833f3c6978e",
    "AnchorAudit.lean": "5fb18fef99524a311526378fc7c12bc29c5c6f2661c0d011d6717e3c4ff5d2cf",
    "anchor-audit.json": "d87b987723e114f6792d20b255489bbe4a1840d876b4e50e9eadd260c3bfbc1c",
    "ObligationTree.lean": "cd18b0839882f77e63483dda9a593c3aef89920b6c6d6261f4fe5a632752dff0",
    "Proof.lean": "dc915c2fb61a414f485d06322479c4e4706a817aceaf4f68a4fb0097af71f9fd",
    "proof-receipt.json": "52138bf5236416854b3550bbdb4263e47e6d34d68c78b7acef253e5a9f2d5310",
    "obligation-registry.json": "eb8f21f00749297d3ee2a3d6320fa8e120fdc6bda146de3a2c628c50f453668c",
    "typed-graphs.json": "bf95a4b6b69aa9583c01aa274c86520713406cead2b56debe15c615aa94f8126",
    "validation-specs.json": "d56e7efae6109c831caae11c1e071b009b4e418965df919198fdb834aad307a3",
    "Validation.lean": "7a6c69dec5d4d4fcbd0670893fc719f5c7ea8d3e31138cedc324069ec2d5caaf",
    "validation-spec.json": "1b135d7df0506e0f7f8234448ad76f6fe2f017d7459d6d31582b7f44d8495207",
}
EXPECTED_TOOL_INPUTS = {
    "lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
TERMINAL_SOURCE_SHA256 = "b161e2c4ce77f1224648467573dd4ba4c0ebc1ed734118e70df4cb39b33b1a72"
TERMINAL_SOURCE_BLOB = "c4fc3737f1859f1e22d387b199b46fe32d5f5093"
TERMINAL_ROUTE_SHA256 = "96c9f9e4da837d7b086b151455f1bcf04f528dced20da5da5625dfc00bd15e62"
TERMINAL_BODY_SHA256 = "bed35e82de1fe7cbabba8e7db71f6c1d606c5b76547a3740c93089490775bf49"
TERMINAL_OLEAN_SHA256 = "cf6e08eb1139645443b085dfe89d87771ba2440ef957ae380b87d1bcd50d908e"
LICENSE_SHA256 = "b40930bbcf80744c86c46a12bc9da056641d722716c378f5659b9e555ef833e1"
CLOSED_IDS = {
    "M0030-ROOT",
    "M0030-X-MATHLIB-BODY",
    "M0030-N-FINITE-MODULE",
    "M0030-N-JACOBSON",
    "M0030-N-LOCAL-CONTAINMENT",
    "M0030-L-PROPER-MAXIMAL",
    "M0030-L-MAXIMAL-JACOBSON",
    "M0030-L-JACOBSON-UNIT",
    "M0030-X-JACOBSON-UNIT-SOURCE",
    "M0030-N-FIXEDPOINT-IFF",
    "M0030-T-FIXEDPOINT-COMPOSE",
    "M0030-B-FIXEDPOINT-FORWARD",
    "M0030-B-FIXEDPOINT-BACKWARD",
}
SOURCE_MAPPED_IDS = {
    "M0030-C-INFIMUM-SUBMODULE",
    "M0030-C-STABLE-INTERSECTION",
    "M0030-L-STABILIZATION-INDEX",
    "M0030-T-STABILITY-EVALUATE",
    "M0030-L-FG-NAKAYAMA",
    "M0030-L-POWER-INDUCTION",
}
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/Validation.lean",
    f"Stage1_Instances/{THEOREM}/check_validation.py",
    f"Stage1_Instances/{THEOREM}/validation-phase.md",
    f"Stage1_Instances/{THEOREM}/validation-receipt.json",
    f"Stage1_Instances/{THEOREM}/validation-spec.json",
}


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict), path
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(argv: list[str], *, cwd: Path = ROOT) -> str:
    result = subprocess.run(
        argv,
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=300,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(f"validation failed ({result.returncode}): {argv!r}\n{result.stdout}")
    return result.stdout


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["git", *args], cwd=cwd).strip()


def code_without_comments(source: str) -> str:
    source = re.sub(r"/-.*?-/", "", source, flags=re.DOTALL)
    return re.sub(r"--.*$", "", source, flags=re.MULTILINE)


def assert_axioms(output: str, declaration: str) -> None:
    match = re.search(
        rf"'{re.escape(declaration)}' depends on axioms:\s*\[([^]]+)\]",
        output,
        re.DOTALL,
    )
    assert match is not None, (declaration, output)
    observed = {part.strip() for part in match.group(1).split(",")}
    assert observed == EXPECTED_AXIOMS, (declaration, observed)


def main() -> None:
    spec = load(HERE / "validation-spec.json")
    receipt = load(HERE / "validation-receipt.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")
    statement = load(HERE / "statement.json")
    anchor = load(HERE / "anchor-audit.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    proof_receipt = load(HERE / "proof-receipt.json")
    instance = load(HERE / "instance.json")
    local_dag = load(HERE / "task-dag.json")
    execution = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item == {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 1075,
        "phase": "validation",
        "layer": 5,
        "state": "[ ]",
        "depends_on": ["S56-M-0030-PROOF"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Run hermetic kernel, trust, provenance, and independent validation gates.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }
    predecessor = next(
        row for row in execution["items"] if row["id"] == "S56-M-0030-PROOF"
    )
    assert predecessor["state"] == "[_]" and predecessor["attempts"] == 1
    local_task = next(row for row in local_dag["tasks"] if row["id"] == ITEM)
    assert local_task["state"] == "open"
    assert local_task["depends_on"] == ["S56-M-0030-PROOF"]

    assert spec["schema_version"] == "stage1-validation-recipe/1.0"
    assert spec["item_id"] == ITEM and spec["theorem_id"] == THEOREM
    assert spec["cwd"] == "."
    assert spec["argv"] == [
        "python3", "-B", f"Stage1_Instances/{THEOREM}/check_validation.py"
    ]
    assert spec["env_allowlist"] == {}
    assert spec["timeout_seconds"] == 300
    assert spec["network_policy"] == "denied" and spec["expected_exit"] == 0
    assert "bubblewrap --unshare-net" in spec["network_enforcement"]
    assert set(spec["covered_obligation_ids"]) == CLOSED_IDS

    for name, expected in EXPECTED_INPUTS.items():
        assert sha256(HERE / name) == expected, f"stale validation input: {name}"
    for name, expected in EXPECTED_TOOL_INPUTS.items():
        assert sha256(LEAN_ROOT / name) == expected, f"changed tool input: {name}"

    formal = statement["canonical_formal_target"]
    assert formal["declaration_or_expression"] == (
        "Stage1Instances.THM_M_0030.KrullIntersectionTarget"
    )
    assert formal["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert formal["statement_file_sha256"] == EXPECTED_INPUTS["Statement.lean"]
    assert anchor["canonical_target_expression_sha256"] == EXPRESSION_SHA256
    assert anchor["canonical_statement_file_sha256"] == EXPECTED_INPUTS["Statement.lean"]
    assert registry["frozen_against_statement_sha256"] == EXPECTED_INPUTS["Statement.lean"]
    assert registry["frozen_against_anchor_audit_sha256"] == EXPECTED_INPUTS["anchor-audit.json"]
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert proof_receipt["proof_body"]["source_sha256"] == EXPECTED_INPUTS["Proof.lean"]
    assert proof_receipt["inputs"]["obligation_tree_sha256"] == EXPECTED_INPUTS["ObligationTree.lean"]
    assert proof_receipt["inputs"]["obligation_registry_sha256"] == EXPECTED_INPUTS["obligation-registry.json"]
    assert proof_receipt["result"]["root_kernel_closed"] is True
    assert set(proof_receipt["closed_obligation_ids"]) == CLOSED_IDS
    assert set(proof_receipt["source_mapped_not_individually_closed_ids"]) == SOURCE_MAPPED_IDS
    assert proof_receipt["accepted_closed_obligation_ids"] == []
    assert proof_receipt["result"]["axioms"] == [
        "propext", "Classical.choice", "Quot.sound"
    ]
    assert instance["lifecycle_mode"] == "planned"
    assert instance["root_vector"] == {"H": "H1", "M": "M3", "R": "R3"}
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == []
    assert instance["audit_complete"] is instance["theorem_complete"] is False
    assert instance["foundation_profile"].startswith("lean4-foundation-planned/")
    assert instance["tcb_profile"].startswith("lean4-mathlib-tcb-planned/")

    closure = graphs["closure_boundary"]
    assert closure["accepted_closed_obligations"] == []
    assert closure["root_closed"] is False and closure["root_machine_debt"] == "M3"
    assert closure["audit_complete"] is closure["theorem_complete"] is False
    assert set(closure["remaining_root_cut_set"]) == {
        "M0030-X-MATHLIB-BODY", "M0030-X-SOURCE", "M0030-S-FOUNDATION",
        "M0030-X-PROVENANCE", "M0030-X-TRUST", "M0030-X-READABLE",
        "M0030-X-WORKFLOW",
    }

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by|extern)\b|"
        r"^[ \t]*(?:axiom|constant|opaque|unsafe)\b",
        re.MULTILINE,
    )
    for name in (
        "Statement.lean", "AnchorAudit.lean", "ObligationTree.lean", "Proof.lean",
        "Validation.lean",
    ):
        source = code_without_comments((HERE / name).read_text(encoding="utf-8"))
        assert prohibited.search(source) is None, f"prohibited source token in {name}"
    differential = (HERE / "Validation.lean").read_text(encoding="utf-8")
    for forbidden in (
        "import Proof", "import ObligationTree", "Proof.krullIntersection",
        "Ideal.iInf_pow_eq_bot_of_isLocalRing I hI",
    ):
        assert forbidden not in differential, forbidden
    assert "Ideal.iInf_pow_smul_eq_bot_of_isLocalRing (M := R) I hI" in differential
    assert "rw [smul_eq_mul, <- Ideal.one_eq_top, mul_one]" in differential

    manifest = load(LEAN_ROOT / "lake-manifest.json")
    mathlib_entry = next(row for row in manifest["packages"] if row["name"] == "mathlib")
    assert mathlib_entry["rev"] == mathlib_entry["inputRev"] == MATHLIB_REVISION
    assert MATHLIB.resolve().is_dir(), "pinned mathlib artifact is unavailable"
    assert git("rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert git("remote", "get-url", "origin", cwd=MATHLIB) == MATHLIB_REMOTE
    assert git("status", "--porcelain=v1", cwd=MATHLIB) == ""
    terminal_source = MATHLIB / "Mathlib/RingTheory/Filtration.lean"
    terminal_olean = MATHLIB / ".lake/build/lib/lean/Mathlib/RingTheory/Filtration.olean"
    assert sha256(terminal_source) == TERMINAL_SOURCE_SHA256
    assert git("rev-parse", "HEAD:Mathlib/RingTheory/Filtration.lean", cwd=MATHLIB) == TERMINAL_SOURCE_BLOB
    lines = terminal_source.read_bytes().splitlines(keepends=True)
    assert hashlib.sha256(b"".join(lines[391:435])).hexdigest() == TERMINAL_ROUTE_SHA256
    assert hashlib.sha256(b"".join(lines[429:435])).hexdigest() == TERMINAL_BODY_SHA256
    assert sha256(terminal_olean) == TERMINAL_OLEAN_SHA256
    assert sha256(MATHLIB / "LICENSE") == LICENSE_SHA256
    assert prohibited.search(code_without_comments(b"".join(lines[391:435]).decode())) is None

    bwrap = shutil.which("bwrap")
    assert bwrap is not None, "bubblewrap is required for network-denied Lean replay"
    lean = Path(run(["lake", "env", "which", "lean"], cwd=LEAN_ROOT).strip())
    lake = Path(run(["lake", "env", "which", "lake"], cwd=LEAN_ROOT).strip())
    lean_version = run(["lake", "env", "lean", "--version"], cwd=LEAN_ROOT)
    assert "4.29.0" in lean_version and LEAN_COMMIT in lean_version
    lean_path = run(["lake", "env", "printenv", "LEAN_PATH"], cwd=LEAN_ROOT).strip()
    with tempfile.TemporaryDirectory(prefix="m0030-validation-", dir=LEAN_ROOT) as tmp_name:
        tmp = Path(tmp_name).resolve()
        for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
            (tmp / name).write_bytes((HERE / name).read_bytes())
        base = [
            bwrap, "--ro-bind", "/", "/", "--bind", str(tmp), str(tmp),
            "--dev", "/dev", "--proc", "/proc", "--unshare-net", "--die-with-parent",
            "--setenv", "LANG", "C.UTF-8", "--setenv", "LC_ALL", "C.UTF-8",
            "--setenv", "TZ", "UTC", "--chdir", str(tmp),
        ]
        statement_output = run(base + [
            "--setenv", "LEAN_PATH", lean_path, str(lean), "--trust=0",
            "-o", "Statement.olean", "Statement.lean",
        ])
        module_env = ["--setenv", "LEAN_PATH", f"{tmp}:{lean_path}"]
        obligation_output = run(base + module_env + [
            str(lean), "--trust=0", "-o", "ObligationTree.olean", "ObligationTree.lean",
        ])
        proof_output = run(base + module_env + [str(lean), "--trust=0", "Proof.lean"])
        validation_output = run(base + module_env + [str(lean), "--trust=0", "Validation.lean"])

    assert "KrullIntersectionTarget" in statement_output
    proof_declarations = (
        "Ideal.iInf_pow_eq_bot_of_isLocalRing",
        "Ideal.iInf_pow_smul_eq_bot_of_isLocalRing",
        "Ideal.iInf_pow_smul_eq_bot_of_le_jacobson",
        "Ideal.mem_iInf_smul_pow_eq_bot_iff",
        "Stage1Instances.THM_M_0030.Proof.exactMathlibAnchor",
        "Stage1Instances.THM_M_0030.Proof.finiteModuleIntersection",
        "Stage1Instances.THM_M_0030.Proof.jacobsonIntersection",
        "Stage1Instances.THM_M_0030.Proof.properToMaximal",
        "Stage1Instances.THM_M_0030.Proof.maximalToJacobson",
        "Stage1Instances.THM_M_0030.Proof.jacobsonUnitSource",
        "Stage1Instances.THM_M_0030.Proof.fixedPointCharacterization",
        "Stage1Instances.THM_M_0030.Proof.fixedPointForward",
        "Stage1Instances.THM_M_0030.Proof.fixedPointBackward",
        "Stage1Instances.THM_M_0030.Proof.localProperIdealJacobson",
        "Stage1Instances.THM_M_0030.Proof.jacobsonUnit",
        "Stage1Instances.THM_M_0030.Proof.fixedPointCharacterization_via_branches",
        "Stage1Instances.THM_M_0030.Proof.jacobsonIntersection_via_frozen_composition",
        "Stage1Instances.THM_M_0030.Proof.finiteModuleIntersection_via_frozen_composition",
        "Stage1Instances.THM_M_0030.Proof.exactMathlibAnchor_via_frozen_composition",
        "Stage1Instances.THM_M_0030.Proof.krullIntersection_direct",
        "Stage1Instances.THM_M_0030.Proof.krullIntersection_via_pinned_anchor",
        "Stage1Instances.THM_M_0030.Proof.krullIntersection_via_frozen_composition",
    )
    for declaration in proof_declarations:
        assert_axioms(proof_output, declaration)
    for declaration in (
        "Ideal.mem_iInf_smul_pow_eq_bot_iff",
        "Ideal.iInf_pow_smul_eq_bot_of_le_jacobson",
        "Ideal.iInf_pow_smul_eq_bot_of_isLocalRing",
        "Ideal.iInf_pow_eq_bot_of_isLocalRing",
        "Stage1Instances.THM_M_0030.Validation.differentialKrullIntersection",
    ):
        assert_axioms(validation_output, declaration)
    assert proof_output.count("Declarations are sorry-free!") == 9
    assert validation_output.count("Declarations are sorry-free!") == 5
    assert "sorryAx" not in obligation_output + proof_output + validation_output
    closure_match = re.search(
        r"VALIDATION_CLOSURE declarations=(\d+) modules=(\d+)", validation_output
    )
    assert closure_match is not None
    assert "VALIDATION_CLOSURE axioms=[propext, Classical.choice, Quot.sound]" in validation_output
    assert "VALIDATION_CLOSURE bodyless_nonaxioms=[]" in validation_output
    assert "VALIDATION_CLOSURE unsafe=[]" in validation_output

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == packet["item_id"] == ITEM
    assert receipt["theorem_id"] == THEOREM
    assert receipt["base_revision"] == packet["base_revision"] == BASE_REVISION
    assert receipt["base_tree"] == BASE_TREE
    assert receipt["started_at"] == "2026-07-14T00:38:45+08:00"
    assert receipt["finished_at"] == receipt["validated_at"] == (
        "2026-07-14T00:39:59+08:00"
    )
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == packet["state"] == "[_]"
    assert receipt["release_grade"] is receipt["accepted"] is False
    for name, expected in EXPECTED_INPUTS.items():
        assert receipt["inputs"][name] == expected
    assert receipt["inputs"]["check_validation.py"] == sha256(HERE / "check_validation.py")
    assert receipt["target"] == {
        "canonical_declaration": "Stage1Instances.THM_M_0030.KrullIntersectionTarget",
        "elaborated_expression_sha256": EXPRESSION_SHA256,
        "registry_denominator_sha256": DENOMINATOR_SHA256,
    }
    environment = receipt["environment"]
    assert environment["lean_executable_sha256"] == sha256(lean)
    assert environment["lake_executable_sha256"] == sha256(lake)
    assert environment["python_executable_sha256"] == sha256(Path(sys.executable).resolve())
    assert environment["git_executable_sha256"] == sha256(Path(shutil.which("git") or "").resolve())
    assert environment["bash_executable_sha256"] == sha256(Path(shutil.which("bash") or "").resolve())
    assert environment["bubblewrap_executable_sha256"] == sha256(Path(bwrap).resolve())
    assert environment["platform"] == f"{platform.system()} {platform.machine()}"
    assert environment["mathlib_revision"] == MATHLIB_REVISION
    assert environment["mathlib_tree"] == MATHLIB_TREE
    provenance = receipt["provenance"]
    assert provenance["terminal_source_sha256"] == TERMINAL_SOURCE_SHA256
    assert provenance["terminal_source_blob"] == TERMINAL_SOURCE_BLOB
    assert provenance["terminal_route_sha256"] == TERMINAL_ROUTE_SHA256
    assert provenance["terminal_body_sha256"] == TERMINAL_BODY_SHA256
    assert provenance["terminal_olean_sha256"] == TERMINAL_OLEAN_SHA256
    assert provenance["license_sha256"] == LICENSE_SHA256
    replayed = provenance["machine_replayed_transitive_closure"]
    assert replayed["declarations"] == int(closure_match.group(1))
    assert replayed["modules"] == int(closure_match.group(2))
    assert replayed["axioms"] == ["propext", "Classical.choice", "Quot.sound"]
    assert replayed["bodyless_nonaxioms"] == replayed["unsafe_declarations"] == []
    for key in (
        "recipe_id", "cwd", "argv", "env_allowlist", "timeout_seconds",
        "network_policy", "network_enforcement", "expected_exit", "expected_outputs",
        "covered_obligation_ids", "covered_declarations",
    ):
        assert receipt["recipe"][key] == spec[key]
    result = receipt["result"]
    assert result["exact_root_kernel_closed"] is True
    assert result["observed_axioms"] == ["propext", "Classical.choice", "Quot.sound"]
    assert result["accepted_root_machine_debt"] == "M3"
    assert result["accepted_closed_obligations"] == []
    assert result["network_isolated_trust_zero_lean_replay"] == "pass"
    assert result["hermetic_release_gate"] == "fail_closed"
    assert result["accepted_foundation_tcb_gate"] == "fail_closed"
    assert result["complete_provenance_gate"] == "fail_closed"
    assert result["independent_distinct_runner_gate"] == "fail_closed"
    assert result["audit_complete"] is result["theorem_complete"] is False
    assert receipt["first_failed_gate"] == "dependency.S56-M-0030-PROOF.master_acceptance"
    assert receipt["first_failed_release_gate"] == "S56-10.6-HERMETIC-COLD-BUILD"

    required_packet_fields = {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert set(packet) == required_packet_fields
    assert set(receipt["changed_paths"]) == set(packet["changed_paths"]) == CHANGED_PATHS
    assert receipt["commands"] == packet["commands"]
    assert receipt["output_summary"] == packet["output_summary"]
    assert receipt["known_failures"] == packet["known_failures"]
    status = git(
        "status", "--porcelain=v1", "--untracked-files=all", "--",
        str(HERE), str(ROOT / ".stage1-worker-selftest.json"),
    )
    actual_changed = {
        line[3:] if line[:2] == "??" else line[2:].lstrip()
        for line in status.splitlines()
    }
    assert actual_changed == CHANGED_PATHS, (actual_changed, CHANGED_PATHS)
    for relative in CHANGED_PATHS:
        data = (ROOT / relative).read_bytes()
        assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())
    for path in (HERE / "validation-receipt.json", HERE / "validation-phase.md"):
        text = path.read_text(encoding="utf-8")
        assert "/home/" not in text and ".cron/" not in text
        assert "theorem_complete=true" not in text

    print("PASS THM-M-0030 narrow validation")
    print("PASS network-isolated trust-zero kernel replay: exact target, frozen composition, proof roots, and differential root elaborated")
    print("PASS trust observation: 22 proof declarations and five validation declarations report exactly propext, Classical.choice, and Quot.sound")
    print(f"PASS transitive environment observation: {closure_match.group(1)} declarations, {closure_match.group(2)} modules, no unexpected bodyless or unsafe declaration")
    print("PASS local provenance: frozen hashes, terminal route/body/olean, clean mathlib pin, remote, and license agree")
    print("OPEN authority: PROOF is provisional; accepted root remains H1/M3/R3 with zero accepted obligations")
    print("BLOCKED release gates: warm shared cache, planned foundation/TCB, incomplete provenance/SBOM, and no distinct signed independent verifier")
    print("audit_complete=false; theorem_complete=false")


if __name__ == "__main__":
    main()
