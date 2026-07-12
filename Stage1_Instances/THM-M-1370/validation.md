# Intake validation

Base revision: `d502dd6f3d278ca9cb0ead8cbdc5f16c0e1fd8c9`; base tree:
`829a47c47ae831cada4f8acc6c2c00ba5883215e`. Validation date: 2026-07-13
(Asia/Shanghai); exact start and end timestamps are recorded in the provisional receipt.

This validation covers target membership, the planned dossier and open task DAG, repository-source
provenance, source-family and name disambiguation, JSON and scoped invariants, a narrow pinned Lean
substrate probe, bounded repository/mathlib search, prohibited-construct hygiene, and whitespace.
It does not validate a canonical KAM statement or proof because the repository record supplies no
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

The catalog record and its Stage0 projection were inspected at their pinned repository revision.
They identify a 1954 original-KAM family but no exact statement. Crossref metadata was inspected for
Kolmogorov's later English reprint, DOI `10.1007/BFb0021737`, and Arnold's 1963 proof article, DOI
`10.1070/RM1963v018n05ABEH004130`. The metadata confirms stable bibliographic leads and exposes
author/date/translation distinctions; it is not a complete primary-source statement audit.

No external source file was added to the repository. No exact edition, theorem passage, assumption
map, proof boundary, translation, correction record, or independent review was accepted. The
English-name conflict with the Kolmogorov-Arnold representation theorem is frozen as an exclusion,
not resolved by substituting that unrelated result.

## Commands and results

All repository commands ran at the repository root unless a different `cwd` is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1370` | 0 | rank 980; planned; no legacy slot; legacy artifacts unaccepted; theorem_complete false |
| `git status --short --untracked-files=all` (preflight) | 0 | only `?? Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree shown above |
| `git blame -L 9985,9990 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog fields originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| Crossref metadata inspection for the Kolmogorov reprint and Arnold proof article | 0 | 1954 original-result and 1963 proof locators recorded; metadata conflict and source-admission boundary preserved; no H0 credited |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, x86_64 Linux |
| `(cd Formalizations/Lean && lake --version)` | 0 | Lake `5.0.0-src+98dc76e`; no update or build run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | pinned revision and tree recorded above; package status clean |
| `sha256sum` on authoritative manifests, source records, toolchain, lock, legacy boundary, and five probed mathlib modules | 0 | hashes recorded in `instance.json` and the provisional receipt |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1370/IntakeProbe.lean)` | 0 | eight adjacent analytic, finite-torus Fourier, ODE, flow, and symplectic APIs elaborated; complete output SHA-256 `efb40640e4ca9ee7f389ed503e5b8711fadcd2571ae65370497c1bebfefab79f`; no target declaration or proof body |
| bounded case-insensitive exact-topic `rg` search in repo-local Lean and pinned mathlib | 1 (expected no match) | no KAM or Hamiltonian quasi-periodic persistence target; intake discovery only, not an exhaustive external anchor audit |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, `intake-receipt.json`, and `.stage1-worker-selftest.json` | 0 | every structured artifact is valid JSON after finalization |
| `python3 -c` with `ast.parse` on `Stage1_Instances/THM-M-1370/check_intake.py` | 0 | scoped validator parsed without writing bytecode |
| `python3 -B Stage1_Instances/THM-M-1370/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target/DAG identity, source and dependency hashes, H1/M4/R4 null target, exact inventory, packet agreement, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-1370/check_intake.py` | 0 | public replay mode passes without the scheduler-only worker packet |
| `sha256sum` on the root worker packet and eight non-receipt owned intake files | 0 | raw nonrelease input digests recorded and replay-checked by the receipt; the receipt output is excluded from its own digest map |
| prohibited Lean construct scan over the owned path | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration in the API-only probe |
| per-file `git diff --no-index --check /dev/null` for every owned file and worker packet | 0 aggregate | no whitespace diagnostics; each no-index exit 1 was only the expected new-file difference |
| `git diff --check -- Stage1_Instances/THM-M-1370 .stage1-worker-selftest.json` | 0 | no tracked whitespace diagnostics; per-file no-index checks cover all untracked artifacts |

## Known open gates

Exact source edition and result selection, complete definition/premise/conclusion/proof-boundary
and translation crosswalk, 1954/1963 attribution reconciliation, correction or errata audit,
immutable source admission, and independent review remain open. So do the canonical Lean target and
minimal imports, expression/environment fingerprints, checked transports, four statement mutation
classes, exhaustive anchor audit, discovery protocol, obligation registry, typed graphs, proof and
composition, source/provenance/trust closure, readable reconstruction, hermetic replay,
deterministic bundle, independent verification, master acceptance, audit completion, and theorem
completion. These failures prevent statement and theorem progress, but do not invalidate a truthful
self-tested `planned` intake.

## Status boundary

This is provisional worker self-test evidence for `S56-M-1370-INTAKE` only. It supports a planned
dossier, not an accepted node receipt. No canonical statement, H0 source closure, proof, audit
completion, theorem completion, or master acceptance is claimed.
