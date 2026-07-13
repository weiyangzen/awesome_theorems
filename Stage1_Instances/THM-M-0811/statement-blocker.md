# THM-M-0811 statement-phase blocker

- Item: `S56-M-0811-STATEMENT`
- Base revision: `561d83df037004ceb2259292d7c63be930b40391`
- Attempt date: 2026-07-13 (Asia/Shanghai)
- Verdict: blocked; no statement receipt or theorem-completion claim

## First failed gate

The exact-statement gate in section 5.1 of `Docs/Stage1_Blueprint_rev-5.6.md` cannot be
truthfully entered from the recorded source boundary. The catalog supplies only the name
"Eulerian path theorem" and the gloss "necessary and sufficient conditions for the existence of
an Eulerian path." It does not state the conditions or identify an immutable modern theorem
passage. Stage0 explicitly leaves the exact definitions and assumptions open.

This omission is proposition-changing, not editorial. The target could use a simple graph or a
multigraph, full-graph connectivity or connectivity only on non-isolated vertices, fixed or
existential endpoints, and an open trail or a convention that includes circuits. It must also
settle finiteness and empty, edgeless, and isolated-vertex cases. For example, a single edge plus
an isolated vertex has an Eulerian trail but is not connected; an edgeless two-vertex simple graph
admits a nil Eulerian walk under the pinned definition but is not connected; an empty vertex type
makes support connectivity and the zero-odd condition vacuous while preventing existential
endpoints; and a cycle distinguishes an Eulerian trail from an endpoint-distinct open trail.
Parallel edges also make the historical multigraph model materially different from a simple graph.

The integrated intake node is provisional `[_]`, its receipt is unaccepted, and its exact source
and graph-model decisions remain open. Selecting the familiar zero-or-two-odd-vertices criterion
now would therefore invent binders, hypotheses, connectivity conventions, and boundary policy.

Consequently there is no canonical expression to elaborate, no honest minimal-import claim, and no
expression or environment fingerprint. Checked transports and the removed-hypothesis,
changed-domain, changed-binder-scope, and boundary mutation classes are not runnable before the
canonical binders and premises exist. The root remains `[H1, M3, R4]`; this statement phase is not
self-tested complete.

## Pinned Lean boundary

The existing `IntakeProbe.lean` was re-elaborated with the pinned environment. Its sole direct
import, `Mathlib.Combinatorics.SimpleGraph.Trails`, exposes the Eulerian-walk predicate, supplied-
walk characterizations, and the necessary endpoint-parity and zero-or-two-odd-degree results. All
six `#check` commands passed. The same pinned module explicitly lists the converse existence
theorem as a TODO. The probe import is not claimed minimal for an unidentified target, and the
necessary direction receives no statement or proof credit for the missing iff.

The environment was Lean 4.29.0 at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` (tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`). The automation-provided `.lake` symlink and pinned
artifacts were used read-only. No `lake update`, `lake build`, dependency clone or fetch, or other
`.lake` mutation was run.

## Commands and exact results

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0811` | 0 | rank 1370; `planned`; `L0/rework_required`; no legacy slot; theorem incomplete |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | revision `561d83df037004ceb2259292d7c63be930b40391`; tree `6eb02475bf5a70139d60615c924b31c930efc2bb` |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `cd Formalizations/Lean && lake --version` | 0 | Lake `5.0.0-src+98dc76e` |
| `cd Formalizations/Lean && git -C .lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | revision `8a178386...eea95`; tree `bdc39a...5e2b`; package worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0811/IntakeProbe.lean` | 0 | all six adjacent Eulerian APIs elaborated; complete output SHA-256 `0b8fcd3037e960843ceda587a3b90419037822a78cfceba648fa7eab0ee9416b` |
| `python3 -B Stage1_Instances/THM-M-0811/check_intake.py` | 1 | the pre-existing intake validator expects the authoritative intake item to remain `[ ]`, but the current DAG records `[_]`; this stale intake-only assertion is outside the assigned statement phase and was not modified |
| `rg -n '\\b(sorry|admit|sorryAx|axiom|constant|opaque|unsafe)\\b' Stage1_Instances/THM-M-0811 --glob '*.lean'` | 1 | expected no-match result; no prohibited declaration token |
| `python3 -m json.tool Stage1_Instances/THM-M-0811/statement-blocker.json` | 0 | blocker is valid JSON |
| scoped Python invariant check over `statement-blocker.json` | 0 | identity, base, blocked/open state, null target/import/hash/fingerprint, false completion flags, unchanged `H1/M3/R4`, four unrunnable mutations, and absent worker manifest agree |
| `git diff --check -- Stage1_Instances/THM-M-0811` plus per-file no-index checks | 0 | no whitespace diagnostics; no-index exit 1 for each new file means only that the file is new |
| `test ! -e .stage1-worker-selftest.json` | 0 | worker self-test manifest is absent as required for a blocked phase |

## Unblocking condition

An accountable source owner must preserve and hash one lawful complete modern edition, select and
independently approve its exact result and proof boundary, and map every incorporated definition,
binder, hypothesis, conclusion, correction, historical relationship, and boundary case. That
decision must freeze graph model, finiteness, connectivity and isolated-vertex policy, endpoints,
circuit inclusion, and parity formulation. The integration lane must also revalidate and accept the
intake dependency. A later statement run can then encode the same claim, establish minimal pinned
imports, serialize its elaborated expression and environment, check transports, and run all four
mutation classes.

Until those prerequisites hold, no exact statement, proof, audit completion, or theorem completion
is claimed. Because the assigned phase is not genuinely self-tested to its completion gate, no
`.stage1-worker-selftest.json` is emitted.
