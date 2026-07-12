# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:10027-10032` supplies exactly the title `Poincare recurrence
theorem`, attribution to Henri Poincare, the year 1890, the gloss `有界系统的回归性`
(`bounded-system recurrence`), importance "high," and status `已验证`. Git history places all six
uncited fields in commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record contains no
definitions, binders, hypotheses, conclusion, proof boundary, source, correction history, or formal
artifact.

`Docs/Stage0_Blueprint.md:37425-37450` repeats the gloss while explicitly leaving the target formal
system, foundation, exact definitions and premises, proof route, dependencies, alternate forms,
axioms, machine status, and artifact links open. The rev-5.6 manifest retains `已验证` only as
untrusted source metadata and resets the target to `L0 / rework_required`.

## Duplicate repository records

`Docs/researches/math_theorems.md:11108-11113` contains the translated title `庞加莱回归定理` with
the same attribution, year, gloss, importance, and status. Rev-5.6 projects it as the separate
target `THM-M-1521` in mathematical physics. A physics-catalog record at
`Docs/researches/physics_theorems.md:6847-6853` gives the stronger wording that in a bounded
conservative system almost all orbits return infinitely often.

The repository has made no accepted alias, deduplication, canonical-root ownership, or intentional
specialization decision for `THM-M-1376` versus `THM-M-1521`. The latter's dossier selects a
discrete finite-measure-preserving proposition, and its Lean artifacts implement a candidate
mathlib route. That work is discovery evidence about a likely interpretation, not source authority,
scope, proof credit, or accepted state for this target.

## Human-source lead

A plausible historical lead is Henri Poincare, *Sur le probleme des trois corps et les equations de
la dynamique*, *Acta Mathematica* 13 (1890), pages 1-270. The existing duplicate dossier points to
the recurrence discussion near pages 65-72. This intake did not preserve and inspect a lawful
complete edition, verify the page locator or translation, map its historical hypotheses to a modern
measure-theoretic theorem, audit corrections, or obtain independent review. It therefore records
the lead at `H1`, not `H0`, and does not select its wording as the root.

## Component crosswalk

| Catalog component | Source-family alternatives | Prospective Lean surface | Intake assessment |
|---|---|---|---|
| `bounded system` | finite measure space; finite invariant subset; compact phase region; bounded Hamiltonian energy shell | `IsFiniteMeasure`, restricted measure, future invariant-region or energy-shell bridge | `bounded` is not a formal substitute for any one alternative |
| recurrence | almost-everywhere infinite return to a measurable set | `Conservative.ae_mem_imp_frequently_image_mem` | exact pinned candidate for a common discrete form, not a selected root |
| recurrent point | return infinitely often to every neighborhood | `Conservative.ae_frequently_mem_of_mem_nhds` | stronger topological form with extra topology assumptions |
| conservative dynamics | a finite-measure-preserving self-map is conservative | `MeasurePreserving.conservative` | checked adjacent bridge; not an ODE or Hamiltonian construction |
| ODE/flow reading | select a time map of a complete measure-preserving flow on an invariant finite-measure carrier | future flow, invariance, restriction, and preservation transports | every physical/differential bridge remains open |
| `已验证` | untrusted inventory label | no canonical proposition or receipt | no H or M credit |

## Pinned Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, module
`Mathlib.Dynamics.Ergodic.Conservative` explicitly labels
`Conservative.ae_mem_imp_frequently_image_mem` as the Poincare recurrence theorem. It also provides
`MeasurePreserving.conservative` for a measure-preserving self-map on a finite measure space and the
topological theorem `Conservative.ae_frequently_mem_of_mem_nhds`. The discovery-only probe checks
these types without adding a theorem or proof body.

`Stage1_Instances/THM-M-1521/Statement.lean` defines the foreign candidate
`Stage1Instances.THM_M_1521.PoincareRecurrenceTarget`; its dossier explicitly excludes silently
inferring Hamiltonian phase space, Liouville preservation, a finite energy shell, or continuous-flow
recurrence. This is useful negative boundary evidence. The file belongs to another owned path and
is neither imported nor modified here.

Before leaving `H1`, accountable reviewers must select and preserve an immutable primary or
authoritative source proposition, verify the exact edition/theorem/page and errata, transcribe every
incorporated definition, ordered binder, premise, conclusion, and proof boundary, decide the
`THM-M-1521` identity and ownership relation, and independently approve the mapping. Only then may
the statement phase freeze minimal imports, an elaborated expression, checked transports, and the
required removed-hypothesis, changed-domain, binder-scope, and boundary mutations.
