import os

from hurby.character.blacklist.blacklist import Blacklist
from hurby.character.character import Character
from hurby.character.character_reference_table import CharacterReferenceTable
from hurby.character.user_id_types import UserIDType
from hurby.twitch.cmd.enums.permission_levels import PermissionLevels
from hurby.twitch.tmi.get_chatters import get_all_chatters_as_list
from hurby.utils import json_loader, logger, hurby_utils
from hurby.utils.const import CONST


class CharacterManager:

    def __init__(self, hurby):
        self.chars: list = []
        self.black_list: Blacklist = Blacklist(hurby)
        self.ref_table: CharacterReferenceTable = CharacterReferenceTable()
        self.hurby = hurby

    def get_character(self, user_id: str, user_id_type: UserIDType, permission_level=PermissionLevels.EVERYBODY,
                      update_perm_level=False, command_issued=True):
        if not self.black_list.is_name_blacklisted(user_id, user_id_type):
            tmp_char = self._search_loaded_characters(user_id, user_id_type)
            if tmp_char is None:
                tmp_char = Character(self.hurby)
                if self._is_in_reference_table(user_id):
                    json_file = self.ref_table.get_json_file_by_user_id(user_id)
                    try:
                        tmp_char.load(json_file)
                        self._add_char_to_table(tmp_char)
                    except FileNotFoundError:
                        logger.log(logger.ERR, "File " + json_file + " not found for user: " + user_id)
                else :
                    tmp_char.init_default_character(user_id, permission_level, user_id_type)
                    tmp_char.save()
                    self._add_char_to_table(tmp_char)
                    self._add_char_to_ref_table(tmp_char, user_id_type)
            if update_perm_level:
                #logger.log(logger.DEV, "Updating permission level for " + user_id + " to: " + permission_level.value)
                tmp_char.set_permission_level(permission_level)
                tmp_char.save()
            return tmp_char
        return None

    def get_character_by_uuid(self, uuid: str):
        for c in self.chars:
            if c is not None:
                if c.uuid == uuid:
                    return c
        return None

    def get_characters(self):
        return self.chars

    def delete_character(self, user_name, user_id_type):
        if user_id_type is UserIDType.TWITCH:
            file_name = self.ref_table.get_json_file_by_user_id(user_name)
            if file_name is not None:
                absolute_file_name = CONST.DIR_CHARACTERS_ABSOLUTE + "/" + file_name
                self.ref_table.remove_from_table(user_name, user_id_type)
                os.remove(absolute_file_name)

    def unload_offline_characters(self, channels: list, user_id_type: UserIDType):
        all_alive_chatters = get_all_chatters_as_list(channels)
        if all_alive_chatters is not None:
            for char in self.chars:
                if char is not None:
                    char_offline = True
                    for alive in all_alive_chatters:
                        if alive == char.twitchid:
                            char_offline = False
                    if char_offline:
                        self._unload_character(char)

    def _unload_character(self, character: Character):
        logger.log(logger.DEV, "User offline, unloading: " + str(character.twitchid))
        character.save()
        self.chars.remove(character)
        self._find_unused_character_files()

    def _add_char_to_table(self, char: Character):
        self.chars.append(char)

    def _search_loaded_characters(self, user_id: str, user_id_type: UserIDType):
        if self.chars is not None:
            for tmp in self.chars:
                if tmp is not None:
                    if user_id_type == UserIDType.TWITCH:
                        if user_id == tmp.twitchid:
                            return tmp
                    elif user_id_type == UserIDType.TWITTER:
                        pass
                    elif user_id_type == UserIDType.PATREON:
                        pass
                    elif user_id_type == UserIDType.YOUTUBE:
                        pass
                    elif user_id_type == UserIDType.STEAM:
                        pass
                    elif user_id_type == UserIDType.DISCORD:
                        pass
        return None

    def _is_in_reference_table(self, user_id: str):
        return self.ref_table.check_user_id(user_id)

    def _add_char_to_ref_table(self, character: Character, user_id_type: UserIDType):
        if user_id_type == UserIDType.TWITCH:
            self.ref_table.add_to_ref_table(character.twitchid, character.uuid)

    def _find_unused_character_files(self):
        char_files = hurby_utils.get_all_files_in_path(CONST.DIR_CHARACTERS_ABSOLUTE)
        excluded_files = [CONST.FILE_BLACKLIST, CONST.FILE_CHAR_REF_TABLE]
        for file in char_files:
            if file not in excluded_files:
                if not self.ref_table.check_uuid_file(file):
                    file_cont = json_loader.load_json(CONST.DIR_CHARACTERS_ABSOLUTE + "/" + file)
                    try:
                        logger.log(logger.WARN,
                                   ["User " + file_cont["twitchid"] + " for uuid " + str(file) + " does not exist!" +
                                    " File removed!"])
                        os.remove(CONST.DIR_CHARACTERS_ABSOLUTE + "/" + file)

                    except KeyError as e:
                        logger.log(logger.ERR, ["File: " + file + " could not be verified for existing user\n", str(e)])
                    except TypeError as e:
                        logger.log(logger.ERR, ["File: " + file + " could not be verified for existing user\n", str(e)])
