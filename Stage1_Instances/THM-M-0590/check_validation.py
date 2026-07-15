#!/usr/bin/env python3
"""Fail-closed narrow validator for S56-M-0590-VALIDATION."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0590"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
ITEM = "S56-M-0590-VALIDATION"
THEOREM = "THM-M-0590"
BASE_REVISION = "e73a459aa33f8b656019c9c36e3d5dfc84dffc30"
BASE_TREE = "81105927f8e46d0076dd20433240ecf0fd185cea"
TOOLCHAIN = "leanprover/lean4:v4.29.0"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
LEAN_SHA256 = "3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf"
LAKE_SHA256 = "a608ff084d7e2af228b92a29d7c2fd083ba0580e46889175ec74a81678c98359"
BWRAP_SHA256 = "0abea81db798ebf6b4742ac0664802d97521547a353c2a0dbdc21d76cbbfd2c0"
TOOLCHAIN_SHA256 = "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2"
MANIFEST_SHA256 = "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MATHLIB_REMOTE = "https://github.com/leanprover-community/mathlib4.git"
MATHLIB_LICENSE_SHA256 = "b40930bbcf80744c86c46a12bc9da056641d722716c378f5659b9e555ef833e1"
STATEMENT_SOURCE_SHA256 = "eae40763685730f42ae296f54c7c41b982efc532836c7db8ce9de31de16b5b67"
DENOMINATOR_SHA256 = "2d5b17d162ed0ef7a445673a25243da41d3aeb4a2be8f39eab68511e1809a9e8"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
ROOT_VECTOR = {"H": "H1", "M": "M4", "R": "R3"}
OPEN_ROOT_CUT = ["M0590-B-FORWARD", "M0590-T-BACKWARD"]
EXPECTED_INPUTS = {
    "Statement.lean": STATEMENT_SOURCE_SHA256,
    "ObligationTree.lean": "cf0aa98535f1ec4a4218378d2950c3d25ca0a6047450bdeb5bbe5c390f38fe96",
    "AnchorAudit.lean": "ff1117ae7af80a96abd661348c4937bdeed6b607008ea88df4b2c691f6537e9f",
    "Proof.lean": "3c3a31613315a3493e2e9786caa41cb33db79aec7df314e08a33ac2ec2912d43",
    "Validation.lean": "3b0e3567b9e271d6fd4d903d7005490cc00626d2e88ca40c8b448672e8d2129b",
    "statement.json": "d20d505e795fbf0c7626d22e508a3cc8ef25f240353ba661f3d9402c1e8b05a0",
    "anchor-audit.json": "6a506ed464abfde062f0d0a8593a1f9eeda50737ab5e6b4feacc6fa31c6470cb",
    "obligation-registry.json": "de449de711d50b330e19da9e251a9a75beb3746a3b45f0ca8cb20298e90d3b0c",
    "typed-graphs.json": "62a92f3bf843dda0dcb90ce7c4016fc4ca91af9611bf69592ae53037ed9371bd",
    "validation-specs.json": "69fd9a9c4aefae5f9efe1e39344085b49cb923e1b13a08e23a63d760a9b8e214",
    "proof-receipt.json": "a3f9fd5d680a560066132385145e71f57720037e6550be9bb1274dacb4e54e84",
    "proof-blocker.json": "7f92f24784ce430766118a182df78a8853e4618c7cee750a5f186e25bc825ac2",
    "check_obligation_tree.py": "c363510152258276fae777bf74ab69a1cbec8cc1648f2046531b0e9b5c2e04b2",
    "check_proof.sh": "05c114a4e38e2d7e447a81cc43715827b8bc0204ea3aa7eb0c4bcf4496c00587",
    "validation-spec.json": "c8aa4dd8771f387c29021ca73874cf91898a88339f158b3c1a6c6bc76ff21a16",
}
SOURCE_PROVENANCE = {
    "Mathlib/Analysis/Normed/Operator/Compact.lean": {
        "blob": "01820209ad9d43873780e46970a0d201846e9afb",
        "source_sha256": "c7ea7893fe1eb516cec45dc6fa9dabd14411a77cf4e1fe94d8eb9e8dcc6091a9",
        "olean_sha256": "5a13a98a04480650977a880d9cced0928600bfc184c8f256a83fce8aa26adc34",
        "olean_bytes": 272496,
    },
    "Mathlib/Analysis/InnerProductSpace/Adjoint.lean": {
        "blob": "0cb9bb1fb2249fe8bf7b57f1a72c591d370dca6a",
        "source_sha256": "08218f9c59623e93818c293000810a2d15a9b543340feaba3b1a58b4749831a6",
        "olean_sha256": "3be11d32be2df343d8845b0eabe6d0dbe553509b68cfd15b31bf75525f97bf29",
        "olean_bytes": 1407200,
    },
}
PROOF_DECLARATIONS = (
    "THMM0590.isEssentiallyNormal_of_adjoint_comp_eq_comp_adjoint",
    "THMM0590.unitaryEquivalentModuloCompacts_refl",
    "THMM0590.isCompactOperator_unitary_conjugate",
    "THMM0590.isEssentiallyNormal_unitary_conjugate",
    "THMM0590.bdfInvariantEquivalence_refl",
)
COMPOSITION_DECLARATION = "THMM0590.root_of_directional_packages"
VALIDATION_DECLARATIONS = (
    "THMM0590.Validation.essentiallyNormalOfNormalDirect",
    "THMM0590.Validation.diagonalInvariantEquivalenceDirect",
    "THMM0590.Validation.conditionalRootDirect",
)
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/Validation.lean",
    f"Stage1_Instances/{THEOREM}/check_validation.py",
    f"Stage1_Instances/{THEOREM}/validation-blocker.json",
    f"Stage1_Instances/{THEOREM}/validation-phase.md",
    f"Stage1_Instances/{THEOREM}/validation-receipt.json",
    f"Stage1_Instances/{THEOREM}/validation-spec.json",
}
SUMMARY_LINES = (
    "PASS network-isolated trust-zero replay: statement, conditional composer, five partial bodies, and three same-worker differential probes elaborated",
    "PASS hygiene: audited sources and declarations are placeholder-free with no bodyless nonaxiom or unsafe declaration in the inspected closure",
    "PASS trust observation: nine proof/composition/probe declarations report exactly propext, Classical.choice, and Quot.sound",
    "PASS selected provenance: frozen inputs, tool identities, clean mathlib pin, license, and two source/blob/olean boundaries agree",
    "OPEN exact BDF root: neither directional package has a terminal proof body and the root remains H1/M4/R3",
    "FAIL CLOSED proof dependency: S56-M-0590-PROOF is worker-provisional, receipt accepted=false, and closes no frozen obligation",
    "FAIL CLOSED complete trust/provenance: accepted foundation policy, serialized transitive body provenance, and full TCB/SBOM are absent",
    "FAIL CLOSED hermetic release: the replay uses the shared warm dependency cache rather than a clean empty-cache cold offline restoration",
    "FAIL CLOSED independent verification: this same-worker probe is not a distinct signed runner or independently implemented minimal verifier",
)
EXPECTED_CLOSURE = {
    "roots": 3,
    "declarations": 18827,
    "modules": 752,
    "bodyless_nonaxioms": 0,
    "unsafe": 0,
}


if not __debug__:
    raise RuntimeError("validation requires Python assertions; optimized mode is forbidden")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path: Path) -> dict:
    def reject_duplicates(pairs: list[tuple[str, object]]) -> dict:
        value: dict[str, object] = {}
        for key, item in pairs:
            assert key not in value, f"duplicate JSON key in {path}: {key}"
            value[key] = item
        return value

    value = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicates)
    assert isinstance(value, dict), path
    return value


BASE_ENV = {
    "HOME": os.environ["HOME"],
    "PATH": f"{os.environ['HOME']}/.elan/bin:/usr/bin:/bin",
    "ELAN_TOOLCHAIN": TOOLCHAIN,
    "LANG": "C.UTF-8",
    "LC_ALL": "C.UTF-8",
    "TZ": "UTC",
    "LEAN_NUM_THREADS": "1",
}


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
    return run(["/usr/bin/git", *args], cwd=cwd, env=BASE_ENV).strip()


def source_without_comments_and_strings(source: str) -> str:
    output: list[str] = []
    depth = 0
    index = 0
    in_string = False
    while index < len(source):
        if not in_string and source.startswith("/-", index):
            depth += 1
            output.extend("  ")
            index += 2
        elif depth and source.startswith("-/", index):
            depth -= 1
            output.extend("  ")
            index += 2
        elif depth:
            output.append("\n" if source[index] == "\n" else " ")
            index += 1
        elif not in_string and source.startswith("--", index):
            end = source.find("\n", index)
            end = len(source) if end < 0 else end
            output.extend(" " * (end - index))
            index = end
        elif source[index] == '"':
            in_string = not in_string
            output.append(" ")
            index += 1
        elif in_string:
            if source[index] == "\\" and index + 1 < len(source):
                output.extend("  ")
                index += 2
            else:
                output.append("\n" if source[index] == "\n" else " ")
                index += 1
        else:
            output.append(source[index])
            index += 1
    assert depth == 0 and not in_string, "unterminated Lean comment or string"
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


def pinned_lean_path(lean: Path, manifest: dict) -> str:
    roots: list[Path] = []
    for entry in manifest["packages"]:
        if entry.get("type") == "path":
            package = (LEAN_ROOT / entry["dir"]).resolve()
        else:
            package = (LEAN_ROOT / ".lake" / "packages" / entry["name"]).resolve()
        build_lib = package / ".lake" / "build" / "lib" / "lean"
        if build_lib.is_dir():
            roots.append(build_lib)
    local = (LEAN_ROOT / ".lake" / "build" / "lib" / "lean").resolve()
    if local.is_dir():
        roots.append(local)
    roots.append(lean.parent.parent / "lib" / "lean")
    assert roots and all(path.is_dir() for path in roots)
    return ":".join(str(path) for path in roots)


def isolated_replay(lean: Path, bwrap: Path, lean_path: str) -> dict[str, str]:
    with tempfile.TemporaryDirectory(prefix="stage1-m0590-validation-", dir="/tmp") as tmp_name:
        tmp = Path(tmp_name).resolve()
        for name in (
            "Statement.lean", "ObligationTree.lean", "AnchorAudit.lean", "Proof.lean",
            "Validation.lean",
        ):
            shutil.copy2(HERE / name, tmp / name)
        (tmp / "home").mkdir()
        base = [
            str(bwrap), "--ro-bind", "/", "/", "--bind", str(tmp), str(tmp),
            "--dev", "/dev", "--proc", "/proc", "--unshare-net", "--die-with-parent",
            "--clearenv", "--setenv", "HOME", str(tmp / "home"), "--setenv", "TMPDIR",
            str(tmp), "--setenv", "LANG", "C.UTF-8", "--setenv", "LC_ALL", "C.UTF-8",
            "--setenv", "TZ", "UTC", "--setenv", "LEAN_NUM_THREADS", "1", "--chdir",
            str(tmp),
        ]

        def lean_run(name: str, module_path: str, emit_olean: bool) -> str:
            argv = base + ["--setenv", "LEAN_PATH", module_path, str(lean), "--trust=0", "-t0"]
            if emit_olean:
                argv += ["-o", name.replace(".lean", ".olean")]
            argv.append(name)
            return run(argv, timeout=600)

        statement = lean_run("Statement.lean", lean_path, True)
        tree = lean_run("ObligationTree.lean", f"{tmp}:{lean_path}", True)
        proof = lean_run("Proof.lean", f"{tmp}:{lean_path}", True)
        return {
            "statement": statement,
            "obligation_tree": tree,
            "proof": proof,
            "anchor_audit": lean_run("AnchorAudit.lean", f"{tmp}:{lean_path}", False),
            "validation": lean_run("Validation.lean", f"{tmp}:{lean_path}", True),
        }


def main() -> None:
    execution = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")
    targets = load(ROOT / "Docs" / "Stage1_Targets_rev-5.6.json")
    statement = load(HERE / "statement.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    frozen_specs = load(HERE / "validation-specs.json")
    proof_receipt = load(HERE / "proof-receipt.json")
    proof_blocker = load(HERE / "proof-blocker.json")
    spec = load(HERE / "validation-spec.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target == {
        "execution_rank": 630,
        "legacy_priority_slot": None,
        "theorem_id": THEOREM,
        "name": "布朗-道格拉斯-菲尔莫尔理论",
        "category": "拓扑学 / 代数拓扑",
        "source_status_untrusted": "已验证",
        "baseline": "L0",
        "rework_required": True,
        "legacy_artifacts_accepted": False,
        "target_lane": "hard_statement_first_partial_verification",
        "intake_score": 132,
        "lifecycle_mode": "planned",
        "theorem_complete": False,
    }
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item == {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 630,
        "phase": "validation",
        "layer": 5,
        "state": "[ ]",
        "depends_on": ["S56-M-0590-PROOF"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Run hermetic kernel, trust, provenance, and independent validation gates.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }
    predecessor = next(row for row in execution["items"] if row["id"] == "S56-M-0590-PROOF")
    assert predecessor["state"] == "[_]" and predecessor["attempts"] == 1

    for name, expected in EXPECTED_INPUTS.items():
        assert sha256(HERE / name) == expected, f"stale validation input: {name}"
    assert sha256(LEAN_ROOT / "lean-toolchain") == TOOLCHAIN_SHA256
    assert sha256(LEAN_ROOT / "lake-manifest.json") == MANIFEST_SHA256
    assert statement["canonical_expression"] == "THMM0590.brownDouglasFillmoreTarget"
    assert statement["environment"]["statement_sha256"] == STATEMENT_SOURCE_SHA256
    assert statement["theorem_complete"] is False
    assert registry["root_obligation_id"] == graphs["root_node_id"] == "M0590-ROOT"
    assert registry["denominator_sha256"] == graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert len(registry["obligations"]) == 17
    required_machine = registry["frozen_denominators"]["required_machine"]
    assert len(required_machine) == 15
    terminal_bodies = {
        row["obligation_id"]: row["terminal_proof_body_id"]
        for row in registry["obligations"] if row["obligation_id"] in required_machine
    }
    assert terminal_bodies["M0590-ROOT"] is None
    assert terminal_bodies["M0590-B-FORWARD"] is None
    assert terminal_bodies["M0590-T-BACKWARD"] is None
    assert terminal_bodies["M0590-T-ASSEMBLE"] is not None
    closure = graphs["closure_boundary"]
    assert closure["root_closed"] is closure["audit_complete"] is closure["theorem_complete"] is False
    assert closure["remaining_root_cut_set"] == OPEN_ROOT_CUT
    assert closure["composition_certificates"] == [COMPOSITION_DECLARATION]
    graph_root = next(node for node in graphs["nodes"] if node["obligation_id"] == "M0590-ROOT")
    assert {
        "H": graph_root["human_debt"],
        "M": graph_root["machine_debt"],
        "R": graph_root["readability_debt"],
    } == ROOT_VECTOR
    assert graphs["graphs"]["evidence"]["edges"] == []

    assert frozen_specs["item_id"] == "S56-M-0590-OBLIGATION_TREE"
    assert len(frozen_specs["recipes"]) == 17
    assert {tuple(recipe["argv"]) for recipe in frozen_specs["recipes"]} == {
        ("python3", f"Stage1_Instances/{THEOREM}/check_obligation_tree.py")
    }
    assert proof_receipt["item_id"] == "S56-M-0590-PROOF"
    assert proof_receipt["support_state"] == "provisional_worker_selftest"
    assert proof_receipt["accepted"] is False
    assert proof_receipt["supported_obligation_ids"] == []
    assert proof_receipt["provisionally_closed_obligation_ids"] == []
    assert proof_receipt["accepted_closed_obligation_ids"] == []
    assert proof_receipt["result"]["proof_phase_complete"] is False
    assert proof_receipt["result"]["root_kernel_closed"] is False
    assert proof_receipt["result"]["theorem_complete"] is False
    assert proof_receipt["remaining_root_cut_set"] == OPEN_ROOT_CUT
    assert proof_blocker["root_closed"] is proof_blocker["theorem_complete"] is False
    assert proof_blocker["remaining_root_cut_set"] == OPEN_ROOT_CUT

    assert spec["schema_version"] == "stage1-validation-spec/1.0"
    assert spec["item_id"] == ITEM and spec["theorem_id"] == THEOREM
    assert spec["cwd"] == "." and spec["network_policy"] == "denied"
    assert spec["argv"] == [
        "python3", "-I", "-B", f"Stage1_Instances/{THEOREM}/check_validation.py"
    ]
    assert spec["expected_exit"] == 0 and spec["timeout_seconds"] == 600
    assert set(spec["covered_declarations"]) == {
        "THMM0590.brownDouglasFillmoreTarget", COMPOSITION_DECLARATION,
        *PROOF_DECLARATIONS, *VALIDATION_DECLARATIONS,
    }

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by|run_tac|oracle)\b|"
        r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
        r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
        r"(?:axiom|constant|opaque|unsafe|extern)\b",
        flags=re.MULTILINE,
    )
    for name in (
        "Statement.lean", "ObligationTree.lean", "AnchorAudit.lean", "Proof.lean",
        "Validation.lean",
    ):
        source = source_without_comments_and_strings((HERE / name).read_text(encoding="utf-8"))
        assert prohibited.search(source) is None, name
    validation_source = source_without_comments_and_strings(
        (HERE / "Validation.lean").read_text(encoding="utf-8")
    )
    assert not re.search(r"^import (?:Proof|ObligationTree)$", validation_source, re.MULTILINE)
    assert "exact THMM0590.root_of_directional_packages" not in validation_source
    proof_source = source_without_comments_and_strings((HERE / "Proof.lean").read_text())
    assert not re.search(
        r"^theorem\s+(?:brownDouglasFillmoreTarget|ForwardInvariantPackage|BackwardClassificationPackage)\b",
        proof_source, re.MULTILINE,
    )

    manifest = load(LEAN_ROOT / "lake-manifest.json")
    mathlib_entry = next(row for row in manifest["packages"] if row["name"] == "mathlib")
    assert mathlib_entry["rev"] == mathlib_entry["inputRev"] == MATHLIB_REVISION
    assert mathlib_entry["url"] == MATHLIB_REMOTE
    assert (LEAN_ROOT / ".lake").is_symlink()
    mathlib = (LEAN_ROOT / ".lake" / "packages" / "mathlib").resolve()
    assert git("rev-parse", "HEAD", cwd=mathlib) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == MATHLIB_TREE
    assert git("status", "--porcelain=v1", "--untracked-files=all", cwd=mathlib) == ""
    assert git("remote", "get-url", "origin", cwd=mathlib) == MATHLIB_REMOTE
    assert sha256(mathlib / "LICENSE") == MATHLIB_LICENSE_SHA256
    for relative, record in SOURCE_PROVENANCE.items():
        source = mathlib / relative
        olean = mathlib / ".lake" / "build" / "lib" / "lean" / relative.replace(".lean", ".olean")
        assert git("rev-parse", f"HEAD:{relative}", cwd=mathlib) == record["blob"]
        assert sha256(source) == record["source_sha256"]
        assert sha256(olean) == record["olean_sha256"]
        assert olean.stat().st_size == record["olean_bytes"]

    lean = Path(run(["lake", "env", "which", "lean"], cwd=LEAN_ROOT, env=BASE_ENV).strip())
    lake = lean.parent / "lake"
    bwrap = Path(shutil.which("bwrap") or "")
    assert lean.is_file() and lake.is_file() and bwrap.is_file()
    assert sha256(lean) == LEAN_SHA256 and sha256(lake) == LAKE_SHA256
    assert sha256(bwrap) == BWRAP_SHA256
    assert LEAN_COMMIT in run([str(lean), "--version"], env=BASE_ENV)
    lean_path = pinned_lean_path(lean, manifest)
    outputs = isolated_replay(lean, bwrap, lean_path)

    assert "THMM0590.brownDouglasFillmoreTarget" in outputs["statement"]
    assert reported_axioms(outputs["obligation_tree"], COMPOSITION_DECLARATION) == EXPECTED_AXIOMS
    for declaration in PROOF_DECLARATIONS:
        assert reported_axioms(outputs["proof"], declaration) == EXPECTED_AXIOMS
    for declaration in VALIDATION_DECLARATIONS:
        assert reported_axioms(outputs["validation"], declaration) == EXPECTED_AXIOMS
    closure = re.search(
        r"VALIDATION_CLOSURE roots=(\d+) declarations=(\d+) modules=(\d+) "
        r"bodyless_nonaxioms=(\d+) unsafe=(\d+)",
        outputs["validation"],
    )
    assert closure is not None
    assert dict(zip(EXPECTED_CLOSURE, map(int, closure.groups()))) == EXPECTED_CLOSURE
    combined = "\n".join(outputs.values())
    for bad in (
        "declaration uses 'sorry'", "declaration has metavariables", "unsolved goals",
        "unknown constant", "error:",
    ):
        assert bad not in combined

    receipt = load(HERE / "validation-receipt.json")
    blocker = load(HERE / "validation-blocker.json")
    selftest = load(ROOT / ".stage1-worker-selftest.json")
    assert receipt["item_id"] == blocker["item_id"] == selftest["item_id"] == ITEM
    assert receipt["theorem_id"] == blocker["theorem_id"] == THEOREM
    assert receipt["base_revision"] == blocker["base_revision"] == selftest["base_revision"] == BASE_REVISION
    assert receipt["base_tree"] == blocker["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == selftest["state"] == "[_]"
    assert receipt["accepted"] is receipt["release_grade"] is False
    assert receipt["verdict"] == blocker["verdict"] == "blocked"
    assert receipt["root_vector_before"] == receipt["root_vector_after"] == ROOT_VECTOR
    assert receipt["result"]["root_kernel_closed"] is False
    assert receipt["result"]["audit_complete"] is receipt["result"]["theorem_complete"] is False
    assert receipt["result"]["accepted_closed_obligation_ids"] == []
    assert receipt["remaining_root_cut_set"] == blocker["remaining_root_cut_set"] == OPEN_ROOT_CUT
    assert receipt["first_failed_gate"] == blocker["first_failed_gate"]
    assert set(receipt["changed_paths"]) == set(selftest["changed_paths"]) == CHANGED_PATHS
    for key in (
        "recipe_id", "cwd", "argv", "env_allowlist", "timeout_seconds", "network_policy",
        "network_enforcement", "expected_exit", "expected_outputs", "covered_obligation_ids",
        "observationally_covered_obligation_ids", "partially_covered_obligation_ids",
        "covered_declarations", "scope_boundary",
    ):
        assert receipt["recipe"][key] == spec[key]

    for line in SUMMARY_LINES:
        print(line)


if __name__ == "__main__":
    main()
