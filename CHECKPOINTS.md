# Hướng dẫn Checkpoints (CHECKPOINTS)

Tài liệu này định nghĩa 6 mốc tiến độ (Checkpoints CP0–CP5) trong buổi lab AI Evaluation (14:15 – 18:00, hoàn thành bài lab trước 17:00). Mỗi checkpoint bao gồm mục tiêu thời gian, sản phẩm đầu ra, kiến thức cốt lõi và các lệnh tự kiểm tra.

---

## Bảng tổng quan tiến độ (Schedule)

| Checkpoint | Khoảng thời gian | Mốc thời gian mẫu | Nội dung trọng tâm | Kết quả kiểm tra chính |
|---|---|---|---|---|
| **CP0** Setup | Start + 0–15m | 14:15–14:30 | Môi trường, `.env`, baseline tests | 42 failed baseline |
| **CP1** Data Models | Start + 15–30m | 14:30–14:45 | Task 1: `QAPair`, `EvalResult`, `overall_score` | 3 passed |
| **CP2** Metrics | Start + 30–65m | 14:45–15:20 | Task 2–3: RAGAS metrics & LLMJudge | 21 passed, 20 failed, 1 skipped |
| **CP3** Runner & Analyzer | Start + 65–85m | 15:20–15:40 | Task 4–5: BenchmarkRunner, FailureAnalyzer | 41 passed, 1 skipped (full suite) |
| **CP4** Dataset & Benchmark | Start + 85–140m | 15:40–16:35 | 20 QA golden dataset, RAG run, Exercise 3.2 & 3.3 | Validator PASS, artifacts generated |
| **CP5** Reflection & Finalize | Start + 140–165m | 16:35–17:00 | `reflection.md`, copy `solution/solution.py`, kiểm tra cuối | 41 passed, validator PASS, clean repo |

---

## Chi tiết từng Checkpoint

### CP0 — Setup & Baseline (Start + 0–15m | 14:15–14:30)

- **Sản phẩm:**
  - Virtual environment `.venv` đã được tạo và kích hoạt.
  - Toàn bộ dependencies trong `requirements.txt` đã được cài đặt.
  - File `.env` được tạo từ `.env.example` (điền `OPENAI_API_KEY` hoặc chọn `GENERATOR_PROVIDER=gemini` và điền `GEMINI_API_KEY` cho Part 3).
- **Cần hiểu:**
  - Cấu trúc thư mục của repository và vai trò của từng module: `template.py` (evaluation engine) vs `domain_assistant.py` (system under evaluation).
  - Tình trạng khởi đầu của starter code: 42 tests được thu thập và 42 tests failed (do các TODO chưa được implement).
- **Tự kiểm tra:**
  ```bash
  python --version                        # Yêu cầu 3.11+
  pytest tests/ -v                         # Baseline: 42 collected, 42 failed
  ```

---

### CP1 — Data Models (Task 1) (Start + 15–30m | 14:30–14:45)

- **Sản phẩm:**
  - Các dataclass `QAPair` và `EvalResult` trong `template.py` có đầy đủ các trường dữ liệu và default factories.
  - Phương thức `EvalResult.overall_score()` trả về giá trị trung bình cộng của 3 answer metrics: `faithfulness`, `relevance`, và `completeness`.
- **Cần hiểu:**
  - Golden dataset cần những trường nào để phục vụ đánh giá (question, expected_answer, context, metadata, retrieved_contexts).
  - Phân định rõ ràng giữa Answer-side metrics (được tính vào `overall_score()`) và Retrieval-side metrics (`context_recall`, `context_precision` chỉ dùng chẩn đoán retrieval, không tính vào `overall_score()`).
- **Tự kiểm tra:**
  ```bash
  pytest tests/test_solution.py::TestEvalResultOverallScore -v
  ```
  *Kỳ vọng:* 3 passed.

---

### CP2 — Metrics & LLM Judge (Tasks 2–3) (Start + 30–65m | 14:45–15:20)

