# THM-M-0487 anchor-audit validation

Item: `S56-M-0487-ANCHOR_AUDIT`

Base revision: `a3b18eec39bf04be025b1641cae02f4d44fdf11a`

Base tree: `fdfff18dea4c6798c5b322b6088dfe556109c134`

Validation date: 2026-07-13 (`Asia/Shanghai`)

## Result

The bounded immutable inventory contains no placeholder-free Lean 4 proof of the frozen weak
Goldbach target. The local declaration is exactly the required proposition but has no proof body.
Pinned mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95` supplies prime predicates,
finite prime sets, prime counting, infinitude, Chebyshev bounds, and divergence of the sum of prime
reciprocals. All ten support declarations re-elaborate in `AnchorAudit.lean`, but none concludes
that every odd natural greater than five is a sum of three primes.

The exact pointwise declaration
`TernaryGoldbachConjecture.ternaryGoldbach` in
`google-deepmind/formal-conjectures@b2e608fc52d765510915a244bb69b1a2741acc3c`
has the required domains, hypotheses, witnesses, and equality. Its terminal body is literally
`by sorry`, so it is rejected as `M5` rather than imported or credited.

The broader search found two additional immutable projects. At
`AlexKontorovich/PrimeNumberTheoremAnd@5754873e8dae73f3b50f8f2b7a4f0b15d4df58aa`,
`Goldbach.odd_conjecture H` is bounded by `Finset.Icc 7 H`; its named Helfgott finite theorem
depends on `e_silva_herzog_piranian_goldbach`, whose body is literally `by sorry`. It is both too
weak for the unbounded target and placeholder-tainted.
`foolishair/Goldbach@751b5ac33d8edc5a7738b0a6ef58ad42f2b15289` has a
target-equivalent `WeakGoldbach` definition under the same Lean and mathlib pins, plus checked split
and assembly lemmas. Its source expressly says the theorem is not yet fully formalized: every
root-returning theorem consumes an open strong-Goldbach, asymptotic, circle-method, all-odd, or
finite premise. Its large native-decide witness corpus is finite and has no bundled contiguous
coverage theorem at its largest displayed value, so it receives no unbounded root credit. At
`lengyijun/goldbach_tm@6cd292062516a0a14ea1b34f2ab75154cae7ab1e`, `Goldbach n` is the
binary two-primes predicate, and the substantive theorems relate binary counterexamples to a
Turing machine halting. That is a different theorem and receives no root credit.

The seven-record frozen inventory is fully classified, but search saturation is not claimed:
authenticated GitHub code search was unavailable, grep.app returned a security checkpoint, and a
broad Sourcegraph `Goldbach` query hit its result limit. The root remains provisionally
`H1/M3/R3`. This worker phase supplies no theorem proof, accepted state, `AUDIT-Z`, or `THEOREM-Z`.

All local validation used the automation-provided canonical `.lake` symlink read-only. No
`lake update`, `lake build`, dependency clone/fetch, checkout, or `.lake` mutation was performed.
One delegated discovery process mistakenly made a shallow `git fetch` into a temporary bare
repository under `/tmp` and immediately removed it. That command did not touch this repository or
`.lake`, and no result from it is admitted anywhere in this inventory. All recorded external
candidate identities come from immutable HTTP raw/tree responses or existing repository evidence.

## Commands and results

Commands ran from the repository root unless a command begins with a parenthesized `cd`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets and ranks 1..1546 passed; every target remains L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0487` | 0 | rank 1366, planned, no accepted legacy artifact, theorem incomplete |
| `git status --short` and `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base IDs above; pre-existing untracked `Formalizations/Lean/.lake` was the only initial status entry |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and `status --short` | 0 | manifest revision `8a178386...ea95`, tree `bdc39a...5c2b`, clean package worktree |
| bounded `rg` alias and structural searches over tracked repository Lean plus every materialized package | 0/1 | only the neighboring eventual-three-primes prose and an unrelated Fermat-number docstring matched broad names; no triple-prime terminal pattern in pinned mathlib |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0487/AnchorAudit.lean)` | 0 | ten pinned support declaration types and the exact audit-local proposition printed; stdout SHA-256 `3080be75...f16` |
| Sourcegraph query `TernaryGoldbach` with archives/forks | 0 | completed with six matches in two repositories: Formal Conjectures and a dataset mirror; response SHA-256 `075a541a...052` |
| Sourcegraph queries for `WeakGoldbach`/`weak Goldbach` and `sum of three primes` with archives/forks | 0 | both completed with zero matches and no skips; response SHA-256 values `54f21e6e...1e0` and `c313f1f4...9dc` |
| Sourcegraph broad `Goldbach` Lean query | 0 | 100 results in four repositories; result-limit warning retained, so it is not negative or saturation evidence; response SHA-256 `11433661...a35` |
| GitHub REST repository query for weak/ternary Goldbach Lean | 0 | complete metadata response with `total_count=0`; SHA-256 `08c082fd...00b` |
| GitHub REST repository query `Goldbach language:Lean` | 0 | complete response with 11 repositories; identified foolishair/Goldbach and other binary/conditional surfaces; SHA-256 `a92e63d0...6ec` |
| GitHub REST repository query `goldbach lean` | 0 | complete response with seven repositories; independently identified foolishair/Goldbach for immutable follow-up; SHA-256 `1aa1cd7e...fb1` |
| GitHub REST code query for exact aliases and phrase | 0 transport / HTTP 401 | authentication blocker recorded; response SHA-256 `b7dbd173...29e`; no negative claim |
| grep.app query for `TernaryGoldbach` | 0 transport / HTTP 429 | Vercel Security Checkpoint recorded; response SHA-256 `824d4633...0c6`; no negative claim |
| immutable Formal Conjectures tree and raw source inspection | 0 | non-truncated 1204-entry tree; one Goldbach path; exact declaration's literal placeholder rejected; tree response SHA-256 `76fa3f96...c61`, source SHA-256 `bf6a587c...447` |
| immutable PrimeNumberTheoremAnd tree, source, toolchain, manifest, and license inspection | 0 | non-truncated 290-entry tree; finite-only definitions and placeholder ancestry classified; tree response SHA-256 `79f8bb83...655`, source SHA-256 `b56f95aa...29e` |
| immutable goldbach_tm tree, README, Basic, Tm25 Content, toolchain, manifest, and license inspection | 0 | non-truncated 36-entry tree; binary-Goldbach Turing-machine mismatch classified; tree response SHA-256 `f6cb7b75...54f` |
| immutable foolishair/Goldbach codeload archive and source/pin/license inspection | 0 | 14-entry archive at full commit; exact-equivalent definition but conditional architecture only; archive SHA-256 `23cc8f4e...8de`, source SHA-256 `0958db8b...07` |
| delegated temporary bare-repository fetch under `/tmp` | invalid and discarded | process violation isolated outside the repository and `.lake`; temporary repository removed; no result admitted as evidence |
| `python3 -B Stage1_Instances/THM-M-0487/check_anchor_audit.py` | 0 | manifest/DAG identity, fingerprints, immutable pins, seven candidates, search limits, packet/receipt, and narrow Lean replay agreed |
| `python3 -m json.tool` on all new JSON artifacts | 0 | every artifact parsed |
| scoped prohibited-construct scan over `AnchorAudit.lean` | 1 (expected no match) | no proof escape, bodyless declaration, unsafe/oracle, or placeholder in the owned Lean probe |
| `git diff --check -- Stage1_Instances/THM-M-0487 .stage1-worker-selftest.json` | 0 | no whitespace diagnostics |

## Open integration gate

Retry root integration only with a concrete immutable Lean 4 candidate whose exact type or checked
transport, terminal body, transitive placeholders and axioms, unsafe/oracle boundary, dependency
graph, toolchain, license, and local replay can all be verified. A bounded finite result, binary
Goldbach equivalence, statement-only declaration, or placeholder body cannot satisfy this gate.
