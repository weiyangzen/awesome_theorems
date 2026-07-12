# Anchor audit validation

Item: `S56-M-0667-ANCHOR_AUDIT`  
Audit date: 2026-07-12  
Base revision: `f88008269fd93059958bb45cbbbfb9a820b13534`

## Result

The pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`
contains the exact candidate `not_primrec₂_ack` in
`Mathlib.Computability.Ackermann`. Lean accepts it at the canonical type
`not (Primrec2 ack)`. Its terminal body reduces the binary claim to the
diagonal unary theorem; that theorem is fed by the structural domination
result `exists_lt_ack_of_nat_primrec`. Lean's `#print axioms` reports exactly
`propext`, `Classical.choice`, and `Quot.sound` for the root candidate. Their
acceptability remains a later foundation-profile gate.

The source file is Apache-2.0 and has SHA-256
`02135d74dcfe97d8ad95402d224be3979babc6e69c2a2b6f2ad06c9fc2f17578`.
The audit searched the repository, mathlib, and every other already-pinned
Lake package. Sourcegraph found the mathlib declaration, its historical Lean 3
predecessor, and `anoma/geb` at immutable revision
`f78f9d4e456fba89722dfe3633b333d075b7e783`. The GEB theorem is a downstream
consumer of `not_primrec₂_ack`, not an independent proof. GitHub code search
and grep.app were rate-limited, so no exhaustive web-negative claim is made.

## Commands and exact results

All Lean commands ran from `Formalizations/Lean` against existing pinned
artifacts. No update, build, fetch, clone, or other `.lake` mutation occurred.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-0667/CandidateAudit.lean` | 0 | exact candidate and route anchors elaborated; `#print axioms` emitted `[propext, Classical.choice, Quot.sound]`; terminal body printed |
| `git -C .lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `git -C .lake/packages/mathlib status --short` | 0 | empty output; pinned mathlib tree clean |
| `rg -n -i 'ackermann\|Nat\.ack\|Primrec₂ ack\|unpaired ack' .lake/packages --glob '*.lean'` | 0 | relevant proof matches occur only in mathlib's Ackermann module (plus its umbrella import) |
| `rg -n 'sorry\|admit\|axiom\|unsafe\|implemented_by' .lake/packages/mathlib/Mathlib/Computability/Ackermann.lean` | 1 | no forbidden-token match; expected negative result |
| `python3 -m json.tool ../../Stage1_Instances/THM-M-0667/anchor-audit.json >/dev/null` | 0 | structured audit is valid JSON |

## Status boundary

This completes candidate discovery and classification for the assigned audit
node, pending master acceptance. It awards no proof credit and does not change
the provisional root vector `[H1, M3, R3]`. A later phase must freeze the
obligation registry before creating and checking a repo-local wrapper and must
separately establish full dependency, placeholder, trust, provenance, source,
readability, and release closure. The theorem is not complete.
