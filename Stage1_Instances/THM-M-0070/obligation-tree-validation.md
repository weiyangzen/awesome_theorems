# THM-M-0070 obligation-tree validation

Item: `S56-M-0070-OBLIGATION_TREE`

Base revision: `250f9e73cbbb3ebd2da9d0cefff78f0ab8c0d056`

Base tree: `b6e8138c58e31e82f8209cb70fbc0fb253f3654a`

Validation date: `2026-07-13` (`Asia/Shanghai`)

## Result

The registry freezes 61 unique semantic obligations with denominator SHA-256
`b9832ebb2a8e07834e24753c74f59a665c5c012f873bfc06eabb637def4c5686`.
The typed graph bundle has 89 directed edges across proof, refinement, provenance, evidence, trust,
documentation, and workflow graphs. The exact conditional Lean route has reciprocal
`proof_requires` and `composes` edges. The MathComp, infrastructure, Bender-Glauberman, and
Peterfalvi routes are open `logical_decomposition` architecture because no semantics-preserving Lean
translation or local composition certificates exist; they receive no closure credit. A 2,084-entry
source declaration subregistry records every exact declaration command in the immutable source
below the package nodes. It additionally freezes 229 body chunks of at most 80 substantive source
lines for oversized declarations; all remain open pending Lean translation and checked composition.

The narrow Lean check re-elaborates the exact statement in a temporary directory, then checks the
translated-body equivalence, adapter, terminal, and root compositions. Each reports only
`[propext, Classical.choice, Quot.sound]`. The translated theorem is an explicit premise. The local
module has no placeholder or escape declaration and does not prove the root.

## Commands and exact outcomes

Commands ran from the repository root unless the table gives another working directory. The
automation-provided pinned `.lake` symlink was reused read-only. No update, build, clone, fetch, or
other dependency mutation command ran.

| Command | Exit | Exact outcome |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0070` | 0 | rank 1101, planned, `L0/rework_required`, theorem incomplete |
| `python3 -B Stage1_Instances/THM-M-0070/build_obligation_artifacts.py` | 0 | deterministically wrote 61 obligations, 89 typed edges, and denominator `b9832ebb...5686` |
| `python3 -B Stage1_Instances/THM-M-0070/check_obligation_tree.py --worker-packet` | 0 | generated artifacts, main and source sub-denominators, 2,084 exact source commands, 229 bounded body chunks, typed graphs, conditional Lean composition, receipt/self-test agreement, public ledger, and open-root boundary passed |
| compile `Statement.lean` to a temporary `.olean`, then elaborate `ObligationTree.lean` with the temporary path under `lake env lean` | 0 each | four conditional declarations elaborated with only `propext`, `Classical.choice`, and `Quot.sound`; obligation output SHA-256 `a5972c2a...1b1f3`; temporary files removed |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0070-obligation-pycache python3 -m py_compile Stage1_Instances/THM-M-0070/build_obligation_artifacts.py Stage1_Instances/THM-M-0070/check_obligation_tree.py` | 0 | generator and validator compiled outside the repository tree |
| `python3 -m json.tool` over all owned JSON files and `.stage1-worker-selftest.json` | 0 | all structured artifacts parsed |
| scoped prohibited-token scan of `ObligationTree.lean` | 1 (expected no match) | no proof gap, bodyless axiom, unsafe/opaque declaration, native oracle, external implementation, TODO, FIXME, or placeholder |
| `git diff --check -- Stage1_Instances/THM-M-0070 .stage1-worker-selftest.json` plus new-file checks | 0 | no whitespace diagnostics |

## Status boundary

This self-test covers only the obligation-tree phase. The exact external Lean declaration remains
an incompatible-pin `by sorry` placeholder. The exact MathComp theorem remains an E3/M3 source and
architecture anchor in Coq/Rocq, not a Lean kernel object. Package nodes need theorem-level recursive
expansion and checked Lean composition before proof acceptance. Human-source H0, independently
reviewed R0, a placeholder-free Lean body, transitive provenance and trust, hermetic replay,
independent verification, validation, release, `AUDIT-Z`, theorem completion, and master acceptance
are all open.
