# Backlog

The AI Agent Team's queue. Primary store: GitHub Issues at
[`kellmat74/agent-backlog`](https://github.com/kellmat74/agent-backlog).
This local `tickets/` dir is a fallback for issues that need to live offline or
contain pointers/specs too long for an issue body.

## Routing labels (which agent picks it up)
- `agent:claude` - synchronous, IDE-bound, needs Matt watching or eager iteration
- `agent:hermes` - async, long-running, scheduled, channel-driven
- `agent:any` - either can claim

## Status labels
- `status:ready` - claimable
- `status:in-progress` - claimed by an agent
- `status:blocked` - needs Matt or external input
- `status:needs-review` - work done, awaiting Matt's review

## Priority
- `priority:p0` - drop other things
- `priority:p1` - this week
- `priority:p2` - whenever there's slack

## Claim protocol
1. Agent lists open issues matching `agent:<self>` or `agent:any` with `status:ready`,
   ordered by priority then created date.
2. Atomic claim: remove `status:ready`, add `status:in-progress`. Post a comment:
   `Claimed by <agent> at <ISO timestamp>.` If the label swap fails because another
   agent beat you to it, drop the ticket and pick another.
3. Work. Post comments for substantial progress, not chatter.
4. Done: close issue with summary comment. Or `status:needs-review` if Matt should look.
5. Stuck: `status:blocked`, comment what's blocking, move on.

## Filing new tickets
Use the issue template (`.github/ISSUE_TEMPLATE/ticket.md` in the agent-backlog repo).
Required: context, acceptance criteria. Optional: constraints, working notes.
