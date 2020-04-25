# KGB_EDITS

**K**ieran **G** **B**icheno's **E**mergency **D**ispatcher **I**n **T**raumatic **S**ituations

A backup bot designed to dispatch emergency services alerts in cases where human agents are no longer able to do so but internet connectivity has not yet been destroyed.

This file also serves as a roadmap for improvements as obvious shortcomings in each command become apparent in the documentation.

## Commands

Brook's commands are invoked with the '$' prefix. At this point there is no way to change this character, though it is on the to-do list.

### %Commands

Shows a list of Brook's commands and their parameters with a short description.

### %News

Parameters:

- *number of articles* [int]

- *as_message* [-m flag]

Shows a list of articles from the main RSS list, defaulting to five if the number of articles parameter is not set, and displayed in the channel if the -m flag is not set.

### $Advice

Parameters:

- *disaster type* [str]

Takes one of three parameters: flood, fire, or all. Flood shows all current warnings from the Bureau of Meteorology. Fire shows all current QFES alerts. All shows warnings from both lists.

### $AddFeed

Parameters:

- *name* [str]

- *new_url* [url]

- *topic* [str]

This command allows users to add new RSS feeds to a moderation queue for inclusion in the main news feed. The name parameter must be either a single-word string or multiple words wrapped in double-quotes. The URL must be properly formed (manually checked during moderation) and the topic must be informative and human-parsable for clarity and appropriateness.

### $AddFeed_Help

This command takes no parameters and sends a Direct Message to the user with a verbose explanation on the best way to use the $AddFeed command.

### $YourShiftIsOver

This command can only be invoked by the bot's owner. The bot sends a confirmation DM to the owner and then logs off using the logout() method.

### $Poetry

This is a placeholder command that currently pays homage to Rae Elliot White, the award-winning and much-respected non-binary poet who spends much of their time as a moderator in the original channel in which Brook was developed.

Eventually this command will be used to reflect a user who made most use of Brook's commands (and will mention Rae as an Easter egg).

### $clear

Parameters:

- *messages* [int]

Clears the channel of a number of messages equal to that passed in as the messages parameter. The maximum number of messages that can be deleted at once is 100. Brook will flag an error to the user if fewer than 1 or more than 100 are passed in through the parameter.

### $Users

Parameters:

- *verbosity* [-v flag]

Sends a Direct Message to the bot owner with details of all members of the guild Brook is currently in. If the -v flag is not set, this information only includes the ID of each user. if the -v flag is set, it also includes their name, display_name, top role, activity, avatar url, and whether or not they are a bot.

### $Economy

Parameters:

- *verbosity* [-v flag]

- *destination* [-m|-c flag]

Sends the user a list of economic reading resources designed to help them stay current with Australian and World economic affairs. If the -v flag is not set, 1 link will be sent: the St George morning report. If the -v flag is set, links to the following publications will also be sent:

- Morning reports
- 2019 Key Indicator Snapshots
- Interest Rate Outlook
- Australian Dollar Outlook
- Quarterly Economic Outlook
- State Economic Reports
- Economic Calendar
- Budget Snapshot
- Weekly Economic Outlook
- Speeches by the RBA
- SportsBet Politics section
- SportsBet Futures section
- Bet365 Australian Politics section

### $Fires

A stand-alone command for adding QFES alerts to the feed for the $News command.

### $BOM

A stand-alone command for adding BOM warnings to the feed for the $News command.

### $playlist_me

A knee-jerk command for when inspiration for a song to play through the Rhythm bot is required. Brook will DM the invoker the entire Triple J Hottest 100 as a series of Rhythm bot commands. More nuance is planned for the command as soon as possible.

### $valid_groups

This command takes no parameters but displays a list of the property groups from the game Monopoly.

### $groups_verbose

This command takes no parameters but displays a list of the property groups from the game Monopoly and the properties within each group.

### $roll

Parameters:

- *both* [bool]

When invoked, the $roll command takes a true or false parameter to see if the user is going to roll one or both six-sided dice as if in the game Monopoly. It will then display the results of such a roll accordingly using Python's random.randrange() function.

### $r

Parameters:

- *diceroll* [str]

An advanced dice roller function capable of taking multiple configurations of polyhedral dice rolls, bonuses and debuffs as the terms of its single parameter.

The default configuration of the $r command's dice roll can be expressed as such:

```css
 [number of dice] [d] [sides per dice] [+|-] [modifier]
```

```diff
+|  3d6+2
+|  d20+5
+|  d20-2
```

At its leanest, the $r command will still return a d20 if provided with nothing but 'd' as a parameter.

It is possible to string together default roll structures to make more complex rolls.

```css
[number of dice] [d] [sides per dice] [+|-] [number of dice] [d] [sides per dice] [+|-] [modifier][+|-] [modifier] [+|-] [number of dice] [d] [sides per dice]
```

```diff
+|  3d6+2d4+6-1d6
+|  8d6-2d4+8-2+4-4d6+9d8+4d9+3+3
+|  d-d6
```

## Future Plans

Brook's feature set is currently based around the most sailent emergency scenario - isolation caused by the COVID-19 pandemic. All of Brook's feature development is currently geared toward feature requests made by channel members who are feeling most impacted by the movement restrictions.
