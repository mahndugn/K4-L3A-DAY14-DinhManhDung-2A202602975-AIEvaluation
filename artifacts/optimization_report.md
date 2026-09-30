# Optimization results

Highest measured result: **18/20 (90%)**, obtained in both v11 and its independent repeat.
The default artifacts are the latest complete repeat, using prompt 1.10.
Every run uses Gemini gemini-3.5-flash-lite and the same 20 golden questions.
Required metrics, thresholds and golden references were unchanged during this optimization.

| Run | Prompt | Temperature | Passed | Faithfulness | Relevance | Completeness | Context Recall | Context Precision |
|---|---|---|---:|---:|---:|---:|---:|---:|
| baseline | 1.0 | provider default | 12/20 | 0.717 | 0.594 | 0.626 | 0.831 | 0.939 |
| v2 | 1.1 | provider default | 11/20 | 0.678 | 0.573 | 0.714 | 0.857 | 0.939 |
| v3 | 1.2 | provider default | 12/20 | 0.712 | 0.597 | 0.728 | 0.857 | 0.939 |
| v4 | 1.3 | provider default | 13/20 | 0.783 | 0.543 | 0.745 | 0.857 | 0.939 |
| v5 | 1.4 | provider default | 9/20 | 0.781 | 0.465 | 0.673 | 0.857 | 0.939 |
| v6 | 1.5 | 0 | 12/20 | 0.626 | 0.627 | 0.755 | 0.857 | 0.939 |
| v7 | 1.6 | 0 | 15/20 | 0.712 | 0.594 | 0.742 | 0.862 | 0.966 |
| v8 | 1.7 | 0 | 15/20 | 0.786 | 0.623 | 0.774 | 0.867 | 0.962 |
| v9 | 1.8 | 0 | 15/20 | 0.764 | 0.628 | 0.746 | 0.867 | 0.962 |
| v10 | 1.9 | 0 | 16/20 | 0.754 | 0.623 | 0.746 | 0.867 | 0.962 |
| v11 | 1.10 | 0 | 18/20 | 0.780 | 0.652 | 0.769 | 0.871 | 0.962 |
| v10_repeat1 | 1.9 | 0 | 16/20 | 0.760 | 0.668 | 0.742 | 0.867 | 0.962 |
| v11_repeat1 | 1.10 | 0 | 18/20 | 0.781 | 0.647 | 0.770 | 0.871 | 0.962 |

## Changes

- Retrieved scope policy for medical requests and intake checklist for repair preparation.
- Retrieved account-security steps and cancellation instructions for unauthorized orders.
- Expanded membership questions with annual-membership terminology.
- Retrieved policy-version selection and the delivery-based start of return windows.
- Kept answers close to source wording, addressed the situation and standard alternatives, and removed source-selection notes.
- Set Gemini temperature to zero and spaced requests 4.2 seconds apart. Temperature zero did not make answers identical.

## Confirmation and limits

Final runs: 18/20 and 18/20. Cases changing pass status: E04, M02.
The current run fails E04 and A01 only on lexical Relevance. E04 gives the correct delivery estimate; A01 safely refuses medical diagnosis and states support scope.
Reference answers themselves fail the Relevance threshold in 14/20 cases. This diagnoses the word-overlap metric; it is not an alternative benchmark or a measured performance ceiling.
These questions were used for development and selection. The maximum is not proof of a global optimum or an estimate of generalization.
No answers were combined across runs. No reference answers were supplied to generation.

## Additional checks

See [validation review](validation_review.md): five initial responses included the required points; V04 exposed an omitted window start.
After the retrieval fix, V04 and the new V07 both give the 21-day window counted from confirmed delivery.
This review was performed by the coding assistant, not an independent human judge.

## Reproduction

Run from the repository root:

~~~powershell
& .venv/Scripts/python.exe domain_assistant.py --output artifacts/actual_answers_new.json
& .venv/Scripts/python.exe evaluate_answers.py --actual artifacts/actual_answers_new.json --output artifacts/benchmark_results_new.json
~~~

Source snapshots are in experiments/domain_assistant_v6.py through domain_assistant_v11.py.
All raw runs remain available beside this report; optimization_summary.json contains the comparison.
