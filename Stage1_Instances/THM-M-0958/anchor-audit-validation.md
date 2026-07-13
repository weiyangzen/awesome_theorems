# THM-M-0958 anchor-audit validation

Item: `S56-M-0958-ANCHOR_AUDIT`

Base revision: `f023dbc3411d83201065d1a1156d7406b81135d4`

Validation date: 2026-07-13 (`Asia/Shanghai`)

## Result

The frozen target is Elkin's equation (5) asymptotic lower bound, with the exact base-two
coefficient and fourth-root logarithmic factor. A repository-local search outside this dossier and
a search of every materialized pinned Lake package found no exact proof declaration. The public
Sourcegraph queries, including archived repositories and forks, likewise returned no `Elkin`,
paper-title, `Real.logb 2`, or `2 * Real.sqrt 2` Lean result. These are complete bounded query
responses, not proof that no unindexed, private, deleted, or future formalization exists.

Pinned mathlib at `8a178386ffc0f5fef0b77738bb5449d50efeea95` does contain a genuine
machine-checked Behrend construction. In particular, `Behrend.roth_lower_bound` proves

```text
(N : Real) * exp (-4 * sqrt (log N)) <= rothNumberNat N.
```

`AnchorAudit.lean` directly checks that result and its explicit asymptotic helper. Both are
sorry-free, and the scoped transitive closure reports only `propext`, `Classical.choice`, and
`Quot.sound`, with no bodyless nonaxiom or unsafe declaration. The audit-local wrapper closes only
this Behrend proposition. A failure fixture guards that it is not definitionally the Elkin target;
the ledger also records the missing base-two coefficient and fourth-root factor. It receives no
exact-root credit.

The only non-mathlib public `ThreeAPFree` hits were unrelated Erdos-problem statements at
`google-deepmind/formal-conjectures@b2e608fc...`; both bodies are `by sorry`, and the project has
different Lean and mathlib pins. They are classified `M5` rejected leads, not candidates.

All seven frozen inventory members are classified. The exact root therefore remains
`[H1, M3, R4]`. This completes only the assigned bounded anchor inventory pending master
acceptance. Global audit completion and theorem completion remain false.

## Commands and exact outcomes

Commands ran inside the isolated worker clone. The scheduler-provided `.lake` symlink was used
read-only. No `lake update`, `lake build`, dependency clone/fetch, or `.lake` mutation was run.

| Command | Exit | Outcome |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets and ranks 1 through 1546 passed |
| `python3 scripts/stage1_target.py show THM-M-0958` | 0 | rank 1492, planned, L0/rework-required, theorem incomplete |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | revision `8a178386...a95`, tree `bdc39a...c2b`, matching the manifest |
| repo-local exact Elkin alias search outside this dossier | 1, expected | no exact local proof body or wrapper |
| exact Elkin alias search over every materialized Lake package | 1, expected | no exact pinned-package candidate |
| pinned mathlib AP-tree and quantitative searches | 0 | only `Defs.lean`, `Behrend.lean`, Roth upper-bound material, and Behrend downstream consumers; no Elkin formula |
| Sourcegraph exact `Elkin`, paper-title, `Real.logb 2`, and `2 * Real.sqrt 2` Lean queries | 0 | four complete responses with `matchCount=0` and content hashes recorded in `anchor-audit.json` |
| Sourcegraph `rothNumberNat` and `ThreeAPFree` Lean queries | 0 | mathlib surfaces plus two unrelated placeholder-bearing formal-conjecture files; all immutable leads classified |
| GitHub REST repository searches | 0 | five complete zero-result metadata queries; anonymous code search separately recorded as an access failure |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0958/Statement.lean` | 0 | exact canonical proposition and checked statement transports re-elaborated |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0958/AnchorAudit.lean` | 0 | Behrend body and mismatch fixture checked; three sorry-free reports; scoped closure 28,257 declarations in 1,079 modules, no bodyless nonaxioms or unsafe declarations |
| `LC_ALL=C TZ=UTC python3 -B Stage1_Instances/THM-M-0958/check_anchor_audit.py` | 0 | pins, blobs, hashes, seven classifications, exact target identity, mismatch, trust boundary, receipt, and packet contract passed |
| `python3 -m json.tool` over the three anchor JSON files and root packet | 0 | all structured artifacts parsed |
| scoped prohibited-construct and whitespace checks | 0 | no prohibited proof device in owned Lean source and no `git diff --check` errors |

The Lean output SHA-256 is
`29005d807865eb32c7af8c3db6641e142e7f0f338ead814ad87667d2ec49ac40`.
The checker also composes the statement and probe sources in a temporary file and confirms by
`rfl` that the audit-local Elkin proposition is definitionally the actual frozen target.

## Open gate

Future proof work must first freeze an obligation tree for Elkin's annulus/shell selection,
concentration and counting estimates, progression-free projection, and asymptotic optimization.
Pinned Behrend lemmas may be reused only as exact typed children; they do not supply the missing
quantitative improvement. Exact root composition, terminal provenance and TCB closure, primary
source `H0`, readable `R0`, hermetic replay, independent verification, and release acceptance all
remain open.
