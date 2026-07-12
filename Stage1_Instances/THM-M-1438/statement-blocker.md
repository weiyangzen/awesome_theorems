# Exact-statement gate: blocked

Item: `S56-M-1438-STATEMENT`

Theorem: `THM-M-1438`

Base revision: `a8aba97a7ef2ff387e7814fe517e1b35524a04dc` (tree
`495e962862c2e7bc7c33c880c06fe39b2cb75db6`).

## Decision

The statement item remains `[ ]`. No exact Lean 4 target can be truthfully elaborated from the
authoritative repository record. That record supplies only the label `Lanford证明`, Oscar Lanford,
the year 1982, and the gloss `Feigenbaum猜想的计算机辅助证明`. It supplies no theorem number,
formula, incorporated definitions, ordered binders, hypotheses, or conclusion. The catalog status
`已验证` is untrusted metadata under rev-5.6.

Lanford's matching 1982 announcement is a multi-result source, not one theorem called "the Lanford
proof." It states inequivalent clauses: Theorem 1 gives an even analytic renormalization fixed
point with negative Schwarzian derivative; Theorem 3 gives derivative hyperbolicity with a
one-dimensional expanding subspace and positive expanding eigenvalue; Theorem 4 gives an
unstable-manifold iterate reaching the period-doubling bifurcation surface; and Theorem 5 gives a
transverse quadratic-family crossing of a stable manifold. Theorems 1 and 3 form the core derived
from the reported interval estimates, while the conjunction of Theorems 1, 3, 4, and 5 is a
strictly larger claim. The repository does not select any of these roots or another conjunction.

Choosing one silently would change the proposition, its analytic and dynamical domains, the
renormalization and scaling conventions, its quantifiers and conclusion, and the boundary between
mathematics and the interval-arithmetic computation. The source also says that a stronger
transversal version discussed immediately after Theorem 4 was not proved. It cannot be promoted
into the target. `THM-M-1437` (Feigenbaum universality) and `THM-M-1439` (Lyubich proof) are
separate repository targets and cannot substitute for this one.

The intake dependency has provisional worker state `[_]`, not master acceptance. More
substantively, its structured authority deliberately leaves the canonical human claim, Lean
module, declaration or expression, expression hash, and target environment fingerprint null at
`[H5, M4, R4]`. It requires accountable selection and independent review before a stable root
exists. The exact-source-statement identity gate therefore fails before minimal imports,
elaboration, alternate transports, or the required removed-hypothesis, changed-domain,
changed-binder-scope, and boundary-case mutations can be defined. These mutations are undefined,
not passed. No surrogate theorem, assumed interface, axiom, placeholder, weakened special case,
broadened target, computation result, or proof body was added.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` directly imports four pinned mathlib modules and successfully
re-elaborates eight adjacent interfaces for analyticity, fixed points, continuous linear maps,
compact operators, and spectra. It encodes neither Lanford's renormalization operator nor a
numbered source theorem. Its successful run is discovery-only substrate evidence; its imports
cannot be called minimal for an unknown target and receive no statement, anchor, computation, or
proof credit.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` link points to canonical pinned artifacts and was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, or other `.lake` mutation was run.

## Validation Evidence

Commands ran in this worker clone on 2026-07-13 (Asia/Shanghai).

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1438` | 0 | rank 936, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all; git rev-parse HEAD 'HEAD^{tree}'` | 0 | before statement edits, only the automation-provided `.lake` link was untracked; the recorded base revision and tree were otherwise clean |
| source record, Stage0, manifest, blueprint, and intake dossier inspection | 0 | the catalog contains only a proof-family label and gloss; the intake leaves the canonical claim and formal target null and lists inequivalent source roots |
| publisher PDF identity check using `file`, `wc -c`, `sha256sum`, and `pdfinfo` | 0 | PDF v1.2, 638627 bytes, 8 scan pages, SHA-256 `210cb7c561788fd8fab5fb2d5f7158619ef698a64fbb2ff0b5750185192ef045`; source suite identity agrees with intake evidence |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0 at the commit above |
| `cd Formalizations/Lean && lake --version` | 0 | Lake version above |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1438/IntakeProbe.lean` | 0 | eight adjacent APIs elaborated; no canonical target was stated |
| pinned mathlib revision, tree, and status inspection | 0 | revision and tree match the fingerprint above; package worktree clean |
| bounded Lanford/Feigenbaum/period-doubling/unimodal name search in repo-local and pinned mathlib Lean sources | 1 | expected no-match exit; discovery only, not an anchor audit |
| `python3 -B Stage1_Instances/THM-M-1438/check_intake.py` | 1 | known historical-receipt failure: the integrated blueprint hash differs from the intake worker's immutable input hash; its intake-only closed file inventory would also reject later statement artifacts, so intake evidence was not rewritten to manufacture agreement |
| prohibited proof-escape scan over `*.lean` source in `Stage1_Instances/THM-M-1438` | 1 | expected no-match exit; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration in owned Lean source |
| `python3 -m json.tool Stage1_Instances/THM-M-1438/statement-blocker.json` | 0 | structured blocker parsed as JSON |
| structured blocker invariant check | 0 | item and base identity, null target, four undefined mutations, unchanged `[H5, M4, R4]`, false completion flags, changed paths, and no-self-test boundary agree |
| scoped tracked and added-file whitespace checks | 0 | `git diff --check` and no-index checks produced no whitespace diagnostics |
| `test ! -e .stage1-worker-selftest.json` | 0 | no worker self-test manifest exists because the exact-statement completion gate is blocked |

## Retry Condition And Status Boundary

After the integration lane accepts the intake dependency, accountable and independent reviewers
must preserve one immutable primary or authoritative source, select and transcribe one exact
numbered theorem or conjunction with all incorporated definitions, hypotheses, conclusion, proof
and computation boundary, pagination and errata decisions, and degenerate cases, and approve its
relationship to `THM-M-1437` and `THM-M-1439`. A later statement worker can then encode that same
claim, minimize pinned imports, serialize and hash the elaborated expression and environment,
compile any alternate transports, and run all four required statement mutations.

The first failed gate is exact source-statement identity. The root remains `[H5, M4, R4]`, with
`audit_complete: false` and `theorem_complete: false`; no debt-vector change is proposed. This is
blocked-attempt evidence, not completion of the statement node or any downstream node. Because the
assigned phase is not genuinely self-tested to its completion gate, no
`.stage1-worker-selftest.json` is emitted and no statement receipt, worker `[_]`, or master
acceptance is claimed.
