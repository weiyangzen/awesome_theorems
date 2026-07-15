#!/usr/bin/env python3
"""Fail-closed proof-phase replay for S56-M-0072-PROOF."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile


if not __debug__:
    raise SystemExit("check_proof.py must run without Python optimization")


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM_ID = "S56-M-0072-PROOF"
THEOREM_ID = "THM-M-0072"
BASE_REVISION = "7a05a580f6eb39b1dcd87bbd8f3d9f4c0ecd4cb4"
BASE_TREE = "681b326462f0271a612a5178ae0846f857b96648"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
CANONICAL_TARGET = "Stage1Instances.THM_M_0072.ThompsonTransferLemmaTarget"
CANONICAL_EXPRESSION_SHA256 = (
    "c8a89538bd8b492ba31ce5d516a0f8fefef70a550e1d2fe74e39a4cba7849051"
)
REGISTRY_DENOMINATOR_SHA256 = (
    "7f5030b02a13572f021c17ac32f2472098e2a5de881bc5a4999716dd411f717b"
)
EXPECTED_INPUT_HASHES = {
    "Statement.lean": "0e9a35c7d2a9eaafb2aa6f8357277e9bf1e79e9a5e88500bda6cd8300a6757aa",
    "ObligationTree.lean": "e30e9833e607eea7a9dd025e86cd6f34a912ed375c0563186c0727424dcb838c",
    "statement.json": "ab2ab89125e95ced56ed588c965b03a283596dd6fb815f967bf9bb91114d1034",
    "obligation-registry.json": (
        "6e60eb6599e9fded2c5ce5100b469faedd20eaa83840917c6e979b5af12f2498"
    ),
    "typed-graphs.json": "d307d8c606150999add6b0e068510dcc70c2ddaa8945c944e1ed9f9980e67b8a",
    "validation-specs.json": (
        "b542c4abffa013978e1609051b9477df078d67022af0493f66d5ed5b464c142c"
    ),
    "anchor-audit.json": "9124610a2becf3f4a5ff4972f9280235ad8217d10a79971ccddd5dbdf23bc6fd",
}
EXPECTED_DAG_SHA256 = "44bc97e9479a34075aa949dbea20dd82f955e54e14bfeeba301650d9a4a0ebd6"
OUTSIDE_DECLARATION = (
    "Stage1Instances.THM_M_0072.Proof.outsideTransferConclusion"
)
ROOT_DECLARATION = (
    "Stage1Instances.THM_M_0072.Proof.thompsonTransferLemma_proof"
)
ALLOWED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
EXPECTED_CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM_ID}/Proof.lean",
    f"Stage1_Instances/{THEOREM_ID}/check_proof.py",
    f"Stage1_Instances/{THEOREM_ID}/proof-receipt.json",
    f"Stage1_Instances/{THEOREM_ID}/proof-validation.md",
}
PROVISIONALLY_CLOSED_PROOF_OBLIGATION_IDS = [
    "M0072-ROOT",
    "M0072-N-OUTSIDE",
    "M0072-B-MEMBERSHIP",
    "M0072-T-INSIDE",
    "M0072-C-NORMAL",
    "M0072-L-INDEX-TWO",
    "M0072-C-QUOTIENT",
    "M0072-C-TRANSFER",
    "M0072-L-SYLOW-ODD",
    "M0072-C-COSET-ACTION",
    "M0072-L-FIXED-PARITY",
    "M0072-L-TRANSFER-FORMULA",
    "M0072-L-FACTOR-DICHOTOMY",
    "M0072-L-ODD-PRODUCT",
    "M0072-L-NOINDEX-TRANSFER",
    "M0072-B-CONTRADICTION",
    "M0072-T-OUTSIDE",
    "M0072-T-ASSEMBLE",
]
PROOF_HELPER_DECLARATIONS = [
    "Stage1Instances.THM_M_0072.Proof.maximal_normal_of_pgroup",
    "Stage1Instances.THM_M_0072.Proof.quotient_isSimpleGroup_of_isCoatom",
    "Stage1Instances.THM_M_0072.Proof.maximal_index_prime_of_pgroup",
    "Stage1Instances.THM_M_0072.Proof.maximal_index_two_of_2group",
    "Stage1Instances.THM_M_0072.Proof.period_eq_one_or_two",
    "Stage1Instances.THM_M_0072.Proof.quotient_eq_of_both_not_mem",
]
PROVISIONAL_OBLIGATION_BODY_MAP = {
    "M0072-ROOT": "thompsonTransferLemma_proof",
    "M0072-N-OUTSIDE": "outsideTransferConclusion",
    "M0072-B-MEMBERSHIP": "ObligationTree.root_of_outsideTransfer",
    "M0072-T-INSIDE": "ObligationTree.insideMaximalConclusion",
    "M0072-C-NORMAL": "maximal_normal_of_pgroup",
    "M0072-L-INDEX-TWO": "maximal_index_two_of_2group",
    "M0072-C-QUOTIENT": "outsideTransferConclusion: quotientMap/x/hQcard/hx1",
    "M0072-C-TRANSFER": "outsideTransferConclusion: transferMap",
    "M0072-L-SYLOW-ODD": "outsideTransferConclusion: hindexOdd",
    "M0072-C-COSET-ACTION": "period_eq_one_or_two and outsideTransferConclusion: Orbits",
    "M0072-L-FIXED-PARITY": "outsideTransferConclusion: period split plus hindexOdd",
    "M0072-L-TRANSFER-FORMULA": "outsideTransferConclusion: htransferValue",
    "M0072-L-FACTOR-DICHOTOMY": "outsideTransferConclusion: hfactor",
    "M0072-L-ODD-PRODUCT": "outsideTransferConclusion: hpow",
    "M0072-L-NOINDEX-TRANSFER": "outsideTransferConclusion: htransferTrivial",
    "M0072-B-CONTRADICTION": "outsideTransferConclusion: hconclusion/htransferOne/hx1",
    "M0072-T-OUTSIDE": "outsideTransferConclusion",
    "M0072-T-ASSEMBLE": "ObligationTree.root_of_outsideTransfer",
}


def need(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_json(path: Path) -> dict:
    def reject_duplicates(pairs: list[tuple[str, object]]) -> dict:
        value: dict[str, object] = {}
        for key, item in pairs:
            need(key not in value, f"duplicate JSON key in {path}: {key}")
            value[key] = item
        return value

    try:
        value = json.loads(
            path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicates
        )
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise SystemExit(f"cannot load {path}: {error}") from error
    need(isinstance(value, dict), f"{path} must contain a JSON object")
    return value


def command(*argv: str, cwd: Path = ROOT, timeout: int = 60) -> str:
    try:
        return subprocess.check_output(
            argv, cwd=cwd, text=True, stderr=subprocess.STDOUT, timeout=timeout
        ).strip()
    except subprocess.CalledProcessError as error:
        sys.stdout.write(error.output)
        raise SystemExit(error.returncode) from error


def strip_comments_and_strings(source: str) -> str:
    """Erase nested comments and quoted strings before the lexical defense scan."""
    output: list[str] = []
    index = 0
    block_depth = 0
    in_string = False
    while index < len(source):
        pair = source[index : index + 2]
        char = source[index]
        if block_depth:
            if pair == "/-":
                block_depth += 1
                output.extend("  ")
                index += 2
            elif pair == "-/":
                block_depth -= 1
                output.extend("  ")
                index += 2
            else:
                output.append("\n" if char == "\n" else " ")
                index += 1
        elif in_string:
            if char == "\\" and index + 1 < len(source):
                output.extend("  ")
                index += 2
            elif char == '"':
                in_string = False
                output.append(" ")
                index += 1
            else:
                output.append("\n" if char == "\n" else " ")
                index += 1
        elif pair == "/-":
            block_depth = 1
            output.extend("  ")
            index += 2
        elif pair == "--":
            while index < len(source) and source[index] != "\n":
                output.append(" ")
                index += 1
        elif char == '"':
            in_string = True
            output.append(" ")
            index += 1
        else:
            output.append(char)
            index += 1
    need(block_depth == 0 and not in_string, "unterminated comment or string in Lean source")
    return "".join(output)


def run_lean(
    lean: str, source: str, output: str, *, cwd: Path, lean_path: str
) -> str:
    environment = os.environ.copy()
    environment.update(
        {
            "LC_ALL": "C.UTF-8",
            "TZ": "Asia/Shanghai",
            "LEAN_NUM_THREADS": "1",
            "LEAN_PATH": lean_path,
        }
    )
    result = subprocess.run(
        [lean, "--trust=0", "-t0", "-o", output, source],
        cwd=cwd,
        env=environment,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=600,
        check=False,
    )
    if result.returncode:
        sys.stdout.write(result.stdout)
        raise SystemExit(result.returncode)
    return result.stdout


def parse_axioms(output: str, declaration: str) -> list[str]:
    match = re.search(
        rf"'{re.escape(declaration)}' depends on axioms:\s*\[([^]]*)\]",
        output,
        re.DOTALL,
    )
    if match is not None:
        return [part.strip() for part in match.group(1).split(",") if part.strip()]
    need(
        f"'{declaration}' does not depend on any axioms" in output,
        f"missing #print axioms report for {declaration}",
    )
    return []


def fresh_lean_replay() -> tuple[str, dict[str, list[str]]]:
    lean = command("lake", "env", "which", "lean", cwd=LEAN_ROOT)
    base_lean_path = command("lake", "env", "printenv", "LEAN_PATH", cwd=LEAN_ROOT)
    with tempfile.TemporaryDirectory(prefix="thm-m-0072-proof-") as temporary:
        temp = Path(temporary)
        for filename in ("Statement.lean", "ObligationTree.lean", "Proof.lean"):
            shutil.copyfile(HERE / filename, temp / filename)
        statement_output = run_lean(
            lean,
            "Statement.lean",
            "Statement.olean",
            cwd=temp,
            lean_path=base_lean_path,
        )
        local_lean_path = f"{temp}{os.pathsep}{base_lean_path}"
        tree_output = run_lean(
            lean,
            "ObligationTree.lean",
            "ObligationTree.olean",
            cwd=temp,
            lean_path=local_lean_path,
        )
        proof_output = run_lean(
            lean,
            "Proof.lean",
            "Proof.olean",
            cwd=temp,
            lean_path=local_lean_path,
        )
        probe = temp / "ProofProbe.lean"
        probe.write_text(
            """import Proof
