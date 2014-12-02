#!/usr/bin/env python
import yaml
import pprint

yamlFile = yaml.load(open('fields.yml', 'r'))

pprint.pprint(yamlFile)

