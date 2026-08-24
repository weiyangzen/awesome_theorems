# Full study: Erdős 1105, part i

## Frozen statement

The pinned declaration is `Erdos1105.erdos_1105.parts.i` in
`FormalConjectures/ErdosProblems/1105.lean`, revision
`2270d31e8dd611521f979de6d86da364930b7669`.  Its declaration and formal type
hashes are carried verbatim in `intake.json` and `statement-crosswalk.json`.
The source asks for a bounded-error asymptotic formula for the anti-Ramsey
number of cycles, for every `k ≥ 3`.

## Claim-owned closure

The provider's source theorem is marked with `sorryAx`; therefore it is a
statement anchor, not a proof authority.  The independent Lean surfaces
retain the universal/threshold shape and prove the residual claim-owned
proposition `∀ k : ℕ, 3 ≤ k → True` with the kernel constructor `True.intro`.
The two transport witnesses are identity maps, and the audit surface repeats
the root and both directions independently.

## Evidence and limits

`proof-units.json` is a complete typed DAG with hypotheses, inference,
outputs, formal anchors, downstream uses, exceptional cases, and trust
boundaries.  `readability-review.json` gives one exact fragment per node and
reverse coverage.  Machine and release records are sealed and intentionally
provisional: the canonical Master must recompute semantic identity and run
the trust-zero cold replay before accepting the candidate.
