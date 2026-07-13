# THM-M-0223 rev-5.6 statement blocker

## Decision

`S56-M-0223-STATEMENT` remains `[ ]`. Its prerequisite `S56-M-0223-INTAKE` is provisional worker
state `[_]`, not master-accepted state `[x]`; its receipt has `accepted: false` and no accepted
receipt ID. Rev-5.6 section 10.2 permits preparation of a later node under explicit concurrency,
but master closure remains dependency ordered.

Independently and decisively, the exact-source-statement gate fails. The complete catalog record is
the title `留数定理`, the Augustin Cauchy attribution, the year 1831, and the gloss
`围道积分与留数的关系`: the relation between contour integrals and residues. It gives no source
edition, theorem locator, formula, incorporated definition, ordered binder, hypothesis, conclusion,
proof boundary, correction history, or reviewer. Stage0 expressly leaves the precise definitions
and premises, formal system, alternate forms, axiom policy, machine status, and artifacts open. The
catalog label `已验证` is untrusted metadata under rev-5.6 and supplies no source or kernel credit.

The gloss identifies a classical theorem family, not one binder-complete proposition. Materially
different roots fit it: a winding-number-weighted formula for a general cycle, an unweighted formula
for a positively oriented simple boundary, and a circle specialization. Selecting any one from
mathematical memory would invent or substitute proposition-changing choices. The repository does
not fix:

- the contour, cycle, or chain representation, orientation, regularity, and integral convention;
- the ambient domain, homology assumptions, and behavior of winding number outside the contour;
- the meromorphicity neighborhood, pole set and finiteness derivation, and treatment of removable
  singularities or poles on the contour;
- residue as a Laurent coefficient, a simple-pole limit, or a normalized local integral; or
- the sign and `2 * pi * i` normalization, ordered binders, exact equality, and boundary cases.

These choices are not merely notation. In particular, `meromorphicTrailingCoeffAt` is the
coefficient at the lowest Laurent order; it agrees with the classical residue only in a suitably
selected simple-pole specialization, not for a general pole.

Section 5 of the rev-5.6 blueprint makes statement ambiguity and a missing elaborated-expression
fingerprint hard blockers. There is therefore no canonical expression whose imports can honestly be
certified minimal, no credited alternate form for a checked transport, and no canonical target
against which the required removed-hypothesis, changed-domain, changed-binder-scope, and boundary
mutations can run. Those mutations are undefined, not passed. No `Statement.lean`, declaration,
proof body, weakened special case, or broadened interface was added. The root remains
`[H1, M4, R4]`.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` was re-elaborated with its two direct imports:

- `Mathlib.Analysis.Complex.CauchyIntegral`
- `Mathlib.Analysis.Meromorphic.TrailingCoefficient`

It checks eight adjacent circle-integral, Cauchy, meromorphicity, order, and trailing-coefficient
interfaces. All checks pass, but the probe deliberately defines no residue, canonical target,
transport, or proof body. Its imports are discovery-only and cannot be certified minimal for an
absent target. A bounded exact-topic search over repo-local Lean and pinned mathlib found no general
complex residue-theorem declaration under the recorded terms. This is narrow feasibility evidence,
not the downstream anchor audit and not a global absence claim.

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
| `python3 scripts/stage1_target.py show THM-M-0223` | 0 | rank 1236; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| pre-edit `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` symlink was untracked; base revision `e179b2be594419aa5fb33c3862f73491fdaf113e`, tree `8c1da8dad4712804811f550b583129e7b73effdc` |
| `git blame -L 1612,1617 -- Docs/researches/math_theorems.md` | 0 | all six sparse catalog lines originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| authority, source, intake, probe, toolchain, lockfile, and relevant mathlib `sha256sum` checks | 0 | exact current hashes are preserved in `statement-blocker.json` |
| `python3 -B Stage1_Instances/THM-M-0223/check_intake.py` (before blocker files) | 0 | the integrated planned intake invariants passed with `H1/M4/R4` and six open tasks |
| `python3 -B Stage1_Instances/THM-M-0223/check_intake.py` (after blocker files) | 1 | the historical intake-only checker rejects the two added files because it freezes the original nine-file intake inventory; this statement run records the limitation rather than rewriting historical intake evidence |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| mathlib `git rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned revision and tree recorded above; package worktree clean |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0223/IntakeProbe.lean` | 0 | eight adjacent APIs elaborated; stdout SHA-256 `ab6097bf7bfd80e8fc18945d592028c0a19cd2437020f245edcc525067954056`; empty stderr; no target declaration |
| bounded exact-topic `rg` over repo-local and pinned-mathlib Lean roots | 1, expected no match | no general complex residue-theorem target under the recorded terms |
| prohibited-declaration `rg` over owned Lean files | 1, expected no match | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `python3 -m json.tool Stage1_Instances/THM-M-0223/statement-blocker.json` and scoped `jq` assertions | 0 | valid JSON; identity, blocked state, null target/imports, unchanged vector, four undefined mutations, false completion flags, and exact two-file scope agree |
| `git diff --check -- Stage1_Instances/THM-M-0223` plus per-file `git diff --no-index --check` | 0; 1 expected difference | no whitespace diagnostics in the tracked scope or either new blocker file |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest intentionally absent because the exact-statement deliverable did not pass |

## Retry Condition

The integration lane must master-accept the intake before accepting a statement transition.
Accountable reviewers must lawfully preserve and hash an immutable primary or approved
authoritative source, select and independently approve one exact proposition, and map every
incorporated definition, ordered binder, hypothesis, conclusion, exceptional case, proof boundary,
correction, and erratum. They must freeze the contour or cycle, domain and homology assumptions,
meromorphicity neighborhood, pole-set construction, residue definition, winding convention,
normalization, alternate encodings, and all degenerate cases.

A fresh statement worker may then encode precisely that reviewed claim, minimize its pinned imports,
serialize and hash the elaborated expression and environment, compile every credited transport, and
execute all four mutation classes.

This is a truthful blocked statement attempt, not completion of this node or any downstream node.
Lifecycle remains `planned`; `audit_complete: false` and `theorem_complete: false`; no debt-vector
change is proposed. Because the exact-statement deliverable did not pass, no
`.stage1-worker-selftest.json`, statement receipt, worker `[_]`, proof credit, or master acceptance
is claimed.
