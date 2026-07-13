# THM-M-0491 exact-statement gate: blocked

- Item: `S56-M-0491-STATEMENT`
- Base revision: `3ef3a6bf4f2f9b86930beb27693f7429fea3e63a` (tree
  `c9eba4c65f6e228f9cefc8bdf62136b7fb69426a`)
- Attempt date: 2026-07-13 (Asia/Shanghai)
- Verdict: blocked; no statement receipt, worker `[_]`, or theorem-completion claim

## First failed gate

The exact-source-result identity and encoding freeze required by sections 5 and 5.1 of
`Docs/Stage1_Blueprint_rev-5.6.md` cannot be completed from the accepted inputs. The repository
record supplies only the name Maynard's theorem, James Maynard, the year 2013, and the qualitative
gloss "improvement of the upper bound on prime gaps." It contains no formula, numeral, theorem
locator, incorporated definitions, ordered binders, hypotheses, conclusion, proof boundary,
correction history, or independent source review. Its `已验证` label is explicitly untrusted under
rev-5.6.

The intake identifies James Maynard's *Small gaps between primes* as the matching primary source
family, but that paper contains materially inequivalent headline results:

- Theorem 1.1 gives a general positive-`m` bound for
  `liminf (p_(n+m) - p_n)` using an absolute implied constant;
- Theorem 1.2 gives a positive-proportion finite-tuple result;
- Theorem 1.3 gives the unconditional adjacent-gap bound
  `liminf (p_(n+1) - p_n) <= 600`;
- Theorem 1.4 gives conditional level-of-distribution bounds of 12 and 600; and
- Propositions 4.2-4.3 provide the multidimensional-sieve engine rather than the same root claim.

Theorem 1.3 is the strongest contextual candidate for the short catalog gloss, but candidate
priority is not source-statement approval. Selecting it would invent the missing result and constant;
selecting Theorem 1.1, 1.2, 1.4, or the sieve engine would make a different unapproved choice.

Even after selecting a result, the source's positive-natural and one-based prime indexing must be
mapped to Lean's zero-based `Nat.nth Nat.Prime`. The canonical statement must also fix the gap
codomain and subtraction, liminf versus infinitely-often encoding, strict versus non-strict bounds,
finite prefixes, equality at 600, the `m`-step off-by-one convention, absolute-constant positivity
and binder order, tuple edge cases, conditional premises, and all coercions and boundary cases.
These are proposition-changing choices or require checked transports.

The intake therefore deliberately leaves the canonical claim, formal module and expression,
ordered binders, hypotheses, elaborated-expression hash, and target environment fingerprint null.
There is no canonical Lean expression whose imports can be certified minimal, no alternate
encoding eligible for a checked transport, and no meaningful removed-hypothesis, changed-domain,
changed-binder-scope, or boundary-case mutation. The root remains `[H1, M4, R4]`.

The prerequisite `S56-M-0491-INTAKE` is only provisional `[_]`. Its receipt declares
`accepted: false`, is unsigned and non-content-addressed, and contains no accepted receipt ID.
Provisional evidence can inform this fail-closed attempt, but master acceptance remains required
before any future statement transition can be accepted.

## Pinned Lean boundary

The existing discovery-only `IntakeProbe.lean` was re-elaborated through these direct imports:

```lean
import Mathlib.NumberTheory.PrimeCounting
import Mathlib.NumberTheory.SelbergSieve
import Mathlib.NumberTheory.ArithmeticFunction.VonMangoldt
```

It checks fourteen nth-prime, prime-counting, filter, generic Selberg upper-bound sieve, and von
Mangoldt interfaces. The command exited 0; stdout was 1,129 bytes with SHA-256
`61b4b48e82bae21d353b19091fd02a89070efcd802ca70643d13940aac2a244e`, and stderr was empty. The
probe declares no canonical Maynard target, source-index transport, liminf or infinitude encoding,
statement mutation, multidimensional sieve, or proof body. Its imports therefore cannot be called
minimal imports for the absent target and receive no statement or proof credit.

