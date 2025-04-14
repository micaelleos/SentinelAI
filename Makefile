install:
	myenv\Scripts\activate.bat
	pip install -r requirements.txt

playwright:
	playwright install

run:
	python -m streamlit run app.py