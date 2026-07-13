# Exact-statement gate: blocked

Item: `S56-M-0270-STATEMENT`

Theorem: `THM-M-0270`

Base revision: `a75b2f3ac5b8b7d34eb73435734edfeecc41bd40` (tree
`66a22e1dc2e1c14c27bd01396a99826ab2536bf1`).

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the received repository record. The
catalog supplies the name Fatou's lemma, Pierre Fatou, the year 1906, and only the gloss "an
inequality for the liminf of integrals." It gives no bibliography, formula, ordered binders,
hypotheses, incorporated definitions, proof boundary, correction history, boundary cases, or
independent reviewer. `Docs/Stage0_Blueprint.md` explicitly leaves the precise definitions and
premises open, and the catalog's verified label is untrusted under rev-5.6.

The gloss does not select the measure space or sequence context; nonnegative real, `ENNReal`,
signed, or lower-bounded functions; measurable versus a.e.-measurable functions; pointwise versus
essential liminf; lower Lebesgue versus signed or Bochner integration; or the exact finite,
infinite, null-set, and measurability boundary cases. These choices change the proposition.

The intake inspected Sheldon Axler's *Measure, Integration & Real Analysis*, Section 3A, Exercise
17, printed page 86. It is a strong modern `H1` lead for the measurable nonnegative pointwise form,
but it does not close the source gate: the catalog does not cite it, the result is an exercise
without a supplied proof, incorporated definitions and integral conventions have not been fully
crosswalked, the relationship to the catalog's 1906 attribution is unverified, and no independent
source reviewer has approved it. Crossref metadata for Fatou's 1906 paper supplies no inspected
exact lemma passage.

The intake therefore deliberately leaves `canonical_statement`, `canonical_claim`, ordered
binders, hypotheses, conclusion, Lean module and expression, elaborated-expression hash, and
canonical-target environment fingerprint null at `[H1, M3, R4]`. Selecting Axler's measurable
form, the a.e.-measurable mathlib form, or a signed or lower-bounded generalization in this phase
would silently settle proposition-changing source choices that the prerequisite explicitly keeps
open. Rev-5.6 sections 5 and 5.1 make that ambiguity and the missing expression fingerprint hard
statement blockers.

Without a canonical expression, no import can be certified minimal, no alternate encoding can
receive a checked transport, and the required removed-hypothesis, changed-domain,
changed-binder-scope, and boundary-case mutations are undefined rather than passed. No
`Statement.lean`, assumed theorem, axiom, placeholder, weakened special case, or broadened theorem
was introduced.

The prerequisite `S56-M-0270-INTAKE` has provisional worker state `[_]`, not master-accepted state
`[x]`. Its receipt declares `accepted: false`, is not content-addressed, and has no accepted receipt
ID. It permits this dependency-ordered attempt but remains an independent acceptance blocker for a
future statement transition.

## Pinned Lean Boundary

The existing discovery-only `IntakeProbe.lean` re-elaborates in the pinned environment. It checks
two exact-topic interfaces from `Mathlib.MeasureTheory.Integral.Lebesgue.Add`:

```text
MeasureTheory.lintegral_liminf_le'
  (forall n, AEMeasurable (f n) mu) ->
  integral^- (liminf f atTop) dmu <= liminf (fun n => integral^- (f n) dmu) atTop

MeasureTheory.lintegral_liminf_le
  (forall n, Measurable (f n)) ->
  integral^- (liminf f atTop) dmu <= liminf (fun n => integral^- (f n) dmu) atTop
```

Both use `f : Nat -> alpha -> ENNReal`, and both axiom reports are exactly `propext`,
`Classical.choice`, and `Quot.sound`. The probe also authenticates three adjacent lower-integral and
liminf APIs. This is real pinned candidate evidence, but the probe defines no canonical target,
source transport, mutation, or proof body. Its import cannot be certified minimal for an absent
root. A bounded repository and pinned-mathlib search found these declarations and downstream uses;
it establishes no accepted source-identical mapping and is not the downstream anchor audit.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` symbolic link was used read-only. No `lake update`, `lake build`,
dependency clone or fetch, or other `.lake` mutation was run.

## Validation Evidence

Commands ran in this isolated worker clone on 2026-07-13 (`Asia/Shanghai`), from the repository
root unless a different working directory is shown.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0270` | 0 | rank 1277; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` before editing | 0 | only the automation-provided untracked `.lake` link existed; base identifiers appear above |
| source record, Stage0, intake dossier, Axler lead, and pinned Fatou source inspection | 0 | confirmed that the received gloss does not select one proposition and the modern lead remains H1 without an accepted complete source map |
| `sha256sum` over authority, intake, toolchain, manifest, probe, and pinned candidate source | 0 | exact fingerprints are recorded in `statement-blocker.json` |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned mathlib revision and tree recorded above; package worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0270/IntakeProbe.lean` | 0 | two Fatou candidates and three adjacent APIs elaborated; candidate axioms were `[propext, Classical.choice, Quot.sound]`; stdout SHA-256 `383e38620a29d7f4812de9da059233c9125365472b6c9ec1e769cf9b47d01008` |
| bounded `rg` exact-topic search in repo-local Lean and pinned mathlib | 0 | found the two declarations and downstream uses; no accepted source-identical root mapping was credited |
| `python3 -B Stage1_Instances/THM-M-0270/check_intake.py` | 1 | historical intake replay stops at its frozen authoritative intake state `[ ]`; the integrated DAG now records provisional `[_]`, so the historical checker was not rewritten |
| prohibited-declaration scan over owned Lean files | 1 | expected no-match result: no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration token; diagnostic `#print axioms` is permitted |
| `python3 -m json.tool Stage1_Instances/THM-M-0270/statement-blocker.json` plus scoped blocker invariants | 0 | structured blocker parses; identity, dependency, null target/imports, undefined mutations, unchanged vector, false completion flags, and absent self-test agree |
| `git diff --check -- Stage1_Instances/THM-M-0270` plus direct byte checks on both blocker files | 0 | no whitespace, newline, carriage-return, or NUL diagnostics |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest intentionally absent because the exact-statement deliverable did not pass |

The intake checker freezes its original authority state and nine-file intake-only inventory. It is
historical evidence rather than a validator for later artifacts. This phase records that limitation
instead of rewriting the intake instance, receipt, checker, task DAG, generated blueprint, or
authoritative execution DAG to manufacture agreement.

## Retry Condition And Status Boundary

The integration lane must master-accept refreshed intake evidence before accepting a later
statement transition. Accountable reviewers must lawfully preserve and hash one immutable primary
or authoritative source, transcribe and independently approve one exact proposition with every
incorporated definition, ordered binder, hypothesis, conclusion, proof boundary, correction,
erratum, and boundary case, and resolve the nonnegative/measurable/liminf/integral conventions.

A later statement worker can then encode precisely that approved claim, minimize its pinned
imports, serialize and hash the elaborated expression and environment, compile every credited
transport, and execute all four required mutation classes.

This is a blocked-attempt record, not completion of the statement node or any downstream node. The
node remains `[ ]`; lifecycle remains `planned`; the root remains `[H1, M3, R4]`, with
`audit_complete: false` and `theorem_complete: false`; no debt-vector change is proposed. Because
the assigned phase is not genuinely self-tested to its completion gate, no
`.stage1-worker-selftest.json`, statement receipt, worker `[_]`, or master acceptance is claimed.
