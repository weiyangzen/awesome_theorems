# Exact-statement gate: blocked

Item: `S56-M-1367-STATEMENT`

Theorem: `THM-M-1367`

Base revision: `a07fc18923e20fd2876d04809a15d5b31e55512f` (tree
`1268491c8f2677e1c8e38754fa93dd190892e69e`).

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the authoritative repository record.
That record supplies only the family name Peixoto's theorem, Mauricio Peixoto, 1962, and the gloss
"structural stability of two-dimensional systems." It supplies no cited proposition, numbered
theorem, incorporated definitions, ordered binders, hypotheses, conclusion, proof boundary,
correction history, or boundary cases. Stage0 explicitly leaves the exact definitions and
premises, proof route, equivalent forms, axioms, formal status, and artifacts open. The catalog's
verified label is untrusted metadata under rev-5.6.

The inspected source leads expose material alternatives rather than selecting a root. Peixoto's
1962 *Topology* article is a matching primary bibliographic lead, but its exact theorem text,
definitions, page-level premise/conclusion map, and proof boundary have not been preserved and
independently admitted. The 1963 same-title "A further remark" is a material follow-up whose impact
has not been reviewed. The authorial Scholarpedia overview distinguishes at least:

- a characterization of structurally stable surface flows by hyperbolicity, recurrence, and
  saddle-connection conditions;
- openness of the structurally stable locus; and
- density, genericity, or open-density results whose orientability and regularity boundaries
  matter.

The catalog selects neither one of these claims nor a source-defined conjunction. It also does not
fix the surface class, compactness, connectedness, orientability, boundary policy, vector-field and
flow model, differentiability index, function-space topology, orbit-equivalence convention, or the
meaning of hyperbolicity, recurrence, saddle connections, and genericity. Those choices change the
proposition. Choosing a familiar formulation would invent, broaden, strengthen, or substitute
mathematics rather than elaborate the exact received target.

The intake consequently leaves the canonical statement, Lean module and expression, target
expression hash, and canonical-target environment fingerprint null at `[H1, M4, R4]`. Without a
canonical expression, no import set can be certified minimal, no alternate encoding can receive a
checked transport, and the required removed-hypothesis, changed-domain, changed-binder-scope, and
boundary-case mutations are undefined rather than passed. No `Statement.lean`, axiom, placeholder,
assumed structural-stability predicate, weakened special case, or broadened theorem was introduced.

The intake prerequisite currently has provisional worker state `[_]`, not master-accepted state
`[x]`. Its receipt declares `accepted: false` and has no accepted receipt ID. Rev-5.6 permits this
dependency-ordered attempt, but dependency acceptance remains independently necessary before a
future statement transition can be master accepted. The first substantive failure here is the
missing exact source-statement identity and variant selection.

## Pinned Lean Boundary

The existing discovery-only `IntakeProbe.lean` re-elaborates with the pinned environment. Its five
direct imports expose twelve adjacent manifold, vector-field, integral-curve, flow, orbit,
semiconjugacy, omega-limit, homeomorphism, and diffeomorphism interfaces. All checks pass. The probe
defines no topology on vector fields, generated-flow perturbation relation, structural-stability or
orbit-equivalence predicate, hyperbolicity or saddle-connection predicate, genericity result, or
canonical Peixoto proposition. Its successful elaboration therefore receives no statement,
minimal-import, anchor, or proof credit.

A bounded case-insensitive search in repo-local Lean and pinned mathlib found no declaration under
Peixoto or dynamical structural-stability terms. This is narrow discovery evidence, not the
downstream immutable anchor audit or a claim of global absence.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` (tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`). The automation-provided
`Formalizations/Lean/.lake` link to the canonical pinned artifacts was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, or other `.lake` mutation was run.

## Validation Evidence