- **Sản phẩm:**
  - `RAGASEvaluator`:
    - 3 Answer metrics: `evaluate_faithfulness`, `evaluate_relevance`, `evaluate_completeness`.
    - 2 Retrieval metrics: `evaluate_context_recall`, `evaluate_context_precision` (Average Precision@K).
    - `run_full_eval()`: kết nối 3 answer metrics và chỉ tính 2 retrieval metrics khi có `contexts`. Xác định đúng `failure_type` ("hallucination", "irrelevant", "incomplete", "off_topic").
  - `LLMJudge`:
    - `score_response()`: tạo prompt, gọi hàm judge LLM, phân tích điểm JSON (hoặc trả 0.5 fallback).
    - `detect_bias()`: phát hiện positional bias, leniency bias (> 0.8), severity bias (< 0.3).
- **Cần hiểu:**
  - Thuật toán token overlap loại bỏ stopwords (`STOPWORDS`).
  - Rank-aware Average Precision@K thưởng cho retriever xếp chunk liên quan lên đầu.
  - Ba loại bias thường gặp của LLM-as-a-Judge và cách thiết kế rubric để giảm thiểu bias.
- **Tự kiểm tra:**
  ```bash
  # Kiểm tra Task 2 (RAGAS Evaluator)
  pytest tests/test_solution.py::TestRAGASEvaluator tests/test_solution.py::TestContextMetrics tests/test_solution.py::TestRetrievalMetricWiring::test_run_full_eval_connects_optional_retrieval_metrics -v
  # Kỳ vọng Task 2: 14 passed, 1 skipped

  # Kiểm tra Task 3 (LLM Judge)
  pytest tests/test_solution.py::TestLLMJudge -v
  # Kỳ vọng Task 3: 4 passed
  ```
  *Toàn bộ suite cộng dồn:* `pytest tests/ -v` đạt 21 passed, 20 failed, 1 skipped.

---

### CP3 — Runner & Failure Analyzer (Tasks 4–5) (Start + 65–85m | 15:20–15:40)

- **Sản phẩm:**
  - `BenchmarkRunner`:
    - `run()`: chạy các QA pairs qua `agent_fn`, truyền `retrieved_contexts` vào `run_full_eval()`.
    - `generate_report()`: tính pass rate và giá trị trung bình của các metrics (bao gồm retrieval averages nếu có).
    - `run_regression()`: phát hiện metric bị giảm quá 0.05 so với baseline.
    - `identify_failures()`: lọc danh sách các kết quả có điểm dưới ngưỡng (threshold).
  - `FailureAnalyzer`:
    - `categorize_failures()`: thống kê số lượng lỗi theo từng loại `failure_type`.
    - `find_root_cause()`: chẩn đoán nguyên nhân gốc dựa trên điểm số thấp nhất.
    - `generate_improvement_suggestions()`: gợi ý ít nhất 3 hành động khắc phục cụ thể.
    - `generate_improvement_log()`: xuất bảng Markdown ghi nhận lỗi và đề xuất xử lý.
- **Cần hiểu:**
  - Tự động hóa benchmark pipeline và vai trò quality gate trong CI / CD (ngăn chặn deploy khi điểm hồi quy > 0.05).
  - Nguyên lý failure clustering: sửa một root cause có thể giải quyết nhiều lỗi cùng lúc.
  - Vòng lặp cải tiến liên tục: Evaluate → Analyze → Improve → Augment → Repeat.
- **Tự kiểm tra:**
  ```bash
  # Kiểm tra Task 4 & Task 5
  pytest tests/test_solution.py::TestBenchmarkRunner tests/test_solution.py::TestRunRegression tests/test_solution.py::TestRetrievalMetricWiring::test_runner_forwards_retrieved_contexts tests/test_solution.py::TestRetrievalMetricWiring::test_report_includes_retrieval_averages -v
  pytest tests/test_solution.py::TestFailureAnalyzer tests/test_solution.py::TestGenerateImprovementLog -v

  # Kiểm tra toàn bộ suite bắt buộc
  pytest tests/ -v
  ```
  *Kỳ vọng:* **41 passed, 1 skipped** (test reranking Exercise 3.5 được skip nếu chưa làm bonus).

