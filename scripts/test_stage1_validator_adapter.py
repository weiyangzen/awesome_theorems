#!/usr/bin/env python3
"""Focused pure tests for the scheduler-owned Stage1 validator adapter."""

from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path
import sys
import unittest


MODULE_PATH = Path(__file__).with_name("stage1_validator_adapter.py")
SPEC = importlib.util.spec_from_file_location(
    "stage1_validator_adapter_under_test", MODULE_PATH
)
assert SPEC is not None and SPEC.loader is not None
adapter = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = adapter
SPEC.loader.exec_module(adapter)


def contract(*, declaration: object = ...) -> bytes:
    phase: dict[str, object] = {"phase": "intake"}
    if declaration is not ...:
        phase[adapter.PROFILE_FIELD] = declaration
    return json.dumps(
        {
            "schema_version": "stage1-phase-acceptance-contracts/1.0",
            "phases": [phase],
        },
        sort_keys=True,
    ).encode()


class Fixture:
    validator = b"print('PASS')\n"

    @staticmethod
    def adapt(
        *,
        contract_bytes: bytes | None = None,
        stdout: bytes = b"PASS\n",
        stderr: bytes = b"",
        exit_code: int | None = 0,
        timed_out: bool = False,
        **overrides: object,
    ) -> dict[str, object]:
        raw_contract = contract() if contract_bytes is None else contract_bytes
        kwargs: dict[str, object] = {
            "contract_bytes": raw_contract,
            "contract_sha256": adapter.sha256_bytes(raw_contract),
            "contract_git_blob": adapter.git_blob_oid(raw_contract),
            "item_id": "S56-M-0001-INTAKE",
            "theorem_id": "THM-M-0001",
            "phase": "intake",
            "validator_path": "Stage1_Instances/THM-M-0001/check_intake.py",
            "validator_bytes": Fixture.validator,
            "validator_git_blob": adapter.git_blob_oid(Fixture.validator),
            "argv": [
                "/usr/bin/python3",
                "-I",
                "-B",
                "Stage1_Instances/THM-M-0001/check_intake.py",
            ],
            "exit_code": exit_code,
            "timed_out": timed_out,
            "stdout": stdout,
            "stderr": stderr,
        }
        kwargs.update(overrides)
        return adapter.adapt_validator_result(**kwargs)


class UnsupportedContractTests(unittest.TestCase):
    def test_current_contract_without_profile_returns_typed_unsupported(self) -> None:
        receipt = Fixture.adapt(stdout=b"PASS: all checks passed\n")
        self.assertFalse(receipt["adapter"]["declared"])
        self.assertFalse(receipt["adapter"]["supported"])
        self.assertEqual(
            receipt["adapter"]["reason"], "phase_adapter_profile_not_declared"
        )
        semantic = receipt["semantic_result"]
        self.assertEqual(
            semantic["schema_version"], adapter.SEMANTIC_RESULT_SCHEMA
        )
        self.assertEqual(semantic["status"], "rejected")
        self.assertEqual(semantic["verdict"], "repair_required")
        self.assertFalse(semantic["phase_accepted"])
        self.assertFalse(semantic["phase_predicate_proven"])
        self.assertEqual(
            semantic["first_failed_gate"], "ADAPTER-PROFILE-UNSUPPORTED"
        )
        adapter.verify_adapter_receipt(receipt)

    def test_unknown_and_malformed_profiles_fail_closed_as_results(self) -> None:
        cases = (
            (
                {
                    "profile_id": "unknown/1",
                    "owner": adapter.PROFILE_OWNER,
                    "output_schema": adapter.SEMANTIC_RESULT_SCHEMA,
                },
                "phase_adapter_profile_not_implemented",
            ),
            (
                {
                    "profile_id": adapter.LEGACY_NEGATIVE_ONLY_PROFILE,
                    "owner": "worker",
                    "output_schema": adapter.SEMANTIC_RESULT_SCHEMA,
                },
                "phase_adapter_profile_malformed",
            ),
        )
        for declaration, reason in cases:
            with self.subTest(reason=reason):
                receipt = Fixture.adapt(contract_bytes=contract(declaration=declaration))
                self.assertEqual(receipt["adapter"]["reason"], reason)
                self.assertFalse(receipt["semantic_result"]["phase_accepted"])

    def test_supported_negative_only_profile_never_accepts_pass_prose(self) -> None:
        declared = contract(
            declaration={
                "profile_id": adapter.LEGACY_NEGATIVE_ONLY_PROFILE,
                "owner": adapter.PROFILE_OWNER,
                "output_schema": adapter.SEMANTIC_RESULT_SCHEMA,
            }
        )
        receipt = Fixture.adapt(contract_bytes=declared, stdout=b"PASS\n")
        self.assertTrue(receipt["adapter"]["supported"])
        self.assertEqual(receipt["adapter"]["reason"], None)
        self.assertEqual(
            receipt["semantic_result"]["first_failed_gate"],
            "ADAPTER-POSITIVE-PROOF-UNAVAILABLE",
        )
        self.assertFalse(receipt["semantic_result"]["phase_accepted"])

    def test_target_owned_positive_json_is_only_observed_not_trusted(self) -> None:
        claimed = {
            "schema_version": adapter.SEMANTIC_RESULT_SCHEMA,
            "status": "passed",
            "verdict": "phase_accepted",
            "phase_accepted": True,
            "phase_predicate_proven": True,
            "blocked": False,
            "open_obligations": 0,
            "stale_inputs": [],
        }
        receipt = Fixture.adapt(stdout=json.dumps(claimed).encode())
        self.assertFalse(receipt["semantic_result"]["phase_accepted"])
        self.assertFalse(receipt["semantic_result"]["phase_predicate_proven"])


