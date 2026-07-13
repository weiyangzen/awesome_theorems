# THM-M-0755 exact-statement gate: blocked

- Item: `S56-M-0755-STATEMENT`
- Base revision: `adc87f8ea24dcc7c5e2668c0a5ede0ca5c5f0f55` (tree
  `3c83596059f716cde0d50a5f6b390ada6ca7c8e1`)
- Attempt date: 2026-07-13 (Asia/Shanghai)
- Verdict: blocked; no statement receipt, worker `[_]`, or theorem-completion claim

## First failed gate

Section 5.1 of `Docs/Stage1_Blueprint_rev-5.6.md` requires an exact source-backed proposition before
a Lean target or minimal imports may be credited. The repository catalog supplies only the title
`解析层次` ("analytical hierarchy"), the attribution Stephen Kleene, the year 1955, and the gloss
`解析集合的层次` ("the hierarchy of analytical sets"). It gives no bibliography, definition,
ordered binders, hypotheses, truth-valued conclusion, proof boundary, correction history, or
independent target-identity review. Stage0 explicitly leaves the definitions and premises open,
and rev-5.6 treats the catalog's `已验证` label as untrusted metadata.

The intake identifies the lightface analytical hierarchy as the leading reading and records the
Spring 2024 Stanford Encyclopedia of Philosophy section 3.6.2 and Theorem 3.13 as an authoritative
secondary orientation. Its strictness theorem says, in one source-specific presentation, that for
each positive level a `Pi^1_n`-definable subset of the naturals exists which is not
`Sigma^1_n`-definable and is in neither class at any lower level, with a dual complement witness.
That is a strong candidate locator, not authority to replace the catalog's missing root. The Kleene
1955 papers listed in the intake are bibliographic leads only: no immutable primary theorem passage,
complete definition and assumption map, proof boundary, errata disposition, or independent review
has been admitted.

The unresolved choices change the proposition rather than merely its notation:

- lightface, relativized, or boldface scope, and standard second-order arithmetic versus a
  specified Polish-space setting;
- set variables over `Set Nat` versus function variables `Nat -> Nat`, the base arithmetic
  language, formula coding, satisfaction, free parameters, arity, and tuple coding;
- the level-zero, alternation, `Sigma`, `Pi`, and `Delta` conventions and whether classified objects
  are formulas, relations, predicates, subsets of naturals, or pointsets;
- definition or normal form, inclusions, strictness, completeness or universality, or the
  `Delta^1_1 = HYP` characterization as the exact conclusion;
- if strictness is intended, the positive-level binder, one or both witnesses, complement
  transport, same-level nonmembership, and lower-level exclusions; and
- level zero, zero arity, empty and full sets, parameters, complement universe, reducibility,
  extensional equality, foundation, TCB, and computation profiles.

Selecting the familiar strictness theorem would silently fix all of those conventions and could
also cross into separately cataloged hyperarithmetic or boldface projective targets. Introducing an
abstract hierarchy argument, structure field, hypothesis, axiom, or unsafe interface would assume
the missing mathematics rather than elaborate it. Consequently there is no canonical expression on
which to certify minimal imports, serialize an elaborated-expression fingerprint, compile alternate
transports, or run the required removed-hypothesis, changed-domain, changed-binder-scope, and
boundary-case mutations. Those tests are undefined, not passed. The root remains `[H5, M4, R4]`.

The execution DAG projects the intake dependency as provisional `[_]`; its worker receipt declares
`accepted: false` and has no accepted receipt ID. Dependency-ordered inspection is possible, but an
accepted statement transition would also require master-accepted intake evidence. The first
substantive blocker is the absent source-frozen proposition.

## Pinned Lean boundary

The existing `IntakeProbe.lean` was re-elaborated with its four direct imports:

- `Mathlib.Computability.Halting`
- `Mathlib.MeasureTheory.Constructions.Polish.Basic`
- `Mathlib.ModelTheory.Complexity`
- `Mathlib.SetTheory.Descriptive.Tree`

