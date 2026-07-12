# Exact-statement gate: blocked

Item: `S56-M-1415-STATEMENT`

Theorem: `THM-M-1415`

Base revision: `3d1d6d3eb018f17657cae1cfd7d25fc30492a12b` (tree
`3aa3dd324b35549da6cf2c5a54183a63ed1bfff9`).

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the authoritative repository record.
That record gives only the title `Markov分割` ("Markov partition"), attributes it to Yakov Sinai
and Rufus Bowen, gives the year 1970, and glosses it as `双曲系统的符号化` ("symbolization of
hyperbolic systems"). These words name a theorem family and purpose, not a truth-valued proposition
with ordered binders, hypotheses, and a conclusion. Stage0 explicitly leaves the exact definitions,
premises, proof route, equivalent forms, axioms, and formal artifacts open. The metadata label
`已验证` is untrusted under rev-5.6.

The provisional intake consequently leaves both the canonical mathematical statement and Lean
expression null. It identifies three serious primary-source candidates, but inspected publisher
metadata only:

- Bowen, *Markov Partitions for Axiom A Diffeomorphisms*, 1970, DOI
  `10.2307/2373370`;
- Sinai, *Markov partitions and C-diffeomorphisms*, 1968, DOI
  `10.1007/BF01075361`; and
- Sinai, *Construction of Markov partitions*, 1968, DOI `10.1007/BF01076126`.

No immutable article text, exact definition or theorem passage, assumptions, proof boundary,
translation relationship, corrections, errata, or independent source approval is available in the
intake evidence. The catalog's 1970 date also does not resolve how the two Sinai 1968 publications
relate to the intended target.

Many inequivalent claims fit the gloss: existence of a finite Markov partition; existence at an
arbitrarily small scale; construction of a one- or two-sided subshift of finite type; or a
continuous surjective, finite-to-one, injective-off-boundaries, or conjugating coding map. These
readings also require different choices of Axiom A, Anosov, `C`-diffeomorphism, or another
hyperbolic system; full manifold, nonwandering set, basic set, or locally maximal invariant set;
rectangle and stable/unstable plaque definitions; Markov inclusions; transition relation; and
boundary and multiple-itinerary policy.

Selecting any one would invent, narrow, or substitute mathematics rather than elaborate the exact
received target. An abstract structure that assumes a Markov partition or coding and merely
projects it would be a placeholder rather than the classical existence or symbolization theorem.
No such declaration was added.

Section 5 of the rev-5.6 blueprint makes statement ambiguity and a missing elaborated-expression
fingerprint hard blockers. Section 5.1 additionally requires minimal target imports, fixed
elaboration context, a serialized expression and environment fingerprint, checked transports, and
removed-hypothesis, changed-domain, changed-binder-scope, and boundary mutations. Without a
canonical proposition those tests are undefined, not passed. The first failed gate is exact
source-statement identity, so the statement node remains unfinished at `M4`.

## Pinned Lean boundary

The existing `IntakeProbe.lean` imports `Mathlib.Data.Setoid.Partition`,
`Mathlib.Data.Stream.Init`, and `Mathlib.Dynamics.PeriodicPts.Defs`. Under the pinned environment it
re-elaborates generic set-partition, stream-tail, semiconjugacy, iterated-semiconjugacy, and
periodic-point transport interfaces. These are possible representation ingredients only. The probe
states no Markov-partition theorem, its imports cannot be claimed minimal for an unknown canonical
target, and its successful elaboration receives no statement, anchor, or proof credit.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. The `lean-toolchain`, `lake-manifest.json`, and probe
SHA-256 values are respectively `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`,
`321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`, and
`98c2abc1d3bbb7cad34446e5313961b4d7e449db6a8b40e1ecd2bfcbf463e012`.

The automation-provided `Formalizations/Lean/.lake` link existed before this phase, points to the
canonical checkout's pinned artifacts, and was used read-only. No `lake update`, `lake build`,
dependency clone or fetch, or other `.lake` mutation was run.

## Validation evidence

Commands ran from this worker clone on 2026-07-12 (Asia/Shanghai).

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1415` | 0 | rank 914, planned, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all && git rev-parse HEAD && git rev-parse HEAD^{tree}` | 0 | before statement edits, only the pre-existing `.lake` link was untracked; base revision and tree are recorded above |
| `rg` for the target ID and Chinese/English glosses in the manifest, catalog, Stage0, and intake | 0 | only the underspecified catalog record, open Stage0 fields, and fail-closed intake were found; no exact proposition |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | Lean 4.29.0 and Lake 5.0.0 at the revisions above |
| `cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json ../../Stage1_Instances/THM-M-1415/IntakeProbe.lean && git -C .lake/packages/mathlib rev-parse HEAD` | 0 | hashes and pinned mathlib revision match `statement-blocker.json` |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1415/IntakeProbe.lean` | 0 | all seven generic candidate interfaces elaborated; no target theorem was stated |
| bounded pinned-source `rg` for Markov partitions, subshifts, symbolic dynamics, Axiom A, Anosov, hyperbolic sets, and local product structures | 0 | no relevant named target surface; only unrelated lexical false positives were returned, so this is not an anchor audit |
| prohibited-construct `rg` over owned Lean files | 1 | expected no-match exit; no `sorry`, `admit`, `sorryAx`, `axiom`, `opaque`, or `unsafe` declaration was found |
| `python3 Stage1_Instances/THM-M-1415/check_intake.py --without-handoff` | 1 | known phase-evolution failure: the intake-only checker requires exactly its original nine artifacts and rejects the two statement blocker files |
| `python3 -m json.tool Stage1_Instances/THM-M-1415/statement-blocker.json` | 0 | structured blocker parsed as JSON |
| scoped Python blocker assertions | 0 | target identity, null target, false completion flags, changed paths, no-self-test boundary, and file-format invariants passed |
| tracked and added-file whitespace checks | 0 | both blocker artifacts passed `git diff --check` / `git diff --no-index --check` |
| `test ! -e .stage1-worker-selftest.json` | 0 | required no-self-test boundary is preserved because the statement deliverable is blocked |

The historical `check_intake.py` intentionally treats its nine intake files as a closed intake-only
artifact set. It will therefore reject the two new statement blocker files. This statement run does
not rewrite the provisional intake receipt, artifact list, or source hashes merely to manufacture
agreement.

## Retry condition and status boundary

The integration lane must first accept the intake dependency. An accountable source reviewer must
then preserve and hash an immutable primary edition, select and transcribe one exact theorem and
every incorporated definition with pinpoint locators, audit the source proof boundary, translation,
corrections, and errata, reconcile the Bowen and Sinai candidates, and independently approve the
source-to-target mapping. That decision must freeze the system and invariant-set scope, partition
and coding definitions, symbolic space, direction and strength of the coding, universes, ordered
binders, every hypothesis and conclusion, and every scale, empty, singleton, boundary, and
multiple-itinerary case.

A later statement worker can then encode that same claim with real Lean definitions, minimize its
pinned imports, serialize and hash the elaborated expression and environment, compile every
credited transport, and run all four required mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. The root remains `[H1, M4, R3]`, with `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. Because the phase is not genuinely
self-tested to its completion gate, no `.stage1-worker-selftest.json` is emitted and no receipt or
master acceptance is claimed.
