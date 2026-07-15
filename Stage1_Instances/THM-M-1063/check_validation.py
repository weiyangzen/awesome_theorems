#!/usr/bin/env python3
"""Fail-closed validation replay for S56-M-1063-VALIDATION."""

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
import time


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-1063"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM = "S56-M-1063-VALIDATION"
THEOREM = "THM-M-1063"
BASE_REVISION = "be2be0dfe2f4f2cbdd35f1f2397e5a372d199eb9"
BASE_TREE = "2d3961f99039c515141bdff4511470530d799581"
EXPRESSION_SHA256 = "a5bb2e2443661e20f8342ed0dba6b7f7ef5f5ce445bc2d5bbdf19ef5ce842c81"
DENOMINATOR_SHA256 = "a55c3e289a005535836506a2ce233e3dbb5fa0a7b84717b38c221583d26a7703"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MATHLIB_REMOTE = "https://github.com/leanprover-community/mathlib4.git"
MATHLIB_LICENSE_SHA256 = "b40930bbcf80744c86c46a12bc9da056641d722716c378f5659b9e555ef833e1"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
REMAINING_CUT = [
    "M1063-L-CLT",
    "M1063-L-MODULUS",
    "M1063-L-ASCOLI",
    "M1063-L-PROKHOROV",
    "M1063-L-LAW-UNIQUE",
    "M1063-T-API",
]
EXPECTED_INPUTS = {
    "DonskerTarget.lean": "de889c475bd663395eb9385627686109c645ba3446ee513c4019cf82f00a1847",
    "ObligationTree.lean": "047c49fd7cefcec9845244077afe72a5cd11d2cbf55022c7b6d307c036991425",
    "AnchorAudit.lean": "dabce3ddee0e44881a0c36e7c9a5ad2153f2a61773c425fe75f9acbee7cf4e43",
    "Proof.lean": "c854d084d0d3b7d3533f9a8995b3fb81883ccfbe06014cead9871680f128174c",
    "Validation.lean": "3ea9e1da4381d75d1518e22b5ee873908f9ef30d6503e31fda93bd75226241ec",
    "statement.json": "a9392798454f8d3a887bd6497b066133b4169fb1a9e1dd07d028f03f461e9ea5",
    "obligation-registry.json": "7886d9ce4b1552493476e336bfb5cc1b7537debe8249e61989cdeec86a85d5e8",
    "typed-graphs.json": "e63f2ce6eab9bc6fa942b6e1a412ab0b07063fcc978676daf125779c6a0875b5",
    "proof-receipt.json": "daa917db3198c92f240f3b1ea53668ae732d252314a5b3d8eea684e6cf2be8a0",
    "proof-blocker.json": "4a47d2ee19bb4fa0a7fa89e22e887f9ff3db6ceffea0bc4477720eb76ef18638",
    "proof-validation.md": "45ee8230a40860916f6844185f7eafba99ef363a6fe57f0f973682adcfea92f7",
    "check_obligation_tree.py": "7b9c5f8eecd83f065f706130694d7a49d566a9f1214b5fac54f4792fd55b8c42",
    "check_proof.sh": "66ceaa959161e55fe2da1cb530ee88dfb3988fe4904b83b8d1c9b9210ea94263",
}
TOOL_INPUTS = {
    "lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
MATHLIB_SOURCES = {
    "Mathlib/Probability/CentralLimitTheorem.lean": (
        "e0cfc897a4679025f71712abbf8834c1f318b2c1",
        "4b42bad9589ec3772fe0e884ad70789c89fd0c11566d980f3df1c862bbc7f03d",
        "d3b747f6dd0a15d12d10d29a4cc86980a72b54d0af741dc31cf5b70a0b70b988",
    ),
    "Mathlib/MeasureTheory/Function/ConvergenceInDistribution.lean": (
        "a95a9ecdbe93c2d4803d555d5d0f409e73a6b3e8",
        "dd3167a8ec5186a193d04992f31b33599c06f5209c29aed64f1f597cc30d843a",
        "f6ddef21cce1667d6a6b4721c2643f0b9d2c7ed3f1f82b120767b85c92e66b89",
    ),
    "Mathlib/Probability/Distributions/Gaussian/IsGaussianProcess/Basic.lean": (
        "5f40ebb2479839da872d565bfe932dfae2074a9d",
        "b324daeb7f5868696e257f603b1eed66e72228890bdc32c251f838f7c08421b3",
        "1b6d9f0530fc05deed850214607c75e822dc19bc0f1929eb75961dd9511180ed",
    ),
}
PROOF_DECLARATIONS = (
    "AwesomeTheorems.Stage1.THM_M_1063.Proof.standardizedIncrement_package",
    "AwesomeTheorems.Stage1.THM_M_1063.Proof.scalarPartialSums_tendstoInDistribution",
)
DIFFERENTIAL_DECLARATIONS = (
    "AwesomeTheorems.Stage1.THM_M_1063.Validation.independentlyStandardized",
    "AwesomeTheorems.Stage1.THM_M_1063.Validation.independentlyReplayedScalarCLT",
)
SUMMARY_LINES = (
    "PASS THM-M-1063 network-isolated trust-zero replay of the exact statement, conditional root interface, anchors, and two partial proof bodies",
    "PASS hygiene and observed trust: proof and differential declarations use exactly propext, Classical.choice, and Quot.sound",
    "PASS selected provenance: frozen hashes, clean mathlib pin/tree/origin/license, selected sources, and oleans agree",
    "OPEN exact Donsker root: zero frozen obligations are closed and all 29 required terminal proof-body IDs are null",
    "BLOCKED validation gates: proof master acceptance/root closure, complete TCB/provenance, cold offline hermetic replay, and distinct-runner verification",
)
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    "Stage1_Instances/THM-M-1063/Validation.lean",
    "Stage1_Instances/THM-M-1063/check_validation.py",
    "Stage1_Instances/THM-M-1063/validation-blocker.json",
    "Stage1_Instances/THM-M-1063/validation-phase.md",
    "Stage1_Instances/THM-M-1063/validation-receipt.json",
    "Stage1_Instances/THM-M-1063/validation-spec.json",
}
STARTED = time.monotonic()
TIMEOUT_SECONDS = 1200.0


