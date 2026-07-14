#!/usr/bin/env python3
"""Fail-closed narrow validation for S56-M-0990-VALIDATION."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import platform
import re
import shutil
import subprocess
import time
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0990"
DEPENDENCY = ROOT / "Stage1_Instances" / "THM-M-0989"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM = "S56-M-0990-VALIDATION"
THEOREM = "THM-M-0990"
BASE_REVISION = "a1a7e939e58f103f5ff5d23af51437fa8658aa04"
BASE_TREE = "d881fd9641fa3e5f3ebe5082b35672981e90adcf"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MATHLIB_REMOTE = "https://github.com/leanprover-community/mathlib4.git"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
DENOMINATOR = "fa799ae86623298ad54105d2041f7903144cc398f769b7da7a3865507a9921f6"
EXPECTED_AXIOMS = ["propext", "Classical.choice", "Quot.sound"]
EXPECTED_CLOSURE_DECLARATIONS = 53310
EXPECTED_CLOSURE_MODULES = 1752
EXPECTED_INPUTS = {
    "Statement.lean": "2f5bd7f9563bb7c8c54a614d7f95f10e8f4508d4cce6f3dd8b0cc620dbdbae53",
    "ObligationTree.lean": "e76c1dfa2dad57e3ec50683ec215cddf9b3150d87fd11d62c0a7aafb0e6badb8",
    "Normalization.lean": "af39e77d8f208a1a6ed9c9bb900e95f482ba0e2cc44db1365ad13fd04ae1b9fc",
    "ProductLimit.lean": "80b4031c79f165efc24b9b38c10b4ceb2331dedf6e6d7eece5c8890cc95b8aaf",
    "GeneralizedLindeberg.lean": "22114c23660d832aced7828b1a2190df1a94eb78c04700b3c40d0136562d544a",
    "Proof.lean": "c69ca904090a8280014b1fe8599fd39118d4b3c28943cb31edb1d8392e42a4ca",
    "Validation.lean": "ff4a80fa9728376c121013b876bfd42bd0371b36c582d512d357b6eb1c4ff971",
    "statement.json": "4694593fa432ddd22537708a5ce601007058db0a366fa3d47d80cc8c30e3f54a",
    "obligation-registry.json": "b2c4ddae47c3b0474899b3a7039ad9f54ff5af3cc2d833e17e08bb92ae08db5b",
    "typed-graphs.json": "164964f565013927072c3657e7c7a35aecc7d7abffd6ae1e453c19ac9f97072d",
    "validation-specs.json": "35b2d14a8cf43b75429e62f71d6bb4fca1894f742b9d47db054b71408074d696",
    "proof-receipt.json": "43de078d2aa1d69fbe7300d27a0f0005ca8cd7c74bdaf98f11fe0671d86ae6b7",
    "check_proof.py": "a91e98b8af66cb5f30912079f8a82448895143262bb0205e50265fb565973147",
    "check_proof.sh": "ea11ee673d9351dcc860adccb2bd47d9e69ba5f7c4a38726d744c7a7dc4a83d5",
    "check_validation.sh": "ec95e7fb514cc8ac6201d3981a6a8fafa192d36d63926c8f1f10f27346345e9e",
    "validation-phase-spec.json": "11eff38d266ced71e67d92964aa50f807dc7a467eb8773865b5e4124e766647b",
}
EXPECTED_DEPENDENCY_INPUTS = {
    "Statement.lean": "ccdd546c1997d1cd38879a6df2ac9acbb8aaf01b7565ce19625c981d7b32772a",
    "ObligationTree.lean": "57005c9602c9d27448871dd595af49980f26b938170b613c08e41ff53c1ecadb",
    "Proof.lean": "d470547c10d1d2eff25cc6b5780a350b4e71fc4a3ad92891fb2d764f2f37808f",
    "CharFunBound.lean": "6c94cf73831e55bb29eecbdf0927622d398b09c4b84d0d15195aa3d041e1b02f",
}
PROVENANCE = {
    "Mathlib/Probability/CentralLimitTheorem.lean": {
        "blob": "e0cfc897a4679025f71712abbf8834c1f318b2c1",
        "source": "4b42bad9589ec3772fe0e884ad70789c89fd0c11566d980f3df1c862bbc7f03d",
        "olean": "d3b747f6dd0a15d12d10d29a4cc86980a72b54d0af741dc31cf5b70a0b70b988",
    },
    "Mathlib/Probability/Independence/CharacteristicFunction.lean": {
        "blob": "5011e757544576dc1e74835578e7607d7f66a690",
        "source": "59038431e678c8e44b7dd26f39cde99e9d68ea781f5fb8e0b595c83f05b23fe2",
        "olean": "ea77f41ff916655a04dd91ff76510576a7649aef46da1ae55e1dc4f34e8c0d95",
    },
    "Mathlib/Probability/Distributions/Gaussian/Real.lean": {
        "blob": "f5795fbfb92475879b67b0ee8577687575a82258",
        "source": "f5321db08f0156c5a12e15986d2ced9108183c907e3082d2566da8ef8da931a8",
        "olean": "b5894530bc315c897142ff650c774ed5ee3180b1df45690021fdd830e6e82ea4",
    },
    "Mathlib/MeasureTheory/Measure/LevyConvergence.lean": {
        "blob": "fc0bf2a7054634763040aa9bbcaae5f2c93b8d5f",
        "source": "54fa4a3baec8a8ab916524dd63c52a6da70bc919031e20318b198fa20755fff8",
        "olean": "9f5a27181b909026ed757f7fd257f83407fdcbf3315cb0560c1a65e22e994865",
    },
}
UTILITY_PROVENANCE = {
    "Mathlib/Util/AssertNoSorry.lean": {
        "source": "aa9f7bebacafc688c894ef2171930e51ed19e0dfe722581848a2414d28900d4d",
        "olean": "c8bf37753d9bad47b9fe67e32436da8b9af516a4abbbe14e74726f01ba2fb30b",
    },
    "Mathlib/Util/PrintSorries.lean": {
        "source": "03670b0b0007740e5390dadd49c3d10a02b7d0919092d2b3214ef8a6a8cf798f",
        "olean": "9bcc4076e0aee5febb2eea5cf9dc959f38526e9f974afdfdd8658bfd318d5bb7",
    },
}
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/Validation.lean",
    f"Stage1_Instances/{THEOREM}/check_validation.py",
    f"Stage1_Instances/{THEOREM}/check_validation.sh",
    f"Stage1_Instances/{THEOREM}/validation-phase-spec.json",
    f"Stage1_Instances/{THEOREM}/validation-receipt.json",
    f"Stage1_Instances/{THEOREM}/validation-validation.md",
}
SUMMARY_LINES = (
    "PASS THM-M-0990 narrow validation",
    "PASS network-isolated kernel replay: nine dependency/proof modules, exact root, and separate final-composition replay elaborated with --trust=0",
    "PASS trust observation: 30 declaration reports contain exactly propext, Classical.choice, and Quot.sound; transitive closure has no unsafe or unexpected bodyless declarations",
    "PASS selected provenance: frozen hashes, clean dependency pin/tree/remote/license, six selected mathlib source/olean boundaries, and tool identities agree",
    "PASS hygiene and architecture: six parser-aware sorry checks, local prohibited scan, proof receipt, denominator, and frozen graph boundary agree",
    "FAIL CLOSED authority/foundation: proof master acceptance, a canonical expression fingerprint, and accepted foundation/TCB profiles remain open at H2/M3/R4",
    "FAIL CLOSED hermetic release: shared warm .lake is not clean-checkout empty-cache bootstrap, offline restoration, or a deterministic TCB/SBOM bundle",
    "FAIL CLOSED independent release: the separate composition shares analytic bodies, this worker, checkout, kernel, and cache; no distinct signed verifier exists",
    "audit_complete=false; theorem_complete=false",
)
TIMEOUT_SECONDS = 1800.0
STARTED = time.monotonic()
SUBPROCESS_ENV = {
    "HOME": os.environ.get("HOME", ""),
    "PATH": os.environ.get("PATH", ""),
    "LANG": "C",
    "LC_ALL": "C",
    "NO_COLOR": "1",
    "TZ": "UTC",
}

if not __debug__:
    raise RuntimeError("validation requires Python assertions (__debug__ must be true)")


def load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict), path
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(argv: list[str], *, cwd: Path = ROOT) -> str:
    remaining = TIMEOUT_SECONDS - (time.monotonic() - STARTED)
    if remaining <= 0:
        raise TimeoutError("validation exceeded its 1800-second wall-clock bound")
    result = subprocess.run(
        argv,
        cwd=cwd,
        env=SUBPROCESS_ENV,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=remaining,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(f"validation failed ({result.returncode}): {argv!r}\n{result.stdout}")
    return result.stdout


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["git", *args], cwd=cwd).strip()


def without_lean_comments(source: str) -> str:
    output: list[str] = []
    index = 0
    depth = 0
    in_string = False
    escaped = False
    while index < len(source):
        char = source[index]
        pair = source[index:index + 2]
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
            output.extend("  ")
            index += 2
        elif pair == "--":
            while index < len(source) and source[index] != "\n":
                output.append(" ")
                index += 1
        else:
            output.append(char)
            if char == '"':
                in_string = True
            index += 1
    assert depth == 0 and not in_string
    return "".join(output)


def changed_paths() -> set[str]:
    output = git("status", "--short", "--untracked-files=all")
    return {
        line[3:]
        for line in output.splitlines()
        if line[3:] == ".stage1-worker-selftest.json"
        or line[3:].startswith(f"Stage1_Instances/{THEOREM}/")
    }


def all_changed_paths() -> set[str]:
    output = git("status", "--short", "--untracked-files=all")
    return {line[3:] for line in output.splitlines()}


def no_index_patch_sha256(path: Path) -> str:
    relative = path.relative_to(ROOT)
    result = subprocess.run(
        ["git", "diff", "--no-index", "--binary", "/dev/null", str(relative)],
        cwd=ROOT,
        env=SUBPROCESS_ENV,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    assert result.returncode == 1, path
    return hashlib.sha256(result.stdout).hexdigest()


def main() -> None:
    spec = load(HERE / "validation-phase-spec.json")
    receipt = load(HERE / "validation-receipt.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")
    targets = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    statement = load(HERE / "statement.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    proof_receipt = load(HERE / "proof-receipt.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 270 and target["baseline"] == "L0"
    assert target["lifecycle_mode"] == "planned"
    assert target["rework_required"] is True and target["theorem_complete"] is False
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    predecessor = next(
        row for row in execution["items"] if row["id"] == "S56-M-0990-PROOF"
    )
    assert item["state"] in {"[ ]", "[_]"}
    assert item["depends_on"] == ["S56-M-0990-PROOF"]
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM}"]
    assert predecessor["state"] == "[_]"

    for name, expected in EXPECTED_INPUTS.items():
        assert sha256(HERE / name) == expected, f"stale validation input: {name}"
    for name, expected in EXPECTED_DEPENDENCY_INPUTS.items():
        assert sha256(DEPENDENCY / name) == expected, f"stale THM-M-0989 input: {name}"
    assert sha256(LEAN_ROOT / "lean-toolchain") == (
        "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2"
    )
    assert sha256(LEAN_ROOT / "lake-manifest.json") == (
        "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81"
    )
    assert statement["declaration"] == "Stage1Instances.THM_M_0990.StatementShape"
    assert statement["elaboration"] == "passed"
    assert statement["proof_claim"] is statement["theorem_complete"] is False
    assert statement.get("elaborated_expression_sha256") is None
    assert registry["root_obligation_id"] == "M0990-ROOT"
    assert registry["denominator_sha256"] == DENOMINATOR
    assert registry["frozen_against_statement_sha256"] == sha256(HERE / "statement.json")
    assert graphs["registry_denominator_sha256"] == DENOMINATOR
    assert graphs["closure_boundary"] == {
        "closed_obligations": [],
        "root_closed": False,
        "root_machine_debt": "M3",
        "remaining_root_cut_set": ["M0990-T-TRIANGULAR-BRIDGE"],
        "composition_certificates_checked": [
            "Stage1Instances.THM_M_0990.ObligationTree.root_compose"
        ],
        "audit_complete": False,
        "theorem_complete": False,
    }
    assert proof_receipt["item_id"] == "S56-M-0990-PROOF"
    assert proof_receipt["accepted"] is proof_receipt["content_addressed"] is False
    assert proof_receipt["canonical_target"] == statement["declaration"]
    assert proof_receipt["result"]["root_kernel_closed"] is True
    assert proof_receipt["result"]["accepted_root_closed"] is False
    assert proof_receipt["result"]["axioms"] == EXPECTED_AXIOMS

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by|extern)\b|"
        r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
        r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
        r"(?:axiom|constant|opaque|unsafe)\b",
        re.MULTILINE,
    )
    for path in [
        *(HERE / name for name in (
            "Statement.lean", "ObligationTree.lean", "Normalization.lean",
            "ProductLimit.lean", "GeneralizedLindeberg.lean", "Proof.lean",
            "Validation.lean",
        )),
        *(DEPENDENCY / name for name in EXPECTED_DEPENDENCY_INPUTS),
    ]:
        source = without_lean_comments(path.read_text(encoding="utf-8"))
        assert prohibited.search(source) is None, f"prohibited source construct in {path}"
    validation_source = without_lean_comments((HERE / "Validation.lean").read_text())
    replay_body = validation_source.split(
        "theorem lyapunovCentralLimit_composition_replay", 1
    )[1].split("assert_no_sorry", 1)[0]
    assert "lyapunovCentralLimit_exact" not in replay_body
    assert "eventualLindebergFeller_exact A" in replay_body

    manifest = load(LEAN_ROOT / "lake-manifest.json")
    mathlib_entry = next(row for row in manifest["packages"] if row["name"] == "mathlib")
    assert mathlib_entry["rev"] == mathlib_entry["inputRev"] == MATHLIB_REVISION
    assert MATHLIB.resolve().is_dir()
    assert git("rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert git("remote", "get-url", "origin", cwd=MATHLIB) == MATHLIB_REMOTE
    assert git("status", "--porcelain=v1", cwd=MATHLIB) == ""
    for source_name, expected in PROVENANCE.items():
        source = MATHLIB / source_name
        olean = MATHLIB / ".lake/build/lib/lean" / source_name.replace(".lean", ".olean")
        assert git("rev-parse", f"HEAD:{source_name}", cwd=MATHLIB) == expected["blob"]
        assert sha256(source) == expected["source"]
        assert sha256(olean) == expected["olean"]
    for source_name, expected in UTILITY_PROVENANCE.items():
        source = MATHLIB / source_name
        olean = MATHLIB / ".lake/build/lib/lean" / source_name.replace(".lean", ".olean")
        assert sha256(source) == expected["source"]
        assert sha256(olean) == expected["olean"]
    assert sha256(MATHLIB / "LICENSE") == (
        "b40930bbcf80744c86c46a12bc9da056641d722716c378f5659b9e555ef833e1"
    )

    lean = Path(run(["lake", "env", "which", "lean"], cwd=LEAN_ROOT).strip())
    lake = Path(run(["lake", "env", "which", "lake"], cwd=LEAN_ROOT).strip())
    python = Path(os.path.realpath(os.sys.executable))
    git_path = Path(os.path.realpath(shutil.which("git") or ""))
    bwrap = Path(os.path.realpath(shutil.which("bwrap") or ""))
    assert LEAN_COMMIT in run(["lake", "env", "lean", "--version"], cwd=LEAN_ROOT)
    assert "5.0.0-src+98dc76e" in run(["lake", "--version"], cwd=LEAN_ROOT)
    expected_tools = {
        lean: "3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf",
        lake: "a608ff084d7e2af228b92a29d7c2fd083ba0580e46889175ec74a81678c98359",
        python: "b8d8288faefdd300201f43fcf00f6f539a27218eeed3a3dff5ab10b9c4c99700",
        git_path: "8a48eefa306b9a2a9c3e576784a74ad7485779279e5a46ec43361a1864760e45",
        bwrap: "0abea81db798ebf6b4742ac0664802d97521547a353c2a0dbdc21d76cbbfd2c0",
    }
    for path, expected in expected_tools.items():
        assert path.is_file() and sha256(path) == expected, path

    tree_output = run(["python3", str(HERE / "check_obligation_tree.py")])
    assert "PASS THM-M-0990 obligation tree: 18 obligations, 43 typed edges" in tree_output
    assert DENOMINATOR in tree_output
    assert "root remains open at M3" in tree_output

    runner_output = run(["bash", str(HERE / "check_validation.sh")])
    assert runner_output.count("depends on axioms:") == 30
    assert runner_output.count("Declarations are sorry-free!") == 6
    assert (
        f"VALIDATION_CLOSURE declarations={EXPECTED_CLOSURE_DECLARATIONS} "
        f"modules={EXPECTED_CLOSURE_MODULES}"
    ) in runner_output
    assert "VALIDATION_CLOSURE axioms=[propext, Classical.choice, Quot.sound]" in runner_output
    assert "VALIDATION_CLOSURE bodyless_nonaxioms=[]" in runner_output
    assert "VALIDATION_CLOSURE unsafe=[]" in runner_output
    assert "sorryAx" not in runner_output and "declaration uses 'sorry'" not in runner_output

    assert spec["schema_version"] == "stage1-validation-recipe/1.0"
    assert spec["recipe_id"] == "S56-M-0990-VALIDATION-narrow-v1"
    assert spec["item_id"] == ITEM and spec["theorem_id"] == THEOREM
    assert spec["cwd"] == "."
    assert spec["argv"] == [
        "python3", "-I", "-B", f"Stage1_Instances/{THEOREM}/check_validation.py",
    ]
    assert spec["timeout_seconds"] == 1800 and spec["network_policy"] == "denied"
    assert spec["expected_exit"] == 0
    assert "bubblewrap --unshare-net" in spec["network_enforcement"]
    assert len(spec["covered_obligation_ids"]) == 15
    assert spec["observed_fail_closed_obligation_ids"] == [
        "M0990-S-FOUNDATION", "M0990-X-SOURCE", "M0990-X-TCB",
    ]
    assert spec["covered_obligation_ids"] == receipt["covered_obligation_ids"]
    assert spec["observed_fail_closed_obligation_ids"] == receipt[
        "observed_fail_closed_obligation_ids"
    ]
    assert spec["covered_declarations"] == receipt["covered_declarations"]
    frozen_replay = receipt["frozen_node_recipe_replay"]
    frozen_specs = load(HERE / "validation-specs.json")
    frozen_argv = {
        tuple(recipe["argv"]) for recipe in frozen_specs["recipes"]
    }
    assert len(frozen_specs["recipes"]) == frozen_replay["recipe_count"] == 18
    assert len(frozen_argv) == frozen_replay["distinct_argv_count"] == 1
    assert list(next(iter(frozen_argv))) == frozen_replay["shared_argv"]

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["phase"] == "validation" and receipt["intent"] == "validate"
    assert receipt["verdict"] == "blocked"
    assert receipt["depends_on"] == ["S56-M-0990-PROOF"]
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["release_grade"] is receipt["content_addressed_release_evidence"] is False
    repository_state = receipt["repository_state"]
    assert repository_state["dirty"] is True
    assert repository_state["tracked_patch_sha256"] is None
    assert repository_state["tracked_patch_bytes"] == 0
    assert repository_state["preexisting_untracked_paths"] == ["Formalizations/Lean/.lake"]
    assert repository_state["canonical_lake_symlink_target_sha256"] == hashlib.sha256(
        os.readlink(ROOT / "Formalizations/Lean/.lake").encode()
    ).hexdigest()
    expected_worker_hashes = {
        ".stage1-worker-selftest.json": "333dcf29201ca08823290d3896ccf7bf667bae7248fb762e163bbbd2f9d4f8fa",
        f"Stage1_Instances/{THEOREM}/Validation.lean": EXPECTED_INPUTS["Validation.lean"],
        f"Stage1_Instances/{THEOREM}/check_validation.sh": EXPECTED_INPUTS[
            "check_validation.sh"
        ],
        f"Stage1_Instances/{THEOREM}/validation-phase-spec.json": EXPECTED_INPUTS[
            "validation-phase-spec.json"
        ],
        f"Stage1_Instances/{THEOREM}/validation-validation.md": (
            "5f970ba74abba181a603ffb2c389d9f00996a3a741e9d6d30b34083e74a7cbeb"
        ),
    }
    for relative, expected in expected_worker_hashes.items():
        assert repository_state["untracked_input_hashes"][relative] == expected
        assert sha256(ROOT / relative) == expected
    expected_patch_hashes = {
        f"Stage1_Instances/{THEOREM}/Validation.lean": (
            "4071e622428b101f462fe9320bbdf688d5dab50078ba390fee803f9ba0ee92bd"
        ),
        f"Stage1_Instances/{THEOREM}/check_validation.sh": (
            "7b43ea187da625e3c4f58857a1327483c2e97928d412879aac3000314f436cef"
        ),
        f"Stage1_Instances/{THEOREM}/validation-phase-spec.json": (
            "c95bba23885206e579de2bd5a8c96ec654bce8e3668d82c46427d39331321a70"
        ),
        f"Stage1_Instances/{THEOREM}/validation-validation.md": (
            "314d9ac937b82be3e92d04f806e076c4b1557f76fdac79304b6ff57ee067faa0"
        ),
    }
    for relative, expected in expected_patch_hashes.items():
        assert repository_state["untracked_no_index_patch_hashes"][relative] == expected
        assert no_index_patch_sha256(ROOT / relative) == expected
    assert receipt["canonical_target"]["declaration"] == statement["declaration"]
    assert receipt["canonical_target"]["elaborated_expression_sha256"] is None
    assert receipt["canonical_target"]["registry_denominator_sha256"] == DENOMINATOR
    for name, expected in EXPECTED_INPUTS.items():
        assert receipt["inputs"][name] == expected, name
    assert receipt["inputs"]["thm_m_0989_dependency"] == EXPECTED_DEPENDENCY_INPUTS
    for key in (
        "recipe_id", "cwd", "argv", "env_allowlist", "timeout_seconds",
        "network_policy", "network_enforcement", "expected_exit", "expected_outputs",
    ):
        assert receipt["recipe"][key] == spec[key], key
    assert receipt["environment"]["platform"] == (
        f"{platform.system()} {platform.release()} {platform.machine()}"
    )
    result = receipt["result"]
    assert result["exit_code"] == 0 and result["kernel_replay"] == "provisional_pass"
    assert result["axioms"] == EXPECTED_AXIOMS and result["axiom_probe_count"] == 30
    assert result["parser_aware_sorry_probe_count"] == 6
    assert result["transitive_declaration_count"] == EXPECTED_CLOSURE_DECLARATIONS
    assert result["transitive_module_count"] == EXPECTED_CLOSURE_MODULES
    assert result["unexpected_bodyless_declarations"] == result["unsafe_declarations"] == []
    assert result["root_closed_locally"] is True
    assert result["accepted_root_closed"] is False
    assert result["accepted_machine_debt"] == "M3"
    assert result["hermetic_release_gate"] == "fail_closed"
    assert result["independent_verification_gate"] == "fail_closed"
    assert result["audit_complete"] is result["theorem_complete"] is False
    run_evidence = receipt["run_evidence"]
    assert run_evidence["exit_code"] == 0
    assert run_evidence["stdout_sha256"] == (
        "d63e2103e3ff9dfeb04c11dc45c82fafea11c279f0797cddb9c055645549f565"
    )
    assert run_evidence["stdout_bytes"] == 1162 and run_evidence["stdout_lines"] == 9
    assert run_evidence["stderr_sha256"] == hashlib.sha256(b"").hexdigest()
    assert run_evidence["stderr_bytes"] == 0
    assert receipt["first_failed_gate"] == "dependency.S56-M-0990-PROOF.master_acceptance"
    assert receipt["first_failed_release_gate"] == "S56-10.6-HERMETIC-COLD-BUILD"

    assert set(packet) == {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert packet["item_id"] == ITEM and packet["base_revision"] == BASE_REVISION
    assert packet["state"] == "[_]"
    assert packet["known_failures"] == receipt["known_failures"]
    assert packet["changed_paths"] == receipt["changed_paths"]
    assert set(packet["changed_paths"]) == CHANGED_PATHS
    assert changed_paths() == CHANGED_PATHS
    assert all_changed_paths() == CHANGED_PATHS | {"Formalizations/Lean/.lake"}
    assert all(isinstance(row, dict) for row in packet["commands"])
    assert all(isinstance(row.get("argv"), list) and row.get("exit_code") == 0
               for row in packet["commands"])
    command_text = json.dumps(packet["commands"], sort_keys=True)
    for command in (
        "check_stage1_standard.py", "stage1_target.py", "check_obligation_tree.py",
        "check_validation.sh", "check_validation.py", "json.tool", "git", "diff",
    ):
        assert command in command_text
    for path in CHANGED_PATHS:
        data = (ROOT / path).read_bytes()
        assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())
    for line in SUMMARY_LINES:
        print(line)


if __name__ == "__main__":
    main()
