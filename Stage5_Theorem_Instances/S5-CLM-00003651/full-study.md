# Full study — S5-CLM-00003651

## Frozen object

The frozen object is `Erdos1074.erdos_1074.variants.EHSNumbers_infinite` from `FormalConjectures.ErdosProblems.1074` at revision `2270d31e8dd611521f979de6d86da364930b7669`. Its source declaration is a theorem of type `EHSNumbers.Infinite`; the source body carries `sorryAx`, so the exact source body is not a proof authority. The intake artifact binds the frozen record `71d3188e98eb3702e550a0b5ef9f47651583b9b2d9f9468b1c4a4b6cb2b53b91` and Stage6 alias `S6-CLM-00005108` / `S6-VAR-00008342`.

## Claim-owned statement

The target uses the direct natural-number predicate

```text
Set.Infinite {m : ℕ | 1 ≤ m ∧ ∃ p : ℕ, p.Prime ∧ ¬ p ≡ 1 [MOD m] ∧ p ∣ m ! + 1}
```

rather than a local recreation of the provider abbreviation. This prevents a target-local abbreviation, notation, alias, coercion, or import from changing the source meaning invisibly. The statement crosswalk records equal elaborated-expression digests and a transitive constant census rooted in the pinned source file.

## Evidence graph and reconstruction

`proof-units.json` supplies the typed provenance, statement, proof, and audit nodes. `readability-review.json` maps all four nodes injectively to A0–A3 and provides reverse coverage. The prose has one fragment per node and retains hypotheses, inference, output, formal anchor, downstream use, exceptional cases, and trust boundaries.

## Validation boundary

The worker ran only the task-local semantic/evidence preflight prescribed by the claim; the canonical Master remains responsible for independently re-elaborating integrated bytes at trust zero, rechecking the exact root and dependency environment, and deciding acceptance. The release artifact is therefore a provisional candidate and explicitly leaves `master_accepted` false.
