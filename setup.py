#!/usr/bin/env python3
import sys

from setuptools import setup

import hurby

if sys.version_info < (3, 10):
    sys.exit('Python >= 3.10 is required to run Hurby')

setup(
    name='hurby',
    version="0.0.1",
    license='GPL-3',
    author='Imo "Vortex Acherontic" Hester',
    author_email='vortex@z-ray.de',
    packages=[
        'hurby',
        'hurby.character',
        'hurby.character.blacklist',
        'hurby.character.exceptions',
        'hurby.config',
        'hurby.items',
        'hurby.modules',
        'hurby.modules.lottery',
        'hurby.twitch',
        'hurby.twitch.cmd',
        'hurby.twitch.cmd.actions',
        'hurby.twitch.cmd.actions.items',
        'hurby.twitch.cmd.enums',
        'hurby.twitch.cmd.events',
        'hurby.twitch.helix',
        'hurby.twitch.irc',
        'hurby.twitch.irc.threads',
        'hurby.twitch.irc.threads.crawler',
        'hurby.twitch.minigame',
        'hurby.twitch.tmi',
        'hurby.utils',
    ],
    entry_points={
        'console_scripts': [
            'hurby = hurby.run',
        ]
    },
    data_files=[],
    zip_safe=False,
    install_requires=[
        'flask',
        'requests'
    ],
    url='https://z-ray.de/software/hurby-twitch-und-social-media-bot/',
    description='Social Media Bot',
    long_description="""Hurby helps you to entertain your viewers on Twitch or to post automatic live notifications to
    your Discord or Twtitter Feed.""",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: End Users/Server',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python',
        'Operating System :: Linux',
        'Topic :: Games/Entertainment'
    ],
)