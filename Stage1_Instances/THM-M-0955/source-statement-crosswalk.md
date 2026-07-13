# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:6973-6978` supplies exactly the title `Bose-Chowla定理`, the
attribution `Bose/Chowla`, year `1960`, gloss `Sidon集的构造`, importance `高`, and status
`已验证`. Git history attributes all six uncited lines to commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record contains no Sidon definition, domain,
parameters, quantifiers, cardinality, bibliography, theorem locator, proof boundary, correction
history, reviewer, or formal artifact.

`Docs/Stage0_Blueprint.md:26038-26063` repeats that gloss while explicitly leaving exact definitions
and premises, proof process, dependencies, equivalent forms, axioms, machine state, and artifact
links open. Its generic statement that a closed result is known is planning metadata, not evidence.
The rev-5.6 manifest retains `已验证` only as untrusted source status and resets the target to
`L0 / rework_required`.

## Primary-source identity lead

Springer and Crossref identify:

> R. C. Bose and S. Chowla, *Theorems in the additive theory of numbers*, Commentarii Mathematici
> Helvetici 37 (December 1962), 141-147, DOI `10.1007/BF02566968`.

The publisher records receipt on 28 March 1962 and summarizes the paper as extending earlier
results on difference sets and `B_2` sequences by Singer, Bose, Erdos and Turan, and Chowla. The
observed publisher HTML had SHA-256
`75b5e6fbd35a72c2b67f381d8b61ef8f391540508bb4d676a9118f96d10b0034`; the observed Crossref
record had SHA-256 `0d1de1cf7f6066174b4c1c5b5b3a8452cb58585b9d48eca20be7c2702a1608ed`.

The publisher exposed only a subscription preview; a direct PDF request returned access HTML, not
a PDF. Therefore no exact numbered theorem, formula, definition, hypothesis, proof passage, or
erratum was transcribed or credited. The 1962 publisher date conflicts with the catalog's 1960
date, for which the repository gives no explanation. The record is a strong `H1` bibliographic
lead, not `H0` source evidence.

## Clause crosswalk

| Catalog component | Source-family question | Prospective Lean surface | Intake result |
|---|---|---|---|
| `Bose-Chowla` | which numbered `B_2` or `B_h` result is the root | one approved proposition or explicit package | exact root open |
| `Sidon` | uniqueness of two-term sums, differences, or unordered multisets | future predicate over a set in an additive group | definition and diagonal policy open |
| `construction` | existential set versus explicit finite-field/logarithm witness | `Exists` with set, cardinality, and property, possibly a construction map | witness interface open |
| parameter | prime or prime power and any exponent `h` | naturals plus primality/prime-power or finite-field data | binders and hypotheses open |
| ambient domain | cyclic group/quotient or integer interval | additive finite group, `ZMod`, or integers | source transport open |
| size and bound | exact size and group order versus lower/asymptotic bound | `Finset.card` and `Fintype.card` equalities/inequalities | conclusion open |
| `1960` | unexplained catalog date | provenance only | conflicts with publisher's 1962 record |
| `已验证` | untrusted inventory label | accepted source and kernel receipts required | no H or M credit |

## Neighbor and substitution boundary

`THM-M-0956`, the immediately following Erdos-Turan construction, has the same catalog gloss
`Sidon集的构造` but distinct attribution and date. The shared gloss does not merge the targets.
Singer difference sets and earlier Erdos-Turan/Chowla results appear in the publisher summary and
reference list only as source-family context; none can silently become this root.

## Lean discovery boundary

At the pinned mathlib revision, a bounded case-insensitive search over pinned mathlib and repository
Lean sources found no occurrence of the precise terms `Sidon`, `Bose-Chowla`, `BhSet`, or `B_h`.
`Mathlib.Combinatorics.Additive.FreimanHom` provides two-term Freiman
interfaces, `Mathlib.Combinatorics.Additive.Energy` counts additive quadruples, and finite-field and
cyclic-group modules provide algebraic substrate. `IntakeProbe.lean` authenticates a small set of
those declarations. None is an exact target or proof, so the machine classification is `M4`.

Before statement work, reviewers must admit and independently inspect an immutable full primary
text, select the exact theorem and definitions, reconcile the date, map every binder, hypothesis,
construction clause, conclusion, boundary case, proof passage, correction, and erratum, and state
what is excluded. Only then can a canonical Lean target and its mutations be frozen.
