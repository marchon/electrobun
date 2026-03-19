# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = source
BUILDDIR      = build

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile clean livehtml check links

# Live reload server for development
livehtml:
	sphinx-autobuild "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

# Clean build files
clean:
	rm -rf $(BUILDDIR)/*

# Check documentation for errors
check:
	@$(SPHINXBUILD) -b doctest "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

# Check all external links
links:
	@$(SPHINXBUILD) -b linkcheck "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

# Build multiversion docs (requires sphinx-multiversion)
multiversion:
	sphinx-multiversion "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS)

# Quick build (no warnings)
quick:
	@$(SPHINXBUILD) -M html "$(SOURCEDIR)" "$(BUILDDIR)" -W $(SPHINXOPTS) $(O)

# Production build (strict)
prod:
	@$(SPHINXBUILD) -M html "$(SOURCEDIR)" "$(BUILDDIR)" -W --keep-going $(SPHINXOPTS) $(O)

# Build PDF via LaTeX
latexpdf:
	@$(SPHINXBUILD) -M latexpdf "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

# Build LaTeX only (for manual PDF generation)
latex:
	@$(SPHINXBUILD) -M latex "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
