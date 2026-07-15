#!/usr/bin/env python3
"""Fail-closed narrow validation for S56-M-0957-VALIDATION."""

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
HERE = ROOT / "Stage1_Instances" / "THM-M-0957"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM = "S56-M-0957-VALIDATION"
THEOREM = "THM-M-0957"
BASE_REVISION = "d6616cc60ad980c635f22ef840e9c5db2ebcab50"
BASE_TREE = "d6f3c3aedec26191f09878fd6eb1fec666adf318"
EXPRESSION_SHA256 = "e611db43ce6f3419553e3ebe0fe85a3ce89e4d3930b3842f5a09be8a7683d2ed"
DENOMINATOR_SHA256 = "84f7eaea7de3659e4324dc64f7849fde4024dd057d4d320c879b0b59dd692a63"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MATHLIB_REMOTE = "https://github.com/leanprover-community/mathlib4.git"
MATHLIB_LICENSE_SHA256 = "b40930bbcf80744c86c46a12bc9da056641d722716c378f5659b9e555ef833e1"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
LEAN_TOOLCHAIN = "leanprover/lean4:v4.29.0"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
MACHINE_IDS = [
    "M0957-ROOT",
    "M0957-S-PREDICATE",
    "M0957-S-EXTREMAL",
    "M0957-T-ASSEMBLE",
    "M0957-T-CONSTRUCTION",
    "M0957-N-SHARP-DIMENSION",
    "M0957-L-RADIX-NONZERO",
    "M0957-T-PARAM-ADMISSIBLE",
    "M0957-L-RADIX-FLOOR",
    "M0957-L-AMBIENT-FIT",
    "M0957-N-RPOW-EXP",
    "M0957-L-OPTIMAL-EXPONENT",
    "M0957-L-PROXY-LOG",
    "M0957-L-PROXY-RPOW-IDENTITY",
    "M0957-L-PROXY-SLACK",
    "M0957-L-RECIPROCAL-LOSS",
    "M0957-L-RECIPROCAL-CORE",
    "M0957-L-LINEAR-LOSS",
    "M0957-L-LINEAR-CEILING",
    "M0957-L-LINEAR-INCREMENT",
    "M0957-L-SUBLEADING-LOSS",
    "M0957-L-DIMENSION-SLACK",
    "M0957-L-LOG-DIMENSION",
    "M0957-T-PROXY-ASYMPTOTIC",
    "M0957-T-RATIO-ASYMPTOTIC",
    "M0957-T-SHARP-ESTIMATE",
    "M0957-T-SHARP-PARAMETERS",
    "M0957-N-INCLUSIVE-INDEX",
]
TRUST_DECLARATIONS = [
    "Stage1Instances.THM_M_0957.sourceThreeAPFree_iff_threeAPFree",
    "Stage1Instances.THM_M_0957.behrendConstructionTarget_iff_finiteSet",
    "Behrend.bound_aux",
    "Stage1Instances.THM_M_0957_ObligationTree.dimensionControl_proof",
    "Stage1Instances.THM_M_0957_ObligationTree.rpowNormalization_proof",
    "Stage1Instances.THM_M_0957_ObligationTree.proxyRpowIdentity_proof",
    "Stage1Instances.THM_M_0957_ObligationTree.proxySlackAbsorption_proof",
    "Stage1Instances.THM_M_0957_ObligationTree.ambientFit_proof",
    "Stage1Instances.THM_M_0957_ObligationTree.linearCeiling_proof",
    "Stage1Instances.THM_M_0957_ObligationTree.linearIncrementAbsorption_proof",
    "Stage1Instances.THM_M_0957_ObligationTree.dimensionSlack_proof",
    "Stage1Instances.THM_M_0957_ObligationTree.logDimensionLoss_proof",
    "Stage1Instances.THM_M_0957_ObligationTree.reciprocalBalancedCore_proof",
    "Stage1Instances.THM_M_0957_ObligationTree.reciprocalDimensionLoss_proof",
    "Stage1Instances.THM_M_0957_ObligationTree.radixBase_eventually_one",
    "Stage1Instances.THM_M_0957_ObligationTree.radixNonzero_proof",
    "Stage1Instances.THM_M_0957_ObligationTree.radixFloor_proof",
    "Stage1Instances.THM_M_0957_ObligationTree.quantitativeConstruction_installed",
    "Stage1Instances.THM_M_0957_ObligationTree.indexMonotonicity_installed",
    "Stage1Instances.THM_M_0957_ObligationTree.parameterAdmissibility_proof",
    "Stage1Instances.THM_M_0957_ObligationTree.proxyLogLower_proof",
    "Stage1Instances.THM_M_0957_ObligationTree.linearDimensionLoss_proof",
    "Stage1Instances.THM_M_0957_ObligationTree.subleadingLoss_proof",
    "Stage1Instances.THM_M_0957_ObligationTree.optimalExponentBridge_proof",
    "Stage1Instances.THM_M_0957_ObligationTree.proxyAsymptotic_proof",
    "Stage1Instances.THM_M_0957_ObligationTree.ratioAsymptotic_proof",
    "Stage1Instances.THM_M_0957_ObligationTree.sharpEstimate_proof",
    "Stage1Instances.THM_M_0957_ObligationTree.sharpParameter_proof",
    "Stage1Instances.THM_M_0957_ObligationTree.exactAssembly_proof",
    "Stage1Instances.THM_M_0957_ObligationTree.exactRoot_proof",
    "Stage1Instances.THM_M_0957_ObligationTree.behrendConstructionTarget_proof",
]
EXPECTED_INPUTS = {
    "Statement.lean": "b4bda6c926b0568d8b244623c12b4784651d55a9eb7df9d9ba3f512ed2cd9e46",
    "ObligationTree.lean": "efbe7ff68dac5f55bd98fbc00339a3850dfc2c1935f1cde4cf5c7eefe1224223",
    "Proof.lean": "fd8e72e675c88d8dc17b9a64764d4c17a45b462b0689140453cf45463bc024e2",
    "statement.json": "b70cb423c41c9d822b85696a57193ca0fc2dc26fe88b2a471bb68f6a9cb8dfab",
    "instance.json": "1291982f7e8f15eca9d00cb6f77d28a1035a97b9851d0b105fd54a2fd4ef4b5f",
    "task-dag.json": "e5631d9c3c802b3d454a487862c4cbf593893061b75415c96551954a32ae1b86",
    "anchor-audit.json": "10eff04369551920531fcacb97521ba95f0e0ee45483e8d66ba4e58e49a24423",
    "obligation-registry.json": "75896bc70b85e96fca7bc0ae9e08da4c30cf6c0fb5cecf33cfda6d37eee0e39c",
    "typed-graphs.json": "7b951fc5715c3c4d5d88b210acc355cb98a0ace927a638951803efb95362dde0",
    "validation-specs.json": "116fb87db35ca024c1ed76d411c1044002cf7ad8f6c8f216a552b90bdf783cfe",
    "proof-receipt.json": "7ed071053e8b7237d95274e0c448366c916253b69a347c848c38f17802f60448",
    "source-statement-crosswalk.md": "a71cfdc4815783314661aa21b38753dbaca921fc4e18922029a9e122d2719113",
    "Validation.lean": "091c0ed8d216e623c51a3f594711eb29e270f4cc3b63172ec931af39aeb59347",
    "check_validation.sh": "7a5c4a671d28b988bbe66567c630678aa0e3fe981fea713e6a3022f3932f722b",
    "validation-spec.json": "4ad216b2511871a109279f9c487a59ef39adb2ebc654cce0a3974597b952e03d",
}
POLICY_INPUTS = {
    "Docs/Stage1_Blueprint_rev-5.6.md": "4d1e2a36d95567a14194a24e43f43093e87e8a4feb6d75f8d5f295607ad34b56",
    "Docs/Stage1_Execution_DAG_rev-5.6.json": "a57538aeee6a0ba948bbcc0ca421ce8cf19014e952e8b25d304c2e5517d270ba",
    "Docs/Stage1_Targets_rev-5.6.json": "02eec284de534dd78e1cf75f82a477ff477567dd682b7445cb7587abd137ab2c",
    "skills/execute-stage1-rev56/SKILL.md": "26d47a66c6535feabb8bbf1051fd55d76a53fe761f4b3d953f86b97ec86152b8",
    "Formalizations/Lean/lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "Formalizations/Lean/lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
    "Formalizations/Lean/lakefile.lean": "43259bbc1b42b1574b78c8584753029dc5e118c0a0e752ac0a5bad9004b4dcda",
}
MATHLIB_BOUNDARIES = {
    "Mathlib/Combinatorics/Additive/AP/Three/Behrend.lean": (
        "7d3eb0e603040dcd72fe35e39c82f4d615b3e254",
        "1f8c1813a75c722ee4d62d63185c53d0b52d27691e531c05e0ecb6c10c15cf65",
        "620e1ce9b071dd2049ce734f4e58bc1e2bbdb6fb9bf9f6e17f1b39ad34bb720f",
        "cfee04d139cac6f7c21da8ccd365033c24020e63c75de5bd75b45985d6452ec9",
    ),
    "Mathlib/Combinatorics/Additive/AP/Three/Defs.lean": (
        "534177a2aa83fa462689226e248953fe38f2e1cc",
        "b325fb632a5398208995fa5beae71c47798086e588f98e46679aa81b923b28e3",
        "19cbfd0bcf347073590f8f60d2aa288874a3fbe3f7c73fda5ade9b1b702bee8c",
        "660e1a59863cf5507489e5c60102b9fce0195449e20ca953ffb33f120a967466",
    ),
    "Mathlib/Analysis/SpecialFunctions/Pow/Asymptotics.lean": (
        "ceabfd6cfcd5054399f02c05830f8b34468527e2",
        "0101f3f891a5ca9af748ee04d69be4c5af5aeed8201b00486bee842d986326e0",
        "ccbffeb3bbfeb8767a77612bb967ec9a28ae6535edf8c00bd8bb64913bb4f8bb",
        "d6c5f72c5e89f9ce8e0b6ecb1b270b995e7dba901b02ebffb578038fea2f4195",
    ),
    "Mathlib/Analysis/SpecialFunctions/Pow/Real.lean": (
        "d33cde833bb5b015daa4c059f024e87987ddc149",
        "4bc70fd7fa295428b59e9d5de98650a98eb4e87f6614d42f5d5d55ccc9d33398",
        "d161223f24657bf0321ea05c65e5012d00a9fc634da7113b220c710d62c1d3f4",
        "e54d3974152af929a147075b91e446a647520d0818d8ca9a706a744ad7d2668f",
    ),
    "Mathlib/Util/AssertNoSorry.lean": (
        "060d8a764d2a6d1d2963d9c500b6084a05bed534",
        "aa9f7bebacafc688c894ef2171930e51ed19e0dfe722581848a2414d28900d4d",
        "c8bf37753d9bad47b9fe67e32436da8b9af516a4abbbe14e74726f01ba2fb30b",
        "fe68271493b88a6aaf132a1168b503f3faf470c3a91852d9233d7e014e10b403",
    ),
    "Mathlib/Util/PrintSorries.lean": (
        "24d72cc680fa8b07f0d1062f670a5a824934a227",
        "03670b0b0007740e5390dadd49c3d10a02b7d0919092d2b3214ef8a6a8cf798f",
        "9bcc4076e0aee5febb2eea5cf9dc959f38526e9f974afdfdd8658bfd318d5bb7",
        "7792c84ebb36aa121cd5709b843add274df463d852d191439e6be55e33525b5d",
    ),
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
    "PASS THM-M-0957 narrow validation",
    "PASS kernel: exact statement, both transports, complete proof route, and exact canonical root replayed at trust zero",
    "PASS trust observation: 31 declarations are sorry-free; root axioms are exactly propext, Classical.choice, and Quot.sound",
    "PASS closure observation: 28337 declarations in 1086 modules; no unexpected bodyless or unsafe declarations",
    "PASS selected provenance: local bodies, bound_aux source/blob/olean/ilean, pins, license, and tool identities agree",
    "FAIL CLOSED authority: proof is provisional and frozen graph/task records predate it; accepted root remains H1/M3/R3",
    "FAIL CLOSED complete trust/provenance: planned fingerprints, accepted foundation policy, full TCB, SBOM, and archive are absent",
    "FAIL CLOSED hermetic release: shared warm .lake is not a clean-checkout empty-cache offline replay or deterministic bundle",
    "FAIL CLOSED independent release: trust probe shares this worker, checkout, kernel, and cache; no distinct signed verifier exists",
    "audit_complete=false; theorem_complete=false",
)
RECIPE_STARTED = time.monotonic()
RECIPE_TIMEOUT_SECONDS = 900.0


