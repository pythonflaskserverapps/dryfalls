from dryfalls import read_string_from_file

############################################################

def test_dryfalls():

    print("testing dryfalls")

    assert read_string_from_file(None, "default") == "default"

############################################################
