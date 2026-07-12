# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:10069-10074` supplies exactly the title `最小作用量原理`,
William Hamilton, the year 1834, the gloss `物理系统的变分原理`, importance "high," and status
`已验证`. Git provenance places all six uncited lines in repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. There is no action formula, system model, definition,
binder, hypothesis, conclusion, proof source, edition/page locator, erratum, reviewer, or formal
artifact.

`Docs/Stage0_Blueprint.md:37587-37612` repeats the gloss while explicitly leaving exact definitions
and premises, proof route, dependencies, alternate forms, axioms, machine status, and artifact links
open. Its generic assertion that a closed result exists is planning metadata, not source evidence.
The rev-5.6 manifest preserves `已验证` only as `source_status_untrusted` and resets the target to
`L0 / rework_required`.

## Literal crosswalk

| Catalog phrase | Necessary mathematical component | Prospective Lean component | Intake status |
|---|---|---|---|
| "physical system" | particles, configuration manifold, constrained system, field, or another axiomatized model | carrier/configuration types, dynamics, structures, units and constraints | model and domain absent |
| "variational principle" | functional, admissible variations, boundary data, topology and a quantified extremality/stationarity relation | action functional, path/variation predicates, derivative or order predicate | no predicate or quantifier supplied |
| "least action" | exact action convention and minimum, extremum, or stationary semantics | interval integral or source-specific functional; `IsMin`, `IsLocalMin`, `IsLocalExtr`, or zero first variation | term is ambiguous and historically overloaded |
| William Hamilton / 1834 | historical source family | provenance only | no edition or passage cited by the catalog |
| `已验证` | untrusted inventory label | accepted source proof and kernel receipt would be required | no H or M credit |

The gloss does not assert a truth-valued conclusion. Quantifying universally over all physical
systems would be false without extensive hypotheses; selecting those hypotheses from memory would
substitute a new theorem.

## Inspected Hamilton source family

William Rowan Hamilton, *On a General Method in Dynamics*, *Philosophical Transactions of the Royal
Society of London*, part II (1834), pp. 247-308, DOI `10.1098/rstl.1834.0017`, was inspected in the
David R. Wilkins 2000 electronic edition hosted by Trinity College Dublin. Crossref independently
confirms the title, author, journal, date, pages, and DOI.

The electronic edition says it is based on the original publication and records two corrections:
`w(n)` to `w(n-1)` in equation `(S5.)`, and an inserted missing minus sign in `(K6.)`. The full PDF
observed during intake has SHA-256
`4b07c76a204c49888111b6dfc0bc53879746cc9f21716f16fc8d2f99ff0d0065`; the inspected Sections 1-3
extract has SHA-256 `8ac2ccdd00c349f845f1207717a0534e0ee3eb995be552731f293b44bc7eb7d1`.

| Source locator | Source component | Possible target component | Intake disposition |
|---|---|---|---|
| Section 1, equations (1)-(3) | equations of motion for mutually attracting/repelling free points and the force function | one historical system model and equations-of-motion endpoint | candidate historical context only |
| Section 2, equations (A)-(B) | variation law for `V`, where `V = integral 2T dt` is accumulated living force/action | source-specific action and varying-endpoint/energy relation | not the modern unrestricted `integral L dt` convention |
| Section 3, Wilkins edition pp. 5-6 (original journal pp. approximately 251-252) | at fixed extreme positions and constant energy, variation of action vanishes for infinitesimally nearby geometrically admissible motions respecting the energy relation | stationary fixed-energy action principle | candidate statement family; assumptions and modern translation require review |
| Section 3 | Hamilton says "least" would be better called "stationary" action | guard against an unqualified minimum target | semantic discriminator, not a full theorem selection |
| Section 3 | Hamilton distinguishes the older stationary-action principle from his law of varying action | separate candidate principles | catalog gloss does not choose between them |

This source sharply demonstrates why the title alone cannot select a theorem. It does not by itself
authorize the modern fixed-time Lagrangian statement, an Euler-Lagrange implication, or a global
minimum claim. The catalog does not cite this edition or pinpoint a clause. Historical notation,
system assumptions, corrections, relation to Maupertuis/Lagrange, modern restatement, proof
boundary, and independent review all remain open; no H0 is claimed.

## Overlap and identity crosswalk

| Repository record | Wording | Boundary |
|---|---|---|
| `THM-M-1381` | Maupertuis principle; gloss "least-action principle" | adjacent fixed-energy principle, separately owned |
| `THM-M-1518` | same title and same broad physical-system gloss; Maupertuis/Hamilton attribution and 1744 | possible duplicate or alternate catalog source; no accepted identity/transport |
| `THM-P-0748` | actual motion makes `S = integral L dt` extremal | more specific physics formulation, outside this target and Stage1 set |
| `THM-P-0749` | Euler-Lagrange as a necessary variational condition | logically related but separately cataloged conclusion |

The existing `THM-M-1518` dossier selects a stationary-action-to-Euler-Lagrange implication, while
its legacy `S1-M-187` statement material contains the converse direction. That mismatch is useful
discovery evidence that implication direction is proposition-changing. Neither artifact belongs to
this target, and neither is imported or credited here.

## Lean boundary and source gate

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the discovery-only probe
elaborates interval-calculus and local-extremum derivative APIs. A bounded search over pinned mathlib
and repository-local Lean sources found no terminal source-identical declaration for the unresolved
`THM-M-1382` claim; the same-label foreign target is explicitly excluded from credit. This is not an
exhaustive external audit or a formal absence theorem.

Before statement elaboration, accountable reviewers must select one immutable source proposition,
freeze every incorporated definition, ordered binder, hypothesis, conclusion and degenerate case,
audit editions/corrections and historical-to-modern translation, decide the duplicate/neighbor
boundaries, and approve the source mapping. Only then may the next phase choose minimal imports,
serialize an elaborated expression, compile checked transports, and run the required statement
mutations.
