# Source-statement crosswalk

| Claim component | Repository source anchor | Exact information present | Intake assessment |
|---|---|---|---|
| Identity | `Docs/Stage1_Targets_rev-5.6.json`, rank 442 | ID `THM-M-1265`, Chinese name `直接法`, category PDE, untrusted status `已验证` | Establishes manifest membership only |
| Historical description | `Docs/Stage0_Blueprint.md`, `THM-M-1265` | “变分问题的直接求解”; attributed to numerous mathematicians, with 1900 recorded | Does not state a proposition or assumptions |
| Research seed | `Docs/researches/math_theorems.md`, heading `直接法` | Attributes the method to David Hilbert and repeats “变分问题的直接求解” | Secondary discovery note; no citation, theorem number, or proof |
| Exact human theorem | none located in the required repository sources | No ambient space, admissible set, functional, topology, hypotheses, or conclusion | `H5`: the claimed theorem is presently unidentifiable |
| Lean target | none selected | Several inequivalent direct-method existence principles are possible | `M4`: choosing one without a source decision would be substitution |

The method usually combines a minimizing sequence, a compactness mechanism, and lower
semicontinuity to obtain a minimizer. This is context only, not a canonical statement and not proof
evidence. In particular, the following are not interchangeable without checked implications:

- a lower-semicontinuous extended-real functional on a nonempty compact topological space;
- a coercive weakly lower-semicontinuous functional on a reflexive Banach space;
- a sequential formulation on a weakly sequentially compact admissible set;
- a problem-specific Sobolev-space existence theorem for a PDE functional.

Resolution requires a primary or authoritative source pinpoint with an exact theorem statement and
assumptions, or an explicit master scope decision bound to this repository ID. The later source
audit must then record an immutable edition/revision, premise-to-statement mapping, errata search,
and reviewer. Until that occurs there is no honest source-to-Lean crosswalk, no alternate encoding
to credit, and no `H0` or machine-closure claim.
