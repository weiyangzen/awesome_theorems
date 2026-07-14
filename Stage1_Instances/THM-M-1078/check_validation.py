#!/usr/bin/env python3
"""Fail-closed narrow validation for S56-M-1078-VALIDATION."""

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
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-1078"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM = "S56-M-1078-VALIDATION"
THEOREM = "THM-M-1078"
BASE_REVISION = "15d20dda8662e4144f32be899edc174f7a431574"
BASE_TREE = "b39eec687e4f172c4ce04e08a255e593a428cf95"
EXPRESSION_SHA256 = "675f66dd17fc5f438fc69d579af60f3784063f985924f2c2b059945a7f038aa8"
DENOMINATOR_SHA256 = "f7a3b25e4d46cf0e67ad09199b7b4035216a1bc5acc4b2c6f7c21fd07e63c73e"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MATHLIB_REMOTE = "https://github.com/leanprover-community/mathlib4.git"
MATHLIB_LICENSE_SHA256 = "b40930bbcf80744c86c46a12bc9da056641d722716c378f5659b9e555ef833e1"
LEAN_TOOLCHAIN = "leanprover/lean4:v4.29.0"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
REMAINING_ROOT_CUT = [
    "M1078-C-EXTERNAL-PIN",
    "M1078-T-ALLTIME",
    "M1078-B-PREDICTABLE",
    "M1078-B-NORM",
]
EXPECTED_INPUTS = {
    "Statement.lean": "a5412e5aa97c474cf21e6bf35b2daa1dbef36176bea025976456042700915a0e",
    "AnchorAudit.lean": "324c7724f1e7e2a87201d934a83f5c7c36671c32343078e6c99b71cc43bd4caa",
    "ObligationTree.lean": "128d1eb0ff0387be4ffdd2c384a916eba14ab2855b414d610f71c6949b1d89fc",
    "Proof.lean": "295b0e67b118672c0b9281d495b88884b95966cbac4ea7a0f4fb814f2d410479",
    "anchor-audit.json": "f01c41549004c76f2f59d13f8348bf66e4e7ac9a019767a8f73d1a98bda6747b",
    "obligation-registry.json": "2fec28e7bf3090e35ec0ab350e723a2eba7faacdd62db57d8536d7c7753263cd",
    "typed-graphs.json": "cf7e8839f6ef5c34f0f6ec7345fd823c29dad2d37b2ff48d4d64aedbb4ef55c1",
    "proof-receipt.json": "927cb2fac7c0cc0b40e632ca1cedd448c446d561d662538d6fb418bc9ad87f6d",
    "proof-validation.md": "3be0af86ea143acd36f6374e5419cce0f21e9481b078e041170124a09cb0f965",
    "proof-blocker.md": "23a7211e2c33b220ee109cacdc52875a56778326c206026199882aba22e24d6e",
    "source-statement-crosswalk.md": "e18e3c70a21af16c6e6a31f9ed8dba59f5c22af4bafcaa142da4d6b09e786633",
    "check_exact_composition.sh": "24aaa7ddc3b30e6db201f3c93bd72d9fb1edbfc6ce878d3007fef980bc849edf",
    "check_obligation_tree.py": "551cdf55b9afee61964a45af9d60e169031880cfefa9755497693d05582f3c8a",
    "check_proof.py": "fe7949e632b795236270cb5ede54c5ef836068630a3492174a0dc97623af8cd2",
}
TOOL_INPUTS = {
    "lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
MATHLIB_SOURCES = {
    "Mathlib/MeasureTheory/Function/ConditionalExpectation/CondJensen.lean": (
        "53f435cfad4ea1abe76bed25f056cab4eb12b9b0",
        "470bca2817459705c7321a05f4792316a99fa422ade152b00a0667a1b18ef305",
        "3ae065396838a2ea8dae753c8a8ed6b4d736483060977742430b43452143be4c",
    ),
    "Mathlib/Probability/Martingale/Basic.lean": (
        "3e4890d4efa15706e76364eb9ce6e4e90f934e9e",
        "15331870d95bc20385c6e93ad09a8eb10d26cad46d7b3a7a73536937f6adbcc0",
        "344372e28370008f10daa1ecd559d4e4c2c265618a6642485c55c25b4a629bec",
    ),
    "Mathlib/MeasureTheory/Function/LpSeminorm/LpNorm.lean": (
        "bc7236b725bc93131df93316e7841911686cef2f",
        "706a35af627c0ab2332765e81df84ab218be350ccc35ccdfd5515f99ad6213bb",
        "d6436f2f5a1faee0b50c4840669f9f0b6af0888e29bf347ac040b78886638bfa",
    ),
}
PROOF_DECLARATIONS = (
    "Stage1Instances.THM_M_1078.Proof.memLp_condExp_of_one_lt",
    "Stage1Instances.THM_M_1078.Proof.earlierMemLpUpTo",
)
SUMMARY_LINES = (
    "PASS THM-M-1078 network-isolated trust-zero replay of the frozen statement, conditional composition, and horizon-local proof unit",
    "PASS hygiene and observed trust: checked declarations are sorry-free and use only propext, Classical.choice, and Quot.sound",
    "PASS selected local provenance: frozen hashes, clean mathlib pin/tree/origin/license, selected sources, and oleans agree",
    "OPEN exact root: the external Burkholder body is absent and the all-future conditional interface cannot consume the proved k <= n bridge",
    "BLOCKED release gates: proof dependency/master acceptance, complete provenance/TCB, cold empty-cache hermetic replay, and distinct-runner verification",
)
RECIPE_ARGV = [
    "/usr/bin/bwrap", "--ro-bind", "/", "/", "--dev", "/dev", "--proc", "/proc",
    "--tmpfs", "/tmp", "--unshare-net", "--die-with-parent", "--clearenv",
    "--setenv", "HOME", "/tmp", "--setenv", "PATH", "/usr/bin:/bin",
    "--setenv", "LANG", "C.UTF-8", "--setenv", "LC_ALL", "C.UTF-8",
    "--setenv", "TZ", "UTC", "--setenv", "LEAN_NUM_THREADS", "1",
    "/usr/bin/python3", "-I", "-B",
    "Stage1_Instances/THM-M-1078/check_validation.py",
]
RECIPE_STARTED = __import__("time").monotonic()
RECIPE_TIMEOUT_SECONDS = 1200.0
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    "Stage1_Instances/THM-M-1078/Validation.lean",
    "Stage1_Instances/THM-M-1078/check_validation.py",
    "Stage1_Instances/THM-M-1078/validation-phase.md",
    "Stage1_Instances/THM-M-1078/validation-receipt.json",
    "Stage1_Instances/THM-M-1078/validation-spec.json",
}


