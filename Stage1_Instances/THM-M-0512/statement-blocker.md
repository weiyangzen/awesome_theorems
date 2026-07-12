# Statement-phase blocker

Item: `S56-M-0512-STATEMENT`  
Theorem: `THM-M-0512`  
Worker base revision: `e9d545372b66f73be63271b2fb408ef134d1d6f7`

## Gate decision

The exact Selberg trace formula cannot be truthfully frozen or elaborated from the repository
source record. The entire supplied mathematical claim is `自守形式的迹公式` ("trace formula for
automorphic forms"), together with the name, attribution to Atle Selberg, and year 1956. No
publication, edition, theorem or formula number, page, displayed identity, or assumptions are
identified. Stage0 expressly leaves the precise definitions and premises open, while the rev-5.6
manifest treats `已验证` only as untrusted source metadata.

This record is compatible with inequivalent compact and cofinite noncompact formulas, as well as
classical upper-half-plane and representation-theoretic formulations. Those choices change the
group and lattice, quotient, automorphic-function space, admissible test functions, trace or
regularization, spectral terms, conjugacy or orbital terms, measures, transforms, and convergence
hypotheses. Selecting any one version without a pinpointed source passage would substitute an
invented theorem for `THM-M-0512`.

Consequently there is no source-faithful canonical mathematical statement, ordered binder list,
Lean declaration or expression, minimal import set, or normalized expression fingerprint to
record. There is likewise no legitimate removed-hypothesis, changed-domain, changed-binder-scope,
or boundary-case mutation suite. The first failed gate is the Stage1 rev-5.6 section 5 exact
statement freeze; section 5.1 elaboration cannot begin. No proof evidence was inspected or
credited.

The existing `IntakeProbe.lean` was re-elaborated only to confirm that the pinned environment and
several nearby APIs are available. `ModularForm`, `CuspForm`, finite-dimensional
`LinearMap.trace`, and Haar measure do not define a Selberg trace formula and receive no statement
credit.

## Exact validation record

Validation date: `2026-07-12` (`Asia/Shanghai`). All commands ran in this worker clone. The
pre-existing canonical `.lake` link and artifacts were used read-only; no update, build, fetch, or
clone was run.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0512` | 0 | rank 886; planned; legacy artifacts unaccepted; source status untrusted; theorem incomplete |
| `rg -n -C 5 '塞尔伯格迹公式\|Selberg trace formula\|自守形式的迹公式' Docs/researches/math_theorems.md Docs/Stage0_Blueprint.md Docs/Stage1_Blueprint_Applicable_Theorems.md` | 0 | found only the short metadata/gloss, open Stage0 fields, and generated manifest projection; no exact formula |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0512/IntakeProbe.lean)` | 0 | five nearby pinned APIs elaborated under Lean 4.29.0; no canonical target asserted |
| `rg -n '\\b(sorry\|admit)\\b\|^[[:space:]]*axiom\\b' Stage1_Instances/THM-M-0512 -g '*.lean'` | 1 | expected no-match exit; no prohibited placeholder or axiom in target Lean source |
| `python3 -m json.tool Stage1_Instances/THM-M-0512/instance.json` | 0 | intake instance is valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-0512/task-dag.json` | 0 | open task DAG is valid JSON |

## Required unblocker and status boundary

Provide an immutable primary-source edition and pinpoint one exact formula by theorem/formula and
page. An independent source inspection must freeze all domains, binders, hypotheses, spectral and
geometric terms, normalizations, convergence conditions, and boundary cases. Only then can this
phase select minimal pinned imports, elaborate and serialize the exact expression, check any
alternate encodings, and run the four mandatory mutation classes.

The lifecycle remains `planned`; the root remains `[H1, M4, R4]`, with `audit_complete=false` and
`theorem_complete=false`. This statement node remains blocked and is not self-tested. No
`.stage1-worker-selftest.json` is emitted.
