# LineBot
Develop a LineBot to do something for me.

## Preparation work
- Having a Line account.
- Having a [Heroku](https://www.heroku.com) account.

### Build Heroku project
1. After login Heroku, click `New` -> `Create New App`.
2. Type in app name, and click `Create app` button.

### Build LineBot channel
1. Enter [Line Console](https://developers.line.me/console/).
2. Creat provider.
3. Type in provider name.
4. Click `create` button.
5. Click `Create Channel`.
6. Fill in Bot information.
7. Agree with the term, and click `create`.
8. Enter the Bot just created.
9. Open webhook.
10. Paste **Channel access token** and **Channel secret**.
11. In terminal: `git clone git@github.com:penguinwang96825/LineBot.git`.
12. Copy paste **Channel access token** and **Channel secret** into `app.py`.

### Upload app to Heroku
1. Download and install [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli).
2. Open terminal: 
```shell
heroku login
````
3. Initialise git: 
```shell
git config --global user.name "Your name"
git config --global user.email [Your email]
git init
```
4. Connect to Heroku
```shell
heroku git:remote -a {HEROKU_APP_NAME}
```
5. Push your code onto Heroku. (**Every time you update your code, please run these three lines of code.**)
```shell
git add .
git commit -m "Add code"
git push -f heroku master
```

### Connect Heroku and Line
1. Enter [Line Console](https://developers.line.me/console/) and choose your bot.
2. Type in url of Heroku in `webhook URL`.
```shell
https://{HEROKU_APP_NAME}.herokuapp.com/callback
```
3. Click `verify` button.

- Debug (Optional)
```shell
heroku login
heroku logs --tail --app {HEROKU_APP_NAME}
```

- File in folder
- `Procfile`：In Heroku, web: {language} {app_name}, so we name it **web: python app.py**。
- `requirements.txt`: You can install the packages you need.

## Line Messaging API Documentation
You can send the following types of messages. By defining actions, you can make these messages interactive.
Here is the official API [documentation](https://developers.line.biz/en/docs/messaging-api/message-types/#text-messages).
- Text message
- Sticker message
- Image message
- Video message
- Audio message
- Location message
- Imagemap message
- Template message
- Flex Message

### TextSendMessage （Text Message）
```python
message = TextSendMessage(text='Hello, world')
line_bot_api.reply_message(event.reply_token, message)
```

### ImageSendMessage（Image Message）
```python
message = ImageSendMessage(
    original_content_url='https://example.com/original.jpg',
    preview_image_url='https://example.com/preview.jpg'
)
line_bot_api.reply_message(event.reply_token, message)
```

### VideoSendMessage（Video Message）
```python
message = VideoSendMessage(
    original_content_url='https://example.com/original.mp4',
    preview_image_url='https://example.com/preview.jpg'
)
line_bot_api.reply_message(event.reply_token, message)
```

### AudioSendMessage（Audio Message）
```python
message = AudioSendMessage(
    original_content_url='https://example.com/original.m4a',
    duration=240000
)
line_bot_api.reply_message(event.reply_token, message)
```

### LocationSendMessage（Location Message）
```python
message = LocationSendMessage(
    title='my location',
    address='Tokyo',
    latitude=35.65910807942215,
    longitude=139.70372892916203
)
line_bot_api.reply_message(event.reply_token, message)
```

### StickerSendMessage（Sticker Message）
```python
message = StickerSendMessage(
    package_id='1',
    sticker_id='1'
)
line_bot_api.reply_message(event.reply_token, message)
```

### ImagemapSendMessage （Imagemap Message）
```python
message = ImagemapSendMessage(
    base_url='https://example.com/base',
    alt_text='this is an imagemap',
    base_size=BaseSize(height=1040, width=1040),
    actions=[
        URIImagemapAction(
            link_uri='https://example.com/',
            area=ImagemapArea(
                x=0, y=0, width=520, height=1040
            )
        ),
        MessageImagemapAction(
            text='hello',
            area=ImagemapArea(
                x=520, y=0, width=520, height=1040
            )
        )
    ]
)
line_bot_api.reply_message(event.reply_token, message)
```

### TemplateSendMessage - ButtonsTemplate （Buttons Interface Message）
```python
message = TemplateSendMessage(
    alt_text='Buttons template',
    template=ButtonsTemplate(
        thumbnail_image_url='https://example.com/image.jpg',
        title='Menu',
        text='Please select',
        actions=[
            PostbackTemplateAction(
                label='postback',
                text='postback text',
                data='action=buy&itemid=1'
            ),
            MessageTemplateAction(
                label='message',
                text='message text'
            ),
            URITemplateAction(
                label='uri',
                uri='http://example.com/'
            )
        ]
    )
)
line_bot_api.reply_message(event.reply_token, message)
```

### TemplateSendMessage - ConfirmTemplate（Confirm Interface Message）
```python
message = TemplateSendMessage(
    alt_text='Confirm template',
    template=ConfirmTemplate(
        text='Are you sure?',
        actions=[
            PostbackTemplateAction(
                label='postback',
                text='postback text',
                data='action=buy&itemid=1'
            ),
            MessageTemplateAction(
                label='message',
                text='message text'
            )
        ]
    )
)
line_bot_api.reply_message(event.reply_token, message)
```

### TemplateSendMessage - CarouselTemplate
![](https://i.imgur.com/982Glgo.png =250x)
```python
message = TemplateSendMessage(
    alt_text='Carousel template',
    template=CarouselTemplate(
        columns=[
            CarouselColumn(
                thumbnail_image_url='https://example.com/item1.jpg',
                title='this is menu1',
                text='description1',
                actions=[
                    PostbackTemplateAction(
                        label='postback1',
                        text='postback text1',
                        data='action=buy&itemid=1'
                    ),
                    MessageTemplateAction(
                        label='message1',
                        text='message text1'
                    ),
                    URITemplateAction(
                        label='uri1',
                        uri='http://example.com/1'
                    )
                ]
            ),
            CarouselColumn(
                thumbnail_image_url='https://example.com/item2.jpg',
                title='this is menu2',
                text='description2',
                actions=[
                    PostbackTemplateAction(
                        label='postback2',
                        text='postback text2',
                        data='action=buy&itemid=2'
                    ),
                    MessageTemplateAction(
                        label='message2',
                        text='message text2'
                    ),
                    URITemplateAction(
                        label='uri2',
                        uri='http://example.com/2'
                    )
                ]
            )
        ]
    )
)
line_bot_api.reply_message(event.reply_token, message)
```

### TemplateSendMessage - ImageCarouselTemplate
![](https://i.imgur.com/2ys1qqc.png =250x)
```python
message = TemplateSendMessage(
    alt_text='ImageCarousel template',
    template=ImageCarouselTemplate(
        columns=[
            ImageCarouselColumn(
                image_url='https://example.com/item1.jpg',
                action=PostbackTemplateAction(
                    label='postback1',
                    text='postback text1',
                    data='action=buy&itemid=1'
                )
            ),
            ImageCarouselColumn(
                image_url='https://example.com/item2.jpg',
                action=PostbackTemplateAction(
                    label='postback2',
                    text='postback text2',
                    data='action=buy&itemid=2'
                )
            )
        ]
    )
)
line_bot_api.reply_message(event.reply_token, message)
```
