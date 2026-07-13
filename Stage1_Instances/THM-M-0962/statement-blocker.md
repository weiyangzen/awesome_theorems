# THM-M-0962 exact-statement gate: blocked

Item: `S56-M-0962-STATEMENT`

Base revision: `1168265f6eea33d947ff470fad2ca6fff9e1130b` (tree
`0d35608cbc6e281a3d9935d452cf33c88c32aa7e`). Validation date: 2026-07-13
(`Asia/Shanghai`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-0962-INTAKE` has only provisional
worker state `[_]`; receipt `S56-M-0962-INTAKE-WORKER-20260713` is unsigned,
non-content-addressed, `accepted=false`, and has no accepted receipt ID. Rev-5.6 permits
provisional preparation, but dependency-ordered master acceptance remains open.

More importantly, the exact mathematical root is not frozen. The repository record supplies only
the eponym, authors, year, and the gloss "upper bound for an intersecting family." It gives no
formula, citation, definitions, parameters, hypotheses, conclusion, or boundary convention.

The matched 1981 publisher abstract states one precise modular result: a family of `k`-subsets of
an `n`-set, distinct residues `mu_0, ..., mu_s` modulo a prime `p`, member size congruent to
`mu_0`, and distinct-pair intersections congruent to one of `mu_1, ..., mu_s`, has cardinality at
most `choose n s`. That abstract is a strong source lead, but it is not enough to select the exact
catalog root here:

- the article body, incorporated definitions, theorem locator, qualifications, proof boundary,
  corrections, errata, and independent source review were unavailable;
- the source does not say that every listed residue must occur, and the catalog does not decide
  whether its root follows the abstract or another result from the paper;
- modern literature also calls the paper's nonuniform exact `L`-intersection result the
  Frankl-Wilson theorem, with a sum-of-binomial-coefficients bound; that is materially different
  from the modular uniform abstract result;
- prime-power generalizations, forbidden-residue specializations, and the geometric application
  are further non-equivalent possibilities.

Choosing the attractive modular `Finset (Finset (Fin n))` formulation would therefore elaborate a
candidate, not the exact accepted target. Rev-5.6 makes this statement ambiguity a hard blocker.
There is no honest canonical expression whose imports can be certified minimal, no credited
alternate form for a checked transport, and no canonical fingerprint against which the four
required mutations can run. The removed-hypothesis, changed-domain, changed-binder-scope, and
boundary-case results are undefined, not passed. The vector remains `[H1, M3, R4]`.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` was re-elaborated using the pinned toolchain. It checks
`Set.IsIntersectingOf`, `Set.Intersecting`, `Set.Sized`, `Finset.powersetCard`,
`Finset.card_powersetCard`, `Nat.ModEq`, and `Nat.choose`. Lean exited `0`; stdout was 547 bytes
with SHA-256 `3efe1de6c2996af6a72dabde1c6f94df0a07395f106dcb4ba88df72f755e14de`, and stderr was
empty. This is interface evidence only. It declares no target, transport, or proof body, and its
imports cannot be certified minimal for an absent canonical target.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib
revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided `.lake` symlink was used
read-only. No update, build, clone, fetch, or dependency mutation was run.

A separate temporary candidate probe confirmed that the modular abstract can be encoded in Lean,
but it is deliberately not an owned statement artifact and receives no statement credit. The
candidate used `Fin n`, a duplicate-free `Finset` family, a `Fin (s + 1)` residue vector, and an
allowed-residue witness for each distinct pair. Those are coherent encoding decisions, not facts
selected by the catalog. Kernel elaboration cannot resolve which human proposition the catalog
owns.

The modular candidate is not dismissed as a corollary of the nonuniform exact-`L` theorem. A
residue class may contain many possible intersection cardinalities, and the bounds `choose n s`
and `sum_{i=0}^s choose n i` differ. It is a substantive result from the 1981 paper. The blocker is
the multi-valued eponymic scope, not mathematical weakness of either candidate.

## Validation Record

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0962` | 0 | rank 1496; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | pre-edit status contained only the automation-provided `.lake` symlink; base revision and tree are recorded above |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'`; `git -C ... status --short --untracked-files=all` | 0 | pinned mathlib revision/tree recorded above; package worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0962/IntakeProbe.lean` | 0 | seven adjacent statement interfaces elaborated; no canonical target or proof body |
| `python3 -B Stage1_Instances/THM-M-0962/check_intake.py` | 1 | historical intake replay fails because it froze the authoritative intake state as `[ ]`; integration advanced that cursor to provisional `[_]` |
| `rg -ni --glob '*.lean' 'frankl.?wilson\|intersection theorems with geometric consequences' ...` | 1 | no eponym or paper-title match in pinned mathlib, repo-local Lean, or the intake probe; bounded discovery only |
| `curl -L --fail --silent --show-error https://link.springer.com/article/10.1007/BF02579457 ...` | 0 | publisher abstract inspected; article body remained subscription-only; normalized first paragraph SHA-256 `7a58f8c114205cd3a2b8326c4f88ea34d6c33bb8f48caeef0fac97efef71a4b0` |
| `curl -L --fail --silent --show-error https://arxiv.org/pdf/1707.01715 ...`; `pdftotext`; scoped inspection | 0 | modern exposition's Theorem 1.3 attributes a different nonuniform exact-`L` sum-of-binomials result to the same 1981 paper; identity ambiguity confirmed |

The final JSON, prohibited-construct scan, scoped ownership check, and whitespace checks are
recorded in `statement-blocker.json`. The stale historical intake validator was preserved rather
than rewritten as statement evidence.

## Retry Condition And Status Boundary

First obtain dependency-ordered master acceptance of refreshed intake evidence. Accountable
reviewers must then lawfully preserve and hash an immutable primary or authoritative source,
select one exact root, and independently approve its theorem locator, incorporated definitions,
ordered binders, hypotheses, conclusion, proof boundary, correction and errata status, and all
boundary choices. They must explicitly decide modular uniform versus exact `L`-intersection scope,
prime versus prime power, residue order/distinctness/occurrence, ground-set and family encodings,
distinct-pair semantics, binomial orientation, equality or application content, and empty,
singleton, `s = 0`, `k = 0`, `n < k`, and `s > n` cases.

A fresh statement worker can then encode only that approved claim, minimize pinned imports,
serialize its elaborated expression and environment, compile credited transports, and execute all
four mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete=false` and
`theorem_complete=false`; no debt-vector change is proposed. Because the assigned deliverable did
not pass, no `.stage1-worker-selftest.json`, statement receipt, worker `[_]`, statement fingerprint,
proof credit, or master acceptance is claimed.
