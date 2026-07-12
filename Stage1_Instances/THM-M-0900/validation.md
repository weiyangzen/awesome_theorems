# Intake validation

Base revision: `d502dd6f3d278ca9cb0ead8cbdc5f16c0e1fd8c9`; base tree:
`829a47c47ae831cada4f8acc6c2c00ba5883215e`. Validation date: 2026-07-13
(Asia/Shanghai). No exact or release-grade timing evidence is claimed.

This validation covers target membership, the planned dossier and open task DAG, literal repository
provenance, source-identity discrimination, JSON and scoped invariants, a narrow pinned Lean
substrate probe, bounded repository/mathlib and bibliographic discovery, prohibited-construct
hygiene, and whitespace. It does not validate a canonical design-existence statement or proof
because the catalog identity and binder-complete proposition are unresolved.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, or other `.lake` mutation was performed.
The owned intake files and root worker packet make the final tree dirty and nonrelease.

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

## Source discovery boundary

The repository record contains no bibliography and all six fields originate in commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. Repository-wide exact search found no other source for
`Keighery`. Bounded arXiv, Crossref, DBLP, Semantic Scholar, and web searches found no
design-theory theorem or mathematician by that name; the result is a bounded no-match, not a claim
of global nonexistence.

Peter Keevash's *The existence of designs*, arXiv `1401.3665v4`, was inspected as a spelling and
subject lead. Its PDF SHA-256 is
`892d8b968c3e56e588297fdc72ef67e36efe9a32173228412b310de63d00eccf`. The introduction defines
`(n,q,r,lambda)` designs, states the natural binomial divisibility conditions, and describes their
sufficiency apart from finitely many `n` for fixed parameters. It distinguishes Wilson's `r = 2`
result and the Erdos-Hanani/Rodl approximate result. Version 4 also acknowledges errors in early
versions. These facts make catalog corruption plausible but do not prove that `Keighery`
means `Keevash`, select the exact corollary, or clear source review. No external source file was
added to the repository and no H0 credit is claimed.

## Commands and results

All repository commands ran at the repository root unless a different `cwd` is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0900` | 0 | rank 1042; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all` (preflight) | 0 | only `?? Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD HEAD^{tree}` | 0 | base revision and tree shown above |
| `git blame -L 6586,6591 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog fields originate at the repository source-record commit |
| bounded repository and bibliographic identity search | expected no-match or successful empty result | no mathematical `Keighery` identity found; Keevash recorded only as an uncredited lead |
| temporary arXiv v4 PDF inspection with `pdfinfo` and `pdftotext` | 0 | exact design definition, divisibility family, fixed-parameter asymptotic claim, Wilson/Rodl boundary, and correction-history warning recorded; no source admitted |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0 and pinned commit/target above |
| `(cd Formalizations/Lean && lake --version)` | 0 | Lake `5.0.0-src+98dc76e`; no update or build run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | pinned revision and tree recorded above; package status clean |
| `sha256sum` on authoritative manifests, source records, toolchain, lock, and probed mathlib module | 0 | hashes recorded in `instance.json` and the provisional receipt |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0900/IntakeProbe.lean)` | 0 | five adjacent finite-set/binomial APIs elaborated; complete output SHA-256 `2514bbeb...0a797d` |
| bounded exact-topic `rg` search in repo-local Lean and pinned mathlib | expected no match | no Keighery, Keevash, Steiner-system, block-design, or `t`-design target; intake discovery only |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, `intake-receipt.json`, and `.stage1-worker-selftest.json` | 0 | every structured artifact is valid JSON after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0900-pycache python3 -m py_compile Stage1_Instances/THM-M-0900/check_intake.py` | 0 | scoped validator compiled without generated files under the owned path |
| `python3 -B Stage1_Instances/THM-M-0900/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target and authoritative-DAG identity, source/dependency hashes, H5/M4/R4 null-target boundary, exact artifact inventory, packet agreement, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0900/check_intake.py` | 0 | public replay mode passed without the scheduler-only worker packet |
| prohibited Lean construct scan over the owned path | expected no match | no proof escape, bodyless declaration, or unsafe declaration in the API-only probe |
| per-file `git diff --no-index --check /dev/null` for every owned file and worker packet | 0 aggregate | no whitespace diagnostics; each no-index exit 1 was only the expected new-file difference |
| `git diff --check -- Stage1_Instances/THM-M-0900 .stage1-worker-selftest.json` | 0 | no tracked whitespace diagnostics; the no-index checks cover every untracked artifact |

## Known open gates

Catalog identity correction, an immutable authoritative source, exact result or corollary selection,
name/attribution/date reconciliation, complete design/parameter/divisibility/threshold/conclusion and
proof-boundary mapping, early-version error and correction-history review, and independent source
approval remain
open. So do the canonical Lean target and minimal imports, expression/environment fingerprints,
checked transports, four statement mutation classes, exhaustive anchor audit, discovery protocol,
obligation registry, typed graphs, proof and composition, source/provenance/trust closure, readable
reconstruction, hermetic replay, deterministic bundle, independent verification, master acceptance,
audit completion, and theorem completion.

These failures block ordinary statement and theorem execution but do not invalidate a truthful
self-tested planned intake. The `H5` classification applies only to the unstable catalog record, not
to Keevash's, Wilson's, Rodl's, or any other well-defined theorem.

## Status boundary

This is provisional worker self-test evidence for `S56-M-0900-INTAKE` only. It supports a planned
dossier and concrete correction blocker, not an accepted node receipt. No canonical statement,
H0 source closure, proof, audit completion, theorem completion, or master acceptance is claimed.
