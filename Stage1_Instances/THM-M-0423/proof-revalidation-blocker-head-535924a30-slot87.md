# THM-M-0423 Proof Revalidation: Blocked

Item `S56-M-0423-PROOF` was rechecked at base
`535924a30a83e9435b71f6163fe33bba6921212f` (tree
`0bce4f0de528486fc5f4e2b76a662697ca308883`) in exact claim order
`(v2 rank 301, phase layer 4, S56-M-0423-PROOF)`.

## Verdict

Outcome: `blocked`; worker verdict: `no_state_change`. No second proof receipt
and no `.stage1-worker-selftest.json` are issued. The assigned phase is already
provisional `[_]` with one attempt, and its obligation-tree predecessor is also
`[_]`, not master accepted. This recheck changes neither cursor and inherits no
acceptance.

The first failed gate is
`P01-ARTIFACTS/IMMUTABLE-VALIDATOR-FRESHNESS`. The exact mathematical phase
predicate also remains open at `P04-KERNEL/M0423-T-LOCAL-GLOBAL`.

## Dependency Audit

The authoritative direct/transitive hard-parent inspection order is exactly
empty. That sequence was traversed once before proof revalidation. There are no
hard edges, reuse hints, parent receipts, parent bodies, or parent artifacts to
consume.

Both nonblocking shared-module groups were inspected:

- `SHARED-MODULE-42c19d5b5a6d6b9e` only co-mentions
  `Mathlib.LinearAlgebra.QuadraticForm.Basic`. `THM-M-0050`, `THM-M-0211`, and
  `THM-M-0212` have intake probes, not frozen proof declarations for the target.
- `SHARED-MODULE-74cc3b6464e1332d` only co-mentions
  `Mathlib.LinearAlgebra.QuadraticForm.Real`. `THM-M-0600` has a conditional
  Morse-lemma package and a zero-dimensional branch, not a Hasse-Minkowski
  endpoint.

Both decisions remain `not_applicable`. No import, copy, transport, provider
receipt, proof credit, or checkbox acceptance is consumed.

The canonical `dependency-reuse-ledger.json` is schema 1.1 but was subsequently
rewritten for `S56-M-0423-VALIDATION`. It binds graph `eaee68bd...7153`, base
`94009a6b...c5e3`, phase layer 5, and the validation item. Current graph SHA-256
is `91ea782c...5067`, while the immutable proof validator requires the earlier
proof ledger at graph `3d32f808...bafa` and base `2dc5a410...9f7`. Rewriting the
canonical path alone would fail the validator's historical byte expectations
and would not prove the missing local-to-global theorem. This blocker therefore
records the exact drift without replacing the canonical ledger or the sole
proof receipt.

## Validator Boundary

The HEAD contract declares `check_proof.py` and `check_proof.sh` candidates.
Exactly one exists:

```text
Stage1_Instances/THM-M-0423/check_proof.py
SHA-256 cbfa4da1faeba717b79f3cc1437fbcf16da9159b914cefce0d4cd8c741430919
Git blob 178ecfb33b9e4027060856db324b268254b26fde
```

The worker did not edit, refresh, replace, rename, delete, or add either
candidate. The required exact replay was:

```text
/usr/bin/python3 -I -B Stage1_Instances/THM-M-0423/check_proof.py
```

It exited `1` and emitted exactly one JSON object with schema
`stage1-validator-semantic-result/1.0`. Its semantic fields were
`status=failed`, `verdict=repair_required`, `phase_accepted=false`,
`phase_predicate_proven=false`, and `first_failed_gate=P01-ARTIFACTS`; the
message was `proof evidence replay failed: repository HEAD differs from the
claimed worker base`.

That negative result is correct. The validator freezes base `2dc5a410...`, tree
`841bdd61...`, graph `3d32f808...`, proof state `[ ]`, and attempts `0`.
Current authority records base `535924a30...`, tree `0bce4f0d...`, graph
`91ea782c...`, state `[_]`, and attempts `1`. The scheduler-owned role map at
`.cron/stage1-v2-app-server/role-maps/S56-M-0423-PROOF.json` is also absent.
The worker cannot lawfully repair either scheduler-owned input.

