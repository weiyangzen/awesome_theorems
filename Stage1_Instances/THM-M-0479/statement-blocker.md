# THM-M-0479 rev-5.6 statement blocker

## Verdict

`S56-M-0479-STATEMENT` is blocked at the exact immutable source-statement identity and
scope-freeze gate. The repository record names Dirichlet's theorem, attributes it to Peter
Dirichlet in 1837, and supplies only the gloss `等差数列中存在无穷多素数` (there are infinitely
many primes in arithmetic progressions). It contains no bibliography, theorem locator, formula,
incorporated definitions, ordered binders, assumptions, proof boundary, translation, corrections,
errata disposition, or independent source review. Its `已验证` label is untrusted metadata under
rev-5.6.

The gloss identifies the usual theorem family, but not one exact proposition. In particular, it
does not settle:

- one fixed arithmetic progression versus every admissible progression;
- natural or integer modulus and residue domains;
- positivity or nonzeroness of the modulus, and whether modulus one is included;
- coprimality of a representative versus invertibility of a residue class;
- equality in `ZMod`, natural `ModEq`, or integer modular equality;
- natural primes versus signed integer representatives; or
- set infinitude versus the existence of a prime above every bound.

These choices change the proposition or require checked transports. Selecting a modern reduced
residue-class formulation merely because pinned mathlib proves it would add the missing universal
quantifiers and admissibility condition without an accepted source mapping. Selecting a weaker
fixed progression, omitting coprimality, or using another carrier would instead narrow, weaken, or
substitute the target.

The intake therefore deliberately leaves the canonical human statement, Lean module and
expression, ordered binders, hypotheses, elaborated-expression hash, and target environment
fingerprint null. Without an approved exact expression, no import can be certified minimal, no
alternate encoding can receive a target-specific checked transport, and the required
removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case mutations are undefined
rather than passed. Sections 5 and 5.1 of the rev-5.6 blueprint make statement ambiguity and a
missing expression fingerprint hard blockers before proof evidence is inspected.

The prerequisite `S56-M-0479-INTAKE` is provisional worker state `[_]`, not master-accepted state
`[x]`. Its receipt is unsigned and non-content-addressed, declares `accepted: false`, and supplies
no accepted receipt ID. It supports dependency-ordered inspection, but master acceptance remains a
separate prerequisite for any future accepted statement transition.

## Pinned Lean Boundary

The discovery-only `IntakeProbe.lean` was re-elaborated under Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740` and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` (tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`). With its single import
`Mathlib.NumberTheory.LSeries.PrimesInAP`, it authenticates the direct candidate

```text
Nat.infinite_setOf_prime_and_eq_mod {q : Nat} [NeZero q] {a : ZMod q}
  (ha : IsUnit a) :
  Set.Infinite {p : Nat | p.Prime and (p : ZMod q) = a}
```

and its unbounded, integer-representative, natural-`ModEq`, and set-infinitude variants. The two
set-infinitude declarations report exactly `propext`, `Classical.choice`, and `Quot.sound`. The
probe output has SHA-256
`f8ebef27763585acc203471f66dd47a3043450dcfbfe01a4baa171bc9d3e7537`.

This is real pinned API evidence only. The probe declares no canonical target, source transport,
statement mutation, or new proof body. Its import is sufficient for the discovery probe but cannot
be certified as the minimal import for an absent canonical target. The candidate module's own
documentation makes the conventional modern formulation explicit; that confirms candidate
relevance, not identity with the sparse repository gloss.

The automation-provided untracked `Formalizations/Lean/.lake` link to canonical pinned artifacts
was used read-only. No `lake update`, `lake build`, dependency clone or fetch, network-triggering
Lake operation, or other `.lake` mutation was run.

## Validation Evidence

Commands ran in the isolated worker clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0479` | 0 | rank 1360; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` before editing | 0 | only the automation `.lake` link was untracked; base revision `902d9ce008e88a35a2307c85355560a230cc33c2`, tree `dfc20d8141f18f6b09a03e818acfff408e836714` |
| repository authority, source record, Stage0 projection, intake dossier, source crosswalk, task DAG, and receipt inspection | 0 | confirmed the provisional intake, sparse gloss, null canonical target fields, unresolved source and encoding choices, and six open downstream phases |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | Lean `4.29.0`, commit `98dc76e3...bf04`; Lake `5.0.0-src+98dc76e` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned mathlib revision and tree shown above; package worktree clean |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0479/IntakeProbe.lean)` | 0 | eleven direct predicates and theorem-family interfaces elaborated; both set-infinitude candidates reported the three named axioms; exact stdout SHA-256 `f8ebef27...e7537` |
| `python3 -B Stage1_Instances/THM-M-0479/check_intake.py` | 1 | historical intake replay now expects the scheduler-only intake worker packet that integration removed after advancing the intake cursor; the historical evidence was not rewritten or represented as statement validation |
| prohibited declaration scan over owned Lean files | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, bodyless `constant`, `opaque`, or `unsafe` declaration; diagnostic `#print axioms` commands are permitted |

Final JSON parsing, scoped blocker invariants, whitespace checks, and the deliberate absence of the
root self-test manifest are recorded in `statement-blocker.json` after finalization.

## Retry Condition And Status Boundary

The integration lane must master-accept refreshed intake evidence before accepting a future
statement transition. Accountable reviewers must lawfully preserve and hash one immutable primary
or authoritative source, select and independently approve its exact proposition and proof boundary,
and map every incorporated definition, ordered binder, hypothesis, conclusion, translation,
correction, erratum, attribution, and boundary case. They must explicitly settle universal scope,
modulus and residue domains, positivity or nonzeroness, coprimality, prime carrier, congruence,
infinitude, binder order, alternate encodings, and the modulus-one and nonunit cases.

A fresh statement attempt can then encode exactly that approved claim, minimize its pinned imports,
serialize and hash the elaborated expression and environment, compile every credited transport,
and execute all four required mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement item or any
downstream item. The root remains `[H1, M3, R4]`; `audit_complete` and `theorem_complete` remain
false; no statement receipt, worker `[_]`, accepted receipt, or master acceptance is claimed.
Because the exact-statement deliverable did not pass, `.stage1-worker-selftest.json` is
deliberately absent.
