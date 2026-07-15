#!/usr/bin/env python3
"""Generate or verify the offline THM-M-0353 vendored-source manifest."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
REPOSITORY = HERE.parents[1]
VENDOR = HERE / "Vendor"
MANIFEST_PATH = HERE / "vendor-manifest.json"
LEAN_ROOT = REPOSITORY / "Formalizations" / "Lean"

SOURCE_PATH = "GaussianField/HermiteFunctions.lean"
EXPECTED_SOURCE_SHA256 = (
    "e25548a1e042a61b340e24931dc05fd49bcaa6cf1daf68c335859df58d3b3d49"
)
EXPECTED_SOURCE_BLOB = "077d911f5e26a11199bc0756f50a803a58490807"
EXPECTED_LICENSE_SHA256 = (
    "2d3b806e6fd270f11819d0f797f721747adb0d497760e1b9053b6cd1fae4cf54"
)
EXPECTED_LICENSE_BLOB = "94f474d4d34ef439ac1bb0f1961d5cc9e9096c7e"
EXPECTED_TARGET_TOOLCHAIN_SHA256 = (
    "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2"
)
EXPECTED_TARGET_MANIFEST_SHA256 = (
    "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81"
)
EXPECTED_TARGET_MATHLIB = "8a178386ffc0f5fef0b77738bb5449d50efeea95"

DIRECT_IMPORTS = [
    "Mathlib.RingTheory.Polynomial.Hermite.Basic",
    "Mathlib.RingTheory.Polynomial.Hermite.Gaussian",
    "Mathlib.Analysis.SpecialFunctions.Gaussian.GaussianIntegral",
    "Mathlib.Analysis.Distribution.SchwartzSpace.Deriv",
    "Mathlib.Analysis.InnerProductSpace.Basic",
    "Mathlib.Analysis.PSeries",
    "Mathlib.Topology.Algebra.InfiniteSum.Order",
    "Mathlib.MeasureTheory.Function.L2Space",
    "Mathlib.Topology.Algebra.Polynomial",
    "Mathlib.Analysis.Calculus.LineDeriv.IntegrationByParts",
    "Mathlib.MeasureTheory.Measure.Haar.NormedSpace",
    "Mathlib.Analysis.Distribution.AEEqOfIntegralContDiff",
    "Mathlib.Analysis.Fourier.FourierTransform",
    "Mathlib.Analysis.Fourier.Inversion",
    "Mathlib.Analysis.Distribution.SchwartzSpace.Fourier",
]


def fail(message: str) -> None:
    raise SystemExit(f"FAIL THM-M-0353 vendor closure: {message}")


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git_blob_sha1(data: bytes) -> str:
    header = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()


def checked_file(path: Path, expected_sha256: str, expected_blob: str) -> bytes:
    if not path.is_file():
        fail(f"missing {path.relative_to(HERE)}")
    data = path.read_bytes()
    if sha256(data) != expected_sha256:
        fail(f"SHA-256 mismatch for {path.relative_to(HERE)}")
    if git_blob_sha1(data) != expected_blob:
        fail(f"Git blob mismatch for {path.relative_to(HERE)}")
    if not data.endswith(b"\n") or b"\r" in data or b"\x00" in data:
        fail(f"noncanonical source bytes in {path.relative_to(HERE)}")
    return data


def build_manifest() -> dict[str, object]:
    actual_files = {
        path.relative_to(VENDOR).as_posix()
        for path in VENDOR.rglob("*")
        if path.is_file()
    }
    expected_files = {SOURCE_PATH, "LICENSE"}
    if actual_files != expected_files:
        fail(f"unexpected vendored files: {sorted(actual_files ^ expected_files)}")

    source = checked_file(
        VENDOR / SOURCE_PATH, EXPECTED_SOURCE_SHA256, EXPECTED_SOURCE_BLOB
    )
    license_data = checked_file(
        VENDOR / "LICENSE", EXPECTED_LICENSE_SHA256, EXPECTED_LICENSE_BLOB
    )
    imports = [
        line.removeprefix("import ")
        for line in source.decode("utf-8").splitlines()
        if line.startswith("import ")
    ]
    if imports != DIRECT_IMPORTS:
        fail("the direct Mathlib import closure changed")
    upstream_manifest = (
        f"{sha256(source)}  SchwartzNuclear/HermiteFunctions.lean\n"
    ).encode("ascii")

    toolchain_path = LEAN_ROOT / "lean-toolchain"
    target_toolchain = toolchain_path.read_bytes()
    if sha256(target_toolchain) != EXPECTED_TARGET_TOOLCHAIN_SHA256:
        fail("target lean-toolchain hash changed")
    if target_toolchain.decode("ascii").strip() != "leanprover/lean4:v4.29.0":
        fail("target lean-toolchain value changed")

    lake_manifest_path = LEAN_ROOT / "lake-manifest.json"
    lake_manifest_bytes = lake_manifest_path.read_bytes()
    if sha256(lake_manifest_bytes) != EXPECTED_TARGET_MANIFEST_SHA256:
        fail("target lake-manifest.json hash changed")
    lake_manifest = json.loads(lake_manifest_bytes)
    mathlib_rows = [
        package
        for package in lake_manifest["packages"]
        if package.get("name") == "mathlib"
    ]
    if len(mathlib_rows) != 1:
        fail("target Lake manifest does not contain exactly one mathlib package")
    mathlib = mathlib_rows[0]
    if (
        mathlib.get("url") != "https://github.com/leanprover-community/mathlib4.git"
        or mathlib.get("rev") != EXPECTED_TARGET_MATHLIB
    ):
        fail("target mathlib pin changed")

    return {
        "schema_version": "stage1-vendored-source-closure/1.0",
        "item_id": "S56-M-0353-PROOF",
        "theorem_id": "THM-M-0353",
        "upstream": {
            "project": "mrdouglasny/gaussian-field",
            "canonical_remote": "https://github.com/mrdouglasny/gaussian-field.git",
            "revision": "d63a28568a75d99f6cb27af1f888a49a69855a66",
            "source_tree": "7b2c1a97a992cacee49dcbd347a9d78d59fdc383",
            "commit_date": "2026-06-06T17:35:17-07:00",
            "commit_subject": "feat: expose eigenbasis_completeness as public API",
            "source_archive_url": (
                "https://github.com/mrdouglasny/gaussian-field/archive/"
                "d63a28568a75d99f6cb27af1f888a49a69855a66.tar.gz"
            ),
            "source_archive_sha256": (
                "3d0504de255e7684f9f7badebff98dcb05619dfe180dbfa56d55c94bcdc4961c"
            ),
            "toolchain": {
                "value": "leanprover/lean4:v4.30.0",
                "path": "lean-toolchain",
                "git_blob_sha1": "af9e5d339aeb37e4e6ba2603fb873e637678e304",
                "sha256": (
                    "54727eec5cba149c18842e6deb5c41b369d66455c93ce135d7d5347c782b2325"
                ),
            },
            "lake_manifest": {
                "path": "lake-manifest.json",
                "git_blob_sha1": "5afd14eb253d63a28cb417c0656c66c5817d613a",
                "sha256": (
                    "a84ca65264f4421feed8111782520deca64d7a12081d90deab9c28c97ca1eeb7"
                ),
                "mathlib_revision": (
                    "c5ea00351c28e24afc9f0f84379aa41082b1188f"
                ),
            },
        },
        "target_environment": {
            "toolchain": "leanprover/lean4:v4.29.0",
            "lean_version": "4.29.0",
            "lean_commit": "98dc76e3c0a9b856c9b98726b713fb04fab16740",
            "toolchain_path": "Formalizations/Lean/lean-toolchain",
            "toolchain_sha256": EXPECTED_TARGET_TOOLCHAIN_SHA256,
            "lake_manifest_path": "Formalizations/Lean/lake-manifest.json",
            "lake_manifest_sha256": EXPECTED_TARGET_MANIFEST_SHA256,
            "mathlib_remote": (
                "https://github.com/leanprover-community/mathlib4.git"
            ),
            "mathlib_revision": EXPECTED_TARGET_MATHLIB,
            "mathlib_tree": "bdc39a3123201dae413a9d9be56ec242c19e5c2b",
        },
        "license": {
            "spdx": "Apache-2.0",
            "upstream_path": "LICENSE",
            "vendored_path": "Vendor/LICENSE",
            "git_blob_sha1": EXPECTED_LICENSE_BLOB,
            "sha256": EXPECTED_LICENSE_SHA256,
            "bytes": len(license_data),
            "lines": len(license_data.splitlines()),
            "verbatim": True,
        },
        "compatibility": {
            "source_transform_count": 0,
            "normalized_patch_sha256": hashlib.sha256(b"").hexdigest(),
            "semantic_scope": "none; source and license are byte-identical upstream copies",
            "path_relocation_only": True,
        },
        "build_order": ["Vendor.GaussianField.HermiteFunctions"],
        "files": [
            {
                "upstream_path": "SchwartzNuclear/HermiteFunctions.lean",
                "vendored_path": f"Vendor/{SOURCE_PATH}",
                "upstream_module": "SchwartzNuclear.HermiteFunctions",
                "vendored_module": "Vendor.GaussianField.HermiteFunctions",
                "git_blob_sha1": EXPECTED_SOURCE_BLOB,
                "upstream_sha256": EXPECTED_SOURCE_SHA256,
                "vendored_sha256": sha256(source),
                "bytes": len(source),
                "lines": len(source.splitlines()),
                "verbatim": True,
                "compatibility_operations": [],
            }
        ],
        "closure": {
            "module_count": 1,
            "source_bytes": len(source),
            "source_lines": len(source.splitlines()),
            "licensed_closure_bytes": len(source) + len(license_data),
            "licensed_closure_lines": (
                len(source.splitlines()) + len(license_data.splitlines())
            ),
            "source_manifest_sha256": (
                sha256(upstream_manifest)
            ),
            "vendored_concat_sha256": sha256(source + license_data),
            "direct_imports": imports,
            "external_dependencies": ["Mathlib"],
            "terminal_declarations": [
                "hermiteFunction_memLp",
                "hermiteFunction_orthonormal",
                "hermiteFunction_complete",
            ],
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="verify that vendor-manifest.json is already canonical; write nothing",
    )
    args = parser.parse_args()
    manifest = build_manifest()
    rendered = (
        json.dumps(manifest, indent=2, ensure_ascii=True) + "\n"
    ).encode("utf-8")

    if args.check:
        if not MANIFEST_PATH.is_file():
            fail("vendor-manifest.json is missing")
        if MANIFEST_PATH.read_bytes() != rendered:
            fail("vendor-manifest.json is stale or noncanonical")
        action = "verified"
    else:
        if not MANIFEST_PATH.is_file() or MANIFEST_PATH.read_bytes() != rendered:
            MANIFEST_PATH.write_bytes(rendered)
            action = "generated"
        else:
            action = "verified"

    print(
        f"PASS THM-M-0353 vendor closure: {action}; "
        f"1 verbatim module, {len((VENDOR / SOURCE_PATH).read_bytes())} source bytes"
    )


if __name__ == "__main__":
    main()
