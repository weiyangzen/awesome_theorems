#!/usr/bin/env python3
"""Fail-closed narrow validator for S56-M-1016-VALIDATION."""

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
import time


ROOT = Path(__file__).resolve().parents[2]
RECIPE_STARTED = time.monotonic()
RECIPE_TIMEOUT_SECONDS = 600
HERE = ROOT / "Stage1_Instances" / "THM-M-1016"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
EXPECTED_MATHLIB = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
EXPECTED_MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
EXPECTED_HASHES = {
    "Statement.lean": "75d7800ccedfe5499e997adb68acbb9f7bef828815cdf2802b4735babaa5f011",
    "ObligationTree.lean": "4e740dd14d4efa9440ea7bb48803b9cd664e41e1dbe2eb7422b01eb6e85694cd",
    "Proof.lean": "64af1c77d3819ed735f7953b8ac62c2b43e77c4acc82f1af2fae839499393bac",
    "statement.json": "d13f68e5c331537b1f701ddb6aeac63329a2194b04ae47e4b4ca695b55b13c81",
    "anchor-audit.json": "0fc50ec020adcd90b00e12e75e083bf9f785a02df13f3ff22480bb9da4d4a829",
    "obligation-registry.json": "5f0efabd00ce7236b0319b8800f38230404495fc01481d6c23d993d651d6a8cc",
    "typed-graphs.json": "c5a024eac21553cb02848024d7e7957ca80a2c095e920e4578313fc5677d1f68",
    "proof-receipt.json": "05045132b311970ba0d7eb9cd96fe36e3e072c5cfb2fd277cad3d96bc1a3409f",
}
TERMINAL_HASHES = {
    "Mathlib/MeasureTheory/Function/ConvergenceInDistribution.lean":
        "dd3167a8ec5186a193d04992f31b33599c06f5209c29aed64f1f597cc30d843a",
    ".lake/build/lib/lean/Mathlib/MeasureTheory/Function/ConvergenceInDistribution.olean":
        "f6ddef21cce1667d6a6b4721c2643f0b9d2c7ed3f1f82b120767b85c92e66b89",
    "Mathlib/Analysis/Calculus/FDeriv/Basic.lean":
        "3e9a21ea0c7ad87b2711fcdc6f8746a54e28b59cdfdc0544a5bc35301a49d31e",
    ".lake/build/lib/lean/Mathlib/Analysis/Calculus/FDeriv/Basic.olean":
        "e7ae50db963c7e5090dfce3ba021c496f30e6d9830e347a0e1c0dda27c86580d",
    "Mathlib/MeasureTheory/Measure/TightNormed.lean":
        "a280a9861fbc6c92fb4eb7d6d60a53f31b3abf5ef95f3ef000cba48b72e80f0f",
    ".lake/build/lib/lean/Mathlib/MeasureTheory/Measure/TightNormed.olean":
        "634e17d262bc9d7c9558d7780f9abcce89303631ea6b467b91a85cf095e9663a",
}


