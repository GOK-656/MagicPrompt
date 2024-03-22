from enum import Enum
import json
import os
from tqdm import tqdm
from collections import Counter, defaultdict
from document_preprocessor import Tokenizer
import gzip


class IndexType(Enum):
    # The three types of index currently supported are InvertedIndex, PositionalIndex and OnDiskInvertedIndex
    InvertedIndex = 'BasicInvertedIndex'
    # NOTE: You don't need to support the following three
    PositionalIndex = 'PositionalIndex'
    OnDiskInvertedIndex = 'OnDiskInvertedIndex'
    SampleIndex = 'SampleIndex'


class InvertedIndex:
    def __init__(self) -> None:
        """
        The base interface representing the data structure for all index classes.
        The functions are meant to be implemented in the actual index classes and not as part of this interface.
        """
        self.statistics = defaultdict(Counter)  # Central statistics of the index
        self.index = {}  # Index
        self.document_metadata = {}  # Metadata like length, number of unique tokens of the documents

    # NOTE: The following functions have to be implemented in the three inherited classes and not in this class

    def remove_doc(self, docid: int) -> None:
        """
        Removes a document from the index and updates the index's metadata on the basis of this
        document's deletion.

        Args:
            docid: The id of the document
        """
        # TODO: Implement this to remove a document from the entire index and statistics
        raise NotImplementedError

    def add_doc(self, docid: int, tokens: list[str]) -> None:
        """
        Adds a document to the index and updates the index's metadata on the basis of this
        document's addition (e.g., collection size, average document length).

        Args:
            docid: The id of the document
            tokens: The tokens of the document
                Tokens that should not be indexed will have been replaced with None in this list.
                The length of the list should be equal to the number of tokens prior to any token removal.
        """
        # TODO: Implement this to add documents to the index
        raise NotImplementedError

    def get_postings(self, term: str) -> list[tuple[int, int]]:
        """
        Returns the list of postings, which contains (at least) all the documents that have that term.
        In most implementation, this information is represented as list of tuples where each tuple
        contains the docid and the term's frequency in that document.
        
        Args:
            term: The term to be searched for

        Returns:
            A list of tuples containing a document id for a document
            that had that search term and an int value indicating the term's frequency in 
            the document
        """
        # TODO: Implement this to fetch a term's postings from the index
        raise NotImplementedError

    def get_doc_metadata(self, doc_id: int) -> dict[str, int]:
        """
        For the given document id, returns a dictionary with metadata about that document.
        Metadata should include keys such as the following:
            "unique_tokens": How many unique tokens are in the document (among those not-filtered)
            "length": how long the document is in terms of tokens (including those filtered)

        Args:
            docid: The id of the document

        Returns:
            A dictionary with metadata about the document
        """
        # TODO: Implement to fetch a particular document stored in metadata
        raise NotImplementedError

    def get_term_metadata(self, term: str) -> dict[str, int]:
        """
        For the given term, returns a dictionary with metadata about that term in the index.
        Metadata should include keys such as the following:
            "count": How many times this term appeared in the corpus as a whole

        Args:
            term: The term to be searched for

        Returns:
            A dictionary with metadata about the term in the index
        """
        # TODO: Implement to fetch a particular term stored in metadata
        raise NotImplementedError

    def get_statistics(self) -> dict[str, int]:
        """
        Returns a dictionary mapping statistical properties (named as strings) about the index to their values.  
        Keys should include at least the following:
            "unique_token_count": how many unique terms are in the index
            "total_token_count": how many total tokens are indexed including filterd tokens), 
                i.e., the sum of the lengths of all documents
            "stored_total_token_count": how many total tokens are indexed excluding filterd tokens
            "number_of_documents": the number of documents indexed
            "mean_document_length": the mean number of tokens in a document (including filter tokens)

        Returns:
              A dictionary mapping statistical properties (named as strings) about the index to their values
        """
        # TODO: Calculate statistics like 'unique_token_count', 'total_token_count',
        #       'number_of_documents', 'mean_document_length' and any other relevant central statistic
        raise NotImplementedError

    def save(self, index_directory_name: str) -> None:
        """
        Saves the state of this index to the provided directory.
        The save state should include the inverted index as well as
        any metadata need to load this index back from disk.

        Args:
            index_directory_name: The name of the directory where the index will be saved
        """
        # TODO: Save the index files to disk
        raise NotImplementedError

    def load(self, index_directory_name: str) -> None:
        """
        Loads the inverted index and any associated metadata from files located in the directory.
        This method will only be called after save() has been called, so the directory should
        match the filenames used in save().

        Args:
            index_directory_name: The name of the directory that contains the index
        """
        # TODO: Load the index files from disk to a Python object
        raise NotImplementedError


