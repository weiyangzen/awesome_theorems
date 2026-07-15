#!/usr/bin/env python3
"""Fail-closed narrow validator for S56-M-1023-VALIDATION."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import platform
import re
import shutil
import subprocess
import sys
import time


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-1023"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = (LEAN_ROOT / ".lake" / "packages" / "mathlib").resolve()
ITEM = "S56-M-1023-VALIDATION"
THEOREM = "THM-M-1023"
BASE_REVISION = "a9274bb02f984e5c74d2c97339044c6db8eb14f9"
BASE_TREE = "c72a5af07dd4ab3f7088c516c74235e794a6de09"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MATHLIB_REMOTE = "https://github.com/leanprover-community/mathlib4.git"
UPSTREAM_REVISION = "93b635fba23398bfb1f0db8d220f88172f6900b6"
TARGET_EXPRESSION = "f84253c83a8c31d9b77246bc0b3eef7715b0d0a04b707bb91cd5c329fdde1a2f"
REGISTRY_DENOMINATOR = "d4c7d2a1d47477fc812ed85f49f768034a99424755d90cb4de202a112a80c825"
EXPECTED_AXIOMS = ["propext", "Classical.choice", "Quot.sound"]
EXPECTED_INPUTS = {
    "Statement.lean": "ebb29fb83091cddccb5eeeeddd8924b2b7960cff12bbdf492070780d4222e296",
    "ObligationTree.lean": "08cbbbaad4f6ea735dcc9da0ce6f26d5782313670295c54c87b0b7115cd10985",
    "Proof.lean": "391a7e04692c213b000229339d6ed734141fc62466c06552d5fa0cd4d50579b8",
    "Validation.lean": "4e15c9af20cfc331f7b328eaedfb6044b1ae096aeb07bca7d9eaf982244b45cc",
    "instance.json": "b09fae7437e8524f4ceaa8ab2a9d9bdec9b41f49f25171ec235c9048067d03a5",
    "anchor-audit.json": "f58cb74240f545238d26d41a0d3f34590ec888b0532db8cd57121ea8a3deaec9",
    "obligation-registry.json": "bd0fba6bed549ab3a196f0ab5fe02f3434093226effd922b10000ab33248d6ac",
    "typed-graphs.json": "4b67e6ef2f2d04cdd4e23758fe00b7125f1b8f5e7b495657db0b9199ee51b698",
    "proof-receipt.json": "2accc37546accb0efd1c5c87c6a5324fb7d90da588335435224bb0106f10fda3",
    "vendor-manifest.json": "0e1ca71947378058abc2580f632f7f2dc656f66aec6a1c6f6478afc96610daa5",
    "VENDOR_PROVENANCE.md": "e69c50cd0bc8b99b6f73882d06072f417b5e0c37a0b40b6f6271b55fb4be5035",
    "source_statement_crosswalk.md": "367fb86d80c0b9a4a62eb1ddaaab60c6bfb2404d26cf89e23c9d4888e3dd2579",
    "check_validation.sh": "96c26d44db76d88ea56d1ac6892e59d2dae7c899f59c882bde9dd725bd3b896e",
    "validation-spec.json": "a626b118bcaaf963ce307b9cc786f8737ca4cd4753d60e46f4956c8a4e83363d",
    "build_vendor_manifest.py": "1551f2d306f9b11248b9e53fb9dd2e559cfaadd03cfff80f65668e2dbfcb7560",
    "Vendor/LICENSE": "9ccb61ce372d47010507d876144053d40f49203851663956ae8c46e469dbfe79",
}
EXPECTED_TOOL_INPUTS = {
    "lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
EXPECTED_TOOL_DIGESTS = {
    "lean": "3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf",
    "lake": "a608ff084d7e2af228b92a29d7c2fd083ba0580e46889175ec74a81678c98359",
    "python3": "b8d8288faefdd300201f43fcf00f6f539a27218eeed3a3dff5ab10b9c4c99700",
    "git": "8a48eefa306b9a2a9c3e576784a74ad7485779279e5a46ec43361a1864760e45",
    "bash": "3efccc187bafa75ff1e37d246270ab3e7aa559f242c7a52bf3ec2a1b5450bdbd",
    "bwrap": "0abea81db798ebf6b4742ac0664802d97521547a353c2a0dbdc21d76cbbfd2c0",
}
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
    "PASS kernel: network-isolated trust-zero replay compiled 20 vendored modules, frozen composition, proof root, and differential root",
    "PASS hygiene: proof and differential roots are transitively sorry-free; local and vendored source scans found no prohibited proof escape",
    "PASS selected provenance: target, vendor reconstruction, upstream pins, license, clean mathlib pin, selected artifact, and tool hashes agree",
    "FAIL CLOSED authority: S56-M-1023-PROOF is worker-provisional; frozen graph and stale anchor audit await master reconciliation",
    "FAIL CLOSED foundation/trust: observed axioms are unaccepted and complete transitive declaration/TCB closure is absent",
    "FAIL CLOSED hermetic release: the shared warm mathlib cache was reused; no cold empty-cache offline restoration or deterministic bundle exists",
    "FAIL CLOSED independent release: the differential root used the same worker, checkout, cache, and terminal proof body",
    "OPEN human/readable gates: H0 and R0 reviews are absent; audit_complete=false and theorem_complete=false",
    "NO STATE CHANGE: accepted root vector remains H1/M3/R4 and accepted_closed_obligation_ids is empty",
)
RECIPE_STARTED = time.monotonic()
RECIPE_TIMEOUT_SECONDS = 3600.0


if sys.flags.optimize:
    raise SystemExit("validation failed: Python optimization disables fail-closed assertions")


def reject_duplicate_keys(pairs: list[tuple[str, object]]) -> dict:
    value: dict[str, object] = {}
    for key, item in pairs:
        assert key not in value, ("duplicate JSON key", key)
        value[key] = item
    return value


def load(path: Path) -> dict:
    value = json.loads(
        path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicate_keys
    )
    assert isinstance(value, dict), path
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(argv: list[str], *, cwd: Path = ROOT, timeout: float | None = None) -> str:
    remaining = RECIPE_TIMEOUT_SECONDS - (time.monotonic() - RECIPE_STARTED)
    if remaining <= 0:
        raise TimeoutError("validation recipe exceeded its 3600-second wall-clock bound")
    result = subprocess.run(
        argv,
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=min(remaining, timeout) if timeout is not None else remaining,
        check=False,
    )
    if result.returncode:
        raise RuntimeError(f"validation failed ({result.returncode}): {argv!r}\n{result.stdout}")
    return result.stdout


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["git", *args], cwd=cwd, timeout=60).strip()


def strip_lean_comments_and_strings(source: str) -> str:
    """Erase nested comments and string/character contents before hygiene scans."""
    out: list[str] = []
    i = 0
    block_depth = 0
    line_comment = False
    quoted: str | None = None
    escaped = False
    while i < len(source):
        pair = source[i:i + 2]
        char = source[i]
        if line_comment:
            out.append("\n" if char == "\n" else " ")
            line_comment = char != "\n"
            i += 1
        elif block_depth:
            if pair == "/-":
                block_depth += 1
                out.extend("  ")
                i += 2
            elif pair == "-/":
                block_depth -= 1
                out.extend("  ")
                i += 2
            else:
                out.append("\n" if char == "\n" else " ")
                i += 1
        elif quoted:
            out.append("\n" if char == "\n" else " ")
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == quoted:
                quoted = None
            i += 1
        elif pair == "/-":
            block_depth = 1
            out.extend("  ")
            i += 2
        elif pair == "--":
            line_comment = True
            out.extend("  ")
            i += 2
        elif char == '"':
            quoted = char
            out.append(" ")
            i += 1
        else:
            out.append(char)
            i += 1
    assert block_depth == 0 and quoted is None
    return "".join(out)


def assert_text_hygiene(path: Path) -> None:
    data = path.read_bytes()
    assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())


def main() -> None:
    os.umask(0o022)
    os.environ.update({"LANG": "C.UTF-8", "LC_ALL": "C.UTF-8", "TZ": "UTC"})
    spec = load(HERE / "validation-spec.json")
    receipt = load(HERE / "validation-receipt.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")
    targets = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    instance = load(HERE / "instance.json")
    anchor = load(HERE / "anchor-audit.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    proof_receipt = load(HERE / "proof-receipt.json")
    vendor = load(HERE / "vendor-manifest.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 499 and target["baseline"] == "L0"
    assert target["target_lane"] == "hard_mathlib_anchor_and_wrapper"
    assert target["lifecycle_mode"] == "planned"
    assert target["rework_required"] is True and target["theorem_complete"] is False
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item == {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 499,
        "phase": "validation",
        "layer": 5,
        "state": "[ ]",
        "depends_on": ["S56-M-1023-PROOF"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Run hermetic kernel, trust, provenance, and independent validation gates.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }
    predecessor = next(row for row in execution["items"] if row["id"] == "S56-M-1023-PROOF")
    assert predecessor["state"] == "[_]"

    assert instance["canonical_formal_target"]["elaborated_expression_hash"] == (
        f"sha256:{TARGET_EXPRESSION}"
    )
    assert instance["root_vector"] == {"human": "H1", "machine": "M3", "readability": "R4"}
    assert instance["audit_complete"] is instance["theorem_complete"] is False
    assert registry["root_obligation_id"] == "M1023-ROOT"
    assert registry["denominator_sha256"] == REGISTRY_DENOMINATOR
    assert graphs["registry_denominator_sha256"] == REGISTRY_DENOMINATOR
    assert graphs["closure_boundary"] == {
        "closed_obligations": ["M1023-S-BOUNDARY", "M1023-S-DEFINITIONS", "M1023-T-ASSEMBLE"],
        "root_closed": False,
        "audit_complete": False,
        "theorem_complete": False,
        "remaining_root_cut_set": ["M1023-T-FORWARD", "M1023-T-REVERSE"],
        "composition_certificates": ["Stage1Instances.THM_M_1023.root_of_directionPackages"],
        "reason": "Final composition is conditional; neither mathematical direction has a proof body.",
    }
    foundation = next(node for node in graphs["nodes"] if node["obligation_id"] == "M1023-S-FOUNDATION")
    provenance = next(node for node in graphs["nodes"] if node["obligation_id"] == "M1023-X-PROVENANCE")
    assert foundation["machine_debt"] == provenance["machine_debt"] == "M4"
    assert foundation["validity"]["revocation_state"] == "open"
    assert provenance["validity"]["revocation_state"] == "open"
    assert anchor["root_machine_classification"] == "M3"
    assert anchor["terminal_result"].startswith("No exact or stronger terminal Lean 4 theorem")
    assert proof_receipt["item_id"] == "S56-M-1023-PROOF"
    assert proof_receipt["accepted"] is False and proof_receipt["proposed_state"] == "[_]"
    assert proof_receipt["covered_obligation_ids"] == ["M1023-ROOT"]
    assert proof_receipt["accepted_closed_obligation_ids"] == []
    assert proof_receipt["canonical_target_expression_sha256"] == TARGET_EXPRESSION
    assert proof_receipt["registry_denominator_sha256"] == REGISTRY_DENOMINATOR

    assert spec["item_id"] == receipt["item_id"] == ITEM
    assert spec["theorem_id"] == receipt["theorem_id"] == THEOREM
    assert spec["argv"] == ["python3", "-I", "-B", str(Path("Stage1_Instances") / THEOREM / "check_validation.py")]
    assert spec["timeout_seconds"] == 3600 and spec["network_policy"] == "denied"
    assert spec["covered_obligation_ids"] == ["M1023-ROOT"]
    assert receipt["canonical_target"]["elaborated_expression_sha256"] == TARGET_EXPRESSION
    assert receipt["canonical_target"]["registry_denominator_sha256"] == REGISTRY_DENOMINATOR

    for name, expected in EXPECTED_INPUTS.items():
        assert sha256(HERE / name) == expected, f"stale validation input: {name}"
        assert receipt["inputs"][name] == expected, name
    for name, expected in EXPECTED_TOOL_INPUTS.items():
        assert sha256(LEAN_ROOT / name) == expected, f"changed tool input: {name}"
        assert receipt["inputs"][name] == expected, name
    assert receipt["inputs"]["check_validation.py"] == sha256(HERE / "check_validation.py")
    assert receipt["inputs"]["validation-phase.md"] == sha256(HERE / "validation-phase.md")

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|implemented_by|native_decide|run_tac)\b|"
        r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
        r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
        r"(?:axiom|constant|opaque|unsafe|extern)\b",
        re.MULTILINE,
    )
    lean_sources = [HERE / name for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean")]
    lean_sources.extend(sorted((HERE / "Vendor").rglob("*.lean")))
    assert len(lean_sources) == 24
    for path in lean_sources:
        source = strip_lean_comments_and_strings(path.read_text(encoding="utf-8"))
        assert prohibited.search(source) is None, f"prohibited proof device in {path}"
    differential = (HERE / "Validation.lean").read_text(encoding="utf-8")
    assert "import Proof" not in differential and "import ObligationTree" not in differential
    assert "independentlyReconstructedRoot" in differential
    assert not list(HERE.rglob("*.olean")) and not list(HERE.glob("tmp*.lean"))

    assert vendor["upstream"]["revision"] == UPSTREAM_REVISION
    assert vendor["upstream"]["source_archive_sha256"] == (
        "585b9255907bc5db4c44f010acf98f7a9d608eea1d845b93f6938ff2437e4621"
    )
    assert vendor["compatibility"]["normalized_patch_sha256"] == (
        "ee3fcdea45ff454fe2aab4886881136af66070659c91a4b010a37964d95d3c84"
    )
    assert vendor["closure"]["module_count"] == len(vendor["files"]) == 20
    assert vendor["closure"]["vendored_bytes"] == 727852
    assert vendor["license"] == {
        "spdx": "MIT",
        "path": "Vendor/LICENSE",
        "sha256": EXPECTED_INPUTS["Vendor/LICENSE"],
    }
    assert {path.relative_to(HERE / "Vendor").as_posix() for path in (HERE / "Vendor").rglob("*") if path.is_file()} == (
        {row["path"] for row in vendor["files"]} | {"LICENSE"}
    )
    for row in vendor["files"]:
        source = HERE / "Vendor" / row["path"]
        assert sha256(source) == row["vendored_sha256"]
        assert source.stat().st_size == row["vendored_bytes"]
    terminal_source = HERE / "Vendor/LeanLevy/Levy/LevyKhintchineUniqueness.lean"
    assert sha256(terminal_source) == (
        "9758db049ce7a4c6d2115b2d8ed077da79f0201716727382f6d148d0547e39b0"
    )
    assert receipt["provenance"]["terminal_proof_body_id"] == (
        f"sha256:{sha256(terminal_source)}"
    )

    assert MATHLIB.is_dir(), "pinned mathlib artifact is unavailable"
    assert git("rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert git("remote", "get-url", "origin", cwd=MATHLIB) == MATHLIB_REMOTE
    assert git("status", "--porcelain=v1", cwd=MATHLIB) == ""
    selected = MATHLIB / "Mathlib/MeasureTheory/Measure/CharacteristicFunction/Basic.lean"
    selected_olean = MATHLIB / ".lake/build/lib/lean/Mathlib/MeasureTheory/Measure/CharacteristicFunction/Basic.olean"
    assert git("rev-parse", "HEAD:Mathlib/MeasureTheory/Measure/CharacteristicFunction/Basic.lean", cwd=MATHLIB) == "7f6995e17108894439cef647132609762bb805b6"
    assert sha256(selected) == "c25fa7bec393a7ff980b5ab783a71e777916e0de76334b21907e1c79a199546b"
    assert sha256(selected_olean) == "ac4c91ea6557bc04e225d37cc0206499c0822f15af19989d2ab513dc5cad53ad"
    assert sha256(MATHLIB / "LICENSE") == "b40930bbcf80744c86c46a12bc9da056641d722716c378f5659b9e555ef833e1"

    lean = Path(run(["lake", "env", "which", "lean"], cwd=LEAN_ROOT, timeout=60).strip())
    lake = Path(run(["lake", "env", "which", "lake"], cwd=LEAN_ROOT, timeout=60).strip())
    tools = {
        "lean": lean,
        "lake": lake,
        "python3": Path(os.path.realpath(sys.executable)),
        "git": Path(shutil.which("git") or ""),
        "bash": Path(shutil.which("bash") or ""),
        "bwrap": Path(shutil.which("bwrap") or ""),
    }
    for name, path in tools.items():
        assert path.is_file() and sha256(path) == EXPECTED_TOOL_DIGESTS[name], (name, path)
        assert receipt["environment"][f"{name}_executable_sha256"] == EXPECTED_TOOL_DIGESTS[name]
    assert "4.29.0" in run([str(lean), "--version"], timeout=60)
    assert "5.0.0-src+98dc76e" in run([str(lake), "--version"], timeout=60)
    assert receipt["environment"]["platform"] == f"{platform.system()} {platform.release()} {platform.machine()}"

    runner_output = run(["bash", str(HERE / "check_validation.sh")])
    assert runner_output == (
        "PASS network-isolated trust-zero replay: 20 vendored modules, exact statement, frozen composition, proof root, and differential root elaborated\n"
        "PASS trust observation: proof/differential declarations are sorry-free; six reports use exactly propext, Classical.choice, and Quot.sound\n"
        "PASS differential scope: Validation.lean reconstructs the exact root without importing Proof or ObligationTree\n"
    )
    assert receipt["execution"]["runner_stdout_sha256"] == hashlib.sha256(runner_output.encode()).hexdigest()
    assert receipt["execution"]["observed_axioms"] == EXPECTED_AXIOMS
    assert receipt["result"]["accepted_foundation_profile"] is False
    assert receipt["result"]["complete_transitive_declaration_closure"] is False
    assert receipt["result"]["complete_transitive_tcb_inventory"] is False
    assert receipt["result"]["accepted_root_closed"] is False
    assert receipt["result"]["audit_complete"] is receipt["result"]["theorem_complete"] is False
    assert receipt["first_failed_gate"] == "dependency.S56-M-1023-PROOF.master_acceptance"
    assert receipt["first_failed_release_gate"] == "S56-10.6-HERMETIC-COLD-BUILD"
    assert receipt["root_vector_before"] == receipt["root_vector_after_worker_selftest"] == {
        "H": "H1", "M": "M3", "R": "R4"
    }
    assert receipt["accepted_closed_obligation_ids"] == []
    assert set(receipt["changed_paths"]) == CHANGED_PATHS

    assert packet == {
        "item_id": ITEM,
        "changed_paths": receipt["changed_paths"],
        "commands": receipt["worker_commands"],
        "output_summary": "\n".join(SUMMARY_LINES),
        "base_revision": BASE_REVISION,
        "known_failures": receipt["known_failures"],
        "state": "[_]",
    }
    actual_changes = {
        line[3:] for line in git("status", "--short", "--untracked-files=all").splitlines()
        if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual_changes == CHANGED_PATHS, (actual_changes, CHANGED_PATHS)
    for path in CHANGED_PATHS:
        assert_text_hygiene(ROOT / path)
    assert receipt["execution"]["summary_sha256"] == hashlib.sha256(
        ("\n".join(SUMMARY_LINES) + "\n").encode()
    ).hexdigest()
    print("\n".join(SUMMARY_LINES))


if __name__ == "__main__":
    main()
