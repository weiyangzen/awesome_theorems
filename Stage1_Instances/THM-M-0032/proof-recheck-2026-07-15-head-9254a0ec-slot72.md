# THM-M-0032 proof recheck at `9254a0ec`

Item: `S56-M-0032-PROOF`

Intent: `prove`

Base revision: `9254a0ec0d0c71b346ae15a911721409e3ab3139`

Base tree: `a3de0086d55c8f209894b07409deeeed04c393a3`

Recorded: 2026-07-15 15:52:04 +08:00

## Verdict

`blocked`; no state change.

The exact frozen target remains

```text
forall (R : Type u) [CommRing R] [IsRegularLocalRing R],
  UniqueFactorizationMonoid R
```

The immediate open machine cut remains `M0032-N-DOMAIN` and
`M0032-A-PRIME-ELEMENT`. Pinned mathlib has no placeholder-free derivation of
`IsDomain R` from the exact regular-local context. Independently, it has no
proof that every height-one prime of a regular local ring is principal, the
central engine needed to show that every nonzero prime ideal contains a prime
element.

`ObligationTree.lean` has genuine checked bodies for the generic Kaplansky
criterion and child-to-root composition. The composition takes
`RegularLocalDomainPackage` and `RegularLocalPrimeElementPackage` as premises;
it constructs neither. Returning it would substitute a conditional theorem
for the requested theorem, while introducing either premise as an axiom or
bodyless declaration would be a prohibited placeholder.

The pinned `RegularLocalRing/Defs.lean` is the only mathlib RingTheory file
using `IsRegularLocalRing`. It contains the class, equivalent views,
ring-equivalence transport, and a reverse support instance from a local
principal ideal domain, but no forward domain bridge, height-one
principalization, localization or quotient regularity, prime-element package,
or UFD terminal. Repository-local and pinned-package searches found no other
exact body.

## Exact External Candidate

