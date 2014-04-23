# jDelay

**Command-line JIRA queue processor**

## Overview

jDelay will walk a given spool directory that contains directories named after the JIRA projects, and the files within those directories that contain the tickets you want to create.

### Example

For example, if you've been finding problems and you want to ticket them up in the ``DEV`` and ``OPS`` projects, your spool directory should look like so.

    spool/
    spool/DEV/
    spool/DEV/annoying-problem-1
    spool/DEV/annoying-problem-2
    spool/OPS/
    spool/OPS/another-annoying-problem
    spool/OPS/random-freeform-text

jDelay will parse the content of ``DEV/annoying-problem-1`` and use the data it finds to create a ticket in the ``DEV`` project.

### Format of Ticket File

The ticket file is a plain text file -- the first three lines are treated specially, and the rest of the file will set the description of the ticket.

    Task
    @assignee
    Summary of This Issue
    Multi-line description of this issue.

This will create a new issue in JIRA with a type of 'Task', assigned to 'assignee', a summary of 'Summary of This Issue', and the rest of the file will be set as the issue description.