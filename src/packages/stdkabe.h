#pragma once
#include <iostream>
#include "String.h"
// there is also "FileReader.h" and "dict.h" but I don't see that as a necessary datatype to import now, but the user may choose to do it later.
#include <stdint.h>
#include <boost/lexical_cast.hpp>
//#include <io.h> //#include <fcntl.h> // don't know when or why I added these two but the program works without them so...

#define u8 uint8_t
#define u16 uint16_t
#define u32 uint32_t
#define u64 uint64_t

// idk if s8...s64 is a thing but it's mentioned here : http://michas.eu/blog/c_ints.php?lang=en
#define s8 int8_t
#define s16 int16_t
#define s32 int32_t
#define s64 int64_t

// this seems to be like 64bit plus integers in case you are running on harware that support more than 64 bits.
#define l64 int_least64_t
#define ul64 uint_least64_t

// idk what fast means tbh but for however need it it's now quicker to write.
#define f8 int_fast8_t
#define uf8 uint_fast8_t
#define f16 int_fast16_t
#define uf16 uint_fast16_t
#define f32 int_fast32_t
#define uf32 uint_fast32_t
#define f64 int_fast64_t
#define uf64 uint_fast64_t

#ifndef HAS_KABE_TYPE_PACKAGE
#define HAS_KABE_TYPE_PACKAGE
#endif // HAS_KABE_TYPE_PACKAGE

// Source: https://codereview.stackexchange.com/questions/107009/easier-user-input-in-c
template <typename T_Input>
T_Input tinput(const kabe::string& prompt)
{
	std::string line{};
	std::cout << prompt;
	if (!std::getline(std::cin, line))
		throw std::istream::failure{ "I/O error" };
	return boost::lexical_cast<T_Input>(line);
}

// using this one and then converting to int or whatever instead of the template 
// version above is probably how things will work in kape lang, kinda like python
kabe::string input(kabe::string prompt = "")
{
	std::string line{};
	std::cout << prompt;
	if (!std::getline(std::cin, line))
		throw std::istream::failure{ "I/O error" };
	return line;
}
