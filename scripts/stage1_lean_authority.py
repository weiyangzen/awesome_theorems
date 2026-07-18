#!/usr/bin/env python3
"""Shared content identity for the pinned Stage1 Lean replay authority.

This module is deliberately dependency-light so focus admission and master
acceptance can use the same authority builder without importing each other.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path
import hashlib
import os
import sys
from typing import Any


def _load_acceptance_module() -> Any:
    path = Path(__file__).with_name("stage1_acceptance_evidence.py")
    spec = importlib.util.spec_from_file_location(
        "stage1_acceptance_evidence_for_lean_authority", path
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("Stage1 acceptance authority module is unavailable")
    module = importlib.util.module_from_spec(spec)
    previous = sys.modules.get(spec.name)
    sys.modules[spec.name] = module
    try:
        spec.loader.exec_module(module)
    except BaseException:
        if previous is None:
            sys.modules.pop(spec.name, None)
        else:
            sys.modules[spec.name] = previous
        raise
    return module


def build_repository_lean_authority(
    repo_root: Path,
    *,
    authority_revision: str,
) -> tuple[dict[str, Any], Path, Path]:
    """Return the exact toolchain/cache authority used by master acceptance."""

    acceptance = _load_acceptance_module()
    return acceptance.build_lean_authority(
        repo_root,
        lake_cache_root=repo_root / "Formalizations" / "Lean" / ".lake",
        authority_revision=authority_revision,
    )


def build_project_lean_authority(
    project_root: Path,
) -> tuple[dict[str, Any], Path, Path | None]:
    """Bind every replay-visible byte for one external Lean project.

    A project without a Lake manifest consumes no package cache and is bound to
    the full pinned toolchain closure.  A Lake project must carry a complete
    local `.lake` closure; focus replay never falls back to an ambient cache.
    """

    acceptance = _load_acceptance_module()
    toolchain_file = project_root / "lean-toolchain"
    toolchain_bytes = acceptance._read_absolute_regular(
        toolchain_file.absolute(), "external Lean toolchain pin"
    )
    try:
        toolchain = toolchain_bytes.decode("utf-8").strip()
    except UnicodeDecodeError as exc:
        raise RuntimeError("external Lean toolchain pin is not UTF-8") from exc
    match = acceptance.LEAN_TOOLCHAIN_RE.fullmatch(toolchain)
    if match is None or toolchain_bytes != (toolchain + "\n").encode("utf-8"):
        raise RuntimeError("external Lean toolchain pin is noncanonical")
    toolchain_root = Path.home() / ".elan" / "toolchains" / (
        "leanprover--lean4---v" + match.group("version")
    )
    toolchain_root = acceptance._require_absolute_directory(
        toolchain_root, "external pinned Lean toolchain"
    )
    acceptance._require_contained_symlinks(
        toolchain_root, "external pinned Lean toolchain"
    )
    toolchain_sha, toolchain_files, toolchain_bytes_count = (
        acceptance._hash_filesystem_closure(
            toolchain_root, "external pinned Lean toolchain"
        )
    )
    lean_bytes = acceptance._read_absolute_regular(
        toolchain_root / "bin" / "lean", "external pinned Lean executable"
    )
    lake_bytes = acceptance._read_absolute_regular(
        toolchain_root / "bin" / "lake", "external pinned Lake executable"
    )

    manifest = project_root / "lake-manifest.json"
    cache_root: Path | None = None
    dependency_bytes = toolchain_bytes
    packages_sha: str | None = None
    cache_sha: str | None = None
    cache_files = 0
    cache_bytes = 0
    if manifest.exists() or manifest.is_symlink():
        dependency_bytes = acceptance._read_absolute_regular(
            manifest.absolute(), "external Lean dependency manifest"
        )
        packages = acceptance._manifest_packages(dependency_bytes)
        cache_root = acceptance._require_absolute_directory(
            (project_root / ".lake").absolute(), "external Lean dependency cache"
        )
        entries = {entry.name: entry for entry in os.scandir(cache_root)}
        if set(entries) != {"build", "config", "packages"}:
            raise RuntimeError("external Lean dependency cache boundary is noncanonical")
        for name in sorted(entries):
            entry = entries[name]
            if entry.is_symlink() or not entry.is_dir(follow_symlinks=False):
                raise RuntimeError("external Lean dependency cache boundary is unsafe")
            acceptance._require_contained_symlinks(
                cache_root / name, f"external Lean dependency cache {name}"
            )
        packages_root = cache_root / "packages"
        package_entries = {entry.name: entry for entry in os.scandir(packages_root)}
        expected_names = {row["cache_name"] for row in packages}
        if set(package_entries) != expected_names:
            raise RuntimeError("external Lean package cache disagrees with its manifest")
        observations = []
        for ordinal, row in enumerate(packages):
            entry = package_entries[row["cache_name"]]
            if entry.is_symlink() or not entry.is_dir(follow_symlinks=False):
                raise RuntimeError("external Lean package cache boundary is unsafe")
            observations.append(
                {
                    "ordinal": ordinal,
                    **row,
                    **acceptance._git_package_observation(
                        packages_root / row["cache_name"], row["revision"]
                    ),
                }
            )
        packages_sha = acceptance.sha256_bytes(
            acceptance.canonical_json(observations)
        )
        cache_sha, cache_files, cache_bytes = acceptance._hash_filesystem_closure(
            cache_root, "external mounted Lean dependency cache"
        )

    authority = {
        "schema_version": "stage1-focus-lean-authority/1.0",
        "toolchain": toolchain,
        "toolchain_file_sha256": hashlib.sha256(toolchain_bytes).hexdigest(),
        "dependency_lock_sha256": hashlib.sha256(dependency_bytes).hexdigest(),
        "dependency_packages_sha256": packages_sha,
        "compiled_cache_sha256": cache_sha,
        "compiled_cache_file_count": cache_files,
        "compiled_cache_bytes": cache_bytes,
        "lean_binary_sha256": hashlib.sha256(lean_bytes).hexdigest(),
        "lake_binary_sha256": hashlib.sha256(lake_bytes).hexdigest(),
        "toolchain_closure_sha256": toolchain_sha,
        "toolchain_closure_file_count": toolchain_files,
        "toolchain_closure_bytes": toolchain_bytes_count,
        "network_policy": "denied",
        "repo_access": "read_only",
    }
    return authority, toolchain_root, cache_root
