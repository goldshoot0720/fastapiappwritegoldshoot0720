cd "C:\Users\chbon\Documents\python\appwrite"
explorer http://127.0.0.1:8000
set APPWRITE_LOCAL_TEST=1
python -m uvicorn main:app --reload
pause