import math


# Use to test the Amplitude of DFT and IDFT
def SignalComapreAmplitude(SignalInput, SignalOutput):
    if len(SignalInput) != len(SignalOutput):
        return False
    else:
        for i in range(len(SignalInput)):
            if abs(SignalInput[i] - SignalOutput[i]) > 0.001:
                return False
        return True


def RoundPhaseShift(P):
    while P < 0:
        P += 2 * math.pi
    return float(P % (2 * math.pi))


# Use to test the PhaseShift of DFT
def SignalComparePhaseShift(SignalInput, SignalOutput):
    rounded_input_phase_shifts = [RoundPhaseShift(p) for p in SignalInput]
    rounded_output_phase_shifts = [RoundPhaseShift(p) for p in SignalOutput]
    if len(rounded_input_phase_shifts) != len(rounded_output_phase_shifts):
        return False
    else:
        for i in range(len(rounded_input_phase_shifts)):
            if abs(rounded_input_phase_shifts[i] - rounded_output_phase_shifts[i]) > 0.0001:
                return False
        return True


def SignalCompare(InputAmplitude, OutputAmplitude, InputPhaseShift, OutputPhaseShift):
    if not SignalComapreAmplitude(InputAmplitude, OutputAmplitude):
        print('<Test case failed - Comparing Phase Shift>')
        return
    if not SignalComparePhaseShift(InputPhaseShift, OutputPhaseShift):
        print('<Test case failed - Comparing Amplitude>')
        return
    print("<Test case passed successfully>")
