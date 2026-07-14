#!/usr/bin/env python3
"""Fail-closed narrow validation for S56-M-1021-VALIDATION."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import time


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-1021"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM = "S56-M-1021-VALIDATION"
THEOREM = "THM-M-1021"
BASE_REVISION = "6cf20c1ab97fcd6970455baa23022062ebc14fe1"
BASE_TREE = "5fa65edc9a9b91b49f7f925ad524ec374328e14c"
EXPRESSION_SHA256 = "5b397ee9de0936db2c62ba953794ee0c2b9dc3192370aa06825fdf4aafc8322b"
DENOMINATOR_SHA256 = "032b467a59ae30caf2d637b9707358e6ba7259edf774ba0bd8bf162e48924688"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MATHLIB_REMOTE = "https://github.com/leanprover-community/mathlib4.git"
MATHLIB_LICENSE_SHA256 = "b40930bbcf80744c86c46a12bc9da056641d722716c378f5659b9e555ef833e1"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
LEAN_TOOLCHAIN = "leanprover/lean4:v4.29.0"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
EXPECTED_AXIOM_LIST = ["propext", "Classical.choice", "Quot.sound"]
UPSTREAM_REVISION = "1b56973aff9b4e6ba761a6bd8af678e38bfd8d10"
UPSTREAM_TREE = "a031b68a944a46488384ba01ac386e1b17dc242d"
UPSTREAM_POSITIVE_DEFINITE = "2f5e07e86773b57551203b3556057a2ee3dd842b627474a76c3ec98c0c74bff2"
UPSTREAM_FEJER = "503f9aaeb17becd77b5f986ebc82a3c17abcce79fd7568d3fcd66524ef352f24"
UPSTREAM_MAIN = "5a23ba46df0866f33eae31354b659f194e5ebc1a26fd47cd92f838658b278d3b"
LICENSE_SHA256 = "8ebdd6164d5245aba45342f898b1a9f1c1509246a22fdf3002a66bbbe5d70089"

EXPECTED_INPUTS = {
    "BochnerStatement.lean": "e17aaf1304266aba6bb84783cf6709b4eca34e08cc9274aebacf1479ac8762cd",
    "Proof.lean": "389f719bb6610fa8978597e793ec743c8f8680d022a166ddecbb35cfb0c5a400",
    "ProofAudit.lean": "039260edb3808462906b6406917911aff9a6af7549ad2669bb641a19a5d4dab9",
    "statement.json": "732283f757dc082397efc69fe2bf0041c7b5baf85c2fab9851f01e607164ecd5",
    "anchor_audit.json": "f5295a343f2b61af865a34352aa46104c973325698e2eeee42c3a78830d784e3",
    "obligation-registry.json": "790f2ed3c2b1683c1b47ddbfeef440bee89ff246da428656a256bffd169d8013",
    "typed-graphs.json": "0f40c21c44439a8604e1745e96af9067d634a9db325f878df38f27e38036cba0",
    "proof-receipt.json": "f2c6baa065adf681dc849127889ec8ec0625b5af55d0253a8cdf0e8d5e01614d",
    "source_statement_crosswalk.md": "6747ce08a059df983741c2778cb5c904f5df636f91fe8a5a9434ec2c95246c86",
    "check_obligation_tree.py": "3c3756fc1fc0259ed50906d65af375c4e833e282101d94997c21b59821defcb9",
    "External/Bochner/PositiveDefinite.lean": "2f5e07e86773b57551203b3556057a2ee3dd842b627474a76c3ec98c0c74bff2",
    "External/Bochner/FejerPD.lean": "a4bc1a1d3a6dc67f02f9afe8b09507131780fc2e4e94f9c0940170e264423a2c",
    "External/Bochner/Main.lean": "9ab4cd83b1694d98059ec4b6cb7b57a56e1d6798f7609938b1939a2a0788cbd0",
    "External/LICENSE": LICENSE_SHA256,
    "Validation.lean": "24a36e59f6040fa321895e0d4172209a36d75c4802d4336bb662f233c0fc61cf",
    "check_validation.sh": "97099743871a6f3a1fb026c4ca658742807abf66e09f691ffd70a742d7070ba6",
    "validation-spec.json": "117bf8d135dae25cdea59d157c7e27f17489c7b534140b7390ced6f55601b1ae",
    "validation-phase.md": "e1be00df7e3a422846aa368e82f48958fef7ca7ed9b74737a07e88ea87bbcd08",
}
EXPECTED_TOOL_INPUTS = {
    "lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
MATHLIB_SOURCES = {
    "Mathlib/MeasureTheory/Integral/Bochner/Basic.lean": (
        "587ad1e81dc387ba2835c29c4ef7aa05c5efd82e",
        "b2e4b3eb233147e1dc8d2cb8fa4eae1773badbf1e37234dd7e8dfd54d9dd0a0a",
    ),
    "Mathlib/MeasureTheory/Measure/CharacteristicFunction/TaylorExpansion.lean": (
        "85217e8085d6958515c385c3a68bc98a86378604",
        "7b7a1ded83c6c7ee6760ee8c613fbc5bf7815e214b45cf15758ee6fb2cb6d225",
    ),
}
TRUST_DECLARATIONS = [
    "bochner_theorem",
    "AwesomeTheorems.Stage1.THM_M_1021.bochner_forward",
    "AwesomeTheorems.Stage1.THM_M_1021.bochner_reverse",
    "AwesomeTheorems.Stage1.THM_M_1021.bochner_exact",
]
WITHHELD_ROUTE_IDS = [
    "M1021-BR", "M1021-C", "M1021-C1", "M1021-C1.1", "M1021-C1.2",
    "M1021-C2", "M1021-C2.1", "M1021-C2.2", "M1021-C3",
    "M1021-C3.1", "M1021-C3.2", "M1021-C4", "M1021-C5",
    "M1021-C5.1", "M1021-C5.2", "M1021-T2",
]
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/Validation.lean",
    f"Stage1_Instances/{THEOREM}/check_validation.py",
    f"Stage1_Instances/{THEOREM}/check_validation.sh",
    f"Stage1_Instances/{THEOREM}/validation-phase.md",
    f"Stage1_Instances/{THEOREM}/validation-receipt.json",
    f"Stage1_Instances/{THEOREM}/validation-spec.json",
}
SUMMARY_LINES = (
    "PASS THM-M-1021 narrow validation",
    "PASS network-isolated trust-zero kernel replay: exact statement, vendored bodies, local proof, and proof-only trust probe elaborated",
    "PASS trust observation: four checked declarations are sorry-free and report exactly propext, Classical.choice, and Quot.sound",
    "PASS selected provenance: upstream reconstruction, license, frozen hashes, clean mathlib pin, selected source blobs, and tool identities agree",
    "FAIL CLOSED authority: proof is provisional and not master-accepted; accepted root remains H1/M3/R3 with no accepted closed obligation",
    "FAIL CLOSED graph: the checked Gaussian/Prokhorov route differs from frozen Riesz C1-C5 and lacks accepted per-node composition evidence",
    "FAIL CLOSED foundation/trust/provenance: accepted policy, complete transitive closure, TCB inventory, and SBOM remain open",
    "FAIL CLOSED hermetic release: shared warm .lake is not a clean-checkout empty-cache offline replay or deterministic bundle",
    "FAIL CLOSED independent release: the trust probe shares this worker, checkout, kernel, and cache; no distinct signed verifier exists",
    "audit_complete=false; theorem_complete=false",
)
STARTED = time.monotonic()
TIMEOUT_SECONDS = 900.0


if sys.flags.optimize:
    raise SystemExit("validation failed: Python optimization disables assertions")


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict), path
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def digest_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def run(argv: list[str], *, cwd: Path = ROOT) -> str:
    remaining = TIMEOUT_SECONDS - (time.monotonic() - STARTED)
    if remaining <= 0:
        raise TimeoutError("validation recipe exceeded its 900-second wall-clock bound")
    result = subprocess.run(
        argv,
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=remaining,
        check=False,
    )
    if result.returncode:
        raise RuntimeError(
            f"validation failed ({result.returncode}): {argv!r}\n{result.stdout}"
        )
    return result.stdout


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["git", *args], cwd=cwd).strip()


def elan_binary(name: str) -> Path:
    env = dict(os.environ)
    env["ELAN_TOOLCHAIN"] = LEAN_TOOLCHAIN
    result = subprocess.run(
        ["elan", "which", name],
        cwd=LEAN_ROOT,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=30,
        check=False,
    )
    if result.returncode:
        raise RuntimeError(f"cannot resolve pinned {name}: {result.stdout}")
    path = Path(result.stdout.strip())
    assert path.is_file(), f"pinned {name} executable missing"
    return path


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


def observed_axioms(output: str, declaration: str) -> set[str]:
    match = re.search(
        re.escape(f"'{declaration}' depends on axioms: [") + r"(.*?)]",
        output,
        re.DOTALL,
    )
    if match is None:
        assert f"'{declaration}' does not depend on any axioms" in output
        return set()
    return {part.strip() for part in match.group(1).split(",") if part.strip()}


def assert_text_hygiene(path: Path) -> None:
    data = path.read_bytes()
    assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())


def main() -> None:
    targets = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    statement = load(HERE / "statement.json")
    anchor = load(HERE / "anchor_audit.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    proof_receipt = load(HERE / "proof-receipt.json")
    spec = load(HERE / "validation-spec.json")
    receipt = load(HERE / "validation-receipt.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 497 and target["baseline"] == "L0"
    assert target["lifecycle_mode"] == "planned"
    assert target["rework_required"] is True and target["theorem_complete"] is False
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item == {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 497,
        "phase": "validation",
        "layer": 5,
        "state": "[ ]",
        "depends_on": ["S56-M-1021-PROOF"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Run hermetic kernel, trust, provenance, and independent validation gates.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }
    predecessor = next(
        row for row in execution["items"] if row["id"] == "S56-M-1021-PROOF"
    )
    assert predecessor["state"] == "[_]" and predecessor["attempts"] == 1

    for name, expected in EXPECTED_INPUTS.items():
        assert sha256(HERE / name) == expected, f"stale validation input: {name}"
    for name, expected in EXPECTED_TOOL_INPUTS.items():
        assert sha256(LEAN_ROOT / name) == expected, f"changed tool input: {name}"

    assert statement["canonical_declaration"] == (
        "AwesomeTheorems.Stage1.THM_M_1021.BochnerTarget"
    )
    assert statement["elaborated_print_sha256"] == EXPRESSION_SHA256
    assert statement["source_sha256"] == EXPECTED_INPUTS["BochnerStatement.lean"]
    assert registry["root_obligation_id"] == "M1021-ROOT"
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    machine_ids = registry["frozen_denominators"]["required_machine"]
    assert len(machine_ids) == 46 and spec["covered_obligation_ids"] == machine_ids
    assert graphs["registry_sha256"] == DENOMINATOR_SHA256
    assert graphs["closure_boundary"] == {
        "closed_obligations": [],
        "root_machine_debt": "M3",
        "remaining_root_cut_set": ["M1021-BR", "M1021-C"],
        "proof_claimed": False,
        "theorem_complete": False,
    }
    root_node = next(row for row in graphs["nodes"] if row["obligation_id"] == "M1021-ROOT")
    assert (root_node["human_debt"], root_node["machine_debt"], root_node["readability_debt"]) == (
        "H1", "M3", "R3"
    )
    assert "policy-audit-pending" in root_node["foundation_profile"]
    assert "transitive-closure-pending" in root_node["tcb_profile"]
    assert all(not node["evidence_ids"] for node in graphs["nodes"])

    assert proof_receipt["item_id"] == "S56-M-1021-PROOF"
    assert proof_receipt["accepted"] is False
    assert proof_receipt["canonical_target_expression_sha256"] == EXPRESSION_SHA256
    assert proof_receipt["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert proof_receipt["closed_obligation_ids"] == []
    assert proof_receipt["accepted_closed_obligation_ids"] == []
    assert proof_receipt["withheld_frozen_route_ids"] == WITHHELD_ROUTE_IDS
    assert proof_receipt["root_evidence"]["root_kernel_declaration_closed"] is True
    assert proof_receipt["root_evidence"]["frozen_graph_closed"] is False
    assert proof_receipt["root_evidence"]["accepted_root_closed"] is False
    assert proof_receipt["result"]["axioms"] == EXPECTED_AXIOM_LIST
    assert proof_receipt["result"]["theorem_complete"] is False
    assert proof_receipt["upstream"]["revision"] == UPSTREAM_REVISION
    assert proof_receipt["upstream"]["tree"] == UPSTREAM_TREE
    assert anchor["exact_candidate_found"] is anchor["external_candidate_found"] is False
    assert anchor["theorem_complete"] is False
    crosswalk = (HERE / "source_statement_crosswalk.md").read_text(encoding="utf-8")
    assert "No `H0`" in crosswalk

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by|extern|oracle)\b|"
        r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
        r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
        r"(?:axiom|constant|opaque|unsafe)\b",
        re.MULTILINE,
    )
    lean_sources = [
        HERE / "BochnerStatement.lean",
        HERE / "Proof.lean",
        HERE / "Validation.lean",
        HERE / "External/Bochner/PositiveDefinite.lean",
        HERE / "External/Bochner/FejerPD.lean",
        HERE / "External/Bochner/Main.lean",
    ]
    for path in lean_sources:
        source = code_without_comments(path.read_text(encoding="utf-8"))
        source = re.sub(r"^#print sorries .*?$", "", source, flags=re.MULTILINE)
        assert prohibited.search(source) is None, f"prohibited source token in {path.name}"
    validation = code_without_comments((HERE / "Validation.lean").read_text(encoding="utf-8"))
    assert "import «Stage1_Instances».«THM-M-1021».Proof" in validation
    assert "theorem " not in validation and "lemma " not in validation and "def " not in validation
    for declaration in TRUST_DECLARATIONS:
        assert f"assert_no_sorry {declaration}" in validation
        assert f"#print sorries {declaration}" in validation
        assert f"#print axioms {declaration}" in validation

    positive = (HERE / "External/Bochner/PositiveDefinite.lean").read_text(encoding="utf-8")
    fejer = (HERE / "External/Bochner/FejerPD.lean").read_text(encoding="utf-8")
    main_source = (HERE / "External/Bochner/Main.lean").read_text(encoding="utf-8")
    assert digest_bytes(positive.encode()) == UPSTREAM_POSITIVE_DEFINITE
    assert fejer.count("import External.Bochner.PositiveDefinite") == 1
    reconstructed_fejer = fejer.replace(
        "import External.Bochner.PositiveDefinite", "import Bochner.PositiveDefinite"
    )
    assert digest_bytes(reconstructed_fejer.encode()) == UPSTREAM_FEJER
    assert main_source.count("import External.Bochner.PositiveDefinite") == 1
    assert main_source.count("import External.Bochner.FejerPD") == 1
    assert main_source.count(
        "The preceding characteristic-function bound makes the family tight."
    ) == 1
    reconstructed_main = main_source.replace(
        "import External.Bochner.PositiveDefinite", "import Bochner.PositiveDefinite"
    ).replace(
        "import External.Bochner.FejerPD", "import Bochner.FejerPD"
    ).replace(
        "The preceding characteristic-function bound makes the family tight.",
        "The set of measures is tight (from axiom)",
    )
    assert digest_bytes(reconstructed_main.encode()) == UPSTREAM_MAIN
    assert sha256(HERE / "External/LICENSE") == LICENSE_SHA256

    manifest = load(LEAN_ROOT / "lake-manifest.json")
    mathlib_entry = next(row for row in manifest["packages"] if row["name"] == "mathlib")
    assert mathlib_entry["rev"] == mathlib_entry["inputRev"] == MATHLIB_REVISION
    assert MATHLIB.resolve().is_dir(), "pinned mathlib artifact is unavailable"
    assert git("rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert git("remote", "get-url", "origin", cwd=MATHLIB) == MATHLIB_REMOTE
    assert git("status", "--porcelain=v1", "--untracked-files=all", cwd=MATHLIB) == ""
    for relative, (blob, source_digest) in MATHLIB_SOURCES.items():
        assert git("rev-parse", f"HEAD:{relative}", cwd=MATHLIB) == blob
        assert sha256(MATHLIB / relative) == source_digest
    assert sha256(MATHLIB / "LICENSE") == MATHLIB_LICENSE_SHA256

    lean = elan_binary("lean")
    lake = elan_binary("lake")
    lean_version = run([str(lean), "--version"], cwd=LEAN_ROOT)
    lake_version = run([str(lake), "--version"], cwd=LEAN_ROOT)
    assert "4.29.0" in lean_version and LEAN_COMMIT in lean_version
    assert "5.0.0-src+98dc76e" in lake_version
    tools = {
        "lean": lean,
        "lake": lake,
        "python": Path(os.path.realpath(sys.executable)),
        "git": Path(os.path.realpath(shutil.which("git") or "")),
        "bash": Path(os.path.realpath(shutil.which("bash") or "")),
        "bubblewrap": Path(os.path.realpath(shutil.which("bwrap") or "")),
        "elan": Path(os.path.realpath(shutil.which("elan") or "")),
    }
    expected_tools = {
        "lean": "3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf",
        "lake": "a608ff084d7e2af228b92a29d7c2fd083ba0580e46889175ec74a81678c98359",
        "python": "b8d8288faefdd300201f43fcf00f6f539a27218eeed3a3dff5ab10b9c4c99700",
        "git": "8a48eefa306b9a2a9c3e576784a74ad7485779279e5a46ec43361a1864760e45",
        "bash": "3efccc187bafa75ff1e37d246270ab3e7aa559f242c7a52bf3ec2a1b5450bdbd",
        "bubblewrap": "0abea81db798ebf6b4742ac0664802d97521547a353c2a0dbdc21d76cbbfd2c0",
        "elan": "840179e70803ef373c2ec53342d6a45ea7d022533e4145489fc1278b4f716385",
    }
    assert {name: sha256(path) for name, path in tools.items()} == expected_tools

    kernel_output = run(["bash", str(HERE / "check_validation.sh")])
    assert kernel_output.count("Declarations are sorry-free!") == len(TRUST_DECLARATIONS)
    assert "declaration uses 'sorry'" not in kernel_output
    assert "sorryAx" not in kernel_output and "error:" not in kernel_output
    for declaration in TRUST_DECLARATIONS:
        assert observed_axioms(kernel_output, declaration) == EXPECTED_AXIOMS

    assert spec["schema_version"] == "stage1-validation-recipe/1.0"
    assert spec["item_id"] == ITEM and spec["theorem_id"] == THEOREM
    assert spec["cwd"] == "."
    assert spec["argv"] == [
        "python3", "-I", "-B", f"Stage1_Instances/{THEOREM}/check_validation.py"
    ]
    assert set(spec["env_allowlist"]) == {
        "PATH", "HOME", "PYTHONPATH", "LANG", "LC_ALL", "TZ", "LEAN_NUM_THREADS"
    }
    assert spec["timeout_seconds"] == 900
    assert spec["network_policy"] == "denied" and spec["expected_exit"] == 0
    assert "--unshare-net" in spec["network_enforcement"]
    assert spec["covered_declarations"] == [
        "AwesomeTheorems.Stage1.THM_M_1021.BochnerTarget", *TRUST_DECLARATIONS
    ]
    assert spec["coverage_kind"] == "validation_subject_only_no_closure_credit"
    assert receipt["recipe"] == spec

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["phase"] == "validation" and receipt["intent"] == "validate"
    assert receipt["depends_on"] == ["S56-M-1021-PROOF"]
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["release_grade"] is receipt["content_addressed_release_evidence"] is False
    assert receipt["canonical_target"] == {
        "declaration": "AwesomeTheorems.Stage1.THM_M_1021.BochnerTarget",
        "root_declaration": "AwesomeTheorems.Stage1.THM_M_1021.bochner_exact",
        "elaborated_expression_sha256": EXPRESSION_SHA256,
        "statement_source_sha256": EXPECTED_INPUTS["BochnerStatement.lean"],
        "registry_denominator_sha256": DENOMINATOR_SHA256,
        "exact_statement_delta": "none",
    }
    assert receipt["covered_obligation_ids"] == machine_ids
    assert receipt["coverage_kind"] == "validation_subject_only_no_closure_credit"
    assert receipt["accepted_closed_obligation_ids"] == []
    assert receipt["validated_declarations"] == spec["covered_declarations"]
    for name, expected in EXPECTED_INPUTS.items():
        assert receipt["inputs"][name] == expected, name
    assert receipt["inputs"]["check_validation.py"] == sha256(HERE / "check_validation.py")
    expected_kernel_sha = hashlib.sha256(kernel_output.encode()).hexdigest()
    assert receipt["result"]["kernel_output_sha256"] == expected_kernel_sha
    assert receipt["result"]["kernel_output_bytes"] == len(kernel_output.encode())
    assert receipt["result"]["network_isolated_trust_zero_replay"] == "pass"
    assert receipt["result"]["exact_root_kernel_replay"] == "provisional_pass"
    assert receipt["result"]["observed_axioms"] == EXPECTED_AXIOM_LIST
    assert receipt["result"]["proof_master_acceptance"] == "fail_closed"
    assert receipt["result"]["frozen_graph_closed"] is False
    assert receipt["result"]["accepted_root_machine_debt"] == "M3"
    assert receipt["result"]["accepted_root_closed"] is False
    assert receipt["result"]["audit_complete"] is receipt["result"]["theorem_complete"] is False
    assert receipt["first_failed_gate"] == "dependency.S56-M-1021-PROOF.master_acceptance"
    assert receipt["first_failed_release_gate"] == "S56-10.6-HERMETIC-COLD-BUILD"
    assert receipt["trust"]["machine_reported_axioms"] == EXPECTED_AXIOM_LIST
    assert receipt["trust"]["accepted_foundation_policy"] is False
    assert receipt["trust"]["tcb_gate"] == "fail_closed"
    assert receipt["provenance"]["upstream_revision"] == UPSTREAM_REVISION
    assert receipt["provenance"]["upstream_tree"] == UPSTREAM_TREE
    assert receipt["provenance"]["complete_provenance_gate"] == "fail_closed"
    independent = receipt["independent_validation"]
    assert independent["same_worker_trust_probe"] == "pass"
    assert independent["proof_independent_exact_root_probe"] is False
    assert independent["distinct_runner"] is independent["distinct_verifier_identity"] is False
    assert independent["release_gate"] == "fail_closed"
    assert receipt["root_vector_before"] == receipt["root_vector_after_worker_selftest"] == {
        "H": "H1", "M": "M3", "R": "R3"
    }
    assert receipt["freshness"]["revocation_state"] == "not_revoked"
    assert receipt["status_boundary"].startswith("Self-tested validation-node evidence")

    assert set(packet) == {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert packet["item_id"] == ITEM and packet["state"] == "[_]"
    assert packet["base_revision"] == BASE_REVISION
    assert set(receipt["changed_paths"]) == set(packet["changed_paths"]) == CHANGED_PATHS
    assert receipt["commands"] == packet["commands"]
    assert receipt["output_summary"] == packet["output_summary"] == list(SUMMARY_LINES)
    assert receipt["known_failures"] == packet["known_failures"]
    untracked_hashes = receipt["worktree_state"]["untracked_input_sha256"]
    assert set(untracked_hashes) == CHANGED_PATHS - {
        f"Stage1_Instances/{THEOREM}/validation-receipt.json"
    }
    for relative, expected in untracked_hashes.items():
        assert sha256(ROOT / relative) == expected, relative
    link_target = os.readlink(LEAN_ROOT / ".lake").encode()
    assert hashlib.sha256(link_target).hexdigest() == receipt["worktree_state"][
        "preexisting_untracked_link_target_sha256"
    ]

    status = git(
        "status", "--porcelain=v1", "--untracked-files=all", "--",
        str(HERE), str(ROOT / ".stage1-worker-selftest.json"),
    )
    actual_changed = {
        line[3:] if line[:2] == "??" else line[2:].lstrip()
        for line in status.splitlines()
    }
    assert actual_changed == CHANGED_PATHS, (actual_changed, CHANGED_PATHS)
    for relative in CHANGED_PATHS:
        assert_text_hygiene(ROOT / relative)
    for path in (HERE / "validation-receipt.json", HERE / "validation-phase.md"):
        text = path.read_text(encoding="utf-8")
        assert "/home/" not in text and ".cron/" not in text
        assert "theorem_complete=true" not in text

    print("\n".join(SUMMARY_LINES))


if __name__ == "__main__":
    main()
