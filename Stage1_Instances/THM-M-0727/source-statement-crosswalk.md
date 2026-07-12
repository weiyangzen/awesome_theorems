# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` records `交互证明`, attributes it to Shafi Goldwasser, Silvio
Micali, and Charles Rackoff in 1985, and gives only `交互证明系统` ("interactive proof systems").
`Docs/Stage0_Blueprint.md` repeats that phrase while leaving exact definitions, premises, proof
route, dependencies, axioms, and formal artifacts open. The rev-5.6 manifest carries `已验证` only
as `source_status_untrusted`.

The phrase names a formal model, not a truth-valued proposition. It supplies no party model,
transcript, probability space, resource or round bound, error threshold, ordered quantifiers,
hypotheses, or conclusion.

## Source-discovery boundary

Goldwasser, Micali, and Rackoff's paper *The Knowledge Complexity of Interactive Proof Systems*
(SIAM Journal on Computing 18(1), 1989, pp. 186-208; preliminary version in STOC 1985) is a
plausible primary source family for the repository attribution. It contains definitions and
multiple results; bibliographic association does not select one of them as this target. The
statement phase needs an accountable scope decision and independent inspection of an immutable
edition with a pinpoint statement, referenced definitions, assumptions, proof boundary, and
errata. No primary source is accepted at intake and no `H0` credit is assigned.

| Repository phrase | Possible mathematical component | Lean discovery candidate | Intake status |
|---|---|---|---|
| interactive proof system | prover/verifier protocol and transcript semantics | future protocol structure over messages and randomness | no definition or proposition selected |
| language membership | completeness for members and soundness for nonmembers | `Language` plus future protocol predicates | language API is vocabulary only |
| efficient verifier | time-bounded probabilistic verifier | `Turing.TM2ComputableInPolyTime` plus a future randomized model | deterministic API anchor only |
| verifier coins | distribution of verifier outcomes/transcripts | `PMF`, `PMF.pure`, `PMF.bind` | discrete probability vocabulary only |
| verified | alleged prior formal status | none | explicitly untrusted; no proof credit |

## Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, module
`Mathlib.Computability.TuringMachine.Computable` provides deterministic time-bounded and
polynomial-time computation, while `Mathlib.Probability.ProbabilityMassFunction.Monad` provides
discrete probability mass functions with pure and bind. `IntakeProbe.lean` checks those types and
`Language`. This establishes only that some encoding ingredients exist. It does not define an
interactive protocol, fix completeness or soundness, select a source proposition, or prove an
interactive-proof result. Formal candidate discovery remains a later dependent phase.
