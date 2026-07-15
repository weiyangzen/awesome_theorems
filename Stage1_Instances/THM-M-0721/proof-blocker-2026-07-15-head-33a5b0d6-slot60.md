# THM-M-0721 proof recheck at `33a5b0d6` (slot60)

Item: `S56-M-0721-PROOF`

Intent: `prove`

Recheck date: `2026-07-15T12:37:06+08:00`

Base revision: `33a5b0d654c92a894e155f5385edaae684091bb0`

Base tree: `74ed89524afb3c118e31a7fce9b5763fee26b180`

## Verdict

`blocked`. No eligible proof body was implemented or found for the exact root
`Stage1Instances.THM_M_0721.ExistsNPCompleteLanguage`. The root remains
`[H1, M3, R4]`, and this proof item remains `[ ]`.

The checked declaration `root_of_candidate_packages` only consumes the two immediate root packages;
it constructs neither:

- `M0721-T-SAT-IN-NP`, requiring a faithful binary SAT encoding, correct bundled polynomial-time
  TM2 verifier, and polynomial certificate bound;
- `M0721-T-UNIVERSAL-HARDNESS`, requiring arbitrary-verifier normalization, Cook-Levin tableaux,
  both correctness directions, and a bundled polynomial-time TM2 reduction.

Eleven frozen SAT/Cook-Levin obligations remain open. Pinned mathlib supplies the TM2 substrate and
identity machine, but no NP-completeness endpoint. Its relevant composition declaration is
source-level `proof_wanted`; a trust-zero Lean query confirms that no checked constant was created.
Empty, universal, identity, and classical-choice constructions do not supply the required universal
polynomial-time verifier and reduction witnesses.

The immutable audit's external candidates remain ineligible: one supplies only fixed-tableau
support, and two headline endpoints contain root-relevant proof gaps or incompatible complexity
contracts. Fresh immutable-source replay failed during an HTTPS handshake timeout, so no new network
result is credited and the frozen content-addressed classifications remain unchanged.

The first failed gate is `M0721-N-SAT-ENCODING`. The immediate root cut is
`M0721-T-SAT-IN-NP` plus `M0721-T-UNIVERSAL-HARDNESS`. Because the positive proof phase is
incomplete, no proof receipt or `.stage1-worker-selftest.json` is emitted.

## Validation

The automation-provided untracked `Formalizations/Lean/.lake` symlink to canonical artifacts was
reused read-only. No dependency update, build, clone, fetch, checkout, or `.lake` mutation was
performed. The canonical `flt-regular` package has an invalid `HEAD`; normal `lake env lean` fails
before target elaboration. The exact target and conditional composition were therefore additionally
elaborated with immutable Lean 4.29.0 and existing precompiled pinned artifacts. This fallback is
nonrelease evidence only.

| Command | Exit | Exact result |
|---|---:|---|
| `git rev-parse HEAD HEAD^{tree}; git status --short --untracked-files=all; readlink Formalizations/Lean/.lake` | 0 | Base `33a5b0d6...1bb0`, tree `74ed8952...b180`; only the automation-provided `.lake` symlink was initially untracked. |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Passed 15 assurance groups and all 1546 uniform-L0 Lean 4 targets. |
| `python3 scripts/stage1_target.py check` | 0 | Passed 1546 unique targets at ranks 1 through 1546. |
| `python3 scripts/stage1_target.py show THM-M-0721` | 0 | Rank 578; `planned`; L0/rework-required; theorem incomplete. |
| `LEAN_NUM_THREADS=1 timeout 600s python3 Stage1_Instances/THM-M-0721/check_statement.py` | 1 | Lake exited through external Git code 128 because the unrelated pinned `flt-regular` checkout could not resolve `HEAD`; no dependency repair was attempted. |
| `python3 Stage1_Instances/THM-M-0721/check_obligation_tree.py` | 0 | Passed 18 obligations and 45 typed edges; denominator `375921a1...b92a`; root remained M3 with both terminal packages M4. |
| Copy `Statement.lean` and an import-adjusted `ObligationTree.lean` to a temporary workspace directory, derive `LEAN_PATH` only from existing pinned build outputs, then run immutable Lean 4.29.0 with `--trust=0 -t0` in dependency order | 0 | The exact target and conditional composition elaborated; `root_of_candidate_packages` reported exactly `[propext, Quot.sound]` and produced no terminal-package inhabitant. |
| Scan owned Lean files for `sorry`, `admit`, `axiom`, `unsafe`, `proof_wanted`, or `sorryAx` | 1 expected | No prohibited token occurs in owned Lean files. |
| Scan pinned mathlib Lean source for NP-completeness, SAT-language, or Cook-Levin endpoints | 1 expected | No eligible endpoint exists. |
| Search other repo-local Lean source for the exact target, terminal packages, and NP-completeness/Cook-Levin endpoints | 1 expected | No endpoint or implementation exists outside this target dossier. |
| Locate `proof_wanted TM2ComputableInPolyTime.comp` in pinned mathlib source | 0 | The open source-level composition declaration occurs at line 284. |
| Ask immutable Lean to `#print axioms Turing.TM2ComputableInPolyTime.comp` under the pinned import and trust-zero environment | 1 expected | Lean reported `Unknown constant`, confirming that source-level `proof_wanted` added no checked declaration. |
| `timeout 120s python3 Stage1_Instances/THM-M-0721/check_anchor_audit.py` | 1 | Fresh immutable-source replay failed on the first GitHub raw request with an SSL handshake timeout. No fresh network result is credited; frozen audit hashes were not changed. |
| Hash frozen source/environment inputs and query immutable Lean/Lake/mathlib identities | 0 | All frozen hashes match; Lean is 4.29.0 at `98dc76e...740`, mathlib is `8a178386...ea95`, tree `bdc39a31...c2b`, and its worktree is clean. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test deliberately absent because the assigned proof phase is blocked. |

## Reopen Condition

Resume after placeholder-free bodies exist for the eleven frozen SAT and Cook-Levin packages, or
after an immutable compatible Lean 4 proof already in the pinned closure can be exact-type checked,
transported to the frozen TM2 encodings, and provenance-audited without changing the dependency
lock. The canonical `flt-regular` checkout must also be repaired outside this worker before the
normal `lake env lean` recipe can replay.

This is current-base nonrelease blocker evidence only. It does not satisfy
`S56-M-0721-PROOF`, change scheduler state, close either terminal package or the root, or claim
audit completion, theorem completion, validation, release, receipt acceptance, or master acceptance.
