# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` records `加权范数不等式`, Benjamin Muckenhoupt, 1972, and the
single gloss `A_p权与算子有界性` ("A_p weights and operator boundedness"). Stage0 repeats it while
marking the exact definitions, assumptions, proof path, equivalent forms, axioms, and machine
artifact as missing. The rev-5.6 manifest retains `已验证` only as `source_status_untrusted`.

Thus the repository record identifies a subject and likely historical neighborhood, not an exact
claim. It supplies no operator, domain, exponent range, quantified constant, theorem/page, proof
source, or errata record.

## Primary-source locator, not accepted crosswalk

A high-priority locator for source audit is Benjamin Muckenhoupt, *Weighted norm inequalities for
the Hardy maximal function*, Transactions of the American Mathematical Society 165 (1972),
207-226. Its title, author, and date align with the metadata and suggest the Hardy-Littlewood
maximal-operator characterization. During this intake no immutable scan and pinpoint theorem/page
passage was independently inspected, so this bibliographic locator does not establish `H0` and
does not authorize transcription of a formal target.

## Crosswalk

| Repository phrase | Possible mathematical component | Lean representation candidate | Intake status |
|---|---|---|---|
| `A_p` weight | product of averages of `w` and a negative power of `w` over balls/cubes | measures, `lintegral`, powers, supremum over measurable sets | convention and boundaries open |
| weighted norm | `L^p(w dx)` norm or an explicitly weighted integral | `Measure.withDensity`, `eLpNorm`, `MemLp` | APIs probed; exact scalar/codomain open |
| operator | plausibly the Hardy-Littlewood maximal operator | requires a source-exact operator definition | absent from repository statement |
| boundedness | existence of `C` with an operator norm inequality | quantified `eLpNorm` inequality | direction and constant dependence open |
| `已验证` | untrusted inventory label | no proposition or proof term | explicitly rejected as evidence |

## Required source audit

The next source pass must retain an immutable copy or digest, record the exact definition and
theorem numbers/pages, transcribe all assumptions and conclusions, check edition and errata, and
map each source clause to the canonical human claim and Lean binder. Independent review is needed.
Only after that pass can the likely maximal-function reading displace the competing readings.

## Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the bounded probe
checks `Measure.withDensity`, `withDensity_apply`, `eLpNorm`, `MemLp`, `lintegral`, and measure
restriction. These are representation ingredients only. A bounded name/text search found no
Muckenhoupt or `A_p` weight definition and no Hardy-Littlewood maximal-function theorem; this is
not the later immutable anchor audit and receives no `M0` credit.
