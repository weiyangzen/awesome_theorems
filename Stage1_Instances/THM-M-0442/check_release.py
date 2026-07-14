#!/usr/bin/env python3
"""Fail-closed release reconciliation for S56-M-0442-RELEASE."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0442"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
ITEM = "S56-M-0442-RELEASE"
THEOREM = "THM-M-0442"
BASE_REVISION = "c470319c4a07f669317557ea705f6546605ac4da"
BASE_TREE = "680bb215853ecfbfa26fe069d1282188ed3944aa"
VALIDATION_BASE_REVISION = "a1a7e939e58f103f5ff5d23af51437fa8658aa04"
VALIDATION_BASE_TREE = "d881fd9641fa3e5f3ebe5082b35672981e90adcf"
VALIDATION_RECEIPT_SHA256 = (
    "88e6484d4db1d7a778a7552d3b34fd063c4f84853584615eba596ec597903b2c"
)
STATEMENT_EXPRESSION_SHA256 = (
    "b65a3a73cac19c57286b3cba584fc84ebda329b70006b409f12ec6e761721658"
)
FIRST_THEOREM_GAP = (
    "M0442-M-MODULI: first identified missing deep package; no kernel-checked "
    "compactified modular-curve/moduli-map body is present in the pinned closure"
)
FROZEN_LEAF_CUT = [
    "M0442-G-FIN",
    "M0442-G-RANK",
    "M0442-C-PRIME",
    "M0442-C-POWER",
    "M0442-B-TWO",
    "M0442-B-INDEX",
    "M0442-M-MODULI",
    "M0442-M-CUSPS",
    "M0442-M-RATIONAL",
    "M0442-A-REDUCTION",
    "M0442-A-DESCENT",
    "M0442-SOURCE",
    "M0442-TRUST",
]
INVENTORY_IDS = [
    "M0442-ROOT",
    "M0442-S",
    "M0442-G",
    "M0442-G-FIN",
    "M0442-G-RANK",
    "M0442-C",
    "M0442-C-PRIME",
    "M0442-C-POWER",
    "M0442-B",
    "M0442-B-TWO",
    "M0442-B-INDEX",
    "M0442-M",
    "M0442-M-MODULI",
    "M0442-M-CUSPS",
    "M0442-M-RATIONAL",
    "M0442-A",
    "M0442-A-REDUCTION",
    "M0442-A-DESCENT",
    "M0442-T",
    "M0442-SOURCE",
    "M0442-TRUST",
]
NONCLOSING_DECLARATIONS = [
    "Stage1Instances.THMM0442.ObligationTree.engine_compose",
    "Stage1Instances.THMM0442.Proof.cyclic_order_le_sixteen",
    "Stage1Instances.THMM0442.Proof.bicyclic_index_four_mul_le_sixteen",
    "Stage1Instances.THMM0442.Proof.torsion_ncard_eq_of_hasCyclicTorsionOrder",
    "Stage1Instances.THMM0442.Proof.torsion_ncard_eq_of_hasBicyclicTorsionIndex",
    "Stage1Instances.THMM0442.Proof.mazurRationalTorsionTarget_implies_torsionBoundAtMostSixteen",
    "Stage1Instances.THMM0442.Validation.cyclic_order_le_sixteen",
    "Stage1Instances.THMM0442.Validation.bicyclic_index_four_mul_le_sixteen",
    "Stage1Instances.THMM0442.Validation.allowed_shape_cardinality_bound",
]
UPSTREAM_INPUTS = {
    "Statement.lean": "8779e87e3bc1c18654f30bb6380798da00baeaf18e8df6a588c6519ae8655ce4",
    "ObligationTree.lean": "6bf3713e057593c9690ea877901e3418d1c1b3f4e41c8f8acd43d01198e7b38e",
    "Proof.lean": "6c0c7737f36b2e0d692828ed596c4d6286d258efcd122835a84eaf8cf9b9630b",
    "Validation.lean": "fbe61d8b76cc9a6c79c3cdf21a74d67603267487b93e7d4d0deec0afab2ac01d",
    "instance.json": "268551416f194ac4e5484627f8f5e63c5431b26142e98b15447914305ae3e983",
    "task-dag.json": "bbc9d056103fdef6902f3cad554d2cc256c48ac3f1a53f421ec3f834fa87f462",
    "statement.json": "3cae15fe8c83c2034eb8149487e4322730d7febfb618fec68cebd7d8f36d807c",
    "anchor-audit.json": "cf6d14efe101761821962b52d54e69c01a5c32557c3502ed1f1112217370ecf0",
    "obligation-registry.json": "1df31d91ca04657c2c90d2effbd80daad2988a1d0b3d64f4a6e1ed8ebd2a15c9",
    "typed-graphs.json": "6248c8a590c5bc358ea0cf0de179d3e3c9db725fa30fb37d05c4be3b9c6f594d",
    "proof-blocker.json": "82ab210fc5c79cb0d29b2d297023daa34f5fac4b5b43818d4002917025b94dfd",
    "proof-validation.md": "82290a891582fc5882021b7d09a83c831c5a8d615062fb13b3e8066c6b41047f",
    "validation-spec.json": "f6af70d4c75edae7d60f11d27803b579bf117e97f21b755e290980c8c8d65518",
    "validation-receipt.json": VALIDATION_RECEIPT_SHA256,
    "check_validation.py": "dd45c522f15d1ab15d494faaf2a4a2a697b158be53e0fe7df6e7528110f79952",
    "source-statement-crosswalk.md": "3ab6e07b49c8f10bf2f4b4aaeea215eb677b241f9a4d94699f03fcbc4fee4b00",
}
AUTHORITY_INPUTS = {
    "Docs/Stage1_Targets_rev-5.6.json": (
        "02eec284de534dd78e1cf75f82a477ff477567dd682b7445cb7587abd137ab2c"
    ),
    "Docs/Stage1_Execution_DAG_rev-5.6.json": (
        "25fa590d23f9b1a3c2c7ab4e0b126394e861c66610244166e3464c208804f22d"
    ),
    "Docs/Stage1_Blueprint_rev-5.6.md": (
        "81085736240d15f7aa6afeff867ef5a49465bad03bc91a93c6e89c485a81cfd0"
    ),
    "skills/execute-stage1-rev56/SKILL.md": (
        "26d47a66c6535feabb8bbf1051fd55d76a53fe761f4b3d953f86b97ec86152b8"
    ),
}
TOOL_INPUTS = {
    "lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/check_release.py",
    f"Stage1_Instances/{THEOREM}/release-decision.json",
    f"Stage1_Instances/{THEOREM}/release-phase.md",
    f"Stage1_Instances/{THEOREM}/release-receipt.json",
    f"Stage1_Instances/{THEOREM}/release-spec.json",
}


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
    timeout: int = 360,
    expected_exit: int = 0,
) -> subprocess.CompletedProcess[str]:
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
    assert result.returncode == expected_exit, (
        f"unexpected exit {result.returncode} (wanted {expected_exit}): {argv!r}\n"
        f"{result.stdout}"
    )
    return result


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["git", *args], cwd=cwd).stdout.rstrip()


def replay_current_narrow_validation() -> str:
    """Re-run substantive validation after adapting only stale snapshot checks."""

    assert run(
        ["git", "merge-base", "--is-ancestor", VALIDATION_BASE_REVISION, BASE_REVISION]
    ).returncode == 0
    source = (HERE / "check_validation.py").read_text(encoding="utf-8")
    replacements = [
        (
            'ROOT = Path(__file__).resolve().parents[2]',
            f'ROOT = Path("{ROOT}")',
        ),
        (
            f'BASE_REVISION = "{VALIDATION_BASE_REVISION}"',
            f'BASE_REVISION = "{BASE_REVISION}"',
        ),
        (
            f'BASE_TREE = "{VALIDATION_BASE_TREE}"',
            f'BASE_TREE = "{BASE_TREE}"',
        ),
        (
            '"state": "[ ]",\n    "depends_on": ["S56-M-0442-PROOF"],',
            '"state": "[_]",\n    "depends_on": ["S56-M-0442-PROOF"],',
        ),
        (
            '"attempts": 0,\n    "children": [],\n}\npredecessor = next',
            '"attempts": 1,\n    "children": [],\n}\npredecessor = next',
        ),
        (
            'selftest_path = ROOT / ".stage1-worker-selftest.json"',
            'selftest_path = ROOT / ".stage1-validation-replay-selftest-absent.json"',
        ),
    ]
    for old, new in replacements:
        assert source.count(old) == 1, old
        source = source.replace(old, new, 1)

    expected = (
        "PASS THM-M-0442 network-isolated trust-zero replay of the frozen Lean target\n"
        "PASS conditional composition, five partial declarations, and three differential "
        "declarations use only the selected classical axiom subset\n"
        "PASS frozen hashes, proof blocker, placeholder scan, and pinned mathlib provenance; "
        "zero frozen obligations closed\n"
        "OPEN M0442-M-MODULI and twelve other root-cut obligations; hermetic release and "
        "distinct-runner verification fail closed\n"
    )
    with tempfile.TemporaryDirectory(prefix="stage1-m0442-release-", dir="/var/tmp") as directory:
        checker = Path(directory) / "check_validation.py"
        checker.write_text(source, encoding="utf-8")
        result = run(
            [
                "/usr/bin/bwrap",
                "--ro-bind", "/", "/",
                "--dev", "/dev",
                "--proc", "/proc",
                "--tmpfs", "/tmp",
                "--unshare-net",
                "--die-with-parent",
                "--clearenv",
                "--setenv", "HOME", "/tmp",
                "--setenv", "PATH", "/usr/bin:/bin",
                "--setenv", "LANG", "C.UTF-8",
                "--setenv", "LC_ALL", "C.UTF-8",
                "--setenv", "TZ", "UTC",
                "--setenv", "LEAN_NUM_THREADS", "1",
                "--setenv", "STAGE1_SKIP_RECEIPT_CHECK", "1",
                "/usr/bin/python3", "-I", "-B", str(checker),
            ],
        )
    assert result.stdout == expected, result.stdout
    assert hashlib.sha256(result.stdout.encode("utf-8")).hexdigest() == (
        "4479f3eb853e1130ba0c86af35613cbe6651c0ff55364f1f14d4cf99ed791e1d"
    )
    assert len(result.stdout.encode("utf-8")) == 451
    return result.stdout


def main() -> None:
    if not __debug__:
        raise RuntimeError("release validation requires Python assertions")

    decision = load(HERE / "release-decision.json")
    spec = load(HERE / "release-spec.json")
    receipt_path = HERE / "release-receipt.json"
    receipt = load(receipt_path) if receipt_path.exists() else None
    validation = load(HERE / "validation-receipt.json")
    instance = load(HERE / "instance.json")
    local_tasks = load(HERE / "task-dag.json")
    statement = load(HERE / "statement.json")
    anchor = load(HERE / "anchor-audit.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    blocker = load(HERE / "proof-blocker.json")
    targets = load(ROOT / "Docs" / "Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    for name, expected in UPSTREAM_INPUTS.items():
        assert sha256(HERE / name) == expected, f"upstream input drifted: {name}"
    for name, expected in AUTHORITY_INPUTS.items():
        assert sha256(ROOT / name) == expected, f"authority input drifted: {name}"
    for name, expected in TOOL_INPUTS.items():
        assert sha256(LEAN_ROOT / name) == expected, f"tool input drifted: {name}"

    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 88
    assert target["baseline"] == "L0" and target["rework_required"] is True
    assert target["lifecycle_mode"] == "planned"
    assert target["legacy_artifacts_accepted"] is False
    assert target["theorem_complete"] is False

    release_item = next(row for row in execution["items"] if row["id"] == ITEM)
    validation_item = next(
        row for row in execution["items"] if row["id"] == "S56-M-0442-VALIDATION"
    )
    assert release_item == {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 88,
        "phase": "release",
        "layer": 6,
        "state": "[ ]",
        "depends_on": ["S56-M-0442-VALIDATION"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Reconcile evidence and decide the exact theorem-completion verdict.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }
    assert validation_item["state"] == "[_]" and validation_item["attempts"] == 1

    assert spec["schema_version"] == "stage1-validation-spec/1.0"
    assert spec["item_id"] == decision["item_id"] == ITEM
    assert spec["theorem_id"] == decision["theorem_id"] == THEOREM
    assert spec["cwd"] == "." and spec["timeout_seconds"] == 360
    assert spec["argv"] == [
        "python3", "-B", f"Stage1_Instances/{THEOREM}/check_release.py"
    ]
    assert spec["network_policy"] == "nested_validation_denied_release_orchestration_not_isolated"
    assert spec["expected_exit"] == 0
    assert spec["covered_obligation_ids"] == INVENTORY_IDS
    assert spec["covered_declarations"] == [
        "Stage1Instances.THMM0442.MazurRationalTorsionTarget",
        "Stage1Instances.THMM0442.mazurRationalTorsionTarget_iff_historicalCandidateShape",
        *NONCLOSING_DECLARATIONS,
    ]

    assert decision["base_revision"] == BASE_REVISION
    assert decision["base_tree"] == BASE_TREE
    assert decision["decision_support"] == "provisional_worker_selftest"
    assert decision["proposed_state"] == "[_]" and decision["release_grade"] is False
    assert decision["canonical_target_expression_sha256"] == STATEMENT_EXPRESSION_SHA256
    assert decision["inputs"] == UPSTREAM_INPUTS
    assert decision["authority_inputs"] == AUTHORITY_INPUTS

    dependency = decision["dependency"]
    assert dependency["item_id"] == validation["item_id"]
    assert dependency["receipt_id"] == validation["receipt_id"]
    assert dependency["receipt_sha256"] == VALIDATION_RECEIPT_SHA256
    assert dependency["scheduler_projection"] == "[_]"
    assert dependency["receipt_support_state"] == validation["support_state"]
    assert dependency["receipt_verdict"] == validation["verdict"] == "blocked"
    assert dependency["receipt_release_grade"] is validation["release_grade"] is False
    assert dependency["receipt_accepted"] is validation["accepted"] is False
    assert dependency["master_accepted"] is False

    assert instance["lifecycle_mode"] == "planned"
    assert instance["root_vector"] == {
        "human": "H1", "machine": "M3", "readability": "R3"
    }
    assert instance["theorem_complete"] is False
    assert local_tasks["frozen"] is False
    local_states = {row["id"]: row["state"] for row in local_tasks["nodes"]}
    assert local_states["S56-M-0442-INTAKE"] == "provisional_self_tested"
    assert all(
        local_states[f"S56-M-0442-{phase}"] == "open"
        for phase in (
            "STATEMENT", "ANCHOR_AUDIT", "OBLIGATION_TREE", "PROOF",
            "VALIDATION", "RELEASE",
        )
    )
    assert statement["canonical_formal_target"]["elaborated_expression_sha256"] == (
        STATEMENT_EXPRESSION_SHA256
    )
    assert statement["theorem_proved"] is statement["theorem_complete"] is False
    assert anchor["root_machine_classification"] == "M4"
    assert anchor["theorem_proved"] is anchor["theorem_complete"] is False
    assert [row["obligation_id"] for row in registry["obligations"]] == INVENTORY_IDS
    closure = graphs["closure_boundary"]
    assert closure["closed_obligations"] == []
    assert closure["conditionally_composed_obligations"] == ["M0442-T"]
    assert closure["remaining_root_cut_set"] == FROZEN_LEAF_CUT
    assert closure["root_closed"] is False
    assert closure["audit_complete"] is closure["theorem_complete"] is False
    root_node = next(row for row in graphs["nodes"] if row["obligation_id"] == "M0442-ROOT")
    assert root_node["debt"] == "H1/M4/R4" and root_node["status"] == "open"

    assert blocker["verdict"] == "blocked" and blocker["state"] == "[_]"
    assert blocker["closed_obligations"] == []
    assert blocker["remaining_root_cut_set"] == FROZEN_LEAF_CUT
    assert blocker["root_closed"] is blocker["audit_complete"] is False
    assert blocker["theorem_complete"] is False
    assert validation["support_state"] == "provisional_worker_selftest"
    assert validation["proposed_state"] == "[_]"
    assert validation["accepted"] is validation["release_grade"] is False
    assert validation["result"]["validated_nonclosing_declarations"] == NONCLOSING_DECLARATIONS
    assert validation["result"]["supported_obligation_ids"] == []
    assert validation["result"]["provisionally_closed_obligation_ids"] == []
    assert validation["result"]["accepted_closed_obligation_ids"] == []
    assert validation["result"]["root_closed"] is False
    assert validation["result"]["root_kernel_closed"] is False
    assert validation["result"]["root_vector_before"] == (
        validation["result"]["root_vector_after"]
    ) == {"H": "H1", "M": "M4", "R": "R4"}
    assert validation["result"]["remaining_root_cut_set"] == FROZEN_LEAF_CUT
    assert validation["result"]["audit_complete"] is False
    assert validation["result"]["theorem_complete"] is False

    disagreement = decision["authority_disagreement"]
    assert disagreement["instance_intake_projection"] == {
        "H": "H1", "M": "M3", "R": "R3"
    }
    assert disagreement["current_graph_and_validation_classification"] == {
        "H": "H1", "M": "M4", "R": "R4"
    }
    assert disagreement["reconciled"] is False
    assert disagreement["status_rule"] == "weaker_status_wins_no_silent_promotion"

    evidence = decision["evidence_reconciliation"]
    assert evidence["exact_frozen_target_elaboration"] == "provisional_pass"
    assert evidence["exact_root_kernel_closure"] == "fail_closed"
    assert evidence["frozen_child_to_parent_composition"] == "conditional_only"
    assert evidence["accepted_closed_obligation_ids"] == []
    false_gates = (
        "validation_dependency_master_accepted",
        "authoritative_public_projection_reconciled",
        "accepted_foundation_profile",
        "complete_transitive_tcb_and_provenance",
        "human_source_h0_accepted",
        "readability_r0_accepted",
        "immutable_clean_release_input",
        "cold_empty_cache_build",
        "offline_archive_replay",
        "complete_sbom_and_license_closure",
        "deterministic_release_bundle",
        "distinct_runner_independent_verification",
        "independently_implemented_minimal_verifier",
        "second_signed_attestation",
        "protected_ci_and_adversarial_gates",
        "master_acceptance",
    )
    assert all(evidence[key] is False for key in false_gates)

    result = decision["decision"]
    assert result["verdict"] == "blocked"
    assert result["lifecycle_before"] == result["lifecycle_after"] == "planned"
    assert result["instance_recorded_projection_before"] == (
        result["instance_recorded_projection_after"]
    ) == {"H": "H1", "M": "M3", "R": "R3"}
    assert result["current_provisional_root_classification_before"] == (
        result["current_provisional_root_classification_after"]
    ) == {"H": "H1", "M": "M4", "R": "R4"}
    assert result["audit_complete"] is result["theorem_complete"] is False
    assert result["release_accepted"] is False
    assert result["audit_z"] == result["theorem_z"] == "blocked"
    assert result["accepted_receipt_ids"] == decision["accepted_receipt_ids"] == []
    assert result["first_failed_gate"] == "S56-10.2-DEPENDENCY-ACCEPTANCE"
    assert result["first_failed_gate_detail"] == (
        "dependency.S56-M-0442-VALIDATION.master_acceptance"
    )
    assert result["first_identified_deep_theorem_gap"] == FIRST_THEOREM_GAP
    assert result["first_failed_release_specific_gate"] == (
        "S56-RELEASE-IMMUTABLE-CLEAN-INPUT"
    )
    assert result["next_failed_release_protocol_gate"] == (
        "S56-10.6-HERMETIC-COLD-EMPTY-CACHE"
    )
    assert result["frozen_effective_leaf_cut"] == FROZEN_LEAF_CUT

    lake_link = LEAN_ROOT / ".lake"
    assert lake_link.is_symlink()
    assert os.readlink(lake_link) == (
        "/home/sansha-2/external/awesome_theorems/Formalizations/Lean/.lake"
    )
    mathlib = lake_link / "packages" / "mathlib"
    assert git("rev-parse", "HEAD", cwd=mathlib) == (
        "8a178386ffc0f5fef0b77738bb5449d50efeea95"
    )
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == (
        "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
    )
    assert git("status", "--porcelain=v1", "--untracked-files=all", cwd=mathlib) == ""
    assert git("remote", "get-url", "origin", cwd=mathlib) == (
        "https://github.com/leanprover-community/mathlib4.git"
    )
    assert sha256(mathlib / "LICENSE") == (
        "b40930bbcf80744c86c46a12bc9da056641d722716c378f5659b9e555ef833e1"
    )

    # The recorded predecessor recipe must stay stale rather than silently mutate its receipt.
    stale = run(
        ["/usr/bin/python3", "-I", "-B", f"Stage1_Instances/{THEOREM}/check_validation.py"],
        env={
            "HOME": "/tmp",
            "PATH": "/usr/bin:/bin",
            "LANG": "C.UTF-8",
            "LC_ALL": "C.UTF-8",
            "TZ": "UTC",
            "LEAN_NUM_THREADS": "1",
        },
        expected_exit=1,
    )
    assert "AssertionError" in stale.stdout
    narrow_output = replay_current_narrow_validation()

    if receipt is not None:
        assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
        assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
        assert receipt["support_state"] == "provisional_worker_selftest"
        assert receipt["proposed_state"] == "[_]"
        assert receipt["accepted"] is receipt["release_grade"] is False
        assert receipt["master_acceptance"] is False
        assert receipt["decision_id"] == decision["decision_id"]
        assert receipt["release_inputs"] == {
            "release-decision.json": sha256(HERE / "release-decision.json"),
            "release-spec.json": sha256(HERE / "release-spec.json"),
            "check_release.py": sha256(Path(__file__).resolve()),
            "validation-receipt.json": VALIDATION_RECEIPT_SHA256,
            "obligation-registry.json": UPSTREAM_INPUTS["obligation-registry.json"],
            "typed-graphs.json": UPSTREAM_INPUTS["typed-graphs.json"],
        }
        assert receipt["current_narrow_replay"]["stdout_sha256"] == hashlib.sha256(
            narrow_output.encode("utf-8")
        ).hexdigest()
        assert receipt["current_narrow_replay"]["stdout_bytes"] == len(
            narrow_output.encode("utf-8")
        )
        assert receipt["result"] == result
        assert receipt["known_failures"] == decision["known_failures"]
        assert set(receipt["changed_paths"]) == CHANGED_PATHS

    for relative in CHANGED_PATHS - {".stage1-worker-selftest.json"}:
        path = ROOT / relative
        if not path.exists():
            continue
        data = path.read_bytes()
        assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())

    selftest_path = ROOT / ".stage1-worker-selftest.json"
    if selftest_path.exists():
        packet = load(selftest_path)
        assert set(packet) == {
            "item_id", "changed_paths", "commands", "output_summary",
            "base_revision", "known_failures", "state",
        }
        assert packet["item_id"] == ITEM and packet["state"] == "[_]"
        assert packet["base_revision"] == BASE_REVISION
        assert set(packet["changed_paths"]) == CHANGED_PATHS
        assert packet["known_failures"] == decision["known_failures"]
        actual_changes = {
            line[3:] for line in git(
                "status", "--short", "--untracked-files=all"
            ).splitlines()
            if line[3:] != "Formalizations/Lean/.lake"
        }
        assert actual_changes == CHANGED_PATHS, (actual_changes, CHANGED_PATHS)

    print("PASS THM-M-0442 release inputs and all 21 frozen obligations reconciled")
    print("PASS current narrow network-isolated trust-zero Lean replay; zero obligations closed")
    print("OPEN projection drift: intake H1/M3/R3 versus current provisional H1/M4/R4")
    print("BLOCKED validation dependency acceptance and M0442-M-MODULI deep package")
    print("BLOCKED clean cold/offline replay, independent verification, and master acceptance")
    print("VERDICT blocked; AUDIT-Z=false; THEOREM-Z=false; theorem_complete=false")


if __name__ == "__main__":
    main()
