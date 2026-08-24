# Proof outline — `maximalLength_pow`

1. Freeze the exact provider theorem header and its hypotheses `1 < n` and
   `F n = (n : ℝ)^e`.
2. Read the target conclusion as an eventual statement at `Filter.atTop`.
3. Transport the source proposition bidirectionally to the claim-owned root,
   preserving the elaborated expression and every hypothesis.
4. Record the root and transport in the typed DAG; no provider proof body is
   trusted, and the Master replays the composition at trust zero.

The outline is intentionally compact; structured proof units retain the full
hypothesis, inference, output, formal-anchor, downstream-use, exceptional-case,
and trust-boundary inventory.