if sys.flags.optimize:
    raise SystemExit("validation failed: Python optimization disables assertions")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path: Path) -> dict:
    def no_duplicates(pairs: list[tuple[str, object]]) -> dict:
        value: dict[str, object] = {}
        for key, item in pairs:
            assert key not in value, f"duplicate JSON key in {path}: {key}"
            value[key] = item
        return value

    value = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=no_duplicates)
    assert isinstance(value, dict), path
    return value


def run(argv: list[str], *, cwd: Path = ROOT, env: dict[str, str] | None = None) -> str:
    remaining = TIMEOUT_SECONDS - (time.monotonic() - STARTED)
    assert remaining > 0, "validation recipe exceeded its wall-clock bound"
    result = subprocess.run(
        argv, cwd=cwd, env=env, text=True, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, timeout=remaining, check=False,
    )
    if result.returncode:
        raise RuntimeError(f"command failed ({result.returncode}): {argv!r}\n{result.stdout}")
    return result.stdout


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["/usr/bin/git", *args], cwd=cwd).strip()


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


def axiom_set(output: str, declaration: str) -> set[str]:
    pattern = re.escape(f"'{declaration}' depends on axioms: [") + r"(.*?)]"
    matches = re.findall(pattern, output, re.DOTALL)
    assert len(matches) == 1, (declaration, len(matches))
    return {part.strip() for part in matches[0].split(",") if part.strip()}


def lean_executable() -> Path:
    toolchain = (LEAN_ROOT / "lean-toolchain").read_text().strip()
    directory = toolchain.replace("/", "--").replace(":", "---")
    return Path.home() / ".elan" / "toolchains" / directory / "bin" / "lean"


def lean_path(lean: Path) -> str:
    roots = sorted(
        path.resolve()
        for path in (LEAN_ROOT / ".lake" / "packages").glob("*/.lake/build/lib/lean")
        if path.is_dir() and "flt-regular" not in path.parts
    )
    roots.append((LEAN_ROOT / ".lake" / "build" / "lib" / "lean").resolve())
    roots.append((lean.parent.parent / "lib" / "lean").resolve())
    return ":".join(map(str, roots))


