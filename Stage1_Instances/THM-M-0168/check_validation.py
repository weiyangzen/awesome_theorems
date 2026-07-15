#!/usr/bin/env python3
"""Fail-closed validation replay for S56-M-0168-VALIDATION."""

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
import time


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0168"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM = "S56-M-0168-VALIDATION"
THEOREM = "THM-M-0168"
BASE_REVISION = "7505614b75de56cf10bbd196a4aaa0ca2a117064"
BASE_TREE = "730e162a2133e4a077d764043b5e722c1f7feb39"
EXPRESSION_SHA256 = "b5cef8a8bb3b5505be6670f226315884282c53bb0040c30345f4fb0dc33254f5"
DENOMINATOR_SHA256 = "170699112c956a2921b831b9e1bb9edbbd627ece6922dda7ab1e43e4d6d389b1"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MATHLIB_REMOTE = "https://github.com/leanprover-community/mathlib4.git"
MATHLIB_LICENSE_SHA256 = "b40930bbcf80744c86c46a12bc9da056641d722716c378f5659b9e555ef833e1"
LEAN_TOOLCHAIN = "leanprover/lean4:v4.29.0"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
LEAN_SHA256 = "3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf"
LAKE_SHA256 = "a608ff084d7e2af228b92a29d7c2fd083ba0580e46889175ec74a81678c98359"
BWRAP_SHA256 = "0abea81db798ebf6b4742ac0664802d97521547a353c2a0dbdc21d76cbbfd2c0"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
FROZEN_CUT = [
    "M0168-C-GRAPH",
    "M0168-N-PDE-MINIMAL",
    "M0168-L-STABILITY",
    "M0168-C-CUTOFF",
    "M0168-L-CURVATURE",
    "M0168-L-DERIVATIVE-RIGIDITY",
    "M0168-T-INTEGRATE",
]
REMAINING_CUT = FROZEN_CUT[:-1]
EXPECTED_INPUTS = {
    "Statement.lean": "5e773260e93f29c5da263e749b8bd5208a7b61e344d45b588ad9cda65d311a78",
    "ObligationTree.lean": "642153a1f88af5d71a954b417b136fd95d1eaf82b8d1fdf176d60b3ace3bf24e",
    "AnchorAudit.lean": "66761bccebfce4e7655321b4d0128e8252f07b7c227d196839ff30c0972fdfb1",
    "Proof.lean": "85c6b4a484d026ce83cee32fbd449f724e3a501fc37f33c49dc05a094b0cf5db",
    "Validation.lean": "27e674bcf28dcd9992b9404237a54907541ce243fd8af6b5a9e336ae640f3fd4",
    "instance.json": "4333aea30e350687a643e027b5f2ab570e5016ba00c722a3d55adbf2d05a4268",
    "statement.json": "390945f4610500c015a125fc307ed9260cd66d756524c5ebbb9b3b99804f7d6f",
    "anchor-audit.json": "f29dd21045e7c2fdf86bb623ab5188254077e5e22b0baa0fa803a18151d4f5b7",
    "obligation-registry.json": "883e0c0a98c6d3b6e5e77adb9c5fb376c87f043dd7b80b4e882cbdb0045ed9ba",
    "typed-graphs.json": "1e8ac1d8a5906eccbd79a35b43fad6e89ee571fa4ee0bc5aa0e6b08894dcac41",
    "task-dag.json": "ed4f6447ff9458943fea6188b8a7a810af553bd9203b7b7316c89e2d1e54e2e4",
    "proof-receipt.json": "23752dfc3c852f1cc36dd990a08bf7a69844e6879b715bd8a0bc6c17d3fe99e3",
    "check_proof.sh": "48d9c087684e32aed49a51d9da25f8aad4103bee478d6db3d9eb6fe2518e1a0b",
    "check_obligation_tree.py": "8b9b0b57f81bb0d3ffdc575f5dbc48333c4d63dcbb2b4ab9dedae1c7b5d0bc32",
    "source-statement-crosswalk.md": "5bbb714424a41fe2fb565557b48c6d1eac40390c4689ffd28b03c14df05595f4",
    "validation-spec.json": "a496ca5a94833b78aa7643b93fd020d16a2f2d9ea9d0e9d3ee2e09849e01ea68",
    "validation-blocker.json": "dbcb6b52ce6e1cc47f30b6f1b7e81753acfc4d41081c43e8fd1948436190f4af",
}
TOOL_INPUTS = {
    "lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
MATHLIB_INPUTS = {
    "Mathlib/Analysis/Calculus/ContDiff/Defs.lean": (
        "48fa38706dd12f7fcf7fc44d3c51a6e763ed5132",
        "562b303f3e948decac52c1ac88dc8e100311a42c0c64a77b4b0972fc85fa7f88",
        "583529ccee3458e367b88fe1edd6c0da3c166888da0da17894aa728ee8cfe1a7",
    ),
    "Mathlib/Analysis/Calculus/MeanValue.lean": (
        "3596c8ca430ed6d2b0b7c65813d69c756fe14153",
        "1709e5d96db3fb21ef9a5725c587a1912d31fe963ff4ed36b917e5e32c7c43cc",
        "8fccc3aaea96147394f71ef964a19eda08b449e25c97fae780f26aedad6061e5",
    ),
    "Mathlib/Util/AssertNoSorry.lean": (
        "060d8a764d2a6d1d2963d9c500b6084a05bed534",
        "aa9f7bebacafc688c894ef2171930e51ed19e0dfe722581848a2414d28900d4d",
        "c8bf37753d9bad47b9fe67e32436da8b9af516a4abbbe14e74726f01ba2fb30b",
    ),
    "Mathlib/Util/PrintSorries.lean": (
        "24d72cc680fa8b07f0d1062f670a5a824934a227",
        "03670b0b0007740e5390dadd49c3d10a02b7d0919092d2b3214ef8a6a8cf798f",
        "9bcc4076e0aee5febb2eea5cf9dc959f38526e9f974afdfdd8658bfd318d5bb7",
    ),
}
TRUST_DECLARATIONS = (
    "Stage1Instances.THM_M_0168_Obligations.compose_root",
    "Stage1Instances.THM_M_0168_Obligations.constantPartials_to_affine",
    "Stage1Instances.THM_M_0168_Obligations.constantPartialsToAffine_proof",
    "Stage1Instances.THM_M_0168_Obligations.bernstein_of_derivativeRigidity",
    "Stage1Instances.THM_M_0168_Obligations.canonicalTarget_iff_obligationTarget",
    "Stage1Instances.THM_M_0168_Obligations.canonical_bernstein_of_derivativeRigidity",
)
SUMMARY_LINES = (
    "PASS THM-M-0168 network-isolated trust-zero replay of the exact statement, frozen conditional composition, affine-integration body, and canonical transport",
    "PASS trust probe and hygiene: six declarations are transitively sorry-free and use exactly propext, Classical.choice, and Quot.sound",
    "PASS selected provenance: frozen local hashes, clean mathlib pin/tree/origin/license, four source/blob/olean triples, and Lean/Lake identities agree",
    "OPEN exact Bernstein root M2: M0168-T-INTEGRATE is provisionally revalidated, while DerivativeRigidity and its six-node root cut remain open",
    "BLOCKED validation gates: proof master acceptance, structured-state freshness, complete TCB/provenance, cold offline hermetic replay, and distinct-runner verification",
    "audit_complete=false; theorem_complete=false",
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
STARTED = time.monotonic()
TIMEOUT_SECONDS = 900.0


if sys.flags.optimize:
    raise SystemExit("validation failed: Python optimization disables assertions")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path: Path) -> dict:
    def no_duplicates(pairs: list[tuple[str, object]]) -> dict:
        result: dict[str, object] = {}
        for key, value in pairs:
            assert key not in result, f"duplicate JSON key in {path}: {key}"
            result[key] = value
        return result

    value = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=no_duplicates)
    assert isinstance(value, dict), path
    return value


