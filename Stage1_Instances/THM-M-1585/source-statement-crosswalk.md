# THM-M-1585 source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:11679-11684` contains exactly:

- title: `编码理论` (coding theory);
- proposer: `众多数学家` (many mathematicians);
- time: `20世纪` (20th century);
- statement gloss: `纠错码的理论` (the theory of error-correcting codes);
- importance: high; and
- formalization status: `已验证` (verified).

All six lines originate at repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. They contain no citation, mathematical formula,
theorem locator, domain, ordered binders, hypotheses, conclusion, proof, formal declaration, or
validation link. The Stage0 projection at `Docs/Stage0_Blueprint.md:43093-43118` repeats the gloss
and explicitly leaves exact definitions and premises, proof route, dependencies, equivalent forms,
axioms, machine status, and artifact links open. Under rev-5.6, `已验证` is untrusted metadata.

## Literal crosswalk

| Repository phrase | What it establishes | Missing exact-statement component | Intake result |
|---|---|---|---|
| `编码理论` | a subject label | one named truth-valued result and scope | open |
| `纠错码的理论` | an error-correcting-code topic boundary | code/channel/error model, binders, hypotheses, conclusion | open |
| `众多数学家` | no accountable source identity | author/work/edition/theorem/page and reviewer | open |
| `20世纪` | only a broad historical range | immutable source revision and result date | open |
| `高` | catalog importance | no mathematical premise or conclusion | no proof relevance |
| `已验证` | catalog inventory status only | source fidelity, kernel evidence, trust and receipt | explicitly untrusted |

There is no clause to map to an ordered binder, hypothesis, or conclusion. The canonical human
claim and Lean expression therefore remain null rather than silently selecting a theorem.

## Taxonomy crosswalk, not a theorem source

`Docs/researches/cs_theorems.md:610-638` has no row asserting a theorem named merely coding theory.
Instead, its coding-theory and error-correcting-code sections enumerate Hamming, Singleton,
Gilbert-Varshamov, Plotkin, Johnson, Elias, MRRW, duality, MacWilliams, algebraic-geometric,
Hamming-code, Reed-Solomon, BCH, convolutional, Turbo, LDPC, Polar, Reed-Muller, Golay, and
list-decoding topics. This confirms that the umbrella phrase ranges over materially different
claims. It does not authorize selecting or conjoining any of them for `THM-M-1585`.

## Candidate source-to-statement rows

| Candidate family | Components a source must fix | Lean obligations if selected | Current boundary |
|---|---|---|---|
| finite extremal bound | alphabet, length, code, distance, size, radius, rounding | finite words/code, balls, cardinalities, inequality | owned by named neighbors unless separately approved |
| algebraic code construction | field, length, generator/check data, dimension, distance | finite-field modules, encoder, parameters | named code families separately cataloged |
| decoder guarantee | channel/error pattern, encoder, decoder, success criterion | executable or relational decoder and soundness | catalog supplies none |
| uniquely decodable source code | finite alphabet, variable-length words, decipherability | word/list code, concatenation, length inequality | adjacent mathlib result is not error-correcting umbrella root |
| asymptotic coding theorem | code family, rate/distance/channel, probability and limits | indexed families, logarithms, limits, existence/converse | overlaps Shannon/capacity and bound targets |

These rows are a resolution checklist for a corrected target, not inherited theorem clauses.

## Pinned formal substrate

The bounded intake search used pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. Relevant declarations include:

- `hammingDist`, `hammingDist_triangle`, and `Hamming.dist_eq_hammingDist` in
  `Mathlib.InformationTheory.Hamming`;
- `InformationTheory.UniquelyDecodable` and
  `InformationTheory.UniquelyDecodable.flatten_injective` in
  `Mathlib.InformationTheory.Coding.UniquelyDecodable`; and
- `InformationTheory.kraft_mcmillan_inequality` in
  `Mathlib.InformationTheory.Coding.KraftMcMillan`.

`IntakeProbe.lean` elaborates those exact interfaces and prints axioms for representative theorems.
A bounded lexical search of pinned mathlib and repository-local Lean found the adjacent Hamming and
source-code files but no general error-correcting theorem called coding theory. The checked APIs
give only discovery evidence. They do not select a canonical root, transfer a neighbor's statement,
or supply any usable artifact or proof credit for `THM-M-1585`; the search is not the later
exhaustive anchor audit.

## Gate result

Human status is provisionally `H5` because the received catalog wording is not one stable
proposition. Machine status is `M4` because no usable formal artifact can match a canonical
expression or source-identical root that has not been selected. Readability status is `R4` because this boundary
map is not a proof reconstruction. Retry requires an accountable immutable source, independent
review, exact target correction, and explicit resolution of every proposition-changing row before
statement elaboration.
