# THM-M-0120 proof-phase blocker

Item: `S56-M-0120-PROOF`  
Base revision: `bb6fb28ac1c55ecb52f3f1c84e7fbb35c26b47ad`  
Validation date: 2026-07-14 (Asia/Shanghai)

## Verdict

`blocked`: the exact frozen Lean target is false, so no placeholder-free positive proof body can
truthfully inhabit it. The assigned item remains `[ ]`; no proof, audit-completion,
theorem-completion, release, or master-acceptance claim is made.

The existing local declaration
`Stage1Instances.THMM0120.Proof.not_moriConeTheoremTarget` kernel-checks

```text
Not (Stage1Instances.THMM0120.MoriConeTheoremTarget.{0, 0, 0, 0})
```

Its countermodel uses an identity proper morphism over `AlgebraicClosure Rat` and makes all six
explicit geometric proposition hypotheses true. This is permitted because `ConeTheoremData` does
not connect those propositions to its arbitrary numerical data. The countermodel chooses
`N1 = Real`, `moriCone = {-1}`, `canonicalPairing = LinearMap.id`, and an empty rational-curve
carrier. Applying the conclusion's decomposition equivalence to `-1` produces
`z0 in NonnegativePart` with `z0 in {-1}`. Hence `z0 = -1`, while membership in the nonnegative
part also gives `0 <= z0`, contradicting `not (0 <= (-1 : Real))`.

This refutes only the current overbroad formal encoding. It does not refute the mathematical Mori
cone theorem. Under rev-5.6, a proof of a repaired or narrower theorem cannot be substituted for the
frozen target during this proof phase.

The frozen predecessor graph still records the root at `M3` and its substantive packages at `M4`.
The checked statement mismatch establishes `M5` for this proof attempt under rev-5.6 section 3.2.
This worker does not rewrite or accept predecessor state; the integration lane must reconcile that
classification when the statement is reopened.

## First Failed Gate

The first failed gate is exact-target consistency. The statement gate must be reopened. A valid
repair must replace the unconstrained stand-ins with intrinsic definitions or noncircular laws that
connect the projective klt pair to its actual numerical curve space, effective cone, canonical
pairing, rational curves, and contractions. Adding `Conclusion`, its decomposition branch, or any
other required output as an input hypothesis would be circular and is not a valid repair.

After repair, the integration lane must freeze and accept a new statement fingerprint and
obligation-registry version, then rerun the anchor audit and proof phase. Until then, the positive
root has no legal proof body.

## Scoped Validation

All checks ran in this worker clone against the existing pinned Lake closure. No update, build,
clone, fetch, or dependency mutation was performed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0120` | 0 | rank 39; planned; L0/rework-required; theorem incomplete |
| isolated `lake env lean -t0` recipe below | 0 | exact statement elaborated; countermodel theorem checked at trust level zero; axiom report was `[propext, Classical.choice, Quot.sound]` |
| `lake env lean --version` from `Formalizations/Lean` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release |
| `git -C .lake/packages/mathlib rev-parse HEAD` from `Formalizations/Lean` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `rg -n --pcre2 '\b(?:sorry|admit|axiom)\b|sorryAx|unsafe' ../../Stage1_Instances/THM-M-0120/Proof.lean` from `Formalizations/Lean` | 1 | no matches; exit 1 is ripgrep's no-match result |
| `test ! -e .stage1-worker-selftest.json` from the repository root | 0 | no completion self-test manifest exists |

Exact Lean recipe, run from `Formalizations/Lean`:

```bash
tmp=$(mktemp -d ./.m0120-proof.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
cp ../../Stage1_Instances/THM-M-0120/Statement.lean \
  ../../Stage1_Instances/THM-M-0120/Proof.lean "$tmp/"
lake env lean -t0 -o "$tmp/Statement.olean" "$tmp/Statement.lean" &&
  LEAN_PATH="$tmp:$(lake env printenv LEAN_PATH)" \
    lake env lean -t0 "$tmp/Proof.lean"
```

The proof source SHA-256 is
`e5c342e97885f6a533fada4b928685ea4c2e888baa5e21699a454049f02f29ab`. The pre-existing
untracked `Formalizations/Lean/.lake` symlink is automation-provided and makes this nonrelease
evidence. Because the assigned positive proof deliverable is blocked rather than self-tested as
complete, `.stage1-worker-selftest.json` is deliberately absent.
