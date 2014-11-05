#!/usr/bin/env python
import yaml
import pprint

fields = yaml.load(open('fields.yml', 'r'))

pprint.pprint(fields)
