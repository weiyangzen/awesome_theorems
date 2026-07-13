# THM-M-0822 statement validation

Item: `S56-M-0822-STATEMENT`

Base revision: `46a0f2a3ea74765a0467c489264b838ffbb70675` (tree
`7b1b5269d7da840fd086da731d6f92903c209c35`). Validation date: 2026-07-13
(`Asia/Shanghai`).

## Selected target

The repository's complete target-bearing gloss is "maximum size of an intersecting family." The
canonical target therefore states a maximum, not merely an upper bound, on the labeled ground set
`Fin n`. For `1 <= r <= n / 2`, a star of `r`-subsets has cardinality
`choose (n - 1) (r - 1)`, and every intersecting `r`-uniform family has at most that cardinality.

This selects the standard uniform specialization supported by the 1961 paper's Theorem 1 and its
following sharpness construction. It does not substitute the broader printed at-most-size
antichain theorem, and it does not add a classification of every equality family. In particular,
the equality boundary `n = 2 * r` is included without claiming all extremizers are stars. Complete
accountable translation, proof mapping, corrections or errata review, independent `H0` review, and
master acceptance remain open.

Families are `Finset (Finset (Fin n))`. Uniformity is `Set.Sized r`; intersection is mathlib's
self-pair `Set.Intersecting`. The positive-rank hypothesis is source-derived and propositionally
important: `sized_intersecting_iff_pairwise` kernel-checks that, under `1 <= r`, this predicate
agrees with distinct-pair intersection. Rank zero is excluded rather than silently identifying the
source's vacuous singleton-empty-family convention with mathlib's convention.

## Lean boundary

The canonical declaration is `Stage1Instances.THM_M_0822.ErdosKoRadoMaximumTarget`. Its only direct
imports are `Mathlib.Combinatorics.SetFamily.Intersecting` and `Mathlib.Data.Finset.Slice`. A
target-only fixture elaborates with the pair and fails after deleting either import. This proves
necessity among the declared imports, not global minimality across all alternative mathlib module
factorizations. The proof-bearing `Mathlib.Combinatorics.SetFamily.KruskalKatona` module is absent.

The module defines the concrete star and kernel-checks its intersection, uniformity, cardinality,
and attainment. A checked iff replaces only the existential witness with this concrete star while
retaining the same universal bound. These elementary witness proofs do not prove the root: the
universal EKR upper bound remains open for the proof and anchor-audit phases.

Four mutations remove intersection from the bound, change the subset carrier, move the universal
family under existential scope, or exclude `r = n / 2`. Lean rejects definitional equality to the
root, and the checker records distinct fully explicit expression fingerprints. These are
statement-identity tests, not claims that every mutation is logically incomparable with the root.

The automation-provided canonical pinned `.lake` link was used read-only. No update, build, clone,
fetch, or dependency mutation was run. This dirty worker evidence is nonrelease evidence.

## Commands and results

Commands ran from the repository root unless another working directory is shown. The two structured
recipes ran with only the recorded `HOME`, `LANG`, and `PATH`; Bubblewrap supplied a fixed root
view and a private network namespace. The root view remained writable because Lake and the checker
need lock and temporary files; dependency cleanliness was checked before and after replay. Exact
finalized hashes and output summaries are recorded in
`statement-receipt.json`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required`. |
| `python3 scripts/stage1_target.py show THM-M-0822` | 0 | Rank 1380, planned, legacy artifacts unaccepted, theorem incomplete. |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | Lean 4.29.0 commit `98dc76e3...`; Lake `5.0.0-src+98dc76e`. |
| pinned mathlib revision/tree/status checks | 0 | Revision `8a178386...`, tree `bdc39a31...`; package worktree clean. |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0822/Statement.lean` | 0 | Canonical and concrete-star targets, star lemmas, checked iff, semantic bridge, three boundaries, four expected identity rejections, axiom reports, and explicit target expression elaborated. |
| `cd Formalizations/Lean && python3 -B ../../Stage1_Instances/THM-M-0822/check_statement.py --worker-packet ../../.stage1-worker-selftest.json` | 0 | Expression SHA-256 `646e9860...e209`; source/receipt/packet invariants passed; four mutations distinct; both import deletions failed; mathlib pin agreed. |
| finalized JSON, prohibited-construct, ownership, and whitespace checks | 0 | Structured artifacts agree; no prohibited construct or whitespace diagnostic was found. |

## Status boundary

This proposal freezes only the exact statement interface. The vector remains `[H1, M3, R4]`.
It supplies no universal EKR upper-bound proof, terminal-body audit, equality classification,
obligation registry, composition certificate, accepted source/readability review, hermetic replay,
independent verification, release decision, or master acceptance. Audit completion and theorem
completion remain false.