class BasicInvertedIndex(InvertedIndex):
    def __init__(self) -> None:
        """
        An inverted index implementation where everything is kept in memory
        """
        super().__init__()
        self.statistics['index_type'] = 'BasicInvertedIndex'
        # For example, you can initialize the index and statistics here:
        #    self.statistics['docmap'] = {}
        #    self.index = defaultdict(list)
        #    self.doc_id = 0
        self.statistics['term_metadata'] = defaultdict(list)
        self.statistics['unique_token_count'] = 0
        self.statistics['total_token_count'] = 0
        self.statistics['stored_total_token_count'] = 0
        self.statistics['number_of_documents'] = 0
        self.statistics['mean_document_length'] = 0
        self.index = defaultdict(list)
  
    # TODO: Implement all the functions mentioned in the interface
    # This is the typical inverted index where each term keeps track of documents and the term count per document
    def remove_doc(self, docid: int) -> None:
        # TODO implement this to remove a document from the entire index and statistics
        for token in self.index:
            for i, (doc, count) in enumerate(self.index[token]):
                if doc == docid:
                    self.index[token].pop(i)
                    self.statistics['stored_total_token_count'] -= count
                    self.statistics['term_metadata'][token][0] -= 1
                    self.statistics['term_metadata'][token][1] -= count
                    break
        self.statistics['total_token_count'] -= self.document_metadata[docid]['length']
        self.statistics['number_of_documents'] -= 1
        del self.document_metadata[docid]
        self.get_statistics()


    def add_doc(self, docid: int, tokens: list[str]) -> None:
        '''
        Adds a document to the index and updates the index's metadata on the basis of this
        document's addition (e.g., collection size, average document length, etc.)

        Arguments:
            docid [int]: the identifier of the document

            tokens list[str]: the tokens of the document. Tokens that should not be indexed will have 
            been replaced with None in this list. The length of the list should be equal to the number
            of tokens prior to any token removal.
        '''
        # TODO implement this to add documents to the index
        if not tokens:
            return
        
        token_counts = Counter(tokens)
        for token in token_counts:
            if token is None:
                continue
            self.index[token].append((docid, token_counts[token]))
            self.statistics['stored_total_token_count'] += token_counts[token]
            if token in self.statistics['term_metadata']:
                self.statistics['term_metadata'][token][0] += 1
                self.statistics['term_metadata'][token][1] += token_counts[token]
            else:
                self.statistics['term_metadata'][token] = [1, token_counts[token]]

        self.document_metadata[docid] = {'unique_tokens': len(token_counts), 'length': len(tokens)}
        self.statistics['total_token_count'] += len(tokens)
        self.statistics['number_of_documents'] += 1
        

    def get_postings(self, term: str) -> list[tuple[int, int]]:
        '''
        Returns the list of postings, which contains (at least) all the documents that have that term.
        In most implementation this information is represented as list of tuples where each tuple
        contains the docid and the term's frequency in that document.
        
        Arguments:
            term [str]: the term to be searched for

        Returns:
            list[tuple[int,str]] : A list of tuples containing a document id for a document
            that had that search term and an int value indicating the term's frequency in 
            the document.
        '''
        # TODO implement this to fetch a term's postings from the index
        if term not in self.index:
            return []
        return self.index[term]

    def get_doc_metadata(self, doc_id: int) -> dict[str, int]:
        '''
        For the given document id, returns a dictionary with metadata about that document. Metadata
        should include keys such as the following:
            "unique_tokens": How many unique tokens are in the document (among those not-filtered)
            "length": how long the document is in terms of tokens (including those filtered)             
        '''
        # TODO implement to fetch a particular documents stored metadata
        if doc_id in self.document_metadata:
            return self.document_metadata[doc_id]
        return {'unique_tokens': 0, 'length': 0}

    def get_term_metadata(self, term: str) -> dict[str, int]:
        '''
        For the given term, returns a dictionary with metadata about that term in the index. Metadata
        should include keys such as the following:
            "count": How many times this term appeared in the corpus as a whole.          
        '''        
        # TODO implement to fetch a particular terms stored metadata
        if term not in self.statistics['term_metadata']:
            return {'document_count': 0, 'count': 0}
        document_count = self.statistics['term_metadata'][term][0]
        term_frequency = self.statistics['term_metadata'][term][1]
        return {'document_count': document_count, 'count': term_frequency}

    def get_statistics(self) -> dict[str, int]:
        '''
        Returns a dictionary mapping statistical properties (named as strings) about the index to their values.  
        Keys should include at least the following:

            "unique_token_count": how many unique terms are in the index
            "total_token_count": how many total tokens are indexed including filterd tokens), 
                i.e., the sum of the lengths of all documents
            "stored_total_token_count": how many total tokens are indexed excluding filterd tokens
            "number_of_documents": the number of documents indexed
            "mean_document_length": the mean number of tokens in a document (including filter tokens)                
        '''
        # TODO calculate statistics like 'unique_token_count', 'total_token_count', 
        #  'number_of_documents', 'mean_document_length' and any other relevant central statistic.
        self.statistics['unique_token_count'] = len(self.index)
        self.statistics['mean_document_length'] = self.statistics['total_token_count']/self.statistics['number_of_documents'] if self.statistics['number_of_documents'] else 0
        return {'unique_token_count': self.statistics['unique_token_count'], 
                'total_token_count': self.statistics['total_token_count'], 
                'stored_total_token_count': self.statistics['stored_total_token_count'], 
                'number_of_documents': self.statistics['number_of_documents'], 
                'mean_document_length': self.statistics['mean_document_length']}

    # NOTE: changes in this method for HW2
    def save(self, index_directory_name) -> None:
        '''
        Saves the state of this index to the provided directory. The save state should include the
        inverted index as well as any meta data need to load this index back from disk
        '''
        # TODO save the index files to disk
        if not os.path.exists(index_directory_name):
            os.mkdir(index_directory_name)
        with open(index_directory_name+'/'+'index.json', 'w', encoding='utf-8') as f:
            json.dump(self.index, f)
        with open(index_directory_name+'/'+'document_metadata.json', 'w', encoding='utf-8') as f:
            json.dump(self.document_metadata, f)
        with open(index_directory_name+'/'+'statistics.json', 'w', encoding='utf-8') as f:
            json.dump(self.statistics, f)
        print('Index saved!')

    # NOTE: changes in this method for HW2
    def load(self, index_directory_name) -> None:
        '''
        Loads the inverted index and any associated metadata from files located in the directory.
        This method will only be called after save() has been called, so the directory should
        match the filenames used in save()
        '''
        # TODO load the index files from disk to a Python object
        with open(index_directory_name+'/'+'index.json', 'r', encoding='utf-8') as f:
            self.index = json.load(f)
        with open(index_directory_name+'/'+'document_metadata.json', 'r', encoding='utf-8') as f:
            document_metadata = json.load(f)
            self.document_metadata = {int(k): v for k, v in document_metadata.items()}
        with open(index_directory_name+'/'+'statistics.json', 'r', encoding='utf-8') as f:
            self.statistics = json.load(f)


