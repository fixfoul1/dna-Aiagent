"""
DNA Mutation Detection & Analysis Toolkit
"""

from Bio import SeqIO
from Bio.Seq import Seq
from Bio.Align import PairwiseAligner
from Bio.Data import CodonTable


def calculate_gc_content(sequence: str) -> float:
    """Calculates the GC content percentage of a DNA sequence."""
    seq_str = sequence.upper().strip()
    if not seq_str:
        return 0.0
    
    gc_total = seq_str.count('G') + seq_str.count('C')
    return round((gc_total / len(seq_str)) * 100, 2)


def get_reverse_complement(sequence: str) -> str:
    """Returns the reverse complement of a DNA sequence."""
    clean_seq = Seq(sequence.upper().strip())
    return str(clean_seq.reverse_complement())


def translate_dna(sequence: str, frame: int = 0) -> str:
    """Translates a DNA sequence into a protein sequence starting from frame 0, 1, or 2."""
    clean_seq = sequence.upper().strip()[frame:]
    trim_len = len(clean_seq) - (len(clean_seq) % 3)
    trimmed_seq = Seq(clean_seq[:trim_len])
    return str(trimmed_seq.translate(to_stop=False))


def find_mutations(ref_seq: str, mut_seq: str, is_coding: bool = False) -> dict:
    """Aligns reference and mutant DNA sequences and identifies substitutions, insertions, and deletions."""
    aligner = PairwiseAligner()
    aligner.mode = 'global'
    aligner.match_score = 2
    aligner.mismatch_score = -1
    aligner.open_gap_score = -2
    aligner.extend_gap_score = -0.5

    alignments = aligner.align(ref_seq.upper(), mut_seq.upper())
    best_alignment = alignments[0]
    
    ref_aligned, mut_aligned = best_alignment[0], best_alignment[1]
    mutations = []
    ref_idx = 0
    mut_idx = 0

    for i in range(len(ref_aligned)):
        r_char = ref_aligned[i]
        m_char = mut_aligned[i]

        if r_char != m_char:
            mutation_info = {
                "alignment_position": i + 1,
                "ref_pos": ref_idx + 1 if r_char != '-' else None,
                "mut_pos": mut_idx + 1 if m_char != '-' else None,
                "ref_base": r_char,
                "mut_base": m_char,
            }

            if r_char == '-':
                mutation_info["type"] = "insertion"
            elif m_char == '-':
                mutation_info["type"] = "deletion"
            else:
                mutation_info["type"] = "substitution"

            mutations.append(mutation_info)

        if r_char != '-':
            ref_idx += 1
        if m_char != '-':
            mut_idx += 1

    return {
        "alignment_score": float(best_alignment.score),
        "total_mutations": len(mutations),
        "mutations": mutations
    }


if __name__ == "__main__":
    ref = "ATGCGATCGTAA"
    mut = "ATGCAATCGTAA"
    print("GC Content:", calculate_gc_content(ref), "%")
    print("Reverse Comp:", get_reverse_complement(ref))
    print("Mutations:", find_mutations(ref, mut))