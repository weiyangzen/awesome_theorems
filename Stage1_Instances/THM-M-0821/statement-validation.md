# THM-M-0821 statement validation

Item: `S56-M-0821-STATEMENT`

Base revision: `561d83df037004ceb2259292d7c63be930b40391` (tree
`6eb02475bf5a70139d60615c924b31c930efc2bb`). Validation date: 2026-07-13
(`Asia/Shanghai`).

## Selected target

The repository's complete target-bearing gloss is "maximum size of an antichain in a power set."
The canonical target therefore states a maximum, not merely an upper bound: for every finite type
`alpha`, an antichain of size `choose (card alpha) (card alpha / 2)` exists, and every antichain has
at most that size. The checked alternate selects the concrete lower middle layer as the witness.

This resolves the intake's three-way variant question without letting the convenient pinned theorem
choose the mathematics. `IsAntichain.sperner` supplies only the upper-bound component and is not
imported. Conversely, the 1928 paper's classification of all equality families is stronger than
the catalog's maximum-size gloss and is not silently added. The source scan, translation, proof
mapping, corrections or errata review, and independent `H0` acceptance remain open.

Families are `Finset (Finset alpha)`. The inclusion relation is non-strict subset, while
`IsAntichain` applies it only to distinct members. Natural division selects the lower middle rank.
No nonempty premise is added: the concrete witness is `{empty}` for both `Fin 0` and `Fin 1`, as
separately kernel-checked in the module.

## Lean boundary

The canonical declaration is `Stage1Instances.THM_M_0821.SpernerMaximumTarget`. The sole direct
import is `Mathlib.Data.Finset.Slice`. It provides the antichain definition, finite Boolean-lattice
layer, layer cardinality, and equal-cardinality antichain fact needed to check the statement and its
attaining witness. A target-only fixture elaborates with this import and fails when it is removed;
the full statement/transport module also elaborates. This proves necessity among the declared
imports, not global minimality across every possible lower-module factorization. The proof-bearing
LYM module is absent.

The module checks an iff with `MiddleLayerMaximumTarget`, four required mutation classes, and the
empty/singleton boundaries. The mutations remove the antichain premise, change subset carrier from
`Finset` to `Set`, move the universally bounded family under an existential, or exclude the empty
ground type. Fully explicit serialization distinguishes all four. These are statement-identity
tests; they do not assert logical inequivalence for every mutation.

The automation-provided canonical pinned `.lake` link was used read-only. No update, build, clone,
fetch, or dependency mutation was run. This dirty worker evidence is nonrelease evidence.

## Commands and results

Commands ran from the repository root unless another working directory is shown. Exact finalized
hashes and output summaries are recorded in `statement-receipt.json`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required`. |
| `python3 scripts/stage1_target.py show THM-M-0821` | 0 | Rank 1379, planned, legacy artifacts unaccepted, theorem incomplete. |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | Lean 4.29.0 commit `98dc76e3...`; Lake `5.0.0-src+98dc76e`. |
| pinned mathlib revision/tree/status checks | 0 | Revision `8a178386...`, tree `bdc39a31...`; package worktree clean. |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0821/Statement.lean` | 0 | Canonical and concrete-layer targets, checked iff, two boundaries, four expected exact-type rejections, axiom report and explicit expression elaborated; output SHA-256 `077e5b78...8ec`. |
| `cd Formalizations/Lean && python3 -B ../../Stage1_Instances/THM-M-0821/check_statement.py` | 0 | Expression SHA-256 `8f5d0542...d7c`; all mutations distinguished and the sole import deletion rejected. |
| finalized JSON, prohibited-construct, ownership, and whitespace checks | 0 | Structured artifacts agree; no prohibited construct or whitespace diagnostic was found. |

## Status boundary

This proposal freezes only the exact statement interface. The vector remains `[H1, M3, R4]`.
It supplies no proof of the universal upper bound, terminal-body audit, equality classification,
obligation registry, composition certificate, accepted source/readability review, hermetic replay,
independent verification, release decision, or master acceptance. Audit completion and theorem
completion remain false.
