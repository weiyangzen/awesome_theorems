#!/usr/bin/env python3
"""Validate the immutable THM-M-0044 formal-anchor inventory."""

from __future__ import annotations

import hashlib
import io
import json
from pathlib import Path
import re
import subprocess
import sys
import tarfile
import urllib.request


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
PACKAGES = LEAN_ROOT / ".lake" / "packages"
MATHLIB = PACKAGES / "mathlib"
ITEM_ID = "S56-M-0044-ANCHOR_AUDIT"
THEOREM_ID = "THM-M-0044"
BASE_REVISION = "72f928bdf1a47d7c119826db45575bd02a3a63ce"
BASE_TREE = "171a6bfae88220f5df9b39cdd6c7e1bf17639889"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
EXPRESSION_SHA256 = "f9a0f27af3e6287fc303bfbd9ecf382111bd44ed8d60e27cff6d0acc59b1052b"
STATEMENT_SHA256 = "29f45600f5bc00edbd42756c7dd70c8599cdf2f04f07a570eb9f4e9b3d30141c"
LEAN_OUTPUT_SHA256 = "1b0e9a5fd645b5cdbec4adc6982c14521f1808d039f1b35caf89f38e576b245b"
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM_ID}/AnchorAudit.lean",
    f"Stage1_Instances/{THEOREM_ID}/README.md",
    f"Stage1_Instances/{THEOREM_ID}/anchor-audit-receipt.json",
    f"Stage1_Instances/{THEOREM_ID}/anchor-audit-validation.md",
    f"Stage1_Instances/{THEOREM_ID}/anchor-audit.json",
    f"Stage1_Instances/{THEOREM_ID}/check_anchor_audit.py",
    f"Stage1_Instances/{THEOREM_ID}/check_intake.py",
    f"Stage1_Instances/{THEOREM_ID}/instance.json",
    f"Stage1_Instances/{THEOREM_ID}/source-statement-crosswalk.md",
}


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


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


def archive_bytes(candidate: dict) -> bytes:
    cache = Path("/tmp") / (
        "thm-m-0044-atlas-34ffe.tar.gz"
        if candidate["candidate_id"].startswith("M0044-C02")
        else "thm-m-0044-gaussian-field-d63a.tar.gz"
    )
    if cache.is_file() and sha256(cache) == candidate["archive_sha256"]:
        return cache.read_bytes()
    request = urllib.request.Request(
        candidate["archive_url"], headers={"User-Agent": "stage1-rev56-anchor-audit"}
    )
    with urllib.request.urlopen(request, timeout=90) as response:
        payload = response.read()
    if sha256_bytes(payload) != candidate["archive_sha256"]:
        raise SystemExit(f"immutable archive changed: {candidate['project']}")
    return payload


def archive_member(payload: bytes, suffix: str) -> bytes:
    with tarfile.open(fileobj=io.BytesIO(payload), mode="r:gz") as archive:
        matches = [member for member in archive.getmembers() if member.name.endswith(suffix)]
        if len(matches) != 1:
            raise SystemExit(f"archive member lookup for {suffix!r} returned {len(matches)} files")
        stream = archive.extractfile(matches[0])
        if stream is None:
            raise SystemExit(f"could not read archive member {matches[0].name}")
        return stream.read()


