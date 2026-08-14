# Beat 6 — Scale It

**Duration:** 10 minutes

**Goal:** Watch two demos. Understand where the agent's reach comes from, and how a Skill leaves your laptop.

<!-- participant-start -->
## Watch this one

Nothing to type. Ten minutes, front of the room.

## Reaching outside the folder

Your report says complaints spiked after the address-picker release. A reasonable next question: is that a known problem with the mapping library the app moved to?

Claude cannot answer that. It is not in your folder, and everything today has come out of your folder.

So it gets given exactly one thing: a browser.

The facilitator connects the **Chrome DevTools MCP server**, and you watch a tab open and run a search on the projector.

Now look at what it was handed. A browser tab. Not your files, not your mail, not your machine. It needed to reach one place, so it was given one place.

**That is the decision worth taking home.** There are agents that want your whole desktop. You can give an agent exactly the reach a task needs instead, and you should. MCP servers are how you do that: one server, one capability, scoped on purpose.

## Handing the Skill to someone else

Right now your Skill lives in `.claude/skills/` on your laptop. Useful to you, invisible to everyone else.

A **plugin** is a versioned bundle: Skills, commands, hooks, MCP servers, packaged together and installed with one command. Your teammate runs `/plugin`, and now they analyse tickets the way you do.

That is how a personal habit becomes how a team works.

## The four pieces

You have now met all of them. They are easy to confuse, and the difference is simple:

| Piece | What it is |
|---|---|
| **Skill** | Something you want the agent to know how to do |
| **Subagent** | Something you delegate to a clean context |
| **MCP server** | A specific capability you choose to grant |
| **Plugin** | Those bundled, so somebody else installs them in one command |

Nobody wrote a framework today. You composed four existing pieces, and tested the result by asking for an isolated run.

> **Building harnesses without building them.** That is the whole idea.
<!-- participant-end -->

## Facilitator

Ten minutes, demo only. Do not let anyone install anything, that is a twenty-minute detour.

### Setup before the session

Have the Chrome DevTools MCP server connected and tested. Have a browser tab ready to be opened. Practise once, because a demo that fails here undercuts the argument you are making about scoped access.

### Running the MCP demo

The setup comes out of their own work, which is what makes it land. Say roughly:

> *"Your report says complaints spiked after v4.2. Is that a known issue with the map library? Claude cannot know. It is not in the folder."*

Then connect it, run the search, and let the tab open where they can see it.

Then the line the whole demo exists for:

> *"Look at what it just got. A browser tab. Not my files, not my mail, not my machine. It needed to reach one place, so I gave it one place."*

Pause there. Do not rush into plugins.

**If someone asks about desktop agents that do everything:** answer straight. They exist, they are convenient, and the trade is that you stop being able to say what the agent can touch. You are not banning anything, you are pointing at a choice most people make without noticing.

### Plugins

Two minutes. Show `/plugin` and the idea of a bundle. Do not demo an install unless you have one ready and tested.

The point is only that the Skill they built this morning can leave their laptop.

### Closing this beat

The four-way summary is the day's argument compressed. Say it slowly, then stop:

> *"Skill, subagent, MCP, plugin. Nobody wrote a framework today. You composed four things that were already there, and you tested it by asking for a clean run."*

[← Back to home](index.html)
