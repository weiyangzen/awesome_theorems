# Source-statement crosswalk

## Available source record

`Docs/researches/math_theorems.md` supplies only the Chinese title "下半连续性", attribution to
multiple mathematicians, twentieth century, the statement "泛函的下半连续性", high importance,
and the untrusted label `已验证`. `Docs/Stage0_Blueprint.md` repeats these fields while leaving exact
definitions, premises, proof, axioms, equivalent formulations, and machine artifacts open. There is
no bibliography, edition, theorem number, page, or errata record.

No primary-source candidate is consequently asserted at intake. Lower semicontinuity is a broad
notion and a hypothesis in many existence theorems, not one canonical proposition. Choosing an
inequivalent member of that family would invent missing mathematics.

## Crosswalk

| Source element | Mathematical information fixed | Lean information required | Intake result |
|---|---|---|---|
| "functional" | some map on an unspecified space | domain, codomain, topology and concrete map | unresolved |
| "lower semicontinuity" | a qualitative continuity property | exact definition and order/topological conventions | unresolved |
| PDE / variational neighborhood | broad subject context | chosen function space and convergence mode | insufficient |
| twentieth century / multiple authors | broad history | none | no theorem identity |
| `已验证` | untrusted repository label | inspectable proof and kernel receipt | no credit |

The first downstream gate is primary-source identification. Before `H0`, an independent reviewer
must verify edition, theorem/page, assumptions, definitions, and errata. Before statement credit,
the resulting row-by-row claim must elaborate as one canonical Lean expression with any alternate
encoding connected by checked transports. No repo-local or upstream Lean candidate has been audited
in this intake phase.
