# THM-M-0423 proof-phase attempt

Item: `S56-M-0423-PROOF`

Intent: `prove`

Base revision: `69662621a19907de342801b09124e8dfe3495e40`

Base tree: `fbfbc07e2045accdd0144baf892481a9bb6717f8`

Recorded: 2026-07-15 19:17:16 +08:00

## Verdict

`blocked`; no state change and no completion self-test.

The exact frozen target is `Stage1.THM_M_0423.HasseMinkowskiStatement`: for every number field and
every nondegenerate finite-dimensional quadratic form, a nonzero global isotropic vector exists
exactly when one exists after scalar extension at every finite and every infinite place. A theorem
only over `Q`, only at finite places, for a different Hasse-principle family, or conditional on the
hard implication cannot replace it.

The first failed gate is `M0423-T-LOCAL-GLOBAL`. No placeholder-free body inhabits
`Stage1.THM_M_0423.ObligationTree.LocalToGlobalObligation` in the repository or installed pinned
dependency closure. The frozen route expands this implication through diagonalization and place
normalization, real/complex/nonarchimedean quadratic-form classification, Hilbert symbols and local
Hasse invariants, arbitrary-number-field Hilbert reciprocity, global invariant realization, global
Witt uniqueness and injectivity, cancellation, witness extraction, and exact transport back. Its
30 executable leaves lie below this hard direction. The whole frozen graph has 32 executable
leaves; none has accepted E0/E1 closure, and there are no child-to-parent composition certificates.

`ObligationTree.lean` does contain real placeholder-free bodies for scalar-extension witness
preservation and the global-to-local direction. Its three root-facing combinators are conditional:
`root_composition` and `direction_package` consume the missing hard implication, and
`root_from_direction_package` consumes a package containing it. Returning one of them with an
assumed premise would prove a different conditional theorem, not the assigned root.

This attempt adds four genuine partial proof bodies in `Proof.lean`:

- `isIsotropic_iff_of_isometryEquiv` implements the planned bidirectional nonzero-witness transport
  planned by `M0423-T-GLOBAL-ISOTROPY-TRANSPORT`.
- `equivalent_weightedSumSquares_units` wraps pinned diagonalization for a nondegenerate form and
  implements the planned signature of `M0423-C-BASIS-DIAGONAL`.
- `equivalent_sumSquares_of_isAlgClosed` wraps the pinned algebraically closed classification, and
  `equivalent_sumSquares_complex` specializes it literally to complex scalars for
  `M0423-L-COMPLEX-CLASSIFICATION`.

All four are placeholder-free and trust-zero elaborated. The registry endpoints still have planned
fingerprints, so these are candidate implementations pending independently reviewed exact endpoint
fingerprints and E0/E1 receipts, not accepted leaf closures or parent composition certificates.
The prerequisite remains provisional `[_]`, so this is non-credit exploratory work rather than a
dependency-legal proof-node transition. The bodies do not supply the hard local-to-global implication.

Pinned mathlib supplies supporting APIs only: finite and infinite completions,
`QuadraticForm.baseChange_tmul`, faithfully-flat tensor injection, real classification, and the
ordinary number-field product formula. A bounded scan of every installed pinned Lean package found
no Hasse-Minkowski, quadratic local-global, Hilbert-symbol/local-Hasse-invariant, or Witt
local-global proof package. The audited external candidates also cannot be used:
`facebookresearch/atlas-lean@34ffed396f376454c1a9b297f3fd74c5c801fb50` is `Q`-only and its
inspected route has 13 `sorry` tokens; `mariainesdff/HassePrinciple@549601cee72a71f9ffc9c99a3eb7afe522b5b42f`
is `Q`-only, has seven direct `sorry` branches in its root and 33 audited `sorry` tokens, and uses
incompatible pins.

No dependency, frozen registry, typed graph, authoritative cursor, or scheduler state was changed.
The new partial bodies do not change accepted closure. Lifecycle stays `planned`; root debt stays `[H1, M3, R3]`;
`audit_complete=false` and `theorem_complete=false`. The prerequisite obligation-tree item is only
provisional `[_]`, not master-accepted. Because the proof deliverable is incomplete,
`.stage1-worker-selftest.json` is deliberately absent.

## Validation

