# Source-statement crosswalk

| Claim component | Human source family | Formal candidate | Intake assessment |
|---|---|---|---|
| Reciprocity for CM values/special points | G. Shimura, *Introduction to the Arithmetic Theory of Automorphic Functions*, Princeton University Press, 1971, complex multiplication and canonical-model chapters | no exact Lean declaration frozen | Primary monograph identified, but edition page/theorem pinpoint and errata review remain open |
| Reflex field and reflex norm | G. Shimura and Y. Taniyama, *Complex Multiplication of Abelian Varieties and Its Applications to Number Theory*, Publications of the Mathematical Society of Japan 6, 1961 | legacy `CMReciprocityInput.reflexField` is not an encoding | Original source family identified; notation, hypotheses, and theorem-node mapping require audit |
| Artin/Galois action compatibility | Same sources; the convention changes with arithmetic versus geometric reciprocity | no repo-local root expression | Convention is root-relevant and must be explicit before statement acceptance |
| CM-field object | Standard CM theory | `NumberField.IsCMField` in pinned mathlib candidate | Object-model anchor only; it does not express CM types, reflex norms, or special points |
| Idelic object model | Standard global class field theory | `NumberField.AdeleRing` and possible future idele API | Discovery anchor only; no checked transport to the root |
| Canonical Shimura variety and CM point | Shimura canonical-model theory | scheme APIs in mathlib; no exact candidate located at intake | Major formalization boundary remains open |

The repository's earlier summary "CM-field class field theory" is too broad to
serve as an exact source statement. This intake selects the special-point
Galois-action form already suggested by the legacy audit, while withholding
statement credit until a reviewer pins an exact source theorem and reconciles
its conventions with a Lean expression.

Required source audit: record immutable scans or edition identifiers, exact
pages/theorem numbers, every assumption, translations between notation,
corrections/errata search, and independent review. Accordingly this is `H2`,
not `H0` or `H1`.

