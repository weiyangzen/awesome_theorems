# Anchor-audit validation

Item: `S56-M-0707-ANCHOR_AUDIT`  
Base revision: `136ebf643dcdcbc42cef34e415177189578060ef`

## Result

Pinned mathlib contains a proof-bearing anchor in `Mathlib.Computability.Halting`:
`ComputablePred.halting_problem n` proves that no computable predicate decides whether an arbitrary
code halts on the fixed input `n`. This is not definitionally the canonical pair predicate, so the
audit added a checked transport rather than claiming a name match. Given a pair decider, composing
its Boolean indicator with the computable map `c |-> (c, 0)` produces the forbidden fixed-input
decider. `AnchorAudit.lean` elaborates that implication at the exact expanded canonical type.

The terminal body is mathlib's theorem, which invokes Rice's theorem using the terminating zero
function and the nowhere-defined function. Machine `#print axioms` output for both the terminal
anchor and the wrapper is `Classical.choice`, `Quot.sound`, and `propext`; it reports no additional
axioms. This is provisional node evidence only: the later obligation-tree and validation phases
must freeze and check the transitive provenance, foundation, and TCB profiles before acceptance.

Repo-local searches found no competing proof body. Bounded external searches found no additional
candidate: two content-hashed Sourcegraph queries returned zero matches, GitHub repository search
returned a complete zero-result response, and the non-truncated 1204-path tree of
`google-deepmind/formal-conjectures@b2e608fc52d765510915a244bb69b1a2741acc3c` has no halting-named
path. These are bounded discovery results, not a claim that no other formalization exists.

## Commands and results

Commands ran on 2026-07-12 in the worker clone. Existing pinned `.lake` artifacts were read only;
no update, build, clone, fetch, or dependency mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546 |
| `python3 scripts/stage1_target.py show THM-M-0707` | 0 | rank 748, planned, theorem incomplete |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | exact manifest pin `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `rg -n -i 'halting[_ -]?problem|computablepred.*eval|eval.*computablepred'` over repo-local, pinned mathlib, and pinned flt-regular Lean sources | 0 | exact proof candidate only in pinned `Mathlib/Computability/Halting.lean`; adjacent local statement surfaces also listed |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0707/Statement.lean)` | 0 | canonical statement and boundary tests re-elaborated |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0707/AnchorAudit.lean)` | 0 | candidate types, exact transport wrapper, and axiom reports checked |
| Sourcegraph immutable-response searches recorded in `anchor-audit.json` | 0 | both `matchCount=0`; response SHA-256 values recorded |
| GitHub REST repository search recorded in `anchor-audit.json` | 0 | `total_count=0`, `incomplete_results=false` |
| GitHub recursive tree for Formal Conjectures commit `b2e608...` | 0 | 1204 paths, `truncated=false`, no halting path; response SHA-256 `76fa3f...fc61` |
| `python3 -m json.tool Stage1_Instances/THM-M-0707/anchor-audit.json` | 0 | valid JSON |
| forbidden-token scan over owned Lean files | 0 | expected no-match condition passed |
| `git diff --check -- Stage1_Instances/THM-M-0707 .stage1-worker-selftest.json` | 0 | no whitespace errors |

## Status boundary

The anchor node is self-tested and supports provisional `M0-W`: the exact conclusion is derived by
a local checked wrapper from a proof-bearing theorem at the pinned mathlib revision. Human-source
debt remains `H1`, readable reconstruction remains incomplete, and the full audit, trust,
reproducibility, independent-verification, and release gates remain open. Consequently
`audit_complete=false` and `theorem_complete=false`.
