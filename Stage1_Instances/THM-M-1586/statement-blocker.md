# Exact-statement gate: blocked

Item: `S56-M-1586-STATEMENT`

Theorem: `THM-M-1586`

Base revision: `bd81d4853a030765585ef6fed4310484ceb1e458` (tree
`fb92fc7476bff9a2ce8c20f1d7be34c6655ca6b4`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-1586-INTAKE` has provisional worker
state `[_]`, not master-accepted state `[x]`. Rev-5.6 permits this dependency-ordered provisional
assessment, but master acceptance is still required before any later statement transition can be
accepted. The intake receipt is unsigned and non-content-addressed, declares `accepted: false`,
and records no accepted receipt ID.

Independently, the exact-statement gate cannot pass. The repository record supplies only the title
`Hamming界`, Richard Hamming, 1950, and the gloss `纠错码的球包装界` (the sphere-packing bound for
error-correcting codes). It supplies no formula, alphabet, code model, ordered binders,
hypotheses, conclusion, proof boundary, correction history, or boundary conventions. Stage0
repeats the gloss while explicitly leaving exact definitions and premises open. The catalog's
`已验证` label is untrusted under rev-5.6.

The intake correctly leaves the canonical mathematical and Lean targets null. The received
wording does not select among materially different roots:

- Hamming's historical binary-code inequality or a modern q-ary arbitrary-code inequality;
- a correction-radius statement or a minimum-distance statement with radius
  `floor ((d - 1) / 2)`;
- actual finite Hamming balls or the closed volume sum
  `sum choose(n,i) * (q - 1)^i`;
- arbitrary finite codes, linear codes, or an extremal function such as `A_q(n,d)`;
- a finite cardinality bound, linear dimension corollary, perfect-code equality case, or
  asymptotic rate bound.

Those choices change the proposition, as do the treatment of empty alphabets, `q = 1`, zero
length, empty and singleton codes, radius zero or greater than the length, natural subtraction,
strict versus weak separation, casts, rounding, and equality cases. Selecting the familiar
q-ary formula from general knowledge would be a broadened or substituted theorem, which the task
explicitly forbids. A binary statement cannot silently stand for the q-ary theorem, and a linear
corollary cannot silently stand for the arbitrary-code bound.

The intake identifies Hamming's 1950 paper as a credible article-level source lead, but it admits
no complete immutable primary text, pinpoint theorem or equation, incorporated definitions,
errata disposition, proof boundary, or independent source review. A fresh access check also found
the recorded repository scan still timed out; another guessed archive URL timed out, and the
available Bitsavers index does not carry volume 29. These observations do not choose a source
variant.

Sections 5 and 5.1 of the rev-5.6 blueprint make statement ambiguity and a missing expression
fingerprint hard blockers. There is therefore no honest expression for which minimal target
imports, a serialized elaborated-expression hash, checked alternate transports, or the required
removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case mutations can be
certified. Those mutation checks are undefined, not passed. The root vector remains
`[H1, M4, R4]`.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` successfully re-elaborates nine adjacent pinned interfaces:
Hamming distance, symmetry, the triangle inequality, its coordinate-cardinality bound, the
`Hamming` metric type and finite instance, its distance bridge, finite function-space cardinality,
and natural binomial coefficients. Its stdout is 1249 bytes with SHA-256
`f3773fe62e0132df4d9a9da795af55486f19f7a12cb886908e86e1699e6197f4`.

This is real substrate validation, but the probe defines no code object, minimum-distance
contract, Hamming ball, volume formula, canonical proposition, checked transport, or proof body.
Its imports cannot be called minimal for an absent target and receive no statement or proof
credit. A bounded exact-topic search found no Hamming-bound, Hamming-ball-code, or code-minimum-
distance declaration in pinned mathlib or repository-local Lean. Broader terms found only generic
Hamming and source-code documentation plus unrelated sphere-packing mentions. This is narrow
feasibility evidence, not the downstream anchor audit or a global absence claim.

As a non-credited feasibility check, the single direct import
`Mathlib.InformationTheory.Hamming` was sufficient to elaborate a scratch definition of the
usual q-ary volume sum and a candidate arbitrary-code packing proposition. That check shows the
candidate is representable in the pinned environment; it does not resolve which candidate the
repository owns, and the scratch proposition was not added as a target.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib
revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` symlink was used read-only. No update, build, clone, fetch, or other
dependency mutation was run.

## Validation Record

Commands ran from this isolated worker clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1586` | 0 | rank 1208; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` (pre-edit) | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| scoped source, Stage0, target-manifest, blueprint, execution-DAG, skill, guidelines, and intake-dossier inspection | 0 | confirmed the family-only gloss, null intake target, proposition-changing variants, boundary cases, and lack of an approved source-selected root |
| `sha256sum` over current authority, source, intake, toolchain, probe, and pinned-library inputs | 0 | exact current hashes are recorded in `statement-blocker.json`; historical intake hashes were not rewritten |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| pinned mathlib revision, tree, and package-status checks | 0 | revision and tree recorded above; package worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1586/IntakeProbe.lean` | 0 | nine adjacent APIs elaborated; stdout hash and byte count recorded above; no target or proof body |
| scratch stdin elaboration with only `import Mathlib.InformationTheory.Hamming` | 0 | the familiar q-ary volume and arbitrary-code candidate were representable; discriminator only, not a canonical or credited target |
| bounded Hamming-bound search in pinned mathlib and repo-local Lean | 1 expected | no exact Hamming-bound, ball-code, or code-minimum-distance declaration; discovery-only evidence |
| `python3 -B Stage1_Instances/THM-M-1586/check_intake.py` | 1 | historical replay stops at its stale pre-integration blueprint hash; this run records rather than rewrites the intake evidence |
| fresh source-access checks with `curl -L -I --max-time 20` | 28, 28, 0 | recorded NPS scan and guessed archive URL timed out; guessed Bitsavers volume URL returned HTTP 404; no primary text admitted |
| prohibited-construct scan over owned Lean files | 1 expected | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| scoped blocker JSON and semantic assertions | 0 | identity, dependency, null target/imports, unchanged vector, four undefined mutations, false completion flags, exact two-file scope, and absent self-test agree |
| `git diff --check` plus no-index checks for both new blocker files | 0 aggregate | no whitespace diagnostics; no-index exit 1 is only the expected added-file difference |

The intake checker freezes earlier authority bytes and its original nine-file inventory. The
integration commit subsequently changed the generated blueprint and execution DAG, and these new
statement artifacts intentionally extend the target directory. This statement run does not
rewrite the intake checker, receipt, instance, task DAG, generated blueprint, or authoritative
execution DAG to manufacture agreement.

## Retry Condition And Status Boundary

The integration lane must master-accept the intake before accepting a later statement transition.
Accountable reviewers must also preserve and hash an immutable primary or authoritative source,
select and independently approve one exact Hamming-bound result, reconcile the parallel catalog
row and neighboring targets, and transcribe every incorporated definition, ordered binder,
hypothesis, conclusion, proof boundary, correction, erratum, arithmetic convention, and boundary
case.

A fresh statement run can then encode precisely that source-selected claim, minimize pinned
imports, serialize and hash the elaborated expression and environment, compile every credited
transport, and execute all four required mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. Because the exact-statement
deliverable did not pass, no `.stage1-worker-selftest.json`, statement receipt, worker `[_]`, or
master acceptance is claimed.