def check_external(candidates: list[dict]) -> None:
    atlas = next(c for c in candidates if c["candidate_id"].startswith("M0044-C02"))
    atlas_archive = archive_bytes(atlas)
    assert sha256_bytes(atlas_archive) == atlas["archive_sha256"]
    atlas_source = archive_member(atlas_archive, "/" + atlas["file"])
    assert sha256_bytes(atlas_source) == atlas["file_sha256"]
    atlas_text = atlas_source.decode()
    for marker in (
        "structure SVD (d T : ℕ) where",
        "σval_nonneg : ∀ j, 0 ≤ σval j",
        "def SVD.toMatrix",
        "def SVD.IsDecompOf",
        "A = S.toMatrix",
    ):
        assert marker in atlas_text, marker
    definition = atlas_text[atlas_text.index("structure SVD") : atlas_text.index("def SVD.toMatrix")]
    assert "Orthonormal" not in definition and "unitary" not in definition.lower()
    assert "theorem" not in atlas_text
    assert archive_member(atlas_archive, "/lean-toolchain").decode().strip() == atlas["toolchain"]
    atlas_manifest = archive_member(atlas_archive, "/lake-manifest.json")
    assert sha256_bytes(atlas_manifest) == atlas["manifest_sha256"]
    atlas_manifest_json = json.loads(atlas_manifest)
    atlas_mathlib = next(p for p in atlas_manifest_json["packages"] if p["name"] == "mathlib")
    assert atlas_mathlib["rev"] == atlas["mathlib_revision"]
    assert sha256_bytes(archive_member(atlas_archive, "/LICENSE")) == atlas["license_sha256"]

    gaussian = next(c for c in candidates if c["candidate_id"].startswith("M0044-C03"))
    gaussian_archive = archive_bytes(gaussian)
    assert sha256_bytes(gaussian_archive) == gaussian["archive_sha256"]
    nuclear = archive_member(gaussian_archive, "/" + gaussian["file"])
    spectral = archive_member(gaussian_archive, "/" + gaussian["support_file"])
    assert sha256_bytes(nuclear) == gaussian["file_sha256"]
    assert sha256_bytes(spectral) == gaussian["support_file_sha256"]
    nuclear_text = nuclear.decode()
    for marker in (
        "theorem nuclear_sequence_svd",
        "[InnerProductSpace ℝ K]",
        "[SeparableSpace K] (h_inf : ¬ FiniteDimensional ℝ K)",
        "(y : ℕ → K) (hy : Summable (fun m => ‖y m‖))",
        "∃ (e : ℕ → K) (σ_ : ℕ → ℝ) (W : ℕ → ℕ → ℝ)",
        "compact_selfAdjoint_spectral_nat",
    ):
        assert marker in nuclear_text, marker
    forbidden = re.compile(r"\b(?:sorry|admit|sorryAx|axiom|opaque|unsafe)\b")
    assert not forbidden.search(without_comments(nuclear_text))
    assert not forbidden.search(without_comments(spectral.decode()))
    assert archive_member(gaussian_archive, "/lean-toolchain").decode().strip() == gaussian["toolchain"]
    gaussian_manifest = archive_member(gaussian_archive, "/lake-manifest.json")
    assert sha256_bytes(gaussian_manifest) == gaussian["manifest_sha256"]
    gaussian_manifest_json = json.loads(gaussian_manifest)
    gaussian_mathlib = next(p for p in gaussian_manifest_json["packages"] if p["name"] == "mathlib")
    assert gaussian_mathlib["rev"] == gaussian["mathlib_revision"]
    assert sha256_bytes(archive_member(gaussian_archive, "/LICENSE")) == gaussian["license_sha256"]


