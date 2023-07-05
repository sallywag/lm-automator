lm-automator
============

Automation framework for creating automated tests for a WordPress layout manager tool.
The framework was developed in house during my time at Fox.

How it works
------------

The framework abstracts web elements into input, widget, component, and region objects, which are accessed and manipulated via page objects.
YAML files are used for defining pages and the various elements found within them. YAML files are also used to create the automated tests. The
YAML is parsed and converted into running code.
