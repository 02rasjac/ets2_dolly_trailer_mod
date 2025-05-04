import os
import argparse

# Set up arguments
parser = argparse.ArgumentParser()
# parser.add_argument("scs_packer", help="Path to scs_packer executable")
parser.add_argument("game_archive", help="Path to the *extracted* game archive")
parser.add_argument("--trailer_defs", action="store_true", help="Generate trailer definitions in base/def/vehicle/trailes_defs")
parser.add_argument("--trailer_owned", action="store_true", help="Generate trailer configurations in base/def/vehicle/trailes_owned/scs.<traile_type>/configurations")
args = parser.parse_args()

# Configs
VEHICLE_PATH = args.game_archive + r"\def\vehicle"
TRAILER_OWNED_PATH = VEHICLE_PATH + r"\trailer_owned"
TRAILER_DEFS_PATH = VEHICLE_PATH + r"\trailer_defs"

DOLLY_WEIGHT = 2800
DOLLY_AXLES = 2
DOLLY_CHASSIS = "/def/vehicle/trailer_owned/scs.flatbed/chassis/dolly_conv_long.sii"

def main():
    if args.trailer_defs:
        generate_trailer_defs()
    if args.trailer_owned:
        generate_trailer_configs()


def generate_trailer_defs():
    directory = os.fsencode(TRAILER_DEFS_PATH)
    for file in os.listdir(directory):
        filename = os.fsdecode(file)

        # Doubles, B-doubles and HCT does not need a dolly inserted
        if "single" in filename:
            new_string = ""
            with open(os.path.join(TRAILER_DEFS_PATH, filename), "r") as from_file:
                lines = from_file.readlines()
                dolly_mass_ratio = 0
                for line in lines:
                    new_line = line.replace("single", "dolly")
                    split_new_line = new_line.split(": ")
                    if "chassis_mass" in new_line:
                        trailer_mass = split_new_line[1]
                        new_mass = int(trailer_mass) + DOLLY_WEIGHT
                        dolly_mass_ratio = DOLLY_WEIGHT / new_mass
                        split_new_line[1] = str(new_mass) + "\n"
                    elif "axles" in new_line:
                        axles = split_new_line[1]
                        split_new_line[1] = str(int(axles) + DOLLY_AXLES) + "\n"
                    elif "mass_ratio" in new_line:
                        new_string += f"\tmass_ratio[]: {dolly_mass_ratio:.2f}\n" 
                        split_new_line[1] = f"{(1-dolly_mass_ratio):.2f}\n"
                    new_string += ": ".join(split_new_line)

                with open(os.path.join("./mod/base/def/vehicle/trailer_defs", filename.replace("single", "dolly")), "w") as to_file:
                    to_file.write(new_string)

def generate_trailer_configs():
    for trailer_type_folder in os.listdir(os.fsencode(TRAILER_OWNED_PATH)):
        configuration_path = os.path.join(TRAILER_OWNED_PATH, os.fsdecode(trailer_type_folder), "configurations")
        if os.fsdecode(trailer_type_folder).endswith(".sii"):
            continue

        for filename in os.listdir(configuration_path):
            # Doubles, B-doubles and HCT does not need a dolly inserted
            if "single" in filename:
                # Modify the main files first (directly under /configurations)
                if os.fsdecode(filename).endswith(".sii"):
                    new_string = ""
                    with open(os.path.join(configuration_path, os.fsdecode(filename)), "r") as from_file:
                        lines = from_file.readlines()
                        for line in lines:
                            # Don't change icon name since there is no dolly icon
                            if "icon" in line.split(": ")[0]:
                                new_string += line
                                continue

                            new_line = line.replace("single", "dolly")
                            split_new_line = new_line.split(": ")
                            if "chassis[]" in new_line:
                                new_string += f"\tchassis[]: \"/def/vehicle/trailer_owned/{os.fsdecode(trailer_type_folder)}/chassis/dolly_conv_long.sii\"\n" 
                            new_string += ": ".join(split_new_line)

                    # Create directory if it doesn't exist
                    mod_file_name = os.path.join("./mod/base/def/vehicle/trailer_owned", os.fsdecode(trailer_type_folder), "configurations", filename.replace("single", "dolly"))
                    os.makedirs(os.path.dirname(mod_file_name), exist_ok=True)

                    # Write the modded file
                    with open(mod_file_name, "w") as to_file:
                        to_file.write(new_string)
                # Modify the bodytypes (/configurations/single_* -> /configurations/dolly_*)
                else:
                    for body_file_name in os.listdir(os.path.join(configuration_path, os.fsdecode(filename))):
                        new_string = ""
                        with open(os.path.join(configuration_path, os.fsdecode(filename), os.fsdecode(body_file_name)), "r") as from_file:
                            lines = from_file.readlines()
                            for line in lines:
                                new_line = line.replace("single", "dolly")
                                split_new_line = new_line.split(": ")
                                if "body[]" in new_line:
                                    new_string += f"\tbody[]: \"\"\n" 
                                new_string += ": ".join(split_new_line)

                        # Create directory if it doesn't exist
                        mod_file_name = os.path.join("./mod/base/def/vehicle/trailer_owned", os.fsdecode(trailer_type_folder), "configurations", filename.replace("single", "dolly"), os.fsdecode(body_file_name))
                        os.makedirs(os.path.dirname(mod_file_name), exist_ok=True)

                        # Write the modded file
                        with open(mod_file_name, "w") as to_file:
                            to_file.write(new_string)



main()