if sys.flags.optimize:
    raise SystemExit("validation failed: Python optimization disables assertions")


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
    argv: list[str], *, cwd: Path = ROOT, env: dict[str, str] | None = None
) -> str:
    remaining = RECIPE_TIMEOUT_SECONDS - (time.monotonic() - RECIPE_STARTED)
    if remaining <= 0:
        raise TimeoutError("validation recipe exceeded its 900-second bound")
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
        raise RuntimeError(
            f"validation failed ({result.returncode}): {argv!r}\n{result.stdout}"
        )
    return result.stdout


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["/usr/bin/git", *args], cwd=cwd).strip()


def elan_binary(name: str) -> Path:
    elan = Path("/home/sansha-2/.elan/bin/elan")
    assert elan.is_file() and sha256(elan) == (
        "840179e70803ef373c2ec53342d6a45ea7d022533e4145489fc1278b4f716385"
    )
    env = {
        "HOME": "/home/sansha-2",
        "PATH": "/usr/bin:/bin",
        "ELAN_TOOLCHAIN": LEAN_TOOLCHAIN,
    }
    result = subprocess.run(
        [str(elan), "which", name],
        cwd=LEAN_ROOT,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=30,
        check=False,
    )
    if result.returncode:
        raise RuntimeError(f"cannot resolve pinned {name}: {result.stdout}")
    path = Path(result.stdout.strip())
    assert path.is_file(), f"pinned {name} executable missing"
    return path


