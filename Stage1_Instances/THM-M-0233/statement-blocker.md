# THM-M-0233 rev-5.6 statement blocker

## Decision

`S56-M-0233-STATEMENT` remains `[ ]`. Its prerequisite `S56-M-0233-INTAKE` is
provisional worker state `[_]`, not master-accepted state `[x]`; the intake receipt has
`accepted: false`, is not content-addressed, and has no accepted receipt ID. Rev-5.6 section 10.2
allows preparation of this later-node blocker, but an accepted transition remains dependency
ordered.

Independently and decisively, the exact-source-statement gate fails. The repository record gives
only the title `辐角原理`, the Augustin Cauchy attribution, the year 1831, and the gloss
`全纯函数零点与极点个数公式`: a formula for the numbers of zeros and poles of a holomorphic
function. It provides no source edition, theorem locator, formula, incorporated definition,
ordered binder, hypothesis, exact conclusion, proof boundary, correction history, or reviewer.
Taken literally, its reference to a holomorphic function conflicts with its reference to poles
unless an unstated meromorphic or analytic-except-poles convention is supplied. The catalog label
`已验证` is untrusted metadata under rev-5.6 and supplies no source or kernel credit.

NIST DLMF version 1.2.7, section 1.10(iv), equation 1.10.9 is a strong inspected source lead. For
its inherited simple closed contour traversed positively, it assumes the singularities inside the
contour are poles and that `f` is analytic and nonvanishing on the contour, and gives

```text
N - P = (1 / (2*pi*i)) * integral_C (f'(z) / f(z)) dz
      = (1 / (2*pi)) * Delta_C phase(f(z)),
```

with zeros and poles counted with multiplicity. It is not the catalog's cited source, its inherited
contour, interior, analyticity, and integration definitions have not been transcribed into an
accepted immutable crosswalk, and no independent source review is recorded. The intake therefore
classifies it as an `H1` lead, not an approved canonical proposition.

Materially different Lean roots fit the catalog gloss: a signed divisor sum for a general cycle, a
positively oriented simple-contour theorem, a circle specialization, a holomorphic zero-only
specialization, the logarithmic-derivative equality alone, the phase-change equality alone, or both
equalities. Choosing one would invent, narrow, broaden, or substitute proposition-changing
mathematics. The repository does not fix:

- the contour or cycle representation, regularity, orientation, traversal count, and interior;
- the ambient domain and whether the point at infinity is in scope;
- meromorphicity versus analytic-except-poles, the pole set, finiteness, and multiplicities;
- boundary nonvanishing and pole exclusions, including how boundary singularities are handled;
- the sign, `2*pi*i` normalization, ordered binders, and exact conclusion clauses; or
- the zero function, constants, empty counts, reversed or repeated traversal, self-intersection,
  degenerate contours, accumulating singularities, and other boundary cases.

