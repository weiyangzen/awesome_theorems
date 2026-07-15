#!/usr/bin/env python3
"""Fail-closed release reconciliation for S56-M-0533-RELEASE."""

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


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0533"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
ITEM = "S56-M-0533-RELEASE"
THEOREM = "THM-M-0533"
BASE_REVISION = "9dd7d7ec7d399cdac6abb2a51d3ea55ed5f4b8ca"
BASE_TREE = "af8d932b6def693afe67a997e2be4c6e813036f2"
TOOLCHAIN_ROOT = Path.home() / ".elan/toolchains/leanprover--lean4---v4.29.0"
LEAN = TOOLCHAIN_ROOT / "bin/lean"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
LEAN_SHA256 = "3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf"
LAKE = TOOLCHAIN_ROOT / "bin/lake"
LAKE_SHA256 = "a608ff084d7e2af228b92a29d7c2fd083ba0580e46889175ec74a81678c98359"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MATHLIB_ORIGIN = "https://github.com/leanprover-community/mathlib4.git"
MATHLIB_LICENSE_SHA256 = (
    "b40930bbcf80744c86c46a12bc9da056641d722716c378f5659b9e555ef833e1"
)
DENOMINATOR_SHA256 = "238242dfcb6274343a6413ed2628d0944bf0882c280b42608d8e19bad2c88dfc"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
PRIORITY_BLOCKERS = [
    "M0533-C-SUBDIVISION",
    "M0533-L-SMALL-QUASIISO",
    "M0533-L-CHAIN-KERNEL",
    "M0533-L-NATURALITY",
    "M0533-T-DEGREE-ZERO",
]
INVENTORY_IDS = [
    "M0533-ROOT", "M0533-S-DEFINITIONS", "M0533-S-BOUNDARY",
    "M0533-S-FOUNDATION", "M0533-C-SUBDIVISION",
    "M0533-L-SMALL-QUASIISO", "M0533-C-CHAIN-SES",
    "M0533-L-CHAIN-KERNEL", "M0533-C-BOUNDARY",
    "M0533-L-NATURALITY", "M0533-T-CONSTRUCTION",
    "M0533-T-EXACT-INTER", "M0533-T-EXACT-BIPROD",
    "M0533-T-EXACT-SPACE", "M0533-T-DEGREE-ZERO",
    "M0533-T-EXACTNESS", "M0533-T-ASSEMBLE", "M0533-X-SOURCE",
    "M0533-X-PROVENANCE",
]
EXPECTED_INPUTS = {
    "instance.json": "5a282e6be764a9e7720f10cc848b95b3251080c6afa0fbea660cb99d4f2c3ed1",
    "README.md": "2f3af46262a3babefee9dbf913bdffcf2014ac221bc4e85de5402032fae5255e",
    "Statement.lean": "cbe35890b43f302b71cf1230a87c21b2ac4eedf196210389598453c61ff18bce",
    "AnchorAudit.lean": "f961c09b06b643a85a22080a7cbbb624f0b55b5f44458e3b068e3d164b9d7312",
    "ObligationTree.lean": "ded027e2345e1b81568067254d083de705bf062e0f9079fe6d2a427c2c21f3b1",
    "Proof.lean": "4b577167c4778809d6585256f7683df4242488b5132669d0c3365a8912360837",
    "Validation.lean": "13a35cba8e198fb9910c1242b359402538c98c6d423eb6d40ed2de58f0f51131",
    "anchor-audit.md": "bf50321ccb27ca382d051c7f5f591e49163b7d07709d6ee8b1b3430831a1060a",
    "source-statement-crosswalk.md": "f42ffd34e8fa4d36f320efb22069a4fd70bea2bfecd93c0e6110af9070bd5459",
    "obligation-registry.json": "cd0411fccc46ee639e87328a41ce396b92f62467fdffd68d9a39761387c9b630",
    "typed-graphs.json": "6ac4e3d41e8e184c6a88f7ffdcde043a79c43e6766a664caf12453aab66a9a24",
    "proof-receipt.json": "7c167975af38f5e3c20d51363852f979ea2c23e966695efae545c71464d8e0cc",
    "proof-blocker.json": "d222d860817cf09ce2bd671a28135a95534092fb921a5c5fb128032825c1b20a",
    "validation-spec.json": "10d49abbc8113eb1d83bf1754cd4df727ae2ecf97af3e668a0ae3f18a8b85589",
    "validation-receipt.json": "715632876390cad57b63b89b2561d13a5873c21dc31f9c04b180d78400ee72cb",
    "validation-phase.md": "c633dea6819ecdc9669c0c605e01698479d76524b33480f8eae2710b3135ed52",
    "check_obligation_tree.py": "72f8ce8e19aec8c3174a7dd2359304811bb1ba228516b7d58d4b27fa4c51d670",
    "check_validation.py": "14f0fcc9897bfd767376125b8bc1bfa3982f4f59dc1be34e0aa494dac63e89e5",
}
EXPECTED_AUTHORITY_INPUTS = {
    "Docs/Stage1_Blueprint_rev-5.6.md": "ea75a2d138d2124aff3dc3d9ce6bd68f1cbf6c4493d2364e7a15c212f81de0d7",
    "Docs/Stage1_Targets_rev-5.6.json": "02eec284de534dd78e1cf75f82a477ff477567dd682b7445cb7587abd137ab2c",
    "Docs/Stage1_Execution_DAG_rev-5.6.json": "a68f9c34a9302906cad3e0f8c3e01fba606ce2d6fb4cc7bd467823dd2c360dac",
    "Docs/Blueprint_Guidelines.md": "a06c07b5ca1b270b4935ad3dab893e9a0e078c29c8da2ef9dca1e71193310535",
    "skills/execute-stage1-rev56/SKILL.md": "26d47a66c6535feabb8bbf1051fd55d76a53fe761f4b3d953f86b97ec86152b8",
    "Formalizations/Lean/lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "Formalizations/Lean/lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
EXPECTED_RELEASE_OUTPUTS = {
    "release-decision.json": "02d84509cdb68da7e045021ac05eb1abcde28e072e5dbfae67690f8623362868",
    "release-spec.json": "260151ff41120b67700e9be9f3f7ed790c8ff0db96dc353f91612aeee805decd",
    "release-validation.md": "b2bcdbbc25e795671148e64adf3f0fbfe3ecd7fd4fa85368cf0e5faebc6ce12c",
}
EXPECTED_LEAN_OUTPUTS = {
    "statement": "289155fdc48045e69bfad0bd2a39354d84e479ce17c88b7f208f4ca70faf9652",
    "obligation": "749d3ca4b389b169c6e15b03832a934fbec792de59777b37f35414bbe7d64217",
    "proof": "87dceff4d92d5d3db3283c9e2ba0d9a8f66134503701a47a18239a4e47fb223b",
    "validation": "1bbf5c2aff6dea6fb4ffbf0d94fd21e43050781727254e2e9ddb68679e122a2a",
}
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    *(f"Stage1_Instances/{THEOREM}/{name}" for name in (
        "check_release.py", "release-decision.json", "release-receipt.json",
        "release-spec.json", "release-validation.md",
    )),
}
SUMMARY_LINES = [
    "PASS release reconciliation: target, DAG, receipts, registry, graphs, and hashes agree",
    "PASS narrow Lean replay: exact statement, conditional assembly, and two elementary partial bodies checked at trust zero",
    "BLOCKED S56-10.2-DEPENDENCY-ACCEPTANCE: validation is provisional and not master accepted",
    "BLOCKED exact root: H3/M3/R4 unchanged; zero frozen obligations accepted",
    "BLOCKED AUDIT-Z and THEOREM-Z: expression, proof, source/readability, trust, hermetic, and independent gates are open",
    "verdict=blocked audit_complete=false theorem_complete=false accepted_receipts=0",
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


def run(
    argv: list[str], *, cwd: Path = ROOT, timeout: int = 900,
    env: dict[str, str] | None = None,
) -> str:
    result = subprocess.run(
        argv, cwd=cwd, env=env, text=True, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, timeout=timeout, check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(f"command failed ({result.returncode}): {argv!r}\n{result.stdout}")
    return result.stdout


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["git", *args], cwd=cwd, timeout=60).strip()


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
        re.escape(f"'{declaration}' depends on axioms: [") + r"(.*?)]",
        re.DOTALL,
    )
    matches = pattern.findall(output)
    assert output.count(no_axioms) + len(matches) == 1, declaration
    if not matches:
        return set()
    return {part.strip() for part in matches[0].split(",") if part.strip()}


