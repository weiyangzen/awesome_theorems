#!/usr/bin/env python3
"""Fail-closed narrow validator for S56-M-0927-VALIDATION."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import socket
import subprocess
import sys
import tempfile


if not __debug__:
    raise SystemExit("check_validation.py must run without Python optimization")


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0927"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM = "S56-M-0927-VALIDATION"
THEOREM = "THM-M-0927"
BASE_REVISION = "c93e664d3a7e0383b037cfa2d5e47ba14adfb2cb"
BASE_TREE = "d8ea21a05ed52ff43d984128352a07f479aae6e6"
TOOLCHAIN = "leanprover/lean4:v4.29.0"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MATHLIB_REMOTE = "https://github.com/leanprover-community/mathlib4.git"
MATHLIB_LICENSE_SHA256 = "b40930bbcf80744c86c46a12bc9da056641d722716c378f5659b9e555ef833e1"
TERMINAL_BLOB = "9e9a9f050354f828a54fb235846405987daa4971"
TERMINAL_SOURCE_SHA256 = "e3a6e5160e654dfb4c5594c66a624fa7a5edffa4c1b839d992be7d1ba2dd7ac3"
TERMINAL_BODY_SHA256 = "e3e11b1c82c6f3718202d10bc5fe89a811e4c0890b0dcd535014a2a6f1385814"
TERMINAL_OLEAN_SHA256 = "4d72dd79c76182da4a00619140ff0d127c815f32c258a9ea3b23e28cf345d88b"
EXPRESSION_SHA256 = "0a05e8c4976c01759ef82d364afc86f498f700edc1a0fcb3f8935765992b5a2f"
DENOMINATOR_SHA256 = "96eb539e67048140003ad8ed68e84ef0fd1daa215803f7915908af2999c373de"
EXPECTED_AXIOMS = ["propext", "Classical.choice", "Quot.sound"]
EXPECTED_CLOSURE_AXIOMS = sorted(EXPECTED_AXIOMS)
LEAN_SHA256 = "3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf"
LAKE_SHIM_SHA256 = "840179e70803ef373c2ec53342d6a45ea7d022533e4145489fc1278b4f716385"
LAKE_BINARY_SHA256 = "a608ff084d7e2af228b92a29d7c2fd083ba0580e46889175ec74a81678c98359"
PYTHON_SHA256 = "b8d8288faefdd300201f43fcf00f6f539a27218eeed3a3dff5ab10b9c4c99700"
GIT_SHA256 = "5516c9f362c29376ab9a499a33082f9f611941d8c75930c880e30ad109e39c9a"
BWRAP_SHA256 = "0abea81db798ebf6b4742ac0664802d97521547a353c2a0dbdc21d76cbbfd2c0"
TIMEOUT_SHA256 = "48893b0fb21436b54619db80486e83ef39dfccaf1aefe83dfa00c02d6146e8c0"
EXPECTED_INPUTS = {
    "Statement.lean": "72172fb6015846b808a81dfc4995767dec5381de5845f68c47cbc5fdb2eeed8d",
    "ObligationTree.lean": "b254d92e1398b4b8f144d9be31339370dd427e333998857d279c80d09debf347",
    "Proof.lean": "340f937f1222e786c41d145d8bd29ac13600eec770a1c53628eb897106f0eafb",
    "Validation.lean": "2f8bdfdd947f35f7bb2036c345a5b508f7ec929ab261df4db3549bc3df113109",
    "statement.json": "4649bc7f024d4dfd353d857ada5829b963c08da5549e060f63e9f6416a37bf95",
    "instance.json": "18fc4a8a74fd092cce4138e64c68a803e16736826262e4ce3e453d6b61693613",
    "task-dag.json": "a23b73fe4200528e269ccd7072e1917187d78207b0f525716df9a090f350df50",
    "anchor-audit.json": "166999961169125272df80df7948f19be2e31b67fc072c8ae6b66286487a1933",
    "obligation-registry.json": "93d2f3f4b48d713ace523b2049ff2aa9505f40f4332a30ca13a5f1bafdc9b05c",
    "typed-graphs.json": "3a4aca9e328628b5513e9aa788eae132fd0827ead3ace586c403b5a577888c87",
    "validation-specs.json": "75da25611b55b3e466e07c9f47c0d711a9a6c3d130b799fd5da1679cb7dccbf5",
    "proof-receipt.json": "d84a1cb91e15c73ecbf00a917f9ebab56bd0a58d107fc9a10ba2ef3915ffc8b7",
    "proof-validation.md": "f0bab569b45b0a9db2f07e9ee8f34929a38d4f53d03916842e12422166da4504",
    "check_proof.py": "99ac9d57d45594b329c43a5e4f2c8f155fcd0ae0ce61b17f2fc8f58d6f32506f",
    "source-statement-crosswalk.md": "a364820431fd8335f6ba7ea588286ed2a34c5fc657e92a2bd58e79681efd0061",
    "obligation-tree.md": "a56a8a17f8d5dca45f34fbb9253a041a9910b21b4793bda6f6e5f431a0686109",
    "README.md": "1f03059b628318458d1767b57158b6622e788eb14adba7fa488f912dac83fedf",
}
AUTHORITY_HASHES = {
    "Docs/Stage1_Blueprint_rev-5.6.md": "a8fd3d878262ba7488c9fdd75b419e4aa32a6bd1d2831c5737c0c743bd3833a5",
    "Docs/Stage1_Execution_DAG_rev-5.6.json": "e4c99404c6ce0f157d5567ac76cbac7470870ed9a25ae9d2afea24bca18859aa",
    "Docs/Stage1_Targets_rev-5.6.json": "02eec284de534dd78e1cf75f82a477ff477567dd682b7445cb7587abd137ab2c",
    "skills/execute-stage1-rev56/SKILL.md": "26d47a66c6535feabb8bbf1051fd55d76a53fe761f4b3d953f86b97ec86152b8",
    "Formalizations/Lean/lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "Formalizations/Lean/lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
DECLARATIONS = (
    "Real.coe_fib_eq'",
    "Stage1Instances.THM_M_0927.Proof.functionBinet_proof",
    "Stage1Instances.THM_M_0927.Proof.binetFormula_proof",
    "Stage1Instances.THM_M_0927.Validation.independentlyRecomposedBinetFormula",
)
PROVISIONAL_IDS = [
    "M0927-ROOT",
    "M0927-T-ROOT-COMPOSE",
    "M0927-T-FUNCTION-BINET",
    "M0927-S-FUNCTION-TRANSPORT",
    "M0927-S-RADICAL-TRANSPORT",
]
REMAINING_ASSURANCE_CUT = [
    "M0927-X-SOURCE",
    "M0927-S-FOUNDATION",
    "M0927-X-PROVENANCE",
    "M0927-X-EVIDENCE",
    "M0927-X-TRUST",
    "M0927-X-READABLE",
    "M0927-X-WORKFLOW",
]
CHANGED_PATHS = [
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/Validation.lean",
    f"Stage1_Instances/{THEOREM}/check_validation.py",
    f"Stage1_Instances/{THEOREM}/validation-phase.md",
    f"Stage1_Instances/{THEOREM}/validation-receipt.json",
    f"Stage1_Instances/{THEOREM}/validation-spec.json",
]
SUMMARY_LINES = [
    "PASS exact kernel replay: fresh trust-zero Statement, ObligationTree, Proof, and differential Validation outputs checked the frozen radical root",
    "PASS trust observation: four declarations use exactly propext, Classical.choice, and Quot.sound; root closure has no unexpected bodyless or unsafe declaration",
    "PASS selected provenance: frozen inputs, mathlib revision/tree/blob/source/body/olean, license, tool identities, and clean pinned package agree",
    "FAIL CLOSED dependency authority: proof remains provisional [_] rather than master accepted",
    "FAIL CLOSED complete trust/provenance: accepted foundation policy and complete transitive TCB, origin, compiled-artifact, and SBOM closure are absent",
    "FAIL CLOSED hermetic/independent: network-isolated fresh outputs reuse the shared warm cache and same-worker recomposition is not distinct signed verification",
    "accepted root remains H1/M3/R4; audit_complete=false; theorem_complete=false",
]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def hash_slice(path: Path, start: int, end: int) -> str:
    lines = path.read_bytes().splitlines(keepends=True)
    return hashlib.sha256(b"".join(lines[start - 1:end])).hexdigest()


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


def run(
    argv: list[str], *, cwd: Path = ROOT, env: dict[str, str] | None = None,
    timeout: int = 1800,
) -> str:
    result = subprocess.run(
        argv, cwd=cwd, env=env, text=True, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, timeout=timeout, check=False,
    )
    if result.returncode:
        sys.stdout.write(result.stdout)
        raise SystemExit(result.returncode)
    return result.stdout


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["/usr/bin/git", *args], cwd=cwd).strip()


def source_without_comments_or_strings(source: str) -> str:
    output: list[str] = []
    index = depth = 0
    in_string = escaped = False
    while index < len(source):
        pair = source[index:index + 2]
        char = source[index]
        if depth:
            if pair == "/-":
                depth += 1
                index += 2
            elif pair == "-/":
                depth -= 1
                index += 2
            else:
                output.append("\n" if char == "\n" else " ")
                index += 1
        elif in_string:
            output.append("\n" if char == "\n" else " ")
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
            index += 1
        elif pair == "/-":
            depth = 1
            index += 2
        elif pair == "--":
            newline = source.find("\n", index)
            if newline < 0:
                output.extend(" " * (len(source) - index))
                index = len(source)
            else:
                output.extend(" " * (newline - index))
                index = newline
        elif char == '"':
            in_string = True
            index += 1
        else:
            output.append(char)
            index += 1
    assert depth == 0 and not in_string
    return "".join(output)


def reported_axioms(output: str, declaration: str) -> list[str]:
    match = re.search(
        re.escape(f"'{declaration}' depends on axioms:") + r"\s*\[([^]]*)]",
        output, re.DOTALL,
    )
    assert match is not None, declaration
    return [part.strip() for part in match.group(1).split(",") if part.strip()]


def check_network_isolation() -> None:
    assert os.environ.get("STAGE1_OUTER_NETWORK_ISOLATED") == "1"
    interfaces = Path("/proc/net/dev").read_text(encoding="utf-8")
    assert all(
        line.strip().startswith("lo:")
        for line in interfaces.splitlines()[2:] if line.strip()
    ), interfaces
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.2)
    try:
        code = sock.connect_ex(("1.1.1.1", 53))
    finally:
        sock.close()
    assert code != 0, "network-denial mutation unexpectedly connected"


def replay_lean() -> dict:
    lake_link = LEAN_ROOT / ".lake"
    assert lake_link.is_symlink()
    lake_target = lake_link.resolve(strict=True)
    before_stat = lake_target.stat()
    before_head = git("rev-parse", "HEAD", cwd=MATHLIB)
    before_status = git("status", "--porcelain=v1", "--untracked-files=all", cwd=MATHLIB)
    discovery_env = os.environ | {"ELAN_TOOLCHAIN": TOOLCHAIN}
    lean_path = run(
        ["/home/sansha-2/.elan/bin/lake", "env", "printenv", "LEAN_PATH"],
        cwd=LEAN_ROOT, env=discovery_env,
    ).strip()
    lean_bin = Path(run(
        ["/home/sansha-2/.elan/bin/lake", "env", "which", "lean"],
        cwd=LEAN_ROOT, env=discovery_env,
    ).strip())
    lake_bin = Path(run(
        ["/home/sansha-2/.elan/bin/lake", "env", "which", "lake"],
        cwd=LEAN_ROOT, env=discovery_env,
    ).strip())
    assert sha256(lean_bin) == LEAN_SHA256
    assert sha256(Path("/home/sansha-2/.elan/bin/lake")) == LAKE_SHIM_SHA256
    assert sha256(lake_bin) == LAKE_BINARY_SHA256
    assert sha256(Path("/usr/bin/python3")) == PYTHON_SHA256
    assert sha256(Path("/usr/bin/git")) == GIT_SHA256
    assert sha256(Path("/usr/bin/bwrap")) == BWRAP_SHA256
    assert sha256(Path("/usr/bin/timeout")) == TIMEOUT_SHA256
    version = run([str(lean_bin), "--version"], env=discovery_env).strip()
    assert "Lean (version 4.29.0" in version and LEAN_COMMIT in version
    outputs: dict[str, str] = {}
    with tempfile.TemporaryDirectory(prefix="thm-m-0927-validation-") as temporary:
        temp = Path(temporary)
        empty_home = temp / "home"
        empty_home.mkdir()
        env = {
            "HOME": str(empty_home),
            "LEAN_PATH": lean_path,
            "LANG": "C.UTF-8",
            "LC_ALL": "C.UTF-8",
            "TZ": "UTC",
            "NO_COLOR": "1",
            "LEAN_NUM_THREADS": "1",
        }
        outputs["statement"] = run(
            [str(lean_bin), "--trust=0", "Statement.lean", "-o", str(temp / "Statement.olean")],
            cwd=HERE, env=env,
        )
        local_env = env | {"LEAN_PATH": str(temp) + os.pathsep + lean_path}
        outputs["tree"] = run(
            [str(lean_bin), "--trust=0", "ObligationTree.lean", "-o", str(temp / "ObligationTree.olean")],
            cwd=HERE, env=local_env,
        )
        outputs["proof"] = run(
            [str(lean_bin), "--trust=0", "Proof.lean", "-o", str(temp / "Proof.olean")],
            cwd=HERE, env=local_env,
        )
        outputs["validation"] = run(
            [str(lean_bin), "--trust=0", "Validation.lean"], cwd=HERE, env=local_env,
        )
    assert lake_link.resolve(strict=True) == lake_target
    assert lake_target.stat() == before_stat
    assert git("rev-parse", "HEAD", cwd=MATHLIB) == before_head
    assert git("status", "--porcelain=v1", "--untracked-files=all", cwd=MATHLIB) == before_status
    outputs["lean_bin"] = str(lean_bin)
    outputs["lean_version"] = version
    return outputs


def inspect_outputs(outputs: dict) -> dict:
    proof = outputs["proof"]
    validation = outputs["validation"]
    for declaration in DECLARATIONS[:3]:
        assert reported_axioms(proof, declaration) == EXPECTED_AXIOMS
    assert reported_axioms(validation, DECLARATIONS[3]) == EXPECTED_AXIOMS
    assert proof.count("Declarations are sorry-free!") == 3
    assert validation.count("Declarations are sorry-free!") == 4
    combined = "\n".join(outputs[key] for key in ("statement", "tree", "proof", "validation"))
    assert "declaration uses 'sorry'" not in combined and "sorryAx" not in combined
    closure = re.search(
        r"VALIDATION_CLOSURE declarations=(\d+) modules=(\d+).*?"
        r"VALIDATION_CLOSURE axioms=\[([^]]*)].*?"
        r"VALIDATION_CLOSURE unexpected_bodyless=\[([^]]*)].*?"
        r"VALIDATION_CLOSURE unsafe=\[([^]]*)]",
        validation, re.DOTALL,
    )
    assert closure is not None
    closure_axioms = sorted(part.strip() for part in closure.group(3).split(",") if part.strip())
    assert closure_axioms == EXPECTED_CLOSURE_AXIOMS
    assert closure.group(4).strip() == "" and closure.group(5).strip() == ""
    semantic_output = {
        "statement": {
            "mutation_type_mismatches": outputs["statement"].count("Type mismatch"),
            "axiom_reports": outputs["statement"].count("depends on axioms:"),
            "canonical_target_printed": (
                "def Stage1Instances.THM_M_0927.BinetFormulaTarget : Prop" in outputs["statement"]
            ),
        },
        "tree": {
            "checked_interfaces": outputs["tree"].count("Stage1Instances.THM_M_0927.ObligationTree."),
            "axiom_reports": outputs["tree"].count("depends on axioms:"),
            "sorry_free_reports": outputs["tree"].count("Declarations are sorry-free!"),
        },
        "proof": {
            "axioms": {name: reported_axioms(outputs["proof"], name) for name in DECLARATIONS[:3]},
            "sorry_free_reports": outputs["proof"].count("Declarations are sorry-free!"),
        },
        "validation": {
            "axioms": {
                name: reported_axioms(outputs["validation"], name)
                for name in DECLARATIONS
            },
            "sorry_free_reports": outputs["validation"].count("Declarations are sorry-free!"),
            "closure_declaration_count": int(closure.group(1)),
            "closure_module_count": int(closure.group(2)),
            "closure_bodyless_nonaxioms": [],
            "closure_unsafe_declarations": [],
        },
    }
    return {
        "lean_semantic_output_sha256": hashlib.sha256(
            json.dumps(semantic_output, sort_keys=True, separators=(",", ":")).encode()
        ).hexdigest(),
        "closure_declaration_count": int(closure.group(1)),
        "closure_module_count": int(closure.group(2)),
        "closure_bodyless_nonaxioms": [],
        "closure_unsafe_declarations": [],
    }


def check_static_inputs(probe: bool) -> tuple[dict, dict, dict]:
    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    for relative, expected in EXPECTED_INPUTS.items():
        assert sha256(HERE / relative) == expected, relative
    for relative, expected in AUTHORITY_HASHES.items():
        assert sha256(ROOT / relative) == expected, relative

    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item == {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 1546,
        "phase": "validation",
        "layer": 5,
        "state": "[ ]",
        "depends_on": ["S56-M-0927-PROOF"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Run hermetic kernel, trust, provenance, and independent validation gates.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }
    predecessor = next(row for row in execution["items"] if row["id"] == "S56-M-0927-PROOF")
    assert predecessor["state"] == "[_]"

    statement = load(HERE / "statement.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    instance = load(HERE / "instance.json")
    local_dag = load(HERE / "task-dag.json")
    proof_receipt = load(HERE / "proof-receipt.json")
    spec = load(HERE / "validation-spec.json")
    assert statement["canonical_formal_target"]["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert graphs["root_node_id"] == registry["root_obligation_id"] == "M0927-ROOT"
    assert graphs["closure_boundary"]["accepted_closed_obligations"] == []
    assert graphs["closure_boundary"]["accepted_root_machine_debt"] == "M3"
    assert graphs["closure_boundary"]["theorem_complete"] is False
    assert instance["root_vector"] == {"H": "H1", "M": "M3", "R": "R4"}
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == []
    assert instance["audit_complete"] is instance["theorem_complete"] is False
    assert local_dag["accepted_states"] == []
    assert all(task["state"] == "open" for task in local_dag["tasks"])
    assert proof_receipt["accepted"] is False and proof_receipt["proposed_state"] == "[_]"
    assert proof_receipt["result"]["root_kernel_closed"] is True
    assert proof_receipt["result"]["accepted_root_closed"] is False
    assert proof_receipt["root_evidence"]["exact_declaration_evidence_ids"] == PROVISIONAL_IDS
    assert proof_receipt["remaining_assurance_cut_set"] == REMAINING_ASSURANCE_CUT
    assert spec["item_id"] == ITEM and spec["theorem_id"] == THEOREM
    assert spec["phase"] == "validation" and len(spec["recipes"]) == 1

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|implemented_by|native_decide|run_tac)\b|"
        r"^[ \t]*(?:axiom|constant|opaque|unsafe|extern)\b",
        re.MULTILINE,
    )
    for filename in ("Statement.lean", "AnchorAudit.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
        clean = source_without_comments_or_strings((HERE / filename).read_text(encoding="utf-8"))
        assert prohibited.search(clean) is None, filename

    terminal = MATHLIB / "Mathlib/NumberTheory/Real/GoldenRatio.lean"
    terminal_olean = MATHLIB / ".lake/build/lib/lean/Mathlib/NumberTheory/Real/GoldenRatio.olean"
    assert git("rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert git("remote", "get-url", "origin", cwd=MATHLIB) == MATHLIB_REMOTE
    assert git("status", "--porcelain=v1", "--untracked-files=all", cwd=MATHLIB) == ""
    assert git("rev-parse", "HEAD:Mathlib/NumberTheory/Real/GoldenRatio.lean", cwd=MATHLIB) == TERMINAL_BLOB
    assert sha256(terminal) == TERMINAL_SOURCE_SHA256
    assert hash_slice(terminal, 180, 195) == TERMINAL_BODY_SHA256
    assert sha256(terminal_olean) == TERMINAL_OLEAN_SHA256
    assert sha256(MATHLIB / "LICENSE") == MATHLIB_LICENSE_SHA256

    if not probe:
        receipt = load(HERE / "validation-receipt.json")
        packet = load(ROOT / ".stage1-worker-selftest.json")
        assert receipt["item_id"] == packet["item_id"] == ITEM
        assert receipt["base_revision"] == packet["base_revision"] == BASE_REVISION
        assert receipt["base_tree"] == BASE_TREE
        assert receipt["proposed_state"] == packet["state"] == "[_]"
        assert receipt["accepted"] is False and receipt["verdict"] == "blocked"
        assert receipt["changed_paths"] == packet["changed_paths"] == CHANGED_PATHS
        assert receipt["known_failures"] == packet["known_failures"]
        assert receipt["output_summary"] == packet["output_summary"]
        assert receipt["validator_inputs"]["check_validation_sha256"] == sha256(HERE / "check_validation.py")
        assert receipt["validator_inputs"]["validation_spec_sha256"] == sha256(HERE / "validation-spec.json")
        actual = {
            line[3:] for line in git("status", "--short", "--untracked-files=all").splitlines()
            if line[3:] != "Formalizations/Lean/.lake"
        }
        assert actual == set(CHANGED_PATHS), (actual, CHANGED_PATHS)
    return proof_receipt, spec, instance


def validate_receipt(observation: dict) -> None:
    receipt = load(HERE / "validation-receipt.json")
    assert receipt["result"]["lean_semantic_output_sha256"] == observation[
        "lean_semantic_output_sha256"
    ]
    assert receipt["result"]["closure_declaration_count"] == observation["closure_declaration_count"]
    assert receipt["result"]["closure_module_count"] == observation["closure_module_count"]
    assert receipt["result"]["observed_axioms"] == sorted(EXPECTED_AXIOMS)
    assert receipt["result"]["accepted_closed_obligation_ids"] == []
    assert receipt["result"]["accepted_root_machine_debt"] == "M3"
    assert receipt["result"]["accepted_state_changed"] is False
    assert receipt["result"]["audit_complete"] is receipt["result"]["theorem_complete"] is False
    assert receipt["trust"]["decision"] == "fail_closed"
    assert receipt["provenance"]["complete_provenance_gate"] == "fail_closed"
    assert receipt["hermeticity"]["decision"] == "fail_closed"
    assert receipt["independent_validation"]["decision"] == "fail_closed"
    assert receipt["first_failed_gate"] == "dependency.S56-M-0927-PROOF.master_acceptance"
    assert receipt["remaining_root_cut_set"] == REMAINING_ASSURANCE_CUT


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--probe", action="store_true")
    args = parser.parse_args()
    check_static_inputs(args.probe)
    check_network_isolation()
    outputs = replay_lean()
    observation = inspect_outputs(outputs)
    if not args.probe:
        validate_receipt(observation)
    for relative in CHANGED_PATHS:
        if args.probe and not (ROOT / relative).exists():
            continue
        data = (ROOT / relative).read_bytes()
        assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())
    print("PASS THM-M-0927 narrow validation")
    for line in SUMMARY_LINES:
        print(line)


if __name__ == "__main__":
    main()
