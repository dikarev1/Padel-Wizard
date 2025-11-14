# Официальный док “Telegram API doc”

# **Telegram Bot API**

> The Bot API is an HTTP-based interface created for developers keen on building bots for Telegram.
> 
> 
> To learn how to create and set up a bot, please consult our [**Introduction to Bots**](https://core.telegram.org/bots) and [**Bot FAQ**](https://core.telegram.org/bots/faq).
> 

### **Recent changes**

> Subscribe to @BotNews to be the first to know about the latest updates and join the discussion in @BotTalk
> 

### **August 15, 2025**

**Bot API 9.2**

**Checklists**

- Added the field *checklist_task_id* to the class [ReplyParameters](https://core.telegram.org/bots/api#replyparameters), allowing bots to reply to a specific checklist task.
- Added the field *reply_to_checklist_task_id* to the class [Message](https://core.telegram.org/bots/api#message).

**Gifts**

- Added the field *publisher_chat* to the classes [Gift](https://core.telegram.org/bots/api#gift) and [UniqueGift](https://core.telegram.org/bots/api#uniquegift) which can be used to get information about the chat that published a gift.

**Direct Messages in Channels**

- Added the field *is_direct_messages* to the classes [Chat](https://core.telegram.org/bots/api#chat) and [ChatFullInfo](https://core.telegram.org/bots/api#chatfullinfo) which can be used to identify supergroups that are used as channel direct messages chats.
- Added the field *parent_chat* to the class [ChatFullInfo](https://core.telegram.org/bots/api#chatfullinfo) which indicates the parent channel chat for a channel direct messages chat.
- Added the class [DirectMessagesTopic](https://core.telegram.org/bots/api#directmessagestopic) and the field *direct_messages_topic* to the class [Message](https://core.telegram.org/bots/api#message), describing a topic of a direct messages chat.
- Added the parameter *direct_messages_topic_id* to the methods [sendMessage](https://core.telegram.org/bots/api#sendmessage), [sendPhoto](https://core.telegram.org/bots/api#sendphoto), [sendVideo](https://core.telegram.org/bots/api#sendvideo), [sendAnimation](https://core.telegram.org/bots/api#sendanimation), [sendAudio](https://core.telegram.org/bots/api#sendaudio), [sendDocument](https://core.telegram.org/bots/api#senddocument), [sendPaidMedia](https://core.telegram.org/bots/api#sendpaidmedia), [sendSticker](https://core.telegram.org/bots/api#sendsticker), [sendVideoNote](https://core.telegram.org/bots/api#sendvideonote), [sendVoice](https://core.telegram.org/bots/api#sendvoice), [sendLocation](https://core.telegram.org/bots/api#sendlocation), [sendVenue](https://core.telegram.org/bots/api#sendvenue), [sendContact](https://core.telegram.org/bots/api#sendcontact), [sendDice](https://core.telegram.org/bots/api#senddice), [sendInvoice](https://core.telegram.org/bots/api#sendinvoice), [sendMediaGroup](https://core.telegram.org/bots/api#sendmediagroup), [copyMessage](https://core.telegram.org/bots/api#copymessage), [copyMessages](https://core.telegram.org/bots/api#copymessages), [forwardMessage](https://core.telegram.org/bots/api#forwardmessage) and [forwardMessages](https://core.telegram.org/bots/api#forwardmessages). This parameter can be used to send a message to a direct messages chat topic.

**Suggested Posts**

- Added the class [SuggestedPostParameters](https://core.telegram.org/bots/api#suggestedpostparameters) and the parameter *suggested_post_parameters* to the methods [sendMessage](https://core.telegram.org/bots/api#sendmessage), [sendPhoto](https://core.telegram.org/bots/api#sendphoto), [sendVideo](https://core.telegram.org/bots/api#sendvideo), [sendAnimation](https://core.telegram.org/bots/api#sendanimation), [sendAudio](https://core.telegram.org/bots/api#sendaudio), [sendDocument](https://core.telegram.org/bots/api#senddocument), [sendPaidMedia](https://core.telegram.org/bots/api#sendpaidmedia), [sendSticker](https://core.telegram.org/bots/api#sendsticker), [sendVideoNote](https://core.telegram.org/bots/api#sendvideonote), [sendVoice](https://core.telegram.org/bots/api#sendvoice), [sendLocation](https://core.telegram.org/bots/api#sendlocation), [sendVenue](https://core.telegram.org/bots/api#sendvenue), [sendContact](https://core.telegram.org/bots/api#sendcontact), [sendDice](https://core.telegram.org/bots/api#senddice), [sendInvoice](https://core.telegram.org/bots/api#sendinvoice), [copyMessage](https://core.telegram.org/bots/api#copymessage), [forwardMessage](https://core.telegram.org/bots/api#forwardmessage). This parameter can be used to send a suggested post to a direct messages chat topic.
- Added the method [approveSuggestedPost](https://core.telegram.org/bots/api#approvesuggestedpost), allowing bots to approve incoming suggested posts.
- Added the method [declineSuggestedPost](https://core.telegram.org/bots/api#declinesuggestedpost), allowing bots to decline incoming suggested posts.
- Added the field *can_manage_direct_messages* to the classes [ChatMemberAdministrator](https://core.telegram.org/bots/api#chatmemberadministrator) and [ChatAdministratorRights](https://core.telegram.org/bots/api#chatadministratorrights).
- Added the parameter *can_manage_direct_messages* to the method [promoteChatMember](https://core.telegram.org/bots/api#promotechatmember).
- Added the field *is_paid_post* to the class [Message](https://core.telegram.org/bots/api#message), which can be used to identify paid posts. Such posts must not be deleted for 24 hours to receive the payment.
- Added the class [SuggestedPostPrice](https://core.telegram.org/bots/api#suggestedpostprice), describing the price of a suggested post.
- Added the class [SuggestedPostInfo](https://core.telegram.org/bots/api#suggestedpostinfo) and the field *suggested_post_info* to the class [Message](https://core.telegram.org/bots/api#message), describing a suggested post.
- Added the class [SuggestedPostApproved](https://core.telegram.org/bots/api#suggestedpostapproved) and the field *suggested_post_approved* to the class [Message](https://core.telegram.org/bots/api#message), describing a service message about the approval of a suggested post.
- Added the class [SuggestedPostApprovalFailed](https://core.telegram.org/bots/api#suggestedpostapprovalfailed) and the field *suggested_post_approval_failed* to the class [Message](https://core.telegram.org/bots/api#message), describing a service message about the failed approval of a suggested post.
- Added the class [SuggestedPostDeclined](https://core.telegram.org/bots/api#suggestedpostdeclined) and the field *suggested_post_declined* to the class [Message](https://core.telegram.org/bots/api#message), describing a service message about the rejection of a suggested post.
- Added the class [SuggestedPostPaid](https://core.telegram.org/bots/api#suggestedpostpaid) and the field *suggested_post_paid* to the class [Message](https://core.telegram.org/bots/api#message), describing a service message about a successful payment for a suggested post.
- Added the class [SuggestedPostRefunded](https://core.telegram.org/bots/api#suggestedpostrefunded) and the field *suggested_post_refunded* to the class [Message](https://core.telegram.org/bots/api#message), describing a service message about a payment refund for a suggested post.

### **July 3, 2025**

**Bot API 9.1**

**Checklists**

- Added the class [ChecklistTask](https://core.telegram.org/bots/api#checklisttask) representing a task in a checklist.
- Added the class [Checklist](https://core.telegram.org/bots/api#checklist) representing a checklist.
- Added the class [InputChecklistTask](https://core.telegram.org/bots/api#inputchecklisttask) representing a task to add to a checklist.
- Added the class [InputChecklist](https://core.telegram.org/bots/api#inputchecklist) representing a checklist to create.
- Added the field *checklist* to the classes [Message](https://core.telegram.org/bots/api#message) and [ExternalReplyInfo](https://core.telegram.org/bots/api#externalreplyinfo), describing a checklist in a message.
- Added the class [ChecklistTasksDone](https://core.telegram.org/bots/api#checklisttasksdone) and the field *checklist_tasks_done* to the class [Message](https://core.telegram.org/bots/api#message), describing a service message about status changes for tasks in a checklist (i.e., marked as done/not done).
- Added the class [ChecklistTasksAdded](https://core.telegram.org/bots/api#checklisttasksadded) and the field *checklist_tasks_added* to the class [Message](https://core.telegram.org/bots/api#message), describing a service message about the addition of new tasks to a checklist.
- Added the method [sendChecklist](https://core.telegram.org/bots/api#sendchecklist), allowing bots to send a checklist on behalf of a business account.
- Added the method [editMessageChecklist](https://core.telegram.org/bots/api#editmessagechecklist), allowing bots to edit a checklist on behalf of a business account.

**Gifts**

- Added the field *next_transfer_date* to the classes [OwnedGiftUnique](https://core.telegram.org/bots/api#ownedgiftunique) and [UniqueGiftInfo](https://core.telegram.org/bots/api#uniquegiftinfo).
- Added the field *last_resale_star_count* to the class [UniqueGiftInfo](https://core.telegram.org/bots/api#uniquegiftinfo).
- Added “resale” as the possible value of the field *origin* in the class [UniqueGiftInfo](https://core.telegram.org/bots/api#uniquegiftinfo).

**General**

- Increased the maximum number of options in a poll to 12.
- Added the method [getMyStarBalance](https://core.telegram.org/bots/api#getmystarbalance), allowing bots to get their current balance of Telegram Stars.
- Added the class [DirectMessagePriceChanged](https://core.telegram.org/bots/api#directmessagepricechanged) and the field *direct_message_price_changed* to the class [Message](https://core.telegram.org/bots/api#message), describing a service message about a price change for direct messages sent to the channel chat.
- Added the method *hideKeyboard* to the class [WebApp](https://core.telegram.org/bots/webapps#initializing-mini-apps).

### **April 11, 2025**

**Bot API 9.0**

**Business Accounts**

- Added the class [BusinessBotRights](https://core.telegram.org/bots/api#businessbotrights) and replaced the field *can_reply* with the field *rights* of the type [BusinessBotRights](https://core.telegram.org/bots/api#businessbotrights) in the class [BusinessConnection](https://core.telegram.org/bots/api#businessconnection).
- Added the method [readBusinessMessage](https://core.telegram.org/bots/api#readbusinessmessage), allowing bots to mark incoming messages as read on behalf of a business account.
- Added the method [deleteBusinessMessages](https://core.telegram.org/bots/api#deletebusinessmessages), allowing bots to delete messages on behalf of a business account.
- Added the method [setBusinessAccountName](https://core.telegram.org/bots/api#setbusinessaccountname), allowing bots to change the first and last name of a managed business account.
- Added the method [setBusinessAccountUsername](https://core.telegram.org/bots/api#setbusinessaccountusername), allowing bots to change the username of a managed business account.
- Added the method [setBusinessAccountBio](https://core.telegram.org/bots/api#setbusinessaccountbio), allowing bots to change the bio of a managed business account.
- Added the class [InputProfilePhoto](https://core.telegram.org/bots/api#inputprofilephoto), describing a profile photo to be set.
- Added the methods [setBusinessAccountProfilePhoto](https://core.telegram.org/bots/api#setbusinessaccountprofilephoto) and [removeBusinessAccountProfilePhoto](https://core.telegram.org/bots/api#removebusinessaccountprofilephoto), allowing bots to change the profile photo of a managed business account.
- Added the method [setBusinessAccountGiftSettings](https://core.telegram.org/bots/api#setbusinessaccountgiftsettings), allowing bots to change the privacy settings pertaining to incoming gifts in a managed business account.
- Added the class [StarAmount](https://core.telegram.org/bots/api#staramount) and the method [getBusinessAccountStarBalance](https://core.telegram.org/bots/api#getbusinessaccountstarbalance), allowing bots to check the current Telegram Star balance of a managed business account.
- Added the method [transferBusinessAccountStars](https://core.telegram.org/bots/api#transferbusinessaccountstars), allowing bots to transfer Telegram Stars from the balance of a managed business account to their own balance for withdrawal.
- Added the classes [OwnedGiftRegular](https://core.telegram.org/bots/api#ownedgiftregular), [OwnedGiftUnique](https://core.telegram.org/bots/api#ownedgiftunique), [OwnedGifts](https://core.telegram.org/bots/api#ownedgifts) and the method [getBusinessAccountGifts](https://core.telegram.org/bots/api#getbusinessaccountgifts), allowing bots to fetch the list of gifts owned by a managed business account.
- Added the method [convertGiftToStars](https://core.telegram.org/bots/api#convertgifttostars), allowing bots to convert gifts received by a managed business account to Telegram Stars.
- Added the method [upgradeGift](https://core.telegram.org/bots/api#upgradegift), allowing bots to upgrade regular gifts received by a managed business account to unique gifts.
- Added the method [transferGift](https://core.telegram.org/bots/api#transfergift), allowing bots to transfer unique gifts owned by a managed business account.
- Added the classes [InputStoryContentPhoto](https://core.telegram.org/bots/api#inputstorycontentphoto) and [InputStoryContentVideo](https://core.telegram.org/bots/api#inputstorycontentvideo) representing the content of a story to post.
- Added the classes [StoryArea](https://core.telegram.org/bots/api#storyarea), [StoryAreaPosition](https://core.telegram.org/bots/api#storyareaposition), [LocationAddress](https://core.telegram.org/bots/api#locationaddress), [StoryAreaTypeLocation](https://core.telegram.org/bots/api#storyareatypelocation), [StoryAreaTypeSuggestedReaction](https://core.telegram.org/bots/api#storyareatypesuggestedreaction), [StoryAreaTypeLink](https://core.telegram.org/bots/api#storyareatypelink), [StoryAreaTypeWeather](https://core.telegram.org/bots/api#storyareatypeweather) and [StoryAreaTypeUniqueGift](https://core.telegram.org/bots/api#storyareatypeuniquegift), describing clickable active areas on stories.
- Added the method [postStory](https://core.telegram.org/bots/api#poststory), allowing bots to post a story on behalf of a managed business account.
- Added the method [editStory](https://core.telegram.org/bots/api#editstory), allowing bots to edit stories they had previously posted on behalf of a managed business account.
- Added the method [deleteStory](https://core.telegram.org/bots/api#deletestory), allowing bots to delete stories they had previously posted on behalf of a managed business account.

**Mini Apps**

- Added the field [DeviceStorage](https://core.telegram.org/bots/webapps#devicestorage), allowing Mini Apps to use persistent local storage on the user's device.
- Added the field [SecureStorage](https://core.telegram.org/bots/webapps#securestorage), allowing Mini Apps to use a secure local storage on the user's device for sensitive data.

**Gifts**

- Added the classes [UniqueGiftModel](https://core.telegram.org/bots/api#uniquegiftmodel), [UniqueGiftSymbol](https://core.telegram.org/bots/api#uniquegiftsymbol), [UniqueGiftBackdropColors](https://core.telegram.org/bots/api#uniquegiftbackdropcolors), and [UniqueGiftBackdrop](https://core.telegram.org/bots/api#uniquegiftbackdrop) to describe the properties of a unique gift.
- Added the class [UniqueGift](https://core.telegram.org/bots/api#uniquegift) describing a gift that was upgraded to a unique one.
- Added the class [AcceptedGiftTypes](https://core.telegram.org/bots/api#acceptedgifttypes) describing the types of gifts that are accepted by a user or a chat.
- Replaced the field *can_send_gift* with the field *accepted_gift_types* of the type [AcceptedGiftTypes](https://core.telegram.org/bots/api#acceptedgifttypes) in the class [ChatFullInfo](https://core.telegram.org/bots/api#chatfullinfo).
- Added the class [GiftInfo](https://core.telegram.org/bots/api#giftinfo) and the field *gift* to the class [Message](https://core.telegram.org/bots/api#message), describing a service message about a regular gift that was sent or received.
- Added the class [UniqueGiftInfo](https://core.telegram.org/bots/api#uniquegiftinfo) and the field *unique_gift* to the class [Message](https://core.telegram.org/bots/api#message), describing a service message about a unique gift that was sent or received.

**Telegram Premium**

- Added the method [giftPremiumSubscription](https://core.telegram.org/bots/api#giftpremiumsubscription), allowing bots to gift a user a Telegram Premium subscription paid in Telegram Stars.
- Added the field *premium_subscription_duration* to the class [TransactionPartnerUser](https://core.telegram.org/bots/api#transactionpartneruser) for transactions involving a Telegram Premium subscription purchased by the bot.
- Added the field *transaction_type* to the class [TransactionPartnerUser](https://core.telegram.org/bots/api#transactionpartneruser), simplifying the differentiation and processing of all transaction types.

**General**

- Increased the maximum price for paid media to 10000 Telegram Stars.
- Increased the maximum price for a subscription period to 10000 Telegram Stars.
- Added the class [PaidMessagePriceChanged](https://core.telegram.org/bots/api#paidmessagepricechanged) and the field *paid_message_price_changed* to the class [Message](https://core.telegram.org/bots/api#message), describing a service message about a price change for paid messages sent to the chat.
- Added the field *paid_star_count* to the class [Message](https://core.telegram.org/bots/api#message), containing the number of [Telegram Stars](https://telegram.org/blog/telegram-stars) that were paid to send the message.

[**See earlier changes »**](https://core.telegram.org/bots/api-changelog)

### **Authorizing your bot**

Each bot is given a unique authentication token [when it is created](https://core.telegram.org/bots/features#botfather). The token looks something like `123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11`, but we'll use simply **<token>** in this document instead. You can learn about obtaining tokens and generating new ones in [this document](https://core.telegram.org/bots/features#botfather).

### **Making requests**

All queries to the Telegram Bot API must be served over HTTPS and need to be presented in this form: `https://api.telegram.org/bot<token>/METHOD_NAME`. Like this for example:

```
https://api.telegram.org/bot123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11/getMe
```

We support **GET** and **POST** HTTP methods. We support four ways of passing parameters in Bot API requests:

- [URL query string](https://en.wikipedia.org/wiki/Query_string)
- application/x-www-form-urlencoded
- application/json (except for uploading files)
- multipart/form-data (use to upload files)

The response contains a JSON object, which always has a Boolean field 'ok' and may have an optional String field 'description' with a human-readable description of the result. If 'ok' equals *True*, the request was successful and the result of the query can be found in the 'result' field. In case of an unsuccessful request, 'ok' equals false and the error is explained in the 'description'. An Integer 'error_code' field is also returned, but its contents are subject to change in the future. Some errors may also have an optional field 'parameters' of the type [ResponseParameters](https://core.telegram.org/bots/api#responseparameters), which can help to automatically handle the error.

- All methods in the Bot API are case-insensitive.
- All queries must be made using UTF-8.

### **Making requests when getting updates**

If you're using [**webhooks**](https://core.telegram.org/bots/api#getting-updates), you can perform a request to the Bot API while sending an answer to the webhook. Use either *application/json* or *application/x-www-form-urlencoded* or *multipart/form-data* response content type for passing parameters. Specify the method to be invoked in the *method* parameter of the request. It's not possible to know that such a request was successful or get its result.

> Please see our FAQ for examples.
> 

### **Using a Local Bot API Server**

The Bot API server source code is available at [telegram-bot-api](https://github.com/tdlib/telegram-bot-api). You can run it locally and send the requests to your own server instead of `https://api.telegram.org`. If you switch to a local Bot API server, your bot will be able to:

- Download files without a size limit.
- Upload files up to 2000 MB.
- Upload files using their local path and [the file URI scheme](https://en.wikipedia.org/wiki/File_URI_scheme).
- Use an HTTP URL for the webhook.
- Use any local IP address for the webhook.
- Use any port for the webhook.
- Set *max_webhook_connections* up to 100000.
- Receive the absolute local path as a value of the *file_path* field without the need to download the file after a [getFile](https://core.telegram.org/bots/api#getfile) request.

### **Do I need a Local Bot API Server**

The majority of bots will be OK with the default configuration, running on our servers. But if you feel that you need one of [these features](https://core.telegram.org/bots/api#using-a-local-bot-api-server), you're welcome to switch to your own at any time.

### **Getting updates**

There are two mutually exclusive ways of receiving updates for your bot - the [getUpdates](https://core.telegram.org/bots/api#getupdates) method on one hand and [webhooks](https://core.telegram.org/bots/api#setwebhook) on the other. Incoming updates are stored on the server until the bot receives them either way, but they will not be kept longer than 24 hours.

Regardless of which option you choose, you will receive JSON-serialized [Update](https://core.telegram.org/bots/api#update) objects as a result.

### **Update**

This [object](https://core.telegram.org/bots/api#available-types) represents an incoming update.

At most **one** of the optional parameters can be present in any given update.

| Field | Type | Description |
| --- | --- | --- |
| update_id | Integer | The update's unique identifier. Update identifiers start from a certain positive number and increase sequentially. This identifier becomes especially handy if you're using [webhooks](https://core.telegram.org/bots/api#setwebhook), since it allows you to ignore repeated updates or to restore the correct update sequence, should they get out of order. If there are no new updates for at least a week, then identifier of the next update will be chosen randomly instead of sequentially. |
| message | [Message](https://core.telegram.org/bots/api#message) | *Optional*. New incoming message of any kind - text, photo, sticker, etc. |
| edited_message | [Message](https://core.telegram.org/bots/api#message) | *Optional*. New version of a message that is known to the bot and was edited. This update may at times be triggered by changes to message fields that are either unavailable or not actively used by your bot. |
| channel_post | [Message](https://core.telegram.org/bots/api#message) | *Optional*. New incoming channel post of any kind - text, photo, sticker, etc. |
| edited_channel_post | [Message](https://core.telegram.org/bots/api#message) | *Optional*. New version of a channel post that is known to the bot and was edited. This update may at times be triggered by changes to message fields that are either unavailable or not actively used by your bot. |
| business_connection | [BusinessConnection](https://core.telegram.org/bots/api#businessconnection) | *Optional*. The bot was connected to or disconnected from a business account, or a user edited an existing connection with the bot |
| business_message | [Message](https://core.telegram.org/bots/api#message) | *Optional*. New message from a connected business account |
| edited_business_message | [Message](https://core.telegram.org/bots/api#message) | *Optional*. New version of a message from a connected business account |
| deleted_business_messages | [BusinessMessagesDeleted](https://core.telegram.org/bots/api#businessmessagesdeleted) | *Optional*. Messages were deleted from a connected business account |
| message_reaction | [MessageReactionUpdated](https://core.telegram.org/bots/api#messagereactionupdated) | *Optional*. A reaction to a message was changed by a user. The bot must be an administrator in the chat and must explicitly specify `"message_reaction"` in the list of *allowed_updates* to receive these updates. The update isn't received for reactions set by bots. |
| message_reaction_count | [MessageReactionCountUpdated](https://core.telegram.org/bots/api#messagereactioncountupdated) | *Optional*. Reactions to a message with anonymous reactions were changed. The bot must be an administrator in the chat and must explicitly specify `"message_reaction_count"` in the list of *allowed_updates* to receive these updates. The updates are grouped and can be sent with delay up to a few minutes. |
| inline_query | [InlineQuery](https://core.telegram.org/bots/api#inlinequery) | *Optional*. New incoming [inline](https://core.telegram.org/bots/api#inline-mode) query |
| chosen_inline_result | [ChosenInlineResult](https://core.telegram.org/bots/api#choseninlineresult) | *Optional*. The result of an [inline](https://core.telegram.org/bots/api#inline-mode) query that was chosen by a user and sent to their chat partner. Please see our documentation on the [feedback collecting](https://core.telegram.org/bots/inline#collecting-feedback) for details on how to enable these updates for your bot. |
| callback_query | [CallbackQuery](https://core.telegram.org/bots/api#callbackquery) | *Optional*. New incoming callback query |
| shipping_query | [ShippingQuery](https://core.telegram.org/bots/api#shippingquery) | *Optional*. New incoming shipping query. Only for invoices with flexible price |
| pre_checkout_query | [PreCheckoutQuery](https://core.telegram.org/bots/api#precheckoutquery) | *Optional*. New incoming pre-checkout query. Contains full information about checkout |
| purchased_paid_media | [PaidMediaPurchased](https://core.telegram.org/bots/api#paidmediapurchased) | *Optional*. A user purchased paid media with a non-empty payload sent by the bot in a non-channel chat |
| poll | [Poll](https://core.telegram.org/bots/api#poll) | *Optional*. New poll state. Bots receive only updates about manually stopped polls and polls, which are sent by the bot |
| poll_answer | [PollAnswer](https://core.telegram.org/bots/api#pollanswer) | *Optional*. A user changed their answer in a non-anonymous poll. Bots receive new votes only in polls that were sent by the bot itself. |
| my_chat_member | [ChatMemberUpdated](https://core.telegram.org/bots/api#chatmemberupdated) | *Optional*. The bot's chat member status was updated in a chat. For private chats, this update is received only when the bot is blocked or unblocked by the user. |
| chat_member | [ChatMemberUpdated](https://core.telegram.org/bots/api#chatmemberupdated) | *Optional*. A chat member's status was updated in a chat. The bot must be an administrator in the chat and must explicitly specify `"chat_member"` in the list of *allowed_updates* to receive these updates. |
| chat_join_request | [ChatJoinRequest](https://core.telegram.org/bots/api#chatjoinrequest) | *Optional*. A request to join the chat has been sent. The bot must have the *can_invite_users* administrator right in the chat to receive these updates. |
| chat_boost | [ChatBoostUpdated](https://core.telegram.org/bots/api#chatboostupdated) | *Optional*. A chat boost was added or changed. The bot must be an administrator in the chat to receive these updates. |
| removed_chat_boost | [ChatBoostRemoved](https://core.telegram.org/bots/api#chatboostremoved) | *Optional*. A boost was removed from a chat. The bot must be an administrator in the chat to receive these updates. |

### **getUpdates**

Use this method to receive incoming updates using long polling ([wiki](https://en.wikipedia.org/wiki/Push_technology#Long_polling)). Returns an Array of [Update](https://core.telegram.org/bots/api#update) objects.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| offset | Integer | Optional | Identifier of the first update to be returned. Must be greater by one than the highest among the identifiers of previously received updates. By default, updates starting with the earliest unconfirmed update are returned. An update is considered confirmed as soon as [getUpdates](https://core.telegram.org/bots/api#getupdates) is called with an *offset* higher than its *update_id*. The negative offset can be specified to retrieve updates starting from *-offset* update from the end of the updates queue. All previous updates will be forgotten. |
| limit | Integer | Optional | Limits the number of updates to be retrieved. Values between 1-100 are accepted. Defaults to 100. |
| timeout | Integer | Optional | Timeout in seconds for long polling. Defaults to 0, i.e. usual short polling. Should be positive, short polling should be used for testing purposes only. |
| allowed_updates | Array of String | Optional | A JSON-serialized list of the update types you want your bot to receive. For example, specify `["message", "edited_channel_post", "callback_query"]` to only receive updates of these types. See [Update](https://core.telegram.org/bots/api#update) for a complete list of available update types. Specify an empty list to receive all update types except *chat_member*, *message_reaction*, and *message_reaction_count* (default). If not specified, the previous setting will be used.Please note that this parameter doesn't affect updates created before the call to getUpdates, so unwanted updates may be received for a short period of time. |

> Notes
> 
> 
> **1.** This method will not work if an outgoing webhook is set up.
> 
> **2.** In order to avoid getting duplicate updates, recalculate *offset* after each server response.
> 

### **setWebhook**

Use this method to specify a URL and receive incoming updates via an outgoing webhook. Whenever there is an update for the bot, we will send an HTTPS POST request to the specified URL, containing a JSON-serialized [Update](https://core.telegram.org/bots/api#update). In case of an unsuccessful request (a request with response [HTTP status code](https://en.wikipedia.org/wiki/List_of_HTTP_status_codes) different from `2XY`), we will repeat the request and give up after a reasonable amount of attempts. Returns *True* on success.

If you'd like to make sure that the webhook was set by you, you can specify secret data in the parameter *secret_token*. If specified, the request will contain a header “X-Telegram-Bot-Api-Secret-Token” with the secret token as content.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| url | String | Yes | HTTPS URL to send updates to. Use an empty string to remove webhook integration |
| certificate | [InputFile](https://core.telegram.org/bots/api#inputfile) | Optional | Upload your public key certificate so that the root certificate in use can be checked. See our [self-signed guide](https://core.telegram.org/bots/self-signed) for details. |
| ip_address | String | Optional | The fixed IP address which will be used to send webhook requests instead of the IP address resolved through DNS |
| max_connections | Integer | Optional | The maximum allowed number of simultaneous HTTPS connections to the webhook for update delivery, 1-100. Defaults to *40*. Use lower values to limit the load on your bot's server, and higher values to increase your bot's throughput. |
| allowed_updates | Array of String | Optional | A JSON-serialized list of the update types you want your bot to receive. For example, specify `["message", "edited_channel_post", "callback_query"]` to only receive updates of these types. See [Update](https://core.telegram.org/bots/api#update) for a complete list of available update types. Specify an empty list to receive all update types except *chat_member*, *message_reaction*, and *message_reaction_count* (default). If not specified, the previous setting will be used.Please note that this parameter doesn't affect updates created before the call to the setWebhook, so unwanted updates may be received for a short period of time. |
| drop_pending_updates | Boolean | Optional | Pass *True* to drop all pending updates |
| secret_token | String | Optional | A secret token to be sent in a header “X-Telegram-Bot-Api-Secret-Token” in every webhook request, 1-256 characters. Only characters `A-Z`, `a-z`, `0-9`, `_` and `-` are allowed. The header is useful to ensure that the request comes from a webhook set by you. |

> Notes
> 
> 
> **1.** You will not be able to receive updates using [getUpdates](https://core.telegram.org/bots/api#getupdates) for as long as an outgoing webhook is set up.
> 
> **2.** To use a self-signed certificate, you need to upload your [public key certificate](https://core.telegram.org/bots/self-signed) using *certificate* parameter. Please upload as InputFile, sending a String will not work.
> 
> **3.** Ports currently supported *for webhooks*: **443, 80, 88, 8443**.
> 
> If you're having any trouble setting up webhooks, please check out this [amazing guide to webhooks](https://core.telegram.org/bots/webhooks).
> 

### **deleteWebhook**

Use this method to remove webhook integration if you decide to switch back to [getUpdates](https://core.telegram.org/bots/api#getupdates). Returns *True* on success.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| drop_pending_updates | Boolean | Optional | Pass *True* to drop all pending updates |

### **getWebhookInfo**

Use this method to get current webhook status. Requires no parameters. On success, returns a [WebhookInfo](https://core.telegram.org/bots/api#webhookinfo) object. If the bot is using [getUpdates](https://core.telegram.org/bots/api#getupdates), will return an object with the *url* field empty.

### **WebhookInfo**

Describes the current status of a webhook.

| Field | Type | Description |
| --- | --- | --- |
| url | String | Webhook URL, may be empty if webhook is not set up |
| has_custom_certificate | Boolean | *True*, if a custom certificate was provided for webhook certificate checks |
| pending_update_count | Integer | Number of updates awaiting delivery |
| ip_address | String | *Optional*. Currently used webhook IP address |
| last_error_date | Integer | *Optional*. Unix time for the most recent error that happened when trying to deliver an update via webhook |
| last_error_message | String | *Optional*. Error message in human-readable format for the most recent error that happened when trying to deliver an update via webhook |
| last_synchronization_error_date | Integer | *Optional*. Unix time of the most recent error that happened when trying to synchronize available updates with Telegram datacenters |
| max_connections | Integer | *Optional*. The maximum allowed number of simultaneous HTTPS connections to the webhook for update delivery |
| allowed_updates | Array of String | *Optional*. A list of update types the bot is subscribed to. Defaults to all update types except *chat_member* |

## **Updating messages**

The following methods allow you to change an existing message in the message history instead of sending a new one with a result of an action. This is most useful for messages with [inline keyboards](https://core.telegram.org/bots/features#inline-keyboards) using callback queries, but can also help reduce clutter in conversations with regular chat bots.

Please note, that it is currently only possible to edit messages without *reply_markup* or with [inline keyboards](https://core.telegram.org/bots/features#inline-keyboards).

ex: 

### **editMessageText**

Use this method to edit text and [game](https://core.telegram.org/bots/api#games) messages. On success, if the edited message is not an inline message, the edited [Message](https://core.telegram.org/bots/api#message) is returned, otherwise *True* is returned. Note that business messages that were not sent by the bot and do not contain an inline keyboard can only be edited within **48 hours** from the time they were sent.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| business_connection_id | String | Optional | Unique identifier of the business connection on behalf of which the message to be edited was sent |
| chat_id | Integer or String | Optional | Required if *inline_message_id* is not specified. Unique identifier for the target chat or username of the target channel (in the format `@channelusername`) |
| message_id | Integer | Optional | Required if *inline_message_id* is not specified. Identifier of the message to edit |
| inline_message_id | String | Optional | Required if *chat_id* and *message_id* are not specified. Identifier of the inline message |
| text | String | Yes | New text of the message, 1-4096 characters after entities parsing |
| parse_mode | String | Optional | Mode for parsing entities in the message text. See [formatting options](https://core.telegram.org/bots/api#formatting-options) for more details. |
| entities | Array of [MessageEntity](https://core.telegram.org/bots/api#messageentity) | Optional | A JSON-serialized list of special entities that appear in message text, which can be specified instead of *parse_mode* |
| link_preview_options | [LinkPreviewOptions](https://core.telegram.org/bots/api#linkpreviewoptions) | Optional | Link preview generation options for the message |
| reply_markup | [InlineKeyboardMarkup](https://core.telegram.org/bots/api#inlinekeyboardmarkup) | Optional | A JSON-serialized object for an [inline keyboard](https://core.telegram.org/bots/features#inline-keyboards). |

### (если тебе нужна инструкция к каким-то конкретным методам, дай знать)

### **Available methods**

> All methods in the Bot API are case-insensitive. We support GET and POST HTTP methods. Use either URL query string or application/json or application/x-www-form-urlencoded or multipart/form-data for passing parameters in Bot API requests.
> 
> 
> On successful call, a JSON-object containing the result will be returned.
> 

ex: 

### **sendMessage**

Use this method to send text messages. On success, the sent [Message](https://core.telegram.org/bots/api#message) is returned.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| business_connection_id | String | Optional | Unique identifier of the business connection on behalf of which the message will be sent |
| chat_id | Integer or String | Yes | Unique identifier for the target chat or username of the target channel (in the format `@channelusername`) |
| message_thread_id | Integer | Optional | Unique identifier for the target message thread (topic) of the forum; for forum supergroups only |
| direct_messages_topic_id | Integer | Optional | Identifier of the direct messages topic to which the message will be sent; required if the message is sent to a direct messages chat |
| text | String | Yes | Text of the message to be sent, 1-4096 characters after entities parsing |
| parse_mode | String | Optional | Mode for parsing entities in the message text. See [formatting options](https://core.telegram.org/bots/api#formatting-options) for more details. |
| entities | Array of [MessageEntity](https://core.telegram.org/bots/api#messageentity) | Optional | A JSON-serialized list of special entities that appear in message text, which can be specified instead of *parse_mode* |
| link_preview_options | [LinkPreviewOptions](https://core.telegram.org/bots/api#linkpreviewoptions) | Optional | Link preview generation options for the message |
| disable_notification | Boolean | Optional | Sends the message [silently](https://telegram.org/blog/channels-2-0#silent-messages). Users will receive a notification with no sound. |
| protect_content | Boolean | Optional | Protects the contents of the sent message from forwarding and saving |
| allow_paid_broadcast | Boolean | Optional | Pass *True* to allow up to 1000 messages per second, ignoring [broadcasting limits](https://core.telegram.org/bots/faq#how-can-i-message-all-of-my-bot-39s-subscribers-at-once) for a fee of 0.1 Telegram Stars per message. The relevant Stars will be withdrawn from the bot's balance |
| message_effect_id | String | Optional | Unique identifier of the message effect to be added to the message; for private chats only |
| suggested_post_parameters | [SuggestedPostParameters](https://core.telegram.org/bots/api#suggestedpostparameters) | Optional | A JSON-serialized object containing the parameters of the suggested post to send; for direct messages chats only. If the message is sent as a reply to another suggested post, then that suggested post is automatically declined. |
| reply_parameters | [ReplyParameters](https://core.telegram.org/bots/api#replyparameters) | Optional | Description of the message to reply to |
| reply_markup | [InlineKeyboardMarkup](https://core.telegram.org/bots/api#inlinekeyboardmarkup) or [ReplyKeyboardMarkup](https://core.telegram.org/bots/api#replykeyboardmarkup) or [ReplyKeyboardRemove](https://core.telegram.org/bots/api#replykeyboardremove) or [ForceReply](https://core.telegram.org/bots/api#forcereply) | Optional | Additional interface options. A JSON-serialized object for an [inline keyboard](https://core.telegram.org/bots/features#inline-keyboards), [custom reply keyboard](https://core.telegram.org/bots/features#keyboards), instructions to remove a reply keyboard or to force a reply from the user |

### (если тебе нужна инструкция к каким-то конкретным методам, дай знать)

### **Available types**

All types used in the Bot API responses are represented as JSON-objects.

It is safe to use 32-bit signed integers for storing all **Integer** fields unless otherwise noted.

> Optional fields may be not returned when irrelevant.
> 

ex: 

### **User**

This object represents a Telegram user or bot.

| Field | Type | Description |
| --- | --- | --- |
| id | Integer | Unique identifier for this user or bot. This number may have more than 32 significant bits and some programming languages may have difficulty/silent defects in interpreting it. But it has at most 52 significant bits, so a 64-bit integer or double-precision float type are safe for storing this identifier. |
| is_bot | Boolean | *True*, if this user is a bot |
| first_name | String | User's or bot's first name |
| last_name | String | *Optional*. User's or bot's last name |
| username | String | *Optional*. User's or bot's username |
| language_code | String | *Optional*. [IETF language tag](https://en.wikipedia.org/wiki/IETF_language_tag) of the user's language |
| is_premium | True | *Optional*. *True*, if this user is a Telegram Premium user |
| added_to_attachment_menu | True | *Optional*. *True*, if this user added the bot to the attachment menu |
| can_join_groups | Boolean | *Optional*. *True*, if the bot can be invited to groups. Returned only in [getMe](https://core.telegram.org/bots/api#getme). |
| can_read_all_group_messages | Boolean | *Optional*. *True*, if [privacy mode](https://core.telegram.org/bots/features#privacy-mode) is disabled for the bot. Returned only in [getMe](https://core.telegram.org/bots/api#getme). |
| supports_inline_queries | Boolean | *Optional*. *True*, if the bot supports inline queries. Returned only in [getMe](https://core.telegram.org/bots/api#getme). |
| can_connect_to_business | Boolean | *Optional*. *True*, if the bot can be connected to a Telegram Business account to receive its messages. Returned only in [getMe](https://core.telegram.org/bots/api#getme). |
| has_main_web_app | Boolean | *Optional*. *True*, if the bot has a main Web App. Returned only in [getMe](https://core.telegram.org/bots/api#getme). |

### (если тебе нужна инструкция к каким-то конкретным методам, дай знать)