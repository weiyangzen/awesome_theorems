# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` twice records only the title `去随机化`, the collective
attribution "many mathematicians", the period "1990s", and the gloss `随机算法的确定化`.
`Docs/Stage0_Blueprint.md` repeats those fields and explicitly leaves the background, exact
definitions and premises, proof route, axioms, and formal artifact open. The manifest correctly
retains `已验证` only as `source_status_untrusted`.

No named theorem, randomized machine model, complexity class, error bound, hardness premise,
conclusion, edition, theorem/page, proof source, errata record, or formal declaration is supplied.
The nearby repository research table lists Adleman's, Nisan-Wigderson's, and
Impagliazzo-Wigderson's results as separate entries. That is evidence that these are distinct
possible neighboring topics, not evidence that any one is the intended target.

## Source-statement crosswalk

| Repository phrase | Possible mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "randomized algorithm" | probabilistic TM, RAM, circuit, or distribution over algorithms | selected machine plus input/random encodings | model absent |
| "determinization" | seed fixing, advice simulation, PRG replacement, or class equality | exact quantifier order and simulator proposition | conclusion absent |
| success | bounded error, one-sided error, expectation, or promise | probability/PMF and threshold predicate | criterion absent |
| efficiency | polynomial time/space, circuit size, or unrestricted termination | cost model and asymptotic bound | resource claim absent |
| "1990s" / many authors | historical topic metadata | pinpoint immutable source and errata audit | not a citation |
| `已验证` | untrusted inventory label | no proposition or proof credit | rejected as evidence |

## Required source work

The next phase needs an immutable, independently inspected source passage identifying one exact
theorem. It must record bibliographic edition/revision, theorem and page, definitions, every
assumption, proof boundary, and errata, then explain why the selected result rather than its
neighbors matches this repository UID. Until then, assigning a named result or an `H0` human proof
would be invented provenance.

## Lean boundary

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, `IntakeProbe.lean` imports
the finite-uniform-distribution and polynomial-time Turing-machine interfaces and checks six API
types. These are possible vocabulary only. The bounded repo/mathlib search found no declaration
that can be crosswalked to the unspecified claim; this is not a substitute for the later immutable
anchor audit.
