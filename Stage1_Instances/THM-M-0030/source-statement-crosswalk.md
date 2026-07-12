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
| "ideal" | arbitrary proper ideal `I` | `(I : Ideal R)` and `(h : I ≠ ⊤)` | exact candidate interface authenticated |
| "intersection property" | intersection of every natural power is zero | `(iInf fun n : Nat => I ^ n) = bot` | exact canonical expression self-tested pending master acceptance |
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

The anchor audit authenticates the first declaration against a literal copy of the frozen Lean
target. The only syntactic interface difference is harmless binder ordering: mathlib places `I`
before the Noetherian and local instance arguments, and the checked adapter introduces the frozen
binders before invoking it. Its transparent body specializes the second declaration at `M = R` and
converts `I ^ n • top` back to the ideal `I ^ n`. The second declaration matches Stacks tag `00IP`
and reduces through the Jacobson-radical bridge. These are one proof path, not independent bodies.

At the pinned revision Lean reports the terminal theorem and both supporting bridges sorry-free and
reports only `propext`, `Classical.choice`, and `Quot.sound`. Bounded external search finds the name
only as downstream uses in Atlas and FLT, not as an independent Lean 4 proof. This supports a
provisional exact `M0-W / E2` candidate, not accepted M0/E1 or theorem completion. Complete
transitive provenance/TCB closure, proof-phase integration, hermetic and independent validation,
and master acceptance remain downstream.

## Exactness and source gate

Before H0, accountable reviewers must preserve the relevant source edition, resolve the historical-
versus-modern provenance, map all definitions and assumptions, check corrections and errata, and
map material proof transitions. For statement identity, pinned Stacks tag `00IR` explicitly ratifies
the ideal specialization of tag `00IP`. The exact Lean context, expression and environment
fingerprints, membership iff, boundary behavior, and required mutations are now self-tested in the
statement packet. The exact pinned declaration is now a self-tested anchor candidate. The accepted
planned root remains `[H1, M3, R3]` with no accepted proof or H0 credit.