def canonical_json_sha256(value: object) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def exact_git_status(cwd: Path = ROOT) -> str:
    output = run(
        ["/usr/bin/git", "status", "--porcelain=v1", "--untracked-files=all"],
        cwd=cwd,
    )
    return output.removesuffix("\n")


def selected_mathlib_snapshot() -> dict[str, object]:
    boundaries: dict[str, list[str]] = {}
    for relative in MATHLIB_BOUNDARIES:
        source = MATHLIB / relative
        compiled = MATHLIB / ".lake/build/lib/lean" / Path(relative).with_suffix("")
        boundaries[relative] = [
            git("rev-parse", f"HEAD:{relative}", cwd=MATHLIB),
            sha256(source),
            sha256(compiled.with_suffix(".olean")),
            sha256(compiled.with_suffix(".ilean")),
        ]
    return {
        "revision": git("rev-parse", "HEAD", cwd=MATHLIB),
        "tree": git("rev-parse", "HEAD^{tree}", cwd=MATHLIB),
        "remote": git("remote", "get-url", "origin", cwd=MATHLIB),
        "status": exact_git_status(MATHLIB),
        "license_sha256": sha256(MATHLIB / "LICENSE"),
        "selected_boundaries": boundaries,
    }


def validation_input_manifest() -> list[dict[str, object]]:
    entries: list[dict[str, object]] = [
        {
            "path": "Formalizations/Lean/.lake",
            "kind": "symlink",
            "target_sha256": hashlib.sha256(
                os.readlink(LEAN_ROOT / ".lake").encode()
            ).hexdigest(),
        }
    ]
    # Receipt and worker packet are outputs. Excluding both avoids a recursive
    # digest while every executable/source/spec input remains byte-bound.
    for relative in sorted(CHANGED_PATHS - {
        ".stage1-worker-selftest.json",
        f"Stage1_Instances/{THEOREM}/validation-receipt.json",
    }):
        path = ROOT / relative
        entries.append({
            "path": relative,
            "kind": "file",
            "mode": oct(path.stat().st_mode & 0o777),
            "sha256": sha256(path),
            "size": path.stat().st_size,
        })
    return entries


