#!/usr/bin/env python3
"""Fail-closed narrow validator for S56-M-0814-VALIDATION."""

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
import tempfile
import time


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0814"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM = "S56-M-0814-VALIDATION"
THEOREM = "THM-M-0814"
BASE_REVISION = "5cca979173a36d739670a3b5ecad23d89dc96292"
BASE_TREE = "97ccf7381b147bf0f25425a5a7678e51265c6eb3"
EXPRESSION_SHA256 = "f9fc7813f437ebcd4b2b7327373dd76134d651c1624d2a06f689e84ec571a21e"
DENOMINATOR_SHA256 = "f0ff554fe8facfa66bbdcbe9f036f7de20ebbe738b1d2cc9b4c06a899d673d7b"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MATHLIB_REMOTE = "https://github.com/leanprover-community/mathlib4.git"
MATHLIB_LICENSE_SHA256 = "b40930bbcf80744c86c46a12bc9da056641d722716c378f5659b9e555ef833e1"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
LEAN_EXECUTABLE_SHA256 = "3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf"
LAKE_EXECUTABLE_SHA256 = "840179e70803ef373c2ec53342d6a45ea7d022533e4145489fc1278b4f716385"
PYTHON_EXECUTABLE_SHA256 = "b8d8288faefdd300201f43fcf00f6f539a27218eeed3a3dff5ab10b9c4c99700"
GIT_EXECUTABLE_SHA256 = "5516c9f362c29376ab9a499a33082f9f611941d8c75930c880e30ad109e39c9a"
BASH_EXECUTABLE_SHA256 = "3efccc187bafa75ff1e37d246270ab3e7aa559f242c7a52bf3ec2a1b5450bdbd"
BWRAP_EXECUTABLE_SHA256 = "0abea81db798ebf6b4742ac0664802d97521547a353c2a0dbdc21d76cbbfd2c0"
LEAN_TOOLCHAIN_SHA256 = "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2"
LAKE_MANIFEST_SHA256 = "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81"
LAKEFILE_SHA256 = "43259bbc1b42b1574b78c8584753029dc5e118c0a0e752ac0a5bad9004b4dcda"
ENV_EXECUTABLE_SHA256 = "48893b0fb21436b54619db80486e83ef39dfccaf1aefe83dfa00c02d6146e8c0"
ALLOWED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
EXPECTED_INPUTS = {
    "Statement.lean": "e2493ef46f9bdd5c8d0b30069efaf27b7ad0f69781d4c4c7317b94a63a06755b",
    "ObligationTree.lean": "bca977e826adfc22fe9e3b3fe583445ff42cfe57f66da706d2827a2f1d62a69d",
    "Proof.lean": "b7f4d1e28d4e9add0ca9f21943bb104b1dd450106a217b9b8298013afe250e76",
    "Validation.lean": "1d2412bbf5e056c6a34865e2b66b5d355ee1614d1b9870c7bf4d181153fbdf36",
    "instance.json": "726dc6f09f476c7060a90ae449e591693a7bbb2e10da4893e525a61e7fafaf8f",
    "statement.json": "ed7b955159e8bc250fe051cc69ad5b067c7f0901a3a401e0ae4890414adda4b0",
    "anchor-audit.json": "4add5128314497037bd14a8cb009edc94f66e78b8a690eb43632477a5e8d191a",
    "obligation-registry.json": "1b771d946118867c69834923a5e107934526d6dd638dd78e31fac2cb6094e63e",
    "typed-graphs.json": "d970a886c6f727962d7dfb3e37d6b9475125d48d7d786f9e9f91b583b201e2fc",
    "validation-specs.json": "a81423575425c8dc960e100037f36a9622a22e62ffcf46695b0f3be78388ee88",
    "task-dag.json": "b68cd92d256cf50cd6780f3536763543f8f8ea2548a5c790da843512516f9644",
    "proof-receipt.json": "d91e637c09b92f21f92d8005d004014912eb1f04ff9fc10ca7a2643291825c8a",
    "proof-blocker.json": "6e4a2aed3868fce77f1368a678b87afcd0bc21346cc62d062c7282de1549ce23",
    "source-statement-crosswalk.md": "a179f8cea8cf7578092f95f15579db8a5fca9bd9f3b359eda5271d24778d9659",
    "validation-spec.json": "03f6a2cfc8c717d34671baf217f938909240c28e3b0246477d632d3d187dc1f0",
    "validation-blocker.json": "4b85c1a2984a505a8e4dc24f77bcdcfcd961d4793130f8cfcb5c49ff53741213",
}
REPO_INPUTS = {
    "Docs/Stage1_Targets_rev-5.6.json": "02eec284de534dd78e1cf75f82a477ff477567dd682b7445cb7587abd137ab2c",
    "Docs/Stage1_Execution_DAG_rev-5.6.json": "948aea6d5368a847ceba2ade6eb9e3e1ee19778b3c76228bce3e9915c6d04794",
    "Docs/Stage1_Blueprint_rev-5.6.md": "d58e9f173b339337832791aa237b25f017d1b62fb261b2d9b8a3d4ac79fb5f57",
    "skills/execute-stage1-rev56/SKILL.md": "26d47a66c6535feabb8bbf1051fd55d76a53fe761f4b3d953f86b97ec86152b8",
    "Formalizations/Lean/lean-toolchain": LEAN_TOOLCHAIN_SHA256,
    "Formalizations/Lean/lake-manifest.json": LAKE_MANIFEST_SHA256,
    "Formalizations/Lean/lakefile.lean": LAKEFILE_SHA256,
}
SELECTED_MATHLIB = {
    "Mathlib/Algebra/BigOperators/Finsupp/Basic.lean": {
        "blob": "f95fc4d751a6e725a97b40839de1138406fba9ef",
        "source_sha256": "11ea32d613fd10d2b4b0e1222caac5ca6bf0a16942202f4109c236e5b25580ad",
        "olean_sha256": "78e7b1959bfab297512f7a823632924f5d7f306cbe530680812160ef8af68c89",
        "ilean_sha256": "79a176c6a8fd0c738638f6faba56ccbf6e808584f498aef832cb676a609dfc1b",
    },
    "Mathlib/Combinatorics/Graph/Basic.lean": {
        "blob": "72ae0789f49228ac2fb458a9bf7da842d0638190",
        "source_sha256": "dc3f9c7793f8de09261868afeb7e1d8804914b90b1fc4615feb139f2452dd2b9",
        "olean_sha256": "4affbfa144a2039c6510cf4faf1d366836f297caa730683b9065bfc198e33f5e",
        "ilean_sha256": "82b933ae2747445b0c07259f9a40f375a9fd409b1fbed9335eaaafe081e312f3",
    },
    "Mathlib/Data/NNReal/Defs.lean": {
        "blob": "5fb2535ec9fd91b90136eeaa2bc732f39f1072a7",
        "source_sha256": "01a2294d1c6bce17e94aed9fbf5c5eaf3558af586f361f362e06552ef067a24e",
        "olean_sha256": "72c00b471d8e2e03ddb9c9e922c095de201fd78fad6770a9986454d041c81bbf",
        "ilean_sha256": "301e2aa0700685423890ca625bb6666f1e034a73c9984cc841b7b8e7b2ba030d",
    },
    "Mathlib/Data/Finsupp/Order.lean": {
        "blob": "d5df81558098c46af6dbeb7b763bb55570c42560",
        "source_sha256": "dd1e5ea371a79fb988e129ae1f7f608d08034723fa16c77003769d5eafea31ff",
        "olean_sha256": "bd5419c51f4d4ecc4f88dca8f5e9e097036582035ee9d5ad7a8ad61ceecb47d8",
        "ilean_sha256": "60f764f8a90773feaa06e1ff8727db5d114e573827ccde72f42ab9d8450a1fda",
    },
    "Mathlib/Algebra/Order/BigOperators/Group/Finset.lean": {
        "blob": "8e0269652e8d94da10230c3be31e960ad2712956",
        "source_sha256": "8e8cb48629c6f4d736b4949b09daa3d726a8a1ed9dcf6d76eb12beee3cb5cb26",
        "olean_sha256": "cafb96a37dd576d384e5bb85f4863b66b60e751a0223570cba475ec053dd3e5e",
        "ilean_sha256": "9dd6a4348af8b2dda45d457238069e846774365eaaa239f825e06b6552702194",
    },
    "Mathlib/Util/AssertNoSorry.lean": {
        "blob": "060d8a764d2a6d1d2963d9c500b6084a05bed534",
        "source_sha256": "aa9f7bebacafc688c894ef2171930e51ed19e0dfe722581848a2414d28900d4d",
        "olean_sha256": "c8bf37753d9bad47b9fe67e32436da8b9af516a4abbbe14e74726f01ba2fb30b",
        "ilean_sha256": "fe68271493b88a6aaf132a1168b503f3faf470c3a91852d9233d7e014e10b403",
    },
    "Mathlib/Util/PrintSorries.lean": {
        "blob": "24d72cc680fa8b07f0d1062f670a5a824934a227",
        "source_sha256": "03670b0b0007740e5390dadd49c3d10a02b7d0919092d2b3214ef8a6a8cf798f",
        "olean_sha256": "9bcc4076e0aee5febb2eea5cf9dc959f38526e9f974afdfdd8658bfd318d5bb7",
        "ilean_sha256": "7792c84ebb36aa121cd5709b843add274df463d852d191439e6be55e33525b5d",
    },
}
LEAN_MODULES = ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean")
AXIOM_DECLARATIONS = {
    "Statement.lean": ("maxFlowMinCutTarget_iff_expanded",),
    "ObligationTree.lean": ("cutCertificate_compose", "compose_root", "root_of_terminal"),
    "Proof.lean": (
        "weakDuality_proof",
        "noChain_case",
        "cutCertificate_of_equalCut",
        "root_of_maximalFlowAttainment_and_equalCut",
    ),
    "Validation.lean": (
        "weakDuality_proof",
        "noChain_case",
        "cutCertificate_of_equalCut",
        "root_of_maximalFlowAttainment_and_equalCut",
    ),
}
PROVISIONAL_IDS = ["M0814-L-WEAK-DUALITY"]
PARTIAL_IDS = ["M0814-B-NO-CHAIN"]
CONDITIONAL_IDS = ["M0814-T-CUT-CERT", "M0814-T-ASSEMBLE"]
REMAINING_CUT = ["M0814-L-MAX-ATTAIN", "M0814-T-EQUAL-CUT"]
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/Validation.lean",
    f"Stage1_Instances/{THEOREM}/check_validation.py",
    f"Stage1_Instances/{THEOREM}/validation-blocker.json",
    f"Stage1_Instances/{THEOREM}/validation-phase.md",
    f"Stage1_Instances/{THEOREM}/validation-receipt.json",
    f"Stage1_Instances/{THEOREM}/validation-spec.json",
}
SUMMARY_LINES = (
    "PASS THM-M-0814 narrow validation",
    "PASS network-isolated trust-zero replay: exact statement, conditional composition, four proof declarations, and trust probe elaborated",
    "PASS trust observation: twelve reports list exactly propext, Classical.choice, and Quot.sound; transitive closure has no unexpected bodyless or unsafe declaration",
    "PASS selected provenance: frozen local inputs, clean mathlib pin, seven selected source/blob/olean/ilean identities, license, and tool identities agree",
    "OPEN exact root H1/M3/R4: maximum-flow attainment and equal-cut construction remain unproved; audit_complete=false; theorem_complete=false",
    "FAIL CLOSED authority: proof is worker-provisional and not master-accepted",
    "FAIL CLOSED release: complete trust/provenance, cold empty-cache offline replay, and distinct signed independent verification are absent",
)
STARTED = time.monotonic()
RECIPE_TIMEOUT_SECONDS = 600.0


