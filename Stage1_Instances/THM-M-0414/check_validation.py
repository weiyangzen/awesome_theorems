#!/usr/bin/env python3
"""Fail-closed narrow validation for S56-M-0414-VALIDATION."""

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
HERE = ROOT / "Stage1_Instances" / "THM-M-0414"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
ITEM = "S56-M-0414-VALIDATION"
THEOREM = "THM-M-0414"
EXPECTED_MATHLIB = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
EXPECTED_MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
EXPECTED_LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
EXPECTED_LEAN_SHA256 = "3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf"
EXPECTED_LAKE_LAUNCHER_SHA256 = "840179e70803ef373c2ec53342d6a45ea7d022533e4145489fc1278b4f716385"
EXPECTED_RESOLVED_LAKE_SHA256 = "a608ff084d7e2af228b92a29d7c2fd083ba0580e46889175ec74a81678c98359"
EXPECTED_PYTHON_SHA256 = "b8d8288faefdd300201f43fcf00f6f539a27218eeed3a3dff5ab10b9c4c99700"
EXPECTED_GIT_SHA256 = "8a48eefa306b9a2a9c3e576784a74ad7485779279e5a46ec43361a1864760e45"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
EXPECTED_RECIPE_ENV = {"LC_ALL": "C", "TZ": "UTC", "PYTHONOPTIMIZE": "0"}
EXPECTED_INPUTS = {
    "Statement.lean": "7fe066774a7105731721a651a959cf67312763e9ed089be248866dc49c9c486d",
    "ObligationTree.lean": "a90129d8ce1293e658ff04e09c689142d1fd04fe2a04729572ad7320c766c413",
    "Proof.lean": "8d462642b07638e85c67710ed20782b9f45d3705b40898ae78223151bc1a8afd",
    "statement.json": "f179056b013a84212e917d8cf4df21c653826c83ccb7f8d9f8e0d766fd64d53c",
    "obligation-registry.json": "441286a90669b8da023fdf1d4167306df19010c5eec1d371ff0ae072329cdfba",
    "typed-graphs.json": "81df7d3a7871a3a6eb2ec15b98f24d9d432501536c6bd7c7f587e3e8f6da8b86",
    "anchor-audit.json": "5a4684932fd4d8ad0a2cef83f94594c8acd0b49e77b876f4e527c459a1a13b57",
    "proof-receipt.json": "cd97c59c827f08a9e26fa288cba685b5949111006b2594c9e0c1cf94770f44da",
    "Validation.lean": "d4a84f52bda0c357660b0ec59434cafec21179482e450879617a3988d8cd0ed5",
    "validation-spec.json": "ea57fe27b8957ba61e48613bf41ebbcd4593706306948c226b4342b05aa38432",
}
EXPECTED_EXTERNAL = {
    "Formalizations/Lean/lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "Formalizations/Lean/lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
EXPECTED_TERMINAL_SOURCES = {
    "Mathlib/RingTheory/DedekindDomain/Ideal/Basic.lean":
        "5bc400f681418676cc6aa134235aeb0373c8165e028fd87672981f3757ebb780",
    "Mathlib/RingTheory/DedekindDomain/Factorization.lean":
        "fe33fa1dfdc3eb884df5fa364757344f9e17183c08828f26b6986ac5d968ad98",
    "LICENSE": "b40930bbcf80744c86c46a12bc9da056641d722716c378f5659b9e555ef833e1",
}
PROVISIONAL_PROOF_IDS = {
    "THM-M-0414-ROOT",
    "THM-M-0414-UFM",
    "THM-M-0414-FINPROD",
}

if sys.flags.optimize:
    raise SystemExit("validation failed: Python optimization disables fail-closed assertions")
for name, expected in EXPECTED_RECIPE_ENV.items():
    if os.environ.get(name) != expected:
        raise SystemExit(f"validation failed: recipe environment requires {name}={expected}")


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict), path
    return value


def run(
    argv: list[str], *, cwd: Path = ROOT, env: dict[str, str] | None = None
) -> str:
    result = subprocess.run(
        argv,
        cwd=cwd,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=180,
        check=False,
    )
    if result.returncode:
        raise SystemExit(
            f"validation failed ({result.returncode}): {argv!r}\n{result.stdout}"
        )
    return result.stdout


def without_comments(source: str) -> str:
    source = re.sub(r"/-.*?-/", "", source, flags=re.DOTALL)
    return re.sub(r"--.*$", "", source, flags=re.MULTILINE)


