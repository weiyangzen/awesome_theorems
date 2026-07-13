# Exact-statement gate: blocked

Item: `S56-M-0964-STATEMENT`

Theorem: `THM-M-0964`

Base revision: `b243ebc0f9058ba5afafef8240b92c2dfb2edc6e` (tree
`b4b092069141ac54ea1ab5a6ea946192a30ec78c`). Validation date: 2026-07-13
(`Asia/Shanghai`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-0964-INTAKE` has provisional worker
state `[_]`, not master-accepted state `[x]`. Its mutable receipt declares `accepted: false`, is
not content-addressed, and lists no accepted receipt ID. Rev-5.6 permits dependency-ordered
investigation, but no accepted statement transition can rely on that predecessor.

Independently, the exact-statement gate cannot pass. The repository record supplies only the
Hilton-Milner name, the Hilton/Milner attribution, the year 1967, and the gloss "maximum size of a
nontrivial intersecting family." It gives no formula, parameter range, definition of nontriviality,
family representation, equality scope, theorem locator, proof boundary, correction history, or
boundary convention. Stage0 explicitly leaves the precise definitions and premises open.

The authenticated primary lead is A. J. W. Hilton and E. C. Milner, *Some Intersection Theorems
for Systems of Finite Sets*, *The Quarterly Journal of Mathematics* 18(1) (1967), 369-384, DOI
`10.1093/qmath/18.1.369`. Crossref and zbMATH confirm the bibliography, but the OUP article and PDF
endpoints returned HTTP 403 Cloudflare challenges. Semantic Scholar, Unpaywall, and OpenAIRE mark
the work closed, and no accessible immutable primary text was located. Consequently this worker
did not inspect or independently approve a primary theorem number or passage, incorporated
definitions, exact range, proof clause, correction, or erratum. Crossref's empty relation metadata
is not affirmative no-errata evidence.

Two immutable secondary restatements identify a strong candidate but disagree on proposition scope.
Hurlbert-Kamat, arXiv `1609.04714v3`, Theorem 11, uses `2 <= r < n/2`, gives the familiar binomial
bound, and classifies equality by the standard Hilton-Milner family plus an exceptional family for
`r = 3`. Bulavka-Woodroofe, arXiv `2411.02513v4`, Theorem 1, displays the bound under `k <= n/2`
and handles uniqueness separately in a stricter range. The catalog does not choose among a bound,
a sharp maximum with attainment, a full extremizer classification, or the original paper's exact
theorem package. Promoting the convenient strict-range, bound-only intake candidate would silently
make that proposition-changing choice.

Other choices remain open: `Fin n` versus an abstract finite ground type; set, finset, or indexed
family semantics; all-pair versus distinct-pair intersection; empty total intersection versus not
being contained in a star; the exact parenthesization of natural subtraction; permutation
isomorphism; and the cases `k = 0, 1, 2, 3`, `n < 2*k`, `n = 2*k`, empty or singleton families,
and a family containing the empty set.

Sections 5 and 5.1 of the rev-5.6 blueprint make statement ambiguity and a missing expression
fingerprint hard blockers. There is therefore no canonical expression whose imports can honestly
be certified minimal, no checked alternate encoding, and no meaningful removed-hypothesis,
changed-domain, changed-binder-scope, or boundary mutation suite. All four mutation classes are
undefined, not passed. No `Statement.lean`, theorem declaration, proof body, substituted theorem,
or circular premise was added. The root remains `H1 / M3 / R4`.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` re-elaborates under the pinned toolchain. It checks adjacent
set-family APIs and elaborates `Stage1.THM_M_0964.Intake.CandidateTargetShape`, an explicitly
unproved and noncanonical proposition definition. Lean exited 0; stdout was 718 bytes and nine
lines with SHA-256 `a88e8dd02ac3509a17a40e29af69c941bf86a6b4c6cd996715b80144c3f770ed`,
and stderr was empty. This is interface evidence only. The candidate uses the strict half-range and
bound-only scope selected from a secondary source, so its imports cannot be certified minimal for
the absent source-approved root.

The probe imports `Mathlib.Combinatorics.SetFamily.KruskalKatona` and
`Mathlib.Data.Finset.Slice`; the first also supplies the neighboring Erdős-Ko-Rado declaration.
A candidate-only import experiment indicates that `Mathlib.Combinatorics.SetFamily.Intersecting`
plus `Mathlib.Data.Finset.Slice` suffices for that candidate shape, but this cannot establish the
minimal imports of an unselected canonical statement.

A bounded exact-topic search over pinned mathlib, repository-local Lean, and this target found only
the intake prose and unrelated uses of the phrase "nontrivial intersection". No Hilton-Milner
terminal declaration was located. That is feasibility evidence only, not the downstream exhaustive
anchor audit or a global absence claim.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib
revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided canonical `.lake`
symlink was used read-only. No update, build, clone, fetch, or dependency mutation was run.

## Validation Record

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0964` | 0 | rank 1498; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| pre-edit `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| scoped authority, intake, source-availability, and pinned-source inspection | 0 | confirmed the provisional dependency, null canonical target, inaccessible closed primary body, conflicting secondary scopes, and current hashes recorded in the structured blocker |
| `python3 -B Stage1_Instances/THM-M-0964/check_intake.py` | 1 | historical intake checker expects authoritative intake state `[ ]`; integration now records provisional `[_]`; the stale intake evidence was preserved rather than rewritten |
| `cd Formalizations/Lean && lake env lean --version`; `lake --version` | 0 | pinned Lean and Lake versions recorded above |
| pinned mathlib `git rev-parse HEAD 'HEAD^{tree}'`; package status | 0 | pinned revision and tree recorded above; package worktree clean |
| `cd Formalizations/Lean && env LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0964/IntakeProbe.lean` | 0 | seven adjacent APIs and the unproved candidate proposition shape elaborated; output hashes recorded above |
| bounded Hilton-Milner/exact-topic Lean search | 0 wrapper | no source-identical terminal declaration located; bounded discovery only |
| prohibited-construct scan over owned Lean files | 1 inner no-match | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |

Final JSON, scoped invariants, whitespace, and absent-self-test checks are recorded in the structured
blocker beside this report.

## Retry Condition And Status Boundary

The integration lane must first master-accept a current intake. Accountable source and scope
reviewers must then lawfully preserve and hash an immutable complete primary edition, select and
independently approve the exact result and incorporated definitions, inspect corrections and
errata, and resolve the bound/attainment/classification strength, endpoint, family, intersection,
nontriviality, isomorphism, arithmetic, and degenerate-case conventions.

A fresh statement worker can then encode only that approved claim, minimize its pinned imports,
serialize and hash the elaborated expression and environment, compile every credited transport,
and execute all four mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. Because the exact-statement
deliverable did not pass, no `.stage1-worker-selftest.json`, node receipt, worker `[_]`, statement
fingerprint, proof credit, or master acceptance is claimed.
