/*
 * This file is meant to partially make code with rand() calls
 * easier for cross platform since rand() does not work the
 * same on all systems and also make code with random calls
 * easier to read.
 * 
 * The code is written with boost but i believe it can be
 * written completely with STD lib.
 * A similar algorithm written completely with STD lib 
 * can be found here : https://codeforces.com/blog/entry/61587
 * 
 * Issues:
 * I'm unsure if and how seeding works/is working.
 * This only works with signed integers for now.
 * 
 * Usage:
 * Random r = Random(true/false/uint seed); // or just Random r = Random();
 * // true = it will update seed every roll (default)
 * // false = it will run with same seed every roll
 * // seed = will disable updating seed every roll and set this as seed
 * int hi = r.roll(0, 1); // will get random number from 0 to 1 including both.
 * int index = r.roll(vec.size());
 * // will get random number from index 0 of std::vector called vec
 * // to last index of vec (i.e. vec.size()-1, since .size includes index 0)
 */
#ifndef KABERANDOM
#define KABERANDOM

#include <chrono>
#include <boost/random.hpp>

namespace kabe {
    class Random {
    private:
        bool alwaysSeed = false;
        unsigned int currentSeed;
        boost::random::mt19937 rng = boost::random::mt19937();
    public:

        void setSeed(unsigned int seed) {
            this->currentSeed = seed; // this should get a copy of seed.
            rng = boost::random::mt19937(this->currentSeed);
        }
        void setSeed() {
            this->setSeed(unsigned(std::chrono::steady_clock::now().time_since_epoch().count()));
        }
        unsigned int getSeed() { return currentSeed; }
        Random(bool _alwaysSeed = true) {
            this->doAlwaysSeed(_alwaysSeed);
            this->setSeed();
        }
        Random(unsigned int seed) {
            this->doAlwaysSeed(false);
            this->setSeed(seed);
        }
        int roll(int max = 10) { return this->roll(0, max-1); }
        int roll(int min, int max) {
            if (this->alwaysSeed) this->setSeed();
            
            boost::uniform_int<> range(min, max);
            boost::variate_generator< boost::random::mt19937, boost::uniform_int<> > dice(this->rng, range);
            return dice();
        }
        void doAlwaysSeed(bool value) {
            this->alwaysSeed = value;
        }
        bool getAlwaysSeed() {
            return this->alwaysSeed;
        }
    };
}

#endif /* end of include guard: KABERANDOM */
