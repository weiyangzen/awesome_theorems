# THM-M-0391 rev-5.6 statement

This directory is the `planned` intake dossier for Mihailescu's theorem, formerly Catalan's
conjecture. The exact root is the positive natural-number statement frozen in `instance.json`:
the sole solution of `x^a = y^b + 1` with both bases and exponents greater than one is
`3^2 = 2^3 + 1`.

`Statement.lean` elaborates that exact proposition using only `Init` under the repository-pinned
Lean 4.29.0 toolchain. A checked iff relates its curried hypotheses to the legacy conjunction
encoding. Two executable counterexamples reject weakening either exponent bound to positivity.
The legacy file itself receives no inherited proof credit.

## Statement verdict

Manifest membership, repository structural gates, and the narrow Lean elaboration pass. Lifecycle
remains `planned`, the provisional debt vector remains `[H1, M4, R4]`, and `theorem_complete` is
false. This node freezes and tests the proposition only; it does not prove it. H1 records that the
exact primary-source theorem/page/errata crosswalk still needs independent source audit, while M4
records that no terminal Lean proof is credited.

See `scope-map.md`, `source-statement-crosswalk.md`, and `validation.md` for the boundaries and
self-test evidence.

## Anchor-audit verdict

`anchor-audit.md` records the immutable mathlib, flt-regular, and external Lean 4 candidate
inventory. The pinned mathlib tree has no terminal Mihailescu declaration; its similarly named
`Polynomial.flt_catalan` has a different polynomial theorem type. Formal Conjectures has a close
statement at commit `7871d8fc7a8164a1ac16c3765b40c25ce015b681`, but its proof is `sorry`.
Consequently there is no terminal body to integrate, and the root remains open at `[H1, M4, R4]`.

## Obligation-tree verdict

`obligation-registry.json` freezes a 15-obligation denominator with no
exclusions, while `typed-graphs.json` keeps proof, refinement, provenance,
evidence, trust, documentation, and workflow edges distinct. The readable
architecture and substantive leaf ledgers are in `obligation-tree.md`.

This is an open proof plan, not machine closure. Only the previously checked
statement transport has a local proof body. The difficult square/odd-prime and
odd-prime/odd-prime classification packages are explicitly marked for further
expansion, so the root remains `[H1, M4, R4]`, `audit_complete=false`, and
`theorem_complete=false`.
