
def handle_uploaded_file(file):
    # Do sth
    return


#=====================================================================================================

def check_mac_formatting(mac_address):
    """
    Takes a MAC address string in uppercase or lowercase without colons,
    checks its format, and returns it in lowercase with colons.

    :param mac: A string representing a MAC address in uppercase or lowercase without colons
    :return: Formatted MAC address in lowercase with colons, or
             a message indicating an invalid format
    """
    formatted_mac_with_colon = mac_address.lower()
    formatted_mac_without_colon = mac_address.lower()

    if len(mac_address) == 12 :
        formatted_mac_with_colon = ":".join(formatted_mac_with_colon[i:i+2] for i in range(0, 12, 2))
    else:
        formatted_mac_without_colon.replace(":", "")

    return formatted_mac_with_colon, formatted_mac_without_colon