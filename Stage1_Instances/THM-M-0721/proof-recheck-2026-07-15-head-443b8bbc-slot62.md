# THM-M-0721 proof recheck at `443b8bbc` (slot62)

Item: `S56-M-0721-PROOF`

Intent: `prove`

Recheck date: `2026-07-15T11:45:51+08:00`

Base revision: `443b8bbc23bf35a1e7a4bb7b3183073f76bbee2b`

Base tree: `c5771c47c12b80aba613e6d844570f83b39ded6d`

## Verdict

`blocked`. No eligible proof body was implemented or found for the exact root
`Stage1Instances.THM_M_0721.ExistsNPCompleteLanguage`. The root remains
`[H1, M3, R4]`, and this proof item remains `[ ]`.

The checked declaration `root_of_candidate_packages` consumes, but does not construct, the two
immediate root packages:

- `M0721-T-SAT-IN-NP`, requiring an encoded SAT language, a correct bundled polynomial-time TM2
  verifier, and a polynomial certificate bound;
- `M0721-T-UNIVERSAL-HARDNESS`, requiring arbitrary-verifier normalization, Cook-Levin tableaux,
  both correctness directions, and a bundled polynomial-time TM2 reduction.

Eleven frozen SAT/Cook-Levin obligations remain open. Pinned mathlib supplies only the TM2
substrate and identity machine. Its relevant composition item is source-level `proof_wanted`, and
Lean confirms that no checked constant was created. The pinned source has no NP-completeness,
SAT-language, or Cook-Levin endpoint. Current repo-local searches also found no terminal package.

The immutable Atlas source still has `sorry` in its tableau correctness, SAT membership, and
polynomial-reduction declarations and uses an incompatible NTM/formula framework. The other frozen
candidates remain supporting-only or placeholder/contract dependent. No candidate is eligible to
pin, import, or transport as proof evidence.

There is no definitional loophole. The alphabet equivalences in `TM2ComputableInPolyTime` rename
individual symbols; they do not implement arbitrary whole-word functions. The identity machine
therefore cannot turn the variable-length `encodePair` verifier input into the one-bit
`encodeBool` output, nor reduce every frozen NP source to one fixed language.

The first failed gate is `M0721-N-SAT-ENCODING`. The remaining immediate root cut is
`M0721-T-SAT-IN-NP` plus `M0721-T-UNIVERSAL-HARDNESS`. Because the assigned proof phase is
incomplete, no proof receipt or `.stage1-worker-selftest.json` is emitted.

## Validation

The automation-provided untracked `Formalizations/Lean/.lake` symlink to canonical pinned artifacts
was reused read-only. No dependency update, build, clone, fetch, checkout, or `.lake` mutation was
performed. The canonical `flt-regular` package directory currently lacks a valid `HEAD`, so the
normal `lake env lean` recipe fails before elaboration. This was recorded rather than repaired;
the narrow target was additionally elaborated using the immutable Lean 4.29.0 binary and existing
precompiled pinned package artifacts.

| Command | Exit | Exact result |
|---|---:|---|
| `git rev-parse HEAD HEAD^{tree}; git status --short --untracked-files=all; readlink Formalizations/Lean/.lake` | 0 | Base `443b8bbc...bee2b`, tree `c5771c47...ded6d`; only the automation-provided `.lake` symlink was initially untracked. |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Passed 15 assurance groups and all 1546 uniform-L0 Lean 4 targets. |
| `python3 scripts/stage1_target.py check` | 0 | Passed 1546 unique targets at ranks 1 through 1546. |
| `python3 scripts/stage1_target.py show THM-M-0721` | 0 | Rank 578; `planned`; L0/rework-required; theorem incomplete. |
| `LEAN_NUM_THREADS=1 timeout 600s python3 Stage1_Instances/THM-M-0721/check_statement.py` | 1 | Lake stopped before elaboration because pinned `flt-regular` has no valid `HEAD`; dependency mutation was prohibited and not attempted. |
| `python3 Stage1_Instances/THM-M-0721/check_obligation_tree.py` | 0 | Passed 18 obligations and 45 typed edges; denominator `375921a1...b92a`; root remained M3 with both terminal packages M4. |
| Assemble `LEAN_PATH` from existing pinned build artifacts, then stream the statement declarations and conditional composition to immutable Lean 4.29.0 with `--trust=0 -t0 --stdin` | 0 | Exact target and conditional composition elaborated; `root_of_candidate_packages` reported exactly `[propext, Quot.sound]` and produced no terminal-package inhabitant. |
| Scan owned Lean files for `sorry`, `admit`, `axiom`, `unsafe`, `proof_wanted`, or `sorryAx` | 1 expected | No prohibited token occurs in the owned Lean files. |
| Scan pinned mathlib Lean source for `IsNPComplete`, `NPcomplete`, `NPComplete`, `CookLevin`, `cook_levin`, or `SATLang` | 1 expected | No eligible NP-completeness, SAT-language, or Cook-Levin endpoint exists. |
| Ask pinned Lean to `#print axioms Turing.TM2ComputableInPolyTime.comp` under the exact import and trust-zero environment | 1 expected | Lean reported `Unknown constant`, confirming that source-level `proof_wanted` added no checked declaration. |
| Search other repo-local Lean source for the exact target, terminal packages, and NP-completeness/Cook-Levin endpoints | 1 expected | No endpoint or implementation exists outside this target dossier. |
| Fetch and hash immutable Atlas `NPCompleteness.lean` at `34ffed396f...fb50` | 0 | SHA-256 matched `4d18245d...008c`; five root-relevant declarations still contain `sorry`. This is blocker discovery only. |
| Run version commands through `lake env` | 1 | Lake hit the unrelated broken `flt-regular` checkout. Direct pinned binaries report Lean 4.29.0 at `98dc76e...740` and Lake 5.0.0; pinned mathlib is `8a178386...ea95`, tree `bdc39a31...c2b`, clean. |

## Reopen Condition

Resume after placeholder-free bodies exist for the eleven frozen SAT and Cook-Levin packages, or
after an immutable compatible Lean 4 proof already in the pinned closure can be exact-type checked,
transported to the frozen TM2 encodings, and provenance-audited without changing the dependency
lock. The canonical `flt-regular` checkout must also be repaired outside this worker before normal
`lake env lean` validation can replay.

This is current-base nonrelease blocker evidence only. It does not satisfy
`S56-M-0721-PROOF`, change scheduler state, close either terminal package or the root, or claim
audit completion, theorem completion, validation, release, receipt acceptance, or master acceptance.
