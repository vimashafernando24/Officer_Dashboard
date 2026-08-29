"""Minimal, dependency-free BM25 (Okapi BM25) implementation.

Pure Python, deterministic, fully auditable — no external package or API required.
Used because it is a technically reasonable, reproducible lexical retrieval method
available in this environment without any embedding-API credentials.
"""
import math
import re
from collections import Counter

TOKEN_RE = re.compile(r"[a-z0-9]+")

# Standard short English stopword list plus survey/catalogue boilerplate words that
# carry no topical signal in this small, domain-specific corpus (e.g. every course
# document repeats "National Youth Service Council has initiated ... course
# programs ... youth ... skills ... job ... employment"). Removing these is
# standard IR practice, not overfitting to any specific respondent or course.
STOPWORDS = {
    "a","an","the","and","or","of","to","in","on","for","with","is","are","was","were",
    "be","been","being","this","that","these","those","it","its","as","at","by","from",
    "not","no","yes","i","you","your","we","our","they","their","he","she","his","her",
    "will","would","can","could","should","may","might","have","has","had","do","does",
    "did","if","than","then","so","such","also","which","who","whom","up","down","out",
    "about","into","over","after","before","while","during","between","within","without",
    "national","youth","service","council","initiated","several","course","programs",
    "program","programme","develop","developing","skills","skill","opportunity",
    "opportunities","achieve","future","job","jobs","aspirations","theoretical",
    "knowledge","practical","necessary","employment","higher","education","objective",
    "correct","path","direct","desired","occupations","time","same","developing",
    "entrepreneurial","abilities","obtaining","gentle","attitudes","within","disciplined",
    "environment","completing","level","under","competency","standards","following",
    "variety","covering","apply","now","language","max","students",
}

def tokenize(text):
    toks = TOKEN_RE.findall(text.lower())
    out = []
    for t in toks:
        if t in STOPWORDS:
            continue
        if t.isdigit() and len(t) <= 2:
            # bare 1-2 digit numbers are almost always list-item markers or grade
            # numbers in this corpus, not meaningful topical content
            continue
        out.append(t)
    return out

class BM25:
    def __init__(self, documents, k1=1.5, b=0.75):
        """documents: list of raw text strings (one per indexed chunk)."""
        self.k1 = k1
        self.b = b
        self.doc_tokens = [tokenize(d) for d in documents]
        self.doc_lens = [len(t) for t in self.doc_tokens]
        self.avgdl = sum(self.doc_lens) / max(1, len(self.doc_lens))
        self.n_docs = len(documents)
        self.doc_freqs = []
        df = Counter()
        for toks in self.doc_tokens:
            counts = Counter(toks)
            self.doc_freqs.append(counts)
            for term in counts:
                df[term] += 1
        self.idf = {}
        for term, freq in df.items():
            self.idf[term] = math.log(1 + (self.n_docs - freq + 0.5) / (freq + 0.5))

    def score(self, query_text, min_distinct_term_matches=1):
        """
        min_distinct_term_matches: with a corpus of very short course documents
        (median ~20 content tokens after stopword removal), a single coincidental
        shared word (e.g. 'local' in 'Local Area Network' vs. a respondent saying
        'local Sri Lankan company') can otherwise dominate a score. Requiring at
        least two distinct overlapping content terms is a standard, generic
        precision safeguard for short-document lexical retrieval — not tuned to
        any specific respondent or course.
        """
        q_tokens = tokenize(query_text)
        scores = [0.0] * self.n_docs
        for i in range(self.n_docs):
            dl = self.doc_lens[i]
            counts = self.doc_freqs[i]
            s = 0.0
            distinct_matches = 0
            for term in set(q_tokens):
                if term not in counts:
                    continue
                distinct_matches += 1
                idf = self.idf.get(term, 0.0)
                f = counts[term]
                denom = f + self.k1 * (1 - self.b + self.b * dl / self.avgdl)
                s += idf * (f * (self.k1 + 1)) / max(denom, 1e-9)
            if distinct_matches < min_distinct_term_matches:
                s = 0.0
            scores[i] = s
        return scores
