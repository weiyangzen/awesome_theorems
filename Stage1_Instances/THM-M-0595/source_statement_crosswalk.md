# Source-statement crosswalk

The repository source record gives the Chinese statement `连续函数可用光滑函数逼近`, translated
literally as "continuous functions can be approximated by smooth functions." The following
crosswalk locates the theorem family without pretending that this short sentence fixes one of its
several inequivalent forms.

| Claim component | Human source anchor | Lean target at intake | Assessment |
|---|---|---|---|
| Historical Whitney approximation theorem family | H. Whitney, "Differentiable manifolds," *Annals of Mathematics* (2) 37 (1936), 645-680 | None selected | Primary historical paper identified bibliographically; exact theorem/page, original hypotheses, and errata still require direct edition audit |
| Continuous scalar function on a smooth manifold | The repository phrase most literally suggests a scalar-valued function, but supplies no codomain | Unselected real-valued function expression | Domain, codomain, regularity class, and manifold hypotheses are absent; this is a candidate, not a frozen root |
| Meaning of "approximated" | Standard formulations use a prescribed positive error function or a specified topology on a function space | Unselected inequality/topological-neighborhood expression | The source gives neither a tolerance quantifier nor a topology, so uniform and strong/Whitney density claims cannot be inferred |
| Map-valued form | A standard Whitney approximation formulation says that a continuous map between smooth manifolds is homotopic to a smooth map | Unselected manifold-map expression | Related theorem form; it is not substituted for the scalar wording at intake |
| Relative form | Standard refinements preserve a map where it is already smooth, under additional neighborhood/closed-set hypotheses | Unselected relative expression | A strict strengthening whose subset and neighborhood hypotheses must be pinned before inclusion |
| Smoothness class and boundary | Historical and modern accounts vary in differentiability notation and manifold conventions | No Lean universes or typeclasses selected | `C^infinity`, finite `C^r`, boundary, second countability, and paracompactness choices change the literal target |

## Provenance boundary

The 1936 paper is a discovery anchor for the historical theorem family, not yet an `H0` receipt.
The statement phase or source-audit phase must inspect an immutable copy, identify the exact theorem
and pages, map every premise and conclusion, account for notation and later corrections, and obtain
independent review. If a modern formulation is selected, its source must also be pinned and its
relationship to Whitney's statement made explicit.

Repository provenance:

- `Docs/researches/math_theorems.md` records the name, year 1936, and the one-line Chinese statement.
- `Docs/Stage0_Blueprint.md` repeats that statement and an untrusted `已验证` metadata label.
- `Docs/Stage1_Targets_rev-5.6.json` admits the target at uniform `L0 / rework_required`; it grants
  no source or machine-proof credit.

No `H0` or Lean-closure claim is made. `H1` means a classical proof source is identified while the
exact formulation, premise mapping, immutable source evidence, errata review, and independent
acceptance remain open.
