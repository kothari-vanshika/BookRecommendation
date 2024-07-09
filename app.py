from flask import Flask,render_template,request
import pickle
from fuzzywuzzy import process
import numpy as np
popular_df=pickle.load(open('popular (2).pkl','rb'))
pt=pickle.load(open('pt.pkl','rb'))
books=pickle.load(open('books.pkl','rb'))
similarity=pickle.load(open('similarity.pkl','rb'))
app=Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html',
                           book_name=list(popular_df['Book-Title'].values),
                           book_author=list(popular_df['Book-Author'].values),
                           book_image=list(popular_df['Image-URL-M'].values),
                           book_votes=list(popular_df['num_ratings'].values),
                           book_rating=list(popular_df['avg_ratings'].values))
@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')
@app.route('/recommend_books',methods=['post'])
def recommend():
    user_input=request.form.get('user-input')
    match = process.extractOne(user_input, pt.index)
    matched_book = match[0]
    index=np.where(pt.index==matched_book)[0][0]
    distances=similarity[index]
    sorted_distances=sorted(list(enumerate(distances)),key= lambda x:x[1],reverse=True)[1:7]
    data=[]
    for i in sorted_distances:
     items=[]
     temp_df=books[books['Book-Title']==pt.index[i[0]]]
     items.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
     items.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
     items.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
     data.append(items)
    return render_template('recommend.html',data=data)
if __name__=="__main__":
    app.run(debug=True)