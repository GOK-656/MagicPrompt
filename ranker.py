"""
This is the template for implementing the rankers for your search engine.
You will be implementing WordCountCosineSimilarity, DirichletLM, TF-IDF, BM25, Pivoted Normalization, and your own ranker.
"""
from collections import Counter, defaultdict
from indexing import InvertedIndex
import math


class Ranker:
    """
    The ranker class is responsible for generating a list of documents for a given query, ordered by their scores
    using a particular relevance function (e.g., BM25).
    A Ranker can be configured with any RelevanceScorer.
    """
    # TODO: Implement this class properly; this is responsible for returning a list of sorted relevant documents
    def __init__(self, index: InvertedIndex, document_preprocessor, stopwords: set[str], scorer: 'RelevanceScorer') -> None:
        """
        Initializes the state of the Ranker object.

        TODO (HW3): Previous homeworks had you passing the class of the scorer to this function
        This has been changed as it created a lot of confusion.
        You should now pass an instantiated RelevanceScorer to this function.

        Args:
            index: An inverted index
            document_preprocessor: The DocumentPreprocessor to use for turning strings into tokens
            stopwords: The set of stopwords to use or None if no stopword filtering is to be done
            scorer: The RelevanceScorer object
        """
        self.index = index
        self.tokenize = document_preprocessor.tokenize
        self.scorer = scorer
        self.stopwords = stopwords

    def query(self, query: str) -> list[tuple[int, float]]:
        """
        Searches the collection for relevant documents to the query and
        returns a list of documents ordered by their relevance (most relevant first).

        Args:
            query: The query to search for

        Returns:
            A list of dictionary objects with keys "docid" and "score" where docid is
            a particular document in the collection and score is that document's relevance

        TODO (HW3): We are standardizing the query output of Ranker to match with L2RRanker.query and VectorRanker.query
        The query function should return a sorted list of tuples where each tuple has the first element as the document ID
        and the second element as the score of the document after the ranking process.
        """
        # TODO: Tokenize the query and remove stopwords, if needed
        tokens = self.tokenize(query)
        query_parts = [token for token in tokens if token not in self.stopwords] if self.stopwords else tokens
     
        # TODO: Fetch a list of possible documents from the index and create a mapping from
        #       a document ID to a dictionary of the counts of the query terms in that document.
        #       You will pass the dictionary to the RelevanceScorer as input.
        doc_word_counts = defaultdict(Counter)
        query_word_counts = Counter(query_parts)
        for term in query_word_counts:
            postings = self.index.get_postings(term)
            for posting in postings:
                doc_word_counts[posting[0]][term] = posting[1]

        # TODO: Rank the documents using a RelevanceScorer (like BM25 from below classes) 
        results = []
        for docid in doc_word_counts:
            res = self.scorer.score(docid, doc_word_counts[docid], query_word_counts)
            if res:
                results.append((docid, res))

        # TODO: Return the **sorted** results as format [{docid: 100, score:0.5}, {{docid: 10, score:0.2}}]
        results.sort(key=lambda x: x[1], reverse=True)
        return results


class RelevanceScorer:
    """
    This is the base interface for all the relevance scoring algorithm.
    It will take a document and attempt to assign a score to it.
    """
    # TODO: Implement the functions in the child classes (WordCountCosineSimilarity, DirichletLM, BM25,
    #  PivotedNormalization, TF_IDF) and not in this one

    def __init__(self, index: InvertedIndex, parameters) -> None:
        raise NotImplementedError

    def score(self, docid: int, doc_word_counts: dict[str, int], query_word_counts: dict[str, int]) -> float:
        """
        Returns a score for how relevance is the document for the provided query.

        Args:
            docid: The ID of the document
            doc_word_counts: A dictionary containing all words in the document and their frequencies.
                Words that have been filtered will be None.
            query_word_counts: A dictionary containing all words in the query and their frequencies.
                Words that have been filtered will be None.

        Returns:
            A score for how relevant the document is (Higher scores are more relevant.)

        """
        raise NotImplementedError


# TODO (HW1): Implement unnormalized cosine similarity on word count vectors
class WordCountCosineSimilarity(RelevanceScorer):
    def __init__(self, index: InvertedIndex, parameters={}) -> None:
        self.index = index
        self.parameters = parameters

    def score(self, docid: int, doc_word_counts: dict[str, int], query_word_counts: dict[str, int]) -> float:
        # 1. Find the dot product of the word count vector of the document and the word count vector of the query

        # 2. Return the score
        cwq = query_word_counts
        score = 0
        flag = 0
        for word in cwq:
            if word in doc_word_counts:
                flag = 1
                score += cwq[word] * doc_word_counts[word]
        if not flag:
            return None
        return score 


