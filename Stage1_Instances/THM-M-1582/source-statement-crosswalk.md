# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:11658-11663` supplies exactly the title
`Kolmogorov复杂度`, Andrey Kolmogorov, 1963, the gloss `对象的最小描述长度`, importance `high`,
and status `已验证`. Git history places all six uncited lines in commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`.

`Docs/Stage0_Blueprint.md:43012-43037` repeats those fields while explicitly leaving precise
definitions and premises, proof history, dependencies, equivalent forms, axioms, machine status,
and artifact links open. The rev-5.6 manifest preserves `已验证` only as
`source_status_untrusted` and resets the target to `L0 / rework_required`.

The repository record contains no truth-valued conclusion, computational model, object/program
domain, encoding, description method, complexity variant, additive-constant convention, binder,
hypothesis, bibliography, theorem locator, proof boundary, correction history, or reviewer. It
therefore does not identify an exact proposition.

## Inspected primary source

A. N. Kolmogorov, *Three Approaches to the Definition of the Concept "Quantity of Information"*,
*Problemy Peredachi Informatsii* 1(1) (1965), pages 3-11, is the mature primary source. MathNet.Ru
identifies the original as Russian, received 9 January 1965, with MathSciNet record MR184801 and
Zentralblatt record 0271.94018. The nine-page MathNet.Ru scan inspected on 2026-07-13 has SHA-256
`77a10807916f52dd48d5eac07e26fd471738f47b6307f3259c3b1787052abab8`.

Section 3 defines a numbered countable object domain and conditional complexity `K_phi(y | x)` as
the minimum length of a program `p` for which a partial recursive description method
`phi(p, x)` outputs `y`, with infinity when no such program exists. Its main theorem states that
there is a partial recursive method `A` such that for every partial recursive method `phi`,

```text
K_A(y | x) <= K_phi(y | x) + C_phi,
```

where `C_phi` is independent of `x` and `y`. The proof uses a universal partial recursive function
and pairs the index of `phi` with its program. The paper calls such an `A` asymptotically optimal
and derives that two optimal methods give complexities differing by a bounded additive constant.

An English translation, *Three approaches to the quantitative definition of information*, appears
in *International Journal of Computer Mathematics* 2 (1968), pages 157-168, DOI
`10.1080/00207166808803030`. The translation was located bibliographically but was not admitted as
a complete inspected source or checked against the Russian scan.

The 1965 source strongly identifies a coherent correction candidate. It does not authorize this
worker to replace the catalog's 1963 concept gloss with that theorem, clear `H0`, or claim a
translation, correction, assumption, and independent-review audit.

## 1963 source boundary

Kolmogorov's *On Tables of Random Numbers*, *Sankhya: The Indian Journal of Statistics, Series A*
25(4) (1963), pages 369-376, is a genuine precursor matching the catalog year. An authorized
reprint appears in *Theoretical Computer Science* 207(2) (1998), pages 387-395, DOI
`10.1016/S0304-3975(98)00075-9`.

The 1965 paper cites the 1963 article as an incomplete presentation of using complexity to
characterize random elements of large finite sets. The 1963 source motivates an algorithmic
complexity measure but is not the inspected source of the mature shortest-program definition and
main optimality theorem. The catalog's year and gloss therefore combine distinct historical
stages and require an accountable correction rather than silent normalization.

## Component crosswalk

| Repository element | Source component | Prospective Lean surface | Intake assessment |
|---|---|---|---|
| `Kolmogorov复杂度` | 1965 Section 3 conditional and unconditional complexity | one source-selected definition plus one exact root `Prop` | concept family only |
| `对象的最小描述长度` | minimum program length for a partial recursive method | program strings, length, partial evaluator, minimum with no-description convention | definition gloss, not a conclusion |
| Andrey Kolmogorov / 1963 | 1963 random-table precursor | immutable source and historical provenance | date does not locate the mature theorem |
| optimality/invariance | 1965 main theorem and bounded-difference corollary | universal evaluator/compiler plus additive bound | strong correction candidate, not catalog-selected |
| `已验证` | untrusted inventory label | reviewed H evidence and kernel receipt would be required | no H or M credit |

## Neighbor and duplicate boundaries

`THM-M-1583` is the broader algorithmic-information-theory target and `THM-M-1584` concerns a
Chaitin number. Stage0-only `THM-C-0392` repeats the Kolmogorov-complexity title with the different
gloss `算法信息论基础`, while `THM-C-0393` separately lists incompressibility. Those records confirm
that the invariance theorem, broad theory, Chaitin result, and counting application must not be
merged or share proof credit by default.

Computability targets `THM-M-0715` through `THM-M-0718` can supply definitions or bridges only;
they are not the shortest-description result.

## Lean discovery boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the intake probe checks
`Computability.Encoding`, `Computability.FinEncoding`, `Computability.finEncodingNatBool`,
`Nat.Partrec.Code`, `Nat.Partrec.Code.eval`, `Nat.Partrec.Code.exists_code`, `Turing.FinTM2`,
`Turing.TM2Outputs`, and `Turing.TM2Computable`. These authenticate adjacent encodings,
partial-recursive programs, evaluation, and Turing semantics only. A bounded exact-topic search
found no Kolmogorov-complexity or shortest-program declaration in pinned mathlib or repo-local
Lean.

No canonical module, expression, expression hash, checked transport, or statement mutation is
credited. The probe and search are not an exhaustive candidate audit or a global absence proof.

## Source and statement gate

Before ordinary theorem execution, accountable reviewers must correct or select one stable
truth-valued proposition; preserve lawful immutable copies of every source used; record the exact
edition, section, page, incorporated definitions, proof boundary, translation, corrections, and
errata; reconcile 1963 with 1965 and the neighboring records; and independently approve every
source-to-target row. The statement phase must then freeze minimal imports, the elaborated
expression and environment fingerprint, checked model/encoding transports, and removed-hypothesis,
changed-domain, binder-scope, and boundary mutations.

Until then, `H5` records that the received catalog wording is not one stable proposition. It does
not refute the 1965 theorem. The canonical mathematical and Lean targets remain null.
