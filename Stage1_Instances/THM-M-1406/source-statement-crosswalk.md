# Source-statement crosswalk

## Repository source record

The source catalog at `Docs/researches/math_theorems.md:10271` records only the name
`Kolmogorov-Sinai熵`, the attribution Kolmogorov/Sinai, the year 1958, and the phrase
`动力系统的熵`. The generated Stage0 entry at `Docs/Stage0_Blueprint.md:38240` repeats those fields
while explicitly leaving the exact definitions, premises, proof path, axioms, and machine artifact
open. The rev-5.6 manifest records rank 905, baseline `L0 / rework_required`, no legacy slot, and
treats `已验证` as `source_status_untrusted`.

The entry therefore identifies an invariant family, not a proposition. It gives no edition,
theorem or definition number, page, exact assumptions, conclusion, errata, translation, or proof
artifact. It also does not explain how this entry differs from the adjacent `THM-M-1404`
measure-theoretic entropy target.

## Source discoveries

- A. N. Kolmogorov, "A new metric invariant of transitive dynamical systems and automorphisms of
  Lebesgue spaces," *Doklady Akademii Nauk SSSR* 119(5) (1958), 861-864, in Russian. Stable
  Math-Net record: `https://www.mathnet.ru/eng/dan22922`; MR0103254; zbMATH 0083.10602.
- A. N. Kolmogorov, "On entropy per unit time as a metric invariant of automorphisms," *Doklady
  Akademii Nauk SSSR* 124(4) (1959), 754-755, in Russian.
- Ya. G. Sinai, "On the notion of entropy of a dynamical system," *Doklady Akademii Nauk SSSR*
  124(4) (1959), 768-771, in Russian.
- Yakov Sinai, "Kolmogorov-Sinai entropy," *Scholarpedia* 4(3):2034 (2009), DOI
  `10.4249/scholarpedia.2034`, fixed revision `91407`.

The 1958 Math-Net scan was retrieved and inspected during intake. It is a four-page Russian primary
artifact with SHA-256
`abf376fa2e2aefaf1492308a8808d79be3431dae4c821ca546719f35a1d4bf85`. The visible structure has
sections 1-4 and numbered Theorems 1-4; section 2 visibly introduces a characteristic `h`, and
section 3 uses `h(T)`. OCR suggests that Theorem 2 concerns independence of `h` from the selected
subalgebra, but that provisional observation is not credited as a translation or as the catalog
root. A qualified translation review, exact premise mapping, errata search, root selection, and
independent approval remain open.

Sinai's fixed Scholarpedia revision was also retrieved twice through the revision-content API; the
two JSON responses were byte-identical, 10,659 bytes, and had SHA-256
`f29e718b4bc265ca6e04b78eb1c1bf13e253549b3f9d0abb0dba926a2710a706`. The response embeds
revision ID `91407`, timestamp `2011-10-21T04:11:14Z`, and the exact article wikitext. This is an
author-written secondary source, not `H0` evidence. It defines the modern discrete-time invariant as
`h(T) = sup_xi h(T, xi)` over finite partitions and distinguishes the generator equality as its
Theorem 1. Its history section says Kolmogorov's 1958 paper defined entropy only for quasi-regular
systems, while Sinai later supplied the general definition. This confirms that a source-controlled
historical-to-modern crosswalk is material and that the generator theorem must remain separate.

## Claim crosswalk

| Repository/source component | Mathematical information fixed | Prospective Lean surface | Intake result |
|---|---|---|---|
| Name `Kolmogorov-Sinai熵` | the modern measure-theoretic entropy family is likely intended | a future entropy definition plus one selected truth-valued theorem | invariant family only; no proposition |
| `动力系统` | some measure-preserving dynamical system is likely intended | `Measure`, `MeasurableSpace`, a typed self-map, and `MeasurePreserving` | measure class, invertibility, time domain, and mod-null conventions absent |
| `熵` | information growth under dynamics | measurable partitions, joins of inverse images, `-p log p`, an asymptotic rate, and a supremum | construction family only; codomain and normalization absent |
| Kolmogorov / 1958 | historical origin in a more restricted invariant | source record plus a checked transport to any modern formulation | exact theorem and equivalence direction unselected |
| Sinai | later general finite-partition formulation and generator result | separate definition/transport and theorem obligations | does not choose whether this root is a definition, transport, or property |
| `已验证` | untrusted catalog metadata | an exact declaration, proof body, and receipt would be required | no source or machine credit |
| Adjacent entropy entries | the catalog schedules related records separately | independent IDs with reviewed identity or exclusion crosswalks | `THM-M-1404` and `THM-M-1405` cannot be folded into this root |

## Lean discovery boundary

The pinned intake probe checks that Lean 4.29.0 with mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` exposes measure-preserving maps and iterates,
probability-measure and ergodicity predicates, finite partitions of measurable sets, measurable
space generation, and the scalar information function `Real.negMulLog`. These are ingredients
only. The probe defines no entropy object and asserts no target theorem.

A bounded source-name search under pinned `Mathlib/Dynamics`, `Mathlib/MeasureTheory`, and
`Mathlib/Probability` found no declaration matching measure-theoretic entropy,
Kolmogorov-Sinai entropy, Kolmogorov entropy, metric entropy, or partition entropy. Mathlib's
topological entropy and scalar binary-entropy APIs concern different objects. This is an intake
search, not a saturated formal-anchor audit and not proof of global absence.

## Intake classification

The catalog wording is provisionally `H5`: an invariant/topic label is not a stable truth-valued
proposition. This is a target-correction status, not a claim that a selected KS-entropy theorem is
false or mathematically open. Before ordinary proof execution, an independent reviewer must select
and transcribe one primary proposition and every incorporated definition, resolve historical and
translation fidelity, map every assumption and conclusion, reconcile `THM-M-1404` and
`THM-M-1405`, and approve the crosswalk. Its human-proof status must then be reassessed rather than
inherited from this intake classification.
