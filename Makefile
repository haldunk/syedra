# Make management targets
.PHONY : help

help :
	@echo "make [target]"
	@echo
	@echo "Folder management:"
	@echo "  clean           - deletes temporary files"
	@echo "Virtual environment management:"
	@echo "  venv            - sets up the virtual environment"
	@echo "Packaging management:"
	@echo "  clear           - clears any built package"
	@echo "  build           - builds python package"


# Folder management targets
.PHONY : clean

clean :
	@printf "Deleting all temporary files..."
	@find . -name "*~" -delete
	@printf "done.\n"


# Virtual environment targets
.PHONY : venv

venv :
	@echo "Setup virtual environment"
	@python -m virtualenv venv
	@source venv/bin/activate && pip install -r requirements.txt

# Packaging management targets
.PHONY : clear build

clear :
	@echo "Delete any compiled package"
	@rm -fr *.egg-info
	@rm -fr dist

build : clear
	@echo "Build python package"
	@source venv/bin/activate && python -m build
