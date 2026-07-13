# Statement validation record

Item: `S56-M-0061-STATEMENT`
Base revision: `ebd5f75831296a8a35e7b33013b964f2baf31bb9`; base tree:
`d1e4bc83c803eefcd9898aac57352265a29f0658`.

## Frozen target

`Stage1Instances.THM_M_0061.LagrangeDivisibilityTarget` freezes the repository claim exactly: for
every `G : Type u` with `[Group G] [Finite G]` and every `H : Subgroup G`, `Nat.card H` divides
`Nat.card G`. The explicit finiteness premise remains part of the target even though the later
mathlib proof candidate has a stronger arbitrary-group domain.

The sole direct import is `Mathlib.Algebra.Group.Subgroup.Finite`. It supplies statement vocabulary,
finite-subgroup cardinality interfaces, and the bottom/top boundary notation. Deleting it fails
elaboration. The proof-bearing `Mathlib.GroupTheory.Coset.Card` module is deliberately absent from
the statement closure.

`lagrangeDivisibilityTarget_iff_fintypeCardTarget` checks the `Finite`/`Nat.card` to
`Fintype`/`Fintype.card` transport. The additive analogue and the stronger arbitrary-group target
remain uncredited rather than silently substituted.

## Commands and results

All Lean commands ran from `Formalizations/Lean` with the existing pinned Lake environment. The
automation-provided `.lake` link and canonical dependencies were used read-only. No `lake update`,
`lake build`, clone, fetch, or dependency mutation ran.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0061` | 0 | rank 1093; planned; no accepted legacy artifact; theorem incomplete |
| `lake env lean ../../Stage1_Instances/THM-M-0061/Statement.lean` | 0 | exact target, checked `Iff` transport, four expected mutation type rejections, three boundary implications, axiom reports, and explicit expression elaborated |
| `python3 ../../Stage1_Instances/THM-M-0061/check_statement.py` | 0 | expression SHA-256 `adff72e...6836`; source `386d2d...dc7d`; output `cb4d37...2f59`; sole import deletion, four mutation fingerprints, transport, boundaries, authority item, metadata, packet, and pins agree |
| `lake env lean --version` and `lake --version` | 0 | Lean 4.29.0 at `98dc76e...1740`; Lake 5.0.0-src+98dc76e |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | pinned mathlib `8a178386...a95`; tree `bdc39a...b2b` |
| `python3 -m json.tool` on the finalized owned JSON and worker packet | 0 | every structured artifact is valid JSON |
| scoped prohibited-declaration scan over owned Lean files | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration found |
| `git diff --check -- Stage1_Instances/THM-M-0061 .stage1-worker-selftest.json` plus per-new-file checks | 0 | no whitespace diagnostics |

## Mutation and boundary record

The mutation suite removes the finite premise, changes multiplicative groups and subgroups to
additive ones, replaces the arbitrary subgroup binder by existence of one subgroup, and excludes
groups of cardinality one. Lean rejects term-level substitution in the direction that could
mis-credit each mutation as the canonical target, and the validator independently serializes five
distinct explicit expressions.

The boundary implications specialize the canonical binders to every subgroup of an ambient group
of order one, the bottom subgroup, and the top subgroup. They check inclusion of those binders and
cases; they do not inhabit or prove `LagrangeDivisibilityTarget`.

## Status boundary

This is provisional worker statement evidence pending master acceptance. Primary-source mapping,
anchor and terminal-body audit, obligation registry, proof, composition, readable reconstruction,
hermetic replay, independent validation, release, audit completion, and theorem completion remain
open. The prior intake receipt is historical provisional evidence and is not cited as the current
statement validator.
