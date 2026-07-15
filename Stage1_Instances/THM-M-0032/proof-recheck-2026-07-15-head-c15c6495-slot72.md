# THM-M-0032 proof recheck at `c15c6495`

Item: `S56-M-0032-PROOF`

Intent: `prove`

Base revision: `c15c649568664c4e58150dd755cb28f156d15ecb`

Base tree: `792c3ed97f9263da7e6a39abdce8d5e37a100368`

Recorded: 2026-07-15 +08:00

## Verdict

`blocked`; no state change.

The exact frozen target remains

```text
forall (R : Type u) [CommRing R] [IsRegularLocalRing R],
  UniqueFactorizationMonoid R
```

The current pinned Lean 4.29.0/mathlib `8a178386` closure contains no placeholder-free body for
either immediate theorem-specific package `M0032-N-DOMAIN` or
`M0032-A-PRIME-ELEMENT`. `PinnedClosureProbe.lean` is a checked negative fixture: in the exact
regular-local context it authenticates failed synthesis of both `IsDomain R` and
`UniqueFactorizationMonoid R`. It declares no theorem, instance, axiom, or proof body.

`ObligationTree.lean` still has genuine checked bodies for the generic Kaplansky criterion and
conditional child-to-root composition. The composition takes `RegularLocalDomainPackage` and
`RegularLocalPrimeElementPackage` as premises and constructs neither. Crediting it would substitute
a conditional theorem for the requested unrestricted theorem.

## External candidate boundary

Mathlib PR #39510 supplies an exact placeholder-free terminal at immutable head
`6d76bb4118837f7f8d7669c9b0b7d06bc59081c7`:

```lean
IsRegularLocalRing.uniqueFactorizationMonoid
    [IsRegularLocalRing R] : UniqueFactorizationMonoid R
```

Its `UFD.lean` snapshot has SHA-256
`f805872158810168eb6a3c58ea1d28959f0d88937712116245dcbaf4dfa8b6a1`, and its prohibited-token
scan is empty. It is not usable in this assignment's frozen environment. The candidate uses Lean
4.32.0-rc1 and directly imports seven modules absent from the pinned worktree:

```text
Mathlib.Algebra.Module.FiniteFreeResolution.BaseChange
Mathlib.Algebra.Module.FiniteFreeResolution.HasProjectiveDimensionLE
Mathlib.Algebra.Module.StablyFree.FreeOfInvertible
Mathlib.Algebra.Module.StablyFree.HasFiniteFreeResolution
Mathlib.RingTheory.Ideal.UFD
Mathlib.RingTheory.LocalProperties.Invertible
Mathlib.RingTheory.RegularLocalRing.Localization
```

The immutable PR commit is also absent from the local pinned Git object store. Importing or
replaying it would therefore require the prohibited dependency/toolchain mutation. It was not
imported, fetched, kernel-replayed, or credited.

No proof source, receipt, obligation status, authoritative cursor, or dependency was changed. The
lifecycle stays `planned`; the root vector stays `[H1, M3, R4]`; accepted receipts and newly closed
obligations stay empty; and `audit_complete` and `theorem_complete` stay false. Because the proof
phase is incomplete, `.stage1-worker-selftest.json` is deliberately absent.

## Validation

All Lean commands ran in this worker clone with the existing pinned Lake closure. The
automation-provided untracked `Formalizations/Lean/.lake` symlink was reused read-only. No `lake
update`, `lake build`, dependency clone/fetch, checkout, or `.lake` mutation ran. Temporary Lean
outputs were written under `/tmp` and removed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0032` | 0 | Rank 1076; lifecycle `planned`; baseline `L0/rework_required`; theorem incomplete. |
| Isolated pinned `lake env lean --trust=0 -t0` replay of `Statement.lean`, `ObligationTree.lean`, `AnchorAudit.lean`, and `PinnedClosureProbe.lean` | 0 | All four elaborated; exact target, checked conditional composition, and intentional missing-instance boundary were rechecked. |
| `python3 -B Stage1_Instances/THM-M-0032/check_obligation_tree.py` | 1 | The predecessor-phase checker reached its final former-worker packet read and failed because `.stage1-worker-selftest.json` is absent; this blocked proof worker must not recreate that packet. |
| Prohibited-construct scan over owned `*.lean` files | 1 | Expected no-match: no `sorry`, `admit`, `sorryAx`, `native_decide`, `axiom`, `constant`, `opaque`, `unsafe`, `extern`, `external`, `implemented_by`, or `run_tac`. |
| Pinned terminal search | 1 | Expected no-match for a regular-local-to-domain or regular-local-to-UFD body; the only pinned RingTheory source using `IsRegularLocalRing` is `RegularLocalRing/Defs.lean`. |
| Required PR-import presence probe | 0 | All seven direct imports of the exact external terminal were confirmed absent from pinned mathlib. |
| `git -C Formalizations/Lean/.lake/packages/mathlib cat-file -e '6d76bb4118837f7f8d7669c9b0b7d06bc59081c7^{commit}'` | 128 | The external candidate commit is absent from the local pinned object store. |
| Environment and pin inspection | 0 | Lean 4.29.0 (`98dc76e3...6740`), mathlib `8a178386...ea95` tree `bdc39a31...c2b`; toolchain and manifest hashes match the dossier. |

## Retry condition

Resume after an authorized compatible pin integrates and independently replays PR #39510 head
`6d76bb4118837f7f8d7669c9b0b7d06bc59081c7`, or after equivalent placeholder-free
implementations of `M0032-N-DOMAIN` and `M0032-A-PRIME-ELEMENT` with their frozen dependencies exist
in the pinned closure. Then run exact-type, provenance, placeholder, axiom, composition, trust, and
receipt checks.

This is durable blocker evidence, not a proof receipt. It does not satisfy `S56-M-0032-PROOF`.
