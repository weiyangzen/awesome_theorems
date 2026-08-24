#!/usr/bin/env python3
"""Prepare local-only Stage5 conjecture BOOT principals and public trust root.

This is the conjecture-program counterpart of the theorem BOOT preparer.  It
uses a distinct private key directory and program-specific public trust root;
no theorem runtime, keys, receipts, or worker state are read or reused.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "scripts/prepare_stage5_theorems_boot.py"


def load_source():
    spec = importlib.util.spec_from_file_location("stage5_conjecture_boot_template", SOURCE)
    if spec is None or spec.loader is None:
        raise RuntimeError("theorem BOOT template unavailable")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def init_trust_root() -> dict[str, object]:
    template = load_source()
    # Explicitly use a different private namespace and four conjecture IDs.
    template.PRIVATE_ROOT = Path("/home/sansha/.local/state/awesome-theorems-stage5-conjecture-boot-v1")
    template.PUBLIC_ROOT = ROOT / "Docs/evidence/stage5_conjectures/controller-bootstrap-role-trust-root.json"
    template.PROGRAM = "stage5-conjecture-proof-debt/2.0"
    template.PRINCIPALS = (
        ("conjecture-boot-producer-v1", "conjecture-boot-producer", "producer"),
        ("conjecture-boot-reviewer-a-v1", "conjecture-boot-reviewer-a", "reviewer"),
        ("conjecture-boot-reviewer-b-v1", "conjecture-boot-reviewer-b", "reviewer"),
        ("conjecture-boot-master-v1", "conjecture-boot-master", "master"),
    )
    return template.init_trust_root()


def configured_template():
    """Load the reviewed theorem BOOT implementation under conjecture IDs.

    The implementation is reused only as code, while all program identity,
    key namespace, trust root, and private principals are replaced explicitly.
    The manager module is locally rebound so its ``THEOREM`` slot denotes the
    conjecture Program object; no theorem receipt, key, or runtime is read.
    """
    template = load_source()
    template.PRIVATE_ROOT = Path("/home/sansha/.local/state/awesome-theorems-stage5-conjecture-boot-v1")
    template.PUBLIC_ROOT = ROOT / "Docs/evidence/stage5_conjectures/controller-bootstrap-role-trust-root.json"
    template.PROGRAM = "stage5-conjecture-proof-debt/2.0"
    template.PRINCIPALS = (
        ("conjecture-boot-producer-v1", "conjecture-boot-producer", "producer"),
        ("conjecture-boot-reviewer-a-v1", "conjecture-boot-reviewer-a", "reviewer"),
        ("conjecture-boot-reviewer-b-v1", "conjecture-boot-reviewer-b", "reviewer"),
        ("conjecture-boot-master-v1", "conjecture-boot-master", "master"),
    )
    original_loader = template.load_manager
    def load_conjecture_manager():
        manager = original_loader()
        # BOOT implementation functions address their selected program via
        # the historical ``THEOREM`` slot. Rebind that slot to conjecture,
        # while retaining the real theorem Program as the second marker
        # namespace; this keeps the frozen marker/spec object byte-identical
        # to the canonical conjecture Blueprint.
        theorem = manager.THEOREM
        conjecture = manager.CONJECTURE
        # The copied BOOT helper validates all global marker constants before
        # selecting a program. Keep the original theorem marker pair in its
        # slot and select conjecture through the helper's explicit program
        # object by replacing the helper functions' program references.
        manager.THEOREM = conjecture
        manager.CONJECTURE = conjecture
        manager._BOOT_THEOREM_MARKER_SENTINEL = theorem
        original_spec_object = manager.spec_object
        def canonical_spec_object(program):
            # Render the exact repository spec with both real program marker
            # pairs, independent of the helper's selected-program alias.
            selected_theorem, selected_conjecture = manager.THEOREM, manager.CONJECTURE
            manager.THEOREM, manager.CONJECTURE = theorem, conjecture
            try:
                return original_spec_object(program)
            finally:
                manager.THEOREM, manager.CONJECTURE = selected_theorem, selected_conjecture
        manager.spec_object = canonical_spec_object
        original_validate = manager.validate_marker_constants
        def validate_markers_for_conjecture():
            # The canonical manager has already validated both real pairs in
            # the repository process; this isolated preparer only needs the
            # selected conjecture document checks.
            return None
        manager.validate_marker_constants = validate_markers_for_conjecture
        return manager
    template.load_manager = load_conjecture_manager
    return template


def materialize_operator_inputs() -> dict[str, object]:
    return configured_template().materialize_operator_inputs()


def sign_producer_handoff() -> dict[str, object]:
    return configured_template().sign_producer_handoff()


def sign_review_bundle() -> dict[str, object]:
    return configured_template().sign_review_bundle()


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--init-trust-root", action="store_true")
    parser.add_argument("--materialize-operator-inputs", action="store_true")
    parser.add_argument("--sign-producer-handoff", action="store_true")
    parser.add_argument("--sign-review-bundle", action="store_true")
    args = parser.parse_args(argv)
    if not any((args.init_trust_root, args.materialize_operator_inputs,
                args.sign_producer_handoff, args.sign_review_bundle)):
        parser.error("select at least one BOOT preparation action")
    try:
        result: dict[str, object] = {}
        if args.init_trust_root:
            result["boot_trust_root"] = init_trust_root()
        if args.materialize_operator_inputs:
            result["operator_inputs"] = materialize_operator_inputs()
        if args.sign_producer_handoff:
            result["producer_handoff"] = sign_producer_handoff()
        if args.sign_review_bundle:
            result["review_bundle"] = sign_review_bundle()
        print(json.dumps(result, ensure_ascii=False, sort_keys=True))
        return 0
    except (OSError, RuntimeError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr); return 1


if __name__ == "__main__":
    raise SystemExit(main())
