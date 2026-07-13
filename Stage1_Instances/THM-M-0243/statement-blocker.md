# Exact-statement gate: blocked

Item: `S56-M-0243-STATEMENT`

Theorem: `THM-M-0243`

Base revision: `db6914155f1f63e835364b89ba0a3b25f1d7f936` (tree
`a5488edccb2687c4ff0bbdccf4650e06b2e45337`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-0243-INTAKE` has provisional worker
state `[_]`, not master-accepted state `[x]`. More importantly, the intake deliberately leaves the
canonical human claim and formal target null. The repository's complete claim is only
`伽马函数的特征刻画` ("characterization of the Gamma function"), together with the theorem name,
attribution, year, and an untrusted `已验证` label. It supplies no source work, edition, theorem or
page, incorporated definitions, ordered binders, hypotheses, conclusion, proof boundary, errata,
or independent source review.

The familiar Bohr-Mollerup family is identifiable, but proposition-changing choices remain open:

- a total `Real -> Real` function restricted to positive inputs versus an intrinsic positive-real
  domain and codomain;
- convexity of `log . f` versus a multiplicative log-convexity inequality, and the transport
  between them;
- explicit positivity versus positivity supplied by the codomain;
- the exact recurrence binder and domain, normalization, and equality domain; and
- a uniqueness implication versus unique existence or a two-sided characterization that also
  packages Gamma's existence-side properties.

The live secondary DLMF lead confirms a conventional uniqueness formulation, but it is not an
admitted immutable primary source and has no approved source-to-Lean crosswalk. Choosing that form,
or strengthening it to a two-sided package, would invent a root decision that the intake expressly
keeps open. Rev-5.6 section 5 makes statement ambiguity and a missing expression fingerprint hard
blockers. There is therefore no canonical target for which minimal imports, checked alternate
transports, or removed-hypothesis, changed-domain, changed-binder-scope, and boundary mutations can
be certified. Those mutation tests are undefined, not passed. The provisional vector remains
`[H1, M3, R4]`.

## Pinned Lean Boundary

Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` contains the exact-topic
module `Mathlib.Analysis.SpecialFunctions.Gamma.BohrMollerup` and declaration
`Real.eq_Gamma_of_log_convex`. Its checked type is the total-function uniqueness implication with
log-convexity, recurrence, positivity, and normalization hypotheses and `Set.EqOn` equality over
`Set.Ioi 0`. Adjacent declarations establish the corresponding properties of `Real.Gamma`.

`IntakeProbe.lean` re-elaborates these interfaces with the sole direct import above. Its two axiom
reports list `propext`, `Classical.choice`, and `Quot.sound`. This authenticates a pinned candidate
API only. It neither selects the source-faithful root nor supplies an expression fingerprint,
checked source transport, terminal proof-body audit, statement receipt, or proof credit. The
probe's import cannot be certified as the minimal import for an absent canonical target.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` symlink was used read-only. No `lake update`, `lake build`, dependency
clone or fetch, or other `.lake` mutation was run.

## Validation Record

Commands ran from this worker clone on 2026-07-13 (Asia/Shanghai).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0243` | 0 | rank 1253; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all` and `git rev-parse HEAD 'HEAD^{tree}'` | 0 | pre-edit status contained only the automation-provided `.lake` symlink; base revision and tree are recorded above |
| `git blame -L 1752,1757 -- Docs/researches/math_theorems.md` | 0 | all six sparse catalog fields originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| bounded exact-topic search in repo-local Lean, pinned mathlib, and this target | 0 | found the pinned Bohr-Mollerup module/declaration and no repo-local source-selected target or transport; discovery evidence only |
| `(cd Formalizations/Lean && lake env lean --version && lake env lake --version)` | 0 | Lean 4.29.0 and Lake 5.0.0 at the revisions above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and `status --short` | 0 | pinned mathlib revision and tree recorded above; package worktree clean |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0243/IntakeProbe.lean)` | 0 | six exact-topic Gamma APIs and two axiom reports elaborated; stdout SHA-256 `8d122b58946005336d4654abfad6b935c7b927d87f48a047e69de744ebbeb7e2` |
| `python3 -B Stage1_Instances/THM-M-0243/check_intake.py` | 1 | historical intake checker expects the pre-integration authoritative intake state `[ ]`; current authority records `[_]`; it was not rewritten as statement evidence |
| prohibited-construct scan over owned Lean files | 1 | expected no-match result: no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `python3 -m json.tool Stage1_Instances/THM-M-0243/statement-blocker.json` and scoped invariant check | 0 each | structured blocker parses; item identity, null target/imports, undefined mutations, unchanged vector, false completion flags, and absent self-test agree |
| scoped `git diff --check` and no-index checks for both new files | 0 / 1 each | no whitespace diagnostics; no-index exit 1 is the expected new-file difference |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest intentionally absent because the exact-statement deliverable did not pass |

The historical intake checker is frozen to intake-time authority and its original nine-file
artifact inventory. Integration has since changed the authoritative intake cursor from `[ ]` to
`[_]`, and this statement attempt adds two blocker files. Its fail-closed replay is recorded rather
than repaired by changing historical intake evidence.

## Retry Condition And Status Boundary

The integration lane must first master-accept refreshed intake evidence. Accountable reviewers
must preserve and hash an immutable primary or approved authoritative source, pinpoint its exact
statement and definition chain, select uniqueness versus two-sided packaging, fix the function
carrier, positivity and log-convexity encodings, recurrence and equality domains, ordered binders,
hypotheses, conclusion, boundary cases, proof boundary, corrections, and errata, and independently
approve the source-to-Lean component map.

A later statement worker can then encode exactly that reviewed claim, minimize its pinned imports,
serialize and hash its elaborated expression and environment, compile every credited transport,
and run all four required mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. Because the exact-statement
deliverable did not pass, no `.stage1-worker-selftest.json`, statement receipt, worker `[_]`, or
master acceptance is claimed.
