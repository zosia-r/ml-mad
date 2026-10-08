#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
import math
import pytest

# nalezy uzupelnic implementacje w miejscach #...

# Klasa Dual pozwala wykonywac tylko dzialania na obiektach Dual,
# wiec np. chcac pomnozyc x (typu Dual) przez 2, musimy pisac
#   x * Dual(2.0, 0.0)
class Dual:
    def __init__(self, real, dual):
        self.real = real
        self.dual = dual

    def __add__(self, other):
        return Dual(self.real + other.real, self.dual + other.dual)
    
    def __sub__(self, other):
        # ...
        pass
    
    def __mul__(self, other):
        # ...
        pass

    def __truediv__(self, other):
        # ...
        pass

    def __neg__(self):
        # ...
        pass

def sin(x):
    # Mamy wzor:
    #   (sin(x))' = cos(x) * x'
    # skad wynika postac czesci dualnej.
    return Dual(math.sin(x.real), math.cos(x.real) * x.dual)

def cos(x):
    # ...
    pass

def exp(x):
    # ...
    pass

# jeszcze jakas funkcja, np. sqrt, log, itp.
# def ...(x):
#   ...

def f(x):
    # Jakas wlasna funkcja do narysowania, uzywajaca tych powyzej
    return Dual(2.0, 0.0) + x   # nudna funkcja, ale po dodaniu implementacji powyzej mozna zmienic


if __name__ == "__main__":
    # przykladowa dziedzina, mozna zmienic w zaleznosci od wybranej funkcji
    x_vals = np.linspace(-10, 10, 400)

    # tutaj po prostu rysujemy, nie trzeba zmieniac
    y_vals = []
    dy_vals = []

    for x in x_vals:
        x_dual = Dual(x, dual=1.0)
        result = f(x_dual)
        y_vals.append(result.real)   # f(x)
        dy_vals.append(result.dual)  # f'(x)


    plt.figure(figsize=(10, 5))
    plt.plot(x_vals, y_vals, label=r"$f(x)$", color="blue", linewidth=2)
    plt.plot(x_vals, dy_vals, label=r"$f'(x)$ (Auto-Diff)", color="red", linestyle="--", linewidth=2)

    plt.axhline(0, color="black", linewidth=0.8, linestyle=":")
    plt.axvline(0, color="black", linewidth=0.8, linestyle=":")
    plt.title("Funkcja i jej pochodna", fontsize=14)
    plt.xlabel("x", fontsize=12)
    plt.ylabel("y", fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.legend(fontsize=11)
    plt.tight_layout()
    plt.show()


def test_cos():
    funkcja = lambda x : x * cos(x)
    pochodna = lambda x : cos(x) - x * sin(x)
    x_vals = np.linspace(-10, 10, 400)
    for x in x_vals:
        x_dual = Dual(x, dual=1.0)
        result = funkcja(x_dual)
        expected = pochodna(x_dual)
        assert result.dual == pytest.approx(expected.real, rel=1e-6)

def test_cosx2():
    funkcja = lambda x : x * cos(x * x)
    pochodna = lambda x : cos(x * x) - Dual(2.0, 0.0) * x * x * sin(x * x)
    x_vals = np.linspace(-10, 10, 400)
    for x in x_vals:
        x_dual = Dual(x, dual=1.0)
        result = funkcja(x_dual)
        expected = pochodna(x_dual)
        assert result.dual == pytest.approx(expected.real, rel=1e-6)

def test_dzielenie():
    sigmoid = lambda x : Dual(1.0, 0.0) / (Dual(1.0, 0.0) + exp(-x))
    pochodna = lambda x : sigmoid(x) * (Dual(1.0, 0.0) - sigmoid(x))
    x_vals = np.linspace(-10, 10, 400)
    for x in x_vals:
        x_dual = Dual(x, dual=1.0)
        result = sigmoid(x_dual)
        expected = pochodna(x_dual)
        assert result.dual == pytest.approx(expected.real, rel=1e-6)

def test_wlasnej_funkcji():
    # 
    pass
                        