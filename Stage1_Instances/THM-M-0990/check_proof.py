#!/usr/bin/env python3
"""Fail-closed source, receipt, and worker-handoff checks for THM-M-0990."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ITEM_ID = "S56-M-0990-PROOF"
THEOREM_ID = "THM-M-0990"
BASE_REVISION = "64ac616628d97140f9ca64eff0298e51d7f4e9ff"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
UPSTREAM_REVISION = "82249ccfc05c0d97b86f33fce2582f0bf4ff9c06"
UPSTREAM_TREE = "7d11c8e993bdecb4b072a9369ee6858db6728c61"
UPSTREAM_LICENSE_SHA256 = (
    "c71d239df91726fc519c6eb72d318ec65820627232b2f796219e87dcf35d0ab4"
)

SOURCE_FILES = (
    "Statement.lean",
    "ObligationTree.lean",
    "Normalization.lean",
    "ProductLimit.lean",
    "GeneralizedLindeberg.lean",
    "Proof.lean",
)

EXACT_DECLARATIONS = (
    "Stage1Instances.THM_M_0990.centered_measurable",
    "Stage1Instances.THM_M_0990.centered_memLp",
    "Stage1Instances.THM_M_0990.centered_integral_eq_zero",
    "Stage1Instances.THM_M_0990.normalizedIncrement_memLp",
    "Stage1Instances.THM_M_0990.normalizedIncrement_integral_eq_zero",
    "Stage1Instances.THM_M_0990.normalizedIncrement_independent",
    "Stage1Instances.THM_M_0990.normalizedIncrement_variance_sum",
    "Stage1Instances.THM_M_0990.normalizedIncrement_sum",
    "Stage1Instances.THM_M_0990.ProductLimit.tendsto_row_prod_one_add_of_sum_norm_sq",
    "Stage1Instances.THM_M_0990.eventualRowSumsAEMeasurable_proof",
    "Stage1Instances.THM_M_0990.eventualRowCharFun_factorization",
    "Stage1Instances.THM_M_0990.eventually_rowSecondMoment_sum",
    "Stage1Instances.THM_M_0990.eventually_rowGaussianQuadraticCoefficient",
    "Stage1Instances.THM_M_0990.eventual_root_of_row_charFun_packages",
    "Stage1Instances.THM_M_0990.rowSecondMoment_mem_unitInterval",
    "Stage1Instances.THM_M_0990.secondMoment_le_sq_add_truncated",
    "Stage1Instances.THM_M_0990.tendsto_sum_rowSecondMoment_sq",
    "Stage1Instances.THM_M_0990.eventualRowLawCharFunConverges_proof",
    "Stage1Instances.THM_M_0990.eventualLindebergFeller_exact",
    "Stage1Instances.THM_M_0990.sq_le_rpow_mul_final",
    "Stage1Instances.THM_M_0990.truncatedSecondMoment_scaled_le_final",
    "Stage1Instances.THM_M_0990.sum_truncatedSecondMoment_normalized_le_final",
    "Stage1Instances.THM_M_0990.normalizedRowSum_measurable_final",
    "Stage1Instances.THM_M_0990.lyapunovCentralLimit_exact",
)

INPUT_HASH_FIELDS = {
    "statement_sha256": "Statement.lean",
    "obligation_tree_sha256": "ObligationTree.lean",
    "normalization_sha256": "Normalization.lean",
    "product_limit_sha256": "ProductLimit.lean",
    "generalized_lindeberg_sha256": "GeneralizedLindeberg.lean",
    "proof_sha256": "Proof.lean",
    "obligation_registry_sha256": "obligation-registry.json",
    "typed_graphs_sha256": "typed-graphs.json",
    "validation_specs_sha256": "validation-specs.json",
    "check_proof_py_sha256": "check_proof.py",
    "check_proof_sh_sha256": "check_proof.sh",
}

DEPENDENCY_HASH_FIELDS = {
    "statement_sha256": "Statement.lean",
    "obligation_tree_sha256": "ObligationTree.lean",
    "proof_sha256": "Proof.lean",
    "char_fun_bound_sha256": "CharFunBound.lean",
}


def fail(message: str) -> None:
    raise SystemExit("proof check failed: " + message)


def require(value: Any, message: str) -> None:
    if not value:
        fail(message)


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        fail(f"cannot load {path.name}: {error}")
    require(isinstance(value, dict), f"{path.name} must contain a JSON object")
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def strip_lean_comments(source: str) -> str:
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
    dependency = ROOT / "Stage1_Instances/THM-M-0989"
    paths = [HERE / name for name in SOURCE_FILES]
    paths += [dependency / name for name in DEPENDENCY_HASH_FIELDS.values()]
    for path in paths:
        require(path.is_file(), f"missing Lean source {path.relative_to(ROOT)}")
        match = forbidden.search(strip_lean_comments(path.read_text(encoding="utf-8")))
        require(match is None, f"prohibited construct in {path.relative_to(ROOT)}")

    public_count = 0
    probe_count = 0
    for name in ("Normalization.lean", "ProductLimit.lean", "GeneralizedLindeberg.lean", "Proof.lean"):
        source = (HERE / name).read_text(encoding="utf-8")
        public_count += len(re.findall(r"(?m)^(?:theorem|lemma)\s+", source))
        probe_count += source.count("#print axioms")
    require(public_count == probe_count == len(EXACT_DECLARATIONS) == 24,
            "public declaration/axiom-probe inventory mismatch")
    replay = (HERE / "check_proof.sh").read_text(encoding="utf-8")
    for declaration in EXACT_DECLARATIONS:
        require(declaration in replay, f"replay omits {declaration}")
    require("--trust=0" in replay and "24 target declarations" in replay,
            "replay does not enforce the declared proof surface")
    require(re.search(r"\blake\s+(update|build)\b|\bgit\s+(clone|fetch)\b", replay) is None,
            "replay mutates dependency state")

    product = (HERE / "ProductLimit.lean").read_text(encoding="utf-8")
    generalized = (HERE / "GeneralizedLindeberg.lean").read_text(encoding="utf-8")
    for source, expected_sha in (
        (product, "6068339f52c68388a0ce45dfd30b4801de1aab5421ef98e1fc19a81cba05851c"),
        (generalized, "64020a1982986ca506b3623ff7b1f9a2bad2a57edb764ef0689ddda0ab43da3c"),
    ):
        require(UPSTREAM_REVISION in source and expected_sha in source,
                "proof source lacks immutable upstream provenance")


def recompute_registry_denominator(registry: dict[str, Any]) -> str:
    fields = (
        "obligation_id", "statement_fingerprint", "kind", "root_relevant",
        "machine_eligibility", "human_source_eligibility", "readable_eligibility",
        "risk_class", "exclusion_reason", "terminal_proof_body_id",
    )
    obligations = registry.get("obligations")
    require(isinstance(obligations, list), "registry obligations are missing")
    canonical = [{field: row[field] for field in fields} for row in obligations]
    payload = json.dumps(canonical, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(payload).hexdigest()


def changed_paths() -> set[str]:
    output = subprocess.check_output(
        ["git", "status", "--short", "--untracked-files=all"], cwd=ROOT, text=True
    )
    prefix = f"Stage1_Instances/{THEOREM_ID}/"
    return {
        line[3:] for line in output.splitlines()
        if line[3:] == ".stage1-worker-selftest.json" or line[3:].startswith(prefix)
    }


def main() -> None:
    check_sources()
    registry = load_json(HERE / "obligation-registry.json")
    receipt = load_json(HERE / "proof-receipt.json")
    blocker = load_json(HERE / "proof-blocker.json")
    selftest = load_json(ROOT / ".stage1-worker-selftest.json")

    require(registry.get("theorem_id") == THEOREM_ID, "wrong obligation registry")
    denominator = recompute_registry_denominator(registry)
    require(registry.get("denominator_sha256") == denominator,
            "frozen registry denominator disagrees")
    require(receipt.get("item_id") == ITEM_ID and receipt.get("theorem_id") == THEOREM_ID,
            "wrong receipt identity")
    require(receipt.get("base_revision") == BASE_REVISION, "wrong receipt base")
    require(receipt.get("support_state") == "provisional_worker_selftest",
            "receipt is not provisional")
    require(receipt.get("proposed_state") == "[_]" and receipt.get("accepted") is False,
            "worker receipt claims acceptance")
    require(receipt.get("canonical_target") == "Stage1Instances.THM_M_0990.StatementShape",
            "wrong canonical target")
    require(receipt.get("exact_declarations") == list(EXACT_DECLARATIONS),
            "exact declaration inventory is stale")
    require(blocker.get("item_id") == ITEM_ID and blocker.get("theorem_id") == THEOREM_ID,
            "wrong resolved-blocker identity")
    require(blocker.get("verdict") == "resolved_by_provisional_proof_receipt" and
            blocker.get("blocker") is None and blocker.get("root_closed") is True,
            "stale proof blocker remains")
    require(blocker.get("accepted_root_closed") is False and
            blocker.get("theorem_complete") is False,
            "resolved blocker overclaims acceptance")

    required_machine = registry["frozen_denominators"]["required_machine"]
    expected_closed = [x for x in required_machine if x != "M0990-S-FOUNDATION"]
    require(receipt.get("provisionally_kernel_closed_obligation_ids") == expected_closed,
            "provisional closure disagrees with frozen denominator")
    require(receipt.get("accepted_closed_obligation_ids") == [],
            "worker receipt claims accepted obligations")
    require(receipt.get("open_assurance_obligation_ids") ==
            ["M0990-S-FOUNDATION", "M0990-X-SOURCE", "M0990-X-TCB"],
            "open assurance inventory is stale")

    inputs = receipt.get("inputs", {})
    for field, name in INPUT_HASH_FIELDS.items():
        require(inputs.get(field) == sha256(HERE / name), f"stale {field}")
    require(inputs.get("registry_denominator_sha256") == denominator,
            "receipt denominator disagrees")
    dependency = ROOT / "Stage1_Instances/THM-M-0989"
    dependency_inputs = inputs.get("thm_m_0989_dependency", {})
    for field, name in DEPENDENCY_HASH_FIELDS.items():
        require(dependency_inputs.get(field) == sha256(dependency / name),
                f"stale dependency {field}")

    proof_body = receipt.get("proof_body", {})
    require(proof_body.get("classification") == "repo_local_adapted_exact_proof",
            "wrong proof classification")
    require(proof_body.get("terminal_root_declaration") ==
            "Stage1Instances.THM_M_0990.lyapunovCentralLimit_exact",
            "wrong terminal root")
    upstream = proof_body.get("upstream_sources", [])
    require(len(upstream) == 3, "incomplete upstream inventory")
    for row in upstream:
        require(row.get("revision") == UPSTREAM_REVISION and row.get("tree") == UPSTREAM_TREE,
                "wrong upstream revision")
        require(row.get("license") == "Apache-2.0" and
                row.get("license_sha256") == UPSTREAM_LICENSE_SHA256,
                "wrong upstream license evidence")

    environment = receipt.get("environment", {})
    require(environment.get("lean_commit") == LEAN_COMMIT,
            "wrong Lean revision")
    require(environment.get("mathlib_revision") == MATHLIB_REVISION,
            "wrong mathlib revision")
    require(environment.get("lake_mutated") is False,
            "receipt claims Lake mutation")
    result = receipt.get("result", {})
    require(result.get("exit_code") == 0 and result.get("root_kernel_closed") is True,
            "root kernel closure is absent")
    require(result.get("accepted_root_closed") is False and
            result.get("theorem_complete") is False,
            "worker receipt overclaims completion")
    require(result.get("axiom_probe_count") == 24 and result.get("axioms") ==
            ["propext", "Classical.choice", "Quot.sound"],
            "wrong axiom evidence")

    require(set(selftest) == {"item_id", "changed_paths", "commands", "output_summary",
                              "base_revision", "known_failures", "state"},
            "wrong worker self-test schema")
    require(selftest.get("item_id") == ITEM_ID and selftest.get("state") == "[_]",
            "wrong self-test identity/state")
    require(selftest.get("base_revision") == BASE_REVISION,
            "wrong self-test base")
    require(selftest.get("changed_paths") == receipt.get("changed_paths") and
            set(selftest["changed_paths"]) == changed_paths(),
            "changed-path inventory is stale")
    require(selftest.get("known_failures") == receipt.get("known_failures"),
            "receipt/self-test failures differ")

    require(subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
            == BASE_REVISION, "worker HEAD differs from receipt")
    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    require(subprocess.check_output(["git", "-C", str(mathlib), "rev-parse", "HEAD"],
                                    text=True).strip() == MATHLIB_REVISION,
            "wrong pinned mathlib revision")
    require(subprocess.check_output(["git", "-C", str(mathlib), "rev-parse", "HEAD^{tree}"],
                                    text=True).strip() == MATHLIB_TREE,
            "wrong pinned mathlib tree")
    require(subprocess.check_output(["git", "-C", str(mathlib), "status", "--short"],
                                    text=True) == "", "pinned mathlib is dirty")

    print(
        "PASS THM-M-0990 proof phase: exact frozen root has a provisional "
        "placeholder-free repo-local body; theorem completion remains false"
    )


if __name__ == "__main__":
    main()
