# S56-M-1259-OBLIGATION_TREE validation

Validation is scoped to registry/graph structure and the one implemented composition certificate.
It does not validate either open PDE leaf or the theorem root.

Exact commands and results are recorded after execution below.

Base revision: `a2155813bf24b8d57420bbdcd9ea603a457a2ec6`.

| Command | Exit | Exact result |
|---|---:|---|
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1259/Statement.lean` | 0 | Printed the root, expanded core, and composition types; no diagnostics |
| `python3 -m json.tool Stage1_Instances/THM-M-1259/obligation_registry.json >/dev/null` | 0 | Registry JSON syntax valid |
| `python3 -m json.tool Stage1_Instances/THM-M-1259/typed_graphs.json >/dev/null` | 0 | Typed-graphs JSON syntax valid |
| dossier graph invariant script | 0 | 7 canonical obligations equal 7 node obligations; proof endpoints valid; proof graph acyclic; all step budgets at most 100 |
| forbidden-token scan of `Statement.lean` | 0 | No `sorry`, `admit`, `axiom`, or `sorryAx` token |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`; 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | `ok`; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1259` | 0 | Rank 161, lane `hard_mathlib_anchor_and_wrapper`, lifecycle `planned`, theorem incomplete |
| `git diff --check -- Stage1_Instances/THM-M-1259` | 0 | No whitespace errors |

The graph invariant script loads both JSON files, checks the declared counts and exact obligation
set, validates proof-edge types and endpoints, performs depth-first cycle detection, checks every
node budget, and verifies that all non-proof edge records are explicitly typed.

SHA-256 after validation: registry
`2eb6b3db5d79dbed5b9f22dd467cfb964b15a3441927919e635670715342d1a0`; graphs
`d48d5c6724a1716e82685ad535cfc8dcc1df6f3f75fc5fe691d6e13fcab7259b`; Lean source
`8258728ff71980a4431fb47213487c8d7655c64d0dd0f3ab2e9b058f8a95c0c7`.

An earlier exploratory command run from the repository root invoked bare `lean` rather than the
pinned Lake environment and exited 1 with `no default toolchain configured`. It did not validate
anything and was superseded by the successful pinned command above. No dependency was fetched or
updated.

The obligation-tree phase is self-tested, but the theorem is not: the two critical PDE leaves and
the later proof-body trust audit remain open, so root debt stays `M4` and theorem completion is
false.
