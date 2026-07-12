# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:10118-10123` supplies exactly the title `Weyl渐近公式`, Hermann
Weyl, 1911, the gloss `特征值的渐近分布`, importance "high," and status `已验证`. The complete
six-line block has SHA-256 `7ed3e16bc0fbe88bf178b2433a20f132bcd80738e20097c992a4172b00dcb956`.
Git history attributes all six uncited lines to repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record has no bibliography, formula, definition,
binder, hypothesis, conclusion, proof boundary, correction history, reviewer, or formal artifact.

`Docs/Stage0_Blueprint.md:37776-37802` repeats the gloss while explicitly leaving the formal system,
foundation, exact definitions and premises, proof process, dependencies, equivalent forms, axioms,
machine status, and artifact links open. Rev-5.6 preserves `已验证` only as untrusted source
metadata and resets the target to `L0 / rework_required`.

## Literal crosswalk

| Repository element | Possible mathematical component | Prospective Lean component | Intake assessment |
|---|---|---|---|
| `Weyl渐近公式` | a leading spectral counting/eigenvalue asymptotic, or a stronger Weyl expansion | one source-selected exact `Prop` | recognizable family, exact root open |
| "eigenvalues" | an infinite discrete spectrum ordered with multiplicity | an operator plus source-defined enumeration or counting function | operator and enumeration absent |
| "asymptotic distribution" | equivalence or normalized limit along an unbounded spectral parameter/index | `Asymptotics.IsEquivalent`, `Tendsto`, filters, coercions, and exact constant | variable, normalization, exponent, and conclusion absent |
| Hermann Weyl / 1911 | historical provenance, possibly announcement chronology | immutable edition and exact result/page mapping | strong lead, but catalog locator absent |
| ODE category | possible Sturm-Liouville specialization | interval operator, coefficients, endpoint conditions, and indexed eigenvalues | conflicts with the classic PDE source lead |
| `已验证` | untrusted inventory field | accepted source proof and kernel receipt would be required | no proof credit |

## Historical source lead

Crossref identifies Hermann Weyl, "Das asymptotische Verteilungsgesetz der Eigenwerte linearer
partieller Differentialgleichungen (mit einer Anwendung auf die Theorie der Hohlraumstrahlung),"
*Mathematische Annalen* 71 (1912), 441-479, DOI `10.1007/BF01456804`. This is a strong primary-
source lead matching the attribution and spectral-asymptotics family. Its title explicitly concerns
linear partial differential equations, whereas the catalog places `THM-M-1389` under ordinary
differential equations and gives the date 1911. Bibliographic metadata also exposes Weyl's later
"Ueber die Randwertaufgabe der Strahlungstheorie und asymptotische Spektralgesetze," 1913,
177-202, DOI `10.1515/crll.1913.143.177`, as related chronology rather than a selected root.

These records discriminate the family but do not make either paper canonical or establish `H0`.
No complete primary-source text was admitted to the repository or fully transcribed in this intake.
An accountable reviewer must determine the 1911 attribution, select a lawful immutable edition and
exact theorem/page, map all incorporated definitions and assumptions, transcribe/translate the
formula, inspect proof boundaries and corrections/errata, and decide its relation to the catalog's
ODE category and modern formulations.

The 1912 DOI metadata quotes Weyl as saying that he had already published a short note on the
subject in the Goettingen Nachrichten, mathematical-physical class, meeting of 25 February 1911.
This plausibly explains the catalog year, but it does not identify which announcement or full-paper
statement the catalog intends. The metadata's reference note locates the full proof in Section 6;
the source text and incorporated context still require direct, independently reviewed admission.

## Modern ODE-family discriminator

Gerald Teschl, *Ordinary Differential Equations and Dynamical Systems*, Graduate Studies in
Mathematics 140, American Mathematical Society (2012), DOI `10.1090/gsm/140`, gives a precise
ordinary-differential-equation variant. In its regular Sturm-Liouville setup, assumptions (5.45),
page 153, require source-specific real coefficient regularity and positivity on a compact interval;
equations (5.52)-(5.55), pages 155-156, define the weighted inner product, operator, domain, and
separated boundary conditions. Theorems 5.11 and 5.17 supply the discrete simple spectrum and its
ordering. After the modified Pruefer-angle estimate in Lemma 5.24, Theorem 5.25, equation (5.108),
page 173, states a leading `n^2` eigenvalue asymptotic with an `O(n)` remainder and a coefficient
involving the integral of `sqrt(r/p)`.

This is an excellent discriminator aligned with the catalog category, but it is a modern secondary
formulation rather than Weyl's primary PDE paper, and the catalog does not cite it. Its exact
coefficient, regularity, index convention, endpoint data, and remainder make it propositionally
different from the classic multidimensional counting law. It is not adopted, transcribed as the
canonical claim, or credited as `H0` in this intake. The inspected preliminary-edition PDF has
SHA-256 `362433156525216abf596c17ce843204510e96d57afa4284a37c7aa5a9ffc36e`; the inspected
official errata has SHA-256 `3eacbac5b8fc762c5d3f21183cba3ae638b9ac5fbe703cc52cf2857b9605996e`
and a bounded search found no entry for Theorem 5.25 or equation (5.108). These observations are
discovery evidence, not an independent source approval.

## PDE to Sturm-Liouville boundary

The classic multidimensional Weyl law counts eigenvalues below a spectral threshold and has a
leading term involving dimension, domain volume, and a phase-space/unit-ball constant. A regular
one-dimensional Sturm-Liouville asymptotic instead enumerates eigenvalues by an integer index and
depends on interval, coefficient, weight, and endpoint data. Modern Laplace-Beltrami and elliptic-
operator laws add further geometric or symbol assumptions. These are related
generalizations/specializations, not spelling changes. The repository record selects none, and no
checked implication or equivalence among them is available at intake.

## Lean discovery boundary

Pinned `Mathlib.Analysis.Asymptotics.AsymptoticEquivalent` provides the generic
`Asymptotics.IsEquivalent` relation and its limit consequences. Pinned
`Mathlib.Analysis.InnerProductSpace.Spectrum` supplies finite-dimensional self-adjoint eigenvalues,
an eigenbasis, multiplicity facts, and monotone ordering. These are useful adjacent interfaces, but
they do not define an elliptic/Sturm-Liouville spectral counting function or state a Weyl law.

A bounded case-insensitive search for Weyl-law and eigenvalue-asymptotic/counting patterns over
pinned mathlib and repo-local Lean found no exact-topic declaration. Hits for `Weyl` concern
root-system Weyl groups and are homonyms. This is neither the later immutable formal-candidate audit
nor a global absence claim. The canonical module, expression, fingerprints, checked transports,
and statement mutations remain null. No statement elaboration, formal proof, audit completion, or
theorem completion is claimed.
