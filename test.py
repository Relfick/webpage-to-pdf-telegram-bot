import main

test_url = "http://help.websiteos.com/websiteos/example_of_a_simple_html_page.htm"
test_chat_id = 111

def test_get_file_name():
    # answer = 'help_websiteos_com_websiteos_example_of_a_simple_html_page_htm.pdf'
    answer = 'help.websiteos.com_websiteos_example_of_a_simple_html_page.htm.pdf'
    test_url_2 = test_url + '/'
    test_url_3 = test_url[:7] + 'www.' + test_url[7:]

    assert main.get_file_name(test_url) == answer
    assert main.get_file_name(test_url_2) == answer
    assert main.get_file_name(test_url_3) == answer


def test_prepare_response():
    input1 = test_url

    input2 = '/start'
    answer2 = "Hello! Send link starting with http or https"

    input3 = test_url[:-2]
    answer3 = "Can't open this link"
    input4 = "hello"
    answer4 = "Incorrect link!"

    assert type(main.prepare_response(input1)) is bytes
    assert main.prepare_response(input2) == answer2
    assert main.prepare_response(input3) == answer3
    assert main.prepare_response(input4) == answer4