# Statement validation record

Item: `S56-M-0390-STATEMENT`  
Base revision: `8e045e956c76e5e69ad561a4730bbe667f470635`

## Frozen target

`Stage1.THM_M_0390.CatalanStatement` is the oriented natural-number equation from the intake:
for ordered binders `x, p, y, q`, all four values exceed one, and
`x ^ p + 1 = y ^ q`; the conclusion fixes the tuple to `(2, 3, 3, 2)`. There are no universes,
implicit parameters, or typeclass parameters. `Init` is the sole direct import and is sufficient
for the target, its exact-type fixture, transport, and mutation counterexamples.

The checked alternate `ConsecutivePowerStatement` classifies the consecutive values rather than
their representations. The canonical tuple theorem implies it. The converse is deliberately not
credited: knowing only `x ^ p = 8` and `y ^ q = 9` requires an additional uniqueness-of-power-
representation argument to recover the four parameters. Thus this phase does not overstate the
relationship as definitional equality or an `iff`.

## Mutation boundary

The Lean module prints nonidentical propositions for removal of the `1 < p` hypothesis, changing
the carrier to `Int`, moving exponent binders beneath the base hypotheses and making them
existential, and weakening `1 < p` to `0 < p`. Concrete kernel-checked counterexamples refute the
removed-hypothesis and boundary mutations at `8 ^ 1 + 1 = 3 ^ 2`. The domain and binder-scope
mutations are structurally distinct printed expressions and receive no transport or proof credit.

## Commands and results

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0390` | 0 | rank 4, planned, L0/rework-required, theorem incomplete |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0390/Statement.lean` | 0 | canonical target and four distinct mutations printed; no Lean diagnostics |
| `python3 -m json.tool Stage1_Instances/THM-M-0390/statement.json >/dev/null` | 0 | statement receipt is valid JSON |
| `sha256sum Stage1_Instances/THM-M-0390/Statement.lean Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | hashes match `statement.json` |
| `git diff --check -- Stage1_Instances/THM-M-0390 .stage1-worker-selftest.json` | 0 | no whitespace errors |

The existing `.lake` symlink points to the canonical checkout's already materialized pinned
artifacts. This worker neither changed nor fetched dependencies. This is narrow elaboration
evidence, not a cold or hermetic release replay. The root proposition has no proof body here;
machine status remains open and theorem completion remains false.
