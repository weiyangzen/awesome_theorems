# Intake validation

Base revision: `a3b18eec39bf04be025b1641cae02f4d44fdf11a` (tree
`fdfff18dea4c6798c5b322b6088dfe556109c134`). Validation ran on 2026-07-13 in the isolated worker
clone.

Validation is limited to target-set consistency, dossier and scope invariants, repository-source
provenance, primary-source discrimination, pinned environment identity, a narrow Lean API probe,
bounded local topic discovery, proof-escape hygiene, JSON validity, and whitespace. The catalog
gloss does not select a binder-complete proposition, so the probe checks only possible substrate
and receives no statement or proof credit.

The preflight worktree contained only the automation-provided untracked `Formalizations/Lean/.lake`
symlink to canonical pinned artifacts. It was used read-only. No `lake update`, `lake build`,
dependency clone or fetch, or other `.lake` mutation was performed. This is nonrelease worker
evidence.

| Command (repository root unless noted) | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0956` | 0 | rank 1490, planned, L0/rework_required, no legacy slot, legacy artifacts unaccepted, theorem_complete false |
| `git status --short --untracked-files=all` and `git rev-parse HEAD 'HEAD^{tree}'` | 0 | isolated base recorded; initial status contained only the pre-existing automation `.lake` symlink |
| `git blame -L 6980,6985 -- Docs/researches/math_theorems.md` | 0 | all six sparse catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| Crossref query for DOI `10.1112/jlms/s1-16.4.212`, download of the Renyi-hosted scan, `pdfinfo`, and `pdftotext` | 0 | title/authors/date/pages confirmed; four-page primary scan inspected, 671160 bytes, SHA-256 `25cc7c8d...b091`; source evidence only, no H0 |
| `python3 -m json.tool` over all structured owned artifacts and the root packet | 0 | valid JSON after finalization |
| `python3 -B Stage1_Instances/THM-M-0956/check_intake.py` and replay with `--worker-packet .stage1-worker-selftest.json` | 0 | target identity, planned H1/M4/R4 boundary, null canonical target, exact inventory, source pins, packet, and six open tasks agree |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | Lean 4.29.0 at commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`; Lake 5.0.0 |
| `(cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0956/IntakeProbe.lean)` | 0 | eight adjacent pinned APIs elaborated; combined output SHA-256 `79534f6c...344c3`; no target theorem stated |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and `status --short` | 0 | mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree `bdc39a31...c2b`; source tree clean |
| bounded `rg` for Sidon, Erdos-Turan, B2-sequence, and unique-pair-sum declarations in pinned mathlib and repo-local Lean | 1 | expected no-match exit; intake discovery only, not an anchor audit |
| scoped prohibited-construct scan over `Stage1_Instances/THM-M-0956` | 1 | expected no-match exit; no `sorry`, `admit`, `sorryAx`, axiom, constant, opaque, or unsafe declaration in the API-only probe |
| scoped `git diff --check`, per-file no-index whitespace checks, and owned-file invariants | 0 | no whitespace diagnostics; no-index exit 1 accepted only as the expected new-file difference |

Known downstream failures remain deliberately open: master acceptance of this provisional intake;
independent admission and review of the source scan; selection of the exact construction or
corollary; Sidon, construction, residue, pair, bound, quantifier, and boundary conventions;
canonical Lean elaboration, fingerprints, checked transports, and mutations; formal anchor audit;
obligation and typed-graph freezes; proof and composition; trust closure; readable reconstruction;
hermetic replay; deterministic evidence bundling; and independent release verification. These
block theorem execution and completion but do not invalidate a truthful, self-tested `planned`
intake.
