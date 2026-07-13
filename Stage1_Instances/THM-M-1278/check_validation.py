#!/usr/bin/env python3
"""Fail-closed narrow validation for S56-M-1278-VALIDATION."""

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
HERE = ROOT / "Stage1_Instances" / "THM-M-1278"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
ITEM = "S56-M-1278-VALIDATION"
THEOREM = "THM-M-1278"
EXPECTED_MATHLIB = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
EXPECTED_MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
EXPECTED_PROOF_DECLARATIONS = {
    "Stage1Instances.THM_M_1278_Obligations.exists_subtract_mean",
    "Stage1Instances.THM_M_1278_Obligations.dirichletEnergy_subtractMean",
}
EXPECTED_VALIDATION_DECLARATIONS = {
    "Stage1Instances.THM_M_1278_Validation.independentlyExistsSubtractMean",
    "Stage1Instances.THM_M_1278_Validation.independentlyDirichletEnergyInvariant",
}
CLOSED_IDS = ["M1278-N-SUBTRACT-MEAN", "M1278-N-ENERGY"]
REMAINING_CUT = ["M1278-L-SHARP-ONOFRI", "M1278-S-AREA", "M1278-S-FINITE"]


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict), path
    return value


def run(
    argv: list[str], *, cwd: Path = ROOT, env: dict[str, str] | None = None,
    timeout: int = 300
) -> str:
    result = subprocess.run(
        argv,
        cwd=cwd,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=timeout,
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


def axiom_reports(output: str) -> dict[str, set[str]]:
    reports = {}
    for declaration, body in re.findall(
        r"'([^']+)' depends on axioms:\s*\[([^]]*)\]", output, re.DOTALL
    ):
        reports[declaration] = {
            part.strip() for part in body.replace("\n", " ").split(",") if part.strip()
        }
    return reports


def sandboxed_lean(
    lean: str, lean_path: str, tmp: Path, source_name: str
) -> str:
    return run(
        [
            "bwrap",
            "--unshare-net",
            "--die-with-parent",
            "--ro-bind",
            "/",
            "/",
            "--bind",
            str(tmp),
            str(tmp),
            "--dev",
            "/dev",
            "--proc",
            "/proc",
            "--dir",
            "/run",
            "--setenv",
            "HOME",
            str(tmp / "home"),
            "--setenv",
            "TMPDIR",
            str(tmp),
            "--setenv",
            "LANG",
            "C.UTF-8",
            "--setenv",
            "LC_ALL",
            "C.UTF-8",
            "--setenv",
            "TZ",
            "UTC",
            "--setenv",
            "LEAN_NUM_THREADS",
            "1",
            "--setenv",
            "LEAN_PATH",
            f"{tmp}:{lean_path}",
            "--chdir",
            str(tmp),
            "--",
            lean,
            "--trust=0",
            "-t0",
            "-o",
            source_name.replace(".lean", ".olean"),
            source_name,
        ],
        timeout=300,
    )


spec = load(HERE / "validation-spec.json")
receipt = load(HERE / "validation-receipt.json")
statement = load(HERE / "statement.json")
anchor = load(HERE / "anchor-audit.json")
registry = load(HERE / "obligation-registry.json")
graphs = load(HERE / "typed-graphs.json")
proof_phase = load(HERE / "proof-phase.json")
proof_receipt = load(HERE / "proof-receipt.json")
execution = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")

assert spec["item_id"] == receipt["item_id"] == ITEM
assert spec["theorem_id"] == receipt["theorem_id"] == THEOREM
assert len(spec["recipes"]) == 1
recipe = spec["recipes"][0]
assert receipt["recipe"] == recipe
assert recipe["cwd"] == "." and isinstance(recipe["argv"], list)
assert recipe["expected_exit"] == 0 and recipe["network_policy"] == "denied"
assert recipe["network_enforcement"] == (
    "bubblewrap --unshare-net for every Lean invocation"
)
assert recipe["covered_obligation_ids"] == CLOSED_IDS
assert set(recipe["covered_declarations"]) == (
    EXPECTED_PROOF_DECLARATIONS | EXPECTED_VALIDATION_DECLARATIONS
)

validation_item = next(row for row in execution["items"] if row["id"] == ITEM)
proof_item = next(row for row in execution["items"] if row["id"] == "S56-M-1278-PROOF")
assert validation_item["phase"] == "validation"
assert validation_item["state"] in {"[ ]", "[_]"}
assert validation_item["depends_on"] == [proof_item["id"]]
assert validation_item["owned_paths"] == [f"Stage1_Instances/{THEOREM}"]
assert proof_item["state"] == "[_]"

assert statement["canonical_formal_target"]["statement_file_sha256"] == digest(
    HERE / "Statement.lean"
)
assert statement["canonical_formal_target"]["elaborated_expression_sha256"] == (
    "a267837ccca68a9ad86620bd4ce7c26c8d56861b57d76d6198ddce94ae671fdb"
)
assert registry["root_obligation_id"] == graphs["root_node_id"] == "M1278-ROOT"
denominator = registry["frozen_denominators"]
denominator_digest = hashlib.sha256(
    json.dumps(denominator, sort_keys=True, separators=(",", ":")).encode()
).hexdigest()
assert graphs["registry_denominator_sha256"] == denominator_digest

closure = graphs["closure_boundary"]
assert closure["closed_obligations"] == []
assert closure["root_closed"] is False
assert closure["audit_complete"] is False
assert closure["theorem_complete"] is False
assert closure["root_machine_debt"] == "M3"
assert closure["remaining_root_cut_set"] == REMAINING_CUT

assert proof_phase["item_id"] == proof_receipt["item_id"] == proof_item["id"]
assert proof_phase["inputs"] == proof_receipt["inputs"]
assert proof_phase["closed_obligation_ids"] == proof_receipt["closed_obligation_ids"] == CLOSED_IDS
assert proof_phase["first_failed_gate"] == proof_receipt["first_failed_gate"] == (
    "M1278-L-SHARP-ONOFRI"
)
assert proof_phase["remaining_root_cut_set"] == proof_receipt["remaining_root_cut_set"] == REMAINING_CUT
assert proof_receipt["accepted"] is False
assert proof_receipt["result"]["root_closed"] is False
assert proof_receipt["result"]["theorem_complete"] is False
assert load(HERE / "instance.json")["foundation_profile"] == (
    "Lean 4 dependent type theory; classical and choice usage not yet frozen"
)

fingerprints = {
    row["obligation_id"]: row["statement_fingerprint"]
    for row in registry["obligations"]
}
assert proof_receipt["obligation_statement_fingerprints"] == {
    obligation_id: fingerprints[obligation_id] for obligation_id in CLOSED_IDS
}

for relative, expected in receipt["inputs"].items():
    assert digest(ROOT / relative) == expected, f"stale validation input: {relative}"

prohibited = re.compile(
    r"\b(?:sorry|admit|sorryAx|implemented_by|native_decide|extern|opaque)\b"
    r"|^[ \t]*(?:axiom|unsafe|constant)\b",
    re.MULTILINE,
)
for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
    source = without_comments((HERE / name).read_text(encoding="utf-8"))
    assert prohibited.search(source) is None, f"prohibited proof device in {name}"
validation_source = without_comments((HERE / "Validation.lean").read_text(encoding="utf-8"))
assert not re.search(r"^import Proof$", validation_source, re.MULTILINE)
assert "subtractMean" not in validation_source.replace("validationSubtractMean", "")

assert digest(LEAN_ROOT / "lean-toolchain") == (
    "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2"
)
assert digest(LEAN_ROOT / "lake-manifest.json") == (
    "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81"
)
manifest = load(LEAN_ROOT / "lake-manifest.json")
mathlib_record = next(p for p in manifest["packages"] if p["name"] == "mathlib")
assert mathlib_record["rev"] == EXPECTED_MATHLIB
mathlib = (LEAN_ROOT / ".lake" / "packages" / "mathlib").resolve()
assert mathlib.is_dir(), "pinned mathlib artifact is unavailable"
assert run(["git", "rev-parse", "HEAD"], cwd=mathlib).strip() == EXPECTED_MATHLIB
assert run(["git", "rev-parse", "HEAD^{tree}"], cwd=mathlib).strip() == EXPECTED_MATHLIB_TREE
assert run(["git", "status", "--porcelain=v1"], cwd=mathlib) == ""

provenance = receipt["selected_provenance"]
assert anchor["environment"]["mathlib_revision"] == provenance["revision"] == EXPECTED_MATHLIB
assert provenance["tree"] == EXPECTED_MATHLIB_TREE
assert run(["git", "remote", "get-url", "origin"], cwd=mathlib).strip() == provenance["remote"]
for record in provenance["selected_import_sources"]:
    source = mathlib / record["file"]
    olean = mathlib / record["olean"]
    assert digest(source) == record["source_sha256"]
    assert run(["git", "rev-parse", f"HEAD:{record['file']}"], cwd=mathlib).strip() == record["git_blob"]
    assert digest(olean) == record["olean_sha256"]
assert digest(mathlib / "LICENSE") == provenance["license_sha256"]

lake_env = os.environ.copy()
lake_env["ELAN_TOOLCHAIN"] = "leanprover/lean4:v4.29.0"
lean = run(["lake", "env", "which", "lean"], cwd=LEAN_ROOT, env=lake_env).strip()
lake = run(["lake", "env", "which", "lake"], cwd=LEAN_ROOT, env=lake_env).strip()
lean_path = run(["lake", "env", "printenv", "LEAN_PATH"], cwd=LEAN_ROOT, env=lake_env).strip()
assert digest(Path(lean)) == receipt["environment"]["lean_executable_sha256"]
assert digest(Path(lake)) == receipt["environment"]["lake_executable_sha256"]
assert digest(Path(shutil.which("bwrap") or "")) == receipt["environment"]["bubblewrap_sha256"]
assert digest(Path(sys.executable)) == receipt["environment"]["python_executable_sha256"]
assert digest(Path(shutil.which("git") or "")) == receipt["environment"]["git_executable_sha256"]

with tempfile.TemporaryDirectory(prefix="m1278-validation-") as tmp_name:
    tmp = Path(tmp_name)
    (tmp / "home").mkdir()
    for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
        shutil.copy2(HERE / name, tmp / name)
    outputs = {
        name: sandboxed_lean(lean, lean_path, tmp, name)
        for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean")
    }

proof_reports = axiom_reports(outputs["Proof.lean"])
assert proof_reports == {
    declaration: EXPECTED_AXIOMS for declaration in EXPECTED_PROOF_DECLARATIONS
}
validation_reports = axiom_reports(outputs["Validation.lean"])
assert validation_reports == {
    declaration: EXPECTED_AXIOMS for declaration in EXPECTED_VALIDATION_DECLARATIONS
}
combined_output = "\n".join(outputs.values())
assert "declaration uses 'sorry'" not in combined_output
assert "sorryAx" not in combined_output
assert "error:" not in combined_output

result = receipt["result"]
assert result["accepted_closed_obligation_ids"] == []
assert result["locally_revalidated_provisional_obligation_ids"] == CLOSED_IDS
assert result["root_closed"] is False
assert result["audit_complete"] is False
assert result["theorem_complete"] is False
for gate in (
    "canonical_root_transport_gate",
    "complete_transitive_provenance_gate",
    "complete_transitive_tcb_gate",
    "hermetic_release_gate",
    "independent_distinct_runner_gate",
):
    assert result[gate] == "fail_closed"
assert receipt["release_grade"] is False
assert receipt["support_state"] == "provisional_worker_selftest"
assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False

selftest_path = ROOT / ".stage1-worker-selftest.json"
if selftest_path.exists():
    selftest = load(selftest_path)
    if selftest.get("item_id") == ITEM:
        assert set(selftest) == {
            "item_id", "changed_paths", "commands", "output_summary",
            "base_revision", "known_failures", "state",
        }
        assert selftest["state"] == "[_]"
        assert selftest["base_revision"] == receipt["base_revision"]
        assert selftest["changed_paths"] == receipt["changed_paths"]
        assert selftest["known_failures"] == receipt["known_failures"]

print("PASS THM-M-1278 narrow validation")
print("kernel: two partial proof bodies and two separately reconstructed probes replayed at trust zero with network denied")
print("trust: machine reports only propext, Classical.choice, Quot.sound; no sorry or prohibited local device")
print("provenance: proof hashes, selected mathlib sources/oleans/license, clean pin, and tool identities agree")
print("root open: sharp Onofri, area/finiteness, normalization transport, and canonical namespace bridge remain unproved")
print("blocked: proof master acceptance, cold empty-cache release replay, complete trust/provenance, and distinct-runner verification")
