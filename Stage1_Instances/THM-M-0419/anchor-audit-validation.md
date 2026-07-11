# THM-M-0419 anchor-audit validation

Item: `S56-M-0419-ANCHOR_AUDIT`  
Base revision: `71fb75ff5b70107068a33e8f5e3f3746a5ae4aa3`

## Result

Pinned mathlib commit `8a178386ffc0f5fef0b77738bb5449d50efeea95` contains cyclotomic-field,
abelian-Galois easy-direction, Dirichlet-character conductor, and ramification/inertia APIs. The 13
declarations in `AnchorAudit.lean` elaborate, but none maps an arbitrary finite abelian extension of
`ℚ` to an embedding in a cyclotomic field. A pinned-source search found no terminal declaration.

The public search did locate a serious external candidate that the legacy audit had missed:
`facebookresearch/atlas-lean@34ffed396f376454c1a9b297f3fd74c5c801fb50`, module
`Atlas.NumberTheoryI.code.KroneckerWeber`, declaration `KroneckerWeber.theorem_20_1`. Its conclusion
has the intended cyclotomic-embedding shape and it uses the same Lean 4 and mathlib revisions as this
clone. It is not machine closure. The immutable source contains 22 `sorry` occurrences, including
`conductor_from_local_cyclotomic_data` and `inertia_minkowski_gives_embedding`, which feed the global
bridge used by the terminal theorem. It also uses a project-local `IsAbelianExtension` context rather
than the frozen mathlib `IsAbelianGalois` context, and no checked adapter exists. Finally, its license
is CC BY-NC 4.0 with an additional no-training rider, so any future reuse needs license review.

The exact root therefore remains `M3`: the proposition is elaborated, but no no-placeholder terminal
proof candidate is available. The debt is `formalization_debt`, not repo-local integration debt,
because the located external artifact itself is incomplete. This is a completed bounded anchor audit,
not theorem completion or a claim that no other Lean proof exists.

## Commands and results

Commands ran on 2026-07-12 in this worker clone. No Lake dependency was updated, fetched, cloned, or
built.

| Command | Exit | Result |
|---|---:|---|
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0419/AnchorAudit.lean` | 0 | All 13 pinned mathlib declarations elaborated and printed their types. |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0419/Statement.lean` | 0 | The frozen exact target re-elaborated. |
| `python3 Stage1_Instances/THM-M-0419/check_anchor_audit.py` | 0 | Audit boundary, probes, manifest pin, installed mathlib HEAD, and external placeholder classification agreed. |
| `rg -n -i 'Kronecker.?Weber\|kronecker_weber\|kroneckerWeber\|IsAbelianGalois.*Cyclotomic\|CyclotomicField.*IsAbelianGalois' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 0 | Only the easy direction appeared in `Cyclotomic/Basic.lean` and a use of it in `NumberField/Cyclotomic/Ideal.lean`; no terminal converse appeared. |
| Sourcegraph API query for the hyphenated, spaced, and camel-case names in Lean | 0 | 74 matches, all in `facebookresearch/atlas-lean` at indexed commit `34ffed...`; response SHA-256 `4d2ec5...27d6`. |
| GitHub API complete-tree query for `facebookresearch/atlas-lean@34ffed...` | 0 | Complete immutable tree (`truncated=false`); response SHA-256 `3a6c23...2233`. |
| Immutable raw inspection of `Atlas/NumberTheoryI/code/KroneckerWeber.lean` | 0 | SHA-256 `0b0d47...3617`; 22 `sorry` occurrences; terminal `theorem_20_1` and its placeholder-bearing global dependencies identified. |
| Immutable raw inspection of external `lean-toolchain`, `lake-manifest.json`, and `LICENSE` | 0 | Lean v4.29.0, mathlib `8a178...`, and restrictive license recorded with content hashes in `anchor-audit.json`. |
| GitHub REST repository searches for quoted and camel-case names | 0 | Both returned `total_count=0`, `incomplete_results=false`; explicitly treated as incomplete discovery because Sourcegraph found a candidate. |
| GitHub REST code search | 0 transport | HTTP 401 authentication blocker; no negative result claimed. |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Rev-5.6 structure and 1546-target coverage passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all uniform L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-0419` | 0 | Rank 74, planned, legacy artifacts unaccepted, theorem incomplete. |
| `git diff --check -- Stage1_Instances/THM-M-0419 .stage1-worker-selftest.json` | 0 | No whitespace errors. |

## Open integration gate

Reopen only for an immutable no-placeholder Lean 4 candidate with a compatible license, exact type or
checked transport, terminal dependency and axiom provenance, and a successful repo-local pinned
wrapper check. The Atlas candidate cannot receive proof credit while its transitive source retains
the recorded placeholders.
