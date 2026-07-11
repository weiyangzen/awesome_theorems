# Statement gate blocker

Item: `S56-M-0134-STATEMENT`  
Theorem: `THM-M-0134`  
Verdict: blocked; no exact canonical Lean target is claimed.

## First failed gate

The repository source record gives only the label "Burnside-Young theorem," the attribution
W. Burnside/A. Young, the decade "1900s," and the topic "representation theory of symmetric
groups." It supplies no work, edition, theorem number, page, field, range of `n`, hypotheses,
equivalence notion, construction, or conclusion. The label has not been established as a unique
historical theorem name. It therefore does not distinguish the intake candidate classification of
irreducible complex representations by partitions from Young's rule, branching results, character
classification, or another result in the same subject.

Choosing the candidate classification as canonical would invent missing source mathematics. The
ordered binders, hypotheses, conclusion, boundary conventions, expression fingerprint, checked
transports, and mutation tests required by section 5.1 of the rev-5.6 standard consequently cannot
be produced truthfully. The legacy `AwesomeTheorems.Stage1.S1_M_050.StatementShape` is discovery
input only: it selected the partition-classification interpretation without source identification
and is explicitly unaccepted under the uniform L0 rework rule.

`StatementInfrastructure.lean` checks only that the pinned environment can express the candidate
object model: `Nat.Partition n`, `Equiv.Perm (Fin n)`, bundled complex representations,
irreducibility, representation isomorphism, and the quotient by that isomorphism relation. It
deliberately declares no canonical theorem, axiom, proxy proposition, or proof.

## Environment fingerprint

- Repository base revision: `9b87a8f31a5e6a549ab5449871f0b311cab9a6ec`.
- Validation date: 2026-07-12.
- Lean toolchain: `leanprover/lean4:v4.29.0`; Lean `4.29.0`, commit
  `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- mathlib Lake pin and checked revision:
  `8a178386ffc0f5fef0b77738bb5449d50efeea95`.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- Lake manifest SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Validation evidence

Lean commands ran from `Formalizations/Lean` with the existing pinned `.lake` artifacts. No update,
fetch, clone, or build command was used.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-0134/StatementInfrastructure.lean` | 0 | candidate partition/representation/isomorphism-class infrastructure elaborated; four expected `#check` types printed |
| `lake env lean AwesomeTheorems/Stage1/S1_M_050.lean` | 0 | legacy discovery artifact elaborated; this supplies no exact-statement credit |
| `lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C .lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `sha256sum lean-toolchain lake-manifest.json` | 0 | hashes match the environment fingerprint above |
| forbidden-term scan of `StatementInfrastructure.lean` | 1 | no `sorry`, `axiom`, `admit`, or `placeholder` token found; 1 is ripgrep's no-match exit |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0134` | 0 | rank 50, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `git diff --check -- Stage1_Instances/THM-M-0134` | 0 | no whitespace errors |

## Retry condition

The authoritative lane must identify and approve a primary source with a pinpoint theorem statement,
including its field, range of `n`, representation and equivalence conventions, construction, and
exact conclusion. The statement phase can then encode the approved claim with minimal pinned
imports, compare it against or reject the legacy candidate, and execute removed-hypothesis,
changed-domain, binder-scope, and boundary mutations.

Until that source decision exists, the statement gate remains blocked at `M4`; statement acceptance
and theorem completion are false. Because the assigned phase is not genuinely self-tested to its
completion gate, no `.stage1-worker-selftest.json` is emitted.
