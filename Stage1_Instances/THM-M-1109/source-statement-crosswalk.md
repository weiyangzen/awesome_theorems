# Source-statement crosswalk

## Repository source record

`Docs/researches/math_theorems.md` records the title "random matrix universality," attributes it to
many mathematicians, dates it only to the twenty-first century, and gives the sentence
"universality phenomena of random matrices." `Docs/Stage0_Blueprint.md` repeats that phrase while
leaving exact definitions, hypotheses, proof route, axioms, and formal artifacts open. The
rev-5.6 manifest deliberately labels the inherited `已验证` value as untrusted.

The record therefore supplies a subject classification but neither an exact human theorem nor
Lean proof evidence. The inherited label grants no `H0`, `M0`, or completion credit.

## Candidate primary-source leads

- Laszlo Erdos, Horng-Tzer Yau, and Jun Yin, "Bulk universality for generalized Wigner
  matrices," *Probability Theory and Related Fields* 154 (2012), 341-407, DOI
  `10.1007/s00440-011-0390-3`. This is a lead for bulk local statistics. Its exact numbered
  statement, assumptions, version history, errata, and relation to neighboring `THM-M-1110` have
  not been audited here.
- Terence Tao and Van Vu, "Random matrices: Universality of local eigenvalue statistics,"
  *Acta Mathematica* 206 (2011), 127-204, DOI `10.1007/s11511-011-0061-3`. This is a comparison-
  theorem lead. Its exact statement cannot be selected without separating it from the dedicated
  four-moment target `THM-M-1111`.
- Laszlo Erdos and Horng-Tzer Yau, *A Dynamical Approach to Random Matrix Theory*, Courant Lecture
  Notes 28 (2017). This is a modern source lead for organizing variants and terminology, but it is
  not a selected root and no edition/page/theorem crosswalk has been performed.

These are discovery leads only, not `E4`/`H0` evidence. A later source audit must bind an immutable
edition or article version, exact theorem/page, assumptions, definitions, proof boundary,
corrections or errata, and independent source review.

## Crosswalk

| Repository/source phrase | Possible mathematical meanings | Required Lean surface | Intake result |
|---|---|---|---|
| random matrix | one finite random matrix or a dimension-indexed ensemble | measurable matrix-valued maps or probability laws, field, symmetry, dimension | unresolved |
| universality | independence of limiting local statistics from much of the entry distribution | explicit admissible ensemble class and comparison/reference law | unresolved |
| spectral statistic | gaps, correlation functions, edge values, or eigenvectors | ordered spectrum and a measurable rescaled observable | unresolved |
| local regime | a bulk energy window, fixed energy, averaged energy, or spectral edge | scale, energy/edge hypotheses, test functions, and uniformity | unresolved |
| limiting law | sine-kernel/GOE/GUE, Airy/Tracy-Widom, or comparison with another ensemble | exact probability measure or point process and convergence predicate | unresolved |
| `已验证` | inherited metadata label | accepted source, kernel, provenance, trust, and release receipts | rejected as evidence |

## Gate to the exact statement

Unique proposition selection is the first blocker. A reviewer must choose one exact primary-source
statement and crosswalk every hypothesis, definition, quantifier, normalization, conclusion,
convention, and degenerate case. The choice must also document its non-duplication or exact
relationship to the neighboring named targets. The resulting Lean expression must elaborate under
pinned imports and pass the required statement mutations. Until then the human status is at most
`H1`, the machine status is `M4`, and no canonical Lean target or proof is claimed.
