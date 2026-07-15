#!/usr/bin/env python3
"""Fail-closed narrow validator for S56-M-1083-VALIDATION."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-1083"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM = "S56-M-1083-VALIDATION"
THEOREM = "THM-M-1083"
BASE_REVISION = "a9274bb02f984e5c74d2c97339044c6db8eb14f9"
BASE_TREE = "c72a5af07dd4ab3f7088c516c74235e794a6de09"
EXPRESSION_SHA256 = "fb7209158513f98f9692a12449560573c5009e1a2366ed34eb8e61f9cae7c58a"
DENOMINATOR_SHA256 = "06ca47d90b0a7af9d99c935d0c7766cea3df5e722f08b563d226d7736baf6a50"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MATHLIB_REMOTE = "https://github.com/leanprover-community/mathlib4.git"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
ALLOWED_AXIOMS = ["propext", "Classical.choice", "Quot.sound"]
RUNNER_STDOUT = (
    "PASS THM-M-1083 network-isolated narrow kernel replay",
    "PASS exact root, vendored terminal, bridges, and frozen composition trust probes",
    "PASS transitive sorry check and observed axiom boundary: propext, Classical.choice, Quot.sound",
)
RUNNER_STDOUT_SHA256 = "d9215301f9c23bc0e1f07e347edf8d5414c83f1558c763cb23b4ec15a431b12e"
EXPECTED_INPUTS = {
    "Statement.lean": "2b9c25f6eec19a8d8366850aa868f7ea13921827859f11e268c69b1149ab3c04",
    "ObligationTree.lean": "3f6337cdfbac95d6bc78d68728fa074219cc54d0f600eeb10dd5447d01731008",
    "Proof.lean": "5bd5472e7170dc88b579d739194b4704c3f44c872d61187612c32117be76db3d",
    "Validation.lean": "00e53b13109bbf26ce31091f6c22bf04554aa774d78c963ab23c5e08b9e7a9ab",
    "instance.json": "3a3d364b600c565fdc8d703d8ecdd9dff5ecb28c9d6a0ceb320f7054087cfaca",
    "task-dag.json": "f13656697985b3342e31abd924dd988b160dfa21013326f47f4528aa9bd3cbd3",
    "statement.json": "3bf4b61d578d08961021ca4bab5d9efef3d5db63b323a07e29124463c7215cb4",
    "anchor-audit.json": "718f29d7e35b729cd9d71ef2ff6dce15c00e6e6a62d32016b9810b55385c3a1e",
    "obligation-registry.json": "5f768dabf5986ffc5e92b5697233e2721c28d5fcdc69f60d65d0f899004ab6ad",
    "typed-graphs.json": "fffb2de52e626df799ca5c785ce4382f1c002a65d86356b1550e173bf3a9ec2f",
    "validation-specs.json": "e865040d2ed76113c298988587c3fb2ac3954d7d87177c4cf1c98bb8a9f9c561",
    "proof-receipt.json": "f07912715f97d9d5328028d3fbfa3b788e73898be8035f0bbc11d3ac4c7d9952",
    "proof-execution.json": "1a0384e6fef08540fe2246a76c231f87e905043e56c972e95f67c5e9dbbaae53",
    "PORT_PROVENANCE.md": "415ee4435783be70d48dcce833bca327200e0fae916cd41d5aae7815a26823c7",
    "Vendor/LICENSE": "c71d239df91726fc519c6eb72d318ec65820627232b2f796219e87dcf35d0ab4",
    "Vendor/README.md": "5bace4c6c3cd3953f478690cda3ec1a13b1a927051dd0a866fbcd6d4d99b0997",
    "check_obligation_tree.py": "1064c0b3de3adc10809a48e9f91f537b36690d46d920d781a4e9ec6b11c752ea",
    "check_validation.sh": "da502295455923bab7547666195c289dc868189248114211cd899bd5ee805b38",
}
EXPECTED_TOOL_INPUTS = {
    "lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
SOURCE_ROWS = {
    "Auxiliary/Algebra.lean": "9bc0dcd6055139822821505897555ae5a501feea0d3a249aa7022b7e6c5b34f3",
    "Auxiliary/ENNReal.lean": "108c7c5320e163d18e1c250d83a7170e1b80b5b631983f87298df5787c569af6",
    "Auxiliary/FiniteInf.lean": "042fae3af08e14c603c4cf85742162488d6a7ccc42f74d29ae70854ee38f3f4a",
    "Auxiliary/MeanInequalities.lean": "67995c387870e772e8882dea0c7a45168946489d6ffb30c2ba870a2c8b23c50d",
    "Auxiliary/MeasureTheory.lean": "3df7b5faa5795bda61419b864048349d2ae32d8381a4376bac0a337089b383e6",
    "Auxiliary/Metric.lean": "13f5040961175788f8631ba4551a00ef4671a0c172ba85f145c57b025f7b7d9e",
    "Auxiliary/Nat.lean": "43ea36f4a153fd31e5d3f329d094a672270d3bed31728bb2f63d543d994177ae",
    "Auxiliary/Topology.lean": "ce23e4180f97416196f30f05f52756ecc46c99737ec9bb674c9ed3f16014e2b6",
    "Continuity/Chaining.lean": "75e88c2b7800ebf9f0f3b3f52538444e3323a30f0cbfd603847d2874e3db87bc",
    "Continuity/CoveringNumber.lean": "1d4cad9147985c271cd58fc90bc60a8697933258db6b8228a85a0e2f125f543b",
    "Continuity/HasBoundedInternalCoveringNumber.lean": "688b05f9a645d3d87f8e5cab131b3d2b1723cac32b44703c8b54d92d45cd29e8",
    "Continuity/IsKolmogorovProcess.lean": "62f9ae5b726aba8f36db7a0cb92f9b446ba62e5b583804707aa2ae18b3378a02",
    "Continuity/KolmogorovChentsov.lean": "8c60d137ebb5918ebde96e5158867ff5a7e25b9711ef68cbcb9cb4626df9360b",
    "Continuity/KolmogorovChentsovInequality.lean": "0d8fd8b5bcd66770c79337fbc2ba9dcac7a888c9703f40ac665cef1504a30576",
    "Gaussian/StochasticProcesses.lean": "c5fc98b72eb3044fe49add5b47ce10ec8a9aeb1e47aa11aa32a91a2e0c393f81",
}
UPSTREAM_SOURCE_ROWS = {
    "Auxiliary/Algebra.lean": "9bc0dcd6055139822821505897555ae5a501feea0d3a249aa7022b7e6c5b34f3",
    "Auxiliary/ENNReal.lean": "108c7c5320e163d18e1c250d83a7170e1b80b5b631983f87298df5787c569af6",
    "Auxiliary/FiniteInf.lean": "042fae3af08e14c603c4cf85742162488d6a7ccc42f74d29ae70854ee38f3f4a",
    "Auxiliary/MeanInequalities.lean": "67995c387870e772e8882dea0c7a45168946489d6ffb30c2ba870a2c8b23c50d",
    "Auxiliary/MeasureTheory.lean": "e6637d648b5782dad84bd3fe114e731a31cb2911534f04e2ef27012b8e1ac7a0",
    "Auxiliary/Metric.lean": "13f5040961175788f8631ba4551a00ef4671a0c172ba85f145c57b025f7b7d9e",
    "Auxiliary/Nat.lean": "43ea36f4a153fd31e5d3f329d094a672270d3bed31728bb2f63d543d994177ae",
    "Auxiliary/Topology.lean": "ce23e4180f97416196f30f05f52756ecc46c99737ec9bb674c9ed3f16014e2b6",
    "Continuity/Chaining.lean": "dbb3f80c0e56d708c4dfcd1a30cd7420f280af2f50cdf2785fa2f2ad34cc7b19",
    "Continuity/CoveringNumber.lean": "89829da52abf33125f18c30f82f2b76d89516682483c1a5cc3caa65d3a649f9d",
    "Continuity/HasBoundedInternalCoveringNumber.lean": "8166a60c831bf60262171d94f53298908e7372ebfb76a136e9e7de6cd4725f03",
    "Continuity/IsKolmogorovProcess.lean": "e54c594363a9cd15f60faeba19b643e972507d5af568f90ee277ec655ea78dcc",
    "Continuity/KolmogorovChentsov.lean": "ce2b9dc8fc18f083d3ebe86c5ef68bd3e8d4e2c1f1587d4fa7c6e503144578a9",
    "Continuity/KolmogorovChentsovInequality.lean": "502061001bd4c2244e3e69d7610aace1e759c0d26f78ada78ccb26e35a6fda51",
    "Gaussian/StochasticProcesses.lean": "c5fc98b72eb3044fe49add5b47ce10ec8a9aeb1e47aa11aa32a91a2e0c393f81",
}
PORT_NOTICE = "-- Modified locally only to namespace-qualify vendored BrownianMotion imports.\n\n"
VENDOR_PREFIX = "«Stage1_Instances».«THM-M-1083».Vendor."
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/Validation.lean",
    f"Stage1_Instances/{THEOREM}/check_obligation_tree.py",
    f"Stage1_Instances/{THEOREM}/check_validation.py",
    f"Stage1_Instances/{THEOREM}/check_validation.sh",
    f"Stage1_Instances/{THEOREM}/validation-phase.md",
    f"Stage1_Instances/{THEOREM}/validation-receipt.json",
    f"Stage1_Instances/{THEOREM}/validation-spec.json",
}
SUMMARY_LINES = (
    "PASS THM-M-1083 narrow validation",
    "PASS network-isolated trust-zero kernel replay: all 15 vendored modules, exact statement, frozen composition, proof root, and trust probe elaborated",
    "PASS hygiene: transitive placeholder collectors and a comment-stripped prohibited-construct scan passed",
    "PASS selected provenance: immutable upstream/local source manifests, license, clean mathlib pin, source/olean anchor, and tool identities agree",
    "FAIL CLOSED authority: proof master acceptance and alternate-route registry/typed-graph reconciliation remain open; planned instance stays H2/M4/R4",
    "FAIL CLOSED foundation/trust: M1083-S-FOUNDATION, accepted axiom policy, and complete transitive declaration/TCB/SBOM closure are absent",
    "FAIL CLOSED source/readability: primary-source H0, independent R0 review, and complete source-boundary coverage remain open",
    "FAIL CLOSED hermetic release: shared warm .lake is not a clean-checkout empty-cache offline-restorable replay or deterministic bundle",
    "FAIL CLOSED independent release: same-worker trust probe is not a distinct signed runner or independently implemented minimal verifier",
    "audit_complete=false; theorem_complete=false",
)


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict), path
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(argv: list[str], *, cwd: Path = ROOT, timeout: int = 1800) -> str:
    result = subprocess.run(
        argv,
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=timeout,
        check=False,
    )
    if result.returncode:
        raise RuntimeError(f"command failed ({result.returncode}): {argv!r}\n{result.stdout}")
    return result.stdout


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["git", *args], cwd=cwd, timeout=120).strip()


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


def assert_text_hygiene(path: Path) -> None:
    data = path.read_bytes()
    assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data, path
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines()), path


def upstream_bytes(source: str, adapted: bool) -> bytes:
    if adapted:
        assert source.count(PORT_NOTICE) == 1
        source = source.replace(PORT_NOTICE, "", 1)
        assert VENDOR_PREFIX in source
        source = source.replace(VENDOR_PREFIX, "")
    else:
        assert PORT_NOTICE not in source and VENDOR_PREFIX not in source
    return source.encode("utf-8")


def main(*, skip_kernel_replay: bool = False) -> None:
    if os.sys.flags.optimize:
        raise RuntimeError("Python optimization disables fail-closed assertions")

    spec = load(HERE / "validation-spec.json")
    receipt = load(HERE / "validation-receipt.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")
    targets = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    instance = load(HERE / "instance.json")
    local_dag = load(HERE / "task-dag.json")
    statement = load(HERE / "statement.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    proof_receipt = load(HERE / "proof-receipt.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 525 and target["baseline"] == "L0"
    assert target["lifecycle_mode"] == "planned"
    assert target["rework_required"] is True and target["theorem_complete"] is False
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item == {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 525,
        "phase": "validation",
        "layer": 5,
        "state": "[ ]",
        "depends_on": ["S56-M-1083-PROOF"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Run hermetic kernel, trust, provenance, and independent validation gates.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }
    predecessor = next(row for row in execution["items"] if row["id"] == "S56-M-1083-PROOF")
    assert predecessor["state"] == "[_]" and predecessor["attempts"] == 1
    local_task = next(row for row in local_dag["tasks"] if row["id"] == ITEM)
    assert local_task["state"] == "open" and local_task["depends_on"] == ["S56-M-1083-PROOF"]

    assert instance["root_vector"] == {"human": "H2", "machine": "M4", "readability": "R4"}
    assert instance["accepted_proof_state"] == []
    assert instance["audit_complete"] is instance["theorem_complete"] is False
    closure = graphs["closure_boundary"]
    assert closure["root_closed"] is False and closure["root_machine_debt"] == "M3"
    assert closure["closed_obligations"] == []
    assert closure["audit_complete"] is closure["theorem_complete"] is False

    for name, expected in EXPECTED_INPUTS.items():
        assert sha256(HERE / name) == expected, f"stale validation input: {name}"
        assert receipt["inputs"][name] == expected, f"receipt input drift: {name}"
    for name, expected in EXPECTED_TOOL_INPUTS.items():
        assert sha256(LEAN_ROOT / name) == expected, f"changed tool input: {name}"
        assert receipt["inputs"][name] == expected, f"receipt tool input drift: {name}"
    assert receipt["inputs"]["validator_sha256"] == sha256(Path(__file__))

    formal = statement["canonical_formal_target"]
    assert formal["declaration_or_expression"] == "Stage1Instances.THM_M_1083.Statement"
    assert formal["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert formal["statement_file_sha256"] == EXPECTED_INPUTS["Statement.lean"]
    assert registry["frozen_against_statement_sha256"] == EXPECTED_INPUTS["Statement.lean"]
    assert registry["denominator_sha256"] == graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256

    assert proof_receipt["canonical_target_expression_sha256"] == EXPRESSION_SHA256
    assert proof_receipt["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert proof_receipt["proof_body"]["source_sha256"] == EXPECTED_INPUTS["Proof.lean"]
    assert proof_receipt["proof_body"]["origin"]["revision"] == (
        "91885e6172648ea7f9c6a16b3a7069f92c88e023"
    )
    assert proof_receipt["proof_body"]["closure"]["lean_file_count"] == 15
    assert proof_receipt["accepted"] is False
    assert proof_receipt["accepted_closed_obligation_ids"] == []
    assert proof_receipt["exact_root_kernel_closed"] is True
    assert proof_receipt["exact_root_frozen_graph_closed"] is False
    assert proof_receipt["foundation_open_ids"] == ["M1083-S-FOUNDATION"]
    assert proof_receipt["result"]["axioms"] == ALLOWED_AXIOMS
    assert proof_receipt["result"]["accepted_root_closed"] is False
    assert proof_receipt["result"]["theorem_complete"] is False

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by|extern)\b|"
        r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
        r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
        r"(?:axiom|constant|opaque|unsafe)\b",
        re.MULTILINE,
    )
    lean_paths = [
        HERE / "Statement.lean",
        HERE / "ObligationTree.lean",
        HERE / "Proof.lean",
        HERE / "Validation.lean",
        *sorted((HERE / "Vendor/BrownianMotion").rglob("*.lean")),
    ]
    assert len(lean_paths) == 19
    for path in lean_paths:
        source = code_without_comments(path.read_text(encoding="utf-8"))
        if path.name == "Validation.lean":
            source = re.sub(r"^import Mathlib\.Util\.(?:AssertNoSorry|PrintSorries)$", "", source, flags=re.MULTILINE)
            source = re.sub(r"^\s*(?:assert_no_sorry|#print sorries)\b.*$", "", source, flags=re.MULTILINE)
        assert prohibited.search(source) is None, f"prohibited source construct in {path}"
    assert len(SOURCE_ROWS) == len(UPSTREAM_SOURCE_ROWS) == 15
    upstream_manifest = []
    adapted_manifest = []
    for relative, expected in SOURCE_ROWS.items():
        path = HERE / "Vendor/BrownianMotion" / relative
        assert sha256(path) == expected, relative
        reconstructed = upstream_bytes(
            path.read_text(encoding="utf-8"),
            expected != UPSTREAM_SOURCE_ROWS[relative],
        )
        assert hashlib.sha256(reconstructed).hexdigest() == UPSTREAM_SOURCE_ROWS[relative], relative
        upstream_manifest.append(f"{UPSTREAM_SOURCE_ROWS[relative]}  BrownianMotion/{relative}\n")
        adapted_manifest.append(f"{expected}  BrownianMotion/{relative}\n")
    assert hashlib.sha256("".join(upstream_manifest).encode()).hexdigest() == (
        "baeba6af6f09aad37899666edf987cba2f75f0ad4dd1740314c2357293f1210c"
    )
    assert hashlib.sha256("".join(adapted_manifest).encode()).hexdigest() == (
        "f43079ae9b6ae2745f57dc63cf07e9508a4532691a99b885bbaf26d33cc9b2aa"
    )

    manifest = load(LEAN_ROOT / "lake-manifest.json")
    mathlib_entry = next(row for row in manifest["packages"] if row["name"] == "mathlib")
    assert mathlib_entry["rev"] == mathlib_entry["inputRev"] == MATHLIB_REVISION
    assert MATHLIB.resolve().is_dir(), "pinned mathlib artifact unavailable"
    assert git("rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert git("remote", "get-url", "origin", cwd=MATHLIB) == MATHLIB_REMOTE
    assert git("status", "--porcelain=v1", cwd=MATHLIB) == ""
    anchor_source = MATHLIB / "Mathlib/Probability/Process/Kolmogorov.lean"
    anchor_olean = MATHLIB / ".lake/build/lib/lean/Mathlib/Probability/Process/Kolmogorov.olean"
    assert git("rev-parse", "HEAD:Mathlib/Probability/Process/Kolmogorov.lean", cwd=MATHLIB) == (
        "74d32fb5c4d8e325be00e090aa0ebdeb4ac7f127"
    )
    assert sha256(anchor_source) == "97f4062f1ebcfbd6fff897c6f95aadd3fe06ed7471874fb783b50ae14b785bde"
    assert sha256(anchor_olean) == "d13c0f13fca06ab0a05ab7bc725a66d95d290ce65311474d71da27ee69866d1b"
    assert sha256(MATHLIB / "LICENSE") == "b40930bbcf80744c86c46a12bc9da056641d722716c378f5659b9e555ef833e1"

    lean = Path(run(["lake", "env", "which", "lean"], cwd=LEAN_ROOT, timeout=120).strip())
    lake = Path(run(["lake", "env", "which", "lake"], cwd=LEAN_ROOT, timeout=120).strip())
    python = Path(os.path.realpath(os.sys.executable))
    git_path = shutil.which("git")
    bwrap_path = shutil.which("bwrap")
    assert git_path is not None and bwrap_path is not None
    assert LEAN_COMMIT in run([str(lean), "--version"], timeout=120)
    assert "5.0.0-src+98dc76e" in run([str(lake), "--version"], timeout=120)
    assert sha256(lean) == receipt["environment"]["lean_executable_sha256"]
    assert sha256(lake) == receipt["environment"]["lake_executable_sha256"]
    assert sha256(python) == receipt["environment"]["python_executable_sha256"]
    assert sha256(Path(os.path.realpath(git_path))) == receipt["environment"]["git_executable_sha256"]
    assert sha256(Path(os.path.realpath(bwrap_path))) == receipt["environment"]["bubblewrap_executable_sha256"]

    if skip_kernel_replay:
        assert receipt["output_evidence"]["runner_stdout_sha256"] == RUNNER_STDOUT_SHA256
    else:
        runner = run(["bash", str(HERE / "check_validation.sh")])
        assert runner.splitlines() == list(RUNNER_STDOUT)
        assert hashlib.sha256(runner.encode()).hexdigest() == RUNNER_STDOUT_SHA256

    assert spec["schema_version"] == "stage1-validation-recipe/1.0"
    assert spec["item_id"] == ITEM and spec["theorem_id"] == THEOREM
    assert spec["cwd"] == "."
    assert spec["argv"] == ["python3", "-B", f"Stage1_Instances/{THEOREM}/check_validation.py"]
    assert spec["env_allowlist"] == {} and spec["timeout_seconds"] == 1800
    assert spec["network_policy"] == "denied" and spec["expected_exit"] == 0
    assert "unshared network namespace" in spec["network_enforcement"]

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["phase"] == "validation" and receipt["intent"] == "validate"
    assert receipt["depends_on"] == ["S56-M-1083-PROOF"]
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["release_grade"] is receipt["content_addressed_release_evidence"] is False
    assert receipt["covered_obligation_ids"] == spec["covered_obligation_ids"]
    assert receipt["validated_declarations"] == spec["covered_declarations"]
    assert receipt["accepted_closed_obligation_ids"] == []
    assert receipt["canonical_target"] == {
        "declaration": "Stage1Instances.THM_M_1083.Statement",
        "elaborated_expression_sha256": EXPRESSION_SHA256,
        "registry_denominator_sha256": DENOMINATOR_SHA256,
    }
    assert receipt["result"]["network_isolated_lean_replay"] == "pass"
    assert receipt["result"]["observed_axioms"] == ALLOWED_AXIOMS
    assert receipt["result"]["accepted_root_closed"] is False
    assert receipt["result"]["audit_complete"] is receipt["result"]["theorem_complete"] is False
    assert receipt["root_vector_before"] == {"H": "H2", "M": "M4", "R": "R4"}
    assert receipt["root_vector_after_worker_selftest"] == receipt["root_vector_before"]
    assert receipt["first_failed_gate"] == "dependency.S56-M-1083-PROOF.master_acceptance"
    assert receipt["first_failed_release_gate"] == "S56-10.6-HERMETIC-COLD-BUILD"
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
    status = subprocess.check_output(
        ["git", "status", "--porcelain=v1", "-z", "--untracked-files=all"],
        cwd=ROOT,
    ).decode("utf-8")
    actual_changes = set()
    entries = status.split("\0")
    index = 0
    while index < len(entries) and entries[index]:
        entry = entries[index]
        code, path = entry[:2], entry[3:]
        if "R" in code or "C" in code:
            index += 1
        if path != "Formalizations/Lean/.lake":
            actual_changes.add(path)
        index += 1
    assert actual_changes == CHANGED_PATHS, (actual_changes, CHANGED_PATHS)
    for path in CHANGED_PATHS:
        assert_text_hygiene(ROOT / path)

    assert receipt["output_evidence"]["runner_stdout_sha256"] == RUNNER_STDOUT_SHA256
    print("\n".join(SUMMARY_LINES))


if __name__ == "__main__":
    if len(sys.argv) == 1:
        main()
    elif sys.argv == [sys.argv[0], "--skip-kernel-replay"]:
        main(skip_kernel_replay=True)
    else:
        raise SystemExit(f"usage: {sys.argv[0]} [--skip-kernel-replay]")
