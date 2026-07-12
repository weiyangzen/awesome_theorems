# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` names Ernst Zermelo, dates the result to 1904, and states
`任意非空集合族存在选择函数` ("every family of nonempty sets has a choice function"). Stage0
repeats that gloss. The manifest deliberately preserves `已验证` only as an untrusted source label.

## Located primary source

The historical locator is Ernst Zermelo, *Beweis, dass jede Menge wohlgeordnet werden kann*,
`Mathematische Annalen` 59 (1904), 514-516. It is the primary well-ordering paper associated with
Zermelo's choice principle. Intake does not claim `H0`: the exact German formulation, page-level
passage, a controlled translation, assumptions, contemporary set-family conventions, errata, and
independent review must still be recorded in the source-audit work.

## Crosswalk

| Repository phrase | Mathematical component | Candidate Lean component | Intake status |
|---|---|---|---|
| "family" | index type and indexed fibers | `(i : Sort u) (A : i → Sort v)` | scope fixed; universes open |
| "nonempty" | each fiber has an inhabitant propositionally | `∀ j, Nonempty (A j)` | candidate elaborated |
| "choice function" | simultaneous dependent selector | `Nonempty (∀ j, A j)` | candidate elaborated |
| "axiom" | foundational principle, not a choice-free theorem | `Classical.choice`, `Classical.axiomOfChoice` | pinned APIs probed |
| `已验证` | untrusted inventory status | no proof credit | rejected as evidence |

## Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, importing
`Mathlib.Logic.Basic` exposes `Classical.choice` and `Classical.axiomOfChoice`. The intake probe also elaborates
the dependent-family proposition corresponding to the repository gloss. These observations locate
the formal surface only. Exact declaration selection, `#print axioms`, equivalence transports,
mutation tests, provenance closure, and theorem credit belong to downstream phases.
