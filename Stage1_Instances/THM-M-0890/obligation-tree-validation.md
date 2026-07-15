# THM-M-0890 obligation-tree validation

Item: `S56-M-0890-OBLIGATION_TREE`

Base revision: `6ac589f0d8c5a9eeb726a1a05def7f9467ea2e2d`

Base tree: `9e8c2b617c489611e447b350a4b4cf4aeff15f39`

Validation date: `2026-07-15` (`Asia/Shanghai`)

## Frozen result

Registry version 1 freezes 33 source-faithful obligations before observed proof status. The seven
typed graph families contain 129 edges. Three exact parent certificates cover the
witness/estimate-to-division-free transport and denominator/division-free-to-root spine. The pinned
maximum-independent-set wrapper is also checked as an interface, without being modeled as a child
composition. Ten deeper spectral, positive-semidefinite, principal-submatrix, and scalar relations
remain explicitly unverified `logical_decomposition` plans. There are no accepted closed
obligations and no terminal proof body.

The registry denominator SHA-256 is
`259c6e160437f0fc2646c6f1e302441c3e129c6d3e70346d04438ea3f7a45169`.

## Commands and exact results

The initial status contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink. Existing canonical pinned artifacts were reused read-only. No
`lake update`, `lake build`, dependency clone/fetch, checkout, network access, or `.lake` mutation
was performed.

| Command | Exit | Exact result and boundary |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and all 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0890` | 0 | rank 1440; planned; legacy artifacts unaccepted; theorem incomplete |
| `python3 -B Stage1_Instances/THM-M-0890/build_obligation_artifacts.py` | 0 | deterministically wrote 33 obligations and 129 typed edges; denominator `259c6e16...5169` |
| `python3 -B Stage1_Instances/THM-M-0890/check_obligation_tree.py` | 0 | regeneration, schemas, hashes, eligibility, mandatory layers, 33 ledgers, anchors, recipes, graph endpoints/reciprocity/reachability/acyclicity, pins, hygiene, receipt, and open root passed |
| `python3 -B Stage1_Instances/THM-M-0890/check_obligation_tree.py --run-lean` | 0 | temporary `Statement.olean` plus exact conditional composition under `--trust=0` passed; five declarations were sorry-free and reported exactly `propext`, `Classical.choice`, `Quot.sound`; stdout SHA-256 `91dcc562...b8ce8` |
| `python3 -m json.tool` on registry, graph bundle, specs, receipt, and worker packet | 0 | every structured artifact parsed |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0890-obligation-pycache python3 -m py_compile ...` | 0 | builder and checker compiled without owned-path cache output |
| comment-aware prohibited-construct scan embedded in the checker | expected no match | no `sorry`, `admit`, `sorryAx`, bodyless axiom/constant, unsafe/opaque declaration, external implementation, native oracle, or placeholder |
| `git diff --check -- Stage1_Instances/THM-M-0890 .stage1-worker-selftest.json` | 0 | no whitespace errors |

## Evidence boundary

`ObligationTree.lean` consumes exact abstract denominator and maximum-independent-set estimate
premises and yields the unchanged root. It also checks the pinned maximum-independent-set witness
API. It does not prove strict negativity of the least eigenvalue, construct or prove positive
semidefinite the Hoffman matrix, evaluate the principal quadratic form, or establish the scalar
estimate. Its axiom report is an observation, not accepted transitive trust closure.

The evidence graph and terminal-body provenance overlay contain no edges because no corresponding
evidence or terminal proof body exists. The import-audit and source maps are non-proof provenance
relations and create no proof premise or closure.
This receipt is warm, non-content-addressed worker evidence pending dependency-ordered master
acceptance. Release-grade source snapshots, TCB/SBOM, cold offline replay, second runner, and
independent verification belong to later gates.

## Status boundary

The minimal open machine root cut is `M0890-N-DENOMINATOR` plus
`M0890-L-SCALAR-ESTIMATE`. Primary-source H0 and independent review, readable R0 and independent
review, ten internal child-to-parent composition certificates, transitive provenance/trust, hermetic validation,
independent verification, `AUDIT-Z`, `THEOREM-Z`, and master acceptance remain open. The root stays
`[H1, M3, R4]`; `audit_complete=false` and `theorem_complete=false`.
