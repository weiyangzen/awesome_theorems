# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md` names Andrew Wiles, gives 1995, and states `半稳定椭圆曲线的模性`
("modularity of semistable elliptic curves"). Stage0 repeats this wording. The target manifest
retains `已验证` only in the explicitly untrusted `source_status_untrusted` field. None of these
repository records supplies definitions, assumptions, a proof crosswalk, or machine evidence.

## Primary theorem locator

Andrew Wiles, "Modular elliptic curves and Fermat's Last Theorem", *Annals of Mathematics* (2)
141 (1995), no. 3, 443-551, DOI `10.2307/2118559`, states on page 443 as Theorem 0.4:
"Every semistable elliptic curve over Q is modular."

The Annals article metadata was checked during intake against the publisher page. The quoted
theorem locator identifies the target but does not by itself close `H0`: the paper's definitions of
semistability and modularity, assumptions and normalization, proof dependencies, the companion
Taylor-Wiles paper, errata, and an independent source review remain to be mapped node by node.

## Crosswalk

| Source component | Mathematical role | Pinned Lean boundary | Intake status |
|---|---|---|---|
| "every" | universal quantification over elliptic curves over `Q` | `WeierstrassCurve Q` plus `WeierstrassCurve.IsElliptic`, subject to representation audit | API elaborated; exact domain open |
| "semistable" | global hypothesis at every finite place | local `HasGoodReduction` / `HasMultiplicativeReduction` in `EllipticCurve.Reduction` | local ingredients elaborate; global predicate absent |
| "modular" | association with a weight-two modular form, with source-exact compatibility | `ModularForm`, `CuspForm`, congruence subgroup, q-expansion APIs | analytic ingredients exist; required relation absent |
| "over Q" | rational base field and its finite places | `Q` and a future place/DVR model family | base field elaborates; global local-model transport open |
| source proof | Wiles's modularity-lifting route and Taylor-Wiles repair | future obligation and provenance graph | not audited at intake |
| `已验证` | untrusted repository inventory label | no proposition or proof body | rejected as evidence |

## Legacy and formal boundary

`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_049.lean` belongs to `THM-M-0132`, not this target.
It truthfully describes itself as a boundary file and uses abstract compatibility `Prop` fields and
an abstract semistable field. It is useful discovery provenance only. Copying its
`SemistableStatementShape` would broaden the trusted input surface and would not encode the source
theorem. No exact repo-local or pinned-mathlib theorem body is credited by this intake.
