#!/usr/bin/env python3
"""Fail-closed release reconciliation for S56-M-0612-RELEASE."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import re
import shutil
import subprocess
import tempfile


if not __debug__:
    raise SystemExit("release validation requires Python assertions")


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0612"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
ITEM = "S56-M-0612-RELEASE"
THEOREM = "THM-M-0612"
BASE_REVISION = "b4d239943a37f6c25c377bbfd85c0e1ec7f4acaa"
BASE_TREE = "5f13e0e86bde3bcaaef38b979819490c648166e3"
STATEMENT_SHA256 = "2de623b53340de741e2b691d81a0e1a9f0a6f74bbdeb133f7ebcc5a20d97f919"
DENOMINATOR_SHA256 = "2cad29b7c0b54afdec80a5d7ac1940a49cccfacdab64c1b75c27e140dd7a4bc8"
PROOF_RECEIPT_SHA256 = "01210378e747d9da81b4d64b6e782c2cff645d274effbf6a164b8ffd164cad5e"
VALIDATION_RECEIPT_SHA256 = "8b4a2ac7d628753c15f85ba81936d36f31559ed7ea85b24a494583b33f698a9a"
VALIDATION_BLOCKER_SHA256 = "e31827ddfb943e08b9f80a92378196c3054a14745f632b849ae967981a95c1ed"
LEAN_TOOLCHAIN = "leanprover/lean4:v4.29.0"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
LEAN_EXECUTABLE_SHA256 = "3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf"
BWRAP_EXECUTABLE_SHA256 = "0abea81db798ebf6b4742ac0664802d97521547a353c2a0dbdc21d76cbbfd2c0"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
ROOT_VECTOR = {"H": "H2", "M": "M3", "R": "R4"}
OPEN_CUT = ["M0612-T-SQUARED"]
ALLOWED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}

UPSTREAM_INPUTS = {
    "README.md": "f787c1b93d014e73cff35c6b415deebee6b1ba69d0c536188f88a990009f71ad",
    "instance.json": "b8fff47fae4911e633009ea85fbb6bc55168d5a44d99563d4eaa4a265122884d",
    "task-dag.json": "f4465bf6c1501e14c57a9be6d4406e1045bfd3b6581852c74333731e2f157050",
    "source-statement-crosswalk.md": "31ddaed1745a62ed07ee7b0ef43a2d3226f23efa38fc42c39784f7c3324ca145",
    "statement-receipt.json": "48405823f937988e425b288ab40ffe0debdf6cfccf6abbd3670f37f240ec6afe",
    "obligation-registry.json": "635af26d6d87637952beb03486a2e29b9f0cde834da54fc2539e800caf538850",
    "typed-graphs.json": "def7053233342a03342983a55bf7a8ec627a13dca40fc86914e07ffa4f0250b2",
    "proof-receipt-2026-07-15-slot26.json": PROOF_RECEIPT_SHA256,
    "proof-blocker.json": "a3c3d2b418ebb38d2a7308d559af41d92496786ca893648f4e87cce1b11111de",
    "validation-receipt.json": VALIDATION_RECEIPT_SHA256,
    "validation-blocker.json": VALIDATION_BLOCKER_SHA256,
    "validation-spec.json": "c4ff473f9c6fe61c063da80ee580a7d4f8a4036d2b2418268cc0cb05f06371b9",
    "check_validation.py": "d8a5593561bffc1f8093e7e9421e9a920a2a978344f5ab9c766b6a9ff44a45ae",
    "Statement.lean": STATEMENT_SHA256,
    "LocalEncoding.lean": "278177c5db75abff44ff5576ce8a6912c7f210f96f0b9f27097f895c6d62a117",
    "EncodingSanityProbe.lean": "1b61df008216231fd46b94bdc2ba26ad141636e9d802a9c84af430b403f0ed82",
    "DimensionTwo.lean": "282b485bfe5bed0dcc7cb68b30775252272e29d1ef1ebb7a9bdd1284d01100fd",
    "ObligationTree.lean": "0392a18a80b7cea4fcbba89e23941228ff861cd6406345bf134ef4b857773007",
    "AnchorAudit.lean": "5b7ae6560bcae68afaedef4576dcd2a0c858ef4223b87461343188390ec12fc1",
    "Validation.lean": "19bd5ccfb3c8dbe101179c48f41565fdb49c05a3e5c116818fbb57dafe16bb90",
}
AUTHORITY_INPUTS = {
    "Docs/Stage1_Targets_rev-5.6.json": "02eec284de534dd78e1cf75f82a477ff477567dd682b7445cb7587abd137ab2c",
    "Docs/Stage1_Blueprint_rev-5.6.md": "30420963279e5084a6c640f0f54ec93e5869796259183a5e18ff94fd5def48f5",
    "Docs/Stage1_Execution_DAG_rev-5.6.json": "ef2b42902181efeaee8be3987e7915d278dc860e79d54bf4247238be67ca3731",
    "skills/execute-stage1-rev56/SKILL.md": "26d47a66c6535feabb8bbf1051fd55d76a53fe761f4b3d953f86b97ec86152b8",
}
RELEASE_INPUTS = {
    "release-decision.json": "90231f47d5c0ad5503ecc8fadaac53af4de1c9c51e997b615ca681686cea04a1",
    "release-phase.md": "ed3b98782b24ef889550b902c55184d2fc8f7ad7f5335326ee40eee2f8b031d0",
    "release-spec.json": "0929afb04f12ae6545531263d897202a8c70645f8fece68504f0e5a0ec064737",
}
CHANGED_PATHS = [
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/check_release.py",
    f"Stage1_Instances/{THEOREM}/release-decision.json",
    f"Stage1_Instances/{THEOREM}/release-phase.md",
    f"Stage1_Instances/{THEOREM}/release-receipt.json",
    f"Stage1_Instances/{THEOREM}/release-spec.json",
]
SUMMARY_LINES = [
    "PASS THM-M-0612 negative release reconciliation: current authority, receipts, hashes, and lifecycle agree",
    "PASS current network-isolated trust-zero replay: unchanged proposed Lean target, local encoding, Fin 1 bodies, conditional composition, anchors, and validation audit elaborated",
    "PASS hygiene and trust observation: seven audited declarations are sorry-free and use only propext, Classical.choice, and Quot.sound",
    "OPEN exact root: no checked declaration inhabits the universal higher-dimensional RadiusSquaredObstruction or StatementShape",
    "BLOCKED AUDIT-Z: primary-source acceptance, H0/R0 review, authority reconciliation, and accepted evidence remain absent",
    "BLOCKED THEOREM-Z: root is M3 and M0612-T-SQUARED remains the open cut set",
    "BLOCKED release assurance: shared warm cache is not a cold offline build, and no distinct signed runner or minimal verifier exists",
    "VERDICT blocked; lifecycle planned; root vector H2/M3/R4; accepted_receipt_ids=[]; theorem_complete=false",
]
SUMMARY_BYTES = ("\n".join(SUMMARY_LINES) + "\n").encode()

AXIOM_DECLARATIONS = {
    "DimensionTwo.lean": (
        "Stage1.THM_M_0612.symplectic_det_dimTwo",
        "Stage1.THM_M_0612.image_volume_eq_dimTwo",
        "Stage1.THM_M_0612.volume_ball_dimTwo",
        "Stage1.THM_M_0612.dimTwo_radiusSquaredObstruction",
    ),
    "Validation.lean": (
        "Stage1.THM_M_0612.radius_le_of_sq_le",
        "Stage1.THM_M_0612.root_of_radiusSquaredObstruction",
        "Stage1.THM_M_0612.Validation.rootFromRadiusSquaredObstruction",
    ),
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


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


def run(
    argv: list[str], *, cwd: Path = ROOT, env: dict[str, str] | None = None,
    timeout: int = 600, check: bool = True,
) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        argv, cwd=cwd, env=env, text=True, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, timeout=timeout, check=False,
    )
    if check and result.returncode != 0:
        raise RuntimeError(f"command failed ({result.returncode}): {argv!r}\n{result.stdout}")
    return result


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["/usr/bin/git", *args], cwd=cwd).stdout.strip()


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
    assert depth == 0 and not in_string
    return "".join(output)


def reported_axioms(output: str, declaration: str) -> set[str]:
    pattern = re.compile(
        re.escape(f"'{declaration}' depends on axioms: [") + r"(.*?)]", re.DOTALL
    )
    matches = pattern.findall(output)
    assert matches, declaration
    return {part.strip() for part in matches[-1].split(",") if part.strip()}


def assert_text_hygiene(path: Path) -> None:
    data = path.read_bytes()
    assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines()), path


def compiled_roots() -> list[Path]:
    roots = sorted(
        (path / ".lake/build/lib/lean").resolve()
        for path in (LEAN_ROOT / ".lake/packages").iterdir()
        if path.is_dir() and (path / ".lake/build/lib/lean").is_dir()
    )
    local = (LEAN_ROOT / ".lake/build/lib/lean").resolve()
    if local.is_dir():
        roots.append(local)
    roots.append(Path.home() / ".elan/toolchains/leanprover--lean4---v4.29.0/lib/lean")
    assert roots
    return roots


def sandboxed_replay(lean: Path, bwrap: Path) -> dict[str, str]:
    tmp = Path(tempfile.mkdtemp(prefix="stage1-m0612-release-", dir="/tmp")).resolve()
    try:
        names = (
            "Statement.lean", "LocalEncoding.lean", "DimensionTwo.lean",
            "ObligationTree.lean", "AnchorAudit.lean", "Validation.lean",
        )
        for name in names:
            shutil.copy2(HERE / name, tmp / name)
        (tmp / "home").mkdir()
        dependency_path = ":".join(str(path) for path in compiled_roots() if path.is_dir())
        base = [
            str(bwrap), "--ro-bind", "/", "/", "--bind", str(tmp), str(tmp),
            "--dev", "/dev", "--proc", "/proc", "--unshare-net", "--die-with-parent",
            "--clearenv", "--setenv", "HOME", str(tmp / "home"), "--setenv", "TMPDIR",
            str(tmp), "--setenv", "LANG", "C.UTF-8", "--setenv", "LC_ALL", "C.UTF-8",
            "--setenv", "TZ", "UTC", "--setenv", "LEAN_NUM_THREADS", "1", "--chdir",
            str(tmp),
        ]

        def lean_run(name: str, local_imports: bool, emit_olean: bool) -> str:
            lean_path = f"{tmp}:{dependency_path}" if local_imports else dependency_path
            argv = base + ["--setenv", "LEAN_PATH", lean_path, str(lean), "--trust=0", "-t0"]
            if emit_olean:
                argv += ["-o", Path(name).with_suffix(".olean").name]
            argv.append(name)
            return run(argv).stdout

        return {
            "Statement.lean": lean_run("Statement.lean", False, True),
            "LocalEncoding.lean": lean_run("LocalEncoding.lean", True, True),
            "DimensionTwo.lean": lean_run("DimensionTwo.lean", True, True),
            "ObligationTree.lean": lean_run("ObligationTree.lean", True, True),
            "AnchorAudit.lean": lean_run("AnchorAudit.lean", False, False),
            "Validation.lean": lean_run("Validation.lean", True, False),
        }
    finally:
        shutil.rmtree(tmp)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker-packet", type=Path)
    args = parser.parse_args()
    os.umask(0o022)

    decision = load(HERE / "release-decision.json")
    spec = load(HERE / "release-spec.json")
    receipt = load(HERE / "release-receipt.json")
    instance = load(HERE / "instance.json")
    tasks = load(HERE / "task-dag.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    proof = load(HERE / "proof-receipt-2026-07-15-slot26.json")
    validation = load(HERE / "validation-receipt.json")
    blocker = load(HERE / "validation-blocker.json")
    targets = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 256
    assert target["baseline"] == "L0" and target["rework_required"] is True
    assert target["legacy_artifacts_accepted"] is False
    assert target["lifecycle_mode"] == "planned" and target["theorem_complete"] is False
    nodes = {row["id"]: row for row in execution["items"] if row["theorem_id"] == THEOREM}
    assert len(nodes) == 7
    assert nodes[ITEM]["state"] == "[ ]"
    assert nodes[ITEM]["depends_on"] == ["S56-M-0612-VALIDATION"]
    assert nodes[ITEM]["owned_paths"] == [f"Stage1_Instances/{THEOREM}"]
    assert nodes["S56-M-0612-VALIDATION"]["state"] == "[_]"
    assert nodes["S56-M-0612-VALIDATION"]["attempts"] == 1
    assert all(nodes[node_id]["state"] == "[_]" for node_id in nodes if node_id != ITEM)

    assert instance["lifecycle"] == "planned"
    assert instance["root_vector"] == ROOT_VECTOR
    assert instance["accepted_proof_state"] == []
    assert instance["audit_complete"] is instance["theorem_complete"] is False
    assert instance["remaining_root_cut_set"] == OPEN_CUT
    assert tasks["lifecycle"] == "planned" and tasks["accepted_states"] == []
    assert all(row["state"] == "open" for row in tasks["tasks"])
    assert registry["root_obligation_id"] == graphs["root_node_id"] == "M0612-ROOT"
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert registry["frozen_against_statement_sha256"] == STATEMENT_SHA256
    assert len(registry["obligations"]) == 26
    root = next(node for node in graphs["nodes"] if node["obligation_id"] == "M0612-ROOT")
    assert {"H": root["human_debt"], "M": root["machine_debt"], "R": root["readability_debt"]} == ROOT_VECTOR
    closure = graphs["closure_boundary"]
    assert closure["root_closed"] is closure["audit_complete"] is closure["theorem_complete"] is False
    assert closure["root_machine_debt"] == "M3" and closure["remaining_root_cut_set"] == OPEN_CUT
    assert graphs["graphs"]["evidence"]["edges"] == []

    for name, expected in UPSTREAM_INPUTS.items():
        assert sha256(HERE / name) == expected, name
        assert receipt["inputs"][name] == expected, name
    for name, expected in AUTHORITY_INPUTS.items():
        assert sha256(ROOT / name) == expected, name
        assert receipt["authority_inputs"][name] == expected, name
    for name, expected in RELEASE_INPUTS.items():
        assert sha256(HERE / name) == expected, name
        assert receipt["inputs"][name] == expected, name
    assert sha256(HERE / "proof-receipt-2026-07-15-slot26.json") == PROOF_RECEIPT_SHA256
    assert sha256(HERE / "validation-receipt.json") == VALIDATION_RECEIPT_SHA256
    assert sha256(HERE / "validation-blocker.json") == VALIDATION_BLOCKER_SHA256
    assert proof["accepted"] is validation["accepted"] is False
    assert proof["accepted_closed_obligation_ids"] == validation["accepted_receipt_ids"] == []
    assert proof["result"]["root_kernel_closed"] is False
    assert proof["result"]["proof_phase_complete"] is False
    assert validation["verdict"] == "blocked" and validation["release_grade"] is False
    assert validation["result"]["validation_phase_complete"] is False
    assert validation["result"]["root_kernel_closed"] is False
    assert validation["result"]["audit_complete"] is validation["result"]["theorem_complete"] is False
    assert validation["remaining_root_cut_set"] == blocker["remaining_root_cut_set"] == OPEN_CUT

    assert decision["item_id"] == ITEM and decision["theorem_id"] == THEOREM
    assert decision["base_revision"] == BASE_REVISION and decision["base_tree"] == BASE_TREE
    assert decision["verdict"] == "blocked" and decision["release_grade"] is False
    assert decision["lifecycle_before"] == decision["lifecycle_after"] == "planned"
    assert decision["root_vector_before"] == decision["root_vector_after"] == ROOT_VECTOR
    assert decision["audit_complete"] is decision["theorem_complete"] is False
    assert decision["terminal_decisions"] == {"audit_z": "blocked", "theorem_z": "blocked"}
    assert decision["accepted_receipt_ids"] == []
    assert decision["dependency"]["receipt_sha256"] == VALIDATION_RECEIPT_SHA256
    assert decision["dependency"]["accepted"] is decision["dependency"]["master_accepted"] is False
    assert decision["first_failed_gate"]["gate_id"] == "S56-10.2-DEPENDENCY-ACCEPTANCE"
    assert decision["first_failed_mathematical_gate"]["gate_id"] == "M0612-B-HIGHER-KERNEL-CLOSURE"
    assert decision["remaining_root_cut_set"] == OPEN_CUT
    assert len(decision["authority_conflicts"]) == 4
    for key in (
        "dependency_master_accepted", "authoritative_state_reconciled",
        "accepted_root_m0", "exact_root_kernel_closed", "audit_z_accepted",
        "pinpoint_h0_source_review", "independent_r0_review",
        "complete_provenance_foundation_tcb_closure", "immutable_clean_release_input",
        "hermetic_cold_empty_cache_offline_replay", "complete_sbom_license_archive_closure",
        "two_independent_signed_runner_attestations",
        "independently_implemented_minimal_release_verifier",
        "protected_ci_and_adversarial_gates",
        "deterministic_content_addressed_release_bundle", "master_acceptance",
    ):
        assert decision["evidence_reconciliation"][key] is False, key

    assert spec["schema_version"] == "stage1-validation-spec/1.0"
    assert spec["item_id"] == ITEM and spec["theorem_id"] == THEOREM
    assert spec["argv"] == [
        "/usr/bin/python3", "-I", "-B", f"Stage1_Instances/{THEOREM}/check_release.py",
        "--worker-packet", ".stage1-worker-selftest.json",
    ]
    assert spec["cwd"] == "." and spec["network_policy"] == "denied"
    assert spec["timeout_seconds"] == 600 and spec["expected_exit"] == 0
    assert spec["covered_decisions"] == ["AUDIT-Z", "THEOREM-Z"]

    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["phase"] == receipt["intent"] == "release"
    assert receipt["depends_on"] == ["S56-M-0612-VALIDATION"]
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["release_grade"] is receipt["content_addressed_release_evidence"] is False
    assert receipt["result"]["verdict"] == "blocked"
    assert receipt["result"]["root_vector"] == ROOT_VECTOR
    assert receipt["result"]["accepted_receipt_ids"] == []
    assert receipt["result"]["audit_complete"] is receipt["result"]["theorem_complete"] is False
    assert receipt["first_failed_gate"] == "S56-10.2-DEPENDENCY-ACCEPTANCE"
    assert receipt["remaining_root_cut_set"] == OPEN_CUT
    assert receipt["recipe"] == {
        key: spec[key] for key in (
            "recipe_id", "cwd", "argv", "env_allowlist", "timeout_seconds",
            "network_policy", "network_enforcement", "expected_exit", "expected_outputs",
            "covered_obligation_ids", "partially_covered_obligation_ids",
            "covered_declarations", "covered_decisions", "scope_boundary",
        )
    }

    validation_source = (HERE / "check_validation.py").read_text(encoding="utf-8")
    assert f'BASE_REVISION = "{validation["base_revision"]}"' in validation_source
    assert validation["base_revision"] != BASE_REVISION
    stale_probe = run(
        ["/usr/bin/python3", "-I", "-B", str(HERE / "check_validation.py"), "--probe"],
        check=False, timeout=60,
    )
    assert stale_probe.returncode != 0
    assert "git(\"rev-parse\", \"HEAD\") == BASE_REVISION" in stale_probe.stdout

    all_source = "\n".join(
        source_without_comments_and_strings((HERE / name).read_text(encoding="utf-8"))
        for name in (
            "Statement.lean", "LocalEncoding.lean", "EncodingSanityProbe.lean",
            "DimensionTwo.lean", "ObligationTree.lean", "AnchorAudit.lean", "Validation.lean",
        )
    )
    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by|run_tac|oracle)\b|"
        r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
        r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
        r"(?:axiom|constant|opaque|unsafe|extern)\b",
        re.MULTILINE,
    )
    assert prohibited.search(all_source) is None
    statement_body = source_without_comments_and_strings(
        (HERE / "Statement.lean").read_text(encoding="utf-8")
    )
    obligation_body = source_without_comments_and_strings(
        (HERE / "ObligationTree.lean").read_text(encoding="utf-8")
    )
    validation_body = source_without_comments_and_strings(
        (HERE / "Validation.lean").read_text(encoding="utf-8")
    )
    assert re.search(r"^def StatementShape\s*:\s*Prop\s*:=", statement_body, re.MULTILINE)
    assert re.search(
        r"theorem root_of_radiusSquaredObstruction\s+"
        r"\(geometry\s*:\s*RadiusSquaredObstruction[^)]*\)\s*:\s*StatementShape",
        obligation_body, re.DOTALL,
    )
    assert re.search(
        r"theorem rootFromRadiusSquaredObstruction\s+"
        r"\(geometry\s*:\s*RadiusSquaredObstruction[^)]*\)\s*:\s*StatementShape",
        validation_body, re.DOTALL,
    )
    root_return_count = len(re.findall(r"\)\s*:\s*StatementShape(?:\.\{u\})?\s*:=", all_source))
    assert root_return_count == 2

    assert (LEAN_ROOT / ".lake").is_symlink()
    mathlib = (LEAN_ROOT / ".lake/packages/mathlib").resolve()
    assert git("rev-parse", "HEAD", cwd=mathlib) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == MATHLIB_TREE
    assert git("status", "--porcelain=v1", "--untracked-files=all", cwd=mathlib) == ""
    lean = Path.home() / ".elan/toolchains/leanprover--lean4---v4.29.0/bin/lean"
    bwrap = Path("/usr/bin/bwrap")
    assert sha256(lean) == LEAN_EXECUTABLE_SHA256
    assert sha256(bwrap) == BWRAP_EXECUTABLE_SHA256
    fixed_env = {
        "ELAN_TOOLCHAIN": LEAN_TOOLCHAIN, "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8",
        "TZ": "UTC", "LEAN_NUM_THREADS": "1",
    }
    assert LEAN_COMMIT in run([str(lean), "--version"], env=fixed_env).stdout
    outputs = sandboxed_replay(lean, bwrap)
    combined = "\n".join(outputs.values())
    assert "sorryAx" not in combined and "declaration uses 'sorry'" not in combined
    assert "error:" not in combined
    observed = []
    for module, declarations in AXIOM_DECLARATIONS.items():
        for declaration in declarations:
            assert reported_axioms(outputs[module], declaration) == ALLOWED_AXIOMS
            observed.append(declaration)
    assert len(observed) == 7
    assert outputs["DimensionTwo.lean"].count("Declarations are sorry-free!") == 4
    assert outputs["Validation.lean"].count("Declarations are sorry-free!") == 1
    assert "VALIDATION_CLOSURE roots=7" in outputs["Validation.lean"]
    assert "VALIDATION_CLOSURE unexpected_axioms=[]" in outputs["Validation.lean"]
    assert "VALIDATION_CLOSURE unsafe=[]" in outputs["Validation.lean"]

    assert receipt["execution"]["stdout_sha256"] == hashlib.sha256(SUMMARY_BYTES).hexdigest()
    assert receipt["execution"]["stdout_bytes"] == len(SUMMARY_BYTES)
    assert receipt["execution"]["stdout_line_count"] == len(SUMMARY_LINES)
    assert receipt["execution"]["observed_axiom_declaration_count"] == len(observed)
    assert receipt["execution"]["observed_axioms"] == [
        "propext", "Classical.choice", "Quot.sound"
    ]
    assert receipt["environment"]["platform"] == (
        f"{platform.system()} {platform.release()} {platform.machine()}"
    )

    if args.worker_packet is not None:
        packet = load(args.worker_packet.resolve())
        assert set(packet) == {
            "item_id", "changed_paths", "commands", "output_summary",
            "base_revision", "known_failures", "state",
        }
        assert packet["item_id"] == ITEM and packet["state"] == "[_]"
        assert packet["base_revision"] == BASE_REVISION
        assert packet["changed_paths"] == CHANGED_PATHS
        assert packet["commands"] == receipt["commands"]
        assert packet["output_summary"] == receipt["output_summary"]
        assert packet["known_failures"] == receipt["known_failures"]
        actual_changes = {
            line[3:] for line in git("status", "--short", "--untracked-files=all").splitlines()
            if line[3:] != "Formalizations/Lean/.lake"
        }
        assert actual_changes == set(CHANGED_PATHS), (actual_changes, CHANGED_PATHS)

    for relative in CHANGED_PATHS:
        assert_text_hygiene(ROOT / relative)
    print("\n".join(SUMMARY_LINES))


if __name__ == "__main__":
    main()
