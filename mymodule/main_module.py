from twitter2 import *
from create_map import *

name_1 = "realDonaldTrump"

names_list = return_list_with_locations(get_locations_from_list(file_writing_func(name_1)))

save_html_map(names_list)