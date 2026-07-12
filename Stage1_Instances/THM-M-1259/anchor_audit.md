# S56-M-1259-ANCHOR_AUDIT receipt

## Audit boundary

The audited root is `Stage1Instances.THM_M_1259.hormanderTarget` from `Statement.lean`, not an
elliptic special case, a generic Sobolev inequality, or a theorem that merely shares Hormander's
name. The search inspected repository-local Lean sources and every Lean source in the already
pinned dependency tree. It also ran bounded external discovery without fetching or mutating a
dependency.

## Pinned mathlib inventory

The Lake manifest pins mathlib4 at `8a178386ffc0f5fef0b77738bb5449d50efeea95` with Lean
`v4.29.0`. A case-insensitive source search for `h[oö]rmander`, `hormander`, `hypoellipt`,
`subellipt`, `sum.of.squares`, and `bracket.generat` found no terminal PDE theorem. The generic
algebraic uses of “sum of squares” are unrelated.

| Candidate | Checked role | Exact mismatch with the root |
|---|---|---|
| `VectorField.lieBracket` | Defines the bracket used by `GeneratedBracket` | No generated-family rank condition or regularity theorem |
| `ContDiff.lieBracket_vectorField` | Smoothness closure for brackets | Does not connect brackets to a differential operator or distributions |
| `Distribution` | Kernel-checked distribution object | No variable-coefficient sum-of-squares action or hypoellipticity result |
| `MeasureTheory.eLpNorm_le_eLpNorm_fderiv` | Gagliardo-Nirenberg-Sobolev estimate | First-order global inequality, not the localized fractional subelliptic estimate |

`AnchorAudit.lean` elaborates these exact declaration names against the pin. They are supporting
anchors only. None has the type of `hormanderTarget`, and composing them does not supply the missing
commutator estimate, subelliptic gain, regularity bootstrap, or hypoellipticity wrapper.

## Local and external candidates

At repository revision `4d48a3c5fbec6d005a64a99338e40c001656264c`, the only matching
Lean files are the frozen statement and legacy `S1_M_161.lean`. The legacy file explicitly records
a statement-shape boundary and proves only elementary Lie-closure wrappers; it neither imports nor
proves the frozen root, so it receives no terminal proof credit.

On 2026-07-12, GitHub repository searches for `Hormander language:Lean`, `hypoelliptic lean`,
`subelliptic lean`, `Hormander theorem prover`, `Hörmander Lean4`, and
`sum of squares hypoelliptic Lean` each returned `total_count: 0`. Thus there was no external Lean 4
candidate to pin or audit for theorem type, proof body, axioms, placeholders, toolchain, license, or
dependency feasibility. This is a bounded negative discovery result, not a claim that an
unindexed/private/future project cannot exist. Three grep.app searches returned HTTP 429 and are a
known discovery limitation, not silently counted as successful searches.

## Verdict

The node-specific anchor inventory is complete and self-tested. The terminal candidate is `null`.
Debt remains `[H2, M4, R3]`: source-page and errata work remains open, no exact kernel closure was
found, and no readable proof reconstruction exists. This audit supports later obligation planning
but makes no theorem-completion, proof, H0, or M0 claim. Exact commands and results are recorded in
`anchor_audit_validation.md`.

