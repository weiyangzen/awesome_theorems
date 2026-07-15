# THM-M-1056 vendored Oseledets closure

`External/Oseledets/ErgodicTheory` is the complete 62-module project-local
source closure imported by `ErgodicTheory.TwoSided.SplittingAssembly`. The
sources come from the Apache-2.0 project
`marcmorningstar/lean4-ergodic-theory` at immutable revision
`ed3fa6b8a30594eeb791160563942ba115581aa0`. The immutable GitHub source
archive has SHA-256
`3c0ef177500430ab55950061cfd73991347f5336b5b3d5032ffe46ac56009a52`.
The upstream project used Lean `v4.30.0-rc2` and mathlib revision
`34f7a6cd150fd7a166958d989d5abab56e9e3d15`.

The closure was ported to this repository's pinned Lean `v4.29.0` and mathlib
revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`. The complete reversible port
is `External/Oseledets/lean429-port-complete.patch` (SHA-256
`7984d9e0199f8cbd1540d6fa8411bd931b79ea3431ae4acb0fbe534594d9c529`).
It changes 26 modules. The changes are API compatibility adjustments for the
older toolchain: renamed mathlib lemmas and fields, adjusted signatures and
proof syntax, and explicit proofs for facts no longer discharged by the same
automation. They do not weaken the headline theorem or add assumptions,
axioms, placeholders, unsafe code, or external oracles.

`vendor-manifest.json` pins every upstream and vendored module hash, byte
count, build position, prior trust-zero olean hash, the license, the source
archive, the environment, and all support files. `check_vendor.py` rejects
extra or missing files, duplicate order entries, hash or size drift,
prohibited Lean constructs after stripping nested comments and strings, and
an irreversible or incomplete patch. It reverses the port locally and checks
all 62 reconstructed sources against their upstream hashes. No network access
or upstream checkout is required.

The vendored tree deliberately contains source only. It contains no `.olean`,
log, cache, or dependency checkout. `source-olean-hashes.tsv` records prior
trust-zero validation outputs as provenance; it is not a substitute for the
fresh proof replay and no compiled artifact is credited from the repository.
The exact headline declaration is
`ErgodicTheory.oseledets_splitting`; its prior kernel dependency probe reported
exactly `propext`, `Classical.choice`, and `Quot.sound`.
