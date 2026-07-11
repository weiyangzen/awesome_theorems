# Source-statement crosswalk

## Repository source

At base revision `23e8c7fd5602b359d75252bd4e37074a071f0c68`,
`Docs/researches/math_theorems.md` supplies the name `泊松过程`, attribution `Siméon Poisson`, year
`1837`, the text `计数过程的基本模型`, importance `高`, and status `已验证`. The Stage0 projection
repeats those fields and explicitly leaves exact definitions, premises, proof route, dependencies,
axioms, and machine artifacts pending. The status is untrusted metadata under rev-5.6.

| Required claim component | Available source text | Intake result |
|---|---|---|
| Theorem identity | `泊松过程` (Poisson process) | Names an object/family, not a unique theorem |
| Claim text | `计数过程的基本模型` | Describes the object's role; it has no truth-valued conclusion |
| Time domain | absent | Discrete time, continuous nonnegative time, or a general measurable index is undecided |
| Parameters | absent | Homogeneous rate, intensity measure, and admissible zero/infinite cases are undecided |
| Probability data | absent | Probability space, filtration, adaptation, and measurability are undecided |
| Defining axioms | absent | Initial value, path regularity, independent/stationary increments, and small-time laws are undecided |
| Hypotheses and conclusion | absent | No ordered binders, premises, or result can be frozen |
| Attribution | Siméon Poisson, 1837 | Historical metadata without a publication, edition, page, or theorem anchor |
| Formal status | `已验证` | Supplies neither an exact Lean target nor proof provenance; no machine credit |
| Lean candidate | absent | Selecting one would precede and bias the exact-statement decision |

## Non-equivalent candidate families

The following are recovery categories, not alternate encodings and not claims adopted by this
dossier: defining a homogeneous counting process; proving existence; proving uniqueness in law;
deriving Poisson-distributed increments; characterizing the process by exponential interarrival
times; characterizing it by a compensated martingale; or proving a Poisson limit theorem. These
have materially different domains, assumptions, and conclusions. Even the common increment and
interarrival descriptions require explicit equivalence transports before they can share credit.

## Recovery requirement

An authoritative scope amendment must provide an exact proposition or an unambiguous theorem
citation. A later source audit must then pin an edition and theorem/page, map every parameter,
binder, hypothesis, and conclusion, inspect errata, and obtain independent review. Until that
happens, choosing a familiar Poisson-process theorem would be substitution rather than faithful
formalization; `H0`, an exact Lean statement, and proof search all remain ineligible.
