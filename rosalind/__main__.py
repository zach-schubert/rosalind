import sys
import argparse
from rosalind import armory, stronghold
from rosalind.utils import SOLVERS

p = argparse.ArgumentParser()
p.add_argument('problem_url')
p.add_argument('-u', dest='rosalind_user', help="Your rosalind.info username.")
p.add_argument('-p', dest='rosalind_password', help="Your rosalind.info password.")
p.add_argument('-e', dest='entrez_email', nargs='?', help="An optional email account to use for Entrez searches.")
args = p.parse_args()

SOLVERS[args.problem_url.strip()](
    rosalind_user=args.rosalind_user,
    rosalind_password=args.rosalind_password,
    entrez_email=args.entrez_email
)
