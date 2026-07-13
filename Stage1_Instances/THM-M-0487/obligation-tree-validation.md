# THM-M-0487 obligation-tree validation

Item: `S56-M-0487-OBLIGATION_TREE`

Base revision: `b56df790fc94c5366cf919a6fe5411d06b427c59`

Validation date: `2026-07-13` (`Asia/Shanghai`)

## Frozen Result

Registry version 1 freezes 54 canonical obligations and 297 directed typed edges across proof,
refinement, provenance, evidence, trust, documentation, and workflow graphs. Its denominator is
`1d456b6ecd31a58a47bac58a2746bc0f8d16ce4b4e2821348331c511e21c1a41`.

The source-visible analytic route and finite prime-ladder route are explicit. Certificate replay is
a selected fail-closed formal refinement, not a claim that the historical paper supplied retained
data or kernel certificates. No deep package is closed and accepted proof state is empty.

## Commands And Results

Commands ran in this worker clone. The existing manifest-pinned Lake artifacts were reused
read-only; no Lake update/build, dependency clone/fetch, or `.lake` mutation command ran.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | rev-5.6 standard and all 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ordered targets passed |
| `python3 scripts/stage1_target.py show THM-M-0487` | 0 | rank 1366; planned; L0/rework-required; theorem incomplete |
| `python3 -B Stage1_Instances/THM-M-0487/build_obligation_artifacts.py` | 0 | wrote 54 obligations, 297 edges, and the denominator above; repeated generation was byte-identical |
| `python3 -B Stage1_Instances/THM-M-0487/check_obligation_tree.py` | 0 | registry, typed graphs, source pins, pinned Lean replay, receipt, open closure, ownership, and hygiene passed |
| checker-managed temporary `Statement.olean` followed by `ObligationTree.lean` under the pinned Lean binary and `LEAN_PATH` | 0 | seven local interfaces elaborated; only `propext`; stdout SHA-256 `0f7c5d25dd2af2e4b97f9227d38d95cf24b34abb97e5971d4db4305ff1d16a40`; temporary outputs removed |
| `python3 -m json.tool` on current structured artifacts | 0 | all JSON parsed |
| external-cache `python3 -m py_compile` on owned Python tools | 0 | Python compilation passed outside the repository |
| scoped prohibited-construct scan over `ObligationTree.lean` | 1 (expected no match) | no proof escape, custom axiom, unsafe/opaque body, native oracle, external implementation, TODO, FIXME, or placeholder |
| `git diff --check -- Stage1_Instances/THM-M-0487 .stage1-worker-selftest.json` | 0 | no whitespace diagnostics |

## Status Boundary

The local Lean module proves only representation equivalence, cutoff exhaustiveness, exact endpoint
arithmetic, finite-interval coverage and restriction, and conditional range recomposition. It
assumes the substantive analytic and finite upper packages and does not validate the historical
Helfgott-Platt computation. Root debt remains `[H1, M3, R3]`; accepted closure, H0, R0, validation,
independent verification, release, `AUDIT-Z`, and theorem completion remain open.
