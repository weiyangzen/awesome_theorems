# THM-M-0931 rev-5.6 intake and statement

This directory is the fail-closed `planned` intake dossier for the Erdős-Ginzburg-Ziv theorem.
The repository catalog gives the faithful shorthand `2n-1个整数中存在n个和为n的倍数`
(`among 2n - 1 integers, n have sum divisible by n`), the three authors, the year 1961, and an
untrusted `已验证` label.

## Intake result

The authors' archive scan of P. Erdős, A. Ginzburg, and A. Ziv, *Theorem in the additive number
theory*, states on scan page 1:

```text
Each set of 2n-1 integers contains some subset of n elements the sum of which is a multiple of n.
```

The complete two-scan-page paper proves the prime case and then proves closure under multiplication
of valid moduli. Its indexed proof makes occurrence selection, rather than duplicate-free set
selection, the source-faithful reading. The paper silently treats `n` as positive; mathlib's natural
number API also covers `n = 0` by truncated subtraction and an empty witness. These conventions,
the exact-count versus at-least-count relationship, corrections or errata, and independent review
were left for the dependent statement phase. Intake therefore recorded the exact source lead before
installing a canonical expression.

## Lean boundary

Pinned mathlib contains indexed and multiset versions over integers and `ZMod n` in
`Mathlib.Combinatorics.Additive.ErdosGinzburgZiv`. The closest occurrence-preserving candidate is
`Int.erdos_ginzburg_ziv_multiset`; it accepts at least `2 * n - 1` elements and reports axioms
`propext`, `Classical.choice`, and `Quot.sound`. `IntakeProbe.lean` authenticates the four public
candidates and their reported axiom surface. It is discovery evidence, not a canonical wrapper,
source transport, downstream anchor audit, or proof receipt.

The statement phase now proposes the positive, exact-count, occurrence-preserving integer root
`Stage1Instances.THM_M_0931.ErdosGinzburgZivTarget`. Its `Multiset Int` input retains repetitions,
and its selected submultiset has exactly `n` occurrences and sum divisible by `n`. A single
non-proof import suffices. Checked transports specialize the at-least-count proposition shape and
rewrite integer divisibility as equality to zero in `ZMod n`; four mutations distinguish positivity,
domain, binder scope, and exact-count boundaries.

The provisional root vector remains `[H1, M3, R4]`: the primary theorem and proof were inspected but
not independently admitted to `H0`; the exact statement is worker-self-tested but dependency-ordered
behind an unaccepted intake receipt; and no source-faithful readable proof reconstruction exists.
No proof body, accepted state, audit completion, theorem completion, or master acceptance is claimed.
