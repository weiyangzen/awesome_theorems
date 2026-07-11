# Anchor-audit validation record

Item: `S56-M-0003-ANCHOR_AUDIT`  
Base revision: `8471ab39f7e977656a7b5ba569063e635a17d5d5`  
Validation date: `2026-07-12` (`Asia/Shanghai`)

## Result

Pinned mathlib supplies the exact pointwise theorem
`ShortComplex.SnakeInput.snake_lemma`. A narrow adapter to every binder of the frozen closed target
elaborates at mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`; Lean reports `propext`,
`Classical.choice`, and `Quot.sound`. Its visible terminal composition uses the four exactness
segments `L0_exact`, `L1'_exact`, `L2'_exact`, and `L3_exact`.

The old repository wrapper has the right pointwise shape but remains unaccepted legacy discovery
evidence. Public search also found an Atlas wrapper at immutable revision `34ffed3...b50`; it uses
the same Lean and mathlib pins and merely calls the same mathlib theorem, while adding no independent
proof body and carrying a restrictive license. The historical Liquid Tensor source at `087fffa...fd`
is Lean 3.48, uses a different encoding, and exposes the inspected exactness statements behind a
`has_snake_lemma` premise. Neither is a useful external integration candidate.

The root is therefore `M1`, not `M0-W`: exact immutable upstream closure and adapter feasibility
are established, but the proof phase must install the canonical root wrapper, and later validation
must close transitive provenance, trust, composition, and TCB gates. This phase does not complete
the target audit or theorem.

## Commands and results

All commands ran inside this worker clone. Lean used only the existing pinned Lake environment; no
update, fetch, clone, build, or other `.lake` mutation command was run.

| Command | Exit | Result |
|---|---:|---|
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0003/AnchorAudit.lean` | 0 | seven declarations checked; exact full-target adapter elaborated; axiom set printed |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0003/Statement.lean` | 0 | frozen target and its checked statement transport re-elaborated |
| `python3 Stage1_Instances/THM-M-0003/check_anchor_audit.py` | 0 | immutable mathlib revision/tree/clean state, license hash, source hash, required bodies, and legacy hash verified; root `M1` |
| `lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `curl` Sourcegraph indexed query for `snake_lemma` or `SnakeInput` | 0 | 27 matches in three repositories; response SHA-256 `6d1349...456`; mathlib, Atlas, and lean-liquid classified |
| GitHub repository search for `snake lemma Lean` | 0 | zero repositories, complete response; SHA-256 `08c082...00b` |
| GitHub code search for `snake_lemma language:Lean` | 0 | captured HTTP 401 authentication blocker; SHA-256 `b7dbd1...29e`; no negative result claimed |
| immutable raw/tree inspection of `facebookresearch/atlas-lean@34ffed3...b50` | 0 | exact wrapper source, Lean/mathlib pins, complete 2860-entry tree, and restrictive license recorded |
| immutable raw/tree inspection of `leanprover-community/lean-liquid@087fffa...fd` | 0 | Lean 3.48/mathlib pins and conditional snake interface recorded from complete 482-entry tree |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | rev-5.6 standard and 1546-target projection valid |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ordered uniform-L0 targets valid |
| `python3 scripts/stage1_target.py show THM-M-0003` | 0 | rank 98, planned, legacy artifacts unaccepted, theorem incomplete |
| `git diff --check -- Stage1_Instances/THM-M-0003 .stage1-worker-selftest.json` | 0 | no whitespace errors |

Bounded public-index searches are discovery evidence, not proof of global absence. Reopen the
external lane if a distinct exact Lean 4 proof body appears at an immutable revision with compatible
licensing and a materializable pinned dependency closure.
