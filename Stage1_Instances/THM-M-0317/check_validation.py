#!/usr/bin/env python3
"""Fail-closed narrow validator for S56-M-0317-VALIDATION."""

from __future__ import annotations

import hashlib
import json
import os
from datetime import datetime
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0317"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
ITEM = "S56-M-0317-VALIDATION"
THEOREM = "THM-M-0317"
BASE_REVISION = "e46e0735d0940bb558acaf027d8386de2579f55d"
BASE_TREE = "9f03ecc77e82eda1f0ea3f0f4b08d1d7419ce0cf"
LEAN_TOOLCHAIN = "leanprover/lean4:v4.29.0"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
LEAN_SHA256 = "3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf"
LAKE_SHA256 = "a608ff084d7e2af228b92a29d7c2fd083ba0580e46889175ec74a81678c98359"
BWRAP_SHA256 = "0abea81db798ebf6b4742ac0664802d97521547a353c2a0dbdc21d76cbbfd2c0"
PYTHON_SHA256 = "b8d8288faefdd300201f43fcf00f6f539a27218eeed3a3dff5ab10b9c4c99700"
ELAN_SHA256 = "840179e70803ef373c2ec53342d6a45ea7d022533e4145489fc1278b4f716385"
TOOLCHAIN_SHA256 = "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2"
MANIFEST_SHA256 = "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MATHLIB_REMOTE = "https://github.com/leanprover-community/mathlib4.git"
MATHLIB_LICENSE_SHA256 = "b40930bbcf80744c86c46a12bc9da056641d722716c378f5659b9e555ef833e1"
DENOMINATOR_SHA256 = "aa74ec72cb476dc8775c8c3f33afbe71b8ea6e6d1cd3422c1e19625e18a8d68d"
EXPECTED_INPUT_HASHES = {
    "Statement.lean": "94c90b4b7a6dda1083b80b80907264b91e89cf5f2a6cb285e06a161be238dff2",
    "ObligationTree.lean": "bba7554df1b27f64cb8a69a0237cdd3b151cbec8b0d49fdfcb2f501b7bae2624",
    "Proof.lean": "da908a598cfd7e18c53fae440f4491b062d6ecd0605903b7fe924bee6a87b216",
    "Validation.lean": "ead54431497749917bc7d8d78798a3829c153461b72a289dc78e3ae0896bd427",
    "anchor-audit.json": "c6bf134e9ab189197b67330111f68f963fbd0d0e2e1de153bd4063f9069b6c39",
    "anchor-audit.md": "65f12bf5f705c60adacc9c6020aaafdcc85c14f373654f4ce308959dbf5791ff",
    "obligation-registry.json": "d67f99adec35a52a547b9ba1b49187613dcd27dfd2746754dc4a0539abbdbbde",
    "typed-graphs.json": "4d8c4f814cc065dc81a5bf90a357a57fc5d7ff3271350901acca64fcd19879a0",
    "validation-specs.json": "1782500c10182512d428735e5df4f2c48184776458ff2a99e9fdf33a1e113300",
    "proof-receipt.json": "b36ca8d96a61b198b6283ce02e21d656826c89ec3a5fbd62b5eb12be20309f02",
    "proof-blocker.json": "edc0c51dac45c1b5d91241f5f75446db07f521f2d4d9338ef910d1d12d617a81",
    "source-statement-crosswalk.md": "b4f9a2dfe294ee41f230c9d4bd84fc17d58d9c080e9903da5a51206ff56f292a",
    "check_obligation_tree.py": "069b4e2e0320604910f0db4cb37ed8b416d6fdb54d678f23ab8f1a7e77cf6cf4",
    "instance.json": "592cba93934fa28e3b10e6324087193146fe61f9df5a6f888ba90a03e1ea81d5",
}
SELECTED_PROVENANCE = {
    "Mathlib/Topology/ClusterPt.lean": {
        "source_sha256": "135af2d589d2ed4f97e734169195a838d98cba4218bd70b1c985c7e1fc699ddc",
        "git_blob": "ee04ae1be70c2840c60e7334388671e3c148bb48",
        "olean_sha256": "9c32e9c6b4de611021a77031fd092569b7b08ced059f0cb5ea22f6468d50c57a",
    },
    "Mathlib/Topology/Compactness/Compact.lean": {
        "source_sha256": "b98c88119c35b7f0a0b8ab922d4f8c63cb2074c3326dbdf58cf1b838b77faf18",
        "git_blob": "cdcc570028e7e6e03be778d3bca8551834ecf3b6",
        "olean_sha256": "08a8a1f958e1bb0f753ae0cca1a07191b7938e31c7fec40c97ece70bb48bb9c8",
    },
    "Mathlib/Topology/Separation/Basic.lean": {
        "source_sha256": "e0287fc4450a66ab81bd9baec0079d88c30547ebd3c4bbd46d4830f5ad05d4f7",
        "git_blob": "a675daef765b420b075c9b5a9d54213e310acdd0",
        "olean_sha256": "c7e4d6ce3a075cfb59db5d80c0228e3387df40612a01e9a70abaa5a0ec4269c2",
    },
}
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
GRAPH_PRE_PROOF_CLOSED = [
    "M0317-S-BOUNDARY",
    "M0317-S-DEFINITIONS",
    "M0317-S-DOMAINS",
    "M0317-T-ASSEMBLE",
]
PROVISIONALLY_VALIDATED = [
    "M0317-N-NEIGHBORHOODS",
    "M0317-L-COMPACT-LIMIT",
    "M0317-T-LIMIT",
]
STATEMENT_DECLARATIONS = (
    "AwesomeTheorems.THM_M_0317.ambient_subtype_fixed_point_iff",
    "AwesomeTheorems.THM_M_0317.empty_boundary_rejects_removed_nonempty",
    "AwesomeTheorems.THM_M_0317.ambient_domain_does_not_imply_member_domain",
    "AwesomeTheorems.THM_M_0317.fixed_point_cannot_precede_map_binder",
    "AwesomeTheorems.THM_M_0317.interval_rejects_removed_mapsTo",
)
COMPOSITION_DECLARATIONS = (
    "AwesomeTheorems.THM_M_0317.root_of_approximation_and_limit",
)
PROOF_DECLARATIONS = (
    "AwesomeTheorems.THM_M_0317.zero_mem_closure_displacement_image",
    "AwesomeTheorems.THM_M_0317.isClosed_displacement_image",
    "AwesomeTheorems.THM_M_0317.compactnessLimitPackage",
)
VALIDATION_DECLARATIONS = (
    "AwesomeTheorems.THM_M_0317.Validation.compactnessLimitPackage_validation",
    "AwesomeTheorems.THM_M_0317.Validation.conditionalExactRoot_validation",
)
EXPECTED_SUMMARY = (
    "PASS S56-M-0317-VALIDATION narrow network-isolated validation\n"
    "kernel: exact statement, four mutations, conditional composition, three partial proof declarations, and two differential declarations replayed with trust zero\n"
    "trust: all proof-bearing declarations are sorry-free and report only propext, Classical.choice, and Quot.sound\n"
    "provenance: local proof hashes, clean pinned mathlib, three selected source/blob/olean identities, license, and tool digests agree\n"
    "blocked: ApproximationPackage and the exact root remain open; complete TCB/provenance, cold empty-cache replay, and distinct-runner verification fail closed\n"
).encode("utf-8")
EXPECTED_SUMMARY_SHA256 = hashlib.sha256(EXPECTED_SUMMARY).hexdigest()
RECIPE_ARGV = [
    "/usr/bin/bwrap", "--ro-bind", "/", "/", "--dev", "/dev",
    "--proc", "/proc", "--tmpfs", "/tmp", "--unshare-net",
    "--die-with-parent", "--setenv", "LANG", "C.UTF-8",
    "--setenv", "LC_ALL", "C.UTF-8", "--setenv", "TZ", "UTC",
    "--setenv", "LEAN_NUM_THREADS", "1", "--setenv",
    "STAGE1_SKIP_RECEIPT_CHECK", "0", "--setenv",
    "STAGE1_OUTER_NETWORK_ISOLATED", "1", "/usr/bin/python3", "-I", "-B",
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

if not __debug__:
    raise RuntimeError("validation requires Python assertions")


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


def run(
    argv: list[str], *, cwd: Path = ROOT, env: dict[str, str] | None = None,
    timeout: int = 720,
) -> str:
    result = subprocess.run(
        argv, cwd=cwd, env=env, text=True, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, timeout=timeout, check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"command failed ({result.returncode}): {argv!r}\n{result.stdout}"
        )
    return result.stdout


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["git", *args], cwd=cwd).rstrip()


