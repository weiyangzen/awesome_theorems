# Anchor-audit validation record

Item: `S56-M-0498-ANCHOR_AUDIT`  
Base revision: `01e0cab0efda724de1660ee854e9a38cebf1e0ab`

## Result

The exact repo-local candidate is only the proposition
`Stage1Instances.THM_M_0498.RiemannVonMangoldtTarget`. Pinned mathlib at
`8a178386ffc0f5fef0b77738bb5449d50efeea95` provides `Chebyshev.psi`, its
prime-power decomposition, a transfer between theta and prime counting, the
von Mangoldt logarithmic-derivative identity, the zeta Euler product, its pole
at one, and its trivial zeros. The nine retained declarations elaborate in
`AnchorAudit.lean`, but none states the canonical limit over nontrivial zeros.

The closest credible external Lean 4 source found was
`AlexKontorovich/PrimeNumberTheoremAnd@baff9f946bcb5349d35b3eba72e28031748e6388`.
Its `BKLNW_app.bklnw_eq_A_7` is a truncated psi formula with an error bound,
not the exact limiting equality, and its proof is incomplete. Its declaration
named `Riemann_vonMangoldt_bound` instead concerns the homonymous zero-counting
function `N(T)`. Immutable raw-source URLs were content-hashed; the project was
not fetched, installed, or treated as local closure. Its declared toolchain is
Lean 4.28.0, while this repository is pinned to Lean 4.29.0.

The root therefore remains `M4`: no eligible exact proof body is available to
integrate. This is a completed bounded audit, not theorem completion and not a
claim that no proof exists anywhere.

## Commands and results

Commands ran on 2026-07-12 inside this worker clone. No Lake dependency was
updated, fetched, cloned, or built.

| Command | Exit | Result |
|---|---:|---|
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0498/AnchorAudit.lean` | 0 | nine pinned mathlib declarations elaborated |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0498/Statement.lean` | 0 | exact statement and definitional expanded transport re-elaborated |
| `python3 Stage1_Instances/THM-M-0498/check_anchor_audit.py` | 0 | audit boundary, nine probes, manifest pin, and installed mathlib HEAD agreed |
| `rg -n -i 'Riemann.?von.?Mangoldt\|explicit formula.{0,100}(prime\|psi\|zeta\|zero)\|nontrivial zeros.{0,100}(psi\|prime\|formula)' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 1 | no terminal-name/content match in pinned mathlib source |
| immutable `curl` reads of the external toolchain, manifest, license, and seven relevant Lean files, followed by `sha256sum` and `rg` | 0 | Lean 4.28.0; Apache-2.0; exact hashes recorded in `anchor-audit.json`; closest explicit-formula body is incomplete |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | standard passed for 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0498` | 0 | rank 258; planned; legacy artifacts unaccepted; theorem incomplete |
| `git diff --check -- Stage1_Instances/THM-M-0498` | 0 | no whitespace errors |

## Open integration gate

An integration attempt requires an immutable repository revision, compatible
toolchain and dependency graph, an exact normalized declaration type, and a
complete eligible proof body. It must then pass local wrapper, declaration
dependency, proof-device, axiom, unsafe/oracle, and license checks. No `M0-P`,
`M1`, or theorem-completion credit is valid before those checks succeed.
