# Anchor-audit validation record

Item: `S56-M-1053-ANCHOR_AUDIT`  
Base revision: `8b61d0242da6b4b6810daf423a82881bc4a5c956`

## Verdict

Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` contains the exact Birkhoff-average
encoding and useful adjacent invariance results, but no pointwise ergodic convergence theorem.
`AnchorAudit.lean` checks that a verbatim copy of the frozen `timeAverage` is definitionally equal
to mathlib's `birkhoffAverage`, and probes the average shift identity and ergodic constant-function
result. These interfaces do not prove the frozen root.

Two external Lean 4 projects were inspected from content-hashed archives at immutable commits.
`lua-vr/pointwise-birkhoff@fc06094c` proves convergence to invariant conditional expectation, but
does not expose the frozen ergodic integral specialization. The stronger
`marcmorningstar/lean4-ergodic-theory@ed3fa6b8` has source-visible theorems for general convergence,
invariance, and the ergodic space-integral conclusion. It is therefore an `M1` exact external
candidate, not `M0`: it is absent from the local dependency closure, uses Lean 4.30.0-rc2 and a
different mathlib revision, and no exact adapter or transitive trust closure was checked locally.

GitHub repository search found those two projects. GitHub code search was rate-limited, and the
Sourcegraph query saturated on mathlib's unrelated Birkhoff results and sum definitions; neither
limitation is reported as proof of global absence. No dependency update, clone, fetch, install, or
build was performed.

## Commands and results

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets valid |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546 |
| `python3 scripts/stage1_target.py show THM-M-1053` | 0 | rank 245; planned; legacy artifacts unaccepted; theorem incomplete |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1053/Statement.lean` | 0 | frozen target re-elaborated |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1053/AnchorAudit.lean` | 0 | average identity and three adjacent anchors checked; wrapper axioms are `propext`, `Classical.choice`, `Quot.sound` |
| `python3 Stage1_Instances/THM-M-1053/check_anchor_audit.py` | 0 | mathlib revision/tree/clean state and scoped source hashes agreed; root `M1` |
| GitHub repository searches for the three recorded queries | 0 | complete counts `1`, `0`, and `2`; response hashes recorded in `anchor-audit.json` |
| immutable archive download and inspection at commits `fc06094c...` and `ed3fa6b8...` | 0 | archive/source/toolchain/manifest hashes and candidate declarations recorded |
| `rg -n '\b(sorry\|admit\|axiom\|unsafe)\b' .../BirkhoffErgodicThm --glob '*.lean'` | 1 | expected no-match: all seven Lean files in the first archive lack forbidden tokens |
| same scoped scan of `ErgodicTheory/Ergodic/Birkhoff.lean` | 1 | expected no-match in the exact candidate source file |
| GitHub code-search API for `Birkhoff language:Lean` | 0 | HTTP 403 rate-limit response captured; not negative evidence |
| Sourcegraph public query recorded in `anchor-audit.json` | 0 | saturated mathlib-only response captured and hashed |
| `python3 -m json.tool Stage1_Instances/THM-M-1053/anchor-audit.json` | 0 | structured audit valid JSON |
| `git diff --check -- Stage1_Instances/THM-M-1053 .stage1-worker-selftest.json` | 0 | no whitespace errors |

## Open gate

The next proof route must either authorize and pin the external project or construct a local proof,
then elaborate an exact `StatementShape` adapter and audit all transitive bodies and axioms. This
anchor audit does not prove the theorem, accept `M0`, close the human-source/readability audits, or
satisfy release gates.