The prior anchor dossier's statement that no exact external terminal was known
is now superseded by read-only discovery, but not by eligible proof credit.
Mathlib PR [#39510](https://github.com/leanprover-community/mathlib4/pull/39510),
`WIP: any regular local ring is a UFD`, has an exact terminal at immutable head
`6d76bb4118837f7f8d7669c9b0b7d06bc59081c7`:

```lean
IsRegularLocalRing.uniqueFactorizationMonoid
    [IsRegularLocalRing R] : UniqueFactorizationMonoid R
```

The same head supplies `isDomain_of_isRegularLocalRing`. The inspected
`Mathlib/RingTheory/RegularLocalRing/UFD.lean` and `Basic.lean` snapshots have
SHA-256 values `f8058721...b6a1` and `dcd3ecb0...5e7e`; their prohibited-token
scan was empty. GitHub reported successful Build, Test-and-lint, and Lint-style
checks for the head. That is credible exact source evidence, not this worker's
kernel replay.

The candidate is ineligible in the frozen environment. Its toolchain is Lean
`v4.32.0-rc1`, not pinned Lean `v4.29.0`; it uses a substantial new chain of
regular-local localization, global-dimension, finite-free-resolution,
invertibility, and ideal-UFD modules absent from pinned mathlib `8a178386`.
The head object and `UFD.lean` are absent locally. The PR is open, draft,
currently dirty/nonmergeable, and has unresolved dependency PRs. Importing or
replaying it here would require a prohibited dependency/toolchain mutation, so
it was not imported, replayed, or credited.

No proof source, receipt, obligation status, authoritative cursor, or
dependency was changed. Lifecycle remains `planned`; the vector remains
`[H1, M3, R4]`; accepted receipts and closed obligations remain empty; and
`audit_complete` and `theorem_complete` remain false. Because the assigned
proof phase is incomplete, `.stage1-worker-selftest.json` is deliberately
absent.

## Validation

All Lean commands ran in this worker clone using the existing pinned Lake
closure. The automation-provided untracked `Formalizations/Lean/.lake` symlink
was reused read-only. No `lake update`, `lake build`, dependency clone/fetch,
checkout, or `.lake` mutation ran. Temporary Lean objects and logs were
created under `/tmp` and removed. Network access was read-only discovery only;
a final unauthenticated GitHub retry received HTTP 403 after rate exhaustion.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0032` | 0 | Rank 1076; lifecycle `planned`; baseline `L0/rework_required`; theorem incomplete. |
| Isolated pinned `lake env lean --trust=0 -t0` replay below | 0 | `Statement.lean`, `ObligationTree.lean`, and `AnchorAudit.lean` elaborated. The exact transport and conditional composition report only `propext`, `Classical.choice`, and `Quot.sound`; the anchor retains the expected UFD synthesis failure. |
| `python3 Stage1_Instances/THM-M-0032/check_obligation_tree.py` | 1 | The historical predecessor-phase validator reached its final former-worker-packet check and failed because `.stage1-worker-selftest.json` is absent; that packet is deliberately not created for this blocked proof phase. |
| Prohibited-construct scan over owned `*.lean` files | 1 | Expected no-match: no `sorry`, `admit`, `sorryAx`, `native_decide`, `axiom`, `constant`, `opaque`, `unsafe`, `extern`, `external`, `implemented_by`, or `run_tac`. |
| Repository/pinned terminal search | 0 | Hits are limited to this dossier and pinned `RegularLocalRing/Defs.lean`; no exact terminal or forward domain bridge exists. |
| Read-only inspection of PR #39510 head `6d76bb41...e1c7` | 0 | Found the exact placeholder-free UFD instance and domain theorem; immutable source hashes match the JSON record. The candidate was not imported or kernel-replayed. |
| Pinned `UFD.lean` absence probe | 0 | The exact candidate module is absent from the pinned mathlib worktree. |
| Pinned Git object probe for `6d76bb41...e1c7` | 128 | `fatal: Not a valid object name`; the external head is not cached locally. |
| Environment and pin inspection | 0 | Lean `4.29.0` (`98dc76e3...6740`), Lake `5.0.0-src+98dc76e`, mathlib `8a178386...ea95` tree `bdc39a31...c2b`; toolchain and manifest hashes agree. |
| Final unauthenticated GitHub retry | 22 | HTTP 403 rate-limit response; no dependency or workspace state changed. |

Exact narrow Lean replay:

```bash
set -euo pipefail
repo=$PWD
lean_root=$repo/Formalizations/Lean
target=$repo/Stage1_Instances/THM-M-0032
tmp=$(mktemp -d /tmp/thm-m-0032-proof-slot72-current.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
lean=$(cd "$lean_root" && lake env which lean)
lean_path=$(cd "$lean_root" && lake env printenv LEAN_PATH)
cd "$target"
LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" \
  "$lean" --trust=0 -t0 -o "$tmp/Statement.olean" Statement.lean
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" \
  "$lean" --trust=0 -t0 ObligationTree.lean
LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" \
  "$lean" --trust=0 -t0 AnchorAudit.lean
```

Output SHA-256 values are `2a26d392...637d1` for the statement,
`fc1829fe...5e12` for the obligation composition, and
`8d3b1018...968f` for the anchor. The temporary `Statement.olean` hash was
`1dd0720b...f19d`. The paired JSON artifact binds the complete source,
environment, failed-gate, candidate, command, and retry evidence.

## Retry Condition

Resume by integrating and independently replaying immutable PR #39510 head
`6d76bb4118837f7f8d7669c9b0b7d06bc59081c7` under an authorized compatible
dependency/toolchain pin, or after equivalent placeholder-free implementations
of `M0032-N-DOMAIN` and `M0032-A-PRIME-ELEMENT` with their frozen dependencies
exist in the pinned closure. Then run exact-type, provenance, placeholder,
axiom, composition, trust, and receipt checks.

This is durable blocker evidence, not a proof receipt, and it does not satisfy
`S56-M-0032-PROOF`.
