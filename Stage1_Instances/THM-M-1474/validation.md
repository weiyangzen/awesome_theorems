# THM-M-1474 intake validation

## Scope

This record validates only the `planned` dossier, scope map, source-statement crosswalk, open task
DAG, source-family observation metadata, and discovery-only pinned Lean API probe. It does not
validate an exact mathematical statement, a finite-difference scheme, a von Neumann stability
criterion, a proof, an accepted receipt, audit completion, or theorem completion.

The worker tree was nonrelease-dirty throughout: the canonical `.lake` link was already untracked,
and this intake's owned artifacts plus the root self-test packet were new. No dependency content,
authority file, or other target path was modified.

## Environment

- Repository base: `f4efdfc7c685252a98f3508a5974ba81c0377a95`
- Base tree: `94a9cfc613f86042a21fdfa174ba887334b93893`
- Lean: `4.29.0`, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`
- Lake: `5.0.0-src+98dc76e`
- mathlib: `8a178386ffc0f5fef0b77738bb5449d50efeea95`
- Platform: Linux `7.0.0-27-generic`, `x86_64`
- Timezone/date: Asia/Shanghai, 2026-07-13

The LeVeque source-family metadata was observed with bounded HTTP requests. The Crossref response,
author companion page, six-page table of contents, and errata had SHA-256 values
`00a5226fb3fa729407dcce209cb296e05789ebe6a014ebc521a6182db952edca`,
`b21cc480d36d39b6b61f29d7cf5ac5d0a86ed4715f2994da862a427ec833227f`,
`e7d8159d30a80e90fa3118f0f7b5b26aad00f4410b45eb131f93ce4ef140d16b`, and
`1f3623cc98ed7c970ed920406f0c05cd4e519654307d9fc76ff3e62b94f903eb`,
respectively. No external source was vendored; these are nonrelease observations.

## Commands and results

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1474` | 0 | rank 1151, planned, L0/rework_required, no legacy slot, theorem_complete false |
| `git status --short --untracked-files=all` at preflight | 0 | only the pre-existing untracked canonical `.lake` link existed before this intake; preserved |
| `git blame -L 10756,10761 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate in commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| bounded observation of Crossref and author-hosted LeVeque companion, contents, and errata | 0 | distinct parabolic Section 9.6 and hyperbolic Section 10.5 von Neumann-analysis roots located; source-family lead only |
| bounded exact-topic `rg` over pinned mathlib and repo-local Lean | 0/1 by query | no source-selected finite-difference stability declaration located; unrelated von Neumann topics and adjacent Fourier/spectrum APIs identified; not an absence proof |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1474/IntakeProbe.lean` | 0 | four adjacent pinned APIs elaborated; two axiom reports contain only `propext`, `Classical.choice`, and `Quot.sound`; no target theorem introduced |
| `python3 -m json.tool` on the three owned JSON files and `.stage1-worker-selftest.json` | 0 | all structured artifacts are valid JSON |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-1474-pycache python3 -m py_compile Stage1_Instances/THM-M-1474/check_intake.py` | 0 | scoped validator parses without writing cache files under the owned path |
| `python3 -B Stage1_Instances/THM-M-1474/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target/item identity, null target, H5/M4/R4 boundary, source and pin hashes, receipt/packet agreement, exact inventory, and six open tasks agree |
| prohibited-construct `rg` over `IntakeProbe.lean` | 1 expected | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` token |
| `git diff --check -- Stage1_Instances/THM-M-1474 .stage1-worker-selftest.json` plus per-new-file no-index whitespace checks | 0 | no whitespace diagnostics |

The final structural and whitespace results are recorded after receipt and worker-packet creation.
The Lean probe's exact stdout SHA-256 is
`85d5cdd84664ff053dd14e8f1afe7d72fd5e6f5694ea82ea5e194a07de423086`.

## Known failures and boundary

Master acceptance is pending. The catalog label still lacks a selected exact proposition. Source
admission, independent source/numerical-stability review, formal target and mutation certificate,
exhaustive anchor audit, obligation registry, typed graphs, proof, composition, trust closure,
readable reconstruction, hermetic replay, deterministic bundle, and independent verification
remain open.

Verdict: `no_state_change`. This self-tested worker proposal may be handed off as `[_]`; it
remains unfinished and unaccepted. `audit_complete=false` and `theorem_complete=false`.
