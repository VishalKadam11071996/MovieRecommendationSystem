from flask import Flask,render_template,request
import pickle
popular_df = pickle.load(open('popular_movies_df.pkl', 'rb'))
movies_df = pickle.load(open('movies_df.pkl', 'rb'))
similarity_mtx = pickle.load(open('similarity_mtx.pkl','rb'))
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',
                           title=list(popular_df['title'].values),
                           genres=list(popular_df['genres'].values),
                           crew=list(popular_df['crew'].values),
                           vote_avg=list(popular_df['vote_average'].values)
                           )

@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')


@app.route('/recommend_movies',methods=['post'])
def recommend():
    user_input = request.form.get('user_input')

    movie_index = movies_df[movies_df['title'] == user_input].index[0]
    distances = similarity_mtx[movie_index]
    top_5_similar_movie = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    data = []
    for movie in top_5_similar_movie:
        item = []
        item.append(movies_df.iloc[movie[0]].title)
        item.extend(movies_df.iloc[movie[0]].crew)
        item.append(movies_df.iloc[movie[0]].genres)

        data.append(item)
    return render_template('recommend.html', data=data)


if __name__ == '__main__':
    app.run(debug=True)