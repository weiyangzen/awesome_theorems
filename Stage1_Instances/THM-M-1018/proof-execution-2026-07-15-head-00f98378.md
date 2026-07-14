# THM-M-1018 partial proof execution at `00f98378`

Item: `S56-M-1018-PROOF`

Date: `2026-07-15T05:50:13+08:00`

Base revision: `00f98378e8c1c63097871ae62aeed895d83b0cb4`

Base tree: `4f2396db6d6d1c2b9948f401079f136dd0ed8f16`

## Implemented bodies

`Proof.lean` adds five placeholder-free local bodies. `frontier_Ioc_null` combines the two exact
endpoint hypotheses into nullity of the frontier of the frozen interval. `measureReal_Icc_eq_Ioc`
and `measureReal_Ioo_eq_Ioc` implement both endpoint conversions. `tendsto_Ioc_mass_of_tendsto`
specializes pinned Portmanteau to the exact half-open interval, and `interval_mass_of_weak_limit`
composes that result with `ENNReal.toReal` and the complex embedding.

These bodies are partial proof work supporting `M1018-L-ENDPOINTS` and a conditional weak-limit
route through `M1018-L-INTEGRAL-LIMIT`. They do not construct the sharp Fourier approximants, prove
the Dirichlet sine-integral limit, or inhabit `LevyInversionTarget`. No whole frozen obligation is
claimed closed because the registry still contains planned interfaces rather than matching exact
Lean signatures for these open analytic nodes.

## Validation

All checks reused the automation-provided canonical pinned `.lake` artifacts read-only. No
`lake update`, `lake build`, dependency clone/fetch, network operation, or `.lake` mutation was
performed. Disposable Lean objects were created under `/tmp` only.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and all 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1 through 1546 passed |
| `python3 scripts/stage1_target.py show THM-M-1018` | 0 | rank 494; planned; legacy artifacts unaccepted; theorem incomplete |
| `python3 Stage1_Instances/THM-M-1018/check_obligation_tree.py` | 0 | 17 obligations and 34 typed edges passed; denominator `c5662da4...d6c2`; root open M3 |
| `bash Stage1_Instances/THM-M-1018/check_proof.sh` | 0 | exact statement plus five bodies elaborated at trust zero; each axiom report was `[propext, Classical.choice, Quot.sound]` |
| `python3 -B Stage1_Instances/THM-M-1018/check_proof.py` | 0 | item/DAG identity, hashes, source hygiene, mathlib pin, receipt, open-root boundary, and worker packet agreed |
| prohibited-construct scan over owned `*.lean` | 1 | expected no-match exit for placeholders, declared axioms, unsafe/oracle hooks, and native shortcuts |
| `git diff --check -- Stage1_Instances/THM-M-1018 .stage1-worker-selftest.json` | 0 | no scoped whitespace errors |

The proof source SHA-256 is `2d147de6...e4334`; its successful disposable olean SHA-256 was
`8ab94477...0de8`. The statement source remains `88009a0b...fdd7`. Mathlib remains pinned at
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree `bdc39a31...e242b`.

## Verdict

The partial artifact is self-tested and proposed as worker state `[_]`, pending integration-lane
review. The proof item itself remains incomplete and the accepted item state remains `[ ]`.
Lifecycle remains `planned`; the accepted root vector remains `[H2, M3, R4]`; `audit_complete` and
`theorem_complete` remain false. The remaining root cut is `M1018-T-ANALYTIC`, with first failed
gate `M1018-L-DIRICHLET` because neither the local dossier nor pinned closure supplies the required
sine-integral evaluation and global bound.

Retry requires placeholder-free sharp Dirichlet, finite-Fubini, normalization, position,
unconditional integral-limit, analytic-composition, and canonical-root bodies, or an immutable
compatible exact theorem admitted into the pinned closure. This receipt makes no whole-obligation,
root, validation, release, theorem-completion, receipt-acceptance, or master-acceptance claim.
