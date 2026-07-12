# Exact-statement gate: blocked

Item: `S56-M-0511-STATEMENT`  
Theorem: `THM-M-0511`  
Base revision: `e9d545372b66f73be63271b2fb408ef134d1d6f7`

## Decision

The exact Rademacher formula cannot yet be truthfully frozen as a Lean 4 proposition. The
authoritative repository wording says only that Hans Rademacher gave an exact formula for the
integer partition function. The intake identifies *On the Partition Function p(n)* as a plausible
primary source, but explicitly leaves its edition, pinpoint statement, formula, assumptions,
errata, and independent source review open.

Bibliographic metadata confirms DOI `10.1112/plms/s2-43.4.241`, the title, author, Proceedings of
the London Mathematical Society volume s2-43, and pages 241-254. It dates the printed article to
1938, which already disagrees with the repository's untrusted year 1937. The publisher's full text
was not available for inspection in this run. Bibliographic metadata does not expose the theorem
formula and therefore cannot settle the exact statement.

In particular, the following source-dependent choices remain unresolved:

- the precise finite sum `A_k(n)`, its residue range, coprimality condition, exponential sign, and
  Dedekind-sum or multiplier normalization;
- placement of constants and powers of `k`, and the exact hyperbolic-sine/derivative expression;
- whether the equality is real- or complex-valued and how reality of the series is expressed;
- the convergence assertion credited by the theorem and the indexing of the infinite series;
- the allowed natural-number values of `n`, especially `n = 0`, and the real extension used by the
  derivative.

Published modern displays vary across those conventions. Choosing one by familiarity would be a
substituted theorem, while defining `A_k` abstractly would weaken the claim into a parameterized
interface. Consequently there is no canonical expression to fingerprint, no credited alternate
transport, and no meaningful removed-hypothesis, changed-domain, binder-scope, or boundary mutation
test. The first failed gate is the canonical mathematical claim freeze in section 5, before the
Lean statement gate in section 5.1.

## Pinned Lean boundary

The existing `IntakeProbe.lean` was re-elaborated with the pinned toolchain. It confirms only that
mathlib supplies `Fintype (Nat.Partition n)`, complex exponential, real square root and hyperbolic
sine, derivatives, and infinite-sum APIs. A narrow pinned-mathlib search found partition generating
function infrastructure but no Rademacher partition formula or Dedekind-sum definition. Hits for
`Rademacher` concern the unrelated differentiability theorem. This distinguishes an available Lean
environment from the missing source statement; it is not a canonical target and receives no
statement or proof credit.

The environment is Lean 4.29.0 at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. Existing `.lake` artifacts were used read-only; no
update, build, clone, fetch, or dependency mutation was run.

## Validation evidence

Commands ran from the worker clone on 2026-07-12 (Asia/Shanghai).

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups; 1546 uniform-L0 Lean 4 targets; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0511` | 0 | rank 885; planned; legacy artifacts unaccepted; theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0 at the commit above |
| `cd Formalizations/Lean && lake --version` | 0 | Lake version above |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | `651c8a...1d2` and `321626...d81` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib revision above |
| repository search for the theorem ID, Chinese/English title, and `partition function p(n)` | 0 | only sparse source metadata and the intake dossier; no exact formula or formal target |
| pinned-mathlib search for `Rademacher`, `Dedekind sum`, and `partition function` | 0 | unrelated differentiability theorem and partition generating-function prose; no target declaration |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0511/IntakeProbe.lean` | 0 | all bounded substrate API checks elaborated; no canonical theorem asserted |
| scoped forbidden-marker search over target Lean files | 1 | expected no-match exit; no prohibited Lean marker found |
| `python3 -m json.tool Stage1_Instances/THM-M-0511/instance.json` | 0 | intake JSON remains syntactically valid |
| `python3 -m json.tool Stage1_Instances/THM-M-0511/task-dag.json` | 0 | open task DAG remains syntactically valid |

## Retry condition and boundary

An accountable reviewer must preserve and hash an immutable full-text primary-source edition,
transcribe the exact result with a page/formula locator and all incorporated definitions, reconcile
the 1937/1938 discrepancy and any errata, and independently approve a symbol-by-symbol crosswalk.
Only then can a statement worker encode the same claim, minimize imports, serialize the elaborated
expression, compile checked transports, and execute all four required mutation classes.

The statement node remains `[ ]` and blocked. The dossier remains `planned` with root vector
`[H1, M3, R4]`, `audit_complete: false`, and `theorem_complete: false`. The assigned deliverable was
not genuinely self-tested, so no `.stage1-worker-selftest.json` is emitted.
