
# MARPT (Morphology Analysis and Recursive Parsing Toolkit)
MARPT (Morphology Analysis and Recursive Parsing Toolkit) is a Python library designed to facilitate morphological analysis and recursive parsing of words. This comprehensive toolkit combines the power of BNF grammars and Mealy machines to provide linguists, researchers, and language enthusiasts with a versatile set of tools for linguistic analysis.

## Installation
To start using MARPT, you'll need to install the required Python libraries. You can install them using pip


``` 
!pip install -q textx 
```
Usage
Morpheme Notation
MARPT uses a straightforward and consistent notation for morphemes

*  '+' Prefix (p)
 * '$' Root (r)
 * '-' Interfix (i)
 * '^' Suffix (s)
 * '*'  Ending (e)
 * '@' Postfix (x)
 * '&', 'T' Start and end of the word

## BNF Parser
MARPT provides a BNF parser that can generate valid word forms based on a given set of morphemes. However, please note that this parser may be less efficient for large-scale analysis.

## Linearized BNF Grammar
For more efficient parsing, MARPT offers a linearized BNF grammar. You can define your grammar from a string and generate possible word forms using this grammar. This method is particularly useful when dealing with a wide range of morphemes.

## Mealy Machine Parser
The Mealy Machine parser in MARPT is highly efficient and suitable for linguistic analysis. It efficiently handles word parsing and can generate all possible morphological paths for a given word.

## Filtering with Linearized BNF
MARPT includes a filtering mechanism for Mealy Machine Parser that allows you to inspect valid morphological paths based on linearized BNF grammar. You can filter and inspect the linguistic structure of words using this feature.

# Demo
MARPT provides a comprehensive demonstration of its features. It showcases how to preprocess morphemes, define prefixes and roots, parse words, and perform linguistic analysis. Additionally, it offers a speed comparison for various parsing methods to help you choose the most suitable approach for your linguistic analysis tasks.

Get Started
MARPT is a powerful toolkit for linguists, language enthusiasts, and researchers who need to analyze and parse words at the morphological level. Whether you're working on language processing, morphology analysis, or linguistic research, MARPT can simplify your tasks and provide efficient parsing capabilities.