if sys.flags.optimize:
    raise SystemExit("validation failed: Python optimization disables fail-closed assertions")


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


def run(
    argv: list[str],
    *,
    cwd: Path = ROOT,
    env: dict[str, str] | None = None,
    timeout: float | None = None,
) -> str:
    remaining = RECIPE_TIMEOUT_SECONDS - (time.monotonic() - STARTED)
    if remaining <= 0:
        raise TimeoutError("validation recipe exceeded its 600-second wall-clock bound")
    limit = remaining if timeout is None else min(remaining, timeout)
    result = subprocess.run(
        argv,
        cwd=cwd,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=limit,
        check=False,
    )
    if result.returncode:
        raise RuntimeError(f"command failed ({result.returncode}): {argv!r}\n{result.stdout}")
    return result.stdout


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["/usr/bin/git", *args], cwd=cwd, timeout=30).strip()


def code_without_comments_and_strings(source: str) -> str:
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
            output.append("\n" if char == "\n" else " ")
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
            newline = source.find("\n", index)
            if newline < 0:
                output.extend(" " * (len(source) - index))
                index = len(source)
            else:
                output.extend(" " * (newline - index))
                index = newline
        elif char == '"':
            in_string = True
            output.append(" ")
            index += 1
        else:
            output.append(char)
            index += 1
    assert depth == 0 and not in_string, "unterminated Lean comment or string"
    return "".join(output)


