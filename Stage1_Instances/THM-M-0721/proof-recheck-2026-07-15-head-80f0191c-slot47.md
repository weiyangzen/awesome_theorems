# THM-M-0721 proof recheck at `80f0191c` (slot47)

Item: `S56-M-0721-PROOF`

Intent: `prove`

Recheck date: `2026-07-15T15:28:29+08:00`

Base revision: `80f0191c83a1bb4026c2d490be957cf109464de1`

Base tree: `b89a01cfc623bf97d1896fb3534a1ac24381fa71`

## Verdict

`blocked`. No eligible proof body was implemented or found for the exact root
`Stage1Instances.THM_M_0721.ExistsNPCompleteLanguage`. The root remains
`[H1, M3, R4]`, and this proof item remains `[ ]`.

The checked `root_of_candidate_packages` declaration is conditional composition only. It consumes,
but does not construct, the immediate root cut:

- `M0721-T-SAT-IN-NP`: faithful binary SAT encoding, verifier correctness, certificate bound, and
  a bundled polynomial-time TM2 verifier;
- `M0721-T-UNIVERSAL-HARDNESS`: arbitrary-verifier normalization, Cook-Levin tableaux, both
  correctness directions, and a bundled polynomial-time TM2 reduction for every frozen `InNP`
  source.

Eleven frozen SAT and Cook-Levin obligations remain open. Their registry entries have planned prose
targets rather than exact Lean declaration types; the only exact open interfaces are
`CandidateMembership candidate` and `CandidateHardness candidate`. Concrete leaf declarations need
an append-only registry refinement before they can receive proof credit.

Pinned mathlib supplies the TM2 substrate and identity implementation, but no NP-completeness
endpoint. Its source-level `TM2ComputableInPolyTime.comp` is `proof_wanted`, and trust-zero Lean
confirms that no checked constant exists. Scoped repo and pinned-mathlib searches found no exact
root or terminal-package implementation. Immutable candidate replay reconfirmed one
supporting-only candidate and two headline endpoints with proof gaps or incompatible contracts;
none transports to the frozen Bool-word TM2 target.

Empty, universal, identity, constant, classical-choice, fixed-source, and conditional shortcuts do
not construct the universally quantified polynomial-time reductions. The first failed gate is
`M0721-N-SAT-ENCODING`. Because the positive proof phase is incomplete, no proof receipt or
`.stage1-worker-selftest.json` is emitted.

## Validation

The automation-provided untracked `Formalizations/Lean/.lake` symlink to canonical pinned artifacts
was reused read-only. No dependency update, build, clone, fetch, checkout, or `.lake` mutation was
performed.

| Command | Exit | Exact result |
|---|---:|---|
| `git rev-parse HEAD HEAD^{tree}; git status --short --untracked-files=all; readlink Formalizations/Lean/.lake` | 0 | Base `80f0191c...64de1`, tree `b89a01cf...fa71`; only the automation-provided `.lake` symlink was initially untracked. |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Passed 15 assurance groups, 41 legacy rows, 300 legacy slots, and all 1546 uniform-L0 Lean 4 targets. |
| `python3 scripts/stage1_target.py check` | 0 | Passed 1546 unique targets at ranks 1 through 1546; all are L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-0721` | 0 | Rank 578; `planned`; L0/rework-required; legacy artifacts unaccepted; theorem incomplete. |
| `LEAN_NUM_THREADS=1 timeout 600s python3 Stage1_Instances/THM-M-0721/check_statement.py` | 0 | Expression hash `758b1033...b204` matched; all four weakened mutations were distinguished. |
| `python3 Stage1_Instances/THM-M-0721/check_obligation_tree.py` | 0 | Passed 18 obligations and 45 typed edges; denominator `375921a1...b92a`; root remained M3 and both terminal packages M4. |
| From `Formalizations/Lean`, stream exact statement and composition declarations to `LEAN_NUM_THREADS=1 timeout 180s lake env lean --trust=0 -t0 --stdin` | 0 | Exact statement and conditional composition elaborated; `root_of_candidate_packages` reported `[propext, Quot.sound]` and supplied no terminal package. |
| Scan owned Lean files for prohibited proof-device command tokens | 1 expected | No placeholder, bodyless-declaration, unsafe, or open-proof command token occurs in owned Lean files. |
| Search repo-local and pinned-mathlib Lean for exact root/package and NP-completeness endpoints | 1 expected | No eligible endpoint or terminal-package implementation exists outside this dossier. |
| Ask trust-zero Lean to print axioms for `Turing.TM2ComputableInPolyTime.comp` | 1 expected | Lean reported `Unknown constant`; source-level `proof_wanted` added no checked declaration. |
| `timeout 60s python3 Stage1_Instances/THM-M-0721/check_anchor_audit.py` | 0 | Local pins/hashes and all three immutable external candidates matched; root classification remained M2. |
| Inspect Lean/Lake/mathlib/flt-regular identities and hash frozen inputs | 0 | Lean 4.29.0 at `98dc76e...740`, Lake 5.0.0, mathlib `8a178386...ea95` tree `bdc39a31...c2b`, and flt-regular `56161b6e...1a27` tree `32c9eace...c893`; all target/environment hashes matched. |
| Inspect `validation-specs.json` recipe keys against blueprint section 10.5 | 0 | Legacy shell-string recipes lack the normative structured `cwd`, `argv`, environment, timeout, expected-output, obligation-list, and declaration-list fields. |

## Reopen Condition

Resume after exact leaf signatures are append-only refined and placeholder-free bodies exist for
the eleven SAT and Cook-Levin packages, or after an immutable compatible Lean 4 proof already in the
pinned closure can be exact-type checked, transported to the frozen TM2 encodings, and
provenance-audited without changing the dependency lock.

This is current-base, warm-cache, nonrelease blocker evidence only. It does not satisfy
`S56-M-0721-PROOF`, change scheduler state, close either terminal package or the root, or claim
audit completion, theorem completion, validation, release, receipt acceptance, or master acceptance.
