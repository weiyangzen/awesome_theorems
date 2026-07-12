# Exact-statement gate: blocked

Item: `S56-M-0227-STATEMENT`

Theorem: `THM-M-0227`

Base revision: `a8aba97a7ef2ff387e7814fe517e1b35524a04dc`

## Decision

The statement item remains `[ ]`. Its intake prerequisite has provisional worker state `[_]`, not
master acceptance. Independently, no exact Lean 4 target can be truthfully elaborated from the
repository's authoritative material.
The complete mathematical wording is the gloss "A simply connected domain is conformally
equivalent to the unit disk." The source record supplies no bibliographic work, immutable edition,
theorem/page, incorporated definitions, complete assumptions, errata disposition, or independent
source review. Stage0 explicitly leaves the exact definitions and premises open, and the accepted
intake therefore leaves both the canonical mathematical statement and formal target null.

The missing decisions change the proposition rather than merely its notation:

- whether "domain" carries nonemptiness, openness, and connectedness definitionally;
- the properness hypothesis excluding the whole complex plane, which is essential;
- the complex-plane ambient space and the convention represented by `IsSimplyConnected`;
- whether a biholomorphism is encoded by subtype maps, ambient inverse maps, or a homeomorphism with
  analytic forward and inverse maps;
- holomorphic equivalence versus mathlib's broader local `ConformalAt`, which also admits
  antiholomorphic behavior;
- existence alone versus a base-point/derivative-normalized result and any uniqueness clause;
- binder order and the empty, whole-plane, unit-disk, unbounded-domain, and boundary cases.

Choosing conventional answers would manufacture a nearby textbook theorem. Encoding the missing
mathematics behind an opaque predicate or assumed interface would instead be a placeholder. Both
are forbidden by rev-5.6. There is consequently no canonical expression for which minimal imports,
an elaborated-expression fingerprint, checked alternate transports, or meaningful
removed-hypothesis, changed-domain, changed-binder-scope, and boundary mutations can be certified.
The first failed gate is exact source-statement identification and its definition chain.

## Pinned Lean boundary

The existing `IntakeProbe.lean` was re-elaborated with the pinned environment. Its four direct
imports expose `Complex.UnitDisc`, `IsSimplyConnected`, analyticity, homeomorphisms, and local
conformality. This establishes only that adjacent APIs are usable. A bounded exact-topic search
found no Riemann-mapping or biholomorphic-unit-disk declaration in pinned mathlib or the repository
Lean tree. Neither result identifies the missing target, proves import minimality for it, completes
an anchor audit, or supplies statement/proof credit.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned
mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`. The automation-provided `.lake`
symlink and its canonical artifacts were used read-only. No update, build, clone, fetch, or
dependency mutation was run.

## Validation record

Commands ran from this worker clone on 2026-07-13 (Asia/Shanghai).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0227` | 0 | rank 939; planned; `L0/rework_required`; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all` (pre-edit) | 0 | only the automation-provided `Formalizations/Lean/.lake` symlink was untracked |
| repository `rg` search for the theorem ID, Chinese/English name, and exact catalog gloss | 0 | found only the underspecified catalog record, Stage0 projection, target listing, and accepted intake; no exact source proposition |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | Lean 4.29.0 at the commit above; Lake 5.0.0 at the same Lean revision |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib revision above |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0227/IntakeProbe.lean` | 0 | ten adjacent unit-disk, openness, simple-connectedness, analyticity, homeomorphism, and conformality API checks elaborated; no target theorem was stated |
| pinned mathlib/repository Lean `rg` search for Riemann mapping, biholomorphism, and conformal equivalence to a unit disk | 1 | expected no-match result; bounded discovery evidence only, not a global absence or anchor-audit claim |
| `python3 Stage1_Instances/THM-M-0227/check_intake.py` | 1 | known intake-only checker failure: it requires the intake worker's absent root self-test manifest; this statement run does not recreate or rewrite intake evidence |
| `sha256sum` over the blueprint, manifests, skill, source records, toolchain files, and probe | 0 | hashes recorded in `statement-blocker.json`; mathlib pin independently matched the Lake manifest |
| prohibited-construct `rg` scan over owned Lean files | 1 | expected no-match result; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `python3 -m json.tool Stage1_Instances/THM-M-0227/statement-blocker.json` | 0 | blocker JSON is syntactically valid |
| `git diff --check -- Stage1_Instances/THM-M-0227` plus `git diff --no-index --check -- /dev/null` for each blocker file | 0 / 1 each | no tracked whitespace diagnostic; each no-index command has expected added-file difference status and no diagnostic |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest intentionally absent because the statement deliverable did not pass |

## Retry condition

An accountable reviewer must preserve and hash an immutable primary or authoritative source,
select and transcribe its exact theorem with all incorporated definitions and assumptions, audit
errata, and independently approve the source-to-target mapping. A later statement worker can then
encode that same claim using real Lean definitions, minimize pinned imports, serialize and hash the
elaborated expression, check every credited alternate transport, and execute all four required
mutation classes.

This records the first failed gate. It does not complete this statement node or any downstream
node. The root remains `[H1, M4, R3]`; audit and theorem completion remain false. The assigned phase
is not genuinely self-tested, so `.stage1-worker-selftest.json` is intentionally absent.
