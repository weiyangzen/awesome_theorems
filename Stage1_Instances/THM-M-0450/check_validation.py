#!/usr/bin/env python3
"""Fail-closed narrow validation for S56-M-0450-VALIDATION."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0450"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
ITEM = "S56-M-0450-VALIDATION"
THEOREM = "THM-M-0450"
EXPECTED_MATHLIB = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
EXPECTED_MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
EXPECTED_PROOF_DECLARATIONS = {
    "Stage1Instances.THM_M_0450.Proof.fg_iff_of_addEquiv",
    "Stage1Instances.THM_M_0450.Proof.finiteIndex_iff_of_addEquiv",
    "Stage1Instances.THM_M_0450.Proof.comap_doubling_range",
    "Stage1Instances.THM_M_0450.Proof.doubling_finiteIndex_iff_of_addEquiv",
    "Stage1Instances.THM_M_0450.Proof.northcott_comp_addEquiv",
    "Stage1Instances.THM_M_0450.Proof.nonnegative_comp_addEquiv",
    "Stage1Instances.THM_M_0450.Proof.parallelogram_comp_addEquiv",
    "Stage1Instances.THM_M_0450.Proof.jacobian_fg_iff_affine_fg",
    "Stage1Instances.THM_M_0450.Proof.jacobian_doubling_finiteIndex_iff_affine",
    "Stage1Instances.THM_M_0450.Proof.exactTarget_of_descent_packages",
}
VALIDATION_DECLARATION = (
    "Stage1Instances.THM_M_0450.Validation.exactTarget_conditional_probe"
)
REMAINING_CUT = [
    "M0450-B-WEAKMW",
    "M0450-H-HEIGHT",
    "M0450-X-TRANSPORT",
    "M0450-X-SOURCE",
    "M0450-X-PROVENANCE",
    "M0450-X-TRUST",
]


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
            part.strip() for part in body.split(",") if part.strip()
        }
    return reports


def sandboxed_lean(
    lean: str, lean_path: str, tmp: Path, source_name: str
) -> str:
    output_name = source_name.replace(".lean", ".olean")
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
            "/tmp/home",
            "--setenv",
            "TMPDIR",
            "/tmp",
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
            "-o",
            output_name,
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
proof_receipt = load(HERE / "proof-receipt.json")
execution = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")

assert spec["item_id"] == receipt["item_id"] == ITEM
assert spec["theorem_id"] == receipt["theorem_id"] == THEOREM
assert len(spec["recipes"]) == 1
recipe = spec["recipes"][0]
assert receipt["recipe"] == recipe
assert recipe["cwd"] == "." and isinstance(recipe["argv"], list)
assert recipe["expected_exit"] == 0
assert recipe["network_policy"] == "denied"
assert recipe["network_enforcement"] == (
    "bubblewrap --unshare-net for every Lean invocation"
)
assert set(recipe["covered_declarations"]) == (
    EXPECTED_PROOF_DECLARATIONS | {VALIDATION_DECLARATION}
)

validation_item = next(row for row in execution["items"] if row["id"] == ITEM)
proof_item = next(
    row for row in execution["items"] if row["id"] == "S56-M-0450-PROOF"
)
assert validation_item["phase"] == "validation"
assert validation_item["state"] in {"[ ]", "[_]"}
assert validation_item["depends_on"] == [proof_item["id"]]
assert validation_item["owned_paths"] == [f"Stage1_Instances/{THEOREM}"]
assert proof_item["state"] == "[_]"

assert statement["lean"]["source_sha256"] == digest(HERE / "Statement.lean")
assert registry["root_obligation_id"] == "M0450-ROOT"
assert registry["frozen_against_statement_sha256"] == digest(HERE / "Statement.lean")
assert graphs["registry_denominator_sha256"] == registry["denominator_sha256"]
closure = graphs["closure_boundary"]
assert closure["root_closed"] is False
assert closure["audit_complete"] is False
assert closure["theorem_complete"] is False
assert closure["remaining_root_cut_set"] == REMAINING_CUT

assert proof_receipt["item_id"] == "S56-M-0450-PROOF"
assert proof_receipt["proof_body"]["source_sha256"] == digest(HERE / "Proof.lean")
assert proof_receipt["inputs"]["statement_sha256"] == digest(HERE / "Statement.lean")
assert proof_receipt["inputs"]["obligation_tree_sha256"] == digest(
    HERE / "ObligationTree.lean"
)
assert proof_receipt["inputs"]["obligation_registry_sha256"] == digest(
    HERE / "obligation-registry.json"
)
assert proof_receipt["inputs"]["typed_graphs_sha256"] == digest(
    HERE / "typed-graphs.json"
)
assert proof_receipt["closed_obligation_ids"] == []
assert proof_receipt["result"]["root_closed"] is False
assert proof_receipt["result"]["theorem_complete"] is False
assert proof_receipt["remaining_root_cut_set"] == REMAINING_CUT

for relative, expected in receipt["inputs"].items():
    path = ROOT / relative
    assert digest(path) == expected, f"stale validation input: {relative}"

prohibited = re.compile(
    r"\b(?:sorry|admit|sorryAx|implemented_by|native_decide|extern|opaque)\b"
    r"|^[ \t]*(?:axiom|unsafe|constant)\b",
    re.MULTILINE,
)
for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
    source = without_comments((HERE / name).read_text(encoding="utf-8"))
    assert prohibited.search(source) is None, f"prohibited proof device in {name}"
validation_source = without_comments((HERE / "Validation.lean").read_text(encoding="utf-8"))
assert not re.search(r"^import (?:Proof|ObligationTree)$", validation_source, re.MULTILINE)
assert "Proof." not in validation_source and "ObligationTree." not in validation_source

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
assert anchor["mathlib"]["revision"] == provenance["revision"] == EXPECTED_MATHLIB
assert anchor["mathlib"]["tree"] == provenance["tree"] == EXPECTED_MATHLIB_TREE
assert run(["git", "remote", "get-url", "origin"], cwd=mathlib).strip() == provenance["remote"]
for record in provenance["terminal_sources"]:
    path = mathlib / record["file"]
    assert digest(path) == record["source_sha256"]
    assert run(["git", "rev-parse", f"HEAD:{record['file']}"], cwd=mathlib).strip() == record["git_blob"]
    assert digest(mathlib / record["olean"]) == record["olean_sha256"]
assert digest(mathlib / "LICENSE") == provenance["license_sha256"]

lean = run(["lake", "env", "which", "lean"], cwd=LEAN_ROOT).strip()
lean_path = run(["lake", "env", "printenv", "LEAN_PATH"], cwd=LEAN_ROOT).strip()
assert digest(Path(lean)) == receipt["environment"]["lean_executable_sha256"]
assert digest(Path(shutil.which("bwrap") or "")) == receipt["environment"]["bubblewrap_sha256"]

with tempfile.TemporaryDirectory(prefix="m0450-validation-") as tmp_name:
    tmp = Path(tmp_name)
    for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
        shutil.copy2(HERE / name, tmp / name)
    outputs = {
        name: sandboxed_lean(lean, lean_path, tmp, name)
        for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean")
    }

proof_reports = axiom_reports(outputs["Proof.lean"])
assert set(proof_reports) == EXPECTED_PROOF_DECLARATIONS
assert all(axioms == EXPECTED_AXIOMS for axioms in proof_reports.values())
validation_reports = axiom_reports(outputs["Validation.lean"])
assert validation_reports == {VALIDATION_DECLARATION: EXPECTED_AXIOMS}
assert "declaration uses 'sorry'" not in outputs["Validation.lean"]
assert "sorryAx" not in "\n".join(outputs.values())

assert receipt["result"]["root_closed"] is False
assert receipt["result"]["audit_complete"] is False
assert receipt["result"]["theorem_complete"] is False
assert receipt["result"]["accepted_closed_obligation_ids"] == []
assert receipt["result"]["hermetic_release_gate"] == "fail_closed"
assert receipt["result"]["complete_transitive_tcb_gate"] == "fail_closed"
assert receipt["result"]["independent_distinct_runner_gate"] == "fail_closed"
assert receipt["release_grade"] is False
assert receipt["support_state"] == "provisional_worker_selftest"

selftest_path = ROOT / ".stage1-worker-selftest.json"
if selftest_path.exists():
    selftest = load(selftest_path)
    if selftest.get("item_id") == ITEM:
        assert set(selftest) == {
            "item_id",
            "changed_paths",
            "commands",
            "output_summary",
            "base_revision",
            "known_failures",
            "state",
        }
        assert selftest["state"] == "[_]"
        assert selftest["base_revision"] == receipt["base_revision"]
        assert selftest["changed_paths"] == receipt["changed_paths"]
        assert selftest["known_failures"] == receipt["known_failures"]

print("PASS THM-M-0450 narrow validation")
print("kernel: 10 proof declarations and a separately reconstructed conditional probe replayed with network denied")
print("trust: machine reports only propext, Classical.choice, Quot.sound; no sorry or prohibited local device")
print("provenance: proof hashes, selected mathlib sources/oleans/license, and clean pin agree")
print("root open: weak Mordell-Weil and elliptic height packages remain unproved; no whole frozen obligation closed")
print("blocked: proof master acceptance, cold empty-cache release replay, complete TCB closure, and distinct-runner verification")
