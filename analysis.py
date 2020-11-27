from sklearn.naive_bayes import MultinomialNB  # type: ignore
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer  # type: ignore
from sklearn.pipeline import Pipeline  # type: ignore
from imblearn.over_sampling import RandomOverSampler  # type: ignore
# from sklearn.model_selection import GridSearchCV, train_test_split, cross_val_score  # type: ignore


def make_model(df):
    print('\nTraining prediction model...')

    # Split X, y
    X = df[['lyrics']]
    y = df['artist']

    # Reduce class imbalance
    ros = RandomOverSampler()
    X, y = ros.fit_resample(X, y)
    X = X['lyrics']

    # Pipeline
    p = Pipeline(steps=[
        ('vectorize', CountVectorizer(ngram_range=(1, 3), stop_words=None)),
        ('tfidf', TfidfTransformer()),
        ('classifier', MultinomialNB(alpha=0.1))
    ])

    p.fit(X, y)

    print('Ok, ready to guess artists.\n')
    return p


def predict_artist(pipeline):
    line = input(
        'Please write down some words from a song (or write "bye" to leave):\n')
    if line == 'bye':
        print('\nOk, bye!')
        return
    else:
        pred = pipeline.predict([line])
        print('\nThe song is probably from:', pred[0])
        print()

        predict_artist(pipeline)


# Used for model optimization:

# def optimize_hyperparams(pipeline, Xtrain, ytrain):
#     print('Optimizing hyperparams')
#     params = {
#         'vectorize__stop_words': ['english', None],
#         'vectorize__ngram_range': [(1, 1), (1, 2), (1, 3)],
#         'tfidf__use_idf': (True, False),
#         'classifier__alpha': (0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0)
#     }

#     gs = GridSearchCV(pipeline, param_grid=params, cv=5, n_jobs=-1)

#     gs = gs.fit(Xtrain, ytrain)

#     print(gs.best_params_)


# def cross_validate(pipeline, Xtrain, ytrain):
#     print("Cross validating model")
#     score = cross_val_score(pipeline, Xtrain, ytrain, cv=5)
#     print(score)
#     print(score.mean())


# def score_test(pipeline, Xtest, ytest):
#     print('Scoring with test data...')
#     ytestpred = pipeline.predict(Xtest)
#     print(pipeline.score(Xtest, ytest))
