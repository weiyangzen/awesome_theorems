# THM-M-0064 source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:477-482` contains the complete catalog record:

- name: `阿贝尔-鲁菲尼定理`;
- attribution: Niels Abel/Paolo Ruffini;
- date: 1824;
- statement: `五次及以上一般多项式方程无根式解`;
- importance: high;
- formalization status: `已验证`.

All six lines originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. They contain no
bibliography, displayed formula, definition of `general`, coefficient field, quantifier order,
definition of radical solution, proof, correction record, or formal artifact. The exact excerpt has
SHA-256 `156ca51bd9e76a1ab2b60eac39308a315d93e9d7c81df516506b923a45a29390`.

`Docs/Stage0_Blueprint.md:1866-1885` repeats the gloss and explicitly leaves the formal system,
foundations, exact definitions and assumptions, proof route, equivalent forms, axioms, machine
status, and artifact links open. Its excerpt SHA-256 is
`a9e6c886d17d5550a58f47da0fda6a527a4d108bea6c6397ed51be7502acab6e`. Rev-5.6 therefore
resets this item to `L0 / rework_required`.

## Historical human-source lead

Niels Henrik Abel, *Demonstration de l'impossibilite de la resolution algebrique des equations
generales qui passent le quatrieme degre*, *Oeuvres completes de Niels Henrik Abel*, nouvelle
edition, pages 66-94, DOI `10.1017/CBO9781139245807.008`, is the strongest primary lead matching
the catalog's degree-above-four language. Publisher citation metadata identifies the title, author,
collected edition, and pages. Abel's shorter *Memoire sur les equations algebriques, ou l'on
demontre l'impossibilite de la resolution de l'equation generale du cinquieme degre*, pages 28-33,
DOI `10.1017/CBO9781139245807.004`, is a second historically aligned but quintic-specific lead.

This remains `H1`, not `H0`. The repository's 1824 date and joint Abel/Ruffini attribution must be
reconciled with the selected Abel text and publication/edition history rather than silently
normalized. The publisher PDF request returned access-gate HTML, so no exact theorem passage,
definition chain, complete proof-node mapping, translation audit, correction or errata
disposition, immutable admitted source packet, or independent review was completed at intake.
Bibliographic metadata is discovery evidence, not source closure.

## Component crosswalk

| Catalog component | Candidate mathematical reading | Pinned Lean interface | Intake status |
|---|---|---|---|
| "polynomial equations" | polynomials and their roots/splitting fields | `Polynomial`, `Polynomial.Gal` | base field and equation/polynomial encoding open |
| "degree five and above" | exactly five, every `n >= 5`, or a generic degree parameter | `Polynomial.natDegree`; `Fin 5` | quantifier and higher-degree transport open |
| "general" | generic coefficients, no uniform formula, or existence of counterexamples | no credited exact interface | proposition-changing ambiguity |
| "by radicals" | membership in a radical closure or radical extension tower | `solvableByRad F E` | one-root/full-splitting-field and source fidelity open |
| obstruction | nonsolvable Galois group | `IsSolvable q.Gal` | necessary direction exists; exact converse/root bridge open |
| degree-five group | symmetric group on five letters is nonsolvable | `Equiv.Perm.fin_5_not_solvable` | group fact only; polynomial realization open |
| `已验证` | untrusted catalog status | none | no H/M/R closure credit |

## Pinned formal candidates

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, module
`Mathlib.FieldTheory.AbelRuffini` defines `solvableByRad F E`, proves
`isSolvable_gal_minpoly`, and proves `isSolvable_gal_of_irreducible`. The last theorem says that
if `x : E` lies in `solvableByRad F E`, `q : F[X]` is irreducible, and `q` vanishes at `x`, then
`q.Gal` is solvable. The module documentation explicitly calls this **one direction** of
Abel-Ruffini. The source file is pinned at SHA-256
`f26182403fbd9ecf7133a967b47fb3ea5d7bc2b291d006fdc8c6838ce45c035b`.

Pinned `Mathlib.GroupTheory.Solvable` proves
`Equiv.Perm.fin_5_not_solvable : not IsSolvable (Equiv.Perm (Fin 5))`. This supplies a relevant
group-theoretic obstruction. `IntakeProbe.lean` checks both declarations and records their axiom
reports in the current environment.

These are credible, kernel-elaborated `M3` interfaces and partial ingredients, not an exact root.
No checked declaration in this intake states a generic polynomial's Galois group is the required
symmetric group, translates "general formula" into `solvableByRad`, proves the chosen converse or
contrapositive with all source assumptions, or handles every degree above five. A later anchor
audit must inventory terminal bodies and transitive trust before any stronger machine status.

## Exactness gaps

The statement gate must admit one precise source and settle generic-versus-existential scope,
degree quantification, fields and characteristic, irreducibility/separability, one root versus all
roots, radical-tower conventions, generic specialization, and the exact Galois obstruction. It
must then elaborate and fingerprint that same claim, check every credited alternate encoding, and
run all four required mutation classes. A matching module title or one necessary implication
cannot close these gaps.
