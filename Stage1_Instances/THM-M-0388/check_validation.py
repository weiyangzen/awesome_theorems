#!/usr/bin/env python3
"""Semantic validation-phase verifier for S56-M-0388-VALIDATION."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0388"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM_ID = "S56-M-0388-VALIDATION"
THEOREM_ID = "THM-M-0388"
BASE_REVISION = "c5037228977a81948bbd6119e1728b4b65b9924e"
BASE_TREE = "78b2627e717156dffe240bea12d14205af667d2a"
GRAPH_SHA256 = "fb17743ff737fd3c528467b6f992a7235a36f0842b528e57de3e4c6d660d3518"
CONTEXT_SHA256 = "068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c"
TOOLCHAIN = "leanprover/lean4:v4.29.0"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
PELL_SOURCE_SHA256 = "ac09716ec72e9d69cc505b7505473a1734408c36178f361155543952aafe86cb"
PELL_OLEAN_SHA256 = "16ae0ab178fa02fd817870da031f064bf16804dd96fbe687723acfe461e63867"
TOOLCHAIN_SHA256 = "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2"
MANIFEST_SHA256 = "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81"
LEAN_SHA256 = "3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf"
LAKE_SHA256 = "a608ff084d7e2af228b92a29d7c2fd083ba0580e46889175ec74a81678c98359"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
EXPECTED_LOCAL_INPUTS = {
    "Proof.lean": "b602b0db2a7d022e5c3f1f8555d82dea500b42bd5f5a0e81ea5df4d4279a49a4",
    "Statement.lean": "bdcd52df2c25d1d86d9dd5fa487abe19ff78d68b3c6ff373b99ee1f3c5554782",
    "Validation.lean": "a68046f6ce19d568a3ec7f3ca6509c50747b952b61741da56e131443a2552ff2",
    "obligation-registry.json": "46fe5c6ecce251c6a0d866112081bbc7483046d1d3e83f15fe3886e4453786f9",
    "typed-graphs.json": "f7c0ea3a2845e4fe9a567fa550e48d256e209323efffa67928a562c689bf995c",
    "proof-receipt.json": "11881f661cc5b72d5c4e573a07c14fc8a3296f8761f103b144d182cbd8cb0f96",
}
EXPECTED_OBLIGATIONS = {
    "M0388-ROOT",
    "M0388-S-PREDICATE",
    "M0388-X-PELL",
    "M0388-N-IRRATIONAL",
    "M0388-C-APPROX",
    "M0388-B-NORM",
    "M0388-C-PAIR",
    "M0388-C-QUOTIENT",
    "M0388-L-EQUATION",
    "M0388-L-NONZERO",
    "M0388-X-TRUST",
}
PROHIBITED = re.compile(
    r"\b(?:sorry|admit|sorryAx)\b|^[ \t]*(?:axiom|unsafe)\b", re.MULTILINE
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path: Path) -> dict:
    def reject_duplicates(pairs: list[tuple[str, object]]) -> dict:
        value: dict[str, object] = {}
        for key, child in pairs:
            if key in value:
                raise ValueError(f"duplicate key {key!r} in {path}")
            value[key] = child
        return value

    value = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicates)
    if not isinstance(value, dict):
        raise ValueError(f"{path} is not a JSON object")
    return value


def run(argv: list[str], *, cwd: Path, env: dict[str, str] | None = None) -> str:
    result = subprocess.run(
        argv,
        cwd=cwd,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=120,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(f"command failed ({result.returncode}): {argv!r}\n{result.stdout}")
    return result.stdout


def git(*argv: str, cwd: Path = ROOT) -> str:
    return run(["/usr/bin/git", *argv], cwd=cwd).strip()


def code_without_comments(source: str) -> str:
    """Strip nested Lean comments, line comments, and string contents."""
    output: list[str] = []
    index = 0
    depth = 0
    in_string = False
    while index < len(source):
        if depth:
            if source.startswith("/-", index):
                depth += 1
                index += 2
            elif source.startswith("-/", index):
                depth -= 1
                index += 2
            else:
                index += 1
        elif in_string:
            if source[index] == "\\" and index + 1 < len(source):
                index += 2
            elif source[index] == '"':
                in_string = False
                output.append('"')
                index += 1
            else:
                index += 1
        elif source.startswith("/-", index):
            depth = 1
            index += 2
        elif source.startswith("--", index):
            newline = source.find("\n", index)
            index = len(source) if newline < 0 else newline
        elif source[index] == '"':
            in_string = True
            output.append('"')
            index += 1
        else:
            output.append(source[index])
            index += 1
    if depth or in_string:
        raise ValueError("unterminated Lean comment or string")
    return "".join(output)


def printed_axioms(output: str, declaration: str) -> set[str]:
    short = declaration.rsplit(".", 1)[-1]
    match = re.search(
        rf"'[^']*{re.escape(short)}' depends on axioms:\s*\[(.*?)\]",
        output,
        flags=re.DOTALL,
    )
    if match is None:
        no_axiom = re.search(
            rf"'[^']*{re.escape(short)}' does not depend on any axioms", output
        )
        if no_axiom is None:
            raise ValueError(f"missing axiom report for {declaration}")
        return set()
    return {
        value.strip()
        for value in match.group(1).replace("\n", "").split(",")
        if value.strip()
    }


def lean_replay() -> tuple[str, str]:
    lean = Path.home() / ".elan" / "toolchains" / "leanprover--lean4---v4.29.0" / "bin" / "lean"
    lake = lean.with_name("lake")
    if sha256(lean) != LEAN_SHA256 or sha256(lake) != LAKE_SHA256:
        raise ValueError("pinned Lean/Lake executable digest mismatch")
    if LEAN_COMMIT not in run([str(lean), "--version"], cwd=LEAN_ROOT):
        raise ValueError("pinned Lean executable identity mismatch")

    with tempfile.TemporaryDirectory(prefix="m0388-validation-", dir="/tmp") as raw:
        scratch = Path(raw)
        for name in ("Proof.lean", "Validation.lean"):
            (scratch / name).write_bytes((HERE / name).read_bytes())
        fixed_env = {
            **os.environ,
            "ELAN_TOOLCHAIN": TOOLCHAIN,
            "LANG": "C.UTF-8",
            "LC_ALL": "C.UTF-8",
            "TZ": "UTC",
            "LEAN_NUM_THREADS": "1",
        }
        proof_output = run(
            [str(lake), "env", "lean", str(scratch / "Proof.lean")],
            cwd=LEAN_ROOT,
            env=fixed_env,
        )
        validation_output = run(
            [str(lake), "env", "lean", str(scratch / "Validation.lean")],
            cwd=LEAN_ROOT,
            env=fixed_env,
        )
    return proof_output, validation_output


def verify() -> None:
    if git("rev-parse", "HEAD") != BASE_REVISION or git("rev-parse", "HEAD^{tree}") != BASE_TREE:
        raise ValueError("worker base revision or tree drifted")
    if sha256(ROOT / "Docs" / "Stage1_Theorem_DAG_v2.json") != GRAPH_SHA256:
        raise ValueError("theorem DAG digest drifted")
    if sha256(LEAN_ROOT / "lean-toolchain") != TOOLCHAIN_SHA256:
        raise ValueError("Lean toolchain file drifted")
    if sha256(LEAN_ROOT / "lake-manifest.json") != MANIFEST_SHA256:
        raise ValueError("Lake manifest drifted")
    for name, expected in EXPECTED_LOCAL_INPUTS.items():
        if sha256(HERE / name) != expected:
            raise ValueError(f"owned input {name} drifted")

    ledger = load(HERE / "dependency-reuse-ledger.json")
    if ledger != {
        "schema_version": "stage1-dependency-reuse-ledger/1.1",
        "consumer_theorem_id": THEOREM_ID,
        "observed_theorem_dag_sha256": GRAPH_SHA256,
        "dependency_context_sha256": CONTEXT_SHA256,
        "repository_revision": BASE_REVISION,
        "direct_parent_ids": [],
        "transitive_ancestor_ids": [],
        "hard_edge_ids": [],
        "reuse_hint_ids": [],
        "shared_group_ids": [],
        "inspections": [],
        "reuse_decisions": [],
        "unresolved_compatibility_obligations": [],
    }:
        raise ValueError("empty dependency/reuse context is incomplete or stale")

    proof_receipt = load(HERE / "proof-receipt.json")
    expected_receipt_inputs = {
        "proof_sha256": EXPECTED_LOCAL_INPUTS["Proof.lean"],
        "statement_sha256": EXPECTED_LOCAL_INPUTS["Statement.lean"],
        "obligation_registry_sha256": EXPECTED_LOCAL_INPUTS["obligation-registry.json"],
    }
    if proof_receipt.get("inputs") != expected_receipt_inputs:
        raise ValueError("proof receipt input hashes are stale")
    if proof_receipt.get("proof_body", {}).get("dependency_revision") != MATHLIB_REVISION:
        raise ValueError("proof receipt dependency revision drifted")

    manifest = load(LEAN_ROOT / "lake-manifest.json")
    mathlib_entry = next(
        (package for package in manifest["packages"] if package.get("name") == "mathlib"), None
    )
    if mathlib_entry is None or mathlib_entry.get("rev") != MATHLIB_REVISION:
        raise ValueError("manifest mathlib pin drifted")
    if git("rev-parse", "HEAD", cwd=MATHLIB) != MATHLIB_REVISION:
        raise ValueError("checked-out mathlib revision drifted")
    if git("rev-parse", "HEAD^{tree}", cwd=MATHLIB) != MATHLIB_TREE:
        raise ValueError("checked-out mathlib tree drifted")
    if git("status", "--porcelain=v1", cwd=MATHLIB) != "":
        raise ValueError("checked-out mathlib worktree is dirty")
    pell_source = MATHLIB / "Mathlib" / "NumberTheory" / "Pell.lean"
    pell_olean = MATHLIB / ".lake" / "build" / "lib" / "lean" / "Mathlib" / "NumberTheory" / "Pell.olean"
    if sha256(pell_source) != PELL_SOURCE_SHA256 or sha256(pell_olean) != PELL_OLEAN_SHA256:
        raise ValueError("Pell terminal source or compiled object digest drifted")

    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    registry_ids = [row["obligation_id"] for row in registry["obligations"]]
    if len(registry_ids) != len(set(registry_ids)) or set(registry_ids) != EXPECTED_OBLIGATIONS:
        raise ValueError("frozen obligation registry identity drifted")
    if set(graphs.get("nodes", [])) != EXPECTED_OBLIGATIONS:
        raise ValueError("typed graph and registry node sets disagree")
    if set(proof_receipt.get("canonical_obligation_ids", [])) != EXPECTED_OBLIGATIONS:
        raise ValueError("proof receipt does not cover the frozen obligation IDs")

    for name in ("Proof.lean", "Validation.lean"):
        source_code = code_without_comments((HERE / name).read_text(encoding="utf-8"))
        if PROHIBITED.search(source_code):
            raise ValueError(f"prohibited construct found in {name}")
    pell_body = pell_source.read_text(encoding="utf-8")
    declaration = re.search(
        r"theorem exists_of_not_isSquare\b.*? := by(?P<body>.*?)(?=\n/--|\nend Existence)",
        pell_body,
        flags=re.DOTALL,
    )
    if declaration is None or PROHIBITED.search(code_without_comments(declaration.group("body"))):
        raise ValueError("terminal Pell declaration body is missing or contains a placeholder")

    proof_output, validation_output = lean_replay()
    if printed_axioms(proof_output, "not_isSquare_of_isNonsquareInteger") != set():
        raise ValueError("proof predicate transport unexpectedly depends on axioms")
    if printed_axioms(validation_output, "independentPredicateTransport") != set():
        raise ValueError("validation predicate transport unexpectedly depends on axioms")
    for output, declaration_name in (
        (proof_output, "Pell.exists_of_not_isSquare"),
        (proof_output, "pellEquationStatement"),
        (validation_output, "Pell.exists_of_not_isSquare"),
        (validation_output, "independentRoot"),
    ):
        if printed_axioms(output, declaration_name) != EXPECTED_AXIOMS:
            raise ValueError(f"unexpected axiom profile for {declaration_name}")


def semantic_result(*, passed: bool, message: str) -> dict:
    return {
        "schema_version": "stage1-validator-semantic-result/1.0",
        "item_id": ITEM_ID,
        "theorem_id": THEOREM_ID,
        "phase": "validation",
        "status": "passed" if passed else "failed",
        "verdict": "phase_accepted" if passed else "repair_required",
        "phase_accepted": passed,
        "audit_complete": False,
        "theorem_complete": False,
        "phase_predicate_proven": passed,
        "first_failed_gate": None if passed else "V02-RECIPES",
        "open_obligations": 0 if passed else 1,
        "stale_inputs": [],
        "blocked": False,
        "message": message,
    }


def main() -> None:
    try:
        verify()
    except Exception as exc:
        result = semantic_result(passed=False, message=f"validation replay failed: {exc}")
    else:
        result = semantic_result(
            passed=True,
            message=(
                "Pinned warm-cache kernel, selected trust/provenance, empty dependency context, "
                "and same-workspace differential validation gates passed."
            ),
        )
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))
    if not result["phase_accepted"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
