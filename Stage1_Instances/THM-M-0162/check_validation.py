#!/usr/bin/env python3
"""Fail-closed narrow validation for S56-M-0162-VALIDATION."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0162"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM = "S56-M-0162-VALIDATION"
THEOREM = "THM-M-0162"
BASE_REVISION = "443b8bbc23bf35a1e7a4bb7b3183073f76bbee2b"
BASE_TREE = "c5771c47c12b80aba613e6d844570f83b39ded6d"
DENOMINATOR_SHA256 = "28db67d8555342a82bfb4d209445a5c10be82fe50e7b8f2763bdebdb54ca23ff"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MATHLIB_REMOTE = "https://github.com/leanprover-community/mathlib4.git"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
LEAN_TOOLCHAIN = "leanprover/lean4:v4.29.0"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
EXPECTED_INPUTS = {
    "Statement.lean": "a3b7283df516fbba35412815a954b6d9ad4acb1e79b2c33fe473ac3da50073c2",
    "ObligationTree.lean": "a4bbed3b1777b7c24c7abf1e7a75e421158b95f8edc0d876ccdfa930aa8b1a3a",
    "Proof.lean": "968d9933bf08d4b315d54ef9bdf8215a5fd4b41b51f168541f2135d1213d09b9",
    "statement.json": "510eaa244250add3617bb8d239e0eb9802b5538da203a6614bff6228baad6754",
    "anchor-audit.json": "97233583a43cca9f53b0397cc3cbf66eae4c31dbdb926e42ee6133571a99047d",
    "obligation-registry.json": "5efb429c678746fbad8e8767a5e2ebcfaf44dc4bae5195be5e7943fb4d93994d",
    "typed-graphs.json": "79efc75d0aa3dc7b126648ad8f135c9e3e69806f365dda23c832fd54ebf43abe",
    "validation-specs.json": "dfac58e3cda47c11ef822befa96b8b078a407552ac70129af1321b6d6b63757c",
    "proof-receipt.json": "3c1bf3f58d0e0f598e3c69540f581afc5bcbad2bef58514ed8a6ebec1e44fd34",
    "source-statement-crosswalk.md": "52964a0a40810440530a0a62c032389c884715d7a8b4d5b0d692265c2d2922fd",
    "check_obligation_tree.py": "b31269817070ecfd131195ab98b9426a93feaf285a8190fd956f0db8774b5655",
    "Validation.lean": "e2f441f72d3b7b02ff4a79d58d89f8b7050d797e4c000213e9b42fb9b0563674",
    "check_validation.sh": "c77fd32158a4cf870c4e823b5ebce665a6932ced746cd1cf4354197cc22756f3",
    "validation-spec.json": "8f6ef9e92f0fe2c32ecd1fab8127fb2fcd7dc37f4206c1ef3c1697c9ada6e733",
}
EXPECTED_TOOL_INPUTS = {
    "lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
EXPECTED_VALIDATION_OLEANS = {
    "Statement.olean": "600c5c2245299aab10f2b06d7c5e265b13645ea765535b4eb6cd5bcdacb740cb",
    "ObligationTree.olean": "49337fdb13e00d360fc326802d5b9d130ccd4b0ca2b0a75c3868127fe702714e",
    "Proof.olean": "d05074e8f9cbfcdf27e08aa7195c4e5d8ea3eca6e96871abcd5d0a35d10b7984",
    "Validation.olean": "8753f976886261190656a942cdd16023af5285548e1ef09a0b365a05fabce75c",
}
MACHINE_IDS = [
    "M0162-ROOT",
    "M0162-S-PREMISES",
    "M0162-S-FOUNDATION",
    "M0162-F-ORTHONORMAL",
    "M0162-D-INNER",
    "M0162-A-DECOMPOSE",
    "M0162-E-TANGENT",
    "M0162-C-NORMAL-T",
    "M0162-C-NORMAL-N",
    "M0162-C-NORMAL-B",
    "M0162-E-NORMAL",
    "M0162-D-CROSS",
    "M0162-C-BINORMAL",
    "M0162-E-BINORMAL",
    "M0162-T-ASSEMBLE",
]
ALL_IDS = MACHINE_IDS + ["M0162-X-SOURCE", "M0162-X-PROVENANCE"]
REPLAYED_IDS = [
    "M0162-ROOT",
    "M0162-S-PREMISES",
    "M0162-E-TANGENT",
    "M0162-E-NORMAL",
    "M0162-E-BINORMAL",
    "M0162-T-ASSEMBLE",
]
TRUST_DECLARATIONS = [
    "Stage1Instances.THM_M_0162.tangentEquation",
    "Stage1Instances.THM_M_0162.normalEquation",
    "Stage1Instances.THM_M_0162.binormalEquation",
    "Stage1Instances.THM_M_0162.frenetSerret",
]
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
    "PASS THM-M-0162 narrow validation",
    "PASS network-denied trust-zero kernel replay: exact statement, frozen composition, local proof, and proof-only trust probe elaborated from fresh outputs",
    "PASS hygiene: Lean transitive sorry collectors and a nested-comment-aware prohibited-construct scan passed",
    "PASS selected provenance: frozen local hashes, proof receipt, mathlib source pin, clean mathlib checkout, license, and tool identities agree",
    "FAIL CLOSED dependency: S56-M-0162-PROOF is provisional [_], not master accepted",
    "FAIL CLOSED authority: registry and typed graphs retain the pre-proof H1/M3/R4 open-root state and accept no proof evidence",
    "FAIL CLOSED foundation/provenance/TCB: observed axioms lack accepted policy and complete transitive closure",
    "FAIL CLOSED hermetic release: shared warm .lake and unavailable root flt-regular package are not an empty-cache clean-checkout offline replay",
    "FAIL CLOSED independent release: trust-only probe shares this worker, checkout, kernel, and cache; no distinct signed runner or minimal verifier exists",
    "audit_complete=false; theorem_complete=false",
)
STARTED = time.monotonic()
TIMEOUT_SECONDS = 900.0


if sys.flags.optimize:
    raise SystemExit("validation failed: Python optimization disables assertions")


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict), path
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(argv: list[str], *, cwd: Path = ROOT, env: dict[str, str] | None = None) -> str:
    remaining = TIMEOUT_SECONDS - (time.monotonic() - STARTED)
    assert remaining > 0, "validation recipe timed out"
    result = subprocess.run(
        argv,
        cwd=cwd,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=remaining,
        check=False,
    )
    if result.returncode:
        raise RuntimeError(f"validation failed ({result.returncode}): {argv!r}\n{result.stdout}")
    return result.stdout


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["git", *args], cwd=cwd).strip()


def code_without_comments(source: str) -> str:
    output: list[str] = []
    depth = 0
    index = 0
    while index < len(source):
        if source.startswith("/-", index):
            depth += 1
            index += 2
        elif depth and source.startswith("-/", index):
            depth -= 1
            index += 2
        elif depth:
            index += 1
        elif source.startswith("--", index):
            newline = source.find("\n", index)
            index = len(source) if newline < 0 else newline
        else:
            output.append(source[index])
            index += 1
    assert depth == 0, "unterminated Lean block comment"
    return "".join(output)


def observed_axioms(output: str, declaration: str) -> set[str]:
    match = re.search(
        re.escape(f"'{declaration}' depends on axioms: [") + r"(.*?)]",
        output,
        re.DOTALL,
    )
    if match is None:
        assert f"'{declaration}' does not depend on any axioms" in output, declaration
        return set()
    return {part.strip() for part in match.group(1).split(",") if part.strip()}


def main() -> None:
    targets = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    statement = load(HERE / "statement.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    frozen_specs = load(HERE / "validation-specs.json")
    proof_receipt = load(HERE / "proof-receipt.json")
    spec = load(HERE / "validation-spec.json")
    receipt = load(HERE / "validation-receipt.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 661 and target["baseline"] == "L0"
    assert target["lifecycle_mode"] == "planned"
    assert target["rework_required"] is True and target["theorem_complete"] is False
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item["theorem_id"] == THEOREM and item["execution_rank"] == 661
    assert item["phase"] == "validation" and item["layer"] == 5
    assert item["state"] in {"[ ]", "[_]"}
    assert item["depends_on"] == ["S56-M-0162-PROOF"]
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM}"]
    predecessor = next(row for row in execution["items"] if row["id"] == "S56-M-0162-PROOF")
    assert predecessor["state"] == "[_]" and predecessor["attempts"] >= 1

    for name, expected in EXPECTED_INPUTS.items():
        assert sha256(HERE / name) == expected, f"stale validation input: {name}"
    for name, expected in EXPECTED_TOOL_INPUTS.items():
        assert sha256(LEAN_ROOT / name) == expected, f"changed tool input: {name}"
    assert statement["declaration"] == "Stage1Instances.THM_M_0162.FrenetSerretTarget"
    assert statement["statement_sha256"] == EXPECTED_INPUTS["Statement.lean"]
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert [row["obligation_id"] for row in registry["obligations"]] == ALL_IDS
    assert {row["obligation_id"] for row in frozen_specs["recipes"]} == set(ALL_IDS)

    proof_body = proof_receipt["proof_body"]
    assert proof_receipt["accepted"] is False
    assert proof_receipt["support_state"] == "provisional_worker_selftest"
    assert proof_body["source_sha256"] == EXPECTED_INPUTS["Proof.lean"]
    assert proof_body["root_declaration"] == TRUST_DECLARATIONS[-1]
    assert proof_receipt["result"]["root_kernel_closed"] is True
    assert proof_receipt["result"]["accepted_root_closed"] is False
    assert set(proof_receipt["result"]["axioms"]) == EXPECTED_AXIOMS
    assert proof_receipt["debt_vector"]["accepted_after_worker_selftest"] == {
        "H": "H1", "M": "M3", "R": "R4"
    }

    assert graphs["closure_boundary"]["root_closed"] is False
    assert graphs["closure_boundary"]["audit_complete"] is False
    assert graphs["closure_boundary"]["theorem_complete"] is False
    assert graphs["closure_boundary"]["remaining_root_cut_set"] == [
        "M0162-E-TANGENT", "M0162-E-NORMAL", "M0162-E-BINORMAL"
    ]
    assert registry["status_observed_after_freeze"]["root_machine_debt"] == "M3"
    assert registry["status_observed_after_freeze"]["closed_obligations"] == [
        "M0162-S-PREMISES", "M0162-T-ASSEMBLE"
    ]

    recipe = spec["recipes"]
    assert len(recipe) == 1
    recipe = recipe[0]
    assert recipe["recipe_id"] == "M0162-validation-fail-closed-runner-v1"
    assert recipe["cwd"] == "."
    assert recipe["argv"] == [
        "python3", "-I", "-B", "Stage1_Instances/THM-M-0162/check_validation.py"
    ]
    assert recipe["env_allowlist"] == {
        "ELAN_TOOLCHAIN": LEAN_TOOLCHAIN,
        "PATH": "explicitly_variable_for_pinned_launcher_and_checked_host_helpers",
    }
    assert recipe["timeout_seconds"] == 900
    assert recipe["network_policy"] == "denied" and recipe["expected_exit"] == 0
    assert recipe["covered_obligation_ids"] == REPLAYED_IDS
    assert set(recipe["covered_declarations"]) == {
        "Stage1Instances.THM_M_0162.FrenetSerretTarget",
        "Stage1Instances.THM_M_0162.root_of_equation_packages",
        *TRUST_DECLARATIONS,
    }

    bad = re.compile(
        r"\b(?:sorry|admit|sorryAx|implemented_by|native_decide)\b"
        r"|^[ \t]*(?:axiom|constant|opaque|unsafe|extern)\b",
        re.MULTILINE,
    )
    for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
        source = (HERE / name).read_text(encoding="utf-8")
        assert not bad.search(code_without_comments(source)), f"prohibited construct: {name}"

    assert git("rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert git("remote", "get-url", "origin", cwd=MATHLIB) == MATHLIB_REMOTE
    assert git("status", "--porcelain=v1", "--untracked-files=all", cwd=MATHLIB) == ""
    assert sha256(MATHLIB / "LICENSE") == "b40930bbcf80744c86c46a12bc9da056641d722716c378f5659b9e555ef833e1"

    lean_env = dict(os.environ)
    lean_env["ELAN_TOOLCHAIN"] = LEAN_TOOLCHAIN
    lean_bin = Path(run(["elan", "which", "lean"], cwd=LEAN_ROOT, env=lean_env).strip())
    lake_bin = Path(run(["elan", "which", "lake"], cwd=LEAN_ROOT, env=lean_env).strip())
    assert lean_bin.is_file() and lake_bin.is_file()
    assert sha256(lean_bin) == "3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf"
    assert sha256(lake_bin) == "a608ff084d7e2af228b92a29d7c2fd083ba0580e46889175ec74a81678c98359"
    lean_version = run(["elan", "run", LEAN_TOOLCHAIN, "lean", "--version"], cwd=LEAN_ROOT, env=lean_env)
    assert "Lean (version 4.29.0" in lean_version and LEAN_COMMIT in lean_version
    replay_env = dict(os.environ)
    replay_env["ELAN_TOOLCHAIN"] = LEAN_TOOLCHAIN
    replay_env["STAGE1_M0162_LAKE_BIN"] = str(lake_bin)
    replay_env["STAGE1_M0162_LEAN_BIN"] = str(lean_bin)
    assert replay_env["STAGE1_M0162_LAKE_BIN"], "Lake launcher missing"
    replay = run(["bash", str(HERE / "check_validation.sh")], env=replay_env)
    assert "PASS network-denied trust-zero fresh-output replay" in replay
    assert replay.count("Declarations are sorry-free!") == len(TRUST_DECLARATIONS)
    for declaration in TRUST_DECLARATIONS:
        assert observed_axioms(replay, declaration) == EXPECTED_AXIOMS
    for name, digest in EXPECTED_VALIDATION_OLEANS.items():
        assert f"{name} sha256: {digest}" in replay
    assert "sorryAx" not in replay and "error:" not in replay

    tree_output = run(["python3", "-I", "-B", str(HERE / "check_obligation_tree.py")])
    assert "PASS THM-M-0162 obligation tree: 17 obligations, 49 typed edges" in tree_output
    assert "root closure: open (M3)" in tree_output

    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["accepted"] is False and receipt["proposed_state"] == "[_]"
    assert receipt["release_grade"] is False
    assert receipt["result"]["provisional_root_kernel_closed"] is True
    assert receipt["result"]["accepted_closed_obligation_ids"] == []
    assert receipt["result"]["audit_complete"] is False
    assert receipt["result"]["theorem_complete"] is False
    assert receipt["first_failed_gate"] == "S56-M-0162-VALIDATION-PREREQUISITE-NOT-ACCEPTED"
    assert receipt["first_failed_release_gate"] == "S56-10.6-HERMETIC-COLD-BUILD"
    assert receipt["inputs"]["check_validation.py"] == sha256(HERE / "check_validation.py")
    assert receipt["inputs"]["validation-receipt.json"] == "self_excluded"
    assert receipt["inputs"]["validation-phase.md"] == sha256(HERE / "validation-phase.md")
    assert receipt["recipe"] == recipe

    assert packet["item_id"] == ITEM and packet["state"] == "[_]"
    assert packet["base_revision"] == BASE_REVISION
    assert set(packet["changed_paths"]) == CHANGED_PATHS
    assert packet["known_failures"] == receipt["known_failures"]
    assert any(command == recipe["argv"] for command in packet["commands"])
    for line in SUMMARY_LINES:
        assert line in packet["output_summary"]

    status = git("status", "--porcelain=v1", "--untracked-files=all").splitlines()
    actual = {line[3:] for line in status if line[3:] != "Formalizations/Lean/.lake"}
    assert actual == CHANGED_PATHS, (actual, CHANGED_PATHS)
    assert all(line == "?? Formalizations/Lean/.lake" or line.startswith("?? ") for line in status)
    run(["git", "diff", "--check", "--", f"Stage1_Instances/{THEOREM}", ".stage1-worker-selftest.json"])

    for line in SUMMARY_LINES:
        print(line)


if __name__ == "__main__":
    main()
