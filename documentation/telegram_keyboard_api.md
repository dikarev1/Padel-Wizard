# Официальный док “Keyboard API”

### **ReplyKeyboardMarkup**

This object represents a [custom keyboard](https://core.telegram.org/bots/features#keyboards) with reply options (see [Introduction to bots](https://core.telegram.org/bots/features#keyboards) for details and examples). Not supported in channels and for messages sent on behalf of a Telegram Business account.

| Field | Type | Description |
| --- | --- | --- |
| keyboard | Array of Array of [KeyboardButton](https://core.telegram.org/bots/api#keyboardbutton) | Array of button rows, each represented by an Array of [KeyboardButton](https://core.telegram.org/bots/api#keyboardbutton) objects |
| is_persistent | Boolean | *Optional*. Requests clients to always show the keyboard when the regular keyboard is hidden. Defaults to *false*, in which case the custom keyboard can be hidden and opened with a keyboard icon. |
| resize_keyboard | Boolean | *Optional*. Requests clients to resize the keyboard vertically for optimal fit (e.g., make the keyboard smaller if there are just two rows of buttons). Defaults to *false*, in which case the custom keyboard is always of the same height as the app's standard keyboard. |
| one_time_keyboard | Boolean | *Optional*. Requests clients to hide the keyboard as soon as it's been used. The keyboard will still be available, but clients will automatically display the usual letter-keyboard in the chat - the user can press a special button in the input field to see the custom keyboard again. Defaults to *false*. |
| input_field_placeholder | String | *Optional*. The placeholder to be shown in the input field when the keyboard is active; 1-64 characters |
| selective | Boolean | *Optional*. Use this parameter if you want to show the keyboard to specific users only. Targets: 1) users that are @mentioned in the *text* of the [Message](https://core.telegram.org/bots/api#message) object; 2) if the bot's message is a reply to a message in the same chat and forum topic, sender of the original message.*Example:* A user requests to change the bot's language, bot replies to the request with a keyboard to select the new language. Other users in the group don't see the keyboard. |

### **KeyboardButton**

This object represents one button of the reply keyboard. At most one of the optional fields must be used to specify type of the button. For simple text buttons, *String* can be used instead of this object to specify the button text.

| Field | Type | Description |
| --- | --- | --- |
| text | String | Text of the button. If none of the optional fields are used, it will be sent as a message when the button is pressed |
| request_users | [KeyboardButtonRequestUsers](https://core.telegram.org/bots/api#keyboardbuttonrequestusers) | *Optional*. If specified, pressing the button will open a list of suitable users. Identifiers of selected users will be sent to the bot in a “users_shared” service message. Available in private chats only. |
| request_chat | [KeyboardButtonRequestChat](https://core.telegram.org/bots/api#keyboardbuttonrequestchat) | *Optional*. If specified, pressing the button will open a list of suitable chats. Tapping on a chat will send its identifier to the bot in a “chat_shared” service message. Available in private chats only. |
| request_contact | Boolean | *Optional*. If *True*, the user's phone number will be sent as a contact when the button is pressed. Available in private chats only. |
| request_location | Boolean | *Optional*. If *True*, the user's current location will be sent when the button is pressed. Available in private chats only. |
| request_poll | [KeyboardButtonPollType](https://core.telegram.org/bots/api#keyboardbuttonpolltype) | *Optional*. If specified, the user will be asked to create a poll and send it to the bot when the button is pressed. Available in private chats only. |
| web_app | [WebAppInfo](https://core.telegram.org/bots/api#webappinfo) | *Optional*. If specified, the described [Web App](https://core.telegram.org/bots/webapps) will be launched when the button is pressed. The Web App will be able to send a “web_app_data” service message. Available in private chats only. |

**Note:** *request_users* and *request_chat* options will only work in Telegram versions released after 3 February, 2023. Older clients will display *unsupported message*.

### **KeyboardButtonRequestUsers**

This object defines the criteria used to request suitable users. Information about the selected users will be shared with the bot when the corresponding button is pressed. [More about requesting users »](https://core.telegram.org/bots/features#chat-and-user-selection)

| Field | Type | Description |
| --- | --- | --- |
| request_id | Integer | Signed 32-bit identifier of the request that will be received back in the [UsersShared](https://core.telegram.org/bots/api#usersshared) object. Must be unique within the message |
| user_is_bot | Boolean | *Optional*. Pass *True* to request bots, pass *False* to request regular users. If not specified, no additional restrictions are applied. |
| user_is_premium | Boolean | *Optional*. Pass *True* to request premium users, pass *False* to request non-premium users. If not specified, no additional restrictions are applied. |
| max_quantity | Integer | *Optional*. The maximum number of users to be selected; 1-10. Defaults to 1. |
| request_name | Boolean | *Optional*. Pass *True* to request the users' first and last names |
| request_username | Boolean | *Optional*. Pass *True* to request the users' usernames |
| request_photo | Boolean | *Optional*. Pass *True* to request the users' photos |

### **KeyboardButtonRequestChat**

This object defines the criteria used to request a suitable chat. Information about the selected chat will be shared with the bot when the corresponding button is pressed. The bot will be granted requested rights in the chat if appropriate. [More about requesting chats »](https://core.telegram.org/bots/features#chat-and-user-selection).

| Field | Type | Description |
| --- | --- | --- |
| request_id | Integer | Signed 32-bit identifier of the request, which will be received back in the [ChatShared](https://core.telegram.org/bots/api#chatshared) object. Must be unique within the message |
| chat_is_channel | Boolean | Pass *True* to request a channel chat, pass *False* to request a group or a supergroup chat. |
| chat_is_forum | Boolean | *Optional*. Pass *True* to request a forum supergroup, pass *False* to request a non-forum chat. If not specified, no additional restrictions are applied. |
| chat_has_username | Boolean | *Optional*. Pass *True* to request a supergroup or a channel with a username, pass *False* to request a chat without a username. If not specified, no additional restrictions are applied. |
| chat_is_created | Boolean | *Optional*. Pass *True* to request a chat owned by the user. Otherwise, no additional restrictions are applied. |
| user_administrator_rights | [ChatAdministratorRights](https://core.telegram.org/bots/api#chatadministratorrights) | *Optional*. A JSON-serialized object listing the required administrator rights of the user in the chat. The rights must be a superset of *bot_administrator_rights*. If not specified, no additional restrictions are applied. |
| bot_administrator_rights | [ChatAdministratorRights](https://core.telegram.org/bots/api#chatadministratorrights) | *Optional*. A JSON-serialized object listing the required administrator rights of the bot in the chat. The rights must be a subset of *user_administrator_rights*. If not specified, no additional restrictions are applied. |
| bot_is_member | Boolean | *Optional*. Pass *True* to request a chat with the bot as a member. Otherwise, no additional restrictions are applied. |
| request_title | Boolean | *Optional*. Pass *True* to request the chat's title |
| request_username | Boolean | *Optional*. Pass *True* to request the chat's username |
| request_photo | Boolean | *Optional*. Pass *True* to request the chat's photo |

### **KeyboardButtonPollType**

This object represents type of a poll, which is allowed to be created and sent when the corresponding button is pressed.

| Field | Type | Description |
| --- | --- | --- |
| type | String | *Optional*. If *quiz* is passed, the user will be allowed to create only polls in the quiz mode. If *regular* is passed, only regular polls will be allowed. Otherwise, the user will be allowed to create a poll of any type. |

### **ReplyKeyboardRemove**

Upon receiving a message with this object, Telegram clients will remove the current custom keyboard and display the default letter-keyboard. By default, custom keyboards are displayed until a new keyboard is sent by a bot. An exception is made for one-time keyboards that are hidden immediately after the user presses a button (see [ReplyKeyboardMarkup](https://core.telegram.org/bots/api#replykeyboardmarkup)). Not supported in channels and for messages sent on behalf of a Telegram Business account.

| Field | Type | Description |
| --- | --- | --- |
| remove_keyboard | True | Requests clients to remove the custom keyboard (user will not be able to summon this keyboard; if you want to hide the keyboard from sight but keep it accessible, use *one_time_keyboard* in [ReplyKeyboardMarkup](https://core.telegram.org/bots/api#replykeyboardmarkup)) |
| selective | Boolean | *Optional*. Use this parameter if you want to remove the keyboard for specific users only. Targets: 1) users that are @mentioned in the *text* of the [Message](https://core.telegram.org/bots/api#message) object; 2) if the bot's message is a reply to a message in the same chat and forum topic, sender of the original message.*Example:* A user votes in a poll, bot returns confirmation message in reply to the vote and removes the keyboard for that user, while still showing the keyboard with poll options to users who haven't voted yet. |

### **InlineKeyboardMarkup**

This object represents an [inline keyboard](https://core.telegram.org/bots/features#inline-keyboards) that appears right next to the message it belongs to.

| Field | Type | Description |
| --- | --- | --- |
| inline_keyboard | Array of Array of [InlineKeyboardButton](https://core.telegram.org/bots/api#inlinekeyboardbutton) | Array of button rows, each represented by an Array of [InlineKeyboardButton](https://core.telegram.org/bots/api#inlinekeyboardbutton) objects |

### **InlineKeyboardButton**

This object represents one button of an inline keyboard. Exactly one of the optional fields must be used to specify type of the button.

[Untitled](%D0%9E%D1%84%D0%B8%D1%86%D0%B8%D0%B0%D0%BB%D1%8C%D0%BD%D1%8B%D0%B9%20%D0%B4%D0%BE%D0%BA%20%E2%80%9CKeyboard%20API%E2%80%9D/Untitled%202adeedc471698047a9fcf57b4707d119.csv)