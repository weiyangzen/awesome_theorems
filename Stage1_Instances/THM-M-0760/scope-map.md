# Scope map

## Preserved repository scope

The repository fixes target `THM-M-0760`, the title Myhill-Nerode theorem, the attribution John
Myhill / Anil Nerode, the year 1958, and the broad claim "a characterization of regular languages."
The separate computer-science source row says "minimal DFA and distinguishable strings." The
importance and `已验证` fields are inventory metadata, not human-source or kernel evidence.

The shared core of the conventional formulations is this. For a language `L` over words, two
prefixes `x` and `y` are Nerode-equivalent when no suffix distinguishes them:
`forall z, x ++ z in L iff y ++ z in L`. A language is regular exactly when this equivalence has
finitely many classes. Equivalently, only finitely many residual/left-quotient languages
`{z | x ++ z in L}` occur. The number of equivalence classes is also conventionally related to the
minimum number of states in a recognizing DFA, but that stronger cardinality conclusion is not
forced by the math-catalog gloss.

## Proposition-changing decisions

The statement phase must obtain accountable source approval and freeze all of the following:

1. Whether the canonical root is only regularity iff finite Nerode index, or also includes the
   minimum-state cardinality theorem and existence/uniqueness properties of a minimal DFA.
2. Whether the alphabet is an arbitrary type, as in the pinned mathlib theorem, or is assumed finite
   as in many textbook formulations. Finiteness of the quotient index must not be confused with
   finiteness of the alphabet or of the word set.
3. Whether Nerode classes are encoded as a quotient/setoid, as the range of the residual map, or as
   pairwise distinguishable functions, and the exact checked relationship between those encodings.
4. The append orientation: `x` is the already-read prefix and `z` is appended on the right. The
   residual is called a left quotient because the prefix is removed from the left.
5. Whether "right congruence" means a right-invariant equivalence only. The usual Nerode relation is
   generally not a two-sided monoid congruence and must not be conflated with syntactic congruence.
6. Whether a state-count statement counts only reachable states, all states of an arbitrary DFA,
   or states of a chosen minimal accessible DFA, including the exact finite-cardinality encoding.
7. Ordered universes and binders, equality/extensionality conventions, any decidability or
   nonemptiness assumptions, and every boundary case below.

These choices are a resolution ledger, not a theorem claim.

## Pinned candidate boundary

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, module
`Mathlib.Computability.MyhillNerode` supplies the candidate

```text
{alpha : Type u} {L : Language alpha} :
  L.IsRegular <-> (Set.range L.leftQuotient).Finite
```

Here `Language alpha` is `Set (List alpha)`, `L.leftQuotient x` contains exactly the suffixes `y`
with `x ++ y` in `L`, and `L.IsRegular` means that some DFA with a finite state type accepts exactly
`L`. The range of `leftQuotient` is therefore extensionally the collection of Nerode classes. This
is an exact-looking formal candidate, but intake does not yet credit it as the canonical expression
or its existing proof body.

## Explicit exclusions and neighbors

- The syntactic two-sided congruence and syntactic monoid are not substituted for Nerode's
  right-invariant equivalence without a checked bridge.
- DFA minimization algorithms, Hopcroft's complexity bound, NFA-to-DFA determinization, pumping
  lemmas, closure properties, and regular-expression equivalence are neighboring results, not this
  root.
- The separate Stage0 computer-science record `THM-C-0134` is provenance evidence only. It cannot
  transfer a statement, proof, or accepted state into `THM-M-0760`.
- A theorem that assumes a finite quotient, a recognizing DFA, or the desired equivalence cannot be
  presented as a proof of the characterization.
- The untrusted catalog label `已验证` and mathlib's theorem name do not by themselves establish
  canonical-statement identity or H0/M0 status.

## Boundary cases

The pinned candidate includes arbitrary alphabets, including empty and singleton alphabets; empty,
universal, finite, and infinite languages; the empty word; and languages with zero, one, or many
distinct residuals as permitted by their definitions. A DFA has a start state, so any recognizing
state type is inhabited. No `Finite alpha`, `Fintype alpha`, decidable-equality, or nonempty-alphabet
hypothesis appears in the candidate.

If the selected source instead assumes a finite alphabet or includes a minimum-state claim, the
later statement must expose that premise/conclusion rather than treating the difference as
notation. Checked transports must cover quotient-versus-range identity, and mutations must include
alphabet domain, append orientation/binder scope, the finiteness conclusion, and empty-word or
empty-alphabet behavior.
