# THM-M-0119 validation-phase evidence

Item: `S56-M-0119-VALIDATION`. Base revision:
`80f0191c83a1bb4026c2d490be957cf109464de1`; base tree:
`b89a01cfc623bf97d1896fb3534a1ac24381fa71`.

Final structured-recipe interval: `2026-07-15T16:09:43+08:00` to
`2026-07-15T16:10:00+08:00` (`Asia/Shanghai`).

## Verdict

`blocked_after_self_test_pending_master_acceptance`. The network-isolated,
trust-zero recipe freshly elaborates the frozen statement, the proof phase's
`Int` countermodel, both conditional composition declarations, and a
separately implemented `ZMod 2` countermodel. The differential module imports
`Statement` but not `Proof`, shares no countermodel declaration or proof body,
and independently checks

```text
Not (Stage1Instances.THMM0119.KawamataViehwegVanishingTarget.{0, 0}).
```

Both countermodels report exactly `propext`, `Classical.choice`, and
`Quot.sound`. The validation declaration is sorry-free, and its transitive
closure reports 15,934 declarations in 589 modules with no unexpected
bodyless nonaxiom or unsafe declaration. The two composition declarations are
axiom-free but consume the missing vanishing premise and close no obligation.

This is blocker validation, not Kawamata--Viehweg vanishing. It confirms that
the frozen abstract backend target is disconnected: the named geometric
propositions do not constrain the arbitrary `cohomology` family. It does not
refute the mathematical theorem, assign human debt `H5`, provide a positive
proof body, or alter the accepted `[H4, M3, R4]` boundary.

The proof predecessor is only a provisional `[_]` scheduler item and remains
`open` with no accepted receipt in the target-local task DAG. The worker run
uses a shared warm dependency cache and the differential probe shares this
worker, checkout, toolchain, and cache. It is therefore neither an empty-cache
cold hermetic release nor section 10.7 distinct-runner independent
verification. `audit_complete=false` and `theorem_complete=false`.

## Commands And Results

No command ran `lake update`, `lake build`, a dependency clone/fetch, or a
network request, and no command mutated `.lake`.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | All 15 assurance groups and 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1 through 1546 passed. |
| `python3 scripts/stage1_target.py show THM-M-0119` | 0 | Rank 38; planned L0/rework-required target; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0119/check_obligation_tree.py` | 0 | 33 obligations and 42 typed edges passed; denominator `d9c76b6b...92db`; frozen root remains open M3. |
| `python3 Stage1_Instances/THM-M-0119/check_anchor_audit.py` | 0 | Immutable local pins and boundaries passed; no exact positive terminal candidate exists. |
| execute `validation-spec.json` `argv` without shell interpolation | 0 | The validator ran every Lean replay with a read-only host root and private `/tmp` in a Bubblewrap network namespace; frozen statement, proof blocker, composition, and differential blocker replayed at trust zero. |
| `python3 -m json.tool` over validation spec, receipt, and worker self-test | 0 | All three structured artifacts parsed. |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-m0119-validation-pycache python3 -m py_compile Stage1_Instances/THM-M-0119/check_validation.py` | 0 | Validator syntax checked outside the repository. |
| `PYTHONOPTIMIZE=1 python3 -B Stage1_Instances/THM-M-0119/check_validation.py --probe` | 1, expected | Fail-closed optimized-mode mutation was rejected before validation. |
| prohibited-device scan over the four target Lean sources | 1, expected | No `sorry`, `admit`, `sorryAx`, bodyless declaration, unsafe/external escape, `native_decide`, or `implemented_by` occurred. |
| `git diff --check -- Stage1_Instances/THM-M-0119 .stage1-worker-selftest.json` | 0 | No scoped whitespace diagnostics. |

The structured recipe's four Lean stream SHA-256 values are:

```text
Statement.lean       e7402bc1bb4f1bc6255436b7d7635869788000c47450782fa75cf8272dac644b
ObligationTree.lean  f2ba3ac92c0cdff043432949d1445d9b85aa8114a413fa9392b7982e801c7f5b
Proof.lean           c6b29f07f5d9175a9aa2439c336d176a5cb200801d6a2769f0fa01754003eb42
Validation.lean      98f89fafdfe3f9c0c604c2f22e0a3909204b3127eaf508a1f3f1e2a004cd58a8
```

The freshly emitted `Statement.olean` SHA-256 is
`01729724a41a4bee420c56a7f3fbcd0d4dd681ba039a7633d3739c2239919e0b`.

## Gate Decisions

| Gate | Decision | Evidence or failure |
|---|---|---|
| Narrow kernel replay | provisional pass for blocker | Both distinct local countermodels negate the same exact frozen specialization at trust zero. |
| Hygiene and observed trust | provisional pass for blocker | Both countermodels are placeholder-free and use only the observed classical trio; complete accepted foundation/TCB closure is absent. |
| Selected provenance | provisional pass for blocker | Frozen local inputs, clean mathlib pin/tree/origin/license, selected sources/oleans, and tool identities agree; complete transitive provenance/SBOM is absent. |
| Positive root and dependency | fail closed | The exact backend target has checked countermodels, and `S56-M-0119-PROOF` is not master accepted. |
| Human source and readability | fail closed | The instance remains H4/R4; no accepted H0 or independently reviewed R0 exists. |
| Hermetic release | fail closed | The run has fresh outputs and denied network but reuses a warm shared dependency cache; no clean checkout, cold build, offline restoration, or deterministic bundle exists. |
| Independent verification | fail closed | The ZMod probe is differential same-worker evidence, not a distinct identity, clean runner/cache, signed attestation pair, or independently implemented minimal verifier. |

The first node failure is
`dependency.S56-M-0119-PROOF.master_acceptance_and_S56-5.1-exact-target-consistency`.
The first release failure is `S56-10.6-HERMETIC-COLD-EMPTY-CACHE`.

The frozen graph's remaining cut stays `M0119-X-APIS`,
`M0119-N-RESOLUTION`, `M0119-L-SMOOTH`, and `M0119-C-PUSH`. The checked
countermodels additionally propose invalidating `S56-M-0119-STATEMENT`,
`M0119-S-DATA`, `M0119-S-HYP`, and `M0119-ROOT`; this validation node does not
rewrite that prerequisite architecture.

Positive execution can resume only after replacing the disconnected fields
with native or law-bearing definitions, accepting a new exact statement
fingerprint and registry version, and rerunning every dependent phase. This
genuinely self-tested validation implementation proposes worker state `[_]`
only for its truthful blocked receipt. It grants no accepted obligation,
`M0-*`, `E0/E1`, `AUDIT-Z`, `THEOREM-Z`, release, theorem completion, or master
acceptance.
