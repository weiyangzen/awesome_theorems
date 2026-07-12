# Intake validation

Base revision: `d502dd6f3d278ca9cb0ead8cbdc5f16c0e1fd8c9`; base tree:
`829a47c47ae831cada4f8acc6c2c00ba5883215e`. Validation date: 2026-07-13
(Asia/Shanghai); exact start and end timestamps are recorded in the provisional receipt.

This validation covers target membership, the planned dossier and open task DAG, repository-source
provenance, source/root discrimination, JSON and scoped invariants, a narrow pinned Lean substrate
probe, bounded repository/mathlib discovery, prohibited-construct hygiene, and whitespace. It does
not validate a canonical Hamiltonian-system statement or proof because the repository record names
a framework and supplies no truth-valued proposition.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, network-triggering Lake operation, or other
`.lake` mutation was performed. The owned intake files and root worker packet make the final tree
dirty and nonrelease.

## Environment

- Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, target
  `x86_64-unknown-linux-gnu`.
- Lake `5.0.0-src+98dc76e`.
- Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package source status was clean before and after the
  probe.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Source boundary

Crossref metadata identifies Hamilton's 1834 *On a General Method in Dynamics*, DOI
`10.1098/rstl.1834.0017`, issue 124, pages 247-308. Semantic Scholar confirms the same title,
author, venue, DOI, and the Royal Society PDF location. Direct retrieval of the advertised PDF
returned HTTP 403, so no source text was preserved or inspected. The bibliography is a plausible
source-family lead only. The catalog does not cite it or choose a theorem, and no definition,
premise, conclusion, proof boundary, correction history, or independent source review was mapped.

The read-only `THM-M-1516` crosswalk distinguishes Hamilton's equations, Legendre correspondence,
energy conservation, and symplectic-flow preservation as inequivalent roots, and its legacy Lean
file records only an abstract interface plus an unpinned Physlib lead. Those observations reinforce
the ambiguity but belong to another target and supply no inherited source identity or proof credit.

## Commands and results

All repository commands ran at the repository root unless a different `cwd` is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1373` | 0 | rank 983; planned; no legacy slot; legacy artifacts unaccepted; theorem_complete false |
| `git status --short --untracked-files=all` (preflight) | 0 | only `?? Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD HEAD^{tree}` | 0 | base revision and tree shown above |
| `git blame -L 10006,10011 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog fields originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| Crossref and Semantic Scholar DOI metadata inspection | 0 | Hamilton 1834 title, author, venue, issue, pages, DOI, and advertised PDF located; Royal Society PDF retrieval returned HTTP 403, so metadata is discovery-only |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, x86_64 Linux |
| `(cd Formalizations/Lean && lake --version)` | 0 | Lake `5.0.0-src+98dc76e`; no update or build run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` and package status | 0 | pinned revision and tree recorded above; package source worktree clean |
| `sha256sum` on authoritative manifests, source records, toolchain, lock, three probed mathlib modules, and the read-only legacy candidate | 0 | hashes recorded in `instance.json` and the provisional receipt |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1373/IntakeProbe.lean)` | 0 | thirteen adjacent ODE, flow, derivative, matrix, and symplectic-group APIs elaborated; complete stdout SHA-256 `db22dedd6b2f69a558430227fcff6c08724f74f2df118497582370262c2834b7` |
| bounded exact-topic `rg` search in repo-local and pinned-mathlib Lean sources | 0 | located topic-adjacent legacy Hamiltonian artifacts but no exact declaration for the unidentified THM-M-1373 root; intake discovery only, not an exhaustive anchor audit |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, `intake-receipt.json`, and `.stage1-worker-selftest.json` | 0 | every structured artifact is valid JSON after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-1373-pycache python3 -m py_compile Stage1_Instances/THM-M-1373/check_intake.py` | 0 | scoped intake validator compiled without generated files under the owned path |
| `python3 -B Stage1_Instances/THM-M-1373/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target and authoritative-DAG identity, source/dependency hashes, H5/M4/R4 null-target boundary, exact inventory, packet agreement, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-1373/check_intake.py` | 0 | public replay mode passed without the scheduler-only worker packet |
| `sha256sum` on the root worker packet and eight non-receipt owned intake files | 0 | every nonrelease untracked input digest is recorded and replay-checked; the receipt output is excluded from its own raw digest |
| prohibited Lean construct scan over the owned path | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration in the API-only probe |
| per-file `git diff --no-index --check /dev/null` for every owned file and worker packet | 0 aggregate | no whitespace diagnostics; each no-index exit 1 was only the expected new-file difference |
| `git diff --check -- Stage1_Instances/THM-M-1373 .stage1-worker-selftest.json` | 0 | tracked-diff command emitted no diagnostics; per-file no-index checks cover all untracked files |

## Known open gates

Target redirection to one truth-valued proposition, exact source/result selection, complete
definition/premise/conclusion/proof-boundary crosswalk, correction or errata audit, lawful immutable
source admission, independent review, and `THM-M-1516` identity/root ownership remain open. So do
the canonical Lean target and minimal imports, expression/environment fingerprints, checked
transports, four statement mutation classes, exhaustive anchor audit, discovery protocol,
obligation registry, typed graphs, proof and composition, source/provenance/trust closure, readable
reconstruction, hermetic replay, deterministic bundle, independent verification, master
acceptance, audit completion, and theorem completion.

These failures prevent statement and theorem progress, but do not invalidate a truthful,
self-tested `planned` intake that classifies the received framework label as not yet a stable
proposition. This does not refute Hamiltonian mechanics or any correctly stated theorem.

## Status boundary

This is provisional worker self-test evidence for `S56-M-1373-INTAKE` only. It supports a planned
dossier, not an accepted node receipt. No canonical statement, H0 source closure, proof, audit
completion, theorem completion, or master acceptance is claimed.
