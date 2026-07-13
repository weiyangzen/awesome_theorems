#!/usr/bin/env python3
"""Fail-closed worker validation for S56-M-0476-VALIDATION."""

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
HERE = ROOT / "Stage1_Instances" / "THM-M-0476"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM = "S56-M-0476-VALIDATION"
THEOREM = "THM-M-0476"
BASE_REVISION = "c45f3c7090cb4adf616d45e5414985f956e807b2"
BASE_TREE = "da6f991c07f11e8608ddc090af9356558d64d360"
EXPRESSION_SHA256 = "ee76edb160426d3e8d95b11bfedca7febcfe915f50007e042875c922ebc8a4ac"
DENOMINATOR_SHA256 = "9375f9b987132465572c04a019d70b32638823c1279dd91a7935007f108fe62b"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
LEAN_BIN = Path.home() / ".elan/toolchains/leanprover--lean4---v4.29.0/bin/lean"
LAKE_BIN = Path.home() / ".elan/toolchains/leanprover--lean4---v4.29.0/bin/lake"
LEAN_BIN_SHA256 = "3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf"
LAKE_BIN_SHA256 = "a608ff084d7e2af228b92a29d7c2fd083ba0580e46889175ec74a81678c98359"
PYTHON_SHA256 = "b8d8288faefdd300201f43fcf00f6f539a27218eeed3a3dff5ab10b9c4c99700"
GIT_SHA256 = "8a48eefa306b9a2a9c3e576784a74ad7485779279e5a46ec43361a1864760e45"
BWRAP_SHA256 = "0abea81db798ebf6b4742ac0664802d97521547a353c2a0dbdc21d76cbbfd2c0"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MATHLIB_REMOTE = "https://github.com/leanprover-community/mathlib4.git"
LICENSE_SHA256 = "b40930bbcf80744c86c46a12bc9da056641d722716c378f5659b9e555ef833e1"
WILSON_SOURCE = Path("Mathlib/NumberTheory/Wilson.lean")
WILSON_SOURCE_SHA256 = "7bd6ec0e909f037f8632e1b495f9647a61fe950f3bfe3af98a5a22914622aeb7"
WILSON_BLOB = "9401f7b96b43c2c0afa1f823857bd31a20ae0ac2"
WILSON_OLEAN_SHA256 = "c932050e2dca74d0ba033d36338122b2927bad7800f2ac592a20daf42c91d9eb"
WILSON_BODY_SHA256 = "b1c47ff748ace891eec5f93cf3b95c777a338a730d71e0dcbcfe8d3d96328116"
CHARACTERIZATION_BODY_SHA256 = "a356d16cbc838fd9579f8aa1f9102381ab47a0497084cd5450ea6d6715196a87"
FINITE_SOURCE = Path("Mathlib/FieldTheory/Finite/Basic.lean")
FINITE_SOURCE_SHA256 = "808bb4eddb8a4b48785e4430f944fe0827c96842dffa0c08cd21b5659bd85d44"
FINITE_BLOB = "fb3668d594f865e52f20c8af45e91e7e3b1eebd8"
FINITE_OLEAN_SHA256 = "4cede73b3c7f85692307990d9cdaf819b5ac61dc50272e31586b7899d9f32119"
FINITE_BODY_SHA256 = "eb9bedbdb8508c6a10c8de64ca751270c6a844fcd69190bfe460b2090a105b66"
EXPECTED_INPUTS = {
    "README.md": "f7632ce212b08df5088d309424e7f1cb21661d6031e09aa1d5f6c399d2597c75",
    "Statement.lean": "3903de3f1e1cdd6d2f048917005da8f2b744d6726507d09120661e79d217dff9",
    "ObligationTree.lean": "9e2b7bfb61e395c370870fa465469358d7380328bd17f513fdce3305939006b0",
    "Proof.lean": "265924bd8debdd56d0ce411c98943cd75f85d69f800a405919f7603ad8e67923",
    "proof-receipt.json": "c0acb3a31e99fa216f0571a34f1587ad9df8fb16e7789bd5daaedef9df404c2a",
    "instance.json": "3bcd14d6c1bccdbfdbc16dbb5afc4ca1b3d22b2ce1e1ac6be75a2fa8f5cf35d2",
    "statement.json": "33dd21aa1be6e4d648d9c6faf28b992660522b7b403d90f39d99523b461dd25f",
    "task-dag.json": "fca75897e1216948d8dc0236335fc9c94f704edbf95e4c42c6547779d399dd5c",
    "anchor-audit.json": "5451205a7be624b019b9d8154fb6a42227006606a21578bdccf5bdba6d9eaddf",
    "obligation-registry.json": "68bbd16f469a5a8265730e709ba17f7353a87345170783de328ab987e66ed666",
    "typed-graphs.json": "56f413b974d8e205a4b57469c47a81580bffd484358e94e07ce4e2fc47508904",
    "validation-specs.json": "ef7c9cb15c65387522bfa77f629f267f7438bdb9e16f0e84ab4c1d599fffea08",
}
MACHINE_IDS = [
    "M0476-ROOT", "M0476-S-INTERFACE", "M0476-S-BOUNDARY",
    "M0476-S-FACT-TRANSPORT", "M0476-S-FOUNDATION", "M0476-T-COMPOSE",
    "M0476-L-WILSON", "M0476-N-FACTORIAL-PRODUCT",
    "M0476-L-FACTORIAL-INTERVAL", "M0476-T-NAT-CAST-PRODUCT",
    "M0476-N-PRIME-ENDPOINT", "M0476-C-RESIDUE-UNITS-BIJECTION",
    "M0476-B-UNIT-VAL-RANGE", "M0476-L-UNIT-VAL-INJECTIVE",
    "M0476-C-RESIDUE-TO-UNIT", "M0476-T-REPRESENTATIVE-COE",
    "M0476-L-UNITS-PRODUCT", "M0476-C-INVERSE-PAIRING",
    "M0476-L-INVERSE-FIXED-POINTS", "M0476-T-INSERT-NEGONE",
    "M0476-T-UNITS-COE-NEGONE", "M0476-X-PROVENANCE", "M0476-X-TRUST",
]
PROVISIONAL_PROOF_IDS = [
    value for value in MACHINE_IDS
    if value not in {
        "M0476-S-INTERFACE", "M0476-S-BOUNDARY", "M0476-S-FOUNDATION",
        "M0476-X-PROVENANCE", "M0476-X-TRUST",
    }
]
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/README.md",
    f"Stage1_Instances/{THEOREM}/Validation.lean",
    f"Stage1_Instances/{THEOREM}/check_validation.py",
    f"Stage1_Instances/{THEOREM}/check_validation.sh",
    f"Stage1_Instances/{THEOREM}/instance.json",
    f"Stage1_Instances/{THEOREM}/validation-phase.md",
    f"Stage1_Instances/{THEOREM}/validation-receipt.json",
    f"Stage1_Instances/{THEOREM}/validation-spec.json",
}
SUMMARY_LINES = (
    "PASS S56-M-0476-VALIDATION: exact statement, frozen composition, direct and expanded proof roots kernel-replayed",
    "PASS differential replay: exact root reconstructed from the stronger pinned Wilson characterization",
    "PASS trust observation: checked declarations are sorry-free and use only propext, Classical.choice, and Quot.sound",
    "PASS selected provenance: frozen hashes, clean mathlib pin/tree, terminal sources, body slices, oleans, remote, and license agree",
    "PASS network isolation: Lean ran with a read-only host root, fresh writable output directory, and unshared network namespace",
    "BLOCKED proof dependency: S56-M-0476-PROOF is provisional rather than master-accepted",
    "BLOCKED foundation/provenance: complete transitive declaration and TCB/SBOM closure is absent",
    "BLOCKED hermetic gate: shared warm canonical .lake is not a clean-checkout empty-cache offline replay",
    "BLOCKED independent gate: differential source ran in this worker and shared cache, not a distinct signed runner",
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sha256_lines(path: Path, start: int, end: int) -> str:
    lines = path.read_bytes().splitlines(keepends=True)
    return hashlib.sha256(b"".join(lines[start - 1:end])).hexdigest()


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict), path
    return value


