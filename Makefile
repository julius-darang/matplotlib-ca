PHASE1_SCRIPTS := $(filter-out %/__init__.py,$(wildcard physics/phase_1/*.py))
PHASE2_SCRIPTS := $(filter-out %/__init__.py,$(wildcard physics/phase_2/*.py))
PHASE1_TOPICS  := $(patsubst physics/phase_1/%.py,phase_1/%,$(PHASE1_SCRIPTS))
PHASE2_TOPICS  := $(patsubst physics/phase_2/%.py,phase_2/%,$(PHASE2_SCRIPTS))
TOPICS         := $(PHASE1_TOPICS) $(PHASE2_TOPICS)
TARGETS        := $(addprefix topic/,$(TOPICS))
PYTHON         ?= $(if $(wildcard .venv/bin/python),.venv/bin/python,python)

.PHONY: all clean watch install

all: $(TARGETS)

topic/phase_1/%: physics/phase_1/%.py outputs
	$(PYTHON) -m physics.phase_1.$*

topic/phase_2/%: physics/phase_2/%.py outputs
	$(PYTHON) -m physics.phase_2.$*

outputs:
	mkdir -p outputs

clean:
	rm -f outputs/*.png outputs/*.gif

watch:
	@which fswatch > /dev/null || (echo "install fswatch: brew install fswatch"; exit 1)
	@while true; do \
		fswatch -1 physics/ theme.py animate.py builder.py 2>/dev/null; \
		$(MAKE) all; \
	done

install:
	$(PYTHON) -m pip install -e .
