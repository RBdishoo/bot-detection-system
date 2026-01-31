import pandas as pd
import numpy as np
from sklearn.metrics import (accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix, classification_report, roc_curve)
import matplotlib.pyplot as plt
import json
from pathlib import Path

class Evaluator:
    """Generate evaluation reports and visualizations"""

    def __init__(self, outputDir: str = 'models/trained'):
        self.outputDir = Path(outputDir)
        self.outputDir.mkdir(parents=True, exist_ok=True)

    def generateReport(self, yTest, yPrediction, yPredictionProbability, modelName: str):
        """Generate text classification report"""

        report = {

            'model': modelName,
            'accuracy': float(accuracy_score(yTest, yPrediction)),
            'precision': float(precision_score(yTest, yPrediction)),
            'recall': float(recall_score(yTest, yPrediction)),
            'f1Score': float(f1_score(yTest, yPrediction)),
            'roc_auc': float(roc_auc_score(yTest, yPredictionProbability)),
            'confusionMatrix': confusion_matrix(yTest, yPrediction).tolist(),
            'classificationReport': classification_report(yTest, yPrediction, output_dict=True)
        }
        return report
    
    def saveReport(self, report: dict, filename: str = 'evaluationReport.json'):
        """save report to JSON"""

        path = self.outputDir / filename
        with open(path, 'w') as f:
            json.dump(report, f, indent = 2)
        print(f"Saved report to {path}")

    def plotConfusionMatrix(self, yTest, yPrediction, modelName: str):
        """
        
        Plot and save confusion matrix

        A confusion matrix is a table that shows how a classification model's predictions compare to the true labels, broken down into counts of correct and incorrect predictions.

        True Positive: Model correctly predicts the positive class
        True Negative: model correctly predicts the negative class
        
        False Positive: Model predicts positive, but the true label is negative (Type I error)
        True Negative: Model predicts negative, but the true label is positive (Type II error)

        can use these to compute metrics such as accuracy, precision, recall, specificity, and F1-score. 
        It shows exactly where the model is making mistakes.
        
        """

        confusionMatrix = confusion_matrix(yTest, yPrediction)
        plt.figure(figsize=(8, 6))
        plt.imshow(confusionMatrix, interpolation='nearest', cmap=plt.cm.Blues)
        plt.title(f'Confusion Matrix for {modelName}')
        plt.colorbar()

        classes = ['Human', 'Bot']
        tickMarks = np.arrange(len(classes))
        plt.xticks(tickMarks, classes)
        plt.yticks(tickMarks, classes)

        #Add text annotations
        for i in range(confusionMatrix.shape[0]):
            for j in range(confusionMatrix.shape[1]):
                plt.text(j, i, str(confusionMatrix[i, j]), ha='center', va='center', color='white')
        
        plt.ylabel('True Label')
        plt.xlabel('Predicted Label')

        path = self.outputDir / f'{modelName}_confusionMatrix.png'
        plt.savefig(path, dpi=100, bbox_inches='tight')
        print(f"Saved conusion matrix to {path}")
        plt.close()
