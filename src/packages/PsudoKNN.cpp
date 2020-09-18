﻿// PsudoKNN.cpp : Defines the entry point for the application.
//

#include "PsudoKNN.h"
#include "KNN.h"
#include "basics.h"
#include "iris.h"

using namespace std;

int main()
{
	// Vars
	vector<vector<double>> X_train = {};
	vector<vector<double>> X_test = X;
	vector<int> y_train = {};
	vector<int> y_test = y;

	// in python:
	// X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5)
	// in c++:
	train_test_split(X_train, X_test, y_train, y_test, 0.5);

	// print the data for good measure.
	print(X_train, X_test, y_train, y_test);

	// Create classifier.
	KNN clf = KNN();// kNearestNeighbor
	clf.fit(X_train, y_train);
	vector<int> predictions = clf.predict(X_test);
	cout << "Predictions(" << predictions.size() << "):" << endl;
	print(predictions);
	float accuracy = accuracy_score(y_test, predictions);
	cout << accuracy << endl;

	return 0;
}
