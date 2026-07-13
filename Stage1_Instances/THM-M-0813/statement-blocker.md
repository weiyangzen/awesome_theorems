# Exact-statement gate: blocked

Item: `S56-M-0813-STATEMENT`

Theorem: `THM-M-0813`

Base revision: `464759128569180ab640c412cd80bc5dd2c3b44a` (tree
`8da3c9130640d08d4e179450a0418368d0454745`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-0813-INTAKE` has provisional worker
state `[_]`, not master-accepted state `[x]`. Its receipt declares `accepted: false`, is unsigned
and non-content-addressed, and has no accepted receipt ID. Rev-5.6 permits this dependency-ordered
statement attempt, but master acceptance remains necessary before a future statement transition
can be accepted.

Independently of that dependency boundary, the exact Lean 4 target cannot be truthfully elaborated
from the authoritative repository record. The complete catalog wording is only `门格尔定理`
(Menger's theorem) and `图中不相交路径的最大数目` ("the maximum number of disjoint paths in a
graph"), with Karl Menger and 1927 as uncited metadata. This is not a proposition: it names one
side of an extremal relation but does not say what the maximum equals. The record also omits:

- finite or infinite, simple or multi, directed or undirected graph scope;
- terminal sets versus two vertices and the treatment of overlapping or equal terminals;
- vertex-disjoint, internally vertex-disjoint, or edge-disjoint paths;
- the separator or cut definition and whether terminal vertices may be removed;
- natural-number, finite-cardinal, or infinite-cardinal extrema;
- local equality versus global connectivity equivalence; and
- ordered binders, hypotheses, conclusion, and all degenerate cases.

These choices select materially different roots. Diestel's sixth-edition Theorem 3.3.1 is a strong
modern lead for the finite set-to-set vertex form, while its Corollary 3.3.5 and Theorem 3.3.6 give
separate point, edge, and global forms. The catalog cites none of them and does not select among
them. The preserved 1927 publisher scan has no text layer, and no exact original passage,
definition and translation mapping, proof boundary, corrections or errata disposition, or
independent source review has been accepted.

The repository also separately retains `THM-M-0862`, with the same attribution and year and the
overlapping gloss "vertex connectivity and disjoint paths." No accepted alias, deduplication,
distinct-root, checked transport, or terminal proof-body ownership decision relates the two
targets. Selecting the familiar set-to-set theorem, copying a future `THM-M-0862` statement, or
conjoining standard variants would invent, narrow, broaden, or substitute mathematics.

Rev-5.6 sections 5 and 5.1 make statement ambiguity and a missing elaborated-expression
fingerprint hard blockers. With no canonical proposition, there is no honest target import set to
minimize, no expression or environment-expression fingerprint, no credited alternate transport,
and no meaningful removed-hypothesis, changed-domain, changed-binder-scope, or boundary-case
mutation. Those four mutation classes are undefined, not passed. The root vector remains
`[H1, M4, R4]`.

## Pinned Lean Boundary

The existing discovery-only `IntakeProbe.lean` re-elaborates with the two direct imports
`Mathlib.Combinatorics.SimpleGraph.Connectivity.EdgeConnectivity` and
`Mathlib.Combinatorics.SimpleGraph.Maps`. It authenticates eight adjacent path, reachability,
induced-subgraph, and edge-connectivity interfaces. It defines no vertex separator or path-family
packing predicate, canonical Menger proposition, checked source transport, or proof body. Its
imports therefore cannot be certified minimal for an absent target.

A bounded exact-topic search under pinned mathlib's simple-graph modules and the repo-local Lean
tree found only `SimpleGraph.Walk.IsPath.disjoint_support_of_append`, a support-disjointness lemma
inside one appended path. It found no direct Menger declaration or vertex-separator/path-packing
theorem. This is discovery-only feasibility evidence, not the downstream exhaustive anchor audit
or a global absence claim.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib
revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` symlink was used read-only. No `lake update`, `lake build`, dependency
clone or fetch, or other `.lake` mutation ran.

## Validation Record

Commands ran from this isolated worker clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0813` | 0 | rank 1372; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| pre-edit `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` symlink was untracked; the base revision and tree are recorded above |
| catalog, Stage0, manifest, blueprint, intake, source-crosswalk, and duplicate-scope inspection | 0 | the gloss is not a proposition, the canonical target is null, materially different variants remain open, and `THM-M-0862` ownership is unresolved |
| `python3 -B Stage1_Instances/THM-M-0813/check_intake.py` before adding this pair | 0 | planned `H1/M4/R4`, null target, original nine-file intake inventory, and six open tasks agreed |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | the pinned Lean and Lake versions above were reported |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned mathlib revision and tree above; empty status output confirmed a clean package worktree |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0813/IntakeProbe.lean` | 0 | eight adjacent APIs elaborated; stdout SHA-256 `acddbc7c967786d595d8bce3393b249946d3bd2b5e495df6f246698d6b8c21d7`; no canonical target or proof body was declared |
| bounded exact-topic `rg` under pinned simple-graph mathlib, repo-local Lean, and the owned dossier | 0 | only the local appended-path support lemma and probe disclaimer matched; discovery evidence only |
| SHA-256 over authority, intake, toolchain, lockfile, probe, and pinned simple-graph sources | 0 | exact current fingerprints are recorded in `statement-blocker.json` |
| `python3 -B Stage1_Instances/THM-M-0813/check_intake.py` after adding this pair | 1 | expected historical boundary: the intake-only checker rejected the enlarged owned-file inventory |
| `python3 -m json.tool Stage1_Instances/THM-M-0813/statement-blocker.json` and recorded `jq -e` invariant check | 0 | JSON syntax, blocked/null-target state, unchanged vector, undefined mutations, false completion flags, and exact change scope agreed |
| prohibited Lean declaration scan, tracked and no-index whitespace checks, and `test ! -e .stage1-worker-selftest.json` | expected no-match/difference exits; wrappers 0 | no prohibited declaration or whitespace diagnostic; self-test manifest absent |

Final structural JSON, blocker-invariant, prohibited-construct, whitespace, and absence-of-self-test
checks are recorded in `statement-blocker.json`. The historical intake checker owns a closed
intake-only inventory, so after this blocker pair is added it is expected to stop at that inventory
assertion. This statement phase records that stale historical boundary rather than rewriting the
intake checker, receipt, task DAG, generated blueprint, or authoritative execution DAG to
manufacture agreement.

## Retry Condition And Status Boundary

The integration lane must master-accept the intake before accepting a later statement transition.
Accountable reviewers must preserve an immutable complete source, independently approve one exact
Menger proposition and every incorporated definition, and issue an accepted identity and
canonical-root ownership decision for `THM-M-0813` versus `THM-M-0862`. That review must freeze the
graph model, terminals, path and disjointness predicates, separator, extremum and cardinality,
local or global formulation, ordered binders, hypotheses, conclusion, proof boundary,
translations, corrections, errata, and every boundary case.

A fresh statement run can then encode precisely that approved claim, minimize its pinned imports,
serialize and hash the elaborated expression and environment, compile every credited transport,
and execute all four mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change, statement receipt, worker `[_]`, proof credit,
or master acceptance is claimed. Because the exact-statement deliverable did not pass, no
`.stage1-worker-selftest.json` is emitted.
