# Source-statement crosswalk

## Available source record

`Docs/researches/math_theorems.md` gives the author Robert Brooks, year 1981, and only the statement
"volume growth and the essential spectrum". `Docs/Stage0_Blueprint.md` repeats those fields while
leaving definitions, premises, proof history, axioms, and machine artifacts open. The manifest
classifies the record as metadata-screened `L0 / rework_required`; its `已验证` value is explicitly
untrusted. No primary bibliography, theorem/page, edition, or errata record is attached.

A publication by Robert Brooks concerning the relation between the spectrum of a complete
Riemannian manifold and its volume growth is a plausible source-search lead. This intake does not
assert its title, journal metadata, theorem number, or formula as verified facts; those belong to
the downstream source audit against the primary document.

## Crosswalk

| Source element | Mathematical information fixed | Lean information required | Intake result |
|---|---|---|---|
| "Robert Brooks" / 1981 | distinguishes the spectral-geometric theorem family | source identity has no direct encoding | provisional identity only |
| "volume growth" | asymptotic growth of metric-ball volume is involved | manifold, metric balls, volume measure, growth functional | unresolved |
| "essential spectrum" | a Laplacian spectral invariant is involved | operator realization, spectrum API, bottom/infimum convention | unresolved |
| "relationship" | some theorem connects the two quantities | exact hypotheses, inequality direction and constants | unresolved |
| `已验证` | untrusted inventory status | inspectable proof and kernel receipts | no credit |

## Statement boundary

No canonical Lean declaration is frozen at intake. In particular, common recollections involving a
square of an exponential volume-growth rate and the bottom of essential spectrum are not adopted:
the primary source must establish the exact rate, coefficient, hypotheses, and convention first.
Only after a row-by-row source crosswalk and independent review may the statement phase claim H0 or
elaborate an exact Lean target. Mathlib and external formalization searches remain downstream work.
