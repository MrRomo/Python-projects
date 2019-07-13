# Requirements
#   pip install matplotlib
#   pip install python-mnist
#   pip install scikit-learn

from mnist import MNIST
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix


defevaluate_classifier(classifier, t_data, t_labels):
    prediction = classifier.predict(t_data)
    c_matrix = confusion_matrix(t_labels, prediction)
    return c_matrix


defgenerate_score(c_matrix):
    return (c_matrix.diagonal().sum() * 100.) / c_matrix.sum()


# define and load data from path
mnData = MNIST('/path/to/data')
data, labels = mnData.load_training()

# split data to train
train_data, test_data, train_labels, test_labels = train_test_split(data, labels, test_size=0.3, random_state=46)

# Decision Tree
dt_classifier = DecisionTreeClassifier()
dt_classifier.fit(train_data, train_labels)
cm = evaluate_classifier(dt_classifier, test_data, test_labels)
print(cm)
score = generate_score(cm)
print(score)

# Random Forest
rf_classifier = RandomForestClassifier(n_estimators=150, min_samples_split=2)
rf_classifier.fit(train_data, train_labels)
cm2 = evaluate_classifier(rf_classifier, test_data, test_labels)
print(cm2)
score2 = generate_score(cm2)
print(score2)