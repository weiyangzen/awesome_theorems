# Source-statement crosswalk

## Available source record

`Docs/researches/math_theorems.md` gives only the title "energy estimate", attribution to multiple
mathematicians, the twentieth century, and the phrase "the energy method for hyperbolic equations".
`Docs/Stage0_Blueprint.md` repeats it while leaving definitions, hypotheses, proof, axioms, and
machine artifacts unspecified. Neither record supplies a bibliography, edition, theorem number,
page, assumptions, or errata. No primary source can therefore be asserted at intake.

## Crosswalk

| Source element | Information actually fixed | Information still required for Lean | Intake result |
|---|---|---|---|
| "energy estimate" | some energy is bounded, controlled, or conserved | energy definition, norms, inequality, quantifiers | unresolved |
| "hyperbolic equations" | broad PDE family | operator/system, hyperbolicity notion, coefficients, domain | unresolved |
| "energy method" | intended proof technique | theorem proposition and admissible solution class | method, not a statement |
| twentieth century / multiple authors | broad historical context | primary edition and exact theorem | insufficient identification |
| `已验证` | untrusted metadata label | inspectable proof and kernel evidence | no credit |

## Formalization boundary

No legacy priority slot or target-specific Lean module is identified by the manifest, and repository
search found no target-specific artifact for `THM-M-1197`. Even if a wave-equation or Gronwall
result exists in mathlib, it cannot establish source identity without a chosen primary theorem.
The next gate is primary-source identification followed by an independently reviewed, row-by-row
mapping of every binder, hypothesis, definition, boundary case, and conclusion to a canonical Lean
expression. Until then H4/M4/R4 remains fail-closed.
