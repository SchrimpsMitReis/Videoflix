import os
from unittest.mock import patch

from django.test import SimpleTestCase

from video_app.tasks import convert_single_hls_variant


class HlsConversionTests(SimpleTestCase):
    @patch("video_app.tasks.subprocess.run")
    def test_hls_variant_uses_browser_compatible_h264_format(self, run_mock):
        convert_single_hls_variant(
            source=os.path.join("media", "example.mp4"),
            output_root=os.path.join("media", "example_hls"),
            height=480,
        )

        command = run_mock.call_args.args[0]

        self.assertEqual(command[command.index("-pix_fmt") + 1], "yuv420p")
        self.assertEqual(command[command.index("-profile:v") + 1], "high")
