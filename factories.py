import os

from nipype.interfaces.fsl import ApplyXFM


class CoRegistrationProcessFactory:
    REG_OUTPUT_PREFIX = "reg_"
    TRANSFORM_MAT_PREFIX = "mat_"
    TRANSFORM_MAT_EXT = ".mat"

    @staticmethod
    def create_co_registration_process_with(file_to_register,
                                            reference_file,
                                            output_folder,
                                            transformation_matrix_file=None):
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # The registered output file path
        output_registered_image = os.path.join(output_folder, CoRegistrationProcessFactory.REG_OUTPUT_PREFIX +
                                               CoRegistrationProcessFactory.extract_file_name_from(
                                                   file_to_register, with_extension=True) + ".gz")
        # Creating the FLIRT process
        co_registration_process = ApplyXFM()
        co_registration_process.inputs.in_file = file_to_register
        co_registration_process.inputs.reference = reference_file
        co_registration_process.inputs.out_file = output_registered_image
        co_registration_process.inputs.out_matrix_file = \
            CoRegistrationProcessFactory.get_transformation_matrix_file_name_from(output_folder, file_to_register)

        # Apply the transformation matrix if provided
        if transformation_matrix_file:
            co_registration_process.inputs.apply_xfm = True
            co_registration_process.inputs.in_matrix_file = transformation_matrix_file
        else:
            co_registration_process.inputs.apply_xfm = False

        return co_registration_process

    @staticmethod
    def extract_file_name_from(path, with_extension):
        return os.path.split(path)[1] if with_extension else os.path.splitext(os.path.split(path)[1])[0]

    @staticmethod
    def get_transformation_matrix_file_name_from(output_folder, file_to_register):
        return os.path.join(output_folder,
                            CoRegistrationProcessFactory.TRANSFORM_MAT_PREFIX +
                            CoRegistrationProcessFactory.extract_file_name_from(file_to_register,
                                                                                with_extension=False) +
                            CoRegistrationProcessFactory.TRANSFORM_MAT_EXT)
