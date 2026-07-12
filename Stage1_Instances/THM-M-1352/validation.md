# Intake validation

Base revision: `122f443c54e4e81d1bf325b07e18ba095823da6d`; base tree:
`2629bb0cacebd896715a9abad7c52ad60e7bccd0`. Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers target membership, the planned dossier and open task DAG, repository-source
provenance, source-family discrimination, JSON and scoped invariants, a narrow pinned Lean substrate
probe, bounded repository/mathlib search, prohibited-construct hygiene, and whitespace. It does not
validate a canonical Floquet statement or proof because the repository record supplies no stable
truth-valued proposition.

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

Crossref metadata for DOI `10.24033/asens.220` confirms Floquet's 1883 article title, journal,
volume, and pages 47-88. This is a historical source-family lead, but the catalog does not cite the
article or a theorem/page passage.

The author-hosted publisher-permitted preliminary edition of Gerald Teschl's *Ordinary
Differential Equations and Dynamical Systems* was inspected as a temporary worker input. Section
3.6, printed pages 91-93, separates Lemma 3.14, Theorem 3.15, and Corollaries 3.16-3.18: principal
matrix shift periodicity, Floquet decomposition, a real doubled-period form, multipliers and
exponents, stability, and reduction to constant coefficients. The PDF has SHA-256
`362433156525216abf596c17ce843204510e96d57afa4284a37c7aa5a9ffc36e` and size 4,133,331
bytes. `pdftotext -f 102 -l 104 -layout` extracted exactly those three printed pages to a temporary
file with SHA-256 `4c786c2321885d6f6fb501e1552e716c8392a3dbe4bbf39b65b0086b0f4c794b`.
No source file was added to the repository. These facts discriminate the theory family but do not
select the catalog target, establish an immutable H0 packet, or supply complete assumption,
proof-boundary, translation, errata, or independent-review closure.

## Commands and results

All repository commands ran at the repository root unless a different `cwd` is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1352` | 0 | rank 962; planned; no legacy slot; legacy artifacts unaccepted; theorem_complete false |
| `git status --short --untracked-files=all` (preflight) | 0 | only `?? Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD HEAD^{tree}` | 0 | base revision and tree shown above |
| `git blame -L 9859,9864 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog fields originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| Crossref API query for DOI `10.24033/asens.220` | 0 | article-level metadata confirmed; response SHA-256 `4cdd27ac2d8f156735eb0fe0932873d57d0cc9dfbc1a6d483a38d80b57b16bee` |
| `pdftotext -f 102 -l 104 -layout <temporary-source-pdf> <temporary-extract>` | 0 | extracted exactly printed pages 91-93; SHA-256 `4c786c23...c794b`; no source admitted to the repository |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, x86_64 Linux |
| `(cd Formalizations/Lean && lake --version)` | 0 | Lake `5.0.0-src+98dc76e`; no update or build run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | pinned revision and tree recorded above |
| `sha256sum` on the authoritative manifests, source records, toolchain, lock, and three probed mathlib modules | 0 | hashes recorded in `instance.json` and the provisional receipt |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1352/IntakeProbe.lean)` | 0 | eight adjacent periodicity, ODE, matrix, determinant, and exponential APIs elaborated; complete output SHA-256 `9643a367...8727` |
| bounded case-insensitive exact-topic `rg` search in repo-local Lean and pinned mathlib | 1 (expected no match) | no Floquet, periodic-linear-system, monodromy-matrix, principal-matrix, or characteristic-exponent target; intake discovery only |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, `intake-receipt.json`, and `.stage1-worker-selftest.json` | 0 | every structured artifact is valid JSON after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-1352-pycache python3 -m py_compile Stage1_Instances/THM-M-1352/check_intake.py` | 0 | scoped validator compiled without generated files under the owned path |
| `python3 -B Stage1_Instances/THM-M-1352/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target and DAG identity, source/dependency hashes, H5/M4/R4 null-target boundary, exact artifact inventory, packet agreement, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-1352/check_intake.py` | 0 | public replay mode passed without the scheduler-only worker packet |
| prohibited Lean construct scan over the owned path | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration in the API-only probe |
| per-file `git diff --no-index --check /dev/null` for every owned file and worker packet | 0 aggregate | no whitespace diagnostics; each no-index exit 1 was only the expected new-file difference |
| `git diff --check -- Stage1_Instances/THM-M-1352 .stage1-worker-selftest.json` | 0 | tracked-diff command emitted no diagnostics; the preceding no-index checks cover all untracked files |

## Known open gates

Exact source and numbered-result selection, complete definition/premise/conclusion/proof-boundary
crosswalk, neighboring target ownership, translation and errata audit, immutable source admission,
and independent review remain open. So do the canonical Lean target and minimal imports,
expression/environment fingerprints, checked transports, four statement mutation classes,
exhaustive anchor audit, discovery protocol, obligation registry, typed graphs, proof and
composition, source/provenance/trust closure, readable reconstruction, hermetic replay,
deterministic bundle, independent verification, master acceptance, audit completion, and theorem
completion. These failures prevent statement and theorem progress, but they do not invalidate a
truthful self-tested `planned` intake.

## Status boundary

This is provisional worker self-test evidence for `S56-M-1352-INTAKE` only. It supports a planned
dossier, not an accepted node receipt. H5 applies to the underspecified catalog wording, not to a
reviewed Floquet theorem. No canonical statement, source closure, proof, audit completion, theorem
completion, or master acceptance is claimed.
