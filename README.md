# Moderator skill for Codex

Working rules and small Python helpers for a task overview: human actions first, followed by project cards with status indicators, expandable details and verified work-chat links. Version: 8 October 2026.

This repository contains the complete original skill. Core rules, programs, tests and UI metadata are unchanged from the version used by Hendrik. This guide is in English; the original rules and reference documents are in German. Only the activation guide was adapted for this standalone package, which needs no access to Hendrik's private setup. The rules still use the name Hendrik. You can replace it with your own name in the text files.

## Install on macOS or Linux

Clone this repository to a permanent local folder, then run the installer with Python 3:

```bash
git clone https://github.com/hendrikgrueger-web/codex-moderator.git
cd codex-moderator
python3 moderator/scripts/install.py
python3 moderator/scripts/install.py --check
```

Or use GitHub's **Code → Download ZIP**, extract it to a permanent folder and run the two Python commands from that folder. Keep the source folder in place: the installer links to it.

Expected: `LINK_CREATED`, followed by `FILES_VERIFIED`. If the correct link already exists, the first command also returns `FILES_VERIFIED`. The link is created at `~/.agents/skills/moderator`. An unrelated existing installation will not be overwritten. The installer does not change Codex configuration or start a service.

User-level skill discovery and linked skill folders are described in the [official documentation](https://learn.chatgpt.com/docs/build-skills). Check that your own environment recognises the skill after installation.

In a new Codex chat, select the skill or write:

```text
$moderator Reply in English. Show only the actions that need me now,
then the verified status of the projects you can actually access.
```

`$moderator` explicitly selects the skill. The package does not register a native `/moderator` command. If it isn't recognised, open a new chat or restart Codex and check the skill list.

Inline cards require the visualize skill in your environment. It is not included in this repository. Without inline support, the Moderator should state the limitation and use a text view. An identical layout across all clients is not guaranteed.

The original German view triggers are `nur ich` (only my actions), `status`, `delta`, `blockiert` (blocked), `ohne mich` (work agents can do), `Baum` (tree) and `Text`. You can include these in an English request. “Ohne mich” means executable agent work; it does not claim that work is already running.

## Check and remove

```bash
python3 -m unittest discover -s moderator/tests -v
python3 moderator/scripts/install.py --remove
```

`--remove` removes only the matching link created by the installer. Source files remain in place. This package has not been tested on a Windows device. If symlink permissions are missing, the installer exits; it does not request administrator access automatically.

## What the package does

The Python checker validates normalised task data, counts tasks and ties reply numbers to a snapshot. It does not discover tasks, generate model responses or grant permission to act. Examples and command syntax are in `moderator/references/snapshot.md`.

Account access, access to other chats, autonomy and scheduling come from your Codex environment and your instructions. The skill does not set them up. A recurring overview is therefore not part of the installation.

The tests check program logic and package structure. They do not replace an actual model run against the counterexamples in `moderator/references/evaluation.md`.
