from sklearn.base import BaseEstimator
from typing import Dict
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC


def create_default_models_dict() -> Dict[str, BaseEstimator]:
    '''
    Returns default versions of 
    - Naive gausian bayes
    - Decision Tree Classifier
    - Random Forest Classifier
    - Support Vector Classifier
    '''
    
    return {
        'GaussianNB': GaussianNB(),
        'DecisionTree': DecisionTreeClassifier(random_state=42),
        'RandomForest': RandomForestClassifier(random_state=42),
        'SVC': SVC(random_state=42)
    }