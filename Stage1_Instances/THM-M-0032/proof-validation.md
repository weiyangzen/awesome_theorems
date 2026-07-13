# THM-M-0032 proof-phase attempt

Item: `S56-M-0032-PROOF`  
Date: `2026-07-13T08:04:13+08:00`  
Base revision: `c76fe0f1a7514b41f191d16840eff25e64ee9d17`

## Verdict

`blocked`: no eligible proof body for the exact unrestricted Auslander-Buchsbaum UFD target exists
in the repository or pinned dependency closure. The immediate machine cut remains
`M0032-N-DOMAIN` and `M0032-A-PRIME-ELEMENT`. Pinned mathlib cannot derive `IsDomain R` from
`[CommRing R] [IsRegularLocalRing R]`, and it has no proof that every nonzero prime ideal in such a
ring contains a prime element.

The frozen expansion shows why the second package is substantive. It needs the theorem that every
height-one prime of a regular local ring is principal, with dimension-zero and positive-dimension
branches, a regular parameter and quotient, localization and dimension decrease, invertible-ideal
trivialization, denominator clearing, atomic factorization, and a primality lift. None of those
theorem-specific terminal bodies exists in the pinned environment.

`ObligationTree.lean` does contain real checked bodies for the generic Kaplansky criterion and for
conditional root composition. The latter consumes `RegularLocalDomainPackage` and
`RegularLocalPrimeElementPackage` as premises; it constructs neither. Returning it as the result
would substitute a conditional theorem for the canonical target.

The prerequisite anchor inventory found no usable external terminal. Atlas has two strengthened
declarations with an added `[IsDomain R]`, both ending in `by sorry`. The older
`JarodAlper/RegularLocalRings` project supplies partial domain and dimension-one infrastructure for
an incompatible regular-local class/toolchain, but no unrestricted UFD theorem. Thus no source was
added: any short local declaration of the missing packages would be an axiom, bodyless declaration,
unproved premise, or other placeholder.

Root debt remains `[H1, M3, R4]`, `root_closed=false`, and `theorem_complete=false`. Because the
assigned proof deliverable is incomplete, `.stage1-worker-selftest.json` is deliberately absent.

## Narrow validation evidence

All commands ran in this worker clone and reused the existing canonical pinned Lake artifacts. No
`lake update`, `lake build`, dependency clone/fetch, or `.lake` mutation was performed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0032` | 0 | Rank 1076; planned; L0/rework-required; theorem incomplete. |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0032/Statement.lean` | 0 | The exact canonical target elaborated. All four intentional mutation failures were rejected, and the binder transport reported only `propext`, `Classical.choice`, and `Quot.sound`. |
| Run the isolated elaboration recipe below | 0 | The generic Kaplansky wrapper and conditional root composition elaborated. Each reported only `propext`, `Classical.choice`, and `Quot.sound`; the temporary directory was removed. |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0032/AnchorAudit.lean` | 0 | The pinned interfaces elaborated; the intentional `#check_failure` confirmed that `UniqueFactorizationMonoid R` cannot be synthesized from `CommRing R` and `IsRegularLocalRing R`. |
| `rg -n -i 'IsRegularLocalRing\|regularLocalRing_isUFD\|auslander_buchsbaum_UFD\|UniqueFactorizationMonoid.*regular\|regular.*UniqueFactorizationMonoid' --glob '*.lean' Stage1_Instances Formalizations/Lean/AwesomeTheorems Formalizations/Lean/.lake/packages/mathlib/Mathlib` | 0 | Local hits were limited to this dossier and pinned `RegularLocalRing/Defs.lean`; no terminal proof body was found. |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release. |
| `sha256sum` on `Statement.lean`, `ObligationTree.lean`, `obligation-registry.json`, and `anchor-audit.json` | 0 | `5391ab5c...3a`; `9c54c27a...17e8`; `29620e59...e18`; `76df6db9...ade1`. |
| `python3 -m json.tool Stage1_Instances/THM-M-0032/proof-blocker.json >/dev/null` | 0 | The blocker record is valid JSON. |
| `git diff --check -- Stage1_Instances/THM-M-0032` | 0 | No whitespace errors. |

Exact isolated elaboration recipe, run from the repository root:

```bash
set -euo pipefail
repo_root=$PWD
lean_root=$repo_root/Formalizations/Lean
target=$repo_root/Stage1_Instances/THM-M-0032
tmp=$(mktemp -d /tmp/thm-m-0032-proof-attempt.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
lean=$(cd "$lean_root" && lake env which lean)
lean_path=$(cd "$lean_root" && lake env printenv LEAN_PATH)
cd "$target"
LEAN_PATH="$lean_path" "$lean" -o "$tmp/Statement.olean" Statement.lean
LEAN_PATH="$tmp:$lean_path" "$lean" ObligationTree.lean
```

The pre-existing untracked `Formalizations/Lean/.lake` entry is the automation-provided symlink to
the canonical pinned artifacts and was not modified. `check_obligation_tree.py` was not used as
proof evidence because it validates the prior worker's root self-test manifest, which is correctly
absent for this blocked proof attempt; the frozen Lean composition was elaborated directly instead.

## Reopen condition

Resume only after placeholder-free implementations of `M0032-N-DOMAIN` and
`M0032-A-PRIME-ELEMENT` with their frozen dependencies, or discovery of an immutable compatible
Lean 4 terminal proof that can be pinned, transported to the exact type, and validated without
changing the dependency lock.
