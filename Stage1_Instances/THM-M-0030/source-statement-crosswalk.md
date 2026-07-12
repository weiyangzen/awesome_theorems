# THM-M-0030 source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:235-240` names the Krull intersection theorem, attributes it to
Wolfgang Krull in 1938, and gives only the gloss `诺特局部环中理想的交集性质`: an
ideal-intersection property in a Noetherian local ring. All six catalog fields entered the
repository at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. There is no citation,
formula, definition, proof, correction history, or formal artifact.

`Docs/Stage0_Blueprint.md:938-963` repeats the gloss but explicitly leaves the exact premises,
definitions, proof route, dependencies, equivalent forms, axioms, machine state, and artifact links
open. The rev-5.6 manifest retains `已验证` only as `source_status_untrusted` and resets the target
to `L0 / rework_required`.

## Inspected modern source lead

Stacks Project, Commutative Algebra, Section 10.51, Lemma 10.51.4, stable tag `00IP`, is explicitly
titled "Krull's intersection theorem." At immutable Stacks revision
`3683021e95ea1610e2250658d59abc18fdf0bd7b`, `algebra.tex:12240-12254` states:

> Let R be a Noetherian local ring, I a proper ideal, and M a finite R-module. Then the
> intersection over n >= 0 of I^n M is zero.

Its proof defines that intersection as `N`, applies Artin-Rees to obtain `N` contained in `I N`,
and concludes `N = 0` by Nakayama. Stacks Remark 10.51.6, tag `00IR`, explicitly records the
specialization `M = R`: the intersection of the powers of a non-unit ideal in a Noetherian local
ring is `(0)`.

This is a pinned authoritative modern source lead, not H0. The historical 1938 source, the exact
relationship to the catalog attribution, incorporated definition chain, correction/errata status,
full source-to-proof-node mapping, and independent review remain open.

## Component mapping

| Catalog component | Intake-selected mathematical meaning | Pinned Lean candidate | Intake status |
|---|---|---|---|
| "Noetherian local ring" | arbitrary commutative Noetherian local ring `R` | `[CommRing R] [IsNoetherianRing R] [IsLocalRing R]` | conventional scope selected; source ratification open |
| "ideal" | arbitrary proper ideal `I` | `(I : Ideal R)` and `(h : I != top)` | exact candidate interface authenticated |
| "intersection property" | intersection of every natural power is zero | `(iInf fun n : Nat => I ^ n) = bot` | conventional conclusion selected; canonical expression not frozen |
| Wolfgang Krull / 1938 | catalog attribution | no formal component | historical primary-source packet open |
| `已验证` | untrusted inventory label | no formal component | no H/M credit |

## Pinned formal candidates

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, module
`Mathlib.RingTheory.Filtration` declares:

```text
Ideal.iInf_pow_eq_bot_of_isLocalRing
  [IsNoetherianRing R] [IsLocalRing R] (h : I ≠ ⊤) :
  (⨅ n : ℕ, I ^ n) = ⊥

Ideal.iInf_pow_smul_eq_bot_of_isLocalRing
  [IsNoetherianRing R] [IsLocalRing R] [Module.Finite R M] (h : I ≠ ⊤) :
  (⨅ n : ℕ, I ^ n • ⊤) = ⊥
```

The exact Lean types are authenticated by `IntakeProbe.lean`. The first declaration closely matches the
catalog's ideal-only gloss. The second matches Stacks tag `00IP` and is a stronger source-form
candidate. Intake records their module, names, and checked types only. It does not accept canonical
statement identity, inspect or credit terminal proof bodies, close transitive provenance or trust,
or derive M0.

## Exactness and source gate

Before H0 or statement acceptance, accountable reviewers must preserve the relevant source
edition, resolve the historical-versus-modern provenance, map all definitions and assumptions,
check corrections and errata, approve the ideal specialization, and map material proof transitions.
The statement phase must separately freeze the exact Lean context, expression and environment
fingerprints, boundary behavior, checked alternate forms, and required mutations. Until then the
pinned declarations are candidates and the planned root remains `[H1, M3, R3]`.
