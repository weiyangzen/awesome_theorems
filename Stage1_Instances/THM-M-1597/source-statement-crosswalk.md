# Source-statement crosswalk

## Repository record

| Repository field | Exact content | Intake interpretation |
|---|---|---|
| title | `RSA加密` | names a cryptosystem family, not a proposition |
| attribution | `Rivest/Shamir/Adleman` | bibliographic lead only |
| year | `1977` | historical metadata; the journal article appeared in 1978 |
| statement gloss | `公钥加密系统` | purpose/object description with no binders, hypotheses, or conclusion |
| status | `已验证` | untrusted catalog metadata; no H/M/R credit |

`Docs/Stage0_Blueprint.md` repeats these fields and explicitly leaves the exact definitions and
premises, proof route, dependencies, equivalent forms, axioms, machine status, and artifact links
unresolved. The catalog therefore cannot determine a canonical source or Lean statement.

## Primary-source lead inspected but not admitted as H0

R. L. Rivest, A. Shamir, and L. Adleman, *A Method for Obtaining Digital Signatures and Public-Key
Cryptosystems*, *Communications of the ACM* 21(2), 1978, pages 120-126,
DOI `10.1145/359340.359342`. An author-hosted electronic reprint was inspected on 2026-07-13
(`https://people.csail.mit.edu/rivest/Rsapaper.pdf`, 182059 bytes, SHA-256
`f7b1f78d9a7cbeb85e32b8c563a6db60771a5cc4bdc55580645f7cb778a4966b`). The PDF is external
discovery input and was not added to the repository.

The paper contains more than one possible root:

| Source locus | Source claim or role | Prospective formal surface | Unresolved boundary |
|---|---|---|---|
| Section II, equations (1)-(2) | `D(E(M)) = M` and `E(D(M)) = M` as public-key-system properties | two inverse laws for selected maps and a selected message type | generic specification or RSA theorem; equality carrier and domain |
| Section V | `n = p*q`; encrypt by `M^e mod n`; decrypt by `C^d mod n`; `e*d` is `1` modulo `(p-1)(q-1)` | definitions and key-validity hypotheses | prime distinctness, representatives, reductions, and exponent order |
| Section VI, equations (3)-(5) | Euler/Fermat and the totient calculation | modular exponent and totient lemmas | the displayed totient product needs distinct/coprime primes |
| Section VI conclusion | for all `0 <= M < n`, `M^(e*d)` is congruent to `M` modulo `n`; hence `E` and `D` are inverse permutations | candidate all-message correctness theorem and checked definitions-to-conclusion bridge | exact binders, two directions, natural equality versus `ZMod`, errata/correction review |
| Section VII | algorithms and operation-count/practicality statements | executable algorithm plus a formal cost relation | machine model, bit complexity, constants, and historical estimates |
| Section IX | security discussion | possible computational reduction or security experiment | the paper explicitly says general security was not proved; no modern security theorem may be inferred |

The statement phase may naturally propose the Section VI all-message round-trip theorem, but intake
does not authorize that redirection. A source-faithful candidate would quantify `p q e d M`, assume
prime and distinct `p q`, the exact exponent congruence, and the canonical message range, then prove
the relevant nested modular exponentiation equals `M` in both selected directions. It must not add a
coprimality assumption on `M`, because Section VI explicitly handles divisibility by either prime.

## Known correction and review debt

The paper says "two primes" while using `phi(p*q) = phi(p)*phi(q)` and recombination modulo `p*q`.
Those steps require `p != q` (equivalently coprime primes). Omitting the condition makes the obvious
formal reading false. This correction must be sourced or independently adjudicated before H0, and
the selected edition, page mapping, errata history, assumptions, and conclusion require independent
review. The catalog-to-paper relationship is not itself cited by the repository.

## Adjacent formal APIs, not proof anchors

Pinned mathlib provides `Nat.ModEq`, `Nat.ModEq.pow`, `Nat.ModEq.pow_totient`,
`Nat.pow_add_mul_totient_mod_eq`, `Nat.totient_mul`, `Nat.totient_prime`,
`Nat.modEq_and_modEq_iff_modEq_mul`, and `ZMod.chineseRemainder`. These APIs could support a future
correctness proof. The totient exponent lemmas assume the base is coprime to the modulus, so they do
not alone establish the all-message conclusion. No exact RSA declaration or terminal proof body is
credited at intake.

## Crosswalk verdict

The repository-to-source mapping is unresolved because the repository identifies a system, while
the paper contains multiple correctness, construction, algorithmic, signature, and security
surfaces. Provisional `H5` means this received target is not yet a stable proposition; it does not
claim the standard RSA correctness theorem is false. H0, a canonical Lean expression, machine
closure, and readable proof reconstruction remain open.
