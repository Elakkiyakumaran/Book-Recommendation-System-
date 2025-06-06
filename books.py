from flask import Flask, request, render_template
import pickle

# Load the data and model
books = pickle.load(open('books.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

app = Flask(__name__)

def recommend(book_title):
    book_title = book_title.strip().lower()
    matches = books[books['title'].str.lower().str.contains(book_title)]

    if matches.empty:
        return []

    book_index = matches.index[0]
    distances = list(enumerate(similarity[book_index]))
    sorted_books = sorted(distances, reverse=True, key=lambda x: x[1])[1:6]

    recommendations = []
    for i in sorted_books:
        item = books.iloc[i[0]]
        recommendations.append({
            'title': item['title'],
            'isbn13': item['isbn13'],
            'thumbnail': item['thumbnail']
        })
    return recommendations


@app.route("/", methods=["GET", "POST"])
def index():
    recs = []
    if request.method == "POST":
        book_title = request.form.get("book_title")
        if book_title:
            recs = recommend(book_title)
    return render_template("index.html", recommendations=recs)

if __name__ == "__main__":
    app.run(debug=True)
