#!/usr/bin/env python3
"""Fail-closed narrow validation for S56-M-0487-VALIDATION."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import platform
import pwd
import re
import shutil
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0487"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM = "S56-M-0487-VALIDATION"
THEOREM = "THM-M-0487"
BASE_REVISION = "9d50d838c8132b2aaf005a4863baeb5385e52a97"
BASE_TREE = "ef268baf236c1fe55806a57847c7f78ed6587b9d"
LEAN_TOOLCHAIN = "leanprover/lean4:v4.29.0"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
LEAN_SHA256 = "3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf"
LAKE_SHA256 = "a608ff084d7e2af228b92a29d7c2fd083ba0580e46889175ec74a81678c98359"
BWRAP_SHA256 = "0abea81db798ebf6b4742ac0664802d97521547a353c2a0dbdc21d76cbbfd2c0"
PYTHON_SHA256 = "b8d8288faefdd300201f43fcf00f6f539a27218eeed3a3dff5ab10b9c4c99700"
TOOLCHAIN_SHA256 = "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2"
MANIFEST_SHA256 = "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MATHLIB_REMOTE = "https://github.com/leanprover-community/mathlib4.git"
MATHLIB_LICENSE_SHA256 = "b40930bbcf80744c86c46a12bc9da056641d722716c378f5659b9e555ef833e1"
STATEMENT_EXPRESSION_SHA256 = (
    "29ac94dd615869191754270061d8fe7123991d403a07bbdf27a09f706665e703"
)
DENOMINATOR_SHA256 = "1d456b6ecd31a58a47bac58a2746bc0f8d16ce4b4e2821348331c511e21c1a41"
SOURCE_HASHES = {
    "Statement.lean": "9d0200046173c0b0d9d0b52cbf696087f4beea6946c92bfa41f03402a4090b0d",
    "ObligationTree.lean": "296af72935ce926686387ce60385a6565831c49029be2a70e1d93025cbd338f8",
    "Proof.lean": "b6257c8fb81fed20ce32c9c15392066a9dfd56e8e96469ca38e12d14689149be",
    "Validation.lean": "24367c2e40260d4329f9281cdd17fc34ddd94712686e58c235da89c563b4f223",
    "statement.json": "9c1088a26cf9eb7bb80753fb900aa189a14bfa0c8a39080325526758b8966247",
    "anchor-audit.json": "569ce7bc7b56c01ae6a8a57f03071e2d95d0bc01aeae28cdd2181217f8a99f36",
    "obligation-registry.json": "6fc1d3df9c49ffcd837ebe26d1a0f9c751480058585985150ff3cdb30086052f",
    "typed-graphs.json": "c3195f3fefd420fadd3875900db9fbb1a86d2bea3d876082e1325d2e369ba236",
    "obligation-tree-receipt.json": "9e03e6556ac99e463e076cf646d5b6eef9a2fd796fee0a0ce3748c004975946d",
    "proof-receipt.json": "d5a5fce77e4dcfbf7e67e2df42d686c5f9c7e61f9bb4c536245907024e601a5e",
    "proof-blocker-current.json": "a84d3920035e7a6aa993df21d650d8bbc77dada4debd6472e89ea536dba2471c",
    "validation-specs.json": "03847d197c034dddec99180a830678daf8fd2a54e8c09700b153da9b559a6773",
    "source-statement-crosswalk.md": "11bc2b4d59fca275412236f32a4b93153e3fc7f6cd1600ca6e6962c57c98eb92",
    "validation-spec.json": "2589c11c75152f01a3c953f07b88e95f1051ae1e5e33781af302b4e703bd2399",
}
SELECTED_PROVENANCE = {
    "Mathlib/Data/Finset/Prod.lean": (
        "9161ff8ee434b8cb3305ad4a86ceb8dfc7d4dd7d",
        "2cdc3c68d117332b7e947e3628a3903cd3a94cbed37764fe05f402966a979744",
        "17246154756657153ca03c888df021501b2befe866bc410c644e3084a20a69eb",
    ),
    "Mathlib/Data/Nat/Prime/Defs.lean": (
        "4c6a3aa35c4fb21f9c55ee336bc5442cb788de35",
        "fb7b8f26c48fdb96c39d264574b70ba382d700a9a97a06ee41bb05377dfc68a4",
        "21bc4f08455ebc7d1f42cceaffea7c043552fc496fb81564b60974b015be0cb0",
    ),
    "Mathlib/Algebra/Ring/Int/Parity.lean": (
        "f76417731fb39a10c7fe4aca34ef2b1c9cedecc9",
        "d3d4c39ee9a880a9da780c09807fa1e7f612cb2813454716edac0b69da2163f4",
        "65cf777fe4458676fd756cb84c35a51a3267563a909367937b3fbaabbfcecd41",
    ),
}
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
EXPECTED_STDOUT = (
    "PASS S56-M-0487-VALIDATION: network-isolated lake env lean --trust=0 "
    "fresh-output replay checked the exact statement, conditional compositions, and two "
    "partial finite-count interfaces\n"
    "PASS trust: both proof declarations are sorry-free and report exactly propext, "
    "Classical.choice, and Quot.sound\n"
    "PASS selected provenance: frozen inputs, clean mathlib pin/origin/license, direct "
    "source/olean hashes, and tool identities agree\n"
    "OPEN exact root: M0487-T-ANALYTIC and M0487-T-FINITE-UPPER remain the minimal cut; "
    "zero obligations are accepted closed\n"
    "FAIL CLOSED predecessor recipes: the frozen 54-recipe runner is snapshot-stale after "
    "integration\n"
    "FAIL CLOSED release: warm shared cache is not cold hermetic evidence, and this trust "
    "probe is not distinct-runner verification\n"
    "audit_complete=false; theorem_complete=false\n"
)
PROOF_DECLARATIONS = (
    "Stage1Instances.THM_M_0487.Proof.representationCount_pos_iff",
    "Stage1Instances.THM_M_0487.Proof.weakGoldbachTarget_iff_positiveRepresentationCountTarget",
)
COMPOSITION_DECLARATIONS = (
    "Stage1Instances.THM_M_0487.ObligationTree.threePrimeRepresentation_iff",
    "Stage1Instances.THM_M_0487.ObligationTree.cutoff_cases",
    "Stage1Instances.THM_M_0487.ObligationTree.analyticCutoff_le_publishedFiniteUpper",
    "Stage1Instances.THM_M_0487.ObligationTree.finiteCoverage_of_publishedUpper",
    "Stage1Instances.THM_M_0487.ObligationTree.finiteRange_of_publishedFiniteUpper",
    "Stage1Instances.THM_M_0487.ObligationTree.root_of_analytic_and_finite",
    "Stage1Instances.THM_M_0487.ObligationTree.root_iff_analytic_and_finite",
)
ROOT_CUT = ["M0487-T-ANALYTIC", "M0487-T-FINITE-UPPER"]
RECIPE_PATH = "/usr/bin:/bin"
RECIPE_ARGV = [
    "/usr/bin/bwrap", "--ro-bind", "/", "/", "--dev", "/dev",
    "--proc", "/proc", "--tmpfs", "/tmp", "--unshare-net",
    "--die-with-parent", "--clearenv", "--setenv", "HOME", "/tmp",
    "--setenv", "PATH", RECIPE_PATH, "--setenv", "LANG", "C.UTF-8",
    "--setenv", "LC_ALL", "C.UTF-8", "--setenv", "TZ", "UTC",
    "--setenv", "LEAN_NUM_THREADS", "1", "/usr/bin/python3", "-I", "-B",
    f"Stage1_Instances/{THEOREM}/check_validation.py",
]
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/Validation.lean",
    f"Stage1_Instances/{THEOREM}/check_validation.py",
    f"Stage1_Instances/{THEOREM}/validation-blocker.json",
    f"Stage1_Instances/{THEOREM}/validation-phase.md",
    f"Stage1_Instances/{THEOREM}/validation-receipt.json",
    f"Stage1_Instances/{THEOREM}/validation-spec.json",
}
KNOWN_FAILURES = [
    "The proof prerequisite is provisional and incomplete: its receipt closes no frozen obligation and supplies no exact weak Goldbach root body.",
    "M0487-T-ANALYTIC has no placeholder-free analytic-range positivity proof, and M0487-T-FINITE-UPPER independently lacks admitted finite data, certificates, and a sound kernel replay.",
    "The 54 frozen predecessor recipes are snapshot-bound to an obsolete checker base/DAG state; their old runner now fails freshness even though this validator freshly replays the underlying Lean declarations.",
    "The foundation profile, complete transitive declaration provenance, imported compiled-object inventory, compiler/bootstrap, supply-chain, SBOM, and TCB closure are not accepted.",
    "The run uses a network namespace and read-only host, but reuses the shared warm canonical .lake artifacts; it is not a clean-checkout cold empty-cache offline archive replay.",
    "Validation.lean is a same-worker trust probe, not a second signed distinct-runner attestation or independently implemented minimal verifier.",
    "Primary-source H0, readable R0, AUDIT-Z, THEOREM-Z, release reconciliation, and master acceptance remain open.",
    "The target-local task-dag.json is a stale planned/open projection and has not been rewritten by this validation worker.",
]


if not __debug__:
    raise RuntimeError("validation requires Python assertions")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path: Path) -> dict:
    def reject_duplicates(pairs: list[tuple[str, object]]) -> dict:
        value: dict[str, object] = {}
        for key, item in pairs:
            assert key not in value, f"duplicate JSON key in {path}: {key}"
            value[key] = item
        return value

    result = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicates)
    assert isinstance(result, dict), path
    return result


def run(
    argv: list[str], *, cwd: Path = ROOT, env: dict[str, str] | None = None,
    timeout: int = 600, expected_exit: int = 0,
) -> str:
    result = subprocess.run(
        argv, cwd=cwd, env=env, text=True, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, timeout=timeout, check=False,
    )
    if result.returncode != expected_exit:
        raise RuntimeError(
            f"command exited {result.returncode}, expected {expected_exit}: {argv!r}\n{result.stdout}"
        )
    return result.stdout


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["/usr/bin/git", *args], cwd=cwd).rstrip()


def source_without_comments(source: str) -> str:
    output: list[str] = []
    index = 0
    depth = 0
    while index < len(source):
        if depth == 0 and source.startswith("--", index):
            newline = source.find("\n", index)
            if newline < 0:
                break
            output.append("\n")
            index = newline + 1
        elif source.startswith("/-", index):
            depth += 1
            index += 2
        elif depth and source.startswith("-/", index):
            depth -= 1
            index += 2
        elif depth:
            if source[index] == "\n":
                output.append("\n")
            index += 1
        else:
            output.append(source[index])
            index += 1
    assert depth == 0, "unterminated Lean block comment"
    return "".join(output)


def reported_axioms(output: str, declaration: str) -> set[str]:
    no_axioms = f"'{declaration}' does not depend on any axioms"
    pattern = re.compile(
        re.escape(f"'{declaration}' depends on axioms: [") + r"(.*?)]", re.DOTALL
    )
    matches = pattern.findall(output)
    assert output.count(no_axioms) + len(matches) == 1, declaration
    if not matches:
        return set()
    return {part.strip() for part in matches[0].split(",") if part.strip()}


def canonical_json_id(document: dict, omitted_field: str) -> str:
    body = dict(document)
    body.pop(omitted_field, None)
    payload = json.dumps(body, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return "sha256:" + hashlib.sha256(payload).hexdigest()


def assert_text_hygiene(path: Path) -> None:
    data = path.read_bytes()
    assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines()), path


def main() -> None:
    spec = load(HERE / "validation-spec.json")
    statement = load(HERE / "statement.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    instance = load(HERE / "instance.json")
    frozen_specs = load(HERE / "validation-specs.json")
    proof_receipt = load(HERE / "proof-receipt.json")
    proof_blocker = load(HERE / "proof-blocker-current.json")
    execution = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")
    targets = load(ROOT / "Docs" / "Stage1_Targets_rev-5.6.json")
    receipt_path = HERE / "validation-receipt.json"
    receipt = load(receipt_path) if receipt_path.exists() else None
    blocker_path = HERE / "validation-blocker.json"
    blocker = load(blocker_path) if blocker_path.exists() else None
    verify_outputs = os.environ.get("STAGE1_SKIP_OUTPUT_CHECK") != "1"

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target == {
        "execution_rank": 1366,
        "legacy_priority_slot": None,
        "theorem_id": THEOREM,
        "name": "弱哥德巴赫猜想",
        "category": "数论 / 初等数论",
        "source_status_untrusted": "已验证",
        "baseline": "L0",
        "rework_required": True,
        "legacy_artifacts_accepted": False,
        "target_lane": "hard_statement_first_partial_verification",
        "intake_score": 86,
        "lifecycle_mode": "planned",
        "theorem_complete": False,
    }
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item == {
        "id": ITEM, "theorem_id": THEOREM, "execution_rank": 1366,
        "phase": "validation", "layer": 5, "state": "[ ]",
        "depends_on": ["S56-M-0487-PROOF"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Run hermetic kernel, trust, provenance, and independent validation gates.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0, "children": [],
    }
    predecessor = next(row for row in execution["items"] if row["id"] == "S56-M-0487-PROOF")
    assert predecessor["state"] == "[_]" and predecessor["attempts"] == 1

    assert spec["schema_version"] == "stage1-validation-spec/1.0"
    assert spec["item_id"] == ITEM and spec["theorem_id"] == THEOREM
    assert spec["argv"] == RECIPE_ARGV and spec["cwd"] == "."
    assert spec["env_allowlist"] == {
        "HOME": "/tmp", "PATH": RECIPE_PATH, "LANG": "C.UTF-8",
        "LC_ALL": "C.UTF-8", "TZ": "UTC", "LEAN_NUM_THREADS": "1",
    }
    assert spec["timeout_seconds"] == 720 and spec["network_policy"] == "denied"
    assert spec["expected_exit"] == 0 and len(spec["expected_outputs"]) == 1
    assert set(spec["covered_obligation_ids"]) == set(
        graphs["closure_boundary"]["interface_checked_obligations"]
    )
    assert set(spec["covered_declarations"]) == {
        "Stage1Instances.THM_M_0487.WeakGoldbachTarget",
        *COMPOSITION_DECLARATIONS,
        *PROOF_DECLARATIONS,
    }

    for name, digest in SOURCE_HASHES.items():
        assert sha256(HERE / name) == digest, f"bound validation input changed: {name}"
    canonical = statement["canonical_formal_target"]
    assert canonical["statement_file_sha256"] == SOURCE_HASHES["Statement.lean"]
    assert canonical["elaborated_expression_sha256"] == STATEMENT_EXPRESSION_SHA256
    assert registry["root_obligation_id"] == graphs["root_obligation_id"] == "M0487-ROOT"
    assert registry["denominator_sha256"] == graphs[
        "registry_denominator_sha256"
    ] == DENOMINATOR_SHA256
    assert instance["lifecycle_mode"] == "planned"
    assert instance["root_vector"] == {"H": "H1", "M": "M3", "R": "R3"}
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == []
    assert instance["audit_complete"] is instance["theorem_complete"] is False
    closure = graphs["closure_boundary"]
    assert closure["accepted_closed_obligations"] == []
    assert closure["root_closed"] is False and closure["root_machine_debt"] == "M3"
    assert closure["minimal_open_proof_cut_sets"] == [ROOT_CUT]
    assert closure["audit_complete"] is closure["theorem_complete"] is False

    assert frozen_specs["item_id"] == "S56-M-0487-OBLIGATION_TREE"
    assert len(frozen_specs["recipes"]) == len(registry["obligations"]) == 54
    assert {tuple(row["argv"]) for row in frozen_specs["recipes"]} == {
        ("python3", "-B", f"Stage1_Instances/{THEOREM}/check_obligation_tree.py")
    }
    old_checker = (HERE / "check_obligation_tree.py").read_text(encoding="utf-8")
    assert 'BASE_REVISION = "b56df790fc94c5366cf919a6fe5411d06b427c59"' in old_checker
    assert '"phase": "obligation_tree", "layer": 3, "state": "[ ]"' in old_checker

    assert proof_receipt["support_state"] == "provisional_worker_selftest"
    assert proof_receipt["proposed_state"] == "[_]" and proof_receipt["accepted"] is False
    assert proof_receipt["proof_body"]["source_sha256"] == SOURCE_HASHES["Proof.lean"]
    assert proof_receipt["supported_obligation_ids"] == []
    assert proof_receipt["partial_progress_toward_obligation_ids"] == [
        "M0487-N-REPRESENTATION"
    ]
    assert proof_receipt["provisionally_closed_obligation_ids"] == []
    assert proof_receipt["accepted_closed_obligation_ids"] == []
    assert proof_receipt["result"]["root_kernel_closed"] is False
    assert proof_receipt["result"]["theorem_complete"] is False
    assert proof_receipt["remaining_root_cut_set"] == ROOT_CUT
    assert proof_blocker["remaining_root_cut_set"] == ROOT_CUT
    assert proof_blocker["root_closed"] is False and proof_blocker["theorem_complete"] is False

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by)\b|"
        r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
        r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
        r"(?:axiom|constant|opaque|unsafe|extern)\b",
        re.MULTILINE,
    )
    lean_names = (
        "Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"
    )
    all_source = "\n".join(
        source_without_comments((HERE / name).read_text(encoding="utf-8"))
        for name in lean_names
    )
    assert prohibited.search(all_source) is None
    validation_source = source_without_comments(
        (HERE / "Validation.lean").read_text(encoding="utf-8")
    )
    assert re.search(r"^(?:theorem|def|abbrev|instance)\b", validation_source, re.MULTILINE) is None
    assert validation_source.count("assert_no_sorry ") == len(PROOF_DECLARATIONS)
    for forbidden in ("AnalyticRangePackage :=", "FiniteUpperBoundPackage :=", "WeakGoldbachTarget :="):
        assert forbidden not in validation_source

    manifest = load(LEAN_ROOT / "lake-manifest.json")
    mathlib_entry = next(row for row in manifest["packages"] if row["name"] == "mathlib")
    assert mathlib_entry["rev"] == mathlib_entry["inputRev"] == MATHLIB_REVISION
    assert MATHLIB.resolve().is_dir(), "pinned mathlib artifact is unavailable"
    assert git("rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert git("remote", "get-url", "origin", cwd=MATHLIB) == MATHLIB_REMOTE
    assert git("status", "--porcelain=v1", "--untracked-files=all", cwd=MATHLIB) == ""
    assert sha256(MATHLIB / "LICENSE") == MATHLIB_LICENSE_SHA256
    for source_name, (blob_hash, source_hash, olean_hash) in SELECTED_PROVENANCE.items():
        assert git("rev-parse", f"HEAD:{source_name}", cwd=MATHLIB) == blob_hash
        assert sha256(MATHLIB / source_name) == source_hash
        olean = MATHLIB / ".lake" / "build" / "lib" / "lean" / source_name.replace(
            ".lean", ".olean"
        )
        assert sha256(olean) == olean_hash
    assert sha256(LEAN_ROOT / "lean-toolchain") == TOOLCHAIN_SHA256
    assert sha256(LEAN_ROOT / "lake-manifest.json") == MANIFEST_SHA256

    toolchain_bin = (
        Path(pwd.getpwuid(os.getuid()).pw_dir)
        / ".elan" / "toolchains" / "leanprover--lean4---v4.29.0" / "bin"
    )
    lean = toolchain_bin / "lean"
    lake = toolchain_bin / "lake"
    bwrap = Path("/usr/bin/bwrap")
    python = Path("/usr/bin/python3")
    assert lean.is_file() and lake.is_file() and bwrap.is_file() and python.is_file()
    assert sha256(lean) == LEAN_SHA256 and sha256(lake) == LAKE_SHA256
    assert sha256(bwrap) == BWRAP_SHA256 and sha256(python) == PYTHON_SHA256
    fixed_env = {
        "HOME": os.environ["HOME"], "PATH": f"{toolchain_bin}:/usr/bin:/bin",
        "ELAN_TOOLCHAIN": LEAN_TOOLCHAIN, "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8",
        "TZ": "UTC", "LEAN_NUM_THREADS": "1",
    }
    assert {key: os.environ[key] for key in spec["env_allowlist"]} == spec["env_allowlist"]
    assert LEAN_COMMIT in run([str(lean), "--version"], cwd=LEAN_ROOT, env=fixed_env)
    assert "5.0.0" in run([str(lake), "--version"], cwd=LEAN_ROOT, env=fixed_env)
    compiled_dirs = sorted(
        path.resolve()
        for path in (LEAN_ROOT / ".lake" / "packages").glob("*/.lake/build/lib/lean")
        if path.is_dir()
    )
    root_build = (LEAN_ROOT / ".lake" / "build" / "lib" / "lean").resolve()
    if root_build.is_dir():
        compiled_dirs.insert(0, root_build)
    assert compiled_dirs and any("/mathlib/" in str(path) for path in compiled_dirs)
    lean_path = ":".join(str(path) for path in compiled_dirs)

    temp_root = Path(tempfile.mkdtemp(prefix="stage1-m0487-validation-", dir="/tmp"))
    try:
        target_dir = temp_root / "Stage1_Instances" / THEOREM
        target_dir.mkdir(parents=True)
        for name in lean_names:
            shutil.copy2(HERE / name, target_dir / name)
        (temp_root / "home").mkdir()

        def isolated_lean(name: str, *, module_path: bool) -> str:
            path = f"{target_dir}:{lean_path}" if module_path else lean_path
            args = [
                str(lake), "env", "lean", "--trust=0", "-t0", "--root", str(target_dir),
                "-o", str(target_dir / f"{Path(name).stem}.olean"),
                str(target_dir / name),
            ]
            return run(
                args, cwd=MATHLIB,
                env={
                    **fixed_env, "HOME": str(temp_root / "home"), "LEAN_PATH": path,
                },
                timeout=600,
            )

        statement_output = isolated_lean("Statement.lean", module_path=False)
        obligation_output = isolated_lean("ObligationTree.lean", module_path=True)
        proof_output = isolated_lean("Proof.lean", module_path=True)
        validation_output = isolated_lean("Validation.lean", module_path=True)
        olean_hashes = {
            name: sha256(target_dir / name)
            for name in (
                "Statement.olean", "ObligationTree.olean", "Proof.olean", "Validation.olean"
            )
        }
    finally:
        shutil.rmtree(temp_root)

    for declaration in COMPOSITION_DECLARATIONS:
        assert reported_axioms(obligation_output, declaration) <= EXPECTED_AXIOMS
    for declaration in PROOF_DECLARATIONS:
        assert reported_axioms(proof_output, declaration) == EXPECTED_AXIOMS
        assert reported_axioms(validation_output, declaration) == EXPECTED_AXIOMS
    combined = "\n".join(
        (statement_output, obligation_output, proof_output, validation_output)
    )
    assert "Stage1Instances.THM_M_0487.WeakGoldbachTarget" in statement_output
    assert proof_output.count("Declarations are sorry-free!") == 2
    assert validation_output.count("Declarations are sorry-free!") == 1
    assert "sorryAx" not in proof_output + validation_output
    assert "declaration uses 'sorry'" not in proof_output + validation_output
    assert "error:" not in combined

    if receipt is not None and verify_outputs:
        assert receipt["schema_version"] == "stage1-node-receipt/1.0"
        assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
        assert receipt["depends_on"] == ["S56-M-0487-PROOF"]
        assert receipt["receipt_id"] == canonical_json_id(receipt, "receipt_id")
        assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
        assert receipt["support_state"] == "provisional_worker_selftest"
        assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
        assert receipt["content_addressed"] is False and receipt["release_grade"] is False
        assert receipt["verdict"] == "blocked"
        assert receipt["canonical_target_expression_sha256"] == STATEMENT_EXPRESSION_SHA256
        assert receipt["registry_denominator_sha256"] == DENOMINATOR_SHA256
        for key, name in (
            ("statement_source_sha256", "Statement.lean"),
            ("obligation_tree_source_sha256", "ObligationTree.lean"),
            ("proof_source_sha256", "Proof.lean"),
            ("validation_probe_sha256", "Validation.lean"),
            ("validation_spec_sha256", "validation-spec.json"),
            ("validator_sha256", "check_validation.py"),
            ("statement_record_sha256", "statement.json"),
            ("anchor_audit_sha256", "anchor-audit.json"),
            ("obligation_registry_sha256", "obligation-registry.json"),
            ("typed_graphs_sha256", "typed-graphs.json"),
            ("obligation_tree_receipt_sha256", "obligation-tree-receipt.json"),
            ("proof_receipt_sha256", "proof-receipt.json"),
            ("proof_blocker_sha256", "proof-blocker-current.json"),
            ("frozen_validation_specs_sha256", "validation-specs.json"),
            ("source_crosswalk_sha256", "source-statement-crosswalk.md"),
        ):
            assert receipt["inputs"][key] == sha256(HERE / name), key
        for key in (
            "recipe_id", "cwd", "argv", "env_allowlist", "timeout_seconds",
            "network_policy", "network_enforcement", "expected_exit",
            "covered_obligation_ids", "covered_declarations",
        ):
            assert receipt["recipe"][key] == spec[key]
        result = receipt["result"]
        assert result["exit_code"] == 0
        assert result["stdout_bytes"] == len(EXPECTED_STDOUT.encode("utf-8"))
        assert result["stdout_sha256"] == hashlib.sha256(
            EXPECTED_STDOUT.encode("utf-8")
        ).hexdigest()
        assert result["started_at"] < result["ended_at"] == receipt["validated_at"]
        assert result["duration_seconds"] > 0
        assert result["fresh_olean_sha256"] == olean_hashes
        assert result["revalidated_partial_progress_ids"] == ["M0487-N-REPRESENTATION"]
        assert result["accepted_closed_obligation_ids"] == []
        assert result["root_kernel_closed"] is False
        assert result["root_vector_before"] == result["root_vector_after"] == {
            "H": "H1", "M": "M3", "R": "R3"
        }
        assert result["remaining_root_cut_set"] == ROOT_CUT
        for gate in (
            "proof_dependency_gate", "exact_root_gate", "predecessor_recipe_freshness_gate",
            "complete_transitive_provenance_gate", "complete_transitive_tcb_gate",
            "hermetic_release_gate", "independent_verification_gate",
        ):
            assert result[gate] == "fail_closed"
        assert result["audit_complete"] is result["theorem_complete"] is False
        assert receipt["known_failures"] == KNOWN_FAILURES
        assert receipt["first_failed_gate"] == "dependency.S56-M-0487-PROOF.not_complete"
        assert receipt["first_failed_root_gate"] == "M0487-T-ANALYTIC"
        assert receipt["first_failed_release_gate"] == "S56-10.6-HERMETIC-COLD-EMPTY-CACHE"
        assert receipt["remaining_root_cut_set"] == ROOT_CUT
        assert receipt["accepted_receipt_ids"] == []
        assert set(receipt["changed_paths"]) == CHANGED_PATHS
    if blocker is not None and verify_outputs:
        assert blocker["item_id"] == ITEM and blocker["verdict"] == "blocked"
        assert blocker["blocker_id"] == canonical_json_id(blocker, "blocker_id")
        assert blocker["first_failed_gate"] == "dependency.S56-M-0487-PROOF.not_complete"
        assert blocker["remaining_root_cut_set"] == ROOT_CUT
        assert blocker["known_failures"] == KNOWN_FAILURES

    if verify_outputs:
        packet = load(ROOT / ".stage1-worker-selftest.json")
        assert set(packet) == {
            "item_id", "changed_paths", "commands", "output_summary",
            "base_revision", "known_failures", "state",
        }
        assert packet["item_id"] == ITEM and packet["state"] == "[_]"
        assert packet["base_revision"] == BASE_REVISION
        assert set(packet["changed_paths"]) == CHANGED_PATHS
        assert packet["known_failures"] == KNOWN_FAILURES
        actual_changes = {
            line[3:] for line in git("status", "--short", "--untracked-files=all").splitlines()
        }
        actual_changes.discard("Formalizations/Lean/.lake")
        assert actual_changes == CHANGED_PATHS, (actual_changes, CHANGED_PATHS)
        for relative in CHANGED_PATHS:
            assert_text_hygiene(ROOT / relative)

    assert platform.system() == "Linux"
    print(EXPECTED_STDOUT, end="")


if __name__ == "__main__":
    main()