def reported_axioms(output: str, declaration: str) -> set[str]:
    quoted = re.search(
        re.escape(f"'{declaration}' depends on axioms: [") + r"(.*?)]",
        output,
        re.DOTALL,
    )
    if quoted:
        return {item.strip() for item in quoted.group(1).split(",") if item.strip()}
    short = declaration.rsplit(".", 1)[-1]
    qualified = re.search(
        r"'[^']*" + re.escape(short) + r"' depends on axioms: \[(.*?)]",
        output,
        re.DOTALL,
    )
    if qualified:
        return {item.strip() for item in qualified.group(1).split(",") if item.strip()}
    legacy = re.search(
        re.escape(short) + r" depends on \[(.*?)]", output, re.DOTALL
    )
    if legacy:
        return {item.strip() for item in legacy.group(1).split(",") if item.strip()}
    raise SystemExit(f"validation failed: missing axiom report for {declaration}")


spec = load(HERE / "validation-spec.json")
statement = load(HERE / "statement.json")
registry = load(HERE / "obligation-registry.json")
graphs = load(HERE / "typed-graphs.json")
anchor = load(HERE / "anchor-audit.json")
proof_receipt = load(HERE / "proof-receipt.json")
execution = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")

assert spec["item_id"] == ITEM and spec["theorem_id"] == THEOREM
assert len(spec["recipes"]) == 1
recipe = spec["recipes"][0]
assert recipe["cwd"] == "." and isinstance(recipe["argv"], list)
assert recipe["network_policy"] == "denied" and recipe["expected_exit"] == 0
assert recipe["env_allowlist"] == EXPECTED_RECIPE_ENV
assert set(recipe["covered_obligation_ids"]) == {
    row["obligation_id"] for row in registry["obligations"]
}

validation_item = next(row for row in execution["items"] if row["id"] == ITEM)
proof_item = next(row for row in execution["items"] if row["id"] == "S56-M-0414-PROOF")
assert validation_item["phase"] == "validation" and validation_item["state"] in {"[ ]", "[_]"}
assert validation_item["depends_on"] == [proof_item["id"]]
assert proof_item["state"] == "[_]", "proof prerequisite is not provisionally self-tested"
assert validation_item["owned_paths"] == [f"Stage1_Instances/{THEOREM}"]

for name, expected in EXPECTED_INPUTS.items():
    assert digest(HERE / name) == expected, f"frozen input hash mismatch: {name}"
for name, expected in EXPECTED_EXTERNAL.items():
    assert digest(ROOT / name) == expected, f"external input hash mismatch: {name}"

assert statement["canonical_formal_target"]["statement_file_sha256"] == digest(
    HERE / "Statement.lean"
)
assert registry["canonical_root"] == "THM-M-0414-ROOT"
assert set(registry["eligibility_denominator"]["root_relevant_machine_ids"]) == {
    row["obligation_id"] for row in registry["obligations"]
}
assert set(graphs["nodes"]) == {
    row["obligation_id"] for row in registry["obligations"]
}
assert proof_receipt["item_id"] == "S56-M-0414-PROOF"
assert proof_receipt["proof_body"]["source_sha256"] == digest(HERE / "Proof.lean")
assert proof_receipt["inputs"]["statement_sha256"] == digest(HERE / "Statement.lean")
assert proof_receipt["inputs"]["obligation_registry_sha256"] == digest(
    HERE / "obligation-registry.json"
)
assert set(proof_receipt["closed_obligation_ids"]) == PROVISIONAL_PROOF_IDS
assert proof_receipt["result"]["root_closed"] is True
assert proof_receipt["result"]["theorem_complete"] is False

prohibited = re.compile(
    r"\b(?:sorry|admit|sorryAx|implemented_by|native_decide|extern|opaque)\b"
    r"|^[ \t]*(?:axiom|unsafe|constant)\b",
    re.MULTILINE,
)
for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
    assert prohibited.search(without_comments((HERE / name).read_text(encoding="utf-8"))) is None

validation_source = (HERE / "Validation.lean").read_text(encoding="utf-8")
assert "import Proof" not in validation_source
assert "import ObligationTree" not in validation_source
assert "idealUniqueFactorizationTarget_proof" not in validation_source
assert "Ideal.uniqueFactorizationMonoid" in validation_source
assert "Ideal.finprod_heightOneSpectrum_factorization" in validation_source

manifest = load(LEAN_ROOT / "lake-manifest.json")
mathlib_record = next(p for p in manifest["packages"] if p["name"] == "mathlib")
assert mathlib_record["rev"] == EXPECTED_MATHLIB
mathlib = (LEAN_ROOT / ".lake" / "packages" / "mathlib").resolve()
assert mathlib.is_dir(), "pinned mathlib artifact is unavailable"
assert run(["git", "rev-parse", "HEAD"], cwd=mathlib).strip() == EXPECTED_MATHLIB
assert run(["git", "rev-parse", "HEAD^{tree}"], cwd=mathlib).strip() == EXPECTED_MATHLIB_TREE
assert run(["git", "status", "--short"], cwd=mathlib) == ""
assert run(["git", "remote", "get-url", "origin"], cwd=mathlib).strip() == (
    "https://github.com/leanprover-community/mathlib4.git"
)
for name, expected in EXPECTED_TERMINAL_SOURCES.items():
    assert digest(mathlib / name) == expected, f"pinned terminal source mismatch: {name}"