def printed_axioms(output: str, declaration: str) -> set[str]:
    pattern = re.escape(f".{declaration}' depends on axioms: [") + r"(.*?)]"
    matches = re.findall(pattern, output, flags=re.DOTALL)
    assert len(matches) == 1, (declaration, len(matches))
    return {part.strip() for part in matches[0].split(",") if part.strip()}


def printed_expression_sha256(output: str, declaration: str) -> str:
    pattern = rf"(?:def|structure) {re.escape(declaration)}"
    match = re.search(pattern, output)
    assert match is not None, f"missing explicit printed expression for {declaration}"
    serialized = output[match.start():].strip()
    assert "?m." not in serialized, f"unresolved metavariable in {declaration}"
    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()


def replay_lean(lean: Path, lean_path: str, bwrap: Path) -> tuple[
    dict[str, str], dict[str, str], dict[str, str]
]:
    outputs: dict[str, str] = {}
    with tempfile.TemporaryDirectory(prefix="m0814-validation-", dir="/tmp") as tmp_name:
        tmp = Path(tmp_name).resolve()
        for name in LEAN_MODULES:
            shutil.copy2(HERE / name, tmp / name)
        home = tmp / "home"
        home.mkdir()
        sandbox = [
            str(bwrap),
            "--ro-bind", "/", "/",
            "--bind", str(tmp), str(tmp),
            "--dev", "/dev",
            "--proc", "/proc",
            "--unshare-net",
            "--die-with-parent",
            "--clearenv",
            "--setenv", "HOME", str(home),
            "--setenv", "LANG", "C.UTF-8",
            "--setenv", "LC_ALL", "C.UTF-8",
            "--setenv", "TZ", "UTC",
            "--setenv", "LEAN_NUM_THREADS", "1",
            "--chdir", str(tmp),
        ]

        def replay(name: str, include_local: bool) -> str:
            module_path = f"{tmp}:{lean_path}" if include_local else lean_path
            return run(
                sandbox + [
                    "--setenv", "LEAN_PATH", module_path,
                    str(lean), "--root", str(tmp), "--trust=0", "-t0",
                    "-o", str(tmp / Path(name).with_suffix(".olean")), str(tmp / name),
                ],
                timeout=300,
            )

        outputs["Statement.lean"] = replay("Statement.lean", False)
        outputs["ObligationTree.lean"] = replay("ObligationTree.lean", True)
        outputs["Proof.lean"] = replay("Proof.lean", True)
        outputs["Validation.lean"] = replay("Validation.lean", True)
        olean_hashes = {
            name: sha256(tmp / Path(name).with_suffix(".olean")) for name in LEAN_MODULES
        }
        assert olean_hashes == {
            "Statement.lean": "d2a8fe23862122b7ff6aa22a9c9ab0b7c5126af71ba03b2a303487002a9f741d",
            "ObligationTree.lean": "d08b1ce3796315cd36fcab7d6edfdd83cf687d2bbb0b463b560acfd73eb33319",
            "Proof.lean": "00b6f67182c7d551e3071dcda874d92489a84a0648c836db74f0317f0cc251ba",
            "Validation.lean": "8cd4b428c46d9ce811786eda2b09be10720c0f09ac15524a9378e99629d3cf90",
        }
    output_hashes = {
        name: hashlib.sha256(output.encode("utf-8")).hexdigest()
        for name, output in outputs.items()
    }
    return outputs, olean_hashes, output_hashes


