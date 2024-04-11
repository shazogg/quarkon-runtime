# quarkon-runtime

The Quarkon runtime is a library that provides a runtime environment for Quarkon programs. The Lexer and  Parser are written in Python and the runtime is written in C++.

## Usage

### Parser

The Parser is written in Python and can be used to parse Quarkon programs. The Parser is used to parse the Quarkon programs and generate an Abstract Syntax Tree (AST) that can be used by the runtime.

to execute the parser, run the following command:

```bash
python3 src/parser/main.py <path-to-quarkon-program> <output-file>
```

to visualize the AST, run the following command:

```bash
python3 src/parser/main.py <path-to-quarkon-program> <output-file> --dot <output-dot-file>
```

Example:

```bash
python3 src/parser/main.py test/main.qk test/main.qkt
python3 src/parser/main.py test/main.qk test/main.qkt --dot test/main.dot
```

## Syntax

You can read the language syntax in the [Syntax repository.](https://github.com/shazogg/quarkon)

## Technologies

- Python 3
- C++

## Notes

- I'm a student, not an expert, so if there's a problem or anything, I'd love to hear from you.

- In the future, the Lexer and Parser will also be written in C++.
