# THM-M-0969 exact-statement gate: blocked

- Item: `S56-M-0969-STATEMENT`
- Base revision: `48abbb2d2eeb89816c5ffc0ad8faafa4b9d24dd0`
- Base tree: `0f26e2c78fb5fff9277cbbdfef5e145fd4ef06f1`
- Attempt date: 2026-07-13 (`Asia/Shanghai`)
- Verdict: blocked; no statement receipt, worker `[_]`, or theorem-completion claim

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the authoritative repository record.
The catalog contributes only the title `Lovász局部引理`, attribution to Laszlo Lovasz in 1975,
and a one-line gloss whose English sense is "the probability that sparsely dependent events all
fail to occur." It gives no bibliography, formula, probability space, event index, dependency
definition, independence semantics, numerical condition, ordered binders, hypotheses, conclusion,
proof boundary, correction or errata history, reviewer, or formal declaration. Stage0 explicitly
leaves the precise definitions and premises open, and the catalog's verified-status label is
untrusted under rev-5.6.

The intake inspected a strong primary source-family lead: P. Erdos and L. Lovasz, *Problems and
results on 3-chromatic hypergraphs and some related questions*, Section 2, printed pp. 616-617. Its
finite graph lemma uses maximum degree `d`, independence from the family assigned to nonneighbors,
the event bound `P(A_i) <= 1/(4d)`, and a positive probability for the intersection of all event
complements. The inspected 19-page scan has SHA-256
`fc99b53c12d75066934e2f4e35c7189b35276f0a006af075010e01cffd74e2e0`.
That identifies an original candidate, but neither the catalog nor an independent reviewer selects
it as the repository root.

Selecting that candidate now would be just as unsupported as selecting a modern symmetric
`e*p*(d+1) <= 1` corollary, the asymmetric weight/product form, a lopsided formulation, or an
infinite extension. Those variants change the graph convention, independence premise, constants,
endpoints, domains, and sometimes the conclusion. The repository also does not decide between
positive `ENNReal` measure, positive real probability, an explicit product lower bound, or
nonemptiness, nor does it resolve empty event families, empty sample spaces, degree zero,
self-neighbors, isolated vertices, probability endpoints, or infinite intersections.

Sections 5 and 5.1 of the rev-5.6 blueprint make statement ambiguity and a missing expression
fingerprint hard blockers. The intake therefore correctly leaves the canonical human claim, Lean
module and expression, minimal imports, elaborated-expression hash, canonical environment
fingerprint, binders, hypotheses, and credited alternate forms null or empty at `[H1, M4, R4]`.
Without a canonical target, import minimality and alternate transports are undefined, and the
required removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case mutations are
not meaningful. They have not passed.

The prerequisite `S56-M-0969-INTAKE` is also only provisional worker state `[_]`, not
master-accepted state `[x]`. Its receipt declares `accepted: false`, is not content-addressed, and
has no accepted receipt ID. Dependency-ordered blocker preparation is allowed, but an accepted
statement transition is independently impossible until that prerequisite is accepted.

No `Statement.lean`, axiom, placeholder, assumed event-system interface, weakened special case, or
broadened substitute was introduced. Lifecycle remains `planned`, the item remains `[ ]`, and the
root remains `[H1, M4, R4]`.

## Pinned Lean Boundary

The existing discovery-only `IntakeProbe.lean` re-elaborates with the direct imports
`Mathlib.Probability.Independence.Basic` and
`Mathlib.Combinatorics.SimpleGraph.Finite`. It authenticates generic measurable-event,
independence, finite-intersection, neighborhood, degree, and maximum-degree APIs. Its complete
stdout has SHA-256 `f78d382b9b5095d38283f09d27dfeef0a94421f2c4de7cf09a4e31e94c12db64`.

The probe declares no dependency-graph event condition, local-lemma criterion, canonical target,
source transport, or proof body. Its two imports therefore cannot be certified as minimal imports
for an absent target and receive no statement or proof credit. A bounded exact-topic search found
no Lovasz-local-lemma target declaration in repository-local or pinned-mathlib Lean. That result is
discovery-only feasibility evidence, not the downstream anchor audit or a global absence claim.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned
mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` link was used read-only. No `lake update`, `lake build`, dependency
clone or fetch, or other `.lake` mutation was run.

## Validation Evidence

Commands ran in this worker clone on 2026-07-13 (`Asia/Shanghai`). Lean commands ran from
`Formalizations/Lean`; all others ran from the repository root unless noted. Exact structured
arguments and results are also preserved in `statement-blocker.json`.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and execution-skill presence passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0969` | 0 | rank 1503; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| pre-edit `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` link was untracked; base revision and tree are recorded above |
| pre-edit `python3 -B Stage1_Instances/THM-M-0969/check_intake.py` | 0 | the intake-only artifact inventory and planned `[H1,M4,R4]` dossier with six open tasks passed before this statement report was added |
| post-edit `python3 -B Stage1_Instances/THM-M-0969/check_intake.py` | 1 expected | the historical intake-only checker rejects the two new statement-phase files as outside its frozen intake artifact inventory; it was preserved rather than weakened |
| `LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0969/IntakeProbe.lean` | 0 | 13 adjacent pinned APIs elaborated; stdout was 2065 bytes with the hash above; no target or proof body |
| bounded exact-topic `rg` search over repository-local and pinned-mathlib Lean | 1 expected | no Lovasz-local-lemma target declaration; discovery only |
| prohibited-construct scan over owned Lean | 1 expected | no `sorry`, `admit`, `sorryAx`, axiom, constant, opaque, or unsafe declaration |
| JSON parse, scoped blocker invariants, no-self-test check, and whitespace checks | 0 | null target/import fingerprints, unchanged vector, four undefined mutation classes, false completion fields, exact two-file change scope, and absent self-test agree |

## Retry Condition And Status Boundary

The integration lane must first master-accept fresh intake evidence bound to current authority.
Accountable reviewers must then lawfully preserve and hash one immutable primary or approved
authoritative edition, select and independently approve one exact result and every incorporated
definition, and map its probability space, event family, graph or relation, independence semantics,
numeric criterion, ordered binders, hypotheses, conclusion, proof boundary, corrections, errata,
and every degenerate case.

A fresh statement worker may then encode only that reviewed claim, minimize its pinned imports,
serialize and hash the elaborated expression and environment, compile every credited transport,
and execute all four required mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. `audit_complete: false` and `theorem_complete: false`; no debt-vector change is
proposed. Because the exact-statement deliverable did not pass, no `.stage1-worker-selftest.json`,
statement receipt, worker `[_]`, master acceptance, statement fingerprint, or proof credit is
claimed.