It checks twelve adjacent computability, powerset, first-order prenex, descriptive-tree, and
boldface analytic-set interfaces. The probe exited successfully, with stdout SHA-256
`a45ba6d4e66af527f230c0cba3b13d52ef84551a190ba57dd7af7e0ed70f76ef` and empty-stderr SHA-256
`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`. It declares no target,
transport, or proof body. In particular, `MeasureTheory.AnalyticSet` is a boldface notion and
`Descriptive.tree` is generic tree infrastructure; neither supplies Kleene's effective hierarchy.
The imports are therefore probe imports, not certified minimal imports for an unidentified target.

A bounded search over relevant pinned mathlib directories and the repo-local Lean project found no
exact-topic analytical-hierarchy declaration under the recorded terms. This is narrow feasibility
evidence only, not the downstream immutable anchor audit or a global absence claim. The scoped Lean
scan found no `sorry`, `admit`, `sorryAx`, axiom, constant, opaque declaration, or unsafe declaration
in the owned source.

The environment is Lean 4.29.0 at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` (tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`). The automation-provided canonical `.lake` symlink
was used read-only. No dependency update, build, clone, fetch, or other `.lake` mutation was run.

## Validation evidence

Commands ran in this worker clone on 2026-07-13 (Asia/Shanghai), from the repository root unless a
different working directory is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0755` | 0 | rank 1341; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| initial `git status --short --untracked-files=all` and `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree are recorded above |
| scoped reads of the blueprint, skill, guidelines, manifest, catalog, Stage0 record, and complete intake dossier | 0 | the repository supplies a topic family but no unique source proposition; intake deliberately leaves the canonical statement, target, imports, and fingerprints null |
| `git blame -L 5563,5568 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| pinned mathlib revision/tree and package-status checks | 0 | pinned revision and tree recorded above; mathlib package worktree clean |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0755/IntakeProbe.lean` | 0 | all twelve adjacent APIs elaborated; output hashes recorded above; no canonical target was declared |
| bounded analytical-hierarchy search over relevant pinned mathlib directories and repo-local Lean | 1 (expected) | no exact-topic declaration matched; this is not an exhaustive anchor audit or global absence claim |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0755-pycache python3 -m py_compile Stage1_Instances/THM-M-0755/check_intake.py` | 0 | historical intake checker syntax compiled without creating an owned generated file |
| `python3 -B Stage1_Instances/THM-M-0755/check_intake.py` | 0 | historical intake invariant check passed before statement artifacts were added |
| scoped prohibited-construct scan over owned Lean files | 1 (expected no match) | no prohibited Lean declaration or escape hatch found |
| `python3 -m json.tool Stage1_Instances/THM-M-0755/statement-blocker.json` and scoped blocker assertions | 0 | structured syntax, identity, null target/imports/hashes, four undefined mutations, unchanged vector, false completion flags, recorded input hashes, and absent self-test agree |
| `git diff --check` plus per-added-file `git diff --no-index --check` | 0 aggregate | no whitespace diagnostics; each raw no-index command returned only its expected new-file difference status 1 |
| `test ! -e .stage1-worker-selftest.json` | 0 | no self-test manifest exists because the exact-statement deliverable did not pass |

The intake validator is phase-local historical evidence: it freezes the original nine-file intake
inventory. Adding statement-phase artifacts makes it inapplicable to final directory replay, so
this attempt records the pre-artifact pass rather than changing the historical checker, receipt,
task DAG, generated blueprint, or authoritative execution DAG to manufacture a statement success.

## Retry condition

The integration lane must first master-accept the intake. Accountable reviewers must then lawfully
preserve and hash an immutable primary or approved authoritative source, select and independently
approve one exact proposition, and map every incorporated definition, ordered binder, hypothesis,
conclusion, proof boundary, correction, erratum, and boundary convention. That review must freeze
the lightface/relativized/boldface scope, syntax and standard-model semantics, number/set/function
variables, codings and parameters, hierarchy indexing, classified objects, exact theorem variant,
foundation profiles, alternate encodings, and all degenerate cases.

A fresh statement run can then encode only that approved claim, establish minimal pinned imports,
serialize and hash the elaborated expression and environment, compile every credited transport,
and run all four mutation classes. Until then this node remains `[ ]`; `audit_complete` and
`theorem_complete` are false. Because the assigned phase did not pass its completion gate, no
`.stage1-worker-selftest.json`, statement receipt, worker `[_]`, proof credit, or master acceptance
is claimed.