basic_source = (mathlib / "Mathlib/RingTheory/DedekindDomain/Ideal/Basic.lean").read_text(
    encoding="utf-8"
)
factorization_source = (
    mathlib / "Mathlib/RingTheory/DedekindDomain/Factorization.lean"
).read_text(encoding="utf-8")
assert "instance Ideal.uniqueFactorizationMonoid" in basic_source
assert "theorem finprod_heightOneSpectrum_factorization {I : Ideal R}" in factorization_source
for candidate in anchor["candidates"][:2]:
    assert candidate["revision"] == EXPECTED_MATHLIB
    assert candidate["tree"] == EXPECTED_MATHLIB_TREE
    assert candidate["file_sha256"] == digest(mathlib / candidate["file"])
    assert candidate["license_sha256"] == digest(mathlib / "LICENSE")

version = run(["lake", "env", "lean", "--version"], cwd=LEAN_ROOT)
assert "version 4.29.0" in version and EXPECTED_LEAN_COMMIT in version
lean_executable = Path(run(["lake", "env", "which", "lean"], cwd=LEAN_ROOT).strip())
resolved_lake = Path(run(["lake", "env", "which", "lake"], cwd=LEAN_ROOT).strip())
lake_launcher = Path(shutil.which("lake") or "")
git_executable = Path(shutil.which("git") or "")
assert digest(lean_executable) == EXPECTED_LEAN_SHA256
assert digest(resolved_lake) == EXPECTED_RESOLVED_LAKE_SHA256
assert digest(lake_launcher) == EXPECTED_LAKE_LAUNCHER_SHA256
assert digest(Path(sys.executable)) == EXPECTED_PYTHON_SHA256
assert digest(git_executable) == EXPECTED_GIT_SHA256

with tempfile.TemporaryDirectory(prefix="m0414-validation-", dir=LEAN_ROOT) as tmp_name:
    tmp = Path(tmp_name)
    for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
        (tmp / name).write_bytes((HERE / name).read_bytes())
    run(
        [
            "lake",
            "env",
            "lean",
            "-o",
            str(tmp / "Statement.olean"),
            str(tmp / "Statement.lean"),
        ],
        cwd=LEAN_ROOT,
    )
    lean_path = run(["lake", "env", "printenv", "LEAN_PATH"], cwd=LEAN_ROOT).strip()
    module_env = os.environ.copy()
    module_env.update(EXPECTED_RECIPE_ENV)
    module_env["LEAN_PATH"] = f"{tmp}:{lean_path}"
    outputs = {}
    for name in ("ObligationTree.lean", "Proof.lean", "Validation.lean"):
        outputs[name] = run(
            ["lake", "env", "lean", str(tmp / name)], cwd=LEAN_ROOT, env=module_env
        )

proof_output = outputs["Proof.lean"]
validation_output = outputs["Validation.lean"]
assert "components_compose" in outputs["ObligationTree.lean"]
assert (
    reported_axioms(outputs["ObligationTree.lean"], "components_compose")
    == EXPECTED_AXIOMS
)
for declaration in (
    "idealUniqueFactorizationMonoid_proof",
    "idealFiniteProductFactorization_proof",
    "idealUniqueFactorizationTarget_proof",
):
    assert reported_axioms(proof_output, declaration) == EXPECTED_AXIOMS
assert reported_axioms(validation_output, "independentExactRoot") == EXPECTED_AXIOMS
assert reported_axioms(validation_output, "Ideal.uniqueFactorizationMonoid") == EXPECTED_AXIOMS
assert (
    reported_axioms(validation_output, "Ideal.finprod_heightOneSpectrum_factorization")
    == EXPECTED_AXIOMS
)
assert "sorryAx" not in "\n".join(outputs.values())

# Validation preserves the fail-closed authority boundary rather than rewriting older graph state.
root_trust_edge = next(
    edge
    for edge in graphs["trust_graph"]["edges"]
    if edge["from"] == "THM-M-0414-ROOT" and edge["to"] == "THM-M-0414-TRUST"
)
assert root_trust_edge["status"] == "open_release_gate"
assert graphs["status_boundary"].endswith("theorem completion.")
assert registry["audit_complete"] is False and registry["theorem_complete"] is False

print("PASS THM-M-0414 narrow validation")
print("kernel: exact statement, conditional composition, proof root, and differential root elaborated")
print("trust: checked local and terminal declarations report only propext, Classical.choice, Quot.sound")
print("provenance: frozen proof hashes and clean pinned mathlib revision/tree/source/license agree")
print("blocked: THM-M-0414-TRUST lacks complete transitive TCB and compiled-import closure")
print("blocked: shared warm .lake is not cold hermetic replay; same worker is not independent verification")