import Mathlib.Util.AssertNoSorry
import Mathlib.Util.PrintSorries

namespace Stage1Instances.THM_M_0072.ProofAudit

universe u

theorem exactOutsideReplay :
    Stage1Instances.THM_M_0072.ObligationTree.TransferOutsideTarget.{u} :=
  Stage1Instances.THM_M_0072.Proof.outsideTransferConclusion

theorem exactRootReplay :
    Stage1Instances.THM_M_0072.ThompsonTransferLemmaTarget.{u} :=
  Stage1Instances.THM_M_0072.Proof.thompsonTransferLemma_proof

assert_no_sorry Stage1Instances.THM_M_0072.Proof.outsideTransferConclusion
assert_no_sorry Stage1Instances.THM_M_0072.Proof.thompsonTransferLemma_proof
#print sorries Stage1Instances.THM_M_0072.Proof.outsideTransferConclusion
#print sorries Stage1Instances.THM_M_0072.Proof.thompsonTransferLemma_proof
#print axioms Stage1Instances.THM_M_0072.Proof.outsideTransferConclusion
#print axioms Stage1Instances.THM_M_0072.Proof.thompsonTransferLemma_proof

end Stage1Instances.THM_M_0072.ProofAudit
""",
            encoding="utf-8",
        )
        probe_output = run_lean(
            lean,
            "ProofProbe.lean",
            "ProofProbe.olean",
            cwd=temp,
            lean_path=local_lean_path,
        )

    combined = statement_output + tree_output + proof_output + probe_output
    need("error:" not in combined.lower(), "Lean replay output contains an error")
    need(
        probe_output.count("Declarations are sorry-free!") == 2,
        "terminal #print sorries reports were not both clean",
    )
    axioms = {
        declaration: parse_axioms(probe_output, declaration)
        for declaration in (OUTSIDE_DECLARATION, ROOT_DECLARATION)
    }
    reported = {axiom for names in axioms.values() for axiom in names}
    need(reported <= ALLOWED_AXIOMS, f"unexpected axiom closure: {sorted(reported)}")
    return combined, axioms


def main() -> None:
    need(command("git", "rev-parse", "HEAD") == BASE_REVISION, "worker HEAD changed")
    need(command("git", "rev-parse", "HEAD^{tree}") == BASE_TREE, "base tree changed")
    need(
        command("git", "rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION,
        "materialized mathlib revision changed",
    )
    need(
        command("git", "rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE,
        "materialized mathlib tree changed",
    )
    need(
        command("git", "status", "--porcelain=v1", cwd=MATHLIB) == "",
        "materialized mathlib worktree is dirty",
    )
    need(
        "check_stage1_standard: ok" in command(
            "python3", "Docs/tools/check_stage1_standard.py", timeout=180
        ),
        "rev-5.6 standard preflight failed",
    )
    need(
        "stage1_target: ok" in command(
            "python3", "scripts/stage1_target.py", "check", timeout=180
        ),
        "ordered target manifest preflight failed",
    )
    for filename, expected in EXPECTED_INPUT_HASHES.items():
        need(sha256(HERE / filename) == expected, f"frozen input changed: {filename}")
    execution_path = ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json"
    need(sha256(execution_path) == EXPECTED_DAG_SHA256, "authoritative DAG changed")

    execution = load_json(execution_path)
    item = next((row for row in execution["items"] if row["id"] == ITEM_ID), None)
    need(item is not None, "authoritative proof item missing")
    need(item["theorem_id"] == THEOREM_ID, "authoritative theorem identity changed")
    need(item["execution_rank"] == 1102, "execution rank changed")
    need(item["phase"] == "proof" and item["layer"] == 4, "phase or layer changed")
    need(item["state"] in {"[ ]", "[_]"}, "proof item is in an unexpected state")
    need(
        item["depends_on"] == ["S56-M-0072-OBLIGATION_TREE"],
        "proof dependency changed",
    )
    need(
        item["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"],
        "proof ownership changed",
    )
    predecessor = next(
        row for row in execution["items"] if row["id"] == "S56-M-0072-OBLIGATION_TREE"
    )
    need(predecessor["state"] == "[_]", "predecessor is not worker-self-tested")

    local_dag = load_json(HERE / "task-dag.json")
    local_item = next(row for row in local_dag["tasks"] if row["id"] == ITEM_ID)
    need(local_item["state"] == "open", "local proof projection unexpectedly promoted")
    need(local_dag["accepted_states"] == [], "local DAG claims an accepted state")
    statement = load_json(HERE / "statement.json")
    target = statement["canonical_formal_target"]
    need(target["declaration_or_expression"] == CANONICAL_TARGET, "canonical target changed")
    need(
        target["elaborated_expression_sha256"] == CANONICAL_EXPRESSION_SHA256,
        "canonical expression fingerprint changed",
    )
    registry = load_json(HERE / "obligation-registry.json")
    graphs = load_json(HERE / "typed-graphs.json")
    need(registry["root_obligation_id"] == "M0072-ROOT", "registry root changed")
    need(
        registry["denominator_sha256"] == REGISTRY_DENOMINATOR_SHA256,
        "registry denominator changed",
    )
    need(len(registry["obligations"]) == 28, "registry obligation count changed")
    boundary = graphs["closure_boundary"]
    need(boundary["root_closed"] is False, "frozen graph was rewritten after proof")
    need(
        boundary["accepted_closed_obligations"] == [],
        "frozen graph claims accepted proof closure",
    )
    need(
        boundary["remaining_root_cut_set"] == ["M0072-T-OUTSIDE"],
        "frozen pre-proof cut changed",
    )
    need(boundary["theorem_complete"] is False, "frozen graph claims completion")

    proof_path = HERE / "Proof.lean"
    need(proof_path.is_file(), "Proof.lean is missing")
    proof = strip_comments_and_strings(proof_path.read_text(encoding="utf-8"))
    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|implemented_by|native_decide|run_tac)\b|"
        r"^[ \t]*(?:axiom|constant|opaque|unsafe|extern)\b",
        re.MULTILINE,
    )
    for filename in ("Statement.lean", "ObligationTree.lean", "Proof.lean"):
        lean_source = strip_comments_and_strings(
            (HERE / filename).read_text(encoding="utf-8")
        )
        need(
            prohibited.search(lean_source) is None,
            f"prohibited proof device in {filename}",
        )
    need(
        re.search(r"^import\s+ObligationTree\s*$", proof, re.MULTILINE) is not None,
        "Proof.lean must import the frozen obligation tree",
    )
    need(
        "namespace Stage1Instances.THM_M_0072.Proof" in proof,
        "proof namespace changed",
    )
    need(
        re.search(r"\btheorem\s+outsideTransferConclusion\b", proof) is not None,
        "missing outside-transfer declaration",
    )
    need(
        re.search(r"\btheorem\s+thompsonTransferLemma_proof\b", proof) is not None,
        "missing canonical-root declaration",
    )
    need(
        "root_of_outsideTransfer" in proof,
        "canonical root does not use the frozen branch composition",
    )

    receipt = load_json(HERE / "proof-receipt.json")
    need(receipt["schema_version"] == "stage1-node-receipt/1.0", "receipt schema changed")
    need(receipt["item_id"] == ITEM_ID and receipt["theorem_id"] == THEOREM_ID, "receipt identity changed")
    need(receipt["phase"] == "proof" and receipt["intent"] == "prove", "receipt intent changed")
    need(receipt["base_revision"] == BASE_REVISION, "receipt base revision changed")
    need(receipt["base_tree"] == BASE_TREE, "receipt base tree changed")
    need(receipt["proposed_state"] == "[_]", "receipt state proposal changed")
    need(receipt["accepted"] is False, "worker receipt may not claim acceptance")
    need(receipt["support_state"] == "provisional_worker_selftest", "receipt support state changed")
    need(receipt["canonical_target"] == CANONICAL_TARGET, "receipt target changed")
    need(
        receipt["canonical_target_expression_sha256"] == CANONICAL_EXPRESSION_SHA256,
        "receipt expression fingerprint changed",
    )
    need(
        receipt["registry_denominator_sha256"] == REGISTRY_DENOMINATOR_SHA256,
        "receipt denominator changed",
    )
    need(
        receipt["exact_declarations"] == [OUTSIDE_DECLARATION, ROOT_DECLARATION],
        "receipt declaration set changed",
    )
    need(
        receipt["proof_helper_declarations"] == PROOF_HELPER_DECLARATIONS,
        "receipt helper declaration set changed",
    )
    need(
        receipt["provisionally_closed_proof_obligation_ids"]
        == PROVISIONALLY_CLOSED_PROOF_OBLIGATION_IDS,
        "receipt provisional proof-closure set changed",
    )
    need(
        receipt["provisional_obligation_body_map"] == PROVISIONAL_OBLIGATION_BODY_MAP,
        "receipt provisional proof-body map changed",
    )
    need(
        receipt["accepted_closed_obligation_ids"] == [],
        "receipt may not claim accepted obligation closure",
    )
    inputs = receipt["inputs"]
    need(inputs["proof_sha256"] == sha256(proof_path), "receipt proof hash is stale")
    need(
        inputs["check_proof_sha256"] == sha256(Path(__file__)),
        "receipt checker hash is stale",
    )
    for filename in EXPECTED_INPUT_HASHES:
        key = filename.lower().replace(".", "_").replace("-", "_") + "_sha256"
        need(inputs[key] == sha256(HERE / filename), f"receipt input hash is stale: {filename}")
    need(
        inputs["execution_dag_sha256"] == sha256(execution_path),
        "receipt execution DAG hash is stale",
    )
    result = receipt["result"]
    need(result["exit_code"] == 0, "receipt does not record a successful replay")
    need(result["root_kernel_closed"] is True, "receipt does not record exact root closure")
    need(result["accepted_root_closed"] is False, "receipt overclaims accepted closure")
    need(result["audit_complete"] is False, "receipt overclaims audit completion")
    need(result["theorem_complete"] is False, "receipt overclaims theorem completion")
    need(
        result["machine_debt_proposal"] == "M0-L pending master acceptance",
        "receipt machine-debt proposal changed",
    )
    need(
        set(receipt["changed_paths"]) == EXPECTED_CHANGED_PATHS,
        "receipt changed-path set changed",
    )

    lean_output, axioms = fresh_lean_replay()
    need("sorryAx" not in lean_output, "Lean replay reached sorryAx")
    need(
        receipt["result"]["axioms_by_declaration"] == axioms,
        "receipt axiom reports are stale",
    )
    reported_axioms = sorted({axiom for names in axioms.values() for axiom in names})
    need(
        sorted(receipt["result"]["axioms"]) == reported_axioms,
        "receipt combined axiom set is stale",
    )

    selftest_path = ROOT / ".stage1-worker-selftest.json"
    expected_present = set(EXPECTED_CHANGED_PATHS)
    if selftest_path.exists():
        packet = load_json(selftest_path)
        need(
            set(packet)
            == {
                "item_id",
                "changed_paths",
                "commands",
                "output_summary",
                "base_revision",
                "known_failures",
                "state",
            },
            "worker packet fields changed",
        )
        need(packet["item_id"] == ITEM_ID and packet["state"] == "[_]", "worker packet identity changed")
        need(packet["base_revision"] == BASE_REVISION, "worker packet base changed")
        need(set(packet["changed_paths"]) == EXPECTED_CHANGED_PATHS, "worker packet paths changed")
        need(packet["known_failures"] == receipt["known_failures"], "worker packet failures changed")
    else:
        expected_present.remove(".stage1-worker-selftest.json")

    status = command("git", "status", "--short", "--untracked-files=all")
    actual_changed = {
        line[3:]
        for line in status.splitlines()
        if line[3:] != "Formalizations/Lean/.lake"
    }
    need(actual_changed == expected_present, f"unexpected worker changes: {sorted(actual_changed)}")
    for relative in expected_present:
        data = (ROOT / relative).read_bytes()
        need(data.endswith(b"\n"), f"missing final newline: {relative}")
        need(b"\r" not in data and b"\x00" not in data, f"invalid bytes in {relative}")
        need(
            all(not line.endswith((b" ", b"\t")) for line in data.splitlines()),
            f"trailing whitespace in {relative}",
        )

    print("PASS THM-M-0072 proof phase: exact outside branch and canonical root replayed")
    print("Lean replay: Statement, ObligationTree, Proof, and exact-type probe passed with --trust=0 -t0")
    print(f"terminal axiom closure: {reported_axioms}")
    print("accepted state unchanged; candidate M0-L remains pending master acceptance")


if __name__ == "__main__":
    main()
