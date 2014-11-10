#!/usr/bin/env python
import yaml
import pprint

yamlFile = yaml.load(open('fieldStatus.yml', 'r'))

pprint.pprint(yamlFile)


