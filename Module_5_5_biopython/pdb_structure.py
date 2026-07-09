# Download a real PDB structure using PDBList (try 1CRN — crambin, a small protein, good for learning).
# Parse it and print: the number of chains, total residues per chain, and the name and coordinates of
# the first atom in each chain.

# Describe the problem in plain English: Use PDBList() function to download 1CRN structure, parse the structure and print it's structural features.
# What do I need to do? Download 1CRN structure, parse the structure and print it's structural features
# What's the primitive operation? Get 1CRN structure and show it's features
# What Python tool does exactly that? PDBList(), PDBParser()

from Bio.PDB import PDBParser, PDBList

# Download 1CRN structure
pdbl = PDBList()
pdbl.retrieve_pdb_file("1CRN", pdir="./pdb_files", file_format="pdb")

# Parse the structure
parser = PDBParser(QUIET=True)   # QUIET suppresses warnings
structure = parser.get_structure("1CRN", "./pdb_files/pdb1crn.ent")

# Print structural features: No. of chains, total residues per chain, Name and coordinates of the first atom in each chain
# Navigate the structure hierarchy: Structure → Model → Chain → Residue → Atom
for model in structure:
  for chain in model:
    print(f"Number of chains: {len(list(model.get_chains()))} chains.")
    print(f"Chain {chain.id}: {len(list(chain.get_residues()))} residues")
    for residue in chain:
      for atom in residue:
        print(atom.name, atom.coord)
        break    # Get only first atom per residue
      break
    break