All commands ran in this worker clone. The automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts was reused read-only. Temporary
Lean files were confined to `/tmp` and removed. No `lake update`, `lake build`, dependency
clone/fetch/checkout, network request, or `.lake` mutation ran.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0423` | 0 | Rank 67; lifecycle `planned`; baseline `L0/rework_required`; theorem incomplete. |
| `python3 -B Stage1_Instances/THM-M-0423/check_anchor_audit.py` | 0 | Four mathlib families, eight probes, and two immutable external candidates agree; exact root open. |
| `python3 -B Stage1_Instances/THM-M-0423/build_obligation_artifacts.py --check` | 0 | 105 obligations and 570 typed edges match deterministic generated bytes; denominator `32a5c78d7f9cf7b59541a9a35c52331cf5055159b93dbe758b3eb6134f7da866`. |
| Isolated `lake env lean --trust=0 -t0` replay described below | 0 | `Statement.lean`, `ObligationTree.lean`, and `Proof.lean` elaborated. The new transport reported `propext` and `Quot.sound`; diagonalization, general algebraically closed classification, and literal complex specialization reported `propext`, `Classical.choice`, and `Quot.sound`; no `sorryAx` occurred. |
| Prohibited-construct scan over owned `*.lean` | 1 expected | No `sorry`, `admit`, `sorryAx`, axiom/bodyless constant, unsafe/opaque declaration, external implementation, `native_decide`, or oracle marker. |
| `rg -n -i --glob '*.lean' '(Hasse.?Minkowski\|Hasse principle\|local.?global.*quadratic\|quadratic.*local.?global\|Hilbert.?symbol\|HasseInvariant\|Witt.*local.?global\|local.?global.*Witt)' Formalizations/Lean/.lake/packages` | 1 expected | On 2026-07-15, no match occurred across all 9,676 installed pinned Lean sources. This is bounded to installed packages; the immutable external-candidate audit remains separate. |
| Environment, pin, status, and frozen-input hash inspection | 0 | Lean `4.29.0` (`98dc76e3...6740`), Lake `5.0.0-src+98dc76e`, mathlib `8a178386...ea95` tree `bdc39a31...c2b`, clean. |

The isolated replay ran from the repository root:

```bash
set -euo pipefail
repo=$PWD
lean_root=$repo/Formalizations/Lean
target=$repo/Stage1_Instances/THM-M-0423
tmp=$(mktemp -d /tmp/thm-m-0423-proof-attempt.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
cp "$target/Statement.lean" "$tmp/Statement.lean"
cp "$target/ObligationTree.lean" "$tmp/ObligationTree.lean"
cp "$target/Proof.lean" "$tmp/Proof.lean"
lean_path=$(cd "$lean_root" && lake env printenv LEAN_PATH)
cd "$lean_root"
LC_ALL=C LANG=C TZ=UTC NO_COLOR=1 LEAN_NUM_THREADS=1 \
  timeout 240 lake env lean --trust=0 -t0 --root="$tmp" \
  "$tmp/Statement.lean" -o "$tmp/Statement.olean"
LC_ALL=C LANG=C TZ=UTC NO_COLOR=1 LEAN_NUM_THREADS=1 \
  LEAN_PATH="$tmp:$lean_path" timeout 240 lake env lean --trust=0 -t0 \
  --root="$tmp" "$tmp/ObligationTree.lean" -o "$tmp/ObligationTree.olean"
LC_ALL=C LANG=C TZ=UTC NO_COLOR=1 LEAN_NUM_THREADS=1 \
  LEAN_PATH="$tmp:$lean_path" timeout 240 lake env lean --trust=0 -t0 \
  --root="$tmp" "$tmp/Proof.lean"
```

The pre-existing modules retain complete standard output SHA-256 values
`4b5061f2c6f01173d7cb6c9b7005ca489aaa1da1f5740e980ea477d37ae04738` for the statement and
`c153357cfd69bc63d7dd6029e2083780babb7b45ec43d9ba0f7afb0e73927168` for the obligation module.
The new proof module's complete standard output SHA-256 is
`4373af4c0021c812a60d7ab63fc3424fee455456a4876bc8f0c178808a5db4bf`; its source SHA-256 is
`32b2fdaf55d05a43679837db4ebc9549ffa7c04e3a74cbc8501f4e3ccc06799a`.
The historical `check_obligation_tree.py` is deliberately not reported as a proof-phase pass: it is
phase-locked to its original obligation-tree worker base and ephemeral worker packet. The fresh
isolated kernel replay above checks the relevant Lean sources at this base without misusing that
old receipt.

## Retry Condition

Resume after exact typed signatures and placeholder-free implementations of the frozen local
classification, Hilbert-symbol/Hasse-invariant, reciprocity, realization, global Witt
uniqueness/injectivity, cancellation, extraction, and transport packages exist in the pinned
closure. An alternative is an immutable, license-reviewed, compatible Lean 4 proof of the exact
arbitrary-number-field target with checked transports and transitive trust provenance. A `Q`-only
proof remains an invalid substitution.

This artifact is durable blocker evidence only. It does not satisfy `S56-M-0423-PROOF`, close an
obligation, accept a receipt, or support validation, release, audit-completion, theorem-completion,
or master-acceptance claims.

## Current rev-5.6 contract refresh

On 2026-07-17 at base `2dc5a410b68eff806858fd6ed0cb33d57f6209f7`, the proof attempt was
replayed against the HEAD phase acceptance contract and v2 dependency context. The complete hard
parent/ancestor inspection order is empty. Both weak shared-module groups were inspected and
recorded as `not_applicable` in `dependency-reuse-ledger.json`; no provider material or acceptance
is consumed.

`check_proof.py` is the sole present contract candidate. It emits exactly one
`stage1-validator-semantic-result/1.0` JSON object and truthfully reports `status=blocked`,
`phase_accepted=false`, and first failed gate `P04-KERNEL.M0423-T-LOCAL-GLOBAL`. It replays
temporary copies of `Statement.lean`, `ObligationTree.lean`, and `Proof.lean` with
`lake env lean --trust=0 -t0`, checks the four partial declarations' exact axiom profiles, and
revalidates the pinned clean mathlib revision/tree without mutating `.lake`.

The current `proof-receipt.json` and worker packet bind the new ledger and validator. This is a
self-tested negative handoff, not proof-phase completion: the exact local-to-global inhabitant,
complete assigned proof predicate, accepted obligation closure, and all downstream gates remain
open.
