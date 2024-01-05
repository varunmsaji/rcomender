
from flask import Flask,render_template,request
import pickle
import numpy as np

popular_df = pickle.load(open('popular.pkl','rb'))
pt = pickle.load(open('pt.pkl','rb'))
books = pickle.load(open('books.pkl','rb'))
similarity_scores = pickle.load(open('similarity_score.pkl','rb'))
book_title = list(popular_df['Book-Title'].values)
image = list(popular_df['Image-URL-M'].values)
author = list(popular_df['Book-Author'].values)



app = Flask(__name__)


@app.route('/')
def index():
    return render_template('test.html',book_title = book_title,image=image,author=author)


@app.route('/recommend')
def recoment():
    return render_template('recomendtest.html')



@app.route('/recommend_books',methods=['post'])
def recommendb():
    user_input = request.form.get('user_input')
    data =[]
    if user_input:
    
        index = np.where(pt.index==user_input)[0][0]
        similar_items = sorted(list(enumerate(similarity_scores[index])),key=lambda x:x[1],reverse=True)[1:6]
        
        for i in similar_items:
            item =[]
            temp_df = books[books['Book-Title']==pt.index[i[0]]]
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
            
            data.append(item)
    # print(data)
    return render_template('recomendtest.html',data=data)





if __name__=='__main__':
    app.run(debug=True)