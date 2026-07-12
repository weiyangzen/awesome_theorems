# Source-statement crosswalk

## Repository sources inspected

`Docs/researches/math_theorems.md:10236` records the title `符号动力学`; lines 10237-10241 give
only "many mathematicians," "twentieth century," the gloss `动力系统的符号表示` (symbolic
representation of dynamical systems), importance "high," and status `已验证`.
`Docs/Stage0_Blueprint.md:38105` repeats these fields while explicitly leaving exact definitions,
premises, proof route, equivalent forms, axioms, and existing machine artifacts open. The rev-5.6
manifest carries `已验证` only as `source_status_untrusted`.

A separate physics-catalog record at `Docs/researches/physics_theorems.md:6691` is titled
`符号动力学理论`, attributes it to Morse and Hedlund in 1938/1940, and glosses it as describing
complex dynamics by symbolic sequences. It is useful discovery context, but the repository does
not identify it as the source statement for `THM-M-1401`, cite a publication, or name a theorem.
It therefore cannot silently replace the mathematical target.

## Crosswalk

| Repository phrase | Possible mathematical component | Required Lean surface | Intake assessment |
|---|---|---|---|
| `符号动力学` | a broad theory of sequence systems and codings | no single declaration follows from a field name | topic identity only |
| "dynamical systems" | a self-map, group/monoid action, flow, or invariant subsystem | exact state type, structure, time action, map, and invariant set | all open |
| "symbols" | a finite, countable, compact, or arbitrary alphabet | alphabet type plus discrete/topological/measurable structure | all open |
| "representation" | itinerary, factor map, embedding, semiconjugacy, conjugacy, or realization | coding map, shift, intertwining law, regularity, injectivity/surjectivity clauses | conclusion strength open |
| twentieth century / many mathematicians | broad historical locator | documentation only | no edition, stable ID, theorem, page, assumptions, or errata |
| Morse/Hedlund physics record | possible historical theory family | source provenance only until identity is reviewed | related discovery record, not accepted crosswalk |
| `已验证` | untrusted inventory label | no proposition and no kernel evidence | explicitly rejected as proof credit |

## Source gate

No primary mathematical source is identified, so neither a proposition nor its human proof status
can be audited. The provisional human classification is `H4` in the dossier's fail-closed sense:
the exact proposition is open, not a claim that the whole subject of symbolic dynamics is an open
problem. Before `H0` or statement credit, an accountable reviewer must:

1. identify a stable primary or authoritative source edition and content hash;
2. pinpoint the exact theorem, section, and page rather than the surrounding theory;
3. transcribe every ordered domain, binder, hypothesis, conclusion, and exceptional case;
4. map dependent definitions and sources, check corrections and errata, and reconcile the
   mathematical and physics catalog records; and
5. explain why the selected proposition is this target rather than one of the separately cataloged
   shift, entropy, Bernoulli, hyperbolic, or Markov-partition entries.

## Lean discovery boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, a bounded name search
for `subshift`, `shift space`, `symbolic dynamics`, and `Bernoulli shift` returned no matches. This
is not a complete anchor audit and makes no claim about external projects. Generic APIs such as
`Stream'.tail`, `Function.Semiconj`, and periodic-point transport are ingredients only; without a
source-frozen proposition, using them to invent a target would be substitution rather than Lean
validation.
