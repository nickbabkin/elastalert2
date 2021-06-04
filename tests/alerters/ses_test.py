import pytest

from elastalert.alerters.ses import SesAlerter
from elastalert.loaders import FileRulesLoader


def test_ses_getinfo():
    rule = {
        'name': 'Test Rule',
        'type': 'any',
        'alert_subject': 'Cool subject',
        'ses_email': 'test@aaa.com',
        'ses_aws_access_key_id': 'access key id',
        'ses_aws_secret_access_key': 'secret access key',
        'alert': []
    }
    rules_loader = FileRulesLoader({})
    rules_loader.load_modules(rule)
    alert = SesAlerter(rule)

    expected_data = {
        'type': 'ses',
        'recipients': ['test@aaa.com']
    }
    actual_data = alert.get_info()
    assert expected_data == actual_data


@pytest.mark.parametrize('ses_email, ses_from_addr, expected_data', [
    ('',             '',       True),
    ('test@aaa.com', '',       True),
    ('',             'xxxxx2', True),
    ('test@aaa.com', 'xxxxx2',
        {
            'type': 'ses',
            'recipients': ['test@aaa.com']
        }),
])
def test_ses_key_error(ses_email, ses_from_addr, expected_data):
    try:
        rule = {
            'name': 'Test Telegram Rule',
            'type': 'any',
            'alert': []
        }

        if ses_email != '':
            rule['ses_email'] = ses_email

        if ses_from_addr != '':
            rule['ses_from_addr'] = ses_from_addr

        rules_loader = FileRulesLoader({})
        rules_loader.load_modules(rule)
        alert = SesAlerter(rule)

        actual_data = alert.get_info()
        assert expected_data == actual_data
    except KeyError:
        assert expected_data
