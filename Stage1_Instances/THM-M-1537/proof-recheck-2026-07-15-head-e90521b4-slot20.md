# THM-M-1537 proof-phase recheck at e90521b4 (slot20)

Item: `S56-M-1537-PROOF`

Intent: `prove`

Base revision: `e90521b4b150b98d81c4dca2462ad36b64d4673e`

Base tree: `f12951f481d2b51f33d6d300dc2874b3c49ed0e0`

Recheck time: `2026-07-15T13:41:37+08:00` (Asia/Shanghai)

## Verdict

`blocked`. No legal positive proof body exists for the exact frozen target. The
`SemiclassicalBlackHole` record stores `thermodynamicEntropy` independently of its area, physical
constants, and regime propositions. The frozen premises therefore cannot imply the requested
universal equality.

The existing placeholder-free declaration

```text
Stage1Instances.THM_M_1537.not_bekensteinHawkingAreaLaw :
  Not Stage1Instances.THM_M_1537.BekensteinHawkingAreaLaw
```

kernel-checks at trust level zero. Its witness has horizon area zero, entropy one, all four
constants one, and all three regime propositions true. Every premise holds, while
`entropyFromArea` reduces to zero, so the target would require `1 = 0`.

This refutes the frozen formal encoding, not the physical Bekenstein-Hawking law. The checked local
declaration `areaLaw_of_bridge` consumes `AreaLawBridge`, which is definitionally the same universal
equality as the root. The historical `S1_M_200` model stores or consumes an area-law predicate, and
its wrappers prove consequences of that predicate. Neither route derives the exact unconstrained
target. The bounded pinned-mathlib search found no terminal proof of this area law.

No proof source, axiom, placeholder, unsafe declaration, weakened statement, substituted theorem,
or unpinned dependency was added. The frozen upstream vector remains `[H2, M5, R3]`; this proof-only
worker does not mutate it. The checked refutation warrants `H5` for the exact formal proposition
under rev-5.6 section 3.1, but an authorized statement phase must reconcile that classification with
the distinct physical claim.

## Failed Gate

The first failed gate is `M1537-B-PHYSICS` / exact-target consistency. Positive proof work can
resume only after an authorized, source-faithful statement/model repair gives the physical regime
substantive entropy-area semantics, followed by accepted replacement statement and obligation-
registry versions and renewed statement, anchor-audit, and obligation-tree gates.

The prerequisite `S56-M-1537-OBLIGATION_TREE` is only worker-provisional `[_]`, not master-accepted
`[x]`. The proof item remains `[ ]`. No audit-completion, theorem-completion, validation, release,
receipt-acceptance, scheduler-transition, or master-acceptance claim is made. Because the assigned
positive proof phase is not genuinely self-tested as complete, `.stage1-worker-selftest.json` is
deliberately absent.

## Validation

The automation-provided untracked `Formalizations/Lean/.lake` symlink was the sole pre-existing
worktree entry. The canonical pinned mathlib checkout is clean at
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. The declared `flt-regular` package artifact is missing
its pinned checkout, and the fresh `lake env` invocation failed while resolving it with
`external command 'git' exited with code 128`. No explicit dependency-management command was
invoked by this worker. The shared canonical dependency artifact showed concurrent fetch activity,
but it cannot be attributed to this validation and is not credited as evidence; this proof does not
import `flt-regular`.

Following the fail-closed missing-artifact rule, the target was also checked narrowly with the
pinned Lean 4.29.0 binary and the already present Lake build-library paths. That direct replay is
real kernel evidence for these two files, but it is not represented as a successful `lake env lean`
recipe or release-grade dependency replay.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-1537` | 0 | Rank 200; lifecycle `planned`; baseline `L0/rework_required`; legacy artifacts unaccepted; theorem incomplete. |
| `git status --short` before edits | 0 | Only `?? Formalizations/Lean/.lake` was present. |
| `python3 Stage1_Instances/THM-M-1537/check_statement.py` | 1 | Lake failed while resolving the missing pinned dependency and ended with `error: external command 'git' exited with code 128`; no statement-validator pass is claimed. |
| direct statement-fingerprint equivalent using pinned `lean` and existing build-library paths | 0 | Canonical expression SHA-256 `0294eb7c...7cc8`; all four structural mutations had distinct hashes. |
| `python3 Stage1_Instances/THM-M-1537/check_anchor_audit.py` | 0 | `ok: exact statement, 6 pinned mathlib probes, partial Physlib candidate, and M4 boundary agree` |
| `python3 Stage1_Instances/THM-M-1537/check_obligation_tree.py` | 0 | Nine obligations and 16 typed edges passed; denominator `8c57fc2c...c19`; root remains refuted at `M5`. |
| isolated direct pinned-`lean --trust=0 -t0` recipe described below | 0 | Both Lean invocations exited 0. The exact statement, conditional composition, and countermodel refutation elaborated. Both printed declarations report exactly `[propext, Classical.choice, Quot.sound]`. Statement olean SHA-256: `21763c76...c4224`; statement output: `ff89d33c...61fb`; obligation output: `a3249e7c...e802b`. |
| bounded exact-target/local-library search | 0 | Found the frozen dossier and historical conclusion-carrying wrappers, but no exact root proof in the pinned closure. |
| `rg -n --pcre2 '\\b(?:sorry|admit|axiom)\\b|sorryAx|unsafe|implemented_by|native_decide' Stage1_Instances/THM-M-1537/Statement.lean Stage1_Instances/THM-M-1537/ObligationTree.lean` | 1 | Expected no-match result: no prohibited construct in the checked Lean sources. |
| pinned Lean binary `--version` | 0 | Lean `4.29.0`, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release. |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | Empty output; the pinned mathlib checkout was clean after validation. |

The narrow kernel replay copied `Statement.lean` and `ObligationTree.lean` to a temporary directory,
constructed `LEAN_PATH` only from already present `.lake/*/build/lib/lean` directories plus the
pinned toolchain library, and invoked:

```bash
LEAN_NUM_THREADS=1 LEAN_PATH="$PINNED_BUILD_PATH" timeout --foreground 300 \
  /home/sansha-2/.elan/toolchains/leanprover--lean4---v4.29.0/bin/lean \
  --trust=0 -t0 --root="$TMP" -o "$TMP/Statement.olean" "$TMP/Statement.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$TMP:$PINNED_BUILD_PATH" timeout --foreground 300 \
  /home/sansha-2/.elan/toolchains/leanprover--lean4---v4.29.0/bin/lean \
  --trust=0 -t0 --root="$TMP" "$TMP/ObligationTree.lean"
```

Pinned environment: Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`; mathlib
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. Exact source hashes, command
results, failed gate, retry condition, changed paths, and the missing Lake artifact limitation are
recorded in the adjacent JSON artifact.

This is current-HEAD, target-specific negative kernel evidence. It is not a proof receipt and does
not satisfy `S56-M-1537-PROOF`.
