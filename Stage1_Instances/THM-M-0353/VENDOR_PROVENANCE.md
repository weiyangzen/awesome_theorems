# THM-M-0353 vendored proof-source provenance

This proof node vendors one complete Lean source file from
`mrdouglasny/gaussian-field`. It is the smallest upstream source closure needed by
`Proof.lean`: the file imports only Mathlib modules, so no other upstream project file is required.
Vendoring the source does not itself establish theorem completion or any later validation or release
gate.

## Immutable upstream

| Field | Pinned value |
|---|---|
| Repository | `https://github.com/mrdouglasny/gaussian-field.git` |
| Commit | `d63a28568a75d99f6cb27af1f888a49a69855a66` |
| Commit tree | `7b2c1a97a992cacee49dcbd347a9d78d59fdc383` |
| Commit date | `2026-06-06T17:35:17-07:00` |
| Commit subject | `feat: expose eigenbasis_completeness as public API` |
| Immutable archive | `https://github.com/mrdouglasny/gaussian-field/archive/d63a28568a75d99f6cb27af1f888a49a69855a66.tar.gz` |
| Archive SHA-256 | `3d0504de255e7684f9f7badebff98dcb05619dfe180dbfa56d55c94bcdc4961c` |
| Upstream toolchain | `leanprover/lean4:v4.30.0` |
| Upstream mathlib | `c5ea00351c28e24afc9f0f84379aa41082b1188f` |
| Upstream `lean-toolchain` SHA-256 | `54727eec5cba149c18842e6deb5c41b369d66455c93ce135d7d5347c782b2325` |
| Upstream `lake-manifest.json` SHA-256 | `a84ca65264f4421feed8111782520deca64d7a12081d90deab9c28c97ca1eeb7` |

The archive hash binds the acquisition snapshot. The archive is not retained in this target; the
offline checker instead verifies the content-addressed files extracted from that immutable snapshot.

## Vendored bytes

| Upstream path | Local path | Git blob | SHA-256 | Treatment |
|---|---|---|---|---|
| `SchwartzNuclear/HermiteFunctions.lean` | `Vendor/GaussianField/HermiteFunctions.lean` | `077d911f5e26a11199bc0756f50a803a58490807` | `e25548a1e042a61b340e24931dc05fd49bcaa6cf1daf68c335859df58d3b3d49` | byte-identical; path relocation only |
| `LICENSE` | `Vendor/LICENSE` | `94f474d4d34ef439ac1bb0f1961d5cc9e9096c7e` | `2d3b806e6fd270f11819d0f797f721747adb0d497760e1b9053b6cd1fae4cf54` | byte-identical Apache-2.0 license |

There is no compatibility patch: its normalized SHA-256 is the empty-stream digest
`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`. The local import name is
`Vendor.GaussianField.HermiteFunctions`; declaration names remain the upstream global names. The
proof adapter consumes `hermiteFunction_memLp`, `hermiteFunction_orthonormal`, and
`hermiteFunction_complete`.

The unchanged upstream header contains historical prose describing key properties as axioms. That
word is not a Lean declaration. Keeping it preserves byte identity; placeholder, declared-axiom,
kernel, and transitive-trust checks belong to the proof and validation receipts.

## Target environment

The compatibility replay uses `leanprover/lean4:v4.29.0` (Lean commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`) and mathlib commit
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The repository `lean-toolchain` and
`lake-manifest.json` SHA-256 values are respectively
`651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2` and
`321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

Run `python3 Stage1_Instances/THM-M-0353/build_vendor_manifest.py --check` from the repository root
for the network-free, write-free check. Without `--check`, the same program deterministically
regenerates `vendor-manifest.json`. It hashes the vendored source and license as both Git blobs and
SHA-256 objects, freezes the exact direct-import list, rejects extra vendor files, and verifies the
repository toolchain and Lake-manifest pins. It performs no network request and does not inspect or
modify `.lake`.