def lean_path() -> str:
    paths: list[str] = []
    for path in (
        LEAN_ROOT / ".lake/packages/batteries/.lake/build/lib/lean",
        LEAN_ROOT / ".lake/packages/Qq/.lake/build/lib/lean",
        LEAN_ROOT / ".lake/packages/aesop/.lake/build/lib/lean",
        LEAN_ROOT / ".lake/packages/proofwidgets/.lake/build/lib/lean",
        LEAN_ROOT / ".lake/packages/importGraph/.lake/build/lib/lean",
        LEAN_ROOT / ".lake/packages/LeanSearchClient/.lake/build/lib/lean",
        LEAN_ROOT / ".lake/packages/plausible/.lake/build/lib/lean",
        LEAN_ROOT / ".lake/packages/mathlib/.lake/build/lib/lean",
        LEAN_ROOT / ".lake/build/lib/lean",
        TOOLCHAIN_ROOT / "lib/lean",
    ):
        assert path.resolve().is_dir(), f"required pinned artifact missing: {path}"
        paths.append(str(path.resolve()))
    return ":".join(paths)


def narrow_lean_replay() -> dict[str, str]:
    bwrap = Path(shutil.which("bwrap") or "")
    assert bwrap == Path("/usr/bin/bwrap") and bwrap.is_file()
    base_path = lean_path()
    with tempfile.TemporaryDirectory(prefix="stage1-m0533-release-", dir="/tmp") as name:
        tmp = Path(name).resolve()
        (tmp / "home").mkdir()
        for source in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
            shutil.copy2(HERE / source, tmp / source)
        base = [
            str(bwrap), "--ro-bind", "/", "/", "--bind", str(tmp), str(tmp),
            "--dev", "/dev", "--proc", "/proc", "--unshare-net",
            "--die-with-parent", "--clearenv", "--setenv", "HOME", str(tmp / "home"),
            "--setenv", "LANG", "C.UTF-8", "--setenv", "LC_ALL", "C.UTF-8",
            "--setenv", "TZ", "UTC", "--setenv", "LEAN_NUM_THREADS", "1",
            "--chdir", str(tmp),
        ]

        def check(source: str, module_path: str, emit_olean: bool) -> str:
            argv = base + [
                "--setenv", "LEAN_PATH", module_path, str(LEAN), "--trust=0", "-t0",
            ]
            if emit_olean:
                argv += ["-o", source.replace(".lean", ".olean")]
            argv.append(source)
            return run(argv, timeout=600)

        outputs = {
            "statement": check("Statement.lean", base_path, True),
            "obligation": check("ObligationTree.lean", f"{tmp}:{base_path}", True),
            "proof": check("Proof.lean", f"{tmp}:{base_path}", True),
            "validation": check("Validation.lean", f"{tmp}:{base_path}", False),
        }

    assert "AwesomeTheorems.THM_M_0533.MayerVietorisSequence" in outputs["statement"]
    for declaration, key in (
        ("AwesomeTheorems.THM_M_0533.root_of_construction_and_exactness", "obligation"),
        ("AwesomeTheorems.THM_M_0533.firstMap_comp_secondMap", "proof"),
        (
            "AwesomeTheorems.THM_M_0533.Validation."
            "independentlyReconstructedFirstSecond",
            "validation",
        ),
    ):
        assert reported_axioms(outputs[key], declaration) == EXPECTED_AXIOMS
    assert outputs["validation"].count("Declarations are sorry-free!") == 1
    combined = "\n".join(outputs.values())
    assert "sorryAx" not in combined and "declaration uses 'sorry'" not in combined
    assert "error:" not in combined
    return {key: hashlib.sha256(value.encode()).hexdigest() for key, value in outputs.items()}


