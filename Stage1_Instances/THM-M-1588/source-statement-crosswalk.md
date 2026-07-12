# Source-statement crosswalk

## Repository records

`Docs/researches/math_theorems.md:11700-11705` supplies exactly the title
`Gilbert-Varshamov界`, attribution Gilbert/Varshamov, year 1952, the gloss `码的存在性下界`,
importance "high," and status `已验证`. Git history attributes all six uncited lines to commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record has no bibliography, theorem locator,
formula, alphabet, code definition, parameter range, proof, correction history, reviewer, or
formal artifact.

`Docs/researches/cs_theorems.md:616` independently repeats the same title, attribution, gloss,
importance, and untrusted status, but dates it 1952-57. Stage0 projects this row as `THM-C-0372`,
outside Stage1 rev-5.6. The date difference is consistent with multiple historical contributions,
but does not tell us which statement the mathematical target selects.

`Docs/Stage0_Blueprint.md:43174-43199` repeats the mathematical gloss while explicitly leaving the
formal system, exact definitions and premises, proof history, dependencies, equivalent forms,
axioms, machine status, and artifact links open. Its generic claim that a closed result is known is
planning metadata, not source evidence. Rev-5.6 preserves `已验证` only as
`source_status_untrusted` and resets the target to `L0 / rework_required`.

## Literal crosswalk

| Catalog element | Necessary mathematical component | Prospective Lean component | Intake status |
|---|---|---|---|
| `Gilbert-Varshamov界` | one historical or modern finite/linear/asymptotic bound | one exact `Prop` with checked relationships to alternates | family only; variant open |
| "code" | subset of words, linear subspace, or another code object | finite set/submodule plus membership and cardinality | object and alphabet open |
| "existence" | an existential code or nonconstructive maximum-size lower bound | explicit `Exists` or inequality for a defined extremal function | conclusion form open |
| "lower bound" | numerator, ball-volume denominator, radius and rounding convention | finite sums, binomial coefficients, powers, division/ceilings | formula absent |
| Gilbert/Varshamov | separate historical constructions and theorem families | source IDs and node-level provenance | attribution is not a statement |
| 1952 versus 1952-57 | catalog provenance discrepancy | no proof-level meaning | must be reconciled, not guessed |
| `已验证` | untrusted inventory field | source proof and kernel receipt would be required | no H or M credit |

## Inspected Gilbert primary source

E. N. Gilbert, *A Comparison of Signalling Alphabets*, *Bell System Technical Journal* 31(3)
(May 1952), pages 504-522, DOI `10.1002/j.1538-7305.1952.tb01393.x`, was inspected in a scan of
the complete issue. The scan identifies the manuscript date as March 24, 1952. Printed pages
506-507 define a binary length-`D` `k`-error-correcting alphabet by pairwise difference in at least
`2k + 1` positions, define `K_0(D,k)` as its maximum size and `N(D,k)` as the number of binary words
within Hamming radius `k`, and state Theorem 1:

```text
2^D / N(D, 2k) <= K_0(D, k) <= 2^D / N(D, k).
```

The proof of the lower inequality greedily selects words and observes that, after `r` choices, at
least `2^D - r N(D,2k)` words remain outside the forbidden radius-`2k` neighborhoods. Printed
pages 510-511 then derive a separate large-alphabet rate theorem using a binomial-tail estimate and
Stirling asymptotics. These are related but distinct possible source nodes.

This is strong discovery evidence and supports provisional H1 rather than H0. The repository does
not cite or select this paper; the scan was not added to the repository; its copyright and durable
archive policy require integration review; OCR is not a canonical transcription; the exact natural
number interpretation of displayed fractional inequalities, all incorporated definitions and
boundary cases, errata, and an independent premise-to-target review remain open. The observed
complete-issue PDF SHA-256 and the text-extract digest are recorded in `instance.json` and the
provisional receipt.

## Varshamov and modern-family boundary

A bibliographic lead commonly cites R. R. Varshamov, *Estimate of the number of signals in
error-correcting codes* (English title), *Doklady Akademii Nauk SSSR* 117 (1957), pages 739-741.
The associated linear q-ary form is commonly stated as existence of a linear `[n,k,d]_q` code when
`q^(n-k)` is greater than the sum of `binom(n-1,i)(q-1)^i` for `i = 0,...,d-2`. This is recorded
only to distinguish the candidate family. No authoritative DOI was found, and the Russian primary
text, title translation, theorem locator, exact inequality, proof, and corrections were admitted or
inspected in this worker intake. None of those details receives source credit.

Likewise, a modern finite q-ary denominator through `d - 1` and the asymptotic entropy expression
`R_q(delta) >= 1 - H_q(delta)` are candidate descendants, not verbatim statements from the
inspected Gilbert pages. Their equivalence or implication relationships would require selected
definitions, parameter ranges, rounding lemmas, asymptotic analysis, and checked transports.

## Source gate

Before H0 or statement acceptance, accountable reviewers must select one exact root, preserve
lawful immutable copies of every primary source used, record edition/issue/page/theorem and errata,
transcribe all incorporated definitions, ordered binders, hypotheses, conclusion, rounding and
boundary conventions, reconcile Gilbert and Varshamov contributions and the `THM-C-0372` duplicate,
map every material premise and proof step, and approve the source-to-Lean crosswalk. Until then the
canonical mathematical statement and formal expression remain null.

## Lean discovery boundary

The pinned probe checks `hammingDist`, `hammingDist_triangle`,
`hammingDist_le_card_fintype`, `Hamming`, `Hamming.dist_eq_hammingDist`, `Fintype.card_fun`,
`Nat.choose`, and `Finset.exists_max_image`. These authenticate useful finite Hamming substrate,
not a code object, minimum-distance extremal function, covering argument, linear Varshamov theorem,
or asymptotic entropy result. No declaration or proof body is credited.
