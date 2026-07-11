# THM-M-0009 anchor audit

## Immutable inventory

The audit cutoff is 2026-07-12 (Asia/Shanghai). The frozen target is the conjunction of the
covariant and contravariant universally indexed Ext exactness branches in `Statement.lean`, with
expression SHA-256 `a5f8f018376a768901a6580f7a4fbfe593d73cfb89d71420b79f268b15d083be`.

The local Lake manifest pins mathlib4 commit
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. Its canonical remote is
`https://github.com/leanprover-community/mathlib4.git`; the audited source is
`Mathlib/Algebra/Homology/DerivedCategory/Ext/ExactSequences.lean`, SHA-256
`0aa08f6a0505e9ef22e03937f2d55e3f35287b4a731282cd7cd1d3e9c0fb7242`. The file entered mathlib at
commit `88c480406bd423b91b691ee43655057aa1f8db63` on 2025-12-28. The pinned license is Apache-2.0.

## Candidate classification

| Candidate | Exact scope | Terminal proof shape | Audit result |
|---|---|---|---|
| `CategoryTheory.Abelian.Ext.covariantSequence_exact` | first/covariant conjunct | combines four adjacent exactness components using `exact_of_δ₀` | exact branch match; adapter elaborates |
| `CategoryTheory.Abelian.Ext.contravariantSequence_exact` | second/contravariant conjunct | combines four adjacent exactness components using `exact_of_δ₀` | exact branch match; adapter elaborates |

`AnchorAudit.lean` fixes both candidates to fully quantified types identical to the respective
branches of the frozen target. Lean reports only `propext`, `Classical.choice`, and `Quot.sound` for
each adapter. A scoped source scan found no `sorry`, `admit`, `axiom`, `unsafe`, or `implemented_by`
token in the candidate source. This is discovery and direct exact-type evidence, not a substitute
for the downstream full transitive provenance and trust audit.

The two candidates jointly cover the exact frozen conjunction. Each branch is therefore an
`M0-W` candidate. The root remains conservatively `M1`: the proof phase has not yet introduced the
canonical conjunction theorem, and the later provenance/trust and release gates are open. No
theorem completion is claimed.

## External search ledger

Repo-local theorem/wrapper search found no earlier declaration closing the frozen target. Pinned
mathlib search used `covariantSequence`, `contravariantSequence`, long-exact/Ext aliases, and all
Lean source files. Three unauthenticated GitHub repository queries were run: `"long exact sequences
of Ext" Lean`, `"Ext" "long exact sequence" Lean4`, and `homological algebra Ext Lean4`. Each
returned HTTP 200 with zero repositories and the same response SHA-256
`08c082fdf7ca87ba911a2aabb0f0cf2d3e482a6feeaac9713e4578c20b2600b2`.

GitHub code search for `covariantSequence_exact language:Lean` returned HTTP 401 because code search
requires authentication; its response SHA-256 was
`b7dbd173f33b19650f61b1c528737e2037cf768d90076fdfce5d32541765e29e`. Thus no distinct external
Lean 4 candidate was identified, but exhaustive external discovery is not claimed. The access
limitation is explicit and does not reduce the already pinned mathlib match.

## Validation

Commands ran in this worker clone on 2026-07-12. No Lake update/build/fetch or dependency mutation
was performed.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-0009/AnchorAudit.lean` from `Formalizations/Lean` | 0 | both exact-type adapters elaborated; both axiom reports were `[propext, Classical.choice, Quot.sound]` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | immutable commit and tree matched the inventory |
| `sha256sum` on candidate source, mathlib license, toolchain, and Lake manifest | 0 | hashes recorded in structured audit |
| scoped `rg` candidate and forbidden-token searches | 0 / 1 | declarations located; forbidden-token scan had no matches (ripgrep exit 1) |
| the four GitHub API requests described above | 0 | repository searches succeeded; code-search access failure recorded |

Status boundary: this completes a self-tested anchor-audit artifact pending master acceptance. It
does not complete the obligation tree, proof, provenance closure, human-source audit, validation,
release, audit endpoint, or theorem endpoint.