Commands ran in this worker clone on 2026-07-13 (`Asia/Shanghai`), from the repository root unless
a different working directory is shown.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and execution skill presence passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1367` | 0 | rank 977; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` before editing | 0 | only the automation-provided untracked `.lake` link existed; the base revision and tree are recorded above |
| `sha256sum` over the authority, source, intake, probe, toolchain, manifest, and relevant pinned mathlib inputs | 0 | hashes agree with `statement-blocker.json` |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, target `x86_64-unknown-linux-gnu`, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release |
| `cd Formalizations/Lean && lake --version` | 0 | Lake `5.0.0-src+98dc76e`, Lean 4.29.0 |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'`; package status | 0 | pinned revision and tree agree with the fingerprint; package worktree is clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1367/IntakeProbe.lean` | 0 | twelve adjacent pinned APIs elaborated; no canonical target or proof body was declared; complete output SHA-256 `f56fda86120182e3f5de5330cc05f1ddf4e87155cc3350f6b0796d029ea44126` |
| bounded repo-local and pinned-mathlib Lean `rg` search for Peixoto and dynamical structural stability | 1 | expected no-match exit; discovery only, not an anchor audit |
| `python3 -B Stage1_Instances/THM-M-1367/check_intake.py` | 1 | historical intake checker stops at line 155 because it freezes intake authority state `[ ]` while the current authoritative DAG records provisional `[_]`; this statement phase records rather than rewrites historical evidence |
| `rg -n --glob '*.lean' '\b(sorry\|admit)\b\|\bsorryAx\b\|^[[:space:]]*(axiom\|constant\|opaque)\b\|^[[:space:]]*unsafe\b' Stage1_Instances/THM-M-1367` | 1 | expected no-match exit; no `sorry`, `admit`, `sorryAx`, axiom, bodyless declaration, or unsafe declaration |
| `python3 -m json.tool Stage1_Instances/THM-M-1367/statement-blocker.json` | 0 | the finalized structured blocker parsed as valid JSON |
| scoped statement-blocker invariant assertions | 0 | IDs, open state, null target and imports, unchanged vector, four undefined mutations, false completion flags, exact two-file change scope, and absent self-test agree |
| `git diff --check -- Stage1_Instances/THM-M-1367` plus `git diff --no-index --check -- /dev/null <each blocker artifact>` | 0 for the scoped check; expected added-file status 1 with empty output for each no-index check | no whitespace diagnostics in either blocker artifact |
| `test ! -e .stage1-worker-selftest.json` | 0 | the self-test manifest is absent because the exact-statement deliverable did not pass |

The historical intake checker is frozen to its original authority state and nine-file intake
inventory. Integration subsequently promoted the intake worker evidence to provisional `[_]`, so
the checker already fails before its inventory assertion. Adding these two statement artifacts also
makes that intake-only inventory historical. This run records the limitation instead of rewriting
the intake checker, intake receipt, instance, task DAG, generated blueprint, or authoritative
execution DAG to manufacture agreement.

## Retry Condition And Status Boundary

The integration lane must master-accept refreshed intake evidence. Accountable reviewers must then
lawfully preserve and hash one complete primary or authoritative source edition, select and
transcribe one exact result or explicit conjunction with pinpoint locators and every incorporated
definition, reconcile the 1963 further remark and any corrections or errata, and independently
approve the source crosswalk. They must freeze the surface and boundary class, orientation,
regularity and topology, vector-field and flow model, orbit equivalence, hyperbolicity, recurrence,
saddle connections, genericity conclusion, ordered binders, hypotheses, conclusion, foundation
profile, and every degenerate case.

A later statement worker can then encode that same claim with real Lean definitions, minimize its
pinned imports, serialize and hash the elaborated expression and environment, compile every
credited transport, and run all four mutation classes.

This is a blocked-attempt record, not completion of the statement node or any downstream node. The
root remains `[H1, M4, R4]`, with `audit_complete: false` and `theorem_complete: false`; no debt
change is proposed. Because the assigned phase is not genuinely self-tested to its completion gate,
no `.stage1-worker-selftest.json`, node receipt, worker `[_]`, or master acceptance is claimed.
