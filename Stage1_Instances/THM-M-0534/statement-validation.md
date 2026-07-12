# Statement validation record

Item: `S56-M-0534-STATEMENT`  
Base revision: `b86b7c60888b8506233bd2a07adc4f7c277ad675`

## Frozen target

The literal inventory claim, "A short exact sequence induces a long exact sequence in homology,"
selects the general theorem about homological complexes. The pair and triple formulations require
additional singular-chain constructions and are applications rather than exact readings of this
sentence. The abstract-homology-theory formulation would assume exactness rather than derive it.

`Stage1Instances.THM_M_0534.LongExactHomologySequenceTarget` states exactness at all three repeating
positions. Same-degree exactness is quantified over every degree; both connecting-map positions are
quantified over every `c.Rel i j`. This retains arbitrary complex shapes and endpoints and does not
collapse the continuing sequence to a single finite window. The grouped alternate encoding has a
kernel-checked `iff` transport.

The sole direct import is `Mathlib.Algebra.Homology.HomologySequence`. No target proof is supplied or
inspected in this phase.

## Commands and results

Commands ran in this worker clone. Lean ran from `Formalizations/Lean` against the existing pinned
Lake environment. No update, build, clone, fetch, or other dependency mutation was run.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-0534/Statement.lean` | 0 | canonical target, grouped transport, four mutations, and the explicit canonical expression elaborated |
| `python3 ../../Stage1_Instances/THM-M-0534/check_statement.py` | 0 | expression SHA-256 `6846afc...b7677`; all four structural mutations distinguished |
| `lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `lake --version` | 0 | Lake `5.0.0-src+98dc76e` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `sha256sum Stage1_Instances/THM-M-0534/Statement.lean Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | `a54782...ea8e3`, `651c8a...b1d2`, and `321626...2d81` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |

One version check was initially invoked from the repository root, where no default Elan toolchain
is configured, and exited 1 without changing anything. Repeating it from the pinned Lean project
gave the successful results above.

## Status boundary

Mutation comparisons distinguish changes of hypothesis, domain/universe, binder scope, and boundary
extent by their fully explicit elaborated expressions. They test statement identity, not the truth
or falsity of each mutation. This is statement-only evidence pending master acceptance. Primary
source pinpoint review, anchor and terminal-body audit, proof, hermetic validation, and release remain
open. Neither theorem completion nor any accepted receipt is claimed.
