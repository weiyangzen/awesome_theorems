# THM-M-0590 rev-5.6 intake

This is the `planned` rev-5.6 instance for the Brown-Douglas-Fillmore classification theorem. The
metadata name denotes a broad theory, so this dossier freezes its central essentially-normal-
operator classification as the exact human claim. The source label `\u5df2\u9a8c\u8bc1` is untrusted intake
metadata and provides no inherited human or machine proof credit.

## Scope map

| Surface | In scope | Intake boundary |
|---|---|---|
| Exact root | Classification of bounded essentially normal operators up to unitary equivalence modulo compact operators | The source theorem/page pinpoint and exact Lean expression remain open |
| Operator domains | Separable infinite-dimensional complex Hilbert spaces, potentially different but unitarily isomorphic | The Lean universe and typeclass packaging are deferred to statement work |
| Essential normality | Compact self-commutator | The commutator orientation is immaterial to compactness but must be fixed syntactically |
| Equivalence relation | A unitary conjugacy whose error is compact | Equality in a Calkin algebra is a candidate alternate encoding, not yet a checked transport |
| Complete invariants | Essential spectrum and the Fredholm-index function on its complement | Index sign (`T - \u03bbI` versus `\u03bbI - T`) must be frozen and mutation-tested |
| Extension-theory layer | Busby invariants and extension classes of `C(X)` by compact operators | This is architecture for later phases, not silently substituted for the root |
| K-homology layer | The BDF `Ext`/odd K-homology relationship | A distinct structural formulation requiring a sourced, checked bridge |
| Foundations | Lean kernel plus pinned mathlib with explicit quotient, classical, choice, and Fredholm policies | Profiles and dependency fingerprint remain open |

The structured binder, hypothesis, boundary-case, and alternate-encoding inventory is in
`intake.json`. The human-source discovery map is in `source_statement_crosswalk.md`.

## Open task DAG

`INTAKE -> STATEMENT -> ANCHOR_AUDIT -> OBLIGATION_TREE -> PROOF -> VALIDATION -> RELEASE`.

The statement phase must first determine whether pinned mathlib has sufficient compact-operator,
Calkin-algebra, essential-spectrum, and Fredholm-index APIs to elaborate the literal root without
replacing it by an interface-level model. It must also mutation-test essential normality, the
infinite-dimensional domain, binder scope for `\u03bb`, and the off-spectrum restriction.

## Exact Lean target

`Statement.lean` elaborates `THMM0590.brownDouglasFillmoreTarget : Prop` using the single pinned
import `Mathlib.Analysis.InnerProductSpace.Adjoint`. Because this mathlib revision has no general
Fredholm-index API, the module expands Fredholmness, its integer index, and the essential spectrum
from kernel, cokernel, closed range, and `T - lambda I`; it does not substitute an uninterpreted
interface. `statement.json` freezes binders and conventions, and `statement_validation.md` records
the Lean replay and environment fingerprint.

This elaboration supplies no inhabitant of the proposition. The source, anchor, proof, validation,
and release phases remain open, the root stays `M3`, and theorem completion remains false.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H1, M3, R3]`. The first failed theorem gate is
the exact Lean statement gate. No theorem completion, formal anchor, or source fidelity is claimed.

## Validation

The commands and exact results establishing manifest consistency, JSON syntax, dossier-local
integrity, and clean patch formatting are recorded in `validation.md`. These checks validate this
intake artifact only; they are not Lean elaboration or theorem evidence.
