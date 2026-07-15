#!/usr/bin/env python3
"""Fail-closed narrow validator for S56-M-0996-VALIDATION."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import platform
import re
import shutil
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0996"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"

ITEM = "S56-M-0996-VALIDATION"
THEOREM = "THM-M-0996"
BASE_REVISION = "443b8bbc23bf35a1e7a4bb7b3183073f76bbee2b"
BASE_TREE = "c5771c47c12b80aba613e6d844570f83b39ded6d"
STATEMENT_SHA256 = "cdecb06daf3ca5cbc2b6f8f5def0a82fb3fc712695fdd5c2a047189d683edd14"
DENOMINATOR_SHA256 = "8d3affee638ef1cc6e3fbb2ee9d52fc76212b0a91327f7b42ecba1b4ae8b6e9e"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MATHLIB_REMOTE = "https://github.com/leanprover-community/mathlib4.git"
MATHLIB_LICENSE_SHA256 = "b40930bbcf80744c86c46a12bc9da056641d722716c378f5659b9e555ef833e1"
FLT_REGULAR_REVISION = "56161b6eb5281fbfe9c38f2bcec0f429ebc11a27"
LEAN_TOOLCHAIN_SHA256 = "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2"
LAKE_MANIFEST_SHA256 = "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81"
LEAN_EXECUTABLE_SHA256 = "3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf"
BWRAP_SHA256 = "0abea81db798ebf6b4742ac0664802d97521547a353c2a0dbdc21d76cbbfd2c0"
LEAN_BIN = Path.home() / ".elan/toolchains/leanprover--lean4---v4.29.0/bin/lean"

LEAN_MODULES = (
    "Statement.lean",
    "ObligationTree.lean",
    "Proof.lean",
    "AnchorAudit.lean",
    "Validation.lean",
)
EXPECTED_INPUTS = {
    "Statement.lean": "cdecb06daf3ca5cbc2b6f8f5def0a82fb3fc712695fdd5c2a047189d683edd14",
    "ObligationTree.lean": "017fd72aaf20e6b2e72077f53c2ea4a467f80d2ea7353529327898f3d8649118",
    "Proof.lean": "f700eaa0401497c645131614d333da45b4a95e5ca9f9e5ef9712edef5c918202",
    "AnchorAudit.lean": "2191c6dfbf4008a7a915a20eb50b1a47bf6d9a219201391af2301d63ed958316",
    "Validation.lean": "79311d28aa5db3305aae2dec9f327f4be988643a964f82d074a5c982de174d53",
    "instance.json": "69f7f955f60c464a198b9c4f80dacd58cb7e294934c90a28da1b056dbc77d48f",
    "statement.json": "bca25f50f58fa2d386905a6520ed390367dac4a029175d0eb66899b1ffe790f7",
    "anchor-audit.json": "37a8f757f327d13d6be0b260b2c70c53cddf30bca7ffd1e21bbb63cba8d282e5",
    "obligation-registry.json": "756adee275abf1d881e9227a3c2019bf4734f96cdc8e5ab5729896cb9c696711",
    "typed-graphs.json": "582265d4259e4dee4e963a4703f3e130ea43424a9168d46fa9987bc43414b06e",
    "proof-receipt.json": "dabbfe02983961d78ed336a9c7655da185871354f79229c1d39229d1f7acbf18",
    "proof-blocker.json": "b214268cbd29cc86aa925c79de4f23427cc574c091cd2939c9b02e478478ddb5",
    "source-statement-crosswalk.md": "7b5f2b9d453b5ebdfec37c9140d32211d810aabc6a9c41b4247fc1b4a0bb0a60",
    "check_obligation_tree.py": "df4593a73890507d88937c42585adce365b7e7e198699a2f2d42c09ca4dc1d65",
}

PINNED_TERMINALS = {
    "Mathlib/Probability/Distributions/Gaussian/Multivariate.lean": {
        "source_sha256": "fb527496c0753fc71e30e26beaf238910ab550bfa4a0cca1219daec608a42370",
        "git_blob": "067057aa442d4d769f1d24c4a52c0578261c8448",
        "olean_sha256": "52f3001d36485d6bc180d832d150e4bddf9286fde39cb2f140ce5862cdd7fc36",
    },
    "Mathlib/Probability/CDF.lean": {
        "source_sha256": "e3a692cef06a8ce6f76419e742b16d642d94f0b286a19c95dada354dd60d42bd",
        "git_blob": "6dce803e028ebbd6199f994a3071c6286de3b41b",
        "olean_sha256": "cacf78e4ccddb13bc16b9481799be092001a7a836e213584d8d126696fa0ca96",
    },
    "Mathlib/Topology/MetricSpace/Thickening.lean": {
        "source_sha256": "3f5708cad3ad2e652465c753d34b126eb3837d7d1126f2b505415c7c42feeb15",
        "git_blob": "2eb11946022bab6d407d95e6e56e97f16f112eab",
        "olean_sha256": "b1bc534fb6d5eba66093fa0a8ee5ed57896eaeb887bd0a868dcf36e1896be0ba",
    },
}

PROOF_DECLARATIONS = (
    "measurableSet_of_isUnitHalfspace",
    "coordEquiv",
    "coordEquiv_map_stdGaussian",
    "coordEquiv_preimage_stdGaussian",
    "coordEquiv_image_stdGaussian",
    "coordEquiv_image_thickening",
    "coordEquiv_preimage_thickening",
    "coordEquiv_thickening_measure",
    "coordEquiv_comp_norm",
    "coordEquiv_image_isUnitHalfspace",
    "stdGaussian_unitHalfspace_measure",
    "norm_sub_apply_le_of_isUnitNormal",
    "thickening_unitHalfspace_subset",
    "shifted_unitHalfspace_subset_thickening",
    "thickening_unitHalfspace_eq",
    "stdGaussian_unitHalfspace_thickening_measure",
    "stdGaussianReal_Ioc_pos",
    "strictMono_stdGaussianReal_Iic",
    "stdGaussianReal_Iic_pos",
    "stdGaussianReal_Iic_lt_one",
    "continuous_stdGaussianReal_cdf",
    "continuous_stdGaussianReal_Iic",
    "stdGaussianReal_Iic_surjective_Ioo",
    "stdGaussianReal_Iic_range",
    "halfspaceProfile",
    "halfspaceProfile_stdGaussianReal_Iic",
    "halfspaceEnlargementFormula",
    "unitHalfspace_profile_formula",
    "coordEquiv_unitHalfspace_profile_formula",
    "no_unitHalfspace_of_finrank_zero",
    "finrank_pos_of_unitHalfspace",
    "target_of_finrank_zero",
    "target_of_generalSetEnlargementBound",
    "target_of_positive_finrank_branch",
)
AXIOM_DECLARATIONS = {
    "ObligationTree.lean": ("target_of_profile_bounds",),
    "Proof.lean": PROOF_DECLARATIONS,
    "Validation.lean": (
        "measurableSet_of_isUnitHalfspace_direct",
        "conditionalTargetDirect",
    ),
}
AUTHORITATIVE_CUT = ["M0996-L-HALFSPACE", "M0996-L-GENERAL"]
SUPPORTED_IDS = [
    "M0996-N-PROFILE",
    "M0996-N-COORD",
    "M0996-B-DIM",
    "M0996-C-HALFSPACE",
    "M0996-L-HALFSPACE",
    "M0996-T-ASSEMBLE",
]
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/Validation.lean",
    f"Stage1_Instances/{THEOREM}/check_validation.py",
    f"Stage1_Instances/{THEOREM}/validation-phase.md",
    f"Stage1_Instances/{THEOREM}/validation-receipt.json",
    f"Stage1_Instances/{THEOREM}/validation-spec.json",
}
SUMMARY_LINES = (
    "PASS network-isolated trust-zero fresh replay: statement, conditional composition, 34 partial proof declarations, and two validation probes elaborated",
    "PASS observed axioms: exactly propext, Classical.choice, and Quot.sound; validation probes are sorry-free and no output contains sorryAx",
    "PASS frozen hashes, open-root graph boundary, clean mathlib pin, selected direct source/blob/olean provenance, and owned-source hygiene",
    "FAIL CLOSED exact root and authority: no accepted frozen premise-free GeneralSetEnlargementBound body is recorded, no frozen obligation closes, and the proof predecessor lacks master acceptance",
    "FAIL CLOSED complete trust/provenance and cold hermetic replay: the dependency cache is shared and warm, Lake replay is unavailable, and no accepted complete TCB or offline-restorable closure exists",
    "FAIL CLOSED independent verification: same-workspace probes are not a second signed clean runner or independently implemented release verifier",
)


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


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode()).hexdigest()


def run(
    argv: list[str],
    *,
    cwd: Path = ROOT,
    env: dict[str, str] | None = None,
    timeout: int = 600,
) -> str:
    result = subprocess.run(
        argv,
        cwd=cwd,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=timeout,
        check=False,
    )
    assert result.returncode == 0, (argv, result.returncode, result.stdout)
    return result.stdout.strip()


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["git", *args], cwd=cwd, timeout=60)


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


def printed_axioms(output: str, declaration: str) -> set[str]:
    match = re.search(
        rf"'[^']*{re.escape(declaration)}' depends on axioms:\s*\[(.*?)\]",
        output,
        flags=re.DOTALL,
    )
    assert match is not None, (declaration, output)
    return {
        part.strip()
        for part in match.group(1).replace("\n", "").split(",")
        if part.strip()
    }


def assert_text_hygiene(path: Path) -> None:
    data = path.read_bytes()
    assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines()), path


def explicit_lean_path(tmp: Path) -> str:
    paths = [tmp]
    package_order = (
        "Cli",
        "batteries",
        "Qq",
        "aesop",
        "proofwidgets",
        "importGraph",
        "LeanSearchClient",
        "plausible",
        "checkdecls",
        "mathlib",
        "flt-regular",
    )
    for package in package_order:
        paths.append(LEAN_ROOT / ".lake" / "packages" / package / ".lake" / "build" / "lib" / "lean")
    paths.extend(
        (
            LEAN_ROOT / ".lake" / "build" / "lib" / "lean",
            LEAN_BIN.parent.parent / "lib" / "lean",
        )
    )
    return ":".join(str(path) for path in paths)


def main() -> None:
    spec = load(HERE / "validation-spec.json")
    receipt = load(HERE / "validation-receipt.json")
    packet_path = ROOT / ".stage1-worker-selftest.json"
    packet = load(packet_path) if packet_path.exists() else None
    instance = load(HERE / "instance.json")
    statement = load(HERE / "statement.json")
    anchor = load(HERE / "anchor-audit.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    proof_receipt = load(HERE / "proof-receipt.json")
    proof_blocker = load(HERE / "proof-blocker.json")

    run(["git", "merge-base", "--is-ancestor", BASE_REVISION, "HEAD"], timeout=60)
    assert git("rev-parse", f"{BASE_REVISION}^{{tree}}") == BASE_TREE

    targets = load(ROOT / "Docs" / "Stage1_Targets_rev-5.6.json")
    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 276 and target["baseline"] == "L0"
    assert target["lifecycle_mode"] == "planned"
    assert target["rework_required"] is True and target["theorem_complete"] is False

    execution = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item["theorem_id"] == THEOREM and item["execution_rank"] == 276
    assert item["phase"] == "validation" and item["layer"] == 5
    assert item["state"] in {"[ ]", "[_]"}
    assert item["depends_on"] == ["S56-M-0996-PROOF"]
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM}"]
    assert item["deliverable"] == (
        "Run hermetic kernel, trust, provenance, and independent validation gates."
    )
    assert item["completion_gate"] == "rev-5.6 node-specific receipt and master acceptance"
    predecessor = next(row for row in execution["items"] if row["id"] == "S56-M-0996-PROOF")
    assert predecessor["state"] in {"[_]", "[x]"}

    for name, expected in EXPECTED_INPUTS.items():
        assert sha256(HERE / name) == expected, f"stale validation input: {name}"
    assert sha256(LEAN_ROOT / "lean-toolchain") == LEAN_TOOLCHAIN_SHA256
    assert sha256(LEAN_ROOT / "lake-manifest.json") == LAKE_MANIFEST_SHA256
    assert statement["declaration"] == "Stage1Instances.THM_M_0996.GaussianIsoperimetricTarget"
    assert statement["statement_sha256"] == STATEMENT_SHA256
    assert instance["lifecycle"] == "planned" and instance["theorem_complete"] is False
    assert instance["root_vector"] == {"H": "H2", "M": "M4", "R": "R4"}
    assert registry["root_obligation_id"] == graphs["root_node_id"] == "M0996-ROOT"
    assert registry["denominator_sha256"] == graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert registry["status_observed_after_freeze"] == {
        "closed_obligations": [],
        "conditionally_checked_compositions": ["M0996-T-ASSEMBLE"],
        "root_machine_debt": "M3",
    }
    assert graphs["remaining_root_cut_set"] == AUTHORITATIVE_CUT
    assert graphs["theorem_complete"] is False
    assert all(row["evidence_ids"] == [] for row in graphs["nodes"])
    by_id = {row["obligation_id"]: row for row in registry["obligations"]}
    assert all(by_id[oid]["statement_fingerprint"].startswith("planned:v1:sha256:") for oid in SUPPORTED_IDS)
    assert all(by_id[oid]["terminal_proof_body_id"] is None for oid in SUPPORTED_IDS if oid != "M0996-T-ASSEMBLE")
    assert by_id["M0996-T-ASSEMBLE"]["terminal_proof_body_id"] == (
        "local:Stage1Instances.THM_M_0996.target_of_profile_bounds"
    )

    assert proof_receipt["support_state"] == "provisional_worker_selftest"
    assert proof_receipt["proposed_state"] == "[_]" and proof_receipt["accepted"] is False
    assert proof_receipt["provisionally_closed_obligation_ids"] == []
    assert proof_receipt["accepted_closed_obligation_ids"] == []
    assert proof_receipt["result"]["root_kernel_closed"] is False
    assert proof_receipt["result"]["theorem_complete"] is False
    assert proof_receipt["authoritative_graph_open_cut_set_unchanged"] == AUTHORITATIVE_CUT
    assert proof_blocker["root_closed"] is False and proof_blocker["theorem_complete"] is False
    assert proof_blocker["authoritative_graph_open_cut_set_unchanged"] == AUTHORITATIVE_CUT
    assert anchor["exact_root_candidate"] is None and anchor["audit_complete"] is False

    manifest = load(LEAN_ROOT / "lake-manifest.json")
    mathlib_pin = next(row for row in manifest["packages"] if row["name"] == "mathlib")
    flt_pin = next(row for row in manifest["packages"] if "flt-regular" in row["name"])
    assert mathlib_pin["rev"] == mathlib_pin["inputRev"] == MATHLIB_REVISION
    assert flt_pin["rev"] == flt_pin["inputRev"] == FLT_REGULAR_REVISION
    assert MATHLIB.resolve().is_dir()
    assert git("rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert git("status", "--porcelain=v1", "--untracked-files=all", cwd=MATHLIB) == ""
    assert git("remote", "get-url", "origin", cwd=MATHLIB) == MATHLIB_REMOTE
    assert sha256(MATHLIB / "LICENSE") == MATHLIB_LICENSE_SHA256
    olean_root = MATHLIB / ".lake" / "build" / "lib" / "lean"
    for relative, expected in PINNED_TERMINALS.items():
        source = MATHLIB / relative
        olean = olean_root / relative.replace(".lean", ".olean")
        assert sha256(source) == expected["source_sha256"]
        assert git("rev-parse", f"HEAD:{relative}", cwd=MATHLIB) == expected["git_blob"]
        assert sha256(olean) == expected["olean_sha256"]

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|implemented_by|native_decide|run_tac)\b|"
        r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
        r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
        r"(?:axiom|constant|opaque|unsafe)\b|\bextern[ \t]+",
        flags=re.MULTILINE,
    )
    for name in LEAN_MODULES:
        source = source_without_comments((HERE / name).read_text(encoding="utf-8"))
        source = source.replace("#print sorries", "")
        assert prohibited.search(source) is None, f"prohibited proof construct in {name}"
    validation_source = source_without_comments((HERE / "Validation.lean").read_text(encoding="utf-8"))
    assert "import Proof" not in validation_source
    assert "import «Stage1_Instances».«THM-M-0996».Proof" not in validation_source
    assert "theorem measurableSet_of_isUnitHalfspace_direct" in validation_source
    assert "theorem conditionalTargetDirect" in validation_source
    assert "hGeneral" in validation_source

    assert LEAN_BIN.is_file() and sha256(LEAN_BIN) == LEAN_EXECUTABLE_SHA256
    assert "Lean (version 4.29.0" in run([str(LEAN_BIN), "--version"], timeout=30)
    bwrap_name = shutil.which("bwrap")
    assert bwrap_name is not None, "bubblewrap is required to enforce network denial"
    bwrap = Path(bwrap_name).resolve()
    assert sha256(bwrap) == BWRAP_SHA256

    outputs: dict[str, str] = {}
    replay_hashes: dict[str, str] = {}
    with tempfile.TemporaryDirectory(prefix="m0996-validation-", dir="/tmp") as tmp_name:
        tmp = Path(tmp_name).resolve()
        module_dir = tmp / "Stage1_Instances" / "THM-M-0996"
        module_dir.mkdir(parents=True)
        for name in LEAN_MODULES:
            shutil.copy2(HERE / name, module_dir / name)
        lean_path = explicit_lean_path(tmp)
        base = [
            str(bwrap),
            "--ro-bind", "/", "/",
            "--bind", str(tmp), str(tmp),
            "--dev", "/dev",
            "--proc", "/proc",
            "--unshare-net",
            "--die-with-parent",
            "--clearenv",
            "--setenv", "HOME", str(tmp),
            "--setenv", "LANG", "C.UTF-8",
            "--setenv", "LC_ALL", "C.UTF-8",
            "--setenv", "TZ", "UTC",
            "--setenv", "LEAN_NUM_THREADS", "1",
            "--setenv", "LEAN_PATH", lean_path,
            "--chdir", str(tmp),
            str(LEAN_BIN), "--trust=0", "-t0", "-R", str(tmp),
        ]

        for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
            source = module_dir / name
            olean = module_dir / name.replace(".lean", ".olean")
            outputs[name] = run(base + ["-o", str(olean), str(source)], timeout=600)
            stem = name.removesuffix(".lean").lower()
            replay_hashes[f"{stem}_output_sha256"] = sha256_text(outputs[name])
            replay_hashes[f"{stem}_olean_sha256"] = sha256(olean)
        outputs["AnchorAudit.lean"] = run(
            base + [str(module_dir / "AnchorAudit.lean")], timeout=300
        )
        replay_hashes["anchor_audit_output_sha256"] = sha256_text(outputs["AnchorAudit.lean"])

    allowed_axioms = {"propext", "Classical.choice", "Quot.sound"}
    for name, declarations in AXIOM_DECLARATIONS.items():
        for declaration in declarations:
            assert printed_axioms(outputs[name], declaration) == allowed_axioms
    assert outputs["Validation.lean"].count("Declarations are sorry-free!") == 2
    all_output = "\n".join(outputs.values())
    assert "sorryAx" not in all_output and "declaration uses 'sorry'" not in all_output
    assert "error:" not in all_output
    for marker in (
        "GaussianIsoperimetricTarget",
        "ProbabilityTheory.stdGaussian",
        "Metric.isOpen_thickening",
    ):
        assert marker in all_output

    assert spec["schema_version"] == "stage1-validation-spec/1.0"
    assert spec["item_id"] == ITEM and spec["theorem_id"] == THEOREM
    assert spec["cwd"] == "." and spec["argv"] == [
        "python3", "-I", "-B", f"Stage1_Instances/{THEOREM}/check_validation.py"
    ]
    assert spec["network_policy"] == "denied" and spec["expected_exit"] == 0
    assert len(spec["covered_obligation_ids"]) == len(set(spec["covered_obligation_ids"]))
    assert len(spec["covered_declarations"]) == len(set(spec["covered_declarations"]))
    assert set(spec["covered_obligation_ids"]) == set(registry["frozen_denominators"]["inventory"])

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["phase"] == "validation" and receipt["intent"] == "validate"
    assert receipt["verdict"] == "blocked"
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["release_grade"] is receipt["content_addressed_release_evidence"] is False
    assert receipt["canonical_target"]["statement_source_sha256"] == STATEMENT_SHA256
    assert receipt["canonical_target"]["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert receipt["inputs"]["validation-spec.json"] == sha256(HERE / "validation-spec.json")
    assert receipt["inputs"]["validation_verifier_sha256"] == sha256(Path(__file__).resolve())
    assert receipt["output_evidence"]["replay_hashes"] == replay_hashes
    assert receipt["result"]["root_kernel_closed"] is False
    assert receipt["result"]["provisionally_closed_obligation_ids"] == []
    assert receipt["result"]["accepted_closed_obligation_ids"] == []
    assert receipt["result"]["complete_transitive_trust_and_provenance"] == "fail_closed"
    assert receipt["result"]["hermetic_release_gate"] == "fail_closed"
    assert receipt["result"]["independent_release_verification_gate"] == "fail_closed"
    assert receipt["result"]["audit_complete"] is receipt["result"]["theorem_complete"] is False
    assert receipt["remaining_root_cut_set"] == AUTHORITATIVE_CUT
    assert receipt["first_failed_gate"] == "dependency.S56-M-0996-PROOF.master_acceptance"
    assert receipt["authoritative_root_vector_before"] == instance["root_vector"]
    assert receipt["authoritative_root_vector_after_worker_selftest"] == instance["root_vector"]
    assert receipt["provisional_evidence_root_vector_after_worker_selftest"] == {
        "H": "H2", "M": "M3", "R": "R4"
    }

    if packet is not None:
        assert set(packet) == {
            "item_id", "changed_paths", "commands", "output_summary",
            "base_revision", "known_failures", "state",
        }
        assert packet["item_id"] == ITEM and packet["state"] == "[_]"
        assert packet["base_revision"] == BASE_REVISION
        assert set(packet["changed_paths"]) == set(receipt["changed_paths"]) == CHANGED_PATHS
        assert packet["commands"] == receipt["commands"]
        assert packet["output_summary"] == receipt["output_summary"]
        assert packet["known_failures"] == receipt["known_failures"]
        status = git("status", "--short", "--untracked-files=all")
        actual_changes = {
            line[3:] for line in status.splitlines()
            if line[3:] != "Formalizations/Lean/.lake"
        }
        assert actual_changes == CHANGED_PATHS, (actual_changes, CHANGED_PATHS)
        manifest = receipt["repository_state"]["untracked_validation_input_manifest"]
        for row in manifest:
            path = ROOT / row["path"]
            if row["kind"] == "file":
                assert path.stat().st_size == row["size"], path
                assert sha256(path) == row["sha256"], path
            else:
                assert row["kind"] == "symlink" and path.is_symlink(), path
                assert sha256_text(str(path.readlink()) + "\n") == row["target_sha256"], path
        for path in [ROOT / relative for relative in CHANGED_PATHS]:
            assert_text_hygiene(path)

    assert platform.system() == "Linux" and platform.machine() == "x86_64"
    for line in SUMMARY_LINES:
        print(line)
    print("REPLAY_HASHES=" + json.dumps(replay_hashes, sort_keys=True, separators=(",", ":")))
    print("audit_complete=false; theorem_complete=false")


if __name__ == "__main__":
    main()
