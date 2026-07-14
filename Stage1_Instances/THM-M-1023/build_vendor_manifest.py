#!/usr/bin/env python3
"""Regenerate the content-addressed minimal LeanLevy source-closure manifest."""

from __future__ import annotations

import hashlib
import json
from difflib import unified_diff
from pathlib import Path


HERE = Path(__file__).resolve().parent
VENDOR = HERE / "Vendor"
FILES = [
    "LeanLevy/Fourier/Bochner.lean",
    "LeanLevy/Fourier/MeasureFourier.lean",
    "LeanLevy/Fourier/PositiveDefinite.lean",
    "LeanLevy/Levy/CharacteristicExponent.lean",
    "LeanLevy/Levy/CompensatedIntegral.lean",
    "LeanLevy/Levy/InfiniteDivisible.lean",
    "LeanLevy/Levy/LevyKhintchine.lean",
    "LeanLevy/Levy/LevyKhintchineProof.lean",
    "LeanLevy/Levy/LevyKhintchineUniqueness.lean",
    "LeanLevy/Levy/LevyMeasure.lean",
    "LeanLevy/Probability/Characteristic.lean",
    "LeanLevy/Probability/Poisson.lean",
    "LeanLevy/Probability/WeakConvergence.lean",
    "LeanLevy/Processes/Cadlag.lean",
    "LeanLevy/Processes/FiniteDimensional.lean",
    "LeanLevy/Processes/Kolmogorov.lean",
    "LeanLevy/Processes/LevyProcess.lean",
    "LeanLevy/Processes/PoissonProcess.lean",
    "LeanLevy/Processes/ProjectiveFamily.lean",
    "LeanLevy/Processes/StochasticProcess.lean",
]
EXPECTED_UPSTREAM_SHA256 = {
    "LeanLevy/Fourier/Bochner.lean":
        "23c1a756750b10c5ad1b9603ff3286ff09cd8b65884718720aabcf4e6399b961",
    "LeanLevy/Fourier/MeasureFourier.lean":
        "24e04a5526fb830bd28e892d5854e9a8507d7cbc1493abc6d9524452555176f1",
    "LeanLevy/Fourier/PositiveDefinite.lean":
        "266135603d57daad96eade5cba7c1cf6605c0f106b07b6394b8f9ab39e9e7759",
    "LeanLevy/Levy/CharacteristicExponent.lean":
        "0c4b2af6bff1ccb5903afd68e7b97f4b1040e36adb19b4fdd23410fbf8d7cdf5",
    "LeanLevy/Levy/CompensatedIntegral.lean":
        "c755578095fc96bb96fcdd3787bf88491bbcf0fca49ed9f75a42d5e5a10d2091",
    "LeanLevy/Levy/InfiniteDivisible.lean":
        "fb097e080935b4d03e39704e707e4c10abc0fddc38238c0ac875d04fe9ac1283",
    "LeanLevy/Levy/LevyKhintchine.lean":
        "f449dbed1d97021a9567e850a69a6eab983139aa2dc0748ab7eec82c7d38a378",
    "LeanLevy/Levy/LevyKhintchineProof.lean":
        "901f06dbc174eacad5ca3a2a5ddd58ab2d69a91138dccfdab5cd5e1f96e15789",
    "LeanLevy/Levy/LevyKhintchineUniqueness.lean":
        "9758db049ce7a4c6d2115b2d8ed077da79f0201716727382f6d148d0547e39b0",
    "LeanLevy/Levy/LevyMeasure.lean":
        "6b54946d41fcf803527fa6372af218beefa43c405ab048b2e3f2f02f1dc56afc",
    "LeanLevy/Probability/Characteristic.lean":
        "a4e21b37e312764c24a0c0af6283dd70ae6292e39146ae52d1d975e301993b1a",
    "LeanLevy/Probability/Poisson.lean":
        "d8de8e31c4774a45093a415978c0af145dfea937fa51123e01d8e7db89ac5028",
    "LeanLevy/Probability/WeakConvergence.lean":
        "7268f4bd53d37f40eeee3a896bff11d622067289c391cf59b4b940f2aad80f78",
    "LeanLevy/Processes/Cadlag.lean":
        "820d0e74d823076469f0b119c82ae93cda8d355ef856a0e4ea5fd2572e832f0c",
    "LeanLevy/Processes/FiniteDimensional.lean":
        "74ac65422fbce3aacbf4a860c41b8935f1dbfc6dec228f00fdac27da09e8150f",
    "LeanLevy/Processes/Kolmogorov.lean":
        "4a3f44540ec2048c74d74e427c89233358f012bd53b07e7196358a0c4b09bcb2",
    "LeanLevy/Processes/LevyProcess.lean":
        "fa99538f9865983909718d0d40d389f631de05d242ea27b88bf21d711bff65d0",
    "LeanLevy/Processes/PoissonProcess.lean":
        "198a9177921c40343909aaf78b70cd834b39f3af2e8a1eef13527d95de9ab261",
    "LeanLevy/Processes/ProjectiveFamily.lean":
        "c60d49699c6ae4a9ec2658b649c1a5a443c038d1f7a2615dc801d044173b631c",
    "LeanLevy/Processes/StochasticProcess.lean":
        "b731151c589c47d4e05cbfc128d93b9c22060d1848e3477d911c1800b306c4db",
}
EXPECTED_PATCH_SHA256 = (
    "ee3fcdea45ff454fe2aab4886881136af66070659c91a4b010a37964d95d3c84"
)
BUILD_ORDER = [
    "LeanLevy.Fourier.MeasureFourier",
    "LeanLevy.Probability.Characteristic",
    "LeanLevy.Fourier.PositiveDefinite",
    "LeanLevy.Probability.WeakConvergence",
    "LeanLevy.Fourier.Bochner",
    "LeanLevy.Processes.Cadlag",
    "LeanLevy.Processes.FiniteDimensional",
    "LeanLevy.Processes.ProjectiveFamily",
    "LeanLevy.Processes.Kolmogorov",
    "LeanLevy.Processes.StochasticProcess",
    "LeanLevy.Processes.LevyProcess",
    "LeanLevy.Probability.Poisson",
    "LeanLevy.Processes.PoissonProcess",
    "LeanLevy.Levy.InfiniteDivisible",
    "LeanLevy.Levy.LevyMeasure",
    "LeanLevy.Levy.CompensatedIntegral",
    "LeanLevy.Levy.LevyKhintchine",
    "LeanLevy.Levy.CharacteristicExponent",
    "LeanLevy.Levy.LevyKhintchineProof",
    "LeanLevy.Levy.LevyKhintchineUniqueness",
]
TRANSFORMS = {
    "LeanLevy/Probability/Poisson.lean": {
        "reason": "mathlib module split compatibility",
        "from": "import Mathlib.Probability.Distributions.Poisson",
        "to": "import Mathlib.Probability.Distributions.Poisson.Basic",
    },
    "LeanLevy/Levy/CharacteristicExponent.lean": {
        "reason": "resource-only elaboration compatibility; theorem term is unchanged",
        "from": "set_option maxHeartbeats 800000 in\n/-- If `f` is right-continuous",
        "to": "set_option maxHeartbeats 4000000 in\n/-- If `f` is right-continuous",
    },
}
PATCH_ORDER = [
    "LeanLevy/Probability/Poisson.lean",
    "LeanLevy/Levy/CharacteristicExponent.lean",
]


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