def run(argv: list[str], *, cwd: Path = ROOT, env: dict[str, str] | None = None) -> str:
    remaining = TIMEOUT_SECONDS - (time.monotonic() - STARTED)
    assert remaining > 0, "validation recipe exceeded its wall-clock bound"
    result = subprocess.run(
        argv,
        cwd=cwd,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=remaining,
        check=False,
    )
    if result.returncode:
        raise RuntimeError(f"command failed ({result.returncode}): {argv!r}\n{result.stdout}")
    return result.stdout


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["/usr/bin/git", *args], cwd=cwd).strip()


def code_without_comments_and_strings(source: str) -> str:
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


def axiom_set(output: str, declaration: str) -> set[str]:
    pattern = re.escape(f"'{declaration}' depends on axioms: [") + r"(.*?)]"
    matches = re.findall(pattern, output, re.DOTALL)
    assert len(matches) == 1, (declaration, len(matches))
    return {part.strip() for part in matches[0].split(",") if part.strip()}


def derive_toolchain() -> tuple[Path, Path]:
    env = dict(os.environ)
    env["ELAN_TOOLCHAIN"] = LEAN_TOOLCHAIN
    lean = Path(run(["lake", "env", "which", "lean"], cwd=MATHLIB, env=env).strip())
    lake = Path(run(["elan", "which", "lake"], cwd=MATHLIB, env=env).strip())
    assert lean.is_file() and os.access(lean, os.X_OK)
    assert lake.is_file() and os.access(lake, os.X_OK)
    assert sha256(lean) == LEAN_SHA256 and sha256(lake) == LAKE_SHA256
    version = run(["lake", "env", "lean", "--version"], cwd=MATHLIB, env=env)
    assert "Lean (version 4.29.0" in version and LEAN_COMMIT in version
    return lean, lake


