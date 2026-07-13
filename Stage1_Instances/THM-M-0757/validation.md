# Intake validation

Base revision: `d05520867fab3367a9b61b9544c3e12241204f54` (tree
`fb2cfc62077d5b53e9938632cd6361dd60872067`). Validation ran on 2026-07-13 in
the isolated worker clone.

Validation is limited to target-set consistency, dossier structure and scope invariants, catalog
provenance, bibliographic metadata discovery, pinned environment identity, a narrow Lean API probe,
a bounded local exact-topic search, proof-escape hygiene, JSON integrity, and whitespace. The
catalog wording is not a proposition, so elaborating a purported canonical target would invent
missing mathematics. `IntakeProbe.lean` checks only generic substrate and supplies no statement or
proof credit.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, or other `.lake` mutation was performed.
The owned intake artifacts and root worker handoff make this nonrelease worker evidence.

## Source boundary

Crossref metadata aligns two Gerald E. Sacks publications from 1966 with the catalog subject:

- *Metarecursively enumerable sets and admissible ordinals*, *Bulletin of the American
  Mathematical Society* 72(1), 59-64, DOI `10.1090/S0002-9904-1966-11416-7`;
- *Post's problem, admissible ordinals, and regularity*, *Transactions of the American
  Mathematical Society* 124(1), 1-23, DOI `10.1090/S0002-9947-1966-0201299-1`.

The observed Crossref response SHA-256 values were respectively
`ddedf298bef44ea5be2d2b1f60523f3ee53ce17641ee9beea1f8bce930ec8fa8` and
`325e8ff5c6478cf0232ed027b8b064805acbb4af22f72d3badacf5cd102d57dc`.
Direct AMS version-of-record access returned an automated-access response, so no primary theorem
passage or proof was admitted. The metadata fixes useful source leads, but maps the catalog gloss
to neither one as a canonical proposition and does not establish H0.

## Environment fingerprint

- Platform: Linux 7.0.0-27-generic, x86_64; worker timezone `Asia/Shanghai`.
- Lean: `4.29.0`, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Lake: `5.0.0-src+98dc76e`.
- Pinned mathlib: revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package worktree clean.
- `Formalizations/Lean/lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `Formalizations/Lean/lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Commands and results

| Command (repository root unless noted) | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0757` | 0 | rank 1343; planned; L0/rework_required; no legacy slot; legacy artifacts unaccepted; theorem_complete false |
| `git status --short --untracked-files=all` (preflight) | 0 | only pre-existing automation symlink `Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree shown above |
| `git blame -L 5577,5582 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `sed -n '5577,5582p' Docs/researches/math_theorems.md \| sha256sum` | 0 | exact catalog block SHA-256 `65df298407a658bce224e99524969adbf6697f3822185c5cb4fd9e34382100bc` |
| Crossref queries for both DOI values above | 0 | author, title, journal, volume, issue, pages, year, and DOI recorded as discovery metadata only |
| Direct AMS PDF/version-of-record requests | 22 | HTTP 403/429 automated-access responses; no full primary source, theorem locator, or H credit admitted |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | Lean and Lake agree with the fingerprint; no update or build was run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned revision and tree above; package worktree clean |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0757/IntakeProbe.lean)` | 0 | six generic ordinal, set-theoretic ordinal, and ordinary oracle-computability APIs elaborated; output SHA-256 `732bbb33471f15eafdaed61049140657b1852e1f56113ea1fec04a0791c9301a` |
| bounded exact-topic `rg` over repo-local Lean and pinned mathlib | 1 | expected no-match result for admissible ordinal, alpha-recursion, metarecursion, Kripke-Platek, constructible hierarchy, and Church-Kleene declarations; intake discovery only |
| `python3 -m json.tool` on all structured owned artifacts and `.stage1-worker-selftest.json` | 0 | instance, open task DAG, provisional receipt, and worker handoff are valid JSON |
| Python `ast.parse` on `Stage1_Instances/THM-M-0757/check_intake.py` | 0 | scoped validator parses without writing bytecode |
| `python3 -B Stage1_Instances/THM-M-0757/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | identity, planned H5/M4/R4 boundary, null target, pinned inputs, artifact hashes, handoff, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0757/check_intake.py` | 0 | public replay mode passes without the scheduler-only packet |
| prohibited Lean proof-escape scan over the owned path | 1 | expected no-match result; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration in the API-only probe |
| per-file no-index whitespace checks plus scoped `git diff --check` | 0 | no whitespace diagnostics in any changed file |

## Known downstream failures

- The catalog wording is not a stable proposition. No approved correction selects an admissibility
  definition, ordinal domain, alpha-recursion model, parameters, hypotheses, conclusion, or
  boundary cases.
- No independently reviewed immutable primary theorem, complete definition/assumption/proof/errata
  crosswalk, or exact theorem locator is accepted. The two 1966 records are discovery leads only.
- No canonical Lean expression, environment/expression fingerprint, exact minimal imports, checked
  alternate encoding, or statement mutation test exists.
- Discovery protocol, exhaustive anchor audit, obligation registry and typed graphs, proof,
  composition and trust checks, readable reconstruction, hermetic replay, deterministic evidence
  bundle, independent release verification, and master acceptance are open.
- Ordinary theorem-proof execution is blocked by `H5` until an approved correction supplies a
  stable proposition.

These failures prevent statement, audit, and theorem-completion claims. They do not invalidate a
truthful, self-tested `planned` intake whose purpose is to freeze the ambiguity boundary and open
DAG. Only the integration lane may accept the provisional worker receipt.
