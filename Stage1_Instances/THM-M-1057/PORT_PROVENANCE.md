# Kingman Port Provenance

The Lean sources in this directory vendor the Kingman proof stack from:

- Repository: <https://github.com/marcmorningstar/lean4-ergodic-theory>
- Revision: `ed3fa6b8a30594eeb791160563942ba115581aa0`
- License: Apache License 2.0, reproduced verbatim in `LICENSE`
- Target toolchain: `leanprover/lean4:v4.29.0`

No theorem statement or proof argument was weakened. The edits are module-path and pinned-API
compatibility changes only. Each source carries a short port notice adjacent to its copyright
header. The table gives the SHA-256 digest of the immutable upstream file and of the vendored
port, making reconstruction and review fail-closed.

| Vendored file | Upstream path | Upstream SHA-256 | Vendored SHA-256 |
| --- | --- | --- | --- |
| `MaximalErgodic.lean` | `ErgodicTheory/Ergodic/MaximalErgodic.lean` | `6b9c40bd0e8d7238919283ad8666d0563d780a3b31eeb67d0ca66aae821817cc` | `1e6ecd26fe2f3587f292e82e41b3bc7e61f5110cf4be6e3a5e4bc53a8a45c6d5` |
| `Birkhoff.lean` | `ErgodicTheory/Ergodic/Birkhoff.lean` | `bed8d81c6eb7f0ba74548255779dad7c3dc4e75ecf7ad935e1c68ef6fcb6ea6a` | `0bb4ef8cc491100c54c8966ba31c44ac86661117b1e1eac8498564bc5384f789` |
| `KingmanFekete.lean` | `ErgodicTheory/Ergodic/Kingman/Fekete.lean` | `7e29b3f2e0dbf26e13d6c1aef53563052e85656e0e868dd50d846d62a474fcff` | `4112aaeb5043c7bc5e659c62ef8f58b5f563ebfe94fae9eb3ad0c9bcbcf3749a` |
| `KingmanDerriennic.lean` | `ErgodicTheory/Ergodic/Kingman/Derriennic.lean` | `f3ca0c3903b1a07ea5533bc962233a834ddf3a3708118dd177b92e636f9a2a62` | `1bd9754dcc2f957084804a9b7136e0a378bd9abc7e857a77b86857298934340a` |
| `KingmanCompanion.lean` | `ErgodicTheory/Ergodic/Kingman/Companion.lean` | `50f3716e5f059afb50086489349726ecb8f1b2f626a5fc2f605e49e4fd54d33e` | `231b552e488d9b693edfaf1b461e612901698e205227db2fc579a4d4d54f9f2a` |
| `KingmanBlockSqueeze.lean` | `ErgodicTheory/Ergodic/Kingman/BlockSqueeze.lean` | `88854f77420ae853bf615b80e600c50b9048f2dccb17dfae4edbf5451c661c71` | `3e26d917b00133917ea10788c8e54542cff61c8d03c7afd6c8138f60720ba567` |
| `KingmanCore.lean` | `ErgodicTheory/Ergodic/Kingman/Core.lean` | `d0335f2c93d23a70700deebd1b568aed91ef7f61ada70cc9ffcf4a4d60e2dbfa` | `fb2fad9b2c30386476fa67b9db71eda07880823d902f183f9eab2a915a5a4d82` |
| `KingmanMeans.lean` | `ErgodicTheory/TwoSided/KingmanMeans.lean` | `80400f3fdb9847121a6f6c5b1a068979a0e223004409a34b4f1a96536f80a053` | `96fc4065af56f39ca17602238a31d6de108d0d0bf3db6fd490c1a5a2b8e6cc52` |
| `LICENSE` | `LICENSE` | `cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30` | `cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30` |

## Exact Compatibility Edits

All eight Lean files receive only the documented port notice in addition to the edits below.

- Target-local sibling imports replace upstream qualified imports:
  `ErgodicTheory.Ergodic.MaximalErgodic` becomes `MaximalErgodic`;
  `ErgodicTheory.Ergodic.Birkhoff` becomes `Birkhoff`;
  the Kingman imports become `KingmanFekete`, `KingmanDerriennic`,
  `KingmanCompanion`, `KingmanBlockSqueeze`, and `KingmanCore` respectively.
  `KingmanMeans.lean` imports `KingmanCore` and `Birkhoff`.
- Pinned mathlib uses snake-case names. Every `integral_finsetSum` occurrence becomes
  `integral_finset_sum`, and every `integrable_finsetSum` occurrence becomes
  `integrable_finset_sum`. This affects `MaximalErgodic.lean`, `KingmanFekete.lean`,
  `KingmanDerriennic.lean`, `KingmanCompanion.lean`, and `KingmanMeans.lean`.
- Pinned Lean 4.29 lacks the convenience methods `Tendsto.limsup_comp_le_limsup` and
  `Tendsto.liminf_le_liminf_comp` used upstream. `KingmanBlockSqueeze.lean` defines private,
  source-local equivalents from `Filter.limsup_comp`, `Filter.limsup_le_limsup_of_le`, and
  order duality, then replaces the four upstream method calls with those private lemmas.

The Apache 2.0 text is unchanged: its upstream and vendored digests are identical.
