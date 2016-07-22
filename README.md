# slackbridging

Scripts for bridging Slack and Slack and Slack and XMPP. Lua module connects to prosody and the python script runs as a CGI somewhere to be a destination for outgoing webhooks either from Prosody or Slack.

Config on the Prosody server:

Component "conference.example.com" "muc"
        outgoing_webhook_routing = {
                ["slackchannel2"] = "http://mywebserver/cgi-bin/slackbridge.py",
        }
        incoming_webhook_path = "/webhook" -- Change this for security by obscurity

        modules_enabled = {
                "slack_webhooks";
        }


