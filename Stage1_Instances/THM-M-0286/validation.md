# THM-M-0286 intake validation

Base revision: `2eea98305d46266f078a50cf0e85853bf6a5e702` (tree
`02279a8caa5f31ed8e37e35c8584a336eed9b974`). Validation ran on 2026-07-13 in
the isolated worker clone.

Validation is limited to target-set consistency, dossier structure and scope invariants, source-
record provenance, pinned environment identity, a narrow Lean API probe, bounded local discovery,
proof-escape hygiene, JSON integrity, and whitespace. The catalog gloss does not determine a
canonical proposition, so the probe checks candidate interfaces only and supplies no statement or
proof credit.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. It was preserved and used read-
only. No `lake update`, `lake build`, dependency clone or fetch, or other `.lake` mutation was
performed. This is nonrelease worker evidence.

## Environment

- Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, target
  `x86_64-unknown-linux-gnu`.
- Lake `5.0.0-src+98dc76e`.
- Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package status was clean after the probe.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Commands and results

| Command (repository root unless noted) | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0286` | 0 | rank 1292, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all` (preflight) | 0 | only the automation-provided untracked `Formalizations/Lean/.lake` symlink existed before intake |
| `git rev-parse HEAD 'HEAD^{tree}'`; `git blame -L 2055,2060 -- Docs/researches/math_theorems.md` | 0 | base revision/tree recorded above; all six uncited catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| bounded Crossref, EuDML, Gallica, BnF, Internet Archive, and OpenAlex source discovery | mixed | no immutable primary scan and exact reviewed theorem passage was admitted; network timeouts, 403/404/429 responses, or no exact result were recorded as non-evidence |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | versions recorded above; no update or build was run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'`; package `status --short` | 0 | pinned revision/tree recorded above; empty status output |
| `(cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0286/IntakeProbe.lean)` | 0 | one supporting definition and four direct Egorov interfaces elaborated; three representative declarations reported `[propext, Classical.choice, Quot.sound]`; complete output SHA-256 `464b3a706f14c55c7158b6e30b175ba6586a88618cdda1bf128c20bedcaf871f` |
| bounded `rg` search in pinned mathlib and repo-local Lean | 0/1 | direct module, downstream uses, and Wikidata mapping found; no repo-local source-identical root outside pinned mathlib, and no proof credit inferred |
| `python3 -m json.tool` on the three owned JSON files and `.stage1-worker-selftest.json` | 0 | all structured artifacts parse after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0286-pycache python3 -m py_compile Stage1_Instances/THM-M-0286/check_intake.py` | 0 | checker compiled without adding generated files to the owned path |
| `python3 -B Stage1_Instances/THM-M-0286/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target/DAG identity, source and dependency hashes, null target, H1/M3/R4 boundary, inventory, receipt/handoff agreement, pinned probe, and six open tasks agree |
| token-anchored prohibited Lean declaration scan over the owned path | 1 | expected no-match; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration token; diagnostic `#print axioms` is permitted |
| `git diff --check` and scoped new-file `git diff --no-index --check` checks | 0 | no whitespace diagnostics |

## Known downstream failures

- No immutable primary edition, exact theorem passage, incorporated definitions, complete premise
  and conclusion map, proof boundary, translation, correction or errata audit, and independent
  source review is admitted.
- The root does not yet select domain, codomain, measure and finiteness scope, sequence index,
  measurability convention, almost-everywhere premise, exceptional-set construction and bound,
  retained set, uniform-convergence predicate, or boundary cases.
- Canonical Lean target, minimal imports, elaborated expression and environment fingerprints,
  checked transports among subset/global and measurable-distance/strong-measurability forms, and
  statement mutation tests are open.
- Exhaustive anchor/provenance audit, discovery protocol, obligation registry, typed graphs, proof,
  composition, trust closure, readable reconstruction, hermetic replay, deterministic bundle,
  independent verification, audit completion, theorem completion, and master acceptance remain
  downstream.

These failures do not invalidate a truthful, self-tested `planned` intake. They do block statement
acceptance and every theorem-completion claim. Only the integration lane may accept the provisional
worker receipt.
