# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md:1964-1969` records only:

- title: `拉东-尼科迪姆定理`;
- attribution: Johann Radon / Otto Nikodym;
- year: 1930;
- gloss: `测度的绝对连续与密度函数`;
- importance: high;
- untrusted formalization label: `已验证`.

All six lines originate in commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. `Docs/Stage0_Blueprint.md:7549-7575`
repeats this metadata while leaving exact definitions, premises, proof route, equivalent forms,
axioms, machine status, and artifact links open. These records establish catalogue identity only.

## Primary-source lead

Publisher and Crossref metadata identify Otton Nikodym, "Sur une generalisation des integrales de
M. J. Radon," *Fundamenta Mathematicae* 15 (1930), pages 131-179, DOI
`10.4064/fm-15-1-131-179`. The observed Crossref payload had SHA-256
`0cd266f2d8c66a63cb894cf4004702140f6883b69043f02e6a3a50e29a4f00a2`.

The publisher scan was retrieved for bounded inspection: 1,993,020 bytes, 25 scanned image spreads,
SHA-256 `4cf86f35545ba7136f64ccf64754aecaf9c258d6043f0975cb48d51889963561`.
Its first article page visibly gives the title and author and describes a generalization of Radon's
measure and integration theory. Printed page 168, Theorem III, was also visually inspected. It says
that a perfectly additive real-valued set function on the field `H`, satisfying the null-set form
`F(E) != 0` implies `mu(E) > 0`, has a function `f` with `F(E) = integral_E f dmu` for all `E` in
`H`; it also states uniqueness modulo a `mu`-null set. The scan has no text layer. Intake has not
completed the preceding definition chain, exact modern translation, full proof boundary, later
corrections or errata, or independent review. The locator is therefore an `H1` primary-source lead,
not an H0 record.

## Clause crosswalk

| Repository phrase or candidate clause | Human-source status | Pinned Lean candidate | Intake decision |
|---|---|---|---|
| "measure" | category and finiteness assumptions absent | positive `Measure alpha` | open; do not substitute |
| "absolute continuity" | orientation and definition absent | `mu << nu` | candidate only |
| "density function" | codomain, measurability, finiteness, and uniqueness absent | `mu.rnDeriv nu : alpha -> ENNReal` | candidate only |
| density represents the measure | equality or integral form absent | `nu.withDensity (mu.rnDeriv nu) = mu` | candidate only |
| existence assumptions | absent | `[HaveLebesgueDecomposition mu nu]`; available from s-finite/sigma-finite conditions | source mapping open |
| theorem direction | printed Theorem III is an implication plus uniqueness; the catalogue is silent | an `iff` declaration plus a one-way theorem | a future transport must not identify the historical implication literally with the modern `iff` |
| `已验证` | untrusted inventory metadata | no proposition or proof object | no H or M credit |

## Formal candidate crosswalk

The intake probe elaborates the following at the pinned revision:

| Declaration | Candidate role | Unclosed gate |
|---|---|---|
| `Measure.absolutelyContinuous_iff_withDensity_rnDeriv_eq` | exact-topic positive-measure equivalence | source identity, exact target serialization, wrapper/transport, provenance and trust audit |
| `Measure.withDensity_rnDeriv_eq` | forward absolute-continuity-to-density direction | same, plus decision whether one direction is the source root |
| `Measure.rnDeriv` | selected `ENNReal` density | source density codomain and a.e.-uniqueness mapping |
| `Measure.haveLebesgueDecomposition_of_sigmaFinite` | decomposition existence substrate | source s-finite/sigma-finite assumptions and instance boundary |
| `Measure.haveLebesgueDecomposition_of_finiteMeasure` | finite-measure substrate | cannot replace a more general root |
| `SignedMeasure.absolutelyContinuous_iff_withDensityᵥ_rnDeriv_eq` | signed-measure equivalence close to the historical real-valued set-function form | source definitions, assumptions, translation, and exact expression match open |

Before leaving `H1`, an accountable source reviewer must select an immutable edition, identify the
exact theorem/section/page, transcribe the incorporated definitions and full ordered statement,
map every premise and conclusion, audit corrections/errata, and approve the Radon/Nikodym historical
boundary. Before statement acceptance, Lean work must freeze minimal imports and an elaborated
expression and pass the required removed-hypothesis, changed-domain, binder-scope, and boundary
mutations.
