#!/usr/bin/env python3
"""Validate the immutable THM-M-0043 anchor inventory and narrow Lean checks."""

from pathlib import Path
import hashlib
import json
import re
import subprocess
import sys
import tempfile
import urllib.request


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
THEOREM_ID = "THM-M-0043"
ITEM_ID = "S56-M-0043-ANCHOR_AUDIT"
BASE_REVISION = "72f928bdf1a47d7c119826db45575bd02a3a63ce"
BASE_TREE = "171a6bfae88220f5df9b39cdd6c7e1bf17639889"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
EXPRESSION_SHA256 = "a46ee23911b8027aa5de93149fd781def441429e386cb9181fc2064b2898557a"
STATEMENT_SHA256 = "d2e524169f6c8a4e8d11b5c33eb3c218a62531966953150b3ec77b9a0f9e0d9c"
ANCHOR_LEAN_SHA256 = "b75caf959f70c8c25724382009622c17abeddd3e31f71390fea92f2747c28cc9"
ATLAS_REVISION = "34ffed396f376454c1a9b297f3fd74c5c801fb50"
ATLAS_SOURCE_SHA256 = "415d4e7784f21d5cf7327a4c6bee96bb3e3ac3e2d7ae18587738785a18b72cc9"
ATLAS_URLS = [
    "https://ghproxy.net/https://raw.githubusercontent.com/facebookresearch/atlas-lean/"
    f"{ATLAS_REVISION}/Atlas/AlgebraNotes/code/SpectralTheorem.lean",
    "https://raw.githubusercontent.com/facebookresearch/atlas-lean/"
    f"{ATLAS_REVISION}/Atlas/AlgebraNotes/code/SpectralTheorem.lean",
]
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM_ID}/AnchorAudit.lean",
    f"Stage1_Instances/{THEOREM_ID}/anchor-audit-receipt.json",
    f"Stage1_Instances/{THEOREM_ID}/anchor-audit-validation.md",
    f"Stage1_Instances/{THEOREM_ID}/anchor-audit.json",
    f"Stage1_Instances/{THEOREM_ID}/check_anchor_audit.py",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def output(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(args, cwd=cwd, text=True).strip()


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise SystemExit(f"{path} must contain a JSON object")
    return value


def without_comments(source: str) -> str:
    source = re.sub(r"/-.*?-/", "", source, flags=re.DOTALL)
    return re.sub(r"--.*", "", source)


def run_lean(source: Path) -> str:
    result = subprocess.run(
        ["lake", "env", "lean", str(source)],
        cwd=LEAN_ROOT,
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


def atlas_source() -> bytes:
    errors = []
    for url in ATLAS_URLS:
        try:
            request = urllib.request.Request(url, headers={"User-Agent": "stage1-anchor-audit/1.0"})
            with urllib.request.urlopen(request, timeout=20) as response:
                data = response.read()
            if hashlib.sha256(data).hexdigest() != ATLAS_SOURCE_SHA256:
                raise RuntimeError("immutable Atlas source hash mismatch")
            return data
        except Exception as error:  # The second immutable URL is an availability fallback.
            errors.append(f"{url}: {error}")
    raise SystemExit("could not replay immutable Atlas source: " + "; ".join(errors))


def main() -> None:
    audit = load(HERE / "anchor-audit.json")
    receipt = load(HERE / "anchor-audit-receipt.json")
    statement = load(HERE / "statement.json")
    manifest = load(ROOT / "Docs" / "Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")
    packet_path = ROOT / ".stage1-worker-selftest.json"
    packet = load(packet_path) if packet_path.exists() else None

    assert audit["schema_version"] == "stage1-anchor-audit/1.0"
    assert audit["item_id"] == ITEM_ID and audit["theorem_id"] == THEOREM_ID
    assert audit["execution_rank"] == 1083
    assert len(audit["candidates"]) == 9
    assert audit["base_revision"] == BASE_REVISION and audit["base_tree"] == BASE_TREE
    assert output("git", "rev-parse", "HEAD") == BASE_REVISION
    assert output("git", "rev-parse", "HEAD^{tree}") == BASE_TREE
    assert receipt["item_id"] == ITEM_ID and receipt["theorem_id"] == THEOREM_ID
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert set(receipt["changed_paths"]) == CHANGED_PATHS
    assert receipt["candidate_result"]["classification"] == "M1"
    assert receipt["candidate_result"]["evidence_level"] == "E2"
    assert receipt["candidate_result"]["master_accepted"] is False
    assert receipt["lean_output_sha256"] == "8ddeb861a2c3f9087b61cfbb56a43b86dc48b815a48bc90b711cf6cd4a301308"
    assert receipt["atlas_axiom_output_sha256"] == "65afdbd2c1fff7b271a399fa2208204ff7344ab2fd9aed530f224df215dc5565"
    assert receipt["audit_complete"] is False and receipt["theorem_complete"] is False
    if packet is not None:
        assert packet["item_id"] == ITEM_ID and packet["state"] == "[_]"
        assert packet["base_revision"] == BASE_REVISION
        assert set(packet["changed_paths"]) == CHANGED_PATHS
        assert packet["known_failures"] == receipt["known_failures"]

    target = next(row for row in manifest["targets"] if row["theorem_id"] == THEOREM_ID)
    assert target["execution_rank"] == 1083
    assert target["baseline"] == "L0" and target["rework_required"] is True
    assert target["theorem_complete"] is False
    item = next(row for row in execution["items"] if row["id"] == ITEM_ID)
    assert item["phase"] == "anchor_audit" and item["layer"] == 2
    assert item["state"] == "[ ]"
    assert item["depends_on"] == ["S56-M-0043-STATEMENT"]
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]

    assert audit["canonical_target_expression_sha256"] == EXPRESSION_SHA256
    assert audit["canonical_statement_file_sha256"] == STATEMENT_SHA256
    assert sha256(HERE / "Statement.lean") == STATEMENT_SHA256
    formal = statement["canonical_formal_target"]
    assert formal["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert formal["statement_file_sha256"] == STATEMENT_SHA256

    env = audit["immutable_environment"]
    assert env["mathlib_revision"] == MATHLIB_REVISION and env["mathlib_tree"] == MATHLIB_TREE
    assert output("git", "rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert output("git", "rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert output("git", "status", "--porcelain=v1", "--untracked-files=no", cwd=MATHLIB) == ""
    assert sha256(MATHLIB / "LICENSE") == env["mathlib_license_sha256"]
    assert sha256(LEAN_ROOT / "lake-manifest.json") == env["manifest_sha256"]

    atlas = next(c for c in audit["candidates"] if c["candidate_id"] == "M0043-C01-ATLAS-EXACT")
    assert atlas["revision"] == ATLAS_REVISION
    assert atlas["file_sha256"] == ATLAS_SOURCE_SHA256
    assert atlas["candidate_classification"] == "M1" and atlas["evidence_level"] == "E2"
    assert atlas["mathlib_revision"] == MATHLIB_REVISION
    atlas_data = atlas_source()
    atlas_text = atlas_data.decode("utf-8")
    for marker in (
        "theorem normal_complex_unitarily_diagonalizable",
        "(M : Matrix n n ℂ) (hM : IsStarNormal M)",
        "have hdecomp := hTh_sym.directSum_isInternal_of_commute hTk_sym hcomm",
        "hdecomp'.subordinateOrthonormalBasis",
        "toMatrix_orthonormalBasis_mem_unitary",
        "calc star P * M * P",
    ):
        assert marker in atlas_text, marker
    forbidden = re.compile(r"\b(?:sorry|admit|sorryAx|axiom|unsafe|opaque)\b")
    assert not forbidden.search(without_comments(atlas_text))

    with tempfile.NamedTemporaryFile("wb", suffix=".lean", dir=HERE, delete=False) as handle:
        handle.write(atlas_data)
        handle.write(b"\n#print axioms SpectralTheorem.normal_complex_unitarily_diagonalizable\n")
        atlas_probe = Path(handle.name)
    try:
        atlas_output = run_lean(atlas_probe)
    finally:
        atlas_probe.unlink()
    assert hashlib.sha256(atlas_output.encode()).hexdigest() == receipt["atlas_axiom_output_sha256"]
    assert atlas_output.strip().endswith(
        "depends on axioms: [propext, Classical.choice, Quot.sound]"
    )

    hermitian = next(c for c in audit["candidates"] if c["candidate_id"] == "M0043-C02-MATHLIB-HERMITIAN")
    hermitian_source = MATHLIB / hermitian["file"]
    assert output("git", "rev-parse", f"HEAD:{hermitian['file']}", cwd=MATHLIB) == hermitian["file_blob"]
    assert sha256(hermitian_source) == hermitian["file_sha256"]
    source_text = hermitian_source.read_text(encoding="utf-8")
    for marker in (
        "theorem spectral_theorem :",
        "A = conjStarAlgAut",
        "rw [← conjStarAlgAut_star_eigenvectorUnitary",
    ):
        assert marker in source_text, marker

    legacy = next(c for c in audit["candidates"] if c["candidate_id"] == "M0043-C04-REPOSITORY-LEGACY-HERMITIAN")
    assert output("git", "rev-parse", f"HEAD:{legacy['file']}") == legacy["file_blob"]
    assert sha256(ROOT / legacy["file"]) == legacy["file_sha256"]

    adapter_path = HERE / "AnchorAudit.lean"
    assert sha256(adapter_path) == ANCHOR_LEAN_SHA256
    adapter = adapter_path.read_text(encoding="utf-8")
    for marker in (
        "def AtlasCandidateTarget : Prop",
        "theorem exactTarget_from_atlasCandidate",
        "theorem hermitianSpecialization_from_mathlib",
        "theorem normal_not_implies_hermitian",
        "#print axioms exactTarget_from_atlasCandidate",
    ):
        assert marker in adapter, marker
    assert not forbidden.search(without_comments(adapter))
    lean_output = run_lean(adapter_path)
    assert hashlib.sha256(lean_output.encode()).hexdigest() == receipt["lean_output_sha256"]
    normalized = re.sub(r"\s+", " ", lean_output)
    if normalized.count("propext, Classical.choice, Quot.sound") != 4:
        sys.stdout.write(lean_output)
        raise SystemExit("unexpected local anchor axiom report")
    assert "sorryAx" not in lean_output

    result = audit["audit_result"]
    assert result["inventory_classified"] is True
    assert result["source_boundary_coverage"].startswith("9/9 classified candidate groups")
    assert result["exact_candidate_located"] is True
    assert result["candidate_kernel_checked"] is True
    assert result["candidate_accepted_by_master"] is False
    assert result["root_machine_debt_before"] == "M3"
    assert result["root_machine_candidate_after"] == "M1"
    assert result["accepted_root_machine_debt_after"] == "M3"
    assert result["root_evidence_level"] == "E2"
    assert result["audit_complete"] is False and result["theorem_complete"] is False
    assert audit["discovery_protocol"]["saturation_claim"] is False

    for relative in CHANGED_PATHS:
        path = ROOT / relative
        data = path.read_bytes()
        assert data.endswith(b"\n"), f"missing final newline: {relative}"
        assert b"\r" not in data and b"\x00" not in data, f"invalid bytes: {relative}"
        assert all(
            not line.endswith((b" ", b"\t")) for line in data.splitlines()
        ), f"trailing whitespace: {relative}"

    print(
        "check_anchor_audit: ok "
        "(THM-M-0043; 9/9 candidate groups; exact Atlas route M1/E2; "
        "accepted root M3; audit_complete=false; theorem_complete=false)"
    )


if __name__ == "__main__":
    main()
