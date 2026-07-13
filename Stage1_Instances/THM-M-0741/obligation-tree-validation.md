# THM-M-0741 obligation-tree validation

Item: `S56-M-0741-OBLIGATION_TREE`

Base revision: `a3b18eec39bf04be025b1641cae02f4d44fdf11a`

Validation date: `2026-07-13` (`Asia/Shanghai`)

## Frozen Result

Registry version 1 freezes 19 records and 70 directed typed edges across separate proof,
refinement, provenance, evidence, trust, documentation, and workflow graphs. The denominator
SHA-256 is `ee9b5029b7cb4a820132e16aeeb1a5c6e304e81bb8624f0f931aee9547cb9bcd`.

The pinned fixed-input theorem is expanded through Rice semantic transfer, fixed-point and
conditional constructions, the exhaustive membership split, and positive/negative definedness
witnesses. Those Rice internals and the statement/boundary records are informational non-machine
expository overlays in registry version 1 and receive no independent machine credit. The pair
target is separately expanded through the computable pair-zero embedding,
restriction of both components of `ComputablePred`, and exact root composition. The target-owned
Lean harness consumes every child of the four checked compositions while leaving imported proof
bodies explicit. It returns the actual frozen `HaltingProblemUndecidable`, not a fixed-input or
self-input substitute.

No obligation is accepted closed. The exact pinned bodies remain proof-phase candidates below E1;
the authoritative root remains `H1/M3/R4`, `audit_complete=false`, and
`theorem_complete=false`.

## Commands And Results

Commands ran in this worker clone. The pre-existing canonical `.lake` symlink was reused read-only;
no update, build, clone, fetch, or dependency mutation command ran.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | rev-5.6 standard and all 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | all 1546 unique ordered targets and ranks passed |
| `python3 scripts/stage1_target.py show THM-M-0741` | 0 | rank 1329; planned; L0/rework-required; theorem incomplete |
| `python3 -B Stage1_Instances/THM-M-0741/build_obligation_artifacts.py` | 0 | wrote 19 registry records, 70 typed edges, and denominator `ee9b5029...7cb9bcd` |
| `python3 -B Stage1_Instances/THM-M-0741/check_obligation_tree.py` | 0 | registry and instance hashes, exclusions, denominator, schema, 19 ledgers, graphs, reciprocal proof edges, root reachability, recipes, source pins, disposable Lean checks, receipt, open closure, and hygiene passed |
| pinned Lean compile of `Statement.lean` to a temporary OLean, then temporary-`LEAN_PATH` elaboration of `ObligationTree.lean` | 0 | exact root and all conditional compositions elaborated; no `sorryAx`; output SHA-256 `5d685af0...57c33df`; temporary artifacts were outside the repository |
| `python3 -m json.tool` on all obligation JSON artifacts and the worker packet | 0 | every structured artifact parses as JSON |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0741-obligation-pycache python3 -m py_compile ...` | 0 | generator and validator compile outside the repository tree |
| deterministic regeneration followed by hash comparison | 0 | registry, graphs, and validation specs reproduced byte-for-byte |
| scoped prohibited-construct scan over `ObligationTree.lean` | 1 (expected no match) | no proof gap, axiom declaration, unsafe/opaque body, oracle, external implementation, TODO, FIXME, or placeholder |
| `git diff --check -- Stage1_Instances/THM-M-0741 .stage1-worker-selftest.json` | 0 | no whitespace diagnostics |

## Status Boundary

This is provisional worker evidence pending dependency-ordered master acceptance. The pinned
fixed-input and Rice bodies are not installed as the canonical proof. Primary-source H0,
independently reviewed R0, full transitive provenance and trust closure, hermetic replay,
independent verification, deterministic release evidence, `AUDIT-Z`, and theorem completion remain
open.
