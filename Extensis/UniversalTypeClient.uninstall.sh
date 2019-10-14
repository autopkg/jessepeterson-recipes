#!/bin/bash

# Enable global debugging of script
## Set to "on" to echo additional comments to screen
## Set to "off" or simply comment out for production
# ECHO_DEBUG=on


: <<TITLE
*
* Universal Type Client Removal Tool
* Removes version v1.0.0 through v7.0.2
* on Mac OS X 10.4.11 through macOS 10.14
* Web: http://www.extensis.com/support
* Email: support@extensis.com
* Last Updated 2019-04-24
*
TITLE

##
## GOALS
##

: <<GOALS

1) remove all universal type client files except logs

2) syntax conventions in effect:
	# i am a comment i.e. comments are prefixed wih a number sign (#) and will not print/run
	I_AM_A_VARIABLE = multi word variables are all caps with underscores
	function_i_am_a_function = function names are prefixed with the word "function" and are all lowercase with underscores
	i-am-a-filename.txt = filenames are all lowercase and dashed

GOALS

##
## LIST ALL FUNCTIONS IN ALPHA ORDER
##


#----------------------------
ECHO_DEBUG ()
#----------------------------
{

# goal of function:
# this function checks for errors to aid in debugging
# will echo passed parameters only if ECHO_DEBUG is set to "on" in header of script
# yes, ECHO_DEBUG breaks our syntax conventions in favor of readability when debugging.
# i grow old, i grow old, i shall wear the bottoms of my trousers rolled ..."
[ "$ECHO_DEBUG" = "on" ] &&  $@

}  # end of function ECHO_DEBUG


#----------------------------
function_letterhead ()
#----------------------------
{

# goal of function:
# print a "letterhead" to screen; 50 characters
# this prints "as is" spaces, new lines and all

ECHO_DEBUG echo "[DEBUG] i am function_letterhead"

cat <<LETTERHEAD

*
* Universal Type Client Removal Tool
* Removes version v1.0.0 through v6.1.5
* on Mac OS X 10.4.11 through macOS 10.13
* http://www.extensis.com/support
*
* Please follow all instructions carefully
* and use at your own risk
*

LETTERHEAD

}  # end of function "letterhead"


