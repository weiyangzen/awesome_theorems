# Birkhoff proof port provenance

`MaximalErgodic.lean` and `Birkhoff.lean` are a target-local compatibility port
of these files from the Apache-2.0 project
[`marcmorningstar/lean4-ergodic-theory`](https://github.com/marcmorningstar/lean4-ergodic-theory)
at immutable commit
`ed3fa6b8a30594eeb791160563942ba115581aa0`:

- `ErgodicTheory/Ergodic/MaximalErgodic.lean`
- `ErgodicTheory/Ergodic/Birkhoff.lean`

The immutable source archive has SHA-256
`3c0ef177500430ab55950061cfd73991347f5336b5b3d5032ffe46ac56009a52`.
The upstream source hashes are respectively
`6b9c40bd0e8d7238919283ad8666d0563d780a3b31eeb67d0ca66aae821817cc`
and
`bed8d81c6eb7f0ba74548255779dad7c3dc4e75ecf7ad935e1c68ef6fcb6ea6a`.
The upstream repository license file has SHA-256
`cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30`.
Both retained source headers identify Marcel Morgenstern as author and state
the Apache-2.0 license. The complete upstream `LICENSE` is included in this
directory; the upstream archive contains no `NOTICE` file.

The port changes exactly two integration surfaces:

1. In `MaximalErgodic.lean`, the upstream Lean 4.30/mathlib name
   `integrable_finsetSum` is changed to the pinned mathlib 4.29 name
   `integrable_finset_sum`.
2. In `Birkhoff.lean`, the upstream sibling import
   `ErgodicTheory.Ergodic.MaximalErgodic` is changed to target-local import
   `MaximalErgodic`.

No theorem statement or proof step is otherwise changed. The upstream files
target Lean 4.30.0-rc2 and mathlib revision
`34f7a6cd150fd7a166958d989d5abab56e9e3d15`; this port is checked with Lean
4.29.0 and repository mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. `check_proof.py` reconstructs
the upstream byte streams by removing the two modification notices and
reversing the two documented compatibility edits, then checks their recorded
SHA-256 hashes. It elaborates both ported bodies and the frozen package/root
adapters using the existing pinned toolchain.