A bounded exact-topic search of pinned mathlib and `Formalizations/Lean/AwesomeTheorems` found no
Maynard small-prime-gap declaration or matching nth-prime liminf bound. The only `Maynard` match in
pinned mathlib concerns the unrelated Duffin-Schaeffer theorem and explicitly says that result is
not formalized there. This is narrow statement-surface feasibility evidence, not the downstream
immutable anchor audit or a global absence claim.

The environment is Lean 4.29.0 at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` (tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`). The automation-provided canonical `.lake` symlink
was used read-only. No `lake update`, `lake build`, dependency clone or fetch, or other `.lake`
mutation was run. The recorded recipe denies network, but this inherited worker execution did not
independently enforce network isolation; it is nonhermetic blocker evidence, not release evidence.

## Validation evidence

Commands ran in this worker clone on 2026-07-13 (Asia/Shanghai), from the repository root unless a
different working directory is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0491` | 0 | rank 1368; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| initial `git status --short --untracked-files=all` and `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree are recorded above |
| scoped inspection of the blueprint, execution skill, guidelines, target manifest and DAG entries, source records, Stage0 projection, and complete intake dossier | 0 | the Maynard small-gap family is identified, but the exact source result, formal expression, imports, and fingerprints remain null |
| `git blame -L 3602,3607 -- Docs/researches/math_theorems.md` | 0 | all six catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `sha256sum` over current authority, source, intake, toolchain, lockfile, probe, and pinned number-theory inputs | 0 | current input digests agree with `statement-blocker.json` |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned mathlib revision and tree recorded above; package worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0491/IntakeProbe.lean` | 0 | fourteen adjacent APIs elaborated; output digest recorded above; no canonical target or proof body |
| bounded exact-topic `rg` over pinned mathlib and repo-local shared Lean | 0 | only the unrelated Duffin-Schaeffer Maynard comment matched; discovery only, not an anchor audit |
| `python3 -B Stage1_Instances/THM-M-0491/check_intake.py` | 1 | historical intake checker expects authoritative intake state `[ ]`; integration now records provisional `[_]`, so it fails closed before statement evidence is considered |
| prohibited-construct scan over owned Lean files | 1 | expected no match; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `python3 -m json.tool Stage1_Instances/THM-M-0491/statement-blocker.json` and scoped blocker assertions | 0 | structured syntax, identity, null target/imports/hashes, four undefined mutations, unchanged vector, false completion flags, exact two-file scope, and absent self-test agree |
| `git diff --check` plus per-added-file `git diff --no-index --check` | 0 aggregate | no whitespace diagnostics; each raw no-index command returned only the expected added-file difference status 1 |
| `test ! -e .stage1-worker-selftest.json` | 0 | no self-test manifest exists because the exact-statement deliverable did not pass |

The intake checker is historical phase-local evidence: it freezes the intake-time authority cursor
and exact nine-file inventory. This phase neither rewrites that checker nor changes scheduler,
blueprint, or DAG state to manufacture freshness.

## Retry condition

The integration lane must master-accept refreshed intake evidence. Accountable reviewers must
lawfully preserve and hash an immutable source edition, select and independently approve exactly
one Maynard result and its proof boundary, reconcile the preprint and journal corrections, and map
every incorporated definition, ordered binder, hypothesis, conclusion, constant, asymptotic
convention, conditional premise, indexing convention, and boundary case.

A later statement run can then encode only that approved claim, establish minimal pinned imports,
serialize and hash the elaborated expression and environment, compile every credited transport,
and run all four mutation classes. Until then this node remains `[ ]`; `audit_complete` and
`theorem_complete` are false. Because the assigned phase did not pass its completion gate, no
`.stage1-worker-selftest.json`, statement receipt, proof credit, or master acceptance is claimed.
