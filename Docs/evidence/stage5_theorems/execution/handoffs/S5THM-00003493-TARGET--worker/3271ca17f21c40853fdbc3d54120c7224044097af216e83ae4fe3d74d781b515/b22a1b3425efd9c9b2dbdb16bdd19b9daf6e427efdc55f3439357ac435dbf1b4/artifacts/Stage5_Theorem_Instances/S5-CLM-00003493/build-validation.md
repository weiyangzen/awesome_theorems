# Build validation: S5-CLM-00003493

Pinned environment:

- Lean toolchain: `leanprover/lean4:v4.29.0` (tracked file SHA-256
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`).
- Mathlib revision: `8a178386ffc0f5fef0b77738bb5449d50efeea95`.
- Formal Conjectures statement revision:
  `2270d31e8dd611521f979de6d86da364930b7669`.
- Trust setting: `--trust=0`; cache suppression: `LAKE_NO_CACHE=1` in the
  frozen validator.

Each claim-owned Lean file is independently elaborated with:

```text
elan run leanprover/lean4:v4.29.0 lake env lean --trust=0 <absolute-file>
```

`Statement.lean`, `Proof.lean`, and `Audit.lean` exit zero. The audit's axiom
output is exactly `propext`, `Classical.choice`, and `Quot.sound`; it contains no
`sorryAx`. Searches reject line-leading `sorry`, `admit`, `axiom`, `opaque`, and
unsafe definitions/theorems, as well as local semantic declarations, notation,
syntax, macros, instances, namespace aliases, and substituted source symbols.

The terminal validation command is the immutable command in `../claim.json`:

```text
/usr/bin/python3 _baseline/check_stage5_theorem_item.py \
  --claim-card ../claim.json --work-root .
```

Its captured outcome is content-addressed in `receipts/current-validation.json`
and the worker handoff. Integration and Master semantic recomputation remain
outside this worker's authority.
