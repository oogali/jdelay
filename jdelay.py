#!/usr/bin/env python

import os
import sys
import ConfigParser
import jira
import logging


class JDelay:
    def __init__(self, url=None, username=None, password=None):
        if url is None or username is None or password is None:
            raise Exception('Must provide JIRA server information')

        self.jira = jira.client.JIRA({'server': url}, basic_auth=(username, password))

    def process_spool(self, directory):
        for root, dirnames, filenames in os.walk(directory):
            # skip directory entry if it's our starting point
            if root == directory:
                continue

            project = os.path.basename(root).upper()
            filenames = map(lambda x: os.path.join(directory, project, x), filenames)

            logging.debug('{} --> {}'.format(project, filenames))
            for filename in filenames:
                logging.info('Processing {}'.format(filename))
                fd = open(filename, 'r')
                issue = fd.readlines()

                new_issue = {
                    'project': {'key': project},
                    'issuetype': {'name': issue[0].strip()},
                    'assignee': {'name': issue[1][1:].strip() if issue[1].startswith('@') else None},
                    'summary': issue[2].strip(),
                    'description': ''.join(issue[3:])
                }

                try:
                    self.jira.create_issue(fields=new_issue)
                except Exception as e:
                    logging.error('Could not create JIRA ticket')
                    logging.exception(e)
                    continue

                try:
                    os.remove(filename)
                except Exception as e:
                    logging.error('Could not remove queue file: {}'.format(filename))
                    logging.exception(e)
                    raise(e)


def main(argv=None):
    if argv is None:
        argv = sys.argv

    config = ConfigParser.SafeConfigParser()
    config.read(os.path.expanduser('~/.jqueue'))

    try:
        url = config.get('jira', 'server')
        username = config.get('jira', 'username')
        password = config.get('jira', 'password')
    except Exception as e:
        logging.error('Could not read JIRA settings from configuration file, please check the [jira] section')
        logging.exception(e)
        return -1

    j = JDelay(url=url, username=username, password=password)
    j.process_spool('/Users/oogali/jqueue')

    return 0

if __name__ == '__main__':
    sys.exit(main())
