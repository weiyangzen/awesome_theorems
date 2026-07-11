# Statement validation record

Item: `S56-M-0387-STATEMENT`  
Base revision: `8e045e956c76e5e69ad561a4730bbe667f470635`

## Frozen target

`Stage1Instances.THM_M_0387.FermatLastTheoremTarget` is the exact natural-number claim: for every
`n : Nat` with `3 <= n`, and every nonzero `a b c : Nat`, `a^n + b^n != c^n`. Its sole direct
import is `Init`. `PinnedMathlibSourceShape` copies the direct unfolding of the three definitions in
the pinned `Mathlib.NumberTheory.FLT.Basic` source, and
`fermatLastTheoremTarget_iff_pinnedMathlibSourceShape` checks that local identity definitionally.

The import is intentionally narrower than `Mathlib.NumberTheory.FLT.Basic`: the canonical target
uses only core natural-number operations. The pinned source revision was inspected, but this
worker's reused canonical `.lake` cache does not contain the corresponding mathlib FLT oleans.
Per worker policy, no dependency was fetched or built. Therefore the known integer, rational, and
primitive transports remain uncredited by this node rather than being reported as revalidated.

## Commands and results

All commands ran inside this worker clone. The Lean commands ran from `Formalizations/Lean` with
the existing pinned toolchain and Lake environment.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-0387/Statement.lean` | 0 | exact target, definitional source-shape iff, mutations, and two exponent-two counterexamples elaborated; explicit target expression printed |
| `python3 ../../Stage1_Instances/THM-M-0387/check_statement.py` | 0 | expression SHA-256 `8e0d406e9e5ba4504c1930352fde324a02df4a30cbfd75f796b9a3d2627113c`; all four mutations distinguished |
| `lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `sha256sum ../../Stage1_Instances/THM-M-0387/Statement.lean lean-toolchain lake-manifest.json` | 0 | hashes `5d7df0...05e5`, `651c8a...1d2`, and `321626...d81`, matching `statement.json` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0387` | 0 | rank 1, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-0387/statement.json >/dev/null` | 0 | structured statement artifact is valid JSON |
| scoped forbidden-term scan of `Statement.lean` and `check_statement.py` | 1 | no proof-gap declarations found; 1 is ripgrep's no-match exit |
| `git diff --check -- Stage1_Instances/THM-M-0387 .stage1-worker-selftest.json` | 0 | no whitespace errors |

## Mutation boundary

The validator compares explicit elaborated expressions and kills changes to the exponent
hypothesis, value domain, binder scope, and exponent-two boundary. The removed-bound and
exponent-two mutations are additionally refuted in the kernel by the concrete Pythagorean triple
`3^2 + 4^2 = 5^2`. A changed domain or binder order is a different proposition even where a later
checked theorem might transport it; neither is silently credited as the root.

This is statement-only evidence pending master acceptance. It does not prove FLT or advance any
proof, anchor-audit, obligation-tree, validation, or release node.
