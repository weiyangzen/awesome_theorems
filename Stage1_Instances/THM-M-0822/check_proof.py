#!/usr/bin/env python3
"""Fail-closed exact-proof, pin, graph, receipt, and worker-packet checks."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile


if not __debug__:
    raise SystemExit("check_proof.py must run without Python optimization")


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ITEM = "S56-M-0822-PROOF"
THEOREM = "THM-M-0822"
BASE_REVISION = "8cfd5229cfb37c4199bfe53eb119c41667c21dc1"
BASE_TREE = "eaabd11d8998cd8462d62808d48ffc4af5912a2b"
EXPRESSION_SHA256 = "646e9860afcf5efd962b6f69c9c2825220f23418d05f7675490b783e63afe209"
DENOMINATOR_SHA256 = "40ff944c9434231f2656a60ff306e27b69ef6fe302df8dc1bd56f89d314a8f15"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MATHLIB_SOURCE = "Mathlib/Combinatorics/SetFamily/KruskalKatona.lean"
MATHLIB_SOURCE_BLOB = "f388fc0bfd201e1d9eb1279b5bd1c6dcbd253b34"
MATHLIB_SOURCE_SHA256 = "c6351d7ee422db9eed8f45335f4128eb3a66fe09997d12abc15eba38e9863f1c"
MATHLIB_OLEAN_SHA256 = "96e8f29576d4353c3fa6450edc9bb096454f80512eb778c1c5da7599cd0c584a"
EKR_BODY_SHA256 = "bafaad9695ea929dc30acd5dbc1275c48eb5d062b99c56e0ddd2013374e783c0"
LAKE_MANIFEST_SHA256 = "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81"
LEAN_EXECUTABLE_SHA256 = "3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf"
MACHINE_PROOF_IDS = [
    "M0822-ROOT",
    "M0822-T-ASSEMBLE",
    "M0822-T-ATTAINMENT",
    "M0822-C-STAR",
    "M0822-L-STAR-IMAGE",
    "M0822-L-STAR-INTERSECTING",
    "M0822-L-STAR-SIZED",
    "M0822-L-STAR-CARD",
    "M0822-L-GROUND-ELEMENT",
    "M0822-T-UPPER-ADAPTER",
    "M0822-T-MATHLIB-EKR",
]
PROOF_REQUIRES = {
    ("M0822-ROOT", "M0822-T-ASSEMBLE"),
    ("M0822-T-ASSEMBLE", "M0822-T-ATTAINMENT"),
    ("M0822-T-ASSEMBLE", "M0822-T-UPPER-ADAPTER"),
    ("M0822-T-ATTAINMENT", "M0822-C-STAR"),
    ("M0822-T-ATTAINMENT", "M0822-L-STAR-INTERSECTING"),
    ("M0822-T-ATTAINMENT", "M0822-L-STAR-SIZED"),
    ("M0822-T-ATTAINMENT", "M0822-L-STAR-CARD"),
    ("M0822-C-STAR", "M0822-L-GROUND-ELEMENT"),
    ("M0822-L-STAR-CARD", "M0822-L-STAR-IMAGE"),
    ("M0822-T-UPPER-ADAPTER", "M0822-T-MATHLIB-EKR"),
}
COMPOSITION_DECLARATIONS = {
    "M0822-ROOT": "Stage1Instances.THM_M_0822.ObligationTree.rootOfExactAssembly",
    "M0822-T-ASSEMBLE": "Stage1Instances.THM_M_0822.ObligationTree.composeRoot",
    "M0822-T-ATTAINMENT": (
        "Stage1Instances.THM_M_0822.ObligationTree.attainment_of_starPackages"
    ),
    "M0822-C-STAR": (
        "Stage1Instances.THM_M_0822.ObligationTree.starConstruction_of_groundElement"
    ),
    "M0822-L-STAR-CARD": "Stage1Instances.THM_M_0822.ObligationTree.starCard_of_image",
    "M0822-T-UPPER-ADAPTER": (
        "Stage1Instances.THM_M_0822.ObligationTree.upperBound_of_mathlibTerminal"
    ),
}
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/Proof.lean",
    f"Stage1_Instances/{THEOREM}/check_proof.py",
    f"Stage1_Instances/{THEOREM}/check_proof.sh",
    f"Stage1_Instances/{THEOREM}/proof-receipt.json",
    f"Stage1_Instances/{THEOREM}/proof-validation.md",
}


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict), path
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sha256_lines(path: Path, start: int, end: int) -> str:
    lines = path.read_bytes().splitlines(keepends=True)
    return hashlib.sha256(b"".join(lines[start - 1 : end])).hexdigest()


def git(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(["git", *args], cwd=cwd, text=True).strip()


def without_comments(source: str) -> str:
    source = re.sub(r"/-.*?-/", "", source, flags=re.DOTALL)
    return re.sub(r"--.*", "", source)


def run_lean() -> str:
    lean_root = ROOT / "Formalizations/Lean"
    lean_bin = subprocess.check_output(
        ["lake", "env", "which", "lean"], cwd=lean_root, text=True
    ).strip()
    lean_path = subprocess.check_output(
        ["lake", "env", "printenv", "LEAN_PATH"], cwd=lean_root, text=True
    ).strip()
    with tempfile.TemporaryDirectory(prefix="thm-m-0822-proof-") as temporary:
        environment = os.environ | {"LEAN_PATH": lean_path}
        for source, output_name in (
            (HERE / "Statement.lean", "Statement.olean"),
            (HERE / "ObligationTree.lean", "ObligationTree.olean"),
        ):
            result = subprocess.run(
                [
                    lean_bin,
                    "-j",
                    "1",
                    str(source),
                    "-o",
                    str(Path(temporary) / output_name),
                ],
                cwd=ROOT,
                env=environment,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                timeout=240,
                check=False,
            )
            if result.returncode:
                sys.stdout.write(result.stdout)
                raise SystemExit(result.returncode)
            environment = environment | {
                "LEAN_PATH": temporary + os.pathsep + lean_path
            }
        result = subprocess.run(
            [lean_bin, "-j", "1", str(HERE / "Proof.lean")],
            cwd=ROOT,
            env=environment,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=240,
            check=False,
        )
    if result.returncode:
        sys.stdout.write(result.stdout)
        raise SystemExit(result.returncode)
    return result.stdout


def check_lean_output(output: str) -> None:
    declarations = (
        "Finset.erdos_ko_rado",
        "Stage1Instances.THM_M_0822.Proof.groundElement",
        "Stage1Instances.THM_M_0822.Proof.starConstruction",
        "Stage1Instances.THM_M_0822.Proof.starImage",
        "Stage1Instances.THM_M_0822.Proof.starIntersecting",
        "Stage1Instances.THM_M_0822.Proof.starSized",
        "Stage1Instances.THM_M_0822.Proof.starCard",
        "Stage1Instances.THM_M_0822.Proof.starAttainment",
        "Stage1Instances.THM_M_0822.Proof.mathlibUpperBound",
        "Stage1Instances.THM_M_0822.Proof.universalUpperBound",
        "Stage1Instances.THM_M_0822.Proof.exactAssembly",
        "Stage1Instances.THM_M_0822.Proof.erdosKoRadoMaximum",
    )
    assert output.count("Declarations are sorry-free!") == len(declarations)
    for declaration in declarations:
        match = re.search(
            re.escape(f"'{declaration}' depends on axioms:") + r"\s*\[([^]]*)\]",
            output,
        )
        assert match is not None, declaration
        axioms = [name.strip() for name in match.group(1).split(",") if name.strip()]
        assert set(axioms) <= {"propext", "Classical.choice", "Quot.sound"}, (
            declaration,
            axioms,
        )
    assert (
        "Stage1Instances.THM_M_0822.Proof.erdosKoRadoMaximum : "
        "ErdosKoRadoMaximumTarget"
    ) in output
    assert "declaration uses 'sorry'" not in output
    assert "sorryAx" not in output and "error:" not in output


def main() -> None:
    proof_path = HERE / "Proof.lean"
    proof = proof_path.read_text(encoding="utf-8")
    receipt = load(HERE / "proof-receipt.json")
    statement = load(HERE / "statement.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    instance = load(HERE / "instance.json")
    local_dag = load(HERE / "task-dag.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item["theorem_id"] == THEOREM and item["execution_rank"] == 1380
    assert item["phase"] == "proof" and item["layer"] == 4
    assert item["state"] == "[ ]" and item["attempts"] == 0
    assert item["depends_on"] == ["S56-M-0822-OBLIGATION_TREE"]
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM}"]
    assert item["deliverable"] == (
        "Implement or pin/import the required proof bodies without placeholders."
    )
    predecessor = next(
        row for row in execution["items"]
        if row["id"] == "S56-M-0822-OBLIGATION_TREE"
    )
    assert predecessor["state"] == "[_]"
    local_task = next(row for row in local_dag["tasks"] if row["id"] == ITEM)
    assert local_task["state"] == "open" and local_dag["accepted_states"] == []

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|implemented_by|native_decide|extern)\b|"
        r"^[ \t]*(?:axiom|constant|opaque|unsafe)\b",
        re.MULTILINE,
    )
    assert prohibited.search(without_comments(proof)) is None
    for marker in (
        "import ObligationTree",
        "theorem groundElement : GroundElementPackage",
        "theorem starConstruction : StarConstructionPackage",
        "starConstruction_of_groundElement groundElement",
        "theorem starImage : StarImagePackage",
        "theorem starIntersecting : StarIntersectingPackage",
        "theorem starSized : StarSizedPackage",
        "theorem starCard : StarCardPackage",
        "starCard_of_image starImage",
        "theorem starAttainment : AttainmentPackage",
        "attainment_of_starPackages starConstruction starIntersecting starSized starCard",
        "theorem mathlibUpperBound : MathlibUpperBoundTerminal",
        "theorem universalUpperBound : UpperBoundPackage",
        "upperBound_of_mathlibTerminal mathlibUpperBound",
        "theorem exactAssembly : ExactAssembly",
        "composeRoot starAttainment universalUpperBound",
        "theorem erdosKoRadoMaximum",
        "rootOfExactAssembly exactAssembly",
        "assert_no_sorry Finset.erdos_ko_rado",
        "#print sorries erdosKoRadoMaximum",
        "#print axioms erdosKoRadoMaximum",
    ):
        assert marker in proof, marker

    formal = statement["canonical_formal_target"]
    assert formal["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert formal["declaration_or_expression"] == (
        "Stage1Instances.THM_M_0822.ErdosKoRadoMaximumTarget"
    )
    assert registry["root_obligation_id"] == "M0822-ROOT"
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert registry["frozen_denominators"]["required_machine"] == MACHINE_PROOF_IDS
    assert registry["status_observed_after_freeze"]["accepted_closed_obligations"] == []
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == []
    assert instance["root_vector"] == {"H": "H1", "M": "M3", "R": "R4"}
    assert instance["theorem_complete"] is False

    proof_edges = graphs["graphs"]["proof"]["edges"]
    proof_requires = {
        (edge["from"], edge["to"])
        for edge in proof_edges
        if edge["type"] == "proof_requires"
    }
    composes = {
        (edge["to"], edge["from"])
        for edge in proof_edges
        if edge["type"] == "composes"
    }
    assert proof_requires == composes == PROOF_REQUIRES
    reachable: set[str] = set()
    pending = ["M0822-ROOT"]
    while pending:
        obligation = pending.pop()
        if obligation in reachable:
            continue
        reachable.add(obligation)
        pending.extend(child for parent, child in proof_requires if parent == obligation)
    assert reachable == set(MACHINE_PROOF_IDS)
    assert graphs["unverified_decomposition_plans"] == []
    certificates = {
        row["parent_obligation_id"]: row for row in graphs["composition_certificates"]
    }
    assert set(certificates) == set(COMPOSITION_DECLARATIONS)
    for parent, declaration in COMPOSITION_DECLARATIONS.items():
        certificate = certificates[parent]
        assert certificate["declaration"] == declaration
        assert certificate["introduces_undeclared_premises"] is False
        assert set(certificate["required_child_ids"]) == {
            child for edge_parent, child in PROOF_REQUIRES if edge_parent == parent
        }

    expected_evidence_declarations = {
        "M0822-ROOT": "Stage1Instances.THM_M_0822.Proof.erdosKoRadoMaximum",
        "M0822-T-ASSEMBLE": "Stage1Instances.THM_M_0822.Proof.exactAssembly",
        "M0822-T-ATTAINMENT": "Stage1Instances.THM_M_0822.Proof.starAttainment",
        "M0822-C-STAR": "Stage1Instances.THM_M_0822.Proof.starConstruction",
        "M0822-L-STAR-IMAGE": "Stage1Instances.THM_M_0822.Proof.starImage",
        "M0822-L-STAR-INTERSECTING": (
            "Stage1Instances.THM_M_0822.Proof.starIntersecting"
        ),
        "M0822-L-STAR-SIZED": "Stage1Instances.THM_M_0822.Proof.starSized",
        "M0822-L-STAR-CARD": "Stage1Instances.THM_M_0822.Proof.starCard",
        "M0822-L-GROUND-ELEMENT": "Stage1Instances.THM_M_0822.Proof.groundElement",
        "M0822-T-UPPER-ADAPTER": (
            "Stage1Instances.THM_M_0822.Proof.universalUpperBound"
        ),
        "M0822-T-MATHLIB-EKR": (
            "Stage1Instances.THM_M_0822.Proof.mathlibUpperBound"
        ),
    }

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == packet["item_id"] == ITEM
    assert receipt["theorem_id"] == THEOREM and receipt["phase"] == "proof"
    assert receipt["intent"] == "prove"
    assert receipt["base_revision"] == packet["base_revision"] == BASE_REVISION
    assert receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["content_addressed"] is False
    assert receipt["canonical_target_expression_sha256"] == EXPRESSION_SHA256
    assert receipt["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert receipt["provisionally_closed_proof_obligation_ids"] == MACHINE_PROOF_IDS
    assert receipt["required_machine_open_ids"] == []
    assert receipt["accepted_closed_obligation_ids"] == []
    terminal_boundary = receipt["terminal_body_boundary"]
    assert terminal_boundary["frozen_distinct_terminal_body_count"] == 10
    assert terminal_boundary["accepted_terminal_body_ids"] == []
    assert terminal_boundary["proof_phase_terminal_body_acceptance_claimed"] is False
    assert set(receipt["changed_paths"]) == CHANGED_PATHS
    assert receipt["proof_body"]["source_sha256"] == sha256(proof_path)
    proof_body = receipt["proof_body"]
    assert proof_body["terminal_declaration"] == "Finset.erdos_ko_rado"
    assert proof_body["terminal_revision"] == MATHLIB_REVISION
    assert proof_body["terminal_source"] == MATHLIB_SOURCE
    assert proof_body["terminal_source_blob"] == MATHLIB_SOURCE_BLOB
    assert proof_body["terminal_source_sha256"] == MATHLIB_SOURCE_SHA256
    assert proof_body["terminal_olean_sha256"] == MATHLIB_OLEAN_SHA256
    assert proof_body["terminal_body_lines"] == "343-390"
    assert proof_body["terminal_body_sha256"] == EKR_BODY_SHA256
    for key, filename in (
        ("statement_sha256", "Statement.lean"),
        ("obligation_tree_sha256", "ObligationTree.lean"),
        ("obligation_registry_sha256", "obligation-registry.json"),
        ("typed_graphs_sha256", "typed-graphs.json"),
        ("anchor_audit_sha256", "anchor-audit.json"),
        ("validation_specs_sha256", "validation-specs.json"),
        ("check_proof_py_sha256", "check_proof.py"),
        ("check_proof_sh_sha256", "check_proof.sh"),
        ("proof_validation_sha256", "proof-validation.md"),
    ):
        assert receipt["inputs"][key] == sha256(HERE / filename)
    assert receipt["inputs"]["worker_packet_sha256"] == sha256(
        ROOT / ".stage1-worker-selftest.json"
    )
    evidence = {
        row["obligation_id"]: row for row in receipt["provisional_obligation_evidence"]
    }
    assert list(evidence) == MACHINE_PROOF_IDS
    registry_rows = {row["obligation_id"]: row for row in registry["obligations"]}
    for obligation in MACHINE_PROOF_IDS:
        assert evidence[obligation]["statement_fingerprint"] == (
            registry_rows[obligation]["statement_fingerprint"]
        )
        assert evidence[obligation]["declarations"]
        assert expected_evidence_declarations[obligation] in (
            evidence[obligation]["declarations"]
        )
    composition = receipt["proof_graph_composition"]
    assert composition["all_required_proof_edges_consumed"] is True
    assert composition["unverified_decomposition_count"] == 0
    assert composition["checked_composition_certificate_count"] == 6
    assert {
        row["parent_obligation_id"]: row["declaration"]
        for row in composition["certificates"]
    } == COMPOSITION_DECLARATIONS
    for row in composition["certificates"]:
        assert set(row["required_child_ids"]) == {
            child
            for parent, child in PROOF_REQUIRES
            if parent == row["parent_obligation_id"]
        }

    recipe = receipt["recipe"]
    assert recipe["recipe_id"] == "S56-M-0822-PROOF-LEAN"
    assert recipe["cwd"] == "."
    assert recipe["argv"] == [
        "bash", "Stage1_Instances/THM-M-0822/check_proof.sh"
    ]
    assert recipe["env_allowlist"] == {
        "LEAN_NUM_THREADS": "1",
        "LANG": "C.UTF-8",
        "LC_ALL": "C.UTF-8",
        "TZ": "UTC",
        "ambient_runner_environment": "inherited_for_nonrelease_worker_evidence",
    }
    assert recipe["timeout_seconds"] == 240
    assert recipe["network_policy"] == (
        "not_used_but_not_os_enforced_in_worker_clone"
    )
    assert recipe["expected_exit"] == 0
    assert recipe["covered_obligation_ids"] == MACHINE_PROOF_IDS
    assert set(recipe["covered_declarations"]) == {
        "Finset.erdos_ko_rado",
        "Stage1Instances.THM_M_0822.Proof.groundElement",
        "Stage1Instances.THM_M_0822.Proof.starConstruction",
        "Stage1Instances.THM_M_0822.Proof.starImage",
        "Stage1Instances.THM_M_0822.Proof.starIntersecting",
        "Stage1Instances.THM_M_0822.Proof.starSized",
        "Stage1Instances.THM_M_0822.Proof.starCard",
        "Stage1Instances.THM_M_0822.Proof.starAttainment",
        "Stage1Instances.THM_M_0822.Proof.mathlibUpperBound",
        "Stage1Instances.THM_M_0822.Proof.universalUpperBound",
        "Stage1Instances.THM_M_0822.Proof.exactAssembly",
        "Stage1Instances.THM_M_0822.Proof.erdosKoRadoMaximum",
    }
    result = receipt["result"]
    assert result["exit_code"] == 0
    assert result["axioms"] == ["propext", "Classical.choice", "Quot.sound"]
    assert result["root_kernel_closed"] is True
    assert result["accepted_root_closed"] is False
    assert result["theorem_complete"] is False
    assert receipt["proposed_root_vector_after_proof_node_acceptance"] == {
        "H": "H1", "M": "M3", "R": "R4"
    }
    assert receipt["eligible_root_vector_after_E1_and_downstream_acceptance"] == {
        "H": "H1", "M": "M0-class-pending", "R": "R4"
    }
    lean_root = ROOT / "Formalizations/Lean"
    assert receipt["inputs"]["lake_manifest_sha256"] == sha256(
        lean_root / "lake-manifest.json"
    ) == LAKE_MANIFEST_SHA256
    lean_bin = Path(
        subprocess.check_output(
            ["lake", "env", "which", "lean"], cwd=lean_root, text=True
        ).strip()
    )
    assert receipt["environment"]["lean_executable_sha256"] == sha256(
        lean_bin
    ) == LEAN_EXECUTABLE_SHA256

    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    source = mathlib / MATHLIB_SOURCE
    olean = mathlib / ".lake/build/lib/lean/Mathlib/Combinatorics/SetFamily/KruskalKatona.olean"
    assert git("rev-parse", "HEAD", cwd=mathlib) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == MATHLIB_TREE
    assert git("status", "--porcelain=v1", cwd=mathlib) == ""
    assert git("rev-parse", f"HEAD:{MATHLIB_SOURCE}", cwd=mathlib) == MATHLIB_SOURCE_BLOB
    assert sha256(source) == MATHLIB_SOURCE_SHA256
    assert sha256(olean) == MATHLIB_OLEAN_SHA256
    assert sha256_lines(source, 343, 390) == EKR_BODY_SHA256
    body = b"".join(source.read_bytes().splitlines(keepends=True)[342:390]).decode()
    assert prohibited.search(without_comments(body)) is None
    for marker in (
        "theorem erdos_ko_rado",
        "Nat.eq_zero_or_pos r",
        "kruskal_katona_lovasz_form",
        "Set.Sized.card_le",
    ):
        assert marker in body

    lean_log = os.environ.get("THM_M_0822_LEAN_LOG")
    captured_output = (
        Path(lean_log).read_text(encoding="utf-8") if lean_log else None
    )
    lean_output = run_lean()
    if captured_output is not None:
        assert captured_output == lean_output
    check_lean_output(lean_output)
    lean_output_bytes = lean_output.encode("utf-8")
    assert result["lean_stdout_sha256"] == hashlib.sha256(
        lean_output_bytes
    ).hexdigest()
    assert result["lean_stdout_bytes"] == len(lean_output_bytes)
    assert result["lean_stderr"] == (
        "merged_into_stdout_by_nonrelease_worker_runner; "
        "no independent stderr digest claimed"
    )

    assert set(packet) == {
        "item_id",
        "changed_paths",
        "commands",
        "output_summary",
        "base_revision",
        "known_failures",
        "state",
    }
    assert packet["state"] == "[_]"
    assert set(packet["changed_paths"]) == CHANGED_PATHS
    assert packet["known_failures"] == receipt["known_failures"]
    assert isinstance(packet["commands"], list) and packet["commands"]
    assert all(
        set(row) == {"command", "exit_code", "result"}
        and isinstance(row["exit_code"], int)
        and isinstance(row["result"], str)
        and row["result"]
        for row in packet["commands"]
    )
    command_results = {row["command"]: row["exit_code"] for row in packet["commands"]}
    assert command_results[
        "bash Stage1_Instances/THM-M-0822/check_proof.sh"
    ] == 0
    assert command_results[
        "python3 -B Stage1_Instances/THM-M-0822/check_proof.py"
    ] == 0
    assert command_results[
        "PYTHONOPTIMIZE=1 python3 -B Stage1_Instances/THM-M-0822/check_proof.py"
    ] == 1

    status = subprocess.check_output(
        ["git", "status", "--short", "--untracked-files=all"],
        cwd=ROOT,
        text=True,
    )
    actual_changes = {
        line[3:] for line in status.splitlines()
        if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual_changes == CHANGED_PATHS, (actual_changes, CHANGED_PATHS)
    for relative in CHANGED_PATHS:
        data = (ROOT / relative).read_bytes()
        assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())

    print(
        "PASS THM-M-0822 proof phase: exact maximum target closes through "
        "all eleven frozen required-machine obligations"
    )
    print("provisional exact route; M0 class pending; accepted root remains H1/M3/R4")
    print("theorem_complete=false")


if __name__ == "__main__":
    main()
