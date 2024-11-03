from flask import Flask, render_template, request, send_from_directory
import os
from whoosh.index import create_in
from whoosh.fields import Schema, TEXT, ID
from whoosh.qparser import QueryParser

app = Flask(__name__)
VIDEO_DIRECTORY = 'C:/DEV/TESTESITE/videos'
INDEX_DIRECTORY = 'C:/DEV/TESTESITE/index'

# Define o esquema para a indexação
schema = Schema(title=TEXT(stored=True), path=ID(stored=True))

# Cria o diretório de índice se não existir
if not os.path.exists(INDEX_DIRECTORY):
    os.mkdir(INDEX_DIRECTORY)
    ix = create_in(INDEX_DIRECTORY, schema)
    writer = ix.writer()
    for video in os.listdir(VIDEO_DIRECTORY):
        writer.add_document(title=video, path=video)
    writer.commit()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    query_str = request.form['query']
    ix = open_dir(INDEX_DIRECTORY)
    query = QueryParser("title", ix.schema).parse(query_str)
    with ix.searcher() as searcher:
        results = searcher.search(query)
        videos = [hit['path'] for hit in results]
    return render_template('search_results.html', videos=videos)

@app.route('/play/<filename>')
def play_video(filename):
    return send_from_directory(VIDEO_DIRECTORY, filename)

if __name__ == '__main__':
    app.run(debug=True)
