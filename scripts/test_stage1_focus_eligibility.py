#!/usr/bin/env python3
"""Focused fail-closed tests for Stage1 v2 focus admission."""

from __future__ import annotations

import copy
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
from unittest import mock

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey


ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "scripts" / "stage1_focus_eligibility.py"
SPEC = importlib.util.spec_from_file_location("stage1_focus_eligibility_under_test", MODULE)
assert SPEC is not None and SPEC.loader is not None
focus = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(focus)

THEOREM = "THM-M-0001"
NOW = datetime(2026, 6, 1, tzinfo=timezone.utc)
SHA_A = "a" * 64
SHA_B = "b" * 64
SHA_C = "c" * 64


class Fixture:
    def __init__(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        schema = self.root / "Docs" / "Stage1_Focus_Eligibility_Schema.json"
        schema.parent.mkdir(parents=True)
        shutil.copy2(ROOT / "Docs" / "Stage1_Focus_Eligibility_Schema.json", schema)
        self.timestamp_key = Ed25519PrivateKey.generate()
        trust_anchors = {
            "schema_version": focus.TRUST_ANCHORS_SCHEMA,
            "signature_algorithm": focus.SIGNATURE_ALGORITHM,
            "keys": [
                {
                    "key_id": "fixture-scheduler-1",
                    "role": "scheduler_issuance",
                    "principal_id": "intake-operator",
                    "public_key_hex": Ed25519PrivateKey.generate().public_key().public_bytes_raw().hex(),
                    "status": "active",
                    "not_before": "2026-01-01T00:00:00Z",
                    "not_after": None,
                },
                {
                    "key_id": "fixture-reviewer-1",
                    "role": "independent_review",
                    "principal_id": "reviewer-1",
                    "public_key_hex": Ed25519PrivateKey.generate().public_key().public_bytes_raw().hex(),
                    "status": "active",
                    "not_before": "2026-01-01T00:00:00Z",
                    "not_after": None,
                },
                {
                    "key_id": "fixture-publication-tsa-1",
                    "role": "publication_timestamp",
                    "principal_id": "external-publication-tsa-1",
                    "public_key_hex": self.timestamp_key.public_key().public_bytes_raw().hex(),
                    "status": "active",
                    "not_before": "2026-01-01T00:00:00Z",
                    "not_after": None,
                },
            ],
        }
        self.trust_anchors = schema.parent / "Stage1_Focus_Trust_Anchors.json"
        self.trust_anchors.write_text(
            json.dumps(trust_anchors, ensure_ascii=True, indent=2) + "\n",
            encoding="utf-8",
        )
        self.trust_anchor_sha = self.digest(self.trust_anchors)
        self.instance = self.root / "Stage1_Instances" / THEOREM
        self.lean_root = self.root / "Formalizations" / "Lean"
        self.instance.mkdir(parents=True)
        self.lean_root.mkdir(parents=True)
        (self.lean_root / "lean-toolchain").write_text(
            "leanprover/lean4:v4.29.0\n", encoding="utf-8"
        )
        self.manifest = self.lean_root / "lake-manifest.json"
        self.manifest.write_text(
            json.dumps(
                {
                    "version": "1.1.0",
                    "packagesDir": ".lake/packages",
                    "packages": [
                        {
                            "url": "https://example.invalid/formal-proof.git",
                            "type": "git",
                            "subDir": None,
                            "scope": "",
                            "rev": "0123456789abcdef0123456789abcdef01234567",
                            "name": "formal-proof",
                            "manifestFile": "lake-manifest.json",
                            "inputRev": "0123456789abcdef0123456789abcdef01234567",
                            "inherited": False,
                            "configFile": "lakefile.toml",
                        }
                    ],
                    "name": "FocusFixture",
                    "lakeDir": ".lake",
                },
                ensure_ascii=True,
            )
            + "\n",
            encoding="utf-8",
        )
        self.bound = self.instance / "focus-evidence.txt"
        self.target = self.instance / "Target.lean"
        self.transport_artifact = self.instance / "MachineTransport.lean"
        self.transport_validator = self.instance / "check_machine_transport.py"
        self.transport_replay_output = self.instance / "machine-transport-replay.txt"
        self.transport_trust_output = self.instance / "machine-transport-trust.txt"
        self.transport_receipt = self.instance / "machine-transport-replay.json"
        self.disposition_report = self.instance / "terminal-disposition-report.json"
        self.bound.write_text("independently checked evidence\n", encoding="utf-8")
        self.external_publication = self.instance / "external-proof-publication.txt"
        self.external_publication.write_text(
            "immutable publication evidence for the external proof\n",
            encoding="utf-8",
        )
        self.external_provenance = self.instance / "external-proof-provenance.json"
        self.human_source = self.instance / "human-source.txt"
        self.human_review = self.instance / "human-source-review.json"
        self.target.write_text("theorem target : True := by trivial\n", encoding="utf-8")
        self.human_source.write_text(
            "Exact Theorem\nTheorem 1\nProof of the exact statement.\n",
            encoding="utf-8",
        )
        human_source_sha = self.digest(self.human_source)
        human_subject = {
            "kind": "human_proof_source",
            "immutable_id": "doi:10.example/exact",
            "citation": "Author, Exact Theorem",
            "locator": "Theorem 1",
            "artifact_sha256": human_source_sha,
            "statement_fingerprint": SHA_A,
            "statement_boundary": "the exact theorem with all hypotheses",
            "hypotheses": ["the declared domain and boundary assumptions"],
        }
        human_review = {
            "schema_version": "stage1-human-source-review/1.0",
            "theorem_id": THEOREM,
            "source": {
                "citation": "Author, Exact Theorem",
                "locator": "Theorem 1",
                "immutable_id": "doi:10.example/exact",
                "artifact_path": f"Stage1_Instances/{THEOREM}/{self.human_source.name}",
                "content_sha256": human_source_sha,
            },
            "publication_timestamp": self.timestamp_token(
                human_subject,
                issued_at="2026-05-30T18:00:00Z",
                token_id="fixture-human-proof-publication-1",
            ),
            "statement_fingerprint": SHA_A,
            "statement_boundary": "the exact theorem with all hypotheses",
            "statement_crosswalk": {
                "source_artifact_sha256": human_source_sha,
                "locator": "Theorem 1",
                "boundary": "the exact theorem with all hypotheses",
                "hypotheses": ["the declared domain and boundary assumptions"],
                "statement_fingerprint": SHA_A,
                "target_declaration_type_sha256": SHA_A,
                "relation": "exact",
            },
            "hypotheses": ["the declared domain and boundary assumptions"],
            "publication_status": "peer_reviewed",
            "license": {"identifier": "CC-BY-4.0", "reviewed_for_use": True},
            "reviewer": {"id": "source-reviewer", "role": "independent_reviewer"},
            "reviewed_at": "2026-05-31T19:00:00Z",
            "decision": "accepted",
        }
        human_review["review_sha256"] = hashlib.sha256(
            json.dumps(human_review, ensure_ascii=True, sort_keys=True,
                       separators=(",", ":")).encode()
        ).hexdigest()
        self.human_review.write_text(
            json.dumps(human_review, ensure_ascii=True, indent=2) + "\n",
            encoding="utf-8",
        )
        self.transport_artifact.write_text(
            "theorem transported_target : True := by trivial\n", encoding="utf-8"
        )
        self.transport_validator.write_text(
            "# scheduler-owned transport replay validator\n", encoding="utf-8"
        )
        self.transport_replay_output.write_text(
            "transport replay passed\n", encoding="utf-8"
        )
        self.transport_trust_output.write_text(
            "transport trust audit passed\n", encoding="utf-8"
        )
        self.write_machine_transport_receipt()
        subprocess.run(["git", "init", "-q"], cwd=self.root, check=True)
        subprocess.run(
            ["git", "config", "user.email", "focus-test@example.invalid"],
            cwd=self.root,
            check=True,
        )
        subprocess.run(
            ["git", "config", "user.name", "Focus Eligibility Test"],
            cwd=self.root,
            check=True,
        )
        blueprint = self.root / "Docs" / "Stage1_Blueprint_v2.md"
        blueprint.write_text(
            "# Test Stage1 v2 authority\n\n"
            f"{focus.CHECKLIST_BEGIN}\n"
            "## Test execution checklist\n"
            f"- [ ] `S56-M-0001-RELEASE` / `{THEOREM}` / `release`: "
            "Reconcile release evidence. {attempts=0}\n"
            f"{focus.CHECKLIST_END}\n",
            encoding="utf-8",
        )
        membership = copy.deepcopy(
            json.loads(
                (ROOT / focus.TARGET_MEMBERSHIP_RELATIVE_PATH).read_text(
                    encoding="utf-8"
                )
            )
        )
        membership_path = self.root / focus.TARGET_MEMBERSHIP_RELATIVE_PATH
        membership_path.write_text(
            json.dumps(membership, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        subprocess.run(["git", "add", "."], cwd=self.root, check=True)
        subprocess.run(
            ["git", "commit", "-q", "-m", "freeze focus fixture"],
            cwd=self.root,
            check=True,
        )
        self.base_revision = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=self.root,
            check=True,
            text=True,
            capture_output=True,
        ).stdout.strip()

    def close(self) -> None:
        self.temp.cleanup()

    @staticmethod
    def digest(path: Path) -> str:
        return hashlib.sha256(path.read_bytes()).hexdigest()

    def evidence(self, role: str) -> dict[str, str]:
        return {
            "path": f"Stage1_Instances/{THEOREM}/{self.bound.name}",
            "sha256": self.digest(self.bound),
            "role": role,
        }

    def timestamp_token(
        self, subject: dict[str, object], *, issued_at: str, token_id: str
    ) -> dict[str, object]:
        subject_sha = hashlib.sha256(
            json.dumps(subject, ensure_ascii=True, sort_keys=True,
                       separators=(",", ":")).encode()
        ).hexdigest()
        signature = self.timestamp_key.sign(
            focus._timestamp_signature_payload(
                token_id=token_id,
                issued_at=issued_at,
                subject_sha256=subject_sha,
            )
        ).hex()
        return {
            "schema_version": focus.TIMESTAMP_TOKEN_SCHEMA,
            "token_id": token_id,
            "issued_at": issued_at,
            "subject": subject,
            "subject_sha256": subject_sha,
            "authority": {
                "id": "external-publication-tsa-1",
                "role": "publication_timestamp_authority",
            },
            "key_id": "fixture-publication-tsa-1",
            "signature_algorithm": "Ed25519",
            "signature": signature,
        }

    def machine_transport_evidence(self) -> dict[str, str]:
        return {
            "path": f"Stage1_Instances/{THEOREM}/{self.transport_receipt.name}",
            "sha256": self.digest(self.transport_receipt),
            "role": "statement_match",
            "evidence_kind": "machine_checked_statement_transport",
            "source_formal_system": "Lean 4",
            "source_declaration": "Proof.Exact.theorem_one",
            "source_declaration_type_sha256": SHA_C,
            "target_formal_system": "Lean 4",
            "target_declaration": "Stage1.THM_M_0001.target",
            "target_declaration_type_sha256": SHA_A,
            "replay_receipt_sha256": self.digest(self.transport_receipt),
        }

    def configure_pinned_transport_receipt(self, receipt: dict) -> dict:
        receipt["machine_evidence_class"] = "exact_pinned_closure"
        receipt["repository_gap"]["local_presence"] = "pinned_dependency"
        receipt["evidence_bindings"][0] = {
            "path": f"Stage1_Instances/{THEOREM}/{self.human_review.name}",
            "sha256": self.digest(self.human_review),
            "role": "human_source_review",
        }
        return receipt

    def rewrite_machine_provenance_timestamp(
        self, receipt: dict, *, issued_at: str, reviewed_at: str
    ) -> None:
        source = receipt["machine_proof"]["source"]
        report = json.loads(self.external_provenance.read_text(encoding="utf-8"))
        subject = {
            "kind": "external_machine_proof",
            "immutable_id": report["publication"]["immutable_id"],
            "repository": source["repository"],
            "revision": source["revision"],
            "tree_or_archive_sha256": source["tree_or_archive_sha256"],
            "file_path": source["file_path"],
            "file_sha256": source["file_sha256"],
            "declaration": source["declaration"],
            "declaration_type_sha256": source["declaration_type_sha256"],
            "terminal_proof_body_sha256": source["terminal_proof_body"]["sha256"],
        }
        report["source"] = {key: value for key, value in subject.items() if key not in {
            "kind", "immutable_id"
        }}
        report["publication"]["timestamp"] = self.timestamp_token(
            subject,
            issued_at=issued_at,
            token_id="fixture-machine-proof-publication-rewritten",
        )
        report["reviewed_at"] = reviewed_at
        report.pop("provenance_sha256", None)
        report["provenance_sha256"] = hashlib.sha256(
            json.dumps(report, ensure_ascii=True, sort_keys=True,
                       separators=(",", ":")).encode()
        ).hexdigest()
        self.external_provenance.write_text(
            json.dumps(report, ensure_ascii=True, indent=2) + "\n", encoding="utf-8"
        )
        subprocess.run(
            ["git", "add", self.external_provenance.relative_to(self.root).as_posix()],
            cwd=self.root, check=True,
        )
        subprocess.run(
            ["git", "commit", "-q", "-m", "rewrite exact proof publication timestamp"],
            cwd=self.root, check=True,
        )
        self.base_revision = subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=self.root, check=True,
            text=True, capture_output=True,
        ).stdout.strip()
        receipt["repository_base_revision"] = self.base_revision
        binding = next(
            row for row in receipt["evidence_bindings"]
            if row["role"] == focus.EXTERNAL_PROVENANCE_ROLE
        )
        binding["sha256"] = self.digest(self.external_provenance)
        source["pre_stage1_provenance"] = {
            "path": binding["path"],
            "sha256": binding["sha256"],
            "provenance_sha256": report["provenance_sha256"],
        }

    def rebind_machine_provenance(self, receipt: dict) -> None:
        self.rewrite_machine_provenance_timestamp(
            receipt,
            issued_at="2026-05-30T20:00:00Z",
            reviewed_at="2026-05-31T18:30:00Z",
        )

    def write_machine_transport_receipt(self, **updates: object) -> None:
        relative = lambda path: f"Stage1_Instances/{THEOREM}/{path.name}"
        value = {
            "schema_version": "stage1-machine-transport-replay/1.0",
            "theorem_id": THEOREM,
            "source": {
                "formal_system": "Lean 4",
                "declaration": "Proof.Exact.theorem_one",
                "declaration_type_sha256": SHA_C,
            },
            "target": {
                "formal_system": "Lean 4",
                "declaration": "Stage1.THM_M_0001.target",
                "declaration_type_sha256": SHA_A,
            },
            "transport_artifact": {
                "path": relative(self.transport_artifact),
                "sha256": self.digest(self.transport_artifact),
                "formal_system": "Lean 4",
                "declaration": "Stage1.THM_M_0001.target",
                "declaration_type_sha256": SHA_A,
                "terminal_proof_body": {
                    "locator": "Stage1.THM_M_0001.target",
                    "kind": "theorem",
                    "sha256": SHA_B,
                },
            },
            "validator": {
                "path": relative(self.transport_validator),
                "sha256": self.digest(self.transport_validator),
                "authority": "scheduler_master_lane",
            },
            "replay": {
                "command": [
                    relative(self.transport_validator),
                    "--transport-artifact",
                    relative(self.transport_artifact),
                ],
                "checked_at": "2026-05-31T20:00:00Z",
                "exit_code": 0,
                "output": {
                    "path": relative(self.transport_replay_output),
                    "sha256": self.digest(self.transport_replay_output),
                },
                "toolchain": "leanprover/lean4:v4.19.0",
                "dependency_lock_sha256": SHA_C,
            },
            "trust_audit": {
                "placeholder_free": True,
                "unsafe_free": True,
                "oracle_free": True,
                "undeclared_axioms_free": True,
                "permitted_axioms": ["Classical.choice", "propext", "Quot.sound"],
                "tcb_description": "Lean kernel and pinned scheduler validator",
                "output": {
                    "path": relative(self.transport_trust_output),
                    "sha256": self.digest(self.transport_trust_output),
                },
            },
            "independent_review": {
                "reviewer": {
                    "id": "machine-transport-reviewer",
                    "role": "independent_reviewer",
                },
                "reviewed_at": "2026-05-31T20:30:00Z",
                "decision": "approved",
            },
        }
        value.update(updates)
        self.transport_receipt.write_text(
            json.dumps(value, ensure_ascii=True, indent=2) + "\n", encoding="utf-8"
        )

    def write_disposition_report(
        self, reason_code: str, facts: dict[str, object]
    ) -> dict[str, str]:
        value = {
            "schema_version": "stage1-terminal-disposition-report/1.0",
            "theorem_id": THEOREM,
            "reason_code": reason_code,
            "reviewer": {
                "id": "terminal-disposition-reviewer",
                "role": "independent_reviewer",
            },
            "reviewed_at": "2026-05-31T20:30:00Z",
            "facts": facts,
        }
        self.disposition_report.write_text(
            json.dumps(value, ensure_ascii=True, indent=2) + "\n", encoding="utf-8"
        )
        subprocess.run(
            ["git", "add", self.disposition_report.relative_to(self.root).as_posix()],
            cwd=self.root,
            check=True,
        )
        subprocess.run(
            ["git", "commit", "-q", "-m", f"freeze disposition report: {reason_code}"],
            cwd=self.root,
            check=True,
        )
        self.base_revision = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=self.root,
            check=True,
            text=True,
            capture_output=True,
        ).stdout.strip()
        return {
            "path": f"Stage1_Instances/{THEOREM}/{self.disposition_report.name}",
            "sha256": self.digest(self.disposition_report),
            "role": (
                "frontier_defer_review"
                if reason_code in focus.FRONTIER_DEFER_REASONS
                else "scope_exclusion_review"
            ),
        }

    def write_frontier_snapshot(self, boundary: str) -> dict[str, object]:
        snapshot = self.instance / "frontier-exception-snapshot.json"
        value = {
            "schema_version": "stage1-frontier-exception-snapshot/1.0",
            "theorem_id": THEOREM,
            "scheduler_owner": "scheduler_master_lane",
            "snapshot_id": "scheduler-snapshot-2026-05-31",
            "search_boundary_sha256": hashlib.sha256(
                boundary.encode("utf-8")
            ).hexdigest(),
            "exception_policy_sha256": None,
            "exception_state": "absent",
            "captured_at": "2026-05-31T20:00:00Z",
        }
        snapshot.write_text(
            json.dumps(value, ensure_ascii=True, indent=2) + "\n", encoding="utf-8"
        )
        subprocess.run(
            ["git", "add", snapshot.relative_to(self.root).as_posix()],
            cwd=self.root,
            check=True,
        )
        subprocess.run(
            ["git", "commit", "-q", "-m", "freeze frontier snapshot"],
            cwd=self.root,
            check=True,
        )
        self.base_revision = subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=self.root, check=True,
            text=True, capture_output=True,
        ).stdout.strip()
        return {
            "path": f"Stage1_Instances/{THEOREM}/{snapshot.name}",
            "sha256": self.digest(snapshot),
            **{key: value[key] for key in (
                "snapshot_id", "search_boundary_sha256",
                "exception_policy_sha256", "exception_state",
            )},
        }

    def base_receipt(self) -> dict:
        receipt = {
            "schema_version": "stage1-focus-eligibility/1.0",
            "theorem_id": THEOREM,
            "requirements_authority": "Docs/Stage1_Blueprint_v2.md",
            "repository_base_revision": self.base_revision,
            "scheduler_owner": "scheduler_master_lane",
            "generated_at": "2026-06-01T00:00:00Z",
            "evidence_as_of": "2026-05-31T21:00:00Z",
            "expires_at": "2026-12-01T00:00:00Z",
            "machine_evidence_class": "unknown",
            "execution_disposition": "research_required",
            "human_proof": {
                "status": "unknown",
                "statement_fingerprint": None,
                "source": None,
            },
            "target_binding": {
                "status": "unverified",
                "formal_system": None,
                "path": None,
                "file_sha256": None,
                "declaration": None,
                "declaration_type_sha256": None,
            },
            "statement_binding": None,
            "machine_proof": {
                "status": "unknown",
                "negative_search_boundary": None,
                "negative_search_inventory": [],
                "source": None,
            },
            "repository_gap": {
                "acceptance_status": "not_integrated",
                "local_presence": "absent",
                "integration_plan": [],
                "owned_paths": [],
            },
            "evidence_bindings": [],
            "issuance_authority": {
                "schema_version": focus.ISSUANCE_AUTHORITY_SCHEMA,
                "authority_revision": self.base_revision,
                "candidate_sha256": SHA_A,
                "proposal_sha256": SHA_B,
                "receipt_facts_sha256": SHA_C,
                "scheduler_issuer": {
                    "id": "intake-operator",
                    "role": "scheduler_master_lane",
                },
                "review_sha256": SHA_A,
                "unsigned_review_sha256": SHA_A,
                "reviewer": {
                    "id": "reviewer-1",
                    "role": "independent_reviewer",
                },
                "candidate_verification_sha256": SHA_B,
                "review_verification_sha256": SHA_C,
                "issuance": None,
            },
            "admission_authority": None,
            "admission_review": {
                "author": {"id": "intake-operator", "role": "scheduler_master_lane"},
                "reviewer": {"id": "reviewer-1", "role": "independent_reviewer"},
                "reviewed_at": "2026-05-31T22:00:00Z",
                "decision": "research_only",
            },
            "disposition_basis": None,
            "frontier_exception": None,
            "invalidation_conditions": sorted(focus.REQUIRED_INVALIDATIONS),
        }
        return receipt

    def exact_receipt(self) -> dict:
        subprocess.run(
            ["git", "reset", "--quiet", "HEAD", "--",
             self.external_publication.relative_to(self.root).as_posix(),
             self.external_provenance.relative_to(self.root).as_posix()],
            cwd=self.root, check=False,
        )
        receipt = self.base_receipt()
        receipt.update(
            machine_evidence_class="exact_external_unintegrated",
            execution_disposition="organize_or_integrate",
        )
        receipt["human_proof"] = {
            "status": "complete_source_confirmed",
            "statement_fingerprint": SHA_A,
            "source": {
                "citation": "Author, Exact Theorem",
                "locator": "Theorem 1",
                "immutable_id": "doi:10.example/exact",
                "content_sha256": self.digest(self.human_source),
                "proof_scope": "the exact theorem with all hypotheses",
                "hypotheses": ["the declared domain and boundary assumptions"],
                "publication_status": "peer_reviewed",
                "license": {
                    "identifier": "CC-BY-4.0",
                    "reviewed_for_use": True,
                },
                "accepted_by": {"id": "source-reviewer", "role": "independent_reviewer"},
                "accepted_at": "2026-05-31T19:00:00Z",
            },
        }
        receipt["target_binding"] = {
            "status": "verified",
            "formal_system": "Lean 4",
            "path": f"Stage1_Instances/{THEOREM}/{self.target.name}",
            "file_sha256": self.digest(self.target),
            "declaration": "Stage1.THM_M_0001.target",
            "declaration_type_sha256": SHA_A,
        }
        receipt["statement_binding"] = {
            "human_statement_fingerprint": SHA_A,
            "target_declaration_type_sha256": SHA_A,
            "match_kind": "exact",
            "evidence": [],
        }
        receipt["machine_proof"] = {
            "status": "exact_kernel_checked",
            "negative_search_boundary": None,
            "negative_search_inventory": [],
            "source": {
                "formal_system": "Lean 4",
                "repository": "https://example.invalid/formal-proof.git",
                "revision": "0123456789abcdef0123456789abcdef01234567",
                "tree_or_archive_sha256": SHA_A,
                "file_path": "Proof/Exact.lean",
                "file_sha256": SHA_B,
                "module": "Proof.Exact",
                "declaration": "Proof.Exact.theorem_one",
                "declaration_type_sha256": SHA_A,
                "match_kind": "exact",
                "transport_evidence": [],
                "pre_stage1_provenance": None,
                "terminal_proof_body": {
                    "locator": "Proof.Exact.theorem_one",
                    "kind": "theorem",
                    "sha256": SHA_A,
                },
                "kernel_replay": {
                    "command": ["lake", "env", "lean", "Proof/Exact.lean"],
                    "checked_at": "2026-05-31T21:00:00Z",
                    "exit_code": 0,
                    "output_sha256": SHA_B,
                    "toolchain": "leanprover/lean4:v4.19.0",
                    "dependency_lock_sha256": SHA_C,
                },
                "trust_audit": {
                    "placeholder_free": True,
                    "unsafe_free": True,
                    "oracle_free": True,
                    "undeclared_axioms_free": True,
                    "permitted_axioms": ["Classical.choice", "propext", "Quot.sound"],
                    "tcb_description": "Lean kernel and pinned compiler",
                    "output_sha256": SHA_A,
                },
                "compatibility": {
                    "status": "adapter_required",
                    "toolchain": "leanprover/lean4:v4.19.0",
                    "dependency_lock_sha256": SHA_C,
                },
                "license": {
                    "identifier": "Apache-2.0",
                    "integration_permitted": True,
                    "evidence_sha256": SHA_B,
                },
            },
        }
        receipt["repository_gap"] = {
            "acceptance_status": "not_integrated",
            "local_presence": "absent",
            "integration_plan": ["pin the source", "add a checked target wrapper"],
            "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        }
        receipt["evidence_bindings"] = [
            self.evidence(role)
            for role in (
                "human_source_review",
                "statement_match",
                "machine_source_pin",
                "kernel_replay",
                "trust_audit",
                "compatibility_audit",
                "license_review",
                "integration_plan",
            )
        ]
        source = receipt["machine_proof"]["source"]
        source_identity = {
            "repository": source["repository"],
            "revision": source["revision"],
            "tree_or_archive_sha256": source["tree_or_archive_sha256"],
            "file_path": source["file_path"],
            "file_sha256": source["file_sha256"],
            "declaration": source["declaration"],
            "declaration_type_sha256": source["declaration_type_sha256"],
            "terminal_proof_body_sha256": source["terminal_proof_body"]["sha256"],
        }
        publication_subject = {
            "kind": "external_machine_proof",
            "immutable_id": "fixture:external-proof:pre-stage1",
            **source_identity,
        }
        provenance = {
            "schema_version": focus.EXTERNAL_PROVENANCE_SCHEMA,
            "theorem_id": THEOREM,
            "source": source_identity,
            "publication": {
                "immutable_id": "fixture:external-proof:pre-stage1",
                "timestamp": self.timestamp_token(
                    publication_subject,
                    issued_at="2026-05-30T20:00:00Z",
                    token_id="fixture-machine-proof-publication-1",
                ),
            },
            "reviewer": {
                "id": "external-provenance-reviewer",
                "role": "independent_reviewer",
            },
            "reviewed_at": "2026-05-31T18:30:00Z",
            "decision": "accepted",
        }
        provenance["provenance_sha256"] = hashlib.sha256(
            json.dumps(provenance, ensure_ascii=True, sort_keys=True,
                       separators=(",", ":")).encode()
        ).hexdigest()
        self.external_provenance.write_text(
            json.dumps(provenance, ensure_ascii=True, indent=2) + "\n",
            encoding="utf-8",
        )
        subprocess.run(
            ["git", "add", self.external_publication.relative_to(self.root).as_posix(),
             self.external_provenance.relative_to(self.root).as_posix()],
            cwd=self.root, check=True,
        )
        subprocess.run(
            ["git", "commit", "-q", "-m", "freeze external proof provenance"],
            cwd=self.root, check=False,
        )
        self.base_revision = subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=self.root, check=True,
            text=True, capture_output=True,
        ).stdout.strip()
        receipt["repository_base_revision"] = self.base_revision
        provenance_binding = {
            "path": f"Stage1_Instances/{THEOREM}/{self.external_provenance.name}",
            "sha256": self.digest(self.external_provenance),
            "role": focus.EXTERNAL_PROVENANCE_ROLE,
        }
        receipt["evidence_bindings"].append(provenance_binding)
        source["pre_stage1_provenance"] = {
            "path": provenance_binding["path"],
            "sha256": provenance_binding["sha256"],
            "provenance_sha256": provenance["provenance_sha256"],
        }
        receipt["admission_review"]["decision"] = "admit_integration"
        receipt["admission_authority"] = self.authority_for(receipt)
        return receipt

    def authority_for(self, receipt: dict) -> dict:
        source = receipt["machine_proof"]["source"]
        target = receipt["target_binding"]
        replay_authority = {
            "schema_version": "stage1-focus-lean-authority/1.0",
            "toolchain": "leanprover/lean4:v4.29.0",
            "toolchain_file_sha256": SHA_A,
            "dependency_lock_sha256": SHA_B,
            "dependency_packages_sha256": None,
            "compiled_cache_sha256": None,
            "compiled_cache_file_count": 0,
            "compiled_cache_bytes": 0,
            "lean_binary_sha256": SHA_A,
            "lake_binary_sha256": SHA_B,
            "toolchain_closure_sha256": SHA_C,
            "toolchain_closure_file_count": 1,
            "toolchain_closure_bytes": 1,
            "network_policy": "denied",
            "repo_access": "read_only",
        }
        if receipt.get("machine_evidence_class") == "exact_pinned_closure":
            replay_authority.update(
                dependency_lock_sha256=self.digest(self.manifest),
                dependency_packages_sha256=SHA_A,
                compiled_cache_sha256=SHA_B,
                compiled_cache_file_count=1,
                compiled_cache_bytes=1,
            )
        external = {
            "schema_version": focus.AUTHORITY_RESULT_SCHEMA,
            "formal_system": source["formal_system"],
            "toolchain": source["kernel_replay"]["toolchain"],
            "dependency_lock_sha256": source["kernel_replay"]["dependency_lock_sha256"],
            "file_path": source["file_path"],
            "file_sha256": source["file_sha256"],
            "module": source["module"],
            "declaration": source["declaration"],
            "declaration_type_sha256": source["declaration_type_sha256"],
            "terminal_proof_body_sha256": source["terminal_proof_body"]["sha256"],
            "kernel_exit_code": 0,
            "placeholder_free": True,
            "unsafe_free": True,
            "oracle_free": True,
            "undeclared_axioms_free": True,
            "permitted_axioms": source["trust_audit"]["permitted_axioms"],
            "trust_audit_output_sha256": source["trust_audit"]["output_sha256"],
            "replay_authority": copy.deepcopy(replay_authority),
        }
        local = {
            "schema_version": focus.LOCAL_TARGET_RESULT_SCHEMA,
            "formal_system": "Lean 4",
            "repository_revision": receipt["repository_base_revision"],
            "file_path": target["path"],
            "file_sha256": target["file_sha256"],
            "declaration": target["declaration"],
            "declaration_type_sha256": target["declaration_type_sha256"],
            "toolchain": "leanprover/lean4:v4.29.0",
            "dependency_lock_sha256": self.digest(self.manifest),
            "kernel_exit_code": 0,
            "permitted_axioms": [],
            "trust_audit_output_sha256": SHA_A,
            "replay_authority": copy.deepcopy(replay_authority),
        }
        transport_authority = None
        if source.get("match_kind") == "checked_transport":
            value = {
                "schema_version": focus.TRANSPORT_AUTHORITY_RESULT_SCHEMA,
                "theorem_id": THEOREM,
                "replay_receipt": {
                    "path": f"Stage1_Instances/{THEOREM}/{self.transport_receipt.name}",
                    "sha256": self.digest(self.transport_receipt),
                },
                "source": {
                    "formal_system": source["formal_system"],
                    "declaration": source["declaration"],
                    "declaration_type_sha256": source["declaration_type_sha256"],
                },
                "local_target": {
                    "formal_system": target["formal_system"],
                    "declaration": target["declaration"],
                    "declaration_type_sha256": target["declaration_type_sha256"],
                },
                "transport_artifact": {
                    "path": f"Stage1_Instances/{THEOREM}/{self.transport_artifact.name}",
                    "sha256": self.digest(self.transport_artifact),
                    "declaration": target["declaration"],
                    "declaration_type_sha256": target["declaration_type_sha256"],
                    "terminal_proof_body_sha256": SHA_B,
                },
                "provider_materialization": {
                    "source_file_sha256": source["file_sha256"],
                    "module": focus.TRANSPORT_PROVIDER_MODULE,
                    "declaration": source["declaration"],
                    "compiled_exit_code": 0,
                },
                "semantic_dependency": {
                    "target_declaration": target["declaration"],
                    "provider_declaration": source["declaration"],
                    "relation": "direct_proof_body_constant_dependency",
                    "joint_kernel_exit_code": 0,
                    "joint_kernel_stdout_sha256": SHA_A,
                    "joint_kernel_stderr_sha256": SHA_B,
                },
            }
            value["transport_verification_sha256"] = hashlib.sha256(
                json.dumps(value, ensure_ascii=True, sort_keys=True,
                           separators=(",", ":")).encode()
            ).hexdigest()
            transport_authority = value

        def verification(actor: dict) -> dict:
            human_review = json.loads(self.human_review.read_text())
            human_support = {
                "path": f"Stage1_Instances/{THEOREM}/{self.human_review.name}",
                "sha256": self.digest(self.human_review),
                "review_sha256": human_review["review_sha256"],
                "source_artifact_path": f"Stage1_Instances/{THEOREM}/{self.human_source.name}",
                "source_content_sha256": self.digest(self.human_source),
                "publication_timestamp": focus._validate_independent_timestamp(
                    self.root,
                    human_review["publication_timestamp"],
                    expected_subject=human_review["publication_timestamp"]["subject"],
                    cutoff=None,
                    forbidden_principals={"source-reviewer", "intake-operator", "reviewer-1"},
                    label="human proof publication timestamp",
                ),
                "statement_crosswalk": human_review["statement_crosswalk"],
                "reviewer": human_review["reviewer"],
                "reviewed_at": human_review["reviewed_at"],
                "decision": "accepted",
            }
            value = {
                "schema_version": "stage1-focus-admission-verification/1.0",
                "theorem_id": THEOREM,
                "verification_kind": "external_lean_kernel_replay",
                "verifier": actor,
                "repository": source["repository"],
                "resolved_revision": source["revision"],
                "archive_sha256": source["tree_or_archive_sha256"],
                "resolved_tree": "1" * 40,
                "file_path": source["file_path"],
                "file_sha256": source["file_sha256"],
                "terminal_proof_body_sha256": source["terminal_proof_body"]["sha256"],
                "kernel_command": source["kernel_replay"]["command"],
                "kernel_exit_code": 0,
                "kernel_stdout_sha256": source["kernel_replay"]["output_sha256"],
                "kernel_authority_result": external,
                "local_target_authority_result": local,
                "kernel_stderr_sha256": SHA_A,
                "repository_access": "temporary_read_only_replay",
                "network_during_replay": False,
                "human_source_review": (
                    {
                        "human_source_review": human_support,
                        "machine_transport_authority": copy.deepcopy(transport_authority),
                    }
                    if transport_authority is not None
                    else human_support
                ),
            }
            value["verification_sha256"] = hashlib.sha256(
                json.dumps(value, ensure_ascii=True, sort_keys=True,
                           separators=(",", ":")).encode()
            ).hexdigest()
            return value
        with mock.patch.object(
            focus, "TRUST_ANCHORS_SHA256", self.trust_anchor_sha
        ):
            scheduler = verification({"id": "scheduler-verifier", "role": "scheduler_focus_verifier"})
            reviewer = verification({"id": "independent-verifier", "role": "independent_reviewer"})
        observed = {"external": external, "local_target": local}
        return {
            "scheduler_verification": scheduler,
            "reviewer_verification": reviewer,
            "observed_facts_sha256": hashlib.sha256(
                json.dumps(observed, ensure_ascii=True, sort_keys=True,
                           separators=(",", ":")).encode()
            ).hexdigest(),
        }

    def frontier_receipt(self) -> dict:
        receipt = self.exact_receipt()
        receipt["admission_authority"] = None
        receipt.update(
            machine_evidence_class="no_exact_candidate_as_of",
            execution_disposition="frontier_exception",
        )
        receipt["machine_proof"] = {
            "status": "no_usable_exact_artifact_located",
            "negative_search_boundary": (
                "No usable exact artifact located as of 2026-05-31 across the "
                "recorded repositories and declarations; no global nonexistence claim."
            ),
            "negative_search_inventory": [{
                "source": "pinned mathlib and the recorded external project index",
                "revision_or_snapshot": "snapshot-2026-05-31",
                "queries": ["exact theorem name", "target declaration type"],
                "searched_at": "2026-05-31T21:00:00Z",
                "candidate_rejections": [{
                    "candidate": "Related.NarrowerTheorem",
                    "reason": "strictly narrower conclusion",
                }],
            }],
            "source": None,
        }
        estimate = self.evidence("frontier_estimate_basis")
        receipt["evidence_bindings"] = [estimate]
        receipt["admission_review"] = {
            "author": {"id": "scheduler-estimator-1", "role": "scheduler_estimator"},
            "reviewer": {"id": "frontier-reviewer-1", "role": "independent_reviewer"},
            "reviewed_at": "2026-05-31T23:30:00Z",
            "decision": "admit_frontier_exception",
        }
        review_input = {
            "schema_version": focus.FRONTIER_REVIEW_INPUT_SCHEMA,
            "candidate_sha256": SHA_A,
            "theorem_id": THEOREM,
            "reviewer": {
                "id": "frontier-reviewer-1",
                "role": "independent_reviewer",
            },
            "authored_at": "2026-05-31T23:00:00Z",
            "decision": "approved",
            "assessed_completion_probability": 0.70,
            "estimation_method_assessment": (
                "Independent calibration against recorded bounded proof attempts."
            ),
            "comparables": ["bounded-attempt-a", "bounded-attempt-b"],
            "budget_assessment": {
                "scope": "exact root theorem and declared wrapper only",
                "wall_clock_seconds": 28800,
                "token_limit": 200000,
                "compute_seconds": 14400,
                "disk_bytes": 1073741824,
                "concurrency_limit": 1,
            },
            "milestone_assessment": [
                {
                    "id": "close_root",
                    "deadline_at": "2026-06-01T08:00:00Z",
                    "evidence_role": "root_proof_closure",
                },
                {
                    "id": "replay_root",
                    "deadline_at": "2026-06-01T20:00:00Z",
                    "evidence_role": "kernel_replay",
                },
            ],
            "validator_assessment": {
                "path": f"Stage1_Instances/{THEOREM}/{self.bound.name}",
                "sha256": self.digest(self.bound),
                "command": [
                    "python3",
                    f"Stage1_Instances/{THEOREM}/{self.bound.name}",
                ],
            },
            "stop_condition_assessment": sorted(
                focus.REQUIRED_FRONTIER_STOP_CONDITIONS
            ),
            "findings": [
                "The bounded controls support an assessed probability at threshold."
            ],
        }
        review_input["review_input_sha256"] = hashlib.sha256(
            json.dumps(
                review_input,
                ensure_ascii=True,
                sort_keys=True,
                separators=(",", ":"),
            ).encode("utf-8")
        ).hexdigest()
        receipt["frontier_exception"] = {
            "scheduler_owner": "scheduler_master_lane",
            "root_obligation": {
                "id": f"{THEOREM}-ROOT",
                "statement_fingerprint": SHA_A,
            },
            "assigned_worker": {"id": "proof-worker-1", "role": "proof_worker"},
            "estimator": {"id": "scheduler-estimator-1", "role": "scheduler_estimator"},
            "estimated_at": "2026-05-31T22:30:00Z",
            "estimation_method": "calibrated comparison against recorded closed proof obligations",
            "completion_probability": 0.70,
            "evidence": [copy.deepcopy(estimate)],
            "budget": {
                "scope": "exact root theorem and declared wrapper only",
                "wall_clock_seconds": 28800,
                "token_limit": 200000,
                "compute_seconds": 14400,
                "disk_bytes": 1073741824,
                "concurrency_limit": 1,
            },
            "milestones": [
                {
                    "id": "close_root",
                    "deadline_at": "2026-06-01T08:00:00Z",
                    "evidence_role": "root_proof_closure",
                },
                {
                    "id": "replay_root",
                    "deadline_at": "2026-06-01T20:00:00Z",
                    "evidence_role": "kernel_replay",
                },
            ],
            "validator": {
                "path": f"Stage1_Instances/{THEOREM}/{self.bound.name}",
                "sha256": self.digest(self.bound),
                "command": [
                    "python3",
                    f"Stage1_Instances/{THEOREM}/{self.bound.name}",
                ],
            },
            "stop_conditions": sorted(focus.REQUIRED_FRONTIER_STOP_CONDITIONS),
            "attempt_limit": 4,
            "lease_expires_at": "2026-06-02T00:00:00Z",
            "revocation_route": "scheduler_master_lane",
            "independent_review": {
                **review_input,
                "reviewed_at": "2026-05-31T23:30:00Z",
            },
        }
        return receipt

    def write(self, receipt: dict) -> str:
        path = self.instance / "focus-eligibility.json"
        path.write_text(json.dumps(receipt, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
        return self.digest(path)

    def set_release_state(self, state: str) -> None:
        text = (self.root / focus.REQUIREMENTS_AUTHORITY).read_text(encoding="utf-8")
        text = text.replace(
            "- [ ] `S56-M-0001-RELEASE`",
            f"- {state} `S56-M-0001-RELEASE`",
        )
        (self.root / focus.REQUIREMENTS_AUTHORITY).write_text(text, encoding="utf-8")
        subprocess.run(
            ["git", "add", focus.REQUIREMENTS_AUTHORITY], cwd=self.root, check=True
        )
        subprocess.run(
            ["git", "commit", "-q", "-m", f"set release cursor {state}"],
            cwd=self.root,
            check=True,
        )
        self.base_revision = subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=self.root, check=True,
            text=True, capture_output=True,
        ).stdout.strip()

    def write_master_release_acceptance(self) -> Path:
        release_decision = {
            "schema_version": "stage1-release-decision/1.0",
            "item_id": "S56-M-0001-RELEASE",
            "theorem_id": THEOREM,
            "verdict": "accepted",
            "terminal_decisions": {
                "audit_complete": True,
                "theorem_complete": True,
            },
            "remaining_root_cut_set": [],
            "root_vector": {"M": "M0-L"},
        }
        decision_path = self.instance / "release-decision.json"
        decision_path.write_text(
            json.dumps(release_decision, ensure_ascii=True, indent=2) + "\n",
            encoding="utf-8",
        )
        semantic_result = {
            "verdict": "accepted",
            "audit_complete": True,
            "theorem_complete": True,
        }
        replay = {
            "semantic_result": semantic_result,
            "semantic_result_sha256": hashlib.sha256(
                focus._master_canonical_json(semantic_result)
            ).hexdigest(),
        }
        replay["result_sha256"] = hashlib.sha256(
            focus._master_canonical_json(replay)
        ).hexdigest()
        semantic = {
            "decision": "phase_accepted",
            "phase_evidence_accepted": True,
            "audit_complete": True,
            "theorem_complete": True,
        }
        semantic["decision_sha256"] = hashlib.sha256(
            focus._master_canonical_json(semantic)
        ).hexdigest()
        receipt = {
            "schema_version": focus.MASTER_ACCEPTANCE_RECEIPT_SCHEMA,
            "item_id": "S56-M-0001-RELEASE",
            "theorem_id": THEOREM,
            "phase": "release",
            "worker_verdict": "accepted",
            "review_verdict": "phase_accepted",
            "phase_evidence_accepted": True,
            "audit_complete": True,
            "theorem_complete": True,
            "artifact_bindings": [{
                "path": f"Stage1_Instances/{THEOREM}/release-decision.json",
                "sha256": self.digest(decision_path),
                "role": "release_decision",
            }],
            "replay_result": replay,
            "replay_result_sha256": replay["result_sha256"],
            "semantic_decision": semantic,
            "semantic_decision_sha256": semantic["decision_sha256"],
        }
        payload = focus._master_canonical_json(receipt) + b"\n"
        digest = hashlib.sha256(payload).hexdigest()
        path = self.instance / "master-acceptance" / "release" / f"{digest}.json"
        path.parent.mkdir(parents=True)
        path.write_bytes(payload)
        subprocess.run(
            ["git", "add", decision_path.relative_to(self.root).as_posix(),
             path.relative_to(self.root).as_posix()], cwd=self.root, check=True,
        )
        subprocess.run(
            ["git", "commit", "-q", "-m", "freeze master release acceptance"],
            cwd=self.root, check=True,
        )
        self.base_revision = subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=self.root, check=True,
            text=True, capture_output=True,
        ).stdout.strip()
        return path

    def evaluate(self, receipt: dict | None = None, expected: str | None = None) -> dict:
        if receipt is not None:
            self.write(receipt)
        def replay(source: dict, **_kwargs: object) -> dict:
            authority = json.loads(
                (self.instance / "focus-eligibility.json").read_text()
            )["admission_authority"]["scheduler_verification"]
            result = dict(authority["kernel_authority_result"])
            result.update({
                "resolved_revision": authority["resolved_revision"],
                "archive_sha256": authority["archive_sha256"],
                "resolved_tree": authority["resolved_tree"],
                "kernel_stdout_sha256": authority["kernel_stdout_sha256"],
                "kernel_stderr_sha256": authority["kernel_stderr_sha256"],
            })
            return result
        def probe(checkout: Path, source: bytes, declaration: str) -> tuple[str, list[str], str]:
            authority = json.loads(
                (self.instance / "focus-eligibility.json").read_text()
            )["admission_authority"]["scheduler_verification"]["local_target_authority_result"]
            return (
                authority["declaration_type_sha256"],
                authority["permitted_axioms"],
                authority["trust_audit_output_sha256"],
            )
        receipt_path = self.instance / "focus-eligibility.json"
        local_replay_authority = (
            json.loads(receipt_path.read_text()).get("admission_authority")
            if receipt_path.is_file()
            else None
        )
        local_replay_authority = (
            local_replay_authority["scheduler_verification"]
            ["local_target_authority_result"]["replay_authority"]
            if local_replay_authority else {}
        )
        with mock.patch.object(focus, "_replay_external_authority", side_effect=replay), \
             mock.patch.object(focus, "_lean_probe", side_effect=probe), \
             mock.patch.object(focus, "_verify_local_pinned_provider"), \
             mock.patch.object(focus, "_replay_machine_transport_semantics"), \
             mock.patch.object(focus, "_validate_issuance_authority"), \
             mock.patch.object(
                 focus.stage1_lean_authority,
                 "build_repository_lean_authority",
                 return_value=(local_replay_authority, Path("/toolchain"), Path("/cache")),
             ), mock.patch.object(
                 focus, "TRUST_ANCHORS_SHA256", self.trust_anchor_sha
             ):
            return focus.evaluate_target(
                self.root, THEOREM, as_of=NOW,
                expected_receipt_sha256=expected,
            )