def fresh_expression_sha256(lean: Path, lean_path: str) -> str:
    source = (HERE / "Statement.lean").read_text(encoding="utf-8")
    marker = (
        "#print Stage1Instances.THM_M_0957.BehrendConstructionTarget"
    )
    assert source.count(marker) == 1
    with tempfile.TemporaryDirectory(
        prefix="stage1-m0957-expression-", dir="/tmp"
    ) as tmp_name:
        tmp = Path(tmp_name)
        fixture = tmp / "Statement.lean"
        fixture.write_text(source, encoding="utf-8")
        output = run(
            [
                "/usr/bin/bwrap", "--ro-bind", "/", "/",
                "--bind", str(tmp), str(tmp), "--dev", "/dev", "--proc", "/proc",
                "--unshare-net", "--die-with-parent", "--clearenv",
                "--setenv", "HOME", str(tmp),
                "--setenv", "PATH", f"{lean.parent}:/usr/bin:/bin",
                "--setenv", "LANG", "C.UTF-8", "--setenv", "LC_ALL", "C.UTF-8",
                "--setenv", "TZ", "UTC", "--setenv", "LEAN_NUM_THREADS", "1",
                "--setenv", "LEAN_PATH", lean_path, "--chdir", str(LEAN_ROOT),
                str(lean), "--trust=0", "-t0", str(fixture),
            ],
            cwd=LEAN_ROOT,
        )
    match = re.search(
        r"def Stage1Instances\.THM_M_0957\.BehrendConstructionTarget\b",
        output,
    )
    assert match is not None
    printed = output[match.start():].strip()
    assert ":=\n" in printed
    serialized = printed.split(":=\n", 1)[1].strip()
    for boundary in (
        "\nType mismatch\n",
        "\n'Stage1Instances.THM_M_0957.sourceThreeAPFree_iff_threeAPFree'",
    ):
        serialized = serialized.split(boundary, 1)[0].strip()
    assert "?m." not in serialized and "sorryAx" not in serialized
    return hashlib.sha256(serialized.encode()).hexdigest()


def code_without_comments_and_strings(source: str) -> str:
    output: list[str] = []
    index = 0
    block_depth = 0
    in_string = False
    escaped = False
    while index < len(source):
        pair = source[index:index + 2]
        char = source[index]
        if block_depth:
            if pair == "/-":
                block_depth += 1
                index += 2
            elif pair == "-/":
                block_depth -= 1
                index += 2
            else:
                index += 1
        elif in_string:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
            index += 1
        elif pair == "/-":
            block_depth = 1
            index += 2
        elif pair == "--":
            newline = source.find("\n", index)
            index = len(source) if newline < 0 else newline
        elif char == '"':
            in_string = True
            index += 1
        else:
            output.append(char)
            index += 1
    assert block_depth == 0 and not in_string
    return "".join(output)


def observed_axioms(output: str, declaration: str) -> set[str]:
    match = re.search(
        re.escape(f"'{declaration}' depends on axioms: [") + r"(.*?)]",
        output,
        re.DOTALL,
    )
    if match is None:
        assert f"'{declaration}' does not depend on any axioms" in output, declaration
        return set()
    return {part.strip() for part in match.group(1).split(",") if part.strip()}


def assert_text_hygiene(path: Path) -> None:
    data = path.read_bytes()
    assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())


