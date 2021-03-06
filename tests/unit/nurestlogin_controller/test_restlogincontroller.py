# -*- coding:utf-8 -*-

from unittest import TestCase
from bambou import NURESTLoginController


class LoginControllerSingleton(TestCase):

    def test_login_controller_is_not_singleton(self):
        """ login controller is singleton """
        ctrl_a = NURESTLoginController()
        ctrl_a.user = 'Christophe'
        ctrl_b = NURESTLoginController()
        ctrl_b.user = 'Toto'

        self.assertEquals(ctrl_a.user, 'Christophe')
        self.assertEquals(ctrl_b.user, 'Toto')
        self.assertNotEqual(ctrl_a, ctrl_b)


class GetAuthenticationHeader(TestCase):

    def test_get_authentication_header_without_api_key(self):
        """ Get authentication header without api key """

        controller = NURESTLoginController()
        controller.user = 'christophe'
        controller.password = 'tuCr0IsKoi?'
        controller.api_key = None

        header = controller.get_authentication_header()
        self.assertEquals(header, 'XREST Y2hyaXN0b3BoZTp0dUNyMElzS29pPw==')

    def test_get_authentication_header_with_api_key(self):
        """ Get authentication header with api key """

        controller = NURESTLoginController()
        controller.user = 'christophe'
        controller.password = None
        controller.api_key = '12345ABCD'

        header = controller.get_authentication_header()
        self.assertEquals(header, 'XREST Y2hyaXN0b3BoZToxMjM0NUFCQ0Q=')


class ResetLoginController(TestCase):

    def test_reset_login_controller(self):
        """ Reset login controller """

        controller = NURESTLoginController()
        controller.user = 'christophe'
        controller.password = 'password'
        controller.url = 'http://www.google.fr'
        controller.api_key = '12345'
        controller.enterprise = 'Alcatel'

        controller.reset()

        self.assertEquals(controller.user, None)
        self.assertEquals(controller.password, None)
        self.assertEquals(controller.url, None)
        self.assertEquals(controller.enterprise, None)
        self.assertEquals(controller.api_key, None)


class ImpersonateLoginController(TestCase):

    def setUp(self):
        """ Set up the context """
        controller = NURESTLoginController()
        controller.user = 'christophe'
        controller.password = 'password'
        controller.url = 'http://www.google.fr'
        controller.api_key = '12345'
        controller.enterprise = 'Alcatel'

    def tearDown(self):
        """ Cleaning context """
        ctrl = NURESTLoginController()
        ctrl.reset()

    def test_impersonate(self):
        """ Start impersonate """

        controller = NURESTLoginController()
        controller.impersonate(user='Alex', enterprise='Google')

        self.assertEquals(controller.is_impersonating, True)
        self.assertEquals(controller.impersonation, 'Alex@Google')

    def test_stop_impersonate(self):
        """ Stop impersonate """
        controller = NURESTLoginController()
        controller.impersonate(user='Alex', enterprise='Google')
        self.assertEquals(controller.is_impersonating, True)

        controller.stop_impersonate()
        self.assertEquals(controller.is_impersonating, False)
        self.assertEquals(controller.impersonation, None)
