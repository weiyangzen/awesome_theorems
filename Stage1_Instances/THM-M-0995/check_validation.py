#!/usr/bin/env python3
"""Fail-closed narrow validator for S56-M-0995-VALIDATION."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import platform
import re
import shutil
import subprocess


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0995"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM = "S56-M-0995-VALIDATION"
THEOREM = "THM-M-0995"
BASE_REVISION = "92246ea92c0c44282c05728798bc7c7e4a5a1464"
BASE_TREE = "bd58be98bf3046078c016d44fb4a677ea231cb23"
LEAN_BIN = Path.home() / ".elan/toolchains/leanprover--lean4---v4.29.0/bin/lean"
LAKE_BIN = Path.home() / ".elan/toolchains/leanprover--lean4---v4.29.0/bin/lake"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MATHLIB_REMOTE = "https://github.com/leanprover-community/mathlib4.git"
EXPRESSION_SHA256 = "0201bd579e5b8f490d8079891aec8d7e8b4d69c1534a18a9e6bc77e464faafa2"
DENOMINATOR_SHA256 = "29fa162b68c22ecc1c0b1edb83306a411eb8ddea7a4b546fbeb082270a425b18"
EXPECTED_AXIOMS = ["propext", "Classical.choice", "Quot.sound"]
EXPECTED_INPUTS = {
    "Statement.lean": "b50beed65dc1cd10f656024aa09085458e94233b0ac9baedec4c0c9ad31856c4",
    "ObligationTree.lean": "e58b7449e67e34bd17d73c7c586865815eb818fcf8527d11d4f861aa04636de2",
    "Proof.lean": "cfd897575f18ac24487454973d704adc1a2a28b3d7d08f9c564dceabb74b35bf",
    "Validation.lean": "3d98335d8e126547900a7c4277ec8a59895ae39c7eb407d85558b9676365e4d7",
    "statement.json": "33903f9a1be5ef4708e3502d1b14089f17fe2914088bc8701c9b8479f2696c7d",
    "intake.json": "9edb86ac0887c1cedd404df5d8b225c4e475df092adaaea3df2df9e138f22aa6",
    "anchor-audit.json": "2d537d4b61da85531850fdc3c3feb749d6202414abb7685caf610b522cd50c5c",
    "obligation-registry.json": "75257ea402dd35de1806255af02bbcd76cd9e542faf95832ca424f3ec4a1dfc0",
    "typed-graphs.json": "9cb8a3570b7ef7be64a66f1398ec6edb295e963c17abc2ca4544ab90c5c1b3c3",
    "validation-specs.json": "136fe9d976b34c554f9a02c78221d7bfbf1e9874599d534fdc2cdf035036fb31",
    "proof-receipt.json": "386a3891cb8c474eebe71971ffbccef7ece1b6dee6b5c9f620cbdfdaba92e3e7",
    "check_validation.sh": "2f528954f5e808906cfae5c5d42939e8338bc94141cf133d6fa4800952dc805c",
    "validation-spec.json": "f02f8269615fd7e22509bd9a861a575620de48ff35b18f2ad0cd1c7626da1c15",
    "validation-phase.md": "96a73d417f4081e2d2c15ffd07dba84b4646258850afe04ed561356175353997",
}
EXPECTED_TOOL_INPUTS = {
    "lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
EXPECTED_EXECUTABLES = {
    "lean": "3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf",
    "lake": "a608ff084d7e2af228b92a29d7c2fd083ba0580e46889175ec74a81678c98359",
    "python3": "b8d8288faefdd300201f43fcf00f6f539a27218eeed3a3dff5ab10b9c4c99700",
    "git": "8a48eefa306b9a2a9c3e576784a74ad7485779279e5a46ec43361a1864760e45",
    "bwrap": "0abea81db798ebf6b4742ac0664802d97521547a353c2a0dbdc21d76cbbfd2c0",
}
SELECTED_SOURCES = {
    "Mathlib/Probability/Moments/Basic.lean": {
        "blob": "57bef34db5d0342498e111a3c1db71192079d58b",
        "source": "9043dc54bc2898ae5a82a89b0f79537f61a6635424360dfb21d49098a63afd73",
        "olean": "f4d70f5712c9c26fb4f87dc186d7d10c0e42ad158315b6c8ff96fb430279f0e8",
        "regions": {(363, 378): "f6214d251c0ec8c8adf6c90283658ff71cb8dcf3c250c0883637e775aed08c74",
                    (429, 457): "dce75b2afa31d0fc3ad9b1c60c21f325c08e1eb8c8c60dc089cb393fbf42eb03"},
    },
    "Mathlib/Probability/Moments/Variance.lean": {
        "blob": "eec6b11abcd6df47b10c86369120299f41447320",
        "source": "920c022075149257307335beccbc8a62c7360fb3d9d73571b8240093dc2d72f0",
        "olean": "f852d980c81e4090e836efd8384cac224bbe6debf8d22178dd7bb5d417bc3262",
        "regions": {(159, 171): "1be112cd3f7afff20625107b2db24be98746c2b07819626e02e8dab43fddd58e"},
    },
    "Mathlib/Analysis/Normed/Algebra/Exponential.lean": {
        "blob": "0cf9823c36161af470a4354341e77c3a85f5bd79",
        "source": "e38a114005b7d7538f9ed037ceae3010607ee882b17cb861f465b245b0297be5",
        "olean": "213ecc5a9ed5647b3041db3422eb12f4fb5c64f828305fb8623722e134d070ca",
        "regions": {(471, 484): "7bd4b5d7eb3ba7939514624b501306e18f4ece6ace522d3546bdfa431c2e745a"},
    },
    "Mathlib/Data/Nat/Factorial/Basic.lean": {
        "blob": "dcd1f66bbdf4699008edd7b5193637b68e545d63",
        "source": "5978ee423d84693e2f488fc0ef1566508499581c0afdd7f0b0d2c3c4ce0b94f3",
        "olean": "f2a6c2cf0834edb61441f609867ec91a68762e9a9fd29b42f3b617d35c67f511",
        "regions": {(175, 185): "5a7759ce0c57e32b5dd8bcb311439c33d3fe45e2986ed862a011be3188ece188"},
    },
}
LICENSE_SHA256 = "b40930bbcf80744c86c46a12bc9da056641d722716c378f5659b9e555ef833e1"
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    "Stage1_Instances/THM-M-0995/Validation.lean",
    "Stage1_Instances/THM-M-0995/check_validation.py",
    "Stage1_Instances/THM-M-0995/check_validation.sh",
    "Stage1_Instances/THM-M-0995/validation-phase.md",
    "Stage1_Instances/THM-M-0995/validation-receipt.json",
    "Stage1_Instances/THM-M-0995/validation-spec.json",
}
SUMMARY = (
    "PASS THM-M-0995 narrow validation",
    "PASS network-isolated trust-zero kernel replay: exact statement, corrected compositions, proof roots, transport, and validation adapters elaborated",
    "PASS trust observation: 31 reports; exact roots and compositions use only propext, Classical.choice, and Quot.sound",
    "PASS selected provenance: frozen hashes, source/blob/body/olean identities, clean mathlib pin/tree/remote, license, and tools agree",
    "PASS hygiene: target Lean sources contain no placeholders, axiom/unsafe declarations, or generated artifacts",
    "FAIL CLOSED authority/trust: proof master acceptance and complete transitive provenance, foundation, and TCB closure remain open",
    "FAIL CLOSED hermetic/independent release: shared warm cache is not a cold offline replay; same-worker adapters are not a distinct signed verifier",
    "audit_complete=false; theorem_complete=false",
)


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict), path
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sha256_lines(path: Path, start: int, end: int) -> str:
    lines = path.read_bytes().splitlines(keepends=True)
    return hashlib.sha256(b"".join(lines[start - 1:end])).hexdigest()


def run(argv: list[str], *, cwd: Path = ROOT, timeout: int = 600) -> str:
    result = subprocess.run(
        argv, cwd=cwd, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        timeout=timeout, check=False,
    )
    if result.returncode:
        raise RuntimeError(f"command failed ({result.returncode}): {argv!r}\n{result.stdout}")
    return result.stdout


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["git", *args], cwd=cwd, timeout=30).strip()


def code_without_comments(source: str) -> str:
    source = re.sub(r"/-.*?-/", "", source, flags=re.DOTALL)
    return re.sub(r"--.*$", "", source, flags=re.MULTILINE)


def main() -> None:
    spec = load(HERE / "validation-spec.json")
    receipt = load(HERE / "validation-receipt.json")
    targets = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    intake = load(HERE / "intake.json")
    statement = load(HERE / "statement.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    proof_receipt = load(HERE / "proof-receipt.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 275 and target["baseline"] == "L0"
    assert target["lifecycle_mode"] == "planned"
    assert target["rework_required"] is True and target["theorem_complete"] is False
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item["state"] == "[ ]" and item["depends_on"] == ["S56-M-0995-PROOF"]
    predecessor = next(row for row in execution["items"] if row["id"] == "S56-M-0995-PROOF")
    assert predecessor["state"] == "[_]"
    assert intake["lifecycle_mode"] == "planned"
    assert intake["root_vector"] == {"human": "H2", "machine": "M3", "readability": "R3"}
    assert intake["theorem_complete"] is False

    formal = statement["canonical_formal_target"]
    assert formal["declaration_or_expression"] == "Stage1Instances.THM_M_0995.StatementShape"
    assert formal["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert registry["root_obligation_id"] == "M0995-ROOT"
    assert registry["registry_version"] == 2
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert graphs["registry_version"] == 2
    assert graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    closure = graphs["closure_boundary"]
    assert closure["root_closed"] is True and closure["root_machine_debt"] == "M0-L"
    assert closure["audit_complete"] is closure["theorem_complete"] is False
    assert proof_receipt["support_state"] == "provisional_worker_selftest"
    assert proof_receipt["result"]["theorem_complete"] is False

    for name, expected in EXPECTED_INPUTS.items():
        assert sha256(HERE / name) == expected, f"stale validation input: {name}"
        assert receipt["inputs"].get(name) == expected or name == "validation-phase.md", name
    for name, expected in EXPECTED_TOOL_INPUTS.items():
        assert sha256(LEAN_ROOT / name) == expected, f"changed tool input: {name}"
        assert receipt["inputs"][name] == expected

    assert MATHLIB.resolve().is_dir()
    assert git("rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert git("status", "--porcelain=v1", cwd=MATHLIB) == ""
    assert git("remote", "get-url", "origin", cwd=MATHLIB) == MATHLIB_REMOTE
    assert sha256(MATHLIB / "LICENSE") == LICENSE_SHA256
    for relative, expected in SELECTED_SOURCES.items():
        source = MATHLIB / relative
        assert git("rev-parse", f"HEAD:{relative}", cwd=MATHLIB) == expected["blob"]
        assert sha256(source) == expected["source"]
        olean = MATHLIB / ".lake/build/lib/lean" / relative.replace(".lean", ".olean")
        assert sha256(olean) == expected["olean"]
        for (start, end), digest in expected["regions"].items():
            assert sha256_lines(source, start, end) == digest

    lean = LEAN_BIN
    lake = LAKE_BIN
    assert lean.is_file() and lake.is_file()
    python_path = shutil.which("python3")
    git_path = shutil.which("git")
    bwrap_path = shutil.which("bwrap")
    assert python_path and git_path and bwrap_path
    executables = {
        "lean": lean,
        "lake": lake,
        "python3": Path(os.path.realpath(python_path)),
        "git": Path(os.path.realpath(git_path)),
        "bwrap": Path(os.path.realpath(bwrap_path)),
    }
    for name, path in executables.items():
        assert sha256(path) == EXPECTED_EXECUTABLES[name], (name, path)

    prohibited = re.compile(r"\b(?:sorry|admit|sorryAx)\b|^\s*(?:axiom|unsafe|extern)\b", re.MULTILINE)
    for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
        assert prohibited.search(code_without_comments((HERE / name).read_text(encoding="utf-8"))) is None
    assert not list(HERE.glob("*.olean")) and not list(HERE.glob("tmp*.lean"))

    for key in (
        "recipe_id", "cwd", "argv", "env_allowlist", "timeout_seconds", "network_policy",
        "expected_exit", "expected_outputs",
    ):
        assert receipt["recipe"][key] == spec[key], key
    assert receipt["item_id"] == spec["item_id"] == ITEM
    assert receipt["theorem_id"] == spec["theorem_id"] == THEOREM
    assert receipt["accepted"] is receipt["release_grade"] is False
    assert receipt["accepted_closed_obligation_ids"] == []
    assert receipt["first_failed_gate"] == "dependency.S56-M-0995-PROOF.master_acceptance"
    assert receipt["first_failed_release_gate"] == "S56-10.6-HERMETIC-COLD-BUILD"
    result = receipt["result"]
    assert result["exact_root_kernel_replay"] == "provisional_pass"
    assert result["observed_axioms"] == EXPECTED_AXIOMS
    assert result["axiom_report_count"] == 31
    assert result["placeholder_and_unsafe_scan"] == "pass"
    assert result["proof_master_acceptance"] == "fail_closed"
    assert result["foundation_and_complete_trust_closure"] == "fail_closed"
    assert result["hermetic_cold_offline_replay"] == "fail_closed"
    assert result["independent_distinct_runner"] == "fail_closed"
    assert result["audit_complete"] is result["theorem_complete"] is False

    assert set(packet) == {
        "item_id", "changed_paths", "commands", "output_summary", "base_revision",
        "known_failures", "state",
    }
    assert packet["item_id"] == ITEM and packet["state"] == "[_]"
    assert packet["base_revision"] == BASE_REVISION
    assert set(packet["changed_paths"]) == CHANGED_PATHS
    status = git("status", "--short", "--untracked-files=all")
    actual_changed = {
        line[3:] for line in status.splitlines()
        if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual_changed == CHANGED_PATHS, (actual_changed, CHANGED_PATHS)

    replay = run(["bash", str(HERE / "check_validation.sh")], timeout=600)
    for token in (
        "PASS axiom profile: 31 reports",
        "PASS validation adapters: three declarations are sorry-free",
        "PASS THM-M-0995 proof hygiene",
    ):
        assert token in replay
    assert "error:" not in replay and "sorryAx" not in replay
    assert platform.system() == "Linux"
    print("\n".join(SUMMARY))


if __name__ == "__main__":
    main()
