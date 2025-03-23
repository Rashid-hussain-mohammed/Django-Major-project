def preprocess_text2(text):
    import nltk
    from nltk.corpus import stopwords
    from nltk.tokenize import word_tokenize
    from nltk.stem import WordNetLemmatizer
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.model_selection import train_test_split
    from sklearn.naive_bayes import MultinomialNB
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.linear_model import LogisticRegression
    from sklearn.model_selection import train_test_split

    import nltk
    nltk.download('stopwords')
    nltk.download('punkt')
    nltk.download('wordnet')


    import pandas as pd

# load CSV file
    df = pd.read_csv('Book123.csv')
    df.dropna(inplace=True)
# extract reviews and labels
    reviews = df['review'].tolist()
    labels = df['label'].tolist()

# preprocess data
    import nltk
    import string

# preprocess dataset
    stop_words = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()

    def preprocess(text):
    # remove punctuation and lowercase text
        text = text.lower().translate(str.maketrans('', '', string.punctuation))
    
    # tokenize text
        tokens = word_tokenize(text)
    
    # remove stopwords
        tokens = [word for word in tokens if word not in stop_words]
    
    # lemmatize tokens
        tokens = [lemmatizer.lemmatize(word) for word in tokens]
    
    # join tokens back into text
        text = ' '.join(tokens)
    
        return text
    reviews = [preprocess(review) for review in reviews]

# vectorize data
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(reviews)
    y = labels

# split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# train model
    model = LogisticRegression()
    model.fit(X_train, y_train)

# evaluate model
    score = model.score(X_test, y_test)
    

# use model to predict sentiment of new review
    new_review = str(text)
    new_review_vector = vectorizer.transform([new_review])
    predicted_label = model.predict(new_review_vector)[0]
    if predicted_label == 1:
        review_sentiment = "Positive"
    else:
        review_sentiment = "Negative"

    return review_sentiment
                    
