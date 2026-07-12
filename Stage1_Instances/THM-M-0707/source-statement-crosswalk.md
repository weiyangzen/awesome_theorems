# Source-statement crosswalk

## Repository sources

`Docs/researches/cs_theorems.md` gives the fullest repository wording: no Turing machine decides
for an arbitrary Turing machine and input whether it halts. It attributes the result to Alan
Turing in 1936. `Docs/Stage0_Blueprint.md` repeats the title and shorter claim while leaving exact
definitions, hypotheses, proof route, equivalent formulations, logical principles, and machine
artifact open. These are secondary inventory records, not `H0` evidence.

## Candidate primary source

Alan M. Turing, *On Computable Numbers, with an Application to the Entscheidungsproblem*,
Proceedings of the London Mathematical Society, series 2, volume 42 (1936-1937), pages 230-265,
is the historical candidate behind the repository record. Turing's paper uses machine
"circularity" and related decision problems rather than the repository's exact modern sentence.
This intake did not independently preserve and inspect a fixed scan to approve the exact section,
page, definitions, implication to the modern arbitrary-machine/input formulation, corrections, or
errata. The citation is therefore a discovery lead, not `E4`/`H0` evidence.

## Crosswalk

| Repository phrase | Material mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "Turing machine" | finite machine descriptions and configurations | concrete machine type, encoding, and valid-code policy | model open |
| "given input" | initial configuration determined by machine and input | explicit input type and initialization function | convention open |
| "halts" | a halting configuration is reached after finitely many steps | transition semantics and existential finite-step predicate | semantics open |
| "can decide" | one total effective Boolean procedure is correct both ways | computability predicate plus total decider and `Bool` correctness | exact contract open |
| "arbitrary" | universal quantification over the selected valid domain | ordered binders over every machine/code and input | domain open |
| "does not exist" | undecidability conclusion | negated existential over the uniform decider | formal expression open |
| `已验证` | untrusted inventory status | no proposition or proof component | rejected as evidence |

## Lean and machine boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the bounded
`IntakeProbe.lean` imports `Mathlib.Computability.PartrecCode` and checks
`Nat.Partrec.Code`, its partial evaluator `Nat.Partrec.Code.eval`, the computability predicates,
the universal evaluator result `Nat.Partrec.Code.eval_part`, and `Nat.Partrec.Code.smn`. This is a
credible alternate computability interface, but the intake does not locate a root theorem saying
that the evaluator's domain is undecidable. Nor is a checked equivalence to the repository's
Turing-machine claim supplied. Accordingly the root remains `M4`; a full immutable candidate and
terminal-body search belongs to the later anchor-audit phase.

Before `H0`, an independent source reviewer must approve a fixed primary-source formulation and a
premise/transition/conclusion crosswalk, including the relation between Turing's terminology and
the modern claim. Before statement credit, a formal reviewer must approve the elaborated Lean
expression, all boundary choices, and checked transports for every credited alternate encoding.