Section 5 of the blueprint makes statement ambiguity and a missing expression fingerprint hard
blockers. There is no canonical expression whose imports can honestly be certified minimal, no
credited alternate encoding for a checked transport, and no canonical target against which the
required removed-hypothesis, changed-domain, changed-binder-scope, and boundary mutations can run.
Those mutations are undefined, not passed. No `Statement.lean`, theorem declaration, proof body,
weakened special case, or broadened interface was added. The root remains `[H1, M4, R4]`.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` was re-elaborated with its three direct imports:

- `Mathlib.Analysis.Complex.CauchyIntegral`
- `Mathlib.Analysis.Complex.JensenFormula`
- `Mathlib.Analysis.SpecialFunctions.Complex.LogDeriv`

It checks eight adjacent meromorphic-order, divisor, logarithmic-derivative, circle-integral, and
Jensen-formula interfaces. All checks pass, but the probe deliberately declares no argument
principle, canonical target, transport, or proof body. Its imports are discovery-only and cannot be
certified minimal for an absent target. A bounded exact-topic search over repo-local Lean and
pinned mathlib found no named argument-principle, phase-principle, or corresponding
logarithmic-derivative bridge under the recorded terms. This is narrow feasibility evidence, not
the downstream anchor audit and not a global absence claim.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided canonical `.lake` symlink was
used read-only. No `lake update`, `lake build`, dependency clone or fetch, or other `.lake` mutation
was run.

## Validation Record

Commands ran from the isolated worker clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0233` | 0 | rank 1245; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| pre-edit `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` symlink was untracked; base revision `bd81d4853a030765585ef6fed4310484ceb1e458`, tree `fb92fc7476bff9a2ce8c20f1d7be34c6655ca6b4` |
| `git blame -L 1682,1687 -- Docs/researches/math_theorems.md` | 0 | all six sparse catalog lines originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `sha256sum Docs/Stage1_Blueprint_rev-5.6.md Docs/Stage1_Targets_rev-5.6.json Docs/Stage1_Execution_DAG_rev-5.6.json skills/execute-stage1-rev56/SKILL.md Docs/Blueprint_Guidelines.md Docs/researches/math_theorems.md Docs/Stage0_Blueprint.md Stage1_Instances/THM-M-0233/{README.md,instance.json,intake-receipt.json,scope-map.md,source-statement-crosswalk.md,task-dag.json,IntakeProbe.lean,check_intake.py,validation.md} Formalizations/Lean/{lean-toolchain,lake-manifest.json}` plus the six relevant pinned mathlib sources | 0 | exact current hashes are preserved in `statement-blocker.json`; the integrated blueprint and DAG differ from the older provisional intake receipt |
| `python3 -B Stage1_Instances/THM-M-0233/check_intake.py` | 1 | the historical intake checker expects authoritative intake state `[ ]`, while the integrated execution DAG records provisional state `[_]`; this statement run records the stale replay boundary rather than rewriting intake evidence |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| mathlib `git rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned revision and tree recorded above; package worktree clean |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0233/IntakeProbe.lean` | 0 | eight adjacent APIs elaborated; stdout SHA-256 `11d4d5f59d7240e3646186b4270d2c78fa69ec232581cc609e96033281eb9842`; stderr was empty; no target declaration |
| bounded exact-topic `rg` over repo-local and pinned-mathlib Lean roots | 1, expected no match | no argument-principle terminal target under the recorded terms |
| prohibited-declaration `rg` over owned Lean files | 1, expected no match | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `python3 -m json.tool Stage1_Instances/THM-M-0233/statement-blocker.json` | 0 | final structured blocker parsed as valid JSON |
| scoped Python assertions loading `Stage1_Instances/THM-M-0233/statement-blocker.json` | 0 | identity, blocker state, null target/imports, unchanged vector, four undefined mutations, false completion flags, exact two-file scope, and absent self-test agree |
| `git diff --check -- Stage1_Instances/THM-M-0233` and `git diff --no-index --check -- /dev/null <new-file>` for each blocker file | 0; 1 expected difference per new file | no whitespace diagnostics |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest intentionally absent because the exact-statement deliverable did not pass |

## Retry Condition

The integration lane must master-accept the intake before accepting a statement transition.
Accountable reviewers must lawfully preserve and hash one immutable primary or approved
authoritative source, select and independently approve one exact proposition, and map every
incorporated definition, ordered binder, hypothesis, conclusion, exceptional case, proof boundary,
correction, and erratum. They must freeze the contour or cycle, interior, domain, function model,
boundary conditions, pole construction, multiplicities, orientation, normalization, root clauses,
alternate encodings, and all degenerate cases.

A fresh statement worker may then encode exactly that reviewed claim, minimize its pinned imports,
serialize and hash the elaborated expression and environment, compile every credited transport,
and execute all four mutation classes.

This is a truthful blocked statement attempt, not completion of this node or any downstream node.
Lifecycle remains `planned`; `audit_complete: false` and `theorem_complete: false`; no debt-vector
change is proposed. Because the exact-statement deliverable did not pass, no
`.stage1-worker-selftest.json`, statement receipt, worker `[_]`, proof credit, or master acceptance
is claimed.
