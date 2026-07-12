# Exact-statement gate: blocked

Item: `S56-M-0558-STATEMENT`  
Theorem: `THM-M-0558`  
Base revision: `60aae17521cd359d0473812b6927789cb4fee9e6`

## Decision

The selected human root is sufficiently specific to reject weaker substitutes, but the exact Lean
4 target cannot be expressed in the pinned environment. The root requires both lower **reduced**
integral homology and the **canonical Hurewicz homomorphism** from `pi_n(X, x)` to integral singular
homology. Pinned mathlib provides higher homotopy groups and ordinary singular homology as separate
APIs, but it provides neither a reduced singular-homology object nor the canonical comparison map.

A proposition quantifying an arbitrary map between the two groups would not say that the Hurewicz
map is an isomorphism. Assuming a map or an isomorphism as structure data would assume the desired
conclusion. Replacing reduced homology below `n` by ordinary homology also changes the degree-zero
boundary. Defining the missing comparison and reduced theory locally would be mathematical proof
infrastructure, not statement elaboration, and cannot be done faithfully without first freezing its
construction and proving that it is the canonical map. All of these shortcuts are forbidden
substitutions.

The intake also leaves source-sensitive space hypotheses open (arbitrary pointed space versus a
CW-type or local-niceness assumption). Adding a CW hypothesis merely to obtain an implementable
target would strengthen the premises; omitting a hypothesis required by the selected exact source
would broaden the theorem. Thus source review remains an independent statement-identity blocker
even if the missing Lean infrastructure is later added.

No canonical declaration, elaborated expression hash, alternate-encoding transport, or meaningful
four-class mutation suite can therefore be produced. Machine status remains `M4`; no proof, audit
completion, or theorem completion is claimed.

## Lean boundary checked

`StatementProbe.lean` uses only the closest pinned substrate imports:

```lean
import Mathlib.Topology.Homotopy.HomotopyGroup
import Mathlib.AlgebraicTopology.SingularHomology.Basic
import Mathlib.Algebra.Category.ModuleCat.Abelian
import Mathlib.Algebra.Category.ModuleCat.Colimits
```

It elaborates `HomotopyGroup.Pi`, notation `pi_ n X x`, the singular chain and homology functors,
and the ordinary integral singular-homology specialization. Repository-wide source searches found
the word `Hurewicz` only in the unrelated sense of Hurewicz fibrations, and found no reduced
singular-homology definition. These negative searches are bounded evidence about pinned mathlib,
not a global impossibility claim. The probe is not the canonical theorem and receives no statement
or proof credit.

The environment was Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, with mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. Existing canonical `.lake` artifacts were used
read-only; no update, build, clone, or fetch was performed.

## Validation record

Commands ran in this worker clone on 2026-07-12 (Asia/Shanghai).

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups; 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546 |
| `python3 scripts/stage1_target.py show THM-M-0558` | 0 | rank 606, planned, L0/rework-required, theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `cd Formalizations/Lean && lake --version` | 0 | Lake `5.0.0-src+98dc76e` |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | hashes recorded in `statement-blocker.json` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | mathlib pin `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| scoped pinned-mathlib `rg` searches for Hurewicz and reduced-homology APIs | 0/1 | unrelated Hurewicz-fibration match; no reduced-homology definition |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0558/StatementProbe.lean` | 0 | all five substrate checks elaborated |
| `python3 -m json.tool Stage1_Instances/THM-M-0558/statement-blocker.json` | 0 | valid JSON |
| `git diff --check -- Stage1_Instances/THM-M-0558` | 0 | no output |

## Retry condition

First, an accountable source review must freeze the exact space hypotheses and conventions against
an immutable edition and pinpoint. Then pinned Lean infrastructure must define reduced integral
singular homology and construct the canonical Hurewicz homomorphism from mathlib's homotopy groups,
with checked functoriality and comparison properties. Only then can a later statement run elaborate
the exact conjunction, serialize its expression/environment, check alternate transports, and run
the required hypothesis, domain, binder-scope, and boundary mutations.

The assigned phase is not genuinely self-tested to completion, so no
`.stage1-worker-selftest.json` is emitted.