def kernel_replay() -> str:
    lean = lean_executable()
    assert lean.is_file() and os.access(lean, os.X_OK)
    path = lean_path(lean)
    with tempfile.TemporaryDirectory(prefix="m1063-validation-") as raw_tmp:
        tmp = Path(raw_tmp)
        for name in ("DonskerTarget.lean", "ObligationTree.lean", "AnchorAudit.lean", "Proof.lean", "Validation.lean"):
            shutil.copy2(HERE / name, tmp / name)
        base = [
            "/usr/bin/bwrap", "--ro-bind", "/", "/", "--bind", str(tmp), str(tmp),
            "--dev", "/dev", "--proc", "/proc", "--unshare-net", "--die-with-parent",
            "--clearenv", "--setenv", "HOME", str(tmp), "--setenv", "LANG", "C.UTF-8",
            "--setenv", "LC_ALL", "C.UTF-8", "--setenv", "TZ", "UTC",
            "--setenv", "LEAN_NUM_THREADS", "1", "--chdir", str(tmp),
        ]

        def replay(name: str) -> str:
            return run(base + ["--setenv", "LEAN_PATH", path, str(lean), "--trust=0", "-t0", str(tmp / name)])

        outputs = {
            name: replay(name)
            for name in ("DonskerTarget.lean", "ObligationTree.lean", "AnchorAudit.lean", "Proof.lean", "Validation.lean")
        }
    assert "DonskerInvariancePrinciple" in outputs["DonskerTarget.lean"]
    assert "exactRoot_of_exactRoot" in outputs["ObligationTree.lean"]
    for declaration in PROOF_DECLARATIONS:
        assert axiom_set(outputs["Proof.lean"], declaration) == EXPECTED_AXIOMS
    for declaration in DIFFERENTIAL_DECLARATIONS:
        assert axiom_set(outputs["Validation.lean"], declaration) == EXPECTED_AXIOMS
    combined = "\n".join(outputs.values())
    assert "sorryAx" not in combined and "declaration uses 'sorry'" not in combined
    assert not re.search(r"(^|\n).*error(?:\([^)]*\))?:", combined)
    return combined


