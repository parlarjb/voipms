## Description ##
In theory, this is a library for interacting with the voip.ms JSON API. 
In reality, I've only implemented enough of the API for reading and writing caller ID filter entries.

### voipms.py ##
This is the wrapper around the API. The idea is that you write individual methods like `get_callerid_filtering` and `create_callerid_filter` which put together information in the "right way" for the low level `method_call` method.

Note that if you call `get_callerid_filtering` with no arguments, then voip.ms will return *all* the caller ID filters for the account.

### transfer_filters.py ###

This is a script that takes advantage of `voipms.py`. It takes five arguments on the command line:

    1. Username of the "old" voip.ms account
    2. Password for this account
    3. Username of the "new" voip.ms account
    4. Password for this account
    5. ID of the IVR in the new account

In my situation, the old account is the one that had a nice large caller ID filter list, which I've built myself over time. The new account is a second voip.ms account I've created for my business. I wanted to automatically transfer my filter list from the old account to the new one.

The IVR ID is specific to my uses. I have a single IVR defined for voip.ms, a "Possible telemarketer" interceptor. When a call comes in matching specific criteria (in my case, 800\*, 866\*, 888\*), they get intercepted by an Interactive Voice Response menu. It tells them to press 1 if they're not a telemarketer, 2 if they are. The system hangs up on them if they press 2.

I have essentially the same IVR defined in both of my voip.ms accounts, but voip.ms (understandably) assigns unique IDs to them. So the fifth argument is the ID that voip.ms assigned to the IVR I created in my new account. Whenever this script encounters an IVR-based rule from the old account, it creates a corresponding rule in the new account, but with the correct IVR ID.

### add_filter.py ###
This is a script for adding the same caller ID filter to multiple voip.ms accounts. When I receive a telemarketer call to one of my lines, I want to make sure that that telemarketer can never again call *any* of my accounts. 

### run_through_km.applescript ###

This is an AppleScript that can be used as a rule for Mail.app. When I send an email to a special address (defined in Mail.app) from one of the addresses listed in "allowedSender", with a subject line:
    
    h 5555555555

or

    i 5555555555

(where `h` and `i` stand for "hangup" and "IVR")

then a new caller ID rule will be created. Whatever I put in the subject of the email will be added as the note of the rule.

Please note that this AppleScript calls out to Keyboard Maestro. So you need Keyboard Maestro installed to actually make this work. I'm sure there's a way to do it without, but I haven't looked into it. The role Keyboard Maestro plays here is to take the variables from the AppleScript and feed them to `add_filter.py`. There's probably a way to directly call shell scripts from AppleScript, and if so, I can remove Keyboard Maestro from the equation.

## Usage Notes ##
To use this, make sure you've turned on API support in your voip.ms accounts. Then it should just be a matter of running whichever script you need.
