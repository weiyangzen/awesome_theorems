# Source-statement crosswalk

## Repository sources

The authoritative local discovery row is `Docs/researches/math_theorems.md` under
`可计算性理论`. It supplies a field name and the circular gloss "the theory of computable
functions", not a theorem. `Docs/Stage0_Blueprint.md` reproduces it and explicitly leaves the exact
definition, assumptions, proof, equivalent formulations, axiom use, and machine artifact open.

`Docs/researches/cs_theorems.md` is useful negative evidence for scope: its computability section
contains dozens of non-equivalent named theorems under the same field heading. It does not say that
their conjunction is THM-M-0715, and its individual entries are not silently imported into this
mathematics target.

## Crosswalk

| Source component | Mathematical interpretation | Pinned Lean discovery surface | Intake status |
|---|---|---|---|
| `可计算性理论` | a mathematical field | `Mathlib.Computability.*` module family | subject only, not a proposition |
| "computable functions" | could mean total, partial-recursive, or machine-computable functions | `Computable`, `Partrec`, `Nat.Partrec`, `TM2Computable` | multiple non-identical encodings |
| basic recursive-function theory | primitive recursion, minimization, closure, enumeration | `Nat.Primrec`, `Nat.Partrec.Code`, `Nat.Partrec.Code.exists_code` | candidate theorem families only |
| undecidability branch | halting or extensional semantic properties | `ComputablePred.halting_problem` | separate possible consequence, not selected |
| machine-model branch | operational Turing-machine computation and simulations | `TM2Computable`, `PartrecToTM2` | exact equivalence target not supplied |
| `已验证` | untrusted catalog status | no expression or kernel receipt | explicitly rejected as evidence |

## Source blocker

No primary mathematical source is identified by author, title, immutable edition, theorem/section,
page, assumptions, proof boundary, or errata. Historical sources by Church, Kleene, and Turing are
candidate source families only; choosing a theorem from them without a pinpoint would invent the
root. The first downstream gate is therefore source identification and exact statement selection.

## Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the intake probe checks
representative definitions and theorems from recursive-function, enumerability, halting, and
Turing-machine APIs. This proves only that those names elaborate in the pinned environment. It is
not an anchor audit, expression fingerprint, model-equivalence certificate, or root proof.
