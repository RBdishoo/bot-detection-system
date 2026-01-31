from models.dataset import ModelDataset
from models.train import ModelTrainer
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if __name__ == '__main__':
    featuresCSV = 'backend/data/processed/training_data_sessions.csv'
    labelsCSV = 'backend/data/raw/labels.csv'

    #Load and Prepare
    dataset = ModelDataset(featuresCSV, labelsCSV)
    xTrain, xTest, yTrain, yTest, featureNames, scaler = dataset.prepare()

    print(f"Train shape: {xTrain.shape}, Test shape: {xTest.shape}")
    print(f"Feature Names: {featureNames[:5]}...") #Shows first 5 


    """
    #Train Models
    trainer = ModelTrainer()

    #RandomForest
    rfModel, rfMetrics, rfImportance = trainer.trainRandomForest(xTrain, xTest, yTrain, yTest, featureNames)

    print(f"RandomForest Accuracy: {rfMetrics['accuracy']:.4f}")
    print(f"RandomForst ROC-AUC: {rfMetrics['roc_auc']:.4f}")
    trainer.saveModel(rfModel, 'RandomForest')

    #XGBoost
    xgbModel, xgbMetrics, xgbImportance = trainer.trainXGBoost(xTrain, xTest, yTrain, yTest, featureNames)

    print(f"XGBoost Accuracy: {xgbMetrics['accuracy']:.4f}")
    print(f"XGBoost ROC-AUC: {xgbMetrics['roc_auc']:.4f}")
    trainer.saveModel(xgbModel, 'XGBoost')

    #Save Metrics
    allMetrics = [rfMetrics, xgbMetrics]
    trainer.saveMetrics(allMetrics)

    #Save Feature Importance
    rfImportance.to_csv('models/trained/rf_feature_importance.csv', index=False)
    xgbImportance.to_csv('models/trained/xgb_feature_importnace.csv', index=False)

    print("\n Training Complete")

    """