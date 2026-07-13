# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:7106-7111` supplies exactly the title `Kim-Vu不等式`, attribution
`Jeong Han Han/Van Vu`, year 2000, the gloss `多项式集中不等式` ("polynomial concentration
inequality"), high importance, and status `已验证`. Git history attributes all six uncited lines to
commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record gives no source, theorem number,
definitions, binders, hypotheses, constants, conclusion, proof locator, errata, reviewer, or formal
artifact. The given first author string does not match the likely paper's bibliographic author.

`Docs/Stage0_Blueprint.md:26524-26549` repeats the gloss while explicitly leaving the target formal
system, foundation, exact definitions and premises, proof route, dependencies, alternate forms,
axioms, machine state, and artifact links open. The rev-5.6 manifest preserves `已验证` only as
untrusted metadata and resets the target to `L0 / rework_required`.

## Published source lead

Jeong Han Kim and Van H. Vu, *Concentration of Multivariate Polynomials and Its Applications*,
*Combinatorica* 20(3), March 2000, pages 417-434, DOI `10.1007/s004930070014`, is the likely
primary bibliographic lead. Crossref and Springer metadata observed on 2026-07-13 confirm the
authors, title, journal, date, volume, issue, page range, and DOI. The observed Crossref response
had SHA-256 `5b6d2a3765bd2bd7bcb8f4b5ddfbbdab942338faad21a5766cef03643b6205d4`.

The publisher abstract says the inputs are independent random variables taking values zero or one,
that `Y` is a multivariable polynomial in them with positive coefficients, and that the paper gives
a condition ensuring strong concentration of `Y` around its mean even when several variables may
have a large effect. The formula-bearing primary article was access-controlled; the accessible HTML
stripped variables/formulas and exposed only the abstract and bibliographic matter. No exact
numbered theorem, page within the article, notation, constants, full assumptions, conclusion, proof
boundary, or errata was therefore transcribed or accepted. A transient author-hosted PDF lead also
timed out and was not admitted. The paper identification plus explicit reconstruction gap supports
provisional `H1`, not H0.

## Clause crosswalk

| Repository/source component | Candidate mathematical component | Prospective Lean surface | Intake assessment |
|---|---|---|---|
| `Kim-Vu不等式`, year 2000 | result family in the Kim-Vu 2000 paper | source identity record | strong lead; exact result not selected |
| `Jeong Han Han/Van Vu` | likely Jeong Han Kim and Van H. Vu | catalog correction record | mismatch recorded, not silently rewritten |
| `多项式集中不等式` | concentration of a random polynomial around its expectation | a future probability proposition | too broad to determine binders or conclusion |
| abstract: independent zero-one variables | Bernoulli coordinate family on a product probability space | `ProbabilityTheory.iIndepFun` or `IsSetBernoulli` may be substrate | index, law, measure, and measurability conventions open |
| abstract: multivariable polynomial | finite positive-coefficient polynomial evaluated on coordinates | `MvPolynomial` plus evaluation is one candidate encoding | multilinearity, coefficient domain, support, and degree open |
| source condition | expectations/maxima of source-defined derivatives or influences | iterated `MvPolynomial.pderiv` plus expectation is only a possible model | derivative family and control parameters untranscribed |
| strong concentration around the mean | source-specific deviation event and probability bound | measure of a set or probability inequality | direction, threshold, constants, and tail form open |
| `已验证` | untrusted inventory label | source review and kernel receipts would be required | no H0 or M credit |

## Pinned Lean boundary

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the intake probe checks
`MvPolynomial`, `MvPolynomial.eval`, `MvPolynomial.eval₂`, `MvPolynomial.pderiv`,
`ProbabilityTheory.iIndepFun`, `ProbabilityTheory.setBernoulli`, and
`ProbabilityTheory.IsSetBernoulli`. These APIs show plausible representational substrate. They do
not define the source's derivative expectation parameters or state a Kim-Vu tail inequality.

A bounded case-insensitive search of repo-local Lean and pinned mathlib found no `Kim-Vu`,
`KimVu`, or polynomial-concentration theorem declaration. This is scoped intake discovery only,
not the later immutable external anchor audit and not a global absence theorem.

## Source gate

Before leaving `H1`, accountable reviewers must preserve and hash an approved lawful primary
edition, inspect and pinpoint one theorem and all incorporated definitions, transcribe every ordered
binder, independence and distribution premise, polynomial and coefficient convention, degree and
derivative parameter, numerical constant, auxiliary range, conclusion and degenerate case, audit
proof boundaries and corrections/errata, resolve the catalog author text, and independently approve
fidelity to `THM-M-0973`. Only then may statement work freeze minimal imports, an elaborated
expression and environment fingerprint, checked alternate encodings, and the required removed-
hypothesis, changed-domain, binder-scope, and boundary-case mutations.
