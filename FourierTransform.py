import cmath
import math
from HelperResources import round_complex

def dft(time_domain_signal):
    harmonics = []
    N = len(time_domain_signal)
    for k in range(N):
        x_k_n = 0
        for n, x_n in enumerate(time_domain_signal):
            power_term = 2 * k * n / N
            pi_factor = power_term * math.pi
            img_term = math.cos(pi_factor) - complex(0, math.sin(pi_factor))
            x_k_n += x_n * img_term
        harmonics.append(x_k_n)

    print("=" * 200)
    print(f"N : {N}")
    print(f"Signal Values   X(n): {time_domain_signal}")
    print(f"Harmonics       X(k): {harmonics}")
    print("=" * 200)
    return harmonics


def idft(freq_domain_signal):
    signal_value = []
    for a, theta in freq_domain_signal:
        real_part = a * cmath.cos(theta)
        imaginary_part = a * cmath.sin(theta)
        signal_value.append(complex(real_part, imaginary_part))

    IDFT_component = []
    signal_length = len(signal_value)
    n_values = [i for i in range(0, signal_length)]
    for n in n_values:
        current_value = 0
        for k, value in enumerate(signal_value):
            current_value += (value * pow(math.e, ((1j * 2 * math.pi * n * k) / signal_length)))
            # print(f'value {k} : {current_value}')
        # print("-" * 50)
        IDFT_component.append(round_complex(current_value).real * (1 / signal_length))

    print(f'signal_value : {signal_value}')
    print(f'IDF : {IDFT_component}')
    print(f'len : {len(IDFT_component)}')
    print(f'first value in IDFT: {abs(IDFT_component[0])}')
    print(f'first value in IDFT: {abs(IDFT_component[1])}')
    print(f'first value in IDFT: {abs(IDFT_component[2])}')
    print(f'first value in IDFT: {abs(IDFT_component[3])}')
    return IDFT_component


def fourier_transform(signal_value, img_factor):
    harmonics = []
    N = len(signal_value)
    for k in range(N):
        x_k_n = 0
        for n, x_n in enumerate(signal_value):
            power_term = 2 * k * n / N
            pi_factor = power_term * math.pi
            img_term = math.cos(pi_factor) + img_factor * complex(0, math.sin(pi_factor))
            x_k_n += x_n * img_term
        if img_factor > 0:
            x_k_n = x_k_n.real / N
        harmonics.append(x_k_n)
    return harmonics
