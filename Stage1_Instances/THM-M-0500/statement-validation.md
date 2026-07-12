# Statement validation

The canonical target is `Stage1Instances.THM_M_0500.DirichletPrimesInAPTarget`: for every
`q : Nat` with `[NeZero q]` and every `a : ZMod q`, `IsUnit a` implies that the natural primes
reducing to `a` form an infinite set. The binder order and the `q = 1` boundary are explicit.

`Statement.lean` uses only `Mathlib.Data.ZMod.Coprime` for the statement vocabulary and
`Mathlib.Order.Interval.Finset.Basic` for the checked equivalence with unbounded existence. It does
not import `Mathlib.NumberTheory.LSeries.PrimesInAP`, so elaborating this phase cannot accidentally
credit mathlib's existing proof of the theorem.

## Validation record

Base revision: `aa55669bb59986e08ea8a0d1d77a1e40343d8142`.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-0500` | exit 0; rank 877, planned, theorem_complete false |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0500/Statement.lean` | exit 0; target and iff elaborated, four expected mutation mismatches printed, exact target and axioms printed |
| `cd Formalizations/Lean && python3 ../../Stage1_Instances/THM-M-0500/check_statement.py` | exit 0; expression SHA-256 `23806a3d...69bc`, file SHA-256 `b25800f3...b37`, all four mutations distinguished |
| `cd Formalizations/Lean && lake env lean --version` | exit 0; Lean 4.29.0 commit `98dc76e3` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | exit 0; `8a178386ffc0f5fef0b77738bb5449d50efeea95` |

The mutations remove the unit hypothesis, change primes from `Nat` to `Int`, existentially scope
the modulus instead of quantifying every modulus, and exclude `q = 1`. Lean rejects each as the
canonical target, and the independent expression comparison confirms that none serializes to the
same proposition. The checked transport reports only `propext`, `Classical.choice`, and
`Quot.sound`; no custom axiom is introduced.

Validation is nonrelease. The clone has a pre-existing untracked `.lake` symlink to canonical
pinned artifacts; it was used read-only. No update, build, clone, fetch, or dependency mutation was
performed.

## Boundary

This is a self-tested statement node pending master acceptance. It claims no primary-source audit,
anchor audit, proof credit, H/M/R promotion, audit completion, or theorem completion. The next gate
is `S56-M-0500-ANCHOR_AUDIT`.
