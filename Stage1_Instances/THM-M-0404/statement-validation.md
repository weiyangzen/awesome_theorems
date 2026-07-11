# Statement validation record

Item: `S56-M-0404-STATEMENT`  
Base revision: `a2d0c4c35be39158b4dbf33e63a3b9c4b80daac5`

## Frozen target

`Stage1Instances.THM_M_0404.SkolemMahlerLechTarget` is the exact intake-selected claim over an
arbitrary characteristic-zero field, a `Nat`-indexed `LinearRecurrence` solution, and its zero
predicate. The conclusion uses finite lists of exceptions and one-sided natural arithmetic
progressions. Its sole direct import is `Mathlib.Algebra.LinearRecurrence`.

`PinnedCandidateSourceShape` directly expands the historical `S1_M_017.StatementShape`, and
`skolemMahlerLechTarget_iff_pinnedCandidateSourceShape` checks the expansion. This statement gate
does not credit the historical proof-like material or the eventual-periodic alternate: the latter
still requires a separately checked predicate-level bridge.

## Commands and results

All commands ran inside this worker clone. Lean commands ran from `Formalizations/Lean` with the
existing pinned toolchain and Lake environment.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-0404/Statement.lean` | 0 | exact target, expanded-source iff, four mutations, and empty/zero-step/universal boundary cases elaborated; explicit target expression printed |
| `python3 ../../Stage1_Instances/THM-M-0404/check_statement.py` | 0 | expression SHA-256 `7b53009924b8101ad44e30b1dfa4367a314fbd142d8834406c146e47201ea3fc`; all four mutations distinguished |
| `lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `sha256sum ../../Stage1_Instances/THM-M-0404/Statement.lean lean-toolchain lake-manifest.json` | 0 | hashes `a7dac1...f9d`, `651c8a...1d2`, and `321626...d81`, matching `statement.json` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0404` | 0 | rank 17, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |

## Mutation and boundary policy

The validator compares explicit elaborated expressions and rejects removal of `CharZero`,
specialization of the arbitrary field to `Rat`, relocation of the solution premise, and exclusion
of zero-step progressions. Kernel-checked examples exercise the empty zero set, the universal zero
set, and the zero-step singleton convention. Zero-order and identically-zero recurrences remain in
scope because the target adds no order or nondegeneracy premise.

This is statement-only evidence pending master acceptance. It does not prove Skolem-Mahler-Lech or
advance anchor-audit, obligation-tree, proof, validation, or release nodes.
