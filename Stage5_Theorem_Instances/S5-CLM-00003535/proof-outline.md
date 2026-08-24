# Proof outline — Boshernitzan root

## Root proposition

For a positive real sequence `r`, if its range is unbounded above and
`r (n + 1) / r n` tends to `1` along `atTop`, then the set of real `ξ` whose
image orbit `↑(ξ * r n)` in `AddCircle (1 : ℝ)` is not dense has Hausdorff
dimension zero.

## Typed composition ledger

1. `PU-SOURCE` freezes the exact provider block and its statement-only trust
   boundary.
2. `PU-HYPOTHESES` preserves all three hypotheses with their original binder
   order and types.
3. `PU-TRANSPORT-FWD` checks source-to-target transport of the fully expanded
   proposition.
4. `PU-TRANSPORT-REV` checks target-to-source transport and blocks a merely
   text-identical but semantically substituted header.
5. `PU-ROOT` applies the claim proof object to the supplied sequence and emits
   exactly the dimension-zero conclusion.

No hypothesis is dropped, strengthened, or silently inferred.  The output,
formal anchors, downstream transport uses, exceptional non-density set, and
trust boundaries are all represented in the structured ledger.
