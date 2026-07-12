# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` gives the title `深度受限电路`, collective attribution, the
period "1980s", and only the gloss `电路深度的下界` ("lower bounds on circuit depth"). Stage0
repeats this metadata while explicitly leaving definitions, assumptions, proof path, dependencies,
axioms, and machine artifacts open. The rev-5.6 manifest preserves `已验证` only as the untrusted
source-status label.

The nearby repository entries for general circuit complexity, Frege systems, and monotone circuit
lower bounds do not select a theorem for this target. Adjacency is not source evidence.

## Crosswalk

| Repository phrase | Possible mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "circuit" | a finite DAG or formula over a fixed Boolean gate basis | syntax, well-formedness, evaluation | absent; model open |
| "depth-bounded" | constant, bounded, or parameterized depth | depth definition and family convention | ambiguous |
| "lower bound" | exact or asymptotic inequality, possibly subject to a size bound | ordered quantifiers and numerical relation | absent |
| possible `AC^0` reading | a named function family evades polynomial-size constant-depth circuits | unbounded-fan-in AND/OR/NOT circuits and size families | candidate only |
| possible bounded-fan-in reading | information propagation forces logarithmic depth | bounded fan-in, dependency/support invariant | candidate only |
| possible tradeoff reading | size lower bound as a function of allowed depth | exact class, function, and asymptotic statement | candidate only |
| `已验证` | untrusted inventory label | no Lean proposition or proof credit | explicitly rejected |

## Source work required

The statement phase must select an immutable primary or authoritative source passage and record its
edition, theorem number/page, exact circuit conventions, quantifiers, hypotheses, lower bound,
proof boundary, and errata. Independent review must verify that the selected proposition is the
intended repository target. Until then, assigning a named theorem or historical author would be
speculation rather than an `H0` crosswalk.

## Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the narrow intake
probe imports `Mathlib.Data.Fintype.BigOperators` and checks finite Boolean types, finite function
spaces, and finite input vectors. These are generic encoding ingredients only. A bounded name
search found no obvious Boolean circuit-depth framework or lower-bound theorem in pinned mathlib;
that negative search is not the later immutable anchor audit.
