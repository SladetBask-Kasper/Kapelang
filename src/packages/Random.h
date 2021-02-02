/*
 * This file is meant to partially make code with rand() calls
 * easier for cross platform since rand() does not work the
 * same on all systems and also make code with random calls
 * easier to read.
 */
#pragma once
#ifndef KABERANDOM
#define KABERANDOM
#include <ctime>
#include <cstdlib>

namespace kabe {
    class Random {
    private:
        int _min = 0;
        int _max = 10;
    public:

        void setSeed() {
            srand ( time(NULL) );
        }
        void setSeed(unsigned int seed) {
            srand(seed);
        }
        Random() {
            setSeed();
        }
        int roll() { return rand() % _max + _min; }
        int roll(int min, int max) { return rand() % (max - min) + min; }
        int roll(int max) { return rand() % max; }
        void setMinMax(int min, int max) {
            _min = min;
            _max = max;
        }
        void setMin(int min) {
            _min = min;
        }
        void setMax(int max) {
            _max = max;
        }
    };
}

#endif /* end of include guard: KABERANDOM */