def main() -> None:
    receipt = load(HERE / "validation-receipt.json")
    spec = load(HERE / "validation-spec.json")
    blocker = load(HERE / "validation-blocker.json")
    statement = load(HERE / "statement.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    proof_receipt = load(HERE / "proof-receipt.json")
    execution = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item["theorem_id"] == THEOREM and item["execution_rank"] == 506
    assert item["phase"] == "validation" and item["layer"] == 5
    assert item["state"] == "[ ]" and item["attempts"] == 0
    assert item["depends_on"] == ["S56-M-1063-PROOF"]
    predecessor = next(row for row in execution["items"] if row["id"] == "S56-M-1063-PROOF")
    assert predecessor["state"] == "[_]"

    for name, digest in EXPECTED_INPUTS.items():
        assert sha256(HERE / name) == digest, name
        assert receipt["inputs"][name] == digest, name
    for name, digest in TOOL_INPUTS.items():
        assert sha256(LEAN_ROOT / name) == digest
        assert receipt["inputs"][name] == digest

    required_machine = registry["frozen_denominators"]["required_machine"]
    assert len(registry["obligations"]) == 31 and len(required_machine) == 29
    assert all(
        row["terminal_proof_body_id"] is None
        for row in registry["obligations"]
        if row["obligation_id"] in required_machine
    )
    denominator = hashlib.sha256(
        json.dumps(registry["frozen_denominators"], sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    assert denominator == graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    formal = statement["canonical_formal_target"]
    assert formal["declaration_or_expression"] == (
        "AwesomeTheorems.Stage1.THM_M_1063.DonskerInvariancePrinciple"
    )
    assert formal["statement_file_sha256"] == EXPECTED_INPUTS["DonskerTarget.lean"]
    root = next(row for row in registry["obligations"] if row["obligation_id"] == "M1063-ROOT")
    assert root["statement_fingerprint"] == f"lean-expression-sha256:{EXPRESSION_SHA256}"
    closure = graphs["closure_boundary"]
    assert closure["closed_obligations"] == [] and closure["root_closed"] is False
    assert closure["root_machine_debt"] == "M4" and closure["theorem_complete"] is False
    assert closure["remaining_root_cut_set"] == REMAINING_CUT
    assert proof_receipt["accepted"] is False
    assert proof_receipt["supported_obligation_ids"] == []
    assert proof_receipt["result"]["root_kernel_closed"] is False

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|implemented_by|native_decide|run_tac|oracle)\b|"
        r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
        r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
        r"(?:axiom|constant|opaque|unsafe|extern)\b",
        re.MULTILINE,
    )
    for name in ("DonskerTarget.lean", "ObligationTree.lean", "AnchorAudit.lean", "Proof.lean", "Validation.lean"):
        clean = code_without_comments_and_strings((HERE / name).read_text(encoding="utf-8"))
        assert prohibited.search(clean) is None, name
    validation_source = (HERE / "Validation.lean").read_text(encoding="utf-8")
    assert "import Proof" not in validation_source and "import ObligationTree" not in validation_source
    assert "DonskerInvariancePrinciple" not in validation_source

    assert git("rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert git("status", "--porcelain=v1", cwd=MATHLIB) == ""
    assert git("remote", "get-url", "origin", cwd=MATHLIB) == MATHLIB_REMOTE
    assert sha256(MATHLIB / "LICENSE") == MATHLIB_LICENSE_SHA256
    for relative, (blob, source_digest, olean_digest) in MATHLIB_SOURCES.items():
        assert git("rev-parse", f"HEAD:{relative}", cwd=MATHLIB) == blob
        assert sha256(MATHLIB / relative) == source_digest
        olean = MATHLIB / ".lake/build/lib/lean" / Path(relative).with_suffix(".olean")
        assert sha256(olean) == olean_digest

    lean = lean_executable()
    assert LEAN_COMMIT in run([str(lean), "--version"])
    assert sha256(lean) == receipt["environment"]["lean_executable_sha256"]
    assert sha256(Path("/usr/bin/bwrap")) == receipt["environment"]["bwrap_executable_sha256"]
    replay_output = kernel_replay()
    replay_digest = hashlib.sha256(replay_output.encode()).hexdigest()
    assert re.fullmatch(r"[0-9a-f]{64}", replay_digest)
    assert len(replay_output.encode()) > 0

    assert spec["schema_version"] == "stage1-validation-spec/1.0"
    assert spec["item_id"] == ITEM and spec["theorem_id"] == THEOREM
    assert spec["argv"] == ["/usr/bin/python3", "-I", "-B", f"Stage1_Instances/{THEOREM}/check_validation.py"]
    assert spec["network_policy"] == "denied" and spec["expected_exit"] == 0
    assert receipt["recipe"] == spec
    assert receipt["item_id"] == blocker["item_id"] == packet["item_id"] == ITEM
    assert receipt["base_revision"] == blocker["base_revision"] == packet["base_revision"] == BASE_REVISION
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["verdict"] == "blocked" and receipt["release_grade"] is False
    assert receipt["canonical_target"] == formal["declaration_or_expression"]
    assert receipt["canonical_target_expression_sha256"] == EXPRESSION_SHA256
    assert receipt["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert receipt["covered_obligation_ids"] == required_machine
    assert receipt["result"]["root_kernel_closed"] is False
    assert receipt["result"]["validation_complete"] is False
    assert receipt["result"]["hermetic_cold_offline_replay"] == "fail_closed"
    assert receipt["result"]["independent_distinct_runner"] == "fail_closed"
    assert receipt["remaining_root_cut_set"] == REMAINING_CUT
    assert blocker["outcome"] == "validation_packet_self_tested_gates_blocked"
    assert blocker["validation_phase_complete"] is False
    assert blocker["root_closed"] is blocker["audit_complete"] is blocker["theorem_complete"] is False

    assert set(packet) == {"item_id", "changed_paths", "commands", "output_summary", "base_revision", "known_failures", "state"}
    assert packet["state"] == "[_]"
    assert set(packet["changed_paths"]) == set(receipt["changed_paths"]) == CHANGED_PATHS
    assert packet["known_failures"] == receipt["known_failures"]
    status = git("status", "--short", "--untracked-files=all")
    actual = {line[3:] for line in status.splitlines() if line[3:] != "Formalizations/Lean/.lake"}
    assert actual == CHANGED_PATHS, (actual, CHANGED_PATHS)
    for relative in CHANGED_PATHS:
        data = (ROOT / relative).read_bytes()
        assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())

    for line in SUMMARY_LINES:
        print(line)


if __name__ == "__main__":
    main()
