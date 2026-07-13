# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:3511-3516` supplies exactly the title `二次互反律`,
attribution to Carl Friedrich Gauss, year 1796, gloss `勒让德符号的互反性质` ("reciprocity
property of the Legendre symbol"), high importance, and status `已验证`. Git history attributes
all six uncited lines to commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record has no
bibliography, formula, definition, binders, hypotheses, conclusion, proof boundary, corrections,
reviewer, or formal artifact.

`Docs/Stage0_Blueprint.md:13109-13134` repeats the gloss and explicitly leaves the formal system,
foundation, precise definitions and premises, proof route, dependencies, equivalent statements,
axioms, machine status, and artifact links open. The rev-5.6 manifest preserves `已验证` only as
untrusted metadata and resets this target to `L0 / rework_required`.

## Inspected historical source leads

The following public GDZ records were inspected on 2026-07-13:

- Carl Friedrich Gauss, *Disquisitiones Arithmeticae*, Article 131, in *Werke*, volume 1,
  Gottingen 1863, printed page 99, persistent record
  `https://gdz.sub.uni-goettingen.de/id/PPN235993352`, canvas `00000103`. The observed OCR XML
  SHA-256 was `77d05ec702c806064b3d4a3b5494a4bc4b7989445c26278bdb132ab7b1c80809`.
- Carl Friedrich Gauss, *Untersuchungen uber hohere Arithmetik*, translated by H. Maser, Berlin
  1889, Article 131, printed page 90, persistent record
  `https://gdz.sub.uni-goettingen.de/id/PPN373456743`, canvas `00000106`. The observed OCR XML
  SHA-256 was `7d5e59b7d9db4bdb263b871a1ddf8df37c752c089004bde2ccf3d7ca9034d6e8`.

Article 131 states the fundamental theorem using signed primes and the preservation or reversal of
quadratic residue/nonresidue status. It is a strong historical anchor for the intended family.
However, the catalog cites no edition; the OCR is imperfect; the original wording is not a literal
modern Legendre-symbol equation; and no accepted transcription, translation, definition-chain
transport, errata audit, lawful immutable archive, or independent review is recorded. This
supports provisional `H1`, not `H0`.

## Clause crosswalk

| Catalog/source component | Historical source lead | Pinned Lean candidate | Intake assessment |
|---|---|---|---|
| two prime arguments | Article 131 compares prime quadratic-residue relations | `p q : Nat` with `[Fact p.Prime] [Fact q.Prime]` | catalog omits domains and binders |
| oddness | primes are separated into forms `4n+1` and `4n+3` | hypotheses `p != 2`, `q != 2` | indispensable premise absent from catalog |
| residue semantics | source uses residue/nonresidue status | `legendreSym p a` is 0, 1, or -1 according to divisibility and square status | definition transport requires review |
| reciprocity sign | source uses `+p` for `p = 4n+1` and `-p` for `p = 4n+3` | sign `(-1) ^ (p / 2 * (q / 2))` and two mod-4 variants | same family; exact equivalence not yet credited |
| distinctness | Article 131 concerns comparison with another prime; exact equality boundary needs transcription | product theorem requires `p != q`; primed equality handles `p = q` by zero symbols | canonical root choice open |
| supplements | not selected by the catalog gloss | `at_two`, `at_neg_two`, and the -1 law are separate declarations | excluded unless an approved source selects them |
| Jacobi extension | not the Article 131 root | separate `jacobiSym.quadratic_reciprocity` family | non-substitute |

Mathlib's argument order is important: `legendreSym p a` denotes the conventional symbol
`(a / p)`. Consequently, `legendreSym q p` denotes `(p / q)`, despite placing `q` first in
the Lean application.

## Pinned Lean discovery anchors

At manifest-pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, module
`Mathlib.NumberTheory.LegendreSymbol.QuadraticReciprocity` contains:

- `legendreSym.quadratic_reciprocity`: the distinct odd-prime product law;
- `legendreSym.quadratic_reciprocity'`: the odd-prime signed equality, including equal primes;
- `legendreSym.quadratic_reciprocity_one_mod_four` and
  `legendreSym.quadratic_reciprocity_three_mod_four`: the two sign branches;
- `ZMod.exists_sq_eq_prime_iff_of_mod_four_eq_one` and
  `ZMod.exists_sq_eq_prime_iff_of_mod_four_eq_three`: square-predicate forms.

`IntakeProbe.lean` imports that pinned module and checks the definition and these candidates. It
does not declare a canonical target, wrapper, transport, or proof body. The statement-selection,
minimal-import, exact-type, terminal-body, transitive-provenance, axiom, TCB, placeholder, and
composition gates remain downstream. Therefore the probe authenticates an `M3` formal interface
lead only; it cannot establish `M0-W`.

## Source gate

Before leaving `H1`, accountable reviewers must preserve an approved immutable edition, select
and transcribe one exact proposition and all incorporated definitions, map every domain, binder,
prime/odd/distinctness premise, symbol orientation, sign, equality case, conclusion, proof
boundary, translation, and correction, and independently approve its identity with
`THM-M-0478`. Only then may the statement phase freeze the Lean expression and environment
fingerprints, checked transports, and required removed-hypothesis, changed-domain, binder-scope,
and boundary-case mutations.
