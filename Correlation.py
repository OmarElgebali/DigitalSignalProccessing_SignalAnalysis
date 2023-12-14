import math

import numpy as np
from FourierTransform import fourier_transform


def direct_correlation_2_signals(signal_value_1, signal_value_2, periodicity):
    def shift_left_signal(signal_v, is_periodic):
        prev_first_element = signal_v.pop(0)
        signal_v.append(prev_first_element if is_periodic else 0)
        return signal_v

    summation_square_of_list = lambda signal: sum([x1 * x1 for x1 in signal])
    calc_normalization_term = lambda signal_1, signal_2, length: math.sqrt(
        summation_square_of_list(signal_1) * summation_square_of_list(signal_2)) / length

    N = len(signal_value_1)
    print("=" * 200)
    print(f"Length (N)                  : {N}")
    normalization_term = calc_normalization_term(signal_value_1, signal_value_2, N)
    print(f"Normalization Term          : {normalization_term}")
    normalized_correlated_signal = []
    for i in range(N):
        r_12 = np.sum([a * b for a, b in zip(signal_value_1, signal_value_2)]) / N
        if periodicity:
            norm_12 = normalization_term
        else:
            norm_12 = calc_normalization_term(signal_value_1, signal_value_2, N)
        normalized_correlated_signal.append(r_12 / norm_12)
        signal_value_2 = shift_left_signal(signal_value_2, periodicity)
    print(f"Normalized Correlated Signal: {normalized_correlated_signal}")
    return normalized_correlated_signal


def fast_correlation_2_signals(signal_value_1, signal_value_2):
    summation_square_of_list = lambda signal: sum([x1 * x1 for x1 in signal])

    N = len(signal_value_1)
    print("=" * 200)
    print(f"Length (N)                  : {N}")

    harmonics_signal_1 = fourier_transform(signal_value_1, -1)
    harmonics_signal_2 = fourier_transform(signal_value_2, -1)
    conjugate_signal_1 = [x_k.conjugate() for x_k in harmonics_signal_1]
    print(f"Conjugate Signal-1          : {conjugate_signal_1}")
    print(f"HarmonicS Signal-2          : {harmonics_signal_2}")

    harmonic_multiplication = [x1_k * x2_k for x1_k, x2_k in zip(conjugate_signal_1, harmonics_signal_2)]
    print(f"Harmonic Multiplication     : {harmonic_multiplication}")

    idft_of_harmonic_multiplication = fourier_transform(harmonic_multiplication, 1)
    correlated_signal = [round(x_n) / N for x_n in idft_of_harmonic_multiplication]
    print(f"Correlated Signal           : {correlated_signal}")

    summation_power_1 = summation_square_of_list(signal_value_1)
    summation_power_2 = summation_square_of_list(signal_value_2)
    normalization_term = math.sqrt(summation_power_1 * summation_power_2) / N
    print(f"Normalization Term          : {normalization_term}")

    normalized_correlated_signal = [r_1_2 / normalization_term for r_1_2 in correlated_signal]
    print(f"Normalized Correlated Signal: {normalized_correlated_signal}")
    print("=" * 200)

    return normalized_correlated_signal
