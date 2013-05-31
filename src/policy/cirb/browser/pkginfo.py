from Products.Five import BrowserView
import sys
import os


class PkginfoView(BrowserView):

    def __call__(self):
        installed = []
        for egg in sys.path:
            if egg.endswith('.egg'):
                installed.append(egg.split(os.sep)[-1])

        installed.sort()
        return "\n".join(installed)
