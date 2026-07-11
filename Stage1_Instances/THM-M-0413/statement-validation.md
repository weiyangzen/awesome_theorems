# Statement validation record

Base revision: `d7fe9d2340a2db439f33d8bff8518970d6e514f4`.

All commands ran in `Formalizations/Lean`, using its pinned toolchain and the canonical read-only
`.lake` artifacts. No dependency update, fetch, clone, or build was run.

| Command | Exit | Exact result summary |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-0413/Statement.lean` | 0 | Printed `Statement.{u} : Prop`, the checked integral-closure iff, and the normalized declaration; no diagnostics |
| `lake env lean ../../Stage1_Instances/THM-M-0413/mutations/RemovedNumberField.lean` | 1 | `failed to synthesize ... IsDedekindDomain (RingOfIntegers K)` |
| `lake env lean ../../Stage1_Instances/THM-M-0413/mutations/ChangedDomain.lean` | 1 | `failed to synthesize ... Field K` at the changed target |
| `lake env lean ../../Stage1_Instances/THM-M-0413/mutations/ChangedBinderScope.lean` | 1 | `failed to synthesize ... Field K` where `[NumberField K]` is bound too early |
| `lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C .lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95` |

The expression digest is SHA-256 over the UTF-8 canonical serialization recorded in
`statement.json`, with no trailing newline. The environment digest is SHA-256 over newline-ended
`key:value` records for toolchain, mathlib revision, sole import, options, and the two lock-file
digests, in that recorded order. The one declared import is the defining mathlib module itself;
its public imports are dependency closure, not additional imports of this statement module.

The positive boundary probe for `K = Rat` is part of `Statement.lean` and therefore passed in the
same kernel run. The three negative fixtures are deliberately noncompiling and are accepted only
when each exits nonzero for its documented reason.
