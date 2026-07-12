# Anchor-audit validation record

Item: `S56-M-0322-ANCHOR_AUDIT`  
Base revision: `8014740e5a37eff82745f6fd2bc69f0ee45e67c9`  
Audit date: 2026-07-12

## Result

The exact formal anchor is mathlib's `closure_convexHull_extremePoints` in
`Mathlib.Analysis.Convex.KreinMilman`. The installed dependency is at the manifest-pinned immutable
commit `8a178386ffc0f5fef0b77738bb5449d50efeea95`; the source blob is
`699ec84030f69d533bc040e02735b8e5fc86beff` and its SHA-256 is
`76a30354400127df51e995389646830f6960ae9c1bb33b2b91a5ad9ab5091e80`. The theorem has the exact
compactness and real-convexity premises and equality conclusion frozen by `KreinMilmanTarget`.
`kreinMilmanTarget_of_pinned` is already a checked repo-local wrapper to that terminal body.

Source inspection shows that the terminal proof establishes the easy inclusion by closedness and
convex-hull minimality. For the reverse inclusion it separates an assumed point outside the closed
convex hull, takes a maximizing exposed face, applies `IsCompact.extremePoints_nonempty`, transports
that face's extreme point back to an extreme point of the original set, and derives the separating
inequality contradiction. The supporting lemma itself uses Zorn minimality and geometric
Hahn-Banach separation. `#print axioms` reports exactly `propext`, `Classical.choice`, and
`Quot.sound` for both declarations. A defensive source scan found no `sorry`, `admit`, line-leading
`axiom`, `unsafe`, or oracle marker in the module. This is module-level evidence; the dependent
obligation-tree and validation phases still own complete transitive provenance and trust closure.

The bounded external search found no distinct Lean 4 implementation. Sourcegraph returned two
matches in one repository, both mathlib4; GitHub repository metadata returned zero repositories.
Unauthenticated GitHub code search returned HTTP 401 and is recorded as blocked, not negative.
Public search responses are dated and content-hashed discovery evidence, not immutable proof
candidates. No dependency was fetched or changed.

The mathlib module cites Barry Simon's 2011 book, chapter 8. Crossref confirms the book DOI and the
historical Krein-Milman paper's DOI and pages, but this formal-anchor node did not inspect an
immutable primary-text copy or complete theorem/page, assumption, errata, and independent-review
gates. Consequently `H2` remains unchanged. This phase supplies neither full audit completion nor
theorem completion.

## Commands and results

All commands ran inside this worker clone. Lean used only the existing pinned `.lake` environment;
no update, build, clone, or fetch was performed.

| Command | Exit | Result |
|---|---:|---|
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0322/AnchorAudit.lean` | 0 | exact root and supporting lemma types printed; both axiom sets were `[propext, Classical.choice, Quot.sound]`; terminal proof body printed |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0322/Statement.lean` | 0 | frozen target and checked pinned wrapper re-elaborated |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95`, equal to `lake-manifest.json` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD:Mathlib/Analysis/Convex/KreinMilman.lean` | 0 | source blob `699ec84030f69d533bc040e02735b8e5fc86beff` |
| `sha256sum Formalizations/Lean/.lake/packages/mathlib/Mathlib/Analysis/Convex/KreinMilman.lean` | 0 | source hash `76a30354400127df51e995389646830f6960ae9c1bb33b2b91a5ad9ab5091e80` |
| `rg -n -i 'sorry|admit|^[[:space:]]*axiom|unsafe|oracle' Formalizations/Lean/.lake/packages/mathlib/Mathlib/Analysis/Convex/KreinMilman.lean` | 1 | expected no-match status |
| Sourcegraph public search for four Krein-Milman aliases, Lean, forks/archives included | 0 | `matchCount=2`, one repository, mathlib4 only; response SHA-256 `0bfea4e...fcd62a6` |
| GitHub REST repository search for `\"Krein-Milman\" lean` | 0 | zero complete results; response SHA-256 `08c082...2600b2` |
| GitHub REST code search for `\"Krein-Milman\" language:Lean` | 0 | captured HTTP 401 authentication blocker; response SHA-256 `b7dbd1...65e29e` |
| `python3 -m json.tool Stage1_Instances/THM-M-0322/anchor-audit.json` | 0 | structured audit JSON valid |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | rev-5.6 standard and 1546-target coverage passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0322` | 0 | rank 819, planned, legacy artifacts unaccepted, theorem incomplete |
| `git diff --check -- Stage1_Instances/THM-M-0322 .stage1-worker-selftest.json` | 0 | no whitespace errors |

## Status boundary

The machine anchor is exact, immutable, pinned, locally imported, and wrapper-checked. The item is
self-tested pending master acceptance. Downstream phases must still freeze the obligation graphs,
audit transitive terminal bodies and trust, validate reproducibility, and decide release. No `M0`,
`AUDIT-Z`, `THEOREM-Z`, or theorem-completion claim is made here.
