# Parser Guidelines


## Parser Requirements


Every parser must:

- inherit BaseParser;
- implement parse();
- validate input;
- handle errors.


Example structure:


parsers/

    avito/

        parser.py
        schemas.py
        config.py



## Parser responsibilities


Parser SHOULD:

- collect data;
- transform raw response.


Parser SHOULD NOT:

- create database connections;
- manage users;
- access API directly.