if sys.flags.optimize:
    raise SystemExit("validation failed: Python optimization disables assertions")


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


def run(argv: list[str], *, cwd: Path = ROOT, env: dict[str, str] | None = None) -> str:
    remaining = RECIPE_TIMEOUT_SECONDS - (__import__("time").monotonic() - RECIPE_STARTED)
    if remaining <= 0:
        raise TimeoutError("validation recipe exceeded its wall-clock bound")
    result = subprocess.run(
        argv, cwd=cwd, env=env, text=True, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, timeout=remaining, check=False,
    )
    if result.returncode:
        raise RuntimeError(f"command failed ({result.returncode}): {argv!r}\n{result.stdout}")
    return result.stdout


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["/usr/bin/git", *args], cwd=cwd).strip()


def code_without_comments(source: str) -> str:
    output: list[str] = []
    depth = 0
    index = 0
    while index < len(source):
        if source.startswith("/-", index):
            depth += 1
            index += 2
        elif depth and source.startswith("-/", index):
            depth -= 1
            index += 2
        elif depth:
            index += 1
        elif source.startswith("--", index):
            newline = source.find("\n", index)
            index = len(source) if newline < 0 else newline
        else:
            output.append(source[index])
            index += 1
    assert depth == 0, "unterminated Lean block comment"
    return "".join(output)


def reported_axioms(output: str, declaration: str) -> set[str]:
    pattern = re.compile(re.escape(f"'{declaration}' depends on axioms: [") + r"(.*?)]", re.DOTALL)
    matches = pattern.findall(output)
    assert len(matches) == 1, declaration
    return {part.strip() for part in matches[0].split(",") if part.strip()}


def expected_changed_paths() -> set[str]:
    status = run(["/usr/bin/git", "status", "--short", "--untracked-files=all"])
    return {line[3:] for line in status.splitlines() if line[3:] != "Formalizations/Lean/.lake"}


