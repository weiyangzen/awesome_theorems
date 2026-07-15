#!/usr/bin/env python3
"""Fail-closed release reconciliation for S56-M-1248-RELEASE."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile


if not __debug__:
    raise RuntimeError("release reconciliation requires Python assertions")


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-1248"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
ITEM = "S56-M-1248-RELEASE"
THEOREM = "THM-M-1248"
BASE_REVISION = "d6616cc60ad980c635f22ef840e9c5db2ebcab50"
BASE_TREE = "d6f3c3aedec26191f09878fd6eb1fec666adf318"
TOOLCHAIN = "leanprover/lean4:v4.29.0"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
EXPRESSION_SHA256 = "f6a65804d336bcc7f72d03e35c0e43715fc92c648507b805117a09ec13648d5b"
DENOMINATOR_SHA256 = "a0c3a82c3c3655d323873c8e3dc1164bbe6021d60d32521261f7d82cdcceaa11"
VALIDATION_RECEIPT_SHA256 = "472d101f432a6def388af8426f7c08a496a7328674ed9b37250d61a765ebdf84"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
INVENTORY_IDS = [
    "M1248-ROOT", "M1248-S-DEFS", "M1248-S-ADMISSIBLE", "M1248-S-TEST",
    "M1248-S-FOUNDATION", "M1248-N-PARAM", "M1248-B-A0", "M1248-B-A1",
    "M1248-B-INTERIOR", "M1248-L-WEIGHTED", "M1248-L-HOLDER", "M1248-L-RPOW",
    "M1248-L-ORIGIN", "M1248-T-ALL-PARAMS", "M1248-T-ASSEMBLE",
    "M1248-X-SOURCE", "M1248-X-PROVENANCE", "M1248-X-TRUST",
]
RECONCILED_INPUTS = {
    "README.md": "be283007813150fcf2e1731256a087b63fe3ab101ea94d6af0047dd68caad024",
    "intake.json": "6677f14e0888a5161502fd75ef5088f8cb8ebf9c798ec6f2662beb5efa9fe51d",
    "statement.json": "a787b9e129b16974309d7c0b4a3d7a576eaa7c40a7b11ce1af7c6836318948ba",
    "anchor-audit.json": "2548e53752cf1cffeceb3a288550997500317e8361b6a34ffd9f7b149b3efac5",
    "obligation-registry.json": "2e1d91b7ee8ff66bcad84eeeb3c21b5ca9c0b670274cac11fc929b5b5474841e",
    "typed-graphs.json": "4b4a42007bfbc4789584aac36e47dadf03da31b57b945a328cc6b2c5bd8b3fad",
    "Statement.lean": "e3e257722b165a262b421b602e0a6e898251549b06c8bc65539dc6ebd2403c00",
    "AnchorAudit.lean": "23cce93594ac13d39ef8f552534e35898ae4a622a5d20c490bf5284c5e87bd0c",
    "ObligationTree.lean": "97334a1ed6471cf8b07774a877651930a63292706f8cbb9051f90d46c5eee8dd",
    "Proof.lean": "ff1d55daac75a934bfb807596d424310f080836c02cc13b05c054e81aeac7f13",
    "Validation.lean": "a8b63f2f24b5defe7db9c6cf030a768cacabfa2a38777c95725fdd905ce21c7d",
    "proof-receipt.json": "6edc8ec3c70fee43d04040e47219d4063ddb025fa1a6228991d60843d79a64b8",
    "validation-spec.json": "f8f51506ef0bcd9bbcdaf02800c1f7029d3fbf0ac6b198d7022204b7ab35d87b",
    "validation-receipt.json": VALIDATION_RECEIPT_SHA256,
    "check_validation.py": "53d6b640cb845609faea605c4125aaf32182ab9b8b08b97a5d46a233bfb606d6",
    "validation-phase.md": "ed321053a6de5d847a26372b286c74671aaddb53a8fac301509e142198041c61",
}
AUTHORITY_INPUTS = {
    "Docs/Stage1_Targets_rev-5.6.json": "02eec284de534dd78e1cf75f82a477ff477567dd682b7445cb7587abd137ab2c",
    "Docs/Stage1_Execution_DAG_rev-5.6.json": "a57538aeee6a0ba948bbcc0ca421ce8cf19014e952e8b25d304c2e5517d270ba",
    "Docs/Stage1_Blueprint_rev-5.6.md": "4d1e2a36d95567a14194a24e43f43093e87e8a4feb6d75f8d5f295607ad34b56",
    "Docs/Blueprint_Guidelines.md": "a06c07b5ca1b270b4935ad3dab893e9a0e078c29c8da2ef9dca1e71193310535",
    "skills/execute-stage1-rev56/SKILL.md": "26d47a66c6535feabb8bbf1051fd55d76a53fe761f4b3d953f86b97ec86152b8",
    "Formalizations/Lean/lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "Formalizations/Lean/lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
RELEASE_OUTPUTS = {
    "release-spec.json": "ddddf9e0059d0cff57ca37543495b75dd4a9eaa53cf7fdebe7d4f81d890c75c4",
    "release-decision.json": "9b96d8adcb3b7c05be624573a9d7f23d6d359e9f53feb1c28e4e2d5147973c02",
    "release-receipt.json": "0d66c8a72465c5c014d17be16af469e6b8e667dfa07e5555e5b6caf1f861b9eb",
    "release-validation.md": "d8536438533ea8107816ff1efc22b59f7dfaa631f953ab469757728ec1af12b6",
}
CHANGED_PATHS = [
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/check_release.py",
    f"Stage1_Instances/{THEOREM}/release-decision.json",
    f"Stage1_Instances/{THEOREM}/release-receipt.json",
    f"Stage1_Instances/{THEOREM}/release-spec.json",
    f"Stage1_Instances/{THEOREM}/release-validation.md",
]
SUMMARY_LINES = [
    "PASS S56-M-1248-RELEASE negative reconciliation",
    "PASS fresh trust-zero network-isolated replay: defective frozen root and no-Proof reconstruction",
    "BLOCKED dependency: S56-M-1248-VALIDATION is provisional and not master-accepted",
    "BLOCKED source identity: analytic top/omega and Pi/sup-versus-Euclidean radial mismatches",
    "BLOCKED assurance: AUDIT-Z/H0/R0/trust/cold-offline/SBOM/independent-verifier/bundle gates remain open",
    "verdict=blocked lifecycle=planned root_vector=H1/M3/R3 audit_complete=false theorem_complete=false",
]


def load(path: Path) -> dict:
    def reject_duplicates(pairs: list[tuple[str, object]]) -> dict:
        result: dict[str, object] = {}
        for key, value in pairs:
            assert key not in result, f"duplicate JSON key in {path}: {key}"
            result[key] = value
        return result

    value = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicates)
    assert isinstance(value, dict), path
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


HOME = os.environ["HOME"]
BASE_ENV = {
    "HOME": HOME,
    "PATH": f"{HOME}/.elan/bin:/usr/bin:/bin",
    "ELAN_TOOLCHAIN": TOOLCHAIN,
    "LANG": "C.UTF-8",
    "LC_ALL": "C.UTF-8",
    "TZ": "UTC",
    "LEAN_NUM_THREADS": "1",
}


def run(argv: list[str], *, cwd: Path = ROOT, env: dict[str, str] | None = None,
        timeout: int = 900) -> str:
    result = subprocess.run(
        argv, cwd=cwd, env=env, text=True, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, timeout=timeout, check=False,
    )
    if result.returncode:
        raise AssertionError(f"command failed ({result.returncode}): {argv!r}\n{result.stdout}")
    return result.stdout


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["/usr/bin/git", *args], cwd=cwd, env=BASE_ENV, timeout=60).strip()


def code_without_comments(source: str) -> str:
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
    pattern = re.compile(re.escape(f"'{declaration}' depends on axioms: [") + r"(.*?)]", re.DOTALL)
    matches = pattern.findall(output)
    assert len(matches) == 1, f"missing or duplicate axiom report for {declaration}"
    return {part.strip() for part in matches[0].split(",") if part.strip()}


def assert_text_hygiene(path: Path) -> None:
    data = path.read_bytes()
    assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())


def pinned_lean_path(lean: Path) -> str:
    package_names = (
        "batteries", "Qq", "aesop", "proofwidgets", "importGraph",
        "LeanSearchClient", "plausible", "mathlib",
    )
    roots = [
        (LEAN_ROOT / ".lake" / "packages" / name / ".lake/build/lib/lean").resolve()
        for name in package_names
    ]
    assert all(path.is_dir() for path in roots)
    local = (LEAN_ROOT / ".lake/build/lib/lean").resolve()
    assert local.is_dir()
    return ":".join([*(str(path) for path in roots), str(local), str(lean.parent.parent / "lib/lean")])


def isolated_replay(lean: Path, lean_path: str) -> dict[str, str]:
    with tempfile.TemporaryDirectory(prefix="stage1-m1248-release-", dir="/tmp") as name:
        tmp = Path(name).resolve()
        for source in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
            shutil.copy2(HERE / source, tmp / source)
        (tmp / "home").mkdir()
        base = [
            "/usr/bin/bwrap", "--ro-bind", "/", "/", "--bind", str(tmp), str(tmp),
            "--dev", "/dev", "--proc", "/proc", "--unshare-net", "--die-with-parent",
            "--clearenv", "--setenv", "HOME", str(tmp / "home"), "--setenv", "TMPDIR", str(tmp),
            "--setenv", "LANG", "C.UTF-8", "--setenv", "LC_ALL", "C.UTF-8",
            "--setenv", "TZ", "UTC", "--setenv", "LEAN_NUM_THREADS", "1", "--chdir", str(tmp),
        ]

        def lean_run(source: str, path: str, emit_olean: bool) -> str:
            argv = base + ["--setenv", "LEAN_PATH", path, str(lean), "--trust=0", "-t0", "--root", str(tmp)]
            if emit_olean:
                argv += ["-o", source.replace(".lean", ".olean")]
            argv.append(source)
            return run(argv, timeout=300)

        return {
            "statement": lean_run("Statement.lean", lean_path, True),
            "obligation": lean_run("ObligationTree.lean", f"{tmp}:{lean_path}", True),
            "proof": lean_run("Proof.lean", f"{tmp}:{lean_path}", False),
            "validation": lean_run("Validation.lean", f"{tmp}:{lean_path}", False),
        }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker-packet", type=Path)
    args = parser.parse_args()
    os.umask(0o022)

    decision = load(HERE / "release-decision.json")
    receipt = load(HERE / "release-receipt.json")
    spec = load(HERE / "release-spec.json")
    intake = load(HERE / "intake.json")
    statement = load(HERE / "statement.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    proof = load(HERE / "proof-receipt.json")
    validation = load(HERE / "validation-receipt.json")
    targets = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 428
    assert target["baseline"] == "L0" and target["rework_required"] is True
    assert target["legacy_artifacts_accepted"] is False
    assert target["lifecycle_mode"] == "planned" and target["theorem_complete"] is False
    release_item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert release_item == {
        "id": ITEM, "theorem_id": THEOREM, "execution_rank": 428,
        "phase": "release", "layer": 6, "state": "[ ]",
        "depends_on": ["S56-M-1248-VALIDATION"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Reconcile evidence and decide the exact theorem-completion verdict.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0, "children": [],
    }
    validation_item = next(row for row in execution["items"] if row["id"] == "S56-M-1248-VALIDATION")
    assert validation_item["state"] == "[_]" and validation_item["attempts"] == 1

    assert decision["reconciled_inputs"] == RECONCILED_INPUTS
    for name, expected in RECONCILED_INPUTS.items():
        assert sha256(HERE / name) == expected, f"reconciled input drifted: {name}"
    assert decision["authority_inputs"] == AUTHORITY_INPUTS
    for relative, expected in AUTHORITY_INPUTS.items():
        assert sha256(ROOT / relative) == expected, f"authority input drifted: {relative}"
    for name, expected in RELEASE_OUTPUTS.items():
        assert sha256(HERE / name) == expected, f"release output drifted: {name}"

    assert statement["canonical_formal_target"]["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert registry["root_expression_sha256"] == EXPRESSION_SHA256
    assert [row["obligation_id"] for row in registry["obligations"]] == INVENTORY_IDS
    assert registry["denominator_sha256"] == graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    closure = graphs["closure_boundary"]
    assert closure["root_closed"] is closure["audit_complete"] is closure["theorem_complete"] is False
    assert closure["remaining_root_cut_set"] == ["M1248-T-ALL-PARAMS"]
    root = next(row for row in graphs["nodes"] if row["obligation_id"] == "M1248-ROOT")
    assert [root["human_debt"], root["machine_debt"], root["readability_debt"]] == ["H1", "M3", "R3"]
    assert intake["root_vector"] == {"human": "H1", "machine": "M4", "readability": "R3"}

    assert proof["accepted"] is False and proof["result"]["exact_frozen_root_kernel_closed"] is True
    assert proof["result"]["source_claim_proved"] is proof["result"]["theorem_complete"] is False
    assert proof["first_failed_completion_gate"] == "S56-5.1-EXACT-TARGET-IDENTITY-OR-TRANSPORT"
    assert sha256(HERE / "validation-receipt.json") == VALIDATION_RECEIPT_SHA256
    assert validation["accepted"] is validation["release_grade"] is False
    assert validation["verdict"] == "blocked" and validation["proposed_state"] == "[_]"
    assert validation["result"]["source_claim_proved"] is False
    assert validation["result"]["accepted_closed_obligation_ids"] == []
    assert validation["result"]["audit_complete"] is validation["result"]["theorem_complete"] is False
    assert validation["first_failed_theorem_gate"] == "S56-5.1-EXACT-TARGET-IDENTITY-OR-TRANSPORT"

    assert decision["schema_version"] == "stage1-release-decision/1.0"
    assert decision["item_id"] == ITEM and decision["theorem_id"] == THEOREM
    assert decision["verdict"] == "blocked" and decision["proposed_state"] == "[_]"
    assert decision["accepted"] is decision["release_grade"] is False
    assert decision["content_addressed_release_evidence"] is False
    assert decision["lifecycle_before"] == decision["lifecycle_after"] == "planned"
    assert decision["accepted_receipt_ids"] == []
    dependency = decision["dependency"]
    assert dependency["item_id"] == validation_item["id"] == validation["item_id"]
    assert dependency["receipt_id"] == validation["receipt_id"]
    assert dependency["receipt_sha256"] == VALIDATION_RECEIPT_SHA256
    assert dependency["accepted"] is dependency["release_grade"] is dependency["master_accepted"] is False
    assert decision["root_vector"]["accepted_before"] == decision["root_vector"]["accepted_after"] == ["H1", "M3", "R3"]
    assert decision["terminal_decisions"] == {
        "audit_complete": False, "theorem_complete": False,
        "audit_z": "blocked", "theorem_z": "blocked",
        "release_accepted": False, "master_acceptance": False,
    }
    assert decision["first_failed_gate"]["dependency_gate"] == "dependency.S56-M-1248-VALIDATION.master_acceptance"
    assert decision["first_failed_theorem_gate"]["gate_id"] == "S56-5.1-EXACT-TARGET-IDENTITY-OR-TRANSPORT"
    assert decision["first_failed_release_gate"]["gate_id"] == "S56-RELEASE-IMMUTABLE-CLEAN-INPUT"
    assert decision["next_failed_release_gate"]["gate_id"] == "S56-10.6-HERMETIC-COLD-BUILD"
    assert decision["evidence_reconciliation"]["accepted_closed_obligation_ids"] == []
    assert decision["evidence_reconciliation"]["source_claim_proved"] is False
    for key in (
        "validation_dependency_acceptance", "audit_inventory_reconciliation",
        "human_source_acceptance", "readability_acceptance",
        "complete_provenance_foundation_tcb_closure", "immutable_clean_release_input",
        "hermetic_cold_offline_replay", "sbom_license_archive_closure",
        "independent_clean_runner_attestations", "independently_implemented_minimal_verifier",
        "protected_ci_and_mutation_gates", "deterministic_release_bundle",
    ):
        assert decision["evidence_reconciliation"][key] == "missing", key
    cut_text = "\n".join(decision["remaining_root_cut_set"])
    for fragment in (
        "master acceptance", "S56-5.1", "M1248-T-ALL-PARAMS", "AUDIT-Z",
        "accepted H0", "accepted R0", "foundation profile", "empty-cache network-denied cold build",
        "SBOM", "two signed attestations", "minimal release verifier", "deterministic build-twice",
    ):
        assert fragment in cut_text, fragment

    assert spec["schema_version"] == "stage1-validation-recipe/1.0"
    assert spec["recipe_id"] == "S56-M-1248-RELEASE-negative-reconciliation-v1"
    assert spec["item_id"] == ITEM and spec["theorem_id"] == THEOREM
    assert spec["argv"] == [
        "python3", "-I", "-B", f"Stage1_Instances/{THEOREM}/check_release.py",
        "--worker-packet", ".stage1-worker-selftest.json",
    ]
    assert spec["network_policy"] == "denied" and spec["expected_exit"] == 0
    assert spec["covered_obligation_ids"] == INVENTORY_IDS
    for key in (
        "recipe_id", "cwd", "argv", "env_allowlist", "timeout_seconds",
        "network_policy", "network_enforcement", "expected_exit",
        "expected_outputs", "covered_obligation_ids", "covered_declarations",
    ):
        assert receipt["recipe"][key] == spec[key], key
    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == ITEM and receipt["depends_on"] == [validation_item["id"]]
    assert receipt["accepted"] is receipt["release_grade"] is receipt["master_accepted"] is False
    assert receipt["verdict"] == "blocked"
    assert receipt["result"]["source_claim_proved"] is False
    assert receipt["result"]["audit_complete"] is receipt["result"]["theorem_complete"] is False
    assert receipt["changed_paths"] == CHANGED_PATHS
    for relative, expected in receipt["input_bindings"].items():
        assert sha256(ROOT / relative) == expected, f"receipt input drifted: {relative}"

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by)\b|"
        r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
        r"(?:axiom|constant|opaque|unsafe|extern)\b", re.MULTILINE,
    )
    combined = "\n".join(
        code_without_comments((HERE / source).read_text(encoding="utf-8"))
        for source in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean")
    )
    assert prohibited.search(combined) is None
    validation_source = (HERE / "Validation.lean").read_text(encoding="utf-8")
    imports = validation_source.split("/-!", 1)[0]
    assert "import Proof" not in imports and "import ObligationTree" not in imports
    assert "theorem frozenOrder_eq_omega" in validation_source
    assert "theorem frozenOrder_ne_infinity" in validation_source

    assert (LEAN_ROOT / ".lake").is_symlink()
    mathlib = (LEAN_ROOT / ".lake/packages/mathlib").resolve()
    assert git("rev-parse", "HEAD", cwd=mathlib) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == MATHLIB_TREE
    assert git("status", "--porcelain=v1", "--untracked-files=all", cwd=mathlib) == ""
    launcher = Path(HOME) / ".elan/bin/lake"
    lean = Path(run([str(launcher), "env", "which", "lean"], cwd=LEAN_ROOT, env=BASE_ENV).strip())
    outputs = isolated_replay(lean, pinned_lean_path(lean))
    proof_decl = "Stage1Instances.THM_M_1248.caffarelliKohnNirenbergTarget"
    validation_decl = "Stage1Instances.THM_M_1248.Validation.independentlyReconstructedFrozenTarget"
    assert reported_axioms(outputs["proof"], proof_decl) == EXPECTED_AXIOMS
    assert reported_axioms(outputs["validation"], validation_decl) == EXPECTED_AXIOMS
    assert "Declarations are sorry-free!" in outputs["validation"]
    assert "VALIDATION_CLOSURE declarations=36964 modules=1341" in outputs["validation"]
    assert "VALIDATION_CLOSURE bodyless_nonaxioms=[]" in outputs["validation"]
    assert "VALIDATION_CLOSURE unsafe=[]" in outputs["validation"]
    expected_output_hashes = validation["result"]["lean_output_sha256"]
    for key, output in outputs.items():
        assert hashlib.sha256(output.encode()).hexdigest() == expected_output_hashes[key], key

    if args.worker_packet is not None:
        packet = load((ROOT / args.worker_packet).resolve())
        assert set(packet) == {
            "item_id", "changed_paths", "commands", "output_summary",
            "base_revision", "known_failures", "state",
        }
        assert packet["item_id"] == ITEM and packet["state"] == "[_]"
        assert packet["base_revision"] == BASE_REVISION
        assert packet["changed_paths"] == CHANGED_PATHS
        assert packet["known_failures"] == decision["known_failures"]
        status = git("status", "--short", "--untracked-files=all")
        actual = {line[3:] for line in status.splitlines() if line[3:] != "Formalizations/Lean/.lake"}
        assert actual == set(CHANGED_PATHS), (actual, set(CHANGED_PATHS))

    for name in (*RELEASE_OUTPUTS, "check_release.py"):
        assert_text_hygiene(HERE / name)
    for line in SUMMARY_LINES:
        print(line)


if __name__ == "__main__":
    main()
