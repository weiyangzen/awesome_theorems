# Intake validation

Base revision: `d502dd6f3d278ca9cb0ead8cbdc5f16c0e1fd8c9`; base tree:
`829a47c47ae831cada4f8acc6c2c00ba5883215e`. Validation date: 2026-07-13
(Asia/Shanghai); exact start and end timestamps are recorded in the provisional receipt.

This validation covers target membership, the planned dossier and open task DAG, repository-source
provenance, source/variant and duplicate-scope discrimination, JSON and scoped invariants, a narrow
pinned Lean substrate probe, bounded repository/mathlib search, prohibited-construct hygiene, and
whitespace. It does not validate a canonical Hasse-Minkowski statement or proof because the catalog
does not supply a binder-complete proposition.

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

Crossref metadata confirmed Hasse's 1924 number-field article, issue 153, pages 113-130, DOI
`10.1515/crll.1924.153.113`, and Minkowski's 1890 rational-form-equivalence article, issue 106,
pages 5-26, DOI `10.1515/crll.1890.106.5`. The publisher challenged full-text access, so no
primary text was admitted or inspected and no exact theorem or premise mapping is claimed. The
bibliographic records distinguish plausible historical contracts only.

The repo-local `THM-M-0423` dossier selects a candidate coordinate-free quadratic
Hasse-Minkowski root for the broader Hasse-principle catalog item. Its statement and legacy shared
source explicitly withhold the hard proof. This exposes a semantic-overlap decision for later
review; it does not transfer statement, evidence, or proof credit into `THM-M-0020`.

## Commands and results

All repository commands ran at the repository root unless a different `cwd` is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0020` | 0 | rank 1014; planned; no legacy slot; legacy artifacts unaccepted; theorem_complete false |
| `git status --short --untracked-files=all` (preflight) | 0 | only `?? Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD HEAD^{tree}` | 0 | base revision and tree shown above |
| `git blame -L 163,168 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog fields originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| Crossref metadata requests for the two recorded DOIs | 0 | Hasse and Minkowski bibliographic leads confirmed; no source admitted or H0 credited |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, x86_64 Linux |
| `(cd Formalizations/Lean && lake --version)` | 0 | Lake `5.0.0-src+98dc76e`; no update or build run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | pinned revision and tree recorded above; package status clean |
| `sha256sum` on authoritative manifests, source records, toolchain, lock, related discovery files, and five probed mathlib modules | 0 | hashes recorded in `instance.json` and the provisional receipt |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0020/IntakeProbe.lean)` | 0 | nine adjacent quadratic-form and number-field-place APIs elaborated; complete output SHA-256 `6662c14e...74ce0` |
| bounded exact-topic `rg` search in pinned mathlib | 1 (expected no match) | no Hasse-Minkowski name match; intake discovery only, not an exhaustive external anchor audit |
| bounded exact-topic `rg` search in repo-local Lean and `THM-M-0423` | 0 | related statement/substrate occurrences found only in foreign discovery surfaces; they explicitly withhold terminal closure |
| `python3 -m json.tool` on owned JSON files and `.stage1-worker-selftest.json` | 0 | every structured artifact is valid JSON after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0020-pycache python3 -m py_compile Stage1_Instances/THM-M-0020/check_intake.py` | 0 | scoped validator compiled without generated files under the owned path |
| `python3 -B Stage1_Instances/THM-M-0020/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target/DAG identity, source/dependency hashes, H1/M4/R4 null-target boundary, exact inventory, packet agreement, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0020/check_intake.py` | 0 | public replay mode passed without the scheduler-only worker packet |
| `sha256sum` on the root worker packet and eight non-receipt owned intake files | 0 | nonrelease input digests recorded and replay-checked; the receipt output is excluded from its own digest map |
| prohibited Lean construct scan over the owned path | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration in the API-only probe |
| per-file `git diff --no-index --check /dev/null` for every owned file and worker packet | 0 aggregate | no whitespace diagnostics; each no-index exit 1 was only the expected new-file difference |
| `git diff --check -- Stage1_Instances/THM-M-0020 .stage1-worker-selftest.json` | 0 | tracked-diff command emitted no diagnostics; per-file no-index checks cover all untracked files |

## Known open gates

Exact source and theorem selection, complete definition/premise/conclusion/proof-boundary and
translation crosswalk, Hasse/Minkowski formulation reconciliation, correction or errata audit,
immutable source admission, independent source review, and duplicate/scope resolution with
`THM-M-0423` remain open. So do the canonical Lean target and minimal imports,
expression/environment fingerprints, checked transports, four mutation classes, exhaustive anchor
audit, discovery protocol, obligation registry, typed graphs, proof and composition,
source/provenance/trust closure, readable reconstruction, hermetic replay, deterministic bundle,
independent verification, master acceptance, audit completion, and theorem completion. These
failures prevent statement and theorem progress but do not invalidate a truthful self-tested
`planned` intake.

## Status boundary

This is provisional worker self-test evidence for `S56-M-0020-INTAKE` only. It supports a planned
dossier, not an accepted node receipt. No canonical statement, H0 source closure, proof, audit
completion, theorem completion, or master acceptance is claimed.
