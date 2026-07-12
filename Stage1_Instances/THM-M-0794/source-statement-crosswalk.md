# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` records the Chinese title `适当力迫`, attributes it to Saharon
Shelah, gives the year 1982, and states only `保持基数的力迫` ("cardinal-preserving forcing").
Stage0 repeats the phrase and explicitly leaves definitions, assumptions, proof route,
dependencies, axioms, and artifacts open. The rev-5.6 manifest preserves `已验证` only as
`source_status_untrusted`. No definition, theorem, binders, hypotheses, conclusion, edition, page,
proof source, errata, or formal artifact is supplied.

The nearby inventory entries `适当力迫公理`, `迭代力迫`, and `力迫公理` show why title matching is
not enough: these are distinct targets and cannot provide this target's statement by adjacency.

## Candidate source work

Shelah's original work and authoritative set-theory monographs are candidate locators, but no
edition or passage is accepted at intake. The source audit must identify a passage stating the
intended definition and exact theorem, record edition, definition/theorem number and page,
foundation and model assumptions, proof boundary, and errata, and obtain independent review. The
generic attribution and year do not establish statement identity or `H0`.

## Crosswalk

| Repository phrase | Possible mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "forcing" | a preorder/partial order, generic filter, names, and extension semantics | order APIs plus a set-theoretic model/forcing encoding | only nearby order APIs probed; semantic encoding open |
| "proper" | master/generic conditions for countable elementary submodels | countable model, elementarity, dense-set/genericity, and condition predicates | definition absent; no substitute admitted |
| "preserves" | comparison between ground model and generic extension | checked interpretation and invariance theorem | relation and direction absent |
| "cardinals" | `ω₁`, selected cardinals, or all cardinals | ordinal/cardinal representation and extension comparison | scope ambiguous; nearby cardinal APIs probed |
| Shelah, 1982 | historical metadata | immutable source identity and pinpoint passage | insufficient for statement freeze |
| `已验证` | untrusted inventory label | no Lean proposition or proof credit | explicitly rejected as evidence |

## Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the bounded intake
probe imports `Mathlib.Order.Ideal`, `Mathlib.SetTheory.Cardinal.Aleph`, and
`Mathlib.SetTheory.ZFC.Cardinal`. It checks preorders, order ideals/cofinal sets, `ω₁`, ZFC sets, and
ZFC-set cardinality. Mathlib's order-ideal module describes its cofinal sets as dual to dense sets
used in forcing and contains a Rasiowa-Sikorski-style construction, but that is not an encoding of
proper forcing or generic extensions. A bounded case-insensitive search found no `proper forcing`
occurrence in pinned mathlib. This intake observation is not the later immutable anchor audit and
makes no claim about all external Lean projects.
