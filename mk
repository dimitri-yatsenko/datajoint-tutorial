pandoc README.md license.md \
citing.md \
publications.md \
the_experiment/scenario.md \
algebra/algebra.md \
algebra/union.md \
--toc -V fontsize=10pt -V geometry:margin=1in --number-sections --listings -H listings-setup.tex -o book.pdf && open book.pdf
