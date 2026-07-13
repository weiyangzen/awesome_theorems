#!/usr/bin/env python3
"""Fail-closed narrow validation for S56-M-0471-VALIDATION."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import platform
import re
import shutil
import subprocess
import time


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0471"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM = "S56-M-0471-VALIDATION"
THEOREM = "THM-M-0471"
BASE_REVISION = "f023dbc3411d83201065d1a1156d7406b81135d4"
BASE_TREE = "3b3a73ec19293a2a9b8d9c7e67f0d25da2a511b4"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MATHLIB_REMOTE = "https://github.com/leanprover-community/mathlib4.git"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
EXPRESSION_SHA256 = "07ae92b7b398b89a1bbe8413563f1c30da5b8bbd0522f6d070fd62dcea0ac4e4"
DENOMINATOR_SHA256 = "d3f11762e2a0f4c384d094d53e44100f20a21f81eb6ce527cd5f9897a9bc445c"
EXPECTED_AXIOMS = ["propext", "Classical.choice", "Quot.sound"]
MACHINE_IDS = [
    "M0471-ROOT",
    "M0471-S-INTERFACE",
    "M0471-S-BOUNDARY",
    "M0471-S-TRANSPORT",
    "M0471-S-FOUNDATION",
    "M0471-T-ROOT-COMPOSE",
    "M0471-T-ASSEMBLE",
    "M0471-C-WITNESS",
    "M0471-L-NONEMPTY",
    "M0471-N-NONZERO",
    "M0471-L-PRIMALITY",
    "M0471-L-PRODUCT",
    "M0471-L-UNIQUENESS",
    "M0471-L-PERM-PRODUCT",
    "M0471-L-PRIME-DVD-PRODUCT",
    "M0471-L-MEM-PRIME-DIVISOR",
    "M0471-C-ERASE-PERM",
    "M0471-N-CANCEL-HEAD",
]
PROOF_IDS = [
    "M0471-ROOT",
    "M0471-T-ROOT-COMPOSE",
    "M0471-T-ASSEMBLE",
    "M0471-C-WITNESS",
    "M0471-L-NONEMPTY",
    "M0471-S-BOUNDARY",
    "M0471-L-PRIMALITY",
    "M0471-L-PRODUCT",
    "M0471-N-NONZERO",
    "M0471-L-UNIQUENESS",
    "M0471-L-PERM-PRODUCT",
    "M0471-L-PRIME-DVD-PRODUCT",
    "M0471-L-MEM-PRIME-DIVISOR",
    "M0471-C-ERASE-PERM",
    "M0471-N-CANCEL-HEAD",
]
OPEN_MACHINE_IDS = [
    "M0471-S-INTERFACE",
    "M0471-S-TRANSPORT",
    "M0471-S-FOUNDATION",
]
EXPECTED_INPUTS = {
    "Statement.lean": "775b86743247571a1a5e5e7f1aa099683f26368e4dd7bee9e23a0b2a2ddbc715",
    "ObligationTree.lean": "f660075c72926a90d5da4b8ea8ce18484eb8dadf8fd2ca3cbab236dce51f1d21",
    "Proof.lean": "0c09e7b2d6df883bb7771edbf7f71b5f015d2bb19fee2559f66b0ecbfc846a34",
    "Validation.lean": "ce4417c183ee07e38a3eaaa4f0a3e842b0290ff1134532a8e1848ff152116e80",
    "statement.json": "ba121a8a637e1cd8a36d640ea1f8f1320a5f66c35c76dba64e0369b6ffa02b54",
    "instance.json": "d0f7b0a357482cb7bf32b3cf8ba673b4fe817091d32f095ffedac603dbfa021d",
    "task-dag.json": "01243ffe02c5e1380496fd01a7b34c31fc850087fb7b4236eeed8a9fcca67b1f",
    "anchor-audit.json": "0252dce7a149abfefde425db99694f8400ccc3e8a2d3a9ac6d39c066b2af31bf",
    "obligation-registry.json": "bc620c7bf04b4c50ad22e5c6bbc62bb94dbec34df2d2aab2d021ca1e22ca3f14",
    "typed-graphs.json": "bd7e7e9455079638bf787ef27557c654627c8eec2c8da903720ed65fedcef89a",
    "validation-specs.json": "d80479698d5e3983172cefcd507928315eab4b45445d8d6261ac1e721a0832eb",
    "proof-receipt.json": "9bf2310bf7cee88f070d1ede4b63b7cb65ffb914f682898e455dc75e2eaa83fc",
    "check_validation.sh": "3a550a2ec13f6d849711419fc67963e3be9a4a10fbf3713405ee64d26789edae",
    "validation-spec.json": "a033e2b3af6fde48a0f1faac975cfa2ee5c6d30f92601846eece1ff575592654",
}
EXPECTED_TOOL_INPUTS = {
    "lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
LEAN_BIN = Path.home() / ".elan/toolchains/leanprover--lean4---v4.29.0/bin/lean"
LAKE_BIN = Path.home() / ".elan/toolchains/leanprover--lean4---v4.29.0/bin/lake"
LEAN_BIN_SHA256 = "3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf"
LAKE_BIN_SHA256 = "a608ff084d7e2af228b92a29d7c2fd083ba0580e46889175ec74a81678c98359"
PYTHON_SHA256 = "b8d8288faefdd300201f43fcf00f6f539a27218eeed3a3dff5ab10b9c4c99700"
GIT_SHA256 = "8a48eefa306b9a2a9c3e576784a74ad7485779279e5a46ec43361a1864760e45"
BWRAP_SHA256 = "0abea81db798ebf6b4742ac0664802d97521547a353c2a0dbdc21d76cbbfd2c0"
FACTORS_SOURCE = Path("Mathlib/Data/Nat/Factors.lean")
FACTORS_BLOB = "292355d305be37499c8415d15b430aa241132c9b"
FACTORS_SHA256 = "3e64e2c8ba907c05209966a7bba8754cf2ab33f328a3010667ffe58c95e0bca3"
FACTORS_OLEAN_SHA256 = "ca04f32795ce6aba7a89b812e7b57cf1a11ebebb4a2428469252dad6fa132b70"
LIST_PRIME_SOURCE = Path("Mathlib/Data/List/Prime.lean")
LIST_PRIME_BLOB = "17337ba91fd2f4b2b947301cca165a253662e377"
LIST_PRIME_SHA256 = "148cf3e70ddc39591270dd3c4d9da733a91ff574e8f5c1bd6fd8fd2f42e33591"
LIST_PRIME_OLEAN_SHA256 = "0070fd6c21af18e3bc139e406be76fc7f7d6d2b62165eee6910aee740126c328"
LICENSE_SHA256 = "b40930bbcf80744c86c46a12bc9da056641d722716c378f5659b9e555ef833e1"
BODY_SHA256 = {
    "Nat.primeFactorsList:lines-37-44": "c7f1900ede17ad807bf5c98b8a22313a617b1cb11ded1bf797174788a1f7ed30",
    "Nat.primeFactorsList-support:lines-55-81": "30138baae00a62af9232fae141b6e8de930d02ebadec324e591a5bc34f3eed4b",
    "Nat.primeFactorsList_ne_nil:lines-131-132": "4fc64ac6920baa49818602f21af9407eea87d063514f69681505069fdb055767",
    "Nat.primeFactorsList_unique:lines-167-179": "485900bbad5a00b60265899a34e558a67eb68d3315ecf2548a3020d5e41240e2",
    "Prime-list-engine:lines-27-78": "847b244f888b9e5b22e6f6ec7666c0b67bc4f485606f89f8522ed4948b271b01",
}
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
    "PASS THM-M-0471 narrow validation",
    "PASS network-isolated kernel replay: exact statement, two frozen compositions, two proof roots, and differential root elaborated",
    "PASS trust observation: composition, proof, terminal, and differential declarations stay within propext, Classical.choice, and Quot.sound",
    "PASS selected provenance: frozen hashes, terminal source/blob/body/olean, clean mathlib pin, remote, license, and tools agree",
    "PASS hygiene: Lean sorry reports and local/selected-terminal prohibited scans agree",
    "FAIL CLOSED authority/trust: proof master acceptance and complete transitive provenance, foundation, and TCB closure remain open at H1/M3/R4",
    "FAIL CLOSED hermetic release: shared warm .lake is not clean-checkout empty-cache bootstrap, offline restoration, or a deterministic TCB/SBOM bundle",
    "FAIL CLOSED independent release: differential proof used this worker and shared cache, not a distinct signed verifier",
    "audit_complete=false; theorem_complete=false",
)
VALIDATION_STARTED = time.monotonic()
TIMEOUT_SECONDS = 180.0


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict), path
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sha256_lines(path: Path, start: int, end: int) -> str:
    lines = path.read_bytes().splitlines(keepends=True)
    return hashlib.sha256(b"".join(lines[start - 1 : end])).hexdigest()


def run(argv: list[str], *, cwd: Path = ROOT, check: bool = True) -> subprocess.CompletedProcess[str]:
    remaining = TIMEOUT_SECONDS - (time.monotonic() - VALIDATION_STARTED)
    if remaining <= 0:
        raise TimeoutError("validation recipe exceeded its 180-second wall-clock bound")
    result = subprocess.run(
        argv,
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=remaining,
        check=False,
    )
    if check and result.returncode != 0:
        raise RuntimeError(
            f"validation failed ({result.returncode}): {argv!r}\n{result.stdout}"
        )
    return result


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["git", *args], cwd=cwd).stdout.strip()


def code_without_comments(source: str) -> str:
    source = re.sub(r"/-.*?-/", "", source, flags=re.DOTALL)
    return re.sub(r"--.*$", "", source, flags=re.MULTILINE)


def assert_text_hygiene(path: Path) -> None:
    data = path.read_bytes()
    assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())


def main() -> None:
    spec = load(HERE / "validation-spec.json")
    receipt = load(HERE / "validation-receipt.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")
    targets = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    instance = load(HERE / "instance.json")
    local_dag = load(HERE / "task-dag.json")
    statement = load(HERE / "statement.json")
    anchor = load(HERE / "anchor-audit.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    frozen_specs = load(HERE / "validation-specs.json")
    proof_receipt = load(HERE / "proof-receipt.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 1353 and target["baseline"] == "L0"
    assert target["lifecycle_mode"] == "planned"
    assert target["rework_required"] is True and target["theorem_complete"] is False
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item == {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 1353,
        "phase": "validation",
        "layer": 5,
        "state": "[ ]",
        "depends_on": ["S56-M-0471-PROOF"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Run hermetic kernel, trust, provenance, and independent validation gates.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }
    predecessor = next(
        row for row in execution["items"] if row["id"] == "S56-M-0471-PROOF"
    )
    assert predecessor["state"] == "[_]" and predecessor["attempts"] == 1
    local_task = next(row for row in local_dag["tasks"] if row["id"] == ITEM)
    assert local_task["state"] == "open"
    assert local_task["depends_on"] == ["S56-M-0471-PROOF"]

    assert instance["lifecycle_mode"] == "planned"
    assert instance["root_vector"] == {"H": "H1", "M": "M3", "R": "R4"}
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == []
    assert instance["audit_complete"] is instance["theorem_complete"] is False
    closure = graphs["closure_boundary"]
    assert closure["accepted_closed_obligations"] == []
    assert closure["root_closed"] is False
    assert closure["root_machine_debt"] == "M3"
    assert closure["audit_complete"] is closure["theorem_complete"] is False

    for name, expected in EXPECTED_INPUTS.items():
        assert sha256(HERE / name) == expected, f"stale validation input: {name}"
    for name, expected in EXPECTED_TOOL_INPUTS.items():
        assert sha256(LEAN_ROOT / name) == expected, f"changed tool input: {name}"
    formal = statement["canonical_formal_target"]
    assert formal["declaration_or_expression"] == (
        "Stage1Instances.THM_M_0471.FundamentalTheoremOfArithmeticTarget"
    )
    assert formal["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert formal["statement_file_sha256"] == EXPECTED_INPUTS["Statement.lean"]
    assert anchor["canonical_target"]["expression_sha256"] == EXPRESSION_SHA256
    assert registry["frozen_against_statement_sha256"] == EXPECTED_INPUTS["Statement.lean"]
    assert registry["frozen_against_anchor_audit_sha256"] == EXPECTED_INPUTS["anchor-audit.json"]
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert registry["frozen_denominators"]["required_machine"] == MACHINE_IDS
    assert graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert proof_receipt["canonical_target_expression_sha256"] == EXPRESSION_SHA256
    assert proof_receipt["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert proof_receipt["proof_body"]["source_sha256"] == EXPECTED_INPUTS["Proof.lean"]
    assert proof_receipt["provisionally_closed_proof_obligation_ids"] == PROOF_IDS
    assert proof_receipt["required_machine_open_ids"] == OPEN_MACHINE_IDS
    assert proof_receipt["accepted_closed_obligation_ids"] == []
    assert proof_receipt["result"]["root_kernel_closed"] is True
    assert proof_receipt["result"]["accepted_root_closed"] is False
    assert proof_receipt["result"]["axioms"] == EXPECTED_AXIOMS
    assert proof_receipt["accepted"] is False
    assert frozen_specs["item_id"] == "S56-M-0471-OBLIGATION_TREE"
    assert all(
        row["argv"] == [
            "python3", "-B", f"Stage1_Instances/{THEOREM}/check_obligation_tree.py"
        ]
        for row in frozen_specs["recipes"]
    )

    proof_edges = {
        (edge["from"], edge["to"])
        for edge in graphs["graphs"]["proof"]["edges"]
        if edge["type"] == "proof_requires"
    }
    children: dict[str, set[str]] = {}
    for parent, child in proof_edges:
        children.setdefault(parent, set()).add(child)
    reachable: set[str] = set()
    pending = ["M0471-ROOT"]
    while pending:
        obligation = pending.pop()
        if obligation in reachable:
            continue
        reachable.add(obligation)
        pending.extend(children.get(obligation, set()))
    assert reachable == set(PROOF_IDS)

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by|extern)\b|"
        r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
        r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
        r"(?:axiom|constant|opaque|unsafe)\b",
        re.MULTILINE,
    )
    for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
        source = code_without_comments((HERE / name).read_text(encoding="utf-8"))
        assert prohibited.search(source) is None, f"prohibited source token in {name}"
    differential = code_without_comments((HERE / "Validation.lean").read_text(encoding="utf-8"))
    for forbidden in (
        "import Proof", "import ObligationTree", "Proof.",
        "exactPrimeListAnchor", "root_of_exactPrimeListAnchor",
        "fundamentalTheoremOfArithmetic_via_frozen_composition",
    ):
        assert forbidden not in differential, forbidden
    assert "let factors := Nat.primeFactorsList n" in differential
    assert "Nat.primeFactorsList_unique hk.2 hk.1" in differential
    assert "assert_no_sorry independentlyReconstructedFundamentalTheoremOfArithmetic" in differential

    manifest = load(LEAN_ROOT / "lake-manifest.json")
    mathlib_entry = next(row for row in manifest["packages"] if row["name"] == "mathlib")
    assert mathlib_entry["rev"] == mathlib_entry["inputRev"] == MATHLIB_REVISION
    assert MATHLIB.resolve().is_dir(), "pinned mathlib artifact is unavailable"
    assert git("rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert git("remote", "get-url", "origin", cwd=MATHLIB) == MATHLIB_REMOTE
    assert git("status", "--porcelain=v1", cwd=MATHLIB) == ""
    factors_source = MATHLIB / FACTORS_SOURCE
    factors_olean = MATHLIB / ".lake/build/lib/lean" / FACTORS_SOURCE.with_suffix(".olean")
    list_source = MATHLIB / LIST_PRIME_SOURCE
    list_olean = MATHLIB / ".lake/build/lib/lean" / LIST_PRIME_SOURCE.with_suffix(".olean")
    assert git("rev-parse", f"HEAD:{FACTORS_SOURCE}", cwd=MATHLIB) == FACTORS_BLOB
    assert git("rev-parse", f"HEAD:{LIST_PRIME_SOURCE}", cwd=MATHLIB) == LIST_PRIME_BLOB
    assert sha256(factors_source) == FACTORS_SHA256
    assert sha256(factors_olean) == FACTORS_OLEAN_SHA256
    assert sha256(list_source) == LIST_PRIME_SHA256
    assert sha256(list_olean) == LIST_PRIME_OLEAN_SHA256
    assert sha256(MATHLIB / "LICENSE") == LICENSE_SHA256
    assert sha256_lines(factors_source, 37, 44) == BODY_SHA256["Nat.primeFactorsList:lines-37-44"]
    assert sha256_lines(factors_source, 55, 81) == BODY_SHA256["Nat.primeFactorsList-support:lines-55-81"]
    assert sha256_lines(factors_source, 131, 132) == BODY_SHA256["Nat.primeFactorsList_ne_nil:lines-131-132"]
    assert sha256_lines(factors_source, 167, 179) == BODY_SHA256["Nat.primeFactorsList_unique:lines-167-179"]
    assert sha256_lines(list_source, 27, 78) == BODY_SHA256["Prime-list-engine:lines-27-78"]
    for source in (factors_source, list_source):
        assert prohibited.search(code_without_comments(source.read_text(encoding="utf-8"))) is None

    python = Path(os.path.realpath(os.sys.executable))
    git_path = shutil.which("git")
    bwrap = shutil.which("bwrap")
    assert git_path is not None and bwrap is not None
    assert LEAN_BIN.is_file() and LAKE_BIN.is_file()
    assert sha256(LEAN_BIN) == LEAN_BIN_SHA256
    assert sha256(LAKE_BIN) == LAKE_BIN_SHA256
    assert sha256(python) == PYTHON_SHA256
    assert sha256(Path(os.path.realpath(git_path))) == GIT_SHA256
    assert sha256(Path(os.path.realpath(bwrap))) == BWRAP_SHA256
    lean_version = run([str(LEAN_BIN), "--version"]).stdout
    assert "4.29.0" in lean_version and LEAN_COMMIT in lean_version

    runner = run(["bash", str(HERE / "check_validation.sh")]).stdout
    assert hashlib.sha256(runner.encode()).hexdigest() == (
        "97ce534ac3d2011dcd3210c0e39711c53181e7cb5462e3ca9e751799a0f4999c"
    )
    assert runner.count("Declarations are sorry-free!") == 25
    assert "sorryAx" not in runner and "declaration uses 'sorry'" not in runner

    predecessor_obligation = run(
        ["python3", "-B", str(HERE / "check_obligation_tree.py")], check=False
    )
    assert predecessor_obligation.returncode != 0
    assert "AssertionError" in predecessor_obligation.stdout
    predecessor_proof = run(
        ["python3", "-B", str(HERE / "check_proof.py")], check=False
    )
    assert predecessor_proof.returncode != 0
    assert "AssertionError" in predecessor_proof.stdout or (
        "FileNotFoundError" in predecessor_proof.stdout
        and ".stage1-worker-selftest.json" in predecessor_proof.stdout
    )

    assert spec["schema_version"] == "stage1-validation-recipe/1.0"
    assert spec["item_id"] == ITEM and spec["theorem_id"] == THEOREM
    assert spec["cwd"] == "."
    assert spec["argv"] == ["python3", "-B", f"Stage1_Instances/{THEOREM}/check_validation.py"]
    assert spec["env_allowlist"] == {} and spec["timeout_seconds"] == 180
    assert spec["network_policy"] == "denied" and spec["expected_exit"] == 0
    assert "read-only host root" in spec["network_enforcement"]
    assert spec["covered_obligation_ids"] == MACHINE_IDS
    assert spec["expected_outputs"] == [{
        "path_or_stream": "stdout",
        "semantic_hash_policy": "exact nine-line PASS/FAIL-CLOSED status summary",
    }]

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["phase"] == "validation" and receipt["intent"] == "validate"
    assert receipt["depends_on"] == ["S56-M-0471-PROOF"]
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["release_grade"] is False
    assert receipt["content_addressed_release_evidence"] is False
    assert receipt["covered_obligation_ids"] == MACHINE_IDS
    assert receipt["accepted_closed_obligation_ids"] == []
    for name, expected in EXPECTED_INPUTS.items():
        assert receipt["inputs"][name] == expected, name
    assert receipt["inputs"]["check_validation.py"] == sha256(HERE / "check_validation.py")
    assert receipt["inputs"]["validation-phase.md"] == sha256(HERE / "validation-phase.md")
    assert receipt["inputs"]["worker_packet"] == sha256(ROOT / ".stage1-worker-selftest.json")
    assert receipt["canonical_target"] == {
        "declaration": "Stage1Instances.THM_M_0471.FundamentalTheoremOfArithmeticTarget",
        "elaborated_expression_sha256": EXPRESSION_SHA256,
        "registry_denominator_sha256": DENOMINATOR_SHA256,
    }
    environment = receipt["environment"]
    assert environment["platform"] == f"{platform.system()} {platform.release()} {platform.machine()}"
    assert environment["lean_executable_sha256"] == sha256(LEAN_BIN)
    assert environment["lake_executable_sha256"] == sha256(LAKE_BIN)
    assert environment["python_executable_sha256"] == sha256(python)
    assert environment["git_executable_sha256"] == sha256(Path(os.path.realpath(git_path)))
    assert environment["bubblewrap_executable_sha256"] == sha256(Path(os.path.realpath(bwrap)))
    assert environment["mathlib_revision"] == MATHLIB_REVISION
    assert environment["mathlib_tree"] == MATHLIB_TREE
    provenance = receipt["provenance"]
    assert provenance["origins"][0]["source_sha256"] == FACTORS_SHA256
    assert provenance["origins"][1]["source_sha256"] == LIST_PRIME_SHA256
    assert provenance["terminal_body_identities"] == {
        key: f"sha256:{value}" for key, value in BODY_SHA256.items()
    }
    assert provenance["license_sha256"] == LICENSE_SHA256
    for key in (
        "recipe_id", "cwd", "argv", "env_allowlist", "timeout_seconds",
        "network_policy", "network_enforcement", "expected_exit",
        "expected_outputs", "covered_obligation_ids", "covered_declarations",
    ):
        assert receipt["recipe"][key] == spec[key], key
    result = receipt["result"]
    assert result["exact_root_kernel_replay"] == "provisional_pass"
    assert result["differential_exact_root_replay"] == "provisional_pass_same_worker"
    assert result["observed_axioms"] == EXPECTED_AXIOMS
    assert result["placeholder_and_unsafe_scan"] == "pass"
    assert result["selected_provenance"] == "pass"
    assert result["network_isolated_lean_replay"] == "pass"
    assert result["predecessor_recipe_freshness"] == "fail_closed"
    assert result["proof_master_acceptance"] == "fail_closed"
    assert result["accepted_root_machine_debt"] == "M3"
    assert result["accepted_root_closed"] is False
    assert result["foundation_and_complete_trust_closure"] == "fail_closed"
    assert result["hermetic_cold_offline_replay"] == "fail_closed"
    assert result["independent_distinct_runner"] == "fail_closed"
    assert result["audit_complete"] is result["theorem_complete"] is False
    assert receipt["first_failed_gate"] == "dependency.S56-M-0471-PROOF.master_acceptance"
    assert receipt["first_failed_release_gate"] == "S56-10.6-HERMETIC-COLD-BUILD"

    assert set(packet) == {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert packet["item_id"] == ITEM and packet["state"] == "[_]"
    assert packet["base_revision"] == BASE_REVISION
    assert set(packet["changed_paths"]) == set(receipt["changed_paths"]) == CHANGED_PATHS
    assert packet["known_failures"] == receipt["known_failures"]
    status = git("status", "--short", "--untracked-files=all")
    actual_changed = {
        line[3:] for line in status.splitlines()
        if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual_changed == CHANGED_PATHS, (actual_changed, CHANGED_PATHS)
    phase_notes = (HERE / "validation-phase.md").read_text(encoding="utf-8")
    assert "audit and theorem completion remain false" in phase_notes
    assert "same-worker differential" in phase_notes
    assert "empty-cache cold bootstrap" in phase_notes
    for relative in CHANGED_PATHS:
        assert_text_hygiene(ROOT / relative)

    print("\n".join(SUMMARY_LINES))


if __name__ == "__main__":
    main()
