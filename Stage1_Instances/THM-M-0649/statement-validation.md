# Statement validation record

Item: `S56-M-0649-STATEMENT`  
Base revision: `730e085f3ee8dfae10bd3b61f2dc8f90e7056880`

## Frozen target

`Stage1.THM_M_0649.ElementaryChainTarget` uses the faithful typed direct-limit encoding. The
stages may have different carrier types. A nonempty linear order indexes nonempty structures in
one language; elementary transition embeddings satisfy mathlib's `DirectedSystem` coherence law.
For every stage, the conclusion asks for an elementary embedding whose underlying embedding is
definitionally the canonical `Language.DirectLimit.of` map. This is the elementary-chain theorem,
not merely existence of some elementary map into the limit.

The two direct imports are `Mathlib.ModelTheory.DirectLimit` and
`Mathlib.ModelTheory.ElementaryMaps`. Neither imports the other in the direction needed here, so
both are minimal for the direct-limit construction and elementary-embedding target vocabulary.

## Commands and results

All commands ran in this worker clone. Lean commands ran from `Formalizations/Lean` against the
existing pinned `.lake` artifacts; no dependency update or fetch was run.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-0649/Statement.lean` | 0 | canonical target, exact expanded-target iff, and three structural mutations elaborated; explicit universe-bearing target printed |
| `lake env lean ../../Stage1_Instances/THM-M-0649/Statement.lean > /tmp/thm649.print 2>&1 && sha256sum /tmp/thm649.print ../../Stage1_Instances/THM-M-0649/Statement.lean` | 0 | printed expression `acb2ab...197`; source `b6f4d9...111` |
| `lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C .lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `sha256sum lean-toolchain lake-manifest.json` | 0 | `651c8a...1d2` and `321626...d81` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | standard and 1546-target projection valid |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ranks, all uniform L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0649` | 0 | rank 695, planned, theorem incomplete |

## Boundary policy

The target excludes an empty chain but includes singleton and greatest-element chains. It is not
restricted to countable or ordinal indices, finite languages, or a common ambient model. The
separate mutations record three rejected boundary changes: forgetting elementarity of transitions,
asserting only one selected stage, and assuming the conclusion. The common-ambient `iSup` encoding
remains open until a checked equivalence is constructed in later work.

This is statement-only evidence pending master acceptance. No proof, anchor-audit result, accepted
task state, audit completion, or theorem completion is claimed.
