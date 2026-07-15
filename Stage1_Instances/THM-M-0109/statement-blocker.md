# Exact-statement gate: blocked

Item: `S56-M-0109-STATEMENT`

Theorem: `THM-M-0109`

Base revision: `d5771f240b8fe26277d018c90fec963af76ed7f2` (tree
`f274a52fcf9e5edcd6b8f8dd43726122a041af50`).

## Decision

There is no exact proposition to elaborate. The repository name conventionally
indicates Chow's lemma, but the only supplied mathematical gloss is "properties
of the coordinate ring of an algebraic variety." That gloss names no property,
base, finiteness or separation hypotheses, domains, ordered binders,
conclusion, or boundary cases. The record has no publication, edition, theorem
or page locator, quotation, definitions, proof boundary, translation review,
correction, or errata disposition that reconciles these descriptions.

The candidate readings are materially different. The scheme-theoretic Chow
lemma concerns a projective model or modification under formulation-dependent
hypotheses. The gloss could instead intend finite generation, a polynomial
quotient presentation, or Noetherianity of an affine coordinate ring. Choosing
either family would invent or substitute mathematics absent from the received
claim. Rev-5.6 therefore makes the ambiguity a hard blocker.

Consequently the canonical human statement, Lean expression, minimal imports,
expression and environment fingerprints, checked alternate transports, and
removed-hypothesis, changed-domain, binder-scope, and boundary mutations are
all undefined. The statement gate fails closed before proof evidence is
inspected. Lifecycle remains `planned`, the vector remains `[H4, M4, R4]`, and
both audit and theorem completion remain false.

The prerequisite is also only provisional: `S56-M-0109-INTAKE` is `[_]`, not
master-accepted `[x]`. Concurrent inspection is permitted, but no statement
transition can be accepted before dependency-ordered review.

## Legacy boundary

The unchanged legacy module
`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_033.lean` elaborates in the
pinned environment. That is discovery evidence only. Its coordinate-ring
wrappers prove auxiliary finite-type facts, not the unidentified root. Its
`AlgebraicGeometry.StatementShape` also uses
`AlgebraicGeometry.IsProper` as a properness-only placeholder for projectivity.
The module itself records this limitation, and the intake expressly forbids
that substitution. Its six imports are therefore not a minimal import set for
an absent canonical target, and elaborating it grants no statement or proof
credit.

## Pinned environment

- Lean toolchain: `leanprover/lean4:v4.29.0`; Lean commit
  `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Lake: `5.0.0-src+98dc76e`.
- mathlib revision: `8a178386ffc0f5fef0b77738bb5449d50efeea95`,
  tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b`.
- The automation-provided canonical `.lake` symlink was used read-only. No
  update, build, clone, fetch, or dependency mutation was run.

## Validation evidence

Commands ran in this worker clone on 2026-07-15 (`Asia/Shanghai`).

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0109` | 0 | rank 33, planned, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions above |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean AwesomeTheorems/Stage1/S1_M_033.lean` | 0 | unchanged legacy discovery module elaborated with empty output; no canonical-target credit applies |
| bounded pinned-mathlib search for the theorem name and literal gloss | 1 | expected no-match result; this is not a completed anchor audit |
| prohibited-declaration scan of the legacy discovery module | 1 | expected no-match result; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | pinned mathlib revision and tree above |
| `python3 -m json.tool Stage1_Instances/THM-M-0109/statement-blocker.json` and scoped `jq -e` assertions | 0 | JSON parsed; blocked identity, null target/imports/fingerprints, unchanged vector, four unavailable mutations, false completion flags, changed paths, and no-self-test boundary agree |
| `git diff --check -- Stage1_Instances/THM-M-0109` plus `git diff --no-index --check /dev/null FILE` for each new blocker file | 0 wrapper result | no whitespace diagnostics; raw no-index commands returned only expected new-file difference status 1 |
| `test ! -e .stage1-worker-selftest.json` | 0 | no self-test packet because the statement gate failed |

The structured record in `statement-blocker.json` binds the input hashes,
commands, exclusions, failed gates, unchanged debt vector, and status boundary.

## Retry condition

Preserve and hash a lawful immutable primary publication or authoritative
catalog correction that reconciles the name, gloss, attribution, and date.
Transcribe one exact theorem with every incorporated definition, domain,
ordered binder, hypothesis, conclusion, proof boundary, terminology change,
translation decision, correction, erratum, and boundary case, then obtain
independent source approval. A later statement run can encode only that claim,
minimize its pinned imports, serialize its elaborated expression and
environment, compile every credited transport, and execute all four mutation
classes. The intake must also receive master acceptance before the statement
node can be accepted.

This blocker is the assigned phase's truthful result, not statement or theorem
completion. No `.stage1-worker-selftest.json`, statement receipt, `[_]` worker
state, statement fingerprint, canonical obligation, proof body, or proof credit
is emitted.
