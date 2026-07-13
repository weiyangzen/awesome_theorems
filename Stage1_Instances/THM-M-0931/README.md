# THM-M-0931 rev-5.6 intake

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
must be frozen by the dependent statement phase. Intake therefore records the exact source lead but
does not prematurely install a canonical expression.

## Lean boundary

Pinned mathlib contains indexed and multiset versions over integers and `ZMod n` in
`Mathlib.Combinatorics.Additive.ErdosGinzburgZiv`. The closest occurrence-preserving candidate is
`Int.erdos_ginzburg_ziv_multiset`; it accepts at least `2 * n - 1` elements and reports axioms
`propext`, `Classical.choice`, and `Quot.sound`. `IntakeProbe.lean` authenticates the four public
candidates and their reported axiom surface. It is discovery evidence, not a canonical wrapper,
source transport, downstream anchor audit, or proof receipt.

The provisional root vector is `[H1, M3, R4]`: the primary theorem and proof were inspected but not
independently admitted to `H0`; exact pinned formal candidates exist but no source-identical target,
transport, provenance closure, or accepted `M0` evidence is frozen; and no source-faithful readable
proof reconstruction exists. All six downstream tasks remain open in `task-dag.json`. No accepted
state, audit completion, theorem completion, or master acceptance is claimed.
