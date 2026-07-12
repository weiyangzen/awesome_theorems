# Statement validation record

Item: `S56-M-1138-STATEMENT`  
Base revision: `a62cb8be3635fb1e66233c8704af547c6bc9abac`

## Frozen target

`Stage1Instances.THM_M_1138.HarmonicWeakMaximumPrinciple` is the exact weak boundary-maximum
claim selected by intake. It quantifies over positive-dimensional finite Euclidean spaces and
nonempty, open, connected, bounded domains. Mathlib's `HarmonicContOnCl` packages harmonicity on
the domain and continuity on its closure. The conclusion supplies an actual point on `frontier U`
whose value dominates all values on `closure U`.

The positive-dimension premise resolves the intake's dimension-zero boundary question: the unique
nonempty open domain in zero-dimensional Euclidean space has empty frontier, so the existential
conclusion would fail even for a constant function. Connectedness remains explicit because it was
part of the intake claim; this phase does not weaken the root merely because the weak principle may
admit a more general formulation.

## Commands and results

All commands ran inside this worker clone. Lean commands used the existing pinned Lake closure; no
dependency update, build, clone, or fetch was performed.

| Command | Exit | Result |
|---|---:|---|
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1138/Statement.lean` | 0 | canonical target and five mutations elaborated; explicit canonical expression printed |
| `python3 Stage1_Instances/THM-M-1138/check_statement.py` | 0 | expression SHA-256 `7ae115564e67b7065344d9b323240a2694c3f1f1f01640d1b542dcc2152f4f5c`; all five mutations distinguished; source SHA-256 `a6a2c5d7cc38249b3d96a3f8037a68175db5d62eecec2790865086dce2747c5a` |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1138` | 0 | rank 343, planned, L0/rework-required, historical status untrusted, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-1138/statement.json >/dev/null` | 0 | structured statement receipt parses |
| scoped prohibited-token scan of `Statement.lean`, `statement.json`, and `check_statement.py` | 1 | no match; exit 1 is the clean no-match result |
| `git diff --check -- Stage1_Instances/THM-M-1138 .stage1-worker-selftest.json` | 0 | no whitespace errors |

This evidence validates statement elaboration only. It supplies no maximum-principle proof, source
acceptance, anchor audit, obligation closure, theorem completion, or master acceptance.
