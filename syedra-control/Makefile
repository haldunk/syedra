# Make management targets
.PHONY : help

help :
	@echo "make [target]"
	@echo
	@echo "Folder management:"
	@echo "  clean           - deletes temporary files"
	@echo "Packaging management:"
	@echo "  clear           - clears any built package"
	@echo "  build           - builds python package"


# Folder management targets
.PHONY : clean

clean :
	@printf "Deleting all temporary files..."
	@find . -name "*~" -delete
	@printf "done.\n"

# Packaging management targets
.PHONY : clear build

clear :
	@echo "All compiled package files deleted"
	@rm -fr dist source/*.egg-info

build : clear
	@if [ -n "$$VIRTUAL_ENV" ]; then \
		echo "Build syedra-core python package"; \
		python -m build; \
	else \
		echo "### activate the virtual environment first ###"; \
	fi
