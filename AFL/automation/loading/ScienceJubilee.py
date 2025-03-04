"""
Interface to get state for science jubilee platform to coordinate loading activities
"""

from AFL.automation.APIServer.Driver import Driver
import requests
from requests.adapters import HTTPAdapter, Retry
import json
import logging
import time

logger = logging.getLogger(__name__)

class ScienceJubilee(Driver):

    def __init__(self, address, safe_position):
        self.address = address
        self.safe_position = safe_position
        #self.connect()
        
        requests_session = requests.Session()
        retries = Retry(
            total=5, backoff_factor=0.1, status_forcelist=[500, 502, 503, 504]
        )

        requests_session.mount("http://", HTTPAdapter(max_retries=retries))
        requests_session.headers["Connection"] = "close"
        self.session = requests_session


    def get_safety_state(self):
        """
        Returns the safety state of the machine.
        """
        positions = self.position()
        print('Jubilee position: ', positions)
        x, y, z = positions[0], positions[1], positions[2]
        
        # Check if position is within safe bounds
        if x > self.safe_position[0]:
            return False
            
        if y < self.safe_position[1]:
            return False
            
        if z < self.safe_position[2]:
            return False

        return True


    def position(self):
        """Returns the current machine control point in mm.

        :return: A dictionary of the machine control point in mm. The keys are the axis name, e.g. 'X'
        :rtype: dict
        """
        # Axes are ordered X, Y, Z, U, E, E0, E1, ... En, where E is a copy of E0.
        response_chunks = self.gcode("M114").split()
        positions = [float(a.split(":")[1]) for a in response_chunks[:3]]
        return positions


    def gcode(self, cmd: str = "", timeout=None, response_wait: float = 60):
        """Send a G-Code command to the Machine and return the response.

        :param cmd: The G-Code command to send, defaults to ""
        :type cmd: str, optional
        :param timeout: The time to wait for a response from the machine, defaults to None
        :type timeout: float, optional
        :param response_wait: The time to wait for a response from the machine, defaults to 30
        :type response_wait: float, optional

        :return: The response message from the machine. If too long, the message might not display in the terminal.
        :rtype: str
        """

        try:
            # Try sending the command with requests.post
            response = requests.post(
                f"http://{self.address}/machine/code", data=f"{cmd}", timeout=timeout
            ).text
            if "rejected" in response:
                raise requests.RequestException
        except requests.RequestException:
            # If requests.post fails ( not supported for standalone mode), try sending the command with requests.get
            try:

                # Paraphrased from Duet HTTP-requests page:
                # Client should query `rr_model?key=seqs` and monitor `seqs.reply`. If incremented, the command went through
                # and the response is available at `rr_reply`.
                reply_response = self.session.get(
                    f"http://{self.address}/rr_model?key=seqs"
                )
                logging.debug(
                    f"MODEL response, status: {reply_response.status_code}, headers:{reply_response.headers}, content:{reply_response.content}"
                )

                reply_count = reply_response.json()["result"]["reply"]
                buffer_response = self.session.get(
                    f"http://{self.address}/rr_gcode?gcode={cmd}", timeout=timeout
                )
                logging.debug(
                    f"GCODE response, status: {buffer_response.status_code}, headers:{buffer_response.headers}, content:{buffer_response.content}"
                )
                # wait for a response code to be appended
                # TODO: Implement retry backoff for managing long-running operations to avoid too many requests error. Right now this is handled by the generic exception catch then sleep. Real fix is some sort of backoff for things running longer than a few seconds.
                tic = time.time()
                try_count = 0
                while True:
                    try:
                        new_reply_response = self.session.get(
                            f"http://{self.address}/rr_model?key=seqs"
                        )

                        logger.debug(
                            f"MODEL response, status: {new_reply_response.status_code}, headers:{new_reply_response.headers}, content:{new_reply_response.content}"
                        )
                        new_reply_count = new_reply_response.json()["result"]["reply"]

                        if new_reply_count != reply_count:
                            response = self.session.get(
                                f"http://{self.address}/rr_reply"
                            )

                            logger.debug(
                                f"REPLY response, status: {response.status_code}, headers:{response.headers}, content:{response.content}"
                            )

                            response = response.text
                            break
                        elif time.time() - tic > response_wait:
                            response = None
                            break
                        time.sleep(self.delay_time(try_count))
                        try_count += 1
                    except Exception as e:
                        print(f"Connection error ({e}), sleeping 1 second")
                        logging.debug(f"Error in gcode reply wait loop: {e}")
                        time.sleep(2)
                        continue

            except requests.RequestException as e:
                print(f"Both `requests.post` and `requests.get` requests failed: {e}")
                response = None
        # TODO: handle this with logging. Also fix so all output goes to logs
        return response


    def connect(self):
        """Connects to Jubilee over http.

        :raises MachineStateError: If the connection to the machine is unsuccessful.
        """
        try:
            # "Ping" the machine by updating the only cacheable information we care about.
            # TODO: This should handle a response from self.gcode of 'None' gracefully.
            max_tries = 50
            for i in range(max_tries):
                response = json.loads(self.gcode('M409 K"move.axes[].homed"'))[
                    "result"
                ][:4]
                if len(response) == 0:
                    continue
                else:
                    break
            # These data members are tied to @properties of the same name

        except json.decoder.JSONDecodeError as e:
            raise MachineStateError("DCS not ready to connect.") from e
        except requests.exceptions.Timeout as e:
            raise MachineStateError(
                "Connection timed out. URL may be invalid, or machine may not be connected to the network."
            ) from e

    def delay_time(self, n):
        """
        Calculate delay time for next request. dumb hard code for now, could be fancy exponential backoff
        """
        if n == 0:
            return 0
        if n < 10:
            return 0.1
        if n < 20:
            return 0.2
        if n < 30:
            return 0.3
        else:
            return 1
