# Source-statement crosswalk

## Available source record

`Docs/researches/math_theorems.md` provides the title "L^p estimate", attribution to multiple
mathematicians, the twentieth century, and the statement "an estimate of the L^p norm of solutions".
`Docs/Stage0_Blueprint.md` repeats this wording while leaving exact definitions, hypotheses, proof,
dependencies, axioms, and machine artifact open. Neither record supplies a bibliography, edition,
theorem number, page, or errata.

There are many inequivalent PDE `L^p` estimates. Consequently no primary-source candidate or
canonical theorem is asserted at intake. Choosing one now would substitute mathematics not fixed by
the source. The source label `已验证` receives no human-proof or kernel-proof credit.

## Crosswalk

| Source element | Mathematical information fixed | Lean information required | Intake result |
|---|---|---|---|
| "solutions" | an unspecified equation has solutions | operator, equation, data, solution predicate | unresolved |
| `L^p` | some integrability exponent and measure are involved | measure space, codomain norm, `p` representation and range | unresolved |
| "norm" | a quantitative functional is bounded | exact `snorm`/Lp-space encoding and finiteness hypotheses | unresolved |
| "estimate" | an inequality with an implicit right-hand side and constant | both sides, order, constant and dependencies | unresolved |
| twentieth century / multiple authors | a broad theorem family | none | insufficient to identify a theorem |
| `已验证` | untrusted repository label | inspectable declaration and kernel receipt | no credit |

## Lean and source boundary

No repo-local Lean declaration is linked to THM-M-1170 by the available records, and intake does not
adopt a merely similar theorem. The downstream statement gate must first identify a primary source,
then record edition, theorem/page, definitions, assumptions, proof boundary, and errata. Only after
independent row-by-row review may it freeze a canonical Lean expression and checked transports.
