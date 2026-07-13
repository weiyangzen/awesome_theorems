# THM-M-0061 obligation-tree validation

Item: `S56-M-0061-OBLIGATION_TREE`

Base revision: `0d2c3bdcd192266bc255ac3d5186da604517145a`

Base tree: `eafbcb48efd51d9cda34f0fc1afe780434abad64`

Validation date: `2026-07-13` (`Asia/Shanghai`)

## Frozen result

Registry version 1 freezes 20 obligations and 79 directed typed edges across separate proof,
refinement, provenance, evidence, trust, documentation, and workflow graphs. The denominator
SHA-256 is `2d426a22d370fa53b308df9aa74a4cbaa69b1b30864da4ec30e1c8c31ba330d7`.

The visible mathlib body is expanded through the quotient-times-subgroup cardinal identity,
`Nat.card_prod`, `Nat.card_congr`, and the fiber/coset construction of
`Subgroup.groupEquivQuotientProdSubgroup`. Five conditional composition declarations consume their
explicit child interfaces and elaborate into the actual frozen root. They do not install the
audited anchor.

No obligation is accepted closed. The anchor audit found a provisional `M0-W` candidate, while the
frozen anchor node remains `M3` pending an exact proof-phase wrapper and E1 receipt; the root stays
`H1/M3/R4`, `audit_complete=false`, and `theorem_complete=false`.

## Commands and results

Commands ran in this worker clone. The canonical pre-existing `.lake` closure was reused read-only;
no update, build, clone, fetch, or other dependency mutation command ran.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | rev-5.6 standard, 15 assurance groups, and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ordered targets with ranks 1 through 1546 passed |
| `python3 scripts/stage1_target.py show THM-M-0061` | 0 | rank 1093; planned; L0/rework-required; theorem incomplete |
| `python3 -B Stage1_Instances/THM-M-0061/build_obligation_artifacts.py` | 0 | wrote 20 obligations, 79 typed edges, and denominator `2d426a22...ba330d7` |
| `python3 -B Stage1_Instances/THM-M-0061/check_obligation_tree.py` | 0 | registry/instance hash, exclusions, denominator, node schemas, seven graphs, reciprocal edges, reachability, recipes, pins, source markers, receipt, readable anchors, and open closure passed |
| compile `Statement.lean` to `/tmp`, then elaborate `ObligationTree.lean` with the temporary local module using pinned `lake env lean` | 0 each | exact root and five conditional compositions elaborated; each reports only `propext`, `Classical.choice`, and `Quot.sound`; obligation stdout SHA-256 `1c91b97e...574fd` |
| `python3 -m json.tool` over the four obligation JSON artifacts and root packet | 0 | all structured artifacts parse as JSON |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0061-obligation-pycache python3 -m py_compile ...` | 0 | generator and validator compile outside the repository tree |
| scoped prohibited-construct scan over `ObligationTree.lean` | 1 (expected no match) | no proof gap, axiom declaration, unsafe/opaque body, native oracle, external implementation, TODO, FIXME, or placeholder |
| `git diff --check -- Stage1_Instances/THM-M-0061 .stage1-worker-selftest.json` plus per-new-file checks | 0 | no whitespace diagnostics |

## Status boundary

This is provisional worker evidence pending dependency-ordered master acceptance. The exact pinned
anchor is not installed as the canonical proof. Primary-source H0, independently reviewed R0, full
transitive provenance and trust closure, hermetic replay, independent verification, deterministic
release evidence, `AUDIT-Z`, theorem completion, and release remain open.
