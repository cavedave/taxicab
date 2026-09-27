CXX      ?= g++
UNAME_S  := $(shell uname -s)
LIBOMP   := $(shell brew --prefix libomp 2>/dev/null)

ifeq ($(UNAME_S),Darwin)
  ifneq ($(LIBOMP),)
    OMPFLAGS := -Xpreprocessor -fopenmp -I$(LIBOMP)/include -L$(LIBOMP)/lib -lomp
  else
    OMPFLAGS :=
  endif
else
  OMPFLAGS := -fopenmp
endif

CXXFLAGS ?= -O3 -std=c++17 -march=native $(OMPFLAGS)

.PHONY: all clean test

all: engine_b9

engine_b9: engine_b9.cpp
	$(CXX) $(CXXFLAGS) -o $@ $<

test: engine_b9
	./engine_b9 --selftest

clean:
	rm -f engine_b9
