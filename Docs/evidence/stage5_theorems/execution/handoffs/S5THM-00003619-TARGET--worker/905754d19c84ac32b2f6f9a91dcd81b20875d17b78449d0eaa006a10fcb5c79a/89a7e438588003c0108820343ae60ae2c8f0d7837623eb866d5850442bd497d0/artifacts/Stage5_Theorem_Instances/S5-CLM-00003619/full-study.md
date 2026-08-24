# Full study: rapid quadratic growth and the Erdős series

## R0 — frozen statement binding

The frozen theorem quantifies an integer sequence `a`, assumes `StrictMono a`,
and assumes one positive real `C` for which `a (n+1) ≥ C * (a n)^2` for every
natural `n`. Its conclusion is precisely `Irrational (ErdosSeries a)`.

## R1 — hypotheses and exceptional cases

Both hypotheses are retained verbatim. No positivity of the sequence is added,
and no initial index or zero-denominator case is silently discarded. These
cases remain inside the provider theorem's quantified statement.

## R2 — formal inference

The claim-owned root applies the exact qualified provider declaration to `a`,
`h_mono`, and `h_rapid`. Lean unification checks that its resulting proposition
is the target proposition. This is the sole proof-composition edge.

## R3 — result, downstream use, and trust

The output is irrationality of the source-defined real series. The audit root
replays the same elaboration, while bidirectional identity transports protect
the statement boundary. The downstream Stage6 alias is `S6-CLM-00006228`.
Worker evidence is provisional: canonical recomputation and acceptance are a
Master-only trust boundary.
