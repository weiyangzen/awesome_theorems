# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md:4706-4711` names `极值定理`, attributes it to Karl Weierstrass in
1860, and states `紧集上连续函数可取到最大最小值`: a continuous function on a compact set can
attain maximum and minimum values. It records high importance and `已验证`, but gives no
bibliography. All six lines originate in the initial repository source-record commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`.

`Docs/Stage0_Blueprint.md:17368-17393` repeats the gloss while explicitly leaving precise
definitions and premises, proof route, dependencies, equivalent forms, axiom use, formal status,
and artifact links unresolved. The rev-5.6 manifest therefore retains only metadata eligibility;
its verified label gives no `H`, `M`, or receipt credit.

## Human-source boundary

The catalog supplies no primary or authoritative proof source and its `1860` attribution is not a
pinpoint theorem locator. The name "Weierstrass theorem" is itself ambiguous in the literature: it
also names approximation, infinite-product, preparation, and convergence theorems. A later source
audit must admit an immutable edition that actually states and proves this compact-domain extremum
claim, map every incorporated compactness, continuity, order, and nonemptiness convention, and
review attribution, translation, corrections, and errata. The well-known theorem family supports
only provisional `H1`, not `H0`.

## Clause crosswalk

| Catalog phrase | Candidate mathematical component | Pinned Lean surface | Intake assessment |
|---|---|---|---|
| `紧集` / compact set | a source-selected nonempty compact subset `K` or compact carrier | `K : Set X`, `IsCompact K`, `K.Nonempty` | compactness stated; carrier and indispensable witness-producing nonemptiness omitted |
| `连续函数` / continuous function | a source-selected ordered-codomain function continuous on `K` | `f : X -> A`, `ContinuousOn f K`, or a subtype `Continuous` map | domain, codomain, order/topology assumptions, and continuity encoding open |
| `可取到最小值` / attains a minimum | a member `x_min` whose value is below every value on `K` | `exists x in K, IsMinOn f K x`, definitionally an inequality over `K` | direct pinned candidate exists; no canonical-root credit |
| `可取到最大值` / attains a maximum | a member `x_max` whose value is above every value on `K` | `exists x in K, IsMaxOn f K x`, definitionally an inequality over `K` | direct pinned candidate exists; no canonical-root credit |
| both extrema | two witnesses, not necessarily the same | conjunction or paired existential plus checked transports | conjunction shape and binder order not supplied by catalog |
| Weierstrass / 1860 | historical identity metadata | immutable source, exact locator, definition/proof boundary, errata, reviewer | uncited lead only |
| `已验证` | inherited catalog status | no formal component | explicitly untrusted |

## Pinned formal lead

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, module
`Mathlib.Topology.Order.Compact` explicitly documents and proves:

- `IsCompact.exists_isMinOn [ClosedIicTopology A] (hK : IsCompact K)
  (hne : K.Nonempty) (hf : ContinuousOn f K) : exists x in K, IsMinOn f K x`; and
- `IsCompact.exists_isMaxOn [ClosedIciTopology A] (hK : IsCompact K)
  (hne : K.Nonempty) (hf : ContinuousOn f K) : exists x in K, IsMaxOn f K x`.

The maximum theorem is obtained through the order dual from the minimum theorem. The module header
calls both declarations the extreme value theorem, and `Mathlib.Order.Filter.Extr` identifies
`IsMinOn` and `IsMaxOn` with the expected universal inequalities. `IntakeProbe.lean` checks those
interfaces and prints their axiom reports in the pinned environment.

This is `M3` support at intake: exact formal interfaces and proof-bearing candidates are present,
but no source-approved combined root, elaborated root expression, checked source transport,
terminal-body provenance audit, or node receipt has been frozen. The statement and anchor-audit
phases must decide whether the generic ordered-codomain pair, a real-valued specialization, a
compact-space formulation, or another source-faithful form is canonical. Availability of both
library theorems does not by itself authorize `M0-W`.

## Source gate

Before `H0`, accountable review must admit a pinpoint proof source and map all premises,
definitions, conclusion clauses, boundary cases, formulation transports, corrections, and errata.
Before statement acceptance, the exact human claim must be frozen and elaborated with minimal
pinned imports, expression and environment fingerprints, checked alternate encodings, and removed-
hypothesis, changed-domain, changed-binder-scope, and boundary-case mutations. Until then this
crosswalk is an intake resolution ledger, not a theorem statement or proof certificate.
