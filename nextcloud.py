import requests
import xml.etree.ElementTree as ET
from datetime import datetime

from config import (
    NEXTCLOUD_URL,
    NEXTCLOUD_USER,
    NEXTCLOUD_PASS,
    UPLOAD_ROOT,
    FOLDER_FORMAT,
    TIMEOUT
)


class Nextcloud:

    def __init__(self):

        self.auth = (
            NEXTCLOUD_USER,
            NEXTCLOUD_PASS
        )

    # ==========================
    # WebDAV URL
    # ==========================

    def dav(self, path=""):

        return (
            f"{NEXTCLOUD_URL}"
            f"/remote.php/dav/files/"
            f"{NEXTCLOUD_USER}/"
            f"{path}"
        )

    # ==========================
    # Folder เดือน
    # ==========================

    def month_folder(self):

        return datetime.now().strftime(
            FOLDER_FORMAT
        )

    # ==========================
    # สร้าง Folder
    # ==========================

    def mkcol(self, path):

        r = requests.request(

            "MKCOL",

            self.dav(path),

            auth=self.auth,

            timeout=TIMEOUT

        )

        return r.status_code

    # ==========================
    # ตรวจ Folder
    # ==========================

    def ensure_folder(self):

        self.mkcol(UPLOAD_ROOT)

        self.mkcol(

            f"{UPLOAD_ROOT}/"

            f"{self.month_folder()}"

        )

    # ==========================
    # Upload
    # ==========================

    def upload(self, filename, filedata):

        self.ensure_folder()

        url = self.dav(
            f"{UPLOAD_ROOT}/"
            f"{self.month_folder()}/"
            f"{filename}"
        )

        r = requests.put(
            url,
            data=filedata,
            auth=self.auth,
            timeout=TIMEOUT
        )

        share = self.create_share_link(filename)

        return {
            "success": r.status_code in (200, 201, 204),
            "status": r.status_code,
            "message": r.text,
            "url": share,
            "filename": filename
        }

    # ==========================
    # URL ของไฟล์
    # ==========================

    def public_url(self, filename):

        return (
            f"{NEXTCLOUD_URL}/"
            f"{UPLOAD_ROOT}/"
            f"{self.month_folder()}/"
            f"{filename}"
        )
    



        # ==========================
    # Create Public Share Link
    # ==========================

    def create_share_link(self, filename):

        path = (
            f"{UPLOAD_ROOT}/"
            f"{self.month_folder()}/"
            f"{filename}"
        )

        url = (
            f"{NEXTCLOUD_URL}"
            "/ocs/v2.php/apps/files_sharing/api/v1/shares"
        )

        headers = {
            "OCS-APIRequest": "true"
        }

        data = {
            "path": path,
            "shareType": 3,
            "permissions": 1
        }

        r = requests.post(
            url,
            headers=headers,
            auth=self.auth,
            data=data,
            timeout=TIMEOUT
        )

        if r.status_code not in (200, 201):
            return None

        try:

            root = ET.fromstring(r.text)

            return root.find(
                ".//url"
            ).text

        except Exception:

            return None