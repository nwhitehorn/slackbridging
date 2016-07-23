# slackbridging

Scripts for bridging Slack and Slack and Slack and XMPP. Lua module connects to prosody and the python script runs as a CGI somewhere to be a destination for outgoing webhooks either from Prosody or Slack.

## The Prosody module: enabling web hooks

The prosody module (mod_slack_webhooks.lua) enables Slack-compatible incoming and outgoing webhooks for a Prosody-hosted XMPP MUC room. This allows the use of any Slack integration script with an XMPP MUC.

Incoming webhooks are at http://conference.example.com/webhook/roomname (to post to roomname@conference.sptwiki.com). Changing "webhook" to something else obscure (random characters) is likely useful for preventing spam. This is set by the incoming_webhook_path option. This accepts incoming requests in the same format as Slack and respects the username and text fields.

Outgoing webhooks are optional and copy messages from one or more MUC rooms to an external web hook. Data matches Slack's outgoing webhooks, though with fewer fields (channel_name, text, team_domain, and user_name are included.)

Config on the Prosody server:

```lua
Component "conference.example.com" "muc"
        outgoing_webhook_routing = {
                ["slackchannel2"] = "http://mywebserver/cgi-bin/slackbridge.py",
        }
        incoming_webhook_path = "/webhook" -- Change this for security by obscurity

        modules_enabled = {
                "slack_webhooks";
        }
```

## The reflector python script

This is a hacked-together CGI script that receives outgoing Slack-style webhook messages, munges them slightly, and forwards them to the incoming webhook on another channel. Notably, it preserves both the user name and body test.

This can be used to add an approximation of XMPP server-to-server federation to Slack. By binding the outgoing webhook of one channel to the incoming hook of another, hosted in a different domain, and then binding the reverse direction hooks as well, all messages from one chat will show up, properly attributed, in the other. This creates a reasonably high-quality illusion of a shared inter-domain Slack chat.

By using the Prosody module described above, one of these "Slack chats" can be a Prosody-hosted XMPP MUC, which lets Slack users participate in an open XMPP MUC room as (apparently) native inhabitants (and vice-versa for the XMPP users in the Slack chat).
