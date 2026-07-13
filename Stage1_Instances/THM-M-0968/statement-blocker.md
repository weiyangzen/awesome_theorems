# THM-M-0968 exact-statement gate: blocked

Item: `S56-M-0968-STATEMENT`

Base revision: `48abbb2d2eeb89816c5ffc0ad8faafa4b9d24dd0` (tree
`0f26e2c78fb5fff9277cbbdfef5e145fd4ef06f1`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-0968-INTAKE` has only provisional worker
state `[_]`. The intake receipt is unsigned, non-content-addressed, has `accepted: false`, and has
no accepted receipt IDs. It also binds older blueprint and execution-DAG hashes, so its historical
checker now fails closed on the first stale authority hash. There is no master-accepted dependency
receipt. Rev-5.6 section 10.2 permits this dependency-ordered blocker attempt, but master closure
remains dependency ordered.

Independently and decisively, the exact-statement gate fails. The complete catalog record supplies
only the title `Erdős盒原理` (literally "Erdős box principle"), Paul Erdős, the year 1965, and the
gloss `超图中的匹配` ("matchings in hypergraphs"). It provides no citation or truth-valued
proposition. Stage0 repeats the gloss while explicitly leaving precise definitions and premises,
the proof route, formal system, alternate forms, axiom policy, machine status, and artifact links
open. The catalog's `已验证` label is untrusted metadata under rev-5.6.

The existing intake records a strong source-family lead, Erdős's 1965 paper *A problem on
independent r-tuples*, but that lead does not select one theorem. The paper proves a
sufficiently-large-`n` threshold equality on page 94 and separately presents a materially broader
unrestricted maximum-of-two-constructions formula as an elusive problem in equation (9) on page
95. The literal title can instead suggest ordinary pigeonhole, which is separately owned by
`THM-M-0914`. A graph special case, the matching-number-one intersecting-family case separately
owned by `THM-M-0822`, or another matching-existence or extremal theorem would also be different
propositions. No independently reviewed repository source correction chooses among these readings.

The following proposition-changing inputs therefore remain open:

- the exact primary-source result, edition, locator, incorporated definitions, correction and
  errata disposition, proof boundary, translation, and independently approved catalog mapping;
- the finite ground-set carrier, hyperedge and family representation, universe, decidability and
  finiteness context, uniformity parameter, and simple-versus-repeated-edge convention;
- the matching predicate and off-by-one convention, including maximum size avoiding `k` disjoint
  edges versus least size forcing `k` disjoint edges;
- every ordered binder and side condition, including positivity, `r <= n`, admissibility of the
  requested matching size, and the sufficiently-large-domain threshold if that result is selected;
- the exact extremal expression, equality or inequality strength, conclusion orientation, and
  credited alternate encodings; and
- zero and small parameters, `n < r * k`, empty families, impossible matchings, and ties between
  the two extremal constructions.

Choosing any familiar formula would invent, narrow, broaden, or substitute mathematics. There is
therefore no canonical Lean expression whose imports can be minimized, no elaborated expression or
canonical-target environment fingerprint, and no approved alternate encoding. Removed-hypothesis,
changed-domain, changed-binder-scope, and boundary-case mutations are undefined rather than passed.
No `Statement.lean`, theorem declaration, proof body, statement receipt, weakened special case, or
broadened interface was added. Lifecycle remains `planned`, and the root remains
`[H5, M4, R4]`.

## Pinned Lean Boundary

The existing discovery-only `IntakeProbe.lean` imports `Mathlib.Data.Finset.Pairwise` and
`Mathlib.Data.Finset.Slice`. It re-elaborates `Set.Sized`, `Set.Sized.card_le`,
`Finset.powersetCard`, `Finset.mem_powersetCard`, `Set.PairwiseDisjoint`, `Disjoint`, and
`Finset.card` in the pinned environment. Those APIs can describe uniform finite set families and
pairwise disjoint members. They neither select nor state an Erdős matching theorem, so the probe's
imports are not claimed to be minimal imports for a canonical target and receive no statement or
proof credit.

A bounded exact-topic search of pinned mathlib and the repo-local Lean tree found no occurrence
under the searched Erdős-matching, matching-conjecture, independent-`r`-tuple, hypergraph-matching,
or box-principle terms. This is only narrow feasibility evidence, not the downstream immutable
anchor audit or a global absence claim.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided `.lake` symlink was present
before this work and was used read-only. No `lake update`, `lake build`, dependency clone or fetch,
network-triggering Lake operation, or other `.lake` mutation was performed.

## Validation Record

Commands ran from this isolated worker clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and execution-skill presence passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0968` | 0 | rank 1502; planned; intake score 86; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| pre-edit `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `Formalizations/Lean/.lake` symlink was untracked; the base revision and tree appear above |
| blueprint, skill, manifest, DAG, catalog, Stage0, and complete intake-dossier inspection | 0 | confirmed statement item `[ ]`, provisional intake `[_]`, null canonical claim and target, and the unresolved title/source/result choices |
| `python3 -B Stage1_Instances/THM-M-0968/check_intake.py` | 1 | historical intake replay failed closed with `AssertionError: stale receipt input hash: Docs/Stage1_Blueprint_rev-5.6.md`; the current blueprint hash is `c0eef703...f8752`, while the receipt records `8607034e...e46d` |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean --version && lake --version` | 0 | Lean and Lake versions recorded above |
| mathlib `git rev-parse HEAD 'HEAD^{tree}'` plus package status | 0 | pinned revision and tree recorded above; package worktree clean |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0968/IntakeProbe.lean` | 0 | seven adjacent APIs elaborated; complete stdout SHA-256 `1211f2485935c978b086759c1537c5c45c506112ba6fc2590d9c2a404c627f1e`; no canonical target or proof credit |
| bounded exact-topic `rg` over pinned mathlib and repo-local Lean | 1, expected no match | no occurrence under the searched terms; no global-absence or anchor-audit claim |
| prohibited-construct scan over owned Lean files | 1, expected no match | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| final JSON parse and scoped blocker-invariant assertions | 0 | identity, base, dependency state, null target/imports/fingerprints, unchanged vector, undefined mutations, false completion flags, and exact two-file change scope agree |
| scoped tracked and per-added-file whitespace checks | 0 | no whitespace diagnostics |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest intentionally absent because the exact-statement deliverable did not pass |

## Retry Condition And Status Boundary

The integration lane must first master-accept refreshed intake evidence. Accountable reviewers must
then lawfully preserve and hash an immutable primary or approved authoritative source, resolve the
title/gloss conflict, independently select one exact result, and approve every incorporated
definition, ordered binder, hypothesis, conclusion, extremal convention, correction, erratum,
neighbor boundary, and degenerate case.

A fresh statement worker can then encode exactly that reviewed claim, minimize its pinned imports,
serialize and hash the elaborated expression and environment, compile every credited transport,
and execute all four required mutation classes.

This is a truthful blocked statement attempt, not completion of this node or any downstream node.
`audit_complete: false` and `theorem_complete: false`; no debt-vector change is proposed. Because
the exact-statement deliverable did not pass, no `.stage1-worker-selftest.json`, statement receipt,
worker `[_]`, proof credit, accepted receipt, or master acceptance is claimed.
