import pyaudio
FORMAT = pyaudio.paInt16
SAMPLES_PER_CHUNK = 4096
CHUNK = SAMPLES_PER_CHUNK
CHANNELS = 1
SAMPLERATE = 44100
THRESHOLD_AMPLIFICATION = 1.2
SLIDWIN_SECONDS = 1
CALIBRATION_RANGE = 15
CHUNKS_PER_SECOND = SAMPLERATE/SAMPLES_PER_CHUNK
PRE_CHUNKS = 2*CHUNKS_PER_SECOND
MAX_SLID_WIN_LEN = int(SLIDWIN_SECONDS*CHUNKS_PER_SECOND)