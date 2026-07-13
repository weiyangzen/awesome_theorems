# THM-M-1598 rev-5.6 intake

`THM-M-1598` is the catalog item `Diffie-Hellman密钥交换` (Diffie-Hellman key exchange).
The repository attributes it to Diffie and Hellman in 1976, gives only the gloss
`公钥密码学的开创` (the beginning of public-key cryptography), and marks it `已验证`. The gloss
is a historical significance claim, not a truth-valued mathematical proposition with ordered
binders, hypotheses, and a conclusion. The verified label is untrusted metadata and supplies no
source or proof credit.

## Intake result

The target could mean the two parties' algebraic shared-value equality, correctness of a specified
finite-field protocol and key-derivation procedure, passive security under a discrete-log/CDH/DDH
assumption, authenticated security, or correctness of an implementation. Those claims have
materially different domains, adversary models, premises, conclusions, and boundary cases. In
particular, the elementary identity `(g^a)^b = (g^b)^a` is necessary substrate for the familiar
protocol, but selecting it alone would replace key agreement with a weaker algebraic fact.

Diffie and Hellman's 1976 paper *New Directions in Cryptography* is a strong primary-source lead.
It distinguishes public-key cryptosystems from public-key distribution, gives a discrete-
exponentiation construction in Section III, and discusses computational infeasibility rather than
a modern game-based theorem. The catalog does not cite the paper or select one of its claims. The
paper was inspected only to disambiguate the result family; no exact source-to-root proposition,
complete assumption and correction crosswalk, or independent review is admitted.

## Formal boundary

`IntakeProbe.lean` elaborates pinned cyclic-group and repeated-exponentiation APIs. A bounded exact-
topic search found no Diffie-Hellman or key-agreement declaration in repository-local Lean or
pinned mathlib. Generic group powers explain how a future correctness statement might be encoded;
they do not encode a protocol, distribution, adversary, hardness assumption, key derivation, or
security theorem. This probe and search are intake discovery, not the downstream anchor audit.

The canonical human statement and Lean expression remain null. The provisional vector is
`[H5, M4, R4]`: the received gloss is not a stable proposition, no usable exact formal artifact is
credited, and no readable proof can attach to an unidentified root. All six downstream phases
remain open. No exact statement, H0, M0, R0, accepted proof state, audit completion, theorem
completion, accepted receipt, or master acceptance is claimed.
