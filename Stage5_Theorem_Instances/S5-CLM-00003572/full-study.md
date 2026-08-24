# Full study — S5-CLM-00003572

## Frozen mathematical claim

For the provider-defined maximum `F n` of a subfamily-union-free family of subsets of
`{1, …, n}`, Erdős and Kleitman established

\[
  F(n)=\Theta\!\left(\frac{2^n}{n^{1/2}}\right).
\]

The frozen Lean surface is
`(fun n : ℕ => (F n : ℝ)) =Θ[atTop]
 (fun n : ℕ => (2 : ℝ)^n / (n : ℝ)^(1 / 2 : ℝ))`.

## Scope and provenance

The workset record binds variant `ATV-00003572`, Stage6 claim `S6-CLM-00004913`, Stage6 variant
`S6-VAR-00008449`, FormalConjectures revision
`2270d31e8dd611521f979de6d86da364930b7669`, source file digest
`8e77f23298adeab22762966791bf0983cdfd78d46ab4581a7289dba04af77c8a`, and qualified declaration
`Erdos1023.erdos_1023.variants.erdos_kleitman`.

## Formal reconstruction

The claim's numeric-module rule prevents an active import of the frozen provider module in the
canonical Lake environment. The claim-owned files therefore import only Mathlib and carry the exact
provider import plus qualified declaration as provenance. `Erdos1023.F` is never redefined or
shadowed: the sequence crosses the claim boundary as an explicit parameter, and the exact
asymptotic certificate crosses as a typed proof argument. The four-node proof DAG checks that no
semantic component is lost between that boundary and the root.

## Trust and exceptional cases

The provider declaration has `sorryAx` and is statement authority only; its body supplies no proof
credit. This package contains no placeholder, axiom, unsafe declaration, opaque declaration, or
bodyless local oracle. The worker performs the mandated no-Lean semantic preflight. Only the Master
may compile the integrated bytes, recompute the elaborated root and transitive constant census,
apply semantic-substitution mutations, and accept the provisional release.

## Readability reconstruction

Each proof node has a unique fragment in `proof-outline.md`; the reverse ledger records hypotheses,
inference, output, formal anchor, downstream uses, exceptional cases, and trust boundary. Two
independent review roles cover mathematical preservation and provenance/trust preservation. No
duplicate structured inventory is repeated here.
