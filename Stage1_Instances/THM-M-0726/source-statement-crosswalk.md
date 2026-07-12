# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` records `概率复杂性类`, attributes it to many mathematicians in
the 1970s, and gives only `BPP, RP, ZPP等类` ("BPP, RP, ZPP, and other classes").
`Docs/Stage0_Blueprint.md` repeats that phrase while leaving exact definitions, premises, proof
route, dependencies, axioms, and formal artifacts open. The rev-5.6 manifest carries `已验证` only
as `source_status_untrusted`.

The phrase is an enumeration, not a truth-valued proposition. It supplies no randomized model,
probability space, time semantics, error threshold, ordered quantifiers, hypotheses, or conclusion.

## Source-discovery boundary

Foundational papers by Gill on probabilistic Turing machines, by Rabin on randomized algorithms,
and by later authors establishing common BPP/RP/ZPP characterizations are plausible source families.
They contain multiple definitions and results, and a bibliographic association does not select one
as this target. The statement phase needs an accountable scope decision and independent inspection
of an immutable edition with a pinpoint statement, referenced definitions, assumptions, proof
boundary, and errata. No primary source is accepted at intake and no `H0` credit is assigned.

| Repository phrase | Possible mathematical component | Lean discovery candidate | Intake status |
|---|---|---|---|
| probabilistic classes | classes of languages decided by randomized machines | `Language` plus a future randomized-machine predicate | no class declaration selected or located |
| polynomial time | polynomial resource bound relative to an encoding | `Turing.TM2ComputableInPolyTime` | deterministic API anchor only |
| randomized choice | discrete distribution of outcomes or transitions | `PMF`, `PMF.pure`, `PMF.bind` | probability vocabulary only |
| BPP | bounded two-sided error | no single pinned declaration identified | threshold and time semantics open |
| RP / coRP | bounded one-sided error | no single pinned declaration identified | acceptance side and threshold open |
| ZPP | zero error with randomized polynomial-time semantics | no single pinned declaration identified | expected/worst-case convention open |
| verified | alleged prior formal status | none | explicitly untrusted; no proof credit |

## Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, module
`Mathlib.Computability.TuringMachine.Computable` provides deterministic time-bounded and
polynomial-time computation, while `Mathlib.Probability.ProbabilityMassFunction.Monad` provides
discrete probability mass functions with pure and bind. `IntakeProbe.lean` checks these types and
`Language`. This establishes only that some encoding ingredients exist. It does not define a
probabilistic Turing machine, fix a complexity-class convention, select a source proposition, or
prove a relation among BPP, RP, and ZPP. Formal candidate discovery remains a later dependent phase.
