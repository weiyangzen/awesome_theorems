# THM-M-0815 exact-statement gate: blocked

Item: `S56-M-0815-STATEMENT`

Base revision: `db4b8793e70ce8af74c9c9490acfa50aa3684d5e`; base tree:
`6434a20532ae7c523ad293e67a6228ab384bfb8a`. Attempt date: `2026-07-13`
(`Asia/Shanghai`).

## Decision

The statement item remains `[ ]`. Its intake predecessor has provisional worker state `[_]`, not
master-accepted state `[x]`, and `intake-receipt.json` is explicitly `accepted: false`. More
importantly, the exact-statement gate independently fails before Lean target elaboration.

The complete repository claim is only `二部图完美匹配存在的条件`, "a condition for the existence
of a perfect matching in a bipartite graph." It does not define perfect matching, specify whether
the bipartition covers every graph vertex, require finite or equal parts, state the Hall
neighborhood condition, fix theorem direction, order binders, or settle boundary cases. The
primary 1935 article text could not be obtained, so no exact proposition or incorporated
definitions can lawfully resolve those omissions.

The inspected secondary formalization paper states the standard finite graph theorem as an iff
between the left-side neighborhood condition and a matching saturating the selected left part.
Pinned mathlib also exposes that one-side sufficient theorem. By contrast, mathlib's
`Subgraph.IsPerfectMatching` spans every graph vertex, and its ready-made perfect-matching theorem
uses a stronger condition quantified over every vertex subset. A balanced covering bipartition can
bridge one-side saturation to graph-wide perfection, but adding balance, coverage, finite scope,
and an iff is a proposition-changing selection not supplied or independently approved by the
received source.

Accordingly, the finite distinct-representative iff, the one-side graph iff, the balanced
graph-wide corollary, and the stronger global sufficient theorem remain materially different
candidates. Choosing any one merely because it is conventional or convenient would substitute,
narrow, or broaden the received target. `instance.json` correctly leaves the human statement,
Lean module/declaration, expression fingerprint, environment fingerprint, binders, hypotheses,
and alternate transports null or open. This attempt does not overwrite that fail-closed boundary.

No `Statement.lean`, canonical declaration, statement receipt, proof body, or root worker self-test
manifest is emitted. Minimal imports cannot be certified for an unidentified target, and the four
required statement mutations are undefined rather than passed.

## Validation record

The existing `IntakeProbe.lean` is discovery-only. It imports
`Mathlib.Combinatorics.SimpleGraph.Hall` and checks finite-family, relation, one-side matching, and
graph-wide perfect-matching interfaces. It elaborates under the pinned environment, but it selects
no target and earns no statement or proof credit.

Commands ran in this worker clone. The automation-provided canonical `.lake` symlink was reused
read-only. No `lake update`, `lake build`, dependency clone or fetch, or other `.lake` mutation ran.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, and the execution skill passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required`. |
| `python3 scripts/stage1_target.py show THM-M-0815` | 0 | Rank 1374; planned; legacy artifacts unaccepted; theorem incomplete. |
| pre-edit `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | Only the automation-provided `.lake` symlink was untracked; base revision and tree appear above. |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | Lean 4.29.0 commit `98dc76e3...`; Lake `5.0.0-src+98dc76e`. |
| pinned mathlib revision/tree/status checks | 0 | Revision `8a178386...`, tree `bdc39a31...`; package worktree clean. |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0815/IntakeProbe.lean` | 0 | Six candidate interfaces, three definition facts, and four axiom reports elaborated; stdout 2913 bytes, SHA-256 `d4d95cb4...ff68`; discovery only. |
| `python3 -B Stage1_Instances/THM-M-0815/check_intake.py` | 1 | Historical intake replay stopped at its pre-integration assertion that the intake authority state is `[ ]`; current integration records provisional `[_]`. No intake artifact was rewritten. |
| `python3 -m json.tool Stage1_Instances/THM-M-0815/statement-blocker.json` and scoped invariant assertions | 0 | Blocker identity, null target, unchanged vector, undefined mutations, false completion flags, exact change scope, and absent self-test agreed. |
| prohibited-construct scan over owned Lean | 1, expected no match | No `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration. |
| `git diff --check -- Stage1_Instances/THM-M-0815` plus no-index checks of both new files | 0 | No whitespace diagnostic. |

The historical intake checker is not statement evidence. This statement attempt records its stale
authority-state assertion rather than editing the historical intake artifacts.

## Retry condition

The integration lane must first decide the predecessor's acceptance. Accountable source and scope
reviewers must then admit an immutable exact proposition and independently fix:

- finite versus generalized scope and the exact graph/domain encoding;
- one-side saturation versus graph-wide perfect matching;
- bipartition disjointness, coverage, balance, and vertices outside the parts;
- the exact neighborhood/cardinality convention and theorem direction;
- ordered binders, universes, typeclass context, hypotheses, conclusion, and empty, isolated,
  singleton, unequal-part, overlapping-part, and infinite cases;
- every alternate encoding and the required checked transport direction.

A fresh statement worker can then encode precisely that reviewed claim, minimize pinned imports,
serialize the elaborated expression and environment fingerprints, compile every credited
transport, and execute removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case
mutations.

This is a truthful blocked statement attempt. Lifecycle stays `planned`, the vector stays
`[H1, M3, R4]`, and `audit_complete` and `theorem_complete` remain false. Because the assigned
deliverable did not pass, `.stage1-worker-selftest.json` is intentionally absent and no worker
`[_]`, receipt, proof, release, or master acceptance is claimed.
