# Statement validation

This record covers only `S56-M-0912-STATEMENT`. It freezes and elaborates the constrained
predecessor recurrence printed by NIST DLMF 26.3.5:

```text
C(m,n) = C(m-1,n) + C(m-1,n-1),  m >= n >= 1.
```

The canonical Lean target uses ordered natural binders `m`, `n`, premises `n <= m` and `1 <= n`,
and the displayed summand order. This is deliberately not the broader zero-extended recurrence for
all natural indices. The preserved source lead is sufficient to select this conservative exact
statement for downstream review; it does not establish the catalog's historical attribution or an
accepted H0 proof-source crosswalk. The stable equation-response hash preserves the formula but not
an immutable full context for the displayed side condition or coefficient definition; the observed
section response and explicit H1 boundary record that remaining source-fidelity limitation.

## Checked surface

`Statement.lean` declares the exact proposition and three checked equivalent encodings: a
conjunction form of the source constraint, the reversed summand order used by a pinned mathlib
predecessor lemma, and a successor reindexing that retains the necessary `k <= r` guard. These are
statement transports only. No inhabitant of the canonical proposition and no pinned terminal proof
body is imported or credited.

Four explicit mutations change, respectively, the positive-column hypothesis, binder domain,
column binder scope, and admitted diagonal. Lean rejects each definitional equality with the root,
and the checker independently serializes and hashes all five elaborated expressions. Semantic
witnesses show that deleting positivity admits a false `(0,0)` instance, the `Fin 10` domain omits
canonical row ten, the existential-column mutation fails already at row zero, and the
strict boundary excludes every diagonal. Additional witnesses cover `(1,1)`, column zero,
out-of-range columns, and the broader unrestricted successor relation.

The canonical-target-only fixture elaborates with the sole direct import
`Mathlib.Data.Nat.Choose.Basic`; deleting that import fails. This establishes deletion-minimality
for the recorded fixture, not a global theorem about every possible refactoring of mathlib imports.

## Environment

- Base revision: `fb0baac89ea0633612be3b47448464b4b8e4bef7`; tree
  `018557070da18ea1733a82de81a238750c59aa84`.
- Lean: 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Lake: `5.0.0-src+98dc76e`.
- mathlib: `8a178386ffc0f5fef0b77738bb5449d50efeea95`; tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package worktree clean.
- Canonical elaborated-expression SHA-256:
  `b322549a05e57fbf466b60eb8ff89f4a08c6ee3b68ea5bf3ff3bf86d99521776`.
- Canonical environment-fingerprint SHA-256:
  `8e8dc7bd4f64ddaca552ca92399f15d52a008ac0d44ad8db83731f9c453b0749`.
- Statement source SHA-256:
  `63fda2462d33fba5f18ba0c46df33d7c34c2442609992e7435a2ab4ac33e434e`.
- Canonical Lean output SHA-256:
  `b042efdd38f3527b1c3b06dfd05f6622f76d2cd78ae3235bb3fdacc640d01262`.

The initial worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. It was used read-only. No
dependency update, build, clone, fetch, or `.lake` mutation was performed. The owned outputs and
root handoff make this dirty, nonrelease evidence.

## Commands and results

All repository commands ran from the repository root on 2026-07-13 Asia/Shanghai unless a `cwd` is
shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets in ranks 1 through 1546 passed |
| `python3 scripts/stage1_target.py show THM-M-0912` | 0 | rank 1454, planned L0/rework_required target, no legacy slot, theorem incomplete |
| `lake env lean --version` (`cwd=Formalizations/Lean`) | 0 | Lean 4.29.0 at the recorded commit |
| `lake --version` (`cwd=Formalizations/Lean`) | 0 | Lake 5.0.0-src+98dc76e |
| `lake env lean ../../Stage1_Instances/THM-M-0912/Statement.lean` (`cwd=Formalizations/Lean`) | 0 | root, transports, mutations, boundaries, axiom reports, and explicit expression elaborated; output hash above |
| `python3 -B ../../Stage1_Instances/THM-M-0912/check_statement.py --worker-packet ../../.stage1-worker-selftest.json` (`cwd=Formalizations/Lean`) | 0 | expression, mutations, import deletion, pins, structured records, receipt, and handoff agreed |
| `python3 -B Stage1_Instances/THM-M-0912/check_intake.py` | 0 | historical intake receipt plus reconciled planned instance, expanded inventory, and six open tasks remain structurally consistent |
| `python3 -m json.tool` on `statement.json`, `statement-receipt.json`, and `.stage1-worker-selftest.json` | 0 | all current structured artifacts parsed |
| prohibited-construct `rg` scan of `Statement.lean` | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, axiom, constant, opaque, or unsafe declaration |
| `git diff --check -- Stage1_Instances/THM-M-0912 .stage1-worker-selftest.json` plus scoped byte checks | 0 | no invalid bytes, missing newlines, trailing whitespace, or diff diagnostics |

## Open gates

The intake and statement proposals remain pending master acceptance. Historical primary-source
ratification, complete proof and correction crosswalk, independent H0 review, formal anchor and
terminal proof-body provenance/trust audit, obligation freeze, proof integration and composition,
readable reconstruction, hermetic validation, independent verification, deterministic release,
audit completion, and theorem completion remain open. The intake checker was reconciled to preserve
the immutable intake receipt while recognizing the expanded statement-phase inventory and current
planned instance; it grants no statement acceptance or proof credit.
