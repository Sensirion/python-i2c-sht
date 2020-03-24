# -*- coding: utf-8 -*-
# (c) Copyright 2020 Sensirion AG, Switzerland

from __future__ import absolute_import, division, print_function
import pytest


@pytest.mark.needs_device
@pytest.mark.needs_sht3x
def test_invalid_config(sht3x):
    """
    Test if the single_shot_measurement() raises an exception for invalid
    inputs.
    """
    with pytest.raises(ValueError):
        sht3x.single_shot_measurement('not_valid')
