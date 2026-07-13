# Exact-statement validation: blocked

Item: `S56-M-0869-STATEMENT`

Theorem: `THM-M-0869`

Base revision: `db4b8793e70ce8af74c9c9490acfa50aa3684d5e` (tree
`6434a20532ae7c523ad293e67a6228ab384bfb8a`). Attempt date: 2026-07-13
(`Asia/Shanghai`).

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the authoritative repository record.
That record gives only the title `禁用子图问题`, the gloss `禁用子图类的刻画`, collective
twentieth-century attribution, and an untrusted `已验证` label. It supplies no bibliography, named
graph class, containment relation, graph universe, formula, binders, hypotheses, conclusion, proof
boundary, correction history, reviewer, or formal artifact. Stage0 calls the entry a problem or
decision proposition while explicitly leaving the precise definitions and premises, proof route,
dependencies, alternate forms, axioms, machine status, and artifacts open.

Several inequivalent roots fit those words:

1. subgraph-closed graph classes represented by forbidden ordinary subgraphs;
2. hereditary graph classes represented by forbidden induced subgraphs;
3. minor-closed classes represented by excluded minors, possibly with a finite-basis conclusion;
4. a concrete graph class characterized by a specified forbidden configuration family; or
5. recognition, decidability, or complexity for avoidance of a fixed obstruction family.

These are not alternate spellings. They change the domain, containment relation, assumptions,
quantifiers, conclusion, and mathematical strength. In particular, a finite excluded-minor basis
requires graph-minor content that the catalog does not assign to this target. Selecting the first
variant merely because pinned mathlib exposes ordinary containment would also be an unsourced
choice, not exact elaboration.

The neighboring targets make substitution especially unsafe. `THM-M-0840` owns the Strong Perfect
Graph Theorem, `THM-M-0865` Kuratowski's theorem, `THM-M-0866` Wagner's theorem,
`THM-M-0867` the Robertson-Seymour graph-minor well-quasi-order theorem, and `THM-M-0868` the Graph
Minor Theorem family. None transfers a proposition, proof body, receipt, or status to this generic
topic.

Rev-5.6 sections 5 and 5.1 make statement ambiguity, unresolved target choices, and a missing
elaborated-expression fingerprint hard blockers. The intake therefore correctly leaves the
canonical human statement, Lean module and expression, imports, expression fingerprint, and
canonical environment fingerprint null at `[H5, M4, R4]`. Without a canonical target, import
minimality cannot be assessed, alternate transports cannot be credited, and the required
removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case mutations are undefined,
not passed. No `Statement.lean`, axiom, placeholder, tautological class encoding, or convenient
ordinary, induced, minor, planar, or perfect-graph substitute was added.