rows = []
upstream_concat = hashlib.sha256()
vendored_concat = hashlib.sha256()
upstream_lines: list[bytes] = []
line_count = 0
vendored_bytes = 0
assert set(FILES) == set(EXPECTED_UPSTREAM_SHA256)
assert list(TRANSFORMS) == PATCH_ORDER
assert {path.relative_to(VENDOR).as_posix() for path in VENDOR.rglob("*") if path.is_file()} == (
    set(FILES) | {"LICENSE"}
)
for name in FILES:
    path = VENDOR / name
    data = path.read_bytes()
    transform = TRANSFORMS.get(name)
    if transform:
        old = transform["from"].encode("utf-8")
        new = transform["to"].encode("utf-8")
        assert data.count(new) == 1, name
        upstream = data.replace(new, old)
    else:
        upstream = data
    assert digest(upstream) == EXPECTED_UPSTREAM_SHA256[name], name
    row = {
        "path": name,
        "upstream_sha256": digest(upstream),
        "vendored_sha256": digest(data),
        "upstream_bytes": len(upstream),
        "vendored_bytes": len(data),
        "compatibility_transform": transform,
    }
    rows.append(row)
    upstream_concat.update(upstream)
    vendored_concat.update(data)
    upstream_lines.append(f"{row['upstream_sha256']}  {name}\n".encode("utf-8"))
    line_count += len(data.splitlines())
    vendored_bytes += len(data)

