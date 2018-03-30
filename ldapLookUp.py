#----------------------------------------------
# Function that returns a users full name in AD
#
# by Sean Conrad
#----------------------------------------------

import re
import ldap

def findFullName (username, pwd):
    # Stores username and ldap server in variabls
    dn = username + ("DOMAIN")
    con = ldap.initialize('LDAP SERVER')

    # Attempts to bind and create connection to server
    try:
        con.simple_bind_s(dn, pwd)
    except ldap.INVALID_CREDENTIALS:
        print 'Bad Credentials'

    # Not sure what this is but leaving it because it works XD
    con.protocol_version = ldap.VERSION3

    # Burrows down the AD hierarchy. This stops right before selecting the Site OU to
    # find all users in PP
    baseDN = "OU"

    #Unsure what this is
    searchScope = ldap.SCOPE_SUBTREE

    # This is the account we query for
    searchFilter = "sAMAccountName=" + username

    # Retrieve all attributes, adjust to your needs
    # Selected this attribute because it contains user's full name
    searchAttribute = ["gecos"]

    # Combines everything in to a parameter to search in AD
    try:
        ldap_result_id = con.search(baseDN, searchScope, searchFilter, searchAttribute)
        # Returns result in a list
        result_set = []
        while 1:
            # Not sure entirely what this does
            result_type, result_data = con.result(ldap_result_id, 0)
            if (result_data == []):
                break
            else:
                ## here you don't have to append to a list
                ## you could do whatever you want with the individual entry
                ## The appending to list is just for illustration.
                if result_type == ldap.RES_SEARCH_ENTRY:
                    result_set.append(result_data)


    except ldap.LDAPError, e:
        print 'Ldap Error'

    #Transform string to get what I need


    a = result_set[0]

    # More string transformation, don't remember what this does off the top of my head.
    str1 = ''.join(str(e) for e in a)
    str2 = str(str1)

    # Perform regular expression to cut out what I need and assing to 'm' then assigns 'm' to 'b'.
    regex = r"\['\w+, \w+"
    m = re.search(regex, str2)
    b = m.group(0)

    #
    words = b.split(",")

    # Flips from last name to first name, to first name to last name and cuts out no needed characters
    finalTransformation = words[1][1:] + " " + words[0][2:]

    # When this function is called it returns a user's full name
    print finalTransformation
    return finalTransformation
