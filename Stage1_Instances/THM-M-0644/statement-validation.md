# Statement validation

Item: `S56-M-0644-STATEMENT`. Base revision:
`ba66c12eb0b1828b8aa19b6fa8eb2171a454e162`.

The one direct import is `Mathlib.ModelTheory.Satisfiability`. The checked target preserves the
universe-polymorphic language and arbitrary theory, and expands `IsFinitelySatisfiable` without
adding hypotheses. A proved transport covers the repository's finite-`Set` wording. Four
deliberately different propositions test containment, sentence domain, binder scope, and the empty
theory boundary using `#check_failure`; their diagnostic messages in the successful Lean run are
expected-negative evidence.

| Command | Exit | Result |
|---|---:|---|
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0644/Statement.lean > /tmp/thm-m-0644.print` | 0 | target and transports elaborated; four mutations rejected; output SHA-256 `b6a0f1d4...0171` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | standard and 1546-target projection valid |
| `python3 scripts/stage1_target.py check` | 0 | manifest valid |
| `python3 scripts/stage1_target.py show THM-M-0644` | 0 | rank 690, planned, theorem incomplete |
| `rg -n '(sorry|axiom|placeholder|admit|unsafe)' Stage1_Instances/THM-M-0644/Statement.lean` | 1 | no matches |
| JSON parsing and scoped invariants | 0 | statement and receipt identity, hashes, state, and completion boundary valid |
| `git diff --check -- Stage1_Instances/THM-M-0644 .stage1-worker-selftest.json` | 0 | no whitespace errors |

This is self-tested statement evidence pending master acceptance, not proof credit. Primary-source
acceptance, anchor provenance/trust, obligation composition, kernel proof closure, hermetic replay,
and independent review remain downstream failures. No `.lake` update, build, clone, fetch, or
mutation was performed.
