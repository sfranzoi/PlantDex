run

bash
uvicorn app.main:app --reload

then
bash
python backend/tests/test_analyze.py