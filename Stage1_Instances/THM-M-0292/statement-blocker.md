# THM-M-0292 exact-statement gate: blocked

- Item: `S56-M-0292-STATEMENT`
- Base revision: `f023dbc3411d83201065d1a1156d7406b81135d4` (tree
  `3b3a73ec19293a2a9b8d9c7e67f0d25da2a511b4`)
- Attempt date: 2026-07-13 (Asia/Shanghai)
- Verdict: blocked; no statement receipt, worker `[_]`, or theorem-completion claim

## First failed gate

The exact-statement gate in sections 5 and 5.1 of
`Docs/Stage1_Blueprint_rev-5.6.md` cannot be truthfully entered from the authoritative record.
The mathematics catalog supplies only the name Dini's theorem, Ulisse Dini, the year 1878, and the
gloss `单调函数列的一致收敛` (uniform convergence of a monotone sequence of functions). It gives no
citation, formula, incorporated definitions, ordered binders, hypotheses, conclusion, or boundary
cases. Stage0 repeats the gloss while explicitly leaving precise definitions, premises, alternate
forms, axioms, machine status, and artifacts open. The catalog's `已验证` value is untrusted metadata
under rev-5.6.

This wording identifies the classical Dini uniform-convergence family but does not identify one
exact proposition. In particular, it does not select:

- a compact topological space, a compact subset, or a closed real interval;
- an increasing sequence, a decreasing sequence, or a conjunction of both directions;
- monotonicity in the sequence index rather than monotonicity of each function in its argument;
- natural-number or generalized preorder indexing, and real or generalized ordered-lattice values;
- the precise continuity and pointwise-convergence premises; or
- `TendstoUniformly`, `TendstoUniformlyOn`, a continuous-map topology, or an epsilon/supremum
  conclusion.

The intake located Dini's 1878 book but did not identify and independently review an exact original
theorem, definition chain, page span, proof, translation, corrections, or errata. Its inspected
secondary source states a nonnegative-series theorem on a closed interval. Treating that as the
catalog root would additionally require a checked, source-approved transport through partial sums,
increments, indexing, continuity, and the meaning of uniform convergence. The intake therefore
deliberately leaves `canonical_statement`, `canonical_claim`, the Lean module and expression, and
their fingerprints null. Selecting one familiar variant now would invent, narrow, broaden, or
substitute proposition-changing mathematics.

Consequently there is no canonical expression to elaborate and no honest minimal-import claim.
Checked alternate transports and the required removed-hypothesis, changed-domain,
changed-binder-scope, and boundary-case mutations are undefined until a source-correct proposition
fixes its binders and premises. The lifecycle remains `planned`, the vector remains
`[H1, M3, R4]`, and no debt change is proposed. No `Statement.lean`, axiom, placeholder, assumed
convergence, or substituted theorem was introduced.

The prerequisite `S56-M-0292-INTAKE` is also only provisional `[_]`. Its receipt declares
`accepted: false`, and the instance contains no accepted receipt ID. This independently prevents
statement-node acceptance. The first substantive failure in this attempt is the absent exact
source proposition and approved source-to-target selection.

## Pinned Lean boundary

The existing `IntakeProbe.lean` was re-elaborated with the pinned environment and its single import,
`Mathlib.Topology.UniformSpace.Dini`. The increasing and decreasing locally uniform, compact-space,
compact-set, and continuous-map interfaces all elaborate. Two classical `Nat`/`Real` compact-set
specializations also elaborate. This proves that strong formal candidates are available; it does
not select either specialization as the exact root, prove import minimality for an unidentified
root, or provide statement or proof credit.

A bounded repo-local and pinned exact-module search located these Dini declarations and no
repo-local Dini theorem. This is feasibility evidence only, not the downstream immutable anchor
audit or a global absence claim.

The environment is Lean 4.29.0 at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` (tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`). The automation-provided
`Formalizations/Lean/.lake` symlink points to the canonical pinned artifacts and was used read-only.
No `lake update`, `lake build`, dependency clone or fetch, or other `.lake` mutation was run.

## Validation evidence

Commands ran in this worker clone on 2026-07-13 (Asia/Shanghai), from the repository root unless a
different working directory is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0292` | 0 | rank 1542; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| initial `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree are recorded above |
| catalog, Stage0, blueprint, skill, manifest, and complete intake-dossier inspection | 0 | confirmed a family-level gloss, null canonical target, and the proposition-changing choices listed above |
| exact `sha256sum` command recorded in `statement-blocker.json` | 0 | current authority, source, intake, toolchain, lockfile, probe, and pinned Dini-source fingerprints were captured |
| `python3 -B Stage1_Instances/THM-M-0292/check_intake.py` | 0 before blocker creation; 1 after | the historical intake snapshot initially passed with vector `H1/M3/R4` and six open tasks; after these two files were added it rejects the expanded owned-file inventory, so this phase records rather than rewrites intake evidence |
| `cd Formalizations/Lean && lake env lean --version`; `lake --version` | 0 | pinned Lean and Lake identities recorded above |
| pinned mathlib `git rev-parse HEAD 'HEAD^{tree}'`; `git status --short` | 0 | revision and tree agree; package worktree is clean |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0292/IntakeProbe.lean` | 0 | eight pinned Dini interfaces and two classical compact-set specializations elaborated; 34 lines, 3714 bytes, stdout SHA-256 `9c8e4610...59133`; no canonical target or proof body |
| bounded exact-topic `rg` over repo-local Lean and the pinned Dini module | 0 | found the pinned Dini interfaces and no repo-local Dini theorem; bounded discovery only |
| prohibited Lean-construct scan over the owned target | 1 | expected no-match; no `sorry`, `admit`, `sorryAx`, axiom, bodyless declaration, opaque declaration, or unsafe declaration |
| `python3 -m json.tool Stage1_Instances/THM-M-0292/statement-blocker.json` | 0 | structured blocker parses as valid JSON |
| scoped invariant check recorded in `statement-blocker.json` | 0 | identity, open blocked state, null target and imports, unchanged vector, undefined mutations, exact path scope, and absent self-test agree |
| scoped `git diff --check` and per-new-file no-index checks | 0 | no whitespace diagnostics |
| `test ! -e .stage1-worker-selftest.json` | 0 | no worker self-test manifest exists because the exact-statement deliverable is blocked |

## Retry condition

The integration lane must master-accept refreshed intake evidence. Accountable reviewers must then
preserve and hash one immutable primary or approved authoritative source, transcribe and
independently approve one exact truth-valued proposition and all incorporated definitions with
pinpoint locators, and audit its proof boundary, translation, corrections, and errata. The decision
must freeze the domain and compactness form, index monotonicity and direction, index and codomain,
continuity and pointwise-convergence premises, conclusion encoding, ordered binders, and every
degenerate or boundary case. Any series formulation also needs an approved checked transport to the
selected monotone-sequence root.

A later statement worker can then encode precisely that claim, minimize its pinned imports,
serialize and hash the elaborated expression and environment, compile every credited transport,
and run all four required mutation classes.

This is a blocked-attempt record, not completion of the statement node or any downstream node.
`audit_complete` and `theorem_complete` remain false. Because the assigned phase is not genuinely
self-tested to its completion gate, no `.stage1-worker-selftest.json`, node receipt, worker `[_]`,
or master acceptance is claimed.
