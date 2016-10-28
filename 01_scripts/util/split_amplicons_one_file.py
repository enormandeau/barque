#!/usr/bin/env python
#!/usr/bin/env python

"""Split amplicons using forward and reverse potentially degenerated primers

Usage:
    %program fastq_file primer_file iupac_file output_folder
"""

# Importing modules
import gzip
import sys
import re
import os

# Defining classes
class Fastq(object):
    """Fastq object with name and sequence
    """
    def __init__(self, name, seq, name2, qual):
        self.name = name
        self.seq = seq
        self.name2 = name2
        self.qual = qual
    def write_to_file(self, handle):
        handle.write("@" + self.name + "\n")
        handle.write(self.seq + "\n")
        handle.write("+" + self.name2 + "\n")
        handle.write(self.qual + "\n")
    def __repr__(self):
        return "\t".join([self.seq[0:51], self.seq[0:51]])

# Defining functions
def myopen(infile, mode="r"):
    if infile.endswith(".gz"):
        return gzip.open(infile, mode=mode)
    else:
        return open(infile, mode=mode)
        
def fastq_iterator(input_file):
    """Takes a fastq file infile and returns a fastq object iterator
    """
    with myopen(input_file) as f:
        while True:
            name = f.readline().strip()[1:]
            if not name:
                break
            seq = f.readline().strip()
            name2 = f.readline().strip()[1:]
            qual = f.readline().strip()
            yield Fastq(name, seq, name2, qual)

def reverse_complement(seq):
    complement =  {
            "A":"T",
            "C":"G",
            "G":"C",
            "T":"A",
            "[":"]",
            "]":"[",
            "(":")",
            ")":"("
            }

    comp = []
    for s in seq:
        if s in complement:
            comp.append(complement[s])
        else:
            comp.append(s)

    return "".join(comp[::-1])

def replace_iupac(seq):
    temp = []
    for s in seq:
        if s in iupac:
            temp.append(iupac[s])
        else:
            temp.append(s)

    return "".join(temp)

# Parsing user input
try:
    fastq_file = sys.argv[1]
    primer_file = sys.argv[2]
    iupac_file = sys.argv[3]
    output_folder = sys.argv[4]
except:
    print __doc__
    sys.exit(0)

# Main
## parse iupac
iupac = {}
with open(iupac_file) as pfile:
    for line in pfile:
        name, sequence = line.strip().split("\t")
        iupac[name] = sequence

## Parse primers
primers = {}
with open(primer_file) as pfile:
    for line in pfile:
        # Skip comment lines
        if line.startswith("#"):
            continue

        # Get primer infos
        name, forward, reverse, min_length, database = line.strip().split("\t")
        forward_length = len(forward)
        reverse_length = len(reverse)

        # Permit dropout at the 3 last bases of the reverse primer sequence
        reverse = "}3,{." + reverse[3:]
        forward = ".{,3}" + forward[3:]

        # Replace iupac characters
        forward = replace_iupac(forward)
        reverse = replace_iupac(reverse)
        reverse = reverse_complement(reverse)

        # Create the regex
        forward = "^" + forward
        reverse = reverse + "$"

        primers[name] = (re.compile(forward), re.compile(reverse), min_length, forward_length, reverse_length)

## Open output fastq.gz files
output_files = {}
input_file = os.path.basename(fastq_file)

# Add fake primers to automatically open file handles
primers["not_found"] = "FAKE"
primers["too_short"] = "FAKE"
primers["forward_only"] = "FAKE"

# Open output file handles
for p in primers:
    output_files[p] = myopen(
            os.path.join(
                output_folder,
                input_file.replace(".fastq", "_" + p + ".fastq")
                )
            , "w")

## Read fastq file
sequences = fastq_iterator(fastq_file)
num = 0
count = 0
for s in sequences:
    count += 1
    sequence_found = False

    for p in primers:
        # Skip fake primers
        if primers[p] == "FAKE":
            continue

        forward, reverse, min_length, forward_length, reverse_length = primers[p]

        # Filter short amplicons
        if len(s.seq) - forward_length - reverse_length < int(min_length):
            s.write_to_file(output_files["too_short"])
            sequence_found = True

        else:
            # Look for forward primer
            forward_found = forward.findall(s.seq)

            if len(forward_found) >= 1:
                # Look for reverse primer
                reverse_found = reverse.findall(s.seq)

                if len(reverse_found) >= 1:
                    # Remove forward primer (+ trim quality)
                    s.seq = re.sub(forward_found[0], "", s.seq)
                    length = len(forward_found[0])
                    s.qual = s.qual[length:]

                    # Remove reverse primer (+ trim quality)
                    s.seq = re.sub(reverse_found[0], "", s.seq)
                    length = len(s.seq)
                    s.qual = s.qual[:length]

                    # Adjust tracking params
                    num += 1
                    sequence_found = True

                    # Write to file
                    s.write_to_file(output_files[p])

                else:
                    # Write to special file
                    s.write_to_file(output_files["forward_only"])

    if not sequence_found:
        s.write_to_file(output_files["not_found"])

## Report success
print "Assigned {}% ({}/{}) of the sequences to an amplicon ({})".format(str(100.0 *float(num)/count)[0:4], num, count, fastq_file)

## Close file handles
for f in output_files:
    output_files[f].close()
