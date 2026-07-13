#!/usr/bin/env python3
"""Fail-closed provenance, pin, kernel, and receipt checks for THM-M-1244."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
LEAN_ROOT = ROOT / "Formalizations/Lean"
ITEM = "S56-M-1244-PROOF"
THEOREM = "THM-M-1244"
BASE_REVISION = "8f22279fd1216cdfb5676c758e6bdb08e0ba3e01"
BASE_TREE = "d2e9e68da52ecfcfe15a9c48ac2262400e602667"
EXPRESSION_SHA256 = "eeff335a47ceaf9d469f25e1570640f17008c1f38d8173499a5429e7ab6397b3"
DENOMINATOR_SHA256 = "edecb957b6903682647ae02dbfff3d6bdd693e6ddf2decd18721fdcae702c297"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MANIFEST_SHA256 = "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81"
UPSTREAM_REVISION = "7b82b1323c80f0c21ca449fd12e1c24315ae9782"
LICENSE_SHA256 = "cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30"

SOURCE_ROWS = {
    "SLT/ConvergenceL1Subseq.lean": ("9c68b82984246989606811af9dc629925b7b4cf33bb93b9639038be1ab2e4236", "9c68b82984246989606811af9dc629925b7b4cf33bb93b9639038be1ab2e4236"),
    "SLT/EfronStein.lean": ("5c1880799e993d938174138055fa2027f0cfb6cfe350be07bdfe61578759d179", "44354c785c5ac07f7da08d21ed38f537fd1299efc9579aa1bdaffb0c435b6456"),
    "SLT/GaussianLSI/BernoulliLSI.lean": ("f7559b7951cf84623385eb47847a9c3a2dd5978282f72250ff9410b79029b984", "36bd56b4c667ab6e8b7c9edaa5d640405cba7c1ec49636e435bb36ed7a9eda11"),
    "SLT/GaussianLSI/DualEntApp.lean": ("d2854bb651567555867f649d2feff5bfd5533d13def74a58828b6e78a3d233e6", "d2854bb651567555867f649d2feff5bfd5533d13def74a58828b6e78a3d233e6"),
    "SLT/GaussianLSI/DualityEntropy.lean": ("8cbfae7f02a04c99e0328c5d33f1ab022e4b54269333f13124cbdb7ee30377b5", "8cbfae7f02a04c99e0328c5d33f1ab022e4b54269333f13124cbdb7ee30377b5"),
    "SLT/GaussianLSI/Entropy.lean": ("00530d1b319448a5a668439018da08b7bd9b40be518262e108fe4ac9ffcdc6b7", "00530d1b319448a5a668439018da08b7bd9b40be518262e108fe4ac9ffcdc6b7"),
    "SLT/GaussianLSI/OneDimGLSI.lean": ("d3e36df5fcc34c1e61be53e538f457c0a657e36929f60dea92fc90b8c661001b", "d3e36df5fcc34c1e61be53e538f457c0a657e36929f60dea92fc90b8c661001b"),
    "SLT/GaussianLSI/OneDimGLSICompSmo.lean": ("ebe756ab83c2439881aa3805fd1de5073c5166f94fa7fbb6e641506502cc13c1", "ebe756ab83c2439881aa3805fd1de5073c5166f94fa7fbb6e641506502cc13c1"),
    "SLT/GaussianLSI/SubAddEnt/Basic.lean": ("02c10a2452dd29d6f6cb3b69e43904a5eafeed1e932b129e0f699f43a6a24e60", "02c10a2452dd29d6f6cb3b69e43904a5eafeed1e932b129e0f699f43a6a24e60"),
    "SLT/GaussianLSI/SubAddEnt/Decomposition.lean": ("e4e6641911c25b40ebd0047f23da951ba87fb2fd92d43740d1ab8318e737d955", "e4e6641911c25b40ebd0047f23da951ba87fb2fd92d43740d1ab8318e737d955"),
    "SLT/GaussianLSI/SubAddEnt/Subadditivity.lean": ("56e92f6158b1ad6af070b94680777f392970c38ccce71ff1aae745bb1b6c2ac0", "56e92f6158b1ad6af070b94680777f392970c38ccce71ff1aae745bb1b6c2ac0"),
    "SLT/GaussianLSI/TensorizedGLSI.lean": ("22eefaf07248a28de214b07154ecd953e50ed7c9432931ac9e2fe34ea9c45e29", "22eefaf07248a28de214b07154ecd953e50ed7c9432931ac9e2fe34ea9c45e29"),
    "SLT/GaussianLSI/TwoPoint.lean": ("b74b7bd6edba94b9b64b7605865b4d4630591b785cb145e787a3aabab5ae4520", "b74b7bd6edba94b9b64b7605865b4d4630591b785cb145e787a3aabab5ae4520"),
    "SLT/GaussianMeasure.lean": ("c679103bbd2a7e2fc652e1c13cba264d012964e6815ab50ef9546c58b3412907", "c679103bbd2a7e2fc652e1c13cba264d012964e6815ab50ef9546c58b3412907"),
    "SLT/GaussianPoincare/EfronSteinApp.lean": ("822375e389fe964533054515c7ceb03c1c41fd27fadd31a2f09aa1916ba7e63f", "2b5631646fc83b07d45d2fc515c407e07ae8dc219f8fe1150736bcf0f30b780d"),
    "SLT/GaussianPoincare/LevyContinuity.lean": ("c43b8d505fd646fd7340a8f29b7364ea134897f71ca8f32d1a5b5203707546c9", "c71e1289fe5f75030ff32465ada05b1522b45009e4844b418f596ab889914d1a"),
    "SLT/GaussianPoincare/Limit.lean": ("ac574efd3fb6d67c47259760265db0565b6c93975d54a21e6d959ec7db117169", "c6c88ea7022fa12e9cb46b4a5667a054300755793fe397416601df8bf8e0a684"),
    "SLT/GaussianPoincare/RademacherApprox.lean": ("796b6d91ff2fd1c2e8702a0e2c7a0af1197ef36c2b2f6dfccd4b69703b343f45", "7ef64a5fc146c92729d1423390f6c99f7bb02311b1e6643c869c95db06e1453b"),
    "SLT/GaussianPoincare/TaylorBound.lean": ("f62c49a5fd5be645a97515b40bfd2a5759cfce142f47ea8935231fa14322a0b0", "863b6903e2fa482631be039f4bef6a0e9af33bae2b4b1f69529fb41aa99aee84"),
    "SLT/GaussianSobolevDense/Cutoff.lean": ("320a4547b0fb1ad886d58451bd43aec61f4a6d01a0051966528ebe3504194dd0", "320a4547b0fb1ad886d58451bd43aec61f4a6d01a0051966528ebe3504194dd0"),
    "SLT/GaussianSobolevDense/Defs.lean": ("a587ce9b807413eef7c49045db83187f0b1bcf23f03831522172094967f62b3a", "a587ce9b807413eef7c49045db83187f0b1bcf23f03831522172094967f62b3a"),
    "SLT/GaussianSobolevDense/Density.lean": ("356e93dfdc51936c1ec37a25f23434ab6966acc3379a350be2ee02996e7f0374", "356e93dfdc51936c1ec37a25f23434ab6966acc3379a350be2ee02996e7f0374"),
    "SLT/GaussianSobolevDense/Mollification.lean": ("98e65bbfe6a509332a4213121a4b30bdde001c6aba848e8a7beb2e56133792a9", "40c30859078f52a87b724aace4d1f829941810149f74c66f1458c501d3aa54cd"),
    "SLT/MeasureInfrastructure.lean": ("21fd2a3c99695943d3b6e0d9b977d5816aedfe73a02cf522365a0ae7af6cec7a", "21fd2a3c99695943d3b6e0d9b977d5816aedfe73a02cf522365a0ae7af6cec7a"),
}

MODULES = [
    "SLT/EfronStein", "SLT/ConvergenceL1Subseq", "SLT/GaussianLSI/Entropy",
    "SLT/GaussianLSI/TwoPoint", "SLT/GaussianPoincare/LevyContinuity",
    "SLT/GaussianPoincare/RademacherApprox", "SLT/GaussianPoincare/EfronSteinApp",
    "SLT/GaussianPoincare/TaylorBound", "SLT/GaussianPoincare/Limit",
    "SLT/GaussianLSI/BernoulliLSI", "SLT/GaussianLSI/OneDimGLSICompSmo",
    "SLT/MeasureInfrastructure", "SLT/GaussianMeasure", "SLT/GaussianSobolevDense/Defs",
    "SLT/GaussianSobolevDense/Cutoff", "SLT/GaussianSobolevDense/Mollification",
    "SLT/GaussianSobolevDense/Density", "SLT/GaussianLSI/OneDimGLSI",
    "SLT/GaussianLSI/DualityEntropy", "SLT/GaussianLSI/DualEntApp",
    "SLT/GaussianLSI/SubAddEnt/Basic", "SLT/GaussianLSI/SubAddEnt/Decomposition",
    "SLT/GaussianLSI/SubAddEnt/Subadditivity", "SLT/GaussianLSI/TensorizedGLSI",
]

REACHABLE_IDS = {
    "M1244-ROOT", "M1244-S-DEFS", "M1244-S-DOMAIN", "M1244-S-BOUNDARY",
    "M1244-N-MEASURE", "M1244-N-ENTROPY", "M1244-N-REGULARITY",
    "M1244-B-ZEROMASS", "M1244-C-COORD", "M1244-L-UPSTREAM",
    "M1244-L-POINTWISE", "M1244-L-INTEGRAL", "M1244-T-PACKAGES",
    "M1244-T-ASSEMBLE",
}
PROOF_IDS = REACHABLE_IDS - {
    "M1244-S-DEFS", "M1244-S-DOMAIN", "M1244-S-BOUNDARY"
}
OPEN_IDS = [
    "M1244-S-DEFS", "M1244-S-DOMAIN", "M1244-S-BOUNDARY", "M1244-S-FOUNDATION"
]


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict), f"{path} must contain a JSON object"
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_output(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(["git", *args], cwd=cwd, text=True).strip()


def strip_comments(source: str) -> str:
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


def replace_once(source: str, port: str, upstream: str, name: str) -> str:
    assert source.count(port) == 1, f"{name}: compatibility block count is not one"
    return source.replace(port, upstream, 1)


def reconstruct_upstream(name: str, source: str) -> str:
    upstream_digest, port_digest = SOURCE_ROWS[name]
    if upstream_digest == port_digest:
        return source
    relative = "../PORT_PROVENANCE.md" if name == "SLT/EfronStein.lean" else "../../PORT_PROVENANCE.md"
    notice = ("/- Port notice: modified for the repository's pinned Lean 4.29/mathlib APIs.\n"
              f"The exact compatibility edit is recorded in `{relative}`. -/\n")
    source = replace_once(source, notice, "", name)
    edits: dict[str, list[tuple[str, str]]] = {
        "SLT/EfronStein.lean": [("        exact e.map_symm_map.symm.trans (congrArg (Measure.map e.symm) h1)",
            "        have h2 : (Measure.map e (Measure.pi (fun _ : Fin 1 => μs 0))).map e.symm = (μs 0).map e.symm := by\n          rw [h1]\n        rw [MeasurableEquiv.map_symm_map] at h2\n        exact h2")],
        "SLT/GaussianLSI/BernoulliLSI.lean": [("rw [integral_fintype Integrable.of_finite]", "rw [integral_fintype _ (Integrable.of_finite)]")],
        "SLT/GaussianPoincare/EfronSteinApp.lean": [("Measure.ae_ennreal_smul_measure_iff", "Measure.ae_smul_measure_iff")],
        "SLT/GaussianPoincare/RademacherApprox.lean": [("Measure.ae_ennreal_smul_measure_iff", "Measure.ae_smul_measure_iff")],
        "SLT/GaussianPoincare/TaylorBound.lean": [("  -- taylorWithinEval f 1", "  simp only [hone_eq] at hξ_eq\n  -- taylorWithinEval f 1")],
        "SLT/GaussianSobolevDense/Mollification.lean": [("        intro y\n        unfold stdMollifierPi\n        simp\n", "        intro y\n        unfold stdMollifierPi\n        simp only [Fintype.univ_ofIsEmpty, Finset.prod_empty]\n")],
    }
    if name == "SLT/GaussianPoincare/LevyContinuity.lean":
        assert source.count("tendsto_iSup_of_tendsto_limsup_atTop") == 3
        source = source.replace("tendsto_iSup_of_tendsto_limsup_atTop", "tendsto_iSup_of_tendsto_limsup")
        for port, upstream in [
            ("h_sup (fun _ ↦ bot_le) ?_", "h_sup (fun _ ↦ zero_le') ?_"),
            ("(h z)\n    (fun _ ↦ bot_le) fun r", "(h z)\n    (fun _ ↦ zero_le') fun r"),
            (".of_forall fun _ ↦ (zero_le _)", ".of_forall fun _ ↦ zero_le'"),
            ("      exact integral_const_mul _ _", "      rw [integral_const_mul]"),
        ]:
            source = replace_once(source, port, upstream, name)
        return source
    if name == "SLT/GaussianPoincare/Limit.lean":
        source = replace_once(source, "import Mathlib.Analysis.Complex.Asymptotics\n", "", name)
        source = replace_once(source,
            "  apply Complex.tendsto_pow_exp_of_isLittleO_sub_add_div t\n  exact (Complex.isLittleO_ofReal_right.mpr hf).congr\n    (fun n => by simp) (fun n => by simp)",
            "  let g n := f n - 1\n  have fg n : f n = 1 + g n := by ring\n  simp_rw [fg, add_sub_add_left_eq_sub] at hf ⊢\n  apply Complex.tendsto_one_add_pow_exp_of_tendsto\n  rw [← tendsto_sub_nhds_zero_iff]\n  apply hf.tendsto_inv_smul_nhds_zero.congr'\n  filter_upwards [eventually_ne_atTop 0] with n h0\n  simpa [mul_sub] using mul_div_cancel₀ t (mod_cast h0)", name)
        source = replace_once(source,
            "    -- Goal: ↑(2⁻¹) * exp(it) + ↑(2⁻¹) * exp(-it) = cos(t)\n    change ((2 : ℝ)⁻¹ : ℝ) • exp (-(↑t * I)) +\n        ((2 : ℝ)⁻¹ : ℝ) • exp (↑t * I) = ↑(Real.cos t)\n    rw [Complex.real_smul, Complex.real_smul]",
            "    simp only [real_smul]\n    -- Goal: ↑(2⁻¹) * exp(it) + ↑(2⁻¹) * exp(-it) = cos(t)", name)
        return source
    for port, upstream in edits[name]:
        source = replace_once(source, port, upstream, name)
    return source


def source_imports(path: Path) -> list[str]:
    return re.findall(r"^import (SLT\.[A-Za-z0-9_.]+)$", path.read_text(encoding="utf-8"), re.MULTILINE)


def run_lean_trust_zero() -> str:
    lean = subprocess.check_output(["lake", "env", "which", "lean"], cwd=LEAN_ROOT, text=True).strip()
    lean_path = subprocess.check_output(["lake", "env", "printenv", "LEAN_PATH"], cwd=LEAN_ROOT, text=True).strip()
    output: list[str] = []
    with tempfile.TemporaryDirectory(prefix="thm-m-1244-proof-") as raw_tmp:
        tmp = Path(raw_tmp)
        for filename in ("Statement.lean", "ObligationTree.lean", "Proof.lean"):
            shutil.copy2(HERE / filename, tmp / filename)
        shutil.copytree(HERE / "SLT", tmp / "SLT")
        env = os.environ.copy()
        env["LEAN_PATH"] = f"{tmp}:{lean_path}"
        env["LEAN_NUM_THREADS"] = "2"
        for module in ["Statement", "ObligationTree", *MODULES, "Proof"]:
            source = tmp / f"{module}.lean"
            obj = tmp / f"{module}.olean"
            command = [lean, "--trust=0", "-t0", "-R", str(tmp), "-o", str(obj), str(source)]
            result = subprocess.run(command, cwd=tmp, env=env, text=True,
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=1800, check=False)
            output.append(f"[{module}]\n{result.stdout}")
            assert result.returncode == 0, "".join(output)
        assert not list(HERE.rglob("*.olean")), "validation wrote an owned .olean"
        assert not list(HERE.rglob("*.ilean")), "validation wrote an owned .ilean"
    return "".join(output)


def main() -> None:
    proof_path = HERE / "Proof.lean"
    receipt_path = HERE / "proof-receipt.json"
    validation_path = HERE / "proof-validation.md"
    packet_path = ROOT / ".stage1-worker-selftest.json"
    statement = load(HERE / "statement.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")

    assert git_output("rev-parse", "HEAD") == BASE_REVISION
    assert git_output("rev-parse", "HEAD^{tree}") == BASE_TREE
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item == {"id": ITEM, "theorem_id": THEOREM, "execution_rank": 425,
        "phase": "proof", "layer": 4, "state": "[ ]",
        "depends_on": ["S56-M-1244-OBLIGATION_TREE"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Implement or pin/import the required proof bodies without placeholders.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0, "children": []}
    predecessor = next(row for row in execution["items"] if row["id"] == "S56-M-1244-OBLIGATION_TREE")
    assert predecessor["state"] == "[_]"

    formal = statement["canonical_formal_target"]
    assert formal["declaration_or_expression"] == "Stage1Instances.THM_M_1244.GaussianLogSobolevTarget"
    assert formal["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert formal["statement_file_sha256"] == sha256(HERE / "Statement.lean")
    assert registry["frozen_against_statement_sha256"] == sha256(HERE / "Statement.lean")
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert set(registry["frozen_denominators"]["required_machine"]) == PROOF_IDS | set(OPEN_IDS)
    children: dict[str, list[str]] = {}
    for edge in graphs["graphs"]["proof"]["edges"]:
        if edge["type"] == "proof_requires":
            children.setdefault(edge["from"], []).append(edge["to"])
    reached: set[str] = set()
    pending = ["M1244-ROOT"]
    while pending:
        node = pending.pop()
        if node not in reached:
            reached.add(node)
            pending.extend(children.get(node, []))
    assert reached == REACHABLE_IDS

    actual_sources = {path.relative_to(HERE).as_posix() for path in (HERE / "SLT").rglob("*.lean")}
    assert actual_sources == set(SOURCE_ROWS)
    imports = {name: source_imports(HERE / name) for name in SOURCE_ROWS}
    assert sum(map(len, imports.values())) == 35
    imported_paths = {module.replace(".", "/") + ".lean" for values in imports.values() for module in values}
    assert imported_paths <= set(SOURCE_ROWS)
    reachable_modules = {"SLT/GaussianLSI/TensorizedGLSI.lean"}
    todo = list(reachable_modules)
    while todo:
        for module in imports[todo.pop()]:
            path = module.replace(".", "/") + ".lean"
            if path not in reachable_modules:
                reachable_modules.add(path)
                todo.append(path)
    assert reachable_modules == set(SOURCE_ROWS)

    prohibited = re.compile(r"\b(sorry|admit|sorryAx|implemented_by|native_decide|extern|opaque)\b|^[ \t]*(axiom|constant|unsafe)[ \t]+", re.MULTILINE)
    lean_paths = [proof_path, *(HERE / name for name in SOURCE_ROWS)]
    provenance = (HERE / "PORT_PROVENANCE.md").read_text(encoding="utf-8")
    assert "PORT_HASH" not in provenance and UPSTREAM_REVISION in provenance
    for name, (upstream_digest, port_digest) in SOURCE_ROWS.items():
        path = HERE / name
        assert sha256(path) == port_digest, name
        source = path.read_bytes().decode("utf-8")
        assert prohibited.search(strip_comments(source)) is None, name
        reconstructed = reconstruct_upstream(name, source).encode("utf-8")
        assert hashlib.sha256(reconstructed).hexdigest() == upstream_digest, name
        for value in (name, upstream_digest, port_digest):
            assert value in provenance, (name, value)
    proof = proof_path.read_text(encoding="utf-8")
    assert prohibited.search(strip_comments(proof)) is None
    for marker in ("import SLT.GaussianLSI.TensorizedGLSI", "theorem coordinateLogSobolevPackage",
        "GaussianLSI.gaussian_logSobolev_W12_pi", "theorem coordinateToOperatorEnergyPackage",
        "theorem gaussianLogSobolev : GaussianLogSobolevTarget", "#print sorries gaussianLogSobolev",
        "#print axioms GaussianLSI.gaussian_logSobolev_W12_pi", "#print axioms gaussianLogSobolev"):
        assert marker in proof, marker

    assert sha256(HERE / "LICENSE") == LICENSE_SHA256
    assert "Apache License" in (HERE / "LICENSE").read_text(encoding="utf-8")
    mathlib = LEAN_ROOT / ".lake/packages/mathlib"
    assert git_output("rev-parse", "HEAD", cwd=mathlib) == MATHLIB_REVISION
    assert git_output("rev-parse", "HEAD^{tree}", cwd=mathlib) == MATHLIB_TREE
    assert git_output("status", "--porcelain=v1", cwd=mathlib) == ""
    assert sha256(LEAN_ROOT / "lake-manifest.json") == MANIFEST_SHA256
    assert (LEAN_ROOT / ".lake").is_symlink()

    lean_output = run_lean_trust_zero()
    assert "declaration uses 'sorry'" not in lean_output
    assert "declaration has metavariables" not in lean_output
    assert lean_output.count("Declarations are sorry-free!") == 4
    for declaration in ("GaussianLSI.gaussian_logSobolev_W12_pi",
        "Stage1Instances.THM_M_1244.coordinateLogSobolevPackage",
        "Stage1Instances.THM_M_1244.coordinateToOperatorEnergyPackage",
        "Stage1Instances.THM_M_1244.gaussianLogSobolev"):
        expected = (re.escape(f"'{declaration}' depends on axioms: [") +
            r"\s*propext,\s*Classical\.choice,\s*Quot\.sound\s*\]")
        assert re.search(expected, lean_output), (declaration, lean_output[-5000:])

    receipt = load(receipt_path)
    packet = load(packet_path)
    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["accepted"] is False and receipt["proposed_state"] == "[_]"
    assert receipt["canonical_target_expression_sha256"] == EXPRESSION_SHA256
    assert receipt["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert set(receipt["provisionally_closed_proof_obligation_ids"]) == PROOF_IDS
    assert receipt["required_machine_open_ids"] == OPEN_IDS
    assert receipt["accepted_closed_obligation_ids"] == []
    assert receipt["proof_body"]["source_sha256"] == sha256(proof_path)
    for key, filename in (
        ("statement_sha256", "Statement.lean"),
        ("obligation_tree_sha256", "ObligationTree.lean"),
        ("obligation_registry_sha256", "obligation-registry.json"),
        ("typed_graphs_sha256", "typed-graphs.json"),
        ("anchor_audit_sha256", "anchor_audit.json"),
        ("validation_markdown_sha256", "validation.md"),
        ("port_provenance_sha256", "PORT_PROVENANCE.md"),
        ("license_sha256", "LICENSE"),
    ):
        assert receipt["inputs"][key] == sha256(HERE / filename), key
    assert receipt["environment"]["mathlib_revision"] == MATHLIB_REVISION
    assert receipt["environment"]["mathlib_tree"] == MATHLIB_TREE
    assert receipt["environment"]["lake_manifest_sha256"] == MANIFEST_SHA256
    assert receipt["result"]["axioms"] == ["propext", "Classical.choice", "Quot.sound"]
    assert receipt["result"]["root_kernel_closed"] is True
    assert receipt["result"]["accepted_root_closed"] is False
    assert receipt["result"]["theorem_complete"] is False
    assert set(packet) == {"item_id", "changed_paths", "commands", "output_summary", "base_revision", "known_failures", "state"}
    assert packet["item_id"] == ITEM and packet["state"] == "[_]" and packet["base_revision"] == BASE_REVISION
    assert packet["known_failures"] == receipt["known_failures"]
    status = subprocess.check_output(
        ["git", "status", "--short", "--untracked-files=all"],
        cwd=ROOT,
        text=True,
    )
    actual_changes = {line[3:] for line in status.splitlines()
        if line[3:] != "Formalizations/Lean/.lake" and not line[3:].startswith("Formalizations/Lean/.lake/")}
    assert all(path == ".stage1-worker-selftest.json" or
        path.startswith(f"Stage1_Instances/{THEOREM}/") for path in actual_changes), actual_changes
    assert set(packet["changed_paths"]) == actual_changes
    assert set(receipt["changed_paths"]) == actual_changes
    validation = validation_path.read_text(encoding="utf-8")
    assert "theorem completion" in validation.lower() and "pending master acceptance" in validation.lower()
    for path in [proof_path, HERE / "LICENSE", HERE / "PORT_PROVENANCE.md", Path(__file__),
                 receipt_path, validation_path, packet_path]:
        data = path.read_bytes()
        assert data.endswith(b"\n") and b"\x00" not in data, path
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines()), path

    print("PASS THM-M-1244 proof: vendored Gaussian LSI closure reconstructs and exact root closes")
    print(f"proof sha256: {sha256(proof_path)}")
    print("provisional proof state only; accepted state and theorem_complete remain unchanged")


if __name__ == "__main__":
    main()