def main() -> None:
    spec = load(HERE / "validation-spec.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    anchor = load(HERE / "anchor-audit.json")
    proof_receipt = load(HERE / "proof-receipt.json")
    targets = load(ROOT / "Docs" / "Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")
    receipt_path = HERE / "validation-receipt.json"
    receipt = load(receipt_path) if receipt_path.exists() else None
    packet_path = ROOT / ".stage1-worker-selftest.json"
    packet = load(packet_path) if packet_path.exists() else None
    verify_outputs = os.environ.get("STAGE1_SKIP_OUTPUT_CHECK") != "1"

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 520 and target["baseline"] == "L0"
    assert target["rework_required"] is True and target["lifecycle_mode"] == "planned"
    assert target["theorem_complete"] is False
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item == {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 520,
        "phase": "validation",
        "layer": 5,
        "state": "[ ]",
        "depends_on": ["S56-M-1078-PROOF"],
        "owned_paths": ["Stage1_Instances/THM-M-1078"],
        "deliverable": "Run hermetic kernel, trust, provenance, and independent validation gates.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }
    predecessor = next(row for row in execution["items"] if row["id"] == "S56-M-1078-PROOF")
    assert predecessor["state"] == "[_]" and predecessor["attempts"] == 1

    for name, expected in EXPECTED_INPUTS.items():
        assert sha256(HERE / name) == expected, f"stale validation input: {name}"
    for name, expected in TOOL_INPUTS.items():
        assert sha256(LEAN_ROOT / name) == expected, f"changed tool input: {name}"

    root_row = next(row for row in registry["obligations"] if row["obligation_id"] == "M1078-ROOT")
    assert root_row["statement_fingerprint"] == f"lean-expression-sha256:{EXPRESSION_SHA256}"
    assert graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert registry["frozen_denominators"]["inventory"] == [
        row["obligation_id"] for row in registry["obligations"]
    ]
    closure = graphs["closure_boundary"]
    assert closure == {
        "closed_obligations": [],
        "root_closed": False,
        "audit_complete": False,
        "theorem_complete": False,
        "remaining_root_cut_set": REMAINING_ROOT_CUT,
        "root_machine_debt": "M2",
    }
    certificate = graphs["composition_certificates"][0]
    assert certificate["status"] == "checked_conditional_composition_only"
    assert certificate["declaration"].endswith("root_of_allTimeMemLpTransformBound")
    assert certificate["exact_target_transport"].endswith("local_target_iff_frozen_target")

    assert proof_receipt["item_id"] == "S56-M-1078-PROOF"
    assert proof_receipt["support_state"] == "provisional_worker_selftest"
    assert proof_receipt["proof_body"]["source_sha256"] == EXPECTED_INPUTS["Proof.lean"]
    assert proof_receipt["closed_obligation_ids"] == ["M1078-T-ALLTIME"]
    assert proof_receipt["result"]["root_closed"] is False
    assert proof_receipt["result"]["theorem_complete"] is False
    assert "forall k, k <= n" in code_without_comments((HERE / "Proof.lean").read_text())
    tree_code = code_without_comments((HERE / "ObligationTree.lean").read_text())
    assert "forall k, MemLp (f k) p mu" in tree_code
    assert "forall k, k <= n" not in tree_code
    assert "MeasureTheory.Lp_Burkholder_inequality_martingaleTransform" not in tree_code
    blocker = (HERE / "proof-blocker.md").read_text()
    assert "unknown module prefix" in blocker and "'Burkholder'" in blocker

    assert anchor["root_machine_classification"] == "M2"
    assert anchor["theorem_proved"] is False and anchor["theorem_complete"] is False
    external = next(row for row in anchor["candidates"] if row["candidate_id"] == "S56-M-1078-C03")
    assert external["revision"] == "afa97ef3c85697fa3b2a67af89af8d6dd09eda69"
    assert external["integration_status"].startswith("not in the local dependency closure")

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by|oracle)\b|"
        r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
        r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
        r"(?:axiom|constant|opaque|unsafe|extern)\b",
        re.MULTILINE,
    )
    for name in ("Statement.lean", "AnchorAudit.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
        assert prohibited.search(code_without_comments((HERE / name).read_text())) is None, name
    validation_code = code_without_comments((HERE / "Validation.lean").read_text())
    assert "import Proof" in validation_code
    assert re.search(r"^(?:theorem|lemma|def)\s", validation_code, re.MULTILINE) is None
    for declaration in PROOF_DECLARATIONS:
        assert f"assert_no_sorry {declaration}" in validation_code

    assert spec["schema_version"] == "stage1-validation-spec/1.0"
    assert spec["item_id"] == ITEM and spec["theorem_id"] == THEOREM
    assert spec["cwd"] == "." and spec["argv"] == RECIPE_ARGV
    assert spec["env_allowlist"] == {
        "HOME": "/tmp", "PATH": "/usr/bin:/bin", "LANG": "C.UTF-8",
        "LC_ALL": "C.UTF-8", "TZ": "UTC", "LEAN_NUM_THREADS": "1",
    }
    assert spec["timeout_seconds"] == 1200 and spec["network_policy"] == "denied"
    assert spec["expected_exit"] == 0
    assert set(REMAINING_ROOT_CUT) <= set(spec["covered_obligation_ids"])
    assert len(spec["covered_declarations"]) == len(set(spec["covered_declarations"]))

    manifest = load(LEAN_ROOT / "lake-manifest.json")
    mathlib_entry = next(row for row in manifest["packages"] if row["name"] == "mathlib")
    assert mathlib_entry["rev"] == mathlib_entry["inputRev"] == MATHLIB_REVISION
    assert MATHLIB.resolve().is_dir()
    assert git("rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert git("remote", "get-url", "origin", cwd=MATHLIB) == MATHLIB_REMOTE
    assert git("status", "--porcelain=v1", "--untracked-files=all", cwd=MATHLIB) == ""
    assert sha256(MATHLIB / "LICENSE") == MATHLIB_LICENSE_SHA256
    for relative, (blob, source_digest, olean_digest) in MATHLIB_SOURCES.items():
        source = MATHLIB / relative
        olean = MATHLIB / ".lake" / "build" / "lib" / "lean" / relative.replace(".lean", ".olean")
        assert git("rev-parse", f"HEAD:{relative}", cwd=MATHLIB) == blob
        assert sha256(source) == source_digest and sha256(olean) == olean_digest

    account_home = Path(pwd.getpwuid(os.getuid()).pw_dir)
    toolchain_bin = account_home / ".elan" / "toolchains" / "leanprover--lean4---v4.29.0" / "bin"
    lean = toolchain_bin / "lean"
    lake = toolchain_bin / "lake"
    assert sha256(lean) == "3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf"
    assert sha256(lake) == "a608ff084d7e2af228b92a29d7c2fd083ba0580e46889175ec74a81678c98359"
    assert sha256(Path("/usr/bin/python3")) == "b8d8288faefdd300201f43fcf00f6f539a27218eeed3a3dff5ab10b9c4c99700"
    assert sha256(Path("/usr/bin/git")) == "5516c9f362c29376ab9a499a33082f9f611941d8c75930c880e30ad109e39c9a"
    assert sha256(Path("/usr/bin/bwrap")) == "0abea81db798ebf6b4742ac0664802d97521547a353c2a0dbdc21d76cbbfd2c0"
    assert LEAN_COMMIT in run([str(lean), "--version"], cwd=LEAN_ROOT)
    assert "5.0.0-src+98dc76e" in run([str(lake), "--version"], cwd=LEAN_ROOT)
    fixed_env = {
        "HOME": os.environ["HOME"],
        "PATH": f"{toolchain_bin}:/usr/bin:/bin",
        "ELAN_TOOLCHAIN": LEAN_TOOLCHAIN,
        "LANG": "C.UTF-8",
        "LC_ALL": "C.UTF-8",
        "TZ": "UTC",
        "LEAN_NUM_THREADS": "1",
    }
    lean_path = run([str(lake), "env", "printenv", "LEAN_PATH"], cwd=LEAN_ROOT, env=fixed_env).strip()

    tmp = Path(tempfile.mkdtemp(prefix="stage1-m1078-validation-", dir="/tmp"))
    try:
        for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
            shutil.copy2(HERE / name, tmp / name)
        (tmp / "home").mkdir()

        def isolated_lean(args: list[str], *, module_path: bool = False) -> str:
            env = dict(fixed_env)
            env["HOME"] = str(tmp / "home")
            env["LEAN_PATH"] = f"{tmp}:{lean_path}" if module_path else lean_path
            return run([str(lean), "--trust=0", "-j1", "-t0", *args], cwd=tmp, env=env)

        combined = tmp / "CombinedComposition.lean"
        statement_text = (HERE / "Statement.lean").read_text()
        statement_prefix = statement_text.split("set_option pp.explicit true in", 1)[0]
        tree_text = (HERE / "ObligationTree.lean").read_text().splitlines()
        composition_body = "\n".join(tree_text[2:]) + "\n"
        combined.write_text(statement_prefix + composition_body + """
namespace Stage1Instances.THM_M_1078.ObligationTree

theorem local_target_iff_frozen_target :
    MartingaleTransformTarget.{u} <-> Stage1Instances.THM_M_1078.MartingaleTransformTarget.{u} := by
  change Stage1Instances.THM_M_1078.ExpandedSourceShape.{u} <->
    Stage1Instances.THM_M_1078.ExpandedSourceShape.{u}
  rfl

#print axioms local_target_iff_frozen_target

end Stage1Instances.THM_M_1078.ObligationTree
""", encoding="utf-8")
        composition_output = isolated_lean(["CombinedComposition.lean"])
        proof_output = isolated_lean(["-o", "Proof.olean", "Proof.lean"])
        validation_output = isolated_lean(["Validation.lean"], module_path=True)
    finally:
        shutil.rmtree(tmp)

    composer = "Stage1Instances.THM_M_1078.ObligationTree.root_of_allTimeMemLpTransformBound"
    assert reported_axioms(composition_output, composer) == EXPECTED_AXIOMS
    transport = "Stage1Instances.THM_M_1078.ObligationTree.local_target_iff_frozen_target"
    assert reported_axioms(composition_output, transport) <= EXPECTED_AXIOMS
    for declaration in PROOF_DECLARATIONS:
        assert reported_axioms(proof_output, declaration) == EXPECTED_AXIOMS
        assert reported_axioms(validation_output, declaration) == EXPECTED_AXIOMS
    assert validation_output.count("Declarations are sorry-free!") == 2
    all_output = proof_output + validation_output + composition_output
    assert "declaration uses 'sorry'" not in all_output and "sorryAx" not in all_output
    assert "error:" not in all_output

    if verify_outputs:
        assert receipt is not None and packet is not None
        assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
        assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
        assert receipt["support_state"] == "provisional_worker_selftest"
        assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
        assert receipt["release_grade"] is False and receipt["verdict"] == "blocked"
        assert receipt["inputs"]["validation_spec_sha256"] == sha256(HERE / "validation-spec.json")
        assert receipt["inputs"]["validator_sha256"] == sha256(Path(__file__).resolve())
        assert receipt["inputs"]["validation_probe_sha256"] == sha256(HERE / "Validation.lean")
        for key, name in (
            ("statement_source_sha256", "Statement.lean"),
            ("obligation_tree_source_sha256", "ObligationTree.lean"),
            ("proof_source_sha256", "Proof.lean"),
            ("anchor_audit_sha256", "anchor-audit.json"),
            ("obligation_registry_sha256", "obligation-registry.json"),
            ("typed_graphs_sha256", "typed-graphs.json"),
            ("proof_receipt_sha256", "proof-receipt.json"),
            ("proof_validation_sha256", "proof-validation.md"),
            ("proof_blocker_sha256", "proof-blocker.md"),
            ("source_crosswalk_sha256", "source-statement-crosswalk.md"),
        ):
            assert receipt["inputs"][key] == sha256(HERE / name), key
        assert receipt["recipe"] == spec
        assert receipt["result"]["validated_partial_obligation_ids"] == ["M1078-T-ALLTIME"]
        assert receipt["result"]["supported_obligation_ids"] == []
        assert receipt["result"]["accepted_closed_obligation_ids"] == []
        assert receipt["result"]["root_closed"] is False
        assert receipt["result"]["theorem_complete"] is False
        assert receipt["remaining_root_cut_set"] == REMAINING_ROOT_CUT
        assert receipt["known_failures"] == packet["known_failures"]
        assert packet["item_id"] == ITEM and packet["state"] == "[_]"
        assert set(packet["changed_paths"]) == CHANGED_PATHS
        assert set(receipt["changed_paths"]) == CHANGED_PATHS
        assert expected_changed_paths() == CHANGED_PATHS

    print("\n".join(SUMMARY_LINES))


if __name__ == "__main__":
    main()
