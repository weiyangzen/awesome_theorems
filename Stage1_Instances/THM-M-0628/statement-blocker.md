# Exact-statement gate: blocked

Item: `S56-M-0628-STATEMENT`

Theorem: `THM-M-0628`

Base revision: `b09b188fbf6e0e288ddccb92314ef863d473ebad` (tree
`d64707bb77427b4e8569657bcd92a2c7f5713dc9`).

## Decision

The statement item remains `[ ]`. Its intake prerequisite is provisional worker state `[_]`, not
master-accepted state `[x]`. More importantly, the exact Lean 4 target cannot be truthfully
elaborated from the complete repository source record.

That record supplies only the title `局部紧性定理` ("local compactness theorem") and the gloss
`局部紧空间的性质` ("properties of locally compact spaces"). It gives no citation, incorporated
definition, ordered binders, hypotheses, conclusion, proof boundary, corrections, errata, or
independent statement review. Stage0 explicitly leaves the precise definitions and premises open,
and the catalog label `已验证` is untrusted metadata under rev-5.6.

The wording is a topic family, not a proposition. In particular, it does not select among:

- existence of some compact neighborhood at every point (`WeaklyLocallyCompactSpace`);
- compact refinement inside every neighborhood (`LocallyCompactSpace`);
- a compact or compact-and-closed neighborhood basis;
- existence of open neighborhoods with compact closure;
- compact refinements for a point or compact set inside an open set; or
- a preservation, regularity, Baire, compact-open, or compactification theorem.

These readings have different conclusions, and some require R1 or stronger separation assumptions.
Mathlib explicitly distinguishes weak and strong local compactness outside the Hausdorff setting.
Choosing one convenient declaration would invent or substitute mathematics. `THM-M-0629`
separately owns the one-point compactification target, so that result cannot be used as this root.

There is consequently no canonical expression on which to certify minimal imports, serialize an
expression and environment fingerprint, check alternate transports, or run removed-hypothesis,
changed-domain, changed-binder-scope, and boundary-case mutations. These checks are undefined, not
passed. No statement, Lean target, declaration, import claim, or proof body was added. The root
remains `[H5, M4, R4]`; audit and theorem completion are false.

## Pinned Lean boundary

The existing discovery-only `IntakeProbe.lean` imports
`Mathlib.Topology.Separation.Basic` and re-elaborates eleven adjacent interfaces. It confirms:

- weak local compactness gives some compact member of `nhds x`;
- strong local compactness refines every `n in nhds x` by a compact neighborhood; and
- an R1 space with weak local compactness has compact-closed neighborhood results, a weak-to-strong
  instance, and open neighborhoods with compact closure.

The probe declares no target or proof body. `Mathlib.Topology.Compactness.LocallyCompact` is a
possible smaller import for non-R1 interfaces; `Mathlib.Topology.Separation.Basic` is needed for the
checked R1-dependent interfaces. Neither import can be called minimal until a source-approved
proposition selects one of those surfaces.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided `.lake` link was reused read
only. No update, build, clone, fetch, or dependency mutation was run.

## Validation evidence

Commands ran in this isolated worker clone on 2026-07-13 (`Asia/Shanghai`). Lean commands ran from
`Formalizations/Lean`; other commands ran from the repository root unless noted.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0628` | 0 | rank 1048, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| pre-edit `git status --short --untracked-files=all` and `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` link was untracked; current base revision and tree are recorded above |
| source, Stage0, manifest, blueprint, DAG, skill, and intake inspection | 0 | the sole claim-bearing phrase is a topic family; the canonical claim, Lean target, imports, expression hash, and target fingerprint are null |
| `lake env lean --version`, `lake --version`, and lockfile hashes | 0 | Lean, Lake, and SHA-256 inputs agree with `statement-blocker.json` |
| pinned mathlib revision, tree, and status inspection | 0 | revision and tree agree with the recorded environment; package worktree was clean |
| `lake env lean ../../Stage1_Instances/THM-M-0628/IntakeProbe.lean` | 0 | eleven materially different adjacent APIs elaborated; stdout SHA-256 `f37e817be67680d8955a41a09d4838459312dd2f687728fab72fc3125283776e`; no target or proof body was declared |
| `python3 -B Stage1_Instances/THM-M-0628/check_intake.py` | 1 | historical intake checker expects intake authority state `[ ]`; current authority records provisional `[_]`, and this phase does not rewrite intake evidence |
| `python3 -m json.tool Stage1_Instances/THM-M-0628/statement-blocker.json` plus scoped assertions | 0 | blocker syntax and statement-phase identity, null-target, unchanged-vector, completion, mutation, and absent-self-test invariants passed |
| prohibited-construct scan over owned Lean files | 1 | expected no-match: no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| scoped whitespace and final-newline checks | 0 | both blocker artifacts passed |
| `test ! -e .stage1-worker-selftest.json` | 0 | no self-test manifest exists because the exact-statement deliverable did not pass |

## Retry condition and status boundary

The integration lane must master-accept the intake dependency. An accountable reviewer must
preserve and hash one immutable primary or authoritative source, select one exact proposition and
pinpoint locator, transcribe every incorporated definition, binder, hypothesis, conclusion, proof
boundary, correction, erratum, translation, and boundary case, and independently approve the
mapping. The review must explicitly fix the local-compactness and separation conventions and the
ownership boundary with `THM-M-0629`.

A later statement worker can then encode exactly that source claim, minimize pinned imports,
serialize and hash the elaborated expression and environment, compile every credited transport,
and run all four mutation classes.

This is a fail-closed blocker report, not completion of the statement node or any downstream node.
No statement receipt, worker `[_]`, proof, audit completion, theorem completion, or master
acceptance is claimed. Because the assigned deliverable did not pass, no
`.stage1-worker-selftest.json` is emitted.