def lean_path(lean: Path) -> str:
    roots = sorted(
        path.resolve()
        for path in (LEAN_ROOT / ".lake" / "packages").glob("*/.lake/build/lib/lean")
        if path.is_dir() and "flt-regular" not in path.parts
    )
    assert (MATHLIB / ".lake/build/lib/lean").resolve() in roots
    roots.append((lean.parent.parent / "lib" / "lean").resolve())
    return ":".join(map(str, roots))


def kernel_replay(lean: Path) -> dict[str, str]:
    path = lean_path(lean)
    with tempfile.TemporaryDirectory(prefix="m0168-validation-") as raw_tmp:
        tmp = Path(raw_tmp)
        for name in ("Statement.lean", "ObligationTree.lean", "AnchorAudit.lean", "Proof.lean", "Validation.lean"):
            shutil.copy2(HERE / name, tmp / name)
        (tmp / "home").mkdir()
        base = [
            "/usr/bin/bwrap", "--ro-bind", "/", "/", "--bind", str(tmp), str(tmp),
            "--dev", "/dev", "--proc", "/proc", "--unshare-net", "--die-with-parent",
            "--clearenv", "--setenv", "HOME", str(tmp / "home"),
            "--setenv", "LANG", "C.UTF-8", "--setenv", "LC_ALL", "C.UTF-8",
            "--setenv", "TZ", "UTC", "--setenv", "LEAN_NUM_THREADS", "1",
            "--chdir", str(tmp),
        ]

        def replay(name: str, include_local: bool) -> str:
            import_path = f"{tmp}:{path}" if include_local else path
            output = tmp / Path(name).with_suffix(".olean")
            return run(base + [
                "--setenv", "LEAN_PATH", import_path, str(lean), "--root", str(tmp),
                "--trust=0", "-t0", "-o", str(output), str(tmp / name),
            ])

        outputs = {
            "Statement.lean": replay("Statement.lean", False),
            "ObligationTree.lean": replay("ObligationTree.lean", False),
            "AnchorAudit.lean": replay("AnchorAudit.lean", False),
            "Proof.lean": replay("Proof.lean", True),
            "Validation.lean": replay("Validation.lean", True),
        }
        oleans = {name: sha256(tmp / Path(name).with_suffix(".olean")) for name in outputs}
    assert "BernsteinMinimalGraphTarget" in outputs["Statement.lean"]
    assert "Stage1Instances.THM_M_0168_Obligations.compose_root" in outputs["ObligationTree.lean"]
    assert all(name in outputs["AnchorAudit.lean"] for name in ("ContDiff", "fderiv"))
    for declaration in TRUST_DECLARATIONS:
        assert axiom_set(outputs["Validation.lean"], declaration) == EXPECTED_AXIOMS
    assert outputs["Validation.lean"].count("Declarations are sorry-free!") == len(TRUST_DECLARATIONS)
    combined = "\n".join(outputs.values())
    assert "sorryAx" not in combined and "declaration uses 'sorry'" not in combined
    assert not re.search(r"(^|\n).*error(?:\([^)]*\))?:", combined)
    return oleans


