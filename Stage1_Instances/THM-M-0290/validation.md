# Intake validation

Base revision: `f294137feee7840fd105a4d3f6073d5cf45508ea` (tree
`234b8f273d252c2c42ce6860315ed973049c871a`). Validation ran on 2026-07-13 in
the isolated worker clone, timezone `Asia/Shanghai`.

Validation is limited to target-set consistency, dossier structure and scope invariants, repository
source provenance, primary-work and external-formalization discovery boundaries, pinned environment
identity, a narrow Lean API probe, a bounded local name search, JSON integrity, proof-escape hygiene,
and whitespace. It does not elaborate an invented canonical statement, import the external project,
or inspect proof closure.

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
- Pinned mathlib `Mathlib/Analysis/Fourier/AddCircle.lean` SHA-256:
  `32363b7144bee4cdc3f96e41237eb6944c8dd6ac92449340a0c27462959e7c81`.

## Commands and results

| Command (repository root unless noted) | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok`; 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0290` | 0 | rank 1296, planned, L0/rework-required, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all` (preflight) | 0 | only pre-existing automation symlink `Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree recorded above |
| `git blame -L 2083,2088 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `sed -n '2083,2088p' Docs/researches/math_theorems.md \| sha256sum` | 0 | exact catalog block SHA-256 `f929da8b6b10af1926974b81d7291945c69d197f490529a56319c2915bc2ac9b` |
| `curl -fsSL` immutable raw URLs for `fpvandoorn/carleson@80e151.../blueprint/src/bibliography.bib`, `Carleson/Classical/CarlesonHunt.lean`, and `Carleson/Classical/Basic.lean`, followed by `sha256sum` and scoped line inspection | 0 | found MR238019 and the exact candidate/cutoff sources; SHA-256 values `0974024f...`, `d9a8d0f...`, and `dcfd4cb1...`; no dependency integration, build, kernel, or proof credit |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | Lean and Lake versions above; no update or build was run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned revision/tree above; package worktree clean |
| bounded exact-name `rg` for `carleson_hunt` and `partialFourierSum` in repo-local Lean and pinned mathlib | 1 | expected no-match apart from prose in this API probe; intake search only, not an exhaustive anchor audit |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0290/IntakeProbe.lean)` | 0 | nine adjacent pinned APIs elaborated; stdout SHA-256 `3473600293b90e19c7ef56a027cc17de93479c69c2a7eb1586d4032070b1de82`; no target or proof declared |
| `python3 -m json.tool` separately on all owned JSON and `.stage1-worker-selftest.json` | 0 | planned instance, open task DAG, provisional receipt, and worker handoff parsed |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0290-pycache python3 -m py_compile Stage1_Instances/THM-M-0290/check_intake.py` | 0 | scoped validator compiled without adding generated files to the owned path |
| `python3 -B Stage1_Instances/THM-M-0290/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target identity, pins, planned H1/M4/R4 boundary, null target, candidate boundary, strict handoff, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0290/check_intake.py --master-replay` | 0 | replay mode passed without the ephemeral worker packet, binds the recorded base commit/tree and base DAG hash as attested inputs, and permits the authority's pre-integration `[ ]` or integrated `[_]` state |
| scoped Lean scan for `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declarations | 1 | expected no-match; no proof escape declaration in the API-only probe |
| scoped `git diff --check` plus no-index checks for every untracked changed file | 0 | no whitespace diagnostics |

## Known downstream failures

- The exact primary-source theorem, incorporated definitions, assumptions, conclusion, proof
  boundary, correction history, errata, and independent review are open; only a primary-work
  bibliographic lead was inspected.
- The exponent range, domain and period, scalar field, function model, measure and Fourier
  normalizations, cutoff convention, representative, quantifier order, and boundary cases are not
  selected by the catalog.
- No canonical Lean target, exact imports, elaborated expression/environment fingerprint, checked
  alternate encoding, or required statement mutation exists.
- The external `carleson_hunt` declaration is not in the dependency lock and was not built,
  imported, checked for transitive placeholders/axioms, source-crosswalked, or adapted locally.
- The exhaustive formal anchor audit, discovery protocol, obligation registry, typed graphs, proof,
  composition, trust closure, readable reconstruction, hermetic replay, deterministic evidence
  bundle, independent release verification, and master acceptance remain open.

These failures block statement, audit, and theorem-completion claims, but not a truthful,
self-tested `planned` intake that freezes the ambiguity boundary and opens the dependency DAG. Only
the integration lane may accept this provisional worker receipt.
