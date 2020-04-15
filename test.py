import unittest
import json

# test baidu.py
from ocs.baidu import fetch_token, get_validate_code
from urllib.parse import urlencode, quote_plus


class TestBaidu(unittest.TestCase):
    def test_image2text(self):
        """
        Test that it can sum a list of integers
        """
        image = '/9j/4AAQSkZJRgABAgAAAQABAAD/2wBDAAgGBgcGBQgHBwcJCQgKDBQNDAsLDBkSEw8UHRofHh0aHBwgJC4nICIsIxwcKDcpLDAxNDQ0Hyc5PTgyPC4zNDL/2wBDAQkJCQwLDBgNDRgyIRwhMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjL/wAARCAAWAEIDASIAAhEBAxEB/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUFBAQAAAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/8QAHwEAAwEBAQEBAQEBAQAAAAAAAAECAwQFBgcICQoL/8QAtREAAgECBAQDBAcFBAQAAQJ3AAECAxEEBSExBhJBUQdhcRMiMoEIFEKRobHBCSMzUvAVYnLRChYkNOEl8RcYGRomJygpKjU2Nzg5OkNERUZHSElKU1RVVldYWVpjZGVmZ2hpanN0dXZ3eHl6goOEhYaHiImKkpOUlZaXmJmaoqOkpaanqKmqsrO0tba3uLm6wsPExcbHyMnK0tPU1dbX2Nna4uPk5ebn6Onq8vP09fb3+Pn6/9oADAMBAAIRAxEAPwDrfD/h/wAJt4A0O5uPDmjs39l281xcPYRs7HylLEnbknqSepp8Ok+A5bB78aHo/wBkicJJJ/ZqcHjtsz3HatDwZ/yI3h//ALBtt/6KWsqV5rOO68OQAqJrhY4G25KwyZZsKeWC4YE579RiohJ3ua15uhFWtZp9Lvmtp16mnc6X8P4dFGqjw9ojWjZCMNNjDSMCRtUFQc5B/n05pmm6N4K1K4a1/wCEQ0+1ulQyeRdaTGjFMgbh8uMZOOvY1q6lpQ1DSLe0spfss9myS2pPzKGQYUHOcjH+T0OHHdajd+NtPW8nsp5LOOVpEsz8kQIK8knO7OAVxwAPU45Z1aiqJLZ2X37/AHHG41VJRluO1a2+G+gXiWup6JokMzxiQJ/ZStlSSM5VCOoNXNL0j4ea1ps1/ZaFoT2kLMssr6bHGEIAJzuQcAEHPSq3xEdn8EaiWP8Azz/9GrW3qk8UGhak1xD58AtZTJFvK7xsOVyOmRxmvUeHXIn1PRnhlChzq/N66aW8jkopvh3NLCW8H21vZTSmGLUJtIiW2Y5IHzEdDg9Rx3xg46d/A3hVMZ8M6Kc/9OEX/wATXA3VtqVv8PNMvb7Xo73ShJEzaYDs8xN3+rEo+Ykd1/h2nH3BXrs7ZfHpWeKpQgk4ea+45MLUlN2kfFfi+CK28a69b28SRQxajcJHHGoVUUSMAABwAB2oqTxt/wAj74i/7Cdz/wCjWorNbFPc9b8P/Gvw3pXhvS9OnstVaa0tIoJGSKMqWVApIzIOMip5PjT4Mk1GK/fS9YN1EuxH8uPgc9vNx3NFFZ2OpvmST1E1D40eC9UgWC80rWJY1beB5aLzgjtKPU0th8afBOmRGOz0fVYVPUiGIluvUmTJ6nrRRVUoRVTmS1C+vN1KWq/FP4e63dLc6joeszTKgjDYVcKCTjCyjuTVrSvjH4H0S1a207SNZhhZzIV2I2WIAzlpT2Aoors9pK1rlutUa5b6Fez+J/wzs79L+Lw5qq3SOZFYRoVVvUKZdox2444xW837QXhMnP8AZ+tf9+Yv/jlFFc1WTm/edzhilCp7uh8/+ItQi1bxNqupW6usN3eTTxrIAGCu5YA4JGcH1ooooQ3uf//Z'
        r = get_validate_code(image)

        self.assertEqual(r, "v9I8")


if __name__ == '__main__':
    unittest.main()
