# Exact-statement gate: blocked

Item: `S56-M-0627-STATEMENT`

Theorem: `THM-M-0627`

Base revision: `d05520867fab3367a9b61b9544c3e12241204f54` (tree
`fb2cfc62077d5b53e9938632cd6361dd60872067`).

## Decision

The statement item remains `[ ]`. Its intake prerequisite is provisional worker state `[_]`, not
master-accepted state `[x]`. More importantly, no exact Lean 4 target can be truthfully elaborated
from the complete repository source record.

The catalog gives only the title `道路连通性定理` (provisionally, "path-connectedness theorem") and
the gloss `道路连通空间的性质` ("properties of path-connected spaces"). It gives no citation,
incorporated definition, ordered binders, hypotheses, conclusion, proof boundary, corrections,
errata, translation, or independent statement review. Stage0 explicitly leaves the precise
definitions and premises open, and the catalog's `已验证` label is untrusted metadata under
rev-5.6.

The wording names a topic family, not a truth-valued proposition. It does not select among:

- nonemptiness plus a path between every two points;
- preservation by continuous images or surjective continuous maps;
- path-connectedness implying connectedness;
- whole-space, universal-set, subtype, path-component, or zeroth-homotopy characterizations; or
- preservation under unions, products, quotients, group operations, or other constructions.

These candidates have different binders, assumptions, conclusions, and boundary cases. Ordinary
Chinese topology terminology supports the provisional path-connected translation, but the catalog
does not formally define its path convention, rule out nonstandard usage, select a set-relative or
space-level root, fix an interval and endpoint convention, or say how nonemptiness is handled.
Selecting any convenient pinned declaration would invent or substitute mathematics. The neighboring
`THM-M-0626` continuous-image theorem for connected sets cannot supply this target's missing
statement.

There is consequently no canonical expression on which to certify minimal imports, serialize an
expression and environment fingerprint, check alternate transports, or run removed-hypothesis,
changed-domain, changed-binder-scope, and boundary-case mutations. These checks are undefined, not
passed. No statement, target declaration, import-minimality claim, transport, mutation fixture, or
proof body was added. The root remains `[H5, M4, R4]`; audit and theorem completion are false.

## Pinned Lean boundary

The existing discovery-only `IntakeProbe.lean` imports
`Mathlib.Topology.Connected.PathConnected` and re-elaborates ten adjacent interfaces. It confirms
that the pinned module separately exposes `Joined`, `JoinedIn`, `IsPathConnected`,
`PathConnectedSpace`, a definitional characterization, continuous-image and connectedness
consequences, a surjective-image result, and universal-set and subtype transports. Their distinct
types expose rather than resolve the missing proposition selection.

The probe declares no canonical target or proof body. Its one direct import is the narrow module
for this adjacent API probe, but it cannot be certified as the minimal import for an absent target
and receives no statement or proof credit.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided `.lake` link was reused read
only. No update, build, clone, fetch, or dependency mutation was run.

## Validation evidence

Commands ran in this worker clone on 2026-07-13 (`Asia/Shanghai`). Lean commands ran from
`Formalizations/Lean`; other commands ran from the repository root unless noted.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0627` | 0 | rank 1321, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| pre-edit `git status --short --untracked-files=all` and `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` link was untracked; the base revision and tree are recorded above |
| `lake env lean --version` and `lake --version` | 0 | Lean and Lake agree with the pinned environment above |
| pinned mathlib revision, tree, package-status, and source-hash checks | 0 | the clean package worktree and pinned inputs agree with `statement-blocker.json` |
| `lake env lean ../../Stage1_Instances/THM-M-0627/IntakeProbe.lean` | 0 | ten materially different adjacent APIs elaborated; stdout SHA-256 `47c3eea7ed73c9c29887a6e9c2abda478e63ff2700883ee33b2dbaefeb308eda`; no target or proof body was declared |
| `python3 -B Stage1_Instances/THM-M-0627/check_intake.py` | 1 | the historical intake checker expects intake authority state `[ ]`; current authority records provisional `[_]`, and this phase does not rewrite intake evidence |
| `python3 -m json.tool Stage1_Instances/THM-M-0627/statement-blocker.json` | 0 | blocker JSON parsed successfully after finalization |
| `rg -n --glob '*.lean' '\b(sorry|admit)\b|\bsorryAx\b|^[[:space:]]*(axiom|constant|opaque|unsafe)[[:space:]]' Stage1_Instances/THM-M-0627` | 1 | expected no-match: no prohibited declaration in the owned Lean probe |
| `git diff --no-index --check /dev/null Stage1_Instances/THM-M-0627/statement-blocker.md` and the same command for `statement-blocker.json` | 1 each | expected new-file difference exits with empty output; no whitespace diagnostics |
| `test ! -e .stage1-worker-selftest.json` | 0 | no self-test manifest exists because the exact-statement deliverable did not pass |

The historical intake checker is bound to the intake-time authority state and original nine-file
inventory. The integration lane has since recorded intake as `[_]`; adding this statement blocker
pair also makes that original inventory historical. This phase records those boundaries rather than
altering the prior intake evidence.

## Retry condition and status boundary

The integration lane must master-accept the intake prerequisite. An accountable reviewer must
preserve and hash one lawful immutable primary or authoritative source, select one exact proposition
and pinpoint locator, transcribe every incorporated definition, ordered binder, hypothesis,
conclusion, proof boundary, correction, erratum, translation, and boundary case, and independently
approve the map. The review must formally define the intended path convention, rule out a
nonstandard arc reading, fix path-domain and nonemptiness conventions, select set versus space
scope, and preserve the boundary with `THM-M-0626`.

A later statement worker can then encode exactly that approved claim, minimize pinned imports,
serialize and hash the elaborated expression and environment, compile every credited transport,
and execute all four mutation classes.

This is a fail-closed blocker report, not completion of the statement node or any downstream node.
No statement receipt, worker `[_]`, proof, audit completion, theorem completion, or master
acceptance is claimed. Because the assigned deliverable did not pass, no
`.stage1-worker-selftest.json` is emitted.