def source_without_comments(source: str) -> str:
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
    no_axioms = f"'{declaration}' does not depend on any axioms"
    pattern = re.compile(
        re.escape(f"'{declaration}' depends on axioms: [") + r"(.*?)]",
        re.DOTALL,
    )
    matches = pattern.findall(output)
    assert output.count(no_axioms) + len(matches) == 1, declaration
    if not matches:
        return set()
    return {part.strip() for part in matches[0].split(",") if part.strip()}


spec = load(HERE / "validation-spec.json")
registry = load(HERE / "obligation-registry.json")
graphs = load(HERE / "typed-graphs.json")
frozen_specs = load(HERE / "validation-specs.json")
proof_receipt = load(HERE / "proof-receipt.json")
proof_blocker = load(HERE / "proof-blocker.json")
execution = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")
receipt_path = HERE / "validation-receipt.json"
receipt = load(receipt_path) if receipt_path.exists() else None
verify_receipt = os.environ.get("STAGE1_SKIP_RECEIPT_CHECK") != "1"
if verify_receipt:
    assert receipt is not None, "final validation receipt is required"
    assert (ROOT / ".stage1-worker-selftest.json").is_file(), (
        "final worker self-test manifest is required"
    )

assert git("rev-parse", "HEAD") == BASE_REVISION
assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
item = next(row for row in execution["items"] if row["id"] == ITEM)
assert item == {
    "id": ITEM,
    "theorem_id": THEOREM,
    "execution_rank": 683,
    "phase": "validation",
    "layer": 5,
    "state": "[ ]",
    "depends_on": ["S56-M-0317-PROOF"],
    "owned_paths": [f"Stage1_Instances/{THEOREM}"],
    "deliverable": "Run hermetic kernel, trust, provenance, and independent validation gates.",
    "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
    "attempts": 0,
    "children": [],
}
predecessor = next(row for row in execution["items"] if row["id"] == "S56-M-0317-PROOF")
assert predecessor["state"] == "[_]" and predecessor["attempts"] == 1

