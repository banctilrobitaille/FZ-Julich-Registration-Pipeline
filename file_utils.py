import os
import re


class FileUtils(object):
    @staticmethod
    def get_files_name_in(folder):
        return list(map(lambda file: os.path.join(folder, file), os.listdir(folder)))

    @staticmethod
    def extract_patient_id_from(file_name):
        m = re.search("AB[0-9]_[0-9]{2}", file_name)
        return m.group(0)

    @staticmethod
    def get_file_of_patient_with_id_from_folder(patient_id, folder):
        return list(filter(lambda file_name: patient_id in file_name,
                           FileUtils.get_files_name_in(folder)))[0]
