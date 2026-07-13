# THM-M-0936 exact-statement gate: blocked

- Item: `S56-M-0936-STATEMENT`
- Base revision: `d66b6e80968b53d5b99774584721ae8976f303a5`
- Base tree: `aaa82721074fccea81033a9a18d21652af89f8e4`
- Attempt date: 2026-07-13 (Asia/Shanghai)
- Verdict: blocked; no statement receipt, worker `[_]`, or theorem-completion claim

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the authoritative repository record.
The complete catalog statement is only `有限域上子集和的下界`: "a lower bound for subset sums over
a finite field." It does not say that there are two sets, define their pointwise sumset, restrict
the carrier to a prime field or prime cyclic group, require nonempty inputs, select a cardinal
encoding, give the capped lower-bound formula, or fix ordered binders and boundary cases. Stage0
explicitly leaves the precise definitions, premises, proof route, equivalent forms, logical
principles, machine status, and artifact links open. The catalog's `已验证` label is untrusted
metadata under rev-5.6.

The inspected versioned modern source makes one conventional candidate precise. Wheeler,
arXiv `1202.1816v1`, Definition 1.1 and Theorem 1.4, states that for prime `p` and nonempty subsets
`A, B` of `Z/pZ`,

```text
|A + B| >= min(p, |A| + |B| - 1).
```

That paper is a modern source lead rather than a catalog-cited primary Cauchy or Davenport
edition. No accepted source-adoption decision, complete primary definition/premise/proof/errata
map, or independent review connects it to the catalog root. It therefore does not authorize this
worker to add every proposition-changing clause omitted by the catalog.

The finite-field wording creates a further material fork. The conventional `Z/pZ` theorem caps at
`p`. A formula for an arbitrary extension field capped by the field cardinality is false: taking a
nontrivial proper additive subgroup `H` and `A = B = H` gives `A + B = H`. A valid generalization
instead uses the characteristic or the additive group's minimal nontrivial element order. The
catalog selects neither the classical prime-cyclic root nor such a generalization. Choosing the
familiar pinned declaration would therefore narrow the received finite-field wording and invent
its missing two-set, nonemptiness, cap, cardinal, subtraction, and boundary semantics.

Sections 5 and 5.1 of the rev-5.6 blueprint make statement ambiguity and a missing elaborated
expression fingerprint hard blockers. The intake correctly leaves the canonical human statement,
Lean module and expression, minimal target imports, expression hash, environment-expression
fingerprint, binders, hypotheses, alternate encodings, and excluded cases null or empty at
`[H1, M3, R4]`. Consequently the removed-hypothesis, changed-domain, changed-binder-scope, and
boundary-case mutations are undefined rather than passed. No `Statement.lean`, assumed target,
proof body, weakened consequence, or broadened theorem was introduced.

The prerequisite `S56-M-0936-INTAKE` is only provisional worker state `[_]`. Its receipt declares
`accepted: false`, is unsigned and not content-addressed, has no accepted receipt ID, and leaves the
canonical target null. That independently prevents an accepted statement transition.

## Pinned Lean Boundary

The existing discovery-only `IntakeProbe.lean` imports
`Mathlib.Combinatorics.Additive.CauchyDavenport`. A fresh narrow replay elaborated these pinned
interfaces:

```lean
ZMod.cauchy_davenport
  {p : Nat} (hp : p.Prime)
  {s t : Finset (ZMod p)}
  (hs : s.Nonempty) (ht : t.Nonempty) :
  min p (s.card + t.card - 1) <= (s + t).card
```

and the stronger group-level `cauchy_davenport_minOrder_add`. Both direct axiom diagnostics
reported only `propext`, `Classical.choice`, and `Quot.sound`. The probe declares no canonical
THM-M-0936 target, checked source transport, or proof body. Its import is therefore a
candidate-interface import, not a certified minimal import for an absent canonical target, and it
receives no statement, anchor, or proof credit.

A bounded search found these names only in the owned intake probe and the pinned mathlib module;
this is narrow discovery evidence, not the downstream exhaustive anchor or terminal-body audit.
The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` link to canonical pinned artifacts was used read-only. No dependency
update, build, clone, fetch, or other `.lake` mutation was run.

## Validation Evidence

Commands ran in this isolated worker clone on 2026-07-13 (Asia/Shanghai), from the repository root
unless another working directory is shown. Exact arguments, exits, result summaries, and input
hashes are also recorded in `statement-blocker.json`.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0936` | 0 | rank 1475; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| pre-edit `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` link was untracked; the base revision and tree appear above |
| current `sha256sum` over authority, source, intake, toolchain, lockfile, and pinned Cauchy-Davenport inputs | 0 | exact fingerprints are recorded in the structured blocker |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | Lean 4.29.0 at commit `98dc76e3...`; Lake `5.0.0-src+98dc76e` |
| mathlib revision, tree, and status checks | 0 | revision `8a178386...ea95`, tree `bdc39a31...5c2b`, clean package worktree |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0936/IntakeProbe.lean` | 0 | two interfaces and two candidate axiom diagnostics elaborated; 548 output bytes; SHA-256 `213f9a1f3818459beca88cfe1305f3901a1bd09f8de0c0dc980c25c8067c6a25` |
| bounded declaration search in the owned path and pinned module | 0 | the probe references and pinned declaration were found; no canonical target identity is inferred |
| `python3 -B Stage1_Instances/THM-M-0936/check_intake.py` | 1 | historical intake checker stops because it expects authoritative intake state `[ ]`, attempts 0, while current authority records `[_]`, attempts 1; historical evidence was not rewritten |
| final JSON parse, scoped invariant assertions, prohibited-declaration scan, and whitespace checks | expected results | recorded in the structured blocker and rerun after final serialization |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test packet intentionally absent because the exact-statement deliverable did not pass |

A blocked-run artifact check is not a statement-node self-test. The passing Lean probe confirms
only the pinned candidate surface described above.

## Retry Condition And Status Boundary

The integration lane must master-accept refreshed intake evidence. Accountable reviewers must
lawfully preserve and hash one complete primary or approved authoritative edition, select and
independently approve the classical prime-cyclic statement or another exact source-defined root,
and transcribe every incorporated definition, binder, premise, conclusion, cap, cardinal and
subtraction convention, correction, erratum, proof boundary, and degenerate case. They must
approve every source-to-Lean specialization, generalization, and transport, including the finite-
field versus prime-field decision.

A fresh statement worker can then encode exactly that approved claim, minimize its pinned imports,
serialize and hash the elaborated expression and environment, compile every credited transport,
and run all four mutation classes.

This is a blocked-attempt record, not completion of the statement node or any downstream node. The
root remains `[H1, M3, R4]`, with `audit_complete: false` and `theorem_complete: false`; no debt
change is proposed. Because the assigned phase is not genuinely self-tested to its completion
gate, no `.stage1-worker-selftest.json`, statement receipt, worker `[_]`, proof credit, or master
acceptance is claimed.
