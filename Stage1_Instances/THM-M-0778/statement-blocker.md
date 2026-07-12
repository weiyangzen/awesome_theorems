# Exact-statement gate: blocked

Item: `S56-M-0778-STATEMENT`  
Theorem: `THM-M-0778`  
Worker base revision: `444819795285695894ff7b29af5c2419e0e000fa`

## Gate decision

The exact Lean 4 target cannot be elaborated truthfully from the repository source record. The
record supplies only the title "Godel's second incompleteness theorem" and the gloss "a consistent
formal system cannot prove its own consistency." Stage0 explicitly leaves the definitions,
premises, foundation, proof route, dependencies, axioms, and machine artifact open. The manifest's
`source_status_untrusted` value `已验证` is inventory metadata, not an exact proposition or evidence.

The gloss is false for arbitrary consistent formal systems and does not fix the restrictions that
make a second-incompleteness theorem valid. In particular, it does not select:

1. the object language, deductive calculus, effective presentation, and exact theory `T`;
2. the arithmetic-strength or interpretability threshold imposed on `T`;
3. the coding of formulas and proofs or the represented proof predicate;
4. the internal provability predicate and the derivability/representability conditions it obeys;
5. the exact internal consistency sentence, such as `not Provable_T(false)`, and its relationship
   to external syntactic consistency; or
6. the external metatheory, induction and classical principles, and whether the conclusion is
   conditional on consistency, soundness, or a stronger assumption in the chosen formulation.

These choices change the ordered binders, hypotheses, definitions, and conclusion. Encoding
unconstrained predicates and assuming all theorem-specific derivability facts would merely wrap
the intended conclusion in opaque premises. Choosing a convenient modern formulation without an
immutable pinpoint source and approved source-to-statement crosswalk would invent missing
mathematics or substitute a related theorem. The intake's 1931 paper citation is explicitly only a
candidate locator: no edition, theorem/section/page, exact passage, incorporated definitions,
translation, errata record, or independent source review is frozen.

Consequently there is no canonical Lean expression to serialize or hash, no defensible minimal
import for that expression, no source-faithful alternate encoding for a checked transport, and no
meaningful removed-hypothesis, changed-domain, binder-scope, or boundary-case mutation suite. The
rev-5.6 statement gate fails before anchor or proof evidence may receive credit. In addition, the
declared intake dependency is only worker-self-tested (`[_]`) in the generated projection and has
not received master acceptance.

## Pinned Lean boundary

The existing `IntakeProbe.lean` was re-elaborated only to distinguish an available pinned Lean
environment from the missing mathematical specification. It confirms generic first-order theory
and formula types plus `Nat.beta`, `Nat.unbeta`, and `Nat.beta_unbeta_coe`. Pinned mathlib describes
the beta-function module as a step toward eventually including the *first* incompleteness theorem;
it supplies no arithmetized provability predicate or second-incompleteness declaration. These APIs
are ingredients only and receive no target or proof credit.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. The `lean-toolchain` and `lake-manifest.json` SHA-256
digests are respectively `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2` and
`321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`. Existing canonical `.lake`
artifacts were consumed read-only; no update, build, clone, fetch, or dependency mutation was run.

## Exact validation record

Commands ran in this worker clone on `2026-07-12` (`Asia/Shanghai`).

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets accepted |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0778` | 0 | rank 783, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| scoped `rg` over the repository source, Stage0 record, manifest, and owned intake for the theorem ID and Chinese/English claim | 0 | only the underspecified gloss, open Stage0 fields, manifest metadata, and intake analysis were found; no exact proposition |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib revision recorded above |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | dependency-file digests recorded above |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0778/IntakeProbe.lean)` | 0 | all five generic syntax/coding API checks elaborated; no canonical target asserted |
| scoped `rg` over pinned mathlib for second incompleteness, incompleteness theorem, derivability conditions, arithmetized provability, provability predicate, consistency sentence, and Lob's theorem | 0 | only beta-function documentation about eventual first-incompleteness support matched; no target declaration |
| `rg -n '\b(sorry\|admit)\b\|^[[:space:]]*axiom\b' Stage1_Instances/THM-M-0778 -g '*.lean'` | 1 | expected no-match exit; no prohibited placeholder or local axiom occurs in owned Lean source |
| `python3 -m json.tool Stage1_Instances/THM-M-0778/instance.json` | 0 | intake JSON is syntactically valid |
| `python3 -m json.tool Stage1_Instances/THM-M-0778/task-dag.json` | 0 | task DAG JSON is syntactically valid |

## Required unblocker and status boundary

An accountable source reviewer must archive and hash an immutable primary or precise modern source,
identify the exact theorem/section/page, transcribe every incorporated definition and assumption,
resolve translation and errata, and independently approve the crosswalk. The intake dependency must
also receive master acceptance. Only then may a statement worker encode precisely that claim, fix
the theory and proof calculus, minimize pinned imports, fingerprint the elaborated expression,
check alternate transports, and execute all four mutation classes.

This statement node remains `[ ]`, blocked at `M4`; the dossier remains `planned` with root
`[H1, M4, R4]`, `audit_complete: false`, and `theorem_complete: false`. This is a truthful
statement-phase blocker, not completion of this or any later node. Because the assigned deliverable
did not pass its gate, no `.stage1-worker-selftest.json` is emitted.
