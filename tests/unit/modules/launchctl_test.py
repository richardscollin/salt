# -*- coding: utf-8 -*-
'''
    :codeauthor: :email:`Rupesh Tare <rupesht@saltstack.com>`
'''

# Import Python libs
from __future__ import absolute_import

# Import Salt Testing Libs
from salttesting import TestCase, skipIf
from salttesting.mock import (
    MagicMock,
    patch,
    NO_MOCK,
    NO_MOCK_REASON
)

# Import Salt Libs
from salt.modules import launchctl

# Globals
launchctl.__salt__ = {}


@skipIf(NO_MOCK, NO_MOCK_REASON)
class LaunchctlTestCase(TestCase):
    '''
    Test cases for salt.modules.launchctl
    '''
    def test_get_all(self):
        '''
        Test for Return all installed services
        '''
        with patch.dict(launchctl.__salt__,
                        {'cmd.run': MagicMock(return_value='A\tB\tC\t\n')}):
            with patch.object(launchctl,
                              '_available_services',
                              return_value={'A': 'a', 'B': 'b'}):
                self.assertEqual(launchctl.get_all(), ['A', 'B', 'C'])

    def test_available(self):
        '''
        Test for Check that the given service is available.
        '''
        with patch.object(launchctl,
                          '_service_by_name', return_value=True):
            self.assertTrue(launchctl.available('job_label'))

    def test_missing(self):
        '''
        Test for The inverse of service.available
        '''
        with patch.object(launchctl,
                          '_service_by_name', return_value=True):
            self.assertFalse(launchctl.missing('job_label'))

    def test_status(self):
        '''
        Test for Return the status for a service
        '''
        launchctl_data = '''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>salt-minion</string>
    <key>LastExitStatus</key>
    <integer>0</integer>
    <key>LimitLoadToSessionType</key>
    <string>System</string>
    <key>OnDemand</key>
    <false/>
    <key>PID</key>
    <integer>71</integer>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/local/bin/salt-minion</string>
    </array>
    <key>TimeOut</key>
    <integer>30</integer>
</dict>
</plist>'''
        with patch.object(launchctl,
                          '_service_by_name',
                          return_value={'plist':
                                        {'Label': 'A'}}):
            with patch.object(launchctl, '_get_launchctl_data',
                              return_value=launchctl_data):
                self.assertTrue(launchctl.status('job_label'))

    def test_stop(self):
        '''
        Test for Stop the specified service
        '''
        with patch.object(launchctl,
                          '_service_by_name',
                          return_value={'file_path': 'A'}):
            with patch.dict(launchctl.__salt__,
                            {'cmd.retcode': MagicMock(return_value=False)}):
                self.assertTrue(launchctl.stop('job_label'))

        with patch.object(launchctl,
                          '_service_by_name',
                          return_value=None):
            self.assertFalse(launchctl.stop('job_label'))

    def test_start(self):
        '''
        Test for Start the specified service
        '''
        with patch.object(launchctl,
                          '_service_by_name',
                          return_value={'file_path': 'A'}):
            with patch.dict(launchctl.__salt__,
                            {'cmd.retcode': MagicMock(return_value=False)}):
                self.assertTrue(launchctl.start('job_label'))

        with patch.object(launchctl,
                          '_service_by_name',
                          return_value=None):
            self.assertFalse(launchctl.start('job_label'))

    def test_restart(self):
        '''
        Test for Restart the named service
        '''
        with patch.object(launchctl, 'stop', return_value=None):
            with patch.object(launchctl, 'start', return_value=True):
                self.assertTrue(launchctl.restart('job_label'))


if __name__ == '__main__':
    from integration import run_tests
    run_tests(LaunchctlTestCase, needs_daemon=False)
