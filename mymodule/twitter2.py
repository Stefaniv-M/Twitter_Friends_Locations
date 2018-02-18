import urllib.request, urllib.parse, urllib.error
import twurl
import json
import ssl

# https://apps.twitter.com/
# Create App and get the four strings, put them in hidden.py

TWITTER_URL = 'https://api.twitter.com/1.1/friends/list.json'

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


def file_writing_func(name_str_1):
    """
    :param name_str_1: str
    :return: result_list: list
    This function writes information from web into list of string lines result_list. It looks up information
    about twitter user with name name_str_1.
    """
    try:
        text_str = ""

        text_str += "\n"
        acct = name_str_1
        if (len(acct) < 1):
            return []

        url = twurl.augment(TWITTER_URL,
                            {'screen_name': acct, 'count': '200'})
        text_str += 'Retrieving ' + str(url) + "\n"
        connection = urllib.request.urlopen(url, context=ctx)
        data = connection.read().decode()

        js = json.loads(data)
        text_str += str(json.dumps(js, indent=2)) + "\n"

        headers = dict(connection.getheaders())
        text_str += 'Remaining ' + str(headers['x-rate-limit-remaining']) + "\n"

        for u in js['users']:
            text_str += str(u['screen_name']) + "\n"
            if 'status' not in u:
                text_str += '   * No status found\n'
                continue
            s = u['status']['text']

            text_str += '   ' + str(s[:50]) + "\n"

        return text_str.split("\n")

    except:
        return []


def get_locations_from_list(list_1):
    """
    :param list_1: list
    :return: result_list: list of tuple

    This function returns list of tuples, each containing three elements: id of the user, name of the user, and
    tuple with location of the user, all str.
    """
    result_list = []
    len_1 = len(list_1)

    # Now I will add four empty lines to initial list so that program won't search non-existent elements later
    # and for the list to be checked completely:
    list_1 += ['', '', '', '']

    # i is just integer cursor:
    for i in range(len_1):
        if (list_1[i].startswith('      "id_str":')
            and list_1[i + 1].startswith('      "name":')
            and list_1[i + 3].startswith('      "location":')
        ):
            id_1 = list_1[i][17:-2]
            name_1 = list_1[i + 1][15:-2]
            location_1 = list_1[i + 3][19:-2]

            # Now let's add those values to the list as a tuple:
            result_list.append(tuple([id_1, name_1, location_1]))

    return result_list


def get_location(location_name):
    """
    (str) -> (float, float) or None
    This function returns location of film. Arguement is a
    last element of <line_in_list_file>.split("\t")[-1]. If
    function can find latitude and longitude of place, it returns
    those values, otherwise it will try to find address of last
    word of location. If it fails even it, the function returns None.
    """
    import geopy

    # For me to type less:
    geostuff = geopy.geocoders.Nominatim()

    try:
        location_1 = geostuff.geocode(location_name)
        return location_1.latitude, location_1.longitude
    except:
        try:
            # If geopy can't find place by it's full address, it will search the last word:
            location_1 = geostuff.geocode(location_name.split(" ")[-1])
            return location_1.latitude, location_1.longitude
        except:
            return None


def return_list_with_locations(list_1):
    """
    This funciton gets list of tuples with last element as string location, and by using module geopy
    returns similar list, but in new list instead of last element there is a tuple with latitude and
    longitude of place. If system can't find latitude and longitude of place, or if element is empty,
    function does not add tuple with this place into result_list, which it returns.
    :param list_1: list of tuple
    :return: result_list: list
    """
    result_list = []

    for tuple_1 in list_1:
        if tuple_1[2] != "":
            try:
                location_1 = tuple(get_location(tuple_1[2]))
            except:
                location_1 = None
            if location_1 is not None:
                result_list.append(tuple([tuple_1[0], tuple_1[1], location_1]))

    return result_list




# print(return_list_with_locations(get_locations_from_list(file_writing_func("realDonaldTrump"))))
