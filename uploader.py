from pathlib import Path

from logger import log
from nextcloud import Nextcloud


class Uploader:

    def __init__(self):
        self.nc = Nextcloud()

    def upload(self, file, filename=None):

        if file is None:
            return {
                "success": False,
                "message": "No file selected."
            }

        original_name = Path(file.filename).name

        if original_name == "":
            return {
                "success": False,
                "message": "Filename is empty."
            }

        if filename is None:
            filename = original_name

        try:

            filedata = file.read()

            result = self.nc.upload(
                filename,
                filedata
            )

            # เพิ่มข้อมูลไว้ให้ Frontend ใช้
            result["original_name"] = original_name
            result["stored_name"] = filename

            if result["success"]:

                log(f"UPLOAD SUCCESS : {filename}")

            else:

                log(
                    f"UPLOAD FAILED : {filename} "
                    f"({result['status']})"
                )

            return result

        except Exception as e:

            log(f"ERROR : {e}")

            return {
                "success": False,
                "message": str(e)
            }