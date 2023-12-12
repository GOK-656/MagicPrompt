from nltk.tokenize import RegexpTokenizer
from nltk.stem import PorterStemmer

class Tokenizer:
    def __init__(
        self,
        lowercase: bool = True,
        multiword_expressions: list[str] = None,
        stemming: bool = False,
    ) -> None:
        """
        A generic class for objects that turn strings into sequences of tokens.
        A tokenizer can support different preprocessing options or use different methods
        for determining word breaks.

        Args:
            lowercase: Whether to lowercase all the tokens
            multiword_expressions: A list of strings that should be recognized as single tokens
                If set to 'None' no multi-word expression matching is performed.
                No need to perform/implement multi-word expression recognition for HW3.
        """
        # TODO: Save arguments that are needed as fields of this class
        self.lowercase = lowercase
        self.multiword_expressions = multiword_expressions
        self.stemming = stemming

    def find_and_replace_mwes(self, input_tokens: list[str]) -> list[str]:
        """
        IGNORE THIS PART; NO NEED TO IMPLEMENT THIS SINCE NO MULTI-WORD EXPRESSION PROCESSING IS TO BE USED.
        For the given sequence of tokens, finds any recognized multi-word expressions in the sequence
        and replaces that subsequence with a single token containing the multi-word expression.

        Args:
            input_tokens: A list of tokens

        Returns:
            A list of tokens containing processed multi-word expressions
        """
        # NOTE: You shouldn't implement this in homework
        raise NotImplemented("MWE is not supported")

    def postprocess(self, input_tokens: list[str]) -> list[str]:
        """
        Performs any set of optional operations to modify the tokenized list of words such as
        lower-casing and stemming and returns the modified list of tokens.

        Args:
            input_tokens: A list of tokens

        Returns:
            A list of tokens processed by lower-casing and stemming depending on the given condition
        """
        # TODO: Add support for lower-casing
        if self.lowercase:
            input_tokens = [token.lower() for token in input_tokens]
        if self.stemming:
            ps = PorterStemmer()
            input_tokens = [ps.stem(token) for token in input_tokens]
        return input_tokens

    def tokenize(self, text: str) -> list[str]:
        """
        Splits a string into a list of tokens and performs all required postprocessing steps.

        Args:
            text: An input text you want to tokenize

        Returns:
            A list of tokens
        """
        raise NotImplementedError(
            "tokenize() is not implemented in the base class; please use a subclass"
        )


class RegexTokenizer(Tokenizer):
    def __init__(
        self,
        token_regex: str,
        lowercase: bool = True,
        multiword_expressions: list[str] = None,
        stemming: bool = False,
    ) -> None:
        """
        Uses NLTK's RegexpTokenizer to tokenize a given string.

        Args:
            token_regex: Use the following default regular expression pattern: '\\w+'
            lowercase: Whether to lowercase all the tokens
            multiword_expressions: A list of strings that should be recognized as single tokens
                If set to 'None' no multi-word expression matching is performed.
                No need to perform/implement multi-word expression recognition for HW3; you can ignore this.
        """
        super().__init__(lowercase, multiword_expressions, stemming)
        # TODO: Save a new argument that is needed as a field of this class
        # TODO: Initialize the NLTK's RegexpTokenizer
        self.tokenizer = RegexpTokenizer(token_regex)

    def tokenize(self, text: str) -> list[str]:
        """Uses NLTK's RegexTokenizer and a regular expression pattern to tokenize a string.

        Args:
            text: An input text you want to tokenize

        Returns:
            A list of tokens
        """
        # TODO: Tokenize the given text and perform postprocessing on the list of tokens
        #       using the postprocess function
        words = self.tokenizer.tokenize(text)
        return self.postprocess(words)
