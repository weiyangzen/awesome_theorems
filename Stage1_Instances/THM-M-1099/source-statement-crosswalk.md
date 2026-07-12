# Source-statement crosswalk

## Available record and candidate source

The repository inventory supplies only the title "petite set", attribution to Meyn/Tweedie, the
year 1993, and the phrase "small sets and ergodicity". `Docs/Stage0_Blueprint.md` explicitly leaves
the definitions, hypotheses, proof path, axioms, and machine artifact open. Its `已验证` value is an
untrusted metadata label under rev-5.6.

A primary-source candidate is Sean P. Meyn and Richard L. Tweedie, *Markov Chains and Stochastic
Stability*, first edition, Springer-Verlag (1993). The immutable edition, definition/theorem number,
page, exact wording, assumptions, and errata have not been independently inspected in this intake.
The citation is therefore a discovery anchor only and supplies no `H0` credit.

## Crosswalk

| Repository/source element | Mathematical information fixed | Lean information required | Intake result |
|---|---|---|---|
| "petite set" | a set satisfying a sampled-kernel minorization notion | measurable set, iterated kernel, sampling law, mixture kernel, nonzero minorizing measure | notion family identified; conventions open |
| "small sets" | usually fixed-step kernel minorization | iteration index and measure inequality | relationship to the target unresolved |
| "ergodicity" | some long-run stability property | invariant measure and exact convergence/recurrence predicate | conclusion unresolved |
| Meyn/Tweedie, 1993 | likely monograph family | no proof credit | candidate edition identified only |
| `已验证` | repository screening metadata | accepted source review or kernel receipt | no credit |

## Statement and machine boundary

The phrase does not decide whether the target is a definition, a small/petite implication, a
T-chain result, a recurrence theorem, or an ergodic criterion. Those alternatives have different
hypotheses and conclusions, so choosing one without a theorem-level source anchor would substitute
mathematics.

A repository search found no theorem-specific Lean artifact for this target. Pinned mathlib does
contain substantial `ProbabilityTheory.Kernel` and `IsMarkovKernel` infrastructure, but the intake
search found no declaration named for petite sets. This is discovery information, not the required
immutable anchor audit and not evidence that the missing sampled-minorization or ergodicity APIs do
or do not exist under another name.

Before `H0`, an independent reviewer must verify the selected edition, definition and theorem/page,
all hypotheses, notation, proof boundary, and errata. Before statement credit, every approved
source component must map row by row to an elaborated canonical Lean expression.
