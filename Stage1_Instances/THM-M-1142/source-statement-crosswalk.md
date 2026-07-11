# Source-statement crosswalk

## Available source record

`Docs/researches/math_theorems.md` gives the title, Axel Harnack, the year 1887, the phrase
"convergence of a sequence of harmonic functions", and the untrusted label `已验证`.
`Docs/Stage0_Blueprint.md` repeats those fields while leaving definitions, hypotheses, proof,
machine status, and artifact links open. Neither record provides a bibliography, edition, theorem
number, page, definitions, or errata. No primary-source candidate is asserted by this intake.

Several inequivalent results are called a Harnack convergence theorem or principle. Choosing among
monotone positive sequences, sequences locally bounded above, and compact-convergence formulations
would add hypotheses and conclusions absent from the source. Exact source identification is thus
the first downstream gate, and the secondary attribution/date remain unverified.

## Crosswalk

| Source element | Information fixed | Lean information required | Intake result |
|---|---|---|---|
| "harmonic functions" | members satisfy some harmonicity predicate | domain, codomain, Laplacian/mean-value definition and regularity | unresolved |
| "sequence" | a countable indexed family | binder order and index type, normally `Nat` | partly fixed |
| "convergence" | some limiting behavior | topology, local/global mode, finite limit or divergence alternative | unresolved |
| Harnack / 1887 | secondary attribution and date | no Lean content | requires primary-source verification |
| `已验证` | untrusted inventory label | inspectable source proof and kernel evidence | no credit |

## Formalization boundary

No target-specific Lean declaration or legacy priority slot was found. Before `H0`, an independent
review must verify a primary edition, theorem/page, definitions, assumptions, and errata and approve
a row-by-row source-to-claim mapping. Before statement acceptance, the canonical Lean expression
and any transports must elaborate under pinned minimal imports. Those are later phases, not intake
evidence.