assert spec["schema_version"] == "stage1-validation-spec/1.0"
assert spec["item_id"] == ITEM and spec["theorem_id"] == THEOREM
assert spec["argv"] == RECIPE_ARGV and spec["cwd"] == "."
assert spec["network_policy"] == "denied" and spec["expected_exit"] == 0
assert spec["timeout_seconds"] == 720
assert spec["env_allowlist"] == {
    "HOME": "variable: host account used only by the Lake/Elan pinned-toolchain locator",
    "PATH": "variable: host path used only to discover the Lake launcher, after which tool binaries are digest-checked",
    "LANG": "C.UTF-8",
    "LC_ALL": "C.UTF-8", "TZ": "UTC", "LEAN_NUM_THREADS": "1",
    "STAGE1_SKIP_RECEIPT_CHECK": "variable: 0 for the recorded final recipe; 1 only for receipt bootstrapping",
    "STAGE1_OUTER_NETWORK_ISOLATED": "1",
}
assert len(spec["covered_obligation_ids"]) == len(set(spec["covered_obligation_ids"]))
assert set(spec["covered_declarations"]) == {
    "AwesomeTheorems.THM_M_0317.TychonoffFixedPointTarget",
    *STATEMENT_DECLARATIONS,
    *COMPOSITION_DECLARATIONS,
    *PROOF_DECLARATIONS,
    *VALIDATION_DECLARATIONS,
}

for name, expected in EXPECTED_INPUT_HASHES.items():
    assert sha256(HERE / name) == expected, f"bound validation input changed: {name}"
assert registry["frozen_against_statement_sha256"] == EXPECTED_INPUT_HASHES["Statement.lean"]
assert registry["denominator_sha256"] == graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
assert registry["root_obligation_id"] == graphs["root_node_id"] == "M0317-ROOT"
closure = graphs["closure_boundary"]
assert closure["closed_obligations"] == GRAPH_PRE_PROOF_CLOSED
assert closure["root_closed"] is closure["audit_complete"] is closure["theorem_complete"] is False
assert closure["remaining_root_cut_set"] == ["M0317-T-APPROX", "M0317-T-LIMIT"]
assert frozen_specs["item_id"] == "S56-M-0317-OBLIGATION_TREE"
assert len(frozen_specs["recipes"]) == 17
assert {recipe["command"] for recipe in frozen_specs["recipes"]} == {
    f"python3 Stage1_Instances/{THEOREM}/check_obligation_tree.py"
}

