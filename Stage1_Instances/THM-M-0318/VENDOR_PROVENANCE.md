# THM-M-0318 vendored Brouwer source closure

The three Lean modules under `Vendor/Gametheory` are the complete transitive
project-local source closure used for the finite-simplex Brouwer theorem. They
come from the MIT-licensed project `math-xmum/Brouwer` at immutable revision
`c02205edf347ad45f0d62db85497598ba2c4291e` (source tree
`5dda2d10fdd4a0db1aba85f1fa1a7acc509f80e4`). The archived revision has
SHA-256 `8591fadd6737d75b921eee27dc9d85d5d9f040a83ad7dcb2d81dc208754c04cd`.
Its original toolchain is Lean `v4.31.0` with mathlib revision
`fabf563a7c95a166b8d7b6efca11c8b4dc9d911f`.

`vendor-manifest.json` pins the upstream and vendored SHA-256 of every module,
the license hash, source archive identity, build order, and the exact reversible
compatibility operations. The port changes only API spellings required by the
repository's pinned Lean 4.29/mathlib environment:

1. Rename two `FunLike` fields from `coe_injective` to `coe_injective'`.
2. Remove the obsolete simp lemma name `Set.mem_sdiff` from six simp lists.
3. Remove one obsolete `SimpleGraph.symm` wrapper.

These are nine API compatibility edits. Separately, the port normalizes one
redundant final blank line in `ScarfPath.lean`.

No declaration type, theorem statement, proof premise, or mathematical proof
step is changed. `build_vendor_manifest.py` reverses every operation and checks
the reconstructed bytes against the independently pinned upstream hashes. The
license text is preserved verbatim in `Vendor/LICENSE`.

The vendored `Scarf.lean` includes the word `sorry` only inside nested block
comments containing abandoned drafts. The proof validator strips nested Lean
comments and strings before its prohibited-construct scan, compiles all three
modules from source with `--trust=0`, and applies `assert_no_sorry` to the
root-relevant declarations. No `.olean` is stored in the owned target path.
