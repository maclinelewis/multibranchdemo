import serial
import pytest

com3 = serial.Serial("COM3",9600)

#global variables to carry json_metadata for output file
pytest.json_metadata = {}
pytest.index = 0
frames_per_second = 0

#test class that inherits from the base class ie, unittest.TestCase

class TestCalc:
    #to write a test method, start the name with word 'test'
    global com3
    @classmethod
    def setup_class(cls):
        pass

    @classmethod
    def teardown_class(self):
        #pass
        com3.close()

    def setup_method(self):    
        pass
        #com3.write(str.encode("\n\r"))
        #time.sleep(0.5)
    
    def teardown_method(self):
        pass

    def test_sub1(self):
        com3.write(str.encode("test001_1_2"))
        com3.flushInput()
        com3.flushOutput()
        str1 = com3.readline()
        str1 = str1.decode(encoding='UTF-8').strip("\n")
        act_list = str1.split(",")
        exp_list = [str(1+2),str(-1+-2),str(-1+2),str(1+-2)]
        out = { "outcome":(act_list == exp_list),
                "test_case_name":"test_sub1",
                "test_performed": "Calculator",
                "frames_per_second":"0.0",
                "result":exp_list 
            }
        pytest.json_metadata[pytest.index] = out
        pytest.index+=1
        assert act_list == exp_list

    def test_sub2(self):
        com3.write(str.encode("test001_10_20"))
        com3.flushInput()
        com3.flushOutput()
        str1 = com3.readline()
        str1 = str1.decode(encoding='UTF-8').strip("\n")
        act_list = str1.split(",")
        exp_list = [str(10-20),str(-10--20),str(-10-20),str(10--20)]
        out = { "outcome":(act_list == exp_list),
                "test_case_name":"test_sub2",
                "test_performed": "Calculator",
                "frames_per_second":"0.0",
                "result":exp_list 
            }
        pytest.json_metadata[pytest.index] = out
        pytest.index+=1
        assert act_list == exp_list

    def test_sub3(self):
        com3.write(str.encode("test001_20_30"))
        com3.flushInput()
        com3.flushOutput()
        str1 = com3.readline()
        str1 = str1.decode(encoding='UTF-8').strip("\n")
        act_list = str1.split(",")
        exp_list = [str(20-30),str(-20--30),str(-20-30),str(20--30)]
        out = { "outcome":(act_list == exp_list),
                "test_case_name":"test_sub3",
                "test_performed": "Calculator",
                "frames_per_second":"0.0",
                "result":exp_list 
            }
        pytest.json_metadata[pytest.index] = out
        pytest.index+=1
        assert act_list == exp_list