def main() -> None:
    initial_root_status = exact_git_status()
    initial_manifest = validation_input_manifest()
    initial_manifest_sha256 = canonical_json_sha256(initial_manifest)
    initial_bound_hashes = {
        **{f"target:{name}": sha256(HERE / name) for name in EXPECTED_INPUTS},
        **{f"policy:{name}": sha256(ROOT / name) for name in POLICY_INPUTS},
        "target:check_validation.py": sha256(Path(__file__).resolve()),
        "target:validation-phase.md": sha256(HERE / "validation-phase.md"),
    }
    targets = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    statement = load(HERE / "statement.json")
    instance = load(HERE / "instance.json")
    task_dag = load(HERE / "task-dag.json")
    anchor = load(HERE / "anchor-audit.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    frozen_specs = load(HERE / "validation-specs.json")
    proof_receipt = load(HERE / "proof-receipt.json")
    spec = load(HERE / "validation-spec.json")
    receipt = load(HERE / "validation-receipt.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")

    initial_root_identity = {
        "revision": git("rev-parse", "HEAD"),
        "tree": git("rev-parse", "HEAD^{tree}"),
    }
    assert initial_root_identity == {
        "revision": BASE_REVISION,
        "tree": BASE_TREE,
    }
    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 1491 and target["baseline"] == "L0"
    assert target["lifecycle_mode"] == "planned"
    assert target["rework_required"] is True and target["theorem_complete"] is False
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item == {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 1491,
        "phase": "validation",
        "layer": 5,
        "state": "[ ]",
        "depends_on": ["S56-M-0957-PROOF"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Run hermetic kernel, trust, provenance, and independent validation gates.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }
    predecessor = next(row for row in execution["items"] if row["id"] == "S56-M-0957-PROOF")
    assert predecessor["state"] == "[_]" and predecessor["attempts"] == 1

    for name, expected in EXPECTED_INPUTS.items():
        assert sha256(HERE / name) == expected, f"stale validation input: {name}"
    for relative, expected in POLICY_INPUTS.items():
        assert sha256(ROOT / relative) == expected, f"changed policy input: {relative}"
    formal = statement["canonical_formal_target"]
    assert formal["declaration_or_expression"] == (
        "Stage1Instances.THM_M_0957.BehrendConstructionTarget"
    )
    assert formal["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert formal["statement_file_sha256"] == EXPECTED_INPUTS["Statement.lean"]
    assert registry["frozen_against_statement_sha256"] == EXPECTED_INPUTS["Statement.lean"]
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert registry["frozen_denominators"]["required_machine"] == MACHINE_IDS
    assert graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    closure = graphs["closure_boundary"]
    assert closure["accepted_closed_obligations"] == [] and closure["root_closed"] is False
    assert closure["accepted_root_machine_debt"] == "M3"
    assert closure["audit_complete"] is closure["theorem_complete"] is False
    assert instance["root_vector"] == {"H": "H1", "M": "M3", "R": "R3"}
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == []
    assert instance["audit_complete"] is instance["theorem_complete"] is False
    assert task_dag["accepted_states"] == [] and task_dag["theorem_complete"] is False

    assert proof_receipt["item_id"] == "S56-M-0957-PROOF"
    assert proof_receipt["accepted"] is False
    assert proof_receipt["canonical_target_expression_sha256"] == EXPRESSION_SHA256
    assert proof_receipt["registry_denominator_sha256"] == DENOMINATOR_SHA256
    proof_route_ids = proof_receipt["closed_obligation_ids"]
    assert len(proof_route_ids) == 26 and set(proof_route_ids) == (
        set(MACHINE_IDS) - {"M0957-S-PREDICATE", "M0957-S-EXTREMAL"}
    )
    assert proof_receipt["accepted_closed_obligation_ids"] == []
    assert proof_receipt["proof_body"]["source_sha256"] == EXPECTED_INPUTS["Proof.lean"]
    assert proof_receipt["result"]["root_kernel_closed"] is True
    assert proof_receipt["result"]["accepted_root_closed"] is False
    assert proof_receipt["result"]["theorem_complete"] is False
    assert len(proof_receipt["exact_declarations"]) == 27
    assert "radixBase_eventually_one" not in "\n".join(proof_receipt["exact_declarations"])
    assert any(
        row["statement_fingerprint"].startswith("planned:v1:")
        for row in registry["obligations"]
    )
    assert frozen_specs["item_id"] == "S56-M-0957-OBLIGATION_TREE"
    assert frozen_specs["recipes"][0]["recipe_id"] == "VAL-M0957-OBLIGATION-BUNDLE"
    assert frozen_specs["recipes"][0]["evidence_boundary"].startswith(
        "Provisional architecture self-test only"
    )
    assert anchor["provenance_packet"]["transitive_trust_closure_hash"] is None
    assert anchor["audit_complete"] is anchor["theorem_complete"] is False
    crosswalk = (HERE / "source-statement-crosswalk.md").read_text(encoding="utf-8")
    assert "not yet `H0`" in crosswalk

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by|extern|oracle)\b|"
        r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
        r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
        r"(?:axiom|constant|opaque|unsafe)\b",
        re.MULTILINE,
    )
    for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
        source = code_without_comments_and_strings((HERE / name).read_text(encoding="utf-8"))
        assert prohibited.search(source) is None, f"prohibited source token in {name}"
    validation = code_without_comments_and_strings((HERE / "Validation.lean").read_text())
    assert "import Proof" in validation
    assert "theorem " not in validation and "def " not in validation
    for declaration in TRUST_DECLARATIONS:
        assert f"assert_no_sorry {declaration}" in validation
        assert f"#print sorries {declaration}" in validation
        assert f"#print axioms {declaration}" in validation

    manifest = load(LEAN_ROOT / "lake-manifest.json")
    mathlib_entry = next(row for row in manifest["packages"] if row["name"] == "mathlib")
    assert mathlib_entry["rev"] == mathlib_entry["inputRev"] == MATHLIB_REVISION
    assert mathlib_entry["url"] == MATHLIB_REMOTE
    assert MATHLIB.resolve().is_dir(), "pinned mathlib artifact is unavailable"
    initial_mathlib = selected_mathlib_snapshot()
    assert initial_mathlib["revision"] == MATHLIB_REVISION
    assert initial_mathlib["tree"] == MATHLIB_TREE
    assert initial_mathlib["remote"] == MATHLIB_REMOTE
    assert initial_mathlib["status"] == ""
    assert initial_mathlib["license_sha256"] == MATHLIB_LICENSE_SHA256
    for relative, (blob, source_hash, olean_hash, ilean_hash) in MATHLIB_BOUNDARIES.items():
        source = MATHLIB / relative
        compiled = MATHLIB / ".lake/build/lib/lean" / Path(relative).with_suffix("")
        assert initial_mathlib["selected_boundaries"][relative] == [
            blob, source_hash, olean_hash, ilean_hash
        ]

    lean = elan_binary("lean")
    lake = elan_binary("lake")
    assert "4.29.0" in run([str(lean), "--version"], cwd=LEAN_ROOT)
    assert LEAN_COMMIT in run([str(lean), "--version"], cwd=LEAN_ROOT)
    assert "5.0.0-src+98dc76e" in run([str(lake), "--version"], cwd=LEAN_ROOT)
    tools = {
        "elan": Path("/home/sansha-2/.elan/bin/elan"),
        "lean": lean,
        "lake": lake,
        "python": Path(os.path.realpath(sys.executable)),
        "git": Path("/usr/bin/git"),
        "bash": Path("/usr/bin/bash"),
        "bubblewrap": Path("/usr/bin/bwrap"),
    }
    expected_tools = {
        "elan": "840179e70803ef373c2ec53342d6a45ea7d022533e4145489fc1278b4f716385",
        "lean": "3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf",
        "lake": "a608ff084d7e2af228b92a29d7c2fd083ba0580e46889175ec74a81678c98359",
        "python": "b8d8288faefdd300201f43fcf00f6f539a27218eeed3a3dff5ab10b9c4c99700",
        "git": "5516c9f362c29376ab9a499a33082f9f611941d8c75930c880e30ad109e39c9a",
        "bash": "3efccc187bafa75ff1e37d246270ab3e7aa559f242c7a52bf3ec2a1b5450bdbd",
        "bubblewrap": "0abea81db798ebf6b4742ac0664802d97521547a353c2a0dbdc21d76cbbfd2c0",
    }
    initial_tool_hashes = {name: sha256(path) for name, path in tools.items()}
    assert initial_tool_hashes == expected_tools

    fixed_tool_env = {
        "HOME": "/home/sansha-2",
        "PATH": f"{lean.parent}:/usr/bin:/bin",
        "ELAN_TOOLCHAIN": LEAN_TOOLCHAIN,
        "LANG": "C.UTF-8",
        "LC_ALL": "C.UTF-8",
        "TZ": "UTC",
        "LEAN_NUM_THREADS": "1",
    }
    lean_path = run(
        [str(lake), "env", "printenv", "LEAN_PATH"],
        cwd=LEAN_ROOT,
        env=fixed_tool_env,
    ).strip()
    assert fresh_expression_sha256(lean, lean_path) == EXPRESSION_SHA256

    kernel_output = run(["/usr/bin/bash", str(HERE / "check_validation.sh")])
    final_mathlib = selected_mathlib_snapshot()
    final_root_identity = {
        "revision": git("rev-parse", "HEAD"),
        "tree": git("rev-parse", "HEAD^{tree}"),
    }
    final_root_status = exact_git_status()
    final_manifest = validation_input_manifest()
    final_bound_hashes = {
        **{f"target:{name}": sha256(HERE / name) for name in EXPECTED_INPUTS},
        **{f"policy:{name}": sha256(ROOT / name) for name in POLICY_INPUTS},
        "target:check_validation.py": sha256(Path(__file__).resolve()),
        "target:validation-phase.md": sha256(HERE / "validation-phase.md"),
    }
    assert final_mathlib == initial_mathlib, "mathlib changed during replay"
    assert final_root_identity == initial_root_identity, "repository identity changed during replay"
    assert final_root_status == initial_root_status, "repository status changed during replay"
    assert final_manifest == initial_manifest, "validation inputs changed during replay"
    assert final_bound_hashes == initial_bound_hashes, "bound inputs changed during replay"
    assert {name: sha256(path) for name, path in tools.items()} == initial_tool_hashes
    assert kernel_output.count("Declarations are sorry-free!") == len(TRUST_DECLARATIONS)
    assert "declaration uses 'sorry'" not in kernel_output
    assert "sorryAx" not in kernel_output and "error:" not in kernel_output.lower()
    for declaration in TRUST_DECLARATIONS:
        assert observed_axioms(kernel_output, declaration) <= EXPECTED_AXIOMS
    assert observed_axioms(kernel_output, TRUST_DECLARATIONS[-1]) == EXPECTED_AXIOMS
    closure_match = re.search(
        r"VALIDATION_CLOSURE roots=4 declarations=(\d+) modules=(\d+)",
        kernel_output,
    )
    assert closure_match and closure_match.groups() == ("28337", "1086")
    assert "VALIDATION_CLOSURE bodyless_nonaxioms=[]" in kernel_output
    assert "VALIDATION_CLOSURE unsafe=[]" in kernel_output
    artifacts_match = re.search(r"^VALIDATION_ARTIFACTS=(\{.*\})$", kernel_output, re.MULTILINE)
    assert artifacts_match is not None
    replay_artifacts = json.loads(artifacts_match.group(1))
    assert set(replay_artifacts) == {
        "Statement", "ObligationTree", "Proof", "Validation"
    }
    for evidence in replay_artifacts.values():
        assert set(evidence) == {
            "stdout_bytes", "stdout_sha256", "olean_bytes", "olean_sha256"
        }
        assert evidence["olean_bytes"] > 0

    assert spec["schema_version"] == "stage1-validation-recipe/1.0"
    assert spec["item_id"] == ITEM and spec["theorem_id"] == THEOREM
    assert spec["cwd"] == "."
    assert spec["argv"] == [
        "python3", "-I", "-B", f"Stage1_Instances/{THEOREM}/check_validation.py"
    ]
    assert set(spec["env_allowlist"]) == {
        "PATH", "HOME", "PYTHONPATH", "LANG", "LC_ALL", "TZ", "LEAN_NUM_THREADS"
    }
    assert spec["timeout_seconds"] == 900
    assert spec["network_policy"] == "denied"
    assert spec["expected_exit"] == 0
    assert "--unshare-net" in spec["network_enforcement_boundary"]
    assert spec["covered_obligation_ids"] == MACHINE_IDS
    assert spec["covered_declarations"] == [
        "Stage1Instances.THM_M_0957.BehrendConstructionTarget", *TRUST_DECLARATIONS
    ]

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["normative_profile"] == "machine-theorem-assurance/1.0"
    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["phase"] == "validation" and receipt["intent"] == "validate"
    assert receipt["depends_on"] == ["S56-M-0957-PROOF"]
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["release_grade"] is receipt["content_addressed_release_evidence"] is False
    assert receipt["verdict"] == "blocked"
    assert receipt["canonical_target_expression_sha256"] == EXPRESSION_SHA256
    assert receipt["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert receipt["covered_obligation_ids"] == MACHINE_IDS
    assert receipt["replayed_route_subject_obligation_ids"] == MACHINE_IDS
    assert receipt["provisionally_validated_obligation_ids"] == []
    assert receipt["accepted_closed_obligation_ids"] == receipt["accepted_receipt_ids"] == []
    assert receipt["validated_declarations"] == spec["covered_declarations"]
    assert receipt["proof_content_added"] is False and receipt["exact_statements_changed"] == []
    for name, expected in EXPECTED_INPUTS.items():
        assert receipt["inputs"][name] == expected, name
    for name, expected in POLICY_INPUTS.items():
        assert receipt["inputs"][name] == expected, name
    assert receipt["inputs"]["check_validation.py"] == sha256(HERE / "check_validation.py")
    assert receipt["inputs"]["validation-phase.md"] == sha256(HERE / "validation-phase.md")
    assert receipt["recipe"] == spec
    environment = receipt["environment"]
    assert environment["platform"] == f"{platform.system()} {platform.release()} {platform.machine()}"
    assert environment["elan_executable_sha256"] == sha256(tools["elan"])
    assert environment["lean_executable_sha256"] == sha256(lean)
    assert environment["lake_executable_sha256"] == sha256(lake)
    assert environment["python_executable_sha256"] == sha256(tools["python"])
    assert environment["git_executable_sha256"] == sha256(tools["git"])
    assert environment["bash_executable_sha256"] == sha256(tools["bash"])
    assert environment["bubblewrap_executable_sha256"] == sha256(tools["bubblewrap"])
    assert environment["mathlib_revision"] == MATHLIB_REVISION
    assert environment["mathlib_tree"] == MATHLIB_TREE
    assert environment["mathlib_worktree_clean"] is True
    assert environment["lake_mutated_by_this_run"] is False
    repository_state = receipt["repository_state"]
    assert repository_state["initial_git_status_porcelain"] == initial_root_status
    assert repository_state["final_git_status_porcelain"] == final_root_status
    assert repository_state["initial_git_status_sha256"] == hashlib.sha256(
        initial_root_status.encode()
    ).hexdigest()
    assert repository_state["final_git_status_sha256"] == hashlib.sha256(
        final_root_status.encode()
    ).hexdigest()
    assert repository_state["tracked_patch_sha256"] == hashlib.sha256(
        run([
            "/usr/bin/git", "diff", "--binary", "--",
            str(HERE), str(ROOT / ".stage1-worker-selftest.json"),
        ]).encode()
    ).hexdigest()
    assert repository_state["untracked_validation_input_manifest"] == initial_manifest
    assert repository_state["untracked_validation_input_manifest_sha256"] == (
        initial_manifest_sha256
    )
    assert repository_state["untracked_outputs"] == [
        ".stage1-worker-selftest.json",
        f"Stage1_Instances/{THEOREM}/validation-receipt.json",
    ]
    assert repository_state["snapshot_equality_across_replay"] is True
    selected_boundaries = receipt["selected_provenance"][
        "selected_source_blob_olean_ilean_boundaries"
    ]
    assert set(selected_boundaries) == set(MATHLIB_BOUNDARIES)
    for relative, expected in MATHLIB_BOUNDARIES.items():
        assert selected_boundaries[relative] == list(expected), (
            relative, selected_boundaries[relative], expected
        )
    assert receipt["selected_provenance"]["complete_transitive_provenance_gate"] == "fail_closed"
    provenance = receipt["selected_provenance"]
    assert provenance["local_role"] == "alias"
    assert provenance["direct_dependencies"] == [
        "Stage1Instances.THM_M_0957_ObligationTree.exactRoot_proof"
    ]
    assert provenance["terminal_proof_body_id"].startswith(
        f"awesome_theorems@{BASE_REVISION}:sha256:{EXPECTED_INPUTS['Proof.lean']}:"
    )
    assert receipt["trust"]["machine_reported_root_axioms"] == [
        "propext", "Classical.choice", "Quot.sound"
    ]
    assert receipt["trust"]["accepted_foundation_policy"] is False
    assert receipt["trust"]["complete_tcb_gate"] == "fail_closed"
    assert receipt["independent_validation"]["same_worker_trust_probe"] == "pass_nonrelease"
    assert receipt["independent_validation"]["distinct_runner"] is False
    assert receipt["independent_validation"]["release_gate"] == "fail_closed"
    expected_kernel_hash = hashlib.sha256(kernel_output.encode()).hexdigest()
    artifact_line = artifacts_match.group(0) + "\n"
    assert kernel_output.count(artifact_line) == 1
    semantic_kernel_output = kernel_output.replace(artifact_line, "", 1)
    assert receipt["execution"]["kernel_output_sha256"] == hashlib.sha256(
        semantic_kernel_output.encode()
    ).hexdigest()
    assert receipt["execution"]["kernel_output_bytes"] == len(
        semantic_kernel_output.encode()
    )
    assert receipt["execution"]["combined_replay_output_bytes"] == len(kernel_output.encode())
    recorded_artifacts = receipt["execution"]["fresh_replay_artifacts"]
    for module, evidence in replay_artifacts.items():
        assert evidence["stdout_bytes"] == recorded_artifacts[module]["stdout_bytes"]
        assert evidence["olean_bytes"] == recorded_artifacts[module]["olean_bytes"]
        assert len(evidence["stdout_sha256"]) == 64
        assert len(evidence["olean_sha256"]) == 64
    assert receipt["execution"]["fresh_expression_sha256"] == EXPRESSION_SHA256
    assert receipt["execution"]["mathlib_snapshot_before"] == initial_mathlib
    assert receipt["execution"]["mathlib_snapshot_after"] == final_mathlib
    assert receipt["execution"]["validation_transitive_closure"] == {
        "roots": 4,
        "declarations": 28337,
        "modules": 1086,
        "unexpected_bodyless": [],
        "unsafe": [],
    }
    result = receipt["result"]
    assert result["exact_root_kernel_replay"] == "provisional_pass"
    assert result["proof_master_acceptance"] == "fail_closed"
    assert result["validation_phase_complete"] is False
    assert result["accepted_root_machine_debt"] == "M3"
    assert result["accepted_root_closed"] is False
    assert result["audit_complete"] is result["theorem_complete"] is False
    assert receipt["root_vector_before"] == receipt["root_vector_after"] == {
        "H": "H1", "M": "M3", "R": "R3"
    }
    assert receipt["first_failed_gate"] == "dependency.S56-M-0957-PROOF.master_acceptance"
    assert receipt["first_failed_release_gate"] == "S56-7.3-TRANSITIVE-PROVENANCE-CLOSURE"
    assert receipt["output_summary"] == list(SUMMARY_LINES)

    assert set(packet) == {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert packet["item_id"] == ITEM and packet["state"] == "[_]"
    assert packet["base_revision"] == BASE_REVISION
    assert set(receipt["changed_paths"]) == set(packet["changed_paths"]) == CHANGED_PATHS
    assert receipt["commands"] == packet["commands"]
    assert receipt["output_summary"] == packet["output_summary"]
    assert receipt["known_failures"] == packet["known_failures"]
    owned_inputs = receipt["nonrelease_input_set"]["owned_untracked_inputs"]
    assert set(owned_inputs) == CHANGED_PATHS - {".stage1-worker-selftest.json"}
    status = final_root_status.splitlines()
    actual = {line[3:] for line in status if line[3:] != "Formalizations/Lean/.lake"}
    assert actual == CHANGED_PATHS, (actual, CHANGED_PATHS)
    for relative in CHANGED_PATHS:
        assert_text_hygiene(ROOT / relative)
    for path in (HERE / "validation-receipt.json", HERE / "validation-phase.md"):
        text = path.read_text(encoding="utf-8")
        assert "/home/" not in text and ".cron/" not in text
        assert "theorem_complete=true" not in text

    print("\n".join(SUMMARY_LINES))


if __name__ == "__main__":
    main()
