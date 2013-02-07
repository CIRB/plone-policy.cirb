from setuptools import setup, find_packages
import os

version = '1.2.2.dev0'

long_description = (
        open('README.txt').read()
        + '\n' +
        'Contributors\n'
        '============\n'
        + '\n' +
        open('CONTRIBUTORS.txt').read()
        + '\n' +
        open('CHANGES.txt').read()
        + '\n')

setup(name='policy.cirb',
        version=version,
        description="'policy of CIRB-CIBG site'",
        long_description=long_description,
        # Get more strings from
        # http://pypi.python.org/pypi?%3Aaction=list_classifiers
        classifiers=[
            "Programming Language :: Python",
            ],
        keywords='',
        author='',
        author_email='',
        url='http://svn.plone.org/svn/collective/',
        license='gpl',
        packages=find_packages('src'),
        package_dir = {'': 'src'},
        namespace_packages=['policy', ],
        include_package_data=True,
        zip_safe=False,
        install_requires=[
            'setuptools',
            # -*- Extra requirements: -*-
            'plonetheme.cirb',
            'Products.PloneFormGen',
            'collective.ckeditor',
            'collective.plonefinder',
            'collective.quickupload',
            'quintagroup.analytics',
            'fourdigits.portlet.twitter',
            'collective.anysurfer',
            'Products.PloneHelpCenter',
            'collective.contentstats',
            'collective.recaptcha',
            'Products.CirbCountdown',
            'Products.Collage',
            'webcouturier.dropdownmenu',
            'collective.collage.portlets',
            'cirb.zopemonitoring',
            'cirb.blog',
            #extra feature for blog
            'archetypes.linguakeywordwidget',
            'collective.categories',
            'collective.diggdigg',
            'collective.portlet.oembed',
            'collective.portlet.twittermultistream',
            'collective.portlet.socialnetworks',
            #/blog
            'plone.api',  # to make upgrade steps easier to write
            #'plone.app.multilingual',
            #'plone.multilingualbehavior',
            ],
        extras_require={'test': ['plone.app.testing']},
        entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
