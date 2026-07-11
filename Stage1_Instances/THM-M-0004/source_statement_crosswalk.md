# Source-statement crosswalk

| Claim component | Human-source discovery anchor | Lean candidate | Intake assessment |
|---|---|---|---|
| Repository wording | `Docs/researches/math_theorems.md`, lines 49-54 | none | Secondary metadata only; it omits the ring, complex, coefficient, degree, hypotheses, maps, and exact conclusion |
| Homological tensor/Tor sequence | Classical universal coefficient theorem for homology; a source-audit lead is C. A. Weibel, *An Introduction to Homological Algebra* (Cambridge University Press, 1994), universal-coefficient material | `CategoryTheory.Tor`, `ShortComplex.ShortExact`, homology APIs | Plausible branch, but edition theorem/page and assumption-level correspondence are not verified at intake |
| Cohomological Hom/Ext sequence | Classical universal coefficient theorem for cohomology; same source family | `Abelian.Ext`, morphism/Hom objects, `ShortComplex.ShortExact` | Plausible sibling branch; the metadata's “Hom” wording does not uniquely select it |
| Chain homology and comparison maps | Standard chain-complex formulation | `HomologicalComplex.homologyFunctor`, `homologyMap`, bifunctor/total-complex APIs | Substrate candidates only; no terminal comparison map or exactness declaration is credited |
| Naturality and splitting | Refinements whose exact scope varies by formulation | legacy output fields `naturalitySquare` and short-exact witnesses | Must be included only if the selected source theorem states them; splitting is often noncanonical and must not be silently strengthened to natural splitting |

The repository discovery record gives a 1950s date, “many mathematicians,” and an `已验证` label.
None is a primary-source receipt, and the label supplies no formal project, revision, declaration, or
build evidence. It therefore provides no `H0` or machine credit.

The legacy module `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_099.lean` proposes
`Stage1.THMM0004.StatementShape`. Its output structure contains abstract term functions, short exact
sequences, naturality propositions, and an unconstrained `termIdentifications : Prop`. This is useful
for discovering relevant APIs, but it is not an exact encoding of either classical UCT branch and is
unaccepted under the uniform rev-5.6 L0 baseline.

The statement phase must first pin a source edition or immutable scan, locate an exact theorem and
pages, record all assumptions and errata, and choose either one canonical branch or an explicitly
justified conjunction. It must then map every source term and map to an elaborated Lean expression.
Until that happens, the honest human status is `H3` and the machine status is `M3`.

