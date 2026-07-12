# Statement-phase blocker

Item: `S56-M-1555-STATEMENT`  
Base revision: `d021f11112bde0e0efd8eac22cc92f1e7d610f13`

## Verdict

The exact Lean 4 target cannot truthfully be frozen from the available source record. This phase is
blocked at the source-statement identity gate and makes no statement-credit, proof, audit, or
theorem-completion claim.

The repository source says only "Darboux transformation", attributes it to Gaston Darboux in 1882,
and glosses it as a transformation of the Schrodinger equation. It supplies no edition, page,
result boundary, equation, domain, regularity assumptions, sign convention, spectral parameters,
seed conditions, or conclusion. The intake correctly records a historical lead, Darboux's *Sur une
proposition relative aux equations lineaires*, but no immutable copy or exact passage is present in
the repository. A direct attempt to inspect the BnF/Gallica lead returned HTTP 403, and the other
catalogue queries made during this phase produced no usable primary-source text.

Consequently, choosing any concrete formula now would invent at least some of the proposition. In
particular, the common modern expression involving a nonvanishing seed and logarithmic derivative
is only a theorem family in the current dossier; it is not an exact source-selected statement.
Encoding that expression would violate the rev-5.6 prohibition on broadened or substituted
theorems. No `.lean` target or artificial mutation test was therefore created.

## Gate evidence

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1555` | exit 0; rank 567, planned, L0/rework_required, legacy artifacts unaccepted, theorem incomplete |
| `rg -n 'Darboux|Darboux变换|Schr.dinger方程的变换' Docs Stage1_Instances Formalizations/Lean/.lake/packages/mathlib/Mathlib` | repository hits reduce to generic metadata/intake material; the mathlib Darboux module concerns derivatives, not this transformation |
| `curl -L --max-time 20 -s 'https://gallica.bnf.fr/ark:/12148/bpt6k3058v/f145.item.texteImage'` | remote response: `Access Denied: 403 Access Interdit`; no primary text obtained |
| `sha256sum Docs/Stage1_Targets_rev-5.6.json Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | exit 0; `02eec284...ab2c`, `651c8acc...b1d2`, `321626c8...2d81` |
| `(cd Formalizations/Lean && lake env lean --version)` | exit 0; Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | exit 0; pinned mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95` |

The pinned Lean environment is available, but elaborating a proposition merely to demonstrate that
the executable works would not validate the assigned exact-statement gate.

## Retry condition

Provide or repository-pin an immutable primary edition and exact page/result for the intended
transformation, then independently freeze its equation, domain, scalar field, differentiability,
seed/nonvanishing treatment, sign and spectral conventions, and precise conclusion. Once that
crosswalk is reviewable, the statement phase can create the minimal-import Lean expression,
serialize its elaborated form and environment fingerprint, and run the required removed-hypothesis,
changed-domain, binder-scope, and boundary-case mutations.

Because this phase is not self-tested, no `.stage1-worker-selftest.json` is emitted.
