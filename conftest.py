#File consisting of fixtures that could be shared between several tests
import pytest
import json
#import test_calc_add 
#import test_calc_sub
#import test_calc_mul
import test_calc_div
import os


def pytest_sessionfinish(session, exitstatus):
    data = test_calc_div.pytest.json_metadata
    with open('result.json', 'w') as f:
        json.dump(data, f, indent=4)