#----------------------------
function_remove_UTC ()
#----------------------------
{

# goal of function:
## remove all components of UTC except for logs

ECHO_DEBUG echo "[DEBUG] i am function_remove UTC"

echo "Closing System Preferences ..."
# close system preferences on osx 10.7, 10.6 and 10.5 machines in case UTCore preference panel is open
# note: unable to close on 10.4 machine
SYSTEM_PREFERENCES=$(ps -ax | grep -i "/Applications/System Preferences.app/Contents/MacOS/System Preferences" | grep -vi "grep" | awk ' { print $1 } ')
if [ -n "$SYSTEM_PREFERENCES" ]; then
	sudo kill -s KILL "$SYSTEM_PREFERENCES" > /dev/null 2>&1
	sleep 3
fi
echo "... Done"

# stop the QuickMatch process called QMRenderer
echo "Shutting down QuickMatch/QMRenderer ..."
QUICK_MATCH=$(ps -ax | grep -i "/Applications/Universal Type Client.app/Contents/Resources/QMRenderer" | grep -vi "grep" | awk ' { print $1 } ')
if [ -n "$QUICK_MATCH" ]; then
	sudo kill -s KILL "$QUICK_MATCH" > /dev/null 2>&1
	sleep 3
fi
echo "... Done"

## stop the FMCore process for v2 thru v6
echo "Shutting down Universal Type Core ..."
UTCORE_NEW=$(ps -ax | grep -i "Universal Type Client.app/Contents/Resources/FMCore" | grep -vi "grep" | awk ' { print $1 } ')
while [ -n "$UTCORE_NEW" ]; do
	sudo kill -s KILL "$UTCORE_NEW" > /dev/null 2>&1
	UTCORE_NEW=$(ps -ax | grep -i "Universal Type Client.app/Contents/Resources/FMCore" | grep -vi "grep" | awk ' { print $1 } ')
done

## stop the UTCore process for v1
UTCORE_OLD=$(ps -ax | grep -i "Universal Type Client.app/Contents/Resources/UTCore" | grep -vi "grep" | awk ' { print $1 } ')
while [ -n "$UTCORE_OLD" ]; do
	sudo kill -s KILL "$UTCORE_OLD" > /dev/null 2>&1
	UTCORE_OLD=$(ps -ax | grep -i "Universal Type Client.app/Contents/Resources/UTCore" | grep -vi "grep" | awk ' { print $1 } ')
done
echo "... Done"

# stop the app
echo "Shutting down $APP application ..."
UTC_APPLICATION=$(ps -ax | grep -i "Universal Type Client.app/Contents/MacOS/Universal Type Client" | grep -vi "grep" | awk ' { print $1 } ')
if [ -n "$UTC_APPLICATION" ]; then
	sudo kill -s KILL "$UTC_APPLICATION" > /dev/null 2>&1
fi
sleep 3
echo "... Done"

# remove the application
echo "Removing $APP application ..."
sudo rm -rf "/Applications/Universal Type Client.app" > /dev/null 2>&1
echo "... Done"

# remove the plugin frameworks, launch agent and ut-core prefpane
echo "Removing $APP plugin frameworks ..."
sudo rm -rf "/Library/Frameworks/ExtensisFontManagement.framework" > /dev/null 2>&1
sudo rm -rf "/Library/Frameworks/ExtensisPluginInterface.framework" > /dev/null 2>&1
sudo rm -rf "/Library/Frameworks/ExtensisPlugins.framework" > /dev/null 2>&1
sudo rm -rf "/Library/LaunchAgents/com.extensis.FMCore.plist" > /dev/null 2>&1
sudo rm -rf "/Library/PreferencePanes/utcore-prefpane.prefPane" > /dev/null 2>&1
echo "... Done"

# remove launch agent
echo "Removing $APP launch agent..."
sudo rm -rf "/Library/LaunchAgents/com.extensis.FMCore.plist" > /dev/null 2>&1
sudo rm -rf "/private/var/run/SCHelper" > /dev/null 2>&1
echo "... Done"

# remove optional config file
echo "Removing $APP config file ..."
sudo rm -rf "/Library/Preferences/com.extensis.UniversalTypeClient.conf"  > /dev/null 2>&1
sudo rm -rf  "/Library/Preferences/com.extensis.TypeServerCoreClient.conf"  > /dev/null 2>&1
echo "... Done"

# remove the user preferences and odds and ends for all user accounts
echo "Removing $APP preference files for all user accounts ..."
# create a variable for all users accounts.
## note: use ls -1 (one) not ls -l (larry)
USERS="$(ls -1 /Users)"
for USERDIR in $USERS; do
	sudo rm -rf "/Users/$USERDIR/.Extensis" > /dev/null 2>&1
	sudo rm -rf "/Users/$USERDIR/.UTCore" > /dev/null 2>&1
	sudo rm -rf "/Users/$USERDIR/Library/Preferences/com.extensis.FontManagement.plugins.*" > /dev/null 2>&1
	sudo rm -rf "/Users/$USERDIR/Library/Preferences/com.extensis.utcore-prefpane.plist" > /dev/null 2>&1
	sudo rm -rf "/Users/$USERDIR/Library/Preferences/com.extensis.UniversalTypeClient.db" > /dev/null 2>&1
	sudo rm -rf "/Users/$USERDIR/Library/Preferences/com.extensis.UniversalTypeClient.plist" > /dev/null 2>&1
	sudo rm -rf "/Users/$USERDIR/Library/Preferences/com.extensis.UniversalType.plugins.*" > /dev/null 2>&1
	sudo rm -rf "/Users/$USERDIR/Library/Preferences/UTCorePrefs.db" > /dev/null 2>&1
	sudo rm -rf "/Users/$USERDIR/Library/Caches/FMCore" > /dev/null 2>&1
	#remove corecli for UTC versions 5 and below
	sudo rm -rf "/usr/bin/corecli" > /dev/null 2>&1
	#remove corecli for UTC version 6
	sudo rm -rf "/usr/local/bin/corecli" > /dev/null 2>&1
done
echo "... Done"

echo "Removing $APP plug-ins ..."
# remove the auto-activation plugins
## Universal Type Client 6x, 5x, 4x, 3x and 2x
### remove illustrator CS2, CS3, CS4, CS5, CS 5.5 (aka 5.1), CS6, CC (aka CS7), CC 2014, CC 2015.x, CC 2017, CC 2018, and CC 2019
sudo rm -rf "/Applications/Adobe Illustrator CS2/Plug-ins.localized/Extensions.localized/ExtensisFontManagementAICS2.aip" > /dev/null 2>&1
sudo rm -rf "/Applications/Adobe Illustrator CS3/Plug-ins.localized/Extensions.localized/ExtensisFontManagementAICS3.aip" > /dev/null 2>&1
sudo rm -rf "/Applications/Adobe Illustrator CS4/Plug-ins.localized/Extensions.localized/ExtensisFontManagementAICS4.aip" > /dev/null 2>&1
sudo rm -rf "/Applications/Adobe Illustrator CS5/Plug-ins.localized/Extensions.localized/ExtensisFontManagementAICS5.aip" > /dev/null 2>&1
sudo rm -rf "/Applications/Adobe Illustrator CS5.1/Plug-ins.localized/Extensions.localized/ExtensisFontManagementAICS5.aip" > /dev/null 2>&1
sudo rm -rf "/Applications/Adobe Illustrator CS6/Plug-ins.localized/Extensions.localized/ExtensisFontManagementAICS6.aip" > /dev/null 2>&1
sudo rm -rf "/Applications/Adobe Illustrator CC/Plug-ins.localized/Extensions.localized/ExtensisFontManagementAICS7.aip" > /dev/null 2>&1
sudo rm -rf "/Applications/Adobe Illustrator CC 2014/Plug-ins.localized/Extensions.localized/ExtensisFontManagementAICC2014.aip" > /dev/null 2>&1
sudo rm -rf "/Applications/Adobe Illustrator CC 2015/Plug-ins.localized/Extensions.localized/ExtensisFontManagementAICC2015.aip" > /dev/null 2>&1
sudo rm -rf "/Applications/Adobe Illustrator CC 2015.3/Plug-ins.localized/Extensions.localized/ExtensisFontManagementAICC2015.aip" > /dev/null 2>&1
sudo rm -rf "/Applications/Adobe Illustrator CC 2017/Plug-ins.localized/Extensions.localized/ExtensisFontManagementAICC2017.aip" > /dev/null 2>&1
sudo rm -rf "/Applications/Adobe Illustrator CC 2018/Plug-ins.localized/Extensions.localized/ExtensisFontManagementAICC2018.aip" > /dev/null 2>&1
sudo rm -rf "/Applications/Adobe Illustrator CC 2019/Plug-ins.localized/Extensions.localized/ExtensisFontManagementAICC2019.aip" > /dev/null 2>&1

### remove incopy CS4, CS5, CS 5.5 (aka 5.1), CS6, CC (aka CS7), CC 2014, CC 2015, CC 2017, CC 2018, and CC 2019
sudo rm -rf "/Applications/Adobe InCopy CS4/Plug-Ins/Font Activation/ExtensisFontManagementICCS4.InDesignPlugin" > /dev/null 2>&1
sudo rm -rf "/Applications/Adobe InCopy CS5/Plug-Ins/Font Activation/ExtensisFontManagementICCS5.InDesignPlugin" > /dev/null 2>&1
sudo rm -rf "/Applications/Adobe InCopy CS5.5/Plug-Ins/Font Activation/ExtensisFontManagementICCS5.5.InDesignPlugin" > /dev/null 2>&1
sudo rm -rf "/Applications/Adobe InCopy CS6/Plug-Ins/Font Activation/ExtensisFontManagementICCS6.InDesignPlugin" > /dev/null 2>&1
sudo rm -rf "/Applications/Adobe InCopy CC/Plug-Ins/Font Activation/ExtensisFontManagementICCS7.InDesignPlugin" > /dev/null 2>&1
sudo rm -rf "/Applications/Adobe InCopy CC 2014/Plug-Ins/Font Activation/ExtensisFontManagementICCC2014.InDesignPlugin" > /dev/null 2>&1
sudo rm -rf "/Applications/Adobe InCopy CC 2015/Plug-Ins/Font Activation/ExtensisFontManagementICCC2015.InDesignPlugin" > /dev/null 2>&1
sudo rm -rf "/Applications/Adobe InCopy CC 2017/Plug-Ins/Font Activation/ExtensisFontManagementICCC2017.InDesignPlugin" > /dev/null 2>&1
sudo rm -rf "/Applications/Adobe InCopy CC 2018/Plug-Ins/Font Activation/ExtensisFontManagementICCC2018.InDesignPlugin" > /dev/null 2>&1
sudo rm -rf "/Applications/Adobe InCopy CC 2019/Plug-Ins/Font Activation/ExtensisFontManagementICCC2019.InDesignPlugin" > /dev/null 2>&1

### remove indesign CS2, CS3, CS4, CS5, CS 5.5, CS6, CC (aka CS7), CC 2014, CC 2015, CC 2017, CC 2018, and CC 2019
sudo rm -rf "/Applications/Adobe InDesign CS2/Plug-Ins/Font Activation/ExtensisFontManagementIDCS2.InDesignPlugin" > /dev/null 2>&1
sudo rm -rf "/Applications/Adobe InDesign CS3/Plug-Ins/Font Activation/ExtensisFontManagementIDCS3.InDesignPlugin" > /dev/null 2>&1
sudo rm -rf "/Applications/Adobe InDesign CS4/Plug-Ins/Font Activation/ExtensisFontManagementIDCS4.InDesignPlugin" > /dev/null 2>&1
sudo rm -rf "/Applications/Adobe InDesign CS5/Plug-Ins/Font Activation/ExtensisFontManagementIDCS5.InDesignPlugin" > /dev/null 2>&1
sudo rm -rf "/Applications/Adobe InDesign CS5.5/Plug-Ins/Font Activation/ExtensisFontManagementIDCS5.5.InDesignPlugin" > /dev/null 2>&1
sudo rm -rf "/Applications/Adobe InDesign CS6/Plug-Ins/Font Activation/ExtensisFontManagementIDCS6.InDesignPlugin" > /dev/null 2>&1
sudo rm -rf "/Applications/Adobe InDesign CC/Plug-Ins/Font Activation/ExtensisFontManagementIDCS7.InDesignPlugin" > /dev/null 2>&1
sudo rm -rf "/Applications/Adobe InDesign CC 2014/Plug-Ins/Font Activation/ExtensisFontManagementIDCC2014.InDesignPlugin" > /dev/null 2>&1
sudo rm -rf "/Applications/Adobe InDesign CC 2015/Plug-Ins/Font Activation/ExtensisFontManagementIDCC2015.InDesignPlugin" > /dev/null 2>&1
sudo rm -rf "/Applications/Adobe InDesign CC 2017/Plug-Ins/Font Activation/ExtensisFontManagementIDCC2017.InDesignPlugin" > /dev/null 2>&1
sudo rm -rf "/Applications/Adobe InDesign CC 2018/Plug-Ins/Font Activation/ExtensisFontManagementIDCC2018.InDesignPlugin" > /dev/null 2>&1
sudo rm -rf "/Applications/Adobe InDesign CC 2019/Plug-Ins/Font Activation/ExtensisFontManagementIDCC2019.InDesignPlugin" > /dev/null 2>&1

### remove photoshop CS4, CS5, CS 5.5 (aka 5.1), CS6, CC (aka CS7), CC 2014, CC 2015, CC 2017, CC 2018, and CC 2019
sudo rm -rf "/Applications/Adobe Photoshop CS4/Plug-Ins/Automate/ExtensisFontManagementPSCS4.plugin" > /dev/null 2>&1
sudo rm -rf "/Applications/Adobe Photoshop CS5/Plug-Ins/Automate/ExtensisFontManagementPSCS5.plugin" > /dev/null 2>&1
sudo rm -rf "/Applications/Adobe Photoshop CS5.1/Plug-ins/Automate/ExtensisFontManagementPSCS5.plugin" > /dev/null 2>&1
sudo rm -rf "/Applications/Adobe Photoshop CS6/Plug-ins/Automate/ExtensisFontManagementPSCS6.plugin" > /dev/null 2>&1
sudo rm -rf "/Applications/Adobe Photoshop CC/Plug-ins/Automate/ExtensisFontManagementPSCS7.plugin" > /dev/null 2>&1
sudo rm -rf "/Applications/Adobe Photoshop CC 2014/Plug-Ins/Automate/ExtensisFontManagementPSCC2014.plugin" > /dev/null 2>&1
sudo rm -rf "/Applications/Adobe Photoshop CC 2015/Plug-Ins/Automate/ExtensisFontManagementPSCC2015.plugin" > /dev/null 2>&1
sudo rm -rf "/Applications/Adobe Photoshop CC 2015.5/Plug-Ins/Automate/ExtensisFontManagementPSCC2015.plugin" > /dev/null 2>&1
sudo rm -rf "/Applications/Adobe Photoshop CC 2017/Plug-Ins/Automate/ExtensisFontManagementPSCC2017.plugin" > /dev/null 2>&1
sudo rm -rf "/Applications/Adobe Photoshop CC 2018/Plug-Ins/Automate/ExtensisFontManagementPSCC2018.plugin" > /dev/null 2>&1
sudo rm -rf "/Applications/Adobe Photoshop CC 2019/Plug-Ins/Automate/ExtensisFontManagementPSCC2019.plugin" > /dev/null 2>&1

### remove After Effects plugins from CC 2015.x and CC 2017, CC 2018, and CC 2019
sudo rm -rf "/Applications/Adobe After Effects CC 2015/Plug-ins/Extensions/ExtensisFontManagementAECC2015.plugin"  > /dev/null 2>&1
sudo rm -rf "/Applications/Adobe After Effects CC 2015.3/Plug-ins/Extensions/ExtensisFontManagementAECC2015.plugin"  > /dev/null 2>&1
sudo rm -rf "/Applications/Adobe After Effects CC 2017/Plug-Ins/Extensions/ExtensisFontManagementAECC2017.plugin" > /dev/null 2>&1
sudo rm -rf "/Applications/Adobe After Effects CC 2018/Plug-Ins/Extensions/ExtensisFontManagementAECC2018.plugin" > /dev/null 2>&1

### we may install an inert plugin to CC 2014 as well, remove it.
sudo rm -rf "/Applications/Adobe After Effects CC 2014/Plug-ins/Extensions/ExtensisFontManagementAECC2015.plugin"  > /dev/null 2>&1

### remove QXP7, QXP8, QXP9, QXP10, QXP2015, QXP2016, and QXP2017 plug-ins
sudo rm -rf "/Applications/QuarkXPress 7/XTensions/ExtensisFontManagementQXT7.xnt" > /dev/null 2>&1
sudo rm -rf "/Applications/QuarkXPress 7.31/XTensions/ExtensisFontManagementQXT7.xnt" > /dev/null 2>&1
sudo rm -rf "/Applications/QuarkXPress 7.5/XTensions/ExtensisFontManagementQXT7.xnt" > /dev/null 2>&1
sudo rm -rf "/Applications/QuarkXPress 8/XTensions/ExtensisFontManagementQXT8.xnt" > /dev/null 2>&1
sudo rm -rf "/Applications/QuarkXPress 9/XTensions/ExtensisFontManagementQXT9.xnt" > /dev/null 2>&1
sudo rm -rf "/Applications/QuarkXPress 10/XTensions/ExtensisFontManagementQXT10.xnt" > /dev/null 2>&1
sudo rm -rf "/Applications/QuarkXPress 2015/XTensions/ExtensisFontManagementQXT2015.xnt" > /dev/null 2>&1
sudo rm -rf "/Applications/QuarkXPress 2016/XTensions/ExtensisFontManagementQXT2016.xnt" > /dev/null 2>&1
sudo rm -rf "/Applications/QuarkXPress 2017/XTensions/ExtensisFontManagementQXT2017.xnt" > /dev/null 2>&1

## Universal Type Client 1.x
### remove CS2, CS3, CS4, QXP7, QXP8 plug-ins
sudo rm -rf "/Applications/Adobe Illustrator CS2/Plug-ins.localized/Extensions.localized/UniversalTypeAICS2.aip" > /dev/null 2>&1
sudo rm -rf "/Applications/Adobe InDesign CS2/Plug-Ins/UniversalTypeIDCS2.framework" > /dev/null 2>&1

sudo rm -rf "/Applications/Adobe Illustrator CS3/Plug-ins.localized/Extensions.localized/UniversalTypeAICS3.aip" > /dev/null 2>&1
sudo rm -rf "/Applications/Adobe InDesign CS3/Plug-Ins/UniversalTypeIDCS3.InDesignPlugin" > /dev/null 2>&1

sudo rm -rf "/Applications/Adobe Illustrator CS4/Plug-ins.localized/Extensions.localized/UniversalTypeAICS4.aip" > /dev/null 2>&1
sudo rm -rf "/Applications/Adobe InDesign CS4/Plug-Ins/UniversalTypeIDCS4.InDesignPlugin" > /dev/null 2>&1

sudo rm -rf "/Applications/QuarkXPress 7/XTensions/UniversalTypeQuarkXT7.xnt" > /dev/null 2>&1
sudo rm -rf "/Applications/QuarkXPress 7.31/XTensions/UniversalTypeQuarkXT7.xnt" > /dev/null 2>&1
sudo rm -rf "/Applications/QuarkXPress 7.5/XTensions/UniversalTypeQuarkXT7.xnt" > /dev/null 2>&1
sudo rm -rf "/Applications/QuarkXPress 8/XTensions/UniversalTypeQuarkXT8.xnt" > /dev/null 2>&1
echo "... Done"

# remove the font panels
echo "Removing $APP font panels ..."
# remove the CS5, CS 5.5, CS6, CC and CC 2014 font panels
# for adobe CC 2014:
sudo rm -rf /Library/Application\ Support/Adobe/CEP/extensions/Extensis_* > /dev/null 2>&1
# for adobe CC:
sudo rm -rf /Library/Application\ Support/Adobe/CEPServiceManager4/extensions/Extensis_* > /dev/null 2>&1
# for CS6:
sudo rm -rf /Library/Application\ Support/Adobe/CS6ServiceManager/extensions/Extensis_* > /dev/null 2>&1
# for CS5:
sudo rm -rf /Library/Application\ Support/Adobe/CS5ServiceManager/extensions/Extensis_* > /dev/null 2>&1
echo "... Done"

# remove receipts for osx 10.6 thru 10.10
echo "Removing $APP receipts ..."
### Universal Type Client 6x, 5x, 4x, 3x, 2x, 1x
### remove with wildcard
sudo rm -rf /private/var/db/receipts/com.extensis.UniversalTypeClient.* > /dev/null 2>&1

# remove receipts for osx 10.4 and 10.5
## Universal Type Client 3.x
sudo rm -rf "/Library/Receipts/universalTypeClient.pkg" > /dev/null 2>&1
sudo rm -rf "/Library/Receipts/info.pkg" > /dev/null 2>&1

## Universal Type Client 2.x
sudo rm -rf "/Library/Receipts/extensisfontmanagement.pkg" > /dev/null 2>&1
sudo rm -rf "/Library/Receipts/extensisfontmanagementaics2.pkg" > /dev/null 2>&1
sudo rm -rf "/Library/Receipts/extensisfontmanagementaics3.pkg" > /dev/null 2>&1
sudo rm -rf "/Library/Receipts/extensisfontmanagementaics4.pkg" > /dev/null 2>&1
sudo rm -rf "/Library/Receipts/extensisfontmanagementaics5.pkg" > /dev/null 2>&1

sudo rm -rf "/Library/Receipts/extensisfontmanagementidcs2.pkg" > /dev/null 2>&1
sudo rm -rf "/Library/Receipts/extensisfontmanagementidcs3.pkg" > /dev/null 2>&1
sudo rm -rf "/Library/Receipts/extensisfontmanagementidcs4.pkg" > /dev/null 2>&1
sudo rm -rf "/Library/Receipts/extensisfontmanagementidcs5.pkg" > /dev/null 2>&1

sudo rm -rf "/Library/Receipts/extensisfontmanagementqxt7.pkg" > /dev/null 2>&1
sudo rm -rf "/Library/Receipts/extensisfontmanagementqxt8.pkg" > /dev/null 2>&1

sudo rm -rf "/Library/Receipts/extensisplugininterface.pkg" > /dev/null 2>&1
sudo rm -rf "/Library/Receipts/extensisplugins.pkg" > /dev/null 2>&1
sudo rm -rf "/Library/Receipts/pluginfinder.pkg" > /dev/null 2>&1
sudo rm -rf "/Library/Receipts/universalTypeClient.pkg" > /dev/null 2>&1
sudo rm -rf "/Library/Receipts/utcoreprefpane.pkg" > /dev/null 2>&1

## Universal Type Client 1.x
sudo rm -rf "/Library/Receipts/Universal Type Client.pkg" > /dev/null 2>&1
sudo rm -rf "/Library/Receipts/UniversalTypeAICS2.pkg" > /dev/null 2>&1
sudo rm -rf "/Library/Receipts/UniversalTypeAICS3.pkg" > /dev/null 2>&1
sudo rm -rf "/Library/Receipts/UniversalTypeIDCS2.pkg" > /dev/null 2>&1
sudo rm -rf "/Library/Receipts/UniversalTypeIDCS3.pkg" > /dev/null 2>&1
sudo rm -rf "/Library/Receipts/UniversalTypeQuarkXT7.pkg" > /dev/null 2>&1
sudo rm -rf "/Library/Receipts/UTCore-Prefpane.pkg" > /dev/null 2>&1
echo "... Done"

# remove the UTC font cache for all users
echo "Removing $APP cache ..."
sudo rm -rf /Library/Extensis/UTC/* > /dev/null 2>&1
sudo rm -rf "/Library/Extensis/com.extensis.FMCore-LaunchInfo.conf" > /dev/null 2>&1
echo "... Done"
echo ""

}  # end function_remove_UTC


#----------------------------
function_verify_is_mac_admin ()
#----------------------------
{

# goal of function:
# verify user has macintosh administrator credentials to continue
# an admin account must have a valid password for our script to work; an admin account with a blank password is a security risk

ECHO_DEBUG echo "[DEBUG] i am function_verify_is_mac_admin"

echo "Hello, "$USER"."
echo ""
echo "This script must be run under an ADMINISTRATOR account."
echo "Enter your MACINTOSH ADMINISTRATOR password and press [RETURN]."
echo ""
echo "NOTE: The cursor will not move and your password will not be displayed"
echo "as you type. That's OK. Just type carefully and press [RETURN]."
echo ""

# call sudo to get admin/root authentication
sudo whoami > /dev/null 2>&1

# if user has a mac admin password then continue
if [ $? = 0 ]; then
	echo ""
	echo "OK. This is a MACINTOSH ADMINISTRATOR account. Let's proceed."
	echo ""
	MAC_ADMIN_PASSWORD=good
	ECHO_DEBUG echo "[DEBUG] MAC_ADMIN_PASSWORD="$MAC_ADMIN_PASSWORD" "
else
	# else exit with error msg
	echo ""
	echo "Sorry, three strikes and you're out :)"
	echo ""
	echo "Please log into a MACINTOSH ADMINISTRATOR account"
	echo "that has a valid password and run this script again."
	echo "NOTE: Using a blank password for your mac is a security risk."
	echo ""
	MAC_ADMIN_PASSWORD=bad
	ECHO_DEBUG echo "[DEBUG] MAC_ADMIN_PASSWORD="$MAC_ADMIN_PASSWORD" "
	exit 1
fi

}   # end of function_verify_is_mac_admin


#################################################
##             SCRIPT starts here              ##
#################################################


# print a "letterhead" to screen with a function
function_letterhead

# declare our variables
APP="Universal Type Client"

# run function_verify_is_mac_admin
function_verify_is_mac_admin

# write a msg to system.log
logger com.extensis.support.UTC-removal-tool: Removing $APP now ...

# run function_remove_UTC
function_remove_UTC

# write a msg to system.log
logger com.extensis.support.UTC-removal-tool: $APP successfully removed.



# print results to screen
echo "--------------------------------------------------------------"
echo "*** RESULT ***"
echo "--------------------------------------------------------------"
echo ""
echo "$APP has been successfully removed."
echo "--------------------------------------------------------------"

# say goodbye
echo ""
echo "You can quit Terminal now."
echo ""
echo "Best Regards, Extensis."
echo ""                         # end with a new line for visibility

exit


#################################################
##                   TO DO                     ##
#################################################

: <<COMMENTBLOCK

[ ] 2017-0:613 enclose me; love me. i am a block of comments


COMMENTBLOCK