class Indexer:
    """
    The Indexer class is responsible for creating the index used by the search/ranking algorithm.
    """
    @staticmethod
    def create_index(index_type: IndexType, dataset_path: str,
                     document_preprocessor: Tokenizer, stopwords: set[str],
                     minimum_word_frequency: int, text_key="prompt",
                     max_docs: int = -1, doc_augment_dict = None) -> InvertedIndex:
        """
        Creates an inverted index.

        Args:
            index_type: This parameter tells you which type of index to create, e.g., BasicInvertedIndex
            dataset_path: The file path to your dataset
            document_preprocessor: A class which has a 'tokenize' function which would read each document's text
                and return a list of valid tokens
            stopwords: The set of stopwords to remove during preprocessing or 'None' if no stopword filtering is to be done
            minimum_word_frequency: An optional configuration which sets the minimum word frequency of a particular token to be indexed
                If the token does not appear in the document at least for the set frequency, it will not be indexed.
                Setting a value of 0 will completely ignore the parameter.
            text_key: The key in the JSON to use for loading the text
            max_docs: The maximum number of documents to index
                Documents are processed in the order they are seen.
            doc_augment_dict: An optional argument; This is a dict created from the doc2query.csv where the keys are
                the document id and the values are the list of queries for a particular document.

        Returns:
            An inverted index
        """
        # TODO (HW3): This function now has an optional argument doc_augment_dict; check README
       
        # HINT: Think of what to do when doc_augment_dict exists, how can you deal with the extra information?
        #       How can you use that information with the tokens?
        #       If doc_augment_dict doesn't exist, it's the same as before, tokenizing just the document text
          
        # TODO: Implement this class properly. This is responsible for going through the documents
        #       one by one and inserting them into the index after tokenizing the document

        # TODO: Figure out what type of InvertedIndex to create.
        #       For HW3, only the BasicInvertedIndex is required to be supported

        # TODO: If minimum word frequencies are specified, process the collection to get the
        #       word frequencies

        # NOTE: Make sure to support both .jsonl.gz and .jsonl as input
                      
        # TODO: Figure out which set of words to not index because they are stopwords or
        #       have too low of a frequency

        # HINT: This homework should work fine on a laptop with 8GB of memory but if you need,
        #       you can delete some unused objects here to free up some space

        # TODO: Read the collection and process/index each document.
        #       Only index the terms that are not stopwords and have high-enough frequency

        index = None
        if index_type == IndexType.InvertedIndex:
            index = BasicInvertedIndex()
        else:
            raise NameError
        

        filtered_tokens = set()
        if minimum_word_frequency:
            word_frequency = Counter()
            if dataset_path.endswith('jsonl'):
                with open(dataset_path, 'r', encoding='utf-8') as f:
                    for i, line in tqdm(enumerate(f)):
                        if max_docs > 0 and i >= max_docs:
                            break
                        docid = json.loads(line)['docid']
                        doc = json.loads(line)[text_key]
                        if doc_augment_dict and docid in doc_augment_dict:
                            doc = ' '.join([doc] + doc_augment_dict[docid])
                        tokens = document_preprocessor.tokenize(doc)
                        word_frequency.update(tokens)
            elif dataset_path.endswith('jsonl.gz'):
                with gzip.open(dataset_path, 'rt', encoding='utf-8') as f:
                    for i, line in tqdm(enumerate(f)):
                        if max_docs > 0 and i >= max_docs:
                            break
                        docid = json.loads(line)['docid']
                        doc = json.loads(line)[text_key]
                        if doc_augment_dict and docid in doc_augment_dict:
                            doc = ' '.join([doc] + doc_augment_dict[docid])
                        tokens = document_preprocessor.tokenize(doc)
                        word_frequency.update(tokens)
            else:
                raise TypeError('Dataset type not supported')
            for word in word_frequency:
                if word_frequency[word] < minimum_word_frequency:
                    filtered_tokens.add(word)

        if stopwords:
            filtered_tokens |= stopwords

        if dataset_path.endswith('jsonl'):
            with open(dataset_path, 'r', encoding='utf-8') as f:
                for i, line in tqdm(enumerate(f)):
                    if max_docs > 0 and i >= max_docs:
                        break
                    docid = json.loads(line)['docid']
                    doc = json.loads(line)[text_key]
                    if doc_augment_dict and docid in doc_augment_dict:
                        doc = ' '.join([doc] + doc_augment_dict[docid])
                    tokens = document_preprocessor.tokenize(doc)
                    for j, token in enumerate(tokens):
                        if token in filtered_tokens:
                            tokens[j] = None
                    index.add_doc(docid, tokens)
        elif dataset_path.endswith('jsonl.gz'):
            with gzip.open(dataset_path, 'rt', encoding='utf-8') as f:
                for i, line in tqdm(enumerate(f)):
                    if max_docs > 0 and i >= max_docs:
                        break
                    docid = json.loads(line)['docid']
                    doc = json.loads(line)[text_key]
                    if doc_augment_dict and docid in doc_augment_dict:
                        doc = ' '.join([doc] + doc_augment_dict[docid])
                    tokens = document_preprocessor.tokenize(doc)
                    for j, token in enumerate(tokens):
                        if token in filtered_tokens:
                            tokens[j] = None
                    index.add_doc(docid, tokens)
        index.get_statistics()

        return index