The prerequisite `S56-M-0869-INTAKE` is provisional worker state `[_]`, not master-accepted `[x]`.
Its receipt is unsigned, non-content-addressed, declares `accepted: false`, and is bound to the
pre-integration base revision. Its public replay now stops at the frozen blueprint hash because the
integration lane changed authoritative bytes. Rev-5.6 section 10.2 permits this dependency-ordered
blocker attempt, but dependency master acceptance independently prevents a statement transition.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` re-elaborates with its single direct import,
`Mathlib.Combinatorics.SimpleGraph.Copy`. It authenticates ordinary copy containment
`SimpleGraph.IsContained`, `SimpleGraph.Free`, induced containment
`SimpleGraph.IsIndContained`, both transitivity interfaces, and the ordinary/induced
existence-of-isomorphic-subgraph witnesses. The seven checked interfaces elaborate under the pinned
toolchain; complete stdout is 1153 bytes with SHA-256
`61d62ae40b39e2759ffafd0922c1129200e982a1aabca4e47143c5575ef674d5`.

The probe defines no graph class, obstruction family, closure property, source transport,
characterization theorem, canonical target, or proof body. Its import is minimal only for that API
probe and cannot be certified minimal for an absent target. It receives no statement or proof
credit.

A bounded exact-topic search over repository-local and pinned-mathlib Lean sources found no generic
forbidden graph-class characterization. A separate bounded search found no minor or contraction
interface in pinned mathlib's `Combinatorics/SimpleGraph` directory. These are discovery-only
results, not the downstream immutable anchor audit or global absence claims.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. Current input fingerprints are:

- target manifest: `02eec284de534dd78e1cf75f82a477ff477567dd682b7445cb7587abd137ab2c`;
- rev-5.6 blueprint: `5d0eb6d57ec108d3083f15d6e3773447c9e9287fa6d2f811ff6197055aa251f5`;
- execution DAG: `7005d2c291a900e175666f0826ee69b15bb77d208b4fb167174d0982f20055a3`;
- toolchain file: `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`;
- Lake manifest: `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`;
- pinned `SimpleGraph.Copy` source:
  `f40e66407ee7bb45be958fee42b54065b547b42ca47aa18c989a04e58a3ffb22`.

The automation-provided `Formalizations/Lean/.lake` link points to canonical pinned artifacts and
was used read-only. No `lake update`, `lake build`, dependency clone or fetch, or other `.lake`
mutation was run.

## Validation Evidence

Commands ran in this worker clone on 2026-07-13 (`Asia/Shanghai`), from the repository root unless
a different working directory is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and execution-skill presence passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0869` | 0 | rank 1423; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| pre-edit `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` link was untracked; base revision and tree appear above |
| scoped manifest, blueprint, skill, guidelines, catalog, Stage0, and complete intake inspection | 0 | the catalog is a topic family and the intake intentionally leaves the exact target null |
| authority, source, intake, toolchain, lockfile, probe, and mathlib `sha256sum` checks | 0 | exact current fingerprints were captured; selected values appear above |
| `python3 -B Stage1_Instances/THM-M-0869/check_intake.py` | 1 | historical intake replay stops at its frozen blueprint hash after integration advanced authoritative bytes; historical evidence was preserved rather than weakened |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| mathlib `git rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned revision and tree agree with the fingerprint; dependency worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0869/IntakeProbe.lean` | 0 | seven adjacent containment interfaces elaborated; stdout SHA-256 `61d62ae...74d5`; no target or proof body |
| bounded forbidden-class search over repository-local and pinned-mathlib Lean | 1, expected no match | no generic characterization declaration matched; discovery only |
| bounded minor/contraction search in pinned mathlib `SimpleGraph` | 1, expected no match | no interface matched; discovery only |
| prohibited Lean construct scan over the owned path | 1, expected no match | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |

The historical intake checker freezes intake-time authority hashes and its original artifact
inventory. Integration advanced the authority inputs. Its failure is recorded rather than
rewriting intake evidence to manufacture a passing statement attempt.

Post-write checks also passed: the new Markdown has a final newline and no trailing whitespace;
`git diff --check` emitted no diagnostics; and the statement-phase invariants confirm the assigned
item and current base, unchanged `[H5, M4, R4]`, null canonical target/import/fingerprint fields,
all four unrunnable mutation classes, false completion flags, and absence of the root self-test
manifest. The only new owned artifact is this report. The pre-existing `.lake` link remains the
only unrelated untracked path.

## Retry Condition

The integration lane must first master-accept refreshed intake evidence. Accountable independent
graph-theory source and scope reviewers must then preserve and admit an immutable source and select
one exact proposition. The review must fix the graph universe and equality convention, graph class,
containment relation and orientation, obstruction family and its minimality/finiteness/effectivity
strength, closure assumptions, ordered binders, hypotheses, conclusion, alternate encodings, and
every empty, infinite, duplicate, isolated-vertex, and relation-specific boundary case.

A fresh statement worker can then encode precisely that reviewed claim, minimize its pinned
imports, serialize and hash its elaborated expression and environment, compile every credited
transport, and execute all four mutation classes.

This is a truthful blocked-attempt record, not completion of the statement node or any downstream
node. Lifecycle remains `planned`; the item remains `[ ]`; the root remains `[H5, M4, R4]`;
`audit_complete: false` and `theorem_complete: false`; no debt change is proposed. Because the
exact-statement deliverable did not pass, no `.stage1-worker-selftest.json`, statement receipt,
worker `[_]`, proof credit, or master acceptance is claimed.
