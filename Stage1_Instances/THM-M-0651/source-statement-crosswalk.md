# Source-statement crosswalk

## Repository source record

The repository's Stage0 record names `THM-M-0651` as the omitting types theorem and gives only the
phrase "conditions for omitting types in a model." Its `已验证` label is explicitly untrusted under
rev-5.6 and supplies neither assumptions nor proof evidence. The manifest places the target at rank
697 in `hard_statement_first_partial_verification`, uniformly at `L0 / rework_required`.

## Human-source candidates

- C. C. Chang and H. J. Keisler, *Model Theory*, North-Holland. The omitting-types chapter is a
  candidate standard source for the countable simultaneous theorem.
- Wilfrid Hodges, *Model Theory*, Cambridge University Press (1993). The omitting-types treatment is
  a candidate modern source for definition and variant comparison.
- David Marker, *Model Theory: An Introduction*, Graduate Texts in Mathematics 217, Springer
  (2002). Its treatment is a candidate reader-facing proof source and terminology check.

These bibliographic anchors have not yet been inspected at a frozen edition and pinpoint theorem
or page. They are not H0 evidence. The statement/source phase must select a stable edition, record
the exact theorem and pages, check errata, and independently review every premise below. The current
`H1` means the classical proof is known but the repository's exact source genealogy and assumption
mapping remain incomplete.

## Statement crosswalk

| Source concept | Frozen intake interpretation | Required Lean representation | Open source question |
|---|---|---|---|
| countable language | countably many first-order symbols | `FirstOrder.Language` plus accepted countability data | concrete enumeration versus typeclass countability |
| consistent theory `T` | syntactically consistent, with completeness-mediated semantic form allowed only by a checked bridge | `Language.Theory` and a pinned consistency/satisfiability predicate | which form the selected theorem states |
| partial type `p` | set of formulas in one finite tuple of variables, finitely satisfiable with `T` | formula set/theory in a constants or variables expansion | arity convention and parameter policy |
| nonprincipal over `T` | no single `T`-consistent formula isolates all formulas of `p` | explicit isolation predicate and its negation | exact isolation definition used by source |
| countable family | simultaneous omission for a countable index | countable index type or enumeration | whether mixed arities occur in the source |
| model of `T` | an `L`-structure satisfying every sentence of `T` | `Theory.Model`/semantic satisfaction API | empty-carrier and inhabitedness conventions |
| omits `p` | no tuple in the model realizes every formula in `p` | universal non-realization predicate | assignment/tuple encoding and nullary case |
| countable model | carrier is at most countable, not silently countably infinite | carrier plus `Countable`/embedding evidence | whether finite models are included explicitly |

## Formal discovery boundary

The pinned mathlib snapshot contains `Mathlib/ModelTheory/Types.lean`, including complete types and
realized-types infrastructure, and `Mathlib/ModelTheory/Satisfiability.lean`. A case-insensitive
search for omitting-types terminology in the pinned `Mathlib` source produced no relevant match.
This does not prove that no compositional candidate exists and does not establish `M0` or `M1`;
the immutable declaration-level audit belongs to `S56-M-0651-ANCHOR_AUDIT` after exact statement
elaboration.

Before H0, an independent reviewer must approve the exact edition/theorem/page, definitions of
type and principality, all countability and consistency hypotheses, simultaneous-family strength,
proof boundaries, and known errata, together with the final source-to-Lean row mapping.