def main() -> None:
    audit = load(HERE / "anchor-audit.json")
    receipt = load(HERE / "anchor-audit-receipt.json")
    statement = load(HERE / "statement.json")
    instance = load(HERE / "instance.json")
    manifest = load(ROOT / "Docs" / "Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")
    packet_path = ROOT / ".stage1-worker-selftest.json"
    packet = load(packet_path) if packet_path.exists() else None

    assert audit["schema_version"] == "stage1-anchor-audit/1.0"
    assert audit["item_id"] == ITEM_ID and audit["theorem_id"] == THEOREM_ID
    assert audit["execution_rank"] == 1084
    assert audit["base_revision"] == BASE_REVISION and audit["base_tree"] == BASE_TREE
    assert output("git", "rev-parse", "HEAD") == BASE_REVISION
    assert output("git", "rev-parse", "HEAD^{tree}") == BASE_TREE
    assert receipt["item_id"] == ITEM_ID and receipt["theorem_id"] == THEOREM_ID
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert set(receipt["changed_paths"]) == CHANGED_PATHS
    assert receipt["audit_complete"] is False and receipt["theorem_complete"] is False
    if packet is not None:
        assert packet["item_id"] == ITEM_ID and packet["state"] == "[_]"
        assert packet["base_revision"] == BASE_REVISION
        assert set(packet["changed_paths"]) == CHANGED_PATHS
        assert packet["known_failures"] == receipt["known_failures"]

    target = next(row for row in manifest["targets"] if row["theorem_id"] == THEOREM_ID)
    assert target["execution_rank"] == 1084
    assert target["baseline"] == "L0" and target["rework_required"] is True
    assert target["theorem_complete"] is False
    item = next(row for row in execution["items"] if row["id"] == ITEM_ID)
    assert item["phase"] == "anchor_audit" and item["layer"] == 2
    assert item["state"] in {"[ ]", "[_]"}
    assert item["depends_on"] == ["S56-M-0044-STATEMENT"]
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]

    assert audit["canonical_target_expression_sha256"] == EXPRESSION_SHA256
    assert audit["canonical_statement_file_sha256"] == STATEMENT_SHA256
    assert sha256(HERE / "Statement.lean") == STATEMENT_SHA256
    formal = statement["canonical_formal_target"]
    assert formal["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert formal["statement_file_sha256"] == STATEMENT_SHA256
    anchor_state = instance["anchor_audit"]
    assert anchor_state["item_id"] == ITEM_ID
    assert anchor_state["exact_candidate_found"] is False
    assert anchor_state["accepted_machine_debt"] == "M3"
    assert instance["root_vector"] == {"H": "H1", "M": "M3", "R": "R3"}
    assert instance["audit_complete"] is False and instance["theorem_complete"] is False

    env = audit["immutable_environment"]
    assert env["mathlib_revision"] == MATHLIB_REVISION
    assert env["mathlib_tree"] == MATHLIB_TREE
    assert output("git", "rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert output("git", "rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert output("git", "status", "--short", cwd=MATHLIB) == ""
    assert sha256(MATHLIB / "LICENSE") == env["license_sha256"]
    assert sha256(LEAN_ROOT / "lake-manifest.json") == env["manifest_sha256"]
    assert sha256(LEAN_ROOT / "lean-toolchain") == env["toolchain_file_sha256"]

    candidates = audit["candidates"]
    candidate_ids = [candidate["candidate_id"] for candidate in candidates]
    assert len(candidate_ids) == len(set(candidate_ids)) == 3
    support = next(c for c in candidates if c["candidate_id"].startswith("M0044-C01"))
    assert support["revision"] == MATHLIB_REVISION and support["tree"] == MATHLIB_TREE
    for source in support["source_files"]:
        path = MATHLIB / source["path"]
        assert source["blob"] == output("git", "rev-parse", f"HEAD:{source['path']}", cwd=MATHLIB)
        assert sha256(path) == source["sha256"]
    assert support["classification"] == "M3_support_only"
    assert support["terminal_declaration"] is None and support["terminal_proof_body"] is None

    exact_phrases: list[tuple[str, str]] = []
    for package in PACKAGES.iterdir():
        if not package.is_dir():
            continue
        for extension in ("*.lean", "*.md"):
            for path in package.rglob(extension):
                if ".git" in path.parts:
                    continue
                text = path.read_text(encoding="utf-8", errors="ignore")
                if re.search(r"singular value decomposition|\bSVD\b", text, re.IGNORECASE):
                    exact_phrases.append((package.name, str(path.relative_to(package))))
    assert exact_phrases == [], exact_phrases

    check_external(candidates)

    adapter = (HERE / "AnchorAudit.lean").read_text(encoding="utf-8")
    for declaration in support["declarations"]:
        assert f"#check {declaration}" in adapter
    forbidden = re.compile(r"\b(?:sorry|admit|sorryAx|axiom|unsafe|opaque)\b")
    assert not forbidden.search(without_comments(adapter))

    result = audit["audit_result"]
    assert result["inventory_classified"] is True
    assert result["source_boundary_coverage"].startswith("3/3 frozen candidates")
    assert result["exact_candidate_located"] is False
    assert result["support_candidates_kernel_checked"] is True
    assert result["candidate_accepted_by_master"] is False
    assert result["root_machine_debt_before"] == "M3"
    assert result["root_machine_candidate_after"] == "M3"
    assert result["accepted_root_machine_debt_after"] == "M3"
    assert result["node_self_tested"] is True
    assert result["audit_complete"] is False and result["theorem_complete"] is False
    assert audit["discovery_protocol"]["saturation_claim"] is False

    lean = subprocess.run(
        ["lake", "env", "lean", "../../Stage1_Instances/THM-M-0044/AnchorAudit.lean"],
        cwd=LEAN_ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=180,
        check=False,
    )
    if lean.returncode:
        sys.stdout.write(lean.stdout)
        raise SystemExit(lean.returncode)
    normalized = re.sub(r"\s+", " ", lean.stdout)
    if normalized.count("propext, Classical.choice, Quot.sound") != 9:
        sys.stdout.write(lean.stdout)
        raise SystemExit("unexpected prerequisite axiom reports")
    if normalized.count("propext, Quot.sound") != 1:
        sys.stdout.write(lean.stdout)
        raise SystemExit("unexpected Gram-Hermitian axiom report")
    if hashlib.sha256(lean.stdout.encode()).hexdigest() != LEAN_OUTPUT_SHA256:
        sys.stdout.write(lean.stdout)
        raise SystemExit("anchor-probe Lean output changed")

    print(
        "check_anchor_audit: ok "
        "(THM-M-0044; 3 candidates classified; pinned support checked; "
        "no exact candidate; accepted root remains M3; audit_complete=false; theorem_complete=false)"
    )


if __name__ == "__main__":
    main()
