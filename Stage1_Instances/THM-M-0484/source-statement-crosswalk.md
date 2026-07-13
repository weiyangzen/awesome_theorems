# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:3553-3558` supplies exactly the title `卢卡斯-莱默检验`, the
attribution `Edouard Lucas/Derrick Lehmer`, the year 1930, the gloss `梅森素数的快速检验`, high
importance, and `已验证`. Git history attributes all six uncited lines to commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record contains no formula, definition,
quantifier, hypothesis, conclusion, bibliography, theorem/page locator, proof boundary, correction
history, reviewer, or formal artifact.

`Docs/Stage0_Blueprint.md:13271-13296` repeats the gloss while explicitly leaving the formal
system, foundation, precise definitions and premises, proof history, dependencies, equivalent
forms, axioms, machine status, and artifact link open. The rev-5.6 target manifest preserves
`已验证` only as untrusted metadata and resets this theorem to `L0 / rework_required`.

## Human-source leads

The PrimePages article *A proof of the Lucas-Lehmer Test*, by Chris Caldwell, states the criterion
as follows: for an odd prime `p`, `M_p = 2^p - 1` is prime iff `S_(p-1) = 0 (mod M_p)`, where
`S_1 = 4` and `S_n = S_(n-1)^2 - 2`. Its bibliography identifies D. H. Lehmer, *An extended
theory of Lucas' functions*, Annals of Mathematics 31 (1930), pages 419-448. Crossref confirms the
title, author, journal, volume, issue, year, starting page, and DOI `10.2307/1968235`.

These are source leads, not `H0`. The modern page says its displayed proof omits necessity; the
paywalled 1930 article itself was not inspected; the catalog cites neither; and no complete
primary-source statement/proof/errata audit or independent review exists. The modern page's
one-based `S_(p-1)` must also be checked against mathlib's zero-based residue at `p - 2`.

## Clause crosswalk

| Catalog/source component | Candidate mathematical meaning | Pinned Lean surface | Intake disposition |
|---|---|---|---|
| Mersenne number | `M_p = 2^p - 1` | `mersenne p : Nat` | direct definition match |
| exponent domain | odd prime `p` in the modern source | `p : Nat` with shared bound `3 <= p`; `Nat.Prime p` follows on the primality side | source-domain transport open |
| recurrence | seed 4, then square and subtract 2 | `LucasLehmer.s`, `sZMod`, and `sMod` | exact-topic encodings; indexing transport open |
| terminal term | one-based `S_(p-1)` | zero-based `lucasLehmerResidue p = sZMod p (p - 2)` | expected index shift, not yet credited |
| zero condition | divisibility/congruence by `M_p` | equality to zero in `ZMod (2^p - 1)` | checked representation transport remains downstream |
| correctness | primality iff terminal residue is zero | sufficiency plus necessity declarations | direct formal candidate under `3 <= p`; no proof credit at intake |
| "fast" | efficient modular recurrence implementation | kernel-backed `norm_num` extension exists | performance is non-propositional without a cost model |

## Pinned Lean candidate

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`, module
`Mathlib.NumberTheory.LucasLehmer` contains:

```text
lucas_lehmer_sufficiency (p : Nat) (w : 1 < p) :
  LucasLehmerTest p -> Nat.Prime (mersenne p)

lucas_lehmer_necessity (p : Nat) (w : 3 <= p)
    (hp : Nat.Prime (mersenne p)) :
  LucasLehmerTest p
```

The necessity direction entered mathlib at immutable commit
`9067089938d4c3675c1193f1b6e8378620ea611a` (2025-08-13, PR #26272); the older Lean 4 port had
only sufficiency. The pinned declarations, rather than the file header's informal unbounded iff,
control the candidate boundary.

`Archive/Examples/MersennePrimes.lean` at the same pin explicitly demonstrates both
`Not (LucasLehmerTest 2)` and `Nat.Prime (mersenne 2)`. Therefore an unconditional iff and an iff
assuming only `p.Prime` are false. `Statement.lean` now freezes the intake-selected sharper iff
under `3 <= p`, its expression and environment fingerprints, two representation transports, four
structural mutations, and the exception. This formal freeze does not turn the unresolved
conventional-source mapping into `H0`.

## Open source gate

Before `H0`, reviewers must inspect and lawfully preserve an approved primary or authoritative
edition, locate the exact theorem and proof, map every definition, domain restriction, index,
direction, congruence encoding, and computation boundary, audit corrections and attribution, and
approve the crosswalk independently. Before formal proof credit, the later phases must separately
audit the pinned terminal bodies, dependency/provenance and trust closure, placeholders, checked
wrapper/composition, and reproducible validation.
