# THM-M-0071 exact-statement gate: blocked

- Item: `S56-M-0071-STATEMENT`
- Base revision: `f23ca64267b6746e12a641dcc66cc4dbaf1e2191` (tree
  `d1872d3251ef6a9c395116467608691849d80496`)
- Attempt date: 2026-07-13 (Asia/Shanghai)
- Verdict: blocked; no statement receipt, worker `[_]`, or theorem-completion claim

## First failed gate

The exact-statement gate in section 5.1 of `Docs/Stage1_Blueprint_rev-5.6.md` cannot be
truthfully completed from the repository record. The catalog supplies only the slogan that every
finite simple group belongs to 18 infinite families or 26 sporadic groups. It gives no citation,
family roster, admissible parameters, exceptions, representatives, incorporated definitions,
ordered binders, precise conclusion, proof boundary, corrections, or independent source review.
Stage0 explicitly leaves the exact definitions and premises open, and the catalog's `部分验证`
label is untrusted metadata under rev-5.6.

The intake records Tatitscheff's arXiv `1902.03118v4`, Theorem 1, as a secondary exact-wording and
family-count witness only. Its cyclic-prime and alternating families plus 16 Lie-type families do
not supply formal group representatives, every parameter restriction, low-rank exclusion, central
quotient, exceptional isomorphism, or the proof-source ledger. Gorenstein's 1983 Volume 1 is a
primary proof-boundary lead, not a self-contained terminal 18/26 theorem or complete source map.
Neither source is accepted as `H0` or independently approved.

The missing choices change the proposition rather than merely its notation:

- the convention for simple groups, including finiteness and nontriviality;
- classification up to `MulEquiv` or another checked equivalence relation;
- the exact convention-sensitive 18-family roster and every admissible parameter, quotient,
  twist, nonsimple exception, and accidental isomorphism;
- actual formal representatives for all 26 sporadic groups and the treatment of the Tits group;
- exhaustiveness alone versus unique classification data, nonduplication, or pairwise
  nonisomorphism; and
- the ordered binders, universes, hypotheses, conclusion, foundations, and all boundary cases.

Inventing an `IsClassified` predicate, using `Fin 18` and `Fin 26` as labels, or assuming a family
enumeration would hide the missing mathematics. A four-class summary, the finite abelian-simple
classification, or simplicity of `A5` would be weaker substituted theorems. Consequently there is
no canonical expression on which to certify minimal target imports, serialize an expression
fingerprint, compile checked alternate transports, or run the required removed-hypothesis,
changed-domain, changed-binder-scope, and boundary-case mutations. Those tests are undefined, not
passed. The root remains `[H1, M4, R4]`.

The intake prerequisite is provisional `[_]` in the current execution DAG, but its worker receipt
declares `accepted: false` and no accepted receipt ID exists. This independently leaves master
acceptance open. The first substantive failure in this attempt remains the absent source-complete
taxonomy and proposition.

## Pinned Lean boundary

`StatementProbe.lean` uses only `Mathlib.Data.Finite.Defs` and
`Mathlib.GroupTheory.Subgroup.Simple`. It elaborates `Finite`, `IsSimpleGroup`, `MulEquiv`, and
`MulEquiv.isSimpleGroup_congr` in the pinned environment. Removing either direct import makes the
corresponding checks fail, so these are narrow substrate imports. They are not claimed to be the
minimal imports for an unidentified canonical target, and the probe declares no theorem or
classification predicate.

The older `IntakeProbe.lean` also re-elaborates nine adjacent simple-group, finite abelian-simple,
and `A5` interfaces. A bounded search found only the CFSG title in mathlib's documentation index,
the adjacent abelian and `A5` branches, and a TODO for general alternating-group simplicity; it
located no exact CFSG, 18-family, or sporadic-representative declaration. This is narrow feasibility
evidence, not the downstream immutable anchor audit or a global absence claim.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` (tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`). The automation-provided
`Formalizations/Lean/.lake` symlink points to canonical pinned artifacts and was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, or other `.lake` mutation was run.

