from utils.AllUtils import *

class StreamerInfo():

    def load_streamer_data(self) -> Dict:
        self.streamer_raw_data = yaml_utils.load("configurations/streamer_info.yaml")
        self.process_streamer_data()

    def process_streamer_data(self) -> Dict:
        self.streamer_data = DotMap(self.streamer_raw_data)

    def __init__(self) -> None:
        self.load_streamer_data()
        self.name = self.streamer_data.get("streamer_name")
        self.platform = self.streamer_data.get("platform")
        self.channel = self.streamer_data.get("stream_channel")
        self.link = self.streamer_data.get("stream_link")
        self.discord = self.streamer_data.get("discord_link")