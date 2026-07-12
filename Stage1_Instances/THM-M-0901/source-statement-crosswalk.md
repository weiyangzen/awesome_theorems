# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:6593-6598` supplies exactly the title `拉丁方` (Latin squares), the
attribution `众多数学家` (many mathematicians), `20世纪` (twentieth century), the gloss
`拉丁方的存在性与计数` (existence and counting of Latin squares), importance `高` (high),
and status `已验证` (verified). All six lines originate in repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record contains no formula, order range,
definitions, binders, hypotheses, conclusion, bibliography, proof boundary, correction history, or
formal artifact.

`Docs/Stage0_Blueprint.md:24575-24600` repeats those fields and explicitly leaves the formal system,
foundation, precise definitions and premises, proof history and dependencies, equivalent forms,
axioms, machine state, and artifact links open. Its generic tree and leaf-budget text is planning
metadata. The rev-5.6 manifest preserves `已验证` only as `source_status_untrusted` and resets
the target to `L0 / rework_required`.

## Literal crosswalk

| Repository element | Mathematical component to freeze | Prospective Lean component | Intake result |
|---|---|---|---|
| `拉丁方` | finite square array and row/column symbol condition | a matrix or binary operation plus exact bijectivity predicates | family identified; representation and boundary conventions open |
| `存在性` | order range, construction or completion problem, and exact existential conclusion | for example, a quantified `Nonempty` subtype after its definition is frozen | materially ambiguous; no source root selected |
| `计数` | total, reduced, quotient, exact-value, formula, bound, or asymptotic count | `Fintype.card` of a concrete subtype or quotient with checked finiteness | materially different claims; no count selected |
| many mathematicians / twentieth century | historical provenance | pinpoint edition and source-to-node ledger | too broad for proof-source credit |
| `已验证` | untrusted inventory metadata | no proposition or proof term | explicitly rejected as H or M evidence |

## Inspected counting-source lead

Brendan D. McKay and Ian M. Wanless, *On the Number of Latin Squares*, *Annals of
Combinatorics* 9(3) (2005), pages 335-344, DOI `10.1007/s00026-005-0261-7`; author version
arXiv `0909.2101v1`. The inspected PDF SHA-256 is
`890c1b8bac1d7ffff1cb8275040eed37b608a4708f6cebc64cf8ac143fcb0d80`.

Printed page 1 defines a `k x n` Latin rectangle for `1 <= k <= n` as an array over
`{1,...,n}` whose entries in every row and column are distinct; a Latin square has `k = n`; a
reduced rectangle has the first row and column in natural order. It distinguishes reduced counts
`R_(k,n)` from total counts `L_(k,n)` and relates them. Printed page 3, Theorem 1 gives graph and
1-factorization formulas for reduced rectangle and square counts. Printed page 7, Theorem 3 gives
a separate permanent-based formula for the total number `L_n`. Printed page 2 states that even the
asymptotic value of `R_n` was unknown at writing.

This source is a strong definition and counting-family lead, but not `H0`: the catalog does not cite
it, choose one of its several results, or say whether its existence and counting words form a
conjunction. Its definitions, formulas, computation boundary, errata, and complete proof nodes have
not been independently reviewed. Selecting only Theorem 3 would drop the existence half; adjoining
an unrelated group-table construction would invent a compound root.

## Existence-source lead

Crossref metadata identifies Marshall Hall, *An existence theorem for latin squares*, *Bulletin of
the American Mathematical Society* 51(6) (1945), pages 387-388, DOI
`10.1090/S0002-9904-1945-08361-X`. Only bibliographic metadata was verified. The theorem text,
incorporated definitions, scope, proof, and errata were not successfully inspected, so no claim from
that paper is quoted or credited. Its title alone cannot determine what the catalog means by
`existence`.

## Neighbor and substitution boundary

The repository separately owns `THM-M-0902` for Euler's orthogonal-Latin-square conjecture and
`THM-M-0903` for its Bose-Shrikhande-Parker negation. The inspected McKay-Wanless source also
distinguishes labelled, reduced, isomorphism, isotopy, and main-class counts. These records show why
the catalog gloss is not one proposition; they do not authorize a cross-target merge or an arbitrary
choice of counting convention.

## Source gate

Before statement acceptance, accountable reviewers must preserve and hash lawful immutable source
editions, decide whether the target is one proposition or a package with separate roots, select the
exact existence and/or counting result, transcribe every incorporated definition, ordered binder,
hypothesis, conclusion, exceptional case, computation boundary, and proof boundary, inspect
corrections and errata, map material proof nodes, and independently approve the source-to-Lean
crosswalk. Until then the canonical statement and expression remain null.