def verify_generated_finsupp_dependency(lean: Path, lean_path: str, bwrap: Path) -> str:
    """Rebuild the direct Finsupp module so the proof is not trusted to a warm-only declaration."""
    relative = "Mathlib/Algebra/BigOperators/Finsupp/Basic.lean"
    source = (MATHLIB / relative).read_text(encoding="utf-8")
    assert re.search(
        r"@\[to_additive(?:\s+\([^]]*\))?\]\s*\n"
        r"theorem prod_finsetProd_comm\b",
        source,
    ), "missing source generator for Finsupp.sum_finsetSum_comm"
    with tempfile.TemporaryDirectory(prefix="m0814-finsupp-source-", dir="/tmp") as tmp_name:
        tmp = Path(tmp_name).resolve()
        overlay = tmp / "overlay"
        warm_root = MATHLIB / ".lake/build/lib/lean"
        target_relative = Path(relative).with_suffix(".olean")

        def mirror_spine(source: Path, destination: Path, parts: tuple[str, ...]) -> None:
            destination.mkdir()
            next_part = parts[0]
            for child in source.iterdir():
                if child.name != next_part:
                    (destination / child.name).symlink_to(child)
            if len(parts) > 1:
                mirror_spine(source / next_part, destination / next_part, parts[1:])

        mirror_spine(warm_root, overlay, target_relative.parts)
        output = overlay / target_relative
        module = MATHLIB / relative
        home = tmp / "home"
        home.mkdir()
        sandbox = [
            str(bwrap),
            "--ro-bind", "/", "/",
            "--bind", str(tmp), str(tmp),
            "--dev", "/dev",
            "--proc", "/proc",
            "--unshare-net",
            "--die-with-parent",
            "--clearenv",
            "--setenv", "HOME", str(home),
            "--setenv", "LANG", "C.UTF-8",
            "--setenv", "LC_ALL", "C.UTF-8",
            "--setenv", "TZ", "UTC",
            "--setenv", "LEAN_NUM_THREADS", "1",
            "--chdir", str(tmp),
        ]
        run(
            sandbox + [
                "--setenv", "LEAN_PATH", lean_path,
                str(lean), "--root", str(MATHLIB), "--trust=0", "-t0",
                "-o", str(output), str(module),
            ],
            timeout=300,
        )
        probe = tmp / "Probe.lean"
        probe.write_text(
            "import Mathlib.Algebra.BigOperators.Finsupp.Basic\n"
            "#check Finsupp.sum_finsetSum_comm\n"
            "#print Finsupp.sum_finsetSum_comm\n"
            "#print axioms Finsupp.sum_finsetSum_comm\n",
            encoding="utf-8",
        )
        probe_output = run(
            sandbox + [
                "--setenv", "LEAN_PATH", f"{overlay}:{lean_path}",
                str(lean), "--root", str(tmp), "--trust=0", "-t0", str(probe),
            ],
            timeout=300,
        )
        assert "Finsupp.sum_finsetSum_comm" in probe_output
        assert "Finset.sum_comm" in probe_output
        assert printed_axioms(probe_output, "sum_finsetSum_comm") == ALLOWED_AXIOMS
        return hashlib.sha256(probe_output.encode("utf-8")).hexdigest()


