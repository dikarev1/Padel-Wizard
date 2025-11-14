# Официальный док “Telegram bot Features”

# **Telegram Bot Features**

This page describes individual **bot elements** and **features** in detail. See also:

- [A General Bot Platform Overview](https://core.telegram.org/bots)
- [Full API Reference for Developers](https://core.telegram.org/bots/api)

### **What features do bots have?**

- [**Inputs**](https://core.telegram.org/bots/features#inputs)
    - [Text](https://core.telegram.org/bots/features#inputs)
    - [Commands](https://core.telegram.org/bots/features#commands)
    - [Buttons](https://core.telegram.org/bots/features#keyboards)
    - [Chat and User Selection](https://core.telegram.org/bots/features#chat-and-user-selection)
- [**Interactions**](https://core.telegram.org/bots/features#interactions)
    - [Inline](https://core.telegram.org/bots/features#inline-requests)
    - [Deep Linking](https://core.telegram.org/bots/features#deep-linking)
    - [Attachment Menu](https://core.telegram.org/bots/features#attachment-menu)
- [**Integration**](https://core.telegram.org/bots/features#integration)
    - [Mini Apps](https://core.telegram.org/bots/features#mini-apps)
    - [Bots for Business](https://core.telegram.org/bots/features#bots-for-business)
    - [Payments](https://core.telegram.org/bots/features#payments)
    - [Web Login](https://core.telegram.org/bots/features#web-login)
    - [HTML5 Games](https://core.telegram.org/bots/features#html5-games)
    - [Stickers](https://core.telegram.org/bots/features#stickers-and-custom-emoji)
- [**Monetization**](https://core.telegram.org/bots/features#monetization)
- [**Language Support**](https://core.telegram.org/bots/features#language-support)
- [**Bot Management**](https://core.telegram.org/bots/features#bot-management)
    - [Privacy Mode](https://core.telegram.org/bots/features#privacy-mode)
    - [Testing Your Bot](https://core.telegram.org/bots/features#testing-your-bot)
    - [Status Alerts](https://core.telegram.org/bots/features#status-alerts)
    - [Local API](https://core.telegram.org/bots/features#local-bot-api)
- [**BotFather, creating and managing bots**](https://core.telegram.org/bots/features#botfather)

---

### **Inputs**

Users can send **messages of all types** to bots, including text, files, locations, stickers, voice messages and even [dice](https://core.telegram.org/bots/api#dice) if they're feeling lucky. However, Telegram bots offer many other tools for building flexible interfaces tailored to your specific needs:

- [Commands](https://core.telegram.org/bots/features#commands) that are highlighted in messages and can be selected from a list after typing /.
- [Keyboards](https://core.telegram.org/bots/features#keyboards) that replace the user's keyboard with predefined answer options.
- [Buttons](https://core.telegram.org/bots/features#inline-keyboards) that are shown next to messages from the bot.

For even more flexibility, [Web Apps](https://core.telegram.org/bots/features#web-apps) support 100% custom interfaces with JavaScript.

**Note:** Telegram bots can support [multiple languages](https://core.telegram.org/bots/features#language-support) that adapt to the users' language settings in the app.

### **Commands**

A command is a simple /keyword that tells the bot what to do. Telegram apps will:

- **Highlight** commands in messages. When the user taps a highlighted command, that command is immediately sent again.
- Suggest a **list of supported commands** with descriptions when the user enters a / (for this to work, you need to have provided a list of commands to [@BotFather](https://t.me/botfather) or via the [appropriate API method](https://core.telegram.org/bots/api#setmycommands)). Selecting a command from the list immediately sends it.
- Show a [menu button](https://core.telegram.org/bots/features#menu-button) containing all or some of a bot’s commands (which you set via [@BotFather](https://t.me/botfather)).

Commands must always start with the / symbol and contain **up to 32 characters**. They can use **Latin letters**, **numbers** and **underscores**, though simple lowercase text is recommended for a cleaner look.

Here are a few examples:

- /next
- /cancel
- /newlocation
- /newrule

Commands should be **as specific as possible** – for example /newlocation or /newrule **is better** than a /new command that then requires an additional parameter from the user like "*location*“ or ”*rule*".

We require **all developers** to support several [Global Commands](https://core.telegram.org/bots/features#global-commands) to make sure Telegram bots offer a consistent and user-friendly experience.

### **Command Scopes**

Your bot is able to **show different commands** to different users and groups – you can control this using [scopes](https://core.telegram.org/bots/api#botcommandscope). For example, your bot could show additional commands to group admins or translate the list based on the user’s [language_code](https://core.telegram.org/bots/api#user).

Keep in mind that Bot API [updates](https://core.telegram.org/bots/api#update) **will not contain any information** about the scope of a command sent by the user – in fact, they may contain commands that don’t exist at all in your bot. Your backend should **always** verify that received commands are valid and that the user was authorized to use them regardless of scope.

Bots with privacy mode enabled will only receive commands in groups under special conditions, [see here](https://core.telegram.org/bots/features#privacy-mode).

### **Keyboards**

Bots are able to interpret free text input from users, but offering **specific suggestions** is often more intuitive – this is where **custom keyboards** can be extremely useful.

Whenever your bot sends a message, it can **display a special keyboard** with predefined reply options (see [ReplyKeyboardMarkup](https://core.telegram.org/bots/api#replykeyboardmarkup)). Telegram apps that receive the message will display your keyboard to the user. Using any of the buttons will immediately send the respective text. This way you can drastically **simplify** and **streamline** user interaction with your bot.

Check out the [one_time_keyboard](https://core.telegram.org/bots/api#replykeyboardmarkup) parameter to automatically hide your bot's keyboard as soon as it's been used.

You can also **customize the text placeholder** in the input field by setting the input_field_placeholder parameter.

### **Inline Keyboards**

There are times when you'd prefer to do things **without sending any messages** to the chat – like when a user is changing settings, toggling options or navigating search results. In such cases, you can use [Inline Keyboards](https://core.telegram.org/bots/api#inlinekeyboardmarkup) that are shown directly below their relevant messages.

Unlike with custom reply keyboards, pressing buttons on inline keyboards **doesn't send messages to the chat**. Instead, inline keyboards support buttons that can work behind the scenes or open different interfaces: [callback buttons](https://core.telegram.org/bots/api#inlinekeyboardbutton), [URL buttons](https://core.telegram.org/bots/api#inlinekeyboardbutton), [switch-to-inline buttons](https://core.telegram.org/bots/api#inlinekeyboardbutton), [game buttons](https://core.telegram.org/bots/api#inlinekeyboardbutton) and [payment buttons](https://core.telegram.org/bots/api#inlinekeyboardbutton).

To provide a **better user experience**, consider [editing your keyboard](https://core.telegram.org/bots/api#editmessagereplymarkup) when the user toggles a setting button or navigates to a new page – this is both **faster** and **smoother** than sending a whole new message and deleting the previous one.

### **Menu Button**

In all bot chats, a menu button appears near the message field. By default, tapping this button **opens a menu** that can hold some or all of a bot's commands, including a short description for each. Users can then **select a command from the menu** without needing to type it out.

You can set different texts of the menu button and its command descriptions for various **individual users** or **groups of users** – for example, showing translated text based on the user’s language, as explained [here](https://core.telegram.org/bots/features#commands).

The **menu button** can alternatively be used to launch a [Web App](https://core.telegram.org/bots/features#web-apps).

### **Global Commands**

To make basic interactions more uniform, we ask all developers to support a few **basic commands**. Telegram apps will have interface shortcuts for these commands.

- /start - begins the interaction with the user, like sending an introductory message. This command can also be used to pass additional parameters to the bot (see [Deep Linking](https://core.telegram.org/bots/features#deep-linking)).
- /help - returns a help message, like a short text about what your bot can do and a list of commands.
- /settings - (if applicable) shows the bot's settings for this user and suggests commands to edit them.

Users will see a **Start** button the first time they open a chat with your bot. **Help** and **Settings** links will be available in the menu on the bot's profile page if you add them in [@BotFather](https://t.me/botfather).

### **Chat and User Selection**

Bots can present the user with a **friendly** and **intuitive** interface that lists any number of groups, channels or other users according to a custom set of **criteria**. Tapping on a chat will send its identifier to the bot in a service message and seamlessly close the interface.

A group management bot is the **perfect example**: an admin could select a chat the bot should manage, and then select a user it should promote – this would happen without ever typing any text.

Here is a **quick start guide** to use this feature:

- Pick a set of criteria and store them in a [KeyboardButtonRequestChat](https://core.telegram.org/bots/api#keyboardbuttonrequestchat) object (or [KeyboardButtonRequestUser](https://core.telegram.org/bots/api#keyboardbuttonrequestuser) for users).
- Create a [KeyboardButton](https://core.telegram.org/bots/api#keyboardbutton) and store the criteria under request_chat or request_user respectively.
- Send a [ReplyKeyboardMarkup](https://core.telegram.org/bots/api#replykeyboardmarkup) that contains the button you just created.
- When the user selects a chat, you'll receive its identifier in a chat_shared or user_shared service message.

Keep in mind that the bot may not be able to use the identifier it receives if the corresponding chat or user is not already known or accessible by some other means.

---

### **Interactions**

In addition to sending commands and messages to the chat with the bot, there are several ways of interacting with them without opening any specific chat or group.

- [**Inline mode**](https://core.telegram.org/bots/features#inline-requests) allows sending requests to bots right from the input field – from any chat on Telegram.
- [**Deep linking**](https://core.telegram.org/bots/features#deep-linking) allows special links that send certain parameters to the bot when opened.
- [**Attachment menu**](https://core.telegram.org/bots/features#attachment-menu) integration makes it possible to use bots from the attachment menu in chats.

### **Inline Requests**

Users can interact with your bot via **inline queries** straight from the message field **in any chat**. All they need to do is start a message with your bot's *@username* and enter a keyword.

Having received the query, your bot can return some results. As soon as the user selects one, it is sent to the **relevant chat**. This way, people can request and send content from your bot in any of their chats, groups or channels.

Remember that inline functionality has to be enabled via [@BotFather](https://t.me/botfather), or your bot will not receive inline [Updates](https://core.telegram.org/bots/api#update).

Examples of inline bots include [@gif](https://gif.t.me/), [@bing](https://bing.t.me/) and [@wiki](https://wiki.t.me/). [Web App](https://core.telegram.org/bots/features#web-apps) bots can also be used inline – try typing [@durgerkingbot](https://durgerkingbot.t.me/) in any chat.

### **Deep Linking**

Telegram bots have a deep linking mechanism that allows **additional parameters** to be passed to the bot on startup. It could be a command that launches the bot – or an authentication token to connect the user's Telegram account to their account on another platform.

Each bot has a link that **opens a conversation** with it in Telegram – https://t.me/<bot_username>. Parameters can be added directly to this link to let your bot work with additional information on the fly, without any user input.

A-Z, a-z, 0-9, _ and - are allowed. We recommend using base64url to encode parameters with binary and other types of content. The parameter can be up to 64 characters long.

**Private Chats**

In private chats, you can use the start parameter to automatically pass any value to your bot whenever a user presses the link. For example, you could use:

https://t.me/your_bot?start=airplane

When someone opens a chat with your bot via this link, you will receive:

/start airplane

**Groups**

In groups, you can add the parameter startgroup to this link. For example:

https://t.me/your_bot?startgroup=spaceship

Following a link with this parameter prompts the user to select a group to add the bot to – the resulting update will contain text in the form:

/start@your_bot spaceship

[Web Apps](https://core.telegram.org/bots/features#web-apps) also support deep linking, for more information check out our [dedicated guide](https://core.telegram.org/bots/webapps#adding-bots-to-the-attachment-menu).

### **Attachment Menu**

Certain bots can be added directly to a user’s **attachment menu** – giving them easy access to the bot in any chat. Currently, this option is restricted to certain [approved bots](https://core.telegram.org/bots/webapps#launching-web-apps-from-the-attachment-menu), but may be expanded later.

Try adding [@DurgerKingBot](https://t.me/durgerkingbot?startattach) to your attachment menu.

---

### **Integration**

There are various ways of further integrating bots with Telegram and other services.

- Use [Web Apps](https://core.telegram.org/bots/features#web-apps) to replace any website.
- Build tools and integrate [business services](https://core.telegram.org/bots/features#bots-for-business).
- Accept [Payments](https://core.telegram.org/bots/features#payments) via third-party payment providers that support integration with Bots and Mini Apps.
- Connect to Telegram using the [Web Login](https://core.telegram.org/bots/features#web-login) functionality.
- Create gaming bots by integrating [HTML5 Games](https://core.telegram.org/bots/features#html5-games).
- Help users create and manage [Telegram Stickers](https://core.telegram.org/bots/features#stickers-and-custom-emoji).

### **Monetization**

Telegram offers a **robust ecosystem** of monetization features, allowing any bot to support its development with **multiple revenue streams**.

### **Telegram Stars**

Telegram Stars power all digital transactions between bots and users. Users can acquire Stars through in-app purchases via Apple and Google or via [@PremiumBot](https://t.me/premiumbot).

Bots can use the Stars they receive to [increase message limits](https://telegram.org/blog/dynamic-video-quality-and-more#increased-message-limits-for-bots), [send gifts](https://core.telegram.org/bots/api#sendgift) to users or [accept rewards](https://telegram.org/blog/monetization-for-channels) in Toncoin.

### **Digital Products**

Services can use their bot to sell **digital goods** and **services** – like online courses, commissioned artwork and **items in games**.

### **Paid Media**

Bots can post **paid photos** and **videos** – and users are only allowed to view the media after paying to unlock it. This functionality is available to **all bots** – including **bot admins** in channels and bots managing [Telegram Business](https://core.telegram.org/bots/features#bots-for-business) accounts.

### **Subscription Plans**

Developers are able to **offer paid subscriptions** to their bot – adding **multiple tiers** of content and features tailored to their audience.

### **Revenue Sharing from Telegram Ads**

Developers can participate in [revenue sharing](https://telegram.org/blog/monetization-for-channels) from [Telegram Ads](https://telegram.org/blog/monetization-for-channels#ton-based-ads) – receiving **50%** of the revenue from ads that appear in the chat with their bot.

### **Mini Apps**

[Mini Apps](https://core.telegram.org/bots/webapps) allow developers to create infinitely flexible interfaces that can be launched right inside Telegram – integrating seamlessly with the app and replacing **any website**.

If your bot is a mini app, you can add a prominent **Launch app** button as well as demo videos and screenshots to the bot’s profile. To do this, go to [@BotFather](https://t.me/botfather) and set up your bot's [Main Mini App](https://core.telegram.org/bots/webapps#launching-the-main-mini-app).

Mini apps are covered in detail in our [dedicated guide](https://core.telegram.org/bots/webapps) – you should read it carefully to learn the wide variety of features they can offer.

If you develop a **mini app**, be sure to follow our [design guidelines](https://core.telegram.org/bots/webapps#design-guidelines) – you'll want your custom interface to **seamlessly integrate** into the app to provide users the best possible experience.

### **Seamless Integration With Telegram**

Mini apps integrate **seamlessly** with Telegram – from receiving detailed [theme settings](https://core.telegram.org/bots/webapps#themeparams) to using native dialogs for reading [QR codes](https://core.telegram.org/bots/webapps#initializing-mini-apps), controlling [biometrics](https://core.telegram.org/bots/webapps#biometricmanager), sharing media [directly to stories](https://core.telegram.org/bots/webapps#initializing-mini-apps) and more.

When opened from a [direct link](https://core.telegram.org/bots/webapps#direct-link-mini-apps) in a group, mini apps can also use the chat_instance parameter to track of the current context, supporting **shared usage** by multiple chat members – to create live whiteboards, group orders, multiplayer games and much more.

### **Mini App Previews**

Developers can **upload screenshots** and **video demos** of their mini app right from the bot's **profile page** – giving users an overview of the app's features and functionality. These media previews will be shown to any user who **views your app** – like in the [Mini App Store](https://core.telegram.org/bots/features#mini-app-store) or via Search.

Previews support **multiple languages** – so you can upload **translated versions** of your previews that will be shown to users based on their **app language**.

### **Mini App Store**

More than **500 million** out of Telegram's [950](https://t.me/durov/337) million users interact with mini apps every month. Successful mini apps have the chance to be **highlighted** in the Telegram Mini App Store – appearing for all users in the *'Apps'* tab of Search.

Featured mini apps are chosen based on how they **enrich the Telegram ecosystem**. To increase the chances of being featured, you must **enable** the [Main Mini App](https://core.telegram.org/bots/webapps#launching-the-main-mini-app) in [@BotFather](https://t.me/botfather), **upload** high-quality media demos showcasing your app to your bot's profile and **accept payments** in [Telegram Stars](https://telegram.org/blog/telegram-stars).

Check out our documentation to learn more about [enabling Main Mini Apps](https://core.telegram.org/bots/webapps#launching-the-main-mini-app) and [accepting payments](https://core.telegram.org/bots/payments-stars) in Stars.

### **Home Screen Shortcuts**

Users can place **direct shortcuts** to specific mini apps on the **home screen** of their devices – accessing their favorite games and services in **one tap**.

### **Customizable Loading Screens**

The loading screen of mini apps can be **customized** in [@Botfather](https://t.me/botfather) – where developers can add **their own icon** and set **specific colors** for both light and dark themes.

To customize your loading screen, go to [@Botfather](https://t.me/botfather) > /mybots > Select bot > *Bot Settings* > *Configure Mini App* > *Configure Splash Screen*. You can tap on *Open Splash Screen Preview* to see the final result.

### **Full-Screen Mode**

Mini apps are able to use the **entire screen** in portrait or **landscape orientation** – allowing for **immersive games** and media with **expanded gestures** and interfaces.

### **Setting Emoji Status**

Users can **set an emoji status** inside mini apps or give an app permission to **update it automatically**.

Developers can also integrate APIs from

**other services**

or request

[geolocation access](https://core.telegram.org/bots/features#geolocation-access)

– instantly changing a user's status when they start a game

[🎮](data:image/png;base64,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)

or leave the office

[💼](data:image/png;base64,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)

.

### **Sharing Media**

Media generated in mini apps can be shared in **any chat** – letting users effortlessly send **referral codes** and **custom images** to contacts, groups and channels. Alternatively, users can [download it](https://core.telegram.org/bots/webapps#downloadfileparams) with a native popup.

### **Sharing from Mini Apps to Stories**

Any media created by the mini app, like whiteboard snapshots, leaderboards and AI-generated videos can be opened with the native story editor via the [shareToStory](https://core.telegram.org/bots/webapps#initializing-mini-apps) method – for users to share as a [Telegram Story](https://telegram.org/tour/stories) right from the mini app.

Mini apps also receive a number of **events**, allowing them to **instantly react** to actions by the user. You can learn more about which events are available [here](https://core.telegram.org/bots/webapps#events-available-for-mini-apps).

### **Geolocation Access**

Mini apps are able to receive **location permissions** from users – giving developers the ability to make **location-based games** and **interactive maps** for events.

### **Device Motion Tracking**

Mini Apps can request [acceleration](https://core.telegram.org/bots/webapps#accelerometer), [orientation](https://core.telegram.org/bots/webapps#deviceorientation) and [rotation](https://core.telegram.org/bots/webapps#gyroscope) data from devices in real time – unlocking support for **motion controls** and **VR experiences**.

### **Device Hardware Info**

A user's device can send [basic hardware info](https://core.telegram.org/bots/webapps#additional-data-in-user-agent) to mini apps, such as its processing power and memory capacity. Mini apps can then use this to **optimize graphics** and automatically **adjust settings** for the smoothest experience.

### **Bots for Business**

Bots can enable **Business Mode**, allowing [Telegram Business](https://telegram.org/blog/telegram-business) subscribers to connect them to their account – streamlining and automating private chat management and interactions with their clients.

The **account owner** can specify which chats your bot can access – within those chats, the bot will receive all updates normally supported by the [Bot API](https://core.telegram.org/bots/api), except messages sent by itself and other bots. Depending on the business connection settings, your bot may also be able to **send messages** and do other actions on behalf of the account owner in chats that were active in the last 24h.

Here is a quick start guide to integrate your bot with Telegram Business:

- Enable **Business Mode** for your bot in [@BotFather](https://t.me/botfather).
- Handle incoming [BusinessConnection](https://core.telegram.org/bots/api#businessconnection) updates, signaling that a user has *established*, *edited* or *ended* a Business Connection with your bot.
- Process business messages by handling business_message, edited_business_message and deleted_business_messages updates.
- Check your bot’s write permissions via can_reply in the latest [BusinessConnection](https://core.telegram.org/bots#businessconnection) update.
- If allowed to, use the business_connection_id field in [sendMessage](https://core.telegram.org/bots/api#sendmessage), [sendChatAction](https://core.telegram.org/bots/api#sendchataction) and other send methods to communicate on behalf of the Business user.

Users who **connect your bot** to their account will see a **quick action bar** at the top of each managed chat – tapping on “Manage Bot” will redirect them to your bot, which will receive a deep link message in the format /start bizChat<user_chat_id>.

Please keep in mind that operating bots on Telegram is subject to the [Telegram Bot Developer Terms of Service](https://telegram.org/tos/bot-developers). Specifically, for Telegram Business, make sure you have read and understood [Section 5.4](https://telegram.org/tos/bot-developers#5-4-telegram-business).

### **Payments**

If your bot or mini app sells **digital goods and services**, be sure to carry out the payment in [Telegram Stars](https://telegram.org/blog/telegram-stars) by specifying XTR as currency. In compliance with third-party store policies, Telegram does not support the sale of digital goods and services using other currencies.

Telegram bots can accept payments with a sleek, streamlined interface that collects all necessary data from the user. Telegram **doesn't collect** any payment data – like the user's credit card information – and sends it directly to one of the supported third-party [payment providers](https://core.telegram.org/bots/payments).

Here is a **quick start guide** to implement payments:

- Pick a [provider](https://core.telegram.org/bots/payments) and obtain the [proper token](https://core.telegram.org/bots/payments#getting-a-token) as well as a **test token** from the "**Stripe TEST MODE**" provider.
- Implement payments via the [appropriate API methods](https://core.telegram.org/bots/api#payments).
- Test your implementation by using your **test token** along with a [test credit card](https://stripe.com/docs/testing#cards).

Then, to issue an **invoice** and process the order flow:

- [Send an invoice](https://core.telegram.org/bots/api#sendinvoice) to the user for the goods or services you are offering.
- Validate the order and accept the checkout via [answerPreCheckoutQuery](https://core.telegram.org/bots/api#answerprecheckoutquery).
- Confirm the payment by checking for a [successful payment service message](https://core.telegram.org/bots/api#successfulpayment).
- Ship the goods or provide the services.

For more details, feel free to check out our full exhaustive **guides** for selling goods and services on Telegram – they include live checklists, parameters and in-depth method descriptions:

- [Guide for digital goods and services](https://core.telegram.org/bots/payments-stars)
- [Guide for physical goods and services](https://core.telegram.org/bots/payments)

Telegram does not directly process the payments, does not store data about orders and does not collect any fees. Invoices are forwarded directly to the third-party payment provider.

For this reason, disputes must be solved between the user, the bot developer and the payment provider. You can read more about this in the [Privacy Policy](https://telegram.org/privacy#7-third-party-payment-services).

### **Web Login**

Telegram offers a **flexible**, **lightweight** and **free** framework to authenticate users on any website and app. This can be used to bridge your platform with Telegram, providing a smooth experience to your users. You can also freely rely on this framework to implement a **fast** and **signup-free** login on your site, regardless of its connection to Telegram.

### **Widgets**

The Telegram login widget is a **simple and secure way to authorize users** on your website.

1. Choose a bot – ideally its name and profile pic **should match** the website title and logo.
2. Use the /setdomain command in [@BotFather](https://t.me/botfather) to pair the bot with your website domain.
3. Configure your widget using [our dedicated tool](https://core.telegram.org/widgets/login#widget-configuration) and embed it on your website.

### **Inline Login**

When users open your website via an **inline button**, you can use the [login_url](https://core.telegram.org/bots/api#loginurl) parameter as an alternative to login widgets. This way, you'll be able to [seamlessly authorize](https://telegram.org/blog/privacy-discussions-web-bots#meet-seamless-web-bots) them on your website or app before the page even loads.

Make sure to review our [guide](https://core.telegram.org/widgets/login#checking-authorization) on authenticating the received data as well as our [sample code](https://gist.github.com/anonymous/6516521b1fb3b464534fbc30ea3573c2).

### **HTML5 Games**

Bots can serve as **standalone gaming platforms** – with our [HTML5 Gaming API](https://core.telegram.org/bots/api#games) you can develop multiplayer or single-player games and let your users have fun comparing **ranks**, **scores** and much more.

To get started, follow these simple steps:

- Send the /newgame command to [@BotFather](https://t.me/botfather)
- Provide a **description text**, an **image** or an **optional gif** to showcase its gameplay
- Send the game to users via the [sendGame](https://core.telegram.org/bots/api#sendgame) method or via an [inline query](https://core.telegram.org/bots/api#inlinequeryresultgame)
- When someone wants to play, you'll receive the appropriate game_short_name in a [CallbackQuery](https://core.telegram.org/bots/api#callbackquery)
- To launch the game, provide the **HTML5 Game URL** as the url param of [answerCallbackQuery](https://core.telegram.org/bots/api#answercallbackquery)

Then, to handle **highscores**:

- Use [setGameScore](https://core.telegram.org/bots/api#setgamescore) to post high scores in the chat with the game
- Use [getGameHighScores](https://core.telegram.org/bots/api#getgamehighscores) to get in-game high score tables

You can also **embed a share button** within your game, play around with **custom inline buttons**, **URL parameters** and much more. To get a better idea, make sure to check out:

- [HTML5 Games Manual](https://core.telegram.org/bots/games)
- [HTML5 Games Bot API Docs](https://core.telegram.org/bots/api#games)

Check out [@GameBot](https://t.me/gamebot) and [@gamee](https://t.me/gamee) for examples of what you can do using our Gaming Platform.

### **Stickers and Custom Emoji**

[Stickers](https://core.telegram.org/stickers) and [Custom Emoji](https://telegram.org/blog/custom-emoji) are a distinctive Telegram feature used by millions of users to share artwork every day. Stickers and custom emoji take many forms – ranging from **basic images** to smooth **vector animations** and high-detail **.WEBM videos**.

All these formats are supported by our [Bot API](https://core.telegram.org/bots/api#stickers), which allows bots to **create**, **edit**, **delete** and **share** new artwork packs on the fly. Telegram's [Import API](https://core.telegram.org/import-stickers) lets users **migrate packs** from other platforms and sticker apps.

**Creating a new pack**

To create a **new pack**, simply:

- **Prepare** your artwork following our [technical requirements](https://core.telegram.org/stickers).
- **Create** a new sticker pack via [createStickerSet](https://core.telegram.org/bots/api#createnewstickerset). Set sticker_type to *regular* to create a sticker pack or to *custom emoji* to create a pack of custom emoji. Attach the [files](https://core.telegram.org/bots/api#file) you wish to include in the pack as an array of [InputSticker](https://core.telegram.org/bots#inputsticker)
- You can use [addStickerToSet](https://core.telegram.org/bots/api#addstickertoset) to add stickers or emoji later on.

**Additional features**

Regular stickers and custom emoji support **keywords** that users can type to quickly find the respective artwork – this can be useful when a sticker doesn't have obvious ties to a specific emoji. You can use the keywords parameter in [InputSticker](https://core.telegram.org/bots#inputsticker) to specify them.

Custom emoji additionally support **adaptive colors** – they will always match the current context (e.g., white on photos, accent color when used as status, etc.); to enable this feature, use the needs_repainting parameter in [createStickerSet](https://core.telegram.org/bots/api#createnewstickerset).

Once you're done creating and sharing your artwork, don't forget to check out our [remaining sticker methods](https://core.telegram.org/bots/api#stickers) to find out how to [edit](https://core.telegram.org/bots/api#setstickersetthumb), [delete](https://core.telegram.org/bots/api#deletestickerfromset) and even [reorder](https://core.telegram.org/bots/api#setstickerpositioninset) your pack.

Note that these methods will only work on packs **created by the bot that is calling them**.

### **Language Support**

Bots can tailor their interfaces to **support multiple languages** – updating inputs and information on the fly. A user’s [language_code](https://core.telegram.org/bots/api#user) is included in every relevant [update](https://core.telegram.org/bots/api#update) as an [IETF language tag](https://en.wikipedia.org/wiki/IETF_language_tag), allowing bots to adapt accordingly.

We recommend that you follow our guidelines to provide **the best user experience**.

- Your interfaces, texts and [inline results](https://core.telegram.org/bots/api#answerinlinequery) should adapt seamlessly to the *language_code*, without user intervention.
- Connected [WebApps](https://core.telegram.org/bots/webapps) will receive the user's *language_code* – your HTML page should account for it.
- [HTML5 Games](https://core.telegram.org/bots/games) can obtain language information if you specify it as a [URL parameter](https://core.telegram.org/bots/games#using-url-parameters). You can generate this parameter from the *language_code* field in the [User](https://core.telegram.org/bots/api#user) object served with the initial game [CallbackQuery](https://core.telegram.org/bots/api#callbackquery).
- The bot's **Name**, **Description** and **About text** can be natively localized with the respective [methods](https://core.telegram.org/bots/api#setmydescription).
- Command lists can also be specified for individual languages – more on this [here](https://core.telegram.org/bots/features#commands).

The *language_code* is an **optional field** – it could be empty.

If you target the general public, your code should always fall back to either the last recorded language tag or English (in this order) when the field is missing for a specific user.

---

### **Bot Management**

### **Privacy Mode**

Bots are frequently added to groups to perform basic tasks or assist moderators – like automatically posting company announcements or even celebrating birthdays. By default, **all bots** added to groups run in Privacy Mode and only see relevant messages and commands:

- Commands explicitly meant for them (e.g., /command@this_bot).
- General commands (e.g. /start) if the bot was the last bot to send a message to the group.
- Inline messages sent [via](https://core.telegram.org/bots/api#inline-mode) the bot.
- Replies to any messages implicitly or explicitly meant for this bot.

All bots will also receive, **regardless of privacy mode**:

- All service messages.
- All messages from private chats.
- All messages from channels where they are a member.

Privacy mode is **enabled by default** for all bots, except bots that were added to a group as admins (bot admins always receive **all messages**). It can be disabled so that the bot receives all messages like an ordinary user (the bot will need to be re-added to the group for this change to take effect). We only recommend doing this in cases where it is **absolutely necessary** for your bot to work. In most cases, using the force reply option for the bot's messages should be more than enough.

This mode not only increases user privacy, but also makes the bot more efficient by reducing the number of inputs it needs to process. Users can always see a bot’s current privacy setting in the list of group members.

### **Testing your bot**

You can quickly test your bot **without interfering** with its users by simply running another instance of your code on a different bot account. To do so, create a *new bot* via [@BotFather](https://t.me/botfather), obtain its token and use it in the testing instance of your code.

All further testing and debugging can happen privately on the new bot, without affecting the original instance.

If you need to share file references across bots, note that the file_id field is tied to a single bot id, so your test instance cannot use a shared file_id database to quickly send media – files must be individually reuploaded.

### **Dedicated test environment**

Telegram also offers a dedicated **test environment** suitable for more advanced testing. Bots and users in this environment generally have more flexible restrictions – for example:

- When working with the test environment, you may use HTTP links without TLS to test your [Web Apps](https://core.telegram.org/bots/features#web-apps) or [Web Login](https://core.telegram.org/bots/features#web-login).

**Flood limits** are not raised in the test environment, and may at times be stricter. To minimize how this impacts your bot, you should make sure that it handles errors with retry policies and does not depend on hardcoded limit values.

### **Creating a bot in the test environment**

The test environment is **completely separate** from the main environment, so you will need to create a new user account and a new bot with [@BotFather](https://t.me/botfather).

To create an account and log in, use either of the following:

- **iOS**: tap 10 times on the Settings icon > Accounts > Login to another account > Test.
- **Telegram Desktop**: open ☰ Settings > Shift + Alt + Right click 'Add Account' and select 'Test Server'.
- **macOS**: click the Settings icon 10 times to open the Debug Menu, ⌘ + click 'Add Account' and log in via phone number.

After logging in, simply [create a new bot](https://core.telegram.org/bots/features#creating-a-new-bot) following the standard procedure and send your requests to the Test Bot API in this format:

https://api.telegram.org/bot<token>/test/METHOD_NAME

When working with the test environment, you may use HTTP links without TLS in the url field of both [LoginUrl](https://core.telegram.org/bots/api#loginurl) and [WebAppInfo](https://core.telegram.org/bots/api#webappinfo).

### **Status alerts**

Millions choose Telegram for its speed. To best benefit users, your bot also **needs to be responsive**. In order to help developers keep their bots in shape, [@BotFather](https://t.me/botfather) will send **status alerts** if it sees something is wrong.

We check the number of replies and the *request/response* conversion rate for popular bots (~300 requests per minute, this value may change in the future). If your bot returns an **abnormally low number**, you will receive a notification from [@BotFather](https://t.me/botfather).

### **Responding to alerts**

By default, **you will only get one alert per bot per hour**.

Each alert has the following buttons:

- **Fixed** - Use this if you found an issue with your bot and fixed it. If you press the fix button, we will resume sending alerts in the regular way so that you can see if your fix worked within 5-10 minutes instead of having to wait for an hour.
- **Support** - Use this to open a chat with [@BotSupport](https://t.me/botsupport) if you don't see any issues with your bot or if you think the problem is on our side.
- **Mute for 8h/1w** - Use this if you can't fix your bot at the moment. This will disable all alerts for the bot in question for the specified period of time. **We do not recommend** using this option since your users may migrate to a more stable bot. You can unmute alerts in your bot's settings via [@BotFather](https://t.me/botfather).

### **Monitored issues**

We currently notify you about the following issues:

- **Too few private messages are sent.** Value: **{value}** - Your bot is sending far fewer messages than it did in previous weeks. This is useful for newsletter-style bots that send messages without prompts from users. The larger the value, the more significant the difference.
- **Too few replies to incoming private messages**. Conversion rate: **{value}** - Your bot is not replying to all messages that are being sent to it (the request/response conversion rate for your bot was too low for at least two of the last three 5-minute periods).

To provide a good user experience, please respond to all messages that are sent to your bot. Respond to message updates by calling send… methods (e.g. [sendMessage](https://core.telegram.org/bots/api#sendmessage)).

- **Too few answers to inline queries**. Conversion rate: **{value}** - Your bot is not replying to all inline queries that are being sent to it, calculated in the same way as above. Respond to inline_query updates by calling [answerInlineQuery](https://core.telegram.org/bots/api#answerinlinequery).
- **Too few answers to callback queries**. Conversion rate: **{value}**
- **Too few answers to callback game queries**. Conversion rate: **{value}** - Your bot is not replying to all callback queries that are being sent to it (with or without games), calculated in the same way as above. Respond to callback_query updates by calling [answerCallbackQuery](https://core.telegram.org/bots/api#answercallbackquery).

### **Local Bot API**

You can host and work with **your own instance** of our open-source [Bot API](https://core.telegram.org/bots/api).

The **source code** is available [here](https://github.com/tdlib/telegram-bot-api), along with a quick [installation guide](https://github.com/tdlib/telegram-bot-api#installation).

After **installing the server**, remember to use the [logOut](https://core.telegram.org/bots/api#logout) method before **redirecting requests** to your new local API URL.

Your local instance runs on port 8081 by default and will only accept HTTP requests, so a TLS termination proxy has to be used to handle remote HTTPS requests.

By hosting our API locally you'll gain access to **some upgrades**, including:

| **API** | **Max File Download** | **Max File Upload** | **WHook URL** | **WHook Port** | **WHook Max Connections** |
| --- | --- | --- | --- | --- | --- |
| [Official](https://core.telegram.org/bots/api#making-requests) | 20MB | 50MB | HTTPS | 443,80,88,8443 | 1-100 |
| [Local](https://core.telegram.org/bots/api#using-a-local-bot-api-server) | Unlimited | 2000MB | HTTP | Any port | 1-100000 |

You can find an exhaustive list [here](https://core.telegram.org/bots/api#using-a-local-bot-api-server).

All limits may be subject to change in the future, so make sure to follow [@BotNews](https://t.me/botnews).

---

### **BotFather**

Below is a detailed guide to using [@BotFather](https://t.me/botfather), Telegram’s tool for **creating** and **managing** bots.

### **Creating a new bot**

Use the /newbot command to create a new bot. [@BotFather](https://t.me/botfather) will ask you for a name and username, then generate an authentication token for your new bot.

- The **name** of your bot is displayed in contact details and elsewhere.
- The **username** is a short name, used in search, mentions and t.me links. Usernames are 5-32 characters long and not case sensitive – but may only include Latin characters, numbers, and underscores. Your bot's username must end in 'bot’, like 'tetris_bot' or 'TetrisBot'.
- The **token** is a string, like 110201543:AAHdqTcvCH1vGWJxfSeofSAs0K5PALDsaw, which is required to authorize the bot and send requests to the Bot API. Keep your token secure and store it safely, it can be used by anyone to control your bot.

Unlike the bot’s name, the username cannot be changed later – so choose it carefully.

When sending a request to api.telegram.org, remember to prefix the word ‘bot’ to your token.

### **About text, description and profile media**

When new users open your bot, they will be met with a helpful description in a box titled “What can this bot do?”.

Properly [setting this field](https://core.telegram.org/bots/features#edit-bots) in [@BotFather](https://t.me/botfather) allows everyone to immediately get an idea of what your bot can do – your description should be **brief**, **to the point** and **on topic**.

You can also add a photo or video to this field with Edit Description Picture in [@BotFather](https://t.me/botfather).

Additionally, just like normal users, bots also come with a **short bio** available on their profile. If you didn't specify this field while first creating your bot, you can set it at any time with the /setabouttext command in [@BotFather](https://t.me/botfather). Users can interact with many bots and they won't have access to their description after starting them – having a quick reminder of the bot's purpose can be very useful.

Note that both the **Description** and the **About text** can be [natively localized](https://core.telegram.org/bots/api#setmydescription) – each user will automatically see the correct translation for their language.

Bots can also have a **profile picture** – you should pick something unique and original so that users can find it in their chat list at a glance.

Starting from April 21, 2023 ([Telegram 9.6](https://telegram.org/blog/shareable-folders-custom-wallpapers)), you can edit your bot directly from its profile page – including setting a custom **profile video**.

### **Generating an authentication token**

If your existing token is **compromised** or **you lost it** for some reason, use the /token command to generate a new one.

### **Transfer ownership**

You can transfer ownership of your bot **to another user**.

To do this, send /mybots, select your bot, then *transfer ownership*.

You can only transfer a bot to users who have interacted with it at least once.

Transferring ownership will give full control of the bot to another user – they will be able to access the bot’s messages and even delete it. The transfer is permanent, so please consider it carefully.

### **BotFather commands**

The remaining commands are pretty self-explanatory:

- /mybots – returns a list of your bots with handy controls to edit their settings.
- /mygames – does the same for your games.

### **Edit bots**

To edit your bot, you have two options.

You can use the available commands:

- /setname – change your bot's **name**.
- /setdescription – change the bot's **description** (short text up to 512 characters). Users will see this text at the beginning of the conversation with the bot, titled '*What can this bot do?*'.
- /setabouttext – change the bot's **about info**, a shorter text up to 120 characters. Users will see this text on the bot's profile page. When they share your bot with someone, this text is sent together with the link.
- /setuserpic – change the bot's **profile picture**.
- /setcommands – change the list of **commands** supported by your bot. Users will see these commands as suggestions when they type / in the chat with your bot. See [commands](https://core.telegram.org/bots/features#commands) for more info.
- /setdomain – link a **website domain** to your bot. See the [login widget](https://core.telegram.org/bots/features#login-widget) section.
- /deletebot – delete your bot and **free its username**. Cannot be undone.

Or you can use the /mybots command, tap on your bot and use the modern inline interface to edit it.

Starting from April 21, 2023 ([Telegram 9.6](https://telegram.org/blog/shareable-folders-custom-wallpapers)), you can edit your bot's public-facing info directly from its profile page – including setting a custom **profile video**.

### **Edit settings**

- /setinline – toggle **inline mode** for your bot.
- /setinlinegeo – request **location data** to provide location-based inline results.
- /setjoingroups – toggle whether your bot can be **added to groups** or not. All bots must be able to process direct messages, but if your bot was not designed to work in groups, you can disable this.
- /setinlinefeedback – toggle whether the API should **send updates about the results** chosen by users. See an in-depth explanation [here](https://core.telegram.org/bots/inline#collecting-feedback).
- /setprivacy – set which messages your bot will receive when added to a group. See [privacy-mode](https://core.telegram.org/bots/features#privacy-mode) for more info.

### **Manage games**

- /newgame – create a new game.
- /listgames – see a list of your games.
- /editgame – edit a game.
- /deletegame – delete an existing game.

Please note that it may take a few minutes for changes to take effect.

---

With this information, you are ready to proceed to our [Full API Reference for Developers](https://core.telegram.org/bots/api).

- If you have any questions, check out our [Bot FAQ](https://core.telegram.org/bots/faq).
- If you're experiencing issues with our API, please contact [@BotSupport](https://t.me/botsupport) on Telegram.