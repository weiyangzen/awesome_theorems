# Vendored Kolmogorov-Chentsov proof closure

The `BrownianMotion` subtree is the exact 15-file transitive Lean source closure needed by
`ProbabilityTheory.exists_modification_holder`, copied from:

- project: `RemyDegenne/brownian-motion`
- remote: `https://github.com/RemyDegenne/brownian-motion`
- revision: `91885e6172648ea7f9c6a16b3a7069f92c88e023`
- source archive SHA-256: `74e42a88acbe271a34cba8668ea8bcba8afe38c0818c1de28e42bcd6d53cf20e`
- upstream closure manifest SHA-256: `baeba6af6f09aad37899666edf987cba2f75f0ad4dd1740314c2357293f1210c`
- adapted closure manifest SHA-256: `f43079ae9b6ae2745f57dc63cf07e9508a4532691a99b885bbaf26d33cc9b2aa`
- license: Apache License 2.0

The upstream proof bodies retain their copyright and license headers. Internal `BrownianMotion.*`
import paths in seven files are mechanically qualified with the repository-local vendor namespace;
those import-only adaptations and their standardized notices are the only source changes. Removing
the notices and namespace prefixes reconstructs every upstream file byte-for-byte. `check_proof.py`
verifies the reconstruction and the per-file hashes recorded in `PORT_PROVENANCE.md`.

The repository-local proof check elaborates every vendored file with pinned Lean 4.29.0 and mathlib
revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`; upstream used Lean 4.30.0-rc1 and mathlib revision
`f23306121184717ace04f3ac514be974e3224c8b`. No dependency update or `.lake` mutation is involved.
