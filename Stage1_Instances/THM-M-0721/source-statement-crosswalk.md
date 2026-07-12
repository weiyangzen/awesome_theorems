# Source-statement crosswalk

## Repository source

The Stage0 record states `NP\u5b8c\u5168\u95ee\u9898\u7684\u5b58\u5728\u6027` (existence of NP-complete problems), dates
the result to 1971, and names Stephen Cook and Richard Karp. It supplies no definition of `NP`, no
reduction notion, and no theorem/page anchor. Its `\u5df2\u9a8c\u8bc1` label is untrusted metadata and gives no
human-source or machine-proof credit under rev-5.6.

## Candidate primary sources

- Stephen A. Cook, "The Complexity of Theorem-Proving Procedures," *Proceedings of the Third
  Annual ACM Symposium on Theory of Computing* (1971), pages 151-158. This is the primary
  historical candidate for the universal reduction and concrete complete-language witness. Its
  original reducibility vocabulary and chosen formula language must be inspected rather than
  silently translated into the modern many-one statement.
- Richard M. Karp, "Reducibility Among Combinatorial Problems," in *Complexity of Computer
  Computations*, Plenum Press (1972), pages 85-103. This is a primary candidate for the modern
  polynomial reducibility/completeness framework and concrete complete problems. Exact definition
  and theorem numbering, assumptions, and corrections remain to be audited.

These bibliographic entries are discovery anchors only, not `H0` evidence. The statement phase must
inspect stable copies and record exact definitions, theorem/page locations, assumptions, and known
errata. An independent reviewer must approve the final mapping.

## Crosswalk

| Repository phrase | Frozen mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "NP-complete" | membership in `NP` plus universal `NP` hardness | definitions of languages, `NP`, many-one reduction, and completeness | included; encodings/API open |
| "existence" | an existentially quantified complete language | witness language and proofs of both conjuncts | included |
| 1971 / Cook | universal polynomial reduction to a Boolean formula language | encoded computation-to-formula construction | candidate proof bridge only |
| Cook/Karp | classical completeness framework and reductions | checked source-definition-to-Lean transport | exact historical mapping open |
| intended SAT witness | a satisfiability language over encoded Boolean formulas | syntax, semantics, well-formedness, certificates, encoding | intended; exact variant open |

## Target distinction and source boundary

`THM-M-0690` separately catalogues the Cook-Levin theorem. `THM-M-0721` freezes only the existential
consequence. A later proof may close the existential by applying an exact, audited Cook-Levin
declaration to SAT, but the invocation remains a root-relevant bridge obligation and cannot be
counted as a trivial leaf. Conversely, proving that one specially chosen finite language is easy
does not establish this source claim.

The pinned mathlib tree was searched at intake for common `NPComplete`, Cook-Levin, and complexity
class spellings. No candidate declaration was found; this is only a bounded local discovery result,
not a claim that no Lean formalization exists. External Lean candidates and non-Lean formalizations
belong to the later anchor-audit phase.
