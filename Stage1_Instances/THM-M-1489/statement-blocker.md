# THM-M-1489 exact-statement gate: blocked

- Item: `S56-M-1489-STATEMENT`
- Base revision: `db6914155f1f63e835364b89ba0a3b25f1d7f936` (tree
  `a5488edccb2687c4ff0bbdccf4650e06b2e45337`)
- Attempt date: 2026-07-13 (Asia/Shanghai)
- Verdict: blocked; no statement receipt, worker `[_]`, or theorem-completion claim

## First failed gate

The exact-statement gate in section 5.1 of `Docs/Stage1_Blueprint_rev-5.6.md` cannot be
truthfully entered from the authoritative record. The mathematics catalog supplies only the title
`Transformer`, the attribution Vaswani et al., the year 2017, and the gloss "an
attention-mechanism neural network." It gives no cited truth-valued proposition, architecture,
definitions, ordered binders, hypotheses, conclusion, or boundary cases. Stage0 explicitly leaves
the precise definitions, premises, proof route, equivalent forms, axioms, formal system, machine
status, and artifacts open. The catalog's `已验证` value is untrusted metadata under rev-5.6.

The wording identifies an architecture family, not one theorem. It does not choose architecture
dimensions, index and scalar types, scaled-attention and softmax conventions, masking, positional
encoding, parameters, data or training semantics, arithmetic, or whether the conclusion concerns
well-formedness, an evaluation identity, normalization, causal masking, equivariance,
expressivity, complexity, optimization, generalization, robustness, or an empirical translation
result. These readings have materially different binders, assumptions, conclusions, computation
policies, and degenerate cases. Selecting one would invent, narrow, broaden, or substitute
proposition-changing mathematics rather than elaborate the received target.

The inspected Vaswani et al. 2017 proceedings paper *Attention Is All You Need* is only an intake
discovery lead. The catalog does not cite it or select one of its definitions, equations,
complexity observations, or empirical results as the target. No immutable pinpoint proposition,
complete incorporated-definition and assumption crosswalk, analytical proof boundary, correction
record, or independent review has been admitted.

Consequently there is no canonical expression to elaborate, no honest minimal-import claim, and
no canonical expression or environment fingerprint. Checked transports and the required removed-
hypothesis, changed-domain, changed-binder-scope, and boundary-case mutations are undefined until
a source-correct proposition fixes the binders and premises. The intake vector remains
`[H5, M4, R4]`; no debt change is proposed. `H5` classifies the received architecture-family gloss
as not yet a stable proposition and does not refute correctly stated Transformer theorems. No
`Statement.lean`, theorem declaration, axiom, placeholder, stored desired property, or substituted
theorem was introduced.

The intake prerequisite is only provisional `[_]`. Its worker receipt is unaccepted and not
content-addressed, contains no accepted receipt ID, and binds an older repository snapshot and
older blueprint and execution-DAG hashes. Its historical checker expects intake `[ ]` with zero
attempts, whereas the current execution DAG records `[_]` with one attempt. This phase records
rather than rewrites that stale intake evidence. The dependency state independently prevents
statement-node acceptance; the first statement-specific failure remains the absent exact source
proposition.

## Pinned Lean boundary

The existing `IntakeProbe.lean` was re-elaborated with the pinned environment. Its three direct
imports expose adjacent real exponential, real square-root, finite dot-product, and matrix APIs.
All ten `#check` commands and three axiom reports passed, but the probe defines no softmax,
attention evaluator, Transformer architecture, canonical theorem, checked transport, or proof
body. Its imports therefore cannot be certified minimal for an unidentified target and receive no
statement, anchor, or proof credit.

A bounded case-insensitive topic search over the owned path, repo-local Lean, and pinned mathlib
matched the probe disclaimer and unrelated uses of the programming term "transformer." It located
no source-identical softmax, self-attention, multi-head-attention, scaled-dot-product-attention,
Vaswani, or Transformer target declaration. This is narrow statement-feasibility evidence, not the
downstream immutable anchor audit or a global absence claim.

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
| `python3 scripts/stage1_target.py show THM-M-1489` | 0 | rank 1166, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| initial `git status --short --untracked-files=all` and `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| `python3 -B Stage1_Instances/THM-M-1489/check_intake.py` | 1 | historical intake replay reached its frozen `[ ]`/zero-attempt assertion; current authority records provisional `[_]`/one attempt |
| `cd Formalizations/Lean && lake env lean --version` and `lake --version` | 0 | Lean and Lake agree with the pinned environment above |
| mathlib revision/tree and package-status checks | 0 | revision and tree agree with the fingerprint; package worktree is clean |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-1489/IntakeProbe.lean` | 0 | ten adjacent APIs and three axiom reports elaborated; stdout SHA-256 `8c54753c7c0ca0c5526c12ba25f8a69133c315c628737c38672cdb9a152e0172`; no canonical target was stated |
| bounded exact-topic search recorded in `statement-blocker.json` | 0 | only the probe disclaimer and unrelated programming-term matches occurred; no source-identical target declaration was found |
| prohibited-construct scan over owned `*.lean` files | 1 | expected no-match exit; no `sorry`, `admit`, `sorryAx`, axiom, bodyless declaration, opaque declaration, or unsafe declaration |
| JSON, scoped invariant, final-newline, and whitespace checks recorded in `statement-blocker.json` | 0 | identity, null target, undefined mutations, unchanged debt, false completion flags, exact path scope, absent self-test, and clean formatting agree |
| `test ! -e .stage1-worker-selftest.json` | 0 | no worker self-test manifest exists because the exact-statement deliverable is blocked |

## Retry condition

The integration lane must first revalidate and master-accept refreshed intake evidence.
Accountable reviewers must then preserve and hash one immutable primary or approved authoritative
source, select and transcribe one exact truth-valued Transformer proposition with pinpoint
locators, audit corrections and errata, reconcile neighboring-target ownership, and independently
approve the source-to-statement mapping. The decision must freeze the architecture and dimensions;
query, key, value, token, sequence, head, and batch domains; attention, scaling, softmax, mask, and
positional semantics; parameters and arithmetic; data, training, or cost model when relevant;
ordered binders; hypotheses; conclusion; proof-versus-empirical boundary; alternate encodings; and
every degenerate case.

A later statement worker can then encode precisely that claim, minimize its pinned imports,
serialize and hash the elaborated expression and environment, compile every credited transport,
and run all four required mutation classes.

This is a blocked-attempt record, not completion of the statement node or any downstream node.
`audit_complete` and `theorem_complete` remain false. Because the assigned phase did not pass its
completion gate, no `.stage1-worker-selftest.json`, node receipt, worker `[_]`, proof credit, or
master acceptance is claimed.
