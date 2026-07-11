# Source-statement crosswalk

## Available source record

`Docs/researches/math_theorems.md` supplies only the title "local smoothing", attribution to
multiple mathematicians, twentieth century, the statement "local smoothing of solutions to
dispersive equations", importance "high", and `已验证`. `Docs/Stage0_Blueprint.md` repeats these
fields while leaving definitions, assumptions, proof, and machine status open. No bibliography,
edition, theorem number, page, or errata record is attached.

The same inventory separately lists a local smoothing conjecture and Sogge local smoothing theorem;
their presence confirms that this generic row cannot silently be identified with either one. No
primary-source candidate is asserted at intake.

## Crosswalk

| Source element | Mathematical information fixed | Lean information required | Intake result |
|---|---|---|---|
| "dispersive equations" | a broad PDE/evolution family | exact operator and solution/propagator definition | unresolved |
| "solutions" | evolved data are involved | initial data, solution notion, existence interval | unresolved |
| "local" | some localization is intended | time interval and/or spatial cutoff/weight | unresolved |
| "smoothing" | regularity gain or integrated estimate | derivative order, norms, exponents, constant | unresolved |
| twentieth century / multiple authors | broad historical family | none | insufficient to identify a theorem |
| `已验证` | untrusted repository label | inspectable human proof or kernel receipt | no credit |

## Existing Lean boundary

No target-specific Lean artifact was found. The numeric legacy hint `S1_M_142.lean` declares itself
to be `THM-M-1314: Penrose inequality`; it is a manifest/legacy-slot mismatch and is excluded rather
than repurposed. The first downstream gate is primary-source identification. Before `H0`, an
independent reviewer must verify edition, theorem/page, definitions, assumptions and errata, then
approve a row-by-row mapping to the canonical Lean statement.
