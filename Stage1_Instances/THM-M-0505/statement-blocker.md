# Statement-phase blocker

Item: `S56-M-0505-STATEMENT`  
Theorem: `THM-M-0505`  
Base revision: `aa55669bb59986e08ea8a0d1d77a1e40343d8142`

## Verdict

The exact-statement gate is blocked, so this worker does not create a
`Statement.lean`, expression hash, statement receipt, or worker self-test
manifest.

The only repository statement is `ζ函数的显式公式` ("an explicit formula for
the zeta function"). The repository also supplies the title "Weil explicit
formula", an attribution to Andre Weil, and the year 1952. These data identify
a family of explicit formulae but do not select a proposition. In particular,
they do not determine:

1. the pinpoint formula or theorem in a fixed primary-source edition;
2. the test-function space and its regularity, support, decay, or symmetry;
3. the Fourier/Mellin transform sign and scaling conventions;
4. the encoding, multiplicities, and limiting prescription for zeta zeros;
5. the prime-power weights and endpoint convention;
6. the pole, trivial-zero, Gamma-factor, and archimedean terms; or
7. whether the claim is a distributional identity or an equality of separately
   convergent sums and integrals.

Choosing any of these data here would broaden or substitute the source claim.
The nearby `THM-M-0498` Chebyshev-psi formula is explicitly excluded by this
dossier unless a checked source equivalence is supplied. An opaque predicate,
a structure field containing the desired equality, or a theorem assuming that
equality would elaborate but would not be the requested theorem.

## Smallest real validation

The existing pinned Lake environment was reused through the worker clone's
`.lake` symlink. No dependency update, clone, fetch, or build was run.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0505` | 0 | rank 879; planned; L0/rework-required; legacy artifacts unaccepted; theorem incomplete |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0505/IntakeProbe.lean)` | 0 | Lean 4.29.0 elaborated the relevant ingredient APIs only |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `rg -n -i 'Weil.*explicit\|explicit.*Weil\|formules explicites' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 1 | no matching pinned-mathlib declaration or source text |
| `sha256sum Docs/researches/math_theorems.md Stage1_Instances/THM-M-0505/source-statement-crosswalk.md Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | hashes: `bdde11...a29`, `7b5f80...25a8`, `651c8a...b1d2`, `321626...2d81` |
| `git diff --check -- Stage1_Instances/THM-M-0505` | 0 | no pre-existing whitespace errors in the owned path |

The intake probe proves only that `riemannZeta`, von Mangoldt, Fourier,
integral, Gamma, and summability APIs exist. It is not an exact-statement
elaboration.

## Retry condition

Attach an immutable primary-source scan (including edition identity and
content hash), a pinpoint page/formula, the complete surrounding hypotheses,
and an errata decision. Then freeze the source-normalized identity and encode
it directly in Lean with minimal imports, a checked expanded-form transport,
an explicit-expression fingerprint, and the four rev-5.6 mutations (removed
hypothesis, changed domain, changed binder scope, and boundary case).

Until that evidence exists, the first failed gate is section 5's exact
canonical-claim requirement, before Lean statement elaboration. The root
remains `[H2, M4, R3]`; `statement_elaborated=false`, `audit_complete=false`,
and `theorem_complete=false`.
