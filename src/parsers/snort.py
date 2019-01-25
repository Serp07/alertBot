import re
import logging
from src import SendNotification

logger = logging.getLogger("alertBot.snort")


class Snort:
    """ Using class BC patterns should only be compiled once..
        And all snort parsers and patterns can be found at one place
    """
    def __init__(self):
        self.pattern = re.compile(
            r"(?P<time>\d+\/\d+\/\d+-\d+:\d+:\d+\.\d+)\s,"  # time
            r"(?P<gid>\d+),"                                # Signature GID
            r"(?P<sid>\d+),"                                # Signature SID
            r"(?P<rev>\d+),"                                # Revision - ??
            r"\"(?P<name>.*?)\","                           # Alert name
            r"(?P<proto>TCP|UDP|ICMP|.?),"                  # Protocol
            r"(?P<src>\d+\.\d+\.\d+\.\d+),"                 # Src IP
            r"(?P<src_port>\d+|.?),"                        # Src port
            r"(?P<dst>\d+\.\d+\.\d+\.\d+),"                 # Dst IP
            r"(?P<dst_port>\d+|.?),"                        # Dst port
            r"\d+,"                                         # Unknown stuff
            r"(?P<class>[a-zA-Z0-9-_ ]+),"                  # Alert class
            r"(?P<pri>\d+)"                                 # Priority
        )

    def snortParserV2(self, line: str) -> dict:
        # Parse snort version 2 alerts/logs

        try:
            match = self.pattern.match(line)
            if not match:
                # Send notification when nothing matches..
                logger.error(f"No match for line. This should not happen!")
                logger.error(line)
                SendNotification().send_notification(
                    message="No match for line. This should not happen..\n{}".format(line),
                    title="Snort parser error"
                )
                return {}
                #exit(1)

            return match.groupdict()

        except re.error as rexerror:
            logger.error(rexerror)
            exit(1)

    def snortParserV3(self, line):
        # Parse snort version 3 alerts/logs
        pass