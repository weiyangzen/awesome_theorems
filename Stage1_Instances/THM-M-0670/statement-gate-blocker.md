# Statement gate blocker

Item: `S56-M-0670-STATEMENT`

Base revision: `72e619798c0efb1ca66df0782a61d8eed273bc3d`.

Validation date: 2026-07-12 (Asia/Shanghai).

## Verdict

The exact Lean 4 target cannot be truthfully elaborated from the repository source material. The
statement phase is blocked and remains unclaimed. No `Statement.lean`, expression fingerprint,
alternate-form transport, or mutation result is emitted, because doing so would require choosing
mathematically material data not present in the source.

## First failed gate

Section 5 of `Docs/Stage1_Blueprint_rev-5.6.md` requires one exact canonical mathematical statement
before the Lean statement gate. The complete repository source for this item is the name
"Ackermann quantifier elimination", the attribution "Wilhelm Ackermann", the year 1928, and the
gloss "quantifier elimination for Presburger arithmetic". It supplies no publication, theorem or
page, formal language, structure or theory, parameter convention, or algorithmic specification.

Those omissions are not cosmetic:

- Pinned mathlib's `FirstOrder.Language.presburger` is the relation-free language `(0, 1, +)`.
  Mathlib explicitly leaves its theory and quantifier elimination as a TODO.
- Ordinary syntactic quantifier elimination is not the same claim in the bare language and in an
  expansion by order and congruence/divisibility predicates. Selecting the expanded signature
  would broaden the stated repository target without source authority.
- Equivalence only in the standard `Nat` structure, equivalence in every model of a specified
  Presburger theory, and correctness of a named elimination algorithm are distinct Lean targets.
- The repository's date and attribution do not identify an inspected Ackermann proposition. The
  nearby modern phrase "Presburger arithmetic" therefore cannot safely be treated as an exact
  quotation or silently reassigned to a different historical source.

Consequently a convenient proposition such as
`forall phi, exists psi, psi.IsQF and forall v, phi.Realize v iff psi.Realize v` would still leave
the language, structure/theory boundary, and source-specific content invented. Elaborating that
shape would be a substituted theorem prohibited by the worker contract.

## Lean boundary actually checked

The existing discovery-only `IntakeProbe.lean` was re-elaborated with the pinned toolchain. It
confirms that the syntax, semantics, quantifier-free predicate, and semilinear-set theorem APIs are
available. It is not the canonical target and grants no statement-gate or proof credit.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0670` | exit 0; rank 714, planned, theorem incomplete |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0670/IntakeProbe.lean)` | exit 0; the seven discovery declarations elaborate |

No dependency command that mutates `.lake` was run.

## Retry condition

Provide and inspect an immutable primary edition that identifies the attributed result by exact
theorem/page. Crosswalk its syntax and semantics to a precise language and standard-model or
theory-relative boundary. Only then can the statement phase add the canonical Lean expression,
fixed environment fingerprint, checked alternate encodings, and the required removed-hypothesis,
changed-domain, changed-binder-scope, and boundary-case mutations.

Current boundary: `[H2, M4, R4]`; lifecycle `planned`; audit complete `false`; theorem complete
`false`; accepted receipts: none.
