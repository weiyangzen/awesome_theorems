# THM-M-1479 exact-statement gate: blocked

Item: `S56-M-1479-STATEMENT`

Base revision: `9e2ab501f9bd297b7bda1d222aec4e6f2029019a` (tree
`eab3198df44944dd50b95951243c5f9d3922a703`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-1479-INTAKE` has provisional worker
state `[_]`, but its receipt is unaccepted and non-content-addressed and contains no accepted
receipt ID. The intake checker also freezes the older authoritative state `[ ]`; it no longer
replays after integration changed the intake task to `[_]`. Master closure therefore remains
dependency ordered.

Independently and decisively, the exact-statement gate fails. The repository supplies only the
label "Monte Carlo methods" and the gloss "a numerical method based on random sampling." This is a
method family, not a proposition. It fixes no target quantity, domain or measure, sampling law,
estimator or algorithm, sample-size convention, measurability or moment assumptions, convergence
or error notion, exact conclusion, constants or rates, computation boundary, ordered binders, or
degenerate cases. Stage0 explicitly leaves exact definitions and premises open. The intake record
therefore leaves the human claim and canonical Lean target null at `[H5, M4, R4]`.

Unbiasedness, almost-sure or in-probability consistency, variance or mean-square error, a central
limit theorem, a concentration or confidence bound, and algorithm-specific correctness are
materially inequivalent. Selecting iid samples, a sample mean, an integral, a law of large numbers,
or a familiar rate would invent, narrow, or substitute mathematics. The 1949 Metropolis-Ulam
article recorded at intake is only a bibliographic source-family lead: it differs from the
catalog's 1946 Ulam-von Neumann attribution, overlaps a separately owned physics target, and has no
admitted exact passage, assumptions, proof boundary, corrections audit, or independent review.

Consequently there is no canonical expression to elaborate, no honest minimal-import claim, no
expression or environment fingerprint, and no credited alternate encoding. The required removed-
hypothesis, changed-domain, changed-binder-scope, and boundary-case mutations are undefined, not
passed. No `Statement.lean`, theorem declaration, proof body, weakened special case, or broadened
interface was added.

## Pinned Lean Boundary

The existing discovery-only `IntakeProbe.lean` was re-elaborated using Lean 4.29.0 at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740` and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` (tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`). Its two imports expose generic integrability,
independence, identical-distribution, variance, Chebyshev-bound, and strong-law APIs. Eight checks
elaborated, and three representative axiom reports list only `propext`, `Classical.choice`, and
`Quot.sound`. The probe defines no source-selected quantity, estimator, algorithm, or conclusion;
its imports cannot be certified minimal for the absent target.

A bounded exact-topic search of repo-local Lean and pinned mathlib found only an unrelated
bibliography mention. This is narrow feasibility evidence, not the downstream anchor audit or a
global absence proof. The automation-provided canonical `.lake` symlink and pinned artifacts were
used read-only. No dependency update, build, clone, fetch, or other `.lake` mutation was run.

## Validation Record

Commands ran from the isolated worker clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1479` | 0 | rank 1156; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| pre-edit `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| authority and null-target assertions over the target manifest, execution DAG, `instance.json`, and intake receipt | 0 | intake `[_]`, statement `[ ]`, dependency, null claim and target, unaccepted receipt, and H5/M4/R4 agree |
| `git blame -L 10791,10796 -- Docs/researches/math_theorems.md` | 0 | all six sparse catalog lines originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `python3 -B Stage1_Instances/THM-M-1479/check_intake.py` | 1 | historical intake checker expects authoritative intake state `[ ]`, while integration records provisional `[_]`; this statement phase records rather than rewrites stale intake evidence |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| pinned mathlib `git rev-parse HEAD 'HEAD^{tree}'` and `status --short` | 0 | revision and tree recorded above; package worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1479/IntakeProbe.lean` | 0 | eight adjacent APIs elaborated; output SHA-256 `804eac01ac63d5f11fb964e6a055933afbdc0770de775ec89f7f177fde6df665`; no target declaration |
| bounded exact-topic `rg` over repo-local Lean and pinned mathlib | 0 | one unrelated bibliography match; output SHA-256 `51897e9eb7ac1f2631f633f9a821a9d7b1b3b04691a1c4048038a7bc8bc04565`; no source-selected declaration located |
| prohibited-construct scan over owned Lean files | 0 | expected no-match branch; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |

Final JSON, invariant, whitespace, and absent-self-test checks are recorded in the structured
blocker beside this report.

## Retry Condition

The integration lane must first master-accept refreshed intake evidence. Accountable reviewers
must then preserve and hash an immutable primary or approved authoritative source and independently
select one exact truth-valued proposition. They must freeze the target quantity; domains and
measures; sampling law; estimator or algorithm; indexing and normalization; every measurability,
integrability, independence, and moment premise; conclusion, error notion, constants, and rates;
ordered binders; computation and randomness boundary; source corrections; neighbor ownership; and
every degenerate case.

A fresh statement worker may then encode exactly that reviewed claim, minimize its pinned imports,
serialize and hash the elaborated expression and environment, compile every credited transport,
and execute all four mutation classes.

This is a truthful blocked statement attempt, not completion of this node or a downstream node.
Lifecycle remains `planned`; `audit_complete: false` and `theorem_complete: false`; no debt-vector
change is proposed. Because the exact-statement deliverable did not pass, no
`.stage1-worker-selftest.json`, statement receipt, worker `[_]`, proof credit, or master acceptance
is claimed.
