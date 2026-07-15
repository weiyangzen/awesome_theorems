#!/usr/bin/env python3
"""Fail-closed release reconciliation for S56-M-0600-RELEASE."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile


if not __debug__:
    raise SystemExit("release validation requires Python assertions")


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0600"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM = "S56-M-0600-RELEASE"
THEOREM = "THM-M-0600"
BASE_REVISION = "443b8bbc23bf35a1e7a4bb7b3183073f76bbee2b"
BASE_TREE = "c5771c47c12b80aba613e6d844570f83b39ded6d"
EXPRESSION_SHA256 = "6ba927d7712fa05ea04ff656eefe32d16a57a2c45f4aa49a30695b263b04911d"
DENOMINATOR_SHA256 = "071b084403b89cd9fb084d9fe7167cad1738e115f6353aaeabfab4516e93f981"
PROOF_RECEIPT_SHA256 = "286c8b9f6256331e0743922be4c5c55e32040e6dcb1420d578f3341990175de1"
VALIDATION_RECEIPT_SHA256 = "9b0a3400358330a83e23d47d5e85796ca95bb22e889b0c904abaf30b371655a6"
LEAN_TOOLCHAIN = "leanprover/lean4:v4.29.0"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
LEAN_EXECUTABLE_SHA256 = "3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf"
BWRAP_EXECUTABLE_SHA256 = "0abea81db798ebf6b4742ac0664802d97521547a353c2a0dbdc21d76cbbfd2c0"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
ALLOWED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}

UPSTREAM_INPUTS = {
    "README.md": "7b7766b64bab1b0d5b43bdad2320691159451c27bcc4183061cc4bb549839214",
    "instance.json": "dc647bcc3af5bf6889f49064f5ab23f730b43db06c1d6e4109820f6863fe070d",
    "task-dag.json": "a97ff34ab5b065d4f5b8908a5524ea902a17e517efe3e66c70608b56f127d458",
    "source-statement-crosswalk.md": "f781ede12f33e77e28f0f48a8f3065db8fe52a8464405f3a2c8f0d9f48711567",
    "statement.json": "fb5b2919203752f6ee859e934df2233002362454a0b9a56d8626e31b89a43cd9",
    "obligation-registry.json": "3746b457df4c0f011582f59aac375739f6d28b02f6dc55c68155d8e8cd4deff0",
    "typed-graphs.json": "38970e70e2007054cc2bb7a27ef6e421c1645f96a8d1653b10d3a0d9cdf28160",
    "proof-receipt.json": PROOF_RECEIPT_SHA256,
    "proof-blocker.json": "f6e44c023a8c4223f5071d9393afcf12e3724e1bb205e2b4b3588b6f2592485b",
    "validation-receipt.json": VALIDATION_RECEIPT_SHA256,
    "validation-spec.json": "ece868df0301ed8a1ca093f5a8a396e83bdf4885bfd0514310345867c938e560",
    "check_validation.py": "bfd13c88a6546a5f1b9d448996a0f2099bdad93800d33af147da8a5d9149ea2b",
    "Statement.lean": "40dced107b293e5045af83deaabd2f898bdf16c4b6f4bced61b6a9fbef2b97dc",
    "ObligationTree.lean": "6e01acd6107af26a9b969495c97edd2d1e3f73ad3e1c78e78765fe81bdb6bb97",
    "Proof.lean": "cfc2225e6c236608ddda93b7038e8a6f584a4164a11e5a093ed375e51e04cf55",
    "AnchorAudit.lean": "bbdd2e32bad8571517658f6ef718d58c06388b15555b991870f95fd39b2a88af",
    "Validation.lean": "957beb3a3a5679e1bcca15c263772d9ea82c3e27b44e5496fd0b2cbeae641341",
}
AUTHORITY_INPUTS = {
    "Docs/Stage1_Targets_rev-5.6.json": "02eec284de534dd78e1cf75f82a477ff477567dd682b7445cb7587abd137ab2c",
    "Docs/Stage1_Blueprint_rev-5.6.md": "c09f9f713bdbc820559e41e1e1840423d60cc2af666aeaf5f3c88587de77f161",
    "Docs/Stage1_Execution_DAG_rev-5.6.json": "0bb2f433832fe71156aa46c0828102ec3fb61a00dec81fae129c2826a59f63ca",
    "skills/execute-stage1-rev56/SKILL.md": "26d47a66c6535feabb8bbf1051fd55d76a53fe761f4b3d953f86b97ec86152b8",
}
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/check_release.py",
    f"Stage1_Instances/{THEOREM}/release-decision.json",
    f"Stage1_Instances/{THEOREM}/release-phase.md",
    f"Stage1_Instances/{THEOREM}/release-receipt.json",
    f"Stage1_Instances/{THEOREM}/release-spec.json",
}
AXIOM_DECLARATIONS = {
    "ObligationTree.lean": (
        "Stage1Instances.THM_M_0600.root_of_morseNormalFormEngine",
    ),
    "Proof.lean": (
        "Stage1Instances.THM_M_0600.zeroDimensionBranch",
        "Stage1Instances.THM_M_0600.morseNormalFormEngine_of_positiveDimension",
        "Stage1Instances.THM_M_0600.morseLemmaTarget_of_positiveDimension",
    ),
    "Validation.lean": (
        "Stage1Instances.THM_M_0600.Validation.zeroDimensionBranchDirect",
        "Stage1Instances.THM_M_0600.Validation.conditionalRootDirect",
    ),
}
SUMMARY_LINES = (
    "PASS THM-M-0600 negative release reconciliation",
    "PASS authority binding: exact target and frozen 18-obligation graph remain current",
    "PASS trust-zero replay: statement, conditional adapters, zero-dimensional body, anchor probes, and differential probes elaborated",
    "PASS hygiene and axioms: six checked declarations are sorry-free and use exactly propext, Classical.choice, and Quot.sound",
    "OPEN exact root: M0600-T-ENGINE has no premise-free proof body",
    "BLOCKED AUDIT-Z: accepted authority, H0/R0, provenance, trust, and public state are unreconciled",
    "BLOCKED THEOREM-Z: dependency acceptance, root M0, cold/offline, supply chain, independent verifier, bundle, and master gates are open",
    "verdict=blocked; lifecycle=planned; accepted_root_vector=H1/M4/R3; audit_complete=false; theorem_complete=false",
)
SUMMARY_BYTES = ("\n".join(SUMMARY_LINES) + "\n").encode()


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
    argv: list[str],
    *,
    cwd: Path = ROOT,
    env: dict[str, str] | None = None,
    timeout: int = 180,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        argv,
        cwd=cwd,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=timeout,
        check=False,
    )


def git(*args: str, cwd: Path = ROOT) -> str:
    completed = run(["git", *args], cwd=cwd, timeout=30)
    assert completed.returncode == 0, completed.stdout
    return completed.stdout.strip()


def source_without_comments(source: str) -> str:
    output: list[str] = []
    index = 0
    depth = 0
    in_string = False
    escaped = False
    while index < len(source):
        pair = source[index : index + 2]
        char = source[index]
        if depth:
            if pair == "/-":
                depth += 1
                index += 2
            elif pair == "-/":
                depth -= 1
                index += 2
            else:
                index += 1
            continue
        if in_string:
            output.append(char)
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
            index += 1
            continue
        if pair == "/-":
            depth = 1
            index += 2
        elif pair == "--":
            newline = source.find("\n", index + 2)
            if newline < 0:
                break
            output.append("\n")
            index = newline + 1
        else:
            output.append(char)
            if char == '"':
                in_string = True
            index += 1
    assert depth == 0 and not in_string
    return "".join(output)


def reported_axioms(output: str, declaration: str) -> set[str]:
    pattern = re.compile(
        re.escape(f"'{declaration}' depends on axioms: [") + r"(.*?)]",
        flags=re.DOTALL,
    )
    matches = pattern.findall(output)
    no_axioms = output.count(f"'{declaration}' does not depend on any axioms")
    assert len(matches) + no_axioms == 1, declaration
    if not matches:
        return set()
    return {part.strip() for part in matches[0].split(",") if part.strip()}


def assert_text_hygiene(path: Path) -> None:
    data = path.read_bytes()
    assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines()), path


def main() -> None:
    os.umask(0o022)
    decision = load(HERE / "release-decision.json")
    spec = load(HERE / "release-spec.json")
    receipt = load(HERE / "release-receipt.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")
    instance = load(HERE / "instance.json")
    tasks = load(HERE / "task-dag.json")
    statement = load(HERE / "statement.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    proof = load(HERE / "proof-receipt.json")
    validation = load(HERE / "validation-receipt.json")
    targets = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 638
    assert target["baseline"] == "L0" and target["rework_required"] is True
    assert target["lifecycle_mode"] == "planned" and target["theorem_complete"] is False
    release_node = next(row for row in execution["items"] if row["id"] == ITEM)
    validation_node = next(
        row for row in execution["items"] if row["id"] == "S56-M-0600-VALIDATION"
    )
    assert release_node["state"] == "[ ]"
    assert release_node["depends_on"] == ["S56-M-0600-VALIDATION"]
    assert release_node["owned_paths"] == [f"Stage1_Instances/{THEOREM}"]
    assert validation_node["state"] == "[_]"

    accepted_vector = {"H": "H1", "M": "M4", "R": "R3"}
    provisional_vector = {"H": "H1", "M": "M3", "R": "R3"}
    assert instance["lifecycle"] == "planned"
    assert instance["root_vector"] == accepted_vector
    assert instance["accepted_proof_state"] == []
    assert instance["audit_complete"] is instance["theorem_complete"] is False
    assert tasks["lifecycle"] == "planned" and tasks["accepted_states"] == []
    assert all(row["state"] == "open" for row in tasks["tasks"])
    formal = statement["canonical_formal_target"]
    assert formal["declaration_or_expression"] == (
        "Stage1Instances.THM_M_0600.MorseLemmaTarget"
    )
    assert formal["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert registry["root_obligation_id"] == graphs["root_node_id"] == "M0600-ROOT"
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert len(registry["obligations"]) == 18
    closure = graphs["closure_boundary"]
    assert closure["root_closed"] is False
    assert closure["root_machine_debt"] == "M3"
    assert closure["remaining_root_cut_set"] == ["M0600-T-ENGINE"]
    assert closure["audit_complete"] is closure["theorem_complete"] is False
    root = next(node for node in graphs["nodes"] if node["obligation_id"] == "M0600-ROOT")
    assert {
        "H": root["human_debt"],
        "M": root["machine_debt"],
        "R": root["readability_debt"],
    } == provisional_vector
    assert graphs["graphs"]["evidence"]["edges"] == []

    assert sha256(HERE / "proof-receipt.json") == PROOF_RECEIPT_SHA256
    assert sha256(HERE / "validation-receipt.json") == VALIDATION_RECEIPT_SHA256
    assert proof["accepted"] is validation["accepted"] is False
    assert proof["accepted_closed_obligation_ids"] == []
    assert validation["accepted_receipt_ids"] == []
    assert validation["verdict"] == "blocked" and validation["release_grade"] is False
    assert validation["result"]["root_kernel_closed"] is False
    assert validation["result"]["accepted_closed_obligation_ids"] == []
    assert validation["result"]["audit_complete"] is False
    assert validation["result"]["theorem_complete"] is False

    assert decision["item_id"] == ITEM and decision["theorem_id"] == THEOREM
    assert decision["base_revision"] == BASE_REVISION and decision["base_tree"] == BASE_TREE
    assert decision["verdict"] == "blocked" and decision["release_grade"] is False
    assert decision["lifecycle_before"] == decision["lifecycle_after"] == "planned"
    assert decision["root_vector_before"] == decision["root_vector_after"] == accepted_vector
    assert decision["best_provisional_root_vector"] == provisional_vector
    assert decision["audit_complete"] is decision["theorem_complete"] is False
    assert decision["terminal_decisions"] == {"audit_z": "blocked", "theorem_z": "blocked"}
    assert decision["accepted_receipt_ids"] == []
    assert decision["dependency"]["receipt_sha256"] == VALIDATION_RECEIPT_SHA256
    assert decision["dependency"]["accepted"] is False
    assert decision["dependency"]["master_accepted"] is False
    assert decision["first_failed_gate"]["gate_id"] == "S56-10.2-DEPENDENCY-ACCEPTANCE"
    assert decision["first_failed_mathematical_gate"]["gate_id"] == (
        "M0600-T-ENGINE-KERNEL-CLOSURE"
    )
    assert decision["remaining_root_cut_set"] == ["M0600-T-ENGINE"]
    assert len(decision["authority_conflicts"]) == 3
    for key in (
        "dependency_master_accepted",
        "authoritative_state_reconciled",
        "accepted_root_m0",
        "exact_root_kernel_closed",
        "audit_z_accepted",
        "pinpoint_h0_source_review",
        "independent_r0_review",
        "complete_provenance_foundation_tcb_closure",
        "immutable_clean_release_input",
        "lake_manifest_package_closure_usable",
        "hermetic_cold_empty_cache_offline_replay",
        "complete_sbom_license_archive_closure",
        "two_independent_signed_runner_attestations",
        "independently_implemented_minimal_release_verifier",
        "protected_ci_and_adversarial_gates",
        "deterministic_content_addressed_release_bundle",
        "master_acceptance",
    ):
        assert decision["evidence_reconciliation"][key] is False, key

    assert spec["schema_version"] == "stage1-validation-spec/1.0"
    assert spec["item_id"] == ITEM and spec["theorem_id"] == THEOREM
    assert spec["argv"] == ["python3", "-I", "-B", str(Path(__file__).relative_to(ROOT))]
    assert spec["cwd"] == "." and spec["network_policy"] == "denied"
    assert spec["timeout_seconds"] == 600 and spec["expected_exit"] == 0
    assert set(spec["covered_obligation_ids"]) == {
        "M0600-S-DEFINITIONS", "M0600-T-ASSEMBLE"
    }
    assert set(spec["partially_covered_obligation_ids"]) == {
        "M0600-S-DIMZERO", "M0600-T-ENGINE"
    }
    assert spec["covered_decisions"] == ["AUDIT-Z", "THEOREM-Z"]

    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["phase"] == receipt["intent"] == "release"
    assert receipt["depends_on"] == ["S56-M-0600-VALIDATION"]
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["release_grade"] is receipt["content_addressed_release_evidence"] is False
    assert receipt["result"]["verdict"] == "blocked"
    assert receipt["result"]["accepted_root_vector"] == accepted_vector
    assert receipt["result"]["best_provisional_root_vector"] == provisional_vector
    assert receipt["result"]["accepted_receipt_ids"] == []
    assert receipt["result"]["audit_complete"] is receipt["result"]["theorem_complete"] is False
    assert receipt["first_failed_gate"] == "S56-10.2-DEPENDENCY-ACCEPTANCE"
    assert receipt["remaining_root_cut_set"] == ["M0600-T-ENGINE"]
    assert receipt["recipe"] == {
        key: spec[key]
        for key in (
            "recipe_id", "cwd", "argv", "env_allowlist", "timeout_seconds",
            "network_policy", "network_enforcement", "expected_exit",
            "expected_outputs", "covered_obligation_ids",
            "partially_covered_obligation_ids", "covered_declarations",
            "covered_decisions", "scope_boundary",
        )
    }
    for name, expected in UPSTREAM_INPUTS.items():
        assert sha256(HERE / name) == expected, name
        assert receipt["inputs"][name] == expected, name
    for name, expected in AUTHORITY_INPUTS.items():
        assert sha256(ROOT / name) == expected, name
        assert receipt["authority_inputs"][name] == expected, name
    for name in (
        "release-decision.json", "release-spec.json", "check_release.py", "release-phase.md"
    ):
        assert receipt["inputs"][name] == sha256(HERE / name), name

    assert git("rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert git("status", "--porcelain=v1", "--untracked-files=all", cwd=MATHLIB) == ""
    selected = validation["provenance"]["selected_mathlib_sources"]
    for relative, evidence in selected.items():
        olean = MATHLIB / ".lake/build/lib/lean" / Path(relative).with_suffix(".olean")
        assert sha256(olean) == evidence["olean_sha256"], relative

    historical_validation = (HERE / "check_validation.py").read_text(encoding="utf-8")
    assert 'BASE_REVISION = "7348dc646fd6babfe2b82c35b4c03a9ed5921f8e"' in historical_validation
    assert 'load(ROOT / ".stage1-worker-selftest.json")' in historical_validation
    stale = run(
        ["python3", "-I", "-B", str(HERE / "check_validation.py")], timeout=60
    )
    assert stale.returncode != 0

    # The separately recorded Lake probe observed an unresolved shared package HEAD.
    # Do not rerun a resolver here: another automation process may be changing that
    # shared cache, and this negative decision must not fetch, wait on, or mutate it.
    flt_head = LEAN_ROOT / ".lake/packages/flt-regular/.git/HEAD"
    if flt_head.is_file():
        flt_head_text = flt_head.read_text(encoding="utf-8").strip()
        assert flt_head_text.startswith("ref: ") or re.fullmatch(
            r"[0-9a-f]{40}", flt_head_text
        )

    all_source = "\n".join(
        source_without_comments((HERE / name).read_text(encoding="utf-8"))
        for name in (
            "Statement.lean", "ObligationTree.lean", "Proof.lean",
            "AnchorAudit.lean", "Validation.lean",
        )
    )
    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by)\b|"
        r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
        r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
        r"(?:axiom|constant|opaque|unsafe|extern)\b",
        re.MULTILINE,
    )
    assert prohibited.search(all_source) is None

    lean = Path.home() / ".elan/toolchains/leanprover--lean4---v4.29.0/bin/lean"
    bwrap = Path(shutil.which("bwrap") or "")
    assert lean.is_file() and bwrap.is_file()
    assert sha256(lean) == LEAN_EXECUTABLE_SHA256
    assert sha256(bwrap) == BWRAP_EXECUTABLE_SHA256
    lean_version = run([str(lean), "--version"], cwd=LEAN_ROOT)
    assert lean_version.returncode == 0 and LEAN_COMMIT in lean_version.stdout
    dependency_paths = [LEAN_ROOT / ".lake/build/lib/lean"]
    dependency_paths.extend(
        sorted(
            path for path in (LEAN_ROOT / ".lake/packages").glob("*/.lake/build/lib/lean")
            if path.is_dir()
        )
    )
    dependency_paths.append(lean.parents[1] / "lib/lean")
    assert MATHLIB / ".lake/build/lib/lean" in dependency_paths
    lean_path = ":".join(str(path) for path in dependency_paths if path.is_dir())

    tmp = Path(tempfile.mkdtemp(prefix="stage1-m0600-release-", dir="/tmp"))
    try:
        for name in (
            "Statement.lean", "ObligationTree.lean", "Proof.lean",
            "AnchorAudit.lean", "Validation.lean",
        ):
            shutil.copy2(HERE / name, tmp / name)
        (tmp / "home").mkdir()

        def isolated_lean(args: list[str], *, module_path: bool) -> str:
            module_search = f"{tmp}:{lean_path}" if module_path else lean_path
            command = [
                str(bwrap), "--ro-bind", "/", "/", "--bind", str(tmp), str(tmp),
                "--dev", "/dev", "--proc", "/proc", "--unshare-net",
                "--die-with-parent", "--clearenv", "--setenv", "HOME", str(tmp / "home"),
                "--setenv", "PATH", "/usr/bin:/bin", "--setenv", "ELAN_TOOLCHAIN",
                LEAN_TOOLCHAIN, "--setenv", "LANG", "C.UTF-8", "--setenv", "LC_ALL",
                "C.UTF-8", "--setenv", "TZ", "UTC", "--setenv", "LEAN_NUM_THREADS", "1",
                "--setenv", "LEAN_PATH", module_search, "--chdir", str(tmp), str(lean),
                "--trust=0", "-t0", *args,
            ]
            completed = run(command, timeout=300)
            assert completed.returncode == 0, completed.stdout
            return completed.stdout

        statement_output = isolated_lean(
            ["-o", "Statement.olean", "Statement.lean"], module_path=False
        )
        obligation_output = isolated_lean(
            ["-o", "ObligationTree.olean", "ObligationTree.lean"], module_path=True
        )
        proof_output = isolated_lean(
            ["-o", "Proof.olean", "Proof.lean"], module_path=True
        )
        anchor_output = isolated_lean(["AnchorAudit.lean"], module_path=True)
        validation_output = isolated_lean(["Validation.lean"], module_path=True)
    finally:
        shutil.rmtree(tmp)

    outputs = {
        "ObligationTree.lean": obligation_output,
        "Proof.lean": proof_output,
        "Validation.lean": validation_output,
    }
    observed = []
    for module, declarations in AXIOM_DECLARATIONS.items():
        for declaration in declarations:
            axioms = reported_axioms(outputs[module], declaration)
            assert axioms == ALLOWED_AXIOMS, (declaration, axioms)
            observed.append(declaration)
    assert len(observed) == 6
    assert proof_output.count("Declarations are sorry-free!") == 3
    assert validation_output.count("Declarations are sorry-free!") == 2
    combined = "\n".join(
        (statement_output, obligation_output, proof_output, anchor_output, validation_output)
    )
    assert "sorryAx" not in combined
    assert "declaration uses 'sorry'" not in combined
    assert "error:" not in combined

    assert receipt["execution"]["stdout_sha256"] == hashlib.sha256(SUMMARY_BYTES).hexdigest()
    assert receipt["execution"]["stdout_bytes"] == len(SUMMARY_BYTES)
    assert receipt["execution"]["stdout_line_count"] == len(SUMMARY_LINES)
    assert set(packet) == {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert packet["item_id"] == ITEM and packet["state"] == "[_]"
    assert packet["base_revision"] == BASE_REVISION
    assert set(packet["changed_paths"]) == set(receipt["changed_paths"]) == CHANGED_PATHS
    assert packet["commands"] == receipt["commands"]
    assert packet["output_summary"] == receipt["output_summary"]
    assert packet["known_failures"] == receipt["known_failures"]
    actual_changes = {
        line[3:]
        for line in git("status", "--short", "--untracked-files=all").splitlines()
        if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual_changes == CHANGED_PATHS, (actual_changes, CHANGED_PATHS)
    for relative in CHANGED_PATHS:
        assert_text_hygiene(ROOT / relative)

    print("\n".join(SUMMARY_LINES))


if __name__ == "__main__":
    main()
