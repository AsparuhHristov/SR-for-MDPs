Code for massaging the output from the gplearn's SR implementation.

As one can see the output is the specific instance's program given in the format of tree:

For example: "sub(X1,add(X0,X3))"

For me that is difficult to interpret, and therefore, decodeTree.py comes to the rescue!
Namely, I transfer it to the more common for me output - a "normal" mathematical formula:

After applying decodeTree.py: "X1-(X0+X3)"

Next to that, decodeTree.py simplifies the inputed expression!!! The used package for SR does not simplified it
by itself, which sometimes (most of the times) turns into a nightmare.

The decodeSymbols.py turns the labeled features (X0, X1, etc.) into the desired name. Note that currently it is
hardcoded as it is simply used once and it is case specific.
