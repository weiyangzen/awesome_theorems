# Exact-statement gate: blocked

Item: `S56-M-1512-STATEMENT`

Theorem: `THM-M-1512`

Base revision: `bdb4ee4eb79433800f3b28633d046959f18b57e9` (tree
`8a7b02bd1c876c4f44ab2e5863e71534155c2629`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-1512-INTAKE` has provisional worker
state `[_]`, not master-accepted state `[x]`. Rev-5.6 section 10.2 permits this dependency-ordered
investigation, but the intake receipt declares `accepted: false`, contains no accepted receipt ID,
and explicitly leaves the canonical mathematical statement and Lean target null. Master acceptance
remains necessary before a future statement transition can be accepted.

Independently, the exact-statement gate cannot pass. The complete repository record is the title
`Nash existence theorem`, attribution to John Nash in 1950, and the gloss `Existence of Nash
equilibrium.` It supplies no bibliography, game definition, ordered binder, hypothesis, exact
conclusion, proof boundary, correction history, or boundary convention. Its `verified` label is
untrusted under rev-5.6.

The inspected primary-source lead is John F. Nash, Jr., *Equilibrium Points in N-Person Games*,
PNAS 36 (1950), pages 48-49, DOI `10.1073/pnas.36.1.48`; the observed scan has SHA-256
`5bf21fdad1ab15779fb1d816298ba338b6d30d854938c15e4f41df1b6659ed85`. It identifies a strong
candidate family: finitely many players, finite pure-strategy sets, a payment vector for each pure
profile, probability distributions as mixed strategies, expected payoffs, and a self-countering
mixed profile as equilibrium. The paper then invokes Kakutani and concludes that an equilibrium
point exists. It does not contain a numbered theorem, and the repository does not cite or adopt
this passage as its exact proposition. No accountable reviewer has approved the incorporated
definitions, assumption and conclusion crosswalk, correction or errata history, or source-to-target
selection.

The proposition-changing formal choices therefore remain open:

- an arbitrary finite player type or `Fin n`, and whether zero players are admitted;
- finite nonempty action types or finite nonempty sets, including empty and singleton cases;
- the source-real payoff table and exact pure-profile encoding;
- `stdSimplex`, `PMF`, or another mixed-strategy representation and any checked transport;
- the exact finite expected-payoff sum, unilateral update, binder order, and coercions;
- pure versus mixed deviations and the lemma connecting them;
- all-player best response, self-countering, or correspondence membership as equilibrium; and
- ties, constant payoffs, dominated actions, nonunique equilibria, and other boundary cases.

Choosing the familiar finite-game formulation, importing the external project's object model, or
assuming a best response, fixed point, or equilibrium in a structure would silently resolve these
open decisions. It would be an invented or substituted target, not elaboration of the exact
received statement.

Sections 5 and 5.1 make statement ambiguity and a missing expression fingerprint hard blockers.
There is consequently no canonical expression for which minimal imports, a serialized elaborated
type, an environment fingerprint, checked alternate transports, or the required removed-hypothesis,
changed-domain, changed-binder-scope, and boundary-case mutations can be certified. All four
mutation classes are undefined, not passed. No `Statement.lean`, theorem declaration, proof body,
weakened special case, or broadened interface was added. The root remains `[H1, M4, R4]`.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` re-elaborates with three direct imports and checks eight adjacent
simplex, compactness, convexity, PMF, hemicontinuity, and fixed-point interfaces. It defines no
game or equilibrium and states no target theorem. Its imports are discovery candidates only; they
cannot be called minimal for a canonical target that does not exist.

A bounded source search over repository-local Lean and pinned mathlib found no Nash-equilibrium,
mixed-strategy, best-response, or game-theory declaration. The only Kakutani-name matches were the
unrelated Riesz-Markov-Kakutani representation theorem. This is narrow feasibility evidence, not
the downstream anchor audit or a global absence claim.

The intake also records `math-xmum/Brouwer` commit
`c02205edf347ad45f0d62db85497598ba2c4291e`. Its `Gametheory/Nash.lean` defines a finite-game
model and proves `ExistsNashEq`, but it targets Lean 4.31 and another mathlib revision. It is absent
from this repository's pinned dependency closure and has not been built, trust-audited, or mapped
to an accepted source proposition here. Static source inspection does not turn it into the
canonical statement or machine evidence.

The worker environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib
revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` symlink was used read-only. No dependency update, build, clone, fetch,
or other `.lake` mutation was run.

## Validation Record

Commands ran in this isolated worker clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1512` | 0 | rank 1026; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| pre-edit `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| scoped catalog, Stage0, manifest, blueprint, skill, guidelines, and intake inspection | 0 | confirmed the one-line catalog gloss, inspected primary lead, explicit null canonical target, and open source and encoding decisions |
| `sha256sum` over authority, source, intake, toolchain, probe, and pinned mathlib inputs | 0 | exact hashes are recorded in `statement-blocker.json` |
| `python3 -B Stage1_Instances/THM-M-1512/check_intake.py` | 1 | the historical intake checker expects authoritative intake state `[ ]`; integration now records provisional `[_]`, so this statement run records rather than rewrites stale intake evidence |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned mathlib revision and tree recorded above; package worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1512/IntakeProbe.lean` | 0 | all eight adjacent API signatures elaborated; no canonical target or proof body |
| bounded Nash/game/best-response/Kakutani search in repository-local Lean and pinned mathlib | 0 | only unrelated Riesz-Markov-Kakutani text matched; no target-relevant declaration was located |
| prohibited-construct scan over owned Lean files | 1 | expected no-match result; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |

Final JSON, invariant, whitespace, and absent-self-test checks are recorded in the structured
blocker beside this report.

## Retry Condition And Status Boundary

The integration lane must master-accept refreshed intake evidence. Accountable reviewers must
lawfully preserve and hash an immutable source edition, adopt one exact proposition with its
incorporated definitions and proof boundary, audit corrections and errata, transcribe every ordered
binder, hypothesis, conclusion, and boundary convention, justify why it represents `THM-M-1512`
rather than `THM-M-1511` or the 1951 continuous-game generalization, and independently approve the
mapping.

A fresh statement worker can then encode precisely that reviewed claim, minimize its pinned
imports, serialize and hash the elaborated expression and environment, compile every credited
transport, and execute all four required mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. Because the exact-statement
deliverable did not pass, no `.stage1-worker-selftest.json`, statement receipt, worker `[_]`, or
master acceptance is claimed.
