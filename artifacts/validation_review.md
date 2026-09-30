# Additional question checks

These checks were reviewed by the coding assistant against the corpus, not by
an independent human judge. They are separate from the fixed 20-case benchmark.

The six questions in `validation_questions.json` were created after freezing
prompt 1.9. Answers are preserved in `validation_answers.json`.

| Case | Required behavior | Observed result |
|---|---|---|
| V01 | Decline medical advice and describe support scope | Correct refusal and supported topics |
| V02 | List repair intake fields and authorization | Serial, contact, symptoms, proof and authorization included |
| V03 | Secure account and cancel Confirmed order | Trusted device, password, sessions, MFA, Account Security and account-page cancellation included |
| V04 | Use old return policy; count days from delivery | Correct 21-day policy, but delivery start omitted |
| V05 | Split refund by payment method and give processing period | Correct replacement gift card, original methods and five to seven business days after inspection |
| V06 | Apply severe-weather exception to express fee | Correct refusal to refund and governing exception |

V04 exposed a missing rule in retrieval. Prompt version 1.10 retains the answer
instructions from 1.9 and adds retrieval query terms for the triggering event,
policy version and confirmed delivery. Both `OT-09-P03` and `OT-09-P04` are now
retrieved for date-dependent return-policy questions.

`validation_followup_answers.json` records a rerun of V04 and a new date variant
V07. Both answers correctly select version 1.0, give 21 calendar days and count
the window from confirmed delivery. V04 was used to fix the system, so it is
no longer an untouched validation case. This small check does not establish
performance on arbitrary new questions.
