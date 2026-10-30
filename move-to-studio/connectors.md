# Connectors: every service the person uses

Connecting a service needs the person to sign in to the vendor in their own browser.
The MCP tools get them there: you hand over a link, they approve, you confirm.
`list_connector_status` and `list_org_mcp_servers` show what is already connected.

## The three routes

Studio offers three ways to connect a service.
Use the first one that gives a normal sign-in; when one doesn't, move to the next.
Don't keep a list of services that "don't work": try the routes.

| Route | How | Who sets it up |
|---|---|---|
| A. Connectors | `get_connector_connect_url(toolkit)`, or Studio: Settings → **Connectors** → Connect | Each person, no admin needed |
| B. Org MCP servers | An admin registers the server once (`register_mcp_server`); each person then signs in from Studio: Settings → **MCP servers** → Connect | Admin once, then each person |
| C. Key form | Studio: the same Connect as A, when it asks for an API key, token or secret | The person types the key |

## Steps

1. Build the service list from the inventory: every MCP server `inventory.py` printed (follow its route column; it already skips local dev servers), every connector your session exposes, merged by service so Linear from three tools is one item. A server marked `key-in-url` carries a key in its address (shown as `<hidden>`): never register that address, because the org-wide list would share the key. Find the vendor's sign-in server instead, or leave it to the person.
   **No shell:** there is no `inventory.py` output. Use the services your own session exposes plus the names the person gave you; for a service with no URL, use the known hosted servers below. Never ask for a local config file: it can hold keys.
2. Drop what is already connected: `list_connector_status` for route A, and `list_org_mcp_servers` (its `your_connections` part) for route B. Anything marked `needs_reauth` or `not_connected` stays on the list. If `list_org_mcp_servers` says custom MCP servers are not enabled, route B isn't available in this organization: skip it and use A or C.
3. For each remaining service:
   - **Try A.** Find its toolkit slug with `list_connector_catalog(search=<service name>)`. Not in the catalog: skip to B. Call `get_connector_connect_url(toolkit)` and give the person the link to open; it shows the vendor's sign-in, then "Connected!". Never open or approve it for them. Then `list_connector_status(toolkit)` confirms it. If the vendor's page asks for an API key, token or service-account secret instead of a sign-in, stop and go to B.
   - **Try B.** If the service is already in `list_org_mcp_servers`, the person signs in from Studio: Settings → **MCP servers** → the server's row → Connect. If it isn't there and the person is an org admin who agrees:
     1. `probe_mcp_server(url)` with the URL `inventory.py` printed (already updated to the vendor's current endpoint) shows whether it wants a sign-in, nothing, or a key.
     2. `register_mcp_server(slug, name, url=<url>)`, or `command` + `args` for a keyless local server. Never pass headers, env values or key arguments from a local config: there is no field for them, by design.
     3. `validate_mcp_server(server_id)` boots it once and records its tools (about 20 seconds). For a server that needs a sign-in, the admin signs in to it in Studio first, then runs this again.
     Not an admin: note the service and its URL for an admin.
   - **Fall back to C.** Tell the person exactly which key the vendor wants and where in the vendor's settings they find it, and which Connect in Studio to paste it into.
4. Offer to open **Manage tools** on each connected service in Studio and set its read-only tools to Allow, so agents don't ask on every read.

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
- A vendor's error message sometimes shows only on its sign-in page, not in Studio. Ask the person what the page said.
- Each `get_connector_connect_url` call starts a fresh sign-in, so give the person the newest link only.
