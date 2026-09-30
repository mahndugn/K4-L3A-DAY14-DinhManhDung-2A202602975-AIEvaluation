"""Regression checks for policy passages needed by common support intents."""

from domain_assistant import BM25Retriever, _is_medical_request, load_corpus


def test_out_of_scope_medical_request_retrieves_scope_rule():
    _, chunks = load_corpus("data/technology_store")
    retrieved = BM25Retriever(chunks).retrieve("Please diagnose my chest pain.")
    assert "OT-00-P03" in {chunk.chunk_id for chunk in retrieved}


def test_repair_preparation_retrieves_required_intake_fields():
    _, chunks = load_corpus("data/technology_store")
    retrieved = BM25Retriever(chunks).retrieve(
        "My laptop has a defect after the return window. What should I prepare for warranty repair?"
    )
    assert "OT-07-P02" in {chunk.chunk_id for chunk in retrieved}


def test_repair_quote_question_keeps_quote_rule_first():
    _, chunks = load_corpus("data/technology_store")
    retrieved = BM25Retriever(chunks).retrieve(
        "My phone has accidental impact damage outside warranty. I decline the repair quote. What happens and is there a fee?"
    )
    assert retrieved[0].chunk_id == "OT-07-P04"


def test_device_diagnosis_is_not_routed_as_medical():
    assert not _is_medical_request("Please diagnose my phone battery problem.")


def test_unauthorized_order_retrieves_security_and_cancellation():
    _, chunks = load_corpus("data/technology_store")
    retrieved = BM25Retriever(chunks).retrieve(
        "Someone placed an unauthorized order from my account. Can I cancel it?"
    )
    ids = {chunk.chunk_id for chunk in retrieved}
    assert {"OT-08-P02", "OT-02-P03"} <= ids


def test_return_policy_retrieves_version_and_window_start():
    _, chunks = load_corpus("data/technology_store")
    retrieved = BM25Retriever(chunks).retrieve(
        "I placed an order on August 20, 2026 and received it on September 2. "
        "Which return policy applies and when does the window start?"
    )
    assert {"OT-09-P03", "OT-09-P04"} <= {c.chunk_id for c in retrieved}
