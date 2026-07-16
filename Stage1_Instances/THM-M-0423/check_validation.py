#!/usr/bin/env python3
"""Fail-closed semantic validator for S56-M-0423-VALIDATION."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
from typing import Any, NoReturn


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0423"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM = "S56-M-0423-VALIDATION"
THEOREM = "THM-M-0423"
BASE_REVISION = "94009a6bebd743588e09c3b45bfbf18bf9b5c5e3"
BASE_TREE = "daabee9f9b2c6e98d84b6290f78a209b950485fc"
GRAPH_SHA256 = "eaee68bdf9fde9e311db076d1997fd8ef91919def0ba0fb399f1df77080f7153"
CONTEXT_SHA256 = "ced38ea3f671f427ebca5031cbe9686378aa8ecec11067923cafe84643218044"
CONTRACT_SHA256 = "1e7adf0f4fae0541b3595d4b0bfbb53f7eb17e28a4a889fec14f6df969e0cec4"
BLUEPRINT_SHA256 = "f7f8bcf307b737c56eb7ebc77fa2192046dc07b27ce58df5876ba4fdc4f1d7fb"
EXECUTION_DAG_SHA256 = "4a99805a42abdee02d4cc89849b6688711bad20b7238ddcef24ca775347d95e4"
TARGETS_SHA256 = "02eec284de534dd78e1cf75f82a477ff477567dd682b7445cb7587abd137ab2c"
REGISTRY_DENOMINATOR = "32a5c78d7f9cf7b59541a9a35c52331cf5055159b93dbe758b3eb6134f7da866"
TOOLCHAIN = "leanprover/lean4:v4.29.0"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
TOOLCHAIN_SHA256 = "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2"
MANIFEST_SHA256 = "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81"
LEAN_SHA256 = "3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf"
LAKE_SHA256 = "a608ff084d7e2af228b92a29d7c2fd083ba0580e46889175ec74a81678c98359"
SHARED_GROUPS = [
    "SHARED-MODULE-42c19d5b5a6d6b9e",
    "SHARED-MODULE-74cc3b6464e1332d",
]
EXPECTED_LOCAL_INPUTS = {
    "Statement.lean": "96abe224c0aa06c54dd30e3d7f5724b6f17cb6a5a2b537bf26fcc8dbba9cc7f0",
    "ObligationTree.lean": "91715b5fa0f62c35688a2669363fea94242b5c936fde217db45c2c021954ba53",
    "Proof.lean": "32b2fdaf55d05a43679837db4ebc9549ffa7c04e3a74cbc8501f4e3ccc06799a",
    "Validation.lean": "6536f1c64089f8b0556ab8ddb898e99a0e26507efed5bd365f931b9178f12352",
    "obligation-registry.json": "bdba1737dd0483b6d847e9dbca0e04dc52d86d52ecf1f5ecb3c286450b664fbc",
    "typed-graphs.json": "36a31f9b605bc91771517b8a2595f034f4fdbb124b55a71637f23a0c716e09e1",
    "proof-receipt.json": "b74ddec595c708786e25368cf1a2ec7f3c73e17a8da466759087d3f87ee40490",
    "proof-blocker.json": "03933458962160c34e3ce34a17433ef8084e321857743a4cfbddb9185f7d52dc",
    "dependency-reuse-ledger.json": "34b38114acfe1e42b7ce2bf3a9bab333f8a2c592e435d1ffa1db55688329e775",
    "validation-specs.json": "8c7a4b4f36db3ff34c5c517ad3777525cae23fc7fd30bb509f32a830023f8707",
}
EXPECTED_GIT_BLOBS = {
    "Statement.lean": "0c4dbb7032e4ab1373f1c9b7e0923979a03445b8",
    "ObligationTree.lean": "d501bd5d9ea805b05d3b13589d1e9400e3e3e5f2",
    "Proof.lean": "dd52e76d2091e9762c4a214b4a1e5a7046f54def",
    "Validation.lean": "03182e4b4b15876ddb5df87aeddfc5f7c06c2f56",
    "obligation-registry.json": "72d60ba9b1d4ba6117886c51329c79543464557b",
    "typed-graphs.json": "1dd225ecceb0b8c7a7905af2b2519977e67c09df",
    "proof-receipt.json": "6809b62d85e47d2434fbab20f8c973cdf5376184",
    "proof-blocker.json": "41f89aec266ceff4f652667a20b19ec1cb21d4ec",
    "dependency-reuse-ledger.json": "77bbdb35491157fc7dc3710f0027498f9524f243",
    "validation-specs.json": "f948aeb28f0a3cd9596e3de9938e9b61ba3dfa1e",
}
MATHLIB_INPUTS = {
    "Mathlib/LinearAlgebra/QuadraticForm/AlgClosed.lean": (
        "ef8f919efce05094681aee729b558bc5f74efe554038e22d475625c840e8e15e",
        "104448e3bba490c34cbabaeaa602e25962e1abfa",
        "c73c631caac58c00b724db13bbeb78994e1d3e030333c6d6eac7d7637e1f42a3",
    ),
    "Mathlib/LinearAlgebra/QuadraticForm/Basic.lean": (
        "a76634a898adec1e5a9148f28a1a72ec5e2c8082c4ffe929fbc1ba8b4bdf5782",
        "cdadc86b91627c654b94098f9d59ffbf93815410",
        "4f2ea6ca154727dcc1f7a4e5937545e3274cb90b96ca0cdae193d3c0613288e3",
    ),
    "Mathlib/LinearAlgebra/QuadraticForm/IsometryEquiv.lean": (
        "77babd75db5aaed92498ead2d62ee89c15f1d8534f1534301bc3b5cbe5feb807",
        "0e1306c26753653b92ff8dca04748ea6af5cf1f2",
        "956c4fbed24df5d6cf7115a933a3626576458b4cc18291f2a76e28849fe83732",
    ),
    "Mathlib/LinearAlgebra/QuadraticForm/Radical.lean": (
        "e75f636382f78a83b2b3cf04b2bcb4ab6bc80dffe6c7aeb84a8630d530316c2e",
        "df01c340bda52dec288c95ba395f72c8a55eef3c",
        "4e854add3a986df7abfa30bf76b4a0df4f888e235ac9b0f2d5392828b0ddacdb",
    ),
    "Mathlib/LinearAlgebra/QuadraticForm/TensorProduct.lean": (
        "602b94e9fef1b494e662d6010d6197d9cd54a71b19a27a28c8ca2cd06205b06f",
        "0221d16b8f9460693c852dd55356b2651886e44d",
        "e8f75f445fc9d71c11609179bd3062a977201c7742077d399bc6908fb9e6d4f3",
    ),
}
EXPECTED_AXIOMS = {
    "isotropic_after_baseChange": {"propext", "Classical.choice", "Quot.sound"},
    "global_to_local": {"propext", "Classical.choice", "Quot.sound"},
    "root_composition": {"propext", "Classical.choice", "Quot.sound"},
    "direction_package": {"propext", "Classical.choice", "Quot.sound"},
    "root_from_direction_package": {"propext", "Classical.choice", "Quot.sound"},
    "isIsotropic_iff_of_isometryEquiv": {"propext", "Quot.sound"},
    "equivalent_weightedSumSquares_units": {"propext", "Classical.choice", "Quot.sound"},
    "equivalent_sumSquares_of_isAlgClosed": {"propext", "Classical.choice", "Quot.sound"},
    "equivalent_sumSquares_complex": {"propext", "Classical.choice", "Quot.sound"},
    "independent_isIsotropic_iff_of_isometryEquiv": {"propext", "Quot.sound"},
    "independent_equivalent_weightedSumSquares_units": {
        "propext", "Classical.choice", "Quot.sound",
    },
    "independent_equivalent_sumSquares_complex": {
        "propext", "Classical.choice", "Quot.sound",
    },
}
PROHIBITED = re.compile(
    r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by|extern|run_tac)\b|"
    r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
    r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
    r"(?:axiom|constant|opaque|unsafe)\b",
    flags=re.MULTILINE,
)


class ValidationError(RuntimeError):
    pass


def fail(message: str) -> NoReturn:
    raise ValidationError(message)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path: Path) -> dict[str, Any]:
    def reject_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        value: dict[str, Any] = {}
        for key, child in pairs:
            if key in value:
                fail(f"duplicate JSON key {key!r} in {path.relative_to(ROOT)}")
            value[key] = child
        return value

    try:
        value = json.loads(
            path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicates
        )
    except (OSError, json.JSONDecodeError) as error:
        fail(f"cannot load {path.relative_to(ROOT)}: {error}")
    if not isinstance(value, dict):
        fail(f"expected JSON object in {path.relative_to(ROOT)}")
    return value


def run(argv: list[str], *, cwd: Path, env: dict[str, str] | None = None,
        timeout: int = 300) -> str:
    result = subprocess.run(
        argv, cwd=cwd, env=env, capture_output=True, text=True, timeout=timeout
    )
    if result.returncode:
        fail(f"command failed ({result.returncode}): {argv!r}\n{result.stdout}{result.stderr}")
    return result.stdout + result.stderr


def git(*argv: str, cwd: Path = ROOT) -> str:
    return run(["/usr/bin/git", *argv], cwd=cwd, timeout=30).strip()


def strip_comments_and_strings(source: str) -> str:
    out: list[str] = []
    index = 0
    depth = 0
    quoted = False
    escaped = False
    while index < len(source):
        pair = source[index:index + 2]
        char = source[index]
        if depth:
            if pair == "/-":
                depth += 1
                out.extend("  ")
                index += 2
            elif pair == "-/":
                depth -= 1
                out.extend("  ")
                index += 2
            else:
                out.append("\n" if char == "\n" else " ")
                index += 1
        elif quoted:
            out.append("\n" if char == "\n" else " ")
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                quoted = False
            index += 1
        elif pair == "/-":
            depth = 1
            out.extend("  ")
            index += 2
        elif pair == "--":
            end = source.find("\n", index)
            if end == -1:
                out.extend(" " * (len(source) - index))
                index = len(source)
            else:
                out.extend(" " * (end - index))
                index = end
        elif char == '"':
            quoted = True
            out.append(" ")
            index += 1
        else:
            out.append(char)
            index += 1
    if depth or quoted:
        fail("unterminated comment or string in Lean source")
    return "".join(out)


def printed_axioms(output: str, declaration: str) -> set[str]:
    match = re.search(
        rf"'[^']*\.{re.escape(declaration)}' depends on axioms:\s*\[(.*?)\]",
        output,
        flags=re.DOTALL,
    )
    if match is None:
        if re.search(
            rf"'[^']*\.{re.escape(declaration)}' does not depend on any axioms",
            output,
        ):
            return set()
        fail(f"missing axiom report for {declaration}")
    return set(re.findall(r"[A-Za-z][A-Za-z0-9_.]*", match.group(1)))


def compiled_roots() -> list[Path]:
    roots = sorted(
        (package / ".lake" / "build" / "lib" / "lean").resolve()
        for package in (LEAN_ROOT / ".lake" / "packages").iterdir()
        if package.is_dir()
        and (package / ".lake" / "build" / "lib" / "lean").is_dir()
    )
    if not roots:
        fail("pinned compiled dependency artifacts are unavailable; fetching is forbidden")
    return roots


def lean_replay() -> dict[str, str]:
    lean = Path.home() / ".elan" / "toolchains" / "leanprover--lean4---v4.29.0" / "bin" / "lean"
    if digest(lean) != LEAN_SHA256 or LEAN_COMMIT not in run([str(lean), "--version"], cwd=LEAN_ROOT):
        fail("pinned Lean executable identity changed")
    with tempfile.TemporaryDirectory(prefix="m0423-validation-", dir="/tmp") as raw:
        scratch = Path(raw).resolve()
        names = ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean")
        for name in names:
            destination = scratch / name
            if os.access(destination.parent, os.W_OK):
                destination.write_bytes((HERE / name).read_bytes())
            else:
                destination = HERE / name
            if digest(destination) != EXPECTED_LOCAL_INPUTS[name]:
                fail(f"Lean replay source changed: {name}")
        dependency_path = ":".join(str(path) for path in compiled_roots())
        def check(name: str, local_imports: bool, emit_olean: bool) -> str:
            lean_path = f"{scratch}:{dependency_path}" if local_imports else dependency_path
            argv = [str(lean), "--trust=0", "-t0", f"--root={scratch}"]
            if emit_olean:
                argv += ["-o", Path(name).with_suffix(".olean").name]
            source = scratch / name
            argv.append(str(source if source.is_file() else HERE / name))
            env = {
                "HOME": str(scratch),
                "TMPDIR": str(scratch),
                "LANG": "C.UTF-8",
                "LC_ALL": "C.UTF-8",
                "TZ": "UTC",
                "LEAN_NUM_THREADS": "1",
                "LEAN_PATH": lean_path,
                "PATH": "/usr/bin:/bin",
                "NO_PROXY": "*",
                "no_proxy": "*",
                "http_proxy": "http://127.0.0.1:9",
                "https_proxy": "http://127.0.0.1:9",
                "ALL_PROXY": "http://127.0.0.1:9",
            }
            return run(argv, cwd=scratch, env=env, timeout=300)

        return {
            "statement": check("Statement.lean", False, True),
            "obligation_tree": check("ObligationTree.lean", True, True),
            "proof": check("Proof.lean", True, True),
            "validation": check("Validation.lean", True, False),
        }


def verify_authorities() -> None:
    if git("rev-parse", "HEAD") != BASE_REVISION or git("rev-parse", "HEAD^{tree}") != BASE_TREE:
        fail("repository worker base changed")
    authorities = {
        "Docs/Stage1_Blueprint_v2.md": BLUEPRINT_SHA256,
        "Docs/Stage1_Theorem_DAG_v2.json": GRAPH_SHA256,
        "Docs/Stage1_Phase_Acceptance_Contracts.json": CONTRACT_SHA256,
        "Docs/Stage1_Execution_DAG_rev-5.6.json": EXECUTION_DAG_SHA256,
        "Docs/Stage1_Targets_rev-5.6.json": TARGETS_SHA256,
    }
    for relative, expected in authorities.items():
        if digest(ROOT / relative) != expected:
            fail(f"authority input changed: {relative}")

    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    item = next(row for row in execution["items"] if row.get("id") == ITEM)
    if item != {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 67,
        "phase": "validation",
        "layer": 5,
        "state": "[ ]",
        "depends_on": ["S56-M-0423-PROOF"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Run hermetic kernel, trust, provenance, and independent validation gates.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }:
        fail("authoritative validation item changed")
    predecessor = next(row for row in execution["items"] if row.get("id") == "S56-M-0423-PROOF")
    if predecessor.get("state") != "[_]" or predecessor.get("attempts") != 1:
        fail("observed proof prerequisite state changed")

    theorem_dag = load(ROOT / "Docs/Stage1_Theorem_DAG_v2.json")
    node = next(row for row in theorem_dag["theorems"] if row.get("theorem_id") == THEOREM)
    if node.get("v2_execution_rank") != 301 or node.get("topological_layer") != 0:
        fail("v2 claim order changed")
    if node.get("dependency_context_sha256") != CONTEXT_SHA256:
        fail("dependency context changed")
    if node.get("direct_hard_parents") != [] or node.get("transitive_hard_ancestors") != []:
        fail("hard-parent closure is no longer empty")
    if node.get("direct_reuse_hint_ids") != [] or node.get("shared_lemma_group_ids") != SHARED_GROUPS:
        fail("reuse context changed")

    contract = load(ROOT / "Docs/Stage1_Phase_Acceptance_Contracts.json")
    phase = next(row for row in contract["phases"] if row.get("phase") == "validation")
    if phase.get("layer") != 5 or phase.get("intent") != "validate":
        fail("validation phase contract changed")
    if [row.get("path_pattern") for row in phase["validator_candidates"]] != [
        "Stage1_Instances/{theorem_id}/check_validation.py",
        "Stage1_Instances/{theorem_id}/check_validation.sh",
    ]:
        fail("validation validator candidates changed")
    if (HERE / "check_validation.sh").exists():
        fail("validation validator selection is ambiguous")


def verify_inputs() -> None:
    for name, expected in EXPECTED_LOCAL_INPUTS.items():
        path = HERE / name
        if digest(path) != expected:
            fail(f"owned input changed: {name}")
        if git("hash-object", str(path)) != EXPECTED_GIT_BLOBS[name]:
            fail(f"owned Git blob changed: {name}")
    if digest(LEAN_ROOT / "lean-toolchain") != TOOLCHAIN_SHA256:
        fail("Lean toolchain file changed")
    if digest(LEAN_ROOT / "lake-manifest.json") != MANIFEST_SHA256:
        fail("Lake manifest changed")
    lean = Path.home() / ".elan" / "toolchains" / "leanprover--lean4---v4.29.0" / "bin" / "lean"
    lake = lean.with_name("lake")
    if digest(lean) != LEAN_SHA256 or digest(lake) != LAKE_SHA256:
        fail("Lean or Lake executable changed")
    manifest = load(LEAN_ROOT / "lake-manifest.json")
    mathlib_entry = next(row for row in manifest["packages"] if row.get("name") == "mathlib")
    if mathlib_entry.get("rev") != MATHLIB_REVISION:
        fail("manifest mathlib pin changed")
    if git("rev-parse", "HEAD", cwd=MATHLIB) != MATHLIB_REVISION:
        fail("checked-out mathlib revision changed")
    if git("rev-parse", "HEAD^{tree}", cwd=MATHLIB) != MATHLIB_TREE:
        fail("checked-out mathlib tree changed")
    if git("status", "--porcelain=v1", cwd=MATHLIB):
        fail("checked-out mathlib worktree is dirty")
    for relative, (source_hash, blob, olean_hash) in MATHLIB_INPUTS.items():
        source = MATHLIB / relative
        olean = MATHLIB / ".lake/build/lib/lean" / Path(relative).with_suffix(".olean")
        if digest(source) != source_hash or git("hash-object", relative, cwd=MATHLIB) != blob:
            fail(f"selected mathlib source changed: {relative}")
        if digest(olean) != olean_hash:
            fail(f"selected mathlib object changed: {olean.relative_to(MATHLIB)}")


def verify_evidence() -> None:
    ledger = load(HERE / "dependency-reuse-ledger.json")
    for field, expected in (
        ("schema_version", "stage1-dependency-reuse-ledger/1.1"),
        ("consumer_theorem_id", THEOREM),
        ("observed_theorem_dag_sha256", GRAPH_SHA256),
        ("dependency_context_sha256", CONTEXT_SHA256),
        ("repository_revision", BASE_REVISION),
    ):
        if ledger.get(field) != expected:
            fail(f"dependency ledger field changed: {field}")
    for field in (
        "direct_parent_ids", "transitive_ancestor_ids", "hard_edge_ids", "reuse_hint_ids",
        "inspections", "unresolved_compatibility_obligations",
    ):
        if ledger.get(field) != []:
            fail(f"dependency ledger field {field} is no longer empty")
    if ledger.get("shared_group_ids") != SHARED_GROUPS:
        fail("dependency ledger shared groups changed")
    decisions = ledger.get("reuse_decisions")
    if not isinstance(decisions, list) or [row.get("source_id") for row in decisions] != SHARED_GROUPS:
        fail("weak shared-group decisions are incomplete or out of order")
    for row in decisions:
        if row.get("decision") != "not_applicable" or row.get("context_digest") != CONTEXT_SHA256:
            fail("dependency ledger invents accepted reuse")
        if not row.get("non_reuse_reason"):
            fail("weak shared-group rejection lacks a reason")
        for relative, expected in row.get("inspected_member_artifacts", {}).items():
            if digest(ROOT / relative) != expected:
                fail(f"inspected weak-group artifact changed: {relative}")
    audit = ledger.get("closure_audit", {})
    if audit.get("parent_inspection_order") != [] or audit.get("claim_order") != {
        "v2_execution_rank": 301,
        "phase_layer": 5,
        "phase_item_id": ITEM,
    }:
        fail("dependency closure audit or claim order changed")

    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    if registry.get("denominator_sha256") != REGISTRY_DENOMINATOR:
        fail("obligation denominator changed")
    if graphs.get("registry_denominator_sha256") != REGISTRY_DENOMINATOR:
        fail("typed graph denominator changed")
    if len(registry.get("obligations", [])) != 105 or len(graphs.get("nodes", [])) != 105:
        fail("frozen obligation node count changed")
    if graphs.get("composition_certificates") != []:
        fail("unaccepted composition certificates appeared")
    boundary = graphs.get("closure_boundary", {})
    if boundary.get("accepted_closed_obligations") != []:
        fail("typed graphs invent accepted closure")
    if boundary.get("root_closed") is not False or boundary.get("root_machine_debt") != "M3":
        fail("typed graph root boundary changed")

    receipt = load(HERE / "proof-receipt.json")
    for field, expected in (
        ("schema_version", "stage1-node-receipt/1.0"),
        ("item_id", "S56-M-0423-PROOF"),
        ("theorem_id", THEOREM),
        ("phase", "proof"),
        ("accepted", False),
        ("verdict", "blocked"),
        ("selftest_status", "passed"),
        ("audit_complete", False),
        ("theorem_complete", False),
    ):
        if receipt.get(field) != expected:
            fail(f"proof receipt field changed: {field}")
    result = receipt.get("result", {})
    if result.get("phase_accepted") is not False or result.get("root_kernel_closed") is not False:
        fail("proof receipt overstates phase or root closure")
    if receipt.get("closed_obligation_ids") != []:
        fail("proof receipt invents accepted obligation closure")
    if receipt.get("first_failed_gate") != "P04-KERNEL.M0423-T-LOCAL-GLOBAL":
        fail("proof receipt blocker changed")
    proof_source = strip_comments_and_strings((HERE / "Proof.lean").read_text(encoding="utf-8"))
    validation_source = strip_comments_and_strings((HERE / "Validation.lean").read_text(encoding="utf-8"))
    if PROHIBITED.search(proof_source) or PROHIBITED.search(validation_source):
        fail("prohibited proof or trust construct found")
    if re.search(r"\btheorem\s+\w+\s*:\s*LocalToGlobalObligation\b", proof_source):
        fail("unexpected local-to-global body appeared without receipt reconciliation")
    if re.search(r"\btheorem\s+\w+\s*:\s*HasseMinkowskiStatement\b", proof_source):
        fail("unexpected unconditional root body appeared without receipt reconciliation")


def verify_receipt_and_packet() -> None:
    contract = load(ROOT / "Docs/Stage1_Phase_Acceptance_Contracts.json")
    phase = next(row for row in contract["phases"] if row.get("phase") == "validation")
    receipt = load(HERE / "validation-receipt.json")
    required = {
        pointer.split("/")[-1]
        for pointer in phase["phase_receipt_required_fields"]
        if pointer.count("/") == 1
    }
    if not required <= set(receipt):
        fail("validation receipt omits contract-required fields")
    for field, expected in (
        ("schema_version", "stage1-node-receipt/1.0"),
        ("item_id", ITEM), ("theorem_id", THEOREM), ("phase", "validation"),
        ("intent", "validate"), ("base_revision", BASE_REVISION), ("base_tree", BASE_TREE),
        ("support_state", "provisional_worker_selftest"), ("proposed_state", "[_]"),
        ("accepted", False), ("verdict", "blocked"), ("selftest_status", "passed"),
        ("first_failed_gate", "G02-TOPOLOGY.S56-M-0423-PROOF"),
        ("audit_complete", False), ("theorem_complete", False),
    ):
        if receipt.get(field) != expected:
            fail(f"validation receipt field changed: {field}")
    if phase.get("raw_blocked_can_close_phase") is not False:
        fail("validation contract unexpectedly accepts a blocked packet")
    result = receipt.get("result", {})
    if result.get("exit_code") != 0 or result.get("semantic_verdict") != "repair_required":
        fail("validation receipt process or semantic result changed")
    if result.get("phase_accepted") is not False or result.get("phase_predicate_proven") is not False:
        fail("validation receipt overstates phase completion")
    if result.get("root_kernel_closed") is not False:
        fail("validation receipt overstates root closure")
    inputs = receipt.get("inputs", {})
    expected_roles = {
        "validation_sources": [{
            "path": f"Stage1_Instances/{THEOREM}/Validation.lean",
            "sha256": EXPECTED_LOCAL_INPUTS["Validation.lean"],
            "git_blob": EXPECTED_GIT_BLOBS["Validation.lean"],
        }],
        "proof_receipt": {
            "path": f"Stage1_Instances/{THEOREM}/proof-receipt.json",
            "sha256": EXPECTED_LOCAL_INPUTS["proof-receipt.json"],
            "git_blob": EXPECTED_GIT_BLOBS["proof-receipt.json"],
        },
    }
    for field, expected in expected_roles.items():
        if inputs.get(field) != expected:
            fail(f"validation receipt role binding changed: {field}")
    if inputs.get("consumer_validation_receipts") != []:
        fail("validation receipt invents hard-edge consumer reuse")
    recipe = receipt.get("recipe", {})
    spec = load(HERE / "validation-specs.json")
    if spec.get("item_id") != ITEM or spec.get("theorem_id") != THEOREM:
        fail("validation specification identity changed")
    recipes = spec.get("recipes")
    if not isinstance(recipes, list) or len(recipes) != 1:
        fail("validation specification recipe cardinality changed")
    if recipe.get("argv") != recipes[0].get("argv") or recipe.get("argv") != [
        "/usr/bin/python3", "-I", "-B", f"Stage1_Instances/{THEOREM}/check_validation.py",
    ]:
        fail("validation receipt and specification argv disagree")
    commands = receipt.get("selftest_result", {}).get("commands")
    if not isinstance(commands, list) or not commands:
        fail("validation receipt lacks self-test commands")
    packet = load(ROOT / ".stage1-worker-selftest.json")
    if set(packet) != {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "verdict", "state",
    }:
        fail("worker packet fields changed")
    if packet.get("item_id") != ITEM or packet.get("state") != "[_]":
        fail("worker packet identity or state changed")
    if packet.get("verdict") != "blocked" or packet.get("base_revision") != BASE_REVISION:
        fail("worker packet verdict or base changed")
    if packet.get("commands") != commands or packet.get("known_failures") != receipt.get("known_failures"):
        fail("worker packet and validation receipt disagree")
    expected_changed = {
        ".stage1-worker-selftest.json",
        f"Stage1_Instances/{THEOREM}/Validation.lean",
        f"Stage1_Instances/{THEOREM}/check_validation.py",
        f"Stage1_Instances/{THEOREM}/dependency-reuse-ledger.json",
        f"Stage1_Instances/{THEOREM}/validation-blocker.json",
        f"Stage1_Instances/{THEOREM}/validation-phase.md",
        f"Stage1_Instances/{THEOREM}/validation-receipt.json",
        f"Stage1_Instances/{THEOREM}/validation-specs.json",
    }
    if set(packet.get("changed_paths", [])) != expected_changed:
        fail("worker packet changed-path inventory is incomplete")
    status = subprocess.check_output(
        ["/usr/bin/git", "status", "--short", "--untracked-files=all"], cwd=ROOT, text=True
    )
    actual_changed = {
        line[3:] for line in status.splitlines()
        if line[3:] != "Formalizations/Lean/.lake"
    }
    if actual_changed != expected_changed:
        fail(f"worktree delta disagrees with worker packet: {sorted(actual_changed)}")
    for relative in expected_changed:
        data = (ROOT / relative).read_bytes()
        if not data.endswith(b"\n") or b"\r" in data or b"\x00" in data:
            fail(f"invalid text encoding or final newline: {relative}")
        if any(line.endswith((b" ", b"\t")) for line in data.splitlines()):
            fail(f"trailing whitespace: {relative}")


def verify() -> None:
    verify_authorities()
    verify_inputs()
    verify_evidence()
    verify_receipt_and_packet()
    outputs = lean_replay()
    combined = "\n".join(outputs.values())
    if "sorryAx" in combined:
        fail("trust-zero replay reported sorryAx")
    for declaration, expected in EXPECTED_AXIOMS.items():
        if printed_axioms(combined, declaration) != expected:
            fail(f"unexpected axiom profile for {declaration}")


def semantic_result(*, replay_passed: bool, message: str) -> dict[str, Any]:
    return {
        "schema_version": "stage1-validator-semantic-result/1.0",
        "item_id": ITEM,
        "theorem_id": THEOREM,
        "phase": "validation",
        "status": "blocked" if replay_passed else "failed",
        "verdict": "repair_required",
        "phase_accepted": False,
        "audit_complete": False,
        "theorem_complete": False,
        "phase_predicate_proven": False,
        "first_failed_gate": (
            "G02-TOPOLOGY.S56-M-0423-PROOF" if replay_passed else "V01-ARTIFACTS"
        ),
        "open_obligations": 94,
        "stale_inputs": [],
        "blocked": replay_passed,
        "message": message,
    }


def main() -> None:
    try:
        verify()
    except (AssertionError, KeyError, OSError, RuntimeError, ValueError) as error:
        result = semantic_result(
            replay_passed=False, message=f"validation evidence replay failed: {error}"
        )
        print(json.dumps(result, sort_keys=True, separators=(",", ":")))
        raise SystemExit(1)
    result = semantic_result(
        replay_passed=True,
        message=(
            "Trust-zero replay with no network-capable command, selected trust/provenance, empty hard-parent "
            "context, rejected weak shared groups, and target-owned differential checks passed; "
            "the proof predecessor remains unaccepted and blocked at the absent local-to-global body."
        ),
    )
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
