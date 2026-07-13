# THM-M-0931 obligation-tree validation

Item: `S56-M-0931-OBLIGATION_TREE`

Base revision: `b243ebc0f9058ba5afafef8240b92c2dfb2edc6e`

Validation date: `2026-07-13` (`Asia/Shanghai`)

## Frozen result

Registry version 1 freezes 32 obligations and 46 directed typed edges across
separate proof, refinement, provenance, evidence, trust, documentation, and
workflow graphs. Its denominator SHA-256 is
`2b96d10afc8120ac78b0b3029f490c99406b9ea53a07ec3a933108354ae5cd6a`.

The pinned four-line multiset wrapper is expanded through occurrence
enumeration, the indexed prime-composite induction, the ZMod prime polynomial
construction and Chevalley-Warning boundary, and the composite disjoint-block
construction. Internal pinned-body edges are recorded as unverified logical
decomposition plans rather than falsely presented as exact composition
certificates. The Lean harness checks the exact occurrence transport and root
interfaces while leaving the imported EGZ engine explicit.

No obligation is accepted closed. The pinned candidate remains provisional
`M0-W`; the authoritative root remains `H1/M3/R4`,
`audit_complete=false`, and `theorem_complete=false`.

## Commands and results

Commands ran in this worker clone. The canonical pre-existing `.lake` closure
was reused read-only; no update, build, clone, fetch, or dependency mutation
command ran.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | rev-5.6 standard, 15 assurance groups, and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ordered targets with ranks 1 through 1546 passed |
| `python3 scripts/stage1_target.py show THM-M-0931` | 0 | rank 1470; planned; L0/rework-required; theorem incomplete |
| `python3 -B Stage1_Instances/THM-M-0931/build_obligation_artifacts.py --write` | 0 | wrote 32 obligations, 46 typed edges, and denominator `2b96d10a...e5cd6a` |
| `python3 -B Stage1_Instances/THM-M-0931/build_obligation_artifacts.py --check` | 0 | generated registry, graph, and recipe bytes are current |
| `python3 -B Stage1_Instances/THM-M-0931/check_obligation_tree.py` | 0 | statement/anchor hashes, registry, schema, seven graphs, reciprocal proof edges, reachability, plans, recipes, source pins, Lean, receipt, and open closure passed |
| compile `Statement.lean` with the pinned Lake-derived Lean/LEAN_PATH, then elaborate `ObligationTree.lean` with the temporary local module | 0 | canonical root and five conditional compositions elaborated; only expected `propext`, `Classical.choice`, and `Quot.sound`; stdout SHA-256 `5c26658e...d5b3d`; temporary files removed |
| `python3 -m json.tool` on all new structured JSON artifacts | 0 | all structured artifacts parse as JSON |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0931-obligation-pycache python3 -m py_compile ...` | 0 | generator and validator compile outside the repository tree |
| scoped prohibited-construct scan over `ObligationTree.lean` | 1 (expected no match) | no proof gap, bodyless axiom, unsafe/opaque body, native oracle, external implementation, TODO, FIXME, or placeholder |
| `git diff --check -- Stage1_Instances/THM-M-0931 .stage1-worker-selftest.json` | 0 | no whitespace diagnostics |

## Status boundary

This is provisional worker evidence pending dependency-ordered master
acceptance. The pinned anchor is not installed as the canonical proof.
Primary-source H0, independently reviewed R0, full transitive provenance and
trust closure, exact internal composition certificates, hermetic replay,
independent verification, deterministic release evidence, `AUDIT-Z`, and
theorem completion remain open.