# TODO (HW1): Implement DirichletLM
class DirichletLM(RelevanceScorer):
    def __init__(self, index: InvertedIndex, parameters={'mu': 2000}) -> None:
        self.index = index
        self.parameters = parameters
        self.mu = parameters['mu']

    def score(self, docid: int, doc_word_counts: dict[str, int], query_word_counts: dict[str, int]) -> float:
        # 1. Get necessary information from index

        # 2. Compute additional terms to use in algorithm

        # 3. For all query_parts, compute score

        # 4. Return the score
        cwq = query_word_counts
        q_len = sum(cwq.values())
        flag = 0
        score = 0
        
        for term in cwq:
            if term in doc_word_counts and docid in self.index.document_metadata:
                flag = 1
                pwc = self.index.get_term_metadata(term)['count']/self.index.statistics['total_token_count']
                first_part = cwq[term]*math.log(1+doc_word_counts[term]/(self.mu*pwc))
                score+=first_part
        if docid in self.index.document_metadata:
            second_part = q_len*math.log(self.mu/(self.mu+self.index.document_metadata[docid]['length']))
            score+=second_part
        if not flag:
            return None
        return score


# TODO (HW1): Implement BM25
class BM25(RelevanceScorer):
    def __init__(self, index: InvertedIndex, parameters={'b': 0.75, 'k1': 1.2, 'k3': 8}) -> None:
        self.index = index
        self.b = parameters['b']
        self.k1 = parameters['k1']
        self.k3 = parameters['k3']

    def score(self, docid: int, doc_word_counts: dict[str, int], query_word_counts: dict[str, int])-> float:
        # 1. Get necessary information from index

        # 2. Find the dot product of the word count vector of the document and the word count vector of the query

        # 3. For all query parts, compute the TF and IDF to get a score

        # 4. Return score
        cwq = query_word_counts
        info = self.index.statistics # statistics
        avg_dl = info['mean_document_length']
        N = info['number_of_documents']
        score = 0
        flag = 0
        for term in cwq:
            if term in doc_word_counts and docid in self.index.document_metadata:
                flag = 1
                third_part = cwq[term]*(self.k3+1)/(self.k3+cwq[term])
                first_part = math.log((N+0.5-self.index.get_term_metadata(term)['document_count'])\
                                      /(self.index.get_term_metadata(term)['document_count']+0.5))
                ctd = doc_word_counts[term]
                second_part = ((self.k1+1)*ctd)\
                    /(self.k1*(1-self.b+self.b*self.index.document_metadata[docid]['length']/avg_dl)+ctd)
                score+=first_part*second_part*third_part
        if not flag:
            return None
        return score


# TODO (HW1): Implement Pivoted Normalization
class PivotedNormalization(RelevanceScorer):
    def __init__(self, index: InvertedIndex, parameters={'b': 0.2}) -> None:
        self.index = index
        self.b = parameters['b']

    def score(self, docid: int, doc_word_counts: dict[str, int], query_word_counts: dict[str, int]) -> float:
        # 1. Get necessary information from index

        # 2. Compute additional terms to use in algorithm

        # 3. For all query parts, compute the TF, IDF, and QTF values to get a score

        # 4. Return the score
        cwq = query_word_counts
        info = self.index.statistics # statistics
        avg_dl = info['mean_document_length']
        N = info['number_of_documents']
        score = 0
        flag = 0
        for term in cwq:
            if term in doc_word_counts and docid in self.index.document_metadata:
                flag = 1
                first_part = cwq[term]
                third_part = math.log((N+1)/self.index.get_term_metadata(term)['document_count'])
                second_part = (1+math.log(1+math.log(doc_word_counts[term])))\
                    /(1-self.b+self.b*self.index.document_metadata[docid]['length']/avg_dl)
                # print(first_part, second_part, third_part)
                score+=first_part*second_part*third_part
        if not flag:
            return None
        return score


# TODO (HW1): Implement TF-IDF
class TF_IDF(RelevanceScorer):
    def __init__(self, index: InvertedIndex, parameters={}) -> None:
        self.index = index
        self.parameters = parameters

    def score(self, docid: int, doc_word_counts: dict[str, int], query_word_counts: dict[str, int]) -> float:
        # 1. Get necessary information from index

        # 2. Compute additional terms to use in algorithm

        # 3. For all query parts, compute the TF, IDF, and QTF values to get a score

        # 4. Return the score
        cwq = query_word_counts
        doc_total = self.index.statistics['number_of_documents']  # statistics
        score = 0
        flag = 0
        for term in cwq:
            if term in doc_word_counts:
                flag = 1
                score += math.log(doc_word_counts[term]+1)*\
                    (1+math.log(doc_total/(self.index.get_term_metadata(term)['document_count'])))*cwq[term]
        if not flag:
            return None
        return score
