# Glossary — Plain-Language Definitions

Every term used in this workshop, defined for people who do not write software. Use it as a reference during any beat.

---

## The four pieces

**Skill**
A folder with a `SKILL.md` inside it, describing a job you want done and how you want it done. Claude reads the first line of every Skill at the start of a session and loads the ones that match what you asked for. Write it once, and next quarter the work starts with the instructions already in place. This is what you take home today.

**Subagent**
A separate Claude session with its own memory, launched by the one you are talking to. It knows nothing about your conversation, which is exactly why it is useful: it is the only thing that can honestly tell you whether your instructions make sense to someone who was not there when you wrote them.

**MCP server (Model Context Protocol)**
An open standard for connecting an AI to something outside its folder. One server grants one capability, like reading a browser tab or querying a database. The point is that you choose what to grant. An agent with an MCP server for a browser has a browser, and nothing else.

**Plugin**
A bundle of Skills, commands and MCP servers, versioned and installable in one step. How a habit that works on your laptop becomes how your team works.

---

## How Claude Code behaves

**Agentic loop**
The cycle Claude Code runs every turn: read your context files, act through tools, show you what it did, wait for you. Not a chatbot that answers questions. It reads, acts, and pauses.

**CLAUDE.md**
A plain-text instruction file in your project folder. Claude reads it at the start of every turn, not just the first. Your conventions live here: how to group things, what to never assume, what to ask about. Think of it as the onboarding memo for a colleague who re-reads it constantly.

The practical consequence is the main lesson of the day. Correct Claude in conversation and the correction dies with the session. Write the same correction into `CLAUDE.md` and it holds forever.

**Plan Mode**
A mode where Claude can only read and plan. It cannot edit files or run commands, because those tools are switched off. Turn it on with **Shift + Tab** twice. Claude writes you a numbered plan, you push back on anything wrong, then you approve. Talk before touching anything.

**Auto-accept mode**
The opposite. Claude works through its plan without stopping after each step. You switch into it once you have approved a plan you actually read.

**Tool**
Something Claude Code can do: read a file, edit a file, run a command, search a folder. You see each call before it happens. In Plan Mode, edit and run are disabled.

**Context window**
How much text Claude can hold at once in a session. Working memory. When your files and conversation history fill it, the oldest parts fall out. This is why a short focused `CLAUDE.md` beats a long thorough one, and why a subagent starting fresh is genuinely a fresh start.

---

## Terms from the task

**Theme**
A group of tickets complaining about the same thing, whatever language they used. *"ما لقى العنوان"*, *"driver couldn't find building"* and *"الـ pin ودى الكابتن لحي ثاني"* are one theme, not three. Grouping by language would produce fake themes and hide a real one.

**Colloquial and fusha**
Fusha is formal written Arabic, the kind used in official complaints and news. Colloquial is how people actually type. The tickets contain both, because real queues contain both. The same customer might write نص ساعة casually and نصف ساعة when they are annoyed enough to be formal.

**Code-switching**
Using two languages in one sentence, usually an Arabic frame with English product words dropped in: *"الـ app يطفي كل ما افتحه"*. Extremely common in Riyadh and completely normal. It is not broken Arabic or broken English.

**Signal**
Something in the data that points at a cause rather than describing a symptom. A pile of complaints is symptoms. A pile of complaints that all start the week after a release is a signal.

---

## Terms from the tools

**Terminal**
The window where you type commands instead of clicking. On a Mac, press Cmd+Space and type "Terminal". On Windows, search for PowerShell. If you can open one and type `ls`, you are ready for today.

**Repository (repo)**
A folder of files tracked by git, usually shared online. Cloning one copies it to your machine.

**Markdown**
Plain text with light formatting marks: `#` for a heading, `**bold**`, `-` for a bullet. Every file you read and write today is markdown. It stays readable even without anything to render it.

**Diff**
The change Claude is proposing, shown as lines added and lines removed. Green is added, red is removed. Reading diffs is how you check work before it becomes permanent. You do not need to read every line, only look for anything that does not belong.

**Cold start**
Running something with no prior context. Your Skill working when you run it means little, because you remember what you meant. Your Skill working cold means it is actually written down.

---

*Something missing or still unclear? Tell the facilitator, and it goes in the next version.*

[← Back to home](index.html)
