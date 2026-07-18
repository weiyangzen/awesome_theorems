#!/usr/bin/env python3
"""End-to-end tests for scheduler-owned focus-admission issuance."""

from __future__ import annotations

import copy
import base64
import datetime as dt
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import stat
import subprocess
import tempfile
import unittest
from unittest import mock

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey


ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "scripts" / "stage1_focus_admission.py"
SPEC = importlib.util.spec_from_file_location("stage1_focus_admission_under_test", MODULE)
assert SPEC is not None and SPEC.loader is not None
admission = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(admission)

FOCUS_MODULE = ROOT / "scripts" / "stage1_focus_eligibility.py"
FOCUS_SPEC = importlib.util.spec_from_file_location(
    "stage1_focus_eligibility_admission_test", FOCUS_MODULE
)
assert FOCUS_SPEC is not None and FOCUS_SPEC.loader is not None
focus = importlib.util.module_from_spec(FOCUS_SPEC)
FOCUS_SPEC.loader.exec_module(focus)


THEOREM = "THM-M-0001"
NOW = dt.datetime.now(dt.timezone.utc)


def run(root: Path, *argv: str) -> str:
    result = subprocess.run(argv, cwd=root, text=True, capture_output=True, check=False)
    if result.returncode:
        raise AssertionError(
            f"{argv!r} failed:\n{result.stdout}\n{result.stderr}"
        )
    return result.stdout.strip()


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical(value: object) -> str:
    return json.dumps(value, ensure_ascii=True, indent=2) + "\n"


def utc(offset: dt.timedelta) -> str:
    return (NOW + offset).isoformat(timespec="microseconds").replace("+00:00", "Z")


