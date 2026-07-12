# Exact-statement gate: blocked

Item: `S56-M-0499-STATEMENT`  
Theorem: `THM-M-0499`  
Base revision: `3f994388953e417edafd54b069ab45d648619698`

## Decision

The exact Lean 4 target cannot be truthfully selected and elaborated from the
authoritative material currently available. The repository gives only
`pi(x)-Li(x)=O(xe^(-c sqrt(ln x)))`; Stage 0 explicitly records the exact
definitions and hypotheses as pending, and the accepted intake dependency
freezes only the theorem family.

The missing choices change the proposition. No inspected, immutable source
passage fixes whether the asymptotic variable is real or natural, how
`Nat.primeCounting` is extended to reals, which additive normalization and
singularity convention define `Li`, whether `c` is existential and strictly
positive, or whether the source claim is an `IsBigO` statement rather than an
explicit constants-and-threshold estimate. Choosing familiar conventions here
would invent missing mathematics. Defining `Li` as an opaque parameter would
broaden the claim, while assuming its desired behavior would hide the theorem
inside a hypothesis; neither is an exact formalization.

Consequently this phase cannot freeze ordered binders, a canonical expression,
an expression hash, minimal imports, checked alternate-encoding transports, or
meaningful hypothesis/domain/boundary mutation tests. The first failed gate is
exact source-statement identity, before Lean target elaboration.

## Pinned Lean boundary

The pinned environment exposes `Nat.primeCounting`, `Real.log`, `Real.sqrt`,
`Real.exp`, `Filter.atTop`, and `Asymptotics.IsBigO`. A scoped search of the
pinned Mathlib source found no named logarithmic-integral definition.
`IntakeProbe.lean`, using `Mathlib.NumberTheory.Chebyshev`, re-elaborates the
available ingredients. It deliberately declares no error-term theorem and
receives no exact-statement credit. Since the proposition is unresolved, its
import is only a substrate probe and cannot be certified as the target's
minimal import.

The reused environment is Lean `4.29.0` (commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`) with mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. The `lean-toolchain` and
`lake-manifest.json` SHA-256 values are respectively
`651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2` and
`321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.
No update, build, clone, fetch, or dependency mutation was performed.

## Validation evidence

Commands ran from this worker clone on 2026-07-12 (Asia/Shanghai).

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0499` | 0 | rank 876; planned; legacy artifacts unaccepted; theorem incomplete |
| `rg -n -C 8 '素数定理的误差项\|pi\\(x\\)-Li' Docs/researches/math_theorems.md Docs/Stage0_Blueprint.md` | 0 | repository formula located; Stage 0 says exact definitions and hypotheses are pending |
| scoped `rg` search for a logarithmic-integral API in pinned Mathlib | 1 | no named logarithmic-integral definition found; this is bounded discovery evidence only |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | pinned revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean `4.29.0`, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0499/IntakeProbe.lean)` | 0 | all six statement-building APIs elaborated and printed their types |
| `python3 -m json.tool Stage1_Instances/THM-M-0499/statement-blocker.json >/dev/null` | 0 | structured blocker is valid JSON |
| scoped forbidden-term scan under `Stage1_Instances/THM-M-0499` | 1 | no proof-gap declaration found; 1 is ripgrep's no-match exit |
| `git diff --check -- Stage1_Instances/THM-M-0499` | 0 | no whitespace errors |

## Gate result

Machine status remains `M4`. There is no statement acceptance, proof credit,
audit completion, or theorem completion. Retry requires a hashed primary-source
passage with an exact locator and independent review, followed by a
source-faithful `Li` definition and domain/endpoint choices.

Because the assigned statement phase is not complete, no
`.stage1-worker-selftest.json` is emitted.
