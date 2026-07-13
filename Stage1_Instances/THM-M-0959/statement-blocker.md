# THM-M-0959 exact-statement gate: blocked

Item: `S56-M-0959-STATEMENT`

Base revision: `5fe11f4b5e32a06ffb4432460319fc8ae906fe7b` (tree
`64c5aacf7cf3eb79008f5a1970151e3e53cb9966`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-0959-INTAKE` has provisional worker
state `[_]`, not master-accepted state `[x]`. The intake receipt has `accepted: false`, is not
content-addressed, and contains no accepted receipt ID. It is also tied to an earlier repository
snapshot and earlier blueprint and execution-DAG hashes. Its historical validator expects the old
authoritative intake state `[ ]` and no longer replays after integration changed that state to
`[_]`. Rev-5.6 section 10.2 permits preparation of this later-node blocker, but master closure
remains dependency ordered.

Independently and decisively, the exact-statement gate cannot pass. The complete repository record
is the label `Croot-Lev-Pach方法`, its author/year metadata, and the gloss "application of the
polynomial method to the cap-set problem." That wording names a method and an application, not one
truth-valued proposition. It supplies no formula, numbered-result locator, ordered binders,
hypotheses, conclusion, proof-provenance boundary, correction policy, erratum review, or independent
statement approval. Stage0 explicitly leaves the exact definitions and premises open, and
rev-5.6 treats the catalog's `已验证` label as untrusted metadata.

The matching primary paper, Croot, Lev, and Pach, *Progression-free sets in Z_4^n are exponentially
small*, contains several materially different candidate roots:

- Theorem 1, the `4^(gamma*n)` upper bound for progression-free subsets of `Z_4^n`;
- Corollary 1, a finite-abelian-group bound involving the number of invariant factors divisible by
  four;
- Lemma 1, the multilinear-polynomial off-diagonal vanishing lemma;
- Proposition 1, the rich-coset bound used in the main proof; or
- a provenance-sensitive method package requiring the polynomial lemma, entropy estimate, coset
  argument, integral estimate, tensor-power step, and checked composition to a selected root.

The repository selects none of these. The phrase "cap-set problem" also does not authorize
substitution of the neighboring Ellenberg-Gijswijt theorem over `F_3^n` or `F_q^n`. The source's
pairwise-distinct progression predicate is not equivalent to mathlib's stronger `ThreeAPFree` in
exponent four, and the source's base-two entropy is not definitionally the natural-log
`Real.binEntropy` API. Selecting a familiar theorem or silently changing either convention would
invent, narrow, broaden, or substitute proposition-changing mathematics.

Sections 5 and 5.1 make statement ambiguity and a missing expression fingerprint hard blockers.
There is no canonical Lean expression whose imports can be minimized, no serialized elaborated
expression or canonical-target environment fingerprint, and no credited alternate transport.
Removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case mutations are undefined,
not passed. No `Statement.lean`, theorem declaration, proof body, weakened special case, or
broadened interface was added. The provisional root remains `[H5, M4, R4]`.

## Source And Lean Boundary

The intake observed the governing publisher PDF at SHA-256
`9829dbcdb774826379ba2c98f62cc4267ca8d0e24ad7a89f596bcc2c5c224b3e`. Theorem 1 is on printed
page 332, and its proof and tensor-power step are on printed pages 335-336. The publication improves
the factor-bearing arXiv v1 bound, while arXiv v2 contains an intermediate `2^(gamma*n)` typo that
the published page 335 prints as `4^(gamma*n)`. These source observations identify candidates and
a correction boundary; the source is not vendored, independently admitted, or selected as the
canonical claim.

The existing `IntakeProbe.lean` re-elaborates four direct pinned imports and eight adjacent APIs:
`ThreeAPFree`, product preservation, finite product cardinality, `ZMod`, and natural-log binary
entropy. They provide substrate only. The probe declares no CLP target, source-predicate transport,
entropy normalization, polynomial lemma, coset estimate, exponential upper bound, or proof body.
Those imports therefore cannot be certified minimal for an absent target and receive no statement
or proof credit.

A bounded exact-topic search over repo-local Lean and pinned mathlib found no source-selected CLP
terminal declaration. This is narrow feasibility evidence, not the downstream anchor audit or a
global absence claim.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib
revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided canonical `.lake` symlink
was used read-only. No `lake update`, `lake build`, dependency clone or fetch, or other `.lake`
mutation was run.

## Validation Record

Commands ran from this isolated worker clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0959` | 0 | rank 1493; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| pre-edit `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| `jq` projections of the manifest, execution DAG, `instance.json`, and intake receipt, followed by the exact Python invariant script recorded in the structured blocker | 0 | intake is `[_]`, statement is `[ ]`, the root is H5/M4/R4, and the canonical claim plus target module, expression, expression hash, and canonical environment fingerprint are null; only discovery import candidates exist |
| `git blame -L 7001,7006 -- Docs/researches/math_theorems.md` | 0 | all six sparse catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `python3 -B Stage1_Instances/THM-M-0959/check_intake.py` | 1 | historical intake replay stops because it expects authoritative intake state `[ ]`, while integration records `[_]`; this phase records rather than rewrites stale intake evidence |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| `cd Formalizations/Lean/.lake/packages/mathlib && git rev-parse HEAD 'HEAD^{tree}' && git status --short` | 0 | revision and tree recorded above; package worktree clean |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0959/IntakeProbe.lean` | 0 | eight adjacent APIs elaborated; stdout SHA-256 `f5a4843fc8b1c60daf2a405ae8f28a656c8d412bc7739bfa2e72fb41ad9f90f7`; no canonical target was declared |
| bounded exact-topic `rg` over repo-local Lean, pinned mathlib, and this dossier | 0 | only the owned probe disclaimer matched; no source-selected terminal declaration was located; output SHA-256 `4f8a11183a3cdf78d78bc96e8cb21c59b7817d1cb990e2cd5da7eeb32beaac58` |

Final JSON parsing, scoped invariant checks, placeholder/declaration scanning, tracked and no-index
whitespace checks, and the absent-self-test check are recorded in the structured blocker beside this
report.

## Retry Condition

The integration lane must first master-accept refreshed intake evidence. Accountable reviewers must
preserve and admit an immutable source edition, select and independently approve exactly one
numbered result or provenance-sensitive package, and map every incorporated definition, binder,
premise, conclusion, proof boundary, correction, and erratum. They must also freeze the ambient
group, progression predicate, entropy normalization, `gamma` optimization, cardinality and real
power conventions, product representation, neighboring-target boundary, and every degenerate case.

A fresh statement worker can then encode exactly that reviewed claim, minimize its pinned imports,
serialize and hash the elaborated expression and environment, compile every credited transport, and
run all four required mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. Because the exact-statement
deliverable did not pass, no `.stage1-worker-selftest.json`, statement receipt, worker `[_]`, proof
credit, or master acceptance is claimed.