class Fixture:
    def __init__(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name) / "repo"
        self.external = Path(self.temp.name) / "external"
        self.root.mkdir()
        self.external.mkdir()
        for repository in (self.root, self.external):
            run(repository, "git", "init", "-b", "main")
            run(repository, "git", "config", "user.email", "tests@example.invalid")
            run(repository, "git", "config", "user.name", "Focus Admission Test")

        self.external_source = self.external / "Proof.lean"
        self.external_source.write_text(
            "theorem exactProof : True := by trivial\n", encoding="utf-8"
        )
        (self.external / "lean-toolchain").write_text(
            "leanprover/lean4:v4.29.0\n", encoding="utf-8"
        )
        run(self.external, "git", "add", ".")
        run(self.external, "git", "commit", "-m", "immutable exact proof")
        self.external_revision = run(self.external, "git", "rev-parse", "HEAD")
        self.external_tree = run(
            self.external, "git", "rev-parse", f"{self.external_revision}^{{tree}}"
        )
        self.type_sha = hashlib.sha256(b"True").hexdigest()
        body_sha, _ = admission._declaration_region(
            self.external_source.read_bytes(), "exactProof"
        )
        self.body_sha = body_sha
        direct_replay = admission._readonly_kernel_command(
            self.external, ["lean", "Proof.lean"], timeout=30
        )
        if direct_replay.returncode != 0:
            raise AssertionError(direct_replay.stderr.decode("utf-8", "replace"))
        probe_type, probe_axioms, probe_sha = admission._lean_probe(
            self.external,
            source_path=self.external_source,
            declaration="exactProof",
            command_runner=admission._readonly_kernel_command,
        )
        if probe_type != self.type_sha or probe_axioms:
            raise AssertionError((probe_type, probe_axioms))

        docs = self.root / "Docs"
        owner = self.root / "Stage1_Instances" / THEOREM
        lean_root = self.root / "Formalizations" / "Lean"
        docs.mkdir()
        owner.mkdir(parents=True)
        lean_root.mkdir(parents=True)
        (lean_root / "lean-toolchain").write_text(
            "leanprover/lean4:v4.29.0\n", encoding="utf-8"
        )
        (lean_root / "lake-manifest.json").write_text(
            json.dumps(
                {
                    "version": "1.1.0",
                    "packagesDir": ".lake/packages",
                    "packages": [],
                    "name": "FocusAdmissionFixture",
                    "lakeDir": ".lake",
                },
                ensure_ascii=True,
            )
            + "\n",
            encoding="utf-8",
        )
        shutil.copy2(
            ROOT / "Docs" / "Stage1_Focus_Eligibility_Schema.json",
            docs / "Stage1_Focus_Eligibility_Schema.json",
        )
        self.scheduler_key = Ed25519PrivateKey.generate()
        self.reviewer_key = Ed25519PrivateKey.generate()
        self.timestamp_key = Ed25519PrivateKey.generate()
        self.scheduler_key_path = Path(self.temp.name) / "scheduler.pem"
        self.reviewer_key_path = Path(self.temp.name) / "reviewer.pem"
        for key, path in (
            (self.scheduler_key, self.scheduler_key_path),
            (self.reviewer_key, self.reviewer_key_path),
        ):
            path.write_bytes(
                key.private_bytes(
                    serialization.Encoding.PEM,
                    serialization.PrivateFormat.PKCS8,
                    serialization.NoEncryption(),
                )
            )
            path.chmod(0o600)
        (docs / "Stage1_Focus_Trust_Anchors.json").write_text(
            canonical(
                {
                    "schema_version": focus.TRUST_ANCHORS_SCHEMA,
                    "signature_algorithm": focus.SIGNATURE_ALGORITHM,
                    "keys": [
                        {
                            "key_id": "fixture-scheduler-1",
                            "role": "scheduler_issuance",
                            "principal_id": "scheduler-master-1",
                            "public_key_hex": self.scheduler_key.public_key().public_bytes_raw().hex(),
                            "status": "active",
                            "not_before": "2026-01-01T00:00:00Z",
                            "not_after": None,
                        },
                        {
                            "key_id": "fixture-reviewer-1",
                            "role": "independent_review",
                            "principal_id": "focus-reviewer-1",
                            "public_key_hex": self.reviewer_key.public_key().public_bytes_raw().hex(),
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
            ),
            encoding="utf-8",
        )
        self.trust_anchor_sha = sha(docs / "Stage1_Focus_Trust_Anchors.json")
        shutil.copy2(
            ROOT / "scripts" / "stage1_focus_eligibility.py",
            self.root / "stage1_focus_eligibility.py",
        )
        self.blueprint = docs / "Stage1_Blueprint_v2.md"
        self.blueprint.write_text(
            "# immutable checklist bytes\n\n"
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
        (docs / "Stage1_Target_Membership_v2.json").write_text(
            json.dumps(membership, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        self.graph = docs / "Stage1_Theorem_DAG_v2.json"
        self.graph.write_text('{"theorems": []}\n', encoding="utf-8")
        self.target = owner / "Target.lean"
        self.target.write_text("theorem target : True := by trivial\n", encoding="utf-8")
        self.evidence = owner / "focus-research-evidence.json"
        self.evidence.write_text(
            canonical({"theorem_id": THEOREM, "fact": "independently auditable"}),
            encoding="utf-8",
        )
        self.human_source = owner / "human-source.txt"
        self.human_source.write_text(
            "Exact Theorem\nTheorem 1\nProof of the exact True statement.\n",
            encoding="utf-8",
        )
        self.human_review = owner / "human-source-review.json"
        human_timestamp_subject = {
            "kind": "human_proof_source",
            "immutable_id": "fixture:exact",
            "citation": "Exact Theorem",
            "locator": "Theorem 1",
            "artifact_sha256": sha(self.human_source),
            "statement_fingerprint": self.type_sha,
            "statement_boundary": "the exact theorem",
            "hypotheses": [],
        }
        human_review = {
            "schema_version": admission.HUMAN_SOURCE_REVIEW_SCHEMA,
            "theorem_id": THEOREM,
            "source": {
                "citation": "Exact Theorem",
                "locator": "Theorem 1",
                "immutable_id": "fixture:exact",
                "artifact_path": (
                    f"Stage1_Instances/{THEOREM}/{self.human_source.name}"
                ),
                "content_sha256": sha(self.human_source),
            },
            "publication_timestamp": self.timestamp_token(
                human_timestamp_subject,
                issued_at=utc(dt.timedelta(hours=-6)),
                token_id="fixture-human-proof-publication-1",
            ),
            "statement_fingerprint": self.type_sha,
            "statement_boundary": "the exact theorem",
            "statement_crosswalk": {
                "source_artifact_sha256": sha(self.human_source),
                "locator": "Theorem 1",
                "boundary": "the exact theorem",
                "hypotheses": [],
                "statement_fingerprint": self.type_sha,
                "target_declaration_type_sha256": self.type_sha,
                "relation": "exact",
            },
            "hypotheses": [],
            "publication_status": "peer_reviewed",
            "license": {"identifier": "CC-BY-4.0", "reviewed_for_use": True},
            "reviewer": {
                "id": "human-source-reviewer",
                "role": "independent_reviewer",
            },
            "reviewed_at": utc(dt.timedelta(hours=-5)),
            "decision": "accepted",
        }
        human_review["review_sha256"] = admission._digest(
            admission._canonical_json(human_review)
        )
        self.human_review.write_text(canonical(human_review), encoding="utf-8")
        self.external_publication = owner / "external-proof-publication.txt"
        self.external_publication.write_text(
            "immutable publication record for the exact external proof\n",
            encoding="utf-8",
        )
        run(self.root, "git", "add", ".")
        run(self.root, "git", "commit", "-m", "authority base")
        self.base = run(self.root, "git", "rev-parse", "HEAD")
        self.runtime = self.root / ".cron" / "stage1-v2-app-server"
        self.runtime.mkdir(parents=True)
        self.proposal_path = owner / admission.PROPOSAL_NAME

        replay_sha = hashlib.sha256(direct_replay.stdout).hexdigest()
        lock_sha = sha(self.external / "lean-toolchain")
        source = {
            "formal_system": "Lean 4",
            "repository": str(self.external),
            "revision": self.external_revision,
            "tree_or_archive_sha256": hashlib.sha256(
                self.external_tree.encode("ascii")
            ).hexdigest(),
            "file_path": "Proof.lean",
            "file_sha256": sha(self.external_source),
            "module": "Proof",
            "declaration": "exactProof",
            "declaration_type_sha256": self.type_sha,
            "match_kind": "exact",
            "transport_evidence": [],
            "pre_stage1_provenance": None,
            "terminal_proof_body": {
                "locator": "exactProof",
                "kind": "theorem",
                "sha256": self.body_sha,
            },
            "kernel_replay": {
                "command": ["lean", "Proof.lean"],
                "checked_at": utc(dt.timedelta(hours=-5)),
                "exit_code": 0,
                "output_sha256": replay_sha,
                "toolchain": "leanprover/lean4:v4.29.0",
                "dependency_lock_sha256": lock_sha,
            },
            "trust_audit": {
                "placeholder_free": True,
                "unsafe_free": True,
                "oracle_free": True,
                "undeclared_axioms_free": True,
                "permitted_axioms": [],
                "tcb_description": "Lean kernel and pinned compiler",
                "output_sha256": probe_sha,
            },
            "compatibility": {
                "status": "compatible",
                "toolchain": "leanprover/lean4:v4.29.0",
                "dependency_lock_sha256": lock_sha,
            },
            "license": {
                "identifier": "Apache-2.0",
                "integration_permitted": True,
                "evidence_sha256": sha(self.evidence),
            },
        }
        roles = (
            "human_source_review",
            "statement_match",
            "machine_source_pin",
            "kernel_replay",
            "trust_audit",
            "compatibility_audit",
            "license_review",
            "integration_plan",
        )
        bindings = [
            {
                "path": (
                    f"Stage1_Instances/{THEOREM}/{self.human_review.name}"
                    if role == "human_source_review"
                    else f"Stage1_Instances/{THEOREM}/{self.evidence.name}"
                ),
                "sha256": (
                    sha(self.human_review)
                    if role == "human_source_review"
                    else sha(self.evidence)
                ),
                "role": role,
            }
            for role in roles
        ]
        self.proposal = {
            "schema_version": admission.PROPOSAL_SCHEMA,
            "proposal_id": "research-proposal-1",
            "theorem_id": THEOREM,
            "author": {"id": "research-worker-1", "role": "research_worker"},
            "submitted_at": utc(dt.timedelta(hours=-1)),
            "repository_base_revision": self.base,
            "evidence_as_of": utc(dt.timedelta(hours=-4)),
            "machine_evidence_class": "exact_external_unintegrated",
            "execution_disposition": "organize_or_integrate",
            "human_proof": {
                "status": "complete_source_confirmed",
                "statement_fingerprint": self.type_sha,
                "source": {
                    "citation": "Exact Theorem",
                    "locator": "Theorem 1",
                    "immutable_id": "fixture:exact",
                    "content_sha256": sha(self.human_source),
                    "proof_scope": "the exact theorem",
                    "hypotheses": [],
                    "publication_status": "peer_reviewed",
                    "license": {"identifier": "CC-BY-4.0", "reviewed_for_use": True},
                    "accepted_by": {
                        "id": "human-source-reviewer",
                        "role": "independent_reviewer",
                    },
                    "accepted_at": utc(dt.timedelta(hours=-5)),
                },
            },
            "target_binding": {
                "status": "verified",
                "formal_system": "Lean 4",
                "path": f"Stage1_Instances/{THEOREM}/Target.lean",
                "file_sha256": sha(self.target),
                "declaration": "target",
                "declaration_type_sha256": self.type_sha,
            },
            "statement_binding": {
                "human_statement_fingerprint": self.type_sha,
                "target_declaration_type_sha256": self.type_sha,
                "match_kind": "exact",
                "evidence": [],
            },
            "machine_proof": {
                "status": "exact_kernel_checked",
                "negative_search_boundary": None,
                "negative_search_inventory": [],
                "source": source,
            },
            "repository_gap": {
                "acceptance_status": "not_integrated",
                "local_presence": "absent",
                "integration_plan": ["pin and import exactProof"],
                "owned_paths": [f"Stage1_Instances/{THEOREM}"],
            },
            "evidence_bindings": bindings,
            "frontier_request": None,
            "invalidation_conditions": sorted(focus.REQUIRED_INVALIDATIONS),
        }
        self.write_external_provenance()
        run(self.root, "git", "commit", "-m", "freeze external proof provenance")
        self.base = run(self.root, "git", "rev-parse", "HEAD")
        self.proposal["repository_base_revision"] = self.base
        self.write_proposal()

    def close(self) -> None:
        self.temp.cleanup()

    def write_proposal(self) -> None:
        self.proposal_path.write_text(canonical(self.proposal), encoding="utf-8")
        run(self.root, "git", "add", str(self.proposal_path.relative_to(self.root)))
        run(self.root, "git", "commit", "-m", "worker research proposal")
        self.authority = run(self.root, "git", "rev-parse", "HEAD")

    def set_release_state(self, state: str) -> None:
        text = self.blueprint.read_text(encoding="utf-8")
        text = text.replace(
            "- [ ] `S56-M-0001-RELEASE`",
            f"- {state} `S56-M-0001-RELEASE`",
        )
        self.blueprint.write_text(text, encoding="utf-8")
        run(self.root, "git", "add", str(self.blueprint.relative_to(self.root)))
        run(self.root, "git", "commit", "-m", f"set release cursor {state}")
        self.authority = run(self.root, "git", "rev-parse", "HEAD")

    def timestamp_token(
        self, subject: dict[str, object], *, issued_at: str, token_id: str
    ) -> dict[str, object]:
        subject_sha = admission._digest(admission._canonical_json(subject))
        signature = self.timestamp_key.sign(
            focus._timestamp_signature_payload(
                token_id=token_id,
                issued_at=issued_at,
                subject_sha256=subject_sha,
            )
        ).hex()
        return {
            "schema_version": admission.TIMESTAMP_TOKEN_SCHEMA,
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

    def write_external_provenance(self) -> None:
        owner = self.proposal_path.parent
        path = owner / "external-proof-provenance.json"
        source = self.proposal["machine_proof"]["source"]
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
        report = {
            "schema_version": admission.EXTERNAL_PROVENANCE_SCHEMA,
            "theorem_id": THEOREM,
            "source": source_identity,
            "publication": {
                "immutable_id": "fixture:external-proof:pre-stage1",
                "timestamp": self.timestamp_token(
                    publication_subject,
                    issued_at="2026-07-15T20:00:00Z",
                    token_id="fixture-machine-proof-publication-1",
                ),
            },
            "reviewer": {
                "id": "external-provenance-reviewer",
                "role": "independent_reviewer",
            },
            "reviewed_at": "2026-07-15T20:15:00Z",
            "decision": "accepted",
        }
        report["provenance_sha256"] = admission._digest(
            admission._canonical_json(report)
        )
        path.write_text(canonical(report), encoding="utf-8")
        binding = {
            "path": path.relative_to(self.root).as_posix(),
            "sha256": sha(path),
            "role": admission.EXTERNAL_PROVENANCE_ROLE,
        }
        self.proposal["evidence_bindings"] = [
            row for row in self.proposal["evidence_bindings"]
            if row["role"] != admission.EXTERNAL_PROVENANCE_ROLE
        ] + [binding]
        source["pre_stage1_provenance"] = {
            "path": binding["path"],
            "sha256": binding["sha256"],
            "provenance_sha256": report["provenance_sha256"],
        }
        run(
            self.root,
            "git",
            "add",
            self.external_publication.relative_to(self.root).as_posix(),
            path.relative_to(self.root).as_posix(),
        )

    def configure_exact_pinned_closure(
        self, *, with_provider_dependency: bool = False
    ) -> None:
        """Install the external proof as the fixture's live manifest package."""

        dependency: Path | None = None
        dependency_revision: str | None = None
        dependency_clause = ""
        if with_provider_dependency:
            dependency = Path(self.temp.name) / "provider-dependency"
            dependency.mkdir()
            run(dependency, "git", "init", "-b", "main")
            run(dependency, "git", "config", "user.email", "tests@example.invalid")
            run(dependency, "git", "config", "user.name", "Focus Admission Test")
            (dependency / "Dependency.lean").write_text(
                "theorem dependencyProof : True := by trivial\n", encoding="utf-8"
            )
            (dependency / "lakefile.toml").write_text(
                'name = "provider-dependency"\nversion = "0.1.0"\n'
                'defaultTargets = ["Dependency"]\n\n'
                '[[lean_lib]]\nname = "Dependency"\n',
                encoding="utf-8",
            )
            (dependency / "lean-toolchain").write_text(
                "leanprover/lean4:v4.29.0\n", encoding="utf-8"
            )
            (dependency / ".gitignore").write_text("/.lake/\n", encoding="utf-8")
            run(dependency, "git", "add", ".")
            run(dependency, "git", "commit", "-m", "provider dependency")
            dependency_revision = run(dependency, "git", "rev-parse", "HEAD")
            dependency_clause = (
                '\n[[require]]\nname = "provider-dependency"\n'
                f'git = "{dependency}"\nrev = "{dependency_revision}"\n'
            )
        (self.external / "lakefile.toml").write_text(
            'name = "formal-proof"\nversion = "0.1.0"\n'
            'defaultTargets = ["Proof"]\n\n'
            '[[lean_lib]]\nname = "Proof"\n'
            + dependency_clause,
            encoding="utf-8",
        )
        (self.external / ".gitignore").write_text(
            "/.lake/\n/lake-manifest.json\n", encoding="utf-8"
        )
        run(self.external, "git", "add", "lakefile.toml", ".gitignore")
        run(self.external, "git", "commit", "-m", "make exact proof importable")
        self.external_revision = run(self.external, "git", "rev-parse", "HEAD")
        self.external_tree = run(
            self.external, "git", "rev-parse", f"{self.external_revision}^{{tree}}"
        )
        lean_root = self.root / "Formalizations" / "Lean"
        package = lean_root / ".lake" / "packages" / "formal-proof"
        package.parent.mkdir(parents=True, exist_ok=True)
        clone = subprocess.run(
            ["git", "clone", "--quiet", "--", str(self.external), str(package)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        if clone.returncode:
            raise AssertionError(clone.stderr.decode("utf-8", "replace"))
        run(package, "git", "checkout", "--detach", self.external_revision)
        manifest = lean_root / "lake-manifest.json"
        manifest_packages = [
            {
                "url": str(self.external),
                "type": "git",
                "subDir": None,
                "scope": "",
                "rev": self.external_revision,
                "name": "«formal-proof»",
                "manifestFile": "lake-manifest.json",
                "inputRev": self.external_revision,
                "inherited": False,
                "configFile": "lakefile.toml",
            }
        ]
        if dependency is not None and dependency_revision is not None:
            dependency_package = lean_root / ".lake" / "packages" / "provider-dependency"
            clone = subprocess.run(
                ["git", "clone", "--quiet", "--", str(dependency), str(dependency_package)],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )
            if clone.returncode:
                raise AssertionError(clone.stderr.decode("utf-8", "replace"))
            run(dependency_package, "git", "checkout", "--detach", dependency_revision)
            manifest_packages.append(
                {
                    "url": str(dependency),
                    "type": "git",
                    "subDir": None,
                    "scope": "",
                    "rev": dependency_revision,
                    "name": "«provider-dependency»",
                    "manifestFile": "lake-manifest.json",
                    "inputRev": dependency_revision,
                    "inherited": True,
                    "configFile": "lakefile.toml",
                }
            )
        manifest.write_text(
            json.dumps(
                {
                    "version": "1.1.0",
                    "packagesDir": ".lake/packages",
                    "packages": manifest_packages,
                    "name": "FocusAdmissionFixture",
                    "lakeDir": ".lake",
                },
                ensure_ascii=True,
            )
            + "\n",
            encoding="utf-8",
        )
        (lean_root / "lakefile.lean").write_text(
            'import Lake\nopen Lake DSL\n\n'
            'package «FocusAdmissionFixture»\n\n'
            'require «formal-proof» from git\n'
            f'  "{self.external}" @ "{self.external_revision}"\n',
            encoding="utf-8",
        )
        config = lean_root / ".lake" / "config"
        config.mkdir(parents=True, exist_ok=True)
        warm = subprocess.run(
            ["lake", "build", "Proof"],
            cwd=package,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        if warm.returncode:
            raise AssertionError(warm.stderr.decode("utf-8", "replace"))
        root_warm = subprocess.run(
            ["lake", "env", "lean", "--version"],
            cwd=lean_root,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        if root_warm.returncode:
            raise AssertionError(root_warm.stderr.decode("utf-8", "replace"))
        run(self.root, "git", "add", manifest.relative_to(self.root).as_posix(),
            (lean_root / "lakefile.lean").relative_to(self.root).as_posix())
        run(self.root, "git", "commit", "-m", "pin exact provider in repository Lake manifest")
        self.base = run(self.root, "git", "rev-parse", "HEAD")
        source = self.proposal["machine_proof"]["source"]
        source["revision"] = self.external_revision
        source["tree_or_archive_sha256"] = hashlib.sha256(
            self.external_tree.encode("ascii")
        ).hexdigest()
        source["kernel_replay"]["dependency_lock_sha256"] = sha(manifest)
        source["compatibility"]["dependency_lock_sha256"] = source["kernel_replay"][
            "dependency_lock_sha256"
        ]
        self.proposal["repository_base_revision"] = self.base
        self.proposal["machine_evidence_class"] = "exact_pinned_closure"
        self.proposal["repository_gap"]["local_presence"] = "pinned_dependency"
        self.write_external_provenance()
        self.write_proposal()

    def configure_checked_transport(self, *, depend_on_provider: bool = True) -> None:
        """Replace the exact provider with a nonidentical, checked Lean source."""
        self.external_source.write_text(
            "theorem exactProof : True /\\ True := by constructor <;> trivial\n",
            encoding="utf-8",
        )
        run(self.external, "git", "add", ".")
        if run(self.external, "git", "status", "--porcelain"):
            run(self.external, "git", "commit", "-m", "nonidentical provider theorem")
        self.external_revision = run(self.external, "git", "rev-parse", "HEAD")
        self.external_tree = run(
            self.external, "git", "rev-parse", f"{self.external_revision}^{{tree}}"
        )
        provider_replay = admission._readonly_kernel_command(
            self.external, ["lean", "Proof.lean"], timeout=30
        )
        if provider_replay.returncode:
            raise AssertionError(provider_replay.stderr.decode("utf-8", "replace"))
        provider_type, _axioms, provider_trust_sha = admission._lean_probe(
            self.external,
            source_path=self.external_source,
            declaration="exactProof",
            command_runner=admission._readonly_kernel_command,
            lean_path=self.external,
        )
        provider_body, _ = admission._declaration_region(
            self.external_source.read_bytes(), "exactProof"
        )

        owner = self.target.parent
        artifact = owner / "MachineTransport.lean"
        validator = owner / "check_machine_transport.py"
        replay_output = owner / "machine-transport-replay.txt"
        trust_output = owner / "machine-transport-trust.txt"
        transport_receipt = owner / "machine-transport-replay.json"
        artifact.write_text(
            (
                "theorem target : True := exactProof.1\n"
                if depend_on_provider
                else "theorem target : True := by trivial\n"
            ),
            encoding="utf-8",
        )
        validator.write_bytes(admission.TRANSPORT_VALIDATOR_SOURCE)
        relative = lambda path: path.relative_to(self.root).as_posix()
        validator_result = subprocess.run(
            [
                "python3",
                relative(validator),
                "--transport-artifact",
                relative(artifact),
            ],
            cwd=self.root,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        if validator_result.returncode or validator_result.stderr:
            raise AssertionError(validator_result)
        replay_output.write_bytes(validator_result.stdout)

        lean_root = self.root / "Formalizations" / "Lean"
        provider_source = lean_root / admission.TRANSPORT_PROVIDER_SOURCE
        provider_olean = lean_root / admission.TRANSPORT_PROVIDER_OLEAN
        probe = lean_root / admission.TRANSPORT_REPLAY_SOURCE
        provider_source.write_bytes(self.external_source.read_bytes())
        try:
            provider_compile = admission._readonly_kernel_command(
                lean_root,
                [
                    "lean",
                    "-o",
                    admission.TRANSPORT_PROVIDER_OLEAN,
                    admission.TRANSPORT_PROVIDER_SOURCE,
                ],
                timeout=30,
                writable=True,
            )
            if provider_compile.returncode:
                raise AssertionError(
                    provider_compile.stderr.decode("utf-8", "replace")
                )
            probe.write_bytes(
                admission._transport_replay_source(
                    artifact.read_bytes(),
                    target_declaration="target",
                    provider_declaration="exactProof",
                )
            )
            if depend_on_provider:
                _type_sha, _axioms, trust_sha = admission._lean_probe(
                    lean_root,
                    source_path=probe,
                    declaration="target",
                    command_runner=admission._readonly_kernel_command,
                    lean_path=lean_root,
                )
            else:
                trust_sha = "0" * 64
        finally:
            probe.unlink(missing_ok=True)
            provider_olean.unlink(missing_ok=True)
            provider_source.unlink(missing_ok=True)
        # The replay receipt binds the scheduler-observed probe output digest;
        # the auxiliary file itself is only the theorem-owned evidence handle.
        trust_output.write_bytes(b"transport trust replay is scheduler-observed\n")
        artifact_body, _ = admission._declaration_region(artifact.read_bytes(), "target")
        toolchain, dependency_sha = admission._dependency_identity(lean_root)
        transport_value = {
            "schema_version": "stage1-machine-transport-replay/1.0",
            "theorem_id": THEOREM,
            "source": {
                "formal_system": "Lean 4",
                "declaration": "exactProof",
                "declaration_type_sha256": provider_type,
            },
            "target": {
                "formal_system": "Lean 4",
                "declaration": "target",
                "declaration_type_sha256": self.type_sha,
            },
            "transport_artifact": {
                "path": relative(artifact),
                "sha256": sha(artifact),
                "formal_system": "Lean 4",
                "declaration": "target",
                "declaration_type_sha256": self.type_sha,
                "terminal_proof_body": {
                    "locator": "target",
                    "kind": "theorem",
                    "sha256": artifact_body,
                },
            },
            "validator": {
                "path": relative(validator),
                "sha256": sha(validator),
                "authority": "scheduler_master_lane",
            },
            "replay": {
                "command": [
                    "python3",
                    relative(validator),
                    "--transport-artifact",
                    relative(artifact),
                ],
                "checked_at": utc(dt.timedelta(hours=-5)),
                "exit_code": 0,
                "output": {"path": relative(replay_output), "sha256": sha(replay_output)},
                "toolchain": toolchain,
                "dependency_lock_sha256": dependency_sha,
            },
            "trust_audit": {
                "placeholder_free": True,
                "unsafe_free": True,
                "oracle_free": True,
                "undeclared_axioms_free": True,
                "permitted_axioms": [],
                "tcb_description": "Lean kernel and pinned scheduler validator",
                "output": {"path": relative(trust_output), "sha256": sha(trust_output)},
            },
            "independent_review": {
                "reviewer": {
                    "id": "machine-transport-reviewer",
                    "role": "independent_reviewer",
                },
                "reviewed_at": utc(dt.timedelta(hours=-4, minutes=-30)),
                "decision": "approved",
            },
        }
        transport_receipt.write_text(canonical(transport_value), encoding="utf-8")
        run(self.root, "git", "add", *map(relative, (
            artifact, validator, replay_output, trust_output, transport_receipt
        )))
        run(self.root, "git", "commit", "-m", "scheduler checked transport evidence")
        self.base = run(self.root, "git", "rev-parse", "HEAD")

        source = self.proposal["machine_proof"]["source"]
        source.update(
            revision=self.external_revision,
            tree_or_archive_sha256=hashlib.sha256(
                self.external_tree.encode("ascii")
            ).hexdigest(),
            file_sha256=sha(self.external_source),
            declaration_type_sha256=provider_type,
            match_kind="checked_transport",
            terminal_proof_body={
                "locator": "exactProof", "kind": "theorem", "sha256": provider_body
            },
        )
        source["kernel_replay"].update(
            output_sha256=hashlib.sha256(provider_replay.stdout).hexdigest()
        )
        source["trust_audit"]["output_sha256"] = provider_trust_sha
        transport_binding = {
            "path": relative(transport_receipt),
            "sha256": sha(transport_receipt),
            "role": "statement_match",
            "evidence_kind": "machine_checked_statement_transport",
            "source_formal_system": "Lean 4",
            "source_declaration": "exactProof",
            "source_declaration_type_sha256": provider_type,
            "target_formal_system": "Lean 4",
            "target_declaration": "target",
            "target_declaration_type_sha256": self.type_sha,
            "replay_receipt_sha256": sha(transport_receipt),
        }
        source["transport_evidence"] = [copy.deepcopy(transport_binding)]
        statement_binding = next(
            row
            for row in self.proposal["evidence_bindings"]
            if row["role"] == "statement_match"
        )
        self.proposal["evidence_bindings"].remove(statement_binding)
        self.proposal["evidence_bindings"].append(
            {
                "path": transport_binding["path"],
                "sha256": transport_binding["sha256"],
                "role": "statement_match",
                "evidence_kind": "machine_checked_statement_transport",
            }
        )
        self.proposal["repository_base_revision"] = self.base
        self.proposal["repository_gap"]["integration_plan"] = [
            "pin provider and retain the checked local transport"
        ]
        self.write_external_provenance()
        if run(self.root, "git", "diff", "--cached", "--name-only"):
            run(self.root, "git", "commit", "-m", "refresh external proof provenance")
        self.base = run(self.root, "git", "rev-parse", "HEAD")
        self.proposal["repository_base_revision"] = self.base
        self.write_proposal()

    def decision(self, **changes: object) -> dict:
        proposal_sha = sha(self.proposal_path)
        human_review = json.loads(self.human_review.read_text())
        result = {
            "schema_version": admission.DECISION_SCHEMA,
            "theorem_id": THEOREM,
            "authority_revision": self.authority,
            "proposal_sha256": proposal_sha,
            "issuer": {"id": "scheduler-master-1", "role": "scheduler_master_lane"},
            "reviewer": {"id": "focus-reviewer-1", "role": "independent_reviewer"},
            "admission_decision": "admit_integration",
            "expires_at": utc(dt.timedelta(days=2)),
            "human_source_authorization": {
                "path": f"Stage1_Instances/{THEOREM}/{self.human_review.name}",
                "sha256": sha(self.human_review),
                "review_sha256": human_review.get("review_sha256", "0" * 64),
                "reviewer": {
                    "id": "human-source-reviewer",
                    "role": "independent_reviewer",
                },
                "decision": "accepted",
            },
            "frontier_authorization": None,
        }
        result.update(changes)
        return result

    def prepare(self, decision: dict | None = None) -> Path:
        replay_authority = {
            "schema_version": "stage1-lean-authority/1.1",
            "toolchain": "leanprover/lean4:v4.29.0",
            "toolchain_file_sha256": "1" * 64,
            "dependency_lock_sha256": sha(
                self.root / "Formalizations" / "Lean" / "lake-manifest.json"
            ),
            "dependency_packages_sha256": "3" * 64,
            "compiled_cache_sha256": "4" * 64,
            "compiled_cache_file_count": 1,
            "compiled_cache_bytes": 1,
            "lean_binary_sha256": "5" * 64,
            "lake_binary_sha256": "6" * 64,
            "toolchain_closure_sha256": "7" * 64,
            "toolchain_closure_file_count": 1,
            "toolchain_closure_bytes": 1,
            "toolchain_mount": "/stage1-toolchain",
            "lake_cache_mount": "/stage1-lake-cache",
            "network_policy": "denied",
            "repo_access": "read_only",
        }
        with mock.patch.object(
            admission.stage1_lean_authority,
            "build_repository_lean_authority",
            return_value=(replay_authority, Path("/toolchain"), Path("/cache")),
        ), mock.patch.object(
            admission.stage1_lean_authority,
            "build_project_lean_authority",
            return_value=(replay_authority, Path("/toolchain"), None),
        ), mock.patch.object(
            admission.focus_eligibility,
            "TRUST_ANCHORS_SHA256",
            self.trust_anchor_sha,
        ):
            return admission.prepare_focus_admission(
                self.root,
                self.runtime,
                self.proposal_path,
                decision or self.decision(),
            )

    def review(self, candidate: Path) -> Path:
        replay_authority = json.loads(candidate.read_text())[
            "candidate_verification"
        ]["local_target_authority_result"]["replay_authority"]
        with mock.patch.object(
            admission.focus_eligibility,
            "TRUST_ANCHORS_SHA256",
            self.trust_anchor_sha,
        ), mock.patch.object(
            admission.stage1_lean_authority,
            "build_repository_lean_authority",
            return_value=(replay_authority, Path("/toolchain"), Path("/cache")),
        ), mock.patch.object(
            admission.stage1_lean_authority,
            "build_project_lean_authority",
            return_value=(replay_authority, Path("/toolchain"), None),
        ):
            return admission.review_focus_admission(
                self.root,
                self.runtime,
                candidate,
                {"id": "focus-reviewer-1", "role": "independent_reviewer"},
                reviewer_signing_key_path=self.reviewer_key_path,
            )

    def regenerate(self, root: Path) -> None:
        receipt = admission.focus_eligibility.evaluate_target(root, THEOREM)
        self.graph.write_text(
            canonical({"theorems": [{"theorem_id": THEOREM, "focus_eligibility": receipt}]}),
            encoding="utf-8",
        )

    def publish(self, candidate: Path, review: Path, **kwargs: object) -> Path:
        candidate_value = json.loads(candidate.read_text())
        replay_authority = candidate_value["candidate_verification"][
            "kernel_authority_result"
        ]["replay_authority"]
        local_authority = candidate_value["candidate_verification"][
            "local_target_authority_result"
        ]["replay_authority"]
        external_result = candidate_value["candidate_verification"][
            "kernel_authority_result"
        ]
        replayed_external = {
            **external_result,
            "resolved_revision": candidate_value["candidate_verification"][
                "resolved_revision"
            ],
            "archive_sha256": candidate_value["candidate_verification"][
                "archive_sha256"
            ],
            "resolved_tree": candidate_value["candidate_verification"][
                "resolved_tree"
            ],
            "kernel_stdout_sha256": candidate_value["candidate_verification"][
                "kernel_stdout_sha256"
            ],
            "kernel_stderr_sha256": candidate_value["candidate_verification"][
                "kernel_stderr_sha256"
            ],
        }
        with mock.patch.object(
            admission.focus_eligibility,
            "TRUST_ANCHORS_SHA256",
            self.trust_anchor_sha,
        ), mock.patch.object(
            admission.focus_eligibility,
            "_lean_probe",
            return_value=(
                candidate_value["candidate_verification"][
                    "local_target_authority_result"
                ]["declaration_type_sha256"],
                candidate_value["candidate_verification"][
                    "local_target_authority_result"
                ]["permitted_axioms"],
                candidate_value["candidate_verification"][
                    "local_target_authority_result"
                ]["trust_audit_output_sha256"],
            ),
        ), mock.patch.object(
            admission.focus_eligibility,
            "_replay_external_authority",
            return_value=replayed_external,
        ), mock.patch.object(
            admission.focus_eligibility.stage1_lean_authority,
            "build_project_lean_authority",
            return_value=(replay_authority, Path("/toolchain"), None),
        ), mock.patch.object(
            admission.focus_eligibility.stage1_lean_authority,
            "build_repository_lean_authority",
            return_value=(local_authority, Path("/toolchain"), Path("/cache")),
        ):
            return admission.publish_focus_admission(
                self.root,
                self.runtime,
                candidate,
                review,
                scheduler_signing_key_path=self.scheduler_key_path,
                **kwargs,
            )

    def evaluate(self) -> dict:
        receipt = json.loads(
            (self.root / focus.receipt_relative_path(THEOREM)).read_text()
        )
        external_authority = receipt["admission_authority"][
            "scheduler_verification"
        ]["kernel_authority_result"]["replay_authority"]
        local_authority = receipt["admission_authority"][
            "scheduler_verification"
        ]["local_target_authority_result"]["replay_authority"]
        with mock.patch.object(
            focus,
            "TRUST_ANCHORS_SHA256",
            self.trust_anchor_sha,
        ), mock.patch.object(
            focus.stage1_lean_authority,
            "build_project_lean_authority",
            return_value=(external_authority, Path("/toolchain"), None),
        ), mock.patch.object(
            focus.stage1_lean_authority,
            "build_repository_lean_authority",
            return_value=(local_authority, Path("/toolchain"), Path("/cache")),
        ):
            return focus.evaluate_target(
                self.root, THEOREM, runtime_root=self.runtime
            )


class FocusAdmissionTests(unittest.TestCase):
    def fixture(self) -> Fixture:
        fixture = Fixture()
        self.addCleanup(fixture.close)
        return fixture

    def test_prepare_rejects_current_master_accepted_release(self) -> None:
        fixture = self.fixture()
        with mock.patch.object(
            admission.focus_eligibility,
            "current_master_release_acceptance",
            return_value=True,
        ), self.assertRaisesRegex(
            admission.AdmissionError, "already master-accepted root"
        ):
            fixture.prepare()

    def test_review_rechecks_release_acceptance_after_prepare(self) -> None:
        fixture = self.fixture()
        candidate = fixture.prepare()
        with mock.patch.object(
            admission.focus_eligibility,
            "current_master_release_acceptance",
            return_value=True,
        ), self.assertRaisesRegex(
            admission.AdmissionError, "already master-accepted root"
        ):
            fixture.review(candidate)

    def test_publish_rechecks_release_acceptance_after_review(self) -> None:
        fixture = self.fixture()
        candidate = fixture.prepare()
        review = fixture.review(candidate)
        with mock.patch.object(
            admission.focus_eligibility,
            "current_master_release_acceptance",
            return_value=True,
        ), self.assertRaisesRegex(
            admission.AdmissionError, "already master-accepted root"
        ):
            fixture.publish(
                candidate,
                review,
                regenerate=fixture.regenerate,
                validate_graph=lambda _root: None,
            )

    @staticmethod
    def write_wal(
        fixture: Fixture,
        rows: list[dict[str, object]],
        *,
        runtime: Path | None = None,
        extra: dict[str, object] | None = None,
    ) -> Path:
        selected = runtime or fixture.runtime
        wal = selected / "focus-admission-wal.json"
        value: dict[str, object] = {
            "schema_version": admission.WAL_SCHEMA,
            "authority_revision": fixture.authority,
            "snapshots": rows,
        }
        if extra:
            value.update(extra)
        wal.parent.mkdir(parents=True, exist_ok=True)
        wal.write_text(canonical(value), encoding="utf-8")
        wal.chmod(0o600)
        return wal

    def test_prepare_rejects_theorem_outside_frozen_membership(self) -> None:
        fixture = self.fixture()
        nonmember = "THM-M-9999"
        owner = fixture.root / "Stage1_Instances" / nonmember
        owner.mkdir()
        proposal = copy.deepcopy(fixture.proposal)
        proposal["theorem_id"] = nonmember
        proposal["proposal_id"] = "nonmember-proposal"
        proposal["repository_base_revision"] = fixture.authority
        proposal_path = owner / admission.PROPOSAL_NAME
        proposal_path.write_text(canonical(proposal), encoding="utf-8")
        run(fixture.root, "git", "add", proposal_path.relative_to(fixture.root).as_posix())
        run(fixture.root, "git", "commit", "-m", "inject nonmember proposal")
        proposal_sha = sha(proposal_path)
        decision = fixture.decision()
        decision.update(
            theorem_id=nonmember,
            authority_revision=run(fixture.root, "git", "rev-parse", "HEAD"),
            proposal_sha256=proposal_sha,
        )
        with self.assertRaisesRegex(
            admission.AdmissionError, "not a frozen Stage1 target"
        ):
            admission.prepare_focus_admission(
                fixture.root, fixture.runtime, proposal_path, decision
            )

    def test_publish_rechecks_frozen_membership_before_writing(self) -> None:
        fixture = self.fixture()
        nonmember = "THM-M-9999"
        with mock.patch.object(
            admission,
            "_reload_candidate",
            return_value=({"theorem_id": nonmember}, {}),
        ), self.assertRaisesRegex(
            admission.AdmissionError, "not a frozen Stage1 target"
        ):
            admission.publish_focus_admission(
                fixture.root,
                fixture.runtime,
                fixture.runtime / "candidate.json",
                fixture.runtime / "review.json",
            )
        self.assertFalse(
            (fixture.root / focus.receipt_relative_path(nonmember)).exists()
        )

    def test_pre_stage1_timestamp_is_signed_content_bound_and_independent(self) -> None:
        fixture = self.fixture()
        source = fixture.proposal["machine_proof"]["source"]
        report_path = fixture.proposal_path.parent / "external-proof-provenance.json"
        report = json.loads(report_path.read_text())

        # Make the report self-consistent while retaining a signature over the
        # original subject, which models a retroactive/local JSON forgery.
        report["publication"]["timestamp"]["subject"]["file_sha256"] = "f" * 64
        report["publication"]["timestamp"]["subject_sha256"] = admission._digest(
            admission._canonical_json(report["publication"]["timestamp"]["subject"])
        )
        report["provenance_sha256"] = admission._digest(
            admission._canonical_json(
                {key: value for key, value in report.items() if key != "provenance_sha256"}
            )
        )
        report_path.write_text(canonical(report), encoding="utf-8")
        run(fixture.root, "git", "add", str(report_path.relative_to(fixture.root)))
        run(fixture.root, "git", "commit", "-m", "forge historical timestamp subject")
        binding = next(
            row for row in fixture.proposal["evidence_bindings"]
            if row["role"] == admission.EXTERNAL_PROVENANCE_ROLE
        )
        binding["sha256"] = sha(report_path)
        source["pre_stage1_provenance"].update(
            sha256=binding["sha256"], provenance_sha256=report["provenance_sha256"]
        )
        fixture.proposal["repository_base_revision"] = run(
            fixture.root, "git", "rev-parse", "HEAD"
        )
        fixture.write_proposal()
        with self.assertRaisesRegex(Exception, "timestamp|published bytes"):
            fixture.prepare()

        good = fixture.timestamp_token(
            {
                "kind": "external_machine_proof",
                "immutable_id": "fixture:external-proof:pre-stage1",
                "repository": source["repository"],
                "revision": source["revision"],
                "tree_or_archive_sha256": source["tree_or_archive_sha256"],
                "file_path": source["file_path"],
                "file_sha256": source["file_sha256"],
                "declaration": source["declaration"],
                "declaration_type_sha256": source["declaration_type_sha256"],
                "terminal_proof_body_sha256": source["terminal_proof_body"]["sha256"],
            },
            issued_at="2026-07-15T20:00:00Z",
            token_id="fixture-machine-proof-publication-2",
        )
        good["authority"] = {
            "id": "research-worker-1",
            "role": "publication_timestamp_authority",
        }
        report["publication"]["timestamp"] = good
        report["provenance_sha256"] = admission._digest(
            admission._canonical_json(
                {key: value for key, value in report.items() if key != "provenance_sha256"}
            )
        )
        report_path.write_text(canonical(report), encoding="utf-8")
        run(fixture.root, "git", "add", str(report_path.relative_to(fixture.root)))
        run(fixture.root, "git", "commit", "-m", "self timestamp machine proof")
        binding["sha256"] = sha(report_path)
        source["pre_stage1_provenance"].update(
            sha256=binding["sha256"], provenance_sha256=report["provenance_sha256"]
        )
        fixture.proposal["repository_base_revision"] = run(
            fixture.root, "git", "rev-parse", "HEAD"
        )
        fixture.write_proposal()
        with self.assertRaisesRegex(Exception, "not independent|not authorized"):
            fixture.prepare()

    def test_changed_remote_mirror_and_repackaged_proof_blob_are_rejected(self) -> None:
        fixture = self.fixture()
        mirror = Path(fixture.temp.name) / "renamed-mirror"
        run(Path(fixture.temp.name), "git", "clone", str(fixture.root), str(mirror))
        run(mirror, "git", "remote", "set-url", "origin", "https://mirror.invalid/renamed.git")
        with self.assertRaisesRegex(admission.AdmissionError, "commit/history/object identity"):
            admission._reject_authoritative_external_identity(
                fixture.root,
                "https://mirror.invalid/renamed.git",
                mirror,
                revision=run(mirror, "git", "rev-parse", "HEAD"),
                source_path="Stage1_Instances/THM-M-0001/Target.lean",
            )

        repack = Path(fixture.temp.name) / "repack"
        repack.mkdir()
        run(repack, "git", "init", "-b", "main")
        run(repack, "git", "config", "user.email", "tests@example.invalid")
        run(repack, "git", "config", "user.name", "Repack Test")
        shutil.copy2(fixture.target, repack / "Proof.lean")
        run(repack, "git", "add", ".")
        run(repack, "git", "commit", "-m", "repackage authoritative proof bytes")
        with self.assertRaisesRegex(admission.AdmissionError, "source blob"):
            admission._reject_authoritative_external_identity(
                fixture.root,
                str(repack),
                repack,
                revision=run(repack, "git", "rev-parse", "HEAD"),
                source_path="Proof.lean",
            )

    def test_human_source_requires_timestamped_bytes_and_exact_crosswalk(self) -> None:
        fixture = self.fixture()
        fixture.human_source.write_text(
            "Arbitrary text that does not match the reviewed archive.\n",
            encoding="utf-8",
        )
        run(fixture.root, "git", "add", str(fixture.human_source.relative_to(fixture.root)))
        run(fixture.root, "git", "commit", "-m", "replace human source with arbitrary text")
        fixture.proposal["repository_base_revision"] = run(
            fixture.root, "git", "rev-parse", "HEAD"
        )
        fixture.write_proposal()
        with self.assertRaisesRegex(admission.AdmissionError, "human source bytes"):
            fixture.prepare()

        fixture = self.fixture()
        review = json.loads(fixture.human_review.read_text())
        review["statement_crosswalk"]["relation"] = "similar"
        review["review_sha256"] = admission._digest(
            admission._canonical_json(
                {key: value for key, value in review.items() if key != "review_sha256"}
            )
        )
        fixture.human_review.write_text(canonical(review), encoding="utf-8")
        run(fixture.root, "git", "add", str(fixture.human_review.relative_to(fixture.root)))
        run(fixture.root, "git", "commit", "-m", "weaken human theorem crosswalk")
        binding = next(
            row for row in fixture.proposal["evidence_bindings"]
            if row["role"] == "human_source_review"
        )
        binding["sha256"] = sha(fixture.human_review)
        fixture.proposal["repository_base_revision"] = run(
            fixture.root, "git", "rev-parse", "HEAD"
        )
        fixture.write_proposal()
        decision = fixture.decision()
        decision["authority_revision"] = fixture.authority
        decision["proposal_sha256"] = sha(fixture.proposal_path)
        decision["human_source_authorization"].update(
            sha256=binding["sha256"], review_sha256=review["review_sha256"]
        )
        with self.assertRaisesRegex(admission.AdmissionError, "statement crosswalk"):
            fixture.prepare(decision)

    def test_external_source_is_materialized_replayed_reviewed_and_published(self) -> None:
        fixture = self.fixture()
        candidate = fixture.prepare()
        review = fixture.review(candidate)
        issuance = fixture.publish(
            candidate,
            review,
            regenerate=fixture.regenerate,
            validate_graph=lambda _root: None,
        )
        receipt_path = fixture.root / focus.receipt_relative_path(THEOREM)
        result = fixture.evaluate()
        self.assertTrue(result["valid"], result["reason_codes"])
        self.assertEqual(result["execution_disposition"], "organize_or_integrate")
        self.assertTrue(receipt_path.is_file())
        status = json.loads(issuance.read_text())
        self.assertEqual(
            status,
            json.loads(receipt_path.read_text())["issuance_authority"]["issuance"],
        )
        candidate_value = json.loads(candidate.read_text())
        review_value = json.loads(review.read_text())
        self.assertEqual(
            candidate_value["candidate_verification"]["verification_kind"],
            "external_lean_kernel_replay",
        )
        self.assertEqual(
            review_value["review_verification"]["kernel_authority_result"][
                "declaration_type_sha256"
            ],
            fixture.type_sha,
        )
        self.assertEqual(
            review_value["review_verification"]["repository_access"],
            "temporary_read_only_replay",
        )
        receipt = json.loads(receipt_path.read_text())
        authority = receipt["admission_authority"]
        self.assertEqual(
            authority["scheduler_verification"]["local_target_authority_result"],
            authority["reviewer_verification"]["local_target_authority_result"],
        )
        self.assertEqual(
            authority["scheduler_verification"]["kernel_authority_result"],
            authority["reviewer_verification"]["kernel_authority_result"],
        )

    def test_machine_source_cannot_self_permit_arbitrary_axiom(self) -> None:
        fixture = self.fixture()
        source = fixture.proposal["machine_proof"]["source"]
        source["trust_audit"]["permitted_axioms"] = ["magic"]
        fixture.write_proposal()
        with mock.patch.object(
            admission,
            "_lean_probe",
            return_value=(fixture.type_sha, ["magic"], source["trust_audit"]["output_sha256"]),
        ), self.assertRaisesRegex(
            admission.AdmissionError, "outside the foundation policy"
        ):
            fixture.prepare()

    def test_kernel_replay_ignores_ambient_lean_and_executes_exact_pin(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            checkout = Path(directory)
            (checkout / "lean-toolchain").write_text(
                "leanprover/lean4:v4.29.0\n", encoding="utf-8"
            )
            (checkout / "Proof.lean").write_text(
                "theorem exactProof : True := by trivial\n", encoding="utf-8"
            )
            completed = subprocess.CompletedProcess([], 0, b"", b"")
            with (
                mock.patch.object(admission.shutil, "which", return_value="/usr/bin/false"),
                mock.patch.object(admission.subprocess, "run", return_value=completed) as run_call,
            ):
                result = admission._readonly_kernel_command(
                    checkout, ["lean", "Proof.lean"], timeout=30
                )
            self.assertIs(result, completed)
            argv = run_call.call_args.args[0]
            separator = argv.index("--")
            self.assertEqual(
                Path(argv[separator + 1]),
                Path.home()
                / ".elan/toolchains/leanprover--lean4---v4.29.0/bin/lean",
            )
            self.assertNotIn("/usr/bin/false", argv)

    def test_nonidentical_lean_transport_is_replayed_by_scheduler_and_reviewer(self) -> None:
        fixture = self.fixture()
        fixture.configure_checked_transport()
        with mock.patch.object(
            admission,
            "_lean_probe",
            wraps=admission._lean_probe,
        ):
            fixture.configure_exact_pinned_closure()
        # The transport receipt is environment-bound. Installing the provider
        # changes the authoritative root manifest, so build the receipt against
        # that final closure rather than preserving a stale pre-pin lock.
        fixture.configure_checked_transport()
        source = fixture.proposal["machine_proof"]["source"]
        source["match_kind"] = "checked_transport"
        fixture.proposal_path.write_text(canonical(fixture.proposal), encoding="utf-8")
        run(fixture.root, "git", "add", fixture.proposal_path.relative_to(fixture.root).as_posix())
        run(fixture.root, "git", "commit", "--amend", "--no-edit")
        fixture.authority = run(fixture.root, "git", "rev-parse", "HEAD")
        candidate = fixture.prepare()
        candidate_value = json.loads(candidate.read_text())
        scheduler_transport = candidate_value["candidate_verification"][
            "human_source_review"
        ]["machine_transport_authority"]
        self.assertEqual(
            scheduler_transport["schema_version"],
            admission.TRANSPORT_AUTHORITY_RESULT_SCHEMA,
        )
        self.assertEqual(scheduler_transport["replay"]["exit_code"], 0)
        self.assertEqual(
            scheduler_transport["provider_materialization"]["declaration"],
            "exactProof",
        )
        self.assertEqual(
            scheduler_transport["semantic_dependency"]["relation"],
            "direct_proof_body_constant_dependency",
        )
        self.assertEqual(
            scheduler_transport["semantic_dependency"]["joint_kernel_exit_code"],
            0,
        )
        review = fixture.review(candidate)
        review_value = json.loads(review.read_text())
        reviewer_transport = review_value["review_verification"][
            "human_source_review"
        ]["machine_transport_authority"]
        self.assertEqual(scheduler_transport, reviewer_transport)
        fixture.publish(
            candidate,
            review,
            regenerate=fixture.regenerate,
            validate_graph=lambda _root: None,
        )
        receipt = json.loads(
            (fixture.root / focus.receipt_relative_path(THEOREM)).read_text()
        )
        self.assertEqual(receipt["issuance_authority"]["issuance"]["state"], "published")
        authority = receipt["admission_authority"]
        self.assertEqual(
            authority["scheduler_verification"]["human_source_review"][
                "machine_transport_authority"
            ],
            authority["reviewer_verification"]["human_source_review"][
                "machine_transport_authority"
            ],
        )

    def test_checked_transport_independent_reproof_without_provider_dependency_fails(self) -> None:
        fixture = self.fixture()
        fixture.configure_checked_transport(depend_on_provider=False)
        with self.assertRaisesRegex(
            admission.AdmissionError,
            "not admissible for an unintegrated external source",
        ):
            fixture.prepare()

    def test_checked_transport_tampering_or_cross_system_provider_fails_closed(self) -> None:
        fixture = self.fixture()
        fixture.configure_checked_transport()
        validator = fixture.target.parent / "check_machine_transport.py"
        validator.write_text("print('worker-authored pass')\n", encoding="utf-8")
        with self.assertRaisesRegex(
            admission.AdmissionError,
            "not admissible for an unintegrated external source",
        ):
            fixture.prepare()

        fixture = Fixture()
        self.addCleanup(fixture.close)
        fixture.configure_checked_transport()
        fixture.proposal["machine_proof"]["source"]["formal_system"] = "Coq"
        fixture.write_proposal()
        with self.assertRaisesRegex(
            admission.AdmissionError,
            "not admissible for an unintegrated external source|only independently replayed Lean 4|generic provider replay authority",
        ):
            fixture.prepare()

    def test_proposal_derived_receipt_without_authority_cannot_open_phases(self) -> None:
        fixture = self.fixture()
        facts = admission._receipt_facts(fixture.proposal, fixture.decision())
        facts["generated_at"] = utc(dt.timedelta(minutes=-1))
        facts["admission_review"] = {
            "author": {"id": "scheduler-master-1", "role": "scheduler_master_lane"},
            "reviewer": {"id": "focus-reviewer-1", "role": "independent_reviewer"},
            "reviewed_at": utc(dt.timedelta(minutes=-2)),
            "decision": "admit_integration",
        }
        facts["admission_authority"] = None
        facts["issuance_authority"] = {
            "schema_version": admission.ISSUANCE_AUTHORITY_SCHEMA,
            "authority_revision": fixture.authority,
            "candidate_sha256": "1" * 64,
            "proposal_sha256": "2" * 64,
            "receipt_facts_sha256": "3" * 64,
            "scheduler_issuer": {
                "id": "scheduler-master-1",
                "role": "scheduler_master_lane",
            },
            "review_sha256": "4" * 64,
            "reviewer": {
                "id": "focus-reviewer-1",
                "role": "independent_reviewer",
            },
            "candidate_verification_sha256": "5" * 64,
            "review_verification_sha256": "6" * 64,
            "issuance": None,
        }
        receipt_path = fixture.root / focus.receipt_relative_path(THEOREM)
        receipt_path.write_text(canonical(facts), encoding="utf-8")
        result = focus.evaluate_target(fixture.root, THEOREM, runtime_root=fixture.runtime)
        self.assertFalse(result["valid"])
        self.assertFalse(any(result["phase_permissions"].values()))
        self.assertIn("schema_invalid", result["reason_codes"])

    def test_eligibility_replays_external_and_local_authorities(self) -> None:
        fixture = self.fixture()
        candidate = fixture.prepare()
        review = fixture.review(candidate)
        fixture.publish(
            candidate, review,
            regenerate=fixture.regenerate, validate_graph=lambda _root: None,
        )
        receipt_path = fixture.root / focus.receipt_relative_path(THEOREM)
        receipt = json.loads(receipt_path.read_text())
        receipt["admission_authority"]["scheduler_verification"][
            "kernel_authority_result"
        ]["declaration_type_sha256"] = "f" * 64
        verification = receipt["admission_authority"]["scheduler_verification"]
        verification.pop("verification_sha256")
        verification["verification_sha256"] = admission._digest(
            admission._canonical_json(verification)
        )
        receipt_path.write_text(canonical(receipt), encoding="utf-8")
        result = focus.evaluate_target(fixture.root, THEOREM, runtime_root=fixture.runtime)
        self.assertFalse(result["valid"])
        self.assertFalse(any(result["phase_permissions"].values()))

        fixture.target.write_text(
            "theorem target : False := by trivial\n", encoding="utf-8"
        )
        # Even with a previously valid receipt, current target bytes no longer
        # match the admitted base snapshot and must fail closed.
        result = focus.evaluate_target(fixture.root, THEOREM, runtime_root=fixture.runtime)
        self.assertFalse(result["valid"])

    def test_worker_cannot_write_receipt_or_self_review(self) -> None:
        fixture = self.fixture()
        injected = fixture.root / focus.receipt_relative_path(THEOREM)
        injected.write_text("{}\n", encoding="utf-8")
        run(fixture.root, "git", "add", str(injected.relative_to(fixture.root)))
        run(fixture.root, "git", "commit", "-m", "worker direct receipt attack")
        fixture.authority = run(fixture.root, "git", "rev-parse", "HEAD")
        with self.assertRaisesRegex(admission.AdmissionError, "not backed by a scheduler issuance"):
            fixture.prepare()
        # Restore a clean authority without weakening the direct-write guard.
        run(fixture.root, "git", "rm", str(injected.relative_to(fixture.root)))
        run(fixture.root, "git", "commit", "-m", "remove worker receipt attack")
        fixture.authority = run(fixture.root, "git", "rev-parse", "HEAD")
        decision = fixture.decision(
            reviewer={"id": "research-worker-1", "role": "independent_reviewer"}
        )
        with self.assertRaisesRegex(admission.AdmissionError, "must be independent"):
            fixture.prepare(decision)

    def test_tampered_evidence_or_candidate_and_expired_decision_are_rejected(self) -> None:
        fixture = self.fixture()
        expired = fixture.decision(expires_at=utc(dt.timedelta(seconds=-1)))
        with self.assertRaisesRegex(admission.AdmissionError, "expired"):
            fixture.prepare(expired)
        candidate = fixture.prepare()
        candidate_value = json.loads(candidate.read_text())
        candidate_value["receipt_facts"]["repository_gap"]["integration_plan"] = ["forged"]
        candidate.write_text(canonical(candidate_value), encoding="utf-8")
        with self.assertRaisesRegex(admission.AdmissionError, "does not bind"):
            fixture.review(candidate)

    def test_tampered_declaration_type_is_rejected_by_scheduler_probe(self) -> None:
        fixture = self.fixture()
        fixture.proposal["machine_proof"]["source"]["declaration_type_sha256"] = "f" * 64
        fixture.proposal["target_binding"]["declaration_type_sha256"] = "f" * 64
        fixture.proposal["statement_binding"]["target_declaration_type_sha256"] = "f" * 64
        fixture.proposal["statement_binding"]["human_statement_fingerprint"] = "f" * 64
        fixture.proposal["human_proof"]["statement_fingerprint"] = "f" * 64
        fixture.write_external_provenance()
        human_review = json.loads(fixture.human_review.read_text())
        human_review["statement_fingerprint"] = "f" * 64
        human_review["statement_crosswalk"]["statement_fingerprint"] = "f" * 64
        human_review["statement_crosswalk"]["target_declaration_type_sha256"] = "f" * 64
        human_subject = human_review["publication_timestamp"]["subject"]
        human_subject["statement_fingerprint"] = "f" * 64
        human_review["publication_timestamp"] = fixture.timestamp_token(
            human_subject,
            issued_at=human_review["publication_timestamp"]["issued_at"],
            token_id="fixture-human-proof-publication-tampered-type",
        )
        human_review.pop("review_sha256")
        human_review["review_sha256"] = admission._digest(
            admission._canonical_json(human_review)
        )
        fixture.human_review.write_text(canonical(human_review), encoding="utf-8")
        binding = next(
            row
            for row in fixture.proposal["evidence_bindings"]
            if row["role"] == "human_source_review"
        )
        binding["sha256"] = sha(fixture.human_review)
        run(fixture.root, "git", "add", str(fixture.human_review.relative_to(fixture.root)))
        run(fixture.root, "git", "commit", "-m", "independent source review update")
        fixture.base = run(fixture.root, "git", "rev-parse", "HEAD")
        fixture.proposal["repository_base_revision"] = fixture.base
        fixture.write_proposal()
        decision = fixture.decision()
        decision["human_source_authorization"].update(
            sha256=sha(fixture.human_review),
            review_sha256=human_review["review_sha256"],
        )
        with self.assertRaisesRegex(admission.AdmissionError, "declaration type"):
            fixture.prepare(decision)

    def test_informational_kernel_options_cannot_masquerade_as_replay(self) -> None:
        for command in (
            ["lean", "--version", "Proof.lean"],
            ["lean", "--help", "Proof.lean"],
            ["lake", "--version", "Proof.lean"],
            ["lake", "env", "lean", "--version", "Proof.lean"],
        ):
            with self.subTest(command=command):
                fixture = Fixture()
                self.addCleanup(fixture.close)
                fixture.proposal["machine_proof"]["source"]["kernel_replay"][
                    "command"
                ] = command
                fixture.write_proposal()
                with self.assertRaisesRegex(
                    admission.AdmissionError, "canonical Lean compilation"
                ):
                    fixture.prepare()

    def test_runtime_issuance_cache_is_not_authority_and_embedded_tamper_fails(self) -> None:
        fixture = self.fixture()
        candidate = fixture.prepare()
        review = fixture.review(candidate)
        issuance = fixture.publish(
            candidate,
            review,
            regenerate=fixture.regenerate,
            validate_graph=lambda _root: None,
        )
        self.assertTrue(fixture.evaluate()["valid"])
        original = issuance.read_bytes()
        issuance.unlink()
        self.assertTrue(fixture.evaluate()["valid"])
        issuance.write_bytes(original)
        receipt_path = fixture.root / focus.receipt_relative_path(THEOREM)
        receipt = json.loads(receipt_path.read_text())
        forged = receipt["issuance_authority"]["issuance"]
        forged["scheduler_issuer"]["id"] = "forged-scheduler"
        forged.pop("issuance_sha256")
        forged["issuance_sha256"] = admission._digest(
            admission._canonical_json(forged)
        )
        receipt_path.write_text(canonical(receipt), encoding="utf-8")
        tampered = focus.evaluate_target(
            fixture.root, THEOREM, runtime_root=fixture.runtime
        )
        self.assertFalse(tampered["valid"])
        self.assertFalse(any(tampered["phase_permissions"].values()))

    def test_forged_roles_and_self_consistent_hashes_cannot_replace_dual_signatures(self) -> None:
        fixture = self.fixture()
        candidate = fixture.prepare()
        review = fixture.review(candidate)
        fixture.publish(
            candidate,
            review,
            regenerate=fixture.regenerate,
            validate_graph=lambda _root: None,
        )
        receipt_path = fixture.root / focus.receipt_relative_path(THEOREM)
        receipt = json.loads(receipt_path.read_text())
        issuance = receipt["issuance_authority"]["issuance"]
        issuance["scheduler_issuer"] = {
            "id": "forged-scheduler",
            "role": "scheduler_master_lane",
        }
        receipt["issuance_authority"]["scheduler_issuer"] = issuance[
            "scheduler_issuer"
        ]
        issuance.pop("issuance_sha256")
        issuance["issuance_sha256"] = admission._digest(
            admission._canonical_json(issuance)
        )
        receipt_path.write_text(canonical(receipt), encoding="utf-8")
        result = fixture.evaluate()
        self.assertFalse(result["valid"])
        self.assertFalse(any(result["phase_permissions"].values()))

    def test_tampered_final_payload_or_reviewer_signature_fails_closed(self) -> None:
        for mutation in ("payload", "signature"):
            with self.subTest(mutation=mutation):
                fixture = Fixture()
                self.addCleanup(fixture.close)
                candidate = fixture.prepare()
                review = fixture.review(candidate)
                fixture.publish(
                    candidate,
                    review,
                    regenerate=fixture.regenerate,
                    validate_graph=lambda _root: None,
                )
                receipt_path = fixture.root / focus.receipt_relative_path(THEOREM)
                receipt = json.loads(receipt_path.read_text())
                if mutation == "payload":
                    receipt["repository_gap"]["integration_plan"] = ["forged plan"]
                else:
                    receipt["issuance_authority"]["issuance"][
                        "reviewer_signature"
                    ] = "0" * 128
                    issuance = receipt["issuance_authority"]["issuance"]
                    issuance.pop("issuance_sha256")
                    issuance["issuance_sha256"] = admission._digest(
                        admission._canonical_json(issuance)
                    )
                receipt_path.write_text(canonical(receipt), encoding="utf-8")
                result = fixture.evaluate()
                self.assertFalse(result["valid"])
                self.assertFalse(any(result["phase_permissions"].values()))

    def test_signing_key_must_match_pinned_anchor_and_be_mode_0600(self) -> None:
        fixture = self.fixture()
        candidate = fixture.prepare()
        fixture.reviewer_key_path.chmod(0o644)
        with self.assertRaisesRegex(admission.AdmissionError, "mode 0600"):
            fixture.review(candidate)
        fixture.reviewer_key_path.chmod(0o600)
        wrong = Ed25519PrivateKey.generate()
        fixture.reviewer_key_path.write_bytes(
            wrong.private_bytes(
                serialization.Encoding.PEM,
                serialization.PrivateFormat.PKCS8,
                serialization.NoEncryption(),
            )
        )
        with self.assertRaisesRegex(admission.AdmissionError, "active trust anchor"):
            fixture.review(candidate)

    def test_scheduler_decision_requires_owner_only_staging(self) -> None:
        fixture = self.fixture()
        decisions = fixture.runtime / "focus-admission" / "decisions"
        decisions.mkdir(parents=True)
        decisions.chmod(0o700)
        decision = decisions / "decision.json"
        decision.write_text(canonical(fixture.decision()), encoding="utf-8")
        decision.chmod(0o600)
        self.assertEqual(
            admission.load_scheduler_decision(fixture.runtime, decision),
            fixture.decision(),
        )
        for mutation, message in (
            ("file_mode", "scheduler-owned staging"),
            ("parent_mode", "lineage is not owner-controlled"),
            ("symlink", "scheduler-owned staging"),
        ):
            with self.subTest(mutation=mutation):
                decision.chmod(0o600)
                decisions.chmod(0o700)
                alias = decisions / "alias.json"
                alias.unlink(missing_ok=True)
                selected = decision
                if mutation == "file_mode":
                    decision.chmod(0o640)
                elif mutation == "parent_mode":
                    decisions.chmod(0o720)
                else:
                    alias.symlink_to(decision.name)
                    selected = alias
                with self.assertRaisesRegex(admission.AdmissionError, message):
                    admission.load_scheduler_decision(fixture.runtime, selected)

    def test_recovery_rejects_external_runtime_before_blueprint_write(self) -> None:
        fixture = self.fixture()
        original = fixture.blueprint.read_bytes()
        external = Path(fixture.temp.name) / "attacker-runtime"
        external.mkdir(mode=0o700)
        self.write_wal(
            fixture,
            [{
                "path": "Docs/Stage1_Blueprint_v2.md",
                "existed": True,
                "mode": 0o644,
                "content_base64": base64.b64encode(b"forged blueprint\n").decode("ascii"),
            }],
            runtime=external,
        )
        with self.assertRaisesRegex(admission.AdmissionError, "canonical repository runtime"):
            admission.recover_focus_admission_wal(fixture.root, external)
        self.assertEqual(fixture.blueprint.read_bytes(), original)

    def test_recovery_rejects_non_authoritative_blueprint_snapshot(self) -> None:
        fixture = self.fixture()
        original = fixture.blueprint.read_bytes()
        self.write_wal(
            fixture,
            [{
                "path": "Docs/Stage1_Blueprint_v2.md",
                "existed": True,
                "mode": 0o600,
                "content_base64": base64.b64encode(b"forged blueprint\n").decode("ascii"),
            }],
        )
        with self.assertRaisesRegex(admission.AdmissionError, "not authoritative"):
            admission.recover_focus_admission_wal(fixture.root, fixture.runtime)
        self.assertEqual(fixture.blueprint.read_bytes(), original)

    def test_recovery_rejects_symlink_lineage_mode_and_schema_attacks(self) -> None:
        for mutation, message in (
            ("ancestor_symlink", "runtime lineage"),
            ("wal_symlink", "missing or unsafe"),
            ("wal_mode", "mode 0600"),
            ("directory_mode", "owner-controlled"),
            ("extra_field", "fields or schema"),
            ("unsafe_target", "unsafe path"),
        ):
            with self.subTest(mutation=mutation):
                fixture = Fixture()
                self.addCleanup(fixture.close)
                graph_before = fixture.graph.read_bytes()
                rows = [{
                    "path": "Docs/Stage1_Theorem_DAG_v2.json",
                    "existed": True,
                    "mode": 0o644,
                    "content_base64": base64.b64encode(graph_before).decode("ascii"),
                }]
                if mutation == "ancestor_symlink":
                    cron = fixture.root / ".cron"
                    shutil.rmtree(cron)
                    real = fixture.root / "runtime-real"
                    (real / "stage1-v2-app-server").mkdir(parents=True)
                    cron.symlink_to(real, target_is_directory=True)
                    self.write_wal(
                        fixture,
                        rows,
                        runtime=real / "stage1-v2-app-server",
                    )
                else:
                    wal = self.write_wal(
                        fixture,
                        ([{**rows[0], "path": "unrelated.txt"}]
                         if mutation == "unsafe_target" else rows),
                        extra={"unexpected": True} if mutation == "extra_field" else None,
                    )
                    if mutation == "wal_symlink":
                        payload = wal.with_name("payload.json")
                        wal.replace(payload)
                        wal.symlink_to(payload.name)
                    elif mutation == "wal_mode":
                        wal.chmod(0o640)
                    elif mutation == "directory_mode":
                        fixture.runtime.chmod(0o720)
                with self.assertRaisesRegex(admission.AdmissionError, message):
                    admission.recover_focus_admission_wal(fixture.root, fixture.runtime)
                self.assertEqual(fixture.graph.read_bytes(), graph_before)

    def test_recovery_rejects_wrong_owner_when_privileged(self) -> None:
        if os.geteuid() != 0:
            self.skipTest("requires chown capability")
        fixture = self.fixture()
        graph_before = fixture.graph.read_bytes()
        wal = self.write_wal(
            fixture,
            [{
                "path": "Docs/Stage1_Theorem_DAG_v2.json",
                "existed": True,
                "mode": 0o644,
                "content_base64": base64.b64encode(graph_before).decode("ascii"),
            }],
        )
        os.chown(wal, 1, -1)
        with self.assertRaisesRegex(admission.AdmissionError, "mode 0600 regular file"):
            admission.recover_focus_admission_wal(fixture.root, fixture.runtime)
        self.assertEqual(fixture.graph.read_bytes(), graph_before)

    def test_recovery_restores_legal_snapshot_and_removes_journal(self) -> None:
        fixture = self.fixture()
        expected = fixture.graph.read_bytes()
        fixture.graph.write_bytes(b"partially published graph\n")
        wal = self.write_wal(
            fixture,
            [{
                "path": "Docs/Stage1_Theorem_DAG_v2.json",
                "existed": True,
                "mode": 0o644,
                "content_base64": base64.b64encode(expected).decode("ascii"),
            }],
        )
        self.assertTrue(admission.recover_focus_admission_wal(fixture.root, fixture.runtime))
        self.assertEqual(fixture.graph.read_bytes(), expected)
        self.assertEqual(stat.S_IMODE(fixture.graph.stat().st_mode), 0o644)
        self.assertFalse(wal.exists())

    def test_candidate_and_review_loader_reject_mode_symlink_and_leaf_swap(self) -> None:
        fixture = self.fixture()
        candidate = fixture.prepare()
        candidate.chmod(0o640)
        with self.assertRaisesRegex(admission.AdmissionError, "mode 0600"):
            admission._reload_candidate(fixture.root, fixture.runtime, candidate)
        candidate.chmod(0o600)

        alias = candidate.with_name("alias.json")
        alias.symlink_to(candidate.name)
        with self.assertRaisesRegex(admission.AdmissionError, "missing or unsafe"):
            admission._load_runtime_record(
                alias,
                candidate.parent,
                "focus candidate",
                root=fixture.root,
                allowed_owner_uids={os.geteuid()},
            )

        original_open = admission.os.open
        swapped = False

        def swap_before_leaf(path: object, flags: int, *args: object, **kwargs: object) -> int:
            nonlocal swapped
            if path == candidate.name and not (flags & os.O_DIRECTORY) and not swapped:
                swapped = True
                target = candidate.with_name("replacement.json")
                target.write_bytes(candidate.read_bytes())
                target.chmod(0o600)
                candidate.unlink()
                candidate.symlink_to(target.name)
            return original_open(path, flags, *args, **kwargs)

        with mock.patch.object(admission.os, "open", side_effect=swap_before_leaf), \
                self.assertRaisesRegex(admission.AdmissionError, "missing or unsafe"):
            admission._load_runtime_record(
                candidate,
                candidate.parent,
                "focus candidate",
                root=fixture.root,
                allowed_owner_uids={os.geteuid()},
            )

    def test_configured_distinct_reviewer_can_read_scheduler_candidate(self) -> None:
        fixture = self.fixture()
        candidate = fixture.prepare()
        reviewer_uid = os.geteuid() + 12345
        repo_owner = os.geteuid()
        with mock.patch.dict(
            os.environ, {"STAGE1_REVIEWER_UID": str(reviewer_uid)}
        ), mock.patch.object(
            admission.os, "geteuid", return_value=reviewer_uid
        ), mock.patch.object(admission, "_repo_owner", return_value=repo_owner):
            loaded, proposal = admission._reload_candidate(
                fixture.root,
                fixture.runtime,
                candidate,
                allowed_caller_uids=admission._reviewer_owner_uids(fixture.root),
            )
        self.assertEqual(loaded["theorem_id"], THEOREM)
        self.assertEqual(proposal["theorem_id"], THEOREM)

    def test_signed_principals_must_match_trust_anchor_acl(self) -> None:
        fixture = self.fixture()
        candidate = fixture.prepare()
        review = fixture.review(candidate)
        fixture.publish(
            candidate,
            review,
            regenerate=fixture.regenerate,
            validate_graph=lambda _root: None,
        )
        receipt = fixture.root / focus.receipt_relative_path(THEOREM)
        original = json.loads(receipt.read_text())
        for location, actor_id in (
            (("issuance_authority", "scheduler_issuer", "id"), "forged-scheduler"),
            (("issuance_authority", "reviewer", "id"), "forged-reviewer"),
        ):
            with self.subTest(location=location):
                forged = copy.deepcopy(original)
                target: dict = forged
                for key in location[:-1]:
                    target = target[key]
                target[location[-1]] = actor_id
                # Mirror the actor through every semantic surface and recompute
                # the non-cryptographic hashes. The pinned key-to-principal ACL
                # must still reject it.
                role = location[-2]
                issuance = forged["issuance_authority"]["issuance"]
                issuance[role]["id"] = actor_id
                forged["admission_review"][
                    "author" if role == "scheduler_issuer" else "reviewer"
                ]["id"] = actor_id
                issuance.pop("issuance_sha256")
                issuance["issuance_sha256"] = admission._digest(
                    admission._canonical_json(issuance)
                )
                receipt.write_text(canonical(forged), encoding="utf-8")
                with mock.patch.object(
                    focus, "TRUST_ANCHORS_SHA256", fixture.trust_anchor_sha
                ):
                    result = focus.evaluate_target(
                        fixture.root, THEOREM, runtime_root=fixture.runtime
                    )
                self.assertFalse(result["valid"])
                self.assertFalse(any(result["phase_permissions"].values()))
                receipt.write_text(canonical(original), encoding="utf-8")

    def test_issuance_timestamp_must_equal_receipt_generation(self) -> None:
        fixture = self.fixture()
        candidate = fixture.prepare()
        review = fixture.review(candidate)
        fixture.publish(
            candidate,
            review,
            regenerate=fixture.regenerate,
            validate_graph=lambda _root: None,
        )
        receipt_path = fixture.root / focus.receipt_relative_path(THEOREM)
        receipt = json.loads(receipt_path.read_text())
        receipt["issuance_authority"]["issuance"]["published_at"] = utc(
            dt.timedelta(minutes=-10)
        )
        issuance = receipt["issuance_authority"]["issuance"]
        issuance.pop("issuance_sha256")
        issuance["issuance_sha256"] = admission._digest(
            admission._canonical_json(issuance)
        )
        receipt_path.write_text(canonical(receipt), encoding="utf-8")
        result = fixture.evaluate()
        self.assertFalse(result["valid"])
        self.assertFalse(any(result["phase_permissions"].values()))

    def test_retired_and_revoked_trust_anchor_policy(self) -> None:
        fixture = self.fixture()
        anchors = json.loads(
            (fixture.root / focus.TRUST_ANCHORS_RELATIVE_PATH).read_text()
        )
        scheduler = anchors["keys"][0]
        scheduler["status"] = "retired"
        scheduler["not_after"] = "2027-01-01T00:00:00Z"
        replacement = Ed25519PrivateKey.generate()
        anchors["keys"].append(
            {
                "key_id": "fixture-scheduler-2",
                "role": "scheduler_issuance",
                "principal_id": "scheduler-master-2",
                "public_key_hex": replacement.public_key().public_bytes_raw().hex(),
                "status": "active",
                "not_before": "2027-01-01T00:00:00Z",
                "not_after": None,
            }
        )
        trust_path = fixture.root / focus.TRUST_ANCHORS_RELATIVE_PATH
        trust_path.write_text(canonical(anchors), encoding="utf-8")
        digest = sha(trust_path)
        with mock.patch.object(focus, "TRUST_ANCHORS_SHA256", digest):
            key_id, principal_id, _key = focus._trust_anchor(
                fixture.root,
                "scheduler_issuance",
                key_id="fixture-scheduler-1",
                issued_at=dt.datetime(2026, 6, 1, tzinfo=dt.timezone.utc),
            )
            self.assertEqual((key_id, principal_id), (
                "fixture-scheduler-1", "scheduler-master-1"
            ))
            scheduler["status"] = "revoked"
            trust_path.write_text(canonical(anchors), encoding="utf-8")
            revoked_digest = sha(trust_path)
        with mock.patch.object(focus, "TRUST_ANCHORS_SHA256", revoked_digest):
            with self.assertRaisesRegex(focus.EligibilityError, "revoked"):
                focus._trust_anchor(
                    fixture.root,
                    "scheduler_issuance",
                    key_id="fixture-scheduler-1",
                    issued_at=dt.datetime(2026, 6, 1, tzinfo=dt.timezone.utc),
                )

    def test_exact_pinned_source_must_match_authoritative_lake_manifest(self) -> None:
        fixture = self.fixture()
        fixture.proposal["machine_evidence_class"] = "exact_pinned_closure"
        fixture.proposal["repository_gap"]["local_presence"] = "pinned_dependency"
        fixture.write_proposal()
        with self.assertRaisesRegex(
            admission.AdmissionError,
            "absent or ambiguous in the authoritative Lake manifest",
        ):
            fixture.prepare()

    def test_exact_pinned_source_replays_from_live_manifest_package(self) -> None:
        fixture = self.fixture()
        fixture.configure_exact_pinned_closure()
        source = fixture.proposal["machine_proof"]["source"]
        provider = admission._pinned_manifest_provider(
            fixture.root, fixture.authority, source
        )
        observed = admission._verify_local_pinned_provider(
            fixture.root,
            fixture.authority,
            source,
            provider,
            command_runner=admission._readonly_kernel_command,
        )
        self.assertEqual(observed["revision"], fixture.external_revision)
        self.assertEqual(observed["file_sha256"], sha(fixture.external_source))
        self.assertEqual(observed["terminal_proof_body_sha256"], fixture.body_sha)
        self.assertEqual(observed["declaration_type_sha256"], fixture.type_sha)

    def test_exact_pinned_source_uses_root_closure_not_provider_local_lake(self) -> None:
        fixture = self.fixture()
        fixture.configure_exact_pinned_closure(with_provider_dependency=True)
        source = fixture.proposal["machine_proof"]["source"]
        provider = admission._pinned_manifest_provider(
            fixture.root, fixture.authority, source
        )
        package = (
            fixture.root / "Formalizations" / "Lean" / ".lake" /
            "packages" / provider["cache_name"]
        )
        # The provider-local closure is deliberately absent.  A replay rooted in
        # this package would try to fetch its dependency, whereas the repository
        # root manifest/cache already contains the exact pinned closure.
        shutil.rmtree(package / ".lake")
        calls: list[tuple[Path, dict[str, object]]] = []

        def root_only_runner(
            checkout: Path, command: list[str], **kwargs: object
        ) -> subprocess.CompletedProcess[bytes]:
            calls.append((checkout, dict(kwargs)))
            if checkout == package:
                return subprocess.CompletedProcess(
                    command, 1, b"", b"provider-local dependencies unavailable"
                )
            return admission._readonly_kernel_command(
                checkout, command, **kwargs
            )

        observed = admission._verify_local_pinned_provider(
            fixture.root,
            fixture.authority,
            source,
            provider,
            command_runner=root_only_runner,
        )
        lean_root = fixture.root / "Formalizations" / "Lean"
        self.assertEqual([checkout for checkout, _kwargs in calls], [lean_root, lean_root])
        self.assertFalse(any(kwargs.get("writable") for _checkout, kwargs in calls))
        self.assertIsNotNone(calls[0][1].get("writable_path"))
        self.assertIsNone(calls[1][1].get("writable_path"))
        self.assertEqual(observed["declaration_type_sha256"], fixture.type_sha)

    def test_exact_pinned_source_cannot_borrow_a_stale_cached_olean(self) -> None:
        fixture = self.fixture()
        fixture.configure_exact_pinned_closure()
        source = copy.deepcopy(fixture.proposal["machine_proof"]["source"])
        previous_revision = fixture.external_revision
        provider = admission._pinned_manifest_provider(fixture.root, fixture.authority, source)
        package = (
            fixture.root / "Formalizations" / "Lean" / ".lake" /
            "packages" / provider["cache_name"]
        )
        stale_olean = package / ".lake" / "build" / "lib" / "lean" / "Proof.olean"
        self.assertTrue(stale_olean.is_file())
        broken = b"theorem exactProof : True := by exact False.elim (by trivial)\n"
        fixture.external_source.write_bytes(broken)
        run(fixture.external, "git", "add", "Proof.lean")
        run(fixture.external, "git", "commit", "-m", "break provider source")
        broken_revision = run(fixture.external, "git", "rev-parse", "HEAD")
        run(package, "git", "fetch", "--quiet", "origin", broken_revision)
        run(package, "git", "checkout", "--quiet", "--detach", broken_revision)
        source["revision"] = broken_revision
        source["file_sha256"] = sha(fixture.external_source)
        body_sha, _text = admission._declaration_region(broken, "exactProof")
        source["terminal_proof_body"]["sha256"] = body_sha
        manifest = fixture.root / "Formalizations" / "Lean" / "lake-manifest.json"
        manifest_value = json.loads(manifest.read_text(encoding="utf-8"))
        manifest_value["packages"][0]["rev"] = broken_revision
        manifest_value["packages"][0]["inputRev"] = broken_revision
        manifest.write_text(json.dumps(manifest_value) + "\n", encoding="utf-8")
        lakefile = fixture.root / "Formalizations" / "Lean" / "lakefile.lean"
        lakefile.write_text(
            lakefile.read_text(encoding="utf-8").replace(
                previous_revision, broken_revision
            ),
            encoding="utf-8",
        )
        run(
            fixture.root,
            "git", "add",
            manifest.relative_to(fixture.root).as_posix(),
            lakefile.relative_to(fixture.root).as_posix(),
        )
        run(fixture.root, "git", "commit", "-m", "pin broken provider source")
        fixture.authority = run(fixture.root, "git", "rev-parse", "HEAD")
        provider = admission._pinned_manifest_provider(
            fixture.root, fixture.authority, source
        )

        with self.assertRaisesRegex(admission.AdmissionError, "Lake replay failed"):
            admission._verify_local_pinned_provider(
                fixture.root,
                fixture.authority,
                source,
                provider,
                command_runner=admission._readonly_kernel_command,
            )

    def test_exact_pinned_live_package_identity_and_replay_fail_closed(self) -> None:
        cases = (
            ("origin", "origin URL"),
            ("head", "revision disagrees"),
            ("dirty", "clean exact checkout"),
            ("source", "source differs"),
            ("body", "proof body differs"),
            ("replay", "Lake replay failed"),
            ("root_lakefile", "tracked root Lakefile"),
        )
        for mutation, message in cases:
            with self.subTest(mutation=mutation):
                fixture = self.fixture()
                fixture.configure_exact_pinned_closure()
                source = copy.deepcopy(fixture.proposal["machine_proof"]["source"])
                provider = admission._pinned_manifest_provider(
                    fixture.root, fixture.authority, source
                )
                package = (
                    fixture.root / "Formalizations" / "Lean" / ".lake" /
                    "packages" / provider["cache_name"]
                )
                runner = admission._readonly_kernel_command
                if mutation == "origin":
                    run(package, "git", "remote", "set-url", "origin", "https://example.invalid/wrong.git")
                elif mutation == "head":
                    run(package, "git", "config", "user.email", "tests@example.invalid")
                    run(package, "git", "config", "user.name", "Focus Admission Test")
                    (package / "Other.lean").write_text(
                        "theorem other : True := by trivial\n", encoding="utf-8"
                    )
                    run(package, "git", "add", "Other.lean")
                    run(package, "git", "commit", "-m", "different package head")
                elif mutation == "dirty":
                    (package / "untracked.txt").write_text("dirty\n", encoding="utf-8")
                elif mutation == "source":
                    source["file_sha256"] = "0" * 64
                elif mutation == "body":
                    source["terminal_proof_body"]["sha256"] = "0" * 64
                elif mutation == "root_lakefile":
                    lakefile = fixture.root / "Formalizations" / "Lean" / "lakefile.lean"
                    lakefile.write_text(
                        "import Lake\nopen Lake DSL\npackage «FocusAdmissionFixture»\n",
                        encoding="utf-8",
                    )
                    run(fixture.root, "git", "add", lakefile.relative_to(fixture.root).as_posix())
                    run(fixture.root, "git", "commit", "-m", "remove root dependency declaration")
                    fixture.authority = run(fixture.root, "git", "rev-parse", "HEAD")
                else:
                    def runner(*_args: object, **_kwargs: object) -> subprocess.CompletedProcess[bytes]:
                        return subprocess.CompletedProcess([], 1, b"", b"forced failure")
                with self.assertRaisesRegex(admission.AdmissionError, message):
                    admission._verify_local_pinned_provider(
                        fixture.root,
                        fixture.authority,
                        source,
                        provider,
                        command_runner=runner,
                    )

    def test_false_or_placeholder_local_target_cannot_borrow_external_type(self) -> None:
        fixture = self.fixture()
        fixture.target.write_text(
            "theorem target : False := by sorry\n", encoding="utf-8"
        )
        run(fixture.root, "git", "add", str(fixture.target.relative_to(fixture.root)))
        run(fixture.root, "git", "commit", "-m", "adversarial local target")
        fixture.base = run(fixture.root, "git", "rev-parse", "HEAD")
        fixture.proposal["repository_base_revision"] = fixture.base
        fixture.proposal["target_binding"]["file_sha256"] = sha(fixture.target)
        # Retain the external True fingerprint: this was previously enough to
        # make the complete admission transaction succeed.
        fixture.write_proposal()
        with self.assertRaisesRegex(
            admission.AdmissionError, "local Lean target contains a prohibited construct"
        ):
            fixture.prepare()

    def test_worker_metadata_and_untyped_human_source_text_cannot_admit(self) -> None:
        fixture = self.fixture()
        fixture.human_review.write_text(
            canonical(
                {
                    "theorem_id": THEOREM,
                    "text": "worker says this arbitrary text is a reviewed proof",
                    "accepted": True,
                    "license": "CC-BY-4.0",
                }
            ),
            encoding="utf-8",
        )
        binding = next(
            row
            for row in fixture.proposal["evidence_bindings"]
            if row["role"] == "human_source_review"
        )
        binding["sha256"] = sha(fixture.human_review)
        run(fixture.root, "git", "add", str(fixture.human_review.relative_to(fixture.root)))
        fixture.write_proposal()
        malformed_review_sha = "f" * 64
        decision = fixture.decision(
            human_source_authorization={
                "path": f"Stage1_Instances/{THEOREM}/{fixture.human_review.name}",
                "sha256": sha(fixture.human_review),
                "review_sha256": malformed_review_sha,
                "reviewer": {
                    "id": "human-source-reviewer",
                    "role": "independent_reviewer",
                },
                "decision": "accepted",
            }
        )
        with self.assertRaisesRegex(
            admission.AdmissionError, "human source review fields"
        ):
            fixture.prepare(decision)

    def test_frontier_probability_below_threshold_fails_before_review(self) -> None:
        fixture = self.fixture()
        fixture.proposal["machine_evidence_class"] = "no_exact_candidate_as_of"
        fixture.proposal["execution_disposition"] = "frontier_exception"
        fixture.proposal["machine_proof"] = {
            "status": "no_usable_exact_artifact_located",
            "negative_search_boundary": "bounded fixture search only",
            "negative_search_inventory": [{
                "source": "fixture index",
                "revision_or_snapshot": "snapshot-1",
                "queries": ["exactProof"],
                "searched_at": utc(dt.timedelta(hours=-4)),
                "candidate_rejections": [],
            }],
            "source": None,
        }
        human_review_binding = next(
            copy.deepcopy(row)
            for row in fixture.proposal["evidence_bindings"]
            if row["role"] == "human_source_review"
        )
        estimate = copy.deepcopy(fixture.proposal["evidence_bindings"][0])
        estimate["role"] = "frontier_estimate_basis"
        fixture.proposal["evidence_bindings"] = [human_review_binding, estimate]
        fixture.proposal["frontier_request"] = {
            "root_obligation": {"id": "root", "statement_fingerprint": fixture.type_sha},
            "evidence": [estimate],
        }
        fixture.write_proposal()
        authorization = {
            "assigned_worker": {"id": "proof-worker-1", "role": "proof_worker"},
            "estimator": {"id": "estimator-1", "role": "scheduler_estimator"},
            "estimated_at": utc(dt.timedelta(minutes=-30)),
            "estimation_method": "calibrated fixture",
            "completion_probability": 0.699,
            "budget": {
                "scope": "root only", "wall_clock_seconds": 60, "token_limit": 100,
                "compute_seconds": 60, "disk_bytes": 1024, "concurrency_limit": 1,
            },
            "milestones": [{
                "id": "close_root", "deadline_at": utc(dt.timedelta(hours=1)),
                "evidence_role": "root_proof_closure",
            }],
            "validator": {
                "path": estimate["path"], "sha256": estimate["sha256"],
                "command": ["python3", estimate["path"]],
            },
            "stop_conditions": sorted(focus.REQUIRED_FRONTIER_STOP_CONDITIONS),
            "attempt_limit": 1,
            "lease_expires_at": utc(dt.timedelta(hours=2)),
        }
        decision = fixture.decision(
            admission_decision="admit_frontier_exception",
            human_source_authorization=fixture.decision()[
                "human_source_authorization"
            ],
            frontier_authorization=authorization,
        )
        with self.assertRaisesRegex(admission.AdmissionError, "below 0.70"):
            fixture.prepare(decision)

    def test_frontier_review_requires_separately_authored_substantive_input(self) -> None:
        fixture = self.fixture()
        fixture.proposal["machine_evidence_class"] = "no_exact_candidate_as_of"
        fixture.proposal["execution_disposition"] = "frontier_exception"
        fixture.proposal["machine_proof"] = {
            "status": "no_usable_exact_artifact_located",
            "negative_search_boundary": "bounded fixture search only",
            "negative_search_inventory": [{
                "source": "fixture index",
                "revision_or_snapshot": "snapshot-1",
                "queries": ["exactProof"],
                "searched_at": utc(dt.timedelta(hours=-4)),
                "candidate_rejections": [],
            }],
            "source": None,
        }
        human_review_binding = next(
            copy.deepcopy(row)
            for row in fixture.proposal["evidence_bindings"]
            if row["role"] == "human_source_review"
        )
        estimate = copy.deepcopy(fixture.proposal["evidence_bindings"][0])
        estimate["role"] = "frontier_estimate_basis"
        fixture.proposal["evidence_bindings"] = [human_review_binding, estimate]
        fixture.proposal["frontier_request"] = {
            "root_obligation": {"id": "root", "statement_fingerprint": fixture.type_sha},
            "evidence": [estimate],
        }
        fixture.write_proposal()
        authorization = {
            "assigned_worker": {"id": "proof-worker-1", "role": "proof_worker"},
            "estimator": {"id": "estimator-1", "role": "scheduler_estimator"},
            "estimated_at": utc(dt.timedelta(minutes=-30)),
            "estimation_method": "calibrated fixture",
            "completion_probability": 0.75,
            "budget": {
                "scope": "root only", "wall_clock_seconds": 60, "token_limit": 100,
                "compute_seconds": 60, "disk_bytes": 1024, "concurrency_limit": 1,
            },
            "milestones": [{
                "id": "close_root", "deadline_at": utc(dt.timedelta(hours=1)),
                "evidence_role": "root_proof_closure",
            }],
            "validator": {
                "path": estimate["path"], "sha256": estimate["sha256"],
                "command": ["python3", estimate["path"]],
            },
            "stop_conditions": sorted(focus.REQUIRED_FRONTIER_STOP_CONDITIONS),
            "attempt_limit": 1,
            "lease_expires_at": utc(dt.timedelta(hours=2)),
        }
        decision = fixture.decision(
            admission_decision="admit_frontier_exception",
            frontier_authorization=authorization,
        )
        candidate = fixture.prepare(decision)
        with mock.patch.object(
            admission.focus_eligibility,
            "TRUST_ANCHORS_SHA256",
            fixture.trust_anchor_sha,
        ), self.assertRaisesRegex(
            admission.AdmissionError, "frontier independent review input path"
        ):
            admission.review_focus_admission(
                fixture.root,
                fixture.runtime,
                candidate,
                {"id": "focus-reviewer-1", "role": "independent_reviewer"},
                reviewer_signing_key_path=fixture.reviewer_key_path,
            )

        candidate_value = json.loads(candidate.read_text())
        frontier = candidate_value["receipt_facts"]["frontier_exception"]
        review_input = {
            "schema_version": admission.FRONTIER_REVIEW_INPUT_SCHEMA,
            "candidate_sha256": candidate_value["candidate_sha256"],
            "theorem_id": THEOREM,
            "reviewer": {"id": "focus-reviewer-1", "role": "independent_reviewer"},
            "authored_at": utc(dt.timedelta(minutes=-10)),
            "decision": "approved",
            "assessed_completion_probability": 0.74,
            "estimation_method_assessment": "Independent calibration against two prior bounded attempts.",
            "comparables": ["fixture-attempt-a", "fixture-attempt-b"],
            "budget_assessment": frontier["budget"],
            "milestone_assessment": frontier["milestones"],
            "validator_assessment": frontier["validator"],
            "stop_condition_assessment": frontier["stop_conditions"],
            "findings": ["Probability remains above threshold under the declared budget."],
        }
        review_input["review_input_sha256"] = admission._digest(
            admission._canonical_json(review_input)
        )
        path = admission._frontier_review_input_path(
            fixture.runtime, candidate_value["candidate_sha256"]
        )
        path.parent.mkdir(parents=True)
        path.write_text(canonical(review_input), encoding="utf-8")
        path.chmod(0o600)
        with mock.patch.object(
            admission.focus_eligibility,
            "TRUST_ANCHORS_SHA256",
            fixture.trust_anchor_sha,
        ):
            review = admission.review_focus_admission(
                fixture.root,
                fixture.runtime,
                candidate,
                {"id": "focus-reviewer-1", "role": "independent_reviewer"},
                reviewer_signing_key_path=fixture.reviewer_key_path,
            )
        review_value = json.loads(review.read_text())
        self.assertEqual(
            review_value["frontier_review_input"]["review_input_sha256"],
            review_input["review_input_sha256"],
        )
        self.assertEqual(review_value["decision"], "approved")
        receipt_payload = admission._final_receipt_payload(
            candidate_value, review_value
        )
        durable = receipt_payload["frontier_exception"]["independent_review"]
        self.assertEqual(
            durable["assessed_completion_probability"],
            review_input["assessed_completion_probability"],
        )
        self.assertEqual(durable["comparables"], review_input["comparables"])
        self.assertEqual(durable["findings"], review_input["findings"])
        self.assertEqual(durable["budget_assessment"], frontier["budget"])
        self.assertEqual(durable["milestone_assessment"], frontier["milestones"])
        self.assertEqual(durable["validator_assessment"], frontier["validator"])
        self.assertEqual(
            durable["stop_condition_assessment"], frontier["stop_conditions"]
        )
        self.assertEqual(durable["authored_at"], review_input["authored_at"])
        self.assertEqual(durable["reviewed_at"], review_value["reviewed_at"])
        self.assertEqual(
            review_value["receipt_payload_sha256"],
            admission._digest(admission._canonical_json(receipt_payload)),
        )

    def test_publication_and_dag_failure_restore_receipt_graph_and_blueprint(self) -> None:
        for failure in ("regenerate", "validate"):
            with self.subTest(failure=failure):
                fixture = Fixture()
                self.addCleanup(fixture.close)
                candidate = fixture.prepare()
                review = fixture.review(candidate)
                graph_before = fixture.graph.read_bytes()
                blueprint_before = fixture.blueprint.read_bytes()

                def regenerate(root: Path) -> None:
                    fixture.regenerate(root)
                    if failure == "regenerate":
                        raise admission.AdmissionError("injected regeneration failure")

                def validate(_root: Path) -> None:
                    if failure == "validate":
                        raise admission.AdmissionError("injected DAG validation failure")

                with self.assertRaisesRegex(admission.AdmissionError, "injected"):
                    fixture.publish(
                        candidate,
                        review,
                        regenerate=regenerate,
                        validate_graph=validate,
                    )
                self.assertFalse(
                    (fixture.root / focus.receipt_relative_path(THEOREM)).exists()
                )
                self.assertEqual(fixture.graph.read_bytes(), graph_before)
                self.assertEqual(fixture.blueprint.read_bytes(), blueprint_before)
                self.assertFalse((fixture.runtime / "focus-admission-wal.json").exists())

    def test_publication_that_changes_blueprint_rolls_back_while_paused(self) -> None:
        fixture = self.fixture()
        candidate = fixture.prepare()
        review = fixture.review(candidate)
        graph_before = fixture.graph.read_bytes()
        blueprint_before = fixture.blueprint.read_bytes()
        paused = fixture.runtime / "PAUSED"
        paused.write_text("paused\n", encoding="utf-8")

        def mutate_blueprint(root: Path) -> None:
            fixture.regenerate(root)
            fixture.blueprint.write_bytes(b"unauthorized checklist mutation\n")

        candidate_value = json.loads(candidate.read_text())
        external_authority = candidate_value["candidate_verification"][
            "kernel_authority_result"
        ]["replay_authority"]
        local_authority = candidate_value["candidate_verification"][
            "local_target_authority_result"
        ]["replay_authority"]
        with mock.patch.object(
            admission.focus_eligibility,
            "TRUST_ANCHORS_SHA256",
            fixture.trust_anchor_sha,
        ), mock.patch.object(
            admission.focus_eligibility.stage1_lean_authority,
            "build_project_lean_authority",
            return_value=(external_authority, Path("/toolchain"), None),
        ), mock.patch.object(
            admission.focus_eligibility.stage1_lean_authority,
            "build_repository_lean_authority",
            return_value=(local_authority, Path("/toolchain"), Path("/cache")),
        ), mock.patch.object(
            admission.focus_eligibility,
            "_replay_external_authority",
            return_value={
                **candidate_value["candidate_verification"][
                    "kernel_authority_result"
                ],
                "resolved_revision": candidate_value["candidate_verification"][
                    "resolved_revision"
                ],
                "archive_sha256": candidate_value["candidate_verification"][
                    "archive_sha256"
                ],
                "resolved_tree": candidate_value["candidate_verification"][
                    "resolved_tree"
                ],
                "kernel_stdout_sha256": candidate_value["candidate_verification"][
                    "kernel_stdout_sha256"
                ],
                "kernel_stderr_sha256": candidate_value["candidate_verification"][
                    "kernel_stderr_sha256"
                ],
            },
        ), self.assertRaisesRegex(
            admission.AdmissionError, "changed frozen blueprint checklist bytes"
        ):
            admission.publish_focus_admission(
                fixture.root,
                fixture.runtime,
                candidate,
                review,
                scheduler_signing_key_path=fixture.scheduler_key_path,
                regenerate=mutate_blueprint,
                validate_graph=lambda _root: None,
            )
        self.assertTrue(paused.is_file())
        self.assertFalse(
            (fixture.root / focus.receipt_relative_path(THEOREM)).exists()
        )
        self.assertEqual(fixture.graph.read_bytes(), graph_before)
        self.assertEqual(fixture.blueprint.read_bytes(), blueprint_before)
        self.assertFalse((fixture.runtime / "focus-admission-wal.json").exists())


if __name__ == "__main__":
    unittest.main()
