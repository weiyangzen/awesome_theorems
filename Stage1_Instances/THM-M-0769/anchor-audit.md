# Anchor audit record

Item: `S56-M-0769-ANCHOR_AUDIT`  
Base revision: `c72bad9e8827ffb1ba1a585dbe346c88393b4a3f`

## Immutable environment

The audit used Lean `v4.29.0` (commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`) and mathlib tag `v4.29.0`, commit
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. Both are already selected by the repository's pinned
toolchain and lake manifest. The mathlib checkout was clean. No dependency update, build, clone, or
fetch was run.

## Candidate inventory

| Candidate | Immutable locator | Exact-target relation | Terminal body and trust |
|---|---|---|---|
| `Pi.instNonempty` | Lean core `Init.Prelude`, line 820, toolchain commit above | Its explicit application to `h : forall i, Nonempty (A i)` has exactly the frozen target conclusion for `Sort u` / `Sort v` | Constructs a Pi inhabitant through `Classical.ofNonempty`; `#print axioms` reports only `Classical.choice` |
| `Classical.nonempty_pi` | `Mathlib.Logic.Nonempty`, line 108, mathlib commit above | The reverse implication of the iff is the exact target, with no domain or universe narrowing | Reverse direction is `@Pi.instNonempty`; `#print axioms` reports only `Classical.choice` |
| `Classical.choice` | Lean core `Init.Prelude`, line 795, toolchain commit above | Direct pointwise selection yields the exact dependent function under `Nonempty` | This is the declared foundational axiom; `Classical.axiomOfChoice` in `Init.Classical`, line 122, is a dependent relational wrapper |

All three compile-time witnesses in `AnchorAudit.lean` have the literal frozen binder sequence and
conclusion. None contains `sorry`, an added axiom, an unsafe declaration, an oracle, or a narrower
substitute. The expected axiom result is important here: this target formalizes choice as a
foundational principle, so hiding `Classical.choice` would be a provenance failure rather than an
improvement.

The pinned-package and repo-local search found no further exact candidate outside Lean core and
mathlib. `Mathlib.Logic.Encodable.Basic.axiom_of_choice` is not eligible as an exact anchor: it is
restricted to `Type` families with `Encodable` fibers. There is therefore no anchor-only external
project to credit and no moving dependency was fetched merely to manufacture one.

## Validation

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | standard valid; 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546 |
| `python3 scripts/stage1_target.py show THM-M-0769` | 0 | rank 779; lifecycle planned; theorem completion false |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0769/AnchorAudit.lean` | 0 | all exact candidate witnesses elaborated; all three axiom reports were `[Classical.choice]` |
| `python3 -m json.tool Stage1_Instances/THM-M-0769/anchor-audit.json` | 0 | structured audit valid JSON |
| `rg -n '\\b(sorry|admit)\\b|^\\s*axiom\\b|unsafe' Stage1_Instances/THM-M-0769/AnchorAudit.lean` | 1 | no placeholder, added axiom, or unsafe declaration found |
| `git diff --check -- Stage1_Instances/THM-M-0769 .stage1-worker-selftest.json` | 0 | no whitespace errors |

This phase establishes a self-tested candidate and provenance audit only. It does not accept a
proof node, close the obligation tree, establish H0/M0/R0, or claim theorem completion. Master
acceptance is still required.
