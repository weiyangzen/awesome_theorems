#!/usr/bin/env python3
"""Fail-closed narrow validator for S56-M-0657-VALIDATION."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import re
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0657"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
ITEM = "S56-M-0657-VALIDATION"
THEOREM = "THM-M-0657"
BASE_REVISION = "8b9311952b6b4186c774d25758d16597a7c10a8b"
BASE_TREE = "69a7cea0132f4b76e7324c2d5cc320dec94d2f10"
TOOLCHAIN = "leanprover/lean4:v4.29.0"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
LEAN_SHA256 = "3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf"
LAKE_SHA256 = "a608ff084d7e2af228b92a29d7c2fd083ba0580e46889175ec74a81678c98359"
BWRAP_SHA256 = "0abea81db798ebf6b4742ac0664802d97521547a353c2a0dbdc21d76cbbfd2c0"
PYTHON_SHA256 = "b8d8288faefdd300201f43fcf00f6f539a27218eeed3a3dff5ab10b9c4c99700"
GIT_SHA256 = "5516c9f362c29376ab9a499a33082f9f611941d8c75930c880e30ad109e39c9a"
ELAN_LAUNCHER_SHA256 = "840179e70803ef373c2ec53342d6a45ea7d022533e4145489fc1278b4f716385"
TOOLCHAIN_SHA256 = "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2"
MANIFEST_SHA256 = "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MATHLIB_REMOTE = "https://github.com/leanprover-community/mathlib4.git"
MATHLIB_LICENSE_SHA256 = "b40930bbcf80744c86c46a12bc9da056641d722716c378f5659b9e555ef833e1"
STATEMENT_EXPRESSION_SHA256 = (
    "95c7d92148fe7e9375ef83729de47149f0cdecec4ce440308515ddae33442fc2"
)
DENOMINATOR_SHA256 = "22647d29b16c9d77f04719fe51238e427dab88b5fd6c57dfab8ac599c627ce44"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
ROOT_VECTOR = {"H": "H1", "M": "M3", "R": "R3"}
PROVISIONAL_IDS = ["M0657-L-COMPLETENESS", "M0657-C-EXISTENCE"]
OPEN_ROOT_CUT = [
    "M0657-C-MORLEY-RANK",
    "M0657-L-STABILITY",
    "M0657-L-SATURATION",
    "M0657-L-SATURATED-ISO",
    "M0657-T-TARGET-CAT",
    "M0657-ROOT",
]
EXPECTED_INPUTS = {
    "Statement.lean": "e70540498a70b7836ef9d70446a69753d3610088ab93669281f05a3ea1286131",
    "AnchorAudit.lean": "465a3d008c98d98934172a4df533d275487b36671fa16c98ae33d52d7a53b856",
    "ObligationTree.lean": "82128d51e2340be71d7838e7b4ffb82a40cfd1b16114f85390a9af98b0d6a911",
    "Proof.lean": "ea6b3cd2b96f0ae1b4901f69fcb22d091da92dcb0777ea86793ba871b21cfaf7",
    "Validation.lean": "ac683858be3f18b8b8beaa632d70351108797c57dfbf1c8c6ade421958ad53ba",
    "statement.json": "830a54a7ebe87d5c97d836afebd4150a3b34d1f4a5946629f62a29cf4a17c00e",
    "anchor-audit.json": "77632635737306a02f378d8350ff956fbcfd1cdb5b0c6865fccefa64d17c0fe0",
    "obligation-registry.json": "cb15499b200bf207bf71ce172a8e227e44bff5dddec58d24fb37a35d60b5babb",
    "typed-graphs.json": "0eeb5ba818108ff6f25271c17472a512d269492175b9895e7d8594a56c47695c",
    "validation-specs.json": "317e0959e7fdd4b1c431b4b8c0b997ee0a0617edc1312ee24a482e6e78e5abc1",
    "proof-receipt.json": "1625fd89c397b4445e8cc01b7c23cdf1bf687c139fe821c90b0d94bf3aad8fbc",
    "proof-blocker.json": "65e0f2092ad9380525d6dfcc25d7f0eff7fa91fd0718c33511fc8e13077a87a6",
    "proof-validation.md": "3049e73b9149adc10b716870a4658113ac14fe323147cf5b7d2c5ae6f7f82020",
    "source-statement-crosswalk.md": "f81e3aa169b740dd620b994200ab56e99b519a33fea27871a50f476648bc899f",
    "check_obligation_tree.py": "1d30f9c7db6dd9b885855f23623ccaabf48ff12898f9cbd58d63c298ff89eed2",
    "check_proof.sh": "49f940f19f29c5805318a16ad8bef85980d4f72ac0669c74d884630be0f67646",
}
SOURCE_BOUNDARIES = {
    "Mathlib/ModelTheory/Satisfiability.lean": {
        "blob": "b0688b14fc0cec8283a3666c886faf010858f401",
        "source_sha256": "0abb92d531851a57909945b740981d79a4cbb29238f2a3d21cb5fa57aa143edb",
        "olean_sha256": "56f4ca802c48e3f8c97fb8bb939f027d2ee2712cacf1de1495bae29796ae9a9b",
        "olean_bytes": 108872,
    },
    "Mathlib/ModelTheory/Semantics.lean": {
        "blob": "1fce49621b43bbf524bc0a816d26fcefa55a2d35",
        "source_sha256": "3baef41c7aba65bbf86e842a307c464fa9041f329308a762783d92fdf48d4fd3",
        "olean_sha256": "161d5af85b8e3c594d414c1cc5625ec22e671f11cb711dc34e6aa972f2816b04",
        "olean_bytes": 1524440,
    },
}
PROOF_DECLARATIONS = (
    "Stage1Instances.THM_M_0657.hasModelCardinality_of_uncountably_categorical",
    "Stage1Instances.THM_M_0657.infinitePart_categorical",
    "Stage1Instances.THM_M_0657.infinitePart_isComplete",
    "Stage1Instances.THM_M_0657.categoricalWithExistence_of_categorical",
    "Stage1Instances.THM_M_0657.morleyCategoricityTarget_of_categoricalTransfer",
)
VALIDATION_DECLARATIONS = (
    "Stage1Instances.THM_M_0657.Validation.differentialHasModelCardinality",
    "Stage1Instances.THM_M_0657.Validation.differentialInfinitePartCategorical",
    "Stage1Instances.THM_M_0657.Validation.differentialInfinitePartIsComplete",
    "Stage1Instances.THM_M_0657.Validation.differentialConditionalRoot",
)
COVERED_IDS = [
    "M0657-S-ENCODING",
    "M0657-N-SOURCE-SHAPE",
    "M0657-L-COMPLETENESS",
    "M0657-C-EXISTENCE",
    "M0657-T-TARGET-CAT",
    "M0657-T-ASSEMBLE",
]
COVERED_DECLARATIONS = [
    "Stage1Instances.THM_M_0657.MorleyCategoricityTarget",
    "Stage1Instances.THM_M_0657.morleyCategoricityTarget_iff_existentialSourceShape",
    *PROOF_DECLARATIONS,
    *VALIDATION_DECLARATIONS,
]
SCOPE_BOUNDARY = (
    "Network-isolated trust-zero warm worker replay of the exact statement, two "
    "unconditional proof-phase bodies, conditional compositions, selected direct pinned "
    "provenance, and same-worker no-import differential reconstructions. The Morley "
    "rank/stability/saturation/uniqueness core, exact root, accepted foundation and complete "
    "trust/provenance closure, cold hermetic reproduction, and distinct-runner independent "
    "verification remain fail-closed."
)
CHANGED_PATHS = [
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/Validation.lean",
    f"Stage1_Instances/{THEOREM}/check_validation.py",
    f"Stage1_Instances/{THEOREM}/validation-phase.md",
    f"Stage1_Instances/{THEOREM}/validation-receipt.json",
    f"Stage1_Instances/{THEOREM}/validation-spec.json",
]
SUMMARY_LINES = [
    "PASS narrow kernel replay: exact statement, proof-phase partial bodies, conditional compositions, and four no-import differential declarations elaborated at trust zero",
    "PASS trust observation: all checked declarations use only propext, Classical.choice, and Quot.sound; differential closure has no bodyless nonaxiom or unsafe declaration",
    "PASS selected provenance: frozen local hashes, two mathlib source/olean boundaries, executable pins, license, and clean pinned revision agree",
    "OPEN exact root: Morley rank, stability, saturation, saturated uniqueness, target categoricity, and the unconditional root remain unproved at M3",
    "FAIL CLOSED complete trust/provenance: proof acceptance, accepted foundation policy, serialized transitive closure, and full TCB/SBOM inventory are absent",
    "FAIL CLOSED release gates: shared warm cache is not cold hermetic evidence and this worker is not a distinct independent verifier",
]

if not __debug__:
    raise RuntimeError("validation requires Python assertions; optimized mode is forbidden")


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
        argv,
        cwd=cwd,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=timeout,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(f"command failed ({result.returncode}): {argv!r}\n{result.stdout}")
    return result.stdout


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


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["/usr/bin/git", *args], cwd=cwd, env=BASE_ENV).strip()


def source_without_comments(source: str) -> str:
    """Remove nested Lean comments and line comments before supplemental scans."""
    output: list[str] = []
    index = 0
    depth = 0
    while index < len(source):
        if depth == 0 and source.startswith("--", index):
            newline = source.find("\n", index)
            if newline < 0:
                break
            output.append("\n")
            index = newline + 1
        elif source.startswith("/-", index):
            depth += 1
            index += 2
        elif depth and source.startswith("-/", index):
            depth -= 1
            index += 2
        elif depth:
            if source[index] == "\n":
                output.append("\n")
            index += 1
        else:
            output.append(source[index])
            index += 1
    assert depth == 0, "unterminated Lean block comment"
    return "".join(output)


def reported_axioms(output: str, declaration: str) -> set[str]:
    pattern = re.compile(
        re.escape(f"'{declaration}' depends on axioms: [") + r"(.*?)]",
        re.DOTALL,
    )
    matches = pattern.findall(output)
    assert len(matches) == 1, f"missing or duplicate axiom report for {declaration}"
    return {part.strip() for part in matches[0].split(",") if part.strip()}


def assert_text_hygiene(path: Path) -> None:
    data = path.read_bytes()
    assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())


def pinned_lean_path(lean: Path) -> str:
    package_names = (
        "batteries", "Qq", "aesop", "proofwidgets", "importGraph",
        "LeanSearchClient", "plausible", "mathlib",
    )
    roots = [
        (LEAN_ROOT / ".lake" / "packages" / name / ".lake/build/lib/lean").resolve()
        for name in package_names
    ]
    assert all(path.is_dir() for path in roots)
    local = (LEAN_ROOT / ".lake/build/lib/lean").resolve()
    assert local.is_dir()
    return ":".join([*(str(path) for path in roots), str(local), str(lean.parent.parent / "lib/lean")])


def isolated_replay(lean: Path, bwrap: Path, lean_path: str) -> dict[str, str]:
    with tempfile.TemporaryDirectory(prefix="stage1-m0657-validation-", dir="/tmp") as tmp_name:
        tmp = Path(tmp_name).resolve()
        for name in (
            "Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean",
        ):
            (tmp / name).write_bytes((HERE / name).read_bytes())
        (tmp / "home").mkdir()
        base = [
            str(bwrap), "--ro-bind", "/", "/", "--bind", str(tmp), str(tmp),
            "--dev", "/dev", "--proc", "/proc", "--unshare-net",
            "--die-with-parent", "--clearenv", "--setenv", "HOME", str(tmp / "home"),
            "--setenv", "TMPDIR", str(tmp), "--setenv", "LANG", "C.UTF-8",
            "--setenv", "LC_ALL", "C.UTF-8", "--setenv", "TZ", "UTC",
            "--setenv", "LEAN_NUM_THREADS", "1", "--chdir", str(tmp),
        ]

        def lean_run(name: str, module_path: str, emit_olean: bool) -> str:
            argv = base + [
                "--setenv", "LEAN_PATH", module_path, str(lean), "--trust=0", "-t0",
            ]
            if emit_olean:
                argv += ["-o", name.replace(".lean", ".olean")]
            argv.append(name)
            return run(argv)

        module_path = f"{tmp}:{lean_path}"
        return {
            "statement": lean_run("Statement.lean", lean_path, True),
            "obligation_tree": lean_run("ObligationTree.lean", module_path, True),
            "proof": lean_run("Proof.lean", module_path, False),
            "validation": lean_run("Validation.lean", module_path, False),
        }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--probe", action="store_true")
    parser.add_argument("--worker-packet", type=Path)
    args = parser.parse_args()

    execution = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")
    targets = load(ROOT / "Docs" / "Stage1_Targets_rev-5.6.json")
    statement = load(HERE / "statement.json")
    anchor = load(HERE / "anchor-audit.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    frozen_specs = load(HERE / "validation-specs.json")
    proof_receipt = load(HERE / "proof-receipt.json")
    proof_blocker = load(HERE / "proof-blocker.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 702 and target["baseline"] == "L0"
    assert target["lifecycle_mode"] == "planned"
    assert target["rework_required"] is True and target["theorem_complete"] is False
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item == {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 702,
        "phase": "validation",
        "layer": 5,
        "state": "[ ]",
        "depends_on": ["S56-M-0657-PROOF"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Run hermetic kernel, trust, provenance, and independent validation gates.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }
    predecessor = next(row for row in execution["items"] if row["id"] == "S56-M-0657-PROOF")
    assert predecessor["state"] == "[_]" and predecessor["attempts"] == 1

    for name, expected in EXPECTED_INPUTS.items():
        assert sha256(HERE / name) == expected, f"stale validation input: {name}"
    assert sha256(LEAN_ROOT / "lean-toolchain") == TOOLCHAIN_SHA256
    assert sha256(LEAN_ROOT / "lake-manifest.json") == MANIFEST_SHA256
    formal = statement["canonical_formal_target"]
    assert formal["declaration_or_expression"] == (
        "Stage1Instances.THM_M_0657.MorleyCategoricityTarget"
    )
    assert formal["elaborated_expression_sha256"] == STATEMENT_EXPRESSION_SHA256
    assert formal["statement_file_sha256"] == EXPECTED_INPUTS["Statement.lean"]
    assert registry["root_obligation_id"] == graphs["root_node_id"] == "M0657-ROOT"
    assert registry["denominator_sha256"] == graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    ids = [row["obligation_id"] for row in registry["obligations"]]
    assert len(ids) == len(set(ids)) == 14
    assert registry["frozen_denominators"]["inventory"] == ids
    assert {row["obligation_id"] for row in frozen_specs["recipes"]} == set(ids)
    root = next(node for node in graphs["nodes"] if node["obligation_id"] == "M0657-ROOT")
    assert {"H": root["human_debt"], "M": root["machine_debt"], "R": root["readability_debt"]} == ROOT_VECTOR
    closure = graphs["closure_boundary"]
    assert closure["root_closed"] is closure["theorem_complete"] is False
    assert closure["root_machine_classification"] == "M3"

    assert anchor["canonical_target"] == formal["declaration_or_expression"]
    assert anchor["classification"]["machine"] == "M3"
    assert anchor["theorem_proved"] is anchor["theorem_complete"] is False
    assert all(
        candidate["exact_root_closure"] is False
        for candidate in anchor["mathlib_candidates"] + anchor["external_candidates"]
    )
    assert proof_receipt["item_id"] == "S56-M-0657-PROOF"
    assert proof_receipt["support_state"] == "provisional_worker_selftest"
    assert proof_receipt["accepted"] is False
    assert proof_receipt["proof_body"]["source_sha256"] == EXPECTED_INPUTS["Proof.lean"]
    assert proof_receipt["provisionally_closed_obligation_ids"] == PROVISIONAL_IDS
    assert proof_receipt["accepted_closed_obligation_ids"] == []
    assert proof_receipt["result"]["root_closed"] is False
    assert proof_receipt["result"]["theorem_complete"] is False
    assert proof_blocker["provisional_remaining_machine_cut"] == OPEN_ROOT_CUT
    assert proof_blocker["root_closed"] is proof_blocker["theorem_complete"] is False

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by|run_tac)\b|"
        r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
        r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
        r"(?:axiom|constant|opaque|unsafe|extern)\b",
        flags=re.MULTILINE,
    )
    all_source = "\n".join(
        source_without_comments((HERE / name).read_text(encoding="utf-8"))
        for name in (
            "Statement.lean", "AnchorAudit.lean", "ObligationTree.lean", "Proof.lean",
            "Validation.lean",
        )
    )
    assert prohibited.search(all_source) is None
    validation = (HERE / "Validation.lean").read_text(encoding="utf-8")
    imports = validation.split("/-!", 1)[0]
    assert "import Proof" not in imports and "import ObligationTree" not in imports
    for fragment in (
        "theorem differentialHasModelCardinality",
        "exists_elementarilyEquivalent_card_eq L M lambda",
        "theorem differentialInfinitePartIsComplete",
        "def DifferentialUniquenessTransfer : Prop",
        "theorem differentialConditionalRoot",
        "(huniq : DifferentialUniquenessTransfer.{u, v, w})",
        "assert_no_sorry differentialConditionalRoot",
        "#print_validation_closure",
    ):
        assert fragment in validation, fragment
    assert re.search(r"theorem\s+differentialConditionalRoot\s*:", validation) is None

    manifest = load(LEAN_ROOT / "lake-manifest.json")
    mathlib_entry = next(row for row in manifest["packages"] if row["name"] == "mathlib")
    assert mathlib_entry["rev"] == mathlib_entry["inputRev"] == MATHLIB_REVISION
    assert mathlib_entry["url"] == MATHLIB_REMOTE
    assert (LEAN_ROOT / ".lake").is_symlink()
    mathlib = (LEAN_ROOT / ".lake/packages/mathlib").resolve()
    assert mathlib.is_dir()
    assert git("rev-parse", "HEAD", cwd=mathlib) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == MATHLIB_TREE
    assert git("status", "--porcelain=v1", "--untracked-files=all", cwd=mathlib) == ""
    assert git("remote", "get-url", "origin", cwd=mathlib) == MATHLIB_REMOTE
    assert sha256(mathlib / "LICENSE") == MATHLIB_LICENSE_SHA256
    for relative, expected in SOURCE_BOUNDARIES.items():
        source = mathlib / relative
        olean = mathlib / ".lake/build/lib/lean" / Path(relative).with_suffix(".olean")
        assert git("rev-parse", f"HEAD:{relative}", cwd=mathlib) == expected["blob"]
        assert sha256(source) == expected["source_sha256"]
        assert sha256(olean) == expected["olean_sha256"]
        assert olean.stat().st_size == expected["olean_bytes"]
        assert prohibited.search(source_without_comments(source.read_text(encoding="utf-8"))) is None

    lake_launcher = Path(HOME) / ".elan/bin/lake"
    assert sha256(lake_launcher) == ELAN_LAUNCHER_SHA256
    lean = Path(run(
        [str(lake_launcher), "env", "which", "lean"], cwd=LEAN_ROOT, env=BASE_ENV
    ).strip())
    lake = Path(run(
        [str(lake_launcher), "env", "which", "lake"], cwd=LEAN_ROOT, env=BASE_ENV
    ).strip())
    bwrap = Path("/usr/bin/bwrap")
    python = Path("/usr/bin/python3").resolve()
    git_executable = Path("/usr/bin/git")
    assert sha256(lean) == LEAN_SHA256 and sha256(lake) == LAKE_SHA256
    assert sha256(bwrap) == BWRAP_SHA256 and sha256(python) == PYTHON_SHA256
    assert sha256(git_executable) == GIT_SHA256
    assert LEAN_COMMIT in run([str(lean), "--version"], env=BASE_ENV)
    assert "5.0.0-src+98dc76e" in run([str(lake), "--version"], env=BASE_ENV)

    outputs = isolated_replay(lean, bwrap, pinned_lean_path(lean))
    combined = "\n".join(outputs.values())
    assert "sorryAx" not in combined and all("error:" not in output for output in outputs.values())
    for declaration in PROOF_DECLARATIONS:
        assert reported_axioms(outputs["proof"], declaration) <= EXPECTED_AXIOMS
    for declaration in VALIDATION_DECLARATIONS:
        assert reported_axioms(outputs["validation"], declaration) <= EXPECTED_AXIOMS
    # `assert_no_sorry` is silent for this proof module on success; the
    # declaration-specific axiom reports and absence of `sorryAx` are the
    # machine-observed checks retained here.
    assert outputs["validation"].count("Declarations are sorry-free!") == 4
    closure_match = re.search(
        r"VALIDATION_CLOSURE declarations=(\d+) modules=(\d+)", outputs["validation"]
    )
    assert closure_match is not None
    assert "VALIDATION_CLOSURE axioms=[propext, Classical.choice, Quot.sound]" in outputs["validation"]
    assert "VALIDATION_CLOSURE bodyless_nonaxioms=[]" in outputs["validation"]
    assert "VALIDATION_CLOSURE unsafe=[]" in outputs["validation"]
    observation = {
        "lean_output_sha256": {
            name: hashlib.sha256(output.encode()).hexdigest()
            for name, output in outputs.items()
        },
        "observed_axioms": sorted(EXPECTED_AXIOMS),
        "validation_closure": {
            "declarations": int(closure_match.group(1)),
            "modules": int(closure_match.group(2)),
            "bodyless_nonaxioms": [],
            "unsafe_declarations": [],
        },
    }
    if args.probe:
        print(json.dumps(observation, sort_keys=True))
        return

    spec = load(HERE / "validation-spec.json")
    receipt = load(HERE / "validation-receipt.json")
    assert spec["schema_version"] == "stage1-validation-spec/1.0"
    assert spec["item_id"] == receipt["item_id"] == ITEM
    assert spec["theorem_id"] == receipt["theorem_id"] == THEOREM
    assert receipt["depends_on"] == ["S56-M-0657-PROOF"]
    assert spec["recipe_id"] == "S56-M-0657-VALIDATION-narrow-v1"
    assert spec["argv"] == [
        "python3", "-I", "-B", f"Stage1_Instances/{THEOREM}/check_validation.py",
        "--worker-packet", ".stage1-worker-selftest.json",
    ]
    assert receipt["recipe"]["argv"] == spec["argv"]
    assert receipt["recipe"]["cwd"] == spec["cwd"] == "."
    assert receipt["recipe"]["timeout_seconds"] == spec["timeout_seconds"] == 600
    assert receipt["recipe"]["network_policy"] == spec["network_policy"] == "denied"
    assert receipt["recipe"]["network_policy_scope"] == spec["network_policy_scope"] == (
        "enforced for every Lean subprocess; the outer validator invokes no network command "
        "but is not itself network-sandboxed"
    )
    assert receipt["recipe"]["env_allowlist"] == spec["env_allowlist"]
    assert spec["env_allowlist"] == {
        "ELAN_TOOLCHAIN": TOOLCHAIN,
        "LANG": "C.UTF-8",
        "LC_ALL": "C.UTF-8",
        "TZ": "UTC",
        "LEAN_NUM_THREADS": "1",
        "HOME": "runner home used only to address the hash-verified .elan/bin/lake launcher",
        "PATH": "<HOME>/.elan/bin:/usr/bin:/bin",
    }
    assert "Bubblewrap" in spec["network_enforcement"]
    assert spec["expected_exit"] == receipt["recipe"]["expected_exit"] == 0
    assert spec["expected_outputs"] == receipt["recipe"]["expected_outputs"] == [{
        "path_or_stream": "stdout",
        "semantic_hash_policy": "exact six-line gate summary bound in validation-receipt.json",
    }]
    assert spec["covered_obligation_ids"] == receipt["recipe"]["covered_obligation_ids"] == COVERED_IDS
    assert spec["covered_declarations"] == receipt["recipe"]["covered_declarations"] == COVERED_DECLARATIONS
    assert spec["scope_boundary"] == receipt["recipe"]["scope_boundary"] == SCOPE_BOUNDARY
    assert Path(BASE_ENV["PATH"].split(":", 1)[1].split(":", 1)[0]) / "python3" == Path(
        "/usr/bin/python3"
    )
    assert Path("/usr/bin/python3").resolve() == python

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["phase"] == "validation" and receipt["intent"] == "validate"
    assert receipt["verdict"] == "blocked"
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["release_grade"] is False
    assert receipt["lifecycle_before"] == receipt["lifecycle_after"] == "planned"
    assert receipt["root_vector_before"] == receipt["root_vector_after"] == ROOT_VECTOR
    assert receipt["accepted_receipt_ids"] == []
    assert receipt["validation_started_at"] < receipt["validation_ended_at"]
    assert receipt["validation_ended_at"] == receipt["validated_at"]
    for key in (
        "repository_state", "environment", "direct_provenance", "trust",
        "hermeticity", "independent_validation", "result", "commands",
        "output_evidence", "known_failures", "freshness", "invalidation_inputs",
    ):
        assert key in receipt
    repository_state = receipt["repository_state"]
    assert repository_state["release_clean"] is False
    assert repository_state["tracked_patch_sha256"] == hashlib.sha256(b"").hexdigest()
    assert repository_state["tracked_patch_bytes"] == 0
    input_payload = [
        {"path": relative, "sha256": sha256(ROOT / relative)}
        for relative in (
            f"Stage1_Instances/{THEOREM}/Validation.lean",
            f"Stage1_Instances/{THEOREM}/check_validation.py",
            f"Stage1_Instances/{THEOREM}/validation-phase.md",
            f"Stage1_Instances/{THEOREM}/validation-spec.json",
        )
    ]
    assert repository_state["untracked_input_sha256"] == hashlib.sha256(
        json.dumps(input_payload, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    assert repository_state["untracked_input_scope"] == [row["path"] for row in input_payload]
    assert repository_state["preexisting_untracked_lake_symlink_target_sha256"] == hashlib.sha256(
        os.readlink(LEAN_ROOT / ".lake").encode()
    ).hexdigest()
    for name, expected in EXPECTED_INPUTS.items():
        assert receipt["inputs"][name] == expected, name
    assert receipt["inputs"]["validation-spec.json"] == sha256(HERE / "validation-spec.json")
    assert receipt["inputs"]["check_validation.py"] == sha256(Path(__file__).resolve())
    assert receipt["target"]["elaborated_expression_sha256"] == STATEMENT_EXPRESSION_SHA256
    assert receipt["target"]["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert receipt["environment"]["platform"] == f"{platform.system()} {platform.release()} {platform.machine()}"
    assert receipt["environment"]["lean_executable_sha256"] == sha256(lean)
    assert receipt["environment"]["lake_executable_sha256"] == sha256(lake)
    assert receipt["environment"]["bubblewrap_executable_sha256"] == sha256(bwrap)
    assert receipt["environment"]["python_executable_sha256"] == sha256(python)
    assert receipt["environment"]["git_executable_sha256"] == sha256(git_executable)
    result = receipt["result"]
    assert result["lean_output_sha256"] == observation["lean_output_sha256"]
    assert result["observed_axioms"] == observation["observed_axioms"]
    assert result["validation_closure"] == observation["validation_closure"]
    assert result["validated_provisional_obligation_ids"] == PROVISIONAL_IDS
    assert result["accepted_closed_obligation_ids"] == []
    assert result["proof_dependency_master_acceptance"] == "fail_closed"
    assert result["root_closed"] is result["root_kernel_closed"] is False
    assert result["root_machine_debt"] == "M3"
    assert result["open_root_cut_set"] == OPEN_ROOT_CUT
    assert result["complete_trust_provenance_gate"] == "fail_closed"
    assert result["hermetic_release_gate"] == "fail_closed"
    assert result["independent_distinct_runner_gate"] == "fail_closed"
    assert result["audit_complete"] is result["theorem_complete"] is False
    direct = receipt["direct_provenance"]
    assert direct["proof_dependency_master_accepted"] is False
    assert direct["complete_terminal_body_import_artifact_source_boundary_and_tcb_closure"] is False
    trust = receipt["trust"]
    assert trust["accepted_foundation_profile"] is False
    assert trust["complete_transitive_trust_closure"] is False
    hermeticity = receipt["hermeticity"]
    assert hermeticity["fresh_clean_checkout"] is False
    assert hermeticity["empty_user_package_and_build_caches"] is False
    assert hermeticity["cold_dependency_rebuild"] is False
    assert hermeticity["decision"].startswith("fail_closed")
    independent = receipt["independent_validation"]
    assert independent["distinct_verifier_identity"] is False
    assert independent["independently_provisioned_clean_runner"] is False
    assert independent["second_signed_attestation"] is False
    assert independent["independently_implemented_minimal_release_verifier"] is False
    assert independent["decision"] == "fail_closed"
    freshness = receipt["freshness"]
    assert freshness["support_state"] == "provisional_nonrelease_worker_evidence"
    assert freshness["revocation_state"] == "unaccepted"
    assert receipt["known_failures"] and receipt["invalidation_inputs"]
    assert receipt["remaining_root_cut_set"] == OPEN_ROOT_CUT
    assert receipt["first_failed_gate"] == "dependency.S56-M-0657-PROOF.master_acceptance"
    assert receipt["first_failed_theorem_gate"] == "M0657-C-MORLEY-RANK.root_closure"
    expected_stdout = ("\n".join(SUMMARY_LINES) + "\n").encode()
    assert receipt["output_evidence"]["stdout_semantic_sha256"] == hashlib.sha256(
        expected_stdout
    ).hexdigest()
    assert receipt["output_evidence"]["expected_line_count"] == len(SUMMARY_LINES)
    assert receipt["output_evidence"]["exit_code"] == 0
    assert receipt["output_evidence"]["raw_logs_retained"] is False
    assert receipt["output_evidence"]["raw_log_sha256"] is None
    assert receipt["changed_paths"] == CHANGED_PATHS

    if args.worker_packet is not None:
        packet = load(args.worker_packet.resolve())
        assert set(packet) == {
            "item_id", "changed_paths", "commands", "output_summary",
            "base_revision", "known_failures", "state",
        }
        assert packet["item_id"] == ITEM and packet["state"] == "[_]"
        assert packet["base_revision"] == BASE_REVISION
        assert packet["changed_paths"] == receipt["changed_paths"] == CHANGED_PATHS
        assert packet["commands"] == receipt["commands"]
        assert packet["output_summary"] == receipt["output_summary"]
        assert packet["known_failures"] == receipt["known_failures"]
        status = git("status", "--short", "--untracked-files=all")
        actual = {
            line[3:] for line in status.splitlines()
            if line[3:] != "Formalizations/Lean/.lake"
        }
        assert actual == set(CHANGED_PATHS), (actual, set(CHANGED_PATHS))

    for relative in CHANGED_PATHS:
        assert_text_hygiene(ROOT / relative)
    for line in SUMMARY_LINES:
        print(line)


if __name__ == "__main__":
    main()
