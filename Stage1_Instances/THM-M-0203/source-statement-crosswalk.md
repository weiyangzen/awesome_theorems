# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:1464-1469` supplies exactly the title `海伦公式`, attribution to
Heron of Alexandria, approximate date 60 CE, gloss `三角形面积与三边关系` ("the relationship between
a triangle's area and its three sides"), medium importance, and formalization status `已验证`.
Git history places all six uncited lines in commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`.

`Docs/Stage0_Blueprint.md:5644-5669` repeats the gloss while explicitly leaving the formal system,
foundation, exact definitions and premises, proof route, dependencies, equivalent forms, axioms,
machine status, and artifact links open. The rev-5.6 manifest retains `已验证` only as untrusted
metadata and resets the item to `L0 / rework_required`.

Neither record contains a bibliography, edition, book/proposition/page locator, formula, area or
triangle definition, ordered binders, hypotheses, proof boundary, translation, correction history,
errata, or reviewer. They establish catalog identity only.

## Human-source boundary

The title and attribution make Heron's *Metrica* a primary-source lead, but no Greek text, critical
edition, translation, exact proposition and proof, archival identifier, correction history, or
errata was inspected and admitted in this intake. The catalog's approximate date also lacks a cited
genealogical source. Consequently the provisional human classification is `H1`, not `H0`: a
classical complete theorem family is known, while its exact source-to-catalog statement and
assumptions remain unaudited.

Before H0 can be proposed, an accountable reviewer must preserve a lawful immutable edition,
identify the exact book/proposition/page or archival locator, transcribe every incorporated
definition and assumption, map the conclusion and proof boundary, audit translation, historical
attribution, corrections and errata, list dependent source IDs, and independently approve the
crosswalk.

## Clause crosswalk

| Repository component | Conventional family component | Prospective Lean surface | Intake assessment |
|---|---|---|---|
| `三角形` / triangle | three Euclidean vertices or three valid side lengths | affine points and `dist`, or real lengths plus triangle inequalities | domain, dimension, and nondegeneracy open |
| `面积` / area | nonnegative triangle area | determinant/orientation form, measure, or `1 / 2 * a * b * sin gamma` | no definition selected |
| `三边` / three sides | nonnegative lengths `a`, `b`, `c` | three pairwise distances with a fixed vertex order | ordering and transport open |
| relationship | conventional `area = sqrt(s(s-a)(s-b)(s-c))` | real equality using `Real.sqrt` | formula absent from repository; candidate only |
| semiperimeter | `s = (a+b+c)/2` | local `let` or explicit binder | not mentioned by repository |
| assumptions | ordinary Euclidean triangle | distinctness, noncollinearity, or triangle inequalities | entirely absent |
| `已验证` | untrusted inventory label | exact expression and accepted receipt would be required | no H or M credit |

## Pinned Lean candidate

Pinned mathlib contains `Archive/Wiedijk100Theorems/HeronsFormula.lean`, whose documentation calls
it Freek number 57 and whose declaration is mapped by `docs/100.yaml:228-231`:

```text
Theorems100.heron
```

For affine points `p1 p2 p3`, it assumes `p1 != p2` and `p3 != p2`, lets
`a = dist p1 p2`, `b = dist p3 p2`, `c = dist p1 p3`, and `s = (a+b+c)/2`, then proves

```text
1 / 2 * a * b * sin (angle p1 p2 p3)
  = sqrt (s * (s-a) * (s-b) * (s-c)).
```

The candidate source has SHA-256
`fc81c1b1a23ff20f5b008d9ee5dcc09abc46ab3cb3e014320c8513bf3cff1d9f` and Git blob
`dc5447dc92b44d441c274c6a88a29eb319bc84dd` at pinned revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. Direct read-only elaboration of that pinned source
with `lake env lean` succeeds without changing the clean mathlib package source. The proof derives
the formula from the cosine rule, the nonnegativity of the resulting numerator, square-root
identities, and ring normalization; it contains no placeholder declaration.

This remains candidate-only evidence. The catalog does not select the candidate's trigonometric
area expression, its two distinctness hypotheses, affine generality, point order, or degenerate
scope. The canonical cache also has no compiled `Archive` object, so repo-local import closure is
not yet demonstrated and no build was run. Exact target identity, human-source fidelity,
proof-body provenance, dependencies, axioms, TCB, and trust acceptance belong to later gates.

## First source and statement gate

An independent source reviewer must admit one immutable exact human proposition and approve every
definition, premise, conclusion, proof boundary, translation, attribution, correction, and erratum.
The statement phase must then fix the area encoding, ambient domain, binders, side order,
nondegeneracy, semiperimeter and square-root conventions, equality form, and boundary cases; compile
checked transports for every credited alternate; serialize the elaborated expression and
environment; and pass the required removed-hypothesis, changed-domain, binder-scope, and
boundary-case mutations.