# The compatibility diff has a fixed order independent of FILES' lexical order.
normalized_patch_parts = []
for name in PATCH_ORDER:
    data = (VENDOR / name).read_bytes()
    transform = TRANSFORMS[name]
    upstream = data.replace(
        transform["to"].encode("utf-8"), transform["from"].encode("utf-8")
    )
    normalized_patch_parts.extend(unified_diff(
        upstream.decode("utf-8").splitlines(keepends=True),
        data.decode("utf-8").splitlines(keepends=True),
        fromfile=f"a/{name}",
        tofile=f"b/{name}",
        n=3,
        lineterm="\n",
    ))
normalized_patch = "".join(normalized_patch_parts).encode("utf-8")
assert len(normalized_patch) == 1004
assert digest(normalized_patch) == EXPECTED_PATCH_SHA256

manifest = {
    "schema_version": "stage1-vendored-source-closure/1.0",
    "theorem_id": "THM-M-1023",
    "item_id": "S56-M-1023-PROOF",
    "upstream": {
        "project": "LeanLevy",
        "canonical_remote": "https://github.com/slink/LeanLevy",
        "source_archive_url": (
            "https://api.github.com/repos/slink/LeanLevy/tarball/"
            "93b635fba23398bfb1f0db8d220f88172f6900b6"
        ),
        "revision": "93b635fba23398bfb1f0db8d220f88172f6900b6",
        "source_archive_sha256": "585b9255907bc5db4c44f010acf98f7a9d608eea1d845b93f6938ff2437e4621",
        "source_archive_root": "slink-LeanLevy-93b635f",
        "upstream_toolchain": "leanprover/lean4:v4.29.0-rc3",
        "upstream_mathlib_revision": "8e096f85f9401f2c359b6708199c0402a980d921",
    },
    "compatibility": {
        "target_toolchain": "Lean 4.29.0 (98dc76e3c0a9b856c9b98726b713fb04fab16740)",
        "target_mathlib_revision": "8a178386ffc0f5fef0b77738bb5449d50efeea95",
        "normalized_patch_sha256": EXPECTED_PATCH_SHA256,
        "semantic_scope": "one renamed mathlib import and one heartbeat-budget increase",
    },
    "license": {
        "spdx": "MIT",
        "path": "Vendor/LICENSE",
        "sha256": digest((VENDOR / "LICENSE").read_bytes()),
    },
    "closure": {
        "module_count": len(rows),
        "vendored_bytes": vendored_bytes,
        "line_count": line_count,
        "upstream_manifest_sha256": digest(b"".join(upstream_lines)),
        "upstream_concat_sha256": upstream_concat.hexdigest(),
        "vendored_concat_sha256": vendored_concat.hexdigest(),
        "root_module": "LeanLevy.Levy.LevyKhintchineUniqueness",
        "excluded_nondependencies": [
            "LeanLevy.Processes.CompoundPoisson",
            "LeanLevy.Processes.CompoundPoissonLaw",
            "LeanLevy.Processes.PiecewisePath",
            "LeanLevy.Representation.BochnerGaussian",
        ],
    },
    "terminal_declarations": [
        "ProbabilityTheory.existsUnique_levyKhintchineTriple",
        "ProbabilityTheory.isInfinitelyDivisible_iff_exists_levyKhintchineTriple",
    ],
    "build_order": BUILD_ORDER,
    "files": rows,
}
(HERE / "vendor-manifest.json").write_text(
    json.dumps(manifest, indent=2, ensure_ascii=True) + "\n", encoding="utf-8"
)