def fail(message: str) -> None:
    print(f"validation: FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def require(value: bool, message: str) -> None:
    if not value:
        fail(message)


def digest(path: Path) -> str:
    if not path.is_file():
        fail(f"required artifact is missing: {path}")
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(
    argv: list[str],
    *,
    cwd: Path,
    env: dict[str, str] | None = None,
    timeout: int | None = None,
) -> str:
    remaining = RECIPE_TIMEOUT_SECONDS - (time.monotonic() - RECIPE_STARTED)
    require(remaining > 0, "whole validation recipe timed out")
    effective_timeout = remaining if timeout is None else min(timeout, remaining)
    try:
        result = subprocess.run(
            argv,
            cwd=cwd,
            env=env,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=effective_timeout,
            check=False,
        )
    except subprocess.TimeoutExpired as error:
        fail(f"command timed out: {argv!r}\n{error.stdout or ''}")
    if result.returncode:
        fail(f"command exited {result.returncode}: {argv!r}\n{result.stdout}")
    return result.stdout


def code_without_comments(source: str) -> str:
    source = re.sub(r"/-.*?-/", "", source, flags=re.DOTALL)
    return re.sub(r"--.*$", "", source, flags=re.MULTILINE)


def resolved_executable(name: str) -> Path:
    executable = shutil.which(name)
    require(executable is not None, f"required executable is unavailable: {name}")
    return Path(executable).resolve()


def printed_axioms(output: str, declaration: str) -> set[str]:
    matches = re.findall(
        rf"'[^']*{re.escape(declaration)}' depends on axioms:\s*\[(.*?)\]",
        output,
        re.DOTALL,
    )
    require(len(matches) == 1, f"expected one axiom report for {declaration}")
    return {part.strip() for part in matches[0].split(",") if part.strip()}


spec = json.loads((HERE / "validation-spec.json").read_text(encoding="utf-8"))
statement = json.loads((HERE / "statement.json").read_text(encoding="utf-8"))
anchor = json.loads((HERE / "anchor-audit.json").read_text(encoding="utf-8"))
registry = json.loads((HERE / "obligation-registry.json").read_text(encoding="utf-8"))
graphs = json.loads((HERE / "typed-graphs.json").read_text(encoding="utf-8"))
proof_receipt = json.loads((HERE / "proof-receipt.json").read_text(encoding="utf-8"))
manifest = json.loads((LEAN_ROOT / "lake-manifest.json").read_text(encoding="utf-8"))

require(spec["item_id"] == "S56-M-1016-VALIDATION", "wrong validation item")
require(spec["theorem_id"] == "THM-M-1016", "wrong theorem")
require(
    spec["argv"] == ["/usr/bin/python3", "Stage1_Instances/THM-M-1016/check_validation.py"],
    "recipe argv drifted",
)
require(spec["network_policy"] == "denied", "validation recipe must deny network use")
require(
    "read-only host root" in spec["network_enforcement"]
    and "isolated network namespace" in spec["network_enforcement"],
    "network enforcement description drifted",
)
require(spec["expected_exit"] == 0 and spec["timeout_seconds"] == 600, "recipe bounds drifted")
require(
    set(spec["covered_obligation_ids"]) == set(registry["frozen_denominators"]["required_machine"]),
    "recipe does not cover the frozen required-machine denominator",
)
require(
    set(spec["obligation_evidence_map"]) == set(spec["covered_obligation_ids"]),
    "obligation evidence map does not cover the declared validation scope",
)
require(
    spec["obligation_evidence_map"]["M1016-S-FOUNDATION"]["worker_result"]
    == "observed_axioms_only_profile_acceptance_open",
    "foundation obligation must remain explicitly open",
)
require(
    spec["env_allowlist"] == {"LC_CTYPE": "C.UTF-8"},
    "top-level recipe environment allowlist drifted",
)
require(
    set(os.environ) == {"LC_CTYPE"}
    and os.environ["LC_CTYPE"] in {"C.UTF-8", "C.utf8"},
    "runner environment must be cleared before invoking the validation recipe",
)

for name, expected in EXPECTED_HASHES.items():
    require(digest(HERE / name) == expected, f"frozen input hash mismatch: {name}")
require(
    statement["canonical_formal_target"]["statement_file_sha256"] == digest(HERE / "Statement.lean"),
    "statement record does not bind Statement.lean",
)
require(
    statement["canonical_formal_target"]["elaborated_expression_sha256"]
    == "9cdb0281811565d62d5b8a7cc2933f27facd49e39aff10c29fe1d7702797dbee",
    "canonical expression fingerprint drifted",
)
require(
    registry["frozen_against_statement_sha256"] == digest(HERE / "Statement.lean"),
    "obligation registry is not frozen against the current statement",
)
require(
    registry["frozen_against_anchor_audit_sha256"] == digest(HERE / "anchor-audit.json"),
    "obligation registry is not frozen against the current anchor audit",
)
require(
    graphs["registry_denominator_sha256"] == registry["denominator_sha256"],
    "typed graph and registry denominators disagree",
)
require(registry["root_obligation_id"] == "M1016-ROOT", "canonical root drifted")
require(
    proof_receipt["proof_body"]["source_sha256"] == digest(HERE / "Proof.lean"),
    "proof receipt does not bind Proof.lean",
)
require(proof_receipt["result"]["root_closed"] is True, "proof receipt does not claim root closure")
require(
    set(proof_receipt["closed_obligation_ids"])
    == set(registry["frozen_denominators"]["required_machine"]) - {
        "M1016-S-DEFINITIONS", "M1016-S-BOUNDARIES", "M1016-S-FOUNDATION"
    },
    "proof receipt closed-obligation route drifted",
)
require(
    set(proof_receipt["exact_declarations"]) <= set(spec["covered_declarations"]),
    "validation spec omits a proof-receipt declaration",
)

prohibited = re.compile(
    r"\b(?:sorry|admit|sorryAx|implemented_by)\b|^[ \t]*(?:axiom|unsafe)\b",
    re.MULTILINE,
)
for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
    source = code_without_comments((HERE / name).read_text(encoding="utf-8"))
    require(prohibited.search(source) is None, f"prohibited mechanism in {name}")

require(
    digest(LEAN_ROOT / "lean-toolchain")
    == "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "Lean toolchain file drifted",
)
require(
    digest(LEAN_ROOT / "lake-manifest.json")
    == "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
    "Lake manifest drifted",
)
mathlib_entry = next((row for row in manifest["packages"] if row["name"] == "mathlib"), None)
require(mathlib_entry is not None, "mathlib is absent from lake-manifest.json")
require(
    mathlib_entry["rev"] == mathlib_entry["inputRev"] == EXPECTED_MATHLIB,
    "manifest mathlib pin drifted",
)
mathlib = (LEAN_ROOT / ".lake" / "packages" / "mathlib").resolve()
require(mathlib.is_dir(), "canonical pinned mathlib artifact is unavailable")
require(run(["git", "rev-parse", "HEAD"], cwd=mathlib).strip() == EXPECTED_MATHLIB,
        "checked-out mathlib revision differs from the manifest")
require(run(["git", "rev-parse", "HEAD^{tree}"], cwd=mathlib).strip() == EXPECTED_MATHLIB_TREE,
        "checked-out mathlib tree drifted")
require(run(["git", "status", "--short"], cwd=mathlib) == "", "pinned mathlib source is dirty")
for relative, expected in TERMINAL_HASHES.items():
    require(digest(mathlib / relative) == expected, f"terminal source/olean hash mismatch: {relative}")
for relative, expected in anchor["candidates"][0]["source_sha256"].items():
    require(digest(mathlib / relative) == expected, f"anchor provenance drifted: {relative}")

lean_path = run(["lake", "env", "printenv", "LEAN_PATH"], cwd=LEAN_ROOT).strip()
lean = run(["lake", "env", "which", "lean"], cwd=LEAN_ROOT).strip()
lake = run(["lake", "env", "which", "lake"], cwd=LEAN_ROOT).strip()
require(
    digest(Path(lean)) == "3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf",
    "Lean executable digest drifted",
)
require(
    digest(Path(lake)) == "a608ff084d7e2af228b92a29d7c2fd083ba0580e46889175ec74a81678c98359",
    "Lake executable digest drifted",
)
bwrap = shutil.which("bwrap")
require(bwrap is not None, "bubblewrap is required for network-isolated Lean replay")
require(
    digest(Path(os.path.realpath(bwrap)))
    == "0abea81db798ebf6b4742ac0664802d97521547a353c2a0dbdc21d76cbbfd2c0",
    "bubblewrap executable digest drifted",
)
require(
    digest(Path(sys.executable).resolve())
    == "b8d8288faefdd300201f43fcf00f6f539a27218eeed3a3dff5ab10b9c4c99700",
    "Python executable digest drifted",
)
require(
    digest(resolved_executable("git"))
    == "8a48eefa306b9a2a9c3e576784a74ad7485779279e5a46ec43361a1864760e45",
    "Git executable digest drifted",
)
outputs: dict[str, str] = {}
with tempfile.TemporaryDirectory(prefix="m1016-validation-") as tmp_name:
    tmp = Path(tmp_name)
    for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
        (tmp / name).write_bytes((HERE / name).read_bytes())
    sandbox = [
        bwrap,
        "--ro-bind", "/", "/",
        "--bind", str(tmp), str(tmp),
        "--dev", "/dev",
        "--proc", "/proc",
        "--unshare-net",
        "--die-with-parent",
        "--clearenv",
        "--setenv", "LEAN_NUM_THREADS", "1",
        "--setenv", "LANG", "C.UTF-8",
        "--setenv", "LC_ALL", "C.UTF-8",
        "--setenv", "TZ", "UTC",
        "--chdir", str(tmp),
    ]
    outputs["Statement.lean"] = run(
        sandbox + ["--setenv", "LEAN_PATH", lean_path, lean, "--trust=0",
                   "-o", "Statement.olean", "Statement.lean"],
        cwd=ROOT,
    )
    local_lean_path = f"{tmp}:{lean_path}"
    outputs["ObligationTree.lean"] = run(
        sandbox + ["--setenv", "LEAN_PATH", local_lean_path, lean,
                   "--trust=0", "-o", "ObligationTree.olean", "ObligationTree.lean"],
        cwd=ROOT,
    )
    outputs["Proof.lean"] = run(
        sandbox + ["--setenv", "LEAN_PATH", local_lean_path, lean,
                   "--trust=0", "-o", "Proof.olean", "Proof.lean"],
        cwd=ROOT,
    )
    outputs["Validation.lean"] = run(
        sandbox + ["--setenv", "LEAN_PATH", local_lean_path, lean,
                   "--trust=0", "Validation.lean"],
        cwd=ROOT,
    )

require(
    printed_axioms(outputs["ObligationTree.lean"], "deltaMethod_of_remainder") == EXPECTED_AXIOMS,
    "unexpected axiom closure for the composition certificate",
)
for declaration in (
    "normalizedLawsTight",
    "normalizedTail",
    "inputConvergesInMeasure",
    "scaledRemainderTendstoInMeasure",
    "transformedAEMeasurable",
    "deltaMethod",
    "statementProof",
):
    require(
        printed_axioms(outputs["Proof.lean"], declaration) == EXPECTED_AXIOMS,
        f"unexpected axiom closure for {declaration}",
    )
require(
    printed_axioms(outputs["Validation.lean"], "exactRootProbe") == EXPECTED_AXIOMS,
    "unexpected axiom closure for exactRootProbe",
)
require(
    outputs["Validation.lean"].count("Declarations are sorry-free!") == 9,
    "expected nine elaborator-aware no-sorry reports",
)
require(
    "sorryAx" not in "".join(outputs.values()),
    "Lean output reports a placeholder axiom",
)

# The graph is an immutable pre-proof observation; validation records staleness instead of rewriting it.
closure = graphs["closure_boundary"]
require(closure["root_closed"] is False, "expected the frozen graph to remain pre-proof")
require(closure["theorem_complete"] is False, "frozen graph must not claim theorem completion")
require(
    closure["remaining_root_cut_set"] == ["M1016-T-REMAINDER"],
    "unexpected frozen root cut set",
)

print("validation: PASS: exact statement, composition, proof root, and exact-type probe kernel-replayed from fresh temporary sources with network isolated and dependency sources read-only")
print("validation: PASS: all nine checked declarations report exactly propext, Classical.choice, and Quot.sound")
print("validation: PASS: elaborator-aware no-sorry checks, source hygiene, frozen hashes, denominator, proof receipt, dependency pin, terminal provenance, and clean mathlib checks passed")
print("validation: STALE: frozen typed graph predates proof closure and awaits master reconciliation")
print("validation: BLOCKED release-only: the read-only shared warm .lake is not a cold empty-cache replay and the foundation/TCB profile is not release-closed")
print("validation: BLOCKED release-only: exact-type replay in this worker is not a distinct independently provisioned verifier")
print(f"validation spec sha256: {digest(HERE / 'validation-spec.json')}")
print(f"validation probe sha256: {digest(HERE / 'Validation.lean')}")
print(f"validator sha256: {digest(HERE / 'check_validation.py')}")
