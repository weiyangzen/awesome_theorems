# THM-M-0128 statement revalidation: blocked

Item: `S56-M-0128-STATEMENT`

Worker base: `6cff7bae0e4547cf9ad8b7abaae20d1abb9fe049`

Base tree: `28c148dbd84fbd549c749f060c92c9a3f00b16d0`

Revalidated: `2026-07-17` (`Asia/Shanghai`)

Verdict: `blocked`. No `.stage1-worker-selftest.json` is emitted, no state
transition is proposed, and no theorem-completion claim is made.

## Authoritative phase boundary

The sole task-state authority records `S56-M-0128-STATEMENT` as `[_]` with one
attempt. This is unfinished worker evidence, not master acceptance. Its intake
predecessor is also `[_]`. The current theorem-DAG node remains at v2 execution
rank 280 and has no direct hard parent, transitive hard ancestor, incoming hard
edge, reuse hint, or shared lemma group. The required parent inspection order
is therefore `[]`; the empty closure was inspected without transferring any
provider acceptance or proof credit.

The statement contract is a positive gate. It requires one exact
kernel-elaborated canonical target, an expression and environment fingerprint,
checked credited transports, and the removed-hypothesis, changed-domain,
changed-binder-scope, and boundary-case mutations. A truthful blocked result
may preserve the negative assessment but cannot close this predicate.

## Mathematical blocker

The tracked source evidence still identifies only the theorem label, Goro
Shimura attribution, year 1971, and the gloss "class field theory of CM
fields." The intake selects the CM-special-point family as provisional prose,
but no admitted immutable theorem passage fixes all of the following:

- the CM datum and concrete CM-type representation;
- the reflex field and reflex norm, including variance and codomain;
- the idele versus idele-class domain and quotient descent;
- arithmetic versus geometric Artin reciprocity and inversion;
- the canonical model, component, level, and special-point carrier;
- left versus right actions and point equality versus orbit/double-coset
  equality;
- ordered binders, hypotheses, conclusion, and degenerate cases.

Those choices change or can reverse the proposition. Supplying arbitrary
carriers and functions, or assuming the desired compatibility in a structure
field, would substitute or circularly assume a different theorem. The later
anchor audit and obligation-tree artifacts confirm the same root cut set,
`M0128-ROOT-IDENTITY`; they do not supply a source-authorized statement.

The pinned Lean environment exposes `NumberField.IsCMField` and
`NumberField.AdeleRing`. `Statement.lean` elaborates those two substrate
anchors, but deliberately declares no Shimura reciprocity proposition. Thus
there is still no canonical expression to fingerprint, no target import set to
prove minimal, no alternate encoding to transport, and no meaningful mutation
suite to run.

## Freshness and validator result

The current theorem DAG has SHA-256
`80cf05109d5b3776b7defe95fdb591b216894a57ecbb7180a59f315a67d487d5`;
the target dependency-context SHA-256 remains
`068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c`.
The canonical `dependency-reuse-ledger.json` is an older anchor-audit snapshot:
it binds graph `cb4b83c4...f675`, repository revision `74d4c272...940a`, and
claim order `(280, 2, S56-M-0128-ANCHOR_AUDIT)`. It passes validation only for
that recorded snapshot and fails the current statement claim's exact
graph/base binding. Because this worker is reporting a blocker and the
canonical path is already tracked, it is not rewritten into a misleading
self-tested statement ledger.

The HEAD contract resolves exactly one validator candidate:
`Stage1_Instances/THM-M-0128/check_statement.py`. It is tracked and unchanged
at Git blob `25b60d1e6f3216c53e5015d53eea953d9bcc0c79` (SHA-256
`212251f3154a8b8ca6747e983655e279ca754e875de6e23cdca50aa644db42b1`).
The required argv was run exactly as
`/usr/bin/python3 -I -B Stage1_Instances/THM-M-0128/check_statement.py`.
It exited 1 and emitted exactly one schema-valid
`stage1-validator-semantic-result/1.0` JSON object with
`status=failed`, `verdict=repair_required`, `phase_accepted=false`, and
`first_failed_gate=S01-ARTIFACTS.negative_evidence_validation`; its message is
`theorem DAG changed`. Exit status alone is not interpreted as acceptance.

The validator's fail-closed result is correct for the current bytes: it is
pinned to the former DAG SHA-256 `3d32f808...afa`, former statement ledger
bytes, and a former worker packet that is absent in this fresh clone. Worker
instructions forbid refreshing or replacing this scheduler-owned validator.
Consequently there is no lawful successful statement self-test at this base.

## Commands and results

No dependency update, build, clone, fetch, or `.lake` mutation was performed.
The automation-provided `.lake` symlink was used read-only.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 1546 uniform-L0 targets, the v2 DAG, seven-phase contract, and execution skill passed |
| `python3 Docs/tools/check_stage1_theorem_dag_v2.py` | 0 | 1546 theorem nodes, 10822 states, typed edges/groups, deterministic order, and acyclicity passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0128` | 0 | execution rank 46, planned lifecycle, legacy artifacts unaccepted, theorem incomplete |
| pinned `lake env lean ../../Stage1_Instances/THM-M-0128/Statement.lean` from `Formalizations/Lean` | 0 | the two substrate declarations elaborated; no canonical target exists |
| `/usr/bin/python3 -I -B Stage1_Instances/THM-M-0128/check_statement.py` | 1 | one typed semantic JSON object reported stale internal bindings and no phase acceptance |
| repository ledger validation against its recorded graph/base | 0 | the empty anchor-audit snapshot is internally valid for its own recorded inputs |
| repository ledger validation against current graph/base | 1 expected | rejected the stale graph binding before any reuse decision could be credited |
| focused acceptance/adapter unit tests | 27 passed, 3 environment failures | pure semantic and binding tests passed; two real-bubblewrap cases fail because `/usr/bin/bwrap` has unsafe ownership/permissions in this sandbox, and one ordering assertion sees that same environmental failure first |
| `git diff --check -- Stage1_Instances/THM-M-0128` | 0 | no whitespace diagnostics |
| `test ! -e .stage1-worker-selftest.json` | 0 | no self-test handoff was manufactured |

The stream-fd permission diagnostics prepended by the command runner are
sandbox diagnostics, not validator stdout. The validator process's captured
stdout itself is the single JSON object described above.

## Retry condition

First, accountable source review must admit one immutable exact theorem passage
with its edition/theorem/page locator, incorporated definitions, assumptions,
corrections, errata, translation, and every reciprocity/action convention. The
corresponding concrete CM/reflex/idele/Artin/canonical-model/special-point Lean
object model must then be implemented or pinned. A future statement execution
can encode only that approved claim, minimize imports, fingerprint the
elaborated expression and environment, compile each credited transport, and
run all four mutation classes.

Separately, the scheduler must provide a future immutable base whose unchanged
statement validator and canonical statement ledger are bound to the current
authority inputs. Until both conditions hold, the first mathematical gate
remains
`S02-EXACT-TARGET.exact_source_statement_identity_and_convention_selection`,
while the immediate current-base self-test failure is
`S01-ARTIFACTS.negative_evidence_validation`. `audit_complete=false` and
`theorem_complete=false` remain mandatory.
