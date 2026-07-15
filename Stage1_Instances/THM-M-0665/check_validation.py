#!/usr/bin/env python3
"""Fail-closed narrow validator for S56-M-0665-VALIDATION."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import pwd
import re
import shutil
import subprocess
import tempfile
import time


if not __debug__:
    raise SystemExit("validation requires Python assertions")

ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0665"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
ITEM = "S56-M-0665-VALIDATION"
THEOREM = "THM-M-0665"
BASE_REVISION = "443b8bbc23bf35a1e7a4bb7b3183073f76bbee2b"
BASE_TREE = "c5771c47c12b80aba613e6d844570f83b39ded6d"
LEAN_TOOLCHAIN = "leanprover/lean4:v4.29.0"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
LEAN_SHA256 = "3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf"
LAKE_SHA256 = "a608ff084d7e2af228b92a29d7c2fd083ba0580e46889175ec74a81678c98359"
BWRAP_SHA256 = "0abea81db798ebf6b4742ac0664802d97521547a353c2a0dbdc21d76cbbfd2c0"
PYTHON_SHA256 = "b8d8288faefdd300201f43fcf00f6f539a27218eeed3a3dff5ab10b9c4c99700"
TOOLCHAIN_SHA256 = "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2"
MANIFEST_SHA256 = "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MATHLIB_REMOTE = "https://github.com/leanprover-community/mathlib4.git"
MATHLIB_LICENSE_SHA256 = "b40930bbcf80744c86c46a12bc9da056641d722716c378f5659b9e555ef833e1"
STATEMENT_EXPRESSION_SHA256 = (
    "da66c715ce12af9ff6dfb55a721665c8240358c0ee547062b3d2fc10c7785944"
)
REGISTRY_DENOMINATOR_SHA256 = (
    "9aa4a6fe979874ca4baa46f7f6b12d9dd965206a2d05614e70330640ac4303e5"
)
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
PROOF_DECLARATIONS = (
    "subset_algebraicPart_of_semialgebraic_preconnected_nontrivial",
    "algebraicPart_subset",
    "algebraicPart_mono",
    "normalizedRatPair_injective",
    "finite_int_natAbs_le",
    "finite_rat_height_le",
    "finite_point_height_le",
    "finite_transcendentalRationalPoints",
    "ncard_transcendentalRationalPoints_le_height_slice",
    "countingConclusion_zero_dimensional",
    "pilaWilkie_zero_dimensional",
    "countingConclusion_of_diff_eq_empty",
    "countingConclusion_of_semialgebraic_preconnected_nontrivial",
    "countingConclusion_empty",
)
VALIDATION_DECLARATIONS = (
    "algebraicPart_subset",
    "normalized_components_bounded",
    "zero_dimensional_height",
)
PARTIAL_IDS = [
    "M0665-N-ALGEBRAIC",
    "M0665-N-HEIGHT",
    "M0665-S-BOUNDARY",
    "M0665-B-DIMENSION",
    "M0665-L-COUNT",
]
REMAINING_CUT = [
    "M0665-C-PARAM",
    "M0665-L-DERIVATIVE",
    "M0665-L-ARITHMETIC",
    "M0665-L-DROP",
    "M0665-L-COUNT",
]
INPUT_HASHES = {
    "Statement.lean": "856703261f1e12c4dd91f209bb001cb7b1a5512770117a5f4527a4804439a175",
    "Proof.lean": "27e92adba1ca818a9e0442661c34c9adc4115653ac9a593fa8057fc18d0a6d07",
    "statement.json": "171e9bedcb4e6b0a274265e5168e88bdc2c1d269406b6e26dbba55c7acf17d33",
    "anchor-audit.json": "80aa453d71ead0d5385bd5db51fa9434facca89bbb40edb35e7b5308be8c9b69",
    "obligation-registry.json": "9970f070b8590a04767a90697c5f642665e49c35284d99ea854f9fbe24d6c7c4",
    "typed-graphs.json": "80cef15dbfcad6f83047e49e70a2fc92cbc173ed2c9fdbb199ee88740a7c93fe",
    "validation-specs.json": "18f73ade70df146ed7866075ce026a74176698c9820ceb98ece099d502b0cce3",
    "proof-receipt.json": "b5347fc4202a439512ee721e8d70c6c0f289bfc881ad3e8f5b3123754a021231",
    "proof-blocker.json": "c00159b709a114173d78fd2cfe0221b3f82a3a8b09ebfed8001875d6776e3f20",
    "source-statement-crosswalk.md": "218aba29acb99d6f6ef292aca5e6e61acd527759f0c44c83b6372da08a581fe1",
    "check_obligation_tree.py": "dd6b1857e9332f16bde32e6f58774dc62a9eb287acdfb47c707d3b4fae83fb67",
}
DIRECT_IMPORTS = {
    "Mathlib/Analysis/SpecialFunctions/Pow/Real.lean": {
        "source": "4bc70fd7fa295428b59e9d5de98650a98eb4e87f6614d42f5d5d55ccc9d33398",
        "blob": "d33cde833bb5b015daa4c059f024e87987ddc149",
        "olean": "d161223f24657bf0321ea05c65e5012d00a9fc634da7113b220c710d62c1d3f4",
    },
    "Mathlib/Data/Set/Card.lean": {
        "source": "09942e2b66a4dfafd949dc32da33c41d3ada901769fda4ceb1f7e06dc8b0b5f5",
        "blob": "1ca79eb8302a1a2ba01d994973a135386712af62",
        "olean": "f9c99acb0b77cbe736df02464b0f2349f57ff5efe638fcd53a7b454e4472b62d",
    },
    "Mathlib/ModelTheory/Algebra/Field/Basic.lean": {
        "source": "ddb9e4b25602b0d692608bed56fa003d74e379bc25420921c326dcbc101397b4",
        "blob": "328f6c840fac7f2cf7496748656f700734e53921",
        "olean": "cf03449f2ee8d6497697c82e895595d8a0eda1e511dc073da5c6e25115374af9",
    },
    "Mathlib/ModelTheory/Definability.lean": {
        "source": "d054402a493cad6d8173abef22f5571a5e02bbb8c1a24abff119918bed0c444c",
        "blob": "054d4b5093c13851d8eac02c56881b6303952837",
        "olean": "3c3ff44bbb4c411644fe0f529a9adb338d9f04015f04691ee61774ac8d3a0a5b",
    },
    "Mathlib/Topology/Closure.lean": {
        "source": "19911cf0e1231c924d154956e7b4454532eada84369fc1ca9722e38c78444b17",
        "blob": "2c498c2afa91c4fb9976a92fb17cdf25088e1ed8",
        "olean": "beefdce7057a5db3af9c7a6914d0ddfe378b42a4804e905f5f8b7d0cfbacda50",
    },
    "Mathlib/Topology/Separation/Connected.lean": {
        "source": "6a69593a4250970a030cae723adecfefb6ccd3edf5bb2a8c508632e75bfb678c",
        "blob": "a26683d2aece625b8ab6c4c1edb93987d406394f",
        "olean": "ef41e189b59603053ccf1806bc1558dd7b7bd7ed40c17fcaa4e00aec2191b5e6",
    },
}
RECIPE_ARGV = [
    "/usr/bin/bwrap", "--ro-bind", "/", "/", "--dev", "/dev",
    "--proc", "/proc", "--tmpfs", "/tmp", "--unshare-net",
    "--die-with-parent", "--clearenv", "--setenv", "HOME", "/tmp",
    "--setenv", "PATH", "/usr/bin:/bin", "--setenv", "LANG", "C.UTF-8",
    "--setenv", "LC_ALL", "C.UTF-8", "--setenv", "TZ", "UTC",
    "--setenv", "LEAN_NUM_THREADS", "1", "/usr/bin/python3", "-I", "-B",
    f"Stage1_Instances/{THEOREM}/check_validation.py",
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
    "PASS THM-M-0665 narrow validation",
    "PASS network-isolated trust-zero fresh-output replay of Statement, Proof, and Validation",
    "PASS 14 partial proof declarations and 3 differential declarations are sorry-free",
    "PASS observed axioms are contained in propext, Classical.choice, and Quot.sound",
    "PASS frozen hashes, proof receipt binding, clean mathlib pin, and direct-import provenance",
    "OPEN exact root at M3: no unconditional Stage1Instances.THM_M_0665.PilaWilkie body",
    "FAIL CLOSED authority, complete trust/provenance, cold hermetic, and distinct-runner gates",
    "audit_complete=false; theorem_complete=false",
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


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


def run(argv: list[str], *, cwd: Path = ROOT,
        env: dict[str, str] | None = None, timeout: int = 600) -> str:
    result = subprocess.run(
        argv, cwd=cwd, env=env, text=True, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, timeout=timeout, check=False,
    )
    if result.returncode:
        raise RuntimeError(f"command failed ({result.returncode}): {argv!r}\n{result.stdout}")
    return result.stdout


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["git", *args], cwd=cwd, timeout=60).strip()


def source_without_comments(source: str) -> str:
    output: list[str] = []
    index = 0
    depth = 0
    in_string = False
    escaped = False
    while index < len(source):
        pair = source[index:index + 2]
        char = source[index]
        if depth:
            if pair == "/-":
                depth += 1
                index += 2
            elif pair == "-/":
                depth -= 1
                index += 2
            else:
                if char == "\n":
                    output.append("\n")
                index += 1
        elif in_string:
            output.append(char)
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
            index += 1
        elif pair == "/-":
            depth = 1
            index += 2
        elif pair == "--":
            newline = source.find("\n", index + 2)
            if newline < 0:
                break
            output.append("\n")
            index = newline + 1
        else:
            output.append(char)
            if char == '"':
                in_string = True
            index += 1
    assert depth == 0 and not in_string, "unterminated Lean comment or string"
    return "".join(output)


def reported_axioms(output: str, declaration: str) -> set[str]:
    pattern = re.compile(
        re.escape(f"'{declaration}' depends on axioms: [") + r"(.*?)]",
        re.DOTALL,
    )
    matches = pattern.findall(output)
    no_axioms = output.count(f"'{declaration}' does not depend on any axioms")
    assert len(matches) + no_axioms == 1, declaration
    if not matches:
        return set()
    return {part.strip() for part in matches[0].split(",") if part.strip()}


def assert_hygiene(path: Path) -> None:
    data = path.read_bytes()
    assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines()), path


def main() -> None:
    started = time.monotonic()
    os.umask(0o022)
    os.environ.update({"LANG": "C.UTF-8", "LC_ALL": "C.UTF-8", "TZ": "UTC"})

    spec = load(HERE / "validation-spec.json")
    statement = load(HERE / "statement.json")
    anchor = load(HERE / "anchor-audit.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    proof_receipt = load(HERE / "proof-receipt.json")
    proof_blocker = load(HERE / "proof-blocker.json")
    execution = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item == {
        "id": ITEM, "theorem_id": THEOREM, "execution_rank": 709,
        "phase": "validation", "layer": 5, "state": "[ ]",
        "depends_on": ["S56-M-0665-PROOF"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Run hermetic kernel, trust, provenance, and independent validation gates.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0, "children": [],
    }
    predecessor = next(row for row in execution["items"] if row["id"] == "S56-M-0665-PROOF")
    assert predecessor["state"] == "[_]" and predecessor["attempts"] == 1

    assert spec["schema_version"] == "stage1-validation-spec/1.0"
    assert spec["item_id"] == ITEM and spec["theorem_id"] == THEOREM
    assert spec["argv"] == RECIPE_ARGV and spec["cwd"] == "."
    assert spec["timeout_seconds"] == 600 and spec["network_policy"] == "denied"
    assert spec["expected_exit"] == 0
    assert set(spec["partially_covered_obligation_ids"]) == set(PARTIAL_IDS)

    for name, expected in INPUT_HASHES.items():
        assert sha256(HERE / name) == expected, f"stale validation input: {name}"
    formal = statement["canonical_formal_target"]
    assert formal["declaration_or_expression"] == "Stage1Instances.THM_M_0665.PilaWilkie"
    assert formal["statement_file_sha256"] == INPUT_HASHES["Statement.lean"]
    assert formal["elaborated_expression_sha256"] == STATEMENT_EXPRESSION_SHA256
    assert anchor["canonical_declaration"] == formal["declaration_or_expression"]
    assert anchor["repo_local"]["exact_closure_found"] is False
    assert registry["root_obligation_id"] == "M0665-ROOT"
    assert registry["denominator_sha256"] == REGISTRY_DENOMINATOR_SHA256
    assert graphs["registry_denominator_sha256"] == REGISTRY_DENOMINATOR_SHA256
    assert len(registry["obligations"]) == 20
    closure = graphs["closure_boundary"]
    assert closure["closed_obligations"] == []
    assert closure["root_closed"] is False and closure["root_machine_debt"] == "M3"
    assert closure["remaining_root_cut_set"] == REMAINING_CUT
    assert closure["composition_certificates_checked"] == []
    assert closure["audit_complete"] is closure["theorem_complete"] is False

    assert proof_receipt["support_state"] == "provisional_worker_selftest"
    assert proof_receipt["accepted"] is False and proof_receipt["proposed_state"] == "[_]"
    assert proof_receipt["proof_body"]["source_sha256"] == sha256(HERE / "Proof.lean")
    assert proof_receipt["provisionally_closed_obligation_ids"] == []
    assert proof_receipt["partial_progress_toward_obligation_ids"] == PARTIAL_IDS
    assert proof_receipt["accepted_closed_obligation_ids"] == []
    assert proof_receipt["result"]["root_kernel_closed"] is False
    assert proof_receipt["result"]["theorem_complete"] is False
    assert proof_receipt["remaining_root_cut_set"] == REMAINING_CUT
    assert proof_blocker["partial_proof_receipt_id"] == proof_receipt["receipt_id"]
    assert proof_blocker["proof_file_sha256"] == sha256(HERE / "Proof.lean")
    assert proof_blocker["root_closed"] is proof_blocker["theorem_complete"] is False

    all_source = "\n".join(
        source_without_comments((HERE / name).read_text(encoding="utf-8"))
        for name in ("Statement.lean", "Proof.lean", "Validation.lean")
    )
    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by|run_tac)\b|"
        r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
        r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
        r"(?:axiom|constant|opaque|unsafe|extern)\b",
        re.MULTILINE,
    )
    assert prohibited.search(all_source) is None
    validation_imports = (HERE / "Validation.lean").read_text(encoding="utf-8").split("/-!", 1)[0]
    assert "import Proof" not in validation_imports
    assert "theorem pilaWilkie : PilaWilkie" not in all_source

    assert sha256(LEAN_ROOT / "lean-toolchain") == TOOLCHAIN_SHA256
    assert sha256(LEAN_ROOT / "lake-manifest.json") == MANIFEST_SHA256
    manifest = load(LEAN_ROOT / "lake-manifest.json")
    mathlib_entry = next(row for row in manifest["packages"] if row["name"] == "mathlib")
    assert mathlib_entry["rev"] == mathlib_entry["inputRev"] == MATHLIB_REVISION
    mathlib = LEAN_ROOT / ".lake" / "packages" / "mathlib"
    assert mathlib.resolve().is_dir(), "pinned mathlib artifact is unavailable"
    assert git("rev-parse", "HEAD", cwd=mathlib) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == MATHLIB_TREE
    assert git("remote", "get-url", "origin", cwd=mathlib) == MATHLIB_REMOTE
    assert git("status", "--porcelain=v1", "--untracked-files=all", cwd=mathlib) == ""
    assert sha256(mathlib / "LICENSE") == MATHLIB_LICENSE_SHA256
    for relative, expected in DIRECT_IMPORTS.items():
        source = mathlib / relative
        olean = mathlib / ".lake/build/lib/lean" / Path(relative).with_suffix(".olean")
        assert sha256(source) == expected["source"]
        assert git("hash-object", relative, cwd=mathlib) == expected["blob"]
        assert sha256(olean) == expected["olean"]

    account_home = Path(pwd.getpwuid(os.getuid()).pw_dir)
    toolchain_bin = account_home / ".elan/toolchains/leanprover--lean4---v4.29.0/bin"
    lean = toolchain_bin / "lean"
    lake = toolchain_bin / "lake"
    bwrap = Path("/usr/bin/bwrap")
    python = Path("/usr/bin/python3")
    assert sha256(lean) == LEAN_SHA256 and sha256(lake) == LAKE_SHA256
    assert sha256(bwrap) == BWRAP_SHA256 and sha256(python) == PYTHON_SHA256
    fixed_env = {
        "HOME": os.environ["HOME"],
        "PATH": f"{toolchain_bin}:/usr/bin:/bin",
        "ELAN_TOOLCHAIN": LEAN_TOOLCHAIN,
        "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8", "TZ": "UTC",
        "LEAN_NUM_THREADS": "1",
    }
    assert LEAN_COMMIT in run([str(lean), "--version"], cwd=LEAN_ROOT, env=fixed_env)
    # Lake cannot resolve the separately pinned flt-regular checkout because
    # its shared artifact is absent. Ask Lake from the clean pinned mathlib
    # checkout, then replace its nested dependency paths with the equivalent
    # complete top-level shared outputs. Nothing is repaired or fetched.
    dependency_outputs = [
        LEAN_ROOT / ".lake/packages" / name / ".lake/build/lib/lean"
        for name in (
            "batteries", "Qq", "aesop", "plausible", "LeanSearchClient",
            "proofwidgets", "importGraph", "mathlib",
        )
    ]
    assert all(path.is_dir() for path in dependency_outputs)
    discovered_path = run(
        [str(lake), "env", "printenv", "LEAN_PATH"], cwd=mathlib, env=fixed_env
    ).strip()
    discovered_entries = discovered_path.split(":")
    mathlib_output = mathlib / ".lake/build/lib/lean"
    assert mathlib_output.is_dir()
    lean_path = ":".join(
        [str(path) for path in dependency_outputs]
        + [str(mathlib_output)]
        + [entry for entry in discovered_entries if entry.endswith("/.elan/toolchains/leanprover--lean4---v4.29.0/lib/lean")]
    )

    tmp = Path(tempfile.mkdtemp(prefix="stage1-m0665-validation-", dir="/tmp"))
    try:
        for name in ("Statement.lean", "Proof.lean", "Validation.lean"):
            shutil.copy2(HERE / name, tmp / name)
        (tmp / "home").mkdir()

        def isolated_lean(args: list[str], *, module_path: bool = False) -> str:
            env = dict(fixed_env)
            env["HOME"] = str(tmp / "home")
            env["LEAN_PATH"] = f"{tmp}:{lean_path}" if module_path else lean_path
            return run(
                [str(lake), "env", "lean", "--trust=0", "-t0", "-j1",
                 "--root", str(tmp), *args],
                cwd=tmp, env=env, timeout=max(60, 600 - int(time.monotonic() - started)),
            )

        statement_output = isolated_lean(["-o", "Statement.olean", "Statement.lean"])
        proof_output = isolated_lean(["-o", "Proof.olean", "Proof.lean"], module_path=True)
        validation_output = isolated_lean(["Validation.lean"], module_path=True)
    finally:
        shutil.rmtree(tmp)

    observed_axioms: set[str] = set()
    for short_name in PROOF_DECLARATIONS:
        declaration = "Stage1Instances.THM_M_0665.Proof." + short_name
        axioms = reported_axioms(proof_output, declaration)
        assert axioms <= EXPECTED_AXIOMS, (declaration, axioms)
        observed_axioms.update(axioms)
    for short_name in VALIDATION_DECLARATIONS:
        declaration = "Stage1Instances.THM_M_0665.Validation." + short_name
        axioms = reported_axioms(validation_output, declaration)
        assert axioms <= EXPECTED_AXIOMS, (declaration, axioms)
        observed_axioms.update(axioms)
    assert proof_output.count("Declarations are sorry-free!") == len(PROOF_DECLARATIONS)
    assert validation_output.count("Declarations are sorry-free!") == len(VALIDATION_DECLARATIONS)
    combined = "\n".join((statement_output, proof_output, validation_output))
    assert "sorryAx" not in combined and "declaration uses 'sorry'" not in combined
    assert "error:" not in combined

    receipt_path = HERE / "validation-receipt.json"
    if receipt_path.exists():
        receipt = load(receipt_path)
        assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
        assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
        assert receipt["support_state"] == "provisional_worker_selftest"
        assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
        assert receipt["release_grade"] is False and receipt["verdict"] == "blocked"
        assert receipt["canonical_target_expression_sha256"] == STATEMENT_EXPRESSION_SHA256
        assert receipt["registry_denominator_sha256"] == REGISTRY_DENOMINATOR_SHA256
        assert receipt["inputs"]["validation_probe_sha256"] == sha256(HERE / "Validation.lean")
        assert receipt["inputs"]["validation_spec_sha256"] == sha256(HERE / "validation-spec.json")
        assert receipt["inputs"]["validator_sha256"] == sha256(Path(__file__))
        assert receipt["result"]["observed_axioms"] == sorted(observed_axioms)
        assert receipt["result"]["provisionally_closed_obligation_ids"] == []
        assert receipt["result"]["validated_partial_progress_ids"] == PARTIAL_IDS
        assert receipt["result"]["accepted_closed_obligation_ids"] == []
        assert receipt["result"]["root_kernel_closed"] is False
        assert receipt["result"]["root_closed"] is False
        assert receipt["result"]["theorem_complete"] is False
        assert receipt["remaining_root_cut_set"] == REMAINING_CUT
        assert receipt["trust"]["accepted_foundation_profile"] is False
        assert receipt["trust"]["complete_transitive_trust_closure"] is False
        assert receipt["provenance"]["root_provenance_closure"] == "open"
        assert receipt["hermeticity"]["fresh_clean_checkout"] is False
        assert receipt["hermeticity"]["cold_dependency_rebuild"] is False
        assert receipt["independent_validation"]["distinct_verifier_identity"] is False
        assert receipt["independent_validation"]["second_signed_attestation"] is False
        assert set(receipt["changed_paths"]) == CHANGED_PATHS
        assert receipt["evidence_log"]["semantic_sha256"] == hashlib.sha256(
            ("\n".join(SUMMARY_LINES) + "\n").encode()
        ).hexdigest()

    packet_path = ROOT / ".stage1-worker-selftest.json"
    if packet_path.exists():
        packet = load(packet_path)
        assert set(packet) == {
            "item_id", "changed_paths", "commands", "output_summary",
            "base_revision", "known_failures", "state",
        }
        assert packet["item_id"] == ITEM and packet["state"] == "[_]"
        assert packet["base_revision"] == BASE_REVISION
        assert set(packet["changed_paths"]) == CHANGED_PATHS
        if receipt_path.exists():
            assert packet["known_failures"] == load(receipt_path)["known_failures"]
        actual = {
            line[3:] for line in git("status", "--short", "--untracked-files=all").splitlines()
            if line[3:] != "Formalizations/Lean/.lake"
        }
        assert actual == CHANGED_PATHS, (actual, CHANGED_PATHS)

    for relative in CHANGED_PATHS - {".stage1-worker-selftest.json"}:
        if (ROOT / relative).exists():
            assert_hygiene(ROOT / relative)
    for line in SUMMARY_LINES:
        print(line)


if __name__ == "__main__":
    main()
