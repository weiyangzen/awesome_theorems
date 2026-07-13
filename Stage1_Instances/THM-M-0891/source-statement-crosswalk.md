# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:6523-6528` records the title "Wilf theorem", Herbert Wilf, 1967,
the gloss "a spectral lower bound for the chromatic number", high importance, and `已验证`. Git
history places all six uncited lines in commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`.

`Docs/Stage0_Blueprint.md:24305-24330` repeats the gloss while leaving the formal system, exact
definitions and hypotheses, proof route, dependencies, equivalent formulations, axiom policy,
machine status, and artifact links open. The rev-5.6 manifest preserves `已验证` only as untrusted
metadata and resets this target to `L0 / rework_required`.

## Primary bibliographic lead

Crossref and OpenAlex metadata identify H. S. Wilf, *The Eigenvalues of a Graph and Its Chromatic
Number*, Journal of the London Mathematical Society s1-42(1) (1967), pages 330-332, DOI
`10.1112/jlms/s1-42.1.330`. Crossref records the author, title, year, journal, volume, issue, and page
range. OpenAlex and Unpaywall report closed access and no open repository copy. The publisher DOI
route returned an access challenge, and its text-mining PDF endpoint returned HTTP 400.

This is a strong historical and lexical match, but only a bibliographic lead. The primary theorem
text, ordered assumptions, equality clause, definitions, proof boundary, and correction history
were not inspected from a lawful immutable edition. It therefore cannot support `H0`.

## Versioned modern corroboration

Thiago Assis, Gabriel Coutinho, and Emanuel Juliano, *Spectral upper bounds for the Grundy number
of a graph*, arXiv `2401.03042v2` (2024), printed page 2, states after defining the adjacency
eigenvalues that Wilf showed

```text
chi(G) <= 1 + lambda_1(G),
```

and reports equality exactly for a complete graph or an odd cycle. Reference [15] on printed page
12 points to Wilf's 1967 paper and page range. The inspected PDF has SHA-256
`59e61f62eed77b712aaef5bbebe6a255ba43077cd1ca1ddecb2422aaf23adbbd`.

This source is useful statement-family corroboration, not a primary-source substitute. It does not
resolve whether connectedness is implicit, how disconnected equality cases are phrased, or whether
the catalog intends the inequality, its rearrangement, or a different spectral lower bound.

## Component crosswalk

| Repository or source element | Prospective Lean surface | Intake assessment |
|---|---|---|
| graph `G` | `G : SimpleGraph V` with finite vertex data and decidable adjacency | credible model candidate; exact carrier and instances open |
| chromatic number `chi(G)` | `G.chromaticNumber : ENat`, or `ENat.toNat` under finite colorability | pinned API exists; cast and minimum convention open |
| adjacency matrix `A(G)` | `G.adjMatrix Real` | pinned finite-matrix API exists |
| largest adjacency eigenvalue `lambda_1(G)` | a maximal entry of `(G.isHermitian_adjMatrix Real).eigenvalues` or `eigenvalues0` | ordering and nonempty index boundary open |
| `chi(G) <= 1 + lambda_1(G)` | real-cast inequality after selecting a natural chromatic number | secondary statement lead only; primary admission open |
| `lambda_1(G) >= chi(G) - 1` | checked algebraic transport from the selected inequality | candidate equivalent orientation, not automatically canonical |
| equality iff complete or odd cycle | graph-isomorphism predicates plus an odd cycle-length witness | candidate clause; connected/disconnected and small-case scope open |
| catalog `色数的谱下界` | direction discriminator, not a formula | conflicts with or ambiguously describes the common Wilf orientation |
| catalog `已验证` | no Lean declaration or proof object | explicitly rejected as evidence |

## Lean discovery boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the intake probe checks
`SimpleGraph.Colorable`, `SimpleGraph.chromaticNumber`, `SimpleGraph.adjMatrix`, Hermitian adjacency,
ordered Hermitian eigenvalues, graph connectedness, and complete graphs. A bounded exact-topic
search found only the unrelated Fine-Wilf periodicity lemma; no Wilf spectral-coloring declaration
was located in repo-local or pinned-mathlib Lean sources.

These observations establish adjacent representation infrastructure only. They are not the
downstream precommitted exhaustive anchor audit and supply no statement fingerprint or proof credit.

## Required source admission

Before leaving `H1`, accountable reviewers must preserve and hash a lawful immutable primary
edition, transcribe the exact theorem and any incorporated definitions, map every premise and
conclusion, identify the proof boundary, audit corrections or errata, decide the relationship to
the modern inequality/equality report, and independently approve the mapping. Only then may the
statement phase freeze minimal imports, the exact Lean expression, checked transports, expression
and environment fingerprints, and the required mutation suite.
