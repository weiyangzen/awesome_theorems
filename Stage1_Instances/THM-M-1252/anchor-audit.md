# Anchor audit

Item: `S56-M-1252-ANCHOR_AUDIT`  
Audit date: `2026-07-12`  
Base revision: `9144fc9aa3522671a4cda7de9d460d01f382367a`

## Selected immutable mathlib anchor

The pinned dependency `leanprover-community/mathlib4` at commit
`8a178386ffc0f5fef0b77738bb5449d50efeea95` contains the exact generic theorem
`Distribution.dsupport_compl_eq` in `Mathlib.Analysis.Distribution.Support`. At that revision its
source is lines 97-99 of `Mathlib/Analysis/Distribution/Support.lean`:

```lean
/-- The complement of the support is the largest open set on which `f` vanishes. -/
theorem dsupport_compl_eq : (dsupport f)ᶜ = ⋃₀ { a | IsVanishingOn f a ∧ IsOpen a } := by
  simp [dsupport, Set.compl_sInter, Set.compl_image_set_of]
```

The file entered mathlib in commit `f3e1fb7e116140d3a763edccd5c1b8a76c2ff100` (Moritz Doll,
2026-03-30, `feat(Analysis/Distribution): support (#34637)`). The checked-out tree is exactly the
manifest pin and is clean. The package declares Apache-2.0 licensing. The terminal body is present,
contains no placeholder, and the Lean axiom report contains only `propext`, `Classical.choice`, and
`Quot.sound`; it does not contain `sorryAx`.

The theorem is more general than the frozen target: it quantifies over a `FunLike` test-function
type, any topological ambient type, and zero-valued codomain. `AnchorAudit.lean` specializes those
parameters to `T : Distribution Ω ℝ ⊤` and checks the frozen equality without rewriting or
adding assumptions. Thus this is an exact `M0-W` candidate already in the local pinned dependency
closure, not merely an upstream URL anchor. Final `M0-W` classification belongs to the later
obligation/proof/validation phases.

## Candidate comparison

| Candidate at the same mathlib pin | Match decision |
|---|---|
| `Distribution.dsupport_compl_eq` | Selected: exact conclusion after parameter specialization. |
| `Distribution.notMem_dsupport_iff` | Rejected as root: pointwise membership corollary, not the frozen set equality. |
| `Distribution.mem_dsupport_iff_not_isVanishingOn` | Rejected as root: neighborhood characterization with a different conclusion. |
| `Distribution.mem_dsupport_iff_forall_exists_ne` | Rejected as root: witness characterization, useful only as a later readable bridge. |
| `Distribution.compl_dsupport_eq_sUnion_isBounded` | Rejected as root: bounded-open indexed family and extra pseudometric structure. |

Repository-local search found no competing proof of the exact target outside this dossier. Search
over all packages already pinned by `lake-manifest.json` found the selected mathlib declaration and
no distinct external-project candidate. A focused GitHub public repository query for distribution
formalizations in Lean returned no relevant repository. Attempts to query the public grep.app code
index for the exact symbol and predicate were rate-limited with HTTP 429. That failure is recorded
as an access limit, not converted into evidence that no other public formalization exists. No
external candidate is assigned `M1` or proof credit.

## Commands and results

Commands ran in the worker clone. Lean commands ran from `Formalizations/Lean`; no update, fetch,
build, clone, or mutation of `.lake` was performed.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-1252/AnchorAudit.lean` | 0 | exact specialization elaborated; both selected theorem and wrapper report only `propext`, `Classical.choice`, and `Quot.sound`, with no `sorryAx` |
| `git -C .lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `git -C .lake/packages/mathlib status --short` | 0 | no output; pinned dependency tree clean |
| `git -C .lake/packages/mathlib log -1 --format=... -- Mathlib/Analysis/Distribution/Support.lean` | 0 | introduction commit `f3e1fb7e...`, author/date/subject recorded above |
| `rg -n 'dsupport_compl_eq|IsVanishingOn' .lake/packages` | 0 | exact mathlib anchor and related declarations inventoried; no distinct pinned-project candidate |
| `curl ... 'https://api.github.com/search/repositories?q=distribution+theorem+prover+lean4&per_page=10'` | 0 | GitHub API reported `total_count: 0` |
| `curl ... 'https://grep.app/api/search?q=dsupport_compl_eq'` | 22 | HTTP 429; explicit external-search limitation |
| `python3 -m json.tool ../../Stage1_Instances/THM-M-1252/anchor-audit.json` | 0 | structured audit is valid JSON |
| `rg -n '\\b(sorry|axiom|admit)\\b' ../../Stage1_Instances/THM-M-1252/AnchorAudit.lean` | 1 | no placeholders or declarations of new axioms |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | rev-5.6 standard and 1546-target projection pass |
| `python3 scripts/stage1_target.py check` | 0 | manifest/checklist consistency passes |
| `python3 scripts/stage1_target.py show THM-M-1252` | 0 | rank 431, planned, theorem incomplete |
| `git diff --check -- Stage1_Instances/THM-M-1252` | 0 | no whitespace errors |

## Status boundary

The anchor-audit deliverable is self-tested pending master acceptance. It establishes an exact,
pinned, locally checkable mathlib candidate. Human primary-source pinpointing remains `H2`; the
intake's Schwartz leads were not upgraded. The obligation tree, final proof artifact, release-grade
trust and provenance closure, hermetic replay, independent review, and theorem completion remain
open.
