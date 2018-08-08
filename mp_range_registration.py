import os

from factories import CoRegistrationProcessFactory
from file_utils import FileUtils


def main(mp_rage_images_folder, pet_images_folder, segmented_regions_folder, output_folder):
    mp_rage_images = FileUtils.get_files_name_in(mp_rage_images_folder)

    for mp_rage_image in mp_rage_images:
        try:
            patient_id = FileUtils.extract_patient_id_from(mp_rage_image)
            pet_image = FileUtils.get_file_of_patient_with_id_from_folder(patient_id, pet_images_folder)
            subject_folder = os.path.join(output_folder, patient_id)

            # Register the mp rage to the pet space
            CoRegistrationProcessFactory.create_co_registration_process_with(mp_rage_image, pet_image, subject_folder).run()

            segmented_regions_image = FileUtils.get_file_of_patient_with_id_from_folder(patient_id,segmented_regions_folder)

            transformation_matrix_path = \
                CoRegistrationProcessFactory.get_transformation_matrix_file_name_from(subject_folder, mp_rage_image)

            # Register the mask to the subject space using the transformation matrix
            CoRegistrationProcessFactory \
                .create_co_registration_process_with(segmented_regions_image, pet_image, subject_folder,
                                                     transformation_matrix_path).run()
        except IndexError as e:
            print("Unable to read file for patient with id {}".format(patient_id))


if __name__ == "__main__":
    main("data/mp_rage", "data/pet", "data/segmented_regions", "output")
