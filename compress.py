import contextlib, sys
import code

def main(args):
	if len(args) != 2:
		sys.exit("Usage: python arithmetic-compress.py InputFile OutputFile")
	inputfile, outputfile = args
	freqs = get_frequencies(inputfile)
	freqs.increment(256)
	with open(inputfile, "rb") as inp, \
			contextlib.closing(code.BitOutputStream(open(outputfile, "wb"))) as bitout:
		write_frequencies(bitout, freqs)
		compress(freqs, inp, bitout, outputfile)

	encryptFile = code.Encrypt("encrypt", outputfile)

def get_frequencies(filepath):
	freqs = code.SimpleFrequencyTable([0] * 257)
	with open(filepath, "rb") as input:
		while True:
			b = input.read(1)
			if len(b) == 0:
				break
			freqs.increment(b[0])
	return freqs

def write_frequencies(bitout, freqs):
	for i in range(256):
		write_int(bitout, 32, freqs.get(i))

def compress(freqs, inp, bitout, outputfile):
	enc = code.ArithmeticEncoder(32, bitout)
	while True:
		symbol = inp.read(1)
		if len(symbol) == 0:
			break
		enc.write(freqs, symbol[0])
	enc.write(freqs, 256)
	enc.finish()

def write_int(bitout, numbits, value):
	for i in reversed(range(numbits)):
		bitout.write((value >> i) & 1)

if __name__ == "__main__":
	main(sys.argv[1 : ])