def run(
    argv: list[str],
    *,
    cwd: Path = ROOT,
    check: bool = True,
    env: dict[str, str] | None = None,
) -> subprocess.CompletedProcess[str]:
    completed = subprocess.run(
        argv,
        cwd=cwd,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=600,
        check=False,
    )
    if check and completed.returncode:
        raise RuntimeError(f"command failed ({completed.returncode}): {argv!r}\n{completed.stdout}")
    return completed


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["git", *args], cwd=cwd).stdout.strip()


def code_without_comments(source: str) -> str:
    source = re.sub(r"/-.*?-/", "", source, flags=re.DOTALL)
    return re.sub(r"--.*$", "", source, flags=re.MULTILINE)


def assert_text_hygiene(path: Path) -> None:
    data = path.read_bytes()
    assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data, path
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines()), path


def main() -> None:
    spec = load(HERE / "validation-spec.json")
    receipt = load(HERE / "validation-receipt.json")
    statement = load(HERE / "statement.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    proof_receipt = load(HERE / "proof-receipt.json")
    instance = load(HERE / "instance.json")
    task_dag = load(HERE / "task-dag.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item == {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 1357,
        "phase": "validation",
        "layer": 5,
        "state": "[ ]",
        "depends_on": ["S56-M-0476-PROOF"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Run hermetic kernel, trust, provenance, and independent validation gates.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }
    predecessor = next(row for row in execution["items"] if row["id"] == "S56-M-0476-PROOF")
    assert predecessor["state"] == "[_]"
    local_task = next(row for row in task_dag["tasks"] if row["id"] == ITEM)
    assert local_task["state"] == "open" and local_task["authoritative_state"] == "[ ]"
    assert task_dag["accepted_states"] == []

    assert statement["canonical_formal_target"]["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert statement["canonical_formal_target"]["statement_file_sha256"] == sha256(HERE / "Statement.lean")
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert proof_receipt["canonical_target_expression_sha256"] == EXPRESSION_SHA256
    assert proof_receipt["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert proof_receipt["provisionally_closed_proof_obligation_ids"] == PROVISIONAL_PROOF_IDS
    assert proof_receipt["result"]["root_kernel_closed"] is True
    assert proof_receipt["accepted"] is False
    assert graphs["closure_boundary"]["root_closed"] is False
    assert registry["status_observed_after_freeze"]["accepted_closed_obligations"] == []
    assert instance["root_vector"] == {"H": "H1", "M": "M3", "R": "R4"}
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == []
    assert instance["audit_complete"] is instance["theorem_complete"] is False
    assert set(instance["owned_artifacts"]) == {path.name for path in HERE.iterdir() if path.is_file()}

    for name, expected in EXPECTED_INPUTS.items():
        assert sha256(HERE / name) == expected, f"stale input: {name}"
        assert receipt["inputs"][name] == expected, name
    for name in ("Validation.lean", "check_validation.sh", "validation-spec.json", "check_validation.py"):
        assert receipt["inputs"][name] == sha256(HERE / name), name

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
    for forbidden in ("import Proof", "import ObligationTree", "Proof.", "factWilsonAnchor"):
        assert forbidden not in differential, forbidden
    assert "Nat.prime_iff_fac_equiv_neg_one hp.ne_one" in differential
    assert "assert_no_sorry wilsonTheorem_via_primeCharacterization" in differential

    manifest = load(LEAN_ROOT / "lake-manifest.json")
    mathlib_entry = next(row for row in manifest["packages"] if row["name"] == "mathlib")
    assert mathlib_entry["rev"] == mathlib_entry["inputRev"] == MATHLIB_REVISION
    assert sha256(LEAN_ROOT / "lean-toolchain") == (
        "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2"
    )
    assert sha256(LEAN_ROOT / "lake-manifest.json") == (
        "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81"
    )
    assert MATHLIB.resolve().is_dir(), "canonical pinned mathlib artifact missing"
    assert git("rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert git("remote", "get-url", "origin", cwd=MATHLIB) == MATHLIB_REMOTE
    assert git("status", "--porcelain=v1", cwd=MATHLIB) == ""
    assert sha256(MATHLIB / "LICENSE") == LICENSE_SHA256

    provenance = receipt["provenance"]
    for relative, source_hash, blob, olean_hash in (
        (WILSON_SOURCE, WILSON_SOURCE_SHA256, WILSON_BLOB, WILSON_OLEAN_SHA256),
        (FINITE_SOURCE, FINITE_SOURCE_SHA256, FINITE_BLOB, FINITE_OLEAN_SHA256),
    ):
        source = MATHLIB / relative
        olean = MATHLIB / ".lake/build/lib/lean" / relative.with_suffix(".olean")
        assert sha256(source) == source_hash
        assert git("rev-parse", f"HEAD:{relative}", cwd=MATHLIB) == blob
        assert sha256(olean) == olean_hash
        assert provenance["origins"][str(relative)]["source_sha256"] == source_hash
        assert provenance["origins"][str(relative)]["source_git_blob"] == blob
        assert provenance["origins"][str(relative)]["olean_sha256"] == olean_hash
        assert prohibited.search(code_without_comments(source.read_text(encoding="utf-8"))) is None
    assert sha256_lines(MATHLIB / WILSON_SOURCE, 43, 68) == WILSON_BODY_SHA256
    assert sha256_lines(MATHLIB / WILSON_SOURCE, 85, 100) == CHARACTERIZATION_BODY_SHA256
    assert sha256_lines(MATHLIB / FINITE_SOURCE, 110, 117) == FINITE_BODY_SHA256
    assert provenance["terminal_body_identities"] == {
        "ZMod.wilsons_lemma:lines-43-68": f"sha256:{WILSON_BODY_SHA256}",
        "Nat.prime_characterization:lines-85-100": f"sha256:{CHARACTERIZATION_BODY_SHA256}",
        "FiniteField.prod_univ_units_id_eq_neg_one:lines-110-117": f"sha256:{FINITE_BODY_SHA256}",
    }
    assert provenance["license_sha256"] == LICENSE_SHA256

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
    version = run([str(LEAN_BIN), "--version"]).stdout
    assert "4.29.0" in version and LEAN_COMMIT in version

    recipe_env = os.environ.copy()
    recipe_env.update(spec["env_allowlist"])
    lean_output = run(["bash", str(HERE / "check_validation.sh")], env=recipe_env).stdout
    assert lean_output.count("Declarations are sorry-free!") == 25
    assert "sorryAx" not in lean_output and "declaration uses 'sorry'" not in lean_output
    assert hashlib.sha256(lean_output.encode("utf-8")).hexdigest() == (
        "06d60bc8482b2b2026ce5900c765fe635fd8ed3b836af7003675e2159ef73699"
    )
    assert len(lean_output.encode("utf-8")) == 10563

    assert spec["schema_version"] == "stage1-validation-recipe/1.0"
    assert spec["item_id"] == ITEM and spec["theorem_id"] == THEOREM
    assert spec["cwd"] == "."
    assert spec["argv"] == ["python3", "-B", f"Stage1_Instances/{THEOREM}/check_validation.py"]
    assert spec["env_allowlist"] == {
        "HOME": "/home/sansha-2",
        "PATH": "/home/sansha-2/.local/bin:/home/sansha-2/.elan/bin:/usr/local/bin:/usr/bin:/bin",
        "LANG": "C.UTF-8",
        "LC_ALL": "C.UTF-8",
        "TZ": "UTC",
    }
    assert spec["timeout_seconds"] == 600
    assert spec["network_policy"] == "denied" and spec["expected_exit"] == 0
    assert spec["observed_exit"] == 0
    assert "read-only host root" in spec["network_enforcement"]
    assert spec["covered_obligation_ids"] == MACHINE_IDS
    assert spec["expected_outputs"] == [{
        "path_or_stream": "stdout",
        "semantic_hash_policy": "exact nine-line PASS/FAIL-CLOSED status summary",
    }]

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["phase"] == "validation" and receipt["intent"] == "validate"
    assert receipt["depends_on"] == ["S56-M-0476-PROOF"]
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["release_grade"] is receipt["content_addressed_release_evidence"] is False
    assert receipt["canonical_target"] == {
        "declaration": "Stage1Instances.THM_M_0476.WilsonTheoremTarget",
        "elaborated_expression_sha256": EXPRESSION_SHA256,
        "registry_denominator_sha256": DENOMINATOR_SHA256,
    }
    assert receipt["covered_obligation_ids"] == MACHINE_IDS
    assert receipt["accepted_closed_obligation_ids"] == []
    for key in (
        "recipe_id", "cwd", "argv", "env_allowlist", "timeout_seconds",
        "network_policy", "network_enforcement", "expected_exit", "expected_outputs",
        "covered_obligation_ids", "covered_declarations", "scope_boundary",
    ):
        assert receipt["recipe"][key] == spec[key], key
    environment = receipt["environment"]
    assert environment["platform"] == f"{platform.system()} {platform.release()} {platform.machine()}"
    assert environment["lean_executable_sha256"] == LEAN_BIN_SHA256
    assert environment["lake_executable_sha256"] == LAKE_BIN_SHA256
    assert environment["python_executable_sha256"] == PYTHON_SHA256
    assert environment["git_executable_sha256"] == GIT_SHA256
    assert environment["bubblewrap_executable_sha256"] == BWRAP_SHA256
    assert environment["mathlib_revision"] == MATHLIB_REVISION
    assert environment["mathlib_tree"] == MATHLIB_TREE
    assert environment["lean_toolchain_sha256"] == sha256(LEAN_ROOT / "lean-toolchain")
    assert environment["lake_manifest_sha256"] == sha256(LEAN_ROOT / "lake-manifest.json")

    result = receipt["result"]
    assert result["exact_root_kernel_replay"] == "provisional_pass"
    assert result["differential_exact_root_replay"] == "provisional_pass_same_worker"
    assert result["observed_axioms"] == ["Classical.choice", "Quot.sound", "propext"]
    assert result["placeholder_and_unsafe_scan"] == "pass"
    assert result["selected_provenance"] == "pass"
    assert result["network_isolated_lean_replay"] == "pass"
    assert result["proof_master_acceptance"] == "fail_closed"
    assert result["foundation_and_complete_trust_closure"] == "fail_closed"
    assert result["hermetic_cold_offline_replay"] == "fail_closed"
    assert result["independent_distinct_runner"] == "fail_closed"
    assert result["accepted_root_machine_debt"] == "M3"
    assert result["accepted_root_closed"] is False
    assert result["audit_complete"] is result["theorem_complete"] is False
    assert result["semantic_output_sha256"] == hashlib.sha256(
        "\n".join(SUMMARY_LINES).encode("utf-8")
    ).hexdigest()
    assert result["lean_replay_stdout_sha256"] == hashlib.sha256(
        lean_output.encode("utf-8")
    ).hexdigest()
    assert result["lean_replay_stdout_bytes"] == len(lean_output.encode("utf-8"))
    assert receipt["first_failed_gate"] == "dependency.S56-M-0476-PROOF.master_acceptance"
    assert receipt["first_failed_release_gate"] == "S56-10.6-HERMETIC-COLD-BUILD"
    assert receipt["started_at"] < receipt["ended_at"] == receipt["validated_at"]
    assert hashlib.sha256("?? Formalizations/Lean/.lake\n".encode("utf-8")).hexdigest() == (
        receipt["base_worktree"]["initial_status_sha256"]
    )
    assert (ROOT / "Formalizations/Lean/.lake").is_symlink()
    assert str((ROOT / "Formalizations/Lean/.lake").resolve()) == (
        receipt["base_worktree"]["preexisting_lake_symlink_target"]
    )
    assert hashlib.sha256(
        receipt["base_worktree"]["preexisting_lake_symlink_target"].encode("utf-8")
    ).hexdigest() == receipt["base_worktree"]["preexisting_lake_symlink_target_sha256"]
    assert receipt["base_worktree"] == {
        "release_clean": False,
        "initial_status": ["?? Formalizations/Lean/.lake"],
        "initial_status_sha256": "8c616a936e1f6b2689a8955b4904494d5639a105b14cc0154b8805f96d28e97e",
        "tracked_patch_sha256_before_validation": (
            "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
        ),
        "preexisting_untracked_paths": ["Formalizations/Lean/.lake"],
        "preexisting_lake_symlink_target": (
            "/home/sansha-2/external/awesome_theorems/Formalizations/Lean/.lake"
        ),
        "preexisting_lake_symlink_target_sha256": (
            "e8714e9ebb75a5da1eeb16fdb6f50831a6cab29f115df43fa8e7535b38f59826"
        ),
        "classification": (
            "nonrelease worker clone with an automation-provided untracked canonical .lake symlink"
        ),
    }

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
        line[3:] if line[:2] == "??" else line[2:].lstrip()
        for line in status.splitlines()
        if (line[3:] if line[:2] == "??" else line[2:].lstrip()) != "Formalizations/Lean/.lake"
    }
    assert actual_changed == CHANGED_PATHS, (actual_changed, CHANGED_PATHS)
    phase_notes = (HERE / "validation-phase.md").read_text(encoding="utf-8")
    assert "audit_complete=false" in phase_notes and "theorem_complete=false" in phase_notes
    assert "same-worker differential" in phase_notes and "empty-cache" in phase_notes
    for relative in CHANGED_PATHS:
        assert_text_hygiene(ROOT / relative)

    print("\n".join(SUMMARY_LINES))


if __name__ == "__main__":
    main()
