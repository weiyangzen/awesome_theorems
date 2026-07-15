#!/usr/bin/env python3
"""Fail-closed release reconciliation for S56-M-0711-RELEASE."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import platform
import re
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0711"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
ITEM = "S56-M-0711-RELEASE"
THEOREM = "THM-M-0711"
BASE_REVISION = "21798c9c8a9ed9ea40e8df489d9c661b59026564"
BASE_TREE = "9150bea4c07c5bc89526ce2540709f0e9e8fda24"
VALIDATION_BASE = "3a40b1969f841e07036db5c4d7f03e97c7c57949"
TOOLCHAIN = "leanprover/lean4:v4.29.0"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
LEAN_SHA256 = "3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf"
ELAN_LAUNCHER_SHA256 = "840179e70803ef373c2ec53342d6a45ea7d022533e4145489fc1278b4f716385"
BWRAP_SHA256 = "0abea81db798ebf6b4742ac0664802d97521547a353c2a0dbdc21d76cbbfd2c0"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MATHLIB_ORIGIN = "https://github.com/leanprover-community/mathlib4.git"
MATHLIB_LICENSE_SHA256 = "b40930bbcf80744c86c46a12bc9da056641d722716c378f5659b9e555ef833e1"
STATEMENT_SHA256 = "624dd9575960ac9d10b05c677f744c333edc7b162ddda57cafa251642b803436"
EXPRESSION_STDOUT_SHA256 = "1186dd31dd2f2126cb5998ef79ec6d9b64396acccdbdfc16dc6baa09c66edd3c"
DENOMINATOR_SHA256 = "9fbdae321a68e51a301e942864c9a785fab407f21f25247ab04cb74277bd8d24"
VALIDATION_RECEIPT_SHA256 = "d7a2e941371877c3aee340706df9afb98fee56be883e25ddbbe6b1f0d505666d"
ROOT_VECTOR = {"H": "H1", "M": "M4", "R": "R4"}
OPEN_ROOT_CUT = ["M0711-B-REDUCTION", "M0711-S-FOUNDATION"]
INVENTORY_IDS = [
    "M0711-ROOT", "M0711-S-ENCODING", "M0711-S-PRESENTATION",
    "M0711-S-FOUNDATION", "M0711-N-EVAL", "M0711-N-QUOTIENT",
    "M0711-B-REDUCTION", "M0711-C-PRESENTATION", "M0711-C-COMPILER",
    "M0711-C-CORRECT", "M0711-L-HALTING", "M0711-L-MANYONE",
    "M0711-L-NONCOMP", "M0711-X-SOURCE", "M0711-X-PROVENANCE",
    "M0711-T-WITNESS", "M0711-T-ASSEMBLE",
]
PROVISIONAL_IDS = ["M0711-N-QUOTIENT", "M0711-L-HALTING", "M0711-L-MANYONE"]
PARTIAL_IDS = ["M0711-L-NONCOMP", "M0711-T-WITNESS", "M0711-ROOT"]
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
EXPECTED_INPUTS = {
    "Statement.lean": STATEMENT_SHA256,
    "ObligationTree.lean": "d5b191ec34e258151ca1a56c041636eda0d5c7149936dca536db492e4d5f8e14",
    "Proof.lean": "119c50417d4559f3142fd67e0375b4cb99865141842f1a1dfc27352f2ada2b65",
    "Validation.lean": "f361ca0ec0c54a9aa9abc26592a7cd27996fe0dc88bd143736c89fdddf0cb789",
    "instance.json": "a0581fdba7291fd3e736c3f80e267d8b993375c003fef649617cca126609432f",
    "task-dag.json": "ec0ada4c3f400cd0be66000681fc85626d02fcb765a5c0ce295c62b5427c1057",
    "source-statement-crosswalk.md": "74e237433a2c2e14ddf347665c7792de36465bda6f72af3adab08445e165eeaa",
    "statement-receipt.json": "0e497c79be5be1727ad57d10553a6224142235390cb8f49dc2b0c26e90241194",
    "anchor-audit-receipt.json": "7f186646b95d2a905cfcc73de8085727e4e130e1e4a0a7eb8de33b1ddf628e41",
    "obligation-registry.json": "0d40d1d7aa73bb51f2c263f27bac6b348c628cf8405af86b2473637981800983",
    "typed-graphs.json": "f24be97eda17d4e9c99da61f43fc7a5886e489aff1fc335611ab14339f5ff94f",
    "obligation-tree-receipt.json": "50ffa832f7800a4a9f9bce1fa33d9daac9650c960e681c7e39650b4b3b79c570",
    "proof-receipt.json": "196f2d0cbbb8145cb78ec6e0ab5f33929cb4cc5e2e0668b5742e56915247acb1",
    "proof-blocker.json": "1ab776204688472c11dc63daab57d29cfc06e11f2a0740d623cb34cd1d7094ef",
    "validation-spec.json": "cff3a5ff8d8d8cf1a473b2d55ecdc50f1316b04c6ed653e98f5b05877e482e92",
    "check_validation.py": "753cf7880f594e20e4721d74a00473cf4a5bec22a204b0ffc7e9e60ea00e0468",
    "validation-receipt.json": VALIDATION_RECEIPT_SHA256,
}
AUTHORITY_INPUTS = {
    "Docs/Stage1_Targets_rev-5.6.json": "02eec284de534dd78e1cf75f82a477ff477567dd682b7445cb7587abd137ab2c",
    "Docs/Stage1_Execution_DAG_rev-5.6.json": "c7a28e4144c2260845177b08a3e0a70629ac15d3a374cea3241245e661b618de",
    "Docs/Stage1_Blueprint_rev-5.6.md": "0c3b72642383ff79ab7164b112ccba44271f7f63cd93d02743718442b4ff377f",
    "Docs/Blueprint_Guidelines.md": "a06c07b5ca1b270b4935ad3dab893e9a0e078c29c8da2ef9dca1e71193310535",
    "skills/execute-stage1-rev56/SKILL.md": "26d47a66c6535feabb8bbf1051fd55d76a53fe761f4b3d953f86b97ec86152b8",
}
TOOL_INPUTS = {
    "lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
SUMMARY_LINES = [
    "PASS release reconciliation: target, DAG, receipts, registry, graphs, and hashes agree",
    "PASS narrow Lean replay: exact statement plus partial, conditional, and differential declarations checked at trust zero",
    "BLOCKED S56-10.2-DEPENDENCY-ACCEPTANCE: validation is provisional and not master accepted",
    "BLOCKED exact root: H1/M4/R4 unchanged; M0711-B-REDUCTION and M0711-S-FOUNDATION remain open",
    "BLOCKED AUDIT-Z and THEOREM-Z: source/readability, trust, hermetic, independent, and public-reconciliation gates are open",
    "verdict=blocked audit_complete=false theorem_complete=false accepted_receipts=0",
]
RELEASE_NAMES = (
    "check_release.py", "release-decision.json", "release-receipt.json",
    "release-spec.json", "release-validation.md",
)
RELEASE_BOUND_NAMES = tuple(
    name for name in RELEASE_NAMES if name != "release-receipt.json"
)
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    *(f"Stage1_Instances/{THEOREM}/{name}" for name in RELEASE_NAMES),
}


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


def run(
    argv: list[str], *, cwd: Path = ROOT, env: dict[str, str] | None = None,
    timeout: int = 600,
) -> str:
    result = subprocess.run(
        argv, cwd=cwd, env=env, text=True, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, timeout=timeout, check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(f"command failed ({result.returncode}): {argv!r}\n{result.stdout}")
    return result.stdout


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["/usr/bin/git", *args], cwd=cwd, timeout=60).strip()


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
    pattern = re.compile(
        re.escape(f"'{declaration}' depends on axioms: [") + r"(.*?)]", re.DOTALL,
    )
    matches = pattern.findall(output)
    assert len(matches) == 1, f"missing or duplicate axiom report for {declaration}"
    return {part.strip() for part in matches[0].split(",") if part.strip()}


def assert_text_hygiene(path: Path) -> None:
    data = path.read_bytes()
    assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())


def pinned_lean_path(lean: Path) -> str:
    packages = (
        "batteries", "Qq", "aesop", "proofwidgets", "importGraph",
        "LeanSearchClient", "plausible", "mathlib",
    )
    roots = [
        (LEAN_ROOT / ".lake" / "packages" / name / ".lake/build/lib/lean").resolve()
        for name in packages
    ]
    assert all(path.is_dir() for path in roots)
    local = (LEAN_ROOT / ".lake/build/lib/lean").resolve()
    assert local.is_dir()
    return ":".join([*(str(path) for path in roots), str(local), str(lean.parent.parent / "lib/lean")])


def narrow_lean_replay() -> dict[str, object]:
    home = os.environ["HOME"]
    fixed_env = {
        "HOME": home,
        "PATH": f"{home}/.elan/bin:/usr/bin:/bin",
        "ELAN_TOOLCHAIN": TOOLCHAIN,
        "LANG": "C.UTF-8",
        "LC_ALL": "C.UTF-8",
        "TZ": "UTC",
        "LEAN_NUM_THREADS": "1",
    }
    lake_launcher = Path(home) / ".elan/bin/lake"
    bwrap = Path("/usr/bin/bwrap")
    assert sha256(lake_launcher) == ELAN_LAUNCHER_SHA256
    assert sha256(bwrap) == BWRAP_SHA256
    mathlib = (LEAN_ROOT / ".lake/packages/mathlib").resolve()
    lean = Path(run([str(lake_launcher), "env", "which", "lean"], cwd=mathlib, env=fixed_env).strip())
    assert sha256(lean) == LEAN_SHA256
    assert LEAN_COMMIT in run([str(lean), "--version"], env=fixed_env)
    lean_path = pinned_lean_path(lean)

    with tempfile.TemporaryDirectory(prefix="stage1-m0711-release-", dir="/tmp") as name:
        tmp = Path(name).resolve()
        (tmp / "home").mkdir()
        for source in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
            (tmp / source).write_bytes((HERE / source).read_bytes())
        base = [
            str(bwrap), "--ro-bind", "/", "/", "--bind", str(tmp), str(tmp),
            "--dev", "/dev", "--proc", "/proc", "--unshare-net",
            "--die-with-parent", "--clearenv", "--setenv", "HOME", str(tmp / "home"),
            "--setenv", "LANG", "C.UTF-8", "--setenv", "LC_ALL", "C.UTF-8",
            "--setenv", "TZ", "UTC", "--setenv", "LEAN_NUM_THREADS", "1",
            "--chdir", str(tmp),
        ]

        def lean_run(source: str, module_path: str, emit_olean: bool) -> str:
            argv = base + ["--setenv", "LEAN_PATH", module_path, str(lean), "--trust=0"]
            if emit_olean:
                argv += ["-o", source.replace(".lean", ".olean")]
            argv.append(source)
            return run(argv, env=fixed_env)

        outputs = {
            "statement": lean_run("Statement.lean", lean_path, True),
            "obligation": lean_run("ObligationTree.lean", f"{tmp}:{lean_path}", True),
            "proof": lean_run("Proof.lean", f"{tmp}:{lean_path}", False),
            "validation": lean_run("Validation.lean", f"{tmp}:{lean_path}", False),
        }

    combined = "\n".join(outputs.values())
    assert "sorryAx" not in combined and "error:" not in combined
    proof_declarations = (
        "Stage1.THM_M_0711.identityPred_iff_normalClosure",
        "Stage1.THM_M_0711.not_computablePred_of_manyOneReducible",
        "Stage1.THM_M_0711.haltingPredicate_not_computable",
        "Stage1.THM_M_0711.fixedPresentationUndecidable_of_haltingReduction",
        "Stage1.THM_M_0711.novikovBooneTarget_of_haltingReduction",
    )
    validation_declarations = (
        "Stage1.THM_M_0711.Validation.differentialIdentityPredIffNormalClosure",
        "Stage1.THM_M_0711.Validation.differentialNotComputablePredOfManyOne",
        "Stage1.THM_M_0711.Validation.differentialHaltingPredicateNotComputable",
        "Stage1.THM_M_0711.Validation.differentialConditionalTarget",
    )
    for declaration in proof_declarations:
        assert reported_axioms(outputs["proof"], declaration) == EXPECTED_AXIOMS
    assert reported_axioms(
        outputs["obligation"], "Stage1.THM_M_0711.novikovBooneTarget_of_witness"
    ) == EXPECTED_AXIOMS
    for declaration in validation_declarations:
        assert reported_axioms(outputs["validation"], declaration) == EXPECTED_AXIOMS
    assert outputs["proof"].count("Declarations are sorry-free!") == 8
    assert outputs["validation"].count("Declarations are sorry-free!") == 4
    closure = re.search(
        r"VALIDATION_CLOSURE declarations=(\d+) modules=(\d+)", outputs["validation"]
    )
    assert closure is not None
    assert "VALIDATION_CLOSURE axioms=[propext, Classical.choice, Quot.sound]" in outputs["validation"]
    assert "VALIDATION_CLOSURE bodyless_nonaxioms=[]" in outputs["validation"]
    assert "VALIDATION_CLOSURE unsafe=[]" in outputs["validation"]
    return {
        "output_sha256": {
            key: hashlib.sha256(value.encode()).hexdigest() for key, value in outputs.items()
        },
        "validation_closure": {
            "declarations": int(closure.group(1)),
            "modules": int(closure.group(2)),
            "bodyless_nonaxioms": [],
            "unsafe_declarations": [],
        },
    }


def main() -> None:
    if not __debug__ or sys.flags.optimize != 0:
        raise RuntimeError("release checker requires Python assertions")

    decision = load(HERE / "release-decision.json")
    spec = load(HERE / "release-spec.json")
    receipt = load(HERE / "release-receipt.json")
    validation = load(HERE / "validation-receipt.json")
    proof = load(HERE / "proof-receipt.json")
    blocker = load(HERE / "proof-blocker.json")
    instance = load(HERE / "instance.json")
    task_dag = load(HERE / "task-dag.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    targets = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    for name, expected in EXPECTED_INPUTS.items():
        assert sha256(HERE / name) == expected, f"target input drifted: {name}"
    for relative, expected in AUTHORITY_INPUTS.items():
        assert sha256(ROOT / relative) == expected, f"authority input drifted: {relative}"
    for name, expected in TOOL_INPUTS.items():
        assert sha256(LEAN_ROOT / name) == expected, f"tool input drifted: {name}"

    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 751 and target["baseline"] == "L0"
    assert target["rework_required"] is True and target["lifecycle_mode"] == "planned"
    assert target["theorem_complete"] is False
    release_item = next(row for row in execution["items"] if row["id"] == ITEM)
    validation_item = next(
        row for row in execution["items"] if row["id"] == "S56-M-0711-VALIDATION"
    )
    assert release_item == {
        "id": ITEM, "theorem_id": THEOREM, "execution_rank": 751,
        "phase": "release", "layer": 6, "state": "[ ]",
        "depends_on": ["S56-M-0711-VALIDATION"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Reconcile evidence and decide the exact theorem-completion verdict.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0, "children": [],
    }
    assert validation_item["state"] == "[_]" and validation_item["attempts"] == 1

    assert instance["lifecycle"] == "planned" and instance["root_vector"] == ROOT_VECTOR
    assert instance["accepted_proof_state"] == []
    assert instance["audit_complete"] is instance["theorem_complete"] is False
    assert task_dag["accepted_states"] == []
    assert registry["root_obligation_id"] == graphs["root_node_id"] == "M0711-ROOT"
    assert registry["denominator_sha256"] == graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert registry["frozen_denominators"]["inventory"] == INVENTORY_IDS
    assert graphs["closure_boundary"] == {
        "root_closed": False,
        "theorem_complete": False,
        "remaining_root_cut_set": OPEN_ROOT_CUT,
    }
    root = next(node for node in graphs["nodes"] if node["obligation_id"] == "M0711-ROOT")
    assert {"H": root["human_debt"], "M": root["machine_debt"], "R": root["readability_debt"]} == ROOT_VECTOR
    assert all(node["evidence_ids"] == [] for node in graphs["nodes"])

    assert proof["accepted"] is False and proof["accepted_closed_obligation_ids"] == []
    assert proof["provisionally_closed_obligation_ids"] == PROVISIONAL_IDS
    assert proof["partial_progress_toward_obligation_ids"] == PARTIAL_IDS
    assert proof["result"]["root_kernel_closed"] is False
    assert proof["remaining_root_cut_set"] == OPEN_ROOT_CUT
    assert blocker["root_closed"] is blocker["audit_complete"] is blocker["theorem_complete"] is False
    assert blocker["remaining_root_cut_set"] == OPEN_ROOT_CUT

    assert sha256(HERE / "validation-receipt.json") == VALIDATION_RECEIPT_SHA256
    assert validation["base_revision"] == VALIDATION_BASE
    assert validation["support_state"] == "provisional_worker_selftest"
    assert validation["accepted"] is validation["release_grade"] is False
    assert validation["verdict"] == "blocked" and validation["accepted_receipt_ids"] == []
    assert validation["root_vector_before"] == validation["root_vector_after"] == ROOT_VECTOR
    validation_result = validation["result"]
    assert validation_result["accepted_closed_obligation_ids"] == []
    assert validation_result["root_closed"] is validation_result["root_kernel_closed"] is False
    assert validation_result["root_machine_debt"] == "M4"
    assert validation_result["open_root_cut_set"] == OPEN_ROOT_CUT
    assert validation_result["audit_complete"] is validation_result["theorem_complete"] is False
    assert validation["hermeticity"]["decision"].startswith("fail_closed")
    assert validation["independent_validation"]["decision"] == "fail_closed"

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by)\b|"
        r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
        r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
        r"(?:axiom|constant|opaque|unsafe|extern)\b",
        re.MULTILINE,
    )
    all_source = "\n".join(
        source_without_comments((HERE / name).read_text(encoding="utf-8"))
        for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean")
    )
    assert prohibited.search(all_source) is None

    assert (LEAN_ROOT / ".lake").is_symlink()
    mathlib = (LEAN_ROOT / ".lake/packages/mathlib").resolve()
    assert git("rev-parse", "HEAD", cwd=mathlib) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == MATHLIB_TREE
    assert git("status", "--porcelain=v1", "--untracked-files=all", cwd=mathlib) == ""
    assert git("remote", "get-url", "origin", cwd=mathlib) == MATHLIB_ORIGIN
    assert sha256(mathlib / "LICENSE") == MATHLIB_LICENSE_SHA256
    observation = narrow_lean_replay()
    assert observation["output_sha256"] == {
        "statement": "1186dd31dd2f2126cb5998ef79ec6d9b64396acccdbdfc16dc6baa09c66edd3c",
        "obligation": "35c2a1a1b2b6d040fb2cd4d03e919d41326809ae3bba6d0b04bb75f46b8f347e",
        "proof": "d96cc7b6f474efe16c8c22e05087c22a39d4433468fe4cdfbd360230b008bb2d",
        "validation": "e4bbeb1f098c45057d59d06378601b5423c10fa5f49cdb81e0377c131ddce940",
    }
    assert observation["validation_closure"] == {
        "declarations": 6104, "modules": 226,
        "bodyless_nonaxioms": [], "unsafe_declarations": [],
    }

    assert decision["schema_version"] == "stage1-release-decision/1.0"
    assert decision["item_id"] == ITEM and decision["theorem_id"] == THEOREM
    assert decision["base_revision"] == BASE_REVISION and decision["base_tree"] == BASE_TREE
    assert decision["proposed_state"] == "[_]" and decision["release_grade"] is False
    assert decision["canonical_target_source_sha256"] == STATEMENT_SHA256
    assert decision["canonical_target_serialized_stdout_sha256"] == EXPRESSION_STDOUT_SHA256
    assert decision["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert decision["accepted_receipt_ids"] == []
    expected_bindings = {
        **{f"Stage1_Instances/{THEOREM}/{name}": digest for name, digest in EXPECTED_INPUTS.items()},
        **AUTHORITY_INPUTS,
        **{f"Formalizations/Lean/{name}": digest for name, digest in TOOL_INPUTS.items()},
    }
    assert decision["input_bindings"] == expected_bindings
    dependency = decision["dependency"]
    assert dependency["item_id"] == validation["item_id"] == "S56-M-0711-VALIDATION"
    assert dependency["scheduler_projection"] == "[_]"
    assert dependency["receipt_id"] == validation["receipt_id"]
    assert dependency["receipt_sha256"] == VALIDATION_RECEIPT_SHA256
    assert dependency["receipt_accepted"] is dependency["receipt_release_grade"] is False
    assert dependency["master_accepted"] is False
    result = decision["decision"]
    assert result["verdict"] == "blocked"
    assert result["lifecycle_before"] == result["lifecycle_after"] == "planned"
    assert result["root_vector_before"] == result["root_vector_after"] == ["H1", "M4", "R4"]
    assert result["audit_complete"] is result["theorem_complete"] is False
    assert result["audit_z"] == result["theorem_z"] == "blocked"
    assert result["release_accepted"] is False and result["accepted_receipt_ids"] == []
    assert result["first_failed_gate"]["gate_id"] == "S56-10.2-DEPENDENCY-ACCEPTANCE"
    assert result["first_failed_audit_gate"]["gate_id"] == (
        "S56-AUDIT-FROZEN-INVENTORY-SOURCE-BOUNDARY-RECONCILIATION"
    )
    assert result["first_failed_theorem_gate"]["gate_detail"] == "M0711-B-REDUCTION"
    assert result["first_failed_release_protocol_gate"]["gate_id"] == (
        "S56-RELEASE-IMMUTABLE-CLEAN-INPUT"
    )
    assert result["next_failed_release_protocol_gate"]["gate_id"] == (
        "S56-10.6-HERMETIC-COLD-EMPTY-CACHE"
    )
    assert result["remaining_root_cut_set"] == OPEN_ROOT_CUT

    assert spec["schema_version"] == "stage1-validation-recipe/1.0"
    assert spec["item_id"] == ITEM and spec["theorem_id"] == THEOREM
    assert spec["argv"] == ["python3", "-I", "-B", f"Stage1_Instances/{THEOREM}/check_release.py"]
    assert spec["cwd"] == "." and spec["timeout_seconds"] == 600
    assert spec["network_policy"] == "denied" and spec["expected_exit"] == 0
    assert spec["covered_obligation_ids"] == INVENTORY_IDS
    assert spec["covered_decisions"] == ["AUDIT-Z", "THEOREM-Z"]

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]"
    assert receipt["accepted"] is receipt["release_grade"] is receipt["master_accepted"] is False
    assert receipt["accepted_receipt_ids"] == []
    assert receipt["decision_id"] == decision["decision_id"]
    assert receipt["input_bindings"] == expected_bindings
    assert receipt["result"]["verdict"] == "blocked"
    assert receipt["result"]["current_release_lean_output_sha256"] == observation["output_sha256"]
    assert receipt["result"]["validation_closure"] == observation["validation_closure"]
    assert receipt["result"]["accepted_closed_obligations"] == []
    assert receipt["result"]["remaining_root_cut_set"] == OPEN_ROOT_CUT
    assert receipt["result"]["audit_complete"] is receipt["result"]["theorem_complete"] is False
    for key in (
        "recipe_id", "cwd", "argv", "env_allowlist", "timeout_seconds",
        "network_policy", "network_enforcement", "expected_exit",
    ):
        assert receipt["recipe"][key] == spec[key], key
    expected_stdout = ("\n".join(SUMMARY_LINES) + "\n").encode()
    assert receipt["output_evidence"]["stdout_semantic_sha256"] == hashlib.sha256(expected_stdout).hexdigest()
    assert receipt["output_evidence"]["expected_line_count"] == len(SUMMARY_LINES)

    assert set(packet) == {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert packet["item_id"] == ITEM and packet["state"] == "[_]"
    assert packet["base_revision"] == BASE_REVISION
    assert set(packet["changed_paths"]) == set(receipt["changed_paths"]) == CHANGED_PATHS
    assert packet["commands"] == receipt["commands"]
    assert packet["output_summary"] == receipt["output_summary"] == SUMMARY_LINES
    assert packet["known_failures"] == receipt["known_failures"] == decision["known_failures"]

    release_bindings = {
        f"Stage1_Instances/{THEOREM}/{name}": sha256(HERE / name)
        for name in RELEASE_BOUND_NAMES
    }
    assert receipt["release_output_bindings"] == release_bindings
    for relative in CHANGED_PATHS:
        assert_text_hygiene(ROOT / relative)
    status = git("status", "--short", "--untracked-files=all")
    actual_changed = {
        line[3:] for line in status.splitlines()
        if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual_changed == CHANGED_PATHS, (actual_changed, CHANGED_PATHS)
    handoff = (HERE / "release-validation.md").read_text(encoding="utf-8")
    for fragment in (
        "`blocked`", "`[H1, M4, R4]`", "`AUDIT-Z`", "`THEOREM-Z`",
        "This worker accepts no", "`accepted=false`", "`release_grade=false`",
    ):
        assert fragment in handoff, fragment
    assert receipt["environment"]["platform"] == (
        f"{platform.system()} {platform.release()} {platform.machine()}"
    )
    print("\n".join(SUMMARY_LINES))


if __name__ == "__main__":
    main()
