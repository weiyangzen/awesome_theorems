# Statement validation record

Item: `S56-M-0772-STATEMENT`  
Base revision: `54912addae847c8bb166d0ef6a8ec7b0abb53004`

## Frozen target

`Stage1Instances.THM_M_0772.HausdorffMaximalPrinciple` is the exact intake-selected claim over an
arbitrary partially ordered type: an inclusion-maximal chain exists. Its only direct import is
`Mathlib.Order.Preorder.Chain`. The proof-bearing `Mathlib.Order.CompleteLattice.Chain` module is not
imported, so this check cannot accidentally claim closure from `maxChain_spec`.

The checked iff with `ExpandedHausdorffMaximalPrinciple` unfolds maximal-chain status into chainhood
and equality with every containing chain. Four explicit-expression mutations test the partial-order
hypothesis, carrier domain, binder scope, and empty-carrier boundary. Kernel-checked witnesses for
the empty and singleton carriers exercise the included degenerate cases without proving the general
target.

## Commands and results

All commands ran in this worker clone. Lean ran from `Formalizations/Lean` against the existing
pinned Lake artifacts; no update, build, clone, fetch, or other `.lake` mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-0772/Statement.lean` | 0 | canonical target, expanded-target iff, four mutations, and empty/singleton boundary proofs elaborated; explicit target expression printed |
| `python3 ../../Stage1_Instances/THM-M-0772/check_statement.py` | 0 | expression SHA-256 `f96455da0bdeabe833120768fad0327421d0f31f540e2ddf6d03725c54ef571a`; all four mutations distinguished |
| `lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0772` | 0 | rank 580, planned statement-first lane, legacy artifacts unaccepted, theorem incomplete |

This is statement-only evidence pending master acceptance. It neither audits nor invokes the
general proof candidate, and it does not advance anchor-audit, obligation-tree, proof, validation,
or release nodes.
