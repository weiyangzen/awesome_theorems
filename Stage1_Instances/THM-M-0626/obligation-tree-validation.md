# THM-M-0626 obligation-tree validation

Item: `S56-M-0626-OBLIGATION_TREE`.

Base revision: `0c019b7194c9c43fa5f683fa82d637a0b275410d` (tree
`43cf6ac322b1dba09be739b52ab3d02e9f9d8f3e`). Validation date: 2026-07-13
(`Asia/Shanghai`).

## Frozen result

Registry version 1 freezes 22 obligations and 51 directed typed edges across separate proof,
refinement, provenance, evidence, trust, documentation, and workflow graphs. The frozen
denominator SHA-256 is `9c6e54699269263a82e13f7b771daf802103b4a4e0114d1c6a76a98918487270`.

The pinned `IsConnected.image` terminal body is expanded into global-to-local continuity, image
nonemptiness, and the substantive `IsPreconnected.image` route. The latter exposes the arbitrary
open-set goal, relative-preimage construction, image-cover normalization, witness pullback, source
intersection, and intersection pushforward. Candidate wrappers and the local conditional body
reconstruction are deduplicated from the same terminal bodies. The pinned candidate is the immediate
machine-proof cut; its reconstructed body is an alternative refinement route, not a mandatory
duplicate premise. The workflow graph separately mirrors all seven authoritative task nodes.

The Lean harness checks six conditional child-to-parent certificates. Each exact child package is
an explicit premise: no candidate or mathematical leaf is installed by this phase. No obligation
is accepted closed. The pinned anchor's `M0-W` label is recorded only as a candidate field while
its accepted node debt remains `M3`. The authoritative root remains `H1/M3/R4`,
`audit_complete=false`, and `theorem_complete=false`.

The per-node validation recipes check structure only and therefore claim no covered Lean
declarations. Kernel coverage for the six conditional compositions comes from the separately
recorded scoped Lean invocation; it must not be inferred from the Python checker recipes.

## Commands and results

Commands ran in the isolated worker clone. The automation-provided canonical `.lake` closure was
used read-only; no update, build, clone, fetch, dependency installation, or dependency mutation
command ran.

| Command | Exit | Exact result summary |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0626` | 0 | rank 1320, planned, legacy artifacts unaccepted, theorem incomplete |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree recorded above |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | Lean 4.29.0 commit `98dc76e3...`; Lake `5.0.0-src+98dc76e` |
| pinned mathlib revision, tree, source hash, and clean-status checks | 0 | revision `8a178386...ea95`, tree `bdc39a31...e5c2b`, `Connected/Basic.lean` SHA-256 `929f0e1c...e9c`, clean package worktree |
| `python3 -B Stage1_Instances/THM-M-0626/build_obligation_artifacts.py` | 0 | wrote 22 obligations and 51 typed edges; denominator `9c6e5469...87270` |
| `python3 -B Stage1_Instances/THM-M-0626/check_obligation_tree.py` | 0 | deterministic generation, assignment/DAG, registry schema, denominators, exclusions, all node fields, seven graphs, reciprocal edges, acyclicity, exact proof reachability, recipes, source markers, open closure, receipt/packet linkage, and hygiene passed |
| `cd Stage1_Instances/THM-M-0626 && LEAN_PATH="$PINNED_LEAN_PATH" "$LEAN_BIN" -o "$TMP_DIR/Statement.olean" -i "$TMP_DIR/Statement.ilean" Statement.lean` followed by `LEAN_PATH="$TMP_DIR:$PINNED_LEAN_PATH" "$LEAN_BIN" ObligationTree.lean` | 0 | `LEAN_BIN` and `PINNED_LEAN_PATH` were obtained read-only via `cd Formalizations/Lean && lake env which lean` and `lake env printenv LEAN_PATH`; exact root and six conditional compositions elaborated; temporary files were outside the repository and removed |
| `python3 -m json.tool Stage1_Instances/THM-M-0626/instance.json Stage1_Instances/THM-M-0626/obligation-registry.json Stage1_Instances/THM-M-0626/typed-graphs.json Stage1_Instances/THM-M-0626/validation-specs.json Stage1_Instances/THM-M-0626/obligation-tree-receipt.json .stage1-worker-selftest.json` (one invocation per file) | 0 | all structured artifacts parsed |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0626-obligation-pycache python3 -m py_compile Stage1_Instances/THM-M-0626/build_obligation_artifacts.py Stage1_Instances/THM-M-0626/check_obligation_tree.py` | 0 | generator and checker compiled outside the repository tree |
| scoped prohibited-construct scan over `ObligationTree.lean` | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, axiom declaration, unsafe/opaque body, native oracle, external implementation, TODO, FIXME, or placeholder |
| `git diff --check -- Stage1_Instances/THM-M-0626 .stage1-worker-selftest.json` | 0 | no whitespace diagnostics |

## Status boundary

This is provisional worker evidence pending dependency-ordered master acceptance. The anchor-audit
predecessor is still `[_]`, not `[x]`. The exact pinned candidate is not installed as the canonical
proof, and the six internal body leaves remain open packages. Pinpoint primary-source `H0`,
independently reviewed `R0`, full transitive provenance/foundation/TCB closure, proof installation,
hermetic replay, deterministic evidence, independent verification, `AUDIT-Z`, validation, release,
and theorem completion remain open.
