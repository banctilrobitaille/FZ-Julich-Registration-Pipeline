import os

from factories import CoRegistrationProcessFactory
from file_utils import FileUtils


def main(subjects_folder_path, masks_folder_path, template_path, output_folder):
    subjects = FileUtils.get_files_name_in(subjects_folder_path)
    masks = FileUtils.get_files_name_in(masks_folder_path)

    for subject in subjects:
        patient_id = FileUtils.extract_patient_id_from(subject)
        subject_folder = os.path.join(output_folder, patient_id)

        # Register the template to the subject space
        CoRegistrationProcessFactory.create_co_registration_process_with(template_path, subject, subject_folder).run()
        for mask in masks:
            transformation_matrix_path = \
                CoRegistrationProcessFactory.get_transformation_matrix_file_name_from(subject_folder, template_path)

            # Register the mask to the subject space using the transformation matrix
            CoRegistrationProcessFactory \
                .create_co_registration_process_with(mask, subject, subject_folder, transformation_matrix_path).run()


if __name__ == "__main__":
    main("data/pet", "data/masks", "data/template/MNI152lin_T1_2mm.nii", "output")
