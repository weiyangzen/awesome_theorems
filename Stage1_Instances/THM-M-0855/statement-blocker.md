# Exact-statement gate: blocked

Item: `S56-M-0855-STATEMENT`

Theorem: `THM-M-0855`

Base revision: `fb0baac89ea0633612be3b47448464b4b8e4bef7` (tree
`018557070da18ea1733a82de81a238750c59aa84`).

## Decision

The exact Lean 4 target cannot yet be truthfully selected. The admitted primary source identifies
Chvatal and Erdos, *A note on Hamiltonian circuits*, Theorem 1, and prints this claim:

> Let G be a graph with at least three vertices. If, for some s, G is s-connected and contains no
> independent set of more than s vertices, then G has a Hamiltonian circuit.

That is enough to distinguish the root from the paper's Hamiltonian-path Theorem 2 and
Hamiltonian-connected Theorem 3. It is not enough to elaborate an exact proposition because the
paper does not define `s`-connected. Its proof instead invokes Dirac, *Generalisation du theoreme
de Menger* (1960), Theorem 1. No immutable copy, exact definition passage, translation,
correction/errata disposition, or independently reviewed transport for that incorporated source
has been admitted.

The unresolved definition determines proposition-changing choices:

- whether `s` ranges over positive integers or all naturals;
- whether `s`-connected includes `s < |V|`, `s <= |V|`, or another graph-order convention;
- whether connectivity after deleting fewer than `s` vertices is expressed by connectedness or
  preconnectedness when the remaining carrier is empty;
- the complete-graph convention and the cases `s = 0`, `s = 1`, and `s >= |V|`; and
- whether a deletion definition or a disjoint-path definition is canonical and what checked
  transport relates it to the source.

These are not cosmetic Lean choices. For example, the tempting local definition

```text
s < Fintype.card V and, after deleting every vertex set of size less than s,
the induced graph is connected
```

is a standard modern candidate, but choosing it without the incorporated-definition audit would
complete missing source mathematics. Omitting the order bound instead makes large `s` cases
vacuous or dependent on the empty-remnant convention. Replacing vertex connectivity with
`SimpleGraph.IsEdgeConnected`, ordinary connectedness, or an assumed disjoint-path witness would
substitute a different theorem.

The independence and conclusion substrates are available but cannot repair that missing premise.
`G.indepNum <= s`, `G.IndepSetFree (s + 1)`, and a quantified finite-independent-set bound are
candidate encodings whose relationship still needs a checked wrapper after the root parameter is
fixed. Likewise, `G.IsHamiltonian` uses mathlib's singleton convention; the printed premise
excludes graphs with fewer than three vertices, but the exact source-to-Lean convention transport
has not been approved.

Sections 5 and 5.1 of the rev-5.6 blueprint make statement ambiguity, unresolved target choices,
and a missing expression fingerprint hard blockers. Accordingly, no `Statement.lean`, canonical
declaration, import-minimality claim, expression/environment fingerprint, alternate-form credit,
or mutation fixture was created. The required removed-hypothesis, changed-domain,
changed-binder-scope, and boundary mutations are undefined, not passed. No axiom, placeholder,
weakened theorem, or convenient substitute was introduced.

The prerequisite `S56-M-0855-INTAKE` is only provisional `[_]`, not master-accepted `[x]`.
Dependency-ordered inspection can record this blocker, but it cannot promote the statement node.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` was re-elaborated with the repository's pinned Lean and mathlib
artifacts. It checks `SimpleGraph.IsHamiltonian`, `Walk.IsHamiltonianCycle`, `IsIndepSet`,
`IsNIndepSet`, `IndepSetFree`, `indepNum`, `Subgraph.deleteVerts`, and `Connected`. Its complete
stdout is 757 bytes over nine lines with SHA-256
`974220c4c5fc618c87634cca8a19a4846c4bdf9b51b206a770ee5a8286acbf28`.

A bounded search of the repository and pinned packages found no direct vertex-`s`-connectivity or
Chvatal-Erdos declaration. `SimpleGraph.IsEdgeConnected` was found and rejected as a non-substitute.
This is discovery evidence only, not an anchor audit or a global absence proof. The probe declares
no canonical target, checked source transport, or proof body, so its imports cannot be certified
minimal for an absent target.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` symlink was used read-only. No update, build, clone, fetch, or other
dependency mutation was run.

## Validation Evidence

Commands ran from this worker clone on 2026-07-13 (`Asia/Shanghai`), from the repository root
unless another working directory is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0855` | 0 | rank 1409, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| initial `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` link was untracked; base revision and tree are recorded above |
| manifest, blueprint sections 0, 3, 5-11 and 14, execution skill, guidelines, and complete intake dossier inspection | 0 | primary Theorem 1 is selected, but its incorporated vertex-connectivity definition and exact formal target remain explicitly open |
| `curl` of the intake-recorded institutional scan followed by `file`, `wc`, `sha256sum`, `pdfinfo`, and `pdftotext -layout` | 0 | three-page, 221449-byte primary scan with SHA-256 `a14dc030...492a7`; Theorem 1 and its Dirac-Theorem-1 dependency inspected |
| `python3 -B Stage1_Instances/THM-M-0855/check_intake.py --primary-pdf /tmp/thm-m-0855-primary.pdf` | 1 | historical receipt checker stops at its frozen repository base `1c0c5fc6...`; current HEAD is `fb0baac8...`, so it is not current statement evidence and was not modified |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions agree with the environment above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned revision/tree agree and the mathlib package worktree is clean |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0855/IntakeProbe.lean` | 0 | eight adjacent APIs elaborated; output fingerprint recorded above; no target or proof declared |
| bounded repo-local and pinned-package exact-topic search | 0 | four disclaimer-only matches, including this intake probe; no direct vertex-connectivity or Chvatal-Erdos declaration found; edge connectivity classified separately as a non-substitute |
| prohibited Lean declaration scan over `IntakeProbe.lean` | expected no-match | no `sorry`, `admit`, `sorryAx`, axiom, bodyless declaration, opaque declaration, or unsafe declaration |

## Retry Condition

The integration lane must first master-accept fresh intake evidence. Accountable graph-theory and
source reviewers must then admit and independently review the incorporated connectivity definition
or another authoritative definition explicitly tied to the 1972 theorem. They must freeze the
parameter domain, graph-order bound, deletion/disjoint-path relationship, complete-graph and empty-
remnant conventions, and all `s = 0`, `s = 1`, and large-`s` cases. A formal reviewer must approve
the independence-bound and Hamiltonicity transports.

A fresh statement run can then encode exactly that approved claim, minimize pinned imports,
serialize the elaborated expression and environment, compile every credited transport, and run all
four mutation classes.

This is a blocked statement attempt, not completion of this or any downstream node. Lifecycle
remains `planned`; the root remains `[H1, M4, R4]`; `audit_complete` and `theorem_complete` remain
false. Because the assigned deliverable is not genuinely self-tested, no root
`.stage1-worker-selftest.json`, statement receipt, worker `[_]`, or master acceptance is claimed.
