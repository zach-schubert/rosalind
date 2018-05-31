import requests
from io import StringIO
from lxml import html
from Bio import SeqIO
from skbio import TabularMSA, DNA
from rosalind.utils import solves, entrez_fetch


@solves('http://rosalind.info/problems/gbk/')
def genbank_introduction(genus=None, from_pub_date=None, to_pub_date=None, dataset=None):
    """
    Problem
    GenBank comprises several subdivisions:

    Nucleotide: a collection of nucleic acid sequences from several sources.
    Genome Survey Sequence (GSS): uncharacterized short genomic sequences.
    Expressed Sequence Tags, (EST): uncharacterized short cDNA sequences.
    Searching the Nucleotide database with general text queries will produce the most relevant results.
    You can also use a simple query based on protein name, gene name or gene symbol.

    To limit your search to only certain kinds of records, you can search using GenBank's Limits page or alternatively
    use the Filter your results field to select categories of records after a search.

    If you cannot find what you are searching for, check how the database interpreted your query by investigating the
    Search details field on the right side of the page. This field automatically translates your search into standard
    keywords.

    For example, if you search for Drosophila, the Search details field will contain (Drosophila[All Fields]), and you
    will obtain all entries that mention Drosophila (including all its endosymbionts). You can restrict your search to
    only organisms belonging to the Drosophila genus by using a search tag and searching for Drosophila[Organism].

    Given: A genus name, followed by two dates in YYYY/M/D format.

    Return: The number of Nucleotide GenBank entries for the given genus that were published between the dates
    specified.
    """
    if dataset:
        genus, from_pub_date, to_pub_date = (dataset or '').split('\n')
    term = '(({genus}[Organism]) AND ("{from_pub_date}"[Publication Date] : "{to_pub_date}"[Publication Date]))'
    term = term.format(genus=genus, from_pub_date=from_pub_date, to_pub_date=to_pub_date)
    response = requests.get('https://www.ncbi.nlm.nih.gov/nuccore', params={'term': term})
    doc = html.fromstring(response.content)
    results = doc.xpath(".//div[@id='maincontent']//div[@class='rslt']")
    return len(results)


@solves("http://rosalind.info/problems/frmt/")
def data_formats(genbank_ids=None, dataset=None):
    """
    Problem
    Given: A collection of n (n≤10) GenBank entry IDs.

    Return: The shortest of the strings associated with the IDs in FASTA format.
    """
    genbank_ids = genbank_ids or (dataset or '').split(' ')
    handle = entrez_fetch(db="nucleotide", id=genbank_ids, rettype="fasta")
    records = list(SeqIO.parse(handle, "fasta"))
    min_length = min(len(record.seq) for record in records)
    record = next(record for record in records if len(record.seq) == min_length)
    return record.format("fasta")


@solves("http://rosalind.info/problems/tfsq/")
def fastq_to_fasta(dataset):
    """
    http://rosalind.info/problems/tfsq/

    Problem
    Sometimes it's necessary to convert data from FASTQ format to FASTA format. For example, you may want to perform a
    BLAST search using reads in FASTQ format obtained from your brand new Illumina Genome Analyzer.

    Given: FASTQ file

    Return: Corresponding FASTA records
    """
    msa = TabularMSA.read(StringIO(dataset), constructor=DNA, variant='illumina1.8')
    fasta = msa.write(StringIO(), format='fasta').getvalue()
    return fasta
