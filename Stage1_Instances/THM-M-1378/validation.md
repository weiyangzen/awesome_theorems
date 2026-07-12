# Intake validation

Base revision: `d502dd6f3d278ca9cb0ead8cbdc5f16c0e1fd8c9` (tree
`829a47c47ae831cada4f8acc6c2c00ba5883215e`). Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers the planned dossier, source and neighboring-target boundaries, open task
DAG, JSON and scoped invariants, and a narrow pinned Lean API probe. It does not validate a
canonical Euler-Lagrange statement or proof because neither is frozen. The automation-provided
canonical `.lake` symlink was present before this work and used read-only; no update, build, clone,
fetch, or other dependency mutation was performed. This dirty worker run is nonrelease evidence.

## Environment

- Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, target
  `x86_64-unknown-linux-gnu`.
- Lake `5.0.0-src+98dc76e`.
- Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package source status was clean.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Commands and results

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; all 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1378` | exit 0; rank 988, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all` | preflight exit 0; only the automation-provided untracked `Formalizations/Lean/.lake` symlink existed before this intake |
| `git blame -L 10041,10046 -- Docs/researches/math_theorems.md` | exit 0; every catalog line originates at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | exit 0; tool versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | exit 0; pinned revision and tree recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | exit 0; empty output |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | exit 0; hashes recorded above |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1378/IntakeProbe.lean)` | exit 0; eight adjacent extremum, interval integration-by-parts, and line-derivative APIs elaborated; no target theorem was declared |
| exact-topic `rg` search in pinned mathlib | exit 1, expected no match; no terminal declaration matching Euler-Lagrange, calculus of variations, stationary action, or first variation; bounded intake discovery only |
| exact-topic `rg` search in repo-local Lean | exit 0; hits are unrelated fields, legacy boundaries, special cases, and source/anchor metadata; none receives target proof credit |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, `intake-receipt.json`, and the root worker packet | exit 0 for each after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-1378-pycache python3 -m py_compile Stage1_Instances/THM-M-1378/check_intake.py` | exit 0; the scoped validator compiled without adding generated files to the owned path |
| `python3 -B Stage1_Instances/THM-M-1378/check_intake.py --worker-packet .stage1-worker-selftest.json` | exit 0; target identity, planned lifecycle, H5/M4/R4 boundary, null target, source and neighbor boundaries, pins, exact artifact inventory, worker packet, and six open tasks agree |
| prohibited Lean construct scan over the owned path | exit 1, expected no match; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| scoped new-file whitespace checks plus `git diff --check` | exit 0; no whitespace errors |

The provisional receipt binds every non-self-referential owned artifact and the root worker packet
by SHA-256, records sorted-path dirty patch and manifest hashes, and binds both structured recipe
identities, input manifests, stdout, and logs. The receipt excludes its own digest to avoid
self-reference and remains unsigned, non-content-addressed, nonrelease evidence pending master
recapture and acceptance.

## Known open gates

The catalog still lacks one stable proposition and an accepted immutable source. Exact functional,
domains, admissible variations, extremum or stationarity premise, regularity, endpoint policy,
conclusion, conventions, primary-source pinpoint, full assumption/errata mapping, and independent
review remain open. So do the canonical Lean expression and environment fingerprints, checked
transports, statement mutations, exhaustive anchor audit, discovery protocol, obligation registry,
typed graphs, proof and composition, trust and provenance closure, readable reconstruction,
hermetic replay, deterministic bundle, independent verification, master acceptance, audit
completion, and theorem completion. Those failures do not invalidate a truthful, self-tested
`planned` intake.
