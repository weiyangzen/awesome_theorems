# Exact-statement gate: blocked

Item: `S56-M-1425-STATEMENT`

Theorem: `THM-M-1425`

Base revision: `5ac2d33ee4b1a16fd90dca63313cd900ffc4bb50`

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the authoritative repository record.
The complete record gives only the title `随机吸引子` ("random attractor"), attributes it to many
mathematicians in the twentieth century, and glosses it as `随机系统的吸引子` ("attractors of
random systems"). This names an object or topic family, not a truth-valued proposition. It gives no
primary-source locator, ordered binders, hypotheses, conclusion, or exceptional cases. Stage0
leaves the exact definitions and premises open, and the catalog label `已验证` is untrusted under
rev-5.6.

Many inequivalent roots fit those words. An attractor may be pullback, forward, weak, global,
local, uniform, compact, set-valued, or a singleton. A theorem may assert existence, uniqueness,
strict or forward invariance, omega-limit representation, minimality, robustness, upper
semicontinuity, or synchronization. Those choices require different noise bases, time actions,
cocycles, random-set measurability conventions, initial-family classes, set distances, convergence
modes, quantifier orders, hypotheses, and boundary cases. A deterministic global-attractor result,
a generic omega-limit lemma, or the neighboring random-dynamical-system or multivalued target
would also be a substitution rather than an encoding of this record.

The intake records Crauel and Flandoli's 1994 paper and its Theorem 3.11 only as a strong
bibliographic discovery candidate. The catalog does not cite or select it, and the dossier has no
immutable reviewed copy, exact definition-and-assumption crosswalk, errata disposition, or
independent source approval. Choosing that existence theorem, or any other familiar
random-attractor result, would therefore invent missing mathematics.

Consequently there is no canonical human proposition from which to derive a minimal import,
elaborated expression fingerprint, checked alternate transport, or meaningful removed-hypothesis,
changed-domain, changed-binder-scope, and boundary mutations. The rev-5.6 statement gate fails at
exact source-statement identity before proof or anchor evidence may be inspected. No theorem
declaration, assumed interface, axiom, placeholder, weakened example, or broadened target was
introduced.

## Pinned Lean boundary

The existing `IntakeProbe.lean` directly imports:

- `Mathlib.Dynamics.Flow`;
- `Mathlib.Dynamics.OmegaLimit`;
- `Mathlib.Topology.MetricSpace.HausdorffDistance`; and
- `Mathlib.MeasureTheory.Constructions.BorelSpace.Basic`.

It re-elaborates generic `Flow`, invariant-set, omega-limit, compactness, Hausdorff-distance,
measurability, and convergence interfaces. These APIs only demonstrate that possible substrate is
present. They state no random-attractor theorem, and the imports are not claimed to be minimal for
an unknown canonical target. A bounded topic search of pinned mathlib found no random-attractor,
pullback-attractor, or random-dynamical-system declaration; its one match was unrelated prose about
a finite random set. Neither the probe nor the search receives statement, anchor, or proof credit.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. The `lean-toolchain` SHA-256 is
`651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`; the
`lake-manifest.json` SHA-256 is
`321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`; and the probe SHA-256 is
`7b014de287f0172351885f199be8c9e79c2f3e2da03ac63857915240b05fca41`. The pre-existing
`Formalizations/Lean/.lake` link points to the canonical pinned artifacts and was used read-only.
No update, build, dependency clone, fetch, or other `.lake` mutation was run.

## Validation evidence

Commands ran in this worker clone on 2026-07-12 (Asia/Shanghai).

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1425` | 0 | rank 923, planned, legacy artifacts unaccepted, theorem incomplete |
| `file Formalizations/Lean/.lake; readlink Formalizations/Lean/.lake; git status --short; git diff --stat; git rev-parse HEAD; git rev-parse HEAD^{tree}` | 0 | the `.lake` path was the automation-provided link to canonical artifacts; it was the only untracked path before this phase, the tracked diff was empty, and the base revision/tree are recorded above |
| `rg -n -C 5 '随机吸引子\|随机系统的吸引子' Docs/researches/math_theorems.md Docs/Stage0_Blueprint.md` | 0 | found only the topic/gloss record and Stage0's open fields; no truth-valued proposition or pinpoint source |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0 at the commit above |
| `(cd Formalizations/Lean && lake --version)` | 0 | Lake version above |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json Stage1_Instances/THM-M-1425/IntakeProbe.lean` | 0 | hashes agree with the fingerprint above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib revision above |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1425/IntakeProbe.lean)` | 0 | all nine generic substrate interfaces elaborated; no target theorem was stated |
| `rg -n -i 'random[ _-]?attractor\|pullback[ _-]?attractor\|random[ _-]?dynamical[ _-]?system\|random[ _-]?(compact[ _-]?)?set' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 0 | one unrelated prose match for a finite random set; no topic-specific declaration found in this bounded search |
| `rg -n --glob '*.lean' '\b(sorry|admit)\b|\bsorryAx\b|^[[:space:]]*(axiom|opaque|constant)[[:space:]]|\bunsafe\b' Stage1_Instances/THM-M-1425` | 1 | expected no-match exit; no prohibited proof hole, bodyless declaration, axiom, or unsafe declaration in target Lean source |
| `python3 Stage1_Instances/THM-M-1425/check_intake.py` | 1 | known stale intake-checker failure: it unconditionally loads the intake worker's now-absent root self-test manifest; once statement artifacts exist its intake-only inventory is also stale |
| `python3 -m json.tool Stage1_Instances/THM-M-1425/statement-blocker.json` | 0 | structured blocker is valid JSON |
| scoped Python assertions over `statement-blocker.json` | 0 | target identity, null target, blocked gate, four undefined mutations, unchanged debt vector, false completion flags, changed paths, and the no-self-test boundary agree |
| `git diff --check -- Stage1_Instances/THM-M-1425`; for each new file, `git diff --no-index --check -- /dev/null "$f"; test $? -le 1` | 0 | tracked scope and both new owned artifacts produced no whitespace diagnostics; expected diff exit 1 was accepted for added files |

The historical `check_intake.py` already exits 1 at this base because it unconditionally loads the
intake worker's now-absent root self-test manifest. After these blocker artifacts are added, its
closed intake-only artifact inventory is stale as well. This statement run does not rewrite the
intake receipt, intake artifact list, historical hashes, or authoritative DAG to manufacture
agreement.

## Retry condition and status boundary

The integration lane must first accept the provisional intake dependency. An accountable source
reviewer must then preserve and hash an immutable primary source, identify and transcribe one exact
proposition and every incorporated definition with a pinpoint locator, audit
errata, and independently approve the source-statement mapping. The review must freeze the base
flow and time action, state space and random cocycle, random-set measurability, attraction and
invariance notions, initial-family class, distance and convergence mode, ordered binders,
hypotheses, exact conclusion, exceptional-set policy, and all boundary and degenerate cases. A
later statement worker can then encode that same claim, minimize its pinned imports, serialize and
hash the elaborated expression and environment, check alternate transports, and run all four
required mutation classes.

This is the first failed gate, not completion of the statement node or a downstream node. The node
remains `[ ]`; the root remains `[H5, M4, R4]`, with `audit_complete: false` and
`theorem_complete: false`. No debt-vector change is proposed. The assigned phase is not genuinely
self-tested to its completion gate, so no `.stage1-worker-selftest.json` is emitted and no
master-acceptance receipt is claimed.
