def sort_2_lists(list_1, list_2):
    combined_lists = list(zip(list_1, list_2))
    combined_lists.sort(key=lambda l: l[0])
    x, y = zip(*combined_lists)
    x = list(x)
    y = list(y)
    return x, y


def extend_signal_calculation(signal_t, signal_val, new_max_length):
    signal_val = signal_val + [0] * (new_max_length - len(signal_val))
    signal_t.extend(range(len(signal_t), new_max_length))
    return signal_t, signal_val


def extend_signals(list_signal_times, list_signal_values):
    signal_lengths = [len(signal) for signal in list_signal_times]
    max_len = max(signal_lengths)
    number_of_signals = len(signal_lengths)
    current_signal = 0
    while current_signal <= number_of_signals - 1:
        list_signal_values[current_signal], list_signal_times[current_signal] = extend_signal_calculation(
            list_signal_values[current_signal], list_signal_times[current_signal], max_len)
        current_signal += 1
    return list_signal_times, list_signal_values


def read_only_signal(signal_file_path):
    with open(signal_file_path, 'r') as file:
        file.readline()
        file.readline()
        file.readline()
        lines = file.readlines()
        signal_time = []
        signal_value = []
        for line in lines:
            parts = line.split()
            signal_time.append(float(parts[0]))
            signal_value.append(float(parts[1]))
    return signal_time, signal_value


def round_complex(c):
    real = round(c.real, 2)
    imag = round(c.imag, 2)
    return complex(real, imag)


def save_freq_domain_signal(amplitudes, phase_shifts, signal_file_path):
    freq_domain_signal = [(amp, phase) for amp, phase in zip(amplitudes, phase_shifts)]
    # freq_domain_signal = [(amplitudes[i], phase_shifts[i]) for i in range(len(amplitudes))]
    with open(signal_file_path, 'w') as file:
        file.write(f"1\n")
        file.write(f"0\n")
        file.write(f"{len(amplitudes)}\n")
        for amp, phase in freq_domain_signal:
            file.write(f"{amp} {phase}\n")


def save_time_domain_signal(signal_values, signal_file_path):
    with open(signal_file_path, 'w') as file:
        file.write(f"0\n")
        file.write(f"0\n")
        file.write(f"{len(signal_values)}\n")
        for time, value in enumerate(signal_values):
            file.write(f"{time} {value}\n")


def read_polar_signal(path):
    with open(path, 'r') as file:
        file.readline()
        file.readline()
        file.readline()
        lines = file.readlines()
    data_tuples = []
    for line in lines:
        columns = line.strip().split()
        amplitude_init = columns[0]
        phase_shift_init = columns[1]
        amplitude = float(amplitude_init.rstrip('f')) if amplitude_init.endswith('f') else float(amplitude_init)
        phase_shift = float(phase_shift_init.rstrip('f')) if phase_shift_init.endswith('f') else float(
            phase_shift_init)
        data_tuple = (amplitude, phase_shift)
        data_tuples.append(data_tuple)
    return data_tuples