class NegativePreservationTests(unittest.TestCase):
    def test_negative_json_preserves_blocked_open_and_stale(self) -> None:
        legacy = {
            "status": "blocked",
            "blocked": True,
            "open_obligations": 3,
            "stale_inputs": ["statement.json", "proof.lean"],
        }
        receipt = Fixture.adapt(stdout=json.dumps(legacy).encode())
        semantic = receipt["semantic_result"]
        self.assertEqual(semantic["status"], "blocked")
        self.assertEqual(semantic["verdict"], "blocked")
        self.assertTrue(semantic["blocked"])
        self.assertEqual(semantic["open_obligations"], 3)
        self.assertEqual(
            semantic["stale_inputs"], ["proof.lean", "statement.json"]
        )
        self.assertFalse(semantic["phase_accepted"])

    def test_nonzero_and_timeout_remain_negative(self) -> None:
        failed = Fixture.adapt(stdout=b"PASS\n", exit_code=7)
        self.assertEqual(failed["semantic_result"]["status"], "failed")
        self.assertFalse(failed["semantic_result"]["phase_accepted"])
        timed_out = Fixture.adapt(
            stdout=b"PASS\n", exit_code=None, timed_out=True
        )
        self.assertEqual(timed_out["semantic_result"]["status"], "failed")
        self.assertEqual(
            timed_out["semantic_result"]["first_failed_gate"],
            "ADAPTER-REPLAY-TIMEOUT",
        )

    def test_negative_stderr_cannot_be_hidden_by_positive_stdout(self) -> None:
        receipt = Fixture.adapt(
            stdout=b"PASS\n", stderr=b"BLOCKED: source is stale\n"
        )
        semantic = receipt["semantic_result"]
        self.assertTrue(semantic["blocked"])
        self.assertEqual(semantic["status"], "blocked")
        self.assertIn("legacy-output-reported-stale", semantic["stale_inputs"])


class ContentBindingTests(unittest.TestCase):
    def test_receipt_binds_validator_argv_complete_output_phase_and_contract(self) -> None:
        stdout = b"line one\nline two\x00\n"
        stderr = b"diagnostic\xff"
        receipt = Fixture.adapt(stdout=stdout, stderr=stderr)
        self.assertEqual(
            receipt["validator"]["sha256"], adapter.sha256_bytes(Fixture.validator)
        )
        self.assertEqual(
            receipt["invocation"]["argv"][0], "/usr/bin/python3"
        )
        self.assertEqual(receipt["output"]["stdout_size"], len(stdout))
        self.assertEqual(receipt["output"]["stderr_size"], len(stderr))
        self.assertEqual(receipt["item_id"], "S56-M-0001-INTAKE")
        self.assertEqual(receipt["phase"], "intake")
        self.assertRegex(receipt["receipt_sha256"], r"^[0-9a-f]{64}$")
        adapter.verify_adapter_receipt(receipt)

    def test_any_bound_field_tamper_is_detected(self) -> None:
        receipt = Fixture.adapt()
        tampered = copy.deepcopy(receipt)
        tampered["invocation"]["argv"].append("--unsafe")
        with self.assertRaisesRegex(adapter.AdapterError, "does not bind"):
            adapter.verify_adapter_receipt(tampered)
        tampered = copy.deepcopy(receipt)
        tampered["semantic_result"]["phase_accepted"] = True
        tampered["semantic_result_sha256"] = adapter.sha256_bytes(
            adapter.canonical_json(tampered["semantic_result"])
        )
        tampered["receipt_sha256"] = adapter.sha256_bytes(
            adapter.canonical_json(
                {key: value for key, value in tampered.items() if key != "receipt_sha256"}
            )
        )
        with self.assertRaisesRegex(adapter.AdapterError, "not fail-closed"):
            adapter.verify_adapter_receipt(tampered)
        tampered = copy.deepcopy(receipt)
        tampered["output"]["stdout_base64"] = "UEFTUw=="
        tampered["receipt_sha256"] = adapter.sha256_bytes(
            adapter.canonical_json(
                {key: value for key, value in tampered.items() if key != "receipt_sha256"}
            )
        )
        with self.assertRaisesRegex(adapter.AdapterError, "stdout binding is stale"):
            adapter.verify_adapter_receipt(tampered)

    def test_stale_contract_or_validator_blob_and_incomplete_output_are_rejected(self) -> None:
        raw = contract()
        cases = (
            {"contract_sha256": "0" * 64},
            {"contract_git_blob": "0" * 40},
            {"validator_git_blob": "0" * 40},
            {"stdout_complete": False},
            {"stderr_complete": False},
        )
        for overrides in cases:
            with self.subTest(overrides=overrides):
                with self.assertRaises(adapter.AdapterError):
                    Fixture.adapt(contract_bytes=raw, **overrides)

    def test_identity_and_path_are_exact(self) -> None:
        cases = (
            {"item_id": "S56-M-0002-INTAKE"},
            {"item_id": "S56-M-0001-PROOF"},
            {"validator_path": "../check.py"},
        )
        for overrides in cases:
            with self.subTest(overrides=overrides):
                with self.assertRaises(adapter.AdapterError):
                    Fixture.adapt(**overrides)


if __name__ == "__main__":
    unittest.main()
