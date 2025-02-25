#!/opt/homebrew/bin/python3.11
# -*- coding: utf-8 -*-
import subprocess, re, logging, os, time
from raindropio import API, Raindrop, CollectionRef, Collection
# Configue logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler("mega.log"),
        logging.StreamHandler()
    ]
)

class MegaCMD:
    def __init__(self):
        pass

    def check(self, url):
        result, output = self.run("import", url)
        time.sleep(1)
        
        if result:
            df_result, df_output = self.run("df")
            self.run("rm", output)
            time.sleep(1)
            if df_result:
                return df_output['size'] > 100
            else:
                logging.error(f"Error getting df: {df_output}")
                return None
        else:
            logging.error(f"Error importing URL: {output}")
            return False

    def run(self, command, arugment=""):
        """
        Run a shell command and return its output.
        """
        if command == "df":
            output = subprocess.run("mega-df", shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            cloud_drive_pattern = r"Cloud drive:\s+(?P<size>\d+)(.*)?\s+in\s+(?P<files>\d+)\s+file\(s\) and\s+(?P<folders>\d+)\s+folder\(s\)"
            match = re.search(cloud_drive_pattern, output.stdout.strip())
            if match:
                data = match.groupdict()
                data["size"] = int(data["size"])
                data["files"] = int(data["files"])
                data["folders"] = int(data["folders"])
                logging.debug(f"Parsed data: {data}")
                return True, data
            else:
                logging.error("Could not parse `mega-df` output. No match found.")
                logging.error(f"Output was:\n{output}")
                return False, output

        if command == "import" and arugment.startswith("https://mega.nz/"):
            try:
                output = subprocess.run(f'mega-import {arugment}', shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                # check the exit code of the command
                if output.returncode == 0:
                    path = output.stdout.replace("Imported folder complete: ", "", 1).strip()
                    logging.debug(f"Imported path: {path}")
                    return True, path
                else:
                    logging.error(f"Command failed with exit code {output.returncode}")
                    logging.debug(f"Error output:\n{output.stderr}")
                    return False, output
            except subprocess.CalledProcessError as e:
                logging.error(f"Command '{e.cmd}' returned non-zero exit status {e.returncode}.")
                logging.debug(f"Error output:\n{e.stderr}")
                return False, e

        if command == "rm" and arugment.startswith("/"):
            try:
                output = subprocess.run(["mega-rm", "-rf", arugment], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                if output.returncode == 0:
                    logging.debug(f"Removed path: {arugment}")
                    return True, 0
                else:
                    logging.error(f"Command failed with exit code {output.returncode}")
                    logging.debug(f"Error output:\n{output.stderr}")
                    return False, output
            except subprocess.CalledProcessError as e:
                logging.error(f"Command '{e.cmd}' returned non-zero exit status {e.returncode}.")
                logging.debug(f"Error output:\n{e.stderr}")
                return False, e
        
        if command == "ls":
            output = subprocess.run("mega-ls", shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            ls = ["/" + line for line in output.stdout.split("\n") if line]
            return ls

        return False, "Invalid command or argument"

    def cleanup(self):
        """
        Cleanup any temporary files or resources.
        """
        for list in self.run("ls"):
            self.run("rm", list)
        
class RaindropIO:
    api = API(os.environ.get("RAINDROP_TOKEN", "dccba67d-e10a-4db0-9148-5229dc7c6684"))
    def __init__(self):
        pass
    

    def get_content(self, collection_id: str):
        '''
        params: collection_id, Path parameter that specify from which collection to get raindrops.
            0 to get all (except Trash)
            -1 to get from "Unsorted"
            -99 to get from "Trash"
        '''
        page = 0
        while (item := Raindrop.search(self.api, collection=CollectionRef({'$id': collection_id}), page=page, perpage=5)):
            yield item  # API by default gives 50 search results per page
            page += 1
            time.sleep(1)  # to avoid hitting API rate limits


    def search_collection(self, name: str):
        # check for root collections``
        for c in Collection.get_roots(self.api):
            if name in c.title:
                return c
        # check for children collections
        for c in Collection.get_childrens(self.api):
            if name in c.title:
                return c


    def get_bookmarks(self, name="all"):
        '''
        Get collection contenet by name
        '''
        id = "0"
        if name == "all":
            id = "0"
        elif name == "unsorted":
            id = "-1"
        elif name == "trash":
            id = "-99"
        else:
            id = self.search_collection(name).id
        return self.get_content(id)


    def get_all_collections(self):
        logging.info("Getting all collections")
        ids = []
        for collection in Collection.get_roots(self.api):
            ids.append((collection.id, collection.title))
        for collection in Collection.get_childrens(self.api):
            ids.append((collection.id, collection.title))
        return ids
    
    def delete_bookmark(self, id):
        Raindrop.remove(self.api, id)
        logging.info(f"Deleted bookmark {id}")
        return True

if __name__ == "__main__":
    mega = MegaCMD()
    # print(mega.check("https://mega.nz/folder/Bn8TBKAY#h4JDaPDqHHlZ4HnRGGMLVw"))
    # Example usage
    # success, output = mega.run("import", "https://mega.nz/folder/Bn8TBKAY#h4JDaPDqHHlZ4HnRGGMLVw")
    # success, output = mega.run("df")
    # success, output = mega.run("rm", "/Victoriae Barret  @OnlyFamOFLeaks TELEGRAM")
    # print(success, output)

    rain = RaindropIO()
    # print(raindrop.get_all_collections())
    # rain.delete_bookmark("878573702")

    for collection in rain.get_bookmarks("SiteRips"):
        for link in collection:
            if link.link.startswith("https://mega.nz/"):
                if mega.check(link.link) == False:
                    logging.info(f"Invalid Link : {link.title} - {link.link}")
                    rain.delete_bookmark(link.id)
            else:
                logging.debug(f"Not a mega link : {link.title} - {link.link}")
        mega.cleanup()
    logging.info("Finished")
