#           Copyright Alexander Malahov 2018.
#  Distributed under the Boost Software License, Version 1.0.
#     (See accompanying file LICENSE.txt or copy at
#           http://www.boost.org/LICENSE_1_0.txt)


import unohelper

# noinspection PyUnresolvedReferences
from com.sun.star.task import XJobExecutor

import logging as log
import os.path


LOG_FILE_PATH = os.path.normpath(os.path.expanduser('~/hello-libreoffice-ext.log'))
log.basicConfig(
    # '~' will be expanded to: 'C:\Users\my-user-name\' on Windows, '/home/my-user-name/' on Linux
    filename=LOG_FILE_PATH,
    format='%(asctime)s [%(levelname)s] %(message)s',
    level=log.DEBUG)
log.info('Hi from logging! Module entered')


def createService(name, context):
    return context.ServiceManager.createInstanceWithContext(name, context)


class OfficeUi:

    # value from https://api.libreoffice.org/docs/idl/ref/namespacecom_1_1sun_1_1star_1_1awt_1_1MessageBoxButtons.html
    MSG_BOX_BUTTONS_OK = 1

    def __init__(self, context):
        self._context = context
        desktop = createService('com.sun.star.frame.Desktop', self._context)
        self._window = desktop.getComponentWindow()
        self._toolkit = createService('com.sun.star.awt.Toolkit', self._context)

    def messageBox(self, message, title='Extension example'):
        # noinspection PyUnresolvedReferences
        from com.sun.star.awt.MessageBoxType import MESSAGEBOX

        box = self._toolkit.createMessageBox(self._window, MESSAGEBOX, self.MSG_BOX_BUTTONS_OK, title, message)

        return box.execute()


class ExampleExtension(unohelper.Base, XJobExecutor):

    # IMPORTANT. This must be the same string as description.xml::<identifier value>
    IMPLEMENTATION_NAME = 'com.github.amalahov.hellooffice.n14'

    def __init__(self, context, *args):
        log.info('constructor invoked')
        self._context = context

    # methods from XJobExecutor
    def trigger(self, args):
        log.info('trigger called')
        ui = OfficeUi(self._context)
        ui.messageBox('Hello from Extension!\nArgs are: ' + str(args) + '\nLogs are saved to ' + LOG_FILE_PATH)


g_ImplementationHelper = unohelper.ImplementationHelper()
g_ImplementationHelper.addImplementation(ExampleExtension, ExampleExtension.IMPLEMENTATION_NAME, ())
