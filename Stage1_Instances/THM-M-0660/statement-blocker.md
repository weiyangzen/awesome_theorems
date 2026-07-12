# Statement-phase blocker

Item: `S56-M-0660-STATEMENT`  
Theorem: `THM-M-0660`  
Base revision: `07cc89a04d18aba80d921bc643786856d7e22ad7`

## Verdict

The exact Lean 4 target cannot be frozen truthfully. The accepted intake preserves only the
repository wording "existence of a main formula in a stable theory". The repository supplies no
primary citation, theorem/page, or definition of `main formula`. The Chinese term `主公式` does not
by itself select a unique standard model-theory construction. It could not safely be translated as
"principal formula", "isolating formula", "defining formula", or another source-specific notion.
Those choices have different quantifiers, stability hypotheses, parameter scopes, and conclusions.

The inherited attribution to Saharon Shelah and year 1978 do not resolve the ambiguity. They are
unreferenced metadata in `Docs/researches/math_theorems.md` and `Docs/Stage0_Blueprint.md`, not a
pinpoint source statement. Choosing a familiar stability result would therefore substitute a new
theorem for the assigned claim, contrary to the exact-statement gate.

The historical discovery module
`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_299.lean` is not a source substitute. It explicitly
chooses singleton-clopen isolation as its local meaning of principal formula, chooses a finite-tuple
type-counting version of omega-stability, excludes parameters, and calls its result a statement-shape
candidate. Its target says every consistent formula has a consistent principal refinement. None of
these strengthening and interpretation choices is justified by the repository's unsourced phrase.
The module itself says its boundary is not a completed formalization of classical stability theory.

Consequently there is no canonical declaration or expression fingerprint, no truthful minimal
import set, no checked alternate encoding, and no meaningful removed-hypothesis, changed-domain,
changed-binder-scope, or boundary mutation suite. The statement node remains blocked at section 5.1
of `Docs/Stage1_Blueprint_rev-5.6.md`. No machine-proof, audit-completion, or theorem-completion credit
is claimed, and no `.stage1-worker-selftest.json` is emitted.

## Required unblock

An accountable source review must identify an immutable primary edition and pinpoint theorem/page,
transcribe the exact statement and the definition translated as `主公式`, and freeze the language,
theory completeness and stability convention, formula arities, parameter/model scope, cardinal
assumptions, and boundary cases. A later statement worker can then encode that claim, minimize its
imports, serialize its elaborated expression, and run all four required mutation classes.

## Narrow validation evidence

Commands ran from this worker clone on 2026-07-12. Lean used the existing pinned Lake environment;
no dependency update, fetch, clone, or other `.lake` mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups; 1546 uniform-L0 Lean 4 targets; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0660` | 0 | rank 299; planned; L0/rework-required; theorem incomplete |
| `cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_299.lean` | 0 | The historical candidate and its model-theory anchors elaborated; this is discovery evidence only |
| `git diff --check -- Stage1_Instances/THM-M-0660` | 0 | no output |

The historical-module check is deliberately not an exact-statement certificate. Its imports are
not claimed to be minimal, and successful elaboration cannot repair the missing source-to-statement
identity.
