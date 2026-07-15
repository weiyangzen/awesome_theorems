#!/usr/bin/env python3
"""Fail-closed release reconciliation for S56-M-0508-RELEASE."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import platform
import re
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0508"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
ITEM = "S56-M-0508-RELEASE"
THEOREM = "THM-M-0508"
BASE_REVISION = "4d389eb47e043f6f44925a418baee0d034f764ba"
BASE_TREE = "64faabd76665273032b8cb1554b90655b5c94256"
VALIDATION_BASE_REVISION = "5b35bc151522d93c7f54966ef64f1fc630371537"
VALIDATION_BASE_TREE = "fe77824631ab2573a4596bddc1a2534c06cd23f8"
VALIDATION_RECEIPT_SHA256 = (
    "54cd6cf363b087299b41645585efed4df4960c00a657e480d959866b3d026051"
)
TOOLCHAIN = "leanprover/lean4:v4.29.0"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MATHLIB_REMOTE = "https://github.com/leanprover-community/mathlib4.git"
MATHLIB_LICENSE_SHA256 = (
    "b40930bbcf80744c86c46a12bc9da056641d722716c378f5659b9e555ef833e1"
)
EXPRESSION_SHA256 = "54ddaa6fe49c75368fd333adae9bc7ab50a9542516ef24d73fb5e43f0c1ac5fb"
DENOMINATOR_SHA256 = "79ff122b736335e90938cf7304db0b680dc23531e4d12d4b8c987d0ddc953bc2"
VECTOR = {"H": "H1", "M": "M4", "R": "R3"}
INVENTORY_IDS = [
    "M0508-ROOT", "M0508-S-COUNT", "M0508-L-COUNT-POS",
    "M0508-N-FOURIER", "M0508-B-ARCS", "M0508-C-MAJOR",
    "M0508-L-MAJOR", "M0508-L-SINGULAR", "M0508-C-MINOR",
    "M0508-L-MINOR", "M0508-L-POSITIVE", "M0508-T-ASSEMBLE",
    "M0508-X-SOURCE", "M0508-X-FOUNDATION", "M0508-X-PROVENANCE",
    "M0508-X-READABLE", "M0508-X-WORKFLOW",
]
MATHEMATICAL_CUT = [
    "M0508-N-FOURIER", "M0508-B-ARCS", "M0508-L-MAJOR",
    "M0508-L-SINGULAR", "M0508-L-MINOR",
]
GRAPH_CLOSED_IDS = ["M0508-L-COUNT-POS", "M0508-T-ASSEMBLE"]
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
EXPECTED_OUTPUT_SHA256 = {
    "statement": "dc51d7aea3ee9b4a2a258ffa97fcb4f5e74d748329bb3ef95690b54f51a19791",
    "anchor_audit": "5a07357f6cf3a2ea3fc344856838e2058260a1eaa0d0a20b93eb833b62fc5e87",
    "obligation_tree": "13c3f7cf67d48dd6d359997222b9a54ec341f1ec73b4423901428a2d18ef0669",
    "proof": "a1f6e807ce786fcef042d3902cb7464def5b3552e0ba34d02ae7c6119c5d67f8",
    "validation": "7d7d53835f26c3d90bb7c98d18b88496d6cf20a0525862685b26988b2c0554d0",
}
EXPECTED_INPUTS = {
    "README.md": "d3059dc69f9957225dca13b444fed22498fd41d459cfd5cfa0ee62a41cee6676",
    "scope-map.md": "eb835ee3c0ccab3291004b0bb0bdf467795d6447e16bf57d25788d956d2e13f5",
    "source-statement-crosswalk.md": "0b9764c62c33ae444f162ace9069eb062dd29012dc9f02cc95828bddbbdfd402",
    "instance.json": "714166282856b99e8d0e1170a5187f7739e565cf38dc05cc57b4393869e24744",
    "task-dag.json": "0ed037db47be3f58c1428162b03c81e67222538d9e337789332ca4808ee77ac0",
    "Statement.lean": "e27734b0b8a7c6ad8f858cba756fd1ac64abd3a7d3bbedde435c3d9a007080da",
    "AnchorAudit.lean": "64a284fa92225bd52c38bcdb665e96a9073503a655fdb2abcdc5592442752ece",
    "ObligationTree.lean": "576a3fc66f3ed890202b5d02acdd4188b5edc1842bc8d06ae8906499e93aa172",
    "Proof.lean": "b93b1556141f269c687cef3d4b738fa6f6dd8c3c49be01a9a4c8e5448bbe5e1f",
    "Validation.lean": "d85ebf994823fc6007a43420312e4d0972a63b7c48f27bda6551941893bb0276",
    "statement.json": "2ada9429a0cc593dddc826cb68156a9974116292fe9f42b433b109290b84a9b9",
    "anchor-audit.json": "dcb3df3d79927fa33a9ac3a28b128befb896b3c93e748f30e020963968a53d00",
    "obligation-registry.json": "1f5afb0285f5b3ed5b76f85ee0fc0dac5363b52a4d2f4c01fec35f1d6708d695",
    "typed-graphs.json": "86e4c89eba8b80aa5c8f4e0edbbd2e79d008ab7222a16e2fe811701568fb6539",
    "proof-receipt.json": "d212c0e5d69066fc0ad5be9588a2aace90555fa030c32012fd32033ee9dcd8b8",
    "proof-blocker.json": "dde0c80cd9f0cbafa25b4f244957f357a7be620b676622255335181c051e4ec0",
    "validation-spec.json": "f8cac3397a971a8a8860b7a6e5d553b96380ed8e0fb39f1478fe89d841881946",
    "validation-receipt.json": VALIDATION_RECEIPT_SHA256,
    "validation-blocker.json": "15729d66dd0bb1aab6510852e5d8e56dfb5997ff223523410a0cfe848b6bae9c",
    "check_validation.py": "b27c22c16969acab09f279187731a526eab8c1e3ea1bc5b992a63d3096dfbe1a",
}
AUTHORITY_INPUTS = {
    "Docs/Stage1_Targets_rev-5.6.json": "02eec284de534dd78e1cf75f82a477ff477567dd682b7445cb7587abd137ab2c",
    "Docs/Stage1_Execution_DAG_rev-5.6.json": "53bf6c3d561c7efd021a8813137f297193e83bbe3b470000eda0ac9773b855ec",
    "Docs/Stage1_Blueprint_rev-5.6.md": "808d1553ee4ed34a5cc6d5ada0e4f4b510780ad250e251c09145dac661a7d5d9",
    "Docs/Blueprint_Guidelines.md": "a06c07b5ca1b270b4935ad3dab893e9a0e078c29c8da2ef9dca1e71193310535",
    "skills/execute-stage1-rev56/SKILL.md": "26d47a66c6535feabb8bbf1051fd55d76a53fe761f4b3d953f86b97ec86152b8",
    "Formalizations/Lean/lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "Formalizations/Lean/lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
RELEASE_NAMES = (
    "check_release.py", "release-decision.json", "release-receipt.json",
    "release-spec.json", "release-validation.md",
)
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    *(f"Stage1_Instances/{THEOREM}/{name}" for name in RELEASE_NAMES),
}
SUMMARY_LINES = [
    "PASS S56-M-0508-RELEASE negative reconciliation",
    "PASS current trust-zero replay: exact interfaces and conditional compositions only",
    "BLOCKED dependency.S56-M-0508-VALIDATION.master_acceptance",
    "BLOCKED exact root: H1/M4/R3 unchanged; five-node analytic cut remains open",
    "BLOCKED AUDIT-Z and THEOREM-Z: source, state, trust, hermetic, and independent gates open",
    "verdict=blocked audit_complete=false theorem_complete=false accepted_receipts=0",
]


def load(path: Path) -> dict:
    def reject_duplicates(pairs: list[tuple[str, object]]) -> dict:
        value: dict[str, object] = {}
        for key, item in pairs:
            assert key not in value, f"duplicate JSON key in {path}: {key}"
            value[key] = item
        return value

    result = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicates)
    assert isinstance(result, dict), path
    return result


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(
    argv: list[str], *, cwd: Path = ROOT, env: dict[str, str] | None = None,
    timeout: int = 600,
) -> str:
    result = subprocess.run(
        argv, cwd=cwd, env=env, text=True, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, timeout=timeout, check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(f"command failed ({result.returncode}): {argv!r}\n{result.stdout}")
    return result.stdout


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["/usr/bin/git", *args], cwd=cwd, timeout=60).strip()


def code_without_comments(source: str) -> str:
    output: list[str] = []
    index = 0
    depth = 0
    in_string = False
    while index < len(source):
        if depth:
            if source.startswith("/-", index):
                depth += 1
                index += 2
            elif source.startswith("-/", index):
                depth -= 1
                index += 2
            else:
                index += 1
        elif in_string:
            if source[index] == "\\" and index + 1 < len(source):
                index += 2
            elif source[index] == '"':
                in_string = False
                output.append('"')
                index += 1
            else:
                index += 1
        elif source.startswith("/-", index):
            depth = 1
            index += 2
        elif source.startswith("--", index):
            newline = source.find("\n", index)
            index = len(source) if newline < 0 else newline
        elif source[index] == '"':
            in_string = True
            output.append('"')
            index += 1
        else:
            output.append(source[index])
            index += 1
    assert depth == 0 and not in_string, "unterminated Lean comment or string"
    return "".join(output)


def reported_axioms(output: str, declaration: str) -> set[str]:
    match = re.search(
        rf"'[^']*{re.escape(declaration)}' depends on axioms:\s*\[(.*?)\]",
        output, flags=re.DOTALL,
    )
    if match is None:
        assert f"'{declaration}' does not depend on any axioms" in output
        return set()
    return {
        part.strip()
        for part in match.group(1).replace("\n", "").split(",")
        if part.strip()
    }


def assert_text_hygiene(path: Path) -> None:
    data = path.read_bytes()
    assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data, path
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines()), path


def compiled_roots() -> list[Path]:
    packages = LEAN_ROOT / ".lake" / "packages"
    roots = sorted(
        (path / ".lake" / "build" / "lib" / "lean").resolve()
        for path in packages.iterdir()
        if path.is_dir() and (path / ".lake" / "build" / "lib" / "lean").is_dir()
    )
    assert roots, "no pre-existing pinned compiled artifacts"
    return roots


def current_lean_replay() -> dict[str, object]:
    fixed_env = {
        "ELAN_TOOLCHAIN": TOOLCHAIN,
        "LANG": "C.UTF-8",
        "LC_ALL": "C.UTF-8",
        "TZ": "UTC",
        "LEAN_NUM_THREADS": "1",
    }
    bwrap = Path("/usr/bin/bwrap")
    lean = Path.home() / ".elan/toolchains/leanprover--lean4---v4.29.0/bin/lean"
    lake = Path.home() / ".elan/toolchains/leanprover--lean4---v4.29.0/bin/lake"
    assert sha256(lean) == (
        "3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf"
    )
    assert sha256(lake) == (
        "a608ff084d7e2af228b92a29d7c2fd083ba0580e46889175ec74a81678c98359"
    )
    assert sha256(bwrap) == (
        "0abea81db798ebf6b4742ac0664802d97521547a353c2a0dbdc21d76cbbfd2c0"
    )
    assert LEAN_COMMIT in run([str(lean), "--version"], env=fixed_env)
    assert "5.0.0-src+98dc76e" in run([str(lake), "--version"], env=fixed_env)
    dependency_path = ":".join(str(path) for path in compiled_roots())

    with tempfile.TemporaryDirectory(prefix="m0508-release-", dir="/tmp") as name:
        tmp = Path(name).resolve()
        for source in (
            "Statement.lean", "AnchorAudit.lean", "ObligationTree.lean",
            "Proof.lean", "Validation.lean",
        ):
            (tmp / source).write_bytes((HERE / source).read_bytes())
        base = [
            str(bwrap), "--ro-bind", "/", "/", "--bind", str(tmp), str(tmp),
            "--dev", "/dev", "--proc", "/proc", "--unshare-net",
            "--die-with-parent", "--clearenv", "--setenv", "HOME", str(tmp),
            "--setenv", "TMPDIR", str(tmp), "--setenv", "LANG", "C.UTF-8",
            "--setenv", "LC_ALL", "C.UTF-8", "--setenv", "TZ", "UTC",
            "--setenv", "LEAN_NUM_THREADS", "1", "--chdir", str(tmp),
        ]

        def lean_run(
            source: str, local_imports: bool, emit_olean: bool,
            *, normalize_tmp_path: bool = False,
        ) -> str:
            lean_path = f"{tmp}:{dependency_path}" if local_imports else dependency_path
            argv = base + [
                "--setenv", "LEAN_PATH", lean_path, str(lake), "env", "lean",
                "--trust=0", f"--root={tmp}",
            ]
            if emit_olean:
                argv += ["-o", str(tmp / Path(source).with_suffix(".olean"))]
            argv.append(str(tmp / source))
            output = run(argv, env=fixed_env)
            if normalize_tmp_path:
                output = output.replace(str(tmp), "/tmp/m0508-release-TMP")
            return output

        outputs = {
            "statement": lean_run("Statement.lean", False, True),
            "anchor_audit": lean_run("AnchorAudit.lean", True, False),
            "obligation_tree": lean_run(
                "ObligationTree.lean", True, True, normalize_tmp_path=True,
            ),
            "proof": lean_run("Proof.lean", True, True),
            "validation": lean_run("Validation.lean", True, False),
        }

    assert {
        key: hashlib.sha256(value.encode()).hexdigest() for key, value in outputs.items()
    } == EXPECTED_OUTPUT_SHA256
    declarations = (
        "Stage1Instances.THM_M_0508.ObligationTree.representationCount_pos_iff",
        "Stage1Instances.THM_M_0508.ObligationTree.root_of_eventualPositiveRepresentationCount",
        "Stage1Instances.THM_M_0508.Proof.vinogradovThreePrimesTarget_iff_eventualPositiveRepresentationCount",
        "Stage1Instances.THM_M_0508.Proof.vinogradovThreePrimesTarget_of_eventualPositiveRepresentationCount",
        "Stage1Instances.THM_M_0508.Validation.rootFromEventualPositiveCount",
    )
    for declaration in declarations[:2]:
        assert reported_axioms(outputs["obligation_tree"], declaration) == EXPECTED_AXIOMS
        assert reported_axioms(outputs["validation"], declaration) == EXPECTED_AXIOMS
    for declaration in declarations[2:4]:
        assert reported_axioms(outputs["proof"], declaration) == EXPECTED_AXIOMS
        assert reported_axioms(outputs["validation"], declaration) == EXPECTED_AXIOMS
    assert reported_axioms(outputs["validation"], declarations[4]) == EXPECTED_AXIOMS
    combined = "\n".join(outputs.values())
    assert "sorryAx" not in combined and "declaration uses 'sorry'" not in combined
    assert all("error:" not in output for output in outputs.values())
    closure = re.search(
        r"VALIDATION_CLOSURE roots=(\d+) declarations=(\d+) modules=(\d+)",
        outputs["validation"],
    )
    assert closure is not None and int(closure.group(1)) == 5
    assert "VALIDATION_CLOSURE axioms=[propext, Classical.choice, Quot.sound]" in outputs["validation"]
    assert "VALIDATION_CLOSURE bodyless_nonaxioms=[]" in outputs["validation"]
    assert "VALIDATION_CLOSURE unsafe=[]" in outputs["validation"]
    return {
        "output_sha256": EXPECTED_OUTPUT_SHA256,
        "closure": {
            "roots": 5,
            "declarations": int(closure.group(2)),
            "modules": int(closure.group(3)),
            "axioms": sorted(EXPECTED_AXIOMS),
            "bodyless_nonaxioms": [],
            "unsafe_declarations": [],
        },
    }


def main() -> None:
    if not __debug__ or sys.flags.optimize != 0:
        raise RuntimeError("release checker requires Python assertions")

    decision = load(HERE / "release-decision.json")
    receipt = load(HERE / "release-receipt.json")
    spec = load(HERE / "release-spec.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")
    instance = load(HERE / "instance.json")
    local_dag = load(HERE / "task-dag.json")
    statement = load(HERE / "statement.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    proof = load(HERE / "proof-receipt.json")
    validation = load(HERE / "validation-receipt.json")
    targets = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    manifest = load(LEAN_ROOT / "lake-manifest.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    assert run([
        "/usr/bin/git", "merge-base", "--is-ancestor",
        VALIDATION_BASE_REVISION, BASE_REVISION,
    ]) == ""
    assert git("rev-parse", f"{VALIDATION_BASE_REVISION}^{{tree}}") == VALIDATION_BASE_TREE
    for name, expected in EXPECTED_INPUTS.items():
        assert sha256(HERE / name) == expected, f"reconciled input drifted: {name}"
    assert decision["reconciled_inputs"] == EXPECTED_INPUTS
    for name, expected in AUTHORITY_INPUTS.items():
        assert sha256(ROOT / name) == expected, f"authority input drifted: {name}"
    assert decision["authority_inputs"] == AUTHORITY_INPUTS

    target_rows = [row for row in targets["targets"] if row["theorem_id"] == THEOREM]
    assert len(target_rows) == 1
    target = target_rows[0]
    assert target["execution_rank"] == 882
    assert target["baseline"] == "L0" and target["rework_required"] is True
    assert target["legacy_artifacts_accepted"] is False
    assert target["lifecycle_mode"] == "planned" and target["theorem_complete"] is False
    items = {row["id"]: row for row in execution["items"]}
    assert items[ITEM] == {
        "id": ITEM, "theorem_id": THEOREM, "execution_rank": 882,
        "phase": "release", "layer": 6, "state": "[ ]",
        "depends_on": ["S56-M-0508-VALIDATION"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Reconcile evidence and decide the exact theorem-completion verdict.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0, "children": [],
    }
    assert items["S56-M-0508-VALIDATION"]["state"] == "[_]"
    assert items["S56-M-0508-VALIDATION"]["attempts"] == 1

    assert instance["lifecycle"] == local_dag["lifecycle"] == "planned"
    assert instance["root_vector"] == VECTOR
    assert instance["accepted_proof_state"] == []
    assert instance["audit_complete"] is instance["theorem_complete"] is False
    assert local_dag["accepted_states"] == []
    local_tasks = {row["id"]: row for row in local_dag["tasks"]}
    assert local_tasks[ITEM]["state"] == "open"
    assert local_tasks["S56-M-0508-VALIDATION"]["state"] == "open"

    assert statement["declaration"] == (
        "Stage1Instances.THM_M_0508.VinogradovThreePrimesTarget"
    )
    assert registry["root_obligation_id"] == "M0508-ROOT"
    assert registry["frozen_denominators"]["inventory"] == INVENTORY_IDS
    assert [row["obligation_id"] for row in registry["obligations"]] == INVENTORY_IDS
    assert graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert [row["obligation_id"] for row in graphs["nodes"]] == INVENTORY_IDS
    root = next(row for row in graphs["nodes"] if row["obligation_id"] == "M0508-ROOT")
    assert {
        "H": root["human_debt"], "M": root["machine_debt"], "R": root["readability_debt"],
    } == VECTOR
    assert root["evidence_ids"] == []
    closure = graphs["closure_boundary"]
    assert closure["closed_local_nodes"] == GRAPH_CLOSED_IDS
    assert closure["root_closed"] is False and closure["theorem_complete"] is False
    assert closure["first_open_cut_set"] == MATHEMATICAL_CUT
    assert all(
        row["evidence_ids"] == []
        for row in graphs["nodes"]
        if row["obligation_id"] in GRAPH_CLOSED_IDS
    )
    assert not (HERE / "validation-specs.json").exists()

    assert proof["support_state"] == "provisional_worker_selftest"
    assert proof["accepted"] is False
    assert proof["accepted_closed_obligation_ids"] == []
    assert proof["result"]["root_kernel_closed"] is False
    assert proof["remaining_root_cut_set"] == MATHEMATICAL_CUT
    assert sha256(HERE / "validation-receipt.json") == VALIDATION_RECEIPT_SHA256
    assert validation["base_revision"] == VALIDATION_BASE_REVISION
    assert validation["base_tree"] == VALIDATION_BASE_TREE
    assert validation["support_state"] == "provisional_worker_selftest"
    assert validation["accepted"] is validation["release_grade"] is False
    assert validation["accepted_receipt_ids"] == []
    assert validation["result"]["accepted_closed_obligation_ids"] == []
    assert validation["result"]["root_kernel_closed"] is False
    assert validation["result"]["open_root_cut_set"] == MATHEMATICAL_CUT
    assert validation["result"]["audit_complete"] is validation["result"]["theorem_complete"] is False
    assert validation["first_failed_gate"] == "dependency.S56-M-0508-PROOF.master_acceptance"
    predecessor = (HERE / "check_validation.py").read_text(encoding="utf-8")
    assert f'BASE_REVISION = "{VALIDATION_BASE_REVISION}"' in predecessor
    assert '"state": "[ ]"' in predecessor and '"attempts": 0' in predecessor
    assert '"--worker-packet", ".stage1-worker-selftest.json"' in predecessor

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by|extern)\b|"
        r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
        r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
        r"(?:axiom|constant|opaque|unsafe)\b",
        re.MULTILINE,
    )
    for name in (
        "Statement.lean", "AnchorAudit.lean", "ObligationTree.lean",
        "Proof.lean", "Validation.lean",
    ):
        source = code_without_comments((HERE / name).read_text(encoding="utf-8"))
        source = re.sub(r"^#print sorries .*?$", "", source, flags=re.MULTILINE)
        assert prohibited.search(source) is None, f"prohibited source construct in {name}"
    obligation_source = code_without_comments((HERE / "ObligationTree.lean").read_text())
    assert "def EventualPositiveRepresentationCount : Prop" in obligation_source
    assert re.search(
        r"(?:theorem|def)\s+eventualPositiveRepresentationCount\b", obligation_source,
    ) is None
    proof_source = code_without_comments((HERE / "Proof.lean").read_text())
    assert "(h : ObligationTree.EventualPositiveRepresentationCount)" in proof_source
    validation_source = code_without_comments((HERE / "Validation.lean").read_text())
    assert "(positive : ObligationTree.EventualPositiveRepresentationCount)" in validation_source

    mathlib_rows = [row for row in manifest["packages"] if row["name"] == "mathlib"]
    assert len(mathlib_rows) == 1
    mathlib_entry = mathlib_rows[0]
    assert mathlib_entry["rev"] == mathlib_entry["inputRev"] == MATHLIB_REVISION
    assert (LEAN_ROOT / ".lake").is_symlink()
    mathlib = (LEAN_ROOT / ".lake" / "packages" / "mathlib").resolve()
    assert git("rev-parse", "HEAD", cwd=mathlib) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == MATHLIB_TREE
    assert git("status", "--porcelain=v1", "--untracked-files=all", cwd=mathlib) == ""
    assert git("remote", "get-url", "origin", cwd=mathlib) == MATHLIB_REMOTE
    assert sha256(mathlib / "LICENSE") == MATHLIB_LICENSE_SHA256
    observation = current_lean_replay()
    assert observation["closure"] == {
        "roots": 5, "declarations": 2567, "modules": 103,
        "axioms": ["Classical.choice", "Quot.sound", "propext"],
        "bodyless_nonaxioms": [], "unsafe_declarations": [],
    }

    assert decision["schema_version"] == "stage1-release-decision/1.0"
    assert decision["item_id"] == ITEM and decision["theorem_id"] == THEOREM
    assert decision["phase"] == decision["intent"] == "release"
    assert decision["base_revision"] == BASE_REVISION and decision["base_tree"] == BASE_TREE
    assert decision["verdict"] == "blocked"
    assert decision["release_grade"] is decision["release_accepted"] is False
    assert decision["lifecycle_before"] == decision["lifecycle_after"] == "planned"
    assert decision["accepted_receipt_ids"] == decision["accepted_closed_obligation_ids"] == []
    assert decision["root_vector"] == {"before": VECTOR, "after": VECTOR}
    assert decision["terminal_decisions"] == {
        "audit_complete": False, "theorem_complete": False,
        "audit_z": "blocked", "theorem_z": "blocked", "release_accepted": False,
    }
    assert decision["first_failed_gate"]["gate_id"] == "S56-10.2-DEPENDENCY-ACCEPTANCE"
    assert decision["first_failed_gate"]["dependency_gate"] == (
        "dependency.S56-M-0508-VALIDATION.master_acceptance"
    )
    assert decision["nested_predecessor_failure"]["gate_id"] == (
        "dependency.S56-M-0508-PROOF.master_acceptance"
    )
    assert decision["first_failed_theorem_gate"]["gate_id"] == "M0508-N-FOURIER"
    assert decision["first_failed_reproduction_gate"]["gate_id"] == (
        "S56-10.6-HERMETIC-COLD-EMPTY-CACHE"
    )
    assert decision["mathematical_root_cut_set"] == MATHEMATICAL_CUT
    dependency = decision["dependency"]
    assert dependency["receipt_id"] == validation["receipt_id"]
    assert dependency["receipt_sha256"] == VALIDATION_RECEIPT_SHA256
    assert dependency["accepted"] is dependency["master_accepted"] is False
    reconciliation = decision["evidence_reconciliation"]
    assert reconciliation["accepted_closed_obligation_ids"] == []
    assert reconciliation["typed_graph_claimed_closed_obligation_ids"] == GRAPH_CLOSED_IDS
    assert reconciliation["graph_claimed_closed_nodes_have_evidence_ids"] is False
    assert reconciliation["proof_and_validation_accepted_closed_obligation_ids"] == []
    assert reconciliation["predecessor_validation_specs_present"] is False
    for key in (
        "validation_dependency_master_accepted", "exact_root_kernel_closed",
        "structured_public_state_reconciled", "pinpoint_h0_and_independent_source_review",
        "independent_r0_review", "audit_z_accepted", "accepted_foundation_profile",
        "complete_transitive_provenance_and_tcb", "immutable_clean_release_input",
        "hermetic_empty_cache_cold_offline_replay", "complete_sbom_license_archive_closure",
        "two_independent_signed_runner_attestations", "independently_implemented_minimal_verifier",
        "protected_ci_and_adversarial_gates", "deterministic_content_addressed_release_bundle",
        "master_acceptance",
    ):
        assert reconciliation[key] is False, key

    assert spec["schema_version"] == "stage1-release-recipe/1.0"
    assert spec["item_id"] == receipt["item_id"] == ITEM
    assert spec["theorem_id"] == receipt["theorem_id"] == THEOREM
    assert spec["argv"] == [
        "/usr/bin/python3", "-I", "-B", f"Stage1_Instances/{THEOREM}/check_release.py",
    ]
    assert spec["cwd"] == "." and spec["timeout_seconds"] == 600
    assert spec["network_policy"] == "denied" and spec["expected_exit"] == 0
    assert spec["covered_obligation_ids"] == []
    assert spec["observed_open_state_obligation_ids"] == INVENTORY_IDS
    assert "proof or acceptance evidence for none" in spec["coverage_semantics"]

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["depends_on"] == ["S56-M-0508-VALIDATION"]
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]"
    assert receipt["accepted"] is receipt["release_grade"] is receipt["master_accepted"] is False
    assert receipt["content_addressed_release_evidence"] is False
    assert receipt["decision_id"] == decision["decision_id"]
    assert receipt["decision_sha256"] == sha256(HERE / "release-decision.json")
    assert receipt["release_spec_sha256"] == sha256(HERE / "release-spec.json")
    assert receipt["release_validation_sha256"] == sha256(HERE / "release-validation.md")
    assert receipt["checker_sha256"] == sha256(HERE / "check_release.py")
    assert receipt["verdict"] == "blocked"
    assert receipt["recipe"] == {
        key: spec[key] for key in (
            "recipe_id", "cwd", "argv", "env_allowlist", "timeout_seconds",
            "network_policy", "network_enforcement", "expected_exit", "expected_outputs",
            "covered_obligation_ids", "observed_open_state_obligation_ids",
            "coverage_semantics", "covered_declarations", "declaration_coverage_semantics",
        )
    }
    result = receipt["result"]
    assert result["verdict"] == "blocked"
    assert result["lifecycle_before"] == result["lifecycle_after"] == "planned"
    assert result["root_vector_before"] == result["root_vector_after"] == VECTOR
    assert result["accepted_receipt_ids"] == result["accepted_closed_obligation_ids"] == []
    assert result["mathematical_root_cut_set"] == MATHEMATICAL_CUT
    assert result["current_lean_replay"] == "pass_nonrelease_warm_cache"
    assert result["current_lean_output_sha256"] == EXPECTED_OUTPUT_SHA256
    assert result["current_trust_closure_observation"] == observation["closure"]
    assert result["audit_complete"] is result["theorem_complete"] is False
    assert result["audit_z"] == result["theorem_z"] == "blocked"
    assert result["release_accepted"] is False
    assert receipt["accepted_receipt_ids"] == []
    assert receipt["known_failures"] == decision["known_failures"]
    assert receipt["output_summary"] == SUMMARY_LINES
    assert receipt["environment"]["platform"] == (
        f"{platform.system()} {platform.release()} {platform.machine()}"
    )

    assert set(packet) == {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert packet["item_id"] == ITEM and packet["state"] == "[_]"
    assert packet["base_revision"] == BASE_REVISION
    assert set(packet["changed_paths"]) == CHANGED_PATHS
    assert packet["known_failures"] == decision["known_failures"]
    assert packet["commands"] == receipt["commands_and_results"]
    assert packet["output_summary"] == receipt["output_summary"]
    assert any(
        command.get("argv") == spec["argv"] and command.get("exit_code") == 0
        for command in packet["commands"]
    )
    actual_changed = {
        line[3:] for line in git(
            "status", "--short", "--untracked-files=all", "--",
            str(HERE.relative_to(ROOT)), ".stage1-worker-selftest.json",
        ).splitlines()
    }
    assert actual_changed == CHANGED_PATHS, (actual_changed, CHANGED_PATHS)

    handoff = (HERE / "release-validation.md").read_text(encoding="utf-8")
    for fragment in (
        "`blocked`", "`[H1, M4, R3]`", "`AUDIT-Z`", "`THEOREM-Z`",
        "This worker accepts no receipt", "release_grade=false",
    ):
        assert fragment in handoff, fragment
    assert str(ROOT) not in handoff
    for relative in CHANGED_PATHS:
        assert_text_hygiene(ROOT / relative)

    print("\n".join(SUMMARY_LINES))


if __name__ == "__main__":
    main()
