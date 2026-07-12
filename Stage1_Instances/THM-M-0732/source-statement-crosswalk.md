# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` gives the title `电路复杂性`, collective attribution, the
period "1980s", and the gloss `布尔电路的下界` ("Boolean-circuit lower bounds"). Stage0 repeats
that metadata and explicitly leaves exact definitions, assumptions, proof path, dependencies,
axioms, and machine artifacts open. The rev-5.6 manifest carries `已验证` only in the untrusted
source-status field.

`Docs/researches/cs_theorems.md` confirms the ambiguity rather than resolving it: its circuit
complexity section separately lists Shannon counting, Lupanov's upper bound, `PARITY` versus
`AC^0`, monotone `CLIQUE` bounds, modular lower bounds, the switching lemma, and other results. It
does not cross-reference `THM-M-0732` to one row or supply a primary-source edition and passage.

## Crosswalk

| Repository phrase | Possible mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "Boolean circuit" | a finite DAG/formula over a fixed gate basis | circuit syntax, well-formedness, evaluation | absent; model open |
| "complexity" | size, depth, formula size, or another resource | a precise measure and family convention | absent |
| "lower bounds" | exact, asymptotic, worst-case, or almost-everywhere inequality | ordered quantifiers and numerical relation | absent |
| possible Shannon reading | most `n`-ary functions need exponential-size circuits | counting, circuit enumeration, asymptotics | candidate only |
| possible `AC^0` reading | a named function family evades bounded-depth polynomial-size circuits | circuit families, depth/size bounds, uniformity convention | candidate only |
| possible monotone reading | a monotone function needs large monotone circuits | monotone gates/functions and exact bound | candidate only |
| `已验证` | untrusted inventory label | no Lean proposition or proof credit | explicitly rejected |

## Source work required

The statement phase must select an immutable primary or authoritative source passage and record its
edition, theorem number/page, exact circuit conventions, quantifiers, hypotheses, bound, proof
boundary, and errata. Independent review must verify that this selection is the intended repository
target. Until then, an author, named theorem, or exact historical date cannot truthfully be assigned.

## Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the narrow intake
probe imports `Mathlib.Data.Fintype.Card` and checks finite types, Boolean cardinality, finite
function-space cardinality, and finite input vectors. These are generic encoding ingredients only.
The bounded mathlib source search found no obvious Boolean circuit-complexity framework or lower
bound declaration. This negative name search is not the later immutable anchor audit.
