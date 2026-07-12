# THM-M-1379 exact-statement gate: blocked

- Item: `S56-M-1379-STATEMENT`
- Base revision: `1fc66febfddf404bb914cec34962d66862b96f2b` (tree
  `49ae48302378d63f3c54b2a43eeca26433c6b7c5`)
- Attempt date: 2026-07-13 (Asia/Shanghai)
- Verdict: blocked; no statement receipt, worker `[_]`, or theorem-completion claim

## First failed gate

The exact-statement gate in section 5.1 of `Docs/Stage1_Blueprint_rev-5.6.md` cannot be
truthfully entered from the authoritative record. The mathematics catalog supplies only the name
"Hamilton-Jacobi equation," attribution to William Hamilton and Carl Jacobi, the year 1837, and the
gloss "the partial-differential-equation formulation of classical mechanics." It gives no formula,
cited truth-valued proposition, incorporated definitions, ordered binders, hypotheses, conclusion,
or boundary cases. Stage0 explicitly leaves the precise definitions, premises, equivalent forms,
axioms, machine status, and artifacts open. The catalog's `已验证` value is untrusted metadata under
rev-5.6. The manifest's ODE category also conflicts with the catalog's PDE gloss; that boundary
must be reconciled rather than silently choosing one classification.

The wording identifies an equation or formalism family, not one theorem. It does not choose whether
the root is an equation definition, a derivation from an action principle, an equivalence with
Hamiltonian characteristics, an existence or uniqueness theorem, a regularity result, or a
canonical-transformation theorem. A complete-integral claim is separately assigned to
`THM-M-1380`. These alternatives require materially different spaces, Hamiltonian and action data,
derivative and solution notions, regularity, initial or boundary data, quantifier order, and
conclusions. Selecting one from convention would invent, narrow, broaden, or substitute
mathematics rather than elaborate the received target.

The distinct physics target `THM-P-0755` displays the familiar schema
`H(q, partial S/partial q, t) + partial S/partial t = 0`. It cannot repair this record: it has a
different UID, discipline, wording, and date, and the displayed equation still does not say what
truth-valued result is to be proved. A stationary equation, a free-particle or one-dimensional
special case, and a predicate that assumes satisfaction of the equation are likewise not valid
substitutes.

Consequently there is no canonical expression to elaborate, no honest minimal-import claim, and no
canonical expression or environment fingerprint. Checked transports and the required
removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case mutations are undefined
until a source-correct statement fixes binders and premises. The intake vector remains
`[H5, M4, R4]`; no debt change is proposed. No `Statement.lean`, axiom, placeholder, assumed
solution, or substituted theorem was introduced.

The intake prerequisite is only provisional `[_]`, and its worker receipt is not accepted. This
independently prevents statement-node acceptance. The first substantive failure in this attempt is
the absent exact source proposition.

## Pinned Lean boundary

The existing `IntakeProbe.lean` was re-elaborated with the pinned environment. Its four imports
expose adjacent Frechet-derivative, gradient, integral-curve, and symplectic-matrix APIs, and all
eight `#check` commands passed. The probe states no Hamilton-Jacobi proposition, and its imports
cannot be certified minimal for an unidentified target. This check receives no statement, anchor,
or proof credit.

A bounded case-insensitive search of repo-local Lean and pinned mathlib located no
Hamilton-Jacobi-named target. One result mentioned the unrelated Jacobi equation for geodesic
variations. This is narrow feasibility evidence, not the downstream immutable anchor audit or a
global absence claim.

The environment is Lean 4.29.0 at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` (tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`). The automation-provided
`Formalizations/Lean/.lake` symlink points to the canonical pinned artifacts and was used read-only.
No `lake update`, `lake build`, dependency clone or fetch, or other `.lake` mutation was run.

## Validation evidence

Commands ran in this worker clone on 2026-07-13 (Asia/Shanghai), from the repository root unless a
different working directory is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1379` | 0 | rank 989, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| initial `git status --short --untracked-files=all` and `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree are recorded above |
| `sed -n '10048,10053p' Docs/researches/math_theorems.md`; `sed -n '6443,6449p' Docs/researches/physics_theorems.md`; `sed -n '37506,37531p' Docs/Stage0_Blueprint.md`; `python3 scripts/stage1_target.py show THM-M-1379`; and `sed -n` reads of the six named intake artifacts | 0 each | only an equation/formalism-family gloss is authoritative; every proposition-changing choice remains open |
| exact `sha256sum` invocation recorded in `statement-blocker.json` | 0 | all 20 current authority, source, intake, toolchain, manifest, probe, and pinned mathlib hashes matched the structured blocker |
| `python3 -B Stage1_Instances/THM-M-1379/check_intake.py` | 1 | historical intake replay stopped at its stale blueprint hash; this phase did not rewrite intake evidence to manufacture freshness |
| `cd Formalizations/Lean && lake env lean --version` and `lake --version` | 0 | Lean and Lake agree with the pinned environment above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and `status --short` | 0 | revision and tree agree with the fingerprint; package worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1379/IntakeProbe.lean` plus the exact combined-output hash pipeline in `statement-blocker.json` | 0 each | all eight adjacent APIs elaborated; combined output SHA-256 `4c165b56...30c097`; no canonical target was stated |
| three exact `rg` invocations recorded in `statement-blocker.json` | 0, 1, 1 | the first found one unrelated Jacobi-equation prose hit; the two expected no-match searches found no exact target |
| prohibited Lean construct scan over `Stage1_Instances/THM-M-1379` | 1 | expected no-match exit; no `sorry`, `admit`, `sorryAx`, axiom, bodyless declaration, or unsafe declaration |
| `python3 -m json.tool Stage1_Instances/THM-M-1379/statement-blocker.json` | 0 | structured blocker parses as JSON |
| exact `python3 -c` invariant script recorded in `statement-blocker.json` | 0 | identity, null target, undefined mutations, unchanged debt, false completion flags, exact path scope, and absent self-test agree |
| exact `bash -lc` whitespace wrapper recorded in `statement-blocker.json` | 0 | `git diff --check` emitted no diagnostics; each untracked-file no-index check returned expected diff exit 1 with no whitespace diagnostics, normalized by the recorded wrapper |
| `test ! -e .stage1-worker-selftest.json` | 0 | no worker self-test manifest exists because the exact-statement deliverable is blocked |

## Retry condition

The integration lane must master-accept refreshed intake evidence. Accountable reviewers must then
preserve and hash one immutable primary or approved authoritative source, select and transcribe one
exact truth-valued claim and all incorporated definitions with pinpoint locators, audit corrections
and errata, reconcile the mathematical target with `THM-P-0755`, `THM-M-1380`, and neighboring
mechanics targets, and independently approve the source crosswalk. The decision must freeze the
claim kind, time-dependent or stationary convention, configuration and phase spaces, Hamiltonian
and action domains, derivative and solution notions, regularity, data, ordered binders, hypotheses,
conclusion, every degenerate or boundary case, and the ODE-category/PDE-gloss conflict.

A later statement worker can then encode precisely that claim, minimize its pinned imports,
serialize and hash the elaborated expression and environment, compile every credited transport,
and run all four required mutation classes.

This is a blocked-attempt record, not completion of the statement node or any downstream node.
`audit_complete` and `theorem_complete` remain false. Because the assigned phase is not genuinely
self-tested to its completion gate, no `.stage1-worker-selftest.json`, node receipt, worker `[_]`,
or master acceptance is claimed.