## Validation evidence

Commands ran in this worker clone on 2026-07-13 (Asia/Shanghai), from the repository root unless a
different working directory is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0071` | 0 | rank 1016; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| initial `git status --short --untracked-files=all` and `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree are recorded above |
| scoped reads of the blueprint, skill, manifest, catalog, Stage0 record, and complete intake dossier | 0 | the literal 18/26 slogan is not a source-complete proposition; the intake intentionally leaves its canonical statement and formal target null |
| `sha256sum` over authority, intake, toolchain, lockfile, probe, and relevant mathlib inputs | 0 | exact current digests are recorded in `statement-blocker.json` |
| `python3 -B Stage1_Instances/THM-M-0071/check_intake.py` | 1 | historical intake checker expects its original authoritative intake state `[ ]`; current authority records provisional `[_]`; this phase did not rewrite intake evidence |
| `cd Formalizations/Lean && lake env lean --version` and `lake --version` | 0 | Lean and Lake agree with the pinned environment above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned revision and tree above; package worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0071/StatementProbe.lean` | 0 | four narrow substrate APIs elaborated; output 323 bytes, 5 lines, SHA-256 `c26d7d678f0a996469e56a7c3270bade6b2cbf26d12504bfb4565f75a6e0345c` |
| repeat the statement probe from temporary copies while omitting each direct import | 1 each | omitting `Finite.Defs` makes `Finite` unknown; omitting `Subgroup.Simple` makes the three group interfaces unknown |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0071/IntakeProbe.lean` | 0 | nine adjacent APIs re-elaborated; output 1,089 bytes, 13 lines, SHA-256 `a0cc26767186f6c4e43b2bd8b9ed22c5a97cdf05aa5ab3ffb00733a3b328ba5c` |
| bounded CFSG, family, representative, and simple-group searches in repo-local Lean and pinned mathlib | 0 / 1 | documentation and adjacent-branch searches found the title, finite abelian-simple and `A5` facts, and the alternating-simplicity TODO; the focused exact-target search returned expected no-match exit 1 |
| prohibited-construct scan over owned Lean | 1 | expected no-match exit; no `sorry`, `admit`, `sorryAx`, axiom, bodyless declaration, or unsafe declaration |
| `python3 -m json.tool Stage1_Instances/THM-M-0071/statement-blocker.json` and scoped invariant/hash assertions | 0 | structured blocker syntax, identity, null target/imports, four undefined mutations, unchanged vector, exact change scope, recorded digests, and absent self-test agree |
| `git diff --check` plus per-added-file `git diff --no-index --check` | 0 aggregate | no whitespace diagnostics; each raw no-index command returned the expected new-file difference status 1 |
| `test ! -e .stage1-worker-selftest.json` | 0 | no self-test manifest exists because the exact-statement deliverable is blocked |

The intake checker is a historical intake-only validator. The integration lane changed the
authoritative intake item to provisional `[_]` after its receipt froze the earlier `[ ]` state, so
replay now stops at that state assertion. This statement attempt does not rewrite the intake
manifest, receipt, checker, task DAG, generated blueprint, or authoritative execution DAG to
manufacture freshness.

## Retry condition

The integration lane must master-accept refreshed intake evidence. Accountable reviewers must
then preserve and hash an immutable primary or approved authoritative source, select and
independently approve one exact proposition and complete proof boundary, and freeze every
incorporated definition, family, representative, parameter, exception, quotient, coincidence,
equivalence convention, Tits-group convention, binder, hypothesis, conclusion, correction,
erratum, and boundary case.

A later statement worker can then encode exactly that claim with real group constructions,
minimize its pinned imports, serialize and hash the elaborated expression and environment, compile
every credited transport, and run all four required mutation classes.

This is a blocked-attempt record, not completion of the statement node or any downstream node.
`audit_complete` and `theorem_complete` remain false. Because the assigned phase is not genuinely
self-tested to its completion gate, no `.stage1-worker-selftest.json`, node receipt, worker `[_]`,
or master acceptance is claimed.
