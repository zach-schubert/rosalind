from rosalind.utils import solves


@solves('http://rosalind.info/problems/dna/')
def counting_dna_nucleotides(dataset=None):
    """
    Problem
    Given: A DNA string s of length at most 1000 nt.

    Return: Four integers (separated by spaces) counting the respective number of times that the
    symbols 'A', 'C', 'G', and 'T' occur in s.
    """
    counts = [dataset.count(nuc) for nuc in 'ACGT']
    return ' '.join(map(str, counts))


@solves('http://rosalind.info/problems/rna/')
def transcribing_dna_into_rna(dataset=None):
    """
    Problem
    Given: A DNA string t having length at most 1000 nt.

    Return: The transcribed RNA string of t.
    """
    return dataset.replace('T', 'U')


@solves('http://rosalind.info/problems/revc/')
def complementing_a_strand_of_dna(dataset=None):
    """
    Problem
    Given: A DNA string s of length at most 1000 bp.

    Return: The reverse complement sc of s.
    """
    rc = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}
    return ''.join(rc[nuc] for nuc in dataset[::-1])
