# Intake validation

Base revision: `0d26adeae663d55eb536120f7d93ede975fe8f49`; base tree:
`6b5ab44050900e9a4a181b4fc56b1e965183f2c9`. Validation date: 2026-07-13
(Asia/Shanghai); exact start and end timestamps are recorded in the provisional receipt.

This validation covers target membership, the planned dossier and open task DAG, repository-source
provenance, source-family discrimination, JSON and scoped invariants, a narrow pinned Lean substrate
probe, bounded repository/mathlib search, prohibited-construct hygiene, and whitespace. It does not
validate a canonical Hopf statement or proof because the repository record supplies no
binder-complete proposition.

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

## Source discovery boundary

A zbMATH Open record identifies Hopf's article in volume 94, no. 1, pages 3-22, published 1943.
The inspected 20-page scan, SHA-256
`f34a1b081ead783d8026c0f2f737ac342ac2bf55a9c6f706e921971728c9072f`, says the work was presented
on 19 January 1942. Visual inspection of its opening pages located an analytic parameterized
differential-system setting, stationary branch, critical imaginary pair, crossing condition, and a
periodic-solution branch theorem. This plausibly explains the attribution and date but does not
constitute a complete transcription, translation, premise/proof-node map, correction audit,
repository-owned source packet, or independent H0 review.

Kuznetsov's reviewed Scholarpedia article was inspected to discriminate a modern smooth
finite-dimensional normal-form theorem: it makes transversality and a nonzero first Lyapunov
coefficient explicit and distinguishes stable supercritical and unstable subcritical cycles. Its
captured HTML has SHA-256
`d6905eb073975f9260c22ebfa72279c234703ad3a2447548859fb80e4fc69482`.

Kawanago's arXiv `2303.18000v3`, Theorem 2.1, was inspected as a different Banach-space contract.
Its PDF has SHA-256 `f999383e5358d9424080407302e23cac131ebb18ee978c4b378aba033684216b`.
It uses a closed operator, periodic Hoelder spaces, a `C^2` induced nonlinearity map, simple critical
eigenvalues, transversality, harmonic nonresonance, and a resolvent bound, then classifies nearby
periodic solutions modulo phase. No external source file was added to the repository. These facts
show that the terse catalog gloss is ambiguous; they do not select or prove its target.

## Commands and results

All repository commands ran at the repository root unless a different `cwd` is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1360` | 0 | rank 970; planned; no legacy slot; legacy artifacts unaccepted; theorem_complete false |
| `git status --short --untracked-files=all` (preflight) | 0 | only `?? Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD HEAD^{tree}` | 0 | base revision and tree shown above |
| `git blame -L 9915,9920 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog fields originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| temporary historical and modern source inspection | 0 | historical presentation/publication dates and three materially different theorem contracts recorded; no source admitted or H0 credited |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, x86_64 Linux |
| `(cd Formalizations/Lean && lake --version)` | 0 | Lake `5.0.0-src+98dc76e`; no update or build run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | pinned revision and tree recorded above; package status clean |
| `sha256sum` on the authoritative manifests, source records, toolchain, lock, and five probed mathlib modules | 0 | hashes recorded in `instance.json` and the provisional receipt |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1360/IntakeProbe.lean)` | 0 | nine adjacent periodicity, ODE, flow, differentiability, eigenvalue, and spectrum APIs elaborated; complete output SHA-256 `8d4b7217...fa280` |
| bounded case-insensitive exact-topic `rg` search in repo-local Lean and pinned mathlib | 1 (expected no match) | no Hopf/Andronov/bifurcation-periodic target; intake discovery only, not an exhaustive external anchor audit |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, `intake-receipt.json`, and `.stage1-worker-selftest.json` | 0 | every structured artifact is valid JSON after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-1360-pycache python3 -m py_compile Stage1_Instances/THM-M-1360/check_intake.py` | 0 | scoped validator compiled without generated files under the owned path |
| `python3 -B Stage1_Instances/THM-M-1360/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target and authoritative-DAG identity, source/dependency hashes, H1/M4/R4 null-target boundary, exact artifact inventory, packet agreement, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-1360/check_intake.py` | 0 | public replay mode passed without the scheduler-only worker packet |
| `sha256sum` on the root worker packet and the eight non-receipt owned intake files | 0 | every nonrelease untracked input digest is recorded and replay-checked by `intake-receipt.json`; the receipt is the output containing that map and is excluded from its own raw digest |
| prohibited Lean construct scan over the owned path | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration in the API-only probe |
| per-file `git diff --no-index --check /dev/null` for every owned file and worker packet | 0 aggregate | no whitespace diagnostics; each no-index exit 1 was only the expected new-file difference |
| `git diff --check -- Stage1_Instances/THM-M-1360 .stage1-worker-selftest.json` | 0 | tracked-diff command emitted no diagnostics; the preceding no-index checks cover all untracked files |

## Known open gates

Exact source and result selection, complete definition/premise/conclusion/proof-boundary and
translation crosswalk, 1942/1943 provenance reconciliation, correction or errata audit, immutable
source admission, and independent review remain open. So do the canonical Lean target and minimal
imports, expression/environment fingerprints, checked transports, four statement mutation classes,
exhaustive anchor audit, discovery protocol, obligation registry, typed graphs, proof and
composition, source/provenance/trust closure, readable reconstruction, hermetic replay,
deterministic bundle, independent verification, master acceptance, audit completion, and theorem
completion. These failures prevent statement and theorem progress, but do not invalidate a truthful
self-tested `planned` intake.

## Status boundary

This is provisional worker self-test evidence for `S56-M-1360-INTAKE` only. It supports a planned
dossier, not an accepted node receipt. No canonical statement, H0 source closure, proof, audit
completion, theorem completion, or master acceptance is claimed.
