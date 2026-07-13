# THM-M-1597 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the catalog label `RSA加密`
(`RSA encryption`). The repository supplies only the gloss `公钥加密系统` ("public-key encryption
system"), attributes it to Rivest, Shamir, and Adleman in 1977, and attaches an untrusted `已验证`
label. A cryptosystem name and purpose do not form a truth-valued proposition with ordered binders,
hypotheses, and a conclusion.

## Intake result

The Rivest-Shamir-Adleman paper was inspected as a primary-source lead. It describes several
materially different claims: construction of public and private exponentiation maps, their
round-trip correctness, signature use, efficient algorithms, and security arguments. Section VI
proves that the encryption and decryption maps are inverse permutations for the paper's key
conditions and message range. Section IX separately says that security was not proved. The catalog
does not select the Section VI result, a security claim, an efficiency claim, or any conjunction as
its root.

This intake preserves that ambiguity. It does not silently substitute textbook RSA correctness,
Euler's theorem for messages coprime to the modulus, a factoring-hardness claim, modern padded RSA,
or the separate catalog record `THM-C-0201` (RSA correctness). The statement phase must receive an
accountable redirection to one immutable proposition and crosswalk every key, message, modular,
correctness, security, and boundary convention.

## Formal boundary

`IntakeProbe.lean` checks only pinned modular congruence, totient, and Chinese-remainder APIs adjacent
to a possible correctness proof. The coprime-base totient lemmas do not by themselves prove the
paper's all-message result. A bounded repository and pinned-mathlib search found no exact RSA
declaration. These observations are discovery evidence only, not an exhaustive anchor audit or a
proof body.

The provisional root vector is `[H5, M4, R4]`. `H5` classifies the received system gloss as not yet
a stable proposition; it does not refute RSA correctness. No usable exact formal artifact is
credited, and no source-faithful reconstruction can attach to an unfrozen root. All six downstream
tasks remain open. No canonical statement, H0, M0, R0, accepted proof state, audit completion,
theorem completion, or master acceptance is claimed.
