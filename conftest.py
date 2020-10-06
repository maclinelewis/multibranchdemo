#File consisting of fixtures that could be shared between several tests
import pytest
import json
import test_calc_add 
#import test_calc_sub
#import test_calc_mul
#import test_calc_div
import os


def pytest_sessionfinish(session, exitstatus):
    data1 = test_calc_add.pytest.json_metadata
    data2 = test_calc_sub.pytest.json_metadata
    data3 = test_calc_mul.pytest.json_metadata
    data4 = test_calc_div.pytest.json_metadata
    data = data1+data2+data3+data4
    with open('result.json', 'w') as f:
        json.dump(data, f, indent=4)
