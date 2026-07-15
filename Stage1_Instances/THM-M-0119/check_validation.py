#!/usr/bin/env python3
"""Fail-closed narrow validation for S56-M-0119-VALIDATION."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import platform
import re
import subprocess
import tempfile


if not __debug__:
    raise RuntimeError("validation requires Python assertions; optimized mode is forbidden")


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0119"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
ITEM = "S56-M-0119-VALIDATION"
THEOREM = "THM-M-0119"
BASE_REVISION = "80f0191c83a1bb4026c2d490be957cf109464de1"
BASE_TREE = "b89a01cfc623bf97d1896fb3534a1ac24381fa71"
TOOLCHAIN = "leanprover/lean4:v4.29.0"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
LEAN_SHA256 = "3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf"
LAKE_SHA256 = "a608ff084d7e2af228b92a29d7c2fd083ba0580e46889175ec74a81678c98359"
BWRAP_SHA256 = "0abea81db798ebf6b4742ac0664802d97521547a353c2a0dbdc21d76cbbfd2c0"
PYTHON_SHA256 = "b8d8288faefdd300201f43fcf00f6f539a27218eeed3a3dff5ab10b9c4c99700"
GIT_SHA256 = "5516c9f362c29376ab9a499a33082f9f611941d8c75930c880e30ad109e39c9a"
ELAN_SHA256 = "840179e70803ef373c2ec53342d6a45ea7d022533e4145489fc1278b4f716385"
TOOLCHAIN_SHA256 = "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2"
MANIFEST_SHA256 = "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MATHLIB_REMOTE = "https://github.com/leanprover-community/mathlib4.git"
MATHLIB_LICENSE_SHA256 = "b40930bbcf80744c86c46a12bc9da056641d722716c378f5659b9e555ef833e1"
EXPRESSION_SHA256 = "e7402bc1bb4f1bc6255436b7d7635869788000c47450782fa75cf8272dac644b"
DENOMINATOR_SHA256 = "d9c76b6bb201afa0b50c3e3a38e86e6db4faab64d250009313606b3ae79592db"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
ROOT_VECTOR = {"H": "H4", "M": "M3", "R": "R4"}
FROZEN_ROOT_CUT = [
    "M0119-X-APIS",
    "M0119-N-RESOLUTION",
    "M0119-L-SMOOTH",
    "M0119-C-PUSH",
]
INVALIDATION_BOUNDARY = [
    "S56-M-0119-STATEMENT",
    "M0119-S-DATA",
    "M0119-S-HYP",
    "M0119-ROOT",
]
EXPECTED_INPUTS = {
    "Statement.lean": "3fe71e3416e702f21689718833e7068685c5861394b556f5d584b01a963dd0a7",
    "ObligationTree.lean": "b59d088fa935449c4ccfddbbaa01370b7d47b23971cdf0cd6af259e8bd68c5f2",
    "Proof.lean": "e3436aa911ddf668b68cc036f0d35609565756075f29bd0e02c773408c33b49f",
    "Validation.lean": "363d5de1fadea621e5eee80700510e06c3f9bc59392f5a7d84bae67470eadcc9",
    "instance.json": "21b2837755eb4e84d229927c19b6c6c30fb904503139bfe328cfd5a129fb3682",
    "statement.json": "f7766c2e39478ec2b05edc69b42bb4cad60c2f1f0fe2ef2506c63182e189d8a4",
    "anchor-audit.json": "3bea41e96b4396198db0537049ad3a0769054619634f943f4dfefc80bf42292d",
    "obligation-registry.json": "51f8b730e77dd8382ffeb655c9446fa6a5dd706fc901c79e3927818cccf6b19a",
    "typed-graphs.json": "c16cf7168f31fd2d5972519e50eb7f361a6215cce0e670a6882e4313f8252c19",
    "task-dag.json": "e0ad9e47967b372cf815f3b83c3b683ddc51acfb167d8212d8609544f35aeb9e",
    "proof-blocker.json": "2242bee155181298fc98a411fce5c68583a2f2c96c960339bd54cf8b1ddd759d",
    "proof-recheck-2026-07-15-head-472dc79e-slot17.json": (
        "01c151c7ffded06be071a1b2cf2cff7fd616b925c3d4c5b575ba38a208f23ebe"
    ),
    "source-statement-crosswalk.md": (
        "e613664aaccefc669cd44ef4703b489e1c28bd833fff7fab74dc21dae77c9844"
    ),
}
SELECTED_MATHLIB_BOUNDARIES = {
    "Mathlib/AlgebraicGeometry/Properties.lean": {
        "blob": "35c57e8db9b0f7f2c147e4197354efbceca8e868",
        "source_sha256": "80f4414415dcbe45caf6cb15a3eef069372f688ca325400d5fee1752d0e7dd05",
        "olean_sha256": "a1e1c4ffb4c9d8a24f309173ca2fe76fe2eaf69d52bec8c5a3a6dacfb4d6cd19",
    },
    "Mathlib/Data/ZMod/Defs.lean": {
        "blob": "70625d7130ba48c4d889b99e2bb67fa57d4d1f42",
        "source_sha256": "d8817b7d6b21da3f09e2d97ac52a01dbd2adf0104c9376f8f7e3f1e1d02bd837",
        "olean_sha256": "a63628791fa0acc4fa196c7e900bc18748cc137b32c4fb76330838f78001e2a4",
    },
    "Mathlib/Util/AssertNoSorry.lean": {
        "blob": "060d8a764d2a6d1d2963d9c500b6084a05bed534",
        "source_sha256": "aa9f7bebacafc688c894ef2171930e51ed19e0dfe722581848a2414d28900d4d",
        "olean_sha256": "c8bf37753d9bad47b9fe67e32436da8b9af516a4abbbe14e74726f01ba2fb30b",
    },
    "Mathlib/Util/PrintSorries.lean": {
        "blob": "24d72cc680fa8b07f0d1062f670a5a824934a227",
        "source_sha256": "03670b0b0007740e5390dadd49c3d10a02b7d0919092d2b3214ef8a6a8cf798f",
        "olean_sha256": "9bcc4076e0aee5febb2eea5cf9dc959f38526e9f974afdfdd8658bfd318d5bb7",
    },
}
PROOF_DECLARATION = (
    "Stage1Instances.THMM0119.not_kawamataViehwegVanishingTarget"
)
COMPOSITION_DECLARATIONS = (
    "Stage1Instances.THMM0119.ObligationTree.positive_degrees_compose",
    "Stage1Instances.THMM0119.ObligationTree.implication_compose",
)
VALIDATION_DECLARATION = (
    "Stage1Instances.THMM0119.Validation.independent_root_countermodel"
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
    "PASS THM-M-0119 narrow validation",
    "PASS network-isolated trust-zero fresh-output replay: frozen statement, Int countermodel, conditional composition, and no-Proof-import ZMod 2 countermodel elaborated",
    "PASS hygiene and trust observation: both countermodels are sorry-free and use exactly propext, Classical.choice, and Quot.sound; validation closure reports no unexpected bodyless nonaxiom or unsafe declaration",
    "PASS selected provenance: frozen local hashes, clean mathlib pin/tree/origin, selected source and olean hashes, license, and executable identities agree",
    "FAIL CLOSED positive root: two different kernel-checked models refute the disconnected frozen backend target; zero frozen obligations are closed",
    "FAIL CLOSED complete trust/provenance and hermetic release: accepted profiles, full transitive TCB/SBOM, clean checkout, empty-cache cold build, and offline restoration are absent",
    "FAIL CLOSED authority and independence: the proof dependency is not master-accepted and same-worker differential replay is not a distinct signed verifier; audit_complete=false; theorem_complete=false",
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
    timeout: int = 900,
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
    if result.returncode:
        raise RuntimeError(
            f"command failed ({result.returncode}): {argv!r}\n{result.stdout}"
        )
    return result.stdout


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["/usr/bin/git", *args], cwd=cwd, env=BASE_ENV).strip()


def source_without_comments_or_strings(source: str) -> str:
    """Strip nested Lean comments and strings for a supplemental token scan."""
    output: list[str] = []
    index = 0
    depth = 0
    in_string = False
    while index < len(source):
        if depth == 0 and not in_string and source.startswith("--", index):
            newline = source.find("\n", index)
            if newline < 0:
                break
            output.append("\n")
            index = newline + 1
        elif not in_string and source.startswith("/-", index):
            depth += 1
            index += 2
        elif depth and source.startswith("-/", index):
            depth -= 1
            index += 2
        elif depth:
            if source[index] == "\n":
                output.append("\n")
            index += 1
        elif source[index] == '"':
            in_string = not in_string
            output.append(" ")
            index += 1
        elif in_string and source[index] == "\\" and index + 1 < len(source):
            output.extend("  ")
            index += 2
        elif in_string:
            output.append("\n" if source[index] == "\n" else " ")
            index += 1
        else:
            output.append(source[index])
            index += 1
    assert depth == 0 and not in_string, "unterminated comment or string"
    return "".join(output)


def reported_axioms(output: str, declaration: str) -> set[str]:
    pattern = re.compile(
        re.escape(f"'{declaration}' depends on axioms: [") + r"(.*?)]",
        re.DOTALL,
    )
    matches = pattern.findall(output)
    assert len(matches) == 1, f"missing or duplicate axiom report for {declaration}"
    return {part.strip() for part in matches[0].split(",") if part.strip()}


def assert_no_axioms(output: str, declaration: str) -> None:
    assert f"'{declaration}' does not depend on any axioms" in output, declaration


def assert_text_hygiene(path: Path) -> None:
    data = path.read_bytes()
    assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())


HOME = os.environ.get("HOME", str(Path.home()))
BASE_ENV = {
    "HOME": HOME,
    "PATH": f"{HOME}/.elan/bin:/usr/bin:/bin",
    "ELAN_TOOLCHAIN": TOOLCHAIN,
    "LANG": "C.UTF-8",
    "LC_ALL": "C.UTF-8",
    "TZ": "UTC",
    "LEAN_NUM_THREADS": "1",
}


def pinned_lean_path(lean: Path) -> str:
    package_root = (LEAN_ROOT / ".lake" / "packages").resolve()
    roots = sorted(
        path.resolve()
        for path in package_root.glob("*/.lake/build/lib/lean")
        if path.is_dir()
    )
    local = (LEAN_ROOT / ".lake/build/lib/lean").resolve()
    assert roots and local.is_dir()
    return ":".join(
        [*(str(path) for path in roots), str(local), str(lean.parent.parent / "lib/lean")]
    )


def isolated_replay(
    lean: Path, bwrap: Path, lean_path: str, outer_isolated: bool,
) -> tuple[dict[str, str], dict[str, str]]:
    with tempfile.TemporaryDirectory(
        prefix="stage1-m0119-validation-", dir="/tmp"
    ) as tmp_name:
        tmp = Path(tmp_name).resolve()
        for name in (
            "Statement.lean",
            "ObligationTree.lean",
            "Proof.lean",
            "Validation.lean",
        ):
            (tmp / name).write_bytes((HERE / name).read_bytes())
        (tmp / "home").mkdir()
        base = [] if outer_isolated else [
            str(bwrap),
            "--ro-bind",
            "/",
            "/",
            "--bind",
            str(tmp),
            str(tmp),
            "--dev",
            "/dev",
            "--proc",
            "/proc",
            "--unshare-net",
            "--die-with-parent",
            "--clearenv",
            "--setenv",
            "HOME",
            str(tmp / "home"),
            "--setenv",
            "TMPDIR",
            str(tmp),
            "--setenv",
            "LANG",
            "C.UTF-8",
            "--setenv",
            "LC_ALL",
            "C.UTF-8",
            "--setenv",
            "TZ",
            "UTC",
            "--setenv",
            "LEAN_NUM_THREADS",
            "1",
            "--chdir",
            str(tmp),
        ]

        def lean_run(name: str, module_path: str, emit_olean: bool) -> str:
            prefix = [] if outer_isolated else ["--setenv", "LEAN_PATH", module_path]
            argv = base + prefix + [str(lean), "--trust=0", "-t0"]
            if emit_olean:
                argv += ["-o", name.replace(".lean", ".olean")]
            argv.append(name)
            child_env = {
                **BASE_ENV,
                "HOME": str(tmp / "home"),
                "TMPDIR": str(tmp),
                "LEAN_PATH": module_path,
            }
            return run(argv, cwd=tmp, env=child_env)

        outputs = {
            "statement": lean_run("Statement.lean", lean_path, True),
            "obligation": lean_run("ObligationTree.lean", lean_path, False),
            "proof": lean_run("Proof.lean", f"{tmp}:{lean_path}", False),
            "validation": lean_run("Validation.lean", f"{tmp}:{lean_path}", False),
        }
        objects = {"Statement.olean": sha256(tmp / "Statement.olean")}
        return outputs, objects


def assert_network_isolation(bwrap: Path, outer_isolated: bool) -> None:
    if outer_isolated:
        interfaces = Path("/proc/net/dev").read_text(encoding="utf-8")
        assert all(
            line.strip().startswith("lo:")
            for line in interfaces.splitlines()[2:]
            if line.strip()
        )
        prefix: list[str] = []
    else:
        prefix = [
            str(bwrap),
            "--ro-bind",
            "/",
            "/",
            "--dev",
            "/dev",
            "--proc",
            "/proc",
            "--unshare-net",
            "--die-with-parent",
        ]
    probe = subprocess.run(
        prefix
        + [
            "/usr/bin/python3",
            "-I",
            "-c",
            "import socket; s=socket.socket(); s.settimeout(.2); s.connect(('1.1.1.1', 53))",
        ],
        env=BASE_ENV,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=10,
        check=False,
    )
    assert probe.returncode != 0, "network-denial mutation unexpectedly connected"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--probe", action="store_true")
    parser.add_argument("--worker-packet", type=Path)
    args = parser.parse_args()
    outer_isolated = os.environ.get("STAGE1_OUTER_NETWORK_ISOLATED") == "1"

    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    targets = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    statement = load(HERE / "statement.json")
    instance = load(HERE / "instance.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    task_dag = load(HERE / "task-dag.json")
    proof_blocker = load(HERE / "proof-blocker.json")
    proof_recheck = load(
        HERE / "proof-recheck-2026-07-15-head-472dc79e-slot17.json"
    )

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target == {
        "execution_rank": 38,
        "legacy_priority_slot": "S1-M-038",
        "theorem_id": THEOREM,
        "name": "川又消没定理",
        "category": "几何学 / 代数几何",
        "source_status_untrusted": "已验证",
        "baseline": "L0",
        "rework_required": True,
        "legacy_artifacts_accepted": False,
        "target_lane": "hard_mathlib_anchor_and_wrapper",
        "intake_score": 154,
        "lifecycle_mode": "planned",
        "theorem_complete": False,
    }
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item == {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 38,
        "phase": "validation",
        "layer": 5,
        "state": "[ ]",
        "depends_on": ["S56-M-0119-PROOF"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Run hermetic kernel, trust, provenance, and independent validation gates.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }
    predecessor = next(
        row for row in execution["items"] if row["id"] == "S56-M-0119-PROOF"
    )
    assert predecessor["state"] == "[_]" and predecessor["attempts"] == 1
    local_predecessor = next(
        row for row in task_dag["tasks"] if row["id"] == "S56-M-0119-PROOF"
    )
    assert local_predecessor["state"] == "open"
    assert local_predecessor["accepted_receipt_ids"] == []

    for name, expected in EXPECTED_INPUTS.items():
        assert sha256(HERE / name) == expected, f"stale validation input: {name}"
    assert sha256(LEAN_ROOT / "lean-toolchain") == TOOLCHAIN_SHA256
    assert sha256(LEAN_ROOT / "lake-manifest.json") == MANIFEST_SHA256
    assert statement["elaborated_print_sha256"] == EXPRESSION_SHA256
    assert instance["canonical_formal_target"]["elaborated_expression_hash"] == (
        f"sha256:{EXPRESSION_SHA256}"
    )
    assert instance["assurance"] == {
        "baseline": "L0",
        "rework_required": True,
        "human_debt": "H4",
        "machine_debt": "M3",
        "readability_debt": "R4",
        "audit_complete": False,
        "theorem_complete": False,
        "accepted_evidence_ids": [],
    }
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    boundary = graphs["closure_boundary"]
    assert boundary["closed_obligations"] == []
    assert boundary["root_machine_debt"] == "M3"
    assert boundary["remaining_root_cut_set"] == FROZEN_ROOT_CUT
    assert boundary["theorem_complete"] is False
    assert proof_blocker["verdict"] == "blocked"
    assert proof_blocker["root_closed"] is proof_blocker["theorem_complete"] is False
    assert proof_recheck["verdict"] == "blocked"
    assert proof_recheck["state"] == "[_]"
    assert proof_recheck["canonical_backend_target_refuted"] is True
    assert proof_recheck["accepted_receipt_ids"] == []
    assert proof_recheck["remaining_root_cut_set"] == FROZEN_ROOT_CUT
    assert proof_recheck["proposed_invalidation_and_retry_boundary"] == (
        INVALIDATION_BOUNDARY
    )

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by|run_tac)\b|"
        r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
        r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
        r"(?:axiom|constant|opaque|unsafe|extern)\b",
        re.MULTILINE,
    )
    for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
        source = source_without_comments_or_strings(
            (HERE / name).read_text(encoding="utf-8")
        )
        assert prohibited.search(source) is None, f"prohibited mechanism in {name}"
    validation_source = (HERE / "Validation.lean").read_text(encoding="utf-8")
    for forbidden in (
        "import Proof",
        "not_kawamataViehwegVanishingTarget",
        "counterexampleData",
        "Int.zero_ne_one",
    ):
        assert forbidden not in validation_source, forbidden
    for required in (
        "ZMod 2",
        "independent_root_countermodel",
        "assert_no_sorry independent_root_countermodel",
        "#print_validation_closure",
    ):
        assert required in validation_source, required

    manifest = load(LEAN_ROOT / "lake-manifest.json")
    mathlib_entry = next(row for row in manifest["packages"] if row["name"] == "mathlib")
    assert mathlib_entry["rev"] == mathlib_entry["inputRev"] == MATHLIB_REVISION
    assert mathlib_entry["url"] == MATHLIB_REMOTE
    assert (LEAN_ROOT / ".lake").is_symlink()
    mathlib = (LEAN_ROOT / ".lake/packages/mathlib").resolve()
    assert git("rev-parse", "HEAD", cwd=mathlib) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == MATHLIB_TREE
    assert git("remote", "get-url", "origin", cwd=mathlib) == MATHLIB_REMOTE
    assert git("status", "--porcelain=v1", "--untracked-files=all", cwd=mathlib) == ""
    assert sha256(mathlib / "LICENSE") == MATHLIB_LICENSE_SHA256
    for relative, evidence in SELECTED_MATHLIB_BOUNDARIES.items():
        source = mathlib / relative
        olean = mathlib / ".lake/build/lib/lean" / relative.replace(".lean", ".olean")
        assert git("rev-parse", f"HEAD:{relative}", cwd=mathlib) == evidence["blob"]
        assert sha256(source) == evidence["source_sha256"]
        assert sha256(olean) == evidence["olean_sha256"]

    elan = Path(HOME) / ".elan/bin/elan"
    assert sha256(elan) == ELAN_SHA256
    lean = Path(run([str(elan), "which", "lean"], env=BASE_ENV).strip())
    lake = Path(run([str(elan), "which", "lake"], env=BASE_ENV).strip())
    bwrap = Path("/usr/bin/bwrap")
    python = Path("/usr/bin/python3").resolve()
    git_executable = Path("/usr/bin/git")
    assert sha256(lean) == LEAN_SHA256
    assert sha256(lake) == LAKE_SHA256
    assert sha256(bwrap) == BWRAP_SHA256
    assert sha256(python) == PYTHON_SHA256
    assert sha256(git_executable) == GIT_SHA256
    assert LEAN_COMMIT in run([str(lean), "--version"], env=BASE_ENV)
    assert_network_isolation(bwrap, outer_isolated)

    outputs, objects = isolated_replay(
        lean, bwrap, pinned_lean_path(lean), outer_isolated
    )
    combined = "\n".join(outputs.values())
    assert "sorryAx" not in combined and "error:" not in combined.lower()
    assert reported_axioms(outputs["proof"], PROOF_DECLARATION) == EXPECTED_AXIOMS
    for declaration in COMPOSITION_DECLARATIONS:
        assert_no_axioms(outputs["obligation"], declaration)
    assert reported_axioms(outputs["validation"], VALIDATION_DECLARATION) == EXPECTED_AXIOMS
    assert outputs["validation"].count("Declarations are sorry-free!") == 1
    closure_match = re.search(
        r"VALIDATION_CLOSURE declarations=(\d+) modules=(\d+)",
        outputs["validation"],
    )
    assert closure_match is not None
    assert (
        "VALIDATION_CLOSURE axioms=[propext, Classical.choice, Quot.sound]"
        in outputs["validation"]
    )
    assert "VALIDATION_CLOSURE bodyless_nonaxioms=[]" in outputs["validation"]
    assert "VALIDATION_CLOSURE unsafe=[]" in outputs["validation"]
    observation = {
        "lean_output_sha256": {
            name: hashlib.sha256(output.encode()).hexdigest()
            for name, output in outputs.items()
        },
        "fresh_object_sha256": objects,
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
    assert args.worker_packet is not None
    packet = load(args.worker_packet)
    assert spec["schema_version"] == "stage1-validation-spec/1.0"
    assert spec["spec_id"] == "S56-M-0119-VALIDATION-local-v1"
    assert spec["item_id"] == receipt["item_id"] == packet["item_id"] == ITEM
    assert spec["theorem_id"] == receipt["theorem_id"] == THEOREM
    assert spec["depends_on"] == receipt["depends_on"] == ["S56-M-0119-PROOF"]
    assert len(spec["recipes"]) == 1 and spec["recipes"][0] == receipt["recipe"]
    recipe = spec["recipes"][0]
    assert recipe["argv"] == [
        "/usr/bin/python3",
        "-I",
        "-B",
        f"Stage1_Instances/{THEOREM}/check_validation.py",
        "--worker-packet",
        ".stage1-worker-selftest.json",
    ]
    assert recipe["network_policy"] == "denied"
    assert recipe["expected_exit"] == 0 and recipe["timeout_seconds"] == 900
    assert recipe["covered_obligation_ids"] == []
    assert recipe["validated_blocker_obligation_ids"] == [
        "M0119-S-DATA",
        "M0119-S-HYP",
        "M0119-ROOT",
    ]
    assert not outer_isolated, "recorded recipe isolates every Lean child, not Python metadata checks"

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["phase"] == "validation" and receipt["intent"] == "validate"
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == packet["state"] == "[_]"
    assert receipt["accepted"] is receipt["release_grade"] is False
    assert receipt["verdict"] == "blocked"
    assert receipt["lifecycle_before"] == receipt["lifecycle_after"] == "planned"
    assert receipt["root_vector_before"] == receipt["root_vector_after"] == ROOT_VECTOR
    assert receipt["accepted_receipt_ids"] == []
    started = datetime.fromisoformat(receipt["validation_started_at"])
    ended = datetime.fromisoformat(receipt["validation_ended_at"])
    validated = datetime.fromisoformat(receipt["validated_at"])
    assert started.tzinfo is not None and ended.tzinfo is not None
    assert validated.tzinfo is not None and started <= ended == validated
    assert ended <= datetime.now(timezone.utc)
    for name, expected in EXPECTED_INPUTS.items():
        assert receipt["inputs"][name] == expected, name
    assert receipt["inputs"]["validation-spec.json"] == sha256(HERE / "validation-spec.json")
    assert receipt["inputs"]["check_validation.py"] == sha256(Path(__file__).resolve())
    assert receipt["inputs"]["lean-toolchain"] == TOOLCHAIN_SHA256
    assert receipt["inputs"]["lake-manifest.json"] == MANIFEST_SHA256

    repository = receipt["repository_state"]
    assert repository["release_clean"] is False
    tracked_patch = run(
        ["/usr/bin/git", "diff", "--binary", "--", f"Stage1_Instances/{THEOREM}"],
        env=BASE_ENV,
    ).encode()
    assert tracked_patch == b""
    assert repository["tracked_patch_sha256"] == hashlib.sha256(tracked_patch).hexdigest()
    assert repository["tracked_patch_bytes"] == 0
    input_scope = [
        f"Stage1_Instances/{THEOREM}/Validation.lean",
        f"Stage1_Instances/{THEOREM}/check_validation.py",
        f"Stage1_Instances/{THEOREM}/validation-phase.md",
        f"Stage1_Instances/{THEOREM}/validation-spec.json",
    ]
    payload = [{"path": path, "sha256": sha256(ROOT / path)} for path in input_scope]
    assert repository["untracked_input_scope"] == input_scope
    assert repository["untracked_input_sha256"] == {
        row["path"]: row["sha256"] for row in payload
    }
    assert repository["untracked_input_bundle_sha256"] == hashlib.sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    assert repository["preexisting_lake_symlink_target_sha256"] == hashlib.sha256(
        os.readlink(LEAN_ROOT / ".lake").encode()
    ).hexdigest()

    environment = receipt["environment"]
    assert environment["platform"] == (
        f"{platform.system()} {platform.release()} {platform.machine()}"
    )
    assert environment["lean_executable_sha256"] == sha256(lean)
    assert environment["lake_executable_sha256"] == sha256(lake)
    assert environment["bubblewrap_executable_sha256"] == sha256(bwrap)
    assert environment["python_executable_sha256"] == sha256(python)
    assert environment["git_executable_sha256"] == sha256(git_executable)

    result = receipt["result"]
    assert result["lean_output_sha256"] == observation["lean_output_sha256"]
    assert result["fresh_object_sha256"] == observation["fresh_object_sha256"]
    assert result["observed_axioms"] == observation["observed_axioms"]
    assert result["validation_closure"] == observation["validation_closure"]
    assert result["supported_obligation_ids"] == []
    assert result["provisionally_closed_obligation_ids"] == []
    assert result["accepted_closed_obligation_ids"] == []
    assert result["validated_blocker_obligation_ids"] == [
        "M0119-S-DATA",
        "M0119-S-HYP",
        "M0119-ROOT",
    ]
    assert result["proof_dependency_master_acceptance"] == "fail_closed"
    assert result["root_closed"] is result["root_kernel_closed"] is False
    assert result["root_machine_debt"] == "M3"
    assert result["machine_debt_diagnosis"] == (
        "M5 proposed for the refutable backend encoding; accepted state remains M3"
    )
    assert result["frozen_graph_remaining_root_cut_set"] == FROZEN_ROOT_CUT
    assert result["proposed_invalidation_and_retry_boundary"] == INVALIDATION_BOUNDARY
    for key in (
        "complete_trust_provenance_gate",
        "human_source_gate",
        "readability_gate",
        "hermetic_release_gate",
        "independent_distinct_runner_gate",
    ):
        assert result[key].startswith("fail_closed"), key
    assert result["audit_complete"] is result["theorem_complete"] is False
    assert result["accepted_state_changed"] is False
    assert receipt["first_failed_gate"] == (
        "dependency.S56-M-0119-PROOF.master_acceptance_and_"
        "S56-5.1-exact-target-consistency"
    )
    assert receipt["first_failed_release_gate"] == (
        "S56-10.6-HERMETIC-COLD-EMPTY-CACHE"
    )
    assert receipt["remaining_root_cut_set"] == FROZEN_ROOT_CUT
    assert receipt["proposed_invalidation_and_retry_boundary"] == (
        INVALIDATION_BOUNDARY
    )
    assert receipt["changed_paths"] == CHANGED_PATHS
    assert receipt["output_summary"] == SUMMARY_LINES
    summary_bytes = ("\n".join(SUMMARY_LINES) + "\n").encode()
    assert receipt["output_evidence"] == {
        "stream": "stdout",
        "bytes": len(summary_bytes),
        "line_count": len(SUMMARY_LINES),
        "sha256": hashlib.sha256(summary_bytes).hexdigest(),
        "exit_code": 0,
        "archive_classification": (
            "deterministic nonrelease semantic summary; transient Lean streams "
            "are separately content-addressed but are not a release archive"
        ),
    }

    assert set(packet) == {
        "item_id",
        "changed_paths",
        "commands",
        "output_summary",
        "base_revision",
        "known_failures",
        "state",
    }
    assert packet["item_id"] == ITEM and packet["base_revision"] == BASE_REVISION
    assert packet["changed_paths"] == CHANGED_PATHS
    assert packet["known_failures"] == receipt["known_failures"]
    assert packet["output_summary"] == SUMMARY_LINES
    actual_changed = {
        line[3:]
        for line in git("status", "--short", "--untracked-files=all").splitlines()
        if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual_changed == set(CHANGED_PATHS), actual_changed
    for relative in CHANGED_PATHS:
        assert_text_hygiene(ROOT / relative)

    print("\n".join(SUMMARY_LINES))


if __name__ == "__main__":
    main()
