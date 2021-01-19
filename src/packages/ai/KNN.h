#pragma once
#include <iterator>
#include <numeric>
#include <algorithm>
#include <vector>
#include <functional>
#include <cmath>
#include <stdexcept>

class KNN
{
private:
	std::vector<std::vector<double>> dX_train;
	std::vector<int> ny_train;

	// Computes the distance between two std::vectors
	// SOURCE : http://www.cplusplus.com/forum/general/209784/
	template <typename T>
	double euc(const std::vector<T>& a, const std::vector<T>& b)
	{
		std::vector<double>	auxiliary;
		std::transform(a.begin(), a.end(), b.begin(), std::back_inserter(auxiliary),
			[](T element1, T element2) {return pow((element1 - element2), 2.0); });
		auxiliary.shrink_to_fit();
		return std::sqrt(std::accumulate(auxiliary.begin(), auxiliary.end(), 0.0));
	}
	int closest(std::vector<double> row)
	{
		double best_dist = euc(row, dX_train.at(0)); // X_test = row | X_train = dX_train
		int best_index = 0;

		for (size_t i = 1; i < dX_train.size(); i++)
		{
			double dist = euc(row, dX_train[i]);
			if (dist < best_dist) {
				best_dist = dist;
				best_index = i;
			}
		}
		return ny_train[best_index];
	}
public:
	KNN(std::vector<std::vector<double>> X, std::vector<int> y) { fit(X, y); }
	KNN() {}
	void fit(std::vector<std::vector<double>> X, std::vector<int> y)
	{
		if (X.size() <= 1 || y.size() <= 1) 
			throw std::invalid_argument("Empty X or y value");

		// I had a problem with this code saving a reference so I hope the below code will make sure to save a copy.
		//dX_train = X; 
		//ny_train = y;

		// This code should now copy which the code above seems to not have done.
		std::copy(y.begin(), y.end(), std::back_inserter(ny_train));
		std::copy(X.begin(), X.end(), std::back_inserter(dX_train));
	}
	std::vector<int> predict(std::vector<std::vector<double>> X_test)
	{
		std::vector<int> predictions = {};
		for (std::vector<double> row : X_test) predictions.push_back(closest(row));
		return predictions;
	}
	~KNN() {}
};
