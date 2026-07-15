#!/usr/bin/env python3
"""Fail-closed narrow validator for S56-M-0072-VALIDATION."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile


if not __debug__:
    raise SystemExit("check_validation.py requires Python assertions")


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0072"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM = "S56-M-0072-VALIDATION"
THEOREM = "THM-M-0072"
BASE_REVISION = "97cd9c492d95baa9b55d2d8b341844107f07e686"
BASE_TREE = "bdd31de5f2fcd38078e4b5793b400a8105a3b8ba"
TOOLCHAIN = "leanprover/lean4:v4.29.0"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
LEAN_SHA256 = "3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf"
LAKE_SHA256 = "a608ff084d7e2af228b92a29d7c2fd083ba0580e46889175ec74a81678c98359"
PYTHON_SHA256 = "b8d8288faefdd300201f43fcf00f6f539a27218eeed3a3dff5ab10b9c4c99700"
GIT_SHA256 = "5516c9f362c29376ab9a499a33082f9f611941d8c75930c880e30ad109e39c9a"
BWRAP_SHA256 = "0abea81db798ebf6b4742ac0664802d97521547a353c2a0dbdc21d76cbbfd2c0"
ELAN_LAKE_SHA256 = "840179e70803ef373c2ec53342d6a45ea7d022533e4145489fc1278b4f716385"
TOOLCHAIN_SHA256 = "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2"
MANIFEST_SHA256 = "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MATHLIB_REMOTE = "https://github.com/leanprover-community/mathlib4.git"
MATHLIB_LICENSE_SHA256 = "b40930bbcf80744c86c46a12bc9da056641d722716c378f5659b9e555ef833e1"
EXPRESSION_SHA256 = "c8a89538bd8b492ba31ce5d516a0f8fefef70a550e1d2fe74e39a4cba7849051"
DENOMINATOR_SHA256 = "7f5030b02a13572f021c17ac32f2472098e2a5de881bc5a4999716dd411f717b"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
EXPECTED_AXIOM_LIST = ["propext", "Classical.choice", "Quot.sound"]
EXPECTED_INPUTS = {
    "Statement.lean": "0e9a35c7d2a9eaafb2aa6f8357277e9bf1e79e9a5e88500bda6cd8300a6757aa",
    "ObligationTree.lean": "e30e9833e607eea7a9dd025e86cd6f34a912ed375c0563186c0727424dcb838c",
    "Proof.lean": "549f8b496b79d82071a93eb95a8e6809dd3afefcb7ee60392a8642fd6749ebc2",
    "statement.json": "ab2ab89125e95ced56ed588c965b03a283596dd6fb815f967bf9bb91114d1034",
    "anchor-audit.json": "9124610a2becf3f4a5ff4972f9280235ad8217d10a79971ccddd5dbdf23bc6fd",
    "obligation-registry.json": "6e60eb6599e9fded2c5ce5100b469faedd20eaa83840917c6e979b5af12f2498",
    "typed-graphs.json": "d307d8c606150999add6b0e068510dcc70c2ddaa8945c944e1ed9f9980e67b8a",
    "validation-specs.json": "b542c4abffa013978e1609051b9477df078d67022af0493f66d5ed5b464c142c",
    "proof-receipt.json": "b7c3c02e977540f8f5279ec5a75b5f9a082ab8bfd970bcb88520eab7d8b8b399",
    "instance.json": "d54c99adc532922ee41821cb3a1a97fbb55980f0087e04bc715d56b86e36a5ba",
    "task-dag.json": "0d838c49048bfb919104e544e147e419ba6fdf5047d61afb0da94cc51c531735",
    "source-statement-crosswalk.md": "fdb7992feb445b6000a591680aa20ae4a80d934305e5e569fb625e4c2747b2fd",
    "Validation.lean": "1bf98acd7715b9efb10d97fb48bc36dd2cd4180ed9d86ea0b6ff896c274a987b",
    "validation-spec.json": "a45eb72a368c55b36666b75f2f2f75e09970e2316bca866f908114b9a642c356",
}
POLICY_INPUTS = {
    "Docs/Stage1_Blueprint_rev-5.6.md": "831954e3dc1d03089c6e867ef720bda39e378be0a84715304680a71b04efba91",
    "Docs/Stage1_Execution_DAG_rev-5.6.json": "52512cc81e0a1fa9348088aeb8085f26fc184a17b19fdc9f6de663079df78f72",
    "Docs/Stage1_Targets_rev-5.6.json": "02eec284de534dd78e1cf75f82a477ff477567dd682b7445cb7587abd137ab2c",
    "skills/execute-stage1-rev56/SKILL.md": "26d47a66c6535feabb8bbf1051fd55d76a53fe761f4b3d953f86b97ec86152b8",
}
SOURCE_BOUNDARIES = {
    "Mathlib/GroupTheory/Transfer.lean": {
        "blob": "1b85149e1029db4df4989249077bc1c18b383c1d",
        "source_sha256": "36b42d3505db3e7dd2af186b8749f9389a994790700ad048030bfa3e5e350889",
        "olean_sha256": "08b808d27cd2211125c3541e66597dac6fc97b1d8d1e334b482a81250f8b042a",
        "olean_bytes": 229120,
    },
    "Mathlib/GroupTheory/Nilpotent.lean": {
        "blob": "953716bcd3ccd93f561d039ff4db093f311e040f",
        "source_sha256": "0a44d6105ae941b99ed6c1dfa68ae96cc8d4039add5da445b4edcb723c4cefb5",
        "olean_sha256": "f467def05946b930d2cdf65bfe784569986deb0ea3ae57621536bd4e0f73f621",
        "olean_bytes": 262184,
    },
    "Mathlib/GroupTheory/IndexNormal.lean": {
        "blob": "15d5a65affcf7eca86d107dafcdfc8083f98c8d9",
        "source_sha256": "06ed89f82b46e8c79385136c686904fda38f1f50114b14d97c6ad37bdb2fe0f1",
        "olean_sha256": "26f0d780d46def5eea2580b56fa2029e04b5be41d83e861f7ea50e191b363acc",
        "olean_bytes": 8176,
    },
    "Mathlib/GroupTheory/GroupAction/Period.lean": {
        "blob": "bc7e49470ee2b65fd95d47575c02febfd604f537",
        "source_sha256": "b5ead3699b586fdde3d03deabff500efd9a58e49d2069d0a294c0b57a2c4dc0d",
        "olean_sha256": "e0f80b79c03f3e396e52a335e24046a705fa311e4e28a052944284c7ca601ff1",
        "olean_bytes": 52824,
    },
    "Mathlib/GroupTheory/Sylow.lean": {
        "blob": "363af2e4b7484f49f8eb300a12d0ef2a34812da4",
        "source_sha256": "065f21a50a881e60f2353ebc1fb9b75b6afe88faeab891883af07bcae93754a6",
        "olean_sha256": "935d6318091fa6885ae6c204cde68353464ea6319d856a7f9b7d5d8fc575ba01",
        "olean_bytes": 398200,
    },
}
PROOF_IDS = [
    "M0072-ROOT", "M0072-N-OUTSIDE", "M0072-B-MEMBERSHIP",
    "M0072-T-INSIDE", "M0072-C-NORMAL", "M0072-L-INDEX-TWO",
    "M0072-C-QUOTIENT", "M0072-C-TRANSFER", "M0072-L-SYLOW-ODD",
    "M0072-C-COSET-ACTION", "M0072-L-FIXED-PARITY",
    "M0072-L-TRANSFER-FORMULA", "M0072-L-FACTOR-DICHOTOMY",
    "M0072-L-ODD-PRODUCT", "M0072-L-NOINDEX-TRANSFER",
    "M0072-B-CONTRADICTION", "M0072-T-OUTSIDE", "M0072-T-ASSEMBLE",
]
COVERED_IDS = PROOF_IDS + ["M0072-X-PROVENANCE", "M0072-X-TRUST"]
PROOF_DECLARATIONS = (
    "Stage1Instances.THM_M_0072.ObligationTree.insideMaximalConclusion",
    "Stage1Instances.THM_M_0072.ObligationTree.assembly_of_outside_and_inside",
    "Stage1Instances.THM_M_0072.ObligationTree.root_of_assembly",
    "Stage1Instances.THM_M_0072.ObligationTree.root_of_outsideTransfer",
    "Stage1Instances.THM_M_0072.Proof.maximal_normal_of_pgroup",
    "Stage1Instances.THM_M_0072.Proof.quotient_isSimpleGroup_of_isCoatom",
    "Stage1Instances.THM_M_0072.Proof.maximal_index_prime_of_pgroup",
    "Stage1Instances.THM_M_0072.Proof.maximal_index_two_of_2group",
    "Stage1Instances.THM_M_0072.Proof.period_eq_one_or_two",
    "Stage1Instances.THM_M_0072.Proof.quotient_eq_of_both_not_mem",
    "Stage1Instances.THM_M_0072.Proof.outsideTransferConclusion",
    "Stage1Instances.THM_M_0072.Proof.thompsonTransferLemma_proof",
)
VALIDATION_DECLARATIONS = (
    "Stage1Instances.THM_M_0072.Validation.exactOutsideReplay",
    "Stage1Instances.THM_M_0072.Validation.exactRootReplay",
)
CHANGED_PATHS = [
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/Validation.lean",
    f"Stage1_Instances/{THEOREM}/check_validation.py",
    f"Stage1_Instances/{THEOREM}/validation-phase.md",
    f"Stage1_Instances/{THEOREM}/validation-receipt.json",
    f"Stage1_Instances/{THEOREM}/validation-spec.json",
]
PACKET_COMMANDS = [
    "python3 Docs/tools/check_stage1_standard.py",
    "python3 scripts/stage1_target.py check",
    "python3 scripts/stage1_target.py show THM-M-0072",
    "python3 -I -B Stage1_Instances/THM-M-0072/check_validation.py --probe",
    "python3 -I -B Stage1_Instances/THM-M-0072/check_validation.py --worker-packet .stage1-worker-selftest.json",
    "python3 -m json.tool Stage1_Instances/THM-M-0072/validation-spec.json",
    "python3 -m json.tool Stage1_Instances/THM-M-0072/validation-receipt.json",
    "python3 -m json.tool .stage1-worker-selftest.json",
    "PYTHONPYCACHEPREFIX=/tmp/stage1-m0072-validation-pycache python3 -m py_compile Stage1_Instances/THM-M-0072/check_validation.py",
    "git diff --check -- Stage1_Instances/THM-M-0072 .stage1-worker-selftest.json",
]
PACKET_OUTPUT_SUMMARY = (
    "Network-isolated trust-zero fresh-output replay passed for the exact statement, "
    "frozen composition, repo-local proof root, and two exact-type aliases. Fourteen "
    "declarations were sorry-free and used only propext, Classical.choice, and Quot.sound; "
    "a 13337-declaration/513-module walk found no unexpected bodyless or unsafe declaration, "
    "and selected direct pinned provenance matched. Proof master acceptance, complete "
    "trust/provenance, cold hermetic replay, distinct-runner independence, AUDIT-Z, "
    "THEOREM-Z, and theorem completion remain fail-closed."
)
SUMMARY_LINES = [
    "PASS THM-M-0072 narrow validation",
    "PASS network-isolated kernel replay: exact statement, frozen composition, proof root, and exact-type validation aliases elaborated at trust zero",
    "PASS trust observation: fourteen declarations are sorry-free and report exactly propext, Classical.choice, and Quot.sound; closure has no unexpected bodyless or unsafe declaration",
    "PASS selected provenance: frozen inputs, local proof-body location, five direct mathlib source/olean boundaries, clean pin, license, and tool identities agree",
    "FAIL CLOSED authority: proof is worker-self-tested but not master-accepted; authoritative instance and graph remain planned pre-proof H1/M3/R4",
    "FAIL CLOSED foundation/trust: the observed axiom ceiling is not an accepted profile and complete transitive TCB provenance remains open",
    "FAIL CLOSED hermetic release: shared warm .lake is not a clean-checkout empty-cache cold build, offline restoration, or deterministic TCB/SBOM bundle",
    "FAIL CLOSED independent release: exact-type aliases share this worker, checkout, proof body, kernel, and cache; no distinct signed verifier exists",
    "audit_complete=false; theorem_complete=false",
]


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


def run(
    argv: list[str], *, cwd: Path = ROOT, env: dict[str, str] | None = None,
    timeout: int = 600,
) -> str:
    result = subprocess.run(
        argv, cwd=cwd, env=env, text=True, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, timeout=timeout, check=False,
    )
    if result.returncode:
        raise RuntimeError(f"command failed ({result.returncode}): {argv!r}\n{result.stdout}")
    return result.stdout


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["/usr/bin/git", *args], cwd=cwd, env=BASE_ENV).strip()


def source_without_comments_and_strings(source: str) -> str:
    """Erase nested Lean comments, line comments, and strings for lexical defense."""
    output: list[str] = []
    index = 0
    depth = 0
    in_string = False
    while index < len(source):
        pair = source[index:index + 2]
        char = source[index]
        if depth:
            if pair == "/-":
                depth += 1
                output.extend("  ")
                index += 2
            elif pair == "-/":
                depth -= 1
                output.extend("  ")
                index += 2
            else:
                output.append("\n" if char == "\n" else " ")
                index += 1
        elif in_string:
            if char == "\\" and index + 1 < len(source):
                output.extend("  ")
                index += 2
            elif char == '"':
                in_string = False
                output.append(" ")
                index += 1
            else:
                output.append("\n" if char == "\n" else " ")
                index += 1
        elif pair == "/-":
            depth = 1
            output.extend("  ")
            index += 2
        elif pair == "--":
            while index < len(source) and source[index] != "\n":
                output.append(" ")
                index += 1
        elif char == '"':
            in_string = True
            output.append(" ")
            index += 1
        else:
            output.append(char)
            index += 1
    assert depth == 0 and not in_string, "unterminated Lean comment or string"
    return "".join(output)


def reported_axioms(output: str, declaration: str) -> set[str]:
    match = re.search(
        re.escape(f"'{declaration}' depends on axioms: [") + r"(.*?)]",
        output, re.DOTALL,
    )
    assert match is not None, f"missing axiom report: {declaration}"
    return {part.strip() for part in match.group(1).split(",") if part.strip()}


def assert_text_hygiene(path: Path) -> None:
    data = path.read_bytes()
    assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())


HOME = os.environ["HOME"]
BASE_ENV = {
    "HOME": HOME,
    "PATH": f"{HOME}/.elan/bin:/usr/bin:/bin",
    "ELAN_TOOLCHAIN": TOOLCHAIN,
    "LANG": "C.UTF-8",
    "LC_ALL": "C.UTF-8",
    "TZ": "UTC",
    "LEAN_NUM_THREADS": "1",
}


def isolated_replay(lean: Path, bwrap: Path, lean_path: str) -> dict[str, object]:
    with tempfile.TemporaryDirectory(prefix="stage1-m0072-validation-", dir="/tmp") as temp_name:
        temp = Path(temp_name).resolve()
        for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
            (temp / name).write_bytes((HERE / name).read_bytes())
        (temp / "home").mkdir()
        base = [
            str(bwrap), "--ro-bind", "/", "/", "--bind", str(temp), str(temp),
            "--dev", "/dev", "--proc", "/proc", "--unshare-net",
            "--die-with-parent", "--clearenv", "--setenv", "HOME", str(temp / "home"),
            "--setenv", "TMPDIR", str(temp), "--setenv", "LANG", "C.UTF-8",
            "--setenv", "LC_ALL", "C.UTF-8", "--setenv", "TZ", "UTC",
            "--setenv", "LEAN_NUM_THREADS", "1", "--chdir", str(temp),
        ]

        def lean_run(name: str, module_path: str) -> str:
            return run(base + [
                "--setenv", "LEAN_PATH", module_path, str(lean), "--trust=0", "-t0",
                "-o", name.replace(".lean", ".olean"), name,
            ])

        outputs: dict[str, object] = {}
        outputs["statement"] = lean_run("Statement.lean", lean_path)
        local_path = f"{temp}:{lean_path}"
        outputs["obligation_tree"] = lean_run("ObligationTree.lean", local_path)
        outputs["proof"] = lean_run("Proof.lean", local_path)
        outputs["validation"] = lean_run("Validation.lean", local_path)
        outputs["olean_sha256"] = {
            name: sha256(temp / name)
            for name in ("Statement.olean", "ObligationTree.olean", "Proof.olean", "Validation.olean")
        }
        return outputs


def observe() -> dict[str, object]:
    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    for name, expected in EXPECTED_INPUTS.items():
        assert sha256(HERE / name) == expected, f"stale validation input: {name}"
    for name, expected in POLICY_INPUTS.items():
        assert sha256(ROOT / name) == expected, f"changed policy input: {name}"
    assert sha256(LEAN_ROOT / "lean-toolchain") == TOOLCHAIN_SHA256
    assert sha256(LEAN_ROOT / "lake-manifest.json") == MANIFEST_SHA256

    manifest = load(LEAN_ROOT / "lake-manifest.json")
    mathlib_entry = next(row for row in manifest["packages"] if row["name"] == "mathlib")
    assert mathlib_entry["rev"] == mathlib_entry["inputRev"] == MATHLIB_REVISION
    assert mathlib_entry["url"] == MATHLIB_REMOTE
    assert (LEAN_ROOT / ".lake").is_symlink()
    assert MATHLIB.resolve().is_dir()
    assert git("rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert git("remote", "get-url", "origin", cwd=MATHLIB) == MATHLIB_REMOTE
    assert git("status", "--porcelain=v1", "--untracked-files=all", cwd=MATHLIB) == ""
    assert sha256(MATHLIB / "LICENSE") == MATHLIB_LICENSE_SHA256
    for relative, expected in SOURCE_BOUNDARIES.items():
        source = MATHLIB / relative
        olean = MATHLIB / ".lake/build/lib/lean" / Path(relative).with_suffix(".olean")
        assert git("rev-parse", f"HEAD:{relative}", cwd=MATHLIB) == expected["blob"]
        assert sha256(source) == expected["source_sha256"]
        assert sha256(olean) == expected["olean_sha256"]
        assert olean.stat().st_size == expected["olean_bytes"]

    lake_launcher = Path(HOME) / ".elan/bin/lake"
    assert sha256(lake_launcher) == ELAN_LAKE_SHA256
    lean = Path(run([str(lake_launcher), "env", "which", "lean"], cwd=LEAN_ROOT, env=BASE_ENV).strip())
    lake = Path(run([str(lake_launcher), "env", "which", "lake"], cwd=LEAN_ROOT, env=BASE_ENV).strip())
    bwrap = Path("/usr/bin/bwrap")
    python = Path("/usr/bin/python3").resolve()
    git_executable = Path("/usr/bin/git")
    assert sha256(lean) == LEAN_SHA256 and sha256(lake) == LAKE_SHA256
    assert sha256(python) == PYTHON_SHA256 and sha256(git_executable) == GIT_SHA256
    assert sha256(bwrap) == BWRAP_SHA256
    lean_version = run([str(lean), "--version"], env=BASE_ENV)
    assert "4.29.0" in lean_version and LEAN_COMMIT in lean_version
    lean_path = run(
        [str(lake_launcher), "env", "printenv", "LEAN_PATH"], cwd=LEAN_ROOT, env=BASE_ENV
    ).strip()

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by|run_tac)\b|"
        r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
        r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
        r"(?:axiom|constant|opaque|unsafe|extern)\b",
        re.MULTILINE,
    )
    for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
        source = source_without_comments_and_strings((HERE / name).read_text(encoding="utf-8"))
        assert prohibited.search(source) is None, f"prohibited Lean device in {name}"

    outputs = isolated_replay(lean, bwrap, lean_path)
    proof_output = str(outputs["proof"])
    validation_output = str(outputs["validation"])
    for declaration in PROOF_DECLARATIONS:
        assert reported_axioms(proof_output + validation_output, declaration) == EXPECTED_AXIOMS
    for declaration in VALIDATION_DECLARATIONS:
        assert reported_axioms(validation_output, declaration) == EXPECTED_AXIOMS
    assert validation_output.count("Declarations are sorry-free!") == 14
    assert "sorryAx" not in "".join(str(outputs[key]) for key in (
        "statement", "obligation_tree", "proof", "validation"
    ))
    closure_match = re.search(
        r"VALIDATION_CLOSURE declarations=(\d+) modules=(\d+)", validation_output
    )
    assert closure_match is not None
    assert "VALIDATION_CLOSURE axioms=[propext, Classical.choice, Quot.sound]" in validation_output
    assert "VALIDATION_CLOSURE bodyless_nonaxioms=[]" in validation_output
    assert "VALIDATION_CLOSURE unsafe=[]" in validation_output
    return {
        "lean_output_sha256": {
            key: hashlib.sha256(str(outputs[key]).encode()).hexdigest()
            for key in ("statement", "obligation_tree", "proof", "validation")
        },
        "fresh_olean_sha256": outputs["olean_sha256"],
        "closure": {
            "declarations": int(closure_match.group(1)),
            "modules": int(closure_match.group(2)),
            "axioms": EXPECTED_AXIOM_LIST,
            "bodyless_nonaxioms": [],
            "unsafe_declarations": [],
        },
        "tools": {
            "lean": str(lean), "lake": str(lake), "python": str(python),
            "git": str(git_executable), "bubblewrap": str(bwrap),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--probe", action="store_true")
    parser.add_argument("--worker-packet", type=Path)
    args = parser.parse_args()

    observation = observe()
    if args.probe:
        print(json.dumps(observation, sort_keys=True))
        return

    assert args.worker_packet is not None, "final self-test requires --worker-packet"
    spec = load(HERE / "validation-spec.json")
    receipt = load(HERE / "validation-receipt.json")
    packet = load(args.worker_packet)
    targets = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    statement = load(HERE / "statement.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    proof_receipt = load(HERE / "proof-receipt.json")
    instance = load(HERE / "instance.json")
    local_dag = load(HERE / "task-dag.json")

    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 1102 and target["baseline"] == "L0"
    assert target["lifecycle_mode"] == "planned"
    assert target["rework_required"] is True and target["theorem_complete"] is False
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item == {
        "id": ITEM, "theorem_id": THEOREM, "execution_rank": 1102,
        "phase": "validation", "layer": 5, "state": "[ ]",
        "depends_on": ["S56-M-0072-PROOF"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Run hermetic kernel, trust, provenance, and independent validation gates.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0, "children": [],
    }
    predecessor = next(row for row in execution["items"] if row["id"] == "S56-M-0072-PROOF")
    assert predecessor["state"] == "[_]" and predecessor["attempts"] == 1
    local_task = next(row for row in local_dag["tasks"] if row["id"] == ITEM)
    assert local_task["state"] == "open" and local_task["depends_on"] == ["S56-M-0072-PROOF"]
    assert local_dag["accepted_states"] == []

    formal = statement["canonical_formal_target"]
    assert formal["declaration_or_expression"] == (
        "Stage1Instances.THM_M_0072.ThompsonTransferLemmaTarget"
    )
    assert formal["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert formal["statement_file_sha256"] == EXPECTED_INPUTS["Statement.lean"]
    assert registry["root_obligation_id"] == "M0072-ROOT"
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert len(registry["obligations"]) == 28
    closure = graphs["closure_boundary"]
    assert closure["root_closed"] is False
    assert closure["accepted_closed_obligations"] == []
    assert closure["remaining_root_cut_set"] == ["M0072-T-OUTSIDE"]
    assert closure["theorem_complete"] is False
    assert proof_receipt["canonical_target_expression_sha256"] == EXPRESSION_SHA256
    assert proof_receipt["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert proof_receipt["inputs"]["proof_sha256"] == EXPECTED_INPUTS["Proof.lean"]
    assert proof_receipt["provisionally_closed_proof_obligation_ids"] == PROOF_IDS
    assert proof_receipt["accepted_closed_obligation_ids"] == []
    assert proof_receipt["result"]["root_kernel_closed"] is True
    assert proof_receipt["result"]["accepted_root_closed"] is False
    assert instance["lifecycle_mode"] == "planned"
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == []
    assert instance["audit_complete"] is instance["theorem_complete"] is False

    assert spec["schema_version"] == "stage1-validation-spec/1.0"
    assert spec["item_id"] == ITEM and spec["theorem_id"] == THEOREM
    assert spec["depends_on"] == ["S56-M-0072-PROOF"] and spec["intent"] == "validate"
    assert len(spec["recipes"]) == 1
    recipe = spec["recipes"][0]
    assert recipe["recipe_id"] == "S56-M-0072-VALIDATION-narrow-v1"
    assert recipe["cwd"] == "." and recipe["argv"] == [
        "python3", "-I", "-B", f"Stage1_Instances/{THEOREM}/check_validation.py",
        "--worker-packet", ".stage1-worker-selftest.json",
    ]
    assert recipe["timeout_seconds"] == 600 and recipe["network_policy"] == "denied"
    assert recipe["expected_exit"] == 0 and "--unshare-net" in recipe["network_enforcement"]
    assert recipe["covered_obligation_ids"] == COVERED_IDS
    assert recipe["expected_outputs"] == [{
        "path_or_stream": "stdout",
        "semantic_hash_policy": (
            "exact nine-line UTF-8 PASS/FAIL-CLOSED summary bound by validation-receipt.json"
        ),
    }]

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == packet["item_id"] == ITEM
    assert receipt["theorem_id"] == THEOREM
    assert receipt["phase"] == "validation" and receipt["intent"] == "validate"
    assert receipt["depends_on"] == ["S56-M-0072-PROOF"]
    assert receipt["base_revision"] == packet["base_revision"] == BASE_REVISION
    assert receipt["base_tree"] == BASE_TREE
    assert receipt["verdict"] == "blocked"
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == packet["state"] == "[_]"
    assert receipt["accepted"] is receipt["release_grade"] is receipt["content_addressed"] is False
    assert receipt["covered_obligation_ids"] == COVERED_IDS
    assert receipt["accepted_closed_obligation_ids"] == []
    for name, expected in EXPECTED_INPUTS.items():
        assert receipt["inputs"][name] == expected
    for name, expected in POLICY_INPUTS.items():
        assert receipt["inputs"][name] == expected
    assert receipt["inputs"]["check_validation.py"] == sha256(HERE / "check_validation.py")
    assert receipt["inputs"]["validation-phase.md"] == sha256(HERE / "validation-phase.md")
    assert receipt["result"]["lean_output_sha256"] == observation["lean_output_sha256"]
    assert receipt["result"]["fresh_olean_sha256"] == observation["fresh_olean_sha256"]
    assert receipt["result"]["transitive_environment_observation"] == observation["closure"]
    assert receipt["result"]["exact_root_kernel_replay"] == "provisional_pass"
    assert receipt["result"]["exact_type_alias_replay"] == "provisional_pass_same_worker"
    assert receipt["result"]["proof_master_acceptance"] == "fail_closed"
    assert receipt["result"]["accepted_root_machine_debt"] == "M3"
    assert receipt["result"]["accepted_root_closed"] is False
    assert receipt["result"]["complete_provenance_tcb_gate"] == "fail_closed"
    assert receipt["result"]["hermetic_release_gate"] == "fail_closed"
    assert receipt["result"]["independent_distinct_runner_gate"] == "fail_closed"
    assert receipt["result"]["audit_complete"] is receipt["result"]["theorem_complete"] is False
    assert receipt["first_failed_gate"] == "dependency.S56-M-0072-PROOF.master_acceptance"
    assert receipt["first_failed_release_gate"] == "S56-10.6-HERMETIC-COLD-EMPTY-CACHE"
    assert receipt["recipe"] == recipe
    assert receipt["output_evidence"] == {
        "stdout_semantic_sha256": hashlib.sha256("\n".join(SUMMARY_LINES).encode()).hexdigest(),
        "expected_line_count": 9,
        "exit_code": 0,
        "raw_logs_retained": False,
        "raw_log_sha256": None,
        "boundary": (
            "Subprocess semantic hashes and the exact final summary are retained; no raw release "
            "log bundle is claimed."
        ),
    }

    expected_keys = {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert set(packet) == expected_keys
    assert set(receipt["changed_paths"]) == set(CHANGED_PATHS)
    assert set(packet["changed_paths"]) == set(CHANGED_PATHS)
    assert packet["commands"] == PACKET_COMMANDS
    assert packet["output_summary"] == PACKET_OUTPUT_SUMMARY
    assert packet["known_failures"] == receipt["known_failures"]
    actual_changed = {
        line[3:] for line in git("status", "--short", "--untracked-files=all").splitlines()
        if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual_changed == set(CHANGED_PATHS), (actual_changed, CHANGED_PATHS)
    for relative in CHANGED_PATHS:
        assert_text_hygiene(ROOT / relative)

    print("\n".join(SUMMARY_LINES))


if __name__ == "__main__":
    main()
