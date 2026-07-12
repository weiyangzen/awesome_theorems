# THM-M-0012 obligation-tree validation

Item: `S56-M-0012-OBLIGATION_TREE`

Base revision: `35681bf154be61836528486ed7830f619fc03231`

Validation date: `2026-07-13` (`Asia/Shanghai`)

## Frozen result

Registry version 1 freezes 20 obligations and 41 directed typed edges across separate proof,
refinement, provenance, evidence, trust, documentation, and workflow graphs. The denominator
SHA-256 is `7b88f176772ea12d0c55182ab67a6bc8cbeb6b786fbca2912819b59f4c103817`.

The visible `Complex.exists_root` body is expanded into root-free contradiction, reciprocal
differentiability, reciprocal decay, Liouville, polynomial identity, and exact composition nodes.
The algebraic-closedness routes are deduplicated to the same terminal body. The checked Lean
harness consumes every premise in the analytic and root compositions while leaving each engine
explicit. It returns the actual frozen `FundamentalTheoremOfAlgebraTarget`, not a weaker or
substituted claim.

No obligation is accepted closed. The exact pinned anchor remains candidate-only `M0-W`; the
authoritative root remains `H1/M3/R4`, `audit_complete=false`, and `theorem_complete=false`.

## Commands and results

Commands ran in this worker clone. The canonical pre-existing `.lake` closure was reused read-only;
no update, build, clone, fetch, or other dependency mutation command ran.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | rev-5.6 standard, 15 assurance groups, and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ordered targets with ranks 1 through 1546 passed |
| `python3 scripts/stage1_target.py show THM-M-0012` | 0 | rank 1062; planned; L0/rework-required; theorem incomplete |
| `python3 -B Stage1_Instances/THM-M-0012/build_obligation_artifacts.py` | 0 | wrote 20 obligations, 41 typed edges, and denominator `7b88f176...103817` |
| `python3 -B Stage1_Instances/THM-M-0012/check_obligation_tree.py` | 0 | registry and instance hash, exclusions, denominator, schema, graphs, reciprocal edges, reachability, recipes, pinned source markers, receipt, and open closure passed |
| compile `Statement.lean` with the pinned Lake-derived Lean/LEAN_PATH, then elaborate `ObligationTree.lean` with the temporary local module | 0 | actual canonical root and three conditional compositions elaborated; only `propext`, `Classical.choice`, and `Quot.sound`; stdout SHA-256 `60775c70...ca1b`; temporary `.olean`/`.ilean` removed |
| `python3 -m json.tool` on the four obligation JSON artifacts and root packet | 0 | all structured artifacts parse as JSON |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0012-obligation-pycache python3 -m py_compile ...` | 0 | generator and validator compile outside the repository tree |
| scoped prohibited-construct scan over `ObligationTree.lean` | 1 (expected no match) | no proof gap, axiom declaration, unsafe/opaque body, native oracle, external implementation, TODO, FIXME, or placeholder |
| `git diff --check -- Stage1_Instances/THM-M-0012 .stage1-worker-selftest.json` | 0 | no whitespace diagnostics |

## Status boundary

This is provisional worker evidence pending dependency-ordered master acceptance. The exact pinned
anchor is not installed as the canonical proof. Primary-source H0, independently reviewed R0,
full transitive provenance and trust closure, hermetic replay, independent verification,
deterministic release evidence, `AUDIT-Z`, and theorem completion remain open.
