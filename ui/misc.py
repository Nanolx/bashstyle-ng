#!/usr/bin/env bashstyle --python
#coding=utf-8
#########################################################
# 							#
# This is BashStyle-NG  				#
#							#
# Licensed under GNU GENERAL PUBLIC LICENSE v3		#
#							#
# Copyright 2007 - 2014 Christopher Bratusek		#
#							#
#########################################################

def SwapDictionary(original_dict):
    try:
            iteritems = original_dict.iteritems
    except AttributeError:
            iteritems = original_dict.items
    return dict([(v, k) for (k, v) in iteritems()])
