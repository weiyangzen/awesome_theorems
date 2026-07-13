#!/usr/bin/env python3
"""Fail-closed narrow validation for S56-M-0028-VALIDATION."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import platform
import re
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0028"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM = "S56-M-0028-VALIDATION"
THEOREM = "THM-M-0028"
BASE_REVISION = "a16267e7165144d202080fb647261658fa75ceb2"
BASE_TREE = "6edd90c440309a0c5ba277ef62d1733b4b9c05b1"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MATHLIB_REMOTE = "https://github.com/leanprover-community/mathlib4.git"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
EXPRESSION_SHA256 = "89e7e911ed4a5b75c153d824133091ad74ba20a0ecab19bd609b23a54badbee4"
DENOMINATOR_SHA256 = "65d02abdd95b23837143f3a9562ea2ae68a7f0e32f917af40827e25b2aec121b"
EXPECTED_INPUTS = {
    "Statement.lean": "db7cbc8250aa905f1d8a2686ab14e9b31eeeba3409179d22e7169627df02f3a7",
    "AnchorAudit.lean": "1a68b8b7e1de95ccfb8f2f5d13d27affd2a200201810688accaf5c0b8aefb09b",
    "anchor-audit.json": "95e508114c44265025b96ce20283388dfd8dfaab0e1c03f0d10e04b9c563310e",
    "ObligationTree.lean": "7c58c2e8b7c63608abfa1f3baeb161b8f80d9f0a159aca962d756d13389f0980",
    "Proof.lean": "eaeb61f403d1cf97fe53de9d4140cb6c4bc9acf4cae05a9b715e6e7a27014bff",
    "proof-receipt.json": "bf7a963cf23bfb06d7f77ffc2dea66f981735c7897179302e592810304492c96",
    "obligation-registry.json": "ec5c959612d823cffb5863ec0e82e858d1a214948b3a9fbb3a11489176bb0344",
    "typed-graphs.json": "3502e4422934fa7e76124f969b06694d50fcdfc917062315f0d605c535602ae5",
    "Validation.lean": "8e9e79e197d06fc8a881775a23ae389b1365492542905b6a750874b8aac9c066",
    "validation-spec.json": "11a2675ad10541e60d07ce6850678d859871ab025ba14450210901830880a4e6",
}
EXPECTED_TOOL_INPUTS = {
    "lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
TERMINAL_SOURCE_SHA256 = "a0e5c5a1aceb564f885573d5c51ec124be20abbd19fabc6af8c798b637530f0b"
TERMINAL_SOURCE_BLOB = "66ddf1f73601e7dbeb04e37b95fcc61e34ee3c14"
TERMINAL_BODY_SHA256 = "15ae568432091fd1cc53f8136d5c12d441abf60af630459c4d27e4d3627c8ebc"
TERMINAL_OLEAN_SHA256 = "03c849fcf99da9c39ec571619185ce54906da2f918dec6d0fdd260138de00c6f"
LICENSE_SHA256 = "b40930bbcf80744c86c46a12bc9da056641d722716c378f5659b9e555ef833e1"
PROVISIONAL_CLOSED = {
    "M0028-ROOT",
    "M0028-T-ROOT-COMPOSE",
    "M0028-B-FG-NOETHERIAN",
    "M0028-B-NOETHERIAN-CHAIN",
    "M0028-X-FG-BODY",
    "M0028-X-CHAIN-BODY",
    "M0028-N-RING-REGULAR",
    "M0028-D-NOETHERIAN-CLASS",
    "M0028-N-CHAIN-IFF",
    "M0028-N-NOETHERIAN-WF",
    "M0028-L-FG-COMPACT",
    "M0028-C-LATTICE-WF",
    "M0028-L-WF-CHAIN",
    "M0028-L-PREORDER-CHAIN",
    "M0028-L-PARTIAL-EQUALITY",
}
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/Validation.lean",
    f"Stage1_Instances/{THEOREM}/check_validation.py",
    f"Stage1_Instances/{THEOREM}/validation-phase.md",
    f"Stage1_Instances/{THEOREM}/validation-receipt.json",
    f"Stage1_Instances/{THEOREM}/validation-spec.json",
}


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict), path
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(
    argv: list[str], *, cwd: Path = ROOT, env: dict[str, str] | None = None
) -> str:
    result = subprocess.run(
        argv,
        cwd=cwd,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=180,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"validation failed ({result.returncode}): {argv!r}\n{result.stdout}"
        )
    return result.stdout


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["git", *args], cwd=cwd).strip()


def code_without_comments(source: str) -> str:
    source = re.sub(r"/-.*?-/", "", source, flags=re.DOTALL)
    return re.sub(r"--.*$", "", source, flags=re.MULTILINE)


def assert_axioms(output: str, declaration: str, expected: set[str]) -> None:
    pattern = re.compile(
        rf"'{re.escape(declaration)}' depends on axioms:\s*\[([^]]+)\]",
        re.DOTALL,
    )
    match = pattern.search(output)
    assert match is not None, (declaration, output)
    observed = {part.strip() for part in match.group(1).split(",")}
    assert observed == expected, (declaration, observed)


def main() -> None:
    spec = load(HERE / "validation-spec.json")
    receipt = load(HERE / "validation-receipt.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")
    statement = load(HERE / "statement.json")
    anchor = load(HERE / "anchor-audit.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    proof_receipt = load(HERE / "proof-receipt.json")
    instance = load(HERE / "instance.json")
    local_dag = load(HERE / "task-dag.json")
    execution = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item == {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 1073,
        "phase": "validation",
        "layer": 5,
        "state": "[ ]",
        "depends_on": ["S56-M-0028-PROOF"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Run hermetic kernel, trust, provenance, and independent validation gates.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }
    proof_item = next(
        row for row in execution["items"] if row["id"] == "S56-M-0028-PROOF"
    )
    assert proof_item["state"] == "[_]"
    local_task = next(row for row in local_dag["tasks"] if row["id"] == ITEM)
    assert local_task["state"] == "open"
    assert local_task["depends_on"] == ["S56-M-0028-PROOF"]

    assert spec["schema_version"] == "stage1-validation-recipe/1.0"
    assert spec["item_id"] == ITEM and spec["theorem_id"] == THEOREM
    assert spec["cwd"] == "."
    assert spec["argv"] == [
        "python3", "-B", f"Stage1_Instances/{THEOREM}/check_validation.py"
    ]
    assert spec["env_allowlist"] == {}
    assert spec["timeout_seconds"] == 180
    assert spec["network_policy"] == "denied" and spec["expected_exit"] == 0
    assert "did not provision a kernel network namespace" in spec["network_enforcement"]
    assert set(spec["covered_obligation_ids"]) == PROVISIONAL_CLOSED

    for name, expected in EXPECTED_INPUTS.items():
        assert sha256(HERE / name) == expected, f"stale validation input: {name}"
    for name, expected in EXPECTED_TOOL_INPUTS.items():
        assert sha256(LEAN_ROOT / name) == expected, f"changed tool input: {name}"

    assert statement["canonical_formal_target"]["elaborated_expression_sha256"] == (
        EXPRESSION_SHA256
    )
    assert statement["canonical_formal_target"]["statement_file_sha256"] == (
        EXPECTED_INPUTS["Statement.lean"]
    )
    assert anchor["canonical_target_expression_sha256"] == EXPRESSION_SHA256
    assert anchor["canonical_statement_file_sha256"] == EXPECTED_INPUTS["Statement.lean"]
    assert registry["frozen_against_statement_sha256"] == EXPECTED_INPUTS["Statement.lean"]
    assert registry["frozen_against_anchor_audit_sha256"] == EXPECTED_INPUTS["anchor-audit.json"]
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert proof_receipt["proof_body"]["source_sha256"] == EXPECTED_INPUTS["Proof.lean"]
    assert proof_receipt["inputs"]["obligation_tree_sha256"] == (
        EXPECTED_INPUTS["ObligationTree.lean"]
    )
    assert proof_receipt["inputs"]["obligation_registry_sha256"] == (
        EXPECTED_INPUTS["obligation-registry.json"]
    )
    assert proof_receipt["result"]["root_kernel_closed"] is True
    assert set(proof_receipt["closed_obligation_ids"]) == PROVISIONAL_CLOSED
    assert proof_receipt["accepted_closed_obligation_ids"] == []
    assert proof_receipt["result"]["axioms"] == [
        "propext", "Classical.choice", "Quot.sound"
    ]
    assert instance["lifecycle_mode"] == "planned"
    assert instance["root_vector"] == {"H": "H1", "M": "M3", "R": "R3"}
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == []
    assert instance["audit_complete"] is instance["theorem_complete"] is False

    proof_edges = graphs["graphs"]["proof"]["edges"]
    children: dict[str, list[str]] = {}
    for edge in proof_edges:
        if edge["type"] == "proof_requires":
            children.setdefault(edge["from"], []).append(edge["to"])
    reachable: set[str] = set()
    pending = [registry["root_obligation_id"]]
    while pending:
        obligation = pending.pop()
        if obligation in reachable:
            continue
        reachable.add(obligation)
        pending.extend(children.get(obligation, []))
    assert reachable == {
        "M0028-ROOT",
        "M0028-T-ROOT-COMPOSE",
        "M0028-B-FG-NOETHERIAN",
        "M0028-B-NOETHERIAN-CHAIN",
    }
    assert set(graphs["closure_boundary"]["remaining_root_cut_set"]) == {
        "M0028-B-FG-NOETHERIAN",
        "M0028-B-NOETHERIAN-CHAIN",
        "M0028-S-FOUNDATION",
        "M0028-X-SOURCE",
        "M0028-X-PROVENANCE",
        "M0028-X-TRUST",
        "M0028-X-READABLE",
        "M0028-X-WORKFLOW",
    }

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by|extern)\b|"
        r"^[ \t]*(?:axiom|constant|opaque|unsafe)\b",
        re.MULTILINE,
    )
    for name in (
        "Statement.lean", "AnchorAudit.lean", "ObligationTree.lean", "Proof.lean",
        "Validation.lean",
    ):
        source = code_without_comments((HERE / name).read_text(encoding="utf-8"))
        assert prohibited.search(source) is None, f"prohibited source token in {name}"
    independent = (HERE / "Validation.lean").read_text(encoding="utf-8")
    for forbidden in (
        "import Proof", "import ObligationTree", "Proof.finiteGenerationToNoetherian",
        "root_of_bridges", "idealAscendingChainTheorem_via_frozen_composition",
    ):
        assert forbidden not in independent, forbidden
    assert "(isNoetherianRing_iff_ideal_fg R).mpr hfg" in independent
    assert "monotone_stabilizes_iff_noetherian.mpr hNoetherian f" in independent

    manifest = load(LEAN_ROOT / "lake-manifest.json")
    mathlib_entry = next(row for row in manifest["packages"] if row["name"] == "mathlib")
    assert mathlib_entry["rev"] == MATHLIB_REVISION
    assert MATHLIB.resolve().is_dir(), "pinned mathlib artifact is unavailable"
    assert git("rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert git("remote", "get-url", "origin", cwd=MATHLIB) == MATHLIB_REMOTE
    assert git("status", "--porcelain=v1", cwd=MATHLIB) == ""

    terminal_source = MATHLIB / "Mathlib/RingTheory/Noetherian/Defs.lean"
    terminal_olean = (
        MATHLIB / ".lake/build/lib/lean/Mathlib/RingTheory/Noetherian/Defs.olean"
    )
    assert sha256(terminal_source) == TERMINAL_SOURCE_SHA256
    assert git("rev-parse", "HEAD:Mathlib/RingTheory/Noetherian/Defs.lean", cwd=MATHLIB) == (
        TERMINAL_SOURCE_BLOB
    )
    lines = terminal_source.read_bytes().splitlines(keepends=True)
    assert hashlib.sha256(b"".join(lines[158:162] + lines[192:204])).hexdigest() == (
        TERMINAL_BODY_SHA256
    )
    assert sha256(terminal_olean) == TERMINAL_OLEAN_SHA256
    assert sha256(MATHLIB / "LICENSE") == LICENSE_SHA256
    source_text = terminal_source.read_text(encoding="utf-8")
    chain = source_text.split("theorem monotone_stabilizes_iff_noetherian", 1)[1].split(
        "variable [IsNoetherian R M]", 1
    )[0]
    finite = source_text.split("theorem isNoetherianRing_iff_ideal_fg", 1)[1].split(
        "lemma Ideal.fg_of_isNoetherianRing", 1
    )[0]
    assert prohibited.search(code_without_comments(chain + finite)) is None

    lean = run(["lake", "env", "which", "lean"], cwd=LEAN_ROOT).strip()
    lake = run(["lake", "env", "which", "lake"], cwd=LEAN_ROOT).strip()
    lean_version = run(["lake", "env", "lean", "--version"], cwd=LEAN_ROOT)
    assert "4.29.0" in lean_version and LEAN_COMMIT in lean_version
    lean_path = run(["lake", "env", "printenv", "LEAN_PATH"], cwd=LEAN_ROOT).strip()
    base_env = os.environ.copy()
    base_env.update({"LANG": "C.UTF-8", "LC_ALL": "C.UTF-8", "TZ": "UTC"})
    with tempfile.TemporaryDirectory(prefix="m0028-validation-") as tmp_name:
        tmp = Path(tmp_name)
        for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
            (tmp / name).write_bytes((HERE / name).read_bytes())
        statement_env = base_env.copy()
        statement_env["LEAN_PATH"] = lean_path
        run([lean, "-o", "Statement.olean", "Statement.lean"], cwd=tmp, env=statement_env)
        module_env = base_env.copy()
        module_env["LEAN_PATH"] = f"{tmp}:{lean_path}"
        obligation_output = run(
            [lean, "-o", "ObligationTree.olean", "ObligationTree.lean"],
            cwd=tmp,
            env=module_env,
        )
        proof_output = run([lean, "Proof.lean"], cwd=tmp, env=module_env)
        validation_output = run([lean, "Validation.lean"], cwd=tmp, env=module_env)

    small_axioms = {"propext", "Quot.sound"}
    full_axioms = {"propext", "Classical.choice", "Quot.sound"}
    expected_proof_axioms = {
        "isNoetherianRing_iff_ideal_fg": small_axioms,
        "monotone_stabilizes_iff_noetherian": full_axioms,
        "Stage1Instances.THM_M_0028.Proof.finiteGenerationToNoetherian": small_axioms,
        "Stage1Instances.THM_M_0028.Proof.noetherianToChainStabilization": full_axioms,
        "Stage1Instances.THM_M_0028.Proof.idealAscendingChainTheorem_direct": full_axioms,
        "Stage1Instances.THM_M_0028.Proof.idealAscendingChainTheorem_via_frozen_composition": full_axioms,
    }
    for declaration, expected in expected_proof_axioms.items():
        assert_axioms(proof_output, declaration, expected)
    assert_axioms(validation_output, "isNoetherianRing_iff_ideal_fg", small_axioms)
    assert_axioms(validation_output, "monotone_stabilizes_iff_noetherian", full_axioms)
    assert_axioms(
        validation_output,
        "Stage1Instances.THM_M_0028.Validation.differentialIdealAscendingChainTheorem",
        full_axioms,
    )
    assert proof_output.count("Declarations are sorry-free!") == 6
    assert validation_output.count("Declarations are sorry-free!") == 3
    assert "sorryAx" not in obligation_output + proof_output + validation_output

    closure = graphs["closure_boundary"]
    assert closure["accepted_closed_obligations"] == []
    assert closure["root_closed"] is False
    assert closure["audit_complete"] is closure["theorem_complete"] is False

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == packet["item_id"] == ITEM
    assert receipt["theorem_id"] == THEOREM
    assert receipt["base_revision"] == packet["base_revision"] == BASE_REVISION
    assert receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["release_grade"] is False and receipt["accepted"] is False
    for name, expected in EXPECTED_INPUTS.items():
        assert receipt["inputs"][name] == expected
    assert receipt["inputs"]["check_validation.py"] == sha256(HERE / "check_validation.py")
    assert receipt["target"] == {
        "canonical_declaration": "Stage1Instances.THM_M_0028.IdealAscendingChainTarget",
        "elaborated_expression_sha256": EXPRESSION_SHA256,
        "registry_denominator_sha256": DENOMINATOR_SHA256,
    }
    assert receipt["environment"]["lean_executable_sha256"] == sha256(Path(lean))
    assert receipt["environment"]["lake_executable_sha256"] == sha256(Path(lake))
    assert receipt["environment"]["platform"] == f"{platform.system()} {platform.machine()}"
    assert receipt["environment"]["mathlib_revision"] == MATHLIB_REVISION
    assert receipt["environment"]["mathlib_tree"] == MATHLIB_TREE
    assert receipt["provenance"]["terminal_source_sha256"] == TERMINAL_SOURCE_SHA256
    assert receipt["provenance"]["terminal_source_blob"] == TERMINAL_SOURCE_BLOB
    assert receipt["provenance"]["terminal_body_sha256"] == TERMINAL_BODY_SHA256
    assert receipt["provenance"]["terminal_olean_sha256"] == TERMINAL_OLEAN_SHA256
    assert receipt["provenance"]["license_sha256"] == LICENSE_SHA256
    for key in (
        "recipe_id", "cwd", "argv", "env_allowlist", "timeout_seconds",
        "network_policy", "network_enforcement", "expected_exit", "covered_obligation_ids",
        "covered_declarations", "expected_outputs", "scope_boundary",
    ):
        assert receipt["recipe"][key] == spec[key]
    assert receipt["result"]["output_summary_sha256"] == (
        "3a0207eb4daa87289f7422c363995f39685eddfd6df009a43625e1c86401e419"
    )
    assert receipt["result"]["exact_root_kernel_closed"] is True
    assert receipt["result"]["observed_axioms"] == [
        "propext", "Classical.choice", "Quot.sound"
    ]
    assert receipt["result"]["accepted_root_machine_debt"] == "M3"
    assert receipt["result"]["accepted_closed_obligations"] == []
    assert receipt["result"]["hermetic_release_gate"] == "fail_closed"
    assert receipt["result"]["independent_distinct_runner_gate"] == "fail_closed"
    assert receipt["result"]["audit_complete"] is receipt["result"]["theorem_complete"] is False
    assert receipt["first_failed_gate"] == "dependency.S56-M-0028-PROOF.master_acceptance"
    assert receipt["first_failed_release_gate"] == "S56-10.6-HERMETIC-COLD-BUILD"

    assert set(packet) == {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert packet["state"] == "[_]"
    assert set(packet["changed_paths"]) == set(receipt["changed_paths"]) == CHANGED_PATHS
    assert packet["known_failures"] == receipt["known_failures"]
    status = run(["git", "status", "--short", "--untracked-files=all"])
    actual_changed = {
        line[3:] for line in status.splitlines()
        if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual_changed == CHANGED_PATHS, (actual_changed, CHANGED_PATHS)

    for relative in CHANGED_PATHS - {".stage1-worker-selftest.json"}:
        data = (ROOT / relative).read_bytes()
        assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())

    print("PASS THM-M-0028 narrow validation")
    print("PASS kernel replay: both terminals, frozen composition, proof roots, and differential exact root elaborated")
    print("PASS trust observation: finite-generation uses propext/Quot.sound; chain and roots additionally use Classical.choice")
    print("PASS local provenance: frozen hashes, terminal source/body/olean, clean mathlib pin, remote, and license agree")
    print("PASS hygiene: Lean assert_no_sorry plus a supplemental prohibited-construct scan passed")
    print("FAIL CLOSED authority: proof/master reconciliation is pending; accepted root remains H1/M3/R3")
    print("FAIL CLOSED hermetic release: shared warm .lake is not an empty-cache offline replay or complete TCB/SBOM archive")
    print("FAIL CLOSED independent release: differential probe used this worker/shared cache, not a distinct signed runner")
    print("audit_complete=false; theorem_complete=false")


if __name__ == "__main__":
    main()
