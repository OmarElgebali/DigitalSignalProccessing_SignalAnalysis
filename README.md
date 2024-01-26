# DigitalSignalProccessing_SignalAnalysis
## Feature Descriptions:
### Task 1: Signal Generation and Display
This feature allows the user to read samples of a signal from a text file and display it in both continuous and discrete representations. Additionally, it provides the ability to generate sinusoidal or cosinusoidal signals with customizable parameters.

### Task 2: Arithmetic Operations
This menu includes various arithmetic operations like addition, subtraction, multiplication, squaring, shifting, normalization, and accumulation on input signals.

### Task 3: Signal Quantization
This feature enables the quantization of input signals. The user is prompted to input either the number of levels or the number of bits available. The application then displays the quantized signal and quantization error.

### Task 4: Frequency Domain Operations
This menu allows the application of Fourier Transform to any input signal. It displays frequency versus amplitude and frequency versus phase relations. Users can modify amplitude and phase, save frequency components to a file, and reconstruct the signal using IDFT.

### Task 5: Discrete Cosine Transform (DCT)
This feature computes DCT for a given input signal, displays the result, and allows the user to choose the first m coefficients to be saved in a text file, also allowing removing the DC component of an input signal.

### Task 6: Time Domain Operations
This menu includes operations like smoothing, sharpening, delaying, advancing, folding, delaying/advancing a folded signal, and removing the DC component in the frequency domain.

### Task 7: Convolution and DC Removal in Time Domain
This menu provides the ability to convolve two signals and remove the DC component.

### Task 8: Correlation Operations
This menu includes features like computing normalized cross-correlation, time delay analysis, and template matching.

### Task 9: Fast Convolution and Correlation in Frequency Domain
This feature implements the fast method for convoluting and correlating two signals in the frequency domain using DFT and IDFT.

## File Structure:
- **DSP_Main.py:** The main program that integrates all the features, menus, and GUI.

- **FourierTransform.py:** A module containing the Fourier Transform methods for Transformation `(TD -> FD & FD -> TD)`.

- **HelperResources.py:** A module with utility functions for reading/writing signals, performing operations, and handling signal input structure.

- **Correlation.py:** A module containing the Correlation fast (Frequency Domain) and direct (Time Domain) methods.

- **\TaskFunctions:** The Folder has test functions for each feature described.

- **\TestCases:** The Folder includes test cases for each feature described.
