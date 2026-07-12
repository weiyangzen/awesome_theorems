# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` gives the statement "a theory has a model if and only if every
finite subset has a model", attributes the result to Kurt Goedel / Anatoly Maltsev, and dates it to
1930. `Docs/Stage0_Blueprint.md` preserves that wording. This identifies first-order semantic
compactness rather than the unrelated topological theorem of the same Chinese name. The generated
`已验证` label is untrusted metadata and supplies no proof credit.

## Candidate human sources

- Kurt Goedel, "Die Vollstaendigkeit der Axiome des logischen Funktionenkalkuels", *Monatshefte
  fuer Mathematik und Physik* 37 (1930), 349-360. This is a historical primary candidate for the
  completeness result from which compactness is classically derived.
- Anatoly I. Maltsev's 1936 work on mathematical logic/model theory is a historical candidate for
  the general model-theoretic formulation associated with his name.

These are discovery anchors only. This intake has not fixed an immutable scan or edition, located
the exact compactness statement by theorem and page, checked its language/cardinality conventions,
translated incorporated definitions, audited corrections, or obtained independent review. They do
not establish `H0`.

## Crosswalk

| Repository phrase | Mathematical meaning | Pinned Lean candidate | Intake status |
|---|---|---|---|
| theory | arbitrary set of sentences over one first-order language | `T : L.Theory` | included |
| has a model | a nonempty structure satisfies every sentence in `T` | `T.IsSatisfiable`, defined as `Nonempty (ModelType T)` | candidate checked |
| every finite subset | every finite set of sentences contained in `T` | `T.IsFinitelySatisfiable`; `T0 : Finset L.Sentence` and `(T0 : L.Theory) \u2286 T` | candidate checked |
| if and only if | restriction direction plus compactness direction | `T.IsSatisfiable \u2194 T.IsFinitelySatisfiable` | candidate checked |
| no stated size restriction | arbitrary language/theory within universe-polymorphic encoding | implicit `L : Language.{u,v}` and `T : L.Theory` | exact fingerprint open |

## Formal-source boundary

Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, module
`Mathlib.ModelTheory.Satisfiability`, declares
`FirstOrder.Language.Theory.isSatisfiable_iff_isFinitelySatisfiable` with the matching candidate
type. Its source body uses an ultraproduct over an ultrafilter for the hard direction. That source
location is a strong anchor-audit candidate, but intake does not yet credit its proof body, axiom
closure, provenance, or exact canonical-statement identity.

Before `H0`, a source reviewer must pin and inspect a primary source, record exact theorem/page and
all assumptions and errata, and approve its row-by-row correspondence with the canonical statement.
