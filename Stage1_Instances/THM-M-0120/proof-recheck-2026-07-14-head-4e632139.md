# THM-M-0120 proof-phase recheck at base `4e632139`

Item: `S56-M-0120-PROOF`  
Intent: `prove`  
Recheck date: 2026-07-14 (Asia/Shanghai)  
Base revision: `4e632139f5060edf088cd107551caac63981263b`  
Base tree: `7a87a6b3f6b71cfb0b2d98872327edc8fe8620e6`

## Verdict

`blocked`. The exact frozen Lean proposition cannot receive the requested positive proof body. The
existing placeholder-free declaration

```text
Stage1Instances.THMM0120.Proof.not_moriConeTheoremTarget :
  Not (Stage1Instances.THMM0120.MoriConeTheoremTarget.{0, 0, 0, 0})
```

kernel-checks against the pinned dependency closure. Its countermodel uses a proper identity
morphism over `AlgebraicClosure Rat` and makes all six explicit geometric proposition hypotheses
true. This is permitted because the statement does not connect those hypotheses to its arbitrary
numerical data. The countermodel takes `N1 = Real`, `moriCone = {-1}`,
`canonicalPairing = LinearMap.id`, and `RationalCurve = Empty`. Applying the required decomposition
to `-1` yields an element `z0` with both `z0 = -1` and `0 <= z0`, a contradiction.

This refutes the current formal encoding, not the mathematical Mori cone theorem. A repaired,
narrower, or circularly strengthened proposition cannot be substituted during this proof phase.
The item remains `[ ]`; no positive proof body, accepted receipt, audit completion, theorem
completion, release, or master acceptance is claimed. The frozen predecessor graph remains at root
`M3` with the substantive geometric packages open; this proof attempt exposes an `M5` exact-target
mismatch but does not rewrite or accept predecessor state.

## First Failed Gate And Retry

The first failed gate is exact-target consistency. `S56-M-0120-STATEMENT` must be reopened. Its
unconstrained stand-ins must be replaced by intrinsic definitions or noncircular semantic laws
relating a genuine relative klt pair to its numerical curve space, effective cone, canonical
pairing, rational curves, dimension, and contractions. Adding `Conclusion`, its decomposition
branch, or another required output as an input hypothesis would be circular.

Positive proof execution may resume only after the integration lane accepts a repaired exact
statement fingerprint and a new obligation-registry version, followed by a fresh anchor audit.

## Structured Handoff

```text
theorem_id: THM-M-0120
intent: prove
verdict: blocked
lifecycle: planned -> planned
task_id: S56-M-0120-PROOF
covered_obligation: M0120-ROOT (countermodel only; no closure or state change)
root_vector: [H2, M3, R4] -> [H2, M3, R4] (authoritative state unchanged)
proof_attempt_classification: M5 exact-target mismatch, pending master reconciliation
audit_complete: false
theorem_complete: false
changed_paths: Stage1_Instances/THM-M-0120/proof-recheck-2026-07-14-head-4e632139.md
accepted_receipt_ids: []
first_failed_gate: exact-target consistency; the frozen canonical proposition is refutable
status_boundary: nonrelease blocker evidence only; no proof, receipt, state, or completion claim
```

## Scoped Validation

All commands ran in this worker clone. Lean checks used only the existing pinned Lake closure; no
`lake update`, `lake build`, clone, fetch, or dependency mutation was performed. The
automation-provided untracked `Formalizations/Lean/.lake` symlink makes this warm-cache evidence
dirty and nonrelease.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0120` | 0 | rank 39; lifecycle planned; L0/rework-required; legacy artifacts unaccepted; theorem incomplete |
| `python3 Stage1_Instances/THM-M-0120/check_statement.py` | 0 | all three structural mutations killed; expression hash `074d45c3...cfd`; pinned toolchain and mathlib revision matched |
| `python3 Stage1_Instances/THM-M-0120/check_anchor_audit.py` | 0 | immutable local candidates, clean pinned mathlib, eight Lean probes, and the `M3` boundary agreed |
| `python3 Stage1_Instances/THM-M-0120/check_obligation_tree.py` | 0 | 25 obligations and 62 typed edges passed; denominator `69152b16...81b1`; root remains `M3`; substantive packages remain open |
| isolated `lake env lean --trust=0 -t0` recipe below | 0 | exact statement elaborated; countermodel checked; axiom report was `[propext, Classical.choice, Quot.sound]` |
| `lake env lean --version` from `Formalizations/Lean` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release |
| `git -C .lake/packages/mathlib rev-parse HEAD` from `Formalizations/Lean` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `test -z "$(git -C .lake/packages/mathlib status --porcelain)"` from `Formalizations/Lean` | 0 | pinned mathlib worktree clean |
| placeholder scan below, from `Formalizations/Lean` | 1 | no matches; exit 1 is ripgrep's no-match result |

Exact Lean recipe, run from `Formalizations/Lean`:

```bash
tmp=$(mktemp -d ./.m0120-proof.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
cp ../../Stage1_Instances/THM-M-0120/Statement.lean "$tmp/Statement.lean"
cp ../../Stage1_Instances/THM-M-0120/Proof.lean "$tmp/Proof.lean"
lake env lean --trust=0 -t0 -o "$tmp/Statement.olean" "$tmp/Statement.lean" &&
  LEAN_PATH="$tmp:$(lake env printenv LEAN_PATH)" \
    lake env lean --trust=0 -t0 "$tmp/Proof.lean"
```

Relevant output:

```text
'Stage1Instances.THMM0120.Proof.not_moriConeTheoremTarget' depends on axioms:
[propext, Classical.choice, Quot.sound]
```

Exact placeholder scan:

```bash
rg -n --pcre2 '\b(?:sorry|admit|axiom)\b|sorryAx|unsafe' \
  ../../Stage1_Instances/THM-M-0120/Proof.lean
```

Content inputs at this base are unchanged: statement SHA-256
`69eabc83cd8b7fe8fa34d598c9de890eea09d8ee8357d551abf3e7727444fd6b`, proof witness
`e5c342e97885f6a533fada4b928685ea4c2e888baa5e21699a454049f02f29ab`, obligation registry
`cd24f57d66422f500f17b348bed362dddcdf032447861f2560518f95c1a48a2d`, typed graphs
`9ca86f175b3413edd03fec0971bb165c9dd0396ade874a0b0c0c674ac861e23f`, and anchor audit
`71ff1889e55e0f4387697db69ff7acae110f0530f94879ef68ae06370475090d`.

Remaining root cut set: repair and accept the statement, refreeze the registry and typed graphs,
rerun the anchor audit, then execute the proof.

No `.stage1-worker-selftest.json` is written because the assigned positive proof deliverable is
blocked rather than genuinely self-tested as complete.