assert proof_receipt["item_id"] == "S56-M-0317-PROOF"
assert proof_receipt["support_state"] == "provisional_worker_selftest"
assert proof_receipt["proof_body"]["source_sha256"] == sha256(HERE / "Proof.lean")
assert proof_receipt["closed_obligation_ids"] == PROVISIONALLY_VALIDATED
assert proof_receipt["result"]["root_closed"] is False
assert proof_receipt["result"]["theorem_complete"] is False
assert proof_receipt["remaining_root_cut_set"] == ["M0317-T-APPROX", "M0317-ROOT"]
assert proof_blocker["root_closed"] is proof_blocker["theorem_complete"] is False
assert proof_blocker["first_failed_gate"].startswith("M0317-T-APPROX")
assert proof_blocker["remaining_root_cut_set"] == ["M0317-T-APPROX", "M0317-ROOT"]
instance = load(HERE / "instance.json")
assert instance["lifecycle"] == "planned"
assert instance["root_vector"] == {"H": "H1", "M": "M4", "R": "R4"}
assert instance["audit_complete"] is instance["theorem_complete"] is False

all_source = "\n".join(
    source_without_comments((HERE / name).read_text(encoding="utf-8"))
    for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean")
)
prohibited = re.compile(
    r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by)\b|"
    r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
    r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
    r"(?:axiom|constant|opaque|unsafe|extern)\b",
    re.MULTILINE,
)
assert prohibited.search(all_source) is None
validation_imports = (HERE / "Validation.lean").read_text(encoding="utf-8").split("/-!", 1)[0]
assert "Proof" not in validation_imports and "ObligationTree" not in validation_imports

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
for relative, record in SELECTED_PROVENANCE.items():
    source = mathlib / relative
    olean = mathlib / ".lake" / "build" / "lib" / "lean" / relative.replace(".lean", ".olean")
    assert sha256(source) == record["source_sha256"]
    assert git("rev-parse", f"HEAD:{relative}", cwd=mathlib) == record["git_blob"]
    assert sha256(olean) == record["olean_sha256"]
assert sha256(LEAN_ROOT / "lean-toolchain") == TOOLCHAIN_SHA256
assert sha256(LEAN_ROOT / "lake-manifest.json") == MANIFEST_SHA256

elan = Path(shutil.which("elan") or "")
bwrap = Path("/usr/bin/bwrap")
python = Path("/usr/bin/python3")
assert elan.is_file() and bwrap.is_file() and python.is_file()
assert sha256(elan) == ELAN_SHA256
discovery_env = {
    **os.environ,
    "ELAN_TOOLCHAIN": LEAN_TOOLCHAIN,
    "LANG": "C.UTF-8",
    "LC_ALL": "C.UTF-8",
    "TZ": "UTC",
    "LEAN_NUM_THREADS": "1",
}
lean = Path(run([str(elan), "which", "lean"], cwd=LEAN_ROOT, env=discovery_env).strip())
lake = Path(run([str(elan), "which", "lake"], cwd=LEAN_ROOT, env=discovery_env).strip())
assert lean.is_file() and lake.is_file()
assert sha256(lean) == LEAN_SHA256 and sha256(lake) == LAKE_SHA256
assert sha256(bwrap) == BWRAP_SHA256 and sha256(python) == PYTHON_SHA256
fixed_env = {
    "HOME": os.environ["HOME"],
    "PATH": "/usr/bin:/bin",
    "ELAN_TOOLCHAIN": LEAN_TOOLCHAIN,
    "LANG": "C.UTF-8",
    "LC_ALL": "C.UTF-8",
    "TZ": "UTC",
    "LEAN_NUM_THREADS": "1",
}
for key, expected in spec["env_allowlist"].items():
    if expected.startswith("variable:"):
        assert os.environ.get(key), key
    elif key == "STAGE1_OUTER_NETWORK_ISOLATED" and not verify_receipt:
        assert os.environ.get(key) in (None, "0", "1")
    elif verify_receipt or key != "STAGE1_SKIP_RECEIPT_CHECK":
        assert os.environ[key] == expected, (key, os.environ.get(key), expected)
assert LEAN_COMMIT in run([str(lean), "--version"], cwd=LEAN_ROOT, env=fixed_env)
assert "5.0.0" in run([str(lake), "--version"], cwd=LEAN_ROOT, env=fixed_env)
lean_path = run(
    [str(lake), "env", "printenv", "LEAN_PATH"], cwd=LEAN_ROOT, env=fixed_env
).strip()

