# how to run
#
# "Onboard Options list"
# "--------------------"
# "(1) Jenkins"
# "(2) Pritunl"
# "(3) Rollbar"
# "(4) Scout APM"
# "(5) Papertrail"
# "(6) Sentry - Jurnal"
#
# command:
# python onboard.py "<username>" "<full_name>" "<email>" "<options_list>"
#
# example:
# python onboard.py "rudy" "Rudy Pangestu" "rudy@mekari.com" "1, 3"
import sys
import jenkins_provider as jp
import pritunl_provider as pp
import rollbar_provider as rp
import scout_provider as sp
import papertrail_provider as ptp
import sentry_provider as stp

def jenkins_onboard(username, full_name, email):
    provider = jp.JenkinsProvider(username, full_name, email)
    provider.onboard()

def pritunl_onboard(username, _full_name, email):
    provider = pp.PritunlProvider(username, email)
    provider.onboard()

def rollbar_onboard(_username, _full_name, email):
    provider = rp.RollbarProvider(email)
    provider.onboard()

def scout_onboard(_username, _full_name, email):
    provider = sp.ScoutProvider(email)
    provider.onboard()

def papertrail_provider(_username, _full_name, email):
    provider = ptp.PapertrailProvider(email)
    provider.onboard()

def sentry_provider(_username, _full_name, email):
    provider = stp.SentryProvider(email)
    provider.onboard()

def string_argument(argument_index):
    return "".join(sys.argv[argument_index])

onboard_options = {
    1: jenkins_onboard,
    2: pritunl_onboard,
    3: rollbar_onboard,
    4: scout_onboard,
    5: papertrail_provider,
    6: sentry_provider
}

if __name__ == '__main__':
    print("Onboard Options list")
    print("--------------------")
    print("(1) Jenkins")
    print("(2) Pritunl")
    print("(3) Rollbar")
    print("(4) Scout APM")
    print("(5) Papetrail")
    print("(6) Sentry - Jurnal")
    print("--------------------")

    username = string_argument(1)
    full_name = string_argument(2)
    email = string_argument(3)
    options = string_argument(4)

    print("Username is '" + username + "'")
    print("Fullname is '" + full_name + "'")
    print("Email is '" + email + "'")
    print("Chosen options is '" + options + "'")

    for option in options.split(","):
        num_option = int(option)
        onboard_options[num_option](username, full_name, email)
