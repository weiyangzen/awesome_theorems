# Source-statement crosswalk

| Claim component | Available source anchor | Lean target | Intake assessment |
|---|---|---|---|
| Target identity | `Docs/Stage0_Blueprint.md`, `THM-M-1158`, title `单层位势` | none frozen | Identifies a topic/object, not a proposition |
| Claimed content | Same entry: `边界积分表示` (boundary integral representation) | none frozen | Formula, quantifiers, hypotheses, and conclusion are absent |
| Verification label | Same entry: `已验证` | none | Explicitly untrusted under rev-5.6; conveys no proof credit |
| Attribution and date | Same entry: `众多数学家`, `19世纪` | not applicable | Too broad for source fidelity or premise mapping |
| Formalization target | Same entry says the formal system is to be selected | Lean 4 required by rev-5.6 | No historical machine artifact is identified |

## Ambiguity ledger

The phrase can plausibly refer to the integral defining a single-layer potential, a
representation formula for solutions, harmonicity away from the boundary, continuity
of traces, or a jump relation for normal derivatives. These claims have different
assumptions and conclusions. Selecting any one from the title alone would substitute a
theorem and violate the exact-statement gate.

An authoritative source must supply, at minimum: a pinpoint statement; ambient
dimension and scalar field; the fundamental solution and its normalization; domain and
boundary regularity; density/function spaces; integration measure; evaluation region;
and the exact equality, regularity, trace, or jump conclusion. Edition/revision, page or
theorem number, assumptions, and errata must then be crosswalked before `H0` is possible.

No primary mathematical source or Lean candidate is credited at intake. The repository
metadata is a provenance anchor for the task wording only, not evidence of mathematical
closure.