class FocusEligibilityTests(unittest.TestCase):
    def fixture(self) -> Fixture:
        fixture = Fixture()
        self.addCleanup(fixture.close)
        return fixture

    def test_missing_receipt_bootstraps_only_research_phases(self) -> None:
        result = self.fixture().evaluate()
        self.assertFalse(result["present"])
        self.assertFalse(result["valid"])
        self.assertEqual(result["reason_codes"], ["receipt_missing"])
        self.assertEqual(
            {phase for phase, allowed in result["phase_permissions"].items() if allowed},
            {"intake", "statement", "anchor_audit"},
        )
        self.assertTrue(focus.phase_allowed(result, "anchor_audit"))
        self.assertFalse(focus.phase_allowed(result, "proof"))

    def test_nonmember_target_never_bootstraps_or_validates(self) -> None:
        fixture = self.fixture()
        theorem_id = "THM-M-9999"
        result = focus.evaluate_target(fixture.root, theorem_id, as_of=NOW)
        self.assertFalse(result["present"])
        self.assertFalse(result["valid"])
        self.assertEqual(
            result["reason_codes"],
            ["theorem_id_outside_frozen_stage1_target_membership"],
        )
        self.assertFalse(any(result["phase_permissions"].values()))
        receipt = fixture.base_receipt()
        receipt["theorem_id"] = theorem_id
        with self.assertRaisesRegex(
            focus.EligibilityError, "outside frozen Stage1 target membership"
        ):
            focus.validate_receipt(fixture.root, theorem_id, receipt, as_of=NOW)

    def test_membership_bytes_are_bound_to_authoritative_head(self) -> None:
        fixture = self.fixture()
        membership = fixture.root / focus.TARGET_MEMBERSHIP_RELATIVE_PATH
        value = json.loads(membership.read_text(encoding="utf-8"))
        value["scope"]["legacy_priority_slots"] += 1
        membership.write_text(
            json.dumps(value, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        result = focus.evaluate_target(fixture.root, THEOREM, as_of=NOW)
        self.assertFalse(result["valid"])
        self.assertFalse(any(result["phase_permissions"].values()))
        self.assertTrue(
            any("differs_from_the_repository_base_revision" in reason
                for reason in result["reason_codes"]),
            result["reason_codes"],
        )

    def test_schema_bytes_are_bound_to_authoritative_head(self) -> None:
        fixture = self.fixture()
        schema_path = fixture.root / focus.SCHEMA_RELATIVE_PATH
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        schema["additionalProperties"] = True
        schema_path.write_text(
            json.dumps(schema, ensure_ascii=True, indent=2) + "\n",
            encoding="utf-8",
        )
        result = fixture.evaluate()
        self.assertFalse(result["valid"])
        self.assertFalse(any(result["phase_permissions"].values()))
        self.assertIn(
            "focus_eligibility_schema_differs_from_the_current_head_authority",
            result["reason_codes"],
        )

    def test_self_consistent_head_schema_rewrite_is_rejected(self) -> None:
        fixture = self.fixture()
        schema_path = fixture.root / focus.SCHEMA_RELATIVE_PATH
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        schema["additionalProperties"] = True
        schema_path.write_text(
            json.dumps(schema, ensure_ascii=True, indent=2) + "\n",
            encoding="utf-8",
        )
        subprocess.run(
            ["git", "add", focus.SCHEMA_RELATIVE_PATH], cwd=fixture.root, check=True
        )
        subprocess.run(
            ["git", "commit", "-q", "-m", "weaken focus schema"],
            cwd=fixture.root,
            check=True,
        )
        result = fixture.evaluate()
        self.assertFalse(result["valid"])
        self.assertFalse(any(result["phase_permissions"].values()))
        self.assertIn(
            "focus_eligibility_schema_differs_from_the_validator_pinned_contract",
            result["reason_codes"],
        )

    def test_self_consistent_head_membership_rewrite_is_rejected(self) -> None:
        fixture = self.fixture()
        membership = fixture.root / focus.TARGET_MEMBERSHIP_RELATIVE_PATH
        value = json.loads(membership.read_text(encoding="utf-8"))
        value["scope"]["legacy_priority_slots"] += 1
        membership.write_text(
            json.dumps(value, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        subprocess.run(
            ["git", "add", focus.TARGET_MEMBERSHIP_RELATIVE_PATH],
            cwd=fixture.root,
            check=True,
        )
        subprocess.run(
            ["git", "commit", "-q", "-m", "rewrite frozen membership"],
            cwd=fixture.root,
            check=True,
        )
        result = focus.evaluate_target(fixture.root, THEOREM, as_of=NOW)
        self.assertFalse(result["valid"])
        self.assertFalse(any(result["phase_permissions"].values()))
        self.assertEqual(
            result["reason_codes"],
            ["stage1_target_membership_is_malformed_or_stale"],
        )

    def test_valid_research_receipt_only_allows_intake_through_anchor_audit(self) -> None:
        fixture = self.fixture()
        result = fixture.evaluate(fixture.base_receipt())
        self.assertTrue(result["valid"], result["reason_codes"])
        self.assertEqual(
            {phase for phase, allowed in result["phase_permissions"].items() if allowed},
            {"intake", "statement", "anchor_audit"},
        )
        self.assertFalse(focus.phase_allowed(result, "proof"))

    def test_unknown_cannot_be_hidden_as_deferred_or_excluded(self) -> None:
        fixture = self.fixture()
        for disposition, decision in (
            ("defer_frontier", "defer"),
            ("exclude_scope", "exclude"),
        ):
            with self.subTest(disposition=disposition):
                receipt = fixture.base_receipt()
                receipt["execution_disposition"] = disposition
                receipt["admission_review"]["decision"] = decision
                result = fixture.evaluate(receipt)
                self.assertFalse(result["valid"])

    def test_terminal_defer_and_exclude_require_positive_typed_evidence(self) -> None:
        fixture = self.fixture()
        deferred = fixture.frontier_receipt()
        deferred["execution_disposition"] = "defer_frontier"
        deferred["frontier_exception"] = None
        deferred["admission_review"]["decision"] = "defer"
        boundary = deferred["machine_proof"]["negative_search_boundary"]
        snapshot = fixture.write_frontier_snapshot(boundary)
        defer_evidence = fixture.write_disposition_report(
            "no_current_frontier_exception",
            {
                "kind": "frontier_exception_snapshot",
                "search_boundary_sha256": snapshot["search_boundary_sha256"],
                "exception_snapshot_id": snapshot["snapshot_id"],
                "snapshot_path": snapshot["path"],
                "snapshot_sha256": snapshot["sha256"],
                "exception_policy_sha256": snapshot["exception_policy_sha256"],
                "exception_state": snapshot["exception_state"],
            },
        )
        deferred["repository_base_revision"] = fixture.base_revision
        deferred["evidence_bindings"].append(defer_evidence)
        deferred["disposition_basis"] = {
            "reason_code": "no_current_frontier_exception",
            "summary": "The bounded search found no exact candidate and no exception is current.",
            "evidence": [copy.deepcopy(defer_evidence)],
            "report_sha256": defer_evidence["sha256"],
        }
        self.assertTrue(fixture.evaluate(deferred)["valid"])

        excluded = fixture.base_receipt()
        excluded["execution_disposition"] = "exclude_scope"
        excluded["human_proof"]["status"] = "partial_or_open"
        excluded["admission_review"]["decision"] = "exclude"
        exclude_evidence = fixture.write_disposition_report(
            "human_claim_unproved_or_conjectural",
            {
                "kind": "open_claim_source_review",
                "source_citation": "Open Problems Register",
                "source_locator": "Entry THM-M-0001",
                "source_immutable_id": "snapshot:2026-05-31",
                "source_path": f"Stage1_Instances/{THEOREM}/{fixture.bound.name}",
                "source_content_sha256": fixture.digest(fixture.bound),
                "claim_status": "partial_or_open",
            },
        )
        excluded["repository_base_revision"] = fixture.base_revision
        excluded["evidence_bindings"].append(exclude_evidence)
        excluded["disposition_basis"] = {
            "reason_code": "human_claim_unproved_or_conjectural",
            "summary": "Independent source review confirms that the claim remains open.",
            "evidence": [copy.deepcopy(exclude_evidence)],
            "report_sha256": exclude_evidence["sha256"],
        }
        self.assertTrue(fixture.evaluate(excluded)["valid"])

    def test_terminal_disposition_rejects_arbitrary_text_with_a_typed_role(self) -> None:
        fixture = self.fixture()
        receipt = fixture.base_receipt()
        receipt["execution_disposition"] = "exclude_scope"
        receipt["admission_review"]["decision"] = "exclude"
        evidence = fixture.evidence("scope_exclusion_review")
        receipt["evidence_bindings"] = [evidence]
        receipt["disposition_basis"] = {
            "reason_code": "unusable_legal_boundary",
            "summary": "An unstructured assertion must not be terminal evidence.",
            "evidence": [copy.deepcopy(evidence)],
            "report_sha256": evidence["sha256"],
        }
        result = fixture.evaluate(receipt)
        self.assertFalse(result["valid"])
        self.assertIn("not_canonical_json", "_".join(result["reason_codes"]))

    def test_each_terminal_reason_requires_its_matching_structured_facts(self) -> None:
        fixture = self.fixture()
        cases = {
            "non_exact_umbrella": {
                "kind": "exact_boundary_comparison",
                "catalogue_statement_sha256": SHA_A,
                "candidate_statement_sha256": SHA_B,
                "comparison": "non_exact",
                "boundary_difference": "candidate omits a required hypothesis",
            },
            "unusable_legal_boundary": {
                "kind": "license_review",
                "artifact_path": f"Stage1_Instances/{THEOREM}/{fixture.bound.name}",
                "artifact_sha256": fixture.digest(fixture.bound),
                "license_identifier": "Proprietary-No-Redistribution",
                "integration_permitted": False,
            },
            "unusable_technical_boundary": {
                "kind": "reproducible_incompatibility",
                "reproduction_command": ["lake", "env", "lean", "Candidate.lean"],
                "exit_code": 1,
                "output_path": f"Stage1_Instances/{THEOREM}/{fixture.bound.name}",
                "output_sha256": fixture.digest(fixture.bound),
                "toolchain": "leanprover/lean4:v4.19.0",
                "dependency_lock_sha256": SHA_B,
                "incompatibility": "requires an incompatible kernel version",
            },
        }
        for reason, facts in cases.items():
            with self.subTest(reason=reason):
                receipt = fixture.base_receipt()
                receipt["execution_disposition"] = "exclude_scope"
                receipt["admission_review"]["decision"] = "exclude"
                if reason == "non_exact_umbrella":
                    receipt["human_proof"]["statement_fingerprint"] = SHA_A
                evidence = fixture.write_disposition_report(reason, facts)
                receipt["repository_base_revision"] = fixture.base_revision
                receipt["evidence_bindings"] = [evidence]
                receipt["disposition_basis"] = {
                    "reason_code": reason,
                    "summary": "Typed independent disposition review.",
                    "evidence": [copy.deepcopy(evidence)],
                    "report_sha256": evidence["sha256"],
                }
                self.assertTrue(fixture.evaluate(receipt)["valid"])

                if reason != "unusable_legal_boundary":
                    wrong = copy.deepcopy(receipt)
                    wrong["disposition_basis"]["reason_code"] = (
                        "unusable_legal_boundary"
                    )
                    self.assertFalse(fixture.evaluate(wrong)["valid"])

    def test_accepted_root_exclusion_requires_a_real_master_release_receipt(self) -> None:
        fixture = self.fixture()
        master = fixture.instance / "master-release-receipt.json"
        master.write_text(
            json.dumps(
                {
                    "schema_version": "stage1-master-phase-acceptance/1.0",
                    "theorem_id": THEOREM,
                    "phase": "release",
                    "phase_evidence_accepted": True,
                    "theorem_complete": True,
                },
                ensure_ascii=True,
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
        subprocess.run(
            ["git", "add", master.relative_to(fixture.root).as_posix()],
            cwd=fixture.root,
            check=True,
        )
        subprocess.run(
            ["git", "commit", "-q", "-m", "freeze master release receipt"],
            cwd=fixture.root,
            check=True,
        )
        fixture.base_revision = subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=fixture.root, check=True,
            text=True, capture_output=True,
        ).stdout.strip()
        facts = {
            "kind": "accepted_root_receipt",
            "master_receipt_id": "master-release-1",
            "master_receipt_path": f"Stage1_Instances/{THEOREM}/{master.name}",
            "master_receipt_sha256": fixture.digest(master),
            "root_statement_sha256": SHA_A,
            "acceptance_status": "master_accepted",
        }
        evidence = fixture.write_disposition_report(
            "already_locally_accepted_root", facts
        )
        receipt = fixture.base_receipt()
        receipt["repository_base_revision"] = fixture.base_revision
        receipt["execution_disposition"] = "exclude_scope"
        receipt["admission_review"]["decision"] = "exclude"
        receipt["target_binding"].update(
            status="verified",
            formal_system="Lean 4",
            path=f"Stage1_Instances/{THEOREM}/{fixture.target.name}",
            file_sha256=fixture.digest(fixture.target),
            declaration="Stage1.THM_M_0001.target",
            declaration_type_sha256=SHA_A,
        )
        receipt["repository_gap"].update(
            acceptance_status="master_accepted",
            local_presence="repository_accepted",
        )
        receipt["evidence_bindings"] = [evidence]
        receipt["disposition_basis"] = {
            "reason_code": "already_locally_accepted_root",
            "summary": "The exact root already has a master-accepted release receipt.",
            "evidence": [copy.deepcopy(evidence)],
            "report_sha256": evidence["sha256"],
        }
        self.assertTrue(fixture.evaluate(receipt)["valid"])

        master.write_text("{}\n", encoding="utf-8")
        receipt["repository_base_revision"] = fixture.base_revision
        self.assertFalse(fixture.evaluate(receipt)["valid"])

    def test_exact_external_machine_proof_enables_integration_phases(self) -> None:
        fixture = self.fixture()
        result = fixture.evaluate(fixture.exact_receipt())
        self.assertTrue(result["valid"], result["reason_codes"])
        self.assertEqual(result["execution_disposition"], "organize_or_integrate")
        self.assertTrue(all(result["phase_permissions"].values()))
        self.assertIsNone(result["frontier_policy"])

    def test_timestamp_and_human_source_authority_tampering_fails_closed(self) -> None:
        fixture = self.fixture()
        receipt = fixture.exact_receipt()
        provenance = json.loads(fixture.external_provenance.read_text())
        provenance["publication"]["timestamp"]["issued_at"] = "2026-05-29T20:00:00Z"
        provenance["provenance_sha256"] = hashlib.sha256(
            json.dumps(
                {key: value for key, value in provenance.items() if key != "provenance_sha256"},
                ensure_ascii=True,
                sort_keys=True,
                separators=(",", ":"),
            ).encode()
        ).hexdigest()
        fixture.external_provenance.write_text(
            json.dumps(provenance, ensure_ascii=True, indent=2) + "\n",
            encoding="utf-8",
        )
        subprocess.run(
            ["git", "add", fixture.external_provenance.relative_to(fixture.root).as_posix()],
            cwd=fixture.root,
            check=True,
        )
        subprocess.run(
            ["git", "commit", "-q", "-m", "forge retroactive publication time"],
            cwd=fixture.root,
            check=True,
        )
        receipt["repository_base_revision"] = subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=fixture.root, check=True,
            text=True, capture_output=True,
        ).stdout.strip()
        row = next(
            item for item in receipt["evidence_bindings"]
            if item["role"] == focus.EXTERNAL_PROVENANCE_ROLE
        )
        row["sha256"] = fixture.digest(fixture.external_provenance)
        receipt["machine_proof"]["source"]["pre_stage1_provenance"].update(
            sha256=row["sha256"], provenance_sha256=provenance["provenance_sha256"]
        )
        result = fixture.evaluate(receipt)
        self.assertFalse(result["valid"])
        self.assertIn("signature", "_".join(result["reason_codes"]))

        fixture = self.fixture()
        receipt = fixture.exact_receipt()
        for principal in ("scheduler_verification", "reviewer_verification"):
            support = receipt["admission_authority"][principal]["human_source_review"]
            support["statement_crosswalk"]["relation"] = "similar"
            verification = receipt["admission_authority"][principal]
            verification["verification_sha256"] = hashlib.sha256(
                json.dumps(
                    {key: value for key, value in verification.items()
                     if key != "verification_sha256"},
                    ensure_ascii=True, sort_keys=True, separators=(",", ":"),
                ).encode()
            ).hexdigest()
        result = fixture.evaluate(receipt)
        self.assertFalse(result["valid"])

    def test_no_machine_proof_cannot_masquerade_as_integration(self) -> None:
        fixture = self.fixture()
        receipt = fixture.exact_receipt()
        receipt["machine_proof"] = {
            "status": "unknown",
            "negative_search_boundary": None,
            "source": None,
        }
        result = fixture.evaluate(receipt)
        self.assertFalse(result["valid"])
        self.assertEqual(result["machine_evidence_class"], "unknown")
        self.assertEqual(result["execution_disposition"], "research_required")
        self.assertFalse(focus.phase_allowed(result, "proof"))

    def test_frontier_exception_at_threshold_with_independent_review_is_admitted(self) -> None:
        fixture = self.fixture()
        result = fixture.evaluate(fixture.frontier_receipt())
        self.assertTrue(result["valid"], result["reason_codes"])
        self.assertEqual(result["execution_disposition"], "frontier_exception")
        self.assertTrue(focus.phase_allowed(result, "proof"))
        policy = result["frontier_policy"]
        self.assertEqual(policy["assigned_worker_id"], "proof-worker-1")
        self.assertEqual(policy["completion_probability"], 0.70)
        self.assertEqual(
            policy["validator"],
            fixture.frontier_receipt()["frontier_exception"]["validator"],
        )
        unhashed = dict(policy)
        embedded = unhashed.pop("policy_sha256")
        self.assertEqual(
            embedded,
            hashlib.sha256(
                json.dumps(
                    unhashed, ensure_ascii=True, sort_keys=True, separators=(",", ":")
                ).encode("utf-8")
            ).hexdigest(),
        )

    def test_exact_pinned_closure_requires_manifest_bound_package_cache(self) -> None:
        fixture = self.fixture()
        receipt = fixture.exact_receipt()
        receipt["machine_evidence_class"] = "exact_pinned_closure"
        receipt["repository_gap"]["local_presence"] = "pinned_dependency"
        manifest_sha = fixture.digest(fixture.manifest)
        for principal in ("scheduler_verification", "reviewer_verification"):
            authority = receipt["admission_authority"][principal][
                "kernel_authority_result"
            ]["replay_authority"]
            authority["dependency_packages_sha256"] = None
            authority["compiled_cache_sha256"] = None
            authority["compiled_cache_file_count"] = 0
            receipt["admission_authority"][principal][
                "local_target_authority_result"
            ]["replay_authority"]["dependency_lock_sha256"] = manifest_sha
            verification = receipt["admission_authority"][principal]
            verification.pop("verification_sha256")
            verification["verification_sha256"] = hashlib.sha256(
                json.dumps(
                    verification,
                    ensure_ascii=True,
                    sort_keys=True,
                    separators=(",", ":"),
                ).encode()
            ).hexdigest()
        scheduler = receipt["admission_authority"]["scheduler_verification"]
        receipt["admission_authority"]["observed_facts_sha256"] = hashlib.sha256(
            json.dumps(
                {
                    "external": scheduler["kernel_authority_result"],
                    "local_target": scheduler["local_target_authority_result"],
                },
                ensure_ascii=True,
                sort_keys=True,
                separators=(",", ":"),
            ).encode()
        ).hexdigest()
        result = fixture.evaluate(receipt)
        self.assertFalse(result["valid"])
        self.assertFalse(focus.phase_allowed(result, "proof"))
        self.assertIn("verified_lake_manifest", "_".join(result["reason_codes"]))

    def test_exact_pinned_closure_requires_pre_cutoff_proof_bytes(self) -> None:
        fixture = self.fixture()
        receipt = fixture.configure_pinned_transport_receipt(fixture.exact_receipt())
        receipt["admission_authority"] = fixture.authority_for(receipt)
        self.assertTrue(fixture.evaluate(receipt)["valid"])

        missing = copy.deepcopy(receipt)
        del missing["machine_proof"]["source"]["pre_stage1_provenance"]
        missing["evidence_bindings"] = [
            row for row in missing["evidence_bindings"]
            if row["role"] != focus.EXTERNAL_PROVENANCE_ROLE
        ]
        result = fixture.evaluate(missing)
        self.assertFalse(result["valid"])
        self.assertIn("schema_invalid", result["reason_codes"])

        fixture = self.fixture()
        post_cutoff = fixture.configure_pinned_transport_receipt(fixture.exact_receipt())
        fixture.rewrite_machine_provenance_timestamp(
            post_cutoff,
            issued_at="2026-07-15T20:32:22Z",
            reviewed_at="2026-07-15T20:32:23Z",
        )
        post_cutoff["evidence_as_of"] = "2026-07-15T20:32:24Z"
        post_cutoff["generated_at"] = "2026-07-15T20:32:25Z"
        post_cutoff["admission_review"]["reviewed_at"] = "2026-07-15T20:32:24Z"
        post_cutoff["admission_authority"] = fixture.authority_for(post_cutoff)
        fixture.write(post_cutoff)
        with self.assertRaisesRegex(
            focus.EligibilityError, "issued after the Stage1 provenance cutoff"
        ):
            with mock.patch.object(focus, "TRUST_ANCHORS_SHA256", fixture.trust_anchor_sha):
                focus._validate_machine_pre_stage1_provenance(
                    fixture.root,
                    post_cutoff,
                    post_cutoff["machine_proof"]["source"],
                )

    def test_probability_below_threshold_is_rejected(self) -> None:
        fixture = self.fixture()
        receipt = fixture.frontier_receipt()
        receipt["frontier_exception"]["completion_probability"] = 0.699
        result = fixture.evaluate(receipt)
        self.assertFalse(result["valid"])
        self.assertIn("schema_invalid", result["reason_codes"])

    def test_frontier_review_probability_and_substance_are_durable(self) -> None:
        fixture = self.fixture()
        receipt = fixture.frontier_receipt()
        review = receipt["frontier_exception"]["independent_review"]
        self.assertEqual(review["assessed_completion_probability"], 0.70)
        self.assertEqual(len(review["comparables"]), 2)
        self.assertTrue(review["findings"])
        self.assertEqual(
            review["budget_assessment"],
            receipt["frontier_exception"]["budget"],
        )
        self.assertTrue(fixture.evaluate(receipt)["valid"])

        for field, replacement in (
            ("assessed_completion_probability", 0.69),
            ("comparables", []),
            ("findings", []),
        ):
            with self.subTest(field=field):
                tampered = copy.deepcopy(receipt)
                tampered["frontier_exception"]["independent_review"][field] = replacement
                result = fixture.evaluate(tampered)
                self.assertFalse(result["valid"])
                self.assertFalse(focus.phase_allowed(result, "proof"))

    def test_frontier_review_digest_and_control_assessments_are_revalidated(self) -> None:
        fixture = self.fixture()
        receipt = fixture.frontier_receipt()
        for field, replacement in (
            ("review_input_sha256", SHA_B),
            (
                "budget_assessment",
                {
                    **receipt["frontier_exception"]["budget"],
                    "token_limit": 1,
                },
            ),
            ("milestone_assessment", []),
            (
                "validator_assessment",
                {
                    **receipt["frontier_exception"]["validator"],
                    "sha256": SHA_B,
                },
            ),
            ("stop_condition_assessment", ["scheduler_revoked"]),
        ):
            with self.subTest(field=field):
                tampered = copy.deepcopy(receipt)
                tampered["frontier_exception"]["independent_review"][field] = replacement
                result = fixture.evaluate(tampered)
                self.assertFalse(result["valid"])
                self.assertFalse(focus.phase_allowed(result, "proof"))

    def test_nonfinite_probability_is_not_valid_json_evidence(self) -> None:
        fixture = self.fixture()
        receipt = fixture.frontier_receipt()
        path = fixture.instance / "focus-eligibility.json"
        payload = json.dumps(receipt, ensure_ascii=True, indent=2).replace(
            '"completion_probability": 0.7', '"completion_probability": NaN'
        )
        path.write_text(payload + "\n", encoding="utf-8")
        result = fixture.evaluate()
        self.assertFalse(result["valid"])
        self.assertEqual(result["reason_codes"], ["receipt_not_canonical_json"])

    def test_malformed_receipt_opens_no_phase(self) -> None:
        fixture = self.fixture()
        receipt = fixture.base_receipt()
        del receipt["admission_review"]
        result = fixture.evaluate(receipt)
        self.assertTrue(result["present"])
        self.assertFalse(result["valid"])
        self.assertFalse(any(result["phase_permissions"].values()))
        self.assertFalse(focus.phase_allowed(result, "anchor_audit"))

    def test_worker_authored_probability_is_rejected(self) -> None:
        fixture = self.fixture()
        receipt = fixture.frontier_receipt()
        receipt["frontier_exception"]["estimator"] = {
            "id": "worker-7",
            "role": "worker_self_assessment",
        }
        result = fixture.evaluate(receipt)
        self.assertFalse(result["valid"])
        self.assertFalse(focus.phase_allowed(result, "proof"))

    def test_same_estimator_and_reviewer_is_not_independent(self) -> None:
        fixture = self.fixture()
        receipt = fixture.frontier_receipt()
        receipt["frontier_exception"]["independent_review"]["reviewer"]["id"] = (
            "scheduler-estimator-1"
        )
        result = fixture.evaluate(receipt)
        self.assertFalse(result["valid"])

    def test_frontier_exception_requires_bounded_budget_and_stop_conditions(self) -> None:
        fixture = self.fixture()
        receipt = fixture.frontier_receipt()
        receipt["frontier_exception"]["budget"]["token_limit"] = 0
        receipt["frontier_exception"]["stop_conditions"] = []
        result = fixture.evaluate(receipt)
        self.assertFalse(result["valid"])
        self.assertFalse(focus.phase_allowed(result, "proof"))

    def test_frontier_exception_requires_bound_validator_and_current_lease(self) -> None:
        fixture = self.fixture()
        receipt = fixture.frontier_receipt()
        receipt["frontier_exception"]["validator"]["sha256"] = SHA_A
        result = fixture.evaluate(receipt)
        self.assertFalse(result["valid"])

    def test_frontier_validator_command_is_exact_bound_python_argv(self) -> None:
        fixture = self.fixture()
        for command in (
            ["python3", "check_frontier.py"],
            ["python3", f"Stage1_Instances/{THEOREM}/{fixture.bound.name}", "--ok"],
            ["sh", f"Stage1_Instances/{THEOREM}/{fixture.bound.name}"],
        ):
            with self.subTest(command=command):
                receipt = fixture.frontier_receipt()
                receipt["frontier_exception"]["validator"]["command"] = command
                result = fixture.evaluate(receipt)
                self.assertFalse(result["valid"])
                self.assertFalse(focus.phase_allowed(result, "proof"))
        receipt = fixture.frontier_receipt()
        receipt["frontier_exception"]["lease_expires_at"] = "2026-05-31T22:00:00Z"
        result = fixture.evaluate(receipt)
        self.assertFalse(result["valid"])

    def test_frontier_lease_that_expired_after_review_is_rejected_at_as_of(self) -> None:
        fixture = self.fixture()
        receipt = fixture.frontier_receipt()
        receipt["frontier_exception"]["lease_expires_at"] = "2026-05-31T23:45:00Z"
        result = fixture.evaluate(receipt)
        self.assertFalse(result["valid"])
        self.assertIn("lease_is_expired", "_".join(result["reason_codes"]))

    def test_frontier_lease_expiring_exactly_at_as_of_is_rejected(self) -> None:
        fixture = self.fixture()
        receipt = fixture.frontier_receipt()
        receipt["frontier_exception"]["lease_expires_at"] = "2026-06-01T00:00:00Z"
        result = fixture.evaluate(receipt)
        self.assertFalse(result["valid"])

    def test_frontier_root_obligation_binds_human_statement(self) -> None:
        fixture = self.fixture()
        receipt = fixture.frontier_receipt()
        receipt["frontier_exception"]["root_obligation"]["statement_fingerprint"] = SHA_B
        result = fixture.evaluate(receipt)
        self.assertFalse(result["valid"])

    def test_human_statement_must_match_exact_target_and_machine_chain(self) -> None:
        fixture = self.fixture()
        receipt = fixture.exact_receipt()
        receipt["human_proof"]["statement_fingerprint"] = SHA_C
        result = fixture.evaluate(receipt)
        self.assertFalse(result["valid"])
        self.assertIn(
            "statement_binding_does_not_bind_the_accepted_human_and_target_fingerprints",
            result["reason_codes"],
        )

    def test_frontier_human_statement_must_match_exact_target(self) -> None:
        fixture = self.fixture()
        receipt = fixture.frontier_receipt()
        receipt["target_binding"]["declaration_type_sha256"] = SHA_C
        result = fixture.evaluate(receipt)
        self.assertFalse(result["valid"])

    def test_human_to_target_label_only_transport_rejects_nonidentical_fingerprints(self) -> None:
        fixture = self.fixture()
        receipt = fixture.exact_receipt()
        transport = fixture.evidence("statement_match")
        transport["evidence_kind"] = "machine_checked_statement_transport"
        receipt["human_proof"]["statement_fingerprint"] = SHA_C
        receipt["statement_binding"] = {
            "human_statement_fingerprint": SHA_C,
            "target_declaration_type_sha256": SHA_A,
            "match_kind": "checked_transport",
            "evidence": [copy.deepcopy(transport)],
        }
        receipt["evidence_bindings"].append(transport)
        result = fixture.evaluate(receipt)
        self.assertFalse(result["valid"])
        self.assertIn("schema_invalid", result["reason_codes"])

    def test_human_to_target_transport_without_typed_machine_evidence_fails(self) -> None:
        fixture = self.fixture()
        receipt = fixture.exact_receipt()
        transport = fixture.evidence("statement_match")
        receipt["human_proof"]["statement_fingerprint"] = SHA_C
        receipt["statement_binding"] = {
            "human_statement_fingerprint": SHA_C,
            "target_declaration_type_sha256": SHA_A,
            "match_kind": "checked_transport",
            "evidence": [copy.deepcopy(transport)],
        }
        result = fixture.evaluate(receipt)
        self.assertFalse(result["valid"])

    def test_checked_transport_requires_distinct_types_and_bound_transport(self) -> None:
        fixture = self.fixture()
        receipt = fixture.configure_pinned_transport_receipt(fixture.exact_receipt())
        source = receipt["machine_proof"]["source"]
        source["match_kind"] = "checked_transport"
        source["declaration_type_sha256"] = SHA_C
        fixture.rebind_machine_provenance(receipt)
        transport = fixture.machine_transport_evidence()
        source["transport_evidence"] = [transport]
        receipt["evidence_bindings"].append(
            {key: transport[key] for key in ("path", "sha256", "role", "evidence_kind")}
        )
        receipt["admission_authority"] = fixture.authority_for(receipt)
        result = fixture.evaluate(receipt)
        self.assertTrue(result["valid"], result["reason_codes"])

        source["declaration_type_sha256"] = SHA_A
        result = fixture.evaluate(receipt)
        self.assertFalse(result["valid"])

        source["declaration_type_sha256"] = SHA_C
        source["transport_evidence"][0]["sha256"] = SHA_A
        result = fixture.evaluate(receipt)
        self.assertFalse(result["valid"])

    def test_machine_transport_must_bind_exact_source_and_target_identities(self) -> None:
        fixture = self.fixture()
        receipt = fixture.configure_pinned_transport_receipt(fixture.exact_receipt())
        source = receipt["machine_proof"]["source"]
        source["match_kind"] = "checked_transport"
        source["declaration_type_sha256"] = SHA_C
        fixture.rebind_machine_provenance(receipt)
        transport = fixture.machine_transport_evidence()
        source["transport_evidence"] = [transport]
        receipt["evidence_bindings"].append(
            {key: transport[key] for key in ("path", "sha256", "role", "evidence_kind")}
        )
        receipt["admission_authority"] = fixture.authority_for(receipt)
        self.assertTrue(fixture.evaluate(receipt)["valid"])

        source["transport_evidence"][0]["target_declaration_type_sha256"] = SHA_B
        result = fixture.evaluate(receipt)
        self.assertFalse(result["valid"])

    def test_embedded_machine_transport_semantics_are_required_and_digest_bound(self) -> None:
        fixture = self.fixture()
        receipt = fixture.configure_pinned_transport_receipt(fixture.exact_receipt())
        source = receipt["machine_proof"]["source"]
        source["match_kind"] = "checked_transport"
        source["declaration_type_sha256"] = SHA_C
        fixture.rebind_machine_provenance(receipt)
        transport = fixture.machine_transport_evidence()
        source["transport_evidence"] = [transport]
        receipt["evidence_bindings"].append(
            {key: transport[key] for key in ("path", "sha256", "role", "evidence_kind")}
        )
        receipt["admission_authority"] = fixture.authority_for(receipt)
        self.assertTrue(fixture.evaluate(receipt)["valid"])

        for principal in ("scheduler_verification", "reviewer_verification"):
            verification = receipt["admission_authority"][principal]
            verification["human_source_review"] = None
            verification["verification_sha256"] = hashlib.sha256(
                json.dumps(
                    {
                        key: value
                        for key, value in verification.items()
                        if key != "verification_sha256"
                    },
                    ensure_ascii=True,
                    sort_keys=True,
                    separators=(",", ":"),
                ).encode()
            ).hexdigest()
        result = fixture.evaluate(receipt)
        self.assertFalse(result["valid"])
        joined = "_".join(result["reason_codes"])
        self.assertTrue(
            any(
                expected in joined
                for expected in (
                    "semantic_replay_authority",
                    "replayable_human_source_review",
                )
            ),
            result["reason_codes"],
        )

        receipt["admission_authority"] = fixture.authority_for(receipt)
        for principal in ("scheduler_verification", "reviewer_verification"):
            verification = receipt["admission_authority"][principal]
            embedded = verification["human_source_review"][
                "machine_transport_authority"
            ]
            embedded["semantic_dependency"]["relation"] = "label_only"
            verification["verification_sha256"] = hashlib.sha256(
                json.dumps(
                    {
                        key: value
                        for key, value in verification.items()
                        if key != "verification_sha256"
                    },
                    ensure_ascii=True,
                    sort_keys=True,
                    separators=(",", ":"),
                ).encode()
            ).hexdigest()
        result = fixture.evaluate(receipt)
        self.assertFalse(result["valid"])
        self.assertIn("does_not_bind_its_content", "_".join(result["reason_codes"]))

        source["transport_evidence"][0] = fixture.evidence("statement_match")
        result = fixture.evaluate(receipt)
        self.assertFalse(result["valid"])

    def test_machine_transport_requires_structured_replay_not_an_arbitrary_blob(self) -> None:
        fixture = self.fixture()
        receipt = fixture.configure_pinned_transport_receipt(fixture.exact_receipt())
        source = receipt["machine_proof"]["source"]
        source["match_kind"] = "checked_transport"
        source["declaration_type_sha256"] = SHA_C
        fixture.rebind_machine_provenance(receipt)
        transport = fixture.machine_transport_evidence()
        transport["path"] = f"Stage1_Instances/{THEOREM}/{fixture.bound.name}"
        transport["sha256"] = fixture.digest(fixture.bound)
        transport["replay_receipt_sha256"] = fixture.digest(fixture.bound)
        source["transport_evidence"] = [transport]
        receipt["admission_authority"] = fixture.authority_for(receipt)
        receipt["evidence_bindings"].append(
            {key: transport[key] for key in ("path", "sha256", "role", "evidence_kind")}
        )
        result = fixture.evaluate(receipt)
        self.assertFalse(result["valid"])
        self.assertIn("not_canonical_json", "_".join(result["reason_codes"]))

    def test_machine_transport_replay_is_identity_authority_and_trust_bound(self) -> None:
        fixture = self.fixture()

        def result_for(**updates: object) -> dict:
            fixture.write_machine_transport_receipt(**updates)
            receipt = fixture.configure_pinned_transport_receipt(fixture.exact_receipt())
            source = receipt["machine_proof"]["source"]
            source["match_kind"] = "checked_transport"
            source["declaration_type_sha256"] = SHA_C
            fixture.rebind_machine_provenance(receipt)
            transport = fixture.machine_transport_evidence()
            source["transport_evidence"] = [transport]
            receipt["evidence_bindings"].append(
                {key: transport[key] for key in ("path", "sha256", "role", "evidence_kind")}
            )
            receipt["admission_authority"] = fixture.authority_for(receipt)
            return fixture.evaluate(receipt)

        self.assertTrue(result_for()["valid"])
        self.assertFalse(
            result_for(
                source={
                    "formal_system": "Lean 4",
                    "declaration": "Related.NarrowerTheorem",
                    "declaration_type_sha256": SHA_C,
                }
            )["valid"]
        )
        fixture.write_machine_transport_receipt()
        replay = json.loads(fixture.transport_receipt.read_text(encoding="utf-8"))
        replay["validator"]["authority"] = "proof_worker"
        self.assertFalse(result_for(**replay)["valid"])
        fixture.write_machine_transport_receipt()
        replay = json.loads(fixture.transport_receipt.read_text(encoding="utf-8"))
        replay["trust_audit"]["placeholder_free"] = False
        self.assertFalse(result_for(**replay)["valid"])

    def test_repository_base_revision_must_exist_and_be_reachable(self) -> None:
        fixture = self.fixture()
        receipt = fixture.exact_receipt()
        receipt["repository_base_revision"] = "f" * 40
        result = fixture.evaluate(receipt)
        self.assertFalse(result["valid"])
        self.assertIn("cannot_be_resolved_by_git", "_".join(result["reason_codes"]))

    def test_repository_bound_file_must_equal_base_revision_blob(self) -> None:
        fixture = self.fixture()
        receipt = fixture.exact_receipt()
        fixture.target.write_text("theorem target : False := by contradiction\n", encoding="utf-8")
        receipt["target_binding"]["file_sha256"] = fixture.digest(fixture.target)
        result = fixture.evaluate(receipt)
        self.assertFalse(result["valid"])
        self.assertIn("differs_from_the_repository_base_revision", "_".join(result["reason_codes"]))

    def test_repository_base_revision_must_be_ancestor_of_current_head(self) -> None:
        fixture = self.fixture()
        receipt = fixture.exact_receipt()
        unrelated = subprocess.run(
            ["git", "commit-tree", "-m", "unrelated", f"{fixture.base_revision}^{{tree}}"],
            cwd=fixture.root,
            check=True,
            text=True,
            capture_output=True,
        ).stdout.strip()
        subprocess.run(
            ["git", "update-ref", "refs/heads/unrelated", unrelated],
            cwd=fixture.root,
            check=True,
        )
        subprocess.run(
            ["git", "symbolic-ref", "HEAD", "refs/heads/unrelated"],
            cwd=fixture.root,
            check=True,
        )
        marker = fixture.root / "unrelated.txt"
        marker.write_text("unrelated history\n", encoding="utf-8")
        result = fixture.evaluate(receipt)
        self.assertFalse(result["valid"])
        self.assertIn("not_reachable_from_current_head", "_".join(result["reason_codes"]))

    def test_frontier_assignee_must_be_independent_from_estimator_and_reviewer(self) -> None:
        fixture = self.fixture()
        receipt = fixture.frontier_receipt()
        receipt["frontier_exception"]["assigned_worker"]["id"] = "scheduler-estimator-1"
        result = fixture.evaluate(receipt)
        self.assertFalse(result["valid"])
        receipt = fixture.frontier_receipt()
        receipt["frontier_exception"]["assigned_worker"]["id"] = "frontier-reviewer-1"
        result = fixture.evaluate(receipt)
        self.assertFalse(result["valid"])

    def test_frontier_budget_requires_every_finite_resource_dimension(self) -> None:
        fixture = self.fixture()
        for field in (
            "wall_clock_seconds",
            "token_limit",
            "compute_seconds",
            "disk_bytes",
            "concurrency_limit",
        ):
            with self.subTest(field=field):
                receipt = fixture.frontier_receipt()
                del receipt["frontier_exception"]["budget"][field]
                result = fixture.evaluate(receipt)
                self.assertFalse(result["valid"])

    def test_frontier_budget_and_attempts_have_operational_policy_maxima(self) -> None:
        fixture = self.fixture()
        for field, maximum in focus.MAX_FRONTIER_BUDGET.items():
            with self.subTest(field=field):
                receipt = fixture.frontier_receipt()
                receipt["frontier_exception"]["budget"][field] = maximum + 1
                result = fixture.evaluate(receipt)
                self.assertFalse(result["valid"])
        receipt = fixture.frontier_receipt()
        receipt["frontier_exception"]["attempt_limit"] = focus.MAX_FRONTIER_ATTEMPTS + 1
        result = fixture.evaluate(receipt)
        self.assertFalse(result["valid"])

    def test_frontier_lease_duration_has_an_operational_policy_maximum(self) -> None:
        fixture = self.fixture()
        receipt = fixture.frontier_receipt()
        receipt["frontier_exception"]["lease_expires_at"] = "2026-07-02T00:00:00Z"
        result = fixture.evaluate(receipt)
        self.assertFalse(result["valid"])

    def test_frontier_requires_the_complete_closed_stop_condition_set(self) -> None:
        fixture = self.fixture()
        receipt = fixture.frontier_receipt()
        receipt["frontier_exception"]["stop_conditions"].remove("scheduler_revoked")
        result = fixture.evaluate(receipt)
        self.assertFalse(result["valid"])
        receipt = fixture.frontier_receipt()
        receipt["frontier_exception"]["stop_conditions"].append("worker_feels_done")
        result = fixture.evaluate(receipt)
        self.assertFalse(result["valid"])

    def test_frontier_milestones_are_unique_ordered_and_inside_lease(self) -> None:
        fixture = self.fixture()
        receipt = fixture.frontier_receipt()
        receipt["frontier_exception"]["milestones"][1]["id"] = "close_root"
        result = fixture.evaluate(receipt)
        self.assertFalse(result["valid"])

        receipt = fixture.frontier_receipt()
        receipt["frontier_exception"]["milestones"][1]["deadline_at"] = (
            "2026-06-01T07:00:00Z"
        )
        result = fixture.evaluate(receipt)
        self.assertFalse(result["valid"])

        receipt = fixture.frontier_receipt()
        receipt["frontier_exception"]["milestones"][1]["deadline_at"] = (
            "2026-06-02T01:00:00Z"
        )
        result = fixture.evaluate(receipt)
        self.assertFalse(result["valid"])

    def test_negative_search_requires_structured_bounded_inventory(self) -> None:
        fixture = self.fixture()
        receipt = fixture.frontier_receipt()
        receipt["machine_proof"]["negative_search_inventory"] = []
        result = fixture.evaluate(receipt)
        self.assertFalse(result["valid"])

    def test_negative_search_never_becomes_a_global_nonexistence_claim(self) -> None:
        fixture = self.fixture()
        receipt = fixture.frontier_receipt()
        receipt["machine_proof"]["negative_search_boundary"] = ""
        result = fixture.evaluate(receipt)
        self.assertFalse(result["valid"])

    def test_already_master_accepted_proof_is_not_integration_debt(self) -> None:
        fixture = self.fixture()
        receipt = fixture.exact_receipt()
        receipt["repository_gap"]["acceptance_status"] = "master_accepted"
        receipt["repository_gap"]["local_presence"] = "repository_accepted"
        result = fixture.evaluate(receipt)
        self.assertFalse(result["valid"])
        self.assertFalse(focus.phase_allowed(result, "release"))

    def test_current_master_release_acceptance_blocks_ordinary_integration(self) -> None:
        fixture = self.fixture()
        receipt = fixture.exact_receipt()
        fixture.write_master_release_acceptance()
        fixture.set_release_state("[x]")
        result = fixture.evaluate(receipt)
        self.assertFalse(result["valid"])
        self.assertIn("already_master_accepted_root", "_".join(result["reason_codes"]))

    def test_release_x_without_master_receipt_fails_closed(self) -> None:
        fixture = self.fixture()
        receipt = fixture.exact_receipt()
        fixture.set_release_state("[x]")
        result = fixture.evaluate(receipt)
        self.assertFalse(result["valid"])
        self.assertIn("content_addressed_receipt", "_".join(result["reason_codes"]))

    def test_master_receipt_without_release_x_does_not_manufacture_acceptance(self) -> None:
        fixture = self.fixture()
        fixture.write_master_release_acceptance()
        self.assertFalse(focus.current_master_release_acceptance(fixture.root, THEOREM))

    def test_historical_worker_release_decision_is_not_master_acceptance(self) -> None:
        fixture = self.fixture()
        (fixture.instance / "release-decision.json").write_text(
            json.dumps({"verdict": "accepted"}, ensure_ascii=True, indent=2) + "\n",
            encoding="utf-8",
        )
        subprocess.run(
            ["git", "add", f"Stage1_Instances/{THEOREM}/release-decision.json"],
            cwd=fixture.root, check=True,
        )
        subprocess.run(
            ["git", "commit", "-q", "-m", "historical worker decision"],
            cwd=fixture.root, check=True,
        )
        self.assertFalse(focus.current_master_release_acceptance(fixture.root, THEOREM))

    def test_tampered_master_release_receipt_fails_closed(self) -> None:
        fixture = self.fixture()
        path = fixture.write_master_release_acceptance()
        fixture.set_release_state("[x]")
        value = json.loads(path.read_text(encoding="utf-8"))
        value["theorem_complete"] = False
        path.write_bytes(focus._master_canonical_json(value) + b"\n")
        with self.assertRaisesRegex(
            focus.EligibilityError, "content-addressed"
        ):
            focus.current_master_release_acceptance(fixture.root, THEOREM)

    def test_exact_machine_source_must_match_target_type(self) -> None:
        fixture = self.fixture()
        receipt = fixture.exact_receipt()
        receipt["machine_proof"]["source"]["declaration_type_sha256"] = SHA_C
        result = fixture.evaluate(receipt)
        self.assertFalse(result["valid"])

    def test_changed_toolchain_between_replay_and_compatibility_is_rejected(self) -> None:
        fixture = self.fixture()
        receipt = fixture.exact_receipt()
        receipt["machine_proof"]["source"]["compatibility"]["toolchain"] = "Lean 3"
        result = fixture.evaluate(receipt)
        self.assertFalse(result["valid"])

    def test_expired_receipt_is_rejected(self) -> None:
        fixture = self.fixture()
        receipt = fixture.exact_receipt()
        receipt["expires_at"] = "2026-05-01T00:00:00Z"
        result = fixture.evaluate(receipt)
        self.assertFalse(result["valid"])
        self.assertEqual(result["execution_disposition"], "research_required")
        self.assertFalse(any(result["phase_permissions"].values()))
        self.assertTrue(any("expired" in reason for reason in result["reason_codes"]))

    def test_changed_bound_evidence_invalidates_receipt(self) -> None:
        fixture = self.fixture()
        receipt = fixture.exact_receipt()
        fixture.write(receipt)
        fixture.bound.write_text("changed after review\n", encoding="utf-8")
        result = fixture.evaluate()
        self.assertFalse(result["valid"])
        self.assertTrue(any("digest_is_stale" in reason for reason in result["reason_codes"]))

    def test_dag_projection_digest_mismatch_is_rejected(self) -> None:
        fixture = self.fixture()
        receipt = fixture.exact_receipt()
        actual = fixture.write(receipt)
        self.assertNotEqual(actual, SHA_A)
        result = fixture.evaluate(expected=SHA_A)
        self.assertFalse(result["valid"])
        self.assertEqual(result["reason_codes"], ["projection_receipt_digest_mismatch"])

    def test_require_phase_allowed_raises_with_reason(self) -> None:
        result = self.fixture().evaluate()
        with self.assertRaisesRegex(focus.EligibilityError, "receipt_missing"):
            focus.require_phase_allowed(result, "proof")

    def test_strict_validator_raises_for_invalid_receipt(self) -> None:
        fixture = self.fixture()
        receipt = fixture.frontier_receipt()
        receipt["frontier_exception"]["completion_probability"] = 0.6
        with self.assertRaisesRegex(focus.EligibilityError, "schema_invalid"):
            focus.validate_receipt(fixture.root, THEOREM, receipt, as_of=NOW)

    def test_symlinked_repository_root_is_rejected(self) -> None:
        fixture = self.fixture()
        link = fixture.root.parent / "focus-repo-link"
        link.symlink_to(fixture.root, target_is_directory=True)
        self.addCleanup(link.unlink)
        with self.assertRaisesRegex(focus.EligibilityError, "repository root traverses"):
            focus.validate_receipt(link, THEOREM, fixture.base_receipt(), as_of=NOW)


if __name__ == "__main__":
    unittest.main()
