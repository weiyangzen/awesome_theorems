# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:6924-6929` supplies exactly the title `Szemeredi theorem`, Endre
Szemeredi, 1975, the slogan `positive-density sets contain arbitrarily long arithmetic
progressions`, importance "high," and status `verified` (these English field values are translations
of the Chinese catalog fields). All six uncited lines entered the repository in commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`.

`Docs/Stage0_Blueprint.md:25849-25874` repeats the slogan while explicitly leaving the target formal
system, foundation, exact definitions and premises, proof route, dependencies, alternate forms,
axioms, machine status, and artifact links open. The rev-5.6 manifest retains the source status only
as `source_status_untrusted` and resets the target to `L0 / rework_required`.

## Primary-source lead

The publisher scan identifies E. Szemeredi, "On sets of integers containing no k elements in
arithmetic progression," *Acta Arithmetica* 27 (1975), 199-245, DOI
`10.4064/aa-27-1-199-245`. The current DOI landing page and Crossref metadata omit the word "no";
the scan itself visibly includes it. The publisher supplies a 24-page scanned PDF whose SHA-256 was
observed as `78620216317099fc4d50f2d8c37359d6d781af7ce8596cd83b7f3bfec842d2d0`.

This is a strong primary-source lead, not an `H0` packet. The scan is image-only, and intake did not
accept a reviewed transcription of the exact theorem, all incorporated definitions and premises,
the proof boundary, corrections or errata, or an independent statement mapping. The remote source
was inspected outside the repository and was not admitted as an immutable public artifact.

## Component crosswalk

| Catalog component | Candidate mathematical component | Prospective Lean surface | Intake status |
|---|---|---|---|
| positive density | positive upper/lower/natural/Banach density of a set of integers | one exact density definition with interval and limit conventions | unspecified; Schnirelmann density is not substituted |
| set | subset of naturals, positive integers, or integers | `Set Nat`, a positive-integer subtype, or `Set Int` | ambient domain open |
| arbitrarily long | every prescribed finite length, normally above a source-defined lower bound | ordered binder over `k : Nat` and boundary clauses | quantifier order and small lengths open |
| arithmetic progression | terms `a + i * d` indexed by a finite interval | witnesses `a`, `d`, membership for every index, and `0 < d` or `d != 0` | representation and nondegeneracy open |
| 1975 / Szemeredi | historical result and proof source | immutable provenance and source-to-node mapping | matching paper found; full mapping and review open |
| `verified` | untrusted inventory metadata | no declaration or proof body | no H, M, or R credit |

## Variant boundary

The infinite and finite forms are not credited as interchangeable until their implication or
equivalence is checked with all density and interval conventions. Roth's length-three theorem,
finite-color Van der Waerden, density Hales-Jewett, Green-Tao, the regularity lemma, and the
Ruzsa-Szemeredi problem are neighboring results, not aliases of this target.

## Pinned Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, a bounded source-name
search found no full arbitrary-length positive-density Szemeredi declaration. The inspected nearby
modules provide:

- `schnirelmannDensity`, while its module explicitly lists lower/upper asymptotic and natural
  densities as future work;
- `roth_3ap_theorem_nat`, which proves only the length-three finite-density result; and
- `exists_mono_homothetic_copy`, a finite-color consequence of Hales-Jewett/Van der Waerden.

The regularity-lemma and Ruzsa-Szemeredi modules are also distinct targets. These are bounded intake
discovery facts only, not a complete formal anchor audit or proof of external absence.

## Required admission

The statement phase must preserve a lawfully accessible immutable edition, select and transcribe
the exact theorem and incorporated definitions, freeze every ordered binder, hypothesis,
conclusion, normalization, and boundary case, inspect corrections and errata, and obtain independent
source review. It must then encode that same claim in Lean, minimize imports, serialize the
elaborated expression and environment, check every credited transport, and run the required
statement mutations. Until then the root remains `H1` and the canonical Lean target is null.