def main() -> None:
    receipt = load(HERE / "validation-receipt.json")
    spec = load(HERE / "validation-spec.json")
    blocker = load(HERE / "validation-blocker.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")
    instance = load(HERE / "instance.json")
    statement = load(HERE / "statement.json")
    anchor = load(HERE / "anchor-audit.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    local_tasks = load(HERE / "task-dag.json")
    proof_receipt = load(HERE / "proof-receipt.json")
    targets = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 665 and target["baseline"] == "L0"
    assert target["lifecycle_mode"] == "planned"
    assert target["rework_required"] is True and target["theorem_complete"] is False
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item["theorem_id"] == THEOREM and item["execution_rank"] == 665
    assert item["phase"] == "validation" and item["layer"] == 5
    assert item["state"] == "[ ]" and item["attempts"] == 0
    assert item["depends_on"] == ["S56-M-0168-PROOF"]
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM}"]
    predecessor = next(row for row in execution["items"] if row["id"] == "S56-M-0168-PROOF")
    assert predecessor["state"] == "[_]" and predecessor["attempts"] >= 1

    for name, digest in EXPECTED_INPUTS.items():
        assert sha256(HERE / name) == digest, f"stale validation input: {name}"
        assert receipt["inputs"][name] == digest, name
    for name, digest in TOOL_INPUTS.items():
        assert sha256(LEAN_ROOT / name) == digest, f"changed tool input: {name}"
        assert receipt["inputs"][name] == digest, name

    assert instance["root_vector"] == {"H": "H1", "M": "M4", "R": "R4"}
    assert instance["audit_complete"] is instance["theorem_complete"] is False
    formal = statement["canonical_formal_target"]
    assert formal["declaration_or_expression"] == "Stage1Instances.THM_M_0168.BernsteinMinimalGraphTarget"
    assert formal["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert formal["statement_file_sha256"] == EXPECTED_INPUTS["Statement.lean"]
    assert statement["theorem_proved"] is statement["theorem_complete"] is False
    assert anchor["root_machine_classification"] == "M4" and anchor["theorem_complete"] is False

    obligations = {row["obligation_id"]: row for row in registry["obligations"]}
    assert len(obligations) == 11 and registry["frozen_before_proof_execution"] is True
    assert registry["canonical_root_expression_sha256"] == EXPRESSION_SHA256
    denominator = hashlib.sha256(json.dumps(
        graphs["coverage_denominators"], sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    assert denominator == DENOMINATOR_SHA256
    assert set(graphs["coverage_denominators"]["canonical_obligations"]) == set(obligations)
    assert graphs["root_cut_set"] == FROZEN_CUT
    assert graphs["closure_metrics_observed"] is False
    assert obligations["M0168-ROOT"]["machine_debt"] == "M2"
    assert obligations["M0168-T-INTEGRATE"]["machine_debt"] == "M4"
    assert obligations["M0168-T-INTEGRATE"]["evidence_ids"] == []
    assert any(row["id"] == ITEM and row["state"] == "open" for row in local_tasks["tasks"])

    assert proof_receipt["accepted"] is False
    assert proof_receipt["support_state"] == "provisional_worker_selftest"
    assert proof_receipt["provisionally_closed_obligation_ids"] == ["M0168-T-INTEGRATE"]
    assert proof_receipt["accepted_closed_obligation_ids"] == []
    assert proof_receipt["proof_body"]["source_sha256"] == EXPECTED_INPUTS["Proof.lean"]
    assert proof_receipt["result"]["root_kernel_closed"] is False
    assert proof_receipt["result"]["theorem_complete"] is False
    assert set(proof_receipt["result"]["axioms"]) == EXPECTED_AXIOMS
    assert proof_receipt["remaining_root_cut_set"] == REMAINING_CUT

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|implemented_by|native_decide|run_tac|oracle)\b|"
        r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
        r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
        r"(?:axiom|constant|opaque|unsafe|extern)\b",
        re.MULTILINE,
    )
    for name in ("Statement.lean", "ObligationTree.lean", "AnchorAudit.lean", "Proof.lean", "Validation.lean"):
        clean = code_without_comments_and_strings((HERE / name).read_text(encoding="utf-8"))
        assert prohibited.search(clean) is None, f"prohibited proof device: {name}"
    validation_source = (HERE / "Validation.lean").read_text(encoding="utf-8")
    assert "theorem " not in code_without_comments_and_strings(validation_source)
    assert "assert_no_sorry" in validation_source and "#print sorries" in validation_source

    assert git("rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert git("remote", "get-url", "origin", cwd=MATHLIB) == MATHLIB_REMOTE
    assert git("status", "--porcelain=v1", "--untracked-files=all", cwd=MATHLIB) == ""
    assert sha256(MATHLIB / "LICENSE") == MATHLIB_LICENSE_SHA256
    for relative, (blob, source_digest, olean_digest) in MATHLIB_INPUTS.items():
        assert git("rev-parse", f"HEAD:{relative}", cwd=MATHLIB) == blob
        assert sha256(MATHLIB / relative) == source_digest
        olean = MATHLIB / ".lake/build/lib/lean" / Path(relative).with_suffix(".olean")
        assert sha256(olean) == olean_digest

    lean, lake = derive_toolchain()
    assert sha256(Path("/usr/bin/bwrap")) == BWRAP_SHA256
    oleans = kernel_replay(lean)
    assert set(oleans) == {"Statement.lean", "ObligationTree.lean", "AnchorAudit.lean", "Proof.lean", "Validation.lean"}
    assert all(re.fullmatch(r"[0-9a-f]{64}", digest) for digest in oleans.values())

    assert spec["schema_version"] == "stage1-validation-spec/1.0"
    assert spec["item_id"] == ITEM and spec["theorem_id"] == THEOREM
    assert spec["argv"] == [
        "/usr/bin/python3", "-I", "-B", f"Stage1_Instances/{THEOREM}/check_validation.py"
    ]
    assert spec["network_policy"] == "denied" and spec["expected_exit"] == 0
    assert receipt["recipe"] == spec
    assert receipt["item_id"] == blocker["item_id"] == packet["item_id"] == ITEM
    assert receipt["base_revision"] == blocker["base_revision"] == packet["base_revision"] == BASE_REVISION
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["verdict"] == "blocked" and receipt["release_grade"] is False
    assert receipt["canonical_target"] == formal["declaration_or_expression"]
    assert receipt["canonical_target_expression_sha256"] == EXPRESSION_SHA256
    assert receipt["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert receipt["result"]["root_kernel_closed"] is False
    assert receipt["result"]["validation_complete"] is False
    assert receipt["result"]["structured_state_freshness"] == "fail_closed"
    assert receipt["result"]["complete_transitive_foundation_tcb_provenance"] == "fail_closed"
    assert receipt["result"]["hermetic_cold_offline_replay"] == "fail_closed"
    assert receipt["result"]["independent_distinct_runner"] == "fail_closed"
    assert receipt["remaining_root_cut_set"] == REMAINING_CUT
    assert receipt["environment"]["lean_executable_sha256"] == sha256(lean)
    assert receipt["environment"]["lake_executable_sha256"] == sha256(lake)
    assert receipt["environment"]["bwrap_executable_sha256"] == sha256(Path("/usr/bin/bwrap"))
    assert blocker["outcome"] == "validation_packet_self_tested_gates_blocked"
    assert blocker["validation_phase_complete"] is False
    assert blocker["root_closed"] is blocker["audit_complete"] is blocker["theorem_complete"] is False

    assert set(packet) == {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert packet["state"] == "[_]"
    assert set(packet["changed_paths"]) == set(receipt["changed_paths"]) == CHANGED_PATHS
    assert packet["known_failures"] == receipt["known_failures"]
    assert any(command == spec["argv"] for command in packet["commands"])
    for line in SUMMARY_LINES:
        assert line in packet["output_summary"]

    status = git("status", "--short", "--untracked-files=all")
    actual = {line[3:] for line in status.splitlines() if line[3:] != "Formalizations/Lean/.lake"}
    assert actual == CHANGED_PATHS, (actual, CHANGED_PATHS)
    for relative in CHANGED_PATHS:
        data = (ROOT / relative).read_bytes()
        assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())

    for line in SUMMARY_LINES:
        print(line)


if __name__ == "__main__":
    main()