---

### CP4 — Golden Dataset & Real Benchmark (Start + 85–140m | 15:40–16:35)

- **Sản phẩm:**
  - File `golden_dataset.json` chứa 20 QA pairs phân bổ theo stratified sampling: 5 Easy, 7 Medium, 5 Hard, 3 Adversarial.
  - Chạy `domain_assistant.py` để sinh `artifacts/actual_answers.json`.
  - Chạy `evaluate_answers.py` để tạo `artifacts/benchmark_results.json`.
  - Hoàn thiện Exercise 3.2 (bảng kết quả 5 metrics + phân tích 3 cases thấp nhất) và Exercise 3.3 (rubric 1–5 cho domain OrbitTech) trong `exercises.md`.
- **Cần hiểu:**
  - Nguyên tắc tránh data leakage: `DomainAssistant` chỉ đọc `question`, không bao giờ được đọc `expected_answer` hay gold contexts khi trả lời.
  - Provenance của ground-truth: Mọi context và expected answer phải bắt nguồn xác thực từ các tài liệu trong `data/technology_store/*.md`.
- **Tự kiểm tra:**
  ```bash
  python validate_golden_dataset.py
  python domain_assistant.py
  python evaluate_answers.py
  ```
  *Kỳ vọng:* `validate_golden_dataset.py` báo kết quả **PASS**. Hai file artifact được tạo ra và có đầy đủ dữ liệu 20 câu hỏi.

---

### CP5 — Reflection & Final Submission (Start + 140–165m | 16:35–17:00)

- **Sản phẩm:**
  - File `reflection.md` được điền đầy đủ: phân tích 3 failure cases bằng kỹ thuật 5 Whys, bảng failure taxonomy, improvement log và chiến lược regression testing.
  - File `solution/solution.py` đã được cập nhật bản hoàn thiện từ `template.py`.
  - Toàn bộ checklist nộp bài trong `SUBMISSION.md` được rà soát và đáp ứng.
- **Cần hiểu:**
  - Phương pháp 5 Whys để đi từ triệu chứng bề mặt đến nguyên nhân gốc rễ (retrieval vs generation vs prompt).
  - Tầm quan trọng của việc kiểm tra toàn diện trước khi nộp bài để tránh mất điểm do lỗi tên repo hoặc thiếu file.
- **Tự kiểm tra:**
  > ⚠️ **Cảnh báo quan trọng về solution:**  
  > Test suite luôn ưu tiên load `solution/solution.py` nếu file này tồn tại.  
  > - **Chỉ chạy lệnh copy sau khi bạn đã hoàn thiện toàn bộ code trong `template.py`**.  
  > - **Nếu bạn làm bài trực tiếp trên `solution/solution.py`, TUYỆT ĐỐI KHÔNG chạy lệnh `cp` này** vì sẽ ghi đè và xóa mất toàn bộ code hoàn thiện của bạn bằng file `template.py` chưa hoàn thành! Hãy giữ hai file đồng bộ cẩn thận.

  ```bash
  # 1. Copy solution hoàn chỉnh (chỉ chạy khi bạn code trên template.py)
  cp template.py solution/solution.py

  # 2. Chạy test suite xác nhận
  pytest tests/ -v
  # Kỳ vọng: 41 passed, 1 skipped

  # 3. Xác thực dataset
  python validate_golden_dataset.py
  # Kỳ vọng: PASS

  # 4. Kiểm tra Git không lộ secret
  git status
  ```

---

## Tài liệu liên quan
- [README.md](README.md) — Tổng quan bài lab và hướng dẫn khởi động
- [SUBMISSION.md](SUBMISSION.md) — Hướng dẫn nộp bài, định dạng tên repo và checklist
- [RUBRIC.md](RUBRIC.md) — Tiêu chí chấm điểm chi tiết và các trường hợp trừ điểm
- [RULES.md](RULES.md) — Quy định làm bài, sử dụng AI và bảo mật
