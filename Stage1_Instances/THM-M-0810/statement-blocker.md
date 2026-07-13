# Exact-statement gate: blocked

Item: `S56-M-0810-STATEMENT`

Theorem: `THM-M-0810`

Base revision: `3ef3a6bf4f2f9b86930beb27693f7429fea3e63a` (tree
`c9eba4c65f6e228f9cefc8bdf62136b7fb69426a`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-0810-INTAKE` has provisional worker
state `[_]` in the authoritative execution DAG, not master-accepted state `[x]`. The intake receipt
also declares `accepted: false`, has no accepted receipt ID, and deliberately leaves the canonical
mathematical statement and Lean target null. Rev-5.6 section 10.2 permits preparation of this later
node, but accepted closure remains dependency ordered.

Independently, the repository record cannot support one exact Lean 4 target. It gives only the title
`欧拉公式`, the Leonhard Euler attribution and year 1750, and the gloss `平面图顶点、边、面的关系`
("the relationship among the vertices, edges, and faces of a planar graph"). It states no equation
and cites no edition, proposition, definition, proof, correction, erratum, or formal artifact. The
`已验证` label is untrusted metadata under rev-5.6. Stage0 calls the family a formula or identity but
explicitly leaves its definitions, premises, equivalent forms, foundation, axiom policy, machine
status, and artifact links open.

The familiar equation `V - E + F = 2` does not repair that omission. Before it is a proposition,
the target must select all of the following:

- a fixed plane embedding or an abstract planar graph plus a checked embedding transport;
- finite simple graphs, multigraphs, pseudographs, combinatorial maps, or another graph class;
- a connected formula or the exact component correction for disconnected graphs;
- a face type or equivalence relation, cellularity, outer-face convention, and the treatment of
  bridges, isolated vertices, and nested components;
- the plane, sphere, or another surface and its Euler-characteristic normalization; and
- ordered binders, hypotheses, number type, equality, and empty, singleton, tree, disconnected,
  noncellular, loop, and parallel-edge cases.

These choices yield materially different propositions. Silently selecting the connected finite
plane-graph formula, its spherical form, or a disconnected correction would invent or substitute
mathematics absent from the received record. A desired equality packaged as a structure field or
hypothesis would be circular rather than a theorem statement.

Rev-5.6 section 5 makes this ambiguity and the missing expression fingerprint a hard blocker.
Section 5.1 is therefore unreachable: there is no honest canonical declaration whose imports can
be minimized, no exact expression or environment-expression fingerprint, no approved alternate
encoding for a checked transport, and no baseline for the removed-hypothesis, changed-domain,
changed-binder-scope, and boundary mutations. Those mutations are undefined, not passed. No
`Statement.lean` was created, and the provisional root remains `[H5, M4, R4]`.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` re-elaborates with the single direct import
`Mathlib.Combinatorics.SimpleGraph.Connectivity.Connected`. It checks `SimpleGraph`, `edgeSet`,
`edgeFinset`, `Connected`, `ConnectedComponent`, and `Fintype.card`. All six checks pass in the
pinned environment.

This authenticates only generic simple-graph finite-edge counting and connectivity vocabulary. It
does not define a plane embedding, planarity predicate, face type or count, Euler identity, source
transport, mutation fixture, or proof body. Its import therefore cannot be certified minimal for a
canonical target that has not been selected. A bounded search found no target-specific interface in
the repository-local Lean sources or pinned `Mathlib.Combinatorics.SimpleGraph` sources; the only
SimpleGraph planar match was a documentation bullet in `Coloring.lean`. That is feasibility evidence
only, not an exhaustive anchor audit or an external absence claim.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib
revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` symlink was used read-only. No update, build, dependency clone or fetch,
or other `.lake` mutation was run.

## Validation Record

Commands ran from this isolated worker clone on 2026-07-13 (Asia/Shanghai).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0810` | 0 | rank 1369; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| pre-edit `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| exact `jq -e` checks over the authoritative DAG and `instance.json` | 0 each | confirmed provisional dependency, open statement node, null mathematical and Lean target, unchanged H5/M4/R4 root, and theorem incomplete |
| `git blame -L 5956,5961 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog fields originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `git log --all --format='%H %cI %s' -S'平面图顶点、边、面的关系' -- Docs/researches/math_theorems.md Docs/Stage0_Blueprint.md Stage0_Blueprint.md` plus source-version inspection | 0 | the phrase first entered at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`; inspected later versions contain no equation |
| exact full-file, excerpt, and pinned SimpleGraph `sha256sum` commands recorded in the JSON | 0 | all recorded digests matched |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| mathlib `git rev-parse HEAD 'HEAD^{tree}'`; package status | 0 | pinned revision and tree recorded above; package worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0810/IntakeProbe.lean` | 0 | six adjacent APIs elaborated; output was 412 bytes and 6 lines with SHA-256 `14589a96d021ff23735e91cb033fd1812a02021b5df8b66a17343db4a8319918`; no canonical target or proof body |
| exact bounded `rg`/`find`/`xargs rg` command recorded in the JSON over repository-local Lean and pinned `SimpleGraph` sources | 0 aggregate | no target-specific planarity, embedding, face-count, or Euler-formula interface found; discovery-only evidence |
| `python3 -B Stage1_Instances/THM-M-0810/check_intake.py` | 1 | historical intake checker expects authoritative intake state `[ ]`, while integration now records `[_]`; its intake-time authority and inventory are not rewritten by this statement phase |
| prohibited-construct scan over owned Lean files | 1 | expected no-match result; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| JSON parse and scoped blocker invariant assertions | 0 each | identity, null target and imports, unchanged vector, four undefined mutations, false completion flags, exact paths, and absent self-test agree |
| scoped `git diff --check` and per-new-file no-index checks | 0; 1 each | no whitespace diagnostics; both no-index exits are only the expected new-file differences |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest intentionally absent because the exact-statement deliverable did not pass |

## Retry Condition And Status Boundary

The integration lane must first accept the intake dependency. Accountable reviewers must then
preserve and hash an immutable primary or authoritative source, select and independently approve one
exact proposition, and transcribe every incorporated definition, binder, hypothesis, conclusion,
graph and embedding convention, face and surface convention, boundary case, proof boundary,
correction, and erratum.

A fresh statement run can then encode precisely that source-selected claim, minimize pinned imports,
serialize and hash its elaborated expression and environment, compile every credited transport, and
run all four required mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. Because the exact-statement
deliverable did not pass, no `.stage1-worker-selftest.json`, statement receipt, worker `[_]`, proof,
release, or master acceptance is claimed.
