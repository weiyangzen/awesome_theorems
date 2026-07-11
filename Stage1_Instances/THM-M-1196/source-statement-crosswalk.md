# Source-statement crosswalk

## Available source record

The repository inventory `Docs/researches/math_theorems.md` records only the title "hyperbolic
equations", the statement "the wave equation and its generalizations", attribution to multiple
mathematicians, the twentieth century, and the label `已验证`. `Docs/Stage0_Blueprint.md` repeats
these fields while leaving exact definitions, assumptions, proof, dependencies, axioms, and machine
status open. No bibliography, edition, theorem number, page, or errata record is attached.

Thus no primary-source theorem is asserted at intake. The metadata describes a subject area rather
than a truth-valued proposition, and selecting one of its inequivalent results would substitute a
new theorem. The source label supplies no `H0` or machine-proof credit.

## Crosswalk

| Source element | Mathematical information fixed | Lean information required | Intake result |
|---|---|---|---|
| "hyperbolic equations" | a PDE family | concrete operator and hyperbolicity predicate | unresolved |
| "wave equation" | a representative second-order PDE | domain, derivatives, coefficients and equation | unresolved |
| "generalizations" | scope extends beyond the basic model | exact permitted class | unresolved |
| no conclusion stated | no theorem is selected | proposition: existence, uniqueness, estimate, propagation, etc. | unresolved |
| twentieth century / multiple authors | broad history only | none | insufficient to identify a theorem |
| `已验证` | untrusted repository label | primary proof or kernel receipt | no credit |

## Formalization boundary

No repository-local Lean module for `THM-M-1196` was found during intake. More importantly, even a
candidate library declaration cannot be matched exactly until the human claim is selected from a
primary source. The next gate is primary-source identification followed by an independently
reviewable edition/theorem/page/assumption/errata crosswalk. Only then may a canonical Lean target,
transports, imports, and mutation tests be frozen.
