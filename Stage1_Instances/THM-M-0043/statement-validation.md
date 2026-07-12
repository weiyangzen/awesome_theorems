# Statement validation record

Item: `S56-M-0043-STATEMENT`
Base revision: `4ecdda4863162748b3ee70bc4ec842789418145d` (tree
`aace54662cd5e9ca38472011f41afdbffdedfa04`)

## Frozen target

`Stage1Instances.THM_M_0043.SpectralTheoremTarget` is the normal-to-diagonal direction of the
finite-dimensional complex spectral theorem. It quantifies over every nonempty finite index type,
matching Axler's standing nonzero-space convention, and every square complex matrix `A`. Its only mathematical antecedent is
`IsStarNormal A`. The conclusion supplies a unitary matrix `U`, diagonal entries `d`, and the exact
equation `A = U * Matrix.diagonal d * star U`.

The source selection is Axler, *Linear Algebra Done Right*, fourth edition, Section 7B, Theorem
7.31(a) to (b), pages 246-247. This supports the exact conventional statement at `H1`; it does not
establish the catalog's Hilbert/1906 attribution or an independently accepted H0 source packet.

## Commands and results

All commands ran in this worker clone on 2026-07-13 (Asia/Shanghai). Lean commands ran from
`Formalizations/Lean` with the existing pinned `.lake` artifacts used read-only.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0043` | 0 | rank 1083; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `lake env lean ../../Stage1_Instances/THM-M-0043/Statement.lean` | 0 | exact target, both statement transports, and all four type-rejection mutations elaborated; fully explicit target printed |
| `python3 -B ../../Stage1_Instances/THM-M-0043/check_statement.py` | 0 | target expression SHA-256 `a46ee239...557a`; four mutation expressions distinct; deleting either direct import fails |
| `python3 -B Stage1_Instances/THM-M-0043/check_intake.py` | 1 | known phase-evolution failure: the intake-only checker expects the earlier authoritative intake item state `[ ]`, base revision, null target, and nine-file inventory; statement work does not rewrite historical intake evidence to manufacture agreement |
| `lake env lean --version` | 0 | Lean 4.29.0 at commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `lake --version` | 0 | Lake `5.0.0-src+98dc76e` |
| pinned mathlib revision/tree/status inspection | 0 | revision `8a178386...95`, tree `bdc39a31...2c`, package worktree clean |
| source, toolchain, manifest, import-source, statement, and output SHA-256 checks | 0 | values agree with `statement.json` and `statement-receipt.json` |
| prohibited Lean construct scan over the owned path | 1 | expected no-match result; no `sorry`, `admit`, `sorryAx`, `axiom`, bodyless/opaque, or `unsafe` declaration |
| JSON parse and `check_statement.py` structured-artifact checks | 0 | statement manifest, receipt, instance reconciliation, hashes, imports, mutations, and status boundary agree |
| scoped `git diff --check` and untracked-file whitespace checks | 0 | no whitespace diagnostics |

No `lake update`, `lake build`, dependency clone/fetch, or other `.lake` mutation was run.

## Mutation and import policy

The removed-normality mutation makes the assertion unconditional. The domain mutation quantifies
over an arbitrary commutative star ring instead of the source's complex field. The binder-scope
mutation demands one `U,d` pair work for every normal matrix at a dimension. The boundary mutation
removes `[Nonempty n]`, adding the zero-dimensional case excluded by Axler's standing convention.
Lean rejects every mutation as a term of the root, and the validator independently compares their
fully explicit expressions.

The two direct imports are minimal for this spelling: deleting `Mathlib.Data.Complex.Basic` removes
the complex scalar surface, while deleting `Mathlib.LinearAlgebra.UnitaryGroup` removes the unitary
matrix and required matrix algebra surface. The broader `Mathlib.Analysis.Matrix.Spectrum` module is
not imported, and the strict Hermitian theorem is not invoked.

## Status boundary

This is statement-only self-test evidence pending master acceptance. It freezes no proof body or
obligation tree and does not prove spectral diagonalization. Source H0, anchor audit, proof,
composition, trust closure, readable reconstruction, hermetic replay, independent verification,
audit completion, theorem completion, and master acceptance remain open.
