import json


def test_gamestate(app, api_prefix):
    # Expected values
    expected_status_code = 200
    expected_outer_subset = {
        'signature', 'score', 'board', 'gameover',
    }
    expected_signature_subset = {
        'message', 'messageHash', 'v', 'r', 's', 'signature',
    }

    # Generate Ouput
    endpoint = api_prefix + '/gamestate'
    output = app.get(endpoint)
    output_status_code = output.status_code

    # Test
    assert output_status_code == expected_status_code
    output_data = json.loads(output.data)
    ouput_outer_set = set(output_data.keys())
    assert expected_outer_subset <= ouput_outer_set
    output_signature_set = set(output_data['signature'].keys())
    assert expected_signature_subset <= output_signature_set
