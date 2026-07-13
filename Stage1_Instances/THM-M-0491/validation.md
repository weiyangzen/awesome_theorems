# Intake validation

Base revision: `997541734bb32f987fb15f163335a82512992120`; base tree:
`2c866b9d840d48c48ac839740c62d3b9440be0e5`. Validation date: 2026-07-13
(`Asia/Shanghai`).

This validation covers target membership, the planned dossier and open task DAG, repository-source
provenance, the primary-source family and non-substitution boundary, structured intake invariants,
a narrow pinned Lean substrate probe, bounded local discovery, prohibited-construct hygiene, and
whitespace. It does not validate a canonical Maynard proposition or proof because the catalog does
not select one. Recorded replay recipes deny network; this inherited worker run did not independently
enforce network isolation and is nonhermetic evidence.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, or other `.lake` mutation was performed.
Owned intake files and the root worker packet make the final tree dirty and nonrelease.

## Source discovery boundary

The official journal page and PDF for James Maynard's *Small gaps between primes*, *Annals of
Mathematics* 181 (2015), issue 1, pages 383-413, DOI
`10.4007/annals.2015.181.1.7`, were inspected as temporary discovery inputs. The observed journal
PDF was 528,115 bytes with SHA-256
`3c24d010f00d1212418351b6f6baed9c94251a3ce958c36f56ebbc450ade9349`.
The observed arXiv v1 and v3 source archives had SHA-256 values
`f22c7cf10b89d3b97d521f98da460c0519743eae6b6c2a92797d862e23218067` and
`b9b9113d1fa1abb4781d1b4b93b3da80c01a10fbee1166ddc654f003c900a2df`.

The paper contains four distinct headline results and a separate sieve engine, so it disambiguates
the theorem family but not the catalog's exact root. Mutable external copies were not added to the
repository and are not an immutable H0 packet. Complete definition, premise, proof-boundary,
revision and correction mapping, source admission, and independent review remain open.

## Environment

- Linux `7.0.0-27-generic`, `x86_64`; timezone `Asia/Shanghai`.
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

All repository commands ran at the repository root unless the command shows another working
directory.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | all 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0491` | 0 | rank 1368; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all` (preflight) | 0 | only `?? Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD HEAD^{tree}` | 0 | base revision and tree recorded above |
| `git blame -L 3602,3607 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| inspect official journal metadata/PDF and arXiv v1/v3 source archives | 0 | Theorems 1.1-1.4 and Propositions 4.2-4.3 located; bytes and digests recorded above; discovery only |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | Lean and Lake versions recorded above; no dependency-mutating operation run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | pinned revision and tree recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | empty output |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | pinned hashes recorded above |
| bounded exact-topic `rg` over repository-local Lean and pinned mathlib | expected no target match | no Maynard, small/bounded prime-gap, or matching nth-prime liminf declaration; the lone Maynard mention is unrelated Duffin-Schaeffer prose |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0491/IntakeProbe.lean)` | 0 | thirteen adjacent API checks elaborated; stdout 1,129 bytes, SHA-256 `61b4b48e82bae21d353b19091fd02a89070efcd802ca70643d13940aac2a244e`; no target theorem declared |
| `python3 -m json.tool` on the three owned JSON files and root worker packet | 0 | all structured artifacts are valid JSON after finalization |
| `PYTHONPYCACHEPREFIX=<temporary-cache> python3 -m py_compile Stage1_Instances/THM-M-0491/check_intake.py` | 0 | scoped validator compiled without adding generated files to the owned path |
| `python3 -B Stage1_Instances/THM-M-0491/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | manifest/DAG identity, source and dependency pins, null target, H1/M4/R4 boundary, exact artifact inventory, packet agreement, replay hashes, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0491/check_intake.py` | 0 | public replay mode passed without the scheduler-only packet |
| `rg -n '\b(sorry\|admit\|sorryAx\|axiom\|constant\|opaque\|unsafe)\b' Stage1_Instances/THM-M-0491 --glob '*.lean'` | 1 (expected no match) | no prohibited declaration or proof escape in the discovery-only probe |
| per-file `git diff --no-index --check /dev/null` for every owned file and the worker packet | 0 aggregate | no whitespace diagnostics; raw no-index exit 1 per new file means only that content differs from `/dev/null` |
| `git diff --check -- Stage1_Instances/THM-M-0491 .stage1-worker-selftest.json` | 0 | no tracked-diff diagnostics; the preceding no-index checks cover untracked files |

## Status boundary

This is provisional worker self-test evidence for `S56-M-0491-INTAKE` only. It supports a truthful
`planned` dossier, not an accepted node receipt. Exact source-result selection and independent
review, canonical Lean elaboration and statement mutations, exhaustive anchor audit and discovery
freeze, obligation registry, typed graphs, proof, composition, trust closure, readable
reconstruction, hermetic replay, deterministic release bundle, and independent verification remain
open. These failures block statement, audit completion, and theorem completion, but do not
invalidate the self-tested planned intake.
