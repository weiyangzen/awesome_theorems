# Exact-statement gate: blocked

Item: `S56-M-0838-STATEMENT`

Theorem: `THM-M-0838`

Base revision: `748243faadc15828fb087059337fd05b7be9fdeb` (tree
`e46d642646f80980838b6f016f5d69b817bd464d`). Attempt date: 2026-07-13
(`Asia/Shanghai`).

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the authoritative repository record.
That record gives the title `Gonthier的形式化证明`, Georges Gonthier, 2008, and the gloss
`四色定理的Coq形式化` (a Coq formalization of the Four Color Theorem). It names a proof artifact,
not one binder-complete truth-valued proposition. It supplies no formula, definition chain, theorem
locator, source edition, formal revision, toolchain, dependency closure, axiom profile, proof-body
boundary, correction, erratum, or reviewer. Stage0 explicitly leaves the formal system, precise
definitions and premises, proof route, dependencies, alternate forms, axioms, machine state, and
artifacts open. The catalog's `已验证` value is untrusted under rev-5.6.

Exact source discovery identifies a likely mathematical root but does not settle this target's root
kind. The immutable historical source lead declares:

```coq
Theorem four_color : forall m : map R, simple_map m -> map_colorable 4 m.
```

The maintained `rocq-community/fourcolor` release similarly declares `four_color_finite` and
`four_color` over its abstract real model and real-plane map vocabulary. These declarations mean,
roughly, that every simple map over an arbitrary real model is colorable with at most four colors.
They are exact discovery anchors only: neither project is a pinned repository dependency, and this
worker did not build or audit their dependency, axiom, placeholder, computation, or terminal-body
closure.

The repository does not decide whether this provenance-specific target owns:

1. the source mathematical theorem transported faithfully into Lean;
2. an artifact claim that an immutable Coq/Rocq development kernel-checks `four_color`; or
3. an explicit conjunction connecting the mathematical claim, artifact closure, and a checked Lean
   encoding or transport.

Those roots are not interchangeable. They have different domains, binders, conclusions, formal
systems, and trust boundaries. A generic theorem that every planar simple graph is
`SimpleGraph.Colorable 4` would erase the source's real-plane map, region, adjacency, face-coloring,
and compactness semantics. It would also duplicate the generic Four Color target `THM-M-0833`.
Targets `THM-M-0836` and `THM-M-0837` separately own the Appel-Haken and
Robertson-Sanders-Seymour-Thomas proof families; none supplies automatic proposition, provenance,
body, receipt, or status credit here.

The source real model, plane points, regions, map, properness, openness, connectedness, cover,
border, corner, adjacency, coloring, finite-to-arbitrary compactness, graph/hypermap representation,
duality, formal revision, foundation, computation and trust profiles, ordered binders, hypotheses,
conclusion, and degenerate cases all remain unapproved. Selecting any candidate now would invent,
broaden, narrow, or substitute proposition-changing mathematics.

Rev-5.6 sections 5 and 5.1 make statement ambiguity and a missing elaborated-expression fingerprint
hard blockers. The intake therefore correctly leaves the canonical mathematical statement, Lean
module, exact expression, imports, and expression/environment fingerprints null at
`[H5, M4, R4]`. Without a canonical target, imports cannot be certified minimal, alternate
transports cannot be credited, and the required removed-hypothesis, changed-domain,
changed-binder-scope, and boundary-case mutations are undefined, not passed. No `Statement.lean`,
axiom, placeholder, generic graph substitute, assumed planarity interface, or weakened theorem was
added.

The prerequisite `S56-M-0838-INTAKE` is only provisional worker state `[_]`, not master-accepted
`[x]`. Its receipt is unsigned, non-content-addressed, declares `accepted: false`, and has no
accepted receipt ID. Rev-5.6 section 10.2 permits this dependency-ordered blocker attempt, but
master acceptance remains independently required before a future statement transition.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` re-elaborates with its single direct import,
`Mathlib.Combinatorics.SimpleGraph.Coloring`. It authenticates `SimpleGraph.Coloring`,
`SimpleGraph.Colorable`, `SimpleGraph.chromaticNumber_le_iff_colorable`, and a graph schema whose
`Planar` predicate is an uninterpreted argument. The probe has no source real-map model, planarity
predicate, representation transport, Four Color declaration, canonical target, or proof body. Its
import is candidate-interface evidence only and cannot be certified minimal for an absent target.

A bounded exact-topic search over repository-local and pinned-mathlib Lean sources found no Four
Color or source-map declaration. The only relevant hit is the coloring module's TODO entry for
planar graphs. This is narrow discovery evidence, not the downstream immutable anchor audit or a
claim of global absence.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The `lean-toolchain`, `lake-manifest.json`, coloring
module, and probe-output SHA-256 values are recorded in `statement-blocker.json`.

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
| `python3 scripts/stage1_target.py show THM-M-0838` | 0 | rank 1395; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| pre-edit `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` link was untracked; base revision and tree appear above |
| scoped manifest, blueprint, skill, guidelines, catalog, Stage0, and complete intake inspection | 0 | the record names an artifact but does not select the mathematical, artifact-closure, or conjoined root; the intake intentionally leaves the target null |
| authority, source, intake, toolchain, lockfile, probe, and mathlib `sha256sum` checks | 0 | exact current fingerprints are recorded in `statement-blocker.json` |
| `python3 -B Stage1_Instances/THM-M-0838/check_intake.py` | 1 | historical intake replay stops at its frozen blueprint hash after integration advanced the blueprint; historical evidence was preserved rather than weakened |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| mathlib `git rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned revision and tree agree with the fingerprint; dependency worktree clean |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0838/IntakeProbe.lean` | 0 | three coloring declarations and `FourColorSchema` elaborated; stdout SHA-256 `3b4420d6...d71`; no canonical target or proof body |
| bounded Four Color and planarity search over repository-local and pinned-mathlib Lean | 0 | only the pinned planar-graphs TODO and unrelated algebra declarations matched; discovery only |
| prohibited Lean construct scan over the owned path | 1, expected no match | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |

The historical intake checker freezes intake-time repository identity and authority hashes. Master
integration advanced those inputs. Its failure is recorded rather than rewriting the intake
validator to manufacture a passing statement attempt.

## Retry Condition

The integration lane must first master-accept refreshed intake evidence. Accountable independent
reviewers must then preserve and hash a lawful immutable authoritative source and formal revision;
select the mathematical root, artifact-closure root, or an explicit conjunction; reconcile
neighbor ownership; and approve every incorporated real-model, map, topology, adjacency, coloring,
compactness, representation, foundation, computation, trust, binder, hypothesis, conclusion,
exception, and degenerate-case choice.

A fresh statement worker can then encode precisely that reviewed claim, minimize its pinned imports,
serialize and hash its elaborated expression and environment, compile every credited transport, and
execute all four required mutation classes.

This is a truthful blocked-attempt record, not completion of the statement node or any downstream
node. Lifecycle remains `planned`; the item remains `[ ]`; the root remains `[H5, M4, R4]`;
`audit_complete: false` and `theorem_complete: false`; no debt change is proposed. Because the
exact-statement deliverable did not pass, no `.stage1-worker-selftest.json`, statement receipt,
worker `[_]`, proof credit, or master acceptance is claimed.
