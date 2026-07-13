# THM-M-0966 exact-statement gate: blocked

Item: `S56-M-0966-STATEMENT`

Base revision: `a1c9974d7fb28cd680e6494b968544bf801a93a2` (tree
`1fa287bc821355aca2ca9e3ce107830a3eb58e64`). Attempt date: 2026-07-13
(`Asia/Shanghai`).

## Decision

The statement item remains `[ ]`. Its prerequisite, `S56-M-0966-INTAKE`, is provisional worker
state `[_]`, not master-accepted state `[x]`. The intake receipt declares `accepted: false`, is not
content-addressed, has no accepted receipt ID, and deliberately leaves the canonical mathematical
statement and Lean expression null. Dependency-ordered inspection may proceed, but this intake is
not accepted statement authority.

Independently and decisively, the complete repository claim is only the title "Kruskal-Katona
theorem" and the gloss `阴影的最小大小` ("minimum size of the shadow"). It supplies no citation,
definition of shadow, ground set or family encoding, uniformity convention, cardinality parameter,
ordered binders, hypotheses, exact conclusion, proof boundary, correction history, or boundary
policy. Stage0 repeats the gloss while explicitly leaving exact definitions and premises open. The
catalog's `已验证` label is untrusted under rev-5.6.

The wording does not select among materially different propositions:

- the conditional one-step comparison with a supplied colex initial segment;
- existence of an exactly equicardinal colex segment and attainment of the minimum;
- the explicit binomial or cascade numerical lower bound;
- an iterated-shadow theorem or the Lovasz binomial-threshold consequence; or
- a characterization of equality cases or all minimizers.

Those alternatives differ in hypotheses, quantifiers, conclusions, and required bridges. Selecting
the familiar mathlib declaration from the theorem name or docstring would therefore substitute
proposition-changing mathematics. Rev-5.6 sections 5 and 5.1 make this ambiguity and the missing
expression fingerprint hard blockers. There is no canonical target for which imports can be
certified minimal, alternate encodings transported, or the required removed-hypothesis,
changed-domain, changed-binder-scope, and boundary-case mutations executed. Those tests are
undefined, not passed. The root remains `[H1, M3, R4]`.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` was re-elaborated with pinned Lean and mathlib. It exposes the
credible direct candidate:

```text
Finset.kruskal_katona
  {n r : Nat} {A C : Finset (Finset (Fin n))}
  (hAr : (A : Set (Finset (Fin n))).Sized r)
  (hCA : C.card <= A.card)
  (hC : Finset.Colex.IsInitSeg C r) :
  C.shadow.card <= A.shadow.card
```

It also exposes `Finset.iterated_kk` and `Finset.kruskal_katona_lovasz_form`. All three reported
only `propext`, `Classical.choice`, and `Quot.sound`. The basic candidate is conditional on a
supplied `C`; it does not state exact-cardinality segment existence, the cascade value, or equality
classification. The iterated and Lovasz declarations are separate proposition-changing forms.
They therefore remain discovery-only evidence, not a selected target, checked source transport, or
proof credit.

The proof-bearing candidate module is
`Mathlib.Combinatorics.SetFamily.KruskalKatona` at pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided canonical `.lake` symlink
was used read-only. No dependency update, build, clone, fetch, or other `.lake` mutation was run.
No target declaration or proof body was added.

## Validation Record

Commands ran in this isolated worker clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | all 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, and execution-skill presence passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0966` | 0 | rank 1500; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| pre-edit `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| scoped blueprint, manifest, execution DAG, skill, guideline, catalog, Stage0, and intake inspection | 0 | confirmed target membership, provisional prerequisite, sparse gloss, null canonical target, and unresolved proposition-changing choices |
| `git blame -L 7057,7062 -- Docs/researches/math_theorems.md` | 0 | all six sparse catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | Lean 4.29.0 commit `98dc76e3...`; Lake `5.0.0-src+98dc76e` |
| pinned mathlib revision, tree, and status checks | 0 | revision and tree recorded above; package worktree clean |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0966/IntakeProbe.lean` | 0 | seven candidate interfaces elaborated; three axiom reports contained only the standard three axioms; stdout SHA-256 `b416f04883079ac7623bbcf222cf7234f6dc5b885015d6c4f34c6a1369424da3` |
| bounded exact-topic search in repo-local Lean and pinned mathlib | 0 | found the pinned Kruskal-Katona module and neighboring discovery probes; no source-approved `THM-M-0966` target identity |
| `python3 -B Stage1_Instances/THM-M-0966/check_intake.py` | 1 | historical intake checker expects its authoritative intake row at `[ ]`; integration now records provisional `[_]`; stale historical evidence, not statement validation |
| prohibited-construct scan over owned Lean files | 1, expected no match | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |

Final JSON, invariant, whitespace, scoped-change, and absent-self-test checks are recorded in the
structured blocker beside this report.

## Retry Condition And Status Boundary

The integration lane must first master-accept refreshed intake evidence. Accountable source and
scope reviewers must then lawfully preserve and hash an immutable primary or approved authoritative
source, select one exact theorem or explicitly reviewed conjunction, and independently approve every
incorporated definition, ordered binder, hypothesis, conclusion, proof boundary, correction,
erratum, parameter range, and degenerate case. They must resolve one-step versus iterated shadow,
comparison versus attainment, colex versus cascade form, ground-set and family encodings, and
whether any equality statement belongs to the root.

A fresh statement worker can then encode precisely that reviewed claim, minimize its pinned
imports, serialize and hash the elaborated expression and environment, compile every credited
transport, and execute all four required mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. Because the exact-statement
deliverable did not pass, no `.stage1-worker-selftest.json`, statement receipt, worker `[_]`, proof
credit, or master acceptance is claimed.
