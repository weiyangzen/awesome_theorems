# Source-statement crosswalk

## Available source record

`Docs/researches/math_theorems.md` records only the title "nonlinear wave equation", attribution to
many mathematicians, twentieth century, and the statement "well-posedness theory of NLW", followed
by the untrusted status `已验证`. `Docs/Stage0_Blueprint.md` repeats this wording while leaving exact
definitions, hypotheses, proof route, axioms, and machine artifact open. No bibliography, edition,
theorem number, page, or errata record is supplied.

This record cannot select one theorem from the inequivalent local/global and subcritical/critical
well-posedness results. No primary-source candidate is asserted at intake.

## Crosswalk

| Source element | Mathematical information fixed | Information still required for Lean | Intake result |
|---|---|---|---|
| "nonlinear wave equation" | a nonlinear hyperbolic PDE family | exact equation, domain, dimension, nonlinearity | unresolved |
| `NLW` | conventional family abbreviation | definitions of data and solution | unresolved |
| "well-posedness" | intended existence/uniqueness/dependence theme | exact quantified clauses, spaces, topology, lifespan | unresolved |
| "theory" | potentially multiple results, not a proposition | select one canonical theorem without broadening | unresolved |
| twentieth century / many mathematicians | broad historical attribution | primary source and pinpoint theorem | insufficient |
| `已验证` | untrusted repository metadata | human proof crosswalk or kernel receipt | no credit |

## Statement and evidence boundary

No target-specific Lean module or declaration was located by the scoped repository search at
intake. This negative search is not an external anchor audit and does not establish nonexistence of
a formalization. The next gate must first identify the exact primary theorem; it must then map every
ordered binder, assumption, conclusion, and boundary case to a canonical Lean expression before
machine proof discovery can receive credit. `H0` additionally requires edition/theorem/page/errata
review, and `M0-*` requires actual pinned kernel closure.