tmp = Path(tempfile.mkdtemp(prefix="stage1-m0317-validation-", dir="/tmp"))
try:
    target = tmp / "Stage1_Instances" / THEOREM
    target.mkdir(parents=True)
    for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
        shutil.copy2(HERE / name, target / name)
    (tmp / "home").mkdir()

    def isolated_lean(
        args: list[str], *, module_paths: list[Path] | None = None,
        module_output: Path | None = None,
    ) -> str:
        prefixes = [str(path) for path in (module_paths or [])]
        path = ":".join([*prefixes, lean_path])
        if module_output is None:
            command_args = args
        else:
            command_args = ["-o", str(module_output), *args]
        child = [str(lean), "--trust=0", "-R", str(tmp), *command_args]
        child_env = {**fixed_env, "HOME": str(tmp / "home"), "LEAN_PATH": path}
        if os.environ.get("STAGE1_OUTER_NETWORK_ISOLATED") == "1":
            return run(child, cwd=LEAN_ROOT, env=child_env)
        return run([
            str(bwrap), "--ro-bind", "/", "/", "--bind", str(tmp), str(tmp),
            "--dev", "/dev", "--proc", "/proc", "--unshare-net",
            "--die-with-parent", "--setenv", "HOME", str(tmp / "home"),
            "--setenv", "ELAN_TOOLCHAIN", LEAN_TOOLCHAIN,
            "--setenv", "LANG", "C.UTF-8", "--setenv", "LC_ALL", "C.UTF-8",
            "--setenv", "TZ", "UTC", "--setenv", "LEAN_NUM_THREADS", "1",
            "--setenv", "LEAN_PATH", path, "--chdir", str(LEAN_ROOT), *child,
        ], cwd=ROOT, env=fixed_env)

    statement_output = isolated_lean(
        [str(target / "Statement.lean")], module_output=target / "Statement.olean",
    )
    obligation_output = isolated_lean(
        [str(target / "ObligationTree.lean")], module_paths=[target],
        module_output=target / "ObligationTree.olean",
    )
    proof_path = ":".join([str(target), lean_path])
    proof_child = [str(lean), "--trust=0", "-R", str(tmp), str(target / "Proof.lean")]
    if os.environ.get("STAGE1_OUTER_NETWORK_ISOLATED") == "1":
        proof_output = run(
            proof_child, cwd=LEAN_ROOT,
            env={**fixed_env, "HOME": str(tmp / "home"), "LEAN_PATH": proof_path},
        )
    else:
        proof_output = run([
            str(bwrap), "--ro-bind", "/", "/", "--bind", str(tmp), str(tmp),
            "--dev", "/dev", "--proc", "/proc", "--unshare-net",
            "--die-with-parent", "--setenv", "HOME", str(tmp / "home"),
            "--setenv", "ELAN_TOOLCHAIN", LEAN_TOOLCHAIN,
            "--setenv", "LANG", "C.UTF-8", "--setenv", "LC_ALL", "C.UTF-8",
            "--setenv", "TZ", "UTC", "--setenv", "LEAN_NUM_THREADS", "1",
            "--setenv", "LEAN_PATH", proof_path, "--chdir", str(LEAN_ROOT),
            *proof_child,
        ], cwd=ROOT, env=fixed_env)
    validation_output = isolated_lean([
        str(target / "Validation.lean")
    ], module_paths=[target])
finally:
    shutil.rmtree(tmp)

for declaration in COMPOSITION_DECLARATIONS:
    assert reported_axioms(obligation_output, declaration) <= EXPECTED_AXIOMS
for declaration in PROOF_DECLARATIONS:
    assert reported_axioms(proof_output, declaration) <= EXPECTED_AXIOMS
for declaration in VALIDATION_DECLARATIONS:
    assert reported_axioms(validation_output, declaration) <= EXPECTED_AXIOMS
for declaration in STATEMENT_DECLARATIONS:
    assert reported_axioms(validation_output, declaration) <= EXPECTED_AXIOMS
assert validation_output.count("Declarations are sorry-free!") == (
    len(STATEMENT_DECLARATIONS) + len(VALIDATION_DECLARATIONS)
)
combined_output = "\n".join(
    (statement_output, obligation_output, proof_output, validation_output)
)
assert "AwesomeTheorems.THM_M_0317.TychonoffFixedPointTarget" in statement_output
assert "sorryAx" not in combined_output
assert "declaration uses 'sorry'" not in combined_output
assert "error:" not in combined_output

