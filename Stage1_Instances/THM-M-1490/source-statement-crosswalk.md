# THM-M-1490 source-statement crosswalk

## Repository source record

`Docs/researches/math_theorems.md` contains the complete received record: title `优化理论`,
attribution `众多数学家`, time `20世纪`, and gloss `数学优化的理论`. It supplies no bibliography,
formula, quantifier, domain, hypothesis, conclusion, theorem locator, proof, correction history,
reviewer, or formal artifact. All six catalog lines originate at repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`; this establishes repository provenance, not a primary
mathematical source.

`Docs/Stage0_Blueprint.md` repeats the gloss and explicitly leaves the formal system, foundations,
exact definitions and premises, proof route, dependencies, equivalent formulations, axioms,
machine status, and artifact links open. Its generic planning prose about a known closed result is
not source evidence. The rev-5.6 manifest preserves `已验证` only in the field
`source_status_untrusted`.

## Crosswalk

| Received component | Required mathematical content | Prospective Lean surface | Intake status |
|---|---|---|---|
| `优化理论` | one truth-valued theorem rather than a field | exact `Prop` and declaration/expression | absent |
| `数学优化` | objective, domain, feasible set, min/max direction, solution notion | types, structures, functions, predicates, ordered binders | absent |
| `理论` | existence, optimality, duality, convergence, rate, complexity, or another exact conclusion | hypotheses and conclusion | absent; no family member selected |
| many mathematicians / twentieth century | author, work, edition, theorem/page and corrections | immutable source revision and node crosswalk | untrusted broad attribution only |
| `已验证` | proof body, formal system, exact declaration, dependency revision and check | kernel evidence and accepted receipt | no credit |

There is no source node to map to a canonical statement. Consequently the canonical statement,
binders, hypotheses, conclusion, Lean expression, minimal imports, expression fingerprint,
alternate transports, and mutations are intentionally unaccepted rather than guessed.

## Bibliographic discovery boundary

Broad references such as Nocedal and Wright, *Numerical Optimization* (2nd ed., 2006, DOI
`10.1007/978-0-387-40065-5`), Rockafellar and Wets, *Variational Analysis* (1998, DOI
`10.1007/978-3-642-02431-3`), and Rockafellar, *Convex Analysis* (1970, DOI
`10.1515/9781400873173`) are possible field-level discovery leads. The catalog cites none of them,
and this intake admits no theorem, page, assumptions, proof, or correction record from them. Their
many inequivalent results cannot select the root by familiarity and grant no `H0` credit.

## Pinned formal discovery boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, distinct generic APIs
include:

- `IsCompact.exists_isMinOn`: continuous functions attain a minimum on a nonempty compact set;
- `IsMinOn.of_isLocalMinOn_of_convexOn`: a local minimum of a convex function on its domain is a
  global minimum; and
- `StrictConvexOn.eq_of_isMinOn`: two global minimizers of a strictly convex function agree.

These declarations have different domains, premises, and conclusions. `IntakeProbe.lean` checks
their availability only. A bounded search found no source-selected declaration corresponding to
the exact broad phrases `optimization theory` or `mathematical optimization`. Repository-local
generic minimizer wrappers in `AwesomeTheorems/Stage1/S1_M_163.lean` belong to `THM-M-1270`
(Ekeland's variational principle), so they are foreign-target evidence and receive no credit here.
This is not the exhaustive immutable anchor audit required by the later phase.

## Status and correction boundary

The source crosswalk supports provisional `H5`: the received catalog label is not a stable
proposition. It does not assess the truth of any corrected optimization theorem. `M4` and `R4`
remain because there is no exact formal target or source-faithful proof route. A corrected intake
must name an immutable primary proposition, provide a complete definition/assumption/conclusion/
proof/errata crosswalk, preserve neighboring-target boundaries, and receive independent review
before statement elaboration.
