#pragma once
#include <iostream>
#include <string>
#include <iterator>
#include <numeric>
#include <algorithm>
#include <vector>
#include <functional>

using namespace std;
class KNN
{
public:
	KNN(vector<vector<double>> X, vector<int> y)
	{
		fit(X, y);
	}
	KNN() {}
	void fit(vector<vector<double>> X, vector<int> y)
	{
		dX_train = X;
		ny_train = y;
	}
	vector<int> predict(vector<vector<double>> X_test)
	{
		vector<int> predictions = {};

		for (vector<double> row : X_test) {
			int label = closest(row);
			predictions.push_back(label);
		}
		return predictions;
	}
	~KNN(){}
private:
	vector<vector<double>> dX_train = {};
	vector<int> ny_train;
	
	// Computes the distance between two std::vectors
	// SOURCE : http://www.cplusplus.com/forum/general/209784/
	template <typename T>
	double euc(const std::vector<T>& a, const std::vector<T>& b)
	{
		std::vector<double>	auxiliary;
		std::transform(a.begin(), a.end(), b.begin(), std::back_inserter(auxiliary),
			[](T element1, T element2) {return pow((element1 - element2), 2); });
		auxiliary.shrink_to_fit();
		// return  sqrt(std::accumulate(auxiliary.begin(), auxiliary.end(), 0 ));
		return std::sqrt(std::accumulate(auxiliary.begin(), auxiliary.end(), 0.0));
	}
	int closest(vector<double> row)
	{
		double best_dist = euc(row, dX_train[0]);
		int best_index = 0;

		for (int i = 1; i < dX_train.size(); i++)
		{
			double dist = euc(row, dX_train[i]);
			if (dist < best_dist) {
				best_dist = dist;
				best_index = i;
			}
		}
		return ny_train[best_index];
	}
};