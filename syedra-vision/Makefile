# Make management targets
.PHONY : help

help :
	@echo "Syedra Python Vision Library"
	@echo
	@echo " Folder management:"
	@echo "   clean   - deletes temporary files"
	@echo
	@echo " Packaging management:"
	@echo "   clear   - clears any built package"
	@echo "   build   - builds python package"
	@echo "   install - install compiled package locally"


# Folder management targets
.PHONY : clean

clean :
	@printf "Deleting all temporary files..."
	@find . -name "*~" -delete
	@printf "done.\n"

# Packaging management targets
.PHONY : clear build install

clear :
	@echo "All compiled package files deleted"
	@rm -fr dist source/*.egg-info

build : clear
	@if [ -n "$$VIRTUAL_ENV" ]; then \
		echo "Build syedra-vision python package"; \
		python -m build; \
	else \
		echo "### activate the virtual environment first ###"; \
	fi

install :
	@echo "Installing syedra-vision package locally"
	@pip uninstall --break-system-packages syedra_vision
	@pip install -U --break-system-packages dist/*.whl
