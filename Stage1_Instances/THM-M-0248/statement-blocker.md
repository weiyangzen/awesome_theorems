# THM-M-0248 rev-5.6 statement blocker

## Decision

`S56-M-0248-STATEMENT` remains `[ ]`. Its prerequisite `S56-M-0248-INTAKE` is provisional worker
state `[_]`, not master-accepted state `[x]`; its receipt is explicitly unaccepted and has no
accepted receipt ID. Rev-5.6 section 10.2 permits preparation of a later-node blocker, but master
closure remains dependency ordered.

Independently and decisively, the exact-source-statement gate fails. The complete catalog record is
the title `毕晓普定理`, the Errett Bishop attribution, the year 1959, and the gloss `有理逼近的充要
条件`: a necessary and sufficient condition for rational approximation. It gives no citation,
formula, incorporated definition, ordered binder, hypothesis, conclusion, proof boundary,
correction history, or reviewer. Stage0 explicitly leaves the formal system, precise definitions
and premises, proof route, alternate forms, axiom policy, machine status, and artifacts open. The
catalog label `已验证` is untrusted metadata under rev-5.6 and supplies no source or kernel credit.

Bishop's *Some theorems concerning function algebras*, Bulletin AMS 65(2) (1959), 77-78, DOI
`10.1090/S0002-9904-1959-10283-4`, is a close discovery source. Its Theorem 4 starts with a compact
subset `C` of the complex plane without interior. It defines an algebra of continuous functions
that are uniform limits of rational functions with poles outside `C`, its minimal boundary `M`, a
real-part approximation class, and a strong-peak set. It states that the peak set equals `M` and
that four conditions are equivalent: universal complex approximation, universal real-part
approximation, `M = C`, and planar measure zero of `C \ M`.

That match identifies a theorem family, not a repository-approved binder-complete root. The catalog
does not cite the paper or select the full four-way equivalence, the complex-approximation iff
`M = C` form, or the measure-zero form. The two-page announcement does not provide the located full
proof, its OCR-sensitive notation needs authoritative transcription, and no correction/errata or
independent source review passed. The repository also does not freeze:

- rational functions and their pole set, cancellation, removable singularities, and infinity;
- restriction to `C`, uniform convergence, and the resulting closed separating algebra;
- minimal versus Shilov boundary, norm attainment, and strong peak points;
- the real-part algebra, ambient planar measure, and the meaning of `C \ M` measure zero; or
- empty and finite compacta, exact empty-interior encoding, binder order, and credited alternate
  forms.

These are proposition-changing choices rather than notation. Selecting any one from the discovery
paper or mathematical memory would broaden, narrow, or substitute the received theorem. Section 5
of the rev-5.6 blueprint makes statement ambiguity and a missing expression fingerprint hard
blockers. There is therefore no canonical expression whose imports can honestly be certified
minimal, no credited alternate form for a checked transport, and no canonical target against which
the required removed-hypothesis, changed-domain, changed-binder-scope, and boundary mutations can
run. Those mutations are undefined, not passed. No `Statement.lean`, declaration, proof body,
weakened special case, or broadened interface was added. The root remains `[H1, M4, R4]`.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` was re-elaborated with its two direct imports:

- `Mathlib.Analysis.Complex.Basic`
- `Mathlib.Topology.ContinuousMap.StoneWeierstrass`

It checks seven adjacent complex-number, compactness, continuous-map, separating-algebra, and real
Stone-Weierstrass interfaces. All checks pass, but the probe deliberately defines no controlled-pole
rational-function algebra, minimal boundary, canonical target, transport, or proof body. Its imports
are discovery-only and cannot be certified minimal for an absent target. A bounded exact-topic
search over repo-local Lean and pinned mathlib found only three unrelated uses of the words
"minimal boundary" and no Bishop rational-approximation terminal declaration under the recorded
terms. This is narrow feasibility evidence, not the downstream anchor audit and not a global absence
claim.

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
| `python3 scripts/stage1_target.py show THM-M-0248` | 0 | rank 1258; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| pre-edit `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` symlink was untracked; base revision `c2e294becadae6ce784f27ee69f2e8dbf57e0b30`, tree `3f567e7f76b189432b73444354070c0ff75925b9` |
| `git blame -L 1787,1792 -- Docs/researches/math_theorems.md` | 0 | all six sparse catalog lines originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| source, authority, intake, toolchain, lockfile, probe, and relevant mathlib `sha256sum` checks | 0 | exact current hashes are preserved in `statement-blocker.json` |
| `python3 -B Stage1_Instances/THM-M-0248/check_intake.py` before blocker files | 1 | the integrated intake check reaches its recorded-source freshness gate, then rejects a stale blueprint hash; the master changed the generated blueprint/DAG while accepting the provisional intake, so historical intake evidence was not rewritten |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| mathlib `git rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned revision and tree recorded above; package worktree clean |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0248/IntakeProbe.lean` | 0 | seven adjacent APIs elaborated; stdout SHA-256 `2dc99e44...3272`; empty stderr; no target declaration |
| bounded exact-topic `rg` over repo-local and pinned-mathlib Lean roots | 0 | three unrelated phrase matches; output SHA-256 `7f5facf2...0661`; no Bishop rational-approximation target located |
| prohibited-declaration `rg` over owned Lean files | 1, expected no match | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `python3 -m json.tool Stage1_Instances/THM-M-0248/statement-blocker.json` and scoped assertions | 0 | valid JSON; identity, blocked state, null target/imports, unchanged vector, undefined mutations, false completion flags, and exact two-file scope agree |
| final standard, manifest, and target-show replays | 0 each | authority projections still pass; target remains planned, uniform L0/rework-required, and theorem-incomplete |
| `git diff --check -- Stage1_Instances/THM-M-0248` plus per-file `git diff --no-index --check` | 0; 1 expected difference | no whitespace diagnostics in the tracked scope or either new blocker file |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest intentionally absent because the exact-statement deliverable did not pass |

## Retry Condition

The integration lane must master-accept fresh intake evidence before accepting a statement
transition. Accountable reviewers must lawfully preserve and hash an immutable primary or approved
authoritative source, select and independently approve one exact proposition, and map every
incorporated definition, ordered binder, hypothesis, conclusion, exceptional case, proof boundary,
correction, and erratum. They must freeze the controlled-pole rational-function model, closure and
continuous-map representation, minimal-boundary and peak predicates, real-part algebra, planar
measure, chosen equivalence, alternate encodings, and all degenerate cases.

A fresh statement worker may then encode precisely that reviewed claim, minimize its pinned imports,
serialize and hash the elaborated expression and environment, compile every credited transport, and
execute all four mutation classes.

This is a truthful blocked statement attempt, not completion of this node or any downstream node.
Lifecycle remains `planned`; `audit_complete: false` and `theorem_complete: false`; no debt-vector
change is proposed. Because the exact-statement deliverable did not pass, no
`.stage1-worker-selftest.json`, statement receipt, worker `[_]`, proof credit, or master acceptance
is claimed.
