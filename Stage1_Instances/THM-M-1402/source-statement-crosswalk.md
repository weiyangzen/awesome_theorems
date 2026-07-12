# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` records the title `移位映射`, attributes it to "many
mathematicians", dates it only to the twentieth century, and gives the complete statement gloss
`符号空间上的移位` ("shift on symbolic space"). It supplies no bibliography, definition,
quantifiers, hypotheses, conclusion, proof, or formal artifact. The record was added to this
repository in commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`; that is repository provenance,
not a mathematical source revision.

`Docs/Stage0_Blueprint.md` repeats the gloss while explicitly leaving definitions and premises,
proof process, dependency graph, equivalent formulations, axioms, machine status, and artifact
links open. The rev-5.6 manifest preserves `已验证` only in `source_status_untrusted`.

## Crosswalk

| Repository phrase | Possible mathematical component | Prospective Lean component | Intake status |
|---|---|---|---|
| "symbolic space" | one-sided full shift `A^Nat` | `Stream' A` or `Nat -> A` | candidate encoding only; alphabet and space open |
| "symbolic space" | two-sided full shift `A^Int` | `Int -> A` | candidate encoding only; source does not select it |
| "symbolic space" | a shift-invariant subspace | subtype/set plus topology or measurable structure and an invariance proof | absent from source |
| "shift" | coordinate precomposition, commonly `x(n) -> x(n + 1)` | `Stream'.tail` or a function on a Pi type | direction and index type open |
| possible topological reading | continuity or a two-sided homeomorphism in product topology | `continuous_pi`, `continuous_apply`, `Homeomorph.piCongrLeft` | APIs probed; no conclusion supplied |
| possible dynamical reading | periodic points, transitivity, mixing, dense periodic points, or entropy | iterates and `Function.IsPeriodicPt`, plus further definitions | materially different candidate theorems |
| `已验证` | untrusted inventory label | no Lean proposition or proof object | explicitly rejected as evidence |

## Source and Lean boundary

No primary or authoritative theorem source is identified at intake. The statement phase must first
select and independently inspect an immutable source passage, record edition, definition/theorem
and page, assumptions, conclusion, proof boundary and errata, and justify why its proposition is
the repository target rather than a convenient fact about shifts. Only then can it freeze ordered
binders, universes, boundary cases, minimal imports, an elaborated expression, and mutation tests.
The provisional human-source status is therefore `H5`: the supplied target is not a stable
proposition. This classification does not say that a corrected, source-selected theorem about
shift maps is false; it requires the statement phase to redirect the topic label to an approved
exact proposition before ordinary theorem-proof execution.

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the bounded intake
probe checks `Stream'.tail`, product-topology continuity primitives, Pi reindexing, and the generic
periodic-point predicate. A bounded name search found no obvious symbolic/full-shift framework in
pinned `Mathlib/Dynamics`. These observations are discovery inputs only, not the downstream
immutable anchor audit, an absence claim about external projects, or statement/proof evidence.
