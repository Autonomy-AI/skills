# Connectors: every service the person uses

Connecting a service needs the person to sign in to the vendor in a browser, so this part runs in Studio's web UI.
The MCP tools only read state here: `list_connector_status` tells you what is already connected.

## The three routes

Studio offers three ways to connect a service.
Use the first one that gives a normal sign-in; when one doesn't, move to the next.
Don't keep a list of services that "don't work": try the routes.

| Route | Where in Studio | Who sets it up |
|---|---|---|
| A. Connectors | Settings → **Connectors** → All connectors → search → Connect | Each person, no admin needed |
| B. MCP servers | Settings → **MCP servers** → the server's row → Connect | An org admin adds the server once; then each person connects |
| C. Key form | The same Connect as A, when it asks for an API key, token or secret | The person types the key |

## Steps

1. Build the service list from the inventory: every MCP server `inventory.py` printed (follow its route column; it already skips local dev servers), every connector your session exposes, merged by service so Linear from three tools is one item. A server marked `key-in-url` carries a key in its address (shown as `<hidden>`): never add that address to Studio, because the org-wide list would share the key. Find the vendor's sign-in server instead, or leave it to the person.
2. Drop what `list_connector_status` already shows as connected. Anything it marks `needs_reauth` stays on the list.
3. Open Studio at Settings → **Connectors** and Settings → **MCP servers**, and read both lists. Anything already connected is done.
4. For each remaining service:
   - **Try A.** Search the catalog and click Connect. A vendor sign-in page: handle the approval per the Rules in SKILL.md. The sign-in tab closes by itself when it worked; confirm the service now shows as connected. A page that asks for an API key, token or service-account secret: don't fill it, go to B.
   - **Try B.** If the service has a row under MCP servers: Connect, approve, wait for the tab to close. If the row then says it needs validation, click Validate and wait about 20 seconds while Studio lists the server's tools. If there is no row, an org admin can add one with one line of JSON: `{"url": "<url>"}` for a hosted server, or `{"command": "npx", "args": ["-y", "<package>"]}` for a keyless local one. Use the URL `inventory.py` printed; it is already updated to the vendor's current endpoint. Do this only if the person is an admin and agrees; otherwise note it for an admin. Never copy headers, env values or key arguments from a local config into Studio.
   - **Fall back to C.** Leave the key form open for the person, and tell them exactly which key it wants and where in the vendor's settings they find it.
5. Offer to open **Manage tools** on each connected service and set its read-only tools to Allow, so agents don't ask on every read.

## Known hosted MCP servers

For a service with no URL in any local config:

- Linear: `https://mcp.linear.app/mcp`
- Notion: `https://mcp.notion.com/mcp`
- LaunchDarkly: `https://mcp.launchdarkly.com/mcp/launchdarkly`
- Datadog: `https://mcp.datadoghq.com/v1/mcp`
- Mixpanel: `https://mcp.mixpanel.com/mcp` (the Mixpanel org needs MCP access turned on)
- Logfire: `https://logfire-us.pydantic.dev/mcp` (EU region: `https://logfire-eu.pydantic.dev/mcp`)

## What to expect

- Some vendors ask for a key on route A but offer a normal sign-in on their own MCP server (route B). LaunchDarkly, Datadog and Mixpanel work this way.
- Some vendors refuse Studio on route B; Studio then shows "Could not start connection". Retrying won't help. Note the vendor's words and use route A or C. Figma, for example, connects through route A.
- A vendor's error message sometimes shows only in the sign-in tab, not in Studio. Read the tab before it closes.
- The sign-in sometimes opens in a separate window. If you can't see it, ask the person to finish it there.
