-- Copyright 2007 The Omni Group.  All rights reserved.
-- I made modifications to The Omni Group's "MailAction.applescript", resulting in what you see below. - Jay Parlar

using terms from application "Mail"
	-- Trims "foo <foo@bar.com>" down to "foo@bar.com"
	on trim_address(theAddress)
		try
			set AppleScript's text item delimiters to "<"
			set WithoutPrefix to item 2 of theAddress's text items
			set AppleScript's text item delimiters to ">"
			set MyResult to item 1 of WithoutPrefix's text items
		on error
			set MyResult to theAddress
		end try
		set AppleScript's text item delimiters to {""} --> restore delimiters to default value
		return MyResult
	end trim_address
	
	
	on process_message(theMessage)
		-- Allow the user to type in the full sender address in case our trimming logic doesn't handle the address they are using.
		set theSender to sender of theMessage
		set trimmedSender to my trim_address(theSender)
        set allowedSender to {"parlar@gmail.com", "jay@parlar.ca"}
        if allowedSender does not contain trimmedSender and allowedSender does not contain theSender then
            return
        end if
        
		
        set theNote to content of theMessage
		set theSubject to subject of theMessage
        set theType to text 1 through 2 of theSubject
        set theNumber to text 3 through -1 of theSubject
        tell application "Keyboard Maestro Engine"
            make variable with properties {name:"callerid", value:theNumber }
            make variable with properties {name:"short_action", value:theType }
            make variable with properties {name:"note", value:theNote }
            do script "55358B8F-ADBA-465E-BF1A-9073F34591BD"
        end tell
	end process_message
	
	on perform mail action with messages theMessages
        set theMessageCount to count of theMessages
        repeat with theMessageIndex from 1 to theMessageCount
            my process_message(item theMessageIndex of theMessages)
        end repeat
	end perform mail action with messages
end using terms from



