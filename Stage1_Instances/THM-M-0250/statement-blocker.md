# THM-M-0250 rev-5.6 statement blocker

## Decision

`S56-M-0250-STATEMENT` remains `[ ]`. Its prerequisite `S56-M-0250-INTAKE` is provisional worker
state `[_]`, not master-accepted state `[x]`; its receipt has `accepted: false`, is not
content-addressed, and contains no accepted receipt ID. Rev-5.6 section 10.2 permits preparation of
a later node under explicit concurrency, but master closure remains dependency ordered.

Independently and decisively, the exact-source-statement gate fails. The complete repository record
provides the title "Hardy space theory," attribution to Godfrey Hardy, the year 1915, and only the
phrase "Hardy spaces on the unit disk." It gives no source edition, theorem locator, verbatim
proposition, incorporated definition, ordered binder, hypothesis, conclusion, proof boundary,
correction history, or reviewer. Stage0 expressly leaves the precise definitions and premises,
formal system, alternate forms, axiom policy, machine status, and artifacts open. The catalog label
`verified` is untrusted metadata under rev-5.6 and supplies no source or kernel credit.

The phrase names a classical analytic subject, not one binder-complete truth-valued proposition.
Materially different roots fit it: constructing an analytic `H^p` carrier, proving completeness,
identifying boundary `L^p` values, characterizing `H^2` coefficients, or proving an evaluation or
growth estimate. Selecting any one from mathematical memory would invent or substitute
proposition-changing mathematics. In particular, the repository does not fix:

- the exponent and endpoint regime, including finite `p`, `0 < p < 1`, or `p = infinity`;
- the analytic-function and unit-disk models, scalar or value spaces, and equality convention;
- a radial or boundary definition, angular-measure normalization, supremum or limit convention,
  and norm or quasinorm;
- the ordered binders, hypotheses, exact conclusion, constants, and alternate encodings; or
- the zero function, radius-zero and radius-one behavior, boundary representatives, and other
  degenerate cases.

The Crossref record for Hardy's 1915 article *The Mean Value of the Modulus of an Analytic
Function* is only a bibliographic discovery lead. No immutable article text, pinpoint theorem,
incorporated definitions, source-to-modern-`H^p` mapping, errata disposition, or independent review
has been admitted. The catalog itself does not cite the article.

Sections 5 and 5.1 of the rev-5.6 blueprint make statement ambiguity and a missing elaborated
expression fingerprint hard blockers. There is therefore no canonical expression whose imports can
honestly be certified minimal, no alternate expression eligible for a checked transport, and no
canonical target against which the required removed-hypothesis, changed-domain,
changed-binder-scope, and boundary-case mutations can run. Those mutations are undefined, not
passed. No `Statement.lean`, declaration, proof body, weakened special case, or broadened interface
was added. The provisional dossier vector remains `[H5, M4, R4]`; `H5` classifies the received noun
phrase, not Hardy-space mathematics or a future corrected statement.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` was re-elaborated with its two direct imports:

- `Mathlib.Analysis.Complex.UnitDisc.Basic`
- `Mathlib.Analysis.Complex.MeanValue`

It checks six adjacent unit-disc, analyticity, circle-average, circle-integrability, and mean-value
interfaces. All checks pass, but the probe deliberately defines no Hardy space, canonical target,
transport, or proof body. Its imports are discovery-only and cannot be certified minimal for an
absent target. A bounded exact-topic search over repo-local Lean and pinned mathlib found no
Hardy-space-named declaration under the recorded terms. This is narrow feasibility evidence, not
the downstream immutable anchor audit and not a global absence claim.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided canonical `.lake` symlink was
used read-only. No `lake update`, `lake build`, dependency clone or fetch, or other `.lake` mutation
was run.

## Validation Record

Commands ran from the isolated worker clone on 2026-07-13 (`Asia/Shanghai`). Base revision:
`c2e294becadae6ce784f27ee69f2e8dbf57e0b30`; tree:
`3f567e7f76b189432b73444354070c0ff75925b9`.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0250` | 0 | rank 1260; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| pre-edit `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree are recorded above |
| repository source, Stage0, manifest, blueprint, DAG, skill, guidelines, and intake-dossier inspection | 0 | the source is a subject phrase; the intake leaves the proposition and formal target null; the statement node depends on provisional intake |
| `git blame -L 1801,1806 -- Docs/researches/math_theorems.md` and scoped hashes | 0 | all six catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`; exact current hashes are in `statement-blocker.json` |
| `python3 -B Stage1_Instances/THM-M-0250/check_intake.py` | 1 | historical intake replay stops at its frozen base-revision assertion (`c6fd6dad...` versus current `c2e294be...`); the statement run records rather than rewrites historical intake evidence |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| mathlib `git rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned revision and tree recorded above; package worktree clean |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0250/IntakeProbe.lean` | 0 | six adjacent APIs elaborated; stdout SHA-256 `ed358da14cfc78581cb4547098669bf10846f220ec750af98d114fdd8a248aca`; empty stderr; no target declaration |
| bounded exact-topic `rg` over repo-local and pinned-mathlib Lean roots | 1, expected no match | no Hardy-space-named declaration under the recorded terms; bounded discovery evidence only |
| prohibited-declaration `rg` over owned Lean files | 1, expected no match | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `python3 -m json.tool Stage1_Instances/THM-M-0250/statement-blocker.json` and scoped Python assertions | 0 | valid JSON; identity, blocked state, null target/imports, unchanged vector, four undefined mutations, false completion flags, and exact two-file scope agree |
| scoped `git diff --check` and per-new-file `git diff --no-index --check` | 0; 1 expected difference | no whitespace diagnostics; no-index exit 1 is only the expected new-file difference |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest intentionally absent because the exact-statement deliverable did not pass |

The historical intake checker is bound to the intake worker's original base revision and exact
nine-file intake inventory. Integration advanced the repository and authority projections; this
statement phase also adds two owned blocker artifacts. Rewriting that checker or its receipt would
alter historical intake evidence, so the current failure is recorded as a known limitation.

## Retry Condition

The integration lane must master-accept the intake before accepting a statement transition.
Accountable reviewers must preserve and hash a lawful immutable primary or approved authoritative
source, select and independently approve one exact proposition, and map every incorporated
definition, ordered binder, hypothesis, conclusion, exceptional case, proof boundary, correction,
and erratum. They must freeze the disk and analytic-function encodings, exponent and endpoints,
radial or boundary functional, measure normalization, equality and norm conventions, constants,
alternate encodings, and all degenerate cases.

A fresh statement worker may then encode precisely that reviewed claim, minimize its pinned
imports, serialize and hash the elaborated expression and environment, compile every credited
transport, and execute all four mutation classes.

This is a truthful blocked statement attempt, not completion of this node or any downstream node.
Lifecycle remains `planned`; `audit_complete: false` and `theorem_complete: false`; no debt-vector
change is proposed. Because the exact-statement deliverable did not pass, no
`.stage1-worker-selftest.json`, statement receipt, worker `[_]`, proof credit, or master acceptance
is claimed.
