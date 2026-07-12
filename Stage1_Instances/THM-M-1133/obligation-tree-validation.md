# THM-M-1133 obligation-tree validation

Validated on 2026-07-12 in the worker clone at base revision
`c9b3209d36dc2f8783831d5a946196783ef8d684`. The checks used only the existing pinned
Lake environment. No dependency update, build, clone, or fetch ran.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Stage1_Instances/THM-M-1133/build_obligation_artifacts.py` | 0 | Deterministically wrote 16 obligations and 37 typed edges; denominator `8ae5b9f05fb5913dcb53d061df667c4fcbc5343c208bd22cba9c7f78ef506fd6` |
| `python3 Stage1_Instances/THM-M-1133/check_obligation_tree.py` | 0 | Input hashes, denominator, all node fields, reciprocal proof edges, root reachability, acyclicity, structured recipes, forbidden proof constructs, and open-root boundary passed; concatenated exact statement plus conditional composition elaborated with pinned `lake env lean` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 1546 uniform-L0 targets, and execution skill consistent |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets with ranks 1 through 1546 |
| `python3 scripts/stage1_target.py show THM-M-1133` | 0 | Rank 338, planned lifecycle, L0/rework-required, theorem incomplete |
| `git diff --check -- Stage1_Instances/THM-M-1133 .stage1-worker-selftest.json` | 0 | No scoped whitespace errors |

The validator creates a temporary combined Lean source under the owned theorem path because the
hyphenated directory is not a Lean module name. It invokes `lake env lean` from
`Formalizations/Lean`, then removes the temporary source and generated olean. The elaborated
composition proves only that a full weak subsolution maximum principle implies the exact caloric
root. It contains no admission, axiom declaration, or substitute theorem.

## Boundary

Registry v1 freezes the strict-perturbation, compact-extremum, boundary/interior, spatial Hessian,
time-endpoint, contradiction, epsilon-limit, and exact-transport obligations. The equality-to-
subsolution transport is locally checked, but `M1133-T-LIMIT` is the minimal open root cut set and
remains `M4`. Root machine debt remains `M3`; source review, analytic proof bodies, provenance/TCB
closure, release evidence, master acceptance, and theorem completion are not claimed.
