# Source-statement crosswalk

| Claim component | Primary-source discovery anchor | Lean target | Intake assessment |
|---|---|---|---|
| Elliptic regularity with discontinuous coefficients | Ennio De Giorgi, *Sulla differenziabilita e l'analiticita delle estremali degli integrali multipli regolari*, Memorie della Accademia delle Scienze di Torino, Classe di Scienze Fisiche, Matematiche e Naturali, Series 3, 3 (1957), 25-43 | none frozen | Original primary paper identified bibliographically; exact theorem/page, notation translation, assumptions, and errata remain unaudited |
| Continuity of solutions of elliptic/parabolic equations | John Nash, *Continuity of solutions of parabolic and elliptic equations*, American Journal of Mathematics 80(4) (1958), 931-954, DOI 10.2307/2372841 | none frozen | Primary paper and page span identified; a theorem-level crosswalk has not been accepted |
| Scalar divergence-form equation | Repository source says only "divergence-form equations" | future exact expression | Scalar, homogeneous, second-order elliptic scope is a conservative candidate family, not yet a source-certified exact statement |
| Bounded measurable uniformly elliptic coefficients | Expected defining hypothesis of the named regularity result | future coefficient structure and predicates | Bounds, symmetry convention, and quantifier order must be read from the selected source theorem |
| Weak solution | Expected Sobolev/variational formulation | future weak-solution predicate | Function space, representative convention, and test-function class remain open |
| Holder continuity | Repository source says "Holder continuity" | future local Holder predicate plus quantitative estimate | Interior versus boundary scope, exponent, constants, norms, and ball geometry remain open |

The two historical papers do not automatically define one identical Lean proposition. Modern texts
also package the result in several variants: oscillation decay, a Holder estimate, a Harnack route,
and elliptic versus parabolic forms. This dossier admits only the scalar elliptic, divergence-form,
interior branch suggested by the repository metadata. The statement phase must select an exact
primary theorem and preserve its coefficient, solution, locality, and quantitative conventions.

The repository's `已验证` label is not evidence that a public Lean proof exists. No mathlib or
external declaration is credited here, and no anchor-only result can upgrade the machine state.

## Open source gate

Before `H0`, obtain immutable copies or hashes, pinpoint theorem/page ranges, map every premise and
conclusion component, check translations and published corrections/errata, and obtain independent
review. Before the statement gate, inspect pinned Lean APIs, elaborate the exact expression, record
its normalized hash and environment fingerprint, check any alternate transport, and mutation-test
coefficient hypotheses, domain, binder scope, and interior boundary cases.

