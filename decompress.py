import sys
import code

def main(args):
	if len(args) != 2:
		sys.exit("Usage: python arithmetic-decompress.py InputFile OutputFile")
	inputfile, outputfile = args
	decrypt_file = code.Encrypt("decrypt", inputfile)

	with open(outputfile, "wb") as out, open(inputfile, "rb") as inp:
		bitin = code.BitInputStream(inp)
		freqs = read_frequencies(bitin)
		decompress(freqs, bitin, out)

def read_frequencies(bitin):
	def read_int(n):
		result = 0
		for _ in range(n):
			result = (result << 1) | bitin.read_no_eof()
		return result
	
	freqs = [read_int(32) for _ in range(256)]
	freqs.append(1)
	return code.SimpleFrequencyTable(freqs)

def decompress(freqs, bitin, out):
	dec = code.ArithmeticDecoder(32, bitin)
	while True:
		symbol = dec.read(freqs)
		if symbol == 256:
			break
		out.write(bytes((symbol,)))

if __name__ == "__main__":
	main(sys.argv[1 : ])