if receipt is not None and verify_receipt:
    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["release_grade"] is False and receipt["verdict"] == "blocked"
    assert receipt["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert receipt["covered_obligation_ids"] == spec["covered_obligation_ids"]
    assert receipt["covered_declarations"] == spec["covered_declarations"]
    started = datetime.fromisoformat(receipt["validation_started_at"])
    ended = datetime.fromisoformat(receipt["validation_ended_at"])
    assert started <= ended
    assert receipt["validated_at"] == receipt["validation_ended_at"]
    assert receipt["inputs"]["validation_spec_sha256"] == sha256(HERE / "validation-spec.json")
    assert receipt["inputs"]["validator_sha256"] == sha256(Path(__file__).resolve())
    for key, name in (
        ("statement_source_sha256", "Statement.lean"),
        ("obligation_tree_source_sha256", "ObligationTree.lean"),
        ("proof_source_sha256", "Proof.lean"),
        ("validation_probe_sha256", "Validation.lean"),
        ("anchor_audit_json_sha256", "anchor-audit.json"),
        ("anchor_audit_md_sha256", "anchor-audit.md"),
        ("obligation_registry_sha256", "obligation-registry.json"),
        ("typed_graphs_sha256", "typed-graphs.json"),
        ("frozen_validation_specs_sha256", "validation-specs.json"),
        ("proof_receipt_sha256", "proof-receipt.json"),
        ("proof_blocker_sha256", "proof-blocker.json"),
        ("source_crosswalk_sha256", "source-statement-crosswalk.md"),
        ("obligation_validator_sha256", "check_obligation_tree.py"),
        ("instance_sha256", "instance.json"),
    ):
        assert receipt["inputs"][key] == sha256(HERE / name), key
    assert receipt["recipe"] == {
        key: spec[key]
        for key in (
            "recipe_id", "cwd", "argv", "env_allowlist", "timeout_seconds",
            "network_policy", "network_enforcement", "expected_exit",
        )
    }
    assert receipt["evidence_log"] == {
        "stream": "stdout",
        "bytes": len(EXPECTED_SUMMARY),
        "sha256": EXPECTED_SUMMARY_SHA256,
        "exit_code": 0,
        "archive_classification": "deterministic nonrelease semantic log digest; transient raw log is not a release archive",
    }
    result = receipt["result"]
    assert result["graph_recorded_pre_proof_closed_obligation_ids"] == GRAPH_PRE_PROOF_CLOSED
    assert result["graph_stale_open_after_proof_ids"] == PROVISIONALLY_VALIDATED
    assert result["newly_accepted_closed_obligation_ids"] == []
    assert result["provisionally_validated_obligation_ids"] == PROVISIONALLY_VALIDATED
    assert result["root_closed"] is False and result["root_kernel_closed"] is False
    assert result["audit_complete"] is result["theorem_complete"] is False
    assert result["accepted_root_vector_before"] == result["accepted_root_vector_after"] == {
        "H": "H1", "M": "M4", "R": "R4"
    }
    assert result["conditional_partial_root_vector_if_foundation_and_proof_acceptance_pass"] == {
        "H": "H1", "M": "M2", "R": "R4"
    }
    assert result["accepted_state_changed"] is False
    assert result["complete_transitive_provenance_gate"] == "fail_closed"
    assert result["complete_transitive_tcb_gate"] == "fail_closed"
    assert result["hermetic_release_gate"] == "fail_closed"
    assert result["independent_verification_gate"] == "fail_closed"
    assert receipt["first_failed_gate"].startswith("dependency.S56-M-0317-PROOF")
    assert receipt["remaining_root_cut_set"] == ["M0317-T-APPROX"]
    assert set(receipt["changed_paths"]) == CHANGED_PATHS

packet_path = ROOT / ".stage1-worker-selftest.json"
if packet_path.exists() and verify_receipt:
    packet = load(packet_path)
    assert set(packet) == {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert packet["item_id"] == ITEM and packet["state"] == "[_]"
    assert packet["base_revision"] == BASE_REVISION
    assert set(packet["changed_paths"]) == CHANGED_PATHS
    assert packet["known_failures"] == receipt["known_failures"]
    actual_changes = {
        line[3:] if line.startswith("?? ") else line[2:].lstrip()
        for line in git("status", "--short", "--untracked-files=all").splitlines()
    }
    actual_changes.discard("Formalizations/Lean/.lake")
    assert actual_changes == CHANGED_PATHS, (actual_changes, CHANGED_PATHS)

for relative in CHANGED_PATHS - {".stage1-worker-selftest.json"}:
    path = ROOT / relative
    if not path.exists():
        continue
    data = path.read_bytes()
    assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines()), path

print(EXPECTED_SUMMARY.decode("utf-8"), end="", flush=True)
