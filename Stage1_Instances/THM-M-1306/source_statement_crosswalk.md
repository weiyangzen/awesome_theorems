# Source-statement crosswalk

| Claim component | Available source anchor | Lean target | Intake assessment |
|---|---|---|---|
| Theorem identity | `Docs/researches/math_theorems.md`, entry "Chemin定理" | none | Names Jean-Yves Chemin, 1990, and `Euler方程的解析性`; this is secondary repository metadata, not a pinpoint primary source |
| Stage0 claim | `Docs/Stage0_Blueprint.md`, `THM-M-1306` | none | Repeats the same phrase and explicitly leaves precise definitions, assumptions, proof path, axioms, and artifacts unresolved |
| Stage1 eligibility | `Docs/Stage1_Targets_rev-5.6.json`, execution rank 474 | Lean 4 required | Membership and lane metadata only; `source_status_untrusted` is not evidence |
| Euler model | absent | none | PDE, dimension, domain, boundary conditions, and solution concept cannot be inferred safely |
| Analyticity predicate | absent | none | Variable of analyticity, function space, radius/norm, interval, and persistence conclusion are unknown |
| Assumptions and conclusion | absent | none | No ordered binders or exact proposition can be frozen |

No primary mathematical source is accepted at intake. In particular, a generic bibliographic match
for Chemin plus Euler would not suffice: the statement phase needs an edition/file pin and an exact
theorem/page crosswalk covering every assumption and conclusion. It must also check corrections or
errata and distinguish the claimed 1990 result from later results on particle trajectories,
Lagrangian regularity, geometric structures, or Gevrey/analytic persistence.

## Required source-resolution task

1. Locate the primary 1990-era Chemin publication meant by the repository metadata.
2. Quote and translate its exact theorem statement without strengthening or weakening it.
3. Record dimension, domain, equation, solution class, initial-data space, analytic variable and
   norm/radius, time interval, and all boundary or compatibility hypotheses.
4. Record edition, page/theorem number, stable identifier and content hash, plus errata findings.
5. Only then select a Lean expression and test alternative interpretations as non-equivalent
   mutations.

Until this task is complete, the source debt is `H4`, the machine debt is `M4`, and there is no
eligible proof target. No `H0`, Lean anchor, or machine closure is claimed.
