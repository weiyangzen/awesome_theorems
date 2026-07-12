# Anchor audit

Item: `S56-M-1013-ANCHOR_AUDIT`  
Base revision: `48a1d632cacabc75bca90db155d57ebb777aee3d`  
Audit date: 2026-07-12

## Immutable search boundary

The dependency manifest pins mathlib to commit
`8a178386ffc0f5fef0b77738bb5449d50efeea95` and Lean to
`leanprover/lean4:v4.29.0`. The local mathlib checkout reports that exact commit and is clean.
The repository-local candidate is the tracked blob
`f720505623eccf9e3899d96f774d2c06fa527b82` at
`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_292.lean`, last changed by repository commit
`16d227cffb7cb7d9e8392b6c0ff8211e498e1330`.

Searches covered the complete pinned mathlib source tree and the tracked repository using the
spellings `CramerWold`, `cramer_wold`, `Cramer-Wold`, `Cramér-Wold`, plus semantic searches for
weak convergence, pushforward continuity, and characteristic functions. Loogle name-index queries
for the four Cramer-Wold spellings returned zero declarations. Attempts to extend coverage with
unauthenticated GitHub and grep.app code search were rejected (HTTP 403 and 429 respectively), so
no claim of exhaustive global Lean 4 ecosystem coverage is made.

## Candidate inventory

| Candidate | Exact source and revision | Type relevance | Provenance and trust | Feasibility / verdict |
|---|---|---|---|---|
| Direct mathlib Cramer-Wold declaration | Entire `Mathlib` tree at `8a178386...a95` | No name or text hit for the theorem spellings | N/A: no declaration located | No direct anchor exists at the pin |
| Continuous-mapping direction | `Mathlib.MeasureTheory.Measure.ProbabilityMeasure`, `ProbabilityMeasure.tendsto_map_of_tendsto_of_continuous`, `8a178386...a95` | Exactly maps weak convergence through each continuous scalar projection | Source proof in pinned mathlib; Apache-2.0; Lean 4.29.0; no unsafe declaration or admitted proof located in the source file | Already dependency-legal; closes only the forward implication |
| Levy characteristic-function bridge | `Mathlib.MeasureTheory.Measure.LevyConvergence`, `ProbabilityMeasure.tendsto_iff_tendsto_charFun`, `8a178386...a95` | Weak convergence iff pointwise characteristic-function convergence on finite-dimensional real inner-product spaces | Source theorem body in pinned mathlib; Apache-2.0; Lean 4.29.0; no unsafe declaration or admitted proof located in the source file | Already dependency-legal; with the projection identity it closes the reverse implication |
| Projection characteristic-function identity | `AnchorAudit.lean`, `projection_charFun_one_measure`, working tree based on `48a1d632...3d` | Identifies the scalar pushforward characteristic function at frequency one with the vector characteristic function at the coefficient vector | Local proof body checked by Lean; terminal dependencies are pinned mathlib declarations | Exact local bridge, no external dependency |
| Repository-local full candidate | `AwesomeTheorems.Stage1.S1_M_292`, tracked blob `f720505...27b82`, repository commit `16d227c...330`; independently reconstructed as `AnchorAudit.repoLocalCandidate` | Exact biconditional frozen in `Statement.lean`, including every `d : Nat` and `d = 0` | Local source proof; kernel report lists only `propext`, `Classical.choice`, and `Quot.sound`; no unsafe declaration or admitted proof found | Exact, importable candidate. Direct import lacked a prebuilt project olean in this clone, so the audit rechecked an exact-type reconstruction against pinned mathlib instead of building shared artifacts |
| Separate external Lean 4 project | Loogle live declaration-name index queried 2026-07-12; GitHub/grep.app fallbacks as above | No terminal candidate identified | No immutable source revision exists to inspect | Not credited; global coverage remains bounded by the documented search failures |

The checked wrapper deliberately proves the exact canonical biconditional rather than the historical
random-variable-only or reverse-only shapes. It imports only the two modules used by the frozen
statement. This audit therefore finds a strong repo-local candidate and the exact pinned mathlib
anchors needed by it, but does not promote machine status or claim anchor-audit acceptance.

## Exact validation

| Command | Exit | Result |
|---|---:|---|
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | empty; pinned dependency checkout is clean |
| `git ls-files -s Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_292.lean` | 0 | tracked blob `f720505623eccf9e3899d96f774d2c06fa527b82` |
| `git log -1 --format='%H %cI' -- Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_292.lean` | 0 | `16d227cffb7cb7d9e8392b6c0ff8211e498e1330 2026-07-11T03:15:26+08:00` |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1013/AnchorAudit.lean` | 0 | exact biconditional elaborated; `#print axioms` reports `[propext, Classical.choice, Quot.sound]` |
| Loogle quoted name queries for `CramerWold`, `cramer_wold`, `Cramer-Wold`, `Cramér-Wold` | 0 | four JSON responses, each with `count: 0` |
| `curl` GitHub code-search API fallback | 22 | HTTP 403; unauthenticated external coverage unavailable |
| `curl` grep.app API fallbacks | 22 | HTTP 429; external coverage unavailable |

## Status boundary

The requested audit is locally self-tested and records a viable exact repo-local candidate at
immutable revisions. Master acceptance is still required. This phase does not establish human
source status, obligation-tree acceptance, proof-phase credit, hermetic validation, independent
review, or theorem completion. The unresolved audit limitation is global external-project coverage;
it does not invalidate the positive pinned candidate evidence, but no negative ecosystem-wide claim
may be derived from this receipt.
