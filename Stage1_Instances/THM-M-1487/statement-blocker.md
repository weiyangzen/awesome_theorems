# THM-M-1487 exact-statement gate: blocked

- Item: `S56-M-1487-STATEMENT`
- Base revision: `04d551db74b7e1d7d9d261bba4727b3daf8a70d5` (tree
  `ee8a3d7a6c48598ca61028d71e21e0802ed968e1`)
- Attempt date: 2026-07-13 (Asia/Shanghai)
- Verdict: blocked; no statement receipt, worker `[_]`, or theorem-completion claim

## First failed gate

The exact-statement gate in section 5.1 of `Docs/Stage1_Blueprint_rev-5.6.md` cannot be
truthfully entered from the authoritative record. The mathematics catalog supplies only the title
"convolutional neural networks," Yann LeCun, 1989, and the gloss "neural networks for image
processing." It gives no cited truth-valued proposition, architecture, definitions, ordered
binders, hypotheses, conclusion, or boundary cases. Stage0 explicitly leaves the precise
definitions, premises, proof route, equivalent forms, axioms, machine status, and artifacts open.
The catalog's `已验证` value is untrusted metadata under rev-5.6.

The wording identifies a model and application family, not one theorem. It does not select a
LeNet or other architecture; an image, tensor, or spatial domain; discrete convolution versus
cross-correlation; indexing, padding, stride, dilation, or boundary conventions; activation,
pooling, readout, loss, or training semantics; or whether the conclusion concerns evaluation,
equivariance, approximation, optimization, generalization, robustness, complexity, or empirical
recognition performance. Those alternatives require materially different binders, hypotheses,
conclusions, arithmetic models, and degenerate cases. Selecting one from historical familiarity
would invent, narrow, broaden, or substitute mathematics rather than elaborate the received
target.

The inspected LeCun et al. 1989 article *Backpropagation Applied to Handwritten Zip Code
Recognition* is only a historical discovery lead. The catalog does not cite it, and the inspected
scan describes an architecture and empirical measurements rather than one exact analytical
theorem and proof matching the gloss. No immutable pinpoint proposition, complete incorporated-
definition and assumption crosswalk, correction record, or independent review has been admitted.

Consequently there is no canonical expression to elaborate, no honest minimal-import claim, and
no canonical expression or environment fingerprint. Checked transports and the required removed-
hypothesis, changed-domain, changed-binder-scope, and boundary-case mutations are undefined until
a source-correct proposition fixes the binders and premises. The intake vector remains
`[H5, M4, R4]`; no debt change is proposed. No `Statement.lean`, theorem declaration, axiom,
placeholder, stored desired property, or substituted theorem was introduced.

The intake prerequisite is only provisional `[_]`, and its worker receipt is unaccepted and not
content-addressed. Its recorded blueprint and execution-DAG hashes are older than the current
authority, and its historical checker expects intake `[ ]` with zero attempts rather than the
integrated `[_]` with one attempt. This independently prevents statement-node acceptance. This
phase records rather than rewrites stale intake evidence. The first statement-specific failure
remains the absent exact source proposition.

## Pinned Lean boundary

The existing `IntakeProbe.lean` was re-elaborated with the pinned environment. Its three imports
expose holors, finite matrix-vector operations, and one scalar sigmoid API. All ten `#check`
commands and three axiom reports passed, but the probe defines no CNN architecture, convolutional
layer, task, theorem, checked transport, or proof body. Its imports therefore cannot be certified
minimal for an unidentified target and receive no statement, anchor, or proof credit.

A bounded exact-topic search over the owned, repo-local, and pinned-mathlib Lean roots matched the
probe disclaimer and one mathlib terminology comment. It located no source-identical CNN target
declaration. This is narrow statement-feasibility evidence, not the downstream immutable anchor
audit or a global absence claim.

The environment is Lean 4.29.0 at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` (tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`). The automation-provided
`Formalizations/Lean/.lake` symlink points to the canonical pinned artifacts and was used read-only.
No `lake update`, `lake build`, dependency clone or fetch, or other `.lake` mutation was run.

## Validation evidence

Commands ran in this worker clone on 2026-07-13 (Asia/Shanghai), from the repository root unless a
different working directory is shown. Exact argument arrays and results are preserved in
`statement-blocker.json`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1487` | 0 | rank 1164, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| initial `git status --short --untracked-files=all` and `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| `python3 -B Stage1_Instances/THM-M-1487/check_intake.py` | 1 | historical intake replay reached its frozen `[ ]`/zero-attempt assertion; current authority records provisional `[_]`/one attempt |
| `cd Formalizations/Lean && lake env lean --version` and `lake --version` | 0 | Lean and Lake agree with the pinned environment above |
| mathlib revision/tree and package-status checks | 0 | revision and tree agree with the fingerprint; package worktree is clean |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-1487/IntakeProbe.lean` | 0 | ten adjacent APIs and three axiom reports elaborated; stdout SHA-256 `f13f0069714bc17f2203e7636ec663a2311bb3023a47e37c20978be4216f3a74`; no canonical target was stated |
| bounded exact-topic search recorded in `statement-blocker.json` | 0 | only the probe disclaimer and a holor terminology comment matched; no source-identical target declaration was found |
| prohibited Lean construct scan over owned `*.lean` files | 1 | expected no-match exit; no `sorry`, `admit`, `sorryAx`, axiom, bodyless declaration, or unsafe declaration |
| JSON, scoped invariant, final-newline, and whitespace checks recorded in `statement-blocker.json` | 0 | identity, null target, undefined mutations, unchanged debt, false completion flags, exact path scope, absent self-test, and clean formatting agree |
| `test ! -e .stage1-worker-selftest.json` | 0 | no worker self-test manifest exists because the exact-statement deliverable is blocked |

## Retry condition

The integration lane must first revalidate and master-accept refreshed intake evidence.
Accountable reviewers must then preserve and hash one immutable primary or approved authoritative
source, select and transcribe one exact truth-valued CNN proposition with pinpoint locators, audit
corrections and errata, reconcile neighboring-target ownership, and independently approve the
source-to-statement mapping. The decision must freeze the architecture, spatial and channel
domains, image and task model, convolution convention, parameters and arithmetic, activation and
pooling, training or statistical semantics when relevant, ordered binders, hypotheses, conclusion,
proof boundary, alternate encodings, and every degenerate or boundary case.

A later statement worker can then encode precisely that claim, minimize its pinned imports,
serialize and hash the elaborated expression and environment, compile every credited transport,
and run all four required mutation classes.

This is a blocked-attempt record, not completion of the statement node or any downstream node.
`audit_complete` and `theorem_complete` remain false. Because the assigned phase is not genuinely
self-tested to its completion gate, no `.stage1-worker-selftest.json`, node receipt, worker `[_]`,
or master acceptance is claimed.
