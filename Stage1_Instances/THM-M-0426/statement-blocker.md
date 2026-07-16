# Statement gate blocker

Item: `S56-M-0426-STATEMENT`  
Theorem: `THM-M-0426`  
Base revision: `6e0ec7fe6fe851da29c6202c7ad2345f35f17800`

## Verdict

The exact source-faithful Lean 4 target cannot yet be selected, so this statement node is blocked
and remains open. The repository's complete source claim is only "the functional equation of the
Hecke L-function". It has no primary-source edition, theorem/page locator, exact transcription, or
normalization. In particular, it does not specify the class of Hecke characters (finite-order,
unitary, algebraic, or general quasicharacters), primitivity, conductor and infinity type, completed
function and gamma factors, reflection center, dual character, epsilon factor, or treatment of the
trivial/polar and imprimitive cases. These choices change the ordered binders, hypotheses, and the
equation itself. Selecting one would broaden or substitute the received claim rather than
elaborate it.

The accepted intake deliberately records this ambiguity with a null canonical statement and
machine state `M4`. The historical module
`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_080.lean` cannot resolve it. Its
`HeckeLFunctionData` takes the completed L-function, conductor factor, root number, center, dual,
and primitivity predicate as arbitrary fields, and `StatementShape` merely asks that those supplied
fields satisfy a chosen equation. Thus it is an abstract interface boundary, not an encoding of a
concrete Hecke character or its L-function, and receives no exact-statement credit.

The historical module elaborates in the pinned environment, while a scoped search of pinned
mathlib finds no `HeckeCharacter`, Hecke L-function, or idele-class character declaration. This
confirms that Lean is available and that the historical discovery artifact is syntactically valid;
it does not establish the missing mathematical identity. Since there is no exact target, no honest
minimal import set, normalized expression fingerprint, checked alternate transport, or required
removed-hypothesis/domain/binder/boundary mutations can be produced. No replacement predicate,
axiom, or unproved declaration was introduced.

First failed gate: exact source-statement identification under rev-5.6 sections 5 and 5.1.
Statement acceptance and theorem completion are false.

## Environment fingerprint

- Validation date: 2026-07-12 (Asia/Shanghai).
- Lean toolchain: `leanprover/lean4:v4.29.0`; Lean `4.29.0`, commit
  `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Checked mathlib revision: `8a178386ffc0f5fef0b77738bb5449d50efeea95`.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.
- Historical module SHA-256:
  `d48833b1368787ecadb73ff635769f28a9e991b5ed760a9785730b80b01abc87`.

## Validation evidence

Commands ran in this worker clone. Lean used the existing canonical pinned `.lake` artifacts; no
update, build, fetch, clone, or dependency mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Standard passed: 15 assurance groups and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | 0 | Manifest passed: 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0426` | 0 | Rank 80, planned, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_080.lean` | 0 | Historical abstract interface module elaborated; no exact-target credit |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0 at commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | Checked mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `rg -n -i 'HeckeCharacter\|Hecke character\|Hecke.*LFunction\|Hecke.*L-function\|idele.class\|IdeleClass' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 1 | No matching declaration or source occurrence in pinned mathlib (`rg` exit 1 means no match) |

## Retry condition

Provide an immutable primary source with an exact theorem/page locator and conventions selecting
the character class and normalization. The crosswalk must identify the number-field assumptions,
conductor, infinity type and gamma factors, completed L-function, dual, reflection center, epsilon
factor, and all primitive/imprimitive and polar boundary branches. The next statement run can then
choose concrete pinned Lean definitions, determine minimal imports, elaborate and fingerprint the
exact expression, and execute the mandatory mutations and checked transports.

## Current rev-5.6 packet

The 2026-07-17 statement retry refreshes this blocker with `statement.json`, a no-target Lean
boundary probe, an empty audited schema-1.1 dependency/reuse ledger, exactly one node receipt, and
the contract-selected validator. The v2 node's parent/reuse inspection order is empty; no provider
body or acceptance is consumed. The validator reports the semantic result `blocked` with
`phase_accepted=false`, rather than inferring acceptance from successful checks.

The negative packet is genuinely self-tested as a blocker handoff, not as the positive statement
deliverable. Its root `.stage1-worker-selftest.json` therefore proposes only `[_]` review of the
truthful blocked result. The exact target, statement fingerprint, mutation suite, statement phase
acceptance, downstream phases, audit completion, and theorem completion remain open.
