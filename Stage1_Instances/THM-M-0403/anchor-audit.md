# THM-M-0403 formal-anchor audit

Audit item: `S56-M-0403-ANCHOR_AUDIT`. Search cutoff: `2026-07-12`
(Asia/Shanghai). This is a candidate and provenance inventory, not a proof
receipt. The exact root remains
`Stage1.THM_M_0403.SchlickeweiEvertseStatement` in `Statement.lean`.

## Immutable inputs and protocol

The repository base is `72e8a2edc0088f19a59d40d8b64c51a5c9143981`.
The Lake lock pins mathlib to
`8a178386ffc0f5fef0b77738bb5449d50efeea95` (tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`) and `flt-regular` to
`56161b6eb5281fbfe9c38f2bcec0f429ebc11a27`. Checked-out HEADs match
those pins. No dependency was fetched, updated, built, or modified.

Search order was repo-local Lean, every pinned substantive dependency,
mathlib documentation, the immutable Formal Conjectures tree, then public
GitHub repository discovery. Queries included the authors' names, S-unit
equations, the Subspace Theorem, exponential polynomials, nondegenerate
linear recurrences, and finite-rank multiplicative-group equations.

## Candidate ledger

| Candidate | Immutable location | Exact audit | Decision |
|---|---|---|---|
| Legacy target | repository base above; `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_016.lean`; `SimpleNondegenerateZeroFinitenessShape` | Restates the same proposition shape and supplies only definitional and conditional wrappers. The file explicitly records formalization debt; no theorem has this proposition as a proved conclusion. | `M3` statement interface only; no proof credit |
| Pinned mathlib | `mathlib4@8a178386...` | Exact-name/topic searches found no Schlickewei, Evertse, multiplicative-group equation, exponential-polynomial zero-finiteness, or nondegenerate-recurrence theorem. `Mathlib.RingTheory.DedekindDomain.SInteger` supplies S-integer definitions, not the deep finiteness theorem. | Related infrastructure only; root stays `M4` |
| mathlib theorem list | same revision; `docs/1000.yaml`, entries `Q7272898` and `Q7632041` | "Quotient of subspace theorem" and "Subspace theorem" have titles but no `decl` field. | Wishlist rows, not Lean declarations |
| `flt-regular` | `leanprover-community/flt-regular@56161b6...` | Complete Lean/Markdown tree search found no relevant theorem; apparent `S unit` matches are ordinary `IsUnit` syntax. | No candidate |
| Formal Conjectures | `google-deepmind/formal-conjectures@b2e608fc52d765510915a244bb69b1a2741acc3c` | Commit-qualified recursive tree search found no Schlickewei, Evertse, S-unit, recurrence-zero, Skolem-Mahler-Lech, or relevant exponential-polynomial path. | No declaration to inspect or integrate |
| Public repository search | GitHub API at cutoff | Counts for `Schlickewei Lean`, `Evertse Lean`, `S-unit Lean theorem`, `exponential polynomial Lean`, and `nondegenerate linear recurrence Lean` were `0,0,0,1,0`. The sole result was an unrelated P-vs-NP repository. | No credible external Lean candidate |

GitHub code search returned HTTP 401 without authentication, and grep.app
returned HTTP 429. Therefore this is a complete audit of the pinned local
closure and the recorded accessible external protocol, not a claim that no
formalization exists anywhere. There is no actionable repo-local integration
debt: no exact external proof artifact was found to pin or import.

## Primary-source crosswalk

The immutable arXiv version `math/0409604v1` of Evertse, Schlickewei, and
Schmidt (Annals of Mathematics 155 (2002), 807-836) has SHA-256
`3c809fcadaddbc08f57045e4f55562c8a379b5fa33d7e83046b63a9c14766e8f`.
Theorem 1.1 on pages 807-808 proves a uniform finite bound for nondegenerate
solutions of a linear equation in a finite-rank subgroup of `(K*)^n` over a
characteristic-zero field. Pages 811-813 define simple and nondegenerate
recurrences, and Theorem 1.2 gives the simple recurrence zero-set structure;
its final clause gives finiteness for the nondegenerate case.

This is strong human-source support for the selected root, but it is not a
Lean anchor. The published recurrence theorem is stated over an algebraically
closed field, on integer indices, and for order at least three. Closing the
canonical arbitrary-field, natural-index target still requires checked scalar
extension, the one- and two-term cases, injectivity/extraction, and the exact
finite-rank-group reduction. Consequently the source classification is `H1`,
not `H0`.

Evertse's earlier *On sums of S-units and linear recurrences*, Compositio
Mathematica 53 (1984), 225-244, is pinned by NUMDAM item
`CM_1984__53_2_225_0`. Its Theorem 1 (pages 227-228) is the number-field
S-unit input, while pages 228-230 define nondegenerate recurrences and apply
that input. It is historically relevant but narrower than the canonical
characteristic-zero-field claim.

## Validation and boundary

The standard and manifest checks passed, as did the dependency revision and
source searches. Fresh replay of `Statement.lean` with `lake env lean` failed
with `unknown module prefix 'Mathlib'`: the reused canonical `.lake` tree has
the pinned mathlib source checkout but lacks its compiled `Mathlib.olean`
root. Worker policy forbids repairing that by building or fetching. The prior
statement receipt is unchanged; this limitation prevents a fresh elaboration
check but does not turn the negative source inventory into proof evidence.

The anchor-audit node is self-tested. The theorem remains `[H1, M4, R3]` with
`audit_complete=false` and `theorem_complete=false`. The next root cut is a
frozen obligation tree followed by a real Lean proof or a future exact pinned
external closure, then trust, validation, independent-review, and release
gates.
