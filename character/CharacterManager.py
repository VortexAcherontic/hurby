from character.Blacklist import Blacklist


class CharacterManager:

     def __init__(self):
         self.chars = [None]
         self.char_ref_table = [None]
         self.black_list = Blacklist()
         self.load_char_ref_table()

     # This will load a configuration file which assosiates any possiblöe user id with his/her character json
     def load_char_ref_table(self):
         pass

     # This will check if a user with an id, wether it is twitch, YouTube or what ever, already is loaded
     # Retruns true a matching character is oaded and false if not
     def check_for_char(self, user_id, user_id_type):
         pass

     # THis will load a matching JSON by it's id. Character jsons are just counted starting by 0
     # 0.json would be the first ever created character
     # 1.json would be the 2nd char and so on
     # And will load it to the self.chars array
     def load_char(self, json_id):
         pass

     # This will store a character on disk if a user will leave the stream or disconnect from discord
     def save_char(self, char_id):
         pass

     # This will create a new default character based on the users id and the id type.
     # The ID type is basically determined by the platfrom the user has appeard
     def new_char(self, user_id, user_id_type):
         pass

     def get_black_list(self):
         return self.black_list