def main() -> None:
    if sys.flags.optimize != 0:
        raise RuntimeError("release checker requires Python assertions")

    decision = load(HERE / "release-decision.json")
    receipt = load(HERE / "release-receipt.json")
    spec = load(HERE / "release-spec.json")
    instance = load(HERE / "instance.json")
    validation = load(HERE / "validation-receipt.json")
    proof = load(HERE / "proof-receipt.json")
    blocker = load(HERE / "proof-blocker.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    targets = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 590 and target["baseline"] == "L0"
    assert target["lifecycle_mode"] == "planned"
    assert target["rework_required"] is True and target["theorem_complete"] is False
    assert instance["lifecycle"] == "planned" and instance["theorem_complete"] is False
    assert instance["root_vector"] == {"H": "H3", "M": "M4", "R": "R4"}

    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item == {
        "id": ITEM, "theorem_id": THEOREM, "execution_rank": 590,
        "phase": "release", "layer": 6, "state": "[ ]",
        "depends_on": ["S56-M-0533-VALIDATION"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Reconcile evidence and decide the exact theorem-completion verdict.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0, "children": [],
    }
    predecessor = next(
        row for row in execution["items"] if row["id"] == "S56-M-0533-VALIDATION"
    )
    assert predecessor["state"] == "[_]" and predecessor["attempts"] == 1

    for name, expected in EXPECTED_INPUTS.items():
        assert sha256(HERE / name) == expected, f"reconciled input drifted: {name}"
    for relative, expected in EXPECTED_AUTHORITY_INPUTS.items():
        assert sha256(ROOT / relative) == expected, f"authority input drifted: {relative}"
    for name, expected in EXPECTED_RELEASE_OUTPUTS.items():
        assert sha256(HERE / name) == expected, f"release output drifted: {name}"
    assert receipt["release_output_bindings"] == {
        f"Stage1_Instances/{THEOREM}/check_release.py": sha256(
            Path(__file__).resolve()
        ),
        **{
            f"Stage1_Instances/{THEOREM}/{name}": expected
            for name, expected in EXPECTED_RELEASE_OUTPUTS.items()
        },
    }
    assert decision["reconciled_inputs"] == EXPECTED_INPUTS
    assert decision["authority_inputs"] == EXPECTED_AUTHORITY_INPUTS

    assert registry["root_obligation_id"] == graphs["root_node_id"] == "M0533-ROOT"
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert registry["frozen_denominators"]["inventory"] == INVENTORY_IDS
    closure = graphs["closure_boundary"]
    assert closure["root_closed"] is False and closure["root_machine_debt"] == "M3"
    assert closure["audit_complete"] is closure["theorem_complete"] is False
    assert closure["remaining_root_cut_set"] == PRIORITY_BLOCKERS
    assert closure["closed_obligations"] == ["M0533-S-DEFINITIONS", "M0533-T-ASSEMBLE"]
    node = next(row for row in graphs["nodes"] if row["obligation_id"] == "M0533-T-ASSEMBLE")
    assert node["machine_debt"] == "M0-L"
    certificate = graphs["composition_certificates"]
    assert certificate == [{
        "parent": "M0533-ROOT",
        "declaration": "AwesomeTheorems.THM_M_0533.root_of_construction_and_exactness",
        "premises": ["M0533-T-CONSTRUCTION", "M0533-T-EXACTNESS"],
        "status": "checked_conditional",
    }]
    assert decision["graph_reconciliation_failure"]["illegally_closed_parent_ids"] == [
        "M0533-T-ASSEMBLE"
    ]

    assert proof["support_state"] == "provisional_worker_selftest"
    assert proof["closed_obligation_ids"] == []
    assert proof["partial_progress_toward_obligation_ids"] == ["M0533-T-CONSTRUCTION"]
    assert proof["result"]["root_closed"] is proof["result"]["theorem_complete"] is False
    assert blocker["root_closed"] is blocker["audit_complete"] is False
    assert blocker["theorem_complete"] is False
    assert blocker["remaining_root_cut_set"] == PRIORITY_BLOCKERS

    assert validation["support_state"] == "provisional_worker_selftest"
    assert validation["accepted"] is validation["release_grade"] is False
    assert validation["verdict"] == "blocked"
    assert validation["result"]["accepted_closed_obligation_ids"] == []
    assert validation["result"]["graph_illegally_closed_parent_ids"] == [
        "M0533-T-ASSEMBLE"
    ]
    assert validation["result"]["root_closed"] is False
    assert validation["result"]["root_kernel_closed"] is False
    assert validation["result"]["root_vector_before"] == {
        "H": "H3", "M": "M3", "R": "R4"
    }
    assert validation["result"]["root_vector_after"] == validation["result"][
        "root_vector_before"
    ]
    assert validation["result"]["audit_complete"] is False
    assert validation["result"]["theorem_complete"] is False
    assert validation["hermeticity"]["decision"] == "fail_closed_nonrelease_warm_cache_replay"
    assert validation["independent_validation"]["decision"] == "fail_closed"

    assert decision["item_id"] == receipt["item_id"] == ITEM
    assert decision["theorem_id"] == receipt["theorem_id"] == THEOREM
    assert decision["base_revision"] == receipt["base_revision"] == BASE_REVISION
    assert decision["base_tree"] == receipt["base_tree"] == BASE_TREE
    assert decision["support_state"] == receipt["support_state"] == (
        "provisional_worker_selftest"
    )
    assert decision["proposed_state"] == receipt["proposed_state"] == "[_]"
    assert decision["accepted"] is receipt["accepted"] is False
    assert decision["release_grade"] is receipt["release_grade"] is False
    assert decision["verdict"] == receipt["verdict"] == "blocked"
    assert decision["accepted_receipt_ids"] == receipt["accepted_receipt_ids"] == []
    result = decision["decision"]
    assert result["lifecycle_before"] == result["lifecycle_after"] == "planned"
    assert result["root_vector_before"] == result["root_vector_after"] == [
        "H3", "M3", "R4"
    ]
    assert result["audit_complete"] is result["theorem_complete"] is False
    assert result["release_accepted"] is False
    assert result["first_failed_gate"]["gate_id"] == "S56-10.2-DEPENDENCY-ACCEPTANCE"
    assert result["first_failed_target_identity_gate"]["gate_id"] == (
        "S56-5.1-EXPRESSION-FINGERPRINT"
    )
    assert result["first_failed_theorem_gate"]["gate_id"] == "M0533-C-SUBDIVISION"
    assert result["first_failed_release_assurance_gate"]["gate_id"] == (
        "S56-10.6-HERMETIC-COLD-EMPTY-CACHE"
    )
    assert result["remaining_root_priority_blocker_set"] == PRIORITY_BLOCKERS
    assert "not a complete or proven minimal graph cut" in result["priority_set_boundary"]

    dependency = decision["dependency"]
    assert dependency["item_id"] == validation["item_id"]
    assert dependency["receipt_id"] == validation["receipt_id"]
    assert dependency["receipt_sha256"] == sha256(HERE / "validation-receipt.json")
    assert dependency["support_state"] == validation["support_state"]
    assert dependency["accepted"] is dependency["release_grade"] is False
    assert dependency["master_accepted"] is False

    for key in (
        "accepted_exact_expression_fingerprint", "accepted_exact_root_kernel_closure",
        "authoritative_graph_reconciled", "audit_z_accepted", "primary_source_h0_review",
        "independent_r0_review", "complete_transitive_provenance_foundation_and_tcb",
        "immutable_clean_release_input", "hermetic_cold_empty_cache_offline_replay",
        "sbom_license_and_archive_closure", "two_distinct_signed_runner_attestations",
        "independently_implemented_minimal_verifier", "protected_mutation_and_metamorphic_ci",
        "deterministic_content_addressed_release_bundle", "master_acceptance",
    ):
        assert decision["evidence_reconciliation"][key] is False, key

    assert spec["schema_version"] == "stage1-validation-recipe/1.0"
    assert spec["item_id"] == ITEM and spec["theorem_id"] == THEOREM
    assert spec["argv"] == [
        "python3", "-I", "-B", f"Stage1_Instances/{THEOREM}/check_release.py"
    ]
    assert spec["cwd"] == "." and spec["timeout_seconds"] == 900
    assert spec["network_policy"] == "denied" and spec["expected_exit"] == 0
    assert spec["covered_obligation_ids"] == INVENTORY_IDS
    assert spec["covered_decisions"] == ["AUDIT-Z", "THEOREM-Z"]

    all_source = "\n".join(
        source_without_comments((HERE / name).read_text(encoding="utf-8"))
        for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean")
    )
    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by)\b|"
        r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
        r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
        r"(?:axiom|constant|opaque|unsafe|extern)\b",
        re.MULTILINE,
    )
    assert prohibited.search(all_source) is None
    proof_and_validation = "\n".join(
        source_without_comments((HERE / name).read_text(encoding="utf-8"))
        for name in ("Proof.lean", "Validation.lean")
    )
    assert re.search(
        r"^theorem[ \t]+MayerVietorisSequence\b", proof_and_validation, re.MULTILINE
    ) is None

    assert LEAN.is_file() and LAKE.is_file()
    assert sha256(LEAN) == LEAN_SHA256 and sha256(LAKE) == LAKE_SHA256
    assert LEAN_COMMIT in run([str(LEAN), "--version"], timeout=60)
    mathlib = LEAN_ROOT / ".lake/packages/mathlib"
    assert mathlib.resolve().is_dir()
    assert git("rev-parse", "HEAD", cwd=mathlib) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == MATHLIB_TREE
    assert git("status", "--porcelain=v1", "--untracked-files=all", cwd=mathlib) == ""
    assert git("remote", "get-url", "origin", cwd=mathlib) == MATHLIB_ORIGIN
    assert sha256(mathlib / "LICENSE") == MATHLIB_LICENSE_SHA256

    lean_hashes = narrow_lean_replay()
    assert lean_hashes == EXPECTED_LEAN_OUTPUTS
    assert receipt["result"]["current_release_lean_output_sha256"] == (
        EXPECTED_LEAN_OUTPUTS
    )

    assert set(packet) == {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert packet["item_id"] == ITEM and packet["base_revision"] == BASE_REVISION
    assert packet["state"] == "[_]" and set(packet["changed_paths"]) == CHANGED_PATHS
    assert receipt["known_failures"] == packet["known_failures"]
    assert set(receipt["changed_paths"]) == CHANGED_PATHS
    assert receipt["output_summary"] == packet["output_summary"] == SUMMARY_LINES
    status = git("status", "--short", "--untracked-files=all")
    actual_changed = {
        line[3:] for line in status.splitlines()
        if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual_changed == CHANGED_PATHS, (actual_changed, CHANGED_PATHS)
    for relative in CHANGED_PATHS:
        path = ROOT / relative
        data = path.read_bytes()
        assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())

    print("\n".join(SUMMARY_LINES))


if __name__ == "__main__":
    main()
