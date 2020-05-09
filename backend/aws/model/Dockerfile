FROM python:3.8

COPY requirements.txt requirements.txt
COPY tokenizer.py tokenizer.py
COPY claim.py claim.py

RUN pip install --no-cache-dir -r requirements.txt
# RUN python -m spacy download en_core_web_sm

EXPOSE 80

CMD [ "python", "tokenizer.py" ]