# THM-M-0744 exact-statement gate: blocked

- Item: `S56-M-0744-STATEMENT`
- Base revision: `1c0c5fc6f43e6ae5ecc3b50589b45c3628e0ead4` (tree
  `61214aa2a03c032134ddc4958b1df63df3430a85`)
- Attempt date: 2026-07-13 (Asia/Shanghai)
- Verdict: blocked; no statement receipt, worker `[_]`, or theorem-completion claim

## First failed gate

The exact-statement gate in section 5.1 of `Docs/Stage1_Blueprint_rev-5.6.md` cannot be truthfully
completed from the authoritative repository record. The record supplies only the title
`s-m-n定理`, Stephen Kleene, 1943, and the gloss `参数定理` (parameter theorem). It supplies no
formula, bibliography, result locator, acceptable-numbering convention, arities, tuple encoding,
ordered binders, hypotheses, conclusion, proof boundary, correction history, or independent
review. Stage0 explicitly leaves the precise definitions and premises open, and rev-5.6 treats the
catalog's `已验证` label as untrusted metadata.

The intake identifies an exact secondary-source formulation and a strong pinned Lean candidate,
but they do not resolve the target:

- the Spring 2024 Stanford Encyclopedia archive, section 3.1, Theorem 3.1, states that for every
  pair of arities `n,m` there is a primitive-recursive natural-index transformer specializing the
  first `m` arguments of every indexed `(n+m)`-ary partial computable function;
- the catalog's Kleene 1943 attribution leads to *Recursive Predicates and Quantifiers*, but only
  bibliographic metadata was accepted at intake; the version-of-record request returned HTTP 429,
  and no primary theorem passage, incorporated definitions, proof, corrections, or errata were
  inspected; and
- pinned `Nat.Partrec.Code.smn` instead gives a packed unary theorem over an inductive `Code`: it
  existentially produces `f : Code -> Nat -> Code`, exposes only `Computable2 f`, and proves
  pointwise equality after pairing one fixed natural with one residual input. The separately
  checked witness `Nat.Partrec.Code.curry` is primitive recursive, but that stronger fact is not
  the effectiveness assertion in `smn`'s proposition.

The repository does not select the general natural-index theorem or the packed unary Code theorem,
nor does it provide checked arity, tuple/pair, natural-index/Code, primitive-recursive/computable,
and semantic-equality transports between them. The outside-Stage1 duplicate `THM-C-0005` adds only
that a computable function combines a program index and parameters; it still supplies no exact
formula or transferable statement authority. Selecting `Nat.Partrec.Code.smn` merely because
mathlib labels it the S-n-m theorem would therefore substitute unresolved encoding and strength
choices rather than elaborate the exact received target.

Consequently there is no canonical expression on which to certify minimal imports, preserve an
elaborated-expression fingerprint, compile credited alternate transports, or run the required
removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case mutations. Those tests
are undefined, not passed. The root remains `[H1, M4, R4]`.

The execution DAG projects the intake dependency as provisional `[_]`, but its worker receipt
declares `accepted: false`, is not content-addressed, and contains no accepted receipt ID. This
dependency-ordered attempt records the independent substantive blocker; eventual statement
acceptance also requires master-accepted intake evidence.

## Pinned Lean boundary

The existing discovery-only `IntakeProbe.lean` was re-elaborated using the sole direct import
`Mathlib.Computability.PartrecCode`. It checks `Code`, `curry`, `eval`, `Computable2`, `Primrec2`,
`primrec2_curry`, `eval_curry`, and `smn`, then reports `smn`'s axioms as `propext`,
`Classical.choice`, and `Quot.sound`. It declares no canonical target or wrapper. Successful probe
elaboration is candidate-feasibility evidence only: its import is not a certified minimal import
for the unidentified target, and neither upstream declaration receives statement or proof credit.

A bounded search over pinned mathlib, shared Lean source, and this dossier found the upstream `smn`
declaration and no repo-local canonical wrapper. This is narrow feasibility evidence, not the
downstream immutable anchor audit or a global absence claim. The scoped Lean scan found no `sorry`,
`admit`, `sorryAx`, axiom, bodyless declaration, opaque declaration, or unsafe declaration in the
owned Lean source.

