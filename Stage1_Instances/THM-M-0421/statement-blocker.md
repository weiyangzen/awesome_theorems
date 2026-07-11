# THM-M-0421 statement-gate blocker

Item: `S56-M-0421-STATEMENT`  
Base revision: `5621fb5119a237a67e9b70d078ce7c9c84a37284`

## Verdict

The exact Lean target cannot yet be frozen without inventing mathematics that is absent from the
source and deliberately unresolved by the accepted intake artifact. Consequently this phase is
blocked at the rev-5.6 exact-statement gate. No canonical `Statement.lean`, expression fingerprint,
or worker self-test receipt is emitted.

The upstream source supplies only the phrases "local class field theory" and "abelian extensions
of local fields." The intake correctly leaves the following target-defining choices open:

1. whether the base-field quantifier covers every nonarchimedean local field supported by
   `IsNonarchimedeanLocalField`, including equal characteristic, or only finite extensions of
   `Q_p`;
2. whether local reciprocity sends a uniformizer to arithmetic or geometric Frobenius;
3. the Lean representation of finite abelian extensions and the equivalence relation used by the
   classification claim;
4. whether tower functoriality and inclusion reversal are root conclusions or later obligations.

These are semantic differences, not presentation choices. The rev-5.6 statement gate forbids
selecting one silently, and it also requires checked transports for credited alternatives.

## Legacy candidate audit

`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_076.lean` elaborates in the pinned environment,
but it is not an exact replacement for the unresolved canonical claim. Its `StatementShape`:

- quantifies over all `IsNonarchimedeanLocalField` instances, thereby choosing the unresolved
  characteristic scope;
- contains no Frobenius normalization condition;
- existentially returns raw extension carrier types rather than classification modulo a frozen
  notion of `K`-isomorphism;
- states existence and finite-level kernel/surjectivity, but not a checked correspondence,
  injectivity, inclusion reversal, or tower compatibility.

Promoting that discovery shape would therefore broaden or substitute the theorem and would
violate the uniform-L0 rule. Its successful elaboration is recorded only as diagnostic evidence
that the pinned low-level APIs exist.

## Commands and results

Commands ran in this worker clone on 2026-07-12. Lean commands ran from `Formalizations/Lean` and
used the existing canonical `.lake` artifacts; no dependency update or fetch was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0421` | 0 | rank 76; planned; `hard_mathlib_anchor_and_wrapper`; theorem incomplete |
| `lake env lean AwesomeTheorems/Stage1/S1_M_076.lean` | 0 | legacy candidate and low-level anchors elaborated; printed `StatementShape : Prop` and audit declarations |
| `lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `sha256sum lean-toolchain lake-manifest.json` | 0 | `651c8acc...1d2` and `321626c8...d81` |

## Required resolution

An authoritative mathematical source receipt must pin the base-field scope, reciprocity
normalization, extension-isomorphism convention, and exact classification/functoriality package.
After those choices are accepted into the intake record, this node can encode that claim, minimize
imports, serialize its elaborated expression, and run the required removed-hypothesis,
changed-domain, changed-scope, and boundary mutations.

Status boundary: this is an actionable blocker record, not statement completion, proof evidence,
or permission to advance `S56-M-0421-ANCHOR_AUDIT`.
