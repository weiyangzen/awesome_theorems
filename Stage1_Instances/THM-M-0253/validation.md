# Intake validation

Base revision: `c6fd6dad8fcfe5fd464416cd452f50286b546978` (tree
`5a80b61d8fa09336779f8d1453dcfe4299c9472f`). Validation ran on 2026-07-13 in
the isolated worker clone, timezone `Asia/Shanghai`.

Validation is limited to target-set consistency, dossier structure and scope invariants, source
provenance, bibliographic-identity discovery, pinned environment identity, a narrow Lean API probe,
a bounded local name search, JSON integrity, proof-escape hygiene, and whitespace. It does not
elaborate an invented canonical statement or inspect proof closure.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. It was used read-only. No `lake
update`, `lake build`, dependency clone/fetch, or other `.lake` mutation was performed. This is
nonrelease worker evidence.

## Environment fingerprint

- Platform: Linux x86_64.
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
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok`; 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0253` | 0 | rank 1263, planned, L0/rework-required, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all` (preflight) | 0 | only pre-existing automation symlink `Formalizations/Lean/.lake`; preserved read-only |
| `git blame -L 1822,1827 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `sed -n '1822,1827p' Docs/researches/math_theorems.md \| sha256sum` | 0 | exact catalog block SHA-256 `1542dfdb9dfbd4bf12659f1c3bfe27abddadfe97522b121730550307615926f5` |
| Crossref and zbMATH queries for DOI `10.2307/2372840` | 0 | Carleson, 1958, *An Interpolation Problem for Bounded Analytic Functions*, American Journal of Mathematics 80(4), pages 921-930; metadata only |
| OpenAlex and Unpaywall queries for that DOI | 0 | closed access, no open repository copy or PDF; no theorem text credited |
| JSTOR landing and PDF requests | 0 | HTTP 420 error pages, not article content; primary theorem remained uninspected |
| Dayan, `arXiv:1912.03765v1`, pages 1 and 15 | 0 | inspected secondary restatement separates the 1958 `H^infinity` product criterion from a measure formulation; source lead only, no canonical-statement or H0 credit |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | Lean and Lake versions above; no update or build was run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned revision/tree above; package worktree clean |
| bounded `rg` for Hardy space, interpolating sequence, Carleson sequence, and pseudohyperbolic names in repo-local Lean and pinned mathlib | 1 | expected no-match; scoped intake search only, not an exhaustive anchor audit |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0253/IntakeProbe.lean)` | 0 | nine adjacent API checks elaborated; stdout SHA-256 `93296f15d9a3b7f310d67a50b31498cedc3b7cdb7f33edf9c7c70294495afa0`; no target or proof declared |
| `python3 -m json.tool` separately on all owned JSON and `.stage1-worker-selftest.json` | 0 | planned instance, open task DAG, provisional receipt, and worker handoff parsed |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0253-pycache python3 -m py_compile Stage1_Instances/THM-M-0253/check_intake.py` | 0 | scoped validator compiled without adding generated files to the owned path |
| `python3 -B Stage1_Instances/THM-M-0253/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target identity, pins, planned H1/M4/R4 boundary, null target, strict handoff, and six open tasks agree |
| scoped Lean scan for `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declarations | 1 | expected no-match; no proof escape declaration in the API-only probe |
| scoped `git diff --check` plus no-index checks for every untracked changed file | 0 | no whitespace diagnostics |

The first probe attempt used the undefined identifier `Sequence` and exited 1. It was replaced by
an explicitly typed `Nat -> Complex.UnitDisc` function before final evidence was recorded. That
failed attempt grants no evidence.

## Known downstream failures

- The exact source theorem and incorporated definitions, assumptions, conclusion, proof boundary,
  correction history, and independent review are open; only primary-work metadata was available.
- The domain, Hardy exponent/model, scalar and data spaces, sequence representation, interpolation
  predicate, characterization, normalizations, constants, quantifier order, and boundary cases are
  not selected by the catalog.
- No canonical Lean target, exact imports, elaborated expression/environment fingerprint, checked
  alternate encoding, or required statement mutation exists.
- The formal anchor audit, discovery protocol, obligation registry, typed graphs, proof,
  composition, trust closure, readable reconstruction, hermetic replay, deterministic evidence
  bundle, and independent release verification remain open.

These failures block statement, audit, and theorem-completion claims, but not a truthful,
self-tested `planned` intake that freezes the ambiguity boundary and opens the dependency DAG. Only
the integration lane may accept this provisional worker receipt.