The environment is Lean 4.29.0 at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` (tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`). The automation-provided canonical `.lake` symlink
was used read-only. No `lake update`, `lake build`, dependency clone or fetch, or other `.lake`
mutation was run.

## Validation evidence

Commands ran in this worker clone on 2026-07-13 (Asia/Shanghai), from the repository root unless a
different working directory is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0744` | 0 | rank 1331; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| initial `git status --short --untracked-files=all` and `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree are recorded above |
| scoped reads of the blueprint, skill, guidelines, manifest, execution DAG, catalogs, Stage0 records, and complete intake dossier | 0 | the source identifies the parameter-theorem family but supplies no binder-complete proposition; intake deliberately leaves the canonical statement, binders, imports, and fingerprints null |
| `git blame -L 5486,5491 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| current authority, source, intake, toolchain, lockfile, probe, and pinned-source SHA-256 checks | 0 | exact input digests are recorded in `statement-blocker.json` |
| `python3 -B Stage1_Instances/THM-M-0744/check_intake.py` before adding blocker artifacts | 0 | historical intake invariants passed for the original nine-file dossier; the checker freezes that inventory and becomes stale after this phase adds two owned artifacts |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}' 'HEAD:Mathlib/Computability/PartrecCode.lean'` and package status | 0 | pinned mathlib revision, tree, and source blob recorded in the JSON blocker; package worktree clean |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0744/IntakeProbe.lean` | 0 | eight interfaces or candidates and one axiom report elaborated; output 865 bytes, 11 lines, SHA-256 `05d134eb92270ea95c2d7f2e43733cf196ed80a3275a9da8089693f5eeeba511`; no canonical target was declared |
| bounded `smn` declaration search in pinned mathlib, shared Lean source, and this dossier | 0 | confirmed the pinned candidate and no repo-local target wrapper; this is not an exhaustive anchor audit |
| scoped prohibited-construct scan over `Stage1_Instances/THM-M-0744/*.lean` | 1 | expected no-match exit; no prohibited Lean declaration or escape hatch found |
| `python3 -m json.tool Stage1_Instances/THM-M-0744/statement-blocker.json` and scoped blocker assertions | 0 | structured blocker syntax, identity, null target/imports/hashes, four undefined mutations, unchanged vector, false completion flags, exact two-file scope, and absent self-test agree; publication-byte hygiene also passed |
| `git diff --check` plus per-added-file `git diff --no-index --check` | 0 aggregate | no whitespace diagnostics; each raw no-index command returned the expected new-file difference status 1 |
| `test ! -e .stage1-worker-selftest.json` | 0 | no self-test manifest exists because the exact-statement deliverable did not pass |

The intake validator is phase-local historical evidence: it freezes the original nine-file intake
inventory. Adding these statement-phase artifacts expands the target directory, so a final replay
is expected to fail at that inventory assertion. This attempt records the known phase-evolution
failure rather than changing the intake checker, receipt, task DAG, generated blueprint, or
authoritative execution DAG to manufacture freshness.

## Retry condition

The integration lane must master-accept refreshed intake evidence. Accountable reviewers must then
preserve and hash an immutable primary or approved authoritative source, pinpoint the exact s-m-n
result and every incorporated definition and assumption, audit corrections and errata, and
independently approve its mapping and ownership relationship with `THM-C-0005`. That selection must
freeze the numbering or Code model, arities, tuple and pairing convention, transformer strength,
ordered binders, semantic-equality convention, exact conclusion, foundations, checked alternate
transports, and all boundary cases.

A fresh statement run can then encode precisely that claim, establish minimal pinned imports,
serialize and hash the elaborated expression and environment, compile every credited transport,
and run all four required mutation classes. Until then this node remains `[ ]`; `audit_complete`
and `theorem_complete` are false. Because the assigned phase did not pass its completion gate, no
`.stage1-worker-selftest.json`, statement receipt, worker `[_]`, proof credit, or master acceptance
is claimed.
