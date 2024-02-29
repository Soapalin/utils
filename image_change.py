from PIL import Image
import os

def resize_images(folder_path):
    # Check if the provided path is a valid directory
    if not os.path.isdir(folder_path):
        print(f"Error: '{folder_path}' is not a valid directory.")
        return

    # Get a list of files in the specified directory
    file_list = os.listdir(folder_path)

    # Iterate through each file in the directory
    for file_name in file_list:
        # Create the full file path
        file_path = os.path.join(folder_path, file_name)

        # Check if the file is an image (you can add more image extensions if needed)
        if file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            try:
                # Open the image file
                with Image.open(file_path) as img:
                    # Get the original dimensions
                    width, height = img.size

                    # Resize the image by 50%
                    new_width = int(width * 0.4)
                    new_height = int(height * 0.4)
                    resized_img = img.resize((new_width, new_height))

                    # Save the resized image, overwrite the original file
                    resized_img.save(file_path)
                    print(f"Resized: {file_name}")

            except Exception as e:
                print(f"Error processing {file_name}: {e}")

    print("Image resizing complete.")

# Example usage:
folder_name = "C:\Sandbox\Learn Python\\test"
resize_images(folder_name)
