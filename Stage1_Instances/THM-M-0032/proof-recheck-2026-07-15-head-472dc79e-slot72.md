# THM-M-0032 proof recheck at `472dc79e`

Item: `S56-M-0032-PROOF`

Intent: `prove`

Base revision: `472dc79eb4d406a6707691193fbe3ab58d0f0cc4`

Base tree: `881d873727dc80435119839b8e60e9e9c2cfb208`

Recorded: 2026-07-15 15:14:03 +08:00

## Verdict

`blocked`; no state change.

The exact frozen target remains

```text
forall (R : Type u) [CommRing R] [IsRegularLocalRing R],
  UniqueFactorizationMonoid R
```

The immediate open machine cut is unchanged:
`M0032-N-DOMAIN` and `M0032-A-PRIME-ELEMENT`. Pinned mathlib has no
placeholder-free derivation of `IsDomain R` from the exact regular-local
context. Independently, it has no proof that every height-one prime of a
regular local ring is principal, which is the central engine required to show
that each nonzero prime ideal contains a prime element.

`ObligationTree.lean` contains genuine checked bodies for the generic
Kaplansky criterion and for child-to-root composition. The latter takes
`RegularLocalDomainPackage` and `RegularLocalPrimeElementPackage` as premises;
it constructs neither. Returning that conditional declaration would weaken
the requested theorem, while declaring either premise as an axiom or bodyless
theorem would be a prohibited placeholder.

The pinned `RegularLocalRing/Defs.lean` is the only mathlib RingTheory file
using `IsRegularLocalRing`. It defines the class, two equivalent views,
ring-equivalence transport, and the reverse support instance from a local
principal ideal domain. It contains no domain, quotient/localization
regularity, height-one-principal, prime-element, or UFD terminal theorem.
Repository-local and pinned-package searches found no other exact body.

A locally materialized, unpinned mathlib Git object at
`e752928d1223d1202d969b623a6f27cc79866e9c` adds generic UFD criteria via
height-one primes and localization. It is absent from the pinned `8a178386`
worktree and manifest, so it was not imported or credited. More importantly,
it still assumes both `IsDomain` and height-one principality and therefore
closes neither theorem-specific cut package. Even the cached master ref has no
`IsRegularLocalRing -> IsDomain` or `IsRegularLocalRing -> UFD` result.

No proof source, receipt, obligation status, authoritative cursor, or
dependency was changed. The lifecycle stays `planned`; the vector stays
`[H1, M3, R4]`; accepted receipts and closed obligations stay empty; and
`audit_complete` and `theorem_complete` stay false. Because this proof phase
is incomplete, `.stage1-worker-selftest.json` is deliberately absent.

## Validation

All commands ran in this worker clone using the existing pinned Lake closure.
The automation-provided untracked `Formalizations/Lean/.lake` symlink was
reused read-only. No `lake update`, `lake build`, dependency clone/fetch,
checkout, or `.lake` mutation ran. Temporary Lean objects and logs were
created under `/tmp` and removed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0032` | 0 | Rank 1076; lifecycle `planned`; baseline `L0/rework_required`; theorem incomplete. |
| Isolated pinned `lake env lean --trust=0 -t0` replay below | 0 | `Statement.lean`, `ObligationTree.lean`, and `AnchorAudit.lean` elaborated. The binder transport and both conditional composition declarations report only `propext`, `Classical.choice`, and `Quot.sound`; the anchor retains the expected UFD synthesis failure. |
| Temporary pre-proof run of `check_obligation_tree.py` with only its historical worker-packet tail omitted | 0 | All generated artifacts, 38 obligations, 83 typed edges, denominator `7ddbec79...451c7`, pins, forbidden-token checks, and the open `H1/M3/R4` boundary passed. |
| `python3 Stage1_Instances/THM-M-0032/check_intake.py` | 1 | Historical validator is stale: it requires intake state `[ ]`, while integration has provisionally advanced that authoritative cursor to `[_]`. |
| `python3 Stage1_Instances/THM-M-0032/check_statement.py` | 1 | Historical validator rejects the current authoritative blueprint hash before its old worker-packet check. |
| `python3 Stage1_Instances/THM-M-0032/check_anchor_audit.py` | 1 | Historical validator requires the former anchor worker's ephemeral root self-test packet, correctly absent from this proof worker. |
| `python3 Stage1_Instances/THM-M-0032/check_obligation_tree.py` | 1 | Structural assertions ran before the historical validator failed only on the former obligation-tree worker packet, correctly absent here. |
| Prohibited-construct scan over owned `*.lean` files | 1 | Expected no-match: no `sorry`, `admit`, `sorryAx`, `native_decide`, `axiom`, `unsafe`, `external`, or `implemented_by`. |
| Pinned/cached-ref terminal search | 1 | Expected no-match for a regular-local-to-domain or regular-local-to-UFD body. |
| Environment and pin inspection | 0 | Lean `4.29.0` (`98dc76e3...6740`), Lake `5.0.0-src+98dc76e`, mathlib `8a178386...ea95` tree `bdc39a31...c2b`; toolchain and manifest hashes agree. |

Exact narrow Lean replay:

```bash
set -euo pipefail
repo=$PWD
lean_root=$repo/Formalizations/Lean
target=$repo/Stage1_Instances/THM-M-0032
tmp=$(mktemp -d /tmp/thm-m-0032-proof-slot72.XXXXXX)
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
environment, failed-gate, command, and retry evidence.

## Retry Condition

Resume after placeholder-free implementations of `M0032-N-DOMAIN` and
`M0032-A-PRIME-ELEMENT` with their frozen dependencies exist in the pinned
closure, or after an immutable compatible exact Lean 4 proof is pinned or
imported and passes exact-type, provenance, placeholder, axiom, composition,
and trust checks.

This is durable blocker evidence, not a proof receipt, and it does not satisfy
`S56-M-0032-PROOF`.
