# LeanLevy vendored proof closure

This directory carries the minimal source closure needed by `Proof.lean` for
`S56-M-1023-PROOF`. It is proof-phase integration evidence, not a claim that
the later trust, hermetic-validation, independent-verification, or release gates
have passed.

## Origin and license

- Project: `slink/LeanLevy`
- Canonical remote: `https://github.com/slink/LeanLevy`
- Immutable revision: `93b635fba23398bfb1f0db8d220f88172f6900b6`
- Exact archive endpoint:
  `https://api.github.com/repos/slink/LeanLevy/tarball/93b635fba23398bfb1f0db8d220f88172f6900b6`
- Source archive SHA-256:
  `585b9255907bc5db4c44f010acf98f7a9d608eea1d845b93f6938ff2437e4621`
- Archive root: `slink-LeanLevy-93b635f`
- License: MIT, copied verbatim to `Vendor/LICENSE`; SHA-256
  `9ccb61ce372d47010507d876144053d40f49203851663956ae8c46e469dbfe79`
- Upstream environment: Lean `v4.29.0-rc3`, mathlib
  `8e096f85f9401f2c359b6708199c0402a980d921`
- Worker compatibility environment: Lean 4.29.0 and repository-pinned mathlib
  `8a178386ffc0f5fef0b77738bb5449d50efeea95`

The 20-module closure is listed file by file in `vendor-manifest.json`. Its
reconstructed upstream checksum-list SHA-256 is
`addd91a5dfdc2d6eef6b10bdd220914d4d49d266d2ff5e4f76fbe4ba0a1c6a92`,
and the concatenated reconstructed upstream sources have SHA-256
`74e551bd8ffae5aefe530b1fd15912940ecd6dfe74eb1ff23c011a5909e7aa9e`.
No upstream `.olean`, `.ilean`, Lake cache, or scratch module is vendored.

## Compatibility delta

Exactly two changes separate these sources from the immutable archive:

1. `Mathlib.Probability.Distributions.Poisson` became
   `Mathlib.Probability.Distributions.Poisson.Basic` after a mathlib module split.
2. The local heartbeat limit around
   `eq_of_rightCts_of_continuous_of_eqOn_ratNNReal` increased from `800000` to
   `4000000`. This changes an elaborator resource bound, not the declaration.

The normalized full-context combined diff has SHA-256
`ee3fcdea45ff454fe2aab4886881136af66070659c91a4b010a37964d95d3c84`.
`build_vendor_manifest.py` reconstructs every upstream source in memory by
reversing these two edits, checks it against 20 independently pinned upstream
SHA-256 values, and recomputes the normalized two-file patch digest before
regenerating the manifest. These pins were independently verified against the
exact archive endpoint above; validation never fetches the archive.

## Proof boundary

The terminal external declarations are:

- `ProbabilityTheory.existsUnique_levyKhintchineTriple`
- `ProbabilityTheory.isInfinitelyDivisible_iff_exists_levyKhintchineTriple`

They live under the terminal import
`LeanLevy.Levy.LevyKhintchineUniqueness`. `Proof.lean` is the repo-local exact
wrapper. It transports the upstream open truncation `|x| < 1` to the frozen
closed truncation `|x| <= 1` by integrating the boundary `{x | |x| = 1}` and
adjusting the drift. It also checks the convolution-power orientation,
uniqueness transport, and recovery of the probability condition at frequency
zero.

The frozen exact root is therefore a provisional `M0-P` candidate. The proof
body originated externally and is now pinned as target-local vendored source. Accepted state remains unchanged until
dependency-ordered master acceptance; source `H0`, readability `R0`, full
transitive trust/provenance review, cold hermetic replay, independent
verification, validation, release, `AUDIT-Z`, `THEOREM-Z`, and theorem
completion remain outside this proof-phase packet.
