#pragma once
#include <iostream>
#include <string>
#include <vector>

// print for vectors for debuging
template <typename T>
void print(std::vector<T> data, std::string label) {
	int count = 0;
	for (T a : data) {
		std::cout << count++ << " " << label << ": " << a << std::endl;
	}
}

template <typename T>
void print(std::vector<std::vector<T>> data, std::string label) {
	int count = 0;
	for (std::vector<T> i : data) {
		print(i, std::to_string(count) + "->" + label);
	}
}

float accuracy_score(std::vector<int> labels, std::vector<int> predicts)
{
	std::vector<int> small;
	std::vector<int> big;
	if (labels.size() >= predicts.size()) {
		small = predicts;
		big = labels;
	}

	int diff = big.size() - small.size();

	for (size_t i = 0; i < small.size(); i++)
	{
		if (big[i] != small[i])
		{
			diff++;
		}
	}

	return 1.0f-((float) ((double)diff/(double)big.size()));
	//return ((float)((double)diff / (double)big.size()));
}

std::string percent(float x) { return (std::to_string(x * 100).substr(0, 4) + ((std::string) "%")); }


template <typename T>
int vecsize(std::vector<T>& vec) { return static_cast<int>(vec.size()); }

std::vector<double> pop(std::vector<std::vector<double>>& vec, int index)
{
	if (index > vecsize(vec)) {
		std::cout << "error" << std::endl;
		exit(0);
	}
	std::vector<double> returnValue = vec[index];
	vec.erase(vec.begin() + index);
	return returnValue;
}
int pop(std::vector<int>& vec, int index)
{
	if (index > vecsize(vec)) {
		std::cout << "error" << std::endl;
		exit(0);
	}
	int returnValue = vec[index];
	vec.erase(vec.begin() + index);
	return returnValue;
}

/*
#SOURCE : https://machinelearningmastery.com/implement-resampling-methods-scratch-python/
from random import randrange

# Split a dataset into a train and test set
def train_test_split(dataset, split=0.60):
	train = list()
	train_size = split * len(dataset)
	dataset_copy = list(dataset)
	while len(train) < train_size:
		index = randrange(len(dataset_copy))
		train.append(dataset_copy.pop(index))
	return train, dataset_copy
*/

//
// <ARGS>
// ref X_train : (should be empty 2d double vector)
// ref X_test : (X data)
// ref y_train : (Same as X_train but for labels)
// y_test : (Same as X_test but for labels/y data)
// test_size : self explaining
// </ARGS>
//
void train_test_split(std::vector<std::vector<double>>& X_train,
	std::vector<std::vector<double>>& X_test, std::vector<int>& y_train, std::vector<int>& y_test,
	float test_size = 0.5)
{
	int train_size = (int)(test_size * vecsize(X_test));
	while (vecsize(X_train) < train_size)
	{

		int index = rand() % (vecsize(X_test));
		X_train.push_back(pop(X_test, index));
		y_train.push_back(pop(y_test, index));
	}
	// Shuffles around X_test
	std::vector<std::vector<double>> tmp_X = {};
	std::vector<int> tmp_y = {};
	while (vecsize(X_test) > 0)
	{
		int index = rand() % (vecsize(X_test));
		tmp_X.push_back(pop(X_test, index));
		tmp_y.push_back(pop(y_test, index));
	}
	X_test = tmp_X;
	y_test = tmp_y;
}