def main() -> None:
    os.umask(0o022)
    os.environ["LANG"] = "C.UTF-8"
    os.environ["LC_ALL"] = "C.UTF-8"
    os.environ["TZ"] = "UTC"

    spec = load(HERE / "validation-spec.json")
    receipt = load(HERE / "validation-receipt.json")
    blocker = load(HERE / "validation-blocker.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")
    instance = load(HERE / "instance.json")
    statement = load(HERE / "statement.json")
    anchor = load(HERE / "anchor-audit.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    frozen_specs = load(HERE / "validation-specs.json")
    local_tasks = load(HERE / "task-dag.json")
    proof_receipt = load(HERE / "proof-receipt.json")
    proof_blocker = load(HERE / "proof-blocker.json")
    targets = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target == {
        "execution_rank": 1373,
        "legacy_priority_slot": None,
        "theorem_id": THEOREM,
        "name": "\u6700\u5927\u6d41\u6700\u5c0f\u5272\u5b9a\u7406",
        "category": "\u7ec4\u5408\u6570\u5b66 / \u56fe\u8bba",
        "source_status_untrusted": "\u5df2\u9a8c\u8bc1",
        "baseline": "L0",
        "rework_required": True,
        "legacy_artifacts_accepted": False,
        "target_lane": "hard_statement_first_partial_verification",
        "intake_score": 86,
        "lifecycle_mode": "planned",
        "theorem_complete": False,
    }
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item == {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 1373,
        "phase": "validation",
        "layer": 5,
        "state": "[ ]",
        "depends_on": ["S56-M-0814-PROOF"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Run hermetic kernel, trust, provenance, and independent validation gates.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }
    predecessor = next(row for row in execution["items"] if row["id"] == "S56-M-0814-PROOF")
    assert predecessor["state"] == "[_]" and predecessor["attempts"] == 1

    for name, expected in EXPECTED_INPUTS.items():
        assert sha256(HERE / name) == expected, f"stale validation input: {name}"
    for relative, expected in REPO_INPUTS.items():
        assert sha256(ROOT / relative) == expected, f"stale repository input: {relative}"

    formal = statement["canonical_formal_target"]
    assert formal["declaration_or_expression"] == "Stage1Instances.THM_M_0814.MaxFlowMinCutTarget"
    assert formal["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert formal["statement_file_sha256"] == EXPECTED_INPUTS["Statement.lean"]
    assert instance["lifecycle"] == instance["lifecycle_mode"] == "planned"
    assert instance["root_vector"] == {"H": "H1", "M": "M3", "R": "R4"}
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == []
    assert instance["audit_complete"] is instance["theorem_complete"] is False
    assert anchor["audit_result"]["exact_proof_candidate_located"] is False
    assert anchor["audit_result"]["theorem_complete"] is False
    assert registry["root_obligation_id"] == "M0814-ROOT"
    assert registry["denominator_sha256"] == graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    by_id = {row["obligation_id"]: row for row in registry["obligations"]}
    for obligation_id in PROVISIONAL_IDS + PARTIAL_IDS + CONDITIONAL_IDS + REMAINING_CUT:
        assert obligation_id in by_id
        assert by_id[obligation_id]["terminal_proof_body_id"] is None
    closure = graphs["closure_boundary"]
    assert closure["closed_obligations"] == []
    assert closure["root_closed"] is closure["audit_complete"] is closure["theorem_complete"] is False
    assert closure["accepted_root_machine_debt"] == "M3"
    assert next(row for row in local_tasks["tasks"] if row["id"] == ITEM)["state"] == "open"
    assert local_tasks["accepted_states"] == []
    assert frozen_specs["item_id"] == "S56-M-0814-OBLIGATION_TREE"

    assert proof_receipt["accepted"] is False
    assert proof_receipt["proposed_state"] == "[_]"
    assert proof_receipt["provisionally_closed_obligation_ids"] == PROVISIONAL_IDS
    assert proof_receipt["partial_progress_toward_obligation_ids"] == PARTIAL_IDS
    assert proof_receipt["accepted_closed_obligation_ids"] == []
    assert proof_receipt["remaining_machine_root_cut_set"] == REMAINING_CUT
    assert proof_receipt["result"]["root_kernel_closed"] is False
    assert proof_receipt["result"]["theorem_complete"] is False
    assert set(proof_receipt["result"]["axioms"]) == ALLOWED_AXIOMS
    assert proof_blocker["root_closed"] is proof_blocker["audit_complete"] is False
    assert proof_blocker["theorem_complete"] is False

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|implemented_by|native_decide|run_tac|oracle)\b|"
        r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
        r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
        r"(?:axiom|constant|opaque|unsafe|extern)\b",
        flags=re.MULTILINE,
    )
    for name in LEAN_MODULES:
        code = code_without_comments_and_strings((HERE / name).read_text(encoding="utf-8"))
        assert prohibited.search(code) is None, f"prohibited proof construct in {name}"
    validation_code = code_without_comments_and_strings(
        (HERE / "Validation.lean").read_text(encoding="utf-8")
    )
    assert "theorem " not in validation_code
    assert "assert_no_sorry weakDuality_proof" in validation_code
    assert "#print_validation_closure" in validation_code
    assert not list(HERE.glob("*.olean")) and not list(HERE.glob("tmp*.lean"))

    manifest = load(LEAN_ROOT / "lake-manifest.json")
    mathlib_pin = next(row for row in manifest["packages"] if row["name"] == "mathlib")
    assert mathlib_pin["rev"] == mathlib_pin["inputRev"] == MATHLIB_REVISION
    assert MATHLIB.resolve().is_dir()
    assert git("rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert git("remote", "get-url", "origin", cwd=MATHLIB) == MATHLIB_REMOTE
    assert git("status", "--porcelain=v1", "--untracked-files=all", cwd=MATHLIB) == ""
    assert sha256(MATHLIB / "LICENSE") == MATHLIB_LICENSE_SHA256
    olean_root = MATHLIB / ".lake/build/lib/lean"
    for relative, expected in SELECTED_MATHLIB.items():
        source = MATHLIB / relative
        olean = olean_root / Path(relative).with_suffix(".olean")
        ilean = olean_root / Path(relative).with_suffix(".ilean")
        assert git("rev-parse", f"HEAD:{relative}", cwd=MATHLIB) == expected["blob"]
        assert sha256(source) == expected["source_sha256"]
        assert sha256(olean) == expected["olean_sha256"]
        assert sha256(ilean) == expected["ilean_sha256"]

    lake_name = shutil.which("lake")
    bwrap_name = shutil.which("bwrap")
    assert lake_name is not None and bwrap_name is not None
    lake = Path(lake_name).resolve()
    bwrap = Path(bwrap_name).resolve()
    python = Path(sys.executable).resolve()
    git_bin = Path("/usr/bin/git")
    bash = Path("/usr/bin/bash")
    assert sha256(lake) == LAKE_EXECUTABLE_SHA256
    assert sha256(bwrap) == BWRAP_EXECUTABLE_SHA256
    assert sha256(python) == PYTHON_EXECUTABLE_SHA256
    assert sha256(git_bin) == GIT_EXECUTABLE_SHA256
    assert sha256(bash) == BASH_EXECUTABLE_SHA256
    assert sha256(Path("/usr/bin/env")) == ENV_EXECUTABLE_SHA256
    lean = Path(run([str(lake), "env", "which", "lean"], cwd=LEAN_ROOT, timeout=60).strip())
    lean_path = run(
        ["/usr/bin/env", "-u", "LEAN_PATH", str(lake), "env", "printenv", "LEAN_PATH"],
        cwd=LEAN_ROOT,
        timeout=60,
    ).strip()
    assert lean.is_file() and sha256(lean) == LEAN_EXECUTABLE_SHA256
    lean_version = run([str(lean), "--version"], timeout=30)
    assert "Lean (version 4.29.0" in lean_version and LEAN_COMMIT in lean_version
    assert "Lake version 5.0.0" in run([str(lake), "--version"], cwd=LEAN_ROOT, timeout=30)

    finsupp_probe_sha256 = verify_generated_finsupp_dependency(lean, lean_path, bwrap)
    outputs, fresh_olean_hashes, lean_output_hashes = replay_lean(lean, lean_path, bwrap)
    report_count = 0
    for module, declarations in AXIOM_DECLARATIONS.items():
        for declaration in declarations:
            assert printed_axioms(outputs[module], declaration) == ALLOWED_AXIOMS
            report_count += 1
    assert report_count == 12
    assert outputs["Validation.lean"].count("Declarations are sorry-free!") == 1
    assert "VALIDATION_CLOSURE axioms=[propext, Classical.choice, Quot.sound]" in outputs["Validation.lean"]
    assert "VALIDATION_CLOSURE unexpected_bodyless=[]" in outputs["Validation.lean"]
    assert "VALIDATION_CLOSURE unsafe=[]" in outputs["Validation.lean"]
    closure_match = re.search(
        r"VALIDATION_CLOSURE declarations=(\d+) modules=(\d+)",
        outputs["Validation.lean"],
    )
    assert closure_match is not None
    closure_counts = {
        "declarations": int(closure_match.group(1)),
        "modules": int(closure_match.group(2)),
        "unexpected_bodyless": [],
        "unsafe": [],
    }
    assert closure_counts == {
        "declarations": 7726,
        "modules": 285,
        "unexpected_bodyless": [],
        "unsafe": [],
    }
    combined = "\n".join(outputs.values())
    assert "sorryAx" not in combined and "declaration uses 'sorry'" not in combined
    assert not re.search(r"(^|\n).*error(?:\([^)]*\))?:", combined)
    assert printed_expression_sha256(
        outputs["Statement.lean"],
        "Stage1Instances.THM_M_0814.MaxFlowMinCutTarget",
    ) == EXPRESSION_SHA256

    assert spec["schema_version"] == "stage1-validation-spec/1.0"
    assert spec["item_id"] == ITEM and spec["theorem_id"] == THEOREM
    assert spec["phase"] == "validation" and spec["intent"] == "validate"
    assert spec["argv"] == [
        "/usr/bin/python3", "-I", "-B", f"Stage1_Instances/{THEOREM}/check_validation.py"
    ]
    assert spec["network_policy"] == "explicitly_required" and spec["expected_exit"] == 0
    assert "--unshare-net" in spec["network_enforcement"]
    assert receipt["recipe"] == spec
    assert receipt["item_id"] == blocker["item_id"] == packet["item_id"] == ITEM
    assert receipt["base_revision"] == blocker["base_revision"] == packet["base_revision"] == BASE_REVISION
    assert receipt["base_tree"] == BASE_TREE
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["verdict"] == "blocked" and receipt["release_grade"] is False
    assert receipt["canonical_target_expression_sha256"] == EXPRESSION_SHA256
    assert receipt["registry_denominator_sha256"] == DENOMINATOR_SHA256
    expected_receipt_inputs = {
        **EXPECTED_INPUTS,
        **REPO_INPUTS,
        "check_validation.py": sha256(HERE / "check_validation.py"),
        "validation-phase.md": sha256(HERE / "validation-phase.md"),
    }
    assert receipt["inputs"] == expected_receipt_inputs
    assert receipt["provisionally_validated_obligation_ids"] == PROVISIONAL_IDS
    assert receipt["validated_partial_progress_toward_obligation_ids"] == PARTIAL_IDS
    assert receipt["conditional_composition_ids"] == CONDITIONAL_IDS
    assert receipt["accepted_closed_obligation_ids"] == receipt["accepted_receipt_ids"] == []
    assert receipt["remaining_machine_root_cut_set"] == REMAINING_CUT
    assert receipt["root_vector_before"] == receipt["root_vector_after"] == instance["root_vector"]
    assert receipt["first_failed_gate"] == (
        "dependency.S56-M-0814-PROOF.master_acceptance_and_exact_root_closure"
    )
    assert receipt["first_failed_theorem_gate"] == "proof.M0814-L-MAX-ATTAIN"
    assert receipt["first_failed_release_gate"] == "S56-7.3-TRANSITIVE-PROVENANCE-CLOSURE"
    assert receipt["result"]["root_kernel_closed"] is False
    assert receipt["result"]["validation_phase_complete"] is False
    assert receipt["result"]["complete_transitive_foundation_tcb_provenance"] == "fail_closed"
    assert receipt["result"]["hermetic_cold_empty_cache_offline_replay"] == "fail_closed"
    assert receipt["result"]["independent_distinct_runner"] == "fail_closed"
    assert receipt["result"]["audit_complete"] is receipt["result"]["theorem_complete"] is False
    assert receipt["execution"]["fresh_olean_sha256"] == fresh_olean_hashes
    expected_output_hashes = receipt["execution"]["lean_stdout_sha256"]
    assert set(expected_output_hashes) == set(LEAN_MODULES)
    assert all(re.fullmatch(r"[0-9a-f]{64}", value) for value in expected_output_hashes.values())
    assert expected_output_hashes == lean_output_hashes
    assert re.fullmatch(
        r"[0-9a-f]{64}", receipt["execution"]["finsupp_probe_stdout_sha256"]
    )
    assert receipt["execution"]["finsupp_probe_stdout_sha256"] == finsupp_probe_sha256
    assert receipt["execution"]["validation_transitive_closure"] == closure_counts
    assert receipt["execution"]["axiom_report_count"] == report_count == 12
    assert receipt["execution"]["summary_sha256"] == hashlib.sha256(
        ("\n".join(SUMMARY_LINES) + "\n").encode("utf-8")
    ).hexdigest()
    final_replay = receipt["execution"]["final_checker_replay"]
    assert final_replay["exit_code"] == 0
    assert final_replay["output"] == "exact seven-line summary whose SHA-256 is recorded below"
    assert final_replay["duration_seconds"] > 0
    assert receipt["validated_at"] == receipt["freshness"]["validated_at"] == final_replay["ended_at"]
    assert blocker["recorded_at"] == final_replay["ended_at"]
    selected_boundaries = receipt["selected_provenance"][
        "selected_source_blob_olean_ilean_boundaries"
    ]
    assert selected_boundaries == {
        relative: [
            values["blob"], values["source_sha256"],
            values["olean_sha256"], values["ilean_sha256"],
        ]
        for relative, values in SELECTED_MATHLIB.items()
    }
    assert receipt["environment"]["lean_executable_sha256"] == sha256(lean)
    assert receipt["environment"]["lake_executable_sha256"] == sha256(lake)
    assert receipt["environment"]["bubblewrap_executable_sha256"] == sha256(bwrap)
    assert blocker["outcome"] == "validation_packet_self_tested_gates_blocked"
    assert blocker["validation_phase_complete"] is False
    assert blocker["root_closed"] is blocker["audit_complete"] is blocker["theorem_complete"] is False
    assert blocker["remaining_machine_root_cut_set"] == REMAINING_CUT
    assert blocker["remaining_machine_root_cut_set_scope"] == receipt[
        "remaining_machine_root_cut_set_scope"
    ]
    assert blocker["validation_receipt_id"] == receipt["receipt_id"]
    assert blocker["provisionally_validated_obligation_ids"] == PROVISIONAL_IDS
    assert blocker["validated_partial_progress_toward_obligation_ids"] == PARTIAL_IDS
    assert blocker["conditional_composition_ids"] == CONDITIONAL_IDS
    assert blocker["accepted_closed_obligation_ids"] == []
    assert blocker["root_vector_before"] == blocker["root_vector_after"] == instance["root_vector"]
    for field in (
        "first_failed_gate", "first_failed_theorem_gate", "first_failed_release_gate",
        "retry_condition", "status_boundary",
    ):
        assert blocker[field] == receipt[field]

    assert set(packet) == {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert packet["state"] == "[_]"
    assert set(packet["changed_paths"]) == set(receipt["changed_paths"]) == CHANGED_PATHS
    assert packet["known_failures"] == receipt["known_failures"]
    assert packet["commands"] == [row["argv"] for row in receipt["commands"]]
    assert packet["output_summary"] == "\n".join(SUMMARY_LINES)

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
