FROM python:3.8

#TODO add all files with .dockerignore
COPY app.py app.py
COPY claim.py claim.py
COPY controller.py controller.py
COPY exceptions.py exceptions.py
COPY tokenizer.py tokenizer.py
COPY tree.py tree.py
COPY wiki_scraper.py wiki_scraper.py


COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
# RUN python -m spacy download en_core_web_sm

EXPOSE 80

CMD [ "python", "tokenizer.py" ]