# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:10467-10472` supplies exactly the title `Brjuno条件`, Alexander
Brjuno, 1971, the gloss `Siegel盘的线性化条件`, importance "high", and status `已验证`. Git blame
attributes all six uncited lines to repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record contains no bibliography, formula,
theorem locator, assumptions, quantifiers, conclusion, or proof.

`Docs/Stage0_Blueprint.md:38969-38994` repeats the gloss while explicitly leaving the formal system,
logical foundation, background, exact definitions and premises, proof route, dependencies,
equivalent forms, axioms, machine status, and artifact links open. Its generic planning text about
a known closed result is not primary-source evidence. The rev-5.6 manifest retains `已验证` only as
`source_status_untrusted` and resets the target to `L0 / rework_required`.

The repository record therefore identifies a named condition and a broad role in complex dynamics,
not one stable proposition. It gives no immutable primary edition, exact theorem, incorporated
definitions, translation, proof boundary, correction, or errata record.

## Bibliographic discovery boundary

The catalog's year and attribution plausibly point toward A. D. Brjuno, *Analytical form of
differential equations*, *Transactions of the Moscow Mathematical Society* **25** (1971),
131-288. An inspected secondary research paper, Timoteo Carletti and Stefano Marmi,
*Linearization of analytic and non-analytic germs of diffeomorphisms of (C, 0)*,
arXiv:`math/0003105v1`, cites that 1971 work at its reference `[Br]`. Its introduction distinguishes
Brjuno's sufficient estimate from Yoccoz's later necessity/sufficiency result, and Appendix A
defines a Brjuno number using a sum over continued-fraction denominators. This confirms several
plausible interpretations rather than selecting one.

Neither the catalog nor an independently reviewed source correction identifies the 1971 edition,
page/theorem, original hypotheses, exact conclusion, or relationship between the source's
differential-equation normal-form setting and the catalog phrase "Siegel disk". The inspected 2000
paper is therefore a discovery lead only. It supplies no H0 identity and cannot choose the Lean
target. Crossref DOI `10.1007/BF01146416` identifies a distinct short 1969 article, *An analytic
form of differential equations*, pages 927-931; it must not be silently treated as the 1971
131-288 source.

## Component crosswalk

| Repository element | Mathematical component to freeze | Required Lean component | Intake assessment |
|---|---|---|---|
| `Brjuno条件` | one exact arithmetic predicate, normally expressed through continued fractions or a Brjuno function | definition over an exact numeric domain with fixed indexing, sum, log, and infinity convention | name only; formula absent |
| Alexander Brjuno / 1971 | historical attribution and likely source family | immutable edition, stable theorem/page, source hash, translations, errata, proof boundary | plausible bibliographic lead, not a frozen source |
| "Siegel disk" | local analytic linearization or a maximal invariant Fatou component | complex map/germ, domain, fixed point, multiplier, conjugacy or component predicate | object and meaning open |
| "linearization" | existence of an analytic change of coordinates conjugating the map to its linear part | analytic maps/germs, composition equality, inverse/local-domain data, normalization | conclusion not stated |
| "condition" | sufficient, necessary, necessary-and-sufficient, quantitative, or merely definitional role | implication direction and ordered binders | logical direction open |
| `已验证` | untrusted inventory label | accepted source review and kernel receipt would be required | no H or M credit |

## Variant and neighbor boundary

Brjuno's classical sufficiency, Yoccoz's necessity/sufficiency over normalized germs, the quadratic
polynomial characterization, quantitative radius estimates, higher-dimensional normal forms, and
the arithmetic definition are separate statements. The neighboring catalog target `THM-M-1432`
explicitly names Yoccoz, so importing his stronger converse or quadratic result would risk merging
two roots. Conversely, proving only convergence properties of continued fractions would omit the
catalog's linearization gloss.

## Source gate

Before the target can leave `H5`, an accountable reviewer must approve a truth-valued correction,
preserve and hash an immutable primary edition, identify an exact theorem and every incorporated
definition, transcribe ordered binders and hypotheses, check translation, corrections, and errata,
map every conclusion clause and boundary case, and justify the boundary against `THM-M-1432` and
other Siegel-linearization targets. A second qualified reviewer must approve the mapping. The
corrected proposition's H status must then be classified afresh; it cannot inherit `已验证`.

## Lean discovery boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, `IntakeProbe.lean`
checks `GenContFract.of`, continued-fraction denominators and convergents, `Real.convergent`,
`AnalyticAt`, analytic composition, fixed points, and semiconjugacy. A bounded source-name search
found no Brjuno/Bryuno, Siegel-disk, Yoccoz, small-divisor, or target analytic-linearization
declaration in repo-local or pinned mathlib Lean sources. Generic continued-fraction and analytic
APIs do not identify the missing root.

The canonical module, declaration/expression, elaborated-expression hash, checked transports, and
statement mutations remain null. The probe and search are intake feasibility evidence only, not a
complete formal-candidate audit and not H0, M0, or readable-proof closure.
