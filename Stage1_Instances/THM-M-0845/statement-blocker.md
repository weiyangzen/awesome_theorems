# THM-M-0845 exact-statement gate: blocked

- Item: `S56-M-0845-STATEMENT`
- Base revision: `fcabbf1e0ad9507eebe91663bccabfa87d22813e`
- Base tree: `873e589c594454b7f263c7ed2342089a4d15e842`
- Attempt date: 2026-07-13 (`Asia/Shanghai`)
- Verdict: blocked; no statement receipt, worker `[_]`, or theorem-completion claim

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the authoritative repository record.
The complete received wording is the label `图同态计数` (graph homomorphism counting), collective
attribution to many mathematicians, the twentieth century, and the gloss `子图同态的计数`
(literally "counting of subgraph homomorphisms"). The catalog supplies no citation, definition,
ordered binder, hypothesis, conclusion, proof boundary, correction, erratum, reviewer, or formal
declaration. Its `已验证` label is untrusted metadata under rev-5.6.

The intake correctly freezes a topic family, not a proposition. The inspected survey *Counting
Graph Homomorphisms* distinguishes materially different candidates:

- the natural number `hom(F,G)` of adjacency-preserving maps;
- the normalized density `t(F,G)`;
- weighted homomorphism sums and partition functions;
- ordinary, injective, induced, and surjective counts and their conversion identities;
- disjoint-union, product, and inequality results;
- hom-profile and graph-parameter characterization theorems;
- graph-limit, metric, testing, and extremal results; and
- algorithmic or complexity classifications.

The Chinese word `子图` also does not decide whether the intended maps are ordinary
homomorphisms, injective embeddings, or induced copies. The repository fixes no graph class, map
convention, count or normalization, coefficient domain, ordered binders, hypotheses, conclusion,
or boundary cases. Choosing a familiar result would invent, narrow, broaden, or substitute
proposition-changing mathematics rather than elaborate the received target.

Sections 5 and 5.1 of the rev-5.6 blueprint make statement ambiguity and a missing elaborated
expression fingerprint hard blockers. The intake therefore leaves `canonical_statement`,
`canonical_claim`, the Lean module and expression, target imports, expression hash, and
canonical-target environment fingerprint null at `[H5, M4, R4]`. Consequently, minimal target
imports, credited alternate transports, and the required removed-hypothesis, changed-domain,
changed-binder-scope, and boundary-case mutations are undefined, not passed. No `Statement.lean`,
axiom, placeholder, raw-cardinality substitute, weakened example, or broadened theorem was added.

The prerequisite `S56-M-0845-INTAKE` is only provisional worker state `[_]`. Its receipt is
explicitly unaccepted and non-content-addressed, supplies no accepted receipt ID, and has no master
acceptance. Rev-5.6 section 10.2 permits preparation of a provisional later-node blocker in stable
topological order, but this dependency independently prevents accepted statement closure.

## Pinned Lean Boundary

The existing discovery-only `IntakeProbe.lean` re-elaborates with two direct imports,
`Mathlib.Combinatorics.SimpleGraph.Maps` and `Mathlib.Data.Fintype.Pi`. It authenticates
`SimpleGraph.Hom`, `Embedding`, `Iso`, homomorphism composition, the finite relation-hom instance,
and `Fintype.card`; it also synthesizes a finite type of graph homomorphisms under finite decidable
graph assumptions.

The probe declares no graph-homomorphism-count proposition, source transport, or proof body. Even
the cardinality expression is a natural-number term, not a truth-valued theorem. Its imports therefore
cannot be certified as minimal imports for an absent target and receive no statement or proof
credit. A bounded exact-topic search over repository-local and pinned-mathlib Lean sources returned
no named general graph-homomorphism-count or density declaration. This is discovery-only evidence,
not the downstream immutable anchor audit or a global absence claim.

The pinned environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The probe's complete output SHA-256 is
`1232bd8bb9229894e0278d5f7553a78785f0f3435095be419cabe9a50636c209`.

The automation-provided `Formalizations/Lean/.lake` symlink points to canonical pinned artifacts
and was used read-only. No `lake update`, `lake build`, dependency clone or fetch, or other `.lake`
mutation was run.

## Validation Evidence

Commands ran in this worker clone on 2026-07-13 (`Asia/Shanghai`). Lean commands ran from
`Formalizations/Lean`; all others ran from the repository root unless noted. Exact arguments,
exits, result summaries, and current input fingerprints are also preserved in
`statement-blocker.json`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and execution-skill presence passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0845` | 0 | rank 1400, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| pre-edit `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| scoped reads of the standard, skill, target manifest, catalog, Stage0 projection, execution DAG, and complete intake dossier | 0 | confirmed provisional intake, a null canonical target, and unresolved proposition-changing choices |
| current `sha256sum` over authority, source, intake, probe, toolchain, lockfile, and relevant mathlib sources | 0 | exact digests are recorded in the structured blocker |
| pinned Lean, Lake, mathlib revision/tree, and package-status checks | 0 | expected versions and clean pinned mathlib worktree passed |
| `lake env lean ../../Stage1_Instances/THM-M-0845/IntakeProbe.lean` | 0 | adjacent graph-map and finite-cardinality APIs elaborated; output hash above; no target or proof body was declared |
| bounded exact-topic search in pinned mathlib and repository-local Lean | 1 expected | no named general count or homomorphism-density occurrence; discovery only |
| `python3 -B Stage1_Instances/THM-M-0845/check_intake.py` | 1 | the historical checker freezes the pre-integration intake state `[ ]`; the current execution DAG records `[_]`, so this phase records rather than rewrites historical evidence |
| prohibited-construct scan over owned Lean | 1 expected | no `sorry`, `admit`, `sorryAx`, axiom, constant, opaque, or unsafe declaration |
| JSON parse, scoped blocker invariants, structural replays, and whitespace checks | 0 | blocker identity, null target/imports, unchanged vector, false completion fields, exact two-file scope, and absent self-test agree |

The historical intake checker is an immutable intake-time validator whose hardcoded authority state
became stale when integration advanced intake from `[ ]` to `[_]`. Rewriting it in the statement
phase would alter predecessor evidence, so its failure is retained as a known boundary.

## Retry Condition And Status Boundary

The integration lane must first master-accept refreshed intake evidence bound to current authority.
Accountable reviewers must then lawfully preserve and hash one immutable primary or approved
authoritative source, select and independently approve an exact numbered proposition, and map every
incorporated definition, ordered binder, hypothesis, conclusion, proof boundary, correction,
erratum, and boundary case. They must resolve the graph and map classes, direction, ordinary versus
injective/induced/surjective convention, count or density semantics, normalization, weights,
coefficient domain, finiteness/decidability encoding, and all empty or degenerate cases.

A fresh statement run may then encode precisely that approved claim, prove its pinned direct
imports minimal, serialize and hash the elaborated expression and environment, compile every
credited transport, and run all four required mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; the root stays `[H5, M4, R4]`;
`audit_complete: false` and `theorem_complete: false`; no debt change is proposed. Because the
exact-statement deliverable did not pass, no `.stage1-worker-selftest.json`, statement receipt,
worker `[_]`, or master acceptance is claimed.
