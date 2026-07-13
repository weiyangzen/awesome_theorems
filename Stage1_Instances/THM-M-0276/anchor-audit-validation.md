# THM-M-0276 Anchor-Audit Validation

Item: `S56-M-0276-ANCHOR_AUDIT`

Base revision: `fcabbf1e0ad9507eebe91663bccabfa87d22813e`

Base tree: `873e589c594454b7f263c7ed2342089a4d15e842`

Validation date: `2026-07-13` (`Asia/Shanghai`)

## Result

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`,
`ContinuousLinearMap.isOpenMap` proves a stronger semilinear Banach open mapping theorem.
`AnchorAudit.lean` specializes it separately to ordinary same-field real and complex maps and
thereby inhabits the exact frozen conjunction. Its fully explicit expanded proposition hashes to
the statement-phase fingerprint `0cfb9796...82fa`.

The terminal body first calls `ContinuousLinearMap.exists_preimage_norm_le`, whose convergent-series
body calls `exists_approx_preimage_norm_le`; that first step uses Baire category on
`union n, closure (f '' ball 0 n)`. The pinned source therefore contains a real formal proof route
and correctly uses radius-`n` balls. This does not by itself repair the independently tracked H2
human-source gap.

Lean reports the two helpers, terminal theorem, and exact adapter sorry-free. All four axiom reports
are exactly `propext`, `Classical.choice`, and `Quot.sound`. A machine traversal of their transitive
environment closure reports 17,187 declarations in 654 modules, no bodyless nonaxiom, and no unsafe
declaration. Full compiled-artifact and executable TCB provenance remains a later validation gate.

The bounded external search found `facebookresearch/atlas-lean@34ffed396f...`, whose
`OpenMapping.open_mapping_theorem` has compatible pins and a stronger same-field statement. A
temporary read-only replay passed, but its entire body is a one-line call to the same mathlib
theorem, so it is a duplicate rather than an independent terminal proof. Its restrictive license
also blocks useful integration. `optsuite/optlib@03124b75...` only consumes the controlled-preimage
lemma for a finite-dimensional inverse bound at older pins; it has no open-mapping declaration.

The exact pinned route is thus an `M1` candidate with a worker-local `E2` probe. This untracked,
provisional audit adapter is not an accepted repo-local validation closure. Under the rev-5.6
evidence hierarchy, `M0-W` requires accepted proof integration and a release-grade `E1` packet; it
cannot be assigned from this audit alone. The accepted root remains `[H2, M3, R4]` until master
acceptance and downstream obligation, proof, composition, provenance, trust, validation, and
release gates. Neither `AUDIT-Z` nor theorem completion is claimed.

## Commands And Results

Local validation used the automation-provided canonical `.lake` symlink read-only. No
`lake update`, `lake build`, dependency clone/fetch, checkout, package edit, or other `.lake`
mutation ran.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, the execution skill, and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets in ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0276` | 0 | rank 1282; planned; no legacy slot; theorem incomplete |
| `git rev-parse HEAD 'HEAD^{tree}'`; initial `git status --short` | 0 | base revision/tree above; only the automation-provided `.lake` symlink was pre-existing and untracked |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'`; status | 0 | exact revision `8a1783...ea95`, tree `bdc39a...5c2b`; dependency worktree clean |
| scoped repo-local and all-package `rg` searches | 0 | direct mathlib route classified; no separate candidate in materialized non-mathlib dependencies |
| mathlib `git log`, `blame`, `show`, ancestry, blob, and source-hash checks | 0 | terminal body, Lean 4 port `81b313...`, semilinear change `d11fcd...`, authors, trees, and ancestry verified |
| seven Sourcegraph global Lean query families with forks/archives | 0 | exact declaration only in mathlib; Atlas duplicate and Optlib consumer classified; response hashes recorded |
| three GitHub repository searches | 0 | each returned `total_count=0`, `incomplete_results=false`; GitHub code/commit API later returned HTTP 403 and was not credited as negative evidence |
| three grep.app queries | HTTP 429 | access checkpoint recorded with response hashes; no negative claim |
| commit-addressed Atlas raw/toolchain/manifest/license/archive inspection and `git ls-remote` | 0 | immutable revision, matching Lean/mathlib pins, source/archive hashes, restrictive license, and duplicate wrapper recorded |
| temporary current-pin replay of Atlas `OpenMapping.lean` plus `#print sorries`, axioms, and body | 0 | wrapper elaborated, was sorry-free, reported only the standard three axioms, and reduced directly to mathlib; output SHA-256 `d2b368...419e` |
| immutable Optlib archive/source/toolchain/manifest inspection | 0 | source SHA `bbf6fe...31db7`; Lean 4.13.0 and mathlib `d731765...bb841`; downstream consumer only |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0276/Statement.lean` | 0 | exact frozen statement re-elaborated |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0276/AnchorAudit.lean` | 0 | exact adapter and terminal bodies checked; four sorry-free reports; four standard-axiom reports; clean transitive closure; stdout SHA-256 `a58da843...04fb` |
| `python3 -B Stage1_Instances/THM-M-0276/check_anchor_audit.py` | 0 | authority item, frozen statement, local pins/blobs/histories, recorded external metadata, inventory, receipt, packet, and narrow Lean replay agreed; exact candidate classified M1/E2 while accepted root remains M3 |
| `python3 -m json.tool` on anchor JSON artifacts and root packet | 0 | all structured artifacts parsed |
| scoped prohibited-construct scan over `AnchorAudit.lean` and direct mathlib body region | 1 (expected no match) | no placeholder, bodyless axiom, unsafe/opaque declaration, oracle, external implementation, or generated proof marker |
| `git diff --check -- Stage1_Instances/THM-M-0276 .stage1-worker-selftest.json` plus per-new-file checks | 0 | no whitespace diagnostics |

## Discovery Boundary

The inventory is bounded rather than globally saturated. Sourcegraph's recorded streams completed
without skipped repositories for those query forms, but public indexing is not the entire Lean
ecosystem. GitHub authenticated code search was unavailable/rate-limited and grep.app returned an
access checkpoint. Those failures cannot support an absence claim. New discoveries must create a
successor inventory rather than overwrite this one.

Atlas, Optlib, and public-search response bytes were inspected and hashed in temporary worker
storage but are not retained in this provisional packet. The ledger validator checks their recorded
metadata for internal consistency, not a fetch-free replay of those external digests. Independent
retrieval and replay remain acceptance work; only the pinned local mathlib evidence is fully
replayed by the current validator.

## Status Boundary

This phase supplies provisional self-tested anchor evidence pending master acceptance. The
obligation registry, canonical proof-phase composition, release-grade provenance and TCB closure,
H0 source correction and independent review, R0 reconstruction, hermetic offline replay,
independent validation, deterministic release evidence, `AUDIT-Z`, and theorem completion remain
open.
