# Statement gate blocker

Item: `S56-M-0143-STATEMENT`  
Theorem: `THM-M-0143`  
Verdict: blocked; no exact canonical Lean target is claimed.

## First failed gate

The repository source record gives only the object-family name "Nakajima quiver varieties," the
gloss "construction of moduli spaces of quiver representations," the year 1994, and an untrusted
`verified` label. It does not state a proposition. The intake's bibliographic discovery candidate,
Nakajima's *Instantons on ALE spaces, quiver varieties, and Kac-Moody algebras*, contains multiple
definitions and results, but the repository supplies no fixed edition, page, definition, theorem,
or errata decision selecting one of them.

The missing choices are mathematically material: quiver or graph orientation conventions,
dimension and framing vectors, base field, representation spaces, moment-map parameter, stability
or character, quotient construction, and the conclusion to prove. Possible conclusions such as
nonemptiness, representability, smoothness, a dimension formula, or a representation-theoretic
consequence are inequivalent. Selecting any one would broaden or substitute the metadata rather
than elaborate its exact claim. It could also duplicate the unresolved adjacent target
`THM-M-0142`, which the intake explicitly keeps separate.

Consequently the required ordered binders, hypotheses, conclusion, degenerate cases, canonical
expression and hash, checked transports, and mutation tests cannot truthfully be produced. The
machine state remains `M4`: no exact formal target has been identified. No `sorry`, axiom, opaque
proxy predicate, placeholder theorem, weakened existence wrapper, or convenient substitute was
introduced.

`StatementInfrastructure.lean` checks only the generic combinatorial `Quiver` API available in the
pinned environment. That API assigns arrow types to pairs of vertices; it does not supply Nakajima
representation spaces, moment maps, stability conditions, quotient constructions, or a proposition
about the resulting variety. Its successful elaboration is environment evidence, not statement
credit.

## Environment fingerprint

- Repository base revision: `89c05a4e0beafda9df991a7ef71e7d74f5eb9644`.
- Validation date: 2026-07-12 (Asia/Shanghai).
- Lean toolchain: `leanprover/lean4:v4.29.0`; Lean `4.29.0`, commit
  `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Checked mathlib revision: `8a178386ffc0f5fef0b77738bb5449d50efeea95`.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- Lake manifest SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Validation evidence

Commands ran from this worker clone. Lean commands used only the existing canonical pinned `.lake`
artifacts. No update, build, fetch, or clone command was used.

| Command | Exit | Result |
|---|---:|---|
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0143/StatementInfrastructure.lean` | 0 | `Quiver` and the local generic arrow-family abbreviation elaborated and printed their checked types; no target proposition was declared |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | checked mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | hashes match the environment fingerprint above |
| `rg -n -i 'Nakajima\|quiver variet' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 1 | no matching pinned mathlib source declaration; exit 1 means no matches |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0143` | 0 | rank 318, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `git diff --check -- Stage1_Instances/THM-M-0143` | 0 | no whitespace errors |
| `rg -n '\\b(sorry\|axiom)\\b' Stage1_Instances/THM-M-0143 --glob '*.lean'` | 1 | no forbidden proof constructs found; exit 1 means no matches |

## Retry condition

The authoritative lane must provide an immutable primary-source edition and pinpoint one exact
definition or theorem, including all referenced construction conventions, assumptions, and the
conclusion intended by this repository item. It must also adjudicate the non-duplication boundary
with `THM-M-0142`. A later statement run can then encode that source-faithful claim with minimal
pinned imports, freeze its expression fingerprint, and mutation-test its hypotheses, domains,
binder scopes, and boundary cases.

Until that input exists, statement acceptance and theorem completion are false. Because the
assigned phase cannot be self-tested to its completion gate, no `.stage1-worker-selftest.json` is
emitted.
