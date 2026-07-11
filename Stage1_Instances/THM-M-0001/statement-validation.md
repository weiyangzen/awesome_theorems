# Statement validation record

Item: `S56-M-0001-STATEMENT`  
Base revision: `3a52761477a87e9aaa92c1052ced6f49387cd607`

## Frozen target

`Stage1Instances.THM_M_0001.LongExactHomologySequenceTarget` states the exactness of all three
repeating positions of the homology sequence induced by a short exact short complex of homological
complexes in an arbitrary abelian category. Same-degree exactness is quantified over every degree;
the two positions involving the connecting map are quantified over every `c.Rel i j`. Thus the
target retains endpoints of arbitrary complex shapes and cannot collapse to one six-term window.

The sole direct import is `Mathlib.Algebra.Homology.HomologySequence`, the module defining the
connecting map and its composition identities. `GroupedLongExactHomologySequenceTarget` is a
logically regrouped form, and `longExactHomologySequenceTarget_iff_grouped` checks the transport in
the kernel. No proof of the canonical target is included or inspected by this phase.

## Commands and results

All commands ran inside this worker clone. Lean commands ran from `Formalizations/Lean` against the
existing pinned Lake environment; no dependency or `.lake` mutation command was run.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-0001/Statement.lean` | 0 | canonical target, grouped transport, and four structural mutations elaborated; explicit canonical expression printed |
| `python3 ../../Stage1_Instances/THM-M-0001/check_statement.py` | 0 | expression SHA-256 `6846afc515ceb8a7479a074f21295620ef4f191bd0804e377b56ae37567b7677`; all four mutations distinguished |
| `lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `sha256sum Stage1_Instances/THM-M-0001/Statement.lean Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | hashes `0b93dd...1d9a`, `651c8a...b1d2`, and `321626...2d81`, matching `statement.json` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0001` | 0 | rank 96, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-0001/{instance,statement}.json` | 0 | both structured artifacts are valid JSON |
| scoped forbidden-term scan of `Statement.lean` and `check_statement.py` | 1 | no proof-gap declarations found; 1 is ripgrep's no-match exit |
| `git diff --check -- Stage1_Instances/THM-M-0001 .stage1-worker-selftest.json` | 0 | no whitespace errors |

## Mutation boundary

The validator compares fully explicit elaborated expressions. It distinguishes removal of the
short-exact hypothesis, a changed category universe/domain together with loss of positions, moving
short-exactness into a `Nonempty` conclusion, and replacement of the universally indexed sequence
by one adjacent window. These mutations are statement-identity tests; this phase makes no claim
that every mutation is mathematically false.

This is statement-only evidence pending master acceptance. It does not establish an anchor audit,
proof closure, H0, M0, audit completion, independent validation, or theorem completion.
