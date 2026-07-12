# Statement gate blocker

Item: `S56-M-1541-STATEMENT`  
Theorem: `THM-M-1541`  
Verdict: blocked; no exact canonical Lean target is claimed.

## First failed gate

The authoritative repository record names the subject "twistor theory" and supplies only the gloss
"complex geometry and physics", attributed to Roger Penrose in 1967. It identifies no work,
edition, theorem, page, objects, quantifiers, hypotheses, or conclusion. Twistor theory is a
programme containing mutually non-equivalent theorem families, including projective incidence
geometry, the Penrose transform, the nonlinear graviton correspondence, and Ward correspondence.
Selecting any one of them would invent missing mathematics and substitute a narrower theorem for
the source record.

The legacy discovery module
`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_202.lean` elaborates, but it does not repair the
source ambiguity. Its `StatementShape` quantifies over user-supplied `TwistorFibrationData`,
`TwistorHolomorphicData`, and `TwistorFieldData` interfaces and concludes that a user-specified
`TwistorTransformPackage` is nonempty. The fields encode the twistor-specific geometry, field
equations, and transform laws as abstract propositions or functions rather than defining a
particular source theorem. The module itself calls this a formalization boundary and explicitly
denies terminal-theorem status. It is therefore discovery input only and receives no exact-
statement credit under the uniform `L0 / rework_required` baseline.

Rev-5.6 section 5 requires a canonical mathematical claim before its Lean expression, minimal
imports, normalized expression hash, and environment fingerprint can be accepted. Since claim
identity fails first, there is no source-faithful expression on which to run the required removed-
hypothesis, changed-domain, binder-scope, and boundary-case mutations. No proxy theorem, new axiom,
or proof hole was introduced. The machine state remains `M4`, and statement acceptance and theorem
completion remain false.

## Environment fingerprint

- Repository base revision: `6d7db94bb24d91df72f83fd7a393db356a7bb93b`.
- Validation date: 2026-07-12 (Asia/Shanghai).
- Lean toolchain: `leanprover/lean4:v4.29.0`; Lean `4.29.0`, commit
  `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Checked mathlib revision: `8a178386ffc0f5fef0b77738bb5449d50efeea95`.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- Lake manifest SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.
- Legacy discovery module SHA-256:
  `fe752383ae3bc1c853395033012abc6a0a5fdfc0df8dc6fabfe1e5e4988c26bc`.

## Validation evidence

Commands ran in this worker clone. Lean used only the existing canonical pinned `.lake` artifacts;
no update, build, fetch, or clone command was used.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1541` | 0 | Rank 202, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_202.lean` | 0 | Legacy abstract boundary elaborated; its printed `StatementShape` is not an exact source theorem |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | Checked mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `rg -n -i 'twistor\|Penrose transform\|nonlinear graviton\|Ward correspondence' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 1 | No matching declaration or source reference in pinned mathlib; exit 1 means no matches |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_202.lean` | 0 | Hashes match the environment fingerprint above |

## Retry condition

The authoritative lane must first pin a primary source and a precise theorem/page and justify why
that exact claim represents `THM-M-1541`. The source crosswalk must fix every object, convention,
hypothesis, conclusion, and degenerate case. A later statement run can then encode that claim with
minimal pinned imports, serialize the elaborated expression and environment, assess alternate
encodings, and run all four required mutation classes.

Until then the statement node is not self-tested to its completion gate. Consequently no
`.stage1-worker-selftest.json` is emitted.
