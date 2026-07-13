# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:6805-6810` supplies the theorem name, Erdős/Ginzburg/Ziv
attribution, year 1961, and the complete gloss `2n-1个整数中存在n个和为n的倍数`. All six uncited
lines originate in repository commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`.
`Docs/Stage0_Blueprint.md:25390-25415` repeats the gloss while leaving exact definitions, premises,
proof route, alternate formulations, axioms, machine state, and artifacts open. Rev-5.6 retains
`已验证` only as untrusted metadata and resets the target to `L0 / rework_required`.

## Primary-source lead

The inspected scan is P. Erdős, A. Ginzburg, and A. Ziv, *Theorem in the additive number theory*,
*Bulletin of the Research Council of Israel*, Section F: Mathematics and Physics, volume 10 F,
number 1 (August 1961), pages 41-43. The authors' archive locator is
`https://www.renyi.hu/~p_erdos/1961-25.pdf`. The observed 236365-byte, two-page PDF has SHA-256
`bae3803dc3e04c41ba10f63c112ba48727dacd1f7c4b1388ec21ff3b084a42b9`.

Scan page 1 states verbatim:

```text
Each set of 2n-1 integers contains some subset of n elements the sum of which is a multiple of n.
```

The proof spans scan pages 1-2. It proves the prime case using a subset-sum lemma and then proves
that validity for `u` and `v` implies validity for `u * v`. It writes occurrences as indexed
integers, selects disjoint blocks, and hence supports the modern sequence or multiset reading even
though the theorem sentence uses "set". It then states an abelian-group extension and says the
nonabelian case was not known.

This supports `H1`, not `H0`: the archive scan and full proof were inspected, but primary-scan
pagination, the incorporated positivity convention, scan transcription, the sole reference,
correction or errata status, and complete premise-to-proof-node mapping have no independent
reviewer receipt.

The issue and page range are secondary bibliographic corroboration from the references in
arXiv:2207.08682, arXiv:2208.07728, and arXiv:math/0305369; those later papers supply no source or
proof credit for this target.

## Component crosswalk

| Repository/source component | Source meaning | Pinned Lean candidate | Intake assessment |
|---|---|---|---|
| `2n-1` integers | exactly that many indexed occurrences | `2 * n - 1 <= Multiset.card s` | candidate is stronger; exact-count specialization open |
| integer domain | arbitrary integers, including repeated and negative values | `s : Multiset Int` | direct domain match after occurrence reading |
| choose `n` | choose exactly `n` input occurrences | `exists t <= s, Multiset.card t = n` | direct container-level match |
| sum multiple of `n` | congruent to zero modulo `n` | `(n : Int) ∣ t.sum` | direct integer conclusion candidate |
| positive modulus | implicit in prime/composite proof | candidate quantifies `n : Nat`, including zero | proposition-changing boundary remains open |
| residue form | implicit modular arithmetic in proof | `t.sum = 0` in `ZMod n` | alternate only after checked transport |
| proof route | elementary prime lemma plus multiplicative closure | Chevalley-Warning prime case plus prime-composite induction | conclusion candidate matches; proof provenance differs |
| abelian extension | separately stated corollary/generalization | not the four probed public roots | excluded as replacement root |
| `已验证` | untrusted catalog label | no receipt | no H or M credit |

## Pinned Lean boundary

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`, the module
`Mathlib.Combinatorics.Additive.ErdosGinzburgZiv` exposes:

```text
Int.erdos_ginzburg_ziv_multiset {n : Nat} (s : Multiset Int)
  (hs : 2 * n - 1 <= s.card) :
  exists t <= s, t.card = n and (n : Int) divides t.sum
```

It also exposes the indexed integer form and corresponding `ZMod n` forms. The pinned file has
SHA-256 `13f8adfc07c9cffd89a0c2a2d3c265348b698fbf724d8b74e6de39434bbc79f7`.
All four public candidates report `propext`, `Classical.choice`, and `Quot.sound` under `#print
axioms`. The feature entered mathlib in commit `07ede5049b7a9e02db2803d6c0f549d983f95fee`
(Yaël Dillies, 2024-07-28), whose message explicitly describes not-necessarily-distinct inputs and
a Chevalley-Warning proof.

`IntakeProbe.lean` establishes candidate availability and justifies `M3` discovery status only.
The statement phase now provisionally freezes the positive exact-count root in
`Stage1Instances.THM_M_0931.ErdosGinzburgZivTarget`, with explicit expression SHA-256
`b872e0de4aedbd0da8825d2c7dd9ecb30e01215131c61e73dc3050776711718a`. Its sole direct import is
`Mathlib.Data.ZMod.Basic`; it deliberately does not import the proof-bearing EGZ module. Checked
wrappers establish the direction from the at-least-count proposition shape to the exact-count root
and an iff between integer divisibility and the same sum cast to zero in `ZMod n`. Four mutations
cover removed positivity, a natural-number input domain, existential modulus scope, and the
at-least-count boundary.

These are worker-self-tested statement identities, not H0 admission or proof credit. The
anchor-audit phase must separately audit terminal bodies, full declaration closure, placeholders,
axioms, trust, license, and external candidates.
