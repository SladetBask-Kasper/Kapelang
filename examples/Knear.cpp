
#include "/home/kada1004/pro/Kapelang/src/packages/ai/KNN.h"
#include "/home/kada1004/pro/Kapelang/src/packages/ai/iris.h"
#include "/home/kada1004/pro/Kapelang/src/packages/ai/common.h"
#include "/home/kada1004/pro/Kapelang/src/packages/stdkabe.h"

#define VER "0.2.6"


void error(const char *msg)
{
    perror(msg);
    exit(1);
}

int main(int argc, char const *argv[]) {
std::vector<std::vector<double>> X_train = std::vector<std::vector<double>>();
std::vector<int> y_train = std::vector<int>();
train_test_split(X_train, X, y_train, y);
KNN clf = KNN();
clf.fit(X_train, y_train);
std::vector<int> predictions = (std::vector<int>) clf.predict(X);
float accuracy = (float) accuracy_score(y, predictions);
kabe::string pc = (kabe::string) percent(accuracy);
std::cout << "Accuracy : "<<pc<<"" << std::endl;
return 0;
}