The existing `proof-receipt.json` is the sole phase receipt. It remains a
historical schema-1.0 receipt from base `2dc5a410...`, bound to the old graph,
old task cursor, and proof-ledger SHA-256 `9036cac5...d91`. It was not replaced
by a misleading second receipt.

## Kernel Boundary

The exact frozen target remains
`Stage1.THM_M_0423.HasseMinkowskiStatement`: for every number field and every
nondegenerate finite-dimensional quadratic form, global nonzero isotropy is
equivalent to isotropy over every finite and infinite completion. A theorem
over `Q`, a finite-place-only theorem, a generic variety Hasse principle, or a
conditional root is not this target.

Scratch copies of the exact tracked `Statement.lean`, `ObligationTree.lean`,
and `Proof.lean` were replayed with `lake env lean --trust=0 -t0` against the
existing pinned cache. All three elaborated. Their olean SHA-256 values were:

- `Statement.olean`: `e36b0b8f894305089b48a67345f750edb3799ef2685ad47081b2eedd830fe26e`
- `ObligationTree.olean`: `b18e17120ae71d513305d7ba82861f9048cc33b7fadfea03d79e9c1d109003fd`
- `Proof.olean`: `f5bc8bd6fcad7fe1af11da34aeefd3b4b5d08c8c6058fe8637f29691385c6561`

The easy global-to-local body, scalar-extension witness lemma, isometry
transport, diagonalization adapter, and complex classification bodies are real
and placeholder-free. Their machine-derived axiom union is exactly `propext`,
`Classical.choice`, and `Quot.sound`.

The three root-facing combinators are conditional. `root_composition` and
`direction_package` take `LocalToGlobalObligation` as an argument, while
`root_from_direction_package` takes a package containing that same missing
direction. None constructs it. No unconditional declaration inhabiting
`LocalToGlobalObligation` or `HasseMinkowskiStatement` exists in the target,
legacy Stage1 module, repository-local Lean closure, or pinned dependency audit.

The frozen registry retains 94 required machine obligations and 32 executable
proof leaves, with zero accepted closures and zero composition certificates.
The immediate root cut is `M0423-T-LOCAL-GLOBAL`; machine debt remains `M3`.

## Checks

Before adding this blocker pair, the Stage1 standard, v2 theorem DAG, phase
acceptance contract, target manifest, and target display all passed. The exact
validator replay failed with the typed result above. Trust-zero Lean replay and
the placeholder scan passed. Pinned mathlib remained clean at revision
`8a178386...ea95`, tree `bdc39a31...c2b`, under Lean 4.29.0.

No network request, `lake update`, `lake build`, dependency clone/fetch, or
`.lake` mutation ran. The automation-provided `.lake` symlink was reused
read-only and remains warm nonrelease input.

After this pair is added, aggregate theorem-DAG freshness is expected to fail
until scheduler integration regenerates the protected evidence inventory. The
worker will validate the new JSON and whitespace but will not edit any
authority or projection.

## Retry Condition

The scheduler must publish a fresh immutable proof validator and the required
per-item role map at a base that already contains both, then issue a new claim.
That claim must refresh the proof-scoped schema-1.1 canonical ledger and sole
phase receipt against the current graph, task cursor, source, validator, role
map, exact commands, and semantic result.

Validator maintenance alone does not close the mathematics. Proof completion
also requires a placeholder-free exact body for the arbitrary-number-field
`LocalToGlobalObligation`, followed by checked root composition and complete
obligation, provenance, trust, and consumer replay evidence.

This pair is current-base target-scoped blocker evidence only. It does not
self-test or satisfy `S56-M-0423-PROOF`, propose a state transition, replace the
sole receipt, canonical ledger, or validator, claim accepted reuse, close an
accepted obligation or the exact root, establish M0, claim validation or
release, decide AUDIT-Z or THEOREM-Z, complete the theorem, or claim master
acceptance.
