# Exact-statement gate: blocked

Item: `S56-M-0019-STATEMENT`

Theorem: `THM-M-0019`

Base revision: `028e2535b68678b8296e63e2cacb05ed9775a2d8`

## Decision

The exact Lean 4 target cannot be truthfully selected or elaborated from the provisional intake and
repository source record. The complete repository wording is only the theorem name, Chebotarev
density theorem, and the gloss "density distribution of prime-ideal splitting." The metadata label
`已验证` is explicitly untrusted under rev-5.6. It supplies neither an exact mathematical
proposition nor machine evidence.

The intake correctly leaves `canonical_claim`, `declaration_or_expression`, and
`elaborated_expression_hash` null. Its 1926 Tschebotareff paper is only a bibliographic candidate:
the dossier has no immutable copy or passage hash, pinpoint theorem/page transcription,
assumption and errata crosswalk, or independent source review. Consequently the source record does
not decide choices that materially change the target:

- natural density, Dirichlet density, or a statement proving both;
- the exact finite Galois extension model and ordered number-field binders;
- nonzero prime versus maximal ideals, the ordering norm, and the ramified-prime exclusion;
- arithmetic versus geometric Frobenius and the inverse-Frobenius convention;
- one conjugacy class, a conjugacy-stable subset, or a splitting-type formulation;
- trivial extensions, empty selected subsets, and other boundary cases.

Choosing the familiar formula `|C| / |Gal(L/K)|` does not resolve those binders, hypotheses, or
conventions. It would silently substitute one standard member of the theorem family for the
unidentified source claim. An abstract structure carrying a `FrobeniusClass` or density conclusion
as an unconstrained proposition would instead be a placeholder, not a formalization. Both choices
are forbidden by the assignment and the rev-5.6 statement gate.

This phase therefore stops at canonical human-claim identity. With no exact proposition, there is
no meaningful minimal-import claim, normalized expression fingerprint, checked alternate-form
transport, or removed-hypothesis, changed-domain, binder-scope, and boundary mutation suite.
Machine status remains `M4`.

The intake dependency itself is only worker-self-tested (`[_]`) and still awaits master acceptance;
nothing in this artifact treats it as accepted state.

## Pinned Lean boundary

The existing `IntakeProbe.lean` was re-elaborated with its three direct imports:

```lean
import Mathlib.NumberTheory.NumberField.Basic
import Mathlib.RingTheory.Ideal.Norm.RelNorm
import Mathlib.GroupTheory.GroupAction.Quotient
```

It checks `NumberField`, `Ideal.primesOver`, `Ideal.relNorm`, `Ideal.inertiaDeg`, `ConjClasses`, and
`ConjClasses.card_carrier`. These are nearby algebraic ingredients only. The probe does not define
an unramified-prime predicate, a prime's Frobenius conjugacy class, a prime-ideal density, or the
Chebotarev conclusion. A bounded name search also found no Chebotarev spelling in the pinned
mathlib sources. Neither result is an anchor audit or canonical-statement evidence.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, with mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. The SHA-256 values of
`Formalizations/Lean/lean-toolchain` and `Formalizations/Lean/lake-manifest.json` are respectively
`651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2` and
`321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`. The worker reused the
pre-existing untracked `.lake` symlink to the canonical pinned artifacts. No update, build, fetch,
clone, or dependency mutation was performed.

## Validation evidence

Commands ran from this worker clone on 2026-07-12 (Asia/Shanghai). The Lean probe command ran from
`Formalizations/Lean`; all other commands ran from the repository root.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0019` | 0 | rank 897, planned, legacy artifacts unaccepted, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-0019/instance.json` | 0 | valid JSON; canonical claim, declaration, and expression hash remain null |
| `python3 -m json.tool Stage1_Instances/THM-M-0019/task-dag.json` | 0 | valid JSON; statement and every downstream task remain open |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0019/IntakeProbe.lean` | 0 | all six nearby pinned APIs elaborated and their types were printed |
| `rg -ni 'chebotarev|chebotaryov|tschebotareff' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 1 | no matching name in pinned mathlib; bounded negative discovery only |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | toolchain and dependency-manifest hashes match the values above |
| `git status --short` (pre-edit) | 0 | only the pre-existing untracked `Formalizations/Lean/.lake` symlink |
| `git diff --no-index --check /dev/null Stage1_Instances/THM-M-0019/statement-blocker.md` | 1 | expected add-file diff status; no whitespace diagnostics |

## Retry condition and boundary

Retry only after an accountable source reviewer supplies an immutable primary-source snapshot and
content hash, transcribes a pinpoint theorem and all referenced definitions and assumptions, audits
errata, and freezes every convention and boundary choice listed above. A later statement worker
must then encode that exact claim without conclusion-bearing placeholder fields, minimize its
pinned imports, serialize and hash its elaborated expression and environment, check every credited
alternate encoding, and run all four required mutation classes.

First failed gate: rev-5.6 section 5 exact canonical-claim identity. The canonical target, minimal
imports, expression fingerprint, checked transports, and mutation suite remain known failures. No
statement credit, proof credit, debt-vector promotion, audit completion, theorem completion, or
downstream-node credit is claimed. Because the assigned phase is not self-tested to its completion
gate, no `.stage1-worker-selftest.json` is emitted.
