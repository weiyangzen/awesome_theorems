# Exact-statement gate: blocked

Item: `S56-M-1254-STATEMENT`  
Base revision: `a80ab2514294b0e85527fd5a7d419748401215b2`  
Assessment date: 2026-07-12

## Gate result

The exact Lean 4 target cannot be elaborated from the repository evidence without inventing or
substituting mathematics. The only target-specific statement is the phrase `微分算子的基本解`
("fundamental solution of a differential operator"). It supplies neither a proposition nor the
data needed to determine one.

In particular, the record does not select:

- a differential operator or a quantified class of operators;
- a domain, dimension, scalar field, coefficient class, or boundary convention;
- a function, distribution, or tempered-distribution solution space;
- the meaning and normalization of the Dirac delta;
- definition, existence, uniqueness, or explicit-formula as the claim kind.

The adjacent source record separately assigns existence of fundamental solutions for
constant-coefficient PDEs to the Malgrange-Ehrenpreis theorem. That is `THM-M-1255`, so adopting it
here would broaden the supplied phrase and duplicate another target. Specializing to the Laplace,
heat, or wave operator would likewise substitute an unselected theorem.

Consequently there is no canonical Lean expression, minimal import set, elaborated-expression hash,
or environment fingerprint to record. The statement gate remains `M4`; no theorem, proof, kernel
closure, or completion is claimed. No `.stage1-worker-selftest.json` is emitted because the assigned
elaboration phase is not self-tested successfully.

## Reproducible checks

All commands were run from the repository root in this worker clone.

| Command | Exit | Exact result relevant to this gate |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-1254` | 0 | Rank 433; lifecycle `planned`; `theorem_complete: false` |
| `sed -n '9168,9183p' Docs/researches/math_theorems.md` | 0 | THM-M-1254 has only `陈述: 微分算子的基本解`; the next record separately states constant-coefficient PDE existence |
| `sed -n '34126,34149p' Docs/Stage0_Blueprint.md` | 0 | Exact definitions, premises, proof path, dependencies, formal system, and logical foundation are all `待补充` or `待选` |
| `git status --short` | 0 | Pre-existing untracked `Formalizations/Lean/.lake`; no target statement or target Lean module exists there |

Running `lake env lean` against a fabricated proposition would only prove that the fabrication
elaborates, not that the repository's exact target elaborates. It is therefore not a valid narrow
validation command for this blocked gate and was not run.

## Unblock condition

A source-owner decision or a primary-source pinpoint must provide a truth-valued claim and fix all
domains, ordered binders, hypotheses, conclusion, equality sense, and degenerate cases. The record
must also distinguish the result from `THM-M-1255` and other specialized fundamental-solution
targets. Only then can this phase encode the claim and determine its genuinely minimal pinned
imports.
