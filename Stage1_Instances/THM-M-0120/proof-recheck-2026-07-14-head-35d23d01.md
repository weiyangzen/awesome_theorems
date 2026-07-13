# THM-M-0120 proof-phase recheck at base `35d23d01`

Item: `S56-M-0120-PROOF`  
Intent: `prove`  
Recheck date: 2026-07-14 (Asia/Shanghai)  
Base revision: `35d23d0193cd7c8fccb1d09f22534c6eba066b02`  
Base tree: `4325d20b5ec8db888f28fcedc79cc1b7745c0c68`

## Verdict

`blocked`. No truthful positive proof body exists for the exact frozen target. The existing
placeholder-free declaration

```text
Stage1Instances.THMM0120.Proof.not_moriConeTheoremTarget :
  Not (Stage1Instances.THMM0120.MoriConeTheoremTarget.{0, 0, 0, 0})
```

kernel-checks at trust level zero in the pinned environment. Its countermodel makes every explicit
geometric proposition hypothesis true for a proper identity morphism but leaves the numerical data
independent, as the frozen structure permits: `N1 = Real`, `moriCone = {-1}`,
`canonicalPairing = LinearMap.id`, and `RationalCurve = Empty`. The conclusion's decomposition of
`-1` then gives `z0` with both `z0 = -1` and `0 <= z0`.

This refutes the current formal encoding, not the mathematical Mori cone theorem. Proving a
repaired, narrower, or circularly strengthened proposition would substitute a different target and
is forbidden in this phase. The item remains `[ ]`; no positive proof body, provisional receipt,
audit completion, theorem completion, release, or master acceptance is claimed. The predecessor
registry still reports root `M3` and open substantive packages; this proof attempt exposes an `M5`
exact-target mismatch without editing predecessor state.

This is a repeated hard blocker after more than five proof execution ticks. Splitting the proof
item cannot repair a refutable root, and this worker does not own the generated DAG. The scheduler
should stop recycling this proof node and route the repair to the statement authority.

## Failed Gate And Retry

The first failed gate is exact-target consistency. `S56-M-0120-STATEMENT` must be reopened. Its
unconstrained stand-ins must be replaced by intrinsic definitions or noncircular semantic laws
relating a genuine relative klt pair to its numerical curve space, effective cone, canonical
pairing, rational curves, relative dimension, and contractions. Adding `Conclusion` or any required
output package as an input would be circular.

Positive proof work may resume only after the integration lane accepts a repaired exact statement
fingerprint and new obligation-registry version, followed by a fresh anchor audit.

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
changed_paths: Stage1_Instances/THM-M-0120/proof-recheck-2026-07-14-head-35d23d01.md
accepted_receipt_ids: []
first_failed_gate: exact-target consistency; the frozen canonical proposition is refutable
remaining_root_cut_set: repair and accept the statement; refreeze the registry and typed graphs;
  rerun anchor audit; execute proof against the repaired target
status_boundary: nonrelease blocker evidence only; no proof, receipt, state, or completion claim
```

## Scoped Validation

All checks ran in this worker clone. Lean checks used only the existing canonical pinned Lake
closure; no update, build, clone, fetch, or dependency mutation was performed. The
automation-provided untracked `Formalizations/Lean/.lake` symlink makes this dirty, nonrelease
evidence.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0120` | 0 | rank 39; planned; L0/rework-required; legacy artifacts unaccepted; theorem incomplete |
| `python3 Stage1_Instances/THM-M-0120/check_statement.py` | 0 | three structural mutations killed; expression SHA-256 `074d45c3...cfd`; pinned toolchain and mathlib revision matched |
| `python3 Stage1_Instances/THM-M-0120/check_anchor_audit.py` | 0 | immutable local candidates, clean pinned mathlib, eight Lean probes, and `M3` boundary agreed |
| `python3 Stage1_Instances/THM-M-0120/check_obligation_tree.py` | 0 | 25 obligations and 62 typed edges passed; denominator `69152b16...81b1`; root remains `M3` |
| isolated `lake env lean --trust=0 -t0` recipe below | 0 | exact statement and countermodel elaborated; axiom report `[propext, Classical.choice, Quot.sound]` |
| `~/.elan/toolchains/leanprover--lean4---v4.29.0/bin/lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release |
| `git -C .lake/packages/mathlib rev-parse HEAD` from `Formalizations/Lean` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `test -z "$(git -C .lake/packages/mathlib status --porcelain)"` from `Formalizations/Lean` | 0 | pinned mathlib worktree clean |
| `rg -n --pcre2 '\b(?:sorry|admit|axiom)\b|sorryAx|unsafe' Stage1_Instances/THM-M-0120 -g '*.lean'` | 1 | no forbidden placeholder, axiom-declaration, or unsafe tokens; exit 1 is ripgrep's no-match result |
| `git diff --check -- Stage1_Instances/THM-M-0120` | 0 | no whitespace errors in the owned-path delta |
| `test ! -e .stage1-worker-selftest.json` | 0 | completion self-test manifest deliberately absent |

Exact Lean recipe, run from `Formalizations/Lean`:

```bash
tmp=$(mktemp -d ./.m0120-proof.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
cp ../../Stage1_Instances/THM-M-0120/Statement.lean "$tmp/Statement.lean"
cp ../../Stage1_Instances/THM-M-0120/Proof.lean "$tmp/Proof.lean"
base=$(lake env printenv LEAN_PATH)
LEAN_NUM_THREADS=1 lake env lean --trust=0 -t0 \
  -o "$tmp/Statement.olean" "$tmp/Statement.lean"
LEAN_PATH="$tmp:$base" LEAN_NUM_THREADS=1 \
  lake env lean --trust=0 -t0 "$tmp/Proof.lean"
```

Relevant output:

```text
'Stage1Instances.THMM0120.Proof.not_moriConeTheoremTarget' depends on axioms:
[propext, Classical.choice, Quot.sound]
```

Input SHA-256 values are statement
`69eabc83cd8b7fe8fa34d598c9de890eea09d8ee8357d551abf3e7727444fd6b`, proof witness
`e5c342e97885f6a533fada4b928685ea4c2e888baa5e21699a454049f02f29ab`, obligation registry
`cd24f57d66422f500f17b348bed362dddcdf032447861f2560518f95c1a48a2d`, typed graphs
`9ca86f175b3413edd03fec0971bb165c9dd0396ade874a0b0c0c674ac861e23f`, and anchor audit
`71ff1889e55e0f4387697db69ff7acae110f0530f94879ef68ae06370475090d`.

No `.stage1-worker-selftest.json` is written because the assigned positive proof deliverable is
blocked rather than genuinely self-tested as complete.
