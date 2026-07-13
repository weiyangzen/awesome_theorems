#!/usr/bin/env python3
"""Fail-closed source, provenance, receipt, and handoff checks for THM-M-0989."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ITEM_ID = "S56-M-0989-PROOF"
THEOREM_ID = "THM-M-0989"
BASE_REVISION = "bb6fb28ac1c55ecb52f3f1c84e7fbb35c26b47ad"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
UPSTREAM_REVISION = "82249ccfc05c0d97b86f33fce2582f0bf4ff9c06"
UPSTREAM_TREE = "7d11c8e993bdecb4b072a9369ee6858db6728c61"
UPSTREAM_LICENSE_SHA256 = (
    "c71d239df91726fc519c6eb72d318ec65820627232b2f796219e87dcf35d0ab4"
)

SOURCE_FILES = (
    "Statement.lean",
    "ObligationTree.lean",
    "Proof.lean",
    "ProdExp.lean",
    "CharFunBound.lean",
    "LindebergArray.lean",
)

EXACT_DECLARATIONS = (
    "Stage1Instances.THM_M_0989.rowSumsAEMeasurable_proof",
    "Stage1Instances.THM_M_0989.rowCharFun_factorization",
    "Stage1Instances.THM_M_0989.rowSecondMoment_sum",
    "Stage1Instances.THM_M_0989.rowExpectation_sum",
    "Stage1Instances.THM_M_0989.rowGaussianQuadraticCoefficient",
    "Stage1Instances.THM_M_0989.truncatedSecondMoment_nonneg",
    "Stage1Instances.THM_M_0989.integrable_truncatedSecondMoment_integrand",
    "Stage1Instances.THM_M_0989.truncatedSecondMoment_le_secondMoment",
    "Stage1Instances.THM_M_0989.root_of_row_charFun_convergence",
    "Stage1Instances.THM_M_0989.ProductLimit.tendsto_row_prod_one_add_of_sum_norm_sq",
    "Stage1Instances.THM_M_0989.CharFunBound.norm_cexp_sub_taylor_two_le",
    "Stage1Instances.THM_M_0989.CharFunBound.norm_cexp_mul_I_sub_one_sub_le_sq",
    "Stage1Instances.THM_M_0989.CharFunBound.norm_cexp_mul_I_sub_taylor_two_le",
    "Stage1Instances.THM_M_0989.CharFunBound.norm_cexp_mul_I_sub_taylor_two_le_crude",
    "Stage1Instances.THM_M_0989.CharFunBound.norm_cexp_mul_I_sub_one_sub_le_half_sq",
    "Stage1Instances.THM_M_0989.rowSecondMoment_mem_unitInterval",
    "Stage1Instances.THM_M_0989.secondMoment_le_sq_add_truncated",
    "Stage1Instances.THM_M_0989.tendsto_sum_rowSecondMoment_sq",
    "Stage1Instances.THM_M_0989.rowLawCharFunConverges_proof",
    "Stage1Instances.THM_M_0989.lindebergFeller_exact",
)

DECLARATION_NEEDLES = {
    "Proof.lean": (
        "theorem rowSumsAEMeasurable_proof",
        "theorem rowCharFun_factorization",
        "theorem rowSecondMoment_sum",
        "theorem rowExpectation_sum",
        "theorem rowGaussianQuadraticCoefficient",
        "theorem truncatedSecondMoment_nonneg",
        "theorem integrable_truncatedSecondMoment_integrand",
        "theorem truncatedSecondMoment_le_secondMoment",
        "theorem root_of_row_charFun_convergence",
        "root_of_row_charFun_packages A (rowSumsAEMeasurable_proof A) hchar",
    ),
    "ProdExp.lean": ("theorem tendsto_row_prod_one_add_of_sum_norm_sq",),
    "CharFunBound.lean": (
        "lemma norm_cexp_sub_taylor_two_le",
        "lemma norm_cexp_mul_I_sub_one_sub_le_sq",
        "lemma norm_cexp_mul_I_sub_taylor_two_le",
        "lemma norm_cexp_mul_I_sub_taylor_two_le_crude",
        "lemma norm_cexp_mul_I_sub_one_sub_le_half_sq",
    ),
    "LindebergArray.lean": (
        "theorem rowSecondMoment_mem_unitInterval",
        "theorem secondMoment_le_sq_add_truncated",
        "theorem tendsto_sum_rowSecondMoment_sq",
        "theorem rowLawCharFunConverges_proof",
        "theorem lindebergFeller_exact : Statement.{u}",
        "root_of_row_charFun_convergence A (rowLawCharFunConverges_proof A)",
    ),
}

AXIOM_PROBE_COUNTS = {
    "Proof.lean": 9,
    "ProdExp.lean": 1,
    "CharFunBound.lean": 5,
    "LindebergArray.lean": 5,
}

INPUT_HASH_FIELDS = {
    "statement_sha256": "Statement.lean",
    "obligation_tree_sha256": "ObligationTree.lean",
    "proof_sha256": "Proof.lean",
    "prod_exp_sha256": "ProdExp.lean",
    "char_fun_bound_sha256": "CharFunBound.lean",
    "lindeberg_array_sha256": "LindebergArray.lean",
    "obligation_registry_sha256": "obligation-registry.json",
    "typed_graphs_sha256": "typed-graphs.json",
    "validation_specs_sha256": "validation-specs.json",
    "check_proof_py_sha256": "check_proof.py",
    "check_proof_sh_sha256": "check_proof.sh",
}


def fail(message: str) -> None:
    raise SystemExit("proof check failed: " + message)


def require(value: Any, message: str) -> None:
    if not value:
        fail(message)


def load_json(name: str) -> dict[str, Any]:
    try:
        value = json.loads((HERE / name).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        fail(f"cannot load {name}: {error}")
    require(isinstance(value, dict), f"{name} must contain a JSON object")
    return value


def sha256(name: str) -> str:
    return hashlib.sha256((HERE / name).read_bytes()).hexdigest()


def strip_lean_comments(source: str) -> str:
    """Remove nested Lean line/block comments while retaining line structure."""
    out: list[str] = []
    index = 0
    block_depth = 0
    in_string = False
    escaped = False
    while index < len(source):
        char = source[index]
        pair = source[index : index + 2]
        if block_depth:
            if pair == "/-":
                block_depth += 1
                out.extend("  ")
                index += 2
            elif pair == "-/":
                block_depth -= 1
                out.extend("  ")
                index += 2
            else:
                out.append("\n" if char == "\n" else " ")
                index += 1
            continue
        if in_string:
            out.append(char)
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
            index += 1
            continue
        if pair == "/-":
            block_depth = 1
            out.extend("  ")
            index += 2
        elif pair == "--":
            while index < len(source) and source[index] != "\n":
                out.append(" ")
                index += 1
        else:
            out.append(char)
            if char == '"':
                in_string = True
            index += 1
    require(block_depth == 0, "unterminated Lean block comment")
    require(not in_string, "unterminated Lean string literal")
    return "".join(out)


def check_sources() -> None:
    forbidden = re.compile(
        r"\b(sorry|admit|sorryAx|native_decide|implemented_by)\b"
        r"|^[ \t]*(axiom|constant|opaque|unsafe|extern)\b",
        flags=re.MULTILINE,
    )
    for name in SOURCE_FILES:
        path = HERE / name
        require(path.is_file(), f"missing source module {name}")
        code = strip_lean_comments(path.read_text(encoding="utf-8"))
        match = forbidden.search(code)
        require(match is None, f"prohibited construct in {name}: {match.group(0)!r}" if match else "")

    for name, needles in DECLARATION_NEEDLES.items():
        source = (HERE / name).read_text(encoding="utf-8")
        missing = [needle for needle in needles if needle not in source]
        require(not missing, f"missing declaration surface in {name}: {missing}")
        require(
            source.count("#print axioms") == AXIOM_PROBE_COUNTS[name],
            f"wrong axiom-probe count in {name}",
        )

    prod_exp = (HERE / "ProdExp.lean").read_text(encoding="utf-8")
    char_fun = (HERE / "CharFunBound.lean").read_text(encoding="utf-8")
    lindeberg = (HERE / "LindebergArray.lean").read_text(encoding="utf-8")
    for source, name, upstream_sha in (
        (
            prod_exp,
            "ProdExp.lean",
            "6068339f52c68388a0ce45dfd30b4801de1aab5421ef98e1fc19a81cba05851c",
        ),
        (
            char_fun,
            "CharFunBound.lean",
            "2c04f861f5c5faf0622f6c39157420f67f4e41d2f5a3b8acc8282461897143e1",
        ),
        (
            lindeberg,
            "LindebergArray.lean",
            "64020a1982986ca506b3623ff7b1f9a2bad2a57edb764ef0689ddda0ab43da3c",
        ),
    ):
        require(UPSTREAM_REVISION in source, f"{name} lacks immutable upstream revision")
        require(upstream_sha in source, f"{name} lacks immutable upstream source hash")


def recompute_registry_denominator(registry: dict[str, Any]) -> str:
    fields = (
        "obligation_id",
        "statement_fingerprint",
        "kind",
        "root_relevant",
        "machine_eligibility",
        "human_source_eligibility",
        "readable_eligibility",
        "risk_class",
        "exclusion_reason",
        "terminal_proof_body_id",
    )
    obligations = registry.get("obligations")
    require(isinstance(obligations, list), "registry obligations are missing")
    try:
        canonical = [{field: row[field] for field in fields} for row in obligations]
    except (KeyError, TypeError) as error:
        fail(f"malformed obligation registry: {error}")
    payload = json.dumps(
        canonical, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def check_replay_script() -> None:
    replay = (HERE / "check_proof.sh").read_text(encoding="utf-8")
    surfaces = (
        "lake env which lean",
        "lake env printenv LEAN_PATH",
        "--trust=0",
        "Statement.olean",
        "ObligationTree.olean",
        "Proof.olean",
        "ProdExp.olean",
        "CharFunBound.olean",
        "LindebergArray.olean",
        "20 declarations have the allowed axiom set",
    )
    missing = [surface for surface in surfaces if surface not in replay]
    require(not missing, f"replay script is incomplete: {missing}")
    for declaration in EXACT_DECLARATIONS:
        require(declaration in replay, f"replay omits axiom check for {declaration}")
    forbidden_commands = re.compile(
        r"\blake\s+(update|build)\b|\bgit\s+(clone|fetch)\b"
    )
    require(forbidden_commands.search(replay) is None, "replay mutates dependency state")


def check_receipt(receipt: dict[str, Any], registry: dict[str, Any]) -> None:
    require(receipt.get("item_id") == ITEM_ID, "wrong receipt item")
    require(receipt.get("theorem_id") == THEOREM_ID, "wrong receipt theorem")
    require(receipt.get("base_revision") == BASE_REVISION, "wrong receipt base revision")
    require(
        receipt.get("support_state") == "provisional_worker_selftest",
        "receipt is not provisional worker evidence",
    )
    require(receipt.get("proposed_state") == "[_]", "wrong proposed worker state")
    require(receipt.get("accepted") is False, "worker receipt claims acceptance")
    require(
        receipt.get("exact_declarations") == list(EXACT_DECLARATIONS),
        "exact declaration inventory is stale",
    )

    required_machine = registry["frozen_denominators"]["required_machine"]
    expected_kernel_closed = [
        obligation for obligation in required_machine if obligation != "M0989-S-FOUNDATION"
    ]
    require(
        receipt.get("provisionally_kernel_closed_obligation_ids")
        == expected_kernel_closed,
        "kernel-closed obligation inventory disagrees with frozen denominator",
    )
    require(
        receipt.get("accepted_closed_obligation_ids") == [],
        "worker receipt claims accepted obligations",
    )
    require(
        receipt.get("open_assurance_obligation_ids")
        == ["M0989-S-FOUNDATION", "M0989-X-SOURCE", "M0989-X-PROVENANCE"],
        "open assurance inventory is stale",
    )

    inputs = receipt.get("inputs")
    require(isinstance(inputs, dict), "receipt inputs are missing")
    for field, name in INPUT_HASH_FIELDS.items():
        require(inputs.get(field) == sha256(name), f"stale {field}")
    denominator = recompute_registry_denominator(registry)
    require(
        inputs.get("registry_denominator_sha256")
        == registry.get("denominator_sha256")
        == denominator,
        "registry denominator hash disagrees",
    )

    proof_body = receipt.get("proof_body")
    require(isinstance(proof_body, dict), "proof-body provenance is missing")
    require(
        proof_body.get("classification") == "repo_local_adapted_exact_proof",
        "wrong proof-body classification",
    )
    require(
        proof_body.get("source") == "Stage1_Instances/THM-M-0989/LindebergArray.lean",
        "wrong terminal proof-body source",
    )
    require(
        proof_body.get("terminal_root_declaration")
        == "Stage1Instances.THM_M_0989.lindebergFeller_exact",
        "wrong terminal root declaration",
    )
    upstream_sources = proof_body.get("upstream_sources")
    require(isinstance(upstream_sources, list), "upstream source inventory is missing")
    upstream_by_path = {
        row.get("path"): row for row in upstream_sources if isinstance(row, dict)
    }
    expected_upstream = {
        "Clt/ProdExp.lean": "6068339f52c68388a0ce45dfd30b4801de1aab5421ef98e1fc19a81cba05851c",
        "Clt/CharFunBound.lean": "2c04f861f5c5faf0622f6c39157420f67f4e41d2f5a3b8acc8282461897143e1",
        "Clt/Lindeberg.lean": "64020a1982986ca506b3623ff7b1f9a2bad2a57edb764ef0689ddda0ab43da3c",
    }
    require(set(upstream_by_path) == set(expected_upstream), "wrong upstream path inventory")
    for path, expected_sha in expected_upstream.items():
        row = upstream_by_path[path]
        require(row.get("repository") == "https://github.com/patrickrd/CLT-lindeberg", f"wrong repository for {path}")
        require(row.get("revision") == UPSTREAM_REVISION, f"wrong revision for {path}")
        require(row.get("tree") == UPSTREAM_TREE, f"wrong tree for {path}")
        require(row.get("source_sha256") == expected_sha, f"wrong source hash for {path}")
        require(row.get("license") == "Apache-2.0", f"wrong license for {path}")
        require(
            row.get("license_sha256") == UPSTREAM_LICENSE_SHA256,
            f"wrong license hash for {path}",
        )
        require(
            row.get("relationship") == "derived_repo_local_adaptation",
            f"wrong adaptation classification for {path}",
        )

    environment = receipt.get("environment")
    require(isinstance(environment, dict), "environment record is missing")
    require(environment.get("lean_commit") == LEAN_COMMIT, "wrong Lean revision")
    require(environment.get("mathlib_revision") == MATHLIB_REVISION, "wrong mathlib revision")
    require(environment.get("lake_mutated") is False, "receipt claims Lake mutation")

    result = receipt.get("result")
    require(isinstance(result, dict), "receipt result is missing")
    require(result.get("exit_code") == 0, "Lean replay is not recorded as passing")
    require(
        result.get("axioms") == ["propext", "Classical.choice", "Quot.sound"],
        "wrong recorded axiom set",
    )
    require(result.get("axiom_probe_count") == 20, "wrong axiom-probe count")
    require(result.get("placeholder_scan") == "pass", "placeholder scan did not pass")
    require(result.get("root_kernel_closed") is True, "kernel root closure is absent")
    require(result.get("accepted_root_closed") is False, "worker claims accepted root")
    require(
        result.get("proposed_machine_debt_after_acceptance") == "M0-L",
        "wrong proposed machine classification",
    )
    require(result.get("theorem_complete") is False, "worker claims theorem completion")


def changed_paths() -> set[str]:
    output = subprocess.check_output(
        ["git", "status", "--short", "--untracked-files=all"],
        cwd=ROOT,
        text=True,
    )
    owned_prefix = "Stage1_Instances/THM-M-0989/"
    return {
        line[3:]
        for line in output.splitlines()
        if line[3:] == ".stage1-worker-selftest.json"
        or line[3:].startswith(owned_prefix)
    }


def check_selftest(receipt: dict[str, Any]) -> None:
    packet_path = ROOT / ".stage1-worker-selftest.json"
    require(packet_path.is_file(), "closed proof phase lacks worker self-test manifest")
    try:
        packet = json.loads(packet_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        fail(f"invalid worker self-test JSON: {error}")
    expected_keys = {
        "item_id",
        "changed_paths",
        "commands",
        "output_summary",
        "base_revision",
        "known_failures",
        "state",
    }
    require(set(packet) == expected_keys, "wrong worker self-test schema")
    require(packet["item_id"] == ITEM_ID, "wrong worker self-test item")
    require(packet["state"] == "[_]", "wrong worker self-test state")
    require(packet["base_revision"] == BASE_REVISION, "wrong worker self-test base")
    require(packet["changed_paths"] == receipt.get("changed_paths"), "receipt/packet paths differ")
    require(packet["known_failures"] == receipt.get("known_failures"), "receipt/packet failures differ")
    require(set(packet["changed_paths"]) == changed_paths(), "changed-path inventory is stale")
    command_text = json.dumps(packet["commands"], sort_keys=True)
    for command in (
        "check_stage1_standard.py",
        "stage1_target.py",
        "check_obligation_tree.py",
        "check_proof.py",
        "check_proof.sh",
    ):
        require(command in command_text, f"worker packet omits command {command}")
    command_argv = [row.get("argv") for row in packet["commands"] if isinstance(row, dict)]
    require(
        ["git", "diff", "--check", "--", "Stage1_Instances/THM-M-0989",
          ".stage1-worker-selftest.json"] in command_argv,
        "worker packet omits scoped git diff --check",
    )
    failures = " ".join(receipt.get("known_failures", []))
    for boundary in ("foundation", "provenance", "validation", "release", "master"):
        require(boundary in failures.lower(), f"known failures omit {boundary} boundary")


def check_environment() -> None:
    require(
        subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
        == BASE_REVISION,
        "worker HEAD differs from recorded base revision",
    )
    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    require(mathlib.is_dir(), "pinned mathlib artifacts are missing")
    require(
        subprocess.check_output(
            ["git", "-C", str(mathlib), "rev-parse", "HEAD"], text=True
        ).strip()
        == MATHLIB_REVISION,
        "wrong pinned mathlib revision",
    )
    require(
        subprocess.check_output(
            ["git", "-C", str(mathlib), "status", "--short"], text=True
        )
        == "",
        "pinned mathlib source is dirty",
    )


def main() -> None:
    check_sources()
    check_replay_script()
    registry = load_json("obligation-registry.json")
    require(registry.get("theorem_id") == THEOREM_ID, "wrong obligation registry")

    receipt_path = HERE / "proof-receipt.json"
    blocker_path = HERE / "proof-blocker.json"
    require(receipt_path.exists() != blocker_path.exists(), "need exactly one proof receipt or blocker")
    if blocker_path.exists():
        blocker = load_json("proof-blocker.json")
        require(blocker.get("outcome") == "blocked", "invalid blocker outcome")
        require(blocker.get("root_closed") is False, "blocker claims root closure")
        require(
            "theorem lindebergFeller_exact : Statement.{u}"
            not in (HERE / "LindebergArray.lean").read_text(encoding="utf-8"),
            "stale blocker coexists with an exact root body",
        )
        require(
            not (ROOT / ".stage1-worker-selftest.json").exists(),
            "blocked proof phase has a worker self-test manifest",
        )
        fail("proof remains blocked")

    receipt = load_json("proof-receipt.json")
    check_receipt(receipt, registry)
    check_selftest(receipt)
    check_environment()
    print(
        "PASS THM-M-0989 proof phase: exact frozen root has a provisional "
        "repo-local adapted body; theorem completion remains false"
    )
    for name in SOURCE_FILES:
        print(f"{name} sha256: {sha256(name)}")


if __name__ == "__main__":
    main()
