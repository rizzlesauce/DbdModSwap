#!/usr/bin/env python3
"""
Module Docstring
"""

import argparse
import sys

from dbdmodswap.helpers.consoleHelpers import sprint, sprintPad
from dbdmodswap.helpers.customizationItemDbHelpers import \
    CustomizationItemDbAssetName
from dbdmodswap.helpers.pakHelpers import UnrealPakProgramFilename
from dbdmodswap.helpers.pathHelpers import getPathInfo
from dbdmodswap.helpers.settingsHelpers import (DefaultAttachmentsDir,
                                                DefaultPakingDir,
                                                DefaultSettingsPath,
                                                getEnabledDisabledStr)
from dbdmodswap.helpers.uassetHelpers import (UassetGuiProgramFilename,
                                              UassetGuiProgramStem)
from dbdmodswap.helpers.windowsHelpers import setConsoleTitle
from dbdmodswap.metadata.programMetaData import (ConsoleTitle, ProgramName,
                                                 Version)
from dbdmodswap.runtime.runCommand import DefaultLauncherStartsGame, runCommand
from dbdmodswap.runtime.runMenu import runMenu

__author__ = 'Ross Adamson'
__version__ = Version
__license__ = 'MIT'

if __name__ == '__main__':
    """ This is executed when run from the command line """
    parser = argparse.ArgumentParser(
        prog=ProgramName,
        description='''Swaps mods and character model accessories

Running with no arguments opens the interactive menu. To get started, configure the
game folder by selecting `MoreOptions`, `GameDir` and choosing the game folder from
the file browser that opens. Then, select `List` from the menu to create a settings
file with helpful inline documentation. Select `Edit` from the menu to edit the
settings file, configuring `modGroups` and `modConfigs`. Finally, run `ActiveModConfig`,
`Install`, and `Launcher` to start the game with your selected mod configuration.
'''.format(
            ProgramName=ProgramName,
            CustomizationItemDbResourceName=CustomizationItemDbAssetName,
            UassetGuiProgramStem=UassetGuiProgramStem,
        ),
    )
    parser.add_argument(
        'settingsFile',
        help=f'path to settings YAML file (default: `{getPathInfo(DefaultSettingsPath)["best"]}`)',
        type=str,
        nargs='?',
    )
    parser.add_argument(
        '--gameDir',
        help='game folder',
        type=str,
    )
    parser.add_argument(
        '--pakingDir',
        help=f'pakchunks storage folder (default: `{getPathInfo(DefaultPakingDir)["best"]}`)',
        type=str,
    )
    parser.add_argument(
        '--attachmentsDir',
        help=f'attachment definitions storage folder (default: `{getPathInfo(DefaultAttachmentsDir)["best"]}`)',
        type=str,
    )
    parser.add_argument(
        '--unrealProjectDir',
        help='Unreal Engine project folder',
        type=str,
    )
    parser.add_argument(
        '--uassetGuiPath',
        help=f'path to {UassetGuiProgramFilename}',
        type=str,
    )
    parser.add_argument(
        '--unrealPakPath',
        help=f'path to {UnrealPakProgramFilename}',
        type=str,
    )
    parser.add_argument(
        '--activeModConfig',
        help=f'override active mod configuration',
        type=str,
    )
    parser.add_argument(
        '--list',
        help='list, inspect, and collect data (and create a settings file if needed)',
        action='store_true',
    )
    parser.add_argument(
        '--create',
        help='create socket attachment definitions interactively',
        action='store_true',
    )
    parser.add_argument(
        '--extract',
        help='extract socket attachment definitions',
        action='store_true',
    )
    parser.add_argument(
        '--rename',
        help='rename each attachment file to match its attachment name',
        action='store_true',
    )
    parser.add_argument(
        '--mix',
        help='mix socket attachments with character models',
        action='store_true',
    )
    parser.add_argument(
        '--pak',
        help='pak content into a pakchunk',
        action='store_true',
    )
    parser.add_argument(
        '--install',
        help='apply the active mod config to the game',
        action='store_true',
    )
    parser.add_argument(
        '--launcher',
        help='enter game launcher menu (and optionally auto launch the game)',
        action='store_true',
    )
    parser.add_argument(
        '--autoLaunch',
        help=f'automatically start the game when entering the launcher menu (default: {getEnabledDisabledStr(DefaultLauncherStartsGame)})',
        action=argparse.BooleanOptionalAction,
    )
    parser.add_argument(
        '--kill',
        help='end game processes if they are running',
        action='store_true',
    )
    parser.add_argument(
        '--overwrite',
        help='overwrite existing files (default: ask to confirm)',
        action=argparse.BooleanOptionalAction,
    )
    parser.add_argument(
        '--dryRun',
        help='simulate actions without making any changes (may still write temporary files)',
        action='store_true',
    )
    parser.add_argument(
        '--debug',
        help='output extra info to the console',
        action='store_true',
    )
    parser.add_argument(
        '-ni',
        help='run non-interactively',
        action='store_true',
    )
    parser.add_argument(
        '--version',
        action='version',
        version=f'%(prog)s {Version}',
    )
    args = parser.parse_args()

    setConsoleTitle(ConsoleTitle)

    if args.ni:
        sprint('Running in non-interactive mode.')

    if (
        not args.list
        and not args.extract
        and not args.create
        and not args.rename
        and not args.mix
        and not args.pak
        and not args.install
        and not args.launcher
        and not args.kill
        and not args.ni
    ):
        exitCode = runMenu(args, parser)
    else:
        exitCode = runCommand(
            settingsFilePath=args.settingsFile,
            gameDir=args.gameDir,
            pakingDir=args.pakingDir,
            attachmentsDir=args.attachmentsDir,
            unrealProjectDir=args.unrealProjectDir,
            activeModConfigName=args.activeModConfig,
            inspecting=args.list,
            creatingAttachments=args.create,
            extractingAttachments=args.extract,
            renamingAttachmentFiles=args.rename,
            mixingAttachments=args.mix,
            paking=args.pak,
            installingMods=args.install,
            openingGameLauncher=args.launcher,
            launcherStartsGame=args.autoLaunch,
            killingGame=args.kill,
            uassetGuiPath=args.uassetGuiPath,
            unrealPakPath=args.unrealPakPath,
            dryRun=args.dryRun,
            overwriteOverride=args.overwrite,
            debug=args.debug,
            nonInteractive=args.ni,
        )

    # TODO: remove
    if False:
        if not len(sys.argv) > 1:
            sprintPad()
            sprint(f'run `{parser.prog} -h` for more options and usage.')
            sprintPad()

    sys.exit(exitCode)
