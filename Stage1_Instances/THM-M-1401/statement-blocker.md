# Exact-statement gate: blocked

Item: `S56-M-1401-STATEMENT`

Theorem: `THM-M-1401`

Base revision: `1f79a3f74a8e206d44c27513f4016a26dd7050e3`

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the authoritative repository record.
That record gives only the title `符号动力学` ("symbolic dynamics"), attributes it to many
mathematicians in the twentieth century, and glosses it as `动力系统的符号表示` ("symbolic
representation of dynamical systems"). These words name a field and purpose, not a truth-valued
proposition. They supply no phase space, time action, alphabet, symbolic space, partition or coding
map, ordered binders, hypotheses, conclusion, or exceptional cases. Stage0 explicitly leaves the
exact definitions, premises, proof route, equivalent forms, axioms, and machine artifacts open.
The source label `已验证` is explicitly untrusted under rev-5.6.

The repository also has a separate physics-catalog topic `符号动力学理论`, attributed to Morse and
Hedlund in 1938/1940 and glossed as describing complex dynamics using symbolic sequences. It gives
no publication or theorem locator, and no repository record identifies it as the source statement
for this mathematical target. It is discovery context only and cannot silently select a root.

Many inequivalent claims fit the metadata: an itinerary construction from a partition, a
shift-commuting law, a continuous or measurable factor map, an embedding or conjugacy, a
finite-to-one coding, a subshift realization or finite-type presentation, or a Markov-partition
consequence. They differ in direction, regularity, strength, hypotheses, and treatment of boundary
points and nonunique names. Selecting one would narrow or substitute the received target. Several
neighboring catalog items separately own the shift map, entropy, Bernoulli shifts, and Markov
partitions, which further rules out using one of those as a convenient replacement.

Consequently there is no canonical human proposition from which to derive a minimal exact-target
import, normalized kernel-expression fingerprint, credited alternate transport, or meaningful
removed-hypothesis, changed-domain, changed-binder-scope, and boundary mutations. The rev-5.6
statement gate fails at exact source-statement identity before proof or anchor evidence may be
inspected. No theorem declaration, axiom, placeholder, weakened special case, or broadened abstract
interface was added.

## Pinned Lean boundary

The existing `IntakeProbe.lean` directly imports `Mathlib.Data.Stream.Init` and
`Mathlib.Dynamics.PeriodicPts.Defs`. It re-elaborates these six generic interfaces:

- `Stream'`;
- `Stream'.tail`;
- `Stream'.get_tail`;
- `Function.Semiconj`;
- `Function.Semiconj.iterate_right`; and
- `Function.Semiconj.mapsTo_periodicPts`.

These interfaces show only that pinned stream, semiconjugacy, iteration, and periodic-point
ingredients are available. They do not identify a symbolic-dynamics proposition, and the two
imports are not claimed to be minimal for an unknown target. The successful probe receives no
statement, anchor, or proof credit.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. The `lean-toolchain` SHA-256 is
`651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`; the
`lake-manifest.json` SHA-256 is
`321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`; and the probe SHA-256 is
`ab971826420847892520efb2a0b5005e91ba122f5336e0d3307817ca1d798132`.

The pre-existing `Formalizations/Lean/.lake` link points to the canonical checkout's pinned
artifacts and was used read-only. No update, build, dependency clone, fetch, or other `.lake`
mutation was run.

## Validation evidence

Commands ran in this worker clone on 2026-07-12 (Asia/Shanghai).

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1401` | 0 | rank 900, planned, legacy artifacts unaccepted, theorem incomplete |
| `git status --short && git rev-parse HEAD && git rev-parse HEAD^{tree}` | 0 | base revision above and tree `5024086eeb6994ff53242ac82b32b2d9af8b2462`; only the pre-existing untracked `.lake` link was present before this phase |
| `rg -n -C 6 '符号动力学\|动力系统的符号表示\|符号动力学理论\|用符号序列描述复杂动力学' Docs/researches/math_theorems.md Docs/researches/physics_theorems.md Docs/Stage0_Blueprint.md` | 0 | found only the topic/gloss records and Stage0's open fields; no exact proposition or pinpoint source |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0 at the commit above |
| `(cd Formalizations/Lean && lake --version)` | 0 | Lake version above |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json Stage1_Instances/THM-M-1401/IntakeProbe.lean` | 0 | hashes agree with the fingerprint above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib revision above |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1401/IntakeProbe.lean)` | 0 | all six generic candidate interfaces elaborated; no target theorem was stated |
| `rg -n 'subshift\|shift space\|symbolic dynamics\|Bernoulli shift' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 1 | expected no-match exit in this bounded name search; not a complete anchor audit |
| `rg -n --glob '*.lean' '\b(sorry\|admit)\b\|\bsorryAx\b\|^[[:space:]]*axiom\b' Stage1_Instances/THM-M-1401` | 1 | expected no-match exit; no prohibited proof hole or axiom in target Lean source |
| `python3 -m json.tool Stage1_Instances/THM-M-1401/statement-blocker.json` | 0 | structured blocker is valid JSON |
| `git diff --check -- Stage1_Instances/THM-M-1401` | 0 | tracked-diff whitespace check passed |
| `for f in Stage1_Instances/THM-M-1401/statement-blocker.{md,json}; do git diff --no-index --check -- /dev/null "$f"; test $? -le 1; done` | 0 | both untracked owned files passed the added-file whitespace check; diff exit 1 was accepted as normal |

## Retry condition and status boundary

An accountable reviewer must preserve and hash an immutable primary or authoritative source,
identify and transcribe one exact proposition with a pinpoint locator and incorporated definitions,
audit errata, reconcile the separate catalog records, and independently approve the
source-statement crosswalk. The selection must freeze the phase space and time action, alphabet and
one- or two-sided symbolic space, partition or coding construction, direction and representation
strength, all regularity and structural hypotheses, ordered binders, conclusion, and boundary,
empty, null-set, and nonunique-coding cases. A later statement worker can then encode that same
claim, minimize its pinned imports, serialize and hash the elaborated expression, check alternate
transports, and run all four required mutation classes.

This is the first failed gate, not completion of the statement node or a downstream node. The root
remains `[H4, M4, R4]`, with `audit_complete: false` and `theorem_complete: false`; no debt-vector
change is proposed. The assigned phase is not genuinely self-tested to its completion gate, so no
`.stage1-worker-selftest.json` is emitted and no master-acceptance receipt is claimed.
